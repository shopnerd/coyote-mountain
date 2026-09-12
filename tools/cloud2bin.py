"""cloud2bin: a point cloud for coyote mountain topo.

Reads a textured OBJ (DroneDeploy / Rhino export: vertices in local metres, x east, y north, z up, textures via the mtl),
a .las / .laz (needs laspy), or a .ply with colours, and writes one compact file the tool's "load points" opens:

  CPC1  little endian
  magic 'CPC1' (4) · count u32 · lat f64 · lon f64 (the local origin, degrees) · min x y z f32 · range x y z f32 (metres) · name 32 bytes
  then count x { x u16, y u16, z u16, rgb u16 (5-6-5) }: 8 bytes a point, positions quantised over the range

Local metres are east / north of the origin; z is metres above sea level after --z0 is added.

  python cloud2bin.py mesh.obj --lat 32.0146986 --lon -116.7779736 --z0 309.732 --out encino-solo-points.bin --cap 1000000
"""
import argparse, os, struct, sys, time
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument('src'); ap.add_argument('--lat', type=float, required=True); ap.add_argument('--lon', type=float, required=True)
ap.add_argument('--z0', type=float, default=0.0, help='added to every z (local relative height -> above sea level)')
ap.add_argument('--cap', type=int, default=1500000); ap.add_argument('--out', default=None); ap.add_argument('--name', default=None)
a = ap.parse_args(); t0 = time.time()
src = a.src; ext = os.path.splitext(src)[1].lower(); name = a.name or os.path.splitext(os.path.basename(src))[0][:31]

if ext == '.obj':
    from PIL import Image
    folder = os.path.dirname(os.path.abspath(src)); mtl = {}; cur = None; mtlfile = None
    xs, ys, zs, vts = [], [], [], []; corner = {}   # vertex -> (material, vt index) from the first face corner that uses it
    with open(src, 'rb') as f:
        for line in f:
            if line.startswith(b'v '): p = line.split(); xs.append(float(p[1])); ys.append(float(p[2])); zs.append(float(p[3]))
            elif line.startswith(b'vt '): p = line.split(); vts.append((float(p[1]), float(p[2])))
            elif line.startswith(b'f '):
                for tok in line.split()[1:]:
                    q = tok.split(b'/'); vi = int(q[0]) - 1
                    if vi not in corner and len(q) > 1 and q[1]: corner[vi] = (cur, int(q[1]) - 1)
            elif line.startswith(b'usemtl'): cur = line.split(maxsplit=1)[1].strip().decode()
            elif line.startswith(b'mtllib'): mtlfile = line.split(maxsplit=1)[1].strip().decode()
    print(f'{len(xs)} vertices, {len(vts)} texture coords, {len(corner)} with a texture corner, {time.time()-t0:.0f}s')
    texmap = {}
    if mtlfile and os.path.exists(os.path.join(folder, mtlfile)):
        m = None
        for line in open(os.path.join(folder, mtlfile), encoding='utf-8', errors='ignore'):
            if line.startswith('newmtl'): m = line.split(maxsplit=1)[1].strip()
            elif line.startswith('map_Kd') and m: texmap[m] = line.split(maxsplit=1)[1].strip()
    x = np.array(xs, np.float32); y = np.array(ys, np.float32); z = np.array(zs, np.float32) + a.z0; n = len(x); del xs, ys, zs
    rgb = np.full((n, 3), 160, np.uint8); vt = np.array(vts, np.float32) if vts else np.zeros((0, 2), np.float32)
    bymat = {}
    for vi, (m, ti) in corner.items(): bymat.setdefault(m, []).append((vi, ti))
    for m, lst in bymat.items():
        tex = texmap.get(m); path = os.path.join(folder, tex) if tex else None
        if not path or not os.path.exists(path): print('no texture for', m); continue
        im = np.asarray(Image.open(path).convert('RGB')); h, w = im.shape[:2]
        idx = np.array(lst, np.int64); u = vt[idx[:, 1], 0]; v = vt[idx[:, 1], 1]
        px = np.clip((u % 1.0) * (w - 1), 0, w - 1).astype(int); py = np.clip(((1 - v) % 1.0) * (h - 1), 0, h - 1).astype(int)
        rgb[idx[:, 0]] = im[py, px]; print(f'  {m}: {len(lst)} points coloured from {tex} ({w}x{h})')
elif ext in ('.las', '.laz'):
    import laspy
    L = laspy.read(src); x = np.asarray(L.x, np.float64); y = np.asarray(L.y, np.float64); z = np.asarray(L.z, np.float32) + a.z0
    x = (x - x.mean()).astype(np.float32); y = (y - y.mean()).astype(np.float32)   # --lat/--lon must be the cloud's centre in that case
    rgb = np.stack([np.asarray(L.red) >> 8, np.asarray(L.green) >> 8, np.asarray(L.blue) >> 8], 1).astype(np.uint8) if 'red' in L.point_format.dimension_names else np.full((len(x), 3), 160, np.uint8)
    n = len(x); print(f'{n} las points')
elif ext == '.ply':
    from plyfile import PlyData
    P = PlyData.read(src)['vertex']; x = np.asarray(P['x'], np.float32); y = np.asarray(P['y'], np.float32); z = np.asarray(P['z'], np.float32) + a.z0
    rgb = np.stack([P['red'], P['green'], P['blue']], 1).astype(np.uint8) if 'red' in P.data.dtype.names else np.full((len(x), 3), 160, np.uint8); n = len(x)
else: sys.exit('unknown file type ' + ext)

if n > a.cap:
    keep = np.random.default_rng(7).choice(n, a.cap, replace=False); keep.sort(); x, y, z, rgb = x[keep], y[keep], z[keep], rgb[keep]; n = a.cap; print('thinned to', n)
mn = np.array([x.min(), y.min(), z.min()], np.float32); rg = np.maximum(np.array([x.max(), y.max(), z.max()], np.float32) - mn, 1e-3)
q = lambda v, k: np.round((v - mn[k]) / rg[k] * 65535).astype(np.uint16)
c565 = ((rgb[:, 0].astype(np.uint16) >> 3) << 11) | ((rgb[:, 1].astype(np.uint16) >> 2) << 5) | (rgb[:, 2].astype(np.uint16) >> 3)
body = np.stack([q(x, 0), q(y, 1), q(z, 2), c565], 1).astype('<u2').tobytes()
out = a.out or os.path.splitext(src)[0] + '-points.bin'
with open(out, 'wb') as f:
    f.write(b'CPC1'); f.write(struct.pack('<I', n)); f.write(struct.pack('<dd', a.lat, a.lon)); f.write(struct.pack('<fff', *mn)); f.write(struct.pack('<fff', *rg)); f.write(name.encode('utf-8')[:32].ljust(32, b'\0')); f.write(body)
print(f'wrote {out}: {n} points, {os.path.getsize(out)/1e6:.1f} MB, x {mn[0]:.1f}..{mn[0]+rg[0]:.1f} y {mn[1]:.1f}..{mn[1]+rg[1]:.1f} z {mn[2]:.1f}..{mn[2]+rg[2]:.1f} m, {time.time()-t0:.0f}s')
