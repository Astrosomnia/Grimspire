# Grimspire art

Everything art-related, kept so sprites can be rebuilt or redrawn in any session. The game embeds packed atlases, so nothing here loads at runtime.

## Folders
| Folder | What it is |
|---|---|
| `reference/north-star.jpg` | **The only style reference.** The drowned gothic city. Read `art-direction.md` in the project for what to take from it |
| `in-game/` | The three atlases the live build uses right now, pulled out of `index.html`. The baseline for scale, framing and what we're replacing |
| `kits/` | Source kits: transparent PNGs, `_emissive` glow layers, `trim` team-colour masks, and a `manifest.json` each |
| `shared/` | Loose images shared along the way. Source material, **not** style references |

## What's live (29 Oct 2026)
- **Troopers** (`in-game/troopers-atlas.png`): body, trim and emissive rows from the walk and trooper-animation kits. Legs are a separate rig (`in-game/legs-atlas.png`) swinging from the hip in code
- **Weapons and props** (`in-game/props-weapons-atlas.png`): the simple weapons from `kits/pixelkit-v2`, plus `kits/expansion-v1` and `kits/props-v1` (dropship, parachute, Godfall pod, tank, crate and symbols, sentry, drone, minigun, chainblade cycle)

## Kits
| Kit | Contents | In game? |
|---|---|---|
| `walk-redrawn-v2` … `v4` | 4-frame walk: body, emissive and trim sheets, preview GIF, stride contact sheet | Walk replaced by the leg rig; upper body still from here |
| `trooper-animations-v1` | Idle, jump, knocked, swim, death and throw sheets, plus a throw arm | Yes |
| `pixelkit-v2` | Aim arm with pivot guide, simple weapons W01–W17 and the mortar shell, each with emissive | Yes, the weapons |
| `weapons-labelled-v1` | More detailed W01–W11 (angled chainblade). Same set as `shared/weapons-sheet.png` | No |
| `expansion-v1` | Martyr charge, promethium tank, Godfall pod and wreck, minigun, sentry with tracking head, drone, teleporter, chainblade cycle, dropship | Yes |
| `props-v1` | Supply crate, four crate symbol masks, parachute | Yes |

Trooper frames are 510×710, feet at y≈661, about 12 source px per art pixel; the trooper is about 27 world px tall in game.

**Status:** first pass, due for a holistic redraw against the north star.
