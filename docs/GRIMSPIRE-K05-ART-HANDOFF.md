# GRIMSPIRE K05 bridge art handoff

> **Portable handoff:** The reference images, Forge JSON studies, and isolated-test source are included in [k05-handoff-assets](k05-handoff-assets/). These are draft/reference files, not approved game assets. The playable comparison requires a clone/download and a local server.

**For the next chat:** Read this first, then read the current repository instructions and art brief. Jarred wants a visible improvement in the playable bridge—not another attractive concept presented as if it were game art. Continue with one bridge, compare it reliably in game, and show the actual result.

## Jarred's feedback and target

- The generated bridge reference shown in the last chat looks great to Jarred. Its masonry has more depth and texture; use it as an art-direction reference while retaining GRIMSPIRE's style.
- The bridge in the local game test looked **worse** to him than before. A large black crack/streak on the left becomes conspicuous when the piece is repeated. Investigate the actual source of that mark before changing it; do not assume whether it comes from Body, Height, lighting, or another layer.
- He wants a more dimensional, textured gothic world, but clear gameplay: players must be able to tell the playable/destructible arena from the background. The tall background and foreground depth-of-field framing are keepers. Trooper and weapon art, plus silhouette weapon icons, remain later priorities; the present task is the first K05 bridge.
- Be token efficient and candid. Do not claim an art pass, a visual improvement, or an in-game test succeeded without evidence.

## Read these first

- Read the repository's `AGENTS.md`, then `docs/HANDOVER.md` and the top of `docs/LOG.md`, followed by the [current art brief on `lit`](https://github.com/Astrosomnia/Grimspire/blob/lit/docs/ART-BRIEF-LIT.md), `ART-DIRECTION.md` and `WORLD-ART.md`. Verify current branch heads and latest instructions before working: this document is a snapshot.
- [Reference shown to Jarred](k05-handoff-assets/bridge-texture-reference-v2.png). Another exploration is [bridge-body-weathered-reference.png](k05-handoff-assets/bridge-body-weathered-reference.png).
- These generated images are **references only**, not game-ready sprites: their shapes and joins are not verified against the bridge, they have partial transparency, and their baked shading conflicts with the lit-art brief. Do not silently import or release them as finished Body art.

## What exists now

The previous session's workspace was not a Git checkout; these handoff files were subsequently uploaded to the `docs/k05-art-handoff` branch. The shared repo is [Astrosomnia/Grimspire](https://github.com/Astrosomnia/Grimspire). On 11 Nov 2026, `main` and `lit` were at `4bf2ff3ce168161b2555b40bf795add6c42d41ca`; `art/weapon-lab` was at `e56808e65a1e52c9a2867a1563a3ad7bcdba82f1`. Check for newer work rather than relying on those hashes.

### Shared Forge

- The shared K05 asset is `custom-294887fc-1769-4d04-ab6c-7b02deff39f3`. Its saved version **Bridge span · 2× relief draft** is a 360×160 enlargement/recolour of the old 180×80 sprite, with a traced Height study. It is a draft, not approved or released.
- Saved test revision: [`20261111T151133Z-c7046c8e`](https://grimspire-forge.jarredpowell88.workers.dev/api/game?debug=1&grounds=1&revision=20261111T151133Z-c7046c8e). As of this handoff it is the **current shared test build**, though it is not a release. Its payload contains K05 Body and Height at game scale 0.5, but normal drowned maps randomly choose K05 and variants K05a–d. Seeing a bridge on a random map does **not** prove that it is this K05. The shared `docs/LOG.md` has no entry for this study yet; coordinate the handoff in the project's usual workflow when continuing.
- The old hosted test was launched successfully, but the earlier assistant did not verify a blast on this specific bridge. Do not report blast behaviour or phone readability as passed.

### Uploaded studies

- [K05-relief-draft.forge.json](k05-handoff-assets/K05-relief-draft.forge.json): export of the shared relief draft.
- [K05-hand-texture-study-v2.forge.json](k05-handoff-assets/K05-hand-texture-study-v2.forge.json): **uploaded to this handoff branch, not saved to the shared Forge**, newer study with manually added surface marks and some corresponding Height marks. This is the version currently embedded in the local test and is the one Jarred says looks worse. It is not approved and has not been saved to the shared Forge. The underlying Height map is still a rough trace and does not align with every Body stone; Guts is the old art enlarged. Do not carry the prominent repeating streak forward.
- The local v2 export was checked against the relief draft: Body alpha unchanged; Body, Height and Guts left/right 8-art-pixel connector strips matched exactly; game scale was 0.5 and `ready` was false. These checks do **not** establish good art, clean-looking repetition, accurate Height relief, or a successful destruction test.
- [bridge-height-study.png](k05-handoff-assets/bridge-height-study.png) and the other files in [k05-handoff-assets](k05-handoff-assets/) are studies/references, not production-ready assets.

## Controlled comparison

[Test instructions](k05-handoff-assets/isolated-test/README.md) describe a playable fixed-seed comparison. It forces bridge selections to K05 and uses the same seed for original and draft. It also biases the generator toward bridge runs, and animated lighting/effects can differ between screenshots. It is a **local game snapshot with the merged 2× renderer patch**, not the exact hosted `4bf2ff3c` build.

After cloning or downloading this branch, build and start the comparison from the repository root:

```sh
cd docs/k05-handoff-assets/isolated-test
python3 build.py ../K05-hand-texture-study-v2.forge.json
python3 -m http.server 8765 --bind 127.0.0.1
```

- [Local draft](http://127.0.0.1:8765/k05-isolated.html?bridge=draft#grounds&drowned)
- [Local original](http://127.0.0.1:8765/k05-isolated.html?bridge=original#grounds&drowned)

The above links work only while the local server is running; GitHub does not host the playable game. To embed a revised Forge JSON, run `python3 build.py ../YOUR-FILE.forge.json` from that directory, then reload. The builder creates only the local test HTML; it does not change the shared game or Forge. Use matching camera/viewport and account for changing lighting when comparing. For final verification, also test in the current actual game renderer.

## Art and integration constraints

- K05 target: **360×160 art pixels**, **game scale 0.5**, **baseline row 159**, **`deck: 36`**. Preserve gameplay silhouette, walkable deck and compatible modular joins; check the current brief/source for updates. The last study used matching 8-pixel left/right connector strips. A mathematically matching seam is not enough: inspect a repeated run for conspicuous motifs and streaks.
- The lit brief calls for flat near-neutral mid-value Body art (roughly 90–150 brightness), native grayscale Height with raised faces and recessed joints, and Guts for the material revealed by blasts. Avoid painted directional highlights and coloured lighting. Keep pixel clusters intentional and assess at actual game and phone scale.
- Height is supported natively in Forge. The latest log says LIT is on `main` by default (`#classic` is the fallback). The game renderer can use the authored Height when LIT is active; the Forge editor's Lit preview is not sufficient to validate the authored Height. Height can improve lighting response but cannot substitute for new, genuinely detailed Body shapes.
- Follow the current repository/Forge workflow. Save draft versions as appropriate; **do not mark ready, release, publish or promote to the live game without Jarred's approval**. Claude has previously handled code integration/review; do not send messages to anyone unless Jarred explicitly asks.

## Recommended next actions

1. Reproduce and locate the black left-side streak in the exact local v2 and in repeated spans; inspect the Body and Height layers separately and distinguish it from generated scenery or lighting. Fix its cause rather than masking the screenshot.
2. Make a substantive stonework pass informed by the reference: deliberate varied block forms, edges and mortar at the native 2× density. Build Height from the **same** stone layout and give Guts a compatible interior; avoid a noisy scatter of speckles or another simple upscale. Preserve collision silhouette and joins.
3. Compare old and new on the fixed K05 scene, first at normal gameplay zoom and then close up; inspect repeated spans, lighting, readability against troopers, and actual blast damage. Validate the current hosted renderer separately before reporting success.
4. Show Jarred the actual in-game result alongside the old bridge, with clear draft/test/release status. If the available tooling cannot reach the reference faithfully, say so and propose a practical alternative rather than implying the gap is closed.
