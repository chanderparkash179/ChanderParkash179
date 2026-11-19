const fs = require('fs');
const si = require('simple-icons');

function pathFromSvg(file) {
  const svg = fs.readFileSync(file, 'utf8');
  const m = svg.match(/path d="([^"]+)/);
  if (!m) throw new Error('No path in ' + file);
  return m[1];
}

function bySlug(slug) {
  const ic = Object.values(si).find((i) => i && i.slug === slug);
  if (!ic) return null;
  return {
    title: ic.title,
    hex: ic.hex,
    path: ic.path,
    source: 'Simple Icons (CC0)',
  };
}

function requireSlug(slug) {
  const ic = bySlug(slug);
  if (!ic) throw new Error('Missing ' + slug);
  return ic;
}

const extra = {
  linkedin: {
    title: 'LinkedIn',
    hex: '0A66C2',
    path: pathFromSvg('assets/icons/linkedin.svg'),
    source: 'Simple Icons 9.19.0 (CC0) via jsDelivr',
  },
  amazonaws: {
    title: 'AWS',
    hex: 'FF9900',
    path: pathFromSvg('assets/icons/amazonaws-si.svg'),
    source: 'Simple Icons 9.19.0 (CC0) via jsDelivr',
  },
  microsoftazure: {
    title: 'Azure',
    hex: '0078D4',
    path: pathFromSvg('assets/icons/microsoftazure-si.svg'),
    source: 'Simple Icons 9.19.0 (CC0) via jsDelivr',
  },
  // Simple globe mark for Portfolio (original geometric path for this README)
  portfolio: {
    title: 'Portfolio',
    hex: '247BFF',
    path: 'M12 0C5.373 0 0 5.373 0 12s5.373 12 12 12 12-5.373 12-12S18.627 0 12 0zm8.94 11h-3.094a15.9 15.9 0 0 0-1.2-5.12A9.03 9.03 0 0 1 20.94 11zM12 2c.9 0 2.3 1.9 3.12 5H8.88C9.7 3.9 11.1 2 12 2zM2.06 13h3.094c.2 1.83.62 3.55 1.2 5.12A9.03 9.03 0 0 1 2.06 13zm3.094-2H2.06a9.03 9.03 0 0 1 4.294-5.12A15.9 15.9 0 0 0 5.154 11zM8.88 13h6.24c-.83 3.1-2.22 5-3.12 5s-2.3-1.9-3.12-5zm6.24-2H8.88c.83-3.1 2.22-5 3.12-5s2.3 1.9 3.12 5zm.672 7.12c.58-1.57 1-3.29 1.2-5.12h3.094a9.03 9.03 0 0 1-4.294 5.12z',
    source: 'Original geometric globe mark for Portfolio link',
  },
};

const slugs = [
  'springboot',
  'nestjs',
  'angular',
  'docker',
  'kubernetes',
  'facebook',
  'instagram',
  'github',
  'gmail',
  'stackoverflow',
  'git',
  'openjdk',
  'javascript',
  'typescript',
  'nodedotjs',
  'go',
  'postgresql',
  'mysql',
  'html5',
  'css',
];

const out = { ...extra };
for (const slug of slugs) {
  out[slug] = requireSlug(slug);
}

// IBM DB2 — brand mark not in current Simple Icons
out.ibm = {
  title: 'IBM DB2',
  hex: '054ADA',
  path: 'M0 8.5h24v2H0v-2zm0 5h24v2H0v-2zM3 3h4.5v18H3V3zm13.5 0H21v18h-4.5V3z',
  source: 'Simplified geometric mark for IBM DB2 (official SI mark unavailable)',
};

out.java = {
  ...out.openjdk,
  title: 'Java',
  source:
    'Simple Icons OpenJDK (CC0) — Oracle Java mark unavailable in current Simple Icons; OpenJDK used',
};

// Aliases used by profile config
out.nodejs = { ...out.nodedotjs, title: 'NodeJS' };
out.css3 = { ...out.css, title: 'CSS3' };

// Oracle / MSSQL may be absent — try common slugs, else geometric fallbacks
for (const [key, tries, title, hex] of [
  ['oracle', ['oracle'], 'Oracle DB', 'F80000'],
  ['mssql', ['microsoftsqlserver'], 'MSSQL', 'CC2927'],
]) {
  let found = null;
  for (const t of tries) {
    found = bySlug(t);
    if (found) break;
  }
  if (found) {
    out[key] = { ...found, title };
  } else {
    out[key] = {
      title,
      hex,
      path: 'M4 4h16v4H4V4zm0 6h16v4H4v-4zm0 6h16v4H4v-4z',
      source: 'Simplified mark fallback (brand unavailable in Simple Icons)',
    };
  }
}

fs.writeFileSync('assets/icons/icons.json', JSON.stringify(out, null, 2));
console.log('icons:', Object.keys(out).join(', '));
