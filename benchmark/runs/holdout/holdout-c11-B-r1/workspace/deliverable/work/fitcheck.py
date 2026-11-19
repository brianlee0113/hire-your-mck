import sys, math
from pptx import Presentation
from pptx.util import Emu
CW = 0.50  # avg char width as fraction of font size (Calibri ~0.47; padded)
def need(tf, width_in, default=12):
    h = 0
    for p in tf.paragraphs:
        txt = "".join(r.text for r in p.runs)
        sz = max([r.font.size.pt for r in p.runs if r.font.size] or [default])
        lines = 0
        for seg in txt.split("\n"):
            lines += max(1, math.ceil(len(seg) * sz * CW / 72 / max(width_in, 0.1)))
        sa = p.space_after.pt if p.space_after is not None else 0
        h += lines * sz * 1.2 / 72 + sa / 72
    return h
prs = Presentation(sys.argv[1])
for i, s in enumerate(prs.slides, 1):
    for sh in s.shapes:
        if sh.has_text_frame and sh.text_frame.text.strip():
            tf = sh.text_frame
            w = Emu(sh.width).inches - Emu(tf.margin_left).inches - Emu(tf.margin_right).inches
            h = Emu(sh.height).inches - Emu(tf.margin_top).inches - Emu(tf.margin_bottom).inches
            n = need(tf, w)
            if n > h * 1.0:
                print(f"slide {i}: TEXT overflow need {n:.2f} > {h:.2f}  '{tf.text[:60]}'")
        if sh.has_table:
            tbl = sh.table; total = 0
            for r in tbl.rows:
                rh = Emu(r.height).inches; mx = rh
                for ci, c in enumerate(r.cells):
                    w = Emu(tbl.columns[ci].width).inches - 0.14
                    mx = max(mx, need(c.text_frame, w) + 0.08)
                total += mx
            bottom = Emu(sh.top).inches + total
            flag = "  <-- OVER 6.98" if bottom > 6.98 else ""
            print(f"slide {i}: table est height {total:.2f} bottom {bottom:.2f}{flag}")
