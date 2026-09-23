#!/usr/bin/env node
/* build_single.mjs - the live page: one self-contained HTML file with the drawing core, director
 * mode and every number baked in. Opens by double-click and serves as-is from GitHub Pages.
 *
 *   node scripts/video/build_single.mjs --page visuals/world/index.html --data visuals/world/data.json \
 *        [--out visuals/dist/index.html] [--title "Project name"]
 *
 * Every local <script src> the page loads is inlined, and the data file becomes window.__RUN__,
 * so the page never fetches anything. No server, no network, no packages. Publishing to gh-pages
 * is a separate, deliberate step (references/visuals.md), done only when the prompt allows it. */
import { writeFileSync, mkdirSync, statSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { arg, inlinePage } from './pagekit.mjs';

const page = arg('page'), data = arg('data');
if (!page || !data) { console.error('usage: build_single.mjs --page <html> --data <json> [--out visuals/dist/index.html]'); process.exit(2); }
const out = resolve(arg('out', 'visuals/dist/index.html'));
let { html, data: run } = inlinePage(page, data);
if (!Number.isInteger(run.contract_version)) throw new Error(`${data} has no integer contract_version`);
const title = arg('title');
if (title) html = html.replace(/<title>[^<]*<\/title>/, `<title>${title.replace(/</g, '&lt;')}${run.fake ? ' (fake data)' : ''}</title>`);
mkdirSync(dirname(out), { recursive: true });
writeFileSync(out, html);
console.log(`${out}: ${(statSync(out).size / 1024).toFixed(0)} KB, data contract v${run.contract_version}` +
  `${run.run_id ? ', run ' + run.run_id : ''}${run.fake ? ', FAKE DATA' : ''}. Opens by double-click.`);
