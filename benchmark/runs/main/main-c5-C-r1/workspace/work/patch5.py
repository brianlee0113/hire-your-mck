p='build_data.py'; s=open(p).read()
R=[('der("late_arr", "ARR from the nine late-stage grocers at the average contract value", "$M", "late * acv / 1000", "9 × $96,000")',
    'der("late_arr", "ARR from the nine late-stage grocers at the average contract value", "$K", "late * acv", "9 × $96,000")'),
   ('"late_arr / sw_cost", "$0.86M ÷ $0.8M"','"late_arr / 1000 / sw_cost", "$864K ÷ $0.8M"'),
   ('"late_arr * gm_sw", "$0.86M × 81%"','"late_arr * gm_sw / 1000", "$864K × 81%"'),
   ('der("be_opd_z",','der("var_z", "Order margin before site costs, median basket with Zipcart\'s fee and promotion cut", "$", "var_m + zfee + zp_save", "median order margin + $3.99 fee + promotion saving", assumptions=ZA[:1])\nder("be_opd_z",'),
]
for a,b in R:
    assert a in s, a[:60]; s=s.replace(a,b)
open(p,'w').write(s)
p='build_spec.py'; s=open(p).read()
R=[('"The regional gap Parcelbird sees may be one rivals left"','"The closest precedent for a regional launch"'),
   ('"metric": "times the cash in the bank, lost each year"','"metric": "the cash in the bank, lost each year by nine median stores"'),
   ('"caption": "times the cash in the bank, lost each year at the median"','"caption": "the cash in the bank, lost each year at the median"'),
   ('LM("The nine late-stage deals alone are worth $0.86M a year, more than the hires needed to scale the software",\n                    nums=[("$0.86M", "late_arr")])',
    'LM("The nine late-stage deals alone are worth $864K a year, more than the hires needed to scale the software",\n                    nums=[("$864K", "late_arr")])'),
   ('"The nine late-stage deals are worth $0.86M a year, more than the hires"','"The nine late-stage deals are worth $864K a year, more than the hires"'),
   ('so_what="For a tenth of the plan\'s $9.5M','so_what="For under a tenth of the plan\'s $9.5M'),
   ('{"label": "Median with Zipcart\'s pricing", "cells": [{"point": P("cpo_z0")}, {"point": P("be_opd_z")}]',
    '{"label": "Median with Zipcart\'s pricing", "cells": [{"point": P("var_z")}, {"point": P("be_opd_z")}]'),
   ('; the Zipcart row shows contribution after site costs at 900 orders a day in the first column"','"'),
]
for a,b in R:
    assert a in s, a[:60]; s=s.replace(a,b)
open(p,'w').write(s); print('ok')
