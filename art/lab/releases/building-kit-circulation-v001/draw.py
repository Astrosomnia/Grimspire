from native_base import *
import pathlib,base64,io
from art_check import check_doc
R=pathlib.Path(__file__).parent
old=json.load(open(R/'../building-kit-batch2/published-manifest.json'));out=[];checks=[]
for a in old:
 id=a['id']
 if id not in ('BK40','BK41','BK42','BK43','BK50a','BK50b','BK81'):continue
 w,h=a['w'],a['h'];ims=drawing(id,w,h)
 b=Plane(w,h);b.im=ims['body'];b.z=ims['height'];k=Plane(w,h);k.im=ims['back']
 note=''
 if id in ('BK40','BK41','BK42'):
  # Diagonal solid flight behind the horizontal treads: no point-only contacts.
  flight=Plane(w,h)
  for x in range(w):
   if id=='BK41' and 48<=x<80:continue
   if id=='BK40':
    spans=[(112-16*(x//32),144-x/2),(16*(x//32),24+x/2)]
   else:spans=[(112-16*(x//16),148-x)]
   for top,bottom in spans:
    flight.rect(x,top,1,round(bottom)-top,4,144)
    flight.rect(x,round(bottom)-9,1,4,3,104)
  # Horizontal tread caps remain legible, with the stringer continuous below.
  for x in range(0,128,32 if id=='BK40' else 16):
   if id=='BK41' and 48<=x<80:continue
   ys=[112-16*(x//32),16*(x//32)] if id=='BK40' else [112-x]
   for y in ys:flight.band(x,y,32 if id=='BK40' else 16,8)
  if id=='BK40':flight.band(112,64,16,16)
  b=flight
  note='Solid diagonal stringer joins all treads in each flight. About20 perpendicular thickness (28 vertical for45degree flight;24 for shallow switchback). BK41 retains full32-wide break x48..80. Tread caps remain horizontal.'
 elif id=='BK43':
  k=Plane(w,h)
  k.rect(58,0,12,128,3,112);k.rect(61,0,6,128,2,88)
  # One full turn over128px. Four broad wrapping fans perhalfturn.
  for y in range(0,128,16):
   phase=(y//16)%8
   if phase<4:
    tip=8+phase*10
    k.poly([(tip,y+8),(58,y),(70,y+5),(tip+10,y+16)],2,96)
    k.line([(tip,y+8),(58,y),(70,y+5)],3,128,3)
   else:
    tip=120-(phase-4)*10
    k.poly([(58,y+5),(70,y),(tip,y+8),(tip-10,y+16)],2,96)
    k.line([(58,y+5),(70,y),(tip,y+8)],3,128,3)
  for y in (24,88):k.rect(54,y,20,6,3,128)
  note='Spiral is entirely Back: central newel and eight broad wrapping tread fans, repeating128high. Body ledges remain exactly left16x16 at112 and right16x16 at48.'
 elif id.startswith('BK50'):
  # Native rows of overlapping roof tiles, all inside the16px roof band.
  b=Plane(w,h)
  for x in range(w):
   y=round((h-16)*(1-x/(w-1)))
   b.rect(x,y,1,16,4,144)
   b.rect(x,y+2,1,4,5,168)
   b.rect(x,y+8,1,3,3,104)
   b.rect(x,y+13,1,3,4,160)
   if x%24 in (10,11):b.rect(x,y+1,1,7,3,112)
   if x%24 in (22,23):b.rect(x,y+8,1,5,3,112)
  b.rect(0,h-14,6,14,5,168);b.rect(2,h-10,2,6,3,104)
  note='Roof tiles in two staggered rows, recessed fascia channel and low-end drip return; all within original16thick slope envelope. Flat material tones, no baked directional lighting.'
 elif id=='BK81':
  # Preserve post appearance but remove every end post pixel from Body collision.
  arr=np.array(b.im);post=np.zeros((h,w),bool);post[24:112,:12]=True;post[24:112,116:]=True
  ka=np.array(k.im);ka[post]=arr[post];k.im=Image.fromarray(ka)
  arr[post]=0;b.im=Image.fromarray(arr);za=np.array(b.z);za[post]=0;b.z=Image.fromarray(za)
  note='Side posts moved from Body to Back at both ends y24..112. Roof/deck remain Body; entire end corridor y28..112 is clear, including tiled joints. Original rear brace retained.'
 # Rebuild coarse Guts from the revised structural mask.
 ba=np.array(b.im);g=np.zeros_like(ba);yy,xx=np.indices((h,w))
 for t in (3,4):g[(ba[...,3]>0)&(3+(xx//32+yy//24)%2==t)]=PAL[t]+(255,)
 ims.update(body=b.im,height=b.z,guts=Image.fromarray(g),back=k.im)
 d=json.load(open(R/'../building-kit-batch2'/a['file']))
 def url(im):
  f=io.BytesIO();im.save(f,format='PNG');return 'data:image/png;base64,'+base64.b64encode(f.getvalue()).decode()
 fr={ly:None for ly in ('body','back','height','guts','emis','trim','cloth')}
 for ly,im in ims.items():
  if ly=='body' or im.getbbox():fr[ly]=url(im);im.save(R/(id+'-'+ly+'.png'))
 d['frames']=[fr];d['notes']='Native-grid revision from Claude building-lab review,17 Nov2026. '+note+' Same family and variant letter; previous saved version retained in Forge history. Draft, readyfalse. Not game-tested or approved.'
 fn=id+'.forge.json';json.dump(d,open(R/fn,'w'),indent=2)
 out.append(dict(a,file=fn));checks.append(dict(id=id,**check_doc(d)))
json.dump(out,open(R/'manifest.json','w'),indent=2);json.dump(checks,open(R/'art-checks.json','w'),indent=2)
for c in checks:print(c)
