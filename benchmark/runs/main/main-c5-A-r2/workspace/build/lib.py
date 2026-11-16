"""Tiny layout layer: every draw call writes to the PPTX *and* to a PIL preview,
so the preview shows exactly the geometry and text wrapping that the deck uses.
Text heights are measured with real Arial metrics so stacked blocks never overflow."""
import re
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.oxml.ns import qn
from PIL import Image, ImageDraw, ImageFont

DPI = 110
FONT_R = "/System/Library/Fonts/Supplemental/Arial.ttf"
FONT_B = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
LINE = 1.18          # line height multiple used for both measurement and pptx
PAD = 0.04           # text-frame inset, inches

INK = "1B1F27"; SEC = "52514E"; MUTED = "8A8984"; GRID = "DDDCD7"; PANEL = "F3F2EE"
BLUE = "2A78D6"; ORANGE = "EB6834"; GRAY = "A3A29D"; WHITE = "FFFFFF"; NAVY = "16324F"

_fonts = {}
def font(size, bold=False):
    k = (round(size * DPI / 72), bold)
    if k not in _fonts:
        _fonts[k] = ImageFont.truetype(FONT_B if bold else FONT_R, k[0])
    return _fonts[k]

def rgb(h): return RGBColor.from_string(h)
def hx(h): return "#" + h

def parse(text, color):
    """'**bold**' and '{c:HEX}..{/c}' markup -> list of (str, bold, color)."""
    runs = []
    for part in re.split(r"(\*\*.+?\*\*)", text):
        if not part:
            continue
        b = part.startswith("**") and part.endswith("**")
        runs.append((part[2:-2] if b else part, b, color))
    return runs

def wrap(runs, size, width_in):
    """Greedy word wrap over styled runs. Returns list of lines; each line list of (word, bold, color)."""
    words = []
    for t, b, c in runs:
        for i, w in enumerate(re.split(r"(\s+)", t)):
            if w == "":
                continue
            words.append((w, b, c))
    lines, cur, curw = [], [], 0.0
    maxw = (width_in - 2 * PAD) * DPI
    for w, b, c in words:
        ww = font(size, b).getlength(w)
        if w.isspace():
            if cur:
                cur.append((" ", b, c)); curw += font(size, b).getlength(" ")
            continue
        if cur and curw + ww > maxw:
            while cur and cur[-1][0] == " ":
                curw -= font(size, cur[-1][1]).getlength(" "); cur.pop()
            lines.append(cur); cur, curw = [], 0.0
        cur.append((w, b, c)); curw += ww
    while cur and cur[-1][0] == " ":
        cur.pop()
    if cur:
        lines.append(cur)
    return lines or [[]]

def text_height(paras, size, width_in, space_after=0.0):
    n = sum(len(wrap(parse(p, INK), size, width_in)) for p in paras)
    return n * size * LINE / 72 + 2 * PAD + space_after * max(0, len(paras) - 1) / 72 * 0  # inches


class Deck:
    def __init__(self):
        self.prs = Presentation()
        self.prs.slide_width = Inches(13.333)
        self.prs.slide_height = Inches(7.5)
        self.W, self.H = 13.333, 7.5
        self.images = []
        self.warnings = []

    def new_slide(self):
        s = self.prs.slides.add_slide(self.prs.slide_layouts[6])
        img = Image.new("RGB", (int(self.W * DPI), int(self.H * DPI)), "white")
        self.images.append(img)
        self.s, self.d = s, ImageDraw.Draw(img)
        self.n = len(self.images)
        return s

    # ---------- primitives ----------
    def rect(self, x, y, w, h, fill, line=None):
        if w < 0: x, w = x + w, -w
        if h < 0: y, h = y + h, -h
        sh = self.s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(max(w, 0.001)), Inches(max(h, 0.001)))
        sh.shadow.inherit = False
        if fill:
            sh.fill.solid(); sh.fill.fore_color.rgb = rgb(fill)
        else:
            sh.fill.background()
        if line:
            sh.line.color.rgb = rgb(line); sh.line.width = Pt(0.75)
        else:
            sh.line.fill.background()
        self.d.rectangle([x * DPI, y * DPI, (x + w) * DPI, (y + h) * DPI], fill=hx(fill) if fill else None,
                         outline=hx(line) if line else None)
        return sh

    def line(self, x1, y1, x2, y2, color=GRID, width=0.75, dash=False):
        c = self.s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1), Inches(x2), Inches(y2))
        c.line.color.rgb = rgb(color); c.line.width = Pt(width)
        if dash:
            ln = c.line._get_or_add_ln()
            pd = ln.makeelement(qn("a:prstDash"), {"val": "dash"}); ln.append(pd)
        px = max(1, round(width * DPI / 72))
        if dash:
            import math
            L = math.hypot(x2 - x1, y2 - y1); n = int(L / 0.08)
            for i in range(0, n, 2):
                a, b = i / n, min(1, (i + 1) / n)
                self.d.line([(x1 + (x2 - x1) * a) * DPI, (y1 + (y2 - y1) * a) * DPI,
                             (x1 + (x2 - x1) * b) * DPI, (y1 + (y2 - y1) * b) * DPI], fill=hx(color), width=px)
        else:
            self.d.line([x1 * DPI, y1 * DPI, x2 * DPI, y2 * DPI], fill=hx(color), width=px)

    def text(self, x, y, w, h, paras, size=14, color=INK, bold=False, align="l", anchor="t",
             space_after=0, check=True):
        """paras: str or list of str (each a paragraph, '**' markup for bold)."""
        if isinstance(paras, str):
            paras = [paras]
        tb = self.s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.auto_size = None
        for side in ("margin_left", "margin_right", "margin_top", "margin_bottom"):
            setattr(tf, side, Inches(PAD))
        tf.vertical_anchor = {"t": MSO_ANCHOR.TOP, "m": MSO_ANCHOR.MIDDLE, "b": MSO_ANCHOR.BOTTOM}[anchor]
        al = {"l": PP_ALIGN.LEFT, "c": PP_ALIGN.CENTER, "r": PP_ALIGN.RIGHT}[align]
        all_lines = []
        for i, p in enumerate(paras):
            para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            para.alignment = al
            para.line_spacing = Pt(size * LINE)  # exact spacing so preview == deck
            if space_after and i < len(paras) - 1:
                para.space_after = Pt(space_after)
            runs = parse(p, color)
            for t, b, c in runs:
                r = para.add_run(); r.text = t
                r.font.size = Pt(size); r.font.name = "Arial"; r.font.bold = bold or b
                r.font.color.rgb = rgb(c)
            lines = wrap([(t, bold or b, c) for t, b, c in runs], size, w)
            all_lines.append(lines)
        # preview + fit check
        lh = size * LINE / 72
        total = sum(len(l) for l in all_lines) * lh + space_after / 72 * (len(paras) - 1) + 2 * PAD
        if check and total > h + 0.02:
            self.warnings.append(f"slide {self.n}: text overflow {total:.2f}in > box {h:.2f}in: {paras[0][:50]!r}")
        if anchor == "t":
            cy = y + PAD
        elif anchor == "m":
            cy = y + (h - total) / 2 + PAD
        else:
            cy = y + h - total + PAD
        for pi, lines in enumerate(all_lines):
            for ln in lines:
                lw = sum(font(size, b).getlength(t) for t, b, c in ln) / DPI
                if align == "l": cx = x + PAD
                elif align == "c": cx = x + (w - lw) / 2
                else: cx = x + w - PAD - lw
                px = cx * DPI
                for t, b, c in ln:
                    f = font(size, bold or b)
                    self.d.text((px, (cy + (lh - size / 72) / 2) * DPI), t, font=f, fill=hx(c))
                    px += f.getlength(t)
                cy += lh
            cy += space_after / 72
        return total

    def measure(self, paras, size, w, bold=False, space_after=0):
        if isinstance(paras, str): paras = [paras]
        n = 0
        for p in paras:
            runs = [(t, bold or b, c) for t, b, c in parse(p, INK)]
            n += len(wrap(runs, size, w))
        return n * size * LINE / 72 + 2 * PAD + space_after / 72 * (len(paras) - 1)

    # ---------- composites ----------
    def bullets(self, x, y, w, items, size=14, gap=0.12, color=INK, marker="•", mcolor=BLUE, indent=0.22):
        cy = y
        for it in items:
            h = self.measure(it, size, w - indent)
            self.text(x, cy, indent, size * LINE / 72 + 2 * PAD, marker, size=size, color=mcolor, bold=True)
            self.text(x + indent, cy, w - indent, h, it, size=size, color=color)
            cy += h + gap
        return cy - gap

    def chrome(self, title, source, section=None):
        """Action title, rule, footer with source and page number."""
        th = self.measure(title, 24, 12.3, bold=True)
        self.text(0.5, 0.38, 12.3, th, title, size=24, bold=True, color=INK)
        ybar = 0.38 + max(th, 0.5) + 0.06
        self.line(0.5, ybar, 12.83, ybar, color=INK, width=1.0)
        self.line(0.5, 7.0, 12.83, 7.0, color=GRID, width=0.5)
        self.text(0.5, 7.03, 11.4, 0.42, source, size=9, color=MUTED)
        self.text(12.2, 7.04, 0.63, 0.32, str(self.n), size=9, color=MUTED, align="r")
        if section:
            self.text(0.5, 0.12, 6, 0.26, section.upper(), size=9, color=BLUE, bold=True)
        return ybar + 0.2

    def save(self, path, preview_dir):
        self.prs.save(path)
        for i, im in enumerate(self.images, 1):
            im.save(f"{preview_dir}/slide_{i:02d}.png")
