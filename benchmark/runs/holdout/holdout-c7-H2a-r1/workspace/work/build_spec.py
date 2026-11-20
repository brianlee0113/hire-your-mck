"""Builds the storyline spec for the Atlas FieldOps / RouteSprout board deck (compile, restyle).
Source of truth: evidence/analysis.md (finished deck). Numbers traced to evidence/briefing-pack.md."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "deliverable", "atlas-routesprout.json")

DPS = []
_ids = set()


def P(i):
    return {"data_ref": i}


def dp(i, slide, label, value, unit, src, excerpt=None, locator=None, used_in=None, period=None, **kw):
    assert i not in _ids, i
    _ids.add(i)
    d = {"id": i, "slide_id": slide, "label": label, "value": value, "unit": unit, "source_id": src}
    if period: d["period"] = period
    if excerpt: d["excerpt"] = excerpt
    if locator: d["locator"] = locator
    if used_in: d["used_in"] = used_in
    d.update(kw)
    DPS.append(d)


def der(i, slide, label, value, unit, calc, frm, formula, used_in=None, est=None, period=None):
    kw = {"derived_from": frm, "formula": formula, "calc": calc}
    if est:
        kw["estimate"] = True
        kw["assumptions"] = est
    dp(i, slide, label, value, unit, "s0", used_in=used_in, period=period, **kw)


# ------------------------------------------------------------------ pack inputs (s1)
X_CASH = "Atlas has $24.0M unrestricted cash and a board floor of $9.0M at all times, so initial cash expenditure cannot exceed $15.0M."
dp("cash", "4", "Atlas unrestricted cash today", 24.0, "$M", "s1", X_CASH, "§2 Hard constraints, bullet 1", "waterfall start; cash tests")
dp("floor", "4", "Board cash floor (at all times)", 9.0, "$M", "s1", X_CASH, "§2 Hard constraints, bullet 1", "title; headroom tests")
dp("ceil", "4", "Ceiling on initial cash expenditure", 15.0, "$M", "s1", X_CASH, "§2 Hard constraints, bullet 1", "upfront-ceiling derivation")
X_CAP = "Systems migration and customer support must stay under $4.0M of one-time integration expenditure through 2028."
dp("intcap", "5", "Cap on one-time integration expenditure through 2028", 4.0, "$M", "s1", X_CAP, "§2 Hard constraints, bullet 2", "cap test; ceiling derivation")
dp("uptime", "5", "Uptime large customers require", 0.997, "%", "s1", "Large customers require at least 99.7% uptime.", "§2 Hard constraints, bullet 2", "stress table; terms")
X_T = "| ARR | $4.8M | 42% year-on-year growth before the last quarter |"
dp("arr", "6", "RouteSprout recognized ARR, FY2026", 4.8, "$M", "s1", X_T, "§3 table, row ARR", "multiples; concentration", period="FY2026")
dp("growth", "6", "RouteSprout ARR growth year on year, before the last quarter", 0.42, "%", "s1", X_T, "§3 table, row ARR", "sidebar bullet", period="FY2026")
dp("ebitda", "4", "RouteSprout annual EBITDA (includes founders' salaries)", -1.0, "$M", "s1",
   "| Annual EBITDA | −$1.0M | Includes founders salaries |", "§3 table, row Annual EBITDA", "drag; contribution", period="FY2026")
X_CH = "| Annual customer logo churn | 21% | Up from 12% in FY2024 |"
dp("churn26", "3", "RouteSprout annual logo churn, FY2026", 0.21, "%", "s1", X_CH, "§3 table, column RouteSprout FY2026, row churn", "churn chart", period="FY2026")
dp("churn24", "3", "RouteSprout annual logo churn, FY2024", 0.12, "%", "s1", X_CH, "§3 table, row churn", "churn chart", period="FY2024")
X_AC = "| Customer accounts | 310 | 58% of ARR from 41 accounts |"
dp("accts", "9", "RouteSprout customer accounts", 310, "accounts", "s1", X_AC, "§3 table, row Customer accounts", "concentration")
dp("topshare", "3", "Share of RouteSprout ARR from its largest accounts", 0.58, "%", "s1", X_AC, "§3 table, row Customer accounts", "concentration")
dp("topn", "3", "Number of RouteSprout's largest accounts", 41, "accounts", "s1", X_AC, "§3 table, row Customer accounts", "concentration")
dp("price", "4", "Proposed acquisition price, all cash", 18.0, "$M", "s1", "| Acquisition price | $18.0M all cash | Not including integration |", "§3 table, row Acquisition price", "Path A; multiples")
X_IN = "| Integration estimate | $4.0M | Six months; 30% of work not yet scoped |"
dp("integ", "4", "Integration estimate, Path A", 4.0, "$M", "s1", X_IN, "§3 table, row Integration estimate", "Path A cash out")
dp("unscoped", "3", "Share of integration work not yet scoped", 0.30, "%", "s1", X_IN, "§3 table, row Integration estimate", "stress table")
dp("xsell", "3", "Potential cross-sell ARR by 2028, Sales VP base case (not signed)", 2.4, "$M", "s1",
   "| Potential cross-sell ARR | $2.4M by 2028 | Sales VP base case; not signed |", "§3 table, row cross-sell", "bridge; crossover")
dp("bookings", "6", "RouteSprout annual bookings used by the sellers", 7.2, "$M", "s1",
   "The sellers call the deal \"2.5 times recurring revenue\" by dividing the $18M headline valuation by annual bookings of $7.2M.", "§3, paragraph under the table", "multiple chart")
dp("smult", "3", "Sellers' multiple: price ÷ bookings", 2.5, "x", "s1",
   "The sellers call the deal \"2.5 times recurring revenue\" by dividing the $18M headline valuation by annual bookings of $7.2M.", "§3, paragraph under the table", "multiple chart")
X_B = "| B · Staged acquisition | $11.0M upfront + $3.5M integration | Up to $7.0M additional earnout in 2029 if renewal and integration targets met |"
dp("bup", "4", "Path B upfront price", 11.0, "$M", "s1", X_B, "§4 table, row B", "waterfall")
dp("bint", "4", "Path B integration estimate", 3.5, "$M", "s1", X_B, "§4 table, row B", "waterfall")
dp("earn", "3", "Path B earnout, payable in 2029 if targets are met", 7.0, "$M", "s1", X_B, "§4 table, row B", "stress table; payback")
X_C = "| C · Commercial partnership | $1.2M two-year minimum | Nonexclusive routing API; gross profit split 55% to Atlas, 45% to RouteSprout |"
dp("cmin", "3", "Partnership two-year minimum commitment", 1.2, "$M", "s1", X_C, "§4 table, row C", "cash test; payback; risks")
dp("splita", "12", "Atlas share of partnership gross profit", 0.55, "%", "s1", X_C, "§4 table, row C", "crossover")
dp("splitr", "14", "RouteSprout share of partnership gross profit", 0.45, "%", "s1", X_C, "§4 table, row C", "terms")
X_D = "| D · Internal build | $3.4M through 2028 | Launch no earlier than late 2028, ongoing maintenance $0.4M/year |"
dp("dcost", "4", "Internal build cost through 2028", 3.4, "$M", "s1", X_D, "§4 table, row D", "cash test; payback")
dp("dops", "8", "Internal build ongoing maintenance a year", 0.4, "$M", "s1", X_D, "§4 table, row D", "build contribution")
dp("xlow", "3", "Cross-sell ARR, finance low case", 0.8, "$M", "s1",
   "The finance team says an explicit low case of $0.8M is plausible if the 21% churn persists and only signed customer trials convert.", "§5, paragraph 1", "bridge; crossover")
X_GM = "Incremental gross margin on new cross-sell subscriptions is 80%, while another $0.85M/year of integration-era customer success and support will be needed."
dp("gmx", "7", "Incremental gross margin on new cross-sell subscriptions", 0.80, "%", "s1", X_GM, "§5, paragraph 1", "bridge")
dp("support", "5", "Integration-era customer success and support a year", 0.85, "$M", "s1", X_GM, "§5, paragraph 1", "bridge; drag")
dp("renew100", "9", "Renewal of existing accounts assumed in the sellers' pitch", 1.0, "%", "s1",
   "The seller's pitch counts the full $2.4M as EBITDA improvement and assumes 100% renewal of the existing 310 accounts.", "§5, paragraph 1", "churn chart (sellers' case = 0% churn)")
dp("barr", "8", "Internal build ARR if it launches on time", 1.3, "$M", "s1",
   "The product could generate $1.3M of 2028 ARR if it launches on time, at 80% incremental gross margin, but it would add about $0.4M of annual operations thereafter.", "§5, paragraph 2", "build contribution")
X_R = "An internal sales deck says \"customers who use routing renew at 95%, so routing causes retention.\" These customers are mostly larger, multi-branch companies with dedicated customer-success teams; smaller customers without routing renew at 78%."
dp("ren95", "10", "Renewal rate of customers who use routing (internal sales deck)", 0.95, "%", "s1", X_R, "§6, paragraph 1", "claims table")
dp("ren78", "10", "Renewal rate of smaller customers without routing", 0.78, "%", "s1", X_R, "§6, paragraph 1", "claims table")
dp("retyrs", "10", "Years key engineers must be retained", 2, "years", "s1",
   "A substantial part of the value depends on leadership retaining key engineers for at least two years.", "§7", "retention condition")
dp("bmonths", "13", "Minimum time for Atlas engineers to build a basic routing product", 18, "months", "s1",
   "Its own engineers need at least eighteen months for a basic routing product; a partner could deliver a limited offering this summer.", "§2 Hard constraints, bullet 3", "timeline")

# ------------------------------------------------------------------ analysis assumptions (s2)
dp("mo18", "4", "Months from an assumed July 2027 close to end-2028 (team assumption)", 18, "months", "s2",
   "| Acquisition close timing | Assumption | July 2027, so 18 months to end-2028 |", "Source deck p.19, assumptions register", "title; operating-drag period")
dp("dilmo", "13", "Assumed length of acquisition diligence (team assumption)", 3, "months", "s2",
   "Timing assumptions: acquisition closes after a roughly 3-month diligence.", "Source deck p.13, footnote", "timeline footnote")
dp("bandlo", "15", "Lower end of the signed cross-sell ARR earnout bands (proposed term)", 1.4, "$M", "s2",
   "signed cross-sell ARR in bands from $1.4M to $2.4M", "Source deck p.15, Earnout row", "term sheet")
dp("up85", "3", "Recommended upfront ceiling for a conditional purchase", 8.5, "$M", "s2",
   "| Recommended ceiling (≈1.8x $4.8M ARR) | 8.5 |", "Source deck p.15, ceiling derivation", "title; exec summary; terms")

# ------------------------------------------------------------------ derived (s0)
A18 = ["18 months of operations from an assumed July 2027 close to end-2028 (team assumption, source deck p.19)"]
der("yrs", "4", "Operating-drag period in years", 1.5, "years", "mo18 / 12", ["mo18"], "18 months ÷ 12")
der("aout", "4", "Path A cash out at close", 22.0, "$M", "price + integ", ["price", "integ"], "18.0 + 4.0")
der("bout", "4", "Path B cash out at signing", 14.5, "$M", "bup + bint", ["bup", "bint"], "11.0 + 3.5")
der("aleft", "4", "Cash left after Path A close, before operating losses", 2.0, "$M", "cash - aout", ["cash", "aout"], "24.0 − 22.0")
der("bclose", "4", "Cash at Path B close", 9.5, "$M", "cash - bout", ["cash", "bout"], "24.0 − 14.5")
der("bhead0", "3", "Path B headroom above the floor at signing", 0.5, "$M", "bclose - floor", ["bclose", "floor"], "9.5 − 9.0")
der("ebitda18", "4", "RouteSprout EBITDA over the 18-month integration era", -1.5, "$M", "ebitda * yrs", ["ebitda", "yrs"], "−1.0 a year × 1.5 years",
    "waterfall", est=A18 + ["RouteSprout EBITDA held flat at FY2026 level (source deck p.19)"])
der("sup18", "4", "Integration-era support over 18 months", -1.275, "$M", "0 - support * yrs", ["support", "yrs"], "−0.85 a year × 1.5 years",
    "waterfall", est=A18 + ["Support cost runs for the full integration era, then ends (source deck p.19)"])
der("gp18b", "4", "Cross-sell gross profit over 18 months, base case", 1.44, "$M", "xsell / 2 * yrs * gmx", ["xsell", "yrs", "gmx"],
    "(2.4 ÷ 2) × 1.5 × 80%", "waterfall", est=A18 + ["Cross-sell ARR ramps linearly from 0 to the target by end-2028, so average ARR is half the target"])
der("gp18l", "4", "Cross-sell gross profit over 18 months, low case", 0.48, "$M", "xlow / 2 * yrs * gmx", ["xlow", "yrs", "gmx"],
    "(0.8 ÷ 2) × 1.5 × 80%", est=A18 + ["Cross-sell ARR ramps linearly from 0 to the target by end-2028"])
der("dragb", "4", "18-month operating drag, base case", -1.335, "$M", "ebitda18 + sup18 + gp18b", ["ebitda18", "sup18", "gp18b"], "−1.5 − 1.275 + 1.44", "basis strip")
der("dragl", "4", "18-month operating drag, low case", -2.295, "$M", "ebitda18 + sup18 + gp18l", ["ebitda18", "sup18", "gp18l"], "−1.5 − 1.275 + 0.48")
der("bminb", "3", "Path B lowest cash, end-2028, base case", 8.165, "$M", "bclose + dragb", ["bclose", "dragb"], "9.5 − 1.335", "waterfall end")
der("bminl", "3", "Path B lowest cash, end-2028, low case", 7.205, "$M", "bclose + dragl", ["bclose", "dragl"], "9.5 − 2.295")
der("hbb", "4", "Path B headroom against the floor, end-2028, base case", -0.835, "$M", "bminb - floor", ["bminb", "floor"], "8.165 − 9.0", "bar chart")
der("hbl", "4", "Path B headroom against the floor, end-2028, low case", -1.795, "$M", "bminl - floor", ["bminl", "floor"], "7.205 − 9.0", "bar chart")
der("hab", "4", "Path A headroom against the floor, end-2028, base case", -8.335, "$M", "aleft + dragb - floor", ["aleft", "dragb", "floor"], "2.0 − 1.335 − 9.0", "bar chart")
der("hal", "4", "Path A headroom against the floor, end-2028, low case", -9.295, "$M", "aleft + dragl - floor", ["aleft", "dragl", "floor"], "2.0 − 2.295 − 9.0", "bar chart")
der("hc", "4", "Partnership headroom against the floor (zero partner revenue)", 13.8, "$M", "cash - cmin - floor", ["cash", "cmin", "floor"], "24.0 − 1.2 − 9.0", "bar chart")
der("hd", "4", "Build headroom against the floor (full $3.4M spent before launch)", 11.6, "$M", "cash - dcost - floor", ["cash", "dcost", "floor"], "24.0 − 3.4 − 9.0", "bar chart")
der("ccash", "11", "Atlas cash with the partnership, worst case", 22.8, "$M", "cash - cmin", ["cash", "cmin"], "24.0 − 1.2")
der("dcash", "11", "Atlas cash with the build", 20.6, "$M", "cash - dcost", ["cash", "dcost"], "24.0 − 3.4")
der("bupn", "4", "Path B upfront price, as a cash outflow", -11.0, "$M", "0 - bup", ["bup"], "− 11.0", "waterfall")
der("bintn", "4", "Path B integration, as a cash outflow", -3.5, "$M", "0 - bint", ["bint"], "− 3.5", "waterfall")
der("floorneg", "4", "Board cash floor, as a deduction", -9.0, "$M", "0 - floor", ["floor"], "− 9.0", "waterfall")
der("capa", "5", "Path A integration spend if integration-era support counts toward the cap", 5.275, "$M", "integ - sup18", ["integ", "sup18"], "4.0 + 1.275")
der("capb", "5", "Path B integration spend if integration-era support counts toward the cap", 4.775, "$M", "bint - sup18", ["bint", "sup18"], "3.5 + 1.275")
der("intleft", "5", "Room left under the $4.0M cap with Path B's estimate", 0.5, "$M", "intcap - bint", ["intcap", "bint"], "4.0 − 3.5")
der("multa", "6", "Price ÷ recognized ARR (Atlas finance)", 3.75, "x", "price / arr", ["price", "arr"], "18.0 ÷ 4.8", "multiple chart; title")
der("multb", "6", "Path B upfront ÷ recognized ARR", 2.2917, "x", "bup / arr", ["bup", "arr"], "11.0 ÷ 4.8", "multiple chart")
der("prem", "6", "Atlas finance multiple compared with the sellers' multiple", 0.5, "%", "multa / smult - 1", ["multa", "smult"], "3.75 ÷ 2.5 − 1", "sidebar big number; title")
der("btotal", "6", "Path B total price including the full earnout", 18.0, "$M", "bup + earn", ["bup", "earn"], "11.0 + 7.0")
der("gpb", "7", "Cross-sell gross profit a year, base case", 1.92, "$M", "xsell * gmx", ["xsell", "gmx"], "2.4 × 80%")
der("gpl", "7", "Cross-sell gross profit a year, low case", 0.64, "$M", "xlow * gmx", ["xlow", "gmx"], "0.8 × 80%")
der("xcb", "7", "Cross-sell contribution after support, base case", 1.07, "$M", "gpb - support", ["gpb", "support"], "1.92 − 0.85")
der("xcl", "7", "Cross-sell contribution after support, low case", -0.21, "$M", "gpl - support", ["gpl", "support"], "0.64 − 0.85")
der("conb", "3", "Run-rate contribution in the integration era, base case", 0.07, "$M", "xcb + ebitda", ["xcb", "ebitda"], "1.07 − 1.00")
der("conl", "3", "Run-rate contribution in the integration era, low case", -1.21, "$M", "xcl + ebitda", ["xcl", "ebitda"], "−0.21 − 1.00")
AS = ["Integration-era support ends after the 18-month integration era (source deck p.19)", "RouteSprout EBITDA held flat at −$1.0M a year"]
der("runb", "5", "Run-rate contribution after support ends, base case", 0.92, "$M", "gpb + ebitda", ["gpb", "ebitda"], "1.92 − 1.00", est=AS)
der("runl", "7", "Run-rate contribution after support ends, low case", -0.36, "$M", "gpl + ebitda", ["gpl", "ebitda"], "0.64 − 1.00", est=AS)
der("riskarr", "7", "RouteSprout ARR at risk each year at current logo churn", 1.008, "$M", "churn26 * arr", ["churn26", "arr"], "21% × 4.8",
    "sidebar", est=["Logo churn used as a proxy for revenue churn (source deck p.7, p.19)"])
der("earnyrs", "5", "Years of base-case run-rate contribution needed to fund the earnout", 7.61, "years", "earn / runb", ["earn", "runb"], "7.0 ÷ 0.92")
PB = ["Simple undiscounted payback: cash committed ÷ annual run-rate contribution (source deck p.8)"]
der("paya", "8", "Path A simple payback, base case", 23.9, "years", "aout / runb", ["aout", "runb"], "22.0 ÷ 0.92", est=PB + AS)
der("payb", "3", "Path B simple payback, base case", 15.76, "years", "bout / runb", ["bout", "runb"], "14.5 ÷ 0.92", est=PB + AS)
der("paybe", "8", "Path B simple payback including the earnout", 23.37, "years", "(bout + earn) / runb", ["bout", "earn", "runb"], "(14.5 + 7.0) ÷ 0.92", est=PB + AS)
der("pmin", "8", "Partnership minimum a year", 0.6, "$M", "cmin / 2", ["cmin"], "1.2 ÷ 2")
der("pgm", "12", "Atlas contribution per $1 of partner-sold routing ARR", 0.44, "$M", "gmx * splita", ["gmx", "splita"], "80% × 55%")
der("pgpb", "8", "Atlas share of partnership gross profit a year, base case", 1.056, "$M", "xsell * pgm", ["xsell", "pgm"], "2.4 × 0.44")
der("pcb", "8", "Partnership run-rate contribution after the minimum, base case", 0.456, "$M", "pgpb - pmin", ["pgpb", "pmin"], "1.056 − 0.6",
    est=["Partner-sold routing uses the same $0.8–2.4M ARR range at 80% gross margin (source deck p.8, p.19)"])
der("pcl", "8", "Partnership run-rate contribution after the minimum, low case", -0.248, "$M", "xlow * pgm - pmin", ["xlow", "pgm", "pmin"], "0.8 × 0.44 − 0.6",
    est=["Partner-sold routing uses the same $0.8–2.4M ARR range at 80% gross margin (source deck p.8, p.19)"])
der("payc", "8", "Partnership simple payback of the $1.2M minimum, base case", 1.136, "years", "cmin / pgpb", ["cmin", "pgpb"], "1.2 ÷ 1.056", est=PB)
der("pcl2", "8", "Partnership net loss over the two-year term, low case", -0.496, "$M", "pcl * 2", ["pcl"], "−0.248 × 2")
der("bec", "8", "Partnership break-even routing ARR", 1.364, "$M", "pmin / pgm", ["pmin", "pgm"], "0.6 ÷ 0.44")
der("dcon", "8", "Build run-rate contribution from 2029", 0.64, "$M", "barr * gmx - dops", ["barr", "gmx", "dops"], "1.3 × 80% − 0.4",
    est=["Build launches on time and reaches $1.3M ARR, treated as a 2029 run-rate (source deck p.13)"])
der("payd", "8", "Build simple payback after launch", 5.31, "years", "dcost / dcon", ["dcost", "dcon"], "3.4 ÷ 0.64", est=PB)
der("afix", "12", "Acquisition fixed costs a year in the integration era (losses plus support)", 1.85, "$M", "support - ebitda", ["support", "ebitda"], "0.85 + 1.0")
der("gdiff", "12", "Extra contribution per $1 of routing ARR under ownership", 0.36, "$M", "gmx - pgm", ["gmx", "pgm"], "0.80 − 0.44")
der("gapfix", "12", "Fixed-cost gap the ownership margin must cover", 1.25, "$M", "afix - pmin", ["afix", "pmin"], "1.85 − 0.6")

der("cross2", "12", "Crossover once support ends and the partner minimum lapses", 2.778, "$M", "(0 - ebitda) / gdiff", ["ebitda", "gdiff"], "1.0 ÷ 0.36")
der("toparr", "9", "ARR from the 41 largest accounts", 2.784, "$M", "topshare * arr", ["topshare", "arr"], "58% × 4.8", "ARR chart")
der("otharr", "9", "ARR from the other accounts", 2.016, "$M", "arr - toparr", ["arr", "toparr"], "4.8 − 2.784", "ARR chart")
der("othn", "9", "Number of other accounts", 269, "accounts", "accts - topn", ["accts", "topn"], "310 − 41")
der("othshare", "9", "Share of ARR from the other accounts", 0.42, "%", "1 - topshare", ["topshare"], "100% − 58%")
der("pertop", "9", "ARR per large account", 67.9, "$K", "toparr / topn * 1000", ["toparr", "topn"], "2.784 ÷ 41 × 1,000")
der("peroth", "9", "ARR per other account", 7.49, "$K", "otharr / othn * 1000", ["otharr", "othn"], "2.016 ÷ 269 × 1,000")
der("needbe", "16", "Cross-sell ARR ownership needs if RouteSprout reaches EBITDA breakeven", 1.0625, "$M", "support / gmx", ["support", "gmx"], "0.85 ÷ 0.8")
der("needloss", "16", "Cross-sell ARR needed to cover RouteSprout's losses and support", 2.3125, "$M", "afix / gmx", ["afix", "gmx"], "1.85 ÷ 0.8")
der("draglabs", "15", "18-month operating drag, low case, as cash consumed", 2.295, "$M", "0 - dragl", ["dragl"], "− (−2.295)", "basis strip")
der("maxup", "15", "Maximum affordable upfront price", 8.705, "$M", "ceil - intcap - draglabs", ["ceil", "intcap", "draglabs"], "15.0 − 4.0 − 2.295", "basis strip",
    est=["Integration uses the full $4.0M cap, since 30% of the work is unscoped", "Low-case 18-month operating drag (losses + support − cross-sell gross profit)"] + A18)
der("upmult", "15", "Upfront ceiling as a multiple of ARR", 1.77, "x", "up85 / arr", ["up85", "arr"], "8.5 ÷ 4.8")
der("earn95", "3", "Maximum earnout under the conditional terms", 9.5, "$M", "price - up85", ["price", "up85"], "18.0 − 8.5", "title; terms")
der("buf", "15", "Buffer between the maximum affordable upfront and the ceiling", 0.205, "$M", "maxup - up85", ["maxup", "up85"], "8.705 − 8.5")
der("retmo", "10", "Retention agreement length", 24, "months", "retyrs * 12", ["retyrs"], "2 years × 12")

# Crossover chart: contribution by routing ARR level
LEVELS = [0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0]
for k, L in enumerate(LEVELS):
    der(f"lp{k}", "12", f"Partnership contribution at ${L:g}M routing ARR", round(0.44 * L - 0.6, 4), "$M", f"pgm * {L:g} - pmin", ["pgm", "pmin"], f"0.44 × {L:g} − 0.6", "line chart")
    der(f"la{k}", "12", f"Acquisition contribution at ${L:g}M routing ARR, integration era", round(0.8 * L - 1.85, 4), "$M", f"gmx * {L:g} - afix", ["gmx", "afix"], f"0.8 × {L:g} − 1.85", "line chart")
    der(f"ls{k}", "12", f"Acquisition contribution at ${L:g}M routing ARR, after support ends", round(0.8 * L - 1.0, 4), "$M", f"gmx * {L:g} + ebitda", ["gmx", "ebitda"], f"0.8 × {L:g} − 1.0", "line chart")

der("cross", "3", "Routing ARR at which ownership earns as much as the partnership (integration era)", 3.472, "$M", "(lp0 - la0) / ((la2 - la0) - (lp2 - lp0))",
    ["lp0", "la0", "lp2", "la2"], "where the two lines meet: (−0.6 + 1.85) ÷ (0.80 − 0.44) = 1.25 ÷ 0.36", "sidebar big number; title")
der("crossv", "12", "Contribution of either path at the crossover", 0.928, "$M", "pgm * cross - pmin", ["pgm", "cross", "pmin"], "0.44 × 3.47 − 0.6")

# ------------------------------------------------------------------ slides
def T(*cells):
    return [{"text": c} if isinstance(c, str) else c for c in cells]


FOOT_PACK = None
slides = [{"id": "c", "role": "cover", "status": "filled"},
          {"id": "es", "role": "exec_summary", "status": "filled", "archetype": "exec-summary", "message_type": "navigation"}]

# 3 · hypothesis test
slides.append({
    "id": "3", "role": "content", "section_id": "1", "status": "filled",
    "lead_message": {"text": "Our starting hypothesis, a staged purchase of RouteSprout in 2027, fails four of five tests; customer protection is unproven"},
    "message_type": "argument", "archetype": "comparison-table",
    "rationale": "Hypothesis tested against five conditions -> comparison table with a verdict column",
    "body": {"kind": "table", "table_type": "comparison", "columns": ["What would have to be true", "What the evidence shows"],
             "verdict_header": "Verdict",
             "rows": [
                 {"label": "1 · Affordable", "cells": T("Cash stays at or above the $9.0M floor through 2028, and the earnout can be funded",
                                                        "Path B leaves $0.5M of headroom at signing, then falls to $7.2M–8.2M by end-2028; the $7.0M earnout has no funding source"), "note": "✖ Fail (p. 4–5)"},
                 {"label": "2 · Fairly priced", "cells": T("The price rests on verified recurring revenue",
                                                          "3.75 times recognized ARR, not 2.5 times; bookings include multi-year value and pilots; no quality-of-earnings (QoE) review"), "note": "✖ Fail (p. 6)"},
                 {"label": "3 · Pays back", "cells": T("Positive incremental contribution within a reasonable horizon",
                                                       "+$0.07M (base) or −$1.21M (low) a year while integration support runs; payback over 15 years"), "note": "✖ Fail (p. 7–8)"},
                 {"label": "4 · Protects customers", "cells": T("Renewals and 99.7% uptime survive integration",
                                                                "Churn rose from 12% to 21%, the case assumes 100% renewal, an early interface swap risks churn, and no cohort data exists"), "note": "? Unproven (p. 9–10)", "highlight": True},
                 {"label": "5 · Beats the alternatives", "cells": T("Better on cash, payback, continuity and execution",
                                                                   "The partnership earns more below about $3.5M of routing ARR and risks at most $1.2M; building is slower but cheaper"), "note": "✖ Fail (p. 11–13)"}]},
    "so_what": "Revised answer: partner now within the cash limits; buy only if set thresholds clear (p. 14–16)",
    "so_what_style": "bar"})

# 4 · cash floor
slides.append({
    "id": "4", "role": "content", "section_id": "1", "status": "filled",
    "lead_message": {"text": "Neither acquisition path keeps cash above the $9.0M board floor once 18 months of operating losses are counted",
                     "numbers": [{"text": "$9.0M", "data_ref": "floorneg"}], "clauses": 1},
    "message_type": "component", "archetype": "multi-chart-panel",
    "rationale": "One claim, two exhibits: lowest cash by path, and the Path B walk that explains it -> two panels, no arrow",
    "layout": {"variant": "split_2"},
    "body": {"kind": "panels", "panels": [
        {"header": "Both acquisition paths end below the floor in both cases; the partnership and the build stay well above it",
         "unit_line": "**Lowest cash through end-2028 compared with the $9.0M floor**, $M (below 0 = breach)",
         "body": {"kind": "chart", "chart_type": "bar", "categories": ["D · Internal build", "C · Partnership", "B · Staged acquisition", "A · Full cash acquisition"],
                  "series": [{"name": "Base case (cross-sell $2.4M)", "points": [P("hd"), P("hc"), P("hbb"), P("hab")]},
                             {"name": "Low case (cross-sell $0.8M)", "points": [P("hd"), P("hc"), P("hbl"), P("hal")]}],
                  "sort": "none", "value_format": "0.0"}},
        {"header": "Path B closes $0.5M above the floor; 18 months of losses take cash to $8.2M, or $7.2M in the low case",
         "unit_line": "**Path B cash walk, July 2027 to December 2028, base case**, $M",
         "body": {"kind": "chart", "chart_type": "waterfall",
                  "categories": ["Cash today", "Upfront price", "Integration", "RouteSprout EBITDA", "Integration-era support", "Cross-sell gross profit", "Board floor", "Headroom"],
                  "series": [{"name": "Path B cash", "points": [P("cash"), P("bupn"), P("bintn"), P("ebitda18"), P("sup18"), P("gp18b"), P("floorneg"), P("hbb")]}],
                  "sort": "none", "value_format": "0.0"}}]},
    "basis": {"header": "How the 18-month operating drag is built (base case)", "terms": [
        {"point": P("ebitda18"), "caption": "RouteSprout EBITDA, −$1.0M a year (pack) × 1.5 years"},
        {"op": "+", "point": P("sup18"), "caption": "integration-era support, $0.85M a year (pack) × 1.5 years"},
        {"op": "+", "point": P("gp18b"), "caption": "cross-sell gross profit: linear ramp to $2.4M, so half on average, at 80%"},
        {"op": "=", "point": P("dragb"), "caption": "drag in the base case; −$2.3M in the low case ($0.8M cross-sell)"}]},
    "so_what": "Path A breaks the $15.0M spend limit ($24.0M − $9.0M) on its own, leaving $2.0M before losses",
    "so_what_style": "line",
    "footnotes": ["C assumes zero partner revenue (worst case); D assumes the full $3.4M is spent before launch", "A and B include RouteSprout losses and integration-era support from an assumed July 2027 close (team assumption)"]})

# 5 · unpriced cash calls
slides.append({
    "id": "5", "role": "content", "section_id": "1", "status": "filled",
    "lead_message": {"text": "Path B's $0.5M margin also faces three unpriced cash calls: unscoped work, the integration cap and the $7.0M earnout"},
    "message_type": "argument", "archetype": "comparison-table",
    "rationale": "Stresses on the cash margin, each with its evidence and effect -> comparison table",
    "body": {"kind": "table", "table_type": "comparison", "columns": ["Evidence in the pack", "Effect on Atlas cash and limits"],
             "rows": [
                 {"label": "Operating losses before synergies", "cells": T("RouteSprout EBITDA is −$1.0M a year and integration-era support costs $0.85M a year; cross-sell is unsigned and ramps over time",
                                                                          "−$1.3M to −$2.3M over 18 months, which alone breaches the $9.0M floor (p. 4)")},
                 {"label": "Unscoped integration work", "highlight": True, "cells": T("30% of the integration work is not yet scoped, and the six-month plan assumes zero change-management delay",
                                                                                     "Every $1 of overrun is $1 below the floor; Path B's $3.5M estimate leaves $0.5M under the $4.0M cap")},
                 {"label": "The $4.0M integration cap", "highlight": True, "cells": T("The cap covers \"systems migration and customer support\"; the pack calls the $0.85M a year of support \"another\" cost, so it may count",
                                                                                     "If it counts: A = $4.0M + $1.3M = $5.3M and B = $3.5M + $1.3M = $4.8M, so both breach the cap; if not, it hits cash instead")},
                 {"label": "The $7.0M earnout due in 2029", "highlight": True, "cells": T("Payable after 2028 if growth and renewal tests pass; the CFO notes an earnout \"does not eliminate future cash strain\"",
                                                                                         "Cash is already below the floor at end-2028; the base-case run-rate contribution of $0.92M a year would need about 7.6 years to fund it")},
                 {"label": "Uptime service credits", "cells": T("Large customers need 99.7% uptime; a missed quarter triggers service credits and renewal risk the sellers leave out",
                                                               "Not quantified in the pack; the risk only runs one way, and a full record migration makes it larger")}]},
    "so_what": "Any deal must leave room for 18 months of losses, unscoped work and an earnout not paid in cash",
    "so_what_style": "bar"})

# 6 · valuation multiple
slides.append({
    "id": "6", "role": "content", "section_id": "2", "status": "filled",
    "lead_message": {"text": "At 3.75 times recognized ARR, the $18.0M price is 50% above the sellers' 2.5 times, and the $4.8M ARR itself is unverified",
                     "numbers": [{"text": "3.75", "data_ref": "multa"}, {"text": "50%", "data_ref": "prem"}, {"text": "2.5", "data_ref": "smult"}],
                     "highlights": ["Atlas finance: $18.0M ÷ $4.8M ARR"], "clauses": 1},
    "message_type": "item", "archetype": "bar-ranking",
    "rationale": "Same price on three revenue bases -> columns, the Atlas policy basis highlighted",
    "unit_line": "**Price ÷ revenue measure**, multiple, FY2026 revenue",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {
        "kind": "big_number", "header": "Why $7.2M of bookings is the wrong denominator", "big_number": P("prem"),
        "caption": "higher multiple on recognized ARR, Atlas's policy basis, than on bookings",
        "bullets": ["**Not recurring:** the $7.2M counts multi-year contract value and one-off pilots as if they renew",
                    "**Unverified:** no QoE review or verified ARR schedule; the 42% growth stops before the last quarter",
                    "**No earnings:** EBITDA is −$1.0M (with founders' pay), so the price rests on revenue quality and synergies"]}},
    "body": {"kind": "chart", "chart_type": "column",
             "categories": ["Sellers: $18.0M ÷ $7.2M bookings", "Atlas finance: $18.0M ÷ $4.8M ARR", "Path B upfront only: $11.0M ÷ $4.8M ARR"],
             "series": [{"name": "Multiple", "points": [P("smult"), P("multa"), P("multb")]}],
             "sort": "none", "highlight": ["Atlas finance: $18.0M ÷ $4.8M ARR"], "value_format": "0.0#\"x\""},
    "footnotes": ["Path B's total including the full earnout is also $18.0M, or 3.75 times ARR: the staged structure moves when the money is paid, not how much"]})

# 7 · cross-sell bridge
slides.append({
    "id": "7", "role": "content", "section_id": "2", "status": "filled",
    "lead_message": {"text": "The $2.4M cross-sell is ARR, not EBITDA: after all costs it adds about $0.1M a year, and loses $1.2M in the low case"},
    "message_type": "component", "archetype": "data-table",
    "rationale": "Bridge from ARR to contribution in two cases, with the basis of each step -> data table; the sellers' pitch is the first row",
    "unit_line": "**Annual run-rate incremental contribution to Atlas**, $M a year, by end-2028",
    "layout": {"variant": "full"},
    "so_what": "Still optimistic: at 21% logo churn about $1.0M of RouteSprout's $4.8M ARR is at risk each year",
    "so_what_style": "line",
    "footnotes": ["The bridge keeps the sellers' 100% renewal; logo churn is used as a proxy for revenue churn. No cost savings are assumed, as the pack instructs",
                  "The low case is the one finance considers plausible if the 21% churn persists and only signed trials convert"],
    "body": {"kind": "table", "table_type": "data", "columns": ["Base", "Low", "Basis"], "rows": [
        {"label": "Sellers' pitch (as EBITDA)", "cells": T("2.40", "—", "Seller pitch")},
        {"label": "Cross-sell ARR, end-2028", "cells": T("2.40", "0.80", "Sales VP / finance")},
        {"label": "× 80% gross margin", "cells": T("1.92", "0.64", "Pack §5")},
        {"label": "− Integration-era support", "cells": T("−0.85", "−0.85", "Pack §5")},
        {"label": "= Cross-sell contribution", "cells": T("1.07", "−0.21", "")},
        {"label": "+ RouteSprout EBITDA", "cells": T("−1.00", "−1.00", "FY2026, flat")},
        {"label": "= Integration-era contribution", "highlight": True, "cells": T("0.07", "−1.21", "Result")},
        {"label": "Memo: after support ends", "cells": T("0.92", "−0.36", "Assumption")}]}})

# 8 · payback
slides.append({
    "id": "8", "role": "content", "section_id": "2", "status": "filled",
    "lead_message": {"text": "Buying takes over 15 years to pay back (never in the low case), building about 5, and partnering risks at most $1.2M"},
    "message_type": "item", "archetype": "comparison-table",
    "rationale": "Four options on the same three measures -> comparison table",
    "unit_line": "**Simple payback by path**, cash committed ÷ annual run-rate contribution, undiscounted, $M and years",
    "body": {"kind": "table", "table_type": "comparison",
             "columns": ["Cash committed, $M", "Run-rate contribution, $M a year (base / low)", "Payback (base / low)", "Comment"],
             "rows": [
                 {"label": "A · Full cash acquisition", "cells": T("22.0", "+0.92 / −0.36 (+0.07 / −1.21 during integration)", "≈24 years / never",
                                                                  "22.0 ÷ 0.92; RouteSprout's losses absorb most of the cross-sell gross profit")},
                 {"label": "B · Staged acquisition", "cells": T("14.5 upfront + 7.0 earnout", "+0.92 / −0.36 (same business)", "≈16 years (23 with earnout) / never",
                                                               "Staging lowers upfront cash, not the total; the earnout is paid only in the base case")},
                 {"label": "C · Partnership", "highlight": True, "cells": T("1.2 (two-year minimum)", "+0.46 / −0.25 (after the 0.6 a year minimum)", "≈1.1 years / not within the two-year term",
                                                                          "Breaks even at $1.36M of routing ARR; worst-case loss $1.2M, about $0.5M over two years in the low case")},
                 {"label": "D · Internal build", "cells": T("3.4 through 2028 + 0.4 a year operations", "+0.64 from 2029 (low case not given)", "≈5.3 years after launch",
                                                           "1.3 × 80% − 0.4 = 0.64; assumes an on-time launch and displaces the compliance upgrade at an unestimated cost")}]},
    "footnotes": ["Deliberately simple, as the board asked: no precise DCF from inputs we do not have", "For C, routing ARR uses the same $0.8M–2.4M range at 80% margin and Atlas's 55% share; the partner offer is limited, so the low end is likelier"]})

# 9 · churn and concentration
slides.append({
    "id": "9", "role": "content", "section_id": "3", "status": "filled",
    "lead_message": {"text": "RouteSprout's churn is rising and its revenue is concentrated, yet the sellers' case assumes every account renews",
                     "highlights": ["Sellers' case"], "clauses": 1},
    "message_type": "item", "archetype": "multi-chart-panel",
    "rationale": "One claim, two pieces of evidence (churn trend and ARR concentration) -> two panels with a takeaway sidebar",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {
        "kind": "bullets", "header": "What this means for the deal",
        "bullets": ["**Concentration magnifies churn:** losing a handful of the 41 large accounts would wipe out a year of cross-sell",
                    "**People drive renewals:** interviews found account managers, not routing features, drive renewal decisions, so RouteSprout's account managers matter as much as its code",
                    "**Interface timing:** the product VP warns that replacing RouteSprout's interface before large customers renew could add churn",
                    "**No cohort data:** we cannot tell whether churn sits in small or large accounts; this is the first diligence item"]}},
    "body": {"kind": "panels", "panels": [
        {"header": "Logo churn rose from 12% to 21% in two years; the sellers' case assumes none",
         "unit_line": "**Annual customer logo churn**, % of accounts",
         "body": {"kind": "chart", "chart_type": "column", "categories": ["FY2024", "FY2026", "Sellers' case"],
                  "series": [{"name": "Logo churn", "points": [P("churn24"), P("churn26"), P("zero")]}],
                  "sort": "none", "highlight": ["Sellers' case"], "value_format": "0%"}},
        {"header": "58% of ARR sits in 41 accounts, about $68K each against $7.5K for the other 269",
         "unit_line": "**FY2026 ARR by account group**, $M",
         "body": {"kind": "chart", "chart_type": "column", "categories": ["41 large accounts", "269 other accounts"],
                  "series": [{"name": "ARR", "points": [P("toparr"), P("otharr")]}],
                  "sort": "none", "value_format": "0.00"}}]}})
der("zero", "9", "Logo churn implied by the sellers' 100% renewal assumption", 0.0, "%", "1 - renew100", ["renew100"], "100% − 100% renewal", "churn chart")

# 10 · claims vs evidence
slides.append({
    "id": "10", "role": "content", "section_id": "3", "status": "filled",
    "lead_message": {"text": "The synergy, retention and integration claims rest on correlations and untested plans, not on evidence of cause"},
    "message_type": "argument", "archetype": "comparison-table",
    "rationale": "Each deal-case claim against its evidence and our treatment -> comparison table",
    "body": {"kind": "table", "table_type": "comparison", "columns": ["What the evidence actually shows", "How we treat it"], "rows": [
        {"label": "\"Customers who use routing renew at 95%, so routing causes retention\"",
         "cells": T("Routing users are mostly larger, multi-branch firms with dedicated customer-success teams; smaller non-users renew at 78%, so the feature effect is not isolated",
                    "No retention uplift credited to Atlas's core base; keep RouteSprout's account managers")},
        {"label": "\"Integration works when the product is under one general manager\"",
         "cells": T("The cited companies were on average twice as large, with lower churn; the link between integration spend and cross-sell is a correlation with no causal identification",
                    "Not transferable: we do not underwrite the $2.4M cross-sell, and earnouts carry that risk instead")},
        {"label": "\"Six months and $4.0M to integrate\"",
         "cells": T("30% of the work is unscoped and the plan assumes zero change-management delay; API plus single sign-on (SSO) is simpler than migrating records and support",
                    "Integrate through the API first; scope 100% of the work and price the contingency before signing")},
        {"label": "\"2.5x recurring revenue\" and $7.2M of \"annual recurring new sales\"",
         "cells": T("The $7.2M includes multi-year contract value and one-time pilots, so it is unsuitable for valuation or for projecting retention",
                    "Value on QoE-verified recognized ARR only")},
        {"label": "Key people stay (implicit)",
         "cells": T("A substantial part of the value depends on keeping key engineers for at least two years, and no agreements are in place",
                    "Signed 24-month retention agreements become a condition of the deal")}]}})

# 11 · four criteria
slides.append({
    "id": "11", "role": "content", "section_id": "4", "status": "filled",
    "lead_message": {"text": "Against the board's four criteria, only the partnership passes in 2027 — the build is the fallback, not the first move"},
    "message_type": "item", "archetype": "comparison-table",
    "rationale": "Four options rated on the board's criteria -> comparison table, the recommended row highlighted",
    "body": {"kind": "table", "table_type": "comparison",
             "columns": ["Cash against the $9.0M floor", "Payback", "Customer continuity", "Execution capacity", "Strategic fit (tie-break)"],
             "legend": "✔ Pass = meets the board limit with margin · ! Watch = meets it with a risk to manage · ✖ Fail = breaches a hard limit or has no credible path. Only one routing strategy can run in 2027",
             "rows": [
                 {"label": "A · Full cash acquisition", "cells": T("✖ Fail: $22.0M out, cash at $2.0M before losses", "✖ Fail: about 24 years in the base case, never in the low case",
                                                                  "✖ Fail: full migration before renewals, with churn at 21%", "✖ Fail: 30% unscoped, zero-delay plan, key engineers at risk", "✔ Pass: owns routing and RouteSprout's team")},
                 {"label": "B · Staged acquisition", "cells": T("✖ Fail: $14.5M at signing, then $7.2M–8.2M by end-2028", "✖ Fail: about 16 years (23 with the earnout), never in the low case",
                                                               "! Watch: same migration risk; the earnout ties sellers to renewals", "✖ Fail: same integration load on a thinner budget", "✔ Pass: owns routing once integrated")},
                 {"label": "C · Commercial partnership", "highlight": True, "cells": T("✔ Pass: at most $1.2M, cash stays at $22.8M or more", "! Watch: breaks even at $1.36M of routing ARR; loss capped at $1.2M",
                                                                                     "✔ Pass: no migration; prospects served from summer 2027", "! Watch: depends on the partner's viability; roadmap has to be shared", "! Watch: no ownership, but first refusal keeps the option")},
                 {"label": "D · Internal build", "cells": T("✔ Pass: $3.4M, cash stays at $20.6M or more", "! Watch: about 5.3 years after a late-2028 launch",
                                                           "! Watch: nothing to offer prospects until late 2028", "✖ Fail: at least 18 months, and it displaces the compliance upgrade", "✔ Pass: Atlas owns the IP, but it arrives late")}]}})

# 12 · crossover
slides.append({
    "id": "12", "role": "content", "section_id": "4", "status": "filled",
    "lead_message": {"text": "The partnership out-earns ownership at any routing ARR below about $3.5M, well above the Sales VP's unsigned $2.4M",
                     "numbers": [{"text": "$3.5M", "data_ref": "cross"}], "highlights": ["Partnership"], "clauses": 1},
    "message_type": "correlation", "archetype": "line-trend",
    "rationale": "Contribution of each path as routing ARR rises; where the lines cross is the point -> line chart over ARR levels",
    "unit_line": "**Annual run-rate contribution to Atlas by routing ARR sold**, $M a year, before acquisition capital",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {
        "kind": "big_number", "header": "Ownership wins only at scale", "big_number": P("cross"),
        "caption": "routing ARR at which ownership first matches the partnership while integration support runs",
        "bullets": ["**Low and base cases:** partner −0.25 against −1.21 at $0.8M; +0.46 against +0.07 at $2.4M",
                    "**After support ends:** the crossover is still $2.78M, once the partner minimum lapses too",
                    "**Capital excluded:** counting the $14.5M to $22.0M paid to acquire widens the partnership's lead",
                    "**Assumption:** partner-sold routing earns the same 80% margin; the $1.2M minimum is a sunk cost"]}},
    "body": {"kind": "chart", "chart_type": "line",
             "categories": [f"${L:.1f}M" for L in LEVELS],
             "series": [{"name": "Partnership", "points": [P(f"lp{k}") for k in range(len(LEVELS))]},
                        {"name": "Acquisition, integration era", "points": [P(f"la{k}") for k in range(len(LEVELS))]},
                        {"name": "Acquisition, after support ends", "points": [P(f"ls{k}") for k in range(len(LEVELS))]}],
             "sort": "none", "highlight": ["Partnership"], "value_format": "0.00"},
    "footnotes": ["Partnership: 0.44 × ARR − 0.6 (55% of 80% gross profit, less the $0.6M a year minimum)", "Acquisition: 0.8 × ARR − 1.85 while support runs ($1.0M losses, $0.85M support), 0.8 × ARR − 1.0 after; crossover 1.25 ÷ 0.36 = $3.47M at +0.93"]})

# 13 · build timing
slides.append({
    "id": "13", "role": "content", "section_id": "4", "status": "filled",
    "lead_message": {"text": "Building is affordable but cannot ship before late 2028, missing renewals the partnership serves from summer 2027"},
    "message_type": "time-series", "archetype": "timeline-roadmap",
    "rationale": "When each path delivers routing, by quarter -> timeline",
    "unit_line": "**When each path delivers routing to customers**, by quarter, March 2027 board to mid-2029",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {
        "kind": "bullets", "header": "The build case in numbers",
        "bullets": ["**Cost:** $3.4M through 2028, plus $0.4M a year in operations after launch",
                    "**Return:** $0.64M a year if $1.3M of ARR arrives (1.3 × 80% − 0.4), about 5.3 years to pay back; the pack's \"2028 ARR\" is unlikely after a late-2028 launch, so we treat it as a 2029 run-rate",
                    "**Hidden cost:** it displaces a planned compliance upgrade, at a customer cost not yet estimated",
                    "**Role:** the fallback if the partnership underperforms and the buy terms fail at the 2028 gate"]}},
    "body": {"kind": "timeline",
             "periods": ["Q1 2027", "Q2 2027", "Q3 2027", "Q4 2027", "Q1 2028", "Q2 2028", "Q3 2028", "Q4 2028", "Q1 2029", "Q2 2029"],
             "rows": [
                 {"label": "C · Partnership", "bars": [{"start": "Q3 2027", "end": "Q2 2029", "label": "Live summer 2027, two-year term to mid-2029", "emphasis": True}]},
                 {"label": "A/B · Acquisition", "bars": [{"start": "Q2 2027", "end": "Q2 2027", "label": "Diligence"},
                                                         {"start": "Q3 2027", "end": "Q4 2027", "label": "Integrate (six-month plan)"},
                                                         {"start": "Q1 2028", "end": "Q2 2028", "label": "Delay risk"}]},
                 {"label": "D · Internal build", "bars": [{"start": "Q2 2027", "end": "Q3 2028", "label": "Build, at least 18 months"},
                                                          {"start": "Q4 2028", "end": "Q4 2028", "label": "Launch"},
                                                          {"start": "Q1 2029", "end": "Q2 2029", "label": "Ramp to $1.3M ARR"}]}],
             "milestones": [{"at": "Q1 2027", "label": "Board, Mar 2027"}, {"at": "Q1 2028", "label": "Gate, Q1 2028"}]},
    "footnotes": ["Timing assumptions: the acquisition closes after a roughly 3-month diligence; Atlas can run only one major routing strategy in 2027", "The build starts after the March 2027 board and takes at least 18 months, so launch comes no earlier than Q4 2028"]})

# 14 · partnership terms
slides.append({
    "id": "14", "role": "content", "section_id": "5", "status": "filled",
    "lead_message": {"text": "Sign the partnership on terms that cap cost, protect uptime and stop a competitor from capturing RouteSprout"},
    "message_type": "structure", "archetype": "text-columns",
    "rationale": "Two groups of contract terms -> text columns, protection emphasized",
    "body": {"kind": "text", "style": "columns", "columns": [
        {"header": "Commercial terms cap the cost and protect uptime", "detail": [
            "**Scope and price (as offered):** non-exclusive routing API with a $1.2M two-year minimum; gross profit splits 55% to Atlas and 45% to RouteSprout",
            "**Ask, credit the minimum:** count minimum payments against RouteSprout's 45% share, which cuts the $1.36M break-even and the $1.2M maximum loss",
            "**Service level:** at least 99.7% quarterly uptime, with service credits passed back to Atlas to match the credits Atlas owes its large customers",
            "**Ask, segment exclusivity:** exclusivity in utilities and repair contractors, Atlas's core segments; negotiate for it, but do not make it a condition"]},
        {"header": "Protection terms stop a competitor capturing RouteSprout", "emphasis": True, "detail": [
            "**Change of control:** right of first refusal on any sale of RouteSprout, plus a right to terminate if a competitor buys it; the founders want to sell, so this is the key protection",
            "**Pre-agreed purchase option:** attach the conditional term sheet (p. 15), exercisable at the Q1 2028 gate, with partnership fees credited against the price",
            "**Information rights:** customer-level churn cohorts, the ARR schedule and pipeline data, which double as diligence evidence",
            "**Continuity and roadmap:** source-code escrow and data portability in case RouteSprout fails (EBITDA −$1.0M); share only interface-level roadmap, through a clean team",
            "**Why walk away without them:** the roadmap risk would then outweigh the speed benefit"]}]},
    "so_what": "Walk away if RouteSprout refuses first-refusal or change-of-control terms; reopen the build",
    "so_what_style": "bar"})

# 15 · conditional purchase terms
slides.append({
    "id": "15", "role": "content", "section_id": "5", "status": "filled",
    "lead_message": {"text": "If evidence clears, buy conditionally: at most $8.5M upfront, up to $9.5M more if earned, never breaching the cash floor",
                     "numbers": [{"text": "$8.5M", "data_ref": "up85"}, {"text": "$9.5M", "data_ref": "earn95"}]},
    "message_type": "structure", "archetype": "comparison-table",
    "rationale": "Term sheet with the limit on each term, and the derivation of the upfront ceiling as a basis strip",
    "body": {"kind": "table", "table_type": "comparison", "columns": ["Limit", "Proposed structure"],
             "rows": [
                 {"label": "Upfront cash", "highlight": True, "cells": [{"point": P("up85")}, {"text": "QoE-verified recognized ARR excluding pilots (about 1.8 times); cut about 1.8 times any shortfall; never raised"}]},
                 {"label": "Earnout", "cells": [{"point": P("earn95")}, {"text": "Total within the sellers' $18.0M; 2028–29 tests: top-41 ARR kept, churn ≤ 12%, signed cross-sell in $1.4M–2.4M bands, 99.7% uptime"}]},
                 {"label": "Payment protection", "cells": T("$9.0M floor + buffer", "Paid only while cash stays above floor plus buffer; excess deferred, or in Atlas equity if shareholders approve")},
                 {"label": "Integration", "cells": T("$4.0M cap", "API and single sign-on first; no interface swap or record migration before large renewals; fully scoped, incl. support")},
                 {"label": "People", "cells": T("24 months", "Retention agreements for key engineers and account managers, signed before close")},
                 {"label": "Walk-away", "cells": T("Over $8.5M upfront or all cash", "Keep the partnership and do not buy")}]},
    "footnotes": ["The ceiling drops $1-for-$1 for partnership fees not credited at close and for any audited integration budget above the cap; never raise it to offset churn in large accounts"],
    "basis": {"header": "Deriving the upfront ceiling", "terms": [
        {"point": P("ceil"), "caption": "cash above the $9.0M floor"},
        {"op": "−", "point": P("intcap"), "caption": "integration at the $4.0M cap (30% unscoped, so assume all of it is used)"},
        {"op": "−", "point": P("draglabs"), "caption": "18-month operating drag, low case (losses + support − cross-sell gross profit)"},
        {"op": "=", "point": P("maxup"), "caption": "maximum affordable; the $8.5M ceiling (about 1.8 times ARR) leaves a thin $0.2M buffer"}]}})

# 16 · six thresholds
slides.append({
    "id": "16", "role": "content", "section_id": "5", "status": "filled",
    "lead_message": {"text": "Six pieces of missing information would change the recommendation, and each has a threshold set in advance", "count_word": 6},
    "message_type": "item", "archetype": "data-table",
    "rationale": "Decision gates: today, threshold, response -> data table",
    "body": {"kind": "table", "table_type": "data", "columns": ["Today", "Threshold to proceed with buying", "If it is not met"], "rows": [
        {"label": "1 · QoE-verified ARR", "cells": T("$4.8M, unverified; bookings include pilots", "Recognized ARR of at least $4.8M, excluding pilots", "Cut the price by about 1.8 times each $1 of shortfall, or walk away")},
        {"label": "2 · Customer-level churn cohort", "cells": T("21% logo churn, no cohort data", "Churn falling toward the FY2024 level of 12%, and stable top-41 accounts", "Stay with the partnership; do not buy")},
        {"label": "3 · Signed routing demand", "cells": T("$0 signed; $2.4M is the Sales VP's view", "At least $1.36M of run-rate shows demand; about $2.3M is needed to cover RouteSprout's losses", "Below $1.36M, reconsider routing altogether, including the build")},
        {"label": "4 · RouteSprout standalone EBITDA", "cells": T("−$1.0M a year", "At breakeven, ownership needs only about $1.06M of cross-sell (0.85 ÷ 0.8)", "Keep the earnout weighted to results")},
        {"label": "5 · Audited integration budget", "cells": T("30% unscoped, zero-delay plan", "Fully scoped at no more than $4.0M, including support and contingency", "Do not buy")},
        {"label": "6 · Key people and seller terms", "cells": T("No retention agreements; $18.0M all cash", "24-month agreements signed, and sellers accept at most $8.5M upfront", "Keep the partnership; revisit the build in 2028")}]},
    "so_what": "Early trigger: if a rival bidder emerges, use first refusal only once items 1, 2 and 5 clear",
    "so_what_style": "bar"})

# 17 · decisions and sequence
slides.append({
    "id": "17", "role": "content", "section_id": "5", "status": "filled",
    "lead_message": {"text": "In March, approve the partnership, fund diligence and set walk-away terms; decide on buying at a Q1 2028 gate"},
    "message_type": "structure", "archetype": "text-columns",
    "rationale": "Decisions asked now, then the sequence after approval -> two text columns",
    "body": {"kind": "text", "style": "columns", "columns": [
        {"header": "Five decisions requested in March 2027", "emphasis": True, "detail": [
            "**Decline** the $18.0M all-cash proposal (Path A) and the staged deal as structured (Path B)",
            "**Approve** the two-year RouteSprout partnership (at most $1.2M minimum) with the protections on p. 14",
            "**Approve preliminary diligence:** QoE, customer cohorts, integration scoping and key-person review; the CFO sizes the budget, which the pack does not give",
            "**Mandate** negotiation of the conditional term sheet: at most $8.5M upfront and up to $9.5M earned, with a set walk-away",
            "**Defer** the internal build, and revisit it at the gate if the partnership underperforms"]},
        {"header": "Sequence after approval", "detail": [
            "**Apr–Jun 2027:** sign the partnership; run diligence in parallel and negotiate the conditional term sheet",
            "**Summer 2027:** routing goes live with the enterprise prospects that asked for it; track attach and ARR",
            "**Q3–Q4 2027:** QoE and cohort results arrive; watch renewal outcomes for RouteSprout's 41 large accounts",
            "**Q1 2028 gate:** buy if all six thresholds are met (p. 16); otherwise continue the partnership, or start the build if demand is proven but the partner falls short",
            "**Any time:** if a competing bid emerges, apply the early trigger (p. 16)"]}]},
    "so_what": "Our reading: partnering in 2027, then buying in 2028, counts as one routing strategy",
    "so_what_style": "line"})

# 18 · risks
slides.append({
    "id": "18", "role": "content", "section_id": "5", "status": "filled",
    "lead_message": {"text": "The recommendation carries five main risks, each with a mitigation, and its cash downside is capped at $1.2M", "count_word": 5},
    "message_type": "item", "archetype": "comparison-table",
    "rationale": "Risks with cause, mitigation and residual exposure -> comparison table with a residual column",
    "body": {"kind": "table", "table_type": "comparison", "columns": ["Why it matters", "Mitigation"], "verdict_header": "Residual exposure", "rows": [
        {"label": "RouteSprout is sold to a competitor during the partnership", "cells": T("The founders want to sell, and Atlas will have shared roadmap details", "Right of first refusal, termination on change of control, interface-only roadmap through a clean team"),
         "note": "Medium: Atlas would lose its routing supplier, and the build becomes the fallback"},
        {"label": "The partner offering is too limited for enterprise prospects", "cells": T("The partner offer is \"limited\", and prospects may want deep integration", "Pilot with the requesting prospects in summer 2027 and measure attach before the gate"),
         "note": "Medium: prospects may wait for the 2028 decision"},
        {"label": "Routing ARR stays below the $1.36M break-even", "cells": T("The $1.2M minimum is a fixed cost", "Ask for the minimum to be credited against the 45% share; weight the gate to signed ARR"),
         "note": "Low: at most $1.2M, about $0.5M net in the low case"},
        {"label": "RouteSprout fails financially", "cells": T("EBITDA is −$1.0M, churn is 21%, and its cash position is unknown", "Source-code escrow, data portability and uptime service credits; our minimum also funds the partner"),
         "note": "Medium: service disruption, so the SLA must be tied to 99.7%"},
        {"label": "The sellers reject the conditional terms", "cells": T("The founders asked for $18.0M in cash", "Walk away: the partnership meets the customer need without ownership"),
         "note": "Low: we give up the option of owning routing, not the capability"}]}})

slides.append({"id": "app", "role": "appendix_divider", "status": "filled"})

# 19 · assumptions register (backup)
slides.append({
    "id": "19", "role": "backup", "backup_of": "4", "section_id": "1", "status": "filled",
    "lead_message": {"prefix": "BACKUP:", "text": "The analysis separates pack evidence from assumptions, each one conservative or tested where it is used"},
    "message_type": "item", "archetype": "definition-table",
    "body": {"kind": "table", "table_type": "data", "columns": ["Type and value used", "Why, and how sensitive"], "rows": [
        {"label": "Close timing", "cells": T("Assumption: July 2027, so 18 months to end-2028", "March board plus about 3 months of diligence; a later close shifts timing, not the conclusion")},
        {"label": "RouteSprout EBITDA", "cells": T("Assumption: held at −$1.0M a year", "42% growth and 21% churn pull opposite ways; breakeven cuts the cross-sell needed to about $1.06M (p. 16)")},
        {"label": "Cross-sell ramp", "cells": T("Assumption: linear from 0 to target by end-2028", "Average ARR over the period is half the target")},
        {"label": "Integration-era support", "cells": T("Evidence + assumption: $0.85M a year for 18 months, then ends", "Amount from the pack, duration assumed; a cost to cash or to the $4.0M cap (p. 5)")},
        {"label": "Partner economics", "cells": T("Assumption: same ARR range at 80% margin; $1.2M minimum fixed", "Conservative: crediting the minimum would improve the partnership case")},
        {"label": "Atlas core operations", "cells": T("Evidence: about cash-break-even", "No offset from, or drain on, core cash")},
        {"label": "Synergies, retention uplift", "cells": T("Evidence + choice: none", "The pack says not to assume savings; the routing-retention link is confounded")},
        {"label": "ARR at risk from churn", "cells": T("Assumption: 21% × $4.8M ≈ $1.0M a year", "Logo churn as a proxy for revenue churn; not in the base numbers")},
        {"label": "One routing strategy", "cells": T("Interpretation: partnering, then buying, counts as one", "If the board disagrees, the 2028 gate is partnership against build only")}]}})

# 20 · calculations (backup), split in two pages so the table reads at full size
CALC = [
        {"label": "Initial cash ceiling", "cells": T("$24.0M cash − $9.0M floor", "$15.0M")},
        {"label": "Path A / B cash out at close", "cells": T("18.0 + 4.0 / 11.0 + 3.5", "$22.0M / $14.5M")},
        {"label": "Operating drag, 18 months", "cells": T("−1.0 × 1.5 − 0.85 × 1.5 + (ARR ÷ 2) × 1.5 × 0.8; ARR 2.4 / 0.8", "−$1.3M / −$2.3M")},
        {"label": "Path B lowest cash", "cells": T("24.0 − 14.5 − 1.3 (base) / − 2.3 (low)", "$8.2M / $7.2M")},
        {"label": "Valuation multiples", "cells": T("18.0 ÷ 7.2 / 18.0 ÷ 4.8 / 11.0 ÷ 4.8", "2.5x / 3.75x / 2.3x")},
        {"label": "Acquisition run-rate contribution", "cells": T("0.8 × ARR − 0.85 − 1.0 (integration era); 0.8 × ARR − 1.0 (after)", "+0.07 / −1.21; +0.92 / −0.36")},
        {"label": "Partnership contribution and break-even", "cells": T("0.8 × 0.55 × ARR − 0.6; break-even 0.6 ÷ 0.44", "+0.46 / −0.25; $1.36M")},
        {"label": "Partner vs acquire crossover", "cells": T("0.44 × ARR − 0.6 = 0.8 × ARR − 1.85, so ARR = 1.25 ÷ 0.36", "$3.47M ARR")},
        {"label": "Build contribution and payback", "cells": T("1.3 × 0.8 − 0.4; 3.4 ÷ 0.64", "$0.64M a year; ≈5.3 years")},
        {"label": "Earnout funding period", "cells": T("7.0 ÷ 0.92 base-case run-rate contribution", "≈7.6 years")},
        {"label": "Upfront ceiling", "cells": T("15.0 − 4.0 − 2.3", "$8.7M → $8.5M")},
        {"label": "Concentration", "cells": T("58% × 4.8 ÷ 41 / 42% × 4.8 ÷ 269", "≈$68K / ≈$7.5K per account")}]
for sid, part, rows in (("20", "1/2", CALC[:6]), ("20b", "2/2", CALC[6:])):
    slides.append({
        "id": sid, "role": "backup", "backup_of": "8", "section_id": "2", "status": "filled",
        "lead_message": {"prefix": "BACKUP:", "text": f"Every figure in the deck traces to briefing-pack inputs through simple arithmetic ({part})"},
        "message_type": "item", "archetype": "data-table",
        "body": {"kind": "table", "table_type": "data", "columns": ["Calculation", "Result"], "rows": rows}})

# ------------------------------------------------------------------ storyline
storyline = {
    "governing_thought": "Do not buy RouteSprout on the proposed terms in 2027: partner now, and keep a conditional option to buy later at no more than $8.5M upfront",
    "exec_summary": [
        {"id": "1", "text": "Neither acquisition path stays inside the cash limits once 18 months of operating losses are counted", "supports": ["3", "4", "5"],
         "sub_points": [{"text": "Path A needs $22.0M against a $15.0M ceiling; Path B fits at signing but falls to $7.2M–8.2M, below the $9.0M floor", "slide_id": "4"},
                        {"text": "Nothing in the plan funds the $7.0M earnout due in 2029", "slide_id": "5"}]},
        {"id": "2", "text": "The value case is overstated, and buying takes more than 15 years to pay back", "supports": ["6", "7", "8"],
         "sub_points": [{"text": "$18.0M is 3.75 times recognized ARR, not the sellers' 2.5 times bookings", "slide_id": "6"},
                        {"text": "The $2.4M cross-sell is ARR, not EBITDA: net it adds about $0.1M a year, and loses $1.2M in the low case", "slide_id": "7"}]},
        {"id": "3", "text": "Customer and execution risk is high and is not priced into the deal case", "supports": ["9", "10"],
         "sub_points": [{"text": "Churn rose from 12% to 21%, 41 accounts hold 58% of ARR and 30% of integration is unscoped, yet sellers assume 100% renewal", "slide_id": "9"}]},
        {"id": "4", "text": "Only the partnership passes all four board criteria in 2027; building is affordable but late", "supports": ["11", "12", "13"],
         "sub_points": [{"text": "At most $1.2M at risk, live this summer, no migration, and it out-earns ownership below about $3.5M of ARR", "slide_id": "12"}]},
        {"id": "5", "text": "Buying stays possible, but only on conditional terms tested at a Q1 2028 gate", "supports": ["14", "15", "16", "17", "18"],
         "sub_points": [{"text": "Partner now with first refusal; buy later for at most $8.5M upfront plus up to $9.5M if earned", "slide_id": "15"},
                        {"text": "Buy only if six thresholds clear; integrate via the API and pay nothing that breaks the cash floor", "slide_id": "16"}]}],
    "next_steps": [
        {"action": "Decline the $18.0M all-cash proposal (Path A) and the staged deal as structured (Path B)", "owner": "Board", "timing": "Mar 2027"},
        {"action": "Approve and sign the two-year RouteSprout partnership with the protections on p. 14", "owner": "Board; CEO", "timing": "Mar–Jun 2027"},
        {"action": "Run preliminary diligence: QoE, customer cohorts, integration scoping, key-person review", "owner": "CFO", "timing": "Apr–Dec 2027"},
        {"action": "Negotiate the conditional term sheet: at most $8.5M upfront, up to $9.5M earned, set walk-away", "owner": "CEO; CFO", "timing": "Apr–Jun 2027"},
        {"action": "Decide at the gate: buy only if all six thresholds are met", "owner": "Board", "timing": "Q1 2028"}]}

sections = [
    {"id": "1", "title": "Cash", "exec_item_id": "1", "tracker_label": "Cash"},
    {"id": "2", "title": "Value and payback", "exec_item_id": "2", "tracker_label": "Value and payback"},
    {"id": "3", "title": "Customer continuity and execution", "exec_item_id": "3", "tracker_label": "Customers and execution"},
    {"id": "4", "title": "Alternatives", "exec_item_id": "4", "tracker_label": "Alternatives"},
    {"id": "5", "title": "Terms and next steps", "exec_item_id": "5", "tracker_label": "Terms"}]

# ------------------------------------------------------------------ compile block
U = []
def unit(i, typ, text, loc, crit, sids):
    U.append({"id": i, "type": typ, "text": text, "source_loc": loc, "critical": crit, "slide_ids": sids})

unit("u1", "answer", "Do not buy RouteSprout on the proposed terms in 2027; partner now and keep a conditional option to buy later at no more than $8.5M upfront", "p.2 title", True, ["es", "3", "17"])
unit("u2", "recommendation", "Reject the $18.0M all-cash deal (Path A) and the staged deal as structured (Path B)", "p.2, p.17", True, ["es", "17"])
unit("u3", "recommendation", "Sign a two-year RouteSprout partnership ($1.2M minimum, live summer 2027) with a right of first refusal and a pre-agreed conditional purchase option", "p.2, p.14, p.17", True, ["es", "14", "17"])
unit("u4", "gate", "Exercise the purchase option at a Q1 2028 gate only if six evidence thresholds are met", "p.2, p.16, p.17", True, ["es", "16", "17"])
unit("u5", "claim", "Path A needs $22.0M against a $15.0M ceiling ($24.0M − $9.0M); leaves $2.0M before operating losses", "p.2, p.4", True, ["es", "4", "11"])
unit("u6", "claim", "Path B fits at signing ($14.5M, $0.5M headroom) but 18 months of operating drag takes cash to $7.2–8.2M, below the $9.0M floor", "p.2, p.3, p.4", True, ["es", "3", "4", "11"])
unit("u7", "claim", "Nothing funds the $7.0M earnout due in 2029; base-case run-rate contribution of $0.92M/yr needs about 7.6 years", "p.2, p.5", True, ["es", "5"])
unit("u8", "risk", "30% of integration unscoped; every $1 overrun is $1 below the floor; if integration-era support counts toward the $4.0M cap, A = $5.3M and B = $4.8M breach it", "p.5", True, ["5"])
unit("u9", "risk", "Uptime service credits (99.7%) are unquantified and only run one way", "p.5", False, ["5"])
unit("u10", "claim", "Any acquisition must leave room for 18 months of losses, a contingency on unscoped work and an earnout that does not have to be paid in cash", "p.5 so what", True, ["5"])
unit("u11", "claim", "$18.0M is 3.75x recognized ARR, 50% above the sellers' 2.5x of bookings; bookings include multi-year contract value and pilots; no QoE; ARR unverified", "p.2, p.6", True, ["es", "6"])
unit("u12", "claim", "Path B total including the full earnout is also $18.0M (3.75x): structure moves timing, not amount", "p.6", False, ["6"])
unit("u13", "claim", "Cross-sell $2.4M is ARR not EBITDA; contribution +$0.07M base / −$1.21M low in integration era; +$0.92M / −$0.36M after support ends", "p.2, p.7", True, ["es", "7"])
unit("u14", "assumption", "About $1.0M of RouteSprout ARR at risk each year at 21% churn (logo churn as proxy), not in the base numbers", "p.7, p.9, p.19", False, ["7", "19"])
unit("u15", "claim", "Payback: A ≈24 years / never; B ≈16 (23 with earnout) / never; C ≈1.1 years, break-even $1.36M, max loss $1.2M; D ≈5.3 years after launch", "p.8", True, ["es", "8", "11"])
unit("u16", "method", "Simple undiscounted payback; no precise DCF from unavailable inputs; partner low end more likely", "p.8", False, ["8"])
unit("u17", "claim", "Logo churn rose from 12% to 21%; 58% of ARR in 41 accounts; sellers assume 100% renewal", "p.2, p.9", True, ["es", "9"])
unit("u18", "claim", "Account managers drive renewals; replacing the interface before large renewals risks churn; no cohort data, first diligence item", "p.9", True, ["9"])
unit("u19", "claim", "Synergy and retention claims rest on correlation (95% vs 78% renewal confounded; cited deals twice as large); no retention uplift credited, $2.4M not underwritten", "p.10", False, ["10"])
unit("u20", "condition", "Integrate through the API first; scope 100% of the work and price contingency before signing", "p.10, p.15", True, ["es", "10", "15"])
unit("u21", "condition", "Signed 24-month retention agreements for key engineers and account managers are a condition of the deal", "p.10, p.15, p.16", True, ["10", "15", "16"])
unit("u22", "claim", "Only the partnership passes all four board criteria in 2027; the build is the fallback, not the first move", "p.2, p.11", True, ["es", "11"])
unit("u23", "claim", "Partnership earns more than ownership below about $3.5M of routing ARR ($3.47M; $2.78M after support ends); capital excluded widens the lead", "p.2, p.12", True, ["es", "12"])
unit("u24", "assumption", "Partner-sold routing at the same 80% margin; $1.2M minimum fixed and not recoupable", "p.12, p.19", False, ["12", "19"])
unit("u25", "claim", "Building is affordable ($3.4M) but cannot ship before late 2028; misses renewal cycles; displaces the compliance upgrade; $1.3M ARR treated as 2029 run-rate", "p.2, p.13", True, ["es", "13"])
unit("u26", "recommendation", "Partnership terms: ask to credit the minimum, 99.7% SLA with credits passed back, information rights, segment exclusivity ask, escrow and data portability, clean team", "p.14", True, ["14"])
unit("u27", "gate", "Walk away from the partnership if RouteSprout refuses first refusal or change-of-control protection; reopen the build", "p.14", True, ["14"])
unit("u28", "recommendation", "Conditional purchase: at most $8.5M upfront (≈1.8x verified ARR), cut ≈1.8x per ARR shortfall; earnout up to $9.5M within $18.0M on four tests; paid only above floor plus buffer, deferred or in equity", "p.2, p.15", True, ["es", "15"])
unit("u29", "condition", "API plus SSO first; no interface replacement or record migration before large-account renewals; scoped budget ≤ $4.0M including support", "p.2, p.15", True, ["es", "15"])
unit("u30", "gate", "Walk away if sellers demand more than $8.5M upfront or all cash; keep the partnership", "p.15, p.18", True, ["15", "18"])
unit("u31", "claim", "Upfront ceiling derivation: 15.0 − 4.0 − 2.3 = 8.7 → 8.5; drops $1-for-$1 for uncredited fees or budget above cap; $0.2M buffer thin", "p.15", True, ["15"])
unit("u32", "gate", "Six thresholds: QoE ARR ≥ $4.8M; churn toward 12% and stable top-41; signed demand ≥ $1.36M (≈$2.3M to cover losses); EBITDA breakeven needs ≈$1.06M; scoped budget ≤ $4.0M; retention agreements and ≤ $8.5M upfront", "p.16", True, ["16"])
unit("u33", "gate", "Early trigger: if a competing buyer emerges, use ROFR on pre-agreed terms only if items 1, 2 and 5 have cleared", "p.16, p.17", True, ["16", "17"])
unit("u34", "next_steps", "Five March 2027 decisions and the sequence to the Q1 2028 gate; CFO sizes the diligence budget", "p.17", True, ["17"])
unit("u35", "assumption", "Partnering in 2027 then buying in 2028 counts as one routing strategy; if the board disagrees the gate is partnership vs build only", "p.17, p.19", True, ["17", "19"])
unit("u36", "risk", "Five risks with mitigations and residual exposure; cash downside capped at $1.2M", "p.18", True, ["18"])
unit("u37", "claim", "Starting hypothesis (staged purchase in 2027) fails four of five tests; customer protection unproven; revised answer partner now, buy as an option", "p.3", False, ["3"])
unit("u38", "assumption", "Assumptions register (close timing, EBITDA flat, linear ramp, support duration, partner economics, no synergies)", "p.19", False, ["19"])
unit("u39", "method", "Calculation trail for every figure", "p.20", False, ["20", "20b"])

n_crit = sum(1 for u in U if u["critical"])
compile_block = {
    "source": "evidence/analysis.md (finished board deck, 20 slides, extracted to text); numbers checked against evidence/briefing-pack.md",
    "variant": "restyle",
    "units": U,
    "untraceable": [
        {"data_point_id": "mo18", "critical": True,
         "ack": "Kept as the analysis's stated timing assumption (close July 2027 after a March board and about 3 months of diligence, so 18 months to end-2028); not in the pack; shown on p.4 as an assumption. Chosen without the user (unavailable), as recommended",
         "note": "Drives the operating drag (1.5 years) behind the cash-floor title and the upfront ceiling"},
        {"data_point_id": "up85", "critical": True,
         "ack": "Kept as the analysis's recommended ceiling: a judgement rounded down from the $8.7M maximum affordable upfront, which is recomputed from the pack (15.0 − 4.0 − 2.3). Chosen without the user (unavailable), as recommended",
         "note": "Policy choice, not a pack figure; its upper bound is traceable"},
        {"data_point_id": "dilmo", "critical": False, "note": "Diligence length (about 3 months) is the analysis's assumption; only used for timeline placement"},
        {"data_point_id": "bandlo", "critical": False, "note": "Lower earnout band ($1.4M) is a proposed term in the analysis; not stated in the pack (close to the $1.36M partnership break-even)"}],
    "check": {"critical_units": n_crit, "preserved": n_crit,
              "notes": "Read unit by unit against the slides: every critical unit is on a main-deck slide with the source's numbers, conditions and option ranking (partner > conditional buy > build fallback > A/B rejected). No corrections: every number in the source reproduces from the pack or from its stated assumptions. Wording changes only: slide 3 title names the unproven test (customer protection) instead of 'the fifth', since test 5 is itself a Fail; slide 7 title shortened with the low case in brackets; British spellings made American."}}

spec = {
    "spec_version": "0.1", "mode": "deck_detailed",
    "meta": {"title": "Routing strategy: partner with RouteSprout now, and buy only on conditional terms",
             "subtitle": "Board pre-read for the March 2027 meeting · Should Atlas buy RouteSprout in 2027, and on what terms, rather than build or partner?",
             "company_name": "Atlas FieldOps", "audience": "Board of Directors",
             "purpose": "Decide whether to buy RouteSprout in 2027, and on what terms, rather than build or partner",
             "date": "2026-11-20", "language": "en-US",
             "confidentiality": "Synthetic benchmark data · figures from the briefing pack or labelled team assumptions · $ in millions unless stated",
             "theme": "navy"},
    "inputs": [
        {"id": "in-1", "kind": "file", "label": "Atlas FieldOps briefing pack (synthetic benchmark data)", "content": "evidence/briefing-pack.md"},
        {"id": "in-2", "kind": "file", "label": "Finished board deck to compile (analysis)", "content": "evidence/analysis.md"}],
    "storyline": storyline, "sections": sections, "slides": slides, "data_points": DPS,
    "sources": [
        {"id": "s1", "kind": "user_provided", "name": "Atlas FieldOps briefing pack (synthetic benchmark data)", "input_id": "in-1"},
        {"id": "s2", "kind": "user_provided", "name": "Team assumptions stated in the source analysis", "input_id": "in-2"},
        {"id": "s0", "kind": "derived", "name": "Team analysis of the briefing pack"}],
    "compile": compile_block}

with open(OUT, "w") as f:
    json.dump(spec, f, ensure_ascii=False, indent=1)
print("wrote", OUT, len(DPS), "data points", n_crit, "critical units")

# ------------------------------------------------------------------ numbers written in slide text (tables, bullets, bars)
# The renderer links only point cells to the workbook; these lists let postprocess.py add the text numbers too.
TEXT_REFS = {
    "3": ["floor", "bhead0", "bminl", "bminb", "earn", "multa", "smult", "conb", "conl", "payb", "uptime", "churn24", "churn26", "renew100", "cross", "cmin"],
    "4": ["aout", "aleft", "ceil", "cash", "floor", "xsell", "xlow", "dcost", "mo18", "bhead0", "bminb", "bminl", "dragl"],
    "5": ["bhead0", "ebitda", "support", "dragb", "dragl", "floor", "unscoped", "bint", "intleft", "intcap", "capa", "capb", "sup18", "earn", "runb", "earnyrs", "uptime", "mo18"],
    "6": ["bookings", "arr", "price", "bup", "growth", "ebitda", "btotal"],
    "7": ["xsell", "xlow", "gmx", "gpb", "gpl", "support", "xcb", "xcl", "ebitda", "conb", "conl", "runb", "runl", "riskarr", "churn26", "arr", "renew100"],
    "8": ["aout", "bout", "earn", "cmin", "dcost", "dops", "runb", "runl", "conb", "conl", "pcb", "pcl", "pmin", "paya", "payb", "paybe", "payc", "bec", "pcl2", "dcon", "barr", "gmx", "splita", "xsell", "xlow"],
    "9": ["topn", "topshare", "pertop", "peroth", "othn", "churn24", "churn26", "renew100"],
    "10": ["ren95", "ren78", "integ", "unscoped", "smult", "bookings", "xsell", "retyrs", "retmo"],
    "11": ["floor", "aout", "aleft", "bout", "bminl", "bminb", "cmin", "ccash", "dcost", "dcash", "paya", "payb", "paybe", "bec", "churn26", "unscoped", "payd", "bmonths"],
    "12": ["xlow", "xsell", "pcl", "conl", "pcb", "conb", "cross2", "bout", "aout", "gmx", "cmin", "pgm", "pmin", "afix", "gdiff", "gapfix", "crossv", "ebitda", "support"],
    "13": ["dcost", "dops", "dcon", "barr", "gmx", "payd", "bmonths", "dilmo"],
    "14": ["cmin", "splita", "splitr", "bec", "uptime", "ebitda"],
    "15": ["price", "churn24", "bandlo", "xsell", "uptime", "floor", "intcap", "retmo", "upmult", "buf", "arr"],
    "16": ["arr", "churn26", "churn24", "xsell", "bec", "needloss", "ebitda", "needbe", "support", "gmx", "intcap", "unscoped", "retmo", "price", "up85", "upmult"],
    "17": ["price", "cmin", "up85", "earn95", "topn"],
    "18": ["bec", "cmin", "splitr", "pcl2", "ebitda", "churn26", "uptime", "price"],
    "19": ["mo18", "dilmo", "ebitda", "growth", "churn26", "needbe", "support", "intcap", "xsell", "gmx", "cmin", "arr", "riskarr"],
    "20": ["ceil", "cash", "floor", "aout", "bout", "price", "integ", "bup", "bint", "dragb", "dragl", "bminb", "bminl", "smult", "multa", "multb"],
    "20b": ["pcb", "pcl", "bec", "cross", "dcon", "payd", "earnyrs", "maxup", "up85", "pertop", "peroth", "conb", "conl", "runb", "runl"]}
for sid_, ids in TEXT_REFS.items():
    for i in ids:
        assert i in _ids, (sid_, i)
with open(os.path.join(HERE, "text_refs.json"), "w") as f:
    json.dump(TEXT_REFS, f, indent=1)
