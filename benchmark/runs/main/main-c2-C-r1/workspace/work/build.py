"""Builds the storyline spec for the Harlow Fresh Markets margin deck from the briefing pack.

Every number is a data point: pack figures carry a verbatim excerpt; our calculations carry calc.
Run: python3 work/build.py  ->  work/harlow-margin-plan.json
"""
import json, re, sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PACK = open(os.path.join(ROOT, "evidence", "briefing-pack.md"), encoding="utf-8").read()
PACK_FLAT = re.sub(r"\s+", " ", PACK)

DP = {}          # id -> data point
ORDER = []


def _ids_in(calc):
    toks = re.findall(r"[A-Za-z_][A-Za-z0-9_]*", calc)
    return [t for t in dict.fromkeys(toks) if t in DP]


def _eval(calc):
    env = {k: v["value"] for k, v in DP.items()}
    return eval(calc, {"__builtins__": {}}, env)


def P(id, label, value, unit, excerpt, locator, period=None, **kw):
    """A number from the briefing pack (user material)."""
    assert id not in DP, id
    flat = re.sub(r"\s+", " ", excerpt)
    if flat not in PACK_FLAT:
        sys.exit(f"excerpt for {id} not found verbatim in the pack: {excerpt!r}")
    d = {"id": id, "slide_id": None, "label": label, "value": value, "unit": unit,
         "source_id": kw.pop("source_id", "s1"), "excerpt": excerpt, "locator": "Briefing pack, " + locator}
    if period:
        d["period"] = period
    d.update(kw)
    DP[id] = d; ORDER.append(id)
    return id


def C(id, label, value, unit, locator, period=None):
    """A planning value chosen by the team (CEO not available to confirm)."""
    d = {"id": id, "slide_id": None, "label": label, "value": value, "unit": unit, "source_id": "s3",
         "locator": "Planning choices log, " + locator}
    if period:
        d["period"] = period
    DP[id] = d; ORDER.append(id)
    return id


def D(id, label, unit, calc, formula, period=None, estimate=False, assumptions=None, nd=6, rnd=None, **kw):
    """A number we calculated from other data points."""
    assert id not in DP, id
    v = _eval(calc)
    if rnd is not None:  # display rounding; later calcs use the rounded value, so every calc still recomputes
        v = round(v, rnd)
    d = {"id": id, "slide_id": None, "label": label, "value": round(v, nd), "unit": unit, "source_id": "s2",
         "derived_from": _ids_in(calc), "formula": formula, "calc": calc}
    if period:
        d["period"] = period
    if estimate:
        d["estimate"] = True
        d["assumptions"] = assumptions or []
    d.update(kw)
    DP[id] = d; ORDER.append(id)
    return id


def r(i):
    assert i in DP, i
    return {"data_ref": i}


# ============================================================ data points: the pack
T1 = "Table 1 (income statement, $ millions)"
P("sal23", "Sales", 1420.0, "$M", "| Sales | 1,420.0 | 1,468.0 | 1,503.0 |", T1 + ", Sales, FY2023", "FY2023")
P("sal24", "Sales", 1468.0, "$M", "| Sales | 1,420.0 | 1,468.0 | 1,503.0 |", T1 + ", Sales, FY2024", "FY2024")
P("sal25", "Sales", 1503.0, "$M", "| Sales | 1,420.0 | 1,468.0 | 1,503.0 |", T1 + ", Sales, FY2025", "FY2025")
P("gp23", "Gross profit", 369.8, "$M", "| Gross profit | 369.8 | 376.0 | 376.1 |", T1 + ", Gross profit, FY2023", "FY2023")
P("gp25", "Gross profit", 376.1, "$M", "| Gross profit | 369.8 | 376.0 | 376.1 |", T1 + ", Gross profit, FY2025", "FY2025")
P("lab23", "Store labor cost", 167.6, "$M", "| Store labor | 167.6 | 176.2 | 181.9 |", T1 + ", Store labor, FY2023", "FY2023")
P("lab25", "Store labor cost", 181.9, "$M", "| Store labor | 167.6 | 176.2 | 181.9 |", T1 + ", Store labor, FY2025", "FY2025")
P("occ23", "Occupancy and energy", 82.4, "$M", "| Occupancy and energy | 82.4 | 86.6 | 90.2 |", T1 + ", Occupancy and energy, FY2023", "FY2023")
P("occ25", "Occupancy and energy", 90.2, "$M", "| Occupancy and energy | 82.4 | 86.6 | 90.2 |", T1 + ", Occupancy and energy, FY2025", "FY2025")
ECX = "| E-commerce fulfillment (picking + delivery, net of delivery fees) | 5.2 | 10.9 | 18.1 |"
P("ec23", "E-commerce fulfillment cost, net of delivery fees", 5.2, "$M", ECX, T1 + ", E-commerce fulfillment, FY2023", "FY2023")
P("ec24", "E-commerce fulfillment cost, net of delivery fees", 10.9, "$M", ECX, T1 + ", E-commerce fulfillment, FY2024", "FY2024")
P("ec25", "E-commerce fulfillment cost, net of delivery fees", 18.1, "$M", ECX, T1 + ", E-commerce fulfillment, FY2025", "FY2025")
P("sga23", "Other SG&A", 66.7, "$M", "| Other SG&A | 66.7 | 69.0 | 70.6 |", T1 + ", Other SG&A, FY2023", "FY2023")
P("sga25", "Other SG&A", 70.6, "$M", "| Other SG&A | 66.7 | 69.0 | 70.6 |", T1 + ", Other SG&A, FY2025", "FY2025")
OIX = "| **Operating income** | **47.9** | **33.4** | **15.3** |"
P("oi23", "Operating income", 47.9, "$M", OIX, T1 + ", Operating income, FY2023", "FY2023")
P("oi25", "Operating income", 15.3, "$M", OIX, T1 + ", Operating income, FY2025", "FY2025")
OMX = "| Operating margin | 3.37% | 2.27% | 1.02% |"
P("om23", "Operating margin", 0.0337, "%", OMX, T1 + ", Operating margin, FY2023", "FY2023")
P("om25", "Operating margin", 0.0102, "%", OMX, T1 + ", Operating margin, FY2025", "FY2025")

T2 = "Table 2 (gross-margin drivers)"
PRX = "| Promotional sales, share of sales | 24.0% | 26.2% | 29.0% |"
P("promo23", "Promotional sales, share of sales", 0.24, "%", PRX, T2 + ", FY2023", "FY2023")
P("promo24", "Promotional sales, share of sales", 0.262, "%", PRX, T2 + ", FY2024", "FY2024")
P("promo25", "Promotional sales, share of sales", 0.29, "%", PRX, T2 + ", FY2025", "FY2025")
PLX = "| Private-label sales, share of sales | 17.0% | 17.7% | 18.5% |"
P("pl23", "Private-label sales, share of sales", 0.17, "%", PLX, T2 + ", FY2023", "FY2023")
P("pl24", "Private-label sales, share of sales", 0.177, "%", PLX, T2 + ", FY2024", "FY2024")
P("pl25", "Private-label sales, share of sales", 0.185, "%", PLX, T2 + ", FY2025", "FY2025")
SHX = "| Shrink, % of sales | 2.1% | 2.3% | 2.6% |"
P("shr23", "Shrink, % of sales", 0.021, "%", SHX, T2 + ", FY2023", "FY2023")
P("shr24", "Shrink, % of sales", 0.023, "%", SHX, T2 + ", FY2024", "FY2024")
P("shr25", "Shrink, % of sales", 0.026, "%", SHX, T2 + ", FY2025", "FY2025")
P("promogap", "Gross-margin gap of promotional against regular-price sales", 14, "pp",
  "Promotional sales earn 14 percentage points less gross margin than regular-price sales (unchanged over the period).",
  "section 5, note under Table 2", "FY2023–FY2025")
P("plgap", "Gross-margin advantage of private label over national brands", 12, "pp",
  "Private-label sales earn 12 percentage points more gross margin than national brands (unchanged).",
  "section 5, note under Table 2", "FY2023–FY2025")
P("vf23", "Share of promotional markdowns covered by vendor funding", 0.55, "%",
  "Vendor funding covered 55% of promotional markdowns in FY2023 and 46% in FY2025.", "section 5, note under Table 2", "FY2023")
P("vf25", "Share of promotional markdowns covered by vendor funding", 0.46, "%",
  "Vendor funding covered 55% of promotional markdowns in FY2023 and 46% in FY2025.", "section 5, note under Table 2", "FY2025")
P("loss38", "Share of FY2025 promotional events that lost money after counting extra units", 0.38, "%",
  "A post-event review of FY2025 promotions found that 38% of events lost money after counting the extra units",
  "section 5, note under Table 2", "FY2025")

T3 = "Table 3 (store labor)"
P("wage23", "Average hourly wage incl. benefits", 16.80, "$", "| Average hourly wage incl. benefits | $16.80 | $18.38 |", T3 + ", FY2023", "FY2023")
P("wage25", "Average hourly wage incl. benefits", 18.38, "$", "| Average hourly wage incl. benefits | $16.80 | $18.38 |", T3 + ", FY2025", "FY2025")
P("hrs23", "Labor hours per $1,000 of sales", 7.02, "hours", "| Labor hours per $1,000 of sales | 7.02 | 6.60 |", T3 + ", FY2023", "FY2023")
P("hrs25", "Labor hours per $1,000 of sales", 6.60, "hours", "| Labor hours per $1,000 of sales | 7.02 | 6.60 |", T3 + ", FY2025", "FY2025")

T4 = "Table 4 (shrink by store labor intensity, FY2025)"
P("q1", "Shrink, Q1 stores (fewest labor hours per $ of sales)", 0.031, "%", "| Q1 (fewest labor hours per $ sales) | 3.1% |", T4 + ", Q1", "FY2025")
P("q2", "Shrink, Q2 stores", 0.027, "%", "| Q2 | 2.7% |", T4 + ", Q2", "FY2025")
P("q3", "Shrink, Q3 stores", 0.024, "%", "| Q3 | 2.4% |", T4 + ", Q3", "FY2025")
P("q4", "Shrink, Q4 stores (most labor hours per $ of sales)", 0.023, "%", "| Q4 (most) | 2.3% |", T4 + ", Q4", "FY2025")
P("nq", "Number of store quartiles in the shrink analysis", 4, "quartiles",
  "Table 4. Shrink by store labor intensity, FY2025 (stores ranked by labor hours per $1,000 of sales)", T4 + ", title", "FY2025")
SCX = "Shrink composition FY2025: fresh and produce waste 45%, theft 35%, administrative and receiving errors 20%."
P("waste45", "Fresh and produce waste, share of shrink", 0.45, "%", SCX, "section 6, under Table 4", "FY2025")
P("theft35", "Theft, share of shrink", 0.35, "%", SCX, "section 6, under Table 4", "FY2025")
P("err20", "Administrative and receiving errors, share of shrink", 0.20, "%", SCX, "section 6, under Table 4", "FY2025")

T5 = "Table 5 (e-commerce operating data)"
P("ecs25", "E-commerce share of sales", 0.085, "%", "| E-commerce share of sales | 3.0% | 5.6% | 8.5% |", T5 + ", FY2025", "FY2025")
ORX = "| Orders, thousands | 453 | 865 | 1,331 |"
P("ord23", "E-commerce orders", 453, "k", ORX, T5 + ", FY2023", "FY2023")
P("ord24", "E-commerce orders", 865, "k", ORX, T5 + ", FY2024", "FY2024")
P("ord25", "E-commerce orders", 1331, "k", ORX, T5 + ", FY2025", "FY2025")
P("bask25", "Average e-commerce basket", 96, "$", "| Average basket | $94 | $95 | $96 |", T5 + ", FY2025", "FY2025")
DLX = "| Share of orders delivered to the home (rest: click-and-collect) | 45% | 52% | 58% |"
P("del23", "Share of orders delivered to the home", 0.45, "%", DLX, T5 + ", FY2023", "FY2023")
P("del24", "Share of orders delivered to the home", 0.52, "%", DLX, T5 + ", FY2024", "FY2024")
P("del25", "Share of orders delivered to the home", 0.58, "%", DLX, T5 + ", FY2025", "FY2025")
PKX = "| Picking cost per order (all orders) | $7.20 | $7.30 | $7.40 |"
P("pick23", "Picking cost per order", 7.20, "$", PKX, T5 + ", FY2023", "FY2023")
P("pick24", "Picking cost per order", 7.30, "$", PKX, T5 + ", FY2024", "FY2024")
P("pick25", "Picking cost per order", 7.40, "$", PKX, T5 + ", FY2025", "FY2025")
TPX = "| Third-party delivery cost per delivered order | $12.90 | $13.40 | $13.80 |"
P("tpd23", "Third-party delivery cost per delivered order", 12.90, "$", TPX, T5 + ", FY2023", "FY2023")
P("tpd24", "Third-party delivery cost per delivered order", 13.40, "$", TPX, T5 + ", FY2024", "FY2024")
P("tpd25", "Third-party delivery cost per delivered order", 13.80, "$", TPX, T5 + ", FY2025", "FY2025")
FEX = "| Average delivery fee collected per delivered order | $3.40 | $3.20 | $3.10 |"
P("fee23", "Average delivery fee collected per delivered order", 3.40, "$", FEX, T5 + ", FY2023", "FY2023")
P("fee24", "Average delivery fee collected per delivered order", 3.20, "$", FEX, T5 + ", FY2024", "FY2024")
P("fee25", "Average delivery fee collected per delivered order", 3.10, "$", FEX, T5 + ", FY2025", "FY2025")
P("thr_old", "Free-delivery threshold before the test", 75, "$", "Delivery is free above $75 (a $4.99 fee below).", "section 7, under Table 5")
P("fee_old", "Delivery fee below the threshold before the test", 4.99, "$", "Delivery is free above $75 (a $4.99 fee below).", "section 7, under Table 5")
P("inc70", "Share of online purchases customers would otherwise have bought in a Harlow store", 0.70, "%",
  "Survey of 2,300 e-commerce customers (FY2025): 70% of what they buy online they say they would otherwise have",
  "section 7, survey of 2,300 e-commerce customers", "FY2025")
P("n2300", "E-commerce customer survey sample", 2300, "respondents",
  "Survey of 2,300 e-commerce customers (FY2025)", "section 7", "FY2025")
P("contr20", "Contribution per dollar of sales new to Harlow, before e-commerce fulfillment", 0.20, "%",
  "Finance estimates that a dollar of sales that is genuinely new to Harlow adds about 20 cents of contribution",
  "section 7, finance estimate (20 cents per dollar)")
FTX = "Delivered orders fell 9%, click-and-collect orders rose 14%, total e-commerce sales fell 2%"
P("ft_del", "Fee test: change in delivered orders", -0.09, "%", FTX, "section 7, fee test (4 stores, 10 weeks, late FY2025)", "FY2025")
P("ft_cc", "Fee test: change in click-and-collect orders", 0.14, "%", FTX, "section 7, fee test", "FY2025")
P("ft_sales", "Fee test: change in total e-commerce sales", -0.02, "%", FTX, "section 7, fee test", "FY2025")
P("ft_fee", "Fee test: average fee collected per delivered order", 6.40, "$",
  "average fee collected per delivered order rose to $6.40", "section 7, fee test", "FY2025")
P("ft_newfee", "Fee test: delivery fee below the threshold", 7.99, "$",
  "delivery fee raised to $7.99 and the free-delivery threshold to $100", "section 7, fee test")
P("ft_thr", "Fee test: free-delivery threshold", 100, "$",
  "delivery fee raised to $7.99 and the free-delivery threshold to $100", "section 7, fee test")
P("ft_weeks", "Fee test duration", 10, "weeks", "(4 stores, 10 weeks, late FY2025)", "section 7, fee test", "FY2025")
P("ecclaim", "E-commerce contribution margin reported by the e-commerce team", 0.061, "%",
  "E-commerce is profitable: a contribution margin of 6.1% of e-commerce sales in FY2025.", "section 10, e-commerce team update", "FY2025")

T6 = "Table 6 (the nine weakest stores, FY2025)"
P("ws9", "Stores with negative four-wall EBITDA", 9, "stores", "| Stores with negative four-wall EBITDA | 9 of 58 |", T6, "FY2025")
P("ws58", "Harlow stores", 58, "stores", "| Stores with negative four-wall EBITDA | 9 of 58 |", T6, "FY2025")
P("wsales", "Combined sales of the nine stores", 118.0, "$M", "| Their combined sales | $118.0M |", T6, "FY2025")
P("webitda", "Combined four-wall EBITDA of the nine stores", -3.1, "$M", "| Their combined four-wall EBITDA | −$3.1M |", T6, "FY2025")
P("wlease6", "Of the nine, stores with leases expiring by end of 2027", 6, "stores", "| Leases expiring by end of 2027 | 6 of the 9 |", T6)
P("wexit", "Lease-exit cost for the three stores with longer leases (one-time)", 7.5, "$M",
  "| Estimated lease-exit cost for the other 3 | $7.5M (one-time) |", T6)
P("wmove", "Share of a closed store's sales that moves to a nearby Harlow store (past closures)", 0.25, "%",
  "| Share of their sales expected to move to a nearby Harlow store if closed (past closures) | 25% |", T6)
P("wcontr", "Contribution on sales moved to a receiving store", 0.12, "%",
  "| Contribution on sales moved to a receiving store | 12% |", T6)

P("vm11", "ValuMart stores opened in Harlow trade areas since 2023", 11, "stores",
  "A discount grocer, ValuMart, has opened 11 stores in Harlow trade areas since 2023.", "section 9")
VMX = "had comparable sales of −4.2% in FY2025, against +1.1% for other Harlow stores."
P("vmc", "Comparable sales, Harlow stores within three miles of a new ValuMart", -0.042, "%", VMX, "section 9", "FY2025")
P("oth", "Comparable sales, other Harlow stores", 0.011, "%", VMX, "section 9", "FY2025")
EXX = "41% say Harlow is \"more expensive than other options\" (FY2023: 33%)"
P("exp41", "Shoppers saying Harlow is more expensive than other options", 0.41, "%", EXX, "section 9, customer survey (n = 3,100), FY2025 wave", "FY2025")
P("exp33", "Shoppers saying Harlow is more expensive than other options", 0.33, "%", EXX, "section 9, customer survey", "FY2023")
RSX = "top reasons to shop Harlow are fresh produce (58%) and convenience (44%)."
P("fresh58", "Shoppers naming fresh produce as a top reason to shop Harlow", 0.58, "%", RSX, "section 9, customer survey (n = 3,100)", "FY2025")
P("conv44", "Shoppers naming convenience as a top reason to shop Harlow", 0.44, "%", RSX, "section 9, customer survey", "FY2025")
P("n3100", "Customer survey sample", 3100, "respondents", "Customer survey (n = 3,100)", "section 9")
CTX = "Stores with the deepest promotions in FY2025 grew comparable sales 1.8%, against 0.2% for the rest."
P("deep18", "Comparable sales growth, stores with the deepest promotions", 0.018, "%", CTX, "section 10, category team", "FY2025")
P("rest02", "Comparable sales growth, other stores", 0.002, "%", CTX, "section 10, category team", "FY2025")

P("tgt30", "Target operating margin", 0.03, "%", "operating margin back to at least 3.0% by FY2028.", "section 3", "FY2028")
P("cap25", "Cap on one-time cost or capital for the plan", 25, "$M",
  "at most $25M of one-time cost or capital for the plan over FY2026–FY2028.", "section 3", "FY2026–FY2028")
P("cov20", "Lender covenant: minimum operating income", 20, "$M",
  "a covenant requires operating income of at least $20M in FY2026.", "section 3", "FY2026")
P("labcut8", "Labor-hour cut in management's draft plan", 0.08, "%",
  "labor hours by 8% in FY2026 (they estimate about $14.5M a year of savings)", "section 4", "FY2026")
P("labsave", "Annual saving management estimates for the 8% cut", 14.5, "$M",
  "labor hours by 8% in FY2026 (they estimate about $14.5M a year of savings)", "section 4", "FY2026")
P("minwage", "State minimum-wage rise in 2027", 0.04, "%", "the state minimum wage rises again in 2027 (+4%).", "section 11")
P("tpdrise", "Rise proposed by the delivery provider at the 2026 renewal", 0.03, "%",
  "the provider proposed a 3% rise", "section 11")

# ============================================================ planning choices (s3)
C("labcut4", "Net cut in store labor hours, recommended plan", 0.04, "%", "choice 4 (labor)", "FY2026")
C("pl_years", "Years of private-label growth to FY2028 (FY2026, FY2027, FY2028)", 3, "years", "choice 6 (private label)")

# ============================================================ derived: section 1 diagnosis
D("gm23", "Gross margin, % of sales", "%", "gp23 / sal23", "369.8 ÷ 1,420.0", "FY2023")
D("gm25", "Gross margin, % of sales", "%", "gp25 / sal25", "376.1 ÷ 1,503.0", "FY2025")
D("dgp", "Change in gross margin, share of sales", "%", "gp25 / sal25 - gp23 / sal23", "26.02% − 26.04%", "FY2023–FY2025")
D("dlab", "Effect of store labor on operating margin", "%", "lab23 / sal23 - lab25 / sal25", "11.80% − 12.10%", "FY2023–FY2025")
D("docc", "Effect of occupancy and energy on operating margin", "%", "occ23 / sal23 - occ25 / sal25", "5.80% − 6.00%", "FY2023–FY2025")
D("dec", "Effect of e-commerce fulfillment on operating margin", "%", "ec23 / sal23 - ec25 / sal25", "0.37% − 1.20%", "FY2023–FY2025")
D("dom", "Change in operating margin", "%", "om25 - om23", "1.02% − 3.37%", "FY2023–FY2025")
D("sh_gpec", "Share of the margin decline from gross margin and e-commerce fulfillment", "%", "(dgp + dec) / dom",
  "(−1.02 − 0.84) ÷ −2.35 percentage points", "FY2023–FY2025", rnd=2)
D("sh_lab", "Share of the margin decline from store labor", "%", "dlab / dom", "−0.30 ÷ −2.35 percentage points", "FY2023–FY2025")
D("ecpct23", "E-commerce fulfillment, % of sales", "%", "ec23 / sal23", "5.2 ÷ 1,420.0", "FY2023")
D("ecpct25", "E-commerce fulfillment, % of sales", "%", "ec25 / sal25", "18.1 ÷ 1,503.0", "FY2025")
D("sgapct25", "Other SG&A, % of sales", "%", "sga25 / sal25", "70.6 ÷ 1,503.0", "FY2025")
D("labpct23", "Store labor, % of sales", "%", "lab23 / sal23", "167.6 ÷ 1,420.0", "FY2023")
D("labpct25", "Store labor, % of sales", "%", "lab25 / sal25", "181.9 ÷ 1,503.0", "FY2025")
D("occpct23", "Occupancy and energy, % of sales", "%", "occ23 / sal23", "82.4 ÷ 1,420.0", "FY2023")
D("occpct25", "Occupancy and energy, % of sales", "%", "occ25 / sal25", "90.2 ÷ 1,503.0", "FY2025")
D("sgapct23", "Other SG&A, % of sales", "%", "sga23 / sal23", "66.7 ÷ 1,420.0", "FY2023")
D("sal_g", "Sales growth", "%", "sal25 / sal23 - 1", "1,503.0 ÷ 1,420.0 − 1", "FY2023–FY2025")
D("oi_chg", "Change in operating income", "%", "oi25 / oi23 - 1", "15.3 ÷ 47.9 − 1", "FY2023–FY2025")
# pp versions for the backup table
for a, b, nm in (("gm23", "gm25", "Gross margin"), ("labpct23", "labpct25", "Store labor"), ("occpct23", "occpct25", "Occupancy and energy"),
                 ("ecpct23", "ecpct25", "E-commerce fulfillment"), ("sgapct23", "sgapct25", "Other SG&A"), ("om23", "om25", "Operating margin")):
    D("pp_" + a[:-2], f"{nm}: change in share of sales", "pp", f"({b} - {a}) * 100", "FY2025 share − FY2023 share", "FY2023–FY2025")

# labor decomposition (Table 3)
D("labc23", "Store labor cost per $ of sales, rebuilt from hours and wage", "%", "hrs23 * wage23 / 1000", "7.02 hours × $16.80 ÷ 1,000", "FY2023")
D("labc25", "Store labor cost per $ of sales, rebuilt from hours and wage", "%", "hrs25 * wage25 / 1000", "6.60 hours × $18.38 ÷ 1,000", "FY2025")
D("wage_eff", "Effect of the higher hourly wage on labor cost per $ of sales", "%", "hrs23 * (wage25 - wage23) / 1000",
  "7.02 × ($18.38 − $16.80) ÷ 1,000", "FY2023–FY2025")
D("prod_eff", "Effect of fewer labor hours per $ of sales", "%", "(hrs25 - hrs23) * wage25 / 1000", "(6.60 − 7.02) × $18.38 ÷ 1,000", "FY2023–FY2025")
D("absorb", "Share of the wage effect offset by fewer hours per $ of sales", "%", "(0 - prod_eff) / wage_eff", "0.77 ÷ 1.11 percentage points", "FY2023–FY2025")
D("wage_rise", "Rise in average hourly wage incl. benefits", "%", "wage25 / wage23 - 1", "$18.38 ÷ $16.80 − 1", "FY2023–FY2025")
D("hrs_chg", "Change in labor hours per $1,000 of sales", "%", "hrs25 / hrs23 - 1", "6.60 ÷ 7.02 − 1", "FY2023–FY2025", rnd=2)

# gross-margin bridge (Table 2)
D("gm_promo", "Gross-margin effect of the higher promotional share", "%", "(promo23 - promo25) * promogap / 100", "−5.0 pp × 14 pp", "FY2023–FY2025")
D("gm_pl", "Gross-margin effect of the higher private-label share", "%", "(pl25 - pl23) * plgap / 100", "+1.5 pp × 12 pp", "FY2023–FY2025")
D("gm_shr", "Gross-margin effect of higher shrink", "%", "shr23 - shr25", "2.1% − 2.6%", "FY2023–FY2025")
D("pl_off", "Share of the promotion and shrink losses offset by private label", "%", "gm_pl / (0 - gm_promo - gm_shr)", "0.18 ÷ 1.20 percentage points", "FY2023–FY2025")

# ============================================================ section 2 gross margin
D("promo_chg", "Change in promotional share of sales", "pp", "(promo25 - promo23) * 100", "29.0% − 24.0%", "FY2023–FY2025")
D("vf_chg", "Change in vendor-funded share of markdowns", "pp", "(vf25 - vf23) * 100", "46% − 55%", "FY2023–FY2025")
D("promo_cut", "Cut in promotional share of sales, back to the FY2024 level", "pp", "(promo25 - promo24) * 100", "29.0% − 26.2%", "FY2025 to FY2028")
D("promo_cutshare", "Promotional sales removed, as a share of FY2025 promotional sales", "%", "(promo25 - promo24) / promo25", "2.8 ÷ 29.0", "FY2025")
LEV_PROMO_A = ["Promotional share returns to its FY2024 level of 26.2% of sales (from 29.0%), taken from events that lost money",
               "Customers buy the same items at regular price; the extra units the cut events sold are lost, and the post-event review shows those events lost money even with them",
               "The 14 percentage point margin gap holds; vendor funding is not counted",
               "Sized on FY2025 sales; no growth assumed"]
D("lev_promo", "Gross margin recovered a year by the promotion reset", "$M", "promo_cut * promogap * sal25 / 10000",
  "2.8 pp × 14 pp × $1,503M", "FY2028 run rate", estimate=True, assumptions=LEV_PROMO_A)
D("str_promo", "Extra gross margin if promotional share fell to the FY2023 level", "$M", "(promo24 - promo23) * promogap * sal25 / 100",
  "2.2 pp × 14 pp × $1,503M", "FY2028 run rate", estimate=True,
  assumptions=["Promotional share falls further, from 26.2% to the FY2023 level of 24.0%", "Same margin gap and customer behavior as the base reset"])
D("promo1pp", "Gross margin per percentage point of promotional share", "$M", "0.01 * promogap * sal25 / 100",
  "1 pp × 14 pp × $1,503M", "FY2025", estimate=True,
  assumptions=["Each point of sales moved between promotional and regular price changes gross margin by the 14 percentage point gap"])

D("vmgap", "Comparable-sales gap of stores near ValuMart", "pp", "(vmc - oth) * 100", "−4.2% − 1.1%", "FY2025")
D("exp_chg", "Change in shoppers calling Harlow more expensive", "pp", "(exp41 - exp33) * 100", "41% − 33%", "FY2023–FY2025")
D("cat_gap", "Comparable-sales gap claimed for deep-promotion stores", "pp", "(deep18 - rest02) * 100", "1.8% − 0.2%", "FY2025")

D("q14", "Shrink in Q1 stores as a multiple of Q4 stores", "x", "q1 / q4", "3.1% ÷ 2.3%", "FY2025")
D("waste_err", "Share of shrink from waste and errors", "%", "waste45 + err20", "45% + 20%", "FY2025")
D("shr_q12", "Combined excess shrink of Q1 and Q2 stores over the Q3 rate", "pp", "(q1 - q3 + q2 - q3) * 100", "(3.1% − 2.4%) + (2.7% − 2.4%)", "FY2025")
LEV_SHR_A = ["Q1 and Q2 stores bring shrink down to the Q3 rate of 2.4% by restoring produce rotation and receiving checks",
             "The four quartiles carry equal sales, as their simple average (2.6%) matches the chain rate",
             "Waste (45%) and receiving and administrative errors (20%) are the parts that labor fixes; theft (35%) is not targeted",
             "Hours for Q1–Q2 come from Q3–Q4 stores inside the net 4% labor cut (3a)"]
D("lev_shr", "Gross margin recovered a year by the shrink program", "$M", "shr_q12 / nq * sal25 / 100",
  "1.0 pp ÷ 4 quartiles × $1,503M", "FY2028 run rate", estimate=True, assumptions=LEV_SHR_A)
D("shr_avg_ex", "Chain-wide shrink reduction from the program", "pp", "shr_q12 / nq", "1.0 pp ÷ 4", "FY2028")
D("str_shr", "Extra gross margin if chain shrink returned to the FY2023 rate", "$M", "(shr25 - shr23) * sal25 - lev_shr",
  "(2.6% − 2.1%) × $1,503M − $3.8M", "FY2028 run rate", estimate=True,
  assumptions=["Chain shrink returns to its FY2023 rate of 2.1%, beyond the Q3 target for Q1–Q2 stores", "Needs the waste and error fixes to reach Q3 and Q4 stores too"])
D("q12avg", "Average shrink of Q1 and Q2 stores", "%", "(q1 + q2) / 2", "(3.1% + 2.7%) ÷ 2", "FY2025")

D("pl_pace", "Yearly gain in private-label share, FY2024 to FY2025", "pp", "(pl25 - pl24) * 100", "18.5% − 17.7%", "FY2024–FY2025")
D("pl_add", "Private-label share added FY2026–FY2028 at the FY2025 pace", "pp", "pl_pace * pl_years", "0.8 pp × 3 years", "FY2026–FY2028",
  estimate=True, assumptions=["Private-label share keeps growing at its FY2025 pace of 0.8 percentage points a year for three years"])
D("pl28", "Private-label share of sales in FY2028 at the FY2025 pace", "%", "pl25 + pl_add / 100", "18.5% + 2.4 pp", "FY2028")
D("lev_pl", "Gross margin added a year by private-label growth", "$M", "(pl28 - pl25) * plgap * sal25 / 100", "2.4 pp × 12 pp × $1,503M",
  "FY2028 run rate", estimate=True,
  assumptions=["Private-label share rises by 2.4 percentage points by FY2028 at the FY2025 pace", "The 12 percentage point margin advantage holds",
               "Sized on FY2025 sales; no growth assumed"])
D("gm_total", "Gross margin recovered a year by promotions, shrink and private label", "$M", "lev_promo + lev_shr + lev_pl", "$5.9M + $3.8M + $4.3M", "FY2028 run rate", rnd=1)

# ============================================================ section 3 e-commerce
D("ecsal25", "E-commerce sales", "$M", "ecs25 * sal25", "8.5% × $1,503M", "FY2025")
D("delord25", "Delivered orders", "k", "ord25 * del25", "1,331k × 58%", "FY2025", rnd=0)
D("ccord25", "Click-and-collect orders", "k", "ord25 * (1 - del25)", "1,331k × 42%", "FY2025")
D("pickc25", "Picking cost", "$M", "pick25 * ord25 / 1000", "$7.40 × 1,331k", "FY2025")
D("tpdc25", "Third-party delivery cost", "$M", "tpd25 * delord25 / 1000", "$13.80 × 772k", "FY2025")
D("feer25", "Delivery fees collected", "$M", "fee25 * delord25 / 1000", "$3.10 × 772k", "FY2025")
D("newshare", "Share of online sales that is new to Harlow", "%", "1 - inc70", "1 − 70%", "FY2025")
D("ec_contr", "Contribution from online sales that are new to Harlow, before fulfillment", "$M", "ecsal25 * newshare * contr20",
  "$127.8M × 30% × 20 cents", "FY2025")
D("ec_netpct", "E-commerce result, % of e-commerce sales, all fulfillment and only new sales counted", "%", "(ec_contr - ec25) / ecsal25",
  "($7.7M − $18.1M) ÷ $127.8M", "FY2025")
D("ec_net", "E-commerce result, all fulfillment and only new sales counted", "$M", "ec_netpct * ecsal25", "−8.2% × $127.8M", "FY2025")
D("st_del", "Third-party delivery net of fees, % of e-commerce sales", "%", "(feer25 - tpdc25) / ecsal25", "($2.4M − $10.7M) ÷ $127.8M", "FY2025")
D("st_inc", "Effect of counting only new sales (and other method differences), % of e-commerce sales", "%", "ec_netpct - ecclaim - st_del",
  "−8.2% − 6.1% + 6.5%", "FY2025")
D("ec_cover", "Share of fulfillment cost covered by contribution from new sales", "%", "ec_contr / ec25", "$7.7M ÷ $18.1M", "FY2025")

D("ord_contr", "Contribution per order from new sales", "$", "bask25 * newshare * contr20", "$96 × 30% × 20 cents", "FY2025")
D("fee_neg", "Delivery fee per delivered order (as an offset to cost)", "$", "0 - fee25", "−$3.10", "FY2025")
D("contr_neg", "Contribution per order from new sales (as an offset to cost)", "$", "0 - ord_contr", "−$5.76", "FY2025")
D("del_loss", "Result per delivered order", "$", "ord_contr - pick25 - tpd25 + fee25", "$5.76 − $7.40 − $13.80 + $3.10", "FY2025")
D("cc_loss", "Result per click-and-collect order", "$", "ord_contr - pick25", "$5.76 − $7.40", "FY2025")
D("del_loss_pos", "Loss per delivered order", "$", "0 - del_loss", "−(−$12.34)", "FY2025")
D("del_share", "Share of the e-commerce loss from delivered orders", "%", "del_loss_pos * delord25 / 1000 / (0 - ec_net)", "$12.34 × 772k ÷ $10.4M", "FY2025")
D("gap23", "Courier cost less fee per delivered order", "$", "tpd23 - fee23", "$12.90 − $3.40", "FY2023")
D("gap25", "Courier cost less fee per delivered order", "$", "tpd25 - fee25", "$13.80 − $3.10", "FY2025")
D("delord23", "Delivered orders", "k", "ord23 * del23", "453k × 45%", "FY2023")
D("delord24", "Delivered orders", "k", "ord24 * del24", "865k × 52%", "FY2024")
for y in ("23", "24"):
    D(f"pickc{y}", "Picking cost", "$M", f"pick{y} * ord{y} / 1000", "picking cost per order × orders", "FY20" + y)
    D(f"tpdc{y}", "Third-party delivery cost", "$M", f"tpd{y} * delord{y} / 1000", "courier cost per delivered order × delivered orders", "FY20" + y, rnd=1 if y == "24" else None)
    D(f"feer{y}", "Delivery fees collected", "$M", f"fee{y} * delord{y} / 1000", "fee per delivered order × delivered orders", "FY20" + y)
for y in ("23", "24", "25"):
    D(f"ful{y}", "E-commerce fulfillment rebuilt from order data", "$M", f"pickc{y} + tpdc{y} - feer{y}", "picking + courier − fees", "FY20" + y)

D("ft_kept", "Share of e-commerce sales kept in the fee test", "%", "1 + ft_sales", "1 − 2%", "FY2025")
D("fee_ratio", "Fee per delivered order in the test as a multiple of FY2025", "x", "ft_fee / fee25", "$6.40 ÷ $3.10", "FY2025")
FT_A = ["Delivered orders fall 9% and click-and-collect orders rise 14% chain-wide, as in the 4-store, 10-week test",
        "The average fee per delivered order reaches the test's $6.40; picking and courier costs per order stay at FY2025 levels",
        "Sales lost (2%) are new to Harlow in the same 30% share as all online sales",
        "The courier's proposed 3% rise is excluded; it is handled at the 2026 renewal (2c)"]
D("new_del", "Delivered orders at the tested fee, FY2025 volumes", "k", "delord25 * (1 + ft_del)", "772k × (1 − 9%)", "FY2028 run rate", estimate=True, assumptions=FT_A)
D("new_cc", "Click-and-collect orders at the tested fee, FY2025 volumes", "k", "ccord25 * (1 + ft_cc)", "559k × (1 + 14%)", "FY2028 run rate", estimate=True, assumptions=FT_A)
D("new_ful", "E-commerce fulfillment cost at the tested fee and threshold", "$M",
  "(pick25 * (new_del + new_cc) + tpd25 * new_del - ft_fee * new_del) / 1000",
  "$7.40 × 1,340k orders + $13.80 × 702k − $6.40 × 702k", "FY2028 run rate", estimate=True, assumptions=FT_A)
D("lost_contr", "Contribution lost on e-commerce sales that leave after the fee change", "$M", "(0 - ft_sales) * ecsal25 * newshare * contr20",
  "2% × $127.8M × 30% × 20 cents", "FY2028 run rate", estimate=True, assumptions=FT_A)
D("lev_ec", "Operating income added a year by repricing delivery", "$M", "ec25 - new_ful - lost_contr", "$18.1M − $15.1M − $0.15M",
  "FY2028 run rate", estimate=True, assumptions=FT_A)
D("del_loss_t", "Result per delivered order at the tested fee", "$", "ord_contr - pick25 - tpd25 + ft_fee", "$5.76 − $7.40 − $13.80 + $6.40", "FY2025")
D("be_fee", "Fee per delivered order at which a delivery breaks even", "$", "pick25 + tpd25 - ord_contr", "$7.40 + $13.80 − $5.76", "FY2025")
D("tpd_rise", "Cost a year of the courier's proposed 3% rise", "$M", "tpd25 * tpdrise * new_del / 1000", "$13.80 × 3% × 702k delivered orders", "FY2026")

# ============================================================ section 4 store costs
D("shr_chg", "Change in shrink, share of sales", "pp", "(shr25 - shr23) * 100", "2.6% − 2.1%", "FY2023–FY2025")
D("q1x", "Q1 shrink rate above the chain average", "pp", "(q1 - shr25) * 100", "3.1% − 2.6%", "FY2025")
SR_A = ["Scenario: an across-the-board 8% cut moves the chain's shrink to today's Q1 rate of 3.1%, from 2.6%",
        "Q1 stores are the ones that already run with the fewest hours per $ of sales",
        "Lost sales from longer waits and stock-outs are not counted"]
D("shr_risk", "Shrink cost a year if the chain ran at the Q1 rate (scenario)", "$M", "0 - q1x * sal25 / 100", "−0.5 pp × $1,503M",
  "FY2026 scenario", estimate=True, assumptions=SR_A)
D("lab_net", "Net saving of the 8% cut after the shrink scenario", "$M", "labsave + shr_risk", "$14.5M − $7.5M", "FY2026 scenario")
D("giveback", "Share of the 8% cut's saving lost to shrink in the scenario", "%", "(0 - shr_risk) / labsave", "$7.5M ÷ $14.5M", "FY2026 scenario")
D("q34", "Shrink difference between Q3 and Q4 stores", "pp", "(q3 - q4) * 100", "2.4% − 2.3%", "FY2025")
D("lev_lab", "Saving a year from the net 4% targeted labor cut", "$M", "labcut4 * lab25", "4% × $181.9M", "FY2028 run rate", estimate=True,
  assumptions=["Hours fall by a net 4%: cuts in the Q3–Q4 stores, part of them moved to rotation and receiving in Q1–Q2 stores",
               "Moved hours cost the same per hour as the hours cut", "Sized on FY2025 store labor; no wage change counted"])
D("hrs_tgt", "Labor hours per $1,000 of sales after the net 4% cut", "hours", "hrs25 * (1 - labcut4)", "6.60 × (1 − 4%)", "FY2028")

D("wshare", "The nine stores' share of chain sales", "%", "wsales / sal25", "$118.0M ÷ $1,503M", "FY2025")
D("w_trs", "Sales that move to nearby Harlow stores if all nine close", "$M", "wsales * wmove", "$118.0M × 25%", "FY2028 run rate",
  estimate=True, assumptions=["25% of the nine stores' sales move to nearby Harlow stores, as in past closures"])
D("w_trans", "Contribution from sales moved to receiving stores", "$M", "w_trs * wcontr", "$29.5M × 12%", "FY2028 run rate", estimate=True,
  assumptions=["Moved sales earn the 12% contribution seen at receiving stores"])
D("w_gain_eb", "Four-wall loss removed by closing the nine stores", "$M", "0 - webitda", "−(−$3.1M)", "FY2025")
W_A = ["25% of the nine stores' sales move to nearby Harlow stores, as in past closures", "Moved sales earn 12% contribution at the receiving store",
       "Four-wall EBITDA is the store's own result; head-office cost and depreciation are not counted",
       "The nine stores' staff, rent and energy leave with them"]
D("w_gain", "Operating income added a year by closing all nine stores", "$M", "w_gain_eb + w_trans", "$3.1M + $3.5M", "FY2028 run rate",
  estimate=True, assumptions=W_A)
D("w_gain6", "Operating income added a year by closing the six stores at lease end", "$M", "w_gain * wlease6 / ws9", "$6.6M × 6 ÷ 9",
  "FY2028 run rate", estimate=True, assumptions=W_A + ["The six and the three stores are of average size for the nine"])
D("w_gain3", "Operating income added a year by closing the three long-lease stores", "$M", "w_gain * (ws9 - wlease6) / ws9", "$6.6M × 3 ÷ 9",
  "FY2028 run rate", estimate=True, assumptions=W_A + ["The six and the three stores are of average size for the nine"])
D("payback", "Payback of the lease-exit cost for the three long-lease stores", "years", "wexit / w_gain3", "$7.5M ÷ $2.2M a year", "FY2027–FY2030")
D("cap_share", "Lease-exit cost as a share of the one-time cost cap", "%", "wexit / cap25", "$7.5M ÷ $25M", "FY2026–FY2028")

# ============================================================ section 5 plan
D("b_promo", "Promotion reset in the FY2028 bridge (sized on 1a)", "$M", "lev_promo", "from 1a", "FY2028")
D("b_lab", "Targeted labor in the FY2028 bridge (sized on 3a)", "$M", "lev_lab", "from 3a", "FY2028")
D("b_ec", "Delivery repricing in the FY2028 bridge (sized on 2c)", "$M", "lev_ec", "from 2c", "FY2028")
D("b_shr", "Shrink program in the FY2028 bridge (sized on 1c)", "$M", "lev_shr", "from 1c", "FY2028")
D("b_pl", "Private label in the FY2028 bridge (sized on 1d)", "$M", "lev_pl", "from 1d", "FY2028")
D("lost_sales", "Sales lost with the nine stores, net of transfers", "$M", "wsales * (1 - wmove)", "$118.0M × 75%", "FY2028")
D("keep", "FY2028 sales base as a share of FY2025 sales", "%", "(sal25 - lost_sales) / sal25", "($1,503M − $88.5M) ÷ $1,503M", "FY2028")
D("overlap", "Store-level levers lost with the closed stores", "$M", "(b_promo + b_lab + b_shr + b_pl) * lost_sales / sal25",
  "($5.9M + $7.3M + $3.8M + $4.3M) × $88.5M ÷ $1,503M", "FY2028")
D("st_net", "Store exits in the FY2028 bridge, net of the other levers' share in those stores", "$M", "w_gain - overlap", "$6.6M − $1.3M", "FY2028")
D("lev_sum", "Operating income added a year by the six moves", "$M", "b_promo + b_lab + b_ec + b_shr + b_pl + st_net", "sum of the six moves", "FY2028")
D("oi28", "FY2028 operating income, plan", "$M", "oi25 + lev_sum", "$15.3M + $29.5M", "FY2028")
D("sal28", "FY2028 sales base: FY2025 sales less the nine stores' sales that do not transfer", "$M", "sal25 - lost_sales", "$1,503M − $88.5M", "FY2028")
D("pm28", "FY2028 operating margin, plan", "%", "oi28 / sal28", "$44.8M ÷ $1,414.5M", "FY2028")
D("tgt_oi", "Operating income a 3.0% margin needs on the FY2028 sales base", "$M", "tgt30 * sal28", "3.0% × $1,414.5M", "FY2028")
D("headroom", "Plan operating income above the 3.0% requirement", "$M", "oi28 - tgt_oi", "$44.8M − $42.4M", "FY2028")
D("quick", "First-wave moves: promotions, targeted labor and delivery repricing", "$M", "b_promo + b_lab + b_ec", "$5.9M + $7.3M + $2.8M", "run rate", rnd=1)
D("quick_sh", "First wave as a share of the plan's added operating income", "%", "quick / lev_sum", "$16.0M ÷ $29.5M", "FY2028")
D("cov_gap", "Operating income needed above FY2025 to meet the covenant", "$M", "cov20 - oi25", "$20M − $15.3M", "FY2026")
D("cov_share", "Share of the first wave's run rate needed in FY2026 to meet the covenant", "%", "cov_gap / quick", "$4.7M ÷ $16.0M", "FY2026")
D("wage_risk", "Cost a year if every hourly rate rose by the 2027 minimum-wage step", "$M", "minwage * lab25", "4% × $181.9M", "FY2027",
  estimate=True, assumptions=["Upper bound: every hourly rate rises 4%, not only those at the minimum wage", "Sized on FY2025 store labor"])
D("stretch", "Stretch levers: promotions to the FY2023 share and shrink to the FY2023 rate", "$M", "str_promo + str_shr", "$4.6M + $3.8M", "FY2028")
D("oi_w", "FY2028 operating income if the wage rise lands in full", "$M", "oi28 - wage_risk * keep", "$44.8M − $7.3M × 94%", "FY2028")
D("pm_w", "FY2028 margin if the wage rise lands in full", "%", "oi_w / sal28", "$37.9M ÷ $1,414.5M", "FY2028")
D("oi_ws", "FY2028 operating income with the wage rise and both stretch levers", "$M", "oi_w + stretch * keep", "$37.9M + $8.4M × 94%", "FY2028")
D("pm_ws", "FY2028 margin with the wage rise and both stretch levers", "%", "oi_ws / sal28", "$45.8M ÷ $1,414.5M", "FY2028")
D("lost6", "Sales lost with the six lease-end stores, net of transfers", "$M", "lost_sales * wlease6 / ws9", "$88.5M × 6 ÷ 9", "FY2028")
D("oi_6", "FY2028 operating income if only the six lease-end stores close", "$M",
  "oi28 - st_net + w_gain6 - (b_promo + b_lab + b_shr + b_pl) * lost6 / sal25", "plan − store step + six-store gain − their lever overlap", "FY2028")
D("pm_6", "FY2028 margin if only the six lease-end stores close", "%", "oi_6 / (sal25 - lost6)", "÷ ($1,503M − $59.0M)", "FY2028")
D("oi_p", "FY2028 operating income if promotional share ends 1 percentage point above plan", "$M", "oi28 - promo1pp * keep", "$44.8M − $2.1M × 94%", "FY2028")
D("pm_p", "FY2028 margin if promotional share ends 1 percentage point above plan", "%", "oi_p / sal28", "$42.8M ÷ $1,414.5M", "FY2028")
D("st_total", "Store-cost moves: targeted labor and store exits", "$M", "b_lab + w_gain", "$7.3M + $6.6M", "FY2028 run rate")
D("gm_total_b", "Gross-margin moves in the FY2028 bridge", "$M", "b_promo + b_shr + b_pl", "$5.9M + $3.8M + $4.3M", "FY2028")

# ============================================================ slides
S = []


def nav(id, role, section=None):
    s = {"id": id, "role": role, "status": "filled"}
    if role == "agenda_tracker":
        s.update({"archetype": "agenda-tracker", "message_type": "navigation"})
    if section:
        s["section_id"] = section
    S.append(s)


def slide(**kw):
    s = {"role": "content", "status": "filled"}
    s.update(kw)
    S.append(s)
    return s


S.append({"id": "c", "role": "cover", "status": "filled"})
S.append({"id": "q", "role": "problem_statement", "status": "filled"})
S.append({"id": "es", "role": "exec_summary", "status": "filled", "archetype": "exec-summary", "message_type": "navigation"})

# ---------------------------------------------------------------- section 1: diagnosis
nav("d1", "agenda_tracker", "1")
slide(id="s1a", section_id="1",
      lead_message={"text": "Gross margin and e-commerce fulfillment explain nearly four-fifths of the margin decline, store labor only an eighth",
                    "highlights": ["Gross margin", "E-commerce fulfillment"], "clauses": 1},
      message_type="component", archetype="waterfall-bridge", rationale="What adds up to the change -> waterfall",
      unit_line="**Operating margin**, % of sales, FY2023 to FY2025; steps are each cost line's change in share of sales",
      layout={"variant": "takeaway_sidebar", "sidebar": {
          "kind": "big_number", "big_number": r("sh_gpec"),
          "caption": "of the margin decline comes from gross margin and e-commerce fulfillment",
          "bullets": ["**Gross margin:** the largest step, driven by deeper promotions and higher shrink (next pages)",
                      "**E-commerce fulfillment:** rose from 0.4% to 1.2% of sales as orders tripled and more went to the home",
                      "**Store labor:** a small step despite a 9.4% rise in hourly pay, because hours per sale fell"]}},
      body={"kind": "chart", "chart_type": "waterfall",
            "categories": ["FY2023 margin", "Gross margin", "Store labor", "Occupancy and energy", "E-commerce fulfillment", "FY2025 margin"],
            "series": [{"name": "Operating margin", "points": [r("om23"), r("dgp"), r("dlab"), r("docc"), r("dec"), r("om25")]}],
            "sort": "none", "highlight": ["Gross margin", "E-commerce fulfillment"], "value_format": "0.00%"},
      footnotes=["Each step is the change in that line's share of sales, FY2023 to FY2025 (Table 1). Other SG&A held at 4.7% of sales and is left out; steps sum to the margin change within rounding"])

slide(id="s1b", section_id="1",
      lead_message={"text": "Wage inflation is real, but fewer labor hours per sale absorbed about 70% of it",
                    "numbers": [{"text": "70%", "data_ref": "absorb"}], "highlights": ["Fewer hours per sale"], "clauses": 1},
      message_type="component", archetype="waterfall-bridge", rationale="Labor cost per sale splits into a wage and an hours effect -> waterfall",
      unit_line="**Store labor cost**, % of sales, FY2023 to FY2025, rebuilt from labor hours and the hourly wage",
      layout={"variant": "takeaway_sidebar", "sidebar": {
          "kind": "big_number", "big_number": r("absorb"),
          "caption": "of the wage effect was offset by scheduling fewer hours per sale",
          "bullets": ["**Hourly pay:** up 9.4% in two years, as management says",
                      "**Hours per sale:** down 6% in the same two years, while shrink rose (1c)"],
          "implication": "Labor is the smallest big driver; more across-the-board hour cuts target the wrong cause"}},
      body={"kind": "chart", "chart_type": "waterfall",
            "categories": ["FY2023 labor cost", "Higher hourly wage", "Fewer hours per sale", "FY2025 labor cost"],
            "series": [{"name": "Store labor cost", "points": [r("labc23"), r("wage_eff"), r("prod_eff"), r("labc25")]}],
            "sort": "none", "highlight": ["Fewer hours per sale"], "value_format": "0.0%"},
      footnotes=["Labor cost per sale = labor hours per $1,000 of sales × average hourly wage incl. benefits (Table 3). Wage effect at FY2023 hours; hours effect at FY2025 wage",
                 "Rebuilt shares differ from the income statement (11.8% and 12.1%) by up to 0.03 percentage points through rounding"])

slide(id="s1c", section_id="1",
      lead_message={"text": "Deeper promotions and higher shrink caused the fall in gross margin; private label offset only 15% of it",
                    "numbers": [{"text": "15%", "data_ref": "pl_off"}], "highlights": ["More promotional sales", "Higher shrink"], "clauses": 1},
      message_type="component", archetype="waterfall-bridge", rationale="What adds up to the gross-margin change -> waterfall",
      unit_line="**Gross margin**, % of sales, FY2023 to FY2025; steps are mix and shrink effects in share of sales",
      layout={"variant": "takeaway_sidebar", "sidebar": {
          "kind": "big_number", "big_number": r("pl_off"),
          "caption": "of the promotion and shrink losses was won back by private-label growth",
          "bullets": ["**Promotions:** rose from 24% to 29% of sales, each sale earning 14 percentage points less margin",
                      "**Shrink:** up from 2.1% to 2.6% of sales; fresh and produce waste is 45% of it",
                      "**Private label:** grew from 17% to 18.5% of sales at 12 percentage points more margin, too slowly to offset"]}},
      body={"kind": "chart", "chart_type": "waterfall",
            "categories": ["FY2023 gross margin", "More promotional sales", "More private label", "Higher shrink", "FY2025 gross margin"],
            "series": [{"name": "Gross margin", "points": [r("gm23"), r("gm_promo"), r("gm_pl"), r("gm_shr"), r("gm25")]}],
            "sort": "none", "highlight": ["More promotional sales", "Higher shrink"], "value_format": "0.00%"},
      footnotes=["Mix effects = change in share of sales × margin gap (Table 2 notes); the effects sum to the reported change within rounding"])

# ---------------------------------------------------------------- section 2: gross margin
nav("d2", "agenda_tracker", "2")
slide(id="L2", section_id="2",
      lead_message={"text": "Gross margin can win back about $14M a year from fewer money-losing promotions, less shrink and more private label",
                    "numbers": [{"text": "$14M", "data_ref": "gm_total"}]},
      message_type="argument", archetype="numbered-levers", unit_line="**Status of each finding**, FY2025 data",
      body={"kind": "levers", "headers": ["Finding", "Evidence"], "total": r("gm_total"),
            "items": [{"code": "1a", "text": "Promotions grew past paying back; the FY2024 share adds about $5.9M a year",
                       "point": r("loss38"), "metric": "of FY2025 promotional events lost money"},
                      {"code": "1b", "text": "Deeper promotions have not held off ValuMart; shoppers come for fresh and convenience",
                       "point": r("vmc"), "metric": "comparable sales near a new ValuMart"},
                      {"code": "1c", "text": "Shrink is highest where hours are thinnest; fixing the weakest half adds about $3.8M",
                       "point": r("q1"), "metric": "shrink in the least-staffed stores"},
                      {"code": "1d", "text": "Private label keeps its margin edge; holding its pace adds about $4.3M by FY2028",
                       "point": r("plgap"), "metric": "more margin than national brands"}]})

slide(id="1a1", section_id="2", tree_node="n1a",
      lead_message={"text": "Promotions grew to 29% of sales while vendors funded a shrinking share of their markdowns",
                    "numbers": [{"text": "29%", "data_ref": "promo25"}], "clauses": 2},
      message_type="time-series", archetype="multi-chart-panel", rationale="Two clauses, one claim -> two panels, no arrow",
      layout={"variant": "split_2"},
      body={"kind": "panels", "panels": [
          {"header": "Promotional sales took a larger share every year", "unit_line": "**Promotional sales**, % of sales",
           "delta": r("promo_chg"),
           "body": {"kind": "chart", "chart_type": "column", "categories": ["FY2023", "FY2024", "FY2025"],
                    "series": [{"name": "Promotional share", "points": [r("promo23"), r("promo24"), r("promo25")]}],
                    "sort": "none", "highlight": [], "value_format": "0.0%"}},
          {"header": "Vendors now fund less than half of the markdowns", "unit_line": "**Vendor funding**, % of promotional markdowns",
           "delta": r("vf_chg"),
           "body": {"kind": "chart", "chart_type": "column", "categories": ["FY2023", "FY2025"],
                    "series": [{"name": "Vendor-funded share", "points": [r("vf23"), r("vf25")]}],
                    "sort": "none", "highlight": [], "value_format": "0%"}}]},
      so_what="Each promotion now costs Harlow more of its own margin: vendor funding is the first negotiation",
      so_what_style="bar",
      footnotes=["Vendor funding reported for FY2023 and FY2025 only; markdown dollars are not in the briefing pack, so the funding lever is not sized and counts as upside"])

slide(id="1a2", section_id="2", tree_node="n1a",
      lead_message={"text": "Cutting promotions back to their FY2024 share of sales would recover about $5.9M of gross margin a year",
                    "numbers": [{"text": "$5.9M", "data_ref": "lev_promo"}]},
      message_type="component", archetype="calculation-bridge",
      unit_line="**Gross margin recovered by the promotion reset**, $ millions a year, on FY2025 sales, team estimate",
      body={"kind": "equation", "terms": [
          {"point": r("promo_cut"), "caption": "of sales moved back to regular price: promotional share from 29.0% to the FY2024 level of 26.2%"},
          {"op": "×", "point": r("promogap"), "caption": "more gross margin on each dollar sold at regular price (pack)"},
          {"op": "×", "point": r("sal25"), "caption": "FY2025 sales"},
          {"op": "=", "point": r("lev_promo"), "caption": "gross margin recovered a year"}],
          "assumptions_header": "The cut comes from events that already lose money",
          "assumptions": ["The cut is about a tenth of promotional sales (9.7%), while 38% of FY2025 events lost money even after their extra units",
                          "Shoppers keep buying the items at regular price; the extra units the cut events sold are lost, which the review shows does not lower profit",
                          "Promotions stay in trade areas within three miles of a ValuMart; the cut is taken elsewhere",
                          "Vendor funding, down from 55% to 46% of markdowns, is not counted and is upside"]})

slide(id="1b1", section_id="2", tree_node="n1b",
      lead_message={"text": "Deeper promotions have not held off ValuMart: nearby stores still lost sales and more shoppers call Harlow expensive",
                    "clauses": 2},
      message_type="item", archetype="multi-chart-panel", rationale="Two clauses, one claim -> two panels, no arrow",
      layout={"variant": "split_2"},
      body={"kind": "panels", "panels": [
          {"header": "Stores near a new ValuMart still lost comparable sales",
           "unit_line": "**Comparable sales growth**, %, FY2025", "delta": r("vmgap"),
           "body": {"kind": "chart", "chart_type": "column", "categories": ["Within three miles of a new ValuMart", "Other Harlow stores"],
                    "series": [{"name": "Comparable sales", "points": [r("vmc"), r("oth")]}],
                    "sort": "none", "highlight": [], "value_format": "0.0%"}},
          {"header": "More shoppers now call Harlow expensive",
           "unit_line": "**Shoppers saying Harlow is more expensive than other options**, % of respondents", "delta": r("exp_chg"),
           "body": {"kind": "chart", "chart_type": "column", "categories": ["FY2023", "FY2025"],
                    "series": [{"name": "More expensive", "points": [r("exp33"), r("exp41")]}],
                    "sort": "none", "highlight": [], "value_format": "0%"}}]},
      so_what="Price promotions are not winning against a discounter; shoppers name fresh produce and convenience as their reasons to choose Harlow",
      so_what_style="line",
      footnotes=["ValuMart has opened 11 stores in Harlow trade areas since 2023; category managers raised promotional depth in FY2024–FY2025 to defend traffic against it",
                 "Customer survey, n = 3,100, FY2025 with an FY2023 comparison; top reasons to shop Harlow: fresh produce 58%, convenience 44%"])

slide(id="1c1", section_id="2", tree_node="n1c",
      lead_message={"text": "Stores with the fewest labor hours per sale run about a third more shrink than the best-staffed stores",
                    "highlights": ["Q1 (fewest hours)"], "clauses": 1},
      message_type="item", archetype="column-time-series", rationale="Ranking of four quartiles against the chain average -> columns with benchmark",
      unit_line="**Shrink**, % of sales, FY2025, stores ranked by labor hours per thousand dollars of sales",
      layout={"variant": "takeaway_sidebar", "sidebar": {
          "kind": "big_number", "big_number": r("q14"),
          "caption": "the shrink rate of the best-staffed quartile, in the least-staffed quartile",
          "bullets": ["**Q1:** store managers say produce rotation and receiving checks are skipped on busy days",
                      "**Q1 to Q3:** the steepest part of the curve, where added hours cut shrink the most",
                      "**Q3 to Q4:** shrink barely moves, so extra hours there buy little"],
          "implication": "Move hours into rotation and receiving in Q1–Q2 stores and take cuts in Q3–Q4 stores (3a)"}},
      body={"kind": "chart", "chart_type": "column", "categories": ["Q1 (fewest hours)", "Q2", "Q3", "Q4 (most hours)"],
            "series": [{"name": "Shrink", "points": [r("q1"), r("q2"), r("q3"), r("q4")]}],
            "sort": "none", "highlight": ["Q1 (fewest hours)"], "value_format": "0.0%",
            "benchmark": {"label": "Chain average", "point": r("shr25")}},
      footnotes=["The pattern is a correlation across 58 stores; store managers' reports point to the mechanism. Waste and receiving errors are 65% of shrink, theft 35%"])

slide(id="1c2", section_id="2", tree_node="n1c",
      lead_message={"text": "Bringing shrink in the two least-staffed quartiles down to the Q3 rate would add about $3.8M a year",
                    "numbers": [{"text": "$3.8M", "data_ref": "lev_shr"}]},
      message_type="component", archetype="calculation-bridge",
      unit_line="**Gross margin recovered by the shrink program**, $ millions a year, on FY2025 sales, team estimate",
      body={"kind": "equation", "terms": [
          {"point": r("shr_q12"), "caption": "combined excess of Q1 (3.1%) and Q2 (2.7%) over the Q3 rate of 2.4%"},
          {"op": "÷", "point": r("nq"), "caption": "quartiles of equal sales: a 0.25 percentage point cut in chain shrink"},
          {"op": "×", "point": r("sal25"), "caption": "FY2025 sales"},
          {"op": "=", "point": r("lev_shr"), "caption": "gross margin recovered a year"}],
          "assumptions_header": "Waste and receiving errors are the part that labor fixes",
          "assumptions": ["Fresh and produce waste (45%) and receiving and administrative errors (20%) make up 65% of shrink; both depend on rotation and checks",
                          "Theft (35%) is not targeted by this program",
                          "The four quartiles carry equal sales; their simple average matches the 2.6% chain rate",
                          "Returning the whole chain to its FY2023 rate of 2.1% would double the gain; it is held as a stretch lever (5d)"]})

slide(id="1d1", section_id="2", tree_node="n1d",
      lead_message={"text": "Holding private label's FY2025 growth pace would add about $4.3M of gross margin a year by FY2028",
                    "numbers": [{"text": "$4.3M", "data_ref": "lev_pl"}], "highlights": ["FY2028 at the same pace"], "clauses": 1},
      message_type="time-series", archetype="column-time-series", rationale="Share over time plus one projected year -> columns with a basis strip",
      unit_line="**Private-label sales**, % of sales, FY2023 to FY2025 and FY2028 at the FY2025 pace",
      layout={"variant": "takeaway_sidebar", "sidebar": {
          "kind": "bullets", "header": "The gain comes from mix, not price",
          "rows": [{"label": "Gross margin added a year by FY2028", "point": r("lev_pl"), "highlight": True,
                    "basis": "2.4 pp more share × 12 pp margin gap × $1,503M FY2025 sales"}],
          "bullets": ["**Margin edge:** each private-label sale earns 12 percentage points more than a national brand",
                      "**Pace held, not raised:** only the FY2024–25 gain of 0.8 percentage points a year continues",
                      "**Fits the price problem:** a cheaper own brand answers the 41% who call Harlow expensive"]}},
      body={"kind": "chart", "chart_type": "column", "categories": ["FY2023", "FY2024", "FY2025", "FY2028 at the same pace"],
            "series": [{"name": "Private-label share", "points": [r("pl23"), r("pl24"), r("pl25"), r("pl28")]}],
            "sort": "none", "highlight": ["FY2028 at the same pace"], "value_format": "0.0%"},
      basis={"header": "How we projected FY2028", "terms": [
          {"point": r("pl25"), "caption": "share of sales, FY2025 (Table 2)"},
          {"op": "+", "point": r("pl_add"), "caption": "FY2025 gain of 0.8 pp a year × 3 years"},
          {"op": "=", "point": r("pl28"), "caption": "share in FY2028"}]})

# ---------------------------------------------------------------- section 3: e-commerce
nav("d3", "agenda_tracker", "3")
slide(id="L3", section_id="3",
      lead_message={"text": "E-commerce loses about $10M a year; repricing home delivery is the first fix and keeps the service the owners want",
                    "numbers": [{"text": "$10M", "data_ref": "ec_net"}]},
      message_type="argument", archetype="numbered-levers", unit_line="**Status of each finding**, FY2025 data",
      body={"kind": "levers", "headers": ["Finding", "Evidence"],
            "items": [{"code": "2a", "text": "Counted in full, e-commerce loses money: the team's 6.1% leaves out the courier and counts every sale as new",
                       "point": r("ec_net"), "metric": "e-commerce result, FY2025, all costs and only new sales counted"},
                      {"code": "2b", "text": "Home delivery causes the loss; a click-and-collect order loses under $2",
                       "point": r("del_loss"), "metric": "result per delivered order after the fee, FY2025"},
                      {"code": "2c", "text": "Customers accept a higher fee by switching to pickup; a rollout adds about $2.8M a year",
                       "point": r("ft_kept"), "metric": "of e-commerce sales kept in the fee test"}]})

slide(id="2a1", section_id="3", tree_node="n2a",
      lead_message={"text": "Counted in full, e-commerce loses about 8% of its sales rather than earning the 6.1% its team reports",
                    "numbers": [{"text": "8%", "data_ref": "ec_netpct"}, {"text": "6.1%", "data_ref": "ecclaim"}],
                    "highlights": ["Counted in full"], "clauses": 1},
      message_type="item", archetype="bar-ranking", rationale="Two figures for the same thing compared; a waterfall would cross zero -> bars, corrections in the sidebar",
      unit_line="**E-commerce contribution**, % of e-commerce sales, FY2025",
      layout={"variant": "takeaway_sidebar", "sidebar": {
          "kind": "bullets", "header": "Two corrections turn the reported profit into a $10.4M loss",
          "bullets": ["**Courier left out, −6.5 percentage points:** finance books third-party delivery, net of fees, in its own line, so the team's figure never carries it",
                      "**Every sale counted as new, −7.8 percentage points:** customers say 70% of what they buy online they would otherwise buy in a Harlow store",
                      "**Scale:** at 8.5% of chain sales, this loss now moves the chain margin"]}},
      body={"kind": "chart", "chart_type": "bar",
            "categories": ["E-commerce team's figure", "Counted in full"],
            "series": [{"name": "E-commerce contribution", "points": [r("ecclaim"), r("ec_netpct")]}],
            "sort": "none", "highlight": ["Counted in full"], "value_format": "0.0%"},
      footnotes=["Full count: 20 cents of contribution per new dollar (finance) on the 30% of online sales new to Harlow, less all e-commerce fulfillment in the income statement",
                 "The 'every sale counted as new' correction is the remainder and also absorbs differences in packaging and cost allocation between the two methods"])

slide(id="2a2", section_id="3", tree_node="n2a",
      lead_message={"text": "With only 30% of online sales new to Harlow, their contribution covers less than half the cost of fulfilling them",
                    "numbers": [{"text": "30%", "data_ref": "newshare"}]},
      message_type="component", archetype="calculation-bridge",
      unit_line="**Contribution from new online sales against fulfillment cost**, $ millions, FY2025",
      body={"kind": "equation", "terms": [
          {"point": r("ecsal25"), "caption": "e-commerce sales, FY2025 (8.5% of chain sales)"},
          {"op": "×", "point": r("newshare"), "caption": "new to Harlow: customers would buy the other 70% in a store (survey, n = 2,300)"},
          {"op": "×", "point": r("contr20"), "caption": "contribution per new dollar before fulfillment (finance)"},
          {"op": "=", "point": r("ec_contr"), "caption": "contribution from new online sales"},
          {"op": "÷", "point": r("ec25"), "caption": "fulfillment cost: picking plus courier, net of fees"},
          {"op": "=", "point": r("ec_cover"), "caption": "of fulfillment cost covered"}],
          "assumptions_header": "Two inputs drive the result, both from Harlow's own data",
          "assumptions": ["The survey share holds for all online sales: 70% would otherwise have been bought in a Harlow store",
                          "Cannibalized sales earn the same margin online as in store, so they add nothing",
                          "Finance's 20 cents per new dollar is gross margin less variable store costs, before fulfillment"]})

slide(id="2b1", section_id="3", tree_node="n2b",
      lead_message={"text": "Home delivery drives the loss: each delivered order loses about $12 once the courier is paid",
                    "numbers": [{"text": "$12", "data_ref": "del_loss_pos"}], "highlights": ["Third-party delivery"], "clauses": 1},
      message_type="component", archetype="waterfall-bridge", rationale="What adds up to the loss per order -> waterfall",
      unit_line="**Cost and loss per delivered order**, $, FY2025",
      layout={"variant": "takeaway_sidebar", "sidebar": {
          "kind": "big_number", "big_number": r("del_share"),
          "caption": "of the e-commerce loss comes from home delivery, 58% of orders",
          "bullets": ["**Courier:** the largest cost in the order, and it rose every year while the fee fell",
                      "**Fee:** free delivery above $75 means the average delivered order pays only $3.10",
                      "**Click-and-collect:** carries picking but no courier, and loses under $2 an order"]}},
      body={"kind": "chart", "chart_type": "waterfall",
            "categories": ["Picking", "Third-party delivery", "Delivery fee collected", "Contribution from new sales", "Loss per delivered order"],
            "series": [{"name": "Per delivered order", "points": [r("pick25"), r("tpd25"), r("fee_neg"), r("contr_neg"), r("del_loss_pos")]}],
            "sort": "none", "highlight": ["Third-party delivery"], "value_format": "0.00"},
      footnotes=["Contribution per order = $96 basket × 30% new to Harlow × 20 cents. Delivered and click-and-collect baskets assumed equal (the pack gives one average)"])

slide(id="2c1", section_id="3", tree_node="n2c",
      lead_message={"text": "The fee test kept 98% of online sales and more than doubled the fee collected per delivery",
                    "numbers": [{"text": "98%", "data_ref": "ft_kept"}]},
      message_type="item", archetype="kpi-big-numbers",
      unit_line="**Fee test results**, 4 stores, 10 weeks, late FY2025",
      body={"kind": "kpi", "items": [
          {"point": r("ft_kept"), "caption": "of e-commerce sales kept", "relation": "Total online sales fell 2%",
           "drivers": ["Delivered orders fell 9%", "Most delivery customers switched to pickup rather than leaving", "Delivery stays available, as the owners require"]},
          {"point": r("ft_fee"), "caption": "average fee per delivered order", "relation": "2.1 times the FY2025 average of $3.10",
           "drivers": ["Fee below the threshold raised from $4.99 to $7.99", "Free-delivery threshold raised from $75 to $100", "Still below the $13.80 courier cost"]},
          {"point": r("ft_cc"), "caption": "more click-and-collect orders", "relation": "Free for customers, no courier for Harlow",
           "drivers": ["Each switch saves the courier cost of the order", "Pickup costs only picking", "Moves demand to the cheaper channel"]}]},
      so_what="Customers pay more for delivery, and those who will not switch to free pickup rather than leave",
      so_what_style="bar")

slide(id="2c2", section_id="3", tree_node="n2c",
      lead_message={"text": "Rolling out the tested fee and threshold chain-wide would add about $2.8M a year while keeping delivery",
                    "numbers": [{"text": "$2.8M", "data_ref": "lev_ec"}]},
      message_type="component", archetype="calculation-bridge",
      unit_line="**Operating income added by repricing delivery**, $ millions a year, at FY2025 volumes, team estimate",
      body={"kind": "equation", "terms": [
          {"point": r("ec25"), "caption": "e-commerce fulfillment cost, FY2025"},
          {"op": "−", "point": r("new_ful"), "caption": "fulfillment at the tested fee: 9% fewer deliveries, 14% more pickups, $6.40 a delivery"},
          {"op": "−", "point": r("lost_contr"), "caption": "contribution lost on the 2% of online sales that leave"},
          {"op": "=", "point": r("lev_ec"), "caption": "operating income added a year"}],
          "assumptions_header": "The test results hold chain-wide",
          "assumptions": FT_A})

slide(id="2c3", section_id="3", tree_node="n2c",
      lead_message={"text": "Even at the tested fee each home delivery still loses about $9: the 2026 courier renewal is the next lever",
                    "numbers": [{"text": "$9", "data_ref": "del_loss_t"}]},
      message_type="argument", archetype="text-columns",
      body={"kind": "text", "style": "columns", "columns": [
          {"header": "Renegotiate the courier contract in 2026", "emphasis": True, "point": r("tpd_rise"),
           "point_caption": "a year avoided by rejecting the proposed 3% rise",
           "detail": ["The contract renews in 2026, and the provider has proposed a 3% rise",
                      "At $13.80 the courier is the largest cost in each delivered order",
                      "Tender against other couriers before accepting any increase"],
           "footer": "Owner: head of e-commerce"},
          {"header": "Test a second fee step", "point": r("be_fee"), "point_caption": "fee per delivered order at which delivery breaks even",
           "detail": ["The first test kept 98% of online sales at a $6.40 average fee",
                      "A second test in a few stores shows where demand starts to fall",
                      "Keeps delivery available, as the owners require"],
           "footer": "Test in FY2026, decide in FY2027"},
          {"header": "Steer orders to click-and-collect", "point": r("del_loss_t"), "point_caption": "per delivered order at the tested fee",
           "detail": ["Pickup orders lose under $2 each and rose 14% in the test",
                      "Promote pickup at checkout and in the app",
                      "Add pickup capacity before delivery capacity"],
           "footer": "Supports the fee change"}]},
      footnotes=["Break-even fee = picking ($7.40) + courier ($13.80) − contribution from new sales ($5.76) per delivered order, FY2025 costs"])

# ---------------------------------------------------------------- section 4: store costs
nav("d4", "agenda_tracker", "4")
slide(id="L4", section_id="4",
      lead_message={"text": "Store costs can fall by about $14M a year through targeted labor cuts and exits from loss-making stores",
                    "numbers": [{"text": "$14M", "data_ref": "st_total"}]},
      message_type="argument", archetype="numbered-levers", unit_line="**Status of each finding**, FY2025 data",
      body={"kind": "levers", "headers": ["Finding", "Evidence"], "total": r("st_total"),
            "items": [{"code": "3a", "text": "A net 4% cut taken in the best-staffed stores saves about $7.3M a year; the 8% cut risks half its saving in shrink",
                       "point": r("giveback"), "metric": "of the 8% cut's saving lost if the chain ran at the Q1 shrink rate"},
                      {"code": "3b", "text": "Nine stores lose money; closing them adds about $6.6M a year, and six can close at lease end",
                       "point": r("ws9"), "metric": "stores with negative four-wall EBITDA, FY2025"}]})

slide(id="3a1", section_id="4", tree_node="n3a",
      lead_message={"text": "Harlow has already cut hours per sale by 6%, and shrink rose half a percentage point over the same years",
                    "numbers": [{"text": "6%", "data_ref": "hrs_chg"}], "clauses": 2},
      message_type="time-series", archetype="multi-chart-panel", rationale="Two clauses, one claim -> two panels, no arrow",
      layout={"variant": "split_2"},
      body={"kind": "panels", "panels": [
          {"header": "Stores already work fewer hours per sale", "unit_line": "**Labor hours per thousand dollars of sales**",
           "delta": r("hrs_chg"),
           "body": {"kind": "chart", "chart_type": "column", "categories": ["FY2023", "FY2025"],
                    "series": [{"name": "Hours", "points": [r("hrs23"), r("hrs25")]}],
                    "sort": "none", "highlight": [], "value_format": "0.00"}},
          {"header": "Shrink rose in the same two years", "unit_line": "**Shrink**, % of sales", "delta": r("shr_chg"),
           "body": {"kind": "chart", "chart_type": "column", "categories": ["FY2023", "FY2024", "FY2025"],
                    "series": [{"name": "Shrink", "points": [r("shr23"), r("shr24"), r("shr25")]}],
                    "sort": "none", "highlight": [], "value_format": "0.0%"}}]},
      so_what="Another across-the-board cut would deepen a pattern already raising shrink (1c)",
      so_what_style="bar")

slide(id="3a2", section_id="4", tree_node="n3a",
      lead_message={"text": "The proposed 8% hours cut could give back about half of its $14.5M saving through higher shrink",
                    "numbers": [{"text": "$14.5M", "data_ref": "labsave"}], "highlights": ["Shrink at the Q1 rate"], "clauses": 1},
      message_type="component", archetype="waterfall-bridge", rationale="Gross saving less the risk -> waterfall",
      unit_line="**Annual saving of the 8% labor-hour cut**, $ millions, management estimate less our shrink scenario",
      layout={"variant": "takeaway_sidebar", "sidebar": {
          "kind": "big_number", "big_number": r("giveback"), "caption": "of the claimed saving lost to shrink in this scenario",
          "bullets": ["**Shrink risk:** Q1 stores already run 3.1% shrink against a 2.6% chain average, and the cut pushes every store toward Q1",
                      "**Customer risk:** checkout waits and stock-outs hit the fresh produce that 58% of shoppers come for",
                      "**Not counted:** sales lost to waits or empty shelves would cut the net further"]}},
      body={"kind": "chart", "chart_type": "waterfall",
            "categories": ["Saving claimed for the 8% cut", "Shrink at the Q1 rate", "Net saving"],
            "series": [{"name": "Saving", "points": [r("labsave"), r("shr_risk"), r("lab_net")]}],
            "sort": "none", "highlight": ["Shrink at the Q1 rate"], "value_format": "0.0"},
      basis={"header": "How we sized the shrink scenario", "terms": [
          {"point": r("q1x"), "caption": "Q1 shrink rate above the chain average (3.1% against 2.6%)"},
          {"op": "×", "point": r("sal25"), "caption": "FY2025 sales"},
          {"op": "=", "point": r("shr_risk"), "caption": "shrink cost a year if the chain ran at the Q1 rate"}]})

slide(id="3a3", section_id="4", tree_node="n3a",
      lead_message={"text": "A net 4% cut in the best-staffed stores saves about $7.3M a year, close to what the 8% cut would net",
                    "numbers": [{"text": "$7.3M", "data_ref": "lev_lab"}]},
      message_type="item", archetype="comparison-table",
      unit_line="**Labor plan options**, FY2025 store labor base, team estimate",
      layout={"variant": "full"},
      body={"kind": "table", "table_type": "comparison", "verdict_header": "Reading",
            "columns": ["8% across the board (management draft)", "Net 4%, targeted (recommended)"],
            "rows": [{"label": "Where hours are cut", "cells": [{"text": "Every store, including the least-staffed"}, {"text": "Q3–Q4 stores; some hours moved to Q1–Q2"}],
                      "note": "Cut where hours are plentiful"},
                     {"label": "Annual saving", "cells": [{"point": r("labsave")}, {"point": r("lev_lab")}], "highlight": True,
                      "note": "Before any shrink effect"},
                     {"label": "Shrink risk", "cells": [{"text": "Up to $7.5M a year (3a scenario)"}, {"text": "Low: Q3 and Q4 shrink differ by 0.1 percentage points"}],
                      "note": "Nets the 8% cut to about $7.0M"},
                     {"label": "Fresh and receiving", "cells": [{"text": "Rotation and checks cut with everything else"}, {"text": "Protected, and added in Q1–Q2 stores"}],
                      "note": "Fresh is why 58% shop here"},
                     {"label": "Customer risk", "cells": [{"text": "Longer checkout waits and stock-outs chain-wide"}, {"text": "Limited to the best-staffed stores"}],
                      "note": "Track waits and availability"}]},
      callout={"target": "Annual saving", "header": "Similar net, far less risk",
               "detail": "Once shrink is counted the 8% cut nets about $7.0M, close to the targeted cut"},
      basis={"header": "How we sized the targeted cut", "terms": [
          {"point": r("lab25"), "caption": "store labor cost, FY2025"},
          {"op": "×", "point": r("labcut4"), "caption": "net cut in hours after moving some to Q1–Q2 (team choice)"},
          {"op": "=", "point": r("lev_lab"), "caption": "saving a year"}]})

slide(id="3b1", section_id="4", tree_node="n3b",
      lead_message={"text": "Nine of Harlow's stores lose money at the four-wall level, and six of their leases end by 2027"},
      message_type="item", archetype="kpi-big-numbers", unit_line="**The nine weakest stores**, FY2025",
      body={"kind": "kpi", "items": [
          {"point": r("ws9"), "caption": "stores with negative four-wall EBITDA", "relation": "of 58 stores, FY2025",
           "drivers": ["Combined sales of $118M, 7.9% of the chain", "Each one is below zero on its own result", "A quarter of their sales would move to nearby Harlow stores"]},
          {"point": r("webitda"), "caption": "combined four-wall EBITDA", "relation": "FY2025",
           "drivers": ["Before head-office cost", "Staff, rent and energy leave with the store", "No turnaround plan is in the pack"]},
          {"point": r("wlease6"), "caption": "of the nine leases end by 2027", "relation": "No board vote needed",
           "drivers": ["Exit at lease end at no cost", "The other three need a board vote", "Their exit would cost $7.5M"]}]},
      so_what="Six exits need only a decision not to renew; the other three are a board choice with a cost",
      so_what_style="line")

slide(id="3b2", section_id="4", tree_node="n3b",
      lead_message={"text": "Closing all nine stores would add about $6.6M a year: $3.1M of losses removed and $3.5M from sales that move",
                    "numbers": [{"text": "$6.6M", "data_ref": "w_gain"}, {"text": "$3.1M", "data_ref": "w_gain_eb"}, {"text": "$3.5M", "data_ref": "w_trans"}]},
      message_type="component", archetype="calculation-bridge",
      unit_line="**Operating income added by closing the nine stores**, $ millions a year, team estimate",
      body={"kind": "equation", "terms": [
          {"point": r("w_trs"), "caption": "of the nine stores' $118M sales move to nearby Harlow stores (25%, past closures)"},
          {"op": "×", "point": r("wcontr"), "caption": "contribution on moved sales at the receiving store"},
          {"op": "=", "point": r("w_trans"), "caption": "contribution kept in the chain"},
          {"op": "+", "point": r("w_gain_eb"), "caption": "four-wall loss removed"},
          {"op": "=", "point": r("w_gain"), "caption": "operating income added a year"}],
          "assumptions_header": "Past closures set the transfer rate",
          "assumptions": W_A})

slide(id="3b3", section_id="4", tree_node="n3b",
      lead_message={"text": "Six stores can close at lease end at no cost; the other three repay their $7.5M exit in about 3.4 years",
                    "numbers": [{"text": "$7.5M", "data_ref": "wexit"}, {"text": "3.4 years", "data_ref": "payback"}]},
      message_type="item", archetype="comparison-table",
      unit_line="**Store-exit options**, team estimate",
      layout={"variant": "full"},
      body={"kind": "table", "table_type": "comparison", "verdict_header": "Reading",
            "columns": ["Six stores at lease end", "Three long-lease stores"],
            "rows": [{"label": "Timing", "cells": [{"text": "As leases expire, by the end of 2027"}, {"text": "After a board vote"}], "note": "Six are a non-renewal decision"},
                     {"label": "One-time cost", "cells": [{"text": "None"}, {"point": r("wexit")}], "note": "30% of the $25M cap"},
                     {"label": "Operating income a year", "cells": [{"point": r("w_gain6")}, {"point": r("w_gain3")}], "note": "Average-size stores assumed"},
                     {"label": "Payback", "cells": [{"text": "Immediate"}, {"point": r("payback")}], "highlight": True, "note": "Inside the cap and the horizon"}]},
      callout={"target": "Payback", "header": "Worth the vote",
               "detail": "Without the three, FY2028 margin lands at about 3.0%, just under the target (backup)"},
      basis={"header": "How we sized the payback", "terms": [
          {"point": r("wexit"), "caption": "one-time lease-exit cost of the three"},
          {"op": "÷", "point": r("w_gain3"), "caption": "a year from the three: a third of the $6.6M nine-store gain"},
          {"op": "=", "point": r("payback"), "caption": "to repay the exit cost"}]})

# ---------------------------------------------------------------- section 5: plan
nav("d5", "agenda_tracker", "5")
slide(id="L5", section_id="5",
      lead_message={"text": "Six moves lift operating income to about $44.8M by FY2028, a 3.2% margin that clears the board's target",
                    "numbers": [{"text": "$44.8M", "data_ref": "oi28"}, {"text": "3.2%", "data_ref": "pm28"}], "clauses": 1},
      message_type="component", archetype="waterfall-bridge", rationale="What adds up to the FY2028 result -> waterfall",
      unit_line="**Operating income**, $ millions, FY2025 actual to FY2028 plan, team estimate on FY2025 volumes",
      layout={"variant": "takeaway_sidebar", "sidebar": {
          "kind": "big_number", "big_number": r("pm28"),
          "caption": "operating margin in FY2028 on sales of $1,414.5M (no growth, nine stores closed)",
          "bullets": ["**First wave:** promotions, labor and delivery give about $16M from FY2026",
                      "**Headroom:** about $2.3M above what a 3.0% margin needs"],
          "implication": "Approve the first wave now: it clears the covenant and carries over half of the gain"}},
      body={"kind": "chart", "chart_type": "waterfall",
            "categories": ["FY2025", "Promotion reset", "Targeted labor", "Delivery repricing", "Shrink program", "Private label", "Store exits, net", "FY2028 plan"],
            "series": [{"name": "Operating income", "points": [r("oi25"), r("b_promo"), r("b_lab"), r("b_ec"), r("b_shr"), r("b_pl"), r("st_net"), r("oi28")]}],
            "sort": "none", "highlight": [], "value_format": "0.0"},
      footnotes=["Each move is sized on its own page (1a, 1c, 1d, 2c, 3a, 3b) on FY2025 sales; store exits are net of the $1.3M those moves would have earned in the closed stores",
                 "Before the 2027 minimum-wage rise and the stretch levers (5d); no sales growth assumed"])

slide(id="5a", section_id="5",
      lead_message={"text": "Promotions, delivery fees and targeted labor come first: together worth about $16M a year, they need no store closures",
                    "numbers": [{"text": "$16M", "data_ref": "quick"}]},
      message_type="item", archetype="harvey-ball-table", layout={"variant": "full"},
      unit_line="**The six moves on speed, cost and risk**, team assessment; value in $ millions a year by FY2028",
      body={"kind": "table", "table_type": "harvey", "verdict_header": "When to start",
            "columns": ["Value a year", "Speed to impact", "Low one-time cost", "Low execution risk"],
            "rows": [{"label": "Promotion reset", "cells": [{"point": r("b_promo")}, {"rating": 4}, {"rating": 4}, {"rating": 3}], "note": "Next promotional calendar"},
                     {"label": "Delivery repricing", "cells": [{"point": r("b_ec")}, {"rating": 4}, {"rating": 4}, {"rating": 3}], "note": "Now: already tested"},
                     {"label": "Targeted labor", "cells": [{"point": r("b_lab")}, {"rating": 3}, {"rating": 4}, {"rating": 3}], "note": "Now: replaces the 8% cut"},
                     {"label": "Shrink program", "cells": [{"point": r("b_shr")}, {"rating": 2}, {"rating": 4}, {"rating": 3}], "note": "FY2026 H2, with the labor moves"},
                     {"label": "Private label", "cells": [{"point": r("b_pl")}, {"rating": 1}, {"rating": 3}, {"rating": 3}], "note": "Builds through FY2028"},
                     {"label": "Store exits, net", "cells": [{"point": r("st_net")}, {"rating": 1}, {"rating": 2}, {"rating": 2}], "note": "FY2027, as leases end"},
                     {"label": "First wave", "cells": [{"point": r("quick")}, {"text": ""}, {"text": ""}, {"text": ""}], "highlight": True,
                      "note": "Over half of the plan"}],
            "legend": "Full circle = fastest, lowest one-time cost, lowest risk; team assessment from the briefing pack"},
      callout={"target": "First wave", "header": "Start in the first quarter",
               "detail": "Under a third of this run rate in FY2026 clears the $20M covenant (5b)"})

slide(id="5b", section_id="5",
      lead_message={"text": "Capturing under a third of the first wave's run rate in FY2026 would clear the lender's $20M covenant",
                    "numbers": [{"text": "$20M", "data_ref": "cov20"}]},
      message_type="component", archetype="calculation-bridge",
      unit_line="**FY2026 covenant test**, $ millions of operating income, team estimate",
      body={"kind": "equation", "terms": [
          {"point": r("cov20"), "caption": "operating income the covenant requires in FY2026"},
          {"op": "−", "point": r("oi25"), "caption": "operating income, FY2025"},
          {"op": "=", "point": r("cov_gap"), "caption": "needed in FY2026 above FY2025"},
          {"op": "÷", "point": r("quick"), "caption": "full-year run rate of the first wave"},
          {"op": "=", "point": r("cov_share"), "caption": "of the run rate needed in FY2026"}],
          "assumptions_header": "The test holds only if the drift stops",
          "assumptions": ["Promotional share and shrink rise no further than their FY2025 levels; each extra percentage point of promotional share costs about $2.1M",
                          "The courier's proposed 3% rise (about $0.3M) is rejected or offset at the 2026 renewal",
                          "We follow the pack in treating FY2026 as the first plan year and the covenant year; if it is already largely past, the test rests on actions taken so far"]})

slide(id="5c", section_id="5",
      lead_message={"text": "Three moves start in the first half of FY2026, and store exits follow as leases end in FY2027"},
      message_type="structure", archetype="timeline-roadmap", rationale="Moves over time with dates -> timeline",
      unit_line="**Plan timing**, by half fiscal year, FY2026 to FY2028", layout={"variant": "full"},
      body={"kind": "timeline", "periods": ["FY2026 H1", "FY2026 H2", "FY2027 H1", "FY2027 H2", "FY2028"],
            "rows": [{"label": "Promotion reset", "bars": [{"start": "FY2026 H1", "end": "FY2026 H1", "label": "Stop money-losing events", "emphasis": True},
                                                          {"start": "FY2026 H2", "end": "FY2028", "label": "Hold share at 26.2%; renegotiate vendor funding"}]},
                     {"label": "Delivery repricing", "bars": [{"start": "FY2026 H1", "end": "FY2026 H1", "label": "Tested fee chain-wide", "emphasis": True},
                                                             {"start": "FY2026 H2", "end": "FY2027 H1", "label": "Courier renewal; second fee test"}]},
                     {"label": "Targeted labor", "bars": [{"start": "FY2026 H1", "end": "FY2026 H1", "label": "Net 4% plan", "emphasis": True},
                                                         {"start": "FY2026 H2", "end": "FY2027 H2", "label": "Hours into rotation and receiving"}]},
                     {"label": "Shrink program", "bars": [{"start": "FY2026 H2", "end": "FY2028", "label": "Q1–Q2 stores to the Q3 rate"}]},
                     {"label": "Private label", "bars": [{"start": "FY2026 H2", "end": "FY2028", "label": "Range growth of 0.8 pp share a year"}]},
                     {"label": "Store exits", "bars": [{"start": "FY2027 H1", "end": "FY2027 H2", "label": "Six at lease end"},
                                                      {"start": "FY2027 H2", "end": "FY2028", "label": "Three after a board vote"}]}],
            "milestones": [{"at": "FY2026 H2", "label": "Covenant: $20M"}, {"at": "FY2028", "label": "Target: 3.0%"}]},
      so_what="The first wave pays in before the $7.5M lease-exit cost falls due",
      so_what_style="line")

slide(id="5d", section_id="5",
      lead_message={"text": "The 2027 minimum-wage rise is the largest risk to the target, and two stretch levers held in reserve would cover it"},
      message_type="item", archetype="comparison-table", layout={"variant": "full"},
      unit_line="**Risks to the FY2028 target**, team estimate",
      body={"kind": "table", "table_type": "comparison", "verdict_header": "Watch",
            "columns": ["What could happen", "Size", "Response"],
            "rows": [{"label": "2027 minimum-wage rise", "highlight": True,
                      "cells": [{"text": "State minimum wage rises 4% in 2027"}, {"text": "Up to $7.3M a year if every hourly rate rose 4%"},
                                {"text": "Two stretch levers worth $8.4M: promotions to the FY2023 share, shrink to 2.1%"}],
                      "note": "Wage bill each quarter"},
                     {"label": "Traffic loss from fewer promotions",
                      "cells": [{"text": "Shoppers near ValuMart leave as promotions fall"}, {"text": "Each percentage point of promotional share is worth $2.1M"},
                                {"text": "Keep promotions within three miles of a ValuMart"}],
                      "note": "Comparable sales by trade area"},
                     {"label": "Delivery customers leave",
                      "cells": [{"text": "The fee rollout loses more orders than the test"}, {"text": "The test lost 2% of online sales"},
                                {"text": "Roll out by store group; keep pickup free"}],
                      "note": "Weekly orders by channel"},
                     {"label": "Closed-store sales do not transfer",
                      "cells": [{"text": "Fewer than 25% of sales move to nearby stores"}, {"text": "Transfers are $3.5M of the $6.6M gain"},
                                {"text": "Target the closed stores' loyalty-card customers"}],
                      "note": "Receiving-store sales"}]},
      callout={"target": "2027 minimum-wage rise", "header": "Largest risk",
               "detail": "The stretch levers bring the margin back to about 3.2% (backup)"})

slide(id="5e", section_id="5",
      lead_message={"text": "Six numbers will tell the board each quarter whether the plan is on track", "count_word": 6},
      message_type="item", archetype="data-table", layout={"variant": "full"},
      unit_line="**Plan tracking measures**, FY2025 actual and FY2028 plan",
      body={"kind": "table", "table_type": "data", "verdict_header": "Reported",
            "columns": ["FY2025", "FY2028 plan"],
            "rows": [{"label": "Promotional share of sales", "cells": [{"point": r("promo25")}, {"point": r("promo24")}], "note": "Monthly, by trade area"},
                     {"label": "Shrink in Q1–Q2 stores", "cells": [{"point": r("q12avg")}, {"point": r("q3")}], "note": "Monthly, by store"},
                     {"label": "Fee per delivered order", "cells": [{"point": r("fee25")}, {"point": r("ft_fee")}], "note": "Monthly"},
                     {"label": "Labor hours per thousand dollars of sales", "cells": [{"point": r("hrs25")}, {"point": r("hrs_tgt")}], "note": "Weekly, by store quartile"},
                     {"label": "Private-label share of sales", "cells": [{"point": r("pl25")}, {"point": r("pl28")}], "note": "Quarterly"},
                     {"label": "Comparable sales near ValuMart", "cells": [{"point": r("vmc")}, {"text": "No worse than FY2025"}], "note": "Monthly: the traffic check"}]},
      footnotes=["Shrink in Q1–Q2 stores is the simple average of the two quartiles; the plan brings both to the Q3 rate"])

# ---------------------------------------------------------------- appendix
S.append({"id": "app", "role": "appendix_divider", "status": "filled"})
S.append({"id": "bx", "role": "backup", "section_id": "1", "status": "filled",
          "lead_message": {"prefix": "BACKUP:", "text": "Five branches were left out on purpose: two cannot be moved, one is a commitment, two are too small"},
          "message_type": "item", "archetype": "definition-table", "tree_node": ["nx1", "nx2", "nx3", "nx4", "nx5"],
          "body": {"kind": "table", "table_type": "definition", "columns": ["Hypothesis", "Why it is not in the plan"],
                   "rows": [{"label": "Broad price rise", "cells": [{"text": "A general price increase would recover margin faster than cost moves"},
                                                                    {"text": "41% of shoppers already call Harlow expensive while ValuMart expands"}]},
                            {"label": "Wage rates", "cells": [{"text": "Harlow can hold hourly pay below the market"},
                                                              {"text": "Set by the state minimum wage and a tight labor market"}]},
                            {"label": "Close e-commerce", "cells": [{"text": "Closing the online service would remove its loss"},
                                                                    {"text": "The owners want delivery kept in some form"}]},
                            {"label": "Other SG&A", "cells": [{"text": "Overhead holds savings that would move the margin"},
                                                              {"text": "Flat at 4.7% of sales: no part of the decline"}]},
                            {"label": "Rent renegotiation", "cells": [{"text": "Occupancy costs can be cut store by store"},
                                                                      {"text": "Leases are fixed until expiry; handled through store exits (3b)"}]}]}})

S.append({"id": "b1", "role": "backup", "section_id": "1", "backup_of": "s1a", "status": "filled",
          "lead_message": {"prefix": "BACKUP:", "text": "Every cost line except other SG&A took a larger share of sales between FY2023 and FY2025"},
          "message_type": "item", "archetype": "data-table", "unit_line": "**Income statement**, % of sales and change in percentage points",
          "layout": {"variant": "full"},
          "body": {"kind": "table", "table_type": "data", "columns": ["FY2023", "FY2025", "Change"],
                   "rows": [{"label": "Gross margin", "cells": [r1 for r1 in ({"point": r("gm23")}, {"point": r("gm25")}, {"point": r("pp_gm")})]},
                            {"label": "Store labor", "cells": [{"point": r("labpct23")}, {"point": r("labpct25")}, {"point": r("pp_labpct")}]},
                            {"label": "Occupancy and energy", "cells": [{"point": r("occpct23")}, {"point": r("occpct25")}, {"point": r("pp_occpct")}]},
                            {"label": "E-commerce fulfillment", "cells": [{"point": r("ecpct23")}, {"point": r("ecpct25")}, {"point": r("pp_ecpct")}]},
                            {"label": "Other SG&A", "cells": [{"point": r("sgapct23")}, {"point": r("sgapct25")}, {"point": r("pp_sgapct")}]},
                            {"label": "Operating margin", "highlight": True, "cells": [{"point": r("om23")}, {"point": r("om25")}, {"point": r("pp_om")}]}]},
          "footnotes": ["Table 1 of the briefing pack; shares are each line divided by sales. Sales grew 5.9% over the two years while operating income fell 68%"]})

S.append({"id": "bcat", "role": "backup", "section_id": "2", "backup_of": "1b1", "status": "filled",
          "lead_message": {"prefix": "BACKUP:", "text": "The category team's case for deeper promotions counts the extra sales but not the margin they cost"},
          "message_type": "argument", "archetype": "text-columns",
          "body": {"kind": "text", "style": "columns", "columns": [
              {"header": "What the claim says", "point": r("deep18"), "point_caption": "comparable sales growth in the deepest-promotion stores",
               "detail": ["Against 0.2% for the other stores in FY2025", "Read as proof that promotions work",
                          "Used to defend deeper promotions against ValuMart"]},
              {"header": "What it leaves out", "point": r("promogap"), "point_caption": "less gross margin on every promotional sale",
               "detail": ["38% of FY2025 events lost money after counting their extra units",
                          "A sales gain of 1.6 percentage points says nothing about profit",
                          "The stores may differ in other ways, such as distance from a ValuMart"]},
              {"header": "What shoppers say brings them in", "emphasis": True, "point": r("fresh58"),
               "point_caption": "name fresh produce as a top reason to shop Harlow",
               "detail": ["Convenience is named by 44%", "41% call Harlow more expensive, up from 33% despite deeper promotions",
                          "Fresh quality depends on produce rotation, the task skipped in thin-staffed stores"]}]}})

S.append({"id": "b2", "role": "backup", "section_id": "3", "backup_of": "2b1", "status": "filled",
          "lead_message": {"prefix": "BACKUP:", "text": "The loss widened as more orders went to the home and the fee fell further behind the courier's cost",
                           "clauses": 2},
          "message_type": "time-series", "archetype": "multi-chart-panel", "layout": {"variant": "split_2"},
          "body": {"kind": "panels", "panels": [
              {"header": "More orders now go to the home", "unit_line": "**Share of orders delivered to the home**, %",
               "body": {"kind": "chart", "chart_type": "column", "categories": ["FY2023", "FY2024", "FY2025"],
                        "series": [{"name": "Delivered share", "points": [r("del23"), r("del24"), r("del25")]}],
                        "sort": "none", "highlight": [], "value_format": "0%"}},
              {"header": "The courier's cost rose while the fee fell", "unit_line": "**Per delivered order**, $",
               "body": {"kind": "chart", "chart_type": "line", "categories": ["FY2023", "FY2024", "FY2025"],
                        "series": [{"name": "Third-party delivery cost", "points": [r("tpd23"), r("tpd24"), r("tpd25")]},
                                   {"name": "Fee collected", "points": [r("fee23"), r("fee24"), r("fee25")]}],
                        "sort": "none", "highlight": [], "value_format": "0.00"}}]},
          "footnotes": ["The gap between courier cost and fee per delivered order widened from $9.50 in FY2023 to $10.70 in FY2025 (Table 5)"]})

S.append({"id": "b3", "role": "backup", "section_id": "3", "backup_of": "2a1", "status": "filled",
          "lead_message": {"prefix": "BACKUP:", "text": "Order volumes and unit costs rebuild the income statement's e-commerce fulfillment line in every year"},
          "message_type": "item", "archetype": "data-table", "unit_line": "**E-commerce fulfillment rebuilt from Table 5**, $ millions unless stated",
          "layout": {"variant": "full"},
          "body": {"kind": "table", "table_type": "data", "columns": ["FY2023", "FY2024", "FY2025"],
                   "rows": [{"label": "Orders, thousands", "cells": [{"point": r("ord23")}, {"point": r("ord24")}, {"point": r("ord25")}]},
                            {"label": "Delivered orders, thousands", "cells": [{"point": r("delord23")}, {"point": r("delord24")}, {"point": r("delord25")}]},
                            {"label": "Picking cost", "cells": [{"point": r("pickc23")}, {"point": r("pickc24")}, {"point": r("pickc25")}]},
                            {"label": "Third-party delivery cost", "cells": [{"point": r("tpdc23")}, {"point": r("tpdc24")}, {"point": r("tpdc25")}]},
                            {"label": "Delivery fees collected", "cells": [{"point": r("feer23")}, {"point": r("feer24")}, {"point": r("feer25")}]},
                            {"label": "Fulfillment, rebuilt", "highlight": True, "cells": [{"point": r("ful23")}, {"point": r("ful24")}, {"point": r("ful25")}]},
                            {"label": "Fulfillment, income statement", "cells": [{"point": r("ec23")}, {"point": r("ec24")}, {"point": r("ec25")}]}]},
          "footnotes": ["Picking = cost per order × all orders; courier and fees = per delivered order × delivered orders (orders × home-delivery share)"]})

S.append({"id": "b4", "role": "backup", "section_id": "5", "backup_of": "L5", "status": "filled",
          "lead_message": {"prefix": "BACKUP:", "text": "Each of the six moves rests on one or two assumptions the CEO should confirm before the board"},
          "message_type": "item", "archetype": "definition-table",
          "body": {"kind": "table", "table_type": "definition", "columns": ["How it is sized", "Assumption to confirm"],
                   "rows": [{"label": "Promotion reset (1a)", "cells": [{"text": "Share back to 26.2% × 14 pp gap × FY2025 sales"}, {"text": "Shoppers buy cut items at regular price"}]},
                            {"label": "Shrink program (1c)", "cells": [{"text": "Q1–Q2 to the Q3 rate, spread over four equal quartiles"}, {"text": "Rotation and checks cut waste and errors"}]},
                            {"label": "Private label (1d)", "cells": [{"text": "0.8 pp share a year for three years × 12 pp gap"}, {"text": "The range can keep growing at that pace"}]},
                            {"label": "Delivery repricing (2c)", "cells": [{"text": "Fee test results applied to FY2025 volumes"}, {"text": "Four stores over 10 weeks represent the chain"}]},
                            {"label": "Targeted labor (3a)", "cells": [{"text": "Net 4% of FY2025 store labor cost"}, {"text": "Q3–Q4 cuts leave shrink unchanged"}]},
                            {"label": "Store exits (3b)", "cells": [{"text": "Four-wall loss removed plus 25% of sales moved at 12%"}, {"text": "Past closures predict the transfer"}]}]}})

S.append({"id": "b5", "role": "backup", "section_id": "5", "backup_of": "5d", "status": "filled",
          "lead_message": {"prefix": "BACKUP:", "text": "The plan clears the target in the base case and with stretch levers, but not if the wage rise is unanswered"},
          "message_type": "item", "archetype": "data-table", "unit_line": "**FY2028 operating income and margin by scenario**, team estimate",
          "layout": {"variant": "full"},
          "body": {"kind": "table", "table_type": "data", "columns": ["Operating income", "Operating margin"], "verdict_header": "Reading",
                   "rows": [{"label": "Base plan", "highlight": True, "cells": [{"point": r("oi28")}, {"point": r("pm28")}], "note": "Clears the target"},
                            {"label": "2027 wage rise in full", "cells": [{"point": r("oi_w")}, {"point": r("pm_w")}], "note": "Misses by about a third of a point"},
                            {"label": "Wage rise and both stretch levers", "cells": [{"point": r("oi_ws")}, {"point": r("pm_ws")}], "note": "Back above target"},
                            {"label": "Only the six lease-end stores close", "cells": [{"point": r("oi_6")}, {"point": r("pm_6")}], "note": "Just under target"},
                            {"label": "Promotional share 1 pp above plan", "cells": [{"point": r("oi_p")}, {"point": r("pm_p")}], "note": "Thin headroom"}]},
          "footnotes": ["Margins on the FY2028 sales base (FY2025 sales less the closed stores' sales that do not transfer); scenarios change one thing at a time from the base plan"]})

S.append({"id": "b6", "role": "backup", "section_id": "5", "backup_of": "L5", "status": "filled",
          "lead_message": {"prefix": "BACKUP:", "text": "Eight planning choices were made without management input and should be confirmed before the board meeting",
                           "count_word": 8},
          "message_type": "item", "archetype": "definition-table",
          "body": {"kind": "table", "table_type": "definition", "columns": ["What we chose", "Why"],
                   "rows": [{"label": "Plan years", "cells": [{"text": "FY2026 is the first plan year and the covenant year"}, {"text": "As the pack's constraints and draft plan use it"}]},
                            {"label": "Promotion target", "cells": [{"text": "Back to the FY2024 share of 26.2%"}, {"text": "Before the steepest rise; keeps ValuMart defense"}]},
                            {"label": "Labor cut", "cells": [{"text": "Net 4% of hours, in Q3–Q4 stores"}, {"text": "Half the draft cut, where shrink is flat"}]},
                            {"label": "Shrink target", "cells": [{"text": "Q1–Q2 stores to the Q3 rate"}, {"text": "Proven in Harlow's own stores"}]},
                            {"label": "Private label", "cells": [{"text": "FY2025 pace for three years"}, {"text": "No faster than shown so far"}]},
                            {"label": "Sales growth", "cells": [{"text": "None to FY2028"}, {"text": "Keeps the target test conservative"}]},
                            {"label": "Store exits", "cells": [{"text": "All nine in the base case"}, {"text": "Three need a board vote"}]},
                            {"label": "Basket size", "cells": [{"text": "Same $96 for delivery and pickup"}, {"text": "The pack gives one average"}]}]}})

S.append({"id": "end", "role": "end_page", "status": "filled"})

# ============================================================ assign slide_id = first slide that shows the number
from itertools import chain


def refs(o):
    if isinstance(o, dict):
        if "data_ref" in o:
            yield o["data_ref"]
        for k, v in o.items():
            if k != "data_ref":
                yield from refs(v)
    elif isinstance(o, list):
        for v in o:
            yield from refs(v)


first = {}
for s in S:
    for x in refs(s):
        assert x in DP, (s["id"], x)
        first.setdefault(x, s["id"])
deps = {}
for i in ORDER:
    for j in DP[i].get("derived_from", []):
        deps.setdefault(j, []).append(i)


def first_slide(i, seen=()):
    if i in first:
        return first[i]
    order_ix = {s["id"]: k for k, s in enumerate(S)}
    cands = [first_slide(k, seen + (i,)) for k in deps.get(i, []) if k not in seen]
    cands = [c for c in cands if c]
    return min(cands, key=lambda c: order_ix[c]) if cands else None


for i in ORDER:
    DP[i]["slide_id"] = first_slide(i) or "s1a"

# ============================================================ storyline and spec
content_by_sec = {}
for s in S:
    if s["role"] == "content":
        content_by_sec.setdefault(s["section_id"], []).append(s["id"])

storyline = {
    "governing_thought": "Fix promotions, shrink and delivery, not wages: six moves reach a 3.2% margin by FY2028",
    "exec_summary": [
        {"id": "1", "text": "Margin fell mainly through promotions, shrink and e-commerce, not wages",
         "supports": content_by_sec["1"],
         "sub_points": [{"text": "Gross margin and e-commerce explain nearly four-fifths of the fall from 3.4% to 1.0%", "slide_id": "s1a"},
                        {"text": "Hourly pay rose 9.4%, but fewer hours per sale absorbed about 70% of it", "slide_id": "s1b"}]},
        {"id": "2", "text": "Promotions, shrink and private label can win back about $14M of gross margin a year",
         "supports": content_by_sec["2"],
         "sub_points": [{"text": "38% of promotions lost money; returning to the FY2024 share adds about $5.9M", "slide_id": "1a2"},
                        {"text": "Fixing shrink in the least-staffed stores adds about $3.8M", "slide_id": "1c2"}]},
        {"id": "3", "text": "E-commerce loses about $10M a year; repricing home delivery adds $2.8M",
         "supports": content_by_sec["3"],
         "sub_points": [{"text": "Each home delivery loses about $12 after the fee; the fee test kept 98% of online sales", "slide_id": "2b1"}]},
        {"id": "4", "text": "Targeted labor cuts and nine store exits save about $14M a year",
         "supports": content_by_sec["4"],
         "sub_points": [{"text": "The proposed 8% cut risks about $7.5M of its $14.5M saving in extra shrink", "slide_id": "3a2"},
                        {"text": "Six stores close at lease end; three repay their $7.5M exit in 3.4 years", "slide_id": "3b3"}]},
        {"id": "5", "text": "Promotions, delivery fees and labor go first, reaching about 3.2% by FY2028",
         "supports": content_by_sec["5"],
         "sub_points": [{"text": "Under a third of the first wave's $16M in FY2026 clears the $20M covenant", "slide_id": "5b"},
                        {"text": "Stretch levers worth $8.4M cover a 2027 wage rise of up to $7.3M", "slide_id": "5d"}]}],
    "next_steps": [
        {"action": "Approve the promotion reset: stop money-losing events, cap promotional share at 26.2%, reopen vendor funding", "owner": "Chief merchant", "timing": "Next promotional calendar"},
        {"action": "Roll out the tested delivery fee and threshold chain-wide; tender the courier contract before renewal", "owner": "Head of e-commerce", "timing": "FY2026 H1"},
        {"action": "Replace the 8% hours cut with the net 4% targeted plan; restore rotation and receiving in Q1–Q2 stores", "owner": "COO", "timing": "FY2026 H1"},
        {"action": "Give notice on the six expiring leases; bring the three long-lease exits to a board vote", "owner": "CFO and real estate", "timing": "FY2027"},
        {"action": "Report the six tracking measures and the covenant forecast to the board every quarter", "owner": "CFO", "timing": "From the next board meeting"}]}

issue_tree = [
    {"id": "n1", "code": "1", "label": "Gross margin", "hypothesis": "Harlow can win back most of its lost gross margin through promotions, shrink and private label"},
    {"id": "n1a", "code": "1a", "parent": "n1", "hypothesis": "Promotions have grown past the point of paying back, and the money-losing events can be cut",
     "priority": {"importance": "high", "influence": "high"},
     "workplan": {"analysis": "Promotional share and vendor funding over time; size a return to an earlier share", "exhibit": "two-panel columns; calculation bridge",
                  "sources": ["Briefing pack Table 2 and notes"], "knock_out": True},
     "finding": {"verdict": "confirmed", "note": "Promotional share rose 5 percentage points to 29%, 38% of events lost money; a return to the FY2024 share adds about $5.9M"}},
    {"id": "n1b", "code": "1b", "parent": "n1", "hypothesis": "Deeper promotions are needed to hold traffic against ValuMart",
     "priority": {"importance": "high", "influence": "medium"},
     "workplan": {"analysis": "Comparable sales near ValuMart; price perception over time; the category team's evidence", "exhibit": "two-panel columns",
                  "sources": ["Briefing pack sections 9 and 10"]},
     "finding": {"verdict": "refuted", "note": "Stores near ValuMart still fell 4.2% and the share calling Harlow expensive rose from 33% to 41% despite deeper promotions"}},
    {"id": "n1c", "code": "1c", "parent": "n1", "hypothesis": "Shrink rose because stores cut the hours that keep produce rotated and receiving checked",
     "priority": {"importance": "high", "influence": "high"},
     "workplan": {"analysis": "Shrink by labor-intensity quartile; shrink composition; size Q1–Q2 to the Q3 rate", "exhibit": "column by quartile; calculation bridge",
                  "sources": ["Briefing pack Table 4 and notes"]},
     "finding": {"verdict": "revised", "note": "True for the least-staffed half of stores; above the Q3 level more hours barely lower shrink"}},
    {"id": "n1d", "code": "1d", "parent": "n1", "hypothesis": "Private label can keep lifting gross margin at its current pace",
     "priority": {"importance": "medium", "influence": "high"},
     "workplan": {"analysis": "Private-label share trend and margin gap; project to FY2028", "exhibit": "column with basis strip",
                  "sources": ["Briefing pack Table 2"]},
     "finding": {"verdict": "confirmed", "note": "Share rose 0.8 percentage points in FY2025 at a 12 percentage point margin edge; holding the pace adds about $4.3M"}},
    {"id": "n2", "code": "2", "label": "E-commerce", "hypothesis": "E-commerce can keep home delivery and stop losing money"},
    {"id": "n2a", "code": "2a", "parent": "n2", "hypothesis": "E-commerce is profitable, as the e-commerce team reports",
     "priority": {"importance": "high", "influence": "high"},
     "workplan": {"analysis": "Rebuild e-commerce contribution with the courier and incrementality", "exhibit": "waterfall from 6.1% to a full count",
                  "sources": ["Briefing pack Tables 1 and 5, survey, finance estimate"], "knock_out": True},
     "finding": {"verdict": "refuted", "note": "Counting the courier and only the 30% of sales that are new, e-commerce loses about $10.4M (−8.2% of its sales)"}},
    {"id": "n2b", "code": "2b", "parent": "n2", "hypothesis": "Home delivery, not click-and-collect, causes the e-commerce loss",
     "priority": {"importance": "high", "influence": "high"},
     "workplan": {"analysis": "Result per delivered and per pickup order", "exhibit": "waterfall per delivered order", "sources": ["Briefing pack Table 5"]},
     "finding": {"verdict": "confirmed", "note": "A delivered order loses about $12.34; a pickup order about $1.64; delivery is about 91% of the loss"}},
    {"id": "n2c", "code": "2c", "parent": "n2", "hypothesis": "Customers accept higher delivery fees by switching to click-and-collect rather than leaving",
     "priority": {"importance": "high", "influence": "high"},
     "workplan": {"analysis": "Fee test results; size the chain-wide rollout", "exhibit": "KPI tiles; calculation bridge", "sources": ["Briefing pack fee test"]},
     "finding": {"verdict": "confirmed", "note": "The test kept 98% of online sales and lifted the fee per delivery to $6.40; rollout adds about $2.8M"}},
    {"id": "n3", "code": "3", "label": "Store costs", "hypothesis": "Store costs can fall without cutting the hours that protect fresh produce and receiving"},
    {"id": "n3a", "code": "3a", "parent": "n3", "hypothesis": "An 8% across-the-board cut in labor hours is the best labor lever",
     "priority": {"importance": "high", "influence": "high"},
     "workplan": {"analysis": "Hours and shrink trend; shrink risk of the cut; compare with a targeted cut", "exhibit": "two panels; waterfall; comparison table",
                  "sources": ["Briefing pack Tables 3 and 4, management plan"], "knock_out": True},
     "finding": {"verdict": "revised", "note": "A cut is right but should be a net 4% in the best-staffed stores; the 8% cut risks about half its saving in shrink"}},
    {"id": "n3b", "code": "3b", "parent": "n3", "hypothesis": "Exiting the loss-making stores adds profit within the lease and capital commitments",
     "priority": {"importance": "medium", "influence": "high"},
     "workplan": {"analysis": "Closure gain with transfers; options by lease status", "exhibit": "KPI tiles; calculation bridge; comparison table",
                  "sources": ["Briefing pack Table 6"]},
     "finding": {"verdict": "confirmed", "note": "Closing all nine adds about $6.6M a year; six close at lease end, three repay $7.5M in about 3.4 years"}},
    {"id": "nx1", "label": "Broad price rise", "hypothesis": "A broad price increase would recover margin faster than cost moves",
     "priority": {"importance": "high", "influence": "low"}, "cut_reason": "41% of shoppers already call Harlow expensive while ValuMart expands"},
    {"id": "nx2", "label": "Wage rates", "hypothesis": "Harlow can hold its hourly wage rates below the market",
     "priority": {"importance": "medium", "influence": "low"}, "cut_reason": "Set by the state minimum wage and a tight labor market"},
    {"id": "nx3", "label": "Close e-commerce", "hypothesis": "Closing the e-commerce service would remove its loss",
     "cut_reason": "Out of scope: the owners want delivery kept in some form"},
    {"id": "nx4", "label": "Other SG&A", "hypothesis": "Other SG&A holds savings large enough to move the margin",
     "priority": {"importance": "low", "influence": "high"}, "cut_reason": "Flat at 4.7% of sales from FY2023 to FY2025; no part of the decline"},
    {"id": "nx5", "label": "Rent renegotiation", "hypothesis": "Occupancy costs can be renegotiated store by store",
     "priority": {"importance": "low", "influence": "low"}, "cut_reason": "Leases are fixed until expiry; handled through store exits (3b)"},
]

CHOICES = ("The CEO was not available to answer questions; the team chose and recorded these: (1) deep deck (client diagnostic), navy theme, "
           "work only from the briefing pack; (2) FY2026 is treated as the first plan year and the covenant year, as the pack does; "
           "(3) promotional share target: the FY2024 level of 26.2%; (4) net labor-hour cut of 4%, taken in the Q3–Q4 stores; "
           "(5) shrink target: Q1–Q2 stores to the Q3 rate; (6) private label grows at its FY2025 pace (0.8 pp a year) for three years; "
           "(7) no sales growth to FY2028; (8) all nine weak stores closed in the base case, three after a board vote; "
           "(9) the same $96 basket for delivered and click-and-collect orders.")

spec = {
    "spec_version": "0.1", "mode": "deck_deep",
    "meta": {"title": "Reversing the margin decline", "subtitle": "Margin plan for the February 2027 board meeting",
             "company_name": "Harlow Fresh Markets", "audience": "CEO and board",
             "purpose": "How should Harlow reverse its declining operating margin, and which actions should it take first?",
             "date": "2027-02-01", "language": "en-US",
             "confidentiality": "Board discussion document; built only from the briefing pack (synthetic benchmark data)",
             "theme": "navy", "deck_type": "client_diagnostic"},
    "inputs": [{"id": "in-1", "kind": "file", "label": "Harlow Fresh Markets briefing pack", "content": "evidence/briefing-pack.md"},
               {"id": "in-2", "kind": "qa_answer", "label": "Planning choices made by the team (CEO unavailable)", "content": CHOICES}],
    "storyline": storyline,
    "problem": {
        "statement": "How can Harlow lift operating margin from 1.0% to at least 3.0% by FY2028, within $25M of one-time cost and the FY2026 covenant, and what comes first?",
        "decision_maker": "CEO, presenting the margin plan for board approval",
        "success_criteria": ["Operating margin of at least 3.0% by FY2028",
                             "At most $25M of one-time cost or capital over FY2026–FY2028",
                             "Operating income of at least $20M in FY2026 (lender covenant)",
                             "No closure of a store with a lease beyond 2027 without a board vote; delivery kept in some form"],
        "deadline": "Board meeting, February 2027",
        "accuracy": "Order of magnitude (±20% on each move); briefing pack only, no outside data",
        "out_of_scope": ["Closing the e-commerce service", "Broad price increases and new stores", "Refinancing or covenant renegotiation"],
        "one_day_answer": {
            "situation": "Sales grew 6% from FY2023 to FY2025, but operating margin fell from 3.4% to 1.0%",
            "complication": "Management blames wages and plans an 8% hours cut, yet promotions, shrink and home delivery explain most of the fall, and the cut risks more shrink",
            "resolution": "Cut money-losing promotions, reprice delivery, rebalance labor toward fresh and receiving, and exit loss-making stores: about 3.2% by FY2028"}},
    "issue_tree": issue_tree,
    "sections": [
        {"id": "1", "title": "Where the margin went", "tracker_label": "Diagnosis", "exec_item_id": "1", "lead_slide": "s1a",
         "question": "What drove operating margin from 3.4% to 1.0% between FY2023 and FY2025?"},
        {"id": "2", "title": "Gross margin: promotions, shrink and private label", "tracker_label": "Gross margin", "exec_item_id": "2",
         "tree_node": "n1", "lead_slide": "L2", "question": "How much gross margin can promotions, shrink and private label win back?"},
        {"id": "3", "title": "E-commerce economics", "tracker_label": "E-commerce", "exec_item_id": "3", "tree_node": "n2", "lead_slide": "L3",
         "question": "Can Harlow keep home delivery and stop e-commerce losing money?"},
        {"id": "4", "title": "Store labor and the store network", "tracker_label": "Store costs", "exec_item_id": "4", "tree_node": "n3",
         "lead_slide": "L4", "question": "Where should store labor and the store network be cut, and where not?"},
        {"id": "5", "title": "Plan and first actions", "tracker_label": "Plan", "exec_item_id": "5", "lead_slide": "L5",
         "question": "Does the plan reach 3.0% by FY2028 within the constraints, and what comes first?"}],
    "slides": S,
    "data_points": [DP[i] for i in ORDER],
    "sources": [
        {"id": "s1", "kind": "user_provided", "name": "Harlow Fresh Markets briefing pack", "input_id": "in-1"},
        {"id": "s2", "kind": "derived", "name": "Team analysis of the briefing pack"},
        {"id": "s3", "kind": "user_provided", "name": "Planning choices made by the team (CEO unavailable to confirm)", "input_id": "in-2"}],
}

out = os.path.join(HERE, "harlow-margin-plan.json")
with open(out, "w", encoding="utf-8") as f:
    json.dump(spec, f, ensure_ascii=False, indent=1)
print("wrote", out, len(S), "slides,", len(DP), "data points")
for k in ("lev_promo", "lev_shr", "lev_pl", "lev_ec", "lev_lab", "w_gain", "overlap", "st_net", "lev_sum", "oi28", "sal28", "pm28", "headroom",
          "quick", "cov_share", "wage_risk", "stretch", "pm_w", "pm_ws", "pm_6", "pm_p", "ec_net", "ec_netpct", "del_loss", "del_share", "giveback",
          "payback", "absorb", "sh_gpec", "sh_lab", "pl_off", "gm_total", "st_total", "quick_sh", "tpd_rise", "be_fee", "del_loss_t"):
    print(f"  {k:10s} {DP[k]['value']}")
