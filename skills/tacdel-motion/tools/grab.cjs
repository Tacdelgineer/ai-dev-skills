// node grab.cjs page.html out.png width cols t1 t2 ... -> contact grid with timestamps + page errors
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path'); const { execFileSync } = require('child_process');
(async () => {
  const [file, out, width, cols, ...ts] = process.argv.slice(2); const tmp = fs.mkdtempSync(path.join(require('os').tmpdir(), 'grab-'));
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 640, height: 1000 } }); const errs = [];
  p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await p.goto('file://' + path.resolve(file) + '?clean'); await p.waitForTimeout(1500);
  const frames = [];
  for (const t of ts) { const url = await p.evaluate(t => { seek(+t); return document.getElementById('c').toDataURL('image/png'); }, t);
    const f = path.join(tmp, `f_${frames.length}.png`); fs.writeFileSync(f, Buffer.from(url.split(',')[1], 'base64')); frames.push([f, t]); }
  await b.close();
  const w = +width, c = +cols, n = frames.length, rows = Math.ceil(n / c), h = Math.round(w * 16 / 9);
  const inputs = frames.flatMap(([f]) => ['-i', f]);
  let filt = frames.map(([, t], i) => `[${i}]scale=${w}:${h},drawtext=text='${t}':x=8:y=8:fontsize=${Math.round(w / 10)}:fontcolor=white:box=1:boxcolor=black@0.6[v${i}]`).join(';');
  const pad = rows * c - n; for (let k = 0; k < pad; k++) filt += `;color=c=gray:s=${w}x${h}:d=1[p${k}]`;
  const all = [...frames.map((_, i) => `[v${i}]`), ...Array.from({ length: pad }, (_, k) => `[p${k}]`)];
  filt += ';' + all.join('') + `xstack=inputs=${all.length}:layout=` + all.map((_, i) => `${(i % c) * w}_${Math.floor(i / c) * h}`).join('|') + '[o]';
  execFileSync('ffmpeg', ['-v', 'error', '-y', ...inputs, '-filter_complex', filt, '-map', '[o]', '-frames:v', '1', out]);
  console.log(errs.length ? 'page errors:\n' + [...new Set(errs)].join('\n') : 'no page errors', '->', out);
})();
