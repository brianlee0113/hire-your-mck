import math, json
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR, MSO_AUTO_SIZE
from pptx.enum.dml import MSO_LINE_DASH_STYLE
from pptx.oxml.ns import qn
from lxml import etree

INK="1A1A1A"; INK2="52514E"; MUTED="8A8984"; GRID="E4E2DC"; RULE="C9C7BF"; NAVY="0D366B"
A="2A78D6"; B="EB6834"; BL="F6B79B"; J="1BAF7A"; PASS="1B7F3B"; FAIL="C0392B"; RISK="A86400"; PANEL="F4F3EF"
FONT="Arial"
W=13.333; H=7.5
WARN=[]
def rgb(h): return RGBColor.from_string(h)

def est_lines(text, w_in, pt, bold=False):
    cw = pt/72*(0.565 if bold else 0.53)
    maxc = max(1,int(w_in/cw))
    lines=0
    for para in text.split("\n"):
        words=para.split(" "); cur=0; n=1
        for wd in words:
            L=len(wd)
            if cur==0: cur=L
            elif cur+1+L<=maxc: cur+=1+L
            else: n+=1; cur=L
            while cur>maxc: n+=1; cur-=maxc
        lines+=n
    return lines

class Deck:
    def __init__(s):
        s.p=Presentation(); s.p.slide_width=Inches(W); s.p.slide_height=Inches(H); s.n=0
    def slide(s):
        s.n+=1; sl=s.p.slides.add_slide(s.p.slide_layouts[6]); sl._num=s.n; return sl

def _run_fmt(r, size, bold, color, italic=False):
    f=r.font; f.size=Pt(size); f.bold=bold; f.italic=italic; f.name=FONT; f.color.rgb=rgb(color)

def text(sl, x,y,w,h, paras, size=12, bold=False, color=INK, align="l", anchor="t", bullet=False, space=4, lh=1.0, tag="", check=True, fill=None, inset=0.04):
    """paras: list of items; each item str or list of runs (text, {bold,color,italic,size})"""
    tb=sl.shapes.add_textbox(Inches(x),Inches(y),Inches(w),Inches(h))
    if fill:
        tb.fill.solid(); tb.fill.fore_color.rgb=rgb(fill)
    tf=tb.text_frame; tf.word_wrap=True; tf.auto_size=MSO_AUTO_SIZE.NONE
    tf.margin_left=tf.margin_right=Inches(inset); tf.margin_top=tf.margin_bottom=Inches(0.03)
    tf.vertical_anchor={"t":MSO_ANCHOR.TOP,"m":MSO_ANCHOR.MIDDLE,"b":MSO_ANCHOR.BOTTOM}[anchor]
    if isinstance(paras,str): paras=[paras]
    total_h=0
    for i,item in enumerate(paras):
        p=tf.paragraphs[0] if i==0 else tf.add_paragraph()
        p.alignment={"l":PP_ALIGN.LEFT,"c":PP_ALIGN.CENTER,"r":PP_ALIGN.RIGHT}[align]
        runs=[(item,{})] if isinstance(item,str) else item
        psize=size; plain=""; anyb=bold
        for t,o in runs:
            r=p.add_run(); r.text=t
            sz=o.get("size",size); psize=max(psize,sz) if "size" in o else psize
            b=o.get("bold",bold); anyb=anyb or b
            _run_fmt(r, sz, b, o.get("color",color), o.get("italic",False))
            plain+=t
        if i<len(paras)-1 or True:
            p.space_after=Pt(space)
        if lh!=1.0: p.line_spacing=lh
        ind=0
        if bullet:
            ind=0.16
            pPr=p._p.get_or_add_pPr()
            pPr.set('marL',str(Inches(ind))); pPr.set('indent',str(-Inches(ind)))
            bf=etree.SubElement(pPr,qn('a:buFont')); bf.set('typeface','Arial')
            bc=etree.SubElement(pPr,qn('a:buChar')); bc.set('char','•')
        n=est_lines(plain, w-2*inset-ind, psize, anyb)
        total_h+= n*psize*1.2*lh/72 + space/72
    if check and total_h > h-0.06+space/72*0.5:
        WARN.append(f"slide {sl._num} [{tag or (plain[:40])}] needs {total_h:.2f}in > box {h:.2f}in")
    if x<0 or y<0 or x+w>W+0.001 or y+h>H+0.001: WARN.append(f"slide {sl._num} [{tag}] out of bounds")
    return tb

def rect(sl,x,y,w,h,fill,line=None,lw=0.75,shape=MSO_SHAPE.RECTANGLE):
    s=sl.shapes.add_shape(shape,Inches(x),Inches(y),Inches(max(w,0.001)),Inches(max(h,0.001)))
    s.shadow.inherit=False
    if fill: s.fill.solid(); s.fill.fore_color.rgb=rgb(fill)
    else: s.fill.background()
    if line: s.line.color.rgb=rgb(line); s.line.width=Pt(lw)
    else: s.line.fill.background()
    if s.has_text_frame: s.text_frame.text=""
    return s

def line(sl,x1,y1,x2,y2,color=INK2,w=1.0,dash=None):
    c=sl.shapes.add_connector(MSO_CONNECTOR.STRAIGHT,Inches(x1),Inches(y1),Inches(x2),Inches(y2))
    c.line.color.rgb=rgb(color); c.line.width=Pt(w)
    if dash: c.line.dash_style={"dash":MSO_LINE_DASH_STYLE.DASH,"dot":MSO_LINE_DASH_STYLE.ROUND_DOT}[dash]
    return c

def dot(sl,cx,cy,d,fill,ring="FFFFFF"):
    s=rect(sl,cx-d/2,cy-d/2,d,d,fill,line=ring,lw=1.5,shape=MSO_SHAPE.OVAL); return s

def frame(sl, deck, section, title, source=None, title_size=22):
    text(sl,0.5,0.28,9,0.28,section.upper(),size=10,bold=True,color=NAVY,tag="section")
    text(sl,0.5,0.55,12.3,0.95,title,size=title_size,bold=True,color=INK,anchor="t",lh=0.95,tag="title",space=0)
    line(sl,0.5,1.5,W-0.5,1.5,RULE,0.75)
    if source:
        text(sl,0.5,6.86,8.6,0.52,source,size=8.5,color=MUTED,tag="source",space=0)
    text(sl,W-1.0,6.98,0.5,0.25,str(sl._num),size=9,color=MUTED,align="r",check=False)
    text(sl,9.35,6.98,2.85,0.25,"Onsoo Botanicals · US entry · Board pre-read",size=8.5,color=MUTED,align="r",check=False)

def legend(sl,x,y,items,size=10,gap=0.25):
    cx=x
    for name,col in items:
        rect(sl,cx,y+0.07,0.14,0.14,col)
        wdt=len(name)*size/72*0.53+0.12
        text(sl,cx+0.18,y,wdt,0.28,name,size=size,color=INK2,check=False)
        cx+=0.18+wdt+gap
    return cx

def status(kind):
    return {"pass":("✓ ",PASS),"fail":("✗ ",FAIL),"risk":("◐ ",RISK),"na":("– ",MUTED)}[kind]

def table(sl,x,y,colw,rows,rowh,size=10.5,header_fill=None,first_bold=True,tag="table",valign="m",zebra=False):
    """rows: list of rows; each cell str or list of runs; header row first."""
    nr=len(rows); nc=len(colw)
    if isinstance(rowh,(int,float)): rowh=[rowh]*nr
    gt=sl.shapes.add_table(nr,nc,Inches(x),Inches(y),Inches(sum(colw)),Inches(sum(rowh)))
    tbl=gt.table
    # strip style banding
    tblPr=tbl._tbl.tblPr; tblPr.set('firstRow','0'); tblPr.set('bandRow','0')
    for j,cw in enumerate(colw): tbl.columns[j].width=Inches(cw)
    for i in range(nr):
        tbl.rows[i].height=Inches(rowh[i])
        for j in range(nc):
            c=tbl.cell(i,j); v=rows[i][j]
            c.margin_left=c.margin_right=Inches(0.06); c.margin_top=c.margin_bottom=Inches(0.03)
            c.vertical_anchor=MSO_ANCHOR.MIDDLE if valign=="m" else MSO_ANCHOR.TOP
            c.fill.solid(); c.fill.fore_color.rgb=rgb(header_fill if (i==0 and header_fill) else ("F7F6F3" if zebra and i%2==0 and i>0 else "FFFFFF"))
            tf=c.text_frame; tf.word_wrap=True
            runs=[(v,{})] if isinstance(v,str) else v
            p=tf.paragraphs[0]; plain=""; anyb=False
            for t,o in runs:
                r=p.add_run(); r.text=t; plain+=t
                b=o.get("bold", (i==0) or (j==0 and first_bold)); anyb=anyb or b
                _run_fmt(r,o.get("size",size),b,o.get("color", INK2 if i==0 else INK),o.get("italic",False))
            if j>0 and isinstance(v,str) and v.startswith("$"): pass
            p.alignment=PP_ALIGN.LEFT
            n=est_lines(plain,colw[j]-0.12,size,anyb)
            need=n*size*1.2/72+0.07
            if need>rowh[i]+0.005: WARN.append(f"slide {sl._num} [{tag} r{i}c{j}] cell needs {need:.2f} > {rowh[i]:.2f}: {plain[:30]}")
            # borders: bottom hairline only
            tcPr=c._tc.get_or_add_tcPr()
            for edge in ('a:lnL','a:lnR','a:lnT','a:lnB'):
                ln=etree.SubElement(tcPr,qn(edge))
                if edge=='a:lnB' or (edge=='a:lnT' and i==0):
                    ln.set('w',str(Pt(1.0 if i==0 else 0.5))); sf=etree.SubElement(ln,qn('a:solidFill')); clr=etree.SubElement(sf,qn('a:srgbClr')); clr.set('val', INK2 if i==0 else GRID)
                else:
                    ln.set('w','0'); etree.SubElement(ln,qn('a:noFill'))
            # tcPr children order: lnL lnR lnT lnB ... solidFill must come after borders
            fills=[e for e in tcPr if e.tag==qn('a:solidFill')]
            for f_ in fills: tcPr.remove(f_); tcPr.append(f_)
    if y+sum(rowh)>6.85: WARN.append(f"slide {sl._num} [{tag}] table bottom {y+sum(rowh):.2f} beyond 6.85")
    return gt

class Axis:
    def __init__(s,y0,y1,vmin,vmax): s.y0=y0; s.y1=y1; s.vmin=vmin; s.vmax=vmax
    def __call__(s,v): return s.y1-(v-s.vmin)/(s.vmax-s.vmin)*(s.y1-s.y0)
