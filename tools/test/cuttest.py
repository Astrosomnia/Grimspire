import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch();ctx=await b.new_context();await ctx.add_init_script("window.requestAnimationFrame=()=>0")
        pg=await ctx.new_page();errs=[];pg.on("pageerror",lambda e:errs.append(str(e)))
        await pg.goto("file:///home/claude/work/grimspire.html");await pg.wait_for_timeout(800)
        r=await pg.evaluate("""()=>{const G=window.__G,S=G.S;G.DROP.chance=0;G.newGame('hot',777,G.mkCfg('hot',[0,1]));const F=(h,p,a)=>G.simStep([h||0,p||0,0,0,a||[]]);
          let k=0;while(S.phase!=='aim'&&k<4000){F();k++}G.testFlat(500,1500,600);const t=S.active;for(const o of G.troopers){o.x=100+G.troopers.indexOf(o)*12;o.y=200}
          t.x=800;t.y=600;t.face=1;t.aim=0;t.air=false;const e=G.troopers.find(o=>o.team!==t.team);e.x=814;e.y=600;e.air=false;e.hp=100;
          // a block of rock so the cutter digs, with the enemy standing in the torch
          G.testWall(826,560,600);G.testWall(830,560,600);
          F(0,0,[['w','cutter']]);F(1<<4,1<<4);const log=[];for(let i=0;i<60*4;i++){F();if(i%20===0)log.push([Math.round(t.x),Math.round(e.x),e.hp,!!S.cut,S.cut&&S.cut.dig])}return ['cutter damage',100-e.hp,log]}""")
        print(r,errs[:2]);await b.close()
asyncio.run(main())
