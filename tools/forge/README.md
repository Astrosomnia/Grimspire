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

Weapons and props have slots (`tools/forge_common.py`, `SLOTS`). Troopers, arms and new set pieces don't have slots yet, so they sync to `art/forge/` but aren't packed.
