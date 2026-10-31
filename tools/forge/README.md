# Grimspire Forge

The pixel art tool for Grimspire. `forge.html` is the published page (the Grimspire Forge artifact). Publish it as an artifact with the `db`, `downloads` and `sample` (images) capabilities.

## The pipeline

1. **Draw** in the Forge. Every sprite has a code and lives in the Forge's library.
2. **Review** through the Notes box (Claude answers in "From Claude") or Ask Claude.
3. **Test** with "Test in range": it copies the sprite and opens the Proving ground in the private Grimspire artifact. Paste it there.
4. **Approve** with "Ready for the game" in the Sprite tab, then Save.
5. **Sync** on push: Claude reads the library and runs
   `python tools/forge_sync.py <library docs> --out art/forge --prune`
   Each sprite becomes a kit folder under `art/forge/` (see that folder's README).
6. **Pack**: `python tools/build_atlas.py <game source> --kits art/forge` adds every ready sprite to the game's props atlas and points its slot at it. Render only, no GV bump.
7. **Push** as usual (`tools/build.py build`, commit, push).

What packs where (`tools/forge_common.py`):
- **Weapons and props** (`SLOTS`): appended to the props atlas, slot repointed, grip/muzzle and other points carried over.
- **Trooper frames** (`TROOP`: T01–T05, T08 torso): replace their frames in the trooper sheet in place. A Forge trooper pixel (x, y) lands at sheet pixel (3x−11, 3y−9). The game draws only the T08 torso now; its **Hip** point sets where the legs attach.
- **Leg pieces** (`LEGS`: A03 thigh, A04 shin): rebuild the legs sheet and the `RIG` numbers. Frame 1 is the near leg, frame 2 the far leg. Each piece is centred on its joint (thigh on Hip, shin on Knee); the thigh's Knee sets where the shin hangs.
- Anything else (T06, T07, new set pieces, arm parts) syncs to `art/forge/` but has no slot in the game yet.

The Proving ground hot-loads all of these too, with the same rules, so what you see there is what packing gives you.
