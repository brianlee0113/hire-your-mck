import sys
from pptx import Presentation
from pptx.util import Emu
p=Presentation(sys.argv[1]); E=914400
for i,sl in enumerate(p.slides,1):
    boxes=[]
    for sh in sl.shapes:
        x,y,w,h=[v/E for v in (sh.left,sh.top,sh.width,sh.height)]
        kind='tbl' if sh.has_table else ('txt' if sh.has_text_frame and sh.text_frame.text.strip() and sh.shape_type==17 else 'shp')
        t=sh.text_frame.text[:30] if sh.has_text_frame else ('TABLE' if sh.has_table else '')
        boxes.append((kind,x,y,w,h,t))
        if y+h>6.92 and not (y>=6.9) and i>1: print(f"s{i} BELOW CONTENT: {kind} {t!r} bottom={y+h:.2f}")
        if x+w>13.34 or x<0: print(f"s{i} OUT X {t!r}")
    big=[b for b in boxes if b[0]=='tbl' or (b[0]=='txt' and b[3]>2.0)]
    for a in range(len(big)):
        for b in range(a+1,len(big)):
            A,B=big[a],big[b]
            ox=min(A[1]+A[3],B[1]+B[3])-max(A[1],B[1]); oy=min(A[2]+A[4],B[2]+B[4])-max(A[2],B[2])
            if ox>0.05 and oy>0.05: print(f"s{i} OVERLAP {A[0]} {A[5]!r} [{A[2]:.2f}-{A[2]+A[4]:.2f}] x {B[0]} {B[5]!r} [{B[2]:.2f}-{B[2]+B[4]:.2f}]")
