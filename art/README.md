# Grimspire art

Source art kits, kept so sprites can be rebuilt in any session. The game itself embeds packed atlases, so nothing here is loaded at runtime.

Every kit follows the rules in the project's art brief: transparent PNGs, glows on a separate `_emissive` layer with matching registration, team colour on a neutral `trim` mask, and a `manifest.json` with sizes, frame order and grip/muzzle or pivot points. Trooper sheets are 510×710 frames, feet at y≈661, about 12 source px per art pixel.

| Kit | What's in it |
|---|---|
| `kits/walk-redrawn-v2` … `v4` | 4-frame walk: body, emissive and trim sheets, a preview GIF and a stride contact sheet. v4 is the latest |
| `kits/trooper-animations-v1` | Idle, jump, knocked, swim, death and throw sheets, plus a throw arm |
| `kits/pixelkit-v2` | Aim arm with pivot guide, weapons W01–W17 and the mortar shell P01, each with emissive |
| `kits/weapons-labelled-v1` | An earlier W01–W11 weapon set with a labelled sheet |
| `kits/expansion-v1` | Martyr charge, promethium tank (normal and critical glow), Godfall pod and wreck, minigun spin, sentry turret with tracking head, tracked drone, teleporter, chainblade chain cycle, dropship |
| `kits/props-v1` | Supply crate, the four crate symbol masks, parachute |
| `refs/` | Loose concept images: trooper, aim arm, weapons sheet |

**Status (29 Oct 2026):** these are the first pass and are due for a redraw against the north star in the art direction doc: near-black backlit silhouettes, flat paint, colour only from emissive light.
