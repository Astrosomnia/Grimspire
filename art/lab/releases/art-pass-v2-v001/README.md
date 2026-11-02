# Art Pass V2 — material-family harmonisation

Requested by Jarred, 1 November 2026. Eight current weapon versions plus a historical Chainblade edge-chase alternative, saved into their existing Forge identities. Nothing released to main or the live game.

## Visual change
A shared eight-step neutral charcoal/gunmetal ramp replaces the blue-purple bias and scattered colour shades in material layers. The ramp comes from the generated V2 material reference, itself matched to the new equipment family. The native material mapping preserves existing pixel placement and alpha; the generated reference is not substituted as geometry. This is a material pass, not a structural redraw.

Jarred explicitly allowed blue and magenta lights: every original emissive PNG is retained byte-for-byte, preserving cyan rails, the four red Las lamps, amber heat and magenta energy. Existing outlines/silhouettes stay intact. Trim and guts also unchanged.

## Animation and rig preservation
proof.json covers all **313 frames across nine versions**. For every corresponding source frame: body alpha unchanged, emissive PNG string byte-identical, trim/guts unchanged. FPS, frame counts, original frame order, dimensions, markers and effective game scales preserved. Fist stays 0.9×; other current weapons stay 1.2×.

The current shared/live Chainblade is a one-frame grid study. Its matching V2 version remains the default and is carried in the saved build. The historical 40-frame edge chase has its own V2 version in the same Library family, retaining that version's own original silhouette/anchors/timing. No saved manual Chainblade rework was removed or overwritten.

## Review
- animated-comparison.gif: current materials versus V2, matching animation times, 3.2 seconds. Nine rows, the last is the historical Chainblade comparison. No bloom; GIF colours are quantised for preview only.
- comparison.png: a static matching-frame comparison.
- Saved Forge test: https://grimspire-forge.jarredpowell88.workers.dev/api/game?debug=1&grounds=1&revision=20261102T053403Z-e018ed93#grounds
- Snapshot pinned to main 94521fd1731f9a935ba7935769273b5fdd6ce601; existing shared current-build pointer left untouched; this linked review does not replace it.

## Validation and status
313 source/output frame invariants passed. Current main's native Canvas renderer loaded and drew all 313 output frames; no empty output. All 42 Forge tests pass. Schema-2 snapshot rebuild/hash validation passes. This is renderer verification, not a signed-in hosted browser walkthrough or a battle playtest. Saved drafts; ready/visual/tested flags remain false pending Jarred's look/game review. No game/renderer/Forge application code changed.

A concurrent ARM save arrived during preparation. All eight weapon geometry/animation sources were confirmed unchanged; the saved review carries the newer shared rig/arm payload and the newer current-build pointer is preserved.
