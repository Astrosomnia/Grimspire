# Grimspire

A Worms-style artillery game in a single HTML file. Two squads of cyber troopers fight over a ruined, neon-lit hive ward. Blow the ground out from under them; the sump below takes anyone who falls in.

**Play:** open `index.html` in a browser, or use the GitHub Pages link once it's switched on.

## Modes
- **Fight the machine:** you lead the Ash Legion against a CPU squad.
- **Two commanders:** pass the device each turn.

## Controls
| | Desktop | Touch |
|---|---|---|
| Move | ← → / A D | Stick, sideways |
| Aim | ↑ ↓ / W S | Stick, up/down |
| Fire | Hold Space to charge, release to fire | Hold FIRE |
| Jump | Enter | JUMP |
| Arsenal | Tab, then arrow keys and Enter | Weapon button |
| Switch trooper (before moving) | X or click a trooper | SWAP or tap a trooper |
| Grenade fuse | 2–5 | Fuse button |
| Pan / zoom | Mouse to the screen edge / scroll | Drag / pinch |
| Recenter | C | Recenter button |
| Pause | Esc | II |

Orbital Lance and Fabricator are placed with a click or tap. Rotate girders with Q/E or the aim stick.

## Arsenal
- **Artillery:** Plasma Mortar, Frag Charge
- **Guns:** Rail Carbine, Scatter Gun, Dakka Bolter, Las Burner, Promethium Flamer
- **Melee:** Chainblade, Thunder Fist
- **Heavy (one use):** Sun Grenade, Orbital Lance, Doomsday Shell
- **Tools:** Rappel Wire ×5, Jump Pack ×2, Plasma Cutter ×5, Fabricator ×3

## Rules of the ward
- Taking damage ends your turn. Two-shot weapons let you move between shots.
- Blasts throw a shockwave that shoves anyone nearby. Thrown troopers skid, get knocked flat, then get up.
- Knock someone past the edge of the map and they're gone.
- The sump is bottomless. Wade where there is footing (5 HP a second), drown where there is not. Ordnance fizzles in it.
- Troopers step out of fire on their own, so fire herds people, ledges included.

## Maps
Four layouts: Spires, Islands, Canyon and Ruins. Ruins uses simplex noise for the natural rock on top of a rolling ground line, with chasms down to the sump, then builds a ruined city on it: twin towers joined by arched bridges, hollow tenements you can hide inside, and lit facades in the background.

## The ward fights back
- **Rising sump:** from turn 10 the water climbs before every turn.
- **Supply drops:** a gunship parachutes in crates holding heavy weapons, health or tool charges. Walk into one to grab it.
- **Promethium tanks:** shoot, burn or blast them and they explode, chain, and leave fire behind.
- **Kill cam:** killing blows and chain reactions drop into slow motion.

Prototype. Built with Claude.
