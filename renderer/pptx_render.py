"""Storyline spec -> editable PPTX.

Every number on a slide comes from spec.data_points via a point's data_ref, or
is a placeholder drawn as a dashed "?" (D5). Charts are native PowerPoint charts
so the data stays editable (D3).
"""
import copy
import re

from lxml import etree
from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE, XL_LABEL_POSITION, XL_LEGEND_POSITION
from pptx.enum.dml import MSO_LINE_DASH_STYLE
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN

from . import measure
from pptx.oxml.ns import qn
from pptx.util import Emu, Inches, Pt

from . import tokens

G = tokens.GRID
S = tokens.SIZES
STICKER = "ILLUSTRATIVE — DATA NEEDED"


def rgb(h):
    h = h.lstrip("#")
    return RGBColor(int(h[:2], 16), int(h[2:4], 16), int(h[4:6], 16))


# ---------------------------------------------------------------- spec index

class Spec:
    def __init__(self, spec):
        self.raw = spec
        self.meta = spec.get("meta", {})
        self.dp = {d["id"]: d for d in spec.get("data_points", [])}
        self.src = {s["id"]: s for s in spec.get("sources", [])}
        self.sections = {s["id"]: s for s in spec.get("sections", [])}
        self.section_order = [s["id"] for s in spec.get("sections", [])]
        self.exec = spec.get("storyline", {}).get("exec_summary", [])

    def value(self, point):
        if not point or point.get("placeholder"):
            return None
        d = self.dp.get(point.get("data_ref"))
        return None if d is None else d.get("value")

    def dpoint(self, point):
        return None if not point or point.get("placeholder") else self.dp.get(point.get("data_ref"))


def collect_refs(obj, out=None):
    """All data_ref ids anywhere inside a slide."""
    out = [] if out is None else out
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == "data_ref" and isinstance(v, str):
                out.append(v)
            elif k in ("data_refs", "derived_from") and isinstance(v, list):
                out.extend(x for x in v if isinstance(x, str))
            else:
                collect_refs(v, out)
    elif isinstance(obj, list):
        for v in obj:
            collect_refs(v, out)
    return out


def has_placeholder(obj):
    if isinstance(obj, dict):
        if obj.get("placeholder") is True:
            return True
        return any(has_placeholder(v) for v in obj.values())
    if isinstance(obj, list):
        return any(has_placeholder(v) for v in obj)
    return False


# ---------------------------------------------------------------- formatting

def excel_format(unit, value_format=None):
    if value_format:
        return value_format
    return {"%": "0.0%", "x": '0.0"x"', "$M": '"$"#,##0"M"', "$B": '"$"#,##0.0"B"'}.get(unit or "", "#,##0.0")


def _num(v, decimals=None):
    if decimals is None:
        decimals = 0 if abs(v - round(v)) < 1e-9 else 1
    return f"{v:,.{decimals}f}"


def fmt(value, unit=None, value_format=None, signed=False):
    """Format a value for display. Without value_format: no trailing .0, unit-aware."""
    if value is None:
        return "?"
    sign = "+" if (signed and value > 0) else ""
    if value_format:
        f = value_format
        decimals = len(re.match(r"0*", f.split(".")[1]).group(0)) if "." in f else 0
        if f.endswith("%"):
            return f"{sign}{value * 100:.{decimals}f}%".replace("-", "−")
        out = f"{value:,.{decimals}f}"
        if unit == "x":
            out = _num(value) + "x"
        elif unit and unit.startswith("$"):
            out = "$" + out + unit[1:]
        elif '"$"' in f:
            out = "$" + out
        return (sign + out).replace("-", "−")
    if unit == "%":
        out = _num(value * 100) + "%"
    elif unit == "x":
        out = _num(value) + "x"
    elif unit and unit.startswith("$"):
        out = "$" + _num(value) + unit[1:]
    elif unit == "pp":
        out = _num(value) + " pp"
    else:
        out = _num(value)
    return (sign + out).replace("-", "−")


def dp_fmt(spec, point, value_format=None, signed=False):
    d = spec.dpoint(point)
    if d is None:
        return "?"
    if d.get("value_high") is not None:  # a range, e.g. 4–5 years
        lo = fmt(d["value"], d.get("unit"), value_format)
        hi = fmt(d["value_high"], d.get("unit"), value_format)
        unit_tail = hi[len(_num(d["value_high"])):] if hi.startswith(_num(d["value_high"])) else ""
        return f"{lo[:len(lo) - len(unit_tail)] if unit_tail and lo.endswith(unit_tail) else lo}–{hi}"
    return fmt(d.get("value"), d.get("unit"), value_format, signed)


# ---------------------------------------------------------------- primitives

class Canvas:
    def __init__(self, slide, tok):
        self.slide = slide
        self.t = tok

    def text(self, x, y, w, h, paras, size=S["body"], color=None, font=None, bold=False,
             align="l", anchor="t", wrap=True, line_spacing=None):
        """paras: str | list of str | list of list of (text, {bold,color,size,font}) runs."""
        box = self.slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
        tf = box.text_frame
        tf.word_wrap = wrap
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        tf.vertical_anchor = {"t": MSO_ANCHOR.TOP, "m": MSO_ANCHOR.MIDDLE, "b": MSO_ANCHOR.BOTTOM}[anchor]
        if isinstance(paras, str):
            paras = [paras]
        for i, para in enumerate(paras):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.alignment = {"l": PP_ALIGN.LEFT, "c": PP_ALIGN.CENTER, "r": PP_ALIGN.RIGHT}[align]
            if line_spacing:
                p.line_spacing = line_spacing
            runs = [(para, {})] if isinstance(para, str) else para
            first = runs[0][0] if runs else ""
            if first.strip() in ("–", "▪", "•") and first.endswith(" "):
                # hanging indent: wrapped lines align with the text, not the marker
                pPr = p._p.get_or_add_pPr()
                ind = int(Inches(0.2))
                pPr.set("marL", str(ind))
                pPr.set("indent", str(-ind))
                runs = [(first.strip() + "\t", runs[0][1])] + list(runs[1:])
            for txt, st in runs:
                r = p.add_run()
                r.text = txt
                f = r.font
                f.name = st.get("font", font or self.t["font_body"])
                f.size = Pt(st.get("size", size))
                f.bold = st.get("bold", bold)
                f.color.rgb = rgb(st.get("color", color or self.t["text"]))
        return box

    def rect(self, x, y, w, h, fill=None, line=None, dash=False, radius=None, weight=0.75, shape=None):
        shp = self.slide.shapes.add_shape(shape or (MSO_SHAPE.ROUNDED_RECTANGLE if radius else MSO_SHAPE.RECTANGLE),
                                          Inches(x), Inches(y), Inches(w), Inches(h))
        if radius and shape is None:
            shp.adjustments[0] = min(0.5, radius / max(0.01, min(w, h)))
        if fill:
            shp.fill.solid()
            shp.fill.fore_color.rgb = rgb(fill)
        else:
            shp.fill.background()
        if line:
            shp.line.color.rgb = rgb(line)
            shp.line.width = Pt(weight)
            if dash:
                shp.line.dash_style = MSO_LINE_DASH_STYLE.DASH
        else:
            shp.line.fill.background()
        shp.shadow.inherit = False
        tf = shp.text_frame
        tf.margin_left = tf.margin_right = Inches(0.08)
        return shp

    def label_in(self, shp, txt, size=S["label"], color=None, bold=False, align="c", font=None):
        tf = shp.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.alignment = {"l": PP_ALIGN.LEFT, "c": PP_ALIGN.CENTER, "r": PP_ALIGN.RIGHT}[align]
        r = p.add_run()
        r.text = txt
        r.font.size = Pt(size)
        r.font.bold = bold
        r.font.name = font or self.t["font_body"]
        r.font.color.rgb = rgb(color or self.t["text"])
        return shp

    def line(self, x1, y1, x2, y2, color=None, weight=0.75, dash=False):
        ln = self.slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1), Inches(x2), Inches(y2))
        ln.line.color.rgb = rgb(color or self.t["rule"])
        ln.line.width = Pt(weight)
        if dash:
            ln.line.dash_style = MSO_LINE_DASH_STYLE.DASH
        return ln


# ---------------------------------------------------------------- slide chrome

def unit_runs(unit_line, tok):
    """'**Metric**, unit' -> runs with the metric in bold."""
    parts = re.split(r"(\*\*[^*]+\*\*)", unit_line)
    runs = []
    for p in parts:
        if not p:
            continue
        if p.startswith("**"):
            runs.append((p[2:-2], {"bold": True, "color": tok["title"]}))
        else:
            runs.append((p, {"color": tok["muted"]}))
    return [runs]


def chrome(c, spec, slide, page_no, footnotes=None):
    t = c.t
    m = G["margin"]
    # tracker (S3): every section label, current one emphasised
    sid = slide.get("section_id")
    if sid and spec.section_order:
        runs = []
        for i, s_id in enumerate(spec.section_order):
            lab = spec.sections[s_id].get("tracker_label") or spec.sections[s_id]["title"]
            if i:
                runs.append(("    ", {}))
            cur = s_id == sid
            runs.append((f"{s_id} {lab}", {"bold": cur, "color": t["primary"] if cur else t["placeholder"]}))
        c.text(m, G["tracker_top"], 8, 0.2, [runs], size=S["tracker"])
    lm = slide.get("lead_message") or {}
    title = (lm.get("prefix", "") + " " + lm.get("text", "")).strip()
    if slide.get("archetype") == "statement" and slide.get("status") != "ghost":
        title = ""  # the statement itself is the title, set large in the body
    if title:
        c.text(m, G["title_top"], G["title_w"], G["title_h"], title, size=S["title"],
               color=t["title"], font=t["font_title"], bold=True, line_spacing=0.95)
    if slide.get("unit_line"):
        c.text(m, G["unit_top"], G["title_w"], G["unit_h"], unit_runs(slide["unit_line"], t), size=S["unit"])
    if slide.get("sticker") or has_placeholder(slide.get("body")) or has_placeholder(slide.get("layout")) or slide.get("status") == "ghost":
        w = 2.5
        shp = c.rect(G["slide_w"] - m - w, G["tracker_top"] - 0.04, w, 0.29, fill=t["caution_bg"],
                     line=t["caution"], radius=0.05)
        c.label_in(shp, slide.get("sticker") or STICKER, size=9, color=t["caution_ink"], bold=True)
    y = G["source_top"]
    notes = list(footnotes or []) + list(slide.get("footnotes", []))
    if notes:
        lines = [f"{i + 1}  {n}" for i, n in enumerate(notes)]
        top = y - 0.02 - G["line_h"] * len(lines)
        c.text(m, top, G["title_w"], G["line_h"] * len(lines), lines, size=S["source"], color=t["muted"])
    src = source_line(spec, slide)
    if src:
        c.text(m, y + (G["line_h"] if notes else 0) * 0, G["title_w"], G["line_h"], src, size=S["source"], color=t["muted"])
    c.text(G["slide_w"] - m - 0.5, y, 0.5, G["line_h"], str(page_no), size=S["source"], color=t["muted"], align="r")


def source_line(spec, slide):
    refs = collect_refs({"b": slide.get("body"), "l": slide.get("layout"), "m": slide.get("lead_message")})
    names, derived = [], False
    for r in refs:
        d = spec.dp.get(r)
        if not d:
            continue
        s = spec.src.get(d.get("source_id"), {})
        if s.get("kind") == "derived":
            derived = True
            for sub in d.get("derived_from", []):
                sd = spec.dp.get(sub)
                if sd:
                    ss = spec.src.get(sd.get("source_id"), {})
                    if ss.get("kind") != "derived" and ss.get("name") not in names:
                        names.append(ss.get("name"))
            continue
        if s.get("name") and s["name"] not in names:
            names.append(s["name"])
    if derived:
        names.append("team analysis")
    if not names:
        needs = has_placeholder(slide.get("body")) or slide.get("status") in ("ghost", "drafted")
        return "Source: to be confirmed" if needs else ""
    label = "Sources" if len(names) > 1 else "Source"
    return f"{label}: " + "; ".join(names)


# ---------------------------------------------------------------- body area

def body_box(slide):
    """(x, y, w, h) of the body: leaves room for the sidebar and the so-what bar."""
    m = G["margin"]
    x, y = m, G["content_top"]
    w = G["slide_w"] - 2 * m
    bottom = G["content_bottom"]
    if slide.get("so_what") and slide.get("status") != "ghost":
        bottom -= G["sowhat_h"] + G["gap"]
    if (slide.get("footnotes")):
        bottom -= G["line_h"] * len(slide["footnotes"])
    if slide.get("basis") and slide.get("status") != "ghost":
        bottom -= BASIS_H + G["gap"]
    lay = slide.get("layout") or {}
    has_side = lay.get("variant") == "takeaway_sidebar" or slide.get("status") == "ghost"
    if has_side and (slide.get("body") or {}).get("kind") != "matrix":
        w = w - G["sidebar_w"] - G["gap"] * 1.6
    return x, y, w, bottom - y


def sidebar(c, spec, slide, x=None, w=None):
    lay = slide.get("layout") or {}
    if lay.get("variant") != "takeaway_sidebar":
        return
    sb = lay.get("sidebar") or {}
    t = c.t
    m = G["margin"]
    w = w or G["sidebar_w"]
    x = x if x is not None else G["slide_w"] - m - w
    y = G["content_top"]
    bottom = G["content_bottom"] - ((G["sowhat_h"] + G["gap"]) if slide.get("so_what") else 0)
    h = bottom - y
    c.rect(x, y, w, h, fill=t["sidebar"], radius=0.06 if t["bar_radius"] else None)
    if (slide.get("body") or {}).get("kind") != "matrix":
        c.rect(x - G["gap"] * 1.35, y + h / 2 - 0.17, 0.2, 0.34, fill=t["sidebar"], shape=MSO_SHAPE.CHEVRON)
    ink = t["sidebar_text"]
    pad = 0.28
    cy = y + 0.24
    if sb.get("header"):
        size = S["takeaway"] + 2
        hh = _est_h(sb["header"], w - 2 * pad, size, 1.0, bold=True, title=True)
        c.text(x + pad, cy, w - 2 * pad, hh, sb["header"], size=size, bold=True, color=ink, font=t["font_title"], line_spacing=1.0)
        cy += hh + (0.06 if sb.get("kind") == "big_number" else 0.2)
    kind = sb.get("kind")
    if kind == "big_number":
        p = sb.get("big_number")
        color = (t["big_number"] if spec.dpoint(p) else t["placeholder"])
        bsize = S["big_number"] + 10
        bh = bsize * 1.0 / 72  # the box hugs the figures; Georgia's line gap would leave a hole above them
        c.text(x + pad, cy, w - 2 * pad, bh, dp_fmt(spec, p), size=bsize, bold=True, color=color, font=t["font_title"],
               line_spacing=0.85)
        cy += bh + 0.12
        if sb.get("caption"):
            ch = _est_h(sb["caption"], w - 2 * pad, S["body"] + 1, 1.1)
            c.text(x + pad, cy, w - 2 * pad, ch, sb["caption"], size=S["body"] + 1, color=ink, line_spacing=1.1)
            cy += ch + 0.22
    if kind == "reasons":
        n = len(sb.get("reasons", []))
        room = (bottom - (0.55 if sb.get("note") else 0.2)) - cy
        step = room / max(1, n)
        for i, r in enumerate(sb.get("reasons", [])):
            ry = cy + i * step
            dot = c.rect(x + pad, ry + 0.02, 0.34, 0.34, fill=t["primary"] if not t["dark_sidebar"] else t["white"], shape=MSO_SHAPE.OVAL)
            c.label_in(dot, str(i + 1), size=S["label"], bold=True, color=t["white"] if not t["dark_sidebar"] else t["primary"])
            head = r["header"]
            pt = r.get("point")
            known = pt and spec.dpoint(pt)
            runs = [(head, {"bold": True, "color": ink, "size": S["header"] + 1})]
            if known:
                runs.append(("   " + dp_fmt(spec, pt), {"bold": True, "color": t["highlight"], "size": S["header"] + 1}))
            c.text(x + pad + 0.5, ry, w - 2 * pad - 0.5, 0.35, [runs], size=S["header"])
            paras = [[(r["detail"], {"color": ink})]]
            if pt and not known:
                need = pt.get("label") or "a number to back this up"
                paras.append([("Data needed: ", {"bold": True, "color": t["caution_ink"], "size": S["label"]}),
                              (need, {"color": t["caution_ink"], "size": S["label"]})])
            dsize = fit_size([r["detail"]] + ([pt.get("label") or ""] if pt and not known else []), w - 2 * pad - 0.5, step - 0.5,
                             S["body"], min_size=11, indent=0, line_spacing=1.1)
            c.text(x + pad + 0.5, ry + 0.36, w - 2 * pad - 0.5, step - 0.45, paras, size=dsize, line_spacing=1.1)
            if i < n - 1:
                c.line(x + pad, ry + step - 0.1, x + w - pad, ry + step - 0.1, color=t["rule"])
    rows = sb.get("rows", [])
    vw = 1.0
    lw_ = w - 2 * pad - vw - 0.1
    def row_need(r):  # label (wraps early: bold, conservative), basis line, bar, gap
        lh = _est_h(r["label"], lw_, S["body"] - 1, 1.0, bold=bool(r.get("highlight")))
        bh_ = (_est_h(r["basis"], lw_, S["label"], 1.0) + 0.04) if r.get("basis") else 0
        return max(0.3, lh) + bh_ + 0.04 + 0.08 + 0.1
    needs_r = [row_need(r) for r in rows]
    reserve = (sum(needs_r) + 0.3 if rows else 0) + (0.5 if sb.get("note") else 0) + 0.1
    bullets = sb.get("bullets", [])
    if bullets:
        room = bottom - reserve - cy
        plain = [b.replace("**", "") for b in bullets]
        size = fit_size(bullets, w - 2 * pad, room - 0.12 * len(bullets), S["body"] + 2, min_size=10.5, line_spacing=1.12)
        heights = [_est_h(b, w - 2 * pad - 0.2, size, 1.12) for b in bullets]
        gap = min(0.42, max(0.06, (room - sum(heights)) / max(1, len(bullets))))
        if rows and cy + sum(heights) + 0.06 * len(bullets) > bottom - reserve + 0.15:
            SIDEBAR_WARN.append(f"slide {slide['id']}: sidebar bullets and value rows do not both fit; shorten the bullets or drop a row")
        for b, bh in zip(bullets, heights):
            runs = [("▪  ", {"color": t["highlight"] if not t["dark_sidebar"] else ink})]
            for k, part in enumerate(b.split("**")):
                if part:
                    runs.append((part, {"color": ink, "bold": k % 2 == 1}))
            c.text(x + pad, cy, w - 2 * pad, bh, [runs], size=size, line_spacing=1.12)
            cy += bh + gap
    if rows:
        # rows sit on the bottom of the sidebar so they can never run out of it (F6); bullets fill the space above
        cy = (bottom - (0.55 if sb.get("note") else 0.1)) - sum(needs_r) - 0.12
        c.line(x + pad, cy, x + w - pad, cy, color=t["rule"] if not t["dark_sidebar"] else ink)
        cy += 0.12
        vals = [abs(spec.value(r["point"]) or 0) for r in rows]
        vmax = max(vals) or 1
        spare = 0.0
        same_unit = len({(spec.dpoint(r["point"]) or {}).get("unit") for r in rows}) == 1
        for r, v, nd in zip(rows, vals, needs_r):
            rh = nd + spare
            on = r.get("highlight")
            ph = spec.dpoint(r["point"]) is None
            lh = _est_h(r["label"], lw_, S["body"] - 1, 1.0, bold=bool(on))
            c.text(x + pad, cy, lw_, lh, r["label"], size=S["body"] - 1, bold=on, color=ink, line_spacing=1.0)
            if r.get("basis"):  # B-08: how the estimate was built
                bh_ = _est_h(r["basis"], lw_, S["label"], 1.0)
                c.text(x + pad, cy + lh + 0.02, lw_, bh_, r["basis"], size=S["label"], color=t["muted"] if not t["dark_sidebar"] else ink, line_spacing=1.0)
                lh += bh_ + 0.04
            c.text(x + w - pad - vw, cy - 0.03, vw, 0.34, dp_fmt(spec, r["point"]), size=S["header"] + 2, bold=True, font=t["font_title"],
                   color=t["placeholder"] if ph else (t["highlight"] if on else ink), align="r")
            by = cy + max(0.3, lh) + 0.04
            if same_unit:  # bars compare values only when they share a unit
                bw_ = (w - 2 * pad) * (v / vmax if not ph else 0.4)
                c.rect(x + pad, by, max(0.04, bw_), 0.08, fill=None if ph else (t["highlight"] if on else t["other_bars"]),
                       line=t["placeholder"] if ph else None, dash=ph)
            else:
                c.line(x + pad, by + 0.06, x + w - pad, by + 0.06, color=t["rule"] if not t["dark_sidebar"] else ink)
            cy = max(cy + rh, by + 0.14)
    if sb.get("note"):
        c.text(x + pad, bottom - 0.45, w - 2 * pad, 0.3, sb["note"], size=S["label"] + 1, bold=True, color=t["caution_ink"] if not t["dark_sidebar"] else ink)


# ---------------------------------------------------------------- charts

CHART_TYPES = {
    "bar": XL_CHART_TYPE.BAR_CLUSTERED,
    "survey_bar": XL_CHART_TYPE.BAR_CLUSTERED,
    "column": XL_CHART_TYPE.COLUMN_CLUSTERED,
    "stacked_column": XL_CHART_TYPE.COLUMN_STACKED,
    "stacked_100": XL_CHART_TYPE.COLUMN_STACKED_100,
    "line": XL_CHART_TYPE.LINE_MARKERS,
    "waterfall": XL_CHART_TYPE.COLUMN_STACKED,
    "scatter": XL_CHART_TYPE.XY_SCATTER,
}


def _font(obj, tok, size=S["label"], color=None, bold=False):
    obj.font.size = Pt(size)
    obj.font.name = tok["font_body"]
    obj.font.bold = bold
    obj.font.color.rgb = rgb(color or tok["text"])


def _clean_axes(chart, tok, show_values=False):
    va = chart.value_axis
    va.has_major_gridlines = False
    va.has_minor_gridlines = False
    va.visible = show_values
    va.format.line.fill.background()
    ca = chart.category_axis
    ca.format.line.color.rgb = rgb(tok["rule"])
    ca.has_major_gridlines = False
    from pptx.enum.chart import XL_TICK_MARK
    ca.major_tick_mark = XL_TICK_MARK.NONE
    va.major_tick_mark = XL_TICK_MARK.NONE
    _font(ca.tick_labels, tok)
    _font(va.tick_labels, tok, color=tok["muted"])


def _fill(fmt_obj, color, dash_line=None):
    if color:
        fmt_obj.fill.solid()
        fmt_obj.fill.fore_color.rgb = rgb(color)
    else:
        fmt_obj.fill.background()
    if dash_line:
        fmt_obj.line.color.rgb = rgb(dash_line)
        fmt_obj.line.width = Pt(1)
        fmt_obj.line.dash_style = MSO_LINE_DASH_STYLE.DASH
    else:
        fmt_obj.line.fill.background()


def _sorted(body, spec):
    cats = list(body["categories"])
    series = body["series"]
    if body.get("sort", "desc") in ("desc", "asc") and body["chart_type"] in ("bar", "survey_bar") and len(series) == 1:
        vals = [spec.value(p) for p in series[0]["points"]]
        order = sorted(range(len(cats)), key=lambda i: (vals[i] is None, -(vals[i] or 0)))
        if body.get("sort") == "asc":
            order = order[::-1]
        cats = [cats[i] for i in order]
        series = [dict(s, points=[s["points"][i] for i in order]) for s in series]
    return cats, series


def chart(c, spec, slide, body, box):
    x, y, w, h = box
    t = c.t
    ctype = body["chart_type"]
    if ctype == "waterfall":
        return waterfall(c, spec, body, box)
    cats, series = _sorted(body, spec)
    known = [spec.value(p) for s in series for p in s["points"] if spec.value(p) is not None]
    stand_in = (sum(known) / len(known)) if known else None
    bench = body.get("benchmark")
    bench_line = bench if (bench and ctype in ("column", "line", "stacked_column")) else None
    if bench_line:
        bench = None
    if bench and ctype in ("bar", "survey_bar") and len(series) == 1:
        cats = cats + [bench["label"]]
        series = [dict(series[0], points=series[0]["points"] + [bench["point"]])]
    synth = _stand_ins(len(cats), ctype)
    cd = CategoryChartData()
    cd.categories = cats
    unit = None
    for s in series:
        vals = []
        for i, p in enumerate(s["points"]):
            v = spec.value(p)
            d = spec.dpoint(p)
            unit = unit or (d or {}).get("unit")
            vals.append(v if v is not None else (stand_in if stand_in is not None else synth[i]))
        cd.add_series(s["name"], vals)
    nf = excel_format(unit, body.get("value_format"))
    gf = c.slide.shapes.add_chart(CHART_TYPES[ctype], Inches(x), Inches(y), Inches(w), Inches(h), cd)
    ch = gf.chart
    ch.has_title = False
    ch.font.name = t["font_body"]
    ch.font.size = Pt(S["label"] + 1)
    if bench_line:
        _bench_line(c, spec, ch, bench_line, (x, y, w, h), [v for s_ in series for v in [spec.value(p) for p in s_["points"]] if v is not None], unit, body.get("value_format"))
    multi = len(series) > 1
    ch.has_legend = multi and ctype != "line"
    if ch.has_legend:
        ch.legend.position = XL_LEGEND_POSITION.TOP
        ch.legend.include_in_layout = False
        _font(ch.legend, t, size=S["label"] + 1)
    _clean_axes(ch, t)
    _font(ch.category_axis.tick_labels, t, size=S["label"] + 1)
    if ctype in ("bar", "survey_bar"):
        ch.category_axis.reverse_order = True
    plot = ch.plots[0]
    if hasattr(plot, "gap_width"):
        plot.gap_width = 45
    if ctype in ("stacked_column", "stacked_100"):
        plot.overlap = 100
    highlight = set(body.get("highlight", []))
    palette = [t["other_bars"], t["gray_light"], t["gray_mid"], t["gray_dark"], t["primary"]]
    for si, (s_spec, s_obj) in enumerate(zip(series, plot.series)):
        base = palette[si % len(palette)] if multi else t["other_bars"]
        if multi and s_spec["name"] in highlight:
            base = t["highlight"]
        if ctype == "line":
            on = s_spec["name"] in highlight or not multi
            s_obj.format.line.color.rgb = rgb(t["highlight"] if on else t["gray_mid"])
            s_obj.format.line.width = Pt(2.75 if on else 2)
            s_obj.smooth = False
            from pptx.enum.chart import XL_MARKER_STYLE
            s_obj.marker.style = XL_MARKER_STYLE.NONE
        else:
            _fill(s_obj.format, base)
        s_obj.invert_if_negative = False
        for pi, p in enumerate(s_spec["points"]):
            pt = s_obj.points[pi]
            cat = cats[pi]
            is_bench = bench is not None and pi == len(cats) - 1 and cat == bench["label"]
            if ctype != "line":
                if p.get("placeholder"):
                    _fill(pt.format, t["gray_light"] if not (cat in highlight) else None,
                          dash_line=t["highlight"] if cat in highlight else t["placeholder"])
                elif is_bench:
                    _fill(pt.format, None, dash_line=t["gray_dark"])
                elif not multi and cat in highlight:
                    _fill(pt.format, t["highlight"])
            if ctype == "line" and pi not in (0, len(s_spec["points"]) - 1):
                continue
            dl = pt.data_label
            dl.has_text_frame = True
            val_txt = "?" if p.get("placeholder") else fmt(spec.value(p), unit, nf)
            if ctype == "line" and pi == len(s_spec["points"]) - 1:
                val_txt = f"{s_spec['name']}  {val_txt}"
            dl.text_frame.text = val_txt
            run = dl.text_frame.paragraphs[0].runs[0]
            hl = (cat in highlight and not multi) or s_spec["name"] in highlight
            run.font.size = Pt(S["label"] + 2)
            run.font.bold = hl or p.get("placeholder", False)
            run.font.name = t["font_body"]
            stacked = ctype in ("stacked_column", "stacked_100")
            on_dark = stacked and s_spec["name"] in highlight
            run.font.color.rgb = rgb(t["white"] if on_dark else (t["placeholder"] if p.get("placeholder") else t["title"]))
            if ctype == "line":
                dl.position = XL_LABEL_POSITION.RIGHT if pi else XL_LABEL_POSITION.LEFT
            else:
                dl.position = XL_LABEL_POSITION.CENTER if stacked else XL_LABEL_POSITION.OUTSIDE_END
    return gf


def waterfall(c, spec, body, box):
    """Native stacked column with an invisible base series (editable)."""
    x, y, w, h = box
    t = c.t
    cats = body["categories"]
    pts = body["series"][0]["points"]
    vals = [spec.value(p) for p in pts]
    unit = next(((spec.dpoint(p) or {}).get("unit") for p in pts if spec.dpoint(p)), None)
    nf = excel_format(unit, body.get("value_format"))
    n = len(cats)
    synth = _stand_ins(n, "waterfall")
    if any(v is not None for v in vals):
        known = [abs(v) for v in vals if v is not None]
        avg = sum(known) / len(known)
        synth = [avg] + [avg * 0.25] * (n - 2) + [avg * 1.2]
    base, height, running = [], [], 0.0
    for i, v0 in enumerate(vals):
        v = synth[i] if v0 is None else v0
        if i == 0 or i == n - 1:
            total = v if (i == 0 or v0 is not None) else running
            base.append(0)
            height.append(total)
            running = total
        else:
            base.append(running if v >= 0 else running + v)
            height.append(abs(v))
            running += v
    cd = CategoryChartData()
    cd.categories = cats
    cd.add_series("base", base)
    cd.add_series(body["series"][0]["name"], height)
    gf = c.slide.shapes.add_chart(XL_CHART_TYPE.COLUMN_STACKED, Inches(x), Inches(y), Inches(w), Inches(h), cd)
    ch = gf.chart
    ch.has_title = False
    ch.has_legend = False
    ch.font.name = t["font_body"]
    _clean_axes(ch, t)
    _font(ch.category_axis.tick_labels, t, size=S["label"] + 1)
    plot = ch.plots[0]
    plot.gap_width = 40
    plot.overlap = 100
    b, s = plot.series
    _fill(b.format, None)
    _fill(s.format, t["other_bars"])
    highlight = set(body.get("highlight", []))
    for i, p in enumerate(pts):
        pt = s.points[i]
        total = i in (0, n - 1)
        hl = cats[i] in highlight
        if p.get("placeholder"):
            _fill(pt.format, t["gray_light"] if total else (None if hl else None),
                  dash_line=t["highlight"] if hl else t["placeholder"])
        elif total:
            _fill(pt.format, t["primary"])
        elif hl:
            _fill(pt.format, t["highlight"])
        dl = pt.data_label
        dl.has_text_frame = True
        v = vals[i]
        unit_ph = "$?M" if (unit or "$M").startswith("$") else "?"
        sign = "+" if (not total and (v is None or v > 0)) else ""
        dl.text_frame.text = (sign + unit_ph) if v is None else sign + fmt(v, unit, nf)
        r = dl.text_frame.paragraphs[0].runs[0]
        r.font.size = Pt(S["label"] + 2)
        r.font.bold = True
        r.font.name = t["font_body"]
        dark = (total or hl) and v is not None
        r.font.color.rgb = rgb(t["white"] if dark else (t["highlight"] if hl else (t["placeholder"] if v is None else t["title"])))
        dl.position = XL_LABEL_POSITION.INSIDE_END
    return gf


# ---------------------------------------------------------------- other bodies

def kpi(c, spec, body, box):
    x, y, w, h = box
    t = c.t
    items = body["items"]
    n = len(items)
    gap = G["gap"]
    tw = (w - gap * (n - 1)) / n
    caps = [_est_h(it["caption"], tw - 0.46, (S["header"] + 2) * 1.08, 1.0) for it in items]
    th = max(min(2.15, h * 0.45), 1.2 + max(caps) + (0.5 if any(it.get("relation") for it in items) else 0.1))
    dh0 = y + h - (y + th + 0.2) - 0.27
    common = min([fit_size(it.get("drivers", []), tw, dh0, S["body"]) for it in items if it.get("drivers")] or [S["body"]])
    for i, it in enumerate(items):
        tx = x + i * (tw + gap)
        ph = it["point"].get("placeholder")
        c.rect(tx, y, tw, th, fill=None if ph else t["panel"], line=t["placeholder"] if ph else None, dash=bool(ph))
        c.rect(tx, y, tw, 0.05, fill=t["placeholder"] if ph else t["primary"])
        c.text(tx + 0.23, y + 0.22, tw - 0.46, 0.85, dp_fmt(spec, it["point"]), size=S["kpi"],
               bold=True, color=t["placeholder"] if ph else t["highlight"], font=t["font_title"])
        cap_h = _est_h(it["caption"], tw - 0.46, (S["header"] + 2) * 1.08, 1.0)
        c.text(tx + 0.23, y + 1.18, tw - 0.46, cap_h, it["caption"], size=S["header"] + 2, bold=True, color=t["title"], line_spacing=1.0)
        if it.get("relation"):
            c.text(tx + 0.23, y + 1.2 + cap_h + 0.04, tw - 0.46, 0.45, it["relation"], size=S["label"], color=t["muted"])
        drivers = it.get("drivers", [])
        if drivers:
            dy = y + th + 0.2
            c.text(tx, dy, tw, 0.22, "WHAT IS MISSING" if ph else "WHAT DRIVES IT", size=S["small"] - 1, bold=True,
                   color=t["caution_ink"] if ph else t["muted"])
            paras = [[("–  ", {"color": t["muted"]}), (d, {"color": t["muted"] if ph else t["text"]})] for d in drivers]
            dh = y + h - dy - 0.27
            c.text(tx, dy + 0.27, tw, dh, paras, size=common, line_spacing=1.1)


def matrix(c, spec, slide, body, box):
    x, y, w, h = box
    t = c.t
    size = min(h - 0.35, w * 0.42)
    ox = x + 0.5
    oy = y + 0.05
    q = size / 2
    labels = body.get("quadrant_labels") or ["", "", "", ""]
    pos = {"top-left": (0, 0), "top-right": (1, 0), "bottom-left": (0, 1), "bottom-right": (1, 1)}
    for i, key in enumerate(["top-left", "top-right", "bottom-left", "bottom-right"]):
        cx, cy = pos[key]
        focus = body.get("focus_quadrant") == key
        c.rect(ox + cx * q, oy + cy * q, q, q, fill=(t["sidebar"] if not t["dark_sidebar"] else t["panel"]) if focus else None, line=t["rule"])
        ly = oy + cy * q + (0.1 if cy == 0 else q - 0.36)
        c.text(ox + cx * q + 0.12, ly, q - 0.24, 0.3, labels[i], size=S["label"] + 1, bold=focus,
               color=t["primary"] if focus else t["muted"])
    xa, ya = body["x_axis"], body["y_axis"]
    c.text(ox, oy + size + 0.06, size, 0.24, xa.get("low", ""), size=S["small"], color=t["muted"])
    c.text(ox, oy + size + 0.06, size, 0.24, xa.get("high", ""), size=S["small"], color=t["muted"], align="r")
    c.text(ox, oy + size + 0.04, size, 0.26, xa["label"] + " →", size=S["label"] + 1, bold=True, color=t["title"], align="c")
    cx_axis, cy_axis = ox - 0.3, oy + size / 2
    for txt, al, sz, bold, col in ((ya["label"] + " →", "c", S["label"] + 1, True, t["title"]),
                                   (ya.get("low", ""), "l", S["small"], False, t["muted"]),
                                   (ya.get("high", ""), "r", S["small"], False, t["muted"])):
        tb = c.text(cx_axis - size / 2, cy_axis - 0.12, size, 0.24, txt, size=sz, bold=bold, color=col, align=al, wrap=False)
        tb.rotation = 270
    hl = set((slide.get("lead_message") or {}).get("highlights", []))
    sizes = [it.get("size") for it in body["items"] if it.get("size")]
    for it in body["items"]:
        px = ox + it["x"] * size
        py = oy + (1 - it["y"]) * size
        r = 0.12 if not it.get("size") else 0.09 + 0.2 * (it["size"] / max(sizes))
        on = it["label"] in hl
        c.rect(px - r, py - r, 2 * r, 2 * r, fill=t["highlight"] if on else t["other_bars"], shape=MSO_SHAPE.OVAL)
        c.text(px + r + 0.07, py - 0.14, 2.4, 0.3, it["label"], size=S["body"], bold=on, color=t["title"] if on else t["text"])
    # the takeaway panel takes the rest of the width (A-12)
    px0 = ox + size + 0.42
    sidebar(c, spec, slide, x=px0, w=x + w - px0)


_LN_ORDER = ["a:lnL", "a:lnR", "a:lnT", "a:lnB"]


def _cell_border(cell, side, color, w_pt=0.75):
    """Set one cell border. a:lnL/R/T/B must come first in tcPr, in this order."""
    tcPr = cell._tc.get_or_add_tcPr()
    tag = {"l": "a:lnL", "r": "a:lnR", "t": "a:lnT", "b": "a:lnB"}[side]
    for old in tcPr.findall(qn(tag)):
        tcPr.remove(old)
    ln = etree.Element(qn(tag), w=str(int(w_pt * 12700)))
    if color is None:
        etree.SubElement(ln, qn("a:noFill"))
    else:
        sf = etree.SubElement(ln, qn("a:solidFill"))
        etree.SubElement(sf, qn("a:srgbClr"), val=color.lstrip("#"))
    rank = _LN_ORDER.index(tag)
    pos = 0
    for i, child in enumerate(list(tcPr)):
        if child.tag in [qn(x) for x in _LN_ORDER[:rank]]:
            pos = i + 1
    tcPr.insert(pos, ln)


def harvey(c, cx, cy, r, rating, tok):
    """Harvey ball: outline circle + filled wedge (editable shapes)."""
    c.rect(cx - r, cy - r, 2 * r, 2 * r, fill=tok["white"], line=tok["primary"], weight=1, shape=MSO_SHAPE.OVAL)
    if rating >= 4:
        c.rect(cx - r, cy - r, 2 * r, 2 * r, fill=tok["primary"], line=tok["primary"], weight=1, shape=MSO_SHAPE.OVAL)
    elif rating > 0:
        pie = c.rect(cx - r, cy - r, 2 * r, 2 * r, fill=tok["primary"], shape=MSO_SHAPE.PIE)
        # python-pptx writes adj * 100000; PowerPoint reads angles in 1/60000 degree,
        # so degrees -> adj is * 0.6. Angles run clockwise from 3 o'clock.
        start = 270.0                                   # 12 o'clock
        end = (start + 90.0 * rating) % 360.0
        pie.adjustments[0] = start * 0.6
        pie.adjustments[1] = end * 0.6


def _lines(text, w, size, bold=False):
    """Lines a text needs in a table cell or shape w inches wide (0.12 in insets each side)."""
    return sum(measure.lines(part, w - 0.26, FONTS["body"], size, bold) for part in str(text).split("\n"))


def table(c, spec, body, box, slide=None):
    """Native table. Row heights are computed from the text so PowerPoint never grows a row on its own;
    Harvey balls, the legend and the verdict column all sit on those computed heights (F7)."""
    x, y, w, h = box
    t = c.t
    cols = list(body["columns"])
    rows = body["rows"]
    co = (slide or {}).get("callout")
    co_row = next((i for i, r_ in enumerate(rows) if co and co["target"] in (r_["label"], r_.get("badge"))), None)
    harvey_type = body["table_type"] == "harvey"
    last_text = harvey_type and all(r["cells"] and r["cells"][-1].get("rating") is None and r["cells"][-1].get("text") for r in rows)
    # verdict lives inside the table as its last column (B-02 reading order, matches public decks)
    verdict = (co_row is not None or any(r.get("note") for r in rows)) and not last_text
    if verdict:
        cols.append(body.get("verdict_header") or "Verdict")
    legend_h = 0.34 if (harvey_type or body.get("legend")) else 0
    ncols = len(cols) + 1
    first_w = w * 0.19
    widths = [first_w] + [0] * (ncols - 1)
    if last_text or verdict:
        widths[-1] = w * 0.27
        mid = (w - first_w - widths[-1]) / max(1, ncols - 2)
        for j in range(1, ncols - 1):
            widths[j] = mid
    else:
        for j in range(1, ncols):
            widths[j] = (w - first_w) / (ncols - 1)

    def cell_texts(i, row):
        out = []
        for j, cell in enumerate(row["cells"], start=1):
            txt = dp_fmt(spec, cell["point"]) if cell.get("point") else cell.get("text", "")
            out.append("" if (harvey_type and cell.get("rating") is not None) else txt)
        if verdict:
            if i == co_row:
                out.append(co["header"] + ("\n" + co["detail"] if co.get("detail") else ""))
            else:
                out.append(row.get("note", ""))
        return out

    def heights(size):
        lsize = size + 1
        hh = max(_lines(col, widths[j], size, bold=True) for j, col in enumerate(cols, start=1)) * size * 1.2 / 72 + 0.16
        rh = []
        for i, row in enumerate(rows):
            n = max([_lines(row["label"], widths[0], lsize, bold=True)] +
                    [_lines(tx, widths[j], size) for j, tx in enumerate(cell_texts(i, row), start=1) if tx])
            need = n * size * 1.2 / 72 + 0.18
            if harvey_type:
                need = max(need, 0.5)
            rh.append(need)
        return hh, rh

    size = S["body"]
    while True:
        head_h, rhs = heights(size)
        if head_h + sum(rhs) <= h - legend_h or size <= 10:
            break
        size -= 0.5
    spare = max(0.0, (h - legend_h) - head_h - sum(rhs))
    rhs = [r_ + spare / len(rhs) for r_ in rhs] if spare < 0.6 * len(rhs) else [r_ + 0.6 for r_ in rhs]
    tops, acc = [], y + head_h
    for r_ in rhs:
        tops.append(acc)
        acc += r_
    nrows = len(rows) + 1
    gf = c.slide.shapes.add_table(nrows, ncols, Inches(x), Inches(y), Inches(w), Inches(head_h + sum(rhs)))
    tb = gf.table
    tblPr = tb._tbl.tblPr
    for attr in ("bandRow", "firstRow"):
        tblPr.set(attr, "0")
    style = tblPr.find(qn("a:tableStyleId"))
    if style is not None:
        style.text = "{2D5ABB26-0587-4C30-8999-92F81FD0307C}"  # "No Style, No Grid"
    for j, cw in enumerate(widths):
        tb.columns[j].width = Inches(cw)
    tb.rows[0].height = Inches(head_h)
    for i, r_ in enumerate(rhs, start=1):
        tb.rows[i].height = Inches(r_)

    def put(cell, text, bold=False, color=None, size=S["body"], align="l", fill=None, runs=None):
        if fill:
            cell.fill.solid()
            cell.fill.fore_color.rgb = rgb(fill)
        else:
            cell.fill.background()
        cell.margin_left = cell.margin_right = Inches(0.12)
        cell.margin_top = cell.margin_bottom = Inches(0.05)
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf = cell.text_frame
        tf.word_wrap = True
        parts = runs or [(text, bold, color)]
        for k, (tx, bd, col) in enumerate(parts):
            p = tf.paragraphs[0] if k == 0 else tf.add_paragraph()
            p.alignment = {"l": PP_ALIGN.LEFT, "c": PP_ALIGN.CENTER}[align]
            if k == 0:
                p.text = ""
            r = p.add_run()
            r.text = tx
            r.font.size = Pt(size)
            r.font.bold = bd
            r.font.name = t["font_body"]
            r.font.color.rgb = rgb(col or t["text"])
        for side in "lrt":
            _cell_border(cell, side, None)
        _cell_border(cell, "b", t["rule"])

    put(tb.cell(0, 0), "")
    for j, col in enumerate(cols, start=1):
        is_text_col = (last_text or verdict) and j == ncols - 1
        put(tb.cell(0, j), col, bold=True, color=t["title"], size=size, align="l" if (is_text_col or not harvey_type) else "c")
    for j in range(ncols):
        _cell_border(tb.cell(0, j), "b", t["primary"], 1.5)
    for i, row in enumerate(rows, start=1):
        on = row.get("highlight") or (i - 1) == co_row
        tint = t["sidebar"] if on and not t["dark_sidebar"] else (t["panel"] if on else None)
        label = (row.get("badge", "") + "  " if row.get("badge") else "") + row["label"]
        put(tb.cell(i, 0), label, bold=True, color=t["highlight"] if on else t["title"], size=size + 1, fill=tint)
        texts = cell_texts(i - 1, row)
        for j, txt in enumerate(texts, start=1):
            cell = row["cells"][j - 1] if j - 1 < len(row["cells"]) else {}
            is_text_col = (last_text or verdict) and j == ncols - 1
            if verdict and j == ncols - 1 and (i - 1) == co_row:
                runs = [(co["header"], True, t["highlight"])] + ([(co["detail"], False, t["title"])] if co.get("detail") else [])
                put(tb.cell(i, j), "", size=size, fill=tint, runs=runs)
                continue
            put(tb.cell(i, j), txt,
                bold=bool(on and (is_text_col or cell.get("point"))),
                color=(t["highlight"] if (on and is_text_col) else (t["title"] if on or cell.get("point") else t["text"])),
                size=size, align="l" if (is_text_col or not harvey_type) else "c", fill=tint)
    bottom = y + head_h + sum(rhs)
    if harvey_type:
        r = min(0.19, min(rhs) * 0.3)
        xs, acc = [], x
        for cw in widths:
            xs.append(acc + cw / 2)
            acc += cw
        for i, row in enumerate(rows):
            cy = tops[i] + rhs[i] / 2
            for j, cell in enumerate(row["cells"]):
                if cell.get("rating") is not None:
                    harvey(c, xs[j + 1], cy, r, cell["rating"], t)
        ly = bottom + 0.1
        c.text(x, ly, 0.6, 0.24, "Weak", size=S["small"], color=t["muted"])
        lx = x + 0.55
        for q_ in range(5):
            harvey(c, lx + 0.1, ly + 0.11, 0.09, q_, t)
            lx += 0.3
        c.text(lx + 0.05, ly, 0.8, 0.24, "Strong", size=S["small"], color=t["muted"])
        if body.get("legend"):
            c.text(lx + 0.9, ly, w - (lx + 0.9 - x), 0.24, body["legend"], size=S["small"], color=t["muted"])
    elif body.get("legend"):
        c.text(x, bottom + 0.1, w, 0.24, body["legend"], size=S["small"], color=t["muted"])
    return gf


def text_body(c, spec, slide, body, box):
    x, y, w, h = box
    t = c.t
    style = body["style"]
    if style == "statement":
        st = body.get("statement") or {}
        lm = (slide.get("lead_message") or {}).get("text", "")
        emph = st.get("emphasis", [])
        pattern = "(" + "|".join(re.escape(e) for e in emph) + ")" if emph else None
        runs = [(part, {"color": t["highlight"] if part in emph else t["title"]})
                for part in (re.split(pattern, lm) if pattern else [lm]) if part]
        if st.get("split"):
            pw = w * 0.5
            c.rect(x, y, pw, h, fill=t["primary"])
            c.text(x + 0.5, y, pw - 1.0, h, [[(r[0], {"color": t["white"]}) for r in runs]], size=32, bold=True,
                   font=t["font_title"], anchor="m")
            if st.get("support"):
                c.text(x + pw + 0.5, y, w - pw - 0.8, h, st["support"], size=S["header"] + 4, anchor="m")
        else:
            # statement and support sit together as one block, centered vertically (as in the references)
            size = 38
            sh = _est_h(lm, w - 0.8, size * 1.25, 1.0)
            sup = st.get("support")
            sup_h = _est_h(sup, w - 0.8, S["header"] + 4, 1.1) if sup else 0
            gap = 0.3 if sup else 0
            top = y + max(0, (h - (sh + gap + sup_h)) / 2)
            c.text(x + 0.4, top, w - 0.8, sh, [runs], size=size, bold=True, font=t["font_title"], align="l", line_spacing=1.0)
            if sup:
                c.rect(x + 0.4, top + sh + gap - 0.12, 0.9, 0.04, fill=t["highlight"])
                c.text(x + 0.4, top + sh + gap, w - 0.8, sup_h, sup, size=S["header"] + 4, color=t["muted"])
        return
    if style == "bullets":
        paras = []
        for b in body.get("bullets", []):
            paras.append([("▪  ", {"color": t["highlight"]}), (b["text"], {"bold": True, "color": t["title"]})])
            for sub in b.get("sub", []):
                paras.append([("      –  " + sub, {})])
        c.text(x, y, w, h, paras, size=S["body"] + 2, line_spacing=1.3)
        return
    cols = body.get("columns", [])
    n = len(cols)
    gap = G["gap"]
    cw = (w - gap * (n - 1)) / n
    common = min([fit_size(col.get("detail", []), cw - 0.38, h - 0.9 - _reserve(slide, col) - 0.3, S["body"])
                  for col in cols] or [S["body"]])
    for i, col in enumerate(cols):
        cx = x + i * (cw + gap)
        emph = col.get("emphasis")
        target = _is_target(slide, col)
        c.rect(cx, y, cw, h, fill=t["white"])
        hdr_h = 0.9
        c.rect(cx, y, cw, hdr_h, fill=t["primary"] if emph else t["panel"])
        # the outline goes on top of the header fill, so the stroke keeps one width all the way round
        c.rect(cx, y, cw, h, fill=None, line=t["highlight"] if target else t["rule"], weight=2 if target else 0.75)
        dot = c.rect(cx + 0.19, y + 0.19, 0.32, 0.32, fill=t["white"] if emph else t["primary"], shape=MSO_SHAPE.OVAL)
        c.label_in(dot, col.get("id") or str(i + 1), size=S["label"], bold=True, color=t["primary"] if emph else t["white"])
        c.text(cx + 0.62, y + 0.2, cw - 0.8, hdr_h - 0.3, col["header"], size=S["header"] + 1, bold=True,
               color=t["white"] if emph else t["title"], line_spacing=1.0)
        paras = [[("–  ", {"color": t["muted"]}), (d, {})] for d in col.get("detail", [])]
        if paras:
            bh = h - hdr_h - _reserve(slide, col) - 0.3
            c.text(cx + 0.19, y + hdr_h + 0.2, cw - 0.38, bh, paras, size=common, line_spacing=1.15)
        _box_bottom(c, spec, slide, col, cx + 0.19, y + h, cw - 0.38, emph)


def ghost(c, spec, slide, box):
    """Storyline-only slide: the real exhibit skeleton with '?' values + takeaway and data needed (A-12)."""
    x, y, w, h = box
    t = c.t
    body = slide.get("body")
    reqs = slide.get("data_requirements", [])
    cap_h = 0.5
    if body and body.get("kind") == "chart":
        chart(c, spec, slide, body, (x, y, w, h - cap_h))
    elif body and body.get("kind") in _ghost_kinds():
        b2 = (x, y, w, h - cap_h)
        fn = _ghost_kinds()[body["kind"]]
        fn(c, spec, body, b2) if body["kind"] in ("kpi", "table") else fn(c, spec, slide, body, b2)
    else:
        c.rect(x, y, w, h - cap_h, line=t["placeholder"], dash=True)
        c.text(x, y + (h - cap_h) / 2 - 0.2, w, 0.4, slide.get("archetype", ""), size=S["header"], color=t["placeholder"], align="c")
    exhibit = next((r.get("recommended_exhibit") for r in reqs if r.get("recommended_exhibit")), None)
    if exhibit:
        c.text(x, y + h - cap_h + 0.12, w, 0.3, [[("Exhibit: ", {"bold": True, "color": t["muted"]}), (exhibit, {"color": t["muted"]})]], size=S["label"])
    # sidebar: takeaway to prove + data needed
    m = G["margin"]
    sw = G["sidebar_w"]
    sx = G["slide_w"] - m - sw
    sy, sh = G["content_top"], G["content_bottom"] - G["content_top"]
    c.rect(sx, sy, sw, sh, fill=t["sidebar"])
    pad = 0.28
    cy = sy + 0.24
    c.text(sx + pad, cy, sw - 2 * pad, 0.22, "TAKEAWAY TO PROVE", size=S["small"], bold=True, color=t["muted"])
    take = slide.get("so_what") or (slide.get("lead_message") or {}).get("text", "")
    c.text(sx + pad, cy + 0.27, sw - 2 * pad, 1.0, take, size=S["takeaway"], bold=True, font=t["font_title"], color=t["title"], line_spacing=1.0)
    cy += 1.45
    c.line(sx + pad, cy, sx + sw - pad, cy, color=t["rule"])
    cy += 0.17
    c.text(sx + pad, cy, sw - 2 * pad, 0.22, "DATA NEEDED", size=S["small"], bold=True, color=t["caution_ink"])
    cy += 0.32
    step = (sy + sh - 0.2 - cy) / max(1, len(reqs))
    for r in reqs:
        c.rect(sx + pad, cy + 0.08, 0.09, 0.09, fill=t["caution"], shape=MSO_SHAPE.OVAL)
        paras = [[(r["description"], {"bold": True, "color": t["title"]})]]
        if r.get("candidate_sources"):
            paras.append([("Look in: " + "; ".join(r["candidate_sources"]), {"color": t["muted"], "size": S["label"]})])
        c.text(sx + pad + 0.2, cy, sw - 2 * pad - 0.2, step - 0.1, paras, size=S["body"] - 1, line_spacing=1.1)
        cy += step


def not_yet(c, slide, box):
    x, y, w, h = box
    c.rect(x, y, w, h, line=c.t["placeholder"], dash=True)
    c.text(x, y + h / 2 - 0.2, w, 0.4, f"{slide.get('archetype')} body: renderer v0 does not draw this kind yet",
           size=S["label"], color=c.t["placeholder"], align="c")


def _ghost_kinds():
    return {"kpi": kpi, "table": table, "text": text_body, "matrix": matrix, "panels": panels, "framework": framework,
            "process": process, "timeline": timeline, "tree": tree, "levers": levers, "case": case}


def content(c, spec, slide, page_no):
    box = body_box(slide)
    body = slide.get("body")
    warn = None
    kinds = {"chart": lambda: chart(c, spec, slide, body, box),
             "kpi": lambda: kpi(c, spec, body, box),
             "matrix": lambda: matrix(c, spec, slide, body, box),
             "table": lambda: table(c, spec, body, box, slide),
             "text": lambda: text_body(c, spec, slide, body, box),
             "panels": lambda: panels(c, spec, slide, body, box),
             "framework": lambda: framework(c, spec, slide, body, box),
             "process": lambda: process(c, spec, slide, body, box),
             "timeline": lambda: timeline(c, spec, slide, body, box),
             "tree": lambda: tree(c, spec, slide, body, box),
             "levers": lambda: levers(c, spec, slide, body, box),
             "case": lambda: case(c, spec, slide, body, box),
             "equation": lambda: equation_body(c, spec, body, box)}
    if slide.get("status") == "ghost":
        ghost(c, spec, slide, box)
    elif not body:
        warn = f"slide {slide['id']}: no body"
    elif body["kind"] in kinds:
        kinds[body["kind"]]()
    else:
        not_yet(c, slide, box)
        warn = f"slide {slide['id']}: body kind '{body['kind']}' not drawn yet"
    if slide.get("callout") and (body or {}).get("kind") not in ("text", "framework", "process", "table", "levers"):
        warn = f"slide {slide['id']}: callout is not drawn for body kind '{(body or {}).get('kind')}'"
    if slide.get("basis") and slide.get("status") != "ghost":
        bx, by, bw, bh = box
        basis_strip(c, spec, slide["basis"], (bx, by + bh + G["gap"], bw, BASIS_H))
    if slide.get("status") != "ghost" and (body or {}).get("kind") != "matrix":
        sidebar(c, spec, slide)
    so_what_bar(c, slide)
    chrome(c, spec, slide, page_no)
    return warn


# ---------------------------------------------------------------- nav slides

def cover(c, spec, slide, page_no):
    t = c.t
    m = G["margin"]
    meta = spec.meta
    c.rect(0, 0, 0.18, G["slide_h"], fill=t["primary"])
    c.text(m + 0.4, 2.3, 10, 1.6, meta.get("title", ""), size=S["cover_title"], bold=True, font=t["font_title"], color=t["title"], anchor="b")
    c.text(m + 0.4, 4.05, 10, 0.4, meta.get("subtitle", ""), size=S["header"] + 2, color=t["muted"])
    lines = [x for x in [meta.get("company_name"), meta.get("audience"), meta.get("date")] if x]
    c.text(m + 0.4, 4.6, 10, 0.9, lines, size=S["body"], color=t["text"])
    if meta.get("confidentiality"):
        c.text(m + 0.4, G["source_top"], 10, G["line_h"], meta["confidentiality"], size=S["source"], color=t["muted"])


def exec_summary(c, spec, slide, page_no, pages=None):
    t = c.t
    m = G["margin"]
    W = G["slide_w"] - 2 * m
    c.text(m, G["title_top"], G["title_w"], G["title_h"], "Executive summary", size=S["title"], bold=True, font=t["font_title"], color=t["title"])
    y = 108 / 96
    gt = spec.raw.get("storyline", {}).get("governing_thought")
    if gt:
        gsize = S["header"] + 2
        while gsize > 13 and _est_h(gt, W - 0.5, gsize, 1.0, bold=True, title=True) > 0.95:
            gsize -= 0.5
        gh = _est_h(gt, W - 0.5, gsize, 1.0, bold=True, title=True) + 0.2
        box = c.rect(m, y, W, gh, fill=t["primary"])
        box.text_frame.margin_left = Inches(0.23)
        box.text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
        c.label_in(box, gt, size=gsize, bold=True, color=t["white"], align="l", font=t["font_title"])
        y += gh + 0.22
    n = max(1, len(spec.exec))
    row = (G["content_bottom"] - y) / n
    tw = W - 0.58 - 1.2
    def need(item, f):  # height of one exec item at scale f, measured with real fonts
        hs, bs = round((S["header"] + 2) * f * 2) / 2, round(S["body"] * f * 2) / 2
        h = _est_h(item["text"], tw, hs, 1.15, bold=True)
        h += sum(_est_h(sp["text"], tw - 0.2, bs, 1.15) for sp in item.get("sub_points", []))
        return h + 0.2  # gap to the rule
    avail = G["content_bottom"] - y
    f = 1.3  # grow the text to fill the page; shrink only when it does not fit
    while f > 0.72 and sum(need(it, f) for it in spec.exec) > avail:
        f -= 0.02
    needs = [need(it, f) for it in spec.exec]
    rows = [nd * avail / sum(needs) for nd in needs]  # rows share the page in proportion to their text
    for i, item in enumerate(spec.exec):
        row = rows[i]
        c.text(m, y - 0.05, 0.55, 0.55, item["id"], size=30, bold=True, color=t["highlight"], font=t["font_title"])
        paras = [[(item["text"], {"bold": True, "color": t["title"], "size": round((S["header"] + 2) * f * 2) / 2})]]
        for sp in item.get("sub_points", []):
            paras.append([("–  ", {"color": t["muted"]}), (sp["text"], {"color": t["text"]})])
        c.text(m + 0.58, y, tw, row - 0.15, paras, size=round(S["body"] * f * 2) / 2, line_spacing=1.15)
        refs = [pages[s] for s in item.get("supports", []) if pages and s in pages]
        if refs:
            c.text(G["slide_w"] - m - 1.1, y + 0.04, 1.1, 0.3, "p. " + ", ".join(str(p) for p in refs), size=S["label"], color=t["muted"], align="r")
        if i < n - 1:
            c.line(m, y + row - 0.12, G["slide_w"] - m, y + row - 0.12, color=t["rule"])
        y += row
    c.text(G["slide_w"] - m - 0.5, G["source_top"], 0.5, G["line_h"], str(page_no), size=S["source"], color=t["muted"], align="r")


def end_page(c, spec, slide, page_no):
    """Next steps. Key takeaways only when the spec gives ones the exec summary does not already say (B-05)."""
    t = c.t
    m = G["margin"]
    W = G["slide_w"] - 2 * m
    story = spec.raw.get("storyline", {})
    steps = story.get("next_steps", [])
    takeaways = story.get("key_takeaways", [])
    title = "Key takeaways and next steps" if takeaways and steps else ("Key takeaways" if takeaways else "Next steps")
    c.text(m, G["title_top"], G["title_w"], G["title_h"], title, size=S["title"], bold=True, font=t["font_title"], color=t["title"])
    y0 = G["content_top"] - 0.25
    lw = W * 0.45 if takeaways and steps else (W if takeaways else 0)
    if takeaways:
        c.text(m, y0, lw, 0.3, "Key takeaways", size=S["header"] + 1, bold=True, color=t["title"])
        c.line(m, y0 + 0.38, m + lw, y0 + 0.38, color=t["primary"], weight=1.5)
        _bullets(c, takeaways, m, y0 + 0.55, lw, G["content_bottom"] - y0 - 0.55,
                 size=fit_size(takeaways, lw, G["content_bottom"] - y0 - 0.55, S["body"] + 2, line_spacing=1.15))
    if steps:
        px = m + lw + (0.4 if lw else 0)
        pw = W - (px - m)
        # a table: action | owner | timing
        cols = [pw * 0.62, pw * 0.2, pw * 0.18]
        heads = ["Action", "Owner", "Timing"]
        hx = px
        for hd, cw in zip(heads, cols):
            c.text(hx + (0.6 if hd == "Action" else 0), y0, cw, 0.3, hd, size=S["header"], bold=True, color=t["muted"])
            hx += cw
        c.line(px, y0 + 0.38, px + pw, y0 + 0.38, color=t["primary"], weight=1.5)
        top = y0 + 0.5
        rh = min(1.0, (G["content_bottom"] - top) / len(steps))
        for i, st in enumerate(steps):
            yy = top + i * rh
            _badge(c, px, yy + rh / 2 - 0.16, str(i + 1), d=0.32)
            c.text(px + 0.6, yy, cols[0] - 0.8, rh, st["action"], size=S["body"] + 1, bold=True, color=t["title"], anchor="m")
            c.text(px + cols[0], yy, cols[1] - 0.15, rh, st.get("owner", ""), size=S["body"], color=t["text"], anchor="m")
            c.text(px + cols[0] + cols[1], yy, cols[2], rh, st.get("timing", ""), size=S["body"], color=t["text"], anchor="m")
            c.line(px, yy + rh, px + pw, yy + rh, color=t["rule"])
    c.text(G["slide_w"] - m - 0.5, G["source_top"], 0.5, G["line_h"], str(page_no), size=S["source"], color=t["muted"], align="r")


def so_what_bar(c, slide):
    if not slide.get("so_what") or slide.get("status") == "ghost":
        return
    t = c.t
    m = G["margin"]
    y = G["content_bottom"] - G["sowhat_h"]
    if slide.get("footnotes"):
        y -= G["line_h"] * len(slide["footnotes"])
    if slide.get("so_what_style") == "line":
        # no label: public decks never print "So what"; a bold sentence under a rule, accent bar on the left
        c.line(m, y + 0.02, G["slide_w"] - m, y + 0.02, color=t["rule"], weight=0.75)
        c.rect(m, y + 0.12, 0.06, G["sowhat_h"] - 0.16, fill=t["highlight"])
        c.text(m + 0.22, y + 0.12, G["slide_w"] - 2 * m - 0.22, G["sowhat_h"] - 0.16, slide["so_what"], size=S["sowhat"] + 2,
               bold=True, color=t["title"], font=t["font_title"], anchor="m")
        return
    bar = c.rect(m, y, G["slide_w"] - 2 * m, G["sowhat_h"], fill=t["primary"])
    tf = bar.text_frame
    tf.margin_left = Inches(0.23)
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    c.label_in(bar, slide["so_what"], size=S["sowhat"], bold=True, color=t["white"], align="l", font=t["font_title"])


def _bench_line(c, spec, ch, bench, box, values, unit, value_format):
    """Benchmark as a dashed horizontal line across a column or line chart (not as an extra category)."""
    x, y, w, h = box
    t = c.t
    bv = spec.value(bench["point"])
    if bv is None:
        return
    top = max(values + [bv]) * 1.18
    va = ch.value_axis
    va.minimum_scale = 0
    va.maximum_scale = top
    # fix the inner plot area so the line can be placed exactly
    lx, ly, lw, lh = 0.03, 0.10, 0.94, 0.78
    plotArea = ch._chartSpace.find(qn("c:chart")).find(qn("c:plotArea"))
    layout = plotArea.find(qn("c:layout"))
    if layout is None:
        layout = etree.SubElement(plotArea, qn("c:layout"))
        plotArea.remove(layout)
        plotArea.insert(0, layout)
    for old in list(layout):
        layout.remove(old)
    ml = etree.SubElement(layout, qn("c:manualLayout"))
    for tag, val in (("c:layoutTarget", "inner"), ("c:xMode", "edge"), ("c:yMode", "edge"),
                     ("c:x", lx), ("c:y", ly), ("c:w", lw), ("c:h", lh)):
        etree.SubElement(ml, qn(tag), val=str(val))
    yy = y + h * (ly + lh * (1 - bv / top))
    c.line(x + w * lx, yy, x + w * (lx + lw), yy, color=t["gray_dark"], weight=1.25, dash=True)
    c.text(x + w * lx, yy - 0.3, 3.4, 0.26,
           [[(bench["label"] + "  ", {"color": t["gray_dark"]}), (fmt(bv, (spec.dpoint(bench["point"]) or {}).get("unit"), value_format), {"bold": True, "color": t["gray_dark"]})]],
           size=S["label"], align="l")


def _stand_ins(n, kind):
    """Skeleton heights when no value is known yet (ghost or fully drafted chart)."""
    if kind == "waterfall":
        steps = [0.30, 0.15, 0.10, 0.08, 0.06, 0.05][: max(0, n - 2)]
        return [1.0] + steps + [1.0 + sum(steps)]
    return [1.0 - 0.12 * i for i in range(n)]


FONTS = {"body": "Arial", "title": "Georgia"}  # set per deck in render()


def _md_runs(text, size, bold=False, title=False):
    """'**Lead:** rest' -> styled runs for measurement."""
    fam = FONTS["title" if title else "body"]
    parts = str(text).split("**")
    return [(pt, fam, size, bold or k % 2 == 1) for k, pt in enumerate(parts) if pt] or [("", fam, size, bold)]


def _est_h(text, w, size, line_spacing=1.15, bold=False, title=False):
    """Height in inches of a paragraph, measured with the deck's real fonts (renderer/measure.py)."""
    return sum(measure.para_height(_md_runs(part, size, bold, title), w, line_spacing)
               for part in str(text).split("\n")) + 0.02


def fit_size(texts, w, h, size, min_size=11, indent=0.2, line_spacing=1.15, para_gap=0.0, bold=False, title=False):
    """Largest font size (pt, step 0.5) at which the paragraphs fit in w x h inches, measured with real fonts."""
    while size > min_size:
        need = sum(_est_h(tx, w - indent, size, line_spacing, bold, title) for tx in texts) + para_gap * len(texts)
        if need <= h:
            return size
        size -= 0.5
    return min_size


def tint(hex_, f=0.88):
    """Mix a color with white (f = share of white)."""
    h = hex_.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return "#%02X%02X%02X" % tuple(round(v + (255 - v) * f) for v in (r, g, b))


def _is_target(slide, item):
    co = (slide or {}).get("callout")
    return bool(co) and co["target"] in [str(item.get(k)) for k in ("header", "label", "id", "code") if item.get(k)]


def _reserve(slide, item):
    """Height kept free at the bottom of a box for its point line, footer and callout."""
    return (0.62 if item.get("point") else 0) + (0.5 if item.get("footer") else 0) + (1.0 if _is_target(slide, item) else 0)


def _callout_box(c, x, y, w, h, co):
    t = c.t
    c.rect(x, y, w, h, fill=tint(t["highlight"]))
    c.rect(x, y, 0.05, h, fill=t["highlight"])
    texts = [co["header"]] + ([co["detail"]] if co.get("detail") else [])
    size = fit_size(texts, w - 0.3, h - 0.2, S["body"], min_size=10, indent=0, line_spacing=1.05)
    paras = [[(co["header"], {"bold": True, "color": t["highlight"] if not t["dark_sidebar"] else t["title"]})]]
    if co.get("detail"):
        paras.append([(co["detail"], {"color": t["text"], "size": max(10, size - 1.5)})])
    c.text(x + 0.18, y + 0.1, w - 0.28, h - 0.15, paras, size=size, line_spacing=1.05)


def _box_bottom(c, spec, slide, item, x, bottom, w, emph=False):
    """Draw, from the bottom up: point line, footer, callout. Returns nothing."""
    t = c.t
    y = bottom
    if item.get("point"):
        y -= 0.62
        _point_line(c, spec, item, x, y, w, emph)
    if item.get("footer"):
        y -= 0.5
        c.line(x, y + 0.04, x + w, y + 0.04, color=t["rule"])
        c.text(x, y + 0.14, w, 0.32, item["footer"], size=S["label"] + 1, bold=True, color=t["highlight"] if emph else t["title"])
    if _is_target(slide, item):
        y -= 1.0
        _callout_box(c, x, y + 0.06, w, 0.88, slide["callout"])


def _bullets(c, items, x, y, w, h, size=None, color=None, fixed=False):
    t = c.t
    paras = [[("–  ", {"color": t["muted"]}), (d, {"color": color or t["text"]})] for d in items]
    if paras:
        sz = size if fixed else fit_size(items, w, h, size or S["body"])
        c.text(x, y, w, h, paras, size=sz, line_spacing=1.15)


def _point_line(c, spec, item, x, y, w, emph=False):
    """Bottom line of a box: caption left, number right (A-12)."""
    t = c.t
    c.line(x, y, x + w, y, color=t["rule"])
    c.text(x, y + 0.17, w * 0.62, 0.3, item.get("point_caption", ""), size=S["label"], color=t["muted"])
    ph = item["point"].get("placeholder")
    c.text(x + w * 0.4, y + 0.05, w * 0.6, 0.5, dp_fmt(spec, item["point"]), size=22, bold=True, font=t["font_title"],
           color=t["placeholder"] if ph else (t["highlight"] if emph else t["title"]), align="r")


def _badge(c, x, y, label, dark=True, d=0.32):
    t = c.t
    w = d if len(label) <= 1 else d + 0.12 * (len(label) - 1)
    dot = c.rect(x, y, w, d, fill=t["primary"] if dark else t["white"],
                 shape=MSO_SHAPE.OVAL if len(label) <= 1 else MSO_SHAPE.ROUNDED_RECTANGLE, radius=d / 2 if len(label) > 1 else None)
    tf = dot.text_frame
    tf.margin_left = tf.margin_right = Inches(0.02)
    c.label_in(dot, label, size=S["label"] - (1 if len(label) > 2 else 0), bold=True, color=t["white"] if dark else t["primary"])
    tf.word_wrap = False


def panels(c, spec, slide, body, box):
    x, y, w, h = box
    t = c.t
    ps = body["panels"]
    n = len(ps)
    gap = 0.42
    pw = (w - gap * (n - 1)) / n
    for i, p in enumerate(ps):
        px = x + i * (pw + gap)
        c.text(px, y, pw - (0.9 if p.get("delta") else 0), 0.62, p["header"], size=S["header"] + 1, bold=True, color=t["title"], line_spacing=1.0)
        if p.get("delta"):
            pill = c.rect(px + pw - 0.85, y + 0.04, 0.85, 0.32, fill=t["highlight"] if spec.dpoint(p["delta"]) else None,
                          line=None if spec.dpoint(p["delta"]) else t["placeholder"], dash=not spec.dpoint(p["delta"]), radius=0.16)
            d_unit = (spec.dpoint(p["delta"]) or {}).get("unit")
            c.label_in(pill, dp_fmt(spec, p["delta"], signed=d_unit != "x"), size=S["label"], bold=True, color=t["white"] if spec.dpoint(p["delta"]) else t["placeholder"])
        cy = y + 0.72
        if p.get("unit_line"):
            c.text(px, cy, pw, 0.26, unit_runs(p["unit_line"], t), size=S["label"])
            cy += 0.32
        c.line(px, cy, px + pw, cy, color=t["rule"])
        inner = (px, cy + 0.1, pw, y + h - cy - 0.1)
        b = p["body"]
        if b["kind"] == "chart":
            chart(c, spec, slide, b, inner)
        else:
            kpi(c, spec, b, inner)
        if i < n - 1 and body.get("connector") == "arrow":  # B-09: parallel evidence gets no arrow
            c.rect(px + pw + gap / 2 - 0.09, y + h / 2, 0.18, 0.3, fill=t["gray_light"], shape=MSO_SHAPE.CHEVRON)


def framework(c, spec, slide, body, box):
    x, y, w, h = box
    t = c.t
    items = body["items"]
    shape = body.get("shape", "pillars")
    top = y
    bottom = y + h
    if body.get("roof"):
        roof = c.rect(x, top, w, 0.55, fill=t["primary"], shape=MSO_SHAPE.TRAPEZOID if shape == "house" else None)
        c.label_in(roof, body["roof"], size=S["header"] + 1, bold=True, color=t["white"], font=t["font_title"])
        top += 0.55 + 0.16
    if body.get("foundation"):
        fnd = c.rect(x, bottom - 0.5, w, 0.5, fill=t["panel"])
        c.label_in(fnd, body["foundation"], size=S["body"], bold=True, color=t["title"])
        bottom -= 0.5 + 0.16
    n = len(items)
    if shape == "tiles" and n > 3:
        cols = 3 if n > 4 else 2
        rows = -(-n // cols)
    else:
        cols, rows = n, 1
    gap = G["gap"]
    cw = (w - gap * (cols - 1)) / cols
    rh = (bottom - top - gap * (rows - 1)) / rows
    hdr_h = min(0.95, rh * 0.38)
    common = min(fit_size(it.get("detail", []), cw - 0.34, rh - hdr_h - _reserve(slide, it) - 0.2, S["body"])
                 for it in items)
    for i, it in enumerate(items):
        r, k = divmod(i, cols)
        bx, by = x + k * (cw + gap), top + r * (rh + gap)
        emph = it.get("emphasis")
        target = _is_target(slide, it)
        c.rect(bx, by, cw, rh, fill=t["white"])
        c.rect(bx, by, cw, hdr_h, fill=t["primary"] if emph else t["panel"])
        c.rect(bx, by, cw, rh, fill=None, line=t["highlight"] if target else t["rule"], weight=2 if target else 0.75)
        _badge(c, bx + 0.17, by + 0.17, it.get("id") or str(i + 1), dark=not emph)
        c.text(bx + 0.6, by + 0.17, cw - 0.75, hdr_h - 0.22, it["header"], size=S["header"], bold=True,
               color=t["white"] if emph else t["title"], line_spacing=1.0)
        _bullets(c, it.get("detail", []), bx + 0.17, by + hdr_h + 0.16, cw - 0.34, rh - hdr_h - _reserve(slide, it) - 0.2, size=common, fixed=True)
        _box_bottom(c, spec, slide, it, bx + 0.17, by + rh - 0.08, cw - 0.34, emph)


def process(c, spec, slide, body, box):
    x, y, w, h = box
    t = c.t
    steps = body["steps"]
    n = len(steps)
    if body.get("from_to"):
        # each step = one dimension: header, detail[0] = from, detail[1] = to
        lw = w * 0.24
        cw = (w - lw - 0.5) / 2
        c.text(x + lw, y, cw, 0.35, "From", size=S["header"] + 1, bold=True, color=t["muted"])
        c.text(x + lw + cw + 0.5, y, cw, 0.35, "To", size=S["header"] + 1, bold=True, color=t["highlight"])
        c.line(x, y + 0.42, x + w, y + 0.42, color=t["primary"], weight=1.5)
        rh = (h - 0.5) / n
        for i, s_ in enumerate(steps):
            ry = y + 0.5 + i * rh
            d = s_.get("detail", []) + ["", ""]
            c.text(x, ry, lw - 0.2, rh, s_["header"], size=S["header"], bold=True, color=t["title"], anchor="m")
            c.text(x + lw, ry, cw - 0.2, rh, d[0], size=S["body"], color=t["muted"], anchor="m")
            c.rect(x + lw + cw + 0.1, ry + rh / 2 - 0.14, 0.28, 0.28, fill=t["gray_light"], shape=MSO_SHAPE.RIGHT_ARROW)
            c.text(x + lw + cw + 0.5, ry, cw, rh, d[1], size=S["body"], bold=True, color=t["title"], anchor="m")
            if i < n - 1:
                c.line(x, ry + rh, x + w, ry + rh, color=t["rule"])
        return
    ch_h = 0.82
    overlap = 0.12
    cw = (w + overlap * (n - 1)) / n
    ramp = [t["other_bars"], t["gray_mid"], t["gray_dark"], t["primary"]]
    common = min(fit_size(s_.get("detail", []), cw - overlap - 0.25, h - ch_h - 0.55 - _reserve(slide, s_), S["body"])
                 for s_ in steps)
    for i, s_ in enumerate(steps):
        cx = x + i * (cw - overlap)
        emph = s_.get("emphasis")
        col = t["highlight"] if emph else ramp[min(len(ramp) - 1, int(i * len(ramp) / n))]
        shp = c.rect(cx, y, cw, ch_h, fill=col, shape=MSO_SHAPE.PENTAGON if i == 0 else MSO_SHAPE.CHEVRON)
        shp.text_frame.margin_left = Inches(0.28 if i else 0.15)
        c.label_in(shp, s_["header"], size=S["body"], bold=True,
                   color=t["title"] if (col in (t["other_bars"], t["gray_mid"]) and not emph) else t["white"])
        bx = cx + (0.15 if i else 0)
        bw = cw - overlap - 0.25
        top = y + ch_h + 0.22
        c.text(bx, top, bw, 0.25, f"STEP {i + 1}", size=S["small"] - 1, bold=True, color=t["highlight"] if emph else t["muted"])
        _bullets(c, s_.get("detail", []), bx, top + 0.3, bw, y + h - top - 0.3 - _reserve(slide, s_), size=common, fixed=True)
        _box_bottom(c, spec, slide, s_, bx, y + h, bw, emph)
        if i < n - 1:
            c.line(cx + cw - overlap + 0.02, top, cx + cw - overlap + 0.02, y + h, color=t["rule"])


def timeline(c, spec, slide, body, box):
    x, y, w, h = box
    t = c.t
    periods = body["periods"]
    rows = body["rows"]
    lw = 2.4
    gx = x + lw
    gw = w - lw
    pw = gw / len(periods)
    idx = {p: i for i, p in enumerate(periods)}
    head_h = 0.4
    ms = body.get("milestones", [])
    # milestone labels: estimate each label's span; a label that would collide moves to a second line
    placed, lanes = [], []
    for m_ in ms:
        if m_["at"] not in idx:
            continue
        mx = gx + (idx[m_["at"]] + 0.5) * pw
        lab_w = min(pw * 1.6, len(m_["label"]) * S["small"] * 0.5 / 72 + 0.1)
        right = mx + 0.14 + lab_w > x + w
        span = (mx - 0.14 - lab_w, mx + 0.14) if right else (mx - 0.14, mx + 0.14 + lab_w)
        lane = 0
        while any(l_ == lane and not (span[1] < a_ or span[0] > b_) for (a_, b_), l_ in zip(placed, lanes)):
            lane += 1
        placed.append(span); lanes.append(lane)
        m_["_layout"] = (mx, lab_w, right, lane)
    ms_h = (0.55 + 0.26 * max(lanes or [0])) if ms else 0
    for i, p in enumerate(periods):
        c.rect(gx + i * pw + 0.02, y, pw - 0.04, head_h, fill=t["panel"])
        c.text(gx + i * pw, y + 0.08, pw, 0.26, p, size=S["label"], bold=True, color=t["title"], align="c")
    if ms:
        my = y + head_h + 0.12
        c.line(gx, my + 0.12, gx + gw, my + 0.12, color=t["rule"])
        for m_ in ms:
            if "_layout" not in m_:
                continue
            mx, lw_, right, lane = m_.pop("_layout")
            c.rect(mx - 0.1, my + 0.02, 0.2, 0.2, fill=t["highlight"], shape=MSO_SHAPE.DIAMOND)
            ly = my - 0.02 + lane * 0.26
            if lane:
                c.line(mx, my + 0.22, mx, ly + 0.04, color=t["rule"])
            c.text(mx - 0.14 - lw_ if right else mx + 0.14, ly, lw_, 0.28, m_["label"], size=S["small"], bold=True,
                   color=t["title"], align="r" if right else "l", wrap=False)
    top = y + head_h + ms_h + 0.12
    rh = (y + h - top) / max(1, len(rows))
    for i in range(1, len(periods)):
        c.line(gx + i * pw, top, gx + i * pw, y + h, color=t["gray_light"], dash=True)
    for r, row in enumerate(rows):
        ry = top + r * rh
        c.text(x, ry, lw - 0.2, rh, row["label"], size=S["body"], bold=True, color=t["title"], anchor="m")
        for b in row["bars"]:
            if b["start"] not in idx or b["end"] not in idx:
                continue
            bx = gx + idx[b["start"]] * pw + 0.05
            bw = (idx[b["end"]] - idx[b["start"]] + 1) * pw - 0.1
            emph = b.get("emphasis")
            lsize = S["label"]
            nl = _lines(b.get("label", ""), bw, lsize, bold=emph) if b.get("label") else 1
            while nl > 1 and lsize > 10:  # shrink before a label spills out of its bar (F8)
                lsize -= 0.5
                nl = _lines(b["label"], bw, lsize, bold=emph)
            bh = min(max(0.42, nl * lsize * 1.2 / 72 + 0.12), rh * 0.85)
            bar = c.rect(bx, ry + (rh - bh) / 2, bw, bh, fill=t["highlight"] if emph else t["other_bars"], radius=0.04)
            if b.get("label"):
                c.label_in(bar, b["label"], size=lsize, bold=emph, color=t["white"] if emph else t["title"], align="l")
        c.line(x, ry + rh, x + w, ry + rh, color=t["rule"])


def _leaves(node):
    ch = node.get("children") or []
    return sum(_leaves(k) for k in ch) if ch else 1


def tree(c, spec, slide, body, box):
    x, y, w, h = box
    t = c.t
    root = body["root"]

    def depth(n):
        return 1 + max([depth(k) for k in n.get("children") or []] or [0])
    levels = depth(root)
    note_h = 0.35 if body.get("mece_note") else 0
    hh = h - note_h
    gapx = 0.55
    bw = (w - gapx * (levels - 1)) / levels
    total = _leaves(root)
    slot = hh / total
    def node_h(n, ls, vs):
        hh_ = _est_h(n["label"], bw - 0.24, ls, 1.0, bold=True)
        return hh_ + (_est_h("$00M", bw - 0.24, vs, 1.0, bold=True, title=True) if n.get("point") else 0) + 0.08
    def all_nodes(n):
        return [n] + [m for k in n.get("children") or [] for m in all_nodes(k)]
    lsize, vsize = S["body"], S["header"] + 2
    while max(node_h(n, lsize, vsize) for n in all_nodes(root)) > slot * 0.92 and lsize > 10:
        lsize -= 0.5; vsize -= 0.5  # shrink text before a node box gets too tall for its slot
    bh = min(0.95, max(slot * 0.8, max(node_h(n, lsize, vsize) for n in all_nodes(root))))

    def draw(node, lvl, y0):
        n_leaves = _leaves(node)
        cy = y0 + n_leaves * slot / 2
        bx = x + lvl * (bw + gapx)
        emph = node.get("emphasis")
        dark = lvl == 0 or emph
        fillc = t["highlight"] if emph else (t["primary"] if lvl == 0 else t["panel"])
        b = c.rect(bx, cy - bh / 2, bw, bh, fill=fillc)
        val = dp_fmt(spec, node["point"]) if node.get("point") else None
        tf = b.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = Inches(0.12)
        tf.margin_top = tf.margin_bottom = Inches(0.03)
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.LEFT
        r = p.add_run()
        r.text = node["label"]
        r.font.size = Pt(lsize)
        r.font.bold = True
        r.font.name = t["font_body"]
        r.font.color.rgb = rgb(t["white"] if dark else t["title"])
        if val:
            p2 = tf.add_paragraph()
            r2 = p2.add_run()
            r2.text = val
            r2.font.size = Pt(vsize)
            r2.font.bold = True
            r2.font.name = t["font_title"]
            ph = node["point"].get("placeholder")
            r2.font.color.rgb = rgb(t["placeholder"] if ph else (t["white"] if dark else t["highlight"]))
        kids = node.get("children") or []
        if kids:
            midx = bx + bw + gapx / 2
            c.line(bx + bw, cy, midx, cy, color=t["gray_mid"], weight=1)
            yk = y0
            ys = []
            for k in kids:
                ky = yk + _leaves(k) * slot / 2
                ys.append(ky)
                c.line(midx, ky, midx + gapx / 2, ky, color=t["gray_mid"], weight=1)
                draw(k, lvl + 1, yk)
                yk += _leaves(k) * slot
            c.line(midx, ys[0], midx, ys[-1], color=t["gray_mid"], weight=1)
            if node.get("operator") and len(ys) > 1:
                for a, b2 in zip(ys, ys[1:]):
                    op = c.rect(midx - 0.14, (a + b2) / 2 - 0.14, 0.28, 0.28, fill=t["white"], line=t["gray_mid"], shape=MSO_SHAPE.OVAL)
                    c.label_in(op, node["operator"], size=S["label"], bold=True, color=t["title"])
    draw(root, 0, y)
    if body.get("mece_note"):
        c.text(x, y + h - 0.28, w, 0.28, [[("MECE: ", {"bold": True, "color": t["muted"]}), (body["mece_note"], {"color": t["muted"]})]], size=S["label"])


def levers(c, spec, slide, body, box):
    x, y, w, h = box
    t = c.t
    items = body["items"]
    total = body.get("total")
    heads = body.get("headers")
    if heads:  # B-10: every column says what it holds
        c.text(x + 0.72, y, w * 0.56, 0.3, heads[0], size=S["header"], bold=True, color=t["muted"])
        c.text(x + w - 3.0, y, 3.0, 0.3, heads[1], size=S["header"], bold=True, color=t["muted"], align="r")
        c.line(x, y + 0.38, x + w, y + 0.38, color=t["primary"], weight=1.5)
        y += 0.46
        h -= 0.46
    n = len(items) + (1 if total else 0)
    rh = min(1.05 if any(it.get("metric") for it in items) else 0.95, h / n)
    vals = [spec.value(it.get("point")) for it in items]
    vmax = max([abs(v) for v in vals if v is not None] or [1])
    same_unit = len({(spec.dpoint(it.get("point")) or {}).get("unit") for it in items if it.get("point")}) <= 1
    tw = w * (0.5 if any(it.get("metric") for it in items) else 0.56)
    vx = x + 0.75 + tw
    barw = w - (vx - x) - 1.3
    for i, it in enumerate(items):
        ry = y + i * rh
        target = _is_target(slide, it)
        if target:
            c.rect(x - 0.08, ry + 0.02, w + 0.16, rh - 0.04, fill=tint(t["highlight"]))
            c.rect(x - 0.08, ry + 0.02, 0.05, rh - 0.04, fill=t["highlight"])
        _badge(c, x, ry + rh / 2 - 0.19, it["code"], d=0.38)
        if target:
            co = slide["callout"]
            c.text(x + 0.72, ry + 0.06, tw, rh - 0.1, [[(it["text"], {"color": t["title"]})],
                   [(co["header"] + (" · " + co["detail"] if co.get("detail") else ""), {"bold": True, "color": t["highlight"], "size": S["label"]})]],
                   size=S["body"] + 1, anchor="m")
        else:
            c.text(x + 0.72, ry, tw, rh, it["text"], size=S["body"] + 1, color=t["title"], anchor="m")
        v = vals[i]
        p = it.get("point")
        if p is not None:
            if not same_unit:
                pass  # different units: a bar would compare apples and oranges
            elif v is None:
                c.rect(vx, ry + rh / 2 - 0.14, barw * 0.5, 0.28, fill=None, line=t["placeholder"], dash=True)
            else:
                c.rect(vx, ry + rh / 2 - 0.14, max(0.05, barw * abs(v) / vmax), 0.28, fill=t["other_bars"])
            col = t["placeholder"] if v is None else t["title"]
            if it.get("metric"):
                mw = 2.6
                c.text(x + w - mw, ry + 0.06, mw, 0.42, dp_fmt(spec, p), size=S["header"] + 3, bold=True, font=t["font_title"], color=col, align="r")
                c.text(x + w - mw, ry + 0.5, mw, rh - 0.52, it["metric"], size=S["label"] + 1, color=t["muted"], align="r", line_spacing=1.0)
            else:
                c.text(x + w - 1.2, ry, 1.2, rh, dp_fmt(spec, p), size=S["header"] + 3, bold=True, font=t["font_title"],
                       color=col, anchor="m", align="r")
        c.line(x, ry + rh, x + w, ry + rh, color=t["rule"])
    if total:
        ry = y + len(items) * rh
        c.line(x, ry, x + w, ry, color=t["primary"], weight=1.5)
        c.text(x + 0.62, ry, tw, rh, "Total", size=S["body"] + 1, bold=True, color=t["title"], anchor="m")
        tv = spec.value(total)
        c.text(x + w - 1.6, ry, 1.6, rh, dp_fmt(spec, total), size=S["header"] + 8, bold=True, font=t["font_title"],
               color=t["placeholder"] if tv is None else t["highlight"], anchor="m", align="r")


def case(c, spec, slide, body, box):
    x, y, w, h = box
    t = c.t
    top = y
    if body.get("subject"):
        c.text(x, y, w, 0.3, [[("CASE  ", {"bold": True, "color": t["highlight"]}), (body["subject"], {"bold": True, "color": t["title"]})]], size=S["body"])
        top += 0.45
    hh = y + h - top
    gap = 0.35
    iw = w * 0.32
    cw = (w - iw - 2 * gap) / 2
    labels = (body.get("situation_header") or "Situation", body.get("approach_header") or "Approach")
    for k, (lab, items) in enumerate(((labels[0], body.get("situation", [])), (labels[1], body.get("approach", [])))):
        cx = x + k * (cw + gap)
        c.text(cx, top, cw, 0.32, lab, size=S["header"] + 1, bold=True, color=t["title"])
        c.line(cx, top + 0.4, cx + cw, top + 0.4, color=t["primary"], weight=1.5)
        _bullets(c, items, cx, top + 0.55, cw, hh - 0.6, size=fit_size(items, cw, hh - 0.6, S["body"] + 2, line_spacing=1.15))
        if k == 1 or body.get("connector") == "all":  # B-09: situation -> approach is not cause and effect
            c.rect(cx + cw + gap / 2 - 0.09, top + hh / 2, 0.18, 0.3, fill=t["gray_light"], shape=MSO_SHAPE.CHEVRON)
    ix = x + 2 * (cw + gap)
    c.rect(ix, top, iw, hh, fill=t["primary"])
    c.text(ix + 0.3, top + 0.22, iw - 0.6, 0.32, "Impact", size=S["header"] + 1, bold=True, color=t["white"])
    imp = body.get("impact", [])
    step = (hh - 0.75) / max(1, len(imp))
    for i, it in enumerate(imp):
        iy = top + 0.7 + i * step
        ph = it["point"].get("placeholder")
        big = 40 if step > 1.45 else 32
        nh = big / 72 * 1.25
        c.text(ix + 0.3, iy, iw - 0.6, nh, dp_fmt(spec, it["point"]), size=big, bold=True, font=t["font_title"],
               color=t["placeholder"] if ph else t["white"])
        c.text(ix + 0.3, iy + nh, iw - 0.6, step - nh - 0.05, it["caption"],
               size=fit_size([it["caption"]], iw - 0.6, step - nh - 0.1, S["body"], min_size=10, indent=0), color=t["white"])


BASIS_H = 1.1
SIDEBAR_WARN = []


def equation_row(c, spec, terms, box, big=False):
    """Number cards joined by operators (B-08). The last term is the result."""
    x, y, w, h = box
    t = c.t
    n = len(terms)
    opw = 0.45 if big else 0.36
    cw = (w - opw * (n - 1)) / n
    for i, tm in enumerate(terms):
        cx = x + i * (cw + opw)
        last = i == n - 1
        if i:
            c.text(cx - opw, y, opw, h, tm.get("op") or "=", size=(30 if big else 20), bold=True,
                   color=t["muted"], align="c", anchor="m", font=t["font_title"])
        known = spec.dpoint(tm["point"]) is not None
        shp = c.rect(cx, y, cw, h, fill=t["primary"] if last else t["sidebar"], radius=0.05 if t["bar_radius"] else None)
        ink = t["white"] if last else t["sidebar_text"]
        pad = 0.16
        nh = 0.75 if big else 0.42
        label = dp_fmt(spec, tm["point"])
        nsize = 40 if big else 22
        while nsize > 12 and measure.width_pt(label, t["font_title"], nsize, True) > (cw - 2 * pad - 0.05) * 72:
            nsize -= 1  # never wrap a number
        c.text(cx + pad, y + (0.25 if big else 0.06), cw - 2 * pad, nh, label,
               size=round(nsize * 2) / 2, bold=True, font=t["font_title"],
               color=(t["placeholder"] if not known else (t["white"] if last else t["highlight"])))
        cap_y = y + (0.25 if big else 0.06) + nh + 0.04
        size = fit_size([tm["caption"]], cw - 2 * pad, y + h - cap_y - 0.1, S["body"] if big else S["label"] + 1,
                        min_size=9, indent=0, line_spacing=1.05)
        if _est_h(tm["caption"], cw - 2 * pad, size, 1.05) > y + h - cap_y - 0.04:
            SIDEBAR_WARN.append(f"equation card '{tm['caption'][:30]}' does not fit; shorten the caption")
        c.text(cx + pad, cap_y, cw - 2 * pad, y + h - cap_y - 0.06, tm["caption"], size=size, color=ink, line_spacing=1.05)


def basis_strip(c, spec, basis, box):
    x, y, w, h = box
    t = c.t
    lab_w = 1.25
    c.text(x, y, lab_w - 0.1, h, basis.get("header") or "How we estimated it", size=S["label"] + 1, bold=True,
           color=t["title"], anchor="m")
    equation_row(c, spec, basis["terms"], (x + lab_w, y, w - lab_w, h))


def equation_body(c, spec, body, box):
    x, y, w, h = box
    t = c.t
    eh = min(2.1, h * 0.5)
    equation_row(c, spec, body["terms"], (x, y, w, eh), big=True)
    ass = body.get("assumptions", [])
    if ass:
        ay = y + eh + 0.4
        c.text(x, ay, w, 0.32, body.get("assumptions_header") or "Assumptions", size=S["header"] + 1, bold=True, color=t["title"])
        c.line(x, ay + 0.4, x + w, ay + 0.4, color=t["primary"], weight=1.5)
        _bullets(c, ass, x, ay + 0.55, w, y + h - ay - 0.55,
                 size=fit_size(ass, w, y + h - ay - 0.55, S["body"] + 1, line_spacing=1.15))


# ---------------------------------------------------------------- entry

def measured_height(sh, body_font="Arial"):
    """Height in inches the text of a shape needs, measured with real font metrics (renderer/measure.py)."""
    tf = sh.text_frame
    w = sh.width / 914400 - ((tf.margin_left or 0) + (tf.margin_right or 0)) / 914400
    total = 0.0
    for para in tf.paragraphs:
        runs = [(r.text, r.font.name or body_font, r.font.size.pt if r.font.size else S["body"], bool(r.font.bold))
                for r in para.runs if r.text]
        if runs and runs[0][0].strip() in ("–", "▪", "•"):  # list marker sits in the hanging indent
            runs = runs[1:]
        if not runs or not "".join(r[0] for r in runs).strip():
            continue
        pPr = para._p.pPr
        indent = int(pPr.get("marL", "0")) / 914400 if pPr is not None else 0.0
        ls = para.line_spacing if isinstance(para.line_spacing, float) else 1.0
        total += measure.para_height(runs, max(0.1, w - indent), ls)
    return total + ((tf.margin_top or 0) + (tf.margin_bottom or 0)) / 914400


def layout_check(slide, page_no, body_font="Arial"):
    """F8: after drawing, flag text that does not fit its box (measured with real fonts), text that runs into
    another element, and shapes that leave the slide."""
    out = []
    W, H = G["slide_w"], G["slide_h"]
    boxes = []
    for sh in slide.shapes:
        x, y = sh.left / 914400, sh.top / 914400
        w, h = sh.width / 914400, sh.height / 914400
        if sh.rotation == 0 and (x < -0.01 or y < -0.01 or x + w > W + 0.01 or y + h > H + 0.01):
            out.append(f"p{page_no}: shape leaves the slide ({x:.2f}, {y:.2f}, {w:.2f} x {h:.2f} in)")
        if sh.shape_type == 19 or not sh.has_text_frame or not sh.text_frame.text.strip() or sh.rotation:
            continue
        tf = sh.text_frame
        if tf.word_wrap is False:
            continue
        need = measured_height(sh, body_font)
        anchor = tf.vertical_anchor
        if anchor == MSO_ANCHOR.MIDDLE:
            top, bot = y + (h - need) / 2, y + (h + need) / 2
        elif anchor == MSO_ANCHOR.BOTTOM:
            top, bot = y + h - need, y + h
        else:
            top, bot = y, y + need
        filled = sh.shape_type == 1 and sh.fill.type == 1
        boxes.append((x, y, w, h, top, bot, need, filled, tf.text.strip().replace("\n", " ")[:40]))
    for i, (x, y, w, h, top, bot, need, filled, label) in enumerate(boxes):
        if need <= h + 0.03:
            continue
        if filled:
            out.append(f"p{page_no}: text does not fit its shape ({need:.2f} in of text in {h:.2f} in): \"{label}\"")
            continue
        for j, (x2, y2, w2, h2, *_r) in enumerate(boxes):
            if j == i or min(x + w, x2 + w2) - max(x, x2) <= 0.05:
                continue
            if (y2 > y + 0.02 and bot > y2 + 0.02 and y2 >= y + h - 0.02) or (y2 + h2 < y + 0.02 and top < y2 + h2 - 0.02):
                out.append(f"p{page_no}: text runs into another element ({need:.2f} in of text in {h:.2f} in): \"{label}\"")
                break
    return out


def render(spec_dict, out_path, theme=None, font_pair=None):
    spec = Spec(spec_dict)
    tok = tokens.resolve(theme or spec.meta.get("theme"), font_pair or spec.meta.get("font_pair"))
    FONTS.update(body=tok["font_body"], title=tok["font_title"])
    prs = Presentation()
    prs.slide_width = Inches(G["slide_w"])
    prs.slide_height = Inches(G["slide_h"])
    blank = prs.slide_layouts[6]
    warnings = []
    pages = {sl["id"]: i for i, sl in enumerate(spec_dict["slides"], start=1)}
    for i, sl in enumerate(spec_dict["slides"], start=1):
        slide = prs.slides.add_slide(blank)
        c = Canvas(slide, tok)
        role = sl["role"]
        if role == "cover":
            cover(c, spec, sl, i)
        elif role == "exec_summary":
            exec_summary(c, spec, sl, i, pages)
        elif role == "end_page":
            end_page(c, spec, sl, i)
        elif role in ("content", "backup"):
            w = content(c, spec, sl, i)
            if w:
                warnings.append(w)
        else:
            warnings.append(f"slide {sl['id']}: role '{role}' not drawn yet")
        warnings += layout_check(slide, i, tok["font_body"]) + SIDEBAR_WARN
        SIDEBAR_WARN.clear()
    prs.save(out_path)
    return {"path": out_path, "slides": len(spec_dict["slides"]), "theme": tok["theme"], "font_pair": tok["font_pair"], "warnings": warnings}
