"""Design configuration built from our own template (D8, D9, D10).

Colors and fonts come from templates/themes.json (mirrors the Figma "Theme"
variable collection). The layout grid comes from the Figma "Slide layout"
tokens and sample slides (1280 x 720 px frame = 13.33 x 7.5 in, 96 px/in).
No value here comes from a company template.
"""
import json
import os

from pptx.dml.color import RGBColor
from pptx.util import Inches, Pt

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
THEMES_PATH = os.path.join(BASE_DIR, "templates", "themes.json")

DEFAULT_SOURCE = "Source: Team analysis"


def _rgb(hex_str):
    """Convert a hex color string to RGBColor."""
    h = hex_str.lstrip("#")
    return RGBColor(int(h[:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def _px(px):
    """Figma px on the 1280 x 720 frame -> inches."""
    return Inches(px / 96)


def load_themes():
    with open(THEMES_PATH, encoding="utf-8") as f:
        return json.load(f)


# Neutrals and semantic colors shared by every theme (Figma "Slide color").
NEUTRALS = {
    "text": "2E3A44",
    "muted": "6A7682",
    "gray_light": "E3E6E9",
    "gray_mid": "B8C1C8",
    "gray_dark": "55636E",
    "rule": "D5DBDF",
    "placeholder": "9AA5AE",
    "good": "2E7D4F",
    "caution": "D99A00",
    "alert": "B4432C",
}

# Layout grid (Figma page 02 Sample deck, slide 1).
GRID = {
    "slide_width": Inches(13.333),
    "slide_height": Inches(7.5),
    "margin_left": _px(40),
    "margin_right": _px(40),
    "tracker_top": _px(26),
    "title_left": _px(40),
    "title_top": _px(48),
    "title_width": _px(1100),
    "title_height": _px(76),          # two lines of 24 pt (A-03)
    "subtitle_top": _px(138),         # unit line: "**Metric**, unit, period"
    "subtitle_height": _px(20),
    "content_top": _px(170),
    "content_bottom": _px(640),
    "content_gap": _px(24),
    "sidebar_width": _px(360),        # takeaway sidebar (A-11)
    "footnote_top": _px(660),
    "footnote_width": _px(1100),
    "footnote_height": _px(14),
    "source_top": _px(682),
    "source_width": _px(1100),
    "source_height": _px(14),
}

# Type scale (Figma text styles, px * 0.75 = pt).
SIZES = {
    "size_title": Pt(24),
    "size_subtitle": Pt(11),
    "size_section_header": Pt(14),
    "size_body": Pt(13),
    "size_label": Pt(11),
    "size_source": Pt(8),
    "size_callout": Pt(42),
}


def load(theme=None, font_pair=None):
    """Return the design config for a theme.

    theme: key in templates/themes.json (default: navy). Unknown keys fall back
        to the default with a warning, so the v1 CLI's --project still works.
    font_pair: optional override of the theme's font pair (D10).
    """
    data = load_themes()
    themes = data["themes"]
    if not theme or theme not in themes:
        if theme:
            print(f"Warning: theme '{theme}' not found, using '{data['default_theme']}'")
        theme = data["default_theme"]
    t = themes[theme]

    pair_key = font_pair or t.get("font_pair") or data["default_font_pair"]
    if pair_key not in data["font_pairs"]:
        print(f"Warning: font pair '{pair_key}' not found, using '{data['default_font_pair']}'")
        pair_key = data["default_font_pair"]
    pair = data["font_pairs"][pair_key]
    dark_sidebar = t["sidebar_text"].upper() == "#FFFFFF"

    cfg = {
        "theme": theme,
        "font_pair": pair_key,
        "template_path": None,        # blank 16:9 deck; no company master
        "layout_default": 5,          # python-pptx default "Title Only"
        "layout_title": 0,

        "font_title": pair["title"],
        "font_body": pair["body"],
        "font_source": pair["body"],
        "font_accent": pair["title"],
        "font_fallback": pair.get("fallback"),

        "color_title": _rgb(t["title"]),
        "color_primary": _rgb(t["primary"]),
        "color_highlight": _rgb(t["highlight"]),
        "color_accent": _rgb(t["highlight"]),
        "color_other_bars": _rgb(t["other_bars"]),
        "color_sidebar": _rgb(t["sidebar"]),
        "color_sidebar_text": _rgb(t["sidebar_text"]),
        "color_big_number": _rgb(t["big_number"]),
        "color_text": _rgb(NEUTRALS["text"]),
        "color_muted": _rgb(NEUTRALS["muted"]),
        "color_white": _rgb("FFFFFF"),
        "color_gray_light": _rgb(NEUTRALS["gray_light"]),
        "color_gray_mid": _rgb(NEUTRALS["gray_mid"]),
        "color_gray_dark": _rgb(NEUTRALS["gray_dark"]),
        "color_rule": _rgb(NEUTRALS["rule"]),
        "color_placeholder": _rgb(NEUTRALS["placeholder"]),
        "color_bg_subtle": _rgb("F1F3F4") if dark_sidebar else _rgb(t["sidebar"]),
        "color_good": _rgb(NEUTRALS["good"]),
        "color_caution": _rgb(NEUTRALS["caution"]),
        "color_alert": _rgb(NEUTRALS["alert"]),

        # One highlight, everything else neutral (A-02). Extra series stay grey.
        "chart_colors": [
            _rgb(t["other_bars"]), _rgb(t["highlight"]), _rgb(t["primary"]),
            _rgb(NEUTRALS["gray_dark"]), _rgb(NEUTRALS["gray_mid"]), _rgb(NEUTRALS["gray_light"]),
        ],
        "bar_corner_radius_pt": t.get("bar_corner_radius_pt", 0),
    }
    cfg.update(GRID)
    cfg.update(SIZES)
    return cfg
