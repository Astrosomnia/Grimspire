# Art workspace instructions

- This directory is an art workspace. Preserve Claude's role maintaining runtime code.
- Work on art/weapon-lab or a short-lived art branch. Do not push experiments to main.
- Limit routine art edits to art/lab/. Do not overwrite root game HTML, debug build,
  existing kits, live atlases or build tools without an explicitly requested integration.
- Treat committed release directories as immutable. Add the next revision, update
  catalog and preview snapshots, and append CHANGELOG in the same commit.
- Keep original and grid variants distinct. Do not claim automatic resizing is a
  hand-cleaned or pixel-identical reproduction. Do not label source resolution game scale.
- Record asset code, revision, variant, content hash, changes, checks and approval.
- Notes and anchors edited in a browser require exported JSON and a new Git commit.
  Local storage does not constitute repository persistence or shared approval.
- Never set ready/approved/integrated just because a file imports. Jarred approves
  exact assets; game scale/rig/effects require actual in-game verification.
- To promote, create an integration branch from latest main and a focused PR.
  Do not merge a stale full Lab tree or deploy the long-lived art branch to production.
- Keep live status tied to an integration commit and verified deployment; do not guess.
