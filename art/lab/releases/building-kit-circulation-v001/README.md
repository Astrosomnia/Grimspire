# Building-kit circulation and roof revisions · 17 Nov 2026

Seven new saved versions from Claude's Skinned review: BK40a, BK41a, BK42a, BK43a, BK50a/b, BK81a. Same families and component letters; earlier saves remain immutable history. No wall variants are changed.

Stairs have solid diagonal stringers beneath horizontal tread caps. Flight thickness is about20 perpendicular, with stepped caps; BK41 retains its32-wide break. BK43 Body ledges are pixel-identical to the previous save, with a new Back newel and eight wrapping tread fans. Both lean-to widths have two staggered tile courses, a recessed fascia and low-end drip return within the16px envelope. BK81 side posts y24–112 are Back; its full-width doorway y28–112 is empty Body, so tiled spans do not add walls at their joints.

Final art is drawn at native1× coordinates in draw.py, using native_base.py primitives. No source resampling. Body/Height/Guts masks match; Height is greyscale. All seven readability checks pass, and all66 Forge tests pass. validate.py checks connected stair flights (two disconnected halves for broken stair), gap preservation, exact spiral ledges and full bridge corridor clearance. proof.png shows raw layers and an illustrative Height-light study; it is not an engine rendering or movement test.

All versions remain ready:false and await Skinned review. No live game changes. Exact saved version IDs and hashes: published-manifest.json.
