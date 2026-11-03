# World-depth batch: wreckage, rocks and distant landmarks

2 November 2026. Thirteen separate Library drafts, native scale 1. Existing architecture and variants retained. Generated raster sources interpreted at native pixel grids; silhouette flattening, palette/alpha edits and rock joint construction in the native documents. Original generated PNGs and the full prompt set are preserved locally under phase3/world-depth-v001/. Built-in image generation used; these are drafts requiring a final native cleanup/art judgement pass.

| Code | Design | Native w×h / baseline | Exact version |
|---|---|---|---|
| B01 | Colossal drowned saint | 252×340 / 339 | asset-f1c7e92862a3bd96d9d7b4ff |
| B02 | Drowned broken dome | 440×216 / 215 | asset-0a7f2e7628b5b71e5d8a8dc1 |
| B03 | Broken horizon bridge | 496×180 / 179 | asset-ee22d601cd15411df40be270 |
| D01 | Broken fluted column | 76×128 / 127 | asset-0fc3c3280f0552a9451174ab |
| D02 | Fallen masonry slab | 184×62 / 61 | asset-b3e7c0fe0d15d44825b743c1 |
| D03 | Half-sunk broken arch | 208×150 / 149 | asset-7295ba0af7475e112c1c7a75 |
| D04 | Chained mooring posts | 150×104 / 103 | asset-f3a523548e40e3efb58e9a2d |
| D05 | Toppled saint hand | 138×90 / 89 | asset-4ca778daa53525c7e1036e3c |
| D06 | Capsized barge ribs | 216×108 / 107 | asset-608e2a13f402d8ddf32e68a4 |
| R01 | Stratified shore shelf | 240×120 / 119 | asset-5dda03bfbf30f92544a3fdc4 |
| R02 | Basalt tooth outcrop | 240×120 / 119 | asset-0e2e2f5f20a389482c2e6de0 |
| R03 | Split boulder shore | 240×120 / 119 | asset-186bf19c1e53f2b95bcb237e |
| R04 | Tumbled talus bank | 240×120 / 119 | asset-1d474c9fee7eee32a8057ec9 |

## Layers and integration

D01–D06: flat near-black Body, Guts, foreground band, non-solid. Lower third goes under renderer water; top edge/reflection/parallax in code. D04 includes the chain already required by the brief. B01–B03: one-value Body and Guts, back band, non-solid; separately emissive small magenta/cyan windows. Haze and reflection in code. R01–R04: neutral natural rock Body/Guts, play band, intended to become destructible terrain. All are 240×120, baseline119, scale1, allowing interchange in the same shore envelope. Four-column side bands match exactly in Body/Guts: transparent above row104, solid below; bottom four rows also match. Other interior/upper geometry differs; connector compatibility does not imply equal collision.

Current Forge accepts these design codes in Library documents, but D/R/B are not live slots yet. Generic PROP/BACKGROUND previews are evidence of loading and scale only. Do not use Save & test / Go live with these raw codes until the proper renderer/slot paths exist. Claude owns that code; none changed by this art save.

## Foundation variation requested by Jarred

Sometimes bury building feet in rock or let masonry protrude from a rocky cliff, varying overlap depth, lateral offset, rock type and building choice with the map seed. Keep ordinary exposed foundations as another option. foundation-overlap-study.png shows existing K01/K02 with three new rocks. It is an ART COMPOSITE, not a runtime screenshot and not a proof of traversal.

Suggested first step: one tower-foot shelf overlap in the drowned generator, then selected nave shoulders/pier feet. Union the terrain silhouettes; material rendering and collision must agree. Keep useful portals, route clearance, stable support, spawn/landing access and blast paths, avoid thin slivers. Check destruction/Guts at the rock–masonry boundary and required deterministic sim/GV/fingerprint checks. No random unseeded geometry. Jarred asked for the capability; exact implementation is Claude's.

## Future dressing direction

Jarred wants occasional chains and dangling torn fabric from the OG/interim North Stars, not dressing on every piece. Pair bare/dressed structural or decoration variants later so map selection produces variety. Keep attachments with their correct parent/depth/occlusion; fabric belongs in neutral-grey Cloth for faction or None tint. Do not imply animation or collision is implemented. The current priority is this D/R/B batch first; no blanket chain/cloth retrofit in this save.

## Evidence and limits

- Native sizes, baseline, scale1, binary transparency and common rock Body/Guts connector checks pass for all13.
- Forge tests: 48 pass (test.mjs plus catalog.test.mjs; includes six catalog checks repeated by the main suite).
- 26 local generic game previews: each of13 tested at desktop1440×900 and phone-layout390×844, zero page-script errors. Existing GV21 game source3b7446d, services blocked; browser emulation, not phone hardware performance approval. preview-checks.json records the results; representative D04/R03/B02 screenshots included.
- Preview screenshots deliberately use generic dummies on existing terrain: rocks are not collision-stamped, foreground pieces not in foreground parallax, back silhouettes not yet hazed/cut by background water. They are not the final scene target. The contact sheets and foundation study are artwork reviews, not in-game evidence.
- No production code/current shared build/revision/approved flag/live release changed. Exact-art and full scene/gameplay approvals pending.

## Ask (Claude)

Use only exact versions in injection-manifest.json. Wire D/R/B slots and the intended depth bands/rock terrain path, preserve current look, water, new architecture and live revisions. Test foreground occlusion so silhouettes stay off trooper paths; background haze/waterline/light restraint; seeded rock joins, standing surfaces, foundation overlap, collision and destruction. Produce a fixed desktop/phone scene for Jarred before release. Keep chain/cloth bare–dressed variants in the future queue, after this batch.

Current live state advanced during creation: Claude released the eight structural architecture alternatives and ghost/deck fixes as GV22, revision 20261103T002340Z-5e856f96. The generic preview evidence above uses GV21 and predates those fixes. This art upload preserves the entire latest GV22 state/revisions unchanged; integration must use the latest main.
