import sys, asyncio, os
from playwright.async_api import async_playwright
html=sys.argv[1]; out=sys.argv[2]
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(proxy={"server":os.environ["HTTPS_PROXY"]} if os.environ.get("HTTPS_PROXY") else None,args=["--ignore-certificate-errors"])
        for name,vp in [("port",{"width":412,"height":915}),("land",{"width":915,"height":412}),("small",{"width":360,"height":740})]:
            pg=await (await b.new_context(viewport=vp,device_scale_factor=2,is_mobile=True,has_touch=True)).new_page()
            pg.on("pageerror",lambda e:print("PAGEERROR",e))
            await pg.goto("file://"+html);await pg.wait_for_timeout(1200)
            await pg.evaluate("()=>{const G=window.__G;G.newGame('hot',4242,G.mkCfg('hot',[2,3,0,1]));}")
            await pg.wait_for_timeout(2500)
            await pg.screenshot(path=f"{out}-{name}.png")
        await b.close()
asyncio.run(main())
