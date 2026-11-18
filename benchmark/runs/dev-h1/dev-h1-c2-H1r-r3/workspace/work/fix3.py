def edit(f, pairs):
    s=open(f).read()
    for a,b in pairs:
        assert s.count(a)==1,(f,a[:70],s.count(a)); s=s.replace(a,b)
    open(f,'w').write(s)
edit('slides.py',[
('"The draft plan leaves FY2028 margin near 1.1%: added shrink erodes the labor saving, and the freeze keeps e-commerce losses"',
 '"The draft plan stalls FY2028 margin near 1.1%: shrink erodes the labor saving, and the freeze keeps e-commerce losses"'),
('so_what="Rebalance hours instead of cutting them: lean stores skip produce and receiving checks, and those errors are 65% of shrink",',
 'so_what="Rebalance hours rather than cut them: waste and receiving errors make up 65% of shrink",'),
('''           footnotes=["Labor % = hours per $1,000 × wage; 11.79% and 12.13% differ from the pack's 11.8% and 12.1% by rounding",''',
'''           footnotes=["Managers in the leanest stores say produce rotation and receiving checks are skipped on busy days",
                      "Labor % = hours per $1,000 × wage; 11.79% and 12.13% differ from the pack's 11.8% and 12.1% by rounding",'''),
('''                   "bullets": ["**Break-even:** delivery needs 94% of its sales to be new to Harlow, click-and-collect 39%; the survey says 30%",
                               "**Mix shift:** delivery rose from 45% to 58% of orders as fees fell from 26% to 22% of its cost"],
                   "implication": "Subsidized delivery is the problem, not e-commerce: a freeze locks in the loss"}},''',
'''                   "bullets": ["**Break-even:** delivery needs 94% of its sales to be new to Harlow, click-and-collect 39%; the survey says 30%",
                               "**Freeze locks in the loss:** the problem is subsidized home delivery, not e-commerce as such"]}},'''),
('''           footnotes=["Contribution per order = $96 basket × 30% new to Harlow (survey, n = 2,300) × 20 cents (finance); costs match Table 1 (p. {p:b2})"]))''',
'''           footnotes=["Contribution per order = $96 basket × 30% new to Harlow (survey, n = 2,300) × 20 cents (finance); costs match Table 1 (p. {p:b2})",
                      "Delivery rose from 45% to 58% of orders while fees fell from 26% to 22% of delivery cost"]))'''),
('"columns": ["FY2028 margin", "One-time cost", "FY2026 income", "Commitments", "Main risks"],',
 '"columns": ["FY2028 margin", "One-time cost", "FY2026 income", "Owners and board", "Main risks"],'),
(''',
                      "Not levers: other SG&A flat at 4.7% of sales; occupancy rose 0.2 percentage points and is partly addressed by the store exits"]))''',
 ''']))'''),
('''                   "bullets": ["**A quarter of the loss:** repricing fixes about 24% of the $10.4M",
                               "**Next test:** cost-recovery pricing or membership; halving the rest is worth $3.2M"]}},''',
'''                   "bullets": ["**A quarter of the loss:** repricing fixes 24% of the $10.4M; halving the rest is worth $3.2M"]}},'''),
('''"Per delivered order after repricing: $5.76 − $7.40 − $13.80 + $6.40 = −$9.04"]))''',
'''"Per delivered order after repricing: $5.76 − $7.40 − $13.80 + $6.40 = −$9.04; next test: cost-recovery pricing or a paid membership"]))'''),
('so_what="If the second wave falls short, click-and-collect only reaches about 3.0%, but closing delivery needs the owners\' consent"))',
 'so_what="If the second wave falls short, click-and-collect only reaches about 3.0%, with the owners\' consent"))'),
('row("6. Delivery pricing and contract", ["Test result −20%; no contract gain", "@lo6", "@lev6", "@hi6", "Test +30%; contract −5%", "@del26"]),',
 'row("6. Delivery pricing", ["Test −20%, no contract", "@lo6", "@lev6", "@hi6", "Test +30%, contract −5%", "@del26"]),'),
('row("FY2028 operating income ($7.7M + levers)", ["", "@oilo", "@oifirm", "@oihi", "", ""]),', 'row("FY2028 operating income", ["", "@oilo", "@oifirm", "@oihi", "", ""]),'),
('row("FY2028 operating margin (on $1,444M)", ["", "@omlo", "@omfirm", "@omhi", "", ""], highlight=True)]},', 'row("FY2028 margin", ["", "@omlo", "@omfirm", "@omhi", "", ""], highlight=True)]},'),
('''                      "Store-exit low and high (3.0, 5.0) are the analysis's estimates; the pack gives only totals for the nine stores"]))''',
'''                      "Store-exit low and high (3.0, 5.0) are the analysis's estimates; the pack gives only totals for the nine stores",
                      "Not levers: other SG&A flat at 4.7% of sales; occupancy rose 0.2 percentage points, partly addressed by the store exits"]))'''),
('"columns": ["Low-case driver", "Low", "Base", "High", "High-case driver", "FY2026 in-year"], "rows": [',
 '"columns": ["Low driver", "Low", "Base", "High", "High driver", "FY2026"], "rows": ['),
])
s=open('slides.py').read()
for sid in ("5a","5b","5c","5d"):
    a='S.append(C("%s", "5",'%sid; assert s.count(a)==1; s=s.replace(a,'S.append(C("%s", "4",'%sid)
a='S.append(B("b5", "5", "5b",'; assert s.count(a)==1; s=s.replace(a,'S.append(B("b5", "4", "5b",')
open('slides.py','w').write(s)
