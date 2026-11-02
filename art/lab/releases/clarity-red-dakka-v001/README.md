# Clarity tidy, red Dakka, category crates and yellow tank

Jarred requested these revisions on 1 November 2026. Fourteen new versions in existing Forge families/states; no application code changed or live release.

## Troopers
Used the latest cloth-layer T10 torso, A07 thigh, A08 shin and A05 arm. The latest torso's Hip is **[21,31]**, moved forward by Jarred: retained exactly. All other markers, scales (1.2×), dimensions and frame counts/FPS retained.

Reduced armour to six dark neutral shades and cloth to four neutral-grey values; merged isolated interior shade speckles. Small warm flecks surrounded by cloth move from material to Cloth, maintaining the combined alpha silhouette. Cloth is still faction-coloured by the new renderer, not baked oxblood. Far leg values slightly darker. Original emissive/trim layers retained. This is native-pixel material/cluster cleanup guided by the generated cleanup reference, not a new silhouette or animation rig.

Four faction cloth variants rendered before/after using current main's actual drawTrooper and cloth-aware renderer; native world-size samples included. See faction-render-comparison.png.

## Dakka
W04 uses red-painted metal on its magazine/receiver and a pale red/almost pink strip on its existing top rail, guided by og.jpg. Existing body alpha, original grip [13,14], muzzle [37,7], game scale 1.2× and 20-frame/20-FPS timing retained. The original staggered lamps remain; top amber is pale pink and an added gentle top-rail breath shares the same loop. Cyan lamps remain for contrast. No weapon behaviour change.

## Crates
Canonical CRATE colours from current main: arms #8fb3dc, heavy #ffb21e, medical #a0ff46, tools #3ff3ff. Four existing symbol states recoloured; four complete category chest variants saved as versions of asset-c01 (arms is the latest default). Variants use the correct functional mark in the central panel. Their category spawning remains a Claude integration task.

## Promethium tank
C04 has a 40-frame, 20-FPS, two-second yellow/pale-yellow rolling lamp scan. Light alpha stays 165–255, so it never switches off. Material PNG, original lamp footprint, points, dimensions and scale unchanged. This does not create an armed/critical gameplay state. The generic PROP target can preview it; real spawning/collision/damage/animation integration still needs Claude.

## Review and evidence
- review.gif shows the Dakka and tank animations with the complete category crates and tidied parts.
- proof.json records silhouette/marker preservation and source identities.
- Current main renderer loaded/drew **74 frames across all 14 new versions**. Four-faction rig rendering and all 42 Forge tests pass.
- Combined trooper/Dakka candidate: https://grimspire-forge.jarredpowell88.workers.dev/api/game?debug=1&grounds=1&revision=20261102T061739Z-50f56248#grounds
- Candidate pinned to main 24c7aa37147abd9f0e1be7d125924f735ff61d84. Current shared build pointer is untouched; this is a direct linked review. Other latest V2 weapon versions are carried in the candidate.

Status: drawn and saved drafts, with model/hash/native-renderer verification. No signed-in hosted browser/battle walkthrough, final art approval or live release. Ready/visual/tested flags remain false. Existing immutable files and all earlier versions preserved.

**Ask (Claude):** when wiring props, select the category-specific full crate/version or compose the coloured symbol, and advance C04 frames by its FPS while retaining the yellow visibility. Do not infer prop gameplay from placement tests.
