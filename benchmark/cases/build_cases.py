"""Build the five benchmark evidence packets and their hidden answer keys from models.py.

Usage: python benchmark/cases/build_cases.py
Writes  benchmark/cases/<case>/packet.md          (given to generation agents, nothing else)
        benchmark/answer_keys/<case>.md / .json   (evaluators only; never copied into a run workspace)
        benchmark/answer_keys/<case>.calc.json    (every model output the key relies on)
"""
from __future__ import annotations

import json
import pathlib

import models

HERE = pathlib.Path(__file__).resolve().parent
KEYS = HERE.parent / "answer_keys"

BANNER = ("> **Synthetic benchmark data.** The company, people, competitors and every figure in this pack are "
          "fictional. They were generated for a reasoning benchmark and are internally consistent, but they are "
          "not real market data.\n")


def M(x, d=1):
    return f"${x:,.{d}f}M"


def P(x, d=1):
    return f"{x * 100:.{d}f}%"


def D(x, d=2):
    return f"${x:,.{d}f}"


def table(head, rows):
    out = ["| " + " | ".join(head) + " |", "|" + "|".join("---" for _ in head) + "|"]
    out += ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]
    return "\n".join(out)


# ====================================================================================================
def case1():
    d = models.case1()
    am, rt = d["amazon_unit_base"], d["retail_unit"]
    S = d["scenarios"]
    packet = f"""# Onsoo Botanicals: US market entry — briefing pack

{BANNER}
## 1. Context

Onsoo Botanicals is a Seoul-based skincare company founded in 2011. FY2025 revenue was KRW 184.0 billion
(about $133M at KRW 1,380 per dollar) with an operating margin of 11.2%. Sales split: Korea 58%, Japan 24%,
Southeast Asia 18%. The best-selling product is the Rice Ferment Barrier Cream (50 ml), 31% of revenue.
Onsoo has no US entity today; since January 2026 a cross-border seller has listed three Onsoo SKUs on
Amazon US as a test.

**Decision maker:** CEO Park Ji-won, with the board, at the March 2027 board meeting.

## 2. Decision question

**Should Onsoo enter the US market in 2027, and if so, by which route?**

## 3. Objectives and constraints (set by the board)

- **Ambition:** build a US business "on the way to $40M revenue by 2030".
- **Investment cap:** cumulative US cash outflow (peak negative cumulative cash) of no more than $18M through 2030.
- **Payback:** cumulative US cash flow back to zero within four years of launch, i.e. by the end of 2030.
- **Group margin floor:** group operating margin at or above 8% in every year.
- **Bandwidth:** management can run only one major new-market launch in 2027 (the US, or a Japan scale-up).

## 4. Current views inside the company

- **CEO (initial hypothesis):** "Launch in the US in 2027 through Amazon, then add specialty beauty retail
  from 2029 once Amazon sales pass $10M and aided awareness passes 15%."
- **Independent board member (former retail executive):** "Amazon alone will never get us to $40M. A national
  specialty-retail launch in 600 doors in 2027 is how every big K-beauty brand built awareness."
- **Head of Japan:** "Japan is the safer use of 2027: we know the market and the retailers."

The planning team has modeled the Amazon-led route (Option A), the retail-led route (Option B) and a Japan
scale-up (Option J). Their inputs are below; they did not draw a conclusion.

## 5. Market data

**Table 1. US facial skincare sales, $ billions**

{table(["", "2021", "2022", "2023", "2024", "2025"],
       [["All facial skincare"] + [f"{x:.1f}" for x in d["tot_mkt"]],
        ["of which K-beauty brands"] + [f"{x:.1f}" for x in d["k_mkt"]]])}

**Table 2. Where US consumers bought K-beauty skincare, 2025, share of sales**

{table(["Channel", "Share"], [["Amazon", "41%"], ["Specialty beauty retail", "27%"], ["Mass retail", "14%"],
                             ["Brand websites (DTC)", "12%"], ["Other", "6%"]])}

## 6. Amazon pilot (January–June 2026, three SKUs, cross-border seller)

**Table 3. Pilot units sold per month**

{table(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Total"], [[f"{u:,}" for u in d["pilot_units"]] + [f"{d['pilot_total_units']:,}"]])}

- Average selling price: {D(24)} per unit. Advertising cost of sales (ACoS, Amazon ad spend as a share of
  Amazon sales) over the pilot: 28%.
- Ratings: 4.5 stars from 2,140 reviews. The most common complaint (6% of reviews): some units carried
  Korean-only label text.
- 90-day repeat purchase rate: 29% of first-time buyers. Benchmarks: 31% for skincare brands in their first
  year on Amazon US (agency data); 48% for Onsoo in Korea.

## 7. Unit economics inputs (Rice Ferment Barrier Cream, per unit)

**Table 4. Per-unit inputs by channel, US dollars**

{table(["Item", "Amazon", "Specialty retail"],
       [["Consumer price", D(24.00), D(28.00) + " (shelf)"],
        ["Price Onsoo receives", D(24.00), D(rt['wholesale']) + " (wholesale = 50% of shelf price)"],
        ["Amazon referral fee", "15% of price", "—"],
        ["Amazon fulfillment (FBA) fee", D(5.10), "—"],
        ["Ex-factory product cost", D(3.50), D(3.50)],
        ["Freight to the US warehouse or retailer DC", D(0.55), D(0.75)],
        ["US import duty", "15% of ex-factory cost", "15% of ex-factory cost"],
        ["Retailer co-op marketing allowance", "—", "8% of wholesale"],
        ["Returns and damages allowance", "—", "4% of wholesale"],
        ["Advertising", "ACoS × price", "in fixed marketing budget"]])}

The planning team applies the hero product's per-unit economics to all SKUs. Working capital: the planning team holds four months of landed product cost (ex-factory + freight + duty) as inventory.

## 8. Planning-team forecasts by option

**Table 5. Volume forecasts, units**

{table(["Option", "2027", "2028", "2029", "2030", "Key assumptions"],
       [["A · Amazon-led: Amazon units"] + [f"{u:,}" for u in d["plan_A_units"]] +
        ["Four more SKUs from 2027; ACoS 25% (planning team: ACoS falls as the brand matures)"],
        ["B · Retail-led: specialty-retail doors", "600", "600", "800", "1,000",
         "4.5 units per door per week (from the retailer's deck on successful newcomer brands)"],
        ["B · Retail-led: Amazon units"] + [f"{int(u * 1.3):,}" for u in d["plan_A_units"]] +
        ["Option A volumes × 1.3 (awareness halo from retail); ACoS 25%"]])}

**Table 6. Fixed and one-time US costs, $ millions**

{table(["Cost", "Option A", "Option B"],
       [["Compliance (MoCRA registration, safety substantiation, labeling), insurance — per year", "0.5", "0.5"],
        ["US team — per year", "0.9", "0.9"],
        ["Off-Amazon brand marketing (influencers, social) — per year", "0.7", "0.7"],
        ["National retail marketing and sampling — per year", "—", "6.0"],
        ["Field sales and merchandising team — per year", "—", "1.5"],
        ["Setup: entity, registration, labels — one-time, 2027", "0.8", "0.8"],
        ["Retailer launch fee — one-time, 2027", "—", "0.5"],
        ["In-store fixtures — one-time per new door", "—", "$1,100 per door"]])}

**Table 7. Option J · Japan scale-up instead of the US in 2027**

{table(["", "2027", "2028", "2029", "2030"],
       [["Incremental revenue, $M", "2.5", "4.5", "6.0", "7.0"],
        ["Contribution margin on that revenue", "30%", "30%", "30%", "30%"],
        ["Added fixed cost, $M per year", "0.8", "0.8", "0.8", "0.8"],
        ["One-time cost, $M", "1.0", "—", "—", "—"]])}

Japan facial skincare grows about 1.5% a year; Onsoo already holds a 3.1% share there.

**Group context.** Excluding the US, the group plans revenue of $140M (2027), $146M (2028), $152M (2029) and
$158M (2030) at an operating margin of 11.0%.

## 9. Retail evidence

**Table 8. First-year sell-through of newcomer skincare brands in US specialty beauty retail**

{table(["Brand's aided awareness among category buyers", "Median units per door per week", "Interquartile range"],
       [["Below 10%", "2.6", "1.9–3.4"], ["10–20%", "3.5", "2.8–4.3"], ["Above 20%", "4.6", "3.9–5.5"]])}

Source: a retail analytics firm, 2025, 46 brands. The leading specialty retailer reviews newcomer brands after
12 months and removes brands selling below 4.0 units per door per week.

## 10. Customer evidence

Survey, September 2026, 1,200 US women aged 18–44 who bought facial skincare in the last six months:

- Aided awareness of Onsoo: 4% of all respondents; 9% among K-beauty buyers.
- 61% of K-beauty buyers say they buy K-beauty on Amazon most often; 22% at specialty beauty retail.
- 38% of K-beauty buyers discovered their last new brand on TikTok; 17% in a store.
- 52% of respondents who tried a K-beauty product said "price compared with US brands" was a reason.

## 11. Competitor evidence

**Table 9. K-beauty brands that entered the US recently (public reporting and interviews)**

{table(["Brand", "Entry route", "Outcome by 2025"],
       [["Mooncrest", "Retail-first 2023, 450 doors", "Removed from shelves in 2025; estimated cumulative US loss $21M"],
        ["Saebom", "Amazon-first 2022", "About $30M US revenue in 2025; added 300 retail doors in 2025"],
        ["Gaon Lab", "Amazon-first 2022", "Below $5M US revenue in 2025"],
        ["Yeoreum", "Amazon-first 2023", "Below $5M US revenue in 2025"]])}

Agency benchmark: for skincare brands scaling from $5M to $20M a year on Amazon US, median ACoS is 32%
(range 26%–38%); ad costs per click rise as brands bid on broader keywords.

## 12. Other material circulated to the board

- A trade-press article (2026) reports that "the US K-beauty market reached $5.2 billion in 2025". The article's
  figure covers skincare, makeup and hair care sold by Korean brands.
- The independent board member's memo: "Across 30 K-beauty brands sold in the US, the number of specialty-retail
  doors a brand is in correlates with its Amazon sales (correlation 0.71). Retail drives Amazon sales; that is where
  the 1.3× halo in Option B comes from."

## 13. Uncertainties

- **Tariff:** the US is reviewing the duty on cosmetics imported from Korea; a rise from 15% to 25% is possible,
  with a decision expected in mid-2027.
- **Advertising cost at scale:** the pilot ran at 28% ACoS on a small budget.
- **Repeat purchase:** US repeat is below Korea's; it is unclear whether it rises with more SKUs.
- **FX:** product costs are in won; a weaker won lowers dollar costs.
"""
    rows = lambda n: "; ".join(f"{x['year']}: {x['cumulative']:+.2f}" for x in S[n]["rows"])
    key = {
        "case_id": "c1", "title": "Onsoo Botanicals — US market entry",
        "decision_question": "Should Onsoo enter the US market in 2027, and if so, by which route?",
        "initial_hypothesis": {
            "holder": "CEO",
            "statement": "Enter the US in 2027 through an Amazon-led launch; add specialty retail from 2029 once proven.",
            "expected_handling": "keep_with_conditions",
            "explanation": ("The evidence supports the CEO's route over the retail-led route, which breaks the investment cap "
                            "and the group-margin floor. But Option A meets the four-year payback only if ACoS stays below "
                            f"about {P(d['breakeven_acos_payback_2030'])} — barely above the pilot's 28% and below the 32% "
                            "scaling benchmark — and it reaches about $26M, not $40M, by 2030. A good answer keeps the "
                            "hypothesis but adds gates and resets the $40M ambition; abandoning the US altogether is defensible "
                            "only if argued from the payback risk, and adopting the retail-led route is not defensible."),
        },
        "key_insights": [
            {"id": "K1", "critical": True, "text": f"Amazon unit contribution before advertising is {D(am['pre_ad'])} ({P(am['pre_ad']/24)} of price); after ads at the pilot's 28% ACoS it is {D(am['contribution'])} per unit. Retail contribution is {D(rt['contribution'])} per unit before the large fixed retail costs."},
            {"id": "K2", "critical": True, "text": f"Option B (retail-led) needs peak cumulative investment of about {M(S['B_plan_4.5_upd']['peak_investment'])} even on the planning team's own 4.5 units/door/week (about {M(S['B_benchmark_2.6_upd']['peak_investment'])} at the 2.6 newcomer median), above the $18M cap, never pays back by 2030, and pushes group operating margin to about {P(S['B_plan_4.5_upd']['group_margin'][0])} in 2027, below the 8% floor."},
            {"id": "K3", "critical": True, "text": f"The 4.5 units/door/week assumption is the 'above 20% awareness' benchmark; Onsoo's awareness is 4% (9% among K-beauty buyers), where the median is 2.6 — below the retailer's 4.0 delisting threshold. Mooncrest's exit illustrates the risk."},
            {"id": "K4", "critical": True, "text": f"Option A at the planning ACoS of 25% pays back in 2030 (cumulative {M(S['A_plan_acos25']['cum_2030'],2)}); at the pilot's 28% it only just pays back ({M(S['A_pilot_acos28']['cum_2030'],2)}); at the 32% scaling benchmark it does not ({M(S['A_benchmark_acos32']['cum_2030'],2)}). Break-even ACoS for payback by 2030 is about {P(d['breakeven_acos_payback_2030'])}. A tariff rise to 25% alone turns the pilot case negative ({M(S['A_acos28_tariff25']['cum_2030'],2)})."},
            {"id": "K5", "critical": True, "text": f"No option meets both the $40M ambition and the constraints: A reaches about {M(S['A_pilot_acos28']['rev_2030'])} of 2030 revenue; B reaches about {M(S['B_plan_4.5_upd']['rev_2030'])} but breaks the cap. The board has to trade the ambition against the constraints."},
            {"id": "K6", "critical": False, "text": f"Peak investment for A is small ({M(S['A_pilot_acos28']['peak_investment'])} at 28% ACoS; {M(S['A_downside_acos32_tariff25']['peak_investment'])} in the combined downside), so the downside of trying A is bounded; group margin stays above 9%."},
            {"id": "K7", "critical": False, "text": f"Option J (Japan) pays back in 2029 with cumulative {M(S['J_japan']['cum_2030'])} by 2030 and lower risk, but it is a small, slow-growing market (1.5% a year; Onsoo already holds 3.1%). It is a credible alternative for 2027 given the one-launch bandwidth constraint."},
            {"id": "K8", "critical": False, "text": f"The pilot is not a novelty spike: monthly units nearly doubled (7,400 to 14,000; June run-rate about {d['june_run_rate_annual_units']:,} units a year), 4.5 stars, and repeat of 29% is close to the 31% newcomer benchmark — but below Korea's 48%, so Korean repeat rates should not be assumed."},
        ],
        "required_calculations": [
            {"id": "Q1", "text": "Amazon per-unit contribution before and after advertising", "expected": f"{D(am['pre_ad'])} before ads; {D(am['contribution'])} after ads at 28% ACoS", "tolerance": "±$0.10"},
            {"id": "Q2", "text": "Retail per-unit contribution", "expected": D(rt['contribution']), "tolerance": "±$0.10"},
            {"id": "Q3", "text": "Option B cumulative cash / peak investment vs the $18M cap", "expected": f"peak about {M(S['B_plan_4.5_upd']['peak_investment'])} on plan assumptions", "tolerance": "any estimate clearly above $18M"},
            {"id": "Q4", "text": "Option A payback / cumulative cash by 2030, with sensitivity to ACoS (and ideally tariff)", "expected": f"25%: {M(S['A_plan_acos25']['cum_2030'],2)}; 28%: {M(S['A_pilot_acos28']['cum_2030'],2)}; 32%: {M(S['A_benchmark_acos32']['cum_2030'],2)}", "tolerance": "±$0.5M; the qualitative pattern (payback only below ~28–29% ACoS) matters more than exact values"},
            {"id": "Q5", "text": "Group operating margin check for Option B in 2027", "expected": P(S['B_plan_4.5_upd']['group_margin'][0]), "tolerance": "any calculation showing it is below 8%"},
            {"id": "Q6", "text": "K-beauty US market growth", "expected": f"CAGR 2021–25 {P(d['kbeauty_cagr_21_25'])}, against {P(d['total_cagr_21_25'])} for all facial skincare; K-beauty share {P(d['kbeauty_share_2025'])} in 2025", "tolerance": "±0.5 pp"},
        ],
        "decision_relevant_evidence": [
            {"id": "E1", "critical": True, "text": "Investment cap $18M, payback by end-2030, group margin ≥ 8%, one launch in 2027"},
            {"id": "E2", "critical": True, "text": "Onsoo aided awareness 4% (9% among K-beauty buyers) vs sell-through benchmarks by awareness band"},
            {"id": "E3", "critical": True, "text": "Retailer delists below 4.0 units per door per week after 12 months"},
            {"id": "E4", "critical": True, "text": "Agency ACoS benchmark for scaling brands: median 32% vs planning assumption 25% and pilot 28%"},
            {"id": "E5", "critical": False, "text": "Possible tariff increase from 15% to 25%"},
            {"id": "E6", "critical": False, "text": "61% of K-beauty buyers buy on Amazon most often; 38% discover on TikTok"},
            {"id": "E7", "critical": False, "text": "Competitor histories (Mooncrest loss; Saebom success but two Amazon-first brands stalled below $5M)"},
            {"id": "E8", "critical": False, "text": "Label complaint (Korean-only text) — a compliance and conversion fix before scaling"},
        ],
        "contradictory_evidence": [
            "The planning team's 25% ACoS vs the 32% scaling benchmark",
            "The retailer's 4.5 units/door/week vs the 2.6 median at Onsoo's awareness",
            "The $40M ambition vs the investment cap and margin floor",
            "Saebom's success vs Gaon Lab and Yeoreum stalling (survivorship bias)",
        ],
        "reasoning_traps": [
            {"id": "T1", "text": "Sizing from the market (\"K-beauty is $3.6B growing 17%; 1% share is $36M\") instead of from channel economics"},
            {"id": "T2", "text": "Accepting the 4.5 units/door/week or the 25% ACoS assumptions without checking them against the benchmarks"},
            {"id": "T3", "text": "Using Saebom as proof that Amazon-first works (ignoring the two stalled brands) or Mooncrest as proof retail never works"},
            {"id": "T4", "text": "Assuming Korean repeat rates (48%) or treating the pilot growth rate as permanent"},
            {"id": "T5", "text": "Recommending retail-led to meet the $40M ambition while ignoring that it breaks the cap and the margin floor"},
        ],
        "key_tradeoffs": [
            {"id": "X1", "text": "Ambition ($40M by 2030) vs investment cap, payback and margin floor"},
            {"id": "X2", "text": "Speed/awareness of retail vs capital risk and delisting risk"},
            {"id": "X3", "text": "US upside vs the safer, smaller Japan scale-up (one launch only in 2027)"},
            {"id": "X4", "text": "Advertising intensity (growth) vs contribution and payback"},
        ],
        "plausible_recommendations": [
            {"id": "R1", "defensible": "yes", "text": "Enter through Amazon in 2027 with explicit gates (e.g. ACoS ≤ ~28%, repeat ≥ ~30%, label fix, tariff watch); add retail only when awareness supports ≥ 4 units/door/week; reset the $40M ambition or accept a later date."},
            {"id": "R2", "defensible": "conditional", "text": "Prioritise the Japan scale-up in 2027 and keep the cross-border Amazon listing as a low-cost US test — defensible if argued from payback risk and the one-launch constraint, with a clear trigger for a US launch later."},
            {"id": "R3", "defensible": "conditional", "text": "Amazon-led entry with a lower fixed-cost base (smaller team, slower brand spend) to protect payback — defensible if numbers are shown."},
            {"id": "R4", "defensible": "no", "text": "National specialty-retail launch in 2027 (Option B)."},
            {"id": "R5", "defensible": "no", "text": "Enter the US 'because the market is large and growing' without channel economics."},
        ],
        "defensibility_criteria": [
            "Compares the options on the board's own constraints (cap, payback, margin floor), not only on revenue",
            "Tests the planning assumptions (ACoS, units per door) against the benchmarks in the pack",
            "States what has to be true for the chosen route to pay back, and what would trigger a change",
            "Acknowledges that the $40M ambition is not reachable within the constraints on the evidence given",
        ],
    }
    key["key_insights"].append({"id": "K9", "critical": False, "text": "The 1.3× Amazon halo in Option B rests on a cross-brand correlation (0.71) that does not show retail causes Amazon sales: brands that are already successful win more doors (reverse causality / confounding). Without the halo, Option B is even worse."})
    key["reasoning_traps"] += [{"id": "T6", "text": "Accepting the board member's correlation as proof that retail drives Amazon sales (the 1.3× halo)"},
                               {"id": "T7", "text": "Using the trade-press $5.2B (skincare + makeup + hair care) as the skincare market"}]
    key["decision_relevant_evidence"].append({"id": "E9", "critical": False, "text": "Definition of the $5.2B trade-press figure vs Table 1 skincare-only $3.6B"})
    key["contradictory_evidence"].append("Board member's correlation memo vs what a correlation across brands can show")
    calcs = {k: v for k, v in d.items()}
    calcs["scenario_cumulative_text"] = {n: rows(n) for n in S}
    return packet, key, calcs


# ====================================================================================================
def case2():
    d = models.case2()
    p = d["pnl"]
    b = d["bridge"]
    t = d["tail"]
    yrs = [2023, 2024, 2025]
    packet = f"""# Harlow Fresh Markets: reversing the margin decline — briefing pack

{BANNER}
## 1. Context

Harlow Fresh Markets is a family-controlled grocery chain with 58 stores in Ohio and Indiana and a home-delivery
and click-and-collect service launched in 2021. Sales grew from $1.42 billion in FY2023 to $1.50 billion in
FY2025, but operating income fell by more than half.

**Decision maker:** CEO Dana Whitfield, presenting a margin plan to the board in February 2027.

## 2. Decision question

**How should Harlow reverse its declining operating margin, and which actions should it take first?**

## 3. Objectives and constraints

- **Target:** operating margin back to at least 3.0% by FY2028.
- **Capital:** at most $25M of one-time cost or capital for the plan over FY2026–FY2028.
- **Commitments:** no closure of a store whose lease runs beyond 2027 without a board vote; the family
  owners want to keep the delivery service in some form ("our customers expect it").
- The plan must be credible to the chain's lender: a covenant requires operating income of at least $20M in FY2026.

## 4. Management's current view

The CFO and COO believe **wage inflation is the main cause** of the decline ("the state minimum wage and a tight
labor market have pushed our hourly rate up more than 9% in two years"). Their draft plan: cut scheduled store
labor hours by 8% in FY2026 (they estimate about $14.5M a year of savings) and freeze the e-commerce service at
its current size.

## 5. Financials

**Table 1. Income statement, $ millions (fiscal years end in January)**

{table(["", "FY2023", "FY2024", "FY2025"],
       [["Sales"] + [f"{p[y]['sales']:,.1f}" for y in yrs],
        ["Gross profit"] + [f"{p[y]['gross_profit']:,.1f}" for y in yrs],
        ["Store labor"] + [f"{p[y]['labor']:,.1f}" for y in yrs],
        ["Occupancy and energy"] + [f"{p[y]['occupancy']:,.1f}" for y in yrs],
        ["E-commerce fulfillment (picking + delivery, net of delivery fees)"] + [f"{p[y]['ecom_fulfillment_net']:,.1f}" for y in yrs],
        ["Other SG&A"] + [f"{p[y]['other_sga']:,.1f}" for y in yrs],
        ["**Operating income**"] + [f"**{p[y]['operating_income']:,.1f}**" for y in yrs],
        ["Operating margin"] + [P(p[y]['operating_margin'], 2) for y in yrs]])}

Gross profit is after shrink (losses from waste, theft and errors). E-commerce sales are included in sales and gross profit.

**Table 2. Gross-margin drivers**

{table(["", "FY2023", "FY2024", "FY2025"],
       [["Promotional sales, share of sales"] + [P(d['promo_share'][y]) for y in yrs],
        ["Private-label sales, share of sales"] + [P(d['pl_share'][y]) for y in yrs],
        ["Shrink, % of sales"] + [P(d['shrink'][y]) for y in yrs]])}

- Promotional sales earn 14 percentage points less gross margin than regular-price sales (unchanged over the period).
- Private-label sales earn 12 percentage points more gross margin than national brands (unchanged).
- Vendor funding covered 55% of promotional markdowns in FY2023 and 46% in FY2025.
- A post-event review of FY2025 promotions found that 38% of events lost money after counting the extra units
  they sold.

## 6. Store labor

**Table 3. Store labor**

{table(["", "FY2023", "FY2025"],
       [["Average hourly wage incl. benefits", "$16.80", "$18.38"],
        ["Labor hours per $1,000 of sales", "7.02", "6.60"],
        ["Store labor, % of sales", P(d['labor'][2023]), P(d['labor'][2025])]])}

**Table 4. Shrink by store labor intensity, FY2025 (stores ranked by labor hours per $1,000 of sales)**

{table(["Quartile", "Shrink, % of sales"], [[k, P(v)] for k, v in d["shrink_by_labor_quartile"].items()])}

Shrink composition FY2025: fresh and produce waste 45%, theft 35%, administrative and receiving errors 20%.
Store managers in the lowest-labor quartile say produce rotation and receiving checks are skipped on busy days.

## 7. E-commerce

**Table 5. E-commerce operating data**

{table(["", "FY2023", "FY2024", "FY2025"],
       [["E-commerce share of sales"] + [P(d['ecom_share'][y]) for y in yrs],
        ["Orders, thousands"] + [f"{p[y]['ecom_orders']/1e3:,.0f}" for y in yrs],
        ["Average basket"] + [D(d['basket'][y], 0) for y in yrs],
        ["Share of orders delivered to the home (rest: click-and-collect)"] + [P(d['delivery_share'][y], 0) for y in yrs],
        ["Picking cost per order (all orders)"] + [D(d['picking'][y]) for y in yrs],
        ["Third-party delivery cost per delivered order"] + [D(d['delivery_cost'][y]) for y in yrs],
        ["Average delivery fee collected per delivered order"] + [D(d['fee_collected'][y]) for y in yrs]])}

- Delivery is free above $75 (a $4.99 fee below). Click-and-collect is free.
- Survey of 2,300 e-commerce customers (FY2025): 70% of what they buy online they say they would otherwise have
  bought in a Harlow store.
- Finance estimates that a dollar of sales that is genuinely new to Harlow adds about 20 cents of contribution
  (gross margin less variable store costs), before e-commerce fulfillment.
- **Fee test** (4 stores, 10 weeks, late FY2025): delivery fee raised to $7.99 and the free-delivery threshold to
  $100. Delivered orders fell 9%, click-and-collect orders rose 14%, total e-commerce sales fell 2%, and the
  average fee collected per delivered order rose to $6.40.

## 8. Store portfolio

**Table 6. The nine weakest stores, FY2025**

{table(["", "Value"],
       [["Stores with negative four-wall EBITDA", "9 of 58"],
        ["Their combined sales", "$118.0M"],
        ["Their combined four-wall EBITDA", "−$3.1M"],
        ["Leases expiring by end of 2027", "6 of the 9"],
        ["Estimated lease-exit cost for the other 3", "$7.5M (one-time)"],
        ["Share of their sales expected to move to a nearby Harlow store if closed (past closures)", "25%"],
        ["Contribution on sales moved to a receiving store", "12%"]])}

## 9. Customers and competitors

- A discount grocer, ValuMart, has opened 11 stores in Harlow trade areas since 2023. Harlow stores within three
  miles of a new ValuMart had comparable sales of −4.2% in FY2025, against +1.1% for other Harlow stores.
- Customer survey (n = 3,100): 41% say Harlow is "more expensive than other options" (FY2023: 33%); top reasons
  to shop Harlow are fresh produce (58%) and convenience (44%).
- Category managers say they raised promotional depth in FY2024–FY2025 "to defend traffic against ValuMart".

## 10. Other material circulated to the board

- **E-commerce team update:** "E-commerce is profitable: a contribution margin of 6.1% of e-commerce sales in FY2025."
  Their calculation takes the gross margin on all e-commerce sales and deducts picking, packaging and an allocation
  of store variable costs. Third-party delivery is not in it (finance books it in "E-commerce fulfillment"), and it
  treats every e-commerce sale as new to Harlow.
- **Category team:** "Stores with the deepest promotions in FY2025 grew comparable sales 1.8%, against 0.2% for the
  rest. Promotions work."

## 11. Uncertainties

- How much of the promotional increase is needed to hold traffic against ValuMart.
- Whether third-party delivery rates can be renegotiated (contract renews in 2026; the provider proposed a 3% rise).
- Wage rates: the state minimum wage rises again in 2027 (+4%).
- How customers would respond to labor-hour cuts (checkout waits, stock-outs).
"""
    lab_cut = 0.08 * p[2025]["labor"]
    key = {
        "case_id": "c2", "title": "Harlow Fresh Markets — reversing the margin decline",
        "decision_question": "How should Harlow reverse its declining operating margin, and which actions should it take first?",
        "initial_hypothesis": {
            "holder": "CFO and COO",
            "statement": "Wage inflation is the main cause; cut store labor hours 8% and freeze e-commerce.",
            "expected_handling": "revise",
            "explanation": (f"Store labor explains only about {M(-b['store_labor'])} of the {M(-b['total'])} decline in operating income "
                            f"(FY2023→FY2025). The largest drivers are e-commerce fulfillment ({M(-b['ecommerce_fulfillment'])}), "
                            f"promotions ({M(-b['promotions'])}) and shrink ({M(-b['shrink'])}). Wage rates rose but hours per $1,000 of sales fell, "
                            "and low-labor stores show the highest shrink, so an 8% hours cut risks raising shrink. Freezing e-commerce "
                            "leaves a loss-making service as it is. A good answer revises the diagnosis."),
        },
        "key_insights": [
            {"id": "K1", "critical": True, "text": f"Operating income fell from {M(p[2023]['operating_income'])} to {M(p[2025]['operating_income'])} (margin {P(p[2023]['operating_margin'],2)} → {P(p[2025]['operating_margin'],2)})."},
            {"id": "K2", "critical": True, "text": f"Bridge FY2023→FY2025 (at FY2025 sales): sales growth +{M(b['sales_growth_at_2023_margin'])}; e-commerce fulfillment {M(b['ecommerce_fulfillment'])}; promotions {M(b['promotions'])}; shrink {M(b['shrink'])}; store labor {M(b['store_labor'])}; occupancy/energy {M(b['occupancy_energy'])}; private label +{M(b['private_label'])}. Labor is about {P(b['store_labor']/b['total'],0)} of the decline."},
            {"id": "K3", "critical": True, "text": f"E-commerce loses money: net fulfillment cost {M(p[2025]['ecom_fulfillment_net'])} in FY2025 ({D(p[2025]['ecom_net_cost_per_order'])} per order) against only about {M(p[2025]['ecom_sales']*0.3*0.2)} of contribution on the 30% of e-commerce sales that are incremental: a net drag of about {M(-d['ecom_incremental_contrib'])} a year."},
            {"id": "K4", "critical": True, "text": "The fee test shows a lever: higher fee and threshold cut delivered orders 9% but raised fee per delivered order from $3.10 to $6.40 and shifted orders to click-and-collect, at a 2% loss of e-commerce sales (mostly cannibalised anyway)."},
            {"id": "K5", "critical": True, "text": f"Labor cuts conflict with shrink: lowest-labor quartile has shrink of 3.1% vs 2.3% in the highest; an 8% hours cut (~{M(lab_cut)}) could be partly offset by higher shrink (each 0.1 pp of shrink is about {M(0.001*p[2025]['sales'])})."},
            {"id": "K6", "critical": False, "text": "Promotional growth is partly a competitive response to ValuMart (−4.2% comps near new stores), and vendor funding fell; 38% of events lose money — cut the losing events rather than all promotions."},
            {"id": "K7", "critical": False, "text": f"Closing the nine weakest stores at lease expiry improves operating income by about {M(t['closure_gain_annual'])} a year when all nine are closed (removing −$3.1M EBITDA plus 25% × $118M × 12% transferred), but three need a $7.5M exit cost and a board vote."},
            {"id": "K8", "critical": False, "text": f"Target: 3.0% of ~$1.5B sales needs roughly $45M operating income, about $30M more than FY2025; the plan must add up to that within $25M one-time cost and protect the $20M FY2026 covenant."},
        ],
        "required_calculations": [
            {"id": "Q1", "text": "Operating margin by year", "expected": " → ".join(P(p[y]['operating_margin'], 2) for y in yrs), "tolerance": "±0.05 pp"},
            {"id": "Q2", "text": "Margin/operating-income bridge by driver", "expected": "; ".join(f"{k}: {v:+.1f}" for k, v in b.items() if k != 'check_residual'), "tolerance": "each driver ±$1M; ranking must be right (e-com, promo, shrink > labor)"},
            {"id": "Q3", "text": "E-commerce net cost per order and economics", "expected": f"{D(p[2025]['ecom_net_cost_per_order'])} per order; net drag ≈ {M(-d['ecom_incremental_contrib'])}", "tolerance": "±$0.5 per order; drag $8–12M"},
            {"id": "Q4", "text": "Size of the 3.0% target gap", "expected": f"≈ {M(0.03*p[2025]['sales'] - p[2025]['operating_income'])} more operating income at FY2025 sales", "tolerance": "±$3M"},
            {"id": "Q5", "text": "Store closure impact", "expected": M(t['closure_gain_annual']), "tolerance": "±$1M"},
        ],
        "decision_relevant_evidence": [
            {"id": "E1", "critical": True, "text": "Income statement lines showing which costs grew as a share of sales"},
            {"id": "E2", "critical": True, "text": "E-commerce per-order costs, fees and 70% cannibalisation"},
            {"id": "E3", "critical": True, "text": "Shrink by labor-hours quartile"},
            {"id": "E4", "critical": True, "text": "Promotional share, 14 pp margin gap, vendor funding fall, 38% losing events"},
            {"id": "E5", "critical": False, "text": "Fee test results"},
            {"id": "E6", "critical": False, "text": "ValuMart competitive pressure and price perception"},
            {"id": "E7", "critical": False, "text": "Weak-store data and lease expiries"},
            {"id": "E8", "critical": False, "text": "Covenant ($20M FY2026) and $25M one-time budget"},
        ],
        "contradictory_evidence": [
            "Hourly wages rose 9.4%, yet labor as a share of sales rose only 0.3 pp because hours per $1,000 fell",
            "Promotions hurt margin but defend traffic against ValuMart",
            "Owners want to keep delivery, but it loses money",
        ],
        "reasoning_traps": [
            {"id": "T1", "text": "Accepting 'wage inflation is the main cause' because the hourly wage rose 9%"},
            {"id": "T2", "text": "Treating e-commerce sales growth as success without counting cannibalisation and fulfillment cost"},
            {"id": "T3", "text": "Recommending deep labor cuts without considering shrink and service effects"},
            {"id": "T4", "text": "Cutting all promotions without considering the competitive response"},
            {"id": "T5", "text": "A list of levers without sizing that does not add up to the 3.0% target"},
        ],
        "key_tradeoffs": [
            {"id": "X1", "text": "Labor savings vs shrink and service"},
            {"id": "X2", "text": "Promotional margin vs traffic defence against ValuMart"},
            {"id": "X3", "text": "Keeping delivery (owners) vs its economics — reprice/redesign rather than freeze or kill"},
            {"id": "X4", "text": "Store closures (savings) vs lease-exit cost and the board-vote commitment"},
        ],
        "plausible_recommendations": [
            {"id": "R1", "defensible": "yes", "text": "Sized plan led by e-commerce redesign (fees/threshold, shift to click-and-collect, renegotiate delivery), shrink reduction, promotional pruning of losing events and private-label growth, with weak-store closures at lease expiry; labor productivity only where it does not raise shrink."},
            {"id": "R2", "defensible": "conditional", "text": "Plan that includes some labor-hour reduction — defensible if targeted (e.g. scheduling, self-checkout) and the shrink risk is acknowledged and sized."},
            {"id": "R3", "defensible": "conditional", "text": "Exit home delivery and keep click-and-collect — defensible with the economics, if the owners' commitment is addressed."},
            {"id": "R4", "defensible": "no", "text": "The management plan as written (8% hours cut + e-commerce freeze) as the main answer."},
        ],
        "defensibility_criteria": [
            "Diagnosis rests on a quantified bridge, not on the most visible cost",
            "Actions are sized and add up (roughly) to the 3.0% target, with the covenant in view",
            "Second-order effects (shrink from labor cuts, traffic from promo cuts) are acknowledged",
        ],
    }
    ec = d["ecom_claim"]
    key["key_insights"].append({"id": "K9", "critical": False, "text": f"The e-commerce team's 6.1% (≈{M(ec['claimed_contribution'])}) leaves out third-party delivery (≈{M(ec['delivery_net_cost'])} net of fees) and cannibalisation; with delivery alone it is ≈{M(ec['after_delivery'])}, and counting only incremental sales the service is a ≈$10M drag."})
    key["reasoning_traps"] += [{"id": "T6", "text": "Accepting the e-commerce team's '6.1% contribution margin' claim"},
                               {"id": "T7", "text": "Reading 'stores with deeper promotions grew faster' as proof that promotions pay (no control for store mix; the post-event review says 38% of events lose money)"}]
    key["contradictory_evidence"].append("E-commerce team's 6.1% margin vs the fulfillment line and cannibalisation")
    return packet, key, d


# ====================================================================================================
def case3():
    d = models.case3()
    b = d["beta"]
    packet = f"""# Brightwork: should we launch an AI dispatch assistant? — briefing pack

{BANNER}
## 1. Context

Brightwork sells field-service management software (scheduling, dispatch, quotes, invoicing) to HVAC,
plumbing and electrical contractors with 3–50 technicians. It has 9,800 customer accounts with an average of
6.2 office seats each (dispatchers and office staff) on the Core plan at $79 per seat per month: annual recurring
revenue (ARR) of {M(d['arr'])}. Gross margin is 78%, annual logo churn 14%, net revenue retention 101%.

The product team has built **Dispatch Copilot**: AI that proposes a day's schedule, drafts quotes from
technician notes, and summarises customer calls. It ran as a free beta for 12 weeks.

**Decision maker:** CEO Maya Okafor and the executive team, at January 2027 planning.

## 2. Decision question

**Should Brightwork launch Dispatch Copilot in Q2 2027, and if so, how should it be packaged and priced?**

## 3. Objectives and constraints

- Raise net revenue retention from 101% to 105% by 2028.
- Keep company gross margin at or above 75%.
- Engineering: 60 engineers in total. Launching Copilot needs 14 engineers for two quarters, which delays the
  rewrite of the technician mobile app by two quarters.

## 4. Current view inside the company

The Chief Product Officer proposes launching Copilot as a **paid add-on at $149 per account per month**: "Our
survey shows 46% of customers are likely to buy it. That is about $8M of new ARR in the first year."
The Head of Customer Success worries about the mobile app delay: "Mobile reliability is what customers complain
about."

## 5. Beta results (240 accounts, 12 weeks, volunteers)

**Table 1. Beta outcomes**

{table(["Measure", "Beta accounts", "Matched non-beta accounts"],
       [["Self-reported dispatcher hours saved per week", f"{b['self_reported_hours_saved']}", "—"],
        ["Change in jobs scheduled per dispatcher-hour vs the prior 12 weeks", "+11%", "+2%"],
        ["90-day renewal rate", "97%", "93%"]])}

- Beta accounts volunteered; they are larger (8.1 seats on average) and more active than the base.
- Usage is concentrated: the top 10% of beta accounts generated 58% of all AI requests.

**Table 2. AI requests per account per month (beta)**

{table(["", "Requests per month"],
       [["Median account", f"{d['req']['median']:,}"], ["Mean account", f"{d['req']['mean']:,}"],
        ["Mean of the top 10% of accounts", f"{d['req']['top_decile_mean']:,}"]])}

- Model inference cost: $0.009 per request under the current provider contract, fixed through December 2027.
  The provider's list prices fell 35% over the past 12 months.
- Running the feature also needs about $0.6M a year of platform, evaluation and support cost.

## 6. Pricing evidence

- **Survey** (October 2026, 610 customer admins): at $149 per account per month, 46% said they were "likely" or
  "very likely" to buy Copilot.
- **Paywall test** (last four weeks of the beta): 120 beta accounts were offered Copilot at $149 per account per
  month after the free period. 17 accounts (14%) bought it. Accounts that bought averaged 6,800 requests a month.
- **Tier option:** a new "Pro" plan that includes Copilot, priced $12 more per seat per month than Core. When
  Brightwork last launched a higher tier (2023), 33% of accounts moved to it within a year.

## 7. Competitor evidence

- **Routewise**, the closest competitor, launched AI scheduling **included in its Pro plan** in September 2026.
- Brightwork's win rate in deals where Routewise competed fell from 44% (Q1–Q2 2026) to 37% (Q3 2026).
  Brightwork has about 2,600 qualified new-customer opportunities a year, and Routewise competes in about 60% of
  them; a new account averages 6.2 seats on Core.
- In Q3 2026 lost deals, 31% of loss notes mention AI features.

## 8. Customer evidence

**Table 3. Main reason given by accounts that churned, 2026 (n = 1,190)**

{table(["Reason", "Share"], [[k, P(v, 0)] for k, v in d["exit_reasons"].items()])}

- Top feature request in the 2026 customer survey: "a reliable technician mobile app" (38% rank it first);
  AI scheduling is ranked first by 19%.

## 9. Costs

- Engineering: 14 engineers for two quarters at a fully loaded $210,000 per engineer-year.

## 10. Other material

- **VP Sales memo:** "31% of our lost deals cite AI, so Copilot would recover about a third of the deals we lose to
  Routewise."
- **Survey method note:** the October survey went to all 9,800 account admins; 610 replied (6%). Respondents average
  9.4 seats, against 6.2 for all accounts.

## 11. Uncertainties

- Whether the productivity gain holds beyond volunteers.
- How fast inference prices fall after 2027.
- Whether Routewise's AI is the cause of the lower win rate or coincides with its price promotion in Q3 2026
  (Routewise also offered 20% off the first year in Q3).
"""
    key = {
        "case_id": "c3", "title": "Brightwork — AI dispatch assistant",
        "decision_question": "Should Brightwork launch Dispatch Copilot in Q2 2027, and if so, how should it be packaged and priced?",
        "initial_hypothesis": {
            "holder": "Chief Product Officer",
            "statement": "Launch as a paid add-on at $149 per account per month; survey implies ~$8M new ARR in year one.",
            "expected_handling": "revise",
            "explanation": (f"Launching is supported (competitive defence, productivity signal), but the revenue case is not: the survey's 46% "
                            f"gives {M(d['survey_arr'])}, while the paywall test's 14% gives about {M(d['revealed_arr'])}, and buyers are heavy users "
                            f"(6,800 requests/month → add-on gross margin about {P(d['addon_gm_adopter'],0)}). A good answer keeps 'launch' but revises "
                            "the packaging/sizing, or argues a delay with the mobile-app trade-off explicitly."),
        },
        "key_insights": [
            {"id": "K1", "critical": True, "text": f"Stated vs revealed preference: 46% survey intent → {M(d['survey_arr'])} ARR; 14% paywall conversion → about {M(d['revealed_arr'])} ARR. The $8M claim overstates by roughly 3x."},
            {"id": "K2", "critical": True, "text": f"Inference cost scales with usage: mean account ${d['cost']['mean']:.0f}/month, top-decile ${d['cost']['top_decile_mean']:.0f}/month against a $149 price (gross margin {P(d['addon_gm_top'],0)} for the top decile). Paying adopters average 6,800 requests → about ${6800*0.009:.0f}/month, {P(d['addon_gm_adopter'],0)} gross margin; add-on inference cost ≈ {M(d['revealed_inference'])} a year at 14% adoption."},
            {"id": "K3", "critical": True, "text": f"The strategic case is defensive: win rate vs Routewise fell 44% → 37%, about {d['lost_wins']:.0f} fewer wins a year ≈ {M(d['lost_new_arr'],2)} of new ARR a year; 31% of loss notes cite AI. But Routewise also discounted 20% in Q3, so the AI effect is uncertain."},
            {"id": "K4", "critical": True, "text": "Trade-off with the mobile app: mobile reliability is the top churn reason (27%) and top request (38%); AI is a churn reason for only 6%. Delaying mobile by two quarters has a retention cost that must be weighed."},
            {"id": "K5", "critical": False, "text": f"Pro tier (+$12/seat): ≈ {M(d['pro_arr'],2)} ARR at 33% migration with ≈ {M(d['pro_inference'],2)} inference cost (gross margin ≈ {P(d['pro_gm'],0)}); needs usage caps or metering to protect the 75% company margin."},
            {"id": "K6", "critical": False, "text": "Beta results are biased (volunteers, larger, more active): +9 pp net productivity and 97% vs 93% renewal are encouraging but not proof."},
            {"id": "K7", "critical": False, "text": f"Engineering cost ≈ {M(d['eng_cost'],2)} plus $0.6M/year run cost — small relative to ARR; the real cost is the mobile delay."},
        ],
        "required_calculations": [
            {"id": "Q1", "text": "Survey-based vs test-based add-on ARR", "expected": f"{M(d['survey_arr'],2)} vs {M(d['revealed_arr'],2)}", "tolerance": "±$0.2M"},
            {"id": "Q2", "text": "Inference cost and gross margin per account at mean/top-decile/adopter usage", "expected": f"${d['cost']['mean']:.1f} / ${d['cost']['top_decile_mean']:.1f} / ${6800*0.009:.1f} per month", "tolerance": "±$2"},
            {"id": "Q3", "text": "Competitive impact of the lower win rate", "expected": f"≈ {d['lost_wins']:.0f} wins ≈ {M(d['lost_new_arr'],2)} new ARR a year", "tolerance": "±20%"},
            {"id": "Q4", "text": "Pro-tier revenue and margin", "expected": f"{M(d['pro_arr'],2)} ARR, ≈{P(d['pro_gm'],0)} gross margin", "tolerance": "±$0.3M; ±5 pp"},
        ],
        "decision_relevant_evidence": [
            {"id": "E1", "critical": True, "text": "Paywall test: 14% conversion, buyers average 6,800 requests"},
            {"id": "E2", "critical": True, "text": "Inference cost per request and usage concentration"},
            {"id": "E3", "critical": True, "text": "Win rate vs Routewise 44% → 37% and Routewise's bundling"},
            {"id": "E4", "critical": True, "text": "Churn reasons: mobile 27% vs AI 6%; mobile app delay"},
            {"id": "E5", "critical": False, "text": "Routewise's 20% first-year discount as an alternative explanation"},
            {"id": "E6", "critical": False, "text": "Beta selection bias (volunteers, larger accounts)"},
            {"id": "E7", "critical": False, "text": "Inference price trend (−35% in 12 months) and fixed contract to Dec 2027"},
        ],
        "contradictory_evidence": [
            "Survey 46% vs paywall 14%",
            "Competitive pressure on AI vs customers' stated priority (mobile app)",
            "Beta productivity gains vs selection bias",
            "Win-rate drop: AI vs Routewise's simultaneous discount",
        ],
        "reasoning_traps": [
            {"id": "T1", "text": "Sizing revenue from stated survey intent"},
            {"id": "T2", "text": "Ignoring variable inference cost (treating AI as zero marginal cost SaaS)"},
            {"id": "T3", "text": "Attributing the whole win-rate drop to AI"},
            {"id": "T4", "text": "Treating volunteer beta results as representative"},
            {"id": "T5", "text": "Ignoring the opportunity cost of delaying the mobile app"},
        ],
        "key_tradeoffs": [
            {"id": "X1", "text": "Monetise (add-on revenue) vs defend (bundle to protect win rate/retention)"},
            {"id": "X2", "text": "Copilot now vs mobile app reliability (the top churn driver)"},
            {"id": "X3", "text": "Adoption vs gross margin (usage caps / metering)"},
        ],
        "plausible_recommendations": [
            {"id": "R1", "defensible": "yes", "text": "Launch, packaged in a Pro tier (or included with a usage cap/metering), sized off the paywall test, with gross-margin guardrails; sequence or staff so the mobile app is not delayed, or accept the delay explicitly."},
            {"id": "R2", "defensible": "yes", "text": "Launch as an add-on at a lower entry price plus usage-based pricing, sized off the 14% test, framed as defensive."},
            {"id": "R3", "defensible": "conditional", "text": "Delay Copilot two quarters to ship the mobile app first — defensible if the win-rate risk is quantified and a limited AI response is planned."},
            {"id": "R4", "defensible": "no", "text": "Launch the $149 add-on on the strength of the $8M survey-based forecast."},
        ],
        "defensibility_criteria": [
            "Uses revealed (test) rather than stated (survey) demand, or explains the gap",
            "Accounts for variable inference cost in pricing/packaging",
            "Weighs the mobile-app delay against the competitive AI threat",
        ],
    }
    key["key_insights"].append({"id": "K8", "critical": False, "text": "The survey is weaker than it looks: a 6% response rate from larger accounts (9.4 vs 6.2 seats) — non-response and size bias on top of stated-vs-revealed preference."})
    key["reasoning_traps"].append({"id": "T6", "text": "Accepting the VP Sales claim that Copilot would recover a third of lost deals (a mention in loss notes is not proof the deal would have been won; Routewise also discounted)"})
    key["decision_relevant_evidence"].append({"id": "E8", "critical": False, "text": "Survey response rate (6%) and respondent size skew"})
    return packet, key, d


# ====================================================================================================
def case4():
    d = models.case4()
    s = d["seg"]
    packet = f"""# Palisade Docs: raise prices while churn is rising? — briefing pack

{BANNER}
## 1. Context

Palisade Docs sells document-workflow and e-signature software. ARR is {M(d['arr_total'])} from 7,400
customers in three segments. Monthly customer churn has risen over the past year, and the CFO wants a price increase.

**Decision maker:** CEO Ravi Menon, deciding on the 2027 pricing plan with the leadership team in December 2026.

## 2. Decision question

**Should Palisade raise prices in 2027 while customer churn is rising, and if so, how?**

## 3. Objectives and constraints

- Grow ARR at least 15% in 2027 (from {M(d['arr_total'])}).
- Keep net revenue retention above 100% overall.
- Price changes apply at renewal; enterprise contracts follow their own terms.

## 4. Current views inside the company

- **CFO:** "Raise list prices 12% on every plan at renewal from January 2027. That is $10.3M of ARR. Churn is an
  onboarding problem, not a price problem."
- **CEO's concern:** "Churn is going up. A price rise now could push it higher."
- **Head of Customer Success:** "The 2025 promotion brought in customers who never set the product up."

## 5. Segments

**Table 1. Segments, mid-2026**

{table(["Segment", "Customers", "ARR, $M", "Monthly logo churn H1 2025", "Monthly logo churn H1 2026", "Net revenue retention (trailing 12 months)"],
       [[k, f"{v['customers']:,}", f"{v['arr']:.1f}", P(v['churn_h1_25']), P(v['churn_h1_26']), P(v['nrr'], 0)] for k, v in s.items()])}

SMB = 1–50 employees, self-serve, monthly or annual plans. Mid-market = 51–1,000 employees, annual contracts.
Enterprise = over 1,000 employees, mostly multi-year contracts.

## 6. The 2025 SMB promotion

- From February to August 2025, new self-serve SMB customers got 50% off for their first six months. The
  promotion brought in 2,100 SMB customers who are still counted in the base above (about $4.4M of ARR at full price).
- Share of new customers who sent at least five documents in their first month: 41% for the promotion cohort,
  72% for other cohorts.
- Monthly churn in H1 2026 for SMB customers who did **not** come through the promotion: 2.1% (H1 2025 for the
  same kind of customers: 2.0%).

**Table 2. Main churn reason "price / found a cheaper option", share of churned customers who answered the exit survey**

{table(["Group", "Share citing price"], [[k, P(v, 0)] for k, v in d["exit_price_reason"].items()])}

Most promotion-cohort customers who left did so within two months of the discount ending.

## 7. Competitor

- **Inkwell** launched a Starter plan at $9 per user per month in October 2025. Palisade's SMB plan is $15 per
  user per month; Business plan $29; Inkwell Pro $24.
- Palisade's win rate in SMB deals where Inkwell was considered fell from 51% (H1 2025) to 38% (H1 2026).
  Inkwell has not been seen in mid-market or enterprise deals with more than 200 seats.

## 8. Pricing history and tests

- **2023 SMB price increase:** +8% at renewal. SMB monthly churn rose from 1.8% to 2.3% for six months, then
  settled at 1.9%.
- **2024 mid-market test:** +10% list price for new mid-market sign-ups for three months: conversion 23.1%
  against 23.6% for the control group (difference not statistically significant).
- **Enterprise:** 60% of enterprise ARR is under contracts that cap annual price increases at 7%. 40% of
  enterprise ARR renews in 2027, as does 85% of mid-market ARR and all SMB ARR.

## 9. Product and customer evidence

- Mid-market and enterprise customers rate Palisade's integrations and audit trail as the main reasons they stay
  (customer advisory board, 2026).
- SMB customers who send fewer than five documents in their first month churn at about three times the rate of
  those who send more.

## 10. Other material

- **Board dashboard (Q2 2026):** "Monthly churn: 1.4% → 2.3%." The dashboard does not define the measure.
- **Head of Customer Success:** "An onboarding programme will halve SMB churn within two quarters."

## 11. Uncertainties

- How price-sensitive non-promotion SMB customers are now that Inkwell exists.
- Whether the promotion cohort can be activated, or will mostly churn regardless.
- Whether the mid-market test (new sign-ups) predicts how existing customers react at renewal.
"""
    key = {
        "case_id": "c4", "title": "Palisade Docs — pricing while churn rises",
        "decision_question": "Should Palisade raise prices in 2027 while customer churn is rising, and if so, how?",
        "initial_hypothesis": {
            "holder": "CFO (with the CEO holding the opposite view)",
            "statement": "Raise list prices 12% on every plan; churn is onboarding, not price ($10.3M).",
            "expected_handling": "revise",
            "explanation": ("Both interpretations are partly right. The SMB churn rise is mostly a mix effect from the 2025 promotion "
                            f"cohort (≈{P(d['promo_churn'])} monthly churn vs 2.1% for other SMB customers; mix effect ≈ {d['mix_effect']*100:.1f} pp "
                            f"of the {(s['SMB']['churn_h1_26']-s['SMB']['churn_h1_25'])*100:.1f} pp rise) — supporting the CFO — but those customers "
                            "leave over price when the discount ends and Inkwell has made SMB more price-competitive — supporting the CEO. "
                            "A good answer differentiates by segment rather than adopting either view wholesale."),
        },
        "key_insights": [
            {"id": "K1", "critical": True, "text": f"Churn rise is concentrated in SMB (2.0% → 3.1%); mid-market rose modestly (0.6% → 0.8%), enterprise flat (0.2%). Revenue-weighted monthly churn rose from {P(d['rev_churn']['h1_25'],2)} to {P(d['rev_churn']['h1_26'],2)}."},
            {"id": "K2", "critical": True, "text": f"Mix decomposition: non-promo SMB churn 2.0% → 2.1% (rate effect ≈ {d['rate_effect']*100:.1f} pp); promotion cohort ≈ {P(d['promo_churn'])} implied; the promotion explains ≈ {d['mix_effect']*100:.1f} pp of the {(s['SMB']['churn_h1_26']-s['SMB']['churn_h1_25'])*100:.1f} pp SMB increase."},
            {"id": "K3", "critical": True, "text": "Price is a real churn reason, but mainly for the promotion cohort at discount expiry (52% cite price) vs 18% for non-promo SMB; Inkwell's $9 plan and the win-rate fall (51% → 38%) make SMB price-sensitive."},
            {"id": "K4", "critical": True, "text": f"The $10.3M is overstated: only renewing ARR reprices in 2027 and 60% of enterprise ARR is capped at 7% → about {M(d['uplift_total'],2)} before any churn response (SMB {M(d['uplift']['SMB'],2)}, mid-market {M(d['uplift']['Mid-market'],2)}, enterprise {M(d['uplift']['Enterprise'],2)})."},
            {"id": "K5", "critical": True, "text": "Mid-market and enterprise look price-inelastic (low churn, NRR 112%/118%, 2024 test showed no conversion effect, no Inkwell presence) — that is where an increase is safest and worth most."},
            {"id": "K6", "critical": False, "text": f"A 12% increase is revenue-neutral if it causes about {P(d['breakeven_loss_share'])} extra loss of the repriced base. The 2023 SMB +8% increase lost about {P(d['hist_extra_loss'])} extra customers and netted about {P(d['hist_net'])} — but that was before Inkwell."},
            {"id": "K7", "critical": False, "text": "Activation (≥5 documents in month one) predicts retention; onboarding fixes for the promotion cohort are a separate lever from pricing."},
        ],
        "required_calculations": [
            {"id": "Q1", "text": "Segment churn comparison and/or revenue-weighted churn", "expected": f"blended logo churn {P(d['blended']['h1_25'],2)} → {P(d['blended']['h1_26'],2)}; revenue-weighted {P(d['rev_churn']['h1_25'],2)} → {P(d['rev_churn']['h1_26'],2)}", "tolerance": "±0.1 pp"},
            {"id": "Q2", "text": "Promotion-cohort churn / mix decomposition", "expected": f"promo ≈ {P(d['promo_churn'])}; mix ≈ {d['mix_effect']*100:.1f} pp, rate ≈ {d['rate_effect']*100:.1f} pp", "tolerance": "±0.3 pp"},
            {"id": "Q3", "text": "Realistic 2027 uplift of a 12% increase", "expected": M(d['uplift_total'], 2), "tolerance": "±$0.5M; any correction for renewal timing or caps counts"},
            {"id": "Q4", "text": "Break-even extra churn / 2023 precedent", "expected": f"{P(d['breakeven_loss_share'])}; 2023 net ≈ {P(d['hist_net'])}", "tolerance": "±1 pp"},
        ],
        "decision_relevant_evidence": [
            {"id": "E1", "critical": True, "text": "Segment churn table (SMB vs mid-market vs enterprise)"},
            {"id": "E2", "critical": True, "text": "Promotion cohort size, activation and non-promo SMB churn 2.1%"},
            {"id": "E3", "critical": True, "text": "Exit reasons by group (52% vs 18% citing price)"},
            {"id": "E4", "critical": True, "text": "Inkwell $9 plan and SMB win-rate decline"},
            {"id": "E5", "critical": True, "text": "Renewal timing and the 7% enterprise cap"},
            {"id": "E6", "critical": False, "text": "2023 SMB price-increase history and 2024 mid-market test"},
            {"id": "E7", "critical": False, "text": "NRR by segment"},
        ],
        "contradictory_evidence": [
            "Churn rise looks like price sensitivity (exit surveys, Inkwell) and like a cohort mix effect (promotion, activation)",
            "2023 precedent says SMB increases pay off; Inkwell says conditions have changed",
            "CFO's $10.3M vs renewal timing and contract caps",
        ],
        "reasoning_traps": [
            {"id": "T1", "text": "Treating blended churn as one number and concluding price sensitivity everywhere (or nowhere)"},
            {"id": "T2", "text": "Taking the $10.3M at face value"},
            {"id": "T3", "text": "Reading exit surveys without splitting by cohort"},
            {"id": "T4", "text": "Generalising the 2024 new-signup test to renewing customers without caveat"},
        ],
        "key_tradeoffs": [
            {"id": "X1", "text": "ARR uplift vs churn risk, by segment"},
            {"id": "X2", "text": "Competing with Inkwell in SMB (price) vs monetising mid-market/enterprise value"},
            {"id": "X3", "text": "Short-term revenue vs NRR/brand (customer trust at renewal)"},
        ],
        "plausible_recommendations": [
            {"id": "R1", "defensible": "yes", "text": "Differentiated increase: raise mid-market (and enterprise within caps); hold or restructure SMB (grandfather, a lower-priced tier vs Inkwell, fix activation), with a staged test and churn guardrails."},
            {"id": "R2", "defensible": "yes", "text": "Raise mid-market/enterprise now; delay SMB changes until the promotion cohort has washed out and activation is fixed."},
            {"id": "R3", "defensible": "conditional", "text": "A smaller uniform increase (e.g. 5–7%) with SMB grandfathering — defensible if the segment evidence is addressed."},
            {"id": "R4", "defensible": "no", "text": "12% across the board as proposed."},
            {"id": "R5", "defensible": "no", "text": "No increase anywhere because 'churn is rising'."},
        ],
        "defensibility_criteria": [
            "Separates the cohort/mix effect from a rate effect",
            "Recognises both interpretations and reconciles them with the evidence",
            "Corrects or questions the $10.3M estimate",
            "Pricing recommendation differs by segment or explains why it should not",
        ],
    }
    key["key_insights"].append({"id": "K8", "critical": False, "text": f"The dashboard's 1.4% → 2.3% matches neither blended logo churn ({P(d['blended']['h1_25'],2)} → {P(d['blended']['h1_26'],2)}) nor revenue-weighted churn ({P(d['rev_churn']['h1_25'],2)} → {P(d['rev_churn']['h1_26'],2)}); a good answer works from the segment table and notes the undefined metric."})
    key["reasoning_traps"].append({"id": "T5", "text": "Accepting 'onboarding will halve SMB churn' without evidence, cost or timing"})
    key["decision_relevant_evidence"].append({"id": "E8", "critical": False, "text": "Undefined dashboard churn metric vs the segment table"})
    return packet, key, d


# ====================================================================================================
def case5():
    d = models.case5()
    c = d["common"]
    packet = f"""# Parcelbird: should we launch 15-minute grocery delivery? — briefing pack

{BANNER}
## 1. Context

Parcelbird, founded in 2023 in Columbus, Ohio, sells software that runs small grocery fulfillment sites (inventory,
picking, rider dispatch) to grocers. ARR is $4.1M, growing 60% a year, gross margin 81%. The company has $12.0M in
cash and burns $0.4M a month.

The founders now propose that Parcelbird become an operator itself: launch **Parcelbird Now**, a 15-minute grocery
delivery service from its own dark stores in Columbus, Indianapolis and Kansas City.

**Decision maker:** the board (two founders and two investors), January 2027.

## 2. Decision question

**Should Parcelbird launch its own quick-commerce grocery delivery service in 2027?**

## 3. Objectives and constraints

- The investors want a path to profitability within the current cash; a new funding round for a delivery
  operator is "unlikely in this market", according to the lead investor.
- Keep at least 12 months of runway at all times.

## 4. The founders' view

"Quick commerce is growing over 40% a year and nobody owns the Midwest. Our software already runs other people's
dark stores, so we know how to run them better than anyone. With density, the unit economics turn positive: our
model shows contribution profit per order by month 18."

## 5. Market

**Table 1. US quick-commerce grocery sales (GMV), $ billions**

{table(["2022", "2023", "2024", "2025"], [[f"{v:.1f}" for v in d["market"].values()]])}

**Table 2. Incumbent operators (2025)**

{table(["Operator", "Revenue", "EBITDA", "Contribution per order"],
       [[k, f"${v['revenue_m']:,}M", f"−${-v['ebitda_m']}M", f"−${-v['contrib_per_order']:.2f}"] for k, v in d["incumbents"].items()])}

QuickBasket closed 4 of its 11 cities in 2025.

## 6. Unit economics

**Table 3. Per-order inputs: industry benchmarks from Parcelbird's software customers (14 sites, 2025) and the founders' plan**

{table(["Input", "Benchmark median", "Best observed site", "Founders' plan"],
       [["Average order value (AOV)", "$34", "$42", "$45"],
        ["Gross margin on goods", "27%", "27%", "27%"],
        ["Delivery fee collected per order, net of payment cost on it", "$1.99", "$1.99", "$1.99"],
        ["Picking and packing labor per order", "$3.10", "$3.10", "$3.10"],
        ["Rider cost per hour (wage, insurance, vehicle)", "$17.75", "$17.75", "$17.75"],
        ["Orders delivered per rider-hour", "2.4", "3.0", "3.5"],
        ["Dark-store fixed cost per site per year (rent, staff, utilities)", "$1.15M", "$1.15M", "$1.15M"],
        ["Orders per site per day", "900", "1,400", "1,800"],
        ["Payment processing and packaging per order", "$1.30", "$1.30", "$1.30"],
        ["Promotions and discounts, % of AOV", "6%", "6%", "2%"]])}

The best observed AOV and the best observed density are from different sites; no site achieved both. The
benchmark range for orders per rider-hour is 1.9–3.0 and for orders per site per day 400–1,400.

## 7. Columbus pop-up test (six weeks, one temporary site, autumn 2026)

- 11,800 orders; AOV $31; orders grew 18% a week on average.
- Promotions averaged 12% of AOV; riders delivered 2.1 orders per hour; the site averaged 280 orders a day;
  the temporary site's annualised fixed cost was $650,000.

## 8. Customers

- Survey of 1,500 Columbus residents aged 25–39: 44% said they would use 15-minute delivery "at least weekly".
- Pop-up customer data: customer acquisition cost $38 (paid social and first-order credits); 22% of customers
  still ordering in month three; those customers ordered 3.1 times a month.

## 9. Capital

- Founders' plan: 9 dark stores at $0.6M capex each ($5.4M), and a total of $9.5M of cash needed to month 18
  (capex, launch marketing, operating losses), against $12.0M in the bank.

## 10. The software business

- 37 grocers are in the sales pipeline for the software, 9 at the late stage; average contract value $96,000 a year.
- Several grocers in the pipeline want to launch their own fast delivery from existing stores.
- Scaling the software business would need 2 more engineers and 2 sales hires (about $0.8M a year).

## 11. Other material

- **Founders' investor update:** "Zipcart turned contribution-positive in its densest city in Q4 2025 (+$0.40 per
  order). It can be done." Zipcart's shareholder letter adds that this followed a new $3.99 service fee on every
  order and a cut in promotions to 1% of order value, and that order volume in that city fell 14% afterwards.

## 12. Uncertainties

- Whether density in mid-size Midwest cities can reach the benchmark median.
- Whether AOV can rise without losing the convenience use case.
- Rider labor rules: two of the three cities are considering minimum pay standards for delivery workers.
"""
    key = {
        "case_id": "c5", "title": "Parcelbird — quick-commerce entry",
        "decision_question": "Should Parcelbird launch its own quick-commerce grocery delivery service in 2027?",
        "initial_hypothesis": {
            "holder": "Founders",
            "statement": "Enter now: the market grows 40%+ a year and density will make unit economics positive by month 18.",
            "expected_handling": "reject",
            "explanation": (f"Contribution per order is negative at benchmark median ({D(d['base']['contribution'])}), at the best observed density "
                            f"({D(d['best']['contribution'])}) and even combining best density with the best AOV ({D(d['best_aov']['contribution'])}), "
                            f"before customer acquisition and overhead. Break-even AOV at the best density is about {D(d['be_aov_best_density'])}. "
                            f"The founders' +{D(d['founder']['contribution'])} relies on every input beating the best observed site. Growth does not "
                            "fix structurally negative unit economics, and the plan would consume most of the cash. A good answer rejects the "
                            "hypothesis (or limits it to a capped, capital-light test with kill criteria)."),
        },
        "key_insights": [
            {"id": "K1", "critical": True, "text": f"Per-order contribution: median {D(d['base']['contribution'])} (rider {D(d['base']['rider'])}, store {D(d['base']['store'])}); best observed density {D(d['best']['contribution'])}; best density + best AOV {D(d['best_aov']['contribution'])}. Negative in every observed case."},
            {"id": "K2", "critical": True, "text": f"The founders' plan (+{D(d['founder']['contribution'])}) needs AOV $45, 3.5 orders/rider-hour, 1,800 orders/day and 2% promotions — each beyond the best observed site; break-even AOV at best observed density is ≈ {D(d['be_aov_best_density'])}."},
            {"id": "K3", "critical": True, "text": f"The pop-up's contribution was about {D(d['popup']['contribution'])} per order (AOV $31, 12% promotions, 2.1 orders/rider-hour, 280 orders/day) — the 18% weekly order growth is promotion-fuelled top-line growth."},
            {"id": "K4", "critical": True, "text": f"Market growth (CAGR {P(d['cagr'])} 2022–25) coexists with structural losses: both incumbents have negative contribution per order and QuickBasket closed 4 of 11 cities."},
            {"id": "K5", "critical": True, "text": f"Capital: $9.5M of the $12.0M cash to month 18 would leave ≈ $2.5M, far below 12 months of runway (≈ $4.8M at the current $0.4M/month burn) — breaking the runway constraint even if the plan works; no follow-on funding expected."},
            {"id": "K6", "critical": False, "text": f"Customer economics are weak: CAC $38 and 22% month-3 retention; at negative contribution per order no customer ever pays back."},
            {"id": "K7", "critical": False, "text": "The better path: grow the 81%-gross-margin software business — 37 grocers in pipeline (9 late stage, ~$96K ACV), several wanting their own fast delivery, i.e. sell the picks and shovels."},
            {"id": "K8", "critical": False, "text": "Stated intent (44% weekly) is not demand at a price; and rider pay rules are a further downside risk."},
        ],
        "required_calculations": [
            {"id": "Q1", "text": "Contribution per order at benchmark median", "expected": D(d['base']['contribution']), "tolerance": "±$0.30"},
            {"id": "Q2", "text": "Contribution at best observed density (and/or best AOV)", "expected": f"{D(d['best']['contribution'])} / {D(d['best_aov']['contribution'])}", "tolerance": "±$0.30"},
            {"id": "Q3", "text": "Pop-up contribution per order", "expected": D(d['popup']['contribution']), "tolerance": "±$0.50"},
            {"id": "Q4", "text": "Cash / runway after the plan", "expected": "$12.0M − $9.5M = $2.5M, about 6 months at $0.4M/month vs 12 months required", "tolerance": "qualitative"},
            {"id": "Q5", "text": "Market CAGR", "expected": P(d['cagr']), "tolerance": "±1 pp"},
        ],
        "decision_relevant_evidence": [
            {"id": "E1", "critical": True, "text": "Per-order benchmark inputs and the best observed site"},
            {"id": "E2", "critical": True, "text": "Incumbent losses and QuickBasket city exits"},
            {"id": "E3", "critical": True, "text": "Cash, burn and runway constraint; no follow-on funding"},
            {"id": "E4", "critical": True, "text": "Pop-up test: low AOV, high promotions, low density"},
            {"id": "E5", "critical": False, "text": "CAC $38 and 22% month-3 retention"},
            {"id": "E6", "critical": False, "text": "Software pipeline (37 grocers, 9 late stage)"},
            {"id": "E7", "critical": False, "text": "Rider minimum-pay rules under consideration"},
        ],
        "contradictory_evidence": [
            "Fast market growth and 18% weekly pop-up growth vs negative unit economics",
            "Survey intent (44% weekly) vs retention (22% at month three)",
            "Founders' model vs benchmark and best observed inputs",
        ],
        "reasoning_traps": [
            {"id": "T1", "text": "'The market is growing fast, so enter'"},
            {"id": "T2", "text": "'Scale/density will fix the economics' without checking the best observed case"},
            {"id": "T3", "text": "Taking the founders' assumptions or the survey at face value"},
            {"id": "T4", "text": "Treating promotion-fuelled order growth as validation"},
            {"id": "T5", "text": "Ignoring the runway constraint and opportunity cost to the software business"},
        ],
        "key_tradeoffs": [
            {"id": "X1", "text": "Growth market upside vs structurally negative unit economics"},
            {"id": "X2", "text": "Becoming an operator vs staying a software supplier (focus, capital)"},
            {"id": "X3", "text": "Learning from a test vs consuming runway"},
        ],
        "plausible_recommendations": [
            {"id": "R1", "defensible": "yes", "text": "Do not launch; focus capital on the software business and sell to grocers launching fast delivery."},
            {"id": "R2", "defensible": "conditional", "text": "A small, capped, capital-light test (e.g. with a grocer partner's existing store, no own dark stores) with explicit kill criteria tied to contribution per order — defensible only if it shows why it cannot become the founders' plan by stealth."},
            {"id": "R3", "defensible": "no", "text": "Launch in three cities as planned."},
            {"id": "R4", "defensible": "no", "text": "Launch in one city 'to prove density' without showing that even the best observed density loses money."},
        ],
        "defensibility_criteria": [
            "Computes per-order contribution under realistic (benchmark/best observed) inputs",
            "Separates market growth from profitability",
            "Checks the cash/runway constraint",
            "Offers the software alternative or an explicitly capped test",
        ],
    }
    fb, fm, fv = d["fee_best"]["contribution"], d["fee_median"]["contribution"], d["fee_median_vol"]["contribution"]
    key["key_insights"].append({"id": "K9", "critical": True, "text": f"Engages with the evidence that partly supports the founders: with a $3.99 fee and 1% promotions, a site at the best observed density would make about {D(fb)} per order, but a benchmark-median site still loses about {D(fm)} (about {D(fv)} if volume falls 14% as at Zipcart), before acquisition cost; Parcelbird's own pop-up ran far below median density. Positive unit economics are possible only at density no Parcelbird site has shown, and the runway constraint is broken regardless."})
    key["reasoning_traps"].append({"id": "T6", "text": "Either ignoring the Zipcart fee evidence, or treating it as proof the plan works without checking density, the volume loss and the runway"})
    key["contradictory_evidence"].append("Zipcart's positive contribution in its densest city (after a fee and promo cut) vs negative economics elsewhere")
    key["initial_hypothesis"]["explanation"] += " The Zipcart fee evidence shows the economics are not impossible at very high density with a fee, which makes a capped, capital-light test (R2) more defensible — but not the three-city plan."
    return packet, key, d


CASES = {
    "c1-market-entry": case1,
    "c2-profitability": case2,
    "c3-ai-assistant": case3,
    "c4-pricing-churn": case4,
    "c5-negative-entry": case5,
}


def key_md(k):
    L = [f"# Answer key · {k['title']}", "", "> **Evaluators only.** Never copy this file into a generation workspace.", "",
         f"**Decision question:** {k['decision_question']}", "",
         "## Initial hypothesis in the pack", "",
         f"- Holder: {k['initial_hypothesis']['holder']}",
         f"- Statement: {k['initial_hypothesis']['statement']}",
         f"- Expected handling: **{k['initial_hypothesis']['expected_handling']}**",
         f"- Why: {k['initial_hypothesis']['explanation']}", ""]
    for sec, field in [("Key analytical insights", "key_insights"), ("Required calculations", "required_calculations"),
                       ("Decision-relevant evidence", "decision_relevant_evidence"), ("Common reasoning traps", "reasoning_traps"),
                       ("Key trade-offs", "key_tradeoffs"), ("Plausible recommendations", "plausible_recommendations")]:
        L += [f"## {sec}", ""]
        for it in k[field]:
            tag = []
            if it.get("critical"):
                tag.append("critical")
            if "defensible" in it:
                tag.append(f"defensible: {it['defensible']}")
            line = f"- **{it['id']}**{' (' + ', '.join(tag) + ')' if tag else ''}: {it['text']}"
            if "expected" in it:
                line += f" — expected: {it['expected']} (tolerance: {it['tolerance']})"
            L.append(line)
        L.append("")
    L += ["## Contradictory evidence", ""] + [f"- {x}" for x in k["contradictory_evidence"]] + [""]
    L += ["## Criteria for a defensible conclusion", ""] + [f"- {x}" for x in k["defensibility_criteria"]] + [""]
    L += ["Alternative conclusions that meet these criteria are acceptable; the list of plausible recommendations is not exhaustive.", ""]
    return "\n".join(L)


def main():
    KEYS.mkdir(exist_ok=True)
    for cid, fn in CASES.items():
        packet, key, calcs = fn()
        (HERE / cid).mkdir(exist_ok=True)
        (HERE / cid / "packet.md").write_text(packet)
        (KEYS / f"{cid}.json").write_text(json.dumps(key, indent=2, ensure_ascii=False) + "\n")
        (KEYS / f"{cid}.md").write_text(key_md(key))
        (KEYS / f"{cid}.calc.json").write_text(json.dumps(calcs, indent=1, default=float) + "\n")
        print(f"{cid}: packet {len(packet.split()):,} words · {len(key['key_insights'])} insights · "
              f"{len(key['required_calculations'])} calculations")


if __name__ == "__main__":
    main()
