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

## Remaining six animated weapons — weapon-lighting-v001 (2026-10-31)

Added six separate alternatives to the hashed shared Library; original assets and prior alternatives are unchanged:
- W02 Rail Carbine — charge sweep: four cyan rail capacitor lamps, 40 frames / 2 s.
- W03 Scatter Gun — twin chamber pulse: alternating upper/lower amber chamber lights, 40 frames / 2 s.
- W04 Dakka Bolter — staggered charge: three rolling amber charge pips plus staggered original cyan indicators, 20 frames / 1 s.
- W06 Promethium Flamer — furnace shimmer: warm orange chamber and four vent lights, smooth combined heat waves, 40 frames / 2 s. This alternative recolours the original blue emissive to orange.
- W07 Chainblade — edge chase: magenta energy wave along both blade edges and breathing drive core, 40 frames / 2 s. Teeth geometry does not move.
- W08 Thunder Fist — knuckle surge: slow magenta core feeds three knuckle lights, 60 frames / 3 s.

All run at 20 fps and loop with smooth overlapping light envelopes. New lamps sit within existing opaque body areas, with bounded dark lamp-seat pixel edits (8/4/3/12/10/6 respectively); alpha/silhouette, dimensions, anchors, scale, trim/guts and all other body pixels remain unchanged. No gameplay timing, firing rules, geometry or 2x-density migration. Sources are weapons-v001 grid documents; current saved set contained only W01 and W05 and was preserved.

Manifest and six-second animated comparison: releases/weapon-lighting-v001/. Documents: hosted/library/W0X_<effect>_v001.forge.json. Library index/catalog register the additions; current_review stays weapons-v001. Each remains draft; in-game visual approval outstanding. No live release.

Validation: all nine alternative documents match their index hashes and pass Forge model validation. Native Canvas loads all frames through the actual sandbox runtime and renders 40/40/20/40/40/60 distinct frames. Source silhouette/anchor/bounded edit invariants checked. 27 hosted tests pass, including accumulation of all eight animated weapon slots into one immutable test build without dropping any frames or changing main.

Animation library follow-up: validate repeated layer strings once per document and copy only the 24-byte PNG header after full base64 syntax validation. This preserves all existing validation rules while avoiding repeated body decoding/copying across frames. Local validation of all nine animated alternatives (332 frames) decreased from about 42 ms to 5 ms; this is a local measurement, not a Cloudflare latency guarantee. 28 hosted tests pass, including malformed base64/PNG rejection in late frames.

## Approved main-game release — 2026-10-31 (Vancouver)

Jarred explicitly approved the eight animated weapons for the main game. Immutable combined revision: 20261101T014956Z-14b37379; lab snapshot commit 9918ffa4c2a26d43da51781dc1cb9e3564ff4780. Focused PR #1: https://github.com/Astrosomnia/Grimspire/pull/1 (merged). Main integration commit db0b85b263bff04befb5c7755793478bc3b54f3b is a direct child of prior main 2974b27b8d230ed6d22042fe6e91f37e3cdbf9d4. Only index.html, debug/index.html and art/integrations/20261101T014956Z-14b37379.json changed. The lab branch was not merged.

Exact selected set: W01 slow pulse, W02 rail sweep, W03 twin chamber, W04 staggered charge, W05 red sequence, W06 furnace shimmer, W07 edge chase and W08 knuckle surge. Latest saved settings were retained: darkness 0.6, emissive 1, bloom 2, scale 1.2, glowColor #ffff00. No 2x-density upgrade, prop dummy, mechanics or collision changes.

Game SHA-256: 8345a7a139d137b7bb21e29f603155e988c799c1398f10e82f8e6f47ab3c0b82. Source preserved exactly after removing adapter. Main/debug scripts compile; all frames rendered with the actual adapter at the approved saved settings; 28 hosted tests passed. Full immutable source/runtime/payload/game/manifest live under hosted/revisions/<revision>/.

GitHub Pages build/deploy succeeded. Live https://astrosomnia.github.io/Grimspire/ was inspected in the browser: embedded revision matches, all eight names/frame counts/fps and settings match, a local Commanders battle starts and renders, with no game-origin console errors observed. Verification scope is Pages commit + live DOM payload + battle smoke test; full HTTP body bytes were not fetched/hash-checked. Deployment evidence and approval are recorded in hosted state/events. Do not edit prior immutable snapshots.

An additional Cloudflare Workers check on the main commit reported failure; the Forge is built from art/weapon-lab with root art/lab/hosted, which is intentionally absent from the focused main tree. The Pages game deploy succeeds independently. If this unwanted main-branch Forge build persists, restrict Cloudflare non-production build branches in the dashboard; do not copy the Forge app into main merely to satisfy that check.

## 1.2-scale hand and muzzle alignment correction — 2026-10-31 (Vancouver)

Jarred requested retaining the enlarged 1.2 weapon scale while correcting handles and muzzles, with authorization to push. The previous adapter pinned the custom grip to the old barrel row rather than the old hand row; several initial sprite anchors were approximate, and ranged origins still used a fixed 13-world-pixel offset.

New immutable anchor-alignment-v001 documents calibrate all eight grips/pivots and muzzle points. Their bodies, all animation-frame layers, dimensions and scale remain byte-for-byte unchanged. The active eight animated Library entries point to these corrected documents; old assets remain immutable and available by their prior paths. Library names are unchanged.

Renderer now scales about the calibrated grip and preserves the original game hand location. A shared rig projects muzzle markers through the same aim, facing, leg drop, squash and tilt transforms as drawTrooper. All six ranged weapons use those origins for projectiles, traces, beams, fire and muzzle effects; other tools and melee keep their existing combat behaviour. A hand-to-tip terrain check prevents firing through cover with the extended barrel. Ranged reticles use the firing origin. Geometry comes from synchronous payload metadata, independent of asynchronous PNG loading. Simulation protocol increments 16 -> 17 because origin positions affect simulation; clients must refresh to play together.

Validation: sandbox/test_alignment.cjs calls the actual drawTrooper function with Native Canvas and checks 768 combinations (eight assets, four scales, two facings, four aim angles, three poses). Grip location is scale-invariant; six ranged muzzle origins match actual draw transforms to 0.0001 world pixels; tool fallback, blocked-barrel collision and pre-load determinism pass. Existing native weapon/category rendering and all 28 hosted tests pass. No animation pixels or lighting settings changed.

Sandbox source includes only two intentional edits beyond the existing adapter: protocol 17 and ranged reticle origins. Pin sandbox/base.json to the resulting main integration commit after release, so future shared saves do not see this completed correction as an unreconciled stale experiment.

### Alignment correction deployed

Merged focused PR #2: https://github.com/Astrosomnia/Grimspire/pull/2. Main commit eb12d9ff299b7deb773ead33c988d49f5b6eef97 is a direct child of db0b85b263bff04befb5c7755793478bc3b54f3b; only index.html, debug/index.html and the new integration receipt changed. Immutable revision 20261101T021713Z-61d0807f, snapshot 7deef79f4eb20048a8bd95ebba0e939c7d9be12e, staged rig code 37a210fc232cccbf8d067b9e2367c6f6f08fa324. Game SHA-256 97f3d7a8473d060c72ad30791ce471b4afbfe2eef48a6062d2e0d7c1d363bcc1.

GitHub Pages deployment passed. Browser verification found the exact corrected revision, scale 1.2, all eight calibrated anchors/frame counts and protocol 17 on the public page. A local Commanders battle rendered; selected Las Burner and fired successfully (ammo 9 -> 8), with no game-origin console errors. Full HTTP response bytes were not hash-checked. The native alignment harness verifies the firing/visual projection across 768 cases. Both lab code and snapshot commits passed Forge CI. The unrelated Forge Worker build on the focused game branch still fails because that tree omits the Forge application; no check was rewritten or branch protection bypassed.

Re-pinned sandbox/base.json to eb12d9ff299b7deb773ead33c988d49f5b6eef97. The clean sandbox source matches the new main source after removing its adapter. Future saves retain corrected rig behaviour and no longer treat the protocol/reticle correction as an unfinished stale experiment. Preserve old releases and journal entries. Old multiplayer clients must refresh for protocol 17.

## Straight gun forearm and glove — gun-hand-v001 (2026-10-31 Vancouver)

Jarred requested a simple arm and gun hand, without an articulated shoulder/elbow. Added a code-native pixel-art sleeve, cuff, glove, thumb and finger marks to the sandbox renderer. It follows the existing weapon aim/facing/pose transform, attaches at the corrected grip position and draws once after the normal weapon pass. Rim passes do not duplicate it. It uses trooper pixel scale rather than the weapon's 1.2 multiplier, keeping human proportions stable as weapon size changes.

Applies to the six guns (mortar, rail, scatter, Dakka, las and flamer). Chainblade/fist/tools and the underlying sprite files are unchanged. Anchors, firing origins, animation frames, lighting settings, physics and multiplayer protocol 17 are unchanged. No new full limb rig or IK.

Preview: releases/gun-hand-v001/gun-hand-preview.gif, rendered with the actual embedded trooper atlas/legs, baked team materials and actual drawTrooper function, showing right/left facings and the enlarged weapons. Manifest records draft status. This is a first pass for visual review in the shared Forge; it has not been promoted to main.

Validation: 768 actual draw transforms still pass, plus normal/rim pass layering, single arm per gun pass, stable hand size across weapon scales, non-gun exclusion and canvas transform restoration. Native weapon/category checks and all 28 hosted tests pass. The alignment harness now preserves the actual renderer wrapper rather than replacing it after initialization, so these checks exercise the foreground hand path too.

## 20261101T033715Z-a104eab1 — Saved gun arm review build

First playable review of the straight foreground gun arm and glove on all six guns. Preserve all eight approved animated weapons, calibrated grips/muzzles and saved 1.2 scale/lighting. No main promotion.

- Source: 64824886956299daac0ecfca9fdaa1c3f9dccba4; baseline main: eb12d9ff299b7deb773ead33c988d49f5b6eef97.
- Draft, awaiting Jarred's visual review. No approval or main integration.
- Validation: 768 actual drawTrooper alignment cases and all 28 hosted tests pass; saved game scripts compile. Snapshot pins source, renderer, full eight-slot payload and SHA-256 hashes.

### Forge catalog and single-arm assets · 2026-10-31

- Index 161 existing source/study/archive assets with SHA-256, thumbnails and
  registered animation frames; preserve originals and game atlas crops.
- Add lazy open, search and category filters to the hosted Library.
- Save every sprite independently in GitHub, including each test revision's art.
- Add A01 single-gun-arm-v001, matching the existing procedural sleeve/glove pixels.
  Single arm in Rig uses a hand point and existing Reach, over the gun. Saved ARM
  sprites drive the game preview and survive subsequent weapon-only saves.
- Checks: all indexed hashes and PNG dimensions/anchors; independent-save retention
  and stale-save refusal; 31 hosted tests; single-arm rig layering/reach; 768 native
  alignment cases with sprite arm plus game category tests. Game main unchanged.
- App update authorized by Jarred; artwork remains draft. Authenticated hosted UI
  verification pending deployment and an available signed-in browser.

## Library families — 2026-10-31

- Replace top-level duplicate browsing with 32 current asset families and four archived references. All 161 catalog documents and nine original registrations are retained unchanged.
- Explicitly map provenance and defaults in hosted/families.json; weapon defaults use the aligned W01–W08 catalog versions. No approval records changed.
- Keep trooper animation states and component overlays inside their asset; preserve complete layers, frames, source resolution and historical document IDs.
- Carry stable asset/state identity through open, browser recovery/export and both shared save paths. Save adds a draft version; New creates a separate asset regardless of display code.
- Keep original catalog defaults accessible alongside drafts. Recover legacy saved-build identity from exact content fingerprints.
- Preserve the single foreground arm, Reach, independent saves, stale-write protection and focused game-release rules. No public-game source or art was changed.
- Checks: hosted save/release tests plus migration completeness, new-versus-version identity, trooper state retention and legacy provenance; local browser verified grouped browsing and four-frame Walk opening. Signed-in hosted saving remains unverified.
- Next: the ordered art plan is recorded in ROADMAP.md.

## Scrollable frame strip — 2026-10-31

- Prevent long animations from expanding the editor's centre grid column and pushing the sidebar off screen.
- Cap the strip at five fixed-width frame thumbnails; overflow scrolls horizontally, with fewer visible on narrow layouts.
- Preserve existing frame selection and automatic scrolling to the selected frame.
- Browser checked a 60-frame animation at 1363px: five fully visible thumbnails, no page overflow, sidebar inside viewport, and scrolling reaches frames 56–60.
- UI layout only; no artwork, saved revisions, runtime or public game changes.

## Responsive frame strip — 2026-10-31

- Replace the five-frame cap with a strip that fills the available width up to the sidebar and scrolls horizontally.
- Size thumbnail cells responsively to leave a 24px glimpse of the next frame when more frames remain.
- Preserve the constrained grid column so long animations cannot push the sidebar outside the viewport.
- Browser checked 60-frame artwork at 900px, 1363px and 1800px: the strip fills available space, clips a partial next frame and keeps the sidebar inside its viewport.
- UI only; all existing artwork and saved builds retained unchanged.
- Correct the migration test fixture to use original mapped registrations, independent of newer user drafts. New draft saves must not invalidate initial-default assertions or block application deployment.

## Per-asset game scale — 2026-11-01

- Replace the shared scale control with This asset’s scale, persisted on sprite versions, recovery/export, test payloads and exact releases.
- Keep unedited assets at their effective sizes when migrating an older shared-scale build; preserve the arm's previous human-scale treatment. Old immutable snapshots are unchanged.
- Use each asset's scale in artwork drawing and the weapon grip/muzzle transform, including origins before PNGs finish loading and wall blocking.
- Restore the opened asset's scale in Forge, including historical revisions and older registered art. New assets start at 1. Lighting remains shared.
- 36 hosted tests pass, including legacy migration, independent scale retention, sprite validation and version round trips.
- Native canvas checks pass across eight weapons, four scales, two facings, aim/pose combinations in both legacy and independent-scale modes; grip fixed, ranged muzzle exact, arm independent.
- Local browser preview with simulated storage verified claw 0.8 save/reopen and rifle remaining at 1.2. Signed-in hosted save walkthrough remains unverified.
- Application/UI and sandbox renderer only. No artwork or public-game main files changed; new sizes require the usual saved test and exact-release approval.

## Shared shoulder pivot — 2026-11-01

- Rotate all eight current held-weapon test slots and the straight arm around the trooper's shoulder, using the existing full-source shoulder/body-anchor coordinates.
- Keep Grip as the hand attachment. Resolve the assembly pivot from the arm shoulder rather than overwriting weapon art's standalone markers.
- Keep shoulder, glove, grip, scaled weapon and muzzle transforms consistent through aim, facing, pose and arm/weapon scales. Trace firing obstruction from the shoulder so an extended hand cannot bypass a nearby wall.
- Keep the arm over gun/blade grips; put it behind the claw's replacement gauntlet. Thrown and unregistered tools retain their separate path.
- A01 shoulder-v002 changes only Pivot metadata to Shoulder; pixels unchanged. Register a new immutable source version under the same asset family and retain the previous version.
- Fix Rig Reach to extend from a fixed shoulder; apply each chosen part's scale and keep its hand/grip connected.
- Checks: 36 hosted tests, category checks, native renderer alignment/shoulder/contact tests across all eight held assets, and native Rig tests at multiple aim/reach/weapon scales pass. Inspected a 24-pose render using the actual trooper/leg atlases.
- No saved snapshots or public-game main files changed. Artwork remains for exact saved-build visual review; throwing-arm art/animation is a separate next step.


## ash-legion-jumppack-v001 — 2026-11-01 — experimental

- Added T09 Ash Legion jump-pack body and A05 single foreground arm from the art-direction handoff as separate Current assets with stable unique identities.
- Preserved original native pixels, anchors, separate glow and false approval/test flags. Short mantle and pack are static; body has one idle frame.
- Recorded exact document hashes and reduction limitations in releases/ash-legion-jumppack-v001/manifest.json, with an assembled preview.
- Verified current sprite validation, new entry visibility and preservation of every previous asset family/current selection. No runtime, main game, saved revision or test-slot changes. In-game fit and motion remain untested.
