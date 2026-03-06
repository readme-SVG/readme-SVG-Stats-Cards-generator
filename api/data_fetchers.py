from __future__ import annotations

from github_stats import COLOR_PALETTE, COLOR_THEMES, ICON_SET, SIZE_MAP, STYLE_MAP

BADGE_PRESETS = {
    "build": {"label": "build", "value": "passing", "icon": "check", "theme": "terminal", "style": "flat", "size": "md"},
    "coverage": {"label": "coverage", "value": "98%", "icon": "bolt", "theme": "dark", "style": "plastic", "size": "md"},
    "release": {"label": "release", "value": "v2.0.0", "icon": "rocket", "theme": "sunset", "style": "for-the-badge", "size": "lg"},
    "docs": {"label": "docs", "value": "stable", "icon": "docs", "theme": "light", "style": "social", "size": "md"},
    "quality": {"label": "quality", "value": "A+", "icon": "star", "theme": "neon", "style": "pill", "size": "sm"},
}


def get_catalog():
    return {
        "themes": sorted(COLOR_THEMES.keys()),
        "styles": sorted(STYLE_MAP.keys()),
        "sizes": sorted(SIZE_MAP.keys()),
        "icons": sorted(ICON_SET.keys()),
        "palette": COLOR_PALETTE,
        "presets": BADGE_PRESETS,
    }


def resolve_preset(name: str):
    return BADGE_PRESETS.get((name or "").strip().lower(), BADGE_PRESETS["build"])
