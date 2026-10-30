import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        ctx=await b.new_context();await ctx.add_init_script("window.requestAnimationFrame=()=>0")
        for f in ['pre_w8.html','grimspire.html']:
            pg=await ctx.new_page();await pg.goto("file:///home/claude/work/"+f);await pg.wait_for_timeout(800)
            r=await pg.evaluate("""()=>{const G=window.__G,S=G.S;G.DROP.chance=0;G.newGame('hot',777,G.mkCfg('hot',[0,1]));G.testFlat(600,1400,600);
              G.spawnShell?0:0;const p={x:1000,y:600,vx:0,vy:0,w:G.WP.nuke,owner:G.troopers[0],age:1};
              // detonate a doomsday shell on flat ground
              G.explode(1000,600,125,0,{big:true});
              let floor=600;while(!G.isSolid(1000,floor)&&floor<900)floor++;
              const zr=r=>{const out=[];for(const dx of[0,60,110]){let y=600;while(!G.isSolid(1000+dx,y)&&y<900)y++;out.push([dx,y])}return out};
              return {floor,spots:zr()}}""")
            print(f,r);await pg.close()
        await b.close()
asyncio.run(main())
