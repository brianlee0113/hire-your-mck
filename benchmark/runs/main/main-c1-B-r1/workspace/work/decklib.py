"""Tiny slide-spec layer with two back ends: python-pptx (deliverable) and PIL (layout preview + overflow check)."""
import re
from PIL import Image, ImageDraw, ImageFont
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.dml import MSO_LINE_DASH_STYLE
from pptx.oxml.ns import qn
from lxml import etree

W, H = 13.333, 7.5
FONT = "Arial"
FD = "/System/Library/Fonts/Supplemental/"
_fonts = {}
def pil_font(size, bold=False, italic=False, px_per_in=100):
    key = (size, bold, italic, px_per_in)
    if key not in _fonts:
        f = "Arial Bold Italic.ttf" if bold and italic else "Arial Bold.ttf" if bold else "Arial Italic.ttf" if italic else "Arial.ttf"
        _fonts[key] = ImageFont.truetype(FD + f, max(1, round(size / 72 * px_per_in)))
    return _fonts[key]

def text_w_in(s, size, bold=False, italic=False):
    f = pil_font(size, bold, italic, 1000)
    return f.getlength(s) / 1000

LINE_K = 1.2      # line height multiple of font size used by checker/preview
WRAP_SAFETY = 0.96  # PowerPoint wraps a bit earlier than PIL measures

def parse_runs(s, base):
    """'**bold**' and '__italic__' markup -> list of (text, style dict)."""
    out = []
    for part in re.split(r"(\*\*.+?\*\*|__.+?__)", s):
        if not part:
            continue
        st = dict(base)
        if part.startswith("**"):
            st["bold"] = True; part = part[2:-2]
        elif part.startswith("__"):
            st["italic"] = True; part = part[2:-2]
        out.append((part, st))
    return out

class Para:
    def __init__(self, text, size=None, bold=None, color=None, bullet=False, level=0, space_before=None, align=None, italic=False):
        self.text, self.size, self.bold, self.color = text, size, bold, color
        self.bullet, self.level, self.space_before, self.align, self.italic = bullet, level, space_before, align, italic

class T:
    def __init__(self, x, y, w, h, paras, size=12, color="333333", bold=False, align="l", valign="t",
                 fill=None, line=None, lw=0.75, inset=(0.06, 0.04), space=3, check=True, italic=False):
        if isinstance(paras, (str, Para)):
            paras = [paras]
        self.paras = [p if isinstance(p, Para) else Para(p) for p in paras]
        self.x, self.y, self.w, self.h = x, y, w, h
        self.size, self.color, self.bold, self.align, self.valign = size, color, bold, align, valign
        self.fill, self.line, self.lw, self.inset, self.space, self.check, self.italic = fill, line, lw, inset, space, check, italic

    def p_attr(self, p, k):
        v = getattr(p, k)
        return getattr(self, k) if v is None else v

    def layout(self):
        """Return list of lines: (indent_in, [(text, style)], size, align, space_before_pt, bullet_flag) and total height."""
        avail = (self.w - 2 * self.inset[0]) * WRAP_SAFETY
        lines = []; total = 0
        for i, p in enumerate(self.paras):
            size = self.p_attr(p, "size"); bold = self.p_attr(p, "bold"); color = self.p_attr(p, "color")
            align = self.p_attr(p, "align")
            italic = p.italic or self.italic
            sb = (self.space if p.space_before is None else p.space_before) if i > 0 else 0
            ind = (0.17 + 0.17 * p.level) if p.bullet else 0
            runs = parse_runs(p.text, dict(bold=bold, color=color, italic=italic, size=size))
            # tokenise into words keeping styles
            toks = []
            for txt, st in runs:
                for wtok in re.findall(r"\S+\s*|\s+", txt):
                    toks.append((wtok, st))
            cur = []; cur_w = 0; first = True
            if not toks:
                lines.append((ind, [], size, align, sb, p.bullet)); total += sb / 72 + size * LINE_K / 72; continue
            for wtok, st in toks:
                ww = text_w_in(wtok.rstrip(), size, st["bold"], st.get("italic"))
                wfull = text_w_in(wtok, size, st["bold"], st.get("italic"))
                if cur and cur_w + ww > avail - ind:
                    lines.append((ind, cur, size, align, sb if first else 0, p.bullet and first))
                    total += (sb if first else 0) / 72 + size * LINE_K / 72
                    first = False; cur = []; cur_w = 0
                cur.append((wtok, st)); cur_w += wfull
            lines.append((ind, cur, size, align, sb if first else 0, p.bullet and first))
            total += (sb if first else 0) / 72 + size * LINE_K / 72
        return lines, total

class R:
    def __init__(self, x, y, w, h, fill="FFFFFF", line=None, lw=0.75, shape="rect", dash=False):
        self.x, self.y, self.w, self.h, self.fill, self.line, self.lw, self.shape, self.dash = x, y, w, h, fill, line, lw, shape, dash

class L:
    def __init__(self, x1, y1, x2, y2, color="999999", w=1.0, dash=False):
        self.x1, self.y1, self.x2, self.y2, self.color, self.w, self.dash = x1, y1, x2, y2, color, w, dash

class P:
    def __init__(self, pts, color, w=2.0, dash=False):
        self.pts, self.color, self.w, self.dash = pts, color, w, dash

class Slide:
    def __init__(self, name):
        self.name = name; self.els = []; self.notes = ""
    def add(self, *els):
        for e in els:
            if isinstance(e, (list, tuple)):
                self.add(*e)
            else:
                self.els.append(e)
        return self

def rgb(h): return RGBColor.from_string(h)

# ---------------- PPTX back end ----------------
def _set_bullet(par, level):
    pPr = par._p.get_or_add_pPr()
    mar = int(Inches(0.17 + 0.17 * level)); pPr.set("marL", str(mar)); pPr.set("indent", str(-int(Inches(0.17))))
    for tag in ("a:buNone", "a:buChar", "a:buAutoNum"):
        for e in pPr.findall(qn(tag)):
            pPr.remove(e)
    bu = etree.SubElement(pPr, qn("a:buFont")); bu.set("typeface", "Arial")
    bc = etree.SubElement(pPr, qn("a:buChar")); bc.set("char", "•")

def _no_bullet(par):
    pPr = par._p.get_or_add_pPr()
    etree.SubElement(pPr, qn("a:buNone"))

ALIGN = {"l": PP_ALIGN.LEFT, "c": PP_ALIGN.CENTER, "r": PP_ALIGN.RIGHT}
VAL = {"t": MSO_ANCHOR.TOP, "m": MSO_ANCHOR.MIDDLE, "b": MSO_ANCHOR.BOTTOM}

def _line_fmt(ln, color, w, dash):
    if color is None:
        ln.fill.background()
    else:
        ln.color.rgb = rgb(color); ln.width = Pt(w)
        if dash:
            ln.dash_style = MSO_LINE_DASH_STYLE.DASH

def to_pptx(slides, path):
    prs = Presentation(); prs.slide_width = Inches(W); prs.slide_height = Inches(H)
    blank = prs.slide_layouts[6]
    for s in slides:
        sl = prs.slides.add_slide(blank)
        for e in s.els:
            if isinstance(e, R):
                shp = sl.shapes.add_shape(MSO_SHAPE.OVAL if e.shape == "oval" else MSO_SHAPE.RECTANGLE,
                                          Inches(e.x), Inches(e.y), Inches(e.w), Inches(e.h))
                if e.fill: shp.fill.solid(); shp.fill.fore_color.rgb = rgb(e.fill)
                else: shp.fill.background()
                _line_fmt(shp.line, e.line, e.lw, e.dash); shp.shadow.inherit = False
                shp.text_frame.text = ""
            elif isinstance(e, L):
                c = sl.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(e.x1), Inches(e.y1), Inches(e.x2), Inches(e.y2))
                _line_fmt(c.line, e.color, e.w, e.dash)
            elif isinstance(e, P):
                fb = sl.shapes.build_freeform(Inches(e.pts[0][0]), Inches(e.pts[0][1]), scale=1.0)
                fb.add_line_segments([(Inches(x), Inches(y)) for x, y in e.pts[1:]], close=False)
                shp = fb.convert_to_shape(); shp.fill.background(); _line_fmt(shp.line, e.color, e.w, e.dash)
                shp.shadow.inherit = False
            elif isinstance(e, T):
                tb = sl.shapes.add_textbox(Inches(e.x), Inches(e.y), Inches(e.w), Inches(e.h))
                if e.fill: tb.fill.solid(); tb.fill.fore_color.rgb = rgb(e.fill)
                if e.line: _line_fmt(tb.line, e.line, e.lw, False)
                tf = tb.text_frame; tf.word_wrap = True; tf.auto_size = None
                tf.margin_left = tf.margin_right = Inches(e.inset[0]); tf.margin_top = tf.margin_bottom = Inches(e.inset[1])
                tf.vertical_anchor = VAL[e.valign]
                for i, p in enumerate(e.paras):
                    par = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
                    par.alignment = ALIGN[e.p_attr(p, "align")]
                    par.line_spacing = 1.0
                    if i > 0:
                        par.space_before = Pt(e.space if p.space_before is None else p.space_before)
                    if p.bullet: _set_bullet(par, p.level)
                    else: _no_bullet(par)
                    for txt, st in parse_runs(p.text, dict(bold=e.p_attr(p, "bold"), color=e.p_attr(p, "color"),
                                                           italic=p.italic or e.italic, size=e.p_attr(p, "size"))):
                        r = par.add_run(); r.text = txt; f = r.font
                        f.name = FONT; f.size = Pt(st["size"]); f.bold = st["bold"]; f.italic = st.get("italic", False)
                        f.color.rgb = rgb(st["color"])
        if s.notes:
            sl.notes_slide.notes_text_frame.text = s.notes
    prs.save(path)

# ---------------- PIL preview + checks ----------------
def to_png(s, path, ppi=100):
    im = Image.new("RGB", (round(W * ppi), round(H * ppi)), "white"); d = ImageDraw.Draw(im)
    X = lambda v: round(v * ppi)
    issues = []
    for e in s.els:
        if isinstance(e, R):
            box = [X(e.x), X(e.y), X(e.x + e.w), X(e.y + e.h)]
            fill = "#" + e.fill if e.fill else None; out = "#" + e.line if e.line else None
            (d.ellipse if e.shape == "oval" else d.rectangle)(box, fill=fill, outline=out, width=max(1, round(e.lw / 72 * ppi)) if out else 0)
        elif isinstance(e, L):
            d.line([X(e.x1), X(e.y1), X(e.x2), X(e.y2)], fill="#" + e.color, width=max(1, round(e.w / 72 * ppi)))
        elif isinstance(e, P):
            d.line([(X(a), X(b)) for a, b in e.pts], fill="#" + e.color, width=max(1, round(e.w / 72 * ppi)))
        elif isinstance(e, T):
            if e.fill or e.line:
                d.rectangle([X(e.x), X(e.y), X(e.x + e.w), X(e.y + e.h)], fill=("#" + e.fill) if e.fill else None,
                            outline=("#" + e.line) if e.line else None)
            lines, total = e.layout()
            inner_h = e.h - 2 * e.inset[1]
            if e.check and total > inner_h + 0.01:
                issues.append(f"OVERFLOW {s.name}: '{e.paras[0].text[:50]}' needs {total:.2f}in, box {inner_h:.2f}in")
            if e.check and e.x + e.w > W - 0.2 + 1e-6 or e.y + e.h > H - 0.05:
                issues.append(f"OFFSLIDE {s.name}: '{e.paras[0].text[:40]}' x2={e.x+e.w:.2f} y2={e.y+e.h:.2f}")
            y = e.y + e.inset[1]
            if e.valign == "m": y += max(0, (inner_h - total) / 2)
            elif e.valign == "b": y += max(0, inner_h - total)
            for ind, runs, size, align, sb, bul in lines:
                y += sb / 72
                lw = sum(text_w_in(t, size, st["bold"], st.get("italic")) for t, st in runs)
                if runs: lw -= text_w_in(runs[-1][0], size) - text_w_in(runs[-1][0].rstrip(), size)
                avail = e.w - 2 * e.inset[0] - ind
                x = e.x + e.inset[0] + ind
                if align == "c": x += (avail - lw) / 2
                elif align == "r": x += avail - lw
                if bul:
                    d.text((X(e.x + e.inset[0] + 0.17 * 0), X(y)), "•", font=pil_font(size, px_per_in=ppi), fill="#333333")
                for t, st in runs:
                    d.text((X(x), X(y)), t, font=pil_font(size, st["bold"], st.get("italic"), ppi), fill="#" + st["color"])
                    x += text_w_in(t, size, st["bold"], st.get("italic"))
                y += size * LINE_K / 72
    im.save(path)
    return issues
