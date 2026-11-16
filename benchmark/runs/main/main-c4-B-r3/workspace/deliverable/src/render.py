"""Approximate PNG preview of a pptx (layout QA only: text wrap, boxes, tables, simple bar charts)."""
import sys, os
from pptx import Presentation
from pptx.util import Emu
from pptx.enum.shapes import MSO_SHAPE_TYPE
from PIL import Image, ImageDraw, ImageFont
from pptx.oxml.ns import qn

DPI = 100
REG = "/System/Library/Fonts/Supplemental/Arial.ttf"
BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
_f = {}


def font(pt, bold):
    k = (pt, bold)
    if k not in _f:
        _f[k] = ImageFont.truetype(BOLD if bold else REG, max(6, int(round(pt * DPI / 72))))
    return _f[k]


def px(emu):
    return int(round(Emu(emu).inches * DPI))


def col(rgb):
    return "#" + str(rgb)


def wrap(draw, words_runs, width):
    """words_runs: list of (word, font, color). returns lines of list of (word, font, color)."""
    lines, cur, w = [], [], 0
    for word, f, c in words_runs:
        ww = draw.textlength(word + " ", font=f)
        if cur and w + draw.textlength(word, font=f) > width:
            lines.append(cur); cur, w = [], 0
        cur.append((word, f, c)); w += ww
    lines.append(cur)
    return lines


def draw_tf(draw, tf, x, y, w, h, default_pt=12):
    ml, mr, mt, mb = [px(v) if v is not None else 0 for v in (tf.margin_left, tf.margin_right, tf.margin_top, tf.margin_bottom)]
    blocks = []
    total = 0
    for p in tf.paragraphs:
        pPr = p._p.find(qn("a:pPr"))
        marL = int(pPr.get("marL", 0)) if pPr is not None else 0
        bullet = pPr is not None and pPr.find(qn("a:buChar")) is not None
        runs = []
        pt = default_pt
        for r in p.runs:
            pt = r.font.size.pt if r.font.size else default_pt
            f = font(pt, bool(r.font.bold))
            c = col(r.font.color.rgb) if r.font.color and r.font.color.type is not None else "#000000"
            for wd in r.text.replace("\n", " ").split(" "):
                if wd:
                    runs.append((wd, f, c))
        indent = px(marL)
        lines = wrap(draw, runs, w - ml - mr - indent) if runs else [[]]
        lh = pt * 1.2 * DPI / 72
        sb = 0
        if pPr is not None:
            sbe = pPr.find(qn("a:spcBef"))
            if sbe is not None:
                sb = int(sbe[0].get("val")) / 100 * DPI / 72
        blocks.append((lines, lh, indent, bullet, sb, p.alignment))
        total += sb + lh * len(lines)
    anchor = tf.vertical_anchor
    yy = y + mt
    if anchor is not None and int(anchor) == 3:  # middle
        yy = y + (h - total) / 2
    elif anchor is not None and int(anchor) == 4:  # bottom
        yy = y + h - mb - total
    for lines, lh, indent, bullet, sb, al in blocks:
        yy += sb
        for li, line in enumerate(lines):
            lw = sum(draw.textlength(wd + " ", font=f) for wd, f, c in line)
            xx = x + ml + indent
            if al is not None and int(al) == 2:
                xx = x + (w - lw) / 2
            elif al is not None and int(al) == 3:
                xx = x + w - mr - lw
            if bullet and li == 0 and line:
                draw.text((xx - px(Emu(int(0.17 * 914400))), yy), "•", font=line[0][1], fill=line[0][2])
            for wd, f, c in line:
                draw.text((xx, yy), wd, font=f, fill=c)
                xx += draw.textlength(wd + " ", font=f)
            yy += lh
    if yy > y + h + 3:
        draw.rectangle([x, y, x + w, y + h], outline="#ff00ff", width=2)
    return yy


def draw_chart(draw, gf, x, y, w, h):
    ch = gf.chart
    plot = ch.plots[0]
    cats = list(plot.categories)
    sers = list(plot.series)
    pa = ch._chartSpace.chart.plotArea
    ml = pa.find(qn("c:layout"))
    fx, fy, fw, fh = 0.06, 0.12, 0.88, 0.7
    if ml is not None and ml.find(qn("c:manualLayout")) is not None:
        m = ml.find(qn("c:manualLayout"))
        g = lambda t: float(m.find(qn(t)).get("val"))
        fx, fy, fw, fh = g("c:x"), g("c:y"), g("c:w"), g("c:h")
    X, Y, W, H = x + fx * w, y + fy * h, fw * w, fh * h
    draw.rectangle([x, y, x + w, y + h], outline="#e0e0ff")
    xml = ch._chartSpace.xml
    horizontal = 'barDir val="bar"' in xml
    stacked = 'grouping val="stacked"' in xml
    vals = [list(s.values) for s in sers]
    vmax = ch.value_axis.maximum_scale or max(max(v) for v in vals) * 1.1
    n = len(cats)
    slot = (H if horizontal else W) / n
    for i in range(n):
        acc = 0
        k = len(sers)
        for si, s in enumerate(sers):
            v = vals[si][i] or 0
            fill = None
            try:
                pt = s.points[i]
                if pt.format.fill.type == 1:
                    fill = col(pt.format.fill.fore_color.rgb)
            except Exception:
                pass
            if fill is None:
                try:
                    if s.format.fill.type == 1:
                        fill = col(s.format.fill.fore_color.rgb)
                except Exception:
                    fill = None
            if horizontal:
                bh = slot * 0.6 / (1 if stacked else k)
                by = Y + slot * i + slot * 0.2 + (0 if stacked else si * bh)
                bx0 = X + W * acc / vmax
                bx1 = X + W * (acc + v) / vmax
                if fill:
                    draw.rectangle([bx0, by, bx1, by + bh], fill=fill)
                draw.text((X - 5, by), "", fill="#000")
                if not stacked:
                    draw.text((bx1 + 3, by), f"{v:.2f}", font=font(9, False), fill="#000")
            else:
                bw = slot * 0.6 / (1 if stacked else k)
                bx = X + slot * i + slot * 0.2 + (0 if stacked else si * bw)
                by0 = Y + H - H * acc / vmax
                by1 = Y + H - H * (acc + v) / vmax
                if fill:
                    draw.rectangle([bx, by1, bx + bw, by0], fill=fill)
                if not stacked:
                    draw.text((bx, by1 - 14), f"{v:.1f}", font=font(9, False), fill="#000")
            if stacked:
                acc += v
        f = font(9, False)
        for li, ln in enumerate(str(cats[i]).split("\n")):
            if horizontal:
                draw.text((x + 2, Y + slot * i + slot * 0.3 + li * 12), ln, font=f, fill="#555")
            else:
                tw = draw.textlength(ln, font=f)
                draw.text((X + slot * i + slot / 2 - tw / 2, Y + H + 4 + li * 12), ln, font=f, fill="#555")


def render(path, outdir):
    prs = Presentation(path)
    W, H = px(prs.slide_width), px(prs.slide_height)
    os.makedirs(outdir, exist_ok=True)
    for idx, slide in enumerate(prs.slides, 1):
        img = Image.new("RGB", (W, H), "white")
        d = ImageDraw.Draw(img)
        for shp in slide.shapes:
            x, y, w, h = px(shp.left), px(shp.top), px(shp.width), px(shp.height)
            if shp.shape_type == MSO_SHAPE_TYPE.TABLE:
                tbl = shp.table
                yy = y
                for ri, row in enumerate(tbl.rows):
                    rh = px(row.height)
                    xx = x
                    need = rh
                    for ci, cell in enumerate(row.cells):
                        cw = px(tbl.columns[ci].width)
                        try:
                            fc = col(cell.fill.fore_color.rgb)
                        except Exception:
                            fc = "white"
                        d.rectangle([xx, yy, xx + cw, yy + rh], fill=fc, outline="#d9d8d3")
                        end = draw_tf(d, cell.text_frame, xx, yy, cw, rh, 10)
                        xx += cw
                    yy += rh
                continue
            if shp.has_chart if hasattr(shp, "has_chart") else False:
                draw_chart(d, shp, x, y, w, h)
                continue
            if shp.shape_type == MSO_SHAPE_TYPE.LINE or shp.__class__.__name__ == "Connector":
                d.line([x, y, x + w, y + h], fill="#bbbbbb", width=1)
                continue
            try:
                if shp.fill.type == 1:
                    d.rectangle([x, y, x + w, y + h], fill=col(shp.fill.fore_color.rgb))
            except Exception:
                pass
            if shp.has_text_frame:
                draw_tf(d, shp.text_frame, x, y, w, h)
        img.save(os.path.join(outdir, f"slide{idx:02d}.png"))
    print("rendered", idx)


if __name__ == "__main__":
    render(sys.argv[1], sys.argv[2])
