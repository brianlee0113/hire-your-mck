def edit(f, pairs):
    s=open(f).read()
    for a,b in pairs:
        assert s.count(a)==1,(f,a[:70],s.count(a)); s=s.replace(a,b)
    open(f,'w').write(s)
edit('dps.py',[('D("delnet",', 'D("ecloss", "Fully costed e-commerce loss, FY2025", "$M", "0 - (cc25 * npo_cc + del25 * npo_del) / 1000", "−(559k × −$1.64 + 772k × −$12.34)")\nD("delnet",')])
edit('slides.py',[
('nums=[("$10M", "ecres"), ("$12", "npo_del")],','nums=[("$10M", "ecloss"), ("$12", "npo_del")],'),
('''"sidebar": {"kind": "big_number", "big_number": r("ecres"),
                   "caption": "fully costed e-commerce result in FY2025",''','''"sidebar": {"kind": "big_number", "big_number": r("ecloss"),
                   "caption": "fully costed e-commerce loss in FY2025",'''),
('"That 1.6-percentage-point gain earns 0.32 percentage points of sales at 20 cents of contribution",','"The 1.6-percentage-point gain earns 0.32 of sales at 20 cents of contribution",'),
('"The stores were not chosen at random: it is a correlation, and sales rather than profit"]},','"A correlation in sales, not profit: the stores were not chosen at random"]},'),
('"Harlow stores within three miles of one ran comparable sales of −4.2% in FY2025, compared with +1.1% elsewhere",','"Harlow stores within three miles of one ran comps of −4.2% in FY2025, compared with +1.1% elsewhere",'),
('"Private label earns 12 percentage points more margin than national brands and can carry the value message",','"Private label earns 12 percentage points more margin and can carry the value message",'),
('row("Vendor funding recovery", ["46% → 50%", "Stays at 46%", "@s_vf", "Funding share in the next two promotion cycles", "Drop events vendors will not fund"], highlight=True),',
 'row("Vendor funding recovery", ["46% → 50%", "Stays at 46%", "@s_vf", "Funding share, next two promo cycles", "Drop events vendors will not fund"], highlight=True),'),
('row("FY2026 trading (no FY2026 data in the pack)", ["Holds at FY2025 run-rate", "Erosion continues", "About $5M of slippage uses up the covenant headroom", "Monthly operating income against the $20M path", "Brief the lender; speed up promotion cuts"])]},',
 'row("FY2026 trading (no data in the pack)", ["Holds at FY2025 run-rate", "Erosion continues", "About $5M of slippage uses up the headroom", "Monthly operating income against the $20M path", "Brief the lender; speed up promotion cuts"])]},'),
('row("Share of e-commerce sales new to Harlow", ["30%", "50%", "E-commerce loss shrinks to $5.3M", "Customer-panel and loyalty data", "None needed: delivery still loses $8.50 an order"]),',
 'row("E-commerce sales new to Harlow", ["30%", "50%", "E-commerce loss shrinks to $5.3M", "Customer panel, loyalty data", "None: delivery still loses $8.50 an order"]),'),
('"Gross margin and e-commerce fulfillment are 79% of the fall; store labor 13% (p. {p:1b})"','"Gross margin and e-commerce are 79% of the fall; labor 13% (p. {p:1b})"'),
('"38% of FY2025 events lost money; the extra promo share needs about $53M of new sales to repay (p. {p:1d})"','"38% of FY2025 events lost money; the extra share needs $53M of new sales (p. {p:1d})"'),
('"Fee test: e-commerce sales only −2%; worth about $2.5M a year, a quarter of the loss (p. {p:3c})"','"Fee test: sales only −2%; worth $2.5M a year, a quarter of the loss (p. {p:3c})"'),
('"6 of the 9 have leases ending by 2027, so no vote is needed; exit adds about $4.4M (p. {p:3d})"','"6 of the 9 leases end by 2027, so no vote; exit adds $4.4M (p. {p:3d})"'),
])
