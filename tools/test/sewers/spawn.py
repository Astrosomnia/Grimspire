import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page()
        await pg.goto("http://localhost:8791/sew.html",wait_until="domcontentloaded"); await pg.wait_for_timeout(2000)
        r=await pg.evaluate("""()=>{const G=window.__G;let maps=0,inside=0,total=0;for(let s=1;s<=40;s++){G.newGame('hot',s,G.mkCfg('hot',[0,1,2,3]));const w=__E('NS.sewers.find(x=>x.x0!==undefined)');if(!w)continue;maps++;
          for(const t of __E('troopers')){total++;if(t.x>Math.min(w.x0,w.cliff??w.x0)&&t.x<Math.max(w.x1,w.cliff??w.x1)&&t.y>w.cy-4&&t.y<=w.fy+2)inside++}}return {maps,total,inside}}""")
        print(r); await b.close()
asyncio.run(main())
