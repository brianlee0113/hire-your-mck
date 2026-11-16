"""Slide-building helpers (python-pptx) with a text-fit checker."""
import re
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LABEL_POSITION, XL_LEGEND_POSITION
from pptx.oxml.ns import qn
from PIL import ImageFont

FONT = "Arial"
INK = RGBColor(0x1A, 0x1A, 0x1A)
INK2 = RGBColor(0x52, 0x51, 0x4E)
MUTED = RGBColor(0x8A, 0x89, 0x84)
RULE = RGBColor(0xD9, 0xD8, 0xD3)
BLUE = RGBColor(0x2A, 0x78, 0xD6)
BLUE_D = RGBColor(0x18, 0x4F, 0x95)
BLUE_L = RGBColor(0xCD, 0xE2, 0xFB)
BLUE_XL = RGBColor(0xEE, 0xF4, 0xFC)
ORANGE = RGBColor(0xEB, 0x68, 0x34)
ORANGE_L = RGBColor(0xFB, 0xE3, 0xD8)
GRAY = RGBColor(0xA8, 0xA7, 0xA1)
GRAY_L = RGBColor(0xF2, 0xF1, 0xEE)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
GOOD = RGBColor(0x00, 0x83, 0x00)
WARN = RGBColor(0xC9, 0x85, 0x00)
BAD = RGBColor(0xC6, 0x2F, 0x2E)

SECTIONS = ["Why churn rose", "Where pricing power is", "What it is worth", "How to execute"]

_fonts = {}


def _font(size, bold=False):
    key = (round(size * 4), bold)
    if key not in _fonts:
        path = "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf"
        _fonts[key] = ImageFont.truetype(path, int(size * 4))  # 4x scale for precision
    return _fonts[key]


def text_width_in(text, size, bold=False):
    """Width in inches of text at size pt (Arial)."""
    return _font(size, bold).getlength(text) / 4 / 72


def wrap_lines(text, size, width_in, bold=False):
    words = text.split(" ")
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if text_width_in(t, size, bold) <= width_in or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    lines.append(cur)
    return len(lines)


WARNINGS = []


def strip_md(s):
    return s.replace("**", "")


class Deck:
    def __init__(self):
        self.prs = Presentation()
        self.prs.slide_width = Inches(13.333)
        self.prs.slide_height = Inches(7.5)
        self.n = 0

    def slide(self, title, section=None, source=None, subtitle=None):
        s = self.prs.slides.add_slide(self.prs.slide_layouts[6])
        self.n += 1
        s._num = self.n
        if section is not None:
            tracker(s, section)
        if title:
            text(s, 0.5, 0.42, 12.33, 0.95, [title], size=21, bold=True, color=INK, anchor="top", name="title", line=1.08)
            ln = s.shapes.add_connector(1, Inches(0.5), Inches(1.42), Inches(12.83), Inches(1.42))
            ln.line.color.rgb = RULE
            ln.line.width = Pt(0.75)
        if subtitle:
            text(s, 0.5, 1.5, 12.33, 0.4, [subtitle], size=12, color=INK2)
        if title is None:
            return s
        # footer
        src = source or "Source: Palisade Docs 2027 pricing briefing pack (synthetic data); team analysis"
        text(s, 0.5, 7.02, 11.3, 0.3, [src], size=8, color=MUTED, name="footer")
        text(s, 12.23, 7.02, 0.6, 0.3, [str(self.n)], size=8, color=MUTED, align="right", name="pageno")
        return s

    def save(self, path):
        self.prs.save(path)


def tracker(s, active):
    x = 0.5
    tb = s.shapes.add_textbox(Inches(x), Inches(0.14), Inches(12.33), Inches(0.26))
    tf = tb.text_frame
    _nomargin(tf)
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.RIGHT
    for i, name in enumerate(SECTIONS):
        r = p.add_run()
        r.text = f"{i+1}  {name}"
        r.font.size = Pt(8.5)
        r.font.name = FONT
        r.font.bold = (i == active)
        r.font.color.rgb = BLUE if i == active else MUTED
        if i < len(SECTIONS) - 1:
            r2 = p.add_run()
            r2.text = "     "
            r2.font.size = Pt(8.5)


def _nomargin(tf, l=0, t=0, r=0, b=0):
    tf.margin_left = Inches(l)
    tf.margin_right = Inches(r)
    tf.margin_top = Inches(t)
    tf.margin_bottom = Inches(b)


def _add_runs(p, s, size, bold, color, italic=False):
    parts = re.split(r"(\*\*.+?\*\*)", s)
    for part in parts:
        if not part:
            continue
        r = p.add_run()
        b = bold
        if part.startswith("**") and part.endswith("**"):
            part = part[2:-2]
            b = True
        r.text = part
        r.font.size = Pt(size)
        r.font.bold = b
        r.font.italic = italic
        r.font.name = FONT
        r.font.color.rgb = color


def _bullet(p, level=0, char="•"):
    pPr = p._p.get_or_add_pPr()
    indent = 0.17 + 0.2 * level
    pPr.set("marL", str(int(Inches(indent))))
    pPr.set("indent", str(int(-Inches(0.17))))
    for tag in ("a:buNone", "a:buChar", "a:buAutoNum"):
        for e in pPr.findall(qn(tag)):
            pPr.remove(e)
    bu = pPr.makeelement(qn("a:buChar"), {"char": char})
    pPr.append(bu)


def _spacing(p, before=0, line=1.0):
    pPr = p._p.get_or_add_pPr()
    if before:
        sb = pPr.makeelement(qn("a:spcBef"), {})
        pts = sb.makeelement(qn("a:spcPts"), {"val": str(int(before * 100))})
        sb.append(pts)
        pPr.insert(0, sb)
    if line != 1.0:
        ls = pPr.makeelement(qn("a:lnSpc"), {})
        pc = ls.makeelement(qn("a:spcPct"), {"val": str(int(line * 100000))})
        ls.append(pc)
        pPr.insert(0, ls)


def text(s, x, y, w, h, paras, size=12, bold=False, color=INK, align="left", anchor="top",
         name=None, fill=None, line_color=None, pad=0.0, line=1.0, check=True):
    """paras: list of str or dict(t=..., b=bool, c=color, s=size, bullet=level, before=pts, i=italic)."""
    if fill is not None or line_color is not None:
        shp = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
        shp.shadow.inherit = False
        if fill is not None:
            shp.fill.solid()
            shp.fill.fore_color.rgb = fill
        else:
            shp.fill.background()
        if line_color is not None:
            shp.line.color.rgb = line_color
            shp.line.width = Pt(0.75)
        else:
            shp.line.fill.background()
        tf = shp.text_frame
    else:
        shp = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
        tf = shp.text_frame
    tf.word_wrap = True
    _nomargin(tf, pad, pad, pad, pad)
    tf.vertical_anchor = {"top": MSO_ANCHOR.TOP, "middle": MSO_ANCHOR.MIDDLE, "bottom": MSO_ANCHOR.BOTTOM}[anchor]
    total_h = 0.0
    for i, para in enumerate(paras):
        if isinstance(para, str):
            para = {"t": para}
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = {"left": PP_ALIGN.LEFT, "center": PP_ALIGN.CENTER, "right": PP_ALIGN.RIGHT}[align]
        sz = para.get("s", size)
        before = para.get("before", 0 if i == 0 else 0)
        _spacing(p, before, para.get("line", line))
        lvl = para.get("bullet")
        if lvl is not None:
            _bullet(p, lvl, para.get("char", "•"))
        _add_runs(p, para["t"], sz, para.get("b", bold), para.get("c", color), para.get("i", False))
        avail = w - 2 * pad - (0.17 + 0.2 * lvl if lvl is not None else 0)
        nl = wrap_lines(strip_md(para["t"]), sz, avail * 0.985, para.get("b", bold))
        total_h += nl * sz * 1.2 * para.get("line", line) / 72 + before / 72
    if check and total_h > h - 2 * pad + 0.02:
        WARNINGS.append(f"slide {getattr(s,'_num','?')}: text overflow ({total_h:.2f}in > {h - 2*pad:.2f}in) in '{strip_md(paras[0] if isinstance(paras[0], str) else paras[0]['t'])[:50]}'")
    if name:
        shp.name = name
    return shp


def rect(s, x, y, w, h, fill, line_color=None, shape=MSO_SHAPE.RECTANGLE):
    shp = s.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    shp.shadow.inherit = False
    if fill is None:
        shp.fill.background()
    else:
        shp.fill.solid()
        shp.fill.fore_color.rgb = fill
    if line_color is None:
        shp.line.fill.background()
    else:
        shp.line.color.rgb = line_color
        shp.line.width = Pt(0.75)
    return shp


def hline(s, x1, y, x2, color=RULE, width=0.75):
    ln = s.shapes.add_connector(1, Inches(x1), Inches(y), Inches(x2), Inches(y))
    ln.line.color.rgb = color
    ln.line.width = Pt(width)
    return ln


def table(s, x, y, col_w, rows, size=10, header_fill=INK, header_color=WHITE, row_h=0.3,
          fills=None, bold_first_col=True, max_bottom=6.95, aligns=None, pad=0.06, header_size=None):
    """rows: list of lists of str (first row = header). fills: dict (r,c)->RGB or r->RGB."""
    nr, nc = len(rows), len(rows[0])
    gf = s.shapes.add_table(nr, nc, Inches(x), Inches(y), Inches(sum(col_w)), Inches(row_h * nr))
    tbl = gf.table
    # strip default style banding
    tblPr = gf._element.graphic.graphicData.tbl.tblPr
    tblPr.set("firstRow", "0")
    tblPr.set("bandRow", "0")
    for j, cw in enumerate(col_w):
        tbl.columns[j].width = Inches(cw)
    est_total = 0
    for i, row in enumerate(rows):
        row_need = row_h
        for j, val in enumerate(row):
            cell = tbl.cell(i, j)
            cell.margin_left = cell.margin_right = Inches(pad)
            cell.margin_top = Inches(0.04)
            cell.margin_bottom = Inches(0.04)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            tf = cell.text_frame
            tf.word_wrap = True
            lines = val.split("\n")
            need = 0.08
            for k, ln in enumerate(lines):
                p = tf.paragraphs[0] if k == 0 else tf.add_paragraph()
                a = (aligns[j] if aligns else "left")
                p.alignment = {"left": PP_ALIGN.LEFT, "center": PP_ALIGN.CENTER, "right": PP_ALIGN.RIGHT}[a]
                sz = (header_size or size) if i == 0 else size
                if i == 0:
                    _add_runs(p, ln, sz, True, header_color)
                else:
                    _add_runs(p, ln, sz, bold_first_col and j == 0, INK)
                bb = (i == 0) or (bold_first_col and j == 0) or ln.startswith("**")
                need += wrap_lines(strip_md(ln), sz, (col_w[j] - 2 * pad) * 0.97, bb) * sz * 1.2 / 72
            row_need = max(row_need, need)
            f = None
            if i == 0:
                f = header_fill
            elif fills:
                f = fills.get((i, j), fills.get(i))
            cell.fill.solid()
            cell.fill.fore_color.rgb = f if f is not None else WHITE
        tbl.rows[i].height = Inches(row_need)
        est_total += row_need
    if y + est_total > max_bottom:
        WARNINGS.append(f"slide {getattr(s,'_num','?')}: table bottom {y+est_total:.2f}in > {max_bottom}")
    # thin borders
    for i in range(nr):
        for j in range(nc):
            _cell_border(tbl.cell(i, j))
    gf._est_h = est_total
    return gf


def _cell_border(cell, color="D9D8D3", width=6350):
    tcPr = cell._tc.get_or_add_tcPr()
    for idx, edge in enumerate(("a:lnL", "a:lnR", "a:lnT", "a:lnB")):
        for e in tcPr.findall(qn(edge)):
            tcPr.remove(e)
        ln = tcPr.makeelement(qn(edge), {"w": str(width) if edge in ("a:lnB", "a:lnT") else "0"})
        if edge in ("a:lnB", "a:lnT"):
            sf = ln.makeelement(qn("a:solidFill"), {})
            c = sf.makeelement(qn("a:srgbClr"), {"val": color})
            sf.append(c)
            ln.append(sf)
        else:
            ln.append(ln.makeelement(qn("a:noFill"), {}))
        tcPr.insert(idx, ln)  # schema order: lnL, lnR, lnT, lnB before fill


def _style_axis_text(axis, size=10, color=INK2):
    axis.tick_labels.font.size = Pt(size)
    axis.tick_labels.font.name = FONT
    axis.tick_labels.font.color.rgb = color


def set_plot_layout(chart, fx, fy, fw, fh):
    """Pin the inner plot area to fractions of the chart frame so overlays can be placed exactly."""
    pa = chart._chartSpace.chart.plotArea
    for e in pa.findall(qn("c:layout")):
        pa.remove(e)
    layout = pa.makeelement(qn("c:layout"), {})
    ml = layout.makeelement(qn("c:manualLayout"), {})
    for tag, val in (("c:layoutTarget", "inner"), ("c:xMode", "edge"), ("c:yMode", "edge"),
                     ("c:x", fx), ("c:y", fy), ("c:w", fw), ("c:h", fh)):
        el = ml.makeelement(qn(tag), {"val": str(val)})
        ml.append(el)
    layout.append(ml)
    pa.insert(0, layout)


def waterfall(s, x, y, w, h, cats, steps, kinds, labels=None, colors=None, size=10, vmax=None,
              label_size=None, gap=55, top_pad=0.35, axis_h=0.5):
    """Waterfall from stacked columns with an invisible base; value labels overlaid above bars."""
    base, up, down, tot = [], [], [], []
    run = 0.0
    tops = []
    for v, k in zip(steps, kinds):
        if k == "total":
            run = v
            base.append(0); tot.append(v); up.append(0); down.append(0); tops.append(v)
        elif v >= 0:
            base.append(run); up.append(v); down.append(0); tot.append(0)
            run += v; tops.append(run)
        else:
            tops.append(run)
            run += v
            base.append(run); down.append(-v); up.append(0); tot.append(0)
    vmax = vmax or max(tops) * 1.05
    cd = CategoryChartData()
    cd.categories = cats
    cd.add_series("base", base)
    cd.add_series("total", tot)
    cd.add_series("increase", up)
    cd.add_series("decrease", down)
    gfr = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_STACKED, Inches(x), Inches(y), Inches(w), Inches(h), cd)
    ch = gfr.chart
    ch.has_legend = False
    ch.font.name = FONT
    ch.font.size = Pt(size)
    plot = ch.plots[0]
    plot.gap_width = gap
    plot.overlap = 100
    sers = list(plot.series)
    sers[0].format.fill.background()
    sers[0].format.line.fill.background()
    default = {1: BLUE_D, 2: BLUE, 3: ORANGE}
    for si in (1, 2, 3):
        sers[si].format.fill.solid()
        sers[si].format.fill.fore_color.rgb = default[si]
        sers[si].format.line.fill.background()
    if colors:
        for i, c in enumerate(colors):
            if c is None:
                continue
            si = 1 if kinds[i] == "total" else (2 if steps[i] >= 0 else 3)
            p = sers[si].points[i]
            p.format.fill.solid()
            p.format.fill.fore_color.rgb = c
    va = ch.value_axis
    va.visible = False
    va.has_major_gridlines = False
    va.minimum_scale = 0
    va.maximum_scale = vmax
    ca = ch.category_axis
    _style_axis_text(ca, size)
    ca.format.line.color.rgb = RULE
    ph = h - top_pad - axis_h
    set_plot_layout(ch, 0.0, top_pad / h, 1.0, ph / h)
    slot = w / len(steps)
    for i, (v, k) in enumerate(zip(steps, kinds)):
        lab = labels[i] if labels else (f"{v:.1f}" if k == "total" else f"{v:+.1f}")
        ytop = y + top_pad + ph * (1 - tops[i] / vmax)
        text(s, x + slot * i, ytop - 0.27, slot, 0.25, [lab], size=label_size or size,
             bold=(k == "total"), align="center", color=INK, anchor="bottom")
    return gfr


def bar_chart(s, x, y, w, h, cats, series, colors, horizontal=False, size=10, number_format='0.0',
              legend=True, gap=60, overlap=0, vmax=None, label_fmt=None, point_colors=None, stacked=False,
              labels=True, legend_pos="top"):
    cd = CategoryChartData()
    cd.categories = cats
    for name, vals in series:
        cd.add_series(name, vals)
    if horizontal:
        t = XL_CHART_TYPE.BAR_STACKED if stacked else XL_CHART_TYPE.BAR_CLUSTERED
    else:
        t = XL_CHART_TYPE.COLUMN_STACKED if stacked else XL_CHART_TYPE.COLUMN_CLUSTERED
    gfr = s.shapes.add_chart(t, Inches(x), Inches(y), Inches(w), Inches(h), cd)
    ch = gfr.chart
    ch.font.name = FONT
    ch.font.size = Pt(size)
    ch.has_legend = legend and len(series) > 1
    if ch.has_legend:
        ch.legend.position = XL_LEGEND_POSITION.TOP if legend_pos == "top" else XL_LEGEND_POSITION.BOTTOM
        ch.legend.include_in_layout = False
        ch.legend.font.size = Pt(size)
        ch.legend.font.color.rgb = INK2
    plot = ch.plots[0]
    plot.gap_width = gap
    plot.overlap = 100 if stacked else overlap
    for i, ser in enumerate(plot.series):
        ser.format.fill.solid()
        ser.format.fill.fore_color.rgb = colors[i]
        ser.format.line.color.rgb = WHITE
        ser.format.line.width = Pt(1.5)
        ser.invert_if_negative = False
        if labels:
            dls = ser.data_labels
            dls.show_value = True
            dls.number_format = number_format
            dls.number_format_is_linked = False
            dls.font.size = Pt(size)
            dls.font.color.rgb = INK
            dls.font.name = FONT
            if not stacked:
                dls.position = XL_LABEL_POSITION.OUTSIDE_END
            else:
                dls.position = XL_LABEL_POSITION.CENTER
    if point_colors:
        for (si, pi), c in point_colors.items():
            p = plot.series[si].points[pi]
            p.format.fill.solid()
            p.format.fill.fore_color.rgb = c
    va = ch.value_axis
    va.visible = False
    va.has_major_gridlines = False
    va.minimum_scale = 0
    if vmax:
        va.maximum_scale = vmax
    ca = ch.category_axis
    _style_axis_text(ca, size)
    ca.format.line.color.rgb = RULE
    if horizontal:
        ca.reverse_order = True
    return gfr


def numbered_point(s, x, y, w, num, head, body, size=11, head_size=12.5, h=None, color=BLUE):
    """A numbered key-point block. Returns bottom y."""
    c = rect(s, x, y + 0.02, 0.34, 0.34, color, shape=MSO_SHAPE.OVAL)
    tf = c.text_frame
    _nomargin(tf)
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    _add_runs(p, str(num), 11, True, WHITE)
    hh = wrap_lines(strip_md(head), head_size, (w - 0.5) * 0.985, True) * head_size * 1.2 / 72
    text(s, x + 0.5, y, w - 0.5, hh + 0.02, [head], size=head_size, bold=True, color=INK)
    bh = wrap_lines(strip_md(body), size, (w - 0.5) * 0.985) * size * 1.2 / 72 if body else 0
    if body:
        text(s, x + 0.5, y + hh + 0.06, w - 0.5, bh + 0.04, [body], size=size, color=INK2)
    return y + hh + 0.06 + bh


def pill(s, x, y, w, h, label, fill, color=WHITE, size=9, bold=True):
    shp = rect(s, x, y, w, h, fill, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    shp.adjustments[0] = 0.5
    tf = shp.text_frame
    _nomargin(tf)
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    _add_runs(p, label, size, bold, color)
    return shp
