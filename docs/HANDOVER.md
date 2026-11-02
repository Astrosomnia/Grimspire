# Grimspire handover

Start here. This is for everyone working on Grimspire: Jarred, Claude and ChatGPT. It says who does what, where things live and how we work. Keep it current; when it's wrong, fix it.

**Every session:** read this file, then the top of [`LOG.md`](LOG.md). **When you finish:** add an entry to `LOG.md`, and update this file if how we work or where things live has changed.

For new ChatGPT project chats, [`CHAT-CONTEXT.md`](CHAT-CONTEXT.md) provides paste-ready project instructions pointing back to these current docs.

## The game
*A dark fable of war and woe.* A Worms-style artillery game: squads of cyber troopers fighting over a drowned, neon-lit hive ward. One HTML file, played at https://astrosomnia.github.io/Grimspire/. Longer term it becomes an artillery roguelike and moves to Godot as a rebuild, not a port. See [`VISION.md`](VISION.md).

## Who does what
- **Jarred:** direction, playtesting, approvals. Nothing reaches the live game without his OK.
- **Claude:** all code: the game, the art renderer inside it, the Forge app, tools and tests. Reviews code changes from anyone else.
- **ChatGPT:** art and art direction. Draws and revises in the Forge, explores concepts, writes briefs. Code changes go to Claude as a request in `LOG.md`, or as a pull request Claude reviews.

## Where things live
| What | Where |
|---|---|
| The game (source of truth) | `index.html` on `main`. Edit it directly. `debug/index.html` is generated |
| Docs | `docs/` on `main` (this folder). World art and props: [`WORLD-ART.md`](WORLD-ART.md) |
| Shared change log | [`docs/LOG.md`](LOG.md) |
| Forge app | https://grimspire-forge.jarredpowell88.workers.dev/ (GitHub sign-in). Code in `art/lab/hosted/` and `art/lab/forge.html` on branch `art/weapon-lab`; Cloudflare deploys from there |
| Art library and Forge saves | `art/lab/hosted/` on `art/weapon-lab` (`library/`, `catalog/`, `revisions/`, `state.json`) |
| Art receipts for releases | `art/integrations/` on `main` |
| References | `art/reference/` on `main`. `north-star.jpg` is the style anchor |
| Old source kits and atlases | `art/kits/`, `art/in-game/` on `main` (provenance; the Forge library is where art is edited now) |
| Tools and tests | `tools/` on `main` |
| Balance sheet, field reports board | Claude artifacts on claude.ai (Claude keeps them in sync and reports changes in `LOG.md`) |
| Online backend | Firebase project `grimspire-9cf6a` (free tier): anonymous auth, Firestore `matches` and `reports` |

Branches: `main` (game, docs, tools), `art/weapon-lab` (Forge app and art data) and `phase3` (Claude's interim North Star work: background depth, water, grade; merged to `main` only with Jarred's OK). Release branches the Forge makes (`art/release-*`) can be deleted once merged. Short-lived art branches (like `art/category-review-sheets-20261101`) are fine; delete them when done.

## How work flows
**Code (Claude):** edit `index.html` on `main`, run `python3 tools/build.py debug`, test, bump `const GV` if the sim changed, commit, push. GitHub Pages deploys `main`. Log it.

**Art (Jarred, ChatGPT):**
1. Draw or open an asset in the Forge Library.
2. **Test** to try it in a battle. Nothing is saved, so test as often as you like.
3. **Save** when it's a version worth keeping. Saves add a version to the asset; identical content isn't saved twice.
4. **Save & test** to make a shared test build (a revision) others can open, or to prepare a release.
5. **Review saved release** (Jarred only) makes a pull request, and **Go live** puts that exact tested build on `main`. The Forge adds a line to `LOG.md` when it does.

Assets made outside the Forge (by ChatGPT, say) go into the Library as new files under `art/lab/hosted/library/`, registered in `library.json` with their hash. See [`FORGE.md`](FORGE.md).

**Art reaching the game:** the Forge writes art into the game's `LAB_PAYLOAD` block (between `// BEGIN/END GRIMSPIRE_ART_ADAPTER`). Everything else in the file, including the art renderer (`// BEGIN/END GRIMSPIRE_ART_RUNTIME`), is game code that Claude maintains. Weapons W01–W08, equipment W09–W21 and M01, the arm, torso and legs, the parachute, dropship, promethium tank and the four crates go live this way. Ground props, whole-body trooper frames and backgrounds can be tested in the Forge but need code before they can go live.

## Rules
- **The sim is deterministic.** Online play replays inputs, so every device must compute the same result. Map generation and sim steps use the seeded generator; cosmetics use `RR` or their own hash. No `Math.pow` and friends in the sim (use lookup tables). Snapshots are plain JSON. Check with `tools/test/dsim*.py`.
- **Bump `GV` on any sim change.** Mismatched online players are told to refresh. Art points that feed firing (grips, muzzles, arm and torso sockets) are covered by an art fingerprint the game compares online, so Forge releases don't need a GV bump.
- **Restricted palette.** Black stone, one sky colour, faction neon. Nothing gets colour just for being an object, except faction cloth in its faction's dark colour. Ash Legion is magenta, Neon Choir cyan, The Hollow green, Halo Guard gold.
- **Crisp over soft.** Pixel edges stay sharp; glow comes from separate light layers.
- **Materialise, don't pop.** Things that appear or vanish build from or break into the squad's neon motes.
- **Lo-fi on purpose.** Fun and fast iteration over polish. Don't over-engineer the HTML; Godot is for the rebuild.
- **Original names only**, Warhammer-flavoured. Keep the roguelike concept private.
- **Test on both screens.** Jarred plays on phone (often portrait) and a high-refresh PC monitor. Phone tests wrap the page with `tools/test/wrap.sh`.
- **Show, don't argue, on look calls.** Render a side-by-side and let Jarred pick.
- **Never commit secrets.** Forge credentials live in Cloudflare.
- **Copy:** Australian/Canadian spelling, human tone, no hype.

## Talking with Jarred
Terse, decides fast, often on his phone. When there's a naming or design call, give 3–4 options, pick one and say why. After a change: what changed in plain words, what to try, what's easy to tweak. Honest pushback beats agreeing.

## Current state
See the top of [`LOG.md`](LOG.md) and [`ROADMAP.md`](ROADMAP.md) (Next up).
