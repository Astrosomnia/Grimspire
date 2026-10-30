import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        for f in ['pre_w6.html','grimspire.html']:
            pg=await (await b.new_context(viewport={"width":1280,"height":720})).new_page()
            await pg.goto("file:///home/claude/work/"+f);await pg.wait_for_timeout(1000)
            await pg.evaluate("()=>{const G=window.__G;G.DROP.chance=0;G.newGame('hot',1234,G.mkCfg('hot',[0,1]));}")
            await pg.add_style_tag(content='#desk,#hud,#recenter{display:none!important}')
            for _ in range(60):
                if await pg.evaluate("()=>window.__G.S.phase==='aim'"):break
                await pg.wait_for_timeout(250)
            await pg.evaluate("()=>{const G=window.__G,S=G.S;S.ammo[S.team].pod=1;G.selectWeapon('pod');S.active.aim=-1.15;S.armed=true;G.tryFire()}")
            fol="()=>{const G=window.__G,S=G.S,p=S.pod;if(!p)return 0;S.camFree=true;S.zoom=2.4;const b=G.base()*2.4;G.camSet(p.x-innerWidth/2/b,p.y-innerHeight/2/b);return p.landed?2:1}"
            got={1:False,2:False}
            for i in range(300):
                st=await pg.evaluate(fol)
                if st==1 and not got[1] and i>25:
                    await pg.screenshot(path=f"shots/psz_{f[:3]}_fly.png",clip={"x":490,"y":210,"width":300,"height":300});got[1]=True
                if st==2 and not got[2]:
                    for _ in range(4): await pg.evaluate(fol);await pg.wait_for_timeout(40)
                    await pg.screenshot(path=f"shots/psz_{f[:3]}_land.png",clip={"x":490,"y":210,"width":300,"height":300});got[2]=True;break
                await pg.wait_for_timeout(30)
            print(f,got)
        await b.close()
asyncio.run(main())
