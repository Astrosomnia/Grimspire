# Dark-enamel icon test — separate from the current UI/PNG draft

3 November 2026. Jarred initially asked to pull the PNGs, then explicitly retracted that: keep current icons/UI if up and also fix the dark-enamel set. This branch does not remove PNG files, change the default icon mode, update main or alter PR #8's branch.

Open art/ui/enamel-revisions-v2/index.html for the self-contained original/revised comparison, full 22-item suite and selected-weapon preview. The seven revisions are Rail Carbine, Scatter Gun, Las Burner, Sun Grenade, Orbital Lance, Godfall and Plasma Cutter; the remaining fifteen SVG geometries are unchanged from art/ui/review-v1.

- Rail Carbine: narrow receiver and long paired rails.
- Scatter Gun: short broad flared double muzzle.
- Las Burner: forked energy emitter with four large capacitor dots and continuous body.
- Sun Grenade: rounded orb with horizontal latitude bands.
- Orbital Lance: descending beam and impact rays only; no satellite/ground object.
- Godfall: points down, landing marks below.
- Plasma Cutter: recognisable angled torch, cutting jet and spark/cut target cue.

Cold-grey body edges, dark enamel fill, restrained category-colour technological accents. No new PNG generation or source replacement. Individual editable SVGs live under icons/. The test page is self-contained and does not depend on sibling image loading.

## Actual-game test mode

On this test branch only, open index.html?icon-test=enamel (or debug/index.html?icon-test=enamel). Omit the query to retain exactly the existing PNG icon path. All PNG files, alignment data, default rendering and the core UI remain in place. Test definitions/CSS are isolated to .ui-enamel. This is opt-in testing, not release approval.

Validation: tools/test/enamel-icons.cjs verifies default PNG mode versus opt-in SVG mode, all 21 displayed arsenal entries (Sentry remains hidden), seven comparisons, all 22 suite entries, original/revised toggle and no script errors/overflow at 1440/390/320px. Evidence is in evidence/. Hardware phone and live online checks not performed.

Branch is based on PR #8 commit 259094f. It is a separate test proposal; no merge or deployment is authorised by its creation.
