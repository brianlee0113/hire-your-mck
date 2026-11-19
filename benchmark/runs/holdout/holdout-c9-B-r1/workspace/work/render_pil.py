"""Approximate PPTX renderer (PIL + Arial metrics) for layout QA: draws shapes, wraps text, flags overflow."""
import sys, os
from pptx import Presentation
from pptx.util import Emu
from pptx.enum.shapes import MSO_SHAPE_TYPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from PIL import Image, ImageDraw, ImageFont

SCALE = 120  # px per inch
FD = "/System/Library/Fonts/Supplemental/"
_fc = {}


def font(pt, bold=False):
    k = (round(pt * 2) / 2, bold)
    if k not in _fc:
        _fc[k] = ImageFont.truetype(FD + ("Arial Bold.ttf" if bold else "Arial.ttf"), int(round(pt / 72 * SCALE)))
    return _fc[k]


def px(emu):
    return Emu(emu).inches * SCALE


def wrap(txt, f, width):
    lines = []
    for para in txt.split("\n"):
        cur = ""
        for w in para.split(" "):
            t = (cur + " " + w) if cur else w
            if f.getlength(t) <= width or not cur:
                cur = t
            else:
                lines.append(cur); cur = w
        lines.append(cur)
    return lines


def rgb(c, default=None):
    try:
        return "#" + str(c.rgb)
    except Exception:
        return default


def layout_tf(tf, width):
    """returns list of (lines, font, color, align, space_before_px, line_h) and total height"""
    out, tot = [], 0
    for p in tf.paragraphs:
        txt = "".join(r.text for r in p.runs)
        r0 = p.runs[0] if p.runs else None
        size = r0.font.size.pt if r0 is not None and r0.font.size else 18
        bold = bool(r0.font.bold) if r0 is not None else False
        col = rgb(r0.font.color, "#000000") if r0 is not None else "#000000"
        f = font(size, bold)
        lines = wrap(txt, f, width)
        lh = size * 1.2 / 72 * SCALE
        sb = (p.space_before.pt / 72 * SCALE) if p.space_before is not None else 0
        out.append((lines, f, col, p.alignment, sb, lh))
        tot += sb + lh * len(lines)
    return out, tot


def draw_tf(d, tf, x, y, w, h, issues, label):
    ml, mr = px(tf.margin_left), px(tf.margin_right)
    mt, mb = px(tf.margin_top), px(tf.margin_bottom)
    paras, tot = layout_tf(tf, w - ml - mr)
    if tot > h - mt - mb + 2:
        issues.append(f"{label}: text {tot / SCALE:.2f}in > box {(h - mt - mb) / SCALE:.2f}in :: "
                      f"{''.join(r.text for r in tf.paragraphs[0].runs)[:50]}")
    anchor = tf.vertical_anchor
    cy = y + mt
    if anchor == MSO_ANCHOR.MIDDLE:
        cy = y + (h - tot) / 2
    elif anchor == MSO_ANCHOR.BOTTOM:
        cy = y + h - mb - tot
    for lines, f, col, al, sb, lh in paras:
        cy += sb
        for ln in lines:
            lw = f.getlength(ln)
            if al == PP_ALIGN.CENTER:
                lx = x + (w - lw) / 2
            elif al == PP_ALIGN.RIGHT:
                lx = x + w - mr - lw
            else:
                lx = x + ml
            d.text((lx, cy + lh * 0.1), ln, font=f, fill=col)
            if lx + lw > x + w + 1:
                issues.append(f"{label}: line wider than box :: {ln[:40]}")
            cy += lh
    return tot


def render(path, outdir):
    os.makedirs(outdir, exist_ok=True)
    prs = Presentation(path)
    W, H = px(prs.slide_width), px(prs.slide_height)
    report = []
    for i, s in enumerate(prs.slides, 1):
        img = Image.new("RGB", (int(W), int(H)), "white")
        d = ImageDraw.Draw(img)
        issues = []
        for sh in s.shapes:
            x, y, w, h = px(sh.left), px(sh.top), px(sh.width), px(sh.height)
            if sh.shape_type == MSO_SHAPE_TYPE.LINE or sh.__class__.__name__ == "Connector":
                col = rgb(sh.line.color, "#999999")
                wd = max(1, int(sh.line.width.pt / 72 * SCALE)) if sh.line.width else 1
                d.line([(px(sh.begin_x), px(sh.begin_y)), (px(sh.end_x), px(sh.end_y))], fill=col, width=wd)
                continue
            if sh.has_table if hasattr(sh, "has_table") else False:
                tbl = sh.table
                cws = [px(c.width) for c in tbl.columns]
                cy = y
                for r_i, row in enumerate(tbl.rows):
                    # needed height
                    need = px(row.height)
                    for c_i, cell in enumerate(row.cells):
                        _, tot = layout_tf(cell.text_frame, cws[c_i] - px(cell.margin_left) - px(cell.margin_right))
                        need = max(need, tot + px(cell.margin_top) + px(cell.margin_bottom))
                    cx = x
                    for c_i, cell in enumerate(row.cells):
                        fill = rgb(cell.fill.fore_color, "#ffffff") if cell.fill.type is not None else "#ffffff"
                        d.rectangle([cx, cy, cx + cws[c_i], cy + need], fill=fill, outline="#d9d8d3")
                        t = cell.text_frame
                        t.vertical_anchor = cell.vertical_anchor
                        draw_tf(d, t, cx, cy, cws[c_i], need, [], "cell")
                        cx += cws[c_i]
                    cy += need
                if cy > px(prs.slide_height) - 0.6 * SCALE:
                    issues.append(f"table bottom at {cy / SCALE:.2f}in (footer zone)")
                report.append((i, f"table bottom {cy / SCALE:.2f}in"))
                continue
            fill = None
            try:
                if sh.fill.type == 1:
                    fill = rgb(sh.fill.fore_color)
            except Exception:
                pass
            if fill:
                d.rectangle([x, y, x + w, y + h], fill=fill)
            try:
                if sh.line.fill.type == 1:
                    d.rectangle([x, y, x + w, y + h], outline=rgb(sh.line.color, "#999"))
            except Exception:
                pass
            if sh.has_text_frame and sh.text_frame.text.strip():
                draw_tf(d, sh.text_frame, x, y, w, h, issues, f"shape@({x / SCALE:.1f},{y / SCALE:.1f})")
        img.save(os.path.join(outdir, f"slide{i:02d}.png"))
        for it in issues:
            report.append((i, it))
    for r in report:
        print(*r)


if __name__ == "__main__":
    render(sys.argv[1], sys.argv[2])
