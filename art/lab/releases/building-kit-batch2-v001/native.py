"""Native-grid drawings. No source raster is read, resized or sampled.
Generated studies inform composition only. All contours, carving and depth
are placed in final art coordinates, with unlit flat material fills.
"""
from PIL import Image, ImageDraw
import numpy as np
import json, math, os
ROOT=os.path.dirname(__file__)
PAL=[(12,17,24),(16,21,29),(20,26,34),(24,30,39),(28,34,43),(31,38,47),(35,42,52),(39,47,57),(44,52,63),(49,58,70),(53,63,76),(58,68,82)]
class Plane:
    def __init__(self,w,h):
        self.w,self.h=w,h
        self.im=Image.new('RGBA',(w,h)); self.z=Image.new('RGBA',(w,h))
        self.clip=None
    def paint(self,kind,coords,t=4,z=128,width=1):
        mask=Image.new('L',(self.w,self.h)); d=ImageDraw.Draw(mask)
        if kind=='rect':
            x,y,w,h=coords
            if w<=0 or h<=0:return
            d.rectangle((round(x),round(y),round(x+w)-1,round(y+h)-1),fill=255)
        elif kind=='poly':d.polygon([(round(x),round(y)) for x,y in coords],fill=255)
        elif kind=='line':d.line([(round(x),round(y)) for x,y in coords],fill=255,width=width)
        elif kind=='oval':d.ellipse(tuple(round(v) for v in coords),fill=255)
        if self.clip is not None:mask=Image.fromarray(np.minimum(np.array(mask),self.clip))
        self.im.paste(PAL[t]+(255,) if t>=0 else (0,0,0,0),(0,0),mask)
        self.z.paste((z,z,z,255) if t>=0 else (0,0,0,0),(0,0),mask)
    def rect(self,x,y,w,h,t=4,z=128):self.paint('rect',(x,y,w,h),t,z)
    def poly(self,pts,t=4,z=128):self.paint('poly',pts,t,z)
    def line(self,pts,t=4,z=128,width=2):self.paint('line',pts,t,z,width)
    def oval(self,box,t=4,z=128):self.paint('oval',box,t,z)
    def freeze(self):self.clip=np.array(self.im)[...,3]
    def unclip(self):self.clip=None
    def band(self,x,y,w,h=16):
        self.rect(x,y,w,h,4,152)
        # A centred fascia channel; no bright top/shadowed bottom pair.
        if h>=12:self.rect(x,y+5,w,h-10,3,112)
        for xx in range(int(x)+32,int(x+w)-2,48):self.rect(xx,y+2,2,h-4,3,120)
    def panel(self,x,y,w,h):
        self.rect(x,y,w,h,5,176);self.rect(x+2,y+2,w-4,h-4,3,104)
        self.rect(x+4,y+4,w-8,h-8,4,120)
    def pointed(self,x,y,w,h,t=4,z=128):
        # Polygonal pointed arch with broad stepped shoulders.
        self.poly([(x,y+h),(x,y+h*.46),(x+w*.12,y+h*.26),(x+w*.3,y+h*.12),(x+w*.5,y),(x+w*.7,y+h*.12),(x+w*.88,y+h*.26),(x+w,y+h*.46),(x+w,y+h)],t,z)
    def niche(self,x,y,w,h):
        self.pointed(x,y,w,h,5,168);self.pointed(x+3,y+5,w-6,h-8,2,88)
        if w>=24:self.pointed(x+6,y+10,w-12,h-16,3,104)
    def quatre(self,cx,cy,r):
        self.poly([(cx,cy-r-3),(cx+r+3,cy),(cx,cy+r+3),(cx-r-3,cy)],5,168)
        for dx,dy in ((-r/2,0),(r/2,0),(0,-r/2),(0,r/2)):
            self.oval((cx+dx-r/2,cy+dy-r/2,cx+dx+r/2,cy+dy+r/2),2,88)
    def pier(self,x,y,w,h,carve=True):
        self.rect(x+3,y,w-6,h,4,144)
        self.rect(x+6,y+12,w-12,h-24,3,112)
        self.rect(x,y,w,8,5,176);self.rect(x+2,y+8,w-4,4,4,152)
        self.rect(x,y+h-8,w,8,5,176);self.rect(x+2,y+h-12,w-4,4,4,152)
        if carve and w>=20 and h>=64:self.niche(x+5,y+20,w-10,min(h-42,56))

def drawing(id,w,h):
    b,k=Plane(w,h),Plane(w,h); em=Image.new('RGBA',(w,h));c=int(id[2:4])
    def courses(p,step=32,t=3):
        p.freeze()
        for y in range(step,h,step):
            p.rect(0,y,w,2,t,112)
            # Quiet half-bay stagger, no mortar on every 16px course.
            for x in range(32 if (y//step)%2 else 64,w,64):p.rect(x,y-step+4,2,step-8,t,112)
        p.unclip()
    def slope(top,th=16,breaks=None):
        for x in range(w):
            if breaks and breaks[0]<=x<breaks[1]:continue
            y=round(top(x));b.rect(x,y,1,th,4,152)
            b.rect(x,y+5,1,max(1,th-10),3,112)
            if x%32 in (14,15):b.rect(x,y+2,1,th-4,3,120)
    if c in (40,41,42):
        if c==40:
            for x in range(0,128,32):b.band(x,112-16*(x//32),32);b.band(x,16*(x//32),32)
            b.band(112,64,16)
            for x,y in ((0,96),(0,0),(112,48)):k.rect(x,y,16,24,2,96)
        else:
            for x in range(0,128,16):
                if c==41 and 48<=x<80:continue
                y=112-x;b.band(x,y,16,20);b.panel(x+3,y+6,10,10)
            if c==42:
                for x in (8,48,88):
                    y=128-x;k.poly([(x,y),(x+28,y-28),(x+28,y+12),(x+8,y+24)],2,80)
                    k.poly([(x+7,y+3),(x+22,y-12),(x+22,y+8)],1,64)
    elif c==43:
        k.rect(58,0,12,128,2,96);k.rect(61,0,6,128,3,112)
        for n in range(8):
            y=n*16;left=4 if n%4<2 else 64
            k.poly([(left,y+8),(left+56,y),(left+56,y+8),(left,y+16)],2,96)
            k.line([(left,y+11),(left+56,y+3)],3,112,3)
        b.band(0,112,16);b.band(112,48,16)
    elif c==44:
        b.rect(0,0,4,16,4,152);b.rect(28,0,4,16,4,152)
        k.poly([(4,12),(8,0),(12,0),(8,12)],2,96)
    elif c in (50,75,95) and id!='BK95pier':
        if c==50:top=lambda x:(h-16)*(1-x/(w-1))
        elif c==75:top=lambda x:12*math.sin(math.pi*x/(w-1))
        else:top=lambda x:48*x/(w-1)-8*math.sin(math.pi*x/(w-1))
        slope(top)
    elif c in (51,52):
        centre=(w-1)/2;top=lambda x:round(abs(x-centre)/centre*(h-4))
        b.poly([(0,h-1),(round(centre),0),(w-1,h-1)],4,120);b.freeze()
        # Two symmetric coping mouldings, relief entirely in depth.
        for x in range(w):
            y=top(x);b.rect(x,y,1,6,5,184);b.rect(x,y+6,1,3,3,100)
            b.rect(x,y+10,1,3,5,160)
        b.band(0,h-10,w,10)
        nw=24 if w==128 else 56 if w==256 else 84
        nh=h-25 if w==128 else h-42
        b.niche((w-nw)//2,h-10-nh,nw,nh)
        if w>=256:
            for x in (w/2-nw/2-14,w/2+nw/2+2):b.pier(x,h-nh-8,12,nh-2,False)
            b.quatre(w/2,19,6 if w==256 else 9)
            for side in (-1,1):
                xx=w/2+side*(nw/2+25)
                pts=[(xx,h-20),(xx,h*.55),(w/2+side*(w/2-38),h-20)]
                b.poly(pts,3,100);b.line(pts+[pts[0]],5,160,3)
        else:b.quatre(w/2,h-25,4)
        b.unclip()
        if c==52:
            gap=(56,104) if w==128 else (128,192)
            b.rect(gap[0],0,gap[1]-gap[0],h,-1)
            # Three large broken shoulders, not tiny rubble chips.
            b.poly([(gap[0]-10,0),(gap[0]-2,h*.48),(gap[0]-8,h*.62),(gap[0],h*.75),(gap[0],0)],-1)
    elif c==53:
        b.poly([(0,62),(8,48),(24,30),(44,20),(56,16),(72,16),(90,22),(106,34),(120,50),(127,62)],4,128)
        b.freeze()
        for x in (24,64,104):
            pts=[(64,18),((x+64)//2,30),(x,60)]
            b.line(pts,3,96,9);b.line(pts,5,176,5)
        b.rect(8,44,112,2,3,112);b.unclip()
        b.rect(55,8,18,14,4,152);b.rect(51,4,26,6,5,184);b.rect(58,0,12,4,4,160)
        b.band(0,60,128,12)
        for x in (4,112):b.pier(x,72,12,32,False)
        for x in (40,76):k.pier(x,72,12,32,False)
        k.rect(10,72,108,4,2,96)
        b.band(0,96,128,8)
    elif c==54:
        slope(lambda x:abs(x-63.5)/63.5*16)
        b.pier(0,20,16,92,False);b.pier(112,20,16,92,False);b.band(0,112,128)
        # Bell behind the traversable bay.
        k.rect(61,28,6,20,2,96);k.poly([(52,48),(76,48),(80,72),(88,80),(40,80),(48,72)],2,112)
        k.rect(40,78,48,5,3,144);k.oval((60,80,67,88),2,112);k.rect(54,53,20,3,3,144)
    elif c==55:
        b.band(0,16,128);b.rect(0,4,128,12,4,144);b.rect(0,7,128,4,3,104)
        for x in (25,89):
            b.poly([(x,2),(x+14,2),(x+18,7),(x+16,20),(x+8,25),(x,20),(x-2,7)],5,184)
            b.rect(x+3,8,10,4,2,88);b.rect(x+5,16,6,6,2,80)
    elif c in (60,61):
        b.rect(0,0,24,128,4,144);b.freeze();b.rect(5,14,14,96,3,112)
        for y in (0,16,96,112):b.band(0,y,24,16)
        b.unclip()
        if c==60:
            b.rect(0,26,24,56,-1);b.band(24,82,40)
            b.poly([(24,98),(56,98),(24,120)],4,152)
            b.poly([(28,101),(44,101),(28,112)],3,96)
        else:b.rect(0,76,24,12,-1)
    elif c==62:
        b.rect(0,0,128,128,4,128);b.freeze();b.band(0,0,128,12)
        b.pointed(12,14,104,98,5,184);b.pointed(17,20,94,92,3,104)
        b.pointed(20,24,88,88,5,160)
        for x in (0,112):b.pier(x,16,16,96,False)
        b.quatre(64,12,5);b.band(0,112,128)
        b.unclip()
        # Contract opening exactly: 80 wide, pointed crown y28, floor y112.
        for x in range(24,104):
            y=math.ceil(28+abs(x-63.5)*.6);b.rect(x,y,1,112-y,-1)
    elif c==63:
        blocks=h//16
        for y in range(h):b.rect(0,y,math.ceil(8+32*(y//16)/(blocks-1)),1,4,144)
        b.freeze();b.rect(2,8,3,h-16,3,104)
        for y in range(32,h,64):
            b.rect(0,y,40,6,5,176)
            edge=8+32*(y//16)/(blocks-1)
            if edge>18:b.niche(7,y+14,edge-10,32)
        b.band(0,h-12,40,12);b.unclip()
    elif c==64:
        slope(lambda x:x/w*24)
        k.rect(0,28,36,84,2,88);k.rect(6,40,22,64,1,64)
        b.rect(36,24,12,88,4,152);b.rect(36,26,12,56,-1)
        b.poly([(0,112),(47,112),(16,127),(0,127)],4,152)
        b.line([(0,119),(30,119)],3,104,3)
    elif c==65:
        b.band(0,0,128)
        for x in (0,52,104):
            b.poly([(x,16),(x+23,16),(x+20,30),(x+14,36),(x+14,48),(x+6,60),(x,64)],4,144)
            b.poly([(x+4,21),(x+17,21),(x+12,33),(x+4,40)],3,96)
            b.rect(x,16,24,5,5,176)
    elif c in (70,71,72,9,10,11):
        k.rect(0,0,w,h,2,80);courses(k,32,1)
        if c==70:
            k.oval((27,13,100,86),3,104);b.oval((32,18,95,81),3,72)
            # Chunky solid glass panes, one stone ring and eight spokes.
            b.oval((36,22,91,77),2,64)
            ImageDraw.Draw(em).ellipse((38,24,89,75),fill=(42,66,78,255))
            b.freeze()
            for a in range(0,360,45):
                r=math.radians(a);b.line([(64,50),(64+32*math.cos(r),50+32*math.sin(r))],4,152,4)
            b.oval((56,42,71,57),4,152);b.unclip()
            ea=np.array(em);za=np.array(b.z);ea[za[...,0]!=64]=0;em=Image.fromarray(ea)
        elif c==71:
            # Two quiet niches, two shelves, only four broad objects.
            for x in (18,76):
                k.pointed(x,18,34,80,3,96);k.pointed(x+4,24,26,70,1,56)
                for y in (58,90):k.rect(x, y,34,4,2,80)
            k.rect(24,40,9,18,2,72);k.rect(36,44,8,14,2,72)
            k.oval((84,73,100,89),2,72);k.rect(89,68,6,8,2,72)
        elif c==72:
            k.poly([(28,0),(110,0),(104,20),(115,32),(99,48),(108,70),(88,94),(42,106),(22,88),(32,72),(20,60),(34,34)],-1)
            for x,y,ww,hh in ((12,112,30,16),(44,104,34,24),(84,116,28,12)):
                k.poly([(x,y+4),(x+ww-8,y),(x+ww,y+hh),(x,y+hh)],2,88)
        elif c==9:
            if id.endswith('b'):k.rect(0,62,w,4,3,96);k.rect(54,48,20,24,2,88)
            else:k.rect(52,28,24,4,3,96)
        elif c==10:
            # Exactly preserve original required cutout below in back revision script.
            k.pointed(44,16,40,70,3,96);k.pointed(48,20,32,62,-1)
        elif c==11:
            for x in (10,70):k.pointed(x,24,48,104,-1)
    elif c==73:
        b.poly([(0,6),(10,2),(18,4),(20,8),(76,8),(78,0),(92,2),(95,20),(80,23),(74,18),(20,18),(16,23),(0,20)],4,144)
        b.freeze();b.rect(18,11,60,4,3,104);b.rect(6,4,6,18,5,176);b.rect(82,2,6,20,5,176)
        b.line([(52,8),(46,13),(50,18)],2,80,3);b.unclip()
    elif c==74:
        b.pier(0,0,24,128)
        for x in range(w):b.rect(x,math.ceil(52+x*.5),1,6,-1)
    elif id in ('BK80plank','BK90deck','BK92slab','BK93','BK96deck','BK97platform'):
        b.band(0,0,w,h)
        if h<=8:b.rect(0,2,w,2,3,112)
        if id=='BK90deck':b.rect(12,2,8,h-4,5,168);b.rect(14,5,4,6,3,112)
        if id=='BK93':b.rect(8,6,40,4,3,96)
    elif id in ('BK80post','BK95pier'):
        b.pier(0,0,w,h)
        if id=='BK80post':b.rect(0,16,w,8,5,176)
    elif id=='BK80rope':
        for x in range(w):k.rect(x,round(12*math.sin(math.pi*x/(w-1))),1,4,2,96)
    elif c==81:
        slope(lambda x:abs(x-63.5)/63.5*8)
        b.rect(0,16,12,96,4,144);b.rect(116,16,12,96,4,144);b.band(0,112,128)
        k.line([(8,104),(120,32)],2,96,6)
        for x in (0,116):b.rect(x+4,24,4,80,3,96)
    elif id=='BK90brace':
        b.rect(0,0,8,64,4,144);b.rect(0,0,64,8,4,144);b.line([(4,60),(60,4)],4,144,8)
        b.rect(0,48,12,16,5,176);b.rect(48,0,16,12,5,176)
        for x,y in ((4,52),(52,4)):b.rect(x,y,4,4,3,112)
    elif id=='BK90lamp':
        k.rect(6,18,4,26,2,104);k.rect(3,44,10,4,3,144)
        k.poly([(3,6),(8,0),(12,6),(12,20),(3,20)],3,128)
        b.rect(5,7,5,10,3,64);ImageDraw.Draw(em).rectangle((5,7,9,16),fill=(98,94,76,255))
        k.rect(2,5,12,3,3,144);k.rect(2,18,12,3,3,144)
    elif c==91:
        b.poly([(0,0),(31,0),(26,5),(30,9),(22,12),(25,16),(14,16),(10,24),(8,16),(0,16)],4,144)
        b.freeze();b.rect(0,5,32,6,3,104);b.unclip()
    elif id=='BK92bracket':
        b.poly([(0,0),(35,0),(35,8),(28,8),(28,14),(20,14),(20,22),(12,22),(12,31),(0,31)],4,144)
        b.poly([(4,9),(23,9),(14,18),(4,25)],3,96);b.rect(0,0,36,5,5,176)
    elif c==94:
        for x in range(w):
            outer=58-math.sqrt(max(0,58*58-x*x));inner=58-math.sqrt(max(0,44*44-x*x)) if x<44 else 58
            b.rect(x,math.ceil(outer),1,math.ceil(inner)-math.ceil(outer),4,160)
            if x<44:k.rect(x,math.ceil(inner),1,122-math.ceil(inner),2,80)
        b.rect(44,58,14,64,4,152);b.rect(0,122,58,58,4,136)
        b.freeze()
        for x in range(w):
            outer=58-math.sqrt(max(0,58*58-x*x));b.rect(x,math.ceil(outer)+5,1,3,3,104)
        b.rect(48,58,5,64,3,112);b.band(0,122,58,12)
        b.rect(0,152,58,2,3,104);b.rect(28,138,2,14,3,104)
        b.unclip();b.rect(42,52,16,40,-1)
    elif id=='BK96post':
        k.rect(3,0,6,128,2,104)
        for y in (28,92):k.rect(0,y,12,8,3,144)
    elif id=='BK96brace':
        k.line([(4,124),(60,4)],2,112,7)
        k.rect(0,116,12,12,3,144);k.rect(52,0,12,12,3,144)
    elif id=='BK96ladder':
        k.rect(1,0,4,128,2,96);k.rect(21,0,4,128,2,96)
        b.rect(0,0,26,6,4,160);b.rect(0,64,26,6,4,160)
    elif id=='BK97jib':
        k.rect(0,0,8,48,2,112);k.rect(0,0,80,8,2,112)
        k.line([(4,44),(72,4)],2,112,7);k.rect(0,0,12,12,3,144)
        k.oval((68,1,79,12),3,144);k.oval((72,5,75,8),1,80)
    elif id=='BK97chain':
        for y in range(0,128,16):
            k.rect(1,y,6,12,2,112);k.rect(3,y+3,2,6,-1);k.rect(3,y+10,2,8,3,128)
    elif c==98:
        k.rect(0,0,44,4,2,112)
        for x in (0,20,40):k.rect(x,4,4,22,2,104)
        b.band(0,26,44,12);b.poly([(0,38),(30,38),(0,59)],4,144)
        b.poly([(4,41),(19,41),(4,51)],3,96)
    else:raise ValueError(id)
    # Native core planes, deliberately coarser than the face carving.
    ba=np.array(b.im);g=np.zeros_like(ba)
    yy,xx=np.indices((h,w));tones=3+((xx//32+yy//24)%2)
    for t in (3,4):g[(ba[...,3]>0)&(tones==t)]=PAL[t]+(255,)
    return {'body':b.im,'back':k.im,'height':b.z,'guts':Image.fromarray(g),'emis':em}

if __name__=='__main__':
    specs=json.load(open(ROOT+'/prompts.json'))['specs']
    os.makedirs(ROOT+'/native',exist_ok=True)
    for id,w,h,*_ in specs:
        if id=='BK90lamp':h=48
        if id=='BK98':h=60
        for ly,im in drawing(id,w,h).items():im.save(f'{ROOT}/native/{id}-{ly}.png')
    print('Native grid:',len(specs),'drawings; no source resampling')
