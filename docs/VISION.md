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

## Open questions
- What the persistent currency is called and buys (gene-seed? relics? clone-vat upgrades?)
- Who or what the Definitor is
- Squad size and how recruits slot in mid-run
- Enemy factions per zone
- **Battle length vs "just one more."** A 4v4 artillery match can run 10+ minutes, which kills a 20–40 minute run. Ideas: 3–5 minute battles, 6–8 per run; deploy 2–3 of your 4; whole-squad turns (XCOM-style); ~20s turn timer and near-instant CPU turns; lethal not grindy; the sump rises early; objectives that end fights early; not every room a full battle; a fast loop around the fights
