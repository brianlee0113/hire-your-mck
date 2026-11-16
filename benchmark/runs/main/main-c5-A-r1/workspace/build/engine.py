"""Tiny layout engine: one slide spec -> PowerPoint (python-pptx) + PNG preview (PIL).

All coordinates in inches on a 13.333 x 7.5 canvas. Text boxes have zero insets and
exact line spacing so the PIL preview wraps text the same way PowerPoint does
(close enough to catch overflow and collisions).
"""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.oxml.ns import qn
from PIL import Image, ImageDraw, ImageFont
import copy

W, H = 13.333, 7.5
DPI = 120
FONT_DIR = "/System/Library/Fonts/Supplemental/"
FONTS = {
    (False, False): FONT_DIR + "Arial.ttf",
    (True, False): FONT_DIR + "Arial Bold.ttf",
    (False, True): FONT_DIR + "Arial Italic.ttf",
    (True, True): FONT_DIR + "Arial Bold Italic.ttf",
}
_font_cache = {}
LINE = 1.18  # line height multiple


def font(size, bold=False, italic=False):
    key = (round(size * DPI / 72), bold, italic)
    if key not in _font_cache:
        _font_cache[key] = ImageFont.truetype(FONTS[(bold, italic)], key[0])
    return _font_cache[key]


def hexrgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


WARNINGS = []


def norm_paras(paras, base):
    """paras: str | list[para]; para: str | dict(runs=[...], **opts) | list[run]; run: str | (text, opts)."""
    if isinstance(paras, str):
        paras = [paras]
    out = []
    for p in paras:
        if isinstance(p, str):
            p = {"runs": [p]}
        elif isinstance(p, list):
            p = {"runs": p}
        p = dict(p)
        opts = {k: v for k, v in base.items()}
        opts.update({k: v for k, v in p.items() if k != "runs"})
        runs = []
        for r in p["runs"]:
            if isinstance(r, str):
                r = (r, {})
            ro = {k: opts[k] for k in ("size", "bold", "italic", "color")}
            ro.update(r[1])
            runs.append((r[0], ro))
        opts["runs"] = runs
        out.append(opts)
    return out


class Slide:
    def __init__(self, deck):
        self.items = []
        self.deck = deck
        self.notes = ""

    def rect(self, x, y, w, h, fill=None, line=None, lw=0.75, shape="rect"):
        self.items.append(("rect", dict(x=x, y=y, w=w, h=h, fill=fill, line=line, lw=lw, shape=shape)))

    def line(self, x1, y1, x2, y2, color="#c3c2b7", lw=0.75):
        self.items.append(("line", dict(x1=x1, y1=y1, x2=x2, y2=y2, color=color, lw=lw)))

    def text(self, x, y, w, h, paras, size=12, bold=False, italic=False, color="#111827",
             align="l", valign="t", space=0, bullet=False, indent=0.18, name=None):
        base = dict(size=size, bold=bold, italic=italic, color=color, align=align, space=space,
                    bullet=bullet, indent=indent)
        self.items.append(("text", dict(x=x, y=y, w=w, h=h, paras=norm_paras(paras, base), valign=valign,
                                        name=name)))


class Deck:
    def __init__(self):
        self.slides = []

    def new(self):
        s = Slide(self)
        self.slides.append(s)
        return s

    # ---------------- layout (shared by both back-ends) ----------------
    @staticmethod
    def layout_text(item):
        """Returns list of lines: (para, [(text, ro)], line_height_in, x_offset_in, first_line_of_para) and total h."""
        w_px = item["w"] * DPI
        lines = []
        total = 0.0
        for pi, p in enumerate(item["paras"]):
            ind = p["indent"] if p["bullet"] else 0
            avail = w_px - ind * DPI
            maxsize = max(ro["size"] for _, ro in p["runs"])
            lh = maxsize * LINE / 72
            sp = (p["space"] / 72) if pi > 0 else 0
            total += sp
            # tokenise into words keeping run styles
            tokens = []
            for t, ro in p["runs"]:
                parts = t.split(" ")
                for i, part in enumerate(parts):
                    if i > 0:
                        tokens.append((" ", ro))
                    if part:
                        tokens.append((part, ro))
            cur, cur_w = [], 0.0
            para_lines = []
            for tok, ro in tokens:
                f = font(ro["size"], ro["bold"], ro["italic"])
                tw = f.getlength(tok)
                if tok == " ":
                    if cur:
                        cur.append((tok, ro)); cur_w += tw
                    continue
                if cur and cur_w + tw > avail + 0.5:
                    # strip trailing space
                    while cur and cur[-1][0] == " ":
                        cur_w -= font(cur[-1][1]["size"], cur[-1][1]["bold"], cur[-1][1]["italic"]).getlength(" ")
                        cur.pop()
                    para_lines.append((cur, cur_w))
                    cur, cur_w = [], 0.0
                if tw > avail + 0.5:
                    WARNINGS.append(f"word wider than box: '{tok}' ({tw/DPI:.2f}in > {avail/DPI:.2f}in)")
                cur.append((tok, ro)); cur_w += tw
            while cur and cur[-1][0] == " ":
                cur.pop()
            para_lines.append((cur, cur_w))
            for li, (ln, lw_) in enumerate(para_lines):
                lines.append((p, ln, lh, ind, li == 0, lw_, sp if li == 0 else 0))
                total += lh
        return lines, total

    # ---------------- PNG back-end ----------------
    def render_png(self, idx, path):
        s = self.slides[idx]
        img = Image.new("RGB", (int(W * DPI), int(H * DPI)), "white")
        d = ImageDraw.Draw(img)
        P = lambda v: int(round(v * DPI))
        for kind, it in s.items:
            if kind == "rect":
                box = [P(it["x"]), P(it["y"]), P(it["x"] + it["w"]), P(it["y"] + it["h"])]
                if box[2] <= box[0] or box[3] <= box[1]:
                    continue
                fill = hexrgb(it["fill"]) if it["fill"] else None
                outline = hexrgb(it["line"]) if it["line"] else None
                width = max(1, int(round(it["lw"] * DPI / 72))) if outline else 0
                if it["shape"] == "ellipse":
                    d.ellipse(box, fill=fill, outline=outline, width=width)
                elif it["shape"] == "round":
                    d.rounded_rectangle(box, radius=P(0.08), fill=fill, outline=outline, width=width)
                else:
                    d.rectangle(box, fill=fill, outline=outline, width=width)
            elif kind == "line":
                d.line([P(it["x1"]), P(it["y1"]), P(it["x2"]), P(it["y2"])], fill=hexrgb(it["color"]),
                       width=max(1, int(round(it["lw"] * DPI / 72))))
            elif kind == "text":
                lines, total = self.layout_text(it)
                if total > it["h"] + 0.02:
                    snippet = it["paras"][0]["runs"][0][0][:40] if it["paras"][0]["runs"] else ""
                    WARNINGS.append(f"slide {idx+1}: text overflows box by {total-it['h']:.2f}in: '{snippet}'")
                if it["x"] + it["w"] > W - 0.2 or it["y"] + it["h"] > H - 0.05:
                    WARNINGS.append(f"slide {idx+1}: text box near/over slide edge at x={it['x']:.2f}, y={it['y']:.2f}")
                y0 = it["y"]
                if it["valign"] == "m":
                    y0 = it["y"] + (it["h"] - total) / 2
                elif it["valign"] == "b":
                    y0 = it["y"] + it["h"] - total
                y = y0
                for p, ln, lh, ind, first, lw_, sp in lines:
                    y += sp
                    if p["align"] == "c":
                        x = it["x"] * DPI + ind * DPI + (it["w"] * DPI - ind * DPI - lw_) / 2
                    elif p["align"] == "r":
                        x = (it["x"] + it["w"]) * DPI - lw_
                    else:
                        x = (it["x"] + ind) * DPI
                    maxsize = max((ro["size"] for _, ro in ln), default=p["size"])
                    base_y = y * DPI + (lh * DPI - maxsize * DPI / 72) / 2
                    if p["bullet"] and first:
                        ro0 = p["runs"][0][1]
                        d.text((it["x"] * DPI, base_y), "•", font=font(ro0["size"], False), fill=hexrgb(ro0["color"]))
                    for tok, ro in ln:
                        f = font(ro["size"], ro["bold"], ro["italic"])
                        d.text((x, base_y + (maxsize - ro["size"]) * DPI / 72 * 0.8), tok, font=f, fill=hexrgb(ro["color"]))
                        x += f.getlength(tok)
                    y += lh
        img.save(path)

    # ---------------- PPTX back-end ----------------
    def save_pptx(self, path):
        prs = Presentation()
        prs.slide_width = Inches(W)
        prs.slide_height = Inches(H)
        blank = prs.slide_layouts[6]
        for s in self.slides:
            sl = prs.slides.add_slide(blank)
            for kind, it in s.items:
                if kind == "rect":
                    if it["w"] <= 0 or it["h"] <= 0:
                        continue
                    st = {"rect": MSO_SHAPE.RECTANGLE, "round": MSO_SHAPE.ROUNDED_RECTANGLE,
                          "ellipse": MSO_SHAPE.OVAL}[it["shape"]]
                    sh = sl.shapes.add_shape(st, Inches(it["x"]), Inches(it["y"]), Inches(it["w"]), Inches(it["h"]))
                    if it["shape"] == "round":
                        sh.adjustments[0] = min(0.5, 0.08 / max(0.01, min(it["w"], it["h"])))
                    sh.shadow.inherit = False
                    if it["fill"]:
                        sh.fill.solid(); sh.fill.fore_color.rgb = RGBColor(*hexrgb(it["fill"]))
                    else:
                        sh.fill.background()
                    if it["line"]:
                        sh.line.color.rgb = RGBColor(*hexrgb(it["line"])); sh.line.width = Pt(it["lw"])
                    else:
                        sh.line.fill.background()
                    sh.text_frame.text = ""
                elif kind == "line":
                    c = sl.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(it["x1"]), Inches(it["y1"]),
                                                Inches(it["x2"]), Inches(it["y2"]))
                    c.line.color.rgb = RGBColor(*hexrgb(it["color"])); c.line.width = Pt(it["lw"])
                elif kind == "text":
                    tb = sl.shapes.add_textbox(Inches(it["x"]), Inches(it["y"]), Inches(it["w"]), Inches(it["h"]))
                    if it.get("name"):
                        tb.name = it["name"]
                    tf = tb.text_frame
                    tf.word_wrap = True
                    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
                    tf.vertical_anchor = {"t": MSO_ANCHOR.TOP, "m": MSO_ANCHOR.MIDDLE, "b": MSO_ANCHOR.BOTTOM}[it["valign"]]
                    bodyPr = tf._txBody.find(qn("a:bodyPr"))
                    for p_i, p in enumerate(it["paras"]):
                        para = tf.paragraphs[0] if p_i == 0 else tf.add_paragraph()
                        para.alignment = {"l": PP_ALIGN.LEFT, "c": PP_ALIGN.CENTER, "r": PP_ALIGN.RIGHT}[p["align"]]
                        maxsize = max(ro["size"] for _, ro in p["runs"])
                        para.line_spacing = Pt(maxsize * LINE)
                        if p_i > 0 and p["space"]:
                            para.space_before = Pt(p["space"])
                        pPr = para._p.get_or_add_pPr()
                        if p["bullet"]:
                            pPr.set("marL", str(int(Inches(p["indent"]))))
                            pPr.set("indent", str(-int(Inches(p["indent"]))))
                            bu = pPr.makeelement(qn("a:buChar"), {"char": "•"})
                            pPr.append(bu)
                        else:
                            pPr.append(pPr.makeelement(qn("a:buNone"), {}))
                        for t, ro in p["runs"]:
                            r = para.add_run()
                            r.text = t
                            f = r.font
                            f.name = "Arial"; f.size = Pt(ro["size"]); f.bold = ro["bold"]; f.italic = ro["italic"]
                            f.color.rgb = RGBColor(*hexrgb(ro["color"]))
            if s.notes:
                sl.notes_slide.notes_text_frame.text = s.notes
        prs.save(path)
