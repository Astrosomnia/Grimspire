import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch();pg=await (await b.new_context(viewport={"width":1280,"height":720})).new_page()
        errs=[];pg.on("pageerror",lambda e:errs.append(str(e)))
        await pg.goto("file:///home/claude/work/grimspire.html");await pg.wait_for_timeout(1000)
        await pg.evaluate("()=>{const G=window.__G;G.DROP.chance=0;G.newGame('hot',9001,G.mkCfg('hot',[0,1]));}")
        await pg.add_style_tag(content='#desk,#hud,#recenter{display:none!important}')
        await pg.wait_for_timeout(8000)
        foc="(i)=>{const G=window.__G,S=G.S,t=G.troopers[i];S.camFree=true;S.zoom=3.2;const b=G.base()*3.2;G.camSet(t.x-innerWidth/2/b,t.y-12-innerHeight/2/b)}"
        print(await pg.evaluate("()=>[window.__G.S.phase,window.__G.troopers.map(t=>[Math.round(t.x),Math.round(t.y),t.alive])]"))
        for i,t in enumerate([2,0]):
            for _ in range(25): await pg.evaluate(foc,t);await pg.wait_for_timeout(40)
            await pg.screenshot(path=f"shots/wrim{i}.png")
        await pg.evaluate("()=>{const G=window.__G;G.kill(G.troopers[5])}")
        await pg.wait_for_timeout(4500)
        await pg.wait_for_timeout(2500)
        gf="()=>{const G=window.__G,S=G.S,g=G.graves[0];if(!g)return null;S.camFree=true;S.zoom=3.2;const b=G.base()*3.2;G.camSet(g.x-innerWidth/2/b,g.y-14-innerHeight/2/b);return [Math.round(g.x),Math.round(g.y),g.bx]}"
        for _ in range(15): info=await pg.evaluate(gf);await pg.wait_for_timeout(40)
        print('grave',info)
        await pg.screenshot(path="shots/grave.png",clip={"x":490,"y":210,"width":300,"height":300});await pg.wait_for_timeout(400)
        for _ in range(3): await pg.evaluate(gf);await pg.wait_for_timeout(30)
        await pg.screenshot(path="shots/grave2.png",clip={"x":490,"y":210,"width":300,"height":300})
        print(errs[:3]);await b.close()
asyncio.run(main())
