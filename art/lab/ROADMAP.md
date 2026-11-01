# GRIMSPIRE art roadmap

Jarred's agreed sequence, October 31, 2026 (Vancouver):

1. **Tidy Library.** One card per actual asset; versions and source material inside it; trooper states inside a character; references in Archive. Preserve all artwork and saves. Stable asset identity distinguishes Save from New.
2. **Sort out the arm.** One editable foreground sprite attached at the hand, with existing Reach. Review its look and placement with Jarred before wider rollout.
3. **Tweak existing assets.** Manual Forge editing alongside assistant-made changes. Keep exact revisions reviewable.
4. **Explore new weapon sheets.** Riff on sheets first, then bring the chosen directions into Forge.
5. **Work toward full asset rollout.** Promote reviewed assets through focused integrations against current main.
6. **Expand the asset set and world art direction.** Follow the project's north star; establish the specific reference/brief with Jarred before broad new art production.

## Library implementation

`hosted/families.json` explicitly maps existing document IDs to stable asset IDs,
animation/component state keys, roles and initial browsing defaults. It retains
all 161 catalog entries and nine old Library registrations. There are 32 current
asset cards and four reference cards in Archive at this checkpoint.

New assets get an independent identity even when their display code matches an
existing item. Saves add draft versions to the same asset/state. The latest draft
opens by default for that state; the initial catalog default stays available in
Versions & sources. Neither browsing default nor Save grants approval/integration.
Original document paths/IDs remain valid for historical builds and rig selections.
New catalog entries without an explicit mapping remain recoverable in Archive.

Verification: automated save/version/state/provenance and existing hosted release
checks; local read-only browser preview of grouped browsing and full animation
opening. This does not constitute a signed-in hosted save walkthrough. Deployment
status must be reported separately after pushing.
