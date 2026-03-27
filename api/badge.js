'use strict';

const TWO_PI = Math.PI * 2;
const MAX_LABEL_LEN = 40;
const PROFILES = new Set(['donut', 'solid-cube', 'hollow-cube', 'triangle']);
const THEMES = {
  dark: { bg: '#0b1020', fg: '#9ad1ff', accent: '#d8ecff' },
  light: { bg: '#f8fafc', fg: '#1e3a8a', accent: '#0f172a' },
  neon: { bg: '#0a0f1f', fg: '#67e8f9', accent: '#c084fc' },
};

function clamp(value, min, max) {
  return Math.max(min, Math.min(max, value));
}

function esc(value) {
  return String(value)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

function rotX(p, a) {
  const c = Math.cos(a);
  const s = Math.sin(a);
  return { x: p.x, y: p.y * c - p.z * s, z: p.y * s + p.z * c };
}

function rotY(p, a) {
  const c = Math.cos(a);
  const s = Math.sin(a);
  return { x: p.x * c + p.z * s, y: p.y, z: -p.x * s + p.z * c };
}

function rotZ(p, a) {
  const c = Math.cos(a);
  const s = Math.sin(a);
  return { x: p.x * c - p.y * s, y: p.x * s + p.y * c, z: p.z };
}

function makeDonutPoints() {
  const pts = [];
  for (let i = 0; i < 48; i += 1) {
    const u = (i / 48) * TWO_PI;
    for (let j = 0; j < 24; j += 1) {
      const v = (j / 24) * TWO_PI;
      const r = 1.4 + 0.55 * Math.cos(v);
      pts.push({
        x: r * Math.cos(u),
        y: r * Math.sin(u),
        z: 0.55 * Math.sin(v),
      });
    }
  }
  return pts;
}

function makeSolidCubePoints() {
  const pts = [];
  for (let x = -1; x <= 1; x += 0.2) {
    for (let y = -1; y <= 1; y += 0.2) {
      for (let z = -1; z <= 1; z += 0.2) {
        pts.push({ x, y, z });
      }
    }
  }
  return pts;
}

function makeHollowCubePoints() {
  const pts = [];
  for (let x = -1; x <= 1; x += 0.2) {
    for (let y = -1; y <= 1; y += 0.2) {
      for (let z = -1; z <= 1; z += 0.2) {
        const edgeCount = [Math.abs(x), Math.abs(y), Math.abs(z)].filter(v => v > 0.8).length;
        if (edgeCount >= 2) pts.push({ x, y, z });
      }
    }
  }
  return pts;
}

function makeTrianglePoints() {
  const pts = [];
  const vertices = [
    { x: 0, y: 1.2, z: 0 },
    { x: -1.2, y: -1, z: 0.2 },
    { x: 1.2, y: -1, z: 0.2 },
    { x: 0, y: -0.1, z: -1.2 },
  ];
  const edges = [
    [0, 1], [1, 2], [2, 0],
    [0, 3], [1, 3], [2, 3],
  ];
  for (const [a, b] of edges) {
    for (let t = 0; t <= 1; t += 0.03) {
      pts.push({
        x: vertices[a].x + (vertices[b].x - vertices[a].x) * t,
        y: vertices[a].y + (vertices[b].y - vertices[a].y) * t,
        z: vertices[a].z + (vertices[b].z - vertices[a].z) * t,
      });
    }
  }
  return pts;
}

function getPointCloud(profile) {
  if (profile === 'solid-cube') return makeSolidCubePoints();
  if (profile === 'hollow-cube') return makeHollowCubePoints();
  if (profile === 'triangle') return makeTrianglePoints();
  return makeDonutPoints();
}

function renderAsciiFrame(points, angle, cols = 42, rows = 18) {
  const depth = Array.from({ length: rows }, () => Array(cols).fill(-Infinity));
  const buf = Array.from({ length: rows }, () => Array(cols).fill(' '));
  const chars = ' .,-~:;=!*#$@';

  for (const p of points) {
    let q = rotY(rotX(rotZ(p, angle * 0.35), angle * 0.8), angle * 0.55);
    q = { x: q.x * 1.1, y: q.y, z: q.z };

    const invZ = 1 / (q.z + 4);
    const px = Math.floor(cols / 2 + q.x * 11 * invZ);
    const py = Math.floor(rows / 2 - q.y * 11 * invZ * 0.6);

    if (px < 0 || px >= cols || py < 0 || py >= rows) continue;

    const lum = clamp((q.z + 2) / 4, 0, 1);
    const ch = chars[Math.floor(lum * (chars.length - 1))];
    if (invZ > depth[py][px]) {
      depth[py][px] = invZ;
      buf[py][px] = ch;
    }
  }

  return buf.map(row => row.join('').replace(/\s+$/g, '')).join('\n');
}

function buildAnimatedSvg({ label, profile, theme }) {
  const frameCount = 20;
  const points = getPointCloud(profile);
  const palette = THEMES[theme] || THEMES.dark;
  const frames = [];

  for (let i = 0; i < frameCount; i += 1) {
    frames.push(renderAsciiFrame(points, (i / frameCount) * TWO_PI));
  }

  const preHeight = 18 * 13.4;
  const width = 460;
  const height = 320;

  const frameGroups = frames
    .map((frame, i) => `<text class="f f${i}" x="18" y="62">${esc(frame)}</text>`)
    .join('');

  const keyframes = Array.from({ length: frameCount }, (_, i) => {
    const start = (i / frameCount) * 100;
    const end = ((i + 1) / frameCount) * 100;
    return `.f${i}{animation:show${i} 3s steps(1,end) infinite}@keyframes show${i}{0%,${start.toFixed(4)}%{opacity:0}${start.toFixed(4)}%,${end.toFixed(4)}%{opacity:1}${end.toFixed(4)}%,100%{opacity:0}}`;
  }).join('');

  return `<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${height}" viewBox="0 0 ${width} ${height}" role="img" aria-label="${esc(label)} ${esc(profile)} animated ascii badge">
  <defs>
    <style>
      .bg{fill:${palette.bg}}
      .label{font:600 20px ui-sans-serif,system-ui,sans-serif;fill:${palette.accent}}
      .sub{font:500 12px ui-sans-serif,system-ui,sans-serif;fill:${palette.fg};opacity:.88}
      .f{font:12px ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;fill:${palette.fg};white-space:pre;dominant-baseline:hanging;opacity:0}
      ${keyframes}
    </style>
  </defs>
  <rect class="bg" x="0" y="0" width="${width}" height="${height}" rx="14"/>
  <text class="label" x="18" y="30">${esc(label)}</text>
  <text class="sub" x="18" y="48">${esc(profile)} • generated by API</text>
  <rect x="14" y="56" width="432" height="${preHeight + 8}" rx="8" fill="rgba(255,255,255,0.04)"/>
  ${frameGroups}
</svg>`;
}

module.exports = function handler(req, res) {
  const profileRaw = String(req.query.profile || 'donut').trim().toLowerCase();
  const profile = PROFILES.has(profileRaw) ? profileRaw : 'donut';
  const label = String(req.query.label || 'Animated ASCII').trim().slice(0, MAX_LABEL_LEN) || 'Animated ASCII';
  const themeRaw = String(req.query.theme || 'dark').trim().toLowerCase();
  const theme = THEMES[themeRaw] ? themeRaw : 'dark';

  const svg = buildAnimatedSvg({ label, profile, theme });

  res.setHeader('Content-Type', 'image/svg+xml; charset=utf-8');
  res.setHeader('Cache-Control', 'public, s-maxage=3600, max-age=0, stale-while-revalidate=86400');
  res.status(200).send(svg);
};
