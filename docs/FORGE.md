# The Forge

Grimspire's shared pixel art editor and the art pipeline into the game.

- **Open:** https://grimspire-forge.jarredpowell88.workers.dev/ and sign in with GitHub. Jarred is the owner; collaborators are invited by numeric GitHub ID (Cloudflare variable `COLLABORATOR_GITHUB_IDS`). Collaborators can draw, save and test; only Jarred can release.
- **Health check:** `/health`
- **Code:** `art/lab/forge.html` (editor), `art/lab/hosted/` (Worker: `worker.mjs`, `model.mjs`, `bridge.js`, `families.*`). Cloudflare builds and deploys every push to `art/weapon-lab` (`node build.mjs && node --test test.mjs`). Maintained by Claude. Deployment settings: `art/lab/hosted/DEPLOY.md`.

## Daily use
1. **Library:** one card per asset, with its versions and animation states inside. Archive holds references.
2. **Draw:** body, emissive (glow), trim (squad colour mask) and guts (revealed when damaged) layers; frames; anchors.
3. **Test in game** (Shared Forge panel → **Test**): opens a local battle with your current canvas in the chosen test slot, plus the art from the current shared build. Nothing is saved. Use it freely.
4. **Save revision:** keeps this version of the asset in the Library and makes a shared test build others can open. Identical art isn't stored twice.
5. **Save & test:** both at once.
6. **Review saved release → Go live** (Jarred only): makes a pull request with the exact tested build and, once approved, puts it on `main` as a fast-forward. It refuses if `main` or the lab moved since the test (save and test again). The release adds an entry to `docs/LOG.md`.

Test targets: W01–W08 (the held weapons), ARM (the foreground arm), TORSO, THIGH, SHIN, PROP, TROOPER, BACKGROUND. W01–W08, ARM, TORSO, THIGH and SHIN can go live; the others are visual placement tests until the game has code for them (props have no collision, TROOPER is a static whole-body frame with no rig, backgrounds no parallax).

**TORSO** replaces the trooper's torso. Its **Hip** point sits on the legs' hip and its **Shoulder** point is where the arm and weapon attach (so moving it moves where shots leave). The Library's Trooper → torso state has the live torso with its sockets set to match today's game; move the points and Test with the Torso slot. **THIGH** and **SHIN** replace the legs and work as a pair (until both are in the build, the game keeps its own legs). The thigh hangs from the torso's Hip and swings there; its **Knee** is where the shin hangs and bends. Frame 1 is the near leg (drawn over the torso), frame 2 the far leg (behind it). The leg lengths set the hip height, so taller legs make a taller trooper. To test a whole trooper, Save the torso, thigh, shin and arm, then Test.

## Technical rules for art
- **Pixel density is fixed:** 12 source px per art pixel; about 1.85 art px per world px. A trooper is drawn about 27 world px tall; trooper frames are 41×58 art px with feet on row 54.
- **Layers:** transparent background, no baked glow or drop shadow. Glow goes on the emissive layer; anything team-coloured is drawn neutral grey on the trim mask. **Cloth** (cloaks, tabards, sleeves) goes on the Cloth layer in greys: the game colours it per faction by brightness, with mid grey (128) becoming the faction's cloth colour, so one set of trooper art dresses all four factions. The Faction picker in the editor previews it.
- **Points** (art px): weapons need **grip** (where the hand holds) and **muzzle** (where shots leave). The arm needs **shoulder** (its joint) and **hand** (where the grip attaches). A torso's **shoulder** and **hip** are sockets: where the arm attaches and where it sits on the legs. A thigh's **hip** is its joint and its **knee** is where the shin hangs. Hover a point's button in the Forge for its meaning. Points that feed firing (grip, muzzle, arm and torso sockets) change the sim; the game fingerprints them, so online players with different art are told to refresh.
- **Scale:** each asset has its own game scale (weapons currently 1.2×; the arm 1×).
- **Weapons:** muzzle facing right, barrel level.
- **Codes:** a type letter and two digits. **W** weapons, **P** projectiles, **M** charges, **A** arm and rig parts, **T** trooper animations, **G** Godfall pod, **C** props, **S** set pieces, **E** terrain, **F** faction marks, **B** background, **U** UI. The code is a display label; each asset also has a stable identity (`asset_id`).

## Adding art made outside the Forge
Assets generated or drawn elsewhere (by ChatGPT, say) go in as Forge sprite documents (`{forge:1, code, name, w, h, fps, base, pixel_scale:12, markers, frames:[{body, emis, trim, guts}]}`, layers as PNG data URLs at 1 art px). From an `art/weapon-lab` checkout:

```sh
node art/lab/tools/add_asset.mjs path/to/sprite.forge.json [--asset <existing asset_id> --state <state_key>]
```

It validates the document with the Forge's own rules, writes it under `art/lab/hosted/library/` named by its hash, and registers it in `library.json`. Without `--asset` it becomes a new asset; with it, a new version of an existing one. Commit, push to `art/weapon-lab`, and refresh the Library. Never edit or delete existing library, catalog or revision files: they're immutable history.

## How art reaches the game
`index.html` on `main` contains:
- `// BEGIN/END GRIMSPIRE_ART_ADAPTER`: `const LAB_PAYLOAD={…}`, the art data. **The Forge owns this block** and replaces it on release.
- `// BEGIN/END GRIMSPIRE_ART_RUNTIME`: the art renderer (draws payload weapons and the arm, ranged origins from the art rig, test props). **Game code, maintained on `main` by Claude.**

A Forge test or saved build is the `main` game with a different payload. A revision stores the payload and the `main` commit it was built on; the game is rebuilt from that when it's opened or released, and checked against the recorded fingerprint.

## Storage
On `art/weapon-lab`, under `art/lab/hosted/`:
- `catalog/` + `assets.json`: the original imported art (immutable)
- `library/` + `library.json`: saved versions (immutable, named by hash)
- `families.json`: groups catalog and library documents into assets and states
- `revisions/<id>/`: saved test builds (`manifest.json`, `payload.json`; older ones also hold full game copies)
- `state.json`, `events/`: current build, history, releases
- `releases/`: hand-made release records with previews (immutable)
