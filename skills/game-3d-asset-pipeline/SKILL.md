---
name: game-3d-asset-pipeline
description: Process GLB characters and weapons for an existing Three.js game with Blender. Use for asset audit, useful optimization, humanoid or mechanical rigging, animation reuse, weapon attachment/stow, export, integration, and a lightweight checkpoint.
---

# Game 3D asset pipeline

Carry out the requested asset work with the target project's existing tools and gameplay. Skip stages already satisfied by a usable source rig, animation, or asset. Keep progress and final output terse; do not build a pipeline framework or expand into combat, AI, camera, arena, or animation-system redesign.

## Inspect and preserve

- Read the project's instructions, current Git state, asset docs, successful Blender scripts, loader, animation controller, and weapon attachment code before editing. Prefer current code and completed commits over older milestone notes describing superseded behavior.
- Identify asset URLs/output folders, character scale and forward axis, required states and hit timings, socket names/parents, resource ownership, validation commands, and checkpoint destination. Reuse working helpers before writing a new script; adapt only what the asset requires.
- Never overwrite, move, or destructively normalize original source GLBs. Record their paths and SHA-256 checksums; save derived GLBs and working scenes separately. Preserve the repository's existing asset/LFS policy.

## Audit and classify

- Record a compact inventory: source path/hash/size, mesh and triangle counts, bounds/dimensions/transforms, materials and texture formats/resolution, skins/skeletons, and animation clips. Distinguish source counts from counts after import and local bounds from transformed scene bounds.
- Inspect a few consistent front/side or three-quarter previews when needed. Classify the requested hero/enemy/weapon/scabbard role from geometry and reference evidence, rather than filenames alone. Respect the user's assigned role; resolve material ambiguity before expensive rig work.
- Confirm whether the source already has a usable rig, clips, or sockets. Audit all relevant meshes, not just the first one. Determine ground alignment, intended facing, weapon grip/guard/tip, and any existing carry anchor.

## Optimize only when useful

- Leave acceptable geometry and textures alone. Simplify only to address an observed download/render cost or project budget; select a budget from the model's silhouette, articulation, close-up detail, and gameplay camera.
- Reuse conservative weld/degenerate cleanup and decimation where appropriate. Preserve UVs, material assignments, joint boundaries, and skin data; avoid indiscriminate welding across rigid parts or contacts. Compare the result with the source and back off if armor, hands, blade shape, or silhouette suffers.
- Recompute normals after geometry rotation/cleanup when imported split normals become stale. Reuse intermediate caches only while their source hash and fitting/normalization settings still match.

## Rig and reuse animation states

- **Humanoid/cloth:** fit the project's existing anatomical chains to actual shoulders, elbows, wrists, hips, knees, and ankles. Normalize weights, respect the project's influence limit, and use rigid weights for accessories/plates where appropriate. Inspect major glove/waist or scarf contacts; fix destructive bridges with targeted cleanup rather than a new retopology/cloth pipeline.
- **Mechanical:** preserve hard parts. Prefer rigid part-to-bone or per-triangle weighting where blended weights stretch metal; split joint seams only as needed. Fit real articulated limbs and mount points instead of assuming every robot shares a humanoid layout. Small hinge seams are preferable to rubber armor.
- Reuse/retarget the game's existing named states and clips. Map only states the current gameplay already uses, such as idle/run/attack/dodge or hit/death. Do not invent attacks, enemy behavior, or gameplay to demonstrate an asset.
- Keep simulation movement, hit detection, attack/dodge timers, pause, and hit-stop authoritative. For an in-place controller, avoid adding animation root travel. Align the authored strike pose to existing impact timing; adjust visual cadence only if needed, without changing travel speed or damage.

## Attach and stow weapons

- Reuse named sockets and their existing parents. Examples such as `weapon_hand_r` and `weapon_sheath` are conventions, not required names; a cannon may need a torso mount, and a scabbard may follow hips or chest. Verify actual loaded node names, which can differ from Blender names.
- Fit the weapon's origin to its physical grip/mount and confirm blade/barrel direction visually. Do not assume a PCA axis sign or universal forward axis is correct.
- Keep **separate configurable hand and stow position/rotation/scale** in a small local binding or constants. Preserve a working hand transform while adjusting carry placement. On switching sockets, apply the chosen local transform explicitly; do not accidentally retain the stow offset in the hand or preserve an unwanted world transform.
- For a draw/stow policy, reuse one sword instance reparented between the hand and carry sockets. Follow existing state rules; for a sheathed hero this normally means idle/run/dodge stowed, attack in hand, and completion/cancellation back to stow. Never show two copies of the sword.
- Place the carry anchor against the actual waist/hip or back. If a scabbard exists, align the guard with its mouth and seat the blade within its direction and length; leave the hilt visible. Adjust the shared carry anchor for sword and scabbard together when necessary. Check ground clearance and major body clipping during movement.
- Preserve the project's sheath visibility behavior. A correctly named parent and `visible=true` do not prove believable placement: inspect the rendered character from the gameplay camera before declaring stow fixed.

## Preserve materials and export

- Retain texture resolution/UVs, PBR assignments, metallic/roughness/normal maps, alpha/double-sided settings, and supported extensions where practical. Record intentional tint/emissive changes separately from preservation. Reuse existing emissive/bloom capabilities if requested; do not add a renderer or dependency.
- If Blender rewrites embedded textures or material values, inspect the existing export-preservation helper first. Restore original payloads only with a verified mapping of images, samplers, material slots, and primitives; do not blindly transplant a single-material JSON layout into a different asset. Check hashes when exact texture preservation is intended.
- Use the installed Blender executable headlessly with a nonzero exit on script errors. Command shape (substitute the project's actual executable, script, and arguments):

  ```sh
  blender --background --python-exit-code 1 --python path/to/project_script.py
  ```

  Pass script arguments after `--` only as supported by that script. Match export options to the installed Blender version; do not hardcode workstation paths or install tools unnecessarily.
- Export glTF 2.0 binary GLB with the required meshes, armature/skin, named socket nodes and their parents, needed animation actions, and embedded textures. Include non-deforming anchors when needed; static weapons need no invented skin/animation. Preserve clip names, loop boundaries, and bind transforms; sample/bake supported actions so export does not silently retain only idle.
- Fresh-import a newly rigged/exported GLB once and sample representative rest, run, strike, and carry poses. Check finite/bounded vertices, valid normalized weights and joint indices, required clips/sockets, and material/texture presence. Keep this asset check proportional; do not render exhaustive frame grids.

## Integrate with Three.js

- Replace the visual/model URL through the current `GLTFLoader` and controller; preserve the simulation root, hitboxes, timing, and fallback behavior. Fit visual scale, ground offset, and facing from actual bounds rather than copying another project's values.
- Let the loader preserve PBR texture semantics: base color/emissive use sRGB; metallic/roughness/normal data do not. Avoid reassigning all maps to one color space.
- Reuse the existing mixer, state mapping, and socket updater. For skinned enemy instances, use skeleton-safe cloning with independent bones/mixers and any independently mutated materials; share immutable geometry/textures where the project already does. Dispose instance-owned and shared resources at their respective owners, without double disposal or serializing live scene objects in clone metadata.

## Validate and checkpoint

- Follow any narrower validation requested by the user. Otherwise run the existing automated tests once, typecheck/build once, and one short browser smoke of the changed states and attachments. Use the existing runner/server; do not replay waves, add diagnostics frameworks, or pursue minor cloth creases/foot sliding outside scope.
- Confirm actual model/material visibility and idle → run → attack → return-to-idle switching, plus dodge/hit/death only when relevant to the change. Inspect rendered grip/stow placement and console-breaking errors. Report visual fixtures or skipped checks honestly. Once checks pass, stop; repeat a failing check only after a relevant fix.
- Briefly update an existing milestone doc with assets changed, validation, and material limitations. Create one small milestone commit containing only the requested work and necessary derived assets. Follow the task's commit/push authorization; when pushing is authorized, use the requested destination or existing upstream. Preserve remotes/LFS and avoid force push or unrelated dirty changes.
- Final output: concise completion/issues, validation result, and commit hash. Do not produce a long pipeline report.
