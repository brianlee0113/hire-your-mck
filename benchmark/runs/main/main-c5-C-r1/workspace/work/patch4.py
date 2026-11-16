p='build_data.py'; s=open(p).read()
R=[('der("w_ratio", "Ratio of last-week daily orders to the six-week average at steady 18% weekly growth", "x",',
    'der("w_ratio", "Last-week daily orders as a share of the six-week average at steady 18% weekly growth", "%",'),
   ('der("exit_opd", "Pop-up orders per day in its last week", "orders", "pu_opd * w_ratio", "280 × ratio", estimate=True, assumptions=WA, nd=1)',
    'der("exit_opd", "Pop-up orders per day in its last week", "orders", "pu_opd * w_ratio", "280 × ratio", estimate=True, assumptions=WA, nd=0)'),
   ('der("cac_pb", "Months to repay acquisition cost at the founders\' plan contribution per order", "months", "cac / (opc * cpo_p)",',
    'der("cac100", "Cost to acquire a hundred customers at the pop-up\'s acquisition cost", "$", "cac * 100", "$38 × 100")\n'
    'der("opc100", "Orders a month from a hundred acquired customers, from month three", "orders", "ret3 * freq * 100", "22 still ordering × 3.1 orders a month", nd=1)\n'
    'der("cac_pb", "Months to repay acquisition cost at the founders\' plan contribution per order", "months", "cac100 / opc100 / cpo_p",'),
]
for a,b in R:
    assert a in s, a[:60]; s=s.replace(a,b)
open(p,'w').write(s)
p='build_spec.py'; s=open(p).read()
R=[('("×", "w_ratio", "last week against the six-week average, at a steady 18% a week")','("×", "w_ratio", "last week\'s daily rate against the six-week average, at a steady 18% a week")'),
   ('''      eq([(None, "cac", "to acquire a customer in the pop-up: paid social and first-order credits"),
          ("÷", "opc", "orders a month per acquired customer: 22% stay × 3.1 orders"),''',
    '''      eq([(None, "cac100", "to acquire a hundred customers at the pop-up's $38 each (paid social, first-order credits)"),
          ("÷", "opc100", "orders a month from them after month three: 22 stay × 3.1 orders"),'''),
   ('LM("Even on the founders\' plan economics, a new customer takes about 28 months to repay the $38 it costs to win",\n                     nums=[("28 months", "cac_pb"), ("$38", "cac")])',
    'LM("Even on the founders\' plan economics, a new customer takes about 28 months to repay what it cost to acquire",\n                     nums=[("28 months", "cac_pb")])'),
   ('"caption": "of runway left at month 18 if the $9.5M covers all spending"','"caption": "months of runway left at month 18 if the $9.5M covers all spending"'),
   ('"caption": "of runway with the hires at today\'s burn"','"caption": "months of runway with the hires at today\'s burn"'),
   ('''      node="n2c",
      unit_line="**Contribution per order, median site with Zipcart's two moves**, $ per order, team estimate"))''',
    '''      node="n2c",
      unit_line="**Contribution per order, median site with Zipcart's two moves**, $ per order, team estimate",
      footnotes=["Cards are rounded; the calculation uses unrounded values (sources workbook, Calculations sheet)"]))'''),
]
for a,b in R:
    assert a in s, a[:60]; s=s.replace(a,b)
open(p,'w').write(s); print('ok')
