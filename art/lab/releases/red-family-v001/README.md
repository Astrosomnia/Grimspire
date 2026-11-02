# Red equipment family — review import

Jarred requested these individual assets in Forge on 1 November 2026. 36 new documents, preserved existing asset identities and immutable history. Six new environmental asset families. No game, renderer or Forge application code changed.

## Direction and included changes
- Red is the dominant equipment light; neutral dark gunmetal, amber for heat. Existing W01–W08 animated weapons are untouched, awaiting a separate family consistency pass. Faction palette is unchanged.
- W10 is an enclosed handheld winch, with no exposed hook. W11 is heavy ore-mining equipment. W18 has a forward bipod. W19 is a larger emplacement. W21 is a handheld tricorder-style teleporter controller.
- P01 mortar shell, W13 Sun grenade and W15 Doomsday shell retain prominent emissive energy, because the current projectiles read as lights. Separate material and emissive PNG layers; no baked bloom. Gameplay visibility remains to be tested.
- W14 has separate safe and armed versions of identical geometry. The latest version is armed. Claude must bind visibility to the armed state; no ambient blinking animation implies gameplay state.
- C01 and C03 share a proposed abstract devotional glyph replacing the winged insignia. This is an equipment-art proposal, not faction lore. C06 helmet follows the T10 Ash Legion profile and magenta vertical visor.
- Godfall closed/opened forms are retained, with red lamps. Both states stay in asset-g01. Crate marks remain existing states in asset-c01.

## Trooper inspection and scale review
T10 torso, A07 thigh, A08 shin and A05 arm are still the existing auto-reduced artwork. Four review versions change game_scale to 1.2, notes and review flags only; original pixels, frames and sockets are preserved. Side-by-side in trooper-scale-review.png uses the actual current main drawTrooper/torso/leg/shoulder runtime, 1× and 1.2× with weapons kept at 1.2×; native world-size row included. This is renderer inspection, not a battle playtest.

1.2× improves body-to-weapon balance. Still pending: noisy palette / stray clusters, coherent dark plate and cloth masses, intentional near/far leg distinction, shoulder/hand/weapon clearance. Do not call this a cleaned final trooper.

A schema-2 review snapshot, 20261102T050235Z-25011463, is added to Forge history with current main pinned; the existing current-build pointer remains 20261101T094357Z-78228871. Open: https://grimspire-forge.jarredpowell88.workers.dev/api/game?debug=1&grounds=1&revision=20261102T050235Z-25011463

## Environment placement brief — Ask (Claude)
Use the six environment sprites as a decorative first pass. Roles: S01 saint head and S02 toppled saint = large half-submerged sump foreground; S03 gargoyle = ledges/rooftops; S04 arch = ground ruin; S05 reliquary = occasional ground focal point; S06 pier = sump edge/support.

Each family needs a ground/water anchor, footprint and clearances, permitted depth band, minimum spacing/repeat cooldown, scale range, optional mirroring and whether cover/destruction is purely decorative or physical. Use sparse grouped arrangements with occasional large landmarks, preserving readable battle lanes and trooper silhouettes. Keep decoration out of projectile collision until deliberately integrated. Paint local colour flat and let scene lighting lead.

Long-term content can grow substantially once those placement tags work: small rubble variants, broken statuary, wall reliefs, signs, pipes, shrines, drowned supports and distant silhouette families. Distribution should respect map shape and districts, rather than uniform random scattering. No spawning system was changed here.

## Status and limitations
Generated concepts were sliced/reduced to native art pixels (12 source px/art px), limited to 24 colours and alpha-clipped; lamps extracted into emissive layers. These are automatic interpretations for editing in Forge, not hand-cleaned production sprites. Initial weapon grip/muzzle markers are estimates and all new equipment scales need game review. Unsupported equipment/prop integration remains Claude's code work; do not release category tests as gameplay replacements.

All drafts have ready=false and visual/tested=false. Saved/imported: yes. Model/hash validation and main-renderer scale comparison: yes. Hosted browser walkthrough, battle playtest, final art approval, main integration and live deployment: no.

Sources are the five transparent image-generation derivatives retained in the originating GRIMSPIRE ChatGPT conversation (handheld tools, illuminated explosives, handheld teleporter/deployables, religious-glyph supplies, unchanged ruins). inventory.json lists the exact native versions; native-import-review.png shows them.
