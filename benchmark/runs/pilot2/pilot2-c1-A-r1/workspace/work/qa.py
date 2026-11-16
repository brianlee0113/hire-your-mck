import sys
from pptx import Presentation
from pptx.util import Emu
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
sys.path.insert(0,'.')
from lib import est_lines
E=914400
p=Presentation(sys.argv[1])
def content_box(sh):
    tf=sh.text_frame; x=sh.left/E; y=sh.top/E; w=sh.width/E; h=sh.height/E
    lines=0; maxw=0; hh=0
    for para in tf.paragraphs:
        t="".join(r.text for r in para.runs)
        if not para.runs: continue
        sz=max((r.font.size.pt if r.font.size else 12) for r in para.runs); b=any(r.font.bold for r in para.runs)
        cw=sz/72*(0.565 if b else 0.53)
        n=est_lines(t,w-0.08,sz,b); hh+=n*sz*1.2/72
        maxw=max(maxw,min(len(t)*cw, w-0.08))
    if hh==0: return None
    al=tf.paragraphs[0].alignment
    if al==PP_ALIGN.CENTER: cx0=x+(w-maxw)/2
    elif al==PP_ALIGN.RIGHT: cx0=x+w-0.04-maxw
    else: cx0=x+0.04
    an=tf.vertical_anchor
    if an==MSO_ANCHOR.MIDDLE: cy0=y+(h-hh)/2
    elif an==MSO_ANCHOR.BOTTOM: cy0=y+h-hh-0.03
    else: cy0=y+0.03
    return (cx0,cy0,cx0+maxw,cy0+hh)
def ov(a,b,tol=0.02): return a[0]<b[2]-tol and b[0]<a[2]-tol and a[1]<b[3]-tol and b[1]<a[3]-tol
for si,sl in enumerate(p.slides,1):
    boxes=[]; fills=[]
    for sh in sl.shapes:
        if sh.has_text_frame and sh.text_frame.text.strip():
            if sh.shape_type==17 or sh.shape_type==None or True:
                cb=content_box(sh)
                if cb and sh.shape_type==17: boxes.append((cb,sh.text_frame.text[:30]))
        if sh.shape_type==1 and not (sh.has_text_frame and sh.text_frame.text.strip()):
            try:
                if sh.fill.type==1: fills.append(((sh.left/E,sh.top/E,(sh.left+sh.width)/E,(sh.top+sh.height)/E),str(sh.fill.fore_color.rgb)))
            except Exception: pass
    for i in range(len(boxes)):
        for j in range(i+1,len(boxes)):
            if ov(boxes[i][0],boxes[j][0]): print(f"slide {si}: TEXT OVERLAP '{boxes[i][1]}' x '{boxes[j][1]}'")
    for b,t in boxes:
        for f,c in fills:
            if c in ("F4F3EF","FFFFFF"): continue
            fw=f[2]-f[0]; fh=f[3]-f[1]
            if fw>2 and fh>0.35: continue  # header bands / phase bars intended to hold text
            if ov(b,f,0.01): print(f"slide {si}: text '{t}' over fill {c} {tuple(round(v,2) for v in f)}")
print("qa done")
