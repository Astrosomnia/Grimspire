# Building parts contract (first batch)

What ChatGPT draws for the building system, and the rules every part follows so the generator can snap them together. Written by Claude from the building lab's real cases (`experiments/building-lab.html`), 17 Nov 2026. Plan: [`BUILDING-SYSTEM.md`](BUILDING-SYSTEM.md). Long-term wish list: [`BUILDING-PARTS-CATALOGUE.md`](BUILDING-PARTS-CATALOGUE.md). This replaces the part list in [`BAY-KIT-BRIEF.md`](BAY-KIT-BRIEF.md).

**Decided:** storey height **128** (Jarred, 16 Nov). Taller rooms are stacks of storeys (double-height halls, later naves), never a different storey size.

All sizes are **art px** at kit density (1×: a trooper is about 50 art px; 1 art px ≈ 0.54 game px).

## 1. The grid

- **Bay: 128 wide × 128 tall.** One storey of one span. Bay lines run through the centre of each pier.
- **Pier: 24 wide**, centred on a bay line (12 each side). Full storey tall.
- **Slab: 16 thick**, at the bottom of each bay; its top is the floor. Slabs run pier centre to pier centre and tuck under the pier.
- **Clear room:** 104 wide (pier face to pier face) × 112 tall (slab top to the slab above).
- **Courses:** masonry courses are 16 tall, so a storey is 8 courses and every part's joints line up with its neighbours. Joints land on bay lines.

## 2. Hard rules (the game's physics depends on these)

These come from the trooper's real movement: step-up 10 game px (18 art), head check 18 game px (33 art), trooper 27 game px (50 art).

- **Floors are flat.** A slab top is one straight line across the bay. Nothing on a walking surface stands taller than **16 art** (a crenel or a lip) unless it's meant to block.
- **Headroom.** Nothing hangs lower than **34 art above a floor** where a trooper should walk, except at the pier faces (the arch span below).
- **Doorways: 84 tall** from floor top (45 game px), the full pier width, round or pointed top. The sill is the floor: no step.
- **Windows** (in a pier or outer wall): sill **30** above the floor, opening **56** tall (Jarred, 17 Nov: windows are firing positions). Standing close, the muzzle reaches past the wall, so level and slightly downward shots go out; 20 felt too low. A trooper steps up at most 18, so they can't walk out, only jump.
- **Body pixels are collision.** Inside the Body, decorate freely. The outline of floors, openings and walking surfaces must match the sizes here to within 2 px.
- **Openings show interior, never more facade.** Behind every window, door and arcade: the Back (a dark room, rubble, a vault) or lit glass (solid in the Body, lit in Emissive).

## 3. Layers

Per [`WORLD-ART.md`](WORLD-ART.md): **Body** (flat, dark, collision), **Height** (depth planes), **Back** where the part has an inside, **Emissive** only for real lights, **Cloth** for banners (grey; the game colours it), **Guts** for anything destructible (all structural parts). Same canvas and alignment across layers.

## 4. Anchors and canvas

- **Bay parts** (slab, back bay, arch span, stair): canvas 128 wide, anchored at the **bottom-left bay corner**.
- **Pier parts:** canvas 24 wide (plus overhang), anchored at the **bottom centre** of the pier.
- **Overhang:** draw anything that sticks out (corbels, crockets, gargoyles, broken ends) inside a margin of up to 32 px around the cell. Note the margin in the Forge draft so the anchor stays exact.
- **Repeats** (ladder rung, crenel, bridge span) say their repeat length.

## 5. First batch (about 30 parts, in order)

**Priority A: enough to skin a whole building in the lab** (about 22 images with variants). Start here; the lab's Skinned toggle can go on once these exist.

| ID | Part | Size | Notes / neighbour case |
|---|---|---|---|
| B01 | Pier, outer wall | 24 × 128 | Exposed on one side. 3 variants |
| B02 | Pier, inner (between two rooms) | 24 × 128 | Both sides inside. 2 variants |
| B03 | Pier with doorway | 24 × 128 | 84 opening at the bottom. Inner and outer variants |
| B04 | Pier with window | 24 × 128 | 30 sill, 56 opening. Lancet and round-headed |
| B05 | Arcade pier (lintel only) | 24 × 128 | Opening 86 tall, 26 lintel left at the top. Ground floors, cloisters |
| B06 | Floor slab | 128 × 16 | Repeats bay to bay. 2 variants |
| B07 | Slab, finished end | 16 × 16 | Where a slab stops at a stairwell, hall or hole |
| B08 | Arch span (under a slab) | 104 × 34 | Hangs from the slab between pier faces: 34 deep at the piers, about 6 in the middle. 2 variants |
| B09 | Back bay, plain | 128 × 128 | The rear wall of a room. 2 variants |
| B10 | Back bay, lancet window | 128 × 128 | 32 × 62 opening, bottom 30 above the floor. Windows align up a column. 2 variants |
| B11 | Back bay, arcade | 128 × 128 | Open arches to the Far Back; galleries and ground floors |
| B12 | Ground plinth | 128 × 48 + below | The ground-floor slab and foundation; extends down into the ground. 2 variants |

**Priority B: circulation and roofs.**

| ID | Part | Size | Notes |
|---|---|---|---|
| B13 | Stair flight | 128 × 128 | 8 risers of 16, thin (about 20 thick) with open space under it. Foot at a pier face, top lands on the next bay's slab. Flips for direction |
| B14 | Ladder rung | 26 × 6 | Repeat. Rungs sit 50–80 apart (the game's climb needs 27–44 game px); the top rung is flush with the floor it reaches |
| B15 | Ladder rails | 26 × 128 | Back layer, repeat per storey |
| B16 | Ladder hole edge | 32 × 16 | The cut in a slab a ladder passes through |
| B17 | Parapet end | 24 × 26 | On an exposed roof edge |
| B18 | Crenellation | 30 repeat, 16 tall | Merlons 15 wide; 16 tall so a trooper can still step over |
| B19 | Gable roof | 1–3 bays wide | About 0.42 of its width tall. One per width |
| B20 | Spire (one-bay tower) | 152 × about 200 | With corner pinnacles |
| B21 | Broken roof edge | 128 wide | Ragged top of a ruined storey. 2 variants |

**Priority C: ruin, Back variety, outside and bridges.**

| ID | Part | Size | Notes |
|---|---|---|---|
| B22 | Broken pier top | 24 × 64 | A pier sheared off partway |
| B23 | Broken slab end | 32 × 16 | Flips left/right |
| B24 | Rubble heap | 64 × 28 | Sits on a floor, half a bay wide. 2 variants |
| B25 | Back bay, vault | 128 × 128 | Ribs, for a top storey or chapel |
| B26 | Back bay, crypt | 128 × 128 | Two small low arches, ground floor |
| B27 | Broken rear skyline | 128 wide | The rear wall's ragged top when the front is sheared |
| B28 | Back column | 18 × 128 | Behind an open inner pier, so the room reads as one space |
| B29 | Far Back strip | 128 × 128 | Colonnade, distant vault, lit window: 3 variants. Lighter, hazier, sky-tinted |
| B30 | Bridge deck span | 128 × 16 | Repeat between buildings, deck at floor level |
| B31 | Bridge pier + arch | 28 wide, to ground | Arch under the deck, rise up to 46 |
| B32 | Outside stair ramp | 16 tread × 15 riser | Stepped mass from the ground up to an upper door |
| B33 | Corbel | 12 × 16 | Under an upper floor on an outer wall |

**Ornaments (any time):** gargoyle (roof corner), banner (Cloth, hangs from a slab), brazier (Emissive), statue niche (Back). These already exist in some form in the kit; reuse them where they fit.

## 6. Art style

**The benchmark is the original K08 cathedral front and the original S01 fallen saint head** (Jarred, 16 Nov): strong, heavy lines, a scannable shape, chunky 1× pixels, about six tones in flat blocks, shading by planes. Full bar: [`ART-READABILITY.md`](ART-READABILITY.md).

- **Kit tier, most restraint.** These parts repeat on every building, so they're the plainest things in the game. Smallest visible feature about 2 game px (4 art). 5–7 tones per material. No mortar on every course, no per-pixel grain.
- **Repetition is the enemy.** A repeating part has no single memorable crack or chip, or you'll see it 40 times. Put character in the variants (2–3 per part, standing practice) and the ruin pieces.
- **Big forms first.** A pier reads as a pier from across the map: its base, its shaft, its capital. Detail goes where it earns attention: doorways, window heads, capitals.
- **Flat paint, no baked light.** No painted rims or highlights; the lit look adds those from the sky, neon and blasts. Dark navy stone, the kit's tone ramp (masonry about RGB 28/34/43).
- **Heights as depth planes:** pier faces and ribs high, wall faces middle, window and door reveals low. Smooth within each plane. Not a copy of the drawing's brightness.
- **Back is a step darker and simpler** than the Body: the inside of the building, never more facade. Far Back lighter and hazier still, toward the sky.
- **Seams must disappear.** Courses line up at 16; joints land on bay lines; a pier and the slab beside it share the same stone. Test two of each part side by side before saving.
- **Judge at play zoom next to terrain**, in the lab's Skinned view once it exists, not as a sprite.

## 7. Delivery

- Draw each part as a Forge draft, named by its ID (`B01 Pier, outer wall a`).
- Export the PNGs to `art/experiments/bay-kit/`, one file per layer: `B01a_body.png`, `B01a_height.png`, `B01a_back.png`, and so on.
- Log a line in `LOG.md` for each batch. Claude wires the Skinned toggle in the lab as soon as Priority A lands, and parts not drawn yet fall back to their placeholder shapes.
- Questions about a case not covered here go in the log as an Ask (Claude).
