"""Minimal dual-target slide library: every primitive is written to a native
python-pptx shape AND drawn on a Pillow canvas, so the preview PNGs show the
real layout (PowerPoint/Chrome rendering is unavailable in this sandbox).
Text is wrapped with real Arial metrics; overflow is reported as a warning."""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR, MSO_AUTO_SIZE
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.oxml.ns import qn
from lxml import etree
from PIL import Image, ImageDraw, ImageFont

DPI = 120
W_IN, H_IN = 13.333, 7.5
FONT_DIR = "/System/Library/Fonts/Supplemental/"
FONT_FILES = {
    (False, False): "Arial.ttf",
    (True, False): "Arial Bold.ttf",
    (False, True): "Arial Italic.ttf",
    (True, True): "Arial Bold Italic.ttf",
}
_font_cache = {}
WARNINGS = []
LINE_K = 1.17     # exact line spacing = size * LINE_K
WRAP_SAFETY = 0.96  # preview wraps narrower than PowerPoint, to stay conservative


def pil_font(size, bold=False, italic=False):
    key = (round(size * 4) / 4, bold, italic)
    if key not in _font_cache:
        _font_cache[key] = ImageFont.truetype(FONT_DIR + FONT_FILES[(bold, italic)], size * DPI / 72)
    return _font_cache[key]


def hexrgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def px(v):
    return int(round(v * DPI))


class Deck:
    def __init__(self):
        self.prs = Presentation()
        self.prs.slide_width = Inches(W_IN)
        self.prs.slide_height = Inches(H_IN)
        self.slides = []

    def new_slide(self, name):
        s = self.prs.slides.add_slide(self.prs.slide_layouts[6])
        sl = Slide(s, name, len(self.slides) + 1)
        self.slides.append(sl)
        return sl

    def save(self, pptx_path, png_dir=None, pdf_path=None):
        self.prs.save(pptx_path)
        imgs = []
        for sl in self.slides:
            if png_dir:
                sl.img.save(f"{png_dir}/slide_{sl.num:02d}.png")
            imgs.append(sl.img.convert("RGB"))
        if pdf_path and imgs:
            imgs[0].save(pdf_path, save_all=True, append_images=imgs[1:], resolution=DPI)


def _norm_paras(paras, size, color, bold, italic, align):
    """paras: str | list of (str | dict). dict keys: runs/text, size, color, bold,
    italic, bullet(bool), align, space_after, indent(level in)"""
    if isinstance(paras, str):
        paras = [paras]
    out = []
    for p in paras:
        if isinstance(p, str):
            p = {"text": p}
        p = dict(p)
        psize = p.get("size", size)
        pcolor = p.get("color", color)
        pbold = p.get("bold", bold)
        pital = p.get("italic", italic)
        if "runs" in p:
            runs = []
            for r in p["runs"]:
                if isinstance(r, str):
                    r = (r, {})
                t, st = r
                runs.append((t, st.get("bold", pbold), st.get("italic", pital), st.get("color", pcolor)))
        else:
            runs = [(p["text"], pbold, pital, pcolor)]
        out.append({
            "runs": runs, "size": psize, "bullet": p.get("bullet", False),
            "align": p.get("align", align), "space_after": p.get("space_after", round(psize * 0.45, 1)),
            "indent": p.get("indent", 0.0),
        })
    return out


class Slide:
    def __init__(self, s, name, num):
        self.s = s
        self.name = name
        self.num = num
        self.img = Image.new("RGB", (px(W_IN), px(H_IN)), "white")
        self.d = ImageDraw.Draw(self.img)

    # ---------- shapes ----------
    def _strip_style(self, shape):
        st = shape._element.find(qn("p:style"))
        if st is not None:
            shape._element.remove(st)

    def rect(self, x, y, w, h, fill=None, line=None, lw=0.75, rounded=False, dash=False):
        shp = self.s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE if rounded else MSO_SHAPE.RECTANGLE,
                                      Inches(x), Inches(y), Inches(w), Inches(h))
        self._strip_style(shp)
        if rounded:
            shp.adjustments[0] = min(0.5, 0.06 / max(min(w, h), 0.01))
        if fill:
            shp.fill.solid()
            shp.fill.fore_color.rgb = RGBColor.from_string(fill.lstrip("#"))
        else:
            shp.fill.background()
        if line:
            shp.line.color.rgb = RGBColor.from_string(line.lstrip("#"))
            shp.line.width = Pt(lw)
            if dash:
                shp.line.dash_style = 4  # dash
        else:
            shp.line.fill.background()
        box = [px(x), px(y), px(x + w), px(y + h)]
        if rounded:
            self.d.rounded_rectangle(box, radius=px(0.06), fill=hexrgb(fill) if fill else None,
                                     outline=hexrgb(line) if line else None,
                                     width=max(1, int(lw * DPI / 72)) if line else 0)
        else:
            self.d.rectangle(box, fill=hexrgb(fill) if fill else None,
                             outline=hexrgb(line) if line else None,
                             width=max(1, int(lw * DPI / 72)) if line else 0)
        return shp

    def oval(self, x, y, d_, fill):
        shp = self.s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(x), Inches(y), Inches(d_), Inches(d_))
        self._strip_style(shp)
        shp.fill.solid()
        shp.fill.fore_color.rgb = RGBColor.from_string(fill.lstrip("#"))
        shp.line.fill.background()
        self.d.ellipse([px(x), px(y), px(x + d_), px(y + d_)], fill=hexrgb(fill))
        return shp

    def line(self, x1, y1, x2, y2, color="8A8986", lw=0.75, dash=False, arrow=False):
        c = self.s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1), Inches(x2), Inches(y2))
        self._strip_style(c)
        c.line.color.rgb = RGBColor.from_string(color.lstrip("#"))
        c.line.width = Pt(lw)
        if dash:
            c.line.dash_style = 4
        if arrow:
            ln = c.line._get_or_add_ln()
            te = etree.SubElement(ln, qn("a:tailEnd"))
            te.set("type", "triangle")
            te.set("w", "med")
            te.set("len", "med")
        wpx = max(1, int(round(lw * DPI / 72)))
        if dash:
            import math
            L = math.hypot(x2 - x1, y2 - y1)
            n = max(1, int(L / 0.08))
            for i in range(0, n, 2):
                a, b = i / n, min(1, (i + 1) / n)
                self.d.line([px(x1 + (x2 - x1) * a), px(y1 + (y2 - y1) * a),
                             px(x1 + (x2 - x1) * b), px(y1 + (y2 - y1) * b)], fill=hexrgb(color), width=wpx)
        else:
            self.d.line([px(x1), px(y1), px(x2), px(y2)], fill=hexrgb(color), width=wpx)
        if arrow:
            import math
            ang = math.atan2(y2 - y1, x2 - x1)
            L, Wd = 0.11, 0.055
            bx, by = x2 - L * math.cos(ang), y2 - L * math.sin(ang)
            pts = [(x2, y2), (bx + Wd * math.sin(ang), by - Wd * math.cos(ang)),
                   (bx - Wd * math.sin(ang), by + Wd * math.cos(ang))]
            self.d.polygon([(px(a), px(b)) for a, b in pts], fill=hexrgb(color))
        return c

    # ---------- text ----------
    def _layout(self, paras, width):
        """Return list of lines: (para_idx, [(text, font, color)], x_offset, size)"""
        lines_all = []
        for pi, p in enumerate(paras):
            size = p["size"]
            ind = p["indent"] + (0.17 * size / 11 if p["bullet"] else 0)
            avail = (width - ind) * DPI * WRAP_SAFETY
            # tokenize
            tokens = []
            for (t, b, it, col) in p["runs"]:
                f = pil_font(size, b, it)
                parts = t.split(" ")
                for k, w_ in enumerate(parts):
                    tokens.append((w_, f, col, k < len(parts) - 1))
            lines = []
            cur, curw = [], 0.0
            for (w_, f, col, sp) in tokens:
                ww = f.getlength(w_)
                spw = f.getlength(" ")
                if cur and curw + ww > avail and w_ != "":
                    lines.append(cur)
                    cur, curw = [], 0.0
                if w_ == "" and not cur:
                    continue
                cur.append((w_, f, col, sp))
                curw += ww + (spw if sp else 0)
                if ww > avail:
                    WARNINGS.append(f"[slide {self.num} {self.name}] word too wide: '{w_}'")
            if cur:
                lines.append(cur)
            if not lines:
                lines = [[]]
            for li, ln in enumerate(lines):
                lines_all.append((pi, ln, ind, size, li == 0))
        return lines_all

    def text(self, x, y, w, h, paras, size=12, color="1F1F1F", bold=False, italic=False,
             align="l", anchor="t", inset=0.04, fill=None, line=None, lw=0.75, tag=None):
        paras = _norm_paras(paras, size, color, bold, italic, align)
        if fill or line:
            self.rect(x, y, w, h, fill=fill, line=line, lw=lw)
        tb = self.s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.auto_size = MSO_AUTO_SIZE.NONE
        tf.margin_left = tf.margin_right = Inches(inset)
        tf.margin_top = tf.margin_bottom = Inches(inset)
        tf.vertical_anchor = {"t": MSO_ANCHOR.TOP, "m": MSO_ANCHOR.MIDDLE, "b": MSO_ANCHOR.BOTTOM}[anchor]
        AL = {"l": PP_ALIGN.LEFT, "c": PP_ALIGN.CENTER, "r": PP_ALIGN.RIGHT}
        for i, p in enumerate(paras):
            para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            para.alignment = AL[p["align"]]
            para.line_spacing = Pt(p["size"] * LINE_K)
            para.space_after = Pt(p["space_after"] if i < len(paras) - 1 else 0)
            for (t, b, it, col) in p["runs"]:
                r = para.add_run()
                r.text = t
                r.font.name = "Arial"
                r.font.size = Pt(p["size"])
                r.font.bold = b
                r.font.italic = it
                r.font.color.rgb = RGBColor.from_string(col.lstrip("#"))
            pPr = para._p.get_or_add_pPr()
            bullet_ind = 0.17 * p["size"] / 11
            if p["bullet"]:
                pPr.set("marL", str(Inches(p["indent"] + bullet_ind)))
                pPr.set("indent", str(-Inches(bullet_ind)))
                bf = etree.SubElement(pPr, qn("a:buFont"))
                bf.set("typeface", "Arial")
                bc = etree.SubElement(pPr, qn("a:buChar"))
                bc.set("char", "•")
            elif p["indent"]:
                pPr.set("marL", str(Inches(p["indent"])))
                etree.SubElement(pPr, qn("a:buNone"))
            else:
                etree.SubElement(pPr, qn("a:buNone"))
        # ---- preview ----
        iw = w - 2 * inset
        lines = self._layout(paras, iw)
        total = 0.0
        for k, (pi, ln, ind, size, first) in enumerate(lines):
            total += size * LINE_K / 72
            last_of_para = (k == len(lines) - 1) or (lines[k + 1][0] != pi)
            if last_of_para and pi < len(paras) - 1:
                total += paras[pi]["space_after"] / 72
        avail_h = h - 2 * inset
        if total > avail_h + 0.01:
            first_txt = paras[0]["runs"][0][0][:50]
            WARNINGS.append(f"[slide {self.num} {self.name}] text overflow {total:.2f}in > {avail_h:.2f}in: '{first_txt}'")
        if anchor == "t":
            cy = y + inset
        elif anchor == "m":
            cy = y + inset + (avail_h - total) / 2
        else:
            cy = y + inset + (avail_h - total)
        for k, (pi, ln, ind, size, first) in enumerate(lines):
            p = paras[pi]
            lh = size * LINE_K / 72
            lw_px = sum(f.getlength(t_) + (f.getlength(" ") if sp else 0) for (t_, f, c_, sp) in ln)
            if ln and ln[-1][3]:
                lw_px -= ln[-1][1].getlength(" ")
            lw_px /= WRAP_SAFETY  # PowerPoint lays out with real width
            x0 = x + inset + ind
            if p["align"] == "c":
                x0 = x + inset + ind + (iw - ind - lw_px / DPI) / 2
            elif p["align"] == "r":
                x0 = x + w - inset - lw_px / DPI
            base_y = cy + lh * 0.80
            if p["bullet"] and first:
                bfnt = pil_font(size)
                self.d.text((px(x + inset + p["indent"]), px(base_y)), "•", font=bfnt,
                            fill=hexrgb(p["runs"][0][3]), anchor="ls")
            cx = px(x0)
            for (t_, f, col, sp) in ln:
                self.d.text((cx, px(base_y)), t_, font=f, fill=hexrgb(col), anchor="ls")
                cx += (f.getlength(t_) + (f.getlength(" ") if sp else 0)) / WRAP_SAFETY
            cy += lh
            last_of_para = (k == len(lines) - 1) or (lines[k + 1][0] != pi)
            if last_of_para:
                cy += p["space_after"] / 72
        return tb

    def text_height(self, w, paras, size=12, bold=False, inset=0.04):
        paras = _norm_paras(paras, size, "000000", bold, False, "l")
        lines = self._layout(paras, w - 2 * inset)
        total = 0.0
        for k, (pi, ln, ind, sz, first) in enumerate(lines):
            total += sz * LINE_K / 72
            last_of_para = (k == len(lines) - 1) or (lines[k + 1][0] != pi)
            if last_of_para and pi < len(paras) - 1:
                total += paras[pi]["space_after"] / 72
        return total + 2 * inset
