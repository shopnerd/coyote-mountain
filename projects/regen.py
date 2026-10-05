exec(open('drain.py',encoding='utf-8').read())
# Sheet A-2 · Diseño regenerativo · Regenerative design (4 Oct 2026, Will: "permaculture, biodynamics, regeneration, no waste, water
# harvest, vivero, community, natural horsemanship, zones, children"). Zones 0-5 drawn from the real objects (shapely buffers),
# the closed loops as a diagram, the numbers, and the notes.
import textwrap, json as _json
from shapely.geometry import Polygon as SP, Point
from shapely.ops import unary_union
from matplotlib.patches import Polygon as MPoly, FancyArrowPatch, Circle as MCircle, FancyBboxPatch
_O=_json.load(open('stable_origin.json')); _r=math.radians(_O['rot']); _ROT=math.radians(90-65.84)
def b2g(bx,by):
    x=(bx*math.cos(_ROT)-by*math.sin(_ROT))*FT; y=(bx*math.sin(_ROT)+by*math.cos(_ROT))*FT
    return (_O['grid'][0]+(x*math.cos(_r)-y*math.sin(_r))/cs, _O['grid'][1]-(x*math.sin(_r)+y*math.cos(_r))/cs)
def foot_of(n):
    o=byname(n); return SP(foot(o[0])) if o else None
def pts_of(n): return np.array([q[:2] for q in byname(n)[0]['pts']])
F=lambda ft: ft/cf                                                                   # feet -> grid cells
ZC=['#7a4a2a','#c96f3a','#d9a441','#8aa04a','#5f8a6a','#3f6b5a']
fig=plt.figure(figsize=(17,11),dpi=170); fig.patch.set_facecolor(globals().get('PAPER','white')); fig._norm_single=True
ax=base_axes(fig,[0.015,0.30,0.665,0.64],alpha=.38)
contours(ax,z); features(ax); ax.set_xlim(18,150); ax.set_ylim(92,8)
stable=foot_of('walker barn 72x40'); stalls=foot_of('covered stalls'); arena=foot_of('arena fence'); rpen=foot_of('round pen fence')
site=foot_of('site fence'); pines=foot_of('pine forest'); natives=foot_of('native planting')
bl=np.array(byname('bleachers')[0]['c']); tr=pts_of('track'); track=SP(tr).buffer(0)
pk=np.array([q[:2] for s_ in S if s_.get('name')=='parking stall' for q in s_['pts']])
Z0=stable
Z1=unary_union([stable.buffer(F(40)), natives.buffer(F(6)) if natives else stable]).difference(Z0)
Z2=unary_union([stalls.buffer(F(25)), arena.buffer(F(18)), rpen.buffer(F(18)), Point(bl).buffer(F(40)), SP(pk).convex_hull.buffer(F(15)), pines.buffer(F(10)),
                unary_union([stable,stalls,rpen]).convex_hull.buffer(F(10))]).difference(Z0.union(Z1))
Z3=track.buffer(F(8)).difference(unary_union([Z0,Z1,Z2]))
Z4=site.difference(unary_union([Z0,Z1,Z2,Z3])) if site else None
def draw(g,col,alpha,hatch=None,lw=1.2):
    for poly in (getattr(g,'geoms',None) or [g]):
        if poly.is_empty or poly.area<.5: continue
        P=np.array(poly.exterior.coords); ax.add_patch(MPoly(P,closed=True,fc=col,ec=col,alpha=alpha,lw=0,hatch=hatch,zorder=4))
        ax.add_patch(MPoly(P,closed=True,fill=False,ec=col,lw=lw,zorder=5))
for g,k,a in ((Z4,4,.16),(Z3,3,.22),(Z2,2,.24),(Z1,1,.32),(Z0,0,.55)):
    if g is not None: draw(g,ZC[k],a)
# zone 5: the hill above the scrub-side road, left wild
rd=pts_of('existing scrub-side road'); hill=np.vstack([rd,[[rd[-1][0],92],[rd[0][0],92]]])
ax.add_patch(MPoly(hill,closed=True,fc=ZC[5],alpha=.13,ec='none',zorder=3))
def ztag(xy,k,es,en):
    ax.text(xy[0],xy[1],f'Z{k}  {es}\n{en}',fontsize=6.6,weight='bold',color='white',ha='center',va='center',zorder=14,bbox=dict(boxstyle='round,pad=.3',fc=ZC[k],ec='none',alpha=.95))
c3=np.array(track.centroid.coords[0])
ztag(np.array(b2g(8,0)),0,'casa del lugar','home of the place')
ztag(np.array(b2g(-62,-52)),1,'cada día','every day')
ztag(np.array(arena.centroid.coords[0])+np.array([16,-4]),2,'trabajo diario','daily work')
ztag(c3+np.array([0,-14]),3,'cada semana · vivero','weekly · nursery')
ztag(np.array([60,24]),4,'manejo · pastoreo','managed · grazing')
ztag(np.array([118,86]),5,'el cerro, silvestre','the hill, wild')
# what goes where
def mark(xy,sym,col,lab,dx=2.2,dy=0,ha='left'):
    ax.scatter([xy[0]],[xy[1]],s=46,marker=sym,c=col,edgecolors='white',linewidths=.8,zorder=15)
    ax.text(xy[0]+dx,xy[1]+dy,lab,fontsize=5.9,color=INK,ha=ha,va='center',zorder=15,bbox=dict(boxstyle='round,pad=.15',fc='white',ec='none',alpha=.82))
mark(np.array(b2g(-62,34)),'s','#6a8f3a','huerto de cocina · kitchen garden',dx=0,dy=-3,ha='center')
# the compost yard, located (Will, 4 Oct): by the barn road below the round pen, a short haul from both stables, next to the nursery
# and the garden, out of the waterway, downhill of nothing it could foul. Four windrows 60 x 8 ft on a 70 x 50 ft pad of compacted
# earth, a roofed bay for the preparations and the finished pile, a small berm on the downhill side.
def road_axes(road,at):                                   # 4 Oct (Will): long sides parallel to the nearest stretch of road
    R_=pts_of(road); k=int(np.argmin(np.hypot(*(R_-at).T))); a_,b_=R_[max(k-2,0)],R_[min(k+2,len(R_)-1)]
    u_=(b_-a_)/np.linalg.norm(b_-a_); return u_,np.array([-u_[1],u_[0]])
CY=np.array([44.0,76.0]); ux,uy=road_axes('existing scrub-side road',CY)
pad=[CY+ux*a*F(35)+uy*b*F(25) for a,b in ((-1,-1),(1,-1),(1,1),(-1,1))]
ax.add_patch(MPoly(np.array(pad),closed=True,fc='#c9b48f',ec='#7a4a2a',lw=1.4,zorder=8))
for k in range(4):
    o=CY+uy*F(-17+k*11); ax.plot(*np.array([o-ux*F(30),o+ux*F(30)]).T,color='#5c3b22',lw=3.2,solid_capstyle='round',zorder=9)
ax.text(CY[0],CY[1]+F(42),'PATIO DE COMPOSTA · COMPOST YARD\n4 camellones 60 ft · 4 windrows, 70 × 50 ft',fontsize=6.4,weight='bold',color='#5c3b22',ha='center',va='center',zorder=15,bbox=dict(boxstyle='round,pad=.25',fc='white',ec='#7a4a2a',lw=.8,alpha=.92))
# market garden for the valley's restaurants: on the flattest open ground beside the main road and its water main, near the compost
MG=np.array([81.5,26.5]); _V=pts_of('existing vineyard road'); _V=_V[(abs(_V[:,0]-MG[0])<25)]; _p=np.polyfit(_V[:,0],_V[:,1],1); ux=np.array([1,_p[0]])/math.hypot(1,_p[0]); uy=np.array([-ux[1],ux[0]]);   # 4 Oct (Will): along the vineyard road, in the open ground above the arena
mg=[MG+ux*a*F(60)+uy*b*F(30) for a,b in ((-1,-1),(1,-1),(1,1),(-1,1))]
ax.add_patch(MPoly(np.array(mg),closed=True,fc='#9bb35a',ec='#4f7a3a',lw=1.2,alpha=.55,zorder=8))
for k in range(9):
    o=MG+uy*F(-26+k*6.5); ax.plot(*np.array([o-ux*F(56),o+ux*F(56)]).T,color='#4f7a3a',lw=.6,zorder=9)
ax.text(MG[0],MG[1]+F(42),'HUERTA PARA RESTAURANTES · MARKET GARDEN\n120 × 60 ft, camas permanentes · permanent beds',fontsize=6.2,weight='bold',color='#3f6b2a',ha='center',va='center',zorder=15,bbox=dict(boxstyle='round,pad=.25',fc='white',ec='#4f7a3a',lw=.8,alpha=.92))
ax.text(18.6,64,'← campo de alfalfa\n(cercado, al oeste)\nalfalfa field\n(fenced, to the west)',fontsize=6.2,color='#3f6b2a',weight='bold',ha='left',va='center',zorder=15,bbox=dict(boxstyle='round,pad=.25',fc='white',ec='#4f7a3a',lw=.8,alpha=.9))   # 4 Oct (Will): the big fenced field to the west grows alfalfa / feed
ax.text(36,14,'← ganado del rancho más allá de la cerca · the ranch’s cattle, beyond the fence',fontsize=6.2,color='#5c3b22',style='italic',zorder=15,bbox=dict(boxstyle='round,pad=.2',fc='white',ec='none',alpha=.85))
mark(c3+np.array([3,-3]),'o','#4f7a3a','vivero (el antiguo) · the nursery')
mark(c3+np.array([10,-21]),'h','#e0a020','colmenas · beehives',dx=2.2)
sc=np.array(stalls.centroid.coords[0]); mark(sc+np.array([-7,0]),'D','#b5602e','gallinas tras los caballos\nchickens behind the horses',dx=-2.2,ha='right')
mark(bl+np.array([4,-3]),'*','#c2412b','niños, picnic, café · children, picnic, café')
mark(np.array(b2g(-30,-44)),'v','#1f78c8','aguas grises a nativas · greywater to natives',dx=2.2)
mark(np.array(rpen.centroid.coords[0]),'P','#6a3d9a','trabajo pie a tierra\ngroundwork, liberty',dx=-4.2,ha='right')
mark(tr[len(tr)//4],'>','#5f8a6a','paseo y pista · riding and the track',dx=2.2)
north(ax,143,15); scalebar(ax,22,88)
fig.text(0.017,0.947,'Zonas y lugares · Zones and places',fontsize=10,weight='bold',color=INK)
# ---- the closed loops ----
lx=fig.add_axes([0.02,0.055,0.40,0.225]); lx.set_xlim(-1.75,1.75); lx.set_ylim(-1.12,1.12); lx.set_aspect('equal'); lx.axis('off')
CYC=[('Lluvia','Rain','#1f78c8'),('Techos y cisternas','Roofs, cisterns','#1f78c8'),('Bebederos vivos','Living troughs','#1f78c8'),('Caballos','Horses','#7a4a2a'),
     ('Estiércol y cama','Manure, bedding','#7a4a2a'),('Composta BD','BD compost','#5f8a6a'),('Vivero y huerta','Nursery, garden','#4f7a3a'),('Árboles, viña, comida','Trees, vines, food','#4f7a3a'),('Restaurantes, sombra, forraje','Restaurants, shade, fodder','#b5602e')]
n=len(CYC); P=[(math.cos(math.pi/2-2*math.pi*k/n)*1.38,math.sin(math.pi/2-2*math.pi*k/n)*.92) for k in range(n)]
for k in range(n):
    a,b=P[k],P[(k+1)%n]; lx.add_patch(FancyArrowPatch(a,b,connectionstyle='arc3,rad=-.18',arrowstyle='-|>',mutation_scale=9,color='#9b927f',lw=1.1,shrinkA=17,shrinkB=17,zorder=2))
for (es,en,col),(x,y) in zip(CYC,P):
    lx.add_patch(FancyBboxPatch((x-.30,y-.115),.60,.23,boxstyle='round,pad=.02,rounding_size=.08',fc='white',ec=col,lw=1.2,zorder=3))
    lx.text(x,y+.035,es,fontsize=5.8,weight='bold',ha='center',va='center',color=INK,zorder=4); lx.text(x,y-.055,en,fontsize=5.2,ha='center',va='center',color='#6a655a',style='italic',zorder=4)
for (es,en,col),(x,y),to in ((('Cocina y café','Kitchen, café','#b5602e'),(-.42,.3),P[5]),(('Gallinas y lombrices','Chickens, worms','#b5602e'),(0,-.22),P[5]),(('Agua del lavado','Wash water','#1f78c8'),(.42,.3),P[7])):
    lx.add_patch(FancyBboxPatch((x-.27,y-.1),.54,.2,boxstyle='round,pad=.02,rounding_size=.07',fc='#f6f1e6',ec=col,lw=.9,ls='--',zorder=3))
    lx.text(x,y+.03,es,fontsize=5.4,weight='bold',ha='center',va='center',zorder=4); lx.text(x,y-.05,en,fontsize=5,ha='center',va='center',color='#6a655a',style='italic',zorder=4)
    lx.add_patch(FancyArrowPatch((x,y),to,arrowstyle='-|>',mutation_scale=8,color='#c9bfae',lw=.9,ls='--',shrinkA=12,shrinkB=17,zorder=1))
fig.text(0.02,0.29,'Ciclos cerrados: nada sale como basura · Closed loops: nothing leaves as waste',fontsize=8.6,weight='bold',color=INK)
# ---- the numbers ----
horses=22; manure_t=horses*23*365/1000; compost_t=manure_t*.55; roof_m3=(88*46+92*36)*0.623*11*3.785/1000
nx_=0.44; ny_=0.27
fig.text(nx_,ny_,'En números · By the numbers',fontsize=8.6,weight='bold',color=INK)
NUM=[(f'≈ {manure_t:,.0f} t','de estiércol al año (22 caballos × 23 kg/día) · of manure a year'),(f'≈ {compost_t:,.0f} t','de composta terminada · of finished compost'),
     (f'≈ {roof_m3:,.0f} m³','de lluvia de los techos en un año normal · of roof rain in a normal year'),('70 m³','en dos cisternas · in two cisterns'),
     ('0','bolsas de basura de los caballos · bin bags from the horses'),('5','zonas, del establo al cerro · zones, stable to hill')]
for k,(big,txt) in enumerate(NUM):
    yy=ny_-.033-k*.034; fig.text(nx_,yy,big,fontsize=11,weight='bold',color='#5f8a6a'); fig.text(nx_+.075,yy+.002,txt,fontsize=6.3,color=INK,va='baseline')
# ---- notes ----
px=0.70
fig.text(px,0.955,'DISEÑO REGENERATIVO',fontsize=20,weight='bold',color=INK)
fig.text(px,0.93,'Regenerative design · permaculture, biodynamics, community',fontsize=12,color='#555')
NOTES_R=[
 ('Zones','Zonas','Z0 the stable with its kitchen and rooms; Z1 what we touch every day: kitchen garden, herbs, troughs, the grape-shaded pad; Z2 daily work: stalls, runs, round pen, arena, café, chickens; Z3 weekly: the old nursery reborn, orchard, bees, compost, the riding track; Z4 managed native meadow and grazing on rotation, swales on contour; Z5 the hill left wild: chaparral, wildlife, our teacher.','Z0 el establo con su cocina y cuartos; Z1 lo que tocamos cada día: huerto de cocina, hierbas, bebederos, la losa bajo la parra; Z2 trabajo diario: caballerizas, corrales, corral redondo, pista, café, gallinas; Z3 cada semana: el vivero antiguo renacido, frutales, abejas, composta, la pista de paseo; Z4 pradera nativa y pastoreo en rotación, zanjas a nivel; Z5 el cerro silvestre: chaparral, fauna, nuestro maestro.'),
 ('No waste','Sin desperdicio',f'About {manure_t:,.0f} t of manure and bedding a year becomes about {compost_t:,.0f} t of black compost in hot windrows: turned by tractor whenever they pass 65 °C (55 °C for three days kills the weed seeds), finished in six to eight weeks (the Luebke method, from Pfeiffer and Steiner), then cured, for the nursery, the trees and the ranch’s vines. Kitchen and café scraps feed chickens and worms; the chickens follow the horses, scratch the manure flat and eat the fly larvae. Feed in bulk, twine reused, no bin bags from the barn.',f'Unas {manure_t:,.0f} t de estiércol y cama al año se vuelven unas {compost_t:,.0f} t de composta negra en camellones calientes: se voltean con tractor cuando pasan de 65 °C (55 °C por tres días mata las semillas), listos en seis a ocho semanas (método Luebke, de Pfeiffer y Steiner), luego se curan, para el vivero, los árboles y la viña del rancho. Las sobras de cocina y café alimentan gallinas y lombrices; las gallinas siguen a los caballos, extienden el estiércol y se comen las larvas de mosca. Alimento a granel, mecate reusado, ninguna bolsa de basura del establo.'),
 ('Water harvest','Cosecha de agua',f'The roofs give about {roof_m3:,.0f} m³ in a normal year into 70 m³ of cisterns and the living troughs (D-3); first-flush pipes keep it clean; the wash water, with plant soaps only, goes to native beds; swales on contour in Z4 slow the hill water and plant it.',f'Los techos dan unos {roof_m3:,.0f} m³ en un año normal a 70 m³ de cisternas y a los bebederos vivos (D-3); los tubos de primera lluvia la mantienen limpia; el agua del lavado, solo con jabones vegetales, va a camas de nativas; zanjas a nivel en Z4 frenan el agua del cerro y la siembran.'),
 ('The vivero','El vivero','This ground was a plant nursery: it becomes one again. Natives, oaks, fruit trees, vetiver for the troughs and the ranch’s grape cuttings, grown in our own compost, for the site, the ranch and for sale at the café; a seed library for the children.','Este terreno fue un vivero: vuelve a serlo. Nativas, encinos, frutales, vetiver para los bebederos y estacas de la viña, crecidos en nuestra propia composta, para el sitio, el rancho y la venta en el café; una biblioteca de semillas para los niños.'),
 ('Biodynamics','Biodinámica','The centre as one living farm: the biodynamic preparations 502–507 go into every compost windrow, 500 and 501 onto the nursery and the meadow, sowing and transplanting by the biodynamic calendar; horses, chickens and bees together; the valley’s biodynamic wineries as neighbours and partners. Will and Walker keep bees: hives in Z3, facing the morning sun, well away from the runs and paths.','El centro como una sola granja viva: las preparaciones biodinámicas 502–507 en cada camellón de composta, 500 y 501 en el vivero y la pradera, siembra y trasplante según el calendario biodinámico; caballos, gallinas y abejas juntos; las vinícolas biodinámicas del valle como vecinas y socias. Will y Walker son apicultores: colmenas en Z3, hacia el sol de la mañana, lejos de corrales y senderos.'),
 ('Natural horsemanship','Horsemanship natural','Horses living as horses: friends, forage and movement. Every stall opens to its run day and night; slow-feed hay nets; turnout as a small herd on a rotation with real rest for the ground (Holistic planned grazing); barefoot trims; the round pen for groundwork and liberty, never force; clinics with natural-horsemanship trainers.','Caballos que viven como caballos: compañía, forraje y movimiento. Cada caballeriza abre a su corral día y noche; redes de heno de comida lenta; salida en pequeña manada con rotación y descanso real para el suelo (pastoreo planificado holístico); recorte sin herraduras; el corral redondo para trabajo pie a tierra y en libertad, nunca a la fuerza; clínicas con entrenadores de horsemanship natural.'),
 ('Cattle and the whole ranch','Ganado y todo el rancho','The ranch runs cattle: the centre’s horses join that herd as one mixed herd (the Holistic Management handbook’s own example is a mixed herd in Mexico), grazing a paddock for three days or less, then resting it 30 to 90 days, longer in drought; slow growth, slow moves. Chickens follow three days behind, when the fly larvae in the dung are fattest. Planned on the grazing chart, the herd moved by the grass, never by the calendar. Cattle manure into the windrows too: the compost Steiner valued most. The big fenced field to the west grows alfalfa or other feed: hay for the stalls, the herd grazes the stubble after the last cut, and the compost goes back on it, so the feed loop closes on the ranch.','El rancho cría ganado: los caballos del centro se suman a ese hato como una sola manada mixta (el ejemplo del propio manual de Manejo Holístico es una manada mixta en México), tres días o menos por potrero, luego 30 a 90 días de descanso, más en sequía; crecimiento lento, movimientos lentos. Las gallinas siguen tres días después, cuando las larvas de mosca en el estiércol están más gordas. Planificado en el cuadro de pastoreo, el hato se mueve según el pasto, nunca según el calendario. El estiércol de vaca también a los camellones: la composta que Steiner más valoraba. El campo grande cercado al oeste da alfalfa u otro forraje: heno para las caballerizas, el hato pastorea el rastrojo después del último corte y la composta regresa a él, así el ciclo del alimento se cierra en el rancho.'),
 ('Food for restaurants','Comida para restaurantes','A market garden of permanent beds by the main road (beside its water main): salad greens, herbs, edible flowers and heirloom vegetables for the valley’s restaurants, picked in the morning, delivered by noon; fruit and nuts from the orchard and food forest in Z3 as it grows; eggs from the chickens. Fed with our compost, watered by drip from the cisterns first.','Una huerta de camas permanentes junto al camino principal (junto a su línea de agua): verduras de hoja, hierbas, flores comestibles y hortalizas criollas para los restaurantes del valle, cosechadas en la mañana y entregadas al mediodía; fruta y nueces del huerto y el bosque comestible en Z3 conforme crezca; huevos de las gallinas. Alimentada con nuestra composta, regada por goteo primero desde las cisternas.'),
 ('The compost yard','El patio de composta','Located on the map where the first outdoor paddocks were drawn: south of the track, about 90 ft in from the scrub-side road (truck access for straw and cattle manure, but not on it), on ground that takes almost no runoff, a tractor haul round the track from both stables and close to the nursery. Four windrows 60 ft long on a compacted pad, a small berm downhill, a roofed corner for the biodynamic preparations and the finished pile. Turned when it passes 65 °C, not more than it needs; watered from the stalls’ cistern; ready in six to eight weeks, then cured.','Ubicado en el mapa donde se dibujaron los primeros corrales exteriores: al sur de la pista, a unos 27 m del camino del matorral (acceso de camión para paja y estiércol de vaca, sin estar encima), en terreno que casi no recibe escurrimiento, a un viaje de tractor por la pista desde los dos establos y cerca del vivero. Cuatro camellones de 60 ft sobre un patio compactado, un bordo pequeño cuesta abajo, una esquina techada para las preparaciones biodinámicas y la composta terminada. Se voltea cuando pasa de 65 °C, no más de lo necesario; se riega desde la cisterna de las caballerizas; lista en seis a ocho semanas, luego se cura.'),
 ('Community and children','Comunidad y niños','A place to come back to: the café and the picnic bleachers; school visits and summer days where children brush and feed the horses, plant in the vivero, open a hive with a veil on and turn the compost; animals you can touch; therapeutic riding; workshops on compost, bees and horses; local people working here.','Un lugar al que se regresa: el café y las gradas del día de campo; visitas escolares y días de verano donde los niños cepillan y alimentan a los caballos, siembran en el vivero, abren una colmena con velo y voltean la composta; animales que se dejan tocar; equinoterapia; talleres de composta, abejas y caballos; gente del lugar trabajando aquí.'),
]
y=0.902
for k,(en,es,ten,tes) in enumerate(NOTES_R):
    fig.text(px,y,f'{k+1}',fontsize=10,weight='bold',color='#5f8a6a')
    fig.text(px+.018,y,f'{es} · {en}',fontsize=8.4,weight='bold',color=INK)
    ly=y-.0135
    for line in textwrap.wrap(tes,118): fig.text(px+.018,ly,line,fontsize=5.4,color=INK); ly-=.0073
    for line in textwrap.wrap(ten,118): fig.text(px+.018,ly,line,fontsize=5.4,color='#6a655a',style='italic'); ly-=.0073
    y=ly-.0036
print('notes end at', round(ly,3))
fig.text(px,0.09,'Fuentes · Sources (PDC library): Holistic Management Handbook + grazing planning manual ·\nCompost and Soil Biology course notes · Salatin (Pathways to ReLocalization) · Mollison, Permaculture II',fontsize=6.2,color='#6a655a',va='top',linespacing=1.4)
if not globals().get('PACK'): fig.savefig('A2-regenerative.png',dpi=170); print('ok')
