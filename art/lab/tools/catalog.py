"""Reproducible Forge documents from existing source PNGs; no redraw or resizing."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,io,base64,hashlib,re
root=Path(__file__).resolve().parents[3]
out=root/'art/lab/hosted/catalog';out.mkdir(exist_ok=True)
entries=[]
def url(im):
 b=io.BytesIO();im.save(b,format='PNG');return 'data:image/png;base64,'+base64.b64encode(b.getvalue()).decode()
def add(id,code,name,frames,markers=None,notes='',path=None):
 w,h=frames[0]['body'].size if frames and hasattr(frames[0]['body'],'size') else (0,0)
 if w:
  frames=[{k:url(v) for k,v in f.items()} for f in frames]
  d=dict(forge=1,code=code,name=name,w=w,h=h,fps=6,base=None,markers=markers or {},frames=frames,notes=notes,ready=False,pixel_scale=12)
 else:d=json.loads(path.read_text());w,h=d['w'],d['h'];code=d.get('code','');name=d['name']
 raw=json.dumps(d,separators=(',',':'))+'\n';p=out/(id+'.forge.json');p.write_text(raw)
 im=Image.open(io.BytesIO(base64.b64decode(d['frames'][0]['body'].split(',')[1]))).convert('RGBA');im.thumbnail((96,96),Image.Resampling.NEAREST)
 entries.append(dict(id=id,path=str(p.relative_to(root)),sha256=hashlib.sha256(raw.encode()).hexdigest(),code=code,name=name,w=w,h=h,frame_count=len(d['frames']),thumbnail=url(im),category='Troopers' if code.startswith('T') else 'Arms' if code.startswith('A') else 'Weapons' if code.startswith('W') else 'Other art'))
# Existing editable studies, including approved alternatives.
for folder in ['art/lab/releases/weapons-v001','art/lab/hosted/library']:
 for p in sorted((root/folder).glob('*.forge.json')):add(('study-' if 'releases' in folder else 'alt-')+p.stem,'','',[],path=p)
# Preserve artwork from every earlier saved build, even after its preview slot changed.
seen=set()
for p in sorted((root/'art/lab/hosted/revisions').glob('*/payload.json')):
 for slot,d in json.loads(p.read_text()).get('assets',{}).items():
  digest=hashlib.sha256(json.dumps(d,sort_keys=True).encode()).hexdigest()
  if digest in seen:continue
  seen.add(digest)
  # Feed the exact saved document through the same immutable catalog writer.
  import tempfile
  with tempfile.NamedTemporaryFile(mode='w',suffix='.json') as f:
   json.dump(d,f);f.flush();add('saved-'+digest[:20],d.get('code',''),d.get('name',''),[],path=Path(f.name))
# All source kits; manifested animation sheets retain their frames and layers.
used=set()
for kit in sorted((root/'art/kits').iterdir()):
 manifest=json.loads((kit/'manifest.json').read_text()) if (kit/'manifest.json').exists() else {}
 states=manifest.get('states',{})
 if 'frame_count' in manifest and 'layers' in manifest:states={'walk':{'frames':manifest['frame_count'],'files':manifest['layers']}}
 for n,s in states.items():
  files=s.get('files',{});frames=[];count=s['frames'];layers={}
  for k,fn in files.items():
   p=kit/fn
   if not p.exists():continue
   layers['emis' if k=='emissive' else k]=Image.open(p).convert('RGBA');used.add(p)
  if 'body' not in layers:continue
  w,h=layers['body'].size;fw=w//count
  for i in range(count):frames.append({k:im.crop((i*fw,0,(i+1)*fw,h)) for k,im in layers.items()})
  add(kit.name+'-'+n,'T01',kit.name+' · '+n,frames,notes=manifest.get('limitations','Original registered animation frames.'))
 for p in sorted(kit.glob('*.png')):
  if p in used or any(x in p.stem for x in ['preview','contact_sheet','stride','guide']):continue
  im=Image.open(p).convert('RGBA')
  if max(im.size)>1024:continue
  # Group base/body with associated layers; remaining source parts stay accessible.
  if p.stem.endswith(('_emissive','_trim')):continue
  stem=re.sub(r'_(body|base)$','',p.stem);layers={'body':im}
  for suffix,k in [('emissive','emis'),('trim','trim')]:
   q=kit/(stem+'_'+suffix+'.png')
   if q.exists():
    layer=Image.open(q).convert('RGBA')
    if layer.size==im.size:layers[k]=layer
  code=p.stem[:3] if re.match('[A-Z][0-9]{2}',p.stem) else 'A02' if 'arm' in p.stem else 'C99'
  add(kit.name+'-'+p.stem,code,kit.name+' · '+stem.replace('_',' '),[layers])
# Exact pixel version of the current procedural foreground sleeve/glove.
im=Image.new('RGBA',(18,8));dr=ImageDraw.Draw(im)
rects=[('#070b12',-14,-3,12,6),('#354152',-13,-2,10,4),('#536277',-12,-2,7,1),('#222b39',-12,1,8,1),('#111926',-5,-3,3,6),('#6c7887',-4,-2,2,4),('#070b12',-2,-3,5,6),('#070b12',-3,-2,2,3),('#687484',-1,-2,3,4),('#a0a9b4',0,-2,2,1),('#a0a9b4',1,0,1,1),('#a0a9b4',1,2,1,1),('#374251',-1,0,2,1),('#374251',-1,2,2,1),('#8995a3',-2,-2,1,2)]
for c,x,y,w,h in rects:dr.rectangle((x+14,y+3,x+14+w-1,y+3+h-1),fill=c)
add('single-gun-arm-v001','A01','Gun arm · single foreground sprite',[{'body':im}],{'hand':[14,3],'shoulder':[0,3],'pivot':[14,3]},'One sprite. Hand anchors to weapon grip; drawn in front of gun. No elbow required.')
# Runtime atlas pieces, preserving the exact source pixels and registration.
game=(root/'art/lab/sandbox/game.html').read_text()
props=json.loads(re.search(r'P:(\{.*?\}),up:4',game).group(1))
atlas=Image.open(root/'art/in-game/props-weapons-atlas.png').convert('RGBA')
for n,m in props.items():
 if n.endswith('_e') or n+'_e' not in props:continue
 x,y,w,h=m['r'];layers={'body':atlas.crop((x,y,x+w,y+h))}
 e=props[n+'_e']['r'];layers['emis']=atlas.crop((e[0],e[1],e[0]+e[2],e[1]+e[3]))
 marks={k:[v[0]*4,v[1]*4] for k,v in [('grip',m.get('g')),('muzzle',m.get('m')),('pivot',m.get('p'))] if v}
 add('game-'+n,'W99' if m.get('g') else 'C99','Game atlas · '+n,[layers],marks,notes='Exact atlas crop at 4 raster pixels per art pixel; source resolution, not game scale.')
atlas=Image.open(root/'art/in-game/troopers-atlas.png').convert('RGBA')
for n,(first,count) in {'walk':(0,4),'idle':(4,3),'jump':(7,3),'knocked':(10,3),'swim':(13,2),'torso':(15,1)}.items():
 frames=[]
 for i in range(first,first+count):
  frames.append({k:atlas.crop((i*114,row*158,(i+1)*114,(row+1)*158)) for row,k in enumerate(['body','trim','emis'])})
 add('game-trooper-'+n,'T01','Game trooper · '+n,frames,notes='Exact live-game atlas frames, registered 114×158 crop.')
for p in sorted((root/'art/shared').glob('*.png')):
 add('reference-'+p.stem,'C99','Reference · '+p.stem,[{'body':Image.open(p).convert('RGBA')}],notes='Original reference image, source resolution.')
(root/'art/lab/hosted/assets.json').write_text(json.dumps({'schema':1,'entries':entries},indent=2)+'\n')
print(len(entries),'catalog assets')
