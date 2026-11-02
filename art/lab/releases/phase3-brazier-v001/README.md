# C04 promethium brazier — first native draft

2 November 2026. Requested in the updated Phase 3 brief. Asset family `asset-c04`; new version `asset-c8fa941c4e57b5adab233d6c`.

32×40 art px, scale 1, baseline 39. Ten hand-keyed emissive frames at 10 FPS (1 second); static neutral iron Body and separate iron/coal Guts. Three supports, bowl with raised iron horns and two burning louvres. Notes contain `light: amber, 75`. No smoke, water, reflection or light baked into body. Native editable pixel draft; no generated source image or automatic reduction.

- `native-review.png`: five enlarged flame keys.
- `flame-strip-1x.png`: all ten keys at native size, 100 ms each.
- `renderer-review.png`: current main `31d3385` art renderer at scale 1; idle current live trooper parts assembled at their sockets, new brazier and current tank. Enlarged 4× for viewing. This is an isolated renderer comparison, not a battle screenshot. Amber glow is the existing renderer's pass; ground/local-light simulation is not represented here.

Validation: all 42 Forge checks pass. Current main renderer loaded/drew ten distinct flame keys and parsed a fire light with radius 75. Shared Library import uses `add_asset.mjs --asset asset-c04`. Current shared build and live tank remain untouched. Battle/phone visual review, exact-version approval and release pending.

Ask (Claude): review this C04 draft and fit the gameplay hit area when Jarred approves the exact art. The total height includes fire; the metal bowl/support occupies rows 14–39. Flame is on Emissive and changes shape; do not use the full flame bounds as a solid hit box by accident. Keep the amber-75 notes light, original tank gameplay and other current art. Hit-area change requires GV/determinism handling on your side. Do not release without approval.
