def edit(f, pairs):
    s=open(f).read()
    for a,b in pairs:
        assert s.count(a)==1,(f,a[:80],s.count(a)); s=s.replace(a,b)
    open(f,'w').write(s)
edit('dps.py',[
('D("plof", "Share of the promotion and shrink loss won back by private label", "%", "mpl / (0 - mpromo - mshr)", "0.18 ÷ (0.70 + 0.50)", "FY2023–FY2025")',
 'D("plof", "Private-label gain as a share of the net gross-margin loss", "%", "mpl / (0 - dgm)", "0.18 ÷ 1.02", "FY2023–FY2025")'),
('D("pd13s", "Share of the gap covered by the starting hypothesis\'s levers", "%", "pd13 / gap", "$13.1M ÷ $35.6M", "FY2028")\n',''),
])
edit('build.py',[('SHARES = {"sh_gmec": 2,','SHARES = {"omC": 3, "sh_gmec": 2,'),
('{"id": "1", "title": "Diagnosis: what drove the margin down",','{"id": "1", "title": "Diagnosis: the size of the gap and what drove it",'),
('"title": "First moves, risks and decisions for the board",','"title": "First moves, risks and the decisions asked of the board",'),
])
edit('slides.py',[
# 1a caption
('"caption": "FY2028 operating margin if nothing changes, against the 3.0% target",',
 '"caption": "FY2028 operating margin if nothing changes ($7.7M of operating income), against the 3.0% target",'),
# 1c caption
('"caption": "of the promotion and shrink loss won back by the higher private-label share",',
 '"caption": "of the net gross-margin loss offset by the higher private-label share",'),
# 2a blind spots
('"**Blind spots:** the freeze keeps the $10.4M e-commerce loss, and nothing addresses promotions, the largest cause at $10.5M",',
 '"**Blind spots:** the freeze stops the e-commerce loss growing but keeps the $10.4M; promotions, the largest cause at $10.5M, are untouched",'),
# 2b table
('''            "columns": ["FY2028 margin", "One-time cost", "FY2026 income", "Owners and board", "Main risks"],
            "rows": [
                row("A. Draft: 8% hours cut, e-commerce freeze", ["@omdraft", "Small", "Met on paper if the cut lands early", "Kept", "Shrink, service, fresh; promotions untouched"], note="Reject"),
                row("B. Margin-first plan", ["@omfirm", "@otot", "@oi26", "Kept; 3 other stores need a board vote", "Traffic response; vendor push-back"], highlight=True, note="Recommend"),
                row("C. As B, click-and-collect only", ["@omC", "@otot", "@oi26", "Breaks keep-delivery", "Backlash; weaker convenience (44% shop for it)"], note="Fallback if second-wave delivery pricing fails")],''',
'''            "columns": ["FY2028 operating income", "FY2028 margin", "FY2026 income", "Owners and board", "Main risks"],
            "rows": [
                row("A. Draft: 8% hours cut, e-commerce freeze", ["@oidraft", "About 1.1%", "Met on paper if the cut lands early", "Kept", "Shrink, service, fresh; promotions untouched"], note="Reject"),
                row("B. Margin-first plan", ["@oifirm", "2.6% on firm levers; 3.4% with the full second wave", "@oi26", "Kept; 3 other stores need a board vote", "Traffic response; vendor push-back"], highlight=True, note="Recommend"),
                row("C. As B, click-and-collect only", ["@optC", "About 3.0% on firm levers", "@oi26", "Breaks keep-delivery", "Backlash; weaker convenience (44% shop for it)"], note="Fallback if second-wave delivery pricing fails")],'''),
('''                    "detail": "2.6% on firm levers, 3.4% with the full second wave"},''',
'''                    "detail": "Reaches 3.0% with about half of the second wave, and keeps delivery"},'''),
('so_what="Also rejected: matching ValuMart with deeper promotions, as each extra percentage point of promo share costs about $2.1M of margin",',
 'so_what="Also rejected: deeper promotions to match ValuMart; each extra percentage point costs about $2.1M and has not fixed price perception",'),
('''           footnotes=["B: promotion, vendor funding, private label, shrink, targeted labor, delivery repricing, six store exits; second wave ready",''',
'''           footnotes=["B: promotion, vendor funding, private label, shrink, targeted labor, delivery repricing, six store exits; second wave ready",
                      "One-time cost: A small (not specified); B and C about $17M, against the $25M cap (p. {p:3f})",'''),
# 3a rounding footnote
('''           footnotes=["Areas: levers 1–4 gross margin, 5 store labor, 6 e-commerce, 7 store portfolio; ranges in appendix p. {p:b3}",''',
'''           footnotes=["Areas: levers 1–4 gross margin, 5 store labor, 6 e-commerce, 7 store portfolio; ranges in appendix p. {p:b3}; rows may not add due to rounding",'''),
# 3b
('"Targeted rebalancing saves about $5.5M a year without the shrink risk of the 8% across-the-board cut"',
 '"Targeted rebalancing saves about $5.5M a year by taking hours out only where extra hours protect least against shrink"'),
('"Unlike the 8% cut, it does not move every store toward the leanest quartile\'s 3.1% shrink"]},',
 '"Evidence is medium: the shrink-by-quartile pattern is a correlation, so the 10-store shrink pilot tests it before scaling"]},'),
# 3d
('"implication": "Notice on the six now; fix test on the three, then a board vote by mid-FY2027"}},',
 '"implication": "Notice on the six now; a fix test on the three, and a board vote by mid-FY2027 if it fails"}},'),
('''                      "Gain = EBITDA losses removed + contribution on sales moved to nearby stores; confirm store P&Ls before giving notice"]))''',
'''                      "Confirm store P&Ls before giving notice; the fix test on the other three (range, fresh, labor) runs over the next six months"]))'''),
# 3e
('"**Starting levers are not enough:** promotions, vendor funding and delivery give only about $13M, 37% of the gap",',
 '"**Starting levers are not enough:** promotions, vendor funding and delivery give about $13M, so the plan adds shrink, labor and store exits",'),
('''           footnotes=["Margins on pro-forma sales: $1,503M (FY2025), $1,444M (six stores exited), $1,415M (nine exited); 3.0% target $42–43M",''',
'''           footnotes=["Margins on pro-forma sales: $1,503M (FY2025), $1,444M (six stores exited), $1,415M (nine exited); 3.0% target $42–43M",
                      "FY2028 with no action: $7.7M (0.5%); gross-margin levers are $16.97M unrounded, $16.9M as the sum of rounded rows",'''),
# 4b
('{"start": "Rest of FY2026", "end": "FY2027", "label": "Fix test, then board vote on the other three"}]},',
 '{"start": "Rest of FY2026", "end": "FY2027", "label": "Fix test on the other three; board vote if it fails"}]},'),
# 5a
('''           layout={"variant": "takeaway_sidebar", "sidebar": {"kind": "bullets", "header": "The second wave is the buffer in every case",''',
'''           layout={"variant": "takeaway_sidebar", "sidebar": {"kind": "bullets", "header": "On the firm levers alone, FY2028 margin spans 1.7% to 3.2%",'''),
('''                               "**High case:** promo share back to 24%, private label at 22%, 4% fewer hours",
                               "**Robust:** the diagnosis and the case against the 8% cut hold in every case"]}},''',
'''                               "**High case:** promo share back to 24%, private label at 22%, 4% fewer hours"]}},'''),
('''           footnotes=["Low and high cases vary one driver per lever (appendix p. {p:b3}); margins on pro-forma sales of $1,444M",
                      "What changes between cases is how much of the second wave is needed, not the diagnosis or the recommendation"]))''',
'''           footnotes=["Low and high cases vary one driver per lever (appendix p. {p:b3}); margins on pro-forma sales of $1,444M"]))'''),
# 5b order + title + robustness line
('"Vendor funding and traffic response are the key risks; each has a trigger, and the diagnosis holds under every test"',
 '"Traffic response and vendor funding are the key risks; each has a trigger, and the diagnosis holds under every test"'),
('''               row("Vendor funding recovery", ["46% → 50%", "Stays at 46%", "@s_vf", "Funding share, next two promo cycles", "Drop events vendors will not fund"], highlight=True),
               row("Traffic response to fewer promotions (ValuMart)", ["25% of gross gain lost", "50% lost", "@s_traf", "Comps in ValuMart trade areas below −4.2%", "Keep depth in exposed stores; lead with private label"], highlight=True),''',
'''               row("Traffic response to fewer promotions (ValuMart)", ["25% of gross gain lost", "50% lost", "@s_traf", "Comps in ValuMart trade areas below −4.2%", "Keep depth in exposed stores; lead with private label"], highlight=True),
               row("Vendor funding recovery", ["46% → 50%", "Stays at 46%", "@s_vf", "Funding share, next two promo cycles", "Drop events vendors will not fund"], highlight=True),'''),
('''           unit_line="**Sensitivity of the plan**, change in FY2028 operating income against the base plan of $37.8M on the firm levers"))''',
'''           unit_line="**Sensitivity of the plan**, change in FY2028 operating income against the base plan of $37.8M on the firm levers",
           so_what="In every row, gross margin and delivery stay the main causes and the 8% cut stays inferior; only the second wave needed changes",
           so_what_style="line"))'''),
# 5c
('so_what="If the second wave falls short, click-and-collect only reaches about 3.0%, with the owners\' consent"))',
 'so_what="If the second wave falls short, click-and-collect only reaches about 3.0%, but needs the owners\' consent"))'),
('"detail": ["Fix test and a board vote on the three other stores by mid-FY2027 ($7.5M)", "Cost-recovery delivery pilot", "Vendor terms toward FY2023\'s 55% funding"]}]},',
 '"detail": ["Fix test on the three other stores; a board vote by mid-FY2027 ($7.5M) if it fails", "Cost-recovery delivery pilot", "Vendor terms toward FY2023\'s 55% funding"]}]},'),
# b1 footnote
('"Hours: 7.02 × $1,420M = 9.97M (FY2023); 6.60 × $1,503M = 9.92M (FY2025). Figures may not sum due to rounding"',
 '"Hours: 7.02 × $1,420M = 9.97M (FY2023); 6.60 × $1,503M = 9.92M (FY2025). Ratios shown rounded; changes computed unrounded"'),
])
b=open('build.py').read()
i0=b.index('exec_summary = ['); i1=b.index('next_steps = [')
b=b[:i0]+'''exec_summary = [
    {"id": "1", "text": "Promotions, shrink and home delivery drove the decline, not wages",
     "supports": by_sec["1"], "sub_points": [
        {"text": "Gross margin and e-commerce fulfillment explain 79% of the fall; store labor only 13%", "slide_id": "1b"},
        {"text": "Fully costed, e-commerce loses about $10M a year, not the reported +6.1%; delivery loses $12 an order", "slide_id": "1g"}]},
    {"id": "2", "text": "The draft 8% labor cut and e-commerce freeze would stall margin near 1.1%",
     "supports": by_sec["2"], "sub_points": [
        {"text": "The cut saves $14.5M on paper, but we expect $4–8M of it back as shrink, before any lost sales", "slide_id": "2a"},
        {"text": "Only margin-first reaches 3.0% and keeps delivery; closing delivery is a fallback needing owner consent", "slide_id": "2b"}]},
    {"id": "3", "text": "Seven firm levers worth $30M reach 2.6%; a prepared second wave closes the gap to 3.0%",
     "supports": by_sec["3"], "sub_points": [
        {"text": "Gross margin $17.0M, labor $5.5M, delivery $3.3M, store exits $4.4M; range $17–38M", "slide_id": "3a"},
        {"text": "About half of the $9.9M second wave is needed; one-time cost of $17M stays inside the $25M cap", "slide_id": "3e"}]},
    {"id": "4", "text": "Four no-regret moves in 90 days keep FY2026 about $5M above the covenant; we ask for three decisions",
     "supports": by_sec["4"], "sub_points": [
        {"text": "Endorse the plan over the 8% cut, approve delivery repricing, prepare the second wave and 3-store vote", "slide_id": "5c"},
        {"text": "A mid-FY2027 checkpoint below about 2.4% triggers the full wave; key risks: ValuMart traffic, vendors", "slide_id": "4b"}]},
]

'''+b[i1:]
# end page before appendix
a='''slides += [s for s in S if s["role"] in ("appendix_divider", "backup")]
slides.append({"id": "end", "role": "end_page", "status": "filled"})'''
assert b.count(a)==1
b=b.replace(a,'''slides.append({"id": "end", "role": "end_page", "status": "filled"})
slides += [s for s in S if s["role"] in ("appendix_divider", "backup")]''')
open('build.py','w').write(b)
