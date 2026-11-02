# Architecture variety pass — six new separate assets

2 November 2026. Two new drawings each for K01, K05 and K07; with the live bases, each repeating family now has three visual choices. Existing versions remain untouched. All native sizes, baseline and game scale 1 match the live base on main `64e43ca`.

| Slot | New version | Size | Baseline | Look |
|---|---|---|---|---|
| K01a | asset-f3434464aab347a5fcd28083 | 112×100 | 99 | paired lancets over recessed arcade |
| K01b | asset-aae574ea8cd4da604cbcd84c | 112×100 | 99 | heavy central buttress, dark windows and scar |
| K05a | asset-0560e310da5e3f8ce1a7a4ea | 180×80 | 79 | double arch rib, large keystone, iron straps |
| K05b | asset-7d814d6320aae149c58ebee5 | 180×80 | 79 | broken balustrade and iron repair plate |
| K07a | asset-e90866b60054c06449c84987 | 360×300 | 299 | paired clerestory panes and fluted ribs |
| K07b | asset-4374fe1595e45bd90c43e9a3 | 360×300 | 299 | breached upper wall, broken parapet, one surviving light |

Body/Guts on all six, separate Emissive where glass is lit. New generated source drawings interpreted at native grid using the shared six-value neutral stone palette; no painted glow, water or coloured rims. Exact source prompts included; source PNGs retained locally in `phase3/variants-v001/`. Native connector edits preserve the live base. Draft interpretations, with final hand cleanup and scene approval pending.

## Compatibility evidence

Every boundary pixel in Body, Guts and Emissive is copied and compared against its LIVE base: outer four columns; bottom four support rows; top four rows on K01; all 120-pixel bay connector bands on K07. Dimensions, baseline and game_scale also asserted equal. Interior appearance/apertures differ, so this does not claim identical complete collision geometry. `connector-checks.json` records counts.

All 42 current Forge tests pass following Library imports. Real local game tests use current main `64e43ca`, all live base assets plus the six drafts, and `/api/game?grounds=1#drowned`. The actual generator selected all six variants across seven desktop maps and two phone-layout maps; zero page-script errors. External services blocked. `battle-checks.json`, `desktop.jpg` and `phone.jpg` are the evidence. Phone layout is browser emulation, not a real-device performance test. Screenshots are actual local battles containing draft art, not live deployment.

The unlit native comparison (`variant-comparison.png`) shows base/a/b columns at the same pixel density. Source base documents used for checks are from live main, not a stale earlier concept.

## Ask (Claude)

Six separate variant slots now available in the shared Library, ready for a focused review build. Use the exact versions above alongside latest live art and code, rather than an older whole payload. Review new internal openings, damaged upper routes, lighting/visibility and destruction, and handle any terrain/sim fingerprint/GV checks as required. Keep the native dimensions, baselines and scale 1. No production game code, shared revision/current build or live release was changed by this save.

Notes include `weight: 0.9` / `state: intact` for a variants and `weight: 0.55` / `state: broken` for b variants. Current generator `pickK` chooses uniformly and does not read these metadata fields; treat them as suggested future composition settings, not verified weighted behaviour.

Drawn and saved: new Library drafts. Tested: exact connector/support compatibility, Forge and actual browser placement/rendering. Exact-art approval, full play/balance and real-phone performance review, and release: pending. Next art batch: D01–D06 foreground wreckage, followed by R01–R04 rocks and B01–B03 distant silhouettes.
