import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        o=[]
        for f in ['pre_w8.html','grimspire.html']:
            pg=await (await b.new_context(viewport={"width":1280,"height":720})).new_page();errs=[];pg.on("pageerror",lambda e:errs.append(str(e)))
            await pg.goto("file:///home/claude/work/"+f);await pg.wait_for_timeout(1000)
            await pg.evaluate("()=>{const G=window.__G,S=G.S;G.DROP.chance=0;G.newGame('hot',777,G.mkCfg('hot',[0,1]));}")
            await pg.add_style_tag(content='#desk,#hud,#recenter{display:none!important}')
            for _ in range(60):
                if await pg.evaluate("()=>window.__G.S.phase==='aim'"):break
                await pg.wait_for_timeout(250)
            await pg.evaluate("""()=>{const G=window.__G,S=G.S;G.testFlat(500,1500,600);const t=S.active;for(const o of G.troopers){o.x=100+G.troopers.indexOf(o)*12;o.y=200}
              t.x=800;t.y=600;t.face=1;t.aim=-.05;t.air=false;const fo=G.troopers.filter(o=>o.team!==t.team);fo.slice(0,3).forEach((o,i)=>{o.x=880+i*24;o.y=600;o.air=false;o.vx=o.vy=0});
              S.ammo[S.team].flamer=2;G.selectWeapon('flamer');S.armed=true;G.tryFire();S.camFree=true;S.zoom=2;const b=G.base()*2;G.camSet(870-innerWidth/2/b,560-innerHeight/2/b)}""")
            await pg.wait_for_timeout(900)
            await pg.evaluate("()=>{const G=window.__G,S=G.S;S.camFree=true;S.zoom=2;const b=G.base()*2;G.camSet(870-innerWidth/2/b,560-innerHeight/2/b)}")
            await pg.screenshot(path=f"shots/flame_{f[:3]}.png",clip={"x":240,"y":160,"width":800,"height":400});print(f,errs[:2])
        await b.close()
asyncio.run(main())
