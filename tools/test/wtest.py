import asyncio, sys
from playwright.async_api import async_playwright
RUN="""([w,dist,group])=>{const G=window.__G,S=G.S;if(G.DROP)G.DROP.chance=0;G.newGame('hot',777,G.mkCfg('hot',[0,1]));S.ctl=[null,null,null,null];
 const F=(h,p,a)=>G.simStep([h||0,p||0,0,0,a||[]]);let k=0;while(S.phase!=='aim'&&k<4000){F();k++}
 G.testFlat(500,1700,600);const t=S.active,foes=G.troopers.filter(o=>o.team!==t.team);
 for(const o of G.troopers){o.x=100+G.troopers.indexOf(o)*12;o.y=200}
 t.x=800;t.y=600;t.face=1;t.aim=0;t.vx=t.vy=0;t.air=false;
 const tg=foes.slice(0,group);tg.forEach((o,i)=>{o.x=800+dist+i*22;o.y=600;o.vx=o.vy=0;o.air=false;o.hp=100;o.alive=true});
 // aim at the first target's chest
 t.aim=Math.atan2((600-11)-(600-12),dist)*1;S.ammo[S.team][w]=3;F(0,0,[['w',w]]);F(1<<4,1<<4);for(let i=0;i<60*7;i++)F(0,0);
 return tg.map(o=>100-o.hp)}"""
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch();ctx=await b.new_context();await ctx.add_init_script("window.requestAnimationFrame=()=>0")
        for f in sys.argv[1:]:
            pg=await ctx.new_page();errs=[];pg.on("pageerror",lambda e:errs.append(str(e)))
            await pg.goto("file:///home/claude/work/"+f);await pg.wait_for_timeout(800)
            print('==',f)
            for w in ['minigun','bolter','flamer']:
                row=[]
                for d in ([30,150,320] if w!='flamer' else [40,110,180]):
                    r=await pg.evaluate(RUN,[w,d,1]);row.append(f"{d}px:{r[0]}")
                if w=='flamer':
                    r=await pg.evaluate(RUN,[w,70,3]);row.append(f"group of 3 at 70px:{r}")
                print(f"  {w:8}",'  '.join(row))
            print('  errors',errs[:2]);await pg.close()
        await b.close()
asyncio.run(main())
