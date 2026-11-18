from draw import *
from art_check import check_doc
report=[]
for a in json.load(open(R/'manifest.json')):
 d=json.load(open(R/a['file']));b=im(d);ba=np.array(b);h=im(d,'height');ha=np.array(h)
 assert d['game_scale']==1 and not d['ready']
 assert np.array_equal(ha,np.array(compute(b,None)))
 assert np.array_equal(ba[...,3],ha[...,3]);assert np.array_equal(ba[...,3],np.array(im(d,'guts'))[...,3])
 for k,v in d['frames'][0].items():
  if v:
   ar=np.array(im(d,k));assert im(d,k).size==(d['w'],d['h']);assert k=='emis' or np.isin(ar[...,3],[0,255]).all()
 if a['code'].startswith('K'):
  prev=load('K10-live' if a['code']=='K10' else 'K11-original');assert np.array_equal(ba[...,3],np.array(im(prev))[...,3])
  for ly in ('emis','back'):assert d['frames'][0].get(ly)==prev['frames'][0].get(ly)
 c=check_doc(d);assert c['verdict']=='pass',c
 lum=ba[ba[...,3]>0,:3].mean(1);report.append(dict(code=a['code'],**c,normalisedRange=round(float((lum.max()-lum.min())/lum.mean()*80),1)))
json.dump(dict(passed=True,checks=['native1x','binary alpha','exact computed Height with no drawn input','Body/Height/Guts alpha registration','architecture alpha/Back/Emissive preservation','readability'],assets=report),open(R/'validation.json','w'),indent=2)
print(report)
# Side-by-side at game scale, with terrain colours, original kit benchmark and50px trooper.
from PIL import ImageFont
W,H=1800,1230;canvas=Image.new('RGB',(W,H),(63,73,87));dr=ImageDraw.Draw(canvas)
fontpath='/System/Library/Fonts/Helvetica.ttc';font=ImageFont.truetype(fontpath,17);small=ImageFont.truetype(fontpath,13)
dr.text((20,15),'18 NOV · LIVE-ASSET REDRAW DRAFTS · native 1x / computed Heights',fill=(225,230,237),font=font)
dr.text((20,42),'Before / after at 27/50 game scale. Raw colours; engine lighting and phone review still needed.',fill=(211,220,232),font=small)
for n,a in enumerate(json.load(open(R/'manifest.json'))):
 code=a['code'];new=json.load(open(R/a['file']));old=load('K10-live' if code=='K10' else code+'-original')
 ox=20+(n%2)*900;oy=110+(n//2)*450;dr.text((ox,oy),code+' · BEFORE',fill=(231,234,240),font=font);dr.text((ox+450,oy),'AFTER',fill=(231,234,240),font=font)
 for j,d in enumerate((old,new)):
  # Presentation-only resizing to the actual game scale, never used as source art.
  b=im(d);s=.54*d.get('game_scale',1);size=(round(b.width*s),round(b.height*s));b=b.resize(size,Image.Resampling.NEAREST)
  xx=ox+j*450;yy=oy+330-size[1];canvas.paste(b,(xx,yy),b)
  # Terrain swatch and one trooper-sized scale marker.
  dr.polygon([(xx,oy+330),(xx+70,oy+323),(xx+150,oy+332),(xx+300,oy+326),(xx+300,oy+354),(xx,oy+354)],fill=(35,42,52))
  dr.rectangle((xx+12,oy+299,xx+18,oy+305),fill=(142,154,168));dr.rectangle((xx+11,oy+307,xx+20,oy+318),fill=(142,154,168));dr.rectangle((xx+11,oy+318,xx+14,oy+326),fill=(142,154,168));dr.rectangle((xx+17,oy+318,xx+20,oy+326),fill=(142,154,168))
 c=next(q for q in report if q['code']==code);dr.text((ox,oy+371),f"Readability {c['verdict']} · {c['colours']} tones · detail {c['detail']} · computed Height",fill=(219,228,238),font=small)
# Benchmark strip
for name,x in [('K08-original',20),('R01-original',700)]:
 b=im(load(name));b=b.resize((round(b.width*.54),round(b.height*.54)),Image.Resampling.NEAREST);canvas.paste(b,(x,1200-b.height),b);dr.text((x,1205),name+' · reference',fill=(219,228,238),font=small)
canvas.save(R/'comparison.png')
