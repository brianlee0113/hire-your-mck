"""Minimal two-backend slide engine: one layout spec -> PPTX (python-pptx) and PNG preview (PIL).
Coordinates in inches on a 13.333 x 7.5 slide. Text supports **bold** markup and bullet paragraphs."""
import re
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.oxml.ns import qn
from PIL import Image, ImageDraw, ImageFont
from lxml import etree

W, H = 13.333, 7.5
DPI = 110
FONT_DIR = "/System/Library/Fonts/Supplemental/"
FONTS = {(False, False): "Arial.ttf", (True, False): "Arial Bold.ttf",
         (False, True): "Arial Italic.ttf", (True, True): "Arial Bold Italic.ttf"}
_fcache = {}
LINE = 1.18          # line height multiple used for fit checks and preview
WARNINGS = []


def font(size, bold=False, italic=False, scale=DPI / 72):
    k = (round(size * scale, 2), bold, italic)
    if k not in _fcache:
        _fcache[k] = ImageFont.truetype(FONT_DIR + FONTS[(bold, italic)], max(1, int(round(size * scale))))
    return _fcache[k]


def parse_runs(text, bold=False):
    """'a **b** c' -> [(a,False),(b,True),(c,False)]"""
    out = []
    parts = re.split(r"(\*\*.+?\*\*)", text)
    for p in parts:
        if not p:
            continue
        if p.startswith("**") and p.endswith("**"):
            out.append((p[2:-2], True))
        else:
            out.append((p, bold))
    return out


def hex2rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


class Text:
    def __init__(self, x, y, w, h, text, size=12, bold=False, italic=False, color="1F1F1F", align="l",
                 valign="t", bullet=False, space=4, fill=None, line=None, pad=0.04, name=None, check=True):
        self.__dict__.update(locals())
        del self.__dict__["self"]

    # ---- layout via PIL metrics (used for preview and fit check)
    def paragraphs(self):
        paras = []
        for raw in self.text.split("\n"):
            b = self.bullet
            lvl = 0
            if raw.startswith("- "):
                b, raw = True, raw[2:]
            elif raw.startswith("-- "):
                b, raw, lvl = True, raw[3:], 1
            elif raw.startswith("~ "):   # explicit non-bullet in bullet box
                b, raw = False, raw[2:]
            paras.append((raw, b, lvl))
        return paras

    def wrap(self, scale=DPI / 72):
        px = DPI
        avail = (self.w - 2 * self.pad) * px * 0.965
        lines = []  # (indent_px, [(word, bold)], is_first, bullet, para_index)
        for pi, (raw, b, lvl) in enumerate(self.paragraphs()):
            indent = (0.17 + 0.2 * lvl) * px if b else 0
            words = []
            for t, bo in parse_runs(raw, self.bold):
                for i, wd in enumerate(re.split(r"(\s+)", t)):
                    if wd == "":
                        continue
                    words.append((wd, bo))
            cur, curw = [], 0
            first = True
            for wd, bo in words:
                f = font(self.size, bo, self.italic, scale)
                ww = f.getlength(wd)
                if wd.isspace():
                    if cur:
                        cur.append((wd, bo)); curw += ww
                    continue
                if cur and curw + ww > avail - indent:
                    while cur and cur[-1][0].isspace():
                        curw -= font(self.size, cur[-1][1], self.italic, scale).getlength(cur[-1][0]); cur.pop()
                    lines.append((indent, cur, first, b, pi, lvl))
                    first = False
                    cur, curw = [], 0
                cur.append((wd, bo)); curw += ww
            lines.append((indent, cur, first, b, pi, lvl))
        return lines

    def text_height(self):
        lines = self.wrap()
        n_para = len(self.paragraphs())
        lh = self.size * LINE / 72
        return len(lines) * lh + (n_para - 1) * self.space / 72

    def check_fit(self, slide_no):
        if not self.check:
            return
        th = self.text_height() + 2 * 0.03
        if th > self.h + 0.01:
            WARNINGS.append(f"slide {slide_no}: text overflows box by {th - self.h:.2f}in: '{self.text[:60]}'")


class Rect:
    def __init__(self, x, y, w, h, fill="FFFFFF", line=None, lw=0.75, shape="rect"):
        self.__dict__.update(locals()); del self.__dict__["self"]


class Line:
    def __init__(self, x1, y1, x2, y2, color="BFBFBF", lw=0.75, dash=False):
        self.__dict__.update(locals()); del self.__dict__["self"]


class Slide:
    def __init__(self):
        self.items = []

    def add(self, *items):
        for it in items:
            self.items.append(it)
        return items[0] if len(items) == 1 else items

    def text(self, *a, **k):
        return self.add(Text(*a, **k))

    def rect(self, *a, **k):
        return self.add(Rect(*a, **k))

    def line(self, *a, **k):
        return self.add(Line(*a, **k))


# ---------------- PPTX backend
def _set_bullet(p, lvl):
    pPr = p._p.get_or_add_pPr()
    mar = int(Inches(0.17 + 0.2 * lvl))
    pPr.set("marL", str(mar))
    pPr.set("indent", str(-int(Inches(0.17))))
    for tag in ("a:buNone", "a:buChar", "a:buFont"):
        for el in pPr.findall(qn(tag)):
            pPr.remove(el)
    buFont = etree.SubElement(pPr, qn("a:buFont")); buFont.set("typeface", "Arial")
    buChar = etree.SubElement(pPr, qn("a:buChar")); buChar.set("char", "•" if lvl == 0 else "–")


def _no_bullet(p):
    pPr = p._p.get_or_add_pPr()
    etree.SubElement(pPr, qn("a:buNone"))


def to_pptx(slides, path, notes=None):
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(W), Inches(H)
    blank = prs.slide_layouts[6]
    for si, s in enumerate(slides):
        sl = prs.slides.add_slide(blank)
        for it in s.items:
            if isinstance(it, Rect):
                shp = sl.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE if it.shape == "round" else
                                          (MSO_SHAPE.OVAL if it.shape == "oval" else MSO_SHAPE.RECTANGLE),
                                          Inches(it.x), Inches(it.y), Inches(it.w), Inches(it.h))
                if it.shape == "round":
                    shp.adjustments[0] = 0.12
                if it.fill:
                    shp.fill.solid(); shp.fill.fore_color.rgb = RGBColor.from_string(it.fill)
                else:
                    shp.fill.background()
                if it.line:
                    shp.line.color.rgb = RGBColor.from_string(it.line); shp.line.width = Pt(it.lw)
                else:
                    shp.line.fill.background()
                shp.shadow.inherit = False
                shp.text_frame.text = ""
            elif isinstance(it, Line):
                c = sl.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(it.x1), Inches(it.y1), Inches(it.x2), Inches(it.y2))
                c.line.color.rgb = RGBColor.from_string(it.color); c.line.width = Pt(it.lw)
                if it.dash:
                    from pptx.enum.dml import MSO_LINE_DASH_STYLE
                    c.line.dash_style = MSO_LINE_DASH_STYLE.DASH
            elif isinstance(it, Text):
                tb = sl.shapes.add_textbox(Inches(it.x), Inches(it.y), Inches(it.w), Inches(it.h))
                if it.name:
                    tb.name = it.name
                tf = tb.text_frame
                tf.word_wrap = True
                tf.auto_size = None
                tf.margin_left = tf.margin_right = Inches(it.pad)
                tf.margin_top = tf.margin_bottom = Inches(0.03)
                tf.vertical_anchor = {"t": MSO_ANCHOR.TOP, "m": MSO_ANCHOR.MIDDLE, "b": MSO_ANCHOR.BOTTOM}[it.valign]
                if it.fill:
                    tb.fill.solid(); tb.fill.fore_color.rgb = RGBColor.from_string(it.fill)
                if it.line:
                    tb.line.color.rgb = RGBColor.from_string(it.line); tb.line.width = Pt(0.75)
                for pi, (raw, b, lvl) in enumerate(it.paragraphs()):
                    p = tf.paragraphs[0] if pi == 0 else tf.add_paragraph()
                    p.alignment = {"l": PP_ALIGN.LEFT, "c": PP_ALIGN.CENTER, "r": PP_ALIGN.RIGHT}[it.align]
                    p.line_spacing = 1.0
                    if pi > 0:
                        p.space_before = Pt(it.space)
                    if b:
                        _set_bullet(p, lvl)
                    else:
                        _no_bullet(p)
                    for t, bo in parse_runs(raw, it.bold):
                        r = p.add_run(); r.text = t
                        r.font.name = "Arial"; r.font.size = Pt(it.size); r.font.bold = bo
                        r.font.italic = it.italic
                        r.font.color.rgb = RGBColor.from_string(it.color)
        if notes and notes[si]:
            sl.notes_slide.notes_text_frame.text = notes[si]
    prs.save(path)


# ---------------- PNG backend
def to_png(slide, path, slide_no=0):
    px = DPI
    img = Image.new("RGB", (int(W * px), int(H * px)), "white")
    d = ImageDraw.Draw(img)
    for it in slide.items:
        if isinstance(it, Rect):
            box = [it.x * px, it.y * px, (it.x + it.w) * px, (it.y + it.h) * px]
            kw = dict(fill=hex2rgb(it.fill) if it.fill else None,
                      outline=hex2rgb(it.line) if it.line else None, width=max(1, int(it.lw * px / 72)))
            if it.shape == "round":
                d.rounded_rectangle(box, radius=min(it.w, it.h) * px * 0.12, **kw)
            elif it.shape == "oval":
                d.ellipse(box, **kw)
            else:
                d.rectangle(box, **kw)
        elif isinstance(it, Line):
            d.line([it.x1 * px, it.y1 * px, it.x2 * px, it.y2 * px], fill=hex2rgb(it.color), width=max(1, int(it.lw * px / 72)))
        elif isinstance(it, Text):
            it.check_fit(slide_no)
            if it.fill or it.line:
                d.rectangle([it.x * px, it.y * px, (it.x + it.w) * px, (it.y + it.h) * px],
                            fill=hex2rgb(it.fill) if it.fill else None, outline=hex2rgb(it.line) if it.line else None)
            lines = it.wrap()
            lh = it.size * LINE / 72 * px
            th = it.text_height() * px
            top = it.y * px + 0.03 * px
            if it.valign == "m":
                top = it.y * px + (it.h * px - th) / 2
            elif it.valign == "b":
                top = (it.y + it.h) * px - th - 0.03 * px
            yy = top
            last_p = 0
            col = hex2rgb(it.color)
            for (indent, words, first, b, pi, lvl) in lines:
                if pi != last_p:
                    yy += it.space / 72 * px; last_p = pi
                lw = sum(font(it.size, bo, it.italic).getlength(wd) for wd, bo in words)
                x0 = it.x * px + it.pad * px
                availw = (it.w - 2 * it.pad) * px
                if it.align == "c":
                    x0 = x0 + (availw - lw - indent) / 2
                elif it.align == "r":
                    x0 = x0 + availw - lw - indent
                if b and first:
                    d.text((x0 + 0.2 * lvl * px, yy + lh * 0.08), "•" if lvl == 0 else "–", font=font(it.size), fill=col)
                xx = x0 + indent
                for wd, bo in words:
                    f = font(it.size, bo, it.italic)
                    d.text((xx, yy + lh * 0.08), wd, font=f, fill=col)
                    xx += f.getlength(wd)
                yy += lh
    img.save(path)
    return img
