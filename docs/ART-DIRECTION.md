# Grimspire art direction

The look we're aiming for. Owned by Jarred, developed with ChatGPT. World art, props and set pieces have their own brief: [`WORLD-ART.md`](WORLD-ART.md). Technical art rules (pixel density, layers, anchors) are in [`FORGE.md`](FORGE.md).

## The north star
`art/reference/north-star.jpg` (set 29 Oct 2026). Not the exact look or scale, but the direction.

A drowned gothic city at night. Ruined cathedral arches, bridges and spires stand in black, still water. Toppled saints' heads and broken statues lie half-sunk in the sump. The sky is deep crimson with a huge blood-red moon and a far ruined skyline in haze. The factions claim territory with glowing graffiti and banners on the stone: a squad's name and sigil sprayed in its neon colour, dripping. One half of the scene is lit magenta and the other cyan, both reflected in the water.

Tone: Dead Cells, Blasphemous. Grim, painterly pixel art, readable silhouettes, colour from light. "Worms meets Warhammer": dark gothic artillery warfare among armoured cyber troopers in drowned, neon-lit ruins. Cyberpunk underneath: weird, frightening and decaying, almost adjacent to hell without becoming literal hell. God in the Machine, almost literally.

## Rules
- **Restricted palette.** A scene uses very few colours: black stone, one sky colour, and the neon of the factions present. Nothing gets a colour just for being an object. **Exception (1 Nov):** faction cloth may carry its faction's own dark colour (Ash Legion oxblood, say), kept dark enough that neon and fire still lead.
- **Colour comes from light.** Stone is near-black. Neon, fire and explosions supply the colour, and the water reflects it.
- **Silhouettes against a lit sky.** Gargoyles, saints and spires read even when small.
- **Backlit troopers.** Near-black silhouettes painted dark and fairly flat; the engine adds rim light from nearby lights and the sky and lights them up near blasts. Visor and squad lights stay emissive.
- **Crisp over soft.** Sharp pixel edges; glow from separate light layers, not blur.
- **Judge at game scale.** Concept detail doesn't survive automatic reduction. Refine actual pixel clusters and silhouettes at the size the game draws them (a trooper is about 27 world px tall).

## Factions
All are cults to some degree. Differentiate shape, material, behaviour and cloth construction, not just colour. All factions share equipment for now; faction weapons are a longer-term idea. Establish Ash Legion first.

| Faction | Game colour | Foundation (Jarred) | Demand |
|---|---|---|---|
| **Ash Legion** | magenta | Inquisitors and arbiters devoted to the one true Divine, an unforgiving God. No heresy tolerated. Half knight, half priest; futuristic templars distorted by zeal. Modern armour with sword-era ancestry | Obedience |
| **Neon Choir** | cyan | Devoted to Central and technological perfection. Divinity through becoming one with the Machine; calls others to join | Assimilation |
| **The Hollow** | green | Flagellants and doomsayers who believe destroying the world makes way for an unimaginable dark power. Chant backwards; Goetic names | Destruction |
| **Halo Guard** | gold | Cold, detached praetors guarding an unimaginably wealthy few for thousands of years; their light must be kept from others. Ascendant names | Exclusion |

Original names only, Warhammer-flavoured. 12-name rosters each.

### Decided: faction colour and cloth (Jarred, 1 Nov 2026, "for now")
Option C from the side-by-side: **Ash Legion is magenta and Neon Choir is cyan** (swapped from before; it fits the lore better), and faction cloth keeps its colour as drawn in the concepts. Cloth is painted on the Forge's Cloth layer and coloured per faction in the game: Ash Legion oxblood, Neon Choir near-black blue-grey, The Hollow ash sackcloth, Halo Guard cream (the `cloth` values in the game's `TEAM` table). Factions may later get their own trooper art; the Cloth layer still colours variants (`art/reference/ash-legion-variants.png`, `faction-lineup.png`). Live in the game from 1 Nov. Revisit if cloth starts competing with the light at game scale.

### Ash Legion: what landed (from ChatGPT sessions)
Preferred anchor: the enclosed-helmet knight-priest (layered dark armour, imposing human proportions, cloak and priestly cloth; anonymous institutional authority).
- Pale ceramic and orderly relic gear drifted toward Halo Guard; lean, ragged or hooded figures read as a rogue
- Wanted balance: "a little more tech and a little less blacksmith"
- Darker cloth, duller armour, recessed face, elongated faceplate, ribbed throat and raised collar moved closer. More gothic character and brighter selective machine light still wanted
- Avoid shiny silver bevels, continuous neon outlines and cloth competing with the sky
- Crosses, gold jewellery, greathelms and tabards push toward medieval Warhammer; machine-derived devotional marks are an open exploration
- A short mantle and exposed twin-thruster pack were tried to clear the jump pack: a fit-test, not a replacement for the long cloak. The experimental T09 body and A05 arm are in the Forge Library (auto-reduced, not approved)

## Lore proposals (not canon)
Jarred proposed Grimspire as a last bastion in a plague-ridden cyber dark age, holding something each faction believes is the key to its ascendance. A dying world that once held 80 billion people, survivors turning to religion. Ideas on the table: other settlements may exist; ancient systems that work flawlessly while basic necessities fail; rituals that preserve real technical procedures; each faction holding a partial demonstrable truth; something beneath Grimspire that might answer. Don't canonise these silently.

## Terrain: higher fidelity, still destructible
The map stays a per-pixel mask that explosions erase. Fidelity comes from what fills it:
1. **Painted fill** drawn like the reference; explosions erase the painting itself
2. **What's inside:** a second painted layer (rubble, rebar) revealed when a blast bites in
3. **Edges:** fresh cuts get a rim of light and soot
4. **Live lighting:** paint flat, no baked lighting
5. **Collapse:** unsupported chunks break off and fall (fuller crumbling is a Godot job)
6. **AI-painted maps:** the generator makes shapes; an image model paints each in style; pre-bake a library

## Easiest wins, in order
1. ~~Faction graffiti as glowing decals near each squad's start~~ (done 29 Oct)
2. Half-sunk statue heads and toppled saints in the sump and on the ground
3. A painted far skyline as the deepest background layer
4. ~~Backlit silhouette troopers with engine rim light~~ (done 29 Oct)
5. ~~Crimson sky~~ (done as the sudden-death bleed)
