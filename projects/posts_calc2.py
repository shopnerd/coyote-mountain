# Base plate on pier + perimeter grade beam carrying the stone wall. First-pass feasibility only.
import math
BAY = 12.0                 # ft, post spacing along the long walls
EAVE = 12.0
CONC, STONE = 0.150, 0.140 # kcf
BEAM_W, BEAM_D = 2.0, 2.0  # ft
WALL_H, WALL_T = 4.5, 1.5  # ft
DOOR_FRAC = 4.0 / 12.0     # one 4 ft stall door per 12 ft bay
PIER_D, PIER_L = 2.5, 5.0  # ft
for V_kmh in (150, 180):
    V = V_kmh / 3.6
    q = 0.613 * V**2 * 0.85 / 47.88
    uplift = q * 1.45 * BAY * 21 / 1000 - 0.6 * 5.0 * BAY * 21 / 1000
    beam = BEAM_W * BEAM_D * BAY * CONC
    wall = WALL_H * WALL_T * BAY * (1 - DOOR_FRAC) * STONE
    pier = math.pi / 4 * PIER_D**2 * PIER_L * CONC
    resist = 0.6 * (beam + wall + pier)
    Vp = q * 1.3 * (76 * (EAVE - 4.5) * 0.5 + 76 * 5) / 1000 / 14
    M = Vp * EAVE
    T_bolt = (M * 12 / 14.0 + uplift / 2) / 2   # 2 bolts in tension, 14 in lever arm
    print(f'V={V_kmh} km/h: uplift {uplift:.1f} kip, hold-down {resist:.1f} kip '
          f'(beam {beam:.1f} + wall {wall:.1f} + pier {pier:.1f}, x0.6) -> {"OK" if resist >= uplift else "SHORT"}; '
          f'base moment {M:.1f} kip-ft, tension per anchor rod {T_bolt:.1f} kip')
# 1 in F1554 Gr 36 anchor rod, ASD tension ~ 0.75*58*0.606 in2 / 2.0
print('1 in F1554-36 rod allowable tension ~ %.1f kip' % (0.75 * 58 * 0.606 / 2.0))
