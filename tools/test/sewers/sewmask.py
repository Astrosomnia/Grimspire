import asyncio,base64
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page()
        await pg.goto("http://localhost:8791/sew.html",wait_until="domcontentloaded"); await pg.wait_for_timeout(2000)
        u=await pg.evaluate("""()=>{const G=window.__G;G.newGame('hot',28,G.mkCfg('hot',[0,1]));return __E(`(()=>{const x0=250,y0=560,w=800,h=320,c=mk(w,h),g=c.getContext('2d'),im=g.createImageData(w,h);
          for(let y=0;y<h;y++)for(let x=0;x<w;x++){const v=solid[(y+y0)*W+x+x0]?190:25,i=(y*w+x)*4;im.data[i]=v;im.data[i+1]=v;im.data[i+2]=v;im.data[i+3]=255}g.putImageData(im,0,0);
          g.fillStyle='#f0f';for(const [x,y] of [[446,683],[648,720]])g.fillRect(x-x0-2,y-y0-24,4,24);
          g.strokeStyle='#0f0';for(const p of SPS.pieces)g.strokeRect(p.x0-x0,p.y0-y0,p.x1-p.x0,p.y1-p.y0);return c.toDataURL()})()`)}""")
        open('t/sewmask.png','wb').write(base64.b64decode(u.split(',')[1])); await b.close()
asyncio.run(main())
