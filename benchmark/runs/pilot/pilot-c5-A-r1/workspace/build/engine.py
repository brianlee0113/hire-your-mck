"""Tiny slide engine: one layout spec -> (a) editable PPTX via python-pptx, (b) PNG preview via PIL.

Every element is a primitive (rect, oval, line, polyline, text) in inches, so the PIL preview
reproduces the PPTX geometry and lets us check wrapping/overflow without PowerPoint.
"""
import re
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR, MSO_AUTO_SIZE
from pptx.oxml.ns import qn
from lxml import etree
from PIL import Image, ImageDraw, ImageFont

W, H = 13.333, 7.5
FONT = "Arial"
FONT_FILES = {
    (False, False): "/System/Library/Fonts/Supplemental/Arial.ttf",
    (True, False): "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    (False, True): "/System/Library/Fonts/Supplemental/Arial Italic.ttf",
    (True, True): "/System/Library/Fonts/Supplemental/Arial Bold Italic.ttf",
}
LINE = 1.17          # line height multiple used by both backends
INS_L = INS_R = 0.05  # text insets (in)
INS_T = INS_B = 0.03


def rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


# ---------------------------------------------------------------- text model
def parse_runs(s, base):
    """'**bold**' markup -> list of (text, style)."""
    out = []
    for i, part in enumerate(re.split(r"\*\*", s)):
        if not part:
            continue
        st = dict(base)
        if i % 2 == 1:
            st["bold"] = True
        out.append((part, st))
    return out


def norm_paras(content, size, color, bold, align, italic=False):
    """content: str | list of (str | dict(text=..., bullet=, size=, color=, bold=, space_after=, align=))."""
    if isinstance(content, (str, dict)):
        content = [content]
    paras = []
    for p in content:
        if isinstance(p, str):
            p = {"text": p}
        st = {"size": p.get("size", size), "color": p.get("color", color),
              "bold": p.get("bold", bold), "italic": p.get("italic", italic)}
        paras.append({
            "runs": parse_runs(p["text"], st),
            "bullet": p.get("bullet", False),
            "indent": p.get("indent", 0.0),
            "size": st["size"],
            "align": p.get("align", align),
            "space_after": p.get("space_after", 0),
            "space_before": p.get("space_before", 0),
        })
    return paras


_font_cache = {}


def pil_font(size_pt, bold, italic, dpi):
    key = (round(size_pt * dpi / 72), bold, italic)
    if key not in _font_cache:
        _font_cache[key] = ImageFont.truetype(FONT_FILES[(bold, italic)], key[0])
    return _font_cache[key]


BULLET_W = 0.17  # in, hanging indent for bullets


def layout_para(p, width_in, dpi):
    """Greedy word wrap with per-run fonts. Returns list of lines; line = list of (text, style, x_px)."""
    left = (BULLET_W if p["bullet"] else 0) + p["indent"]
    maxw = (width_in - left) * dpi
    tokens = []
    for text, st in p["runs"]:
        for piece in re.split(r"(\s+)", text):
            if piece:
                tokens.append((piece, st))
    lines, cur, curw = [], [], 0.0
    for tok, st in tokens:
        f = pil_font(st["size"], st["bold"], st["italic"], dpi)
        tw = f.getlength(tok)
        if tok.isspace():
            if cur:
                cur.append((tok, st, curw)); curw += tw
            continue
        if curw + tw > maxw and cur:
            while cur and cur[-1][0].isspace():
                curw -= pil_font(cur[-1][1]["size"], cur[-1][1]["bold"], cur[-1][1]["italic"], dpi).getlength(cur[-1][0])
                cur.pop()
            lines.append((cur, curw)); cur, curw = [], 0.0
        cur.append((tok, st, curw)); curw += tw
    while cur and cur[-1][0].isspace():
        curw -= pil_font(cur[-1][1]["size"], cur[-1][1]["bold"], cur[-1][1]["italic"], dpi).getlength(cur[-1][0])
        cur.pop()
    lines.append((cur, curw))
    return lines, left, maxw


def measure(paras, width_in, dpi=150):
    """Return (height_in, max_line_width_in, too_long_word)."""
    h, mw, bad = 0.0, 0.0, False
    for i, p in enumerate(paras):
        lines, left, maxw = layout_para(p, width_in, dpi)
        lh = p["size"] * LINE / 72
        h += (p["space_before"] if i else 0) / 72
        h += lh * len(lines)
        h += (p["space_after"] / 72 if i < len(paras) - 1 else 0)
        for ln, w in lines:
            mw = max(mw, left + w / dpi)
            if w > maxw + 1:
                bad = True
    return h, mw, bad


# ---------------------------------------------------------------- slide spec
class Slide:
    def __init__(self):
        self.els = []

    def rect(self, x, y, w, h, fill=None, line=None, lw=0.75):
        self.els.append(("rect", dict(x=x, y=y, w=w, h=h, fill=fill, line=line, lw=lw)))

    def oval(self, x, y, w, h, fill=None, line=None, lw=0.75):
        self.els.append(("oval", dict(x=x, y=y, w=w, h=h, fill=fill, line=line, lw=lw)))

    def line(self, x1, y1, x2, y2, color="#c3c2b7", lw=0.75):
        self.els.append(("line", dict(x1=x1, y1=y1, x2=x2, y2=y2, color=color, lw=lw)))

    def poly(self, pts, color, lw=2.0):
        self.els.append(("poly", dict(pts=pts, color=color, lw=lw)))

    def text(self, x, y, w, h, content, size=12, color="#0b0b0b", bold=False, align="l",
             valign="t", italic=False, fill=None, check=True):
        paras = norm_paras(content, size, color, bold, align, italic)
        self.els.append(("text", dict(x=x, y=y, w=w, h=h, paras=paras, valign=valign, fill=fill, check=check)))


# ---------------------------------------------------------------- PPTX backend
ALIGN = {"l": PP_ALIGN.LEFT, "c": PP_ALIGN.CENTER, "r": PP_ALIGN.RIGHT}
VALIGN = {"t": MSO_ANCHOR.TOP, "m": MSO_ANCHOR.MIDDLE, "b": MSO_ANCHOR.BOTTOM}


def _fill_line(shp, fill, line, lw):
    if fill:
        shp.fill.solid(); shp.fill.fore_color.rgb = RGBColor(*rgb(fill))
    else:
        shp.fill.background()
    if line:
        shp.line.color.rgb = RGBColor(*rgb(line)); shp.line.width = Pt(lw)
    else:
        shp.line.fill.background()
    shp.shadow.inherit = False


def build_pptx(slides, path, notes=None):
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(W), Inches(H)
    blank = prs.slide_layouts[6]
    for si, s in enumerate(slides):
        sl = prs.slides.add_slide(blank)
        for kind, e in s.els:
            if kind in ("rect", "oval"):
                shp = sl.shapes.add_shape(MSO_SHAPE.RECTANGLE if kind == "rect" else MSO_SHAPE.OVAL,
                                          Inches(e["x"]), Inches(e["y"]), Inches(e["w"]), Inches(e["h"]))
                _fill_line(shp, e["fill"], e["line"], e["lw"])
                shp.text_frame.text = ""
            elif kind == "line":
                c = sl.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(e["x1"]), Inches(e["y1"]),
                                            Inches(e["x2"]), Inches(e["y2"]))
                c.line.color.rgb = RGBColor(*rgb(e["color"])); c.line.width = Pt(e["lw"])
            elif kind == "poly":
                pts = e["pts"]
                fb = sl.shapes.build_freeform(Inches(pts[0][0]), Inches(pts[0][1]), scale=1.0)
                fb.add_line_segments([(Inches(x), Inches(y)) for x, y in pts[1:]], close=False)
                shp = fb.convert_to_shape()
                shp.fill.background()
                shp.line.color.rgb = RGBColor(*rgb(e["color"])); shp.line.width = Pt(e["lw"])
                shp.shadow.inherit = False
            elif kind == "text":
                tb = sl.shapes.add_textbox(Inches(e["x"]), Inches(e["y"]), Inches(e["w"]), Inches(e["h"]))
                if e["fill"]:
                    tb.fill.solid(); tb.fill.fore_color.rgb = RGBColor(*rgb(e["fill"]))
                tf = tb.text_frame
                tf.word_wrap = True
                tf.auto_size = MSO_AUTO_SIZE.NONE
                tf.margin_left, tf.margin_right = Inches(INS_L), Inches(INS_R)
                tf.margin_top, tf.margin_bottom = Inches(INS_T), Inches(INS_B)
                tf.vertical_anchor = VALIGN[e["valign"]]
                for pi, p in enumerate(e["paras"]):
                    para = tf.paragraphs[0] if pi == 0 else tf.add_paragraph()
                    para.alignment = ALIGN[p["align"]]
                    para.line_spacing = LINE / 1.17 * 1.0  # single spacing; Arial single ~1.17
                    para.space_after = Pt(p["space_after"])
                    para.space_before = Pt(p["space_before"])
                    pPr = para._p.get_or_add_pPr()
                    left = (BULLET_W if p["bullet"] else 0) + p["indent"]
                    if p["bullet"]:
                        pPr.set("marL", str(Inches(left)))
                        pPr.set("indent", str(-Inches(BULLET_W)))
                        bf = etree.SubElement(pPr, qn("a:buFont")); bf.set("typeface", "Arial")
                        bc = etree.SubElement(pPr, qn("a:buChar")); bc.set("char", "•")
                    else:
                        if left:
                            pPr.set("marL", str(Inches(left)))
                        etree.SubElement(pPr, qn("a:buNone"))
                    for text, st in p["runs"]:
                        r = para.add_run(); r.text = text
                        f = r.font; f.name = FONT; f.size = Pt(st["size"]); f.bold = st["bold"]
                        f.italic = st["italic"]; f.color.rgb = RGBColor(*rgb(st["color"]))
        if notes and si < len(notes) and notes[si]:
            sl.notes_slide.notes_text_frame.text = notes[si]
    prs.save(path)


# ---------------------------------------------------------------- PIL backend
def render_png(s, path, dpi=150):
    img = Image.new("RGB", (int(W * dpi), int(H * dpi)), "white")
    d = ImageDraw.Draw(img)
    P = lambda v: int(round(v * dpi))
    for kind, e in s.els:
        if kind in ("rect", "oval"):
            box = [P(e["x"]), P(e["y"]), P(e["x"] + e["w"]) - 1, P(e["y"] + e["h"]) - 1]
            if box[2] < box[0]: box[2] = box[0]
            if box[3] < box[1]: box[3] = box[1]
            fn = d.rectangle if kind == "rect" else d.ellipse
            fn(box, fill=rgb(e["fill"]) if e["fill"] else None,
               outline=rgb(e["line"]) if e["line"] else None,
               width=max(1, int(e["lw"] * dpi / 72)) if e["line"] else 0)
        elif kind == "line":
            d.line([P(e["x1"]), P(e["y1"]), P(e["x2"]), P(e["y2"])], fill=rgb(e["color"]),
                   width=max(1, int(round(e["lw"] * dpi / 72))))
        elif kind == "poly":
            d.line([(P(x), P(y)) for x, y in e["pts"]], fill=rgb(e["color"]),
                   width=max(1, int(round(e["lw"] * dpi / 72))), joint="curve")
        elif kind == "text":
            if e["fill"]:
                d.rectangle([P(e["x"]), P(e["y"]), P(e["x"] + e["w"]), P(e["y"] + e["h"])], fill=rgb(e["fill"]))
            inner_w = e["w"] - INS_L - INS_R
            th, _, _ = measure(e["paras"], inner_w, dpi)
            top = e["y"] + INS_T
            avail = e["h"] - INS_T - INS_B
            if e["valign"] == "m":
                top += (avail - th) / 2
            elif e["valign"] == "b":
                top += avail - th
            y = top
            for i, p in enumerate(e["paras"]):
                if i:
                    y += p["space_before"] / 72
                lines, left, maxw = layout_para(p, inner_w, dpi)
                lh = p["size"] * LINE / 72
                for li, (ln, lw_) in enumerate(lines):
                    if p["align"] == "c":
                        x0 = e["x"] + INS_L + left + (inner_w - left - lw_ / dpi) / 2
                    elif p["align"] == "r":
                        x0 = e["x"] + e["w"] - INS_R - lw_ / dpi
                    else:
                        x0 = e["x"] + INS_L + left
                    if li == 0 and p["bullet"]:
                        st0 = p["runs"][0][1]
                        f = pil_font(st0["size"], False, False, dpi)
                        d.text((P(e["x"] + INS_L + p["indent"]), P(y)), "•", font=f, fill=rgb(st0["color"]))
                    for tok, st, xo in ln:
                        f = pil_font(st["size"], st["bold"], st["italic"], dpi)
                        # baseline-ish offset to mimic PowerPoint's ascent placement
                        off = (lh - st["size"] * 1.117 / 72) / 2
                        d.text((P(x0) + xo, P(y + off)), tok, font=f, fill=rgb(st["color"]))
                    y += lh
                y += p["space_after"] / 72
    img.save(path)


# ---------------------------------------------------------------- QA
def check(slides):
    issues = []
    for si, s in enumerate(slides, 1):
        boxes = []
        for kind, e in s.els:
            if kind == "text":
                inner_w = e["w"] - INS_L - INS_R
                th, mw, bad = measure(e["paras"], inner_w)
                avail = e["h"] - INS_T - INS_B
                label = "".join(t for t, _ in e["paras"][0]["runs"])[:40]
                if e["check"] and th > avail + 0.01:
                    issues.append(f"slide {si}: overflow {th:.2f}>{avail:.2f} in '{label}'")
                if bad:
                    issues.append(f"slide {si}: word wider than box in '{label}'")
                # actual text extent
                top = e["y"] + INS_T
                if e["valign"] == "m":
                    top += (avail - th) / 2
                elif e["valign"] == "b":
                    top += avail - th
                al = e["paras"][0]["align"]
                if al == "l":
                    x0 = e["x"] + INS_L
                elif al == "r":
                    x0 = e["x"] + e["w"] - INS_R - mw
                else:
                    x0 = e["x"] + INS_L + (inner_w - mw) / 2
                boxes.append((x0, top, x0 + mw, top + th, label))
            for v in (e.get("x"), e.get("x1"), e.get("x2")):
                pass
            if kind in ("rect", "oval", "text"):
                if e["x"] < -0.01 or e["y"] < -0.01 or e["x"] + e["w"] > W + 0.01 or e["y"] + e["h"] > H + 0.01:
                    issues.append(f"slide {si}: {kind} off-slide at ({e['x']:.2f},{e['y']:.2f})")
        for i in range(len(boxes)):
            for j in range(i + 1, len(boxes)):
                a, b = boxes[i], boxes[j]
                ox = min(a[2], b[2]) - max(a[0], b[0])
                oy = min(a[3], b[3]) - max(a[1], b[1])
                if ox > 0.02 and oy > 0.02:
                    issues.append(f"slide {si}: text overlap '{a[4]}' x '{b[4]}' ({ox:.2f}x{oy:.2f})")
    return issues
