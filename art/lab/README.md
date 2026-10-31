# Grimspire Art Lab

An isolated space for Jarred + ChatGPT to explore art while Claude primarily
maintains the game. Branch: `art/weapon-lab`. This branch is not a deployment.

## Start

Open `index.html` directly in a browser for review, notes, anchors and JSON export.
Open `forge.html` for pixel editing, layers, animation and rig tools. Both pages
are self-contained and work without a server. Forge's Library contains all eight
weapons in source-detail and grid versions. The review page's exported JSON can
be imported into Forge and the game Proving ground.

Browser changes are local working drafts. Downloading JSON does not commit to
GitHub or sync with Claude. To preserve changes, send the exported file back for
a new repository revision. The downloaded original Claude-hosted Forge has its
own storage; it is a separate store from this repository workspace.

## Boundaries

Only `art/lab/` is changed by this workspace. Live `index.html`, `debug/index.html`,
`art/in-game/`, existing kits and `tools/build.py` belong to game integration.
No game code is copied into the Lab, so Claude's newer game changes cannot be
accidentally overwritten by merging an old game snapshot from this branch.
The gallery is an artwork preview, not proof of gameplay correctness.

## Version and approval rules

`releases/weapons-v001/` is the initial immutable review snapshot. After this
initial commit, create `weapons-v002`, etc. rather than editing previous source
files or manifests. Keep each release manifest's SHA-256 hashes aligned with its
Forge files. `catalog.json` identifies the current review revision. Update the
review/Forge pages to that release and add a CHANGELOG entry together in one commit.

Statuses: draft → review → approved → integrated. Approval is explicit from
Jarred and identifies asset code, variant, revision and file hash. Source-detail
approval is not approval of the automatically reduced grid artwork. Track checks
per variant: pixel cleanup, scale, anchors and in-game preview. Record integration
commit and PR after integration, not in advance. Approval/integration records go
in a new revision or appended change-log entry, preserving previous snapshots.

## Passing approved art to Claude / going live

1. Choose exact approved asset(s), variant(s) and revision; update the record.
2. Refresh from current `main` in a NEW integration branch. Avoid wholesale
   merging this long-lived Lab branch as a game update.
3. Supply Claude the manifest, matching Forge documents and the change-log notes.
4. Claude checks current game mappings, scale, rig, effects and behaviour; exports
   body/emissive/trim layers and updates the game's packed atlas and source.
   Existing art paths alone do not update embedded runtime atlases.
5. Open a focused PR against current main listing exact approved revision/hashes,
   checks and affected assets. Review against current game code; no force-push.
6. Merge/deploy when Jarred requests promotion, verify the deployed result, then
   append the integration commit, PR and deployed status to the Lab notes.

Do not enable automatic production deploys from `art/weapon-lab`. Publishing a
separate Lab preview is a separate decision; this setup does not change Pages.

## Existing Claude pipeline

At setup time the repository also has a separate `forge-pipeline` branch
(`e6a2dfc705c24f01ee1154c39814c901e3b25a5c`) with Claude's Forge sync/atlas
integration work. This Lab does not modify or merge that branch. Its documented
pipeline uses `tools/forge_sync.py`, `tools/build_atlas.py` and generated
`art/forge/` kits. Let Claude reconcile that pipeline with current main when
integrating approved art. Do not edit generated kits by hand or run a pruning
sync against only this experimental subset; other game assets must be retained.
Only explicitly approved art variants should be marked ready for packing.
