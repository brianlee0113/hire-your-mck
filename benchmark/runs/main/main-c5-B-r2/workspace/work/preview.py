"""Approximate renderer for layout QA: draws text boxes, shapes, tables (true Calibri metrics),
charts as simple bar/line sketches. Reports text overflow. Usage: python3 preview.py deck.pptx outdir"""
import sys, os
from pptx import Presentation
from pptx.util import Emu
from PIL import Image, ImageDraw, ImageFont

FD = "/Applications/Microsoft PowerPoint.app/Contents/Resources/DFonts"
FONTS = {}
def font(size_pt, bold=False, italic=False, scale=1.0):
    name = "Calibriz.ttf" if bold and italic else "Calibrib.ttf" if bold else "Calibrii.ttf" if italic else "Calibri.ttf"
    key = (name, round(size_pt * scale, 1))
    if key not in FONTS:
        FONTS[key] = ImageFont.truetype(os.path.join(FD, name), max(1, int(round(size_pt * scale))))
    return FONTS[key]

DPI = 100
px = lambda emu: int(emu / 914400 * DPI)
PT = DPI / 72.0

def color_of(fill):
    try:
        if fill.type == 1:
            c = fill.fore_color.rgb; return (c[0], c[1], c[2])
    except Exception:
        pass
    return None

def wrap_runs(paragraph, width_px, default_size=18):
    """returns list of lines; each line list of (text, font, color); and line height"""
    runs = []
    for r in paragraph.runs:
        f = r.font
        size = f.size.pt if f.size else default_size
        col = (0, 0, 0)
        try:
            if f.color and f.color.type is not None: col = tuple(f.color.rgb)
        except Exception: pass
        runs.append((r.text, font(size, bool(f.bold), bool(f.italic), PT), col, size))
    if not runs:
        return [[]], default_size
    maxsize = max(r[3] for r in runs)
    lines, cur, curw = [], [], 0
    for text, fnt, col, size in runs:
        for seg_i, seg in enumerate(text.split("\n")):
            if seg_i > 0:
                lines.append(cur); cur, curw = [], 0
            words = seg.split(" ")
            for wi, w in enumerate(words):
                token = (" " if (wi > 0) else "") + w
                tw = fnt.getlength(token)
                if curw + tw > width_px and cur:
                    lines.append(cur); cur, curw = [], 0
                    token = w; tw = fnt.getlength(token)
                cur.append((token, fnt, col)); curw += tw
    lines.append(cur)
    return lines, maxsize

def draw_tf(d, tf, x, y, w, h, issues, label, ml=None):
    ml = tf.margin_left if ml is None else ml
    l, r_, t, b = px(tf.margin_left), px(tf.margin_right), px(tf.margin_top), px(tf.margin_bottom)
    width = w - l - r_
    blocks, total = [], 0
    for p in tf.paragraphs:
        lines, size = wrap_runs(p, width)
        ls = p.line_spacing if isinstance(p.line_spacing, float) else 1.0
        lh = size * PT * 1.2 * ls
        sa = p.space_after.pt * PT if p.space_after is not None else 0
        blocks.append((p, lines, lh, sa)); total += lh * len(lines) + sa
    avail = h - t - b
    anchor = tf._txBody.bodyPr.get("anchor", "t")
    yy = y + t + (max(0, avail - total) / 2 if anchor == "ctr" else max(0, avail - total) if anchor == "b" else 0)
    if total > avail + 2:
        issues.append(f"{label}: text overflows by {(total-avail)/DPI:.2f}in")
    for p, lines, lh, sa in blocks:
        align = p.alignment
        for line in lines:
            lw = sum(f.getlength(tk) for tk, f, c in line)
            xx = x + l + ((width - lw) / 2 if align == 2 else (width - lw) if align == 3 else 0)
            for tk, f, c in line:
                d.text((xx, yy), tk, font=f, fill=c); xx += f.getlength(tk)
            yy += lh
        yy += sa

def render(pptx, outdir):
    prs = Presentation(pptx)
    W, H = px(prs.slide_width), px(prs.slide_height)
    os.makedirs(outdir, exist_ok=True)
    all_issues = []
    for si, slide in enumerate(prs.slides, 1):
        img = Image.new("RGB", (W, H), "white"); d = ImageDraw.Draw(img)
        issues = []
        for sh in slide.shapes:
            x, y, w, h = px(sh.left), px(sh.top), px(sh.width), px(sh.height)
            if sh.shape_type == 9 or sh.has_text_frame is False and getattr(sh, "begin_x", None) is not None:
                pass
            if sh.shape_type == 9:  # line
                d.line([(x, y), (x + w, y + h)], fill=(120, 120, 120), width=1); continue
            if sh.has_chart:
                ch = sh.chart
                d.rectangle([x, y, x + w, y + h], outline=(200, 200, 230))
                try:
                    plot = ch.plots[0]; cats = list(plot.categories)
                    sers = [list(s.values) for s in plot.series]
                    vals = [v for s in sers for v in s if v is not None]
                    lo, hi = min(0, min(vals)), max(0, max(vals))
                    try:
                        if ch.value_axis.minimum_scale is not None: lo = ch.value_axis.minimum_scale
                        if ch.value_axis.maximum_scale is not None: hi = ch.value_axis.maximum_scale
                    except Exception: pass
                    py0, py1 = y + 30, y + h - 40
                    yv = lambda v: py1 - (v - lo) / (hi - lo) * (py1 - py0)
                    d.line([(x, yv(0)), (x + w, yv(0))], fill=(150, 150, 150))
                    n = len(cats); cw_ = (w - 40) / max(1, n)
                    for ci, c in enumerate(cats):
                        cx = x + 40 + ci * cw_
                        if n <= 12:
                            d.text((cx, py1 + 4), str(c).replace("\n", " ")[:22], font=font(8, scale=PT), fill=(80, 80, 80))
                    if "LINE" in str(ch.chart_type):
                        for s in sers:
                            pts = [(x + 40 + i * cw_, yv(v)) for i, v in enumerate(s) if v is not None]
                            d.line(pts, fill=(42, 120, 214), width=2)
                    else:
                        stacked = "STACKED" in str(ch.chart_type)
                        horiz = "BAR" in str(ch.chart_type)
                        for ci in range(n):
                            pos = neg = 0
                            for k, s in enumerate(sers):
                                v = s[ci] or 0
                                if stacked:
                                    base = pos if v >= 0 else neg
                                    top = base + v
                                    if v >= 0: pos = top
                                    else: neg = top
                                    if k in (1, 3):
                                        bx = x + 40 + ci * cw_ + cw_ * 0.2
                                        d.rectangle([bx, min(yv(base), yv(top)), bx + cw_ * 0.6, max(yv(base), yv(top))], fill=(42, 120, 214) if v >= 0 else (235, 104, 52))
                                else:
                                    bw = cw_ * 0.7 / len(sers)
                                    bx = x + 40 + ci * cw_ + cw_ * 0.15 + k * bw
                                    d.rectangle([bx, min(yv(0), yv(v)), bx + bw - 2, max(yv(0), yv(v))], fill=(42, 120, 214) if k == 0 else (235, 104, 52))
                    d.text((x + 4, y + 4), f"[chart: {str(ch.chart_type).split('.')[-1]}]", font=font(8, scale=PT), fill=(150, 150, 150))
                except Exception as e:
                    d.text((x + 4, y + 4), f"[chart err {e}]", font=font(8, scale=PT), fill=(255, 0, 0))
                continue
            if sh.has_table:
                tbl = sh.table
                yy = y
                for ri, row in enumerate(tbl.rows):
                    rh = px(row.height); xx = x
                    for ci, col in enumerate(tbl.columns):
                        cw = px(col.width); cell = tbl.cell(ri, ci)
                        fc = color_of(cell.fill) or (255, 255, 255)
                        d.rectangle([xx, yy, xx + cw, yy + rh], fill=fc, outline=(225, 224, 217))
                        tf = cell.text_frame
                        # cell margins
                        l, r_ = px(cell.margin_left), px(cell.margin_right)
                        tot = 0; blocks = []
                        for p in tf.paragraphs:
                            lines, size = wrap_runs(p, cw - l - r_)
                            blocks.append((p, lines, size * PT * 1.2)); tot += size * PT * 1.2 * len(lines)
                        if tot > rh - px(cell.margin_top) - px(cell.margin_bottom) + 2:
                            issues.append(f"table r{ri}c{ci} '{tf.text[:35]}' overflows row by {(tot-rh)/DPI:.2f}in (row grows)")
                        ty = yy + max(0, (rh - tot) / 2)
                        for p, lines, lh in blocks:
                            for line in lines:
                                lw = sum(f.getlength(tk) for tk, f, c in line)
                                tx = xx + l + ((cw - l - r_ - lw) / 2 if p.alignment == 2 else 0)
                                for tk, f, c in line:
                                    d.text((tx, ty), tk, font=f, fill=c); tx += f.getlength(tk)
                                ty += lh
                        xx += cw
                    yy += rh
                continue
            fc = None
            try: fc = color_of(sh.fill)
            except Exception: pass
            if fc: d.rectangle([x, y, x + w, y + h], fill=fc)
            if sh.has_text_frame and sh.text_frame.text.strip():
                draw_tf(d, sh.text_frame, x, y, w, h, issues, f"'{sh.text_frame.text[:40]}'")
            if x + w > W + 1 or y + h > H + 1:
                issues.append(f"shape off-slide: {sh.name}")
        img.save(os.path.join(outdir, f"slide{si:02d}.png"))
        for i in issues: all_issues.append(f"slide {si}: {i}")
    print("\n".join(all_issues) if all_issues else "no issues")

if __name__ == "__main__":
    render(sys.argv[1], sys.argv[2])
