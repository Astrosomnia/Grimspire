# Height layers for the current kit (brief for ChatGPT)

11 Nov 2026 · from Claude, agreed with Jarred.

## What we're doing
Adding a **Height layer to the existing kit art at its current size**. No redraws, no 2×. The 2× pass waits for the rebuild. Jarred's rule: finish the current pieces as they are before adding anything new.

## Why
Without a Height layer the lit look invents its own small brick grid, and that grid covers the painted stones. With a Height layer that matches the Body, the grid switches off and the painted stones take the light. See [`height-brief/K05-height-comparison.jpg`](height-brief/K05-height-comparison.jpg): top is K05 today, middle is a Height with an edge line (ghosted), bottom is K05 with [`height-brief/K05-height.png`](height-brief/K05-height.png).

The earlier 2× relief draft failed for two reasons worth avoiding: its Height showed a different stone layout from its Body, and it was drawn with soft gradients.

## Rules for a Height layer
1. **Same size as the Body, same alpha.** K05 stays 180×80, game scale 1. Do not resize anything.
2. **Trace the Body exactly.** Every joint in the Height sits on a painted joint in the Body, pixel for pixel. No stones the Body doesn't show.
3. **Flat faces, hard steps.** Each stone is one flat grey. Mortar is one darker grey. No gradients, no blur, no anti-aliasing.
4. **No bevel or chamfer lines.** One step per joint. A second step just inside the stone edge lights up as a doubled, ghosted outline (Jarred spotted this on the first test).
5. **Greyscale only:** white raised, black recessed. Mortar about 45, stones 110–215.
6. **Lighter paint sits further forward.** Arch ring, keystone, copings and rails proud; infill walling back.
7. **Seams:** left and right edge columns must match wherever the Body's do, so spans still tile.
8. **Leave Body, Guts and Emissive untouched.**

## Workflow
1. **First pass by rule.** `tools/art/height_from_body.py` builds a Height from any Body under rules 1–6 (`python3 tools/art/height_from_body.py asset.forge.json out.png`). `height-brief/K05-height.png` came from it and is ready to go onto K05's Height layer. In the Forge the same start is: select the Body layer, Ctrl+C (copies the whole frame), switch to Height, Ctrl+V, Enter. That gives the exact pixels to repaint in greys. To load a finished map from a file, use **PNG to layer** in the Forge's Trace tab with the Height layer active (same-size PNG, placed pixel for pixel).
2. **Hand pass (the part that needs an eye).** Fix what the rule can't know:
   - parts the paint shade gets wrong (a dark stone that should still sit proud, a light patch that is only weathering);
   - stones the Body splits with a stray shade pixel;
   - depth order of whole parts: openings and recesses back, piers and buttresses forward;
   - a little character on hero pieces (a slipped stone, a chipped corner), always as flat steps.
3. **Save as a draft** in the Forge Library. Do not mark ready or release.
4. **Check in the game, not the Forge preview.** A normal map mixes K05 with K05a–d, so a random bridge may not be the one you changed.

## Order
K05, then K05a–d · K01 and variants · K06 · K07 and variants · K02–K04 · K08 · K09 · then landmarks K10+ and rocks R01+.

## Asks
- **Done (Claude, 11 Nov):** relief for authored Height is stronger (Jarred picked the stronger setting to start; it may come back down). Still to do: a test link that forces every bridge to one chosen piece.
- **Ask (ChatGPT):** flag any piece whose Body has too many shades or too vague a stone layout to trace; those need a decision before a Height is drawn.
