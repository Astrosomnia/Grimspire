import asyncio
from playwright.async_api import async_playwright
async def run(f,seed):
    async with async_playwright() as p:
        b=await p.chromium.launch();pg=await (await b.new_context()).new_page();errs=[]
        pg.on("pageerror",lambda e:errs.append(str(e)))
        await pg.goto("file:///home/claude/work/"+f);await pg.wait_for_timeout(800)
        r=await pg.evaluate("(s)=>{const G=window.__G;G.newGame('hot',s,G.mkCfg('hot',[0,1,2,3]));return [G.stateHash(),G.S.layout,G.troopers.map(t=>Math.round(t.x)).join(',')]}",seed)
        await b.close();return r,errs
async def main():
    for seed in [1234,77,9001,42]:
        a=await run('orig.html',seed);b=await run('grimspire.html',seed)
        print(seed,'MATCH' if a[0]==b[0] else 'DIFF',a[0][:2],b[0][:2],b[1])
asyncio.run(main())
