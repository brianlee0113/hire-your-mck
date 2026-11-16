import sys
sys.path.insert(0, sys.argv[0].rsplit('/',2)[0] if False else '')
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.oxml.ns import qn
from lxml import etree
import os
HERE=os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from fontm import TTF
FR=TTF('/System/Library/Fonts/Supplemental/Arial.ttf')
FB=TTF('/System/Library/Fonts/Supplemental/Arial Bold.ttf')

INK='0B0B0B'; SEC='52514E'; MUTED='898781'; GRID='E1E0D9'; AXIS='C3C2B7'; SURF='FFFFFF'
NAVY='13294B'; BLUE='2A78D6'; ORANGE='EB6834'; AQUA='1BAF7A'; LIGHTBLUE='CDE2FB'; PALE='F4F3EF'
GOOD='0CA30C'; WARN='FAB219'; CRIT='D03B3B'; GRAYBAR='C3C2B7'
FONT='Arial'
W,H=13.333,7.5
ML=0.55; CW=W-2*ML
ISSUES=[]

def rgb(h): return RGBColor.from_string(h)

def wrap_lines(text, size, width_in, bold=False):
    f=FB if bold else FR
    maxw=width_in*72
    lines=0
    for para in text.split('\n'):
        words=para.split(' '); cur=''
        n=1
        for w_ in words:
            t=(cur+' '+w_) if cur else w_
            if f.width(t,size)<=maxw: cur=t
            else:
                if cur: n+=1; cur=w_
                else: cur=w_
                if f.width(cur,size)>maxw: ISSUES.append(f'word too long: {w_!r} @{size}pt in {width_in:.2f}in')
        lines+=n
    return lines

class Deck:
    def __init__(s):
        s.prs=Presentation(); s.prs.slide_width=Inches(W); s.prs.slide_height=Inches(H)
        s.n=0
    def slide(s, tracker=None, title=None, source=None, number=True):
        sl=s.prs.slides.add_slide(s.prs.slide_layouts[6]); s.n+=1
        sl._label=f'slide {s.n}'
        if tracker: text(sl, ML, 0.28, 8, 0.25, tracker.upper(), 9, MUTED, bold=True)
        if title:
            text(sl, ML, 0.5, CW, 0.95, title, 22, NAVY, bold=True, anchor='top', spacing=1.08)
            rect(sl, ML, 1.5, CW, 0.02, BLUE)
        if source: text(sl, ML, 6.98, CW-1.0, 0.36, source, 8.5, MUTED, anchor='top')
        if number: text(sl, W-ML-0.6, 7.05, 0.6, 0.25, str(s.n), 9, MUTED, align='right')
        return sl
    def save(s, path): s.prs.save(path)

def _apply_font(run, size, color, bold, italic=False):
    run.font.name=FONT; run.font.size=Pt(size); run.font.bold=bold; run.font.italic=italic
    run.font.color.rgb=rgb(color)

def text(sl, x,y,w,h, content, size=12, color=INK, bold=False, align='left', anchor='top',
         bullet=False, spacing=1.0, para_space=0, check=True, italic=False, margin=0.04):
    """content: str, or list of paragraphs; each paragraph is str or list of runs (text, dict)"""
    tb=sl.shapes.add_textbox(Inches(x),Inches(y),Inches(w),Inches(h))
    tf=tb.text_frame; tf.word_wrap=True
    tf.margin_left=tf.margin_right=Inches(margin); tf.margin_top=tf.margin_bottom=Inches(0.02)
    tf.vertical_anchor={'top':MSO_ANCHOR.TOP,'middle':MSO_ANCHOR.MIDDLE,'bottom':MSO_ANCHOR.BOTTOM}[anchor]
    paras=content if isinstance(content,list) else [content]
    total_h=0
    for i,p in enumerate(paras):
        para=tf.paragraphs[0] if i==0 else tf.add_paragraph()
        runs=p if isinstance(p,list) else [(p,{})]
        if isinstance(p,tuple): runs=[p]
        psize=size; pbul=bullet
        full=''
        anybold=False
        for r in runs:
            t,o=r
            if t=='' and o.get('size'): psize=o['size']; continue
            run=para.add_run(); run.text=t
            rs=o.get('size',size); psize=max(psize,rs) if o.get('size') else psize
            _apply_font(run, rs, o.get('color',color), o.get('bold',bold), o.get('italic',italic))
            full+=t; anybold=anybold or o.get('bold',bold)
        para.alignment={'left':PP_ALIGN.LEFT,'center':PP_ALIGN.CENTER,'right':PP_ALIGN.RIGHT}[align]
        para.line_spacing=spacing
        if para_space and i>0: para.space_before=Pt(para_space)
        indent=0
        if pbul:
            indent=0.2
            pPr=para._p.get_or_add_pPr()
            pPr.set('marL',str(int(Inches(indent)))); pPr.set('indent',str(int(-Inches(indent))))
            for tag in ('a:buFont','a:buChar'):
                pass
            buf=etree.SubElement(pPr,qn('a:buFont')); buf.set('typeface','Arial')
            buc=etree.SubElement(pPr,qn('a:buChar')); buc.set('char','•')
        # estimate
        bold_frac = anybold and all(o.get('bold',bold) for t,o in runs if t)
        nl=wrap_lines(full, psize, w-2*margin-indent-0.02, bold=bold_frac or (anybold and False))
        if anybold and not bold_frac:
            # mixed: estimate using bold for safety on bold part
            nl=max(nl, wrap_lines(full, psize, w-2*margin-indent-0.06, bold=False))
        total_h+= nl*psize*1.2*spacing/72 + (para_space/72 if i>0 else 0)
    if check and total_h > h-0.04+0.005:
        ISSUES.append(f'{sl._label}: text overflow {total_h:.2f}in > box {h:.2f}in :: {str(paras[0])[:60]}')
    if check and (x+w>W+0.01 or y+h>H+0.01):
        ISSUES.append(f'{sl._label}: box off slide :: {str(paras[0])[:40]}')
    return tb

def rect(sl,x,y,w,h,fill,line=None,shape=MSO_SHAPE.RECTANGLE, radius=None):
    s=sl.shapes.add_shape(shape,Inches(x),Inches(y),Inches(max(w,0.001)),Inches(max(h,0.001)))
    if fill is None: s.fill.background()
    else: s.fill.solid(); s.fill.fore_color.rgb=rgb(fill)
    if line: s.line.color.rgb=rgb(line); s.line.width=Pt(0.75)
    else: s.line.fill.background()
    s.shadow.inherit=False
    if radius is not None and shape==MSO_SHAPE.ROUNDED_RECTANGLE:
        s.adjustments[0]=radius
    return s

def line(sl,x1,y1,x2,y2,color,width=1.0,dash=False):
    c=sl.shapes.add_connector(MSO_CONNECTOR.STRAIGHT,Inches(x1),Inches(y1),Inches(x2),Inches(y2))
    c.line.color.rgb=rgb(color); c.line.width=Pt(width)
    if dash:
        ln=c.line._get_or_add_ln(); pd=etree.SubElement(ln,qn('a:prstDash')); pd.set('val','dash')
    ln=c.line._get_or_add_ln(); ln.set('cap','rnd')
    return c

def dot(sl,cx,cy,r,fill,ring=SURF):
    s=sl.shapes.add_shape(MSO_SHAPE.OVAL,Inches(cx-r),Inches(cy-r),Inches(2*r),Inches(2*r))
    s.fill.solid(); s.fill.fore_color.rgb=rgb(fill); s.line.color.rgb=rgb(ring); s.line.width=Pt(1.5)
    s.shadow.inherit=False
    return s

def chip(sl,x,y,status,w=0.72,h=0.26,size=9):
    fill,txt,tc={'pass':(GOOD,'PASS','FFFFFF'),'fail':(CRIT,'FAIL','FFFFFF'),'thin':(WARN,'AT RISK',INK),
                 'na':('E1E0D9','N/A',SEC),'miss':(CRIT,'MISS','FFFFFF')}[status]
    s=rect(sl,x,y,w,h,fill,shape=MSO_SHAPE.ROUNDED_RECTANGLE,radius=0.3)
    tf=s.text_frame; tf.margin_left=tf.margin_right=Inches(0.02); tf.margin_top=tf.margin_bottom=Inches(0)
    p=tf.paragraphs[0]; p.alignment=PP_ALIGN.CENTER; r=p.add_run(); r.text=txt
    _apply_font(r,size,tc,True); tf.vertical_anchor=MSO_ANCHOR.MIDDLE
    return s

class Axis:
    def __init__(s, y0, y1, vmin, vmax):
        s.y0,s.y1,s.vmin,s.vmax=y0,y1,vmin,vmax  # y0 top inch, y1 bottom inch
    def __call__(s,v): return s.y1-(v-s.vmin)/(s.vmax-s.vmin)*(s.y1-s.y0)

def yaxis(sl, ax, x0, x1, ticks, fmt, label_w=0.6, size=9.5, zero=None):
    for t in ticks:
        yy=ax(t)
        line(sl,x0,yy,x1,yy, AXIS if (zero is not None and t==zero) else GRID, 1.0 if (zero is not None and t==zero) else 0.75)
        text(sl,x0-label_w-0.05,yy-0.11,label_w,0.22,fmt(t),size,MUTED,align='right')

def columns(sl, ax, x0, x1, cats, series, colors, bar_w=0.38, gap=0.04, cat_size=10, labels=None, label_fmt=None, label_size=10):
    """series: list of value lists (grouped). labels: set of (si,ci) to label or 'all'"""
    n=len(cats); slot=(x1-x0)/n; k=len(series)
    group_w=k*bar_w+(k-1)*gap
    pos=[]
    for ci,c in enumerate(cats):
        cx=x0+slot*(ci+0.5)
        text(sl,cx-slot/2,ax.y1+0.06,slot,0.25,c,cat_size,SEC,align='center')
        for si,vals in enumerate(series):
            v=vals[ci]
            if v is None: continue
            bx=cx-group_w/2+si*(bar_w+gap)
            top=ax(max(v,0)); bot=ax(min(v,0))
            col=colors[si][ci] if isinstance(colors[si],list) else colors[si]
            rect(sl,bx,top,bar_w,bot-top,col)
            pos.append((si,ci,bx,top,bot))
            if labels=='all' or (labels and (si,ci) in labels):
                text(sl,bx-0.3,top-0.27,bar_w+0.6,0.24,label_fmt(v),label_size,INK,bold=True,align='center')
    return pos

def legend(sl,x,y,items,size=10,sw=0.14,gapx=0.25, kind='box'):
    cx=x
    for name,col in items:
        if kind=='line': line(sl,cx,y+0.11,cx+0.26,y+0.11,col,2.25); off=0.32
        else: rect(sl,cx,y+0.04,sw,sw,col); off=sw+0.07
        wtxt=FR.width(name,size)/72+0.1
        text(sl,cx+off,y-0.01,wtxt+0.05,0.24,name,size,SEC)
        cx+=off+wtxt+gapx
    return cx

def polyline(sl, pts, color, width=2.25, markers=True, r=0.055):
    for (a,b) in zip(pts,pts[1:]): line(sl,a[0],a[1],b[0],b[1],color,width)
    if markers:
        for p in pts: dot(sl,p[0],p[1],r,color)

def table(sl, x, y, col_w, rows, row_h=0.32, size=10.5, header_fill='F4F3EF', bold_first_col=False, aligns=None, row_fills=None, header=True, bold_rows=()):
    """rows: list of lists of str (first row header)"""
    yy=y
    for ri,row in enumerate(rows):
        rh=row_h[ri] if isinstance(row_h,list) else row_h
        if header and ri==0: rect(sl,x,yy,sum(col_w),rh,header_fill)
        elif row_fills and row_fills.get(ri): rect(sl,x,yy,sum(col_w),rh,row_fills[ri])
        xx=x
        for ci,cell in enumerate(row):
            al=(aligns[ci] if aligns else ('left' if ci==0 else 'right'))
            b=(header and ri==0) or (bold_first_col and ci==0) or ri in bold_rows
            col= SEC if (header and ri==0) else INK
            if isinstance(cell,str) and cell.startswith('-') and len(cell)>1 and (cell[1].isdigit() or cell[1]=='$'): cell='−'+cell[1:]
            text(sl,xx+0.04,yy,col_w[ci]-0.08,rh,cell,size,col,bold=b,align=al,anchor='middle')
            xx+=col_w[ci]
        yy+=rh
        line(sl,x,yy,x+sum(col_w),yy,GRID if ri else AXIS,0.75)
    return yy
