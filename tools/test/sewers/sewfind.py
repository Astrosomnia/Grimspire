import asyncio,json
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(); errs=[]; pg.on("pageerror",lambda e:errs.append(str(e)[:200]))
        await pg.goto("http://localhost:8791/sew.html",wait_until="domcontentloaded"); await pg.wait_for_timeout(2500)
        r=await pg.evaluate("""()=>{const G=window.__G,out=[];const t0=performance.now();for(let s=1;s<=60;s++){G.newGame('hot',s,G.mkCfg('hot',[0,1]));out.push([s,G.S.layout,__E('JSON.stringify(NS.sewers.filter(x=>x.x0!==undefined).map(x=>[x.x0,x.cy,x.pit,x.cliff!==null]))'),__E('NS.falls.length')])}return [performance.now()-t0,out]}""")
        print('ms',round(r[0]));layouts={}
        for s,l,sw,f in r[1]:
            layouts.setdefault(l,[0,0]);layouts[l][0]+=1
            if sw!='[]':layouts[l][1]+=1;print(s,l,sw,f)
        print(layouts,errs[:3]); await b.close()
asyncio.run(main())
