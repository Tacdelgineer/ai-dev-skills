#!/usr/bin/env node
/* render.mjs - film a canvas world, frame by exact frame, into the video's footage folders.
 *
 * FOOTAGE (default): every shot in a shot list, wide and vertical, 30 fps H.264, named by the
 * naming contract, plus ORDER.txt:
 *
 *   node scripts/video/render.mjs --page visuals/world/index.html --data visuals/world/data.json \
 *        --shots visuals/world/shots.mjs [--shapes wide,vertical] [--fps 30] [--only 03,curve] \
 *        [--out results/final_footage] [--png]
 *
 *   -> results/final_footage/{wide,vertical}/NN_chapter_shot.mp4 and results/final_footage/ORDER.txt
 *
 * STAT CARDS (--cards): every card the stat-card page lists, about 6 s each:
 *
 *   node scripts/video/render.mjs --cards --page visuals/statcard/index.html --data results/stats.json \
 *        [--seconds 6] [--only S1,S7] [--out results/film-stats]
 *
 *   -> results/film-stats/S#_name_wide.mp4 / _vertical.mp4, plus a PNG of each card's last frame
 *
 * SMOKE CHECK (--smoke): draw every room once and fail on anything the page logs as an error.
 * Works on a local page or on the live URL after publishing:
 *
 *   node scripts/video/render.mjs --smoke --page https://OWNER.github.io/REPO/
 *
 * How it works: the page is opened with ?record, which hands its clock to this script. Each frame
 * is api.step(1000/fps) then a screenshot piped straight into ffmpeg, so a take is identical
 * every time and cannot drop a frame however slowly Chrome draws. Frames travel as JPEG at
 * quality 95 (three times faster than PNG, and the H.264 output is 4:2:0 either way); --png
 * sends lossless frames instead. A local page is inlined with
 * its data first (pagekit.mjs); a URL is filmed as served. Without an ffmpeg that has libx264,
 * PNG frames are written instead, with the command to encode them elsewhere.
 *
 * A shot list is a module whose default export is a function (async is fine) returning shots in
 * video order. It is given { ask, rooms, stages, fps, ease, lerp }, where ask(expr) evaluates an
 * expression in the page with `api` bound to its control surface. A shot is:
 *   { chapter, shot, desc, seconds, setup: 'api.shot("room","floor",0)', at: (f, n) => 'api.stage(2)' }
 * `setup` runs once before the first frame; `at`, if given, runs before every frame f of n. */
import { spawn, execFileSync } from 'node:child_process';
import { writeFileSync, mkdirSync, rmSync } from 'node:fs';
import { join, resolve } from 'node:path';
import { pathToFileURL } from 'node:url';
import { arg, flag, SHAPES, API, openPage, findFfmpeg } from './pagekit.mjs';

const page = arg('page'), data = arg('data');
if (!page) { console.error('usage: render.mjs --page <html or url> [--data file.json] (--shots list.mjs | --cards | --smoke)'); process.exit(2); }
const fps = +arg('fps', 30), shapes = arg('shapes', 'wide,vertical').split(',');
const only = arg('only', null)?.split(',');
const ease = u => (u < .5 ? 4 * u * u * u : 1 - Math.pow(-2 * u + 2, 3) / 2);
const lerp = (a, b, t) => a + (b - a) * t;
const inPage = code => `(function(api){${code}})(${API})`;
const ask = b => expr => b.evaluate(`(function(api){return (${expr})})(${API})`);
const slug = s => String(s).toLowerCase().replace(/[^a-z0-9]+/g, '_').replace(/^_|_$/g, '');
const ffmpeg = findFfmpeg();
const lossless = flag('png') || !ffmpeg;          // PNG frames on disk when there is no encoder

/* Record n frames of whatever the page is showing, into one mp4 (or a folder of PNGs). */
async function take(b, target, n, before) {
  let enc = null, done = null;
  const framesDir = target.replace(/\.mp4$/, '');
  if (ffmpeg) {
    enc = spawn(ffmpeg, ['-loglevel', 'error', '-y', '-f', 'image2pipe', '-c:v', lossless ? 'png' : 'mjpeg', '-framerate', String(fps), '-i', 'pipe:0',
      '-an', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-r', String(fps), '-movflags', '+faststart', target],
      { stdio: ['pipe', 'ignore', 'pipe'] });
    let err = ''; enc.stderr.on('data', d => { err += d; });
    done = new Promise((ok, fail) => enc.on('exit', c => c === 0 ? ok() : fail(new Error(`ffmpeg: ${err.trim()}`))));
  } else { rmSync(framesDir, { recursive: true, force: true }); mkdirSync(framesDir, { recursive: true }); }
  const t0 = Date.now();
  for (let f = 0; f < n; f++) {
    if (before) await b.evaluate(inPage(before(f, n)));
    await b.evaluate(inPage(`api.step(${(1000 / fps).toFixed(4)})`));
    const img = lossless ? await b.shot('png') : await b.shot('jpeg', 95);
    if (enc) await new Promise(ok => enc.stdin.write(img, ok));
    else writeFileSync(join(framesDir, `frame_${String(f + 1).padStart(5, '0')}.png`), img);
  }
  if (enc) { enc.stdin.end(); await done; }
  const perFrame = (Date.now() - t0) / n;
  return { last: await b.shot('png'), perFrame };   // the page has not moved: this is the last frame
}

function probe(file) {
  try {
    const [w, h, rate, frames] = execFileSync('ffprobe', ['-v', 'error', '-select_streams', 'v:0', '-count_packets',
      '-show_entries', 'stream=width,height,r_frame_rate,nb_read_packets', '-of', 'csv=p=0', file]).toString().trim().split(',');
    const [a, c] = rate.split('/').map(Number);
    return `${w}x${h} ${Math.round(a / c)} fps ${frames} frames`;
  } catch { return 'written (no ffprobe to check it)'; }
}

async function footage() {
  const out = resolve(arg('out', 'results/final_footage'));
  const make = (await import(pathToFileURL(resolve(arg('shots'))).href)).default;
  let order = null;
  for (const shape of shapes) {
    const b = await openPage(page, { data, params: `record${shape === 'vertical' ? '&vertical' : ''}`, size: SHAPES[shape] });
    try {
      const rooms = await ask(b)('api.rooms()'), stages = await ask(b)('api.stages?api.stages():0');
      const shots = (await make({ ask: ask(b), rooms, stages, fps, ease, lerp })).map((s, k) =>
        ({ ...s, nn: String(k + 1).padStart(2, '0'), name: `${String(k + 1).padStart(2, '0')}_${slug(s.chapter)}_${slug(s.shot)}` }));
      order ??= shots;
      mkdirSync(join(out, shape), { recursive: true });
      for (const s of shots.filter(s => !only || only.some(o => s.name.includes(o)))) {
        if (s.setup) await b.evaluate(inPage(s.setup));
        const target = join(out, shape, `${s.name}.mp4`);
        const { perFrame } = await take(b, target, Math.round(s.seconds * fps), s.at);
        console.log(`  ${shape} ${s.name}: ${ffmpeg ? probe(target) : 'PNG frames'} (${(perFrame / 1000).toFixed(2)} s/frame)`);
      }
    } finally { b.close(); }
  }
  // ORDER.txt always lists the whole film, so an --only re-render never renumbers anything
  writeFileSync(join(out, 'ORDER.txt'), ['NN | chapter | shot | description | seconds',
    ...order.map(s => `${s.nn} | ${slug(s.chapter)} | ${slug(s.shot)} | ${s.desc || ''} | ${s.seconds}`)].join('\n') + '\n');
  console.log(`${join(out, 'ORDER.txt')}: ${order.length} shots, ${order.reduce((a, s) => a + s.seconds, 0)} s`);
}

async function cards() {
  const out = resolve(arg('out', 'results/film-stats')), seconds = +arg('seconds', 6);
  mkdirSync(out, { recursive: true });
  for (const shape of shapes) {
    const b = await openPage(page, { data, params: `record${shape === 'vertical' ? '&vertical' : ''}`, size: SHAPES[shape] });
    try {
      for (const c of (await ask(b)('api.cards()')).filter(c => !only || only.includes(c.id))) {
        await b.evaluate(inPage(`api.card(${JSON.stringify(c.id)})`));
        const target = join(out, `${c.id}_${slug(c.name)}_${shape}.mp4`);
        const { last } = await take(b, target, Math.round(seconds * fps));
        writeFileSync(target.replace(/\.mp4$/, '.png'), last);
        console.log(`  ${shape} ${c.id}: ${ffmpeg ? probe(target) : 'PNG frames'} -> ${target}`);
      }
    } finally { b.close(); }
  }
}

async function smoke() {
  const b = await openPage(page, { data, params: 'record', size: [1600, 900] });
  let fails = 0;
  try {
    // rooms log their own errors as console.error('room ' + id, e) and keep going, so an error is
    // pinned on the room it names; anything that names no room fails the building shot
    const rooms = await ask(b)('api.rooms()');
    const names = e => rooms.some(r => e.includes(`room ${r}`));
    for (const where of [...rooms.map(r => ['room', r]), ['building', null]]) {
      const before = b.errors.length;
      await b.evaluate(inPage(`api.shot(${JSON.stringify(where[0])},${JSON.stringify(where[1])},0)`));
      for (let f = 0; f < 6; f++) await b.evaluate(inPage('api.step(83.3333)'));
      const errs = b.errors.slice(before).filter(e => where[1] ? e.includes(`room ${where[1]}`) : !names(e));
      console.log(`  ${errs.length ? 'FAIL' : 'ok  '} ${where[1] || where[0]}${errs.length ? '   ' + errs[0].split('\n')[0] : ''}`);
      if (errs.length) fails++;
    }
  } finally { b.close(); }
  console.log(fails ? `${fails} failed` : 'every room drew without an error');
  process.exit(fails ? 1 : 0);
}

if (!ffmpeg && !flag('smoke')) console.log('No ffmpeg with libx264 (apt install ffmpeg, or set $FFMPEG): writing PNG frames instead.\n' +
  `Encode each folder elsewhere with: ffmpeg -framerate ${fps} -i frame_%05d.png -c:v libx264 -pix_fmt yuv420p -crf 18 shot.mp4`);
if (flag('smoke')) await smoke();
else if (flag('cards')) await cards();
else if (arg('shots')) await footage();
else { console.error('say what to render: --shots list.mjs, --cards or --smoke'); process.exit(2); }
