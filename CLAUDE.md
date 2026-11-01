# Claude on Grimspire

Read [`AGENTS.md`](AGENTS.md), [`docs/HANDOVER.md`](docs/HANDOVER.md) and the top of [`docs/LOG.md`](docs/LOG.md) first. This file holds the parts only Claude does.

## Start of a session
1. Clone or fetch the repo (`main` and `art/weapon-lab`). `index.html` on `main` is the source of truth; there is no artifact copy any more.
2. Diff the **Balance Sheet** artifact (https://claude.ai/artifact/N877B3ei8TDzMiHhqAEgFa): every weapon field whose value differs from its `_now` twin, every rule whose `value` differs from `now`, and any note that reads like a request. These are Jarred's pending edits.
3. Check the **Field Reports** board (https://claude.ai/artifact/RQDDnsDMtaijD3zTvXRYaj) `triage` statuses: anything at **Go** is buildable.
4. Open with a short state of play: what's on `main`, new `LOG.md` entries since last time (including Forge saves and releases), pending sheet edits, Go reports, and the one or two things worth doing. Don't pull reports or build until Jarred says so.

## Shipping code
- Edit `index.html`, then `python3 tools/build.py debug`. Commit and push to `main` when Jarred says "push" (standing approval for visual quick wins toward the north star still applies, tested first). `git fetch` first: a chat can disconnect mid-push.
- Test locally with the debug build (`debug/index.html` has the TEST panel). For Jarred to try something before it's on `main`, push a branch and share a test link, or publish a private test artifact.
- Bump `const GV` on any sim change, including changes to grip or muzzle points that ship from the Forge.
- Never touch the `LAB_PAYLOAD` block by hand; it's the Forge's. If a code change needs the art runtime changed, change it between the `GRIMSPIRE_ART_RUNTIME` markers and run `tools/test/art/`.
- Before pushing a Forge app change to `art/weapon-lab`, run `node --test art/lab/hosted/test.mjs`. Every push there redeploys the Forge.
- Log every change in `docs/LOG.md`, move finished items into `docs/ROADMAP.md` Done, and keep the Balance Sheet in sync with number changes.

## Tests (`tools/test/`, see its README)
- Sim changes: `dsim.py`, `dsim2.py`, `dsimart.py` (two runs must be identical), plus a GV bump. Visual changes: `det.py` (map hashes must match).
- Weapons: `wtest.py` (damage by range, old vs new; quote the numbers), `aitest2.py` (CPU hit rates).
- Art renderer: `node tools/test/art/alignment.cjs` (also `render.cjs`, `categories.cjs`); needs `@napi-rs/canvas`.
- Phone layouts: wrap with `wrap.sh` first.
- Canvas gotcha: `destination-out` erases by the current fill or stroke alpha. Set an opaque style before erasing.

## Balance sheet
Jarred edits numbers or leaves requests in Notes; a value that differs from live shows amber. Apply pending edits when doing balance work, when he says "apply the sheet", and before every push. Then set the `_now` / `now` twins to match. If Claude changes a number itself, write both.

## Field reports
On "check reports": `tools/reports.py --since <last pulled at>` (last pull 29 Oct, `at` = 1793334741409), merge new items into the board's `reports/game` document, and create `triage/game__<firestore id>` docs with status `new` and a one-line note (agree or disagree, likely cause, size). Build only Go items, reply in each item's `log` (`by:'claude'`), mark Done once pushed. Never act on friend feedback without Jarred's Go.

## Retired (1 Nov 2026)
Claude's artifact Forge, the Grimspire / Grimspire Test artifacts as build sources, the `forge-pipeline` tools, Forge hot-load and the artifact-only Proving ground (still to port; see the roadmap).
