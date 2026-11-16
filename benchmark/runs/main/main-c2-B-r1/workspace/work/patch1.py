p='build.py'; s=open(p).read()
def R(a,b,cnt=1):
    global s
    n=s.count(a)
    assert n==cnt, (n,a[:70])
    s=s.replace(a,b)
# 1 exec title
R('header("Executive summary", "Harlow can rebuild its margin to ~2.9–3.1% by FY2028 by fixing promotions, shrink and delivery pricing, rebalancing labor and exiting loss-making stores. The 8% labor cut should not go ahead.")',
  'header("Executive summary", "Fix promotions, shrink and delivery pricing, rebalance labor and exit loss-making stores: margin returns to ~2.9–3.1% by FY2028. The 8% labor cut should not go ahead.")')
R('D.text(2.45, yy + 0.38, 10.4, 0.85,','D.text(2.45, yy + 0.5, 10.4, 0.72,')
R('D.text(2.45, yy - 0.04, 10.4, 0.45, P(head, size=12.5, bold=True), margin=0.03)','D.text(2.45, yy - 0.04, 10.4, 0.5, P(head, size=12, bold=True), margin=0.03)')
# 3 minus signs in waterfall
R('''        if kind == "total":
            lo, hi = sorted((0, v)); run = v
            col = col or INK2
            txt = tfmt(v)''','''        if kind == "total":
            lo, hi = sorted((0, v)); run = v
            col = col or INK2
            txt = tfmt(v).replace("-", "−")''')
R('''            txt = fmt(v)
        bars.append''','''            txt = fmt(v).replace("-", "−")
        bars.append''')
# 4 clip at ymin
R('''    Y = lambda v: bot - (v - vmin) * sc''','''    Y = lambda v: bot - (max(v, vmin) - vmin) * sc''')
R('''    D.line(x, Y(0), x + w, Y(0), color=GRAY, lw=0.75)''','''    D.line(x, Y(max(0, vmin)), x + w, Y(max(0, vmin)), color=GRAY, lw=0.75)''')
# 5 slide 7 table
R('table(8.2, 1.8, [2.4, 1.08, 1.15], rows, rowh=0.36, size=10, bold_last=True)','table(8.2, 1.8, [2.75, 0.9, 0.98], rows, rowh=0.36, size=10, bold_last=True)')
R('''        ["Incremental contribution ($96 × 30% × 20¢)", "$5.76", "$5.76"],''','''        ["Contribution ($96 × 30% new × 20¢)", "$5.76", "$5.76"],''')
R('''        ["Delivery cost net of fee ($13.80 − $3.10)", "–", "−$10.70"],''','''        ["Delivery net of fee ($13.80 − $3.10)", "–", "−$10.70"],''')
R('''D.text(8.2, 3.75, 4.63, 3.05, [P("Why the team's''','''D.text(8.2, 3.75, 4.63, 2.6, [P("Why the team's''')
# 6 target line
R('''D.line(0.5, Y(41.9), 9.7, Y(41.9), color=INK, lw=0.75, dash=True)''','''D.line(0.5, Y(41.9), 0.5 + 10 * 9.2 / 11, Y(41.9), color=INK, lw=0.75, dash=True)''')
# 7 slide 4 table
R('table(8.95, 1.75, [1.6, 0.8, 0.95, 0.53], rows, rowh=0.3, size=9.5, bold_last=True)','table(8.95, 1.75, [1.45, 0.75, 1.15, 0.53], rows, rowh=0.3, size=9.5, bold_last=True)')
R('["Driver", "pt of sales", "$M at FY25 sales", "Share"]','["Driver", "pt", "$M, FY25 sales", "Share"]')
R('D.text(8.95, 4.0, 3.88, 2.7, [P("What this means"','D.text(8.95, 4.0, 3.88, 2.15, [P("What this means"')
# 8 panels
R('''D.text(0.5, 5.25, 5.6, 1.55, [P("So what"''','''D.text(0.5, 5.35, 5.6, 1.05, [P("So what"''')
R('''    fill=PANEL, margin=0.1)
footer("Source: briefing pack Table 5 and §7 fee test''','''    fill=PANEL, margin=0.1)
footer("Source: briefing pack Table 5 and §7 fee test''')
R('D.text(7.95, 1.75, 4.88, 5.1, [','D.text(7.95, 1.75, 4.88, 4.0, [')
R('D.text(0.5, 5.05, 4.0, 1.8, [P("Why it matters','D.text(0.5, 5.05, 4.0, 1.3, [P("Why it matters')
R('D.text(4.67, 5.05, 4.0, 1.8, [P("How the rebalance','D.text(4.67, 5.05, 4.0, 1.3, [P("How the rebalance')
R('D.text(8.83, 5.05, 4.0, 1.8, [P("Wage outlook"','D.text(8.83, 5.05, 4.0, 1.3, [P("Wage outlook"')
R('D.text(10.75, 1.75, 2.08, 3.6, [P("Recommendation"','D.text(10.75, 1.75, 2.08, 1.85, [P("Recommendation"')
R('D.text(0.5, 5.65, 12.33, 1.2, [P("Ranking logic"','D.text(0.5, 5.65, 12.33, 0.9, [P("Ranking logic"')
R('D.text(9.3, 1.75, 3.53, 4.9, [P("Notes"','D.text(9.3, 1.75, 3.53, 3.6, [P("Notes"')
R('D.text(9.55, 1.75, 3.28, 5.1, [P("Sensitivities','D.text(9.55, 1.75, 3.28, 4.25, [P("Sensitivities')
R('D.text(0.5, 5.4, 12.33, 1.45, [P("Contingency','D.text(0.5, 5.4, 12.33, 1.0, [P("Contingency')
# 9 slide 17
R('"Traffic loss when events are cut; share reaches 24–26%"','"Traffic loss when events are cut"')
R('"FY2028 margin ranges from 2.0% to 3.8%. Even the low case keeps operating income near $27M, well above the $20M covenant level."',
  '"FY2028 margin ranges from 2.0% to 3.8%. Even in the low case operating income is ~$27M, well above the $20M level the lender requires."')
# 10 less fees
R('["Delivery fees collected ($M; $3.10 → $6.40 per order)", "−2.4", "−4.5", "−2.1"]','["Less: delivery fees ($M; $3.10 → $6.40 per order)", "−2.4", "−4.5", "−2.1"]')
# contingency claim
R('Together ~$5M, enough to cover the gap between the base and low cases on vendor funding and the wage step.',
  'Together ~$5M: enough to cover either vendor funding failing entirely (−$3.6M) or the wage step going wholly unrecovered (−$3.6M), but not both.')
R('"Markdowns ≈ 14 pt ÷ (1 − 46%) = 25.9% of promoted sales; 25% × $1,398M × 25.9% = $90M × 4 pt"','"Markdowns ≈ 14 pt ÷ (1 − 46%) = 25.9% of promoted sales; 25% × $1,398M × 25.9% = $90.6M × 4 pt"')
R('footer("I could not ask questions while this deck was being prepared, so each choice above is the option I would recommend. Each is flagged for management to confirm.")',
  'footer("Prepared without the chance to ask clarifying questions: each choice above is the recommended option and is flagged for management to confirm.")')
# decisions spacing / size
R('''D.text(xx + 0.5, yy, 5.55, 1.45, [P(h, size=13, bold=True), P(t, size=11, color=INK2, space_before=4)], margin=0.03)''',
  '''D.text(xx + 0.5, yy, 5.55, 1.45, [P(h, size=14, bold=True), P(t, size=12, color=INK2, space_before=4)], margin=0.03)''')
open(p,'w').write(s)
