# game-3d-asset-pipeline

A compact Codex Skill for bringing GLB characters and weapons into an existing Three.js game: audit/classify → optimize if useful → rig/skin if needed → reuse states → attach/stow → export → integrate → light validation → checkpoint.

[SKILL.md](SKILL.md) contains the operational instructions. Supply the target repository, incoming assets and intended role; existing game states, helpers and attachment behavior guide the work. Installation follows the [repository README](../../README.md). Commit/push instructions in the task determine the checkpoint destination.

Example invocation:

```text
Use game-3d-asset-pipeline.
Process the new GLB in incoming-assets as a melee enemy.
Reuse the project's existing melee animation/gameplay states.
Integrate it, run lightweight validation, and checkpoint.
```

Provenance: Neon Ronin's completed character pipeline and weapon fixes through commit `6e76fb2`:

- [Blender audit/rig/animation/export helpers](https://github.com/Tacdelgineer/neon-ronin/tree/6e76fb2/tools/forge3d-step04).
- [Final single-sword hand/stow placement](https://github.com/Tacdelgineer/neon-ronin/blob/6e76fb2/lib/game/player-model.js).
- [Pipeline milestone notes](https://github.com/Tacdelgineer/neon-ronin/blob/6e76fb2/docs/step-04-final-character-assets.md); earlier attachment descriptions are historical, so consult the linked runtime code for the final behavior.

No Neon Ronin scripts, models, textures, or project dependencies are copied. Its fitted skeletons, skinning thresholds, weapon axes/pivots, texture-restoration assumptions and paths remain project-specific. The Skill captures the reusable decisions; it is self-contained and does not require the reference repository.
