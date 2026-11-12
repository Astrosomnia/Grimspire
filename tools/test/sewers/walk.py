import asyncio,sys
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page()
        await pg.goto("http://localhost:8791/sew.html",wait_until="domcontentloaded"); await pg.wait_for_timeout(2000)
        r=await pg.evaluate("""(bit)=>{const G=window.__G;G.newGame('hot',28,G.mkCfg('hot',[0,1]));return __E(`(()=>{const w=NS.sewers.find(s=>s.x0!==undefined),t=S.active;
          for(const o of troopers)if(o!==t){o.x=-900;o.alive=false}
          t.x=w.ramp[1]+20;t.y=w.fy-1;t.air=true;S.phase='aim';S.timer=999;S.armed=true;S.locked=false;const out=[];
          for(let i=0;i<1600;i++){simStep([1<<${bit},0,0,0,[]]);S.timer=999;if(i%100===0)out.push([i,Math.round(t.x),Math.round(t.y),t.alive?1:0,t.wet?1:0])}
          return JSON.stringify({w:[w.ramp,w.cy,w.fy,w.manhole,w.pit,w.cliff],out})})()`)}""",int(sys.argv[1]))
        print(r); await b.close()
asyncio.run(main())
