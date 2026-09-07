"""DroneDeploy export -> a survey package the topo tool can load.

  python tools/dd2survey.py "<DroneDeploy folder>" "<out folder>"

Reads the textured mesh OBJ (local metres, z up, origin at the survey centre) and the orthomosaic
GeoTIFF (Web Mercator, deflate + predictor), writes:
  <out>/<name>-dem.tif    float32 GeoTIFF in lat/lon (EPSG:4326), uncompressed, NaN where the mesh has no ground
  <out>/<name>-ortho.kmz  the orthomosaic as a JPEG ground overlay with its lat/lon box
Only numpy and Pillow are needed.
"""
import sys, os, glob, re, struct, zlib, io, zipfile, math
import numpy as np
from PIL import Image

src, out = sys.argv[1], sys.argv[2]; name = sys.argv[3] if len(sys.argv) > 3 else 'survey'
os.makedirs(out, exist_ok=True)
CELL = 1.0   # metres per DEM pixel: about six mesh vertices per cell, so the scatter average is smooth and nearly hole-free

def bbox_of(kml_path):
    t = open(kml_path).read(); g = lambda k: float(re.search('<%s>([^<]+)</%s>' % (k, k), t).group(1))
    return g('north'), g('south'), g('east'), g('west')

# ---------- 1. mesh -> DEM ----------
obj = glob.glob(os.path.join(src, 'model*', 'scene_mesh_textured.obj'))[0]
kml = glob.glob(os.path.join(src, '*Orthomosaic*', '*.kml'))[0]
N, S, E, Wd = bbox_of(kml); lat0, lon0 = (N + S) / 2, (E + Wd) / 2
print('ortho box', N, S, E, Wd, 'centre', lat0, lon0)
xs, ys, zs = [], [], []
with open(obj, 'rb') as f:
    for line in f:
        if line[:2] == b'v ':
            p = line.split(); xs.append(float(p[1])); ys.append(float(p[2])); zs.append(float(p[3]))
x = np.array(xs, np.float64); y = np.array(ys, np.float64); z = np.array(zs, np.float64); del xs, ys, zs
print('vertices', len(x), 'x', x.min(), x.max(), 'y', y.min(), y.max(), 'z', z.min(), z.max())
x0, x1, y0, y1 = x.min(), x.max(), y.min(), y.max()
gw, gh = int(math.ceil((x1 - x0) / CELL)) + 1, int(math.ceil((y1 - y0) / CELL)) + 1
acc = np.zeros((gh, gw)); cnt = np.zeros((gh, gw))
ci = np.clip(((x - x0) / CELL).round().astype(int), 0, gw - 1); cj = np.clip(((y1 - y) / CELL).round().astype(int), 0, gh - 1)   # row 0 = north
np.add.at(acc, (cj, ci), z); np.add.at(cnt, (cj, ci), 1)
dem = np.where(cnt > 0, acc / np.maximum(cnt, 1), np.nan)
# where is the survey? the vertex footprint, closed (grow then shrink by 6 cells) so interior holes count as inside but the outline does not creep outward
valid = cnt > 0
def grow(m, k):
    out = m.copy()
    for _ in range(k):
        pad = np.pad(out, 1, constant_values=False); out = pad[:-2, 1:-1] | pad[2:, 1:-1] | pad[1:-1, :-2] | pad[1:-1, 2:] | out
    return out
def shrink(m, k): return ~grow(~m, k)
inside = shrink(grow(valid, 6), 6)
# fill holes inside the footprint by averaging neighbours until none are left
for _ in range(400):
    m = np.isnan(dem) & inside
    if not m.any(): break
    pad = np.pad(dem, 1, constant_values=np.nan); s = np.zeros_like(dem); n = np.zeros_like(dem)
    for dj in (0, 1, 2):
        for di in (0, 1, 2):
            v = pad[dj:dj + gh, di:di + gw]; ok = ~np.isnan(v); s[ok] += v[ok]; n[ok] += 1
    fill = m & (n >= 1); dem[fill] = s[fill] / n[fill]
print('footprint', int(inside.sum()), 'of', gw * gh, 'cells')
dsm = dem.copy()
# ground filter (progressive morphological, after Zhang 2003): open the surface with growing windows; anything that stands up more than the slope allows is canopy or roof and drops to the opened surface
def erode(a, r):
    out = a.copy()
    for _ in range(r):
        pad = np.pad(out, 1, mode='edge'); out = np.fmin(np.fmin(pad[:-2, 1:-1], pad[2:, 1:-1]), np.fmin(pad[1:-1, :-2], pad[1:-1, 2:]))
    return out
def dilate(a, r):
    out = a.copy()
    for _ in range(r):
        pad = np.pad(out, 1, mode='edge'); out = np.fmax(np.fmax(pad[:-2, 1:-1], pad[2:, 1:-1]), np.fmax(pad[1:-1, :-2], pad[1:-1, 2:]))
    return out
SLOPE, DH0, DHMAX = 0.35, 0.3, 4.0   # terrain slope allowance, base threshold (m), cap (m)
ground = dem.copy(); removed = np.zeros(dem.shape, bool)
for r in (1, 2, 4, 8, 16):
    opened = dilate(erode(ground, r), r); dh = min(DHMAX, DH0 + SLOPE * r * CELL * 2)
    up = (ground - opened) > dh; removed |= up; ground = np.where(up, opened, ground)
# smooth the ground a little where things were removed, so tree footprints do not leave dimples
pad = np.pad(ground, 2, mode='edge'); s = np.zeros_like(ground); n = np.zeros_like(ground)
for dj in range(5):
    for di in range(5):
        v = pad[dj:dj + gh, di:di + gw]; ok = ~np.isnan(v); s[ok] += v[ok]; n[ok] += 1
smooth = np.where(n > 0, s / np.maximum(n, 1), np.nan); ground = np.where(removed, smooth, ground)
print('ground filter: removed canopy and roofs on', int(removed[inside].sum()), 'cells of', int(inside.sum()), '· max drop', round(float(np.nanmax(dsm - ground)), 1), 'm')
dem = ground
# light smooth to take the scatter noise off
pad = np.pad(dem, 1, mode='edge'); s = np.zeros_like(dem); n = np.zeros_like(dem)
for dj in (0, 1, 2):
    for di in (0, 1, 2):
        v = pad[dj:dj + gh, di:di + gw]; ok = ~np.isnan(v); s[ok] += v[ok]; n[ok] += 1
sm = np.where(n > 0, s / np.maximum(n, 1), np.nan); dem = np.where(np.isnan(dem), np.nan, sm)
print('dem', gw, 'x', gh, 'cells at', CELL, 'm ·', int(np.isnan(dem).sum()), 'empty cells')

# georeference: local metres east/north about the ortho box centre -> degrees
mlat = 111320.0; mlon = 111320.0 * math.cos(math.radians(lat0))
west = lon0 + x0 / mlon; north = lat0 + y1 / mlat; dlon = CELL / mlon; dlat = CELL / mlat

def geotiff_f32(path, arr, west, north, dlon, dlat):
    h, w = arr.shape; data = arr.astype('<f4').tobytes()
    tags = []  # (tag, type, count, value-bytes-or-int)
    def t(tag, typ, vals):
        tags.append((tag, typ, vals))
    t(256, 4, [w]); t(257, 4, [h]); t(258, 3, [32]); t(259, 3, [1]); t(262, 3, [1]); t(273, 4, [0]); t(277, 3, [1]); t(278, 4, [h]); t(279, 4, [len(data)])
    t(284, 3, [1]); t(339, 3, [3]); t(33550, 12, [dlon, dlat, 0.0]); t(33922, 12, [0.0, 0.0, 0.0, west, north, 0.0])
    t(34735, 3, [1, 1, 0, 4, 1024, 0, 1, 2, 1025, 0, 1, 1, 2048, 0, 1, 4326, 2054, 0, 1, 9102]); t(42113, 2, list(b'nan\x00'))
    tags.sort(key=lambda q: q[0])
    sizes = {2: 1, 3: 2, 4: 4, 12: 8}; fmts = {2: 'B', 3: 'H', 4: 'I', 12: 'd'}
    ifd_off = 8; ifd_len = 2 + 12 * len(tags) + 4; extra_off = ifd_off + ifd_len; extra = b''; entries = b''
    for tag, typ, vals in tags:
        raw = struct.pack('<' + fmts[typ] * len(vals), *vals)
        if tag == 273: raw = None
        if raw is not None and len(raw) <= 4: entries += struct.pack('<HHI', tag, typ, len(vals)) + raw.ljust(4, b'\x00')
        elif raw is None: entries += struct.pack('<HHII', tag, typ, 1, 0)   # patched below
        else: entries += struct.pack('<HHII', tag, typ, len(vals), extra_off + len(extra)); extra += raw
    data_off = extra_off + len(extra)
    # patch strip offset
    ent = bytearray(entries); pos = [i for i in range(0, len(ent), 12) if struct.unpack('<H', ent[i:i + 2])[0] == 273][0]; ent[pos + 8:pos + 12] = struct.pack('<I', data_off)
    with open(path, 'wb') as f:
        f.write(b'II*\x00' + struct.pack('<I', ifd_off) + struct.pack('<H', len(tags)) + bytes(ent) + struct.pack('<I', 0) + extra + data)

dem_path = os.path.join(out, name + '-dem.tif'); geotiff_f32(dem_path, dem, west, north, dlon, dlat); geotiff_f32(os.path.join(out, name + '-dsm.tif'), dsm, west, north, dlon, dlat)   # dem = ground (trees and roofs filtered), dsm = the surface as flown
print('wrote', dem_path, round(os.path.getsize(dem_path) / 1e6, 1), 'MB · west', west, 'north', north, 'deg/px', dlon, dlat)

# ---------- 2. orthomosaic -> JPEG ground overlay ----------
kmz_path = os.path.join(out, name + '-ortho.kmz')
if os.path.exists(kmz_path): print('ortho kmz already there, kept'); sys.exit(0)
tif = glob.glob(os.path.join(src, '*Orthomosaic*', '*.tif'))[0]
f = open(tif, 'rb'); hdr = f.read(8); bo = '<' if hdr[:2] == b'II' else '>'; ifd = struct.unpack(bo + 'I', hdr[4:8])[0]; f.seek(ifd); n = struct.unpack(bo + 'H', f.read(2))[0]; tags = {}
for i in range(n):
    tag, typ, cnt = struct.unpack(bo + 'HHI', f.read(8)); val = f.read(4); tags[tag] = (typ, cnt, val)
def rd(tag):
    typ, cnt, val = tags[tag]; sz = {1: 1, 2: 1, 3: 2, 4: 4, 12: 8}[typ]; tot = sz * cnt
    if tot <= 4: raw = val[:tot]
    else: f.seek(struct.unpack(bo + 'I', val)[0]); raw = f.read(tot)
    return list(struct.unpack(bo + {1: 'B', 2: 'B', 3: 'H', 4: 'I', 12: 'd'}[typ] * cnt, raw))
W, H, tw, th = rd(256)[0], rd(257)[0], rd(322)[0], rd(323)[0]; offs, cnts = rd(324), rd(325); pred = rd(317)[0] if 317 in tags else 1; comp = rd(259)[0]; bands = rd(277)[0]
assert comp == 8 and bands == 4, (comp, bands)
RED = 8; ow, oh = W // RED, H // RED; img = np.zeros((oh, ow, 4), np.uint8); ntx = -(-W // tw)
print('ortho', W, 'x', H, 'tiles', len(offs), '-> reduced', ow, 'x', oh)
for t, (o, c) in enumerate(zip(offs, cnts)):
    if c == 0: continue
    f.seek(o); raw = zlib.decompress(f.read(c)); a = np.frombuffer(raw, np.uint8).reshape(th, tw, bands)
    if pred == 2: a = np.cumsum(a, axis=1, dtype=np.uint8)
    tx, ty = t % ntx, t // ntx; sub = a[::RED, ::RED]; y0, x0 = ty * th // RED, tx * tw // RED
    hh, ww = min(sub.shape[0], oh - y0), min(sub.shape[1], ow - x0)
    if hh > 0 and ww > 0: img[y0:y0 + hh, x0:x0 + ww] = sub[:hh, :ww]
    if t % 2000 == 0: print('  tile', t, 'of', len(offs))
rgb = Image.fromarray(img[:, :, :3]); alpha = img[:, :, 3]
rgb = Image.fromarray(np.where(alpha[:, :, None] > 0, img[:, :, :3], 255).astype(np.uint8))   # transparent edge -> white
buf = io.BytesIO(); rgb.save(buf, 'JPEG', quality=86)
kml = '<?xml version="1.0" encoding="UTF-8"?>\n<kml xmlns="http://www.opengis.net/kml/2.2"><Document><GroundOverlay><name>%s orthomosaic</name><Icon><href>ortho.jpg</href></Icon><LatLonBox><north>%.9f</north><south>%.9f</south><east>%.9f</east><west>%.9f</west></LatLonBox></GroundOverlay></Document></kml>' % (name, N, S, E, Wd)
kmz_path = os.path.join(out, name + '-ortho.kmz')
with zipfile.ZipFile(kmz_path, 'w', zipfile.ZIP_DEFLATED) as zf:
    zf.writestr('doc.kml', kml); zf.writestr('ortho.jpg', buf.getvalue())
print('wrote', kmz_path, round(os.path.getsize(kmz_path) / 1e6, 1), 'MB')
