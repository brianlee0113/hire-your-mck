# Minimal slide DSL with two backends: python-pptx (deliverable) and PIL (preview / overflow check)
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn
from PIL import Image, ImageDraw, ImageFont
import copy

W, H = 13.333, 7.5
DPI = 150
FONT = "/System/Library/Fonts/Supplemental/Arial.ttf"
FONTB = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
LS = 1.18  # line spacing multiple (exact points in pptx)

def hexrgb(h): h=h.lstrip('#'); return tuple(int(h[i:i+2],16) for i in (0,2,4))

class Slide:
    def __init__(self): self.items=[]
    def rect(self,x,y,w,h,fill=None,line=None,lw=0.75):
        self.items.append(('rect',dict(x=x,y=y,w=w,h=h,fill=fill,line=line,lw=lw)))
    def line(self,x1,y1,x2,y2,color='#000000',lw=1.0,dash=False):
        self.items.append(('line',dict(x1=x1,y1=y1,x2=x2,y2=y2,color=color,lw=lw,dash=dash)))
    def text(self,x,y,w,h,paras,size=14,color='#0b0b0b',bold=False,align='l',valign='t',space=0,bullet=False,indent=0.22,name=None):
        # paras: str | list of paragraphs; paragraph: str | list of (text, style dict) runs | dict(runs=..., bullet=..., size=..., space=...)
        if isinstance(paras,str): paras=[paras]
        norm=[]
        for p in paras:
            if isinstance(p,dict): d=dict(p)
            else: d=dict(runs=p)
            if isinstance(d['runs'],str): d['runs']=[(d['runs'],{})]
            d.setdefault('bullet',bullet); d.setdefault('size',size); d.setdefault('space',space)
            norm.append(d)
        self.items.append(('text',dict(x=x,y=y,w=w,h=h,paras=norm,color=color,bold=bold,align=align,valign=valign,indent=indent,name=name)))

# ---------- PIL backend ----------
_fc={}
def font(size_pt,bold):
    k=(round(size_pt*DPI/72),bold)
    if k not in _fc: _fc[k]=ImageFont.truetype(FONTB if bold else FONT,k[0])
    return _fc[k]

def layout_para(d,wpx,defcolor,defbold):
    """returns list of lines; each line list of (text,font,color) segments, plus line height px"""
    size=d['size']; toks=[]
    for txt,st in d['runs']:
        b=st.get('bold',defbold); c=st.get('color',defcolor); s=st.get('size',size)
        f=font(s,b)
        parts=txt.replace('\n',' \n ').split(' ')
        for i,pw in enumerate(parts):
            if pw=='\n': toks.append(('\n',f,c)); continue
            toks.append((pw+(' ' if i<len(parts)-1 else ''),f,c))
    lines=[[]]; cur=0; warn=[]
    for t,f,c in toks:
        if t=='\n': lines.append([]); cur=0; continue
        if t=='': continue
        tw=f.getlength(t); twn=f.getlength(t.rstrip())
        if cur+twn>wpx and lines[-1]:
            lines.append([]); cur=0
        if twn>wpx: warn.append('word too wide: '+t)
        lines[-1].append((t,f,c)); cur+=tw
    lh=size*LS*DPI/72
    return lines,lh,warn

def render_pil(slide,path,num):
    im=Image.new('RGB',(int(W*DPI),int(H*DPI)),'white'); dr=ImageDraw.Draw(im); warns=[]
    P=lambda v:v*DPI
    for kind,a in slide.items:
        if kind=='rect':
            dr.rectangle([P(a['x']),P(a['y']),P(a['x']+a['w']),P(a['y']+a['h'])],fill=hexrgb(a['fill']) if a['fill'] else None,
                         outline=hexrgb(a['line']) if a['line'] else None,width=max(1,int(a['lw']*DPI/72)) if a['line'] else 0)
        elif kind=='line':
            dr.line([P(a['x1']),P(a['y1']),P(a['x2']),P(a['y2'])],fill=hexrgb(a['color']),width=max(1,int(a['lw']*DPI/72)))
        elif kind=='text':
            x,y,w,h=P(a['x']),P(a['y']),P(a['w']),P(a['h'])
            blocks=[]; total=0
            for i,d in enumerate(a['paras']):
                ind=P(a['indent']) if d['bullet'] else 0
                lines,lh,wr=layout_para(d,w-ind,a['color'],a['bold']); warns+=wr
                sp=P(d['space']/72) if i>0 else 0
                blocks.append((d,lines,lh,ind,sp)); total+=sp+lh*len(lines)
            if total>h+1: warns.append(f"OVERFLOW slide{num} '{a['paras'][0]['runs'][0][0][:40]}' need {total/DPI:.2f}in have {a['h']:.2f}in")
            cy=y if a['valign']=='t' else (y+(h-total)/2 if a['valign']=='m' else y+h-total)
            for d,lines,lh,ind,sp in blocks:
                cy+=sp
                for li,ln in enumerate(lines):
                    lw_=sum(f.getlength(t) for t,f,c in ln) - (ln[-1][1].getlength(' ') if ln and ln[-1][0].endswith(' ') else 0)
                    if a['align']=='c': cx=x+ind+(w-ind-lw_)/2
                    elif a['align']=='r': cx=x+w-lw_
                    else: cx=x+ind
                    if d['bullet'] and li==0:
                        bf=font(d['size'],False); dr.text((x,cy+lh*0.08),'•',font=bf,fill=hexrgb(a['color']))
                    for t,f,c in ln:
                        dr.text((cx,cy+lh*0.08),t,font=f,fill=hexrgb(c)); cx+=f.getlength(t)
                    cy+=lh
    im.save(path); return warns

# ---------- PPTX backend ----------
AL={'l':PP_ALIGN.LEFT,'c':PP_ALIGN.CENTER,'r':PP_ALIGN.RIGHT}
VA={'t':MSO_ANCHOR.TOP,'m':MSO_ANCHOR.MIDDLE,'b':MSO_ANCHOR.BOTTOM}
def render_pptx(slides,path,notes=None):
    prs=Presentation(); prs.slide_width=Inches(W); prs.slide_height=Inches(H)
    blank=prs.slide_layouts[6]
    for si,s in enumerate(slides):
        sl=prs.slides.add_slide(blank)
        for kind,a in s.items:
            if kind=='rect':
                sh=sl.shapes.add_shape(MSO_SHAPE.RECTANGLE,Inches(a['x']),Inches(a['y']),Inches(a['w']),Inches(a['h']))
                sh.shadow.inherit=False
                if a['fill']: sh.fill.solid(); sh.fill.fore_color.rgb=RGBColor(*hexrgb(a['fill']))
                else: sh.fill.background()
                if a['line']: sh.line.color.rgb=RGBColor(*hexrgb(a['line'])); sh.line.width=Pt(a['lw'])
                else: sh.line.fill.background()
            elif kind=='line':
                c=sl.shapes.add_connector(1,Inches(a['x1']),Inches(a['y1']),Inches(a['x2']),Inches(a['y2']))
                c.line.color.rgb=RGBColor(*hexrgb(a['color'])); c.line.width=Pt(a['lw'])
            elif kind=='text':
                tb=sl.shapes.add_textbox(Inches(a['x']),Inches(a['y']),Inches(a['w']),Inches(a['h']))
                tf=tb.text_frame; tf.word_wrap=True; tf.auto_size=None
                tf.margin_left=tf.margin_right=tf.margin_top=tf.margin_bottom=0
                tf.vertical_anchor=VA[a['valign']]
                if a['name']: tb.name=a['name']
                for i,d in enumerate(a['paras']):
                    p=tf.paragraphs[0] if i==0 else tf.add_paragraph()
                    p.alignment=AL[a['align']]; p.line_spacing=Pt(d['size']*LS)
                    if i>0 and d['space']: p.space_before=Pt(d['space'])
                    if d['bullet']:
                        pPr=p._p.get_or_add_pPr(); ind=int(Inches(a['indent']))
                        pPr.set('marL',str(ind)); pPr.set('indent',str(-ind))
                        bu=pPr.makeelement(qn('a:buChar'),{'char':'•'}); pPr.append(bu)
                    for txt,st in d['runs']:
                        r=p.add_run(); r.text=txt
                        r.font.name='Arial'; r.font.size=Pt(st.get('size',d['size']))
                        r.font.bold=st.get('bold',a['bold']); r.font.color.rgb=RGBColor(*hexrgb(st.get('color',a['color'])))
        if notes and notes[si]:
            sl.notes_slide.notes_text_frame.text=notes[si]
    prs.save(path)
