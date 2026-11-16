"""Rough PIL preview renderer for the shapes this deck uses (approximate, for layout QA only)."""
import sys, os
from pptx import Presentation
from pptx.util import Emu
from pptx.enum.shapes import MSO_SHAPE_TYPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from PIL import Image, ImageDraw, ImageFont

DPI = 110
FF = {False: "/System/Library/Fonts/Supplemental/Arial.ttf", True: "/System/Library/Fonts/Supplemental/Arial Bold.ttf"}
_c = {}
def F(b, px):
    k = (b, px)
    if k not in _c: _c[k] = ImageFont.truetype(FF[b], max(px, 6))
    return _c[k]
def px(e): return int(round(Emu(e).inches * DPI))
def rgb(c):
    try: return "#" + str(c)
    except Exception: return None

def fill_of(shape):
    try:
        if shape.fill.type == 1: return "#" + str(shape.fill.fore_color.rgb)
    except Exception: pass
    return None

def draw_tf(d, tf, x, y, w, h, ml=0.04, mr=0.04, mt=0.02, anchor=None):
    ml = px(tf.margin_left) if tf.margin_left is not None else int(0.1 * DPI)
    mr = px(tf.margin_right) if tf.margin_right is not None else int(0.1 * DPI)
    mt = px(tf.margin_top) if tf.margin_top is not None else int(0.05 * DPI)
    aw = w - ml - mr
    lines = []  # (list of (text,font,color), align, height)
    for pi, p in enumerate(tf.paragraphs):
        runs = [(r.text, r.font.bold or False, (r.font.size.pt if r.font.size else 18), str(r.font.color.rgb) if r.font.color and r.font.color.type else "000000") for r in p.runs]
        if not runs: continue
        sz = max(r[2] for r in runs)
        lh = int(sz / 72 * DPI * 1.2 * (p.line_spacing if isinstance(p.line_spacing, float) else 1.0))
        sb = int((p.space_before.pt if p.space_before else 0) / 72 * DPI) if pi > 0 else 0
        # tokens
        toks = []
        for t, b, s, c in runs:
            parts = t.replace("\n", " \n ").split(" ")
            for i, wd in enumerate(parts):
                toks.append((wd + (" " if i < len(parts) - 1 else ""), b, s, c))
        cur = []; curw = 0; first = True
        for tok in toks:
            f = F(tok[1], int(tok[2] / 72 * DPI))
            tw = f.getlength(tok[0])
            if tok[0].strip() == "\n":
                lines.append((cur, p.alignment, lh, sb if first else 0)); first = False; cur = []; curw = 0; continue
            if curw + f.getlength(tok[0].rstrip()) > aw and cur:
                lines.append((cur, p.alignment, lh, sb if first else 0)); first = False; cur = []; curw = 0
            cur.append(tok); curw += tw
        lines.append((cur, p.alignment, lh, sb if first else 0))
    total = sum(l[2] + l[3] for l in lines)
    va = tf.vertical_anchor if anchor is None else anchor
    if va == MSO_ANCHOR.MIDDLE: yy = y + (h - total) / 2
    elif va == MSO_ANCHOR.BOTTOM: yy = y + h - total - mt
    else: yy = y + mt
    for cur, al, lh, sb in lines:
        yy += sb
        lw = sum(F(t[1], int(t[2] / 72 * DPI)).getlength(t[0]) for t in cur)
        if al == PP_ALIGN.CENTER: xx = x + ml + (aw - lw) / 2
        elif al == PP_ALIGN.RIGHT: xx = x + w - mr - lw
        else: xx = x + ml
        for t, b, s, c in cur:
            f = F(b, int(s / 72 * DPI))
            d.text((xx, yy), t, font=f, fill="#" + c)
            xx += f.getlength(t)
        yy += lh
    return yy > y + h + 2  # overflow flag

def render(path, outdir):
    prs = Presentation(path)
    W, H = px(prs.slide_width), px(prs.slide_height)
    os.makedirs(outdir, exist_ok=True)
    for n, sl in enumerate(prs.slides, 1):
        im = Image.new("RGB", (W, H), "white"); d = ImageDraw.Draw(im)
        for sh in sl.shapes:
            x, y, w, h = px(sh.left), px(sh.top), px(sh.width), px(sh.height)
            if sh.shape_type == MSO_SHAPE_TYPE.TABLE:
                tbl = sh.table; yy = y
                for r, row in enumerate(tbl.rows):
                    xx = x; rh = px(row.height)
                    for c, col in enumerate(tbl.columns):
                        cw = px(col.width); cell = tbl.cell(r, c)
                        fc = None
                        try: fc = "#" + str(cell.fill.fore_color.rgb)
                        except Exception: pass
                        d.rectangle([xx, yy, xx + cw, yy + rh], fill=fc or "white", outline="#d9d7d2")
                        draw_tf(d, cell.text_frame, xx, yy, cw, rh, anchor=cell.vertical_anchor)
                        xx += cw
                    yy += rh
                continue
            if sh.shape_type == MSO_SHAPE_TYPE.FREEFORM:
                el = sh._element
                ns = {"a": "http://schemas.openxmlformats.org/drawingml/2006/main"}
                path_el = el.find(".//a:path", ns)
                pw, ph = int(path_el.get("w")), int(path_el.get("h"))
                pts = [(int(p.get("x")), int(p.get("y"))) for p in path_el.iter("{%s}pt" % ns["a"])]
                P = [(x + (a / pw * w if pw else 0), y + (b / ph * h if ph else 0)) for a, b in pts]
                col = "#" + str(sh.line.color.rgb)
                d.line(P, fill=col, width=max(1, int(sh.line.width.pt / 72 * DPI)))
                continue
            if sh.shape_type == MSO_SHAPE_TYPE.LINE or sh.__class__.__name__ == "Connector":
                bx, by, ex, ey = px(sh.begin_x), px(sh.begin_y), px(sh.end_x), px(sh.end_y)
                try: col = "#" + str(sh.line.color.rgb)
                except Exception: col = "#000000"
                d.line([bx, by, ex, ey], fill=col, width=max(1, int(sh.line.width.pt / 72 * DPI)))
                continue
            fc = fill_of(sh)
            outline = None
            try:
                if sh.line.fill.type == 1: outline = "#" + str(sh.line.color.rgb)
            except Exception: pass
            if fc or outline:
                try: ast = sh.auto_shape_type
                except Exception: ast = None
                if ast is not None and "OVAL" in str(ast):
                    d.ellipse([x, y, x + w, y + h], fill=fc, outline=outline)
                else:
                    d.rectangle([x, y, x + w, y + h], fill=fc, outline=outline)
            if sh.has_text_frame and sh.text_frame.text.strip():
                if draw_tf(d, sh.text_frame, x, y, w, h):
                    d.rectangle([x, y, x + w, y + h], outline="red", width=2)
        im.save(os.path.join(outdir, f"slide{n:02d}.png"))
    print("rendered", len(prs.slides))

if __name__ == "__main__":
    render(sys.argv[1], sys.argv[2])
