import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch();pg=await (await b.new_context(viewport={"width":1280,"height":720})).new_page()
        errs=[];pg.on("pageerror",lambda e:errs.append(str(e)))
        await pg.goto("file:///home/claude/work/grimspire.html");await pg.wait_for_timeout(1000)
        await pg.evaluate("()=>{const G=window.__G;G.DROP.chance=0;G.newGame('hot',1234,G.mkCfg('hot',[0,1]));}")
        await pg.add_style_tag(content='#desk{display:none!important}')
        for _ in range(60):
            if await pg.evaluate("()=>window.__G.S.phase==='aim'"):break
            await pg.wait_for_timeout(250)
        await pg.evaluate("()=>{const G=window.__G,S=G.S;S.ammo[S.team].pod=1;G.selectWeapon('pod');S.active.aim=-1.15;S.armed=true;S.zoom=2;G.tryFire()}")
        times=[150,250,250,350,500,700,900,900,700,500,500,600]
        for i,ms in enumerate(times):
            await pg.wait_for_timeout(ms)
            st=await pg.evaluate("()=>{const p=window.__G.S.pod;return p?(p.stage||'')+(p.landed?'landed':'')+' t'+(p.t||0).toFixed(2):'none'}")
            await pg.screenshot(path=f"shots/pseq{i}.png");print(i,st)
        print(errs[:3]);await b.close()
asyncio.run(main())
