"""Rough preview renderer + overflow checker for the deck (no LibreOffice available).
Draws shapes, wraps text with real Calibri metrics, grows table rows like PowerPoint does, and reports
text boxes whose wrapped text exceeds the box, tables that grow beyond their nominal height, and overlaps.
Charts are drawn as labelled placeholders with their series values."""
import sys, os
from pptx import Presentation
from pptx.util import Emu
from PIL import Image, ImageDraw, ImageFont

FD = "/Applications/Microsoft PowerPoint.app/Contents/Resources/DFonts/"
DPI = 110
fonts = {}
def font(size, bold):
    k = (round(size * 2) / 2, bold)
    if k not in fonts:
        fonts[k] = ImageFont.truetype(FD + ("Calibrib.ttf" if bold else "Calibri.ttf"), max(6, int(k[0] * DPI / 72)))
    return fonts[k]
def inch(e): return Emu(e).inches
def px(i): return int(i * DPI)

def wrap_para(p, width_in, default_size=12):
    """Return list of lines (each list of (text, font)) and line height in inches."""
    runs = [(r.text, font(r.font.size.pt if r.font.size else default_size, bool(r.font.bold))) for r in p.runs]
    size = max([r.font.size.pt if r.font.size else default_size for r in p.runs] or [default_size])
    lh = size * 1.2 / 72
    words = []
    for t, f in runs:
        for i, w in enumerate(t.replace("\n", " \n ").split(" ")):
            words.append((w, f))
    lines, cur, curw = [], [], 0.0
    maxw = width_in * DPI
    for w, f in words:
        if w == "\n":
            lines.append(cur); cur, curw = [], 0; continue
        ww = f.getlength(w + " ")
        if curw + ww > maxw and cur:
            lines.append(cur); cur, curw = [], 0
        cur.append((w, f)); curw += ww
    lines.append(cur)
    return lines, lh

def frame_height(tf, width_in):
    h, out = 0.0, []
    for p in tf.paragraphs:
        ind = 0.0
        pPr = p._p.pPr
        if pPr is not None and pPr.get("marL"): ind = inch(int(pPr.get("marL")))
        lines, lh = wrap_para(p, width_in - ind)
        sa = (p.space_after.pt / 72) if p.space_after is not None else 0
        out.append((lines, lh, ind, h))
        h += lh * len(lines) + sa
    return h, out

def render(path, outdir):
    prs = Presentation(path)
    W, H = inch(prs.slide_width), inch(prs.slide_height)
    issues = []
    boxes = []
    for si, slide in enumerate(prs.slides, 1):
        img = Image.new("RGB", (px(W), px(H)), "white"); d = ImageDraw.Draw(img)
        for sh in slide.shapes:
            x, y, w, h = inch(sh.left), inch(sh.top), inch(sh.width), inch(sh.height)
            if sh.shape_type == 1 or (sh.has_text_frame and sh.shape_type == 17) or sh.shape_type == 9:
                pass
            fill = None
            try:
                if sh.fill.type == 1: fill = "#" + str(sh.fill.fore_color.rgb)
            except Exception: pass
            if sh.has_chart:
                d.rectangle([px(x), px(y), px(x + w), px(y + h)], outline="#bbbbbb")
                ch = sh.chart
                cats = list(ch.plots[0].categories)
                txt = f"[{ch.chart_type}] " + "; ".join(f"{s.name}: " + ", ".join(f"{v:.1f}" for v in s.values) for s in ch.plots[0].series)
                d.text((px(x) + 4, px(y) + 4), txt[:160], fill="#888888", font=font(8, False))
                d.text((px(x) + 4, px(y) + 18), "cats: " + " | ".join(str(c).replace("\n", "/") for c in cats), fill="#888888", font=font(8, False))
                # crude bar sketch
                s0 = ch.plots[0].series[0]; vals = list(s0.values)
                vmax = max(abs(v) for v in vals) or 1
                for i, v in enumerate(vals):
                    bx = x + 0.4 + (w - 0.8) * (i + 0.2) / len(vals); bw = (w - 0.8) / len(vals) * 0.6
                    base = y + h * 0.6; bh = (h * 0.35) * v / vmax
                    d.rectangle([px(bx), px(min(base, base - bh)), px(bx + bw), px(max(base, base - bh))], fill="#cfe0f6")
                boxes.append((si, "chart", x, y, w, h)); continue
            if sh.has_table:
                tbl = sh.table
                cy = y; total = 0
                colw = [inch(c.width) for c in tbl.columns]
                for ri, row in enumerate(tbl.rows):
                    rh = inch(row.height)
                    need = 0
                    for ci, cell in enumerate(row.cells):
                        if cell.is_spanned: continue
                        cw = colw[ci]
                        if cell.is_merge_origin: cw = sum(colw[ci:ci + cell.span_width])
                        hh, _ = frame_height(cell.text_frame, cw - 0.12 - 0.02)
                        need = max(need, hh + 0.06 + 0.02)
                    rh2 = max(rh, need)
                    cx = x
                    for ci, cell in enumerate(row.cells):
                        cw = colw[ci]
                        if cell.is_spanned: cx += cw; continue
                        if cell.is_merge_origin: cw = sum(colw[ci:ci + cell.span_width])
                        try: f = "#" + str(cell.fill.fore_color.rgb)
                        except Exception: f = "#ffffff"
                        d.rectangle([px(cx), px(cy), px(cx + cw), px(cy + rh2)], fill=f, outline="#dddddd")
                        hh, lines = frame_height(cell.text_frame, cw - 0.14)
                        ty = cy + (rh2 - hh) / 2
                        for ls, lh, ind, off in lines:
                            for li, ln in enumerate(ls):
                                tx = cx + 0.06
                                for wd, fo in ln:
                                    d.text((px(tx), px(ty + off + li * lh)), wd, fill="#222222", font=fo); tx += fo.getlength(wd + " ") / DPI
                        cx += colw[ci] if not cell.is_merge_origin else cw
                    cy += rh2
                nominal = h
                if cy - y > nominal + 0.05:
                    issues.append(f"slide {si}: table grows {nominal:.2f}->{cy - y:.2f}in (bottom {cy:.2f})")
                boxes.append((si, "table", x, y, w, cy - y)); continue
            if fill:
                d.rectangle([px(x), px(y), px(x + w), px(y + h)], fill=fill)
            if sh.shape_type == 9 or (hasattr(sh, "begin_x") and not sh.has_text_frame):
                try:
                    d.line([px(inch(sh.begin_x)), px(inch(sh.begin_y)), px(inch(sh.end_x)), px(inch(sh.end_y))], fill="#e34948", width=2)
                except Exception: pass
                continue
            if sh.has_text_frame and sh.text_frame.text.strip():
                tf = sh.text_frame
                ml = inch(tf.margin_left or 0); mr = inch(tf.margin_right or 0); mt = inch(tf.margin_top or 0)
                hh, lines = frame_height(tf, w - ml - mr)
                anchor = tf.vertical_anchor
                ty = y + mt
                if anchor is not None and int(anchor) == 3: ty = y + (h - hh) / 2
                for ls, lh, ind, off in lines:
                    for li, ln in enumerate(ls):
                        tx = x + ml + ind
                        for wd, fo in ln:
                            col = "#ffffff" if fill and fill.lower() in ("#14213d", "#2a78d6", "#2f4a7a", "#5b6f94") else "#222222"
                            d.text((px(tx), px(ty + off + li * lh)), wd, fill=col, font=fo); tx += fo.getlength(wd + " ") / DPI
                if hh + 2 * mt > h + 0.04:
                    issues.append(f"slide {si}: text overflow {hh + 2*mt:.2f} > {h:.2f}in: '{tf.text[:60]}'")
                if y + hh > H - 0.05: issues.append(f"slide {si}: text below slide bottom")
                boxes.append((si, "text", x, y, w, max(h, hh)))
        img.save(os.path.join(outdir, f"s{si:02d}.png"))
    # overlap check between tables/charts and text boxes with content (excluding contained)
    by = {}
    for b in boxes: by.setdefault(b[0], []).append(b)
    for si, bs in by.items():
        for i in range(len(bs)):
            for j in range(i + 1, len(bs)):
                a, b = bs[i], bs[j]
                if a[1] == "text" and b[1] == "text": continue
                ox = min(a[2] + a[4], b[2] + b[4]) - max(a[2], b[2]); oy = min(a[3] + a[5], b[3] + b[5]) - max(a[3], b[3])
                if ox > 0.05 and oy > 0.05:
                    issues.append(f"slide {si}: overlap {a[1]}@({a[2]:.2f},{a[3]:.2f}) with {b[1]}@({b[2]:.2f},{b[3]:.2f}) by {ox:.2f}x{oy:.2f}")
    return issues

if __name__ == "__main__":
    out = sys.argv[2]; os.makedirs(out, exist_ok=True)
    for i in render(sys.argv[1], out): print(i)
