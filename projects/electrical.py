exec(open('drain.py',encoding='utf-8').read())
# Sheet E-1 · Plan eléctrico, iluminación y solar · Electrical, lighting and solar plan (4 Oct 2026, Will): power from the ranch's
# main buildings in the main-road water trench (Andrés), a main disconnect where it enters the site, a small electrical room,
# dark-sky lighting for both stables and the site, solar on both roofs (potential + a first phase), room for two renderings.
import matplotlib.patches as mpatches, textwrap, json as _json
from matplotlib.patches import Polygon as MPoly, Circle as MCircle, Rectangle as MRect, Wedge
_O=_json.load(open('stable_origin.json')); _r=math.radians(_O['rot']); _ROT=math.radians(90-65.84)
def b2g(bx,by):                                        # stable frame ft (x east along the aisle, y north) -> site grid
    x=(bx*math.cos(_ROT)-by*math.sin(_ROT))*FT; y=(bx*math.sin(_ROT)+by*math.cos(_ROT))*FT
    return (_O['grid'][0]+(x*math.cos(_r)-y*math.sin(_r))/cs, _O['grid'][1]-(x*math.sin(_r)+y*math.cos(_r))/cs)
import geo as _g0                                      # covered stalls frame (covered_stalls.py): x along the corridor toward the NE, y across
_st=[(-116.7637927468709,31.99970749966619),(-116.7635094983617,31.99998532313917),(-116.7633790473066,31.99988684382775),(-116.7636714287398,31.99959200352455)]
_k=111320*math.cos(math.radians(_g0.la0)); _enu=lambda la,lo:np.array([(lo-_g0.lo0)*_k,(la-_g0.la0)*111320])
_A,_B,_C,_D=(_enu(la,lo) for lo,la in _st); _u=(_B-_A)/np.linalg.norm(_B-_A); _v=(_D-_A)/np.linalg.norm(_D-_A); _v=_v-_u*(_v@_u); _v/=np.linalg.norm(_v)
def s2g(x,y):
    e=_A+(_u*(70+x)+_v*(28+y))*FT; return GR(_g0.la0+e[1]/111320,_g0.lo0+e[0]/_k)
def pts_of(name): return np.array([q[:2] for q in byname(name)[0]['pts']])
POW='#6a3d9a'; AMBER='#e39a2d'; WARM='#f2c14e'; PV='#1d2b3a'; PVF='#3c5878'
# ---------------- numbers ----------------
PANEL=(5.64,3.71,435)                                  # 1722 x 1134 mm all-black module, 435 W
YIELD=dict(stS=1743,stN=1390,stalls=1600)              # kWh per kWp a year, PVGIS (NSRDB) 31.9999 N 116.7641 W, 14 % losses: stable S half 13.4° az 204°, N half az 24°, butterfly 4.8° both ways (1565/1634)
def rows_cols(depth,length,margin=(1.5,1.0)):
    return int((depth-margin[0]-margin[1])//PANEL[1]), int((length-3)//PANEL[0])
st_r,st_c=rows_cols(18/math.cos(math.radians(13.4)),88)          # 4 Oct: the stable is 84 ft (88 with overhangs)          # stable half: eave (with overhang) to the clerestory edge, along the slope
sl_r,sl_c=rows_cols(18,92)                                        # each butterfly plane: eave to valley
N_ST=st_r*st_c; N_SL=2*sl_r*sl_c; kw=lambda n:n*PANEL[2]/1000
PV_ROWS=[('Establo, mitad sur · Stable, south half','13° SSO · SSW',N_ST,YIELD['stS']),('Establo, mitad norte · Stable, north half','13° NNE',N_ST,YIELD['stN']),('Caballerizas, techo mariposa · Covered stalls, butterfly','5° NO/SE · NW/SE',N_SL,YIELD['stalls'])]
PH1=16; PH1_KW=kw(PH1); PH1_MWH=PH1_KW*YIELD['stS']/1000
LOADS=[('Luces interiores · Indoor lights',0.6,3),('Luces exteriores bajas · Low outdoor lights',.15,5),('Pista y corral redondo, 3 noches/sem · Arena + round pen, 3 nights/wk',1.7,1.5*3/7),
       ('Bombas de bebederos (4) · Trough pumps (4)',.16,12),('Bombas de cisternas (2) · Cistern pumps (2)',1.5,1),('Ventiladores, verano · Stall fans, summer',1.8,10/2),
       ('Agua caliente: lavado y baño · Hot water: wash + bathroom',.5,8),('Cocina: refri, inducción, café · Kitchen: fridge, induction, coffee',.6,5),('Monturas: refri y varios · Tack fridge + small loads',.25,10),('Café, días de evento · Café trailer, event days',2,2)]
DAY=sum(k*h for _,k,h in LOADS); YEAR=DAY*365
POT_KW=sum(kw(n) for _,_,n,_ in PV_ROWS); POT_MWH=sum(kw(n)*y/1000 for _,_,n,y in PV_ROWS)
print(f'PV: stable half {N_ST} panels ({st_r}x{st_c}), stalls {N_SL}; potential {POT_KW:.1f} kWp {POT_MWH:.0f} MWh/yr; use {DAY:.1f} kWh/day {YEAR:,.0f}/yr; phase 1 {PH1_KW:.1f} kWp {PH1_MWH:.1f} MWh')
# ---------------- figure ----------------
fig=plt.figure(figsize=(17,11),dpi=170); fig.patch.set_facecolor(globals().get('PAPER','white'))
ax=base_axes(fig,[0.012,0.565,0.385,0.375],alpha=.40)
contours(ax,z); features(ax)
ax.set_xlim(24,150); ax.set_ylim(88,14)
def foot_of(name):
    o=byname(name); return np.array(foot(o[0])) if o else None
# the electrical room (stable frame, south of C1, west of the pad trough) and cistern C1 for reference
ER=[(-48,-21),(-36,-21),(-36,-15),(-48,-15)]                        # 4 Oct (Will): inside the stable's new SW corner bay
P=np.array([b2g(*q) for q in ER+ER[:1]]); ax.fill(P[:,0],P[:,1],color=POW,alpha=.85,zorder=9)
erc=np.array(b2g(-48,-18))
# feeders: along the main road (shared trench with the water main), then branches
mr=pts_of('main road, north-east gate to south gate'); br=pts_of('barn to cross-fence road')
def along(path,target):
    i=int(np.argmin(np.hypot(path[:,0]-target[0],path[:,1]-target[1]))); return i
i_er=along(mr,erc); feed=np.vstack([mr[:i_er+1],[erc]])
ax.plot(feed[:,0],feed[:,1],color=POW,lw=2.4,zorder=10,solid_capstyle='round')
sp2=np.array(s2g(-46,-7)); j=along(br,sp2); i_b=along(mr,br[0])
b2=np.vstack([[erc],br[:j+1],[sp2]]); ax.plot(b2[:,0],b2[:,1],color=POW,lw=1.5,zorder=10,dashes=(5,2))
bl=np.array(byname('bleachers')[0]['c']); sp3=bl+np.array([1.6,1.6]); i_bl=along(mr,sp3)
b3=np.vstack([mr[i_bl:i_er+1][::-1],[sp3]]) if i_bl>i_er else np.vstack([[mr[i_bl]],[sp3]])
ax.plot(b3[:,0],b3[:,1],color=POW,lw=1.5,zorder=10,dashes=(5,2))
g=pts_of('gate · north-east, main road').mean(axis=0)
ax.add_patch(MRect((g[0]-1.1,g[1]+.6),2.2,2.2,facecolor='white',edgecolor=POW,lw=1.8,zorder=13)); ax.text(g[0],g[1]+1.7,'MD',fontsize=5.2,weight='bold',color=POW,ha='center',va='center',zorder=14)
ax.annotate('',xy=(g[0]+.4,g[1]-.2),xytext=(g[0]+7,g[1]-5.5),arrowprops=dict(arrowstyle='-|>',color=POW,lw=1.6,ls=(0,(3,2))),zorder=13)
ax.text(g[0]+7.4,g[1]-5.9,'desde los edificios del rancho\nfrom the ranch buildings (Andrés)',fontsize=6,color=POW,ha='left',va='bottom',zorder=13)
for (x,y),lab in ((sp2,'SP-2'),(sp3,'SP-3')):
    ax.add_patch(MRect((x-.9,y-.9),1.8,1.8,facecolor='white',edgecolor=POW,lw=1.4,zorder=13)); ax.text(x,y-1.6,lab,fontsize=5.6,weight='bold',color=POW,ha='center',va='bottom',zorder=13)
# lights on the site
def dots(pts,col,s=11,mk='o',ec=INK,z=14): pts=np.array(pts); ax.scatter(pts[:,0],pts[:,1],s=s,c=col,marker=mk,edgecolors=ec,linewidths=.5,zorder=z)
wp=pts_of('walking path, parking to barn'); L=np.r_[0,np.cumsum(np.hypot(*np.diff(wp,axis=0).T))]
bol=[wp[int(np.argmin(abs(L-d)))] for d in np.linspace(L[-1]*.08,L[-1]*.92,5)]
pk=np.array([q[:2] for s_ in S if s_.get('name')=='parking stall' for q in s_['pts']])
bol+= [(x,pk[:,1].min()-.9) for x in np.linspace(pk[:,0].min()+1,pk[:,0].max()-1,4)]
dots(bol,AMBER,10)
for gn in ('gate · north-east, main road','gate · east, parking'): q=pts_of(gn).mean(axis=0); dots([q+np.array([.9,.9])],AMBER,22,'s')
def poles(name,fr,off,n_r=None):
    P=foot_of(name); c=P.mean(0); U,Sv,Vt=np.linalg.svd(P-c); a=Vt[0]; bvec=Vt[1]
    pa=(P-c)@a; pb=(P-c)@bvec; out=[]
    if n_r:                                                       # round: n poles on a circle
        r=np.abs(pa).max()+off
        for k in range(n_r): t=2*math.pi*k/n_r+.5; out.append((c+r*(math.cos(t)*a+math.sin(t)*bvec),c))
    else:
        for f in fr:
            for sg in (-1,1): out.append((c+a*f*np.abs(pa).max()+bvec*sg*(np.abs(pb).max()+off),c+a*f*np.abs(pa).max()))
    for p_,aim in out:
        d=(np.array(aim)-p_); ang=math.degrees(math.atan2(d[1],d[0]))
        ax.add_patch(Wedge(p_,3.2,ang-28,ang+28,facecolor=WARM,edgecolor='none',alpha=.75,zorder=12)); dots([p_],INK,9,'o','white',15)
    return len(out)
NARENA=poles('arena fence',(-.62,0,.62),.45); NRP=poles('round pen fence',None,.45,n_r=3)
# the buildings: a warm wash where the lights are (detail in the insets)
for n in ('walker barn 72x40','covered stalls'):
    F=foot_of(n); ax.fill(F[:,0],F[:,1],color=WARM,alpha=.55,zorder=6)
tr=foot_of('trailer 8 x 40'); dots([bl+np.array([-1.2,-1.2])],AMBER,10)
for nm,xy in (('track',None),):
    t_=pts_of('track'); q=t_.mean(axis=0); ax.text(q[0]+4,q[1]+7,'pista sin luz · track unlit',fontsize=6.2,color=MUTED if 'MUTED' in globals() else '#6a655a',rotation=0,ha='right',zorder=13,bbox=dict(boxstyle='round,pad=.2',fc='white',ec='none',alpha=.75))
q=mr[len(mr)//3]; ax.text(q[0]+2,q[1],'caminos sin luz · roads unlit',fontsize=6.2,color='#6a655a',ha='left',zorder=13,bbox=dict(boxstyle='round,pad=.2',fc='white',ec='none',alpha=.75))
north(ax,143,22); scalebar(ax,28,84)
CALLE=[((g[0]-4.2,g[1]+1.2),1),((erc[0]-3.6,erc[1]+2.6),2),((b2g(0,30)[0]+2.5,b2g(0,30)[1]-2.5),3),((sp2[0]-3.5,sp2[1]+3),4),((np.array(foot_of('arena fence')).mean(0)[0]-6,np.array(foot_of('arena fence')).mean(0)[1]),5)]
for xy,n in CALLE: callout(ax,xy,n)
# legend (in the map's empty north-west corner)
lg=[(POW,'-',2.4,'Alimentación del rancho, en la zanja del agua · Ranch feed, in the water-main trench'),(POW,'--',1.5,'Ramal enterrado · Buried branch'),
    (AMBER,'o',0,'Bolardo ámbar 24 in / poste de puerta · Amber 24 in bollard / gate light'),(WARM,'>',0,'Poste de pista, apuntado hacia adentro · Arena pole, aimed in'),(POW,'s',0,'MD desconexión principal · SP subtablero · ER cuarto eléctrico')]
for k,(c,st,lw,tx) in enumerate(lg):
    yy=19.2+k*2.55; xx=26.5
    if lw: ax.plot([xx,xx+3.2],[yy,yy],color=c,lw=lw,ls=st,zorder=16)
    else: ax.scatter([xx+1.6],[yy],s=16,c=c,marker=st,edgecolors=INK,linewidths=.4,zorder=16)
    ax.text(xx+4.2,yy,tx,fontsize=5.6,va='center',color=INK,zorder=16,bbox=dict(boxstyle='square,pad=.1',fc='white',ec='none',alpha=.7))
fig.text(0.014,0.947,'Sitio · Site',fontsize=10,weight='bold',color=INK)

# ---------------- stable inset: lights, outlets, the electrical room ----------------
sx=fig.add_axes([0.405,0.565,0.30,0.375]); sx.set_aspect('equal'); sx.axis('off'); sx.set_xlim(-70,46); sx.set_ylim(-46,27); sx.set_gid('stable-electrical')
fig.text(0.407,0.947,'Establo y cuarto eléctrico · Stable and electrical room',fontsize=10,weight='bold',color=INK)
LN=dict(color=INK,lw=.7)
sx.add_patch(MRect((-48,-21),84,42,fc='#efe6d2',ec=INK,lw=1.8)); sx.add_patch(MRect((-48,-7),84,14,fc='#f7f1e3',ec='none'))   # 4 Oct: 84 ft, the new west bay
for k in range(6): sx.add_patch(MRect((-36+12*k,7),12,14,fc='none',ec=INK,lw=.5))
for k in range(4): sx.add_patch(MRect((-12+12*k,-21),12,14,fc='none',ec=INK,lw=.5))
sx.add_patch(MRect((-36,-21),12,14,fc='#ddd8cf',ec=INK,lw=1)); sx.add_patch(MRect((-24,-21),12,14,fc='#ddd8cf',ec=INK,lw=1))
sx.add_patch(MRect((-48,7),12,14,fc='#f6e3c8',ec=INK,lw=1)); sx.text(-42,18.2,'cocina\nkitchen',fontsize=5.4,ha='center',va='center',color='#6a655a')
sx.add_patch(MRect((-48,-15),12,8,fc='#dcecf4',ec=INK,lw=1)); sx.text(-41,-9.6,'baño · bath',fontsize=5.0,ha='center',va='center',color='#6a655a')
sx.add_patch(MRect((-48,-21),12,6,fc='#e9e2f2',ec=POW,lw=1.6)); sx.text(-42,-20.4,'ER',fontsize=6.0,weight='bold',color=POW,ha='center',va='bottom')
sx.text(-30,-17.5,'lavado\nwash',fontsize=5.6,ha='center',va='center',color='#6a655a'); sx.text(-18,-17.5,'monturas\ntack/feed',fontsize=5.6,ha='center',va='center',color='#6a655a')
for k in range(6): sx.text(-30+12*k,18.6,f'{k+1}',fontsize=5.6,ha='center',color='#6a655a')
for k in range(4): sx.text(-6+12*k,-19.4,f'{k+7}',fontsize=5.6,ha='center',color='#6a655a')
sx.add_patch(MRect((-48,-33.75),36,12,fc='#e4e1da',ec=INK,lw=.6)); sx.text(-24,-31.6,'losa · pad 12 × 36',fontsize=5.6,ha='center',color='#6a655a')
sx.add_patch(MRect((-51,-36.75),3,13.5,fc='#a9c6dc',ec=INK,lw=.5))
sx.add_patch(MRect((-66.5,-41.5),13,13,fc='none',ec=WATER,lw=1,ls=(0,(3,2)))); sx.text(-60,-35,'C1',fontsize=6.5,color=WATER,ha='center',va='center',weight='bold')
for (x,y,t) in ((-45.2,-17.6,'MP'),(-42,-17.6,'INV'),(-38.8,-17.6,'BAT')):
    sx.add_patch(MRect((x-1.3,y-.9),2.6,1.5,fc='white',ec=POW,lw=.7)); sx.text(x,y-.15,t,fontsize=3.7,color=POW,ha='center',va='center')
sx.add_patch(MRect((-48.4,-20.2),.8,3,fc='white',ec='none',zorder=7))                     # its outside door in the west gable
sx.plot([-48.9,-48.9],[-16.6,-15.4],color=POW,lw=2.4,zorder=8)                           # shut-off + PV rapid shutdown beside the door
sx.annotate('puerta exterior, desconexión + paro solar\noutside door, shut-off + PV rapid shutdown',xy=(-49.2,-18.5),xytext=(-50.5,-3),fontsize=4.6,color=POW,ha='right',va='center',arrowprops=dict(arrowstyle='-',color=POW,lw=.6))
# fixtures
def L(x,y,kind,s=26):
    st=dict(L1=('o',WARM,INK),L2=('o','white',INK),L3=('s',WARM,INK),L4=('v',AMBER,INK),L5=('o',AMBER,INK))[kind]
    sx.scatter([x],[y],s=s,marker=st[0],c=st[1],edgecolors=st[2],linewidths=.7,zorder=8)
    if kind=='L1': sx.plot([x-.9,x+.9],[y-.9,y+.9],color=INK,lw=.5,zorder=9); sx.plot([x-.9,x+.9],[y+.9,y-.9],color=INK,lw=.5,zorder=9)
def OUT(x,y,ang=0,col=INK):
    sx.scatter([x],[y],s=18,marker=(3,0,ang),c='white',edgecolors=col,linewidths=.8,zorder=8)
for x in (-36,-24,-12,0,12,24): L(x,0,'L1')
for k in range(6): L(-30+12*k,14,'L2'); OUT(-27+12*k,7.9,180)
for k in range(4): L(-6+12*k,-14,'L2'); OUT(-3+12*k,-7.9,0)
for x,y in ((-32.5,-11),(-27.5,-11),(-20.5,-11),(-15.5,-11),(-45,13),(-39,13),(-44.5,-11.5),(-35.6,-18)): L(x,y,'L3',20)
for x,y in ((-33,-15),(-26.5,-9.5),(-22,-15),(-14,-15),(-18,-9.5),(-13.5,-12),(-46.5,16),(-46.5,10),(-37.6,16),(-37.2,-13.5)): OUT(x,y,0,'#1f78c8' if (x<-24 and y<0) else INK)
sx.scatter([-34.2],[-19.4],s=22,marker='h',c='white',edgecolors='#1f78c8',linewidths=.8,zorder=8)
for x,y,a in ((-48.6,9.5,0),(36.6,9.5,0),(-30,-34.4,0),(-49.2,-21.8,0)): L(x,y,'L4',24)
sx.scatter([-48.9,36.9],[-9.5,-9.5],s=16,marker='$S$',c=INK,zorder=8); OUT(-46.8,3.5,90); OUT(34.8,3.5,-90)
sx.add_patch(MRect((-22.8,-20.6),3.2,1.4,fc=POW,ec='none',zorder=8)); sx.text(-21.2,-22.4,'LP',fontsize=4.6,color=POW,ha='center')
for (x,y,t) in ((-60.5,-34,'P'),(-49.5,-30,'P'),(36.5,19,'P')): sx.scatter([x+3.5],[y+3],s=18,marker='D',c='#cfe3f3',edgecolors=WATER,linewidths=.8,zorder=8)
sx.text(38.6,24.4,'bomba del bebedero este · east trough pump',fontsize=4.6,color=WATER,ha='right',va='center')
sx.annotate('',xy=(-69,4),xytext=(-63,-27),arrowprops=dict(arrowstyle='-|>',color=WATER,lw=.8)); sx.text(-69.5,5.5,'al bebedero largo\nto the long trough',fontsize=4.6,color=WATER,ha='left',va='bottom')
sx.text(5,-2.6,'pasillo · aisle',fontsize=5.6,color='#6a655a',ha='center')
# inset legend
ly=-29.0
for k,(fn,tx) in enumerate([(lambda x,y:L(x,y,'L1'),'L1 pasillo, regulable · aisle, dimmable'),(lambda x,y:L(x,y,'L2'),'L2 caballeriza + modo ámbar de ronda · stall + amber night-check'),
                            (lambda x,y:L(x,y,'L3',20),'L3 trabajo, mojado · work, wet-rated'),(lambda x,y:L(x,y,'L4',24),'L4 puerta, blindada, sensor · door, shielded, motion'),
                            (lambda x,y:OUT(x,y),'contacto GFCI en caja de acero, 5 ft · GFCI outlet, steel box, 5 ft'),
                            (lambda x,y:sx.scatter([x],[y],s=18,marker='D',c='#cfe3f3',edgecolors=WATER,linewidths=.8,zorder=8),'P bomba · pump   S apagadores · switches')]):
    yy=ly-k*3.2; fn(-5,yy); sx.text(-3,yy,tx,fontsize=5.0,va='center',color=INK)
sx.text(-5,ly+3.6,'Luces y contactos · Lights and outlets',fontsize=5.8,weight='bold',color=INK)

# ---------------- covered stalls inset ----------------
cx_=fig.add_axes([0.012,0.335,0.235,0.195]); cx_.set_aspect('equal'); cx_.axis('off'); cx_.set_xlim(-64,48); cx_.set_ylim(-29,25)
fig.text(0.014,0.538,'Caballerizas techadas · Covered stalls',fontsize=10,weight='bold',color=INK)
HL,HC,HD,RE,XS=44,6,26,18,20
cx_.add_patch(MRect((-46,-RE),92,2*RE,fc='none',ec='#b5602e',lw=.8,ls=(0,(5,3))))
for sg in (-1,1):
    for q in range(4): cx_.add_patch(MRect((-HL+16*q,min(sg*HC,sg*HD)),16,HD-HC,fc='#f1ead9',ec=INK,lw=.5))
    cx_.add_patch(MRect((XS,min(sg*HC,sg*RE)),24,RE-HC,fc='#e8d9a8',ec=INK,lw=.8)); cx_.text(XS+12,sg*12,'alfalfa',fontsize=5.4,ha='center',va='center')
    for q in range(4): cx_.scatter([-HL+8+16*q],[sg*(HC+5)],s=22,marker='o',c='white',edgecolors=INK,linewidths=.7,zorder=8)
    for q in (1,3): cx_.scatter([-HL+16*q],[sg*(HC+.8)],s=16,marker=(3,0,0 if sg<0 else 180),c='white',edgecolors=INK,linewidths=.8,zorder=8)
for x in (-36,-20,-4,12,32):
    cx_.scatter([x],[0],s=24,c=WARM,edgecolors=INK,linewidths=.7,zorder=8); cx_.plot([x-.9,x+.9],[-.9,.9],color=INK,lw=.5,zorder=9); cx_.plot([x-.9,x+.9],[.9,-.9],color=INK,lw=.5,zorder=9)
for x in (-46.6,46.6): cx_.scatter([x],[3.5],s=22,marker='v',c=AMBER,edgecolors=INK,linewidths=.7,zorder=8)
cx_.add_patch(mpatches.Circle((-55,0),4,fc='#cfe3f3',ec=INK,lw=.8)); cx_.scatter([-55],[-5.5],s=16,marker='D',c='#cfe3f3',edgecolors=WATER,linewidths=.8,zorder=8)
cx_.add_patch(MRect((-46.9,-8),1.8,1.8,fc='white',ec=POW,lw=1.2,zorder=9)); cx_.text(-48.5,-9.5,'SP-2',fontsize=5.4,weight='bold',color=POW,ha='right',va='top')
cx_.text(XS+12,-RE-3,'nada eléctrico dentro de las bodegas de alfalfa\nnothing electrical inside the alfalfa bays',fontsize=4.9,ha='center',va='top',color='#b5602e')
cx_.text(-HL+32,HD+1.2,'corredor 12 ft · corridor',fontsize=5.2,ha='center',color='#6a655a'); cx_.annotate('',xy=(46,21.5),xytext=(30,21.5),arrowprops=dict(arrowstyle='-|>',lw=.6)); cx_.text(38,22.5,'NE · establo',fontsize=4.8,ha='center',va='bottom')

# ---------------- roof plans: solar ----------------
rx=fig.add_axes([0.252,0.302,0.258,0.228]); rx.set_aspect('equal'); rx.axis('off'); rx.set_xlim(-50,120); rx.set_ylim(-2,100)   # 4 Oct (Will): the two roofs stacked, bigger
fig.text(0.254,0.538,'Techos solares · Solar roofs',fontsize=10,weight='bold',color=INK)
def panels(ax_,x0,y0,nr,nc,dy,col,alpha,lw=.3,sel=None):
    pw,ph=PANEL[0],PANEL[1]*(math.cos(math.radians(13.4)) if dy else 1)
    for r_ in range(nr):
        for c_ in range(nc):
            on=sel is None or sel(r_,c_)
            yy=y0+(r_*ph if dy>0 else -(r_+1)*ph); ax_.add_patch(MRect((x0+c_*pw,yy),pw,ph,fc=PV if on else 'none',ec=PVF if on else PV,lw=lw if on else .35,alpha=alpha if on else .55,ls='-' if on else (0,(2,1.2))))
# stable roof (76 x 46 with overhangs), the open clerestory, ridge; plan y up = north
Y0=52                                                                                              # stable roof on top (y 52..98), stalls roof below (y 0..36)
rx.add_patch(MRect((-44,Y0),88,46,fc='#cfcac0',ec=INK,lw=.8)); rx.plot([-44,44],[Y0+23,Y0+23],color=INK,lw=.5)
rx.add_patch(MRect((-18,Y0+18),48,10,fc='#f7f1e3',ec=INK,lw=.6)); rx.text(6,Y0+23,'claraboya · clerestory',fontsize=4.8,ha='center',va='center',color='#6a655a')
w0=-st_c*PANEL[0]/2
panels(rx,w0,Y0+1.5,st_r,st_c,1,PV,.95,sel=lambda r_,c_:abs(w0+(c_+.5)*PANEL[0]-6)<=2*PANEL[0])                    # south half: phase 1 = the middle 4 x 4
panels(rx,w0,Y0+44.5,st_r,st_c,-1,PV,.95,sel=lambda r_,c_:False)                                   # north half: optional
rx.text(50,Y0+40,'Establo · Stable',fontsize=6.4,weight='bold',va='center'); rx.text(50,Y0+34.5,'88 × 46 ft',fontsize=5.4,va='center')
rx.text(50,Y0+29,f'{st_r}×{st_c} paneles por mitad · panels per half',fontsize=5.0,va='center')
rx.text(50,Y0+15,'mitad sur (abajo), cae al SSO\nsouth half (below), falls SSW',fontsize=5.0,va='center',color='#6a655a')
rx.add_patch(MRect((-46,0),92,36,fc='#cfcac0',ec=INK,lw=.8)); rx.plot([-46,46],[18,18],color='#1f78c8',lw=.8)
s0=-sl_c*PANEL[0]/2; panels(rx,s0,1.5,sl_r,sl_c,1,PV,.95,sel=lambda r_,c_:False); panels(rx,s0,36-1.5,sl_r,sl_c,-1,PV,.95,sel=lambda r_,c_:False)
rx.text(0,18,'valle · valley',fontsize=4.8,ha='center',va='center',color='#1f78c8',bbox=dict(fc='#cfcac0',ec='none',pad=.6))
rx.text(52,28,'Caballerizas · Covered stalls',fontsize=6.4,weight='bold',va='center'); rx.text(52,22.5,'92 × 36 ft, techo mariposa · butterfly roof',fontsize=5.4,va='center')
rx.text(52,17,f'2 × {sl_r}×{sl_c} paneles, a futuro · panels, future',fontsize=5.0,va='center')
rx.add_patch(MRect((50,Y0+1.5),5,3.4,fc=PV,ec=PVF,lw=.3)); rx.text(57,Y0+3.2,f'fase 1 · phase 1: {PH1} paneles · panels, {PH1_KW:.1f} kWp',fontsize=5.0,va='center')
rx.add_patch(MRect((50,Y0-5),5,3.4,fc='none',ec=PV,lw=.35,ls=(0,(2,1.2)))); rx.text(57,Y0-3.3,'después · later',fontsize=5.0,va='center')
# ---------------- solar + load table ----------------
tx0=0.512; ty=0.538
fig.text(tx0,ty,'Potencial solar · Solar potential',fontsize=8.6,weight='bold',color=INK); ty-=.017
fig.text(tx0,ty,'techo · roof',fontsize=5.6,color='#6a655a');
for x,t in ((.105,'paneles'),(.135,'kWp'),(.162,'MWh/año·yr')): fig.text(tx0+x,ty,t,fontsize=5.6,color='#6a655a',ha='right' if x<.16 else 'left')
ty-=.0125
for nm,orient,n,y in PV_ROWS:
    fig.text(tx0,ty,nm.split(' · ')[1],fontsize=6,color=INK); fig.text(tx0,ty-.0098,f'{nm.split(" · ")[0]} · {orient}',fontsize=5.0,color='#6a655a',style='italic')
    fig.text(tx0+.105,ty,f'{n}',fontsize=6.4,ha='right'); fig.text(tx0+.135,ty,f'{kw(n):.1f}',fontsize=6.4,ha='right'); fig.text(tx0+.175,ty,f'{kw(n)*y/1000:.0f}',fontsize=6.4,ha='right'); ty-=.0235
ty-=.005; fig.add_artist(matplotlib.lines.Line2D([tx0,tx0+.19],[ty+.0165,ty+.0165],color=INK,lw=.6))
fig.text(tx0,ty+.003,'Todo · All',fontsize=6.4,weight='bold'); fig.text(tx0+.105,ty+.003,f'{N_ST*2+N_SL}',fontsize=6.4,ha='right',weight='bold'); fig.text(tx0+.135,ty+.003,f'{POT_KW:.0f}',fontsize=6.4,ha='right',weight='bold'); fig.text(tx0+.175,ty+.003,f'{POT_MWH:.0f}',fontsize=6.4,ha='right',weight='bold')
ty-=.016; fig.text(tx0,ty,'Fase 1 · Phase 1',fontsize=6.4,weight='bold',color='#b5602e'); fig.text(tx0+.105,ty,f'{PH1}',fontsize=6.4,ha='right',color='#b5602e'); fig.text(tx0+.135,ty,f'{PH1_KW:.1f}',fontsize=6.4,ha='right',color='#b5602e'); fig.text(tx0+.175,ty,f'{PH1_MWH:.1f}',fontsize=6.4,ha='right',color='#b5602e')
ty-=.02; fig.text(tx0,ty,f'Uso estimado · Est. use ≈ {DAY:.0f} kWh/día·day ≈ {YEAR/1000:.1f} MWh/año·yr',fontsize=6.6,weight='bold',color=INK); ty-=.0125
for i_,(nm,kwh,h) in enumerate(LOADS):
    cx2=tx0+.004+(i_%2)*.097; yy_=ty-(i_//2)*.0094
    fig.text(cx2,yy_,nm.split(' · ')[1].replace(', 3 nights/wk','').replace(' + small loads','').replace(', event days',''),fontsize=4.9,color=INK); fig.text(cx2+.09,yy_,f'{kwh*h:.1f}',fontsize=4.9,ha='right',color=INK)
ty-=.0094*((len(LOADS)+1)//2)
fig.text(tx0,ty-.002,f'Paneles {PANEL[2]} W negros · all-black {PANEL[2]} W panels; rendimiento PVGIS · PVGIS yields',fontsize=4.9,color='#6a655a',style='italic')

# ---------------- renderings: two slots ----------------
R_SLOTS={'E1-0':{'rect':[30,1160,505,1420],'src':'C:/Users/wrollins/WebDev/coyote-studio/projects/renders/fans/painted/4-hill-s-fan-blue-google.png','crop':[0,0,1,1]},
         'E1-1':{'rect':[525,1160,1000,1420],'src':'C:/Users/wrollins/WebDev/coyote-studio/projects/renders/fans/painted/4-hill-s-fan-dusk-google.png','crop':[0,0,1,1]}}
R_CAP=[('Desde el cerro, hora azul (antes de las luces)','From the hill at blue hour (before the lights)'),('Al anochecer, con las luces del plan encendidas','Just after sundown, with the plan’s lights on')]
if 'SLOTS' in globals():
    for _k,_v in R_SLOTS.items():
        if _k not in SLOTS: SLOTS[_k]={**_v,**(LAYOUT.get('slots') or {}).get(_k,{})}
for k,key in enumerate(R_SLOTS):
    if 'slot' in globals(): r_=slot(fig,key)
    else:
        r_=R_SLOTS[key]['rect']; a_=fig.add_axes([r_[0]/2550,1-r_[3]/1650,(r_[2]-r_[0])/2550,(r_[3]-r_[1])/1650]); a_.axis('off')
        if R_SLOTS[key]['src'] and os.path.exists(R_SLOTS[key]['src']):
            from PIL import Image as _I; im_=_I.open(R_SLOTS[key]['src']).convert('RGB'); asp=(r_[2]-r_[0])/(r_[3]-r_[1]); w_,h_=im_.size
            if w_/h_>asp: m_=(w_-h_*asp)/2; im_=im_.crop((m_,0,w_-m_,h_))
            else: m_=(h_-w_/asp)/2; im_=im_.crop((0,m_,w_,h_-m_))
            a_.imshow(im_)
        else: a_.add_patch(MRect((0,0),1,1,transform=a_.transAxes,color='#ddd3c3'))
    src_=(SLOTS[key]['src'] if 'SLOTS' in globals() else R_SLOTS[key]['src'])
    if not src_ or not os.path.exists(str(src_)):
        fig.text((r_[0]+r_[2])/2/2550,1-(r_[1]+r_[3])/2/1650,'render pendiente\nrendering to come',fontsize=9,ha='center',va='center',color='#8a7d66',zorder=5)
    fig.text(r_[0]/2550+.001,1-(r_[3]+24)/1650,R_CAP[k][0],fontsize=7.6,weight='bold',color=INK); fig.text(r_[0]/2550+.001,1-(r_[3]+46)/1650,R_CAP[k][1],fontsize=6.8,color='#6a655a',style='italic')

# ---------------- fixture schedule ----------------
FX=[('L1','Pasillos · Aisles','2700 K · 1,500 lm · regulable · dimmable','bajo la cuerda, 11 ft · under the chord',f'escena atardecer 30 % · dusk scene 30 %',11),
    ('L2','Caballerizas · Stalls','2700 K · 1,000 lm + ámbar · amber','enrejada, 10 ft · caged','apagador por caballeriza · switch each',18),
    ('L3','Lavado, monturas, cocina, baño, ER · Wash, tack, kitchen, bath, ER','3000 K · IRC/CRI 90 · 2,500 lm','techo, mojado · ceiling, wet','apagador · switch',8),
    ('L4','Puertas, losa · Doors, pad','2200 K · 600 lm · blindada · full cutoff','muro 9 ft · wall 9 ft','sensor · motion',6),
    ('L5','Senderos, estacionamiento · Paths, parking','ámbar · amber · 150 lm','bolardo 24 in · bollard','reloj hasta 22:00 · timer to 22:00',11),
    ('L6','Puertas del sitio · Site gates','2200 K · 400 lm','poste de la puerta · gate post','sensor · motion',2),
    ('L7','Pista oval · Arena',f'3000 K · 15,000 lm · lente plana · flat lens','postes 18 ft, 2 c/u · poles, 2 each','llave + 2 h · key + 2 h',2*NARENA),
    ('L8','Corral redondo · Round pen','3000 K · 15,000 lm · lente plana · flat lens','postes 16 ft · poles','llave + 2 h · key + 2 h',NRP),
    ('L9','Gradas · Bleachers','ámbar · amber · 50 lm','escalón · step riser','reloj · timer',8)]
fx0=0.405; fy0=0.322
fig.text(fx0,fy0,'Cuadro de luminarias · Fixture schedule',fontsize=8.6,weight='bold',color=INK); fy0-=.016
COLX=[0,.02,.10,.178,.24,.292]
for x,t in zip(COLX,['tipo','dónde · where','luz · light','montaje · mount','control','#']): fig.text(fx0+x,fy0,t,fontsize=5.2,color='#6a655a')
fy0-=.004; fig.add_artist(matplotlib.lines.Line2D([fx0,fx0+.298],[fy0,fy0],color=INK,lw=.5)); fy0-=.0105
for row in FX:
    hgt=1
    for x,t,w in zip(COLX,row,(4,25,25,19,17,4)):
        lines=textwrap.wrap(str(t),w) if x not in (0,.292) else [str(t)]
        for m,l_ in enumerate(lines): fig.text(fx0+x,fy0-m*.0082,l_,fontsize=5.0 if x else 5.6,color=INK,weight='bold' if x==0 else 'normal')
        hgt=max(hgt,len(lines))
    fy0-=.0082*hgt+.0035
print('schedule ends at',round(fy0,3))

# ---------------- side panel: notes ----------------
px=0.718
fig.text(px,0.955,'PLAN ELÉCTRICO Y DE ILUMINACIÓN',fontsize=15.5,weight='bold',color=INK)
fig.text(px,0.932,'Electrical, lighting and solar plan · Centro Equino, Chichihuas',fontsize=11,color='#555')
NOTES_E=[
 ('Power in, main disconnect','Acometida y desconexión','Power comes from the ranch’s main group of buildings (Andrés) in its own buried conduit in the main-road trench, beside the 2 in water main (a foot apart, warning tape above). Where it enters the site, at the north-east gate, a small stone pillar holds a sub-meter and the MAIN DISCONNECT (MD, about 100 A, 127/220 V, lockable): one handle turns off the whole centre. Size and spare capacity at the ranch to confirm.','La luz viene del grupo principal de edificios del rancho (Andrés) en su propio tubo enterrado en la zanja del camino principal, junto a la línea de agua de 2 in (a 30 cm, cinta de aviso arriba). Donde entra al sitio, en la puerta noreste, un pilar de piedra lleva un submedidor y la DESCONEXIÓN PRINCIPAL (MD, unos 100 A, 127/220 V, con candado): una palanca apaga todo el centro. Capacidad y calibre por confirmar con el rancho.'),
 ('Electrical room','Cuarto eléctrico','In the stable’s new south-west corner bay (12 × 6 ft, beside the bathroom; Will, 4 Oct), away from all hay, with its own outside door in the west gable: main panel (MP), room for the solar inverter and battery (option b, note 5), C1’s pump control, the timers. Beside its door a second shut-off and the solar rapid-shutdown switch for the firefighters. It feeds the stable, SP-2 at the covered stalls and SP-3 at the bleachers.','En la nueva crujía suroeste del establo (12 × 6 ft, junto al baño; Will, 4 oct), lejos de toda la paja, con su propia puerta exterior en el hastial oeste: tablero principal (MP), lugar para el inversor y la batería solar (opción b, nota 5), control de la bomba de C1, los relojes. Junto a su puerta, una segunda desconexión y el paro rápido solar para los bomberos. Alimenta al establo, el SP-2 de las caballerizas y el SP-3 de las gradas.'),
 ('Both stables','Los dos establos','One caged light in every stall on its own switch, with an amber setting for night checks that doesn’t blind the horses; dimmable lights along both aisles; work lights in wash and tack; a GFCI outlet in a steel box at each stall front, aisle side, 5 ft up, for fans and clippers. Wash and bathroom: GFCI outlets and the water heater; tack and feed: four outlets and the fridge; kitchen: counter outlets, induction top and fridge. All wiring in metal conduit out of reach of teeth; no extension cords. At the covered stalls, nothing electrical inside the alfalfa bays.','Una luz enrejada en cada caballeriza con su apagador y un modo ámbar para las rondas nocturnas que no deslumbra a los caballos; luces regulables en los dos pasillos; luces de trabajo en lavado y monturas; un contacto GFCI en caja de acero en cada frente, lado pasillo, a 1.5 m, para ventiladores y rasuradoras. Lavado y baño: contactos GFCI y calentador; monturas y alimento: cuatro contactos y el refri; cocina: contactos en la barra, parrilla de inducción y refri. Todo el cableado en tubo metálico fuera del alcance de los dientes; sin extensiones. En las caballerizas techadas, nada eléctrico dentro de las bodegas de alfalfa.'),
 ('Site lighting','Luz del sitio',f'Roads and the riding track stay dark (reflectors on fence posts). Knee-high amber bollards along the walking path and the parking edge; a motion light on the north-east and east gate posts. Arena: {NARENA} poles with two flat-lens heads each, round pen: {NRP}; aimed in with back shields, on a key switch at the gate that turns them off after 2 hours. Amber step lights on the bleachers; a 50 A pedestal for the café trailer. No light on trees, walls or water.',f'Los caminos y la pista de paseo quedan oscuros (reflejantes en los postes). Bolardos ámbar a la rodilla en el sendero y la orilla del estacionamiento; luz con sensor en los postes de las puertas noreste y este. Pista oval: {NARENA} postes con dos cabezas de lente plana; corral redondo: {NRP}; apuntados hacia adentro con pantalla trasera, con llave en la puerta y apagado a las 2 horas. Luces ámbar en los escalones de las gradas; un pedestal de 50 A para el café. Sin luz sobre árboles, muros o agua.'),
 ('Solar on the roofs','Solar en los techos',f'The stable’s south half (SSW, 13°) is the best plane. Full, the three roof planes hold {N_ST*2+N_SL} panels, about {POT_KW:.0f} kWp and {POT_MWH:.0f} MWh a year, some {POT_MWH*1000/YEAR:.0f} times what the centre uses. Phase 1: {PH1} all-black panels ({PH1_KW:.1f} kWp) over the horses cover the year. The ranch already has a grid-tied system, so the ranch decides: (a) tie in through the ranch feed, simplest; or (b) the centre’s own hybrid inverter and a 15 kWh battery in the electrical room, for outages. The panels also shade the dark roof, with air under them: a cooler stable in summer. Frames checked for about 3 lb/ft².',f'La mitad sur del establo (SSO, 13°) es el mejor plano. Completos, los tres planos llevan {N_ST*2+N_SL} paneles, unos {POT_KW:.0f} kWp y {POT_MWH:.0f} MWh al año, unas {POT_MWH*1000/YEAR:.0f} veces lo que usa el centro. Fase 1: {PH1} paneles negros ({PH1_KW:.1f} kWp) sobre los caballos cubren el año. El rancho ya tiene un sistema interconectado, así que el rancho decide: (a) sumarlos por la alimentación del rancho, lo más sencillo; o (b) un inversor híbrido propio y una batería de 15 kWh en el cuarto eléctrico, para los apagones. Los paneles además dan sombra al techo oscuro, con aire por debajo: un establo más fresco en verano. Revisar estructuras para unos 15 kg/m².'),
 ('Dark sky','Cielo oscuro','Ensenada’s light-pollution regulation (2006) protects the sky of the San Pedro Mártir observatory: no light above the horizon. Every fixture shielded and aimed down, 2200–3000 K (amber outdoors), as low and dim as works, on timers or motion; outdoor lights off at 10 pm except motion lights. The one glow we keep is the one Will imagined: at dusk the aisle lights at 30 % so warm light pours out between the sticks, while the fixtures hang under the chords so none shines up through the open clerestory (below).','El reglamento de contaminación lumínica de Ensenada (2006) protege el cielo del observatorio de San Pedro Mártir: nada de luz arriba del horizonte. Cada luminaria blindada y hacia abajo, 2200–3000 K (ámbar afuera), tan baja y tenue como funcione, con reloj o sensor; las luces exteriores se apagan a las 22:00 salvo las de sensor. El único resplandor que guardamos es el que Will imaginó: al anochecer los pasillos al 30 % y la luz cálida sale entre las varas, con las luminarias colgadas bajo las cuerdas para que nada brille hacia arriba por la claraboya abierta (abajo).'),
]
y=0.905
for k,(en,es,ten,tes) in enumerate(NOTES_E):
    fig.text(px,y,f'{k+1}',fontsize=10,weight='bold',color='#b5602e')
    fig.text(px+.018,y,f'{es} · {en}',fontsize=8.4,weight='bold',color=INK)
    ly=y-.0142
    for line in textwrap.wrap(tes,99): fig.text(px+.018,ly,line,fontsize=6.1,color=INK); ly-=.0089
    for line in textwrap.wrap(ten,99): fig.text(px+.018,ly,line,fontsize=6.1,color='#6a655a',style='italic'); ly-=.0089
    y=ly-.0045
print('notes end at', round(ly, 3))
# ---------------- night section: the glow through the sticks, nothing up ----------------
nx=fig.add_axes([px,0.062,0.985-px,min(.16,max(.105,y-.075))]); nx.set_xlim(-33,33); nx.set_ylim(-4.5,25); nx.set_aspect('equal'); nx.set_anchor('C'); nx.axis('off')
nx.add_patch(MRect((-33,-4.5),66,29.5,fc='#1f2a40',ec='none'))
nx.add_patch(MRect((-33,-4.5),66,4.5,fc='#2b2a26',ec='none'))
HD_,EAVE,RIDGE=21,12,17; rz=lambda yy:RIDGE-(RIDGE-EAVE)/HD_*abs(yy)
for sgn in (-1,1):
    x=sgn*HD_; nx.add_patch(MRect((x-.8,0),1.6,5,fc='#6d6458',ec='none')); nx.plot([x-.6,x+.6],[6,6],color='#2a2a2a',lw=1.5)
    for yy in np.arange(6.4,EAVE-.1,.42):
        nx.plot([x-.5,x+.5],[yy,yy],color='#3a2c20',lw=1.1)
        nx.plot([x+sgn*.6,x+sgn*(2.4+1.6*np.random.RandomState(int(yy*10)).rand())],[yy+.2,yy+.2],color=WARM,lw=.9,alpha=.7)
    nx.plot([x+sgn*2,0],[rz(HD_+2),RIDGE],color='#9aa3ad',lw=1.4)
nx.plot([-HD_,HD_],[EAVE,EAVE],color='#9aa3ad',lw=1); nx.plot([-6,0,6],[rz(5)+2.3,RIDGE+3.2,rz(5)+2.3],color='#9aa3ad',lw=1.2)
for xx in (-8,8):
    nx.plot([xx,xx],[EAVE,EAVE-.7],color='#9aa3ad',lw=.6); nx.add_patch(MPoly([(xx-.5,EAVE-.7),(xx+.5,EAVE-.7),(xx+5,0),(xx-5,0)],closed=True,fc=WARM,ec='none',alpha=.30))
    nx.add_patch(MRect((xx-.55,EAVE-1.0),1.1,.35,fc=WARM,ec='none'))
nx.add_patch(MPoly([(-HD_+.8,0),(HD_-.8,0),(HD_-.8,6),(-HD_+.8,6)],closed=True,fc=WARM,ec='none',alpha=.10))
nx.annotate('',xy=(0,RIDGE+6.4),xytext=(0,EAVE+.3),arrowprops=dict(arrowstyle='-|>',color='#c9d2dd',lw=.8,ls=(0,(2,2))))
nx.plot([-1.4,1.4],[RIDGE+4.6,RIDGE+6.1],color='#e05a4a',lw=1.6); nx.plot([-1.4,1.4],[RIDGE+6.1,RIDGE+4.6],color='#e05a4a',lw=1.6)
nx.text(2.2,RIDGE+5.35,'nada hacia el cielo\nnothing up',fontsize=5.4,color='#e8e2d6',va='center')
nx.text(-32,23.2,'Al anochecer\nJust after sundown',fontsize=6.4,color='white',weight='bold',va='top')
nx.text(-32,-1.6,'pasillos al 30 %: la luz sale entre las varas',fontsize=5.0,color='#e8e2d6'); nx.text(-32,-3.6,'aisles at 30 %: warm light pours out between the sticks',fontsize=5.0,color='#c9c2b4',style='italic')
fig.text(0.02,0.03,'31.9999 N, 116.7641 W · Hoja / Sheet E-1 · 4 oct 2026 · Diseño preliminar, no para construcción · Preliminary design, not for construction',fontsize=8,color='#6a655a')
if not globals().get('PACK'): fig.savefig('E1-electrical.png',dpi=170); print('ok')
