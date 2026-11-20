"""Builds the storyline spec for the Boreal Autonomy board deck (compile, restyle).

Source of truth: evidence/analysis.md (the finished deck). Numbers are traced to evidence/briefing-pack.md
or recomputed from it; the few that are the analysis's own choices are sourced to the analysis and listed
in compile.untraceable.
"""
import json, sys

DP = []
_ids = set()


def P(id, slide, label, value, unit, src, excerpt=None, locator=None, **kw):
    assert id not in _ids, id
    _ids.add(id)
    d = {"id": id, "slide_id": slide, "label": label, "value": value, "unit": unit, "source_id": src}
    if excerpt:
        d["excerpt"] = excerpt
    if locator:
        d["locator"] = locator
    for k, v in kw.items():
        if v is not None:
            d[k] = v
    DP.append(d)
    return id


def D(id, slide, label, value, unit, calc, derived_from, formula, **kw):
    return P(id, slide, label, value, unit, "s3", calc=calc, derived_from=derived_from, formula=formula, **kw)


def r(i):
    return {"data_ref": i}


PK = "s1"  # board briefing pack
AN = "s2"  # the analysis deck itself

# ---------------------------------------------------------------- inputs from the briefing pack
P("cash", "13", "Unrestricted cash", 4.9, "$M", PK,
  "Boreal has $4.9M unrestricted cash and requires a $2.6M liquidity buffer for continued product development and customer support.",
  "§2 Non-negotiable restrictions")
P("buffer", "13", "Required liquidity buffer", 2.6, "$M", PK,
  "Boreal has $4.9M unrestricted cash and requires a $2.6M liquidity buffer for continued product development and customer support.",
  "§2 Non-negotiable restrictions")
P("assess", "6", "Security and industrial-safety assessment, one-time cost", 0.45, "$M", PK,
  "A security and industrial-safety assessment costing $0.45M must be completed before any large OEM production deployment.",
  "§2 Non-negotiable restrictions")
for y, v in (("27", 5000), ("28", 10000), ("29", 14000)):
    P("f" + y, "4", f"OEM robots shipped, partner forecast, 20{y}", v, "robots", PK,
      f'"Robots shipped, partner forecast"; column 20{y} = "{v:,}"', "§3 OEM forecast table", period="20" + y)
for y, v in (("27", "1.50"), ("28", "3.00"), ("29", "4.20")):
    P("r" + y, "4", f"Nominal royalty at $300 per robot, plan, 20{y}", float(v), "$M", PK,
      f'"Nominal royalty at $300/robot"; column 20{y} = "${v}M"', "§3 OEM forecast table", period="20" + y)
P("sup", "5", "Variable support cost per shipped robot", 80, "$", PK,
  '"Support variable cost per robot"; column 2027 = "$80"', "§3 OEM forecast table")
P("roy", "4", "Option X royalty per robot shipped", 300, "$", PK,
  "The OEM proposes three years of exclusive distribution in North America, a $2.0M payment at signing and a $300 royalty per robot shipped.",
  "§1 The proposed deal")
P("adv", "4", "Payment at signing (advance minimum guarantee)", 2.0, "$M", PK,
  "The OEM proposes three years of exclusive distribution in North America, a $2.0M payment at signing and a $300 royalty per robot shipped.",
  "§1 The proposed deal", definition="recoupable advance credited against the first $2.0M of earned royalties (§3)")
P("st", "6", "Low case: share of partner forecast volumes", 0.65, "%", PK,
  "The board wants the economics of the advance credit explained without double-counting, a comparison with the direct and nonexclusive channels, and a low-case test at 65% of projected shipments.",
  "§7 Decision requirements")
P("eng", "5", "OEM-specific engineering, quality and support effort per year", 0.9, "$M", PK,
  "Boreal also expects $0.9M per year of OEM-specific engineering, quality and support effort once deployments begin, in addition to $80 variable support cost per shipped robot.",
  "§3 OEM forecast and deal economics")
P("arr", "5", "New direct software ARR in the exclusivity area, 2028", 1.8, "$M", PK,
  "Boreal expects to generate approximately $1.8M of new direct software ARR in 2028 from customers in the exclusivity area that might instead be routed through the OEM.",
  "§4 Direct channel economics", period="2028")
P("gm", "5", "Direct gross margin on new ARR", 0.82, "%", PK,
  "Finance uses 82% direct gross margin on that ARR before incremental sales support", "§4 Direct channel economics")
P("ov30", "6", "Channel overlap, Sales low estimate", 0.30, "%", PK,
  "The CEO says the OEM channel is entirely incremental, but Sales estimates that 30–70% of OEM buyers could overlap with its direct pipeline.",
  "§4 Direct channel economics")
P("ov70", "6", "Channel overlap, Sales high estimate", 0.70, "%", PK,
  "The CEO says the OEM channel is entirely incremental, but Sales estimates that 30–70% of OEM buyers could overlap with its direct pipeline.",
  "§4 Direct channel economics")
P("integ", "11", "Integration firm nonexclusive pilot size", 1200, "robots", PK,
  "A separate industrial integration firm has offered a smaller nonexclusive pilot for 1,200 robots, with a $0.22M support budget and no minimum guarantee.",
  "§4 Direct channel economics")
P("integ_sup", "15", "Integration firm pilot support budget", 0.22, "$M", PK,
  "A separate industrial integration firm has offered a smaller nonexclusive pilot for 1,200 robots, with a $0.22M support budget and no minimum guarantee.",
  "§4 Direct channel economics")
P("uptime", "8", "Lab trial uptime (60 robots, twelve weeks)", 0.988, "%", PK,
  "A twelve-week lab trial on 60 robots had 98.8% uptime, but the OEM's required production acceptance is 99.5% uptime and documented safe-stop performance in a fully loaded warehouse.",
  "§5 Evidence from the commercial pilot")
P("bar", "8", "OEM production acceptance uptime", 0.995, "%", PK,
  "A twelve-week lab trial on 60 robots had 98.8% uptime, but the OEM's required production acceptance is 99.5% uptime and documented safe-stop performance in a fully loaded warehouse.",
  "§5 Evidence from the commercial pilot")
P("trial_n", "8", "Robots in the lab trial", 60, "robots", PK,
  "A twelve-week lab trial on 60 robots had 98.8% uptime", "§5 Evidence from the commercial pilot")
P("dash", "5", "Gross margin on the royalty in the CFO dashboard", 1.0, "%", PK,
  'The CFO\'s "partner contribution margin" dashboard reports 100% gross margin on the $300 royalty; it excludes $80 per-robot support, dedicated $0.9M annual engineering and the potential lost direct channel.',
  "§5 Evidence from the commercial pilot")
P("booked", "9", "OEM robots called 'booked devices' in the competitor deck", 14000, "robots", PK,
  'The competitor deck also calls the OEM\'s expected 14,000 future robots "booked devices" although customers have not yet issued purchase orders.',
  "§5 Evidence from the commercial pilot")
P("nroy", "7", "Option N royalty per shipped robot", 350, "$", PK,
  "Option N is a 12-month nonexclusive pilot, $350 per shipped robot and no upfront guarantee",
  "§6 Internal negotiation options")
P("nmonths", "11", "Option N pilot length", 12, "months", PK,
  "Option N is a 12-month nonexclusive pilot, $350 per shipped robot and no upfront guarantee",
  "§6 Internal negotiation options")
P("mgate", "7", "Option M volume gate proposed by the OEM, annualized", 5000, "robots", PK,
  "Option M, grants exclusivity only after certification and two consecutive quarters above 5,000 shipped robots annualized",
  "§6 Internal negotiation options")

# ---------------------------------------------------------------- inputs that are the analysis's own
P("ov0", "6", "Channel overlap, CEO view (entirely incremental), lower bound", 0.0, "%", AN,
  "Channel overlap: no customer-level data. We used Sales' 30–70% range, bounded by 0% and 100%.", "Analysis, Appendix B")
P("ov100", "6", "Channel overlap, upper bound (all displaced)", 1.0, "%", AN,
  "Channel overlap: no customer-level data. We used Sales' 30–70% range, bounded by 0% and 100%.", "Analysis, Appendix B")
P("hrs", "8", "Operating hours per robot-year assumed (24/7)", 8760, "hours", AN,
  "Downtime hours assume 24/7 operation (8,760 h/yr).", "Analysis, slide 8 source line",
  estimate=True, calc="365 * 24", assumptions=["Robots operate 24 hours a day, 365 days a year (analysis assumption)"])
P("weeks", "8", "Lab trial length", 12, "weeks", AN, "Lab uptime: 60 robots, 12 weeks", "Analysis, slide 8 (pack §5: 'twelve-week lab trial')")
P("step10", "9", "Overlap step used to size the sensitivity", 0.10, "%", AN,
  "Each 10 points of overlap is worth ~$0.15M a year of displaced direct gross margin ($1.8M × 82% × 10%).", "Analysis, slide 9")
P("gate_q", "14", "Gate 2 volume: audited robots per quarter", 2250, "robots", AN,
  "Two consecutive audited quarters of ≥ 2,250 robots (~9,000/yr), at or above breakeven at 70% overlap.", "Analysis, slide 14, Gate 2",
  definition="the analysis's proposed gate, rounded up from the 8,787-robot breakeven at 70% overlap")
P("gate_y", "7", "Gate 2 volume, annualized", 9000, "robots", AN,
  "Two consecutive audited quarters of ≥ 2,250 robots (~9,000/yr), at or above breakeven at 70% overlap.", "Analysis, slide 14, Gate 2")
P("fwd", "4", "Cash the advance brings forward into 2027", 1.5, "$M", AN,
  "What the advance buys: timing only. It brings $1.5–2.0M of cash forward into 2027", "Analysis, slide 4 sidebar", value_high=2.0)

# ---------------------------------------------------------------- volumes
D("pl_rob", "4", "OEM robots shipped 2027–29, plan", 29000, "robots", "f27 + f28 + f29", ["f27", "f28", "f29"], "5,000 + 10,000 + 14,000")
for y in ("27", "28", "29"):
    D("st" + y, "4", f"OEM robots shipped, 65% stress, 20{y}", {"27": 3250, "28": 6500, "29": 9100}[y], "robots",
      f"f{y} * st", ["f" + y, "st"], f"plan 20{y} × 65%", period="20" + y)
D("st_rob", "4", "OEM robots shipped 2027–29, 65% stress", 18850, "robots", "st27 + st28 + st29", ["st27", "st28", "st29"], "sum of stress years")

# ---------------------------------------------------------------- advance mechanics (p. 4)
D("pl_roy", "4", "Royalties earned 2027–29, plan", 8.7, "$M", "r27 + r28 + r29", ["r27", "r28", "r29"], "1.50 + 3.00 + 4.20")
for y in ("27", "28", "29"):
    D(f"st{y}r", "4", f"Royalties earned, 65% stress, 20{y}", {"27": 0.975, "28": 1.95, "29": 2.73}[y], "$M",
      f"st{y} * roy / 1000000", [f"st{y}", "roy"], f"stress robots 20{y} × $300", period="20" + y,
      definition="pack §3 shows $0.97M for 2027 and the analysis $0.98M: both round the same $0.975M" if y == "27" else None)
D("st_roy", "4", "Royalties earned 2027–29, 65% stress", 5.655, "$M", "st27r + st28r + st29r", ["st27r", "st28r", "st29r"], "sum of stress years")
D("rem28", "4", "Advance credit still to recoup in 2028, plan", 0.5, "$M", "adv - r27", ["adv", "r27"], "$2.0M − $1.5M of 2027 royalties")
D("cash28", "4", "Royalty cash received 2028, plan (net of credit)", 2.5, "$M", "r28 - rem28", ["r28", "rem28"], "3.00 − 0.50")
D("pl_rcash", "4", "Royalty cash received 2027–29, plan", 6.7, "$M", "cash28 + r29", ["cash28", "r29"], "0 + 2.50 + 4.20")
D("pl_cash", "4", "Total OEM cash 2027–29 incl. advance, plan", 8.7, "$M", "adv + cash28 + r29", ["adv", "cash28", "r29"], "2.00 + 2.50 + 4.20")
D("rem28s", "4", "Advance credit still to recoup in 2028, stress", 1.025, "$M", "adv - st27r", ["adv", "st27r"], "$2.0M − $0.975M")
D("cash28s", "4", "Royalty cash received 2028, stress", 0.925, "$M", "st28r - rem28s", ["st28r", "rem28s"], "1.95 − 1.025")
D("st_rcash", "4", "Royalty cash received 2027–29, stress", 3.655, "$M", "cash28s + st29r", ["cash28s", "st29r"], "0 + 0.925 + 2.73")
D("st_cash", "4", "Total OEM cash 2027–29 incl. advance, stress", 5.655, "$M", "adv + cash28s + st29r", ["adv", "cash28s", "st29r"], "2.00 + 0.925 + 2.73")
D("framing", "4", "Three-year OEM income implied by the 'revenue win plus recurring royalties' framing", 10.7, "$M",
  "adv + pl_roy", ["adv", "pl_roy"], "$2.0M advance counted on top of $8.7M of royalties")
D("overst", "4", "Overstatement of three-year OEM income in the framing", 0.23, "%", "adv / pl_cash", ["adv", "pl_cash"], "$2.0M ÷ $8.7M")
D("rev27x", "4", "2027 'revenue' if the advance were counted as revenue", 3.5, "$M", "r27 + adv", ["r27", "adv"], "$1.5M + $2.0M")
D("zero", "4", "Advance credit applied in 2029, plan", 0.0, "$M", "adv - r27 - rem28", ["adv", "r27", "rem28"], "fully recouped by end-2028")

# ---------------------------------------------------------------- 2028 unit economics (p. 5)
D("cu", "5", "Option X contribution per robot after support", 220, "$", "roy - sup", ["roy", "sup"], "$300 − $80")
D("cshare", "5", "Option X contribution per robot as share of royalty", 0.73, "%", "cu / roy", ["cu", "roy"], "$220 ÷ $300")
D("sup28", "5", "Variable support cost 2028, plan", 0.8, "$M", "f28 * sup / 1000000", ["f28", "sup"], "10,000 × $80")
D("contr28", "5", "OEM contribution 2028, plan", 1.3, "$M", "r28 - sup28 - eng", ["r28", "sup28", "eng"], "3.00 − 0.80 − 0.90")
D("dgm", "5", "Direct gross margin at risk on new 2028 ARR", 1.476, "$M", "arr * gm", ["arr", "gm"], "$1.8M × 82%")
D("ov50", "5", "Channel overlap, midpoint of Sales' range", 0.5, "%", "(ov30 + ov70) / 2", ["ov30", "ov70"], "midpoint of 30–70%")
D("lost50", "5", "Displaced direct gross margin at 50% overlap", 0.738, "$M", "ov50 * dgm", ["ov50", "dgm"], "50% × $1.476M")
D("lost30", "6", "Displaced direct gross margin at 30% overlap", 0.4428, "$M", "ov30 * dgm", ["ov30", "dgm"], "30% × $1.476M")
D("lost70", "6", "Displaced direct gross margin at 70% overlap", 1.0332, "$M", "ov70 * dgm", ["ov70", "dgm"], "70% × $1.476M")
D("inc50", "5", "Incremental value of 2028 royalties after full costs, plan, 50% overlap", 0.562, "$M", "contr28 - lost50", ["contr28", "lost50"], "1.30 − 0.738")
D("incsh", "5", "Incremental value as share of 2028 royalties, plan, 50% overlap", 0.19, "%", "inc50 / r28", ["inc50", "r28"], "$0.562M ÷ $3.00M")
D("inc30", "5", "Incremental value 2028, plan, 30% overlap", 0.857, "$M", "contr28 - lost30", ["contr28", "lost30"], "1.30 − 0.443")
D("inc70", "5", "Incremental value 2028, plan, 70% overlap", 0.267, "$M", "contr28 - lost70", ["contr28", "lost70"], "1.30 − 1.033")
D("sup28s", "5", "Variable support cost 2028, stress", 0.52, "$M", "st28 * sup / 1000000", ["st28", "sup"], "6,500 × $80")
D("inc50s", "5", "Incremental value 2028, 65% stress, 50% overlap", -0.208, "$M", "st28r - sup28s - eng - lost50",
  ["st28r", "sup28s", "eng", "lost50"], "1.95 − 0.52 − 0.90 − 0.74")
D("w_sup", "5", "Waterfall step: variable support 2028", -0.8, "$M", "0 - sup28", ["sup28"], "−(10,000 × $80)")
D("w_eng", "5", "Waterfall step: OEM-specific engineering 2028", -0.9, "$M", "0 - eng", ["eng"], "−$0.9M")
D("w_lost", "5", "Waterfall step: displaced direct gross margin, 50% overlap", -0.738, "$M", "0 - lost50", ["lost50"], "−$0.738M")

# ---------------------------------------------------------------- three-year value grid (p. 6, appendix A)
D("sup27", "13", "Variable support cost 2027, plan", 0.4, "$M", "f27 * sup / 1000000", ["f27", "sup"], "5,000 × $80")
D("sup29", "A", "Variable support cost 2029, plan", 1.12, "$M", "f29 * sup / 1000000", ["f29", "sup"], "14,000 × $80")
D("pl_sup", "A", "Variable support cost 2027–29, plan", 2.32, "$M", "pl_rob * sup / 1000000", ["pl_rob", "sup"], "29,000 × $80")
D("eng3", "6", "OEM engineering 2027–29 (full years)", 2.7, "$M", "eng * 3", ["eng"], "$0.9M × 3 years",
  assumptions=["Full-year engineering from 2027 on every OEM route (conservative; equal across X, N and M)"])
D("contr27", "A", "OEM contribution 2027, plan", 0.2, "$M", "r27 - sup27 - eng", ["r27", "sup27", "eng"], "1.50 − 0.40 − 0.90")
D("contr29", "A", "OEM contribution 2029, plan", 2.18, "$M", "r29 - sup29 - eng", ["r29", "sup29", "eng"], "4.20 − 1.12 − 0.90")
D("pl_contr", "A", "OEM contribution 2027–29, plan", 3.68, "$M", "pl_roy - pl_sup - eng3", ["pl_roy", "pl_sup", "eng3"], "8.70 − 2.32 − 2.70")
D("pl_v0", "6", "Option X value 2027–29 before channel effects, plan", 3.23, "$M", "pl_contr - assess", ["pl_contr", "assess"], "3.68 − 0.45")
D("sup27s", "A", "Variable support cost 2027, stress", 0.26, "$M", "st27 * sup / 1000000", ["st27", "sup"], "3,250 × $80")
D("sup29s", "A", "Variable support cost 2029, stress", 0.728, "$M", "st29 * sup / 1000000", ["st29", "sup"], "9,100 × $80")
D("st_sup", "A", "Variable support cost 2027–29, stress", 1.508, "$M", "st_rob * sup / 1000000", ["st_rob", "sup"], "18,850 × $80")
D("contr27s", "A", "OEM contribution 2027, stress", -0.185, "$M", "st27r - sup27s - eng", ["st27r", "sup27s", "eng"], "0.975 − 0.26 − 0.90")
D("contr28s", "A", "OEM contribution 2028, stress", 0.53, "$M", "st28r - sup28s - eng", ["st28r", "sup28s", "eng"], "1.95 − 0.52 − 0.90")
D("contr29s", "A", "OEM contribution 2029, stress", 1.102, "$M", "st29r - sup29s - eng", ["st29r", "sup29s", "eng"], "2.73 − 0.728 − 0.90")
D("st_contr", "A", "OEM contribution 2027–29, stress", 1.447, "$M", "st_roy - st_sup - eng3", ["st_roy", "st_sup", "eng3"], "5.655 − 1.508 − 2.70")
D("st_v0", "6", "Option X value 2027–29 before channel effects, stress", 0.997, "$M", "st_contr - assess", ["st_contr", "assess"], "1.447 − 0.45")
LOST = {"30": "lost30", "50": "lost50", "70": "lost70", "100": "dgm"}
for case, base in (("pl", "pl_v0"), ("st", "st_v0")):
    vals = {"pl": {"30": 2.787, "50": 2.492, "70": 2.197, "100": 1.754}, "st": {"30": 0.554, "50": 0.259, "70": -0.036, "100": -0.479}}[case]
    valsB = {"pl": {"30": 2.344, "50": 1.754, "70": 1.164, "100": 0.278}, "st": {"30": 0.111, "50": -0.479, "70": -1.069, "100": -1.955}}[case]
    nm = "plan" if case == "pl" else "65% stress"
    for o in ("30", "50", "70", "100"):
        D(f"{case}_v{o}", "6", f"Option X value 2027–29, {nm}, {o}% overlap (2028 cohort only)", vals[o], "$M",
          f"{base} - {LOST[o]}", [base, LOST[o]], f"value before channel effects − {o}% × $1.476M")
        D(f"{case}B{o}", "6", f"Option X value 2027–29, {nm}, {o}% overlap, if lost 2028 customers renew in 2029", valsB[o], "$M",
          f"{base} - {LOST[o]} * 2", [base, LOST[o]], f"value before channel effects − 2 × {o}% × $1.476M",
          assumptions=["Lost 2028 direct customers would also have renewed in 2029 (direct churn is not in the pack)"])
D("vol_swing", "9", "Change in Option X three-year value from plan to 65% volumes", -2.233, "$M", "st_v0 - pl_v0", ["st_v0", "pl_v0"], "0.997 − 3.23")

# ---------------------------------------------------------------- breakevens (p. 7, p. 16)
D("be0", "7", "Breakeven OEM robots a year, 0% overlap", 4090.9, "robots", "eng * 1000000 / cu", ["eng", "cu"], "$0.9M ÷ $220")
for o, v in (("30", 6103.6), ("50", 7445.5), ("70", 8787.3)):
    D("be" + o, "7", f"Breakeven OEM robots a year, {o}% overlap", v, "robots", f"(eng + lost{o}) * 1000000 / cu",
      ["eng", "lost" + o, "cu"], f"($0.9M + {o}% × $1.476M) ÷ $220")
D("be100", "7", "Breakeven OEM robots a year, 100% overlap", 10800, "robots", "(eng + dgm) * 1000000 / cu", ["eng", "dgm", "cu"], "($0.9M + $1.476M) ÷ $220")
D("be_rng", "7", "Breakeven range at Sales' 30–70% overlap, rounded", 6100, "robots", "be30", ["be30", "be70"],
  "6,104 and 8,787 rounded to the nearest hundred", value_high=8800)
D("nunit", "7", "Option N contribution per robot after support", 270, "$", "nroy - sup", ["nroy", "sup"], "$350 − $80")
D("beN", "7", "Option N breakeven robots a year (OEM programme alone)", 3333.3, "robots", "eng * 1000000 / nunit", ["eng", "nunit"], "$0.9M ÷ $270")
D("beN_r", "16", "Option N breakeven, rounded", 3300, "robots", "beN * 0.99", ["beN"], "3,333 rounded to the nearest hundred")
D("be0_r", "16", "Option X breakeven at 0% overlap, rounded", 4100, "robots", "be0", ["be0"], "4,091 rounded to the nearest hundred")
D("prem", "12", "Option N royalty premium over Option X per robot", 50, "$", "nroy - roy", ["nroy", "roy"], "$350 − $300")
D("thr70", "16", "Support cost per robot at which Option X loses value at plan volume, 70% overlap", 107, "$",
  "(r28 - eng - lost70) * 1000000 / f28", ["r28", "eng", "lost70", "f28"], "($3.0M − $0.9M − 70% × $1.476M) ÷ 10,000")
D("thr30", "16", "Support cost per robot at which Option X loses value at plan volume, 30% overlap", 166, "$",
  "(r28 - eng - lost30) * 1000000 / f28", ["r28", "eng", "lost30", "f28"], "($3.0M − $0.9M − 30% × $1.476M) ÷ 10,000")

# ---------------------------------------------------------------- uptime (p. 8)
D("lab_dt", "8", "Downtime share of hours, lab trial", 0.012, "%", "1 - uptime", ["uptime"], "1 − 98.8%")
D("bar_dt", "8", "Downtime share of hours allowed by the OEM bar", 0.005, "%", "1 - bar", ["bar"], "1 − 99.5%")
D("cut", "8", "Downtime cut still needed to reach the OEM bar", -0.58, "%", "0 - (1 - bar_dt / lab_dt)", ["bar_dt", "lab_dt"], "−(1 − 0.5% ÷ 1.2%)")
EST = ["Robots operate 24 hours a day, 365 days a year (analysis assumption)"]
D("hr_lab", "8", "Downtime hours per robot-year at lab uptime", 105, "hours", "lab_dt * hrs", ["lab_dt", "hrs"], "1.2% × 8,760 h", estimate=True, assumptions=EST)
D("hr_bar", "8", "Downtime hours per robot-year at the OEM bar", 44, "hours", "bar_dt * hrs", ["bar_dt", "hrs"], "0.5% × 8,760 h", estimate=True, assumptions=EST)
D("trial_h", "8", "Hours in the 12-week trial at 24/7 operation", 2016, "hours", "weeks * 7 * 24", ["weeks"], "12 weeks × 168 h", estimate=True, assumptions=EST)
D("tr_lab", "8", "Downtime hours per robot over the trial, lab", 24, "hours", "lab_dt * trial_h", ["lab_dt", "trial_h"], "1.2% × 2,016 h", estimate=True, assumptions=EST)
D("tr_bar", "8", "Downtime hours per robot over the trial, at the OEM bar", 10, "hours", "bar_dt * trial_h", ["bar_dt", "trial_h"], "0.5% × 2,016 h", estimate=True, assumptions=EST)

# ---------------------------------------------------------------- overlap sensitivity (p. 9)
D("ov10", "9", "Displaced direct gross margin per 10 percentage points of overlap, a year", 0.1476, "$M", "dgm * step10", ["dgm", "step10"], "$1.8M × 82% × 10%")

# ---------------------------------------------------------------- Option N value and parity (p. 11, 12)
NA = ["Option N's $350 terms and partner volumes persist for three years, which the OEM has not guaranteed (upper bound)",
      "Same $0.9M a year of engineering and $0.45M assessment as Option X"]
D("pl_N", "11", "Option N terms, value 2027–29, plan volumes", 4.68, "$M", "pl_rob * nunit / 1000000 - eng3 - assess",
  ["pl_rob", "nunit", "eng3", "assess"], "29,000 × $270 − $2.7M − $0.45M", assumptions=NA)
D("st_N", "11", "Option N terms, value 2027–29, 65% volumes", 1.94, "$M", "st_rob * nunit / 1000000 - eng3 - assess",
  ["st_rob", "nunit", "eng3", "assess"], "18,850 × $270 − $2.7M − $0.45M", assumptions=NA)
D("par30", "12", "Robots at which N matches X's three-year value, 30% overlap", 22000, "robots", "(pl_v30 + eng3 + assess) * 1000000 / nunit",
  ["pl_v30", "eng3", "assess", "nunit"], "($2.79M + $2.7M + $0.45M) ÷ $270, rounded")
D("par70", "12", "Robots at which N matches X's three-year value, 70% overlap", 19800, "robots", "(pl_v70 + eng3 + assess) * 1000000 / nunit",
  ["pl_v70", "eng3", "assess", "nunit"], "($2.20M + $2.7M + $0.45M) ÷ $270, rounded")
D("cush30", "12", "Volume cushion: fewer robots at which N still matches X, plan, 30% overlap", 0.24, "%", "1 - par30 / pl_rob",
  ["par30", "pl_rob"], "1 − 22,000 ÷ 29,000")
D("cush70", "12", "Volume cushion: fewer robots at which N still matches X, plan, 70% overlap", 0.32, "%", "1 - par70 / pl_rob",
  ["par70", "pl_rob"], "1 − 19,800 ÷ 29,000")
D("spar30", "12", "Robots at which N matches X, stress, 30% overlap", 13719, "robots", "(st_v30 + eng3 + assess) * 1000000 / nunit",
  ["st_v30", "eng3", "assess", "nunit"], "($0.554M + $2.7M + $0.45M) ÷ $270")
D("spar70", "12", "Robots at which N matches X, stress, 70% overlap", 11533, "robots", "(st_v70 + eng3 + assess) * 1000000 / nunit",
  ["st_v70", "eng3", "assess", "nunit"], "(−$0.036M + $2.7M + $0.45M) ÷ $270")
D("cush_s", "12", "Volume cushion in the stress case", 0.27, "%", "1 - spar30 / st_rob", ["spar30", "spar70", "st_rob"],
  "1 − 13,719 ÷ 18,850 and 1 − 11,533 ÷ 18,850", value_high=0.39)

# ---------------------------------------------------------------- liquidity (p. 13)
D("hd0", "13", "Headroom above the buffer today", 2.3, "$M", "cash - buffer", ["cash", "buffer"], "$4.9M − $2.6M")
D("hd_def", "13", "Headroom end-2027: defer (assessment only)", 1.85, "$M", "hd0 - assess", ["hd0", "assess"], "2.3 − 0.45")
D("nrev27", "13", "Option N royalties 2027, plan, collected in-year", 1.75, "$M", "f27 * nroy / 1000000", ["f27", "nroy"], "5,000 × $350")
D("hd_N", "13", "Headroom end-2027: N, royalties collected in-year", 2.3, "$M", "hd0 - assess - eng - sup27 + nrev27",
  ["hd0", "assess", "eng", "sup27", "nrev27"], "2.3 − 0.45 − 0.90 − 0.40 + 1.75")
D("hd_Nlag", "13", "Headroom end-2027: N, no 2027 royalty cash (reporting lag)", 0.55, "$M", "hd0 - assess - eng - sup27",
  ["hd0", "assess", "eng", "sup27"], "2.3 − 0.45 − 0.90 − 0.40")
D("hd_X", "13", "Headroom end-2027: X at plan, advance in hand", 2.55, "$M", "hd0 + adv - assess - eng - sup27",
  ["hd0", "adv", "assess", "eng", "sup27"], "2.3 + 2.0 − 0.45 − 0.90 − 0.40 (2027 royalties all credited to the advance)")
D("hd_Xslip", "13", "Headroom end-2027: X, certification slips and $2.0M offset demanded", 1.85, "$M", "hd0 + adv - adv - assess",
  ["hd0", "adv", "assess"], "2.3 + 2.0 advance − 2.0 offset − 0.45; no deployments, so no engineering or support")
D("hd_direct", "13", "Headroom end-2027: direct sales only", 2.3, "$M", "hd0", ["hd0"], "no deal cash flows")

# ---------------------------------------------------------------- slides
SL = []


def slide(id, section, title, archetype, mtype, body, **kw):
    s = {"id": id, "role": "content", "status": "filled", "section_id": section or "1"}
    lm = {"text": title}
    for k in ("numbers", "highlights", "count_word", "clauses"):
        if k in kw:
            lm[k] = kw.pop(k)
    s["lead_message"] = lm
    s["message_type"] = mtype
    s["archetype"] = archetype
    s.update({k: v for k, v in kw.items() if k in ("rationale", "unit_line")})
    if "layout" in kw:
        s["layout"] = kw["layout"]
    s["body"] = body
    for k in ("so_what", "so_what_style", "callout", "footnotes", "basis"):
        if k in kw:
            s[k] = kw[k]
    SL.append(s)
    return s


def T(*cells):
    return [{"text": c} if isinstance(c, str) else c for c in cells]


SL.append({"id": "c", "role": "cover", "status": "filled"})
SL.append({"id": "es", "role": "exec_summary", "status": "filled", "archetype": "exec-summary", "message_type": "navigation"})

# p.3 hypothesis test
slide("3", None,
      "With only one of six conditions for exclusivity at signing even partly met, the 'don't sign yet' hypothesis stands",
      "comparison-table", "argument",
      {"kind": "table", "table_type": "comparison",
       "columns": ["For exclusivity at signing to be right, it must be true that…", "What the evidence shows"],
       "rows": [
           {"label": "Value 1 · does not hold", "cells": T("The $2.0M signing payment adds value on top of royalties",
                                           "It is an advance against the first $2.0M of royalties, open to offset; three-year cash is $8.7M either way (p. 4)")},
           {"label": "Value 2 · partly holds: plan case only", "highlight": True,
            "cells": T("Exclusivity creates value even in the low case, with realistic overlap",
                       "+$2.2–2.8M at plan; −$0.04M to +$0.55M at 65% volumes, Sales' 30–70% overlap (p. 5–7)")},
           {"label": "Evidence 3 · does not hold", "cells": T("The product is production-ready in the OEM's hardware",
                                              "98.8% lab uptime against 99.5% required; no loaded or peak test; assessment not started (p. 8)")},
           {"label": "Evidence 4 · does not hold", "cells": T("OEM volumes and the growth story are reliable enough to commit on",
                                              "Shipments unaudited; 14,000 'booked devices' without purchase orders; competitor case correlational (p. 9)")},
           {"label": "Alternatives 5 · does not hold", "cells": T("Exclusivity is the only way to win the OEM's volume",
                                                  "The OEM will consider N (nonexclusive, $350 a robot) and M (gated exclusivity) (p. 11–12)")},
           {"label": "Protection 6 · does not hold", "cells": T("The contract protects Boreal if forecasts or certification miss",
                                                "No audit right, no royalty floor after the advance, no release triggers, no code escrow (p. 10)")}]},
      count_word=6, clauses=1,
      rationale="Conditions tested on the same criteria -> comparison table; the verdict sits inside the table",
      unit_line="**Test of the initial hypothesis**: what must be true for exclusivity at signing (Option X) to be right, checked against the briefing pack",
      so_what="The problem is exclusivity before evidence, not exclusivity itself: the answer is a gated path, not a flat 'no'",
      footnotes=["The hypothesis survives, refined. Stated before testing: do not grant exclusivity at signing; a nonexclusive or milestone deal keeps the OEM upside and the direct channel", "Source: board briefing pack §1–6; team analysis"])

# p.4 advance
ROWS4 = [
    ("Plan 2027", "f27", "1.50", "−1.50", "0.00", "2.00", False),
    ("Plan 2028", "f28", "3.00", "−0.50", "2.50", "2.50", False),
    ("Plan 2029", "f29", "4.20", "0.00", "4.20", "4.20", False),
    ("Plan total", "pl_rob", "8.70", "−2.00", "6.70", "8.70", True),
    ("65% stress 2027", "st27", "0.98", "−0.98", "0.00", "2.00", False),
    ("Stress 2028", "st28", "1.95", "−1.03", "0.93", "0.93", False),
    ("Stress 2029", "st29", "2.73", "0.00", "2.73", "2.73", False),
    ("Stress total", "st_rob", "5.66", "−2.00", "3.66", "5.66", True)]
slide("4", "1",
      "The $2.0M is an advance on royalties, not extra revenue: three-year OEM cash is $8.7M, not the implied $10.7M",
      "data-table", "component",
      {"kind": "table", "table_type": "data",
       "columns": ["Robots shipped", "Royalties earned at $300", "Advance credit applied", "Royalty cash received", "Total OEM cash, incl. $2.0M at signing"],
       "rows": [{"label": a, "cells": [{"point": r(b)}] + T(c, d, e, f), **({"highlight": True} if h else {})} for a, b, c, d, e, f, h in ROWS4]},
      numbers=[{"text": "$10.7M", "data_ref": "framing"}],
      rationale="Year-by-year cash mechanics of the advance -> data table, kept as the source's table",
      unit_line="**Option X cash from the OEM**, $ millions (robots in units), plan and 65% stress, 2027–29, undiscounted",
      layout={"variant": "takeaway_sidebar", "sidebar": {
          "kind": "big_number", "header": "Counting the advance as revenue double-counts it",
          "big_number": r("framing"),
          "caption": "implied by the 'revenue win plus recurring royalties' framing: 23% more than the $8.7M Boreal will receive",
          "bullets": ["**Revenue** is royalties earned as robots ship and payment is collected: $1.5M in 2027 at plan, not $3.5M",
                      "**The $2.0M** is a minimum-guarantee liability until earned; the partner can demand an offset if guaranteed performance is missed",
                      "**It buys timing only:** it brings $1.5–2.0M of cash forward into 2027, which Boreal does not need to stay above its buffer"]}},
      footnotes=["Reading the table: the advance is cash received early, then netted out of 2028 royalty cash, so total cash always equals royalties earned",
                 "In the stress case, 2028 royalty cash falls to $0.93M because $1.03M of credit is still being recouped"])

# p.5 waterfall
slide("5", "1",
      "After full costs, only about $0.56M of the $3.00M in 2028 plan royalties is incremental: 19%, not the dashboard's 100%",
      "waterfall-bridge", "component",
      {"kind": "chart", "chart_type": "waterfall", "sort": "none", "value_format": '"$"0.00"M"',
       "categories": ["2028 royalties (10,000 × $300)", "Variable support (10,000 × $80)", "OEM-specific engineering",
                      "Displaced direct gross margin", "Incremental value"],
       "series": [{"name": "2028, plan", "points": [r("r28"), r("w_sup"), r("w_eng"), r("w_lost"), r("inc50")]}],
       "highlight": ["Incremental value"]},
      numbers=[{"text": "$3.00M", "data_ref": "r28"}, {"text": "$0.56M", "data_ref": "inc50"}, {"text": "19%", "data_ref": "incsh"}],
      highlights=["Incremental value"],
      rationale="What the royalty shrinks to after each cost -> waterfall bridge",
      unit_line="**Option X, 2028 plan year**, $ millions; displaced direct margin at 50% overlap, the midpoint of Sales' 30–70%",
      layout={"variant": "takeaway_sidebar", "sidebar": {
          "kind": "big_number", "header": "Three views of the same royalty",
          "big_number": r("incsh"),
          "caption": "of the royalty is incremental at plan in the complete view, against 100% in the CFO dashboard, which counts only the $300 royalty",
          "bullets": ["**Per robot:** $220 (73%) after $80 of support, before any fixed cost; $1.30M of OEM contribution before channel effects",
                      "**Across Sales' overlap range:** $0.27–0.86M for 30–70%",
                      "**At 65% volumes:** negative, $1.95M − $0.52M − $0.90M − $0.74M = −$0.21M in 2028"]}},
      footnotes=["Exclusivity bars all new direct North American licences, including customers on other OEMs' robots: that forgone margin is a cost of Option X, not of the OEM channel in general",
                 "Lost direct margin = 50% (midpoint of Sales' 30–70% overlap) × $1.8M ARR × 82% gross margin"])

# p.6 three-year value: two panels (base and renewal sensitivity)
OVC = ["0% (CEO view)", "30% (Sales low)", "50% (midpoint)", "70% (Sales high)", "100% (all displaced)"]
VF = '+"$"0.00"M";-"$"0.00"M"'
slide("6", "1",
      "Exclusivity is worth +$2.2–2.8M over 2027–29 at plan but only −$0.04M to +$0.55M if the OEM ships 65% of plan",
      "multi-chart-panel", "item",
      {"kind": "panels", "connector": "none", "panels": [
          {"header": "A. Base case, lost direct customers counted in 2028 only: the low case leaves at most $0.55M for three years of irreversible exclusivity",
           "unit_line": "**Option X value, 2027–29**, $M, by channel overlap",
           "body": {"kind": "chart", "chart_type": "column", "sort": "none", "value_format": VF, "categories": OVC,
                    "series": [{"name": "Plan, 29,000 robots", "points": [r("pl_v0"), r("pl_v30"), r("pl_v50"), r("pl_v70"), r("pl_v100")]},
                               {"name": "65% stress, 18,850 robots", "points": [r("st_v0"), r("st_v30"), r("st_v50"), r("st_v70"), r("st_v100")]}],
                    "highlight": ["65% stress, 18,850 robots"]}},
          {"header": "B. If lost 2028 direct customers would also have renewed in 2029, the low case destroys up to $1.1M at Sales' 70% overlap",
           "unit_line": "**Option X value, 2027–29**, $M, by channel overlap",
           "body": {"kind": "chart", "chart_type": "column", "sort": "none", "value_format": VF, "categories": OVC,
                    "series": [{"name": "Plan, 29,000 robots", "points": [r("pl_v0"), r("plB30"), r("plB50"), r("plB70"), r("plB100")]},
                               {"name": "65% stress, 18,850 robots", "points": [r("st_v0"), r("stB30"), r("stB50"), r("stB70"), r("stB100")]}],
                    "highlight": ["65% stress, 18,850 robots"]}}]},
      numbers=[{"text": "+$2.2–2.8M", "data_ref": "pl_v70"}, {"text": "+$2.2–2.8M", "data_ref": "pl_v30"},
               {"text": "−$0.04M", "data_ref": "st_v70"}, {"text": "+$0.55M", "data_ref": "st_v30"}],
      highlights=["65% stress, 18,850 robots"],
      rationale="Sensitivity grid (volume case × overlap) for the base case and the renewal sensitivity -> two panels of multi-series columns",
      unit_line="**Option X three-year incremental value, 2027–29**, $ millions, undiscounted, by OEM volume case and channel overlap",
      footnotes=["Value = Σ(royalties − $80 × robots − $0.9M engineering) − $0.45M assessment − overlap × ($1.8M × 82%). A is the pack-grounded floor (favours X); B is a sensitivity (churn not in pack)",
                 "Full-year engineering from 2027 is conservative: a late start helps all OEM options equally, so the ranking does not change. No NPV, per board instruction"])

# p.7 breakeven
slide("7", "1",
      "Exclusivity breaks even only at 6,100–8,800 robots a year; the 65% case of 6,500 barely clears the most optimistic end",
      "bar-ranking", "item",
      {"kind": "chart", "chart_type": "bar", "sort": "none", "value_format": "#,##0",
       "categories": ["Breakeven, 0% overlap", "Breakeven, 30% overlap", "Breakeven, 50% overlap", "Breakeven, 70% overlap",
                      "Breakeven, 100% overlap", "OEM 2028: 65% stress", "OEM 2028: partner plan"],
       "series": [{"name": "Robots per year", "points": [r("be0"), r("be30"), r("be50"), r("be70"), r("be100"), r("st28"), r("f28")]}],
       "highlight": ["Breakeven, 30% overlap", "Breakeven, 70% overlap", "OEM 2028: 65% stress"]},
      numbers=[{"text": "6,500", "data_ref": "st28"}],
      highlights=["Breakeven, 30% overlap", "Breakeven, 70% overlap", "OEM 2028: 65% stress"],
      rationale="Hurdle against expected volumes -> bars in a fixed order, Sales' range and the stress case highlighted",
      unit_line="**OEM robots a year** needed for exclusivity to beat staying nonexclusive, by channel overlap, against 2028 OEM volumes",
      layout={"variant": "takeaway_sidebar", "sidebar": {
          "kind": "bullets", "header": "The plan clears the hurdle; the stress case clears only the 30% end",
          "bullets": ["**Breakeven bars:** each robot contributes $220, which must cover $0.9M of engineering plus the displaced direct margin",
                      "**Sales' 30–70% overlap:** a hurdle of 6,100–8,800 robots a year; the plan's 10,000 clears it, the stress case's 6,500 clears only the 30% end",
                      "**Option M's gate:** 5,000 annualised is below every realistic breakeven; raise it to about 9,000 (2,250 a quarter) unless the scope excludes customers on other OEMs' robots",
                      "**Under Option N:** the OEM programme alone breaks even at 3,333 robots ($0.9M ÷ $270), and the direct channel is untouched"]}},
      footnotes=["Breakeven = ($0.9M + overlap × $1.476M) ÷ ($300 − $80)"])

# p.8 production bar
slide("8", "2",
      "The software still misses the OEM's bar, yet Option X binds exclusivity at signing, at least five months before certification",
      "timeline-roadmap", "time-series",
      {"kind": "timeline", "periods": ["Nov 2026", "Apr 2027", "Sep 2027", "Dec 2027"],
       "rows": [
           {"label": "Certification", "bars": [{"start": "Nov 2026", "end": "Sep 2027", "label": "Third-party assessment ($0.45M) not started; September is an engineering projection, not a plan with a vendor"}]},
           {"label": "Option X exclusivity", "bars": [{"start": "Apr 2027", "end": "Dec 2027", "emphasis": True, "label": "Binding from signing, before any validation in OEM hardware"}]},
           {"label": "OEM 2027 plan", "bars": [{"start": "Apr 2027", "end": "Dec 2027", "label": "5,000 robots assumed shipped, yet deployment cannot start until the assessment is complete"}]}],
       "milestones": [{"at": "Nov 2026", "label": "Today"}, {"at": "Apr 2027", "label": "Board meets: X binds"},
                      {"at": "Sep 2027", "label": "Earliest certification"}]},
      rationale="Option X timing against the board's own condition -> timeline; the readiness gap reads in the sidebar",
      unit_line="**Option X timing against certification**, November 2026 to December 2027",
      layout={"variant": "takeaway_sidebar", "sidebar": {
          "kind": "reasons", "header": "The production bar is not yet met",
          "reasons": [
              {"header": "Lab uptime", "point": r("uptime"), "detail": "60 robots, 12 weeks; no fully loaded warehouse, no collision-heavy peaks"},
              {"header": "OEM bar", "point": r("bar"), "detail": "In production hardware, with documented safe-stop: not yet demonstrated"},
              {"header": "Downtime cut", "point": r("cut"), "detail": "1.2% → 0.5% of hours: 105 → 44 hours a robot-year at 24/7 (24 → 10 over the trial)"}]}},
      so_what="The board requires validation in OEM hardware before irreversible exclusivity; X fails this by design",
      footnotes=["The 2027 plan of 5,000 robots, and with it the advance's offset exposure, is at risk. The gap is closable but unproven: conditions will be harsher than the lab"])

# p.9 upside evidence
slide("9", "2",
      "The upside case rests on unaudited volumes, an untested 'fully incremental' claim and a correlational competitor analogy",
      "text-columns", "argument",
      {"kind": "text", "style": "columns", "columns": [
          {"header": "OEM volumes are a forecast, not a commitment",
           "detail": ["Quarterly shipment data are not independently audited, and the draft contract has no audit right",
                      "The 14,000 'booked devices' have no purchase orders: treat them as a 2029 forecast",
                      "The 2027 forecast of 5,000 assumes production shipments in a year when certification lands in September at the earliest",
                      "The board is unwilling to rely solely on verbal OEM launch forecasts"],
           "footer": "Plan → 65%: −$2.2M of value (p. 6)"},
          {"header": "Channel overlap is unknown, and it drives the answer",
           "detail": ["The CEO says the OEM channel has 0% overlap (entirely incremental); Sales says 30–70% of OEM buyers overlap with its pipeline",
                      "Neither view is backed by customer-level identifiers",
                      "Each 10 percentage points of overlap is worth about $0.15M a year of displaced direct gross margin ($1.8M × 82% × 10%)",
                      "Overlap can be measured during a nonexclusive pilot, not after exclusivity has closed the direct channel"],
           "footer": "30% → 70%: breakeven 6,100 → 8,800"},
          {"header": "'Exclusivity caused competitors' growth' is not shown",
           "detail": ["Five competitors' exclusive OEM deals coincided with faster growth: a correlation",
                      "Those firms had more marketing support, more mature products and higher market share before they signed; any of these could explain the growth",
                      "Boreal has none of these advantages yet: its product is uncertified and its leverage limited",
                      "No causal evidence is available, so the economics give this argument zero weight"],
           "footer": "No proof it adds volume over N"}]},
      rationale="Three separate weaknesses of the upside case -> text columns, each with its impact",
      unit_line="**Evidence behind the upside case**, by claim, with its impact on the economics",
      footnotes=["Source: board briefing pack §2, §4–5; team analysis"])

# p.10 contract
slide("10", "2",
      "As drafted, the contract leaves Boreal exposed on six terms, with a scope that blocks the growing direct channel",
      "comparison-table", "item",
      {"kind": "table", "table_type": "comparison",
       "columns": ["Draft agreement", "Risk to Boreal", "Required before any exclusivity"],
       "rows": [
           {"label": "Audit rights", "cells": T("No clear right to audit reported shipments", "Royalties and volume gates rest on unaudited OEM reports",
                                                "Independent, shipment-level audit right; quarterly reports reconciled to invoices")},
           {"label": "Royalty floor", "cells": T("None once the $2.0M advance is used up", "Direct channel barred with no minimum income",
                                                 "Annual minimum royalty; exclusivity lapses automatically if missed")},
           {"label": "Release triggers", "cells": T("No automatic release", "Locked in if the model is retired or certification slips",
                                                    "Automatic release on model retirement, certification slip or missed minimums")},
           {"label": "IP protection", "cells": T("Source code delivered as freely reusable OEM IP", "Loss of Boreal's core asset and future leverage",
                                                 "Source code escrow with narrow release conditions; no IP transfer")},
           {"label": "Scope", "highlight": True,
            "cells": T("All new North American sales, including customers on other OEMs' robots",
                       "Chief strategic opportunity cost: about $1.48M a year of direct margin at risk",
                       "Limit to the OEM's robot series; carve out existing and other-OEM customers")},
           {"label": "Guarantee offset", "cells": T("Partner can demand an offset if guaranteed performance is missed",
                                                    "The $2.0M can claw back, e.g. if certification delays 2027 shipments",
                                                    "Define the offset; cap it at the unearned balance; no offset for OEM-driven shortfalls")}]},
      count_word=6, clauses=1,
      rationale="Six contract terms on the same three criteria -> comparison table, the scope row highlighted",
      unit_line="**Draft OEM agreement**, by term: what it says, the risk to Boreal and what any exclusivity requires",
      so_what="Existing direct contracts cannot be terminated for convenience, so any exclusivity can cover only future new North American robot sales",
      so_what_style="line",
      footnotes=["Without that limit, Boreal faces unquantified contract claims. Source: board briefing pack §2, §3, §6 (legal counsel and software team review); team analysis"])

# p.11 five routes
slide("11", "3",
      "Of five routes, only the phased N→M structure keeps the OEM upside without an irreversible bet before the evidence exists",
      "comparison-table", "item",
      {"kind": "table", "table_type": "comparison",
       "columns": ["Indicative value, 2027–29", "Low-case resilience", "Reversibility", "Board conditions*", "Deal risk with OEM"],
       "rows": [
           {"label": "X: exclusive at signing · reject as drafted", "cells": T("+$2.2–2.8M plan; −$0.04M to +$0.55M at 65%", "Weak: thin margin, offset exposure",
                                                         "None: 3 years, binding at signing", "Fails validation-first",
                                                         "Lowest: it is the OEM's ask")},
           {"label": "N: 12-month nonexclusive pilot · recommend, phase 1", "highlight": True,
            "cells": T("Up to +$4.7M plan / +$1.9M at 65% if terms hold (upper bound)", "Strong: no guarantee to recoup; $270 a robot",
                       "High: 12 months", "Meets all", "Medium: OEM's offer; price not guaranteed")},
           {"label": "M: exclusivity after gates · recommend, phase 2", "highlight": True,
            "cells": T("X-like upside, taken only once proven", "Strong: gates screen out the low case", "High until the gates are met",
                       "Meets all", "Medium: termination payment open")},
           {"label": "Direct sales only · fallback", "cells": T("Keeps ~$1.48M a year of direct margin (2028 ARR); no OEM upside", "Strong", "High",
                                                     "Meets all", "Forgoes the OEM")},
           {"label": "Defer until certified · fallback if N refused", "cells": T("As direct, less the $0.45M assessment", "Strong", "High", "Meets all",
                                                         "High: OEM may pick another supplier")}]},
      count_word=5, clauses=1,
      rationale="Five options on the same criteria -> comparison table; options as rows, verdict in the row label, recommended pair highlighted",
      unit_line="**Routes open to the board**, compared on value, resilience, reversibility, board conditions and deal risk",
      footnotes=["*Validation in OEM hardware before irreversible exclusivity; existing licences protected; $2.6M liquidity buffer held. Values from p. 6, 12 and 13",
                 "The integration firm's 1,200-robot nonexclusive pilot complements N and the fallbacks; X would likely bar it. Its royalty terms are not in the pack. Source: board briefing pack §1, §4, §6; team analysis"])

# p.12 N vs X value
slide("12", "3",
      "Nonexclusive terms would match exclusivity's value even if the OEM shipped 24–32% fewer robots without exclusivity",
      "column-time-series", "item",
      {"kind": "chart", "chart_type": "column", "sort": "none", "value_format": VF,
       "categories": ["Partner plan (29,000 robots)", "65% stress (18,850 robots)"],
       "series": [{"name": "X, 30% overlap", "points": [r("pl_v30"), r("st_v30")]},
                  {"name": "X, 70% overlap", "points": [r("pl_v70"), r("st_v70")]},
                  {"name": "N terms, same volumes", "points": [r("pl_N"), r("st_N")]}],
       "highlight": ["N terms, same volumes"]},
      numbers=[{"text": "24–32%", "data_ref": "cush30"}, {"text": "24–32%", "data_ref": "cush70"}],
      highlights=["N terms, same volumes"],
      rationale="Value of the same volumes under X and N terms -> clustered columns, N highlighted",
      unit_line="**Three-year value, 2027–29**, $ millions, Option X at Sales' overlap range against Option N terms at the same volumes",
      layout={"variant": "takeaway_sidebar", "sidebar": {
          "kind": "bullets", "header": "Why N wins on value per unit of risk",
          "bullets": ["**Per robot:** N pays $350 compared with $300 ($270 compared with $220 after support), with no direct-channel displacement",
                      "**Stress case:** the volume cushion is 27–39%",
                      "**Caveats:** the OEM may ship less without exclusivity and will not guarantee pricing; the N bars are an upper bound, the cushion is the robust finding"],
          "rows": [{"label": "Fewer robots at which N still matches X, 30% overlap", "basis": "1 − 22,000 ÷ 29,000 plan robots", "point": r("cush30"), "highlight": True},
                   {"label": "Fewer robots at which N still matches X, 70% overlap", "basis": "1 − 19,800 ÷ 29,000 plan robots", "point": r("cush70"), "highlight": True}]}},
      footnotes=["N assumes its $350 terms and partner volumes persist for 3 years (not guaranteed); some OEM buyers would substitute for direct buyers under N. Parity = (X value + $2.7M + $0.45M) ÷ $270"])

# p.13 liquidity
slide("13", "3",
      "Every route keeps cash above the $2.6M buffer; the advance's liquidity benefit is temporary and can be clawed back",
      "bar-ranking", "item",
      {"kind": "chart", "chart_type": "bar", "sort": "none", "value_format": '"$"0.00"M"',
       "categories": ["Direct sales only", "Defer: assessment only", "N: royalties collected in-year", "N: worst case, no 2027 royalty cash (lag)",
                      "X: plan, advance in hand", "X: certification slips, $2.0M offset"],
       "series": [{"name": "Headroom above $2.6M buffer, end-2027", "points": [r("hd_direct"), r("hd_def"), r("hd_N"), r("hd_Nlag"), r("hd_X"), r("hd_Xslip")]}],
       "highlight": ["X: plan, advance in hand", "X: certification slips, $2.0M offset"]},
      highlights=["X: plan, advance in hand", "X: certification slips, $2.0M offset"],
      rationale="Headroom by route against the same buffer -> bars in route order, the two X cases highlighted",
      unit_line="**Cash headroom above the $2.6M liquidity buffer**, end-2027, $ millions, by route",
      layout={"variant": "takeaway_sidebar", "sidebar": {
          "kind": "bullets", "header": "Liquidity does not require the advance",
          "bullets": ["**Start:** $4.9M of cash leaves $2.3M of headroom above the buffer; OEM routes then spend the $0.45M assessment, $0.9M of engineering and $80 a robot of support ($0.40M at 5,000 robots) before royalty cash arrives",
                      "**N's tightest point is $0.55M**, if reporting lags push all 2027 royalties into 2028; mitigations: monthly remittance, engineering phased to shipments, OEM-funded integration work",
                      "**X looks richest ($2.55M)** only because the advance is unearned; a certification slip plus an offset demand takes it back to $1.85M"],
          "implication": "The advance is not a reason to sign X"}},
      footnotes=["Headroom = $4.9M cash − $2.6M buffer + deal cash flows to end-2027. Rest-of-business burn is not in the pack and is assumed to be covered by the buffer"])

# p.14 recommendation
slide("14", "4",
      "Sign Option N now; three pre-agreed gates switch on limited exclusivity once certification and audited volumes show it pays",
      "process-flow", "structure",
      {"kind": "process", "steps": [
          {"header": "Phase 0 · now to Apr 2027: prepare",
           "detail": ["Commission the $0.45M third-party security and safety assessment now",
                      "Negotiate the N term sheet with the M gates pre-agreed",
                      "Tag customers so OEM and direct overlap can be measured"],
           "footer": "Board decision in April 2027"},
          {"header": "Phase 1 · Apr 2027 to ~Q1 2028: Option N, nonexclusive pilot", "emphasis": True,
           "detail": ["12 months, $350 per shipped robot, no advance",
                      "Boreal keeps all direct and other-OEM rights",
                      "Audit rights and monthly royalty reports from day one"],
           "footer": "Exit: Gates 1–3, all passed"},
          {"header": "Phase 2 · earliest ~Q2 2028: Option M, limited exclusivity",
           "detail": ["Existing licences untouched; new North American sales of the OEM's robot series only",
                      "Up to 3 years, with an annual minimum royalty",
                      "Automatic release if minimums are missed, the model is retired or certification lapses",
                      "Termination payment of at least 1 year of displaced direct margin (~$1.5M)"]}]},
      count_word=3, clauses=1,
      rationale="Phased path with gates between phases -> process flow; the three gates read in the sidebar",
      unit_line="**Recommended path**, three phases; exclusivity only after all three gates are passed",
      layout={"variant": "takeaway_sidebar", "sidebar": {
          "kind": "reasons", "header": "All three gates must pass before Phase 2",
          "reasons": [
              {"header": "Certification", "detail": "≥ 99.5% uptime in OEM production hardware, loaded warehouse, peaks; documented safe-stop; assessment passed"},
              {"header": "Verified demand", "detail": "Two consecutive audited quarters ≥ 2,250 robots (~9,000 a year), breakeven at 70% overlap; 5,000 only with other-OEM carve-out"},
              {"header": "Contract protections", "detail": "Audit right, royalty floor, release triggers, code escrow, existing and other-OEM carve-outs, defined offset"}]}},
      footnotes=["Gates verified by the board, not by OEM assertion. Gate 2 volume: the p. 7 breakeven at 70% overlap (8,787 robots a year), rounded up. Source: board briefing pack §2, §5–7; team analysis"])

# p.15 negotiation
slide("15", "4",
      "Negotiate by trading price, scope and timing for evidence, and walk away from any form of exclusivity that binds at signing",
      "text-columns", "argument",
      {"kind": "text", "style": "columns", "columns": [
          {"header": "Must-haves: walk away without them", "emphasis": True,
           "detail": ["No exclusivity before Gates 1–3 are met",
                      "Existing direct contracts excluded; exclusivity covers future new sales only",
                      "Independent shipment audit right",
                      "Source code escrow; no transfer of reusable IP",
                      "Automatic release on model retirement or certification slip"]},
          {"header": "Tradeables: give to get",
           "detail": ["Royalty: concede from $350 toward $300 at conversion in return for a royalty floor",
                      "Volume gate: accept 5,000 a year instead of about 9,000 if the scope excludes other-OEM customers",
                      "Geography: narrower regions or named verticals first",
                      "Term: shorter initial exclusivity (e.g. 2 years) with renewal on performance",
                      "An advance at conversion, structured as a capped and clearly defined guarantee"]},
          {"header": "Fallback if the OEM refuses: direct sales plus the integration pilot",
           "detail": ["Continue direct sales: about $1.8M of new ARR in 2028, about $1.48M of gross margin",
                      "Take the integration firm's nonexclusive 1,200-robot pilot ($0.22M support budget, no guarantee)",
                      "Complete certification anyway; return to the OEM with production evidence",
                      "This loses the OEM's upside (+$2.2–2.8M at plan) but avoids the low-case downside"]}]},
      rationale="Negotiating position in three parts -> text columns, must-haves emphasised",
      unit_line="**Negotiating position with the OEM**: must-haves, tradeables and the fallback (BATNA)",
      so_what="Leverage is limited, but the OEM itself put N and M on the table, and Boreal has not committed its IP",
      footnotes=["Messaging: announce a 'strategic OEM partnership' now; report any advance as a recoupable guarantee, never as revenue. Source: board briefing pack §1, §4, §6; team analysis"])

# p.16 signposts
slide("16", "4",
      "The pilot is designed to produce all four measurable signposts that would change the recommendation",
      "comparison-table", "item",
      {"kind": "table", "table_type": "comparison",
       "columns": ["Today", "Move toward exclusivity if…", "Move away from the OEM if…"],
       "rows": [
           {"label": "Verified OEM shipments", "cells": T("Unaudited forecast; no purchase orders",
                                                          "Audited run-rate ≥ ~8,800 robots a year: exclusivity pays even at 70% overlap",
                                                          "Run-rate < ~3,300 a year (N) or ~4,100 a year (X): royalties do not cover $0.9M of engineering")},
           {"label": "Realised direct-channel overlap", "cells": T("0% (CEO) against 30–70% (Sales); no customer IDs",
                                                                   "Measured ≤ 30%: breakeven falls to ~6,100 robots a year",
                                                                   "Measured ≥ 70%: breakeven ~8,800 a year; insist on carving out other-OEM customers")},
           {"label": "Support cost per device", "cells": T("$80 estimate", "Pilot confirms ≤ $80 and the $0.9M a year of engineering holds",
                                                           "Above ~$107 a robot, X loses value even at plan volume with 70% overlap (~$166 at 30%)")},
           {"label": "Audit right", "cells": T("Absent from draft", "Shipment-level independent audit agreed and the first audit reconciles",
                                               "No satisfactory audit right: no exclusivity at any reported volume")}]},
      count_word=4, clauses=1,
      rationale="Four signposts on the same three criteria -> comparison table",
      unit_line="**Signposts the board asked for**, with the thresholds that would move the decision either way",
      footnotes=["Thresholds from the p. 7 breakeven formula. Support-cost threshold = ($3.0M − $0.9M − overlap × $1.476M) ÷ 10,000 robots = $107 (70%) or $166 (30%) a robot. Source: board briefing pack §7; team analysis"])

# p.17 assumptions and risks
slide("17", "4",
      "The recommendation holds under its key assumptions; the fallback limits the downside of the main risk, an OEM walkout",
      "text-columns", "argument",
      {"kind": "text", "style": "columns", "columns": [
          {"header": "Key assumptions, and which way each biases the answer",
           "detail": ["**$0.9M a year of engineering for all of 2027–29 on every OEM route:** conservative, equal across X, N and M; the $0.45M assessment, needed for any OEM production route, is neutral across them",
                      "**30–70% overlap applied to the $1.8M direct ARR, 2028 cohort only in the base case:** favours X (a floor on the lost margin)",
                      "**82% direct gross margin, before unquantified sales support:** slightly overstates direct value",
                      "**N's $350 and partner volumes persist beyond 12 months:** favours N; shown as an upper bound",
                      "**No discounting; headroom counts deal cash only:** per the board; rest-of-business burn is not in the pack"]},
          {"header": "Risks and mitigations: the OEM walking away matters most", "emphasis": True,
           "detail": ["**The OEM rejects N and M and signs with a competitor (limited leverage):** M is the OEM's own proposal; trade price, scope and term; the fallback is direct sales plus the integration pilot",
                      "**Certification slips past September 2027:** start the assessment now; release triggers; no exclusivity until passed",
                      "**Royalty reporting lag squeezes cash to $0.55M of headroom:** monthly remittance, phased engineering, OEM-funded integration work",
                      "**Support cost, engineering effort or OEM volumes miss the estimate or plan:** measure in the pilot and reprice before conversion; Gate 2 uses audited volumes, with a royalty floor after conversion",
                      "**The competitor claim proves causal after all:** gated M still captures exclusivity benefits once proven"]}]},
      clauses=2, layout={"variant": "split_2"},
      rationale="Two sides of one robustness claim (assumptions, risks) -> two text columns",
      unit_line="**Robustness of the recommendation**: assumptions with the direction of their bias, and risks with their mitigation",
      footnotes=["Source: board briefing pack §2–7; team analysis"])

# p.18 next steps
slide("18", "4",
      "Start certification now because every OEM route depends on it; bring the gated N→M term sheet to the April 2027 board",
      "data-table", "time-series",
      {"kind": "table", "table_type": "data",
       "columns": ["Action", "Proposed owner", "Output or decision point"],
       "rows": [
           {"label": "Nov–Dec 2026", "highlight": True, "cells": T("Engage the security and industrial-safety assessor ($0.45M)", "CTO / Engineering", "Signed scope; plan to Sep 2027")},
           {"label": "Dec 2026–Mar 2027", "cells": T("Add customer-level identifiers to pipeline and OEM reports", "Sales + Finance", "Baseline for measuring overlap")},
           {"label": "Jan–Mar 2027", "cells": T("Negotiate N: audit, escrow, release, gates, carve-outs", "Partnerships + Legal", "Term sheet for board approval")},
           {"label": "Jan–Mar 2027 ", "cells": T("Replace the CFO dashboard with full incremental margin", "CFO", "Royalty − $80 a robot − $0.9M − lost direct margin")},
           {"label": "Apr 2027", "highlight": True, "cells": T("Board decision: approve N→M or a fallback", "Board", "Signed pilot, or direct + integration pilot")},
           {"label": "Sep 2027", "cells": T("Certification in OEM hardware, loaded and at peak", "Engineering", "Gate 1")},
           {"label": "Q4 2027–Q1 2028", "cells": T("Two audited quarters of shipments; support-cost readout", "Finance", "Gate 2 evidence")},
           {"label": "~Q2 2028", "cells": T("Gate review: convert to M, extend N or exit", "Board", "Exclusivity decision on evidence")}]},
      rationale="Dated actions with owners and outputs -> data table in time order",
      unit_line="**Decisions requested today:** reject Option X as drafted · authorise management to negotiate N with the M gates and must-haves · approve the $0.45M assessment",
      footnotes=["Approving the assessment now leaves $1.85M of headroom above the buffer. Owners are proposed. Source: board briefing pack §1, §2, §5; team analysis"])

# appendix
SL.append({"id": "app", "role": "appendix_divider", "status": "filled"})
AROWS = [
    ("Robots shipped", ["5,000", "10,000", "14,000", "29,000", "3,250", "6,500", "9,100", "18,850"]),
    ("Royalties earned ($300)", ["1.50", "3.00", "4.20", "8.70", "0.98", "1.95", "2.73", "5.66"]),
    ("Variable support ($80)", ["−0.40", "−0.80", "−1.12", "−2.32", "−0.26", "−0.52", "−0.73", "−1.51"]),
    ("OEM engineering", ["−0.90", "−0.90", "−0.90", "−2.70", "−0.90", "−0.90", "−0.90", "−2.70"]),
    ("OEM contribution", ["0.20", "1.30", "2.18", "3.68", "−0.19", "0.53", "1.10", "1.45"]),
    ("Security / safety assessment", ["−0.45", "", "", "−0.45", "−0.45", "", "", "−0.45"]),
    ("Value before channel effects", ["", "", "", "3.23", "", "", "", "1.00"]),
    ("Lost direct GM, 30% / 70%", ["", "−0.44 / −1.03", "", "−0.44 / −1.03", "", "−0.44 / −1.03", "", "−0.44 / −1.03"]),
    ("Exclusivity value, 30% / 70%", ["", "", "", "2.79 / 2.20", "", "", "", "0.55 / −0.04"]),
    ("Memo: cash incl. advance", ["2.00", "2.50", "4.20", "8.70", "2.00", "0.93", "2.73", "5.66"])]
SL.append({"id": "A", "role": "backup", "backup_of": "6", "section_id": "1", "status": "filled",
           "lead_message": {"text": "Option X year-by-year economics under the plan and 65% stress cases", "prefix": "Appendix A:"},
           "message_type": "component", "archetype": "data-table",
           "rationale": "Year-by-year build of the three-year values -> data table",
           "unit_line": "**Option X economics**, $ millions, undiscounted; lost direct margin at 30% / 70% overlap, 2028 cohort only",
           "body": {"kind": "table", "table_type": "data",
                    "columns": ["Plan 2027", "Plan 2028", "Plan 2029", "Plan total", "Stress 2027", "Stress 2028", "Stress 2029", "Stress total"],
                    "rows": [{"label": a, "cells": T(*c), **({"highlight": True} if a.startswith("Exclusivity") else {})} for a, c in AROWS]},
           "footnotes": ["Direct gross margin at risk = $1.8M new 2028 ARR × 82% = $1.476M; × 30% = $0.44M; × 70% = $1.03M. Totals may differ by ±0.01 (rounding). Source: board briefing pack §3–4; team analysis"]})
SL.append({"id": "B", "role": "backup", "backup_of": "7", "section_id": "1", "status": "filled",
           "lead_message": {"text": "Formulas, data sources and the gaps the pilot should close", "prefix": "Appendix B:"},
           "message_type": "structure", "archetype": "text-columns",
           "rationale": "Formulas and data gaps -> text columns",
           "unit_line": "**Method**: formulas behind every number, and how each gap in the pack was handled",
           "body": {"kind": "text", "style": "columns", "columns": [
               {"header": "Value formulas",
                "detail": ["Royalty cash (X) = royalties earned − advance credit still unrecouped (first $2.0M of royalties)",
                           "OEM contribution = robots × (royalty − $80) − $0.9M engineering a year",
                           "Exclusivity value = Σ contribution − $0.45M assessment − overlap × $1.8M × 82%",
                           "Breakeven robots a year = ($0.9M + overlap × $1.476M) ÷ ($300 − $80)"]},
               {"header": "Parity, cash and uptime formulas",
                "detail": ["N parity volume = (X value + $2.7M + $0.45M) ÷ ($350 − $80)",
                           "Headroom = $4.9M − $2.6M + deal cash flows to end-2027",
                           "Downtime cut = 1 − (0.5% ÷ 1.2%) = 58%"]},
               {"header": "Gaps bounded with ranges or sensitivities",
                "detail": ["Channel overlap: no customer-level data; Sales' 30–70% range used, bounded by 0% and 100%",
                           "Direct churn and later cohorts: not in the pack; base case counts the 2028 cohort only, with a 2029 renewal sensitivity on p. 6",
                           "Discount rate: not in the pack; no NPV is computed, per the board"]},
               {"header": "Gaps treated qualitatively or as indicative",
                "detail": ["OEM enforcement terms and termination payment: not in the pack; treated qualitatively",
                           "Integration-firm royalty: not in the pack; treated as a nonexclusive complement, not valued",
                           "Rest-of-business cash burn: not in the pack; the $2.6M buffer is assumed to cover it",
                           "Pricing under N and M: the OEM will not guarantee it; shown as indicative"]}]},
           "footnotes": ["Source: board briefing pack §1–7 and team analysis; the Calculations sheet of the source workbook holds every formula live"]})
SL.append({"id": "end", "role": "end_page", "status": "filled"})

# ---------------------------------------------------------------- storyline
storyline = {
    "governing_thought": "Decline exclusivity at signing: sign a 12-month nonexclusive pilot (Option N) at $350 a robot, with pre-agreed gates that switch on limited exclusivity (Option M)",
    "exec_summary": [
        {"id": "1", "text": "The deal is worth less than it is being presented as", "supports": ["3", "4", "5", "6", "7"],
         "sub_points": [
             {"text": "The $2.0M is a recoupable advance, not extra revenue: three-year OEM cash is $8.7M, not $10.7M", "slide_id": "4"},
             {"text": "Net of all costs, exclusivity is worth +$2.2–2.8M at plan but only −$0.04M to +$0.55M at 65% volumes", "slide_id": "6"}]},
        {"id": "2", "text": "The evidence the board requires for irreversible exclusivity does not exist yet", "supports": ["8", "9", "10"],
         "sub_points": [
             {"text": "Lab uptime is 98.8% against a 99.5% production bar, and the third-party assessment has not started", "slide_id": "8"},
             {"text": "Volumes are unaudited, the growth claim is correlational; the draft lacks audit, floor, release, escrow", "slide_id": "9"}]},
        {"id": "3", "text": "The phased N→M structure beats every alternative", "supports": ["11", "12", "13"],
         "sub_points": [
             {"text": "It earns $50 more a robot, keeps the direct channel and matches X's value even at 24–32% fewer robots", "slide_id": "12"},
             {"text": "It holds cash at least $0.55M above the $2.6M buffer and fails none of the board's conditions", "slide_id": "13"}]},
        {"id": "4", "text": "Gates, signposts and next steps make the decision reversible", "supports": ["14", "15", "16", "17", "18"],
         "sub_points": [
             {"text": "Switch on exclusivity only after certification, two audited quarters of 2,250+ robots and signed protections", "slide_id": "14"},
             {"text": "If the OEM insists on exclusivity at signing, walk away to direct sales plus the integration-firm pilot", "slide_id": "15"},
             {"text": "Start the $0.45M assessment now: it is on the critical path for every OEM route", "slide_id": "18"}]}],
    "next_steps": [
        {"action": "Engage the third-party security and industrial-safety assessor ($0.45M)", "owner": "CTO / Engineering", "timing": "Nov–Dec 2026"},
        {"action": "Add customer-level identifiers to the direct pipeline and OEM reports", "owner": "Sales + Finance", "timing": "Dec 2026–Mar 2027"},
        {"action": "Negotiate the N term sheet with audit, escrow, release, gates and carve-outs", "owner": "Partnerships + Legal", "timing": "Jan–Mar 2027"},
        {"action": "Replace the CFO dashboard with a full incremental-margin view", "owner": "CFO", "timing": "Jan–Mar 2027"},
        {"action": "Decide: approve the gated N→M structure or a fallback", "owner": "Board", "timing": "Apr 2027"}]}

sections = [
    {"id": "1", "title": "The deal is worth less than presented", "exec_item_id": "1", "tracker_label": "Value"},
    {"id": "2", "title": "The evidence does not exist yet", "exec_item_id": "2", "tracker_label": "Evidence"},
    {"id": "3", "title": "N→M beats every alternative", "exec_item_id": "3", "tracker_label": "Alternatives"},
    {"id": "4", "title": "Gates make it reversible", "exec_item_id": "4", "tracker_label": "Path forward"}]

# ---------------------------------------------------------------- compile block
U = lambda id, type, text, loc, crit, sids: {"id": id, "type": type, "text": text, "source_loc": loc, "critical": crit, "slide_ids": sids}
units = [
    U("u1", "answer", "Decline Option X as drafted; sign Option N, a 12-month nonexclusive pilot at $350 per robot, and agree up front the gates under which Option M takes effect", "slides 1, 2, 14", True, ["c", "es", "14", "18"]),
    U("u2", "condition", "Option M takes effect only when certification is passed, two audited quarters at about 9,000 robots a year are shown and contract protections are signed", "slides 2, 14", True, ["es", "14"]),
    U("u3", "claim", "The $2.0M is a recoupable advance, not extra revenue: three-year OEM cash is $8.7M, not $10.7M", "slides 2, 4", True, ["es", "4"]),
    U("u4", "claim", "The 'revenue win' framing overstates three-year OEM income by 23%; revenue is royalties earned ($1.5M in 2027, not $3.5M); the $2.0M is a liability until earned", "slide 4", False, ["4", "15"]),
    U("u5", "claim", "The advance buys timing only ($1.5–2.0M into 2027), which Boreal does not need to stay above its buffer", "slides 4, 13", False, ["4", "13"]),
    U("u6", "claim", "After full costs, only about $0.56M of the $3.00M in 2028 plan royalties is incremental: 19%, not the dashboard's 100%", "slide 5", True, ["5"]),
    U("u7", "claim", "Per robot $220 (73%) after support; $0.27–0.86M across 30–70% overlap; at 65% volumes 2028 is −$0.21M", "slide 5", False, ["5"]),
    U("u8", "claim", "Exclusivity bars all new direct North American licences incl. other-OEM customers: that forgone margin is a cost of Option X, not of the OEM channel", "slides 5, 10", False, ["5", "10"]),
    U("u9", "claim", "Exclusivity is worth +$2.2–2.8M at plan but only −$0.04M to +$0.55M at 65% volumes over 2027–29", "slides 2, 3, 6", True, ["es", "3", "6", "11"]),
    U("u10", "stress case", "If lost 2028 direct customers would also renew in 2029, the low case destroys up to $1.1M at 70% overlap", "slide 6", True, ["6"]),
    U("u11", "assumption", "Full-year engineering from 2027 is conservative; a late start helps all OEM options equally and does not change the ranking", "slides 6, 17", False, ["6", "17"]),
    U("u12", "threshold", "Exclusivity breaks even at 6,100–8,800 robots a year at 30–70% overlap; the plan clears it, the 65% case (6,500) clears only the 30% end", "slide 7", True, ["7"]),
    U("u13", "gate", "Option M's 5,000 gate is below every realistic breakeven and should rise to about 9,000 (2,250 a quarter) unless other-OEM customers are carved out", "slides 7, 14, 15", True, ["7", "14", "15"]),
    U("u14", "threshold", "Under Option N the OEM programme alone breaks even at 3,333 robots a year", "slides 7, 16", False, ["7", "16"]),
    U("u15", "evidence", "Lab uptime 98.8% against a 99.5% bar; loaded-warehouse, peak and production-hardware performance not demonstrated; assessment not started; September 2027 certification is a projection", "slides 2, 3, 8", True, ["es", "3", "8"]),
    U("u16", "claim", "Option X makes exclusivity binding at signing, about five months before the earliest certification, and so fails the board's validation condition by design", "slide 8", True, ["8"]),
    U("u17", "risk", "Deployment cannot start before the assessment, so the 2027 plan of 5,000 robots and the advance's offset exposure are at risk", "slide 8", False, ["8"]),
    U("u18", "claim", "Downtime must fall 58% (105 → 44 hours a robot-year; about 24 → 10 hours over the trial): closable but unproven", "slide 8", False, ["8"]),
    U("u19", "evidence", "OEM volumes are unaudited; the 14,000 'booked devices' have no purchase orders; the board will not rely on verbal forecasts", "slides 2, 9", True, ["es", "9"]),
    U("u20", "evidence", "Channel overlap is unknown (0% CEO against 30–70% Sales), worth about $0.15M a year per 10 percentage points, and measurable only in a nonexclusive pilot", "slide 9", True, ["9"]),
    U("u21", "evidence", "The competitor growth claim is correlational and gets zero weight", "slides 2, 9", True, ["es", "9"]),
    U("u22", "claim", "The draft contract leaves Boreal exposed on six terms (audit, floor, release, IP, scope, offset), each with the fix required", "slides 2, 10", True, ["es", "10"]),
    U("u23", "constraint", "Existing direct contracts cannot be terminated for convenience: any exclusivity can cover only future new North American sales", "slides 10, 15", True, ["10", "15"]),
    U("u24", "alternatives", "Five routes compared: X reject as drafted; N recommend as phase 1; M recommend as phase 2; direct sales fallback; defer fallback if N refused", "slide 11", True, ["11"]),
    U("u25", "claim", "N's value is up to +$4.7M at plan / +$1.9M at 65% if its terms hold: an upper bound", "slides 11, 12", False, ["11", "12"]),
    U("u26", "alternative", "The integration firm's 1,200-robot nonexclusive pilot complements N and the fallbacks; X would likely bar it", "slides 11, 15", False, ["11", "15"]),
    U("u27", "claim", "N matches X's three-year value even if the OEM ships 24–32% fewer robots (27–39% in the stress case); the volume cushion is the robust finding", "slides 2, 12", True, ["es", "12"]),
    U("u28", "claim", "N earns $50 more per robot and does not displace the direct channel", "slides 2, 12", True, ["es", "12"]),
    U("u29", "constraint", "Every route keeps cash above the $2.6M buffer; N's worst case leaves $0.55M, with mitigations", "slides 2, 13", True, ["es", "13"]),
    U("u30", "claim", "X's $2.55M headroom exists only because the advance is unearned; a slip plus offset takes it to $1.85M; liquidity does not require the advance", "slide 13", True, ["13"]),
    U("u31", "plan", "Phase 0 prepare, Phase 1 Option N, Phase 2 Option M (series only, up to 3 years, minimum royalty, release triggers, termination payment ≥ ~$1.5M)", "slide 14", True, ["14"]),
    U("u32", "gates", "Gate 1 certification, Gate 2 two audited quarters ≥ 2,250 robots, Gate 3 contract protections; all three before Phase 2, each verifiable by the board", "slides 2, 14", True, ["es", "14"]),
    U("u33", "negotiation", "Must-haves: no exclusivity before the gates, existing contracts excluded, audit right, escrow, automatic release; walk away without them", "slide 15", True, ["15"]),
    U("u34", "negotiation", "Tradeables: royalty toward $300 for a floor, 5,000 gate if scope carved out, narrower geography, shorter term, a defined capped advance at conversion", "slide 15", False, ["15"]),
    U("u35", "fallback", "If the OEM refuses: continue direct sales, take the integration pilot, certify anyway; loses +$2.2–2.8M of upside but avoids the low-case downside", "slides 2, 15", True, ["es", "15"]),
    U("u36", "context", "Leverage is limited but the OEM put N and M on the table and Boreal has not committed its IP; announce a partnership; report any advance as a guarantee", "slide 15", False, ["15"]),
    U("u37", "signposts", "Four signposts with thresholds: verified shipments (~8,800 / ~3,300 / ~4,100), realised overlap (≤30% / ≥70%), support cost ($80; $107 / $166), audit right", "slide 16", True, ["16"]),
    U("u38", "assumptions", "Key assumptions and the direction of their bias", "slide 17", False, ["17"]),
    U("u39", "risks", "The main risk is the OEM walking away; the fallback limits it; other risks with mitigations", "slide 17", True, ["17"]),
    U("u40", "decisions", "Decisions requested: reject X as drafted; authorise negotiation of N with the pre-agreed M gates and must-haves; approve the $0.45M assessment now (leaves $1.85M headroom)", "slide 18", True, ["18"]),
    U("u41", "next steps", "Dated next steps with proposed owners, from the assessor in Nov–Dec 2026 to the gate review around Q2 2028", "slide 18", True, ["18", "end"]),
    U("u42", "claim", "Only one of six conditions for exclusivity at signing partly holds: the hypothesis survives, refined to a gated path rather than a flat 'no'", "slide 3", True, ["3"]),
    U("u43", "backup", "Option X year-by-year economics, plan and stress", "slide 19", False, ["A"]),
    U("u44", "backup", "Formulas and data gaps", "slide 20", False, ["B"]),
    U("u45", "framing", "Synthetic benchmark data from the briefing pack only; all $ figures undiscounted; no NPV, as the board requested", "slide 1", False, ["c", "6", "B"])]

compile_block = {
    "source": "evidence/analysis.md (finished board deck, 20 slides, extracted to text) built from evidence/briefing-pack.md",
    "variant": "restyle",
    "units": units,
    "untraceable": [
        {"data_point_id": "gate_q", "critical": True,
         "ack": "Kept as the analysis's proposed gate (choice made in the user's absence): it is a policy threshold rounded up from the 8,787-robot breakeven at 70% overlap, which is recomputed from the pack; flagged on p. 14 as rounded up",
         "note": "Not a pack number; reproducible only as a rounding choice, so sourced to the analysis"},
        {"data_point_id": "gate_y", "critical": True,
         "ack": "Kept as the analysis's proposed gate, annualised (4 × 2,250); same basis as gate_q",
         "note": "Not a pack number"},
        {"data_point_id": "fwd", "critical": False,
         "note": "The analysis does not show how the $1.5–2.0M range is built; kept as written on p. 4 and marked as the analysis's figure"},
        {"data_point_id": "hrs", "critical": False,
         "note": "24/7 operation (8,760 hours a year) is the analysis's assumption, not in the pack; downtime hours on p. 8 are estimates built on it, with the basis shown"}],
    "corrections": [],
    "check": {"critical_units": sum(1 for u in units if u["critical"]), "preserved": sum(1 for u in units if u["critical"]),
              "notes": ("Read unit by unit against the deck: every critical unit is on a main-deck slide with the source's numbers, conditions and option ranking "
                        "(X reject; N phase 1; M phase 2; direct fallback; defer fallback if N refused). All source numbers recomputed from the pack; no correction was needed. "
                        "Pack §3 prints the 2027 stress royalty as $0.97M and the analysis as $0.98M: both round 3,250 × $300 = $0.975M, so the analysis's 0.98 is kept. "
                        "Changes of form only: p. 5 drops the source's separate subtotal bar (the $1.30M contribution moves to the sidebar); p. 6 shows the two sensitivity grids as two multi-series column panels instead of shaded tables; "
                        "p. 11 transposes the options table (options as rows); p. 17 combines two pairs of rows into single bullets. Titles shortened to 25 words or fewer while keeping every qualifier.")}}

spec = {
    "spec_version": "0.1", "mode": "deck_detailed",
    "meta": {"title": "Don't give exclusivity away before it is earned",
             "subtitle": "Sign a nonexclusive OEM pilot now; make North American exclusivity conditional on certification and audited volumes",
             "company_name": "Boreal Autonomy", "audience": "Board of Directors · board pre-read for the April 2027 decision",
             "purpose": "Should Boreal Autonomy grant North American exclusivity to an OEM for its industrial robot navigation software in 2027?",
             "date": "2026-11-20", "language": "en-US",
             "confidentiality": "Board pre-read from the board briefing pack only (synthetic benchmark data); all $ figures undiscounted, no NPV",
             "theme": "navy"},
    "inputs": [{"id": "in-1", "kind": "file", "label": "Board briefing pack", "content": "evidence/briefing-pack.md"},
               {"id": "in-2", "kind": "file", "label": "Finished analysis deck (source of truth for the storyline)", "content": "evidence/analysis.md"}],
    "storyline": storyline, "sections": sections, "slides": SL, "data_points": DP,
    "sources": [{"id": "s1", "kind": "user_provided", "name": "Board briefing pack", "input_id": "in-1"},
                {"id": "s2", "kind": "user_provided", "name": "Team analysis deck (Nov 2026)", "input_id": "in-2"},
                {"id": "s3", "kind": "derived", "name": "Team analysis"}],
    "compile": compile_block}

out = sys.argv[1] if len(sys.argv) > 1 else "build/boreal-exclusivity.json"
json.dump(spec, open(out, "w"), ensure_ascii=False, indent=1)
print("wrote", out, len(SL), "slides", len(DP), "data points")
