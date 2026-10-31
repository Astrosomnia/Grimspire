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
