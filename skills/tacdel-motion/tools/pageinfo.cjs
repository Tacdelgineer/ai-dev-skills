// Print a page's window.PROOF as JSON (null when the page has no proof beat): node pageinfo.cjs page.html
const { chromium } = require('playwright'); const path = require('path');
(async () => { const b = await chromium.launch(); const p = await b.newPage();
  await p.goto('file://' + path.resolve(process.argv[2]) + '?t=0'); await p.waitForTimeout(300);
  console.log(JSON.stringify(await p.evaluate(() => window.PROOF || null))); await b.close(); })();
