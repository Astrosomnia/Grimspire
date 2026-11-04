# Interim UI pass — final-review draft

Jarred authorised pushing this UI and the attached icon edits. He explicitly dislikes most icons and wants a design restart later; the current set is usable interim art only. Do not present it as a final art-direction approval.

## Actual game implementation

index.html and regenerated debug/index.html contain the selected UI, not just a standalone mockup. Clock 1 / Reliquary has optically raised numerals and changes only the affected digit. Faction-colour wind has no number, uses directional flow proportional to strength, and crossfades to RETREAT. Pause has a compact visible mark and 44px hit area. On portrait phones, the clock remains between the team health bars in the same row; side ornaments are clipped down and the header stays under 90px in the two-squad narrow-phone test. Chat sits to the other side of the clock when available, avoiding narrow-phone overlap.

Team names use open Georgia small caps, neutral type and thin faction health lines. Active-side contrast indicates ownership. Standing counts remain, without Your turn / Their turn text. The faction/trooper intro still appears without the extra Your turn line. Allied and multi-squad layout logic is retained.

Selected weapon is an 80×66 clipped tile with a 50%-opaque backing, clean outer category border and subtle border glow. Off-white PNGs receive a stronger separate dark shadow. Ammo is beside the caption in 18px Georgia, not in the tiny tile corner. Both desktop and touch controls retain their existing listeners. Touch movement/aim/fire/jump locations are unchanged; fuse sits beside the selected control.

Arsenal retains the existing categories, descriptions, ammo and disabled logic, with the neutral PNG suite and restrained category selection border. Disabled Sentry Turret has a PNG for completeness but stays hidden in the arsenal as before. Important rope, wet-trooper, second-shot, targeting/build placement and imminent sump/sudden-death instructions move to a neutral context line; normal redundant trooper/weapon text is suppressed below the timer.

## Icon edits and approval provenance

submitted-review.json is the user's exact uploaded review. Every source SHA was checked against the original PNG before edits. asset-receipt.json records old/new SHA, note, state and display alignment.

Eight approved files are byte-for-byte unchanged: Plasma Mortar, Frag Charge, Rail Carbine, Sun Grenade, Orbital Lance, Sentry Turret, Tracked Drone and Plasma Cutter.

Fourteen targeted edits: flatter Scatter Gun top; conventional boxy Dakka Bolter; Las Burner capacitor apertures; flamer muzzle flame/no spire; chainsaw guide bar; angular power gauntlet; mine blast sparks; horizontal warhead; longer minigun barrels with ammunition belt; downward Godfall/impact marks; spool and wire; compact jetpack/flames; simple girder; sliced human teleporter symbol. These are new imagegen-edited PNG candidates, included at Jarred's direction for final draft review, not marked exact-version approved.

Source PNGs live under assets/ui/icons/. Rendering alignment is computed from alpha bounds and visual mass, encoded in UI_ICONS_DATA; original files are not cropped or overwritten. New UI icons do not enter the Forge weapon library or simulation fingerprint. Reduced motion suppresses digit/wind animations and transitions.

## Validation

Run tools/test/ui-pass.cjs with Playwright. It serves test-only access to private functions; no test hook is shipped. Desktop 1440×900, phone 390×844/320×740, landscape 844×390; actual game starts, all visible arsenal PNGs load, single-digit identity, retreat/wind, pause/resume and arsenal open/close, four squads/allies, chat touch target bounds, no page overflow/errors. Generated debug PNG paths also checked. Tests block external services and use browser phone emulation, not phone hardware or a live online session.

ui-pass-evidence contains battle/arsenal/four-squad screenshots, checks.json and state-hashes.json. Six initial terrain/trooper hashes (3 seeds, 2/4 squads) match baseline f736bb6. The Forge payload/runtime are byte-identical and GV remains 33. Full ongoing combat determinism was not rerun because simulation code did not change.

## Claude review

Please inspect CSS/layout at live match states and real-phone safe areas, online chat, narrow landscape controls, long names and multi-squad/allies. Review hint relocation and fade timing. Source remains the one-file game and build helper; no deployment mechanism changed. Regenerate debug via python3 tools/build.py debug after revisions. Confirm with Jarred before merge/release. Keep the deferred icon redesign clearly separate from this interim UI pass.
