"""Slide-building helpers: layout, text, tables and shape-drawn charts (python-pptx)."""
import math
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR

def rgb(h): return RGBColor.from_string(h)
INK, INK2, MUTED, RULE, PANEL = "1A1A1A", "52514E", "8A8985", "D9D8D4", "F3F2EF"
BLUE, ORANGE, TOTAL, NAVY = "2A78D6", "EB6834", "52514E", "1C3D6B"
BLUE_LT = "CDE2FB"
FONT = "Calibri"
W, H = 13.333, 7.5
LM, RM = 0.5, 0.5
CW = W - LM - RM

WARN = []

def est_lines(text, width_in, pt, char_w=0.50):
    cpl = max(1, int(width_in * 72 / (pt * char_w)))
    n = 0
    for para in text.split("\n"):
        words, line, cnt = para.split(" "), 0, 1
        for wd in words:
            L = len(wd) + (1 if line else 0)
            if line + L > cpl:
                cnt += 1; line = len(wd)
            else:
                line += L
        n += cnt
    return n

def check_fit(name, text, w, h, pt, spacing=1.2, pad=0.1):
    need = est_lines(text, w - 2 * pad, pt) * pt * spacing / 72 + 2 * pad * 0.5
    if need > h + 0.02:
        WARN.append(f"[overflow?] {name}: need {need:.2f}in > box {h:.2f}in :: {text[:60]!r}")

class Deck:
    def __init__(self):
        self.p = Presentation()
        self.p.slide_width, self.p.slide_height = Inches(W), Inches(H)
        self.n = 0

    def slide(self, tracker, title, source=None, number=True):
        s = self.p.slides.add_slide(self.p.slide_layouts[6])
        self.n += 1
        s._num = self.n
        if tracker:
            text(s, LM, 0.28, 8, 0.28, tracker.upper(), 9, color=MUTED, bold=True)
        if title:
            text(s, LM, 0.52, CW, 0.95, title, 21, bold=True, color=INK, anchor="top", name=f"title{self.n}")
            line(s, LM, 1.5, LM + CW, 1.5, RULE, 0.75)
        if source:
            text(s, LM, 6.92, CW - 0.8, 0.45, source, 8, color=MUTED, anchor="top", name=f"src{self.n}")
        if number:
            text(s, W - RM - 0.6, 7.05, 0.6, 0.3, str(self.n), 9, color=MUTED, align="r")
        return s

    def save(self, path):
        self.p.save(path)

def _apply_run(r, size, bold, color, italic=False):
    r.font.name = FONT; r.font.size = Pt(size); r.font.bold = bold
    r.font.italic = italic; r.font.color.rgb = rgb(color)

def text(s, x, y, w, h, content, size=12, bold=False, color=INK, align="l", anchor="top",
         fill=None, name=None, spacing=1.0, bullets=False, pad=0.05, line_color=None, check=True):
    """content: str (\n = paragraphs) or list of paragraphs; a paragraph may be a list of
    (text, {bold,color,size,italic}) runs."""
    if fill and not isinstance(content, str) or (fill and isinstance(content, str) and len(content) > 40):
        _pl = "\n".join("".join(t for t, _ in (para if not isinstance(para, str) else [(para, {})]))
                         for para in (content if not isinstance(content, str) else content.split("\n")))
        _need = est_lines(_pl, w - 0.2, size) * size * 1.2 / 72 + 0.2
        h = min(h, max(_need, 0.4))
    tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    if fill:
        tb.fill.solid(); tb.fill.fore_color.rgb = rgb(fill)
    if line_color:
        tb.line.color.rgb = rgb(line_color); tb.line.width = Pt(0.75)
    tf = tb.text_frame; tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(pad if not fill else max(pad, 0.1))
    tf.margin_top = tf.margin_bottom = Inches(0.04 if not fill else 0.07)
    tf.vertical_anchor = {"top": MSO_ANCHOR.TOP, "mid": MSO_ANCHOR.MIDDLE, "bot": MSO_ANCHOR.BOTTOM}[anchor]
    paras = content.split("\n") if isinstance(content, str) else content
    plain = []
    for i, para in enumerate(paras):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = {"l": PP_ALIGN.LEFT, "c": PP_ALIGN.CENTER, "r": PP_ALIGN.RIGHT}[align]
        p.line_spacing = spacing
        runs = [(para, {})] if isinstance(para, str) else para
        ptxt = ""
        for t, o in runs:
            if bullets and t is runs[0][0]:
                t = "•  " + t
            r = p.add_run(); r.text = t; ptxt += t
            _apply_run(r, o.get("size", size), o.get("bold", bold), o.get("color", color), o.get("italic", False))
        if i > 0 and bullets:
            p.space_before = Pt(4)
        plain.append(ptxt)
    if check and name is not False:
        check_fit(name or f"text@{x:.1f},{y:.1f}", "\n".join(plain), w, h, size, spacing * 1.2 + (0.08 if bullets else 0))
    return tb

def rect(s, x, y, w, h, color, line_color=None, shape=MSO_SHAPE.RECTANGLE):
    r = s.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(max(h, 0.005)))
    r.fill.solid(); r.fill.fore_color.rgb = rgb(color)
    if line_color: r.line.color.rgb = rgb(line_color); r.line.width = Pt(0.75)
    else: r.line.fill.background()
    r.shadow.inherit = False
    return r

def line(s, x1, y1, x2, y2, color=RULE, width=0.75):
    c = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1), Inches(x2), Inches(y2))
    c.line.color.rgb = rgb(color); c.line.width = Pt(width)
    return c

def pill(s, x, y, w, h, label, color, size=10):
    r = rect(s, x, y, w, h, color, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    tf = r.text_frame; tf.margin_left = tf.margin_right = Inches(0.04)
    tf.margin_top = tf.margin_bottom = Inches(0.0)
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    run = p.add_run(); run.text = label; _apply_run(run, size, True, "FFFFFF")
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    return r

def table(s, x, y, w, col_w, rows, size=10, header_fill=NAVY, row_h=None, bold_rows=(), shade_rows=(),
          align=None, name="table", max_h=None, first_col_bold=False):
    """rows[0] is header. col_w: relative widths. Returns estimated height."""
    tot = sum(col_w); cws = [w * c / tot for c in col_w]
    nr, nc = len(rows), len(rows[0])
    # estimate heights
    hs = []
    for i, r in enumerate(rows):
        lines = max(est_lines(str(c), cws[j] - 0.14, size) for j, c in enumerate(r))
        hs.append(max(row_h or 0, lines * size * 1.18 / 72 + 0.1))
    est = sum(hs)
    if max_h and est > max_h + 0.02:
        WARN.append(f"[table overflow?] {name}: est {est:.2f}in > {max_h:.2f}in")
    gt = s.shapes.add_table(nr, nc, Inches(x), Inches(y), Inches(w), Inches(est)).table
    for j, cw in enumerate(cws): gt.columns[j].width = Inches(cw)
    for i in range(nr):
        gt.rows[i].height = Inches(hs[i])
        for j in range(nc):
            c = gt.cell(i, j); c.margin_left = c.margin_right = Inches(0.07)
            c.margin_top = Inches(0.035); c.margin_bottom = Inches(0.035)
            c.vertical_anchor = MSO_ANCHOR.MIDDLE
            val = rows[i][j]
            tf = c.text_frame; tf.word_wrap = True
            paras = str(val).split("\n")
            for k, ptxt in enumerate(paras):
                p = tf.paragraphs[0] if k == 0 else tf.add_paragraph()
                a = (align[j] if align else "l")
                p.alignment = {"l": PP_ALIGN.LEFT, "c": PP_ALIGN.CENTER, "r": PP_ALIGN.RIGHT}[a]
                r = p.add_run(); r.text = ptxt
                hdr = i == 0
                b = hdr or i in bold_rows or (first_col_bold and j == 0)
                _apply_run(r, size, b, "FFFFFF" if hdr else INK)
            c.fill.solid()
            if i == 0: c.fill.fore_color.rgb = rgb(header_fill)
            elif i in shade_rows: c.fill.fore_color.rgb = rgb(PANEL)
            else: c.fill.fore_color.rgb = rgb("FFFFFF")
    tblPr = gt._tbl.tblPr
    # remove default banding style look
    tblPr.set("bandRow", "0"); tblPr.set("firstRow", "1")
    return est

def M(t):
    """typographic minus"""
    return t.replace("-", "\u2212")

def waterfall(s, x, y, w, h, items, vmax, vmin=0.0, fmt="{:+.1f}", tfmt="{:.1f}", label_size=10,
              cat_size=9, cat_h=0.75, refline=None, total_colors=None):
    """items: (label, value, kind) kind: 'total' (absolute), 'delta', 'sub' (absolute subtotal)."""
    ph = h - cat_h
    def Y(v): return y + ph * (vmax - v) / (vmax - vmin)
    n = len(items); slot = w / n; bw = slot * 0.62
    run = 0.0; prev_end = None
    line(s, x, Y(vmin), x + w, Y(vmin), INK2, 0.75)
    for i, (lab, v, kind) in enumerate(items):
        cx = x + i * slot + (slot - bw) / 2
        if kind in ("total", "sub"):
            lo, hi, run = vmin, v, v
            col = (total_colors or {}).get(i, TOTAL)
            lbl = tfmt.format(v)
        else:
            lo, hi = sorted([run, run + v]); run += v
            col = BLUE if v >= 0 else ORANGE
            lbl = M(fmt.format(v)) if abs(v) > 1e-9 else fmt.format(0).lstrip('+')
        rect(s, cx, Y(hi), bw, Y(lo) - Y(hi), col)
        if prev_end is not None:
            line(s, prev_end[0], Y(prev_end[1]), cx, Y(prev_end[1]), MUTED, 0.5)
        prev_end = (cx + bw, run)
        text(s, cx - 0.25, Y(hi) - 0.3, bw + 0.5, 0.28, lbl, label_size, bold=True, color=INK, align="c", name=False)
        text(s, x + i * slot, Y(vmin) + 0.05, slot, cat_h - 0.05, lab, cat_size, color=INK2, align="c", name=f"wf-cat {lab}")
    if refline is not None:
        v, lab, frm = (list(refline) + [0])[:3]
        x0 = x + frm * slot
        line(s, x0, Y(v), x + w, Y(v), INK, 1.25)
        if lab:
            text(s, x0, Y(v) - 0.3, 2.6, 0.28, lab, 9, bold=True, color=INK, align="l", name=False)
    return Y

def hbars(s, x, y, w, h, items, vmin, vmax, fmt="{:+.2f}", label_w=2.6, size=10, zero=True):
    """Horizontal diverging bars. items: (label, value, color)."""
    n = len(items); slot = h / n; bh = slot * 0.55
    neg = any(v < 0 for _, v, _ in items)
    px = x + label_w + (0.85 if neg else 0.1)
    pw = x + w - 0.8 - px
    def X(v): return px + pw * (v - vmin) / (vmax - vmin)
    for i, (lab, v, col) in enumerate(items):
        cy = y + i * slot + (slot - bh) / 2
        a, b = sorted([X(0), X(v)])
        rect(s, a, cy, b - a, bh, col)
        text(s, x, cy - 0.1, label_w - 0.1, bh + 0.2, lab, size, color=INK, align="r", anchor="mid", name=f"hb {lab}")
        if v >= 0: text(s, b + 0.05, cy - 0.05, 0.9, bh + 0.1, M(fmt.format(v)), size, bold=True, anchor="mid", name=False)
        else: text(s, a - 0.95, cy - 0.05, 0.9, bh + 0.1, M(fmt.format(v)), size, bold=True, align="r", anchor="mid", name=False)
    if zero: line(s, X(0), y, X(0), y + h, INK2, 0.75)
    return X

def vbars(s, x, y, w, h, items, vmax, fmt="{:.1f}%", size=10, cat_h=0.5, color=BLUE):
    ph = h - cat_h; n = len(items); slot = w / n; bw = slot * 0.5
    def Y(v): return y + ph * (vmax - v) / vmax
    line(s, x, Y(0), x + w, Y(0), INK2, 0.75)
    for i, (lab, v, *c) in enumerate(items):
        cx = x + i * slot + (slot - bw) / 2
        rect(s, cx, Y(v), bw, Y(0) - Y(v), c[0] if c else color)
        text(s, cx - 0.2, Y(v) - 0.3, bw + 0.4, 0.28, fmt.format(v), size, bold=True, align="c", name=False)
        text(s, x + i * slot, Y(0) + 0.05, slot, cat_h, lab, size - 1, color=INK2, align="c", name=f"vb {lab}")
    return Y

def number_badge(s, x, y, n, color=NAVY, d=0.42):
    r = rect(s, x, y, d, d, color, shape=MSO_SHAPE.OVAL)
    tf = r.text_frame; tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    run = p.add_run(); run.text = str(n); _apply_run(run, 14, True, "FFFFFF")
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
