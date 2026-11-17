# Building kit — Priority A / 17 November 2026

22 images for BK01–BK12, saved as 12 new Forge Library assets. Variants are immutable **versions inside each asset**, not separate families. The current version alone is not the complete kit: use `published-manifest.json` to retrieve every variant by `library_path` / `version_id`. BK IDs follow the 17 Nov rename and avoid the older B01–B03 skyline labels.

## Direction and provenance

Imagegen originals, one call per image; prompt set in `prompts.json`. Technical processing crops, registers, normalises the navy palette and enforces the contract's collision masks. 1× density, game_scale 1. Jarred explicitly widened the budget to **8–12 tones when useful** during the session. Final Body palette has at most 10 flat tones; rear walls use a quieter subset. Four-pixel sampling removes fine source variation. Height is independently authored geometric depth planes, not Body luminance. Guts are a coarse provisional stone core. No Emissive or Cloth needed for this batch.

## Placement contract

Coordinates use exclusive lower/right bounds. Geometric anchors in the manifest may be at canvas boundaries; Forge `pivot` is the last in-canvas pixel (one pixel above the geometric bottom).

- BK01–BK05: 24×128, anchor (12,128), bay line through pier centre. Storey origin y0; floor top y112; bottom16 overlaps the slab. No overhang.
- BK03: arch crown y28, 84 high, with the full-width throat from y40 to floor112 and no step. Variant a is pointed; b is round-headed. It is a wall cross-section, not a door-frame facade.
- BK04: full-width window y26–82, 56 high; floor y112 makes the sill30. Lancet / round-headed carving distinguishes the upper blocks.
- BK05: upper26 lintel; opening y26–112 (86); bottom16 only occupies the slab overlap. This resolves the table's 26+86=112 within the 128 storey.
- BK06: 128×16, anchor (0,16), flat walk surface, repeat128. BK07:16×16 finished edge.
- BK08: **canvas128×34**, visible104×34 with transparent12 at each side, per the bay-canvas rule. Place canvas x on bay line; top directly beneath the slab. Geometric bottom-left anchor (0,34). Depth34 at pier faces,6 in middle. Pointed and round variants.
- BK09–BK11:128×128, anchor(0,128), **Back only**. An empty transparent Body PNG satisfies the current Forge schema; it is NOT a collision plate. Keep Height and Guts null for these non-colliding rear walls. Assemble separately behind the foreground piers.
- BK10: opening32×62, bbox x48–80/y20–82, pointed head; bottom30 above floor y112. Both variants align.
- BK12:128×64 = nominal48 + buried16. Geometric anchor(0,48), top at floor top; bottom16 extends below the nominal foundation. Repeat128.

No generic dark Back is packed into a pier: BK09–BK11 supply the room interior. The rear arcade opens toward the eventual Far Back layer.

## Checks and status

- Drawn and packaged:22/22, all distinct.
- Validation:Forge schema, dimensions, binary alpha, exact Body/Height/Guts masks, scale1, draft flags, clear door/window/arcade openings, flat slab/plinth tops, matching horizontal repeat edges, rear window alignment and palette limits.
- Forge regression suite:66/66 pass after build (test, back, height, catalog).
- Visual inspection:contact sheet, four-bay/two-storey assembly and reduced-scale proof beside a flat terrain swatch and 50-art-pixel scale figure. These are raw compositing proofs, not the game shader or a movement test.
- Saved in Forge Library via add_asset.mjs. No existing asset files changed. No game payload, state/revision or live game changes. All ready flags false.
- **Next / Claude:** export all manifest variants to the building lab and enable Skinned. Check lighting, movement, shots through sill30, destruction, and joins beside actual terrain in #bldtest. Guts and Height need that runtime check. No approval or live-release claim.

The local working folder also retains individual PNG layers, original generated images, processing scripts and Forge drafts. The immutable Forge receipt contains this handoff, exact asset/version map, prompts, checks and preview sheets.
