# ai-dev-skills

Small, practical Codex and Claude Skills drawn from completed development work.

- [game-3d-asset-pipeline](skills/game-3d-asset-pipeline/README.md): process GLB characters and weapons for an existing Three.js game using its current Blender helpers, animation states, and attachment system.
- [tacdel-video](skills/tacdel-video/SKILL.md): turn a coding or AI experiment into a faceless YouTube explainer: code-drawn neon risograph rooms filmed to footage, stat cards and charts from the results files, a script written to the footage, voice, CapCut edit and packaging. Carries the renderer, a starter room, a stat-card template and director-mode controls. A Claude skill: install the folder under `~/.claude/skills/`, or zip it (`cd skills && zip -r ../dist/tacdel-video.zip tacdel-video`) and upload it to claude.ai. Drawn from [hedgefly](https://github.com/Tacdelgineer/hedgefly); the drawing core is adapted from IshaanKalra2103's [creative-skills](https://github.com/IshaanKalra2103/creative-skills) (MIT, notice in `assets/NOTICE.txt`), and the look is inspired by Kevin Ngo's "a small light, room by room".

Each Skill has a `SKILL.md` instruction entrypoint; the Codex Skills also carry a short README with usage and provenance. Install a Codex Skill folder under `$CODEX_HOME/skills` (normally `~/.codex/skills`) to make it available in future sessions. Project code and source assets stay in their own repositories.
