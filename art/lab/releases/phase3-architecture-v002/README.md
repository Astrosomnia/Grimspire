# Architecture base kit completed — K01–K09 drafts

2 November 2026. Adds the remaining five base components to the first four in `phase3-architecture-v001`. The combined kit image includes all nine at the same art-pixel density, with repeated bridge spans/pier supports and three crown options. This is an unlit native assembly proof, not integrated game terrain.

| Code | New Library version | Native size | Baseline |
|---|---|---|---|
| K04 broken crown | asset-61a606ff2c29995ad833c64e | 112×64 | 63 |
| K05 bridge span | asset-3c3d92f58ad58d62c16652d8 | 180×80 | 79 |
| K06 bridge pier | asset-4e5644372c5465b42a9616ad | 40×200 | 199 |
| K07 three-bay nave | asset-6482c0ef61c25d583ddb9dd6 | 360×300 | 299 |
| K09 timber/iron jetty | asset-6e6ed36ecb94fec528c1e01a | 360×30 | 29 |

All scale 1. Body/Guts on each; K07 magenta clerestory glass in Emissive. Neutral stone ramp matches the first batch. K09 uses the neutral dark timber/iron treatment with continuous structural beam interior. Source illustrations generated with built-in image_gen, then interpreted at exact native grids; deliberate native connector edits. Full prompts in `source-prompts.json`, source PNGs retained locally in `phase3/architecture-v002/`. These remain draft interpretations; no claim of finished hand cleanup or exact-art approval.

## Connections checked

- K04 bottom rows 60–63 match the existing K01 top rows 0–3 exactly in Body and Guts. Fits the same 112-pixel-wide shaft as K02/K03.
- K05 side columns 0–3 match 176–179 across the full height; tile at pitch 180. Pointed lower arch is transparent. End bottom anchors (0,80)/(180,80) align to a K06 top centre (20,0). This is a nominal assembly anchor, subject to collision/stamping review.
- K06 top rows 0–3 match 196–199; vertical pitch 200. Actual lower extent is cut/submerged by code.
- K07 side connector bands match at each 120-pixel bay boundary; three bays per 360-pixel module. All three lower arches remain open. This supports full-width tiling or 120-pixel bay slicing; Claude must verify collision edges and decoration if slicing.
- K09 side columns 0–3 match 356–359. Deck connector rows 0–15, supporting posts below; horizontal pitch 360. No water or reflection painted in.

Body/Guts equality and four open arch checks pass (`checks.json`). All 42 Forge tests pass after Library import. No new game code, shared test revision, current build, live release or terrain/sim changes from this work. In-game stamping, collision, break-up behaviour and phone/desktop art review remain Claude/Jarred's next integration step.

## Ask (Claude)

All nine base components are now available: first four exact versions are in v001; these five complete the base set. Use them in the drowned district on `phase3`, at scale 1. Review collision/playable surfaces separately from ornament, particularly balustrades, jetty posts and glass; maintain open arches and matching connectors. Verify Guts exposure and your GV/determinism checks before any approved gameplay merge. Keep the current shipping grade until Jarred says otherwise.

## Variety still to make

One base piece per code is coverage, not enough visual variety. Next architecture pass: 2–3 separate letter-suffixed drawings each for K01 shafts, K05 bridges and K07 nave bays, sharing the exact dimensions and joints above. Vary lit/dark window layout, missing masonry, buttresses and damage; avoid making every repeated module visibly identical. Existing K02/K03/K04 already offer three crown silhouettes. Foreground wreckage, rocks and distant landmark silhouettes remain in the broader queue.
