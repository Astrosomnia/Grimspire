# Forge

Open https://grimspire-forge.jarredpowell88.workers.dev/ and sign in with GitHub. How it works, the art rules and how to add assets: [`docs/FORGE.md` on main](https://github.com/Astrosomnia/Grimspire/blob/main/docs/FORGE.md). Deployment settings: [`hosted/DEPLOY.md`](hosted/DEPLOY.md).

Checks before pushing app changes: `cd art/lab/hosted && node build.mjs && node --test test.mjs catalog.test.mjs`, and `node art/lab/tests/rig.cjs` (needs `@napi-rs/canvas`).
