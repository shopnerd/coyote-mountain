import os, glob, pickle, sys
from PIL import Image, ImageOps
from concurrent.futures import ThreadPoolExecutor
R="G:/My Drive/MEXICO/Chichihaus/"
dirs=["2026-09-23 Centro Equino pack/renderings","Horses","Reference Photos","Reference Images","Centro Equino paints","Site photos"]
fs=[]
for d in dirs:
  for ext in ("png","jpg","jpeg","webp","PNG","JPG","JPEG"):
    fs+=glob.glob(R+d+"/**/*."+ext,recursive=True)
fs+=glob.glob("C:/Users/wrollins/WebDev/coyote-studio/projects/renders/**/*.png",recursive=True)
fs=sorted(set(fs))
def th(f):
  try:
    im=Image.open(f); im.draft("RGB",(400,400)); W,H=im.size
    im=ImageOps.exif_transpose(im).convert("RGB"); sz=im.size; im.thumbnail((256,256))
    return f,im,Image.open(f).size if False else None
  except Exception as e: return f,None,str(e)
with ThreadPoolExecutor(16) as ex: res=list(ex.map(th,fs))
db={f:im for f,im,_ in res if im is not None}
pickle.dump(db,open("thumbs.pkl","wb")); print(len(fs),len(db))
