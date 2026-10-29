# Test scripts

Playwright (Python) scripts used to check builds. They expect the game source at `/home/claude/work/grimspire.html` (extract it from the artifact with `tools/build.py extract`) and the previous build at `/home/claude/work/orig.html` for comparisons. Chromium is preinstalled in the Claude workspace.

- `wrap.sh src out`: wraps the source the way claude.ai does (adds the phone viewport). **Always test phone layouts on a wrapped copy**, or the page renders at desktop width.
- `shot.py html prefix seed…`: desktop overview and close-ups, plus a phone close-up
- `phone.py html prefix`: portrait, landscape and small-phone screenshots with four squads
- `stress.py`: measures whether the top bar spills past the screen edge with wide fonts
- `det.py`: map hash after `newGame` for four seeds, old build vs new (visual changes must match)
- `dsim.py`: scripted minigun and Godfall turns run twice in fresh browsers; hashes must be identical
- `blast.py`, `podshot.py`: a blast next to a trooper, and a Godfall flight in frames

The game exposes `window.__G` for tests: `newGame`, `mkCfg`, `simStep`, `stateHash`, `camSet`, `base`, `explode`, `selectWeapon`, `tryFire`, `troopers`, `dress`.
