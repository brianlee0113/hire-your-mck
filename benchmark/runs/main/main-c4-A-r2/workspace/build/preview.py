"""Rough preview: renders shapes, text (real Arial metrics) and tables; charts as simple bars. Flags overflow."""
import sys, os
from pptx import Presentation
from pptx.util import Emu
from PIL import Image, ImageDraw, ImageFont
FD="/System/Library/Fonts/Supplemental/"
DPI=110
def px(e): return int(Emu(e).inches*DPI)
_fc={}
def font(sz,b):
    k=(round(sz*DPI/72),b)
    if k not in _fc: _fc[k]=ImageFont.truetype(FD+("Arial Bold.ttf" if b else "Arial.ttf"),k[0])
    return _fc[k]
def rgb(c):
    try: return "#"+str(c.rgb)
    except: return None
def layout_tf(tf, wpx):
    """returns list of (line_runs, size, align) and total height px"""
    lines=[]; H=0
    for p in tf.paragraphs:
        runs=[(r.text, r.font.size.pt if r.font.size else 14, bool(r.font.bold), rgb(r.font.color) or "#000000") for r in p.runs]
        if not runs: H+= 14*DPI/72*1.2; continue
        sz=max(r[1] for r in runs)
        pPr=p._p.pPr
        marL=int(pPr.get("marL",0)) if pPr is not None else 0
        ind=px(marL)
        avail=wpx-ind
        # word wrap across runs
        words=[]
        for t,s,b,c in runs:
            for i,wd in enumerate(t.split(" ")):
                words.append((wd,s,b,c, i>0 or (words and words[-1][0]=="" )))
        cur=[];curw=0
        out=[]
        for wd,s,b,c,_ in words:
            f=font(s,b); ww=f.getlength(wd); sp=f.getlength(" ")
            add = ww + (sp if cur else 0)
            if cur and curw+add>avail:
                out.append(cur); cur=[(wd,s,b,c)]; curw=ww
            else:
                cur.append((wd,s,b,c)); curw+=add
        out.append(cur)
        bullet = pPr is not None and pPr.find('{http://schemas.openxmlformats.org/drawingml/2006/main}buChar') is not None
        for k,l in enumerate(out):
            lines.append((l,sz,p.alignment,ind, bullet and k==0))
        lh=sz*DPI/72*1.2
        H+=lh*len(out)+ (p.space_after.pt*DPI/72 if p.space_after else 0)
    return lines,H
def draw_tf(d,tf,x,y,w,h,name,warn):
    ml=px(tf.margin_left); mt=px(tf.margin_top)
    lines,H=layout_tf(tf,w-2*ml)
    if H>h-2*mt+2: warn.append(f"OVERFLOW {name}: need {H/DPI:.2f}in have {(h-2*mt)/DPI:.2f}in :: {tf.text[:60]!r}")
    anchor=tf.vertical_anchor
    yy=y+mt
    if anchor is not None and int(anchor)==3: yy=y+(h-H)/2
    elif anchor is not None and int(anchor)==4: yy=y+h-mt-H
    for l,sz,al,ind,bul in lines:
        lh=sz*DPI/72*1.2
        tw=sum(font(s,b).getlength(wd+" ") for wd,s,b,c in l)
        xx=x+ml+ind
        if al is not None and int(al)==2: xx=x+(w-tw)/2
        elif al is not None and int(al)==3: xx=x+w-ml-tw
        if bul: d.text((xx-px(int(1.5*91440*0.12*10/10*1.37))*0+ -12,yy),"•",font=font(sz,False),fill="#000")
        for wd,s,b,c in l:
            d.text((xx,yy+(sz-s)*DPI/72),wd,font=font(s,b),fill=c); xx+=font(s,b).getlength(wd+" ")
        yy+=lh
def render(path,outdir):
    prs=Presentation(path); W=px(prs.slide_width); Hh=px(prs.slide_height)
    os.makedirs(outdir,exist_ok=True); allw=[]
    for i,sl in enumerate(prs.slides,1):
        im=Image.new("RGB",(W,Hh),"white"); d=ImageDraw.Draw(im); warn=[]
        for sh in sl.shapes:
            x,y,w,h=px(sh.left),px(sh.top),px(sh.width),px(sh.height)
            if x+w>W+2 or y+h>Hh+2: warn.append(f"OFFSLIDE {sh.name}")
            if sh.has_chart if hasattr(sh,'has_chart') else False:
                ch=sh.chart; d.rectangle([x,y,x+w,y+h],outline="#ddd")
                try:
                    cats=list(ch.plots[0].categories); sers=[list(s.values) for s in ch.plots[0].series]
                    n=len(cats); vals=[[v or 0 for v in s] for s in sers]
                    stacked='STACKED' in str(ch.chart_type)
                    horiz='BAR' in str(ch.chart_type)
                    mx=ch.value_axis.maximum_scale or max(sum(c) if stacked else max(c) for c in zip(*vals))*1.1
                    mn=ch.value_axis.minimum_scale or 0
                    for j,c in enumerate(cats):
                        if horiz:
                            cy=y+h*(j+0.5)/n; d.text((x+2,cy-6),str(c)[:28],font=font(9,False),fill="#555")
                            v=vals[0][j]; d.rectangle([x+w*0.35,cy-8,x+w*0.35+(w*0.6)*(v-mn)/(mx-mn),cy+8],fill="#2a78d6")
                        else:
                            cx=x+w*(j+0.5)/n; bot=y+h*0.85; acc=0
                            for k,s in enumerate(vals):
                                v=s[j]
                                if stacked:
                                    y0=bot-(h*0.78)*(acc+v-mn)/(mx-mn); y1=bot-(h*0.78)*max(acc-mn,0)/(mx-mn); acc+=v
                                    if k>0 or 'base' not in str(ch.plots[0].series[0].name): d.rectangle([cx-w/n*0.3,y0,cx+w/n*0.3,y1],fill=["#2a78d6","#0d366b","#2a78d6","#eb6834"][k%4] if 'base' in str(ch.plots[0].series[0].name) else ["#2a78d6","#b5b4ab"][k%2])
                                else:
                                    bw=w/n*0.6/len(vals); bx=cx-w/n*0.3+k*bw
                                    y0=bot-(h*0.78)*(v-mn)/(mx-mn); d.rectangle([bx,y0,bx+bw-2,bot],fill=["#b5b4ab","#2a78d6"][k%2] if len(vals)>1 else "#2a78d6")
                                    d.text((bx,y0-14),f"{v:g}",font=font(9,True),fill="#000")
                            for li,ln in enumerate(str(c).split("\n")): d.text((cx-30,bot+4+li*12),ln,font=font(8.5,False),fill="#555")
                except Exception as e: warn.append(f"chart preview err {e}")
                continue
            if sh.shape_type==19 or getattr(sh,'has_table',False) and sh.has_table:
                tbl=sh.table; yy=y
                for r,row in enumerate(tbl.rows):
                    xx=x; rh=px(row.height)
                    # compute needed height
                    need=rh
                    for c,cell in enumerate(row.cells):
                        cw=px(tbl.columns[c].width); _,H=layout_tf(cell.text_frame,cw-px(cell.margin_left)*2)
                        need=max(need,H+px(cell.margin_top)*2)
                    if need>rh+2: warn.append(f"TABLE row {r} grows {rh/DPI:.2f}->{need/DPI:.2f}in")
                    for c,cell in enumerate(row.cells):
                        cw=px(tbl.columns[c].width)
                        try: f=rgb(cell.fill.fore_color)
                        except: f=None
                        d.rectangle([xx,yy,xx+cw,yy+need],fill=f or "white",outline="#fff")
                        _,H=layout_tf(cell.text_frame,cw-2*px(cell.margin_left))
                        draw_tf(d,cell.text_frame,xx,yy+(need-H)/2-px(cell.margin_top),cw,H+2*px(cell.margin_top)+2,f"cell{r},{c}",[])
                        xx+=cw
                    yy+=need
                if yy>y+h+4: warn.append(f"TABLE height {h/DPI:.2f}->{(yy-y)/DPI:.2f}in bottom at {yy/DPI:.2f}in")
                continue
            try: f=rgb(sh.fill.fore_color) if sh.fill.type==1 else None
            except: f=None
            if sh.shape_type==9 or sh.name.startswith("Connector"):
                d.line([x,y,x+w,y],fill="#ccc",width=1); continue
            if f:
                if 'Oval' in sh.name: d.ellipse([x,y,x+w,y+h],fill=f)
                else: d.rectangle([x,y,x+w,y+h],fill=f)
            if sh.has_text_frame and sh.text_frame.text.strip():
                draw_tf(d,sh.text_frame,x,y,w,h,sh.name,warn)
        im.save(f"{outdir}/s{i:02d}.png")
        for wv in warn: allw.append(f"slide {i}: {wv}")
    print("\n".join(allw) or "no warnings")
render(sys.argv[1],sys.argv[2])
