# Building kit — Batch 2 and 2b / 17 November 2026

52 new images across 34 part IDs, plus five additional rear-wall variants (BK09c/d, BK10c/d, BK11b). Batch 2: BK40–BK44, BK50–BK55, BK60–BK65, BK70–BK75, BK80–BK81. Batch 2b: BK90–BK98. Width alternatives and multi-part sets are stored as immutable versions in one Library asset per part ID. **Read every entry in `published-manifest.json`, not only each family's current version.**

This extends Priority A (BK01–BK12) and adds five rear walls under new variant letters, preserving every existing wall. No game code, renderer, live payload or shared release state changes.

## Art direction

Jarred authorised 8–12 tones and, after the early stair previews, asked for a little more detail closer to the original S01 saint head. The final direction uses S01 as an actual image reference for carved planes, layered mouldings, deep panels and architectural joints. The early stripped-back stairs and gables were replaced before saving. Important silhouettes get more attention than repeated deck/post surfaces.

Final drawings are authored directly at native 1× in `native.py`: no source raster is read, sampled or resized. Generated studies supplied composition references only. Flat navy material colours, centred channels and symmetric recesses avoid painted directional light. The actual mouldings, ribs and recessed panels have corresponding depth in Height. Bodies use a subset of the shared twelve-tone ramp, with base RGB28/34/43. Guts use coarser structural cores; glass has separate emission.

All 52 new drawings pass the exact current `tools/art_check.py` (0 warns, 0 fails). These metrics support visual review; they do not replace an in-game lighting check. The five additional rear walls retain original window/arcade transparency, use quiet native coursing and stay darker than foreground stone. Every component is given a unique terminal variant letter so `bk_import.py` retains the whole set. See the manifest for component-to-letter mapping.

## How to export

Each manifest item gives exact `asset_id`, `version_id`, immutable `library_path`, hash, canvas and geometric anchor. Versions may be width variants OR separate components; the `id` distinguishes these. For example all three BK97 versions (jib, chain, platform) are needed to assemble the crane. A Library current-version export alone would show only the platform.

Coordinates use right/bottom-exclusive bounds. Geometric anchors can sit on the canvas edge; the Forge pivot is clipped to the last in-canvas pixel. Geometry/masks are at native1×, game_scale1, pixel_scale12. No art is approved or marked ready.

### Stairs and roofs

- BK40:128×128 switchback. Two4×16-riser flights,32 tread,16 structural thickness; lower footleft128, landingright64, upper endleft0. Decorative newels in Back. Actual movement around the return needs the generator's new switchback rule.
- BK41/BK42:128×128,8×16 risers. BK41 has a32-wide through-gap x48–80. BK42 cantilever corbel decoration is Back; foreground stair20 thick.
- BK43:128×128; spiral art Back, Body ledges16 deep at left y112 and right y48. Repeat128,64 vertical separation. BK44:32×16 hatch with clear24-wide centre; raised lid Back.
- BK50:128×64 and256×128, thin16 roof with slope under40degrees. No incidental source-image pillars are included in collision.
- BK51:128×54,256×108,384×162 native gables. BK52:128×64 and256×112 broken gables with48/64-wide drop-through gaps. Do not stretch one width into another.
- BK53:128×104 cupola with rear arcade; BK54:128×128 belfry,16-wide piers and floor at112; bell in Back, open central shot corridor. BK55:128×32 low terrace edge,16-thick slab with at most16 of parapet above.

### Outside and silhouette

- BK60:64×128, wall24 plus balcony40. Window y26–82, floor112, balcony top at sill82. BK61:24×128; shots-only slot12 high at y76–88. This is a side-view THROUGH wall cut, not a12-wide hole surrounded by solid collision.
- BK62:128×128 grand entrance,80-wide pointed opening,84 high at crown, flat floor y112. BK63:40×128/256/384 buttresses, native drawings per height;16px step cadence on taper. These need the new generator rule and actual reachability check, not an assertion that a narrow buttress is a walkable staircase.
- BK64:48×128 corbelled turret; left joins upper opening; rear interior in Back. BK65:128×64 gallery deck/corbels, deck16 thick. The contract's “40 out” describes projection into/out of the facade; the sprite is its side elevation.
- BK90: deck32×16 repeat, brace64×64, lamp16×48. Assemble70–150-long deck using repeats and an endpoint crop; brace beneath; lamp at free end. **Lamp is decorative/noncolliding:** its Body glass exists to support Emissive, not to block bullets.
- BK91:32×24 snapped endpoint; attach to intact repeat. BK92:36×32 bracket and48×16 slab extension, carrying the wall36 outward. BK93:56×16 setback ledge, flat top/drip edge.
- BK94:58×180 quarter-round apse, matching the lab. Floor at122; cap outer radius58/inner44 centred(0,58); wall14; right firing slot y52–92,40 high with sill30. Foundation extends58 belowfloor; crop/bury to terrain. Left opens to ground door. Back is a dark nook.
- BK95:128/160×64 flying arches,16 thick and48 vertical drop, plus28×128 repeatable free pier. Highleft origin is anchor(0,0). The lab chooses a terrain-dependent drop; map/crop the material along its curve or select a suitable span, do not blindly stretch the paint. Join arch and pier at their top surfaces.
- BK96: deck64×8 (Body), post12×128 and brace64×128 (Back), ladder26×128 (Body rungs/Back rails). Rungs at0 and64,6 high; repeat128 produces64 spacing with no doubled bottom rung. Use ladder/rung runtime semantics, with top rung flush to reached floor. Stacks up to3 storeys.
- BK97: jib80×48 and chain8×128 in Back; platform48×8 in Body. Repeat/crop chain to required height. The lab's overhead jib/chain are visual, not collision.
- BK98: **44×60 canvas**, because the actual lab shape has26 of railing above floor,12 of deck and22 of corbel below. Anchor(0,26) at floor. Railing Back; deck/corbel Body. The brief's44×26 is the railing itself, not the full combined bounds.

### Interiors, ruin and bridges

- BK70:128×128 rear chapel wall. The rose disc is solid Body with Height and Emissive, and its wall is Back. **Render the entire asset in the rear/background system; do not add the Body disc to foreground collision.** This is the brief's “Body of the Back” glass case. Needs Claude's explicit layer-role mapping.
- BK71/BK72:128×128 Back-only shelves/niches and collapsed rear wall, respectively; transparent Body PNG satisfies the Forge schema. No Height/Guts for noncolliding Back-only parts.
- BK73:96×24 fallen column cover; BK74:24×128 pier with a6px diagonal through-crack; BK75:128×28 canvas preserves16 slab thickness plus12 centre dip. Its endpoints remain at y0; never squash to16 totalheight.
- BK80: planks32×6 repeat,16×64 endpost and32×20 Back rope. BK81:128×128 covered bridge; deck16, sideposts12, roof16; central corridor y28–112 clear. Rear brace is Back.

## Validation and limits

`validation.json` records actual PNG/schema checks, binary alpha, canvas dimensions, scale1, draft flags, pure-grey Height and exact Body/Height/Guts masks,12-tone cap, distinct image data, horizontal repeat seams, flat decks, stair gap/risers, hatch/window/slit openings, belfry/bridge headroom,12px slab dip, apse firing slit,64px rung spacing and Emissive-on-solid-Body registration.

The Forge suite covers test/back/height/catalog after building. Contact sheets and the combined roof/silhouette assembly are raw-layer visual proofs beside a terrain swatch and50-art-pixel scale figure. They are **not** a game shader, movement, shot or destruction test. New generator rules and compositing roles are Claude's integration work; the brief already marks these G/N. All drawings remain drafts awaiting that review.

Nothing in this delivery is released to the live game. The accompanying shared-log entry asks Claude to export the full manifest into Skinned, with explicit attention to rear-only rose/lamp rendering, variable-span flying arches, switchback traversal and the combined bounds noted above.

Additional rear walls are BK09c/d, BK10c/d and BK11b. Jarred explicitly requested that prior walls remain available; importer-key checks confirm all 57 additions have new keys and shadow no old variant. The 52 batch drawings pass readability; rear additions have three passes and two warnings (BK10c/d, edge-light metric 28.8, detail 0.005, four colours). Their material fills are flat and unlit; the original cutout masks are retained. These two need review in Skinned; no readability fails are present.
