import json, math, numpy as np, sys
sys.path.insert(0,'.'); sys.path.insert(0,'../roads')
import geo18 as geo
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import os
DRAWING=os.path.join(os.path.dirname(os.path.abspath('drain.py')),'centro-equino-2026-09-26-stalls16-nopad.json')   # 26 Sep: covered stalls, paddocks and two roads gone
p=json.load(open(DRAWING,encoding='utf-8'))
W,H=p['grid']; FT=0.3048; cs=float(p['sliders']['siteW'])/(W-1); cf=cs/FT
z=np.array(p['z']).reshape(H,W)/FT; b=np.array(p['base']).reshape(H,W)/FT
from flow import flow                     # the export's own __flow is stale once the ground is edited outside the app
acc,down=flow(np.array(p['z']).reshape(H,W))
A_ac=cs*cs/4047
S=p['strokes']; byname=lambda n:[s for s in S if s.get('name')==n]
la0,lo0=p['world']['lat'],p['world']['lon']; t=math.radians(float(p['sliders']['rot']))
def GR(lat,lon):
    dy=(lat-la0)*111320; dx=(lon-lo0)*111320*math.cos(math.radians(la0))
    sx=dx*math.cos(t)-dy*math.sin(t); sy=dx*math.sin(t)+dy*math.cos(t)
    return sx/cs+(W-1)/2, (H-1)/2-sy/cs
def foot(o):
    r=math.radians(o['rot']); sc=o.get('sc',1)
    return [(o['c'][0]+(x*sc*math.cos(r)-y*sc*math.sin(r))/cs, o['c'][1]-(x*sc*math.sin(r)+y*sc*math.cos(r))/cs) for x,y in o['foot']]
plt.rcParams['font.family']='DejaVu Sans'
INK='#2a2824'; WATER='#1f78c8'
def base_axes(fig,rect,alpha=.55):
    ax=fig.add_axes(rect); img=np.asarray(geo.render(0,0,W-1,H-1,8)).astype(float)/255
    img=img*alpha+(1-alpha)*np.array([.96,.95,.92]); ax.imshow(img,extent=(0,W-1,H-1,0))
    ax.set_xlim(0,W-1); ax.set_ylim(H-1,0); ax.set_aspect('equal'); ax.axis('off'); return ax
def features(ax,lw=1):
    for s in S:
        n=s.get('name') or ''; k=s.get('kind')
        if k=='path':
            P=np.array([q[:2] for q in s['pts']]); w=(s.get('pw',3.66)/FT)/cf
            ax.plot(P[:,0],P[:,1],color='#c9b48f',lw=max(1.2,w*5.2),solid_capstyle='round',zorder=2,alpha=.9)
        elif k=='obj' and n in ('walker barn 72x40','covered stalls','trailer 8 x 40','stone trough (long)','wash pad trough','east trough','bleachers'):
            P=np.array(foot(s)+[foot(s)[0]]); ax.fill(P[:,0],P[:,1],color='white',alpha=.85,zorder=3); ax.plot(P[:,0],P[:,1],color=INK,lw=.8,zorder=4)
        elif k=='obj' and n in ('arena fence','round pen fence','site fence','cross fence'):
            pass
    for i in (1,2):
        P=np.array([q[:2] for q in S[i]['pts']]); ax.plot(P[:,0],P[:,1],color=INK,lw=1,zorder=4)
    loop=[s for s in S if s.get('shape') and not s.get('name') and len(s['pts'])==10 and abs(s['pts'][0][0]-26.6)<.3][0]
    P=np.array([q[:2] for q in loop['pts']]); ax.plot(P[:,0],P[:,1],color=INK,lw=1.6,dashes=(6,2,1,2),zorder=5)
    cr=[s for s in S if s.get('shape') and not s.get('name') and s.get('dash') and len(s['pts'])==2 and abs(s['pts'][0][0]-69.3)<.3][0]
    P=np.array([q[:2] for q in cr['pts']]); ax.plot(P[:,0],P[:,1],color=INK,lw=1,dashes=(6,2,1,2),zorder=5)
def contours(ax,Z,col=INK):
    X,Y=np.meshgrid(np.arange(W),np.arange(H))
    ax.contour(X,Y,Z,levels=np.arange(1050,1120,1),colors=col,linewidths=.35,alpha=.55,zorder=3)
    cs5=ax.contour(X,Y,Z,levels=np.arange(1050,1120,5),colors=col,linewidths=.9,alpha=.8,zorder=3)
    ax.clabel(cs5,fmt='%d',fontsize=6.5,inline=True)
def drainage(ax):
    # flow arrows on a lattice, sized by upstream area
    for j in range(2,H-2,3):
        for i in range(2,W-2,3):
            n=j*W+i; d=down[n]
            if d<0: continue
            di=(d%W)-i; dj=(d//W)-j; L=math.hypot(di,dj); a=acc[j,i]*A_ac
            s=.9+min(1.6,math.log10(1+a*20)); w=.0022+min(.004,a*.0006)
            ax.arrow(i,j,di/L*s,dj/L*s,width=w*W/150*1.0,head_width=.9,head_length=.7,length_includes_head=True,color=WATER,alpha=.35+min(.55,a*.1),lw=0,zorder=6)
    # concentrated flow lines (> 1/3 acre)
    segs=[];ws=[]
    for n in range(W*H):
        a=acc.flat[n]*A_ac
        if a<.33 or down[n]<0: continue
        i,j=n%W,n//W; d=down[n]; segs.append([(i,j),(d%W,d//W)]); ws.append(.5+min(2.6,a*.3))
    ax.add_collection(LineCollection(segs,linewidths=ws,colors=WATER,alpha=.8,zorder=7,capstyle='round'))
def works(ax,labels=True):
    for f in p['records']['ditches']:
        P=np.array([GR(q[0],q[1]) for q in f['pts']]); nm=f.get('name','')
        if nm.startswith('infield basin'):
            X,Y=np.meshgrid(np.arange(W),np.arange(H)); near=np.zeros((H,W),bool)
            for q in P: near|=np.hypot(X-q[0],Y-q[1])<4.5
            wet=near&((b-z)>.6)
            ax.contourf(X,Y,wet.astype(float),levels=[.5,1.5],colors=[WATER],alpha=.8,zorder=8)
        else:
            ax.plot(P[:,0],P[:,1],color='#0b4f8a',lw=2.4,dashes=(5,2),zorder=8)
    for s in S:
        if (s.get('name') or '').startswith('culvert'):
            P=np.array([q[:2] for q in s['pts']]); ax.plot(P[:,0],P[:,1],color='#0b4f8a',lw=4.5,solid_capstyle='butt',zorder=9)
    for s in byname('natural water sink'):
        P=np.array([q[:2] for q in s['pts']]); ax.fill(P[:,0],P[:,1],color=WATER,alpha=.45,zorder=8); ax.plot(P[:,0],P[:,1],color=WATER,lw=1,dashes=(3,2),zorder=8)
    for s in byname('stalls trough overflow pipe'):
        P=np.array([q[:2] for q in s['pts']]); ax.plot(P[:,0],P[:,1],color=WATER,lw=1.6,dashes=(2,1.5),zorder=9)
    ws=byname('existing watering station')[0]; P=np.array([q[:2] for q in ws['pts']]); ax.fill(P[:,0],P[:,1],color=WATER,zorder=9)
d=(z-b); cutyd=-(d[d<0].sum())*cf*cf*FT**0 * (0.3048**0)  # ft * cell ft^2
cell_ft2=cf*cf; cut=-(d[d<0].sum())*cell_ft2/27; fill=(d[d>0].sum())*cell_ft2/27
print('cut %.0f fill %.0f yd3'%(cut,fill))
def north(ax,x,y,r=4):
    a=GR(la0,lo0); b2=GR(la0+.0005,lo0); vx,vy=b2[0]-a[0],b2[1]-a[1]; L=math.hypot(vx,vy); vx,vy=vx/L,vy/L
    ax.annotate('',xy=(x+vx*r,y+vy*r),xytext=(x-vx*r,y-vy*r),arrowprops=dict(arrowstyle='-|>',color=INK,lw=1.4),zorder=20)
    ax.text(x+vx*(r+2.2),y+vy*(r+2.2),'N',ha='center',va='center',fontsize=10,weight='bold',color=INK,zorder=20)
def scalebar(ax,x,y):
    L=200/cf; ax.plot([x,x+L],[y,y],color=INK,lw=3,solid_capstyle='butt',zorder=20); ax.plot([x,x+L/2],[y,y],color='white',lw=1.4,zorder=21)
    ax.text(x,y-1.4,'0',fontsize=7,ha='center'); ax.text(x+L,y-1.4,'200 ft · 61 m',fontsize=7,ha='center')
def callout(ax,xy,n):
    ax.add_patch(matplotlib.patches.Circle(xy,2.2,facecolor='white',edgecolor='#b5602e',lw=1.6,zorder=22))
    ax.text(xy[0],xy[1],str(n),ha='center',va='center',fontsize=8.5,weight='bold',color='#b5602e',zorder=23)
CALL=[((79,79),1),((68,71.5),2),((65.4,76.2),3),((46,57.2),4),((27,61.8),5),((113,69),6),((121.5,50),7),((104,58.5),8),((96.4,50.6),9),((34.5,55.5),10),((72.5,66.5),11),((104,74.5),12)]
NCULV=sum(1 for s in S if (s.get('name') or '').startswith('culvert'))
NOTES=[
 ('Road-bend crossing','Cruce en la curva del camino','Up to about 16 acres of hillside can reach this crossing (the full watershed above the site, measured zoomed out). Rock-lined ford preferred; if piped, a 30 in culvert with a rock apron.','Hasta unas 6.5 ha de ladera pueden llegar a este cruce (toda la cuenca arriba del sitio, medida con vista amplia). Se prefiere vado empedrado; si se entuba, alcantarilla de 75 cm con delantal de piedra.'),
 ('Grassed waterway','Canal empastado','Wide, shallow, planted channel along the natural low line; joined by the paddock-end branch.','Canal ancho, poco profundo y sembrado sobre la línea baja natural; recibe el ramal del extremo de los corrales.'),
 ('Natural sink at the track end','Bajo natural al final de la pista','Soft, shallow low spot below the track where water collects and soaks in; Walker confirmed it on site (26 Sep). About 1.5 ft deep, roughly 4,000 gal; it now drains about 0.9 acre, fills in about half an inch of rain, and overflows west along the waterway.','Bajo suave abajo de la pista donde el agua se junta y se infiltra; Walker lo confirmó en sitio (26 sep). Unos 45 cm de hondo, aprox. 15,000 L; ahora recibe unas 0.36 ha, se llena con 1.3 cm de lluvia y el excedente sigue al oeste por el canal.'),
 ('Infield basin','Cuenca del interior','Shallow planted basin where the infield flattens; slows and soaks the first flush.','Cuenca baja y sembrada donde el interior se aplana; frena y absorbe la primera lluvia.'),
 ('Outlet at the west fence','Salida en la cerca oeste','Rock level spreader sized for the full watershed (about twice what the site alone shows); water leaves as a thin sheet toward the gully and the vineyard (same owner).','Esparcidor de piedra a nivel, dimensionado para toda la cuenca (cerca del doble de lo que muestra el sitio solo); el agua sale en lámina delgada hacia la cañada y el viñedo (mismo dueño).'),
 ('Crossings under roads and track','Cruces bajo caminos y pista',f'{NCULV} rock-armoured dips or culverts where the waterway meets a road or the track (two roads removed 26 Sep).',f'{NCULV} vados empedrados o alcantarillas donde el canal cruza un camino o la pista (dos caminos quitados el 26 sep).'),
 ('Barn diversion and outfall','Desvío del establo y descarga','Swale on the uphill side carries water around the barn pad to the natural draw.','Zanja del lado alto que lleva el agua alrededor del establo hacia la cañada natural.'),
 ('Barn roof to the stone trough','Techo del establo al bebedero','The 76 × 46 ft roof (with its 2 ft overhangs) sheds about 2,180 gal per inch of rain; gutters on both long sides: the south one feeds the long stone trough and the pad trough, the north one the east trough at the run fence.','El techo de 23 × 14 m (con aleros de 60 cm) capta unos 8,250 L por cada 2.5 cm de lluvia; canales en ambos lados largos: la del sur alimenta el bebedero largo de piedra y el de la losa, la del norte el bebedero del este en la cerca del corral.'),
 ('Ditch above the barn road','Zanja arriba del camino del establo','Protects the round pen and arena from runoff off the slope above; now also takes the covered stalls’ ditch, about 0.5 acre in all, well within its size.','Protege el corral redondo y la pista oval del escurrimiento de la pendiente; ahora recibe también la zanja de las caballerizas, unas 0.2 ha en total, holgada para su tamaño.'),
 ('Existing watering station','Bebedero existente','Round stone trough, kept and filled.','Bebedero redondo de piedra, se conserva y se llena.'),
 ('Covered stalls','Caballerizas techadas','The butterfly roof (92 × 36 ft) sheds about 2,060 gal per inch of rain down its valley and an open chute into the round trough (about 500 gal full). A ditch above the stalls and the trough’s overflow pipe run to the ditch above the barn road (9).','El techo mariposa (28 × 11 m) capta unos 7,800 L por cada 2.5 cm de lluvia; baja por el valle y un canalón abierto al bebedero redondo (unos 1,900 L lleno). Una zanja arriba de las caballerizas y el tubo de demasías del bebedero van a la zanja del camino del establo (9).'),
 ('Gully above the scrub-side road','Zanja sobre el camino del matorral','Interceptor on the hill side of the owner’s road, 6 ft off its edge, 1 ft deep, 2 ft bottom, 2:1 sides. East leg (640 ft) into crossing 1; west leg (450 ft) to a new rock crossing at the south-west corner, then down the west fence to the spreader (5). Catches the hill water now landing on the road. Agreed in principle with the owner (4 Oct); his road, build it with him.','Zanja del lado alto del camino del dueño, a 1.8 m del borde, 30 cm de hondo, fondo de 60 cm, taludes 2:1. Tramo este (195 m) al cruce 1; tramo oeste (137 m) a un cruce nuevo de piedra en la esquina suroeste y de ahí por la cerca oeste al esparcidor (5). Recoge el agua del cerro que hoy cae al camino. Acordado en principio con el dueño (4 oct); es su camino, se hace con él.'),
]
