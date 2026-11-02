# Additional local battle checks — first set-piece batch

Follows `phase3-setpieces-v001` without changing that saved record. Main source `dd6555a`, current live payload plus S01/S09/S07/S03 drafts and no-vent C04; local `/api/game?grounds=1` builds. Desktop 1366×768 and phone-shaped touch 390×844 browser contexts. External services blocked; no online match or field report sent.

All five browser launches loaded the Forge art/testing ground with zero page-script errors. The normal head placed by desktop attempt 3; pedestal saint by attempt 2; gargoyle by attempt 1. S09 did not fit in 12 sampled desktop restarts, but did place on phone-layout attempt 9 (map generation varies; phone shape is not claimed as the cause). `battle-checks.json` records exact placed pieces, sockets and errors from the final sampled map per context.

**Finding for Claude:** S09's candidate support/headroom is scarce on current generated terrain even with selected-slot test weighting. Keep the 200-art-pixel height. Please review sump candidate pools/support spans and bounding-box clearance before final scene review; do not silently scale it down. S01 also does not fit every map, which is reasonable. Need a fixed suitable test map to compare both heads at waterline.

Screenshots saved locally in the task workspace under `phase3/setpieces-v001/`. The default camera shows saints/gargoyles and braziers; sump heads may be outside its initial view. These checks establish browser loading and actual generated placement, not a complete phone visual approval of the heads, water animation, destruction or combat. Native staged head/sink/light comparison remains in the prior review folder. Exact-art approval and live release remain pending.
