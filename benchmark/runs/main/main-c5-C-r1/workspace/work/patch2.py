p='build_spec.py'; s=open(p).read()
R=[('hm_cols = ["AOV, $", "Promotions, % of AOV", "Orders per rider-hour", "Orders per site per day", "Contribution per order, $"]',
    'hm_cols = ["AOV, $", "Promos, % of AOV", "Orders per rider-hour", "Orders per site a day", "Result per order, $"]'),
   ('"low_is_better": ["Promotions, % of AOV"]','"low_is_better": ["Promos, % of AOV"]'),
   ('"Darker = better for the case; low end uses','"Result per order = contribution after site fixed cost; darker = better; low end uses'),
   ('so_what="The pop-up also trailed on basket ($31 against $34) and riders (2.1 orders an hour against 2.4): knowing the software did not make a better site"',
    'so_what="It also trailed on basket and rider speed: knowing the software did not make a better site"'),
   ('''          {"point": P("need"), "caption": "the plan's own cash need to month 18",
           "relation": "Taken as given from the founders",
           "drivers": ["Capex, launch marketing, operating losses", "Built on the plan's above-best inputs (2b)", "No downside case in the plan"]}]},''',
    '''          ]},'''),
   ('''          "implication": "One median store loses about $2.0M a year, so even a single-store trial costs real runway"}},''','''          }},'''),
   ('"governing_thought": "Do not launch Parcelbird Now in 2027: no observed dark store makes money and the plan breaks the runway rule, so grow the software business instead"',
    '"governing_thought": "Do not launch Parcelbird Now in 2027: no observed dark store makes money and the plan breaks the runway rule; grow the software instead"'),
]
for a,b in R:
    assert a in s, a[:70]
    s=s.replace(a,b)
# exec summary: shorter items, two sub-points each
start=s.index('"exec_summary": [')
end=s.index('"next_steps": [')
new='''"exec_summary": [
        {"id": "1", "text": "Quick commerce grows fast, but its operators lose money; the one profitable city got there by charging more",
         "supports": sec_slides("1"), "sub_points": [
             {"text": "US quick-commerce sales grew 2.8 times from 2022 to 2025", "slide_id": "1a1"},
             {"text": "Zipcart's best city needed a $3.99 fee and lost 14% of orders", "slide_id": "1b2"}]},
        {"id": "2", "text": "A median dark store loses $6.2 an order; the founders' profit needs inputs above the best site observed",
         "supports": sec_slides("2"), "sub_points": [
             {"text": "The best basket and density combined still lose $1.8 an order", "slide_id": "2a2"},
             {"text": "Zipcart's fee and promotion cuts still leave a $1.05 loss an order", "slide_id": "2c1"}]},
        {"id": "3", "text": "Parcelbird's pop-up ran below the benchmark, and too few customers stayed to repay their acquisition",
         "supports": sec_slides("3"), "sub_points": [
             {"text": "The pop-up lost about $12.6 on every order it delivered", "slide_id": "3a2"},
             {"text": "Only 22% of pop-up customers still ordered in month three", "slide_id": "3b1"}]},
        {"id": "4", "text": "The plan needs $9.5M, but Parcelbird can spend only $7.2M and keep 12 months of runway",
         "supports": sec_slides("4"), "sub_points": [
             {"text": "At the benchmark median, nine stores would lose $18.2M a year", "slide_id": "4b1"}]},
        {"id": "5", "text": "Grow the software business instead, and revisit Parcelbird Now only if a real site passes four gates",
         "supports": sec_slides("5"), "sub_points": [
             {"text": "The nine late-stage deals are worth $0.86M a year, more than the hires", "slide_id": "5a"}]}],
    '''
s=s[:start]+new+s[end:]
open(p,'w').write(s); print('ok')
