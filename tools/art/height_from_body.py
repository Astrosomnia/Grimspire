#!/usr/bin/env python3
"""Make a first-pass Height layer from a kit piece's Body layer, pixel for pixel.

usage: python3 height_from_body.py body.png height.png
   or: python3 height_from_body.py asset.forge.json height.png   (reads frame 0's Body)

Rules (same for every piece, so the light behaves the same across the kit):
- the darkest Body shade is mortar / joint: height 45
- every connected run of one other shade is a stone with one flat height:
  second-darkest 120, then 165, then 205 (lighter paint sits further forward), each stone +/-9
- no bevels, no blur, no extra lines: one hard step at each painted joint and nowhere else
- alpha is the Body's alpha exactly
Needs: pillow, numpy, scipy."""
import sys,json,base64,io
import numpy as np
from PIL import Image
from scipy import ndimage as ndi
src,dst=sys.argv[1:3]
if src.endswith('.json'):
    d=json.load(open(src)); im=Image.open(io.BytesIO(base64.b64decode(d['frames'][0]['body'].split(',')[1])))
else: im=Image.open(src)
O=np.array(im.convert('RGBA')).astype(int); a=O[...,3]>127
lum=lambda c:c[0]*.3+c[1]*.59+c[2]*.11
shades=sorted({tuple(c) for c in O[a][:,:3]},key=lum)
if len(shades)>8: sys.exit(f'{len(shades)} shades in Body: too painterly for the rule pass, needs a hand-made height')
rank=np.zeros(a.shape,int)
for i,c in enumerate(shades): rank[(O[...,:3]==c).all(-1)&a]=i
top=max(1,len(shades)-1); H=np.zeros(a.shape); rng=np.random.RandomState(5); n_st=0
for r in range(1,len(shades)):
    lab,n=ndi.label(a&(rank==r)); n_st+=n
    for k in range(1,n+1): H[lab==k]=120+85*(r-1)/max(1,top-1)+rng.randint(-9,10)
H[a&(rank==0)]=45
out=np.zeros(O.shape,np.uint8); out[...,:3]=np.clip(H,1,255).astype(np.uint8)[...,None]; out[...,3]=np.where(a,255,0)
Image.fromarray(out,'RGBA').save(dst); print(f'{dst}: {im.size[0]}x{im.size[1]}, {len(shades)} shades, {n_st} stones')
