import sys, asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        for f in ['t_grimspire.html']:
          for cfg in ['[2,3]','[2,3,0,1]']:
            for w in [360,393,412]:
                pg=await (await b.new_context(viewport={"width":w,"height":860},device_scale_factor=2,is_mobile=True,has_touch=True)).new_page()
                await pg.goto("file:///home/claude/work/"+f);await pg.wait_for_timeout(800)
                await pg.evaluate("(c)=>{const G=window.__G;G.newGame('hot',4242,G.mkCfg('hot',c));}",eval(cfg))
                await pg.add_style_tag(content='.tname,#turn,.tcount,#timer{font-family:"DejaVu Sans",Verdana,sans-serif!important;font-weight:700!important} .tname{font-size:clamp(18px,5vw,26px)!important}')
                await pg.wait_for_timeout(600)
                r=await pg.evaluate("()=>{let mx=0;for(const e of document.querySelectorAll('#hud *')){const b=e.getBoundingClientRect();if(b.width)mx=Math.max(mx,b.right)}return [Math.round(mx),innerWidth,document.documentElement.scrollWidth]}")
                print(f,cfg,w,'hud right edge',r[0],'of',r[1],'OVER' if r[0]>r[1]+1 else 'ok')
                if f=='t_grimspire.html' and w==360 and cfg=='[2,3]': await pg.screenshot(path='shots/stress.png',clip={"x":0,"y":0,"width":360,"height":120})
        await b.close()
asyncio.run(main())
