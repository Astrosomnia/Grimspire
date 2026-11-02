# Architecture first batch — Parts 3/4 brief, 2 November 2026

| Code | Library version | Size | Baseline |
|---|---|---|---|
| K08 cathedral front | asset-a4bcf746ba5984c9bf412403 | 512×360 | 359 |
| K01 tower shaft | asset-7b136c7a17200bcf120a312d | 112×100 | 99 |
| K02 spire cap | asset-9fa21f5a16bd94b652aeb063 | 112×192 | 191 |
| K03 crenellated crown | asset-6768333ba4cd15664ae8b807 | 112×40 | 39 |

Scale 1 throughout. Body/Guts on all four; magenta glass in separate Emissive on K08/K01. Dark windows are material, no baked glow or coloured rims. Source drawings use built-in image generation with the approved interim North Star; exact final native grids and six-value neutral ramp encoded afterwards. Source PNGs retained locally under `phase3/architecture-v001/`; prompt descriptions in `source-prompts.json` (cathedral entry is a summary). These are draft interpretations, with hand cleanup and final scene judgement still required.

## Joints

- Common tower connector width 112, x=0–111 inclusive. K01 rows 0–3 match rows 96–99 byte for byte in Body and Guts. Stack at pitch 100; no overlap or scale multiplier. The four-row connector pattern repeats once at each join; visible band is intentional masonry, not a transparent seam.
- K02 rows 188–191 and K03 rows 36–39 match the shaft connector. Put either cap immediately above K01. Shaft ×2 + spire = 392 art px high; shaft ×2 + crown = 240.
- K08 foundation baseline 359; centre portal remains transparent at the floor. Shoulder galleries are drawn, but their exact walkable/collision anchors need Claude's stamping review. Do not stretch K08 to the spike placeholder's bounding box; choose layout dimensions in world units using the shared art density.
- Opaque Body behind lit glass is neutral dark material; Emissive carries the glass colour. Claude should deliberately choose the window/glass collision rule when stamping rather than infer one from emission.

## Review and evidence

`kit-native-1x.png`: unlit Body + glass Emissive at native art grid, showing a cathedral, two-shaft spire tower and two-shaft crown tower. No game lighting or bloom applied. `spike-comparison.png`: this assembly beside a real local capture of phase3 `cf28511` drowned test scene (zero page errors, external services blocked). It is a side-by-side art handoff, not a screenshot of integrated new buildings. `checks.json`: joint width/band equality and open central portal checks.

Saved through `add_asset.mjs`; all 42 Forge checks pass. K slots/stamping do not exist yet, as the brief states; no fake PROP release or game-code edits supplied. No new shared build, terrain integration, collision test, final phone art review, exact-version approval or release. The shipping grade remains unchanged.

## Ask (Claude)

First four pieces are ready for a stamping experiment on your `phase3` drowned district. Add K support and use these exact versions; preserve current lighting/water, other art and main. Review module joints, playable shoulder/merlon surfaces, portal and glass collision, and Guts exposure. Terrain mask changes belong to your sim/GV/determinism checks. Send a fixed-scene desktop/phone comparison before any live merge. Keep pixel scale 1 and let the new soft illumination reveal the broad planes.

Next architecture work: K05 bridge, K06 pier, K07 nave; then K04 broken crown and K09 jetty. Following the forwarded queue, D01–D06 foreground wreckage comes after the architecture kit, then R01–R04 rocks, then B01–B03 background silhouettes. Ordinary skyline architecture remains procedural; B01–B03 are the explicit distant landmark exceptions in Part 4.
