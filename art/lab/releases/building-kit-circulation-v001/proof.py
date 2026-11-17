from PIL import Image,ImageDraw,ImageFont
import numpy as np,json,pathlib,io,base64
R=pathlib.Path(__file__).parent;m=json.load(open(R/'manifest.json'));c=Image.new('RGB',(1000,80+len(m)*155),(64,74,88));dr=ImageDraw.Draw(c)
dr.text((18,14),'GRIMSPIRE: circulation + roof fixes / native 1x',fill=(230,234,239));dr.text((18,40),'Left: raw layers. Right: Height-light study (illustrative, not game shader).',fill=(220,224,230))
for n,a in enumerate(m):
 d=json.load(open(R/a['file']));f=d['frames'][0]
 def read(k):return Image.open(io.BytesIO(base64.b64decode(f[k].split(',')[1]))).convert('RGBA') if f.get(k) else Image.new('RGBA',(a['w'],a['h']))
 body,back,z=read('body'),read('back'),read('height');im=Image.alpha_composite(back,body);raw=np.asarray(body).astype(float);zz=np.asarray(z)[...,0].astype(float);al=raw[...,3]>0
 # Symmetric bevel depth response with a top-left test light, generated only for proof.
 dzx=np.gradient(zz,axis=1);dzy=np.gradient(zz,axis=0);fac=np.clip(1.5+(-dzx-dzy)*.025,.55,2.8)
 raw[...,:3]=np.clip(raw[...,:3]*fac[...,None],0,255);lit=Image.alpha_composite(back,Image.fromarray(raw.astype('uint8')))
 scale=min(1,420/a['w'],128/a['h']);sz=(round(a['w']*scale),round(a['h']*scale));y=80+n*155
 dr.text((18,y),a['id']+' '+d['name'],fill=(230,234,239));c.paste(im.resize(sz,Image.Resampling.NEAREST),(18,y+22),im.resize(sz,Image.Resampling.NEAREST));c.paste(lit.resize(sz,Image.Resampling.NEAREST),(520,y+22),lit.resize(sz,Image.Resampling.NEAREST))
c.save(R/'proof.png')
