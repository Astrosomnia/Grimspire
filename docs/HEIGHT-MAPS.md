# Height maps: running list

**16 Nov:** every noisy Height in the Library has a new smoothed version (readability pass, see `ART-READABILITY.md`). The bar: under 8% speckle, depth planes, not a brightness copy.

Which pieces still need a Height layer (relief for the lit look). Update this whenever a piece is saved, refreshed or released: add new pieces, move them down the list as their Height lands. Claude checks it on every release.

**Who needs Height:** anything the lit stone shader draws, which is the kit (K), rock (R), set pieces (S) and the bridge/tower variants. Foreground wreckage (D, drawn as silhouettes) and skyline plates (SKY, B) don't use it.

**Heads-up (16 Nov):** the shader already uses the drawing's brightness as relief when a piece has no Height, so a Height that just copies the brightness (most first passes are 0.95–0.99 correlated) adds almost nothing. A useful Height separates depth layers: front ribs and piers high, wall faces middle, recesses low. `art/lab/tools/height_punch.py` can flatten texture and push planes as a quick pass.

**Rules:** Height alpha must match Body alpha exactly, pure grey, same size and density as the Body (a 2× piece needs a 2× Height). Rocks want angular chunks at different depths (Jarred, 11 Nov); relief is 4.

## Needed (no Height)

| Piece | Where | Since | Note |
|---|---|---|---|
| Building parts B01–B08, B12–B14, B16–B24, B30–B33 (not drawn yet) | `BUILDING-PARTS-CONTRACT.md` | 17 Nov | Height required in the same save as the Body; tick off as each lands |

Latest refreshed drafts now have provisional Height; older live versions can still lack it until a reviewed release.

## Provisional (has a first pass, wants a proper one)

| Piece | Where | Since | Note |
|---|---|---|---|
| R10 Terraced split crag | live | 15 Nov | Rule-derived first pass |
| R11 Natural rock arch | live | 15 Nov | Rule-derived first pass |
| K03 Tower crown refresh | Forge draft | 15 Nov | Rule-derived; redesigned silhouette, gameplay pending |
| K04 Broken crown refresh | Forge draft | 15 Nov | Rule-derived; redesigned silhouette, gameplay pending |
| K06 Bridge pier refresh | Forge draft | 15 Nov | Rule-derived; matched stacking bands, gameplay pending |
| K01c depth refresh | Forge draft | 15 Nov | Rule-derived; refreshed silhouette, gameplay/relief review pending |
| K01d depth refresh | Forge draft | 15 Nov | Rule-derived; refreshed silhouette, gameplay/relief review pending |
| K02a depth refresh | Forge draft | 15 Nov | Rule-derived; refreshed silhouette, gameplay/relief review pending |
| K02b depth refresh | Forge draft | 15 Nov | Rule-derived; refreshed silhouette, gameplay/relief review pending |
| K05 depth refresh | Forge draft | 15 Nov | Rule-derived; refreshed silhouette, gameplay/relief review pending |
| K05c depth refresh | Forge draft | 15 Nov | Rule-derived; refreshed silhouette, gameplay/relief review pending |
| K07 depth refresh | Forge draft | 15 Nov | Rule-derived; refreshed silhouette, gameplay/relief review pending |
| K07a depth refresh | Forge draft | 15 Nov | Rule-derived; refreshed silhouette, gameplay/relief review pending |
| K07b depth refresh | Forge draft | 15 Nov | Rule-derived; refreshed silhouette, gameplay/relief review pending |
| K07c depth refresh | Forge draft | 15 Nov | Rule-derived; refreshed silhouette, gameplay/relief review pending |
| K07d depth refresh | Forge draft | 15 Nov | Rule-derived; refreshed silhouette, gameplay/relief review pending |
| K08 depth refresh | Forge draft | 15 Nov | Rule-derived; refreshed silhouette, gameplay/relief review pending |
| K09 depth refresh | Forge draft | 15 Nov | Rule-derived; refreshed silhouette, gameplay/relief review pending |
| K14 depth refresh | Forge draft | 15 Nov | Rule-derived; refreshed silhouette, gameplay/relief review pending |
| K15 depth refresh | Forge draft | 15 Nov | Rule-derived; refreshed silhouette, gameplay/relief review pending |
| K16 depth refresh | Forge draft | 15 Nov | Rule-derived; refreshed silhouette, gameplay/relief review pending |
| K02 Stepped spire refresh | Forge draft | 15 Nov | Rule-derived; refreshed shape, not yet live |
| K05d Weathered stone arch (revised) | Forge draft | 15 Nov | Height in the redrawn area provisional |

| K10 refreshed draft | Forge draft | 16 Nov | Rule-derived provisional Height; new silhouette; gameplay/relief review pending |
| K11 refreshed draft | Forge draft | 16 Nov | Rule-derived provisional Height; new silhouette; gameplay/relief review pending |
| R05 refreshed draft | Forge draft | 16 Nov | Rule-derived provisional Height; new silhouette; gameplay/relief review pending |
| R06 refreshed draft | Forge draft | 16 Nov | Rule-derived provisional Height; new silhouette; gameplay/relief review pending |
| R07 refreshed draft | Forge draft | 16 Nov | Rule-derived provisional Height; new silhouette; gameplay/relief review pending |
| R08 refreshed draft | Forge draft | 16 Nov | Rule-derived provisional Height; new silhouette; gameplay/relief review pending |
| R09 refreshed draft | Forge draft | 16 Nov | Rule-derived provisional Height; new silhouette; gameplay/relief review pending |

| K12 refreshed draft | Forge draft | 16 Nov | Exact Body alpha; rule-derived provisional Height; lit-game relief review pending |
| K13 refreshed draft | Forge draft | 16 Nov | Exact Body alpha; rule-derived provisional Height; lit-game relief review pending |
| K20 refreshed draft | Forge draft | 16 Nov | Exact Body alpha; rule-derived provisional Height; lit-game relief review pending |
| K21 refreshed draft | Forge draft | 16 Nov | Exact Body alpha; rule-derived provisional Height; lit-game relief review pending |
| K26 refreshed draft | Forge draft | 16 Nov | Exact Body alpha; rule-derived provisional Height; lit-game relief review pending |
| K22 refreshed draft | Forge draft | 16 Nov | Exact Body alpha; rule-derived provisional Height; lit-game relief review pending |
| K22a refreshed draft | Forge draft | 16 Nov | Exact Body alpha; rule-derived provisional Height; lit-game relief review pending |
| K22b refreshed draft | Forge draft | 16 Nov | Exact Body alpha; rule-derived provisional Height; lit-game relief review pending |
| S01 refreshed draft | Forge draft | 16 Nov | Exact Body alpha; rule-derived provisional Height; lit-game relief review pending |
| S03 refreshed draft | Forge draft | 16 Nov | Exact Body alpha; rule-derived provisional Height; lit-game relief review pending |
| S07 refreshed draft | Forge draft | 16 Nov | Exact Body alpha; rule-derived provisional Height; lit-game relief review pending |
| S09 refreshed draft | Forge draft | 16 Nov | Exact Body alpha; rule-derived provisional Height; lit-game relief review pending |
| R01 refreshed draft | Forge draft | 16 Nov | Exact Body alpha; rule-derived provisional Height; lit-game relief review pending |
| R02 refreshed draft | Forge draft | 16 Nov | Exact Body alpha; rule-derived provisional Height; lit-game relief review pending |
| R03 refreshed draft | Forge draft | 16 Nov | Exact Body alpha; rule-derived provisional Height; lit-game relief review pending |
| R04 refreshed draft | Forge draft | 16 Nov | Exact Body alpha; rule-derived provisional Height; lit-game relief review pending |
| K17 refreshed draft | Forge draft | 16 Nov | Exact Body alpha; rule-derived provisional Height; lit-game relief review pending |

## Done

- K01 / K01a / K01b, K05a / K05b: redrawn at 2× with the depth refresh (15 Nov, live)
- Everything else in the live kit and rocks: K01c–d, K02–K11 with variants, K14–K17, R01–R09 (11 Nov)
