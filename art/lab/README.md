# Grimspire Forge

Our shared weapon/art workspace. GitHub holds the authoritative artwork, game
source, renderer experiments, notes and revision history.

**Hosted Forge:** https://grimspire-forge.jarredpowell88.workers.dev/

**Status:** Hosted application code is prepared. The existing Cloudflare Worker
still needs its account-side Git build connection and first verified deployment.
The URL alone does not prove the hosted editor is running. No artwork has been
approved or published to main by this setup work.

## Finish the one-time deployment

[Exact Cloudflare settings and acceptance checks](hosted/DEPLOY.md). Use the existing
grimspire-forge Worker and the art/weapon-lab branch. Cloudflare's production branch
setting applies to the Forge application; it does not publish the main game.

## Everyday workflow

1. Open the hosted Forge and sign in with GitHub.
2. Open art from Library, edit it, or create a new sprite.
3. Choose an existing weapon behaviour to preview as and adjust lighting/scale.
4. Add an update note, then Save revision or Save & test in game.
5. Test the exact saved revision in a local battle using the TEST controls.
6. Review the saved release and its PR. Explicitly approve the tested build to Go live.

New work from Claude or ChatGPT is detected. Refresh shared library to see it; your
unsaved canvas is kept. A stale save is refused rather than silently replacing
someone else's revision. If main changes after a test, save a new revision and
test again before release. Main updated and public deployment verified are shown
separately. The original editor's Ready checkbox is not publication approval.

## Working with Claude

[CLAUDE-HANDOFF.md](CLAUDE-HANDOFF.md) describes what has been built, deployment
status, file paths, how to add alternatives and release constraints.
[CHANGELOG.md](CHANGELOG.md) records changes.

Shared alternatives go in hosted/library/ and are indexed with file hashes in
hosted/library.json. Hosted saves create immutable hosted/revisions/ snapshots and
update hosted/state.json in the same commit. Existing source-art studies remain
under releases/weapons-v001/. Do not merge the whole lab branch into main.

## Current art limitations

Detailed studies remain source-resolution art. Grid variants are automatic
reductions requiring cleanup. Test both facing directions, scale, anchors and
effects. The current adapter uses grip/pivot for artwork placement and retains
existing game firing/projectile origins; muzzle markers do not move those yet.
Weapon lighting controls currently apply to the saved weapon set.

The previous local companion remains available for development; its optional
[local instructions](sandbox/LOCAL.md) are not required for hosted use. The old
Claude Artifact library is not synchronised with this repository workflow.

## Full asset Library and single arm

Hosted Forge's Library defaults to one card per actual asset. Search or filter by
category, then Open its latest draft or initial catalog default. Versions & sources
contains the historical/source artwork; animation states and component overlays
stay inside their asset. Archive holds reference sheets. All art is retained.
Source images retain their original raster resolution; importing is not a redraw.
`hosted/assets.json` indexes immutable documents and SHA-256 values. Rebuild the
source catalog with `python art/lab/tools/catalog.py` from the repository root.
The worker fetches selected documents lazily. `hosted/families.json` maps exact
source IDs and provenance to asset families; update that mapping intentionally
when adding catalog art. Unmapped imports stay recoverable in Archive.

New creates a separate asset using the existing editor controls, even if its code
matches another asset. Save asset writes a draft version under the opened asset
and animation state. Catalog defaults remain accessible; saving is not approval. Save revision / Save & test also retain that
sprite in the Library, in addition to preparing an immutable test build. Earlier
versions remain accessible after a different sprite replaces their test slot.
Concurrent saves are rejected without overwriting another editor's work.

Open **A01 · Gun Arm** under Arms. Edit its pixels or
hand marker. In Rig, choose it in **Single arm**, and choose a weapon. The hand
point sits at the weapon's grip; Reach moves the assembly forward. Upper arm and
Forearm remain optional alternatives and are ignored when Single arm is selected.
To see edited arm art in a local game test, choose **Single foreground arm** as
the shared test target, then Save & test. Weapon-only saves retain the arm.
The arm inherits gun aim/facing and stays at trooper scale when weapons enlarge.
These Forge changes do not promote the arm to the public game's main branch.

The agreed next art steps are recorded in [ROADMAP.md](ROADMAP.md).

## Per-asset game scale

Open an asset, then Test in game / Shared Forge. **This asset’s scale** affects
only that open asset. Save asset remembers it with the sprite version; Save
revision / Save & test also carries it into the test build and exact release.
Opening another asset restores its own scale. New assets start at 1.

Older builds retain their original shared sizing. The first new test save freezes
those inherited sizes per asset, then applies the chosen scale only to the selected
asset. The foreground arm keeps its previous human-scale size unless edited itself.
Weapon grips stay fixed; muzzle effects and firing origins use the same per-asset
transform as the drawn weapon. Lighting settings remain shared across the build.
