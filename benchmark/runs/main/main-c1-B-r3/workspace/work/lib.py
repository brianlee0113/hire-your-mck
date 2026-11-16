"""Small slide-building library on top of python-pptx (shape-drawn charts for exact layout)."""
import re
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR, MSO_AUTO_SIZE
from pptx.enum.dml import MSO_LINE_DASH_STYLE

FONT = "Arial"
NAVY = "14213D"
INK = "1F1F1F"
INK2 = "52514E"
MUTED = "8A8984"
GRID = "E4E3DF"
RULE = "C9C8C3"
PANEL = "F4F3F0"
A_COL = "2A78D6"
A_LIGHT = "86B6EF"
B_COL = "EB6834"
J_COL = "1BAF7A"
NEUTRAL = "A3A29C"
GOOD = "0CA30C"
CRIT = "D03B3B"
WARN = "FAB219"
GOOD_T = "E2F3E2"
CRIT_T = "F9E1E1"
WARN_T = "FEF1D2"
WHITE = "FFFFFF"

W, H = 13.333, 7.5
L, R = 0.5, 0.5
CW = W - L - R


def rgb(h):
    return RGBColor.from_string(h)


def new_prs():
    p = Presentation()
    p.slide_width = Inches(W)
    p.slide_height = Inches(H)
    return p


def _runs(par, text, size, bold, color, italic=False):
    parts = re.split(r"(\*\*.+?\*\*)", text)
    for part in parts:
        if not part:
            continue
        b = bold
        if part.startswith("**") and part.endswith("**"):
            part = part[2:-2]
            b = True
        r = par.add_run()
        r.text = part
        f = r.font
        f.name = FONT
        f.size = Pt(size)
        f.bold = b
        f.italic = italic
        f.color.rgb = rgb(color)


from pptx.oxml.ns import qn
from lxml import etree


def _bullet(par, size):
    pPr = par._p.get_or_add_pPr()
    ind = int(Inches(0.17 if size >= 10 else 0.15))
    pPr.set("marL", str(ind)); pPr.set("indent", str(-ind))
    for tag in ("a:buFont", "a:buChar"):
        pass
    bf = etree.SubElement(pPr, qn("a:buFont")); bf.set("typeface", "Arial")
    bc = etree.SubElement(pPr, qn("a:buChar")); bc.set("char", "•")


def fm(v, d=1, plus=False, pre="", suf=""):
    """number with en-dash minus"""
    s = f"{abs(v):,.{d}f}"
    if round(v, d) < 0:
        return "–" + pre + s + suf
    return ("+" if plus and round(v, d) > 0 else "") + pre + s + suf


def text(slide, x, y, w, h, paras, size=12, bold=False, color=INK, align="l", anchor="t",
         bullet=False, space_after=4, line_spacing=1.08, margin=0.04, italic=False, fill=None, border=None):
    """paras: str or list of str / dict(t=, size=, bold=, color=, bullet=, space=, indent=)."""
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    if fill:
        tb.fill.solid(); tb.fill.fore_color.rgb = rgb(fill)
    if border:
        tb.line.color.rgb = rgb(border); tb.line.width = Pt(0.75)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.auto_size = MSO_AUTO_SIZE.NONE
    tf.margin_left = tf.margin_right = Inches(margin)
    tf.margin_top = tf.margin_bottom = Inches(0.03)
    tf.vertical_anchor = {"t": MSO_ANCHOR.TOP, "m": MSO_ANCHOR.MIDDLE, "b": MSO_ANCHOR.BOTTOM}[anchor]
    if isinstance(paras, str):
        paras = [paras]
    for i, p in enumerate(paras):
        if isinstance(p, str):
            p = dict(t=p)
        par = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        par.alignment = {"l": PP_ALIGN.LEFT, "c": PP_ALIGN.CENTER, "r": PP_ALIGN.RIGHT}[p.get("align", align)]
        par.line_spacing = line_spacing
        par.space_after = Pt(p.get("space", space_after))
        b = p.get("bullet", bullet)
        t = p["t"]
        if b:
            _bullet(par, p.get("size", size))
        _runs(par, t, p.get("size", size), p.get("bold", bold), p.get("color", color), p.get("italic", italic))
    tb._qa = dict(bullet=bullet)
    return tb


def rect(slide, x, y, w, h, fill=None, line=None, lw=0.75, shape=MSO_SHAPE.RECTANGLE, dash=False):
    s = slide.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    if fill:
        s.fill.solid(); s.fill.fore_color.rgb = rgb(fill)
    else:
        s.fill.background()
    if line:
        s.line.color.rgb = rgb(line); s.line.width = Pt(lw)
        if dash:
            s.line.dash_style = MSO_LINE_DASH_STYLE.DASH
    else:
        s.line.fill.background()
    s.shadow.inherit = False
    return s


def line(slide, x1, y1, x2, y2, color=RULE, width=0.75, dash=False):
    c = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1), Inches(x2), Inches(y2))
    c.line.color.rgb = rgb(color)
    c.line.width = Pt(width)
    if dash:
        c.line.dash_style = MSO_LINE_DASH_STYLE.DASH
    return c


def polyline(slide, pts, color, width=2.0, dash=False):
    fb = slide.shapes.build_freeform(Inches(pts[0][0]), Inches(pts[0][1]), scale=1.0)
    fb.add_line_segments([(Inches(a), Inches(b)) for a, b in pts[1:]], close=False)
    s = fb.convert_to_shape()
    s.fill.background()
    s.line.color.rgb = rgb(color)
    s.line.width = Pt(width)
    if dash:
        s.line.dash_style = MSO_LINE_DASH_STYLE.DASH
    s.shadow.inherit = False
    return s


def dot(slide, cx, cy, d, color, ring=WHITE):
    s = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(cx - d / 2), Inches(cy - d / 2), Inches(d), Inches(d))
    s.fill.solid(); s.fill.fore_color.rgb = rgb(color)
    s.line.color.rgb = rgb(ring); s.line.width = Pt(1.5)
    s.shadow.inherit = False
    return s


# ---------- slide chrome ----------
def header(slide, section, title, n=None):
    if section:
        text(slide, L, 0.28, CW, 0.28, section.upper(), size=10, bold=True, color=A_COL)
    text(slide, L, 0.52, CW, 0.95, title, size=22, bold=True, color=NAVY, anchor="t", line_spacing=1.0)
    line(slide, L, 1.5, W - R, 1.5, color=RULE, width=0.75)


def footer(slide, source, n):
    if source:
        text(slide, L, 6.98, CW - 0.8, 0.36, "Source: " + source, size=8.5, color=MUTED)
    text(slide, W - R - 0.6, 7.02, 0.6, 0.3, str(n), size=9, color=MUTED, align="r")


def pill(slide, x, y, w, h, kind, label=None, size=10.5):
    fill, border, sym, default = {
        "good": (GOOD_T, GOOD, "✓", "Holds"),
        "bad": (CRIT_T, CRIT, "✗", "Fails"),
        "part": (WARN_T, WARN, "◐", "Partly"),
    }[kind]
    s = rect(slide, x, y, w, h, fill=fill, line=border, lw=1.0, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    s.adjustments[0] = 0.3
    text(slide, x, y, w, h, f"{sym}  {label or default}", size=size, bold=True, color=INK, align="c", anchor="m")
    return s


def number_badge(slide, x, y, d, n, color=NAVY):
    s = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(x), Inches(y), Inches(d), Inches(d))
    s.fill.solid(); s.fill.fore_color.rgb = rgb(color); s.line.fill.background(); s.shadow.inherit = False
    text(slide, x, y, d, d, str(n), size=12, bold=True, color=WHITE, align="c", anchor="m", margin=0)


def table(slide, x, y, colw, rows, rowh=0.36, size=10.5, header_fill=NAVY, header_color=WHITE,
          zebra=False, first_bold=True, aligns=None, row_heights=None, bold_rows=(), highlight_rows=None,
          fills=None):
    """rows[0] is header. Cells are strings (support **bold**). Drawn with rectangles + textboxes."""
    cy = y
    for ri, row in enumerate(rows):
        rh = row_heights[ri] if row_heights else rowh
        cx = x
        for ci, cell in enumerate(row):
            cw = colw[ci]
            if ri == 0:
                rect(slide, cx, cy, cw, rh, fill=header_fill)
                text(slide, cx + 0.04, cy, cw - 0.08, rh, cell, size=size - 0.5, bold=True, color=header_color,
                     align=(aligns[ci] if aligns else "l"), anchor="m")
            else:
                f = None
                if fills and fills.get((ri, ci)):
                    f = fills[(ri, ci)]
                elif highlight_rows and ri in highlight_rows:
                    f = highlight_rows[ri]
                elif zebra and ri % 2 == 0:
                    f = PANEL
                if f:
                    rect(slide, cx, cy, cw, rh, fill=f)
                text(slide, cx + 0.04, cy, cw - 0.08, rh, cell, size=size,
                     bold=(first_bold and ci == 0) or ri in bold_rows, color=INK,
                     align=(aligns[ci] if aligns else "l"), anchor="m")
            cx += cw
        cy += rh
        line(slide, x, cy, x + sum(colw), cy, color=GRID if ri else RULE, width=0.75)
    return cy


# ---------- charts ----------
class Axis:
    def __init__(self, y0, y1, vmin, vmax):
        self.y0, self.y1, self.vmin, self.vmax = y0, y1, vmin, vmax  # y0 top inch, y1 bottom inch

    def __call__(self, v):
        return self.y1 - (v - self.vmin) / (self.vmax - self.vmin) * (self.y1 - self.y0)


def grid_y(slide, x, w, ax, ticks, fmt, size=9, label_w=0.55):
    for t in ticks:
        yy = ax(t)
        line(slide, x + label_w, yy, x + w, yy, color=GRID if t != 0 else MUTED, width=0.75 if t else 1.0)
        text(slide, x, yy - 0.11, label_w - 0.06, 0.22, fmt(t).replace("-", "–"), size=size, color=MUTED, align="r")


def bar_chart(slide, x, y, w, h, cats, series, vmin, vmax, ticks, fmt, label_fmt=None, gap=0.35,
              cat_size=9.5, label_size=9.5, show_axis_labels=True, label_w=0.55, inner_gap=0.03, stacked=False,
              stack_labels=None, cat_h=0.32):
    """Vertical grouped (or stacked) bars. series: list of dict(name, values, color)."""
    plot_x = x + (label_w if show_axis_labels else 0)
    plot_w = w - (label_w if show_axis_labels else 0)
    ax = Axis(y, y + h - cat_h - 0.03, vmin, vmax)
    if show_axis_labels:
        grid_y(slide, x, w, ax, ticks, fmt, label_w=label_w)
    n = len(cats)
    slot = plot_w / n
    groupw = slot * (1 - gap)
    k = 1 if stacked else len(series)
    bw = (groupw - inner_gap * (k - 1)) / k
    for i, c in enumerate(cats):
        gx = plot_x + i * slot + (slot - groupw) / 2
        base_pos = 0
        for si, s in enumerate(series):
            v = s["values"][i]
            if v is None:
                continue
            bx = gx if stacked else gx + si * (bw + inner_gap)
            if stacked:
                top, bot = ax(base_pos + v), ax(base_pos)
                base_pos += v
            else:
                top, bot = (ax(v), ax(0)) if v >= 0 else (ax(0), ax(v))
            col = s["colors"][i] if s.get("colors") else s["color"]
            if bot - top > 0.005:
                rect(slide, bx, top, bw, bot - top - (0.02 if stacked else 0), fill=col)
            if label_fmt and s.get("labels", True):
                lab = label_fmt(v)
                if stacked:
                    if bot - top > 0.22:
                        text(slide, bx, top, bw, bot - top, lab, size=label_size, color=WHITE if s.get("dark", True) else INK, align="c", anchor="m", bold=True)
                elif v >= 0:
                    text(slide, bx - 0.15, top - 0.26, bw + 0.3, 0.24, lab, size=label_size, color=INK, align="c", bold=True)
                else:
                    text(slide, bx - 0.15, bot + 0.02, bw + 0.3, 0.24, lab, size=label_size, color=INK, align="c", bold=True)
        if stacked and stack_labels:
            text(slide, gx - 0.2, ax(base_pos) - 0.26, groupw + 0.4, 0.24, stack_labels[i], size=label_size, color=INK, align="c", bold=True)
        text(slide, plot_x + i * slot, y + h - cat_h, slot, cat_h, c, size=cat_size, color=INK2, align="c")
    return ax, plot_x, plot_w, slot


def line_chart(slide, x, y, w, h, cats, series, vmin, vmax, ticks, fmt, label_w=0.55, cat_size=9.5,
               end_labels=True, end_label_w=1.6, marker=0.09):
    plot_x = x + label_w
    plot_w = w - label_w - (end_label_w if end_labels else 0)
    ax = Axis(y, y + h - 0.35, vmin, vmax)
    grid_y(slide, x, w - (end_label_w if end_labels else 0), ax, ticks, fmt, label_w=label_w)
    n = len(cats)
    step = plot_w / n
    xs = [plot_x + step * (i + 0.5) for i in range(n)]
    for i, c in enumerate(cats):
        text(slide, xs[i] - step / 2, y + h - 0.32, step, 0.32, c, size=cat_size, color=INK2, align="c")
    for s in series:
        pts = [(xs[i], ax(v)) for i, v in enumerate(s["values"]) if v is not None]
        if len(pts) > 1:
            polyline(slide, pts, s["color"], width=s.get("width", 2.25), dash=s.get("dash", False))
        if s.get("markers", True):
            for (px, py) in pts:
                dot(slide, px, py, marker, s["color"])
        if s.get("point_labels"):
            for i, v in enumerate(s["values"]):
                if v is None or s["point_labels"][i] is None:
                    continue
                off = s["label_offsets"][i] if s.get("label_offsets") else s.get("label_offset", -0.3)
                dx = s["label_dx"][i] if s.get("label_dx") else 0
                text(slide, xs[i] - 0.45 + dx, ax(v) + off, 0.9, 0.24, s["point_labels"][i], size=9, color=INK, align="c", bold=True)
        if end_labels and s.get("end_label"):
            lx, ly = pts[-1]
            dy = s.get("end_dy", 0)
            text(slide, lx + 0.12, ly - 0.2 + dy, end_label_w - 0.1, 0.42, s["end_label"], size=9.5, color=INK, bold=True, line_spacing=0.95)
    return ax, xs


def waterfall(slide, x, y, w, h, steps, vmax, color_total, color_neg="B9B8B2", label_w=0.0, cat_size=8.5):
    """steps: list of (label, value, kind) kind in {'start','neg','total'}"""
    ax = Axis(y, y + h - 0.55, 0, vmax)
    line(slide, x, ax(0), x + w, ax(0), color=MUTED, width=1.0)
    n = len(steps)
    slot = w / n
    bw = slot * 0.62
    run = 0
    prev_top = None
    for i, (lab, v, kind) in enumerate(steps):
        bx = x + i * slot + (slot - bw) / 2
        if kind == "start":
            top, bot = ax(v), ax(0); run = v; col = NEUTRAL; vl = f"${v+1e-9:.2f}"
        elif kind == "neg":
            top, bot = ax(run), ax(run - v); run -= v; col = color_neg; vl = f"–{v+1e-9:.2f}"
        else:
            top, bot = ax(v), ax(0); col = color_total; vl = f"${v+1e-9:.2f}"
        rect(slide, bx, top, bw, max(bot - top, 0.01), fill=col)
        if i > 0:
            line(slide, bx - (slot - bw), top if kind == "neg" else top, bx, top if kind == "neg" else top, color=MUTED, width=0.5, dash=True)
        text(slide, x + i * slot, top - 0.24, slot, 0.22, vl, size=9, color=INK, align="c", bold=(kind != "neg"))
        text(slide, x + i * slot, y + h - 0.52, slot, 0.52, lab, size=cat_size, color=INK2, align="c", line_spacing=0.95)
    return ax


def legend(slide, x, y, items, size=9.5, gap=0.25, sw=0.22, line_items=()):
    cx = x
    for name, col in items:
        if name in line_items:
            line(slide, cx, y + 0.11, cx + sw, y + 0.11, color=col, width=2.25, dash=(line_items[name] == "dash"))
        else:
            rect(slide, cx, y + 0.04, sw * 0.7, 0.14, fill=col)
        tw = 0.075 * len(name) * size / 10 + 0.15
        text(slide, cx + sw + 0.04, y, tw, 0.24, name, size=size, color=INK2)
        cx += sw + 0.04 + tw + gap
