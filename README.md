# Grimspire · art/weapon-lab

This branch holds the **Forge** (the shared art editor) and the **art library**. The game, docs and tools live on [`main`](https://github.com/Astrosomnia/Grimspire/tree/main).

Start with [`AGENTS.md` on main](https://github.com/Astrosomnia/Grimspire/blob/main/AGENTS.md), then [`docs/HANDOVER.md`](https://github.com/Astrosomnia/Grimspire/blob/main/docs/HANDOVER.md) and [`docs/FORGE.md`](https://github.com/Astrosomnia/Grimspire/blob/main/docs/FORGE.md). Log changes in [`docs/LOG.md`](https://github.com/Astrosomnia/Grimspire/blob/main/docs/LOG.md) on main.

- `art/lab/forge.html`: the editor
- `art/lab/hosted/`: the Cloudflare Worker (deploys on every push here) and the library data
- `art/lab/tools/add_asset.mjs`: add art made outside the Forge to the library
- `art/lab/releases/`: hand-made release records (immutable)
- `art/lab/tests/`: editor rig test
