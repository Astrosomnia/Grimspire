# Building parts catalogue (ChatGPT's proposal, 16 Nov)

The long-term catalogue of parts for the building system ([`BUILDING-SYSTEM.md`](BUILDING-SYSTEM.md)). Written by ChatGPT; agreed by Jarred as the catalogue, **not** the first batch.

**Before anything here is drawn:**
1. Jarred calls the storey height (128 or 160 px) after playing the building lab. The lab found a 128 px storey only fits a full jump on about half the floors (160: 77%). Every part's dimensions depend on it.
2. Claude writes the part contract from the lab's actual cases: grid footprint, connection edges, layer (Body, Near Back, Far Back), play role (stand, cover, blocks shots, decoration).
3. The first batch is about 25 parts matching the contract: the 14 bay-kit images, doorway, window, arcade, wall end, one foundation, one bridge family (end, span, pier, stub), parapet, roof, ladders (bottom, repeat, top, floor exit), two Near Back and one Far Back.

**Claude's notes on the list:** one grid (half-bay only for a few named parts); ladders are in (the lab uses them); gates, portcullises, timber or iron as separate break materials, and decorative railings that look like cover need a gameplay call first; wetness and crack overlays may duplicate what the shader already does; industrial, sewer and canal parts are a later theme.

---

I’d build the baseline around **a drowned gothic district that can function entirely as playable architecture**: towers, halls, streets, courtyards, bridges and interiors, with rock used where it belongs.

The important distinction is between **parts we draw** and **arrangements the generator builds**. A nave should emerge from compatible piers, arches, galleries and vaults, with a few bespoke focal pieces giving it identity.

For the shared kit, I’d use the agreed 128 px bay as the starting grid, with half-bay and double-bay options where useful. Everything should follow the same masonry scale, restrained palette and strong lines at play zoom.

1. **Foundations and building bases**
   
   These let buildings meet water, streets, other buildings and occasional rock without sitting on an obvious island.

   - Straight foundation wall: repeating centre, left end, right end.
   - Heavy plinth: plain and stepped.
   - Foundation pier: square masonry and clustered gothic.
   - Waterline base: intact, eroded and partially breached.
   - Building-to-rock abutment.
   - Retaining wall: low and tall.
   - Exposed footing for a ruined building.
   - Drain or culvert opening through a base.
   - Deep foundation continuation that can extend below the screen.

   **Key variants:** dry/wet treatment, intact/broken termination, exposed/enclosed side. Water stains should be reusable overlays rather than separate drawings of every foundation.

2. **Structural piers, columns and supports**

   - Square masonry pier.
   - Clustered column for churches and vaulted halls.
   - Narrow iron support for industrial spaces.
   - Broad buttress.
   - Stepped exterior buttress.
   - Flying buttress.
   - Wall-attached pilaster.
   - Corbel or bracket supporting a balcony or floor.
   - Column bases and capitals.
   - Broken pier tops: shallow break and substantial sheared break.

   **Key variants:** plain versus ceremonial; freestanding versus attached; intact versus damaged. Columns need stackable shafts with distinct bases and caps.

3. **Solid walls and exterior façades**

   - Plain masonry wall bay—the quiet workhorse.
   - Banded masonry bay with a strong horizontal course.
   - Recessed wall panel.
   - Buttressed wall bay.
   - Low wall for cover.
   - Thick defensive wall.
   - Exterior corner and exposed wall end.
   - Gable-shaped wall infill.
   - Sloped or stepped wall termination.
   - Broken wall: top missing, side missing, large breach.
   - Industrial infill: iron panel or barred service opening.

   **Key variants:** narrow/full-width, plain/ornamented, intact/breached. Avoid making every wall equally ornate; the plain bays are essential.

4. **Doors, windows, gates and other openings**

   - Small pedestrian doorway.
   - Tall pointed doorway.
   - Broad ceremonial entrance.
   - Open arcade arch.
   - Narrow lancet window.
   - Paired lancets.
   - Round window or oculus.
   - Rose-window focal piece.
   - Rectangular industrial opening.
   - Sewer mouth.
   - Gatehouse opening.
   - Portcullis.
   - Heavy timber-and-iron gate.
   - Iron grille or barred window.

   **Key variants:** empty opening, recessed interior, glass, bars, damaged frame. Open and closed gate art is useful, but an operable gate would need its own gameplay decision.

   Frames, glass and closures should be separable. **A doorway, window and arcade must read differently at play zoom.**

5. **Floors, ceilings and exposed slab edges**

   - Standard stone floor.
   - Heavy vaulted-building floor.
   - Thin gallery floor.
   - Timber floor.
   - Iron gantry or grating.
   - Floor-to-wall junction.
   - Exposed slab edge and underside.
   - Cantilevered floor end.
   - Broken floor end with convincing thickness.
   - Floor opening: small drop hole and wide collapsed section.
   - Ceiling infill between supports.
   - Vault springing—the point where an arch grows from a support.

   **Key variants:** half/full bay, repeating middle, supported/free end, clean/broken. The edge players stand on needs to remain unmistakable under lighting.

6. **Stairs, ladders and vertical circulation**

   - Full-storey stone stair.
   - Half-storey stair.
   - Short doorstep or street stair.
   - Freestanding stair with open space beneath.
   - Stair backed by solid masonry.
   - Iron service stair.
   - Landing platform.
   - Stair-to-floor connector.
   - Vertical ladder: bottom, repeat, top.
   - Ladder exit through a floor.
   - Broken stair ending in a jump.
   - Stairwell Back showing the continuation deeper into the building.

   **Key variants:** left/right ascent, intact/broken, stone/industrial. Mirror where sensible; redraw only where lighting-independent geometry or ornament demands it.

7. **Balconies, galleries and projecting platforms**

   - Shallow exterior balcony.
   - Deep fighting balcony.
   - Continuous interior gallery.
   - Corner balcony.
   - Small lookout or firing platform.
   - Balcony over an entrance.
   - Cantilevered industrial platform.
   - Balcony support: corbels, arch or iron bracket.
   - Broken balcony stub.
   - Gallery end and wall connection.

   **Key variants:** open edge, stone parapet, iron railing; intact/partially collapsed. These provide useful intermediate positions between rooms and rooftops.

8. **Parapets, railings and defensive roof edges**

   - Plain low stone parapet.
   - Crenellated parapet.
   - Pierced gothic balustrade.
   - Iron railing.
   - Industrial safety rail.
   - Heavy battlement merlon.
   - Parapet corner, end post and cap.
   - Broken parapet with a clear firing gap.
   - Damaged railing with a missing section.

   **Key variants:** low continuous cover versus alternating tall cover; plain/ceremonial. Decorative Back railings must look distinct from solid cover.

9. **Roofs, tower tops and upper silhouettes**

   - Flat roof with parapet.
   - Shallow pitched roof.
   - Steep gothic roof.
   - Gable end.
   - Roof ridge and eaves.
   - Small spire cap.
   - Broad tower crown.
   - Belfry cap.
   - Dome sections or a compact dome cap.
   - Roof-to-tower junction.
   - Broken roof exposing the interior.
   - Sheared tower top.
   - Exposed roof ribs or rafters.

   **Key variants:** low/high, intact/ruined, plain/landmark accent. Some roofs should support traversal; others can sit behind a playable roof deck. That distinction must be deliberate.

10. **Bridges and connectors**

   This deserves a substantial family because it joins the city into a battlefield.

   - Plain stone deck span.
   - Single-arch stone span.
   - Ribbed gothic span.
   - Narrow high walkway.
   - Covered bridge or enclosed gallery.
   - Iron truss span.
   - Chain-supported walkway.
   - Timber or rope bridge.
   - Bridge-to-building doorway connection.
   - Bridge-to-rock abutment.
   - Bridge pier: land base and water base.
   - Pier cap supporting one or two spans.
   - Broken bridge stub with a heavy fractured end.
   - Damaged span with partial balustrade.
   - Small central gatehouse or shrine.
   - Stair or ramp connector between unequal elevations.

   **Key variants:** narrow/wide deck, short/repeating span, open/parapeted, intact/broken. Large bridges should assemble from ends, spans and supports rather than stretch one drawing.

11. **Near Back: the interiors immediately behind play**

   These need actual architectural purpose.

   - Quiet rear masonry wall.
   - Recessed wall bay.
   - Rear arcade.
   - Vaulted wall with ribs.
   - Blind arch or sealed doorway.
   - Window recess with deep jambs.
   - Rear stair and landing.
   - Upper gallery seen beyond the foreground.
   - Chapel apse.
   - Crypt niches.
   - Industrial pipes and service wall.
   - Broken rear wall.
   - Rear rubble bank.
   - Dark passage leading into another room.

   **Key variants:** plain, windowed, arcaded, broken. Keep broad dark areas so characters and foreground structure remain readable.

12. **Far Back: depth beyond the first interior**

   - Distant colonnade.
   - Repeating vault receding into darkness.
   - Far wall with a few lit windows.
   - Another room seen through a doorway.
   - Distant staircase.
   - Deep shaft or well.
   - Courtyard beyond an arcade.
   - Building across a narrow street.
   - Cathedral interior silhouette.
   - Broken skyline visible through a ruined rear wall.

   **Key variants:** enclosed darkness, borrowed light, open sky. These should have fewer edges and less contrast than Near Back. Far Back is planned functionality, so its packaging needs to follow the renderer contract Claude establishes.

13. **Streets, courtyards, canals and water infrastructure**

   This is how we replace the generic ground strip with places.

   - Paved street surface and exposed edge.
   - Raised pavement or narrow ledge.
   - Quay wall.
   - Canal retaining wall.
   - Steps descending into water.
   - Drain outlet.
   - Culvert.
   - Sewer tunnel lining.
   - Reservoir wall and lip.
   - Spillway.
   - Sluice frame and gate.
   - Large pipe: straight, elbow, junction and broken mouth.
   - Grated channel.
   - Small landing stage or dock.

   **Key variants:** dry/flooded appearance, intact/breached, stone/industrial fittings. Water itself remains a system, rather than a painted part of each asset.

14. **Ruin, damage and exposed construction**

   We need designed ruin for generation as well as the damage caused during play.

   - Broken masonry edges: horizontal, vertical and diagonal.
   - Exposed wall core.
   - Exposed floor core.
   - Rubble heaps: shallow, tall, wedged into a corner.
   - Fallen column sections.
   - Dislodged arch stones.
   - Collapsed roof ribs.
   - Hanging rebar or iron ties.
   - Broken timber beams.
   - Cracked-but-intact structural overlays.
   - Small debris clusters.
   - Matching Guts material families: masonry, carved stone, timber and iron.

   **Key variants:** light damage and major collapse. Breaks should follow the construction: a snapped pier should not look like a clipped rectangular sprite.

15. **Architectural ornament and identity**

   - Gargoyle perched on a corner.
   - Small standing saint.
   - Statue niche: empty and occupied.
   - Relief panel.
   - Sacred machine emblem.
   - Keystone ornament.
   - Capital ornament.
   - Finial and pinnacle.
   - Cornice or carved horizontal band.
   - Buttress shrine.
   - Bell and suspension frame.
   - Chains and hanging censers.
   - Banner brackets.
   - Banners: short, long and torn.
   - Faction graffiti and sigils.

   **Key variants:** restrained everyday pieces and a few ceremonial accents. Ornament should concentrate at entrances, roof corners and focal spaces, leaving most surfaces calm.

16. **Lighting and small environmental props**

   - Wall lamp.
   - Hanging lamp.
   - Standing brazier.
   - Recessed votive lights.
   - Window-light inserts.
   - Small machinery indicator.
   - Lamp-post bridge fitting.
   - Candle cluster.
   - Pipe valve.
   - Reliquary or altar.
   - Bench, pew or simple furnishing.
   - Crate stack and service cabinet.
   - Grate, hatch and maintenance panel.

   **Key variants:** mounted/freestanding, working/broken. Separate emissive art from materials. Props that block shots or act as cover need explicit gameplay treatment; visual clutter alone should stay sparse.

17. **Exterior backgrounds and foreground framing**

   - Distant tower groups.
   - Long cathedral mass.
   - Dense roofline.
   - Aqueduct or elevated bridge silhouette.
   - Industrial stacks and pipework.
   - Colossal statue silhouette.
   - Far retaining walls descending into water.
   - Near dark arch framing a view.
   - Foreground broken pier.
   - Hanging chain or ruined railing at the screen edge.
   - Half-submerged wreckage.

   **Key variants:** low, medium and tall skyline profiles; sparse/dense groupings. The background should suggest that the playable district continues far beyond the arena.

18. **Designed assemblies and landmark set pieces**

   Alongside the parts, I’d establish these reusable compositions:

   - **Stair hall:** multiple levels, a central opening and alternate routes.
   - **Nave:** broad firing space, side galleries and a strong focal window.
   - **Gatehouse:** passage below, defended room above.
   - **Bell tower:** vertical circulation with exposed upper positions.
   - **Courtyard/cloister:** open artillery space enclosed by galleries.
   - **Bridge chapel:** a meaningful midpoint between buildings.
   - **Reservoir chamber:** water held above or beside playable space.
   - **Collapsed wing:** irregular floors and routes through broken structure.
   - **Crypt:** lower, tighter chambers that contrast with the open skyline.
   - **Industrial pump hall:** pipes, platforms and a large central void.

   Keep the fallen arch, shattered dome and colossal saints as bespoke landmarks. Each assembly should have intact and ruined layouts, with variations in entrances and elevation—not merely different surface decoration.

**I would not multiply all of this into every possible combination.** The baseline variant system should be:

| Variation | How we should usually produce it |
|---|---|
| Longer or taller structure | Repeat compatible middle sections |
| Left/right orientation | Mirror compatible geometry |
| Plain versus ceremonial | Add selected ornament |
| Faction ownership | Separate banners, marks and emissives |
| Wetness and age | Controlled overlays |
| Structural damage | Authored broken ends and ruin arrangements |
| Different room purpose | Change Back, openings, props and layout |
| Major landmark identity | Bespoke art |

**For the first usable district, I’d prioritise:** the original 14 bay-kit images, door/window frames, wall ends, foundations, one complete bridge family, balcony/parapet pieces, a roof family, and a small Near/Far Back set. That is enough to prove a tower, hall, courtyard and connecting bridge together.

Every part should be reviewed **assembled, lit, at play zoom, with a trooper beside it**. The success criterion is that we can immediately read where we can stand, what blocks a shot, what lies behind us, and how the place holds together.