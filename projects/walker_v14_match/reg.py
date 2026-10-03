import pickle, json, glob, numpy as np, cv2
from PIL import Image
F=pickle.load(open("sift.pkl","rb")); slots=json.load(open("slots.json"))
sift=cv2.SIFT_create(1500); bf=cv2.BFMatcher()
pages={int(f[8:10]):np.asarray(Image.open(f).convert("L")) for f in glob.glob("v14img/p0[1-8]-*.jpeg")}
out={}
for pg,s in sorted(slots.items(),key=lambda x:int(x[0])):
  for k,r in enumerate(s['rects']):
    x0,y0,x1,y1=r; sl=pages[int(pg)][y0:y1,x0:x1]
    sc=700/max(sl.shape); slr=cv2.resize(sl,None,fx=sc,fy=sc)
    ks,ds=sift.detectAndCompute(slr,None); best=(0,None,None)
    for f,v in F.items():
      if v is None or v[1] is None or len(v[1])<8: continue
      m=bf.knnMatch(ds,v[1],k=2); g=[a for a,b in (p for p in m if len(p)==2) if a.distance<.7*b.distance]
      if len(g)<12 or len(g)<=best[0]: continue
      src=np.float32([ks[a.queryIdx].pt for a in g]); dst=v[0][[a.trainIdx for a in g]]
      M,inl=cv2.estimateAffinePartial2D(src,dst,ransacReprojThreshold=4)
      if M is None: continue
      n=int(inl.sum())
      if n>best[0]: best=(n,f,M,v[2])
    n,f,M,sz=best
    if f is None: out[f"{pg}-{k}"]={'rect':r,'src':None}; print(pg,k,'NONE'); continue
    # slot corners (in slr px) -> source fraction
    h,w=slr.shape; C=np.float32([[0,0],[w,0],[w,h],[0,h]]); D=(M[:,:2]@C.T).T+M[:,2]
    fr=[float(D[:,0].min()/sz[0]),float(D[:,1].min()/sz[1]),float(D[:,0].max()/sz[0]),float(D[:,1].max()/sz[1])]
    out[f"{pg}-{k}"]={'rect':r,'src':f,'inliers':n,'crop':fr}
    print(pg,k,n,f[-55:],[round(x,3) for x in fr])
json.dump(out,open("reg.json","w"),indent=0)
