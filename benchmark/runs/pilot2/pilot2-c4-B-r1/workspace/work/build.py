import json
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION, XL_LABEL_POSITION, XL_TICK_LABEL_POSITION

M=json.load(open("work/model.json"))
P=M["plans"]; A,B,C,D=[P[k] for k in P]
def r1(x): return f"{x:.1f}"
NAVY=RGBColor(0x0d,0x36,0x6b); BLUE=RGBColor(0x2a,0x78,0xd6); ORANGE=RGBColor(0xeb,0x68,0x34)
INK=RGBColor(0x0b,0x0b,0x0b); INK2=RGBColor(0x52,0x51,0x4e); MUTE=RGBColor(0x8a,0x89,0x86)
GRID=RGBColor(0xd9,0xd8,0xd4); LIGHT=RGBColor(0xf0,0xef,0xec); WHITE=RGBColor(255,255,255)
GOOD=RGBColor(0x00,0x63,0x00); BAD=RGBColor(0xb0,0x2a,0x2a); AMBER=RGBColor(0x9a,0x5b,0x00)
LBLUE=RGBColor(0xe6,0xef,0xfb)

prs=Presentation(); prs.slide_width=Inches(13.333); prs.slide_height=Inches(7.5)
BL=prs.slide_layouts[6]
SECTIONS=["Diagnosis","Pricing power","Value","Plan"]
SRC="Source: Palisade Docs briefing pack (synthetic data); team analysis."
state={"n":0}

def tb(sl,x,y,w,h,text="",size=12,bold=False,color=INK,align=PP_ALIGN.LEFT,anchor=MSO_ANCHOR.TOP,font="Calibri",wrap=True):
    s=sl.shapes.add_textbox(Inches(x),Inches(y),Inches(w),Inches(h)); tf=s.text_frame; tf.word_wrap=wrap
    tf.margin_left=tf.margin_right=Inches(0.04); tf.margin_top=tf.margin_bottom=Inches(0.02); tf.vertical_anchor=anchor
    paras=text if isinstance(text,list) else [text]
    for i,p in enumerate(paras):
        para=tf.paragraphs[0] if i==0 else tf.add_paragraph()
        runs=p if isinstance(p,list) else [(p,{})] if isinstance(p,str) else [p]
        for r in runs:
            if isinstance(r,str): r=(r,{})
            t,o=r; run=para.add_run(); run.text=t
            f=run.font; f.name=font; f.size=Pt(o.get("size",size)); f.bold=o.get("bold",bold)
            f.color.rgb=o.get("color",color); f.italic=o.get("italic",False)
        para.alignment=align
        para.space_after=Pt(o.get("after",4)) if runs else Pt(4)
    return s

def bullets(sl,x,y,w,h,items,size=13,color=INK,gap=6):
    s=sl.shapes.add_textbox(Inches(x),Inches(y),Inches(w),Inches(h)); tf=s.text_frame; tf.word_wrap=True
    tf.margin_left=tf.margin_right=Inches(0.04)
    for i,it in enumerate(items):
        para=tf.paragraphs[0] if i==0 else tf.add_paragraph()
        lvl=0; 
        if isinstance(it,tuple) and it[0]=="sub": lvl=1; it=it[1]
        runs=it if isinstance(it,list) else [it]
        bullet="•  " if lvl==0 else "–  "
        r=para.add_run(); r.text=("      " if lvl else "")+bullet; r.font.size=Pt(size-lvl); r.font.color.rgb=BLUE if lvl==0 else MUTE; r.font.name="Calibri"
        for t in runs:
            if isinstance(t,str): t=(t,{})
            rr=para.add_run(); rr.text=t[0]; rr.font.size=Pt(t[1].get("size",size-lvl)); rr.font.bold=t[1].get("bold",False)
            rr.font.color.rgb=t[1].get("color",color if lvl==0 else INK2); rr.font.name="Calibri"
        para.space_after=Pt(gap)
    return s

def rect(sl,x,y,w,h,fill=LIGHT,line=None,shape=MSO_SHAPE.RECTANGLE):
    s=sl.shapes.add_shape(shape,Inches(x),Inches(y),Inches(w),Inches(h))
    s.fill.solid(); s.fill.fore_color.rgb=fill
    if line is None: s.line.fill.background()
    else: s.line.color.rgb=line; s.line.width=Pt(0.75)
    s.shadow.inherit=False
    return s

def slide(title,section=None,source=SRC):
    sl=prs.slides.add_slide(BL); state["n"]+=1
    if section is not None:
        x=0.5
        for i,sname in enumerate(SECTIONS):
            act=(i+1==section)
            tb(sl,x,0.18,1.6,0.25,f"{i+1}  {sname}",size=9,bold=act,color=NAVY if act else MUTE)
            if act: rect(sl,x+0.04,0.43,1.2,0.03,fill=BLUE)
            x+=1.55
    tb(sl,0.5,0.52,12.3,0.95,title,size=22,bold=True,color=NAVY,anchor=MSO_ANCHOR.TOP)
    ln=sl.shapes.add_connector(1,Inches(0.5),Inches(1.47),Inches(12.83),Inches(1.47)); ln.line.color.rgb=GRID; ln.line.width=Pt(1)
    if source: tb(sl,0.5,6.98,10.8,0.35,source,size=8.5,color=MUTE)
    tb(sl,12.2,6.98,0.65,0.35,str(state["n"]),size=9,color=MUTE,align=PP_ALIGN.RIGHT)
    return sl

def table(sl,x,y,w,h,data,colw=None,size=11,header_fill=NAVY,first_bold=True,rowh=None,fills=None,colors=None,aligns=None):
    rows,cols=len(data),len(data[0])
    gt=sl.shapes.add_table(rows,cols,Inches(x),Inches(y),Inches(w),Inches(h)); t=gt.table
    tblPr=gt._element.graphic.graphicData.tbl.tblPr; tblPr.set("bandRow","0"); tblPr.set("firstRow","0")
    if colw:
        for i,cw in enumerate(colw): t.columns[i].width=Inches(cw)
    for r in range(rows):
        if rowh: t.rows[r].height=Inches(rowh[r] if isinstance(rowh,list) else rowh)
        for c in range(cols):
            cell=t.cell(r,c); v=data[r][c]
            cell.margin_left=cell.margin_right=Inches(0.06); cell.margin_top=cell.margin_bottom=Inches(0.03)
            cell.vertical_anchor=MSO_ANCHOR.MIDDLE
            tf=cell.text_frame; tf.word_wrap=True; tf.text=""
            runs=v if isinstance(v,list) else [v]
            p=tf.paragraphs[0]
            for rv in runs:
                if isinstance(rv,str): rv=(rv,{})
                run=p.add_run(); run.text=rv[0]; run.font.name="Calibri"; run.font.size=Pt(rv[1].get("size",size))
                if r==0:
                    run.font.bold=True; run.font.color.rgb=WHITE
                else:
                    run.font.bold=rv[1].get("bold",first_bold and c==0)
                    col=rv[1].get("color",None)
                    if col is None and colors and colors.get((r,c)): col=colors[(r,c)]
                    run.font.color.rgb=col or INK
            if aligns: p.alignment=aligns[c]
            cell.fill.solid()
            if r==0: cell.fill.fore_color.rgb=header_fill
            elif fills and fills.get((r,c)) is not None: cell.fill.fore_color.rgb=fills[(r,c)]
            elif fills and fills.get(r) is not None: cell.fill.fore_color.rgb=fills[r]
            else: cell.fill.fore_color.rgb=WHITE if r%2 else RGBColor(0xf7,0xf7,0xf5)
    return t

def style_chart(ch,legend=True,size=11,gridlines=False,numfmt='0.0',vmax=None,vmin=None,cat_size=None):
    ch.font.size=Pt(size); ch.font.name="Calibri"; ch.font.color.rgb=INK2
    ch.has_legend=legend
    if legend:
        ch.legend.position=XL_LEGEND_POSITION.TOP; ch.legend.include_in_layout=False; ch.legend.font.size=Pt(size)
    va=ch.value_axis; va.has_major_gridlines=gridlines; va.visible=False
    if vmax is not None: va.maximum_scale=vmax
    if vmin is not None: va.minimum_scale=vmin
    ca=ch.category_axis; ca.format.line.color.rgb=GRID; ca.tick_labels.font.size=Pt(cat_size or size); ca.tick_labels.font.color.rgb=INK
    ca.has_major_gridlines=False
    from pptx.enum.chart import XL_TICK_MARK
    ca.major_tick_mark=XL_TICK_MARK.NONE

def color_series(ch,colors,labels=True,numfmt='0.0',lsize=11,gap=60,overlap=None):
    plot=ch.plots[0]; plot.gap_width=gap
    if overlap is not None: plot.overlap=overlap
    for s,c in zip(plot.series,colors):
        s.format.fill.solid(); s.format.fill.fore_color.rgb=c; s.format.line.color.rgb=WHITE; s.format.line.width=Pt(1.5)
        s.invert_if_negative=False
        if labels:
            s.data_labels.show_value=True; s.data_labels.number_format=numfmt; s.data_labels.number_format_is_linked=False
            s.data_labels.font.size=Pt(lsize); s.data_labels.font.color.rgb=INK; s.data_labels.position=XL_LABEL_POSITION.OUTSIDE_END

def callout(sl,x,y,w,h,head,body,fill=LBLUE,size=12):
    rect(sl,x,y,w,h,fill=fill); rect(sl,x,y,0.06,h,fill=BLUE)
    tb(sl,x+0.18,y+0.1,w-0.3,0.4,head,size=size+1,bold=True,color=NAVY)
    if isinstance(body,list): bullets(sl,x+0.14,y+0.5,w-0.28,h-0.6,body,size=size,gap=5)
    else: tb(sl,x+0.18,y+0.5,w-0.3,h-0.6,body,size=size,color=INK)

def waterfall(sl,x,y,w,h,cats,vals,kinds,numfmt='0.0',vmax=None,size=11):
    # kinds: 'total','down','up'
    base=[];neg=[];pos=[];tot=[];run=0
    for v,k in zip(vals,kinds):
        if k=='total': base.append(0);tot.append(v);neg.append(0);pos.append(0);run=v
        elif k=='down': run-=v; base.append(run);neg.append(v);pos.append(0);tot.append(0)
        else: base.append(run);pos.append(v);neg.append(0);tot.append(0);run+=v
    cd=CategoryChartData(); cd.categories=cats
    cd.add_series("base",base); cd.add_series("Total",tot); cd.add_series("Reduction",neg); cd.add_series("Increase",pos)
    gf=sl.shapes.add_chart(XL_CHART_TYPE.COLUMN_STACKED,Inches(x),Inches(y),Inches(w),Inches(h),cd); ch=gf.chart
    style_chart(ch,legend=False,size=size,vmax=vmax,vmin=0)
    plot=ch.plots[0]; plot.gap_width=45; plot.overlap=100
    cols=[None,NAVY,ORANGE,BLUE]
    for i,s in enumerate(plot.series):
        if i==0: s.format.fill.background(); s.format.line.fill.background(); continue
        s.format.fill.solid(); s.format.fill.fore_color.rgb=cols[i]; s.format.line.fill.background()
    # labels: manual per point
    for i,s in enumerate(plot.series):
        if i==0: continue
        arr=[tot,neg,pos][i-1]
        for j,v in enumerate(arr):
            if v:
                pt=s.points[j]; dl=pt.data_label; dl.has_text_frame=True
                dl.text_frame.text=(("−" if i==2 else "+" if i==3 else "")+format(v,numfmt.replace('0.0','.1f').replace('0.00','.2f')))
                dl.text_frame.paragraphs[0].runs[0].font.size=Pt(size); dl.text_frame.paragraphs[0].runs[0].font.bold=True
                dl.text_frame.paragraphs[0].runs[0].font.color.rgb=WHITE if i==1 else INK
                dl.position=XL_LABEL_POSITION.INSIDE_END if i==1 else XL_LABEL_POSITION.CENTER
    return ch

# ---------------- 1 Title
sl=prs.slides.add_slide(BL); state["n"]+=1
rect(sl,0,0,13.333,7.5,fill=NAVY)
tb(sl,0.8,2.0,11.5,1.6,"Raise prices in 2027 — but only where Palisade has pricing power",size=36,bold=True,color=WHITE)
tb(sl,0.8,3.7,11.5,1.0,"Recommendation on the 2027 pricing plan: should Palisade raise prices while churn is rising, and if so, how?",size=18,color=RGBColor(0xcd,0xe2,0xfb))
tb(sl,0.8,5.4,11.5,0.9,["CEO and leadership team  |  Pricing decision meeting, December 2026","Prepared from the 2026 briefing pack only (synthetic benchmark data); all figures $M ARR unless stated"],size=13,color=RGBColor(0xcd,0xe2,0xfb))

# ---------------- 2 Executive summary
sl=slide("Yes, raise prices in 2027 by segment: +10% for mid-market and enterprise, hold SMB until a test reads out, and retain the promo cohort without a price rise",None)
rect(sl,0.5,1.62,12.33,0.95,fill=LBLUE); rect(sl,0.5,1.62,0.07,0.95,fill=NAVY)
tb(sl,0.72,1.68,12.0,0.85,[[("Answer: ",{"bold":True,"color":NAVY}),("The recommended plan adds about ",{}),("$3.0M of net ARR",{"bold":True}),
   (" in 2027, and up to $0.5M more if the SMB test passes. It gives the same ~$2.0M as the CFO's flat +12% in the downside case and less SMB risk. No pricing option reaches the 15% growth target on its own; new customers must supply the last ~$1.9M.",{})]],size=14,anchor=MSO_ANCHOR.MIDDLE)
pts=[("1","Churn is rising because of one cohort, not because customers broadly reject the price",
      f"Core SMB churn went from 2.0% to only 2.1% a month. The 2,100 customers from the 2025 promotion churn at ~{M['promo_monthly_churn']*100:.1f}% a month and make up {M['promo_share_of_smb_churners']*100:.0f}% of SMB churners. Better onboarding explains only ~30% of their excess churn; the rest is a reaction to the discount ending."),
     ("2","Mid-market and enterprise can take a price rise; SMB has not shown it can",
      "Mid-market: a +10% test had no significant effect on conversion (23.1% vs 23.6%), churn is 0.8% a month and NRR is 112%. Enterprise: 0.2% churn, NRR 118%. SMB: Inkwell's $9 plan has cut Palisade's win rate from 51% to 38%."),
     ("3","The CFO's $10.3M is really ~$4.2M, and the extra $1.2M over our plan depends on SMB",
      f"Contracts not renewing in 2027 and the 7% enterprise cap cut it to $7.6M; churn cuts it to ${B['base']:.1f}M. Our plan gives ${C['base']:.1f}M. If customers are more price-sensitive than we assume, both give ~$2.0M, so the flat 12% buys upside only if Inkwell has not changed SMB behaviour."),
     ("4","Raise in January, gate SMB on a test, and plan for new customers to close the 15% gap",
      f"ARR reaches ~${C['end_arr']:.1f}M (+{C['growth']*100:.1f}%) before new customers; NRR stays ~{C['nrr']*100:.0f}%. Mid-market and enterprise rises start at January renewals. An SMB test runs in Q1–Q2, with an H2 rise only if it passes. Churn triggers can pause any step.")]
y=2.75
for n,h,b in pts:
    rect(sl,0.5,y,0.42,0.42,fill=NAVY,shape=MSO_SHAPE.OVAL); tb(sl,0.5,y+0.03,0.42,0.36,n,size=14,bold=True,color=WHITE,align=PP_ALIGN.CENTER)
    tb(sl,1.07,y-0.04,11.7,0.4,h,size=14,bold=True,color=NAVY)
    tb(sl,1.07,y+0.32,11.7,0.62,b,size=11.5,color=INK2)
    y+=1.04

# ---------------- 3 Hypothesis
sl=slide("We started with 'raise by segment, including a modest SMB rise'; the evidence supported raising mid-market and enterprise, but not SMB yet",None)
tb(sl,0.5,1.58,12.3,0.55,[[("Initial hypothesis (stated before testing): ",{"bold":True,"color":NAVY}),("Raise prices in 2027, but vary the rise by segment: about +10% for mid-market and enterprise and +8% for SMB (the size of the 2023 rise), with no rise for the promo cohort.",{})]],size=12.5)
data=[["What would have to be true","Test against the evidence","Verdict"],
 ["H1. Rising churn does not reflect a general reaction against the price",f"Core SMB churn 2.0% → 2.1%; share citing price 19% → 18% for this group. The promo cohort churns at ~{M['promo_monthly_churn']*100:.1f}%: it is {2100/5900*100:.0f}% of SMB customers but {M['promo_share_of_smb_churners']*100:.0f}% of SMB churners. Mid-market 0.6% → 0.8%, enterprise flat.","Supported"],
 ["H2a. Mid-market and enterprise can absorb a rise without churn wiping out the gain","Mid-market +10% test: conversion 23.1% vs 23.6%, not significant. Churn ≤0.8% a month, NRR 112–118%. Customers stay for integrations and the audit trail. Inkwell not seen in deals over 200 seats. Caveat: the test was on new sign-ups, not renewals.","Supported"],
 ["H2b. Core SMB can absorb +8% as it did in 2023","In 2023, +8% added 0.5pp to monthly churn for 6 months and the rise still paid off. Since then, Inkwell launched at $9 against our $15 and the SMB win rate fell from 51% to 38%. We have no data on how renewing SMB customers react to price after Inkwell.","Not proven: revised to test first"],
 ["H3. The rise is big enough to matter for the 2027 targets",f"It is worth ${C['base']:.1f}–{B['base']:.1f}M net, not $10.3M. NRR stays above 100% in every option. No option reaches +15% without new customers.","Partly: changes the plan"],
 ["H4. The downside can be seen early and limited","Prices change only at renewal, so the effect shows up month by month. Break-even churn levels are known for each segment. A test design worked in 2024.","Supported"]]
fills={}; colors={}
for r,v in [(1,GOOD),(2,GOOD),(3,BAD),(4,AMBER),(5,GOOD)]: colors[(r,2)]=v
t=table(sl,0.5,2.2,12.33,4.2,data,colw=[3.3,7.13,1.9],size=11,rowh=[0.36,0.85,0.85,0.85,0.7,0.6],colors=colors)
for r in range(1,6):
    for run in t.cell(r,2).text_frame.paragraphs[0].runs: run.font.bold=True
tb(sl,0.5,6.48,12.3,0.48,[[("What changed: ",{"bold":True,"color":NAVY}),("The SMB rise moved from 'raise in January' to 'test now, decide by end of Q2'. The value estimate fell from the $10.3M headline to $3–4M net.",{})]],size=11.5)

# ---------------- 4 Diagnosis: churn by group
sl=slide("Churn is rising because of the 2025 promotion cohort: core SMB and enterprise churn are flat, and mid-market is up only 0.2pp",1)
cd=CategoryChartData(); cd.categories=["Core SMB\n(3,800 customers)","Promo cohort\n(2,100 customers)","All SMB\n(5,900)","Mid-market\n(1,350)","Enterprise\n(150)"]
cd.add_series("H1 2025",(2.0,None,2.0,0.6,0.2)); cd.add_series("H1 2026",(2.1,round(M['promo_monthly_churn']*100,1),3.1,0.8,0.2))
gf=sl.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED,Inches(0.5),Inches(1.7),Inches(7.9),Inches(4.6),cd); ch=gf.chart
style_chart(ch,legend=True,size=11,vmax=5.8,cat_size=10.5); color_series(ch,[RGBColor(0x9e,0xc5,0xf4),BLUE],numfmt='0.0"%"',gap=70,overlap=-10)
tb(sl,0.5,1.55,7.9,0.3,"Monthly logo churn, % of customers",size=11,bold=True,color=INK2)
tb(sl,2.2,4.65,1.4,0.5,"joined Feb–Aug 2025",size=9,color=MUTE,align=PP_ALIGN.CENTER)
tb(sl,0.5,6.3,7.9,0.6,f"Promo-cohort churn is derived: (5,900 × 3.1% − 3,800 × 2.1%) ÷ 2,100 = {M['promo_monthly_churn']*100:.1f}% a month. This uses mid-2026 customer counts for H1 rates, so treat it as approximate.",size=9.5,color=INK2)
callout(sl,8.7,1.7,4.13,5.1,"What this means",[
 [("Core SMB churn has barely moved",{"bold":True}),(": 2.0% → 2.1%. The share of these churners citing price fell from 19% to 18%, so Inkwell has not yet hurt retention.",{})],
 [(f"The promo cohort drives the rise",{"bold":True}),(f": {2100/5900*100:.0f}% of SMB customers but {M['promo_share_of_smb_churners']*100:.0f}% of SMB churners. {2100*M['promo_monthly_churn']:.0f} of the {5900*0.031:.0f} SMB customers lost each month come from it.",{})],
 [("The rise should fade",{"bold":True}),(" as this cohort leaves the base. If they churned like other SMB customers, SMB churn would be 2.1%, not 3.1%.",{})],
 [("Mid-market churn is slightly up",{"bold":True}),(" (0.6% → 0.8%) and the pack does not explain it. We watch it as a guardrail metric.",{})]],size=11.5)

# ---------------- 5 Diagnosis: promo decomposition
sl=slide("Better onboarding explains only ~30% of the promo cohort's excess churn; the rest is a reaction to the discount ending, so a further rise would make it worse",1)
cd=CategoryChartData(); cd.categories=["Core SMB","Promo cohort"]
act_gap=(M['pred_promo_from_activation']-0.021)*100; resid=(M['promo_monthly_churn']-M['pred_promo_from_activation'])*100
cd.add_series("Core SMB churn level",(2.1,2.1)); cd.add_series("Explained by low activation",(None,round(act_gap,1))); cd.add_series("Not explained: discount ending / bargain hunters",(None,round(resid,1)))
gf=sl.shapes.add_chart(XL_CHART_TYPE.COLUMN_STACKED,Inches(0.5),Inches(1.85),Inches(5.4),Inches(4.3),cd); ch=gf.chart
style_chart(ch,legend=True,size=10.5,vmax=5.5); ch.legend.font.size=Pt(10)
color_series(ch,[RGBColor(0x9e,0xc5,0xf4),BLUE,ORANGE],numfmt='0.0"%"',gap=55,overlap=100)
for s in ch.plots[0].series: s.data_labels.position=XL_LABEL_POSITION.CENTER
tb(sl,0.5,1.55,5.4,0.3,"Monthly churn, H1 2026, % of customers",size=11,bold=True,color=INK2)
tb(sl,0.5,6.15,5.4,0.8,f"Method: customers who send <5 documents in month 1 churn ~3× as often as those who send more. Fitting the core mix (72% activated) to 2.1% gives activated churn of {M['activated_churn']*100:.2f}%. The promo mix (41% activated) then predicts {M['pred_promo_from_activation']*100:.1f}%; the actual is {M['promo_monthly_churn']*100:.1f}%.",size=9.5,color=INK2)
data=[["Evidence","Core SMB","Promo cohort"],["Sent ≥5 docs in month 1","72%","41%"],["Churners citing price, H1 2026","18%","52%"],["When they leave","Steady","Mostly within 2 months of the discount ending"],["Monthly churn, H1 2026","2.1%",f"~{M['promo_monthly_churn']*100:.1f}%"]]
table(sl,6.2,1.7,6.63,2.3,data,colw=[2.6,1.3,2.73],size=11,rowh=0.44)
callout(sl,6.2,4.2,6.63,2.65,"Implications for the two internal claims",[
 [("CFO, 'onboarding, not price': half right.",{"bold":True}),(" Core customers are not leaving over price, but the promo cohort is: they left when their price doubled.",{})],
 [("Customer Success, 'halve SMB churn in two quarters': not credible.",{"bold":True}),(f" Halving it means 1.55%, below the 2.1% of customers who were onboarded normally. Full activation is worth ~${1.995-1.729:.1f}M of ARR in 2027. Even churn at the core rate would save only ~${1.995-0.989:.1f}M.",{})],
 [("So:",{"bold":True}),(" no rise for the promo cohort, retention work for it, and no more 50%-off acquisition offers.",{})]],size=11)

# ---------------- 6 Pricing power matrix
sl=slide("Every signal of pricing power points the same way: mid-market and enterprise can absorb a rise, SMB is exposed to Inkwell, and the promo cohort cannot take one",2)
data=[["Signal","Mid-market ($41.0M)","Enterprise ($24.0M)","Core SMB ($16.6M)","Promo cohort ($4.4M)"],
 ["Monthly churn trend","0.6% → 0.8%","0.2% → 0.2%","2.0% → 2.1%","~4.9% (new cohort)"],
 ["Net revenue retention","112%","118%","94% (whole SMB segment)","94% (whole SMB segment)"],
 ["Churners citing price","n/a","n/a","18% (19% in 2025)","52%"],
 ["Direct price evidence","+10% test: conversion −0.5pp, not significant","60% of ARR capped at +7%","2023: +8% → +0.5pp churn for 6 months, then net gain","Left when the discount ended"],
 ["Competitive pressure","Inkwell not seen above 200 seats","Inkwell not seen","Inkwell at $9 vs $15; win rate 51% → 38%","Same as core SMB, and more price-driven"],
 ["Why customers stay","Integrations, audit trail","Integrations, audit trail","Not reported","Low activation (41%)"],
 ["Share of ARR that can reprice in 2027","85%","40% (contract terms)","100%","100%"],
 ["Assessment","Strong pricing power","Pricing power, limited by contracts","Unproven since Inkwell","No pricing power"]]
G_=RGBColor(0xe3,0xf1,0xe3); Y_=RGBColor(0xfb,0xf0,0xd9); R_=RGBColor(0xf7,0xe0,0xe0)
fills={(8,1):G_,(8,2):G_,(8,3):Y_,(8,4):R_}
colors={(8,1):GOOD,(8,2):GOOD,(8,3):AMBER,(8,4):BAD}
t=table(sl,0.5,1.65,12.33,5.0,data,colw=[2.35,2.5,2.4,2.62,2.46],size=11,rowh=[0.4,0.5,0.5,0.5,0.72,0.72,0.5,0.5,0.5],fills=fills,colors=colors)
for c in range(1,5):
    for run in t.cell(8,c).text_frame.paragraphs[0].runs: run.font.bold=True
tb(sl,0.5,6.68,12.3,0.3,"Caveat: the mid-market test covered new sign-ups over three months; how existing customers react at renewal is untested. Hence the guardrails on slide 13.",size=10,color=INK2)

# ---------------- 7 Inkwell
sl=slide("Inkwell is hurting SMB customer acquisition, not yet retention; a 12% SMB rise would widen the price gap just when new customers are most needed",2)
cd=CategoryChartData(); cd.categories=["H1 2025","H1 2026"]; cd.add_series("Win rate",(51,38))
gf=sl.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED,Inches(0.5),Inches(1.9),Inches(3.6),Inches(4.0),cd); ch=gf.chart
style_chart(ch,legend=False,size=11,vmax=62,vmin=0); color_series(ch,[BLUE],numfmt='0"%"',gap=80)
ch.plots[0].series[0].points[1].format.fill.solid(); ch.plots[0].series[0].points[1].format.fill.fore_color.rgb=ORANGE
tb(sl,0.5,1.55,3.6,0.4,"Palisade win rate in SMB deals where Inkwell was considered",size=10.5,bold=True,color=INK2)
cd=CategoryChartData(); cd.categories=["Inkwell Starter","Palisade SMB today","Palisade SMB +8%","Palisade SMB +12%"]
cd.add_series("$ per user per month",(9,15,16.2,16.8))
gf=sl.shapes.add_chart(XL_CHART_TYPE.BAR_CLUSTERED,Inches(4.4),Inches(1.9),Inches(4.4),Inches(4.0),cd); ch=gf.chart
style_chart(ch,legend=False,size=11,vmax=20,vmin=0); color_series(ch,[RGBColor(0x9e,0xc5,0xf4)],numfmt='"$"0.0',gap=60)
ch.category_axis.reverse_order=True
pts_=ch.plots[0].series[0].points
pts_[0].format.fill.solid(); pts_[0].format.fill.fore_color.rgb=MUTE
pts_[1].format.fill.solid(); pts_[1].format.fill.fore_color.rgb=BLUE
for i in (2,3): pts_[i].format.fill.solid(); pts_[i].format.fill.fore_color.rgb=ORANGE
tb(sl,4.4,1.55,4.4,0.4,"Entry-plan list price, $ per user per month",size=11,bold=True,color=INK2)
tb(sl,4.4,5.9,4.4,0.6,f"Palisade costs {M['gap_now']:.2f}× Inkwell today, {M['gap_8']:.2f}× after +8% and {M['gap_12']:.2f}× after +12%. Business plan $29 vs Inkwell Pro $24.",size=10,color=INK2)
callout(sl,9.1,1.6,3.73,5.2,"Why this matters",[
 "Inkwell launched in October 2025, yet core SMB churn in H1 2026 was flat and price was cited by only 18% of churners. Existing customers are staying.",
 "The pressure is on winning new customers: Palisade lost 13 points of win rate in Inkwell deals.",
 [("The 15% target needs $0.7–1.9M of net new-customer ARR",{"bold":True}),(" under either price-rise option, and SMB is where Inkwell competes.",{})],
 "How price-sensitive SMB customers now are is the main uncertainty in the pack. Test it before rolling it out."],size=11)

# ---------------- 8 CFO waterfall
el=M['cfo_eligible_gross']; gB=B['gross']
sl=slide(f"The CFO's $10.3M headline shrinks to ${el:.1f}M once renewal timing and contract caps apply, and to ~${B['base']:.1f}M after churn",3)
cats=["CFO headline\n(12% × $86M)","ARR not renewing\nin 2027","Enterprise 7% cap","Eligible to\nreprice in 2027","Customers who\nchurn anyway","Churn caused\nby the rise","Net ARR gain\n(base case)"]
vals=[10.32,M['cfo_lost_not_renewing'],M['cfo_lost_to_cap'],el,el-gB,gB-B['base'],B['base']]
waterfall(sl,0.5,1.75,8.3,4.85,cats,vals,['total','down','down','total','down','down','total'],vmax=11.5,size=11)
tb(sl,0.5,1.55,8.3,0.3,"2027 ARR gain from +12% on all plans at renewal, $M",size=11,bold=True,color=INK2)
data=[["Step","Calculation"],
 ["Not renewing in 2027","12% × (15% of mid-market $41.0M + 60% of enterprise $24.0M) = $2.47M"],
 ["Enterprise cap","Capped 60% of the $9.6M renewing: (12% − 7%) × $5.76M = $0.29M"],
 ["Churn anyway","Customers who leave at their usual rate never pay the higher price. Retained: core SMB 77.5%, promo 54.7%, mid-market 90.8%, enterprise 97.6% (12-month survival at the H1 2026 rate)"],
 ["Churn caused by the rise","Extra ARR lost per point of price: SMB 0.45% (2023), mid-market and enterprise 0.21% (2024 test), promo cohort 2.9× SMB (52% vs 18% cite price)"]]
table(sl,9.0,1.65,3.83,5.0,data,colw=[1.1,2.73],size=9.5,rowh=[0.32,0.9,0.8,1.5,1.48])

# ---------------- 9 Break-even
sl=slide("A rise pays while the churn it causes stays below p/(1+p): mid-market and enterprise clear this easily, core SMB narrowly, the promo cohort not at all",3)
segs=["Mid-market +10%","Enterprise +7% (capped)","Enterprise +10% (uncapped)","Core SMB +8%","Core SMB +12%","Promo cohort +12%"]
ks=M['k_smb'];km=M['k_mm'];pm=52/18
base=[km*10,km*7,km*10,ks*8,ks*12,ks*pm*12]; down=[ks*10,ks*7,ks*10,2*ks*8,2*ks*12,1.5*ks*pm*12]; be=[1/11,.07/1.07,1/11,.08/1.08,.12/1.12,.12/1.12]
cd=CategoryChartData(); cd.categories=segs
cd.add_series("Base estimate",[round(v*100,1) for v in base]); cd.add_series("Downside estimate",[round(v*100,1) for v in down]); cd.add_series("Break-even, p/(1+p)",[round(v*100,1) for v in be])
gf=sl.shapes.add_chart(XL_CHART_TYPE.BAR_CLUSTERED,Inches(0.5),Inches(1.85),Inches(8.3),Inches(4.85),cd); ch=gf.chart
style_chart(ch,legend=True,size=10.5,vmax=26,vmin=0); color_series(ch,[RGBColor(0x86,0xb6,0xef),ORANGE,RGBColor(0x52,0x51,0x4e)],numfmt='0.0"%"',gap=45,overlap=-5,lsize=10)
ch.category_axis.reverse_order=True
tb(sl,0.5,1.55,8.3,0.3,"Extra ARR lost to the rise, % of renewing ARR, compared with break-even",size=11,bold=True,color=INK2)
callout(sl,9.1,1.6,3.73,5.2,"Reading the chart",[
 [("Break-even:",{"bold":True}),(" a rise of p gains p on customers who stay and loses (1+p) on each extra one who leaves. It pays while extra churn < p/(1+p): 9.1% at +10%, 10.7% at +12%.",{})],
 [("Mid-market and enterprise:",{"bold":True}),(" the estimate is 2.1% at +10%, a quarter of break-even. Even at SMB-level sensitivity (4.5%) the rise pays.",{})],
 [("Core SMB:",{"bold":True}),(" fine at 2023 sensitivity. At twice that, the downside if Inkwell has changed behaviour, +12% loses money and +8% roughly breaks even.",{})],
 [("Promo cohort:",{"bold":True}),(" loses money even in the base case.",{})]],size=11)

# ---------------- 10 Options
sl=slide(f"Our plan gives up ~${B['base']-C['base']:.1f}M of base-case upside against the CFO's flat 12%, but does as well in the downside and keeps SMB risk off the table",3)
def f(x): return f"{x:+.1f}" if abs(x)>0.05 else "0.0"
data=[["Option","What changes in 2027","Net ARR gain, base","Net ARR gain, downside","Exit ARR, base (growth)","Main risk"],
 ["A. Hold all prices","Nothing; fix onboarding only","0.0","0.0",f"{A['end_arr']:.1f} (+{A['growth']*100:.1f}%)","Leaves $3M+ of low-risk value unused; $4.9M gap to 15%"],
 ["B. CFO: +12% on every plan","All renewals from January",f"{B['base']:+.1f}",f"{B['down']:+.1f}",f"{B['end_arr']:.1f} (+{B['growth']*100:.1f}%)","SMB part is ~0 to negative in the downside; widens the Inkwell gap (1.87×); speeds promo churn; mid-market rise above the tested 10%"],
 ["C. Recommended: mid-market and enterprise +10% (within caps), hold SMB","Mid-market and enterprise renewals from January",f"{C['base']:+.1f}",f"{C['down']:+.1f}",f"{C['end_arr']:.1f} (+{C['growth']*100:.1f}%)","Mid-market renewal reaction is untested; needs ~$1.9M from new customers"],
 ["C + gate: core SMB +8% from July if the test passes","Adds an SMB rise in H2 if the test passes",f"+{C['base']+D['rows_base']['core']*0.5:.1f} to +{D['base']:.1f}",f"{D['down']:+.1f}",f"{C['end_arr']+D['rows_base']['core']*0.5:.1f}–{D['end_arr']:.1f}","Only goes ahead if renewal churn and Inkwell win rate hold"]]
fills={3:LBLUE,4:LBLUE}
t=table(sl,0.5,1.65,12.33,3.75,data,colw=[2.55,2.35,1.3,1.4,1.6,3.13],size=10.5,rowh=[0.5,0.62,0.85,0.85,0.75],fills=fills,
 aligns=[PP_ALIGN.LEFT,PP_ALIGN.LEFT,PP_ALIGN.CENTER,PP_ALIGN.CENTER,PP_ALIGN.CENTER,PP_ALIGN.LEFT])
bullets(sl,0.5,5.55,12.33,1.4,[
 [("Why C over B: ",{"bold":True}),(f"B's extra ${B['base']-C['base']:.1f}M is SMB rises (+$0.6M net) and mid-market at 12% instead of 10% (+$0.5M). The SMB part pays only if Inkwell has not changed SMB price sensitivity, and both downside cases come to ~$2.0M. Upside at risk is only ~$0.6M once the SMB gate recovers up to $0.5M.",{})],
 [("Downside case: ",{"bold":True}),("mid-market and enterprise as price-sensitive as SMB was in 2023, core SMB twice as sensitive, promo cohort 1.5× its base. Exit ARR = $86.0M + trailing-NRR movement ($8.0M) + net price gain; NRR is 112–114% in every option.",{})]],size=11,gap=4)

# ---------------- 11 Bridge
sl=slide(f"No pricing option reaches 15% on its own: the recommended plan takes ARR to ~${C['end_arr']:.1f}M, and new customers must supply the last ~${C['gap_new_logo']:.1f}M",3)
bn=M['base_nrr_delta']
cats=["ARR mid-2026","SMB at\n94% NRR","Mid-market at\n112% NRR","Enterprise at\n118% NRR","Mid-market\n+10%","Enterprise\n+10% / 7% cap","2027 exit ARR\nbefore new customers","Needed from\nnew customers","15% target"]
vals=[86.0,-bn['SMB'],bn['MM'],bn['ENT'],C['rows_base']['MM'],C['rows_base']['ENT'],C['end_arr'],C['gap_new_logo'],M['target']]
kinds=['total','down','up','up','up','up','total','up','total']
ch=waterfall(sl,0.5,1.75,8.6,4.85,cats,vals,kinds,vmax=104,size=10.5)
ch.value_axis.minimum_scale=70
# recolor price bars orange-ish? keep blue; mark new-logo bar
s=ch.plots[0].series[3]; p=s.points[7]; p.format.fill.solid(); p.format.fill.fore_color.rgb=RGBColor(0xb7,0xd3,0xf6)
tb(sl,0.5,1.55,8.6,0.3,"ARR bridge to December 2027, $M (axis starts at $70M)",size=11,bold=True,color=INK2)
callout(sl,9.35,1.6,3.48,5.2,"What has to be true",[
 [("Trailing NRR holds in 2027",{"bold":True}),(" (SMB 94%, mid-market 112%, enterprise 118%), giving +$8.0M. This is the biggest assumption in the bridge.",{})],
 [(f"Price adds ${C['base']:.1f}M net",{"bold":True}),(" (downside $2.0M); the SMB gate could add up to $0.5M.",{})],
 [(f"New-customer ARR of ≥${C['gap_new_logo']:.1f}M",{"bold":True}),(" net of churn by December. The pack has no pipeline data, so Sales must confirm this.",{})],
 [("For comparison:",{"bold":True}),(f" the CFO's plan reaches ${B['end_arr']:.1f}M and still needs ${B['gap_new_logo']:.1f}M from new customers.",{})]],size=11)

# ---------------- 12 Plan by segment
sl=slide("The 2027 pricing plan: raise where customers value the product most, hold where Inkwell competes, and use retention work for the promo cohort",4)
data=[["Segment","2027 price action","When","Why","Net ARR, base / downside"],
 ["Mid-market\n$41.0M, 85% renews in 2027","+10% list price at renewal; Customer Success leads renewal conversations, focused on integrations and the audit trail","January renewals onwards","The tested level (no significant conversion effect); churn ≤0.8%; NRR 112%. We stop at 10% because 12% is untested",f"{C['rows_base']['MM']:+.1f} / {C['rows_down']['MM']:+.1f}"],
 ["Enterprise\n$24.0M, 40% renews in 2027","Capped contracts (60%): +7%. Uncapped: +10%. Multi-year contracts keep their own terms","At each 2027 renewal","Churn 0.2%, NRR 118%, high switching costs; contracts set the ceiling",f"{C['rows_base']['ENT']:+.1f} / {C['rows_down']['ENT']:+.1f}"],
 ["Core SMB\n$16.6M, 3,800 customers","Hold $15 / $29 in H1. Test +8% on new sign-ups and on a group of renewing customers. Roll out from July only if the test passes","Test Q1–Q2; decide end of Q2","Retention is stable but sensitivity since Inkwell is unknown; the win rate is already down 13 points","0 now; +0.3–0.5 if rolled out"],
 ["Promo cohort\n$4.4M, 2,100 customers","No rise. Activation outreach to the ~59% who are not using the product; offer an annual plan at the standard price","Q1","Price-driven churn (52% cite price); a rise loses money even in the base case","Protects ~$0.3M; not counted"],
 ["New SMB customers","No more 50%-off introductory offers; compete with Inkwell on product and packaging, not discounts","From now","The promo cohort activated at 41% vs 72% and churns 2.3× as often","Supports the new-customer ARR needed"]]
table(sl,0.5,1.65,12.33,5.15,data,colw=[2.05,3.6,1.6,3.48,1.6],size=10.5,rowh=[0.4,1.0,0.85,1.0,0.85,0.75],fills={1:LBLUE,2:LBLUE},
 aligns=[PP_ALIGN.LEFT]*4+[PP_ALIGN.CENTER])

# ---------------- 13 Roadmap & guardrails
sl=slide("Run the plan in stages with set decision points and churn triggers, so a bad reaction shows up in weeks, not at year-end",4)
phases=[("Dec 2026","Decide",["Approve the segmented plan","Fix the board churn metric (appendix)","Sales confirms new-customer ARR plan"]),
        ("Q1 2027","Launch",["Mid-market and enterprise rises from Jan renewals","SMB +8% test starts (new sign-ups + renewal test group)","Promo activation outreach"]),
        ("Q2 2027","Read out",["SMB test results after 3 months","Review mid-market renewal churn","Gate: SMB rise from July, or hold"]),
        ("H2 2027","Scale or stop",["SMB +8% from July if gate passed","Plan the 2028 rise using actual renewal data"])]
x=0.5
for i,(when,name,items) in enumerate(phases):
    rect(sl,x,1.65,2.95,0.62,fill=NAVY if i!=2 else BLUE,shape=MSO_SHAPE.PENTAGON if i<3 else MSO_SHAPE.RECTANGLE)
    tb(sl,x+0.12,1.68,2.7,0.56,[[(when+"  ",{"bold":True,"color":WHITE,"size":13}),(name,{"color":WHITE,"size":12})]],anchor=MSO_ANCHOR.MIDDLE)
    bullets(sl,x,2.37,2.95,1.35,items,size=10.5,gap=2)
    x+=3.1
data=[["Guardrail","Baseline","Trigger","Action if triggered"],
 ["Mid-market monthly logo churn","0.8%","> 1.2% two months in a row (downside case; break-even ≈ 1.55%)","Pause further mid-market rises; offer multi-year price locks to at-risk accounts"],
 ["Mid-market accounts ≤200 seats: churn and Inkwell mentions","Not tracked","Any sustained rise in Inkwell mentions","Consider a lower rise for small mid-market accounts at renewal"],
 ["SMB test: churn in the renewal test group vs control","2.1%","Extra churn > 0.5pp a month (the 2023 level)","Do not roll out the SMB rise in H2"],
 ["SMB win rate vs Inkwell","38%","Falls further in the test group","Do not roll out; review packaging"],
 ["Promo cohort activation (≥5 docs a month)","41% at month 1","No improvement by end of Q1","Stop CS spend on this cohort; accept the expected ~$2.0M churn"]]
table(sl,0.5,3.78,12.33,3.1,data,colw=[3.1,1.25,3.9,4.08],size=10.5,rowh=[0.36,0.6,0.55,0.5,0.45,0.55])

# ---------------- 14 Risks & assumptions
sl=slide("The recommendation holds under the main uncertainties; the biggest open risks are whether NRR holds and whether new customers arrive, not the price rise",4)
data=[["Key assumption or uncertainty","Basis in the evidence","If wrong","Effect on the recommendation"],
 ["Mid-market renewals react like the +10% new sign-up test","2024 test; NRR 112%; integrations make the product sticky","At 2× (SMB-level) sensitivity, gain falls from $2.4M to $1.6M","Still positive; break-even needs 4× the estimate. Guardrail on slide 13"],
 ["Core SMB price sensitivity since Inkwell","Retention flat; win rate down; no post-Inkwell price data","A rise could cost money and new customers","This is why SMB is tested, not rolled out"],
 ["Promo cohort cannot be won back with activation alone","Activation explains ~30% of its excess churn","If activation works better, more of the $4.4M survives","Upside only; not counted in the plan"],
 ["Trailing NRR by segment repeats in 2027","Trailing 12-month NRR","Each point of overall NRR ≈ $0.9M of exit ARR","Affects every option equally; does not change the ranking"],
 ["New-customer ARR of ≥$1.9M net by Dec 2027","Not in the pack","Growth falls short of 15%","Confirm with Sales in December; another reason to protect SMB win rate"],
 ["Capped share of enterprise ARR is the same in the 2027 renewals","The 60% applies to all enterprise ARR","±$0.1M","Immaterial"],
 ["Board metric '1.4% → 2.3%' cannot be reconciled","Undefined; segment data gives 1.7% → 2.6% (by customers)","The board may be misreading the trend","Restate the metric (appendix)"]]
table(sl,0.5,1.65,12.33,5.2,data,colw=[3.2,3.1,2.8,3.23],size=10.5,rowh=[0.38]+[0.68]*7)

# ---------------- 15 Decisions
sl=slide("Four decisions in December secure ~$3.0M of low-risk ARR now and keep the option of an SMB rise from July",4)
dec=[("1","Approve +10% for mid-market and enterprise from January 2027 renewals","Enterprise capped contracts at +7%; multi-year contracts on their own terms. Worth ~$3.0M net ARR ($2.0M downside)."),
     ("2","Hold SMB list prices in H1 and approve the +8% test","New sign-ups plus a renewal test group, run Q1–Q2. Leadership decides on a July rollout at the end of Q2 against the slide 13 gates."),
     ("3","Exclude the promo cohort from any rise and stop 50%-off offers","Fund activation outreach to the ~59% of the cohort who are not using the product; review at end of Q1."),
     ("4","Close the 15% gap and fix the metrics","Sales to commit a plan for ≥$1.9M of net new-customer ARR; Finance to restate the board churn metric by segment and cohort.")]
y=1.75
for n,h,b in dec:
    rect(sl,0.5,y,12.33,1.1,fill=LIGHT)
    rect(sl,0.7,y+0.27,0.56,0.56,fill=NAVY,shape=MSO_SHAPE.OVAL); tb(sl,0.7,y+0.33,0.56,0.45,n,size=16,bold=True,color=WHITE,align=PP_ALIGN.CENTER)
    tb(sl,1.5,y+0.1,11.2,0.45,h,size=15,bold=True,color=NAVY)
    tb(sl,1.5,y+0.55,11.2,0.5,b,size=12,color=INK2)
    y+=1.25

# ---------------- Appendix A1 method
sl=slide("Appendix A1: Net gain = renewing ARR × retention × (price rise − churn caused by the rise), calibrated on the 2023 and 2024 price evidence",None)
bullets(sl,0.5,1.65,6.1,5.2,[
 [("Net gain per segment = R × g × [p − c × (1 + p)]",{"bold":True})],
 ("sub","R = ARR renewing in 2027: SMB 100% of $21.0M; mid-market 85% of $41.0M = $34.85M; enterprise 40% of $24.0M = $9.6M"),
 ("sub","g = share retained over 12 months at the H1 2026 monthly churn rate, (1 − m)^12"),
 ("sub","p = price rise; enterprise capped portion (60%) limited to 7%"),
 ("sub","c = extra share of retained ARR lost because of the rise; break-even when c = p/(1+p)"),
 [("Sensitivity (c per point of price)",{"bold":True})],
 ("sub","SMB 0.45%: 2023 +8% added 0.5pp churn for 6 months and 0.1pp for the next 6 = 3.6% ÷ 8"),
 ("sub","Mid-market and enterprise 0.21%: 2024 test conversion 23.1% vs 23.6% = 2.1% relative ÷ 10"),
 ("sub","Promo cohort: SMB × 2.9 (52% ÷ 18% citing price)"),
 ("sub","Downside: mid-market and enterprise at SMB sensitivity; core SMB ×2; promo ×1.5"),
 [("Simplifications",{"bold":True})],
 ("sub","All repricing measured as a December 2027 run-rate, regardless of renewal month; this overstates revenue booked within 2027"),
 ("sub","Effect of the price rise on new-customer conversion not modelled (no SMB data)")],size=11.5,gap=3)
data=[["Segment","R, $M","g","Base net, $M (plan B / plan C)"],
 ["Core SMB","16.6",f"{M['G']['core']*100:.1f}%",f"{B['rows_base']['core']:+.2f} / 0"],
 ["Promo cohort","4.4",f"{M['G']['promo']*100:.1f}%",f"{B['rows_base']['promo']:+.2f} / 0"],
 ["Mid-market","34.85",f"{M['G']['MM']*100:.1f}%",f"{B['rows_base']['MM']:+.2f} / {C['rows_base']['MM']:+.2f}"],
 ["Enterprise","9.6",f"{M['G']['ENT']*100:.1f}%",f"{B['rows_base']['ENT']:+.2f} / {C['rows_base']['ENT']:+.2f}"],
 ["Total","","",f"{B['base']:+.2f} / {C['base']:+.2f}"]]
table(sl,6.9,1.65,5.93,2.6,data,colw=[1.6,0.9,0.9,2.53],size=11,rowh=0.42,aligns=[PP_ALIGN.LEFT,PP_ALIGN.CENTER,PP_ALIGN.CENTER,PP_ALIGN.CENTER])
data=[["Other derived figures","Value"],
 ["Promo cohort monthly churn",f"{M['promo_monthly_churn']*100:.1f}%"],
 ["Promo share of SMB churners",f"{M['promo_share_of_smb_churners']*100:.0f}%"],
 ["Price-cited share implied by mix (reported 34%)",f"{M['implied_price_cited_all_smb']*100:.0f}% (survey response mix differs)"],
 ["Promo ARR lost in 2027 at current churn",f"${M['promo_loss_unchanged']:.1f}M"],
 ["Overall trailing NRR (ARR-weighted)",f"{M['overall_nrr']*100:.1f}%"]]
table(sl,6.9,4.45,5.93,2.4,data,colw=[3.4,2.53],size=10.5,rowh=0.38)

# ---------------- Appendix A2 dashboard
sl=slide("Appendix A2: The board dashboard's 'monthly churn 1.4% → 2.3%' does not match any weighting of the segment data; restate it",None)
data=[["Way of measuring","H1 2025","H1 2026","Calculation"],
 ["Board dashboard (undefined)","1.4%","2.3%","Not stated"],
 ["Logo churn, weighted by customers",f"{M['cust_wtd_25']:.1f}%",f"{M['cust_wtd_26']:.1f}%","Σ customers × churn ÷ 7,400 (mid-2026 counts)"],
 ["Logo churn, weighted by customers, excluding promo cohort",f"{M['cust_wtd_25_excl_promo']:.1f}%","—","Base without the 2,100 promo customers"],
 ["Churn weighted by ARR",f"{M['arr_wtd_25']:.1f}%",f"{M['arr_wtd_26']:.1f}%","Σ ARR × churn ÷ $86.0M"]]
table(sl,0.5,1.75,12.33,2.4,data,colw=[4.2,1.4,1.4,5.33],size=12,rowh=0.46,aligns=[PP_ALIGN.LEFT,PP_ALIGN.CENTER,PP_ALIGN.CENTER,PP_ALIGN.LEFT])
callout(sl,0.5,4.45,12.33,2.3,"Recommendation",[
 "Report churn separately by segment and by cohort (promo vs core), as both logo churn and gross revenue churn, each with a written definition.",
 "Weighted by customers, SMB dominates the blended figure (80% of customers but 24% of ARR). Weighted by ARR, churn is about 1.2% a month, a much less alarming picture for the board.",
 "Until the metric is restated, the board's '2.3%' should not be used to judge the price decision."],size=12)

prs.save("deliverable/Palisade_2027_Pricing_Recommendation.pptx")
print("slides",len(prs.slides))
