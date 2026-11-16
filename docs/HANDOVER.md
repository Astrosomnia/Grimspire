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

### Pick up here (Claude, from 16 Nov)
- **Next job:** build the building-lab playground per [`BUILDING-SYSTEM.md`](BUILDING-SYSTEM.md): `experiments/building-lab.html`, standalone, placeholder shapes in the play-diagram style, 24 seeded buildings per page, generator passes 1–8 driven by one weight table, reachability and artillery checks, keep/cut that shifts weights, lock-as-template, export. Start from the bay grid in [`BAY-KIT-BRIEF.md`](BAY-KIT-BRIEF.md) and read the existing building generator in `index.html` first (search for the building and sewer/tunnel generation) so the rules can port back. Publish it as a private test artifact for Jarred, then log it.
- **Live art (GV 72, Forge revision `20261116T223943Z-ef850d01`):** ChatGPT's refreshes de-dappled with `deblob.py`, K10 rose glass fixed, rocks with baked grit (`grit.py`), K17 kept original, grime dots removed from the stone shader.
- **Art bar:** [`ART-READABILITY.md`](ART-READABILITY.md). Benchmarks are the original K08 cathedral and S01 head. Judge at play zoom next to terrain; normal density for kit pieces; never plane-rebuild good Heights; dapple lives in the Body, so fix it there. Its Back work list is ChatGPT's queue (K10 worst; K13 dome needs Back).
- **Art tools** on `art/weapon-lab`, `art/lab/tools/`: `deblob.py`, `grit.py`, `height_punch.py` (`--despeckle`, `--deblob`), `simplify.py`, `pixel_snap.py`.
- **Releasing art outside the Forge UI** (how Claude has done it with Jarred's go): build the payload with the Forge's `build()` from `art/lab/hosted/model.mjs`, bump GV if collision changed, run `dsim`, `dsim2`, `dsimart` and the art tests, sweep about 60 maps for errors, push `main`, then add the revision (`revisions/<id>/manifest.json`, `payload.json`), point `state.json` `current` at it, and write a receipt in `art/integrations/`. Stage only the files you mean on `art/weapon-lab` (a soft reset once swept in deletions).
- **Testing tips:** headless Chromium with SwiftShader works; the camera drifts between shots, so frame by kit coordinates and retry; `det.py` compares `/home/claude/work/orig.html` vs `grimspire.html`, so refresh those first; a `Tainted canvas` error from `file://` is harmless.
