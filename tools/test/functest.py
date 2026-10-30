import asyncio
from playwright.async_api import async_playwright
SETUP="""()=>{const G=window.__G,S=G.S;G.DROP.chance=0;G.newGame('hot',1234,G.mkCfg('hot',[0,1]));S.ctl=[null,null,null,null];
 const F=(h,p,a)=>G.simStep([h||0,p||0,0,0,a||[]]);let k=0;while(S.phase!=='aim'&&k<4000){F();k++}
 // flat arena: active trooper at 1000, an enemy right in front
 G.testFlat(800,1300,600);const t=S.active,e=G.troopers.find(o=>o.team!==t.team);
 for(const o of G.troopers){if(o!==t&&o!==e){o.x=200+G.troopers.indexOf(o)*20;}}
 t.x=1000;t.y=600;t.face=1;t.vx=t.vy=0;t.air=false;e.x=1018;e.y=600;e.vx=e.vy=0;e.air=false;
 return [S.team,t.hp,e.hp]}"""
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch();ctx=await b.new_context();await ctx.add_init_script("window.requestAnimationFrame=()=>0")
        pg=await ctx.new_page();errs=[];pg.on("pageerror",lambda e:errs.append(str(e)))
        await pg.goto("file:///home/claude/work/grimspire.html");await pg.wait_for_timeout(800)
        # 1. fist through a wall
        await pg.evaluate(SETUP)
        r=await pg.evaluate("""()=>{const G=window.__G,S=G.S,F=(h,p,a)=>G.simStep([h||0,p||0,0,0,a||[]]),t=S.active,e=G.troopers.find(o=>o.team!==t.team);
          G.testWall(1008,560,600);const h0=e.hp;F(0,0,[['w','fist']]);F(1<<4,1<<4);for(let i=0;i<30;i++)F();return ['wall: enemy hp',h0,'->',e.hp]}""")
        print(r)
        # 2. fist uppercut in the open
        await pg.evaluate(SETUP)
        r=await pg.evaluate("""()=>{const G=window.__G,S=G.S,F=(h,p,a)=>G.simStep([h||0,p||0,0,0,a||[]]),t=S.active,e=G.troopers.find(o=>o.team!==t.team);
          const x0=e.x;F(0,0,[['w','fist']]);F(1<<4,1<<4);let top=e.y;for(let i=0;i<240;i++){F();top=Math.min(top,e.y)}return ['uppercut: hp',e.hp,'peak height',Math.round(600-top),'landed dx',Math.round(e.x-x0)]}""")
        print(r)
        # 3. jump pack: thrust, land with fuel, press fire again -> thrusts, not mortar
        await pg.evaluate(SETUP)
        r=await pg.evaluate("""()=>{const G=window.__G,S=G.S,F=(h,p,a)=>G.simStep([h||0,p||0,0,0,a||[]]),t=S.active;S.ammo[S.team].jet=2;
          F(0,0,[['w','jet']]);F(1<<4,1<<4);for(let i=0;i<20;i++)F(1<<4,0);for(let i=0;i<200;i++)F();
          const landed={air:t.air,weapon:S.weapon[S.team],parked:!!(S.jet&&S.jet.parked),fuel:S.jet&&+S.jet.fuel.toFixed(2),projs:G.projs.length};
          const y0=t.y;F(1<<4,1<<4);for(let i=0;i<20;i++)F(1<<4,0);return ['jet',landed,'after fire again: rose',Math.round(y0-t.y),'projectiles',G.projs.length,'phase',S.phase]}""")
        print(r)
        # 4. drone hop
        await pg.evaluate(SETUP)
        r=await pg.evaluate("""()=>{const G=window.__G,S=G.S,F=(h,p,a)=>G.simStep([h||0,p||0,0,0,a||[]]),t=S.active;S.ammo[S.team].drone=1;G.testWall(1060,570,600);
          F(0,0,[['w','drone']]);F(1<<4,1<<4);for(let i=0;i<40;i++)F();let d=G.S.drone;const x0=Math.round(d.x);for(let i=0;i<60;i++)F(1<<1,0);const stuck=Math.round(G.S.drone.x);
          F(1<<1,1<<5);for(let i=0;i<70;i++)F(1<<1,0);return ['drone start',x0,'at wall',stuck,'after hop',Math.round(G.S.drone?G.S.drone.x:-1)]}""")
        print(r)
        print('errors',errs[:3]);await b.close()
asyncio.run(main())
