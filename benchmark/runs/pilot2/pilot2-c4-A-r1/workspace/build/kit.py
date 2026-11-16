"""Small slide kit: every element is added to the PPTX *and* recorded so a PIL
preview can be rendered and text overflow can be checked without PowerPoint."""
from pptx import Presentation
from pptx.util import Emu, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.oxml.ns import qn
from lxml import etree
from PIL import Image, ImageDraw, ImageFont

IN = 914400
W_IN, H_IN = 13.333, 7.5
FONT = "Arial"
FONT_FILES = {False: "/System/Library/Fonts/Supplemental/Arial.ttf",
              True: "/System/Library/Fonts/Supplemental/Arial Bold.ttf"}

INK = "0B0B0B"; SEC = "52514E"; MUTED = "8A8984"; RULE = "D9D8D3"; PANEL = "F4F3EF"
BLUE = "2A78D6"; BLUE_D = "1C5CAB"; BLUE_L = "CDE2FB"; ORANGE = "EB6834"; GRAY = "B9B8B2"
WHITE = "FFFFFF"

_fonts = {}
def font(size, bold=False, scale=1.0):
    k = (round(size * scale, 2), bold)
    if k not in _fonts:
        _fonts[k] = ImageFont.truetype(FONT_FILES[bold], max(1.0, float(size * scale)))
    return _fonts[k]

def rgb(h):
    return RGBColor.from_string(h)


class Deck:
    def __init__(self):
        self.prs = Presentation()
        self.prs.slide_width = Emu(int(W_IN * IN))
        self.prs.slide_height = Emu(int(H_IN * IN))
        self.slides = []  # list of (slide, ops)
        self.warnings = []

    def new(self):
        s = self.prs.slides.add_slide(self.prs.slide_layouts[6])
        ops = []
        self.slides.append((s, ops))
        return Slide(self, s, ops, len(self.slides))

    def save(self, path):
        self.prs.save(path)

    # ---------------- preview -----------------
    def render(self, outdir, dpi=110):
        paths = []
        for i, (_, ops) in enumerate(self.slides, 1):
            sc = dpi / 72.0
            img = Image.new("RGB", (int(W_IN * dpi), int(H_IN * dpi)), "white")
            d = ImageDraw.Draw(img)
            for op in ops:
                kind = op[0]
                if kind == "rect":
                    _, x, y, w, h, fill, line = op
                    d.rectangle([x * dpi, y * dpi, (x + w) * dpi, (y + h) * dpi],
                                fill="#" + fill if fill else None,
                                outline="#" + line if line else None)
                elif kind == "oval":
                    _, x, y, w, h, fill = op
                    d.ellipse([x * dpi, y * dpi, (x + w) * dpi, (y + h) * dpi], fill="#" + fill)
                elif kind == "line":
                    _, x1, y1, x2, y2, color, wpt = op
                    d.line([x1 * dpi, y1 * dpi, x2 * dpi, y2 * dpi], fill="#" + color,
                           width=max(1, int(round(wpt * sc))))
                elif kind == "text":
                    _, x, y, w, h, layout, anchor = op
                    total = sum(l["h"] for l in layout)
                    if anchor == "middle":
                        cy = y * 72 + (h * 72 - total) / 2
                    elif anchor == "bottom":
                        cy = y * 72 + h * 72 - total
                    else:
                        cy = y * 72
                    for l in layout:
                        if l["text"]:
                            # draw runs
                            lw = l["w"]
                            if l["align"] == "center":
                                cx = x * 72 + l["indent"] + (w * 72 - l["indent"] - lw) / 2
                            elif l["align"] == "right":
                                cx = x * 72 + w * 72 - lw
                            else:
                                cx = x * 72 + l["indent"]
                            for (t, size, bold, color) in l["runs"]:
                                f = font(size, bold, sc)
                                d.text((cx * sc, (cy + l["base_off"]) * sc), t, font=f,
                                       fill="#" + color, anchor="ls")
                                cx += font(size, bold).getlength(t)
                        if l.get("bullet"):
                            b, size, color = l["bullet"]
                            f = font(size, False, sc)
                            d.text(((x * 72 + l["bx"]) * sc, (cy + l["base_off"]) * sc), b,
                                   font=f, fill="#" + color, anchor="ls")
                        cy += l["h"]
            p = f"{outdir}/slide-{i:02d}.png"
            img.save(p)
            paths.append(p)
        return paths


def _wrap_runs(runs, width_pt):
    """runs: list of (text, size, bold, color). Returns list of lines (list of runs)."""
    # tokenise into words keeping style
    tokens = []
    for (t, size, bold, color) in runs:
        parts = t.split(" ")
        for j, p in enumerate(parts):
            tok = p + (" " if j < len(parts) - 1 else "")
            if tok:
                tokens.append((tok, size, bold, color))
    lines, cur, curw = [], [], 0.0
    for tok in tokens:
        tw = font(tok[1], tok[2]).getlength(tok[0].rstrip(" "))
        tw_full = font(tok[1], tok[2]).getlength(tok[0])
        if cur and curw + tw > width_pt:
            lines.append(cur)
            cur, curw = [], 0.0
        cur.append(tok)
        curw += tw_full
    if cur:
        lines.append(cur)
    return lines


class Slide:
    def __init__(self, deck, s, ops, num):
        self.deck, self.s, self.ops, self.num = deck, s, ops, num

    # ---- primitives ----
    def rect(self, x, y, w, h, fill=None, line=None, line_w=0.75):
        shp = self.s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Emu(int(x * IN)), Emu(int(y * IN)),
                                      Emu(max(1, int(w * IN))), Emu(max(1, int(h * IN))))
        if fill:
            shp.fill.solid(); shp.fill.fore_color.rgb = rgb(fill)
        else:
            shp.fill.background()
        if line:
            shp.line.color.rgb = rgb(line); shp.line.width = Pt(line_w)
        else:
            shp.line.fill.background()
        shp.shadow.inherit = False
        self.ops.append(("rect", x, y, w, h, fill, line))
        return shp

    def oval(self, x, y, w, h, fill):
        shp = self.s.shapes.add_shape(MSO_SHAPE.OVAL, Emu(int(x * IN)), Emu(int(y * IN)),
                                      Emu(int(w * IN)), Emu(int(h * IN)))
        shp.fill.solid(); shp.fill.fore_color.rgb = rgb(fill)
        shp.line.fill.background(); shp.shadow.inherit = False
        self.ops.append(("oval", x, y, w, h, fill))
        return shp

    def line(self, x1, y1, x2, y2, color=RULE, w=0.75, dash=False):
        c = self.s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Emu(int(x1 * IN)), Emu(int(y1 * IN)),
                                        Emu(int(x2 * IN)), Emu(int(y2 * IN)))
        c.line.color.rgb = rgb(color); c.line.width = Pt(w)
        if dash:
            ln = c.line._get_or_add_ln()
            pd = etree.SubElement(ln, qn("a:prstDash")); pd.set("val", "dash")
        self.ops.append(("line", x1, y1, x2, y2, color, w))
        return c

    def text(self, x, y, w, h, paras, size=12, color=INK, bold=False, align="left",
             anchor="top", space_after=4, line_spacing=1.0, name=None, check=True):
        """paras: str | list of para. para: str | dict(runs=[...] or text=..., size, bold, color,
        bullet=True/level, align, space_after). Runs: (text, {opts}) or str with **bold** markup."""
        if isinstance(paras, str):
            paras = [paras]
        tb = self.s.shapes.add_textbox(Emu(int(x * IN)), Emu(int(y * IN)), Emu(int(w * IN)), Emu(int(h * IN)))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        tf.vertical_anchor = {"top": MSO_ANCHOR.TOP, "middle": MSO_ANCHOR.MIDDLE, "bottom": MSO_ANCHOR.BOTTOM}[anchor]
        bodyPr = tf._txBody.find(qn("a:bodyPr"))
        for child in list(bodyPr):
            bodyPr.remove(child)  # no autofit
        layout = []
        first = True
        for para in paras:
            if isinstance(para, str):
                para = {"text": para}
            psize = para.get("size", size); pcol = para.get("color", color); pbold = para.get("bold", bold)
            palign = para.get("align", align); psa = para.get("space_after", space_after)
            bullet = para.get("bullet", False)
            runs = para.get("runs")
            if runs is None:
                runs = parse_markup(para["text"])
            norm = []
            for r in runs:
                if isinstance(r, str):
                    r = (r, {})
                t, o = r
                norm.append((t, o.get("size", psize), o.get("bold", pbold), o.get("color", pcol)))
            p = tf.paragraphs[0] if first else tf.add_paragraph()
            first = False
            p.alignment = {"left": PP_ALIGN.LEFT, "center": PP_ALIGN.CENTER, "right": PP_ALIGN.RIGHT}[palign]
            p.space_after = Pt(psa)
            p.line_spacing = line_spacing
            indent_pt = 0
            if bullet:
                lvl = 1 if bullet is True else bullet
                indent_pt = 12 * lvl
                pPr = p._p.get_or_add_pPr()
                pPr.set("marL", str(int(indent_pt * 12700)))
                pPr.set("indent", str(int(-11 * 12700)))
                bc = etree.SubElement(pPr, qn("a:buClr"))
                sc_ = etree.SubElement(bc, qn("a:srgbClr")); sc_.set("val", para.get("bullet_color", SEC))
                bf = etree.SubElement(pPr, qn("a:buFont")); bf.set("typeface", FONT)
                bu = etree.SubElement(pPr, qn("a:buChar")); bu.set("char", "–" if lvl > 1 else "•")
            for (t, sz, b, c) in norm:
                run = p.add_run(); run.text = t
                run.font.name = FONT; run.font.size = Pt(sz); run.font.bold = b
                run.font.color.rgb = rgb(c)
            # layout for preview + fit check
            avail = w * 72 - indent_pt
            lines = _wrap_runs(norm, avail * 0.985) if norm else [[]]
            maxsize = max([r[1] for r in norm] or [psize])
            lh = maxsize * 1.2 * line_spacing
            for li, ln in enumerate(lines):
                lw = sum(font(r[1], r[2]).getlength(r[0]) for r in ln)
                if ln:
                    last = ln[-1]
                    lw -= font(last[1], last[2]).getlength(" ") if last[0].endswith(" ") else 0
                entry = {"text": bool(ln), "runs": [(r[0], r[1], r[2], r[3]) for r in ln], "w": lw,
                         "h": lh + (psa if li == len(lines) - 1 else 0), "indent": indent_pt,
                         "align": palign, "base_off": maxsize * 0.95 * line_spacing + (lh - maxsize * 1.2 * line_spacing) / 2}
                if bullet and li == 0:
                    entry["bullet"] = ("–" if (bullet is not True and bullet > 1) else "•", psize, para.get("bullet_color", SEC))
                    entry["bx"] = indent_pt - 11
                layout.append(entry)
        total = sum(l["h"] for l in layout) - (layout[-1]["h"] - (layout[-1]["h"] - psa) if layout else 0)
        total = sum(l["h"] for l in layout) - psa
        if check and total > h * 72 + 1:
            self.deck.warnings.append(f"slide {self.num}: text overflow {total:.0f}pt > {h*72:.0f}pt in box '{(name or str(paras)[:50])}'")
        for l in layout:
            if l["w"] > (w * 72 - l["indent"]) + 1:
                self.deck.warnings.append(f"slide {self.num}: word too wide in '{(name or str(paras)[:40])}'")
        self.ops.append(("text", x, y, w, h, layout, anchor))
        self.last_text_height = total / 72
        return tb


def parse_markup(s):
    """'**bold**' segments -> runs."""
    out = []
    parts = s.split("**")
    for i, p in enumerate(parts):
        if p:
            out.append((p, {"bold": True} if i % 2 == 1 else {}))
    return out
