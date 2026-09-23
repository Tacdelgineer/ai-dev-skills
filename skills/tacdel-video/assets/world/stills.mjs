/* stills.mjs - README screenshots and GIFs for scripts/stills.mjs, from the live page or a local one.
 *
 *   node scripts/video/stills.mjs --page https://OWNER.github.io/REPO/ --stills visuals/world/stills.mjs \
 *        --size 1600x900 --out docs/screenshots
 *
 * One entry per image. A still is framed by `setup`, then held for a few frames; a GIF runs `at`
 * before each frame. `api` is the page's control surface (window.__world). */
export default async ({ stages }) => [
  { name: 'building', setup: "api.shot('building',null,0); api.play(false); api.stage(api.stages()-1)" },
  { name: 'floor', setup: "api.shot('room','floor',0); api.play(false); api.stage(api.stages()-1)" },
  { name: 'curve_draws', gif: { seconds: 5, fps: 12, width: 800 },
    setup: "api.shot('room','curve',0); api.play(false); api.stage(0)",
    at: (f, n) => `api.stage(${Math.min(stages - 1, Math.floor(f / (n * .8) * stages))})` },
];
