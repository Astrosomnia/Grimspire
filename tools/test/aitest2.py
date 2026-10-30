import asyncio, sys
from playwright.async_api import async_playwright
SCRIPT = """(seed)=>{const G=window.__G,S=G.S;if(G.DROP)G.DROP.chance=0;G.newGame('hot',seed,G.mkCfg('hot',[0,1]));S.ctl=['c','c',null,null];
  const F=()=>G.simStep([0,0,0,0,[]]);const hp=()=>G.troopers.map(t=>t.alive?t.hp:0);const res=[];let turns=0,guard=0;
  while(turns<18&&S.phase!=='over'&&guard<200000){while(S.phase!=='aim'&&S.phase!=='over'&&guard<200000){F();guard++}
    if(S.phase==='over')break;const team=S.team,h0=hp(),pos=S.active?Math.round(S.active.x):0;let k=0;
    let PL=null;while(S.phase==='aim'&&k<5000){F();k++;guard++;if(G.AI.plan)PL=G.AI.plan}while(S.phase!=='aim'&&S.phase!=='over'&&k<12000){F();k++;guard++}
    const h1=hp();let foeDmg=0,ownDmg=0;G.troopers.forEach((t,i)=>{const d=h0[i]-h1[i];if(t.team!==team)foeDmg+=d;else ownDmg+=d});
    res.push([foeDmg,ownDmg,(PL&&PL.w)||'-',PL&&PL.hx!==undefined?Math.round(Math.abs(PL.hx-pos)):(PL&&PL.target?Math.round(Math.abs(PL.target.x-pos)):-1),PL&&PL.relocate?1:0]);turns++}
  return res}"""
async def run(f,seed):
    async with async_playwright() as p:
        b=await p.chromium.launch();ctx=await b.new_context();errs=[]
        await ctx.add_init_script("window.requestAnimationFrame=()=>0")
        pg=await ctx.new_page();pg.on("pageerror",lambda e:errs.append(str(e)))
        await pg.goto("file:///home/claude/work/"+f);await pg.wait_for_timeout(800)
        r=await pg.evaluate(SCRIPT,seed);await b.close();return r,errs
async def main():
    for f in sys.argv[1:]:
        allr=[];errs=[]
        for seed in [11,22,33,44,55,66]:
            r,e=await run(f,seed);allr+=r;errs+=e
        n=len(allr);hits=sum(1 for r in allr if r[0]>=1);big=sum(1 for r in allr if r[0]>=30);zero=n-hits
        avg=sum(r[0] for r in allr)/max(1,n)
        from collections import defaultdict
        by=defaultdict(list)
        for r in allr: by[r[2]].append(r)
        for w,v in sorted(by.items(),key=lambda x:-len(x[1])): print("   ",w,len(v),"avg dmg",round(sum(x[0] for x in v)/len(v),1),"avg dist",round(sum(x[3] for x in v)/len(v)),"30+:",sum(1 for x in v if x[0]>=30),"reloc",sum(x[4] for x in v))
        print(f"{f}: turns {n}, avg foe dmg/turn {avg:.1f}, turns with any hit {hits/n:.0%}, 30+ dmg turns {big/n:.0%}, whiffs {zero/n:.0%}, errors {errs[:2]}")
asyncio.run(main())
