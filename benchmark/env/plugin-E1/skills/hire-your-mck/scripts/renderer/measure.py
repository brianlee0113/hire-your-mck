"""Text measurement with real font metrics, so layout never guesses how a line wraps.

PowerPoint wraps on word boundaries inside the text box width; this module does the same with the
actual font files (Pillow). If a font file is missing it falls back to a metric-compatible font
(Liberation Sans for Arial, etc.) and, as a last resort, to an average-width estimate.
"""
import functools
import glob
import math
import os

try:
    from PIL import ImageFont
except ImportError:  # measurement falls back to estimates
    ImageFont = None

LINE = 1.2  # PowerPoint line pitch for single spacing, as a multiple of the font size

_DIRS = ["/System/Library/Fonts/Supplemental", "/System/Library/Fonts", "/Library/Fonts",
         os.path.expanduser("~/Library/Fonts"), "/usr/share/fonts", "/usr/local/share/fonts",
         os.path.expanduser("~/.fonts"), "C:/Windows/Fonts",
         # Office for Mac keeps Calibri and Aptos inside the app bundles
         "/Applications/Microsoft PowerPoint.app/Contents/Resources/DFonts",
         "/Applications/Microsoft Word.app/Contents/Resources/DFonts"]

# family -> candidate file names (regular, bold). First match wins; later entries are metric-compatible stand-ins.
_FILES = {
    "arial": (["Arial.ttf", "arial.ttf", "LiberationSans-Regular.ttf", "Arimo-Regular.ttf"],
              ["Arial Bold.ttf", "arialbd.ttf", "LiberationSans-Bold.ttf", "Arimo-Bold.ttf"]),
    "georgia": (["Georgia.ttf", "georgia.ttf", "Gelasio-Regular.ttf", "DejaVuSerif.ttf"],
                ["Georgia Bold.ttf", "georgiab.ttf", "Gelasio-Bold.ttf", "DejaVuSerif-Bold.ttf"]),
    "calibri": (["Calibri.ttf", "calibri.ttf", "Carlito-Regular.ttf", "LiberationSans-Regular.ttf"],
                ["Calibri Bold.ttf", "calibrib.ttf", "Calibrib.ttf", "Carlito-Bold.ttf", "LiberationSans-Bold.ttf"]),
    "aptos": (["Aptos.ttf", "aptos.ttf", "LiberationSans-Regular.ttf"],
              ["Aptos-Bold.ttf", "Aptos Bold.ttf", "aptos-bold.ttf", "LiberationSans-Bold.ttf"]),
    "aptos serif": (["Aptos Serif.ttf", "AptosSerif.ttf", "Georgia.ttf", "Gelasio-Regular.ttf"],
                    ["Aptos Serif Bold.ttf", "AptosSerif-Bold.ttf", "Georgia Bold.ttf", "Gelasio-Bold.ttf"]),
}


@functools.lru_cache(maxsize=None)
def _find(name):
    for d in _DIRS:
        if not os.path.isdir(d):
            continue
        p = os.path.join(d, name)
        if os.path.exists(p):
            return p
        hits = glob.glob(os.path.join(d, "**", name), recursive=True)
        if hits:
            return hits[0]
    return None


@functools.lru_cache(maxsize=None)
def _font(family, bold):
    if ImageFont is None:
        return None
    names = _FILES.get((family or "arial").lower(), _FILES["arial"])[1 if bold else 0]
    for n in names:
        p = _find(n)
        if p:
            return ImageFont.truetype(p, 200)  # measure at 200 px, scale to points
    return None


def width_pt(text, family, size, bold=False):
    """Width of a run in points."""
    f = _font(family, bold)
    if f is None:
        return len(text) * size * (0.52 if bold else 0.48) * (1.08 if (family or "").lower() == "georgia" else 1.0)
    return f.getlength(text) * size / 200.0


def wrap(runs, width_in):
    """Greedy word wrap of styled runs [(text, family, size, bold)] in a box width_in inches wide.
    Returns the lines, each a list of (text, family, size, bold)."""
    width = width_in * 72.0
    tokens = []
    for text, fam, size, bold in runs:
        parts = text.replace("\t", " ").split(" ")
        for k, part in enumerate(parts):
            tokens.append([part, fam, size, bold, k < len(parts) - 1])  # last flag: a space follows
    lines, cur, cur_w = [], [], 0.0
    for word, fam, size, bold, space in tokens:
        w = width_pt(word, fam, size, bold)
        sp = width_pt(" ", fam, size, bold) if space else 0.0
        if cur and cur_w + w > width + 0.01:
            lines.append(cur)
            cur, cur_w = [], 0.0
        while not cur and w > width and len(word) > 1:  # a word longer than the line breaks mid-word
            cut = max(1, int(len(word) * width / w))
            lines.append([(word[:cut], fam, size, bold)])
            word = word[cut:]
            w = width_pt(word, fam, size, bold)
        cur.append((word, fam, size, bold))
        cur_w += w + sp
    if cur:
        lines.append(cur)
    return lines or [[("", runs[0][1] if runs else "arial", runs[0][2] if runs else 12, False)]]


@functools.lru_cache(maxsize=None)
def line_pitch(family, bold=False):
    """Single-spaced line pitch as a multiple of the size: 1.2, or the font's own ascent + descent when taller
    (Calibri and Aptos run about 1.22)."""
    f = _font(family, bold)
    if f is None:
        return LINE
    a, d = f.getmetrics()
    return max(LINE, (a + d) / 200.0)


def para_height(runs, width_in, line_spacing=1.0):
    """Height in inches of one paragraph of styled runs."""
    lines = wrap(runs, width_in)
    h = 0.0
    for ln in lines:
        size = max((r[2] for r in ln), default=12)
        pitch = max((line_pitch(r[1], r[3]) for r in ln), default=LINE)
        h += size * pitch * line_spacing / 72.0
    return h


def lines(text, width_in, family, size, bold=False):
    return len(wrap([(text, family, size, bold)], width_in))


def height(text, width_in, family, size, bold=False, line_spacing=1.0):
    return para_height([(text, family, size, bold)], width_in, line_spacing)


def fit(text_list, width_in, height_in, family, size, min_size=9, bold=False, line_spacing=1.0, gap=0.0):
    """Largest size (0.5 pt steps) at which the paragraphs fit width x height."""
    while size > min_size:
        h = sum(height(t, width_in, family, size, bold, line_spacing) for t in text_list) + gap * max(0, len(text_list) - 1)
        if h <= height_in:
            return size
        size -= 0.5
    return min_size


def available():
    """True when real font metrics are in use for the default pair."""
    return _font("arial", False) is not None and _font("georgia", True) is not None
