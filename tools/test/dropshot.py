import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch();pg=await (await b.new_context(viewport={"width":1280,"height":720})).new_page()
        pg.on("pageerror",lambda e:print("PAGEERROR",e))
        await pg.goto("file:///home/claude/work/grimspire.html");await pg.wait_for_timeout(1000)
        await pg.evaluate("()=>{const G=window.__G;G.DROP.chance=1;G.DROP.superChance=1;G.newGame('hot',1234,G.mkCfg('hot',[0,1]));}")
        await pg.add_style_tag(content='#desk{display:none!important}')
        for _ in range(60):
            if await pg.evaluate("()=>window.__G.S.phase==='aim'"):break
            await pg.wait_for_timeout(250)
        await pg.evaluate("()=>{const G=window.__G,S=G.S;S.phase='end'}")
        for i in range(8):
            await pg.wait_for_timeout(700);await pg.screenshot(path=f"shots/drop{i}.png")
        print(await pg.evaluate("()=>window.__G.crates.map(c=>Math.round(c.x)+':'+c.type).join(' ')"))
        await b.close()
asyncio.run(main())
