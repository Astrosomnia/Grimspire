import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        for name,vp,mob in [("desk",{"width":1280,"height":720},False),("phone",{"width":844,"height":390},True)]:
            pg=await (await b.new_context(viewport=vp,device_scale_factor=2 if mob else 1,is_mobile=mob,has_touch=mob)).new_page()
            pg.on("pageerror",lambda e:print("PAGEERROR",e))
            await pg.goto("file:///home/claude/work/grimspire.html");await pg.wait_for_timeout(1200)
            await pg.evaluate("()=>{const G=window.__G;G.newGame('hot',9001,G.mkCfg('hot',[0,1]));}")
            await pg.wait_for_timeout(9000)
            foc="()=>{const G=window.__G,S=G.S,t=G.troopers[2];S.camFree=true;S.zoom=2;const b=G.base()*2;G.camSet(t.x-innerWidth/2/b,t.y-12-innerHeight/2/b)}"
            for _ in range(6): await pg.evaluate(foc); await pg.wait_for_timeout(50)
            await pg.screenshot(path=f"shots/e-{name}-calm.png")
            await pg.evaluate("()=>{const G=window.__G,t=G.troopers[2];G.explode(t.x+60,t.y-30,30,0)}")
            await pg.wait_for_timeout(60)
            for _ in range(2): await pg.evaluate(foc); await pg.wait_for_timeout(30)
            await pg.screenshot(path=f"shots/e-{name}-blast.png")
        await b.close()
asyncio.run(main())
