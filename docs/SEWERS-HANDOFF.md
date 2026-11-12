# Sewers: handoff (12 Nov 2026)

For a fresh chat picking up the sewer work. Read this, then the top of `docs/LOG.md` (the 12 Nov sewer entries hold the detail). Reference art: `docs/sewers/reference.png` (our HUD and palette, the look to aim for) and `docs/sewers/first-pass.png` (an early render).

## Where it stands

- **Off on `main`.** Sewers only generate with `#sewers` in the address (`const SEWERS_ON` in `index.html`). Jarred's call: close, but not there yet; the Power Claw and balance work shipped without them.
- **Jarred's test link** (private artifact `Grimspire: lit look test build`, slug `44792b2a-1605-427b-be3b-17aca7270036`) still has the last live-on version (GV 47).
- **Art style is in flux.** There's now a pixel look on `main` behind `#pixel` (render only, GV 48) and Jarred is torn between it and the lit look. Sewers are mostly geometry and gameplay, so keep iterating; check both looks before calling anything done.

## What exists (all in `index.html`)

**The generator** is a block inside `genTerrain`, starting at the comment `// ---- sewers (Jarred 12 Nov)`. It runs after statues and before `// neon fixtures`, so it carves through anything placed before it.

1. **Site search.** It scans runs 360–600 px wide. `ground(x)` measures the top of the land mass from the water up, climbing over caves (gaps of 90 px or less) but not up to floating islands. It takes the 88th percentile of ground as `tmax`. It needs one end within 150 px of `tmax`, a tunnel band at least 60% rock and a floor at least 70% rock, and no landmark (`K08`, `K10`–`K13`) in the way. Buried rock and tower feet don't count against a site.
2. **Its own seeded random numbers:** `hrand((S.seed^0x5e3e7)|0)`. Maps without a sewer stay byte-identical to before (`det.py` matches on them).
3. **Geometry.**
   - **Ramp:** from the lower end down to the tunnel floor, skipped if masonry (`K*`) stands over it.
   - **Tunnel:** `cy`..`fy`, 40 px tall, ceiling at `tmax + 26`.
   - **Chamber:** a vaulted chamber in the middle.
   - **Manhole:** tries four spots for a column clear of masonry, otherwise none.
   - **Chamber floor:** a pit to the sump if it's within 300 px, else a shallow pool.
   - **Cliff end:** if the far end meets a cliff, the tunnel runs out to it, blocked by a solid grate, with an outlet pipe below.
4. **Thin roofs are opened to the sky:** under 90 px over the ramp, under 30 px over the tunnel. This stopped slabs jutting out.
5. **Art and lighting.**
   - **Lining:** brick within 7 px of the cut, pushed as a kit piece `SEWER`.
   - **Small pieces:** grate (`SEWER_GRATE`), pipe (`SEWER_PIPE`) and manhole lid (`SEWER_LID`) are also kit pieces.
   - **Back wall:** painted into `hollow` (the rock-interior layer the lit look shows underground), and only where `hollow` already existed and rock was there before the cut. So above the ground line a cut shows sky, like any natural hole.
   - **Lights:** one or two `strip` fixtures (mostly cyan, sometimes amber or faulty) and a `post` lamp at the ramp top.
6. **Outflow falls:** `NS.falls`, drawn by `drawFalls()` and `fallEnd()` in the world pass. They're dark like the sump, with thin glints, and lit faintly in `gatherLights`.
7. **Set pieces keep out:** see the `// keep sewers clear` line in the set-piece placement check.
8. **Records:** `NS.sewers` holds `{x0,x1,cy,fy,pit,cliff,ramp,manhole}` (plus `{pool}` entries).
9. **Constants:** `SEWERS_ON` and `SEWER_CHANCE = .85` (chance once a map qualifies). The Balance Sheet rule `sewerChance` tracks it.

**Measured at the last live-on version:** about 34 of 43 non-drowned maps got one (too many). 5 of 300 troopers spawned inside one. A trooper walks down the ramp, along the tunnel and into the pit (where they drown, as intended).

**Tests:** `tools/test/sewers/` has the scripts (frequency, walk, screenshots, spawn count, mask), with a README on serving the test copy. Before any push: `det.py`, `dsim.py`, `dsim2.py`, `dsimart.py`, and a `GV` bump if generation changes.

## Jarred's feedback, latest first (12 Nov, 23:14)

1. **Too near the surface, and too eager.** Many maps get what is basically an open pit. Require a real depth below the surface. Prefer no sewer to a forced one, but aim for **25–30% of maps**.
2. **Odd cut-outs** against backgrounds and set pieces.
3. **Underpass, not bunker.** Almost always two true ends, both real outlets, so it opens up fighting space.
4. **Cyan lights 5% brighter.** Cyan only.
5. **Extra rooms are the priority**, for scale and so it doesn't get samey after three rounds. He's happy for Claude to pick: square rooms, stairs, different sump areas, more than one pipe design.
6. **Entrances as engineered openings.** On his marked screenshot: a lined cut dipping down to a **grate or gate (open or closed variants; decorative only, no complicated mechanics)**. Remove the mountain background in the cut, so it doesn't read as a ramp carved into the hillside. Where a sewer comes out on a near-vertical wall, use a **real outlet pipe that sticks out, with a regular drip**.
7. **Vertical shafts shouldn't cut through props.** They should stop at the foot of a building. Partly done: the shaft and ramp now avoid masonry, but this is not verified on Jarred's map.
8. **Earlier notes, already handled:** dark and moody like natural holes, one or two lights; falls not cartoony; the back wall in the normal stone texture; jutting edges fixed.

## Plan Claude proposed (not started; Jarred said wait while he weighs the art style)

1. **Placement first.** At least ~60 px of rock between the surface and the tunnel ceiling along the whole length. Give up rather than force it, then tune to 25–30% of maps. This should also stop the cut-outs.
2. **Two true ends every time.** Each end is either the engineered opening (a lined cut dipping to a gate, open or closed, background removed in the cut) or an outlet pipe when it reaches a cliff face. The manhole becomes an occasional extra.
3. **Modules.** A sewer is a chain of 3–5 pieces from a set: straight run, square room, stair run (up or down a level), flooded channel, pool with a ledge, sump pit, round grate chamber. Two levels when the rock is deep enough.
4. **Spawns.** Reserve at most one spawn spot per squad inside a sewer, so they become fighting space without anyone starting buried.
5. **Cyan lights 5% brighter.**
6. **Work in the test link only,** and show Jarred screenshots before anything touches `main`.

## Later

- **Catacombs** as the other half of the roll (50/50 sewer or catacomb).
- **A sewer art kit for ChatGPT** (brick, grates, gates, pipes, pool edges, with height maps), matched to the reference and to whichever look wins.

## Working rules that matter here

- Don't push to `main` without Jarred's go. Test builds go to his test link.
- Log every change in `docs/LOG.md`, and keep the Balance Sheet rule in step.
- Don't touch the `LAB_PAYLOAD` block by hand.
