"""
GitHub Stats SVG Card Generators.

Produces four card types:
  1. stats   — stars, commits, PRs, issues, total contributions
  2. streak  — current streak, longest streak, total contributions
  3. graph   — contribution heatmap (calendar grid)
  4. views   — profile view counter badge

All cards are returned as inline SVG (image/svg+xml).
"""

import math
import datetime
import hashlib
import json
from typing import Optional

# ─── colour helpers ──────────────────────────────────────────────

THEMES = {
    "dark": {
        "bg": "#0d1117",
        "border": "#30363d",
        "title": "#58a6ff",
        "text": "#c9d1d9",
        "icon": "#58a6ff",
        "accent": "#58a6ff",
        "subtext": "#8b949e",
        "bar": "#238636",
        "bar_bg": "#161b22",
        "cell_empty": "#161b22",
        "cell_l1": "#0e4429",
        "cell_l2": "#006d32",
        "cell_l3": "#26a641",
        "cell_l4": "#39d353",
    },
    "radical": {
        "bg": "#141321",
        "border": "#443760",
        "title": "#fe428e",
        "text": "#a9fef7",
        "icon": "#f8d847",
        "accent": "#fe428e",
        "subtext": "#a9fef7",
        "bar": "#fe428e",
        "bar_bg": "#1a1830",
        "cell_empty": "#1a1830",
        "cell_l1": "#5a1040",
        "cell_l2": "#9b1860",
        "cell_l3": "#d42878",
        "cell_l4": "#fe428e",
    },
    "tokyonight": {
        "bg": "#1a1b27",
        "border": "#383951",
        "title": "#70a5fd",
        "text": "#a9b1d6",
        "icon": "#bf91f3",
        "accent": "#70a5fd",
        "subtext": "#787c99",
        "bar": "#70a5fd",
        "bar_bg": "#20222e",
        "cell_empty": "#20222e",
        "cell_l1": "#1c3a5f",
        "cell_l2": "#2d5a9e",
        "cell_l3": "#4d7cc4",
        "cell_l4": "#70a5fd",
    },
    "gruvbox": {
        "bg": "#282828",
        "border": "#3c3836",
        "title": "#fabd2f",
        "text": "#ebdbb2",
        "icon": "#fe8019",
        "accent": "#fabd2f",
        "subtext": "#a89984",
        "bar": "#b8bb26",
        "bar_bg": "#1d2021",
        "cell_empty": "#1d2021",
        "cell_l1": "#4a4520",
        "cell_l2": "#7a7a20",
        "cell_l3": "#98971a",
        "cell_l4": "#b8bb26",
    },
    "ocean": {
        "bg": "#0a192f",
        "border": "#1e3a5f",
        "title": "#64ffda",
        "text": "#ccd6f6",
        "icon": "#64ffda",
        "accent": "#64ffda",
        "subtext": "#8892b0",
        "bar": "#64ffda",
        "bar_bg": "#112240",
        "cell_empty": "#112240",
        "cell_l1": "#0a3a3a",
        "cell_l2": "#0d6060",
        "cell_l3": "#20a0a0",
        "cell_l4": "#64ffda",
    },
    "sunset": {
        "bg": "#1a1020",
        "border": "#3d2050",
        "title": "#ff6b6b",
        "text": "#f0d0e0",
        "icon": "#feca57",
        "accent": "#ff6b6b",
        "subtext": "#a08090",
        "bar": "#ff9ff3",
        "bar_bg": "#201030",
        "cell_empty": "#201030",
        "cell_l1": "#5a2040",
        "cell_l2": "#a03060",
        "cell_l3": "#d04080",
        "cell_l4": "#ff6b6b",
    },
    "light": {
        "bg": "#ffffff",
        "border": "#d0d7de",
        "title": "#0969da",
        "text": "#1f2328",
        "icon": "#0969da",
        "accent": "#0969da",
        "subtext": "#656d76",
        "bar": "#2da44e",
        "bar_bg": "#eaeef2",
        "cell_empty": "#ebedf0",
        "cell_l1": "#9be9a8",
        "cell_l2": "#40c463",
        "cell_l3": "#30a14e",
        "cell_l4": "#216e39",
    },
}


def _esc(t: str) -> str:
    return (
        t.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#39;")
    )


def _get_theme(name: str) -> dict:
    return THEMES.get(name, THEMES["dark"])


def _parse_color(raw: str, fallback: str) -> str:
    c = raw.strip().lstrip("#")
    if len(c) in (3, 6) and all(ch in "0123456789abcdefABCDEF" for ch in c):
        return f"#{c}"
    return fallback


# ─── icons (mini inline SVG paths) ──────────────────────────────

ICONS = {
    "star": '<path d="M8 .25a.75.75 0 01.673.418l1.882 3.815 4.21.612a.75.75 0 01.416 1.279l-3.046 2.97.719 4.192a.75.75 0 01-1.088.791L8 12.347l-3.766 1.98a.75.75 0 01-1.088-.79l.72-4.194L.818 6.374a.75.75 0 01.416-1.28l4.21-.611L7.327.668A.75.75 0 018 .25z"/>',
    "commit": '<path d="M11.93 8.5a4.002 4.002 0 01-7.86 0H.75a.75.75 0 010-1.5h3.32a4.002 4.002 0 017.86 0h3.32a.75.75 0 010 1.5zm-1.43-.25a2.5 2.5 0 10-5 0 2.5 2.5 0 005 0z"/>',
    "pr": '<path d="M7.177 3.073L9.573.677A.25.25 0 0110 .854v4.792a.25.25 0 01-.427.177L7.177 3.427a.25.25 0 010-.354zM3.75 2.5a.75.75 0 100 1.5.75.75 0 000-1.5zm-2.25.75a2.25 2.25 0 113 2.122v5.256a2.251 2.251 0 11-1.5 0V5.372A2.25 2.25 0 011.5 3.25zM11 2.5h-1V4h1a1 1 0 011 1v5.628a2.251 2.251 0 101.5 0V5A2.5 2.5 0 0011 2.5zm1 10.25a.75.75 0 100 1.5.75.75 0 000-1.5zM3.75 12a.75.75 0 100 1.5.75.75 0 000-1.5z"/>',
    "issue": '<path d="M8 9.5a1.5 1.5 0 100-3 1.5 1.5 0 000 3z"/><path d="M8 0a8 8 0 100 16A8 8 0 008 0zM1.5 8a6.5 6.5 0 1113 0 6.5 6.5 0 01-13 0z"/>',
    "contrib": '<path d="M2 2.5A2.5 2.5 0 014.5 0h8.75a.75.75 0 01.75.75v12.5a.75.75 0 01-.75.75h-2.5a.75.75 0 110-1.5h1.75v-2h-8a1 1 0 00-.714 1.7.75.75 0 01-1.072 1.05A2.495 2.495 0 012 11.5zm10.5-1h-8a1 1 0 00-1 1v6.708A2.486 2.486 0 014.5 9h8zM5 12.25v3.25a.25.25 0 00.4.2l1.45-1.087a.25.25 0 01.3 0L8.6 15.7a.25.25 0 00.4-.2v-3.25a.25.25 0 00-.25-.25h-3.5a.25.25 0 00-.25.25z"/>',
    "fire": '<path d="M7.998 14.5c2.832 0 5-1.98 5-4.5 0-1.463-.68-2.19-1.879-3.383l-.036-.037c-1.013-1.008-2.3-2.29-2.834-4.434-.322.256-.63.579-.864.953-.432.696-.621 1.58-.046 2.73.473.947.67 2.284-.278 3.232-.61.61-1.545.84-2.403.588a2.06 2.06 0 01-1.162-.96C2.344 10.267 3.96 14.5 7.998 14.5z"/>',
    "calendar": '<path d="M4.75 0a.75.75 0 01.75.75V2h5V.75a.75.75 0 011.5 0V2h1.25c.966 0 1.75.784 1.75 1.75v10.5A1.75 1.75 0 0113.25 16H2.75A1.75 1.75 0 011 14.25V3.75C1 2.784 1.784 2 2.75 2H4V.75A.75.75 0 014.75 0zm0 3.5H2.75a.25.25 0 00-.25.25V6h11V3.75a.25.25 0 00-.25-.25H4.75zm-2.5 4v6.75c0 .138.112.25.25.25h10.5a.25.25 0 00.25-.25V7.5z"/>',
    "eye": '<path d="M8 2c1.981 0 3.671.992 4.933 2.078 1.27 1.091 2.187 2.345 2.637 3.023a1.62 1.62 0 010 1.798c-.45.678-1.367 1.932-2.637 3.023C11.67 13.008 9.981 14 8 14c-1.981 0-3.671-.992-4.933-2.078C1.797 10.831.88 9.577.43 8.9a1.619 1.619 0 010-1.798c.45-.678 1.367-1.932 2.637-3.023C4.33 2.992 6.019 2 8 2zM1.679 7.932a.12.12 0 000 .136c.411.622 1.241 1.75 2.366 2.717C5.176 11.758 6.527 12.5 8 12.5c1.473 0 2.825-.742 3.955-1.715 1.124-.967 1.954-2.096 2.366-2.717a.12.12 0 000-.136c-.412-.621-1.242-1.75-2.366-2.717C10.824 4.242 9.473 3.5 8 3.5c-1.473 0-2.824.742-3.955 1.715-1.124.967-1.954 2.096-2.366 2.717zM8 10a2 2 0 110-4 2 2 0 010 4z"/>',
}


def _icon_svg(name: str, color: str, size: int = 16) -> str:
    path = ICONS.get(name, "")
    return f'<svg viewBox="0 0 16 16" width="{size}" height="{size}" fill="{_esc(color)}">{path}</svg>'


# ─── number formatting ───────────────────────────────────────────

def _fmt(n: int) -> str:
    if n >= 1_000_000:
        return f"{n/1_000_000:.1f}M"
    if n >= 1_000:
        return f"{n/1_000:.1f}k"
    return str(n)


# ─── rank calculation ────────────────────────────────────────────

def _calc_rank(stars: int, commits: int, prs: int, issues: int, contribs: int) -> str:
    score = (
        stars * 1.0
        + commits * 0.25
        + prs * 0.5
        + issues * 0.25
        + contribs * 0.1
    )
    if score >= 500:
        return "S+"
    if score >= 200:
        return "S"
    if score >= 100:
        return "A+"
    if score >= 50:
        return "A"
    if score >= 20:
        return "B+"
    if score >= 10:
        return "B"
    return "C"


def _rank_progress(stars, commits, prs, issues, contribs) -> float:
    score = stars * 1.0 + commits * 0.25 + prs * 0.5 + issues * 0.25 + contribs * 0.1
    thresholds = [0, 10, 20, 50, 100, 200, 500, 1000]
    for i in range(len(thresholds) - 1):
        if score < thresholds[i + 1]:
            lo, hi = thresholds[i], thresholds[i + 1]
            return (score - lo) / (hi - lo)
    return 1.0


# ─── animation helpers ───────────────────────────────────────────

def _fade_in(delay_ms: int = 0) -> str:
    return f"opacity:0;animation:fadeIn .4s ease {delay_ms}ms forwards"


# ─── CARD 1: GitHub Stats ────────────────────────────────────────

def generate_stats_card(
    username: str = "octocat",
    stars: int = 0,
    commits: int = 0,
    prs: int = 0,
    issues: int = 0,
    contribs: int = 0,
    theme: str = "dark",
    custom_title: Optional[str] = None,
    hide_border: bool = False,
    hide_rank: bool = False,
    border_radius: int = 10,
    bg_color: Optional[str] = None,
    title_color: Optional[str] = None,
    text_color: Optional[str] = None,
    icon_color: Optional[str] = None,
    border_color: Optional[str] = None,
    animate: bool = True,
) -> str:
    t = _get_theme(theme)
    bg = _parse_color(bg_color, t["bg"]) if bg_color else t["bg"]
    border = _parse_color(border_color, t["border"]) if border_color else t["border"]
    title_c = _parse_color(title_color, t["title"]) if title_color else t["title"]
    text_c = _parse_color(text_color, t["text"]) if text_color else t["text"]
    icon_c = _parse_color(icon_color, t["icon"]) if icon_color else t["icon"]

    card_w, card_h = 495, 195
    title = _esc(custom_title or f"{username}'s GitHub Stats")
    rank = _calc_rank(stars, commits, prs, issues, contribs)
    progress = _rank_progress(stars, commits, prs, issues, contribs)

    border_attr = f'stroke="{_esc(border)}" stroke-width="1"' if not hide_border else 'stroke="none"'

    anim_css = ""
    if animate:
        anim_css = """
    <style>
      @keyframes fadeIn { from {opacity:0;transform:translateX(-8px)} to {opacity:1;transform:translateX(0)} }
      @keyframes scaleIn { from {opacity:0;transform:scale(0)} to {opacity:1;transform:scale(1)} }
      @keyframes growBar { from {stroke-dashoffset:251} to {stroke-dashoffset:OFFSET} }
      .stat-row { opacity:0; animation: fadeIn .5s ease forwards; }
      .rank-circle { opacity:0; animation: scaleIn .6s ease .4s forwards; transform-origin: center; }
      .rank-bar { animation: growBar 1s ease .5s forwards; stroke-dashoffset: 251; }
    </style>""".replace("OFFSET", f"{251 - 251 * progress:.1f}")
    else:
        anim_css = "<style>.stat-row{opacity:1}.rank-circle{opacity:1}</style>"

    stats_data = [
        ("star", "Total Stars", stars),
        ("commit", "Total Commits", commits),
        ("pr", "Total PRs", prs),
        ("issue", "Total Issues", issues),
        ("contrib", "Contributed to", contribs),
    ]

    rows = ""
    for i, (icon_name, label, value) in enumerate(stats_data):
        y = 48 + i * 28
        delay = i * 100
        rows += f'''    <g class="stat-row" style="animation-delay:{delay}ms" transform="translate(25, {y})">
      {_icon_svg(icon_name, icon_c, 16)}
      <text x="24" y="12" fill="{_esc(text_c)}" font-size="13" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif">{_esc(label)}:</text>
      <text x="190" y="12" fill="{_esc(text_c)}" font-size="13" font-weight="700" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif">{_fmt(value)}</text>
    </g>
'''

    rank_svg = ""
    if not hide_rank:
        cx, cy, r = 420, 105, 40
        circumference = 2 * math.pi * r
        offset = circumference - circumference * progress
        rank_svg = f'''    <g class="rank-circle" transform="translate({cx},{cy})">
      <circle r="{r}" fill="none" stroke="{_esc(t.get('bar_bg', '#161b22'))}" stroke-width="6" />
      <circle class="rank-bar" r="{r}" fill="none" stroke="{_esc(title_c)}" stroke-width="6"
        stroke-dasharray="{circumference:.1f}" stroke-dashoffset="{offset:.1f}"
        stroke-linecap="round" transform="rotate(-90)" style="{'animation:growBar 1s ease .5s forwards;stroke-dashoffset:'+str(circumference) if animate else ''}" />
      <text x="0" y="8" text-anchor="middle" fill="{_esc(title_c)}" font-size="22" font-weight="800"
        font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif">{rank}</text>
    </g>
'''

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{card_w}" height="{card_h}" viewBox="0 0 {card_w} {card_h}">
  {anim_css}
  <rect x="0.5" y="0.5" width="{card_w - 1}" height="{card_h - 1}" rx="{border_radius}" ry="{border_radius}"
    fill="{_esc(bg)}" {border_attr} />
  <text x="25" y="30" fill="{_esc(title_c)}" font-size="16" font-weight="700"
    font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif">{title}</text>
{rows}{rank_svg}</svg>'''


# ─── CARD 2: Streak Stats ────────────────────────────────────────

def generate_streak_card(
    username: str = "octocat",
    current_streak: int = 0,
    longest_streak: int = 0,
    total_contribs: int = 0,
    streak_start: str = "",
    streak_end: str = "",
    longest_start: str = "",
    longest_end: str = "",
    theme: str = "dark",
    hide_border: bool = False,
    border_radius: int = 10,
    bg_color: Optional[str] = None,
    title_color: Optional[str] = None,
    text_color: Optional[str] = None,
    accent_color: Optional[str] = None,
    border_color: Optional[str] = None,
    animate: bool = True,
) -> str:
    t = _get_theme(theme)
    bg = _parse_color(bg_color, t["bg"]) if bg_color else t["bg"]
    border = _parse_color(border_color, t["border"]) if border_color else t["border"]
    title_c = _parse_color(title_color, t["title"]) if title_color else t["title"]
    text_c = _parse_color(text_color, t["text"]) if text_color else t["text"]
    accent = _parse_color(accent_color, t["accent"]) if accent_color else t["accent"]
    sub_c = t["subtext"]

    card_w, card_h = 495, 195
    border_attr = f'stroke="{_esc(border)}" stroke-width="1"' if not hide_border else 'stroke="none"'

    anim_css = ""
    if animate:
        anim_css = """
    <style>
      @keyframes fadeIn { from {opacity:0;transform:translateY(6px)} to {opacity:1;transform:translateY(0)} }
      @keyframes countUp { from {opacity:0;transform:scale(.5)} to {opacity:1;transform:scale(1)} }
      .streak-col { opacity:0; animation: fadeIn .5s ease forwards; }
      .big-num { opacity:0; animation: countUp .4s ease forwards; transform-origin:center; }
    </style>"""
    else:
        anim_css = "<style>.streak-col{opacity:1}.big-num{opacity:1}</style>"

    col_w = card_w / 3
    sections = [
        ("Total Contributions", _fmt(total_contribs), "All Time", 0),
        ("Current Streak", str(current_streak), f"{streak_start} - {streak_end}" if streak_start else "N/A", 1),
        ("Longest Streak", str(longest_streak), f"{longest_start} - {longest_end}" if longest_start else "N/A", 2),
    ]

    cols_svg = ""
    for label, value, sub, idx in sections:
        cx = col_w * idx + col_w / 2
        delay = idx * 150
        fire = _icon_svg("fire", accent, 20) if idx == 1 and current_streak > 0 else ""
        cols_svg += f'''    <g class="streak-col" style="animation-delay:{delay}ms" transform="translate({cx:.0f}, 55)">
      <text y="0" text-anchor="middle" fill="{_esc(sub_c)}" font-size="12"
        font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif">{_esc(label)}</text>
      <g class="big-num" style="animation-delay:{delay + 100}ms">
        <text y="50" text-anchor="middle" fill="{_esc(text_c)}" font-size="36" font-weight="800"
          font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif">{_esc(value)}</text>
      </g>
      <text y="75" text-anchor="middle" fill="{_esc(sub_c)}" font-size="10"
        font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif">{_esc(sub)}</text>
    </g>
'''
        if idx < 2:
            sep_x = col_w * (idx + 1)
            cols_svg += f'    <line x1="{sep_x:.0f}" y1="35" x2="{sep_x:.0f}" y2="165" stroke="{_esc(border)}" stroke-width="1" />\n'

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{card_w}" height="{card_h}" viewBox="0 0 {card_w} {card_h}">
  {anim_css}
  <rect x="0.5" y="0.5" width="{card_w - 1}" height="{card_h - 1}" rx="{border_radius}" ry="{border_radius}"
    fill="{_esc(bg)}" {border_attr} />
  <text x="{card_w/2}" y="25" text-anchor="middle" fill="{_esc(title_c)}" font-size="16" font-weight="700"
    font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif">{_esc(username)}'s Streak Stats</text>
{cols_svg}</svg>'''


# ─── CARD 3: Contribution Graph ──────────────────────────────────

def _generate_sample_contributions(username: str, weeks: int = 52) -> list:
    """Generate deterministic pseudo-random contribution data from username hash."""
    seed = int(hashlib.md5(username.encode()).hexdigest()[:8], 16)
    rng_state = seed
    data = []
    for w in range(weeks):
        week = []
        for d in range(7):
            rng_state = (rng_state * 1103515245 + 12345) & 0x7FFFFFFF
            raw = rng_state % 100
            if raw < 30:
                count = 0
            elif raw < 55:
                count = 1 + (rng_state >> 4) % 3
            elif raw < 78:
                count = 4 + (rng_state >> 8) % 5
            elif raw < 92:
                count = 9 + (rng_state >> 12) % 6
            else:
                count = 15 + (rng_state >> 16) % 10
            week.append(count)
        data.append(week)
    return data


def generate_graph_card(
    username: str = "octocat",
    contributions: Optional[list] = None,
    theme: str = "dark",
    hide_border: bool = False,
    border_radius: int = 10,
    bg_color: Optional[str] = None,
    title_color: Optional[str] = None,
    text_color: Optional[str] = None,
    border_color: Optional[str] = None,
    cell_size: int = 11,
    cell_gap: int = 3,
    weeks: int = 52,
    animate: bool = True,
) -> str:
    t = _get_theme(theme)
    bg = _parse_color(bg_color, t["bg"]) if bg_color else t["bg"]
    border = _parse_color(border_color, t["border"]) if border_color else t["border"]
    title_c = _parse_color(title_color, t["title"]) if title_color else t["title"]
    text_c = _parse_color(text_color, t["text"]) if text_color else t["text"]

    cell_colors = [t["cell_empty"], t["cell_l1"], t["cell_l2"], t["cell_l3"], t["cell_l4"]]

    if contributions is None:
        contributions = _generate_sample_contributions(username, weeks)

    grid_w = weeks * (cell_size + cell_gap)
    grid_h = 7 * (cell_size + cell_gap)
    pad_x, pad_y = 45, 55
    card_w = grid_w + pad_x + 25
    card_h = grid_h + pad_y + 30
    border_attr = f'stroke="{_esc(border)}" stroke-width="1"' if not hide_border else 'stroke="none"'

    anim_css = ""
    if animate:
        anim_css = """
    <style>
      @keyframes cellPop { from {opacity:0;transform:scale(0)} to {opacity:1;transform:scale(1)} }
      .cell { opacity:0; animation: cellPop .2s ease forwards; transform-origin:center; }
    </style>"""
    else:
        anim_css = "<style>.cell{opacity:1}</style>"

    day_labels = ["Mon", "Wed", "Fri"]
    day_label_svg = ""
    for label, row_idx in [("Mon", 1), ("Wed", 3), ("Fri", 5)]:
        y = pad_y + row_idx * (cell_size + cell_gap) + cell_size - 2
        day_label_svg += f'    <text x="{pad_x - 8}" y="{y}" text-anchor="end" fill="{_esc(t["subtext"])}" font-size="9" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif">{label}</text>\n'

    month_labels_svg = ""
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    today = datetime.date.today()
    for m_idx in range(12):
        week_approx = int(m_idx * (weeks / 12))
        x = pad_x + week_approx * (cell_size + cell_gap)
        month_labels_svg += f'    <text x="{x}" y="{pad_y - 8}" fill="{_esc(t["subtext"])}" font-size="9" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif">{months[(today.month - 12 + m_idx) % 12]}</text>\n'

    cells_svg = ""
    total = 0
    for w_idx, week in enumerate(contributions[:weeks]):
        for d_idx, count in enumerate(week[:7]):
            total += count
            if count == 0:
                level = 0
            elif count <= 3:
                level = 1
            elif count <= 8:
                level = 2
            elif count <= 14:
                level = 3
            else:
                level = 4
            x = pad_x + w_idx * (cell_size + cell_gap)
            y = pad_y + d_idx * (cell_size + cell_gap)
            delay = w_idx * 8 + d_idx * 2
            cells_svg += f'    <rect class="cell" style="animation-delay:{delay}ms" x="{x}" y="{y}" width="{cell_size}" height="{cell_size}" rx="2" ry="2" fill="{cell_colors[level]}"><title>{count} contributions</title></rect>\n'

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{card_w}" height="{card_h}" viewBox="0 0 {card_w} {card_h}">
  {anim_css}
  <rect x="0.5" y="0.5" width="{card_w - 1}" height="{card_h - 1}" rx="{border_radius}" ry="{border_radius}"
    fill="{_esc(bg)}" {border_attr} />
  <text x="{pad_x}" y="28" fill="{_esc(title_c)}" font-size="14" font-weight="700"
    font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif">{_esc(username)}'s Contribution Graph</text>
  <text x="{pad_x}" y="42" fill="{_esc(t['subtext'])}" font-size="11"
    font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif">{_fmt(total)} contributions in the last year</text>
{month_labels_svg}{day_label_svg}{cells_svg}</svg>'''


# ─── CARD 4: Profile Views Counter ───────────────────────────────

def generate_views_card(
    username: str = "octocat",
    count: int = 0,
    theme: str = "dark",
    label: str = "Profile Views",
    style: str = "flat",
    bg_color: Optional[str] = None,
    label_color: Optional[str] = None,
    count_color: Optional[str] = None,
    icon_show: bool = True,
) -> str:
    t = _get_theme(theme)
    bg = _parse_color(bg_color, t["bg"]) if bg_color else t["bg"]
    label_c = _parse_color(label_color, t["subtext"]) if label_color else t["subtext"]
    count_c = _parse_color(count_color, t["accent"]) if count_color else t["accent"]

    count_str = _fmt(count)
    label_w = len(label) * 7 + 20
    count_w = len(count_str) * 8 + 20
    icon_w = 22 if icon_show else 0
    total_w = label_w + count_w + icon_w
    h = 28

    if style == "for-the-badge":
        h = 32
        label_w += 10
        count_w += 10

    icon_svg = ""
    if icon_show:
        icon_svg = f'<g transform="translate(8, 6)">{_icon_svg("eye", label_c, 14)}</g>'

    if style == "flat":
        return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{total_w}" height="{h}">
  <rect width="{label_w + icon_w}" height="{h}" fill="{_esc(bg)}" rx="3"/>
  <rect x="{label_w + icon_w}" width="{count_w}" height="{h}" fill="{_esc(count_c)}" rx="3"/>
  <rect x="{label_w + icon_w}" width="4" height="{h}" fill="{_esc(count_c)}"/>
  {icon_svg}
  <text x="{icon_w + label_w/2}" y="{h/2 + 4}" text-anchor="middle" fill="{_esc(label_c)}" font-size="11"
    font-family="Verdana,DejaVu Sans,sans-serif">{_esc(label)}</text>
  <text x="{label_w + icon_w + count_w/2}" y="{h/2 + 4}" text-anchor="middle" fill="#fff" font-size="11" font-weight="700"
    font-family="Verdana,DejaVu Sans,sans-serif">{_esc(count_str)}</text>
</svg>'''
    else:
        return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{total_w}" height="{h}">
  <rect width="{total_w}" height="{h}" fill="{_esc(bg)}" rx="4" stroke="{_esc(t['border'])}" stroke-width="1"/>
  {icon_svg}
  <text x="{icon_w + 8}" y="{h/2 + 4}" fill="{_esc(label_c)}" font-size="11"
    font-family="Verdana,DejaVu Sans,sans-serif">{_esc(label)}</text>
  <text x="{icon_w + label_w + 4}" y="{h/2 + 4}" fill="{_esc(count_c)}" font-size="12" font-weight="700"
    font-family="Verdana,DejaVu Sans,sans-serif">{_esc(count_str)}</text>
</svg>'''
