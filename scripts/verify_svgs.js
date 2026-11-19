/**
 * Serve assets over localhost, screenshot each SVG as <img> at 0/2/5/9/13s,
 * mobile width, and animation-stripped. Assert zero external requests.
 */
const fs = require('fs');
const http = require('http');
const path = require('path');
const { chromium } = require('playwright');

const ROOT = path.resolve(__dirname, '..');
const OUT = path.join(ROOT, 'preview', 'frames');
const SVGS = [
  'hero.svg',
  'about-life.svg',
  'stack.svg',
  'id-dashboard.svg',
  'connect.svg',
];
const TIMES = [0, 2, 5, 9, 13];

function ensureDir(d) {
  fs.mkdirSync(d, { recursive: true });
}

function stripAnimations(svg) {
  return svg
    .replace(
      /<style><!\[CDATA\[[\s\S]*?\]\]><\/style>/g,
      '<style><![CDATA[ * { animation: none !important; transition: none !important; } ]]></style>'
    )
    .replace(/<animateTransform[\s\S]*?\/>/g, '')
    .replace(/<animate[\s\S]*?\/>/g, '')
    .replace(/<animateTransform[\s\S]*?<\/animateTransform>/g, '')
    .replace(/<animate[\s\S]*?<\/animate>/g, '');
}

function contentType(filePath) {
  if (filePath.endsWith('.svg')) return 'image/svg+xml; charset=utf-8';
  if (filePath.endsWith('.png')) return 'image/png';
  if (filePath.endsWith('.html')) return 'text/html; charset=utf-8';
  return 'application/octet-stream';
}

function startServer() {
  return new Promise((resolve) => {
    const server = http.createServer((req, res) => {
      const urlPath = decodeURIComponent((req.url || '/').split('?')[0]);
      let rel = urlPath.replace(/^\/+/, '');
      if (!rel || rel === '') rel = 'preview.html';
      const filePath = path.join(ROOT, rel);
      if (!filePath.startsWith(ROOT) || !fs.existsSync(filePath) || fs.statSync(filePath).isDirectory()) {
        res.writeHead(404);
        res.end('not found');
        return;
      }
      res.writeHead(200, {
        'Content-Type': contentType(filePath),
        'Cache-Control': 'no-store',
      });
      fs.createReadStream(filePath).pipe(res);
    });
    server.listen(0, '127.0.0.1', () => {
      const { port } = server.address();
      resolve({ server, port });
    });
  });
}

async function main() {
  ensureDir(OUT);
  // Prepare no-animation variants
  for (const file of SVGS) {
    const svg = fs.readFileSync(path.join(ROOT, 'assets', file), 'utf8');
    fs.writeFileSync(path.join(OUT, `${file.replace('.svg', '')}_noanim.svg`), stripAnimations(svg));
  }

  const { server, port } = await startServer();
  const base = `http://127.0.0.1:${port}`;
  const browser = await chromium.launch();
  const report = { externalHits: [], frames: [], issues: [], sizes: {} };

  try {
    for (const file of SVGS) {
      const svgPath = path.join(ROOT, 'assets', file);
      const svg = fs.readFileSync(svgPath, 'utf8');
      report.sizes[file] = fs.statSync(svgPath).size;
      const imgUrl = `${base}/assets/${file}`;

      const page = await browser.newPage();
      const external = [];
      page.on('request', (req) => {
        const u = req.url();
        if (u.startsWith(base) || u.startsWith('data:') || u.startsWith('about:')) return;
        external.push(u);
      });

      await page.setViewportSize({ width: 1200, height: 900 });
      await page.setContent(
        `<!doctype html><html><body style="margin:0;background:#123456;">
          <img id="i" src="${imgUrl}" style="width:1100px;height:auto;display:block"/>
        </body></html>`,
        { waitUntil: 'networkidle' }
      );
      await page.waitForTimeout(300);

      let elapsed = 0;
      for (const t of TIMES) {
        const wait = Math.max(0, t * 1000 - elapsed);
        if (wait) await page.waitForTimeout(wait);
        elapsed = t * 1000;
        const box = await page.locator('#i').boundingBox();
        if (!box || box.height < 40) {
          report.issues.push(`${file}: img height too small at t=${t}s (${box && box.height})`);
        }
        const out = path.join(OUT, `${file.replace('.svg', '')}_t${t}s_w1100.png`);
        await page.locator('#i').screenshot({ path: out });
        report.frames.push(out);
      }
      if (external.length) report.externalHits.push({ file, urls: [...new Set(external)] });
      await page.close();

      const page2 = await browser.newPage();
      await page2.setViewportSize({ width: 390, height: 900 });
      await page2.setContent(
        `<!doctype html><html><body style="margin:0;background:#123456;">
          <img id="i" src="${imgUrl}" style="width:100%;height:auto;display:block"/>
        </body></html>`,
        { waitUntil: 'networkidle' }
      );
      await page2.waitForTimeout(5000);
      const mobileOut = path.join(OUT, `${file.replace('.svg', '')}_t5s_w390.png`);
      await page2.locator('#i').screenshot({ path: mobileOut });
      report.frames.push(mobileOut);

      const noanimUrl = `${base}/preview/frames/${file.replace('.svg', '')}_noanim.svg`;
      await page2.setViewportSize({ width: 1200, height: 900 });
      await page2.setContent(
        `<!doctype html><html><body style="margin:0;background:#123456;">
          <img id="i" src="${noanimUrl}" style="width:1100px;height:auto;display:block"/>
        </body></html>`,
        { waitUntil: 'networkidle' }
      );
      await page2.waitForTimeout(250);
      const noanimOut = path.join(OUT, `${file.replace('.svg', '')}_noanim_w1100.png`);
      await page2.locator('#i').screenshot({ path: noanimOut });
      report.frames.push(noanimOut);
      await page2.close();

      if (/foreignObject/i.test(svg)) report.issues.push(`${file}: foreignObject`);
      if (/<script/i.test(svg)) report.issues.push(`${file}: script`);
      if (!/prefers-reduced-motion/.test(svg)) report.issues.push(`${file}: missing reduced motion`);
      const bad = [...svg.matchAll(/https?:\/\/[^"'>\s]+/g)]
        .map((m) => m[0])
        .filter((u) => !u.includes('www.w3.org'));
      if (bad.length) report.issues.push(`${file}: external URLs ${bad.join(', ')}`);
    }

    const readme = fs.readFileSync(path.join(ROOT, 'README.md'), 'utf8');
    report.readmeLinks = [...readme.matchAll(/\[([^\]]+)\]\(([^)]+)\)/g)].map((m) => m[2]);
    for (const u of report.readmeLinks) {
      if (!u.startsWith('mailto:') && !/^https?:\/\//.test(u)) {
        report.issues.push(`Non-http link: ${u}`);
      }
    }
    for (const f of SVGS) {
      if (!readme.includes(`assets/${f}?v=1`)) report.issues.push(`README missing assets/${f}?v=1`);
    }
  } finally {
    await browser.close();
    server.close();
  }

  fs.writeFileSync(path.join(OUT, 'report.json'), JSON.stringify(report, null, 2));
  console.log(
    JSON.stringify(
      {
        frames: report.frames.length,
        sizes: report.sizes,
        externalHits: report.externalHits,
        issues: report.issues,
        links: report.readmeLinks,
      },
      null,
      2
    )
  );
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
