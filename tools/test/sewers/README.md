# Sewer test scripts (12 Nov 2026)

Throwaway Playwright scripts used while building the sewer generator. They expect:

- a test copy of the game served at `http://localhost:8791/sew.html`, from a folder `t/`;
- that copy made from `index.html` with sewers forced on and a debug eval hook:

```
python3 -I -c "
s=open('index.html').read().replace('const SEWERS_ON=/(^#|&)sewers\\\\b/.test(location.hash)','const SEWERS_ON=true')
open('t/sew.html','w').write(s.replace('window.__G={','window.__E=s=>eval(s);window.__G={',1))"
python3 -m http.server 8791 --directory t &
```

| Script | What it does |
|---|---|
| `sewfind.py` | Generates seeds 1–60 and counts sewers per layout (the frequency check). |
| `walk.py <bit>` | Puts a trooper at the ramp foot and walks it (bit 0 = left, 1 = right) to check the route is walkable. |
| `sewshot.py <seeds>` | Lit-renderer screenshots of each seed's sewer (needs SwiftShader WebGL). |
| `rampshot.py <seeds>` | Same, framed on the ramp entrance. |
| `spawn.py` | Counts troopers that spawn inside a sewer. |
| `sewmask.py` | Draws the collision mask around a sewer (debugging stuck walks). |
