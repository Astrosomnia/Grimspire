# Art Lab change log

## weapons-v001 — 2026-10-31 — draft

- Workspace created on `art/weapon-lab`, based on game commit `ae7247a9b94aeb834342cd40e8aea2eb82308bb8`.
- Imported eight source-detail studies and eight grid interpretations.
- Las Burner: red-dot sight and laser-emitter muzzle cue.
- Chainblade: horizontal pose and brighter steel edge.
- Flamer: previous detailed trace and 47×20 grid version retained.
- Confirmed W01–W08 mappings against the repository's pixelkit-v2 manifest.
- Added initial grip/pivot/muzzle points; not yet approved against the trooper.
- Detailed artwork remains source resolution, not game-native pixel art.
- Automatic grid reductions need cleanup. All entries remain draft.
- Validation: Forge layer pixels round-trip through its import/render/export functions.
- Live game impact: none. No runtime, atlas or build files changed.

Append each new revision's changed assets, reason, checks, approval and integration
commit/PR here. Never describe a revision as live until the integration and
deployment have actually been verified.

Existing-work note: `forge-pipeline` already contains Claude's sync/packing work.
It was inspected for compatibility and left untouched. See the workflow README.

## Git-linked sandbox v1 — 2026-10-31 — implementation, not deployed

- Added a local Git companion and Forge controls for save, game test, refresh,
  focused release review and explicit Go live approval.
- Pinned a sandbox copy of main at ae7247a9b94aeb834342cd40e8aea2eb82308bb8.
- Added weapon sprite/frame rendering and darkness, emissive, bloom, scale and
  glow-colour controls. New art can preview using an existing W01–W08 behaviour.
- Saves capture source, adapter, art/settings payload, notes and file hashes in
  immutable revisions; failed pushes report local-only persistence.
- Release preparation creates a focused branch/PR. Publication uses an atomic
  fast-forward lease and records the exact approved build and integration commit.
- Refuses stale main, tampered snapshots, unrelated dirty work and changed release
  branches. Repeat-release refresh removes the previous injected adapter.
- Validation: seven Git/HTTP flow tests; HTTP origin/path checks; native Canvas
  loading/render/fallback checks; source syntax and original 16-variant validation.
- Browser interaction remains unverified: no browser executable is installed.
- Main, live assets, deployment configuration and forge-pipeline remain unchanged.

Baseline refreshed to `2974b27b8d230ed6d22042fe6e91f37e3cdbf9d4` after a concurrent README-only main update. Game source is byte-identical to the checked baseline; no runtime conflict.

## Hosted Forge v1 — 2026-10-31 — code prepared, deployment awaiting verification

- Added owner-only GitHub sign-in and a Cloudflare Worker backend using the existing
  GitHub App; private credentials remain in Cloudflare's encrypted runtime secrets.
- Added GitHub-backed Library, immutable save/test revisions and indexed alternatives
  Claude can add directly. Stale editor saves are rejected; unsaved canvas is retained.
- Snapshots bind game source, renderer, art/settings, notes and hashes in one commit.
- Added focused PR preparation, explicit exact-build approval, full-tree checks,
  non-force atomic publication and integration/deployment receipts.
- Added public deployment verification by matching actual served game bytes where
  GitHub Pages can be discovered; main update alone is never labelled verified live.
- Added deployment instructions and CLAUDE-HANDOFF.md with canonical paths and limits.
- Offline hosted tests: 15 passing cases covering save/release concurrency, stale
  bases, auth/CSRF/session checks, RSA signing, tampering and large-file blob reads.
- Local Git/HTTP, original asset validation and native Canvas checks remain available.
- Real Cloudflare runtime, credentials, browser UI and public deployment remain to
  be verified after Jarred connects the existing Worker to this prepared source.
- No main/game files, production hosting settings or forge-pipeline files changed.

## Hosted key-loading follow-up — 2026-10-31

- First Cloudflare build succeeded and Jarred reached the editor after GitHub sign-in.
- Repository authentication failed in the previous combined PEM parse/sign catch.
- Replaced node:crypto PEM/signing with native Web Crypto; support GitHub PKCS#1
  and PKCS#8 plus CRLF, escaped-newline and JSON-quoted clipboard text.
- Added fixed, non-secret key-readability diagnostics to /health and specific errors.
- Editor now labels the failed connection explicitly instead of staying Connecting.
- 17 hosted tests pass. Actual key readability/connection still needs post-deploy
  verification; no private secret was accessed and main is untouched.

## Hosted GitHub transport follow-up — 2026-10-31

- Live key diagnostics confirmed that the configured PKCS#1 key is readable.
- Fixed native fetch receiver preservation in the GitHub client for Cloudflare.
- Added regression tests for receiver-sensitive fetch and safe transport errors.
- Unexpected backend errors now identify operation/type without exposing secrets.
- 19 hosted tests pass; full live repository connection still requires verification.

## Category testing and launch repair — 2026-10-31

Hosted Save & test supplies a default update note, keeps save errors visible in the reserved tab, and leaves an exact-revision link even when a popup is blocked. Library refresh failure no longer hides a successful save. Test URLs use `grounds=1` to start a local hotseat battle automatically with unlimited timer and Forge placement controls.

Targets: W01–W08 weapons, PROP (ground prop/set piece), TROOPER (static frame/part), BACKGROUND (static background/skyline). C/S/E codes default to PROP, T/A to TROOPER, B to BACKGROUND; users can override the target. Nonweapons do not require grip/pivot. Props anchor at `[w/2,base+1]`, or bottom centre `[w/2,h]` without a baseline. Place on a terrain surface by tapping, add nearby or clear props. Payload records selected_slot; no weapon slot is overwritten by a prop.

These category dummies test visual placement only. Props have no collision/destruction; trooper replacements are static frames with facing and position, without articulated rig; background is a static world placement, without parallax integration. Release preparation blocks snapshots containing category dummies until Claude implements their real game integration. Existing weapon release protections and immutable snapshots remain active.

Validation: 24 hosted tests including blank notes, popup fallback, visible save errors, category persistence and release guards; Native Canvas weapon regression plus category harness covering automatic local launch, prop pixels/baseline, map placement and trooper fallback. Authenticated hosted browser acceptance remains outstanding. Main unchanged.

Weapon saves include a checked “exclude category dummies” option, so prior prop experiments do not permanently block weapon releases. Older category revisions remain immutable and accessible through history.

## Collaborator roles and readable working surfaces — 2026-10-31

- Owner identity remains ALLOWED_GITHUB_USER_ID. Invite collaborator numeric GitHub account IDs with Cloudflare runtime variable COLLABORATOR_GITHUB_IDS, comma separated (example: `123456,987654`). No collaborators are enabled by this code change. Resolve usernames to their numeric IDs before adding them. Keep the list in Cloudflare; keep_vars preserves it on deploy. Do not add spaces inside an ID or use usernames in this field.
- Invited users need only a GitHub account and the Forge link, not repository write access or Cloudflare access. They may draw, save and test. prepare/publish/check-deployment require the owner on the server, independent of client buttons or a session role field. The invite list is checked on every request; removal revokes existing sessions. The release button is hidden for collaborators. Direct repository permissions remain a separate concern.
- Drawing toolbar now includes Board: transparency grid or solid colour, a colour picker and Light/Dark shortcuts. Preferences persist in local browser storage; they do not modify sprite pixels, serialization or exported transparency. Lit mode also respects the selected solid board.
- Preview backdrops are now labelled Stone wall and Sump water, with visible masonry/ripple textures. Neutral grey and Board colour are additional readability options; Transparent remains available. These are illustrative view backdrops, not exact game lighting simulations.
- Checks: 25 hosted tests pass, including collaborator editor access/save attribution, direct release endpoint denial, forged-role denial and revoked-session denial. All editor inline scripts compile; native Canvas preview render checks pass. Main and immutable saved art revisions unchanged.

## Weapon pulse alternatives — pulse-v001 (2026-10-31)

Added W01 slow pulse (40 frames at 20 fps, 2 s period) and W05 quick pulse (20 frames at 20 fps, 1 s period) as extra shared-library entries. Only emissive alpha follows `(1-cos(2*pi*frame/count))/2`; no held on/off states. Full peak matches source emissive; trough reveals the unchanged underlying body. W01 uses Jarred’s latest saved W01 from revision 20261031T224300Z-d1a36881 (preserves his current colours); W05 uses weapons-v001 grid source. Bodies/trim/guts, emissive RGB, dimensions, anchors and scale remain unchanged. No 2x-resolution experiment included.

Files: hosted/library/W01_slow_pulse_v001.forge.json and W05_quick_pulse_v001.forge.json; immutable release record and animated comparison at releases/pulse-v001/. Catalog records the alternative release; current_review stays weapons-v001. Hosted library index hashes the two documents. No existing saved revision or main file is edited.

Checks: every body/trim/guts frame equals its source, anchor/dimension equality, unchanged emissive RGB, smooth symmetric wrap and exact zero/full intensity verified. Actual sandbox renderer under Native Canvas loads both animations and produces increasing dark/mid/peak pixel brightness. Model validation passes for both docs. Art/in-game readability approval pending. Open either named pulse alternative in shared Library, play, then Save & test using W01 or W05. The source-detail variants are unchanged.

## Four-lamp las sequence — laser-sequence-v001 (2026-10-31)

Added `Las Burner — red charge sequence`, W05, as a new shared-library alternative. Four two-pixel red lamps along the barrel at (26,9), (29,9), (32,9), (35,9) brighten rear to muzzle, with smooth overlapping cosine-cubed envelopes. 32 frames at 20 fps, 1.6-second loop, peak frames 0/8/16/24. Eight underlying body pixels form dark red lamp seats. Body alpha/silhouette, dimensions, anchors, trim/guts and all other body pixels remain unchanged. Existing cyan emissive still pulses smoothly. No firing-trigger or gameplay behaviour changes; no 2x-density work. Previous pulse alternatives and saved art remain immutable.

Multi-weapon testing already accumulates saved slots: save W01 with Save revision, open/save W05, then launch Save & test once. A new regression verifies both animated documents are present unchanged in that final snapshot. Saving to the same slot replaces that slot only in the new snapshot. Props still have one shared dummy slot; several distinct prop documents are not yet supported together. Added concise batching guidance in the Shared Forge dialog.

Checks: source pixel bounds and unchanged alpha/anchors verified; four peak times and smooth wrap verified; model validation and multi-slot snapshot tests pass. Preview GIF and manifest are in releases/laser-sequence-v001/. In-game visual approval pending; nothing published to main.
