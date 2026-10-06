"""coyote mountain sandbox bridge

Reads depth frames from a depth camera and serves them to the topo tool over plain HTTP on this machine. The browser does
everything else: calibration, contours, water, projection.

  python bridge.py --mode k4a --dll "C:/path/to/OrbbecSDK_K4A_Wrapper/bin"     Orbbec Femto Bolt / Mega, Azure Kinect (k4a.dll)
  python bridge.py --mode kinect1 [--dll folder]                               Kinect v1 (Xbox 360): libfreenect, or the Kinect SDK 1.8 on Windows
  python bridge.py --mode orbbec [--dll folder]                                Orbbec Astra / Gemini / Femto: pyorbbecsdk, or OpenNI2 for older Astras
  python bridge.py --mode fake                                                 invented dunes that drift, for building without a camera
  python bridge.py --mode replay --file frame.bin                              a saved frame (GET /snap saves one)

Then in the topo tool press "sandbox · live". Needs Python 3.9+ and numpy, plus the camera's own driver (see README.md).

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
ap.add_argument('--mode', default='fake', choices=['k4a', 'kinect1', 'orbbec', 'fake', 'replay'])
ap.add_argument('--dll', default='', help='k4a: folder with k4a.dll from the Orbbec K4A wrapper · kinect1: folder with freenect_sync or Kinect10.dll · orbbec: the OpenNI2 Redist folder (older Astras)')
ap.add_argument('--port', type=int, default=8787)
ap.add_argument('--fps', type=float, default=10)
ap.add_argument('--out', type=int, default=160, help='served frame width in pixels; height follows the sensor aspect')
ap.add_argument('--wide', action='store_true', help='use the wide field of view (1024x1024 at 15 fps) instead of narrow (640x576 at 30 fps)')
ap.add_argument('--file', default='', help='replay: a frame saved by /snap')
ap.add_argument('--avg', type=int, default=4, help='frames averaged before serving')
A = ap.parse_args()

latest = {'frame': None, 'w': 0, 'h': 0, 'n': 0, 'src_w': 0, 'src_h': 0, 'err': '', 'backend': ''}
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

# ---------- a camera loop shared by the kinect1 and orbbec modes: grab() returns depth in mm (uint16, 0 = no reading) or None ----------
def stream(grab, close, label):
    print('camera streaming ·', label); latest['backend'] = label; frames = []; period = 1 / A.fps; last = 0
    try:
        while True:
            d = grab()
            if d is None: continue
            frames.append(d); frames = frames[-A.avg:]
            if time.time() - last >= period: publish(frames); last = time.time()
    finally:
        try: close()
        except Exception: pass

def fail(msg): latest['err'] = msg; print(msg)

# ---------- Kinect v1 (Xbox 360, models 1414 / 1473; Kinect for Windows 1517): libfreenect anywhere, or Microsoft's Kinect SDK 1.8 on Windows ----------
def kinect1_freenect():                   # libfreenect's sync wrapper: one call per frame, depth already in mm
    import ctypes.util
    names = ['freenect_sync.dll', 'libfreenect_sync.dll', 'libfreenect_sync.so.0', 'libfreenect_sync.so', 'libfreenect_sync.dylib', 'libfreenect_sync.0.dylib']
    tries = [os.path.join(A.dll, n) for n in names] if A.dll else []
    tries += names + [p for p in [ctypes.util.find_library('freenect_sync')] if p]
    lib = None
    for t in tries:
        try: lib = ctypes.CDLL(t); break
        except OSError: continue
    if not lib: return None
    lib.freenect_sync_get_depth.argtypes = [ctypes.POINTER(ctypes.c_void_p), ctypes.POINTER(ctypes.c_uint32), ctypes.c_int, ctypes.c_int]; lib.freenect_sync_get_depth.restype = ctypes.c_int
    buf, ts = ctypes.c_void_p(), ctypes.c_uint32()
    if lib.freenect_sync_get_depth(ctypes.byref(buf), ctypes.byref(ts), 0, 5) != 0:   # 5 = FREENECT_DEPTH_MM
        fail('libfreenect loaded but found no Kinect. is it plugged into its power adapter, and (on Windows) is its "Xbox NUI Camera" given the libusbK driver with Zadig?'); return False
    def grab():
        if lib.freenect_sync_get_depth(ctypes.byref(buf), ctypes.byref(ts), 0, 5) != 0: time.sleep(.05); return None
        return np.ctypeslib.as_array(ctypes.cast(buf, ctypes.POINTER(ctypes.c_uint16)), shape=(480, 640)).copy()
    stream(grab, lambda: lib.freenect_sync_stop(), 'kinect v1 through libfreenect'); return True

class NuiViewArea(ctypes.Structure): _fields_ = [('eDigitalZoom', ctypes.c_int), ('lCenterX', ctypes.c_long), ('lCenterY', ctypes.c_long)]
class NuiImageFrame(ctypes.Structure): _fields_ = [('liTimeStamp', ctypes.c_int64), ('dwFrameNumber', ctypes.c_uint32), ('eImageType', ctypes.c_int), ('eResolution', ctypes.c_int), ('pFrameTexture', ctypes.c_void_p), ('dwFrameFlags', ctypes.c_uint32), ('ViewArea', NuiViewArea)]
class NuiLockedRect(ctypes.Structure): _fields_ = [('Pitch', ctypes.c_int), ('size', ctypes.c_int), ('pBits', ctypes.c_void_p)]

def kinect1_nui():                        # Microsoft's Kinect for Windows SDK 1.8 (Kinect10.dll); the depth texture is a COM object, reached through its vtable
    if os.name != 'nt': return None
    try: nui = ctypes.WinDLL(os.path.join(A.dll, 'Kinect10.dll') if A.dll and os.path.isfile(os.path.join(A.dll, 'Kinect10.dll')) else 'Kinect10.dll')
    except OSError: return None
    H = ctypes.c_void_p; F = ctypes.POINTER(NuiImageFrame)
    nui.NuiInitialize.argtypes = [ctypes.c_uint32]; nui.NuiImageStreamOpen.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_uint32, ctypes.c_uint32, H, ctypes.POINTER(H)]
    nui.NuiImageStreamGetNextFrame.argtypes = [H, ctypes.c_uint32, ctypes.POINTER(F)]; nui.NuiImageStreamReleaseFrame.argtypes = [H, F]
    for f in ('NuiInitialize', 'NuiImageStreamOpen', 'NuiImageStreamGetNextFrame', 'NuiImageStreamReleaseFrame'): getattr(nui, f).restype = ctypes.c_long
    if nui.NuiInitialize(0x20) < 0:          # NUI_INITIALIZE_FLAG_USES_DEPTH
        fail('the Kinect SDK loaded but found no Kinect. is it on its power adapter and showing in Device Manager under "Kinect for Windows"?'); return False
    st = H()
    if nui.NuiImageStreamOpen(4, 2, 0, 2, None, ctypes.byref(st)) < 0:   # NUI_IMAGE_TYPE_DEPTH, 640x480, two frames buffered
        fail('the Kinect opened but its depth stream would not start'); nui.NuiShutdown(); return False
    LOCK = ctypes.WINFUNCTYPE(ctypes.c_long, H, ctypes.c_uint, ctypes.POINTER(NuiLockedRect), H, ctypes.c_uint32); UNLOCK = ctypes.WINFUNCTYPE(ctypes.c_long, H, ctypes.c_uint)
    def grab():
        fr = F()
        if nui.NuiImageStreamGetNextFrame(st, 1000, ctypes.byref(fr)) < 0: return None
        try:
            tex = fr.contents.pFrameTexture; vt = ctypes.cast(ctypes.cast(tex, ctypes.POINTER(ctypes.c_void_p))[0], ctypes.POINTER(ctypes.c_void_p))   # INuiFrameTexture: IUnknown(3), BufferLen, Pitch, LockRect = 5, GetLevelDesc, UnlockRect = 7
            lr = NuiLockedRect()
            if LOCK(vt[5])(tex, 0, ctypes.byref(lr), None, 0) < 0 or not lr.pBits: return None
            try: raw = np.ctypeslib.as_array(ctypes.cast(lr.pBits, ctypes.POINTER(ctypes.c_uint16)), shape=(480, lr.Pitch // 2))[:, :640].copy()
            finally: UNLOCK(vt[7])(tex, 0)
        finally: nui.NuiImageStreamReleaseFrame(st, fr)
        nz = raw[raw > 0]
        return (raw >> 3) if nz.size and np.median(nz) > 4500 else raw   # SDK 1.x packs depth in the top 13 bits (a player index below); a sandbox is never 4.5 m away, so a median that high means packed
    stream(grab, lambda: nui.NuiShutdown(), 'kinect v1 through the Kinect for Windows SDK'); return True

def run_kinect1():
    tried = []
    for backend in (kinect1_freenect, kinect1_nui):
        r = backend(); tried.append(r)
        if r: return
    if not any(r is False for r in tried): fail('no Kinect v1 driver found. install either libfreenect (Linux: apt install libfreenect-dev; macOS: brew install libfreenect; Windows: build it, then give the camera the libusbK driver with Zadig) '
         'and point --dll at the folder holding freenect_sync, or on Windows the Kinect for Windows SDK 1.8 (Kinect10.dll). see sandbox/README.md')

# ---------- Orbbec (Astra, Gemini, Femto): Orbbec's SDK in Python, or OpenNI2 for older Astras ----------
def orbbec_sdk():                         # pyorbbecsdk2 (SDK v2: Femto, Gemini 330, Astra 2 …) or pyorbbecsdk 1.x (Astra+, Astra Pro Plus, Gemini 2 XL); both import as pyorbbecsdk
    try: import pyorbbecsdk as ob
    except ImportError: return None
    try:   # count first: pyorbbecsdk2 2.1.2 takes the whole process down (heap corruption, 0xc0000374) if Pipeline() is made with no camera attached
        n = ob.Context().query_devices().get_count()
    except Exception: n = -1
    if n == 0:
        fail('the Orbbec SDK sees no camera. is it on USB (a USB 3 port for the Femto and Gemini cameras)? an Astra+ or Astra Pro Plus needs pyorbbecsdk 1.x (Python 3.11 or older), not pyorbbecsdk2; an older Astra like the Mini S needs OpenNI2 (see README)'); return False
    try:
        pipe = ob.Pipeline(); cfg = ob.Config(); plist = pipe.get_stream_profile_list(ob.OBSensorType.DEPTH_SENSOR)
        try: prof = plist.get_video_stream_profile(640, 0, ob.OBFormat.Y16, 30)
        except Exception: prof = plist.get_default_video_stream_profile()
        cfg.enable_stream(prof); pipe.start(cfg)
    except Exception as e:
        fail(f'the Orbbec SDK found no camera it supports ({e}). is the camera on USB? an Astra+ or Astra Pro Plus needs pyorbbecsdk 1.x (Python 3.11 or older), not pyorbbecsdk2; an older Astra like the Mini S may need OpenNI2 instead (see README)'); return False
    def grab():
        fs = pipe.wait_for_frames(1000); df = fs.get_depth_frame() if fs else None
        if df is None: return None
        w, h, sc = df.get_width(), df.get_height(), float(df.get_depth_scale() or 1)
        d = np.frombuffer(df.get_data(), dtype=np.uint16).reshape(h, w)
        return d.copy() if abs(sc - 1) < 1e-6 else np.clip(d.astype(np.float32) * sc, 0, 65535).astype(np.uint16)   # some cameras count in 0.1 or 0.125 mm
    stream(grab, pipe.stop, 'orbbec through the Orbbec SDK'); return True

def orbbec_openni():                      # OpenNI2 with Orbbec's redistributable (older Astra, Astra Mini S): pip install openni, --dll = the OpenNI2 Redist folder
    try: from openni import openni2
    except ImportError: return None
    try:
        openni2.initialize(A.dll or None); dev = openni2.Device.open_any(); ds = dev.create_depth_stream(); ds.start()
    except Exception as e:
        fail(f'OpenNI2 found no camera ({e}). point --dll at the folder holding OpenNI2.dll from Orbbec\'s OpenNI2 package'); return False
    def grab():
        f = ds.read_frame(); return np.ctypeslib.as_array(f.get_buffer_as_uint16()).reshape(f.height, f.width).copy()
    stream(grab, lambda: (ds.stop(), openni2.unload()), 'orbbec through OpenNI2'); return True

def run_orbbec():
    tried = []
    for backend in (orbbec_sdk, orbbec_openni):
        r = backend(); tried.append(r)
        if r: return
    if not any(r is False for r in tried):
        fail('no Orbbec driver found. for most cameras: python -m pip install pyorbbecsdk2 (Python 3.8 to 3.13). for an Astra+ or Astra Pro Plus: pyorbbecsdk (1.x, Python 3.11 or older). for an older Astra or Mini S: pip install openni plus Orbbec\'s OpenNI2 package. see sandbox/README.md')

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
        if self.path.startswith('/info'): self._send(200, 'application/json', json.dumps({'w': w, 'h': h, 'mode': A.mode, 'fps': A.fps, 'units': 'mm', 'frames': n, 'source': [latest['src_w'], latest['src_h']], 'camera': latest['backend'], 'error': err}).encode())
        elif self.path.startswith('/depth'): self._send(200, 'application/octet-stream', fr) if fr else self._send(503, 'text/plain', (err or 'no frame yet').encode())
        elif self.path.startswith('/snap'):
            if not fr: return self._send(503, 'text/plain', b'no frame yet')
            k = 1
            while os.path.exists(f'frame-{k}.bin'): k += 1
            with open(f'frame-{k}.bin', 'wb') as f: f.write(json.dumps({'w': w, 'h': h}).encode() + b'\n' + fr)
            self._send(200, 'text/plain', f'frame-{k}.bin'.encode())
        else:   # the tool itself, served from the folder above this script, so the sandbox runs offline from http://localhost:8787/topo.html
            name = self.path.split('?')[0].lstrip('/') or 'index.html'; root = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); full = os.path.normpath(os.path.join(root, name))
            ext = name.split('.')[-1].lower(); types = {'html': 'text/html; charset=utf-8', 'json': 'application/json', 'md': 'text/plain; charset=utf-8', 'py': 'text/plain', 'txt': 'text/plain', 'js': 'text/javascript; charset=utf-8', 'css': 'text/css', 'png': 'image/png', 'jpg': 'image/jpeg', 'webmanifest': 'application/manifest+json'}
            if not full.startswith(root) or not os.path.isfile(full) or ext not in types: return self._send(404, 'text/plain', b'/info /depth /snap, or topo.html')
            ctype = types[ext]
            with open(full, 'rb') as f: self._send(200, ctype, f.read())

threading.Thread(target={'k4a': run_k4a, 'kinect1': run_kinect1, 'orbbec': run_orbbec, 'fake': run_fake, 'replay': run_replay}[A.mode], daemon=True).start()
print(f'sandbox bridge · mode {A.mode} · open http://localhost:{A.port}/topo.html · frames at /depth · ctrl+c stops')
try: ThreadingHTTPServer(('127.0.0.1', A.port), Handler).serve_forever()
except KeyboardInterrupt: pass
