import sys, json
from pptx import Presentation
from pptx.util import Emu
from pptx.enum.shapes import MSO_SHAPE_TYPE, MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.oxml.ns import qn
prs=Presentation(sys.argv[1]); E=914400/72.0
out=[]
def col(fill):
    try:
        if fill.type==1: return str(fill.fore_color.rgb)
    except Exception: pass
    return None
for sl in prs.slides:
    items=[]
    for sh in sl.shapes:
        it={'x':sh.left/E,'y':sh.top/E,'w':sh.width/E,'h':sh.height/E}
        if sh.shape_type==MSO_SHAPE_TYPE.LINE or sh.__class__.__name__=='Connector':
            it.update(kind='line',x1=sh.begin_x/E,y1=sh.begin_y/E,x2=sh.end_x/E,y2=sh.end_y/E,
                      color=str(sh.line.color.rgb),lw=sh.line.width/12700)
            items.append(it); continue
        kind='rect'
        try:
            ast=sh.auto_shape_type
            if ast==MSO_SHAPE.OVAL: kind='oval'
            elif ast==MSO_SHAPE.ROUNDED_RECTANGLE: kind='rrect'
        except Exception: kind='text'
        it['kind']=kind
        if kind!='text':
            it['fill']=col(sh.fill)
            ln=sh._element.spPr.find(qn('a:ln'))
            it['stroke']=None
            if ln is not None and ln.find(qn('a:noFill')) is None and ln.find(qn('a:solidFill')) is not None:
                it['stroke']=str(sh.line.color.rgb); it['slw']=(sh.line.width or 12700)/12700
        if sh.has_text_frame and sh.text_frame.text.strip():
            tf=sh.text_frame
            anchor={MSO_ANCHOR.MIDDLE:'middle',MSO_ANCHOR.BOTTOM:'bottom'}.get(tf.vertical_anchor,'top')
            paras=[]
            for p in tf.paragraphs:
                pPr=p._p.pPr
                bul=pPr is not None and pPr.find(qn('a:buChar')) is not None
                ind=int(pPr.get('marL','0'))/E if (pPr is not None and pPr.get('marL')) else 0
                runs=[{'t':r.text,'s':r.font.size.pt if r.font.size else 18,'b':bool(r.font.bold),'i':bool(r.font.italic),
                       'c':str(r.font.color.rgb) if r.font.color and r.font.color.type else '000000'} for r in p.runs]
                al={PP_ALIGN.CENTER:'center',PP_ALIGN.RIGHT:'right'}.get(p.alignment,'left')
                sb=p.space_before.pt if p.space_before is not None else 0
                paras.append({'runs':runs,'align':al,'ls':p.line_spacing if isinstance(p.line_spacing,float) else 1.0,'sb':sb,'bullet':bul,'ind':ind})
            it['text']={'paras':paras,'anchor':anchor,'ml':tf.margin_left/E,'mr':tf.margin_right/E,'mt':tf.margin_top/E,'mb':tf.margin_bottom/E}
        items.append(it)
    out.append(items)
json.dump(out,open(sys.argv[2],'w'))
print(len(out))
