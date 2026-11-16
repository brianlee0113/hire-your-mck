"""Tiny layout layer: every element is drawn to python-pptx AND to a PIL preview,
so the layout can be checked visually and text overflow detected."""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn
from PIL import Image, ImageDraw, ImageFont
import copy

FONT = "Arial"
REG = "/System/Library/Fonts/Supplemental/Arial.ttf"
BLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
PX = 110  # preview pixels per inch
W, H = 13.333, 7.5

INK = "0B0B0B"; INK2 = "52514E"; MUTED = "8A8984"; RULE = "D6D5D0"; PANEL = "F3F2EF"
BLUE = "2A78D6"; BLUE_D = "184F95"; BLUE_L = "CDE2FB"; RED = "E34948"; RED_L = "FBE3E2"; GRAY = "B4B2AC"
GREEN = "0CA30C"; AMBER = "EDA100"

_fc = {}
def font(size_pt, bold=False):
    k = (size_pt, bold)
    if k not in _fc:
        _fc[k] = ImageFont.truetype(BLD if bold else REG, int(round(size_pt / 72 * PX)))
    return _fc[k]

def rgb(h):
    return RGBColor.from_string(h)

def hex2t(h):
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


class Para:
    def __init__(self, runs, size=12, bold=False, color=INK, bullet=False, align="l",
                 space_before=0, level=0):
        if isinstance(runs, str):
            runs = [(runs, bold, color)]
        self.runs = [(r if isinstance(r, tuple) else (r, bold, color)) for r in runs]
        self.runs = [(t, b if b is not None else bold, c or color) for t, b, c in self.runs]
        self.size, self.bullet, self.align, self.sb, self.level = size, bullet, align, space_before, level


class Deck:
    def __init__(self):
        self.prs = Presentation()
        self.prs.slide_width = Inches(W); self.prs.slide_height = Inches(H)
        self.blank = self.prs.slide_layouts[6]
        self.previews = []
        self.warnings = []
        self.n = 0

    # ---------------------------------------------------------------- slide
    def slide(self):
        self.n += 1
        s = self.prs.slides.add_slide(self.blank)
        img = Image.new("RGB", (int(W * PX), int(H * PX)), "white")
        self.cur = (s, ImageDraw.Draw(img), img)
        self.previews.append(img)
        return s

    # ---------------------------------------------------------------- shapes
    def rect(self, x, y, w, h, fill=None, line=None, lw=0.75, shape="rect"):
        s, d, _ = self.cur
        st = MSO_SHAPE.ROUNDED_RECTANGLE if shape == "round" else MSO_SHAPE.RECTANGLE
        sh = s.shapes.add_shape(st, Inches(x), Inches(y), Inches(max(w, 0.001)), Inches(max(h, 0.001)))
        if shape == "round":
            sh.adjustments[0] = 0.08
        if fill:
            sh.fill.solid(); sh.fill.fore_color.rgb = rgb(fill)
        else:
            sh.fill.background()
        if line:
            sh.line.color.rgb = rgb(line); sh.line.width = Pt(lw)
        else:
            sh.line.fill.background()
        sh.shadow.inherit = False
        box = [x * PX, y * PX, (x + w) * PX, (y + h) * PX]
        d.rectangle(box, fill=hex2t(fill) if fill else None,
                    outline=hex2t(line) if line else None, width=max(1, int(lw * PX / 72)) if line else 0)
        return sh

    def line(self, x1, y1, x2, y2, color=RULE, lw=0.75, dash=False):
        s, d, _ = self.cur
        c = s.shapes.add_connector(1, Inches(x1), Inches(y1), Inches(x2), Inches(y2))
        c.line.color.rgb = rgb(color); c.line.width = Pt(lw)
        if dash:
            ln = c.line._get_or_add_ln()
            pd = ln.makeelement(qn("a:prstDash"), {"val": "dash"}); ln.append(pd)
        d.line([x1 * PX, y1 * PX, x2 * PX, y2 * PX], fill=hex2t(color), width=max(1, int(round(lw * PX / 72))))

    # ---------------------------------------------------------------- text
    def _wrap(self, p, width_px):
        """returns list of lines; each line = list of (text, bold, color) pieces"""
        words = []
        for t, b, c in p.runs:
            for i, wd in enumerate(t.split(" ")):
                words.append([wd, b, c, i > 0 or (words and True)])
        lines, cur, curw = [], [], 0
        ind = self.indent_px(p)
        avail = width_px - ind
        for wd, b, c, _ in words:
            f = font(p.size, b)
            sp = f.getlength(" ")
            ww = f.getlength(wd)
            add = ww + (sp if cur else 0)
            if cur and curw + add > avail:
                lines.append(cur); cur, curw = [], 0; add = ww
            cur.append((wd, b, c)); curw += add
        if cur:
            lines.append(cur)
        return lines or [[("", False, INK)]]

    def indent_px(self, p):
        return (0.17 + 0.17 * p.level) * PX if p.bullet else 0

    def text(self, x, y, w, h, paras, valign="t", fill=None, line=None, margin=0.06, name=None, shape="rect", lw=0.75):
        if isinstance(paras, (str, Para)):
            paras = [paras if isinstance(paras, Para) else Para(paras)]
        s, d, _ = self.cur
        if fill or line:
            self.rect(x, y, w, h, fill=fill, line=line, shape=shape, lw=lw)
        tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.auto_size = None
        for side in ("left", "right", "top", "bottom"):
            setattr(tf, f"margin_{side}", Inches(margin))
        tf.vertical_anchor = {"t": MSO_ANCHOR.TOP, "m": MSO_ANCHOR.MIDDLE, "b": MSO_ANCHOR.BOTTOM}[valign]
        # preview layout
        wpx = (w - 2 * margin) * PX
        blocks, total = [], 0
        for i, p in enumerate(paras):
            ls = self._wrap(p, wpx)
            lh = p.size / 72 * PX * 1.2
            sb = (p.sb / 72 * PX) if i else 0
            blocks.append((p, ls, lh, sb)); total += sb + lh * len(ls)
        hpx = (h - 2 * margin) * PX
        if total > hpx + 2:
            first = "".join(t for t, _, _ in paras[0].runs)[:60]
            self.warnings.append(f"slide {self.n}: text overflow {total / PX:.2f}in > {h - 2 * margin:.2f}in :: {first}")
        widest = max((self.indent_px(p) + sum(font(p.size, b).getlength(t + " ") for t, b, c in ln)
                      for p, ls, _, _ in blocks for ln in ls), default=0)
        if widest > wpx + 4:
            self.warnings.append(f"slide {self.n}: single word too wide in box :: {paras[0].runs[0][0][:40]}")
        ytop = y * PX + margin * PX + {"t": 0, "m": (hpx - total) / 2, "b": hpx - total}[valign]
        cy = ytop
        for p, ls, lh, sb in blocks:
            cy += sb
            for li, ln in enumerate(ls):
                lw_ = sum(font(p.size, b).getlength(t) for t, b, c in ln) + font(p.size).getlength(" ") * (len(ln) - 1)
                x0 = x * PX + margin * PX + self.indent_px(p)
                if p.align == "c":
                    x0 = x * PX + margin * PX + (wpx - lw_) / 2
                elif p.align == "r":
                    x0 = x * PX + margin * PX + wpx - lw_
                if p.bullet and li == 0:
                    d.text((x0 - 0.15 * PX, cy + lh * 0.1), "•" if p.level == 0 else "–", fill=hex2t(p.runs[0][2]), font=font(p.size))
                cx = x0
                for t, b, c in ln:
                    d.text((cx, cy + lh * 0.1), t, fill=hex2t(c), font=font(p.size, b))
                    cx += font(p.size, b).getlength(t + " ")
                cy += lh
        # pptx paragraphs
        for i, p in enumerate(paras):
            para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            para.alignment = {"l": PP_ALIGN.LEFT, "c": PP_ALIGN.CENTER, "r": PP_ALIGN.RIGHT}[p.align]
            if i and p.sb:
                para.space_before = Pt(p.sb)
            para.line_spacing = 1.0
            pPr = para._p.get_or_add_pPr()
            if p.bullet:
                mar = int(Inches(0.17 + 0.17 * p.level))
                pPr.set("marL", str(mar)); pPr.set("indent", str(-int(Inches(0.15))))
                bf = pPr.makeelement(qn("a:buFont"), {"typeface": "Arial"}); pPr.append(bf)
                bc = pPr.makeelement(qn("a:buChar"), {"char": "•" if p.level == 0 else "–"}); pPr.append(bc)
            else:
                pPr.append(pPr.makeelement(qn("a:buNone"), {}))
            for t, b, c in p.runs:
                r = para.add_run(); r.text = t
                r.font.size = Pt(p.size); r.font.bold = b; r.font.name = FONT
                r.font.color.rgb = rgb(c)
        if name:
            tb.name = name
        return tb

    def notes(self, txt):
        s = self.cur[0]
        s.notes_slide.notes_text_frame.text = txt

    def save(self, path, preview_dir):
        self.prs.save(path)
        for i, im in enumerate(self.previews, 1):
            im.save(f"{preview_dir}/slide_{i:02d}.png")
