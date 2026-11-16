"""Tiny slide engine: slides are lists of primitives rendered to PPTX (python-pptx)
and to PNG (PIL) with the same text-wrapping rules, so layout can be checked visually
and overflow is flagged automatically."""
from PIL import Image, ImageDraw, ImageFont
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR, MSO_AUTO_SIZE
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.oxml.ns import qn
from lxml import etree

W, H = 13.333, 7.5
DPI = 120
FONT_DIR = "/System/Library/Fonts/Supplemental/"
FONT = {False: FONT_DIR + "Arial.ttf", True: FONT_DIR + "Arial Bold.ttf"}
LS = 1.18          # line height multiple (set explicitly in pptx too)
INS_X, INS_Y = 0.04, 0.02
_fcache = {}


def font(size, bold):
    key = (round(size * DPI / 72 * 4), bold)
    if key not in _fcache:
        _fcache[key] = ImageFont.truetype(FONT[bold], key[0] / 4)
    return _fcache[key]


def hexrgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


class Slide:
    def __init__(self, notes=""):
        self.items = []
        self.notes = notes

    def rect(self, x, y, w, h, fill, line=None, lw=0.75, shape="rect"):
        self.items.append(("rect", dict(x=x, y=y, w=w, h=h, fill=fill, line=line, lw=lw, shape=shape)))

    def oval(self, x, y, d, fill):
        self.items.append(("rect", dict(x=x, y=y, w=d, h=d, fill=fill, line=None, lw=0, shape="oval")))

    def line(self, x1, y1, x2, y2, color, lw=1.0, dash=False):
        self.items.append(("line", dict(x1=x1, y1=y1, x2=x2, y2=y2, color=color, lw=lw, dash=dash)))

    def text(self, x, y, w, h, paras, size=12, color="#1a1a1a", bold=False, align="l",
             valign="t", space_after=0, name=None):
        """paras: str | list of para; para: str | dict(runs=[(text, {style})], bullet, size, ...)"""
        if isinstance(paras, (str, dict)):
            paras = [paras]
        norm = []
        for p in paras:
            if isinstance(p, str):
                p = dict(runs=[(p, {})])
            elif "runs" not in p:
                p = dict(p, runs=[(p.pop("t"), {})]) if "t" in p else p
            q = dict(size=size, color=color, bold=bold, align=align, bullet=False,
                     space_after=space_after, indent=0.0)
            q.update({k: v for k, v in p.items() if k != "runs"})
            runs = []
            for r in p["runs"]:
                if isinstance(r, str):
                    r = (r, {})
                st = dict(size=q["size"], color=q["color"], bold=q["bold"])
                st.update(r[1])
                runs.append((r[0], st))
            q["runs"] = runs
            norm.append(q)
        self.items.append(("text", dict(x=x, y=y, w=w, h=h, paras=norm, valign=valign, name=name)))


# ---------------- layout (shared) ----------------
def layout_text(t):
    """Return list of lines: (para, indent_in, [(text, style, x_in)], height_in, baseline...)"""
    lines_out = []
    avail = t["w"] - 2 * INS_X
    total_h = 0
    overflow_w = False
    for pi, p in enumerate(t["paras"]):
        hang = 0.0
        if p["bullet"]:
            hang = p["size"] / 72 * 0.9
        left = p["indent"] + hang
        width = avail - left
        # tokenise into words with styles
        toks = []
        for txt, st in p["runs"]:
            parts = txt.split(" ")
            for i, part in enumerate(parts):
                sp = " " if i < len(parts) - 1 else ""
                toks.append((part, sp, st))
        lines = [[]]
        cur = 0.0
        for word, sp, st in toks:
            f = font(st["size"], st["bold"])
            wl = f.getlength(word) / DPI
            sl = f.getlength(sp) / DPI
            if lines[-1] and cur + wl > width + 1e-6 and word != "":
                lines.append([])
                cur = 0.0
            if wl > width:
                overflow_w = True
            lines[-1].append((word + sp, st, cur))
            cur += wl + sl
        if not lines[-1]:
            lines[-1] = [("", p["runs"][0][1] if p["runs"] else dict(size=p["size"], color=p["color"], bold=False), 0)]
        for li, ln in enumerate(lines):
            sz = max(st["size"] for _, st, _ in ln) if ln else p["size"]
            lh = sz * LS / 72
            # merge consecutive same-style tokens
            lines_out.append(dict(p=p, first=(li == 0), left=left, hang=hang, width=width,
                                  toks=ln, lh=lh, size=sz))
            total_h += lh
        if pi < len(t["paras"]) - 1:
            total_h += p["space_after"] / 72
            lines_out[-1]["after"] = p["space_after"] / 72
    return lines_out, total_h, overflow_w


# ---------------- PNG backend ----------------
def render_png(slide, path, warn, idx):
    im = Image.new("RGB", (int(W * DPI), int(H * DPI)), "white")
    d = ImageDraw.Draw(im)
    P = lambda v: int(round(v * DPI))
    for kind, a in slide.items:
        if kind == "rect":
            box = [P(a["x"]), P(a["y"]), P(a["x"] + a["w"]) - 1, P(a["y"] + a["h"]) - 1]
            if box[2] < box[0] or box[3] < box[1]:
                continue
            fill = hexrgb(a["fill"]) if a["fill"] else None
            outline = hexrgb(a["line"]) if a["line"] else None
            width = max(1, int(a["lw"] / 72 * DPI)) if a["line"] else 0
            if a["shape"] == "oval":
                d.ellipse(box, fill=fill, outline=outline, width=width)
            elif a["shape"] == "round":
                d.rounded_rectangle(box, radius=P(0.08), fill=fill, outline=outline, width=width)
            else:
                d.rectangle(box, fill=fill, outline=outline, width=width)
        elif kind == "line":
            wpx = max(1, int(round(a["lw"] / 72 * DPI)))
            if a["dash"]:
                import math
                x1, y1, x2, y2 = a["x1"], a["y1"], a["x2"], a["y2"]
                L = math.hypot(x2 - x1, y2 - y1)
                n = max(1, int(L / 0.08))
                for i in range(0, n, 2):
                    t0, t1 = i / n, min(1, (i + 1) / n)
                    d.line([P(x1 + (x2 - x1) * t0), P(y1 + (y2 - y1) * t0), P(x1 + (x2 - x1) * t1), P(y1 + (y2 - y1) * t1)],
                           fill=hexrgb(a["color"]), width=wpx)
            else:
                d.line([P(a["x1"]), P(a["y1"]), P(a["x2"]), P(a["y2"])], fill=hexrgb(a["color"]), width=wpx)
        elif kind == "text":
            lines, th, ow = layout_text(a)
            avail_h = a["h"] - 2 * INS_Y
            if th > avail_h + 0.01:
                warn.append(f"slide {idx}: text overflow {th:.2f}>{avail_h:.2f}in: '{a['paras'][0]['runs'][0][0][:50]}'")
            if ow:
                warn.append(f"slide {idx}: word wider than box: '{a['paras'][0]['runs'][0][0][:50]}'")
            if a["x"] < 0 or a["x"] + a["w"] > W + 0.01 or a["y"] + a["h"] > H + 0.01:
                warn.append(f"slide {idx}: box off-slide '{a['paras'][0]['runs'][0][0][:40]}'")
            y = a["y"] + INS_Y
            if a["valign"] == "m":
                y += max(0, (avail_h - th) / 2)
            elif a["valign"] == "b":
                y += max(0, avail_h - th)
            for ln in lines:
                p = ln["p"]
                linew = 0
                if ln["toks"]:
                    lw_last = ln["toks"][-1]
                    f = font(lw_last[1]["size"], lw_last[1]["bold"])
                    linew = lw_last[2] + f.getlength(lw_last[0].rstrip(" ")) / DPI
                x0 = a["x"] + INS_X + ln["left"]
                if p["align"] == "c":
                    x0 += (ln["width"] - linew) / 2
                elif p["align"] == "r":
                    x0 += ln["width"] - linew
                base = y + ln["lh"] * 0.80
                if ln["first"] and p["bullet"]:
                    f = font(p["size"], False)
                    d.text((P(a["x"] + INS_X + p["indent"]), P(base)), "•", font=f, fill=hexrgb(p["color"]), anchor="ls")
                for txt, st, xo in ln["toks"]:
                    f = font(st["size"], st["bold"])
                    d.text((P(x0 + xo), P(base)), txt, font=f, fill=hexrgb(st["color"]), anchor="ls")
                y += ln["lh"] + ln.get("after", 0)
    im.save(path)
    return im


# ---------------- PPTX backend ----------------
ALIGN = {"l": PP_ALIGN.LEFT, "c": PP_ALIGN.CENTER, "r": PP_ALIGN.RIGHT}
VALIGN = {"t": MSO_ANCHOR.TOP, "m": MSO_ANCHOR.MIDDLE, "b": MSO_ANCHOR.BOTTOM}


def _no_shadow(shape):
    sp = shape._element.spPr
    ef = etree.SubElement(sp, qn("a:effectLst"))


def render_pptx(slides, path):
    prs = Presentation()
    prs.slide_width = Inches(W)
    prs.slide_height = Inches(H)
    blank = prs.slide_layouts[6]
    for s in slides:
        sl = prs.slides.add_slide(blank)
        for kind, a in s.items:
            if kind == "rect":
                if a["w"] <= 0 or a["h"] <= 0:
                    continue
                st = {"rect": MSO_SHAPE.RECTANGLE, "oval": MSO_SHAPE.OVAL, "round": MSO_SHAPE.ROUNDED_RECTANGLE}[a["shape"]]
                sh = sl.shapes.add_shape(st, Inches(a["x"]), Inches(a["y"]), Inches(a["w"]), Inches(a["h"]))
                if a["shape"] == "round":
                    sh.adjustments[0] = min(0.5, 0.08 / min(a["w"], a["h"]))
                if a["fill"]:
                    sh.fill.solid()
                    sh.fill.fore_color.rgb = RGBColor(*hexrgb(a["fill"]))
                else:
                    sh.fill.background()
                if a["line"]:
                    sh.line.color.rgb = RGBColor(*hexrgb(a["line"]))
                    sh.line.width = Pt(a["lw"])
                else:
                    sh.line.fill.background()
                _no_shadow(sh)
                sh.text_frame.text = ""
            elif kind == "line":
                c = sl.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(a["x1"]), Inches(a["y1"]),
                                            Inches(a["x2"]), Inches(a["y2"]))
                c.line.color.rgb = RGBColor(*hexrgb(a["color"]))
                c.line.width = Pt(a["lw"])
                if a["dash"]:
                    from pptx.enum.dml import MSO_LINE_DASH_STYLE
                    c.line.dash_style = MSO_LINE_DASH_STYLE.DASH
            elif kind == "text":
                tb = sl.shapes.add_textbox(Inches(a["x"]), Inches(a["y"]), Inches(a["w"]), Inches(a["h"]))
                if a.get("name"):
                    tb.name = a["name"]
                tf = tb.text_frame
                tf.word_wrap = True
                tf.auto_size = MSO_AUTO_SIZE.NONE
                tf.margin_left = tf.margin_right = Inches(INS_X)
                tf.margin_top = tf.margin_bottom = Inches(INS_Y)
                tf.vertical_anchor = VALIGN[a["valign"]]
                for i, p in enumerate(a["paras"]):
                    para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
                    para.alignment = ALIGN[p["align"]]
                    para.line_spacing = Pt(p["size"] * LS)
                    para.space_after = Pt(p["space_after"])
                    pPr = para._p.get_or_add_pPr()
                    if p["bullet"]:
                        hang = p["size"] / 72 * 0.9
                        pPr.set("marL", str(int(Inches(p["indent"] + hang))))
                        pPr.set("indent", str(int(-Inches(hang))))
                        bf = etree.SubElement(pPr, qn("a:buFont"))
                        bf.set("typeface", "Arial")
                        bc = etree.SubElement(pPr, qn("a:buChar"))
                        bc.set("char", "•")
                    else:
                        if p["indent"]:
                            pPr.set("marL", str(int(Inches(p["indent"]))))
                        etree.SubElement(pPr, qn("a:buNone"))
                    for txt, st in p["runs"]:
                        r = para.add_run()
                        r.text = txt
                        r.font.name = "Arial"
                        r.font.size = Pt(st["size"])
                        r.font.bold = st["bold"]
                        r.font.color.rgb = RGBColor(*hexrgb(st["color"]))
        if s.notes:
            sl.notes_slide.notes_text_frame.text = s.notes
    prs.save(path)
