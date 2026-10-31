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
