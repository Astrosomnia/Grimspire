import asyncio,json,sys
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(args=["--use-gl=swiftshader","--enable-unsafe-swiftshader","--ignore-gpu-blocklist"])
        for sd in [int(x) for x in sys.argv[1].split(',')]:
            pg=await (await b.new_context(viewport={"width":1600,"height":900})).new_page(); errs=[]
            pg.on("pageerror",lambda e:errs.append(str(e)[:200]))
            await pg.goto("http://localhost:8791/sew.html",wait_until="domcontentloaded",timeout=90000); await pg.wait_for_function("window.GRIMSPIRE_ART_READY===true",timeout=60000)
            sw=json.loads(await pg.evaluate(f"()=>{{const G=window.__G;G.newGame('hot',{sd},G.mkCfg('hot',[0,1]));return __E('JSON.stringify(NS.sewers.find(s=>s.x0!==undefined))')}}"))
            await pg.wait_for_timeout(5000)
            for z,k in [('wide',2.0)]:
                cx=(sw['x0']+sw['x1'])/2;cy=sw['fy']-20
                await pg.evaluate("(a)=>__E(`(()=>{S.camFree=true;S.zoom=${a[0]}/window.__G.base();window.__G.camSet(${a[1]}-innerWidth/2/${a[0]},${a[2]}-innerHeight/2/${a[0]})})()`)",[k,cx,cy])
                await pg.wait_for_timeout(1300); await pg.screenshot(path=f"t/sew_{sd}_{z}.png")
            print(sd,sw,errs[:2]); await pg.close()
        await b.close()
asyncio.run(main())
