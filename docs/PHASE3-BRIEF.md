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
| `ground` | Flat runs of terrain away from spawns and crate landings | Props, braziers, toppled statues |
| `sump` | Low ground at or below the starting waterline | Half-sunk heads, pier pilings, wreckage |
| `hang` | Undersides of bridges, islands and arches | Banners, chains, censers |

A piece picks a socket by its `place` value, sits its baseline on the surface, and only lands where its `footprint` columns are fully supported and its `clear` headroom is free. The rising sump drowns sump pieces naturally, which is the point.

**First pass is decorative only** (`solid: none`): no collision, no GV change, and they don't block shots. Pieces that a blast reaches will break into debris (Part 2), so draw a **Guts** layer anyway.

### The first six pieces
Redraw at **final size, scale 1**. The S01–S06 studies are 17–44 art px and read as ornaments; these are set pieces. A trooper is about 50 art px tall.

| # | Piece | Socket | Size (art px tall) | Notes |
|---|---|---|---|---|
| S01 | **Fallen saint head**, face up or tilted, crack through the brow | `sump` | 90–110 | Taller than the trooper beside it. Tide line about a third of the way up. `sink` 0.3–0.5 |
| S07 | **Saint on a pedestal**, praying or blessing, halo optional (halo can be emissive amber, small) | `pinnacle` | 70–100 | Pedestal footprint 20–40 columns wide, centred. Reads against the sky: strong silhouette, no interior noise |
| S03 | **Perched gargoyle**, leaning out, wings half open | `ledge` | 40–60 | Only the rear third rests on stone; the rest overhangs. Draw facing right; the game flips it |
| S06 | **Pier pilings**, two or three posts with a broken crossbeam and chain | `sump` | 60–100 | `sink` 0.4–0.7. Same tide line height as S01 |
| S08 | **Hanging banner**, long, torn hem, iconography in the cloth | `hang` | 60–120 | Cloth layer (greys, the game tints per faction). **Row 0 is the anchor**; set baseline to 0. Faction version near spawns, "None" grey elsewhere |
| L01 | **Brazier**, iron bowl on a tripod, coals and flame | `ground` | 22–32 | Emissive coals and flame (amber, animated 8–12 frames is plenty). `light: amber, radius 70` |

If one of these needs a different size to read, say so; size sets meaning more than exact numbers do.

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
- Keep S02 (toppled saint) and S05 (reliquary) for batch two.

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
1. S01, S07, S03 first (one each for `sump`, `pinnacle`, `ledge`), then S06, S08, L01.
2. Palettes and the small-blast flipbook next; the rest of Part 2 after.
3. Save in the Forge Library; don't Go live. Add a `LOG.md` entry per batch with asset ids and an **Ask (Claude):** line.

Claude will test placements with the existing S01–S06 studies as stand-ins until the redraws land, then swap them in.
