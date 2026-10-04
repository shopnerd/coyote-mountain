import os, glob, textwrap, numpy as np, math
PACK=True
exec(open('drain.py',encoding='utf-8').read())
from matplotlib.backends.backend_pdf import PdfPages
from PIL import Image
OUTDIR='G:/My Drive/MEXICO/Chichihaus/2026-09-23 Centro Equino pack'
DL=OUTDIR+'/renderings'
CLAY='#b5602e'; MUTED='#6a655a'
PAGES=[]
def img(n):
    f=n if os.path.isabs(str(n)) else os.path.join(DL,str(n))
    if not os.path.exists(f):                      # a rendering not made yet: a quiet placeholder frame
        a=np.full((900,1400,3),236,np.uint8); a[::40]=226; a[:,::40]=226; return a
    im=Image.open(f).convert('RGB'); a=np.asarray(im).astype(int); c=a[2,2]; d=np.abs(a-c).sum(2)>30
    r=np.where(d.mean(1)>.02)[0]; k=np.where(d.mean(0)>.02)[0]
    if len(r) and len(k) and (r[-1]-r[0])>a.shape[0]*.5 and (k[-1]-k[0])>a.shape[1]*.5: im=im.crop((k[0],r[0],k[-1]+1,r[-1]+1))
    return np.asarray(im)
def newpage():
    fig=plt.figure(figsize=(17,11),dpi=100); fig.patch.set_facecolor('white'); return fig
def tblock(fig,num,es,en,dark=False):
    c='white' if dark else INK; m='#d8d2c4' if dark else MUTED
    if not dark: fig.add_artist(matplotlib.lines.Line2D([0.02,0.98],[0.055,0.055],color=INK,lw=.8))
    fig.text(0.02,0.025,'CENTRO EQUINO · CHICHIHUAS',fontsize=10,weight='bold',color=c)
    fig.text(0.215,0.025,f'{es}  ·  {en}',fontsize=10,color=c)
    fig.text(0.627,0.025,'GIANT NATURE',fontsize=9.5,weight='bold',color='#4f6b3a' if not dark else 'white')   # Walker's v14 branding
    fig.text(0.70,0.025,'Diseño preliminar · Preliminary design · oct 2026',fontsize=8.5,color=m)
    fig.text(0.98,0.022,f'{num:02d}',fontsize=18,weight='bold',color=CLAY,ha='right')
def heading(fig,es,en,y=0.945):
    fig.text(0.02,y,es,fontsize=24,weight='bold',color=INK); fig.text(0.02,y-0.033,en,fontsize=14,color=MUTED,style='italic')
def para(fig,x,y,es,en,w=80,fs=10.5):
    for line in textwrap.wrap(es,w): fig.text(x,y,line,fontsize=fs,color=INK); y-=fs*0.0021
    y-=.004
    for line in textwrap.wrap(en,w): fig.text(x,y,line,fontsize=fs,color=MUTED,style='italic'); y-=fs*0.0021
    return y-.012
num=[0]
def nxt(): num[0]+=1; return num[0]
# ---- 1 cover
def cover(win):
    fig=newpage(); ax=fig.add_axes([0,0,1,1]); a=img(win); H0,W0=a.shape[:2]
    # fill 17x11 (aspect 1.545) by cropping
    tgt=17/11
    if W0/H0>tgt: w=int(H0*tgt); a=a[:,(W0-w)//2:(W0-w)//2+w]
    else: h=int(W0/tgt); a=a[(H0-h)//2:(H0-h)//2+h]
    ax.imshow(a,aspect='auto'); ax.axis('off')
    band=fig.add_axes([0,0,1,.2]); band.axis('off'); band.add_patch(matplotlib.patches.Rectangle((0,0),1,1,transform=band.transAxes,color='black',alpha=.55))
    fig.text(0.03,0.125,'Centro Equino',fontsize=46,weight='bold',color='white')
    fig.text(0.03,0.085,'Chichihuas · Valle de Guadalupe, Baja California',fontsize=16,color='#f1ece0')
    fig.text(0.97,0.125,'Propuesta de diseño',fontsize=20,color='white',ha='right')
    fig.text(0.97,0.09,'Design proposal · septiembre 2026',fontsize=14,color='#f1ece0',ha='right',style='italic')
    tblock(fig,nxt(),'Portada','Cover',dark=True); PAGES.append(fig)
# ---- 2 plan view (illustrative)
def planview(n):
    fig=newpage(); heading(fig,'Vista en planta','Plan view')
    ax=fig.add_axes([0.02,0.075,0.70,0.81]); ax.imshow(img(n)); ax.axis('off')
    items=[('Establo principal','Main stable','72 × 42 ft en retícula de 12 ft · cerchas de acero, piedra a 5 ft con tubo arriba, paneles de varas horizontales, claraboya abierta · 10 caballerizas con corral de 12 × 40 ft, 6 al norte y 4 al sur · lavado y monturas en la esquina oeste','72 × 42 ft on a 12 ft grid · steel trusses, rock to 5 ft with a pipe rail, horizontal stick panels, open clerestory · 10 stalls with 12 × 40 ft runs, 6 north and 4 south · wash and tack at the west corner'),
           ('Pista oval','Oval arena','182 × 78 ft, arena rastrillada','182 × 78 ft, raked sand'),
           ('Corral redondo','Round pen','60 ft de diámetro','60 ft across'),
           ('Pista de trote','Riding track','1,224 ft, usa el camino oeste existente','1,224 ft, uses the existing west road'),
           ('Caballerizas techadas','Covered stalls','8 caballerizas de 16 × 20 ft y la alfalfa bajo el mismo techo mariposa, que llena un bebedero redondo','8 stalls of 16 × 20 ft and the alfalfa under one butterfly roof that fills a round trough'),
           ('Agua','Water','bajo natural abajo de la pista (confirmado en sitio), bebedero largo de piedra de 40 ft junto a la entrada del establo, bebedero redondo en las caballerizas, bebedero redondo existente','natural water sink below the track (confirmed on site), 40 ft stone trough beside the stable drive-in, round trough at the stalls, existing round watering station'),
           ('Estacionamiento','Parking','franja angosta al extremo este, 13 cajones a 60°','narrow strip at the far east corner, 13 stalls at 60°')]
    y=0.86
    for es,en,tes,ten in items:
        fig.text(0.74,y,f'{es} · {en}',fontsize=10.5,weight='bold',color=INK); y-=.02
        y=para(fig,0.74,y,tes,ten,w=52,fs=8.0)
    tblock(fig,nxt(),'Vista en planta','Plan view'); PAGES.append(fig)
X,Y=np.meshgrid(np.arange(W),np.arange(H))
LOOP=[s for s in S if s.get('shape') and not s.get('name') and len(s['pts'])==10 and abs(s['pts'][0][0]-26.6)<.3][0]
CROSS=[s for s in S if s.get('shape') and not s.get('name') and s.get('dash') and len(s['pts'])==2 and abs(s['pts'][0][0]-69.3)<.3][0]
def plain_axes(fig,rect):
    ax=fig.add_axes(rect); ax.set_xlim(0,W-1); ax.set_ylim(H-1,0); ax.set_aspect('equal'); ax.axis('off'); return ax
def fence(ax,col=INK):
    for s in (LOOP,CROSS):
        P=np.array([q[:2] for q in s['pts']]); ax.plot(P[:,0],P[:,1],color=col,lw=1.4,dashes=(7,2,1,2),zorder=6)
def samp(Z,x,y):
    i=int(np.floor(x)); j=int(np.floor(y)); fx=x-i; fy=y-j; i=min(max(i,0),W-2); j=min(max(j,0),H-2)
    return Z[j,i]*(1-fx)*(1-fy)+Z[j,i+1]*fx*(1-fy)+Z[j+1,i]*(1-fx)*fy+Z[j+1,i+1]*fx*fy
def existing():
    fig=newpage(); heading(fig,'Topografía existente','Existing topography')
    ax=plain_axes(fig,[0.02,0.075,0.74,0.82])
    ax.contour(X,Y,b,levels=np.arange(1050,1125,1),colors='#8a8478',linewidths=.35)
    c5=ax.contour(X,Y,b,levels=np.arange(1050,1125,5),colors=INK,linewidths=.9); ax.clabel(c5,fmt='%d',fontsize=7,inline=True)
    for nm in ('existing vineyard road','existing scrub-side road'):
        for s in byname(nm):
            P=np.array([q[:2] for q in s['pts']]); ax.plot(P[:,0],P[:,1],color='#b9a784',lw=6,alpha=.7,solid_capstyle='round',zorder=2)
    fence(ax)
    step=50/cf; spots=[(x,y) for x in np.arange(step/2,W-1,step) for y in np.arange(step/2,H-1,step)]
    for (x,y) in spots:
        if 1<x<W-2 and 1<y<H-2:
            ax.plot(x,y,'+',color=CLAY,ms=4,mew=.8,zorder=7); ax.text(x+.5,y-.4,f'{samp(b,x,y):.1f}',fontsize=5.2,color=CLAY,zorder=7)
    north(ax,140,8); scalebar(ax,6,96)
    y=0.86
    y=para(fig,0.78,y,'Terreno natural antes de cualquier movimiento de tierra. Curvas cada 1 pie, rotuladas cada 5 pies. Las cruces marcan la elevación del terreno cada 50 pies, en pies.','Natural ground before any earthwork. Contours every 1 ft, labelled every 5 ft. Crosses mark ground elevation every 50 ft, in feet.',w=40,fs=9.5)
    y=para(fig,0.78,y,f'El sitio cae unos {b.max()-b.min():.0f} pies, de {b.max():.0f} ft junto al camino del cerro a {b.min():.0f} ft junto al viñedo (≈ 6 %).',f'The site falls about {b.max()-b.min():.0f} ft, from {b.max():.0f} ft by the scrub-side road to {b.min():.0f} ft by the vineyard (about 6%).',w=40,fs=9.5)
    y=para(fig,0.78,y,'Fuente: datos públicos de elevación de 30 m; precisión vertical de varios pies. Un levantamiento con dron la mejoraría.','Source: 30 m public elevation data; vertical accuracy of several feet. A drone survey would sharpen it.',w=40,fs=9.5)
    items=[(INK,'-',.9,'Curva cada 5 ft · 5 ft contour'),('#8a8478','-',.4,'Curva cada 1 ft · 1 ft contour'),('#b9a784','-',6,'Caminos existentes · Existing roads'),(INK,(0,(7,2,1,2)),1.4,'Cerca del predio · Site fence')]
    ly=0.30
    for c,st,lw,t in items:
        fig.add_artist(matplotlib.lines.Line2D([0.78,0.81],[ly,ly],color=c,lw=lw,ls=st)); fig.text(0.818,ly-.005,t,fontsize=8.5,color=INK); ly-=.025
    fig.text(0.78,ly-.005,'+ 1082.4   Punto de elevación · Spot elevation (ft)',fontsize=8.5,color=CLAY)
    tblock(fig,nxt(),'Topografía existente','Existing topography'); PAGES.append(fig)
PADS=[('Establo · Barn','1087.6',(107.5,57.5),'1 %'),('Caballerizas · Stalls','1089.3',(84.6,64.8),'0.2 %'),('Bebedero redondo · Round trough','1089.1',(76.2,67.6),'0 %'),('Pista oval · Arena','1073.3',(89.4,38.4),'1 %'),('Corral redondo · Pen','1080.6',(86.4,53.1),'1 %'),('Estacionamiento · Parking','1102.4',(136,60.3),'5 %'),('Bebedero · Trough','1087.1',(100.3,59.8),'0 %')]
def grading():
    fig=newpage(); heading(fig,'Plan de terracería','Grading plan')
    ax=plain_axes(fig,[0.02,0.075,0.74,0.82])
    dd=z-b; lim=6
    ax.imshow(np.ma.masked_where(np.abs(dd)<.15,dd),cmap=matplotlib.colors.LinearSegmentedColormap.from_list('cf',['#7d786d','#f4f1ea','#c96b3a']),vmin=-lim,vmax=lim,extent=(-.5,W-.5,H-.5,-.5),alpha=.55,zorder=1)
    ax.contour(X,Y,b,levels=np.arange(1050,1125,1),colors='#9d978a',linewidths=.4,linestyles='dashed',zorder=2)
    ax.contour(X,Y,z,levels=np.arange(1050,1125,1),colors=INK,linewidths=.45,zorder=3)
    c5=ax.contour(X,Y,z,levels=np.arange(1050,1125,5),colors=INK,linewidths=1.1,zorder=3); ax.clabel(c5,fmt='%d',fontsize=7,inline=True)
    for s in S:
        if s.get('kind')=='path':
            P=np.array([q[:2] for q in s['pts']]); w=(s.get('pw',3.66)/FT)/cf
            ax.plot(P[:,0],P[:,1],color='#c9b48f',lw=max(1.2,w*4.6),alpha=.55,solid_capstyle='round',zorder=4)
    for nm in ('walker barn 72x40','covered stalls','stone trough (long)','trailer 8 x 40','bleachers'):
        for s in byname(nm):
            P=np.array(foot(s)+[foot(s)[0]]); ax.fill(P[:,0],P[:,1],color='white',alpha=.9,zorder=5); ax.plot(P[:,0],P[:,1],color=INK,lw=.9,zorder=6)
    for i in (1,2):
        P=np.array([q[:2] for q in S[i]['pts']]); ax.plot(P[:,0],P[:,1],color=INK,lw=1.2,zorder=6)
    fence(ax); works(ax)
    for s in S:
        if (s.get('name') or '').startswith('gate'):
            P=np.array([q[:2] for q in s['pts']]); ax.fill(P[:,0],P[:,1],color=CLAY,zorder=9)
    for lab,lev,(x,y),g in PADS:
        ax.text(x,y,f'{lev}',fontsize=8,weight='bold',color=INK,ha='center',va='center',zorder=12,bbox=dict(boxstyle='round,pad=.25',fc='#fffbe8',ec=INK,lw=.6))
    north(ax,140,8); scalebar(ax,6,96)
    y=0.86
    y=para(fig,0.78,y,'Rasante terminada con todos los cambios. Curvas terminadas continuas; terreno existente punteado. Gris es corte, ocre es relleno.','Finished grade with every change. Finished contours solid, existing ground dashed. Grey is cut, ochre is fill.',w=40,fs=9.5)
    fig.text(0.78,y,'Plataformas · Pads (nivel terminado, ft)',fontsize=10,weight='bold',color=INK); y-=.024
    for lab,lev,xy,g in PADS:
        fig.text(0.78,y,lab,fontsize=8.8,color=INK); fig.text(0.95,y,lev,fontsize=8.8,color=INK,weight='bold',ha='right'); fig.text(0.985,y,g,fontsize=8.8,color=MUTED,ha='right'); y-=.021
    y-=.012
    fig.text(0.78,y,'Movimiento de tierra · Earthwork',fontsize=10,weight='bold',color=INK); y-=.024
    fig.text(0.78,y,f'Corte · Cut   ≈ {cut:,.0f} yd³  ({cut*.7646:,.0f} m³)',fontsize=8.8,color=INK); y-=.02
    fig.text(0.78,y,f'Relleno · Fill ≈ {fill:,.0f} yd³  ({fill*.7646:,.0f} m³)',fontsize=8.8,color=INK); y-=.028
    y=para(fig,0.78,y,'Taludes 3:1 con bordes suaves. Volúmenes ±30–50 % sobre terreno de 30 m.','3:1 side slopes with soft edges. Volumes ±30–50% on 30 m terrain.',w=40,fs=8.8)
    items=[(INK,'-',1.1,'Curva terminada · Finished contour'),('#9d978a',(0,(3,2)),.8,'Terreno existente · Existing ground'),(CLAY,'-',5,'Puerta · Gate'),(WATER,'-',5,'Agua · Water'),('#0b4f8a','--',2.2,'Zanja · Swale')]
    ly=0.235
    for c,st,lw,t in items:
        fig.add_artist(matplotlib.lines.Line2D([0.78,0.81],[ly,ly],color=c,lw=lw,ls=st)); fig.text(0.818,ly-.005,t,fontsize=8.5,color=INK); ly-=.023
    tblock(fig,nxt(),'Plan de terracería','Grading plan'); PAGES.append(fig)
def sheet(fname,es,en):
    src=open(fname,encoding='utf-8').read().replace("exec(open('drain.py',encoding='utf-8').read())","")
    src='\n'.join(l for l in src.split('\n') if not l.startswith('fig.text(0.02,0.03,'))
    g=dict(globals()); exec(src,g); fig=g['fig']; fig.set_dpi(100)
    tblock(fig,nxt(),es,en); PAGES.append(fig)
def views(items,es,en):
    fig=newpage(); heading(fig,es,en)
    n=len(items); cols=2 if n<=4 else 3; rows=math.ceil(n/cols)
    top=0.87; bot=0.085; gap=0.018; cw=(0.96-(cols-1)*gap)/cols; rh=(top-bot-(rows-1)*0.05)/rows
    for k,(num_,tes,ten) in enumerate(items):
        r,c=divmod(k,cols); x=0.02+c*(cw+gap); y=top-(r+1)*rh-r*0.05+0.03
        ax=fig.add_axes([x,y,cw,rh-0.03]); a=img(num_); ax.imshow(a); ax.set_aspect('auto') if False else None; ax.axis('off')
        fig.text(x,y-0.018,tes,fontsize=9.5,weight='bold',color=INK); fig.text(x,y-0.034,ten,fontsize=8.5,color=MUTED,style='italic')
    tblock(fig,nxt(),es,en); PAGES.append(fig)
def placeholder(es,en,goes_es,goes_en,boxes,notes=None):
    fig=newpage(); heading(fig,es,en)
    y=para(fig,0.02,0.85,goes_es,goes_en,w=150,fs=11)
    n=len(boxes); cols=min(3,n); rows=math.ceil(n/cols); cw=(0.96-(cols-1)*0.02)/cols; top=y-0.01; rh=(top-0.09-(rows-1)*0.03)/rows
    for k,(bes,ben) in enumerate(boxes):
        r,c=divmod(k,cols); x=0.02+c*(cw+.02); yy=top-(r+1)*rh-r*.03
        fig.add_artist(matplotlib.patches.FancyBboxPatch((x,yy),cw,rh,boxstyle='round,pad=0,rounding_size=0.006',transform=fig.transFigure,fc='#f4f1ea',ec='#cfc7b5',lw=1,ls=(0,(4,3))))
        fig.text(x+cw/2,yy+rh/2+.012,bes,fontsize=12,color=INK,ha='center',weight='bold'); fig.text(x+cw/2,yy+rh/2-.014,ben,fontsize=10,color=MUTED,ha='center',style='italic')
        if notes and k in notes:                       # filled box: the note sits under the heading
            fig.texts[-2].set_y(yy+rh-.04); fig.texts[-1].set_y(yy+rh-.064); ty=yy+rh-.105
            for es_,en_ in notes[k]: ty=para(fig,x+.012,ty,es_,en_,w=int(cw*190),fs=9)
        else: fig.text(x+cw/2,yy+rh/2-.04,'por agregar · to come',fontsize=8,color=CLAY,ha='center')
    tblock(fig,nxt(),es,en); PAGES.append(fig)
def text_refs():
    fig=newpage(); heading(fig,'Texto y referencias','Text and references')
    y=0.85
    blocks=[('La idea','The idea','Un centro ecuestre sencillo y bien cuidado en el valle: un establo de piedra y varas bajo un techo oscuro con claraboya, 8 caballerizas techadas entre las palmas, gradas frente a la pista, una pista oval, un corral redondo y una pista de trote que aprovecha el camino existente. Todo acomodado a la pendiente natural, con el agua de lluvia guiada y guardada en lugar de dejarla correr.','A simple, well-kept equestrian centre in the valley: a stable of stone and sticks under a dark roof with a clerestory, 8 covered stalls among the palms, bleachers facing the arena, an oval arena, a round pen and a riding track that uses the existing road. Everything sits into the natural slope, and rainwater is guided and kept instead of left to run off.'),
            ('Materiales','Materials','Cerchas de acero cada 12 ft sobre postes de tubo de 6 in; piedra del lugar apilada hasta 5 ft con un tubo negro que flota arriba; hasta el alero, paneles de varas horizontales como nido de pájaro en marco de acero oscuro; lámina gris oscuro con claraboya abierta; cuartos de lavado y monturas en paca de paja o cob aplanado; cercas de tubo negro; piso de tierra y caminos de tierra compactada; arena rastrillada en pista y corral.','Steel trusses every 12 ft on 6 in pipe posts; local fieldstone stacked to 5 ft with a black pipe floating above; up to the eave, bird’s-nest panels of horizontal sticks in dark steel frames; dark grey sheet roof with an open clerestory; wash and tack rooms in straw bale or plastered cob; black pipe fences; dirt floor and compacted dirt roads; raked sand in the arena and round pen.'),
            ('Agua','Water','El techo del establo alimenta el bebedero largo y el techo mariposa de las caballerizas llena un bebedero redondo; el agua del cerro se lleva por un canal empastado a un bajo natural abajo de la pista; el excedente sale al oeste.','The stable roof feeds the long trough and the stalls’ butterfly roof fills a round trough; hillside water runs down a grassed waterway to a natural low spot below the track; overflow leaves to the west.')]
    for tes,ten,bes,ben in blocks:
        fig.text(0.02,y,f'{tes} · {ten}',fontsize=13,weight='bold',color=INK); y-=.028
        y=para(fig,0.02,y,bes,ben,w=78,fs=10)
    boxes=[('Muro de piedra','Fieldstone wall'),('Varas de tomate','Tomato-stake walls'),('Techo con claraboya','Clerestory roof'),('Cerca de tubo','Pipe-rail fence'),('Bebedero de piedra','Stone trough'),('Canal empastado','Grassed waterway')]
    cw=0.145; ch=0.23
    for k,(es,en) in enumerate(boxes):
        r,c=divmod(k,3); x=0.52+c*(cw+.012); yy=0.62-r*(ch+.05)
        fig.add_artist(matplotlib.patches.FancyBboxPatch((x,yy),cw,ch,boxstyle='round,pad=0,rounding_size=0.006',transform=fig.transFigure,fc='#f4f1ea',ec='#cfc7b5',lw=1,ls=(0,(4,3))))
        fig.text(x+cw/2,yy+ch/2+.01,es,fontsize=10.5,weight='bold',color=INK,ha='center'); fig.text(x+cw/2,yy+ch/2-.014,en,fontsize=9,color=MUTED,ha='center',style='italic'); fig.text(x+cw/2,yy+ch/2-.04,'foto por agregar · photo to come',fontsize=7.5,color=CLAY,ha='center')
    fig.text(0.52,0.88,'Referencias de materiales y métodos · Material and method references',fontsize=11,weight='bold',color=INK)
    tblock(fig,nxt(),'Texto y referencias','Text and references'); PAGES.append(fig)
def barn_plan():
    fig=newpage(); heading(fig,'Planos arquitectónicos · Establo','Architectural drawings · Stable')
    ax=fig.add_axes([0.03,0.1,0.62,0.76]); ax.set_aspect('equal'); ax.axis('off')
    Rect=matplotlib.patches.Rectangle
    L,D,RUN,ST,AI=72,40,40,12,14; HL,HD=L/2,D/2; RD=(D-AI)/2
    for k in range(6):
        x=-HL+ST*k; ax.add_patch(Rect((x,HD),ST,RUN,fc='#f1ead9',ec=INK,lw=.8)); ax.text(x+6,HD+RUN/2,'corral\nrun\n12×40',ha='center',va='center',fontsize=6.5,color=MUTED)
    for k in range(4):                     # 27 Sep: runs off the four south stalls too (climbing 5 %, low rock wall at the end)
        x=-HL+ST*k; ax.add_patch(Rect((x,-HD-RUN),ST,RUN,fc='#f1ead9',ec=INK,lw=.8)); ax.text(x+6,-HD-RUN/2,'corral\nrun\n12×40',ha='center',va='center',fontsize=6.5,color=MUTED)
    ax.plot([-HL,-HL+4*ST],[-HD-RUN,-HD-RUN],color='#8a7d66',lw=4,solid_capstyle='butt')
    ax.plot([-HL,HL,HL,-HL,-HL],[-HD-2,-HD-2,HD+2,HD+2,-HD-2],color=MUTED,lw=.7,ls=(0,(4,3)))        # roof edge, 2 ft overhang on the long sides
    ax.add_patch(Rect((-HL,-HD),L,D,fc='#b9ad97',ec=INK,lw=2.2))                                      # rock wall on the column lines
    ax.add_patch(Rect((-HL+1.3,-HD+1.3),L-2.6,D-2.6,fc='white',ec='none'))
    for k in range(6):
        x=-HL+ST*k; ax.add_patch(Rect((x+(1.3 if k==0 else 0),HD-RD),ST-(1.3 if k in (0,5) else 0),RD-1.3,fc='white',ec=INK,lw=.8)); ax.text(x+6,HD-RD/2,f'{k+1}\ncaballeriza\nstall',ha='center',va='center',fontsize=6.3)
        ax.add_patch(Rect((x+4,HD-.7),4,1.4,fc=CLAY,ec='none'))                                    # stall door to its run
    x=-HL
    for es,en,w in (('7 caballeriza','stall',12),('8 caballeriza','stall',12),('9 caballeriza','stall',12),('10 caballeriza','stall',12),('monturas y alimento','tack / feed',12),('lavado','wash',12)):
        ax.add_patch(Rect((x+(1.3 if x==-HL else 0),-HD+1.3),w-(1.3 if x==-HL or x+w==HL else 0),RD-1.3,fc='white',ec=INK,lw=.8)); ax.text(x+w/2,-HD+RD/2,f'{es}\n{en}',ha='center',va='center',fontsize=6.3)
        ax.add_patch(Rect((x+w/2-2,-HD-.7),4,1.4,fc=CLAY,ec='none')); x+=w
    ax.text(0,0,'pasillo · aisle 14 ft',ha='center',va='center',fontsize=9,color=MUTED)
    for x in (-HL,HL): ax.add_patch(Rect((x-1,-AI/2),2,AI,fc='white',ec='none')); ax.plot([x,x],[-AI/2,AI/2],color=CLAY,lw=3,ls=(0,(2,1.5)))
    for sx in (-1,1): ax.text(sx*(HL+3),0,'entrada\nentry',ha='center',va='center',fontsize=7,color=CLAY,rotation=90)
    for x in (-36,-12,12,36):
        for y in (-HD,HD): ax.add_patch(matplotlib.patches.Circle((x,y),.9,fc='#6f7d86',ec=INK,lw=.6,zorder=5))
    ax.annotate('',xy=(-HL+4*ST,-HD-4),xytext=(HL,-HD-4),arrowprops=dict(arrowstyle='<->',lw=.8)); ax.text(HL-12,-HD-6,'72 ft (21.9 m) total',ha='center',va='top',fontsize=8)
    ax.annotate('',xy=(HL+8,-HD),xytext=(HL+8,HD),arrowprops=dict(arrowstyle='<->',lw=.8)); ax.text(HL+10,0,'40 ft\n(12.2 m)',va='center',fontsize=9)
    ax.annotate('',xy=(HL+8,HD),xytext=(HL+8,HD+RUN),arrowprops=dict(arrowstyle='<->',lw=.8)); ax.text(HL+10,HD+RUN/2,'40 ft\ncorrales\nruns',va='center',fontsize=8); ax.text(-HL+2*ST,-HD-RUN-3,'muro bajo de piedra · low rock wall',ha='center',va='top',fontsize=7,color=MUTED)
    ax.text(-HL,HD+RUN+3,'N ↑',fontsize=10,weight='bold')
    ax.set_xlim(-50,58); ax.set_ylim(-HD-RUN-8,HD+RUN+6)
    y=0.85
    specs=[('Planta 72 × 40 ft a ejes, pasillo central de 14 ft abierto de punta a punta; una entrada grande en cada extremo, con el marco de tubo a la vista.','72 × 40 ft on the column lines, a 14 ft centre aisle open end to end; a large entry at each gable end, with the pipe frame exposed.'),
           ('10 caballerizas de 12 × 13 ft, 6 al norte y 4 al sur, cada una con su corral de 12 × 40 ft y cerca de tubo negro a 5.5 ft; los corrales del sur suben 5 % con un muro bajo de piedra al final. En el extremo este del lado sur: monturas y alimento, y lavado. La alfalfa se guarda en las caballerizas techadas.','10 stalls of 12 × 13 ft, 6 north and 4 south, each with its own 12 × 40 ft run and a 5.5 ft black pipe fence; the south runs climb 5 % with a low rock wall at their end. At the east end of the south side: tack and feed, and wash. The alfalfa is kept at the covered stalls.'),
           ('Piedra apilada, de grande a chica, hasta 4.5 ft en todo el perímetro; arriba varas de tomate horizontales, sueltas como nido de pájaro, que dejan pasar aire y luz.','Stacked rock, big to small, to 4.5 ft all the way round; above it horizontal tomato stakes, loose like a bird’s nest, that let air and light through.'),
           ('Alero a 12 ft, cumbrera a 17 ft, 2 ft de alero en los lados largos. Techo metálico gris oscuro con una claraboya corrida de 60 × 10 ft sobre el pasillo: 2½ ft de vidrio a cada lado bajo su propio techo, luz y ventilación de cumbrera.','Eave 12 ft, ridge 17 ft, 2 ft overhang on the long sides. Dark grey metal roof with a 60 × 10 ft clerestory over the aisle: 2½ ft of glazing each side under its own roof, for light and ridge ventilation.'),
           ('Los corrales del norte quedan en plano sobre la plataforma; los del sur suben al cerro al 5 %.','The north runs sit flat on the pad; the south runs climb the hill at 5 %.')]
    for es,en in specs: y=para(fig,0.68,y,es,en,w=64,fs=7.3)
    # roof plan with the clerestory (27 Sep)
    ar=fig.add_axes([0.69,0.125,0.26,0.13]); ar.set_aspect('equal'); ar.axis('off')
    ar.add_patch(Rect((-HL,-HD-2),L,D+4,fc='#6c7278',ec=INK,lw=1)); ar.plot([-HL,HL],[0,0],color=INK,lw=.8)
    for x in (-36,-12,12,36): ar.plot([x,x],[-HD-2,HD+2],color='#4f6f86',lw=.5,ls=(0,(3,2)))
    ar.add_patch(Rect((-30,-6),60,12,fc='#4a4f55',ec=INK,lw=.8)); ar.plot([-30,30],[0,0],color='#d9d4c8',lw=.6)
    for s in (-1,1): ar.add_patch(Rect((-30,s*5-.5),60,1,fc='#e8f0f4',ec=INK,lw=.4))
    ar.set_xlim(-HL-2,HL+2); ar.set_ylim(-HD-4,HD+9)
    ar.text(0,HD+5,'Techo y claraboya · Roof and clerestory',ha='center',fontsize=8.5,weight='bold')
    fig.text(0.68,0.1,'Esquema preliminar a partir del diseño de Walker; no es plano de construcción.',fontsize=8,color=MUTED)
    fig.text(0.68,0.085,'Preliminary diagram from Walker’s design; not a construction drawing.',fontsize=8,color=MUTED,style='italic')
    tblock(fig,nxt(),'Planos arquitectónicos','Architectural drawings'); PAGES.append(fig)

def posts_page():
    fig=newpage(); heading(fig,'Estructura · postes de tubo de acero','Structure · steel pipe posts')
    R=matplotlib.patches.Rectangle
    # --- section through post and pier
    ax=fig.add_axes([0.02,0.09,0.30,0.78]); ax.set_aspect('equal'); ax.axis('off'); ax.set_xlim(-6,7); ax.set_ylim(-9.5,14.5)
    ax.add_patch(R((-6,-9.5),13,9.5,fc='#efe6d2',ec='none'))
    ax.plot([-6,7],[0,0],color=INK,lw=1.2)
    ax.add_patch(R((-1.5,-8.3),3,8.3,fc='#cfcac0',ec=INK,lw=1.2,hatch='..'))
    ax.add_patch(matplotlib.patches.Polygon([(-1.5,0),(1.5,0),(1.9,-.01),(-1.9,-.01)],fc='#cfcac0',ec=INK))
    ax.add_patch(R((-.53,-7.9),1.06,19.9,fc='#6f7d86',ec=INK,lw=1))
    ax.add_patch(R((-.8,-8.0),1.6,.12,fc=INK))
    for x in (-.6,.6): ax.plot([x,x],[-8,-7.2],color=INK,lw=1.5)
    ax.add_patch(R((-6,-.0),4.4,4.5,fc='#b9ad97',ec=INK,lw=.8)); ax.text(-3.8,2.2,'piedra\nstone\n4.5 ft',ha='center',va='center',fontsize=7)
    for yy in np.arange(4.8,12,.45): ax.plot([-6,-1.6],[yy,yy],color='#8a6a42',lw=2.2,solid_capstyle='round')
    ax.text(-3.8,8.4,'varas · sticks',ha='center',fontsize=7,color='white',bbox=dict(fc='#8a6a42',ec='none',pad=1))
    ax.add_patch(R((-.8,12),1.6,.14,fc=INK)); ax.plot([-3,4],[12.15,13.9],color='#5d95c2',lw=3)
    dims=[(12,0,'12 ft sobre terreno\nabove grade'),(0,-8,'≈ 8 ft empotrado\nembedded')]
    for top,bot,t in dims:
        ax.annotate('',xy=(3.2,top),xytext=(3.2,bot),arrowprops=dict(arrowstyle='<->',lw=.8)); ax.text(3.5,(top+bot)/2,t,fontsize=7.5,va='center')
    ax.annotate('',xy=(-1.5,-9),xytext=(1.5,-9),arrowprops=dict(arrowstyle='<->',lw=.8)); ax.text(0,-9.4,'pila Ø 3 ft · pier',ha='center',va='top',fontsize=7.5)
    ax.text(1.2,-7.6,'placa ancla soldada\nwelded anchor plate',fontsize=6.5); ax.text(.7,13.2,'placa tapa\ncap plate',fontsize=6.5)
    ax.text(0,14.3,'Tubo de 20 ft sin cortar · 20 ft tube, uncut',ha='center',fontsize=8.5,weight='bold')
    # --- post plan
    ax2=fig.add_axes([0.34,0.52,0.30,0.34]); ax2.set_aspect('equal'); ax2.axis('off'); ax2.set_xlim(-45,45); ax2.set_ylim(-30,30)
    ax2.add_patch(R((-38,-21),76,42,fc='none',ec='#999',lw=.8,ls='--'))
    for x in np.arange(-36,37,12):
        for y in (-21,21): ax2.add_patch(matplotlib.patches.Circle((x,y),1.4,fc='#6f7d86',ec=INK,lw=.6))
    for x in np.arange(-36,37,12): ax2.plot([x,x],[-21,21],color='#5d95c2',lw=.9)
    ax2.text(0,-27,'14 postes a cada 12 ft · armaduras de 42 ft sin postes intermedios',ha='center',fontsize=7.5)
    ax2.text(0,-30.5,'14 posts at 12 ft · 42 ft clear-span trusses, no centre posts',ha='center',fontsize=7.5,style='italic',color=MUTED)
    ax2.text(0,26,'Planta de postes · Post plan',ha='center',fontsize=9,weight='bold')
    rows=[('Tubo · Tube','12 in, cédula 40 o más · Sch 40 or heavier','20–30 % de su capacidad · of its capacity'),
          ('Viento de diseño · Design wind','150–180 km/h (verificar CFE MDOC Viento 2020)','check against CFE wind code'),
          ('Succión del techo · Roof uplift','≈ 6–9 kip (2.7–4.2 t) por poste','per post · governs the footing'),
          ('Pila · Pier','Ø 3 ft (0.9 m) × 8 ft (2.4 m), concreto','governs by uplift, not bending'),
          ('Postes · Posts','14 tubos de 20 ft','14 tubes of 20 ft')]
    y=0.47
    for a,b_,c in rows:
        fig.text(0.34,y,a,fontsize=8.8,weight='bold',color=INK); fig.text(0.34,y-.018,b_,fontsize=8.3,color=INK); fig.text(0.34,y-.034,c,fontsize=8,color=MUTED,style='italic'); y-=.056
    y=0.86
    notes=[('Por qué empotrar: un tubo de 20 ft da 12 ft al alero y 8 ft dentro de una pila de concreto. No hay que cortar, y la base empotrada resiste el momento sin una placa base crítica.','Why embed: a 20 ft tube gives 12 ft to the eave and 8 ft inside a concrete pier. No cutting, and the embedded base takes the bending without a critical base plate.'),
           ('Placa ancla: placa de 16 × 16 × ¾ in soldada al pie del tubo con 4 barras o pernos de cortante, dentro de la pila; placa tapa de ½ in arriba con cartelas para la armadura.','Anchor plate: 16 × 16 × ¾ in plate welded to the tube foot with 4 bars or shear studs, inside the pier; ½ in cap plate on top with gussets for the truss.'),
           ('Opción B: placa base de 20 × 20 × 1¼ in con 4 anclas de 1 in sobre zapata de 6 × 6 × 3 ft; el tubo se corta a 12 ft y el sobrante de 8 ft sirve para corrales y puertas.','Option B: 20 × 20 × 1¼ in base plate, 4 × 1 in anchor rods on a 6 × 6 × 3 ft footing; the tube is cut to 12 ft and the 8 ft offcut serves the runs and gates.'),
           ('Soldadura: si son tubos de pozo petrolero (probable), el acero puede tener más carbono: precalentar, electrodo E7018 bajo hidrógeno y probar una soldadura de muestra.','Welding: if these are oil-field casing (likely), the steel may be higher carbon: preheat, low-hydrogen E7018 rod, and test a sample weld.'),
           ('Muros: la piedra lleva su propio cimiento corrido entre postes; las varas se amarran a largueros de ángulo soldados entre postes a 4.5 y 12 ft.','Walls: the stone gets its own strip footing between posts; the sticks tie to angle girts welded between posts at 4.5 and 12 ft.'),
           ('Antes de construir: medir diámetro y espesor, estudio de suelo, y cálculo firmado por un ingeniero estructural (DRO / corresponsable en seguridad estructural).','Before building: measure diameter and wall, a soil test, and calculations signed by a structural engineer (DRO / structural co-responsible).')]
    for es,en in notes: y=para(fig,0.67,y,es,en,w=60,fs=7.9)
    fig.text(0.67,0.1,'Cálculo preliminar de viabilidad, no es diseño estructural.',fontsize=8.5,weight='bold',color=CLAY)
    fig.text(0.67,0.085,'Preliminary feasibility check, not a structural design.',fontsize=8.5,color=CLAY,style='italic')
    tblock(fig,nxt(),'Estructura','Structure'); PAGES.append(fig)

exec(open('topo_pages.py',encoding='utf-8').read())
exec(open('posts_page.py',encoding='utf-8').read())
exec(open('structure_pages.py',encoding='utf-8').read())
exec(open('stalls_page.py',encoding='utf-8').read())
exec(open('stable_pages_0928.py',encoding='utf-8').read())   # 28 Sep stable: plan + truss structure page
exec(open('walker_pages.py',encoding='utf-8').read())    # 3 Oct: Walker's v14 photo pages (Giant Nature), photos at native resolution
FIN=DL+'/2026-09-28 finalists/'
w_cover()
w_renders(2,[(1,'Alzado oeste: la entrada, el bebedero y las plantas','West elevation: the entry drive, trough and planting'),(2,'Alzado norte: las caballerizas y sus corrales','North elevation: the stalls and their runs'),
             (3,'Alzado sur: el lavado y los corrales','South elevation: the wash room and runs'),(4,'Alzado este: la entrada desde el estacionamiento','East elevation: the parking entry')])
barn_plan()
import qrcode                                             # Walker added a QR to the 3D model; point it at the public copy
_qr=qrcode.QRCode(border=0,box_size=10); _qr.add_data('https://will.100xbtr.com/equino/model/'); _qr.make(fit=True)
_fig=PAGES[-1]; _ax=_fig.add_axes([0.03,0.115,0.05,0.077]); _ax.imshow(np.asarray(_qr.make_image(fill_color='black',back_color='white').convert('L')),cmap='gray',interpolation='nearest'); _ax.axis('off')
_fig.text(0.085,0.168,'Modelo 3D del establo · 3D model of the stable',fontsize=10,weight='bold',color=INK)
_fig.text(0.085,0.150,'Gírelo y explórelo en línea · Turn it and explore it online',fontsize=8.5,color=MUTED)
_fig.text(0.085,0.133,'will.100xbtr.com/equino/model',fontsize=8.5,color=CLAY)
w_renders(3,[(5,'Sobre las caballerizas techadas','Over the covered stalls'),(6,'Bajo el techo mariposa','Under the butterfly roof'),
             (7,'El bebedero redondo y el techo mariposa, desde el oeste','The round trough and the butterfly roof, from the west'),(8,'Desde el cerro: las caballerizas y el establo','From the hill: the covered stalls and the stable')])
stalls_page()
w_renders('3b',[(9,'El lado norte y sus corrales','The north side and its runs'),(10,'Dentro del establo','Inside the stable'),
             (11,'Las gradas y el día de campo','The bleachers and a picnic'),(12,'Los escalones, de lado','The steps from the side')])
w_site()
planview(FIN+'00-plan.png')
w_text_refs()
w_site_materials()
w_inspirations()
truss_page()
existing()
grading()
operator_sheet()
sheet('sheet1.py','Plan de drenaje','Drainage plan')
sheet('sheet2.py','Cortes de terracería','Grading sections')
placeholder('Conversación','Discussion','Resumen del intercambio entre Walker, nosotros, Andrés y Don Miguel sobre este proyecto. Walker completará los acuerdos.','Summary of the exchange between Walker, us, Andrés and Don Miguel about this project. Walker will fill in the agreements.',[('Acuerdos · Walker completa','Agreements · Walker to fill in'),('Preguntas abiertas','Open questions'),('Próximos pasos','Next steps')],
            notes={1:[('Caballerizas del establo: en la v14 Walker puso 12 × 12 ft con corrales de 12 × 30 ft; el modelo y estos planos siguen con 12 × 14 ft y corrales de 12 × 40 ft. ¿Cuál queda?','Stable stalls: in v14 Walker wrote 12 × 12 ft with 12 × 30 ft runs; the model and these drawings still have 12 × 14 ft and 12 × 40 ft runs. Which one stays?')]})

out=os.path.join(OUTDIR,'Centro-Equino-pack-11x17-2026-10-04-v21.pdf')
tmp=os.path.join(os.path.dirname(os.path.abspath('pack.py')),'_pack_vectors.pdf')
with PdfPages(tmp) as pdf:
    for f in PAGES: pdf.savefig(f,dpi=200)
rep=place_photos(tmp,out)
with open('pack_photo_report.txt','w',encoding='utf-8') as fh:
    for pg,src,px,dpi in rep: fh.write(f'p{pg:02d}  {dpi:4d} dpi  {px:>11}  {src}'+chr(10))
for k,f in enumerate(PAGES): f.savefig(f'prev-{k+1:02d}.png',dpi=40)
# web copy of the pack (4 Oct): page images for will.100xbtr.com/equino/pack/, refreshed on every build
import pymupdf as _pm
_web=os.path.join(os.path.dirname(os.path.abspath('pack.py')),'..','..','will-os','equino','pack'); os.makedirs(_web,exist_ok=True)
_doc=_pm.open(out); _n=len(_doc)
for _k,_pg in enumerate(_doc):
    _pix=_pg.get_pixmap(matrix=_pm.Matrix(2200/_pg.rect.width,2200/_pg.rect.width)); Image.frombytes('RGB',(_pix.width,_pix.height),_pix.samples).save(os.path.join(_web,f'p{_k+1:02d}.jpg'),quality=82)
for _old in os.listdir(_web):
    if _old.startswith('p') and _old.endswith('.jpg') and int(_old[1:3])>_n: os.remove(os.path.join(_web,_old))
import json as _json; _json.dump({'pages':_n,'version':os.path.basename(out),'built':__import__('datetime').date.today().isoformat()},open(os.path.join(_web,'pages.json'),'w'))
print('web pages:',_n)
print(out,len(PAGES))
