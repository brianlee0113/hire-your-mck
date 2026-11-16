"""Approximate PNG preview of python-pptx slides (rects, lines, text boxes, tables) using Calibri."""
import sys, os
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE
from PIL import Image, ImageDraw, ImageFont
FD="/Applications/Microsoft PowerPoint.app/Contents/Resources/DFonts/"
DPI=110; E=914400
_fc={}
def font(pt,b,it=False):
    k=(round(pt*DPI/72),b,it)
    if k not in _fc: _fc[k]=ImageFont.truetype(FD+("Calibriz.ttf" if b and it else "Calibrib.ttf" if b else "Calibrii.ttf" if it else "Calibri.ttf"),k[0])
    return _fc[k]
px=lambda v: int(v/E*DPI)
def col(c):
    try: return '#'+str(c.rgb)
    except Exception: return None
def layout_tf(tf, width):
    """returns list of lines: each line list of (text,font,color); and line heights"""
    lines=[]
    for p in tf.paragraphs:
        runs=[(r.text, font(r.font.size.pt if r.font.size else 18, bool(r.font.bold), bool(r.font.italic)), col(r.font.color) or '#000') for r in p.runs]
        if not runs: lines.append(([],18*DPI/72*1.2,p.alignment)); continue
        cur=[];curw=0;lh=max(f.size for _,f,_ in runs)*1.2
        for t,f,c in runs:
            for wi,word in enumerate(t.split(' ')):
                tok=(' ' if (cur and wi>0) or (cur and wi==0 and t.startswith(' ')) else '')+word
                if wi==0 and cur: tok=word
                w=f.getlength(tok)
                if curw+w>width and cur:
                    lines.append((cur,lh,p.alignment)); cur=[];curw=0; tok=word; w=f.getlength(tok)
                cur.append((tok,f,c)); curw+=w
            # next run continues on same line
        lines.append((cur,lh,p.alignment))
    return lines
def draw_tf(d,tf,x,y,w,h,anchor=None):
    ml,mr,mt,mb=[px(v) if v is not None else px(91440) for v in (tf.margin_left,tf.margin_right,tf.margin_top,tf.margin_bottom)]
    lines=layout_tf(tf,w-ml-mr)
    tot=sum(l[1] for l in lines)
    va=str(tf.vertical_anchor)
    yy=y+mt
    if 'MIDDLE' in va: yy=y+(h-tot)/2
    elif 'BOTTOM' in va: yy=y+h-mb-tot
    for segs,lh,al in lines:
        lw=sum(f.getlength(t) for t,f,_ in segs)
        xx=x+ml
        if al is not None and 'CENTER' in str(al): xx=x+(w-lw)/2
        elif al is not None and 'RIGHT' in str(al): xx=x+w-mr-lw
        for t,f,c in segs:
            d.text((xx,yy+lh*0.1),t,font=f,fill=c); xx+=f.getlength(t)
        yy+=lh
    return tot+mt+mb
def render(path,out):
    p=Presentation(path); os.makedirs(out,exist_ok=True)
    for i,sl in enumerate(p.slides,1):
        im=Image.new('RGB',(px(p.slide_width),px(p.slide_height)),'white'); d=ImageDraw.Draw(im)
        for sh in sl.shapes:
            x,y,w,h=px(sh.left),px(sh.top),px(sh.width),px(sh.height)
            if sh.shape_type==MSO_SHAPE_TYPE.LINE or sh.__class__.__name__=='Connector':
                d.line([(px(sh.begin_x),px(sh.begin_y)),(px(sh.end_x),px(sh.end_y))],fill=col(sh.line.color) or '#000',width=max(1,int(sh.line.width.pt*DPI/72)) if sh.line.width else 1); continue
            if sh.has_table:
                tb=sh.table; yy=y
                for r in tb.rows:
                    hs=[]
                    xx=x
                    for ci,c in enumerate(r.cells):
                        cw=px(tb.columns[ci].width)
                        lines=layout_tf(c.text_frame,cw-px(c.margin_left)-px(c.margin_right))
                        hs.append(sum(l[1] for l in lines)+px(c.margin_top)+px(c.margin_bottom))
                    rh=max(max(hs),px(r.height))
                    xx=x
                    for ci,c in enumerate(r.cells):
                        cw=px(tb.columns[ci].width)
                        fc=col(c.fill.fore_color) if c.fill.type else None
                        d.rectangle([xx,yy,xx+cw,yy+rh],fill=fc or 'white',outline='#bbbbbb')
                        tf=c.text_frame
                        lines=layout_tf(tf,cw-px(c.margin_left)-px(c.margin_right)); tot=sum(l[1] for l in lines)
                        ty=yy+(rh-tot)/2
                        for segs,lh,al in lines:
                            lw=sum(f.getlength(t) for t,f,_ in segs); tx=xx+px(c.margin_left)
                            if al is not None and 'RIGHT' in str(al): tx=xx+cw-px(c.margin_right)-lw
                            if al is not None and 'CENTER' in str(al): tx=xx+(cw-lw)/2
                            for t,f,cc in segs: d.text((tx,ty+lh*0.1),t,font=f,fill=cc); tx+=f.getlength(t)
                            ty+=lh
                        xx+=cw
                    yy+=rh
                if yy>y+h+3: d.rectangle([x,y+h,x+6,yy],fill='red')
                continue
            try:
                if sh.fill.type==1:
                    try: shape=sh.auto_shape_type
                    except Exception: shape=None
                    if shape is not None and 'OVAL' in str(shape): d.ellipse([x,y,x+w,y+h],fill=col(sh.fill.fore_color))
                    else: d.rectangle([x,y,x+w,y+h],fill=col(sh.fill.fore_color))
            except Exception: pass
            if sh.has_text_frame and sh.text_frame.text:
                need=draw_tf(d,sh.text_frame,x,y,w,h)
                if need>h+4: d.rectangle([x+w-4,y,x+w,y+need],fill='red')
        im.save(f"{out}/s{i:02d}.png")
render(sys.argv[1],sys.argv[2])
