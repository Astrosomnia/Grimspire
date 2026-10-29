import asyncio, json
from playwright.async_api import async_playwright
SCRIPT = """(seed)=>{const G=window.__G,S=G.S;G.newGame('hot',seed,G.mkCfg('hot',[0,1]));const out=[];const F=(h,p,acts)=>G.simStep([h,p,0,0,acts||[]]);
  const waitAim=()=>{let k=0;while(S.phase!=='aim'&&k<2400){F(0,0);k++}return k};
  for(const tm of[0,1,2,3])if(S.ammo[tm]){S.ammo[tm].minigun=2;S.ammo[tm].pod=2}
  for(let turn=0;turn<4;turn++){waitAim();const wpn=turn%2?'pod':'minigun';F(0,0,[['w',wpn]]);
    if(wpn==='pod')for(let i=0;i<70;i++)F(1<<2,0);
    F(1<<4,1<<4);for(let i=0;i<500;i++)F(wpn==='minigun'&&i%3===0?1<<3:0,0);
    out.push([wpn,S.phase,G.stateHash(),S.pod?'pod':'-',G.troopers.map(t=>t.hp).join(',')]);
    let k=0;while(S.phase!=='aim'&&k<3000){F(0,0);k++}}
  out.push(['end',G.stateHash()]);return out}"""
async def run(seed):
    async with async_playwright() as p:
        b=await p.chromium.launch();ctx=await b.new_context();errs=[]
        await ctx.add_init_script("window.requestAnimationFrame=()=>0")
        pg=await ctx.new_page();pg.on("pageerror",lambda e:errs.append(str(e)))
        await pg.goto("file:///home/claude/work/grimspire.html");await pg.wait_for_timeout(800)
        r=await pg.evaluate(SCRIPT,seed);await b.close();return r,errs
async def main():
    for seed in [1234,9001]:
        a,ea=await run(seed);b,eb=await run(seed)
        print(seed,'IDENTICAL' if a==b else 'DIFFERENT',ea[:2],eb[:2])
        for row in a:print('  ',row)
asyncio.run(main())
