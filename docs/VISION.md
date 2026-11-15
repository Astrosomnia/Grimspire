# Grimspire: design vision

*A dark fable of war and woe.* Private: share deliberately.

## The pitch
An artillery roguelike set in a dark, technoreligious future. Lead a squad of four cyber troopers up a drowned, neon-lit citadel, battle by battle, to face the Definitor. Every level is generated and destructible. Every trooper who falls stays dead. When the squad dies the run ends, but your gene-line endures, and the next squad is cloned from what the last one earned.

**In one line:** Worms meets Slay the Spire in a grimdark cathedral-hive.

## Why it works
- **It fixes artillery's weakness.** Worms-likes are brilliant with friends and thin alone. A roguelike run gives solo play a spine and every battle stakes.
- **Generated, destructible terrain suits a roguelike.** No two fights play the same.
- **Named troopers with permadeath** (the XCOM effect). Losing a veteran hurts, and that hurt is the hook.
- **Meta-progression that belongs to the world.** Dead squads feed the clone vats, and new recruits inherit gene mutations.
- **A clear goal:** climb the citadel, face the Definitor.
- **The hardest part already exists:** a playable destructible artillery engine with lighting, a full arsenal, supply drops, hazards, online play and a CPU opponent.

## Core loop
1. **Battle:** your squad against an enemy squad on a generated, destructible map
2. **Reward:** after each victory, choose one of three crates (a new weapon, more health, a revive, shields, more ammo, a weapon level, a new recruit)
3. **Path:** choose the next room on a branching map up the citadel (battle, elite, armoury, medicae, shrine, event)
4. **Repeat** through each zone to a boss, then the Definitor
5. **Death:** a fallen trooper is gone for good. Squad wiped means the run is over. Persistent currency and gene mutations carry into the next run

## Structure (draft)
- Zones climbing the citadel, for example **The Sump → Manufactorum → Cathedral → The Spire**, each with its own look, hazards and enemies
- Elites and a boss per zone; the **Definitor** at the top
- Target run length 20–40 minutes

## Replayability (later)
- **Relics and synergies** that bend the rules ("Promethium Litany: fire spreads twice as far", "Martyr's Seal: fallen troopers detonate")
- **Enemy variety and smart AI.** In single-player the CPU is the whole game; the biggest piece of work
- **Trooper traits and levelling**

## Multiplayer (later)
1. **Skirmish:** standalone versus, pass-and-play or online
2. **Draft duels:** best of five, both players pick crates between rounds
3. **Daily citadel:** the same seeded run for everyone
4. **Co-op runs:** two commanders, one squad, shared gene-line
5. **Invasions:** a real player invades your run as an enemy elite commander

Priority: solo run first, then daily seed and draft duels, then co-op and invasions on the final platform.

## Plan (Jarred, 28 Oct 2026)
1. **Nail the core gameplay** in the HTML prototype first
2. **Move to a proper engine** (likely Godot) and build the full game: runs, meta-progression, content, saves
3. **Build a compelling proposition:** a playable vertical slice plus a sharp pitch
4. **Take it out:** share online to build interest, approach Vancouver developers, show publishers

**Platforms:** PC first (Steam, Steam Deck), consoles later, mobile only as a port. Keep runs short and controls touch-capable so a port stays cheap.

### Pitching
- A focused 10–15 minute playable slice beats a long design doc
- Pair it with a short deck: hook, comparable games, platforms, scope, what's done, what's needed
- Execution is what's hard to copy. Build in public through devlogs and clips; keep the repo private for now

### Competition: Worms Galactic Tactics (Team17, Gamescom 2026)
Isometric, grid-based roguelike tactics. Overlaps: squads, upgrades between fights, run ends on a wipe, crates, rising water. Differences: grid not free-aim physics, cartoon not grimdark, generous undo and cheap revives instead of permadeath, weak knockback. A comp, not a threat. Pitch angle: real physics, real permadeath.

## Campaign direction and What If bank (15 Nov 2026)

**Working principle:** Campaign is the adventure; multiplayer is the playground. Campaign can depart radically from symmetric Worms-style combat. Multiplayer preserves the already-fun artillery PvP format, refined with the best campaign weapons, characters, assists, hazards and environments. Like GoldenEye's campaign-inspired PvP arenas, each mode stands alone; campaign progression must not gate competitive multiplayer.

**The central design problem:** Artillery is naturally brilliant against humans, but a symmetrical CPU opponent struggles to reproduce human improvisation, mistakes and surprise. Don't assume the answer is merely smarter Worms AI. Test solo encounters designed *for* artillery: asymmetry, physical problems, pressure, objectives and enemies with legible behaviours. The player should regularly feel clever, powerful or delighted.

### Roadmap of capabilities (directions, not committed implementations)
- **Different level structures:** not only islands or towers; spires-only arenas, interiors, catacombs, swamps, sky spaces, waterfalls and more. Prioritise playable geometry over endless decorative assets.
- **Connected traversal:** linked rooms, vertical routes and levels that feel like places rather than isolated arenas.
- **Different engagement types and objectives:** asymmetric battles, survival, extraction, defence, escape, sabotage and environmental challenges—not always eliminate every opponent.
- **Enemy variety:** weak hordes, hunters, artillery engines, fortresses, elites and bosses. AI can have specific readable behaviours rather than full player-equivalent intelligence.
- **Different scales:** close-quarters fights, long-range artillery and large set-piece encounters.
- **Meaningful progression:** weapons, upgrades, powers, limited resources, mutations and synergies that change decisions and the flow of a fight; rewards and branching choices between encounters.
- **Actual runs:** short, repeatable sequences with persistent damage, ammo, trooper losses and consequential rewards. The rhythm of encounters is more important than the quantity of content.
- **Discovery through locations:** distinctive areas and biomes whose art suggests a larger world; reuse systems and modular architecture so variety isn't exclusively handcrafted.
- **Classes and squad-building:** Heavy, assault, demolitions, medic, scout, etc.; weapon affinities or restrictions, armour, mobility and abilities create complementary roles. Recruit and evolve a squad; losing a specialist matters. Whether restrictions are hard or soft remains open.
- **Faction identity and unlocks:** start campaign as **Ash Legion**, unlock **Neon Choir, The Hollow and Halo Guard** through play, in the spirit of Monster Train. Each faction should offer distinct weapons, skills and tactical character. Possible primary/secondary faction combinations later; preserve each faction's identity. Unlocks apply to campaign, not PvP access.
- **Real-time-ish combat:** explore cooldown-based weapons, real-time movement, deliberate aiming or slow-time windows—an almost artillery-MMO rhythm. A major experiment, not an approved change.
- **More physical destruction:** rubble, structural failures, material interactions, water, fire and dirt; world manipulation should produce tactical opportunities. Seek readable, fun consequences rather than simulation fidelity for its own sake.
- **Bonus Mechanic X:** leave room for an unexpected, genuinely defining interaction that emerges from prototypes; do not make finding it a blocker.

### Key What Ifs to prototype, not prematurely decide
1. **One soldier vs four:** a single protagonist, a switchable squad, or one directly controlled soldier with allies/assists. Preserve the possibility of named soldiers and meaningful permadeath without inheriting four separate Worms turns.
2. **Turn-based vs real-time-lite:** compare classic artillery against hordes, cooldown-based real-time movement/attacks, and a shared-turn or squad-command hybrid. Protect the pleasure of a deliberate, skilful shot.
3. **Symmetric CPU vs authored asymmetry:** enemies as physics problems—swarm, hunter, siege machine, destructible fortress—rather than humans simulated badly.
4. **Environmental simulation:** rising water every turn, breached reservoirs, collapsible bridges, spreading fire, destructible chambers and open-ended physics puzzles (From Dust / Noita territory). Can reshaping the world be more useful than a direct hit?
5. **Procedural architecture:** modular functional bays (supports, shafts, chambers, bridges, reservoirs) dressed with Body + Back art. A small rule set should produce varied playable spaces, not only varied silhouettes.
6. **Squad classes × faction styles:** class defines role; faction changes its expression. Test whether mixed compositions create interesting trade-offs without overcomplication.

### First proving milestone: a small playable run
Build a deliberately minimal **three-encounter, 10–15-minute test** with existing assets where possible: (1) short skirmish, (2) vertical gauntlet with a non-elimination objective, (3) distinctive guardian/boss. Carry health, ammunition and losses between battles; offer two meaningful upgrade decisions. Test pacing, AI, traversal, rewards and attachment before scaling art or content. This is a proposed experiment, not a shipped feature or locked final campaign structure.

**Decision rule:** Protect what already works in PvP. Prefer experiments that multiply interesting interactions and replayability over making more content. Judge repeat play, not the first impressive spectacle. Record prototypes as tested or rejected before promoting any What If into canon.

## Open questions
- What the persistent currency is called and buys (gene-seed? relics? clone-vat upgrades?)
- Who or what the Definitor is
- Squad size and how recruits slot in mid-run
- Enemy factions per zone
- **Battle length vs "just one more."** A 4v4 artillery match can run 10+ minutes, which kills a 20–40 minute run. Ideas: 3–5 minute battles, 6–8 per run; deploy 2–3 of your 4; whole-squad turns (XCOM-style); ~20s turn timer and near-instant CPU turns; lethal not grindy; the sump rises early; objectives that end fights early; not every room a full battle; a fast loop around the fights
