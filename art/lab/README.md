# Grimspire Art Lab

An isolated Git workspace for Jarred + ChatGPT to draw, test weapon art and
experiment with rendering while Claude primarily maintains the game.
Branch: `art/weapon-lab`. Main is changed only through explicit release.

## Start the Git-linked Forge

One-time requirements on your computer: Git, Python 3.10+, and GitHub CLI (`gh`)
with access to Astrosomnia/Grimspire. Authenticate GitHub CLI with `gh auth login`
and configure Git access with `gh auth setup-git` if needed. No token is entered
into the Forge, committed, or sent to the browser.

```sh
git clone --branch art/weapon-lab https://github.com/Astrosomnia/Grimspire.git
cd Grimspire
python3 art/lab/sandbox/serve.py
```

Open the `http://127.0.0.1:8765/art/lab/forge.html` URL printed by the companion.
For an existing clone, commit/stash your work, fetch, and switch to the lab branch.
Use the computer running the companion; this first version is not a hosted phone
app. Opening the HTML directly still works for drawing and local exports, but
Git buttons need the companion. GitHub access connected in ChatGPT does not
authenticate a separate browser or computer automatically.

## Draw → save → test → release

1. Open a weapon from **Library**, or draw a new one. Set a grip/pivot.
2. Open **Git sandbox** (also accessible through **Test in range**). Choose the
   existing weapon behaviour to preview as. A new sprite does not need a permanent
   game code. This choice does not invent a new firing behaviour.
3. Adjust weapon darkness, emissive strength, bloom, glow colour and scale; add a
   change note. These controls affect the saved weapon set. Source-detail art and
   grid art require different scales; check against the trooper.
4. **Save revision to Git** creates an immutable snapshot and commits/pushes it on
   the lab branch. **Save & test in game** does the same, then opens the exact saved
   game build with debug controls. Failed pushes are reported as local saves;
   **Retry push** retries without overwriting remote history.
5. Start a local battle. **TEST** gives weapons, adds troopers and freezes the turn
   timer. Online play and reporting are disabled in companion previews. Check both
   facing directions, held scale, animations, muzzle/effects and lighting.
6. **Review release…** prepares a focused integration branch and GitHub PR from
   the exact main commit used by this test build. Review its revision, content hash
   and changes. Preparing a release does not change main.
7. Check the explicit approval box for that exact tested build, then **Go live**.
   This fast-forwards main to the prepared commit, using an atomic Git lease so a
   simultaneous Claude push cannot be overwritten. Branch protection is respected:
   if GitHub rejects direct updates, use the focused PR through the required process.
   No automatic bypass or force retry is performed.

The button updates main; it reports deployment as **unverified**. Whether a main
push publishes the game depends on the repository's hosting setup. Verify the
actual published game before calling a revision live. Deployment configuration
has not been changed by the lab. A subsequent rollback is a new reviewed commit,
not a reset of main history.

## Editing rendering code

`sandbox/game.html` is a pinned copy of the game source. `sandbox/runtime.js`
is a small adapter, inserted inside the game's closure, that renders selected
Forge weapons without replacing the packed atlas or touching other sprites.
It supports body, trim, emissive layers and frame animation. The lighting controls
currently change weapons; environment and trooper lighting remain in game source.
We can experiment with those in `sandbox/game.html` and capture them in a revision.
The candidate contains those source edits, so inspect the integration diff.

The adapter places art by grip/pivot. Existing weapon rules, shot origins and
procedural effects remain the game's rules. Muzzle markers are retained in Forge
JSON, but this first adapter does not yet move projectile origins to them.
Source-detail art is not game-native pixel art. Grid variants still need cleanup.
A successful import or render is not artistic approval or proof of rig correctness.

## Staying current with Claude

**Refresh from main** updates the pinned source if it has no custom source edits;
it retains the saved art and adapter. Save a new revision and retest afterwards.
If game source has custom edits, reconcile them against current main manually
before updating `sandbox/base.json`; the companion refuses to silently discard them.
The builder removes its own previously promoted adapter on refresh, so releases
can be repeated without stacking multiple render overrides.

Each release must be tested against current main. If main advances between testing,
preparation and publication, promotion stops. Do not merge the long-lived lab branch
into main. The prepared commit changes only `index.html`, `debug/index.html` and
an integration receipt; lab files and experiments are excluded. The prepared commit
has current tested main as its only parent. The same game bytes tested locally
become `index.html`; debug gets only its normal debug flag.

## Version records

- `releases/weapons-v001/`: original immutable artwork studies and manifests.
- `sandbox/revisions/<id>/`: immutable game, input payload, source, adapter and hashes.
- `sandbox/current.json`: current saved review revision, committed alongside it.
- `sandbox/integrations/`: main commit and explicit approval receipts after promotion.
- `CHANGELOG.md`: human-readable change notes and integration records.

Browser **Save** remains browser storage. It is distinct from **Save revision to
Git**. ChatGPT and Claude should read current Git files and receipts, not assume
that another tool's local browser state has been committed.

Claude's separate `forge-pipeline` branch and its sync/atlas tools are untouched.
This preview adapter is a separate first implementation. Claude can later reconcile
it with atlas packing; avoid running a pruning sync against only the lab subset.

## Validation

```sh
python3 art/lab/validate.py
python3 art/lab/sandbox/test_companion.py
```

The companion tests use temporary local repositories, mock only PR creation, and
exercise real saves, pushes, repeated releases, tamper checks and concurrent main
updates. They never touch the real remote. Optional native Canvas renderer check:
`node art/lab/sandbox/test_render.js` (requires `@napi-rs/canvas`).

Git/HTTP and native Canvas checks passed in the build environment. Full interactive
browser QA remains outstanding because the environment has no installed browser.
