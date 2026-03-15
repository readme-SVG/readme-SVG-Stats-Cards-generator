/**
 * Badge Forge — app.js
 * Client-side SVG badge generator. Zero backend required.
 * Faithfully ports the Python/Flask badge rendering engine to pure JS.
 *
 * Architecture:
 *   CONSTANTS  → badge styles, themes, sizes, icons, presets, palette
 *   ENGINE     → SVG generation (textWidth, generateBadge)
 *   STATE      → reactive badge parameters object
 *   UI         → DOM wiring, gallery, color sync, icon picker, toast
 */

'use strict';

/* ═══════════════════════════════════════════════════════════════
   CONSTANTS — mirror the Python backend exactly
   ═══════════════════════════════════════════════════════════════ */

const FONT = 'Verdana,DejaVu Sans,sans-serif';

/** @type {Record<string, {radius:number, fontSize:number, fontWeight:string, padX:number, height:number, uppercase:boolean, borderWidth:number}>} */
const STYLES = {
  'flat':          { radius: 4,   fontSize: 11, fontWeight: '600', padX: 10, height: 24, uppercase: false, borderWidth: 0 },
  'flat-square':   { radius: 0,   fontSize: 11, fontWeight: '600', padX: 10, height: 24, uppercase: false, borderWidth: 0 },
  'for-the-badge': { radius: 4,   fontSize: 12, fontWeight: '700', padX: 12, height: 28, uppercase: true,  borderWidth: 0 },
  'plastic':       { radius: 4,   fontSize: 11, fontWeight: '700', padX: 10, height: 24, uppercase: false, borderWidth: 1 },
  'social':        { radius: 3,   fontSize: 11, fontWeight: '600', padX: 10, height: 24, uppercase: false, borderWidth: 1 },
  'rounded':       { radius: 12,  fontSize: 11, fontWeight: '600', padX: 11, height: 24, uppercase: false, borderWidth: 0 },
  'pill':          { radius: 999, fontSize: 11, fontWeight: '700', padX: 12, height: 24, uppercase: false, borderWidth: 0 },
  'outline':       { radius: 6,   fontSize: 11, fontWeight: '600', padX: 10, height: 24, uppercase: false, borderWidth: 1 },
  'soft':          { radius: 8,   fontSize: 11, fontWeight: '600', padX: 11, height: 24, uppercase: false, borderWidth: 0 },
};

const STYLE_ORDER = ['flat','flat-square','for-the-badge','plastic','social','rounded','pill','outline','soft'];

/** @type {Record<string, {labelBg:string, labelText:string, valueBg:string, valueText:string, border:string}>} */
const THEMES = {
  'dark':     { labelBg: '#1f2937', labelText: '#f3f4f6', valueBg: '#111827', valueText: '#93c5fd', border: '#374151' },
  'light':    { labelBg: '#f3f4f6', labelText: '#111827', valueBg: '#ffffff', valueText: '#1d4ed8', border: '#d1d5db' },
  'neon':     { labelBg: '#151026', labelText: '#67e8f9', valueBg: '#1e1237', valueText: '#c4b5fd', border: '#7c3aed' },
  'sunset':   { labelBg: '#7c2d12', labelText: '#ffedd5', valueBg: '#9a3412', valueText: '#fde68a', border: '#fdba74' },
  'terminal': { labelBg: '#052e16', labelText: '#dcfce7', valueBg: '#14532d', valueText: '#86efac', border: '#22c55e' },
};

const THEME_ORDER = ['dark','light','neon','sunset','terminal'];

/** @type {Record<string, number>} */
const SIZES = { xs: 0.82, sm: 0.92, md: 1.0, lg: 1.16, xl: 1.32 };
const SIZE_ORDER = ['xs','sm','md','lg','xl'];

/** @type {Record<string, string>} Built-in icon characters */
const ICONS = {
  'none':   '',
  'star':   '★',
  'heart':  '❤',
  'check':  '✓',
  'fire':   '🔥',
  'bolt':   '⚡',
  'rocket': '🚀',
  'code':   '⌘',
  'build':  '⚙',
  'docs':   '📘',
};

const ICON_ORDER = ['none','star','heart','check','fire','bolt','rocket','code','build','docs'];

/** Presets — match data_fetchers.py BADGE_PRESETS */
const PRESETS = {
  build:    { label: 'build',    value: 'passing', icon: 'check',  theme: 'terminal', style: 'flat',          size: 'md' },
  coverage: { label: 'coverage', value: '98%',     icon: 'bolt',   theme: 'dark',     style: 'plastic',       size: 'md' },
  release:  { label: 'release',  value: 'v2.0.0',  icon: 'rocket', theme: 'sunset',   style: 'for-the-badge', size: 'lg' },
  docs:     { label: 'docs',     value: 'stable',  icon: 'docs',   theme: 'light',    style: 'social',        size: 'md' },
  quality:  { label: 'quality',  value: 'A+',      icon: 'star',   theme: 'neon',     style: 'pill',          size: 'sm' },
};

const COLOR_PALETTE = [
  '#111827','#1f2937','#374151','#4b5563','#6b7280','#9ca3af',
  '#ffffff','#f3f4f6','#1d4ed8','#2563eb','#0ea5e9','#06b6d4',
  '#7c3aed','#a855f7','#db2777','#ef4444','#f97316','#f59e0b',
  '#84cc16','#22c55e','#10b981','#14b8a6','#8b5cf6','#ec4899',
];

/* ═══════════════════════════════════════════════════════════════
   SVG BADGE ENGINE
   ═══════════════════════════════════════════════════════════════ */

/** Escape XML/SVG special chars */
function esc(s) {
  return String(s)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

/** Clamp a value between lo and hi */
function clamp(v, lo, hi) { return Math.min(Math.max(v, lo), hi); }

/** Validate a 6-digit hex color string */
function isHex(s) { return typeof s === 'string' && /^#[0-9a-fA-F]{6}$/.test(s.trim()); }

/**
 * Estimate rendered text width — mirrors Python _text_width().
 * Uses character-count heuristic (no canvas measurement needed).
 */
function textWidth(text, fontSize) {
  const multiplier = fontSize >= 12 ? 0.62 : 0.58;
  return Math.floor(Math.max(1, text.length) * fontSize * multiplier);
}

/**
 * Generate an SVG badge string from parameters.
 * Faithfully ports api/github_stats.py → generate_custom_badge().
 *
 * @param {object} opts
 * @returns {string} SVG markup
 */
function generateBadge(opts) {
  const {
    label       = 'build',
    value       = 'passing',
    icon        = 'none',
    iconData    = '',        // base64 data URI of custom uploaded image
    style       = 'flat',
    theme       = 'dark',
    size        = 'md',
    scale       = 1.0,
    labelBg     = '',
    valueBg     = '',
    labelColor  = '',
    valueColor  = '',
    borderColor = '',
    borderRadius = null,     // null = use style default
    gradient    = false,
    uppercase   = false,
    compact     = false,
  } = opts;

  const profile = STYLES[style] || STYLES['flat'];
  const palette = THEMES[theme] || THEMES['dark'];

  /* ── Text content ── */
  const activeUppercase = profile.uppercase || uppercase;
  const rawLabel = String(label || 'label').slice(0, 40);
  const rawValue = String(value || 'value').slice(0, 52);

  /* ── Icon resolution ── */
  const hasCustomIcon = typeof iconData === 'string' && iconData.startsWith('data:image/');
  const symbol = hasCustomIcon ? '' : (ICONS[icon] || '');
  const fullLabelText = (symbol && !hasCustomIcon) ? `${symbol} ${rawLabel}`.trim() : rawLabel;

  /* ── Colors ── */
  const lbg  = isHex(labelBg)     ? labelBg.trim()     : palette.labelBg;
  const vbg  = isHex(valueBg)     ? valueBg.trim()     : palette.valueBg;
  const ltxt = isHex(labelColor)  ? labelColor.trim()  : palette.labelText;
  const vtxt = isHex(valueColor)  ? valueColor.trim()  : palette.valueText;
  const bdr  = isHex(borderColor) ? borderColor.trim() : palette.border;

  /* ── Scaling ── */
  const sizeFactor    = SIZES[size] || 1.0;
  const scaleFactor   = clamp(parseFloat(scale) || 1.0, 0.7, 2.0);
  const compactFactor = compact ? 0.88 : 1.0;
  const factor        = sizeFactor * scaleFactor * compactFactor;

  /* ── Dimensions (pre-scale base values, then round after scaling) ── */
  const basePad    = profile.padX;
  const baseFont   = profile.fontSize;
  const baseHeight = profile.height;
  const baseRadius = (borderRadius !== null)
    ? clamp(parseInt(borderRadius, 10) || 0, 0, 999)
    : profile.radius;

  const height   = Math.max(16, Math.round(baseHeight * factor));
  const padX     = Math.max(5,  Math.round(basePad    * factor));
  const fontSize = Math.max(9,  Math.round(baseFont   * factor));
  const radius   = Math.min(Math.round(baseRadius * factor), Math.floor(height / 2));

  /* ── Icon space ── */
  const iconSize       = hasCustomIcon ? Math.round(height * 0.65) : 0;
  const iconPad        = hasCustomIcon ? Math.round(iconSize * 0.4) : 0;
  const iconTotalSpace = hasCustomIcon ? iconSize + iconPad : 0;

  /* ── Width calculation ── */
  const labelRender = activeUppercase ? fullLabelText.toUpperCase() : fullLabelText;
  const valueRender = activeUppercase ? rawValue.toUpperCase()      : rawValue;

  const leftWidth  = textWidth(labelRender, fontSize) + 2 * padX + iconTotalSpace;
  const rightWidth = textWidth(valueRender, fontSize) + 2 * padX;
  const totalWidth = leftWidth + rightWidth;

  /* ── Outline style: transparent fill, only stroke ── */
  const isOutline  = style === 'outline';
  const leftFill   = isOutline ? 'none' : lbg;
  const rightFill  = isOutline ? 'none' : vbg;
  const borderAttr = profile.borderWidth > 0
    ? ` stroke="${esc(bdr)}" stroke-width="${profile.borderWidth}"`
    : '';

  /* ── Gradient overlay (plastic-style) ── */
  let defs    = '';
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

  /* ── Text Y position — mirrors Python: height/2 + fontSize*0.33 ── */
  const textY = (height / 2) + (fontSize * 0.33);

  /* ── Icon SVG ── */
  let iconSvg      = '';
  let labelTextX   = leftWidth / 2;

  if (hasCustomIcon) {
    const ix = padX;
    const iy = (height - iconSize) / 2;
    iconSvg    = `<image x="${ix}" y="${iy}" width="${iconSize}" height="${iconSize}" href="${esc(iconData)}"/>`;
    labelTextX = iconTotalSpace + padX + textWidth(labelRender, fontSize) / 2;
  }

  /* ── Junction fill rect: covers the right-concave corner of the left rect ── */
  const junctionX    = Math.max(0, leftWidth - radius);
  const junctionFill = isOutline ? 'none' : lbg;

  /* ── Compose SVG ── */
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

/* ═══════════════════════════════════════════════════════════════
   STATE
   ═══════════════════════════════════════════════════════════════ */

const DEFAULT_STATE = {
  label:        'build',
  value:        'passing',
  icon:         'check',
  iconData:     '',
  style:        'flat',
  theme:        'terminal',
  size:         'md',
  scale:        1.0,
  labelBg:      '',
  valueBg:      '',
  labelColor:   '',
  valueColor:   '',
  borderColor:  '',
  borderRadius: null,
  gradient:     false,
  uppercase:    false,
  compact:      false,
  activePreset: 'build',
};

let state = { ...DEFAULT_STATE };

/* ═══════════════════════════════════════════════════════════════
   UI HELPERS
   ═══════════════════════════════════════════════════════════════ */

/** Show a short toast message */
function showToast(msg, duration = 2000) {
  const el = document.getElementById('toast');
  el.textContent = msg;
  el.classList.add('show');
  clearTimeout(el._timer);
  el._timer = setTimeout(() => el.classList.remove('show'), duration);
}

/** Copy text to clipboard with feedback */
async function copyText(text, label = 'Copied') {
  try {
    await navigator.clipboard.writeText(text);
    showToast(`${label} copied!`);
  } catch {
    // Fallback for older browsers
    const ta = document.createElement('textarea');
    ta.value = text;
    ta.style.cssText = 'position:fixed;opacity:0;pointer-events:none';
    document.body.appendChild(ta);
    ta.select();
    document.execCommand('copy');
    ta.remove();
    showToast(`${label} copied!`);
  }
}

/** Trigger an SVG file download */
function downloadSVG(svgString, filename = 'badge.svg') {
  const blob = new Blob([svgString], { type: 'image/svg+xml' });
  const url  = URL.createObjectURL(blob);
  const a    = Object.assign(document.createElement('a'), { href: url, download: filename });
  document.body.appendChild(a);
  a.click();
  a.remove();
  URL.revokeObjectURL(url);
  showToast('SVG downloaded!');
}

/** Pop animation on preview */
function popPreview() {
  const wrap = document.getElementById('previewSvgWrap');
  wrap.classList.remove('pop');
  void wrap.offsetWidth; // reflow
  wrap.classList.add('pop');
  setTimeout(() => wrap.classList.remove('pop'), 120);
}

/* ═══════════════════════════════════════════════════════════════
   RENDER — build badge and push to DOM
   ═══════════════════════════════════════════════════════════════ */

let _currentSvg = '';

function render() {
  const svg = generateBadge(state);
  _currentSvg = svg;

  /* Preview */
  const wrap = document.getElementById('previewSvgWrap');
  wrap.innerHTML = svg;
  popPreview();

  /* Dimensions */
  const svgEl = wrap.querySelector('svg');
  if (svgEl) {
    document.getElementById('badgeDimensions').textContent =
      `${svgEl.getAttribute('width')} × ${svgEl.getAttribute('height')} px`;
  }

  /* Markdown output */
  const label = state.label || 'label';
  const alt   = `${label} badge`;
  document.getElementById('outputMarkdown').value = `![${alt}](data:image/svg+xml;base64,${btoa(unescape(encodeURIComponent(svg)))})`;

  /* SVG output */
  document.getElementById('outputSvg').value = svg;

  /* Update galleries in background */
  requestAnimationFrame(updateGalleries);
}

/* ═══════════════════════════════════════════════════════════════
   GALLERIES — show badge in all styles / all themes
   ═══════════════════════════════════════════════════════════════ */

function buildGalleryItem(svg, labelText, clickFn) {
  const div = document.createElement('div');
  div.className = 'gallery-item';
  div.setAttribute('role', 'button');
  div.setAttribute('tabindex', '0');
  div.innerHTML = svg;
  const span = document.createElement('span');
  span.className = 'gallery-item-label';
  span.textContent = labelText;
  div.appendChild(span);
  div.addEventListener('click', clickFn);
  div.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') clickFn(); });
  return div;
}

function updateGalleries() {
  const baseOpts = {
    label:       state.label,
    value:       state.value,
    icon:        state.icon,
    iconData:    state.iconData,
    size:        'md',
    scale:       1.0,
    gradient:    state.gradient,
    uppercase:   state.uppercase,
    compact:     state.compact,
    labelBg:     '',
    valueBg:     '',
    labelColor:  '',
    valueColor:  '',
    borderColor: '',
    borderRadius: null,
  };

  /* ── Style Gallery ── */
  const styleGrid = document.getElementById('galleryStyles');
  styleGrid.innerHTML = '';
  for (const styleName of STYLE_ORDER) {
    const svg = generateBadge({ ...baseOpts, style: styleName, theme: state.theme });
    styleGrid.appendChild(buildGalleryItem(svg, styleName, () => {
      state.style = styleName;
      document.getElementById('inputStyle').value = styleName;
      render();
    }));
  }

  /* ── Theme Gallery ── */
  const themeGrid = document.getElementById('galleryThemes');
  themeGrid.innerHTML = '';
  for (const themeName of THEME_ORDER) {
    const svg = generateBadge({ ...baseOpts, style: state.style, theme: themeName });
    themeGrid.appendChild(buildGalleryItem(svg, themeName, () => {
      state.theme = themeName;
      document.getElementById('inputTheme').value = themeName;
      // Reset color overrides when switching theme
      state.labelBg = state.valueBg = state.labelColor = state.valueColor = state.borderColor = '';
      syncColorFieldsFromTheme();
      render();
    }));
  }
}

/* ═══════════════════════════════════════════════════════════════
   COLOR SYNC — text inputs ↔ color pickers ↔ palette
   ═══════════════════════════════════════════════════════════════ */

const COLOR_FIELDS = [
  { key: 'labelBg',     inputId: 'inputLabelBg',     pickerId: 'pickerLabelBg'     },
  { key: 'valueBg',     inputId: 'inputValueBg',      pickerId: 'pickerValueBg'     },
  { key: 'labelColor',  inputId: 'inputLabelColor',   pickerId: 'pickerLabelColor'  },
  { key: 'valueColor',  inputId: 'inputValueColor',   pickerId: 'pickerValueColor'  },
  { key: 'borderColor', inputId: 'inputBorderColor',  pickerId: 'pickerBorderColor' },
];

let activeColorField = 'labelBg'; // which field receives palette clicks

function getColorDefault(key) {
  const theme = THEMES[state.theme] || THEMES['dark'];
  const map = { labelBg: 'labelBg', valueBg: 'valueBg', labelColor: 'labelText', valueColor: 'valueText', borderColor: 'border' };
  return theme[map[key]] || '#000000';
}

function syncColorFieldsFromTheme() {
  for (const { key, inputId, pickerId } of COLOR_FIELDS) {
    const val = state[key] || getColorDefault(key);
    document.getElementById(inputId).value   = val;
    document.getElementById(pickerId).value  = isHex(val) ? val : getColorDefault(key);
  }
}

function applyColorToField(key, hex) {
  state[key] = hex;
  const cf = COLOR_FIELDS.find(f => f.key === key);
  if (cf) {
    document.getElementById(cf.inputId).value  = hex;
    document.getElementById(cf.pickerId).value = hex;
  }
  render();
}

function initColorSync() {
  for (const { key, inputId, pickerId } of COLOR_FIELDS) {
    const textEl   = document.getElementById(inputId);
    const pickerEl = document.getElementById(pickerId);
    const fieldEl  = textEl.closest('[data-color-field]');

    /* Focus tracking → determines which field gets palette clicks */
    const markActive = () => {
      activeColorField = key;
      document.querySelectorAll('[data-color-field]').forEach(el => el.classList.remove('focused'));
      if (fieldEl) fieldEl.classList.add('focused');
    };

    textEl.addEventListener('focus', markActive);
    pickerEl.addEventListener('focus', markActive);

    /* Text input → validate hex → sync picker + state */
    textEl.addEventListener('input', () => {
      markActive();
      const v = textEl.value.trim();
      if (isHex(v)) {
        pickerEl.value = v;
        state[key] = v;
        render();
      } else if (v === '') {
        state[key] = '';
        render();
      }
    });

    /* Color picker → sync text + state */
    pickerEl.addEventListener('input', () => {
      markActive();
      const v = pickerEl.value;
      textEl.value = v;
      state[key] = v;
      render();
    });
  }

  /* Palette dots */
  const paletteGrid = document.getElementById('paletteGrid');
  for (const hex of COLOR_PALETTE) {
    const dot = document.createElement('button');
    dot.className = 'palette-dot';
    dot.style.background = hex;
    dot.title = hex;
    dot.setAttribute('aria-label', `Apply color ${hex}`);
    dot.addEventListener('click', () => applyColorToField(activeColorField, hex));
    paletteGrid.appendChild(dot);
  }
}

/* ═══════════════════════════════════════════════════════════════
   ICON PICKER
   ═══════════════════════════════════════════════════════════════ */

function initIconPicker() {
  const grid = document.getElementById('iconPickerGrid');

  for (const key of ICON_ORDER) {
    const btn = document.createElement('button');
    btn.className = 'icon-btn';
    btn.dataset.icon = key;
    btn.title = key;
    btn.setAttribute('aria-label', `Icon: ${key}`);
    btn.textContent = key === 'none' ? '∅' : (ICONS[key] || key);
    if (key === state.icon) btn.classList.add('active');

    btn.addEventListener('click', () => {
      state.icon = key;
      state.iconData = ''; // clear custom upload
      document.getElementById('iconFileInput').value = '';
      document.getElementById('iconPreviewImg').hidden = true;
      document.getElementById('iconClearBtn').hidden = true;
      grid.querySelectorAll('.icon-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      render();
    });

    grid.appendChild(btn);
  }

  /* File upload */
  const fileInput  = document.getElementById('iconFileInput');
  const previewImg = document.getElementById('iconPreviewImg');
  const clearBtn   = document.getElementById('iconClearBtn');

  fileInput.addEventListener('change', () => {
    const file = fileInput.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (e) => {
      const img = new Image();
      img.onload = () => {
        /* Resize to 64×64 via canvas */
        const canvas    = document.createElement('canvas');
        canvas.width    = 64;
        canvas.height   = 64;
        const ctx       = canvas.getContext('2d');
        const s         = Math.min(64 / img.width, 64 / img.height);
        const w         = img.width  * s;
        const h         = img.height * s;
        ctx.drawImage(img, (64 - w) / 2, (64 - h) / 2, w, h);
        const dataUrl   = canvas.toDataURL('image/png');

        state.iconData  = dataUrl;
        state.icon      = 'none';
        previewImg.src  = dataUrl;
        previewImg.hidden = false;
        clearBtn.hidden = false;

        /* Deactivate built-in icon buttons */
        document.querySelectorAll('.icon-btn').forEach(b => b.classList.remove('active'));
        render();
      };
      img.src = e.target.result;
    };
    reader.readAsDataURL(file);
  });

  clearBtn.addEventListener('click', () => {
    state.iconData  = '';
    fileInput.value = '';
    previewImg.hidden = true;
    clearBtn.hidden   = true;
    /* Re-activate default icon */
    const defaultBtn = grid.querySelector('[data-icon="none"]');
    if (defaultBtn) defaultBtn.classList.add('active');
    state.icon = 'none';
    render();
  });
}

/* ═══════════════════════════════════════════════════════════════
   PRESETS
   ═══════════════════════════════════════════════════════════════ */

function applyPreset(name) {
  const p = PRESETS[name];
  if (!p) return;

  state.activePreset = name;
  state.label        = p.label;
  state.value        = p.value;
  state.icon         = p.icon;
  state.iconData     = '';
  state.style        = p.style;
  state.theme        = p.theme;
  state.size         = p.size || 'md';
  state.scale        = 1.0;
  state.gradient     = false;
  state.uppercase    = false;
  state.compact      = false;
  state.borderRadius = null;
  state.labelBg      = '';
  state.valueBg      = '';
  state.labelColor   = '';
  state.valueColor   = '';
  state.borderColor  = '';

  syncAllFieldsFromState();
  render();
}

function initPresets() {
  const grid = document.getElementById('presetGrid');
  for (const name of Object.keys(PRESETS)) {
    const btn = document.createElement('button');
    btn.className = 'preset-btn';
    btn.dataset.preset = name;
    btn.textContent = name;
    if (name === state.activePreset) btn.classList.add('active');

    btn.addEventListener('click', () => {
      grid.querySelectorAll('.preset-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      applyPreset(name);
    });

    grid.appendChild(btn);
  }
}

/* ═══════════════════════════════════════════════════════════════
   SYNC ALL FIELDS → DOM (called after preset or reset)
   ═══════════════════════════════════════════════════════════════ */

function syncAllFieldsFromState() {
  document.getElementById('inputLabel').value       = state.label;
  document.getElementById('inputValue').value       = state.value;
  document.getElementById('inputStyle').value       = state.style;
  document.getElementById('inputTheme').value       = state.theme;
  document.getElementById('inputSize').value        = state.size;
  document.getElementById('inputScale').value       = state.scale;
  document.getElementById('scaleVal').textContent   = `${parseFloat(state.scale).toFixed(2)}×`;

  const br = state.borderRadius !== null ? state.borderRadius : (STYLES[state.style] || STYLES['flat']).radius;
  document.getElementById('inputRadius').value      = br;
  document.getElementById('radiusVal').textContent  = br;

  document.getElementById('optGradient').checked   = state.gradient;
  document.getElementById('optUppercase').checked  = state.uppercase;
  document.getElementById('optCompact').checked    = state.compact;

  /* Icon picker */
  document.querySelectorAll('.icon-btn').forEach(b => {
    b.classList.toggle('active', b.dataset.icon === state.icon);
  });

  /* Clear custom icon */
  if (!state.iconData) {
    const fi = document.getElementById('iconFileInput');
    if (fi) fi.value = '';
    document.getElementById('iconPreviewImg').hidden = true;
    document.getElementById('iconClearBtn').hidden   = true;
  }

  /* Colors */
  syncColorFieldsFromTheme();

  /* Preset buttons */
  document.querySelectorAll('.preset-btn').forEach(b => {
    b.classList.toggle('active', b.dataset.preset === state.activePreset);
  });
}

/* ═══════════════════════════════════════════════════════════════
   FORM WIRING — connect every control to state + re-render
   ═══════════════════════════════════════════════════════════════ */

function initFormWiring() {
  /* Text inputs */
  const textFields = [
    ['inputLabel',  'label'],
    ['inputValue',  'value'],
  ];
  for (const [id, key] of textFields) {
    document.getElementById(id).addEventListener('input', (e) => {
      state[key] = e.target.value;
      render();
    });
  }

  /* Selects */
  const selectFields = [
    ['inputStyle', 'style'],
    ['inputTheme', 'theme'],
    ['inputSize',  'size'],
  ];
  for (const [id, key] of selectFields) {
    /* Populate select options */
    const el = document.getElementById(id);
    const lists = { inputStyle: STYLE_ORDER, inputTheme: THEME_ORDER, inputSize: SIZE_ORDER };
    for (const opt of lists[id]) {
      el.insertAdjacentHTML('beforeend', `<option value="${opt}">${opt}</option>`);
    }
    el.value = state[key];
    el.addEventListener('change', (e) => {
      state[key] = e.target.value;
      if (key === 'style') {
        /* Reset border radius to style default when style changes */
        state.borderRadius = null;
        const defR = (STYLES[e.target.value] || STYLES['flat']).radius;
        document.getElementById('inputRadius').value = defR;
        document.getElementById('radiusVal').textContent = defR;
      }
      if (key === 'theme') {
        state.labelBg = state.valueBg = state.labelColor = state.valueColor = state.borderColor = '';
        syncColorFieldsFromTheme();
      }
      render();
    });
  }

  /* Scale range */
  const scaleEl = document.getElementById('inputScale');
  scaleEl.addEventListener('input', () => {
    state.scale = parseFloat(scaleEl.value);
    document.getElementById('scaleVal').textContent = `${state.scale.toFixed(2)}×`;
    render();
  });

  /* Border radius range */
  const radiusEl = document.getElementById('inputRadius');
  radiusEl.addEventListener('input', () => {
    state.borderRadius = parseInt(radiusEl.value, 10);
    document.getElementById('radiusVal').textContent = radiusEl.value;
    render();
  });

  /* Checkboxes */
  const checkFields = [
    ['optGradient',  'gradient'],
    ['optUppercase', 'uppercase'],
    ['optCompact',   'compact'],
  ];
  for (const [id, key] of checkFields) {
    document.getElementById(id).addEventListener('change', (e) => {
      state[key] = e.target.checked;
      render();
    });
  }
}

/* ═══════════════════════════════════════════════════════════════
   ACTION BUTTONS
   ═══════════════════════════════════════════════════════════════ */

function initActions() {
  document.getElementById('btnCopySvg').addEventListener('click', () => {
    copyText(_currentSvg, 'SVG');
  });

  document.getElementById('btnCopyMarkdown').addEventListener('click', () => {
    copyText(document.getElementById('outputMarkdown').value, 'Markdown');
  });

  document.getElementById('btnDownloadSvg').addEventListener('click', () => {
    const name = `badge-${(state.label || 'label').replace(/\s+/g, '-')}-${Date.now()}.svg`;
    downloadSVG(_currentSvg, name);
  });

  document.getElementById('btnReset').addEventListener('click', () => {
    state = { ...DEFAULT_STATE };
    syncAllFieldsFromState();
    render();
    showToast('Reset to defaults');
  });

  /* Inline copy buttons next to textareas */
  document.querySelectorAll('.output-copy-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const ta = document.getElementById(btn.dataset.target);
      if (ta) copyText(ta.value, btn.closest('.output-group')?.querySelector('.output-label')?.textContent?.trim() || 'Text');
    });
  });
}

/* ═══════════════════════════════════════════════════════════════
   PREVIEW BACKGROUND SWITCHER
   ═══════════════════════════════════════════════════════════════ */

function initPreviewBg() {
  const stage   = document.getElementById('previewStage');
  const buttons = document.querySelectorAll('.bg-btn');

  buttons.forEach(btn => {
    btn.addEventListener('click', () => {
      buttons.forEach(b => { b.classList.remove('active'); b.setAttribute('aria-pressed', 'false'); });
      btn.classList.add('active');
      btn.setAttribute('aria-pressed', 'true');
      stage.className = `preview-stage ${btn.dataset.bg}`;
    });
  });
}

/* ═══════════════════════════════════════════════════════════════
   DARK / LIGHT MODE TOGGLE
   ═══════════════════════════════════════════════════════════════ */

function initThemeToggle() {
  const btn    = document.getElementById('themeToggle');
  const html   = document.documentElement;
  const stored = localStorage.getItem('badge-forge-theme');

  if (stored === 'light') html.setAttribute('data-theme', 'light');

  btn.addEventListener('click', () => {
    const current = html.getAttribute('data-theme');
    const next    = current === 'dark' ? 'light' : 'dark';
    html.setAttribute('data-theme', next);
    localStorage.setItem('badge-forge-theme', next);
  });
}

/* ═══════════════════════════════════════════════════════════════
   INITIALISE
   ═══════════════════════════════════════════════════════════════ */

function init() {
  initThemeToggle();
  initPresets();
  initFormWiring();
  initColorSync();
  initIconPicker();
  initActions();
  initPreviewBg();

  /* Set initial state to 'build' preset */
  applyPreset('build');
}

document.addEventListener('DOMContentLoaded', init);
