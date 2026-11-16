"""Tiny slide layout engine: one spec -> native PPTX + PIL preview PNGs with overflow checks."""
import re
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LABEL_POSITION, XL_TICK_LABEL_POSITION
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn
from PIL import Image, ImageDraw, ImageFont
from lxml import etree

W, H = 13.333, 7.5
INK = "0b0b0b"; INK2 = "52514e"; MUTED = "898781"; RULE = "d9d8d3"; GRID = "e1e0d9"
BLUE = "2a78d6"; ORANGE = "eb6834"; LBLUE = "cde2fb"; LGRAY = "f2f1ee"; MGRAY = "b9b8b2"
GOOD = "0ca30c"; CRIT = "d03b3b"; WARN = "fab219"; LRED = "f8d3d3"; GOODTXT = "006300"
FONT = "Arial"
FR = "/System/Library/Fonts/Supplemental/Arial.ttf"
FB = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
PX = 100  # preview pixels per inch
INSET = 0.06

_fcache = {}
def pilfont(pt, bold=False):
    k = (pt, bold)
    if k not in _fcache:
        _fcache[k] = ImageFont.truetype(FB if bold else FR, max(1, round(pt * PX / 72)))
    return _fcache[k]

def rgb(h):
    return RGBColor.from_string(h)

def parse_runs(s):
    """'a **b** c' -> [(a,False),(b,True),(c,False)]"""
    parts = s.split("**")
    return [(p, i % 2 == 1) for i, p in enumerate(parts) if p]

# ---------------- measurement ----------------
def wrap_runs(runs, width_in, pt, base_bold=False):
    """Greedy word wrap over mixed bold runs. returns number of lines."""
    words = []
    for text, b in runs:
        for tok in re.split(r"(\s+)", text):
            if tok:
                words.append((tok, b or base_bold))
    maxw = width_in * PX
    lines = 1; cur = 0.0
    for tok, b in words:
        w = pilfont(pt, b).getlength(tok)
        if tok.isspace():
            cur += w; continue
        if cur + w > maxw and cur > 0:
            lines += 1; cur = w
        else:
            cur += w
    return lines

def para_height(p, width_in, default_pt):
    pt = p.get("size", default_pt)
    ind = 0.2 if p.get("bullet") else 0
    n = wrap_runs(parse_runs(p["text"]), width_in - ind, pt, p.get("bold", False))
    return n * pt * 1.2 / 72 + p.get("space_before", 0) / 72, n

def text_height(paras, width_in, pt):
    total = 0
    for p in paras:
        h, _ = para_height(p, width_in - 2 * INSET, pt)
        total += h
    return total + 2 * INSET

# ---------------- PPTX writer ----------------
class Deck:
    def __init__(self):
        self.prs = Presentation()
        self.prs.slide_width = Inches(W); self.prs.slide_height = Inches(H)
        self.specs = []
        self.warnings = []

    def add(self, elements, name):
        self.specs.append((name, elements))

    def build(self, path, preview_dir):
        for idx, (name, els) in enumerate(self.specs, 1):
            s = self.prs.slides.add_slide(self.prs.slide_layouts[6])
            img = Image.new("RGB", (int(W * PX), int(H * PX)), "white")
            d = ImageDraw.Draw(img)
            for e in els:
                getattr(self, "_" + e["t"])(s, e)
                getattr(self, "_pv_" + e["t"])(d, e)
                self._check(e, name)
            if "notes" in dict(els[0]) if False else False:
                pass
            img.save(f"{preview_dir}/slide_{idx:02d}.png")
        self.prs.save(path)

    # --- checks
    def _check(self, e, name):
        if e["t"] == "text" and not e.get("nocheck"):
            need = text_height(e["paras"], e["w"], e.get("size", 12))
            if need > e["h"] + 0.02:
                self.warnings.append(f"[{name}] text overflow '{e['paras'][0]['text'][:40]}' need {need:.2f} > {e['h']:.2f}")
        for k in ("x", "y"):
            pass
        if e.get("x", 0) + e.get("w", 0) > W + 0.01 or e.get("y", 0) + e.get("h", 0) > H + 0.01:
            self.warnings.append(f"[{name}] element off-slide {e['t']}")
        if e["t"] == "table":
            tot = sum(e["_rowh"])
            if e["y"] + tot > e.get("maxy", 6.85):
                self.warnings.append(f"[{name}] table too tall: bottom {e['y']+tot:.2f}")

    # --- text
    def _text(self, s, e):
        tb = s.shapes.add_textbox(Inches(e["x"]), Inches(e["y"]), Inches(e["w"]), Inches(e["h"]))
        if e.get("fill"):
            tb.fill.solid(); tb.fill.fore_color.rgb = rgb(e["fill"])
        if e.get("line"):
            tb.line.color.rgb = rgb(e["line"]); tb.line.width = Pt(e.get("lw", 0.75))
        tf = tb.text_frame; tf.word_wrap = True
        tf.auto_size = None
        for m in ("margin_left", "margin_right", "margin_top", "margin_bottom"):
            setattr(tf, m, Inches(INSET))
        tf.vertical_anchor = {"top": MSO_ANCHOR.TOP, "middle": MSO_ANCHOR.MIDDLE, "bottom": MSO_ANCHOR.BOTTOM}[e.get("valign", "top")]
        for i, p in enumerate(e["paras"]):
            para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            para.alignment = {"l": PP_ALIGN.LEFT, "c": PP_ALIGN.CENTER, "r": PP_ALIGN.RIGHT}[p.get("align", e.get("align", "l"))]
            para.line_spacing = 1.0
            if p.get("space_before"):
                para.space_before = Pt(p["space_before"])
            if p.get("bullet"):
                pPr = para._p.get_or_add_pPr()
                pPr.set("marL", str(Inches(0.2))); pPr.set("indent", str(-Inches(0.2)))
                bu = etree.SubElement(pPr, qn("a:buFont")); bu.set("typeface", FONT)
                bc = etree.SubElement(pPr, qn("a:buChar")); bc.set("char", "•")
            for text, b in parse_runs(p["text"]):
                r = para.add_run(); r.text = text
                f = r.font; f.name = FONT; f.size = Pt(p.get("size", e.get("size", 12)))
                f.bold = b or p.get("bold", False) or e.get("bold", False)
                f.italic = p.get("italic", False)
                f.color.rgb = rgb(p.get("color", e.get("color", INK)))

    def _pv_text(self, d, e):
        x0, y0 = e["x"] * PX, e["y"] * PX
        if e.get("fill"):
            d.rectangle([x0, y0, x0 + e["w"] * PX, y0 + e["h"] * PX], fill="#" + e["fill"])
        if e.get("line"):
            d.rectangle([x0, y0, x0 + e["w"] * PX, y0 + e["h"] * PX], outline="#" + e["line"])
        width = e["w"] - 2 * INSET
        total = text_height(e["paras"], e["w"], e.get("size", 12)) - 2 * INSET
        va = e.get("valign", "top")
        y = y0 + INSET * PX
        if va == "middle": y = y0 + (e["h"] * PX - total * PX) / 2
        if va == "bottom": y = y0 + e["h"] * PX - total * PX - INSET * PX
        for p in e["paras"]:
            pt = p.get("size", e.get("size", 12))
            y += p.get("space_before", 0) / 72 * PX
            ind = 0.2 if p.get("bullet") else 0
            col = "#" + p.get("color", e.get("color", INK))
            # layout words
            words = []
            for text, b in parse_runs(p["text"]):
                for tok in re.split(r"(\s+)", text):
                    if tok: words.append((tok, b or p.get("bold", False) or e.get("bold", False)))
            maxw = (width - ind) * PX
            lines = [[]]; cur = 0
            for tok, b in words:
                w = pilfont(pt, b).getlength(tok)
                if not tok.isspace() and cur + w > maxw and cur > 0:
                    lines.append([]); cur = 0
                if tok.isspace() and cur == 0: continue
                lines[-1].append((tok, b, w)); cur += w
            lh = pt * 1.2 / 72 * PX
            for li, ln in enumerate(lines):
                lw = sum(w for _, _, w in ln)
                al = p.get("align", e.get("align", "l"))
                xs = x0 + INSET * PX + ind * PX
                if al == "c": xs = x0 + (e["w"] * PX - lw) / 2
                if al == "r": xs = x0 + e["w"] * PX - INSET * PX - lw
                if li == 0 and p.get("bullet"):
                    d.text((x0 + INSET * PX, y), "•", font=pilfont(pt), fill=col)
                for tok, b, w in ln:
                    d.text((xs, y), tok, font=pilfont(pt, b), fill=col); xs += w
                y += lh

    # --- rect / line
    def _rect(self, s, e):
        shp = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE if e.get("round") else MSO_SHAPE.RECTANGLE,
                                 Inches(e["x"]), Inches(e["y"]), Inches(e["w"]), Inches(e["h"]))
        if e.get("round"):
            shp.adjustments[0] = e["round"]
        if e.get("fill"):
            shp.fill.solid(); shp.fill.fore_color.rgb = rgb(e["fill"])
        else:
            shp.fill.background()
        if e.get("line"):
            shp.line.color.rgb = rgb(e["line"]); shp.line.width = Pt(e.get("lw", 0.75))
        else:
            shp.line.fill.background()
        shp.shadow.inherit = False

    def _pv_rect(self, d, e):
        d.rectangle([e["x"] * PX, e["y"] * PX, (e["x"] + e["w"]) * PX, (e["y"] + e["h"]) * PX],
                    fill=("#" + e["fill"]) if e.get("fill") else None,
                    outline=("#" + e["line"]) if e.get("line") else None)

    def _line(self, s, e):
        c = s.shapes.add_connector(1, Inches(e["x"]), Inches(e["y"]), Inches(e["x2"]), Inches(e["y2"]))
        c.line.color.rgb = rgb(e.get("color", RULE)); c.line.width = Pt(e.get("lw", 0.75))
        if e.get("dash"):
            ln = c.line._get_or_add_ln(); pd = etree.SubElement(ln, qn("a:prstDash")); pd.set("val", "dash")

    def _pv_line(self, d, e):
        d.line([e["x"] * PX, e["y"] * PX, e["x2"] * PX, e["y2"] * PX], fill="#" + e.get("color", RULE), width=2)

    # --- table
    def _rowheights(self, e):
        if "_rowh" in e: return e["_rowh"]
        hs = []
        for ri, row in enumerate(e["rows"]):
            mh = e.get("minh", 0.3)
            for ci, cell in enumerate(row):
                txt = cell if isinstance(cell, str) else cell["text"]
                pt = e.get("hsize", e["size"]) if ri == 0 else e["size"]
                bold = ri == 0 or (isinstance(cell, dict) and cell.get("bold"))
                paras = [{"text": t, "bold": bold, "size": pt} for t in txt.split("\n")]
                h = 0
                for p in paras:
                    ph, _ = para_height(p, e["cols"][ci] - 0.16, pt)
                    h += ph
                mh = max(mh, h + 0.1)
            hs.append(mh)
        e["_rowh"] = hs
        return hs

    def _table(self, s, e):
        hs = self._rowheights(e)
        nr, nc = len(e["rows"]), len(e["cols"])
        gs = s.shapes.add_table(nr, nc, Inches(e["x"]), Inches(e["y"]), Inches(sum(e["cols"])), Inches(sum(hs)))
        tbl = gs.table
        tblPr = tbl._tbl.tblPr
        # remove default style banding look
        tblPr.set("bandRow", "0"); tblPr.set("firstRow", "0")
        for ci, cw in enumerate(e["cols"]):
            tbl.columns[ci].width = Inches(cw)
        for ri, row in enumerate(e["rows"]):
            tbl.rows[ri].height = Inches(hs[ri])
            for ci, cell in enumerate(row):
                c = tbl.cell(ri, ci)
                spec = cell if isinstance(cell, dict) else {"text": cell}
                fill = spec.get("fill") or (e.get("hfill", INK) if ri == 0 else (e.get("zebra") if ri % 2 == 0 and e.get("zebra") else "ffffff"))
                c.fill.solid(); c.fill.fore_color.rgb = rgb(fill)
                c.margin_left = c.margin_right = Inches(0.08); c.margin_top = c.margin_bottom = Inches(0.04)
                c.vertical_anchor = MSO_ANCHOR.MIDDLE if e.get("vmid", True) else MSO_ANCHOR.TOP
                tf = c.text_frame; tf.word_wrap = True
                lines = spec["text"].split("\n")
                for li, ln in enumerate(lines):
                    para = tf.paragraphs[0] if li == 0 else tf.add_paragraph()
                    para.alignment = {"l": PP_ALIGN.LEFT, "c": PP_ALIGN.CENTER, "r": PP_ALIGN.RIGHT}[spec.get("align", e.get("aligns", ["l"] * nc)[ci])]
                    for text, b in parse_runs(ln):
                        r = para.add_run(); r.text = text
                        r.font.name = FONT
                        r.font.size = Pt(e.get("hsize", e["size"]) if ri == 0 else e["size"])
                        r.font.bold = b or ri == 0 or spec.get("bold", False)
                        r.font.color.rgb = rgb(spec.get("color", "ffffff" if ri == 0 and not e.get("hcolor") else (e.get("hcolor", INK) if ri == 0 else INK)))
                # borders: bottom hairline
                tcPr = c._tc.get_or_add_tcPr()
                for ti, tag in enumerate(("a:lnL", "a:lnR", "a:lnT", "a:lnB")):
                    ln = etree.Element(qn(tag)); tcPr.insert(ti, ln)
                    if tag == "a:lnB":
                        ln.set("w", str(Pt(0.75))); sf = etree.SubElement(ln, qn("a:solidFill"))
                        clr = etree.SubElement(sf, qn("a:srgbClr")); clr.set("val", RULE)
                    else:
                        ln.set("w", "0"); etree.SubElement(ln, qn("a:noFill"))

    def _pv_table(self, d, e):
        hs = self._rowheights(e)
        y = e["y"]
        for ri, row in enumerate(e["rows"]):
            x = e["x"]
            for ci, cell in enumerate(row):
                spec = cell if isinstance(cell, dict) else {"text": cell}
                fill = spec.get("fill") or (e.get("hfill", INK) if ri == 0 else (e.get("zebra") if ri % 2 == 0 and e.get("zebra") else "ffffff"))
                d.rectangle([x * PX, y * PX, (x + e["cols"][ci]) * PX, (y + hs[ri]) * PX], fill="#" + fill)
                d.line([x * PX, (y + hs[ri]) * PX, (x + e["cols"][ci]) * PX, (y + hs[ri]) * PX], fill="#" + RULE)
                pt = e.get("hsize", e["size"]) if ri == 0 else e["size"]
                col = spec.get("color", "ffffff" if ri == 0 and not e.get("hcolor") else (e.get("hcolor", INK) if ri == 0 else INK))
                paras = [{"text": t, "bold": ri == 0 or spec.get("bold", False), "size": pt, "color": col,
                          "align": spec.get("align", e.get("aligns", ["l"] * len(row))[ci])} for t in spec["text"].split("\n")]
                self._pv_text(d, {"x": x + 0.02, "y": y, "w": e["cols"][ci] - 0.04, "h": hs[ri], "paras": paras, "size": pt,
                                  "valign": "middle" if e.get("vmid", True) else "top"})
                x += e["cols"][ci]
            y += hs[ri]

    # --- charts
    def _chart(self, s, e):
        cd = CategoryChartData()
        cd.categories = e["cats"]
        for name, vals in e["series"]:
            cd.add_series(name, vals)
        kind = {"bar": XL_CHART_TYPE.BAR_CLUSTERED, "col": XL_CHART_TYPE.COLUMN_CLUSTERED,
                "stackcol": XL_CHART_TYPE.COLUMN_STACKED, "stackbar": XL_CHART_TYPE.BAR_STACKED}[e["kind"]]
        gf = s.shapes.add_chart(kind, Inches(e["x"]), Inches(e["y"]), Inches(e["w"]), Inches(e["h"]), cd)
        ch = gf.chart
        ch.has_legend = bool(e.get("legend"))
        if ch.has_legend:
            from pptx.enum.chart import XL_LEGEND_POSITION
            ch.legend.position = XL_LEGEND_POSITION.TOP; ch.legend.include_in_layout = False
            ch.legend.font.size = Pt(10); ch.legend.font.name = FONT; ch.legend.font.color.rgb = rgb(INK2)
        ch.font.name = FONT; ch.font.size = Pt(e.get("size", 11)); ch.font.color.rgb = rgb(INK2)
        plot = ch.plots[0]
        plot.gap_width = e.get("gap", 60)
        if e["kind"].startswith("stack"):
            plot.overlap = 100
        else:
            plot.overlap = e.get("overlap", -10)
        ca = ch.category_axis; va = ch.value_axis
        ca.format.line.color.rgb = rgb("c3c2b7"); ca.has_major_gridlines = False
        ca.tick_labels.font.size = Pt(e.get("catsize", e.get("size", 11))); ca.tick_labels.font.color.rgb = rgb(INK)
        from pptx.enum.chart import XL_TICK_MARK
        ca.major_tick_mark = XL_TICK_MARK.NONE
        if e["kind"] in ("bar", "stackbar"):
            ca.reverse_order = True
        if e.get("ticklow"):
            ca.tick_label_position = XL_TICK_LABEL_POSITION.LOW
        va.visible = e.get("vaxis", False)
        va.has_major_gridlines = False
        if "vmax" in e: va.maximum_scale = e["vmax"]
        if "vmin" in e: va.minimum_scale = e["vmin"]
        va.tick_labels.font.size = Pt(10)
        for si, ser in enumerate(plot.series):
            colors = e["colors"][si]
            ser.invert_if_negative = False
            for pi in range(len(e["cats"])):
                pt = ser.points[pi]
                c = colors[pi] if isinstance(colors, list) else colors
                if c is None:
                    pt.format.fill.background(); pt.format.line.fill.background()
                else:
                    pt.format.fill.solid(); pt.format.fill.fore_color.rgb = rgb(c)
                    pt.format.line.color.rgb = rgb("ffffff"); pt.format.line.width = Pt(1.5)
            labels = e.get("labels", [None] * len(e["series"]))[si]
            if labels:
                for pi, lab in enumerate(labels):
                    if lab is None: continue
                    dl = ser.points[pi].data_label
                    dl.has_text_frame = True
                    dl.text_frame.text = lab
                    r = dl.text_frame.paragraphs[0].runs[0]
                    r.font.size = Pt(e.get("lsize", 11)); r.font.bold = True; r.font.name = FONT
                    r.font.color.rgb = rgb(e.get("lcolor", [INK] * 9)[si] if isinstance(e.get("lcolor"), list) else e.get("lcolor", INK))
                    lp = e.get("lpos", XL_LABEL_POSITION.OUTSIDE_END)
                    dl.position = lp[si] if isinstance(lp, list) else lp

    def _pv_chart(self, d, e):
        x0, y0, w, h = e["x"] * PX, e["y"] * PX, e["w"] * PX, e["h"] * PX
        d.rectangle([x0, y0, x0 + w, y0 + h], outline="#eeeeee")
        n = len(e["cats"])
        horiz = e["kind"] in ("bar", "stackbar")
        stacked = e["kind"].startswith("stack")
        vmax = e.get("vmax") or max(sum(v for v in col if v) if stacked else max(v for v in col if v is not None)
                                   for col in zip(*[s[1] for s in e["series"]])) * 1.15
        vmin = e.get("vmin", 0)
        catw = 0.32 * w if horiz else 0
        f = pilfont(e.get("catsize", e.get("size", 11)))
        for i, cat in enumerate(e["cats"]):
            base = 0
            for si, (name, vals) in enumerate(e["series"]):
                v = vals[i] or 0
                c = e["colors"][si]; c = c[i] if isinstance(c, list) else c
                ns = 1 if stacked else len(e["series"])
                if horiz:
                    slot = (h / n); bh = slot * 0.6 / ns
                    by = y0 + i * slot + slot * 0.2 + (0 if stacked else si * bh)
                    bx = x0 + catw + (base - vmin) / (vmax - vmin) * (w - catw)
                    bw = v / (vmax - vmin) * (w - catw)
                    if c: d.rectangle([min(bx, bx + bw), by, max(bx, bx + bw), by + bh], fill="#" + c)
                    lab = (e.get("labels") or [[None] * n] * 9)[si][i] if e.get("labels") and e["labels"][si] else None
                    if lab: d.text((bx + bw + 4, by), lab, font=pilfont(e.get("lsize", 11), True), fill="#0b0b0b")
                else:
                    slot = (w / n); bw = slot * 0.6 / ns
                    bx = x0 + i * slot + slot * 0.2 + (0 if stacked else si * bw)
                    plot_h = h - 0.5 * PX
                    by = y0 + plot_h - (base + v - vmin) / (vmax - vmin) * plot_h
                    bh = v / (vmax - vmin) * plot_h
                    if c: d.rectangle([bx, by, bx + bw, by + bh], fill="#" + c)
                    lab = e["labels"][si][i] if e.get("labels") and e["labels"][si] else None
                    if lab: d.text((bx, by - 18), lab, font=pilfont(e.get("lsize", 11), True), fill="#0b0b0b")
                if stacked: base += v
            if horiz:
                d.text((x0 + 2, y0 + i * (h / n) + (h / n) * 0.3), cat[:40], font=f, fill="#0b0b0b")
            else:
                d.text((x0 + i * (w / n) + 4, y0 + h - 0.45 * PX), cat.replace("\n", " ")[:24], font=f, fill="#0b0b0b")
