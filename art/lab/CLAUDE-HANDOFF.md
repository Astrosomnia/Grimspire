# Grimspire Forge: handoff to Claude

Updated 2026-10-31. Read this on the current art/weapon-lab branch, then read
AGENTS.md and CHANGELOG.md. Repository files are authoritative; chat recollections
and browser drafts may be older. No private credentials are in this document.

## What Jarred wants

A shared browser Forge for Jarred, ChatGPT and Claude to riff on weapon art,
create alternatives, adjust anchors/lighting, test in the actual game, save exact
revisions and deliberately promote approved changes to main. Claude primarily
maintains gameplay/code; ChatGPT and Jarred primarily explore art. Renderer code
experiments are allowed inside the isolated sandbox. Ignore the old Claude
Artifact store for now: it is not synchronised and must not become a second source
of truth. GitHub is the authoritative shared source.

## Current state — distinguish implementation from deployment

- art/weapon-lab contains the original art lab, local companion and new hosted app.
- Hosted app implementation and offline tests are present under art/lab/hosted/.
- Jarred created a Cloudflare Worker and installed/configured a GitHub App.
- Account-side Git/build connection and first real hosted sign-in/save are still
  awaiting deployment/verification. A workers.dev address alone does not prove the
  application is deployed; it was initially created as Hello World.
- No art revision has been approved or promoted by ChatGPT. No main game, live
  atlas, Pages setup or existing forge-pipeline branch was changed by this work.
- Offline checks include hosted auth/RSA gateway, save/release/race/tamper tests,
  local real-Git flow tests, native Canvas rendering and the original release validator.
- No browser executable is installed in the build environment. Full interactive
  browser/real Cloudflare acceptance remains outstanding.

Deployment instructions and exact dashboard fields: hosted/DEPLOY.md.
Target URL: https://grimspire-forge.jarredpowell88.workers.dev/

## Branches and files

| Location | Role |
| --- | --- |
| main:index.html | Current game, with embedded atlases |
| main:debug/index.html | Game debug build |
| art/weapon-lab:art/lab/forge.html | Existing editable Forge UI; shared hosted controls are added at build |
| art/lab/releases/weapons-v001/ | Immutable first eight weapon studies, detail + grid, with hashes |
| art/lab/catalog.json | Current source-art review manifest |
| art/lab/hosted/worker.mjs | Hosted authentication, GitHub API, revision and release backend |
| art/lab/hosted/model.mjs | Validation, fingerprints and game generation |
| art/lab/hosted/bridge.js | Shared library/save/test/release controls |
| art/lab/hosted/library.json | Index for alternatives added directly by Claude/ChatGPT |
| art/lab/hosted/library/ | Individual added alternative Forge documents |
| art/lab/hosted/state.json | Runtime-created current revision, revision history and integrations |
| art/lab/hosted/revisions/<id>/ | Runtime-created immutable snapshots |
| art/lab/hosted/events/ | Runtime-created approval/deployment receipts |
| art/lab/sandbox/game.html | Editable pinned game-source experiment |
| art/lab/sandbox/base.json | Main commit that pinned source was based on |
| art/lab/sandbox/runtime.js | Weapon renderer adapter read at save time |
| art/lab/sandbox/serve.py | Earlier local-only companion; optional, not the hosted workflow |
| forge-pipeline branch | Your earlier sync/atlas tools; inspected previously and left untouched |

Do not merge the long-lived lab branch into main. Promotion creates a narrow
candidate from current tested main, changing only index.html, debug/index.html and
art/integrations/<revision>.json. The production game remains a single HTML file.
This v1 inserts an art renderer adapter rather than repacking the atlas. Reconcile
that deliberately with forge-pipeline later; do not stack competing overrides.

## Artwork and known limitations

W01 launcher/mortar; W02 carbine; W03 scatter; W04 dakka; W05 las gun;
W06 flamer; W07 chainsword; W08 claw/thunder fist. Existing game behaviours are reused.
Source-detail art is not native game-scale pixel art. Grid variants are automatic
reductions and still need pixel cleanup/rig review. W05 has a red-dot sight; W07
is horizontal with brighter blade edges; the previous flamer was retained.

The renderer supports frame animation, body, trim, emissive, grip/pivot, darkness,
emissive strength, glow, bloom and scale. Lighting controls apply to the saved
weapon set. It does not yet move firing/projectile origins to the Forge muzzle
marker; existing game effect origins/behaviour remain in force. Environment/trooper
lighting is still in game source. Do not claim anchors/effects are validated from
an import test. Old editor Ready is not release approval.

## How to supply alternatives directly to the shared Forge

1. Fetch/pull current art/weapon-lab. Keep an existing user's work; never force-push.
2. Read the current source document or hosted revision's payload/manifest. Name the
   revision and variant you are changing. Ask Jarred if the intended source is unclear.
3. Create a NEW native Forge JSON under
   art/lab/hosted/library/flamer-alt-01.forge.json (unique immutable descriptive filename).
   Schema: forge:1, code, name, w, h, fps, markers, frames. Each frame has body/emis/
   trim/guts as embedded PNG data URLs or null; layer dimensions equal w/h. Set a
   grip or pivot and in-bounds anchors. Keep ready:false and explain the change in notes.
4. Append to hosted/library.json:

```json
{
  "id": "flamer-alt-01",
  "path": "art/lab/hosted/library/flamer-alt-01.forge.json",
  "sha256": "SHA256_OF_THE_EXACT_UTF8_FILE_BYTES"
}
```

5. Commit the new document, index and CHANGELOG entry together. Push a normal
   fast-forward. If another save arrived, reconcile with it; never replace state.json
   or old snapshots to make a push succeed.
6. Jarred clicks Refresh shared library. The new document appears in Library. His
   unsaved canvas is retained. He chooses an existing W01–W08 behaviour to preview it,
   adds a note, saves a revision and tests it.

The library loads the source-art catalog, current saved set and indexed alternatives
from one pinned Git commit. It verifies their hashes. Do not assume adding arbitrary
files anywhere in the repo will make them appear. Keep IDs unique and preserve old
alternatives; add another ID/path for another version. Desktop browser drafts and
exports alone do not constitute shared persistence.

## Revision and publication guarantees

Save compares the editor's loaded lab head to current GitHub head. Stale clients
are rejected and told to refresh. It snapshots current main source (or an explicitly
rebased custom source), renderer, art/lighting payload, built game, notes and hashes
in one commit. Existing snapshots must remain immutable.

If custom sandbox game edits are on an older base, save stops for reconciliation;
it does not discard those edits. Otherwise it automatically uses latest main.
A main change after saving invalidates the release candidate and requires a new
save/test. Each test URL names an immutable revision rather than “whatever is latest”.

Review creates an art/release-<id> branch and focused PR. Go live requires explicit
approval of its fingerprint. The backend checks source main, lab head, candidate
head, full candidate tree and commit checks. Candidate's sole parent must be tested
main. The final reference update is force:false, so a concurrent main push rejects
it instead of overwriting Claude's newer work. Branch protection is not bypassed.
Integration receipts record approval and the exact main commit. Public deployment
is only verified when served game bytes match the expected fingerprint.

## Connection details (public identifiers only)

GitHub App name: Grimspire Forge. App ID: 5558397.
Client ID: Iv23liLKlHD9cghoqijI. Installation ID: 177300737.
Repository: Astrosomnia/Grimspire. Allowed owner user ID: 144634800.
Callback: https://grimspire-forge.jarredpowell88.workers.dev/auth/github/callback

GITHUB_PRIVATE_KEY and GITHUB_CLIENT_SECRET were entered by Jarred as encrypted
Cloudflare runtime secrets. Values were never supplied to ChatGPT. Never request,
commit or log them. The configuration preserves dashboard variables and secrets.
GitHub sign-in proves the user's identity; installation tokens perform repository
operations. Only the configured owner ID is admitted. Cloudflare's own Git build
integration is separate from this runtime app.

## Checks and next actions

```sh
cd art/lab/hosted
node build.mjs
node --test test.mjs
```

Additional local checks: python3 art/lab/validate.py;
python3 art/lab/sandbox/test_companion.py; optional native Canvas test_render.js.

Next: connect existing Worker to the configured branch/root, deploy, verify sign-in,
shared library, one draft save and its game preview. Confirm main is untouched.
Keep actual game art approval separate from infrastructure acceptance. Only then
exercise publishing on an exact revision Jarred actually wants in the game.

## Hosted deployment checkpoint — 2026-10-31

Cloudflare successfully deployed commit ca76a598f1c7a1a35e638213cf49b119cdf0320f
(version 85046993-4252-48d1-87f5-1a11a586114a). Jarred reached the signed-in
editor. Repository access then failed at the private-key parse/sign step.

The follow-up key-loading change uses native Web Crypto RSA signing, wrapping
GitHub PKCS#1 keys in PKCS#8 when required and accepting literal escaped newlines
as well as normal/CRLF PEM text. /health reports only private_key.readable, format
or a fixed reason code; it never emits key contents or a key fingerprint. The
user's actual secret has not been read by ChatGPT. Do not assume the paste was
wrong based on the original catch-all error. Verify the new deployed health result
and repository connection before calling authentication resolved.

Hosted tests now cover both RSA formats, newline/quoted clipboard variants and
non-disclosure in diagnostics (17 passing tests at this checkpoint).

## GitHub transport follow-up — 2026-10-31

Live /health on deployed commit 6221f65ba51bbe0c24ca1829e468083bcea20030
confirmed private_key.readable=true, format=pkcs1 and configured=true. The key
material Jarred entered is readable; no credential replacement is indicated.

Jarred then encountered the generic backend error during shared-library startup.
The GitHub client's native fetch reference had been stored as an object method,
which supplies the client instance as its receiver. Cloudflare workerd requires
the native global receiver; the corrected transport explicitly preserves it.
A regression test models that receiver requirement (Node's ordinary fetch mock
did not enforce it). Transport errors now have fixed, non-secret categories;
unexpected backend errors include operation/type instead of the old catch-all.

19 backend tests pass. The receiver fix needs confirmation in the user's live
repository session after deployment; key parsing itself was verified live.

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
