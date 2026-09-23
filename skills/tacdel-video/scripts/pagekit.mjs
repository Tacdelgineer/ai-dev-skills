/* pagekit.mjs - shared plumbing for render.mjs, stills.mjs and build_single.mjs. Not run directly.
 *
 * - findChrome(): $CHROME, else Playwright's newest headless shell, else chromium/chrome on PATH.
 *   Google ships no Chrome for ARM64 Linux; on a DGX Spark or any ARM box use
 *   `npx playwright install chromium-headless-shell` once.
 * - findFfmpeg(): $FFMPEG, else an ffmpeg on PATH that has libx264 (`apt install ffmpeg`).
 *   Playwright's bundled ffmpeg is VP8-only and cannot write the H.264 the edit needs.
 * - inlinePage(): one page + its local <script src> files + the data file -> one HTML string that
 *   runs from file:// or GitHub Pages with no server. The data becomes window.__RUN__.
 * - launch()/openPage(): headless Chrome over the DevTools protocol using Node's own WebSocket
 *   (Node 22+), no npm packages. openPage() waits for the page's control surface to be ready.
 *
 * Paths are resolved from the current directory: run the scripts from the project root. */
import { spawn, execFileSync } from 'node:child_process';
import { readFileSync, writeFileSync, readdirSync, existsSync, rmSync } from 'node:fs';
import { resolve, dirname, join } from 'node:path';
import { homedir, tmpdir } from 'node:os';

export const arg = (name, fallback) => { const k = process.argv.indexOf(`--${name}`); return k > 0 ? process.argv[k + 1] : fallback; };
export const flag = name => process.argv.includes(`--${name}`);
export const SHAPES = { wide: [1920, 1080], vertical: [1080, 1920] };
export const isUrl = s => /^https?:\/\//.test(s);

/* The control surface a filmable page exposes. hedgefly called it __hedgefly; both are accepted. */
export const API = '(window.__world||window.__hedgefly)';

const LS = String.fromCharCode(0x2028), PS = String.fromCharCode(0x2029);
const safeJson = v => JSON.stringify(v).replace(/</g, '\\u003c').split(LS).join('\\u2028').split(PS).join('\\u2029');

export function inlinePage(pagePath, dataPath) {
  const page = resolve(pagePath);
  let html = readFileSync(page, 'utf8');
  // every local <script src="..."></script> is replaced by the file's contents
  html = html.replace(/<script\s+src="([^"]+)"\s*><\/script>/g, (tag, src) => {
    if (/^(https?:)?\/\//.test(src)) return tag;
    const code = readFileSync(resolve(dirname(page), src), 'utf8');
    if (/<\/script/i.test(code)) throw new Error(`${src} contains a closing script tag and cannot be inlined`);
    return `<script>/* inlined from ${src} */\n${code}\n</script>`;
  });
  let data = null;
  if (dataPath) {
    data = JSON.parse(readFileSync(resolve(dataPath), 'utf8'));
    const at = html.search(/<script[\s>]/i);
    if (at < 0) throw new Error(`${pagePath} has no script to put the data in front of`);
    html = html.slice(0, at) + `<script>window.__RUN__=${safeJson(data)};</script>\n` + html.slice(at);
  }
  return { html, data };
}

export function findChrome() {
  if (process.env.CHROME) return process.env.CHROME;
  const cache = join(homedir(), '.cache', 'ms-playwright');
  if (existsSync(cache)) {
    for (const d of readdirSync(cache).filter(d => d.startsWith('chromium_headless_shell-')).sort().reverse())
      for (const sub of readdirSync(join(cache, d))) {
        const bin = join(cache, d, sub, 'chrome-headless-shell');
        if (existsSync(bin)) return bin;
      }
  }
  for (const bin of ['chromium', 'chromium-browser', 'google-chrome', 'google-chrome-stable'])
    try { execFileSync('which', [bin], { stdio: 'ignore' }); return bin; } catch { /* next */ }
  throw new Error('no headless Chrome: set $CHROME, or run `npx playwright install chromium-headless-shell`');
}

export function findFfmpeg() {
  if (process.env.FFMPEG) return process.env.FFMPEG;
  try { if (execFileSync('ffmpeg', ['-hide_banner', '-encoders'], { stdio: ['ignore', 'pipe', 'ignore'] }).toString().includes('libx264')) return 'ffmpeg'; }
  catch { /* none */ }
  return null;
}

export async function launch(w, h) {
  const chrome = spawn(findChrome(), ['--headless', '--disable-gpu', '--no-sandbox', '--hide-scrollbars', '--mute-audio',
    '--allow-file-access-from-files', '--remote-debugging-port=0', `--window-size=${w},${h}`, 'about:blank'],
    { stdio: ['ignore', 'ignore', 'pipe'] });
  const wsUrl = await new Promise((ok, fail) => {
    let buf = '';
    const t = setTimeout(() => fail(new Error('Chrome did not start (no DevTools endpoint within 20 s)')), 20000);
    chrome.stderr.on('data', d => { buf += d; const m = buf.match(/DevTools listening on (ws:\/\/\S+)/); if (m) { clearTimeout(t); ok(m[1]); } });
    chrome.on('exit', c => fail(new Error(`Chrome exited with ${c} before it was ready:\n${buf.slice(-600)}`)));
  });
  const ws = new WebSocket(wsUrl);
  await new Promise((ok, fail) => { ws.onopen = ok; ws.onerror = fail; });
  let id = 0; const pending = new Map(), listeners = [];
  ws.onmessage = e => { const m = JSON.parse(e.data);
    if (m.id && pending.has(m.id)) { const { ok, fail } = pending.get(m.id); pending.delete(m.id); m.error ? fail(new Error(JSON.stringify(m.error))) : ok(m.result); }
    else if (m.method) for (const l of listeners) l(m); };
  const send = (method, params = {}, sessionId) => new Promise((ok, fail) => {
    const msg = { id: ++id, method, params }; if (sessionId) msg.sessionId = sessionId;
    pending.set(msg.id, { ok, fail }); ws.send(JSON.stringify(msg)); });
  const { targetId } = await send('Target.createTarget', { url: 'about:blank' });
  const { sessionId } = await send('Target.attachToTarget', { targetId, flatten: true });
  const page = (m, p) => send(m, p, sessionId);
  await page('Page.enable'); await page('Runtime.enable');
  await page('Emulation.setDeviceMetricsOverride', { width: w, height: h, deviceScaleFactor: 1, mobile: false });
  const errors = [];
  listeners.push(m => {
    if (m.sessionId !== sessionId) return;
    if (m.method === 'Runtime.exceptionThrown') errors.push(m.params.exceptionDetails.exception?.description || m.params.exceptionDetails.text);
    if (m.method === 'Runtime.consoleAPICalled' && m.params.type === 'error') errors.push(m.params.args.map(a => a.value ?? a.description ?? '').join(' '));
  });
  const once = method => new Promise(ok => listeners.push(m => m.method === method && m.sessionId === sessionId && ok(m)));
  const evaluate = async expr => {
    const r = await page('Runtime.evaluate', { expression: expr, returnByValue: true, awaitPromise: true });
    if (r.exceptionDetails) throw new Error(`page error in ${expr.slice(0, 120)}: ${r.exceptionDetails.exception?.description || r.exceptionDetails.text}`);
    return r.result.value;
  };
  const shot = async (format = 'png', quality) =>
    Buffer.from((await page('Page.captureScreenshot', quality ? { format, quality } : { format })).data, 'base64');
  const close = () => { try { ws.close(); } catch { /* gone */ } chrome.kill('SIGKILL'); };
  return { page, once, evaluate, shot, errors, close };
}

/* Open a page for filming: a URL as it is (a live gh-pages build), or a local page inlined with
 * its data into a temporary file. `params` are added to the query, e.g. 'record&vertical'. */
export async function openPage(target, { data, params = 'record', size = SHAPES.wide } = {}) {
  let url = target, tmp = null;
  if (!isUrl(target)) {
    tmp = join(tmpdir(), `video-page-${process.pid}-${Date.now()}.html`);
    writeFileSync(tmp, inlinePage(target, data).html);
    url = `file://${tmp}`;
  }
  url += (url.includes('?') ? '&' : '?') + params;
  const b = await launch(...size);
  const loaded = b.once('Page.loadEventFired');
  await b.page('Page.navigate', { url });
  await loaded;
  for (let k = 0; k < 300 && !(await b.evaluate(`!!(${API}&&${API}.ready)`)); k++) await new Promise(r => setTimeout(r, 100));
  if (!(await b.evaluate(`!!(${API}&&${API}.ready)`)))
    { b.close(); throw new Error(`${target}: no ready control surface (window.__world) after 30 s\n${b.errors.join('\n')}`); }
  const close = b.close;
  b.close = () => { close(); if (tmp) rmSync(tmp, { force: true }); };
  return b;
}
