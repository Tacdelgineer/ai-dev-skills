// node sheet.cjs <page.html> <sheet.png> t1 t2 ...  -> one contact sheet (270 px per frame) + any page errors
// Look at ONE sheet per round of fixes: cheaper than single frames.
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path'); const { execFileSync } = require('child_process');
(async () => {
  const [file, out, ...ts] = process.argv.slice(2); const tmp = fs.mkdtempSync(path.join(require('os').tmpdir(), 'sheet-'));
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 640, height: 1000 } }); const errs = [];
  p.on('pageerror', e => errs.push(e.message));
  await p.goto('file://' + path.resolve(file) + '?clean'); await p.waitForTimeout(1800);
  const frames = [];
  for (const t of ts) { const url = await p.evaluate(t => { seek(+t); return document.getElementById('c').toDataURL('image/png'); }, t);
    const f = path.join(tmp, `f_${t}.png`); fs.writeFileSync(f, Buffer.from(url.split(',')[1], 'base64')); frames.push(f); }
  await b.close();
  const inputs = frames.flatMap(f => ['-i', f]), filt = frames.map((_, i) => `[${i}]scale=270:-1[v${i}]`).join(';') + ';' + frames.map((_, i) => `[v${i}]`).join('') + `hstack=${frames.length}`;
  execFileSync('ffmpeg', ['-v', 'error', '-y', ...inputs, '-filter_complex', frames.length > 1 ? filt : '[0]scale=270:-1', out]);
  console.log(errs.length ? 'page errors:\n' + errs.join('\n') : 'no page errors', '->', out);
})();
