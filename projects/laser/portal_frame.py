"""Centro Equino stable: one pitched portal frame from 12 in pipe, 2D stiffness analysis.
First-pass feasibility only (ASD, simple load cases); a licensed engineer must design the real thing.

Frame: span 42 ft, eave 12 ft, ridge 17 ft, frames every 24 ft. Bases fixed (base plate + 4 anchor rods)
and, as a check, pinned. Rafters welded rigid to the column tops (knees) and to each other at the ridge.
"""
import numpy as np, math, json

E = 29000.0                 # ksi
PIPES = {'12 in Sch 40 (12.75 x 0.406)': (12.75, 0.406), '12 in Sch 80 (12.75 x 0.500)': (12.75, 0.500)}
FY = 35.0                   # ksi, A53 Gr B (casing may be higher; test it)
SPAN, EAVE, RIDGE, BAY = 42.0, 12.0, 17.0, 24.0

def props(D, t):
    d = D - 2 * t
    A = math.pi / 4 * (D ** 2 - d ** 2); I = math.pi / 64 * (D ** 4 - d ** 4); S = I / (D / 2)
    return A, I, S

def solve(A, I, base_fixed, loads):
    ft = 12.0
    nodes = np.array([[0, 0], [0, EAVE], [SPAN / 2, RIDGE], [SPAN, EAVE], [SPAN, 0]], float) * ft
    elems = [(0, 1), (1, 2), (2, 3), (3, 4)]
    nd = len(nodes) * 3; K = np.zeros((nd, nd)); F = np.zeros(nd)
    FEF = {}
    for e, (i, j) in enumerate(elems):
        dx, dy = nodes[j] - nodes[i]; L = math.hypot(dx, dy); c, s = dx / L, dy / L
        k = np.array([[E * A / L, 0, 0, -E * A / L, 0, 0],
                      [0, 12 * E * I / L ** 3, 6 * E * I / L ** 2, 0, -12 * E * I / L ** 3, 6 * E * I / L ** 2],
                      [0, 6 * E * I / L ** 2, 4 * E * I / L, 0, -6 * E * I / L ** 2, 2 * E * I / L],
                      [-E * A / L, 0, 0, E * A / L, 0, 0],
                      [0, -12 * E * I / L ** 3, -6 * E * I / L ** 2, 0, 12 * E * I / L ** 3, -6 * E * I / L ** 2],
                      [0, 6 * E * I / L ** 2, 2 * E * I / L, 0, -6 * E * I / L ** 2, 4 * E * I / L]])
        T = np.zeros((6, 6)); r = np.array([[c, s, 0], [-s, c, 0], [0, 0, 1]]); T[:3, :3] = r; T[3:, 3:] = r
        idx = [3 * i, 3 * i + 1, 3 * i + 2, 3 * j, 3 * j + 1, 3 * j + 2]
        K[np.ix_(idx, idx)] += T.T @ k @ T
        # member load: global (wx, wy) in kip/in along the member length
        wx, wy = loads.get(e, (0.0, 0.0))
        wl = r @ np.array([wx, wy, 0])      # local axial, transverse
        q, p = wl[1], wl[0]
        fef = np.array([p * L / 2, q * L / 2, q * L ** 2 / 12, p * L / 2, q * L / 2, -q * L ** 2 / 12])
        FEF[e] = (fef, T, k, idx)
        F[idx] += T.T @ fef
    fixed = [0, 1, 12, 13] + ([2, 14] if base_fixed else [])
    free = [d for d in range(nd) if d not in fixed]
    U = np.zeros(nd); U[free] = np.linalg.solve(K[np.ix_(free, free)], F[free])
    out = {}
    for e, (fef, T, k, idx) in FEF.items():
        f = k @ (T @ U[idx]) - fef          # member end forces, local
        out[e] = f
    R = K @ U - F
    return U, out, R

res = {}
Lr_ = math.hypot(SPAN / 2, RIDGE - EAVE); cosr = (SPAN / 2) / Lr_
q = 27.2                                     # psf at 180 km/h, exposure C ~15 ft
for bay in (24.0, 12.0):
  for name, (D, t) in PIPES.items():
    A, I, S = props(D, t); Ma = 0.6 * FY * S / 12
    k = bay / 1000 / 12
    dead = 5 * k * cosr; live = 20 * k * cosr
    up = 1.1 * q * k * cosr                  # roof suction + internal, averaged over the rafter
    wall = 1.0 * q * k                        # windward + leeward on the columns
    cases = {
      'D + Lr': {1: (0, -(dead + live)), 2: (0, -(dead + live))},
      '0.6D + 0.6W (uplift)': {0: (0.6 * wall * .6, 0), 1: (0, 0.6 * up - 0.6 * dead), 2: (0, 0.6 * up - 0.6 * dead), 3: (0.6 * wall * .4, 0)},
      'D + 0.75(0.6W) + 0.75Lr': {0: (0.45 * wall * .6, 0), 1: (0, -(dead + 0.75 * live)), 2: (0, -(dead + 0.75 * live)), 3: (0.45 * wall * .4, 0)},
    }
    for case, L_ in cases.items():
      U, f, R = solve(A, I, True, L_)
      Mmax = max(max(abs(f[e][2]), abs(f[e][5])) for e in f) / 12
      axial = max(abs(f[e][0]) for e in f)
      res[f'bay {bay:.0f} ft | {name} | {case}'] = dict(M=round(Mmax, 1), cap=round(Ma, 1), used=round(Mmax / Ma * 100),
          sag_in=round(abs(U[7]), 2), sway_in=round(max(abs(U[3]), abs(U[9])), 2), base_M=round(abs(R[2]) / 12, 1),
          base_V=round(max(abs(R[0]), abs(R[12])), 1), base_vert=round(R[1], 1), axial=round(axial, 1))
for kk, v in res.items(): print(kk, v)
json.dump(res, open('portal_frame_results.json', 'w'), indent=1)
