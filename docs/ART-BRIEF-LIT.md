# Art brief: the lit look (big push)

For ChatGPT, from Claude and Jarred, 10 Nov 2026. This replaces nothing in [`ART-DIRECTION.md`](ART-DIRECTION.md) or [`WORLD-ART.md`](WORLD-ART.md). It adds what the new renderer needs, and lists the art for one large push that Claude can integrate cheaply.

## What changed
The game now has a lit mode (branch `lit`, add `#lit` to the address). A shader under the game draws the sky, water, haze and all lighting. It lights every pixel of stone from the moon, the lamps, fire, blasts and the cyan glow off the water, with shadow and direction. Troopers, props and effects go through the same light. Blast holes are now jagged, with lit broken edges and embers along the true edge.

What this means for art:
- **Light is no longer painted.** It never was meant to be; now it's enforced. A painted highlight or rim will fight the real light and look wrong as soon as anything moves.
- **The shader guesses depth from brightness.** Today it reads each pixel's brightness as a rough height, which is why the stone looks embossed. A real height map per asset (below) is the single biggest quality jump available.
- **Dark art is a problem now.** The shader darkens what isn't lit. Art drawn near-black, like the current kit, goes muddy and needs a code lift to stay readable. Draw at mid value and let the light do the darkening.

## Rules for every asset in this push

### Pixel density: 2×
- Draw everything at **twice today's density**: about **3.7 art px per world px**, not 1.85. A trooper is about 100 art px tall instead of 50.
- In the Forge, set the asset's **game scale to 0.5**, and 0.6 for weapons (today's 1.2× halved). The game already reads per-asset scale, so no code change is needed for slots that respect it.
- Keep 12 source px per art px; the art canvas is simply bigger.
- Pixel craft rules still hold: clusters of at least 2×2, no lone pixels except deliberate glints, judge at game size on a phone.

### Layers
| Layer | What goes on it | Notes |
|---|---|---|
| **Body** | The object, flat, at **mid value** | No light, rims, highlights, cast shadows or outlines |
| **Height** (new) | Greyscale, same canvas as Body | White is nearest the viewer, black is deepest. Stone faces light; mortar, cracks and recesses dark; carved detail in between. Smooth gradients on curved forms (heads, columns), hard steps on cut stone |
| **Emissive** | Only real light sources | Windows, lamps, visors, status lights, glyphs. Saturated and bright; it blooms |
| **Cloth** | Cloaks, banners, tabards | Greys, as now; mid grey 128 becomes the faction's cloth colour |
| **Trim** | Faction marks | Neutral grey, as now |
| **Guts** | What's inside when a blast bites in | Rubble, rebar, hollow stone. Every destructible piece needs it |

**Height layer:** until Claude adds a Height layer to the Forge, export each height map as a separate PNG named `<CODE>.height.png` at the Body's size (one per frame: `<CODE>.f2.height.png`), and put them in `art/incoming/height/` on `art/weapon-lab`. Claude wires them in.

### Value and colour
- **Stone, iron, bone:** mid values, near-neutral and slightly cool. Aim for body brightness of roughly 90–150 out of 255. Not near-black.
- **No colour on objects except:** faction cloth (on the Cloth layer), real lights (on Emissive), faction marks (on Trim). Magenta and cyan come from the light, not from the paint.
- **Material ramps:** use the shared ramps in `WORLD-ART.md` (wet stone, iron, bone, rust, wax, cloth), shifted up so they centre on mid value.
- **Emissive colours carry meaning:** faction neon only on faction things; true red for equipment warnings; amber for fire, candles and sodium lamps; cool white for windows.

### Seams and joins
The game stamps kit pieces next to each other and runs one shared brick texture over flat stone. To make pieces meet without seams:
- **Course height:** stone courses about 26 art px tall at 2×, so drawn brickwork lines up with the generated masonry.
- **Join edges** on a 32 art px grid. Tops of walkable pieces are flat and level at the deck row.
- **Wear at the edges, clean in the middle:** chips and cracks near joins hide the seam; the middle stays calm.
- **Tide line:** pieces that reach the water get a wet band and tide line at the same height, about 22 world px above the waterline (about 80 art px at 2×).

### Leave these to the engine
Sky, moon glow, haze, water, reflections, rim light, light colour, bloom, fire flicker, embers, sparks, smoke, scorch, depth blur. Don't paint any of them into sprites.

## Deliverables
In priority order. Codes are existing Forge slots unless marked **new**. Each line notes how cheaply it integrates.

### 1. Terrain kit at 2× with height (biggest visual win)
Replace in place; keep the codes, deck rows and variants.
- **K01** tower shaft, stackable lancets (and K01a–d)
- **K02** tower spire
- **K04** broken tower crown
- **K05** bridge span, pointed open arch (and K05a–d)
- **K06** bridge pier, stackable rib
- **K07** nave wall, three open bays (and K07a–d)
- **K09** jetty
- **R01–R04** shore shelf, basalt tooth, split boulder, talus bank

Each needs Body, Height and Guts. Windows get Emissive.
Integration: cheap for art; Claude adjusts the kit stamping for the new density once.

### 2. Tiles for generated terrain (new)
Generated maps (hills, islands, canyon) fill large areas with code-made stone. Two seamless tiles fix that:
- **E01 masonry tile,** 256×256 art px, seamless both ways, with Height
- **E02 guts tile,** 256×256, seamless: rubble, rebar, hollow stone
- **E03–E06 stamps:** a crack, a chip, a carved band, a tide-line strip, each with Height

Integration: moderate. Claude swaps the procedural fill for the tile.

### 3. Water foreground: sump pieces
Half-sunk, cut flat at the waterline. Body, Height, Guts. Set-piece size: a head should be taller than a trooper standing next to it.
- **S01** fallen saint head, broken halo (redraw at 2× and at set-piece size, about 200 art px)
- **S09** colossal fallen head, shattered crown (about 380 art px)
- **New S10** toppled statue lying on its side, half-sunk (about 300 art px wide)
- **New S11** broken saint hand reaching out of the water
- **New S12–S13** two rubble and rock clusters at the waterline, different silhouettes
- **New S14** sunken iron halo or wheel, a third out of the water

Integration: cheap for S01 and S09 (existing sump placement). New codes need one placement-table line each, using `place: sump` and `sink` in the notes as `WORLD-ART.md` describes.

### 4. Near foreground: depth-of-field layer
Pieces between the camera and the fight, drawn big and simple; the engine blurs them. **Body only,** near-black silhouettes, no detail needed.
- **D01–D06** redraw at 2×: broken column, fallen slab, half-sunk arch, mooring posts, saint hand, barge ribs
- **New D07** hanging chains entering from the top edge
- **New D08** a broken balustrade rail
- **New D09** a huge out-of-focus saint shoulder at the bottom edge

Integration: cheap (existing slots).

### 5. Set pieces on the play layer
At set-piece size, Body, Height, Guts, placement notes as in `WORLD-ART.md`:
- **S03** perched gargoyle (40–60 art px today, so about 100 at 2×)
- **S07** praying saint on a pedestal
- **New S08** hanging faction banner, two to three troopers long, on the Cloth layer

Integration: cheap for S03 and S07. S08 needs hanging-attachment code (small).

### 6. Troopers (Ash Legion first)
Rework the current rig at 2× and keep its structure, so integration stays cheap:
- **TORSO, ARM, THIGH, SHIN** at 2×, same sockets (hip, shoulder, knee, hand) re-marked on the bigger canvas
- Use Jarred's latest studies (the chunky helmeted knight with a cloak and jump pack) as the target. Keep the silhouette readable at game size on a phone.
- **Readability against busy stone:** a strong, simple silhouette; emissive visor slit and one or two status lights; cloak on the Cloth layer. The engine adds a faction-coloured rim, so don't outline.
- **Jump pack** as part of TORSO, with its exhausts on Emissive.

Integration: cheap if sockets are marked; Claude checks firing origins with the alignment tests.

### 7. Weapons and icons
Jarred's note: the current weapon models and their icons don't feel like the world.
- **W01–W08** held weapons and **W09–W21** equipment, redrawn at 2×. Dark gunmetal and worn bronze, gothic detailing (fluting, small reliquary housings, chain, devotional plates), and status lights on Emissive. Muzzle facing right, barrel level, **grip** and **muzzle** points marked.
- **Weapon-select icons:** one per weapon, a clean single-colour silhouette of that weapon's new model, 160×160 PNG, transparent, light grey (#c9c6cf). Same filenames as now in `assets/ui/icons/`: bolter, chain, cutter, drone, fab, fist, flamer, frag, jet, lance, las, mine, minigun, mortar, nuke, pod, rail, rope, scatter, sentry, sun, warp.

Integration: cheap. Weapons are existing slots; icons are a file swap.

### 8. Props
At 2×, with Body, Emissive and Guts:
- **CRATE_ARMS, CRATE_HEAVY, CRATE_MED, CRATE_TOOL**
- **C04** promethium brazier
- **C03, C06** (existing props)
- **New C07–C10** light fixtures to replace the code-drawn ones: a hanging lamp, a wall bar light, a neon cross, a street post. Each is one piece with an Emissive layer.

Integration: cheap for crates and the brazier. The fixtures need a small code change to draw art instead of shapes.

### 9. Far background
The game's own pixel skyline stays; Jarred prefers it.
- **Far city plate (redo):** about 3500×700 px, seamless left to right, flat values, **no fog, no gradient sky, no moon** baked in. The engine adds haze and fades it.
- **Moon:** a simple disc, 256×256, transparent, very little surface detail. The engine tints it and adds the glow.
- **No sky gradient:** the sky is now rendered in code.

Integration: cheap (file swap in `assets/bg/`).

## Not in this push
Destruction sprite sheets, falling chunks, whole-body animation frames, other factions' troopers. Ash Legion first, as the art direction says.

## How to hand it over
- Forge assets: save versions in the Forge as usual; don't release.
- Files outside the Forge (height maps, tiles, icons, background): commit to `art/weapon-lab` under `art/incoming/` with this brief's codes in the filenames.
- Add one `LOG.md` entry listing what's ready, then Claude integrates on the `lit` branch and posts a test link.
