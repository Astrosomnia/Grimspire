import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch();ctx=await b.new_context();await ctx.add_init_script("window.requestAnimationFrame=()=>0")
        for f in ['pre_w5.html','grimspire.html']:
            pg=await ctx.new_page();await pg.goto("file:///home/claude/work/"+f);await pg.wait_for_timeout(800)
            r=await pg.evaluate("""()=>{const G=window.__G,S=G.S;G.newGame('hot',1234,G.mkCfg('hot',[0,1]));const out=[];
              for(const off of[3,6,10]){const t=G.troopers[0];G.testFlat(800,1300,600);t.x=1000;t.y=600;t.vx=t.vy=0;t.air=false;t.alive=true;t.hp=100;
                // a mortar shell coming down from the left lands just past the trooper's middle
                G.explode(1000+off,598,40,0,{v:[420,380]});out.push([off,Math.round(t.vx)])}return out}""")
            print(f,'shell from the left, landing N px past centre -> trooper vx:',r);await pg.close()
        await b.close()
asyncio.run(main())
