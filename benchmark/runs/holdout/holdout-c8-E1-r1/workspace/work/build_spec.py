"""Builds the storyline spec for the Northline Home East DC decision deck.

Every number comes from evidence/briefing-pack.md (source s1) or is derived from those numbers (source s0).
"""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
PACK = (ROOT / "evidence" / "briefing-pack.md").read_text()

DP = []


def src(id_, label, value, unit, excerpt, locator, period="2027", slide="1", used_in="", **kw):
    d = {"id": id_, "slide_id": slide, "label": label, "value": value, "unit": unit, "period": period,
         "source_id": "s1", "excerpt": excerpt, "locator": locator}
    if used_in:
        d["used_in"] = used_in
    d.update(kw)
    DP.append(d)


def der(id_, label, value, unit, derived_from, formula, calc, period="2027", slide="1", used_in="", estimate=False,
        assumptions=None, **kw):
    d = {"id": id_, "slide_id": slide, "label": label, "value": value, "unit": unit, "period": period,
         "source_id": "s0", "derived_from": derived_from, "formula": formula, "calc": calc}
    if used_in:
        d["used_in"] = used_in
    if estimate:
        d["estimate"] = True
        d["assumptions"] = assumptions or []
    d.update(kw)
    DP.append(d)


T3 = "Briefing pack §3, volumes and costs table"
T4 = "Briefing pack §4, service and capacity table"

# ------------------------------------------------------------------ inputs from the briefing pack
src("vE", "East DC 2027 annual shipments (East → East)", 200000, "shipments",
    '"East → East", column "2027 annual shipments" = "200,000"', T3, slide="1")
src("vC", "Central DC 2027 annual shipments (Central → Central)", 160000, "shipments",
    '"Central → Central", column "2027 annual shipments" = "160,000"', T3, slide="3")
src("vW", "West DC 2027 annual shipments (West → West)", 140000, "shipments",
    '"West → West", column "2027 annual shipments" = "140,000"', T3, slide="3")
src("tE", "Transport cost per shipment, East → East", 8, "$",
    '"East → East", column "Current transport per shipment" = "$8"', T3, slide="1",
    definition="parcel label plus carrier line haul; excludes warehouse fixed cost, damage and exit charge")
src("tC2E", "Transport cost per shipment, Central → East if East closes", 13, "$",
    '"Central → East if East closes", column "Current transport per shipment" = "$13"', T3, slide="1",
    definition="parcel label plus carrier line haul; excludes the carrier surcharge needed to improve service")
src("tX", "Transport cost per shipment, Eastern third-party cross-dock", 11, "$",
    '"Eastern third-party cross-dock", column "Current transport per shipment" = "$11"', T3, slide="6")
src("fE", "East DC fixed facility cost per year", 1.3, "$M",
    '"East → East", column "Fixed facility cost/year" = "$1.30M"', T3, slide="1")
src("fX", "Cross-dock minimum annual commitment", 0.85, "$M",
    '"Eastern third-party cross-dock", column "Fixed facility cost/year" = "$0.85M minimum annual commitment"', T3,
    slide="6", definition="read as a fixed annual fee on top of freight, because the pack lists it in the fixed facility cost column")
src("dmg", "Additional annual damage and handling if East closes and Central ships Eastern orders", 0.2, "$M",
    '"Additional annual damage/handling", column "Close and ship from Central" = "$0.20M"', T4, slide="1")
src("exit", "One-time East lease termination fee in 2027", 0.75, "$M",
    "The East lease can be terminated in 2027 for a one-time $0.75M fee.", "Briefing pack §2, board commitments",
    slide="2")
src("cfo", "Annual saving claimed on the CFO's slide for closing East", 1.3, "$M",
    'The CFO\'s slide calls closure a "$1.3M annual saving" because it removes the East site\'s fixed cost.',
    "Briefing pack §5, claims circulated", slide="b1")
src("slaT", "Board commitment: share of all customer orders delivered within two calendar days", 0.92, "%",
    "At least 92% of all customer orders must be delivered within two calendar days.",
    "Briefing pack §2, board commitments", slide="3", definition="all orders, all ZIP codes; the contracted KPI")
src("capC", "Central DC certified practical capacity", 360000, "shipments",
    "The Central warehouse has a certified practical capacity of 360,000 shipments/year under its current staffing and fire-code permit.",
    "Briefing pack §2, board commitments", slide="4", period="per year")
src("retro", "Central expansion retrofit cost", 1.1, "$M",
    "Expanding it requires a two-quarter permit application and a $1.1M retrofit that the 2027 budget does not include.",
    "Briefing pack §2, board commitments", slide="5")
src("budget", "One-time network change budget authorized for 2027", 0.9, "$M",
    "The board authorizes only $0.9M of one-time network change costs in 2027.",
    "Briefing pack §2, board commitments", slide="5")
src("rK", "Eastern two-day on-time rate, keep East (all-ZIP)", 0.96, "%",
    '"2027 Eastern two-day on-time rate", column "Keep East" = "96%"', T4, slide="3")
src("rClose", "Eastern two-day on-time rate, close and ship from Central (modeled)", 0.84, "%",
    '"2027 Eastern two-day on-time rate", column "Close and ship from Central" = "84% modeled"', T4, slide="3")
src("rX", "Eastern two-day on-time rate, outsourced cross-dock (pilot)", 0.93, "%",
    '"2027 Eastern two-day on-time rate", column "Outsource East cross-dock" = "93% pilot"', T4, slide="3")
src("rW", "West two-day on-time rate at current routing", 0.95, "%",
    "West and Central deliveries are currently 95% and 94% within two days, respectively, at their current routing.",
    "Briefing pack §4, text under the table", slide="3")
src("rC", "Central two-day on-time rate at current routing", 0.94, "%",
    "West and Central deliveries are currently 95% and 94% within two days, respectively, at their current routing.",
    "Briefing pack §4, text under the table", slide="3")
src("gE", "Eastern demand growth assumption, 2028", 0.10, "%",
    "The commercial forecast shows Eastern demand up 10% and Central demand up 6% in 2028; West remains flat.",
    "Briefing pack §4", slide="2", period="2028")
src("gC", "Central-region demand growth assumption, 2028", 0.06, "%",
    "The commercial forecast shows Eastern demand up 10% and Central demand up 6% in 2028; West remains flat.",
    "Briefing pack §4", slide="4", period="2028")
src("loadC27", "Central hub 2027 load if East closes", 360000, "shipments",
    '"Central hub 2027 load", column "Close and ship from Central" = "360,000"', T4, slide="4")
src("kSav", "Option K annual saving (facility audit estimate)", 0.3, "$M",
    "a facility audit estimates savings of $0.30M/year, with $0.15M upfront in systems changes.",
    "Briefing pack §6, alternative designs", slide="6", period="per year from 2027")
src("kUp", "Option K upfront systems cost", 0.15, "$M",
    "a facility audit estimates savings of $0.30M/year, with $0.15M upfront in systems changes.",
    "Briefing pack §6, alternative designs", slide="7", period="one-time, 2027")
src("pilot", "Eastern orders in the cross-dock pilot", 12000, "orders",
    "The outsourced cross-dock's 93% result came from a six-week pilot covering 12,000 Eastern orders and excludes holiday weeks.",
    "Briefing pack §4, text under the table", slide="8", period="six-week pilot, holiday weeks excluded")
src("reopen", "Time to return an East-style fulfillment center after closure", 9, "months",
    "The COO notes that returning an East-style fulfillment center after closure would take nine months and expensive customer migrations.",
    "Briefing pack §7, risks", slide="5", period="after closure")
src("xTerm", "Minimum term of the cross-dock contract", 2, "years",
    "Option X terminates East and signs a two-year minimum with a cross-dock provider.",
    "Briefing pack §6, alternative designs", slide="8", period="from signing")
src("fin98", "East two-day rate on Finance's headline (rural deliveries excluded)", 0.98, "%",
    'Finance also circulated a headline "East delivers 98% in two days" based on an internal report that excluded rural deliveries; the contract-compliant all-ZIP measure is 96%.',
    "Briefing pack §5, claims circulated", slide="b1")
src("mkt8", "Renewal gap claimed by Marketing for Eastern customers served by East", 8, "pp",
    'Marketing says "Eastern customers renew 8 percentage points more often when served by East, so the warehouse causes loyalty."',
    "Briefing pack §5, claims circulated", slide="b1", period="not stated")

# ------------------------------------------------------------------ derived numbers
der("trStep", "Higher freight on Eastern orders shipped from Central", -1.0, "$M", ["vE", "tE", "tC2E"],
    "200,000 × ($8 − $13)", "vE * (tE - tC2E) / 1000000", slide="1", used_in="waterfall step")
der("dmgStep", "Extra damage and handling if East closes (as a negative step)", -0.2, "$M", ["dmg"],
    "0 − $0.20M", "0 - dmg", slide="1", used_in="waterfall step")
der("sav27", "Net annual saving from closing East, 2027 volumes", 0.1, "$M", ["fE", "vE", "tC2E", "tE", "dmg"],
    "$1.30M − 200,000 × ($13 − $8) − $0.20M", "fE - vE * (tC2E - tE) / 1000000 - dmg", slide="1",
    used_in="waterfall total, titles, exec summary")
der("eaten", "Share of East's fixed-cost saving absorbed by higher freight and damage", 0.923, "%",
    ["vE", "tC2E", "tE", "dmg", "fE"], "($1.0M + $0.20M) ÷ $1.30M", "(vE * (tC2E - tE) / 1000000 + dmg) / fE",
    slide="1", used_in="sidebar row")
der("payback", "Years for the 2027 saving to repay the $0.75M exit fee", 7.5, "years", ["exit", "sav27"],
    "$0.75M ÷ $0.10M a year", "exit / sav27", slide="1", used_in="sidebar row")

A28 = ["Eastern demand grows 10% in 2028 (commercial forecast), so Eastern shipments reach 220,000",
       "Transport from Central stays at $13 against $8 from East, with no carrier surcharge",
       "Extra damage held at $0.20M a year; if it grows with volume, the 2028 result is slightly worse for closure",
       "Central fixed cost is unchanged and no retrofit is counted"]
der("vE28", "Eastern shipments in 2028 at forecast growth", 220000, "shipments", ["vE", "gE"],
    "200,000 × (1 + 10%)", "vE * (1 + gE)", period="2028", slide="2", estimate=True,
    assumptions=["Eastern demand grows 10% in 2028, per the commercial forecast, which includes a marketplace promotion not yet contracted"])
der("sav27k", "Net annual saving from closing East, 2027 volumes, in $ thousands", 100, "$K", ["sav27"],
    "$0.10M × 1,000", "sav27 * 1000", slide="2", used_in="equation term")
der("exitk", "One-time East lease termination fee, in $ thousands", 750, "$K", ["exit"],
    "$0.75M × 1,000", "exit * 1000", slide="2", used_in="equation term")
der("sav28", "Net annual saving from closing East, 2028 at forecast growth", 0, "$K", ["fE", "vE28", "tC2E", "tE", "dmg"],
    "($1.30M − 220,000 × ($13 − $8) − $0.20M) × 1,000", "(fE - vE28 * (tC2E - tE) / 1000000 - dmg) * 1000", period="2028", slide="2",
    estimate=True, assumptions=A28)
der("net2y", "Net result of closing East in January 2027, through the 2029 lease end", -650, "$K",
    ["sav27k", "sav28", "exitk"], "$100K + $0K − $750K", "sav27k + sav28 - exitk", period="2027–28", slide="2",
    estimate=True, assumptions=A28 + ["Closure takes effect on January 1, 2027; a June close would halve the 2027 saving"])
der("netK", "Network two-day on-time rate, keep East", 0.9508, "%", ["vE", "rK", "vC", "rC", "vW", "rW"],
    "(200,000 × 96% + 160,000 × 94% + 140,000 × 95%) ÷ 500,000",
    "(vE * rK + vC * rC + vW * rW) / (vE + vC + vW)", slide="3", used_in="bar")
der("netX", "Network two-day on-time rate, outsourced Eastern cross-dock", 0.9388, "%", ["vE", "rX", "vC", "rC", "vW", "rW"],
    "(200,000 × 93% + 160,000 × 94% + 140,000 × 95%) ÷ 500,000",
    "(vE * rX + vC * rC + vW * rW) / (vE + vC + vW)", slide="3", used_in="bar")
der("netClose", "Network two-day on-time rate, close East and ship from Central", 0.9028, "%",
    ["vE", "rClose", "vC", "rC", "vW", "rW"], "(200,000 × 84% + 160,000 × 94% + 140,000 × 95%) ÷ 500,000",
    "(vE * rClose + vC * rC + vW * rW) / (vE + vC + vW)", slide="3", used_in="bar, title, exec summary")
der("shareE", "East's share of all 2027 network orders", 0.4, "%", ["vE", "vC", "vW"], "200,000 ÷ 500,000",
    "vE / (vE + vC + vW)", slide="3", used_in="sidebar header")
der("reqE", "Eastern two-day rate needed for the network to reach 92%", 0.883, "%",
    ["slaT", "vE", "vC", "vW", "rC", "rW"], "(92% × 500,000 − 160,000 × 94% − 140,000 × 95%) ÷ 200,000",
    "(slaT * (vE + vC + vW) - vC * rC - vW * rW) / vE", slide="3", used_in="sidebar big number")
der("util27", "Central load as a share of certified capacity, 2027, if East closes", 1.0, "%", ["loadC27", "capC"],
    "360,000 ÷ 360,000", "loadC27 / capC", slide="4", used_in="exec summary")
der("loadK28", "Central's own load in 2028 at forecast growth", 169600, "shipments", ["vC", "gC"],
    "160,000 × (1 + 6%)", "vC * (1 + gC)", period="2028", slide="4", estimate=True,
    assumptions=["Central-region demand grows 6% in 2028, per the commercial forecast"])
der("loadC28", "Central load in 2028 if East closes, at forecast growth", 389600, "shipments", ["loadK28", "vE28"],
    "169,600 + 220,000", "loadK28 + vE28", period="2028", slide="4", estimate=True,
    assumptions=["Central-region demand grows 6% and Eastern demand 10% in 2028, per the commercial forecast",
                 "All Eastern orders ship from Central"])
der("over28", "Amount by which Central's 2028 load would exceed its certified capacity if East closes", 0.0822, "%",
    ["loadC28", "capC"], "389,600 ÷ 360,000 − 1", "loadC28 / capC - 1", period="2028", slide="4", estimate=True,
    assumptions=["Central-region demand grows 6% and Eastern demand 10% in 2028, per the commercial forecast"])
der("surBE", "Carrier surcharge per Eastern shipment equal to the whole closure saving", 50, "cents",
    ["sav27", "vE"], "$0.10M ÷ 200,000 shipments", "sav27 * 1000000 / vE * 100", slide="5", used_in="KPI tile")
der("oneC", "One-time cost of closing East and expanding Central", 1.85, "$M", ["exit", "retro"],
    "$0.75M + $1.1M", "exit + retro", slide="5", used_in="KPI tile")
der("oneCx", "One-time cost of exiting East and expanding Central as a multiple of the 2027 one-time budget", 2.0556, "x",
    ["oneC", "budget"], "$1.85M ÷ $0.9M", "oneC / budget", slide="5", used_in="KPI tile")
der("costKeep", "Annual cost of serving Eastern orders, keep East as today", 2.9, "$M", ["vE", "tE", "fE"],
    "200,000 × $8 + $1.30M", "vE * tE / 1000000 + fE", slide="6", used_in="bar")
der("costK", "Annual cost of serving Eastern orders, Option K (keep and optimize)", 2.6, "$M", ["costKeep", "kSav"],
    "$2.90M − $0.30M", "costKeep - kSav", slide="6", used_in="bar, title")
der("costC", "Annual cost of serving Eastern orders, close East and ship from Central", 2.8, "$M", ["vE", "tC2E", "dmg"],
    "200,000 × $13 + $0.20M (Central fixed cost unchanged)", "vE * tC2E / 1000000 + dmg", slide="6", used_in="bar")
der("costX", "Annual cost of serving Eastern orders, outsourced cross-dock", 3.05, "$M", ["vE", "tX", "fX"],
    "200,000 × $11 + $0.85M", "vE * tX / 1000000 + fX", slide="6", used_in="bar")
der("perK", "All-in cost per Eastern shipment, Option K", 13, "$", ["costK", "vE"], "$2.60M ÷ 200,000",
    "costK * 1000000 / vE", slide="6", used_in="sidebar row")
der("perKeep", "All-in cost per Eastern shipment, keep East as today", 14.5, "$", ["costKeep", "vE"], "$2.90M ÷ 200,000",
    "costKeep * 1000000 / vE", slide="6", used_in="sidebar row")
der("xExtra", "Extra annual cost of the cross-dock compared with keeping East as today", 0.15, "$M", ["costX", "costKeep"],
    "$3.05M − $2.90M", "costX - costKeep", slide="6", used_in="exec summary")
der("beVolK", "Eastern volume at which closure and Option K cost the same", 160000, "shipments",
    ["fE", "kSav", "dmg", "tC2E", "tE"], "($1.30M − $0.30M − $0.20M) ÷ ($13 − $8)",
    "(fE - kSav - dmg) * 1000000 / (tC2E - tE)", slide="7", used_in="table verdict")
der("beX", "Cross-dock freight per shipment at which it matches Option K's annual cost", 8.75, "$",
    ["costK", "fX", "vE"], "($2.60M − $0.85M) ÷ 200,000", "(costK - fX) * 1000000 / vE", slide="8", used_in="column text")
der("beXcut", "Cut in the cross-dock's $11 freight rate needed to match Option K", 0.20454545, "%", ["beX", "tX"],
    "1 − $8.75 ÷ $11", "1 - beX / tX", slide="8", used_in="column point")
der("xLock", "Minimum commitment locked in by the two-year cross-dock contract", 1.7, "$M", ["xTerm", "fX"],
    "2 years × $0.85M", "xTerm * fX", slide="8", used_in="column text")
der("costXfl", "Annual cost of the cross-dock if the $0.85M is a spending floor rather than a fee", 2.2, "$M", ["vE", "tX"],
    "200,000 × $11 (above the $0.85M floor)", "vE * tX / 1000000", slide="8", used_in="column text, table")
der("savHi", "Annual closure saving if transshipment adds no damage", 0.3, "$M", ["fE", "vE", "tC2E", "tE"],
    "$1.30M − 200,000 × ($13 − $8)", "fE - vE * (tC2E - tE) / 1000000", slide="10", used_in="table")
der("payHi", "Years to repay the exit fee if transshipment adds no damage", 2.5, "years", ["exit", "savHi"],
    "$0.75M ÷ $0.30M a year", "exit / savHi", slide="10", used_in="table")
der("allIn", "All-in cost per Eastern shipment at East today (transport plus facility)", 14.5, "$", ["costKeep", "vE"],
    "$2.90M ÷ 200,000", "costKeep * 1000000 / vE", slide="b1", used_in="table")


def p(ref):
    return {"data_ref": ref}


# ------------------------------------------------------------------ storyline
storyline = {
    "governing_thought": "Keep the East DC open in 2027 and optimize it: closing saves only $0.1M a year while breaking the 92% two-day commitment and Central's capacity",
    "exec_summary": [
        {"id": "1", "text": "Closing East saves $0.1M a year, not $1.3M, and would lose $650K before the East lease ends in 2029",
         "supports": ["1", "2"],
         "sub_points": [
             {"text": "Higher freight from Central and extra damage absorb 92% of the fixed-cost saving the CFO's slide counts", "slide_id": "1"},
             {"text": "With 10% Eastern growth the 2028 saving falls to zero, so the $0.75M exit fee is never recovered", "slide_id": "2"}]},
        {"id": "2", "text": "Closure also breaks the board's hard limits: the 92% two-day contract KPI and Central's permitted capacity",
         "supports": ["3", "4", "5"],
         "sub_points": [
             {"text": "Network two-day delivery would fall to 90.3% of orders, while keeping East delivers 95.1%", "slide_id": "3"},
             {"text": "Central would run at 100% of its permit in 2027 and about 8% above it in 2028", "slide_id": "4"},
             {"text": "Fixing service or capacity would cost more than the saving or the $0.9M one-time budget allows", "slide_id": "5"}]},
        {"id": "3", "text": "Retaining and optimizing East (Option K) is the cheapest design that meets every commitment",
         "supports": ["6", "7", "8"],
         "sub_points": [
             {"text": "Option K serves Eastern orders for $2.6M a year, compared with $2.8M for closure and $3.05M for the cross-dock", "slide_id": "6"},
             {"text": "Option K is the only design that passes service, capacity, budget and reversibility tests", "slide_id": "7"},
             {"text": "The cross-dock's 93% rests on a 12,000-order pilot without holiday weeks, and its fee terms are unclear", "slide_id": "8"}]},
        {"id": "4", "text": "Approve Option K now and settle East's future at the 2029 lease end, after a holiday-peak cross-dock test",
         "supports": ["9", "10"],
         "sub_points": [
             {"text": "Option K starts in the first half of 2027; the board takes the 2029 lease decision in mid-2028", "slide_id": "9"},
             {"text": "Only a cross-dock fee that proves to be a spending floor, plus proven peak service, would change the answer", "slide_id": "10"}]},
    ],
    "next_steps": [
        {"action": "Approve Option K and its $0.15M systems budget; renegotiate East shifts and set up the low-volume SKU transfer buffer",
         "owner": "COO with East site lead", "timing": "Decision Dec 2026; live by Q2 2027"},
        {"action": "Report the contracted all-ZIP two-day KPI, not the rural-excluded rate, on the board dashboard",
         "owner": "VP Customer Operations", "timing": "From Jan 2027"},
        {"action": "Get a written cross-dock re-quote: all-ZIP service, a peak guarantee, termination for cause, and whether the $0.85M is a fee or a floor",
         "owner": "CFO with procurement", "timing": "Q1–Q2 2027"},
        {"action": "Run the cross-dock through the 2027 holiday peak and measure true damage on transshipped goods",
         "owner": "VP Customer Operations", "timing": "Q4 2027"},
        {"action": "Bring the 2029 East lease decision to the board with test results, East renewal terms and 2028 demand actuals",
         "owner": "CEO and CFO", "timing": "Mid-2028"},
    ],
}

decision_audit = {
    "constraints": [
        {"item": "92% of all orders delivered within two days, measured on all ZIP codes (contract KPI)", "reflected": True,
         "effect": "closure drops the network to 90.3%, so it fails; the deck uses the all-ZIP 96% for East, not the 98% rural-excluded headline",
         "slide_ids": ["3", "b1"]},
        {"item": "Central certified capacity of 360,000 shipments a year; expansion needs a $1.1M retrofit and a two-quarter permit outside the 2027 budget",
         "reflected": True, "effect": "closure fills Central in 2027 and overruns it in 2028 at any positive growth", "slide_ids": ["4", "5"]},
        {"item": "One-time budget of $0.9M for 2027", "reflected": True,
         "effect": "Option K's $0.15M fits; closure plus retrofit needs $1.85M", "slide_ids": ["5", "7"]},
        {"item": "East exit fee of $0.75M, payable only for a 2027 exit; lease otherwise expires in 2029", "reflected": True,
         "effect": "included in the two-year closure result and in the case for deciding at the 2029 lease end, when no fee applies",
         "slide_ids": ["2", "9"]},
        {"item": "Higher Central → East freight ($13 against $8) and $0.20M extra damage", "reflected": True,
         "effect": "turn the CFO's $1.3M into $0.1M a year", "slide_ids": ["1"]},
        {"item": "Carrier surcharge needed to improve closure's service, not priced", "reflected": True,
         "effect": "any surcharge above 50 cents per shipment erases the saving", "slide_ids": ["5", "10"]},
        {"item": "Customer service may not be deliberately degraded for a freight discount", "reflected": True,
         "effect": "closure cuts Eastern on-time delivery from 96% to 84% to save fixed cost; noted on the service slide", "slide_ids": ["3"]},
        {"item": "Option K's $0.15M upfront cost and an audit-only saving estimate", "reflected": True,
         "effect": "the answer holds even if the saving is zero, because keeping East as today still beats closure over 2027–28",
         "slide_ids": ["6", "10"]},
        {"item": "Cross-dock two-year minimum term", "reflected": True,
         "effect": "locks in $1.7M of commitment before holiday service is proven", "slide_ids": ["8"]},
    ],
    "alternatives": [
        {"option": "Outsource Eastern orders to a third-party cross-dock now (Option X)", "verdict": "rejected",
         "why": "costs $0.15M a year more than today's East on the additive reading of its fee, adds the $0.75M exit fee, and its 93% comes from a six-week pilot without holiday weeks",
         "triage": "body", "slide_ids": ["6", "7", "8"]},
        {"option": "Keep East and optimize it, but get a re-quote from the cross-dock now (all-ZIP terms, fee or floor) and test it at holiday peak for the 2029 lease end",
         "verdict": "adopted", "why": "the sceptic's cheaper middle path; it becomes the recommendation's second half and costs nothing until 2029",
         "triage": "body", "slide_ids": ["9"]},
        {"option": "Close East but stage it (June 2027 close, as in the cost consultant's draft)", "verdict": "rejected",
         "why": "halves the 2027 saving, still pays the full exit fee and still puts Central at its full permitted load",
         "triage": "body", "slide_ids": ["2", "b1"]},
    ],
    "failure_threshold": {
        "driver": "Whether the cross-dock's $0.85M minimum annual commitment is a fee on top of freight or a spending floor",
        "threshold": "if it is a floor, the cross-dock costs $2.2M a year and beats Option K, but only once holiday service is proven above the 88.3% Eastern rate the network needs; closure never wins (it loses to K at any Eastern volume above 160,000)",
        "range": "closure saving low / base / high: $0.0M (2028 growth) / $0.1M (2027) / $0.3M (no extra damage); payback 2.5 years even in the high case, beyond the 2029 lease end",
        "triage": "body", "slide_ids": ["8", "10"]},
    "consistency": {"headline": storyline["governing_thought"], "holds": True,
                    "fix": "Titles say the cross-dock is unproven rather than ruled out, because the floor reading of its fee would make it cheaper than Option K"},
}

sections = [
    {"id": "1", "title": "The real saving from closure", "exec_item_id": "1", "tracker_label": "Cost"},
    {"id": "2", "title": "Service and capacity limits", "exec_item_id": "2", "tracker_label": "Limits"},
    {"id": "3", "title": "The options compared", "exec_item_id": "3", "tracker_label": "Options"},
    {"id": "4", "title": "Recommendation and plan", "exec_item_id": "4", "tracker_label": "Plan"},
]

SRC_NOTE = "All figures from the Northline Home briefing pack; calculations in the source workbook"


def nav(id_, sec):
    return {"id": id_, "role": "section_divider", "section_id": sec, "status": "filled",
            "archetype": "section-divider", "message_type": "navigation"}


slides = [
    {"id": "c", "role": "cover", "status": "filled"},
    {"id": "es", "role": "exec_summary", "status": "filled", "archetype": "exec-summary", "message_type": "navigation"},
    nav("d1", "1"),
    # ---------------------------------------------------------------- S1 waterfall
    {"id": "1", "role": "content", "section_id": "1", "status": "filled",
     "lead_message": {"text": "The CFO's $1.3M closure saving shrinks to $0.1M a year once Eastern orders pay Central's freight and damage costs",
                      "numbers": [{"text": "$1.3M", "data_ref": "fE"}, {"text": "$0.1M", "data_ref": "sav27"}],
                      "highlights": ["Net annual saving"], "clauses": 1},
     "message_type": "component", "archetype": "waterfall-bridge",
     "rationale": "What adds up to the net saving -> waterfall from the fixed cost removed to the net saving",
     "unit_line": "**Annual saving from closing East and serving Eastern orders from Central**, $ millions, 2027 volumes",
     "layout": {"variant": "takeaway_sidebar", "sidebar": {
         "kind": "bullets", "header": "Freight, not rent, decides the case",
         "bullets": [
             "**Freight:** each Eastern order costs $13 from Central, compared with $8 from East",
             "**Damage:** transshipped goods add handling losses",
             "**Not counted:** the $0.75M exit fee and any service surcharge"],
         "rows": [
             {"label": "Share of the fixed-cost saving absorbed by freight and damage", "basis": "($1.0M + $0.20M) ÷ $1.30M",
              "point": p("eaten"), "highlight": True},
             {"label": "Years for the 2027 saving to repay the exit fee", "basis": "$0.75M ÷ $0.10M a year", "point": p("payback")}]}},
     "body": {"kind": "chart", "chart_type": "waterfall",
              "categories": ["East fixed cost removed", "Higher freight from Central", "Extra damage and handling", "Net annual saving"],
              "series": [{"name": "Saving", "points": [p("fE"), p("trStep"), p("dmgStep"), p("sav27")]}],
              "sort": "none", "highlight": ["Net annual saving"], "value_format": "\"$\"0.00\"M\""},
     "footnotes": ["The CFO's figure equals East's $1.30M fixed facility cost; Central's fixed cost does not change if East closes",
                   "Transport costs include parcel labels and carrier line haul; the CFO's cost-per-shipment dashboard counts only the carrier invoice"]},
    # ---------------------------------------------------------------- S2 equation
    {"id": "2", "role": "content", "section_id": "1", "status": "filled",
     "lead_message": {"text": "Closing in 2027 would lose $650K before the East lease would have expired anyway in 2029",
                      "numbers": [{"text": "$650K", "data_ref": "net2y"}], "clauses": 1},
     "message_type": "component", "archetype": "calculation-bridge",
     "rationale": "Our own two-year estimate; it needs its formula shown -> calculation-bridge (B-08)",
     "unit_line": "**Net result of closing East in January 2027 compared with keeping it**, $ thousands, 2027–28",
     "body": {"kind": "equation",
              "terms": [
                  {"point": p("sav27k"), "caption": "net saving in 2027 at 200,000 Eastern shipments (p. 4)"},
                  {"op": "+", "point": p("sav28"), "caption": "net saving in 2028: 10% Eastern growth to 220,000 shipments adds $5 of freight to each"},
                  {"op": "−", "point": p("exitk"), "caption": "one-time fee to end the East lease in 2027 (briefing pack)"},
                  {"op": "=", "point": p("net2y"), "caption": "net loss from closing, before any surcharge or Central retrofit"}],
              "assumptions_header": "Each open assumption makes closure look better than it would be",
              "assumptions": [
                  "Eastern demand grows 10% in 2028 per the commercial forecast; at lower growth the 2028 saving stays near the 2027 level, still far short of the fee",
                  "Extra damage stays at $0.20M a year; if it grows with volume, 2028 turns negative",
                  "Closure starts January 1, 2027; the June close in the cost consultant's draft would halve the 2027 saving",
                  "No carrier surcharge and no Central retrofit are counted, though closure needs both (section 2)"]},
     "footnotes": ["After 2027 the lease cannot be ended early; it expires in 2029, when Northline Home can leave East without a fee"]},
    nav("d2", "2"),
    # ---------------------------------------------------------------- S3 SLA bar
    {"id": "3", "role": "content", "section_id": "2", "status": "filled",
     "lead_message": {"text": "Beyond cost, only closure breaks the 92% two-day contract: the network would fall to 90.3% of orders",
                      "numbers": [{"text": "92%", "data_ref": "slaT"}, {"text": "90.3%", "data_ref": "netClose"}],
                      "highlights": ["Close East, ship from Central"], "clauses": 1},
     "message_type": "item", "archetype": "bar-ranking",
     "rationale": "Options ranked against a contract threshold -> bar-ranking with the threshold as benchmark",
     "unit_line": "**Orders delivered within two calendar days, whole network**, % of all orders (all ZIP codes), 2027",
     "layout": {"variant": "takeaway_sidebar", "sidebar": {
         "kind": "big_number", "header": "East carries 40% of orders, so its rate sets the network's",
         "big_number": p("reqE"),
         "caption": "Eastern two-day rate needed to keep the whole network at 92%",
         "bullets": [
             "**Close:** Eastern orders fall from 96% to 84% on time, a deliberate service cut the board has ruled out",
             "**Cross-dock:** clears the bar on a pilot rate of 93%, but holiday weeks were not tested",
             "**Keep East:** the 96% all-ZIP rate counts, not Finance's 98% headline that excludes rural deliveries"]}},
     "body": {"kind": "chart", "chart_type": "bar",
              "categories": ["Keep East", "Outsource to cross-dock", "Close East, ship from Central"],
              "series": [{"name": "Network two-day rate", "points": [p("netK"), p("netX"), p("netClose")]}],
              "sort": "none", "highlight": ["Close East, ship from Central"], "value_format": "0.0%",
              "benchmark": {"label": "Contract minimum", "point": p("slaT")}},
     "footnotes": ["Network rate weights each region's two-day rate by its 2027 shipments: East 200,000, Central 160,000 at 94%, West 140,000 at 95%",
                   "Central's 94% is measured at today's load; at full permitted load it would likely be lower, so 90.3% is a best case for closure"]},
    # ---------------------------------------------------------------- S4 capacity column
    {"id": "4", "role": "content", "section_id": "2", "status": "filled",
     "lead_message": {"text": "Central cannot absorb Eastern orders, which would fill its permit in 2027 and exceed it by about 8% in 2028",
                      "numbers": [{"text": "8%", "data_ref": "over28"}], "highlights": ["Close East"], "clauses": 1},
     "message_type": "item", "archetype": "column-time-series",
     "rationale": "Load against a fixed capacity line, two years, two designs -> clustered columns with a benchmark",
     "unit_line": "**Shipments handled at the Central DC**, per year, 2027 and 2028 at forecast growth",
     "layout": {"variant": "takeaway_sidebar", "sidebar": {
         "kind": "bullets", "header": "Capacity binds whatever the growth case",
         "rows": [{"label": "Central's 2028 load above its certified capacity if East closes", "basis": "389,600 ÷ 360,000 − 1",
                   "point": p("over28"), "highlight": True}],
         "bullets": [
             "**2027:** a full load leaves no headroom for the spring promotion or a demand spike",
             "**2028:** the overrun needs a $1.1M retrofit and a two-quarter permit the 2027 budget does not include",
             "**Lower growth:** the uncontracted promotion may not come, but any growth at all breaks the permit"]}},
     "body": {"kind": "chart", "chart_type": "column", "categories": ["2027", "2028"],
              "series": [{"name": "Keep East", "points": [p("vC"), p("loadK28")]},
                         {"name": "Close East", "points": [p("loadC27"), p("loadC28")]}],
              "sort": "none", "highlight": ["Close East"], "value_format": "#,##0",
              "benchmark": {"label": "Certified capacity", "point": p("capC")}},
     "basis": {"header": "How we projected 2028", "terms": [
         {"point": p("loadK28"), "caption": "Central's own orders: 160,000 grown 6% (commercial forecast)"},
         {"op": "+", "point": p("vE28"), "caption": "Eastern orders: 200,000 grown 10% (commercial forecast)"},
         {"op": "=", "point": p("loadC28"), "caption": "Central's 2028 load if East closes"}]},
     "footnotes": ["Forecast growth includes a marketplace promotion not yet contracted; capacity is 360,000 shipments a year under current staffing and fire-code permit"]},
    # ---------------------------------------------------------------- S5 KPI
    {"id": "5", "role": "content", "section_id": "2", "status": "filled",
     "lead_message": {"text": "Closure's gaps cannot be repaired within the saving or the budget, and the move would take nine months to undo",
                      "numbers": [{"text": "nine months", "data_ref": "reopen"}], "clauses": 1},
     "message_type": "item", "archetype": "kpi-big-numbers",
     "rationale": "Three numbers that each close off a repair route -> KPI tiles",
     "unit_line": "**What it would take to make closure work**, 2027",
     "body": {"kind": "kpi", "items": [
         {"point": p("surBE"), "caption": "cents per Eastern shipment: the carrier surcharge that erases the whole saving",
          "relation": "Service fix: the only lever is a surcharge outside the $13 price",
          "drivers": ["The $0.1M saving spread over 200,000 Eastern orders", "Lifting 84% toward the 88.3% the network needs requires faster carrier service",
                      "No carrier quote for that surcharge exists yet"]},
         {"point": p("oneCx"), "caption": "the $0.9M one-time budget: what exiting East and expanding Central would cost",
          "relation": "Capacity fix: $1.85M against the board's 2027 authorization",
          "drivers": ["$0.75M lease exit fee plus the $1.1M Central retrofit", "The retrofit also needs a two-quarter permit before it adds capacity",
                      "Neither is in the 2027 budget"]},
         {"point": p("reopen"), "caption": "months to bring back an East-style fulfillment center if closure fails",
          "relation": "Reversal: slow and costly once the lease is gone",
          "drivers": ["Customers would have to be migrated back at high cost", "Penalty clauses run on the contract KPI throughout",
                      "Keeping East preserves the option at no extra cost"]}]},
     "so_what": "Closure saves too little to fund its own repairs, and a wrong call would take most of a year to undo",
     "so_what_style": "bar"},
    nav("d3", "3"),
    # ---------------------------------------------------------------- S6 cost bar
    {"id": "6", "role": "content", "section_id": "3", "status": "filled",
     "lead_message": {"text": "Keeping and optimizing East is also the cheapest way to serve Eastern orders, at $2.6M a year all-in",
                      "numbers": [{"text": "$2.6M", "data_ref": "costK"}], "highlights": ["Option K: keep and optimize East"], "clauses": 1},
     "message_type": "item", "archetype": "bar-ranking",
     "rationale": "Four designs ranked on one all-in cost -> bar-ranking, cheapest first",
     "unit_line": "**Annual cost of serving Eastern orders**, transport + facility + damage, $ millions, 2027 volumes",
     "layout": {"variant": "takeaway_sidebar", "sidebar": {
         "kind": "bullets", "header": "Option K wins without moving a single order",
         "bullets": [
             "**Option K:** renegotiated East shifts and a transfer buffer for low-volume SKUs, for $0.15M of systems changes",
             "**Closure:** cheaper than today only before the surcharge, growth and the $0.75M exit fee",
             "**Cross-dock:** the $0.85M minimum commitment on top of $11 freight costs more than running East"],
         "rows": [
             {"label": "All-in cost per Eastern shipment, Option K", "basis": "$2.60M ÷ 200,000 shipments", "point": p("perK"), "highlight": True},
             {"label": "All-in cost per Eastern shipment, East as today", "basis": "$2.90M ÷ 200,000 shipments", "point": p("perKeep")}]}},
     "body": {"kind": "chart", "chart_type": "bar",
              "categories": ["Option K: keep and optimize East", "Close East, ship from Central", "Keep East as today", "Outsource to cross-dock"],
              "series": [{"name": "Annual cost", "points": [p("costK"), p("costC"), p("costKeep"), p("costX")]}],
              "sort": "none", "highlight": ["Option K: keep and optimize East"], "value_format": "\"$\"0.00\"M\""},
     "footnotes": ["Option K's $0.30M saving is a facility audit estimate; Central's fixed cost is the same in every design and is left out",
                   "Cross-dock cost treats the $0.85M minimum annual commitment as a fee on top of freight, as the briefing pack lists it with fixed facility costs"]},
    # ---------------------------------------------------------------- S7 harvey
    {"id": "7", "role": "content", "section_id": "3", "status": "filled",
     "lead_message": {"text": "Option K is the only design that meets every board commitment at the lowest annual cost",
                      "highlights": ["Option K: keep and optimize"], "clauses": 1},
     "message_type": "item", "archetype": "harvey-ball-table",
     "rationale": "Options compared on the same criteria, qualitative plus cost -> harvey-ball table",
     "unit_line": "**Designs for Eastern orders against the board's tests**, annual cost in $ millions, 2027",
     "layout": {"variant": "full"},
     "body": {"kind": "table", "table_type": "harvey",
              "columns": ["Annual cost", "92% two-day", "Central capacity", "One-time budget", "Reversible", "Verdict"],
              "rows": [
                  {"label": "Option K: keep and optimize", "highlight": True,
                   "cells": [{"point": p("costK")}, {"rating": 4}, {"rating": 4}, {"rating": 4}, {"rating": 4},
                             {"text": "Recommend: cheapest, and pays back its $0.15M within the first year"}]},
                  {"label": "Keep East as today",
                   "cells": [{"point": p("costKeep")}, {"rating": 4}, {"rating": 4}, {"rating": 4}, {"rating": 4},
                             {"text": "Safe, but leaves the $0.30M audit saving unclaimed"}]},
                  {"label": "Outsource to cross-dock",
                   "cells": [{"point": p("costX")}, {"rating": 2}, {"rating": 4}, {"rating": 3}, {"rating": 1},
                             {"text": "Test for 2029: service proven only outside holiday weeks"}]},
                  {"label": "Close East, ship from Central",
                   "cells": [{"point": p("costC")}, {"rating": 0}, {"rating": 0}, {"rating": 1}, {"rating": 0},
                             {"text": "Drop: loses to Option K at any Eastern volume above 160,000 a year"}]}],
              "legend": "Full circle = meets the test with margin; empty = fails it. Team assessment from the briefing pack"},
     "footnotes": ["Tests: network two-day rate of 92% or more; Central within its permit in 2028; 2027 one-time cost within $0.9M; ease of undoing the move"]},
    # ---------------------------------------------------------------- S8 text columns
    {"id": "8", "role": "content", "section_id": "3", "status": "filled",
     "lead_message": {"text": "The cross-dock deserves a holiday-peak test, not a 2027 contract, because its price, service and terms are unproven",
                      "clauses": 1},
     "message_type": "argument", "archetype": "text-columns",
     "rationale": "Three separate proofs the cross-dock still owes -> text columns",
     "body": {"kind": "text", "style": "columns", "columns": [
         {"header": "Price: freight must fall by about a fifth to match Option K",
          "detail": ["At the $11 quote, Eastern orders cost $3.05M a year with the fee",
                     "Break-even is about $8.75 per shipment against Option K",
                     "If the $0.85M is a spending floor, not a fee, the cross-dock costs $2.2M and wins"],
          "point": p("beXcut"), "point_caption": "cut in the $11 freight rate needed on the fee reading"},
         {"header": "Service: the 93% comes from a short pilot outside the peak",
          "detail": ["Six-week pilot, holiday weeks excluded",
                     "No guarantee during the national spring promotion",
                     "The network holds 92% only while Eastern stays above 88.3%"],
          "point": p("pilot"), "point_caption": "Eastern orders in the pilot", "emphasis": True},
         {"header": "Terms: the contract locks in cost before service is proven",
          "detail": ["The quote does not say how service is measured",
                     "Provider accepts termination for cause if all-ZIP service is defined",
                     "Two-year minimum term from signing"],
          "point": p("xLock"), "point_caption": "minimum commitment over the two-year term"}]},
     "so_what": "Clarify the fee and test the holiday peak in 2027; the 2029 lease end then allows a switch with no exit fee",
     "so_what_style": "line"},
    nav("d4", "4"),
    # ---------------------------------------------------------------- S9 timeline
    {"id": "9", "role": "content", "section_id": "4", "status": "filled",
     "lead_message": {"text": "Retaining East through 2029 keeps the choice open while the cross-dock is tested at holiday peak",
                      "clauses": 1},
     "message_type": "structure", "archetype": "timeline-roadmap",
     "rationale": "Work streams with dates and one decision gate -> timeline",
     "unit_line": "**Plan for the East DC to the 2029 lease end**, by quarter",
     "layout": {"variant": "full"},
     "body": {"kind": "timeline",
              "periods": ["Q1 2027", "Q2 2027", "Q3 2027", "Q4 2027", "Q1 2028", "Q2 2028", "H2 2028", "2029"],
              "rows": [
                  {"label": "Option K at East", "bars": [
                      {"start": "Q1 2027", "end": "Q2 2027", "label": "Shifts and SKU buffer", "emphasis": True},
                      {"start": "Q3 2027", "end": "H2 2028", "label": "Run East optimized"}]},
                  {"label": "Cross-dock test", "bars": [
                      {"start": "Q1 2027", "end": "Q3 2027", "label": "Re-quote on all-ZIP terms"},
                      {"start": "Q4 2027", "end": "Q4 2027", "label": "Holiday peak", "emphasis": True}]},
                  {"label": "Evidence for the board", "bars": [
                      {"start": "Q1 2027", "end": "Q2 2028", "label": "All-ZIP KPI, damage rate, demand actuals"}]},
                  {"label": "2029 lease", "bars": [
                      {"start": "H2 2028", "end": "2029", "label": "Renew East or switch, no exit fee"}]}],
              "milestones": [{"at": "Q1 2027", "label": "Approve Option K"},
                             {"at": "Q2 2028", "label": "Lease decision"}]},
     "so_what": "One board decision in mid-2028 settles East on tested evidence instead of today's forecasts",
     "so_what_style": "bar",
     "footnotes": ["Mid-2028 leaves more than the nine months the COO says a new East-style center would need, if the test fails after a switch"]},
    # ---------------------------------------------------------------- S10 sensitivity table
    {"id": "10", "role": "content", "section_id": "4", "status": "filled",
     "lead_message": {"text": "No open input reverses the answer for 2027; only the cross-dock fee could change the 2029 decision",
                      "clauses": 1},
     "message_type": "item", "archetype": "comparison-table",
     "rationale": "Open inputs, today's value and the value that would flip the answer -> comparison table with a verdict column",
     "unit_line": "**Inputs the board lacks, with the value at which the recommendation would change**, 2027",
     "layout": {"variant": "full"},
     "body": {"kind": "table", "table_type": "comparison",
              "columns": ["Value used", "Answer changes if", "Value at the threshold"],
              "rows": [
                  {"label": "Damage on transshipped goods",
                   "cells": [{"point": p("dmg")}, {"text": "Closure repays its fee before 2029"}, {"text": "2.5 years payback at zero damage"}],
                   "note": "Holds: even at zero damage, payback runs past 2029"},
                  {"label": "Carrier surcharge for closure",
                   "cells": [{"text": "Not priced"}, {"text": "Closure still saves money after it"}, {"text": "Above 50 cents per shipment"}],
                   "note": "Holds: any surcharge above 50 cents erases the saving"},
                  {"label": "Eastern two-day rate if closed",
                   "cells": [{"point": p("rClose")}, {"text": "Network still reaches 92%"}, {"point": p("reqE")}],
                   "note": "Holds: modeled rate is well short"},
                  {"label": "Option K audit saving",
                   "cells": [{"point": p("kSav")}, {"text": "Option K costs more than closure"}, {"text": "Below $0.1M a year"}],
                   "note": "Holds: even with no saving, East beats closure over 2027–28"},
                  {"label": "Cross-dock $0.85M fee",
                   "cells": [{"text": "Fee on top of freight"}, {"text": "It is a spending floor instead"}, {"text": "Cross-dock at $2.2M a year beats Option K"}],
                   "note": "Could flip in 2029, once peak service is proven"}],
              "verdict_header": "Effect on the recommendation"},
     "callout": {"target": "Cross-dock $0.85M fee", "header": "Settle before 2029",
                 "detail": "Ask the provider in writing whether the fee is a floor; that one answer decides the 2029 lease"},
     "footnotes": ["Closure payback at zero damage: $0.75M exit fee ÷ $0.30M a year. Floor reading: 200,000 shipments × $11, above the $0.85M floor"]},
    {"id": "app", "role": "appendix_divider", "status": "filled"},
    # ---------------------------------------------------------------- B1 claims
    {"id": "b1", "role": "backup", "section_id": "1", "backup_of": "1", "status": "filled",
     "lead_message": {"prefix": "BACKUP:", "text": "Five figures circulated before the board overstate their case and need correcting before use",
                      "count_word": 5, "clauses": 1},
     "message_type": "item", "archetype": "data-table",
     "rationale": "Claims against corrected figures -> comparison table",
     "unit_line": "**Figures circulated before the board**, as stated and as corrected",
     "layout": {"variant": "full"},
     "body": {"kind": "table", "table_type": "comparison",
              "columns": ["As stated", "What it leaves out", "Corrected"],
              "rows": [
                  {"label": "CFO: annual saving from closure",
                   "cells": [{"point": p("cfo")}, {"text": "Higher Central freight, extra damage, the exit fee"}, {"point": p("sav27")}]},
                  {"label": "Finance: East two-day rate",
                   "cells": [{"point": p("fin98")}, {"text": "Rural ZIP codes, which the contract KPI includes"}, {"point": p("rK")}]},
                  {"label": "CFO dashboard: cost per East shipment",
                   "cells": [{"point": p("tE")}, {"text": "Warehouse rent, returns and replacements"}, {"point": p("allIn")}]},
                  {"label": "Consultant: absorb East at Central",
                   "cells": [{"text": "June 2027, no staffing change"}, {"text": "Central's permit; Operations says it fills"}, {"point": p("loadC27")}]},
                  {"label": "Marketing: renewal gap from East service",
                   "cells": [{"point": p("mkt8")}, {"text": "East's mix of high-volume accounts with dedicated sales teams"}, {"text": "Not established: no controlled analysis"}]}]},
     "footnotes": ["Corrected all-in cost per shipment adds East's $1.30M fixed facility cost to transport; returns and replacements are not quantified in the pack",
                   "The deck does not rely on the renewal claim; retention elasticity to two-day service is one of the inputs the board lacks"]},
    {"id": "end", "role": "end_page", "status": "filled"},
]

spec = {
    "spec_version": "0.1",
    "mode": "deck_detailed",
    "meta": {"title": "East regional distribution center: close in 2027 or retain and optimize?",
             "subtitle": "Discussion document for the CEO and board",
             "company_name": "Northline Home", "audience": "CEO and board",
             "purpose": "Decide whether to close the East DC in 2027 or retain and optimize it",
             "date": "2026-11-20", "language": "en-US",
             "confidentiality": "Board confidential. Built on synthetic benchmark data", "theme": "navy"},
    "inputs": [{"id": "in-1", "kind": "file", "label": "Northline Home briefing pack (evidence/briefing-pack.md)", "content": PACK}],
    "storyline": storyline,
    "decision_audit": decision_audit,
    "sections": sections,
    "slides": slides,
    "data_points": DP,
    "sources": [
        {"id": "s1", "kind": "user_provided", "name": "Northline Home briefing pack", "publisher": "Northline Home", "input_id": "in-1"},
        {"id": "s0", "kind": "derived", "name": "Team analysis of the briefing pack"}],
}

out = ROOT / "work" / "northline-east-dc.json"
out.write_text(json.dumps(spec, ensure_ascii=False, indent=2))
print("wrote", out, len(slides), "slides", len(DP), "data points")
