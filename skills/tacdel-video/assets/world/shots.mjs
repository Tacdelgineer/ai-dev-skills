/* shots.mjs - the film's shot list for scripts/render.mjs, in the order the clips appear in the video.
 *
 *   node scripts/video/render.mjs --page visuals/world/index.html --data visuals/world/data.json \
 *        --shots visuals/world/shots.mjs
 *
 * Each shot becomes NN_chapter_shot.mp4 (NN = its place in this list) in wide/ and vertical/, and a
 * line in ORDER.txt. `chapter` must match the script's chapter names. Four kinds of shot cover
 * most of a video: a room as it stands, a room while its data advances, a camera move, and the
 * whole building. `api` is the page's control surface (window.__world); `ask` reads from it. */
export default async ({ ask, stages, ease, lerp }) => {
  const floor = await ask("api.frame('floor')"), desk = await ask("api.spot('floor', 5.8, 5.7, 1)");
  return [
    { chapter: 'hook', shot: 'building', desc: 'the whole building, drifting', seconds: 8,
      setup: "api.shot('building',null,0); api.play(true)" },

    { chapter: 'floor', shot: 'room', desc: 'the floor with the data playing', seconds: 10,
      setup: "api.shot('room','floor',0); api.stage(0); api.play(true)" },

    // the data drives the shot: one stage per slice, so the curve draws itself on camera
    { chapter: 'curve', shot: 'draws', desc: 'the curve draws itself, stage by stage', seconds: 12,
      setup: "api.play(false); api.shot('room','curve',0)",
      at: (f, n) => `api.stage(${Math.min(stages - 1, Math.floor(f / (n * .85) * stages))})` },

    // a camera move: an eased push from the room's framing toward a point inside it
    { chapter: 'floor', shot: 'push', desc: 'slow push onto the table', seconds: 10,
      setup: `api.play(false); api.stage(${stages - 1})`,
      at: (f, n) => { const u = ease(f / (n - 1));
        return `api.cam(${lerp(floor.x, desk.x, u * .8)},${lerp(floor.y, desk.y, u * .8)},${lerp(floor.zoom, floor.zoom * 2.2, u)})`; } },
  ];
};
