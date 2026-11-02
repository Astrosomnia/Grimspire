# Working on Grimspire

For any assistant or person working in this repo (Claude, ChatGPT/Codex, Jarred).

1. Read [`docs/HANDOVER.md`](docs/HANDOVER.md) first, then the top of [`docs/LOG.md`](docs/LOG.md).
2. When you finish a piece of work, add an entry to `docs/LOG.md` **on `main`** (newest first), even when the work itself lives on another branch, so everyone sees it. Update the handover if how we work or where things live changed.
3. `index.html` on `main` is the game. Code changes are Claude's; send requests through `docs/LOG.md` ("**Ask (Claude):** …") or a pull request.
4. Art goes through the Forge or, from outside it, `art/lab/tools/add_asset.mjs` on `art/weapon-lab` (see [`docs/FORGE.md`](docs/FORGE.md)). Never edit or delete existing library, catalog, revision or release files.
5. The Forge owns only the `LAB_PAYLOAD` block in `index.html` (`// BEGIN/END GRIMSPIRE_ART_ADAPTER`). Everything else in the file is game code.
6. Nothing reaches `main` or the live game without Jarred's approval. Never force-push, rewrite history or commit secrets.
7. Report states separately and with evidence: drawn, saved, tested, approved, on `main`, deployed.
