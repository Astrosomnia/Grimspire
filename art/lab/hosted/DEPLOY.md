# Deploy the hosted Grimspire Forge

Target Worker: `grimspire-forge` in Jarred's existing Cloudflare account.
URL: https://grimspire-forge.jarredpowell88.workers.dev/
This deploys the Forge application. It does not deploy the live game or merge main.

## Existing Worker: one-time connection

In Cloudflare, open **Workers & Pages → grimspire-forge → Settings → Builds**
and connect a Git repository. Authorise Cloudflare's own GitHub integration for
Astrosomnia/Grimspire if requested. This integration deploys the application;
it is separate from the Grimspire Forge GitHub App used at runtime.

Use these exact settings:

| Setting | Value |
| --- | --- |
| Repository | `Astrosomnia/Grimspire` |
| Production branch | `art/weapon-lab` |
| Root directory | `art/lab/hosted` |
| Build command | `node build.mjs && node --test test.mjs` |
| Deploy command | `npx --yes wrangler@4.156.0 deploy` |
| Non-production branch deployments | Disabled for now |

Cloudflare's word “Production” here refers to the hosted Forge, not the game.
The root directory is relative to the repository. Leave output directory fields
alone: this is a Worker deployment using wrangler.jsonc, not legacy Pages hosting.
If an existing Worker cannot be connected in the current dashboard, do not create
or overwrite Dream Atlas: supply the screen/error so the integration can be adjusted.

The config names the existing Worker, retains dashboard variables with keep_vars,
and includes the three public GitHub IDs plus owner/origin restrictions. Secrets
remain in Cloudflare. Do not put them into repository files or build variables.

Runtime variables already entered by Jarred:
- GITHUB_APP_ID = 5558397
- GITHUB_CLIENT_ID = Iv23liLKlHD9cghoqijI
- GITHUB_INSTALLATION_ID = 177300737
- GITHUB_PRIVATE_KEY = Secret (complete PEM; value not available to ChatGPT)
- GITHUB_CLIENT_SECRET = Secret (value not available to ChatGPT)

After connecting, trigger the first build/deploy. Subsequent application updates
can deploy from Git. To avoid rebuilding on every artwork save, restrict Build
watch paths to application source/config files and art/lab/forge.html; exclude
hosted/revisions/, hosted/events/ and hosted/state.json. Library data is fetched
from GitHub at runtime and does not need a Worker rebuild.

## First hosted acceptance check

1. Visit `/health`. It should identify Grimspire Forge, report configured=true,
   and show the source build SHA. This checks variable presence, not GitHub validity.
2. Open the root URL and sign in with GitHub as Astrosomnia. Other user IDs are refused.
3. Open Library: original detail/grid variants and shared alternatives should load.
4. Open W04 grid art, add a test note and use Save & test in game.
5. Confirm a revision commit appears only on art/weapon-lab and its saved game loads.
6. Start a local battle and check the weapon, both facings, lighting and effects.
7. Ask Claude to add one alternate via library.json; refresh the shared library
   and confirm it appears without replacing an unsaved canvas.
8. Prepare a release PR if desired, but do NOT publish unapproved studies merely
   to test the button. Publication needs Jarred's exact-revision approval.

GitHub App authentication, real Cloudflare runtime and interactive browser QA must
be verified after this account-side deployment. Offline tests cannot prove the
contents of the secrets or the dashboard build settings.

## Release and hosting status

The Go live button prepares a PR, then updates main to its exact candidate only
after explicit approval. The candidate is a direct child of tested main; GitHub's
non-force ref update refuses a concurrent main advance. Branch protection is
respected. If protection requires GitHub's PR merge process, the direct ref update
will be rejected; the app does not bypass the rule or substitute an untested merge.

Main updated is distinct from public deployment verified. The Forge discovers a
GitHub Pages URL through deployment metadata or Pages settings, then checks actual
public HTML bytes against the approved SHA-256. Deployment records require the App's
existing Deployments read permission; Pages discovery can additionally require Pages
read-only permission. If there is no discoverable Pages site, or the game uses another
host, it reports deployment unverified. Do not claim public release on that basis.

No Pages configuration or production game host has been changed by this work.
