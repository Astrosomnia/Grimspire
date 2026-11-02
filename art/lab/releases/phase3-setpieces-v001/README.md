# First Phase 3 set-piece drafts — 2 November 2026

Four new Library versions, scale 1, Body plus separate hollow-masonry/iron-tie Guts. No emissive, cloth, water, reflections or baked glow. The heads are separate drawings, not the same sprite enlarged. All use six neutral material values. Current live art/build unchanged.

| Slot | New version | Native size | Baseline | Inclusive support columns | Family |
|---|---|---|---|---|---|
| S01 normal head | asset-30663904acde901ec8905590 | 138×104 | 103 | 30–108 | custom-98e34866-4b73-497c-9766-bbc294a47f57 (existing) |
| S09 colossal head | asset-d0b4af1b0a7dd9235dcd6ac8 | 258×200 | 199 | 57–201 | custom-b1597c3e-35c2-40b7-822b-75e5dc366781 (new) |
| S07 pedestal saint | asset-b4c513d2e6d153bc9159400c | 31×96 | 95 | 1–28 | custom-de76d228-834e-4026-89f0-3ce226ddc7df (new) |
| S03 perched gargoyle | asset-a858277c30ab4cdd7b55381f | 74×56 | 53 | 30–49 | custom-0b9c856f-d060-487e-a119-dd8c04efef15 (existing) |

Each document carries the parsed placement block in its notes: play band, decorative/non-solid, no local light, flippable. Heads: sump, sink 0.3–0.5; S09 weight 0.3, limit 1. Saint: pinnacle, centred pedestal. Gargoyle: ledge, faces right; 20 supported columns under the rear haunch, tail curling back across the roof and foreclaws over the drop. The curled tail/wing makes the overall silhouette wider than the haunch: support is deliberately under the foot, not the first third of the bounding box. Baseline 53 lets the tail/claws drape two rows lower.

## Evidence and limits

- Added with the Forge's `add_asset.mjs`, preserving S01/S03 families and all old versions. All 42 Forge checks pass.
- Main `dd6555a` actual parser, geometry, socket scan and footprint/headroom checks exercised on a small constructed terrain fixture at actual game PX (27/(611/12)). Both head fits, pinnacle fit and both gargoyle facings pass. `placement-checks.json` records them. This is not a test across generated battle maps.
- `renderer-native-1x.png`: actual main `setPiecesDraw` at one raster pixel per art pixel, with 35% sump clipping and magenta/cyan local edge lights. Current live torso/arm/leg PNGs assembled in idle at their sockets for scale. Simplified ground, not the game's complete map/water renderer.
- `renderer-review.png`: the same proof enlarged 1.5× for convenient reading; use native file to inspect exact pixels. This enlarged presentation does not alter asset scale.
- Source drawings made using built-in image generation with the approved concept sheet as reference; exact prompts in `source-prompts.json`. Encoded to the final native grid, six-step ramp, with disconnected dust removal and isolated-material-cluster cleanup. Those are draft interpretations, not a claim of fully hand-drawn final art. Remaining artistic cleanup/readability should be judged in battle, especially the 31-pixel-wide saint and fine halo fractures.

Drawn: yes. Saved: new Library drafts. Tested: Forge schema/index plus isolated renderer/constructed-terrain placement checks. Approved exact art: pending. In main/live game: no. Full battle and phone review: pending. No new shared revision/current build, game-code change or release supplied.

## Ask (Claude)

Please load only these four slots into the latest Phase 3 test build when preparing the scene; preserve the other current art and don't promote an older complete payload. Test both heads at 0.3 and 0.5 sink, saint on narrow crowns, gargoyle on both ledge directions, and breakup/lost support on real generated maps. Keep SP_LIVE false. Jarred has approved the direction and asked for progress, not these exact versions or a live release. Background/water on `phase3` can proceed against these drafts. Confirm any pedestal/halo visibility or fit failures with a screenshot before changing scale; all art remains scale 1.
