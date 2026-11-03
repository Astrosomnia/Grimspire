# Traversal and foundations — nine saved art drafts

Jarred requested the complete Claude brief in one cohesive pass, with limited remaining rounds of refinement. This delivers four traversal structures plus five substantial load-bearing foundations. New assets, not replacements for existing architecture/shore strips. Prepared with built-in image generation, then interpreted into native grids and the established six-step stone palette. Source PNGs, individual native layers/documents, measured masks and a common-scale review are included.

## Inventory

| Code | Piece | Native canvas | Baseline | Placement intent |
|---|---|---|---|---|
| K14 | Fallen cathedral span | 320×200 | 199 | Low left end sinks into shore/water; high right landing connects to a bridge/tower |
| K15 | Flying buttress crossing | 320×224 | 223 | High left attachment, low right rock foot, open underpass |
| K16 | Broken stair ramp | 320×192 | 191 | Lower-left approach to upper-right landing; lower arch route |
| K17 | Snapped bridge stub | 180×80 | 79 | Clean left join, broken right end; deck row 18 |
| R05 | Cathedral crag foundation | 480×240 | 239 | Broad building seat and lower shelf |
| R06 | Sea-stack foundation | 272×320 | 319 | Tower-sized crown, thick neck, flared foot |
| R07 | Overhanging cliff foundation | 448×272 | 271 | Upper shelf, lower ledge, open recess |
| R08 | Scree access ramp | 448×224 | 223 | Continuous rocky ascent to a building seat |
| R09 | Rock-to-masonry footing | 448×240 | 239 | Flat masonry plinth embedded in substantial bedrock |

All scale 1, pixel_scale 12; Body and Guts, no Emissive. Art is dark unlit material; the renderer supplies light. Sources were uniformly fitted, not distorted: some canvases have transparent space above the actual geometry. Use actual Body alpha/occupied bounds, not the rectangular canvas, for physical joins. The source and native images are art studies, not runtime captures.

## Claude integration handoff

- Exact immutable Library paths, IDs, hashes and dimensions: `injection-manifest.json`. Every original registration is retained. Nothing in this batch changes current shared build/state/revisions or the production game.
- New K14–K17 / R05–R09 slots and game integration are Claude work. Use current main and preserve GV25 high bridges, stacked decks, broken stubs, earlier art and any newer changes. No runtime rotation: the diagonals are drawn at angle.
- K17 deliberately uses K05's **180×80 canvas, base79 and deck18**; first four Body/Guts columns are byte-identical to original K05, including the decorative upper connector. Only rows18+ should be solid along this join. Its opaque snapped tip ends before the right edge of the canvas; do not stretch or tile it like a full span.
- The other diagonals **cannot keep an 80-row canvas without clipping or compressing the drawn angle**. They are standalone angled pieces with larger canvases; place their measured landing points at existing deck heights. They are not dimension-compatible K05 variants. Flat top runs are measured in each asset's notes and manifest; those are candidate landing surfaces, not validated placement sockets or spawn approval.
- Keep full native collision silhouettes for K14–K16 and all five R pieces, including lower openings and overhangs: **no global automatic deck cut**. Only K17 uses `deck: 18`. Lower branches/feet must meet supporting rock or masonry, with consistent visible and collision unions. Do not hang K14 arch fragments unsupported above the water; bury/support the lower ends.
- R05/R06/R09 crowns support masonry. For R07, carry buildings over the substantial left/central rock, not the unsupported far nose. Bury irregular rock bottoms; overlap buildings into foundations enough to hide gaps. Vary burial/overlap rather than pixel size; retain useful arch exits and paths above starting water. R08 supplies a rocky ascent, not just shoreline decoration.
- Inspect K16 tread heights against step-up code; rails/recess details should not snag walking. Check crossings, headroom, projectiles, falling/knockback destinations, spawn access, destruction/Guts, sump rise, portrait framing and actual phone performance. New collision/placement needs deterministic tests and GV handling.

## Generation prompt set

Built-in image generation, nine separate transparent assets. Existing K05 Body and R01 Body were material/style references. Common constraints: side-on orthographic 2D pixel art; coarse deliberate clusters; dark neutral charcoal blue-grey, restricted 5–6-value ramp; flat unlit surfaces; no coloured rim, glow, scene, water, sky, people or labels; true alpha openings; solid masonry and load-bearing geology; no thin metal truss/shipyard treatment. Single complete object per output.

Individual briefs: K14 substantial 25-degree fallen bridge rising left to right with low broken end and upper landing; K15 thick descending flying buttress from high left attachment to low right rock foot and a large pointed underpass; K16 shallow-tread stone stair ramp rising left to right with a lower arch and broken upper landing; K17 horizontal bridge stub with clean left join and chunky snapped right end. R05 broad crag plateau with a central building seat; R06 thick-necked sea stack with broad crown and foot; R07 supported overhang with thick upper shelf and a lower ledge; R08 continuous talus/bedrock access slope; R09 interlocked natural rock and embedded Gothic masonry plinth.

## Evidence and limits

- `native-checks.json`: dimensions, occupied bounds, binary transparency, matching Body/Guts alpha, colours, single connected silhouette for every piece, and exact K17 left connector checks.
- `forge-tests.txt`: all42 Forge checks pass. The import tool validated each document using the Forge's own model.
- `native-review.png`: actual encoded Body layers, all at the same 1:1 art-pixel scale, with a 50-art-pixel size bar per panel. No runtime or phone battle testing is claimed.
- Drawn and saved drafts; final native cluster cleanup, exact in-scene art approval, traversal/collision/destruction and live release remain pending. Ready for Claude to integrate and review, not marked ready/approved production art.
