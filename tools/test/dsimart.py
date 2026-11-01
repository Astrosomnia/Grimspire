import asyncio, sys
from playwright.async_api import async_playwright
SCRIPT = """(a)=>{const[seed,wait]=a;const G=window.__G,S=G.S;G.newGame('hot',seed,G.mkCfg('hot',[0,1]));const out=[];const F=(h,p,acts)=>G.simStep([h,p,0,0,acts||[]]);
  const W=['mortar','rail','scatter','bolter','las','flamer','rail','mortar'];
  for(let turn=0;turn<8;turn++){let k=0;while(S.phase!=='aim'&&k<2400){F(0,0);k++}
    const wpn=W[turn];for(const tm of[0,1])if(S.ammo[tm])S.ammo[tm][wpn]=5;F(0,0,[['w',wpn]]);
    for(let i=0;i<20+turn*3;i++)F(1<<(turn%2?0:1),0);
    F(1<<4,1<<4);for(let i=0;i<40;i++)F(1<<4,0);for(let i=0;i<600;i++)F(0,0);
    out.push([wpn,S.phase,G.stateHash(),G.troopers.map(t=>t.hp).join(',')]);
    k=0;while(S.phase!=='aim'&&k<3000){F(0,0);k++}}
  out.push(['end',G.stateHash()]);return out}"""
async def run(path,seed,wait):
    async with async_playwright() as p:
        b=await p.chromium.launch();ctx=await b.new_context();errs=[]
        await ctx.add_init_script("window.requestAnimationFrame=()=>0")
        pg=await ctx.new_page();pg.on("pageerror",lambda e:errs.append(str(e)))
        await pg.goto("file://"+path);await pg.wait_for_timeout(wait)
        ready=await pg.evaluate("[!!window.GRIMSPIRE_ART_READY,window.GRIMSPIRE_ART_ERROR||'']")
        r=await pg.evaluate(SCRIPT,[seed,wait]);await b.close();return r,errs,ready
async def main():
    import os;path=os.path.abspath(sys.argv[1])
    for seed in [1234,9001]:
        a,ea,ra=await run(path,seed,50);b,eb,rb=await run(path,seed,1500)
        print(seed,'IDENTICAL' if a==b else 'DIFFERENT','art ready',ra,rb,ea[:2],eb[:2])
        for x,y in zip(a,b):print('  ',x,'' if x==y else ' <> '+str(y))
asyncio.run(main())
