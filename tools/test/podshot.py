import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch();pg=await (await b.new_context(viewport={"width":1280,"height":720})).new_page()
        pg.on("pageerror",lambda e:print("PAGEERROR",e))
        await pg.goto("file:///home/claude/work/grimspire.html");await pg.wait_for_timeout(1000)
        await pg.evaluate("()=>{const G=window.__G;G.newGame('hot',1234,G.mkCfg('hot',[0,1]));}")
        await pg.add_style_tag(content='#desk{display:none!important}')
        for _ in range(40):
            ph=await pg.evaluate("()=>window.__G.S.phase")
            if ph=='aim':break
            await pg.wait_for_timeout(300)
        await pg.evaluate("()=>{const G=window.__G,S=G.S;S.ammo[S.team].pod=1;G.selectWeapon('pod');S.active.aim=-1.15;S.armed=true;G.tryFire()}")
        for i,ms in enumerate([300,900,900,700,400,250,600,700]):
            await pg.wait_for_timeout(ms);await pg.screenshot(path=f"shots/pod{i}.png")
        await b.close()
asyncio.run(main())
