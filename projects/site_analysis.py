exec(open('drain.py',encoding='utf-8').read())
# Sheet A-1 · Lectura del sitio · Reading the site (4 Oct 2026, Will: "add some analysis"). Permaculture sector analysis from real
# data: seasonal wind roses (Open-Meteo / ERA5, hourly 2016-25, wind_roses_2016_2025.json), solstice sun angles, water flow (the
# drainage model), the Santa Ana fire sector, views; and the design checked against Yeomans' Scale of Permanence.
import textwrap, json as _json
from matplotlib.patches import Wedge, FancyArrowPatch, Polygon as MPoly
WR=_json.load(open('wind_roses_2016_2025.json'))
SUN='#e0a020'; WINDC='#2f6fa8'; FIRE='#c2412b'; VIEW='#4f7a3a'
fig=plt.figure(figsize=(17,11),dpi=170); fig.patch.set_facecolor(globals().get('PAPER','white')); fig._norm_single=True
ax=base_axes(fig,[0.015,0.30,0.665,0.64],alpha=.42)
contours(ax,z); features(ax); works(ax); ax.set_xlim(18,150); ax.set_ylim(92,8)
# concentrated flow (over 1/3 acre), quietly
segs=[];ws=[]
for n_ in range(W*H):
    a_=acc.flat[n_]*A_ac
    if a_<.33 or down[n_]<0: continue
    i_,j_=n_%W,n_//W; d_=down[n_]; segs.append([(i_,j_),(d_%W,d_//W)]); ws.append(.4+min(2.2,a_*.25))
ax.add_collection(LineCollection(segs,linewidths=ws,colors=WATER,alpha=.55,zorder=6,capstyle='round'))
stb=np.array(byname('walker barn 72x40')[0]['c'])
def bvec(bearing):                                   # compass bearing (deg from true north) -> unit vector in grid coords
    a=GR(la0,lo0); b=GR(la0+math.cos(math.radians(bearing))*1e-4, lo0+math.sin(math.radians(bearing))*1e-4/math.cos(math.radians(la0)))
    v=np.array(b)-np.array(a); return v/np.linalg.norm(v)
def gang(bearing): v=bvec(bearing); return math.degrees(math.atan2(v[1],v[0]))
# ---- sun: solstice and equinox sunrise / sunset bearings at 32 N (cos Az = sin dec / cos lat) ----
lat=math.radians(32.0)
for dec,col,lab in ((23.44,SUN,'21 jun'),(0,'#d9b65a','equinoccio · equinox'),(-23.44,'#b98a2a','21 dic · dec')):
    az=math.degrees(math.acos(math.sin(math.radians(dec))/math.cos(lat)))
    for b_,word in ((az,'sale · rise'),(360-az,'pone · set')):
        v=bvec(b_); p=stb+v*30
        ax.plot([stb[0]+v[0]*10,p[0]],[stb[1]+v[1]*10,p[1]],color=col,lw=1.6,dashes=(6,3),zorder=11)
        ax.add_patch(matplotlib.patches.Circle(p,1.2,fc=col,ec='white',lw=.8,zorder=12))
        if dec!=0: ax.text(p[0]+v[0]*4.2,p[1]+v[1]*4.2,f'{lab}\n{word} {b_:.0f}°',fontsize=5.6,color=INK,ha='center',va='center',zorder=13,bbox=dict(boxstyle='round,pad=.15',fc='white',ec='none',alpha=.8))
# ---- wind: the afternoon sea breeze from the W, winter's cold NE and the Santa Anas ----
for b_,col,w_,lab in ((270,WINDC,5.5,'brisa del mar, tardes · afternoon sea breeze\nW 53 % · SW 20 % · NW 17 % de las horas de tarde'),
                      (45,FIRE,4.5,'invierno y Santa Ana · winter and Santa Ana\nNE 33 % en invierno · ~8 días Santa Ana al año')):
    v=bvec(b_); a=stb+v*(40 if b_==270 else 30); b=stb+v*13
    ax.add_patch(FancyArrowPatch(a,b,arrowstyle='simple,head_width=8,head_length=8,tail_width=%g'%w_,color=col,alpha=.75,zorder=12,mutation_scale=1.6))
    ax.text(a[0]+v[0]*3+(0 if b_==270 else -12),a[1]+v[1]*3+(-3 if b_==270 else -4),lab,fontsize=6.2,color=col,weight='bold',ha='center',va='center',zorder=13,bbox=dict(boxstyle='round,pad=.2',fc='white',ec='none',alpha=.85))
# fire sector: NE to E, the Santa Ana quarter
ax.add_patch(Wedge(stb,40,gang(100),gang(20),width=14,fc=FIRE,alpha=.07,ec=FIRE,lw=.8,ls='--',zorder=5))
v=bvec(75); q=stb+v*33; ax.text(q[0],q[1],'sector de fuego\nfire sector',fontsize=6.4,color=FIRE,ha='center',va='center',zorder=13,weight='bold')
# views: north over the vineyard to the valley
for b_ in (330,20):
    v=bvec(b_); ax.annotate('',xy=stb+v*34,xytext=stb+v*12,arrowprops=dict(arrowstyle='->',color=VIEW,lw=1.4,ls='--'),zorder=11)
v=bvec(355); q=stb+v*37; ax.text(q[0],q[1],'vistas al viñedo y al valle · views to the vineyard and valley',fontsize=6.2,color=VIEW,ha='center',zorder=13,bbox=dict(boxstyle='round,pad=.2',fc='white',ec='none',alpha=.8))
ax.add_patch(matplotlib.patches.Circle(stb,.9,fc=INK,ec='white',lw=.8,zorder=14))
north(ax,143,15); scalebar(ax,22,88)
fig.text(0.017,0.947,'Sectores · Sectors',fontsize=10,weight='bold',color=INK)
# ---- seasonal wind roses ----
SEAS=[('DJF','invierno · winter'),('MAM','primavera · spring'),('JJA','verano · summer'),('SON','otoño · fall')]
BIN=['#9ec3e0','#4f8fc4','#1f4f80']
for k,(key,lab) in enumerate(SEAS):
    pa=fig.add_axes([0.03+k*0.168,0.075,0.13,0.155],projection='polar'); pa.set_theta_zero_location('N'); pa.set_theta_direction(-1)
    S_=WR['seasons'][key]; n=S_['n']; th=np.radians(np.arange(16)*22.5); bot=np.zeros(16)
    for b in range(3):
        h_=np.array([c[b] for c in S_['counts']])/n*100
        pa.bar(th,h_,width=np.radians(20),bottom=bot,color=BIN[b],edgecolor='white',lw=.3); bot+=h_
    pa.set_ylim(0,max(12,bot.max()*1.05)); pa.set_yticks([]); pa.set_xticks(np.radians([0])); pa.set_xticklabels(['N'],fontsize=6)
    pa.tick_params(pad=-2); pa.set_facecolor('none'); pa.spines['polar'].set_color('#b9b2a6'); pa.grid(color='#d8d2c4',lw=.4)
    pa.set_title(lab,fontsize=7.5,pad=4)
fig.text(0.02,0.282,'Rosas de viento por temporada · Seasonal wind roses',fontsize=8.6,weight='bold',color=INK)
fig.text(0.02,0.268,'Horas por dirección (de donde viene el viento); azul claro < 8 mph, medio 8–16, oscuro ≥ 16. ERA5 2016–25 vía Open-Meteo · Hours by direction the wind comes from; light < 8 mph, mid 8–16, dark ≥ 16.',fontsize=5.4,color='#6a655a',style='italic')
# ---- sun path ----
sp=fig.add_axes([0.725,0.085,0.255,0.24])
for dec,col,lab in ((23.44,SUN,'21 jun'),(0,'#d9b65a','equinoccio'),(-23.44,'#b98a2a','21 dic')):
    H=np.radians(np.linspace(-180,180,721)); d_=math.radians(dec)
    alt=np.degrees(np.arcsin(np.sin(lat)*math.sin(d_)+np.cos(lat)*math.cos(d_)*np.cos(H)))
    az=np.degrees(np.arctan2(np.sin(H),np.cos(H)*math.sin(lat)-math.tan(d_)*math.cos(lat)))+180
    m_=alt>0; sp.plot(az[m_],alt[m_],color=col,lw=1.8); i_=np.argmax(alt); sp.text(az[i_],alt[i_]+2.5,f'{lab} · {alt[i_]:.0f}°',fontsize=6,ha='center',color=INK)
# the stable's south roof plane: 13.4 deg, facing 204 (SSW)
sp.axvspan(204-45,204+45,color='#1d2b3a',alpha=.06); sp.text(204,4,'techo solar SSO · solar roof SSW',fontsize=5.6,ha='center',color='#1d2b3a')
sp.set_xlim(45,315); sp.set_ylim(0,90); sp.set_xticks([60,90,120,150,180,210,240,270,300]); sp.set_xticklabels(['ENE','E','ESE','SE','S','SO','OSO','O','ONO'],fontsize=5.6)
sp.set_yticks([0,30,60,90]); sp.tick_params(labelsize=5.6); sp.set_ylabel('altura · altitude °',fontsize=6)
for s_ in ('top','right'): sp.spines[s_].set_visible(False)
sp.set_facecolor('none'); fig.text(0.70,0.35,'Trayectoria del sol, 32° N · Sun path, 32° N',fontsize=8.6,weight='bold',color=INK)
# ---- notes ----
px=0.70
fig.text(px,0.955,'LECTURA DEL SITIO',fontsize=20,weight='bold',color=INK)
fig.text(px,0.93,'Reading the site · sectors, climate, permanence',fontsize=12,color='#555')
NOTES_A=[
 ('Climate','Clima','Mediterranean: about 280 mm of rain, nearly all December to March; long dry summers; hot, still days on the valley floor and cool nights; frost is rare but the low ground holds the cold. Design for drought first, then for the few big storms.','Mediterráneo: unos 280 mm de lluvia, casi toda de diciembre a marzo; veranos largos y secos; días calientes y quietos en el fondo del valle y noches frescas; heladas raras, pero el terreno bajo guarda el frío. Diseñar primero para la sequía, luego para las pocas tormentas grandes.'),
 ('Wind','Viento','Afternoons belong to the sea breeze: from the west 53 % of the hours, SW 20 %, NW 17 %. Winter turns it around: NE is the most common wind (33 %), cold air sliding down the valley at night, and about eight Santa Ana days a year (October to February) bring the strongest gusts, up to 56 mph. So: the stable’s solid west end and its backed west doors break the daily wind; the east end will need panels for the winter NE.','Las tardes son de la brisa del mar: del oeste 53 % de las horas, SO 20 %, NO 17 %. El invierno la voltea: el NE es el viento más común (33 %), aire frío que baja por el valle de noche, y unos ocho días de Santa Ana al año (octubre a febrero) traen las rachas más fuertes, hasta 90 km/h. Así: el extremo oeste macizo del establo y sus puertas forradas frenan el viento diario; el extremo este necesitará paneles para el NE de invierno.'),
 ('Sun','Sol','At 32° N the summer sun rises at 62° (ENE) and climbs to 81°; in winter it rises at 118° (ESE) and reaches only 35°. Deep eaves, the covered stalls and the grape trellis shade the summer; the low winter sun reaches into the open stalls and dries the runs. The stable’s south roof faces 204° at 13°: the best solar plane on the site.','A 32° N el sol de verano sale a 62° (ENE) y sube a 81°; en invierno sale a 118° (ESE) y solo llega a 35°. Aleros profundos, las caballerizas techadas y la parra dan sombra en verano; el sol bajo de invierno entra en las caballerizas abiertas y seca los corrales. El techo sur del establo ve a 204° a 13°: el mejor plano solar del sitio.'),
 ('Water','Agua','About 16 acres of hillside drain toward the site from the south-east; the water runs north-west down the natural low line to the sink below the track (sheet D-1). Everything that sheds water, roofs, roads and the hill, is slowed, spread and sunk before it leaves.','Unas 6.5 ha de ladera escurren hacia el sitio desde el sureste; el agua corre al noroeste por la línea baja natural hasta el bajo de la pista (hoja D-1). Todo lo que suelta agua, techos, caminos y el cerro, se frena, se reparte y se infiltra antes de salir.'),
 ('Fire','Fuego','The danger comes with the Santa Anas, from the NE and E, dry and fast, across the chaparral of the hill to the south. Stone walls, metal roofs and no hay in the stable already help; keep 30 m of lean, green, watered ground around the buildings, a fire-hose coupling on each cistern (70 m³ on site) and the roads as fire breaks.','El peligro llega con los Santa Ana, del NE y E, secos y rápidos, sobre el chaparral del cerro al sur. Los muros de piedra, techos metálicos y nada de paja en el establo ya ayudan; mantener 30 m de terreno limpio, verde y regado alrededor de los edificios, una toma de bombero en cada cisterna (70 m³ en sitio) y los caminos como cortafuegos.'),
 ('The scale of permanence','La escala de permanencia','Yeomans: decide in the order things are hard to change. Climate (read above) → landform (the slope kept, grading minimal) → water (gully, waterway, cisterns, troughs) → roads (on the contour, with the water) → trees (old nursery, pines and palms kept, natives added) → buildings (on the level ground, out of the flow) → fences (follow the use) → soil (built every year by compost, sheet A-2).','Yeomans: decidir en el orden de lo difícil de cambiar. Clima (arriba) → forma del terreno (la pendiente se respeta, terracería mínima) → agua (zanja, canal, cisternas, bebederos) → caminos (en curva de nivel, con el agua) → árboles (vivero antiguo, pinos y palmas se quedan, nativas se suman) → edificios (en lo plano, fuera del escurrimiento) → cercas (siguen el uso) → suelo (se construye cada año con composta, hoja A-2).'),
]
y=0.902
for k,(en,es,ten,tes) in enumerate(NOTES_A):
    fig.text(px,y,f'{k+1}',fontsize=10,weight='bold',color='#b5602e')
    fig.text(px+.018,y,f'{es} · {en}',fontsize=8.6,weight='bold',color=INK)
    ly=y-.014
    for line in textwrap.wrap(tes,107): fig.text(px+.018,ly,line,fontsize=6.1,color=INK); ly-=.0087
    for line in textwrap.wrap(ten,107): fig.text(px+.018,ly,line,fontsize=6.1,color='#6a655a',style='italic'); ly-=.0087
    y=ly-.0045
print('notes end at', round(ly,3))
fig.text(0.02,0.03,'31.9999 N, 116.7641 W · Hoja / Sheet A-1 · 4 oct 2026 · Viento: Open-Meteo.com (CC BY 4.0), ERA5 · Diseño preliminar · Preliminary design',fontsize=8,color='#6a655a')
if not globals().get('PACK'): fig.savefig('A1-site-analysis.png',dpi=170); print('ok')
