'use strict';

const FONT = 'Verdana,DejaVu Sans,sans-serif';

const STYLES = {
  flat: { radius: 4, fontSize: 11, fontWeight: '600', padX: 10, height: 24, uppercase: false, borderWidth: 0 },
  'flat-square': { radius: 0, fontSize: 11, fontWeight: '600', padX: 10, height: 24, uppercase: false, borderWidth: 0 },
  'for-the-badge': { radius: 4, fontSize: 12, fontWeight: '700', padX: 12, height: 28, uppercase: true, borderWidth: 0 },
  plastic: { radius: 4, fontSize: 11, fontWeight: '700', padX: 10, height: 24, uppercase: false, borderWidth: 1 },
  social: { radius: 3, fontSize: 11, fontWeight: '600', padX: 10, height: 24, uppercase: false, borderWidth: 1 },
  rounded: { radius: 12, fontSize: 11, fontWeight: '600', padX: 11, height: 24, uppercase: false, borderWidth: 0 },
  pill: { radius: 999, fontSize: 11, fontWeight: '700', padX: 12, height: 24, uppercase: false, borderWidth: 0 },
  outline: { radius: 6, fontSize: 11, fontWeight: '600', padX: 10, height: 24, uppercase: false, borderWidth: 1 },
  soft: { radius: 8, fontSize: 11, fontWeight: '600', padX: 11, height: 24, uppercase: false, borderWidth: 0 },
};

const THEMES = {
  dark: { labelBg: '#1f2937', labelText: '#f3f4f6', valueBg: '#111827', valueText: '#93c5fd', border: '#374151' },
  light: { labelBg: '#f3f4f6', labelText: '#111827', valueBg: '#ffffff', valueText: '#1d4ed8', border: '#d1d5db' },
  neon: { labelBg: '#151026', labelText: '#67e8f9', valueBg: '#1e1237', valueText: '#c4b5fd', border: '#7c3aed' },
  sunset: { labelBg: '#7c2d12', labelText: '#ffedd5', valueBg: '#9a3412', valueText: '#fde68a', border: '#fdba74' },
  terminal: { labelBg: '#052e16', labelText: '#dcfce7', valueBg: '#14532d', valueText: '#86efac', border: '#22c55e' },
};

const SIZES = { xs: 0.82, sm: 0.92, md: 1.0, lg: 1.16, xl: 1.32 };

const ICONS = {
  none: '', star: '★', heart: '❤', check: '✓', fire: '🔥',
  bolt: '⚡', rocket: '🚀', code: '⌘', build: '⚙', docs: '📘',
};

const DATA_URI_RE = /^data:image\/[a-zA-Z0-9+\-]+;base64,[A-Za-z0-9+/=]+$/;
const MAX_ICON_DATA_LEN = 200000;

function esc(s) {
  return String(s)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

function clamp(v, lo, hi) {
  return Math.min(Math.max(v, lo), hi);
}

function isHex(s) {
  return typeof s === 'string' && /^#[0-9a-fA-F]{6}$/.test(s.trim());
}

function textWidth(text, fontSize) {
  const multiplier = fontSize >= 12 ? 0.62 : 0.58;
  return Math.floor(Math.max(1, text.length) * fontSize * multiplier);
}

function validateIconData(dataUri) {
  if (!dataUri || typeof dataUri !== 'string') return null;
  if (dataUri.length > MAX_ICON_DATA_LEN) return null;
  if (!DATA_URI_RE.test(dataUri)) return null;
  return dataUri;
}

function parseBool(v) {
  if (v === true || v === 'true' || v === '1' || v === 1) return true;
  return false;
}

function generateBadge(opts = {}) {
  const {
    label = 'build',
    value = 'passing',
    icon = 'none',
    iconData = '',
    style = 'flat',
    theme = 'dark',
    size = 'md',
    scale = 1.0,
    labelBg = '',
    valueBg = '',
    labelColor = '',
    valueColor = '',
    borderColor = '',
    borderRadius = null,
    gradient = false,
    uppercase = false,
    compact = false,
  } = opts;

  const profile = STYLES[style] || STYLES.flat;
  const palette = THEMES[theme] || THEMES.dark;

  const activeUppercase = profile.uppercase || uppercase;
  const rawLabel = String(label || 'label').slice(0, 40);
  const rawValue = String(value || 'value').slice(0, 52);

  const validatedIconData = validateIconData(iconData);
  const hasCustomIcon = !!validatedIconData;
  const symbol = hasCustomIcon ? '' : (ICONS[icon] || '');
  const fullLabelText = symbol ? `${symbol} ${rawLabel}`.trim() : rawLabel;

  const lbg = isHex(labelBg) ? labelBg.trim() : palette.labelBg;
  const vbg = isHex(valueBg) ? valueBg.trim() : palette.valueBg;
  const ltxt = isHex(labelColor) ? labelColor.trim() : palette.labelText;
  const vtxt = isHex(valueColor) ? valueColor.trim() : palette.valueText;
  const bdr = isHex(borderColor) ? borderColor.trim() : palette.border;

  const sizeFactor = SIZES[size] || 1.0;
  const scaleFactor = clamp(parseFloat(String(scale)) || 1.0, 0.7, 2.0);
  const compactFactor = compact ? 0.88 : 1.0;
  const factor = sizeFactor * scaleFactor * compactFactor;

  const baseRadius = borderRadius !== null
    ? clamp(parseInt(String(borderRadius), 10) || 0, 0, 999)
    : profile.radius;

  const height = Math.max(16, Math.round(profile.height * factor));
  const padX = Math.max(5, Math.round(profile.padX * factor));
  const fontSize = Math.max(9, Math.round(profile.fontSize * factor));
  const radius = Math.min(Math.round(baseRadius * factor), Math.floor(height / 2));

  const iconSize = hasCustomIcon ? Math.round(height * 0.65) : 0;
  const iconPad = hasCustomIcon ? Math.round(iconSize * 0.4) : 0;
  const iconTotalSpace = hasCustomIcon ? iconSize + iconPad : 0;

  const labelRender = activeUppercase ? fullLabelText.toUpperCase() : fullLabelText;
  const valueRender = activeUppercase ? rawValue.toUpperCase() : rawValue;

  const leftWidth = textWidth(labelRender, fontSize) + 2 * padX + iconTotalSpace;
  const rightWidth = textWidth(valueRender, fontSize) + 2 * padX;
  const totalWidth = leftWidth + rightWidth;

  const isOutline = style === 'outline';
  const leftFill = isOutline ? 'none' : lbg;
  const rightFill = isOutline ? 'none' : vbg;
  const borderAttr = profile.borderWidth > 0
    ? ` stroke="${esc(bdr)}" stroke-width="${profile.borderWidth}"`
    : '';

  let defs = '';
  let overlay = '';
  if (gradient) {
    defs = `<defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="#ffffff" stop-opacity="0.42"/>
<stop offset="0.49" stop-color="#ffffff" stop-opacity="0.10"/>
<stop offset="0.5" stop-color="#000000" stop-opacity="0.10"/>
<stop offset="1" stop-color="#000000" stop-opacity="0.18"/>
</linearGradient></defs>`;
    overlay = `<rect x="0" y="0" width="${totalWidth}" height="${height}" fill="url(#g)" rx="${radius}" ry="${radius}"/>`;
  }

  const textY = (height / 2) + (fontSize * 0.33);

  let iconSvg = '';
  let labelTextX = leftWidth / 2;
  if (hasCustomIcon) {
    const ix = padX;
    const iy = (height - iconSize) / 2;
    iconSvg = `<image x="${ix}" y="${iy}" width="${iconSize}" height="${iconSize}" href="${esc(validatedIconData)}"/>`;
    labelTextX = iconTotalSpace + padX + textWidth(labelRender, fontSize) / 2;
  }

  const junctionX = Math.max(0, leftWidth - radius);
  const junctionFill = isOutline ? 'none' : lbg;

  return `<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="${totalWidth}" height="${height}" role="img" aria-label="${esc(labelRender)}: ${esc(valueRender)}">
<title>${esc(labelRender)}: ${esc(valueRender)}</title>
${defs}
<rect x="0" y="0" width="${leftWidth}" height="${height}" fill="${esc(leftFill)}" rx="${radius}" ry="${radius}"${borderAttr}/>
<rect x="${leftWidth}" y="0" width="${rightWidth}" height="${height}" fill="${esc(rightFill)}" rx="${radius}" ry="${radius}"${borderAttr}/>
<rect x="${junctionX}" y="0" width="${radius}" height="${height}" fill="${esc(junctionFill)}"/>
${iconSvg}
<text x="${labelTextX}" y="${textY.toFixed(1)}" fill="${esc(ltxt)}" font-size="${fontSize}" font-family="${FONT}" font-weight="${profile.fontWeight}" text-anchor="middle">${esc(labelRender)}</text>
<text x="${leftWidth + rightWidth / 2}" y="${textY.toFixed(1)}" fill="${esc(vtxt)}" font-size="${fontSize}" font-family="${FONT}" font-weight="${profile.fontWeight}" text-anchor="middle">${esc(valueRender)}</text>
${overlay}
</svg>`.trim();
}

const MAX_ICON_FETCH_BYTES = 200000;
const ICON_FETCH_TIMEOUT_MS = 3000;

async function fetchIconAsDataUri(url) {
  const parsed = new URL(url);
  if (parsed.protocol !== 'https:') return null;

  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), ICON_FETCH_TIMEOUT_MS);

  try {
    const resp = await fetch(url, {
      signal: controller.signal,
      headers: {
        'User-Agent': 'Mozilla/5.0 (compatible; CustomBadgeGenerator/1.0)',
        'Accept': 'image/*, */*',
      },
      redirect: 'follow',
    });
    clearTimeout(timer);

    if (!resp.ok) return null;

    let contentType = (resp.headers.get('content-type') || '').split(';')[0].trim().toLowerCase();
    const path = url.toLowerCase().split('?')[0];

    if (!contentType || contentType === 'text/plain' || contentType === 'application/octet-stream') {
      if (path.endsWith('.svg')) contentType = 'image/svg+xml';
      else if (path.endsWith('.png')) contentType = 'image/png';
      else if (path.endsWith('.jpg') || path.endsWith('.jpeg')) contentType = 'image/jpeg';
      else if (path.endsWith('.gif')) contentType = 'image/gif';
      else if (path.endsWith('.webp')) contentType = 'image/webp';
    }

    if (!contentType.startsWith('image/')) return null;

    const buf = await resp.arrayBuffer();
    if (buf.byteLength > MAX_ICON_FETCH_BYTES) return null;

    const base64 = Buffer.from(buf).toString('base64');
    return `data:${contentType};base64,${base64}`;
  } catch {
    clearTimeout(timer);
    return null;
  }
}

module.exports = async function handler(req, res) {
  try {
    const q = req.query || {};

    // Resolve icon data: prefer iconUrl (server-side fetch), fall back to iconData (legacy)
    let resolvedIconData;
    if (typeof q.iconUrl === 'string' && q.iconUrl.length > 0) {
      resolvedIconData = await fetchIconAsDataUri(q.iconUrl);
    } else if (typeof q.iconData === 'string' && q.iconData.length > 0) {
      // Fix URL decoding: query params turn '+' into ' ', restore before validation
      resolvedIconData = q.iconData.replace(/ /g, '+');
    }

    const params = {
      label: typeof q.label === 'string' ? q.label : undefined,
      value: typeof q.value === 'string' ? q.value : undefined,
      icon: typeof q.icon === 'string' ? q.icon : undefined,
      iconData: resolvedIconData || '',
      style: typeof q.style === 'string' ? q.style : undefined,
      theme: typeof q.theme === 'string' ? q.theme : undefined,
      size: typeof q.size === 'string' ? q.size : undefined,
      scale: q.scale !== undefined ? parseFloat(String(q.scale)) : undefined,
      labelBg: typeof q.labelBg === 'string' ? q.labelBg : undefined,
      valueBg: typeof q.valueBg === 'string' ? q.valueBg : undefined,
      labelColor: typeof q.labelColor === 'string' ? q.labelColor : undefined,
      valueColor: typeof q.valueColor === 'string' ? q.valueColor : undefined,
      borderColor: typeof q.borderColor === 'string' ? q.borderColor : undefined,
      borderRadius: q.borderRadius !== undefined ? parseInt(String(q.borderRadius), 10) : null,
      gradient: parseBool(q.gradient),
      uppercase: parseBool(q.uppercase),
      compact: parseBool(q.compact),
    };

    const svg = generateBadge(params);
    res.setHeader('Content-Type', 'image/svg+xml; charset=utf-8');
    res.setHeader('Cache-Control', 'public, max-age=300, s-maxage=300, stale-while-revalidate=86400');
    res.status(200).send(svg);
  } catch {
    const errorSvg = generateBadge({ label: 'error', value: 'badge generation failed', style: 'flat', theme: 'dark' });
    res.setHeader('Content-Type', 'image/svg+xml; charset=utf-8');
    res.setHeader('Cache-Control', 'no-store');
    res.status(500).send(errorSvg);
  }
};
