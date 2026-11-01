# Art lab instructions

Read [`AGENTS.md` on main](https://github.com/Astrosomnia/Grimspire/blob/main/AGENTS.md) and `docs/HANDOVER.md` there first. Lab-specific rules:

- Add art through the Forge or `node art/lab/tools/add_asset.mjs`. Never edit or delete existing files in `hosted/catalog/`, `hosted/library/`, `hosted/revisions/` or `releases/`; they're immutable history. A change is a new version.
- `hosted/library.json` indexes every saved version, not just current ones. Only append (the tool does this).
- Forge app code (`forge.html`, `hosted/*.mjs`, `hosted/bridge.js`) is maintained by Claude. Every push to this branch redeploys the Forge, so run the tests first.
- The game's art renderer lives in `index.html` on main, not here. `hosted/fixtures/` holds a pinned pre-November game and renderer for the Forge's own tests only.
- Never set ready or approved flags just because a file imports. Jarred approves exact assets; game scale, rig and effects need an in-game check.
- Releases to main only through the Forge's Go live (exact tested build, fast-forward). Never merge this branch into main.
