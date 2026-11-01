# GRIMSPIRE — handoff to Claude

Updated 1 November 2026 (Vancouver). This overview supersedes the historical entries
below where they conflict. It consolidates available Forge, weapon, character and
worldbuilding context from the recent work; it is not a complete transcript of
every gameplay discussion. Read `AGENTS.md`, `CHANGELOG.md` and current source before
editing. GitHub is authoritative for shared assets, code and revisions.

## Working arrangement and immediate direction

Jarred and ChatGPT primarily develop art and visual direction; Claude primarily
maintains gameplay/runtime code. Jarred explicitly wants further art jamming in
the ChatGPT conversation, outside the other Codex chat, while selected assets are
supplied to the shared test Forge. Preserve this split and the established upload
route. The old Claude Artifact and disconnected local Forge copies are not shared
sources of truth.

Immediate creative goal: continue the Ash Legion trooper, retaining the imposing
knight-priest silhouette while adding gothic/macabre character and visibly
illuminated technology. Account for existing jump packs and animation. The latest
body/arm are experimental fit-tests, not an approved replacement or a completed
animation system.

## Current repository and service checkpoints

| Item | Location / observed state |
| --- | --- |
| Repository | https://github.com/Astrosomnia/Grimspire |
| Public game | https://astrosomnia.github.io/Grimspire/ |
| Shared test Forge | https://grimspire-forge.jarredpowell88.workers.dev/forge.html |
| Forge health | https://grimspire-forge.jarredpowell88.workers.dev/health |
| Forge branch | `art/weapon-lab` |
| Lab head inspected before this documentation update | `84114d095b0976fb519e1bcc012455abed5e2f7d` |
| Main head observed during this update | `f603f22795f41603584ccd784d27e0b6d6787083` |
| Latest saved test in inspected state | `20261101T094357Z-78228871`, ARM, “Test Gun arm · shared shoulder pivot as Single foreground arm” |
| Today's Ash Legion asset addition | `84114d095b0976fb519e1bcc012455abed5e2f7d` |

These are observed checkpoints, not fixed future heads. Refresh current refs before
writing. Browser saves advance the lab branch separately from the deployed Worker
code; those SHAs need not match. The hosted service has been deployed and used for
shared saves: do not restart its setup based on older “awaiting deployment” notes.
This documentation session did not perform a fresh hosted browser or public-game
walkthrough.

## Implemented Forge and weapon work

- Eight animated weapon alternatives were approved and integrated through focused
  releases. W01 slow pulse; W02 rail sweep; W03 twin chamber pulse; W04 staggered
  charge; W05 four red lamps sequencing rear-to-muzzle; W06 furnace shimmer;
  W07 edge chase; W08 knuckle surge. These are looping emissive animations, not new
  combat timings. Existing source/detail/grid variants remain distinct.
- The 1.2 weapon enlargement was retained and corrected: grip alignment, visible
  barrel-tip muzzle markers, ranged projectile/effect origins and reticles use the
  same transforms. Nearby cover blocks the extended weapon path. Historical
  alignment release incremented simulation protocol to 17; consult current game
  source before making any new protocol claim.
- Library cleanup is implemented. One card per asset, versions/sources inside it,
  trooper animation/component states grouped, references in Archive. Stable asset
  identity is separate from display code, document/version ID and test slot.
  Save adds a version; New creates an asset. Existing artwork/history is retained.
  Today's two additions bring the organised collection from 36 to 38 families.
- Animation frame strip is responsive, scrolls horizontally and peeks the next
  frame when more remain. The earlier five-frame cap was superseded.
- “This asset's scale” is implemented and persists with versions, exports and saved
  tests. Changing one asset preserves the others' effective scales. Grip/muzzle
  transforms follow the selected scale; the arm has independent scale. Lighting
  settings remain shared. Jarred's motivating example was reducing the claw
  without shrinking the larger guns.
- A01 is one editable foreground arm, not a mandatory upper-arm/forearm pair.
  Single arm plus Reach remain available. All eight current held-weapon test slots
  rotate with the arm around the trooper shoulder; Grip remains the hand
  attachment. The renderer resolves the assembly pivot from the arm shoulder
  rather than rewriting every weapon's standalone marker.
- Shoulder, arm/glove, weapon grip and muzzle stay connected through aim, facing,
  pose and scale. Reach extends from a fixed shoulder. Arm is drawn over gun/blade
  grips and behind the claw replacement gauntlet. Thrown/unregistered tools keep
  their separate path. Jarred wants thrown weapons to have a different arm and
  throwing motion, potentially animation; that is not delivered by the held rig.
- Existing rig/reach functionality must remain. Do not expand this into mandatory
  full elbow articulation before it is wanted.

Source detail: `CHANGELOG.md` records the implementation and verification for
library families, responsive frame strip, per-asset scale and shared shoulder
pivot. Historical test counts reached 36 hosted tests plus native alignment,
category and rig checks; these were not rerun for this documentation-only update.
Signed-in hosted saving was not verified in every earlier implementation session;
repository state now contains actual owner-attributed shared saves.

## Live game versus saved experiments

Do not infer public integration from lab implementation or a Library card.
Recorded integrations include:

- PR #1 / `db0b85b263bff04befb5c7755793478bc3b54f3b`: eight animated weapons.
- PR #2 / `eb12d9ff299b7deb773ead33c988d49f5b6eef97`: corrected 1.2-scale
  alignment. Historical verification included Pages deployment, live payload and
  a local battle/firing smoke test; full HTTP response hash was not checked.
- PR #5 / `fe079ec310813ed4439c4102bf054c3ded5734c1`: saved revision
  `20261101T073211Z-d4aec61a`, selected W08, carrying W01–W08 and ARM.
  Inspected state includes a deployment record with matching game SHA-256
  `939f17e7058d070318399a4dbe347e5de2e011a2769c8e0c8e69a0420e073af4`
  and verification time, although its status text still says “deployment
  unverified.” Treat this as recorded evidence, not a fresh check of today's page.

Main has advanced beyond those historical integration commits. Inspect current
main and payload before asserting which later rig/scale changes it includes.
The latest ARM test is not by itself a new main release.

## Art direction and faction foundations

Original brief: “Worms meets Warhammer.” Dark gothic artillery warfare among
armoured cyber troopers in drowned, neon-lit ruins. Warhammer is an acknowledged
influence; preserve the strongest silhouette while developing specific identity.
The world remains cyberpunk: weird, frightening and decaying, almost adjacent to
hell without becoming literal hell. “God in the Machine,” almost literally.

Environmental anchors: monumental spires, broken arches, statues, faction
banners/graffiti, layered distant silhouettes, dark water, magenta moon and
cyan/magenta illumination. Crisp pixel art with readable masses and selective
emissives; dark material layers and engine lighting rather than uniformly bright,
studio-lit bevels. Character density should become finer/less blocky than the old
troopers and sit convincingly with the existing guns. Enlarging an old sprite does
not supply that detail.

| Faction | User-authored foundation | Demand |
| --- | --- | --- |
| Ash Legion | Inquisitors/arbiters devoted to the one true Divine, an unforgiving God. No heresy tolerated. Half knight, half priest; futuristic templars distorted by zeal. Modern protective armour retaining sword-era construction ancestry. | Obedience |
| Neon Choir | Devoted to Central and supreme technological perfection. Divinity through becoming one with the Machine; calls others to join. | Assimilation |
| The Hollow | Flagellants and doomsayers who believe destroying the world makes way for an unimaginable dark power. | Destruction |
| Halo Guard | Cold, detached praetors/centurions guarding an unimaginably wealthy few for thousands of years; their light must be kept from others. | Exclusion |

All are cults to some degree. Differentiate shapes, materials, behaviour and cloth
construction, not just colours. All factions currently share equipment. Establish
Ash Legion first; faction-specific weapons are a longer-term possibility.

### Lore proposals — not settled canon

Jarred proposed Grimspire as a last bastion in a plague-ridden cyber dark age,
containing something each faction believes is the key to its emergence. Perhaps
the Forge is there. The dying world may once have held 80 billion people, with
survivors turning to religion.

Optional discussion ideas: other settlements could still exist; the Forge should
have a specific capability and constraint; ancient systems might work flawlessly
while basic necessities fail; rituals may preserve real technical procedures;
each faction may hold a partial demonstrable truth; something beneath Grimspire
might actually answer. These remain suggestions. Do not silently canonise them
or equate the in-world Forge with the editor's established technical capabilities.

### Ash Legion character: what landed

Preferred anchor in the supplied ZIP: `references/04-preferred-character.png`.
Enclosed helmet, layered dark armour, imposing human proportions, burgundy cloak
and priestly cloth: anonymous institutional authority, a soldier of an order.

- Pale ceramic and orderly ceremonial relic equipment drifted toward Halo Guard.
- Lean/ragged or hooded figures became “some dude” or a rogue/hero.
- Desired balance: “a little more tech and a little less blacksmith.”
- Darker oxblood cloth, duller armour, recessed face, elongated faceplate, ribbed
  throat and raised collar moved closer. More gothic character and brighter
  selective machine illumination are still wanted.
- Avoid shiny silver bevels, continuous neon outlines and cloth competing with the
  magenta sky. Selective magenta upper/back light and cyan reflected light should
  support readable torso values.
- Crosses, gold devotional jewellery, greathelms and tabards reinforce the
  medieval/Warhammer association. Machine-derived devotional marks are an
  unresolved exploration, not a completed symbol system.
- Judge the result at game scale. Concept atmosphere and detail have not survived
  automatic reduction sufficiently; refine actual pixel clusters and silhouette.

A short oxblood mantle, shortened front vestment and exposed compact dual-thruster
pack were proposed to clear jump-pack inlets/exhaust. This is a fit-test solution,
not an approved replacement for the preferred long-cloak concept. Pack and cloth
are static pixels; no cloth simulation or jump animation was supplied.

## Ash Legion assets now in shared test Forge

The supplied `GRIMSPIRE-art-direction-handoff.zip` originally recorded local-only
T09/A05 saves. That limitation is now superseded: both were added to the shared
Git-backed Library in commit `84114d095b0976fb519e1bcc012455abed5e2f7d`.
Refresh shared Library and search “Ash Legion.”

| Part | Code / stable identity | Immutable Forge document |
| --- | --- | --- |
| Body, jump-pack study v1 | T09 / `custom-ash-legion-jumppack-body` | `hosted/library/asset-227d2b092253c04d4ef0382a.forge.json` |
| Single near-side arm v1 | A05 / `custom-ash-legion-jumppack-arm` | `hosted/library/asset-b298f7879633c641a7fed93b.forge.json` |

Both are 41×58, baseline 54, shoulder [18,19]. Arm elbow [21,27], hand [32,30],
pivot [18,19]. Body has head, torso, legs, cloth and pack, without a weapon or
near-side arm. Material and glow are separate; no faction trim mask. Native pixels
and anchors were preserved. Body and arm each have one frame. Source was generated,
cropped, automatically reduced and palette-limited, not hand-cleaned final art.

Exact hashes, limitations, README and assembled preview are recorded under
`releases/ash-legion-jumppack-v001/`. Validation used the current sprite model and
family organisation, checked unique codes/identities and preservation of all prior
families/current selections, then read back both documents and index byte-for-byte.
No saved test slots or game snapshots were changed by the upload. No hosted
browser walkthrough, gameplay alignment, walk/aim/jump motion or game-feel test
was performed. Ready and visual/test flags remain false; upload is not approval.

The original six concept/environment references remain in Jarred's supplied ZIP;
they were inspected in this conversation but were not uploaded with the two
shared Forge documents. Obtain the ZIP for exact visual comparison rather than
assuming the small assembled preview preserves the concept quality.

## Shared asset workflow and safeguards

1. Read current `art/weapon-lab` head, `AGENTS.md`, existing asset identity/state
   and current Library. Preserve other users' newer work.
2. Add new immutable Forge documents under `hosted/library/`, with `forge:1`,
   code/name, dimensions, fps, markers and PNG layers. Validate through current
   `hosted/model.mjs`. Maintain appropriate anchors and false approval flags.
3. Register exact UTF-8 SHA-256 hashes in `hosted/library.json`. For genuinely new
   assets, assign unique `custom-...` asset identities and metadata (name/category,
   state key, code, dimensions, frame count). For versions of existing assets,
   retain their family/state. Display code alone is not identity.
4. Commit the documents, index, release notes/preview/hash record and CHANGELOG
   together. Fast-forward with an expected-head check. If a save arrives,
   reconcile; never overwrite `state.json` or immutable revisions to force success.
5. Refresh shared Library. Body visual test target is TROOPER; single foreground
   arm is ARM; W01–W08 are weapon behaviours. Save/test an exact revision with
   settings/notes when requested. TROOPER is a static visual placement test,
   not a full replacement animation/rig integration.
6. Promotion requires approval of the exact saved candidate. Use a focused
   integration from current tested main, not a wholesale merge of the lab branch.
   Preserve session/origin/CSRF checks, branch protection and stale-save refusal.
   Never commit credentials.

Key files: `hosted/worker.mjs` (API/persistence), `hosted/model.mjs` (validation),
`hosted/families.json` and `families.mjs` (identity/grouping), `hosted/bridge.js`
(shared UI), `forge.html` (editor/rig), `sandbox/runtime.js` (test renderer),
`sandbox/base.json` and `game.html` (pinned source), `hosted/state.json` and
`revisions/` (saved builds/history). Source registry is `hosted/assets.json`;
do not blindly regenerate it or alter old documents.

Useful code checks when code actually changes: `node --test art/lab/hosted/test.mjs`,
`node art/lab/sandbox/test_alignment.cjs`,
`node art/lab/sandbox/test_single_rig.cjs`,
`node art/lab/sandbox/test_categories.js`, and the hosted build. Discover runtime
dependency paths rather than copying paths from another machine.

## Recommended continuation

Continue visual exploration with Jarred in ChatGPT. Before character integration,
inspect current main's rig/scale/jump-pack behaviour. Refine native pixels against
the preferred knight-priest concept; then evaluate idle, aiming, both facings,
movement, jump ignition, flight and landing in the real environment. Keep thrown
arm work separate. Report creation, shared save, saved test, main integration and
deployment as separate states with evidence.

## Historical implementation journal

The entries below are preserved from the earlier handoff. Their “pending,”
“not live” and test-count statements describe those dated checkpoints, not the
current overview above.

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
