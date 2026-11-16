import math,sys
from pptx import Presentation
from pptx.util import Emu
prs=Presentation(sys.argv[1]); CW=0.50
def para_lines(p,width_pt):
    txt="".join(r.text for r in p.runs); 
    if not p.runs: return 1, 12
    sz=max((r.font.size.pt if r.font.size else 12) for r in p.runs)
    lines=0
    for seg in txt.split("\n"):
        lines+=max(1,math.ceil(len(seg)*sz*CW/width_pt))
    return lines,sz
def need(tf,width_pt):
    h=0
    for p in tf.paragraphs:
        l,sz=para_lines(p,width_pt); h+=l*sz*1.2+(p.space_after.pt if p.space_after else 0)
    return h
for i,sl in enumerate(prs.slides,1):
    for sh in sl.shapes:
        if sh.has_text_frame and sh.text_frame.text.strip():
            w=Emu(sh.width).pt-6; h=Emu(sh.height).pt
            n=need(sh.text_frame,w)
            if n>h*1.02: print(f"S{i} TEXT over {n:.0f}>{h:.0f}: {sh.text_frame.text[:60]!r}")
            bottom=Emu(sh.top).inches+n/72
            if bottom>7.0 and Emu(sh.top).inches<6.9: print(f"S{i} TEXT bottom {bottom:.2f}in: {sh.text_frame.text[:50]!r}")
        if sh.has_table:
            t=sh.table; tot=0
            for r,row in enumerate(t.rows):
                req=0
                for c,cell in enumerate(row.cells):
                    w=Emu(t.columns[c].width).pt-9
                    req=max(req,need(cell.text_frame,w)+5)
                tot+=max(req,Emu(row.height).pt)
                if req>Emu(row.height).pt*1.02: print(f"S{i} TABLE row {r} grows {Emu(row.height).pt:.0f}->{req:.0f}")
            bottom=Emu(sh.top).inches+tot/72
            print(f"S{i} table bottom {bottom:.2f}in") if bottom>6.9 else None
