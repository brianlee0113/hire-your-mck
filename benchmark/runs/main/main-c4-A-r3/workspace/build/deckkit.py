"""Tiny slide kit: each slide is a list of primitive ops (rect, line, text, oval, diamond),
emitted both to a .pptx (python-pptx) and to a PIL preview PNG so layout can be checked
without PowerPoint. Units are inches. Text supports **bold** inline markup."""
import re
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR, MSO_AUTO_SIZE
from pptx.oxml.ns import qn
from PIL import Image, ImageDraw, ImageFont

W, H = 13.333, 7.5
FONT_DIR = "/System/Library/Fonts/Supplemental/"
FONT_REG, FONT_BOLD = FONT_DIR + "Arial.ttf", FONT_DIR + "Arial Bold.ttf"
FACE = "Arial"
INSET = 0.04          # text box inset, inches
LINE_H = 1.17         # line height multiple used by preview + fit check
DPI = 120

_font_cache = {}
def _font(bold, size_pt, dpi=DPI):
    px = max(1, round(size_pt / 72 * dpi))
    k = (bold, px)
    if k not in _font_cache:
        _font_cache[k] = ImageFont.truetype(FONT_BOLD if bold else FONT_REG, px)
    return _font_cache[k]

def parse_runs(s):
    """'a **b** c' -> [('a ',False),('b',True),(' c',False)]"""
    out, bold = [], False
    for i, part in enumerate(re.split(r"\*\*", s)):
        if part:
            out.append((part, bold))
        bold = not bold
    return out

class P:
    """Paragraph."""
    def __init__(self, text, size=None, bold=None, color=None, bullet=False, level=0,
                 space_before=None, align=None):
        self.text, self.size, self.bold, self.color = text, size, bold, color
        self.bullet, self.level, self.space_before, self.align = bullet, level, space_before, align

class Slide:
    def __init__(self, deck):
        self.ops, self.deck = [], deck
    def rect(self, x, y, w, h, fill=None, line=None, lw=0.75):
        self.ops.append(("rect", dict(x=x, y=y, w=w, h=h, fill=fill, line=line, lw=lw)))
    def oval(self, x, y, w, h, fill=None, line=None, lw=0.75):
        self.ops.append(("oval", dict(x=x, y=y, w=w, h=h, fill=fill, line=line, lw=lw)))
    def diamond(self, cx, cy, s, fill):
        self.ops.append(("diamond", dict(x=cx - s / 2, y=cy - s / 2, w=s, h=s, fill=fill)))
    def line(self, x1, y1, x2, y2, color="C3C2B7", lw=0.75):
        self.ops.append(("line", dict(x1=x1, y1=y1, x2=x2, y2=y2, color=color, lw=lw)))
    def text(self, x, y, w, h, paras, size=12, color="0B0B0B", bold=False, align="l",
             valign="t", fill=None, para_space=0, bullet_indent=0.18, name=None):
        if isinstance(paras, (str, P)):
            paras = [paras]
        paras = [p if isinstance(p, P) else P(p) for p in paras]
        self.ops.append(("text", dict(x=x, y=y, w=w, h=h, paras=paras, size=size, color=color,
                                      bold=bold, align=align, valign=valign, fill=fill,
                                      para_space=para_space, bi=bullet_indent, name=name)))

class Deck:
    def __init__(self):
        self.slides = []
        self.warnings = []
    def new(self):
        s = Slide(self); self.slides.append(s); return s

    # ---------------- layout measurement (shared by preview + fit check) -------------
    def layout_text(self, op, dpi=DPI):
        """Return list of lines: (y_px_offset, x_px_offset, [(text,bold,size,color)]) and total height px."""
        x, w = op["x"], op["w"]
        avail = (w - 2 * INSET) * dpi
        lines, ycur = [], 0.0
        for pi, p in enumerate(op["paras"]):
            size = p.size or op["size"]
            color = p.color or op["color"]
            base_bold = op["bold"] if p.bold is None else p.bold
            lh = size / 72 * dpi * LINE_H
            sb = (p.space_before if p.space_before is not None else (op["para_space"] if pi else 0))
            ycur += sb / 72 * dpi
            indent = (op["bi"] * (1 + p.level) * dpi) if p.bullet else 0
            width = avail - indent
            # tokens
            toks = []
            for t, b in parse_runs(p.text):
                for piece in re.split(r"( )", t):
                    if piece:
                        toks.append((piece, b or base_bold))
            cur, curw, first = [], 0.0, True
            def flush():
                nonlocal cur, curw, ycur, first
                while cur and cur[-1][0] == " ":
                    cur.pop()
                lines.append((ycur, indent, [(t, b, size, color) for t, b in cur], p, first, lw_(cur, size)))
                ycur += lh; cur, curw, first = [], 0.0, False
            def lw_(cur, size):
                return sum(_font(b, size, dpi).getlength(t) for t, b in cur)
            for t, b in toks:
                if t == "\n":
                    flush(); continue
                tw = _font(b, size, dpi).getlength(t)
                if t != " " and curw + tw > width * 0.965 and cur:
                    flush()
                    if t == " ":
                        continue
                if t == " " and not cur:
                    continue
                cur.append((t, b)); curw += tw
            flush()
        return lines, ycur

    def check_fit(self, si, op):
        lines, total = self.layout_text(op)
        avail = (op["h"] - 2 * INSET) * DPI
        if total > avail + 1:
            snippet = op["paras"][0].text[:50]
            self.warnings.append(f"slide {si+1}: text overflow {total/DPI:.2f}in > {op['h']-2*INSET:.2f}in :: {snippet!r}")

    # ---------------- preview ----------------
    def render_png(self, path_tpl):
        paths = []
        for si, s in enumerate(self.slides):
            img = Image.new("RGB", (round(W * DPI), round(H * DPI)), "white")
            d = ImageDraw.Draw(img)
            px = lambda v: round(v * DPI)
            for kind, op in s.ops:
                if kind in ("rect", "oval", "diamond"):
                    box = [px(op["x"]), px(op["y"]), px(op["x"] + op["w"]), px(op["y"] + op["h"])]
                    fill = "#" + op["fill"] if op.get("fill") else None
                    outline = "#" + op["line"] if op.get("line") else None
                    wd = max(1, round(op.get("lw", 0.75) / 72 * DPI)) if outline else 0
                    if kind == "rect":
                        d.rectangle(box, fill=fill, outline=outline, width=wd)
                    elif kind == "oval":
                        d.ellipse(box, fill=fill, outline=outline, width=wd)
                    else:
                        cx, cy = (box[0] + box[2]) / 2, (box[1] + box[3]) / 2
                        d.polygon([(cx, box[1]), (box[2], cy), (cx, box[3]), (box[0], cy)], fill=fill)
                elif kind == "line":
                    d.line([px(op["x1"]), px(op["y1"]), px(op["x2"]), px(op["y2"])], fill="#" + op["color"],
                           width=max(1, round(op["lw"] / 72 * DPI)))
                elif kind == "text":
                    self.check_fit(si, op)
                    if op["fill"]:
                        d.rectangle([px(op["x"]), px(op["y"]), px(op["x"] + op["w"]), px(op["y"] + op["h"])],
                                    fill="#" + op["fill"])
                    lines, total = self.layout_text(op)
                    inner_h = (op["h"] - 2 * INSET) * DPI
                    off = {"t": 0, "m": (inner_h - total) / 2, "b": inner_h - total}[op["valign"]]
                    x0, y0 = op["x"] * DPI + INSET * DPI, op["y"] * DPI + INSET * DPI + off
                    avail = (op["w"] - 2 * INSET) * DPI
                    for (ly, ind, runs, p, first, lwid) in lines:
                        align = p.align or op["align"]
                        if align == "c":
                            xx = x0 + ind + (avail - ind - lwid) / 2
                        elif align == "r":
                            xx = x0 + avail - lwid
                        else:
                            xx = x0 + ind
                        size = runs[0][2] if runs else (p.size or op["size"])
                        if p.bullet and first:
                            col = runs[0][3] if runs else op["color"]
                            d.text((x0 + ind - op["bi"] * DPI, y0 + ly), "•", font=_font(False, size), fill="#" + col)
                        for t, b, sz, col in runs:
                            f = _font(b, sz)
                            d.text((xx, y0 + ly), t, font=f, fill="#" + col)
                            xx += f.getlength(t)
            p = path_tpl.format(si + 1)
            img.save(p); paths.append(p)
        return paths

    # ---------------- pptx ----------------
    def save_pptx(self, path):
        prs = Presentation()
        prs.slide_width, prs.slide_height = Inches(W), Inches(H)
        blank = prs.slide_layouts[6]
        for s in self.slides:
            sl = prs.slides.add_slide(blank)
            for kind, op in s.ops:
                if kind in ("rect", "oval", "diamond"):
                    shp_t = {"rect": MSO_SHAPE.RECTANGLE, "oval": MSO_SHAPE.OVAL, "diamond": MSO_SHAPE.DIAMOND}[kind]
                    shp = sl.shapes.add_shape(shp_t, Inches(op["x"]), Inches(op["y"]), Inches(op["w"]), Inches(op["h"]))
                    shp.shadow.inherit = False
                    if op.get("fill"):
                        shp.fill.solid(); shp.fill.fore_color.rgb = RGBColor.from_string(op["fill"])
                    else:
                        shp.fill.background()
                    if op.get("line"):
                        shp.line.color.rgb = RGBColor.from_string(op["line"]); shp.line.width = Pt(op["lw"])
                    else:
                        shp.line.fill.background()
                    if shp.has_text_frame:
                        shp.text_frame.text = ""
                elif kind == "line":
                    c = sl.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(op["x1"]), Inches(op["y1"]),
                                                Inches(op["x2"]), Inches(op["y2"]))
                    c.line.color.rgb = RGBColor.from_string(op["color"]); c.line.width = Pt(op["lw"])
                elif kind == "text":
                    tb = sl.shapes.add_textbox(Inches(op["x"]), Inches(op["y"]), Inches(op["w"]), Inches(op["h"]))
                    if op["name"]:
                        tb.name = op["name"]
                    if op["fill"]:
                        tb.fill.solid(); tb.fill.fore_color.rgb = RGBColor.from_string(op["fill"])
                    tf = tb.text_frame
                    tf.word_wrap = True
                    tf.auto_size = MSO_AUTO_SIZE.NONE
                    for side in ("margin_left", "margin_right", "margin_top", "margin_bottom"):
                        setattr(tf, side, Inches(INSET))
                    tf.vertical_anchor = {"t": MSO_ANCHOR.TOP, "m": MSO_ANCHOR.MIDDLE, "b": MSO_ANCHOR.BOTTOM}[op["valign"]]
                    for pi, p in enumerate(op["paras"]):
                        para = tf.paragraphs[0] if pi == 0 else tf.add_paragraph()
                        align = p.align or op["align"]
                        para.alignment = {"l": PP_ALIGN.LEFT, "c": PP_ALIGN.CENTER, "r": PP_ALIGN.RIGHT}[align]
                        para.line_spacing = 1.0
                        sb = p.space_before if p.space_before is not None else (op["para_space"] if pi else 0)
                        if sb:
                            para.space_before = Pt(sb)
                        size = p.size or op["size"]
                        color = p.color or op["color"]
                        base_bold = op["bold"] if p.bold is None else p.bold
                        pPr = para._p.get_or_add_pPr()
                        if p.bullet:
                            ind = Inches(op["bi"] * (1 + p.level))
                            pPr.set("marL", str(int(ind))); pPr.set("indent", str(-int(Inches(op["bi"]))))
                            bu = pPr.makeelement(qn("a:buChar"), {"char": "•"})
                            pPr.append(bu)
                        else:
                            pPr.append(pPr.makeelement(qn("a:buNone"), {}))
                        runs = parse_runs(p.text)
                        for t, b in runs:
                            # explicit line breaks
                            chunks = t.split("\n")
                            for ci, ch in enumerate(chunks):
                                if ci:
                                    br = para._p.makeelement(qn("a:br"), {})
                                    para._p.append(br)
                                if not ch:
                                    continue
                                r = para.add_run(); r.text = ch
                                r.font.size = Pt(size); r.font.bold = bool(b or base_bold)
                                r.font.name = FACE
                                r.font.color.rgb = RGBColor.from_string(color)
        prs.save(path)
