import math, io, os, requests, numpy as np
from PIL import Image
W,H,siteW,rot=150,100,400.0,318.0
cs=siteW/(W-1); D=math.pi/180; t=rot*D
la0,lo0=31.999872751999938,-116.76412450955283
def LL(i,j):
    sx=(i-(W-1)/2)*cs; sy=((H-1)/2-j)*cs
    dx=sx*math.cos(t)+sy*math.sin(t); dy=-sx*math.sin(t)+sy*math.cos(t)
    return la0+dy/111320, lo0+dx/(111320*math.cos(la0*D))
def GR(lat,lon):  # inverse
    dy=(lat-la0)*111320; dx=(lon-lo0)*111320*math.cos(la0*D)
    sx=dx*math.cos(t)-dy*math.sin(t); sy=dx*math.sin(t)+dy*math.cos(t)
    return sx/cs+(W-1)/2, (H-1)/2-sy/cs
Z=19
def tile_xy(lat,lon,z=Z):
    n=2**z; x=(lon+180)/360*n; y=(1-math.asinh(math.tan(lat*D))/math.pi)/2*n; return x,y
def mosaic():
    if os.path.exists('mosaic.npy'): return np.load('mosaic.npy'), tuple(np.load('origin.npy'))
    corners=[LL(i,j) for i in (0,W-1) for j in (0,H-1)]
    xs=[tile_xy(*c)[0] for c in corners]; ys=[tile_xy(*c)[1] for c in corners]
    x0,x1,y0,y1=int(min(xs)),int(max(xs)),int(min(ys)),int(max(ys))
    M=np.zeros(((y1-y0+1)*256,(x1-x0+1)*256,3),np.uint8)
    for ty in range(y0,y1+1):
        for tx in range(x0,x1+1):
            r=requests.get(f'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{Z}/{ty}/{tx}',timeout=30,headers={'User-Agent':'coyote-topo'})
            im=Image.open(io.BytesIO(r.content)).convert('RGB'); M[(ty-y0)*256:(ty-y0+1)*256,(tx-x0)*256:(tx-x0+1)*256]=np.array(im)
    np.save('mosaic.npy',M); np.save('origin.npy',np.array([x0,y0])); return M,(x0,y0)
def render(i0,j0,i1,j1,ppc):
    M,(x0,y0)=mosaic()
    w=int((i1-i0)*ppc); h=int((j1-j0)*ppc)
    I=i0+np.arange(w)/ppc; J=j0+np.arange(h)/ppc; II,JJ=np.meshgrid(I,J)
    sx=(II-(W-1)/2)*cs; sy=((H-1)/2-JJ)*cs
    dx=sx*math.cos(t)+sy*math.sin(t); dy=-sx*math.sin(t)+sy*math.cos(t)
    lat=la0+dy/111320; lon=lo0+dx/(111320*math.cos(la0*D))
    n=2**Z; px=((lon+180)/360*n-x0)*256; py=((1-np.arcsinh(np.tan(lat*D))/math.pi)/2*n-y0)*256
    px=np.clip(px.astype(int),0,M.shape[1]-1); py=np.clip(py.astype(int),0,M.shape[0]-1)
    return Image.fromarray(M[py,px])
