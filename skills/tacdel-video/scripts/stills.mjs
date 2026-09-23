#!/usr/bin/env node
/* stills.mjs - still frames and GIFs of a canvas world: README screenshots, thumbnails' raw
 * material, and chart PNGs for the edit.
 *
 *   node scripts/video/stills.mjs --page https://OWNER.github.io/REPO/ --stills docs/stills.mjs \
 *        [--size 1600x900] [--out docs/screenshots] [--max-kb 400] [--max-gif-mb 5] [--only pile]
 *   node scripts/video/stills.mjs --page visuals/charts/index.html --data visuals/world/data.json \
 *        --stills visuals/charts/stills.mjs --size 3840x2160 --format png --out results/filmpack
 *
 * The page is opened with ?record&clean&still: the clock is this script's, the UI is hidden and
 * the idle camera drift is off, so every still is framed exactly and comes out the same each time.
 * A JPG is re-taken at lower quality until it fits --max-kb; a GIF is re-encoded narrower until it
 * fits --max-gif-mb (ffmpeg needed for GIFs).
 *
 * A stills list is a module whose default export is a function (async is fine) returning stills.
 * It is given { ask, rooms, stages }, where ask(expr) evaluates in the page with `api` bound to its
 * control surface. A still is one of:
 *   { name: 'vault_open', setup: "api.shot('room','vault',0); api.open(1)", steps: 6 }
 *   { name: 'pile_fills', setup: '...', gif: { seconds: 6, fps: 12, width: 800 }, at: (f, n) => '...' }
 * `setup` runs once; `steps` frames of 1/12 s then pass so tweens land and the drawing settles;
 * a GIF runs `at(f, n)` before each of its frames. */
import { execFileSync } from 'node:child_process';
import { writeFileSync, mkdirSync, rmSync, statSync, mkdtempSync } from 'node:fs';
import { join, resolve } from 'node:path';
import { tmpdir } from 'node:os';
import { pathToFileURL } from 'node:url';
import { arg, API, openPage, findFfmpeg } from './pagekit.mjs';

const page = arg('page'), list = arg('stills');
if (!page || !list) { console.error('usage: stills.mjs --page <html or url> --stills list.mjs [--data file.json] [--size 1600x900]'); process.exit(2); }
const [w, h] = arg('size', '1600x900').split('x').map(Number);
const out = resolve(arg('out', 'docs/screenshots')), format = arg('format', 'jpg');
const maxKb = +arg('max-kb', 400), maxGif = +arg('max-gif-mb', 5) * 1024 * 1024;
const only = arg('only', null)?.split(',');
const inPage = code => `(function(api){${code}})(${API})`;
const ask = b => expr => b.evaluate(`(function(api){return (${expr})})(${API})`);
const kb = f => Math.round(statSync(f).size / 1024);
mkdirSync(out, { recursive: true });

const b = await openPage(page, { data: arg('data'), params: arg('params', 'record&clean&still'), size: [w, h] });
try {
  const rooms = await ask(b)('api.rooms?api.rooms():[]'), stages = await ask(b)('api.stages?api.stages():0');
  const stills = await (await import(pathToFileURL(resolve(list)).href)).default({ ask: ask(b), rooms, stages });
  for (const s of stills.filter(s => !only || only.some(o => s.name.includes(o)))) {
    if (s.setup) await b.evaluate(inPage(s.setup));
    if (!s.gif) {
      for (let k = 0; k < (s.steps ?? 6); k++) await b.evaluate(inPage('api.step(83.3333)'));
      if (format === 'png') { const f = join(out, `${s.name}.png`); writeFileSync(f, await b.shot('png')); console.log(`  ${f}  ${kb(f)} KB`); continue; }
      const f = join(out, `${s.name}.jpg`);
      let q = 86;
      do { writeFileSync(f, await b.shot('jpeg', q)); q -= 6; } while (kb(f) > maxKb && q >= 40);
      console.log(`  ${f}  ${kb(f)} KB, quality ${q + 6}${kb(f) > maxKb ? '  STILL OVER ' + maxKb + ' KB' : ''}`);
      continue;
    }
    const ffmpeg = findFfmpeg();
    if (!ffmpeg) throw new Error('GIFs need ffmpeg (apt install ffmpeg, or set $FFMPEG)');
    const { seconds = 6, fps = 12 } = s.gif, n = Math.round(seconds * fps), dir = mkdtempSync(join(tmpdir(), 'gif-'));
    for (let f = 0; f < n; f++) {
      if (s.at) await b.evaluate(inPage(s.at(f, n)));
      await b.evaluate(inPage(`api.step(${(1000 / fps).toFixed(4)})`));
      writeFileSync(join(dir, `f_${String(f).padStart(4, '0')}.png`), await b.shot('png'));
    }
    const gif = join(out, `${s.name}.gif`);
    // narrower until it fits: one palette for the whole clip, ordered dither so the halftone stays crisp
    for (let width = s.gif.width || 800; ; width = Math.round(width * .85 / 2) * 2) {
      execFileSync(ffmpeg, ['-loglevel', 'error', '-y', '-framerate', String(fps), '-i', join(dir, 'f_%04d.png'), '-vf',
        `scale=${width}:-2:flags=lanczos,split[a][b];[a]palettegen=max_colors=128:stats_mode=diff[p];[b][p]paletteuse=dither=bayer:bayer_scale=3:diff_mode=rectangle`,
        '-loop', '0', gif]);
      if (statSync(gif).size <= maxGif || width < 360) { console.log(`  ${gif}  ${(statSync(gif).size / 1048576).toFixed(1)} MB, ${width} wide, ${n} frames`); break; }
    }
    rmSync(dir, { recursive: true, force: true });
  }
  if (b.errors.length) console.log(`the page logged ${b.errors.length} error(s); first: ${b.errors[0].split('\n')[0]}`);
} finally { b.close(); }
