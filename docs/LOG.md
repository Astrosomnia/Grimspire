# Grimspire log

One shared log for everyone: Jarred, Claude, ChatGPT and the Forge. Whatever you changed, wherever you changed it (code, art, Forge, balance, docs, decisions), add an entry here.

**How to write an entry:** newest at the top, under a heading `## YYYY-MM-DD · who · what`. A few bullets: what changed, where it lives, what's waiting on someone. Link commits, revisions or files when useful. Keep it short; detail belongs in commits and the Forge history. Questions or requests for someone else start with **Ask (name):**.

---

## 2026-11-01 · Claude · One source of truth, Forge test without saving
- **Source of truth:** `main` holds the game and these docs; the hosted Forge and `art/weapon-lab` hold art. Claude's old artifact Forge, its `forge-pipeline` branch and the push-from-artifact flow are retired. `docs/` replaces the Claude project docs and the lab handoff (archived in `docs/archive/`).
- **Art renderer moved into the game.** It now sits in `index.html` between `GRIMSPIRE_ART_RUNTIME` markers, outside the block the Forge rewrites. The Forge only swaps `LAB_PAYLOAD`. Same behaviour (determinism hashes unchanged, GV stays 17).
- **Forge Test no longer saves.** Test builds the game in place from your current canvas; nothing is committed, so no new versions. Save when you want to keep a version.
- **Leaner saves.** New revisions store the art payload plus the `main` commit they were tested against, not two full copies of the game (about 0.7 MB instead of 3.3 MB). The game is rebuilt from `main` when a revision is opened or released. Older revisions are unchanged.
- **Releases are logged here** automatically by the Forge.
- **Renderer tests moved to `main`:** `tools/test/art/` runs against the live game and its art. Added `tools/test/dsimart.py` (ranged weapons, determinism with and without art loaded).
- **Cleanup:** stale game copies and the old local Forge companion removed from `art/weapon-lab`. Reference images renamed; duplicate `og.jpg` removed.
- **Ask (Jarred):** Claude can't delete branches from its session. In GitHub → Branches, delete the five `art/release-*` branches (three are merged; deleting the other two closes stale PRs #3 and #4, whose art is kept in the Forge history) and `forge-pipeline`. Keep `vector-backup` and `sprites` as backups, or delete them if you don't need them.
- **Moved Jarred's three sprites** from the old Forge into the Library: aim arm (edited), lower aim arm, chainblade rework.
- **Ask (ChatGPT):** concepts give Ash Legion magenta, oxblood and bone cloth. In the game Ash Legion is cyan, magenta is Neon Choir, and coloured cloth breaks the restricted palette. Settle with Jarred before more Ash Legion art.

## 2026-11-01 · ChatGPT · Ash Legion fit-test, faction foundations, shoulder pivot
- Added T09 Ash Legion jump-pack body and A05 single arm to the Library as experiments (auto-reduced, not hand-cleaned, not approved).
- Faction foundations recorded in `ART-DIRECTION.md`. Lore ideas are proposals, not canon.
- Held weapons and the arm rotate around the trooper's shoulder; per-asset scale; Library grouped by asset with versions inside.
- Forge release `20261101T073211Z-d4aec61a` (W08 claw tweak, W01–W08 + arm) went live on `main`.

## 2026-10-31 · ChatGPT · Hosted Forge, animated weapons live (GV 17)
- Hosted Forge on Cloudflare with GitHub sign-in, shared Library, saved test builds and Go live releases.
- Eight animated weapon glows released to `main` (PR #1), then the 1.2× weapon scale with corrected grips and muzzles; shots fire from the real muzzle (PR #2, GV 17).
- Straight foreground gun arm and glove.

## 2026-10-30 · Claude · GV 16, crimson sudden death, artifact Forge
- Jarred's balance sheet edits applied (GV 16); crimson sky bleeds in at sudden death.
- Built the first Forge as a Claude artifact plus atlas-packing tools (now retired in favour of the hosted Forge).

## 2026-10-29 · Claude · North star visuals, weapon feel, field report fixes (GV 12–15)
- Backlit troopers, baked faction graffiti, gothic skyline, phone layout. Wind curve, minigun, overwatch sentry (since switched off), supply drop rates. First field report pass. Flamer hose, minigun and bolter rework, 10-turn fallout (GV 15).
