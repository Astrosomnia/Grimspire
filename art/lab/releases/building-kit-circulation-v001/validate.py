from PIL import Image
import numpy as np,json,pathlib,base64,io
R=pathlib.Path(__file__).parent;m=json.load(open(R/'manifest.json'))
for a in m:
 d=json.load(open(R/a['file']));f=d['frames'][0];ls={k:np.array(Image.open(io.BytesIO(base64.b64decode(v.split(',')[1]))).convert('RGBA')) for k,v in f.items() if v};b=ls['body'];mask=b[...,3]>0
 assert not d['ready'] and d['game_scale']==1
 for k,v in ls.items():assert v.shape==b.shape and np.isin(v[...,3],[0,255]).all()
 for k in ('height','guts'):assert np.array_equal(ls[k][...,3],b[...,3])
 assert (ls['height'][...,0]==ls['height'][...,1]).all() and (ls['height'][...,0]==ls['height'][...,2]).all()
 if a['id']=='BK81':assert not mask[28:112,:].any()
 if a['id']=='BK43':
  prev=json.load(open(R/'../building-kit-batch2'/a['file']));assert np.array_equal(b,np.array(Image.open(io.BytesIO(base64.b64decode(prev['frames'][0]['body'].split(',')[1]))).convert('RGBA')))
 if a['id'] in ('BK40','BK41','BK42'):
  seen=set();sizes=[]
  for yy,xx in zip(*np.where(mask)):
   if (yy,xx) in seen:continue
   q=[(yy,xx)];seen.add((yy,xx));size=0
   while q:
    y,x=q.pop();size+=1
    for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
     ny,nx=y+dy,x+dx
     if 0<=ny<d['h'] and 0<=nx<d['w'] and mask[ny,nx] and (ny,nx) not in seen:seen.add((ny,nx));q.append((ny,nx))
   sizes.append(size)
  assert len(sizes)==(2 if a['id']=='BK41' else 1),(a['id'],sizes)
  if a['id']=='BK41':assert not mask[:,48:80].any()
print('PASS: masks, scale, alpha, greyscale, connected stair flights, broken gap, preserved ledges, full bridge end corridor')
