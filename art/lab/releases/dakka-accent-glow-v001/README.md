# Dakka restraint and tank emission check

Jarred requested dark gunmetal again, a piercing pale-pink rail and only a tiny red material accent. W04 restores the V2 neutral material body and adds eight oxblood magazine-edge pixels (2% of 400 opaque pixels). All 20 pink-rail emissive PNGs, silhouette, markers, scale and cadence are unchanged from the previous pink-rail version. Saved into asset-w04 as another review version.

The C04 tank already has an emissive bar/pilot light in all 40 distinct frames at 20 FPS (two seconds). This pass changes no tank raster or frame data. Added provisional placement/light metadata and explicit lit-preview settings: emissive 1.5–1.8, bloom 6, glowColor #ffe62a. Proposed local-light radius 28 world px is an integration request, not a new implemented light source.

review.gif uses the actual current main art renderer, not a painted glow: before/after Dakka above, identical tank emission with bloom off/on below. The bloom pass adds visible spill (992 pixels brighten in the enlarged diagnostic). Image enlargement is for inspection. In-game scale remains unchanged. Earlier comparison GIFs composited body and emissive only, without bloom.

proof.json records exact frame/marker preservation; glow-proof.json records the renderer check. All 42 Forge tests pass. Saved draft versions only: no live release, main art integration or hosted battle playtest. No application code changed and current shared build untouched.

**Ask (Claude):** preserve C04 yellow emission/bloom when integrating it, and use the proposed light tag if it should illuminate nearby troopers/stone.
