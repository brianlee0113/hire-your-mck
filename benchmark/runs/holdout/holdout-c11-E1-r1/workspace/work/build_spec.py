"""Builds the Boreal Autonomy storyline spec from the briefing pack."""
import ast, json, operator, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
PACK = (ROOT / "evidence" / "briefing-pack.md").read_text()
OUT = ROOT / "deliverable" / "boreal-oem-exclusivity.json"

DP, VAL = [], {}
_OPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.Div: operator.truediv}


def _ev(expr):
    def ev(n):
        if isinstance(n, ast.Expression): return ev(n.body)
        if isinstance(n, ast.BinOp): return _OPS[type(n.op)](ev(n.left), ev(n.right))
        if isinstance(n, ast.UnaryOp): return -ev(n.operand)
        if isinstance(n, ast.Constant): return n.value
        if isinstance(n, ast.Name): return VAL[n.id]
        raise ValueError(expr)
    return ev(ast.parse(expr, mode="eval"))


def P(id, slide, label, value, unit, excerpt, locator, period=None, used=None):
    if "; column " in excerpt:  # table cell: row label and cell value must both be in the pack
        lab, cell = excerpt.split("; column ")
        assert lab.strip('"') in PACK and cell.split(" = ")[1].strip('"') in PACK, f"cell not in pack: {id}"
    else:
        assert excerpt.replace("**", "") in PACK.replace("**", ""), f"excerpt not in pack: {id}"
    d = {"id": id, "slide_id": slide, "label": label, "value": value, "unit": unit,
         "source_id": "s1", "excerpt": excerpt, "locator": locator}
    if period: d["period"] = period
    if used: d["used_in"] = used
    DP.append(d); VAL[id] = value


def D(id, slide, label, calc, unit, formula, period=None, estimate=False, assumptions=None, nd=4, used=None):
    v = round(_ev(calc), nd)
    names = [n.id for n in ast.walk(ast.parse(calc, mode="eval")) if isinstance(n, ast.Name)]
    d = {"id": id, "slide_id": slide, "label": label, "value": v, "unit": unit, "source_id": "s0",
         "derived_from": list(dict.fromkeys(names)), "formula": formula, "calc": calc}
    if period: d["period"] = period
    if used: d["used_in"] = used
    if estimate:
        d["estimate"] = True
        d["assumptions"] = assumptions
    DP.append(d); VAL[id] = v
    return v


def R(i): return {"data_ref": i}


T3 = '| OEM planning item | 2027 | 2028 | 2029 |'
# ---------------- pack inputs ----------------
P("adv", "1", "Signing payment (advance minimum guarantee)", 2.0, "$M",
  "a $2.0M payment at signing and a $300 royalty per robot shipped", "Briefing pack §1, The proposed deal", "at signing, 2027")
P("roy", "2", "Royalty per robot shipped, proposed exclusive deal (Option X)", 300, "$",
  "a $2.0M payment at signing and a $300 royalty per robot shipped", "Briefing pack §1, The proposed deal")
P("term", "3", "Term of the proposed exclusivity", 3, "years",
  "The OEM proposes three years of exclusive distribution in North America", "Briefing pack §1")
for y, v in (("27", 5000), ("28", 10000), ("29", 14000)):
    P(f"v{y}", "b1", f"Robots shipped, partner forecast, 20{y}", v, "robots",
      f'"Robots shipped, partner forecast"; column 20{y} = "{v:,}"', "Briefing pack §3 table, row 1", f"20{y}")
for y, v in (("27", 1.50), ("28", 3.00), ("29", 4.20)):
    P(f"r{y}", "1", f"Nominal royalty at $300 per robot, 20{y}", v, "$M",
      f'"Nominal royalty at $300/robot"; column 20{y} = "${v:.2f}M"', "Briefing pack §3 table, row 2", f"20{y}")
for y, v in (("27", 0.97), ("28", 1.95), ("29", 2.73)):
    P(f"s{y}", "3", f"Royalty at 65% of plan volumes (stress), 20{y}", v, "$M",
      f'"Stress: 65% of plan volumes"; column 20{y} = "${v:.2f}M"', "Briefing pack §3 table, row 3", f"20{y}")
P("str", "3", "Stress case volumes as a share of plan", 0.65, "%",
  "Stress: 65% of plan volumes", "Briefing pack §3 table, row 3")
P("sup", "2", "Variable support cost per shipped robot", 80, "$",
  '"Support variable cost per robot"; column 2027 = "$80"', "Briefing pack §3 table, row 4", "2027–29")
P("eng", "2", "OEM-specific engineering, quality and support effort", 0.9, "$M",
  "Boreal also expects $0.9M per year of OEM-specific engineering, quality and support effort once deployments begin",
  "Briefing pack §3", "per year")
P("ass", "3", "Security and industrial-safety assessment before large OEM deployment", 0.45, "$M",
  "A security and industrial-safety assessment costing $0.45M must be completed before any large OEM production deployment",
  "Briefing pack §2", "one-time")
P("cash", "8", "Unrestricted cash", 4.9, "$M", "Boreal has $4.9M unrestricted cash", "Briefing pack §2")
P("buf", "8", "Required liquidity buffer", 2.6, "$M",
  "requires a $2.6M liquidity buffer for continued product development and customer support", "Briefing pack §2")
P("arr", "4", "New direct software ARR expected in 2028 in the exclusivity area", 1.8, "$M",
  "approximately $1.8M of new direct software ARR in 2028 from customers in the exclusivity area", "Briefing pack §4", "2028")
P("gm", "4", "Direct gross margin used by Finance", 0.82, "%",
  "Finance uses 82% direct gross margin on that ARR before incremental sales support", "Briefing pack §4")
P("ovl_lo", "4", "Sales estimate of OEM buyers overlapping the direct pipeline, low end", 0.30, "%",
  "Sales estimates that 30–70% of OEM buyers could overlap with its direct pipeline", "Briefing pack §4")
P("ovl_hi", "4", "Sales estimate of OEM buyers overlapping the direct pipeline, high end", 0.70, "%",
  "Sales estimates that 30–70% of OEM buyers could overlap with its direct pipeline", "Briefing pack §4")
P("one", "4", "Contractual ceiling: share of new direct North American licensing barred by exclusivity", 1.0, "%",
  "The proposed exclusivity would also bar direct licensing to new customers that buy robots from other OEMs",
  "Briefing pack §6; 100% = all new direct licensing in the territory")
P("integ", "5", "Robots in the integration firm's nonexclusive pilot offer", 1200, "robots",
  "A separate industrial integration firm has offered a smaller nonexclusive pilot for 1,200 robots", "Briefing pack §4")
P("up_t", "6", "Uptime in the twelve-week lab trial", 0.988, "%",
  "A twelve-week lab trial on 60 robots had 98.8% uptime", "Briefing pack §5", "12-week lab trial")
P("up_r", "6", "Uptime required for OEM production acceptance", 0.995, "%",
  "the OEM's required production acceptance is 99.5% uptime", "Briefing pack §5")
P("trial_n", "6", "Robots in the lab trial", 60, "robots",
  "A twelve-week lab trial on 60 robots had 98.8% uptime", "Briefing pack §5")
P("dash", "2", "Gross margin on the $300 royalty shown on the CFO's partner dashboard", 1.0, "%",
  "reports 100% gross margin on the $300 royalty", "Briefing pack §5")
P("comp", "5", "Competitors the CEO cites as evidence", 5, "competitors",
  "The CEO cites five competitors whose exclusive OEM partnerships coincided with faster revenue growth", "Briefing pack §5")
P("booked", "5", "Future robots the competitor deck calls booked devices", 14000, "robots",
  "the OEM's expected 14,000 future robots \"booked devices\"", "Briefing pack §5", "2029 forecast")
P("n_roy", "9", "Royalty per robot shipped, nonexclusive pilot (Option N)", 350, "$",
  "Option N is a 12-month nonexclusive pilot, $350 per shipped robot and no upfront guarantee", "Briefing pack §6")
P("n_mo", "11", "Length of the nonexclusive pilot (Option N)", 12, "months",
  "Option N is a 12-month nonexclusive pilot", "Briefing pack §6")
P("m_thr", "11", "Volume gate offered in Option M, robots shipped annualized", 5000, "robots",
  "two consecutive quarters above 5,000 shipped robots annualized", "Briefing pack §6")

# ---------------- derived ----------------
D("cash28", "1", "Cash received in 2028 under Option X, net of the remaining advance credit", "r28 - (adv - r27)", "$M",
  "$3.00M royalties − ($2.0M advance − $1.50M credited in 2027)", "2028")
D("roy3", "1", "Royalties earned, 2027–29, plan volumes", "r27 + r28 + r29", "$M", "1.50 + 3.00 + 4.20", "2027–29")
D("cash3", "1", "Cash received, 2027–29, plan volumes (advance credited once)", "adv + cash28 + r29", "$M", "2.0 + 2.5 + 4.2", "2027–29")
D("over", "1", "Overstatement of three-year deal value if the advance is counted on top of royalties", "adv / roy3", "%",
  "$2.0M ÷ $8.7M", "2027–29", nd=2)
D("cov27s", "1", "Share of the advance used up by 2027 royalties at 65% of plan", "s27 / adv", "%", "$0.97M ÷ $2.0M", "2027")
D("unit", "2", "Royalty after variable support, per robot, Option X", "roy - sup", "$", "$300 − $80")
D("nsup", "2", "Variable support per robot (negative step)", "0 - sup", "$", "−$80")
D("eng_pr", "2", "Dedicated OEM team cost per robot at 2027 plan volume (negative step)", "0 - eng * 1000000 / v27", "$",
  "−$0.9M ÷ 5,000 robots", "2027")
D("left27", "2", "Left per robot after support and the dedicated team, 2027 plan volume", "roy - sup - eng * 1000000 / v27", "$",
  "$300 − $80 − $180", "2027")
D("lsh", "2", "Share of the $300 royalty left after support and the dedicated team, 2027 plan volume", "left27 / roy", "%", "$40 ÷ $300", "2027")
D("be", "2", "Robots a year needed to cover the dedicated OEM team at $220 a robot", "eng * 1000000 / unit", "robots",
  "$0.9M ÷ $220", "per year", nd=0)
D("vt", "b1", "Robots shipped, 2027–29, partner forecast", "v27 + v28 + v29", "robots", "5,000 + 10,000 + 14,000", "2027–29")
for y in ("27", "28", "29"):
    D(f"nsup{y}", "b1", f"Variable support cost, 20{y}, plan (negative)", f"0 - v{y} * sup / 1000000", "$M", f"−robots × $80", f"20{y}")
    D(f"nsups{y}", "b1", f"Variable support cost, 20{y}, 65% of plan (negative)", f"0 - v{y} * str * sup / 1000000", "$M",
      "−robots × 65% × $80", f"20{y}")
D("neng", "b1", "Dedicated OEM team, per year (negative)", "0 - eng", "$M", "−$0.9M", "per year")
D("nass", "3", "Safety assessment (negative step)", "0 - ass", "$M", "−$0.45M", "2027")
D("nsup3", "3", "Variable support, 2027–29, plan (negative step)", "0 - vt * sup / 1000000", "$M", "−29,000 robots × $80", "2027–29")
D("neng3", "3", "Dedicated OEM team, 2027–29 (negative step)", "0 - eng * term", "$M", "−$0.9M × 3 years", "2027–29")
D("net3", "3", "Net contribution of Option X, 2027–29, plan volumes, before lost direct sales", "roy3 + nsup3 + neng3 + nass", "$M",
  "8.70 − 2.32 − 2.70 − 0.45", "2027–29")
D("sroy3", "3", "Royalties earned, 2027–29, at 65% of plan", "s27 + s28 + s29", "$M", "0.97 + 1.95 + 2.73", "2027–29")
D("nsups3", "3", "Variable support, 2027–29, at 65% of plan (negative step)", "0 - vt * str * sup / 1000000", "$M",
  "−29,000 × 65% × $80", "2027–29")
D("snet3", "3", "Net contribution of Option X, 2027–29, at 65% of plan, before lost direct sales", "sroy3 + nsups3 + neng3 + nass", "$M",
  "5.65 − 1.51 − 2.70 − 0.45", "2027–29")
D("keep3", "3", "Stress-case net contribution as a share of plan-case net contribution", "snet3 / net3", "%", "$0.99M ÷ $3.23M", "2027–29")
# backup year rows
D("net27", "b1", "Net contribution, 2027, plan", "r27 + nsup27 + neng + nass", "$M", "1.50 − 0.40 − 0.90 − 0.45", "2027")
D("c28", "4", "Option X contribution, 2028, plan, before lost direct sales", "r28 + nsup28 + neng", "$M", "3.00 − 0.80 − 0.90", "2028")
D("c29", "b1", "Net contribution, 2029, plan", "r29 + nsup29 + neng", "$M", "4.20 − 1.12 − 0.90", "2029")
D("snet27", "b1", "Net contribution, 2027, 65% of plan", "s27 + nsups27 + neng + nass", "$M", "0.97 − 0.26 − 0.90 − 0.45", "2027")
D("sc28", "4", "Option X contribution, 2028, 65% of plan, before lost direct sales", "s28 + nsups28 + neng", "$M", "1.95 − 0.52 − 0.90", "2028")
D("sc29", "b1", "Net contribution, 2029, 65% of plan", "s29 + nsups29 + neng", "$M", "2.73 − 0.73 − 0.90", "2029")
# direct channel
D("dgp", "4", "2028 direct gross profit at stake in the exclusivity area", "arr * gm", "$M", "$1.8M × 82%", "2028")
OVA = ["Sales' 30–70% overlap of OEM buyers with the direct pipeline is used as a proxy for the share of new direct gross profit lost; no customer-level data exists",
       "100% is the contractual ceiling: exclusivity bars all new direct licensing in North America, including buyers of other OEMs' robots",
       "Direct gross profit uses Finance's 82% margin before incremental sales support, so the loss is slightly overstated",
       "Only the 2028 direct cohort is counted; it recurs in 2029 and later cohorts are not sized in the pack, so the loss is understated"]
D("disp30", "4", "2028 direct gross profit lost at 30%", "dgp * ovl_lo", "$M", "$1.48M × 30%", "2028", True, OVA)
for tag, f, cap in (("0", None, "0%"), ("30", "ovl_lo", "30%"), ("70", "ovl_hi", "70%"), ("100", "one", "100%")):
    if f is None:
        continue
    D(f"x28_{tag}", "4", f"Option X 2028 contribution at plan, after losing {cap} of direct gross profit", f"c28 - dgp * {f}", "$M",
      f"$1.30M − $1.48M × {cap}", "2028")
    D(f"sx28_{tag}", "4", f"Option X 2028 contribution at 65% of plan, after losing {cap} of direct gross profit", f"sc28 - dgp * {f}", "$M",
      f"$0.53M − $1.48M × {cap}", "2028")
D("thr", "4", "Share of 2028 direct gross profit lost at which Option X stops paying at 65% of plan", "sc28 / dgp", "%",
  "$0.53M ÷ $1.48M", "2028", nd=2)
D("thr_b", "4", "Share of 2028 direct gross profit lost at which Option X stops paying at plan volumes", "c28 / dgp", "%",
  "$1.30M ÷ $1.48M", "2028")
# readiness
D("dtr", "6", "Lab-trial downtime as a multiple of the downtime the OEM allows", "(1 - up_t) / (1 - up_r)", "x",
  "(100% − 98.8%) ÷ (100% − 99.5%)", nd=2)
# liquidity
D("nbuf", "8", "Liquidity buffer (negative step)", "0 - buf", "$M", "−$2.6M")
D("head", "8", "Cash headroom above the liquidity buffer", "cash - buf", "$M", "$4.9M − $2.6M")
D("left", "8", "Cash left above the buffer after a first year of OEM costs, with no royalty cash", "cash - buf - ass - eng + nsup27", "$M",
  "$4.9M − $2.6M − $0.45M − $0.9M − $0.40M", "2027")
D("hshare", "8", "Share of the headroom used by a first year of OEM costs", "(ass + eng - nsup27) / head", "%",
  "($0.45M + $0.9M + $0.40M) ÷ $2.3M", "2027")
# pilot vs exclusivity
D("unitN", "9", "Royalty after variable support, per robot, Option N", "n_roy - sup", "$", "$350 − $80")
VNA = ["The pilot's $350 rate and no advance would carry into 2028; the OEM has not guaranteed final pricing",
       "The dedicated OEM team costs $0.9M a year under either option",
       "Exclusivity is charged with losing 30% of 2028 direct gross profit, the low end of Sales' range; the pilot keeps direct licensing open",
       "Overlap between OEM buyers and the direct pipeline would cut direct sales under both options, so it is not charged to either"]
D("vN", "9", "Robots the OEM must ship in 2028 for pilot terms to match Option X (30% direct loss)", "(x28_30 + eng) * 1000000 / unitN",
  "robots", "($0.86M + $0.90M) ÷ $270", "2028", True, VNA, nd=0)
D("vN_sh", "9", "Volume shortfall against the 2028 plan at which pilot terms still match Option X", "1 - vN / v28", "%",
  "1 − 6,507 ÷ 10,000", "2028", True, VNA)
D("vN70", "9", "Robots the OEM must ship in 2028 for pilot terms to match Option X (70% direct loss)", "(x28_70 + eng) * 1000000 / unitN",
  "robots", "($0.27M + $0.90M) ÷ $270", "2028", True, VNA, nd=0)
# gates and signals
D("gate", "11", "Annualized robots needed to cover the dedicated team and 70% of direct gross profit at $220 a robot",
  "(eng + dgp * ovl_hi) * 1000000 / unit", "robots", "($0.9M + $1.48M × 70%) ÷ $220", "per year", nd=0)
D("gate30", "12", "Annualized robots needed to cover the dedicated team and 30% of direct gross profit at $220 a robot",
  "(eng + dgp * ovl_lo) * 1000000 / unit", "robots", "($0.9M + $1.48M × 30%) ÷ $220", "per year", nd=0)
D("sup_thr", "12", "Support cost per robot at which 2027 plan royalties stop covering the dedicated team", "roy - eng * 1000000 / v27", "$",
  "$300 − $0.9M ÷ 5,000", "2027")

def K(i, slide="b1"):
    d = next(x for x in DP if x["id"] == i)
    D(f"{i}_k", slide, d["label"] + " ($ thousands)", f"{i} * 1000", "$K", f"{d['formula'] if 'formula' in d else d['label']} in $ thousands",
      d.get("period"), nd=0)
    return f"{i}_k"


for _i in ["r27", "r28", "r29", "roy3", "adv", "cash28", "cash3", "nsup27", "nsup28", "nsup29", "nsup3", "neng", "neng3", "nass",
           "net27", "c28", "c29", "net3", "s27", "s28", "s29", "sroy3", "snet27", "sc28", "sc29", "snet3"]:
    K(_i)
K("dgp", "4"); K("disp30", "4"); K("x28_30", "9"); K("eng", "9")
VAL["r29_k"]  # sanity

# ---------------- slides ----------------
S = []
S += [{"id": "c", "role": "cover", "status": "filled"},
      {"id": "es", "role": "exec_summary", "status": "filled", "archetype": "exec-summary", "message_type": "navigation"}]


def div(n): return {"id": f"d{n}", "role": "section_divider", "section_id": str(n), "status": "filled",
                    "archetype": "section-divider", "message_type": "navigation"}


SRC_FOOT = "Source: Boreal Autonomy briefing pack (partner forecast, Finance and Sales estimates); team analysis"

# 1 cash vs royalties
S += [div(1), {
    "id": "1", "role": "content", "section_id": "1", "status": "filled",
    "lead_message": {"text": "The $2.0M signing payment is prepaid royalty, not new revenue: counting it on top would overstate the deal by 23%",
                     "numbers": [{"text": "$2.0M", "data_ref": "adv"}, {"text": "23%", "data_ref": "over"}], "clauses": 1},
    "message_type": "time-series", "archetype": "column-time-series",
    "rationale": "Royalties earned against cash received by year -> clustered columns, three periods",
    "unit_line": "**Option X royalties earned and cash received**, $ millions, partner plan volumes, 2027–29",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {
        "kind": "big_number", "header": "The advance moves cash forward; it adds nothing to the total",
        "big_number": R("over"), "caption": "overstatement of three-year value if the advance is booked on top of royalties",
        "bullets": ["**2027:** the advance absorbs all of the year's royalties",
                    "**2028:** cash trails royalties while the unused credit is netted",
                    "**At 65% of plan:** 2027 royalties use under half the advance, and the OEM can demand an offset"]}},
    "body": {"kind": "chart", "chart_type": "column", "categories": ["2027", "2028", "2029"],
             "series": [{"name": "Royalties earned", "points": [R("r27"), R("r28"), R("r29")]},
                        {"name": "Cash received", "points": [R("adv"), R("cash28"), R("r29")]}],
             "sort": "none", "highlight": [], "value_format": "\"$\"0.0\"M\""},
    "footnotes": ["The $2.0M is an advance minimum guarantee credited against the first $2.0M of earned royalties; royalties count only when robots ship, and cash arrives after a reporting lag",
                  "Royalties and cash both total $8.7M over 2027–29 at plan volumes; year-by-year detail in the appendix"]}]

# 2 per-robot waterfall
S.append({
    "id": "2", "role": "content", "section_id": "1", "status": "filled",
    "lead_message": {"text": "At 2027 plan volumes, support and the dedicated OEM team absorb most of each royalty, leaving $40 of the $300",
                     "numbers": [{"text": "$40", "data_ref": "left27"}, {"text": "$300", "data_ref": "roy"}],
                     "highlights": ["Dedicated OEM team"], "clauses": 1},
    "message_type": "component", "archetype": "waterfall-bridge",
    "rationale": "What one royalty breaks down into -> waterfall from royalty to what is left",
    "unit_line": "**Option X economics per robot shipped**, $ per robot, 2027 partner plan of 5,000 robots",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {
        "kind": "big_number", "header": "The dashboard's margin is not the deal's margin",
        "big_number": R("lsh"), "caption": "of each royalty is left at 2027 plan volume, against the 100% margin the CFO dashboard reports",
        "bullets": ["**Support:** the dashboard leaves out the $80 support cost on every robot shipped",
                    "**Dedicated team:** $0.9M a year of engineering, quality and support, a fixed cost spread over few robots in 2027",
                    "**Volume:** the team is covered only above about 4,091 robots a year, which the 65% stress case misses"]}},
    "body": {"kind": "chart", "chart_type": "waterfall",
             "categories": ["Royalty per robot", "Variable support", "Dedicated OEM team", "Left per robot"],
             "series": [{"name": "Per robot", "points": [R("roy"), R("nsup"), R("eng_pr"), R("left27")]}],
             "sort": "none", "highlight": ["Dedicated OEM team"], "value_format": "\"$\"0"},
    "footnotes": ["Dedicated team cost per robot = $0.9M a year ÷ 5,000 robots in the 2027 partner forecast; the dashboard's 100% margin also leaves out the direct sales exclusivity would give up (section 2)"]})

# 3 three-year panels
S.append({
    "id": "3", "role": "content", "section_id": "1", "status": "filled",
    "lead_message": {"text": "Net of all OEM costs, three years of exclusivity contribute $3.2M at plan but only $1.0M at 65% of volumes",
                     "numbers": [{"text": "$3.2M", "data_ref": "net3"}, {"text": "$1.0M", "data_ref": "snet3"}], "clauses": 2},
    "message_type": "component", "archetype": "multi-chart-panel",
    "rationale": "Two cases of one bridge (plan and stress) -> two waterfall panels, no arrow",
    "layout": {"variant": "split_2"},
    "body": {"kind": "panels", "panels": [
        {"header": "At plan, fixed and variable costs take nearly two-thirds of royalties",
         "unit_line": "**Option X, 2027–29, partner plan**, $ millions",
         "body": {"kind": "chart", "chart_type": "waterfall",
                  "categories": ["Royalties", "Support", "OEM team", "Assessment", "Net"],
                  "series": [{"name": "Plan", "points": [R("roy3"), R("nsup3"), R("neng3"), R("nass"), R("net3")]}],
                  "sort": "none", "highlight": ["Net"], "value_format": "\"$\"0.00\"M\""}},
        {"header": "At 65% of plan, the same fixed costs leave about a sixth of royalties",
         "unit_line": "**Option X, 2027–29, 65% of plan volumes**, $ millions",
         "body": {"kind": "chart", "chart_type": "waterfall",
                  "categories": ["Royalties", "Support", "OEM team", "Assessment", "Net"],
                  "series": [{"name": "Stress", "points": [R("sroy3"), R("nsups3"), R("neng3"), R("nass"), R("snet3")]}],
                  "sort": "none", "highlight": ["Net"], "value_format": "\"$\"0.00\"M\""}}]},
    "so_what": "Fixed costs do not shrink with volume, so a 35% shortfall in shipments wipes out more than two-thirds of the deal's value",
    "so_what_style": "line",
    "footnotes": ["Before any direct sales lost to exclusivity (section 2); the $0.9M team is counted for all three years and the $0.45M safety assessment once, in 2027",
                  "Support at $80 a robot on 29,000 planned robots (18,850 at 65%)"]})

# 4 direct channel sensitivity
S += [div(2), {
    "id": "4", "role": "content", "section_id": "2", "status": "filled",
    "lead_message": {"text": "Exclusivity's 2028 value hinges on direct sales nobody has measured: at 65% of volumes it turns negative above 36% lost",
                     "numbers": [{"text": "36%", "data_ref": "thr"}], "clauses": 1},
    "message_type": "item", "archetype": "column-time-series",
    "rationale": "Same 2028 contribution under four direct-loss scenarios, plan and stress -> clustered columns",
    "unit_line": "**Option X contribution in 2028 after lost direct gross profit**, $ millions, by share of 2028 direct gross profit lost",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {
        "kind": "big_number", "header": "The answer turns on a number the pipeline cannot yet show",
        "big_number": R("thr"), "caption": "of 2028 direct profit lost, and exclusivity stops paying at 65% of volumes",
        "bullets": ["**CEO view:** assumes no loss, yet the contract bars all new direct licensing",
                    "**Ceiling:** negative even at plan, which breaks even at 88% lost",
                    "**Understated:** the lost 2028 ARR recurs in 2029"]}},
    "body": {"kind": "chart", "chart_type": "column",
             "categories": ["0% (CEO view)", "30% (Sales low)", "70% (Sales high)", "100% (all new direct)"],
             "series": [{"name": "Plan volumes", "points": [R("c28"), R("x28_30"), R("x28_70"), R("x28_100")]},
                        {"name": "65% of plan", "points": [R("sc28"), R("sx28_30"), R("sx28_70"), R("sx28_100")]}],
             "sort": "none", "highlight": [], "value_format": "\"$\"0.00\"M\""},
    "basis": {"header": "How each bar is built", "terms": [
                 {"point": R("dgp_k"), "caption": "2028 direct gross profit ($1.8M ARR × 82%)"},
                 {"op": "×", "point": R("ovl_lo"), "caption": "share lost (Sales: 30–70%; ceiling 100%)"},
                 {"op": "=", "point": R("disp30_k"), "caption": "direct profit lost, deducted per bar"}]},
    "footnotes": ["Bars start from 2028 contribution of $1.30M at plan and $0.53M at 65% (royalties less support and team); Sales' overlap is a proxy for direct loss, with no customer-level data behind it"]}]

# 5 text columns
S.append({
    "id": "5", "role": "content", "section_id": "2", "status": "filled",
    "lead_message": {"text": "The growth case for exclusivity rests on correlation and an unbooked forecast, while what it gives up is certain",
                     "clauses": 1},
    "message_type": "argument", "archetype": "text-columns",
    "rationale": "Contrast of evidence quality on both sides -> text columns",
    "layout": {"variant": "full"},
    "body": {"kind": "text", "style": "columns", "columns": [
        {"header": "Competitor wins show correlation, not cause",
         "detail": ["The five firms got more OEM marketing support than Boreal is offered",
                    "Their products were more mature when they signed",
                    "They already held more market share before exclusivity",
                    "Nothing isolates what exclusivity itself added"],
         "point": R("comp"), "point_caption": "competitors cited by the CEO as proof"},
        {"header": "The volume is a forecast, not a booking",
         "detail": ["The competitor deck calls the 2029 forecast \"booked devices\"",
                    "No customer has issued a purchase order",
                    "OEM quarterly shipment data are not independently audited",
                    "Royalties count only when robots ship, and cash arrives after a lag"],
         "point": R("booked"), "point_caption": "robots called booked, with no purchase orders"},
        {"header": "The cost is Boreal's freedom to sell",
         "detail": ["Bars direct licensing to new North American customers, even on other OEMs' robots",
                    "Conflicts with the integration firm's nonexclusive pilot offer",
                    "Runs three years and starts at signing, before certification",
                    "Existing direct contracts must stay outside it, or Boreal faces claims"],
         "point": R("arr"), "point_caption": "new direct ARR expected in 2028 in the territory", "emphasis": True}]},
    "footnotes": ["The integration firm offers a 1,200-robot nonexclusive pilot with no minimum guarantee; its royalty is not in the pack"]})

# 6 KPI readiness
S += [div(3), {
    "id": "6", "role": "content", "section_id": "3", "status": "filled",
    "lead_message": {"text": "The software is not production-ready yet: lab downtime ran at 2.4 times the OEM's limit, before any peak-load test",
                     "numbers": [{"text": "2.4 times", "data_ref": "dtr"}], "clauses": 1},
    "message_type": "item", "archetype": "kpi-big-numbers",
    "rationale": "Three readiness facts against one bar -> KPI tiles",
    "unit_line": "**Production readiness of Boreal's navigation stack in OEM hardware**, lab trial and acceptance criteria",
    "body": {"kind": "kpi", "items": [
        {"point": R("up_t"), "caption": "uptime in a 12-week lab trial on 60 robots", "relation": "Below the OEM's production bar",
         "drivers": ["Run in a lab, not in a fully loaded warehouse", "Collision-heavy peak conditions were not tested",
                     "Safe-stop performance is not yet documented"]},
        {"point": R("up_r"), "caption": "uptime the OEM requires for production acceptance", "relation": "Plus documented safe stops at full load",
         "drivers": ["The board wants this proven in OEM hardware before irreversible exclusivity",
                     "The draft makes exclusivity effective at signing, before this test",
                     "The 2027 forecast assumes shipments before certification is done"]},
        {"point": R("dtr"), "caption": "trial downtime as a multiple of the downtime the OEM allows", "relation": "Downtime has to fall by more than half",
         "drivers": ["The $0.45M third-party assessment has not started",
                     "Engineering targets certification by September 2027",
                     "Any slip delays royalties under every option"]}]},
    "footnotes": ["Downtime = 100% − uptime: 1.2% in the trial against 0.5% allowed; small sample, so the multiple is indicative only"]}]

# 7 contract protections
ROWS7 = [("Timing of exclusivity", "Effective at signing, before certification", "Only after documented uptime and safety validation", "Board condition"),
         ("Scope", "Exclusive North American distribution", "New OEM robot sales only; existing and other-OEM customers stay direct", "Avoids contract claims"),
         ("Shipment audit", "No clear right to audit reported shipments", "Audit right over quarterly shipment reports", "OEM data unaudited"),
         ("Royalty floor", "No minimum once the advance is used", "Minimum royalty floor for any exclusive period", "Protects the price of exclusivity"),
         ("Release", "No release if the model is retired or certification slips", "Automatic release on either event", "Caps the downside"),
         ("Source code", "No escrow; code reusable by the OEM", "Source code held in escrow, not handed over", "Protects Boreal's IP")]
S.append({
    "id": "7", "role": "content", "section_id": "3", "status": "filled",
    "lead_message": {"text": "As drafted, the contract lacks six protections the board and counsel require before any exclusivity", "count_word": 6, "clauses": 1},
    "message_type": "item", "archetype": "comparison-table",
    "rationale": "Draft terms against required terms, row by row -> comparison table with verdict column",
    "unit_line": "**Proposed OEM agreement (Option X) against board and counsel requirements**, April 2027",
    "layout": {"variant": "full"},
    "body": {"kind": "table", "table_type": "comparison", "columns": ["What the draft says", "What Boreal needs"],
             "rows": [{"label": l, "cells": [{"text": a}, {"text": b}], "note": n} for l, a, b, n in ROWS7],
             "verdict_header": "Why it matters"},
    "callout": {"target": "Timing of exclusivity", "header": "Breaks a board condition", "detail": "Exclusivity before certification is irreversible"},
    "footnotes": ["From legal counsel, the software team and the board's stated conditions in the briefing pack; the OEM has not yet agreed to any of these terms"]})

# 8 liquidity waterfall
S.append({
    "id": "8", "role": "content", "section_id": "3", "status": "filled",
    "lead_message": {"text": "Boreal can fund a first year of OEM work without the advance, with $0.55M to spare above its liquidity buffer",
                     "numbers": [{"text": "$0.55M", "data_ref": "left"}], "highlights": ["Left above buffer"], "clauses": 1},
    "message_type": "component", "archetype": "waterfall-bridge",
    "rationale": "Cash to what is left after the buffer and OEM costs -> waterfall",
    "unit_line": "**Cash available for the OEM program before any royalty cash**, $ millions, first year from signing",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {
        "kind": "bullets", "header": "The advance is not what makes the program affordable",
        "bullets": ["**Assessment:** due under any OEM option",
                    "**Advance risk:** the OEM can demand an offset if royalties fall short",
                    "**Thin cushion:** new costs need board sign-off"],
        "rows": [{"label": "Share of headroom used by year-one OEM costs",
                  "basis": "($0.45M + $0.90M + $0.40M) ÷ $2.3M", "point": R("hshare"), "highlight": True}]}},
    "body": {"kind": "chart", "chart_type": "waterfall",
             "categories": ["Unrestricted cash", "Liquidity buffer", "Safety assessment", "Dedicated OEM team", "Support, 5,000 robots", "Left above buffer"],
             "series": [{"name": "Cash", "points": [R("cash"), R("nbuf"), R("nass"), R("neng"), R("nsup27"), R("left")]}],
             "sort": "none", "highlight": ["Left above buffer"], "value_format": "\"$\"0.00\"M\""},
    "footnotes": ["Conservative: a full year of team and support cost at 2027 plan volume, no royalty cash; the pack gives no operating burn beyond what the $2.6M buffer covers"]})

# 9 calc bridge pilot vs X
S += [div(4), {
    "id": "9", "role": "content", "section_id": "4", "status": "filled",
    "lead_message": {"text": "On pilot terms, 6,508 robots in 2028 would match exclusivity's value, a third below the OEM's own plan",
                     "numbers": [{"text": "6,508", "data_ref": "vN"}], "clauses": 1},
    "message_type": "component", "archetype": "calculation-bridge",
    "rationale": "Our estimate of the volume at which the sceptic's alternative wins -> calculation-bridge",
    "unit_line": "**Robots the OEM must ship in 2028 for the nonexclusive pilot terms to match Option X**, team estimate",
    "body": {"kind": "equation", "terms": [
        {"point": R("x28_30_k"), "caption": "Option X contribution in 2028 at plan, after losing 30% of direct gross profit (p. 8)"},
        {"op": "+", "point": R("eng_k"), "caption": "dedicated OEM team, a cost under either option"},
        {"op": "÷", "point": R("unitN"), "caption": "pilot royalty of $350 a robot, after $80 support"},
        {"op": "=", "point": R("vN"), "caption": "robots in 2028 for the pilot to match exclusivity, against a plan of 10,000"}],
     "assumptions_header": "Exclusivity wins only if withholding it cuts OEM volume by more than a third",
     "assumptions": VNA[:2] + ["Exclusivity is charged with losing 30% of 2028 direct gross profit; at 70% the pilot needs only 4,321 robots",
                               VNA[3]]},
    "footnotes": ["Team estimate from briefing-pack inputs; live formula in the Calculations sheet of the source workbook"]}]

# 10 harvey options
H = [("X: exclusive at signing", [0, 0, 0, 3], R("unit"), "Reject: breaks the board's certification condition"),
     ("M: gated exclusivity now", [2, 4, 2, 3], "To negotiate", "Gate too low; pricing and termination payment open"),
     ("N, then earned exclusivity", [3, 4, 4, 4], R("unitN"), "Recommend: best rate, gates Boreal can audit"),
     ("Direct sales only", [4, 4, 1, 1], "No OEM rate", "Safe, but no OEM scale; integrator pilot is small"),
     ("Defer until certified", [4, 4, 0, 0], "None", "Little leverage now, and none gained by waiting")]
S.append({
    "id": "10", "role": "content", "section_id": "4", "status": "filled",
    "lead_message": {"text": "Starting nonexclusive and earning exclusivity through gates is the only option that keeps both the direct channel and the OEM",
                     "highlights": ["N, then earned exclusivity"], "clauses": 1},
    "message_type": "structure", "archetype": "harvey-ball-table",
    "rationale": "Five options on the board's criteria -> Harvey-ball table with a rate column and verdicts",
    "unit_line": "**Deal options against the board's tests**, team assessment; royalty after $80 support, $ per robot",
    "layout": {"variant": "full"},
    "body": {"kind": "table", "table_type": "harvey",
             "columns": ["Direct channel kept", "Certified first", "Volume verified", "OEM royalty", "$ per robot", "Verdict"],
             "rows": [{"label": l, "highlight": l.startswith("N,"),
                       "cells": [{"rating": r} for r in rs] + [{"point": p} if isinstance(p, dict) else {"text": p}] + [{"text": v}]}
                      for l, rs, p, v in H],
             "legend": "Team assessment from the briefing pack; full circle = fully meets the test"},
    "footnotes": ["The OEM will consider N and M but will not guarantee final pricing; the integration firm offers 1,200 robots with no minimum guarantee"]})

# 11 process gates
S.append({
    "id": "11", "role": "content", "section_id": "4", "status": "filled",
    "lead_message": {"text": "Four steps let the OEM earn exclusivity, and each closes with a gate Boreal can verify", "count_word": 4, "clauses": 1},
    "message_type": "structure", "archetype": "process-flow",
    "rationale": "Sequenced steps with gates -> process flow",
    "layout": {"variant": "full"},
    "body": {"kind": "process", "steps": [
        {"header": "Sign the nonexclusive pilot",
         "detail": ["12 months at $350 a robot, no advance", "Direct sales and the integrator pilot stay open",
                    "Audit right, escrow and contract carve-out from day one", "Extends on the same terms until the gates are met"],
         "footer": "Gate: protections signed, Q2 2027"},
        {"header": "Certify in OEM hardware",
         "detail": ["Start the $0.45M safety assessment now", "Reach 99.5% uptime with documented safe stops",
                    "Test the collision-heavy peak loads the lab skipped"],
         "emphasis": True, "footer": "Gate: certified, target Sept 2027"},
        {"header": "Prove volume",
         "detail": ["Two audited quarters above 8,787 robots a year", "The OEM's offer of 5,000 is too low",
                    "Measure direct loss with customer-level IDs", "Track support cost per robot against $80"],
         "footer": "Gate: audited volume, earliest Q1 2028"},
        {"header": "Grant limited exclusivity",
         "detail": ["New robots of this OEM in North America only", "Royalty floor and audit right stay in force",
                    "Automatic release if the model is retired", "Termination payment agreed up front"],
         "footer": "Board approval, earliest mid-2028"}]},
    "callout": {"target": "Certify in OEM hardware", "header": "Nothing irreversible before this", "detail": "The board's own condition for exclusivity"},
    "footnotes": ["Volume gate = ($0.9M team + 70% of $1.48M direct gross profit) ÷ $220 a robot; it falls to 6,104 robots if measured direct loss is 30%"]})

# 12 levers: signals
S.append({
    "id": "12", "role": "content", "section_id": "4", "status": "filled",
    "lead_message": {"text": "Four signals from the pilot would change this recommendation, and each has a threshold set in advance", "count_word": 4, "clauses": 1},
    "message_type": "argument", "archetype": "numbered-levers",
    "rationale": "Things that would change the answer, each with a threshold -> numbered levers",
    "unit_line": "**What would change the recommendation**, with the threshold for each signal",
    "body": {"kind": "levers", "headers": ["Signal and what it would change", "Threshold"], "items": [
        {"code": "1", "text": "Verified shipments: two audited quarters above the gate open limited exclusivity",
         "point": R("gate"), "metric": "robots a year: ($0.9M + 70% of $1.48M) ÷ $220"},
        {"code": "2", "text": "Measured direct loss: a low loss lowers the gate; a high loss keeps Boreal nonexclusive",
         "point": R("gate30"), "metric": "robots a year if measured loss is 30%"},
        {"code": "3", "text": "Support cost per device: above this, 2027 royalties stop covering the OEM team",
         "point": R("sup_thr"), "metric": "per robot, against $80 planned"},
        {"code": "4", "text": "Audit right: without one, no exclusivity at any self-reported volume",
         "point": R("m_thr"), "metric": "robots a year: the OEM's own, unaudited gate"}]},
    "so_what": "Decision today: reject exclusivity at signing and offer the OEM the pilot with pre-agreed gates to earn it",
    "so_what_style": "bar"})

# backup year table
def row(label, refs, total):
    return {"label": label, "cells": [{"point": R(r)} for r in refs] + [{"point": R(total)}]}


S += [{"id": "app", "role": "appendix_divider", "status": "filled"}, {
    "id": "b1", "role": "backup", "section_id": "1", "backup_of": "1", "status": "filled",
    "lead_message": {"prefix": "BACKUP:", "text": "Year by year, the advance is counted once and fixed costs leave 2027 negative in both cases", "clauses": 1},
    "message_type": "item", "archetype": "data-table",
    "unit_line": "**Option X economics by year**, $ thousands unless stated, partner plan and 65% stress case",
    "layout": {"variant": "full"},
    "body": {"kind": "table", "table_type": "data", "columns": ["2027", "2028", "2029", "2027–29"], "rows": [
        row("Robots shipped, plan", ["v27", "v28", "v29"], "vt"),
        row("Royalties earned at $300", ["r27_k", "r28_k", "r29_k"], "roy3_k"),
        row("Cash received, advance credited", ["adv_k", "cash28_k", "r29_k"], "cash3_k"),
        row("Support at $80 a robot", ["nsup27_k", "nsup28_k", "nsup29_k"], "nsup3_k"),
        {"label": "Dedicated OEM team", "cells": [{"point": R("neng_k")}] * 3 + [{"point": R("neng3_k")}]},
        {"label": "Safety assessment", "cells": [{"point": R("nass_k")}, {"text": "—"}, {"text": "—"}, {"point": R("nass_k")}]},
        dict(row("Net contribution, plan", ["net27_k", "c28_k", "c29_k"], "net3_k"), highlight=True),
        row("Royalties at 65% of plan", ["s27_k", "s28_k", "s29_k"], "sroy3_k"),
        row("Net contribution, 65% of plan", ["snet27_k", "sc28_k", "sc29_k"], "snet3_k")]},
    "footnotes": ["Before lost direct sales (p. 8); cash timing ignores the royalty reporting lag; 2027 volumes depend on certification by September 2027"]}]

S.append({"id": "end", "role": "end_page", "status": "filled"})

# ---------------- storyline ----------------
storyline = {
    "governing_thought": "Boreal should decline exclusivity at signing and offer a nonexclusive pilot through which the OEM can earn limited exclusivity",
    "exec_summary": [
        {"id": "1", "text": "The $2.0M is prepaid royalty, not new revenue; net of OEM costs, exclusivity earns $3.2M over three years at plan, $1.0M at 65%",
         "supports": ["1", "2", "3"], "sub_points": [
            {"text": "Booking the advance on top of royalties overstates the deal by 23%", "slide_id": "1"},
            {"text": "At 2027 plan volume, $40 of each $300 royalty is left after OEM costs", "slide_id": "2"}]},
        {"id": "2", "text": "Exclusivity bars new direct licensing; at 65% of volumes it loses money in 2028 once over 36% of direct profit is lost",
         "supports": ["4", "5"], "sub_points": [
            {"text": "$1.48M of 2028 direct gross profit is at stake, with no data on how much goes", "slide_id": "4"},
            {"text": "The growth case rests on five correlational cases and an unbooked forecast", "slide_id": "5"}]},
        {"id": "3", "text": "Exclusivity at signing breaks the board's own conditions, and the work is fundable without the advance",
         "supports": ["6", "7", "8"], "sub_points": [
            {"text": "Lab downtime ran at 2.4 times the OEM's limit, and the draft lacks six protections", "slide_id": "6"},
            {"text": "Without the advance, a year of OEM costs leaves $0.55M above the buffer", "slide_id": "8"}]},
        {"id": "4", "text": "Sign the nonexclusive pilot; grant limited exclusivity only after certification and audited volume",
         "supports": ["9", "10", "11", "12"], "sub_points": [
            {"text": "Pilot terms match exclusivity in 2028 even with a third fewer robots", "slide_id": "9"},
            {"text": "Shipments, direct loss, support cost or audit rights could change it", "slide_id": "12"}]}],
    "next_steps": [
        {"action": "Offer the OEM the 12-month pilot with pre-agreed gates to earn limited exclusivity; decline exclusivity at signing", "owner": "CEO and Head of Partnerships", "timing": "Board decision, April 2027"},
        {"action": "Commission the $0.45M third-party safety assessment and plan peak-load uptime tests", "owner": "Engineering", "timing": "Start May 2027; certify by Sept 2027"},
        {"action": "Draft audit right, source-code escrow, release, royalty floor and existing-contract carve-out", "owner": "Legal counsel", "timing": "Before signing, Q2 2027"},
        {"action": "Tag customers to measure direct-channel overlap; report full OEM contribution, not dashboard margin", "owner": "CFO and Sales", "timing": "From pilot start"},
        {"action": "Review certification, audited shipments and direct loss against the gates", "owner": "Board", "timing": "Q1–Q2 2028"}]}

audit = {
    "constraints": [
        {"item": "$2.6M liquidity buffer against $4.9M unrestricted cash", "reflected": True,
         "effect": "a first year of OEM costs uses about three-quarters of the $2.3M headroom; the title says the work is fundable, not that the advance is unnecessary for all purposes", "slide_ids": ["8"]},
        {"item": "$0.45M safety assessment before any large OEM deployment", "reflected": True, "effect": "in the three-year net and the liquidity bridge", "slide_ids": ["3", "8"]},
        {"item": "$80 support per robot and $0.9M a year of OEM-specific engineering", "reflected": True,
         "effect": "cut the $300 royalty to $40 a robot at 2027 volume and the three-year value to $3.2M", "slide_ids": ["2", "3"]},
        {"item": "Advance is credited against royalties and can be offset", "reflected": True, "effect": "counted once; offset risk named", "slide_ids": ["1", "8"]},
        {"item": "Exclusivity bars all new direct licensing in North America; the direct ARR recurs", "reflected": False,
         "effect": "only the 2028 cohort is counted, so the direct loss is understated; the slide says so", "slide_ids": ["4"]},
        {"item": "Board requires certification before irreversible exclusivity; existing contracts cannot be terminated", "reflected": True,
         "effect": "Option X as drafted fails; the recommended structure gates exclusivity on certification", "slide_ids": ["6", "7", "11"]},
        {"item": "2027 volumes depend on certification that has not started", "reflected": False,
         "effect": "plan figures use the partner's 2027 forecast; slides flag that 2027 shipments assume certification", "slide_ids": ["6", "b1"]}],
    "alternatives": [
        {"option": "Sign Option X now, with carve-outs, for the $2.0M cash", "verdict": "rejected",
         "why": "the advance is prepaid royalty, the program fits above the buffer without it, and the pilot's $350 terms match X in 2028 unless the OEM ships 35% fewer robots",
         "triage": "body", "slide_ids": ["1", "8", "9"]},
        {"option": "Option M as offered (exclusivity after certification and 5,000 robots annualized)", "verdict": "combined",
         "why": "the gate structure is adopted, but 5,000 robots does not cover the direct profit given up; the gate rises to about 8,800 and scope is limited to the OEM's own robots",
         "triage": "body", "slide_ids": ["10", "11", "12"]},
        {"option": "Defer any deal until certification, or continue direct only with the integration firm's pilot", "verdict": "rejected",
         "why": "gives up OEM volume and leverage; the 1,200-robot integrator pilot cannot carry the $0.9M team",
         "triage": "body", "slide_ids": ["10"]}],
    "failure_threshold": {"driver": "share of 2028 direct gross profit lost to exclusivity, combined with OEM volume",
                          "threshold": "at 65% of plan, exclusivity turns negative in 2028 above 36% lost; at plan, above 88%; the volume gate covering a 70% loss is about 8,800 robots",
                          "range": "three-year net before direct loss: $1.0M at 65% of plan, $3.2M at plan; no upside case in the pack",
                          "triage": "body", "slide_ids": ["3", "4", "11", "12"]},
    "consistency": {"headline": storyline["governing_thought"], "holds": True,
                    "fix": "after the audit: overlap treated as a proxy with a 100% contractual ceiling, volume gate raised from 5,000 to about 8,800, and the liquidity claim narrowed to 'fundable without the advance'"}}

spec = {
    "spec_version": "0.1", "mode": "deck_detailed",
    "meta": {"title": "An exclusive OEM license for Boreal's navigation software",
             "subtitle": "Should Boreal grant North American exclusivity in 2027? Board discussion document, April 2027",
             "company_name": "Boreal Autonomy", "audience": "Board of directors",
             "purpose": "Decide whether to grant North American exclusivity to an OEM in 2027",
             "date": "2026-11-20", "language": "en-US",
             "confidentiality": "Synthetic benchmark data; every number from the briefing pack", "theme": "navy"},
    "inputs": [{"id": "in-1", "kind": "pasted_research", "label": "Boreal Autonomy briefing pack (evidence/briefing-pack.md)", "content": PACK}],
    "storyline": storyline, "decision_audit": audit,
    "sections": [{"id": "1", "title": "What the deal is worth", "exec_item_id": "1", "tracker_label": "Economics"},
                 {"id": "2", "title": "What exclusivity gives up", "exec_item_id": "2", "tracker_label": "Direct channel"},
                 {"id": "3", "title": "Why not at signing", "exec_item_id": "3", "tracker_label": "Readiness"},
                 {"id": "4", "title": "How to structure the deal", "exec_item_id": "4", "tracker_label": "Recommendation"}],
    "slides": S, "data_points": DP,
    "sources": [{"id": "s1", "kind": "user_provided", "name": "Boreal Autonomy briefing pack", "input_id": "in-1"},
                {"id": "s0", "kind": "derived", "name": "Team analysis of the briefing pack"}]}
OUT.write_text(json.dumps(spec, indent=1, ensure_ascii=False))
print("wrote", OUT, len(S), "slides", len(DP), "data points")
for k in ("net3", "snet3", "thr", "thr_b", "left", "hshare", "vN", "vN_sh", "vN70", "gate", "gate30", "sup_thr", "dtr", "over", "be"):
    print(k, VAL[k])
