const http = require('http');
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const ROOT = process.cwd();
const shots = [
  ['about-life.svg', 5],
  ['stack.svg', 5],
  ['hero.svg', 0],
  ['hero.svg', 2],
  ['id-dashboard.svg', 0],
  ['id-dashboard.svg', 6],
  ['connect.svg', 2],
];

const server = http.createServer((req, res) => {
  const rel = decodeURIComponent(req.url.split('?')[0]).replace(/^\/+/, '');
  const fp = path.join(ROOT, rel);
  if (!fp.startsWith(ROOT) || !fs.existsSync(fp)) {
    res.writeHead(404);
    res.end();
    return;
  }
  res.writeHead(200, {
    'Content-Type': fp.endsWith('.svg') ? 'image/svg+xml' : 'text/html',
    'Cache-Control': 'no-store',
  });
  fs.createReadStream(fp).pipe(res);
});

server.listen(0, '127.0.0.1', async () => {
  const port = server.address().port;
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.setViewportSize({ width: 1200, height: 900 });
  for (const [file, t] of shots) {
    await page.setContent(
      `<body style="margin:0;background:#123456"><img id="i" src="http://127.0.0.1:${port}/assets/${file}" style="width:1100px"/></body>`,
      { waitUntil: 'networkidle' }
    );
    await page.waitForTimeout(t * 1000 + 250);
    const out = `preview/frames/check_${file.replace('.svg', '')}_t${t}.png`;
    await page.locator('#i').screenshot({ path: out });
    console.log('wrote', out);
  }
  await browser.close();
  server.close();
});
