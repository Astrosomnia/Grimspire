# World art and props

How Grimspire's world is built: the north star, the rules every piece follows, and the process from idea to live. For Jarred, ChatGPT and Claude. The faction and character look is in [`ART-DIRECTION.md`](ART-DIRECTION.md); the Forge's technical rules are in [`FORGE.md`](FORGE.md).

## North star
**Black gothic ruins against a burning sky. A drowned cathedral-city where colossal saints lie half-sunk in black water, faction neon is sprayed across the stone, and every lit edge glows the colour of the light that hits it. The stone is dark; the sky and the lights are vivid. The troopers, the light and the explosions do the talking.**

Three tests every piece must pass:
1. **It belongs to this place.** A drowned, sacred, industrial ruin: stone, iron, bone, wax, chain, water. If it could sit in any fantasy or sci-fi game, it isn't specific enough.
2. **It stays out of the way.** Nothing in the world competes with a trooper, a projectile or a crate for attention.
3. **It reads as a silhouette.** Dark against the sky or the lit stone, before any detail.

## What the references show
Two images set the look: `art/reference/north-star.jpg` (the world) and `og.jpg` (the mood and the trooper). Concretely:

- **Contrast, not darkness.** Near-black architecture against a bright crimson-magenta sky with a huge blood moon. The darks are very dark and the sky is luminous; there is little in between.
- **Rim light carries the form.** Stone shows almost no surface detail in shadow. Its shape comes from thin lit edges: magenta-crimson where the sky and Ash Legion light reach, cyan on Neon Choir's side. Light colour, not object colour.
- **Faction territory lights the world.** Ash Legion's half of the scene is washed magenta, Neon Choir's half cyan. Their graffiti is wall-sized and dripping, their banners hang two or three troopers long with the faction sigil, and the stone near them picks up their colour.
- **Architecture is the terrain.** Towers, arches, bridges and broken walls are what troopers stand on. Set pieces crown and decorate it: a saint on a pinnacle, a gargoyle on a ledge, a banner hanging from an arch, a rope bridge between towers.
- **Colossal and half-sunk.** Fallen saint heads three or four troopers tall sit in the water up to the cheekbone. Statues are larger than people. Scale makes the city feel ancient.
- **Depth fades toward the sky.** The distant skyline is lighter and tinted toward the sky colour, with soft edges, not darker. Each layer back loses contrast and gains sky.
- **The water is a mirror.** Black, still, reflecting the neon and the moon. Wreckage pokes out of it as dark silhouettes with lit edges.
- **Supply crates glow.** Small, but their lit symbols make them pop on any ledge.
- **The OG adds the grim.** Skull and bone piles, iron spikes, chains, crimson banners with a circle-and-cross sigil, neon lines running up spires, gunships in the sky, aqueducts and falling water lit cyan. Dense, oppressive, holy and industrial at once.

## Attention ladder
What the eye should find first, in order. Each level is darker and calmer than the one above it.

1. Troopers, projectiles, explosions, fire
2. Things you can use or hit: crates, tanks, mines, sentries
3. Terrain edges (where you can stand)
4. Set pieces on the play layer
5. Back walls and facades
6. Skyline, sky, moon

If a set piece draws the eye before a trooper standing next to it, it's too bright, too saturated or too busy.

## Depth bands
The engine draws the world in these bands, back to front. Every piece belongs to exactly one.

| Band | What lives there | Moves | Look |
|---|---|---|---|
| **Sky** | Gradient, moon, smog, searchlights, the far sky war | Fixed or barely | Code only |
| **Skyline** | Distant spires, domes, cathedral fronts, colossal statues | Parallax, slow | Flat silhouettes tinted toward the sky colour, lighter and softer the farther back, tiny window lights, no detail |
| **Back wall** | Facades, arches, lancet windows, graffiti, banners, colossal saints behind the fight | With the world, non-solid | Dark, lower contrast than the play layer and a step toward the sky colour |
| **Play layer** | Destructible terrain, props, set pieces, troopers | With the world | Full contrast for things that matter; set pieces one step darker |
| **Sump** | The water and what's half-sunk in it | With the world, bobbing | Pieces cut by the waterline, reflections in code |
| **Foreground** | Wreckage in the water, chains, a broken rail, a hanging censer | Faster parallax | Near-black silhouettes with lit edges, never over a trooper's path |

Skyline and back-wall pieces are large and cheap: big shapes, few pixels of detail. Play-layer pieces are small and careful.

## Scale
Everything is drawn at the trooper's pixel density: **12 source px per art px, about 1.9 art px per world px**. A trooper is about **50 art px tall** (27 world px). The map is 2000 × 900 world px (about 3800 × 1700 art px).

| Tier | Size (art px tall) | Next to a trooper | Examples |
|---|---|---|---|
| Debris | 4–16 | Ankle to knee | Rubble, skulls, candles, chain links, shell casings |
| Props | 16–50 | Knee to head | Crates, tanks, graves, reliquaries, braziers, lecterns |
| Set pieces | 50–200 | One to four troopers | Fallen saint heads (three to four troopers, half-sunk), statues on pinnacles, gargoyles, banners, arches, piers, bells |
| Landmarks | 150–500 | A building | Colossal saints, cathedral fronts, broken spires (back wall or skyline) |

**Size sets meaning.** Saints and gargoyles are colossal: a fallen saint's head should be taller than the trooper standing beside it. The first six set pieces (S01–S06) are drawn at prop size (17–31 art px tall); they read as altar ornaments, not ruins. Redraw them at set-piece size, or keep them as props and give them prop jobs.

**Draw at final size.** The Forge's per-asset scale is for testing. A sprite scaled by 1.2 has pixels 1.2 times the size of everything around it, and mixed pixel sizes are the fastest way to make a world look pasted together. Once a size is chosen, redraw at that size and set scale back to 1. This applies to the 1.2 trooper and weapon reviews too.

## Light and colour
- **No baked lighting.** Paint flat. The engine adds rim light from the sky and from neon, fire and blasts, in the colour of that light. Don't paint rims or highlights in a fixed colour: they'd be wrong as soon as the light changes.
- **Dark stone, bright light.** World pieces stay in the lower half of the shared ramps; the brightness in a scene comes from the sky, the lights and the rims. Set pieces sit one value step below terrain edges. Farther bands lose contrast and shift toward the sky colour.
- **Colour comes from light.** Stone, iron and bone are near-neutral. Colour on a piece is either a real light (emissive layer) or faction cloth (Cloth layer).
- **Light colours mean something:**
  - Faction neon (magenta Ash Legion, cyan Neon Choir, green Hollow, gold Halo Guard): only on faction things, near that faction's ground
  - Equipment red: warning and status lamps on shared kit. Keep it a true red, clearly apart from Ash Legion's magenta
  - Amber: fire, candles, braziers, sodium lamps. The world's warm light
  - Sky light: whatever the sky is (cold moonlight at night, crimson when the sky bleeds). Never painted, only rim light
- **The game's sky is darker than the reference.** The north star's crimson sky is the target mood; today it appears when sudden death bleeds the sky red. A brighter per-map crimson sky is an open question in `ART-DIRECTION.md`.
- **A light that glows should light things.** Braziers, candle racks and lamps get an emissive layer and a light tag (below), so the engine lights troopers near them.

### Shared material ramps
Small ramps, 4–6 steps each, shared across all world art. Pick from them; don't invent near-duplicates.
- **Wet stone:** cold charcoal to blue-grey (the terrain's own range)
- **Iron and gunmetal:** neutral charcoal (Art Pass V2's eight-step palette)
- **Bone and marble:** desaturated warm grey, never white
- **Rust and bronze:** dark umber to dull bronze, for age and machinery
- **Wax and candle:** dull ivory, only around amber light
- **Cloth:** greys on the Cloth layer; the game colours it per faction

## Pixel craft
- **Silhouette first.** Fill the shape in one dark value and check it reads at game size before any detail. Gothic shapes (pointed arches, spires, crockets, ribs, wings, halos) are the vocabulary.
- **Clusters, not noise.** At least 2×2 clusters for any detail. No lone pixels except deliberate glints. Auto-reduced art always needs this cleanup pass.
- **No full outlines.** Dark-on-dark silhouettes and the engine's rim do the work. Use a darker edge only where a piece touches the ground or overlaps itself.
- **Wear tells the story.** Chips, cracks, water lines, moss, wax drips, bullet scars. A tide line at the same height on everything in the sump ties it together.
- **Judge at game size.** Look at every piece at 1× in the game on a phone before it's done. The Forge's readability view and Test in game are the check.

## Layers for world pieces
- **Body:** the piece, flat and dark
- **Emissive:** only real lights (lamps, candles, glyphs, neon)
- **Cloth:** banners, tarps, shrouds, hanging flags; faction-coloured in game. Neutral world cloth uses the grey "None" faction
- **Trim:** faction marks (graffiti, painted sigils) for faction-territory pieces
- **Guts:** what's inside when a blast bites in: rebar, rubble, hollow stone, cogs. Every piece that can be destroyed needs it

## Placement data
Every set piece and prop carries this, so the game can place it without hand-made maps. Until the Forge has fields for it, write it in the asset's notes in this form:

```
place: ground | sump | ledge | wall | hang
band: play | back | skyline | foreground
base: the art row that sits on the surface (the Forge's baseline)
footprint: the art columns that must rest on solid ground, e.g. 6–33
clear: headroom above in art px
sink: for sump pieces, how deep it may sit (fraction of height)
weight: how often it appears (1 = common, 0.2 = rare)
limit: most per map
zones: sump, ruins, manufactorum, cathedral, spire (or any)
faction: none, or the faction whose ground it marks
solid: none (default) | top (walkable top) | terrain (becomes destructible terrain)
flip: yes | no
light: none, or colour and radius for pieces that cast light
```

Defaults: decorative, non-solid, flippable, play band. Solid pieces become part of the destructible terrain, so they need guts and a clean silhouette.

## Composing a map
- **One landmark** per map in the back wall or skyline: a colossal saint, a cathedral front, a broken spire, ideally against the moon
- **Three to six set pieces** on the play layer and in the sump, spread out, never two of the same within view
- **Debris scattered** to break up flat ground, thinning out near spawn points so troopers stay readable
- **Faction territory** around each spawn: wall-sized graffiti, long banners and a shrine in that faction's colours, lighting the stone around them
- **The sump is a stage:** half-sunk heads, pier pilings and wreckage at the waterline make the rising water feel like the city drowning
- Nothing decorative inside a trooper's spawn area or on a crate's landing spot

## Generated world (Phase 3 art)
Maps stay generated; hand-made art supplies what you see. The generator decides the shape and where things go. In this order:

1. **Sockets instead of scatter.** The generator marks tower tops, ledges, arch keystones, wall faces, spawn walls and the waterline. Set pieces snap into those spots by their placement data: saints on pinnacles, gargoyles on ledges, banners under arches, heads at the waterline, graffiti near spawns.
2. **One grade over everything.** A final pass snaps colours to the shared ramps, fades each depth band toward the sky colour and lights everything with the same rims, so generated and hand-drawn pixels can't drift apart.
3. **Material tiles for terrain.** Hand-drawn seamless tiles fill the generated shape by surface type: masonry blocks for walls, rubble for rock, carved bands for ledges, each with a matching guts tile for craters. Edge details are stamped along surfaces: drips, moss, cracks, a tide line at the sump. Tiles are drawn on the art grid in the Forge and line up in world space.
4. **A modular architecture kit.** The generator builds from hand-drawn modules (wall spans, arch segments, tower caps, buttresses, rose-window panels, broken tops) joined by sockets, and the destructible shape comes from the modules' own pixels. Prove the look on one map first.
5. **A composition director.** One landmark against the moon, faction territory and light around each spawn, the sump staged with wreckage, density thinning near troopers, no repeats in view.

Decoration is cosmetic and may vary per device. Anything solid becomes part of the destructible terrain, so it must be seeded and synced, and it needs guts.

## Destruction
Blasts should break the world the way the art is drawn: in pixels and chunks, not smooth circles.

**In the HTML game:**
- **Crater shapes on the art grid.** Craters follow a noisy, broken outline snapped to art pixels, with stepped edges, loose fragments and short cracks running out from the rim. Stone breaks along its masonry lines once material tiles exist; rock crumbles. This changes the playable shape, so it uses the seeded generator and a GV bump.
- **Debris made of the terrain.** Chunks thrown out are sampled from the pixels that were destroyed, so a broken saint sheds pieces of saint. They tumble, bounce, settle and catch the blast light. Cosmetic.
- **Effects drawn as pixel art.** Fire, smoke, dust and explosions render into a buffer at the art-pixel grid and scale up crisp, using stepped palette colours and dithering instead of smooth gradients. Light from the blast stays soft; the shapes stay pixel.
- **Fresh damage reads.** Scorched, dithered rims; embers glowing in the cut for a few seconds; the guts layer showing inside.
- **Collapse.** Pieces with nothing holding them up break off and fall as rigid chunks.

**In the Godot rebuild:** a pixel-material simulation in the spirit of Noita: every pixel knows what it is (stone, rubble, iron, water, fire), stone breaks into rigid chunks with real physics, rubble pours, water flows into craters, fire spreads by material, and normal-mapped tiles let fresh cracks catch the light. That's the 2D equivalent of voxel destruction and suits a side-on artillery game better than true 3D voxels.

## Process: idea to live
1. **Pick from the backlog** (below), or add to it. Name the band, size tier and placement first.
2. **Concept sheet** (ChatGPT): a few options at roughly final pixel size, each shown as a silhouette and in a mock scene next to a trooper. Concept-resolution paintings are reference only.
3. **Jarred picks** one option per piece.
4. **Native pixel draft** in the Forge at final size. Automatic reduction is only for blocking in; every final piece gets a hand cleanup pass.
5. **Layers, baseline and placement data**, as above.
6. **Test in game** with the Forge's prop test, next to troopers, in the dark and near a light.
7. **Review against the checklist.** Jarred approves the exact version.
8. **Release** through the Forge, then **log it** in `docs/LOG.md` on `main`.

Batch work by family (all sump pieces, all faction shrines) so palettes and wear stay consistent.

## Review checklist
- [ ] Belongs to the drowned cathedral-city
- [ ] Right band and size tier; drawn at final size, scale 1
- [ ] Reads as a shape at 1× on a phone
- [ ] Darker and calmer than troopers and usable props next to it
- [ ] Flat paint, no baked light; colour only from emissive and cloth
- [ ] Colours from the shared ramps; equipment red distinct from Ash Legion magenta
- [ ] Clean clusters, no noise, no full outline
- [ ] Layers correct, including guts if it can be destroyed
- [ ] Baseline and placement data filled in
- [ ] Tested in game next to troopers

## Backlog
A starting list. Add freely; mark what's in progress.

**Sump:** fallen saint heads (several faces, set-piece size), toppled saint torsos, drowned bell, pier pilings, chained barge hulls, sunken reliquary, floating candles, drowned pilgrims' cages
**Ruins:** shattered arches, broken pillars and capitals, ossuary niches, collapsed rood screen, gargoyles (perched and fallen), confessional booths, broken organ pipes
**Faction territory:** a long banner, a shrine and a wall-sized graffiti set per faction (Ash Legion's circle-and-cross sigil from the OG image is a strong start) (Ash Legion inquisitor's gibbet, Neon Choir cable reliquary, Hollow flagellant's post, Halo Guard sealed vault door)
**Industrial:** pipes and valves, cranes and hooks, pumps, cable bundles, sodium lamps, broken servitors, aqueducts with falling water
**Grim:** skull and bone piles, iron spikes, gibbets, chained cages, rope bridges
**Lights:** braziers, candle racks, votive walls, hanging censers, neon saints
**Landmarks:** colossal praying saint, winged angel, cathedral front with rose window, drowned spire
