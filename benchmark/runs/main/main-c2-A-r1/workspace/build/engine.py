"""Tiny layout engine: one element model rendered to both PPTX (python-pptx) and PNG (PIL) for QA.

All geometry is in inches. Text uses Arial in both renderers so wrapping checks are meaningful.
"""
import re
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.oxml.ns import qn
from PIL import Image, ImageDraw, ImageFont

W, H = 13.333, 7.5
FONT_DIR = "/System/Library/Fonts/Supplemental/"
_font_cache = {}
LINE_H = 1.2  # line height as multiple of font size (conservative vs PowerPoint single spacing)
INSET = 0.04  # text box inset, inches


def font(size, bold=False, scale=100):
    key = (size, bold, scale)
    if key not in _font_cache:
        path = FONT_DIR + ("Arial Bold.ttf" if bold else "Arial.ttf")
        _font_cache[key] = ImageFont.truetype(path, max(1, round(size / 72 * scale)))
    return _font_cache[key]


def hexrgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def parse_runs(s, color, bold=False):
    """'plain **bold** plain' -> [(text, bold, color)]; '[[c=#hex]]text[[/c]]' also supported."""
    out = []
    for part in re.split(r"(\*\*.+?\*\*)", s):
        if not part:
            continue
        if part.startswith("**") and part.endswith("**"):
            out.append((part[2:-2], True, color))
        else:
            out.append((part, bold, color))
    return out


class Text:
    def __init__(self, x, y, w, h, paras, size=12, color="#0b0b0b", bold=False, align="l",
                 valign="t", fill=None, line=None, inset=INSET, name=None):
        self.x, self.y, self.w, self.h = x, y, w, h
        self.size, self.color, self.bold, self.align, self.valign = size, color, bold, align, valign
        self.fill, self.line, self.inset, self.name = fill, line, inset, name
        if isinstance(paras, str):
            paras = [paras]
        self.paras = []
        for p in paras:
            if isinstance(p, str):
                p = {"t": p}
            p = dict(p)
            p.setdefault("bullet", False)
            p.setdefault("size", size)
            p.setdefault("color", color)
            p.setdefault("bold", bold)
            p.setdefault("before", 0)
            p.setdefault("align", align)
            p["runs"] = parse_runs(p["t"], p["color"], p["bold"])
            self.paras.append(p)


class Rect:
    def __init__(self, x, y, w, h, fill=None, line=None, lw=0.75, shape="rect"):
        self.x, self.y, self.w, self.h, self.fill, self.line, self.lw, self.shape = x, y, w, h, fill, line, lw, shape


class Line:
    def __init__(self, x1, y1, x2, y2, color="#9a9893", lw=0.75, dash=False):
        self.x1, self.y1, self.x2, self.y2, self.color, self.lw, self.dash = x1, y1, x2, y2, color, lw, dash


class Slide:
    def __init__(self):
        self.els = []
        self.notes = ""

    def add(self, *els):
        self.els.extend(els)
        return els[0] if len(els) == 1 else els


BULLET_INDENT = 0.18


# ---------------------------------------------------------------- PIL measurement / render
def layout_text(t, scale=100):
    """Return list of lines: (y_offset_in, x_offset_in, [(text, bold, color, size)]) and total height."""
    lines = []
    y = 0.0
    avail_w = t.w - 2 * t.inset
    for pi, p in enumerate(t.paras):
        size = p["size"]
        lh = size / 72 * LINE_H
        if pi > 0:
            y += p["before"] / 72
        indent = BULLET_INDENT if p["bullet"] else 0.0
        width = avail_w - indent
        # tokenise into words with style
        tokens = []
        for text, b, c in p["runs"]:
            for w_ in re.split(r"(\s+)", text):
                if w_ == "":
                    continue
                tokens.append((w_, b, c))
        cur, cur_w = [], 0.0
        para_lines = []
        for tok, b, c in tokens:
            tw = font(size, b, scale).getlength(tok) / scale
            if tok.isspace():
                if cur:
                    cur.append((tok, b, c, size))
                    cur_w += tw
                continue
            if cur and cur_w + tw > width:
                # strip trailing space
                while cur and cur[-1][0].isspace():
                    cur_w -= font(size, cur[-1][1], scale).getlength(cur[-1][0]) / scale
                    cur.pop()
                para_lines.append((cur, cur_w))
                cur, cur_w = [], 0.0
            cur.append((tok, b, c, size))
            cur_w += tw
        while cur and cur[-1][0].isspace():
            cur.pop()
        para_lines.append((cur, sum(font(s, b, scale).getlength(x) / scale for x, b, c, s in cur)))
        for li, (ln, lw) in enumerate(para_lines):
            lines.append({"y": y, "indent": indent, "runs": ln, "w": lw, "size": size,
                          "bullet": p["bullet"] and li == 0, "align": p["align"], "avail": width,
                          "color": p["color"]})
            y += lh
    return lines, y


def render_png(slide, path, scale=100, show_boxes=False):
    img = Image.new("RGB", (round(W * scale), round(H * scale)), "white")
    d = ImageDraw.Draw(img)
    S = lambda v: round(v * scale)
    warnings = []
    for e in slide.els:
        if isinstance(e, Rect):
            box = [S(e.x), S(e.y), S(e.x + e.w), S(e.y + e.h)]
            if e.shape == "oval":
                d.ellipse(box, fill=e.fill, outline=e.line)
            else:
                d.rectangle(box, fill=e.fill, outline=e.line, width=max(1, round(e.lw / 72 * scale)) if e.line else 0)
        elif isinstance(e, Line):
            d.line([S(e.x1), S(e.y1), S(e.x2), S(e.y2)], fill=e.color, width=max(1, round(e.lw / 72 * scale * 1.3)))
        elif isinstance(e, Text):
            if e.fill or e.line:
                d.rectangle([S(e.x), S(e.y), S(e.x + e.w), S(e.y + e.h)], fill=e.fill, outline=e.line)
            if show_boxes:
                d.rectangle([S(e.x), S(e.y), S(e.x + e.w), S(e.y + e.h)], outline="#ff00ff")
            lines, th = layout_text(e, scale)
            if th > e.h - 2 * e.inset + 0.01:
                warnings.append(f"OVERFLOW {th:.2f}in > {e.h - 2 * e.inset:.2f}in: {e.paras[0]['t'][:60]!r}")
            for ln in lines:
                if ln["w"] > ln["avail"] + 0.01:
                    warnings.append(f"WIDE word {ln['w']:.2f}>{ln['avail']:.2f}: {e.paras[0]['t'][:50]!r}")
            if e.valign == "m":
                y0 = e.y + (e.h - th) / 2
            elif e.valign == "b":
                y0 = e.y + e.h - e.inset - th
            else:
                y0 = e.y + e.inset
            for ln in lines:
                x0 = e.x + e.inset + ln["indent"]
                if ln["align"] == "c":
                    x0 = e.x + e.inset + ln["indent"] + (ln["avail"] - ln["w"]) / 2
                elif ln["align"] == "r":
                    x0 = e.x + e.w - e.inset - ln["w"]
                ty = y0 + ln["y"] + ln["size"] / 72 * (LINE_H - 1.0) / 2
                if ln["bullet"]:
                    d.text((S(e.x + e.inset), S(ty)), "•", font=font(ln["size"], False, scale), fill=ln["color"])
                cx = x0
                for tok, b, c, s in ln["runs"]:
                    f = font(s, b, scale)
                    d.text((S(cx), S(ty)), tok, font=f, fill=c)
                    cx += f.getlength(tok) / scale
    img.save(path)
    return warnings


# ---------------------------------------------------------------- PPTX render
ALIGN = {"l": PP_ALIGN.LEFT, "c": PP_ALIGN.CENTER, "r": PP_ALIGN.RIGHT}
VALIGN = {"t": MSO_ANCHOR.TOP, "m": MSO_ANCHOR.MIDDLE, "b": MSO_ANCHOR.BOTTOM}


def _rgb(h):
    return RGBColor(*hexrgb(h))


def render_pptx(slides, path):
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(W), Inches(H)
    blank = prs.slide_layouts[6]
    for s in slides:
        ps = prs.slides.add_slide(blank)
        for e in s.els:
            if isinstance(e, Rect):
                shp = ps.shapes.add_shape(MSO_SHAPE.OVAL if e.shape == "oval" else MSO_SHAPE.RECTANGLE,
                                          Inches(e.x), Inches(e.y), Inches(e.w), Inches(e.h))
                shp.shadow.inherit = False
                if e.fill:
                    shp.fill.solid(); shp.fill.fore_color.rgb = _rgb(e.fill)
                else:
                    shp.fill.background()
                if e.line:
                    shp.line.color.rgb = _rgb(e.line); shp.line.width = Pt(e.lw)
                else:
                    shp.line.fill.background()
            elif isinstance(e, Line):
                c = ps.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(e.x1), Inches(e.y1), Inches(e.x2), Inches(e.y2))
                c.line.color.rgb = _rgb(e.color); c.line.width = Pt(e.lw)
                if e.dash:
                    from pptx.enum.dml import MSO_LINE
                    c.line.dash_style = MSO_LINE.DASH
            elif isinstance(e, Text):
                tb = ps.shapes.add_textbox(Inches(e.x), Inches(e.y), Inches(e.w), Inches(e.h))
                if e.fill:
                    tb.fill.solid(); tb.fill.fore_color.rgb = _rgb(e.fill)
                if e.line:
                    tb.line.color.rgb = _rgb(e.line); tb.line.width = Pt(0.75)
                tf = tb.text_frame
                tf.word_wrap = True
                tf.auto_size = None
                for side in ("left", "right", "top", "bottom"):
                    setattr(tf, f"margin_{side}", Inches(e.inset))
                tf.vertical_anchor = VALIGN[e.valign]
                for i, p in enumerate(e.paras):
                    para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
                    para.alignment = ALIGN[p["align"]]
                    if i > 0 and p["before"]:
                        para.space_before = Pt(p["before"])
                    para.line_spacing = 1.0
                    if p["bullet"]:
                        pPr = para._p.get_or_add_pPr()
                        pPr.set("marL", str(Inches(BULLET_INDENT)))
                        pPr.set("indent", str(-Inches(BULLET_INDENT)))
                        buf = pPr.makeelement(qn("a:buFont"), {"typeface": "Arial"})
                        buc = pPr.makeelement(qn("a:buChar"), {"char": "•"})
                        pPr.append(buf); pPr.append(buc)
                    for text, b, c in p["runs"]:
                        r = para.add_run()
                        r.text = text
                        r.font.name = "Arial"
                        r.font.size = Pt(p["size"])
                        r.font.bold = b
                        r.font.color.rgb = _rgb(c)
        if s.notes:
            ps.notes_slide.notes_text_frame.text = s.notes
    prs.save(path)
