p='build_spec.py'; s=open(p).read()
R=[("Neither incumbent makes money on an order, and the regional operator is already shrinking","Scale has not brought profit: neither incumbent makes money on an order it delivers"),
("No dark store we can observe earns a profit on an order, and the plan needs inputs no site has reached","No observed dark store makes a profit on an order — the plan depends on inputs no site has reached"),
('LM("The plan\'s profit rests on four assumptions, and 46% of their effect lies beyond the best site observed",\n                     nums=[("46%", "beyond")], hl=[], count=4)',
 'LM("Nearly half of the plan\'s gain per order, 46%, depends on inputs beyond the best site ever observed",\n                     nums=[("46%", "beyond")], hl=[])'),
("Each of the plan's four key inputs is set above the best benchmark site, and rider productivity is furthest out","Each of the plan's four key inputs is set above the best benchmark site, rider productivity most of all"),
("The plan absorbs rider cost only up to $24.8 an hour, and two launch cities are weighing pay floors","With two launch cities weighing pay floors, the plan absorbs rider cost only up to $24.8 an hour"),
("Parcelbird's own test ran below the benchmark, and too few customers stayed to repay their acquisition","Parcelbird's own test ran below the benchmark on every input, with too few customers staying to repay acquisition"),
("The pop-up drew under a third of median volume, and it bought that volume with twice the median promotions","The pop-up drew under a third of median volume while spending twice the median rate on promotions"),
("The plan breaks the board's runway rule, and a median outcome would lose more each year than the company holds","The plan breaks the runway rule, while a median outcome would lose more each year than the company holds"),
("In 2027 the cash goes to the software pipeline first, with a board review of the operator idea in the fourth quarter","The 2027 plan puts cash into the software pipeline and reviews the operator idea in the fourth quarter"),
("Four gates would justify revisiting Parcelbird Now, and today none of them is met","None of the four gates for revisiting Parcelbird Now is met today"),
("Saying no carries four risks, and each has an early signal and an owner","Each of the four risks of saying no has an early signal and an owner"),
("The plan departs from the benchmark on four of ten per-order inputs and holds the other six at the median","The plan departs from the benchmark median on four of its ten per-order inputs"),
("Line by line, the rider and site costs decide every case, and only the plan's inputs turn them positive","Line by line, rider and site costs decide every case: only the plan's inputs turn them positive"),
('LM("A median dark store loses $6.2 on every order, because its costs run 55% above what an order earns",\n                     nums=[("$6.2", "cpo_m"), ("55%", "cost_x")], hl=[])',
 'LM("A median dark store loses $6.2 on every order, as riders, site and picking alone cost more than an order earns",\n                     nums=[("$6.2", "cpo_m")], hl=[])'),
('"header": "Costs are 1.55 times what an order earns"','"header": "Costs run far above what an order earns"'),
(',\n                 "Cost per order ÷ earned per order = 1.55, so costs run 55% above earnings"]',']'),
('LM("Even after six weeks of 18% weekly growth, the pop-up ended at about 400 orders a day, under half the median",\n                     nums=[("18%", "pu_growth"), ("400", "exit_opd")])',
 'LM("Even after six weeks of fast growth, the pop-up ended at about 400 orders a day, under half the median",\n                     nums=[("400", "exit_opd")])'),
('LM("The plan needs $9.5M, but only $7.2M can be spent while keeping 12 months of runway",\n                     nums=[("$9.5M", "need"), ("$7.2M", "spend"), ("12 months", "rwy_min")])',
 'LM("The plan needs $9.5M, but only $7.2M can be spent without breaking the runway rule",\n                     nums=[("$9.5M", "need"), ("$7.2M", "spend")])'),
('{"code": "2c", "text": "Copying Zipcart\'s fee and promotion cuts still leaves a median site losing money", "point": P("cpo_z"),\n           "metric": "contribution per order with Zipcart\'s pricing and volume loss"}',
 '{"code": "2c", "text": "Copying Zipcart\'s fee and promotion cuts still leaves a median site losing money", "point": P("be_opd_z"),\n           "metric": "orders a day a median site would need at Zipcart\'s prices, against 900 today"}'),
('leaf("n2d", "2d", "n2", "The economics hold if launch cities set minimum pay for delivery riders", "medium", "low",','leaf("n2d", "2d", "n2", "The economics hold if launch cities set minimum pay for delivery riders", "medium", "medium",'),
('"text": "Parcelbird\'s own pop-up ran below the benchmark, and too few customers stayed to repay their acquisition"','"text": "Parcelbird\'s own pop-up ran below the benchmark on every input, and too few customers stayed to repay their acquisition"'),
]
for a,b in R:
    assert a in s, a[:70]
    s=s.replace(a,b)
b6=open('b6.txt').read()
s=s.replace('add({"id": "end", "role": "end_page", "status": "filled"})', b6+'add({"id": "end", "role": "end_page", "status": "filled"})')
open(p,'w').write(s)
print("ok")
