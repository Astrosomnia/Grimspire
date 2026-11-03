# Cathedral traversal landmarks — K10–K13

Jarred requested the three reviewed cathedral shapes, LARGE, in the shared Forge Library, plus one dome. Standalone landmark terrain drafts, not variants of the existing modular kit. Exact documents, identities and hashes: `injection-manifest.json`. Generated sources, native layer PNGs and review PNGs accompany this handoff.

| Code | Piece | Art pixels | Baseline | Approx world pixels at 1.9 art/world |
|---|---|---|---|---|
| K10 | Collapsed nave wedge | 768 × 363 | 362 | 404 × 191 |
| K11 | Breached belfry / buttress | 576 × 524 | 523 | 303 × 276 |
| K12 | Fallen arch / choir loft | 768 × 364 | 363 | 404 × 192 |
| K13 | Shattered dome | 768 × 476 | 475 | 404 × 251 |

Scale 1, pixel_scale 12. Trooper reference height 50 art pixels: widths 11.5–15 troopers, heights 7–10.5 troopers. Use current runtime PX for exact world dimensions. Do not stretch into K08 boxes. Body, sparse magenta Emissive, matching-alpha dark Guts, transparent openings, bottom baseline. Six-step neutral stone ramp matches existing architecture. Generated sources interpreted at native sizes with nearest-neighbour sampling, binary alpha and palette/layer separation; final manual cluster cleanup pending. Native reviews show imported art, not battle tests. Guts is a dark material interpretation, not a detailed interior drawing.

## Why these exist

Jarred finds the drowned city visually excellent but too flat in play: isolated vertical slots encourage dropping explosives into compartments. These shapes introduce diagonal ascents, staggered landings and lower routes. The goal is interesting movement, shot angles and knockback. Faster rounds alone are insufficient. Standalone battles are already fun with friends; the short roguelike encounter loop is a separate unresolved design task.

## Ask (Claude)

Load exact manifest versions from the shared Library into a focused test scene. K10–K13 are NEW CODES: registration works, but slots and terrain placement/game support are your next work. Do not map them silently to existing modular families or assume seamless joints. Jarred requested your integration next; this save is not a live release.

**Preserve full multi-level collision.** Do NOT flatten pieces at one automatic `deck` row; that would erase slopes, platforms and upper walls. Notes include `state: broken`, but verify handling for new codes. Review masonry as solid, openings as air, thin railings as decoration, and glass collision separately. Body alpha includes decorative ribs and balustrades: pixel stamping alone does not guarantee good traversal. K12's upper diagonal may need jump-pack access. Support these on shore/foundations and keep lower exits above starting water, so the lower routes survive. Try one or two landmarks first. Preserve latest GV23 art, lighting and fixes.

Test stair climb/scramble limits, jump-pack clearance, lower headroom, varied spawn elevations, shot travel, knockback destinations, destruction and Guts. Terrain changes require seeded-map, sim/GV and determinism checks. Review fixed desktop and phone scenes with Jarred before release.

## Status

Drawn: four concepts. Saved: four Library drafts. Checked: native dimensions, binary alpha, matching Body/Guts alpha, Forge schema and old-index preservation. Full Forge results: `forge-tests.txt`. Not battle-tested, integrated, approved as exact collision/art, or live. Shared build, revisions and production game untouched. Prior assets and immutable history retained.
