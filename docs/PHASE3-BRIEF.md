# Phase 3 brief: set pieces and destruction

For ChatGPT, from Claude, 2 Nov 2026. Read [`WORLD-ART.md`](WORLD-ART.md) first (scale, bands, light rules, placement data, review checklist). This brief says what to draw first and exactly what the code needs from each piece.

Two pieces of work, in this order:
1. **Set pieces, first pass.** The generator marks sockets; set pieces snap into them.
2. **Destruction.** Pixel-art effects first, then broken art-grid craters and debris made of the stone.

Claude builds the sockets, the placement code, the set-piece release path in the Forge and all destruction code. ChatGPT supplies the art and the look targets below.

## Part 1: set pieces

### What the code will do
The map generator already knows where its towers, bridges, floating islands, facades and flat ground are. Claude turns those into **sockets**:

| Socket | Where it comes from | What sits there |
|---|---|---|
| `pinnacle` | Flat tops of towers, crenellated and broken crowns, pillar tops | Statues, finials |
| `ledge` | The outer edge of a flat run of terrain, with a drop beside it | Gargoyles leaning out over the drop |
| `ground` | Flat runs of terrain away from spawns and crate landings | Toppled statues, reliquaries, arches |
| `sump` | Low ground at or below the starting waterline | Half-sunk heads, pier pilings, wreckage |
| `hang` | Undersides of bridges, islands and arches | Banners, chains, censers |

A piece picks a socket by its `place` value, sits its baseline on the surface, and only lands where its `footprint` columns are fully supported and its `clear` headroom is free. The rising sump drowns sump pieces naturally, which is the point.

**First pass is decorative only** (`solid: none`): no collision, no GV change, and they don't block shots. Pieces that a blast reaches will break into debris (Part 2), so draw a **Guts** layer anyway.

### The first seven pieces
Redraw at **final size, scale 1**. The S01–S06 studies are 17–44 art px and read as ornaments; these are set pieces. A trooper is about 50 art px tall.

| # | Piece | Socket | Size (art px tall) | Notes |
|---|---|---|---|---|
| S01 | **Fallen saint head**, face up or tilted, crack through the brow | `sump` | 90–110 | Taller than the trooper beside it. Tide line about a third of the way up. `sink` 0.3–0.5 |
| S07 | **Saint on a pedestal**, praying or blessing, halo optional (halo can be emissive amber, small) | `pinnacle` | 70–100 | Pedestal footprint 20–40 columns wide, centred. Reads against the sky: strong silhouette, no interior noise |
| S03 | **Perched gargoyle**, leaning out, wings half open | `ledge` | 40–60 | Only the rear third rests on stone; the rest overhangs. Draw facing right; the game flips it |
| S06 | **Pier pilings**, two or three posts with a broken crossbeam and chain | `sump` | 60–100 | `sink` 0.4–0.7. Same tide line height as S01 |
| S08 | **Hanging banner**, long, torn hem, iconography in the cloth | `hang` | 60–120 | Cloth layer (greys, the game tints per faction). **Row 0 is the anchor**; set baseline to 0. Faction version near spawns, "None" grey elsewhere |
| S02 | **Toppled saint**, lying along the ground, arm raised or broken off, robe folds as big shapes | `ground` | 40–60 tall, 120–180 long | A long low silhouette troopers walk past. Footprint is most of its length, so it only lands on long flat runs. `weight` 0.4, `limit` 1 |
| C04 | **Promethium brazier**, replacing the promethium tank 1:1 (see below) | tank's spots | 34–40 | Iron bowl on a tripod or squat plinth, burning promethium. Emissive coals and flame, amber, animated 8–12 frames. Notes: `light: amber, 75` |

If one of these needs a different size to read, say so; size sets meaning more than exact numbers do.

### The brazier replaces the tank
Jarred's call: the promethium brazier takes the tank's place one for one. Same spots, same job: shoot it or blast it and it explodes and spills burning promethium. So it is a **gameplay item, not decoration**, and should read as one:
- A little bigger than the tank (21×28 now): about **28–32 wide, 34–40 tall**, baseline on the bottom row, scale 1.
- The brightest thing at its size: a lit bowl of fire you'd avoid standing next to. Strong silhouette, dark iron, all the colour in the emissive fire.
- Save it as a new version of **C04** (family `asset-c04`). Notes need only `light: amber, 75`; the game then lights it amber and flickers it like fire. Without that line it keeps the tank's yellow lamp light.
- Claude fits the hit area to the new art when it lands (a sim change, GV bump). It replaces the yellow-ring tank.

### Per piece, deliver
- Forge Library asset at scale 1, layers per `WORLD-ART.md` (Body, Emissive, Cloth, Guts).
- **Baseline** set in the Forge. For `hang`, baseline 0 (the top row).
- **Placement data in the asset notes**, exactly in this form so Claude can parse it:

```
place: sump
band: play
base: 104
footprint: 18–74
clear: 0
sink: 0.3–0.5
weight: 0.6
limit: 1
zones: any
faction: none
solid: none
flip: yes
light: none
```

- A review image beside a live trooper at game scale, on dark stone and near a light (as you've been doing).
- Hand cleanup pass: 2×2 clusters, no lone pixels, no full outline, colours from the shared ramps, set pieces one value step darker than terrain edges.

### What not to do
- No per-asset scale other than 1.
- No baked rims or highlights; the engine lights them.
- Don't paint water or reflections; the sump is code.
- Keep S05 (reliquary) for batch two.

## Part 2: destruction look targets

Claude draws effects procedurally at the art-pixel grid so they scale to any blast radius. What's needed from you is the **look**, not sprite sheets the game plays back.

### Deliver
1. **Stepped palettes**, 5–7 steps each, as hex, darkest to brightest:
   - Explosion core and fireball (white-hot to deep ember)
   - Fire and embers (matches braziers and burning ground)
   - Smoke (warm near the fire, cold charcoal as it rises)
   - Stone dust (from the wet stone ramp, lighter and drier)
   - Plasma (blue-white, for plasma weapons) and equipment red sparks
   - Scorch on cut stone (the crater rim, fresh to cooled)
2. **Reference flipbooks** at true art-pixel size, 1× (PNG strip or GIF, plus frame timing):
   - Small blast, about 24 art px across, 8–10 frames
   - Large blast, about 64 art px across, 10–14 frames
   - Smoke puff rising and thinning, 10–12 frames
   - Dust burst off broken stone, 6–8 frames
   - Fire tongue loop, 6–8 frames

   Use dithering for falloff, never smooth gradients. Show where the soft light glow would be as a separate layer or a note; the glow stays soft in game, the shapes stay pixel.
3. **One crater mock-up**: a still of a blast hole in the current terrain at 1×, broken outline snapped to art pixels, stepped edge, a few loose fragments and short cracks off the rim, scorch from your palette. This is the target for the crater rewrite.
4. **One seamless stone guts tile**, 48×48 art px: what's inside the stone when a blast bites in (hollow masonry, rebar, rubble). Shows inside craters.

No debris art needed: debris is cut from the pixels the blast destroyed, so a broken saint sheds pieces of saint.

## Order and handoff
1. C04 brazier and S01, S07, S03 first, then S06, S08, S02.
2. Palettes and the small-blast flipbook next; the rest of Part 2 after.
3. Save in the Forge Library; don't Go live. Add a `LOG.md` entry per batch with asset ids and an **Ask (Claude):** line.

Claude will test placements with the existing S01–S06 studies as stand-ins until the redraws land, then swap them in.

## Part 3: architecture kit for the drowned district (added 2 Nov, from the `phase3` spike)

The spike on `phase3` (`#drowned`, or the TEST panel's "Drowned map") builds a fixed district standing in high water, the composition of the interim North Star. Its buildings are code placeholders: flat stone shapes with cut arches. They are the pieces to draw. The game stamps them into the destructible terrain, so each needs a **Guts** layer and a clean silhouette (no thin spikes a single shot erases).

Draw at scale 1 on the art grid (1.9 art px per world px). Sizes below are art px. Keep the neutral stone ramp; all colour is emissive (window glass) or comes from the engine's light. Each piece tiles or stacks cleanly with the others at the marked joints.

| Code | Piece | Size (w × h) | Notes |
|---|---|---|---|
| K01 | Tower shaft segment | 90–120 × 100 | Stackable vertically (top and bottom rows match). Two or three lancet windows, some lit magenta in the Emissive layer, some dark. Buttress option as a variant. |
| K02 | Spire cap | 100–120 × 160–220 | Sits on K01. Crockets up the edges, finial and cross at the tip. |
| K03 | Crenellated crown | 100–120 × 40 | Sits on K01. Corner pinnacles. Flat walkable top between merlons. |
| K04 | Broken crown | 100–120 × 40–80 | Sits on K01. Jagged, chunky breaks. |
| K05 | Bridge span | 150–200 × 80 | Deck with balustrade, one pointed arch below, joins at both ends to K06 or a tower. Tiles horizontally. |
| K06 | Bridge pier | 40 × 200 | Runs down into the water; tiles vertically, the bottom will be underwater. |
| K07 | Nave wall | 240–480 × 300 | Arcade of tall pointed arches (open, see through), clerestory windows above, crenellated walkway on top. Tiles horizontally in 120 px steps. |
| K08 | Cathedral front | 480–520 × 360 | Gable with a big rose window (glass in Emissive, magenta), two flanking lancets, a walkway on top. The landmark of the district. |
| K09 | Pier / jetty | 240–400 × 30 | Low timber-and-iron platform at the waterline with posts into the water; tiles horizontally. Where the fallen heads sit. |

**Variants are welcome** once the first of each piece exists: name them K01a, K01b, K01c and so on (a separate drawing of the same piece, not a new version of it). Variants of one piece share its size, joints and footprint, so any of them fits wherever the piece goes; only the look changes (window layout, damage, a buttress, a collapsed corner). Optional `weight:` and `state: intact | broken` in the notes let the generator keep rare ones rare and put broken tops higher up. Start with one of each; then 2–3 variants for the pieces that repeat most (K01 tower shaft, K05 bridge span, K07 nave wall). Claude allows the letter suffix in the Forge when the stamping code goes in.

Order: K08 and K01–K03 first (they define the silhouette), then K05–K07, then K04 and K09. Save each in the Forge Library under its code with a short note on its joints; there is no K slot in the Forge yet, and Claude adds the stamping code when the first pieces land. A side-by-side with the spike screenshot is the review.

The skyline behind is now drawn by code (gothic towers, cathedral fronts with rose windows, arcades, magenta windows), so no background art is needed for now.

## Part 4: decoration off the action plane, and rocky ground (added 2 Nov)

The `phase3` build now has depth on both sides of the play layer (Jarred's call, after the crimson concept): the skyline stands on its own water receding to a horizon above the waterline, foreground wreckage stands in the water nearer the camera, and set pieces appear hazed and half-sunk in the background water. All of these are code placeholders except the background set pieces, which reuse the Forge art.

| Code | Piece | Band | Size (art px) | Notes |
|---|---|---|---|---|
| D01–D06 | Foreground wreckage, six variants: broken column, fallen masonry slab, half-sunk arch, mooring post with chain, a toppled statue's hand or shoulder, a capsized boat or barge rib | `foreground` | 40–220 wide, 30–160 tall | Near-black silhouettes only (flat dark body, no interior detail needed); the game adds a cold top edge and the reflection. Readable at a glance, never busy. The bottom third goes under the water. |
| R01–R04 | Rock outcrops and shore, four variants | `play` | 120–340 wide, 60–180 tall | Broken rock (not masonry) standing out of the water, flat-ish tops troopers can stand on, a Guts layer. Tiles at the sides so two can join into a longer shore. |
| B01–B03 | Background silhouettes that read at a distance: a colossal saint in the water, a drowned dome, a broken bridge spanning the horizon | `back` | 200–500 wide | Flat silhouettes in one value, with a few lit windows in the Emissive layer (magenta, some cyan). The game hazes them. |

Order: D01–D06 first (cheap, big payoff), then R01–R04, then B01–B03. Save in the Forge Library with the band in the notes (`band: foreground`, `band: back`); Claude wires them in when they land. The crimson concept is a mood reference; the shipping grade stays as tested unless Jarred asks for a crimson variant.
