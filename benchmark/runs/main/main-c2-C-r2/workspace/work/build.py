"""Builds the storyline spec for the Harlow Fresh Markets margin deck.

Every number is a data point: facts quote the briefing pack verbatim, derived numbers carry a calc
that this script evaluates (so values and formulas cannot drift apart)."""
import json, re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
PACK = (ROOT / "evidence" / "briefing-pack.md").read_text()

DP, V = [], {}

def _ev(calc):
    e = calc
    for k in sorted(V, key=len, reverse=True):
        e = re.sub(rf"(?<![\w.]){re.escape(k)}(?![\w-])", f"V[{k!r}]", e)
    return eval(e)

def fact(i, label, value, unit, period, excerpt, locator, **kw):
    excerpt = re.sub(r"\s+", " ", excerpt)
    assert excerpt in re.sub(r"\s+", " ", PACK), f"excerpt not verbatim for {i}: {excerpt}"
    V[i] = value
    DP.append(dict(id=i, label=label, value=value, unit=unit, period=period, source_id="s1",
                   excerpt=excerpt, locator=locator, **kw))

def assume(i, label, value, unit, period, note):
    V[i] = value
    DP.append(dict(id=i, label=label, value=value, unit=unit, period=period, source_id="s3",
                   locator=f"Planning assumption: {note}"))

def der(i, label, unit, period, calc, formula, estimate=False, assumptions=None, **kw):
    ids = [k for k in sorted(V, key=len, reverse=True) if re.search(rf"(?<![\w.]){re.escape(k)}(?![\w-])", calc)]
    val = _ev(calc)
    V[i] = val
    d = dict(id=i, label=label, value=round(val, 6), unit=unit, period=period, source_id="s2",
             derived_from=ids, formula=formula, calc=calc, **kw)
    if estimate:
        d["estimate"] = True
        d["assumptions"] = assumptions
    DP.append(d)
    return val

P = lambda i: {"data_ref": i}

# ---------------------------------------------------------------- facts: income statement (Table 1)
T1 = {"s": "| Sales | 1,420.0 | 1,468.0 | 1,503.0 |", "gp": "| Gross profit | 369.8 | 376.0 | 376.1 |",
      "lab": "| Store labor | 167.6 | 176.2 | 181.9 |", "occ": "| Occupancy and energy | 82.4 | 86.6 | 90.2 |",
      "ef": "| E-commerce fulfillment (picking + delivery, net of delivery fees) | 5.2 | 10.9 | 18.1 |",
      "sga": "| Other SG&A | 66.7 | 69.0 | 70.6 |", "oi": "| **Operating income** | **47.9** | **33.4** | **15.3** |",
      "om": "| Operating margin | 3.37% | 2.27% | 1.02% |"}
NAMES = {"s": "Sales", "gp": "Gross profit", "lab": "Store labor", "occ": "Occupancy and energy",
         "ef": "E-commerce fulfillment, net of delivery fees", "sga": "Other SG&A", "oi": "Operating income",
         "om": "Operating margin"}
VALS = {"s": (1420.0, 1468.0, 1503.0), "gp": (369.8, 376.0, 376.1), "lab": (167.6, 176.2, 181.9),
        "occ": (82.4, 86.6, 90.2), "ef": (5.2, 10.9, 18.1), "sga": (66.7, 69.0, 70.6), "oi": (47.9, 33.4, 15.3),
        "om": (0.0337, 0.0227, 0.0102)}
for k, vals in VALS.items():
    for y, v in zip((23, 24, 25), vals):
        fact(f"{k}{y}", f"{NAMES[k]}, Harlow", v, "%" if k == "om" else "$M", f"FY20{y}", T1[k],
             f"Briefing pack, section 5, Table 1, row {NAMES[k].split(',')[0]}, column FY20{y}")

# ---------------------------------------------------------------- facts: gross-margin drivers (Table 2)
for k, row, vals, lab in (("promo", "| Promotional sales, share of sales | 24.0% | 26.2% | 29.0% |", (0.24, 0.262, 0.29), "Promotional sales, share of sales"),
                          ("plsh", "| Private-label sales, share of sales | 17.0% | 17.7% | 18.5% |", (0.17, 0.177, 0.185), "Private-label sales, share of sales"),
                          ("shr", "| Shrink, % of sales | 2.1% | 2.3% | 2.6% |", (0.021, 0.023, 0.026), "Shrink, % of sales")):
    for y, v in zip((23, 24, 25), vals):
        fact(f"{k}{y}", lab, v, "%", f"FY20{y}", row, f"Briefing pack, section 5, Table 2, column FY20{y}")
fact("promo_gap", "Gross-margin gap, promotional against regular-price sales", 14, "pp", "FY2023–25",
     "Promotional sales earn 14 percentage points less gross margin than regular-price sales", "Briefing pack, section 5, note 1")
fact("pl_gap", "Gross-margin premium, private label against national brands", 12, "pp", "FY2023–25",
     "Private-label sales earn 12 percentage points more gross margin than national brands", "Briefing pack, section 5, note 2")
fact("vf23", "Vendor funding, share of promotional markdowns", 0.55, "%", "FY2023",
     "Vendor funding covered 55% of promotional markdowns in FY2023 and 46% in FY2025", "Briefing pack, section 5, note 3")
fact("vf25", "Vendor funding, share of promotional markdowns", 0.46, "%", "FY2025",
     "Vendor funding covered 55% of promotional markdowns in FY2023 and 46% in FY2025", "Briefing pack, section 5, note 3")
fact("ev38", "FY2025 promotional events that lost money after counting extra units", 0.38, "%", "FY2025",
     "38% of events lost money after counting the extra units", "Briefing pack, section 5, note 4")

# ---------------------------------------------------------------- facts: store labor (Tables 3, 4)
fact("wage23", "Average hourly wage incl. benefits", 16.80, "$", "FY2023", "| Average hourly wage incl. benefits | $16.80 | $18.38 |", "Briefing pack, section 6, Table 3, column FY2023")
fact("wage25", "Average hourly wage incl. benefits", 18.38, "$", "FY2025", "| Average hourly wage incl. benefits | $16.80 | $18.38 |", "Briefing pack, section 6, Table 3, column FY2025")
fact("hrs23", "Labor hours per $1,000 of sales", 7.02, "hours", "FY2023", "| Labor hours per $1,000 of sales | 7.02 | 6.60 |", "Briefing pack, section 6, Table 3, column FY2023")
fact("hrs25", "Labor hours per $1,000 of sales", 6.60, "hours", "FY2025", "| Labor hours per $1,000 of sales | 7.02 | 6.60 |", "Briefing pack, section 6, Table 3, column FY2025")
fact("k1000", "Sales unit for labor hours", 1000, "$", "FY2023–25", "| Labor hours per $1,000 of sales | 7.02 | 6.60 |", "Briefing pack, section 6, Table 3, row label")
fact("lp23", "Store labor, % of sales", 0.118, "%", "FY2023", "| Store labor, % of sales | 11.8% | 12.1% |", "Briefing pack, section 6, Table 3, column FY2023")
fact("lp25", "Store labor, % of sales", 0.121, "%", "FY2025", "| Store labor, % of sales | 11.8% | 12.1% |", "Briefing pack, section 6, Table 3, column FY2025")
for k, row, v in (("q1", "| Q1 (fewest labor hours per $ sales) | 3.1% |", 0.031), ("q2", "| Q2 | 2.7% |", 0.027),
                  ("q3", "| Q3 | 2.4% |", 0.024), ("q4", "| Q4 (most) | 2.3% |", 0.023)):
    fact(k, f"Shrink, % of sales, stores in labor-intensity quartile {k.upper()}", v, "%", "FY2025", row, f"Briefing pack, section 6, Table 4, row {k.upper()}")
fact("sh_fresh", "Fresh and produce waste, share of shrink", 0.45, "%", "FY2025", "fresh and produce waste 45%", "Briefing pack, section 6, shrink composition")
fact("sh_theft", "Theft, share of shrink", 0.35, "%", "FY2025", "theft 35%", "Briefing pack, section 6, shrink composition")
fact("sh_admin", "Administrative and receiving errors, share of shrink", 0.20, "%", "FY2025", "administrative and receiving errors 20%", "Briefing pack, section 6, shrink composition")
fact("mgmt_cut", "Management's planned cut in scheduled store labor hours", 0.08, "%", "FY2026",
     "cut scheduled store labor hours by 8% in FY2026", "Briefing pack, section 4")
fact("mgmt_sav", "Management's estimated saving from the 8% hours cut", 14.5, "$M", "per year",
     "they estimate about $14.5M a year of savings", "Briefing pack, section 4")
fact("mw27", "State minimum-wage rise in 2027", 0.04, "%", "2027", "the state minimum wage rises again in 2027 (+4%)", "Briefing pack, section 11")

# ---------------------------------------------------------------- facts: e-commerce (Table 5)
T5 = {"esh": ("| E-commerce share of sales | 3.0% | 5.6% | 8.5% |", (0.03, 0.056, 0.085), "%", "E-commerce share of sales"),
      "ord": ("| Orders, thousands | 453 | 865 | 1,331 |", (453, 865, 1331), "k", "E-commerce orders"),
      "bsk": ("| Average basket | $94 | $95 | $96 |", (94, 95, 96), "$", "Average e-commerce basket"),
      "dsh": ("| Share of orders delivered to the home (rest: click-and-collect) | 45% | 52% | 58% |", (0.45, 0.52, 0.58), "%", "Share of e-commerce orders delivered to the home"),
      "pick": ("| Picking cost per order (all orders) | $7.20 | $7.30 | $7.40 |", (7.20, 7.30, 7.40), "$", "Picking cost per order"),
      "dlv": ("| Third-party delivery cost per delivered order | $12.90 | $13.40 | $13.80 |", (12.90, 13.40, 13.80), "$", "Third-party delivery cost per delivered order"),
      "fee": ("| Average delivery fee collected per delivered order | $3.40 | $3.20 | $3.10 |", (3.40, 3.20, 3.10), "$", "Average delivery fee collected per delivered order")}
for k, (row, vals, unit, lab) in T5.items():
    for y, v in zip((23, 24, 25), vals):
        fact(f"{k}{y}", lab, v, unit, f"FY20{y}", row, f"Briefing pack, section 7, Table 5, column FY20{y}")
fact("thr", "Free-delivery threshold today", 75, "$", "FY2025", "Delivery is free above $75 (a $4.99 fee below)", "Briefing pack, section 7")
fact("fee_low", "Delivery fee below the threshold today", 4.99, "$", "FY2025", "Delivery is free above $75 (a $4.99 fee below)", "Briefing pack, section 7")
fact("n_ecs", "E-commerce customer survey sample", 2300, "respondents", "FY2025", "Survey of 2,300 e-commerce customers (FY2025)", "Briefing pack, section 7")
fact("cann", "Share of online purchases customers would otherwise have bought in a Harlow store", 0.70, "%", "FY2025",
     "70% of what they buy online they say they would otherwise have", "Briefing pack, section 7, survey")
fact("cr", "Contribution per dollar of sales genuinely new to Harlow, before e-commerce fulfillment", 0.20, "%", "FY2025",
     "a dollar of sales that is genuinely new to Harlow adds about 20 cents of contribution", "Briefing pack, section 7, finance estimate")
fact("t_fee_new", "Delivery fee in the fee test", 7.99, "$", "late FY2025", "delivery fee raised to $7.99", "Briefing pack, section 7, fee test")
fact("t_thr", "Free-delivery threshold in the fee test", 100, "$", "late FY2025", "the free-delivery threshold to\n  $100", "Briefing pack, section 7, fee test")
fact("t_dl", "Change in delivered orders, fee test", -0.09, "%", "late FY2025, 10 weeks", "Delivered orders fell 9%", "Briefing pack, section 7, fee test")
fact("t_cc", "Change in click-and-collect orders, fee test", 0.14, "%", "late FY2025, 10 weeks", "click-and-collect orders rose 14%", "Briefing pack, section 7, fee test")
fact("t_sales", "Change in total e-commerce sales, fee test", -0.02, "%", "late FY2025, 10 weeks", "total e-commerce sales fell 2%", "Briefing pack, section 7, fee test")
fact("t_fee", "Average fee collected per delivered order, fee test", 6.40, "$", "late FY2025, 10 weeks",
     "the\n  average fee collected per delivered order rose to $6.40", "Briefing pack, section 7, fee test")
fact("team_cm", "E-commerce contribution margin reported by the e-commerce team", 0.061, "%", "FY2025",
     "a contribution margin of 6.1% of e-commerce sales in FY2025", "Briefing pack, section 10")
fact("deep_comp", "Comparable-sales growth, stores with the deepest promotions", 0.018, "%", "FY2025",
     "Stores with the deepest promotions in FY2025 grew comparable sales 1.8%", "Briefing pack, section 10")
fact("rest_comp", "Comparable-sales growth, other stores", 0.002, "%", "FY2025", "against 0.2% for the\n  rest", "Briefing pack, section 10")
fact("pl_rise", "Rate rise proposed by the third-party delivery provider", 0.03, "%", "2026 renewal", "the provider proposed a 3% rise", "Briefing pack, section 11")

# ---------------------------------------------------------------- facts: stores, customers, constraints
fact("n_st", "Harlow stores", 58, "stores", "FY2025", "| Stores with negative four-wall EBITDA | 9 of 58 |", "Briefing pack, section 8, Table 6")
fact("weak_n", "Stores with negative four-wall EBITDA", 9, "stores", "FY2025", "| Stores with negative four-wall EBITDA | 9 of 58 |", "Briefing pack, section 8, Table 6")
fact("weak_s", "Combined sales of the nine weakest stores", 118.0, "$M", "FY2025", "| Their combined sales | $118.0M |", "Briefing pack, section 8, Table 6")
fact("weak_e", "Combined four-wall EBITDA of the nine weakest stores", -3.1, "$M", "FY2025", "| Their combined four-wall EBITDA | −$3.1M |", "Briefing pack, section 8, Table 6")
fact("lease6", "Weak stores with leases expiring by end of 2027", 6, "stores", "FY2025", "| Leases expiring by end of 2027 | 6 of the 9 |", "Briefing pack, section 8, Table 6 (FY2025)")
fact("exit_c", "Estimated lease-exit cost for the other three weak stores", 7.5, "$M", "one-time", "| Estimated lease-exit cost for the other 3 | $7.5M (one-time) |", "Briefing pack, section 8, Table 6")
fact("transfer", "Share of a closed store's sales expected to move to a nearby Harlow store", 0.25, "%", "past closures",
     "| Share of their sales expected to move to a nearby Harlow store if closed (past closures) | 25% |", "Briefing pack, section 8, Table 6")
fact("recv_cm", "Contribution on sales moved to a receiving store", 0.12, "%", "past closures", "| Contribution on sales moved to a receiving store | 12% |", "Briefing pack, section 8, Table 6")
fact("vm_n", "ValuMart stores opened in Harlow trade areas since 2023", 11, "stores", "2023–FY2025", "has opened 11 stores in Harlow trade areas since 2023", "Briefing pack, section 9")
fact("vm_comp", "Comparable-sales growth, Harlow stores within three miles of a new ValuMart", -0.042, "%", "FY2025",
     "comparable sales of −4.2% in FY2025", "Briefing pack, section 9")
fact("oth_comp", "Comparable-sales growth, other Harlow stores", 0.011, "%", "FY2025", "against +1.1% for other Harlow stores", "Briefing pack, section 9")
fact("perc25", "Shoppers who say Harlow is more expensive than other options", 0.41, "%", "FY2025 survey, n = 3,100",
     "41% say Harlow is \"more expensive than other options\" (FY2023: 33%)", "Briefing pack, section 9, customer survey, FY2025 survey, n = 3,100")
fact("perc23", "Shoppers who say Harlow is more expensive than other options", 0.33, "%", "FY2023",
     "41% say Harlow is \"more expensive than other options\" (FY2023: 33%)", "Briefing pack, section 9")
fact("fresh", "Shoppers naming fresh produce as a top reason to shop Harlow", 0.58, "%", "FY2025 survey, n = 3,100",
     "top reasons\n  to shop Harlow are fresh produce (58%) and convenience (44%)", "Briefing pack, section 9")
fact("conv", "Shoppers naming convenience as a top reason to shop Harlow", 0.44, "%", "FY2025 survey, n = 3,100",
     "fresh produce (58%) and convenience (44%)", "Briefing pack, section 9")
fact("n_cs", "Customer survey sample", 3100, "respondents", "FY2025", "Customer survey (n = 3,100)", "Briefing pack, section 9")
fact("tgt", "Operating-margin target", 0.03, "%", "FY2028", "operating margin back to at least 3.0% by FY2028", "Briefing pack, section 3")
fact("capcap", "Limit on one-time cost or capital for the plan", 25, "$M", "FY2026–FY2028", "at most $25M of one-time cost or capital", "Briefing pack, section 3")
fact("cov", "Lender covenant: minimum operating income", 20, "$M", "FY2026", "a covenant requires operating income of at least $20M in FY2026", "Briefing pack, section 3")

# ---------------------------------------------------------------- planning assumptions chosen on the user's behalf
assume("qshare", "Share of chain sales in each labor-intensity quartile of stores", 0.25, "%", "FY2025",
       "each quartile carries about a quarter of sales; the four quartiles then average 2.6%, the chain's FY2025 shrink")
assume("yrs", "Years from FY2025 to FY2028", 3, "years", "FY2026–FY2028", "FY2026, FY2027 and FY2028")
assume("half", "Share of the promotion reset landing in FY2026", 0.5, "%", "FY2026",
       "loss-making events go first, so half the move back to 24% of sales lands in the first year")
assume("one", "One dollar off the delivery rate per delivered order", 1, "$", "renewal", "unit for the sensitivity")

# ---------------------------------------------------------------- derived: section 1
der("sg", "Sales growth, FY2023 to FY2025", "%", "FY2023–25", "s25 / s23 - 1", "1,503.0 ÷ 1,420.0 − 1")
der("oi_chg", "Change in operating income, FY2023 to FY2025", "%", "FY2023–25", "oi25 / oi23 - 1", "15.3 ÷ 47.9 − 1")
der("oi_fall25", "Fall in operating income in FY2025", "$M", "FY2025", "oi24 - oi25", "33.4 − 15.3")
der("sales_add", "Sales added, FY2023 to FY2025", "$M", "FY2023–25", "s25 - s23", "1,503.0 − 1,420.0")
der("wf_g", "Operating income from sales growth at the FY2023 margin", "$M", "FY2023–25", "sales_add * oi23 / s23", "83.0 × 47.9 ÷ 1,420.0")
der("wf_gm", "Change in gross margin rate, applied to FY2025 sales", "$M", "FY2023–25", "(gp25 / s25 - gp23 / s23) * s25", "(376.1 ÷ 1,503.0 − 369.8 ÷ 1,420.0) × 1,503.0")
der("wf_lab", "Change in store labor rate, applied to FY2025 sales", "$M", "FY2023–25", "(lab23 / s23 - lab25 / s25) * s25", "(167.6 ÷ 1,420.0 − 181.9 ÷ 1,503.0) × 1,503.0")
der("wf_occ", "Change in occupancy and energy rate, applied to FY2025 sales", "$M", "FY2023–25", "(occ23 / s23 - occ25 / s25) * s25", "(82.4 ÷ 1,420.0 − 90.2 ÷ 1,503.0) × 1,503.0")
der("wf_ef", "Change in e-commerce fulfillment rate, applied to FY2025 sales", "$M", "FY2023–25", "(ef23 / s23 - ef25 / s25) * s25", "(5.2 ÷ 1,420.0 − 18.1 ÷ 1,503.0) × 1,503.0")
der("short", "Operating-income shortfall from the four cost and margin lines", "$M", "FY2023–25", "0 - (wf_gm + wf_lab + wf_occ + wf_ef)", "sum of the four rate effects")
der("sh_gmef", "Share of the shortfall from gross margin and e-commerce", "%", "FY2023–25", "(wf_gm + wf_ef) / (wf_gm + wf_lab + wf_occ + wf_ef)", "(15.3 + 12.6) ÷ 35.4")
der("sh_lab", "Share of the shortfall from store labor", "%", "FY2023–25", "wf_lab / (wf_gm + wf_lab + wf_occ + wf_ef)", "4.5 ÷ 35.4")
for k in ("gp", "lab", "occ", "ef", "sga", "oi"):
    for y in (23, 24, 25):
        der(f"{k}{y}r", f"{NAMES[k]}, % of sales", "%", f"FY20{y}", f"{k}{y} / s{y}", f"{NAMES[k]} ÷ sales, FY20{y}")
    der(f"{k}_dpp", f"Change in {NAMES[k].lower()}, % of sales", "pp", "FY2023–25", f"({k}25r - {k}23r) * 100", "FY2025 share − FY2023 share")
der("om_drop", "Fall in operating margin, FY2023 to FY2025", "pp", "FY2023–25", "(om23 - om25) * 100", "3.37% − 1.02%")
der("gap_cov", "Operating income needed in FY2026 to meet the covenant", "$M", "FY2026", "cov - oi25", "20 − 15.3")
der("tgt_oi25", "Operating income at a 3.0% margin on FY2025 sales", "$M", "FY2025 base", "tgt * s25", "3.0% × 1,503.0")
der("gap_tgt", "Operating income needed to reach 3.0% at FY2025 sales", "$M", "FY2025 base", "tgt * s25 - oi25", "3.0% × 1,503.0 − 15.3")
der("mgmt_m", "Operating margin if management's full $14.5M saving holds", "%", "FY2025 base", "(oi25 + mgmt_sav) / s25", "(15.3 + 14.5) ÷ 1,503.0")
der("mgmt_half", "Management's saving as a share of the gap to 3.0%", "%", "FY2025 base", "mgmt_sav / gap_tgt", "14.5 ÷ 29.8")

# ---------------------------------------------------------------- derived: section 2
der("d_promo", "Gross-margin effect of the shift to promotions", "pp", "FY2023–25", "(promo23 - promo25) * promo_gap", "(24.0% − 29.0%) × 14 pp")
der("d_pl", "Gross-margin effect of the shift to private label", "pp", "FY2023–25", "(plsh25 - plsh23) * pl_gap", "(18.5% − 17.0%) × 12 pp")
der("d_shr", "Gross-margin effect of higher shrink", "pp", "FY2023–25", "(shr23 - shr25) * 100", "2.1% − 2.6%")
der("d_gm3", "Gross-margin effect of the three drivers together", "pp", "FY2023–25", "d_promo + d_pl + d_shr", "−0.70 + 0.18 − 0.50")
der("promo_cost", "Annual cost of the shift to promotions at FY2025 sales", "$M", "FY2025", "0 - d_promo / 100 * s25", "0.70% × 1,503.0")
der("pl_off", "Private-label gain as a share of the promotional loss", "%", "FY2023–25", "d_pl / (0 - d_promo)", "0.18 ÷ 0.70")
der("promo_shift", "Rise in the promotional share of sales", "pp", "FY2023–25", "(promo25 - promo23) * 100", "29.0% − 24.0%")
der("vf_chg", "Change in vendor funding of markdowns", "pp", "FY2023–25", "(vf25 - vf23) * 100", "46% − 55%")
der("hf23", "Share of promotional markdowns Harlow pays itself", "%", "FY2023", "1 - vf23", "100% − 55%")
der("hf25", "Share of promotional markdowns Harlow pays itself", "%", "FY2025", "1 - vf25", "100% − 46%")
der("bk", "Extra sales needed for the promotional shift to pay for itself", "%", "FY2023–25", "promo_shift * promo_gap / 100 / cr / 100",
    "5 pp × 14 pp ÷ 20 cents", estimate=True, assumptions=[
        "Each new dollar of sales from promotions earns the finance estimate of 20 cents of contribution",
        "Promoted sales earn less than that, so the true break-even is higher",
        "The margin given up is the FY2023–25 shift of 5 percentage points of sales into promotions"])
der("comp_gap", "Comparable-sales gap, deepest-promotion stores against the rest", "pp", "FY2025", "(deep_comp - rest_comp) * 100", "1.8% − 0.2%")
der("bk_mult", "Break-even sales gain as a multiple of the category team's comparable-sales gap", "x", "FY2025", "bk * 100 / comp_gap",
    "3.5% ÷ 1.6 pp", estimate=True, assumptions=["Compares the break-even with a one-year comparable-sales gap that may not be caused by promotions"])
der("pl_pace", "Private-label share gained a year", "pp", "FY2023–25", "(plsh25 - plsh23) * 100 / 2", "(18.5% − 17.0%) ÷ 2")
der("pl_add", "Private-label share added over FY2026–28 at the FY2023–25 pace", "pp", "FY2026–28", "pl_pace * yrs",
    "0.75 pp × 3 years", estimate=True, assumptions=["Private label keeps gaining share at its FY2023–25 pace of 0.75 percentage points a year"])
der("pl28", "Private-label share of sales, FY2028, at the FY2023–25 pace", "%", "FY2028", "plsh25 + pl_add / 100",
    "18.5% + 2.25 pp", estimate=True, assumptions=["Private label keeps gaining share at its FY2023–25 pace of 0.75 percentage points a year"])
der("pl_pp", "Gross-margin gain from private label by FY2028", "pp", "FY2028", "pl_add * pl_gap / 100",
    "2.25 pp × 12 pp", estimate=True, assumptions=["Moved sales come from national brands in the same aisles", "The 12 percentage-point margin premium holds"])
der("stay", "Share of a closed store's sales that does not move to another Harlow store", "%", "past closures", "1 - transfer", "100% − 25%")
der("es25", "E-commerce sales", "$M", "FY2025", "esh25 * s25", "8.5% × 1,503.0")
der("lost_st", "Sales lost to Harlow if the nine stores close", "$M", "FY2028", "weak_s * stay", "118.0 × 75%")
der("B", "Chain sales after the nine store exits and the delivery fee change", "$M", "FY2028 run rate, FY2025 prices",
    "s25 - lost_st + t_sales * es25", "1,503.0 − 88.5 − 2% × 127.8", estimate=True, assumptions=[
        "Sales held at FY2025 levels apart from the store exits and the fee change: no growth or inflation",
        "25% of the nine stores' sales moves to nearby Harlow stores, as in past closures",
        "E-commerce sales fall 2%, as in the fee test"])
der("promo_pp", "Gross-margin gain from bringing promotions back to 24% of sales", "pp", "FY2028", "promo_shift * promo_gap / 100",
    "5 pp × 14 pp", estimate=True, assumptions=["Sales that leave promotion sell at regular price", "The 14 percentage-point promotional margin gap holds"])
der("g_promo", "Operating-income gain from promotions back to 24% of sales", "$M", "FY2028 run rate", "promo_pp / 100 * B",
    "0.70% × $1,412M", estimate=True, assumptions=[
        "Promotions return to FY2023's 24% of sales by cutting events that lose money, starting outside ValuMart areas",
        "Sales that leave promotion sell at regular price; any lost volume makes the gain smaller",
        "Sized on the sales base after store exits"])
der("q1gap", "Shrink gap, Q1 stores against Q3", "pp", "FY2025", "(q1 - q3) * 100", "3.1% − 2.4%")
der("q2gap", "Shrink gap, Q2 stores against Q3", "pp", "FY2025", "(q2 - q3) * 100", "2.7% − 2.4%")
der("q34", "Shrink gap, Q3 stores against Q4", "pp", "FY2025", "(q3 - q4) * 100", "2.4% − 2.3%")
der("q_gap", "Combined excess shrink of Q1 and Q2 stores over Q3", "pp", "FY2025", "q1gap + q2gap", "0.7 + 0.3")
der("q_ratio", "Shrink of Q1 stores as a multiple of Q4", "x", "FY2025", "q1 / q4", "3.1% ÷ 2.3%")
der("sh_ctrl", "Share of shrink from fresh waste and receiving errors", "%", "FY2025", "sh_fresh + sh_admin", "45% + 20%")
der("sh_pp", "Chain shrink reduction if Q1 and Q2 stores reach Q3's rate", "pp", "FY2028", "q_gap * qshare",
    "1.0 pp × 25%", estimate=True, assumptions=["Each quartile of stores carries about a quarter of sales"])
der("g_sh", "Operating-income gain from lower shrink", "$M", "FY2028 run rate", "sh_pp / 100 * B", "0.25% × $1,412M",
    estimate=True, assumptions=[
        "Q1 and Q2 stores reach Q3's 2.4% shrink by protecting receiving checks and produce rotation",
        "The hours come from Q4 stores, where extra hours cut shrink by only 0.1 percentage points, so total hours do not rise",
        "Each quartile carries about a quarter of sales; theft is unchanged"])
der("shr_new", "Chain shrink after the shrink actions", "%", "FY2028", "(q3 + q3 + q3 + q4) / 4",
    "average of 2.4%, 2.4%, 2.4% and 2.3%", estimate=True, assumptions=["Each quartile carries about a quarter of sales"])
der("g_pl", "Operating-income gain from private label", "$M", "FY2028 run rate", "(pl28 - plsh25) * pl_gap / 100 * B", "(20.75% − 18.5%) × 12 pp × $1,412M",
    estimate=True, assumptions=["Private label gains 0.75 percentage points of share a year to FY2028", "The 12 percentage-point margin premium holds",
                                "Sized on the sales base after store exits"])
der("gm_pp", "Gross-margin gain from the three gross-margin actions", "pp", "FY2028", "promo_pp + pl_pp + sh_pp", "0.70 + 0.27 + 0.25",
    estimate=True, assumptions=["See the three actions"])
der("gm_gain", "Operating-income gain from the three gross-margin actions", "$M", "FY2028 run rate", "(promo_pp + pl_pp + sh_pp) / 100 * B",
    "1.22% × $1,412M", estimate=True, assumptions=["Promotions back to 24% of sales; private label to about 21%; Q1 and Q2 stores at Q3's shrink",
                                                    "Sized on the sales base after store exits"])

# ---------------------------------------------------------------- derived: section 3
der("wage_g", "Rise in average hourly wage incl. benefits", "%", "FY2023–25", "wage25 / wage23 - 1", "18.38 ÷ 16.80 − 1")
der("hrs_g", "Change in labor hours per $1,000 of sales", "%", "FY2023–25", "hrs25 / hrs23 - 1", "6.60 ÷ 7.02 − 1")
der("lab_pp", "Change in store labor as a share of sales", "pp", "FY2023–25", "(lp25 - lp23) * 100", "12.1% − 11.8%")
der("shr_chg", "Rise in shrink, FY2023 to FY2025", "pp", "FY2023–25", "(shr25 - shr23) * 100", "2.6% − 2.1%")
der("el", "Rise in shrink for each 1% fewer labor hours per $1,000 of sales", "pp", "FY2023–25", "shr_chg / (0 - hrs_g * 100)",
    "0.5 pp ÷ 6.0%", estimate=True, assumptions=["All of the FY2023–25 rise in shrink is put down to thinner staffing, an upper bound"])
der("sh_add", "Extra shrink from an 8% hours cut", "pp", "FY2026", "el * mgmt_cut * 100", "0.084 pp × 8",
    estimate=True, assumptions=["All of the FY2023–25 rise in shrink is put down to thinner staffing, an upper bound"])
der("giveback", "Extra shrink cost of an 8% hours cut", "$M", "per year", "el * mgmt_cut * 100 / 100 * s25", "0.67% × 1,503.0",
    estimate=True, assumptions=["Shrink rises with fewer hours as it did in FY2023–25, when hours per $1,000 fell 6.0% and shrink rose 0.5 percentage points",
                                "All of that rise is put down to thinner staffing, so this is an upper bound",
                                "Lost sales from checkout waits and stock-outs are not counted"])
der("net_cut", "Net saving from the 8% hours cut after extra shrink", "$M", "per year", "mgmt_sav - giveback", "14.5 − 10.0",
    estimate=True, assumptions=["Shrink rises with fewer hours as in FY2023–25 (upper bound)", "Lost sales are not counted"])
der("mgmt_low", "Operating margin under management's plan if shrink rises as in FY2023–25", "%", "FY2025 base", "(oi25 + net_cut) / s25",
    "(15.3 + 4.5) ÷ 1,503.0", estimate=True, assumptions=["Shrink rises with fewer hours as in FY2023–25 (upper bound)"])
der("mgmt26", "FY2026 operating income under management's plan, full saving", "$M", "FY2026", "oi25 + mgmt_sav", "15.3 + 14.5")
der("mgmt26_low", "FY2026 operating income under management's plan, after extra shrink", "$M", "FY2026", "oi25 + net_cut", "15.3 + 4.5",
    estimate=True, assumptions=["Shrink rises with fewer hours as in FY2023–25 (upper bound)"])
der("wage_f", "Wage factor after the 2027 minimum-wage rise", "x", "2027", "1 + mw27", "1 + 4%")
der("hrs_need", "Labor hours per $1,000 of sales that hold labor at 12.1% of sales after the 2027 wage rise", "hours", "FY2027",
    "hrs25 / wage_f", "6.60 ÷ 1.04", estimate=True, assumptions=["The 4% minimum-wage rise lifts the whole average wage, an upper bound",
                                                               "Sales per store and the sales mix stay at FY2025 levels"])
der("hrs_need_g", "Cut in hours per $1,000 of sales needed to absorb the 2027 wage rise", "%", "FY2027", "hrs_need / hrs25 - 1",
    "6.35 ÷ 6.60 − 1", estimate=True, assumptions=["The 4% minimum-wage rise lifts the whole average wage, an upper bound"])
der("weak_sh", "Nine weakest stores' share of chain sales", "%", "FY2025", "weak_s / s25", "118.0 ÷ 1,503.0")
der("e_loss9", "Four-wall EBITDA loss removed by exiting the nine stores", "$M", "per year", "0 - weak_e", "−(−3.1)")
der("st_tr", "Contribution on sales moved to receiving stores", "$M", "per year", "weak_s * transfer * recv_cm", "118.0 × 25% × 12%",
    estimate=True, assumptions=["25% of the nine stores' sales moves to nearby Harlow stores, as in past closures", "Moved sales earn 12% contribution"])
der("g_st", "Operating-income gain from exiting the nine stores", "$M", "FY2028 run rate", "weak_s * transfer * recv_cm + e_loss9",
    "118.0 × 25% × 12% + 3.1", estimate=True, assumptions=["Four-wall EBITDA stands in for the operating-income effect; depreciation saved is not counted",
                                                         "25% of sales moves to nearby Harlow stores, as in past closures"])
der("g_st6", "Gain from the six stores with leases ending by 2027", "$M", "FY2028 run rate", "g_st * lease6 / weak_n", "6.6 × 6 ÷ 9",
    estimate=True, assumptions=["The gain splits evenly across the nine stores"])
der("g_st3", "Gain from the three stores with leases beyond 2027", "$M", "FY2028 run rate", "g_st * (weak_n - lease6) / weak_n", "6.6 × 3 ÷ 9",
    estimate=True, assumptions=["The gain splits evenly across the nine stores"])
der("payback3", "Payback on exiting the three stores with leases beyond 2027", "years", "FY2027–", "exit_c / g_st3", "7.5 ÷ 2.2",
    estimate=True, assumptions=["The gain splits evenly across the nine stores"])
der("st6_sh", "Share of the store-exit gain needing no board vote", "%", "FY2028", "lease6 / weak_n", "6 ÷ 9")

# ---------------------------------------------------------------- derived: section 4
der("dl25", "Delivered orders", "k", "FY2025", "ord25 * dsh25", "1,331 × 58%")
der("cc25", "Click-and-collect orders", "k", "FY2025", "ord25 - dl25", "1,331 − 772")
der("pick_t", "Picking cost", "$M", "FY2025", "ord25 * pick25 / 1000", "1,331k × $7.40")
der("dlv_t", "Third-party delivery cost", "$M", "FY2025", "dl25 * dlv25 / 1000", "772k × $13.80")
der("fee_t", "Delivery fees collected", "$M", "FY2025", "dl25 * fee25 / 1000", "772k × $3.10")
der("ef_m", "E-commerce fulfillment rebuilt from order data", "$M", "FY2025", "pick_t + dlv_t - fee_t", "9.85 + 10.65 − 2.39")
der("dnet", "Third-party delivery cost net of fees", "$M", "FY2025", "dlv_t - fee_t", "10.65 − 2.39")
der("inc", "Share of online spend new to Harlow", "%", "FY2025", "1 - cann", "100% − 70%")
der("e_ctb", "Contribution from e-commerce sales new to Harlow", "$M", "FY2025", "es25 * inc * cr", "127.8 × 30% × 20%",
    estimate=True, assumptions=["30% of online spend is new to Harlow, from customers' survey answers", "A new dollar adds 20 cents of contribution (finance)"])
der("e_loss", "E-commerce contribution after fulfillment", "$M", "FY2025", "es25 * inc * cr - ef25", "7.7 − 18.1",
    estimate=True, assumptions=["30% of online spend is new to Harlow (survey of 2,300 online customers)",
                                "A new dollar adds 20 cents of contribution before fulfillment (finance)",
                                "Store costs saved when an existing customer shops online are not counted"])
der("e_cover", "Share of fulfillment cost covered by contribution on new sales", "%", "FY2025", "e_ctb / ef25", "7.7 ÷ 18.1",
    estimate=True, assumptions=["30% of online spend is new to Harlow", "20 cents of contribution per new dollar"])
der("e_rate", "E-commerce loss as a share of e-commerce sales", "%", "FY2025", "e_loss / es25", "−10.4 ÷ 127.8",
    estimate=True, assumptions=["30% of online spend is new to Harlow", "20 cents of contribution per new dollar"])
der("team_usd", "E-commerce profit as the team reports it", "$M", "FY2025", "team_cm * es25", "6.1% × 127.8")
der("ef_mult", "E-commerce fulfillment cost, FY2025 as a multiple of FY2023", "x", "FY2023–25", "ef25 / ef23", "18.1 ÷ 5.2")
der("ef_ps", "Fulfillment cost per dollar of e-commerce sales", "%", "FY2025", "ef25 / es25", "18.1 ÷ 127.8")
der("ord_mult", "E-commerce orders, FY2025 as a multiple of FY2023", "x", "FY2023–25", "ord25 / ord23", "1,331 ÷ 453")
der("gap_d23", "Third-party cost less fee, per delivered order", "$", "FY2023", "dlv23 - fee23", "12.90 − 3.40")
der("gap_d25", "Third-party cost less fee, per delivered order", "$", "FY2025", "dlv25 - fee25", "13.80 − 3.10")
der("c_do", "Contribution per order from sales new to Harlow", "$", "FY2025", "bsk25 * inc * cr", "$96 × 30% × 20%",
    estimate=True, assumptions=["Delivered and collected orders have the same $96 basket and the same 30% of new spend"])
der("pick_n", "Picking cost per order, as a deduction", "$", "FY2025", "0 - pick25", "−$7.40")
der("dlv_n", "Third-party delivery cost per delivered order, as a deduction", "$", "FY2025", "0 - dlv25", "−$13.80")
der("cost_do", "Picking plus delivery less the fee, per delivered order", "$", "FY2025", "pick25 + dlv25 - fee25", "7.40 + 13.80 − 3.10")
der("loss_do", "Result per delivered order", "$", "FY2025", "c_do - cost_do", "5.76 − 18.10",
    estimate=True, assumptions=["Delivered and collected orders have the same $96 basket and the same 30% of new spend"])
der("cc_loss", "Result per click-and-collect order", "$", "FY2025", "c_do - pick25", "5.76 − 7.40",
    estimate=True, assumptions=["Delivered and collected orders have the same $96 basket and the same 30% of new spend"])
der("lossx", "Loss per delivered order as a multiple of the loss per click-and-collect order", "x", "FY2025", "loss_do / cc_loss", "12.34 ÷ 1.64")
der("dl_lsh", "Home delivery's share of the e-commerce loss", "%", "FY2025", "dl25 * loss_do / 1000 / e_loss", "772k × $12.34 ÷ $10.4M",
    estimate=True, assumptions=["Same basket and new-spend share for both order types"])
der("fee_mult", "Fee per delivered order in the test as a multiple of FY2025", "x", "late FY2025", "t_fee / fee25", "6.40 ÷ 3.10")
der("dl_t", "Delivered orders with the tested fee, chain-wide", "k", "FY2025 volumes", "dl25 * (1 + t_dl)", "772k × (1 − 9%)",
    estimate=True, assumptions=["The test's response holds across the chain"])
der("cc_t", "Click-and-collect orders with the tested fee, chain-wide", "k", "FY2025 volumes", "cc25 * (1 + t_cc)", "559k × (1 + 14%)",
    estimate=True, assumptions=["The test's response holds across the chain"])
der("ef_t", "E-commerce fulfillment cost with the tested fee, chain-wide", "$M", "FY2025 volumes",
    "(dl25 * (1 + t_dl) + cc25 * (1 + t_cc)) * pick25 / 1000 + dl25 * (1 + t_dl) * (dlv25 - t_fee) / 1000",
    "(703k + 637k) × $7.40 + 703k × ($13.80 − $6.40)", estimate=True, assumptions=[
        "Delivered orders fall 9%, click-and-collect orders rise 14% and the fee per delivery averages $6.40, as in the test",
        "Picking and delivery cost per order stay at FY2025 levels"])
der("lost_c", "Contribution lost on lower e-commerce sales", "$M", "FY2025 volumes", "0 - t_sales * es25 * inc * cr", "2% × 127.8 × 30% × 20%",
    estimate=True, assumptions=["Lost online sales are new to Harlow in the same 30% share as all online spend"])
der("g_fee", "Operating-income gain from the tested delivery fee, chain-wide", "$M", "FY2028 run rate",
    "ef25 - ef_t - lost_c", "18.1 − 15.1 − 0.15", estimate=True, assumptions=[
        "The 4-store, 10-week fee test holds chain-wide: delivered orders −9%, click-and-collect +14%, e-commerce sales −2%",
        "The fee per delivered order averages $6.40, as in the test",
        "Picking and delivery costs per order stay at FY2025 levels"])
der("e_after", "E-commerce contribution after fulfillment, with the tested fee", "$M", "FY2025 volumes", "e_loss + g_fee", "−10.4 + 2.8",
    estimate=True, assumptions=["The fee test holds chain-wide"])
der("per1", "Annual gain from each $1 off the delivery rate", "$M", "per year", "dl25 * (1 + t_dl) * one / 1000", "703k × $1",
    estimate=True, assumptions=["Delivered orders at the level the fee test implies"])
der("rise_c", "Annual cost of the proposed 3% delivery-rate rise", "$M", "per year", "dl25 * (1 + t_dl) * dlv25 * pl_rise / 1000",
    "703k × $13.80 × 3%", estimate=True, assumptions=["Delivered orders at the level the fee test implies"])

# ---------------------------------------------------------------- derived: section 5
der("oi28", "Operating income, FY2028 run rate, with the plan", "$M", "FY2028 run rate",
    "oi25 + (promo_pp + pl_pp + sh_pp) / 100 * B + g_fee + g_st", "15.3 + 17.2 + 2.8 + 6.6", estimate=True, assumptions=[
        "FY2025 prices, volumes and cost rates except for the plan's actions",
        "Scheduling absorbs the 2027 minimum-wage rise, holding store labor at 12.1% of sales",
        "No sales growth, delivery-rate cut or depreciation saving counted"])
der("m28", "Operating margin, FY2028 run rate, with the plan", "%", "FY2028 run rate", "oi28 / B", "42.0 ÷ 1,412",
    estimate=True, assumptions=["See operating income, FY2028 run rate"])
der("tgt28", "Operating income at a 3.0% margin on the post-exit sales base", "$M", "FY2028 run rate", "tgt * B", "3.0% × 1,412",
    estimate=True, assumptions=["Sales base after store exits and the fee change"])
der("short28", "Plan operating income against 3.0% of sales", "$M", "FY2028 run rate", "oi28 - tgt * B", "42.0 − 42.4",
    estimate=True, assumptions=["See operating income, FY2028 run rate"])
der("cut_need", "Delivery-rate cut per delivered order that closes the gap to 3.0%", "$", "renewal", "(tgt * B - oi28) / (dl25 * (1 + t_dl) / 1000)",
    "$0.35M ÷ 703k orders", estimate=True, assumptions=["Delivered orders at the level the fee test implies"])
der("promo26", "Promotional share of sales at the end of FY2026", "%", "FY2026", "promo25 - (promo25 - promo23) * half", "29% − 5 pp × 50%",
    estimate=True, assumptions=["Half the move back to 24% lands in FY2026"])
der("B26", "Sales base in FY2026, before store exits", "$M", "FY2026", "s25 + t_sales * es25", "1,503.0 − 2% × 127.8",
    estimate=True, assumptions=["No store exits in FY2026; e-commerce sales fall 2% with the fee change"])
der("g_promo26", "FY2026 gain from the first half of the promotion reset", "$M", "FY2026", "promo_pp * half / 100 * B26", "0.70% × 50% × 1,500",
    estimate=True, assumptions=["Half the move back to 24% lands in FY2026, loss-making events first", "Sales that leave promotion sell at regular price"])
der("oi26", "FY2026 operating income with the promotion reset and the tested fee", "$M", "FY2026", "oi25 + promo_pp * half / 100 * B26 + g_fee",
    "15.3 + 5.3 + 2.8", estimate=True, assumptions=["Every other line holds at its FY2025 share of sales", "The fee applies for the whole year"])
der("head26", "FY2026 headroom over the covenant", "$M", "FY2026", "oi25 + promo_pp * half / 100 * B26 + g_fee - cov", "23.4 − 20",
    estimate=True, assumptions=["Every other line holds at its FY2025 share of sales"])
der("g_ph", "Promotion gain if only half is delivered", "$M", "FY2028", "promo_pp / 100 * B * half", "9.9 × 50%",
    estimate=True, assumptions=["Half the promotion reset holds"])
der("m_ph", "FY2028 margin if the promotion reset delivers half", "%", "FY2028", "(oi28 - promo_pp / 100 * B * half) / B", "(42.0 − 4.9) ÷ 1,412",
    estimate=True, assumptions=["Half the promotion reset holds"])
der("m_n3", "FY2028 margin if the three stores with longer leases stay open", "%", "FY2028",
    "(oi28 - g_st * (weak_n - lease6) / weak_n) / (B + lost_st * (weak_n - lease6) / weak_n)", "(42.0 − 2.2) ÷ (1,412 + 29.5)",
    estimate=True, assumptions=["The three stores keep their share of the nine stores' loss and sales"])
der("wage_c", "Cost of the 2027 wage rise if scheduling does not absorb it", "$M", "FY2028", "mw27 * lp25 * B", "4% × 12.1% × 1,412",
    estimate=True, assumptions=["The 4% rise lifts the whole average wage, an upper bound"])
der("m_w", "FY2028 margin if the 2027 wage rise is not absorbed", "%", "FY2028", "(oi28 - mw27 * lp25 * B) / B", "(42.0 − 6.8) ÷ 1,412",
    estimate=True, assumptions=["The 4% rise lifts the whole average wage, an upper bound"])
der("m_d1", "FY2028 margin with $1 off the delivery rate", "%", "FY2028", "(oi28 + dl25 * (1 + t_dl) * one / 1000) / B", "(42.0 + 0.7) ÷ 1,412",
    estimate=True, assumptions=["Delivered orders at the level the fee test implies"])

# ---------------------------------------------------------------- helpers for text built from values
def m(x, d=1): return f"${x:,.{d}f}M"
def pc(x, d=1): return f"{x*100:.{d}f}%"

# ---------------------------------------------------------------- slides
S = []
def add(**kw): S.append(kw); return kw
def nav(i, sec): add(id=i, role="agenda_tracker", section_id=sec, status="filled", archetype="agenda-tracker", message_type="navigation")
MONEY = '"$"#,##0.0"M"'
PP = '+0.00" pp";-0.00" pp"'

add(id="c", role="cover", status="filled")
add(id="q", role="problem_statement", status="filled")
add(id="es", role="exec_summary", status="filled", archetype="exec-summary", message_type="navigation")

# ---------- section 1
nav("d1", "1")
add(id="p11", role="content", section_id="1", status="filled", message_type="time-series", archetype="multi-chart-panel",
    rationale="Two sides of one point, two clauses -> two panels",
    lead_message={"text": "Sales grew 6% in two years, but operating income fell by more than two-thirds to $15.3M",
                  "numbers": [{"text": "6%", "data_ref": "sg"}, {"text": "$15.3M", "data_ref": "oi25"}], "clauses": 2},
    layout={"variant": "split_2"},
    body={"kind": "panels", "panels": [
        {"header": "Sales rose in both years, adding $83M by FY2025", "unit_line": "**Sales**, $ millions, FY2023–FY2025",
         "delta": P("sg"), "body": {"kind": "chart", "chart_type": "column", "categories": ["FY2023", "FY2024", "FY2025"],
                                    "series": [{"name": "Sales", "points": [P("s23"), P("s24"), P("s25")]}], "sort": "none", "value_format": MONEY}},
        {"header": "Operating income fell in both years, and faster in FY2025", "unit_line": "**Operating income**, $ millions, FY2023–FY2025",
         "delta": P("oi_chg"), "body": {"kind": "chart", "chart_type": "column", "categories": ["FY2023", "FY2024", "FY2025"],
                                        "series": [{"name": "Operating income", "points": [P("oi23"), P("oi24"), P("oi25")]}], "sort": "none", "value_format": MONEY}}]},
    footnotes=["Fiscal years end in January. Operating margin fell from 3.37% to 1.02% of sales over the period",
               f"Operating income fell {m(V['oi_fall25'])} in FY2025 alone"])

add(id="p12", role="content", section_id="1", status="filled", message_type="component", archetype="waterfall-bridge",
    rationale="What adds up to the fall -> waterfall",
    lead_message={"text": "Gross margin and e-commerce, not store labor, account for nearly four-fifths of the lost operating income",
                  "highlights": ["Gross margin rate", "E-commerce fulfillment"]},
    unit_line="**Operating income bridge**, $ millions, FY2023 to FY2025; each line's change in % of sales, applied to FY2025 sales",
    layout={"variant": "takeaway_sidebar", "sidebar": {
        "kind": "big_number", "header": "Wages are a small part of the story", "big_number": P("sh_gmef"),
        "caption": f"of the {m(V['short'])} shortfall comes from gross margin and e-commerce",
        "bullets": [f"**Gross margin rate:** down from {pc(V['gp23r'])} to {pc(V['gp25r'])} of sales, through promotions and shrink (section 2)",
                    f"**E-commerce:** fulfillment net of fees rose from {pc(V['ef23r'])} to {pc(V['ef25r'])} of sales (section 4)",
                    f"**Store labor:** {pc(V['sh_lab'], 0)} of the shortfall, yet it is the only line the draft plan targets",
                    f"**Other SG&A:** unchanged at {pc(V['sga25r'])} of sales"]}},
    body={"kind": "chart", "chart_type": "waterfall",
          "categories": ["FY2023", "Sales growth", "Gross margin rate", "Store labor", "Occupancy and energy", "E-commerce fulfillment", "FY2025"],
          "series": [{"name": "Operating income", "points": [P(x) for x in ("oi23", "wf_g", "wf_gm", "wf_lab", "wf_occ", "wf_ef", "oi25")]}],
          "sort": "none", "highlight": ["Gross margin rate", "E-commerce fulfillment"], "value_format": MONEY},
    footnotes=["Sales growth: the FY2023 operating margin applied to the $83M of extra sales. Other SG&A moved by less than $0.1M and is not shown"])

add(id="p13", role="content", section_id="1", status="filled", message_type="item", archetype="kpi-big-numbers",
    lead_message={"text": "Reaching 3.0% by FY2028 takes about $30M more operating income a year, and the covenant needs $4.7M more in FY2026",
                  "numbers": [{"text": "$30M", "data_ref": "gap_tgt"}, {"text": "$4.7M", "data_ref": "gap_cov"}]},
    unit_line="**Operating income**, $ millions, FY2025 actual against the lender covenant and the FY2028 target",
    body={"kind": "kpi", "items": [
        {"point": P("gap_cov"), "caption": "more needed in FY2026 to meet the lender's $20M covenant", "relation": f"FY2025: $15.3M, down {m(V['oi_fall25'])} in one year",
         "drivers": ["Another year like FY2025 would take operating income below zero", "Must come from actions that pay inside the year", "Sets the order of the plan (section 5)"]},
        {"point": P("gap_tgt"), "caption": "more a year to reach the 3.0% target at FY2025 sales", "relation": f"3.0% of $1,503M is {m(V['tgt_oi25'])}",
         "drivers": ["About twice today's operating income", "Within $25M of one-time cost or capital",
                     "Fewer stores lower the dollars needed (section 5)"]},
        {"point": P("mgmt_sav"), "caption": "a year: what management's 8% hours cut is expected to save", "relation": f"About {pc(V['mgmt_half'], 0)} of the gap to 3.0%",
         "drivers": [f"Margin of {pc(V['mgmt_m'])} even if all of it holds", "Aimed at labor, the smallest of the three causes", "Section 3 tests whether it would hold"]}]})

# ---------- section 2
nav("d2", "2")
add(id="L2", role="content", section_id="2", status="filled", message_type="argument", archetype="numbered-levers",
    lead_message={"text": "Gross margin offers the largest prize, through three moves: fewer promotions, more private label and less shrink", "count_word": 3},
    unit_line="**What the evidence shows for each move**, FY2025",
    body={"kind": "levers", "headers": ["Finding", "Evidence"], "items": [
        {"code": "2a", "text": "Promotions grew past the point where they pay, and the events that lose money can go first", "point": P("ev38"),
         "metric": "of FY2025 promotional events lost money after counting the extra units sold"},
        {"code": "2b", "text": "Private label earns more on every dollar and answers ValuMart on price", "point": P("pl_gap"),
         "metric": "more gross margin on private label than on national brands"},
        {"code": "2c", "text": "Shrink follows staffing, so it falls where receiving and produce work is protected", "point": P("q1"),
         "metric": "shrink in the least-staffed quarter of stores, against 2.3% in the best-staffed"}]},
    so_what=f"Sized on the following pages, the three moves are worth about {m(V['gm_gain'], 0)} a year by FY2028", so_what_style="line")

add(id="p2a1", role="content", section_id="2", tree_node="n2a", status="filled", message_type="component", archetype="bar-ranking",
    rationale="Drivers of one change, ranked -> bar",
    lead_message={"text": "The shift to promotions was the largest drag on gross margin, about four times what private label won back",
                  "highlights": ["Promotional mix"]},
    unit_line="**Change in gross margin by driver**, percentage points of sales, FY2023 to FY2025",
    layout={"variant": "takeaway_sidebar", "sidebar": {
        "kind": "big_number", "header": "Promotions, not prices, drained gross margin", "big_number": P("promo_cost"),
        "caption": "a year: what the shift to promotions costs at FY2025 sales",
        "bullets": ["**Promotional mix:** promoted sales earn 14 percentage points less, and their share rose by 5 percentage points",
                    "**Shrink:** up from 2.1% to 2.6% of sales, highest in thinly staffed stores (2c)",
                    "**Private label:** share up from 17.0% to 18.5%, at 12 percentage points more margin (2b)"]}},
    body={"kind": "chart", "chart_type": "bar", "categories": ["Promotional mix", "Shrink", "Private-label mix"],
          "series": [{"name": "Gross-margin effect", "points": [P("d_promo"), P("d_shr"), P("d_pl")]}],
          "sort": "none", "highlight": ["Promotional mix"], "value_format": PP},
    footnotes=[f"The three drivers add up to the {abs(V['d_gm3']):.2f} percentage-point fall in the gross-margin rate. Lower vendor funding works through the promotional gap and is not counted again"])

add(id="p2a2", role="content", section_id="2", tree_node="n2a", status="filled", message_type="time-series", archetype="multi-chart-panel",
    lead_message={"text": "Harlow pays more for promotions on two counts: 29% of sales are now promoted, and vendors fund less of each markdown",
                  "numbers": [{"text": "29%", "data_ref": "promo25"}], "clauses": 2},
    layout={"variant": "split_2"},
    body={"kind": "panels", "panels": [
        {"header": "One sales dollar in four was promoted in FY2023; nearly three in ten by FY2025", "unit_line": "**Promotional sales**, % of sales",
         "delta": P("promo_shift"), "body": {"kind": "chart", "chart_type": "column", "categories": ["FY2023", "FY2024", "FY2025"],
                                             "series": [{"name": "Promotional share", "points": [P("promo23"), P("promo24"), P("promo25")]}], "sort": "none", "value_format": "0.0%"}},
        {"header": f"Harlow now pays {pc(V['hf25'], 0)} of each markdown itself, up from {pc(V['hf23'], 0)}", "unit_line": "**Vendor funding**, % of promotional markdowns",
         "delta": P("vf_chg"), "body": {"kind": "chart", "chart_type": "column", "categories": ["FY2023", "FY2025"],
                                        "series": [{"name": "Vendor funding", "points": [P("vf23"), P("vf25")]}], "sort": "none", "value_format": "0%"}}]},
    footnotes=["Category managers raised promotional depth in FY2024–FY2025 \"to defend traffic against ValuMart\"; vendor funding for FY2024 is not in the briefing pack"])

add(id="p2a3", role="content", section_id="2", tree_node="n2a", status="filled", message_type="component", archetype="calculation-bridge",
    lead_message={"text": "To pay for themselves, promotions would need about 3.5% more sales, more than twice the gain the category team cites",
                  "numbers": [{"text": "3.5%", "data_ref": "bk"}]},
    unit_line="**Extra sales needed to pay for the shift to promotions**, % of sales, FY2023 to FY2025, team estimate",
    body={"kind": "equation", "terms": [
        {"point": P("promo_shift"), "caption": "more of sales sold on promotion, FY2023 to FY2025"},
        {"op": "×", "point": P("promo_gap"), "caption": "less gross margin on each promoted dollar"},
        {"op": "÷", "point": P("cr"), "caption": "contribution on a dollar of new sales (finance estimate)"},
        {"op": "=", "point": P("bk"), "caption": "more sales needed to cover the margin given up"}],
        "assumptions_header": "The category team's evidence falls well short of that bar",
        "assumptions": ["Stores with the deepest promotions grew comparable sales 1.8% in FY2025, against 0.2% for the rest: a gap of 1.6 percentage points",
                        "That gap is a one-year correlation; it does not show that promotions caused it",
                        "Promoted sales earn less than the 20 cents a dollar used here, so the true bar is higher",
                        "Meanwhile 41% of shoppers call Harlow more expensive, up from 33%: deeper promotions did not change price perception"]})

add(id="p2a4", role="content", section_id="2", tree_node="n2a", status="filled", message_type="item", archetype="bar-ranking",
    lead_message={"text": "The threat promotions were meant to answer is local: stores near a new ValuMart lost 4.2% of comparable sales",
                  "numbers": [{"text": "4.2%", "data_ref": "vm_comp"}], "highlights": ["Within 3 miles of a new ValuMart"]},
    unit_line="**Comparable-sales growth**, %, FY2025, Harlow stores by distance to a new ValuMart",
    layout={"variant": "takeaway_sidebar", "sidebar": {
        "kind": "bullets", "header": "Defend where ValuMart competes, cut elsewhere",
        "bullets": ["**Near ValuMart:** 11 stores have opened in Harlow trade areas since 2023; price investment can protect traffic there",
                    "**Rest of the chain:** still growing, so loss-making events can go there first, at the lowest risk",
                    "**Why shoppers come:** fresh produce (58%) and convenience (44%) lead, so broad promotions buy little loyalty"],
        "implication": "Cut loss-making events away from ValuMart first; keep targeted price investment where it competes"}},
    body={"kind": "chart", "chart_type": "bar", "categories": ["Within 3 miles of a new ValuMart", "Other Harlow stores"],
          "series": [{"name": "Comparable sales", "points": [P("vm_comp"), P("oth_comp")]}], "sort": "none",
          "highlight": ["Within 3 miles of a new ValuMart"], "value_format": "+0.0%;-0.0%"},
    footnotes=["The briefing pack does not give the number of Harlow stores within three miles of a ValuMart; that count sets how much promotional spend stays"])

add(id="p2b1", role="content", section_id="2", tree_node="n2b", status="filled", message_type="time-series", archetype="column-time-series",
    lead_message={"text": "Keeping private label's current pace would lift its share to about 21% by FY2028, worth about $3.8M a year",
                  "numbers": [{"text": "21%", "data_ref": "pl28"}, {"text": "$3.8M", "data_ref": "g_pl"}], "highlights": ["FY2028 plan"]},
    unit_line="**Private-label sales**, % of sales, FY2023–FY2025 actual, FY2028 at the FY2023–25 pace",
    layout={"variant": "takeaway_sidebar", "sidebar": {
        "kind": "bullets", "header": "The value answer that also pays",
        "bullets": ["**Margin:** each dollar moved from national brands earns 12 cents more gross margin",
                    "**ValuMart:** an own-brand price ladder answers the 41% who find Harlow expensive, without deeper promotions"],
        "rows": [{"label": "Gross margin gained a year by FY2028", "basis": f"{V['pl_add']:.2f} pp of sales × 12 pp margin gap × ${V['B']:,.0f}M sales",
                  "point": P("g_pl"), "highlight": True}]}},
    body={"kind": "chart", "chart_type": "column", "categories": ["FY2023", "FY2024", "FY2025", "FY2028 plan"],
          "series": [{"name": "Private-label share", "points": [P("plsh23"), P("plsh24"), P("plsh25"), P("pl28")]}],
          "sort": "none", "highlight": ["FY2028 plan"], "value_format": "0.0%"},
    basis={"header": "How we projected it", "terms": [
        {"point": P("plsh25"), "caption": "private-label share of sales, FY2025"},
        {"op": "+", "point": P("pl_add"), "caption": "added by FY2028: 0.75 pp a year for 3 years"},
        {"op": "=", "point": P("pl28"), "caption": "share in FY2028"}]})

add(id="p2c1", role="content", section_id="2", tree_node="n2c", status="filled", message_type="item", archetype="bar-ranking",
    lead_message={"text": "Shrink rises as staffing thins: the least-staffed stores lose 3.1% of sales, against 2.3% in the best-staffed",
                  "numbers": [{"text": "3.1%", "data_ref": "q1"}, {"text": "2.3%", "data_ref": "q4"}], "highlights": ["Q1, fewest hours"]},
    unit_line="**Shrink**, % of sales, FY2025, stores in quarters by labor hours per $1,000 of sales",
    layout={"variant": "takeaway_sidebar", "sidebar": {
        "kind": "bullets", "header": "Thin staffing shows up as waste",
        "bullets": ["**Q1:** store managers say produce rotation and receiving checks are skipped on busy days",
                    f"**Q3 to Q4:** the extra hours buy only {V['q34']:.1f} percentage points less shrink, so Q4 stores can give hours up",
                    "**What is lost:** fresh and produce waste is 45% of shrink and receiving errors 20%, the losses staffing controls",
                    f"**Chain:** shrink rose from 2.1% to 2.6% of sales as hours per $1,000 of sales fell {abs(V['hrs_g'])*100:.1f}%"]}},
    body={"kind": "chart", "chart_type": "bar", "categories": ["Q1, fewest hours", "Q2", "Q3", "Q4, most hours"],
          "series": [{"name": "Shrink", "points": [P("q1"), P("q2"), P("q3"), P("q4")]}], "sort": "none",
          "highlight": ["Q1, fewest hours"], "benchmark": {"label": "Chain average", "point": P("shr25")}, "value_format": "0.0%"})

add(id="p2c2", role="content", section_id="2", tree_node="n2c", status="filled", message_type="component", archetype="calculation-bridge",
    lead_message={"text": "Bringing the two least-staffed quarters of stores to the third quarter's shrink would save about $3.5M a year",
                  "numbers": [{"text": "$3.5M", "data_ref": "g_sh"}]},
    unit_line="**Shrink saving**, $ millions a year, FY2028 run rate on the sales base after store exits, team estimate",
    body={"kind": "equation", "terms": [
        {"point": P("q_gap"), "caption": f"excess shrink of Q1 ({V['q1gap']:.1f} pp) and Q2 ({V['q2gap']:.1f} pp) stores over Q3's 2.4%"},
        {"op": "×", "point": P("qshare"), "caption": "of chain sales in each quarter of stores"},
        {"op": "×", "point": P("B"), "caption": "sales base after the store exits (section 5)"},
        {"op": "=", "point": P("g_sh"), "caption": "saving a year"}],
        "assumptions_header": "Hours move between stores; they are not added",
        "assumptions": ["Hours for receiving checks and produce rotation come from Q4 stores, where extra hours cut shrink the least",
                        "Each quarter of stores carries about a quarter of sales; the four then average 2.6%, the chain's FY2025 shrink",
                        "Theft, 35% of shrink, is assumed unchanged",
                        "Treats the pattern across store quarters as cause and effect; Q4 shrink may rise a little as hours leave",
                        f"Chain shrink would fall from 2.6% to about {pc(V['shr_new'])}, still above FY2023's 2.1%"]})

# ---------- section 3
nav("d3", "3")
add(id="L3", role="content", section_id="3", status="filled", message_type="argument", archetype="numbered-levers",
    lead_message={"text": "Store costs should be reshaped rather than cut, by redeploying hours and exiting the weakest stores as leases end"},
    unit_line="**What the evidence shows for each store-cost move**, FY2025",
    body={"kind": "levers", "headers": ["Finding", "Evidence"], "items": [
        {"code": "3a", "text": "An 8% hours cut targets the smallest cause, and much of its saving would come back as shrink", "point": P("sh_lab"),
         "metric": "of the operating-income shortfall since FY2023 came from store labor"},
        {"code": "3b", "text": "Six of the nine loss-making stores can close at lease end, with no board vote needed", "point": P("lease6"),
         "metric": "of the nine stores with negative four-wall EBITDA have leases ending by 2027"}]},
    callout={"target": "3a", "header": "Management's draft plan", "detail": "Built on wages, the line behind about an eighth of the decline"})

add(id="p3a1", role="content", section_id="3", tree_node="n3a", status="filled", message_type="item", archetype="kpi-big-numbers",
    lead_message={"text": "Wages are not the main cause: fewer hours absorbed most of a 9% pay rise, and labor rose 0.3 percentage points",
                  "numbers": [{"text": "9%", "data_ref": "wage_g"}, {"text": "0.3 percentage points", "data_ref": "lab_pp"}]},
    unit_line="**Store labor**, FY2023 to FY2025",
    body={"kind": "kpi", "items": [
        {"point": P("wage_g"), "caption": "rise in the average hourly wage, including benefits", "relation": "From $16.80 to $18.38 an hour",
         "drivers": ["State minimum-wage increases", "A tight local labor market", "The cause the draft plan is built on"]},
        {"point": P("hrs_g"), "caption": "change in labor hours per $1,000 of sales", "relation": "From 7.02 to 6.60 hours",
         "drivers": ["Stores already run leaner than in FY2023", "Total hours roughly flat while sales grew 6%", "The least-staffed stores now show the most shrink (2c)"]},
        {"point": P("lab_pp"), "caption": "rise in store labor as a share of sales", "relation": "From 11.8% to 12.1% of sales",
         "drivers": ["Fewer hours per sales dollar offset nearly three-quarters of the wage rise", "Labor is the smallest of the three causes (section 1)",
                     "The 2027 minimum-wage rise of 4% needs the same productivity again (backup)"]}]})

add(id="p3a2", role="content", section_id="3", tree_node="n3a", status="filled", message_type="component", archetype="calculation-bridge",
    lead_message={"text": "An 8% hours cut could give back up to $10M of its $14.5M saving through higher shrink",
                  "numbers": [{"text": "$10M", "data_ref": "giveback"}, {"text": "$14.5M", "data_ref": "mgmt_sav"}]},
    unit_line="**Net saving from an 8% cut in store labor hours**, $ millions a year, team estimate",
    body={"kind": "equation", "terms": [
        {"point": P("mgmt_sav"), "caption": "saving management expects: 8% of $181.9M of store labor"},
        {"op": "−", "point": P("giveback"), "caption": "extra shrink if it rises with fewer hours as it did in FY2023–25"},
        {"op": "=", "point": P("net_cut"), "caption": "net saving, before any lost sales"}],
        "assumptions_header": "The upper bound puts the whole FY2023–25 rise in shrink down to thinner staffing",
        "assumptions": [f"FY2023–25: hours per $1,000 of sales fell {abs(V['hrs_g'])*100:.1f}% and shrink rose 0.5 percentage points, about {V['el']:.2f} for each 1% fewer hours",
                        f"An 8% cut would add about {V['sh_add']:.2f} percentage points of shrink on FY2025 sales of $1,503M",
                        "Not counted: lost sales from checkout waits and stock-outs, though fresh produce (58%) and convenience (44%) are why shoppers come",
                        f"Even if all of the $14.5M held, the margin would reach only about {pc(V['mgmt_m'])}"]})

add(id="p3b1", role="content", section_id="3", tree_node="n3b", status="filled", message_type="item", archetype="kpi-big-numbers",
    lead_message={"text": "Nine stores lose money at the four-wall level, and six can go without a board vote as leases end",
                  "numbers": [{"text": "Nine", "data_ref": "weak_n"}, {"text": "six", "data_ref": "lease6"}]},
    unit_line="**Stores with negative four-wall EBITDA**, FY2025",
    body={"kind": "kpi", "items": [
        {"point": P("weak_n"), "caption": "of 58 stores had negative four-wall EBITDA", "drivers": ["Before any allocation of head-office cost", "Candidates to exit or turn around"]},
        {"point": P("weak_s"), "caption": "combined sales of the nine stores, with a four-wall EBITDA loss of $3.1M", "relation": f"{pc(V['weak_sh'])} of chain sales",
         "drivers": ["25% of the sales would move to nearby Harlow stores, as in past closures", "The EBITDA loss goes away with an exit", "Store depreciation would also stop"]},
        {"point": P("lease6"), "caption": "of the nine have leases ending by 2027", "drivers": ["No board vote needed to let them expire", "The other three need a vote and $7.5M to exit"]}]},
    so_what="Letting the six leases run out costs nothing and needs no board vote")

add(id="p3b2", role="content", section_id="3", tree_node="n3b", status="filled", message_type="component", archetype="calculation-bridge",
    lead_message={"text": "Exiting the nine stores would add about $6.6M a year, and the six with expiring leases need no board vote",
                  "numbers": [{"text": "$6.6M", "data_ref": "g_st"}]},
    unit_line="**Gain from exiting the nine stores**, $ millions a year, team estimate",
    body={"kind": "equation", "terms": [
        {"point": P("weak_s"), "caption": "combined sales of the nine stores"},
        {"op": "×", "point": P("transfer"), "caption": "moves to a nearby Harlow store (past closures)"},
        {"op": "×", "point": P("recv_cm"), "caption": "contribution on the moved sales"},
        {"op": "+", "point": P("e_loss9"), "caption": "four-wall EBITDA loss removed"},
        {"op": "=", "point": P("g_st"), "caption": "gain a year from exiting all nine"}],
        "assumptions_header": "Six exits need no board vote; the other three cost $7.5M",
        "assumptions": [f"The six stores with leases ending by 2027 add about {m(V['g_st6'])} a year, if the gain splits evenly by store",
                        f"The other three add about {m(V['g_st3'])} a year for a one-time $7.5M, a payback of about {V['payback3']:.1f} years, and need a board vote",
                        "Four-wall EBITDA stands in for the operating-income effect; depreciation saved is not counted",
                        f"Chain sales fall by about {m(V['lost_st'])}, the 75% of the nine stores' sales that does not move"]})

# ---------- section 4
nav("d4", "4")
add(id="L4", role="content", section_id="4", status="filled", message_type="argument", archetype="numbered-levers",
    lead_message={"text": "E-commerce can keep its delivery service, but only if delivery stops being subsidized"},
    unit_line="**What the evidence shows on e-commerce**, FY2025",
    body={"kind": "levers", "headers": ["Finding", "Evidence"], "items": [
        {"code": "4a", "text": "Counted in full, e-commerce loses money; the reported profit leaves out delivery and counts every sale as new", "point": P("inc"),
         "metric": "of online spend is new to Harlow; the rest would have been spent in its stores"},
        {"code": "4b", "text": "Home delivery, not click-and-collect, causes most of the loss", "point": P("gap_d25"),
         "metric": "per delivered order: third-party delivery cost minus the fee collected"},
        {"code": "4c", "text": "Repricing delivery as tested recovers part of the loss and keeps the service", "point": P("t_fee"),
         "metric": "average fee per delivered order in the fee test, against $3.10 today"}]})

add(id="p4a1", role="content", section_id="4", tree_node="n4a", status="filled", message_type="time-series", archetype="column-time-series",
    lead_message={"text": "E-commerce fulfillment cost more than tripled in two years, to $18.1M, the fastest-rising cost Harlow has",
                  "numbers": [{"text": "$18.1M", "data_ref": "ef25"}], "highlights": ["FY2025"]},
    unit_line="**E-commerce fulfillment cost**, picking plus third-party delivery net of delivery fees, $ millions",
    layout={"variant": "takeaway_sidebar", "sidebar": {
        "kind": "bullets", "header": "Growth came with the costliest kind of order",
        "bullets": [f"**Orders:** {V['ord_mult']:.1f} times as many as in FY2023, at a steady basket of about $96",
                    "**Home delivery:** up from 45% to 58% of orders, the order type that costs the most",
                    f"**Gap per delivery:** third-party cost minus fee widened from ${V['gap_d23']:.2f} to ${V['gap_d25']:.2f}"],
        "rows": [{"label": "Fulfillment cost per dollar of e-commerce sales, FY2025", "point": P("ef_ps")}]}},
    body={"kind": "chart", "chart_type": "column", "categories": ["FY2023", "FY2024", "FY2025"],
          "series": [{"name": "Fulfillment cost", "points": [P("ef23"), P("ef24"), P("ef25")]}], "sort": "none",
          "highlight": ["FY2025"], "value_format": MONEY},
    footnotes=["E-commerce rose from 3.0% to 8.5% of sales over the same two years"])

add(id="p4a2", role="content", section_id="4", tree_node="n4a", status="filled", message_type="component", archetype="calculation-bridge",
    lead_message={"text": "Counted in full, e-commerce loses about $10M a year, because its new sales cover less than half of fulfillment",
                  "numbers": [{"text": "$10M", "data_ref": "e_loss"}]},
    unit_line="**E-commerce contribution after fulfillment**, $ millions, FY2025, team estimate",
    body={"kind": "equation", "terms": [
        {"point": P("es25"), "caption": "e-commerce sales: 8.5% of $1,503M"},
        {"op": "×", "point": P("inc"), "caption": "new to Harlow: 70% would have been spent in its stores (survey, n = 2,300)"},
        {"op": "×", "point": P("cr"), "caption": "contribution on a dollar of new sales (finance)"},
        {"op": "−", "point": P("ef25"), "caption": "fulfillment: picking plus delivery, net of fees"},
        {"op": "=", "point": P("e_loss"), "caption": "contribution after fulfillment"}],
        "assumptions_header": "Where data is missing, the estimate favors e-commerce",
        "assumptions": ["Store costs saved when an existing customer shops online instead are not in the pack and are not counted",
                        "The 30% of new spend comes from customers' own answers and could be lower",
                        "Packaging and technology costs outside the fulfillment line are not counted",
                        f"New sales cover {pc(V['e_cover'], 0)} of fulfillment; home delivery carries about nine-tenths of the loss (4b)"]})

add(id="p4a3", role="content", section_id="4", tree_node="n4a", status="filled", message_type="item", archetype="comparison-table",
    lead_message={"text": "The team's 6.1% profit comes from leaving out delivery and counting every online sale as new",
                  "numbers": [{"text": "6.1%", "data_ref": "team_cm"}]},
    body={"kind": "table", "table_type": "comparison", "columns": ["E-commerce team", "Full count (this review)"], "rows": [
        {"label": "Sales counted", "cells": [{"text": "All e-commerce sales, as if every one were new"}, {"text": "Only the 30% of online spend that is new to Harlow"}],
         "note": "Survey of 2,300 online customers"},
        {"label": "Third-party delivery", "cells": [{"text": "Left out: finance books it under fulfillment"}, {"text": "Included, net of the fees customers pay"}],
         "note": f"{m(V['dnet'])} net in FY2025"},
        {"label": "Picking and store costs", "cells": [{"text": "Picking, packaging and a share of store variable costs deducted"}, {"text": "Picking deducted; store costs sit inside the 20 cents of contribution"}],
         "note": "Similar on both sides"},
        {"label": "Result, FY2025", "cells": [{"point": P("team_cm")}, {"text": f"A loss of about {m(abs(V['e_loss']))}, {pc(abs(V['e_rate']), 0)} of e-commerce sales"}],
         "note": f"A swing of nearly {m(V['team_usd'] - V['e_loss'], 0)}"}],
        "verdict_header": "What it changes"},
    callout={"target": "Sales counted", "header": "Largest correction", "detail": "70% of online spend would have been spent in Harlow stores anyway"},
    footnotes=[f"Team figure: 6.1% of FY2025 e-commerce sales of {m(V['es25'])}, about {m(V['team_usd'])}"])

add(id="p4b1", role="content", section_id="4", tree_node="n4b", status="filled", message_type="component", archetype="waterfall-bridge",
    lead_message={"text": "Each home delivery loses about $12, more than seven times the loss on a click-and-collect order",
                  "numbers": [{"text": "$12", "data_ref": "loss_do"}], "highlights": ["Third-party delivery"]},
    unit_line="**Economics of one delivered order**, $ per order, FY2025, team estimate",
    layout={"variant": "takeaway_sidebar", "sidebar": {
        "kind": "big_number", "header": "Delivery, not online shopping, is the problem", "big_number": P("lossx"),
        "caption": "the loss on a click-and-collect order, which carries no delivery charge",
        "bullets": [f"**Click-and-collect:** loses about ${abs(V['cc_loss']):.2f} an order, the picking cost less contribution",
                    "**Third-party delivery:** the largest cost, rising every year while the fee fell",
                    "**Delivered orders:** 58% of orders but about nine-tenths of the e-commerce loss"]}},
    body={"kind": "chart", "chart_type": "waterfall",
          "categories": ["Contribution from new sales", "Picking", "Third-party delivery", "Delivery fee", "Result per delivered order"],
          "series": [{"name": "$ per order", "points": [P("c_do"), P("pick_n"), P("dlv_n"), P("fee25"), P("loss_do")]}],
          "sort": "none", "highlight": ["Third-party delivery"], "value_format": '"$"0.00;-"$"0.00'},
    basis={"header": "How we estimated it", "terms": [
        {"point": P("bsk25"), "caption": "average basket"},
        {"op": "×", "point": P("inc"), "caption": "new to Harlow (survey)"},
        {"op": "×", "point": P("cr"), "caption": "contribution per new dollar"},
        {"op": "−", "point": P("cost_do"), "caption": "picking plus delivery, less the fee"},
        {"op": "=", "point": P("loss_do"), "caption": "result per delivered order"}]})

add(id="p4c1", role="content", section_id="4", tree_node="n4c", status="filled", message_type="item", archetype="kpi-big-numbers",
    lead_message={"text": "Customers accept a higher delivery fee: the test doubled the fee per delivery while e-commerce sales fell only 2%",
                  "numbers": [{"text": "2%", "data_ref": "t_sales"}]},
    unit_line="**Fee test results**, 4 stores, 10 weeks, late FY2025: delivery fee $7.99, free delivery from $100",
    body={"kind": "kpi", "items": [
        {"point": P("t_fee"), "caption": "average fee per delivered order, up from $3.10", "relation": f"{V['fee_mult']:.1f} times the FY2025 average",
         "drivers": ["Fee below the threshold up from $4.99 to $7.99", "Free-delivery threshold up from $75 to $100"]},
        {"point": P("t_dl"), "caption": "change in delivered orders", "drivers": ["Some customers moved to click-and-collect", "Fewer of the orders that lose the most"]},
        {"point": P("t_cc"), "caption": "change in click-and-collect orders", "drivers": ["Click-and-collect stays free", "Keeps the customer at a fraction of the cost (4b)"]},
        {"point": P("t_sales"), "caption": "change in total e-commerce sales", "drivers": ["Most demand stayed with Harlow", "Only 4 stores for 10 weeks: confirm in the rollout"]}]},
    so_what="Delivery stays, priced closer to what it costs")

add(id="p4c2", role="content", section_id="4", tree_node="n4c", status="filled", message_type="component", archetype="calculation-bridge",
    lead_message={"text": "Rolled out to every store, the tested fee would cut the e-commerce loss by about $2.8M a year",
                  "numbers": [{"text": "$2.8M", "data_ref": "g_fee"}]},
    unit_line="**Annual gain from the tested delivery fee, chain-wide**, $ millions, FY2025 volumes, team estimate",
    body={"kind": "equation", "terms": [
        {"point": P("ef25"), "caption": "fulfillment cost, FY2025"},
        {"op": "−", "point": P("ef_t"), "caption": "fulfillment cost with the test's order mix and fee"},
        {"op": "−", "point": P("lost_c"), "caption": "contribution lost on 2% lower e-commerce sales"},
        {"op": "=", "point": P("g_fee"), "caption": "gain a year"}],
        "assumptions_header": "The fee is a first step; the delivery contract matters as much",
        "assumptions": ["Delivered orders fall 9% and click-and-collect orders rise 14%, as in the test; fees average $6.40 a delivery",
                        "Costs per order stay at FY2025 levels: $7.40 to pick, $13.80 to deliver",
                        f"Every $1 off the delivery rate at renewal adds about {m(V['per1'])} a year; the proposed 3% rise would cost about {m(V['rise_c'])}",
                        f"E-commerce would still lose about {m(abs(V['e_after']))} a year, so the contract renewal and the shift to click-and-collect must follow"]})

# ---------- section 5
nav("d5", "5")
add(id="L5", role="content", section_id="5", status="filled", message_type="component", archetype="calculation-bridge",
    lead_message={"text": "Together the actions would lift operating income from $15.3M to about $42M a year by FY2028",
                  "numbers": [{"text": "$15.3M", "data_ref": "oi25"}, {"text": "$42M", "data_ref": "oi28"}]},
    unit_line="**Operating income, FY2025 to FY2028 run rate**, $ millions, at FY2025 prices and volumes, team estimate",
    body={"kind": "equation", "terms": [
        {"point": P("oi25"), "caption": "operating income, FY2025"},
        {"op": "+", "point": P("gm_gain"), "caption": "gross margin: promotions to 24% of sales, private label to about 21%, less shrink (2)"},
        {"op": "+", "point": P("g_fee"), "caption": "delivery fee and threshold as tested (4c)"},
        {"op": "+", "point": P("g_st"), "caption": "nine store exits, three of them subject to a board vote (3b)"},
        {"op": "=", "point": P("oi28"), "caption": "operating income, FY2028 run rate"}],
        "assumptions_header": "What the total includes and leaves out",
        "assumptions": [f"Gross margin: promotions {m(V['g_promo'])}, private label {m(V['g_pl'])}, shrink {m(V['g_sh'])}, on sales of ${V['B']:,.0f}M after the exits",
                        "One-time cost: $7.5M to exit three leases, within the $25M limit; the other actions need little capital",
                        "Store labor held at 12.1% of sales: scheduling must absorb the 2027 minimum-wage rise of 4%",
                        "Not counted: sales growth, a lower delivery rate at renewal, and depreciation saved by the exits",
                        f"On the smaller sales base, 3.0% means about {m(V['tgt28'])} of operating income, not the {m(V['tgt_oi25'])} at FY2025 sales"]})

add(id="p5b", role="content", section_id="5", status="filled", message_type="time-series", archetype="column-time-series",
    lead_message={"text": "The plan returns the operating margin to about 3.0% by FY2028, with almost no cushion",
                  "numbers": [{"text": "3.0%", "data_ref": "m28"}], "highlights": ["FY2028 plan"]},
    unit_line="**Operating margin**, % of sales, FY2023–FY2025 actual, FY2028 plan run rate",
    layout={"variant": "takeaway_sidebar", "sidebar": {
        "kind": "bullets", "header": "The cushion has to come from contracts and scheduling",
        "bullets": [f"**Gap:** about {m(abs(V['short28']))} below 3.0% of sales",
                    f"**Delivery:** each $1 off the rate adds {m(V['per1'])} a year",
                    "**2027 wage rise:** if scheduling does not absorb it, about 2.5%"],
        "rows": [{"label": "Rate cut that closes the gap", "basis": f"{m(abs(V['short28']))} ÷ about {V['dl_t']:,.0f} thousand delivered orders",
                  "point": P("cut_need"), "highlight": True}],
        "implication": "Treat the delivery re-tender as part of the plan, not an upside"}},
    body={"kind": "chart", "chart_type": "column", "categories": ["FY2023", "FY2024", "FY2025", "FY2028 plan"],
          "series": [{"name": "Operating margin", "points": [P("om23"), P("om24"), P("om25"), P("m28")]}], "sort": "none",
          "highlight": ["FY2028 plan"], "benchmark": {"label": "Target, FY2028", "point": P("tgt")}, "value_format": "0.00%"},
    basis={"header": "How the margin is computed", "terms": [
        {"point": P("oi28"), "caption": "operating income, FY2028 run rate"},
        {"op": "÷", "point": P("B"), "caption": "sales after store exits and the fee change"},
        {"op": "=", "point": P("m28"), "caption": "operating margin, FY2028"}]})

add(id="p5c", role="content", section_id="5", status="filled", message_type="item", archetype="comparison-table",
    lead_message={"text": "The recommended plan beats the labor-cut plan on margin, on the covenant and on risk to shoppers"},
    body={"kind": "table", "table_type": "comparison",
          "columns": ["Management's draft: cut hours 8%, freeze e-commerce", "Recommended plan"], "rows": [
        {"label": "FY2028 operating margin", "highlight": True,
         "cells": [{"text": f"About {pc(V['mgmt_m'])} if the full $14.5M holds; nearer {pc(V['mgmt_low'])} if shrink rises as in FY2023–25"},
                   {"text": f"About 3.0% ({pc(V['m28'], 2)}), with the delivery contract as the cushion"}], "note": "Only the plan reaches the target"},
        {"label": "FY2026 operating income", "cells": [{"text": f"{m(V['mgmt26_low'])} to {m(V['mgmt26'])}, depending on how shrink responds"},
                                                     {"text": f"About {m(V['oi26'], 0)} from promotions and the fee alone"}], "note": "Ours clears $20M without a bet on shrink"},
        {"label": "Risk to shoppers", "cells": [{"text": "Fewer staff for fresh produce and checkouts, the top reasons to shop Harlow"},
                                               {"text": "Fewer promotions, with price investment kept near ValuMart"}], "note": "Smaller and targeted"},
        {"label": "E-commerce", "cells": [{"text": f"Frozen at a loss of about {m(abs(V['e_loss']), 0)} a year"},
                                         {"text": f"Loss cut to about {m(abs(V['e_after']))}; delivery kept"}], "note": "Both keep delivery"},
        {"label": "One-time cost", "cells": [{"text": "None"}, {"text": "$7.5M for three lease exits, of the $25M limit"}], "note": "Within the limit"}],
          "verdict_header": "Verdict"})

add(id="p5d", role="content", section_id="5", status="filled", message_type="component", archetype="calculation-bridge",
    lead_message={"text": "Started at the beginning of FY2026, promotions and delivery pricing alone would lift operating income to about $23M",
                  "numbers": [{"text": "$23M", "data_ref": "oi26"}]},
    unit_line="**FY2026 operating income**, $ millions, team estimate",
    body={"kind": "equation", "terms": [
        {"point": P("oi25"), "caption": "operating income, FY2025"},
        {"op": "+", "point": P("g_promo26"), "caption": f"half the promotion reset: loss-making events cut first, promotions to {pc(V['promo26'])} of sales"},
        {"op": "+", "point": P("g_fee"), "caption": "delivery fee and threshold from the start of the year"},
        {"op": "=", "point": P("oi26"), "caption": "operating income, FY2026"}],
        "assumptions_header": "The covenant holds only if the FY2025 slide stops",
        "assumptions": [f"Every other line holds at its FY2025 share of sales; a repeat of FY2025's {m(V['oi_fall25'])} fall would breach the covenant",
                        "That fall came from promotions, shrink and e-commerce, the lines these two actions address",
                        f"Headroom over the $20M covenant: about {m(V['head26'])}",
                        "If FY2026 is the year ending January 2027, most of it has passed by the board meeting: start both actions now and agree the test with the lender"]})

add(id="p5e", role="content", section_id="5", status="filled", message_type="structure", archetype="timeline-roadmap",
    lead_message={"text": "Promotions and the delivery fee come first because they need no capital and add profit within FY2026"},
    unit_line="**Plan sequence by action**, half-years, FY2026–FY2028",
    layout={"variant": "full"},
    body={"kind": "timeline", "periods": ["FY2026 H1", "FY2026 H2", "FY2027 H1", "FY2027 H2", "FY2028"], "rows": [
        {"label": "Promotions", "bars": [{"start": "FY2026 H1", "end": "FY2026 H2", "label": "Cut loss-making events, away from ValuMart first", "emphasis": True},
                                         {"start": "FY2027 H1", "end": "FY2027 H2", "label": "Back to 24% of sales"}]},
        {"label": "Delivery", "bars": [{"start": "FY2026 H1", "end": "FY2026 H1", "label": "Tested fee chain-wide", "emphasis": True},
                                       {"start": "FY2026 H2", "end": "FY2026 H2", "label": "Re-tender the contract"}]},
        {"label": "Shrink", "bars": [{"start": "FY2026 H1", "end": "FY2026 H2", "label": "Move hours to receiving and produce"}]},
        {"label": "Private label", "bars": [{"start": "FY2026 H2", "end": "FY2028", "label": "New own-brand lines, about 0.75 pp of share a year"}]},
        {"label": "Store exits", "bars": [{"start": "FY2027 H1", "end": "FY2027 H2", "label": "Six leases end; three exits after a board vote"}]}],
          "milestones": [{"at": "FY2026 H1", "label": "Board approval"}, {"at": "FY2026 H2", "label": "Covenant test"}]},
    so_what="Approve the promotion reset and the fee now; the store vote and private label follow", so_what_style="line",
    footnotes=["Fiscal years as in the briefing pack, with FY2026 as the first plan year; confirm the covenant test period with the CFO"])

add(id="p5f", role="content", section_id="5", status="filled", message_type="item", archetype="comparison-table",
    lead_message={"text": "Five risks need an owner from the start, led by a loss of traffic to ValuMart", "count_word": 5},
    body={"kind": "table", "table_type": "comparison", "columns": ["What could go wrong", "How we reduce it", "Owner"], "rows": [
        {"label": "ValuMart traffic", "cells": [{"text": "Shoppers leave when promotions are cut"}, {"text": "Cut away from ValuMart first; private label as the value answer"}, {"text": "Chief merchant"}],
         "note": "Comparable sales near ValuMart"},
        {"label": "2027 wage rise", "cells": [{"text": "A 4% rise lifts labor above 12.1% of sales"}, {"text": f"Schedule to demand: about {V['hrs_need']:.2f} hours per $1,000 of sales"}, {"text": "COO"}],
         "note": "Labor, % of sales"},
        {"label": "Delivery demand", "cells": [{"text": "Customers drop delivery at the higher fee"}, {"text": "Steer them to free click-and-collect; review after a quarter"}, {"text": "E-commerce lead"}],
         "note": "Delivered and collected orders"},
        {"label": "Delivery contract", "cells": [{"text": "The provider pushes through its 3% rise"}, {"text": "Re-tender before renewal"}, {"text": "CFO"}],
         "note": "Rate per delivered order"},
        {"label": "Store exits", "cells": [{"text": "Less than 25% of the stores' sales moves to nearby stores"}, {"text": "Plan the transfer of customers before each exit"}, {"text": "Real estate"}],
         "note": "Sales kept after exits"}], "verdict_header": "Watch point"},
    callout={"target": "ValuMart traffic", "header": "Largest risk", "detail": "Stores near a new ValuMart already lost 4.2% of comparable sales"})

add(id="p5g", role="content", section_id="5", status="filled", message_type="item", archetype="data-table",
    lead_message={"text": "Six numbers will tell the board each quarter whether the plan is working", "count_word": 6},
    body={"kind": "table", "table_type": "data", "columns": ["FY2025", "Target", "By"], "rows": [
        {"label": "Promotional sales, % of sales", "cells": [{"point": P("promo25")}, {"text": "24%, the FY2023 level"}, {"text": "FY2027"}], "note": "Biggest lever; watch comps near ValuMart (2a)"},
        {"label": "Shrink, % of sales", "cells": [{"point": P("shr25")}, {"text": f"About {pc(V['shr_new'])}"}, {"text": "FY2027"}], "note": "Q1 and Q2 stores first, monthly (2c)"},
        {"label": "Average fee per delivered order", "cells": [{"point": P("fee25")}, {"text": "$6.40, as in the test"}, {"text": "FY2026"}], "note": "With delivered and collected orders (4c)"},
        {"label": "Private-label sales, % of sales", "cells": [{"point": P("plsh25")}, {"text": "About 21%"}, {"text": "FY2028"}], "note": "The value answer to ValuMart (2b)"},
        {"label": "Store labor, % of sales", "cells": [{"point": P("lp25")}, {"text": "12.1% or less"}, {"text": "Every year"}], "note": "Absorbs the 2027 wage rise (3a)"},
        {"label": "Operating income, $M", "cells": [{"point": P("oi25")}, {"text": "$20M or more; about $42M"}, {"text": "FY2026; FY2028"}], "note": "Covenant first, then the target (5)"}],
          "verdict_header": "Why it matters"},
    footnotes=["Reported to the board each quarter; promotional share, shrink and the delivery fee also by store group (near ValuMart, rest of chain)"])

# ---------- appendix
add(id="app", role="appendix_divider", status="filled")
add(id="bx", role="backup", section_id="1", status="filled", message_type="item", archetype="comparison-table",
    lead_message={"prefix": "BACKUP:", "text": "Four other routes were left out on purpose, two because they would make the problem worse"},
    tree_node=["nx1", "nx2", "nx3", "nx4"],
    body={"kind": "table", "table_type": "definition", "columns": ["Hypothesis", "Why it is not in the plan"], "rows": [
        {"label": "Overhead", "cells": [{"text": "Cutting other SG&A would restore the margin"}, {"text": "It held at 4.7% of sales in FY2023–25, so it did not cause the decline"}]},
        {"label": "Close delivery", "cells": [{"text": "Closing home delivery would remove most of the e-commerce loss"}, {"text": "The family owners want delivery kept; repricing it is the route (4c)"}]},
        {"label": "Match ValuMart", "cells": [{"text": "Matching ValuMart's prices chain-wide would win back traffic"}, {"text": "Deeper promotions already lost margin and did not change price perception (2a)"}]},
        {"label": "Raise prices", "cells": [{"text": "Raising shelf prices chain-wide would rebuild gross margin"}, {"text": "41% of shoppers already call Harlow more expensive, up from 33%"}]}]})

ROWS_PL = [("Gross profit", "gp"), ("Store labor", "lab"), ("Occupancy and energy", "occ"), ("E-commerce fulfillment", "ef"), ("Other SG&A", "sga"), ("Operating income", "oi")]
add(id="b1", role="backup", section_id="1", backup_of="p12", status="filled", message_type="item", archetype="data-table",
    lead_message={"prefix": "BACKUP:", "text": "As a share of sales, every line except other SG&A has moved against Harlow since FY2023"},
    unit_line="**Income statement**, % of sales, fiscal years ending in January",
    body={"kind": "table", "table_type": "data", "columns": ["FY2023", "FY2024", "FY2025", "Change, pp"], "rows": [
        {"label": lab, "cells": [P2 for P2 in ({"point": P(f"{k}23r")}, {"point": P(f"{k}24r")}, {"point": P(f"{k}25r")}, {"point": P(f"{k}_dpp")})],
         **({"highlight": True} if k in ("gp", "ef") else {})} for lab, k in ROWS_PL]},
    footnotes=["Source figures in $ millions in Table 1 of the briefing pack; FY2024 operating income is reported as $33.4M although the lines sum to $33.3M"])

add(id="b2", role="backup", section_id="2", backup_of="p2a1", status="filled", message_type="item", archetype="data-table",
    lead_message={"prefix": "BACKUP:", "text": "Promotional mix, private label and shrink account for essentially all of the fall in the gross-margin rate"},
    unit_line="**Gross-margin drivers**, % of sales and percentage points, FY2023–FY2025",
    body={"kind": "table", "table_type": "data", "columns": ["FY2023", "FY2024", "FY2025", "Margin effect, pp"], "rows": [
        {"label": "Promotional sales, share of sales", "cells": [{"point": P("promo23")}, {"point": P("promo24")}, {"point": P("promo25")}, {"point": P("d_promo")}], "highlight": True},
        {"label": "Private-label sales, share of sales", "cells": [{"point": P("plsh23")}, {"point": P("plsh24")}, {"point": P("plsh25")}, {"point": P("d_pl")}]},
        {"label": "Shrink, % of sales", "cells": [{"point": P("shr23")}, {"point": P("shr24")}, {"point": P("shr25")}, {"point": P("d_shr")}]},
        {"label": "Sum of the three drivers", "cells": [{"text": ""}, {"text": ""}, {"text": ""}, {"point": P("d_gm3")}]},
        {"label": "Reported gross-margin rate", "cells": [{"point": P("gp23r")}, {"point": P("gp24r")}, {"point": P("gp25r")}, {"point": P("gp_dpp")}]}]},
    footnotes=["Margin effects: change in share × 14 pp (promotions) or × 12 pp (private label); shrink is a direct deduction",
               "Vendor funding fell from 55% to 46% of markdowns; it acts through the promotional margin gap and is not a separate driver"])

add(id="b3", role="backup", section_id="3", backup_of="p3a1", status="filled", message_type="time-series", archetype="column-time-series",
    lead_message={"prefix": "BACKUP:", "text": "Absorbing the 2027 wage rise needs about 4% fewer hours per sales dollar, less than the drop since FY2023",
                  "numbers": [{"text": "4%", "data_ref": "hrs_need_g"}], "highlights": ["FY2027 needed"]},
    unit_line="**Labor hours per $1,000 of sales**, hours, FY2023 and FY2025 actual, FY2027 needed to hold labor at 12.1% of sales",
    layout={"variant": "takeaway_sidebar", "sidebar": {
        "kind": "big_number", "header": "Scheduling, not cuts, holds the labor line", "big_number": P("hrs_need_g"),
        "caption": "change in hours per $1,000 of sales needed after the 2027 rise",
        "bullets": [f"**FY2023 to FY2025:** stores cut {abs(V['hrs_g'])*100:.1f}% of hours per sales dollar, more than is needed now",
                    "**Where:** trim in Q4 stores, where extra hours barely lower shrink, not in Q1 and Q2",
                    "**Upper bound:** assumes the 4% rise lifts every wage, not only those at the minimum"]}},
    body={"kind": "chart", "chart_type": "column", "categories": ["FY2023", "FY2025", "FY2027 needed"],
          "series": [{"name": "Hours per $1,000", "points": [P("hrs23"), P("hrs25"), P("hrs_need")]}], "sort": "none",
          "highlight": ["FY2027 needed"], "value_format": "0.00"},
    basis={"header": "How we estimated it", "terms": [
        {"point": P("hrs25"), "caption": "hours per $1,000 of sales, FY2025"},
        {"op": "÷", "point": P("wage_f"), "caption": "wage factor after the 4% rise in 2027"},
        {"op": "=", "point": P("hrs_need"), "caption": "hours that keep labor at 12.1% of sales"}]})

add(id="b4", role="backup", section_id="4", backup_of="p4a1", status="filled", message_type="item", archetype="data-table",
    lead_message={"prefix": "BACKUP:", "text": "Orders nearly tripled and home delivery's share rose while the fee collected per delivery fell"},
    unit_line="**E-commerce operating data**, FY2023–FY2025",
    body={"kind": "table", "table_type": "data", "columns": ["FY2023", "FY2024", "FY2025"], "rows": [
        {"label": "E-commerce share of sales", "cells": [{"point": P("esh23")}, {"point": P("esh24")}, {"point": P("esh25")}]},
        {"label": "Orders, thousands", "cells": [{"point": P("ord23")}, {"point": P("ord24")}, {"point": P("ord25")}]},
        {"label": "Average basket", "cells": [{"point": P("bsk23")}, {"point": P("bsk24")}, {"point": P("bsk25")}]},
        {"label": "Share of orders delivered to the home", "cells": [{"point": P("dsh23")}, {"point": P("dsh24")}, {"point": P("dsh25")}], "highlight": True},
        {"label": "Picking cost per order", "cells": [{"point": P("pick23")}, {"point": P("pick24")}, {"point": P("pick25")}]},
        {"label": "Third-party delivery cost per delivered order", "cells": [{"point": P("dlv23")}, {"point": P("dlv24")}, {"point": P("dlv25")}]},
        {"label": "Fee collected per delivered order", "cells": [{"point": P("fee23")}, {"point": P("fee24")}, {"point": P("fee25")}], "highlight": True}]},
    footnotes=["Delivery is free above $75, with a $4.99 fee below; click-and-collect is free"])

add(id="b5", role="backup", section_id="4", backup_of="p4a2", status="filled", message_type="item", archetype="data-table",
    lead_message={"prefix": "BACKUP:", "text": "Picking, delivery and fees rebuild the $18.1M fulfillment cost, so the order data can be trusted",
                  "numbers": [{"text": "$18.1M", "data_ref": "ef_m"}]},
    unit_line="**E-commerce fulfillment cost rebuilt from order data**, FY2025",
    body={"kind": "table", "table_type": "data", "columns": ["FY2025", "How it is calculated"], "rows": [
        {"label": "Orders, thousands", "cells": [{"point": P("ord25")}, {"text": "Table 5"}]},
        {"label": "Delivered orders, thousands", "cells": [{"point": P("dl25")}, {"text": "Orders × 58% delivered"}]},
        {"label": "Click-and-collect orders, thousands", "cells": [{"point": P("cc25")}, {"text": "Orders − delivered orders"}]},
        {"label": "Picking cost, $M", "cells": [{"point": P("pick_t")}, {"text": "All orders × $7.40"}]},
        {"label": "Third-party delivery cost, $M", "cells": [{"point": P("dlv_t")}, {"text": "Delivered orders × $13.80"}]},
        {"label": "Delivery fees collected, $M", "cells": [{"point": P("fee_t")}, {"text": "Delivered orders × $3.10"}]},
        {"label": "Fulfillment cost, net of fees, $M", "cells": [{"point": P("ef_m")}, {"text": "Picking + delivery − fees; Table 1 reports $18.1M"}], "highlight": True}]})

add(id="b6", role="backup", section_id="5", backup_of="L5", status="filled", message_type="item", archetype="definition-table",
    lead_message={"prefix": "BACKUP:", "text": "The plan rests on eight planning assumptions for the CEO and CFO to confirm", "count_word": 8},
    body={"kind": "table", "table_type": "data", "columns": ["Value", "Basis"], "rows": [
        {"label": "Promotions, share of sales", "cells": [{"point": P("promo23")}, {"text": "FY2023 level"}]},
        {"label": "Private-label gain a year, pp", "cells": [{"point": P("pl_pace")}, {"text": "FY2023–25 pace"}]},
        {"label": "Shrink, Q1 and Q2 stores", "cells": [{"point": P("q3")}, {"text": "Today's Q3 level"}]},
        {"label": "Sales in each store quarter", "cells": [{"point": P("qshare")}, {"text": "Equal quarters"}]},
        {"label": "Online spend new to Harlow", "cells": [{"point": P("inc")}, {"text": "Customer survey"}]},
        {"label": "Contribution per new dollar", "cells": [{"point": P("cr")}, {"text": "Finance estimate"}]},
        {"label": "Sales kept from closed stores", "cells": [{"point": P("transfer")}, {"text": "Past closures"}]},
        {"label": "Store gain from six leases", "cells": [{"point": P("st6_sh")}, {"text": "Even split by store"}]}]},
    footnotes=["All lever sizes use FY2025 prices, volumes and cost rates; the 3.0% target is measured on the sales left after the store exits and the fee change"])

add(id="b7", role="backup", section_id="5", backup_of="p5b", status="filled", message_type="item", archetype="comparison-table",
    lead_message={"prefix": "BACKUP:", "text": "Whether the plan reaches the target depends most on the promotion reset and on absorbing the 2027 wage rise"},
    body={"kind": "table", "table_type": "comparison", "columns": ["What changes", "FY2028 operating margin"], "rows": [
        {"label": "Plan as sized", "cells": [{"text": f"Operating income of about {m(V['oi28'])} on sales of ${V['B']:,.0f}M"}, {"text": f"About {pc(V['m28'], 2)}"}], "note": "Just short of 3.0%"},
        {"label": "Promotions deliver half", "cells": [{"text": f"Promotion gain halved, to about {m(V['g_ph'])}"}, {"text": f"About {pc(V['m_ph'], 2)}"}], "highlight": True, "note": "Largest swing"},
        {"label": "Three stores kept", "cells": [{"text": f"No board vote: {m(V['g_st3'])} of gain lost, sales base larger"}, {"text": f"About {pc(V['m_n3'], 2)}"}], "note": "The vote matters"},
        {"label": "2027 wage rise not absorbed", "cells": [{"text": f"Labor up 4%, about {m(V['wage_c'])} a year"}, {"text": f"About {pc(V['m_w'], 2)}"}], "note": "Scheduling is a must"},
        {"label": "Delivery rate $1 lower", "cells": [{"text": f"Re-tender adds about {m(V['per1'])} a year"}, {"text": f"About {pc(V['m_d1'], 2)}"}], "note": "Clears 3.0%"}],
          "verdict_header": "Reading"})

add(id="end", role="end_page", status="filled")

# ---------------------------------------------------------------- slide ids for data points: first slide that shows them
def refs(o):
    if isinstance(o, dict):
        if "data_ref" in o: yield o["data_ref"]
        for v in o.values(): yield from refs(v)
    elif isinstance(o, list):
        for v in o: yield from refs(v)
first = {}
for s in S:
    for r in refs(s):
        first.setdefault(r, s["id"])
byid = {d["id"]: d for d in DP}
def sid(i, seen=()):
    if i in first: return first[i]
    for d in DP:  # first slide of a number built from this one
        if i in d.get("derived_from", []) and d["id"] not in seen:
            x = sid(d["id"], seen + (i,))
            if x: return x
    return None
for d in DP:
    d["slide_id"] = sid(d["id"]) or "p12"
    if d["id"] in first: d["used_in"] = "shown on slide " + first[d["id"]]
missing = [r for s in S for r in refs(s) if r not in byid]
assert not missing, missing

# ---------------------------------------------------------------- storyline, problem, tree
def tree():
    def leaf(i, code, parent, hyp, imp, inf, analysis, exhibit, verdict, note, ko=False):
        return {"id": i, "code": code, "parent": parent, "hypothesis": hyp, "priority": {"importance": imp, "influence": inf},
                "workplan": {"analysis": analysis, "exhibit": exhibit, "sources": ["Briefing pack"], **({"knock_out": True} if ko else {})},
                "finding": {"verdict": verdict, "note": note}}
    return [
        {"id": "n2", "code": "2", "label": "Gross margin", "hypothesis": "Resetting promotions, growing private label and cutting shrink can win back most of the gross margin lost since FY2023"},
        leaf("n2a", "2a", "n2", "Promotions grew beyond what pays back and can be cut back without losing the traffic they defend", "high", "high",
             "Gross-margin bridge by driver; promotional share and vendor funding over time; break-even of the promotional shift; comps near ValuMart",
             "bar-ranking of drivers; two-panel trend; calculation-bridge; bar of comps", "revised",
             "The 5 pp shift costs 0.70 pp of margin and 38% of events lose money, but stores near ValuMart lost 4.2% of comps, so cuts start elsewhere", True),
        leaf("n2b", "2b", "n2", "Private label can keep gaining share and margin as Harlow's value answer to ValuMart", "medium", "high",
             "Private-label share trend projected at its own pace; margin premium", "column-time-series with basis", "confirmed",
             "12 pp more margin; share up 0.75 pp a year; worth about $3.8M by FY2028"),
        leaf("n2c", "2c", "n2", "Shrink rose because stores are too thinly staffed for receiving and produce rotation", "high", "high",
             "Shrink by labor-intensity quartile; shrink composition; saving if Q1 and Q2 reach Q3", "bar-ranking by quartile; calculation-bridge", "confirmed",
             "Shrink is 3.1% in the least-staffed quarter against 2.3% in the best; fresh waste and receiving errors are 65% of it"),
        {"id": "n3", "code": "3", "label": "Store costs", "hypothesis": "Store costs can fall without cutting the staffing that shoppers and shrink control depend on"},
        leaf("n3a", "3a", "n3", "An 8% cut in store labor hours would close most of the gap to the margin target", "high", "high",
             "Wage, productivity and labor share; shrink response to fewer hours", "KPI tiles; calculation-bridge", "refuted",
             "Labor explains 13% of the decline; the cut could give back up to $10M in shrink and reaches 2.0% margin at best", True),
        leaf("n3b", "3b", "n3", "Exiting the nine stores with negative four-wall EBITDA would lift operating income within the board's constraints", "medium", "high",
             "Four-wall EBITDA, lease dates, sales transfer and exit cost", "KPI tiles; calculation-bridge", "revised",
             "Worth about $6.6M a year; six exits need no vote, the other three need a vote and $7.5M"),
        {"id": "n4", "code": "4", "label": "E-commerce", "hypothesis": "E-commerce can keep its delivery service and stop draining the margin"},
        leaf("n4a", "4a", "n4", "E-commerce is profitable, as the e-commerce team reports", "high", "medium",
             "Full-cost contribution with cannibalization; reconciliation with the team's method", "calculation-bridge; comparison-table", "refuted",
             "Counting delivery and only new sales, it loses about $10.4M a year", True),
        leaf("n4b", "4b", "n4", "Home delivery, not click-and-collect, causes most of the e-commerce loss", "high", "high",
             "Economics per delivered and collected order", "waterfall per order", "confirmed",
             "A delivered order loses about $12.34, a collected one about $1.64"),
        leaf("n4c", "4c", "n4", "Repricing delivery as tested would remove the loss without losing e-commerce customers", "medium", "high",
             "Fee-test results scaled to the chain", "KPI tiles; calculation-bridge", "revised",
             "Gains about $2.8M a year for a 2% sales loss, but e-commerce still loses about $7.6M"),
        {"id": "nx1", "label": "Overhead", "hypothesis": "Cutting other SG&A would restore the operating margin", "cut_reason": "Flat at 4.7% of sales in FY2023–25: not a cause of the decline"},
        {"id": "nx2", "label": "Close delivery", "hypothesis": "Closing home delivery would remove most of the e-commerce loss", "cut_reason": "The family owners want delivery kept in some form"},
        {"id": "nx3", "label": "Match ValuMart", "hypothesis": "Matching ValuMart's prices across the chain would win back traffic", "cut_reason": "Deeper promotions already cost margin without improving price perception"},
        {"id": "nx4", "label": "Raise prices", "hypothesis": "Raising shelf prices across the chain would rebuild gross margin", "cut_reason": "41% of shoppers already see Harlow as more expensive"}]

spec = {
    "spec_version": "0.1", "mode": "deck_deep",
    "meta": {"title": "Reversing the decline in operating margin", "subtitle": "Margin plan for the board meeting, February 2027",
             "company_name": "Harlow Fresh Markets", "audience": "CEO, presenting to the board",
             "purpose": "Decide how to bring operating margin back to at least 3.0% by FY2028 and which actions come first",
             "date": "2026-11-15", "language": "en-US", "confidentiality": "Fictional company; synthetic figures from the briefing pack",
             "theme": "navy", "deck_type": "client_diagnostic"},
    "inputs": [{"id": "in-1", "kind": "pasted_research", "label": "Harlow Fresh Markets briefing pack (evidence/briefing-pack.md)", "content": PACK},
               {"id": "in-2", "kind": "qa_answer", "label": "Planning assumptions chosen on the user's behalf (user unavailable during the build)",
                "content": "Equal sales across the four labor-intensity quartiles; three plan years FY2026–FY2028; half of the promotion reset lands in FY2026; $1 unit for the delivery-rate sensitivity; FY2026 read as the first plan year, as in the brief."}],
    "problem": {
        "statement": "How can Harlow lift its operating margin from 1.0% to at least 3.0% by FY2028, within $25M of one-time cost and with at least $20M of operating income in FY2026, and which actions should come first?",
        "decision_maker": "CEO, asking the board to approve the margin plan",
        "success_criteria": ["Operating margin of at least 3.0% by FY2028", "Operating income of at least $20M in FY2026 (lender covenant)",
                             "At most $25M of one-time cost or capital over FY2026–FY2028",
                             "Delivery kept in some form; no closure of a store with a lease beyond 2027 without a board vote"],
        "deadline": "Board meeting, February 2027",
        "accuracy": "Order of magnitude (about ±20%) on each lever, sized at FY2025 prices and volumes",
        "out_of_scope": ["Closing the delivery service", "New stores, acquisitions and refinancing", "Sales growth from new formats"],
        "one_day_answer": {
            "situation": "Harlow grew sales 6% in two years, but its operating margin fell from 3.4% to 1.0%",
            "complication": "Management blames wages and plans an 8% hours cut, yet promotions, shrink and e-commerce caused most of the fall, and the cut would raise shrink",
            "resolution": "Reset promotions, grow private label, move hours to where shrink is high, reprice delivery and exit weak stores as leases end"}},
    "issue_tree": tree(),
    "sections": [
        {"id": "1", "title": "Where the margin went", "tracker_label": "Diagnosis", "exec_item_id": "1",
         "question": "What caused the fall in operating margin since FY2023, and how large is the gap to close?"},
        {"id": "2", "title": "Gross margin: promotions, private label and shrink", "tracker_label": "Gross margin", "exec_item_id": "2", "tree_node": "n2", "lead_slide": "L2",
         "question": "How much of the lost gross margin can promotions, private label and shrink win back?"},
        {"id": "3", "title": "Store costs: labor hours and the weakest stores", "tracker_label": "Store costs", "exec_item_id": "3", "tree_node": "n3", "lead_slide": "L3",
         "question": "Should Harlow cut store hours, and should it exit its weakest stores?"},
        {"id": "4", "title": "E-commerce: the cost of delivery", "tracker_label": "E-commerce", "exec_item_id": "4", "tree_node": "n4", "lead_slide": "L4",
         "question": "Does e-commerce make money, and how can Harlow keep delivery without draining the margin?"},
        {"id": "5", "title": "How to make it happen", "tracker_label": "Plan", "exec_item_id": "5", "lead_slide": "L5",
         "question": "Which actions come first, and does the plan meet the target, the covenant and the capital limit?"}],
    "storyline": {
        "governing_thought": "Fix promotions, shrink and delivery pricing, not store hours, to get close to 3.0%",
        "exec_summary": [
            {"id": "1", "text": "Gross margin and e-commerce, not wages, explain nearly four-fifths of the fall in operating income",
             "supports": ["p11", "p12", "p13"],
             "sub_points": [{"text": "Operating income fell from $47.9M to $15.3M while sales grew 6%", "slide_id": "p11"},
                            {"text": "3.0% needs about $30M more a year; the FY2026 covenant needs $4.7M more", "slide_id": "p13"}]},
            {"id": "2", "text": f"Fewer promotions, more private label and less shrink would win back about {m(V['gm_gain'], 0)} of gross margin a year",
             "supports": ["L2", "p2a1", "p2a2", "p2a3", "p2a4", "p2b1", "p2c1", "p2c2"],
             "sub_points": [{"text": "38% of FY2025 promotional events lost money", "slide_id": "L2"},
                            {"text": "Shrink is 3.1% of sales in the least-staffed stores, 2.3% in the best", "slide_id": "p2c1"}]},
            {"id": "3", "text": "Store hours should be moved, not cut, and the weakest stores exited as their leases end",
             "supports": ["L3", "p3a1", "p3a2", "p3b1", "p3b2"],
             "sub_points": [{"text": "An 8% hours cut could give back up to $10M of its $14.5M saving", "slide_id": "p3a2"},
                            {"text": "Exiting the nine loss-making stores adds about $6.6M a year", "slide_id": "p3b2"}]},
            {"id": "4", "text": "E-commerce loses about $10M a year; the tested delivery fee cuts that by $2.8M and keeps the service",
             "supports": ["L4", "p4a1", "p4a2", "p4a3", "p4b1", "p4c1", "p4c2"],
             "sub_points": [{"text": "Each home delivery loses about $12, seven times a collected order", "slide_id": "p4b1"},
                            ]},
            {"id": "5", "text": "The plan gets to about 3.0% by FY2028 for $7.5M; its first two actions can clear the FY2026 covenant",
             "supports": ["L5", "p5b", "p5c", "p5d", "p5e", "p5f", "p5g"],
             "sub_points": [{"text": "Started at once, promotions and the fee lift FY2026 to about $23M", "slide_id": "p5d"},
                            {"text": f"About {m(abs(V['short28']))} short of 3.0%; it also needs the 2027 wage rise absorbed", "slide_id": "p5b"}]}],
        "next_steps": [
            {"action": "Start the promotion reset: stop repeating loss-making events, beginning away from ValuMart", "owner": "Chief merchant", "timing": "Now"},
            {"action": "Roll out the tested $7.99 delivery fee and $100 free-delivery threshold to every store", "owner": "E-commerce lead", "timing": "Within a month"},
            {"action": "Re-tender the delivery contract and confirm with the lender which months the FY2026 covenant covers", "owner": "CFO", "timing": "Now, before renewal"},
            {"action": "Replace the 8% hours cut with a move of hours to receiving and produce in Q1 and Q2 stores", "owner": "COO", "timing": "First quarter"},
            {"action": "Let the six leases lapse and put the other three exits to a board vote", "owner": "CEO with the board", "timing": "February 2027 board"}]},
    "slides": S,
    "data_points": DP,
    "sources": [
        {"id": "s1", "kind": "user_provided", "name": "Harlow Fresh Markets briefing pack", "input_id": "in-1"},
        {"id": "s2", "kind": "derived", "name": "Team analysis of the Harlow briefing pack"},
        {"id": "s3", "kind": "user_provided", "name": "Planning assumptions chosen in this review (user unavailable to confirm)", "input_id": "in-2"}],
}
out = ROOT / "work" / "harlow-margin-plan.json"
out.write_text(json.dumps(spec, indent=1, ensure_ascii=False))
print("wrote", out, len(S), "slides", len(DP), "data points")
for k in ("short", "sh_gmef", "sh_lab", "gm_gain", "g_promo", "g_pl", "g_sh", "g_fee", "g_st", "B", "oi28", "m28", "short28", "oi26", "e_loss", "e_after", "giveback", "net_cut", "cut_need", "m_ph", "m_n3", "m_w", "m_d1"):
    print(f"  {k} = {V[k]:.4f}")
