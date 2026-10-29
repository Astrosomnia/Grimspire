import asyncio
from playwright.async_api import async_playwright
SCRIPT = """(seed)=>{const G=window.__G,S=G.S;G.newGame('hot',seed,G.mkCfg('hot',[0,1]));const out=[];const F=(h,p,acts)=>G.simStep([h,p,0,0,acts||[]]);
  const waitAim=()=>{let k=0;while(S.phase!=='aim'&&k<4000){F(0,0);k++}return k};
  for(const tm of[0,1])S.ammo[tm].sentry=3;let drops=0,supers=0,shots=0;
  for(let turn=0;turn<10;turn++){waitAim();if(S.phase==='over')break;
    if(turn<2){F(0,0,[['w','sentry']]);F(1<<4,1<<4)}
    else{const dir=turn%4<2?1:0;for(let i=0;i<160;i++)F(1<<dir,0);F(0,0,[['w','mortar']]);for(let i=0;i<40;i++)F(1<<4,0);F(0,1<<4)}
    for(let i=0;i<400;i++)F(0,0);
    out.push([turn,S.phase,G.stateHash(),G.sentries.map(q=>q.ammo).join('/'),G.troopers.map(t=>t.hp).join(',')]);
    let k=0;while(S.phase!=='aim'&&S.phase!=='over'&&k<4000){if(S.phase==='event'&&G.S.ev&&G.S.ev.k==='drop'&&!G.S.ev._c){G.S.ev._c=1;drops++}F(0,0);k++}}
  out.push(['end',G.stateHash(),'drops seen',drops]);return out}"""
async def run(seed):
    async with async_playwright() as p:
        b=await p.chromium.launch();ctx=await b.new_context();errs=[]
        await ctx.add_init_script("window.requestAnimationFrame=()=>0")
        pg=await ctx.new_page();pg.on("pageerror",lambda e:errs.append(str(e)))
        await pg.goto("file:///home/claude/work/grimspire.html");await pg.wait_for_timeout(800)
        r=await pg.evaluate(SCRIPT,seed);await b.close();return r,errs
async def main():
    for seed in [1234,9001,77]:
        a,ea=await run(seed);b,eb=await run(seed)
        print(seed,'IDENTICAL' if a==b else 'DIFFERENT',ea[:2],eb[:2])
        for row in a:print('  ',row)
asyncio.run(main())
