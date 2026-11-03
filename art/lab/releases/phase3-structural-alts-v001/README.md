# Structural alternatives — different construction and negative space

2 November 2026. Jarred asked to retain the first six variants but add much more substantial alternatives: different crossbeams, spires, holes and building structures. All existing bases and a/b variants remain. This adds eight separate assets.

| Slot | Version | Native size | Baseline | Structure |
|---|---|---|---|---|
| K01c | asset-d9966228c1007fddab1a4399 | 112×100 | 99 | open iron X-frame |
| K01d | asset-12500b4059a82b074ff90d28 | 112×100 | 99 | offset diagonal flying buttress |
| K02a | asset-9062ed294c1ae89204b0181e | 112×192 | 191 | unequal twin pinnacles and open V |
| K02b | asset-dbc29a8ff8702c13dc83ffbf | 112×192 | 191 | open bell cage, hipped roof and ring finial |
| K05c | asset-3df5a2fd850cd778a741a33f | 180×80 | 79 | iron X-truss, triangular openings |
| K05d | asset-ca1384c2c3ff98e74a606484 | 180×80 | 79 | asymmetric cantilever rib, large diagonal void |
| K07c | asset-d359b425ae0f0e77d4982e09 | 360×300 | 299 | open cloister/scaffold, X braces and rectangular portals |
| K07d | asset-8dce9dda7eaf3781a5b1668b | 360×300 | 299 | solid fortress mass, circular breach and trapezoidal portals |

Scale 1; Body and Guts everywhere, separate restrained glass emission where present. K05d's decorative wheel motifs are unlit to avoid another paired-light face. Built-in image-generation sources interpreted at native grid with the shared material ramp; native joint edits. Source prompts are included; full source PNGs remain locally under `phase3/structural-alts-v001/`. Final hand cleanup and exact-art approval pending.

## Fixed joints, free structure

The earlier live bases are retained unchanged. New shaft/span/nave connectors, lower four-row support footprints, K01 upper band and K07 120-pixel bay joints match their live bases byte-for-byte in Body/Guts/Emissive. K02 alternatives preserve their base connector only; copying the old spire's side mask would defeat the new silhouette. Their dimensions, baseline and scale still match K02. Live base art was checked unchanged after Claude's GV21 release.

The new mass and holes are substantially different. Alpha occupancy differs from base over approximately 25–53% of the union of the two masks; this is a geometry diagnostic, not an artistic-quality score. `silhouette-comparison.png` shows the change without shading or lights. `variant-comparison.png` is the corresponding unlit native material/glass sheet.

## Checks and limits

- Connector/support comparisons and all 42 Forge checks pass.
- Local browser tests first passed against main bc2b5a8; then rerun against the newly generated GV21 district on main 3b7446d, preserving its live old variants and adding these eight in memory. All eight selected across three desktop maps; seven selected across five sampled phone-layout maps (K07d was not selected in that phone sample). Zero page-script errors. External services blocked.
- `battle-checks.json`, `desktop.jpg`, `phone.jpg` record the latest GV21 run. Browser phone emulation is not hardware performance approval. This checks loading, generation and rendering; not a full walking/combat/balance or deterministic simulation audit of the new terrain shapes.
- No game code, current shared build or live release changed by this save. New Library drafts only. Earlier six variants remain, including their now-live versions; latest current-build files must be preserved.

## Ask (Claude)

Use the exact versions in `injection-manifest.json` for a focused test build alongside all current live bases/a-b variants and latest GV21 code/lighting/scorch. The goal is genuinely different structures, not more weathering. Because apertures and mass change markedly, check walkable paths, blast travel, hanging supports, spawn accessibility, collision and destruction/Guts, plus required sim/GV/fingerprint tests. In particular, open shafts and diagonal bridge ribs may change tactics. Keep sizes/joints/scale 1; do not stretch or replace old variants. Request Jarred's exact scene/art approval before release. K07d is marked broken/weight 0.55, the others intact/0.9; current generator can now honour weights.
