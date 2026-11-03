# Skyline plates and optional chain/cloth dressing

2 November 2026. Jarred requested occasional chain/fabric variants, then at least twelve architectural skyline plates to replace the procedural vector-looking skyline. Three BACKGROUND planes are supplied: four near, four middle, four far. These near plates are still behind the fight, not foreground/gameplay terrain. All existing D/R/B and K art stays.

| Design | Plane | Native size/baseline | Exact Library version |
|---|---|---|---|
| D01a | dressed foreground | 76×128/127 | asset-3d83158bb4785a0726b69950 |
| D03a | dressed foreground | 208×150/149 | asset-505c8ba97bd106e4860fe4ab |
| D06a | dressed foreground | 216×108/107 | asset-04735ea8946e139c6f4bd0b8 |
| SKY01 | near | 768×384/383 | asset-2461036631197ee20ee4f22c |
| SKY02 | near | 768×384/383 | asset-6ec55febf7bb48e33c81db8b |
| SKY03 | near | 768×384/383 | asset-16ba893c2c344f16b6602f27 |
| SKY04 | near | 768×384/383 | asset-476ec65bb9c9e19121a6c311 |
| SKY05 | middle | 768×384/383 | asset-446c3b3d1f2521ac55f85f95 |
| SKY06 | middle | 768×384/383 | asset-865b479388754587fd42212f |
| SKY07 | middle | 768×384/383 | asset-6a1460b240bff38a174bec93 |
| SKY08 | middle | 768×384/383 | asset-76de8350b5fd9c4161691e03 |
| SKY09 | far | 768×384/383 | asset-ad6f306c2a05aeaf55023753 |
| SKY10 | far | 768×384/383 | asset-9a1c9ccaf417a7088694b208 |
| SKY11 | far | 768×384/383 | asset-d02c008bc2a5adc282999ca9 |
| SKY12 | far | 768×384/383 | asset-22ae7b65564560dc6e04d7d4 |

## What is in the art

SKY01–SKY04: cathedral causeway, sacred-industrial manufactorum, broken aqueduct ward, ribbed dome quarter. Broad masses/structural shapes in a three-value neutral ramp. SKY05–SKY08: needle-spire congregation, terraced shrine quarter, bell-tower embankment, suspension viaduct. Two-value structural silhouettes. SKY09–SKY12: serrated hive, drowned domes, far furnaces, pilgrims' skyline. One-value distant city edge. Distinct roof rhythms, open arches, uneven density, quiet gaps. Built-in generated sources interpreted at native grids with palette/alpha/join edits; source PNGs and all15 prompts preserved under phase3/skyline-plates-v001 locally. Final native cleanup and exact-art judgement pending.

Every SKY plate has a 768×384 transparent canvas, baseline383, scale1, neutral Body and separate window Emissive. No sky, fog, moon, water, reflection or coloured edge light baked into it. Intended profile heights are 352/248/144 art px for near/middle/far. They are decorative and have no collision/Guts. Sparse magenta/cyan window masks are real lights, not fixed fog. Do not use normal play-terrain rim lighting on skyline silhouettes.

Matching low apron: bottom16 rows solid neutral, outer8 columns transparent above row368 and solid below, no edge emission. Hide or submerge this apron at each plane's own background waterline. Start with64px overlap (704px stride); low edge masses and open upper edges avoid slicing spires. These are overlap plates, not a promise that the entire facing edges form a seamless masonry pattern. Choose plate count to cover viewport plus parallax scroll margin. Three plates cover2176 art px before camera offset (~1154 world px at current PX); wide views can require more. Never stretch three plates across the full 2000-world-px map. Avoid immediate repeats and vary order/offset by a stable cosmetic seed; don't reshuffle per frame.

## Let code fog them

Recommended: preserve neutral source values, bake/cached-tint Body toward the current sky/haze colour per plane, increase haze near each plane's waterline, and attenuate Emissive independently with distance. Retain opaque silhouette masks while shifting their colours; merely lowering alpha lets farther city shapes bleed through solid buildings. Keep art edges crisp on the shared pixel grid, with soft atmosphere handled separately. Suggested first parallax factors near0.55/middle0.35/far0.18; fog mixes0.14/0.48/0.75; window strengths0.68/0.38/0.18. These are study starting points, not existing engine settings. Cache selected plate bakes per grade/sky state, not per-frame pixel processing. Water/reflections belong to each depth plane in the engine, as in the North Star.

cold-layer-study.png and crimson-layer-study.png use the SAME neutral art with different sky/fog palettes, three selected plates per plane. Both are standalone ART COMPOSITION STUDIES, not gameplay screenshots or implemented renderer changes. Crimson illustrates reusability; shipping grade is unchanged. plate-library.png shows all12 neutral sources. The far and middle silhouettes are deliberately quieter than the nearest backgrounds and should remain behind trooper/terrain contrast.

## Occasional dressed wreckage

D01a column, D03a broken arch and D06a barge ribs add chain and torn cloth. Bare D01/D03/D06 originals retained. Native sizes, baseline/scale and every pre-existing Body pixel are exactly preserved; only chain additions and separate neutral-grey Cloth/Guts masks were added within the same canvas. Low weight0.3 suggested against bare0.8. Faction None by default for these foreground pieces; no glowing cloth or movement implemented. dressed-pairs.png shows bare/dressed pairs. Foreground cloth must stay subdued; cosmetic dressing must not gain collision or block play paths. New D-letter codes need routing on Claude's side.

## Evidence

- Native dimensions, baseline, scale1, binary alpha and all12 matching side joints pass. Emission lies within Body. All3 dressed variants preserve every original Body pixel and contain new chain and Cloth masks.
- All15 load/placement previews on current fetched main965f763/GV22:30 generic previews (15 desktop1440×900,15 phone-layout390×844), zero page errors, external services blocked. Generic BACKGROUND/PROP dummies test decoding/size/cloth rendering, not SKY-plane composition, haze, parallax or final occlusion. Representative preview screenshots and preview-checks.json included; emulation is not hardware performance approval.
- Forge tests pass48/48 (main plus catalog suites, six catalog checks repeated). No ready/approved flags set. No production game code, shared revision/current build, release data or previous art changed.

## Ask (Claude)

Wire SKY01–SKY12 into the three skyline planes as a pool of overlapping neighbourhood plates, replacing current procedural architectural silhouettes in the north look while retaining sky/lighting/water and appropriate background set pieces. The user has authorised this direction; exact scene and performance still need review before release. Use only versions in injection-manifest.json and keep scale1. Preview at least two plate orders, cold grade, and a portrait camera; check scroll coverage, joins, waterline apron hiding, reflections, window restraint, trooper contrast and cached-bake phone performance. Use latest main/current Forge build, preserving GV22 ghost/deck fixes and any newer work. Wire D01a/D03a/D06a as occasional cosmetic choices alongside bare originals, with separate Cloth tint and no collision. Runtime/code remains Claude's; no skyline implementation is claimed in this save.
