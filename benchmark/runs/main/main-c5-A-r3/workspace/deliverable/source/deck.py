import sys; sys.path.insert(0, sys.argv[1])
from engine import *
OUT=sys.argv[2]; PREV=sys.argv[3]
INK='#0b0b0b'; INK2='#52514e'; MUTED='#7d7c77'; RULE='#d9d8d4'; SOFT='#f4f3f0'
BLUE='#2a78d6'; BLUEL='#cde2fb'; RED='#e34948'; REDL='#fbe3e2'; GREY='#b9b8b3'
GOOD='#0ca30c'; CRIT='#d03b3b'
L=0.6; R=W-0.6; CW=R-L
SRC='Source: Parcelbird briefing pack (Nov 2026); Parcelbird analysis. All figures are synthetic benchmark data.'
slides=[]; notes=[]

def new(section,title,src=SRC,note=''):
    s=Slide(); slides.append(s); notes.append(note)
    n=len(slides)
    if section:
        s.text(L,0.32,CW,0.25,section.upper(),size=10.5,color=BLUE,bold=True)
        s.text(L,0.58,CW,1.0,title,size=23,bold=True,color=INK)
        s.line(L,1.62,R,1.62,RULE,0.75)
    s.text(L,7.05,CW-1.0,0.25,src,size=8.5,color=MUTED)
    if n>1: s.text(R-0.6,7.05,0.6,0.25,str(n),size=8.5,color=MUTED,align='r')
    return s

def takeaway(s,txt,y=6.28,h=0.56):
    s.rect(L,y,CW,h,fill=SOFT)
    s.rect(L,y,0.07,h,fill=BLUE)
    s.text(L+0.25,y,CW-0.4,h,txt,size=13.5,bold=True,valign='m')

def table(s,x,y,colw,rows,rowh,size=12,header=True,hdr_fill=None,bold_first_col=True,aligns=None,fills=None,valign='m',pad=0.08):
    cy=y
    for ri,row in enumerate(rows):
        rh=rowh[ri] if isinstance(rowh,list) else rowh
        cx=x
        if fills and fills.get(ri): s.rect(x,cy,sum(colw),rh,fill=fills[ri])
        for ci,cell in enumerate(row):
            al=(aligns[ci] if aligns else 'l')
            if header and ri==0:
                s.text(cx+pad,cy,colw[ci]-2*pad,rh,cell,size=size-1,bold=True,color=INK2,align=al,valign='b')
            else:
                s.text(cx+pad,cy+0.04,colw[ci]-2*pad,rh-0.08,cell,size=size,bold=(bold_first_col and ci==0),align=al,valign=valign)
            cx+=colw[ci]
        cy+=rh
        s.line(x,cy,x+sum(colw),cy,INK if (header and ri==0) else RULE,1.0 if (header and ri==0) else 0.6)
    return cy

def status_fix(s):
    new=[]
    for kind,a in s.items:
        if kind=='text':
            t=a['paras'][0]['runs'][0][0]
            if t[:1] in '✓✗':
                c=GOOD if t[0]=='✓' else CRIT
                a['paras'][0]['runs'][0]=(t[1:].lstrip(),a['paras'][0]['runs'][0][1])
                a['color']=c; a['bold']=True
                new.append(('rect',dict(x=a['x'],y=a['y']+0.06+(a['h']-0.06)/2-0.07 if a['valign']=='m' else a['y']+0.06,w=0.14,h=0.14,fill=c,line=None,lw=0)))
                a['x']+=0.24; a['w']-=0.24
        new.append((kind,a))
    s.items=new

def money(v,dec=2):
    return ('+' if v>0 else '−' if v<0 else '')+'$'+f"{abs(v):,.{dec}f}"

def hbars(s,x,y,w,rows,lo,hi,barh=0.42,gap=0.32,labw=2.6,size=12.5,fmt=money,sub=None):
    """rows: (label, value, sublabel). zero line; positive blue, negative red."""
    px=x+labw; pw=w-labw
    sc=lambda v: px+(v-lo)/(hi-lo)*pw
    zero=sc(0); cy=y
    for i,(lab,v,sl) in enumerate(rows):
        s.text(x,cy-0.05,labw-0.15,barh+0.1,[dict(runs=[(lab,{'bold':True})])]+([dict(runs=sl,size=10)] if sl else []),size=size,valign='m')
        x0,x1=(zero,sc(v)) if v>=0 else (sc(v),zero)
        s.rect(x0,cy,x1-x0,barh,fill=BLUE if v>=0 else RED)
        if v>=0: s.text(x1+0.08,cy,1.2,barh,fmt(v),size=size,bold=True,valign='m')
        else: s.text(x0-1.28,cy,1.2,barh,fmt(v),size=size,bold=True,valign='m',align='r')
        cy+=barh+gap
    s.line(zero,y-0.15,zero,cy-gap+0.15,INK,1.0)
    return cy

# ---------------- 1. Title ----------------
s=new(None,None,src='Prepared for the January 2027 board meeting · Synthetic benchmark data: company, competitors and figures are fictional.')
s.rect(0,0,W,7.5,fill='#ffffff')
s.rect(L,2.2,0.09,2.1,fill=BLUE)
s.text(L+0.35,2.1,11,0.4,'PARCELBIRD · BOARD PAPER',size=12,bold=True,color=BLUE)
s.text(L+0.35,2.5,11.5,1.4,'Should Parcelbird launch its own quick-commerce grocery delivery service in 2027?',size=34,bold=True)
s.text(L+0.35,3.95,11,0.4,'Assessment of the Parcelbird Now proposal and recommendation',size=16,color=INK2)
s.text(L+0.35,5.3,11,0.6,['Decision makers: the board (two founders, two investors)','Basis: Parcelbird briefing pack, November 2026 — no outside research used'],size=12,color=INK2,space=2)

# ---------------- 2. Exec summary ----------------
s=new('Executive summary','Recommendation: do not launch Parcelbird Now in 2027 — grow the software business that already sells into this market')
pts=[
 ('The market is growing, but no one in it makes money. ','US quick-commerce sales grew ~42% a year to $5.1B in 2025, yet both incumbents lose money on every order (Zipcart −$1.90, QuickBasket −$3.40), and QuickBasket closed 4 of its 11 cities.'),
 ('Our own data say a Parcelbird dark store would lose money. ','At the median of the 14 sites that run our software, a store loses $6.17 per order after site costs. Our Columbus pop-up lost $12.57.'),
 ('The plan’s +$2.02 per order needs every input to beat the best site on record: ','average order $45 vs $42, 3.5 vs 3.0 orders per rider-hour, 1,800 vs 1,400 orders a day. Miss the order-value or rider-productivity assumption alone and the store loses money.'),
 ('It fails both of the board’s conditions. ','Even on plan, $2.5M would be left at month 18, about 6 months of runway against a 12-month floor. At benchmark economics, nine stores would lose ~$18M a year, 1.5× our cash.'),
 ('Selling to grocers is the funded way into quick commerce. ','9 late-stage deals are worth $0.86M of ARR, and grocers in the pipeline want fast delivery from their own stores. Scaling to win them costs ~$0.8M a year.'),
]
cy=1.85
for i,(b,t) in enumerate(pts):
    s.text(L,cy,0.4,0.4,str(i+1),size=15,bold=True,color=BLUE)
    s.text(L+0.45,cy+0.02,CW-0.45,0.8,[[(b,{'bold':True}),(t,{})]],size=13.5)
    cy+=0.8
s.rect(L,5.95,CW,0.9,fill=SOFT); s.rect(L,5.95,0.07,0.9,fill=BLUE)
s.text(L+0.25,5.95,CW-0.4,0.9,[[('Decisions asked of the board:  ',{'bold':True}),('(1) decline the nine-store launch; (2) approve ~$0.8M a year for 2 engineers and 2 sales hires; (3) adopt the triggers on page 14 for reopening the operator question, with a review in H1 2028.',{})]],size=13,valign='m')

# ---------------- 3. Founders' claims ----------------
s=new('The founders’ case','Of the founders’ three claims, only the first holds up; our own operating data contradict the other two')
rows=[['Founders’ claim','What the briefing pack shows','Verdict'],
 ['“Quick commerce is growing over 40% a year and nobody owns the Midwest”','Sales grew from $1.8B to $5.1B in 2022–25, a 41.5% compound rate. But growth has not brought profit: Zipcart’s EBITDA is −26% of revenue, QuickBasket’s −46%. The regional player is pulling back (4 of 11 cities closed).','✓  Growth claim holds'],
 ['“Our software already runs other people’s dark stores, so we know how to run them better than anyone”','The 14 benchmark sites already run on Parcelbird software, so our edge is already in their numbers. Their median loses $2.67 per order before any site fixed cost. Our own pop-up did worse than that median on every input.','✗  Not supported'],
 ['“With density, unit economics turn positive: contribution profit per order by month 18”','The +$2.02 per order needs order value, rider productivity and density all above the best of 14 sites, a mix no site has reached. Density explains about $1.75 of the $8.19 gap between plan and benchmark.','✗  Not supported'],
]
y=table(s,L,1.85,[3.6,6.0,2.53],rows,[0.4,1.25,1.25,1.25],size=12.5)
# colour verdict text with status colours (icon + label)
for it in s.items[-12:]:
    pass
takeaway(s,'The opportunity is real; the claim that Parcelbird can run dark stores profitably is not supported by the evidence.')
status_fix(s)

# ---------------- 4. Market ----------------
s=new('Market','Quick commerce is growing ~40% a year, but the established operators lose money on every order')
s.text(L,1.85,5.6,0.3,'US quick-commerce grocery sales (GMV), $B',size=12.5,bold=True)
vals=[1.8,2.6,3.6,5.1]; yrs=['2022','2023','2024','2025']; gr=[None,'+44%','+38%','+42%']
bx=L+0.2; base=5.55; top=2.8; bw=0.8; step=1.35
for i,v in enumerate(vals):
    hh=(base-top)*v/5.1; x=bx+i*step
    s.rect(x,base-hh,bw,hh,fill=BLUE)
    s.text(x-0.2,base-hh-0.32,bw+0.4,0.28,f'{v:.1f}',size=12.5,bold=True,align='c')
    s.text(x-0.2,base+0.06,bw+0.4,0.28,yrs[i],size=11.5,color=INK2,align='c')
    if gr[i]: s.text(x-0.2,base-hh-0.58,bw+0.4,0.26,gr[i],size=10.5,color=INK2,align='c')
s.line(L,base,L+5.6,base,INK,1.0)
s.text(L,5.95,5.6,0.3,'41.5% compound annual growth, 2022–25',size=11,color=INK2)
# right
rx=7.0
s.text(rx,1.85,R-rx,0.3,'Incumbent operators, 2025',size=12.5,bold=True)
rows=[['Operator','Revenue','EBITDA','EBITDA margin','Contribution per order'],
      ['Zipcart (national)','$1,200M','−$310M','−26%','−$1.90'],
      ['QuickBasket (regional)','$210M','−$96M','−46%','−$3.40']]
table(s,rx,2.25,[1.75,0.95,0.9,0.9,1.23],rows,[0.55,0.5,0.5],size=12,aligns=['l','r','r','r','r'])
s.rect(rx,4.15,R-rx,1.35,fill=REDL)
s.text(rx+0.2,4.22,R-rx-0.4,1.2,[[('QuickBasket closed 4 of its 11 cities in 2025. ',{'bold':True}),('The regional incumbent, the closest match to Parcelbird Now, is retreating from cities, not adding them.',{})]],size=12.5,valign='m')
takeaway(s,'Growth is not in question. What matters is whether an operator can make money on each order, and neither incumbent does.')

# ---------------- 5. Scenarios ----------------
s=new('Unit economics','At benchmark economics a Parcelbird dark store would lose about $6 per order; only the founders’ plan makes money')
s.text(L,1.85,7.4,0.3,'Contribution per order after dark-store fixed costs, $',size=12.5,bold=True)
rows=[('Founders’ plan',2.02,[('AOV $45 · 3.5/rider-hr · 1,800/day',{})]),
      ('Best observed*',-1.76,[('AOV $42 · 3.0/rider-hr · 1,400/day',{})]),
      ('Benchmark median',-6.17,[('14 sites · AOV $34 · 2.4 · 900/day',{})]),
      ('Columbus pop-up',-12.57,[('AOV $31 · 2.1/rider-hr · 280/day',{})])]
hbars(s,L,2.4,7.1,rows,-14.5,4.2,barh=0.42,gap=0.3,labw=2.9)
rx=8.2
s.text(rx,1.85,R-rx,0.3,'How each case builds up, $ per order',size=12.5,bold=True)
t=[['','Plan','Best*','Median','Pop-up'],
   ['Order margin before site costs','+3.77','+0.49','−2.67','−6.21'],
   ['Site fixed cost per order','−1.75','−2.25','−3.50','−6.36'],
   ['Contribution per order','+2.02','−1.76','−6.17','−12.57'],
   ['Result per store per year','+$1.3M','−$0.9M','−$2.0M','−$1.3M']]
table(s,rx,2.3,[1.45,0.74,0.74,0.76,0.84],t,[0.35,0.62,0.62,0.62,0.62],size=11.5,aligns=['l','r','r','r','r'])
s.text(L,5.5,CW,0.6,'* The best order value and the best density come from different sites; no site achieved both. Pop-up uses its temporary site cost of $650k a year; at a standard $1.15M store it would be −$17.46. Order margin = goods margin + delivery fee − picking − rider − payment and packaging − promotions.',size=9.5,color=INK2)
takeaway(s,'Even the best composite site loses $1.76 per order. The plan is the only case that makes money, and it is a forecast, not an observation.')

# ---------------- 6. Inputs ----------------
s=new('Unit economics','The plan assumes order value, rider productivity and density above the best of our 14 benchmark sites')
rows=[['Input','Columbus pop-up','Benchmark median','Best observed (range)','Founders’ plan','Plan vs best observed'],
 ['Average order value','$31','$34','$42','$45','7% above best'],
 ['Orders per rider-hour','2.1','2.4','3.0  (1.9–3.0)','3.5','17% above top of range'],
 ['Orders per site per day','280','900','1,400  (400–1,400)','1,800','29% above top of range; 6.4× the pop-up'],
 ['Promotions, % of order value','12%','6%','6%','2%','One-third of the benchmark; one-sixth of the pop-up'],
]
fills={i:None for i in range(5)}
y=table(s,L,1.85,[2.6,1.55,1.65,2.05,1.55,2.73],rows,[0.55,0.58,0.58,0.58,0.58],size=12.5,aligns=['l','r','r','r','r','l'])
# highlight plan column
s.rect(L+2.6+1.55+1.65+2.05,1.85,1.55,y-1.85,fill=None,line=BLUE,lw=1.5)
s.text(L,y+0.1,CW,0.6,'Same in every case: 27% gross margin on goods; $1.99 net delivery fee; $3.10 picking and packing; $17.75 rider cost per hour; $1.30 payment and packaging; $1.15M fixed cost per store per year.',size=11,color=INK2)
s.rect(L,y+0.68,CW,0.72,fill=REDL)
s.text(L+0.2,y+0.68,CW-0.4,0.72,[[('The plan needs all four at once. ',{'bold':True}),('The best order value ($42) and the best density (1,400 a day) were reached at different sites; no site has achieved both, let alone at the plan’s higher levels and with promotions at a third of the norm.',{})]],size=12.5,valign='m')
takeaway(s,'Each plan input is a stretch on its own. Together they describe a store that does not exist anywhere in our data.')

# ---------------- 7. Waterfall ----------------
s=new('Unit economics','Four assumptions carry the plan: set each to the benchmark median and the store goes from +$2.02 to −$6.17 per order')
s.text(L,1.85,7.8,0.3,'Contribution per order after site fixed costs, $ (assumptions replaced in the order shown)',size=12.5,bold=True)
steps=[('Founders’\nplan',2.02,'total'),('Order value\n$45 → $34',-2.75,'d'),('Promotions\n2% → 6%',-1.36,'d'),('Rider-hour\n3.5 → 2.4',-2.32,'d'),('Orders/day\n1,800 → 900',-1.75,'d'),('Benchmark\nmedian',-6.17,'total')]
cx0=L+0.55; colw=1.22; bw=0.78; top=2.55; bot=5.45; vmax=2.8; vmin=-7.0
sy=lambda v: top+(vmax-v)/(vmax-vmin)*(bot-top)
s.line(L+0.35,sy(0),L+0.55+6*colw,sy(0),INK,1.0)
s.text(L-0.1,sy(0)-0.13,0.4,0.26,'0',size=10,color=INK2,align='r')
run=0
for i,(lab,v,k) in enumerate(steps):
    x=cx0+i*colw+(colw-bw)/2
    if k=='total': a,b=0,v; run=v
    else: a,b=run,run+v; run=run+v
    y0,y1=sorted([sy(a),sy(b)])
    s.rect(x,y0,bw,y1-y0,fill=(BLUE if v>0 else RED) if k=='total' else '#ec8a89')
    lbl=money(v)
    if v>0: s.text(x-0.2,y0-0.3,bw+0.4,0.26,lbl,size=12,bold=True,align='c')
    else: s.text(x-0.2,y1+0.04,bw+0.4,0.26,lbl,size=12,bold=True,align='c')
    if i<len(steps)-1:
        s.line(x+bw,sy(run),x+colw,sy(run),GREY,0.75)
    s.text(cx0+i*colw,5.62,colw,0.5,lab.split('\n'),size=10.5,color=INK2,align='c')
rx=8.6
s.rect(rx,1.85,R-rx,4.2,fill=SOFT)
s.text(rx+0.2,1.97,R-rx-0.4,0.55,'If only one assumption misses (others stay at plan)',size=12.5,bold=True)
rows=[['Input set to median','Result'],['Order value $34','−$0.73'],['Rider productivity 2.4','−$0.31'],['Promotions 6%','+$0.22'],['Orders per day 900','+$0.27']]
table(s,rx+0.2,2.6,[2.3,1.33],rows,[0.35,0.45,0.45,0.45,0.45],size=12,aligns=['l','r'])
s.text(rx+0.2,4.85,R-rx-0.4,1.1,'Miss either the order-value or the rider assumption and the store loses money. Miss any two and it loses money whichever two they are.',size=11.5)
takeaway(s,'Density, the founders’ main argument, explains only about a fifth of the gap. Order value and rider productivity matter more.')

# ---------------- 8. What would have to be true ----------------
s=new('Unit economics','Even generous combinations only reach break-even; nothing in the evidence supports +$2 per order')
tiles=[('Best of everything','−$0.08','per order',
        ['Best order value ($42), best rider productivity (3.0) and best density (1,400 a day), plus the plan’s 2% promotions.','No site has combined even the first three. At best, the store breaks even.']),
       ('Zipcart’s playbook','−$1.05','per order',
        ['Take a benchmark-median store, add Zipcart’s $3.99 service fee and cut promotions to 1%, then lose 14% of orders, as Zipcart did.','Zipcart reached +$0.40 only in its densest city and still lost $310M (EBITDA) overall.']),
       ('Density needed','~6,400','orders a day',
        ['At the best composite site’s order margin (+$0.49), a store covers its $1.15M fixed cost only at ~6,400 orders a day, 4.6× the best site.','At the plan’s margin (+$3.77) it would need ~840; the pop-up averaged 280.'])]
tw=(CW-0.5)/3
for i,(h,big,unit,body) in enumerate(tiles):
    x=L+i*(tw+0.25)
    s.rect(x,1.9,tw,4.1,fill=SOFT)
    s.text(x+0.25,2.05,tw-0.5,0.35,h,size=14,bold=True,color=BLUE)
    s.text(x+0.25,2.5,tw-0.5,0.7,big,size=34,bold=True,color=CRIT if big.startswith('−') else INK)
    s.text(x+0.25,3.25,tw-0.5,0.3,unit,size=12,color=INK2)
    s.text(x+0.25,3.7,tw-0.5,2.2,body,size=12.5,space=8)
takeaway(s,'To make +$2.02, Parcelbird would have to run better stores than any its software has ever run, in mid-size Midwest cities.')

# ---------------- 9. Pop-up ----------------
s=new('Columbus pop-up test','Our own Columbus pop-up did worse than the benchmark median on every input and lost $12.57 per order')
s.text(L,1.85,6.8,0.3,'Pop-up economics per order, $ (autumn 2026, six weeks, 11,800 orders)',size=12.5,bold=True)
items=[('Goods margin (27% of $31)',8.37),('Delivery fee, net',1.99),('Picking and packing',-3.10),('Riders ($17.75 ÷ 2.1 orders/hr)',-8.45),('Payment and packaging',-1.30),('Promotions (12% of order)',-3.72),('Order margin',-6.21),('Site fixed cost ($650k ÷ 280/day)',-6.36),('Contribution per order',-12.57)]
lo,hi=-13.5,9.5; px=L+3.0; pw=3.9; sc=lambda v:px+(v-lo)/(hi-lo)*pw; z=sc(0); cy=2.3; bh=0.3; g=0.13
for lab,v in items:
    tot=lab in ('Order margin','Contribution per order')
    s.text(L,cy-0.03,2.9,bh+0.06,lab,size=11.5,bold=tot,valign='m')
    a,b=(z,sc(v)) if v>=0 else (sc(v),z)
    s.rect(a,cy,b-a,bh,fill=(BLUE if v>=0 else RED) if tot or v>=0 else '#ec8a89')
    if v>=0: s.text(b+0.06,cy,0.9,bh,money(v),size=11.5,bold=tot,valign='m')
    else: s.text(a-0.96,cy,0.9,bh,money(v),size=11.5,bold=tot,valign='m',align='r')
    cy+=bh+g
    if lab=='Promotions (12% of order)' or lab=='Site fixed cost ($650k ÷ 280/day)': s.line(L,cy-g/2,px+pw,cy-g/2,RULE,0.6)
s.line(z,2.2,z,cy,INK,1.0)
rx=8.0
s.text(rx,1.85,R-rx,0.3,'What the test does and does not tell us',size=12.5,bold=True)
s.text(rx,2.3,R-rx,3.7,[
  [('Riders alone cost more than the goods earn: ',{'bold':True}),('$8.45 per order against $8.37 of gross margin.',{})],
  [('Density does not rescue it. ',{'bold':True}),('With the pop-up’s order value, promotions and rider productivity, a full store at 900 orders a day would still lose $9.71 per order.',{})],
  [('Growth was real but bought. ',{'bold':True}),('Orders grew 18% a week (about 180 to about 410 a day, our estimate), helped by promotions at 12% of order value and first-order credits.',{})],
  [('The limits: ',{'bold':True}),('one temporary site, six weeks, one city. It is an early read, but it points the same way as the 14 established sites.',{})]],
  size=12,bullet=True,space=9)
takeaway(s,'The one dark store Parcelbird has operated itself did worse than the customers’ stores we benchmark, not better.')

# ---------------- 10. Customers ----------------
s=new('Customers','Demand is shallower than the survey suggests, and at benchmark economics a new customer never pays back')
cw3=3.55
s.rect(L,1.9,cw3,1.95,fill=SOFT)
s.text(L+0.25,2.0,cw3-0.5,0.7,'44%',size=34,bold=True)
s.text(L+0.25,2.75,cw3-0.5,1.0,'of 1,500 Columbus residents aged 25–39 said they would use 15-minute delivery at least weekly (stated intent)',size=11.5)
s.rect(L,4.0,cw3,1.95,fill=REDL)
s.text(L+0.25,4.1,cw3-0.5,0.7,'22%',size=34,bold=True,color=CRIT)
s.text(L+0.25,4.85,cw3-0.5,1.0,'of pop-up customers, acquired at $38 each, were still ordering in month three, about 3.1 times a month (actual behaviour)',size=11.5)
rx=L+cw3+0.45
s.text(rx,1.85,R-rx,0.3,'Months for a customer to pay back the $38 acquisition cost',size=12.5,bold=True)
rows=[['Case','Order margin','Margin per retained customer / month','Payback'],
      ['Founders’ plan','+$3.77','+$11.68','~15 months'],
      ['Best observed composite','+$0.49','+$1.53','~113 months'],
      ['Benchmark median','−$2.67','−$8.26','Never'],
      ['Columbus pop-up','−$6.21','−$19.25','Never']]
table(s,rx,2.25,[2.35,1.35,2.35,1.48],rows,[0.6,0.5,0.5,0.5,0.5],size=12,aligns=['l','r','r','r'])
s.text(rx,5.0,R-rx,0.95,'Method: $38 ÷ 22% retained = $173 to acquire each customer still ordering in month three. Each pays back at 3.1 orders a month × order margin. We leave out orders from customers who churn before month three and costs from customers who lapse later. Survey and retention measure different groups, so the two figures are indicative and not like-for-like.',size=9.5,color=INK2)
takeaway(s,'Four in five customers we pay to acquire are gone by month three. Even on plan, payback is more than a year.')

# ---------------- 11. Capital ----------------
s=new('Capital','Even if everything goes to plan, the launch breaks the 12-month runway floor; at benchmark economics it would burn through our cash')
s.text(L,1.85,5.8,0.3,'Cash, $M: founders’ plan to month 18',size=12.5,bold=True)
bars=[('Cash today',12.0,0,BLUE),('Plan needs to month 18',9.5,2.5,RED),('Left at month 18',2.5,0,BLUE)]
base=5.4; top=2.6; sc=lambda v:(base-top)*v/12.0; bw=1.05; stp=1.8
for i,(lab,v,off,c) in enumerate(bars):
    x=L+0.3+i*stp
    s.rect(x,base-sc(off+v),bw,sc(v),fill=c)
    s.text(x-0.3,base-sc(off+v)-0.32,bw+0.6,0.28,('−' if c==RED else '')+f'${v:.1f}M',size=12.5,bold=True,align='c')
    s.text(x-0.35,base+0.06,bw+0.7,0.5,lab,size=10.5,color=INK2,align='c')
s.line(L,base,L+5.6,base,INK,1.0)
fy=base-sc(4.8)
s.line(L,fy,L+5.6,fy,CRIT,1.5)
s.text(L+3.55,fy-0.55,2.2,0.5,['12-month floor at today’s','burn: $4.8M'],size=10.5,color=CRIT,bold=True,align='r')
rx=7.05
s.text(rx,1.85,R-rx,0.3,'Annual result of nine stores at full volume, $M',size=12.5,bold=True)
rows=[('Founders’ plan',11.93,None),('Best observed*',-8.08,None),('Benchmark median',-18.23,None)]
hbars(s,rx,2.4,R-rx,rows,-26,22,barh=0.45,gap=0.35,labw=2.0,fmt=lambda v:('+' if v>0 else '−')+f'${abs(v):.1f}M')
s.text(rx,4.85,R-rx,1.2,[[('Cash in the bank: $12.0M. ',{'bold':True}),('At median economics, nine stores lose 1.5× that every year, before $5.4M of store capex. The lead investor calls a new round for a delivery operator “unlikely”.',{})]],size=11.5)
s.text(L,5.8,CW,0.45,'Generous reading: treats the $9.5M as all company spending. If it covers Parcelbird Now only, today’s $0.4M monthly burn adds $7.2M over 18 months and cash runs out (−$4.7M). * Composite, as on page 5.',size=9.5,color=INK2)
takeaway(s,'The plan fails the runway test even if it works. If it doesn’t, there is no cash left to fix it.',y=6.35,h=0.55)

# ---------------- 12. Options ----------------
s=new('Options','Of three options, only focusing on the software business meets both of the board’s conditions')
rows=[['Option','Cash required','12-month runway floor','Path to profit within current cash','Verdict'],
 ['A. Founders’ plan: 9 dark stores in Columbus, Indianapolis, Kansas City','$9.5M to month 18 (plan); ~$18M a year of losses at median economics','Breached even on plan: $2.5M left at month 18 vs $4.8M floor','Only if all four key inputs beat the best of 14 sites. Upside if they do: ~+$12M a year','✗  Reject'],
 ['B. One-store pilot in Columbus','$0.6M capex plus ~$2.0M a year of losses at median economics','Breached around month 8 (at today’s $0.4M burn)','Would retest what 14 sites and the pop-up already show; scaling it brings back option A','✗  Not now'],
 ['C. Software focus, adding store-based fast delivery for grocers','~$0.8M a year (2 engineers, 2 sales)','Runway falls from 30 to ~26 months at today’s burn; burn must fall as ARR grows','81% gross margin; 9 late-stage deals add ~$0.70M of gross profit a year, close to the hiring cost','✓  Recommend'],
]
table(s,L,1.85,[3.0,2.35,2.45,2.73,1.6],rows,[0.55,1.05,1.05,1.05],size=12)
status_fix(s)
s.text(L,5.65,CW,0.5,'Runway = cash ÷ monthly burn, holding today’s burn flat. That ignores revenue growth, so it is conservative for option C. Even with no new spending, flat burn would reach the floor in about 18 months, so the core business needs to cut its burn whatever the board decides.',size=10,color=INK2)
takeaway(s,'Option C keeps Parcelbird in the fastest-growing part of grocery without betting the company’s cash on store economics.')

# ---------------- 13. Software ----------------
s=new('The alternative','Grocers want fast delivery from their own stores, and Parcelbird sells the system that runs it')
s.text(L,1.85,6.0,0.3,'ARR, $M: today and potential from the current pipeline',size=12.5,bold=True)
base=5.35; top=2.55; sc=lambda v:(base-top)*v/7.7; bw=1.1; stp=1.85
bars=[('ARR today',[(4.1,BLUE)],'$4.1M'),('+ 9 late-stage deals',[(4.1,BLUE),(0.86,'#86b6ef')],'$5.0M (+21%)'),('+ full pipeline of 37',[(4.1,BLUE),(3.55,'#86b6ef')],'$7.7M (+87%)')]
for i,(lab,segs,tot) in enumerate(bars):
    x=L+0.35+i*stp; acc=0
    for v,c in segs:
        s.rect(x,base-sc(acc+v),bw,sc(v)-(0.02 if acc>0 else 0),fill=c); acc+=v
    s.text(x-0.4,base-sc(acc)-0.32,bw+0.8,0.28,tot,size=12,bold=True,align='c')
    s.text(x-0.4,base+0.06,bw+0.8,0.5,lab,size=10.5,color=INK2,align='c')
s.line(L,base,L+5.9,base,INK,1.0)
s.rect(L+0.35,5.95,0.18,0.18,fill=BLUE); s.text(L+0.6,5.92,1.6,0.25,'Existing ARR',size=10,color=INK2)
s.rect(L+2.1,5.95,0.18,0.18,fill='#86b6ef'); s.text(L+2.35,5.92,3.6,0.25,'New contracts at $96k a year each',size=10,color=INK2)
rx=7.15
s.text(rx,1.85,R-rx,0.3,'Why this is the better route into quick commerce',size=12.5,bold=True)
s.text(rx,2.3,R-rx,3.8,[
 [('It sells into demand that already exists. ',{'bold':True}),('Several grocers in the pipeline want to launch fast delivery from stores they already run, with no dark-store rent or capex for anyone.',{})],
 [('It pays for itself quickly. ',{'bold':True}),('The 9 late-stage deals ($0.86M ARR at 81% gross margin) bring ~$0.70M of gross profit a year, against ~$0.8M a year for the four hires.',{})],
 [('It avoids competing with our customers. ',{'bold':True}),('As an operator, Parcelbird would compete for shoppers with the grocers it wants to sign. This is our inference; the pack does not measure it.',{})],
 [('It keeps the operator option open. ',{'bold':True}),('Our software data on 14+ sites will show early whether store economics improve.',{})]],
 size=12,bullet=True,space=9)
takeaway(s,'Conversion of the late-stage pipeline is the critical path: it funds the hires and brings down burn.')

# ---------------- 14. Recommendation ----------------
s=new('Recommendation','Decisions requested: decline the launch, fund the software plan, and agree what would reopen the operator question')
cols=[('Decide today',[
        'Decline the nine-store Parcelbird Now launch for 2027.',
        'Approve ~$0.8M a year for 2 engineers and 2 sales hires.',
        'Adopt the reopen triggers (right) and a review in H1 2028.']),
      ('Next six months',[
        'Q1: hire; work to close the 9 late-stage deals ($0.86M ARR).',
        'Q1: scope a store-based fast-delivery offer with pipeline grocers as design partners.',
        'Q2: plan to reduce burn so runway stays above 12 months as cash falls.',
        'Every quarter: report contribution per order across benchmark sites to the board.']),
      ('Reopen the operator question only if',[
        'A site on our platform earns positive contribution after site costs for two quarters in a row, with promotions ≤6% of order value.',
        'Rider pay rules in the three cities are settled and costed. Each +$1 an hour costs $0.29–0.42 per order.',
        'Funding for an operator is committed, or the software business alone supports 24+ months of runway.'])]
cw=(CW-0.5)/3
for i,(h,b) in enumerate(cols):
    x=L+i*(cw+0.25)
    s.rect(x,1.9,cw,0.5,fill=BLUE if i==0 else SOFT)
    s.text(x+0.2,1.9,cw-0.4,0.5,h,size=13.5,bold=True,color='#ffffff' if i==0 else INK,valign='m')
    s.text(x+0.2,2.6,cw-0.35,3.5,b,size=12.5,bullet=True,space=10)
takeaway(s,'Quick commerce stays a growth market for Parcelbird, as the company that sells the software, not as an operator losing money on each order.')

# ---------------- 15. Appendix: unit economics ----------------
s=new('Appendix A','Unit economics build-up per order for the four cases')
rows=[['$ per order','Founders’ plan','Best observed*','Benchmark median','Columbus pop-up'],
 ['Goods margin (27% of order value)','+12.15  ($45)','+11.34  ($42)','+9.18  ($34)','+8.37  ($31)'],
 ['Delivery fee, net of payment cost','+1.99','+1.99','+1.99','+1.99'],
 ['Picking and packing labour','−3.10','−3.10','−3.10','−3.10'],
 ['Rider cost ($17.75 per hour ÷ orders per hour)','−5.07  (3.5)','−5.92  (3.0)','−7.40  (2.4)','−8.45  (2.1)'],
 ['Payment processing and packaging','−1.30','−1.30','−1.30','−1.30'],
 ['Promotions and discounts','−0.90  (2%)','−2.52  (6%)','−2.04  (6%)','−3.72  (12%)'],
 ['Order margin before site costs','+3.77','+0.49','−2.67','−6.21'],
 ['Site fixed cost (annual ÷ orders a year)','−1.75  (1,800/day)','−2.25  (1,400/day)','−3.50  (900/day)','−6.36  (280/day, $650k)'],
 ['Contribution per order','+2.02','−1.76','−6.17','−12.57'],
 ['Result per store per year','+$1.33M','−$0.90M','−$2.03M','−$1.28M']]
table(s,L,1.85,[4.2,1.98,1.98,1.98,1.99],rows,[0.42]+[0.37]*10,size=11.5,aligns=['l','r','r','r','r'],fills={7:SOFT,9:SOFT})
s.text(L,6.15,CW,0.6,'* The best order value and the best density come from different sites (the pack’s “best observed site” column); no site achieved both. Fixed cost per order = $1.15M ÷ (orders per day × 365); pop-up uses its $650k annualised temporary-site cost. Figures may not sum because of rounding.',size=9.5,color=INK2)

# ---------------- 16. Appendix: choices & method ----------------
s=new('Appendix B','Judgement calls made in preparing this paper (no clarification was available)')
items=[
 ('Definition of contribution. ','The pack does not define “contribution profit per order”. We show order margin (before store fixed costs) and contribution (after them). The plan is positive on both, so the conclusion does not depend on the choice.'),
 ('Reading of the $9.5M. ','We treat it generously, as all company cash needed to month 18. The stricter reading (Parcelbird Now only, with the existing $0.4M monthly burn on top) leaves −$4.7M.'),
 ('Runway. ','Cash ÷ monthly burn, holding today’s burn flat. This ignores 60% ARR growth, so it understates runway for the software option.'),
 ('Zipcart playbook test. ','We assume the $3.99 fee is all extra revenue (the pack does not say if it is net of payment cost), and hold rider productivity at the median despite 14% fewer orders. Both choices favour the plan.'),
 ('Pop-up growth path. ','The ~180 to ~410 orders a day (week 1 to week 6) assumes steady 18% weekly growth that sums to 11,800 orders. It is our estimate, not reported data.'),
 ('Waterfall order. ','The assumptions affect each other, so step sizes on page 7 depend on the order shown. The one-at-a-time results are shown alongside.'),
 ('One-store pilot. ','The month-8 runway breach assumes today’s $0.4M monthly burn plus a benchmark-median store (−$2.0M a year) and $0.6M capex.'),
 ('Channel conflict. ','The risk of competing with grocer customers is our inference; the pack does not say where pipeline grocers operate.'),
]
s.text(L,1.85,CW,4.9,[[(b,{'bold':True}),(t,{})] for b,t in items],size=12,bullet=True,space=7)

warns=[]
for i,sl in enumerate(slides):
    warns+=render_pil(sl,f'{PREV}/slide{i+1:02d}.png',i+1)
render_pptx(slides,OUT,notes)
print('\n'.join(warns) if warns else 'no overflow warnings'); print(len(slides),'slides')
