"""Design tokens: one place for theme colors, fonts, grid and type scale.

Colors and fonts: templates/themes.json (mirrors the Figma "Theme" collection).
Grid: Figma sample slide, 1280 x 720 px = 13.333 x 7.5 in (96 px per inch).
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
THEMES_PATH = os.path.join(ROOT, "templates", "themes.json")

PX = 1 / 96  # inches per Figma px

# Shared neutrals and semantic colors (Figma "Slide color").
NEUTRALS = {
    "text": "#2E3A44",
    "muted": "#6A7682",
    "gray_light": "#E3E6E9",
    "gray_mid": "#B8C1C8",
    "gray_dark": "#55636E",
    "rule": "#D5DBDF",
    "placeholder": "#9AA5AE",
    "panel": "#F1F3F4",
    "good": "#2E7D4F",
    "caution": "#D99A00",
    "caution_bg": "#FFF4D6",
    "caution_ink": "#7A5200",
    "alert": "#B4432C",
    "white": "#FFFFFF",
}

# Grid in inches. v2 density (2026-11-05), matched to 2020+ public decks:
# side margin 4.5% of width, content down to 91% of height, body 14 pt, title 25 pt.
GRID = {
    "slide_w": 13.333,
    "slide_h": 7.5,
    "margin": 58 * PX,
    "tracker_top": 24 * PX,
    "title_top": 50 * PX,
    "title_w": 1080 * PX,
    "title_h": 80 * PX,
    "unit_top": 136 * PX,
    "unit_h": 22 * PX,
    "content_top": 170 * PX,
    "content_bottom": 656 * PX,
    "gap": 22 * PX,
    "sidebar_w": 392 * PX,
    "sowhat_h": 50 * PX,
    "source_top": 684 * PX,
    "line_h": 16 * PX,
}

# Type scale in pt (Figma px * 0.75).
SIZES = {
    "title": 25,
    "cover_title": 38,
    "unit": 12,
    "tracker": 10,
    "header": 15,
    "body": 14,
    "label": 12,
    "small": 11,
    "source": 9,
    "sowhat": 15,
    "takeaway": 17,
    "big_number": 46,
    "kpi": 48,
}


def load_themes():
    with open(THEMES_PATH, encoding="utf-8") as f:
        return json.load(f)


def resolve(theme=None, font_pair=None):
    """Return a flat token dict for one theme (+ optional font-pair override)."""
    data = load_themes()
    key = theme if theme in data["themes"] else data["default_theme"]
    t = data["themes"][key]
    pair_key = font_pair if font_pair in data["font_pairs"] else (t.get("font_pair") or data["default_font_pair"])
    pair = data["font_pairs"][pair_key]
    tok = dict(NEUTRALS)
    tok.update({k: v for k, v in t.items() if isinstance(v, str) and v.startswith("#")})
    tok.update({
        "theme": key,
        "font_pair": pair_key,
        "font_title": pair["title"],
        "font_body": pair["body"],
        "bar_radius": t.get("bar_corner_radius_pt", 0),
        "dark_sidebar": t["sidebar_text"].upper() == "#FFFFFF",
    })
    return tok
