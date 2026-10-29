import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch();pg=await (await b.new_context(viewport={"width":1280,"height":720})).new_page()
        await pg.goto("file:///home/claude/work/grimspire.html");await pg.wait_for_timeout(1000)
        await pg.evaluate("()=>{const G=window.__G;G.DROP.chance=0;G.newGame('hot',1234,G.mkCfg('hot',[0,1]));}")
        await pg.wait_for_timeout(1500)
        t=await pg.evaluate("()=>{const q=window.__G.dress().tags[0];return [q.x+q.w/2,q.y+q.h/2]}")
        x,y=t[0]-30,t[1]-4
        print('before',[await pg.evaluate(f"()=>window.__G.dress().scan('{c}',{x},{y},22)") for c in "gtm"])
        await pg.evaluate(f"()=>window.__G.explode({x},{y},22,0)")
        await pg.wait_for_timeout(100)
        print('after',[await pg.evaluate(f"()=>window.__G.dress().scan('{c}',{x},{y},22)") for c in "gtm"])
        await b.close()
asyncio.run(main())
