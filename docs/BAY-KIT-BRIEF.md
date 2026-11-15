# Bay kit: buildings from parts (test brief)

15 Nov 2026 · from Claude, agreed with Jarred. A small, contained test. Nothing here goes into the game.

## The question
Can a dozen small drawn parts make buildings that feel as good as K20 Collapsed Nave and K26 Rib Vault Bay, without hand-drawing each one?

Today every set piece is a whole building drawn by hand, split into Body + Back + Guts, then redrawn 2–3 times for variety, and a fixed image often can't find room on a map. Worms looks hand-made because it stamps good parts densely, not because every spot is drawn. If parts work, hand-drawn pieces become the rare landmark hits and everything else is assembled to fit the space.

Why we think it might fail: the earlier procedural walls looked like a mishmash because they were patterned slabs with no structure. These parts are real architecture with a job in play (floor, stair, cover). The ruin pass decides whether the result looks hand-made or gridded.

## Grid
- Art px at trooper density, game scale 1 (a trooper is about 50 art px tall).
- **Bay: 128 × 128 art px.** One bay is one storey of one span, pier included. Clear interior is about 104 wide × 112 tall: room for two troopers side by side and a jump.
- Piers sit on bay edges, 24 px wide, centred on the line (12 px each side), so neighbouring bays share one pier.
- Floor slabs are 16 px thick at the bottom of a bay.
- Every part snaps to this grid, so any two parts that touch line up without a seam.

## Parts (first set, 14 images)
Draw each as a Forge asset like any kit piece. Same palette, stone size and edge treatment as K26.

**Body** (what troopers stand on and hide behind):
1. Pier, one storey (2 variants)
2. Floor slab, one bay wide
3. Arch span, hangs under a slab between two piers
4. Stair flight, rises one storey across one bay (flips for the other direction)
5. Parapet / roof edge, one bay
6. Broken pier top (the pier sheared off partway)
7. Broken slab end (flips for left/right)
8. Rubble heap, sits on a floor, about half a bay wide

**Back** (behind troopers, never blocks; full value, the game darkens it):

9. Rear wall bay with arched window (2 variants)
10. Rear vault bay (ribs, for a top storey)
11. Rear arcade bay (open arches, for a ground storey)
12. Broken rear top edge (the rear wall's ragged skyline)

Guts: use the shared rubble texture clipped to the Body, as the K20/K26 drafts do. No Height for this test.

Slicing K26 and K20 for parts is fine and probably fastest; they're already built from bays. Redraw the edges so they sit on the grid.

## Assembler
A standalone page, `experiments/bay-kit.html`, loading the parts from `art/experiments/bay-kit/`. Not `index.html`, no game code touched.

- **Layout as text.** A building is a small grid, one cell per bay, one row per storey, top row first. `F` floor bay, `S` stair (rising right), `s` stair (rising left), `.` empty (no slab, sky or a drop), `R` rubble on the floor. Example, two storeys, three bays:
  ```
  F.F
  FSF
  ```
- **Generator.** From a seed: 2–5 bays wide, 1–3 storeys. One stair links each storey to the one above, alternating sides. Back fills every bay that has a floor or a pier beside it.
- **Ruin pass.** Remove 0–2 upper slabs (never the ground floor) and drop rubble under them; shear the top storey on a diagonal using broken pier tops, broken slab ends and the broken rear skyline; knock out one rear window bay to sky now and then.
- **Output.** 12 seeded buildings on one page at game scale, each with Body over darkened Back, a trooper silhouette for scale, and the walkable route drawn as a dashed line (the play-diagram style). K26 sits in the corner for comparison. A reroll button, and a text box to type a layout by hand.

## What Jarred judges
1. Of 12, how many would you be happy to see next to K26?
2. Can you spot the repeats or the grid?
3. Does each one have a route you'd actually want to fight on (floors, stair, cover, a drop)?
4. Does the Back make the inside read, the way it does on the nave and vault?

**Go:** the kit gets a proper brief (more parts, nave and belfry recipes, game placement into reserved lots). **No go:** we've lost an evening, and the hand-drawn pieces carry on with the reserved-lot placement.

## Not in this test
Game placement, destruction, Height, lit rendering, multiplayer, Forge changes.

## Asks
- **Ask (ChatGPT):** draw or slice the 14 parts on the grid above; save them as Forge drafts and export the PNGs to `art/experiments/bay-kit/`.
- **Ask (Claude):** build `experiments/bay-kit.html` once the parts land (can start with placeholder blocks before then).
