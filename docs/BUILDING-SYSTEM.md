# Building system: rules + parts (plan)

16 Nov 2026 · Jarred and Claude. Supersedes the scope of [`BAY-KIT-BRIEF.md`](BAY-KIT-BRIEF.md); its grid and first parts list still stand.

## Why
Hand-drawn set pieces are slow, drift in style, can't find room on maps, and make solid lumps everyone stands on top of. The procedural buildings already give what matters for play (rooms, floors, stairs, a back wall, cover inside, destruction that just works, fits any map) but look like flat brick slabs. Plan: **the generator decides the space, a library of small drawn parts decides the look.** A handful of big hand-drawn landmarks (fallen arch, dome, colossal heads) stay on top as rare wow moments.

North star: Tiny Glade. Place a rough shape and the rules work out arches, roofs, stairs and trim so it always looks considered.

It serves every direction the game might take (friends mode, the roguelike climb, an all-interior castle level), and small parts are far easier to keep on the art bar ([`ART-READABILITY.md`](ART-READABILITY.md)) than big pieces.

## Reference: Dead Cells' hybrid approach
Shared by Jarred, 16 Nov ([article](https://deepnight.net/tutorial/the-level-design-of-dead-cells-a-hybrid-approach/), by its lead designer). Fixed world frame; hand-made room "tiles" with variations, each with a purpose and belonging to one biome; a concept graph per biome (entrance, exit, special rooms, length, how labyrinthine); the generator tries random rooms per graph node and rejects ones that don't fit; pacing with peaks and breaks. Their lesson: pure procedural hurt consistency; hand-authored constraints kept identity and still gave variety.

What we take from it: a middle layer between parts and the generator.
1. **Parts:** as below.
2. **Room templates:** small hand-designed rooms with variation slots (stair hall, chapel, belfry crown, bridge-end gatehouse, crypt). The playground's lock-as-template is how we author them: generate, keep the good ones, refine.
3. **Theme graphs:** one per level theme (drowned city, castle interior, spire climb). How many buildings, how linked, where the landmark sits, how open or cramped. Same parts, different feel.
Plus pacing: alternate open, exposed stretches with tight interior fights.

## The generator: passes with intent
A building is a grid of bays (one span × one storey, 128 art px, see the bay-kit brief). Each pass reads what's already there and rolls weighted choices. Every rule and percentage lives in one data table so it can be tuned without touching code.

1. **Footprint:** bays wide from the space available; the ground storey steps to follow terrain.
2. **Massing:** overall type: hall, keep, twin towers, stepped, tower-and-wing, cloister. Rules like "end bay: 40% rises two more storeys and becomes a tower".
3. **Floors and roofs:** each storey gets a floor; a tall bay has a chance to become a double-height hall with a balcony; each top gets a roof type (parapet, crenellations, gable, spire, broken).
4. **Circulation:** stairs, ladders, drop holes. A check guarantees every floor is reachable with headroom for a jump.
5. **Openings:** windows aligned across storeys, doors at ground, arcades in halls. Shots must be able to get in: no sealed rooms.
6. **Rooms and dressing:** partitions with doorways; each room gets a purpose (chapel, stair hall, crypt) that picks its Back and ornaments (statue niche, gargoyles on corners, braziers, banners).
7. **Bridges and connectors** (after the buildings): find gaps where a doorway or floor lines up across to another building or rock; span count from the width, piers past a set length; ruin rolls (missing middle → two stubs and a jumpable gap, or a collapse into rubble); high walkways between towers, flying buttresses, chains or rope bridges, ladders. Connectors only link reachable floors, so every bridge is a route.
8. **Ruin:** knock out slabs, shear tops, collapse corners, rubble under breaks; reachability runs again so a ruined building is still a level.

**Artillery rules from day one:** halls tall enough for arcs, ceilings that can be blown through, openings for shots to enter, destruction that stays readable.

**Style references:** the existing custom buildings (K08 cathedral front, K10 nave, K11 belfry, K12 arch, K13 dome, K26 vault bay) set proportions, rhythms and ornament. Their vocabulary becomes rules, so generated buildings sit naturally next to them.

## Depth layers
- **Body:** stone you stand on and hide behind.
- **Back (near):** the room's rear wall, darker, never blocks.
- **Far Back:** what's visible through openings in the Back: columns, a distant vault, a lit window in another room. Darker still, non-blocking. This is what makes interiors read as spaces, not boxes.

## Parts (bay kit, widened)
On the 128 px bay grid, game scale 1 (normal density), at the art bar: flat tones, strong edges, smallest feature about 2 game pixels.

- **Structure:** piers and columns (2–3 variants), floor slab and slab edge, arch span under a slab, stair flight, ladder, parapet, crenellations, gable, spire cap, broken pier top, broken slab end, rubble heap.
- **Openings:** frames for arch, lancet, round window, door, arcade bay.
- **Back types:** brick wall, vault ribs, arcade, rubble, lit window, broken rear skyline.
- **Far Back:** colonnade, distant vault, window to another room.
- **Ornaments:** gargoyle (corner), statue in niche, banner, brazier, corbels under floors.
- **Bridges:** abutment into rock, end meeting a doorway, broken stub, spans (plain, arched, ribbed, iron truss, damaged balustrade), pier (on rock / out of water), middle piece (chapel, gatehouse, lamp post), walkway, flying buttress, chain or rope bridge.

## Playground (Claude builds)
`experiments/building-lab.html`, standalone, no game code touched until the rules are worth it.

- 24 buildings at a time, drawn in the play-diagram style (flat shapes, walkable route marked, a trooper for scale), so the structure is judged, not the art.
- **Keep / cut** on each. The tool records which rule choices each building used; after a batch it shifts the weights toward kept, away from cut. The weight table is visible and has sliders for manual overrides.
- **Lock** a building you love: it becomes a fixed template the generator can reuse.
- **Export** the tuned rule table straight into the game.
- Later: sketch a rough layout and let the rules dress it (Tiny Glade-style authoring for key levels and set pieces).

## Order
1. Claude: generator + playground on placeholder shapes.
2. ChatGPT, in parallel: the parts above, starting with the 14 in the bay-kit brief, then openings, Back and Far Back types, ornaments, bridge parts. Each judged at play zoom before it's used.
3. Join them: skin the tuned generator with the parts, in the game, and play.
4. Then an all-interior castle level from the same rules plus a few castle-only ones.
5. A small number of big landmark set pieces stay hand-drawn.

## Risks
- **Time sink:** generators are endlessly tweakable. Judge by play: drop the rules into the game early and play rounds before polishing.
- **Art drift:** parts are held to the art bar like everything else.
