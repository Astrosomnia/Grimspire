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
        # put the active trooper's sentry next to the nearest enemy, then end the turn
        await pg.evaluate("""()=>{const G=window.__G,S=G.S,t=S.active,e=G.troopers.filter(o=>o.team!==t.team).sort((a,b)=>Math.abs(a.x-t.x)-Math.abs(b.x-t.x))[0];
          t.x=e.x-120;t.y=G.surfY?G.surfY(t.x):t.y;t.face=1;S.ammo[S.team].sentry=1;G.selectWeapon('sentry');S.armed=true;G.tryFire()}""")
        await pg.wait_for_timeout(5000)
        for i in range(4):
            await pg.screenshot(path=f"shots/sent{i}.png");await pg.wait_for_timeout(900)
        print(errs[:3], await pg.evaluate("()=>window.__G.sentries.map(q=>q.ammo+' q'+q.queue.length)"))
        await b.close()
asyncio.run(main())
