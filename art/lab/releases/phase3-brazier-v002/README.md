# C04 brazier — remove accidental face

New version `asset-8d844e9f942923aa41893d3a` in `asset-c04`, replacing draft `asset-c8fa941c4e57b5adab233d6c` for review. Follows Claude's 2 Nov review on main: the paired orange vents looked like eyes.

Removed only the two 2×2 emissive patches at columns 11–12 and 19–20, rows 23–24, from all ten frames. Body and Guts PNG strings are identical to v001. Pixel comparison across all frames confirms every other emissive RGBA pixel is unchanged. Dimensions 32×40, baseline 39, scale 1, ten frames/10 FPS, flame loop and `light: amber, 75` retained. Existing body hardware is unlit. Native renderer comparison included.

Saved draft only. Claude's GV 18 hit-area work and exact-version release approval stay with Claude/Jarred; do not promote an older complete build. Ask (Claude): use this no-vents C04 version with your iron-only hit area when Jarred gives Go. Preserve the current set-piece gate, other art and latest game code.
