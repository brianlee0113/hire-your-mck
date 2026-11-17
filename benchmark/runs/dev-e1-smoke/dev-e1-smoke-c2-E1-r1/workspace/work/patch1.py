import pathlib
p = pathlib.Path('work/build_spec.py'); s = p.read_text()

def between(a, b, new):
    global s
    i = s.index(a); j = s.index(b, i)
    s = s[:i] + new + s[j:]

# ---- slide 2 data points
between("# ---------------------------------------------------------------- slide 2: labor",
        "# ---------------------------------------------------------------- slide 3",
'''# ---------------------------------------------------------------- slide 2: labor
der("wage_chg", "2", "Change in average hourly wage incl. benefits", "%", "FY2023–25", "wage25 / wage23 - 1", "18.38 ÷ 16.80 − 1 = +9.4%", "KPI 1", rnd=4)
der("hrs_chg", "2", "Change in labor hours per $1,000 of total sales", "%", "FY2023–25", "hrs25 / hrs23 - 1", "6.60 ÷ 7.02 − 1 = −6%", "KPI 2 driver text", rnd=2)
der("hrsT23", "2", "Total store labor hours", "M hours", "FY2023", "lab23 / wage23", "$167.6M ÷ $16.80 = 9.98M hours", "KPI 2 relation", rnd=3)
der("hrsT25", "2", "Total store labor hours", "M hours", "FY2025", "lab25 / wage25", "$181.9M ÷ $18.38 = 9.90M hours", "KPI 2 relation", rnd=3)
der("hrsT_chg", "2", "Change in total store labor hours", "%", "FY2023–25", "hrsT25 / hrsT23 - 1", "9.90 ÷ 9.98 − 1 = −0.8%", "KPI 2", rnd=3)
der("lab_usd", "2", "Increase in store labor cost", "$M", "FY2023–25", "lab25 - lab23", "181.9 − 167.6 = $14.3M", "KPI 3, title", rnd=1)
der("labps23", "2", "Store labor, % of in-store (non-e-commerce) sales", "%", "FY2023", "lab23 / (sales23 - sales23 * es23)", "167.6 ÷ 1,377.4 = 12.2%", "KPI 3 relation", rnd=3)
der("labps25", "2", "Store labor, % of in-store (non-e-commerce) sales", "%", "FY2025", "lab25 / (sales25 - sales25 * es25)", "181.9 ÷ 1,375.2 = 13.2%", "KPI 3 relation", rnd=3)
der("ps_usd", "2", "Gross margin lost to deeper promotions and higher shrink, at FY2025 sales", "$M", "FY2023–25",
    "(0 - w_promo - w_shr) * sales25", "(0.70 + 0.50) pp × $1,503M = $18.0M", "KPI 4 driver", rnd=1)
der("ecf_up", "2", "Increase in e-commerce fulfillment cost", "$M", "FY2023–25", "ecf25 - ecf23", "18.1 − 5.2 = $12.9M", "KPI 4 driver", rnd=1)
der("pse_usd", "2", "Cost of promotions, shrink and e-commerce fulfillment changes", "$M", "FY2023–25", "ps_usd + ecf_up", "18.0 + 12.9 = $30.9M", "KPI 4", rnd=1)
der("wage_hw", "2", "Cost of the 2027 minimum-wage rise on store labor", "$M", "a year from 2027",
    "wage27 * lab25", "4% × $181.9M = $7.3M", "KPI driver text; FY2028 bridge", estimate=True,
    assumptions=["The 4% rise is applied to the whole FY2025 store wage bill of $181.9M",
                 "Hours stay at the FY2025 level"], rnd=3)
der("wage_avg", "13", "Average yearly rise in the hourly wage", "%", "FY2023–25", "(wage25 / wage23 - 1) / 2", "9.4% ÷ 2 = 4.7% a year", "assumption text", rnd=3)
der("wage_drift", "13", "Cost of one more year of wage inflation at the FY2023–25 pace, prices flat", "$M", "a year",
    "wage_avg * lab25", "4.7% × $181.9M = $8.5M", "assumption text", estimate=True,
    assumptions=["Hourly wages keep rising at the FY2023–25 average of 4.7% a year", "Prices and sales do not rise with them"], rnd=2)

''')

# ---- slides 7-8 data points
between("# ---------------------------------------------------------------- slide 7: shrink by staffing quartile",
        "# ---------------------------------------------------------------- slide 9",
'''# ---------------------------------------------------------------- slide 7: shrink by staffing quartile
A_SHR = ["The four staffing quartiles carry equal sales; their simple average, 2.6%, matches the chain's FY2025 shrink",
         "Stores in Q1 and Q2 reach the 2.4% of Q3 by restoring produce rotation and receiving checks",
         "The hours this needs are not yet costed, so the saving is second-wave upside, not part of wave one"]
der("shr_gain", "7", "Upside from bringing Q1 and Q2 stores to the Q3 shrink level", "$M", "a year",
    "((q1 - q3) + (q2 - q3)) / 4 * sales25", "((3.1% − 2.4%) + (2.7% − 2.4%)) ÷ 4 × $1,503M = $3.8M", "sidebar row 1",
    estimate=True, assumptions=A_SHR, rnd=3)
der("fixable", "7", "Share of shrink from fresh waste and receiving or admin errors", "%", "FY2025", "waste + admin",
    "45% + 20% = 65%", "sidebar row 2", rnd=3)

# ---------------------------------------------------------------- slide 8: targeted hours cut
A_LAB = ["Quartiles carry equal sales, so Q3 and Q4 stores, which use the most hours per sales dollar, hold at least half of store hours",
         "If their shrink rose all the way to Q2's 2.7%, a cautious case: Q3 and Q4 shrink differ by only 0.1 percentage points today",
         "Labor cost per hour is the same across stores"]
der("q34", "8", "Shrink gap between the third and fourth staffing quartiles", "pp", "FY2025", "(q3 - q4) * 100", "2.4% − 2.3% = 0.1 pp", "assumption text", rnd=3)
der("lab_tgt_save", "8", "Saving from cutting 8% of hours in Q3 and Q4 stores (lower bound)", "$M", "a year",
    "mgmt_cut * lab25 / 2", "8% × $181.9M × 50% = $7.3M", "equation term 1", estimate=True, assumptions=A_LAB, rnd=3)
der("giveback", "8", "Shrink give-back if Q3 and Q4 shrink rose to Q2's level (cautious case)", "$M", "a year",
    "((q2 - q3) + (q2 - q4)) / 4 * sales25", "((2.7% − 2.4%) + (2.7% − 2.3%)) ÷ 4 × $1,503M = $2.6M", "equation term 2",
    estimate=True, assumptions=A_LAB, rnd=3)
der("lab_tgt_net", "8", "Net saving from the targeted hours cut (at least)", "$M", "a year", "lab_tgt_save - giveback",
    "7.3 − 2.6 = $4.7M", "equation result, title; FY2028 bridge", estimate=True, assumptions=A_LAB, rnd=3)

''')

# ---- slides 13-15 data points
between("# ---------------------------------------------------------------- slide 13: FY2028 bridge",
        "# ================================================================ storyline",
'''# ---------------------------------------------------------------- slide 13: FY2028 bridge
A_BR = ["FY2025 costs and sales hold flat apart from the moves and headwinds shown; the FY2023–25 drift in promotions and shrink stops",
        "The 4% minimum-wage rise falls on the whole store wage bill; other wage inflation is matched by prices",
        "If wages kept rising 4.7% a year with prices flat, each further year would cost about $8.5M",
        "FY2028 sales of $1,443M: FY2025 sales less the six exited stores' sales not recaptured and online sales lost to the fee change"]
der("gm28", "13", "Gross-margin moves by FY2028: promotions and private label", "$M", "a year by FY2028",
    "promo_gain + pl_gain", "10.5 + 4.1 = $14.6M", "equation term 2", estimate=True, assumptions=A_BR, rnd=3)
der("st28", "13", "Store-cost moves by FY2028: targeted hours cut and six store exits", "$M", "a year by FY2028",
    "lab_tgt_net + gain6", "4.6 + 4.4 = $9.1M", "equation term 3", estimate=True, assumptions=A_BR, rnd=3)
der("hw28", "13", "Headwinds by FY2028: minimum-wage and delivery-rate rises", "$M", "a year by FY2028",
    "wage_hw + rate_hw", "7.3 + 0.3 = $7.6M", "equation term 5", estimate=True, assumptions=A_BR, rnd=3)
der("oi28", "13", "FY2028 operating income with wave one", "$M", "FY2028E",
    "oi25 + gm28 + st28 + fee_gain - hw28", "15.3 + 14.6 + 9.1 + 2.8 − 7.6 = $34.2M", "equation result", estimate=True, assumptions=A_BR, rnd=3)
der("sales28", "13", "FY2028 sales with wave one", "$M", "FY2028E",
    "sales25 - st_sales * 6 / 9 * (1 - st_tr) - ec25 * (0 - ft_sales) * newsh", "1,503 − 78.7 × 75% − 127.8 × 2% × 30% = $1,443M",
    "row basis", estimate=True, assumptions=A_BR, rnd=3)
der("m28", "13", "FY2028 operating margin with wave one", "%", "FY2028E", "oi28 / sales28", "34.2 ÷ 1,443 = 2.4%", "sidebar row 1, title",
    estimate=True, assumptions=A_BR, rnd=4)
der("m28lo", "13", "FY2028 operating margin, low case: promotions back only to FY2024 depth", "%", "FY2028E",
    "(oi28 - promo_gain + promo_low) / sales28", "(34.2 − 10.5 + 5.9) ÷ 1,443 = 2.1%", "sidebar row 2", estimate=True, assumptions=A_BR, rnd=3)
der("need28", "13", "FY2028 operating income needed for a 3.0% margin", "$M", "FY2028E", "tgt * sales28",
    "3.0% × $1,443M = $43.3M", "audit", estimate=True, assumptions=A_BR, rnd=3)
der("gap28", "13", "Operating income still to find for the 3.0% target after wave one", "$M", "FY2028E", "need28 - oi28",
    "43.3 − 34.2 = $9.1M", "exec summary", estimate=True, assumptions=A_BR, rnd=1)

# ---------------------------------------------------------------- slide 14: second wave
A_SW = ["The 14 percentage-point promotional margin gap is net of vendor funding (the FY2023–25 gross-margin bridge closes without a separate funding effect), so gross markdowns are about 26% of promotional sales",
        "Vendors return to FY2023's 55% share of markdowns, on promotions held at FY2023's 24% of sales",
        "The three stores with longer leases carry a third of the nine stores' sales and four-wall losses"]
der("sales_sw", "14", "FY2028 sales with wave one and three more store exits", "$M", "FY2028E",
    "sales28 - st_sales * 3 / 9 * (1 - st_tr)", "1,443 − 39.3 × 75% = $1,414M", "assumption text", estimate=True, assumptions=A_SW, rnd=3)
der("gross_md", "14", "Gross promotional markdown, % of promotional sales, before vendor funding", "%", "FY2025",
    "promo_gap / 100 / (1 - vf25)", "14% ÷ (1 − 46%) = 26%", "assumption text", estimate=True, assumptions=A_SW, rnd=2)
der("vf_gain", "14", "Operating income added by vendor funding back at 55% of markdowns", "$M", "a year by FY2028",
    "(vf23 - vf25) * gross_md * promo23 * sales_sw", "9 pp × 26% × 24% × $1,414M = $7.9M", "equation term 1", estimate=True, assumptions=A_SW, rnd=3)
der("sw_add", "14", "Operating income added by the sized second wave", "$M", "a year by FY2028", "vf_gain + gain3",
    "7.9 + 2.2 = $10.2M", "equation result, title", estimate=True, assumptions=A_SW, rnd=3)
der("m_sw", "13", "FY2028 operating margin with wave one and the sized second wave", "%", "FY2028E",
    "(oi28 + sw_add) / sales_sw", "(34.2 + 10.2) ÷ 1,414 = 3.1%", "slide 13 sidebar row 3; slide 14 assumption", estimate=True, assumptions=A_SW, rnd=4)
der("vf_need", "14", "Vendor-funded share of markdowns needed to reach the 3.0% target", "%", "FY2028E",
    "vf25 + (tgt * sales_sw - oi28 - gain3) / (gross_md * promo23 * sales_sw)", "46% + ($42.4M − $36.4M) ÷ $88.2M per 100 pp = 53%",
    "so-what bar", estimate=True, assumptions=A_SW, rnd=2)
der("be_fee", "14", "Delivery fee per delivered order at which a home delivery breaks even", "$", "FY2025",
    "pick_u + delc_u - basket * newsh * ncontrib", "$7.40 + $13.80 − $5.76 = $15.44", "assumption text", rnd=2)

# ---------------------------------------------------------------- slide 15: roadmap and covenant
der("cov_gap", "15", "Covenant shortfall if FY2026 operating income stayed at the FY2025 level", "$M", "FY2026", "oi25 - cov",
    "15.3 − 20.0 = −$4.7M", "sidebar row 3", rnd=1)
der("del_kept", "11", "Share of home deliveries kept after the fee change", "%", "test", "1 + ft_del", "1 − 9% = 91%", "sidebar bullet", rnd=3)


''')
p.write_text(s)
print("ok")
