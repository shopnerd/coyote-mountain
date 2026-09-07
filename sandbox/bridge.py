"""coyote mountain sandbox bridge

Reads depth frames from an Orbbec Femto Bolt (through Orbbec's Kinect-compatible k4a.dll) and serves them to the
topo tool over plain HTTP on this machine. The browser does everything else: calibration, contours, water, projection.

  python bridge.py --mode k4a --dll "C:/path/to/OrbbecSDK_K4A_Wrapper/bin"     the camera
  python bridge.py --mode fake                                                 invented dunes that drift, for building without a camera
  python bridge.py --mode replay --file frame.bin                              a saved frame (GET /snap saves one)

Then in the topo tool press "sandbox · live". Needs Python 3.9+ and numpy. Nothing else.

Endpoints (all allow any origin):
  /info        {"w":160,"h":144,"mode":"k4a","fps":10,"units":"mm"}
  /depth       little-endian uint16 depth in mm, w*h values, row 0 = the top of the sensor image, 0 = no reading
  /snap        saves the current frame next to this script as frame-<n>.bin and returns its name
"""
import argparse, ctypes, json, os, sys, threading, time, math
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler

try:
    import numpy as np
except ImportError:
    sys.exit('numpy is needed: python -m pip install numpy')

ap = argparse.ArgumentParser()
ap.add_argument('--mode', default='fake', choices=['k4a', 'fake', 'replay'])
ap.add_argument('--dll', default='', help='folder holding k4a.dll, depthengine_2_0.dll and OrbbecSDK.dll from the Orbbec K4A wrapper')
ap.add_argument('--port', type=int, default=8787)
ap.add_argument('--fps', type=float, default=10)
ap.add_argument('--out', type=int, default=160, help='served frame width in pixels; height follows the sensor aspect')
ap.add_argument('--wide', action='store_true', help='use the wide field of view (1024x1024 at 15 fps) instead of narrow (640x576 at 30 fps)')
ap.add_argument('--file', default='', help='replay: a frame saved by /snap')
ap.add_argument('--avg', type=int, default=4, help='frames averaged before serving')
A = ap.parse_args()

latest = {'frame': None, 'w': 0, 'h': 0, 'n': 0, 'src_w': 0, 'src_h': 0, 'err': ''}
lock = threading.Lock()

def downsample(depth):                    # mean of the valid readings in each block; 0 where a block has none
    h, w = depth.shape; ow = A.out; oh = max(1, round(h * ow / w)); by, bx = h // oh, w // ow
    if by < 1 or bx < 1: return depth.astype(np.uint16)
    d = depth[:oh * by, :ow * bx].reshape(oh, by, ow, bx).astype(np.float32)
    valid = d > 0; s = (d * valid).sum(axis=(1, 3)); n = valid.sum(axis=(1, 3))
    out = np.where(n > 0, s / np.maximum(n, 1), 0); return out.astype(np.uint16)

def publish(frames):                      # temporal average of the last few frames (invalid readings left out), then serve
    st = np.stack(frames).astype(np.float32); valid = st > 0; s = (st * valid).sum(axis=0); n = valid.sum(axis=0)
    avg = np.where(n > 0, s / np.maximum(n, 1), 0).astype(np.uint16); small = downsample(avg)
    with lock:
        latest['frame'] = small.tobytes(); latest['w'] = int(small.shape[1]); latest['h'] = int(small.shape[0]); latest['n'] += 1; latest['src_w'] = int(avg.shape[1]); latest['src_h'] = int(avg.shape[0])

# ---------- the camera, through the K4A C API in ctypes ----------
class K4AConfig(ctypes.Structure):
    _fields_ = [('color_format', ctypes.c_int), ('color_resolution', ctypes.c_int), ('depth_mode', ctypes.c_int), ('camera_fps', ctypes.c_int),
                ('synchronized_images_only', ctypes.c_bool), ('depth_delay_off_color_usec', ctypes.c_int32), ('wired_sync_mode', ctypes.c_int),
                ('subordinate_delay_off_master_usec', ctypes.c_uint32), ('disable_streaming_indicator', ctypes.c_bool)]

def run_k4a():
    folder = A.dll or os.path.dirname(os.path.abspath(__file__))
    if hasattr(os, 'add_dll_directory'): os.add_dll_directory(folder)
    try: k = ctypes.CDLL(os.path.join(folder, 'k4a.dll'))
    except OSError as e: latest['err'] = f'could not load k4a.dll from {folder}: {e}. put the Orbbec K4A wrapper DLLs there (k4a.dll, depthengine_2_0.dll, OrbbecSDK.dll)'; print(latest['err']); return
    H = ctypes.c_void_p
    k.k4a_device_open.argtypes = [ctypes.c_uint32, ctypes.POINTER(H)]; k.k4a_device_start_cameras.argtypes = [H, ctypes.POINTER(K4AConfig)]
    k.k4a_device_get_capture.argtypes = [H, ctypes.POINTER(H), ctypes.c_int32]; k.k4a_capture_get_depth_image.argtypes = [H]; k.k4a_capture_get_depth_image.restype = H
    k.k4a_image_get_buffer.argtypes = [H]; k.k4a_image_get_buffer.restype = ctypes.POINTER(ctypes.c_uint16)
    for f in ('k4a_image_get_width_pixels', 'k4a_image_get_height_pixels', 'k4a_image_get_stride_bytes'): getattr(k, f).argtypes = [H]; getattr(k, f).restype = ctypes.c_int
    k.k4a_image_release.argtypes = [H]; k.k4a_capture_release.argtypes = [H]; k.k4a_device_stop_cameras.argtypes = [H]; k.k4a_device_close.argtypes = [H]
    dev = H()
    if k.k4a_device_open(0, ctypes.byref(dev)) != 0: latest['err'] = 'no depth camera found (k4a_device_open failed). is the Femto Bolt on USB 3 and its firmware 1.1.2 or newer?'; print(latest['err']); return
    cfg = K4AConfig(color_format=0, color_resolution=0, depth_mode=4 if A.wide else 2, camera_fps=1 if A.wide else 2, synchronized_images_only=False, depth_delay_off_color_usec=0, wired_sync_mode=0, subordinate_delay_off_master_usec=0, disable_streaming_indicator=False)
    if k.k4a_device_start_cameras(dev, ctypes.byref(cfg)) != 0: latest['err'] = 'the camera opened but would not start streaming'; print(latest['err']); k.k4a_device_close(dev); return
    print('camera streaming', 'wide' if A.wide else 'narrow'); frames = []; period = 1 / A.fps; last = 0
    try:
        while True:
            cap = H()
            if k.k4a_device_get_capture(dev, ctypes.byref(cap), 1000) != 0: continue
            img = k.k4a_capture_get_depth_image(cap)
            if img:
                w, h, stride = k.k4a_image_get_width_pixels(img), k.k4a_image_get_height_pixels(img), k.k4a_image_get_stride_bytes(img)
                buf = k.k4a_image_get_buffer(img); arr = np.ctypeslib.as_array(buf, shape=(h, stride // 2))[:, :w].copy(); k.k4a_image_release(img)
                frames.append(arr); frames = frames[-A.avg:]
            k.k4a_capture_release(cap)
            if time.time() - last >= period and frames: publish(frames); last = time.time()
    finally:
        k.k4a_device_stop_cameras(dev); k.k4a_device_close(dev)

# ---------- invented dunes, so the tool can be built and demonstrated without the camera ----------
def run_fake():
    w, h = 640, 576; yy, xx = np.mgrid[0:h, 0:w].astype(np.float32); t0 = time.time()
    def hills(t):
        a = np.sin(xx / 90 + t * .05) * np.cos(yy / 70 - t * .04) + .5 * np.sin(xx / 37 + yy / 41 + t * .1) + .3 * np.cos(yy / 23 - t * .07)
        mound = np.exp(-(((xx - w * (.5 + .25 * math.sin(t * .09))) ** 2 + (yy - h * .5) ** 2) / (2 * 90 ** 2))) * 2.2
        return 1000 - (a * 25 + 60 + mound * 60)   # floor about 1 m from the sensor; sand rises toward the camera, so depth falls
    while True:
        t = time.time() - t0; d = hills(t)
        if int(t) % 12 == 5: d[(xx - w * .3) ** 2 + (yy - h * .3) ** 2 < 60 ** 2] = 480   # a hand over the box for a second, well above the sand
        d += np.random.normal(0, 1.5, d.shape); d[np.random.rand(h, w) < .002] = 0
        publish([d.astype(np.uint16)]); time.sleep(1 / A.fps)

def run_replay():
    raw = open(A.file, 'rb').read(); hdr = json.loads(raw[:raw.index(b'\n')]); arr = np.frombuffer(raw[raw.index(b'\n') + 1:], dtype=np.uint16).reshape(hdr['h'], hdr['w'])
    while True: publish([arr]); time.sleep(1 / A.fps)

class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def _send(self, code, ctype, body):
        self.send_response(code); self.send_header('Content-Type', ctype); self.send_header('Access-Control-Allow-Origin', '*'); self.send_header('Cache-Control', 'no-store'); self.send_header('Content-Length', str(len(body))); self.end_headers(); self.wfile.write(body)
    def do_GET(self):
        with lock: fr, w, h, n, err = latest['frame'], latest['w'], latest['h'], latest['n'], latest['err']
        if self.path.startswith('/info'): self._send(200, 'application/json', json.dumps({'w': w, 'h': h, 'mode': A.mode, 'fps': A.fps, 'units': 'mm', 'frames': n, 'source': [latest['src_w'], latest['src_h']], 'error': err}).encode())
        elif self.path.startswith('/depth'): self._send(200, 'application/octet-stream', fr) if fr else self._send(503, 'text/plain', (err or 'no frame yet').encode())
        elif self.path.startswith('/snap'):
            if not fr: return self._send(503, 'text/plain', b'no frame yet')
            k = 1
            while os.path.exists(f'frame-{k}.bin'): k += 1
            with open(f'frame-{k}.bin', 'wb') as f: f.write(json.dumps({'w': w, 'h': h}).encode() + b'\n' + fr)
            self._send(200, 'text/plain', f'frame-{k}.bin'.encode())
        else: self._send(404, 'text/plain', b'/info /depth /snap')

threading.Thread(target={'k4a': run_k4a, 'fake': run_fake, 'replay': run_replay}[A.mode], daemon=True).start()
print(f'sandbox bridge · mode {A.mode} · http://localhost:{A.port}/depth · ctrl+c stops')
try: ThreadingHTTPServer(('127.0.0.1', A.port), Handler).serve_forever()
except KeyboardInterrupt: pass
