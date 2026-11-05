# Grimspire roadmap

What's done, what's next. How we work and where things live are in [`HANDOVER.md`](HANDOVER.md); the long-term game in [`VISION.md`](VISION.md); the look in [`ART-DIRECTION.md`](ART-DIRECTION.md).

## Tech plan
Prototype in HTML/canvas to nail the loop, weapons and feel, then rebuild in **Godot** once the design settles. Treat the move as a rebuild, not a port: the rules, numbers and feel carry over, not the code.

## Art sequence (Jarred, 31 Oct)
1. ~~Tidy the Forge Library~~ (done: one card per asset, versions inside)
2. ~~Sort out the arm~~ (done: one foreground arm with Reach, rotating at the shoulder)
3. Tweak existing assets: manual Forge edits alongside assistant-made changes, every version reviewable
4. Explore new weapon sheets, then bring chosen directions into the Forge
5. Roll assets out through focused releases against current `main`
6. Expand the asset set and world art direction, agreeing the reference and brief with Jarred first

## Art phases
- **Phase 1 (done):** weapons, the arm, the Forge pipeline
- **Phase 2 (now):** troopers as rig parts (torso, legs, arm, cloth layer), equipment and tool slots, first set pieces
- **Phase 3 (started 2 Nov):** the generated world made cohesive with hand art. In: sockets and decorative set-piece placement. Next: the redrawn set pieces (ChatGPT), pixel-art effects, art-grid craters and debris from terrain; later one grade over everything, material tiles, a modular architecture kit and a composition director. See `WORLD-ART.md`

## Next up
- **North Star look, all maps (Jarred, 2 Nov):** one look everywhere (sky, horizon, water, lighting, decor), variety from the layouts. Order: (1) ~~kit stamped, drowned district in rotation, look on, set pieces live~~ (done 2 Nov, GV 19); (2) convert spires (towers in water, bridges), then canyon (drowned gorge between cliffs), islands (over open water, piers), ruins (shores and drowned streets), one per push with a playtest each: own starting water level, rock base cut into shores and outcrops, same kit; (3) retire the classic look. Work happens on `phase3`.
- **Art direction:** continue the Ash Legion trooper (magenta, cloth as drawn) by hand at game scale (idle, aim, both facings, walk, jump-pack ignition, flight, landing)
- **Throwing arm:** separate arm and throw motion for grenades and other thrown items
- **Trooper art in game:** the renderer can show test trooper frames; real integration needs code (rig, animation, jump pack)
- **Payload weight:** the art payload is embedded PNG data (about 685 KB, doubling the game). Pack it into sprite sheets once the art settles
- Playtest GV 17: CPU feel, Godfall, wind, drop rate, enlarged weapons
- Sentry redesign (switched off for now)
- Painted terrain fill experiment on one fixed map; half-sunk statues in the sump once more of it shows
- Playtest four-squad matches; tune squad size, map size and turn length for 3–4 players
- CPU: teleporter, smarter heavy timing, maybe a difficulty setting
- Port the Proving ground (dummy range, wind control) from Claude's retired artifact as a Forge test option
- The roguelike prototype (expect big changes to core systems)

## Done
**Phases 1–5:** feel and controls, the original 17-weapon arsenal, rising sump, supply drops, promethium tanks, fire, knockback and knockdowns, rappel wire, procedural maps (Spires, Islands, Canyon, Ruins) with gothic architecture, a planning CPU, death camera and animations, group slow-mo.

**Phase 6, online (28 Oct):** match codes like ASH-4721, no accounts. Async turns that feel live: the active device streams inputs, the others replay about a second behind. Deterministic sim with a full snapshot at every handover. Version check (`GV`).

**Wave 1 polish (28 Oct):** dissolving bodies, grenade-martyr death, starting kit and limited-use weapons with an arms crate, wider flamer and barrel fire, cuttable parachutes, Doomsday fallout, smog and sky traffic.

**Sprites (28 Oct):** pixel weapons, crates with glowing symbols, parachute, dropship, rigged troopers (one torso plus two-piece legs from the hip).

**Wave 2A weapons (28 Oct):** Chainblade with stagger; heavy crate weapons Minigun, Sentry, Tracked Drone, Godfall; Teleporter.

**Wave 2B factions (28 Oct):** The Hollow and Halo Guard; fight the machine against 1–3 CPU squads; 2–4 squad pass-and-play and online; free-for-all or 2v2.

**Playtest pass (28 Oct):** online chat, gentler blast falloff and a concussion ring, sump timing, one swap per turn, phone levers, ledge scramble, test build, in-game field reports.

**North star visuals (29 Oct):** backlit near-black troopers with mixed side rims, faction graffiti baked into stone, gothic skyline with saints and angels, crater ghost fix.

**Phone layout (29 Oct):** top bar fits portrait, small round levers, icon swap and weapon chip.

**Weapon feel (29 Oct, GV 12–13):** wind curve (lookup table), minigun climb and recoil, overwatch sentry, supply drop rates.

**Field report fixes (29 Oct, GV 14):** melee needs a clear line, jump pack parking, uppercut fist, drone hop, human-feeling CPU, Godfall reborn as a materialising drop pod, no tap-to-swap.

**Weapons pass (29 Oct, GV 15):** sentry off for now, flamer hose, minigun 75 rounds, bolter down a notch, 10-turn fallout, crate mix.

**GV 16 (30 Oct):** balance sheet edits (Godfall 55, heavy crate odds, drop rates, barrel fire scatter, burning damage, sump after round 8); crimson sky bleeds in at sudden death.

**Art pipeline and GV 17 (31 Oct–1 Nov):** hosted Forge with shared Library and releases; eight animated weapon glows; weapons at 1.2× with corrected grips and real muzzle firing origins; straight foreground arm rotating at the shoulder; per-asset scale. Art renderer moved into the game; Forge test without saving.

**Drowned district plays, kit on every map (2–3 Nov, GV 19–26):** north look everywhere, drowned district from ChatGPT's kit, skyline plates, world depth, landmarks K10–K13 on rock, up-and-over decks and stubs, diagonals K14–K17 and big rock R05–R09, kit towers and landmarks on the generated maps, spawns through the levels.

**Field reports 4 Nov (GV 34):** lighter phone HUD (smaller weapon tile, Flamer short name, compact fuse, chat square, health lines off the clock), no name line, full screen toggle, longer death camera, idle music score detached.

**Field reports 4 Nov, round 2 (GV 35):** crates land at a random spot 80 px+ clear, jump pack only cushions steered falls, flamer panic before fleeing.

## Backlog
**Content:** terrain materials (rubble, armour plate), objectives beyond last-man-standing, hand-designed set pieces mixed into generated maps, per-faction sprites or trims, faction-specific weapons (long term).
**Feel:** hit-stop on big impacts, barks on hits and kills, instant replay of big hits (parked).
**Bigger swings (likely Godot):** a pixel-material destruction simulation (stone breaking into rigid chunks, rubble, water and fire by material), real 2D lighting with normal maps, AI-painted map library, the roguelike run structure, per-zone map personalities (Sump, Manufactorum, Cathedral, Spire).

## Open questions
- Crimson sky: done as the sudden-death bleed; also a per-map mood?
- Promethium tanks: code version until redrawn
- Sounds: still procedural
