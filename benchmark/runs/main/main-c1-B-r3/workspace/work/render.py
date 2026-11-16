"""Approximate renderer for QA: draws shapes + wrapped text with PIL, reports text overflow."""
import sys, os
from PIL import Image, ImageDraw, ImageFont
from pptx import Presentation
from pptx.util import Emu
from pptx.enum.shapes import MSO_SHAPE_TYPE

DPI = 120
FD = "/System/Library/Fonts/Supplemental/"
_fc = {}


def font(size_pt, bold=False, sym=False):
    px = max(1, int(round(size_pt / 72 * DPI)))
    key = (px, bold, sym)
    if key not in _fc:
        f = "Arial Unicode.ttf" if sym else ("Arial Bold.ttf" if bold else "Arial.ttf")
        _fc[key] = ImageFont.truetype(FD + f, px)
    return _fc[key]


SYM = set("✓✗◐→–•×≤≥≈Δ“”’…")


def emu2px(v):
    return v / 914400 * DPI


def col(c, default=None):
    try:
        return "#" + str(c.rgb)
    except Exception:
        return default


def wrap_runs(runs, maxw):
    """runs: list of (text, font, color). returns lines: list of list of (text, font, color, width)."""
    words = []  # (word_with_trailing_space, font, color)
    for t, f, c in runs:
        parts = t.replace("\n", " \n ").split(" ")
        for i, p in enumerate(parts):
            if p == "\n":
                words.append(("\n", f, c)); continue
            w = p + (" " if i < len(parts) - 1 else "")
            if w:
                words.append((w, f, c))
    lines, cur, curw = [], [], 0
    overflow_w = False
    for w, f, c in words:
        if w == "\n":
            lines.append(cur); cur, curw = [], 0; continue
        ww = sum(f.getlength(ch) if ch not in SYM else font(f.size * 72 / DPI, sym=True).getlength(ch) for ch in w)
        trimmed = sum(f.getlength(ch) for ch in w.rstrip(" "))
        if curw + trimmed > maxw and cur:
            lines.append(cur); cur, curw = [], 0
        if trimmed > maxw:
            overflow_w = True
        cur.append((w, f, c, ww)); curw += ww
    if cur:
        lines.append(cur)
    return lines, overflow_w


def render(path, outdir, only=None):
    prs = Presentation(path)
    SW, SH = emu2px(prs.slide_width), emu2px(prs.slide_height)
    issues = []
    for si, slide in enumerate(prs.slides, 1):
        if only and si not in only:
            continue
        img = Image.new("RGB", (int(SW), int(SH)), "white")
        d = ImageDraw.Draw(img)
        tboxes = []
        for sh in slide.shapes:
            x, y, w, h = [emu2px(v or 0) for v in (sh.left, sh.top, sh.width, sh.height)]
            tag = sh._element.tag.split("}")[1]
            if tag == "cxnSp":
                ln = sh.line
                c = col(ln.color, "#999999")
                wpx = max(1, int(round((ln.width or Emu(9525)) / 12700 / 72 * DPI)))
                x1, y1, x2, y2 = x, y, x + w, y + h
                if sh._element.spPr.find('.//{http://schemas.openxmlformats.org/drawingml/2006/main}xfrm').get('flipV') == '1':
                    y1, y2 = y2, y1
                d.line([(x1, y1), (x2, y2)], fill=c, width=wpx)
                continue
            if tag == "sp":
                el = sh._element
                cust = el.find('.//{http://schemas.openxmlformats.org/drawingml/2006/main}custGeom')
                fillc = None
                try:
                    if sh.fill.type == 1:
                        fillc = col(sh.fill.fore_color)
                except Exception:
                    pass
                linec = None
                try:
                    if sh.line.fill.type == 1:
                        linec = col(sh.line.color)
                except Exception:
                    pass
                if cust is not None:
                    ns = '{http://schemas.openxmlformats.org/drawingml/2006/main}'
                    p = cust.find(f'.//{ns}path')
                    pw_, ph_ = float(p.get('w')), float(p.get('h'))
                    pts = []
                    for e in p:
                        pt = e.find(f'{ns}pt')
                        if pt is not None:
                            pts.append((x + float(pt.get('x')) / max(pw_, 1) * w, y + float(pt.get('y')) / max(ph_, 1) * h))
                    wpx = max(1, int(round((sh.line.width or Emu(9525)) / 12700 / 72 * DPI)))
                    if linec and len(pts) > 1:
                        d.line(pts, fill=linec, width=wpx)
                elif sh.shape_type == MSO_SHAPE_TYPE.AUTO_SHAPE:
                    st = sh.auto_shape_type
                    name = str(st)
                    if "OVAL" in name:
                        d.ellipse([x, y, x + w, y + h], fill=fillc, outline=linec)
                    elif "CHEVRON" in name or "PENTAGON" in name:
                        tip = h * 0.5
                        poly = [(x, y), (x + w - tip, y), (x + w, y + h / 2), (x + w - tip, y + h), (x, y + h)]
                        if "CHEVRON" in name:
                            poly.append((x + tip, y + h / 2))
                        d.polygon(poly, fill=fillc, outline=linec)
                    elif "ROUNDED" in name:
                        d.rounded_rectangle([x, y, x + w, y + h], radius=min(w, h) * 0.3, fill=fillc, outline=linec, width=1)
                    else:
                        d.rectangle([x, y, x + w, y + h], fill=fillc, outline=linec)
                elif sh.has_text_frame and fillc:
                    d.rectangle([x, y, x + w, y + h], fill=fillc, outline=linec)
                if sh.has_text_frame and sh.text_frame.text.strip():
                    tf = sh.text_frame
                    ml = emu2px(tf.margin_left or 0); mr = emu2px(tf.margin_right or 0)
                    mt = emu2px(tf.margin_top or 0); mb = emu2px(tf.margin_bottom or 0)
                    maxw = w - ml - mr
                    blocks = []
                    total = 0
                    wflag = False
                    for par in tf.paragraphs:
                        runs = []
                        size = 18
                        for r in par.runs:
                            size = r.font.size.pt if r.font.size else 18
                            runs.append((r.text, font(size, bool(r.font.bold)), col(r.font.color, "#000000")))
                        if not runs:
                            continue
                        pPr = par._p.pPr
                        bu = pPr is not None and pPr.find('{http://schemas.openxmlformats.org/drawingml/2006/main}buChar') is not None
                        indpx = emu2px(int(pPr.get('marL'))) if bu else 0
                        lines, of = wrap_runs(runs, maxw - indpx)
                        if bu:
                            lines[0].insert(0, ("•", runs[0][1], runs[0][2], 0))
                        wflag |= of
                        ls = par.line_spacing or 1.0
                        lh = size / 72 * DPI * 1.17 * ls
                        sa = (par.space_after.pt if par.space_after is not None else 0) / 72 * DPI
                        blocks.append((lines, lh, sa, par.alignment, indpx))
                        total += lh * len(lines) + sa
                    if blocks:
                        total -= blocks[-1][2]
                    anchor = tf.vertical_anchor
                    avail = h - mt - mb
                    if anchor is not None and int(anchor) == 3:
                        cy = y + mt + (avail - total) / 2
                    elif anchor is not None and int(anchor) == 4:
                        cy = y + h - mb - total
                    else:
                        cy = y + mt
                    if total > avail + 2:
                        issues.append((si, "V-OVERFLOW", round((total - avail) / DPI, 2), tf.text[:70]))
                    if wflag:
                        issues.append((si, "WORD-TOO-WIDE", 0, tf.text[:70]))
                    if x + w > SW + 1 or y + h > SH + 1 or x < -1 or y < -1:
                        issues.append((si, "OFF-SLIDE", 0, tf.text[:50]))
                    for lines, lh, sa, al, indpx in blocks:
                        for ln in lines:
                            lw = sum(t[3] for t in ln) - (ln[-1][1].getlength(" ") if ln and ln[-1][0].endswith(" ") else 0)
                            if al is not None and int(al) == 2:
                                cx = x + ml + (maxw - lw) / 2
                            elif al is not None and int(al) == 3:
                                cx = x + w - mr - lw
                            else:
                                cx = x + ml + indpx
                            for t, f, c, ww in ln:
                                if t == "•" and ww == 0:
                                    d.text((x + ml, cy + (lh - f.size * 1.17) / 2), "•", font=f, fill=c); continue
                                for ch in t:
                                    ff = font(f.size * 72 / DPI, sym=True) if ch in SYM else f
                                    d.text((cx, cy + (lh - f.size * 1.17) / 2), ch, font=ff, fill=c)
                                    cx += ff.getlength(ch)
                            cy += lh
                        cy += sa
                    tboxes.append((x, y + mt, x + w, y + mt + total, tf.text[:40]))
        img.save(os.path.join(outdir, f"s{si:02d}.png"))
        # overlap check between rendered text extents
        for i in range(len(tboxes)):
            for j in range(i + 1, len(tboxes)):
                a, b = tboxes[i], tboxes[j]
                ix = min(a[2], b[2]) - max(a[0], b[0]); iy = min(a[3], b[3]) - max(a[1], b[1])
                if ix > 4 and iy > 4:
                    issues.append((si, "TEXT-OVERLAP?", round(iy / DPI, 2), f"[{a[4]}] x [{b[4]}]"))
    return issues


if __name__ == "__main__":
    out = sys.argv[2]
    os.makedirs(out, exist_ok=True)
    only = set(map(int, sys.argv[3].split(","))) if len(sys.argv) > 3 else None
    for i in render(sys.argv[1], out, only):
        print(i)
