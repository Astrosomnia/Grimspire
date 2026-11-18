from PIL import Image,ImageDraw,ImageFilter
import numpy as np,json,pathlib,base64,io,sys,copy
R=pathlib.Path(__file__).parent
sys.path.insert(0,str(R/'python-deps'));from scipy import ndimage as nd
from bk_height import compute
PAL=[(17,22,29),(25,31,40),(35,42,52),(46,54,65),(59,67,79),(76,84,96)]
def load(code):return json.load(open(R/'references'/(code+'.forge.json')))
def im(d,k='body'):return Image.open(io.BytesIO(base64.b64decode(d['frames'][0][k].split(',')[1]))).convert('RGBA')
def url(im):
 f=io.BytesIO();im.save(f,format='PNG');return 'data:image/png;base64,'+base64.b64encode(f.getvalue()).decode()
class Art:
 def __init__(self,w,h,mask=None):self.w,self.h=w,h;self.im=Image.new('RGBA',(w,h));self.mask=mask
 def poly(self,pts,t):ImageDraw.Draw(self.im).polygon(pts,fill=PAL[t]+(255,))
 def rect(self,box,t):
  if box[2]>=box[0] and box[3]>=box[1]:ImageDraw.Draw(self.im).rectangle(box,fill=PAL[t]+(255,))
 def line(self,pts,t,width=3):ImageDraw.Draw(self.im).line(pts,fill=PAL[t]+(255,),width=width)
 def finish(self):
  a=np.array(self.im)
  if self.mask is not None:a[...,3]=self.mask
  return Image.fromarray(a)
def rock(code):
 w,h=(480,256) if code=='R10' else (448,256);a=Art(w,h)
 if code=='R10':
  outline=[(0,255),(20,221),(38,208),(48,166),(62,149),(54,120),(67,95),(63,57),(80,37),(99,8),(128,15),(147,31),(164,24),(180,42),(191,81),(214,92),(232,105),(269,112),(287,96),(310,86),(325,68),(352,61),(374,75),(385,110),(400,126),(397,155),(419,176),(428,198),(447,210),(461,238),(479,247),(479,255)]
  facets=[(2,[(0,255),(45,201),(82,203),(71,255)]),(3,[(47,168),(74,144),(104,156),(89,196),(43,214)]),(1,[(68,96),(106,79),(99,123),(72,149),(55,123)]),(4,[(65,58),(99,8),(128,15),(147,31),(110,46)]),(3,[(70,61),(109,48),(106,79),(68,96)]),(2,[(111,47),(148,33),(164,25),(178,43),(169,86),(134,105),(108,81)]),(1,[(107,81),(133,106),(118,151),(98,157),(100,121)]),(4,[(137,107),(168,87),(188,81),(213,94),(198,117),(161,134)]),(2,[(122,152),(160,136),(176,169),(153,212),(132,255),(90,255),(92,202)]),(3,[(162,134),(199,118),(229,105),(245,128),(224,150),(212,187),(175,171)]),(1,[(178,173),(212,189),(197,242),(174,255),(138,255)]),(2,[(217,189),(227,151),(247,130),(273,114),(287,130),(270,174),(277,216),(251,255),(204,255)]),(4,[(291,97),(326,69),(352,61),(374,75),(354,96),(322,104)]),(3,[(289,103),(321,107),(313,143),(281,166),(273,142)]),(2,[(324,107),(354,99),(382,111),(400,128),(383,151),(355,159),(319,144)]),(1,[(320,148),(351,163),(338,211),(321,255),(274,255),(285,215),(276,176)]),(4,[(357,162),(385,154),(417,178),(398,188),(364,185)]),(3,[(355,188),(399,191),(426,199),(447,211),(422,229),(382,221),(349,244)]),(2,[(384,225),(422,232),(458,239),(479,250),(479,255),(331,255),(352,244)])]
 else:
  outline=[(0,255),(6,220),(18,205),(16,182),(34,165),(42,141),(64,129),(79,105),(97,105),(109,84),(127,77),(145,80),(167,75),(184,83),(205,77),(225,78),(242,70),(263,73),(282,62),(300,62),(322,50),(342,53),(354,44),(369,50),(377,73),(387,87),(391,114),(408,129),(410,153),(427,169),(433,200),(444,221),(447,255)]
  facets=[(3,[(0,255),(18,205),(49,205),(62,234),(46,255)]),(2,[(20,182),(41,143),(66,130),(86,148),(70,188),(51,204),(18,205)]),(4,[(66,132),(81,106),(97,106),(109,84),(127,78),(145,81),(128,105),(103,119)]),(3,[(84,150),(105,122),(129,108),(158,119),(143,147),(114,161),(103,187),(72,190)]),(1,[(63,235),(73,193),(104,191),(117,219),(112,255),(49,255)]),(2,[(132,105),(149,83),(169,77),(185,84),(206,78),(225,79),(225,107),(192,123),(160,118)]),(4,[(193,126),(229,109),(245,74),(263,75),(283,64),(300,64),(289,88),(261,104),(243,131)]),(2,[(246,133),(264,108),(292,93),(315,108),(304,146),(277,163)]),(3,[(301,65),(323,52),(342,55),(355,46),(370,52),(378,75),(361,99),(333,111),(318,105),(295,87)]),(1,[(334,115),(360,103),(389,88),(392,116),(407,131),(385,156),(356,165),(309,147)]),(4,[(359,167),(385,158),(407,155),(425,171),(431,200),(412,210),(376,195)]),(2,[(309,151),(352,169),(372,198),(357,231),(341,255),(294,255),(298,208)]),(3,[(376,200),(411,214),(431,204),(445,225),(447,255),(349,255),(361,235)]),(1,[(110,166),(144,148),(165,125),(191,126),(206,148),(174,171),(145,197),(129,227),(112,255)])]
 a.poly(outline,1)
 mask=np.array(a.im)[...,3]
 for t,p in facets:a.poly(p,t)
 # The drawn arch opening remains a large clean portal, with irregular rock abutments.
 if code=='R11':
  ImageDraw.Draw(a.im).polygon([(118,256),(125,225),(137,207),(151,183),(173,165),(189,153),(208,149),(226,155),(243,161),(261,180),(275,192),(286,216),(293,234),(289,256)],fill=(0,0,0,0))
 # A handful of drawn fracture branches and broken facet lips, in chunky clusters.
 paths=([[(103,49),(113,61),(106,78)],[(162,137),(152,149),(155,160)],[(223,154),(239,165),(235,179)],[(323,108),(333,121),(327,135)],[(370,187),(380,200),(395,204)]] if code=='R10' else [[(106,121),(119,134),(114,147)],[(193,125),(206,112),(222,112)],[(292,94),(301,110),(296,122)],[(357,168),(370,179),(369,190)],[(65,211),(75,220),(71,232)]])
 before=np.array(a.im)[...,3].copy()
 for pts in paths:a.line(pts,1,4)
 a.mask=np.minimum(mask,before);body=a.finish();return body

def architecture(code):
 d=load('K10-live' if code=='K10' else 'K11-original');src=im(d);arr=np.array(src);mask=arr[...,3];solid=mask>128
 # Re-establish the original K08 material ramp on the native source clusters.
 u,c=np.unique(arr[solid,:3],axis=0,return_counts=True);order=np.argsort(u.mean(1));tone=np.zeros(mask.shape,int)
 for t,idx in enumerate(order):tone[(arr[...,:3]==u[idx]).all(2)]=min(5,round(t*5/max(1,len(u)-1)))
 a=Art(d['w'],d['h'],mask);base=np.zeros_like(arr)
 for t in range(6):base[solid&(tone==t)]=PAL[t]+(255,)
 a.im=Image.fromarray(base)
 if code=='K10':
  # Preserve the strong existing design; redraw broad joints and structural face lines.
  for x,y,w,h in [(245,222,42,114),(393,175,36,165),(567,159,32,181),(700,128,36,214),(614,81,20,101),(700,70,18,98)]:
   a.rect((x+5,y+8,x+w-6,y+h-8),1);a.line([(x+4,y+7),(x+4,y+h-7)],3,4);a.line([(x+w-5,y+7),(x+w-5,y+h-7)],3,4)
   for yy in range(y+30,y+h-10,32):a.line([(x+3,yy),(x+w-4,yy)],0,3)
  # Deep recessed arch joints keep the large spans readable.
  for pts in [[(281,317),(282,279),(300,245),(325,226),(348,224),(373,237),(391,265)],[(424,321),(434,274),(459,244),(493,226),(529,221),(561,230),(584,255),(602,295)]]:
   a.line(pts,0,9);a.line(pts,3,4)
  for y,x0,x1 in [(315,29,237),(345,18,749),(188,445,571),(211,601,727)]:
   a.line([(x0,y),(x1,y)],0,3)
   for x in range(x0+22,x1,46):a.line([(x,y-12),(x,y)],1,3)
 else:
  # Rebuild block interiors as articulated masonry, leaving the broken edges and openings.
  for x,y,w,h in [(20,112,65,397),(193,324,49,188),(367,434,50,80),(68,45,23,145)]:
   a.rect((x+5,y,x+w-6,y+h),2)
   a.rect((x+12,y+12,x+w-13,y+h-12),1)
   a.line([(x+8,y+4),(x+8,y+h-5)],3,4);a.line([(x+w-9,y+4),(x+w-9,y+h-5)],3,4)
   for yy in range(y+26,y+h,28):
    a.line([(x+4,yy),(x+w-5,yy)],0,3)
    if (yy-y)//28%2:a.line([(x+w//2,yy),(x+w//2,yy+24)],1,3)
  # Native arch mouldings and wide recessed reveals.
  arches=[[(80,189),(80,100),(92,77),(111,58),(131,48),(145,71),(151,102),(151,189)],[(84,271),(94,232),(114,211),(139,202),(164,210),(183,232),(195,271)],[(85,348),(101,312),(126,295),(154,293),(180,307),(195,333)],[(84,517),(86,432),(104,401),(133,379),(158,395),(181,428),(184,518)],[(242,518),(246,461),(266,433),(287,419),(311,438),(339,465),(350,518)]]
  for pts in arches:a.line(pts,0,12);a.line(pts,3,7);a.line(pts,2,3)
  # Horizontal cornices: paired channels, no directional highlight/shadow pair.
  for x0,x1,y in [(11,89,201),(8,100,278),(9,109,375),(15,83,505),(88,273,196),(92,292,279),(108,299,359)]:
   a.rect((x0,y-5,x1,y+5),3);a.line([(x0+2,y),(x1-2,y)],1,3)
   for xx in range(x0+24,x1,40):a.line([(xx,y-4),(xx,y+4)],1,3)
  # A few quiet bed joints on the exposed descending nave.
  for x,y in [(322,403),(365,428),(409,453),(451,480)]:a.line([(x,y),(x+32,y+15)],1,4)
 body=a.finish()
 # All architecture openings, glass, routes, and rear layers stay in their original positions.
 return body,d

out=[]
lib=json.load(open(R/'../live-redraw-forge/art/lab/hosted/library.json'))['entries']
for code in ('R10','R11','K10','K11'):
 if code.startswith('R'):
  body=rock(code);d=copy.deepcopy(load(code+'-original'));d['w'],d['h']=body.size;d['game_scale']=1
  # New native canvas is exactly the old .5 game footprint; marker coordinates follow it.
  for key,v in (d.get('markers') or {}).items():
   if isinstance(v,list):d['markers'][key]=[round(v[0]/2),round(v[1]/2)]
  if d.get('base') is not None:d['base']=round(d['base']/2)
  fr={k:None for k in ('body','back','height','guts','emis','trim','cloth')}
 else:
  body,d=architecture(code);fr=copy.deepcopy(d['frames'][0])
 # Exact code-computed Height, no hand-authored map input.
 height=compute(body,None)
 a=np.array(body);g=a.copy();yy,xx=np.indices(a.shape[:2]);sel=a[...,3]>0
 for t in range(2):g[sel&((xx//28+yy//20)%2==t)]=PAL[t+1]+(255,)
 fr.update(body=url(body),height=url(height),guts=url(Image.fromarray(g)))
 fr.setdefault('back',None)
 d.update(name=code+' · '+{'R10':'Terraced crag — drawn facets','R11':'Rock arch — drawn facets','K10':'Stair nave — restored recesses and linework','K11':'Belfry — articulated masonry and arches'}[code],ready=False,game_scale=1)
 d['notes']='18 Nov2026 draft redraw. References: original K01/K08 and R01–R09. Native1x art grid, no source resampling. Height computed by exact tools/bk_height.py compute(body,None); no drawn Height input. '+('New480x256 or448x256 native canvas preserves previous .5-scaled game footprint; redrawn silhouette requires collision/placement review. ' if code.startswith('R') else 'Original Body alpha, dimensions, Emissive and Back retained; structural linework and material clusters revised at native1x. ')+'Not approved or live. Jarred reviews exact version in game.'
 d['frames']=[fr];json.dump(d,open(R/(code+'.forge.json'),'w'),indent=2)
 for k in ('body','height','back'):
  if fr.get(k):(R/(code+'-'+k+'.png')).write_bytes(base64.b64decode(fr[k].split(',')[1]))
 e=next(e for e in reversed(lib) if e.get('code')==code);out.append(dict(id=code,code=code,title=d['name'],w=d['w'],h=d['h'],file=code+'.forge.json',asset_id=e['asset_id']))
json.dump(out,open(R/'manifest.json','w'),indent=2)
print('Drew4 native drafts; Heights computed with no drawn-map input')
