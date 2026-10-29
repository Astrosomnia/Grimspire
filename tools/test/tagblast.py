import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch();pg=await (await b.new_context(viewport={"width":1280,"height":720})).new_page()
        errs=[];pg.on("pageerror",lambda e:errs.append(str(e)))
        await pg.goto("file:///home/claude/work/grimspire.html");await pg.wait_for_timeout(1000)
        await pg.evaluate("()=>{const G=window.__G;G.DROP.chance=0;G.newGame('hot',1234,G.mkCfg('hot',[0,1]));}")
        await pg.add_style_tag(content='#desk,#hud,#recenter{display:none!important}')
        await pg.wait_for_timeout(8000)
        t=await pg.evaluate("()=>{const q=window.__G.dress().tags[0];return [q.x+q.w/2,q.y+q.h/2,q.w]}")
        foc=f"()=>{{const G=window.__G,S=G.S;S.camFree=true;S.zoom=2.2;const b=G.base()*2.2;G.camSet({t[0]}-innerWidth/2/b,{t[1]}-innerHeight/2/b)}}"
        for _ in range(5): await pg.evaluate(foc);await pg.wait_for_timeout(60)
        await pg.screenshot(path="shots/tag0.png")
        for k,(dx,r) in enumerate([(-30,22),(20,26)]):
            await pg.evaluate(f"()=>window.__G.explode({t[0]+dx},{t[1]-4},{r},0)")
            for _ in range(6): await pg.evaluate(foc);await pg.wait_for_timeout(50)
            await pg.screenshot(path=f"shots/tag{k+1}a.png")
            await pg.wait_for_timeout(1500)
            for _ in range(3): await pg.evaluate(foc);await pg.wait_for_timeout(50)
            await pg.screenshot(path=f"shots/tag{k+1}.png")
        print(errs[:3],await pg.evaluate("()=>window.__G.dress().tags.map(q=>q.left.toFixed(2))"))
        await b.close()
asyncio.run(main())
