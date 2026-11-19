import sys
from pptx import Presentation
from pptx.util import Emu
prs = Presentation(sys.argv[1])
E = 914400
for i, sl in enumerate(prs.slides, 1):
    boxes = []
    for sh in sl.shapes:
        x, y, w, h = sh.left/E, sh.top/E, sh.width/E, sh.height/E
        txt = sh.text_frame.text[:30] if sh.has_text_frame else sh.shape_type
        if x + w > 13.34 or y + h > 7.5 or x < 0 or y < 0:
            print(f"p{i} OUT OF SLIDE {txt!r} {x:.2f},{y:.2f},{w:.2f},{h:.2f}")
        is_footer = y >= 6.99
        if not is_footer and y + h > 6.98 and i > 1:
            print(f"p{i} into footer: {txt!r} bottom={y+h:.2f}")
        if sh.has_text_frame and sh.text_frame.text.strip() and sh.shape_type == 17:  # text box
            boxes.append((x, y, w, h, txt))
        if sh.has_table or sh.has_chart:
            boxes.append((x, y, w, h, "TABLE" if sh.has_table else "CHART"))
    for a in range(len(boxes)):
        for b in range(a+1, len(boxes)):
            x1,y1,w1,h1,t1 = boxes[a]; x2,y2,w2,h2,t2 = boxes[b]
            ox = min(x1+w1, x2+w2) - max(x1, x2); oy = min(y1+h1, y2+h2) - max(y1, y2)
            if ox > 0.05 and oy > 0.05:
                print(f"p{i} overlap {t1!r} <> {t2!r} ({ox:.2f}x{oy:.2f})")
