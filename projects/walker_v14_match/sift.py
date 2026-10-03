import pickle, json, glob, numpy as np, cv2
from PIL import Image, ImageOps
from concurrent.futures import ThreadPoolExecutor
db=pickle.load(open("thumbs.pkl","rb")); fs=list(db)
sift=cv2.SIFT_create(800)
def feat(f):
  try:
    im=Image.open(f); im.draft("RGB",(900,900)); im=ImageOps.exif_transpose(im).convert("L"); W,H=Image.open(f).size
    sc=700/max(im.size); im=im.resize((int(im.width*sc),int(im.height*sc)))
    k,d=sift.detectAndCompute(np.asarray(im),None)
    return f,(np.float32([p.pt for p in k]),d,im.size)
  except Exception as e: return f,None
with ThreadPoolExecutor(12) as ex: R=dict(ex.map(feat,fs))
pickle.dump(R,open("sift.pkl","wb")); print(len(R))
