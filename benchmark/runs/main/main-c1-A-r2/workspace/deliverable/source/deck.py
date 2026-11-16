import sys, os, io, contextlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *
with contextlib.redirect_stdout(io.StringIO()):
    import model as M

OUT=sys.argv[1]
d=Deck()
SRC='Source: Onsoo briefing pack (fictional benchmark data); team analysis.'
def m(v,dp=1): return ('−' if v<0 else '')+f'${abs(v):.{dp}f}M'
A=M.A(); B=M.B(); J=M.J()
mA=M.margins(A); mB=M.margins(B); mJ=M.margins(J)
A32=M.A(0.32); A28=M.A(0.28)
def peak(r): return min(0,min(x['cum'] for x in r))

# ---------- 1 Title
sl=d.slide(number=False)
rect(sl,0,0,W,H,NAVY)
rect(sl,ML,2.35,1.2,0.05,BLUE)
text(sl,ML,1.55,9,0.5,'ONSOO BOTANICALS · BOARD DISCUSSION DOCUMENT',11,'B7D3F6',bold=True)
text(sl,ML,2.6,11.5,1.6,'US market entry: enter in 2027 through Amazon, and earn the move into specialty retail',36,'FFFFFF',bold=True,spacing=1.05)
text(sl,ML,4.45,11,0.8,'Should Onsoo enter the US market in 2027, and if so, by which route?\nPrepared for CEO Park Ji-won and the board, for the March 2027 board meeting',15,'CDE2FB',spacing=1.15)
text(sl,ML,6.6,12,0.5,'Draft prepared November 2026 · Based solely on the planning team briefing pack. All company, competitor and market figures in the pack are fictional benchmark data.',10,'9EC5F4')

# ---------- 2 Exec summary
sl=d.slide('Executive summary','Recommendation: enter the US in 2027 through Amazon (Option A); turn down the 600-door retail launch and hold the Japan scale-up', SRC)
rows=[
 ('Enter the US in 2027',
  'US K-beauty skincare is $3.6B and has grown 17% a year since 2021, against 5% for all facial skincare. 41% of it sells on Amazon, where Onsoo\'s six-month pilot already sells 14,000 units a month at 4.5 stars.'),
 ('Lead with Amazon (A)',
  f'On the planning team\'s own inputs, A\'s cumulative cash bottoms out at {m(peak(A))}, recovers to {m(A[-1]["cum"])} by 2030, and keeps group margin at 9.5% or above. It is the only US route that passes the board\'s money tests.'),
 ('Reject retail-led (B)',
  f'B burns {m(-B[-1]["cum"])} by 2030 and never pays back. It also cuts group margin to {mB[0]*100:.1f}% in 2027. Its two key inputs do not hold: it assumes 4.5 units per door per week where brands at Onsoo\'s awareness sell 2.6, and its 1.3× Amazon "halo" rests on a correlation.'),
 ('Hold Japan (J)',
  'J is safe but small: $7M of extra revenue and $1.8M of cash by 2030, in a market growing 1.5% a year. Management can run only one launch in 2027, and the US is the larger prize.'),
 ('Accept two trade-offs',
  'No route within the cash limits reaches $40M by 2030: A reaches $26M, which points to about 2032 for $40M. And payback by 2030 holds only if Amazon ad cost stays at or below ~28.5% of sales. The plan assumes 25%, the pilot ran at 28%, and scaling brands run at 32%.'),
 ('Decide in March',
  'Approve A with a $4M cash envelope (well inside the $18M cap) and an ad-cost guardrail. Set the retail trigger at 20% aided awareness, not 15%, and restate the US ambition as $40M by 2032.'),
]
y=1.72
for i,(h_,b_) in enumerate(rows):
    rh=0.84
    rect(sl,ML,y+0.06,0.06,rh-0.16,BLUE if i<4 else (WARN if i==4 else NAVY))
    text(sl,ML+0.2,y,2.6,rh,h_,13.5,NAVY,bold=True,anchor='middle')
    text(sl,ML+2.9,y,CW-2.9,rh,b_,12.5,INK,anchor='middle',spacing=1.05)
    if i<5: line(sl,ML+0.2,y+rh,ML+CW,y+rh,GRID,0.75)
    y+=rh+0.02

# ---------- 3 Scorecard
sl=d.slide('The answer on one page','Only the Amazon-led route passes the board\'s investment, payback and margin tests; no route reaches $40M of US revenue by 2030',
 SRC+' Planning-team inputs as given (ACoS 25%, duty 15%, retail 4.5 units/door/week, 1.3× halo). Pre-tax, undiscounted cash; inventory at four months of landed cost.')
cols=[('A · Amazon-led',BLUE),('B · Retail-led (600 doors)',ORANGE),('J · Japan scale-up',AQUA)]
x0=ML; cw0=3.05; cwi=(CW-cw0)/3
y=1.75
rect(sl,x0,y,CW,0.42,PALE)
text(sl,x0+0.1,y,cw0,0.42,'Board test',11,SEC,bold=True,anchor='middle')
for i,(n_,c_) in enumerate(cols):
    xx=x0+cw0+i*cwi
    rect(sl,xx+0.1,y+0.14,0.14,0.14,c_)
    text(sl,xx+0.3,y,cwi-0.35,0.42,n_,12,INK,bold=True,anchor='middle')
y+=0.42
tests=[
 ('Ambition','"On the way to $40M US revenue by 2030"',
   [('miss',f'${A[-1]["rev"]:.1f}M in 2030 (66% of target)'),('miss',f'${B[-1]["rev"]:.1f}M in 2030, on optimistic inputs'),('miss','No US revenue; +$7.0M in Japan')]),
 ('Investment cap','Peak cumulative US cash outflow ≤ $18M',
   [('pass',f'Peak {m(peak(A))}'),('fail',f'Peak {m(peak(B))}, still falling in 2030'),('pass',f'Peak {m(peak(J))}')]),
 ('Payback','Cumulative cash back to zero by end-2030',
   [('thin',f'+{m(A[-1]["cum"])} by 2030; needs ad cost ≤ ~28.5%'),('fail',f'Never: {m(B[-1]["cum"])} at end-2030'),('pass',f'In 2029; +$1.8M by 2030')]),
 ('Group margin floor','Group operating margin ≥ 8% every year',
   [('pass',f'Lowest {min(mA)*100:.1f}% (2027)'),('fail',f'{mB[0]*100:.1f}% / {mB[1]*100:.1f}% / {mB[2]*100:.1f}% in 2027–29'),('pass',f'Lowest {min(mJ)*100:.1f}% (2027)')]),
 ('Bandwidth','One major new-market launch in 2027',
   [('pass','One launch; light US team'),('pass','One launch, but the heaviest to run'),('pass','One launch, known market')]),
]
for (t_,s_,cells) in tests:
    rh=0.82
    text(sl,x0+0.1,y+0.08,cw0-0.2,0.3,t_,13,NAVY,bold=True)
    text(sl,x0+0.1,y+0.38,cw0-0.2,0.4,s_,10,SEC)
    for i,(st,txt) in enumerate(cells):
        xx=x0+cw0+i*cwi
        chip(sl,xx+0.1,y+0.12,st,w=0.82)
        text(sl,xx+0.1,y+0.42,cwi-0.2,0.38,txt,10.5,INK)
    y+=rh
    line(sl,x0,y,x0+CW,y,GRID,0.75)
text(sl,x0,y+0.12,CW,0.5,[[('Reading the card: ',{'bold':True}),('A fails only the revenue ambition, which every option misses. B fails three tests even on its own optimistic inputs. J passes the money tests but builds no US business. The weak point in A is payback, which depends on the cost of Amazon advertising (slide 12).',{})]],11,INK)

# ---------- 4 Market
sl=d.slide('Why the US','The US is worth entering: K-beauty skincare is a $3.6B market growing 17% a year, and 41% of it sells on Amazon',
 'Source: briefing pack Tables 1–2 and September 2026 survey (n=1,200 US women aged 18–44). CAGR = compound annual growth rate, 2021–25.')
# left chart
text(sl,ML,1.75,6,0.3,'US sales of K-beauty facial skincare, $B',12,INK,bold=True)
ax=Axis(2.35,5.55,0,4.0)
yaxis(sl,ax,ML+0.55,ML+5.6,[0,1,2,3,4],lambda t:f'{t:.0f}',label_w=0.4,zero=0)
kb=[1.9,2.3,2.7,3.1,3.6]
columns(sl,ax,ML+0.55,ML+5.6,['2021','2022','2023','2024','2025'],[kb],[BLUE],bar_w=0.5,labels='all',label_fmt=lambda v:f'{v:.1f}')
text(sl,ML,5.95,5.8,0.9,[[('+17% a year',{'bold':True}),(' vs +5% for all US facial skincare ($20.1B → $24.5B). K-beauty\'s share of the category rose from 9.5% to 14.7%.',{})]],11,INK)
# right chart: channel
x0=7.1
text(sl,x0,1.75,5.6,0.3,'Where US consumers bought K-beauty skincare, 2025',12,INK,bold=True)
ch=[('Amazon',41),('Specialty beauty retail',27),('Mass retail',14),('Brand websites (DTC)',12),('Other',6)]
by=2.35; bw_max=3.0
for i,(n_,v) in enumerate(ch):
    yy=by+i*0.5
    text(sl,x0,yy,1.95,0.32,n_,10.5,SEC,anchor='middle')
    rect(sl,x0+2.0,yy+0.05,bw_max*v/41,0.22,BLUE if i==0 else GRAYBAR)
    text(sl,x0+2.0+bw_max*v/41+0.05,yy,0.6,0.32,f'{v}%',10.5,INK,bold=(i==0),anchor='middle')
text(sl,x0,5.0,5.6,1.8,[
 [('Survey confirms the channel: ',{'bold':True}),('61% of US K-beauty buyers buy K-beauty most often on Amazon, vs 22% at specialty retail. 38% discovered their last new brand on TikTok, vs 17% in a store.',{})],
 [('Use the right base: ',{'bold':True}),('the "$5.2B US K-beauty market" figure circulated to the board includes makeup and hair care. The market Onsoo competes in is the $3.6B of skincare.',{})]],11,INK,para_space=6)

# ---------- 5 Pilot
sl=d.slide('Amazon pilot evidence','The Amazon pilot shows real demand: monthly sales nearly doubled in six months, with ratings and repeat purchase in line with benchmarks',
 'Source: briefing pack §6 (pilot January–June 2026, three SKUs, sold by a cross-border seller). ACoS = Amazon ad spend as a share of Amazon sales.')
text(sl,ML,1.75,6.5,0.3,'Pilot units sold per month, 2026 (three SKUs)',12,INK,bold=True)
ax=Axis(2.35,5.65,0,16000)
yaxis(sl,ax,ML+0.75,ML+6.6,[0,4000,8000,12000,16000],lambda t:f'{t:,.0f}',label_w=0.6,zero=0)
pu=[7400,8600,10100,11800,12900,14000]
columns(sl,ax,ML+0.75,ML+6.6,['Jan','Feb','Mar','Apr','May','Jun'],[pu],[BLUE],bar_w=0.45,labels={(0,0),(0,5)},label_fmt=lambda v:f'{v:,.0f}')
text(sl,ML,6.0,6.6,0.8,'Month-on-month growth slowed from ~17% (Feb–Apr) to ~9% (May–Jun). The 2027 plan of 300,000 units is 1.8× the June run-rate of 168,000 a year, with seven SKUs instead of three.',10.5,SEC)
# tiles
tiles=[('+89%','Unit growth, Jan → Jun','7,400 → 14,000 units a month; $4.0M a year run-rate at $24'),
       ('4.5 / 5','Rating, 2,140 reviews','Top complaint (6% of reviews): Korean-only label text. Fix it in the 2027 setup'),
       ('29%','90-day repeat purchase','In line with the 31% first-year benchmark on Amazon US; below Onsoo Korea at 48%'),
       ('28%','Ad cost (ACoS) in the pilot','On a small budget. The plan assumes 25%; brands scaling from $5M to $20M run at 32%')]
tx=7.75; tw=(W-ML-tx-0.2)/2; th=2.3
for i,(v,l,s_) in enumerate(tiles):
    xx=tx+(i%2)*(tw+0.2); yy=1.8+(i//2)*(th+0.2)
    rect(sl,xx,yy,tw,th,PALE)
    text(sl,xx+0.15,yy+0.12,tw-0.3,0.6,v,28,NAVY if i<3 else 'B26F00',bold=True)
    text(sl,xx+0.15,yy+0.8,tw-0.3,0.3,l,11,INK,bold=True)
    text(sl,xx+0.15,yy+1.12,tw-0.3,1.1,s_,10.5,SEC)

# ---------- 6 Competitors
sl=d.slide('Competitor evidence','Recent entrants: the one retail-first brand lost $21M and was delisted; Amazon-first brands lost far less, but only one in three reached scale',
 'Source: briefing pack Table 9 (public reporting and interviews). Four brands is a small sample: read as direction, not proof.')
rows=[['Brand','Entry route','Outcome by 2025','What it tells Onsoo'],
      ['Mooncrest','Retail-first, 2023, 450 doors','Removed from shelves in 2025; est. cumulative US loss $21M','A national retail launch without awareness is the costliest way to fail'],
      ['Saebom','Amazon-first, 2022','~$30M US revenue in 2025; added 300 retail doors in 2025','Amazon can carry a brand to ~$30M; retail came after scale, not before'],
      ['Gaon Lab','Amazon-first, 2022','Below $5M US revenue in 2025','Amazon-first does not guarantee scale…'],
      ['Yeoreum','Amazon-first, 2023','Below $5M US revenue in 2025','…but the downside is a small business, not a $21M loss']]
table(sl,ML,1.8,[1.6,2.7,3.9,4.03],rows,row_h=[0.42,0.72,0.72,0.62,0.62],size=11,aligns=['left','left','left','left'],bold_first_col=True)
rect(sl,ML,5.25,CW,0.95,PALE)
text(sl,ML+0.2,5.25,CW-0.4,0.95,[
 [('Implication: ',{'bold':True}),('Amazon-first is the lower-risk way in, and the route that worked for Saebom. Whether Onsoo becomes a Saebom or a Gaon Lab depends on two measurable things: ad cost at scale and repeat purchase. Both go into the 2027 guardrails (slide 16).',{})]],12,INK,anchor='middle')

# ---------- 7 Unit economics
sl=d.slide('Unit economics','Retail earns more per unit than Amazon ($7.55 vs $4.73), but its extra $7.5M a year of fixed cost would take ~4,200 doors to cover; B plans 600–1,000',
 'Source: briefing pack Tables 4 and 6. Rice Ferment Barrier Cream, applied to all SKUs as the planning team does. Landed cost = ex-factory $3.50 + freight + 15% duty on ex-factory.')
au,_=M.amz_unit(); ru,_=M.ret_unit()
rows=[['Per unit, $','Amazon','Specialty retail'],
      ['Consumer price','24.00','28.00'],
      ['Onsoo receives','24.00','14.00'],
      ['Amazon referral fee (15%)','−3.60','—'],
      ['Amazon fulfilment (FBA)','−5.10','—'],
      ['Landed product cost','−4.58','−4.78'],
      ['Retailer co-op (8%) + returns (4%)','—','−1.68'],
      ['Advertising (ACoS 25% of price)','−6.00','in fixed budget'],
      ['Contribution per unit','4.73','7.55'],
      ['Contribution margin on Onsoo revenue','20%','54%']]
table(sl,ML,1.8,[3.3,1.25,1.55],rows,row_h=0.36,size=11,bold_rows=(8,),row_fills={8:'E8F1FC'})
x0=7.0
text(sl,x0,1.8,W-ML-x0,0.3,'Why the higher unit margin does not rescue retail',13,NAVY,bold=True)
text(sl,x0,2.2,W-ML-x0,4.6,[
 [('Fixed cost is the problem. ',{'bold':True}),('B adds $6.0M a year of national retail marketing and $1.5M of field sales on top of A\'s $2.1M base. At 4.5 units per door per week a door earns ~$1,770 a year, so covering $7.5M takes ~4,200 doors. At the 2.6 that brands at Onsoo\'s awareness sell, it takes ~7,400.',{})],
 [('Amazon\'s lever is ad cost. ',{'bold':True}),('Each point of ACoS costs $0.24 per unit. At the pilot\'s 28%, contribution falls to $4.01; at the 32% benchmark, to $3.05. Before advertising, Amazon earns $10.73 a unit, so unit contribution only turns negative above 45% ACoS.',{})],
 [('Tariff exposure is modest. ',{'bold':True}),('A rise in duty from 15% to 25% adds $0.35 a unit in either channel.',{})]],12,INK,para_space=10,spacing=1.05)
text(sl,x0,5.0,W-ML-x0,0.3,'Doors needed to cover $7.5M a year of retail fixed cost',11,INK,bold=True)
dbars=[('At 4.5 units/door/wk (B\'s assumption)',7.5e6/(4.5*52*ru)),('At 2.6 units/door/wk (Onsoo\'s band)',7.5e6/(2.6*52*ru)),('B\'s plan, 2030',1000)]
for i,(n_,v) in enumerate(dbars):
    yy=5.38+i*0.42
    text(sl,x0,yy,2.75,0.34,n_,10,SEC,anchor='middle')
    rect(sl,x0+2.8,yy+0.06,2.4*v/7500,0.22,GRAYBAR if i<2 else ORANGE)
    text(sl,x0+2.8+2.4*v/7500+0.05,yy,0.8,0.34,f'{round(v,-2):,.0f}',10,INK,bold=True,anchor='middle')

# ---------- 8 Cash
sl=d.slide('Cash: investment cap and payback','On the planning team\'s own inputs, retail-led breaches the $18M cap and never pays back; Amazon-led bottoms out at $1.9M and pays back in 2030',
 SRC+' Cumulative pre-tax US cash flow including inventory build; Japan (J) shown for comparison, as given in Table 7 (no working capital provided).')
text(sl,ML,1.75,8,0.3,'Cumulative cash flow, $M (end of year)',12,INK,bold=True)
legend(sl,ML+0.1,2.08,[('A · Amazon-led',BLUE),('B · Retail-led',ORANGE),('J · Japan scale-up',AQUA)],kind='line')
px0,px1=ML+0.7,ML+7.6
ax=Axis(2.5,6.45,-22,5)
yaxis(sl,ax,px0,px1,[-20,-15,-10,-5,0,5],lambda t:f'{t:+.0f}' if t else '0',label_w=0.45,zero=0)
cats=['Start','2027','2028','2029','2030']
xs=[px0+0.3+i*(px1-px0-0.9)/4 for i in range(5)]
for i,c in enumerate(cats): text(sl,xs[i]-0.4,ax.y1+0.06,0.8,0.25,c,10,SEC,align='center')
line(sl,px0,ax(-18),px1,ax(-18),CRIT,1.25)
text(sl,px0+0.05,ax(-18)-0.27,3.2,0.25,'Investment cap: −$18M',10,CRIT,bold=True)
for r,col in ((J,AQUA),(A,BLUE),(B,ORANGE)):
    pts=[(xs[0],ax(0))]+[(xs[i+1],ax(x['cum'])) for i,x in enumerate(r)]
    polyline(sl,pts,col)
text(sl,xs[4]+0.1,ax(A[-1]['cum'])-0.3,1.0,0.25,m(A[-1]['cum']),10.5,INK,bold=True)
text(sl,xs[4]+0.1,ax(J[-1]['cum'])+0.0,1.0,0.25,m(J[-1]['cum']),10.5,INK,bold=True)
text(sl,xs[4]+0.1,ax(B[-1]['cum'])-0.12,1.0,0.25,m(B[-1]['cum']),10.5,INK,bold=True)
x0=8.75
rows=[['$M','A','B','J'],
      ['Peak outflow',f'{peak(A):.1f}',f'{peak(B):.1f}',f'{peak(J):.1f}'],
      ['Cash at end-2030',f'{A[-1]["cum"]:+.1f}',f'{B[-1]["cum"]:.1f}',f'{J[-1]["cum"]:+.1f}'],
      ['2030 cash flow',f'{A[-1]["cf"]:+.1f}',f'{B[-1]["cf"]:.1f}',f'{J[-1]["cf"]:+.1f}'],
      ['Payback year','2030','none','2029']]
table(sl,x0,1.85,[1.7,0.7,0.7,0.7],rows,row_h=0.36,size=10.5)
text(sl,x0,3.85,W-ML-x0,2.9,[
 [('B is still losing $1.9M a year in 2030. ',{'bold':True}),('Its cumulative loss of $20.8M is about what Mooncrest lost ($21M).',{})],
 [('A\'s outflow is small and short: ',{'bold':True}),('the 2027 setup and the inventory build, then positive cash flow from 2028.',{})]],11,INK,para_space=8)

# ---------- 9 Margin
sl=d.slide('Group margin floor','Retail-led would pull group operating margin below the 8% floor for three years running, to 4.5% in 2027; Amazon-led stays above 9%',
 SRC+' Group = ex-US plan ($140–158M revenue at 11.0% operating margin) plus the option\'s revenue and operating result.')
text(sl,ML,1.75,8,0.3,'Group operating margin by option, %',12,INK,bold=True)
legend(sl,ML+0.1,2.08,[('A · Amazon-led',BLUE),('B · Retail-led',ORANGE),('J · Japan scale-up',AQUA)],kind='line')
px0,px1=ML+0.6,ML+7.6
ax=Axis(2.55,6.45,0,12)
yaxis(sl,ax,px0,px1,[0,2,4,6,8,10,12],lambda t:f'{t}%',label_w=0.45,zero=0)
xs=[px0+0.5+i*(px1-px0-1.2)/3 for i in range(4)]
for i,c in enumerate(['2027','2028','2029','2030']): text(sl,xs[i]-0.4,ax.y1+0.06,0.8,0.25,c,10,SEC,align='center')
line(sl,px0,ax(8),px1,ax(8),CRIT,1.25)
text(sl,px0+3.0,ax(8)+0.02,2.6,0.25,'Board floor: 8%',10,CRIT,bold=True)
for r,col in ((mJ,AQUA),(mA,BLUE),(mB,ORANGE)):
    polyline(sl,[(xs[i],ax(v*100)) for i,v in enumerate(r)],col)
text(sl,xs[0]-0.25,ax(mB[0]*100)+0.08,0.8,0.25,f'{mB[0]*100:.1f}%',10.5,INK,bold=True)
text(sl,xs[0]-0.25,ax(mA[0]*100)+0.06,0.8,0.25,f'{mA[0]*100:.1f}%',10.5,INK,bold=True)
x0=8.75
rows=[['%','2027','2028','2029','2030']]+[[n_]+[f'{v*100:.1f}' for v in r] for n_,r in (('A',mA),('B',mB),('J',mJ))]
table(sl,x0,1.85,[0.8,0.68,0.68,0.68,0.68],rows,row_h=0.36,size=10.5)
text(sl,x0,3.55,W-ML-x0,3.2,[
 [('B\'s 2027 US loss of $8.7M ',{'bold':True}),('takes more than half of the ex-US group\'s $15.4M operating profit.',{})],
 [('A costs the group 1.5 points of margin in 2027 ',{'bold':True}),('and adds to margin from 2028.',{})],
 [('A stays above 8% in every stress case we ran: ',{'bold':True}),(f'its lowest is {min(M.margins(M.A(0.38,0.25)))*100:.1f}%, at 38% ACoS and 25% duty.',{})]],11,INK,para_space=8)

# ---------- 10 Retail sell-through
sl=d.slide('Testing Option B: sell-through','Retail-led assumes 4.5 units per door per week; brands at Onsoo\'s awareness sell a median 2.6, below the 4.0 at which the leading retailer delists',
 'Source: briefing pack Table 8 (retail analytics firm, 2025, 46 newcomer brands; first-year sell-through), §10 survey (Sept 2026), Table 9.')
text(sl,ML,1.75,7.5,0.3,'First-year units per door per week, by brand\'s aided awareness among category buyers',12,INK,bold=True)
text(sl,ML,2.05,7.5,0.25,'Bar = median; whisker = interquartile range',10,SEC)
px0,px1=ML+0.6,ML+7.4
ax=Axis(2.6,6.2,0,6)
yaxis(sl,ax,px0,px1,[0,1,2,3,4,5,6],lambda t:f'{t}',label_w=0.35,zero=0)
med=[2.6,3.5,4.6]; iqr=[(1.9,3.4),(2.8,4.3),(3.9,5.5)]
pos=columns(sl,ax,px0,px1-0.9,['Below 10%','10–20%','Above 20%'],[med],[[BLUE,GRAYBAR,GRAYBAR]],bar_w=0.6,labels=None)
for (si,ci,bx,top,bot),(lo,hi) in zip(pos,iqr):
    cx=bx+0.3
    line(sl,cx,ax(lo),cx,ax(hi),INK,1.0); line(sl,cx-0.08,ax(lo),cx+0.08,ax(lo),INK,1.0); line(sl,cx-0.08,ax(hi),cx+0.08,ax(hi),INK,1.0)
    text(sl,bx,bot-0.32,0.6,0.26,f'{med[ci]:.1f}',11,'FFFFFF' if ci==0 else INK,bold=True,align='center')
line(sl,px0,ax(4.5),px1,ax(4.5),ORANGE,1.5)
text(sl,px1-1.25,ax(4.5)-0.48,1.35,0.45,'B assumes 4.5',10,INK,bold=True,align='right')
line(sl,px0,ax(4.0),px1,ax(4.0),CRIT,1.25)
text(sl,px1-1.25,ax(4.0)+0.02,1.35,0.45,'Delisting bar 4.0',10,CRIT,bold=True,align='right')
text(sl,pos[0][2]-0.35,ax.y1+0.3,1.3,0.25,'Onsoo today',9.5,BLUE,bold=True,align='center')
x0=8.6
text(sl,x0,1.8,W-ML-x0,5.0,[
 [('Onsoo sits in the lowest band. ',{'bold':True}),('Aided awareness is 4% among US skincare buyers and 9% even among K-beauty buyers.',{})],
 [('At that awareness, even a top-quartile brand (3.4) sells below the 4.0 bar. ',{'bold':True}),('The leading retailer reviews newcomers after 12 months, so a 2027 launch would most likely be delisted in 2028.',{})],
 [('The 4.5 figure comes from the retailer\'s deck on ',{'bold':False}),('successful',{'italic':True}),(' newcomers. It describes the winners, not the typical brand.',{})],
 [('Mooncrest shows the cost: ',{'bold':True}),('450 doors in 2023, removed in 2025, and an estimated $21M lost.',{})]],11.5,INK,para_space=9)

# ---------- 11 Halo
sl=d.slide('Testing Option B: the Amazon "halo"','The 1.3× Amazon halo rests on a correlation, not cause and effect; and retail-led fails the cash tests even if the halo is real',
 SRC+' Correlation from the independent board member\'s memo (30 brands). Halo = B\'s Amazon units as a multiple of Option A\'s.')
text(sl,ML,1.8,5.6,0.3,'Why a 0.71 correlation does not show that retail drives Amazon',13,NAVY,bold=True)
text(sl,ML,2.2,5.6,4.5,[
 [('Common cause. ',{'bold':True}),('Strong brands with bigger budgets win more doors and more Amazon sales. Both follow from brand strength, so neither need cause the other.',{})],
 [('Reverse direction. ',{'bold':True}),('Retailers recruit brands that are already winning online. Saebom added 300 doors in 2025 only after reaching ~$30M on Amazon.',{})],
 [('No before-and-after. ',{'bold':True}),('A snapshot of 30 brands cannot show what happened to Amazon sales after a brand entered stores.',{})],
 [('Shoppers point the other way. ',{'bold':True}),('Only 17% of K-beauty buyers found their last new brand in a store; 38% found it on TikTok.',{})]],11.5,INK,para_space=9)
x0=6.6
text(sl,x0,1.8,W-ML-x0,0.3,'Option B under different assumptions',13,NAVY,bold=True)
cases=[('Planning case: 4.5 units/door/wk, 1.3× halo',M.B()),
       ('No halo (Amazon = Option A volumes)',M.B(halo=1.0)),
       ('2.6 units/door/wk (Onsoo\'s awareness band)',M.B(upw=2.6)),
       ('2.6 units/door/wk and no halo',M.B(upw=2.6,halo=1.0)),
       ('… and ACoS at the 32% benchmark',M.B(upw=2.6,halo=1.0,acos=0.32))]
rows=[['Case','Cash at end-2030','Lowest group margin']]+[[n_,m(r[-1]['cum']),f'{min(M.margins(r))*100:.1f}%'] for n_,r in cases]
table(sl,x0,2.2,[3.65,1.35,1.18],rows,row_h=0.4,size=10.5)
# halo needed
lo,hi=1.0,6.0
for _ in range(50):
    mid=(lo+hi)/2
    if M.B(halo=mid)[-1]['cum']>=0: hi=mid
    else: lo=mid
hb=M.B(halo=hi)
rect(sl,x0,4.85,W-ML-x0,1.2,PALE)
text(sl,x0+0.15,4.85,W-ML-x0-0.3,1.2,[
 [('To pay back by 2030, B would need a halo of about ',{}),(f'{hi:.1f}×',{'bold':True}),(f', not 1.3×: Amazon sales of {hi*0.3:.1f}M units in 2027, against 0.3M planned for Amazon-led and {hi*300/168:.1f}× the pilot\'s June run-rate. ',{}),
  (f'Even then, group margin would fall to {min(M.margins(hb))*100:.1f}% in 2027.',{'bold':True})]],11.5,INK,anchor='middle')
rect(sl,ML,4.85,5.6,1.2,PALE)
text(sl,ML+0.15,4.85,5.3,1.2,[[('The memo\'s claim: ',{'bold':True}),('"Across 30 K-beauty brands, doors correlate with Amazon sales (0.71). Retail drives Amazon sales; that is where the 1.3× halo comes from."',{'italic':True})]],10.5,SEC,anchor='middle')

# ---------- 12 A risk ACoS
sl=d.slide('Testing Option A: the payback risk','Amazon-led\'s weak point is payback: it pays back by 2030 only if ad cost stays at or below ~28.5% of sales, against a 32% median for scaling brands',
 SRC+' Option A volumes as planned (0.3M → 1.1M units). Duty applied to all four years in the 25% case (decision due mid-2027). Agency benchmark: brands scaling $5M → $20M on Amazon US.')
text(sl,ML,1.75,8,0.3,'Option A: cumulative cash at end-2030, $M, by Amazon ad cost (ACoS)',12,INK,bold=True)
legend(sl,ML+0.1,2.08,[('US duty 15% (today)',BLUE),('US duty 25% (under review)',NAVY)],kind='line')
px0,px1=ML+0.6,ML+7.7
ax=Axis(2.85,6.25,-8,4)
yaxis(sl,ax,px0,px1,[-8,-6,-4,-2,0,2,4],lambda t:f'{t:+d}' if t else '0',label_w=0.4,zero=0)
xa=lambda a:px0+0.2+(a-0.24)/(0.38-0.24)*(px1-px0-0.4)
# benchmark range band
rect(sl,xa(0.26),ax.y0,xa(0.38)-xa(0.26),ax.y1-ax.y0,'F1F6FD')
for a in [0.24,0.26,0.28,0.30,0.32,0.34,0.36,0.38]:
    text(sl,xa(a)-0.3,ax.y1+0.06,0.6,0.22,f'{a*100:.0f}%',9.5,MUTED,align='center')
text(sl,px0,ax.y1+0.3,px1-px0,0.25,'Amazon ACoS (ad spend as % of Amazon sales)',10,SEC,align='center')
text(sl,xa(0.38)-3.25,ax.y0+0.03,3.2,0.22,'Benchmark range for scaling brands: 26–38%',9,SEC,align='right')
for a,lab in ((0.25,'Plan 25%'),(0.28,'Pilot 28%'),(0.32,'Benchmark median 32%')):
    line(sl,xa(a),ax.y0+0.3,xa(a),ax.y1,MUTED,0.75)
    text(sl,xa(a)+0.04,ax(-7.0),1.8,0.22,lab,9,INK,bold=True,margin=0.0)
for duty,col in ((0.15,BLUE),(0.25,NAVY)):
    pts=[(xa(a),ax(M.A(a,duty)[-1]['cum'])) for a in (0.24,0.38)]
    line(sl,pts[0][0],pts[0][1],pts[1][0],pts[1][1],col,2.25)
    for a in (0.25,0.28,0.32):
        dot(sl,xa(a),ax(M.A(a,duty)[-1]['cum']),0.055,col)
v=M.A(0.25)[-1]['cum']; text(sl,xa(0.25)+0.06,ax(v)-0.34,0.8,0.24,'+'+m(v),10,INK,bold=True)
v=M.A(0.32)[-1]['cum']; text(sl,xa(0.32)+0.06,ax(v)-0.34,0.8,0.24,m(v),10,INK,bold=True)
x0=8.75
text(sl,x0,1.8,W-ML-x0,0.3,'What holds and what doesn\'t',13,NAVY,bold=True)
text(sl,x0,2.2,W-ML-x0,4.6,[
 [('Payback is the test at risk. ',{'bold':True}),('It breaks even at ACoS of 28.6%, or 26.9% if duty rises to 25%. At the 32% benchmark, A is $2.3M short at end-2030, and on 2030\'s cash flow it would take until about 2032–33 to pay back.',{})],
 [('The cap and the margin floor hold in every case. ',{'bold':True}),(f'Even at 38% ACoS and 25% duty, peak outflow is ${-peak(M.A(0.38,0.25)):.1f}M (cap $18M) and group margin stays at or above {min(M.margins(M.A(0.38,0.25)))*100:.1f}%.',{})],
 [('Volume matters less. ',{'bold':True}),('At 25% ACoS, A still breaks even by 2030 with 20% fewer units.',{})],
 [('So the plan must manage ad cost: ',{'bold':True}),('grow only as fast as ACoS allows, and hold it at or below 28% (slide 16).',{})]],11,INK,para_space=8)

# ---------- 13 Ambition
sl=d.slide('The $40M ambition','No route within the cash limits reaches $40M by 2030; Amazon-led reaches $26M, so we suggest restating the target as $40M by 2032',
 SRC+' Retail revenue at wholesale ($14 per unit), i.e. Onsoo\'s revenue. The ~2032 date for $40M is a simple extrapolation of A\'s 2030 growth rate, not a forecast.')
text(sl,ML,1.75,8,0.3,'Revenue by option, $M',12,INK,bold=True)
legend(sl,ML+0.1,2.08,[('A · Amazon-led',BLUE),('B · Retail-led',ORANGE),('J · Japan scale-up',AQUA)])
px0,px1=ML+0.6,ML+7.7
ax=Axis(2.6,6.3,0,45)
yaxis(sl,ax,px0,px1,[0,10,20,30,40],lambda t:f'{t}',label_w=0.4,zero=0)
pos=columns(sl,ax,px0,px1,['2027','2028','2029','2030'],[[x['rev'] for x in A],[x['rev'] for x in B],[x['rev'] for x in J]],[BLUE,ORANGE,AQUA],bar_w=0.36,gap=0.04,labels={(0,3),(2,3)},label_fmt=lambda v:f'{v:.1f}')
bx=[p for p in pos if p[0]==1 and p[1]==3][0]
text(sl,bx[2]-0.1,bx[3]+0.05,0.56,0.24,f'{B[-1]["rev"]:.1f}',10,'FFFFFF',bold=True,align='center')
line(sl,px0,ax(40),px1,ax(40),CRIT,1.25)
text(sl,px0+0.05,ax(40)-0.27,2.5,0.25,'Ambition: $40M in 2030',10,CRIT,bold=True)
x0=8.75
text(sl,x0,1.8,W-ML-x0,4.9,[
 [('A reaches $26.4M in 2030, ',{'bold':True}),('two-thirds of the way. It is still growing 29% a year; at that pace it would pass $40M in about 2032.',{})],
 [('B\'s $37.6M would come only on its optimistic inputs, ',{'bold':True}),('at a cumulative cost of $20.8M and three failed board tests.',{})],
 [('Hitting $40M on Amazon alone by 2030 ',{'bold':True}),('would need 1.67M units, 50% above plan, and buying that volume would push ACoS up.',{})],
 [('Our suggestion: ',{'bold':True}),('keep the cash, payback and margin tests as set, and restate the ambition as "$25M+ in 2030, $40M by 2032".',{})]],11,INK,para_space=8)

# ---------- 14 Japan
sl=d.slide('The Japan alternative','The Japan scale-up is safe but small: $7M of revenue and $1.8M of cash by 2030, in a market growing 1.5% a year',
 SRC+' Option J from Table 7 (30% contribution, $0.8M a year fixed cost, $1.0M one-time). "A at 32% ACoS" is the benchmark stress case from slide 12.')
cols3=[('A · Amazon-led (plan)',A,BLUE),('A at 32% ACoS',A32,BLUE),('J · Japan scale-up',J,AQUA)]
rows=[['', 'A · Amazon-led\n(planning case)','A · Amazon-led\n(ACoS 32%)','J · Japan\nscale-up'],
      ['Revenue in 2030',f'${A[-1]["rev"]:.1f}M',f'${A32[-1]["rev"]:.1f}M',f'${J[-1]["rev"]:.1f}M'],
      ['Cumulative cash, end-2030',m(A[-1]['cum']),m(A32[-1]['cum']),m(J[-1]['cum'])],
      ['Cash flow in 2030',m(A[-1]['cf']),m(A32[-1]['cf']),m(J[-1]['cf'])],
      ['Market growth','K-beauty skincare +17%/yr','K-beauty skincare +17%/yr','Japan skincare +1.5%/yr'],
      ['Builds a new growth platform','Yes','Yes','No: Japan is already 24% of sales']]
table(sl,ML,1.85,[2.3,2.15,2.15,2.65],rows,row_h=[0.62,0.4,0.4,0.4,0.4,0.4],size=11,aligns=['left','right','right','right'])
x0=10.2
text(sl,x0,1.85,W-ML-x0,4.9,[
 [('The Head of Japan is right that J is safer. ',{'bold':True}),('If US ad cost goes to benchmark, J ends 2030 ahead on cash by about $4M.',{})],
 [('But J is capped. ',{'bold':True}),('Onsoo already holds 3.1% of a market growing 1.5% a year.',{})],
 [('The bandwidth rule covers 2027 only. ',{'bold':True}),('We suggest revisiting the Japan scale-up for 2028, once the US launch is stable.',{})]],11,INK,para_space=8)
rect(sl,ML,4.85,9.25,1.05,PALE)
text(sl,ML+0.2,4.85,8.9,1.05,[
 [('Trade-off for the board: ',{'bold':True}),('J gives up about $19M of 2030 revenue, and the US platform behind it, to avoid a downside of about $4M of cumulative cash by 2030. Both cases sit far inside the $18M cap. We think the US is the better use of 2027, provided ad cost is managed.',{})]],12,INK,anchor='middle')

# ---------- 15 Retail gate
sl=d.slide('The path into retail','Treat specialty retail as an option to earn, not a 2029 date: raise the awareness trigger to 20% and redesign retail costs to fit payback',
 'Source: briefing pack §4 (CEO hypothesis), Tables 6, 8, 9; team analysis. Proposed gates are our recommendation.')
rows=[['Gate','CEO\'s hypothesis','Proposed','Why'],
      ['Aided awareness\n(category buyers)','> 15%','> 20%','In the 10–20% band the median brand sells 3.5 units/door/week, below the 4.0 delisting bar. Above 20% the median is 4.6.'],
      ['Amazon sales','> $10M a year','> $10M a year at ACoS ≤ 28%','The plan passes $10M in 2028. Sales bought with heavy advertising do not prove the brand.'],
      ['Repeat purchase','—','90-day repeat ≥ 31%','Repeat at the first-year benchmark shows the brand holds customers, not just wins trials.'],
      ['Retail economics','—','Retail case pays its own way and keeps 2030 payback','At $7.5M a year of fixed cost, retail needs ~4,200 doors. A test of ~300 doors (Saebom\'s scale) needs a matching, smaller budget.'],
      ['Timing','Retail from 2029','Decide at end-2028 on the gates','A\'s planning case leaves only $2.4M of cash headroom at 2030, so a full-cost national launch in 2029 would break payback.']]
table(sl,ML,1.8,[2.1,1.9,2.45,5.78],rows,row_h=[0.4,0.72,0.66,0.6,0.72,0.72],size=10.5,aligns=['left','left','left','left'],bold_first_col=True)
rect(sl,ML,5.85,CW,0.95,'E8F1FC')
text(sl,ML+0.2,5.9,CW-0.4,0.85,[[('We agree with the CEO\'s sequence: Amazon first, retail later. ',{'bold':True}),('Two changes would avoid a Mooncrest-style retail entry: a higher awareness bar, and a retail plan sized to what the US business can already fund.',{})]],12,INK,anchor='middle')

# ---------- 16 Plan & guardrails
sl=d.slide('Recommendation and 2027 plan','Launch Amazon-led in 2027 with a small cash envelope and quarterly guardrails that slow spending if ad cost or repeat purchase falls short',
 SRC+' Envelope, guardrail levels and triggers are proposals for board approval.')
cw3=(CW-0.4)/3
blocks=[('H1 2027 · Set up',[
  'Form US entity; take the three SKUs back from the cross-border seller',
  'US-compliant English labels for all SKUs (fixes the 6% complaint); MoCRA registration',
  'Hire the US team ($0.9M a year); set up FBA inventory (~4 months of stock)']),
 ('2027 · Launch and grow',[
  'Launch four more SKUs on Amazon; plan of 300,000 units ($7.2M)',
  'Off-Amazon marketing ($0.7M) aimed at TikTok, where 38% of K-beauty buyers discover brands',
  'Twice-yearly awareness survey to track progress to the 20% retail gate']),
 ('Guardrails · reviewed quarterly',[
  'ACoS ≤ 28%; if above 30% for two quarters, slow paid growth and re-forecast payback',
  'Repeat ≥ 29% (pilot); rating ≥ 4.5; units vs plan',
  'Cumulative cash within a $4M envelope; board approval needed to go beyond it',
  'Mid-2027 tariff decision: if 25%, payback needs ACoS ≤ 27%; review pricing'])]
for i,(h_,items) in enumerate(blocks):
    xx=ML+i*(cw3+0.2)
    rect(sl,xx,1.8,cw3,0.45,NAVY if i<2 else 'B26F00')
    text(sl,xx+0.15,1.8,cw3-0.3,0.45,h_,12.5,'FFFFFF',bold=True,anchor='middle')
    rect(sl,xx,2.25,cw3,2.35,PALE)
    text(sl,xx+0.12,2.36,cw3-0.24,2.2,items,11,INK,bullet=True,para_space=7)
text(sl,ML,4.8,4,0.28,'Key dates',11,NAVY,bold=True)
tl=[('Mar 2027','Board approves A'),('Mid-2027','US tariff decision: re-plan if duty rises to 25%'),('Q4 2027','First full board review vs guardrails'),('End-2028','Retail gate decision for 2029–30'),('End-2030','Payback test')]
ty=5.32; line(sl,ML+0.1,ty,ML+CW-0.1,ty,AXIS,1.5)
for i,(d_,t_) in enumerate(tl):
    tx=ML+0.1+i*(CW-0.2)/4
    dot(sl,tx,ty,0.07,NAVY)
    al='left' if i==0 else ('right' if i==4 else 'center')
    bx_=tx if i==0 else (tx-2.3 if i==4 else tx-1.15)
    text(sl,bx_,ty+0.1,2.3,0.25,d_,10.5,INK,bold=True,align=al)
    text(sl,bx_,ty+0.34,2.3,0.45,t_,9.5,SEC,align=al)
text(sl,ML,6.2,CW,0.7,[[('Why a $4M envelope: ',{'bold':True}),('it covers A\'s peak outflow in the benchmark-ACoS case ($3.2M) with some headroom, and is less than a quarter of the $18M cap. Anything beyond it would signal the plan is off track, which is the moment for the board to decide whether to push on, slow down or stop.',{})]],11.5,INK)

# ---------- 17 Decisions
sl=d.slide('Decisions requested','Five decisions for the March 2027 board meeting',SRC)
dec=[('1','Approve US entry in 2027 through the Amazon-led route (Option A).','Only route that passes the investment, payback and margin tests'),
     ('2','Approve a $4M envelope for cumulative US cash outflow, with board review before going beyond it.','Covers the benchmark-ACoS case; under a quarter of the $18M cap'),
     ('3','Decline the 600-door national retail launch for 2027; adopt the retail gates (20% awareness, ACoS ≤ 28%, repeat ≥ 31%, self-funding retail case).','B fails three board tests; sell-through and halo assumptions do not hold'),
     ('4','Restate the US ambition as "$25M+ in 2030, $40M by 2032".','No route within the cash limits reaches $40M by 2030'),
     ('5','Hold the Japan scale-up in 2027 and revisit it for 2028.','Bandwidth allows one launch in 2027; Japan upside is ~$7M of revenue')]
y=1.8
for n_,t_,w_ in dec:
    rect(sl,ML,y+0.1,0.5,0.5,BLUE,shape=MSO_SHAPE.OVAL)
    text(sl,ML,y+0.1,0.5,0.5,n_,16,'FFFFFF',bold=True,align='center',anchor='middle')
    text(sl,ML+0.75,y,7.6,0.72,t_,13,INK,bold=True,anchor='middle')
    text(sl,ML+8.6,y,CW-8.6,0.72,w_,11,SEC,anchor='middle')
    y+=0.8
    line(sl,ML+0.75,y-0.04,ML+CW,y-0.04,GRID,0.75)
text(sl,ML,y+0.1,CW,0.55,[[('Risk the board accepts with decision 1: ',{'bold':True}),('payback by end-2030 is likely on the planning inputs but not assured. It needs ACoS at or below ~28.5%, against 28% in the pilot and 32% for scaling brands.',{})]],11.5,INK)

# ---------- Appendix divider
sl=d.slide(number=True)
rect(sl,0,0,W,H,NAVY)
text(sl,ML,3.0,10,0.8,'Appendix',36,'FFFFFF',bold=True)
text(sl,ML,3.9,11,0.9,'A1 Model outputs by option · A2 Option A sensitivities · A3 Method and choices made',15,'CDE2FB')

# ---------- A1 model outputs
sl=d.slide('Appendix A1','Model outputs by option, 2027–2030 ($M, planning-team inputs)',
 SRC+' Operating result = contribution − fixed − one-time (fixtures included). Cash flow = operating result − inventory build. Pre-tax, undiscounted.')
def block(name,r,y,extra=None):
    rows=[[name,'2027','2028','2029','2030']]
    rows.append(['Revenue']+[f'{x["rev"]:.1f}' for x in r])
    if 'contr' in r[0]: rows.append(['Contribution']+[f'{x["contr"]:.1f}' for x in r])
    rows.append(['Operating result']+[f'{x["op"]:.1f}' for x in r])
    rows.append(['Cash flow']+[f'{x["cf"]:.1f}' for x in r])
    rows.append(['Cumulative cash']+[f'{x["cum"]:.1f}' for x in r])
    rows.append(['Group op. margin']+[f'{v*100:.1f}%' for v in M.margins(r)])
    return rows
ra=block('A · Amazon-led',A,0); rb=block('B · Retail-led',B,0); rj=block('J · Japan scale-up',J,0)
cwA=[1.51,0.61,0.61,0.61,0.61]
table(sl,ML,1.75,cwA,ra,row_h=0.33,size=10)
table(sl,ML+4.14,1.75,cwA,rb,row_h=0.33,size=10)
table(sl,ML+8.28,1.75,cwA,rj,row_h=0.33,size=10)
text(sl,ML,4.3,CW,2.5,[
 [('Volumes. ',{'bold':True}),('A: Amazon 0.30 / 0.56 / 0.85 / 1.10M units. B: Amazon 1.3× A; retail 600 / 600 / 800 / 1,000 doors × 4.5 units × 52 weeks (140k / 140k / 187k / 234k units).',{})],
 [('Fixed and one-time cost. ',{'bold':True}),('A: $2.1M a year plus $0.8M setup. B: $9.6M a year plus $0.8M setup, $0.5M launch fee and $1,100 fixtures per new door ($0.66M in 2027, $0.22M in 2029 and 2030).',{})],
 [('Inventory. ',{'bold':True}),(f'Four months of landed cost, built as volumes grow: A ends 2030 holding ${A[-1]["inv"]:.1f}M, B ${B[-1]["inv"]:.1f}M. J has no working capital in the pack and none is added.',{})]],10.5,INK,para_space=6)

# ---------- A2 sensitivities
sl=d.slide('Appendix A2','Option A sensitivities: ad cost drives payback; the cap and the margin floor are never at risk',
 SRC+' 25% duty applied to all four years (conservative; decision due mid-2027).')
acs=[0.25,0.28,0.30,0.32,0.38]
rows=[['Cumulative cash at end-2030, $M']+[f'ACoS {a*100:.0f}%' for a in acs]]
for dt in (0.15,0.25):
    rows.append([f'Duty {dt*100:.0f}%']+[f'{M.A(a,dt)[-1]["cum"]:+.1f}' for a in acs])
rows.append(['Peak outflow, duty 25%']+[f'{min(x["cum"] for x in M.A(a,0.25)):.1f}' for a in acs])
rows.append(['Lowest group margin, duty 25%']+[f'{min(M.margins(M.A(a,0.25)))*100:.1f}%' for a in acs])
table(sl,ML,1.8,[3.3]+[1.4]*5,rows,row_h=0.38,size=11)
rows=[['Volume vs plan (cumulative cash at end-2030, $M)','100%','90%','80%']]
for a in (0.25,0.28):
    rows.append([f'ACoS {a*100:.0f}%, duty 15%']+[f'{M.A(a,0.15,v)[-1]["cum"]:+.1f}' for v in (1.0,0.9,0.8)])
table(sl,ML,4.15,[4.5,1.3,1.3,1.3],rows,row_h=0.38,size=11)
text(sl,ML,5.5,CW,1.3,[[('Break-even ACoS for 2030 payback: ',{'bold':True}),('28.6% at 15% duty and 26.9% at 25% duty. Contribution per Amazon unit is $10.73 before advertising, less $0.24 per point of ACoS.',{})]],11,INK)

# ---------- A3 method & choices
sl=d.slide('Appendix A3','Method, and the judgement calls made in preparing this document',
 'All inputs from the briefing pack; no outside data used. Where the pack was silent or ambiguous, the choices listed here were made; all are open to challenge.')
items=[
 ('$40M ambition','Read as a 2030 US revenue target. If the board meant "a trajectory toward $40M", A\'s $26M growing 29% a year may already satisfy it.'),
 ('Revenue basis','Retail revenue counted at wholesale ($14), the price Onsoo receives; Amazon at $24. Shelf-price revenue would overstate B.'),
 ('Cash definition','Pre-tax, undiscounted; operating result less inventory build (four months of landed cost). No receivables or payables, which would make B worse (retailer terms).'),
 ('Doors and fixtures','Doors sell for the full year they are listed; fixtures paid in the year a door opens. Delisting after 12 months is not modelled, which flatters B.'),
 ('Tariff stress','25% duty applied to all four years, although the decision is due mid-2027; conservative for both options.'),
 ('Group margin','Ex-US plan (11.0% margin) plus the option\'s revenue and operating result. Japan option used exactly as given in Table 7.'),
 ('Gates and envelope','The $4M envelope, ACoS guardrails and 20% awareness gate are our proposals, derived from the pack\'s benchmarks.'),
 ('Planning volumes','A and B volumes used as given. The pilot supports 2027 (1.8× the June run-rate with seven SKUs instead of three); later years are untested.'),
 ('Format','Charts are drawn as native shapes, so they can be edited but are not linked to data. Model figures can be regenerated from the build script.')]
y=1.8
for h_,b_ in items:
    text(sl,ML,y,2.3,0.5,h_,11,NAVY,bold=True)
    text(sl,ML+2.4,y,CW-2.4,0.5,b_,10.5,INK)
    y+=0.56
    line(sl,ML,y-0.05,ML+CW,y-0.05,GRID,0.5)

d.save(OUT)
print('slides',d.n)
for i in ISSUES: print('ISSUE',i)
