"""Build the storyline spec for the Northline Home East DC deck (compile, restyle).

Every number comes from evidence/briefing-pack.md (s1), from a stated analysis choice in
evidence/analysis.md (s2), or is recomputed from those inputs (s3, derived, with calc).
"""
import json
import re
import sys

DP = {}       # id -> data point
ORDER = []


def _add(d):
    assert d["id"] not in DP, d["id"]
    DP[d["id"]] = d
    ORDER.append(d["id"])
    return d["id"]


T1 = "Section 3, table 'Current volumes, costs and routing' (2027 annual shipments)"
T2 = "Section 4, table 'Demand, capacity and service testing'"


def P(i, sl, label, value, unit, excerpt, locator, period=None, **kw):
    d = {"id": i, "slide_id": sl, "label": label, "value": value, "unit": unit, "source_id": "s1",
         "excerpt": excerpt, "locator": locator}
    if period:
        d["period"] = period
    d.update(kw)
    return _add(d)


def A(i, sl, label, value, unit, excerpt, locator, **kw):
    d = {"id": i, "slide_id": sl, "label": label, "value": value, "unit": unit, "source_id": "s2",
         "excerpt": excerpt, "locator": locator}
    d.update(kw)
    return _add(d)


def ev(calc):
    e = calc
    for k in sorted(DP, key=len, reverse=True):
        e = re.sub(rf"(?<![\w.]){re.escape(k)}(?![\w-])", f"({DP[k]['value']!r})", e)
    return eval(e)  # noqa: S307 (our own formulas over our own numbers)


def D(i, sl, label, unit, calc, formula, period=None, value=None, estimate=False, assumptions=None, **kw):
    v = ev(calc)
    refs = [k for k in sorted(DP, key=len, reverse=True) if re.search(rf"(?<![\w.]){re.escape(k)}(?![\w-])", calc)]
    refs = sorted(set(refs), key=lambda k: calc.find(k))
    if value is None:
        value = round(v, 6)
    else:
        assert abs(v - value) <= max(0.011, abs(value) * 0.01), (i, v, value)
    d = {"id": i, "slide_id": sl, "label": label, "value": value, "unit": unit, "source_id": "s3",
         "derived_from": refs, "formula": formula, "calc": calc}
    if period:
        d["period"] = period
    if estimate:
        d["estimate"] = True
        d["assumptions"] = assumptions or []
    d.update(kw)
    return _add(d)


def R(i):
    assert i in DP, i
    return {"data_ref": i}


# ------------------------------------------------------------------ sourced: briefing pack
P("sla", "3", "Contracted floor: orders delivered within two days, all ZIP codes", 0.92, "%",
  "At least 92% of all customer orders must be delivered within two calendar days.", "Section 2, Board commitments")
P("cap", "3", "Central certified practical capacity", 360, "k",
  "The Central warehouse has a certified practical capacity of 360,000 shipments/year under its current staffing and fire-code permit.",
  "Section 2, Board commitments", definition="thousand shipments a year; one order per shipment")
P("retro", "6", "Central retrofit needed to expand (not in 2027 budget)", 1.1, "$M",
  "Expanding it requires a two-quarter permit application and a $1.1M retrofit that the 2027 budget does not include.",
  "Section 2, Board commitments")
P("exitfee", "3", "East lease early-termination fee, 2027 (one-time exit and transfer)", 0.75, "$M",
  "The East lease can be terminated in 2027 for a one-time $0.75M fee. If retained, it expires in 2029.",
  "Section 2, Board commitments", period="2027")
P("auth", "3", "Board authority for one-time network change cost, 2027", 0.9, "$M",
  "The board authorizes only $0.9M of one-time network change costs in 2027.", "Section 2, Board commitments", period="2027")
P("e27", "3", "Eastern orders (East → East shipments)", 200, "k", "| East → East | 200,000 | $8 | $1.30M |", T1, period="2027")
P("c27", "9", "Central-region orders", 160, "k", "| Central → Central | 160,000 | $9 | $1.80M |", T1, period="2027")
P("w27", "9", "West-region orders", 140, "k", "| West → West | 140,000 | $10 | $1.20M |", T1, period="2027")
P("re", "6", "East transport per Eastern order", 8, "$", "| East → East | 200,000 | $8 | $1.30M |", T1, period="2027")
P("rc", "7", "Central transport per order", 9, "$", "| Central → Central | 160,000 | $9 | $1.80M |", T1, period="2027")
P("rw", "7", "West transport per order", 10, "$", "| West → West | 140,000 | $10 | $1.20M |", T1, period="2027")
P("rC", "3", "Transport per Eastern order shipped from Central (Option C)", 13, "$",
  "| Central → East if East closes | 200,000 | $13 | Central fixed cost unchanged |", T1, period="2027")
P("rX", "3", "Transport per Eastern order through the cross-dock (Option X)", 11, "$",
  "| Eastern third-party cross-dock | 200,000 | $11 | $0.85M minimum annual commitment |", T1, period="2027")
P("fe", "5", "East site fixed facility cost a year", 1.3, "$M", "| East → East | 200,000 | $8 | $1.30M |", T1, period="2027")
P("fc", "7", "Central fixed facility cost a year", 1.8, "$M", "| Central → Central | 160,000 | $9 | $1.80M |", T1, period="2027")
P("fw", "7", "West fixed facility cost a year", 1.2, "$M", "| West → West | 140,000 | $10 | $1.20M |", T1, period="2027")
P("xmin", "3", "Cross-dock minimum annual commitment", 0.85, "$M",
  "| Eastern third-party cross-dock | 200,000 | $11 | $0.85M minimum annual commitment |", T1, period="2027")
P("s_keep", "4", "Eastern two-day on-time rate, keep East (all-ZIP)", 0.96, "%",
  "| 2027 Eastern two-day on-time rate | 96% | 84% modeled | 93% pilot |", T2, period="2027")
P("s_C", "4", "Eastern two-day on-time rate, close and ship from Central (modeled)", 0.84, "%",
  "| 2027 Eastern two-day on-time rate | 96% | 84% modeled | 93% pilot |", T2, period="2027")
P("s_X", "4", "Eastern two-day on-time rate, cross-dock (pilot)", 0.93, "%",
  "| 2027 Eastern two-day on-time rate | 96% | 84% modeled | 93% pilot |", T2, period="2027")
P("s_w", "9", "West two-day delivery rate, current routing", 0.95, "%",
  "West and Central deliveries are currently 95% and 94% within two days, respectively, at their current routing.", "Section 4, text")
P("s_c", "9", "Central two-day delivery rate, current routing", 0.94, "%",
  "West and Central deliveries are currently 95% and 94% within two days, respectively, at their current routing.", "Section 4, text")
P("g_e", "3", "Eastern demand growth assumption", 0.10, "%", "| 2028 Eastern growth assumption | 10% | 10% | 10% |", T2, period="2028")
P("g_c", "3", "Central-region demand growth assumption", 0.06, "%", "| 2028 Central-region growth assumption | 6% | 6% | 6% |", T2, period="2028")
P("dmg", "5", "Additional annual damage and handling, close to Central", 0.2, "$M",
  "| Additional annual damage/handling | Included in current cost | $0.20M | Included in third-party quote |", T2)
P("k_save", "3", "Option K saving a year (facility audit estimate)", 0.3, "$M",
  "a facility audit estimates savings of $0.30M/year, with $0.15M upfront in systems changes", "Section 6, Option K")
P("k_up", "3", "Option K upfront systems cost (one-time)", 0.15, "$M",
  "a facility audit estimates savings of $0.30M/year, with $0.15M upfront in systems changes", "Section 6, Option K")
P("pilot_n", "10", "Eastern orders in the cross-dock pilot", 12000, "orders",
  "The outsourced cross-dock's 93% result came from a six-week pilot covering 12,000 Eastern orders and excludes holiday weeks.",
  "Section 4, text")
P("pilot_wk", "10", "Length of the cross-dock pilot", 6, "weeks", "came from a six-week pilot", "Section 4, text")
P("cfo", "5", "CFO's claimed annual saving from closing East", 1.3, "$M",
  "The CFO's slide calls closure a \"$1.3M annual saving\" because it removes the East site's fixed cost.", "Section 5")
P("fin98", "5", "Finance headline two-day rate for East (excludes rural deliveries)", 0.98, "%",
  "Finance also circulated a headline \"East delivers 98% in two days\" based on an internal report that excluded rural deliveries",
  "Section 5")
P("mkt", "5", "Marketing's renewal gap for customers served by East", 8, "pp",
  "Eastern customers renew 8 percentage points more often when served by East", "Section 5")
P("loadC", "11", "Central hub 2027 load if East closes and ships from Central", 360, "k",
  "| Central hub 2027 load | 160,000 | 360,000 | 160,000 |", T2, period="2027")

# ------------------------------------------------------------------ analysis choices (source deck)
AN = "evidence/analysis.md"
A("testcap", "12", "Cross-dock test cost cap (analysis assumption)", 0.25, "$M",
  "*The cross-dock test cap of $0.25M is a Northline assumption, pending a provider quote.", AN + ", slide 12 footnote")
A("peak90", "10b", "Proposed gate: cross-dock two-day rate in peak weeks", 0.90, "%",
  "Service: at least 92% all-ZIP over the full test period and at least 90% in peak weeks, keeping the network at or above 93.5%",
  AN + ", slide 10, proposed gate criteria")
A("costgate", "15", "Proposed gate: cross-dock cost below K at forecast volume", 0.2, "$M",
  "At least $0.2M a year below K at forecast volume", AN + ", slide 15, gate table")
A("guard95", "15", "Proposed guardrail: East all-ZIP two-day rate", 0.95, "%",
  "Guardrail: East all-ZIP two-day rate at or above 95%, tracked weekly", AN + ", slide 15, step 1")

# ------------------------------------------------------------------ derived: costs, 2027
D("tE_SQ", "7", "Eastern-order transport, status quo and K", "$M", "e27 * re / 1000", "200k × $8", "2027")
D("tE_C", "7", "Eastern-order transport, close to Central", "$M", "e27 * rC / 1000", "200k × $13", "2027")
D("tE_X", "7", "Eastern-order transport, cross-dock", "$M", "e27 * rX / 1000", "200k × $11", "2027")
D("tC", "7", "Central transport", "$M", "c27 * rc / 1000", "160k × $9", "2027")
D("tW", "7", "West transport", "$M", "w27 * rw / 1000", "140k × $10", "2027")
D("tCW", "7", "Central and West transport", "$M", "tC + tW", "1.44 + 1.40", "2027")
D("fix_SQ", "7", "Facility fixed cost, status quo", "$M", "fe + fc + fw", "1.30 + 1.80 + 1.20", "2027")
D("fix_K", "7", "Facility fixed cost, K (after the $0.30M audit saving)", "$M", "fix_SQ - k_save", "4.30 − 0.30", "2027")
D("fe_K", "17", "East fixed facility cost under K (after the audit saving)", "$M", "fe - k_save", "1.30 − 0.30", "2027")
D("fix_C", "7", "Facility fixed cost without East (Central + West)", "$M", "fc + fw", "1.80 + 1.20", "2027")
D("fix_X", "7", "Facility fixed cost, cross-dock incl. its minimum (Reading A)", "$M", "fix_C + xmin", "3.00 + 0.85", "2027")
D("all_SQ27", "4", "All-in annual cost, status quo", "$M", "tE_SQ + tCW + fix_SQ", "transport + fixed", "2027")
D("all_K27", "4", "All-in annual cost, K", "$M", "all_SQ27 - k_save", "8.74 − 0.30", "2027")
D("all_C27", "7", "All-in annual cost, close to Central", "$M", "tE_C + tCW + fix_C + dmg", "2.60 + 2.84 + 3.00 + 0.20", "2027")
D("all_X27", "4", "All-in annual cost, cross-dock (Reading A)", "$M", "tE_X + tCW + fix_X", "2.20 + 2.84 + 3.85", "2027")
# 2028
D("e28", "6", "Eastern orders in 2028 at the pack's +10% growth", "k", "e27 * (1 + g_e)", "200k × 1.10", "2028")
D("c28", "11", "Central-region orders in 2028 at the pack's +6% growth", "k", "c27 * (1 + g_c)", "160k × 1.06", "2028")
D("d_e", "6", "Extra Eastern orders in 2028", "k", "e28 - e27", "220k − 200k", "2028")
D("tE_SQ28", "17", "Eastern-order transport, SQ and K", "$M", "e28 * re / 1000", "220k × $8", "2028")
D("tE_C28", "17", "Eastern-order transport, close to Central", "$M", "e28 * rC / 1000", "220k × $13", "2028")
D("tE_X28", "17", "Eastern-order transport, cross-dock", "$M", "e28 * rX / 1000", "220k × $11", "2028")
D("tC28", "17", "Central transport", "$M", "c28 * rc / 1000", "169.6k × $9", "2028")
D("all_SQ28", "7", "All-in annual cost, status quo", "$M", "tE_SQ28 + tC28 + tW + fix_SQ", "transport + fixed", "2028")
D("all_K28", "7", "All-in annual cost, K", "$M", "all_SQ28 - k_save", "SQ − 0.30", "2028")
D("all_C28", "7", "All-in annual cost, close to Central (damage held at $0.20M)", "$M", "tE_C28 + tC28 + tW + fix_C + dmg", "transport + fixed + damage", "2028")
D("all_X28", "7", "All-in annual cost, cross-dock (Reading A)", "$M", "tE_X28 + tC28 + tW + fix_X", "transport + fixed incl. minimum", "2028")
D("tw_SQ", "7", "Two-year total cost incl. one-time, status quo", "$M", "all_SQ27 + all_SQ28", "2027 + 2028", "2027–28")
D("tw_K", "7", "Two-year total cost incl. one-time, K", "$M", "all_K27 + all_K28 + k_up", "2027 + 2028 + 0.15 one-time", "2027–28")
D("tw_C", "7", "Two-year total cost incl. one-time, close to Central", "$M", "all_C27 + all_C28 + exitfee", "2027 + 2028 + 0.75 exit", "2027–28")
D("tw_X", "7", "Two-year total cost incl. one-time, cross-dock", "$M", "all_X27 + all_X28 + exitfee", "2027 + 2028 + 0.75 exit", "2027–28")
D("k_vs_sq2", "7", "K saving against the status quo over 2027–28, after its setup cost", "$M", "tw_SQ - tw_K", "17.73 − 17.28", "2027–28")
for opt, a27, a28 in (("SQ", "all_SQ27", "all_SQ28"), ("C", "all_C27", "all_C28"), ("X", "all_X27", "all_X28")):
    D(f"gap27_{opt}", "7", f"All-in cost above K, {opt}", "$M", f"{a27} - all_K27", f"{opt} − K", "2027")
    D(f"gap28_{opt}", "7", f"All-in cost above K, {opt}", "$M", f"{a28} - all_K28", f"{opt} − K", "2028")

# ------------------------------------------------------------------ slide 6: close-to-Central saving
D("c_trans", "6", "Higher transport if Central serves the East (negative = cost)", "$M", "e27 * (re - rC) / 1000", "200k × ($8 − $13)", "2027")
D("dmg_neg", "6", "Transshipment damage (negative = cost)", "$M", "0 - dmg", "−0.20", "2027")
D("c_net27", "4", "Net annual saving of close-to-Central against the status quo", "$M", "fe + c_trans - dmg", "1.30 − 1.00 − 0.20", "2027")
D("c_extra28", "6", "Extra transport cost of 2028 Eastern growth under C", "$M", "d_e * (rC - re) / 1000", "20k × $5", "2028")
D("c_net28", "6", "Net annual saving of close-to-Central against the status quo", "$M", "c_net27 - c_extra28", "0.10 − 0.10", "2028", value=0)
D("be_c_sq", "6", "Break-even Eastern volume, C against the status quo", "k", "(fe - dmg) / (rC - re) * 1000", "($1.30M − $0.20M) ÷ $5")
D("payback", "6", "Payback of the $0.75M exit fee at $0.10M a year", "years", "exitfee / c_net27", "0.75 ÷ 0.10")
D("c_net27_x", "5", "Close-to-Central saving in 2027 after the exit fee", "$M", "c_net27 - exitfee", "0.10 − 0.75", "2027")
D("x_fix", "4", "Fixed cost removed by the cross-dock against the status quo", "$M", "fe - xmin", "1.30 − 0.85", "2027")
D("x_trans", "4", "Extra transport through the cross-dock", "$M", "e27 * (rX - re) / 1000", "200k × $3", "2027")
D("x_net", "4", "Cross-dock saving against the status quo (negative = costs more)", "$M", "x_fix - x_trans", "0.45 − 0.60", "2027")

# ------------------------------------------------------------------ slide 8: break-evens
VOLS = [100, 120, 140, 160, 180, 200, 220, 240]
for v in VOLS:
    D(f"lc{v}", "8", f"Saving of C against K at {v}k Eastern orders", "$M", f"fe - k_save - dmg - (rC - re) * {v} / 1000",
      f"(1.30 − 0.30 − 0.20) − $5 × {v}k")
    D(f"lx{v}", "8", f"Saving of X against K at {v}k Eastern orders", "$M", f"fe - k_save - xmin - (rX - re) * {v} / 1000",
      f"(1.30 − 0.30 − 0.85) − $3 × {v}k")
D("be_c_k", "8", "Break-even Eastern volume, C against K", "k", "(fe - k_save - dmg) / (rC - re) * 1000", "($1.30M − $0.30M − $0.20M) ÷ $5")
D("be_x_k", "8", "Break-even Eastern volume, X against K", "k", "(fe - k_save - xmin) / (rX - re) * 1000", "($1.30M − $0.30M − $0.85M) ÷ $3")
D("be_x_sq", "8", "Break-even Eastern volume, X against the status quo", "k", "(fe - xmin) / (rX - re) * 1000", "($1.30M − $0.85M) ÷ $3")
D("fall_c", "8", "Fall in Eastern volume needed for C to beat K", "%", "1 - be_c_k / e27", "1 − 160 ÷ 200")
D("fall_x", "8", "Fall in Eastern volume needed for X to beat K", "%", "1 - be_x_k / e27", "1 − 50 ÷ 200")

# ------------------------------------------------------------------ slide 9: service
D("tot", "9", "Network orders", "k", "e27 + c27 + w27", "200 + 160 + 140", "2027")
D("on_c", "9", "Central orders on time", "k", "c27 * s_c", "160k × 94%", "2027")
D("on_w", "9", "West orders on time", "k", "w27 * s_w", "140k × 95%", "2027")
D("on_cw", "9", "Central and West orders on time", "k", "on_c + on_w", "150.4 + 133.0", "2027")
D("need", "9", "On-time orders needed for 92% network-wide", "k", "sla * tot", "92% × 500k", "2027")
D("thr", "9", "Minimum Eastern all-ZIP two-day rate that keeps the network at 92%", "%", "(need - on_cw) / e27", "(460.0k − 283.4k) ÷ 200k", "2027")
D("on_E_C", "9", "Eastern orders on time, close to Central", "k", "e27 * s_C", "200k × 84%", "2027")
D("net_K", "4", "Network two-day rate, retain East (K or SQ)", "%", "(e27 * s_keep + on_cw) / tot", "(192.0 + 283.4) ÷ 500", "2027")
D("net_X", "4", "Network two-day rate, cross-dock (pilot rate)", "%", "(e27 * s_X + on_cw) / tot", "(186.0 + 283.4) ÷ 500", "2027")
D("net_C", "4", "Network two-day rate, close to Central", "%", "(on_E_C + on_cw) / tot", "(168.0 + 283.4) ÷ 500", "2027")
D("m_K", "9", "Network margin over the 92% floor, retain East", "pp", "(net_K - sla) * 100", "95.1% − 92%", "2027")
D("m_X", "9", "Network margin over the 92% floor, cross-dock", "pp", "(net_X - sla) * 100", "93.9% − 92%", "2027")
D("m_C", "9", "Network margin over the 92% floor, close to Central", "pp", "(net_C - sla) * 100", "90.3% − 92%", "2027")
D("h_C", "9", "Eastern rate against the 88.3% threshold, close to Central", "pp", "(s_C - thr) * 100", "84% − 88.3%", "2027")
D("h_X", "9", "Eastern rate headroom over the 88.3% threshold, cross-dock pilot", "pp", "(s_X - thr) * 100", "93% − 88.3%", "2027")
D("h_K", "9", "Eastern rate headroom over the 88.3% threshold, retain East", "pp", "(s_keep - thr) * 100", "96% − 88.3%", "2027")
D("short_C", "9", "Orders a year that miss two days beyond the 92% floor, close to Central", "orders", "(need - on_E_C - on_cw) * 1000", "460.0k − 451.4k", "2027")

# ------------------------------------------------------------------ slide 10: pilot
D("pilot_sh", "10", "Share of annual Eastern volume in the pilot", "%", "pilot_n / (e27 * 1000)", "12,000 ÷ 200,000")
D("rural", "10b", "East's ex-rural rate less its all-ZIP rate", "pp", "(fin98 - s_keep) * 100", "98% − 96%")
D("e91", "10b", "Cross-dock Eastern rate if the pilot excluded rural ZIPs (illustrative)", "%", "s_X - rural / 100", "93% − 2 pp",
  estimate=True, assumptions=["Illustrative: assumes the pilot's 93% excluded rural ZIP codes (the quote does not state its basis)",
                              "Assumes the rural gap equals East's: 98% excluding rural deliveries against 96% on all ZIP codes"])
D("net_Xr", "10b", "Network two-day rate if the pilot excluded rural ZIPs", "%", "(e27 * e91 + on_cw) / tot", "(182.0 + 283.4) ÷ 500")
D("h_Xr", "10b", "Eastern headroom over 88.3% if the pilot excluded rural ZIPs", "pp", "(e91 - thr) * 100", "91% − 88.3%")
D("net_gate", "10b", "Network two-day rate if the cross-dock runs at exactly 92% all-ZIP", "%", "(e27 * sla + on_cw) / tot", "(184.0 + 283.4) ÷ 500", value=0.935)
D("buffer", "15", "Gate buffer above the 92% contract floor", "pp", "(net_gate - sla) * 100", "93.5% − 92%")
D("late_pp", "14b", "Late Eastern orders a year per percentage point of Eastern service", "orders", "e27 * 1000 / 100", "1% × 200,000")

# ------------------------------------------------------------------ slide 11: capacity
D("util27", "11", "Central utilization under C", "%", "loadC / cap", "360k ÷ 360k", "2027")
D("load28", "11", "Central load under C, 2028 forecast", "k", "c28 + e28", "169.6k + 220k", "2028")
D("over28", "11", "Central load above certified capacity under C", "k", "load28 - cap", "389.6k − 360k", "2028")
D("util28", "11", "Central utilization under C", "%", "load28 / cap", "389.6k ÷ 360k", "2028", value=1.08)
D("utilK28", "11", "Central utilization under K or X", "%", "c28 / cap", "169.6k ÷ 360k", "2028", value=0.47)
LG = LG_ = ["Lower-growth case set at half the pack's 2028 forecast growth (analysis choice; the pack asks for a lower case to be discussed but does not size it)"]
D("g_e_lo", "11", "Eastern growth, lower-growth case", "%", "g_e / 2", "10% ÷ 2", "2028", estimate=True, assumptions=LG)
D("g_c_lo", "11", "Central growth, lower-growth case", "%", "g_c / 2", "6% ÷ 2", "2028", estimate=True, assumptions=LG)
D("lg_c", "11", "Central-region orders, lower-growth case", "k", "c27 * (1 + g_c_lo)", "160k × 1.03", "2028", estimate=True, assumptions=LG)
D("lg_e", "11", "Eastern orders, lower-growth case", "k", "e27 * (1 + g_e_lo)", "200k × 1.05", "2028", estimate=True, assumptions=LG)
D("lg_load", "11", "Central load under C, lower-growth case", "k", "lg_c + lg_e", "164.8k + 210k", "2028", estimate=True, assumptions=LG)
D("lg_over", "11", "Central load above capacity under C, lower-growth case", "k", "lg_load - cap", "374.8k − 360k", "2028")

# ------------------------------------------------------------------ slide 12: one-time and lease
D("ot_D", "12", "One-time cost, K plus capped cross-dock test (D)", "$M", "k_up + testcap", "0.15 + 0.25")
D("ot_Cf", "12", "One-time cost, close to Central incl. Central retrofit", "$M", "exitfee + retro", "0.75 + 1.1")
D("spare", "12", "Authority left after the $0.75M exit", "$M", "auth - exitfee", "0.9 − 0.75")
D("mins", "12", "Cross-dock minimums committed over the two-year term", "$M", "2 * xmin", "2 × 0.85")

# ------------------------------------------------------------------ slide 14: Reading B and deferral
D("xb27", "14", "Cross-dock all-in cost if the minimum is credited (Reading B)", "$M", "tE_X + tCW + fix_C", "2.20 + 2.84 + 3.00", "2027")
D("xb28", "14", "Cross-dock all-in cost if the minimum is credited (Reading B)", "$M", "tE_X28 + tC28 + tW + fix_C", "2.42 + 1.53 + 1.40 + 3.00", "2028")
D("b27", "14", "Cross-dock against K, Reading B (negative = saving)", "$M", "xb27 - all_K27", "8.04 − 8.44", "2027")
D("b28", "14", "Cross-dock against K, Reading B (negative = saving)", "$M", "xb28 - all_K28", "8.35 − 8.69", "2028")
D("swing", "14", "Swing between the two readings of the cross-dock quote", "$M", "gap27_X - b27", "0.45 − (−0.40)", "2027")
D("b_gain", "14b", "Gain over K from closing in 2027 under Reading B, two years", "$M", "0 - b27 - b28 - exitfee + k_up",
  "0.40 + 0.34 − 0.75 + 0.15", "2027–28")
D("dmg28", "18", "Extra C damage in 2028 if scaled to volume", "$M", "dmg * g_e", "0.20 × 10%", "2028")

# ------------------------------------------------------------------ helpers for the slides
def txt(s):
    return {"text": s}


def row(label, *cells, **kw):
    r = {"label": label, "cells": [({"point": c} if "data_ref" in c else c) if isinstance(c, dict) else txt(c) for c in cells]}
    r.update(kw)
    return r


# ------------------------------------------------------------------ slides
S = []
S.append({"id": "c", "role": "cover", "status": "filled"})
S.append({"id": "es", "role": "exec_summary", "status": "filled", "archetype": "exec-summary", "message_type": "navigation"})

# 3 · options and tests
S.append({
    "id": "3", "role": "content", "section_id": "1", "status": "filled",
    "lead_message": {"text": "We judged four designs and a deferral path on the board's four tests plus reversibility, using all-in cost and all-ZIP service", "clauses": 1},
    "message_type": "structure", "archetype": "text-columns",
    "rationale": "Options set against the criteria they are judged on: two contrasting columns (source: two lists)",
    "layout": {"variant": "full"},
    "body": {"kind": "text", "style": "columns", "columns": [
        {"header": "Four network designs and a deferral path", "detail": [
            "**SQ, status quo:** keep all three sites as they are today; the reference case",
            "**K, retain and optimize:** renegotiate East staffing shifts and add a transfer buffer for low-volume SKUs; saves $0.30M a year for $0.15M upfront",
            "**C, close East and serve from Central:** end the East lease in 2027 ($0.75M) and ship all 200k Eastern orders from Central at $13 each",
            "**X, close East and use a cross-dock:** a two-year third-party deal at $11 per order plus a $0.85M annual minimum",
            "**D, defer (middle path):** run K now, test the cross-dock through holiday peak, and decide at the 2029 lease end"]},
        {"header": "Five tests: four set by the board, plus reversibility", "detail": [
            "**1 Economics:** lowest all-in annual cost (transport, facility fixed cost, damage) plus one-time cost, not the CFO's carrier-only cost per shipment",
            "**2 Service:** at least 92% of all orders delivered within two days, network-wide, on all ZIP codes; the contracted KPI, not the ex-rural dashboard",
            "**3 Capacity:** Central at or below its 360k certified practical capacity in 2027 and under 2028 growth (East +10%, Central +6%)",
            "**4 Funding and lease:** no more than $0.9M of one-time change cost in 2027; East early exit $0.75M; West lease fixed to 2030",
            "**5 Risk:** decision-grade evidence and reversibility; rebuilding East-type capacity takes nine months"],
         "emphasis": True}]},
    "so_what": "Closure is hard to reverse, so it must pass all five tests on today's evidence; a gap is a risk, not a pass",
    "so_what_style": "line",
    "footnotes": ["Source: Northline Home briefing pack (synthetic case data), sections 2, 3, 6."]})

# 4 · hypothesis
S.append({
    "id": "4", "role": "content", "section_id": "1", "status": "filled",
    "lead_message": {"text": "The CEO's 'keep East open in 2027' held up under testing, but it needed three refinements", "clauses": 1},
    "message_type": "argument", "archetype": "comparison-table",
    "rationale": "Five conditions, each with evidence and a verdict -> table; the refined answer reads it in the sidebar",
    "unit_line": "**Hypothesis tested (CEO's view):** keep East open in 2027, because Central lacks spare capacity for growth",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {"kind": "bullets", "header": "Refined answer", "bullets": [
        "**Retain and optimize, not just retain:** Option K beats the status quo by $0.30M a year at low risk",
        "**Capacity rules out only close-to-Central:** the cross-dock fails on cost, $0.45M a year above K in the base case, and on unproven peak service",
        "**Keep East through 2029, not permanently:** the exit fee falls away at lease end; test the cross-dock now and decide at a Q3 2028 gate"]}},
    "body": {"kind": "table", "table_type": "comparison", "verdict_header": "Verdict", "columns": ["What the evidence shows"], "rows": [
        row("a  Closing saves little once all costs count",
            "C nets $0.10M a year, not $1.3M, and $0 at 2028 volume; X costs $0.15M a year more than today", note="Holds"),
        row("b  Closing puts the 92% SLA at risk",
            "C: 90.3% network rate (fail); X: 93.9% on paper, from non-peak pilot data", note="Partly"),
        row("c  Central cannot absorb Eastern demand",
            "True for C (108% of capacity in 2028); not relevant to X, which does not use Central", note="Partly"),
        row("d  Keeping East fits the lease and budget",
            "Lease runs to 2029 with no fee; K needs $0.15M of the $0.9M authorized", note="Holds"),
        row("e  Keeping East is the cheapest way to the SLA",
            "Even unoptimized, East ($8.74M) beats X ($8.89M), the only closure that meets the SLA; K is $8.44M", note="Holds")]},
    "footnotes": ["Source: Northline Home briefing pack (synthetic case data), sections 2–7; Northline analysis."]})

# 5 · claims corrected
S.append({
    "id": "5", "role": "content", "section_id": "1", "status": "filled",
    "lead_message": {"text": "Five claims in the board pre-read overstate the case for one side or the other and should not anchor the decision", "count_word": 5, "clauses": 1},
    "message_type": "item", "archetype": "comparison-table",
    "rationale": "Claims set against what they leave out and the corrected figure -> comparison table",
    "layout": {"variant": "full"},
    "body": {"kind": "table", "table_type": "comparison", "columns": ["Source", "What it leaves out", "Evidence-based figure"], "rows": [
        row("“Closing East saves $1.3M a year”", "CFO slide",
            "Counts East's fixed cost only; leaves out higher Central-to-East transport (+$5 × 200k), $0.2M extra damage and the $0.75M exit fee",
            "$0.10M a year before the $0.75M exit fee (−$0.65M in 2027); $0 at 2028 volume", highlight=True),
        row("Cost per shipment as the cost KPI", "CFO dashboard",
            "Carrier invoice ÷ orders; excludes warehouse rent, returns and replacements, so it is a transport KPI only",
            "Use all-in cost: $8.44–8.89M a year by option"),
        row("“East delivers 98% in two days”", "Finance report",
            "Excludes rural deliveries; the contract KPI counts every ZIP code", "96% all-ZIP"),
        row("“East causes 8 percentage points higher renewal”", "Marketing",
            "Correlation only: East serves more high-volume accounts with dedicated sales teams, and this is not controlled for",
            "Not usable as causal evidence; retention response to service is unknown"),
        row("“Close in June 2027 and absorb at Central with today's staffing”", "Cost consultant",
            "Puts Central at its full 360k practical load before any demand spike; 2028 growth takes it past capacity",
            "100% of capacity in 2027; 108% in 2028")]},
    "so_what": "The corrections cut both ways: they shrink the closure saving and the service and loyalty case for East",
    "so_what_style": "bar",
    "footnotes": ["Source: Northline Home briefing pack (synthetic case data), sections 3, 5. Corrected figures: Northline analysis."]})

# 6 · waterfall
S.append({
    "id": "6", "role": "content", "section_id": "1", "status": "filled",
    "lead_message": {"text": "After routing and damage costs, the CFO's $1.3M closure saving shrinks to $0.10M a year, and to zero at 2028 volume",
                     "numbers": [{"text": "$1.3M", "data_ref": "fe"}, {"text": "$0.10M", "data_ref": "c_net27"}],
                     "highlights": ["Net saving, 2027"], "clauses": 1},
    "message_type": "component", "archetype": "waterfall-bridge",
    "rationale": "What takes the claimed saving down to the net -> waterfall",
    "unit_line": "**Option C (close East, serve from Central): annual saving compared with the status quo**, $M, 2027",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {"kind": "big_number", "header": "At 2028 volume the saving is gone",
        "big_number": R("be_c_sq"),
        "caption": "thousand Eastern orders a year at which it reaches zero, ($1.30M − $0.20M) ÷ $5: exactly the 2028 forecast",
        "bullets": [
            "**Not yet included, and all make it worse:** the $0.75M exit fee, a 7.5-year payback at $0.10M a year for a lease that ends in 2029 anyway",
            "**Also unpriced:** the carrier surcharge needed to lift Eastern service above 84%, and the $1.1M Central retrofit 2028 growth needs",
            "**Against Option K:** close-to-Central costs $0.20M a year more even before these items"]}},
    "body": {"kind": "chart", "chart_type": "waterfall",
             "categories": ["East fixed cost removed", "Higher transport (200k × $5)", "Transshipment damage", "Net saving, 2027"],
             "series": [{"name": "Saving", "points": [R("fe"), R("c_trans"), R("dmg_neg"), R("c_net27")]}],
             "sort": "none", "highlight": ["Net saving, 2027"], "value_format": "0.00"},
    "footnotes": ["Transport rates exclude facility cost, damage and the exit charge. 2028: Eastern volume +10% to 220k; the 20k extra orders cost $5 more each."]})

# 7 · all-in cost
S.append({
    "id": "7", "role": "content", "section_id": "1", "status": "filled",
    "lead_message": {"text": "Under the base reading of the cross-dock quote, optimized retention (K) is the cheapest all-in design in 2027 and 2028", "clauses": 1},
    "message_type": "item", "archetype": "multi-chart-panel",
    "rationale": "Totals by option, then the gap to K by year -> two column panels (source: build-up table and gap chart)",
    "layout": {"variant": "split_2"},
    "body": {"kind": "panels", "panels": [
        {"header": "K has the lowest all-in cost of the four designs in both years",
         "unit_line": "**All-in annual cost by option**, $M",
         "body": {"kind": "chart", "chart_type": "column",
                  "categories": ["SQ Status quo", "K Retain + optimize", "C Close to Central", "X Cross-dock"],
                  "series": [{"name": "2027", "points": [R("all_SQ27"), R("all_K27"), R("all_C27"), R("all_X27")]},
                             {"name": "2028", "points": [R("all_SQ28"), R("all_K28"), R("all_C28"), R("all_X28")]}],
                  "sort": "none", "value_format": "0.00"}},
        {"header": "Both closures cost more than K every year, and their gap widens in 2028 as each extra Eastern order costs $3–5 more",
         "unit_line": "**Annual all-in cost above Option K**, $M",
         "body": {"kind": "chart", "chart_type": "column",
                  "categories": ["SQ Status quo", "C Close to Central", "X Cross-dock"],
                  "series": [{"name": "2027", "points": [R("gap27_SQ"), R("gap27_C"), R("gap27_X")]},
                             {"name": "2028", "points": [R("gap28_SQ"), R("gap28_C"), R("gap28_X")]}],
                  "sort": "none", "value_format": "0.00"}}]},
    "so_what": "Over 2027–28, K is $0.45M cheaper than the status quo even after its $0.15M setup cost",
    "so_what_style": "bar",
    "footnotes": ["Two-year totals incl. one-time cost: SQ $17.73M, K $17.28M, C $18.38M, X $18.84M. K's $0.30M saving is set against facility cost; build-up in the appendix.",
                  "C excludes the unpriced carrier surcharge and the $1.1M retrofit. 2028: East +10%, Central +6%, West flat."]})

# 8 · break-even
S.append({
    "id": "8", "role": "content", "section_id": "1", "status": "filled",
    "lead_message": {"text": "Closure beats optimized retention only below 160k Eastern orders, against 200k in 2027 and 220k forecast for 2028",
                     "numbers": [{"text": "160k", "data_ref": "be_c_k"}], "highlights": [], "clauses": 1},
    "message_type": "correlation", "archetype": "line-trend",
    "rationale": "Saving as a function of volume, two options -> two lines crossing zero at their break-evens",
    "unit_line": "**Annual saving of each closure option compared with Option K, by Eastern volume**, $M, thousand Eastern orders a year",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {"kind": "big_number", "header": "Closure loses at every plausible volume",
        "big_number": R("be_c_k"),
        "caption": "thousand Eastern orders a year: only below this would close-to-Central beat K",
        "bullets": [
            "**Close to Central:** breaks even with K at 160k and with the status quo at 220k orders",
            "**Cross-dock:** zero at 50k against K and 150k against the status quo; at 200k it costs $0.15M a year more than today",
            "**Lower growth does not rescue closure:** volume would have to fall 20% (C) or 75% (X)"]}},
    "body": {"kind": "chart", "chart_type": "line", "categories": [f"{v}k" for v in VOLS],
             "series": [{"name": "C Close to Central", "points": [R(f"lc{v}") for v in VOLS]},
                        {"name": "X Cross-dock", "points": [R(f"lx{v}") for v in VOLS]}],
             "sort": "none", "highlight": [], "value_format": "0.00"},
    "footnotes": ["Saving against K: C = ($1.30M − $0.30M − $0.20M) − $5 × orders; X = ($1.30M − $0.30M − $0.85M) − $3 × orders. K's $0.30M is lost if East closes.",
                  "One-time costs excluded; assumes rates and fixed costs do not change with volume."]})

# 9 · SLA
S.append({
    "id": "9", "role": "content", "section_id": "2", "status": "filled",
    "lead_message": {"text": "Serving East from Central breaches the contracted 92% SLA; the cross-dock clears it on paper by 1.9 percentage points",
                     "numbers": [{"text": "1.9 percentage points", "data_ref": "m_X"}],
                     "highlights": ["X Cross-dock (East 93% pilot)", "C Close to Central (East 84%)"], "clauses": 1},
    "message_type": "item", "archetype": "bar-ranking",
    "rationale": "Margin of each option against one floor -> bars, kept in option order",
    "unit_line": "**Network-wide two-day delivery rate compared with the 92% contract floor**, percentage points, 2027",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {"kind": "big_number", "header": "The threshold that matters",
        "big_number": R("thr"),
        "caption": "minimum Eastern all-ZIP two-day rate that keeps the network at 92%",
        "bullets": [
            "**Close to Central (84%):** 4.3 percentage points short; about 8,600 orders a year fall short, triggering retailer penalty clauses",
            "**Cross-dock pilot (93%):** 4.7 percentage points of headroom, but on non-peak data with an unstated measurement basis",
            "**Retaining East (96%):** 7.7 percentage points of headroom"]}},
    "body": {"kind": "chart", "chart_type": "bar",
             "categories": ["K / SQ Retain East (East 96%)", "X Cross-dock (East 93% pilot)", "C Close to Central (East 84%)"],
             "series": [{"name": "Margin compared with the 92% floor", "points": [R("m_K"), R("m_X"), R("m_C")]}],
             "sort": "none", "highlight": ["X Cross-dock (East 93% pilot)", "C Close to Central (East 84%)"], "value_format": "0.0"},
    "basis": {"header": "How the network rate is built: close-to-Central case", "terms": [
        {"point": R("on_E_C"), "caption": "k Eastern orders on time (200k × 84%)"},
        {"op": "+", "point": R("on_cw"), "caption": "k Central and West on time (94%, 95%)"},
        {"op": "÷", "point": R("tot"), "caption": "k orders in the network"},
        {"op": "=", "point": R("net_C"), "caption": "network rate; 92% needs 460.0k"}]},
    "footnotes": ["Central and West keep their 94% and 95%. East's 96% is all-ZIP; the basis of the 84% (modeled) and the 93% (pilot) is not stated.",
                  "Finance's 98% (ex-rural) and the dashboard are not the contract KPI. C's 84% rises only with an unpriced carrier surcharge, widening its $0.20M gap to K.",
                  "Threshold = (460.0k − 283.4k) ÷ 200k: on-time orders needed for 92% of 500k, less Central and West on time, over Eastern orders."]})

# 10 · pilot (first half of source slide 10)
S.append({
    "id": "10", "role": "content", "section_id": "2", "status": "filled",
    "lead_message": {"text": "The cross-dock's 93% comes from a short, non-peak pilot with an unstated measurement basis and no promotion guarantee",
                     "numbers": [{"text": "93%", "data_ref": "s_X"}], "clauses": 1},
    "message_type": "item", "archetype": "kpi-big-numbers",
    "rationale": "Three facts about one piece of evidence -> KPI tiles (source: four tiles; the two non-numeric ones are driver lines here)",
    "unit_line": "**Cross-dock pilot behind the 93% two-day rate**, six-week pilot excluding holiday weeks",
    "body": {"kind": "kpi", "items": [
        {"point": R("pilot_sh"), "caption": "of annual Eastern volume tested",
         "drivers": ["12,000 pilot orders, against 200k Eastern orders a year",
                     "A full-year rate is a weighted average, so a short non-peak sample can overstate it"]},
        {"point": R("pilot_wk"), "caption": "weeks of pilot, with no holiday weeks",
         "drivers": ["Holiday weeks were excluded from the pilot", "Peak weeks carry the most service risk"]},
        {"point": R("s_X"), "caption": "two-day rate in the pilot, on an unstated basis",
         "drivers": ["The quote does not say whether the 93% covers all ZIP codes",
                     "The operator has not guaranteed service during the national spring promotion",
                     "The provider would accept termination for cause if the contract defines all-ZIP service"]}]},
})

# 10b · headroom and test (second half of source slide 10)
S.append({
    "id": "10b", "role": "content", "section_id": "2", "status": "filled",
    "lead_message": {"text": "The cross-dock needs a holiday-peak, all-ZIP test to show its 4.7 percentage points of headroom are real",
                     "numbers": [{"text": "4.7 percentage points", "data_ref": "h_X"}], "clauses": 1},
    "message_type": "item", "archetype": "data-table",
    "rationale": "Sensitivity grid of the pilot rate stays a grid; the test criteria read it in the sidebar",
    "unit_line": "**How much headroom the pilot really gives**, Eastern and network two-day rates, 2027",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {"kind": "bullets", "header": "What a decision-grade test must show (proposed)", "bullets": [
        "**Coverage:** holiday peak 2027 and the spring 2028 promotion, including rural ZIPs",
        "**Service:** at least 92% all-ZIP over the full test and at least 90% in peak weeks, keeping the network at or above 93.5%",
        "**Contract:** an all-ZIP SLA, a termination-for-cause clause, and clarity on whether the $0.85M minimum is extra or credited",
        "**Cost:** a measured damage and handling rate on transshipped goods"]}},
    "body": {"kind": "table", "table_type": "data", "columns": ["Eastern rate", "Network rate", "Eastern headroom over 88.3%"], "rows": [
        row("Pilot as reported", R("s_X"), R("net_X"), R("h_X")),
        row("If the pilot excluded rural ZIPs (−2 pp)", R("e91"), R("net_Xr"), R("h_Xr"), highlight=True),
        row("Break-even for the 92% contract", R("thr"), R("sla"), "0 pp")]},
    "basis": {"header": "Illustrative rural adjustment", "terms": [
        {"point": R("s_X"), "caption": "cross-dock pilot two-day rate (briefing pack)"},
        {"op": "−", "point": R("rural"), "caption": "East's ex-rural 98% against its all-ZIP 96% (briefing pack)"},
        {"op": "=", "point": R("e91"), "caption": "Eastern rate if the pilot excluded rural ZIPs"}]},
    "so_what": "Weak peak weeks could erase the remaining 3–5 percentage points of headroom after the minimum is signed",
    "so_what_style": "bar",
    "footnotes": ["The 2 pp gap is illustrative only. Test thresholds are proposed by Northline analysis, not taken from the pack."]})

# 11 · capacity
S.append({
    "id": "11", "role": "content", "section_id": "2", "status": "filled",
    "lead_message": {"text": "Close-to-Central would fill Central to 100% of capacity from day one and 108% in 2028; even lower growth does not fit",
                     "numbers": [{"text": "100%", "data_ref": "util27"}, {"text": "108%", "data_ref": "util28"}],
                     "highlights": ["C, 2027", "C, 2028 forecast"], "clauses": 1},
    "message_type": "item", "archetype": "column-time-series",
    "rationale": "Load against a fixed capacity by case -> columns with the capacity as a dashed line",
    "unit_line": "**Central hub annual shipments compared with its 360k certified practical capacity**, thousands",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {"kind": "bullets", "header": "Capacity rules out Option C",
        "bullets": [
            "**2028 forecast:** 169.6k Central plus 220k Eastern orders is 29.6k over capacity; only zero growth fits, at exactly 100%",
            "**The fix does not fit the plan:** expansion needs a two-quarter permit and a $1.1M retrofit that is not in the 2027 budget",
            "**K and X add no load:** capacity is not a reason to reject them"],
        "rows": [{"label": "Central utilization under C, 2027", "point": R("util27")},
                 {"label": "Under C, 2028 forecast", "point": R("util28"), "highlight": True},
                 {"label": "Under K or X, 2028 forecast", "point": R("utilK28")}]}},
    "body": {"kind": "chart", "chart_type": "column",
             "categories": ["C, 2027", "C, 2028 lower growth", "C, 2028 forecast", "K or X, 2028 forecast"],
             "series": [{"name": "Central load", "points": [R("loadC"), R("lg_load"), R("load28"), R("c28")]}],
             "sort": "none", "highlight": ["C, 2027", "C, 2028 forecast"], "value_format": "0.0",
             "benchmark": {"label": "Certified capacity", "point": R("cap")}},
    "basis": {"header": "Lower-growth case: half the forecast (illustrative)", "terms": [
        {"point": R("lg_c"), "caption": "thousand Central-region orders, +3%"},
        {"op": "+", "point": R("lg_e"), "caption": "thousand Eastern orders, +5%"},
        {"op": "=", "point": R("lg_load"), "caption": "thousand orders at Central under C, 14.8k over capacity"}]},
    "footnotes": ["Operations: absorbing East with today's staffing (the consultant's June 2027 plan) puts Central at full practical load before any demand spike.",
                  "The pack asks for a lower-growth case to be discussed but does not size it; half the forecast is the analysis's illustrative choice."]})

# 12 · one-time cost
S.append({
    "id": "12", "role": "content", "section_id": "2", "status": "filled",
    "lead_message": {"text": "Retention and deferral fit the $0.9M one-time authority; close-to-Central fits only if its $1.1M retrofit stays unfunded",
                     "numbers": [{"text": "$0.9M", "data_ref": "auth"}],
                     "highlights": ["K Retain + optimize", "D K + cross-dock test"], "clauses": 1},
    "message_type": "item", "archetype": "bar-ranking",
    "rationale": "One-time cost by option against one authority -> columns with the authority as a dashed line",
    "unit_line": "**One-time network change cost by option**, $M, 2027, against the board's $0.9M authority",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {"kind": "bullets", "header": "Lease position by site", "bullets": [
        "**East:** exit in 2027 costs a one-time $0.75M, otherwise the lease expires in 2029; waiting avoids the fee, so 2029 is the natural point to decide",
        "**West:** cannot change before 2030; outside this decision",
        "**Central:** fixed cost unchanged in every option; expansion needs a permit and an unbudgeted $1.1M retrofit, to be budgeted for 2028 or later",
        "**Cross-dock:** a two-year minimum at $0.85M a year locks in about $1.7M before peak service is proven"]}},
    "body": {"kind": "chart", "chart_type": "column",
             "categories": ["K Retain + optimize", "D K + cross-dock test", "X Cross-dock", "C incl. Central retrofit"],
             "series": [{"name": "One-time cost", "points": [R("k_up"), R("ot_D"), R("exitfee"), R("ot_Cf")]}],
             "sort": "none", "highlight": ["K Retain + optimize", "D K + cross-dock test"], "value_format": "0.00",
             "benchmark": {"label": "Board authority", "point": R("auth")}},
    "footnotes": ["C's $1.85M = $0.75M exit + $1.1M retrofit; without it C leaves $0.15M for customer migration, and a two-quarter permit misses a June 2027 closure.",
                  "The board rule against degrading service for a freight discount limits closing C's cost gap with cheaper, slower carriers.",
                  "The $0.25M test cap is an assumption pending a provider quote."]})

# 13 · scorecard
S.append({
    "id": "13", "role": "content", "section_id": "3", "status": "filled",
    "lead_message": {"text": "Only K and D pass all five tests: the cross-dock fails on cost and is unproven on service; close-to-Central fails four", "count_word": 5, "clauses": 1},
    "message_type": "item", "archetype": "comparison-table",
    "rationale": "Options compared on the same five tests -> comparison table, the recommended rows highlighted",
    "layout": {"variant": "full"},
    "body": {"kind": "table", "table_type": "comparison",
             "columns": ["1 Economics", "2 Service (92% all-ZIP)", "3 Central capacity", "4 Funding and lease", "5 Risk and reversibility"],
             "rows": [
                 row("SQ  Status quo", "FAIL: $0.30M a year dearer than K", "PASS: 95.1%", "PASS: 47% in 2028", "PASS: $0", "PASS: no change"),
                 row("K  Retain + optimize", "PASS: cheapest, $8.44M (2027)", "PASS: 95.1%; watch shift changes", "PASS: 47% in 2028",
                     "PASS: $0.15M of $0.9M", "PASS: fully reversible", highlight=True),
                 row("D  K + test, decide in 2028", "PASS: K's cost; ≤$0.25M buys the option", "PASS: 95.1%", "PASS: 47% in 2028",
                     "PASS: $0.40M of $0.9M", "PASS: generates the missing evidence", highlight=True),
                 row("X  Close, use cross-dock", "FAIL: +$0.45M a year against K (base case)", "UNPROVEN: 93.9% from non-peak pilot",
                     "PASS: Central unaffected", "PASS: $0.75M; $0.15M spare", "FAIL: two-year minimum; nine months to reverse"),
                 row("C  Close, serve from Central", "FAIL: +$0.20M a year against K; $0 saving against SQ by 2028", "FAIL: 90.3%",
                     "FAIL: 100% in 2027, 108% in 2028", "PARTLY: $0.75M fits; $1.1M retrofit unbudgeted", "FAIL: nine months to reverse")]},
    "so_what": "K and D pass today; D also buys a cheap cross-dock option for the 2029 lease, so D is the recommended path",
    "so_what_style": "line",
    "footnotes": ["'Unproven' counts as a fail until a peak test is complete. Source: Northline Home briefing pack (synthetic case data), sections 2–7; Northline analysis."]})

# 14 · two readings (first half of source slide 14)
S.append({
    "id": "14", "role": "content", "section_id": "3", "status": "filled",
    "lead_message": {"text": "The cross-dock's economics swing by $0.85M a year on one open question: is its minimum a fee or a credited floor",
                     "highlights": [], "clauses": 1},
    "message_type": "item", "archetype": "bar-ranking",
    "rationale": "Two readings by two years stays a grid, drawn as clustered bars (positive = costs more than K)",
    "unit_line": "**Cross-dock annual all-in cost compared with Option K**, $M (positive = costs more than K)",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {"kind": "bullets", "header": "Reading A is the base case: the pack lists the $0.85M under fixed facility cost", "bullets": [
        "**Reading A, a fee on top of $11 per order:** the cross-dock costs more than K every year and is never worth closing East for at forecast volumes",
        "**Reading B, a spend floor credited against charges:** it would save $0.40M a year against K in 2027 and $0.34M in 2028, worth it only if peak all-ZIP service is proven",
        "**Settle it before signing:** the test contract must state whether the minimum is extra or credited"]}},
    "body": {"kind": "chart", "chart_type": "bar",
             "categories": ["Reading A (base case): $0.85M on top", "Reading B (sensitivity): $0.85M credited"],
             "series": [{"name": "2027", "points": [R("gap27_X"), R("b27")]}, {"name": "2028", "points": [R("gap28_X"), R("b28")]}],
             "sort": "none", "highlight": [], "value_format": "0.00"},
    "footnotes": ["Reading B is a sensitivity, not the base case. Under it the cross-dock costs $8.04M in 2027 and $8.35M in 2028, against K's $8.44M and $8.69M.",
                  "Inputs: Northline Home briefing pack (synthetic case data), sections 3 and 6; Reading B is the analysis's sensitivity."]})

# 14b · deferral (second half of source slide 14)
S.append({
    "id": "14b", "role": "content", "section_id": "3", "status": "filled",
    "lead_message": {"text": "Waiting for the 2029 lease end costs little and answers the one contract question that could make the cross-dock pay", "clauses": 1},
    "message_type": "argument", "archetype": "data-table",
    "rationale": "What the middle path costs and buys -> value table; why waiting wins reads it in the sidebar",
    "unit_line": "**What the deferral path costs and buys**",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {"kind": "bullets", "header": "Waiting beats closing now, even under Reading B", "bullets": [
        "**Closing in 2027 gains little:** under Reading B, $0.40M + $0.34M − $0.75M exit + $0.15M of K setup avoided = $0.14M over two years",
        "**Waiting avoids the early-exit fee:** the lease ends in 2029, so the $0.75M charge falls away (transfer costs within it may remain)",
        "**The downside is lopsided:** each percentage point of Eastern service below 88.3% adds 2,000 late orders a year and pushes the network below 92%, with penalties and nine months to reverse"]}},
    "body": {"kind": "table", "table_type": "data", "columns": ["Value"], "rows": [
        row("K saving locked in now", "$0.30M a year"),
        row("Test cost (capped; assumption)", "≤$0.25M one-time"),
        row("Early-exit fee avoided by waiting to 2029", "Up to $0.75M"),
        row("Cross-dock minimums not committed before proof", "About $1.7M over two years"),
        row("Decision date", "Q3 2028 board gate", highlight=True)]},
    "so_what": "Close-to-Central is dropped, not deferred: it loses to K at any volume above 160k",
    "so_what_style": "line",
    "footnotes": ["The ≤$0.25M test cost is an assumption pending a provider quote. Source: Northline Home briefing pack (synthetic case data), sections 3, 6, 7."]})

# 15 · plan
S.append({
    "id": "15", "role": "content", "section_id": "3", "status": "filled",
    "lead_message": {"text": "Three steps: optimize East now, test the cross-dock through peak and promotion, then decide the lease at a Q3 2028 gate",
                     "count_word": 3, "clauses": 1},
    "message_type": "structure", "archetype": "process-flow",
    "rationale": "Phases with dates and an exit gate -> process flow; the decisions asked today read it in the sidebar",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {"kind": "bullets", "header": "Decisions requested from the board today", "bullets": [
        "**1:** Keep East open in 2027; do not serve the East region from Central",
        "**2:** Approve Option K ($0.15M one-time)",
        "**3:** Authorize a cross-dock test of up to $0.25M with an all-ZIP SLA and no two-year minimum (subject to provider agreement)",
        "**4:** Schedule the 2029 lease gate for Q3 2028"]}},
    "body": {"kind": "process", "steps": [
        {"header": "1 Optimize East (Option K)", "detail": [
            "Approve $0.15M for systems changes",
            "Renegotiate East shifts; set up the low-volume SKU transfer buffer",
            "Guardrail: East all-ZIP two-day rate at or above 95%, tracked weekly",
            "Confirm East can handle 220k orders in 2028"], "footer": "Q1–Q2 2027"},
        {"header": "2 Test the cross-dock", "detail": [
            "Test contract: all-ZIP SLA, termination for cause, how the minimum is treated",
            "Route a sample of Eastern orders, incl. rural ZIPs, through holiday 2027 and spring 2028",
            "Measure all-ZIP rate, peak weeks, damage and cost per order"], "footer": "Q2 2027 – Q2 2028"},
        {"header": "3 Board gate: 2029 lease", "detail": [
            "Close East at lease end only if all four hold:",
            "Service: ≥92% all-ZIP over the test, ≥90% in peak weeks",
            "Network SLA (modeled): ≥93.5%, a 1.5 pp buffer",
            "Cost: at least $0.2M a year below K at forecast volume",
            "Contract: all-ZIP SLA, termination for cause, budget fit"],
         "footer": "Q3 2028; otherwise renew East", "emphasis": True}]},
    "footnotes": ["Either way, transition before the 2029 expiry; confirm the expiry date leaves at least six months after the gate. Gate thresholds are proposals.",
                  "Source: Northline Home briefing pack (synthetic case data), sections 6, 7; Northline analysis."]})

# 16 · risks
S.append({
    "id": "16", "role": "content", "section_id": "3", "status": "filled",
    "lead_message": {"text": "The recommendation holds under the main uncertainties: each one has a monitoring trigger and a planned response", "clauses": 1},
    "message_type": "item", "archetype": "comparison-table",
    "rationale": "Risks set against their effect and trigger -> table",
    "layout": {"variant": "full"},
    "body": {"kind": "table", "table_type": "comparison", "columns": ["Effect on the recommendation", "Mitigation or trigger"], "rows": [
        row("K's $0.30M saving does not materialize (audit estimate)",
            "Still right: the status quo ($8.74M) beats X ($8.89M), and C fails the SLA and capacity tests regardless",
            "Track savings quarterly; stop shift changes if service suffers"),
        row("Shift renegotiation hurts East service", "Headroom of 7.7 pp on the Eastern rate (96% against 88.3%)",
            "Weekly all-ZIP tracking; act if East drops below 95%"),
        row("Growth falls short (marketplace promotion not contracted)",
            "Closure still loses: 2027 volume is already 200k, above every break-even except C against SQ (220k)",
            "Rerun break-evens at the gate with actual volumes"),
        row("Growth beats forecast", "East site capacity is not in the pack; 220k is assumed to fit",
            "Confirm East capacity in the Q1 2027 audit"),
        row("Customer retention response to service is unknown",
            "Not used: the 92% floor binds regardless; Marketing's 8 pp claim is confounded",
            "Controlled renewal analysis by account size and sales coverage"),
        row("Cross-dock peak service, damage rate and terms are unknown",
            "Exactly what the test resolves; no commitment before the gate", "Gate criteria on the plan page"),
        row("Central permit timing is unknown", "Matters only for close-to-Central, which is dropped", "None needed now")]},
    "footnotes": ["Source: Northline Home briefing pack (synthetic case data), sections 4, 5, 7; Northline analysis."]})

S.append({"id": "app", "role": "appendix_divider", "status": "filled"})

# 17 · cost model (backup)
S.append({
    "id": "17", "role": "backup", "backup_of": "7", "section_id": "1", "status": "filled",
    "lead_message": {"prefix": "BACKUP:", "text": "Cost model detail: every option is built from the same rates, volumes and fixed costs in the briefing pack", "clauses": 1},
    "message_type": "component", "archetype": "data-table",
    "unit_line": "**Annual cost by line item and option**, $M, 2027 and 2028",
    "layout": {"variant": "full"},
    "body": {"kind": "table", "table_type": "data",
             "columns": ["SQ 2027", "K 2027", "C 2027", "X 2027", "SQ 2028", "K 2028", "C 2028", "X 2028"],
             "rows": [
                 row("East-region transport", "1.60", "1.60", "2.60", "2.20", "1.76", "1.76", "2.86", "2.42"),
                 row("Central transport", "1.44", "1.44", "1.44", "1.44", "1.53", "1.53", "1.53", "1.53"),
                 row("West transport", "1.40", "1.40", "1.40", "1.40", "1.40", "1.40", "1.40", "1.40"),
                 row("East fixed", "1.30", "1.00", "–", "–", "1.30", "1.00", "–", "–"),
                 row("Central + West fixed", "3.00", "3.00", "3.00", "3.00", "3.00", "3.00", "3.00", "3.00"),
                 row("Cross-dock minimum", "–", "–", "–", "0.85", "–", "–", "–", "0.85"),
                 row("Extra damage", "–", "–", "0.20", "–", "–", "–", "0.20", "–"),
                 row("All-in annual cost", "8.74", "8.44", "8.64", "8.89", "8.99", "8.69", "8.99", "9.20", highlight=True),
                 row("One-time, 2027", "–", "0.15", "0.75", "0.75", "", "", "", ""),
                 row("Memo: X, Reading B", "", "", "", "8.04", "", "", "", "8.35")]},
    "footnotes": ["Basis: East-region $8 (SQ, K), $13 (C), $11 (X) per order; Central orders × $9; West 140k × $10; East fixed $1.30M, K −$0.30M; Central $1.80M + West $1.20M.",
                  "Minimum $0.85M a year (Reading A; Reading B credits it); C damage $0.20M held flat; one-time: systems $0.15M, exit $0.75M. 2028 = East 220k, Central 169.6k.",
                  "Not modeled (no figure in the pack): C's carrier surcharge, retrofit timing, returns and replacements, penalties, Central's 94% under full load. Totals may not add.",
                  "Source: Northline Home briefing pack (synthetic case data), sections 3, 4, 6."]})

# 18 · analyst choices (backup)
S.append({
    "id": "18", "role": "backup", "backup_of": "13", "section_id": "3", "status": "filled",
    "lead_message": {"prefix": "BACKUP:", "text": "Analyst choices made without client input, each stated so the board can challenge it", "clauses": 1},
    "message_type": "item", "archetype": "definition-table",
    "layout": {"variant": "full"},
    "body": {"kind": "table", "table_type": "definition", "columns": ["Choice made", "Why, and sensitivity"], "rows": [
        row("Cross-dock $0.85M minimum", "Treated as a fixed fee on top of $11 per order (Reading A)",
            "Listed under fixed facility cost. Under Reading B the cross-dock would be $0.34–0.40M a year cheaper than K, but still unproven on service: this is why we test, not close"),
        row("Where K's $0.30M lands", "Reduction of East facility and operating cost", "Placement does not affect totals"),
        row("Damage under C in 2028", "Held at $0.20M (not scaled to volume)", "Scaling would make C worse by $0.02M"),
        row("Central and West service", "Stay at 94% and 95% in every option", "Generous to C: Central at 100% load would probably slip"),
        row("Cross-dock test cost", "Capped at $0.25M; no two-year minimum", "No test quote in the pack (only a two-year minimum); needs provider agreement"),
        row("Lower-growth case", "Half the forecast (East +5%, Central +3%)", "The pack asks for one but does not size it; capacity fails at any growth above zero"),
        row("Gate timing", "Q3 2028, before the 2029 lease expiry", "Expiry month not given; allows six or more months to transition"),
        row("Deck format", "16:9 PowerPoint with native, editable charts", "Board pre-read and presentation use")]},
    "footnotes": ["These choices were made because the pack is silent or ambiguous; none changes the recommendation except where noted. Source: briefing pack, sections 2–7."]})

S.append({"id": "end", "role": "end_page", "status": "filled"})

# ------------------------------------------------------------------ storyline
storyline = {
    "governing_thought": "Retain and optimize East through its 2029 lease end and test the cross-dock: closing saves at most $0.10M a year, not $1.3M, and fails or cannot yet prove the board's tests",
    "exec_summary": [
        {"id": "1", "text": "Closing East does not pay once routing and handling are counted",
         "supports": ["3", "4", "5", "6", "7", "8"],
         "sub_points": [
             {"text": "Serving East from Central nets $0.10M a year, not the $1.3M claimed, and zero at 2028 volume, before the $0.75M exit fee", "slide_id": "6"},
             {"text": "The cross-dock costs $0.15M a year more than today: $0.60M of extra transport outweighs $0.45M of fixed cost removed", "slide_id": "8"},
             {"text": "Optimized retention (K) is cheapest in the base case: $8.44M in 2027, $0.20–0.45M a year below either closure", "slide_id": "7"}]},
        {"id": "2", "text": "Closure also breaks, or cannot yet prove, the board's binding constraints",
         "supports": ["9", "10", "10b", "11", "12"],
         "sub_points": [
             {"text": "Close to Central: 90.3% against the 92% contract; Central at 100% in 2027 and 108% in 2028; $1.85M one-time with its unbudgeted retrofit, against $0.9M", "slide_id": "9"},
             {"text": "Cross-dock: 93.9% on paper, but from a six-week, non-holiday pilot with no all-ZIP definition and no promotion guarantee", "slide_id": "10"},
             {"text": "Retain and optimize: 95.1% network rate, Central at 47% of capacity in 2028, and $0.15M one-time", "slide_id": "11"}]},
        {"id": "3", "text": "Optimize now, test the cross-dock, and decide the 2029 lease at a Q3 2028 gate",
         "supports": ["13", "14", "14b", "15", "16"],
         "sub_points": [
             {"text": "Approve Option K and a cross-dock test capped at $0.25M through holiday 2027 and spring 2028, measured on all ZIP codes", "slide_id": "15"},
             {"text": "Waiting avoids the $0.75M exit fee and settles whether the $0.85M minimum is extra or credited, a swing of $0.85M a year", "slide_id": "14"},
             {"text": "Drop close-to-Central: its $5-per-order penalty makes it no cheaper than today at 2028 volume, even if Central were expanded", "slide_id": "14b"}]}],
    "next_steps": [
        {"action": "Keep East open in 2027 and approve Option K ($0.15M one-time)", "owner": "Board", "timing": "Today"},
        {"action": "Authorize a cross-dock test of up to $0.25M with an all-ZIP SLA and no two-year minimum, subject to provider agreement", "owner": "Board", "timing": "Today"},
        {"action": "Renegotiate East shifts, set up the SKU transfer buffer, track East's all-ZIP rate weekly against 95%", "timing": "Q1–Q2 2027"},
        {"action": "Run the cross-dock test through holiday 2027 and spring 2028, including rural ZIPs", "timing": "Q2 2027 – Q2 2028"},
        {"action": "Take the 2029 lease decision against the four gate criteria", "owner": "Board", "timing": "Q3 2028"}]}

sections = [
    {"id": "1", "title": "Economics", "exec_item_id": "1", "tracker_label": "Economics"},
    {"id": "2", "title": "Constraints", "exec_item_id": "2", "tracker_label": "Constraints"},
    {"id": "3", "title": "Recommended path", "exec_item_id": "3", "tracker_label": "Recommended path"}]

# ------------------------------------------------------------------ compile block
U = [
    ("u1", "answer", "Retain and optimize East through its 2029 lease end, and use 2027–28 to test the cross-dock alternative before the lease decision", "slides 1, 2", True, ["es", "13", "15"]),
    ("u2", "recommendation", "Approve Option K: saves $0.30M a year for $0.15M one-time", "slides 2, 15", True, ["es", "3", "15"]),
    ("u3", "recommendation", "Authorize a cross-dock test of up to $0.25M (assumption) with an all-ZIP SLA and no two-year minimum, through holiday 2027 and spring 2028, subject to provider agreement", "slides 2, 15", True, ["es", "14b", "15"]),
    ("u4", "recommendation", "Keep East open in 2027; do not serve the East region from Central. Close-to-Central is dropped, not deferred", "slides 2, 14, 15", True, ["es", "14b", "15"]),
    ("u5", "recommendation", "Schedule the 2029 lease gate for Q3 2028; close East at lease end only if all four gate criteria are met, otherwise renew", "slide 15", True, ["es", "15"]),
    ("u6", "claim", "The CFO's $1.3M is East's gross fixed cost; close-to-Central nets $0.10M a year, zero at 2028 volume, before the $0.75M exit fee (7.5-year payback)", "slides 2, 5, 6", True, ["es", "4", "5", "6"]),
    ("u7", "claim", "The cross-dock costs $0.15M a year more than today: $0.60M of extra transport against $0.45M of fixed cost removed", "slides 2, 4", True, ["es", "4", "8"]),
    ("u8", "claim", "Under the base reading, K is the cheapest all-in design in 2027 ($8.44M) and 2028; $0.20–0.45M a year below either closure", "slides 2, 7", True, ["es", "7"]),
    ("u9", "claim", "K is $0.45M cheaper than the status quo over 2027–28 after its $0.15M setup; the gap to closures widens with volume", "slide 7", False, ["7"]),
    ("u10", "threshold", "Closure beats K only below 160k Eastern orders (C) or 50k (X); 2027 volume is already 200k; volume would have to fall 20% or 75%", "slide 8", True, ["8", "16"]),
    ("u11", "claim", "Network two-day rate: C 90.3% (fails 92%; about 8,600 orders short), X 93.9% on paper, K 95.1%", "slides 2, 9", True, ["es", "9", "13"]),
    ("u12", "threshold", "Minimum Eastern all-ZIP rate that keeps the network at 92% is 88.3%", "slide 9", True, ["9", "10b", "14b"]),
    ("u13", "claim", "The cross-dock's 93% is from a six-week, 12,000-order (6%) non-holiday pilot with unstated measurement basis and no promotion guarantee; needs a peak, all-ZIP test", "slides 2, 10", True, ["es", "10", "10b"]),
    ("u14", "sensitivity", "Pilot headroom 4.7 pp as reported, 2.7 pp if the pilot excluded rural ZIPs (illustrative); peak weeks could erase the rest", "slide 10", False, ["10b"]),
    ("u15", "gate", "Gate criteria: ≥92% all-ZIP over the test and ≥90% in peak weeks; network ≥93.5%; cross-dock ≥$0.2M a year below K; all-ZIP SLA, termination for cause, budget fit / treatment of the minimum", "slides 10, 15", True, ["10b", "15"]),
    ("u16", "constraint", "Under C, Central runs at 100% of capacity in 2027 and 108% in 2028; even the lower-growth case does not fit; K or X leave Central at 47%", "slides 2, 11", True, ["es", "11"]),
    ("u17", "constraint", "Expansion needs a two-quarter permit and a $1.1M retrofit not in the 2027 budget; C's one-time cost incl. retrofit is $1.85M against $0.9M", "slides 2, 11, 12", True, ["es", "11", "12"]),
    ("u18", "constraint", "One-time cost: K $0.15M, D $0.40M, X $0.75M ($0.15M spare), all within the $0.9M authority", "slides 12, 13", True, ["12", "13"]),
    ("u19", "constraint", "East exit in 2027 costs $0.75M, otherwise the lease expires in 2029; West fixed to 2030; signing the cross-dock locks in about $1.7M of minimums", "slide 12", True, ["12", "14b"]),
    ("u20", "sensitivity", "Reading B (minimum credited) makes the cross-dock $0.40M (2027) and $0.34M (2028) cheaper than K; the reading swings its economics by $0.85M a year; Reading A is the base case", "slides 2, 14, 18", True, ["es", "14", "18"]),
    ("u21", "claim", "Waiting beats closing now: under Reading B closing in 2027 gains only $0.14M over two years; the exit fee falls away at 2029; each point below 88.3% adds 2,000 late orders a year", "slide 14", True, ["14b"]),
    ("u22", "claim", "Five pre-read claims overstate one side or the other (CFO $1.3M, cost per shipment, Finance 98%, Marketing 8 percentage points, consultant's June 2027 plan) and cut both ways", "slide 5", True, ["5"]),
    ("u23", "claim", "The CEO's 'keep East open' hypothesis held but needed three refinements: optimize, capacity rules out only C, keep East through 2029 not permanently", "slide 4", True, ["4"]),
    ("u24", "alternatives", "Only K and D pass all five tests; X fails on cost and risk and is unproven on service; C fails four tests; D is the recommended path", "slide 13", True, ["13"]),
    ("u25", "risks", "The recommendation holds under seven uncertainties, each with a trigger and response (K saving, shift changes, growth short or above, retention, cross-dock unknowns, permit timing)", "slide 16", True, ["16"]),
    ("u26", "approach", "Four designs and a deferral path judged on five tests (board's four plus reversibility), all-in cost and all-ZIP service; burden of proof on closure", "slide 3", False, ["3"]),
    ("u27", "assumptions", "Analyst choices where the pack is silent (Reading A, damage held flat, Central and West service held, test cap, lower-growth case, gate timing)", "slide 18", False, ["18"]),
    ("u28", "detail", "Cost model line items for every option, 2027 and 2028, and items not modeled", "slide 17", False, ["17"]),
    ("u29", "guardrail", "Guardrail: East all-ZIP two-day rate at or above 95%, tracked weekly, during the shift renegotiation", "slides 15, 16", True, ["15", "16"]),
    ("u30", "plan", "Three steps with timing: optimize East Q1–Q2 2027; test Q2 2027 – Q2 2028; board gate Q3 2028, transition before the 2029 expiry", "slide 15", True, ["15"]),
    ("u31", "claim", "C's 84% can be lifted only with a carrier surcharge not in the $13 rate; the board will not degrade service for a freight discount", "slides 6, 9, 12", False, ["6", "9", "12"]),
]
units = [{"id": i, "type": t, "text": tx, "source_loc": loc, "critical": c, "slide_ids": sl} for i, t, tx, loc, c, sl in U]
ACK = ("User not available during the build; the recommended option was taken: keep it as the analysis's stated "
       "assumption or proposal, labelled as such on the slide and in the delivery note (not verified against the pack)")
compile_block = {
    "source": "evidence/analysis.md: finished 18-slide CEO and board decision paper, extracted to text; built from evidence/briefing-pack.md",
    "variant": "restyle",
    "units": units,
    "untraceable": [
        {"data_point_id": "testcap", "critical": True, "ack": ACK, "note": "Northline assumption pending a provider quote; the pack gives only a two-year minimum"},
        {"data_point_id": "peak90", "critical": True, "ack": ACK, "note": "Proposed gate threshold from the analysis"},
        {"data_point_id": "costgate", "critical": True, "ack": ACK, "note": "Proposed gate threshold from the analysis"},
        {"data_point_id": "guard95", "critical": True, "ack": ACK, "note": "Proposed guardrail from the analysis"}],
    "corrections": [],
    "check": {"critical_units": sum(1 for u in units if u["critical"]), "preserved": sum(1 for u in units if u["critical"]),
              "notes": ("Every number in the source was recomputed from the briefing pack and matched; no corrections. "
                        "Source slides 10 and 14 each carried three blocks that cannot be read at the theme's sizes, so each was split in two "
                        "(10 -> 10 and 10b; 14 -> 14 and 14b), keeping the order and the point. Charts redrawn natively: slide 6 as a 2027 waterfall "
                        "(the 2028 step is in the sidebar and footnote), slide 7 as two column panels (line-item build-up kept in the backup), "
                        "slide 11 as columns against a capacity line, slide 12 against an authority line, slide 14's readings as clustered bars. "
                        "The lease table on slide 12 became sidebar bullets with the same content.")}}

spec = {
    "spec_version": "0.1",
    "mode": "deck_detailed",
    "meta": {"title": "East regional distribution center: close in 2027, or retain and optimize?",
             "subtitle": "CEO and board decision paper · Board meeting pre-read, November 2026",
             "company_name": "Northline Home", "audience": "CEO and board",
             "purpose": "Decide whether to close the East regional distribution center in 2027 or retain and optimize it",
             "date": "2026-11-20", "language": "en-US",
             "confidentiality": "Based only on the board briefing pack (synthetic case data). All figures in US$, at 2027 volumes unless stated",
             "theme": "navy"},
    "inputs": [
        {"id": "in-1", "kind": "file", "label": "Northline Home board briefing pack (synthetic case data)", "content": "evidence/briefing-pack.md"},
        {"id": "in-2", "kind": "file", "label": "Finished analysis deck, extracted to text (the source of truth for this compile)", "content": "evidence/analysis.md"}],
    "storyline": storyline,
    "sections": sections,
    "slides": S,
    "data_points": [DP[i] for i in ORDER],
    "sources": [
        {"id": "s1", "kind": "user_provided", "name": "Northline Home briefing pack (synthetic case data)", "input_id": "in-1"},
        {"id": "s2", "kind": "user_provided", "name": "Northline analysis (source decision paper)", "input_id": "in-2"},
        {"id": "s3", "kind": "derived", "name": "Northline analysis, recomputed from the briefing pack"}],
    "compile": compile_block,
}

out = sys.argv[1] if len(sys.argv) > 1 else "work/northline-east-dc.json"
with open(out, "w") as f:
    json.dump(spec, f, ensure_ascii=False, indent=1)
print(f"wrote {out}: {len(S)} slides, {len(DP)} data points")
