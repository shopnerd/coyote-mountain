exec(open('drain.py',encoding='utf-8').read())
fig=plt.figure(figsize=(17,11),dpi=170); fig.patch.set_facecolor('white')
ax=base_axes(fig,[0.015,0.14,0.665,0.80],alpha=.42)
contours(ax,z); features(ax); drainage(ax); works(ax)
for xy,n in CALL: callout(ax,xy,n)
north(ax,140,8); scalebar(ax,6,96)
# side panel
px=0.70
fig.text(px,0.955,'PLAN DE DRENAJE',fontsize=20,weight='bold',color=INK)
fig.text(px,0.93,'Drainage plan · Centro Equino, Chichihuas',fontsize=12.5,color='#555')
y=0.895
for k,(en,es,ten,tes) in enumerate(NOTES):
    fig.text(px,y,f'{k+1}',fontsize=10,weight='bold',color='#b5602e')
    fig.text(px+.018,y,f'{es} · {en}',fontsize=9.5,weight='bold',color=INK)
    import textwrap
    ly=y-.017
    for line in textwrap.wrap(tes,70): fig.text(px+.018,ly,line,fontsize=7.4,color=INK); ly-=.0128
    for line in textwrap.wrap(ten,70): fig.text(px+.018,ly,line,fontsize=7.4,color='#6a655a',style='italic'); ly-=.0128
    y=ly-.008
# legend
items=[(WATER,'-',3,'Flujo concentrado · Concentrated flow'),(WATER,'>',0,'Dirección del agua · Direction of runoff'),('#0b4f8a','--',2.4,'Zanja o canal · Swale or waterway'),('#0b4f8a','-',6,'Alcantarilla o vado · Culvert or ford'),(INK,'-',.9,'Curvas terminadas, 1 pie · Finished contours, 1 ft'),('#c9b48f','-',6,'Caminos y pista · Roads and track')]
for k,(c,st,lw,tx) in enumerate(items):
    lx=0.02+(k%3)*0.225; ly=0.105-(k//3)*0.024
    if st=='>': fig.text(lx+.004,ly-.005,'➜',color=c,fontsize=11)
    else: fig.add_artist(matplotlib.lines.Line2D([lx,lx+.03],[ly,ly],color=c,lw=lw,ls=st))
    fig.text(lx+.038,ly-.005,tx,fontsize=8,color=INK)
fig.text(px,0.118,'Movimiento de tierra · Earthwork',fontsize=8.5,color=INK,weight='bold'); fig.text(px,0.102,f'corte / cut ≈ {cut:,.0f} yd³ ({cut*0.7646:,.0f} m³) · relleno / fill ≈ {fill:,.0f} yd³ ({fill*0.7646:,.0f} m³)',fontsize=8.2,color=INK)
fig.text(px,0.086,'Terreno de datos públicos de 30 m: volúmenes ±30–50 %. Confirmar con levantamiento de dron.',fontsize=7.6,color='#6a655a')
fig.text(px,0.072,'30 m public terrain: volumes ±30–50%. Confirm with a drone survey before building.',fontsize=7.6,color='#6a655a',style='italic')
fig.text(0.02,0.03,'31.9999 N, 116.7641 W · Hoja / Sheet D-1 · 23 sep 2026 · Diseño preliminar, no para construcción · Preliminary design, not for construction',fontsize=8,color='#6a655a')
if not globals().get('PACK'): fig.savefig('D1-drainage.png',dpi=170); print('ok')
