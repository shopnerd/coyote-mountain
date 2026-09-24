# 24 ft bays: 8 pipe posts, 4 roof trusses, Z purlins, perimeter grade beam. First-pass feasibility only.
import math
BAY, SPAN, EAVE, RIDGE = 24.0, 42.0, 12.0, 17.0
CONC, STONE = 0.150, 0.140
for V_kmh in (150, 180):
    V = V_kmh / 3.6
    q = 0.613 * V**2 * 0.85 / 47.88                       # psf
    up_psf = q * 1.45; dead = 5.0
    # interior post carries a full bay; corner posts half (use interior)
    uplift = up_psf * BAY * SPAN / 2 / 1000 - 0.6 * dead * BAY * SPAN / 2 / 1000
    beam = 2 * 2 * BAY * CONC
    wall = 4.5 * 1.5 * BAY * (1 - 8 / 24) * STONE        # two 4 ft stall doors per 24 ft bay
    pier = math.pi / 4 * 2.5**2 * 6 * CONC
    hold = 0.6 * (beam + wall + pier)
    wall_area = 76 * (EAVE - 4.5) * 0.5 + 76 * 5
    Vp = q * 1.3 * wall_area / 1000 / 8
    M = Vp * EAVE
    Sx = 43.8                                             # 12 in Sch 40
    Ma = 0.6 * 35 * Sx / 12
    lever = 18.0                                          # in, rod spacing on a 22 in plate
    T_rod = (M * 12 / lever + uplift / 2) / 2
    # purlins: 24 ft span, spacing s, uplift + dead
    for s in (4, 5):
        w = (up_psf - 0.6 * dead) * s                     # plf
        Mp = w * BAY**2 / 8 / 1000                        # kip-ft simple span
        print(f'   purlins @ {s} ft: net uplift {w:.0f} plf, M = {Mp:.1f} kip-ft')
    # truss: each carries one bay, 42 ft span, 5 ft rise
    wT = (up_psf - 0.6 * dead) * BAY / 1000               # kip/ft
    MT = wT * SPAN**2 / 8
    chord = MT / 4.0                                      # kip, with ~4 ft effective depth at mid
    print(f'V={V_kmh}: q={q:.1f} psf | uplift/post {uplift:.1f} kip vs hold-down {hold:.1f} ({"OK" if hold >= uplift else "SHORT"}) '
          f'| base M {M:.1f} kip-ft ({M/Ma*100:.0f}% of Sch 40) | rod tension {T_rod:.1f} kip | truss chord force ~{chord:.1f} kip')
print('1-1/4 in F1554 Gr 55 rod allowable tension ~ %.1f kip' % (0.75 * 75 * 0.969 / 2.0))
