exec(open('drain.py',encoding='utf-8').read())
import textwrap
# three sections through the heaviest grading
SECS=[('A','Corrales y bajo natural','Paddocks and water sink',(46,64),(46,88)),
      ('B','Establo y bebedero','Barn and trough',(92,52),(126,62)),
      ('C','Pista oval y corral redondo','Arena and round pen',(88,30),(86,62))]
def samp(Z,x,y):
    i=int(np.floor(x)); j=int(np.floor(y)); fx=x-i; fy=y-j; i=min(max(i,0),W-2); j=min(max(j,0),H-2)
    return Z[j,i]*(1-fx)*(1-fy)+Z[j,i+1]*fx*(1-fy)+Z[j+1,i]*(1-fx)*fy+Z[j+1,i+1]*fx*fy
fig=plt.figure(figsize=(17,11),dpi=170)
fig.text(0.02,0.955,'CORTES DE TERRACERÍA',fontsize=20,weight='bold',color=INK)
fig.text(0.02,0.93,'Grading sections · existing ground dashed, finished grade solid · vertical exaggeration 3×',fontsize=12,color='#555')
fig.text(0.02,0.912,'Terreno existente punteado, rasante terminada continua · exageración vertical 3×',fontsize=10,color='#6a655a',style='italic')
# key plan
kax=base_axes(fig,[0.70,0.60,0.28,0.30],alpha=.5); contours(kax,z); features(kax)
for s,es,en,a,bb in SECS:
    kax.plot([a[0],bb[0]],[a[1],bb[1]],color='#b5602e',lw=2,zorder=30)
    for q in (a,bb): kax.text(q[0],q[1],s,fontsize=10,weight='bold',color='white',ha='center',va='center',zorder=31,bbox=dict(boxstyle='circle,pad=.2',fc='#b5602e',ec='none'))
fig.text(0.70,0.585,'Plano llave · Key plan',fontsize=9,color=INK,weight='bold')
for k,(s,es,en,a,bb) in enumerate(SECS):
    ax=fig.add_axes([0.06,0.66-k*0.27,0.60,0.2])
    n=300; xs=np.linspace(0,1,n); P=[(a[0]+(bb[0]-a[0])*t,a[1]+(bb[1]-a[1])*t) for t in xs]
    L=math.hypot(bb[0]-a[0],bb[1]-a[1])*cf; d=xs*L
    e=np.array([samp(b,*q) for q in P]); f=np.array([samp(z,*q) for q in P])
    ax.fill_between(d,e,f,where=f<e,color='#9a9488',alpha=.55,lw=0,label='Corte · Cut')
    ax.fill_between(d,e,f,where=f>e,color='#c96b3a',alpha=.55,lw=0,label='Relleno · Fill')
    ax.plot(d,e,color=INK,lw=1,ls=(0,(4,3))); ax.plot(d,f,color=INK,lw=1.8)
    lo=min(e.min(),f.min())-3; hi=max(e.max(),f.max())+4; ax.set_ylim(lo,hi); ax.set_xlim(0,L)
    ax.set_aspect(3); ax.grid(color='#ddd',lw=.5); ax.set_ylabel('pies · ft',fontsize=8); ax.tick_params(labelsize=7.5)
    ax.set_title(f'Corte {s}–{s}′ · {es} · Section {s}–{s}′ · {en}',loc='left',fontsize=11,weight='bold',color=INK)
    mx=np.argmax(np.abs(f-e)); ax.annotate(f'{(f-e)[mx]:+.1f} ft ({(f-e)[mx]*0.3048:+.1f} m)',xy=(d[mx],f[mx]),xytext=(d[mx],hi-1),fontsize=8,ha='center',arrowprops=dict(arrowstyle='-',color='#888',lw=.7))
    for side,x0 in ((s,0),(s+'′',L)): ax.text(x0,hi-1,side,fontsize=10,weight='bold',color='#b5602e',ha='left' if x0==0 else 'right')
    if k==0: ax.legend(loc='lower right',fontsize=8,frameon=False)
    ax.set_xlabel('pies desde '+s+' · ft from '+s,fontsize=8)
notes=[('A','Los corrales quedan en una plataforma a nivel (1,082.5 ft) y junto a ellos un bajo natural recibe el agua al final de la pista.','The paddocks sit on one level pad (1,082.5 ft); beside them a natural low spot collects water at the end of the track.'),
       ('B','El establo queda en plataforma con 1 % de caída; su techo alimenta el bebedero largo de piedra.','The barn sits on a pad falling 1%; its roof feeds the long stone trough.'),
       ('C','La pista oval y el corral redondo quedan casi a nivel con cortes y rellenos menores a 2.5 ft.','The arena and round pen sit nearly level, with cut and fill under 2.5 ft.')]
y=0.54
for s,es,en in notes:
    fig.text(0.70,y,s,fontsize=11,weight='bold',color='#b5602e')
    ly=y
    for line in textwrap.wrap(es,52): fig.text(0.715,ly,line,fontsize=8.4,color=INK); ly-=.017
    for line in textwrap.wrap(en,52): fig.text(0.715,ly,line,fontsize=8.4,color='#6a655a',style='italic'); ly-=.017
    y=ly-.02
fig.text(0.70,0.2,'Bordes suaves en todos los taludes, pendiente 3:1.',fontsize=8.4,color=INK)
fig.text(0.70,0.183,'Soft edges on every bank, 3:1 side slopes.',fontsize=8.4,color='#6a655a',style='italic')
fig.text(0.02,0.03,'31.9999 N, 116.7641 W · Hoja / Sheet D-2 · 23 sep 2026 · Terreno de 30 m, ±30–50 % · 30 m terrain, volumes ±30–50% · Diseño preliminar · Preliminary design',fontsize=8,color='#6a655a')
if not globals().get('PACK'): fig.savefig('D2-sections.png',dpi=170); print('ok')
