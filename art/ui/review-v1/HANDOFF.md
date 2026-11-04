# GRIMSPIRE UI workshop — review v1

3 November 2026. Jarred authorised completing two alternatives per UI component while away, with refinement and final choices on return. He explicitly authorised UI work here and a testing branch for Claude review. The game itself is unchanged.

## Open and review

Open `index.html` in a browser. No build step or external font/network dependency. A simple static server also works. Phone layouts stack the alternatives. Links in the page jump between sections.

1. **Timer A / Reliquary:** compact stepped faction frame retained from the near-approved study, with a pale Georgia numeral lifted to optically centre it. **Timer B / Signal:** open brackets, simpler numeral. Both animate only changing digit slots: try 24→23 and 20→19. Wind has a signed tapered bar with directional flow; retreat softly replaces it. Pause has its own 44px target beside the frame. Reduced motion removes movement.
2. **Team A / Open typography:** restrained Georgia small caps, no block, 2px neon health line. **Team B / Inscribed plaque:** Palatino, dark clipped plaque and thin health line. Current-team diamond + Your turn sits with team state. Health, active side and long-name controls are interactive. System serif fonts are exploratory; final font licensing/embedding is not selected.
3. **Icons A / Solid signal:** filled silhouettes with engraved cuts. **Icons B / Dark enamel:** dark mass, cold-grey edge, small category-colour feature. Toggle category neon versus quiet grey independently. All 22 arsenal entries drawn on one 48px SVG grid, with 48/32/24px comparisons. These are new simplified studies, informed by weapon identities and Forge metadata, not exact vector traces or approved asset replacements. The disabled Sentry Turret is included for completeness.
4. **Current weapon A / Icon & caption:** framed icon with ammo and separate caption. **B / Equipment block:** icon, name and ammo contained in one horizontal block. Selecting a suite card updates both; clicking either scrolls to the arsenal.
5. **Arsenal A / Field cards:** persistent descriptions and category groups. **B / Equipment manifest:** smaller rows with a persistent selected-item detail area. Empty/unavailable slots remain legible and disabled. This is a review of all inventory types, not a new loadout design.

## Assets and notes

- `review.css`, `review.js`, `data.js`: standalone prototype implementation.
- `weapons.json`: 22 weapon names, descriptions, base ammo and disabled status from `main` d6ab5d6, plus new SVG geometry. Base ammo is demonstration state, not live match inventory. Source data refreshed against latest main after initial snapshot inspection.
- `icons/*.svg`: 22 neutral editable source SVGs.
- `icons/solid/*.svg`, `icons/enamel/*.svg`: 22 ready-to-view quiet-palette SVGs per treatment. Live inline variants inherit category/accent colours via CSS; standalone files contain default colours.
- `battle-reference.png`: Jarred's supplied gameplay screenshot, used as static context only.
- Card notes and ratings save in browser localStorage; Export review notes downloads JSON. Notes are never uploaded. On storage failure, export still works. No main-game save keys are used.
- Screenshot evidence and `checks.json` from the local review page are included. Screenshots freeze animations and cannot demonstrate transition quality.

## Validation

Headless Chrome: desktop 1440px, phone 390px and narrow phone 320px. Verified all 22 suite and arsenal entries; stable identity and zero animation on unchanged tens digit; changed-digit cleanup; retreat/pause; signed wind direction; health and long names; suite/current/arsenal selection; notes surviving reload; palette/treatment changes; disabled items; category filtering; reduced motion; note export; no page or component overflow and no script errors. `check.cjs` repeats checks with Playwright; set PLAYWRIGHT_MODULE to its installed module path and BROWSER_PATH if Chrome is elsewhere. Real phone hardware/performance not tested.

## Suggested first picks, pending Jarred

Timer A, team A, dark-enamel icons in the quiet palette, current weapon B, arsenal A. This keeps ornament and glow concentrated around meaningful state. Team B and current A offer the more ceremonial alternative. Do not treat these suggestions as approved choices.

## Integration request (Claude)

After Jarred's refinements, port selected component styles into the current game's existing DOM/ICONS hooks in small stages. Preserve IDs/listeners, live ammo/health/wind/retreat state, keyboard/touch input, joystick positions and pause modal. The demo pause only stops its local countdown. Do not port the demo state machine or static data as game logic. Preserve the game's real active-trooper and selected-weapon context elsewhere when removing the line beneath the timer.

Check multi-squad and allied HUDs (the two-team workshop does not prove those layouts), actual phone portrait and landscape, low-time and retreat, long names, empty inventory, focus order, open arsenal and overlays, safe areas, recenter/chat/pause interactions, live weapon icons at final sizes and FPS. No sim change is intended. The existing disabled Sentry Turret stays disabled; hiding it in the production arsenal remains the current behaviour.

**State:** drawn, saved, locally browser-tested. Choices awaiting Jarred. Dedicated review branch; main/live untouched. No Forge Library upload, game integration, hardware-phone approval or release claimed. A log entry is supplied on the review branch for Claude to bring to main after review; this branch does not authorise a main push.
