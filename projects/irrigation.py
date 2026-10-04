exec(open('drain.py',encoding='utf-8').read())
# Sheet D-3 · Plan de riego y agua · Irrigation and water plan (4 Oct 2026, Will): vineyard supply, two underground cisterns
# under the roofs' downspouts, recirculating troughs, drip zones for native planting and the old nursery's trees.
import matplotlib.patches as mpatches
import json as _json
_O=_json.load(open('stable_origin.json')); _r=math.radians(_O['rot']); _ROT=math.radians(90-65.84)
def b2g(bx,by):                                        # stable frame ft -> site grid (same maths as site_extras.b2m + m2grid)
    x=(bx*math.cos(_ROT)-by*math.sin(_ROT))*FT; y=(bx*math.sin(_ROT)+by*math.cos(_ROT))*FT
    return (_O['grid'][0]+(x*math.cos(_r)-y*math.sin(_r))/cs, _O['grid'][1]-(x*math.sin(_r)+y*math.cos(_r))/cs)
from matplotlib.patches import Polygon as MPoly, Circle as MCircle, Rectangle as MRect
PIPE='#b5602e'; TANK='#0b4f8a'; ZONE=dict(trees='#4f7a3a', natives='#8a9a3a', lawn='#c9b830')
def foot_of(name):
    o=byname(name)
    return np.array(foot(o[0])) if o else None
def pts_of(name): return np.array([q[:2] for q in byname(name)[0]['pts']])
# ---- water numbers (ft², gal) ----
RAIN_IN=11.0                                           # Valle de Guadalupe, lower canyon: ~280 mm/yr, Dec–Mar
stable_ft2=88*46; stalls_ft2=92*36                     # roofs with their 2 ft overhangs (stable), butterfly roof (stalls)
gpi=lambda a: a*0.623                                  # gal per inch of rain on a ft² (0.623 gal/ft²/in)
stable_gpi, stalls_gpi = gpi(stable_ft2), gpi(stalls_ft2)
C1_M3, C2_M3 = 40, 30                                  # underground concrete cisterns (m³)
m3gal=264.2
horses=22; drink=10                                    # gal/horse/day, hot weather
WT, WD = 0.7, 1.25                                     # stone walls 0.7 ft thick, water 1.25 ft deep (lip .4 to water line 1.65)
trough_gal={'long':(44-2*WT)*(3.5-2*WT)*WD*7.48, 'east':(32-2*WT)*(3.5-2*WT)*WD*7.48, 'pad':(14-2*WT)*(3-2*WT)*WD*7.48, 'round':math.pi*(4-WT)**2*1.5*7.48}   # inside measure
# ---- figure ----
fig=plt.figure(figsize=(17,11),dpi=170); fig.patch.set_facecolor(globals().get('PAPER','white'))
ax=base_axes(fig,[0.015,0.27,0.665,0.67],alpha=.42)
contours(ax,z); features(ax)
# objects
for n,col in (('walker barn 72x40','white'),('covered stalls','white'),('stone trough (long)',WATER),('wash pad trough',WATER),('east trough',WATER),('bleachers','#e8e2d6')):
    F=foot_of(n)
    if F is not None: P=np.vstack([F,F[:1]]); ax.fill(P[:,0],P[:,1],color=col,alpha=.9,zorder=5); ax.plot(P[:,0],P[:,1],color=INK,lw=.8,zorder=6)
# ---- zones ----
def zone(poly,kind,lab,xy=None,hatch='//'):
    P=np.array(poly); ax.add_patch(MPoly(P,closed=True,facecolor=ZONE[kind],edgecolor=ZONE[kind],alpha=.22,lw=1.2,hatch=hatch,zorder=4))
    ax.add_patch(MPoly(P,closed=True,fill=False,edgecolor=ZONE[kind],lw=1.4,zorder=4))
    if xy=='': return
    if xy is None: xy=P.mean(axis=0)
    ax.text(xy[0],xy[1],lab,fontsize=7.2,weight='bold',color=INK,ha='center',va='center',zorder=12,bbox=dict(boxstyle='round,pad=.25',fc='white',ec='none',alpha=.85))
tr=pts_of('track'); cx,cy=tr[:,0].mean(),tr[:,1].mean()
infield=[(cx+(x-cx)*.72, cy+(y-cy)*.72) for x,y in tr[::2]]                           # inside the track: the old nursery's trees
zone(infield,'trees','Z3 · árboles del antiguo vivero (existentes)\nold nursery trees, existing','',hatch='..')
ax.text(cx,cy-3,'Z3 · árboles del antiguo vivero\nold nursery trees (existing)',fontsize=7.2,weight='bold',color=INK,ha='center',va='center',zorder=12,bbox=dict(boxstyle='round,pad=.25',fc='white',ec='none',alpha=.85))
pf=foot_of('pine forest')
if pf is not None: zone(pf,'trees','Z2 · pinar · pine grove',xy=(pf[:,0].mean(),pf[:,1].min()-1.6),hatch='..')
np_=foot_of('native planting')
if np_ is not None: zone(np_,'natives','Z1 · nativas · natives',xy=(np_[:,0].mean()-2.5,np_[:,1].max()+2.4))
cs_=foot_of('covered stalls')
if cs_ is not None:
    c0=cs_.mean(axis=0); zone([(c0[0]+(x-c0[0])*1.35, c0[1]+(y-c0[1])*1.35) for x,y in cs_],'trees','Z4 · palmas y sombra de las caballerizas\nstall palms and shade','',hatch='..')
    ax.text(c0[0]+2,c0[1]+7.2,'Z4 · palmas · stall palms',fontsize=7.2,weight='bold',color=INK,ha='center',zorder=12,bbox=dict(boxstyle='round,pad=.25',fc='white',ec='none',alpha=.85))
bl=byname('bleachers')[0]['c']; zone([(bl[0]-5,bl[1]-4),(bl[0]+5,bl[1]-4),(bl[0]+5,bl[1]+4),(bl[0]-5,bl[1]+4)],'trees','Z5 · sombra · picnic shade',xy=(bl[0],bl[1]-5.6))
# parking + main road: new shade trees as a dotted line
pk=np.array([q[:2] for s_ in S if s_.get('name')=='parking stall' for q in s_['pts']])
ax.plot([pk[:,0].min()-1,pk[:,0].max()+1],[pk[:,1].max()+1.6]*2,color=ZONE['trees'],lw=2.2,dashes=(1,2.2),zorder=6)
ax.text(pk[:,0].mean(),pk[:,1].max()+3.6,'Z6 · sombra del estacionamiento (nueva)\nparking shade trees (new)',fontsize=6.6,color=INK,ha='center',zorder=12,bbox=dict(boxstyle='round,pad=.2',fc='white',ec='none',alpha=.8))
# ---- supply: vineyard main at the NE gate, along the main road, branches ----
mr=pts_of('main road, north-east gate to south gate'); br=pts_of('barn to cross-fence road')
stb=byname('walker barn 72x40')[0]['c']
ax.plot(mr[:,0],mr[:,1],color=PIPE,lw=2.2,zorder=9,solid_capstyle='round')                            # 2 in main along the main road
ax.plot(br[:,0],br[:,1],color=PIPE,lw=1.6,zorder=9,dashes=(6,2))                                       # 1.5 in branch along the barn road to the stalls + round pen
g=pts_of('gate · north-east, main road').mean(axis=0)
ax.add_patch(MCircle(g,1.6,facecolor='white',edgecolor=PIPE,lw=2,zorder=13)); ax.text(g[0]-2.4,g[1]+1.2,'toma del viñedo · vineyard tap\n(por confirmar · to confirm)',fontsize=6.6,color=PIPE,zorder=13,ha='right',va='top')
# branch to the infield trees and the arena/round-pen shade
ax.plot([br[-1][0],cx+6],[br[-1][1],cy],color=PIPE,lw=1.3,zorder=9,dashes=(3,2))
# ---- cisterns ----
lt=byname('stone trough (long)')[0]['c']; C1=b2g(-60,-35)                 # at the stable's SW corner, between the pad trough and the long trough, off the roads
if cs_ is not None:
    # 4 Oct (Will): C2 sits just DOWNHILL of the round trough, so the valley chute, the trough's overflow and the roof all fall into it
    _op=[s_ for s_ in S if s_.get('name')=='stalls trough overflow pipe']
    if _op:
        _a=np.array(_op[0]['pts'][0][:2]); _b=np.array(_op[0]['pts'][-1][:2]); _u=(_b-_a)/np.linalg.norm(_b-_a); RT=(_a-_u*(4*FT/cs))   # round trough centre
        C2=tuple(RT+_u*(16*FT/cs)); RT=tuple(RT)
    else: sw=cs_[np.argmax(cs_[:,1]-cs_[:,0]*.3)]; C2=(sw[0]-2.6,sw[1]+2.2); RT=None
else: C2=(80,70); RT=None
for (x,y),lab,m3 in ((C1,'C1',C1_M3),(C2,'C2',C2_M3)):
    s_=math.sqrt(m3/2.5)/cs/2                                                                           # 2.5 m deep → side in cells
    ax.add_patch(MRect((x-s_,y-s_),2*s_,2*s_,facecolor=TANK,edgecolor=TANK,alpha=.35,lw=1.4,ls='--',zorder=10))
    ax.text(x,y,f'{lab}',fontsize=7.5,weight='bold',color='white',ha='center',va='center',zorder=12)
# downspout pipes roof → cistern → trough (dashed water)
sw_=b2g(-48,-23); ax.plot([sw_[0],C1[0]],[sw_[1],C1[1]],color=WATER,lw=1.6,dashes=(2,1.5),zorder=9)          # south gutter, SW downspout -> C1
pt_=b2g(-49.5,-28); ax.plot([C1[0],pt_[0]],[C1[1],pt_[1]],color=WATER,lw=1.2,dashes=(2,1.5),zorder=9)        # C1 -> pad trough
ax.plot([C1[0],lt[0]],[C1[1],lt[1]],color=WATER,lw=1.6,dashes=(2,1.5),zorder=9)
if RT: ax.plot([RT[0],C2[0]],[RT[1],C2[1]],color=WATER,lw=1.6,dashes=(2,1.5),zorder=9)   # trough overflow + chute -> C2, downhill
et=byname('east trough');
if et: e=et[0]['c']; ne_=b2g(36,23); ax.plot([ne_[0],e[0]],[ne_[1],e[1]],color=WATER,lw=1.6,dashes=(2,1.5),zorder=9)   # north gutter, NE downspout -> east trough
works(ax)
FFP=[sw_,ne_]+([tuple(np.array(RT)-_u*(9*FT/cs))] if RT else [])
for q in FFP: ax.scatter([q[0]],[q[1]],s=26,marker='o',c='white',edgecolors=WATER,linewidths=1.4,zorder=14); ax.scatter([q[0]],[q[1]],s=5,c=WATER,zorder=15)
# recirculation symbol on each trough
for n in ('stone trough (long)','east trough','wash pad trough'):
    o=byname(n)
    if o: c_=o[0]['c']; ax.annotate('',xy=(c_[0]+1.6,c_[1]-1.8),xytext=(c_[0]-1.6,c_[1]-1.8),arrowprops=dict(arrowstyle='<->',color=WATER,lw=1.1,connectionstyle='arc3,rad=.6'),zorder=13)
north(ax,140,8); scalebar(ax,6,96)
# callouts
CALLI=[((g[0]+2.8,g[1]+2.2),1),((C1[0]-1.2,C1[1]+3.9),2),((C2[0]-2.0,C2[1]-4.0),3),((lt[0]-2.2,lt[1]+5.4),4),((cx,cy+9),5),((pf.mean(axis=0)[0]+3,pf.mean(axis=0)[1]-9) if pf is not None else (118,48),6),((np_.mean(axis=0)[0]+1.5,np_.mean(axis=0)[1]-6.2) if np_ is not None else (100,52),7),((pk[:,0].min()-4,pk[:,1].mean()),8)]
for xy,n in CALLI: callout(ax,xy,n)
# ---- detail (4 Oct, Will + Walker): first-flush standpipe, then a trough that works like a natural pool ----
dx=fig.add_axes([0.02,0.105,0.325,0.15]); dx.set_xlim(0,100); dx.set_ylim(-10,33); dx.axis('off')
GR_='#5d8a3a'; SAND='#e3cf9a'; STN='#d9d4cb'
# first flush: downspout -> tee -> standpipe (ball seals when full, drip valve empties it) -> on to the cistern and trough
dx.plot([6,6],[24,15.5],color=INK,lw=2.4); dx.add_patch(MRect((4.2,1.5),3.6,13.2,facecolor='#eef3f7',edgecolor=INK,lw=.9)); dx.add_patch(MRect((4.5,1.8),3.0,6.5,facecolor=WATER,alpha=.35,edgecolor='none'))
dx.add_patch(MCircle((6,8.9),1.2,facecolor='white',edgecolor=INK,lw=.8)); dx.plot([6,6],[1.5,-.6],color=INK,lw=1); dx.plot([5.2,6.8],[-.6,-.6],color=INK,lw=1)
dx.plot([6,16,16],[15.5,15.5,10.5],color=WATER,lw=1.4); dx.text(0,29.5,'1ª lluvia · first flush',fontsize=5.6,weight='bold',color=INK)
dx.text(0,-5.2,'tubo 8 in, ~8 ft: se llena, la bola sella, el agua limpia sigue',fontsize=5.0,color=INK); dx.text(0,-8.0,'8 in, ~8 ft standpipe: fills, a ball seals it, clean water runs on',fontsize=5.0,color='#6a655a',style='italic')
dx.text(7.6,-.6,'goteo · drip',fontsize=4.8,color=INK,va='center')
# the trough: bubbler + fish
dx.add_patch(MRect((18,4),46,10,facecolor=STN,edgecolor=INK,lw=1)); dx.add_patch(MRect((20,6),42,6.5,facecolor=WATER,alpha=.55,edgecolor='none'))
for k_,(xx,yy) in enumerate(((30,6.6),(30.6,8.3),(29.6,9.9),(30.4,11.4),(42,6.6),(42.5,8.6),(41.6,10.6))): dx.add_patch(MCircle((xx,yy),.35+.08*(k_%3),facecolor='white',edgecolor='none',alpha=.9))
dx.add_patch(MRect((28.8,6.0),2.4,.6,facecolor='#555',edgecolor='none')); dx.add_patch(MRect((40.8,6.0),2.4,.6,facecolor='#555',edgecolor='none'))
from matplotlib.patches import Ellipse as _El
for xx,yy in ((50,9),(54,7.6)): dx.add_patch(_El((xx,yy),2.2,.9,facecolor='#e8892c',edgecolor='none')); dx.add_patch(MPoly([(xx+1.0,yy),(xx+1.8,yy+.5),(xx+1.8,yy-.5)],facecolor='#e8892c',edgecolor='none'))
dx.text(41,1.6,'burbujeador + peces · bubbler + fish',fontsize=4.9,ha='center',color=INK)
# spout -> lower basin = vetiver in gravel over a sand layer (Walker), behind a pipe rail
dx.plot([64,66,67.5],[12.4,10.6,6.5],color=WATER,lw=2); dx.add_patch(MRect((62,12.2),5,.9,facecolor=STN,edgecolor=INK,lw=.8))
dx.add_patch(MRect((66,-1),18,9,facecolor=STN,edgecolor=INK,lw=1)); dx.add_patch(MRect((67.3,.3),15.4,1.6,facecolor=SAND,edgecolor='none'))
import random as _rnd; _g=_rnd.Random(4)
for _ in range(70): dx.add_patch(MCircle((_g.uniform(67.8,82.2),_g.uniform(2.3,6.6)),_g.uniform(.25,.5),facecolor='#b9b2a6',edgecolor='none'))
dx.add_patch(MRect((67.3,2.0),15.4,4.9,facecolor=WATER,alpha=.25,edgecolor='none'))
for xx in np.linspace(68.5,81.5,7):
    for dd in (-1.4,-.6,0,.7,1.5): dx.plot([xx,xx+dd],[6.8,11.5+_g.uniform(0,4)],color=GR_,lw=.7)
    for dd in (-.5,0,.5): dx.plot([xx,xx+dd],[6.6,2.2],color='#8a6a48',lw=.4)
dx.plot([65,85],[17.5,17.5],color='#2c2f33',lw=1.6); dx.plot([65,65],[8,17.5],color='#2c2f33',lw=1.2); dx.plot([85,85],[8,17.5],color='#2c2f33',lw=1.2)
dx.text(75,18.6,'vetiver en grava · vetiver in gravel',fontsize=5.0,ha='center',color=GR_,weight='bold'); dx.text(75,-2.0,'arena · sand',fontsize=4.8,ha='center',color=INK,va='top')
# pump draws from under the sand and returns it to the far end
dx.plot([84,90,90,92],[1,1,6,6],color=WATER,lw=1.3,dashes=(3,2)); dx.add_patch(MCircle((92,8),2.2,facecolor='white',edgecolor=INK,lw=1)); dx.text(92,8,'B',fontsize=6,ha='center',va='center')
dx.plot([92,92,97,97,20,20],[10.2,22,22,27,27,13.5],color=WATER,lw=1.3,dashes=(3,2)); dx.text(58,28,'regreso al otro extremo · back to the far end',fontsize=4.9,ha='center',color=WATER)
fig.text(0.02,0.262,'Bebedero como alberca natural: el agua cae a una pileta de vetiver en grava sobre arena, se filtra y una bomba la regresa;',fontsize=6.0,color=INK)
fig.text(0.02,0.252,'Trough as a natural pool: water falls into a basin of vetiver in gravel over sand, is filtered, and a pump sends it back.',fontsize=6.0,color='#6a655a',style='italic')
# ---- side panel ----
px=0.70
fig.text(px,0.955,'PLAN DE RIEGO Y AGUA',fontsize=20,weight='bold',color=INK)
fig.text(px,0.93,'Irrigation and water plan · Centro Equino, Chichihuas',fontsize=12.5,color='#555')
NOTES_I=[
 ('Vineyard supply','Toma del viñedo',f'A 2 in HDPE main from the vineyard line, assumed at the north-east gate (point and pressure to confirm with the ranch), buried along the main road to the stable turn-off (about 400 ft); a 1.5 in branch along the barn road to the covered stalls and the round pen, and a drip branch into the track infield.',f'Línea principal de HDPE de 2 in desde la red del viñedo, supuesta en la puerta noreste (punto y presión por confirmar con el rancho), enterrada por el camino principal hasta la entrada del establo (unos 120 m); ramal de 1.5 in por el camino del establo a las caballerizas y al corral redondo, y ramal de goteo al interior de la pista.'),
 ('Cistern C1, stable','Cisterna C1, establo',f'Underground concrete cistern of {C1_M3} m³ ({C1_M3*m3gal:,.0f} gal) at the stable’s south-west corner, between the pad trough and the long trough, dug with the ranch’s machinery. The SOUTH roof half feeds it and, through it, the long trough and the pad trough; the NORTH half feeds the east trough at the run fence (4). The whole roof ({stable_ft2:,} ft² with its overhangs) gives about {stable_gpi:,.0f} gal per inch of rain, about {stable_gpi*RAIN_IN:,.0f} gal in a normal year. Every downspout first drops into a first-flush standpipe (detail): an 8 in pipe about 8 ft tall that holds the first ~80 L, the dust and droppings; when it is full a floating ball seals it and the clean water runs on to the cistern and troughs, and a drip valve empties it over a day. Leaf screens at the gutters; overflow to the barn-road ditch; submersible pump.',f'Cisterna de concreto enterrada de {C1_M3} m³ en la esquina suroeste del establo, entre el bebedero de la losa y el bebedero largo, excavada con la maquinaria del rancho. La alimenta la mitad SUR del techo y, a través de ella, el bebedero largo y el de la losa; la mitad NORTE alimenta el bebedero del este, en la cerca del corral (4). Todo el techo ({stable_ft2*0.0929:,.0f} m² con aleros) da unos {stable_gpi*3.785/2.54:,.0f} L por cm de lluvia, unos {stable_gpi*RAIN_IN*3.785/1000:,.0f} m³ en un año normal. Cada bajada cae primero a un tubo de primera lluvia (detalle): un tubo de 8 in y unos 2.4 m que guarda los primeros ~80 L, el polvo y las cacas de pájaro; lleno, una bola flotante lo sella y el agua limpia sigue a la cisterna y los bebederos, y una válvula de goteo lo vacía en un día. Rejillas de hojas en los canalones; rebose a la zanja del camino del establo; bomba sumergible.'),
 ('Cistern C2, covered stalls','Cisterna C2, caballerizas',f'Underground cistern of {C2_M3} m³ ({C2_M3*m3gal:,.0f} gal) just downhill of the round trough at the south-west end, so the valley chute, the trough’s overflow and the butterfly roof all fall into it by gravity’s valley gutter ({stalls_gpi:,.0f} gal per inch, about {stalls_gpi*RAIN_IN:,.0f} gal a year). Two first-flush standpipes at the valley leader, then the chute still pours into the round trough for show; the cistern takes the rest. Overflow to the stalls’ ditch.',f'Cisterna enterrada de {C2_M3} m³ justo cuesta abajo del bebedero redondo en el extremo suroeste, para que el canalón, el rebose del bebedero y el techo caigan a ella por gravedad; alimentada por el canalón del valle del techo mariposa ({stalls_gpi*3.785/2.54:,.0f} L por cm, unos {stalls_gpi*RAIN_IN*3.785/1000:,.0f} m³ al año). Dos tubos de primera lluvia en la bajada del valle; luego el canalón sigue vertiendo al bebedero redondo a la vista; la cisterna recibe el resto. Rebose a la zanja de las caballerizas.'),
 ('Fresh troughs, natural filtration','Bebederos frescos, filtro natural',f'Each trough works like a small natural pool (detail). Water pours from a stone spout into a lower stone basin at its end planted with vetiver in gravel (Walker): the roots and the gravel’s bacteria take up what feeds algae. A small pump draws the clean water from under a sand layer and returns it to the far end; an air stone bubbles in the trough and a few goldfish eat larvae and algae. No chlorine. A pipe rail keeps horses off the vetiver (safe if nibbled). Float top-up from the cistern, overflow to the ditch. Held: long trough ~{trough_gal["long"]:,.0f} gal, east (outside the NE run fence) {trough_gal["east"]:,.0f}, pad {trough_gal["pad"]:,.0f}, round {trough_gal["round"]:,.0f}.',f'Cada bebedero funciona como una pequeña alberca natural (detalle). El agua cae por un caño de piedra a una pileta de piedra más baja en su extremo, sembrada con vetiver en grava (Walker): las raíces y las bacterias de la grava se comen lo que alimenta a las algas. Una bomba pequeña toma el agua limpia bajo una capa de arena y la regresa al otro extremo; una piedra difusora burbujea en el bebedero y unos peces dorados comen larvas y algas. Sin cloro. Un tubo protege el vetiver de los caballos (no les hace daño si lo muerden). Flotador desde la cisterna, rebose a la zanja. Contienen: largo ~{trough_gal["long"]*3.785/1000:,.1f} m³, este (fuera de la cerca del corral NE) {trough_gal["east"]*3.785/1000:,.1f}, losa {trough_gal["pad"]*3.785/1000:,.1f}, redondo {trough_gal["round"]*3.785/1000:,.1f}.'),
 ('Z3 · the old nursery’s trees','Z3 · los árboles del antiguo vivero','For years this ground was a rented plant nursery; the trees inside the track and under the covered stalls are what it left. They are kept, and a drip ring (two 2 gal/h emitters per tree, deep and slow) carries them through the first dry summers of the new use, then is weaned off. A good story for the place, and the start of a vivero again.','Durante años este terreno fue un vivero rentado; los árboles dentro de la pista y bajo las caballerizas son lo que dejó. Se conservan, y un anillo de goteo (dos goteros de 8 L/h por árbol, hondo y lento) los acompaña en los primeros veranos secos del nuevo uso, luego se retira. Una buena historia para el lugar, y el inicio de un vivero otra vez.'),
 ('Z2 · pine grove and Z4 · stall palms','Z2 · pinar y Z4 · palmas','Existing trees between the parking and the stable, and the palms at the stall backs: drip rings for establishment years only. New shade trees (Z5 picnic, Z6 parking) are natives that live on winter rain once rooted: encino (coast live oak), pirul (California pepper), palo verde, mesquite, aliso (sycamore) in the draw.','Árboles existentes entre el estacionamiento y el establo, y las palmas al fondo de las caballerizas: anillos de goteo solo los años de establecimiento. Los árboles de sombra nuevos (Z5 día de campo, Z6 estacionamiento) son nativos que viven de la lluvia de invierno una vez arraigados: encino, pirul, palo verde, mezquite, aliso en la cañada.'),
 ('Z1 · native planting','Z1 · plantas nativas','The beds along the entry drive and around the troughs: the palette used before on the ranch’s landscapes (white and Cleveland sage, buckwheat, brittlebush, deer grass, agave). Drip at 1 gal per plant a week in summer for two years, then rain only. No lawn anywhere; mulch from the ranch’s own prunings.','Los macizos de la entrada y alrededor de los bebederos: la paleta usada antes en los paisajes del rancho (salvia blanca y de Cleveland, trigo sarraceno silvestre, incienso, muhly, agave). Goteo de 4 L por planta a la semana en verano por dos años, luego solo lluvia. Sin pasto en ningún lado; acolchado de las podas del rancho.'),
 ('Water budget','Presupuesto de agua',f'Horses are the real use: {horses} horses × {drink} gal a day ≈ {horses*drink*7:,.0f} gal a week, from the cisterns first, mains second. Summer irrigation at full establishment ≈ 2,000 gal a week; a season of recirculating troughs loses only evaporation. The two cisterns ({(C1_M3+C2_M3)*m3gal:,.0f} gal) hold about {(C1_M3+C2_M3)*m3gal/(horses*drink*7+2000):.0f} weeks of everything with no rain; one inch of rain puts about {stable_gpi/2+stalls_gpi:,.0f} gal into the cisterns (south half of the stable + the stalls) and {stable_gpi/2:,.0f} gal into the east trough.',f'Los caballos son el uso real: {horses} caballos × {drink*3.785:.0f} L al día ≈ {horses*drink*7*3.785/1000:,.1f} m³ a la semana, primero de las cisternas, luego de la red. El riego de verano en pleno establecimiento ≈ {2000*3.785/1000:,.1f} m³ por semana; una temporada de bebederos recirculantes solo pierde evaporación. Las dos cisternas ({(C1_M3+C2_M3)} m³) guardan unas {(C1_M3+C2_M3)*m3gal/(horses*drink*7+2000):.0f} semanas de todo sin lluvia; 2.5 cm de lluvia meten unos {(stable_gpi/2+stalls_gpi)*3.785/1000:,.1f} m³ a las cisternas (mitad sur del establo + caballerizas) y {stable_gpi/2*3.785/1000:,.1f} m³ al bebedero del este.'),
]
y=0.902
import textwrap
for k,(en,es,ten,tes) in enumerate(NOTES_I):
    fig.text(px,y,f'{k+1}',fontsize=10,weight='bold',color='#b5602e')
    fig.text(px+.018,y,f'{es} · {en}',fontsize=8.6,weight='bold',color=INK)
    ly=y-.014
    for line in textwrap.wrap(tes,107): fig.text(px+.018,ly,line,fontsize=6.0,color=INK); ly-=.0085
    for line in textwrap.wrap(ten,107): fig.text(px+.018,ly,line,fontsize=6.0,color='#6a655a',style='italic'); ly-=.0085
    y=ly-.0042
print('notes end at', round(ly, 3), '(footer rule 0.055)')   # 4 Oct: guard against running into the footer
# vision box
fig.text(0.355,0.245,'Visión · Vision',fontsize=8.5,color=INK,weight='bold')
for k,line in enumerate(textwrap.wrap('Agua primero, luego árboles, luego edificios: el centro ecuestre como vivero otra vez, con café, cata de vino, juegos para niños y animales que se dejan tocar, todo regado por la lluvia que cae en los techos.',112)): fig.text(0.355,0.230-k*.0105,line,fontsize=6.6,color=INK)
for k,line in enumerate(textwrap.wrap('Water first, then trees, then buildings: the horse centre as a nursery again, with a café, wine tasting, children’s play and animals you can touch, all watered by the rain that falls on the roofs.',112)): fig.text(0.355,0.206-k*.0105,line,fontsize=6.6,color='#6a655a',style='italic')
fig.text(0.355,0.176,f'Lluvia ≈ {RAIN_IN*25.4:.0f} mm/año (dic–mar) · techos ≈ {(stable_gpi+stalls_gpi)*3.785/2.54:,.0f} L por cm · cisternas {C1_M3+C2_M3} m³',fontsize=7.2,color=INK); fig.text(0.355,0.163,f'Rain ≈ {RAIN_IN:.0f} in/yr · roofs ≈ {stable_gpi+stalls_gpi:,.0f} gal/in · cisterns {(C1_M3+C2_M3)*m3gal:,.0f} gal',fontsize=7.2,color='#6a655a',style='italic')
# legend
items=[(PIPE,'-',2.2,'Línea principal 2 in · 2 in main'),(PIPE,'--',1.6,'Ramal 1.5 in / goteo · 1.5 in branch / drip'),(WATER,':',1.6,'Bajada y alimentación · Downspout and feed'),(TANK,'--',1.4,'Cisterna enterrada · Underground cistern'),(ZONE['trees'],'-',6,'Zona de árboles · Tree zone'),(ZONE['natives'],'-',6,'Zona de nativas · Native zone'),(WATER,'o',0,'Tubo de primera lluvia · First-flush standpipe')]
for k,(c,st,lw,tx) in enumerate(items):
    lx=0.355+(k%2)*0.165; ly=0.145-(k//2)*0.02
    if lw: fig.add_artist(matplotlib.lines.Line2D([lx,lx+.03],[ly,ly],color=c,lw=lw,ls=st,alpha=.6 if lw==6 else 1))
    else: fig.add_artist(matplotlib.lines.Line2D([lx+.015],[ly],marker='o',markersize=5,markerfacecolor='white',markeredgecolor=c,markeredgewidth=1.4,lw=0))
    fig.text(lx+.038,ly-.005,tx,fontsize=7.4,color=INK)
fig.text(0.02,0.03,'31.9999 N, 116.7641 W · Hoja / Sheet D-3 · 4 oct 2026 · Diseño preliminar, no para construcción · Preliminary design, not for construction',fontsize=8,color='#6a655a')
if not globals().get('PACK'): fig.savefig('D3-irrigation.png',dpi=170); print('ok')
