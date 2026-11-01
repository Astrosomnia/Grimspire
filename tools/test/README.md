# Test scripts

Playwright (Python) scripts used to check builds. Most expect the game at `/home/claude/work/grimspire.html` and the previous build at `/home/claude/work/orig.html` for comparisons: copy `index.html` (or `debug/index.html`) there, and the old one with `git show <ref>:index.html`. Chromium is preinstalled in the Claude workspace.

- `wrap.sh src out`: wraps the source the way claude.ai does (adds the phone viewport). **Always test phone layouts on a wrapped copy**, or the page renders at desktop width.
- `shot.py html prefix seed…`: desktop overview and close-ups, plus a phone close-up
- `phone.py html prefix`: portrait, landscape and small-phone screenshots with four squads
- `stress.py`: measures whether the top bar spills past the screen edge with wide fonts
- `det.py`: map hash after `newGame` for four seeds, old build vs new (visual changes must match)
- `dsim.py`: scripted minigun and Godfall turns run twice in fresh browsers; hashes must be identical
- `blast.py`, `podshot.py`: a blast next to a trooper, and a Godfall flight in frames

The game exposes `window.__G` for tests: `newGame`, `mkCfg`, `simStep`, `stateHash`, `camSet`, `base`, `explode`, `selectWeapon`, `tryFire`, `troopers`, `dress`.

- `dsimart.py path/to/index.html`: ranged weapons (the ones whose firing origins come from the art rig), run twice per seed, with art loaded early and late; hashes must be identical

## Art renderer (`art/`)
Node tests that run the game's art runtime (between the `GRIMSPIRE_ART_RUNTIME` markers in `index.html`) against its live `LAB_PAYLOAD`. Install once with `npm i @napi-rs/canvas` (or point `NODE_PATH` at it), then:

- `node tools/test/art/alignment.cjs`: grips, muzzles, firing origins and the arm across weapons, scales, facings, aims and poses
- `node tools/test/art/render.cjs`: PNG loading, emissive and bloom path, fallback
- `node tools/test/art/categories.cjs`: Forge test grounds (props, trooper dummy, timer)

Set `GRIMSPIRE_GAME` to test another build.
