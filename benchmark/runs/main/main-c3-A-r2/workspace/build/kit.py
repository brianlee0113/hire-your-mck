"""Tiny layout kit: every element is emitted to python-pptx AND to a PIL preview
from the same coordinates, so the preview can be used for visual QA."""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn
from PIL import Image, ImageDraw, ImageFont
from lxml import etree

W, H = 13.333, 7.5
DPI = 120
FONT = "Arial"
FDIR = "/System/Library/Fonts/Supplemental/"
FFILES = {False: FDIR + "Arial.ttf", True: FDIR + "Arial Bold.ttf"}
_fcache = {}
WARN = []

INK = "#0b0b0b"; INK2 = "#52514e"; MUTED = "#898781"; GRID = "#e1e0d9"; AXIS = "#c3c2b7"
BLUE = "#2a78d6"; BLUE_D = "#184f95"; BLUE_L = "#cde2fb"; GRAYBAR = "#c9c8c1"; PANEL = "#f4f3ef"
GOOD = "#0ca30c"; GOOD_T = "#006300"; CRIT = "#d03b3b"; WARNC = "#fab219"; SER = "#ec835a"


FALLBACK = FDIR + "Arial Unicode.ttf"


def font(size_pt, bold=False):
    k = (round(size_pt * DPI / 72), bold)
    if k not in _fcache:
        _fcache[k] = ImageFont.truetype(FFILES[bold], k[0])
    return _fcache[k]


def rgb(h):
    h = h.lstrip("#"); return RGBColor(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def px(v):
    return int(round(v * DPI))


def norm_para(p, base):
    """paragraph -> dict(runs=[(text, style)], bullet, space_after, align)"""
    if isinstance(p, str):
        p = {"runs": [(p, {})]}
    elif isinstance(p, list):
        p = {"runs": p}
    elif isinstance(p, tuple):
        p = {"runs": [p]}
    runs = []
    for r in p["runs"]:
        if isinstance(r, str):
            r = (r, {})
        st = dict(base); st.update(r[1]); runs.append((r[0], st))
    out = dict(p); out["runs"] = runs
    out.setdefault("bullet", base.get("bullet", False))
    out.setdefault("space_after", base.get("space_after", 4))
    out.setdefault("align", base.get("align", "l"))
    out.setdefault("indent", base.get("indent", 0.18))
    return out


def wrap_para(p, width_in):
    """returns list of lines; each line = list of (text, style) chunks; plus line height pt"""
    words = []  # (word, style, space_before)
    pending_space = False
    for text, st in p["runs"]:
        parts = text.split(" ")
        for i, w in enumerate(parts):
            sp = pending_space or i > 0
            if w == "":
                if i > 0:
                    pending_space = True
                continue
            words.append((w, st, sp)); pending_space = False
        if text.endswith(" "):
            pending_space = True
    avail = (width_in - (p["indent"] if p["bullet"] else 0)) * DPI * 0.965  # safety margin
    lines, cur, curw = [], [], 0
    for idx, (w, st, sp) in enumerate(words):
        f = font(st["size"], st.get("bold", False))
        ww = f.getlength(w)
        spw = f.getlength(" ") if (cur and sp) else 0
        if cur and sp and curw + spw + ww > avail:
            lines.append(cur); cur, curw = [], 0; spw = 0
        cur.append((("" if not (cur and sp) else " ") + w, st)); curw += spw + ww
    if cur:
        lines.append(cur)
    maxsize = max(st["size"] for _, st in p["runs"])
    return lines, maxsize


class Slide:
    def __init__(self, deck, slide):
        self.deck, self.s = deck, slide
        self.img = Image.new("RGB", (px(W), px(H)), "white")
        self.d = ImageDraw.Draw(self.img)
        self.name = ""

    # ---------- primitives
    def rect(self, x, y, w, h, fill=None, line=None, lw=0.75, shape=MSO_SHAPE.RECTANGLE):
        sh = self.s.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
        sh.shadow.inherit = False
        if fill:
            sh.fill.solid(); sh.fill.fore_color.rgb = rgb(fill)
        else:
            sh.fill.background()
        if line:
            sh.line.color.rgb = rgb(line); sh.line.width = Pt(lw)
        else:
            sh.line.fill.background()
        if shape == MSO_SHAPE.OVAL:
            self.d.ellipse([px(x), px(y), px(x + w), px(y + h)], fill=fill, outline=line)
        else:
            self.d.rectangle([px(x), px(y), px(x + w) - 1, px(y + h) - 1], fill=fill, outline=line,
                             width=max(1, round(lw * DPI / 72)) if line else 0)
        return sh

    def line(self, x1, y1, x2, y2, color=AXIS, lw=0.75, dash=False):
        c = self.s.shapes.add_connector(1, Inches(x1), Inches(y1), Inches(x2), Inches(y2))
        c.line.color.rgb = rgb(color); c.line.width = Pt(lw)
        if dash:
            ln = c.line._get_or_add_ln()
            pd = etree.SubElement(ln, qn("a:prstDash")); pd.set("val", "dash")
        wpx = max(1, round(lw * DPI / 72))
        if dash:
            import math
            L = math.hypot(x2 - x1, y2 - y1); n = int(L / 0.08)
            for i in range(0, n, 2):
                a, b = i / n, min(1, (i + 1) / n)
                self.d.line([px(x1 + (x2 - x1) * a), px(y1 + (y2 - y1) * a), px(x1 + (x2 - x1) * b), px(y1 + (y2 - y1) * b)], fill=color, width=wpx)
        else:
            self.d.line([px(x1), px(y1), px(x2), px(y2)], fill=color, width=wpx)

    def text(self, x, y, w, h, paras, size=13, color=INK, bold=False, align="l", valign="t",
             bullet=False, space_after=4, ls=1.2, name=None, check=True):
        base = {"size": size, "color": color, "bold": bold, "bullet": bullet,
                "space_after": space_after, "align": align}
        if not isinstance(paras, list) or (paras and isinstance(paras[0], tuple)):
            paras = [paras]
        P = [norm_para(p, base) for p in paras]
        # ---- measure
        laid = []; total = 0
        for i, p in enumerate(P):
            lines, ms = wrap_para(p, w)
            lh = ms * ls / 72
            laid.append((p, lines, lh))
            total += lh * len(lines) + (p["space_after"] / 72 if i < len(P) - 1 else 0)
        if check and total > h + 0.02:
            WARN.append(f"[{self.deck.idx}] overflow {total:.2f}in > {h:.2f}in : {P[0]['runs'][0][0][:50]}")
        # ---- pptx
        tb = self.s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
        tf = tb.text_frame; tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        tf.vertical_anchor = {"t": MSO_ANCHOR.TOP, "m": MSO_ANCHOR.MIDDLE, "b": MSO_ANCHOR.BOTTOM}[valign]
        bodyPr = tf._txBody.find(qn("a:bodyPr"))
        for el in bodyPr.findall(qn("a:spAutoFit")) + bodyPr.findall(qn("a:normAutofit")):
            bodyPr.remove(el)
        for i, (p, lines, lh) in enumerate(laid):
            para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            para.alignment = {"l": PP_ALIGN.LEFT, "c": PP_ALIGN.CENTER, "r": PP_ALIGN.RIGHT}[p["align"]]
            ms = max(st["size"] for _, st in p["runs"])
            para.line_spacing = Pt(ms * ls)
            para.space_after = Pt(p["space_after"] if i < len(laid) - 1 else 0)
            para.space_before = Pt(0)
            pPr = para._p.get_or_add_pPr()
            if p["bullet"]:
                ind = Emu(Inches(p["indent"]))
                pPr.set("marL", str(ind)); pPr.set("indent", str(-ind))
                bf = etree.SubElement(pPr, qn("a:buFont")); bf.set("typeface", "Arial")
                bc = etree.SubElement(pPr, qn("a:buChar")); bc.set("char", "•")
            else:
                etree.SubElement(pPr, qn("a:buNone"))
            for t, st in p["runs"]:
                r = para.add_run(); r.text = t
                r.font.name = FONT; r.font.size = Pt(st["size"]); r.font.bold = st.get("bold", False)
                r.font.color.rgb = rgb(st["color"])
                if st.get("italic"):
                    r.font.italic = True
        if name:
            tb.name = name
        # ---- preview
        oy = {"t": 0, "m": (h - total) / 2, "b": h - total}[valign]
        cy = y + oy
        for p, lines, lh in laid:
            ind = p["indent"] if p["bullet"] else 0
            for li, ln in enumerate(lines):
                lw_ = sum(font(st["size"], st.get("bold", False)).getlength(t) for t, st in ln)
                avail = (w - ind) * DPI
                if p["align"] == "c":
                    cx = px(x + ind) + (avail - lw_) / 2
                elif p["align"] == "r":
                    cx = px(x + w) - lw_
                else:
                    cx = px(x + ind)
                base_y = px(cy) + (lh * DPI) * 0.8
                if p["bullet"] and li == 0:
                    st0 = p["runs"][0][1]
                    self.d.text((px(x), base_y), "•", font=font(st0["size"]), fill=st0["color"], anchor="ls")
                for t, st in ln:
                    f = font(st["size"], st.get("bold", False))
                    for ch in t:
                        ff = f if (ord(ch) < 0x2190 or ch in "→≤≥−–—’“”…×·•") else ImageFont.truetype(FALLBACK, round(st["size"] * DPI / 72))
                        self.d.text((cx, base_y), ch, font=ff, fill=st["color"], anchor="ls")
                        cx += ff.getlength(ch)
                cy += lh
            cy += p["space_after"] / 72
        return total

    def notes(self, t):
        self.s.notes_slide.notes_text_frame.text = t

    # ---------- template pieces
    def header(self, section, title):
        self.text(0.6, 0.38, 10, 0.25, section.upper(), size=10, color=BLUE, bold=True)
        self.text(0.6, 0.62, 12.1, 0.95, title, size=22, bold=True, color=INK, ls=1.15)
        self.line(0.6, 1.62, 12.73, 1.62, color=GRID, lw=0.75)

    def footer(self, source):
        self.text(0.6, 7.0, 11.2, 0.3, source, size=8.5, color=MUTED)
        self.text(12.2, 7.0, 0.53, 0.3, str(self.deck.idx), size=8.5, color=MUTED, align="r")


class Deck:
    def __init__(self):
        self.prs = Presentation()
        self.prs.slide_width = Inches(W); self.prs.slide_height = Inches(H)
        self.slides = []; self.idx = 0

    def new(self):
        self.idx += 1
        s = Slide(self, self.prs.slides.add_slide(self.prs.slide_layouts[6]))
        self.slides.append(s)
        return s

    def save(self, path, preview_dir):
        self.prs.save(path)
        import os
        os.makedirs(preview_dir, exist_ok=True)
        for i, s in enumerate(self.slides, 1):
            s.img.save(f"{preview_dir}/slide_{i:02d}.png")
