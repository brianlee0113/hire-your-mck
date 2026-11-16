"""Tiny slide toolkit: every element is written to the PPTX *and* recorded so a
PIL preview can be rendered and text-fit can be checked with real Arial metrics."""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.oxml.ns import qn
from PIL import Image, ImageDraw, ImageFont
import copy

FONT = "Arial"
FDIR = "/System/Library/Fonts/Supplemental/"
INK = "1F1F1F"; SEC = "52514E"; MUTED = "898781"; RULE = "C3C2B7"; GRID = "E1E0D9"
BLUE = "2A78D6"; DBLUE = "184F95"; RED = "E34948"; PANEL = "F3F2EE"; WHITE = "FFFFFF"
TOTAL = "52514E"; LBLUE = "CDE2FB"
GOOD = "006300"; AMBER = "B06F00"

SW, SH = 13.333, 7.5
PX = 100  # preview px per inch
LINE = 1.2  # line height multiple used for fit checks (conservative)


def rgb(h):
    return RGBColor.from_string(h)


class Deck:
    def __init__(self):
        self.prs = Presentation()
        self.prs.slide_width = Inches(SW)
        self.prs.slide_height = Inches(SH)
        self.pages = []  # list of op lists
        self.issues = []

    def new(self):
        s = self.prs.slides.add_slide(self.prs.slide_layouts[6])
        ops = []
        self.pages.append(ops)
        return Slide(self, s, ops, len(self.pages))

    def save(self, path):
        self.prs.save(path)


def _font(size, bold=False, italic=False):
    name = "Arial Bold.ttf" if bold else "Arial.ttf"
    if italic:
        name = "Arial Bold Italic.ttf" if bold else "Arial Italic.ttf"
    return ImageFont.truetype(FDIR + name, max(1, round(size / 72 * PX)))


def norm_paras(paras, size, color, bold):
    """paras: str | list of (str | dict). dict keys: runs [(text,bold,color)], text, size,
    bold, color, bullet, before, align"""
    if isinstance(paras, str):
        paras = [paras]
    out = []
    for p in paras:
        if isinstance(p, str):
            p = {"text": p}
        p = dict(p)
        p.setdefault("size", size)
        p.setdefault("bold", bold)
        p.setdefault("color", color)
        if "runs" not in p:
            p["runs"] = [(p.get("text", ""), p["bold"], p["color"])]
        else:
            p["runs"] = [(r[0], r[1] if len(r) > 1 else p["bold"], r[2] if len(r) > 2 else p["color"]) for r in p["runs"]]
        p.setdefault("bullet", False)
        p.setdefault("before", 0)
        out.append(p)
    return out


def wrap_runs(runs, size, width_px, indent_px=0):
    """Return list of lines; each line = list of (text,bold,color). Word wrapping with real metrics."""
    words = []  # (word, bold, color, trailing_space)
    for text, b, c in runs:
        parts = text.split(" ")
        for i, w in enumerate(parts):
            words.append((w, b, c, i < len(parts) - 1))
    lines, cur, curw = [], [], 0.0
    avail = width_px - indent_px
    for w, b, c, sp in words:
        f = _font(size, b)
        wl = f.getlength(w)
        spl = f.getlength(" ")
        if cur and curw + wl > avail + 0.5:
            lines.append(cur)
            cur, curw = [], 0.0
        cur.append((w + (" " if sp else ""), b, c))
        curw += wl + (spl if sp else 0)
    if cur:
        lines.append(cur)
    return lines


class Slide:
    def __init__(self, deck, s, ops, num):
        self.deck, self.s, self.ops, self.num = deck, s, ops, num

    # ---------- primitives
    def rect(self, x, y, w, h, fill=None, line=None, lw=0.75, shape="rect"):
        st = MSO_SHAPE.RECTANGLE if shape == "rect" else MSO_SHAPE.OVAL
        sh = self.s.shapes.add_shape(st, Inches(x), Inches(y), Inches(w), Inches(h))
        sh.shadow.inherit = False
        if fill:
            sh.fill.solid(); sh.fill.fore_color.rgb = rgb(fill)
        else:
            sh.fill.background()
        if line:
            sh.line.color.rgb = rgb(line); sh.line.width = Pt(lw)
        else:
            sh.line.fill.background()
        sh.text_frame.text = ""
        self.ops.append(("rect", x, y, w, h, fill, line, lw, shape))
        return sh

    def line(self, x1, y1, x2, y2, color=RULE, lw=0.75, dash=False):
        c = self.s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1), Inches(x2), Inches(y2))
        c.line.color.rgb = rgb(color); c.line.width = Pt(lw)
        if dash:
            from pptx.enum.dml import MSO_LINE
            c.line.dash_style = MSO_LINE.DASH
        self.ops.append(("line", x1, y1, x2, y2, color, lw))
        return c

    def text(self, x, y, w, h, paras, size=13, color=INK, bold=False, align="l", anchor="t",
             fill=None, line=None, pad=0.0, name=None, spacing=1.0, after=0):
        paras = norm_paras(paras, size, color, bold)
        if fill or line:
            self.rect(x, y, w, h, fill, line)
        tb = self.s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
        tf = tb.text_frame
        tf.word_wrap = True
        for side in ("margin_left", "margin_right", "margin_top", "margin_bottom"):
            setattr(tf, side, Inches(pad))
        tf.vertical_anchor = {"t": MSO_ANCHOR.TOP, "m": MSO_ANCHOR.MIDDLE, "b": MSO_ANCHOR.BOTTOM}[anchor]
        al = {"l": PP_ALIGN.LEFT, "c": PP_ALIGN.CENTER, "r": PP_ALIGN.RIGHT}[align]
        for i, p in enumerate(paras):
            para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            para.alignment = p.get("align_enum", al) if "align" not in p else {"l": PP_ALIGN.LEFT, "c": PP_ALIGN.CENTER, "r": PP_ALIGN.RIGHT}[p["align"]]
            para.line_spacing = spacing
            if p["before"]:
                para.space_before = Pt(p["before"])
            if after:
                para.space_after = Pt(after)
            if p["bullet"]:
                pPr = para._p.get_or_add_pPr()
                ind = 0.18 if p["bullet"] is True else p["bullet"]
                pPr.set("marL", str(int(Inches(ind))))
                pPr.set("indent", str(-int(Inches(ind))))
                bf = pPr.makeelement(qn("a:buFont"), {"typeface": "Arial"})
                bc = pPr.makeelement(qn("a:buChar"), {"char": "•"})
                pPr.append(bf); pPr.append(bc)
            for t, b, c in p["runs"]:
                r = para.add_run()
                r.text = t
                r.font.name = FONT; r.font.size = Pt(p["size"]); r.font.bold = b
                r.font.color.rgb = rgb(c)
        self.ops.append(("text", x, y, w, h, paras, align, anchor, pad, spacing, after, name))
        self._fit(x, y, w, h, paras, pad, spacing, after, name)
        return tb

    def _fit(self, x, y, w, h, paras, pad, spacing, after, name):
        wpx = (w - 2 * pad) * PX
        total = 0
        for i, p in enumerate(paras):
            ind = (0.18 if p["bullet"] is True else p["bullet"]) * PX if p["bullet"] else 0
            lines = wrap_runs(p["runs"], p["size"], wpx, ind)
            total += len(lines) * p["size"] * LINE * spacing / 72 * PX
            total += (p["before"] + (after if i < len(paras) - 1 else 0)) / 72 * PX
            for ln in lines:
                if len(ln) == 1:
                    f = _font(p["size"], ln[0][1])
                    if f.getlength(ln[0][0].strip()) > wpx - ind + 1:
                        self.deck.issues.append(f"p{self.num}: word too wide '{ln[0][0]}' in {name or paras[0]['runs'][0][0][:30]}")
        hpx = (h - 2 * pad) * PX
        if total > hpx + 1:
            self.deck.issues.append(f"p{self.num}: overflow {total/PX:.2f}in > {hpx/PX:.2f}in in '{name or paras[0]['runs'][0][0][:40]}'")

    # ---------- page furniture
    def header(self, section, title):
        self.text(0.6, 0.32, 9, 0.25, section.upper(), size=10, color=BLUE, bold=True, name="section")
        self.text(0.6, 0.58, 12.1, 0.95, title, size=22, bold=True, color=INK, anchor="t", spacing=0.95, name="title")
        self.line(0.6, 1.58, SW - 0.6, 1.58, color=RULE, lw=0.75)

    def footer(self, source):
        self.line(0.6, 6.98, SW - 0.6, 6.98, color=GRID, lw=0.5)
        if source:
            self.text(0.6, 7.03, 11.2, 0.4, source, size=8.5, color=MUTED, name="source")
        self.text(SW - 1.2, 7.03, 0.6, 0.25, str(self.num), size=9, color=MUTED, align="r", name="pagenum")


# ---------- preview renderer
def render(deck, outdir):
    paths = []
    for i, ops in enumerate(deck.pages, 1):
        im = Image.new("RGB", (int(SW * PX), int(SH * PX)), "white")
        d = ImageDraw.Draw(im)
        for op in ops:
            k = op[0]
            if k == "rect":
                _, x, y, w, h, fill, line, lw, shape = op
                box = [x * PX, y * PX, (x + w) * PX, (y + h) * PX]
                if shape == "rect":
                    d.rectangle(box, fill=("#" + fill) if fill else None, outline=("#" + line) if line else None,
                                width=max(1, round(lw / 72 * PX)) if line else 0)
                else:
                    d.ellipse(box, fill=("#" + fill) if fill else None, outline=("#" + line) if line else None)
            elif k == "line":
                _, x1, y1, x2, y2, color, lw = op
                d.line([x1 * PX, y1 * PX, x2 * PX, y2 * PX], fill="#" + color, width=max(1, round(lw / 72 * PX)))
            elif k == "text":
                _, x, y, w, h, paras, align, anchor, pad, spacing, after, name = op
                wpx = (w - 2 * pad) * PX
                blocks = []
                total = 0
                for j, p in enumerate(paras):
                    ind = (0.18 if p["bullet"] is True else p["bullet"]) * PX if p["bullet"] else 0
                    lines = wrap_runs(p["runs"], p["size"], wpx, ind)
                    lh = p["size"] * 1.17 * spacing / 72 * PX
                    total += p["before"] / 72 * PX
                    blocks.append((p, lines, lh, ind, total))
                    total += len(lines) * lh + (after / 72 * PX if j < len(paras) - 1 else 0)
                top = y * PX + pad * PX
                hpx = (h - 2 * pad) * PX
                if anchor == "m":
                    top += (hpx - total) / 2
                elif anchor == "b":
                    top += hpx - total
                for p, lines, lh, ind, off in blocks:
                    al = p.get("align", align)
                    for li, ln in enumerate(lines):
                        ly = top + off + li * lh
                        lw_ = sum(_font(p["size"], b).getlength(t) for t, b, c in ln)
                        if al == "c":
                            lx = x * PX + pad * PX + (wpx - lw_) / 2
                        elif al == "r":
                            lx = x * PX + pad * PX + wpx - lw_
                        else:
                            lx = x * PX + pad * PX + ind
                        if p["bullet"] and li == 0:
                            d.text((x * PX + pad * PX, ly), "•", font=_font(p["size"]), fill="#" + p["color"])
                        for t, b, c in ln:
                            f = _font(p["size"], b)
                            d.text((lx, ly), t, font=f, fill="#" + c)
                            lx += f.getlength(t)
        pth = f"{outdir}/slide{i:02d}.png"
        im.save(pth)
        paths.append(pth)
    return paths
