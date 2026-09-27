# pack page: the covered stalls (26 Sep). exec'd by pack.py after barn_plan(); numbers match covered_stalls.py
def stalls_page():
    fig=newpage(); heading(fig,'Caballerizas techadas','Covered stalls')
    Rect=matplotlib.patches.Rectangle
    PS,SW,SD,CW,OV=4,16,20,12,12; NB=PS+1; L=NB*SW; HL=L/2; HC=CW/2; HD=HC+SD; RE=HC+OV; XS=-HL+PS*SW
    TR,TX=4,-HL-7-4; TO=TX-TR-10
    ax=fig.add_axes([0.02,0.34,0.66,0.52]); ax.set_aspect('equal'); ax.axis('off')
    for sg in (-1,1):
        y0,y1=sorted((sg*HC,sg*HD)); ys0,ys1=sorted((sg*HC,sg*RE))
        ax.add_patch(Rect((-HL,y0),PS*SW,y1-y0,fc='#f1ead9',ec='none'))                                # open backs
        ax.add_patch(Rect((-HL,ys0),L,ys1-ys0,fc='#d9e6ef',ec='none'))                                # under the roof
        yl0,yl1=sorted((sg*HC,sg*(HC+6))); ax.add_patch(Rect((-HL,yl0),PS*SW,yl1-yl0,fc='none',ec='#9fb6c7',lw=0,hatch='////'))   # level strip
        for q in range(PS+1): ax.plot([-HL+q*SW]*2,[y0,y1],color=INK,lw=.9)
        ax.plot([-HL,XS],[sg*HC]*2,color=INK,lw=1.4); ax.plot([-HL,XS],[sg*HD]*2,color=INK,lw=1.1)
        for q in range(PS): ax.text(-HL+q*SW+SW/2,sg*(RE+(HD-RE)/2),f'{q+1 if sg<0 else q+5}',ha='center',va='center',fontsize=7.5,color=MUTED)
        for q in range(1,PS,2): ax.add_patch(matplotlib.patches.Circle((-HL+q*SW,sg*(HC+1)),.9,fc='#1f78c8',ec=INK,lw=.5,zorder=5))
        for q in range(NB+1):
            for yy in (sg*HC,sg*RE): ax.add_patch(Rect((-HL+q*SW-.5 if 0<q<NB else (-HL if q==0 else HL-1),yy-.5),1,1,fc=INK,zorder=6))
    ax.add_patch(Rect((XS,-RE),SW,2*RE,fc='#e8d9a8',ec=INK,lw=1.2,zorder=4)); ax.plot([HL,HL],[-6,6],color='#e8d9a8',lw=3,zorder=5)   # alfalfa bay under the roof, gate on the road end
    ax.text(XS+SW/2,0,'alfalfa\n16 × 36',ha='center',va='center',fontsize=7.5,weight='bold',zorder=6)
    ax.text(HL+2,0,'puerta · gate',ha='left',va='center',fontsize=6.5,color=MUTED,rotation=90)
    ax.plot([-HL-2,HL+2,HL+2,-HL-2,-HL-2],[-RE,-RE,RE,RE,-RE],color=CLAY,lw=1.1,ls=(0,(5,3)))            # roof edge
    ax.annotate('',xy=(-HL-2,0),xytext=(HL-4,0),arrowprops=dict(arrowstyle='-|>',color='#1f78c8',lw=1.4))
    ax.text(0,1.2,'valle del techo, cae 0.5 % · roof valley, falls 0.5%',fontsize=7.5,color='#1f78c8',ha='center',va='bottom')
    ax.plot([-HL-2,TX+2],[0,0],color='#1f78c8',lw=3.5,solid_capstyle='butt')                           # open chute
    ax.add_patch(matplotlib.patches.Circle((TX,0),TR,fc='#cfe3f3',ec=INK,lw=1.2)); ax.text(TX,-TR-2.2,'bebedero\ntrough Ø 8 ft',ha='center',va='top',fontsize=7)
    ax.plot([TX-TR,TO],[0,0],color='#1f78c8',lw=1.2,ls=(0,(2,1.5)))
    ax.plot([HL+10,TO,TO],[HD+6,HD+6,-HD-20],color='#0b4f8a',lw=1.8,ls=(0,(5,2)))
    ax.text(-10,HD+8,'zanja arriba, cae 1 % al suroeste · ditch above, falls 1% to the south-west',ha='center',fontsize=7.3,color='#0b4f8a')
    ax.text(TO-2,-HD-14,'a la zanja del camino\ndel establo · to the ditch\nabove the barn road',ha='right',fontsize=7,color='#0b4f8a')
    ax.text(0,-3.2,'pasillo · corridor 12 ft',ha='center',fontsize=8.5,color=INK)
    ax.annotate('',xy=(-HL,-HD-6),xytext=(HL,-HD-6),arrowprops=dict(arrowstyle='<->',lw=.8)); ax.text(0,-HD-8,'80 ft (24 m) · 5 × 16 ft',ha='center',va='top',fontsize=8.5)
    ax.annotate('',xy=(HL+6,-HD),xytext=(HL+6,HD),arrowprops=dict(arrowstyle='<->',lw=.8)); ax.text(HL+8,0,'52 ft\n(16 m)\n20 + 12 + 20',va='center',fontsize=8)
    ax.annotate('',xy=(-HL-7,-HD+1),xytext=(-HL,-HD+1),arrowprops=dict(arrowstyle='<->',lw=.6)); ax.text(-HL-3.5,-HD+2.5,'7 ft',ha='center',fontsize=6.5)
    ax.text(HL+14,HD-6,'NE →\ncamino principal\nmain road',fontsize=7,color=MUTED)
    ax.text(-HL,HD+14,'cuesta arriba (SE) ↑ uphill',fontsize=7.5,color=MUTED)
    ax.set_xlim(TO-14,HL+22); ax.set_ylim(-HD-24,HD+17)
    lx,ly=0.02,0.325
    for fc,hat,t in (('#d9e6ef',None,'bajo techo · under the roof (12 ft of each stall)'),('#f1ead9',None,'fondo abierto · open back (8 ft of each stall)'),('none','////','franja a nivel · level strip (6 ft) for waterer and feeder')):
        fig.add_artist(Rect((lx,ly-.006),.018,.012,transform=fig.transFigure,fc=fc,ec='#9fb6c7',hatch=hat)); fig.text(lx+.024,ly-.004,t,fontsize=7.8,color=INK); lx+=.22
    fig.add_artist(matplotlib.patches.Circle((0.028,0.301),.004,transform=fig.transFigure,fc='#1f78c8',ec=INK,lw=.5)); fig.text(0.044,0.297,'bebedero automático, uno por cada dos caballerizas · automatic waterer, one per two stalls',fontsize=7.8,color=INK)
    # cross-section through the butterfly roof
    sx=fig.add_axes([0.03,0.085,0.62,0.19]); sx.set_aspect('equal'); sx.axis('off')
    val,rise=10.5,.75
    def g(y):
        e=abs(y)-HC-6
        if e<=0: return 0.0
        drop=.05*min(e,2)+.08*max(0,e-2)
        return -drop if y<0 else drop
    Y=np.linspace(-HD,HD,200); G=[g(y) for y in Y]
    sx.fill_between(Y,G,-4,color='#e8dfcc'); sx.plot(Y,G,color=INK,lw=1.4)
    sx.plot(Y,[.11*y for y in Y],color=MUTED,lw=.8,ls=(0,(3,2)))
    for y in (-RE,-HC,HC,RE): sx.plot([y,y],[g(y),val+rise*abs(y)/RE],color='#6f7d86',lw=2.2)
    for sg in (-1,1):
        sx.plot([sg*HD]*2,[g(sg*HD),g(sg*HD)+5],color=INK,lw=.9); sx.plot([sg*HC]*2,[0,5],color=INK,lw=.9)
    sx.plot([-RE,0,RE],[val+rise,val,val+rise],color=CLAY,lw=2.6)
    sx.text(0,val-.9,'valle · valley 10.3–10.7 ft',ha='center',va='top',fontsize=7)
    sx.text(RE+.5,val+rise+.3,'alero · eave ≈ 11–11.5 ft',fontsize=7)
    sx.text(-HD,-3.4,'NO · NW (cuesta abajo · downhill)',fontsize=7,color=MUTED); sx.text(HD,-3.4,'SE (cuesta arriba · uphill)',fontsize=7,color=MUTED,ha='right')
    sx.text(-HD+1,13,'Corte transversal · Cross-section (terreno natural punteado · natural ground dashed)',fontsize=8.5,weight='bold')
    sx.set_xlim(-HD-2,HD+2); sx.set_ylim(-4.5,14)
    y=0.85
    specs=[('8 caballerizas de 16 × 20 ft, 4 por lado, frente a un pasillo de 12 ft; en el extremo del lado del establo, bajo el mismo techo, la bodega de alfalfa de 16 × 36 ft; 80 × 52 ft en total.','8 stalls of 16 × 20 ft, 4 a side, facing a 12 ft corridor; at the stable end, under the same roof, the 16 × 36 ft alfalfa bay; 80 × 52 ft overall.'),
           ('Techo mariposa de 84 × 36 ft sobre el pasillo y los primeros 12 ft de cada caballeriza; pendiente de ½:12 hacia un valle central, el mínimo para lámina de junta alzada.','Butterfly roof 84 × 36 ft over the corridor and the first 12 ft of every stall; ½:12 down to a centre valley, the least a standing-seam roof takes.'),
           ('El valle cae 0.5 % al suroeste y sigue como canalón abierto, en voladizo de 7 ft sin poste, hasta un bebedero redondo de 8 ft a 7 ft del extremo, con paso libre alrededor.','The valley falls 0.5% to the south-west and carries on as an open chute, cantilevered 7 ft with no post, into an 8 ft round trough 7 ft from the building end, with room to walk round it.'),
           ('Agua: el techo capta unos 7,100 L por cada 2.5 cm de lluvia; el bebedero (unos 1,900 L) se llena con unos 7 mm. Las demasías van por tubo enterrado a la zanja.','Water: the roof sheds about 1,900 gal per inch of rain; the trough (about 500 gal) fills with about a quarter inch. Overflow runs in a buried pipe to the ditch.'),
           ('Pasillo a nivel de lado a lado (1,089 ft); frentes techados con franja a nivel de 6 ft y caída de 5 % como máximo; fondos abiertos hasta 8 %, siguiendo el terreno. Las palmas pueden quedar en los fondos. La alfalfa se descarga por una puerta al camino principal, junto al establo, y los caballos no la alcanzan.','Corridor level side to side (about 1,089 ft); covered fronts with a 6 ft level strip and at most 5%; open backs up to 8%, following the ground. Palms can stay in the open backs. The alfalfa unloads through a gate on the main road by the stable, out of the horses’ reach.'),
           ('Holguras: 18 ft al camino principal, 34 ft al camino del corral redondo, 29 ft al camino del cerro.','Clearances: 18 ft to the main road, 34 ft to the round pen road, 29 ft to the scrub-side road.')]
    for es,en in specs: y=para(fig,0.70,y,es,en,w=60,fs=7.4)
    fig.text(0.70,0.1,'Esquema preliminar; la estructura del techo requiere cálculo de un ingeniero (DRO).',fontsize=8,color=MUTED)
    fig.text(0.70,0.085,'Preliminary diagram; the roof structure needs an engineer’s calculation (DRO).',fontsize=8,color=MUTED,style='italic')
    tblock(fig,nxt(),'Caballerizas techadas','Covered stalls'); PAGES.append(fig)
