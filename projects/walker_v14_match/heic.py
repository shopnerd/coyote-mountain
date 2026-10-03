import glob, json, pickle, numpy as np, cv2
from PIL import Image, ImageOps
import pillow_heif; pillow_heif.register_heif_opener()
from concurrent.futures import ThreadPoolExecutor
R="G:/My Drive/MEXICO/Chichihaus/"
fs=[f for f in glob.glob(R+"**/*.heic",recursive=True)+glob.glob(R+"**/*.HEIC",recursive=True)]
fs+=[f for f in glob.glob(R+"Site photos/*.*")+glob.glob(R+"Horses/**/*.*",recursive=True) if f.lower().endswith(('.jpg','.jpeg','.png'))]
fs=sorted(set(fs)); print(len(fs),flush=True)
sift=cv2.SIFT_create(800)
def feat(f):
  try:
    im=ImageOps.exif_transpose(Image.open(f)); sz=im.size; im=im.convert("L"); sc=700/max(im.size); im=im.resize((int(im.width*sc),int(im.height*sc)))
    k,d=sift.detectAndCompute(np.asarray(im),None); return f,(np.float32([p.pt for p in k]),d,im.size,sz)
  except Exception as e: return f,None
with ThreadPoolExecutor(8) as ex: F=dict(ex.map(feat,fs))
pickle.dump(F,open("sift_heic.pkl","wb"))
slots=json.load(open("slots.json")); reg=json.load(open("reg.json"))
s2=cv2.SIFT_create(1500); bf=cv2.BFMatcher()
pages={int(f[8:10]):np.asarray(Image.open(f).convert("L")) for f in glob.glob("v14img/p0[1-8]-*.jpeg")}
for key in ["1-0","7-2","7-4","7-5","7-6","7-7","6-5"]:
  x0,y0,x1,y1=reg[key]['rect']; pg=int(key.split('-')[0]); sl=pages[pg][y0:y1,x0:x1]; sc=700/max(sl.shape); slr=cv2.resize(sl,None,fx=sc,fy=sc)
  ks,ds=s2.detectAndCompute(slr,None); best=(0,None,None,None)
  for f,v in F.items():
    if v is None or v[1] is None or len(v[1])<8: continue
    m=bf.knnMatch(ds,v[1],k=2); g=[a for a,b in (p for p in m if len(p)==2) if a.distance<.7*b.distance]
    if len(g)<12 or len(g)<=best[0]: continue
    src=np.float32([ks[a.queryIdx].pt for a in g]); dst=v[0][[a.trainIdx for a in g]]
    M,inl=cv2.estimateAffinePartial2D(src,dst,ransacReprojThreshold=4)
    if M is None or abs(M[0,0])<1e-3: continue
    n=int(inl.sum())
    if n>best[0]: best=(n,f,M,v[2])
  n,f,M,sz=best
  if f is None: print(key,'NONE',flush=True); continue
  h,w=slr.shape; C=np.float32([[0,0],[w,0],[w,h],[0,h]]); D=(M[:,:2]@C.T).T+M[:,2]
  fr=[float(D[:,0].min()/sz[0]),float(D[:,1].min()/sz[1]),float(D[:,0].max()/sz[0]),float(D[:,1].max()/sz[1])]
  print(key,n,f[-60:],[round(x,3) for x in fr],flush=True)
  reg[key+"-heic"]={'rect':reg[key]['rect'],'src':f,'inliers':n,'crop':fr}
json.dump(reg,open("reg2.json","w"),indent=0)
