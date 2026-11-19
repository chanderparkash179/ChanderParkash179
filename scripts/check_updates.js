const http = require('http');
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const ROOT = process.cwd();
const files = [
  ['id-dashboard.svg', 6],
  ['connect.svg', 2],
  ['stack.svg', 3],
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
    'Content-Type': 'image/svg+xml',
    'Cache-Control': 'no-store',
  });
  fs.createReadStream(fp).pipe(res);
});

server.listen(0, '127.0.0.1', async () => {
  const port = server.address().port;
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.setViewportSize({ width: 1200, height: 900 });
  for (const [file, t] of files) {
    await page.setContent(
      `<body style="margin:0;background:#123456"><img id="i" src="http://127.0.0.1:${port}/assets/${file}" style="width:1100px"/></body>`,
      { waitUntil: 'networkidle' }
    );
    await page.waitForTimeout(t * 1000 + 200);
    const out = `preview/frames/update_${file.replace('.svg', '')}.png`;
    await page.locator('#i').screenshot({ path: out });
    console.log('wrote', out);
  }
  await browser.close();
  server.close();
});
