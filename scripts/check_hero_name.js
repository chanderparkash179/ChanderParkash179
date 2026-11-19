const http = require('http');
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const ROOT = process.cwd();
const server = http.createServer((req, res) => {
  const rel = decodeURIComponent(req.url.split('?')[0]).replace(/^\/+/, '');
  const fp = path.join(ROOT, rel);
  if (!fp.startsWith(ROOT) || !fs.existsSync(fp)) {
    res.writeHead(404);
    res.end();
    return;
  }
  res.writeHead(200, {
    'Content-Type': 'image/svg+xml',
    'Cache-Control': 'no-store',
  });
  fs.createReadStream(fp).pipe(res);
});

server.listen(0, '127.0.0.1', async () => {
  const port = server.address().port;
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.setViewportSize({ width: 1200, height: 600 });
  await page.setContent(
    `<body style="margin:0;background:#123456"><img id="i" src="http://127.0.0.1:${port}/assets/hero.svg" style="width:1100px"/></body>`,
    { waitUntil: 'networkidle' }
  );
  await page.waitForTimeout(2200);
  await page.locator('#i').screenshot({ path: 'preview/frames/hero_name_fix.png' });
  console.log('wrote preview/frames/hero_name_fix.png');
  await browser.close();
  server.close();
});
