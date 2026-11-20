"""Builds the storyline spec for the Atlas FieldOps / RouteSprout board deck.
Every number comes from ./evidence/briefing-pack.md (source s1) or is derived from those numbers (source s0)."""
import json, re, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "deliverable" / "atlas-routesprout.json"

DP = []
VAL = {}

def src(id_, slide, label, value, unit, excerpt, locator, period="FY2026", **kw):
    d = {"id": id_, "slide_id": slide, "label": label, "value": value, "unit": unit, "period": period,
         "source_id": "s1", "excerpt": excerpt, "locator": locator}
    d.update(kw)
    DP.append(d); VAL[id_] = value

def der(id_, slide, label, unit, calc, formula, period="FY2026", estimate=False, assumptions=None, **kw):
    refs = re.findall(r"[A-Za-z_][A-Za-z0-9_]*", calc)
    value = eval(calc, {}, dict(VAL))
    value = round(value, 4)
    d = {"id": id_, "slide_id": slide, "label": label, "value": value, "unit": unit, "period": period,
         "source_id": "s0", "derived_from": sorted(set(refs), key=refs.index), "formula": formula, "calc": calc}
    if estimate:
        d["estimate"] = True
        d["assumptions"] = assumptions
    d.update(kw)
    DP.append(d); VAL[id_] = value
    return value

P = lambda r: {"data_ref": r}

# ------------------------------------------------------------------ sourced inputs
src("cash", "1", "Atlas unrestricted cash", 24.0, "$M",
    "Atlas has $24.0M unrestricted cash and a board floor of $9.0M at all times", "§2 Hard constraints, bullet 1", period="2027 start")
src("floor", "1", "Board cash floor", 9.0, "$M",
    "Atlas has $24.0M unrestricted cash and a board floor of $9.0M at all times", "§2 Hard constraints, bullet 1", period="at all times")
src("headroom", "12", "Maximum initial cash expenditure", 15.0, "$M",
    "so initial cash expenditure cannot exceed $15.0M", "§2 Hard constraints, bullet 1", period="2027")
src("int_cap", "7", "Cap on one-time integration expenditure through 2028", 4.0, "$M",
    "Systems migration and customer support must stay under $4.0M of one-time integration expenditure through 2028", "§2 Hard constraints, bullet 2", period="through 2028")
src("uptime", "7", "Uptime large customers require", 0.997, "%",
    "Large customers require at least 99.7% uptime.", "§2 Hard constraints, bullet 2", period="quarterly")
src("price", "1", "RouteSprout acquisition price, all cash", 18.0, "$M",
    "Acquisition price | $18.0M all cash | Not including integration", "§3 table, Acquisition price row", period="2027 offer")
src("integA", "1", "Integration estimate, full acquisition", 4.0, "$M",
    "Integration estimate | $4.0M | Six months; 30% of work not yet scoped", "§3 table, Integration estimate row", period="six-month plan")
src("unscoped", "7", "Share of integration work not yet scoped", 0.30, "%",
    "Integration estimate | $4.0M | Six months; 30% of work not yet scoped", "§3 table, Integration estimate row", period="2026 estimate")
src("arr", "2", "RouteSprout recognized ARR", 4.8, "$M",
    "ARR | $4.8M | 42% year-on-year growth before the last quarter", "§3 table, ARR row")
src("growth", "2", "RouteSprout ARR growth, year on year, before the last quarter", 0.42, "%",
    "ARR | $4.8M | 42% year-on-year growth before the last quarter", "§3 table, ARR row")
src("ebitda", "3", "RouteSprout annual EBITDA", -1.0, "$M",
    "Annual EBITDA | −$1.0M | Includes founders salaries", "§3 table, Annual EBITDA row")
src("churn26", "5", "RouteSprout annual customer logo churn, FY2026", 0.21, "%",
    "Annual customer logo churn | 21% | Up from 12% in FY2024", "§3 table (RouteSprout FY2026 column), churn row")
src("churn24", "5", "RouteSprout annual customer logo churn, FY2024", 0.12, "%",
    "Annual customer logo churn | 21% | Up from 12% in FY2024", "§3 table, churn row", period="FY2024")
src("accts", "5", "RouteSprout customer accounts", 310, "accounts",
    "Customer accounts | 310 | 58% of ARR from 41 accounts", "§3 table, Customer accounts row")
src("top41", "5", "Accounts that make up 58% of ARR", 41, "accounts",
    "Customer accounts | 310 | 58% of ARR from 41 accounts", "§3 table, Customer accounts row")
src("top_share", "5", "Share of RouteSprout ARR from the 41 largest accounts", 0.58, "%",
    "Customer accounts | 310 | 58% of ARR from 41 accounts", "§3 table, Customer accounts row")
src("xsell", "3", "Potential cross-sell ARR, Sales VP base case, not signed", 2.4, "$M",
    "Potential cross-sell ARR | $2.4M by 2028 | Sales VP base case; not signed", "§3 table, cross-sell row", period="by end-2028")
src("bookings", "2", "RouteSprout annual bookings (incl. multi-year value and pilots)", 7.2, "$M",
    "dividing the $18M headline valuation by annual bookings of $7.2M", "§3, paragraph under the table")
src("sellmult", "2", "Sellers' quoted multiple (price ÷ bookings)", 2.5, "x",
    "The sellers call the deal \"2.5 times recurring revenue\" by dividing the $18M headline valuation by annual bookings of $7.2M.", "§3, paragraph under the table")
src("B_up", "8", "Staged acquisition, upfront payment", 11.0, "$M",
    "B · Staged acquisition | $11.0M upfront + $3.5M integration | Up to $7.0M additional earnout in 2029", "§4 table, row B (proposed 2027 offer)", period="2027 offer")
src("B_int", "8", "Staged acquisition, integration cost", 3.5, "$M",
    "B · Staged acquisition | $11.0M upfront + $3.5M integration | Up to $7.0M additional earnout in 2029", "§4 table, row B (integration through 2028)", period="through 2028")
src("earnout", "8", "Staged acquisition, maximum earnout", 7.0, "$M",
    "Up to $7.0M additional earnout in 2029 if renewal and integration targets met", "§4 table, row B", period="2029")
src("C_min", "8", "Partnership, two-year minimum", 1.2, "$M",
    "C · Commercial partnership | $1.2M two-year minimum | Nonexclusive routing API; gross profit split 55% to Atlas, 45% to RouteSprout", "§4 table, row C", period="2027–28")
src("C_split", "9", "Partnership gross profit share to Atlas", 0.55, "%",
    "gross profit split 55% to Atlas, 45% to RouteSprout", "§4 table, row C", period="2027–28")
src("C_rs", "9", "Partnership gross profit share to RouteSprout", 0.45, "%",
    "gross profit split 55% to Atlas, 45% to RouteSprout", "§4 table, row C", period="2027–28")
src("D_cost", "8", "Internal build cost through 2028", 3.4, "$M",
    "D · Internal build | $3.4M through 2028 | Launch no earlier than late 2028, ongoing maintenance $0.4M/year", "§4 table, row D", period="through 2028")
src("D_maint", "10", "Internal build, annual operations after launch", 0.4, "$M",
    "it would add about $0.4M of annual operations thereafter", "§5, paragraph 2", period="a year, from launch")
src("D_arr", "10", "Internal build, 2028 ARR if launched on time", 1.3, "$M",
    "The product could generate $1.3M of 2028 ARR if it launches on time, at 80% incremental gross margin", "§5, paragraph 2", period="2028")
src("D_gm", "10", "Internal build, incremental gross margin", 0.80, "%",
    "The product could generate $1.3M of 2028 ARR if it launches on time, at 80% incremental gross margin", "§5, paragraph 2", period="2028")
src("D_months", "10", "Minimum engineering time for a basic routing product", 18, "months",
    "Its own engineers need at least eighteen months for a basic routing product", "§2 Hard constraints, bullet 3", period="from start")
src("xlow", "4", "Cross-sell ARR, finance low case", 0.8, "$M",
    "an explicit low case of $0.8M is plausible if the 21% churn persists and only signed customer trials convert", "§5, paragraph 1", period="by end-2028")
src("xgm", "3", "Incremental gross margin on new cross-sell subscriptions", 0.80, "%",
    "Incremental gross margin on new cross-sell subscriptions is 80%", "§5, paragraph 1", period="by end-2028")
src("cs", "3", "Integration-era customer success and support, per year", 0.85, "$M",
    "another $0.85M/year of integration-era customer success and support will be needed", "§5, paragraph 1", period="a year")
src("seller_ren", "4", "Renewal of existing accounts assumed in the sellers' pitch", 1.0, "%",
    "The seller's pitch counts the full $2.4M as EBITDA improvement and assumes 100% renewal of the existing 310 accounts.", "§5, paragraph 1", period="seller pitch")
src("ren_routing", "6", "Renewal rate, customers who use routing", 0.95, "%",
    "customers who use routing renew at 95%, so routing causes retention.", "§6, paragraph 1 (internal sales deck)", period="latest year")
src("ren_small", "6", "Renewal rate, smaller customers without routing", 0.78, "%",
    "smaller customers without routing renew at 78%", "§6, paragraph 1", period="latest year")
src("ret_years", "13", "Minimum key-engineer retention the value depends on", 2, "years",
    "A substantial part of the value depends on leadership retaining key engineers for at least two years.", "§7", period="from close")

# ------------------------------------------------------------------ derived numbers
der("wf_price", "1", "Purchase price as a cash outflow", "$M", "0 - price", "−$18.0M")
der("wf_int", "1", "Integration as a cash outflow", "$M", "0 - integA", "−$4.0M")
der("A_total", "1", "Path A initial cash (price + integration)", "$M", "price + integA", "$18.0M + $4.0M")
der("A_cash_after", "1", "Atlas cash after Path A initial spend", "$M", "cash - price - integA", "$24.0M − $18.0M − $4.0M")
der("A_gap_floor", "1", "Path A: cash after deal compared with the board floor", "$M", "A_cash_after - floor", "$2.0M − $9.0M")
der("arr_mult", "2", "Price as a multiple of recognized ARR", "x", "price / arr", "$18.0M ÷ $4.8M")
der("book_over", "2", "Amount by which bookings exceed recognized ARR", "%", "bookings / arr - 1", "$7.2M ÷ $4.8M − 1")

base_assume = ["Cross-sell reaches the Sales VP base case of $2.4M of ARR by end-2028 (not signed)",
               "Cross-sell subscriptions earn the stated 80% incremental gross margin",
               "Integration-era support of $0.85M a year is needed as long as integration runs",
               "RouteSprout's FY2026 EBITDA of −$1.0M (including founders' salaries) continues; no cost savings are assumed without evidence",
               "Uptime service credits and renewal losses are not included (not quantified in the pack)"]
der("xs_gp", "3", "Cross-sell gross profit a year, Sales VP base case", "$M", "xsell * xgm", "$2.4M × 80%",
    period="end-2028 run rate", estimate=True, assumptions=base_assume[:2])
der("cs_neg", "3", "Added customer success and support as a cost", "$M", "0 - cs", "−$0.85M", period="a year")
der("contrib_base", "3", "Annual incremental contribution of the acquisition, Sales VP base case", "$M",
    "xsell * xgm - cs + ebitda", "$2.4M × 80% − $0.85M − $1.0M", period="end-2028 run rate", estimate=True, assumptions=base_assume)
der("contrib_low", "4", "Annual incremental contribution of the acquisition, finance low case", "$M",
    "xlow * xgm - cs + ebitda", "$0.8M × 80% − $0.85M − $1.0M", period="end-2028 run rate", estimate=True,
    assumptions=["Cross-sell reaches only the finance low case of $0.8M (21% churn persists, only signed trials convert)"] + base_assume[1:])
der("contrib_pitch", "4", "Annual EBITDA gain as the sellers' pitch counts it", "$M", "xsell + ebitda",
    "$2.4M counted as EBITDA − $1.0M loss", period="seller pitch", estimate=True,
    assumptions=["Sellers' framing: the full $2.4M of cross-sell ARR counted as EBITDA, with no cost of sale or support",
                 "100% renewal of the existing 310 accounts, as the pitch assumes"])
der("drain", "3", "RouteSprout loss plus added support, per year, before cross-sell", "$M", "cs - ebitda",
    "$0.85M + $1.0M", period="a year")
der("breakeven", "4", "Cross-sell ARR at which the acquisition covers its own running costs", "$M",
    "(cs - ebitda) / xgm", "($0.85M + $1.0M) ÷ 80%", period="end-2028 run rate", estimate=True,
    assumptions=["Support cost and RouteSprout's loss stay at $0.85M and $1.0M a year", "Cross-sell earns 80% gross margin"])
der("be_share", "4", "Break-even cross-sell as a share of the Sales VP base case", "%", "breakeven / xsell",
    "$2.31M ÷ $2.4M", period="end-2028 run rate", estimate=True,
    assumptions=["Break-even as estimated on this slide", "Base case of $2.4M as stated by the Sales VP"])
der("payback_pitch", "4", "Years for Path A cash to pay back on the sellers' own EBITDA framing", "years",
    "(price + integA) / (xsell + ebitda)", "$22.0M ÷ $1.4M a year", period="seller pitch", estimate=True,
    assumptions=["Sellers' EBITDA framing of $1.4M a year holds from the first year", "No discounting, no growth"])
der("top41_arr", "5", "ARR from the 41 largest accounts", "$M", "arr * top_share", "$4.8M × 58%")
der("top41_acct_share", "5", "41 largest accounts as a share of all 310 accounts", "%", "top41 / accts", "41 ÷ 310")
der("scoped", "7", "Share of integration work already scoped", "%", "1 - unscoped", "1 − 30%", period="2026 estimate")
der("full_int", "7", "Integration cost if the unscoped 30% comes on top of the $4.0M estimate", "$M",
    "integA / (1 - unscoped)", "$4.0M ÷ (1 − 30%)", period="through 2028", estimate=True,
    assumptions=["The $4.0M covers only the scoped 70% of the work", "The unscoped 30% costs the same per unit of work as the scoped part"])
der("A_cash_after_b", "8", "Atlas cash after Path B initial spend", "$M", "cash - B_up - B_int", "$24.0M − $11.0M − $3.5M")
der("C_cash_after", "8", "Atlas cash after Path C initial spend", "$M", "cash - C_min", "$24.0M − $1.2M")
der("D_cash_after", "8", "Atlas cash after Path D spend", "$M", "cash - D_cost", "$24.0M − $3.4M")
der("B_after_y1", "8", "Path B cash after one year of RouteSprout loss and added support, before cross-sell", "$M",
    "A_cash_after_b - drain", "$9.5M − ($0.85M + $1.0M)", period="12 months after close", estimate=True,
    assumptions=["RouteSprout's FY2026 EBITDA of −$1.0M continues for the first year", "Added support of $0.85M a year starts at close",
                 "No cross-sell gross profit in the first year (none is signed)", "Atlas's own operations stay cash-break-even"])
der("B_y1_gap", "8", "Path B cash after one year compared with the board floor", "$M", "B_after_y1 - floor",
    "$7.65M − $9.0M", period="12 months after close", estimate=True, assumptions=["As for Path B cash after one year"])
der("A_total_b", "9", "Path B initial cash (upfront + integration)", "$M", "B_up + B_int", "$11.0M + $3.5M")
der("C_gp", "9", "Atlas gross profit per routing revenue dollar under the partnership", "%", "xgm * C_split",
    "80% × 55%", period="2027–28", estimate=True,
    assumptions=["Partner routing revenue earns the same 80% gross margin as RouteSprout's software", "The 55/45 gross profit split applies to all routing revenue"])
der("D_contrib", "10", "Internal build annual contribution from launch", "$M", "D_arr * D_gm - D_maint",
    "$1.3M × 80% − $0.4M", period="from late-2028 launch", estimate=True,
    assumptions=["Launch on time, reaching $1.3M of ARR", "80% incremental gross margin", "$0.4M a year of operations after launch",
                 "Cost of delaying the compliance upgrade not included (not estimated in the pack)"])
der("C_be_rev", "9", "Routing revenue over two years at which Atlas's gross profit share recovers the partnership minimum", "$M",
    "C_min / C_gp", "$1.2M ÷ 44%", period="2027–28", estimate=True,
    assumptions=["The $1.2M minimum is a cost on top of the gross profit split", "Partner routing revenue earns an 80% gross margin"])
der("D_payback", "10", "Years after launch for the internal build to pay back its cost", "years", "D_cost / D_contrib",
    "$3.4M ÷ $0.64M a year", period="from launch", estimate=True,
    assumptions=["Contribution as estimated on this slide, flat from launch", "No discounting"])
der("upfront_max", "12", "Maximum upfront payment that keeps Atlas above its floor through a year of losses", "$M",
    "headroom - C_min - B_int - drain", "$15.0M − $1.2M − $3.5M − $1.85M", period="2028 close", estimate=True,
    assumptions=["The partnership's $1.2M two-year minimum is paid before any purchase and not credited back",
                 "Integration stays at the staged plan's $3.5M", "RouteSprout's loss stays at the FY2026 level of $1.0M a year",
                 "Added support of $0.85M a year", "No cross-sell gross profit in the first year after close"])
der("int_cs", "12", "Staged integration plus one year of integration-era support", "$M", "B_int + cs", "$3.5M + $0.85M",
    period="through 2028", estimate=True,
    assumptions=["Integration-era customer success counts against the cap, which covers systems migration and customer support",
                 "One year of support falls within 2028"])
der("upfront_mult", "12", "Maximum upfront payment as a multiple of recognized ARR", "x", "upfront_max / arr",
    "$8.45M ÷ $4.8M", period="2028 close", estimate=True, assumptions=["Ceiling as estimated on this slide", "ARR of $4.8M, not yet verified"])
der("B_up_mult", "12", "Staged offer upfront payment as a multiple of recognized ARR", "x", "B_up / arr", "$11.0M ÷ $4.8M")

# ------------------------------------------------------------------ slides
slides = [
    {"id": "c", "role": "cover", "status": "filled"},
    {"id": "es", "role": "exec_summary", "status": "filled", "archetype": "exec-summary", "message_type": "navigation"},
    {"id": "d1", "role": "section_divider", "section_id": "1", "status": "filled", "archetype": "section-divider", "message_type": "navigation"},
]

slides.append({
    "id": "1", "role": "content", "section_id": "1", "status": "filled",
    "lead_message": {"text": "Paying the asking price in cash would leave Atlas with $2M, $7M below the board's cash floor",
                     "numbers": [{"text": "$2M", "data_ref": "A_cash_after"}, {"text": "$7M", "data_ref": "A_gap_floor"}],
                     "highlights": ["Cash after deal"], "clauses": 1},
    "message_type": "component", "archetype": "waterfall-bridge",
    "rationale": "What takes cash from today's level to the post-deal level -> waterfall",
    "unit_line": "**Atlas unrestricted cash**, $ millions, before and after Path A (full cash acquisition), 2027",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {
        "kind": "big_number", "header": "Path A fails the board's cash test on day one",
        "big_number": P("A_gap_floor"), "caption": "gap to the $9M floor the board requires at all times",
        "bullets": ["**Purchase price:** all from reserves; no financing round is planned in 2027",
                    "**Integration:** at the board's cap, with 30% of the work unscoped",
                    "**Cash after deal:** before RouteSprout's losses, which widen the gap"],
}},
    "body": {"kind": "chart", "chart_type": "waterfall",
             "categories": ["Unrestricted cash", "Purchase price", "Integration", "Cash after deal"],
             "series": [{"name": "Cash", "points": [P("cash"), P("wf_price"), P("wf_int"), P("A_cash_after")]}],
             "sort": "none", "highlight": ["Cash after deal"], "value_format": "\"$\"#,##0\"M\""},
    "footnotes": ["Path A as proposed by the CEO: $18M all-cash price plus the sellers' $4M six-month integration estimate; no external financing facility assumed"],
})

slides.append({
    "id": "2", "role": "content", "section_id": "1", "status": "filled",
    "lead_message": {"text": "The sellers' 2.5 times multiple rests on bookings; on recognized ARR the price is nearly 3.8 times revenue",
                     "numbers": [{"text": "2.5", "data_ref": "sellmult"}, {"text": "3.8", "data_ref": "arr_mult"}], "clauses": 1},
    "message_type": "item", "archetype": "kpi-big-numbers",
    "rationale": "Two multiples and the gap between their bases, three items -> kpi-big-numbers",
    "unit_line": "**RouteSprout valuation multiples**, $18M headline price, FY2026 revenue measures",
    "body": {"kind": "kpi", "items": [
        {"point": P("sellmult"), "caption": "sellers' multiple: price divided by $7.2M of annual bookings",
         "relation": "Flatters the price with a measure that is not recurring",
         "drivers": ["Bookings include multi-year contract value and one-time pilots",
                     "One-year pilots are counted with no adjustment for being non-renewable",
                     "Audit notes call bookings inadequate for valuation multiples"]},
        {"point": P("arr_mult"), "caption": "price divided by $4.8M of recognized ARR, the basis Atlas finance uses",
         "relation": "The multiple the board would actually pay",
         "drivers": ["Atlas corporate finance values recurring revenue on recognized ARR",
                     "ARR grew 42% year on year before the last quarter, but churn is rising",
                     "No independent quality-of-earnings review has confirmed the ARR yet"]},
        {"point": P("book_over"), "caption": "by which bookings overstate recognized ARR",
         "relation": "The gap diligence has to explain",
         "drivers": ["Bookings cannot be used to project retention-adjusted revenue",
                     "Any offer should be priced on a verified ARR schedule",
                     "Integration of $4M comes on top of either multiple"]}]},
    "footnotes": ["Multiples are the $18M headline price divided by FY2026 measures from the briefing pack; neither includes integration cost"],
})

slides.append({
    "id": "3", "role": "content", "section_id": "1", "status": "filled",
    "lead_message": {"text": "Even if the full, unsigned cross-sell plan arrives, the deal nets only $0.07M a year after its own costs",
                     "numbers": [{"text": "$0.07M", "data_ref": "contrib_base"}],
                     "highlights": ["Net contribution"], "clauses": 1},
    "message_type": "component", "archetype": "waterfall-bridge",
    "rationale": "What adds up to the annual contribution -> waterfall, with the cross-sell estimate's basis strip",
    "unit_line": "**Annual incremental contribution of the acquisition**, $ millions a year, Sales VP base case at end-2028 run rate",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {
        "kind": "bullets", "header": "The base case leaves nothing to repay the purchase",
        "bullets": ["**Cross-sell gross profit:** rests on a pipeline with no signed contracts",
                    "**Added support:** integration-era customer success that the sellers' pitch leaves out",
                    "**RouteSprout loss:** held at the FY2026 level; no cost savings are assumed without evidence",
                    "**Net contribution:** still before uptime service credits, which the sellers' case also omits"],
        "implication": "At this run rate the $22M outlay would not pay back within any planning horizon"}},
    "body": {"kind": "chart", "chart_type": "waterfall",
             "categories": ["Cross-sell gross profit", "Added support", "RouteSprout loss", "Net contribution"],
             "series": [{"name": "Contribution", "points": [P("xs_gp"), P("cs_neg"), P("ebitda"), P("contrib_base")]}],
             "sort": "none", "highlight": ["Net contribution"], "value_format": "\"$\"#,##0.00\"M\""},
    "basis": {"header": "How we estimated the base case", "terms": [
        {"point": P("xsell"), "caption": "cross-sell ARR, Sales VP base"},
        {"op": "×", "point": P("xgm"), "caption": "gross margin"},
        {"op": "−", "point": P("drain"), "caption": "support + RouteSprout loss"},
        {"op": "=", "point": P("contrib_base"), "caption": "net contribution a year"}]},
    "footnotes": ["Team estimate from briefing-pack inputs; live formulas in the Calculations sheet of the source workbook"],
})

slides.append({
    "id": "4", "role": "content", "section_id": "1", "status": "filled",
    "lead_message": {"text": "The deal only covers its own costs if cross-sell reaches about $2.3M a year, 96% of an unsigned plan",
                     "numbers": [{"text": "$2.3M", "data_ref": "breakeven"}, {"text": "96%", "data_ref": "be_share"}],
                     "highlights": ["Sales VP base case"], "clauses": 1},
    "message_type": "item", "archetype": "column-time-series",
    "rationale": "Three cases of one measure compared -> columns, base case highlighted",
    "unit_line": "**Annual incremental contribution of the acquisition**, $ millions a year, by cross-sell case, end-2028 run rate",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {
        "kind": "bullets", "header": "The answer turns on one unsigned number",
        "bullets": ["**Low case:** if 21% churn persists, the deal loses money every year",
                    "**Base case:** barely above break-even, with nothing signed",
                    "**Sellers' pitch:** ignores margin and support; payback still takes 15.7 years"],
        "rows": [{"label": "Cross-sell ARR to break even", "basis": "$1.85M ÷ 80% margin", "point": P("breakeven"), "highlight": True},
                 {"label": "Share of the base case", "basis": "$2.3M ÷ $2.4M", "point": P("be_share")}]}},
    "body": {"kind": "chart", "chart_type": "column",
             "categories": ["Finance low case", "Sales VP base case", "Sellers' pitch"],
             "series": [{"name": "Contribution", "points": [P("contrib_low"), P("contrib_base"), P("contrib_pitch")]}],
             "sort": "none", "highlight": ["Sales VP base case"], "value_format": "\"$\"#,##0.00\"M\""},
    "basis": {"header": "How each case is built (low case shown)", "terms": [
        {"point": P("xlow"), "caption": "cross-sell ARR, low case"},
        {"op": "×", "point": P("xgm"), "caption": "gross margin"},
        {"op": "−", "point": P("drain"), "caption": "support + RouteSprout loss"},
        {"op": "=", "point": P("contrib_low"), "caption": "contribution a year"}]},
    "footnotes": ["Sellers' pitch = $2.4M of cross-sell counted as EBITDA less RouteSprout's $1M loss, as the pitch presents it; payback = $22M ÷ $1.4M a year"],
})

slides.append({"id": "d2", "role": "section_divider", "section_id": "2", "status": "filled", "archetype": "section-divider", "message_type": "navigation"})

slides.append({
    "id": "5", "role": "content", "section_id": "2", "status": "filled",
    "lead_message": {"text": "RouteSprout's base is getting less stable: logo churn reached 21%, while a few large accounts hold 58% of ARR",
                     "numbers": [{"text": "21%", "data_ref": "churn26"}, {"text": "58%", "data_ref": "top_share"}], "clauses": 2},
    "message_type": "item", "archetype": "multi-chart-panel",
    "rationale": "Two clauses proving one claim (instability) -> two panels, no arrow",
    "layout": {"variant": "split_2"},
    "body": {"kind": "panels", "panels": [
        {"header": "Churn has almost doubled in two years",
         "unit_line": "**Annual customer logo churn**, % of accounts, FY2024 and FY2026",
         "body": {"kind": "chart", "chart_type": "column", "categories": ["FY2024", "FY2026"],
                  "series": [{"name": "Logo churn", "points": [P("churn24"), P("churn26")]}],
                  "sort": "none", "highlight": ["FY2026"], "value_format": "0%"}},
        {"header": "A small group of accounts carries most of the revenue",
         "unit_line": "**Concentration of RouteSprout ARR**, FY2026",
         "body": {"kind": "kpi", "items": [
             {"point": P("top_share"), "caption": "of ARR comes from 41 of 310 accounts",
              "drivers": ["Those 41 accounts are 13% of the customer base"]},
             {"point": P("top41_arr"), "caption": "of ARR rides on those 41 renewals",
              "drivers": ["No customer-level churn cohort shows whether they are the ones leaving"]}]}}]},
    "so_what": "Any integration that unsettles the 41 largest accounts puts more than half of RouteSprout's ARR at risk",
    "so_what_style": "bar",
    "footnotes": ["Seller-reported figures; no customer-level churn cohort or independently verified ARR schedule exists yet"],
})

slides.append({
    "id": "6", "role": "content", "section_id": "2", "status": "filled",
    "lead_message": {"text": "The 95% renewal of routing users reflects who those customers are, not what routing does for them",
                     "numbers": [{"text": "95%", "data_ref": "ren_routing"}], "highlights": ["Routing users"], "clauses": 1},
    "message_type": "item", "archetype": "bar-ranking",
    "rationale": "A is higher than B, two items, but the point is why -> columns with an interpreting sidebar",
    "unit_line": "**Annual renewal rate**, % of customers, from an internal Atlas sales deck, latest year",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {
        "kind": "bullets", "header": "No retention uplift belongs in the deal value",
        "bullets": ["**Routing users:** mostly larger, multi-branch companies with dedicated customer-success teams",
                    "**Smaller customers without routing:** differ in size and support as well as in the feature, so the gap does not isolate routing",
                    "**What drives renewal:** customer-success interviews point to account managers, not routing features alone"],
        "implication": "Value the deal without a retention uplift, and keep account managers in place through any integration"}},
    "body": {"kind": "chart", "chart_type": "column",
             "categories": ["Routing users", "Smaller customers without routing"],
             "series": [{"name": "Renewal rate", "points": [P("ren_routing"), P("ren_small")]}],
             "sort": "none", "highlight": ["Routing users"], "value_format": "0%"},
    "footnotes": ["The sales deck concludes \"routing causes retention\"; the comparison does not control for customer size or support model"],
})

slides.append({
    "id": "7", "role": "content", "section_id": "2", "status": "filled",
    "lead_message": {"text": "An API-first link protects renewals better than a six-month full migration that uses the whole $4M integration cap",
                     "numbers": [{"text": "$4M", "data_ref": "integA"}], "clauses": 1},
    "message_type": "item", "archetype": "comparison-table",
    "rationale": "Two integration options on the same criteria -> comparison-table",
    "unit_line": "**Integration options for RouteSprout**, team assessment from the briefing pack, 2027–28",
    "layout": {"variant": "full"},
    "body": {"kind": "table", "table_type": "comparison",
             "columns": ["Full migration in six months (sellers' plan)", "API and single sign-on first"],
             "rows": [
                 {"label": "Scope", "cells": [{"text": "All customer records and support operations moved; assumes zero change-management delay"},
                                              {"text": "Products linked by API and single sign-on; RouteSprout's interface kept"}]},
                 {"label": "Integration cost", "cells": [{"point": P("integA")},
                                                         {"text": "Simpler, per the Integration Director; not yet costed"}]},
                 {"label": "Work not yet scoped", "cells": [{"point": P("unscoped")},
                                                            {"text": "Smaller scope to define and audit before signing"}]},
                 {"label": "Customer change", "cells": [{"text": "Interface replaced, possibly before the largest accounts renew"},
                                                        {"text": "Large customers keep the screens they renew on"}]},
                 {"label": "Uptime", "cells": [{"text": "Migration cut-overs put the 99.7% uptime target at risk; credits are not in the sellers' case"},
                                               {"text": "Fewer cut-overs to test against the uptime target"}]},
                 {"label": "Evidence it works", "cells": [{"text": "Sellers cite peers twice RouteSprout's size with lower churn; correlation only"},
                                                          {"text": "Matches the product VP's concern about churn at renewal"}]}]},
    "so_what": "If the unscoped 30% is extra, integration reaches about $5.7M ($4M ÷ 70%), over the cap",
    "so_what_style": "bar",
    "footnotes": ["The board caps one-time integration spend at $4M through 2028; a missed quarterly uptime target triggers service credits and renewal risk"],
})

slides.append({"id": "d3", "role": "section_divider", "section_id": "3", "status": "filled", "archetype": "section-divider", "message_type": "navigation"})

slides.append({
    "id": "8", "role": "content", "section_id": "3", "status": "filled",
    "lead_message": {"text": "The staged deal clears the cash floor at signing, but a year of RouteSprout losses would push Atlas below it",
                     "highlights": ["B · Staged deal"], "clauses": 1},
    "message_type": "item", "archetype": "bar-ranking",
    "rationale": "Four paths against one threshold -> columns with the floor as a dashed benchmark",
    "unit_line": "**Atlas unrestricted cash after each path's initial spend**, $ millions, 2027, against the board floor",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {
        "kind": "bullets", "header": "Only the partnership and the build leave a real cushion",
        "bullets": ["**A · Full deal:** below the floor from day one",
                    "**B · Staged deal:** the earnout of up to $7M falls due in 2029, after the cushion has been drawn down",
                    "**C and D:** both keep most of the reserve, with room for delays"],
        "rows": [{"label": "Staged deal: cash after a year of losses and support, before cross-sell", "basis": "$9.5M − $1.85M a year",
                  "point": P("B_after_y1")},
                 {"label": "Staged deal: gap to the floor after that year", "basis": "$7.65M − $9M floor", "point": P("B_y1_gap"), "highlight": True}]}},
    "body": {"kind": "chart", "chart_type": "column",
             "categories": ["A · Full deal", "B · Staged deal", "C · Partnership", "D · Build"],
             "series": [{"name": "Cash after initial spend", "points": [P("A_cash_after"), P("A_cash_after_b"), P("C_cash_after"), P("D_cash_after")]}],
             "sort": "none", "highlight": ["B · Staged deal"], "value_format": "\"$\"#,##0.0\"M\"",
             "benchmark": {"label": "Board cash floor", "point": P("floor")}},
    "footnotes": ["Initial spend: A $18M + $4M; B $11M + $3.5M; C $1.2M two-year minimum; D $3.4M through 2028. Atlas's own operations assumed cash-break-even"],
})

slides.append({
    "id": "9", "role": "content", "section_id": "3", "status": "filled",
    "lead_message": {"text": "On the board's four tests, the partnership is the strongest 2027 path and the full acquisition the weakest",
                     "highlights": ["C · Partnership"], "count_word": 4, "clauses": 1},
    "message_type": "structure", "archetype": "harvey-ball-table",
    "rationale": "Options compared on the board's criteria, qualitative ratings -> harvey-ball-table",
    "unit_line": "**Routing paths against the board's tests**, team assessment; initial cash in $ millions",
    "layout": {"variant": "full"},
    "body": {"kind": "table", "table_type": "harvey",
             "columns": ["Cash within limits", "Path to payback", "Customer continuity", "Execution capacity", "Initial cash", "Verdict"],
             "rows": [
                 {"label": "A · Full deal", "cells": [{"rating": 0}, {"rating": 0}, {"rating": 1}, {"rating": 1}, {"point": P("A_total")},
                                                     {"text": "Reject: breaks the floor; no payback in the base case"}]},
                 {"label": "B · Staged deal", "cells": [{"rating": 1}, {"rating": 1}, {"rating": 2}, {"rating": 2}, {"point": P("A_total_b")},
                                                       {"text": "Not as offered; only restructured, after diligence"}]},
                 {"label": "C · Partnership", "highlight": True,
                  "cells": [{"rating": 4}, {"rating": 2}, {"rating": 3}, {"rating": 3}, {"point": P("C_min")},
                            {"text": "Do in 2027; limits: nonexclusive, 45% of gross profit to RouteSprout"}]},
                 {"label": "D · Build", "cells": [{"rating": 3}, {"rating": 2}, {"rating": 2}, {"rating": 1}, {"point": P("D_cost")},
                                                 {"text": "Reject: late 2028 at best, displaces compliance work"}]}],
             "legend": "Team assessment from the briefing pack; full circle = best of the four paths"},
    "footnotes": ["Partnership payback: Atlas keeps about 44% of each routing dollar as gross profit (80% × 55%), so about $2.7M of revenue over two years recovers the minimum",
                  "Founders want to sell and the API is nonexclusive: add change-of-control protection"],
})

slides.append({
    "id": "10", "role": "content", "section_id": "3", "status": "filled",
    "lead_message": {"text": "An in-house build would add only about $0.64M a year, and not before late 2028",
                     "numbers": [{"text": "$0.64M", "data_ref": "D_contrib"}], "clauses": 1},
    "message_type": "component", "archetype": "calculation-bridge",
    "rationale": "Our own estimate of the build's contribution -> calculation-bridge (B-08)",
    "unit_line": "**Annual contribution of an internal routing build**, $ millions a year, from launch",
    "body": {"kind": "equation", "terms": [
        {"point": P("D_arr"), "caption": "2028 ARR if the build launches on time (product head)"},
        {"op": "×", "point": P("D_gm"), "caption": "incremental gross margin"},
        {"op": "−", "point": P("D_maint"), "caption": "annual operations after launch"},
        {"op": "=", "point": P("D_contrib"), "caption": "annual contribution from launch"}],
        "assumptions_header": "The build is slower and riskier than the partnership on four counts",
        "assumptions": ["Engineers need at least 18 months for a basic product, so launch comes no earlier than late 2028; a partner could ship a limited offer this summer",
                        "At $0.64M a year, the $3.4M build takes about 5.3 years after launch to pay back, a best case given the late launch",
                        "The effort displaces a planned compliance upgrade, whose delay has a customer cost not yet estimated",
                        "Only one major routing strategy is allowed in 2027, so building rules out the partnership for the year"]},
    "footnotes": ["Team estimate from briefing-pack inputs; live formula in the Calculations sheet of the source workbook"],
})

slides.append({"id": "d4", "role": "section_divider", "section_id": "4", "status": "filled", "archetype": "section-divider", "message_type": "navigation"})

slides.append({
    "id": "11", "role": "content", "section_id": "4", "status": "filled",
    "lead_message": {"text": "Five pieces of missing evidence decide whether buying RouteSprout later is worth doing at all",
                     "count_word": 5, "clauses": 1},
    "message_type": "item", "archetype": "comparison-table",
    "rationale": "Evidence gaps compared on what they test and what would change the answer -> comparison-table",
    "unit_line": "**Diligence questions for a RouteSprout purchase**, and the result that would change the recommendation",
    "layout": {"variant": "full"},
    "body": {"kind": "table", "table_type": "comparison",
             "columns": ["What it tells the board"], "verdict_header": "Result that changes the answer",
             "rows": [
                 {"label": "Churn cohort and renewal dates", "cells": [{"text": "Whether the 21% logo churn hits the 41 largest accounts, and when they renew"}],
                  "note": "Churn in large accounts: walk away"},
                 {"label": "Verified ARR schedule", "cells": [{"text": "Whether the $4.8M holds once pilots and multi-year value are stripped out"}],
                  "note": "Lower ARR: cut the price in proportion"},
                 {"label": "Signed cross-sell pipeline", "cells": [{"text": "How much of the $2.4M base case is actually contracted"}],
                  "note": "Well short of break-even: no deal"},
                 {"label": "Audited integration budget", "cells": [{"text": "Whether the unscoped 30% and integration-era support fit under the $4M cap"}],
                  "note": "Over the cap: API-first scope only, or no deal"},
                 {"label": "Key people retention", "cells": [{"text": "Whether key engineers commit to two years and account managers stay"}],
                  "note": "No commitments: the product's value falls away"}]},
    "callout": {"target": "Signed cross-sell pipeline", "header": "The deciding test",
                "detail": "The deal breaks even only at about $2.3M of cross-sell ARR"},
    "footnotes": ["None of the five exists today: the board has offered to approve preliminary due diligence before committing to a deal"],
})

slides.append({
    "id": "12", "role": "content", "section_id": "4", "status": "filled",
    "lead_message": {"text": "To keep Atlas above its floor through a year of losses, upfront cash must stay below about $8.4M",
                     "numbers": [{"text": "$8.4M", "data_ref": "upfront_max"}], "clauses": 1},
    "message_type": "component", "archetype": "calculation-bridge",
    "rationale": "Our own estimate of the price ceiling -> calculation-bridge (B-08)",
    "unit_line": "**Maximum upfront payment for a staged purchase**, $ millions, first year after a 2028 close",
    "body": {"kind": "equation", "terms": [
        {"point": P("headroom"), "caption": "spendable cash above the $9M floor"},
        {"op": "−", "point": P("C_min"), "caption": "partnership minimum, paid first"},
        {"op": "−", "point": P("B_int"), "caption": "integration, staged plan"},
        {"op": "−", "point": P("drain"), "caption": "a year of loss and support"},
        {"op": "=", "point": P("upfront_max"), "caption": "maximum upfront payment"}],
        "assumptions_header": "The ceiling rests on four assumptions to test in diligence",
        "assumptions": ["Integration stays at $3.5M; unscoped work lowers the ceiling dollar for dollar, and with a year of support it already reaches $4.35M against the $4M cap",
                        "RouteSprout's loss stays at $1M a year (including founders' salaries), with no savings and no first-year cross-sell",
                        "At the ceiling cash sits on the floor after a year, so the $7M earnout must be funded by the business itself",
                        "The ceiling is about 1.8 times recognized ARR, compared with 2.3 times for the $11M staged offer"]},
    "footnotes": ["Team estimate from briefing-pack inputs; live formula in the Calculations sheet of the source workbook"],
})

slides.append({
    "id": "13", "role": "content", "section_id": "4", "status": "filled",
    "lead_message": {"text": "Five terms would make a later purchase fit Atlas's cash limits and protect the renewals that carry the value",
                     "count_word": 5, "clauses": 1},
    "message_type": "argument", "archetype": "numbered-levers",
    "rationale": "N things to negotiate -> numbered-levers",
    "unit_line": "**Conditions for a staged RouteSprout purchase**, and the evidence behind each",
    "body": {"kind": "levers", "headers": ["Term", "Why it matters"], "items": [
        {"code": "1", "text": "Price on ARR verified by a quality-of-earnings review",
         "point": P("arr"), "metric": "recognized ARR, not yet verified"},
        {"code": "2", "text": "Cap upfront cash to fit a year of losses above the floor",
         "point": P("headroom"), "metric": "spendable cash above the board floor"},
        {"code": "3", "text": "Tie the earnout to retention-adjusted ARR, paid from surplus cash",
         "point": P("earnout"), "metric": "maximum earnout, due 2029"},
        {"code": "4", "text": "Integrate by API and single sign-on before touching the interface",
         "point": P("top_share"), "metric": "of ARR sits with the 41 largest accounts"},
        {"code": "5", "text": "Close only once key engineers and account managers commit",
         "point": P("ret_years"), "metric": "years of key-engineer retention needed"}]},
})

slides.append({
    "id": "14", "role": "content", "section_id": "4", "status": "filled",
    "lead_message": {"text": "One routing strategy for 2027: partner from the summer, run diligence alongside and decide at year end on a 2028 purchase",
                     "clauses": 1},
    "message_type": "structure", "archetype": "timeline-roadmap",
    "rationale": "Plan with dates -> timeline-roadmap",
    "unit_line": "**Proposed 2027–28 routing plan**, by quarter",
    "layout": {"variant": "full"},
    "body": {"kind": "timeline", "periods": ["Q1 2027", "Q2 2027", "Q3 2027", "Q4 2027", "H1 2028", "H2 2028"],
             "rows": [
                 {"label": "Board", "bars": [{"start": "Q1 2027", "end": "Q1 2027", "label": "Approve partner + diligence"},
                                             {"start": "Q4 2027", "end": "Q4 2027", "label": "Go / no-go, close in 2028", "emphasis": True}]},
                 {"label": "Partnership", "bars": [{"start": "Q2 2027", "end": "Q2 2027", "label": "Sign API + change-of-control terms"},
                                                   {"start": "Q3 2027", "end": "H2 2028", "label": "Limited routing offer live", "emphasis": True}]},
                 {"label": "Diligence", "bars": [{"start": "Q2 2027", "end": "Q3 2027", "label": "ARR, churn, pipeline, integration"}]},
                 {"label": "If go: integration", "bars": [{"start": "H1 2028", "end": "H2 2028", "label": "API and single sign-on first"}]}],
             "milestones": [{"at": "Q1 2027", "label": "March board"}]},
    "so_what": "If diligence fails any of the five tests, the partnership simply continues and no cash beyond its $1.2M minimum is at stake",
    "so_what_style": "line",
    "footnotes": ["Partnership delivery this summer per the briefing pack; diligence and gate timing are the team's proposal. A 2028 close pushes cross-sell later than the end-2028 run rate used on the deal economics"],
})

slides += [
    {"id": "app", "role": "appendix_divider", "status": "filled"},
    {"id": "b1", "role": "backup", "section_id": "1", "status": "filled", "backup_of": "3",
     "lead_message": {"prefix": "BACKUP:", "text": "Most headline inputs are seller or management figures that diligence has not yet verified"},
     "message_type": "item", "archetype": "data-table",
     "unit_line": "**Key inputs**, $ millions unless stated, FY2026 or as noted, with their evidence status",
     "layout": {"variant": "full"},
     "body": {"kind": "table", "table_type": "data", "columns": ["Value", "Status of the evidence"], "rows": [
         {"label": "Recognized ARR", "cells": [{"point": P("arr")}, {"text": "Seller figure; no quality-of-earnings review"}]},
         {"label": "Annual bookings", "cells": [{"point": P("bookings")}, {"text": "Includes multi-year value and one-time pilots"}]},
         {"label": "Logo churn", "cells": [{"point": P("churn26")}, {"text": "Seller figure; no customer-level cohort"}]},
         {"label": "Cross-sell ARR, base case", "cells": [{"point": P("xsell")}, {"text": "Sales VP estimate; nothing signed"}]},
         {"label": "Cross-sell ARR, low case", "cells": [{"point": P("xlow")}, {"text": "Finance estimate if churn persists"}]},
         {"label": "Integration estimate", "cells": [{"point": P("integA")}, {"text": "Sellers' plan; 30% unscoped, not audited"}]},
         {"label": "Added support a year", "cells": [{"point": P("cs")}, {"text": "Finance estimate for the integration era"}]},
         {"label": "Build ARR in 2028", "cells": [{"point": P("D_arr")}, {"text": "Only if the build launches on time"}]}]},
     "footnotes": ["All values from the briefing pack; none has been independently verified"]},
    {"id": "end", "role": "end_page", "status": "filled"},
]

storyline = {
    "governing_thought": "Partner with RouteSprout in 2027 instead of buying it on the proposed terms, and keep a staged, ARR-priced purchase that diligence must earn",
    "exec_summary": [
        {"id": "1", "text": "The proposed $18M all-cash deal breaks the cash floor and pays back only on the sellers' assumptions",
         "supports": ["1", "2", "3", "4"], "sub_points": [
             {"text": "Price plus integration leaves $2M of cash, $7M below the floor", "slide_id": "1"},
             {"text": "It covers its costs only if cross-sell reaches $2.3M, 96% of an unsigned plan", "slide_id": "4"}]},
        {"id": "2", "text": "RouteSprout's customers are less stable than the pitch assumes, so integration must protect renewals",
         "supports": ["5", "6", "7"], "sub_points": [
             {"text": "Logo churn rose from 12% to 21%, and 41 accounts hold 58% of ARR", "slide_id": "5"},
             {"text": "A full migration uses the whole $4M integration cap, with 30% unscoped", "slide_id": "7"}]},
        {"id": "3", "text": "Of the four paths, only the partnership meets the board's cash, timing and continuity tests in 2027",
         "supports": ["8", "9", "10"], "sub_points": [
             {"text": "The staged deal clears the floor at signing, then falls below it within a year", "slide_id": "8"},
             {"text": "The partnership costs a $1.2M minimum and delivers routing this summer", "slide_id": "9"}]},

        {"id": "4", "text": "Keep buying as an option: run diligence alongside the partnership, then buy only on staged terms",
         "supports": ["11", "12", "13", "14"], "sub_points": [
             {"text": "Upfront cash must stay below about $8.4M, about 1.8 times ARR", "slide_id": "12"},
             {"text": "The board decides at a Q4 2027 gate; if diligence fails, the partnership continues", "slide_id": "14"}]}],
    "next_steps": [
        {"action": "Approve the RouteSprout partnership as Atlas's single 2027 routing strategy and fund preliminary due diligence", "owner": "Board", "timing": "March 2027"},
        {"action": "Sign API partnership terms with change-of-control protection and roadmap sharing limited to the API scope", "owner": "CEO and General Counsel", "timing": "Q2 2027"},
        {"action": "Commission the quality-of-earnings review, churn cohort, pipeline check and integration audit", "owner": "CFO and Integration Director", "timing": "Q2–Q3 2027"},
        {"action": "Secure retention commitments from RouteSprout's key engineers and account managers before any offer", "owner": "CEO with RouteSprout founders", "timing": "Q3 2027"},
        {"action": "Bring a go / no-go on staged, ARR-priced terms within the cash limits, for closing in 2028", "owner": "CEO and CFO", "timing": "Q4 2027 board"}],
}

decision_audit = {
    "constraints": [
        {"item": "Board cash floor of $9.0M at all times; initial spend capped at $15.0M; no financing", "reflected": True,
         "effect": "rules out Path A outright and shows the staged deal breaching the floor within a year of losses", "slide_ids": ["1", "8", "12"]},
        {"item": "One-time integration spend under $4.0M through 2028, with 30% of the work unscoped", "reflected": True,
         "effect": "the full migration has no room left; if integration-era support counts, even the staged plan reaches $4.35M; API-first scope is a deal term", "slide_ids": ["7", "11", "12", "13"]},
        {"item": "Partnership two-year minimum of $1.2M", "reflected": True, "effect": "deducted from the cash available for a later purchase", "slide_ids": ["12"]},
        {"item": "Integration-era customer success of $0.85M a year and RouteSprout's continuing −$1.0M EBITDA", "reflected": True,
         "effect": "included in every contribution and cash figure; turns the base case into a near-zero contribution", "slide_ids": ["3", "4", "8", "12"]},
        {"item": "Uptime service credits and renewal risk from a missed 99.7% target (not quantified)", "reflected": False,
         "effect": "would lower the acquisition's contribution further; the slides say the figures are before these credits", "slide_ids": ["3", "7"]},
        {"item": "Only one major routing strategy in 2027", "reflected": True,
         "effect": "the partnership is the 2027 strategy; a purchase of the same partner is decided at the Q4 gate and closes in 2028", "slide_ids": ["10", "14"]},
        {"item": "Earnout of up to $7.0M due in 2029 after renewal tests", "reflected": True,
         "effect": "earnout must be payable only from cash above the floor", "slide_ids": ["8", "13"]},
        {"item": "Build displaces a compliance upgrade with an unestimated customer cost", "reflected": False,
         "effect": "would make the build worse than the $0.64M contribution shows; stated on the build slide", "slide_ids": ["10"]}],
    "alternatives": [
        {"option": "Sign the staged deal (Path B) now, since $14.5M fits under the $15.0M limit", "verdict": "rejected",
         "why": "clears the floor by only $0.5M; a year of losses and support ($1.85M) takes cash below it, and economics are the same near-zero base case",
         "triage": "body", "slide_ids": ["8", "9"]},
        {"option": "Build routing in-house for $3.4M and keep all the gross profit", "verdict": "rejected",
         "why": "launches late 2028 at best, adds about $0.64M a year, pays back in about 5.3 years after launch and displaces compliance work",
         "triage": "body", "slide_ids": ["10"]},
        {"option": "A restructured staged purchase with a lower upfront payment", "verdict": "combined",
         "why": "kept as the conditional option after diligence: upfront below about $8.4M once the partnership minimum is paid, earnout tied to retention", "triage": "body", "slide_ids": ["12", "13"]},
        {"option": "Partner only, with no purchase path", "verdict": "combined",
         "why": "the founders want to sell and the API is nonexclusive, so the partnership needs change-of-control protection; the purchase option guards against losing the product", "triage": "body", "slide_ids": ["9", "14"]}],
    "failure_threshold": {"driver": "signed cross-sell ARR (and verified ARR) found in diligence",
                          "threshold": "the acquisition covers its own costs only at about $2.3M of cross-sell ARR; with signed pipeline near that level, verified ARR and upfront below about $8.4M, buying becomes attractive",
                          "range": "acquisition contribution a year: low −$1.21M (finance) / base +$0.07M (Sales VP) / high +$1.4M (sellers' framing)",
                          "triage": "body", "slide_ids": ["4", "11", "12"]},
    "consistency": {"headline": storyline["governing_thought"], "holds": True,
                    "fix": "Recommendation is 'partner now, buy only conditionally'; no title claims the deal pays back"},
}

spec = {
    "spec_version": "0.1", "mode": "deck_detailed",
    "meta": {"title": "Routing strategy: buy, partner or build RouteSprout",
             "subtitle": "Recommendation for the March 2027 board meeting",
             "company_name": "Atlas FieldOps", "audience": "Board of directors",
             "purpose": "Decide whether to buy RouteSprout in 2027, and on what terms, rather than build or partner",
             "date": "2026-11-20", "language": "en-US",
             "confidentiality": "Synthetic benchmark data; every company and number is fictional", "theme": "navy"},
    "inputs": [{"id": "in-1", "kind": "file", "label": "Briefing pack (evidence/briefing-pack.md)",
                "content": "Atlas FieldOps acquisition or partnership briefing pack, sections 1–7"}],
    "storyline": storyline,
    "decision_audit": decision_audit,
    "sections": [
        {"id": "1", "title": "The deal as proposed", "exec_item_id": "1", "tracker_label": "Deal"},
        {"id": "2", "title": "The customer base behind the price", "exec_item_id": "2", "tracker_label": "Customers"},
        {"id": "3", "title": "Four routing paths compared", "exec_item_id": "3", "tracker_label": "Options"},
        {"id": "4", "title": "A conditional path to buying", "exec_item_id": "4", "tracker_label": "Terms"}],
    "slides": slides,
    "data_points": DP,
    "sources": [
        {"id": "s1", "kind": "user_provided", "name": "Atlas FieldOps briefing pack (synthetic), markdown emphasis removed from excerpts",
         "publisher": "Atlas FieldOps", "input_id": "in-1"},
        {"id": "s0", "kind": "derived", "name": "Team analysis of the briefing pack"}],
}

OUT.write_text(json.dumps(spec, indent=1, ensure_ascii=False))
print("wrote", OUT, len(DP), "data points")
for k in ["A_cash_after", "A_gap_floor", "arr_mult", "contrib_base", "contrib_low", "contrib_pitch", "breakeven", "be_share",
          "payback_pitch", "B_after_y1", "B_y1_gap", "D_contrib", "D_payback", "upfront_max", "upfront_mult", "full_int", "C_gp", "C_be_rev", "int_cs"]:
    print(k, VAL[k])
