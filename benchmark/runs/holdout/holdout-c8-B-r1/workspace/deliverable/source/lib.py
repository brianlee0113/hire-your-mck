"""Slide-building helpers: python-pptx output + PIL preview + text-fit checks."""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn
from PIL import Image, ImageDraw, ImageFont
import copy

FONT = "Arial"
F_REG = "/System/Library/Fonts/Supplemental/Arial.ttf"
F_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"

INK = "0B0B0B"; INK2 = "52514E"; MUTED = "898781"; GRID = "E1E0D9"; AXIS = "C3C2B7"
NAVY = "0D366B"; BLUE = "2A78D6"; ORANGE = "EB6834"; AQUA = "1BAF7A"; GRAY = "A9A8A2"
GOOD = "0CA30C"; WARN = "FAB219"; CRIT = "D03B3B"; GOODTXT = "006300"
PALE = "F4F3EF"; PALEBLUE = "EAF2FC"; WHITE = "FFFFFF"

SW, SH = 13.333, 7.5
PX = 100  # preview px per inch
LINE_K = 1.2  # line height multiple used for fit checks

_fonts = {}
def font(bold, size_pt):
    key = (bold, round(size_pt * 4))
    if key not in _fonts:
        # size in preview px: pt/72 in * PX
        _fonts[key] = ImageFont.truetype(F_BOLD if bold else F_REG, max(1, int(round(size_pt / 72 * PX * 4))))
    return _fonts[key]  # 4x oversampled font for measurement

def text_w_in(s, bold, size):
    f = font(bold, size)
    return f.getlength(s) / 4 / PX

def wrap(s, bold, size, width_in):
    lines = []
    for hard in s.split("\n"):
        words = hard.split(" ")
        cur = ""
        for w in words:
            t = (cur + " " + w) if cur else w
            if text_w_in(t, bold, size) <= width_in or not cur:
                cur = t
            else:
                lines.append(cur); cur = w
        lines.append(cur)
    return lines

def rgb(h):
    return RGBColor.from_string(h)

class Deck:
    def __init__(self):
        self.prs = Presentation()
        self.prs.slide_width = Inches(SW); self.prs.slide_height = Inches(SH)
        self.slides = []
        self.warnings = []

    def new(self):
        s = Slide(self, self.prs.slides.add_slide(self.prs.slide_layouts[6]), len(self.slides) + 1)
        self.slides.append(s)
        return s

    def save(self, path):
        self.prs.save(path)

    def previews(self, outdir):
        for s in self.slides:
            s.render(f"{outdir}/slide_{s.n:02d}.png")

def norm_paras(paras, size, color, bold):
    """paras: str | list of items; item: str | dict(runs=[(text,bold,color)], text=, bold=, color=, size=, bullet=, sb=, align=)"""
    if isinstance(paras, str):
        paras = [paras]
    out = []
    for p in paras:
        if isinstance(p, str):
            p = {"text": p}
        p = dict(p)
        sz = p.get("size", size)
        if "runs" not in p:
            p["runs"] = [(p.get("text", ""), p.get("bold", bold), p.get("color", color))]
        p["runs"] = [(r[0], r[1] if len(r) > 1 else bold, r[2] if len(r) > 2 else color) for r in p["runs"]]
        p["size"] = sz
        p.setdefault("bullet", False)
        p.setdefault("sb", 0)
        out.append(p)
    return out

class Slide:
    def __init__(self, deck, slide, n):
        self.deck, self.s, self.n = deck, slide, n
        self.els = []

    # ---------- primitives ----------
    def rect(self, x, y, w, h, fill=None, line=None, lw=0.75, shape=MSO_SHAPE.RECTANGLE):
        sh = self.s.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
        if fill: sh.fill.solid(); sh.fill.fore_color.rgb = rgb(fill)
        else: sh.fill.background()
        if line: sh.line.color.rgb = rgb(line); sh.line.width = Pt(lw)
        else: sh.line.fill.background()
        sh.shadow.inherit = False
        if shape == MSO_SHAPE.ROUNDED_RECTANGLE:
            sh.adjustments[0] = 0.15
        self.els.append(("rect", x, y, w, h, fill, line))
        return sh

    def hline(self, x, y, w, color=AXIS, lw=0.75):
        c = self.s.shapes.add_connector(1, Inches(x), Inches(y), Inches(x + w), Inches(y))
        c.line.color.rgb = rgb(color); c.line.width = Pt(lw)
        self.els.append(("line", x, y, x + w, y, color))

    def vline(self, x, y, h, color=AXIS, lw=0.75):
        c = self.s.shapes.add_connector(1, Inches(x), Inches(y), Inches(x), Inches(y + h))
        c.line.color.rgb = rgb(color); c.line.width = Pt(lw)
        self.els.append(("line", x, y, x, y + h, color))

    def text(self, x, y, w, h, paras, size=12, color=INK, bold=False, align="l", anchor="t",
             fill=None, line=None, inset=0.06, shape=None, name=""):
        P = norm_paras(paras, size, color, bold)
        if shape is not None or fill or line:
            sh = self.s.shapes.add_shape(shape or MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
            if fill: sh.fill.solid(); sh.fill.fore_color.rgb = rgb(fill)
            else: sh.fill.background()
            if line: sh.line.color.rgb = rgb(line); sh.line.width = Pt(0.75)
            else: sh.line.fill.background()
            sh.shadow.inherit = False
            if shape == MSO_SHAPE.ROUNDED_RECTANGLE:
                sh.adjustments[0] = 0.2
        else:
            sh = self.s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
        tf = sh.text_frame
        tf.word_wrap = True
        tf.auto_size = None
        for side in ("left", "right", "top", "bottom"):
            setattr(tf, f"margin_{side}", Inches(inset))
        tf.vertical_anchor = {"t": MSO_ANCHOR.TOP, "m": MSO_ANCHOR.MIDDLE, "b": MSO_ANCHOR.BOTTOM}[anchor]
        al = {"l": PP_ALIGN.LEFT, "c": PP_ALIGN.CENTER, "r": PP_ALIGN.RIGHT}
        BUL_IN = 0.18
        for i, p in enumerate(P):
            para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            para.alignment = al[p.get("align", align)]
            if p["sb"]:
                para.space_before = Pt(p["sb"])
            para.line_spacing = 1.0
            for (t, b, c) in p["runs"]:
                r = para.add_run(); r.text = t
                r.font.size = Pt(p["size"]); r.font.bold = b; r.font.name = FONT
                r.font.color.rgb = rgb(c)
            pPr = para._p.get_or_add_pPr()
            if p["bullet"]:
                pPr.set("marL", str(int(Inches(BUL_IN)))); pPr.set("indent", str(-int(Inches(BUL_IN))))
                bf = pPr.makeelement(qn("a:buFont"), {"typeface": "Arial"}); pPr.append(bf)
                bc = pPr.makeelement(qn("a:buChar"), {"char": "•"}); pPr.append(bc)
            else:
                pPr.append(pPr.makeelement(qn("a:buNone"), {}))
        # ---- fit check ----
        usable_w = w - 2 * inset
        total = 0.0
        lines_out = []
        for p in P:
            full = "".join(r[0] for r in p["runs"])
            anyb = any(r[1] for r in p["runs"])
            ww = usable_w - (BUL_IN if p["bullet"] else 0)
            ls = wrap(full, anyb, p["size"], ww * 0.97 - 0.02)
            total += p["sb"] / 72
            lh = p["size"] / 72 * LINE_K
            lines_out.append((p, ls, lh))
            total += len(ls) * lh
        if total > h - 2 * inset + 0.01:
            self.deck.warnings.append(f"slide {self.n}: text overflow {total:.2f}in > {h - 2*inset:.2f}in  '{full[:50]}'")
        self.els.append(("text", x, y, w, h, fill, line, lines_out, inset, anchor, align, total))
        return sh

    def chart_placeholder(self, x, y, w, h, label):
        self.els.append(("chart", x, y, w, h, label))

    # ---------- preview ----------
    def render(self, path):
        im = Image.new("RGB", (int(SW * PX), int(SH * PX)), "white")
        d = ImageDraw.Draw(im)
        def P(v): return int(round(v * PX))
        for e in self.els:
            if e[0] == "rect":
                _, x, y, w, h, fill, line = e
                d.rectangle([P(x), P(y), P(x + w), P(y + h)], fill=("#" + fill) if fill else None,
                            outline=("#" + line) if line else None)
            elif e[0] == "line":
                _, x1, y1, x2, y2, c = e
                d.line([P(x1), P(y1), P(x2), P(y2)], fill="#" + c, width=1)
            elif e[0] == "chart":
                _, x, y, w, h, label = e
                d.rectangle([P(x), P(y), P(x + w), P(y + h)], outline="#2A78D6")
                d.text((P(x) + 6, P(y) + 6), "CHART: " + label, fill="#2A78D6",
                       font=ImageFont.truetype(F_REG, 12))
            elif e[0] == "text":
                _, x, y, w, h, fill, line, lines_out, inset, anchor, align, total = e
                if fill or line:
                    d.rectangle([P(x), P(y), P(x + w), P(y + h)], fill=("#" + fill) if fill else None,
                                outline=("#" + line) if line else None)
                if total > h - 2 * inset + 0.01:
                    d.rectangle([P(x), P(y), P(x + w), P(y + h)], outline="#FF00FF", width=3)
                cy = y + inset
                if anchor == "m": cy = y + (h - total) / 2
                if anchor == "b": cy = y + h - inset - total
                for p, ls, lh in lines_out:
                    cy += p["sb"] / 72
                    r0 = p["runs"][0]
                    anyb = any(r[1] for r in p["runs"])
                    f = ImageFont.truetype(F_BOLD if anyb else F_REG, max(1, int(round(p["size"] / 72 * PX))))
                    for li, ln in enumerate(ls):
                        xx = x + inset + (0.18 if p["bullet"] else 0)
                        tw = f.getlength(ln) / PX
                        a = p.get("align", align)
                        if a == "c": xx = x + (w - tw) / 2
                        if a == "r": xx = x + w - inset - tw
                        if p["bullet"] and li == 0:
                            d.text((P(x + inset), P(cy)), "•", fill="#" + r0[2], font=f)
                        d.text((P(xx), P(cy)), ln, fill="#" + r0[2], font=f)
                        cy += lh
        im.save(path)
