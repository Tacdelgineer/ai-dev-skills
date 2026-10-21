// node still.cjs page.html t out.png  -> one clean 1080x1920 frame without captions
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
(async () => { const [file, t, out] = process.argv.slice(2); const b = await chromium.launch(); const p = await b.newPage();
  await p.goto('file://' + path.resolve(file) + '?clean&nocaps'); await p.waitForTimeout(1200);
  const url = await p.evaluate(t => { seek(+t); return document.getElementById('c').toDataURL('image/png'); }, t);
  fs.writeFileSync(out, Buffer.from(url.split(',')[1], 'base64')); await b.close(); console.log(out); })();
