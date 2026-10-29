"""Screenshot a Grimspire battle.  python3 shot.py <html> <out-prefix> [seed ...]
For each seed: a desktop overview, a desktop close-up on the first two troopers, and a phone close-up."""
import sys, asyncio
from playwright.async_api import async_playwright

html, out = sys.argv[1], sys.argv[2]
seeds = [int(s) for s in sys.argv[3:]] or [1234]

SETUP = """(seed)=>{const G=window.__G;G.newGame('hot',seed,G.mkCfg('hot',[0,1]));}"""
FOCUS = """([i,z])=>{const G=window.__G,S=G.S,t=G.troopers[i];S.camFree=true;S.zoom=z;
  const b=G.base()*z;G.camSet(t.x-innerWidth/2/b,t.y-12-innerHeight/2/b);return [Math.round(t.x),Math.round(t.y),t.team]}"""
OVER = """()=>{const G=window.__G,S=G.S;S.camFree=true;S.zoom=.55;G.camSet(0,900);}"""

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(args=["--use-gl=swiftshader", "--enable-unsafe-swiftshader"])
        for seed in seeds:
            for name, vp, mobile in [("desk", {"width": 1280, "height": 720}, False), ("phone", {"width": 844, "height": 390}, True)]:
                ctx = await b.new_context(viewport=vp, device_scale_factor=2 if mobile else 1, is_mobile=mobile, has_touch=mobile)
                pg = await ctx.new_page()
                pg.on("pageerror", lambda e: print("PAGEERROR", e))
                await pg.goto("file://" + html)
                await pg.wait_for_timeout(1500)
                await pg.evaluate(SETUP, seed)
                await pg.add_style_tag(content='#desk,#touch,#recenter{display:none!important}')
                await pg.wait_for_timeout(9000)
                if name == "desk":
                    await pg.evaluate(OVER); await pg.wait_for_timeout(250)
                    await pg.screenshot(path=f"{out}-{seed}-over.png")
                for i in ([0, 1] if name == "desk" else [0]):
                    info = await pg.evaluate(FOCUS, [i, 2.2])
                    await pg.wait_for_timeout(250)
                    await pg.screenshot(path=f"{out}-{seed}-{name}-t{i}.png")
                await ctx.close()
        await b.close()

asyncio.run(main())
