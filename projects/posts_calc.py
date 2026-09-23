import math
# ---- pipe candidates (OD in, wall in) ----
pipes={'12 in Sch 40 (12.75 × 0.406)':(12.75,0.406),'12 in Sch 80 (12.75 × 0.500)':(12.75,0.500),'11-3/4 in casing (11.75 × 0.375)':(11.75,0.375)}
def props(D,t):
    d=D-2*t; A=math.pi/4*(D**2-d**2); I=math.pi/64*(D**4-d**4); S=I/(D/2); Z=(D**3-d**3)/6; w=A*3.4
    return A,I,S,Z,w
# ---- barn & wind ----
L,Bw,eave,ridge=76,42,12,17
bay=12; posts_side=7
for V_kmh in (150,180):
    V=V_kmh/3.6; q=0.613*V**2*0.85/47.88   # psf, exposure C at ~15 ft
    uplift_psf=q*(0.9+0.55)                 # roof suction + internal pressure (partially enclosed)
    trib=bay*Bw/2
    D_roof=5.0
    T=uplift_psf*trib/1000 - 0.6*D_roof*trib/1000   # kip net uplift per eave post
    # transverse: stick walls ~50% solid above 4.5 ft stone; all 14 posts cantilever and share via roof
    wall=(L*(eave-4.5))*0.5 + L*4.5*0 + L*(ridge-eave)*1.0   # stone takes own load at base
    Ftot=q*1.3*wall/1000
    Vp=Ftot/(2*posts_side); M=Vp*eave
    print(f'V={V_kmh} km/h  q={q:.1f} psf  uplift/post={T:.1f} kip  shear/post={Vp:.2f} kip  M={M:.1f} kip-ft')
    for n,(D,t) in pipes.items():
        A,I,S,Z,w=props(D,t); Ma=0.6*35*S/12  # ASD allowable-ish, Fy 35 ksi A53B
        defl=Vp*1000*(eave*12)**3/(3*29e6*I)
        print(f'   {n}: {w:.0f} lb/ft, 20 ft = {w*20:.0f} lb, M allow ≈ {Ma:.0f} kip-ft ({M/Ma*100:.0f}% used), top drift {defl:.2f} in')
    # embedded pier, IBC 1807.3.2.1 nonconstrained
    for b in (2.5,3.0):
        S1_per_ft=150*2   # psf/ft, class 4 sandy soil, doubled for isolated pole
        d=4.0
        for _ in range(40):
            S1=S1_per_ft*d/3; A_=2.34*Vp*1000/(S1*b); d=0.5*A_*(1+math.sqrt(1+4.36*eave/A_))
        Wc=math.pi/4*b*b*d*0.150; 
        print(f'   pier {b} ft dia: embed ≈ {d:.1f} ft, concrete weight {Wc:.1f} kip vs uplift {T:.1f} kip ({"OK" if 0.6*Wc>=T else "needs bell/friction"})')
