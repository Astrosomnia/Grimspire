# art/forge

Sprites from the Grimspire Forge, one folder per sprite, written by `tools/forge_sync.py`. Don't edit these by hand: change the sprite in the Forge and sync again.

## Naming

Folder and files are `CODE_name`, and every image is `CODE_name_layer.png` with layer `body`, `emissive`, `trim` or `guts`. Variants go after the name (`C04_promethium_tank_critical_emissive.png`).

Codes are a type letter and two digits: **W** weapons, **P** projectiles, **M** charges, **A** arm and rig parts, **T** trooper animations, **G** Godfall pod, **C** props, **S** set pieces, **E** terrain, **F** faction marks, **B** background, **U** UI.

## In each folder

| File | What it is |
|---|---|
| `CODE_name.forge.json` | The source. Drop it on the Forge's plate to open it |
| `CODE_name_body.png` etc. | ×12 sheets, frames left to right |
| `native/CODE_name_*.png` | The same sheets at 1 art px |
| `CODE_name_aseprite.json` | Aseprite sprite-sheet JSON for the native body sheet; points are 1-pixel slices |
| `manifest.json` | Code, name, size, frames, fps, points (×12 and native), feet row, game slot, ready, notes |

`index.json` lists every sprite, its slot in the game and whether it's ready to pack.
