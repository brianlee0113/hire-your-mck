"""Build the storyline spec for the Pelican Packaging IC deck (compile, restyle of evidence/analysis.md)."""
import json, re, sys, ast, operator
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "deliverable" / "pelican-capacity.json"

DPS = {}
ORDER = []


def _ev(expr):
    e = expr
    env = {}
    for k, i in enumerate(sorted(DPS, key=len, reverse=True)):
        e2 = re.sub(rf"(?<![\w.]){re.escape(i)}(?![\w-])", f"_v{k}", e)
        if e2 != e:
            env[f"_v{k}"] = DPS[i]["value"]; e = e2
    ops = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.Div: operator.truediv}
    def ev(n):
        if isinstance(n, ast.Expression): return ev(n.body)
        if isinstance(n, ast.BinOp): return ops[type(n.op)](ev(n.left), ev(n.right))
        if isinstance(n, ast.Constant): return n.value
        if isinstance(n, ast.Name): return env[n.id]
        raise ValueError(expr)
    return ev(ast.parse(e, mode="eval"))


def P(id_, label, value, unit, excerpt=None, locator=None, src="s1", **kw):
    d = {"id": id_, "slide_id": "es", "label": label, "value": value, "unit": unit, "source_id": src}
    if excerpt: d["excerpt"] = excerpt
    if locator: d["locator"] = locator
    d.update(kw)
    DPS[id_] = d; ORDER.append(id_)
    return id_


def D(id_, label, unit, calc, formula, value=None, digits=4, **kw):
    """Derived number: value = calc unless the value shown on the slide is given (kept as the analysis shows it)."""
    got = _ev(calc)
    v = round(got, digits) if value is None else value
    ids = [i for i in sorted(DPS, key=len, reverse=True) if re.search(rf"(?<![\w.]){re.escape(i)}(?![\w-])", calc)]
    seen = []
    for tok in re.findall(r"[A-Za-z_][\w]*", calc):
        if tok in DPS and tok not in seen: seen.append(tok)
    d = {"id": id_, "slide_id": "es", "label": label, "value": v, "unit": unit, "source_id": "s3",
         "derived_from": seen, "formula": formula, "calc": calc}
    d.update(kw)
    DPS[id_] = d; ORDER.append(id_)
    return id_


def r(i):
    assert i in DPS, i
    return {"data_ref": i}


PK = "evidence/briefing-pack.md"
AN = "evidence/analysis.md"

# ---------------------------------------------------------------- briefing pack inputs (s1)
P("cash", "Available unrestricted cash", 11.0, "$M", "Available unrestricted cash is $11.0M", f"{PK} §2 Binding constraints", period="2027")
P("rd", "Already-approved validation and R&D spending, 2027", 2.2, "$M", "Already-approved validation and R&D spending in 2027 is $2.2M", f"{PK} §2", period="2027")
P("floor", "Debt covenant minimum cash balance", 7.0, "$M", "A debt covenant requires a $7.0M minimum cash balance after commitments; no committed borrowing facility is available", f"{PK} §2")
P("capex", "New line equipment and installation", 4.8, "$M", "The new line requires $4.8M of equipment and installation", f"{PK} §2")
P("lead", "New line lead time after order", 12, "months", locator=f"{PK} §2: 'has a twelve-month lead time after order'")
P("fixed", "New line fixed maintenance and quality staffing", 0.55, "$M", "adds $0.55M/year of fixed maintenance and quality staffing from commissioning", f"{PK} §2", period="per year from commissioning")
P("dep", "Installation slot deposit", 0.6, "$M", "A $0.60M slot deposit is credited toward the $4.8M if the machine is ordered; if cancelled it is forfeited", f"{PK} §1–2")
P("fill", "Required monthly fill rate", 0.98, "%", "Medical-device customers require a 98% monthly fill rate", f"{PK} §2")
P("mold_cap", "Contract molder ceiling, incremental accepted units a year", 2.5, "M units", "The contract molder can provide up to 2.5M incremental accepted units per year, with five months' lead time", f"{PK} §2")
P("mold_lead", "Contract molder notice", 5, "months", locator=f"{PK} §2: 'with five months' lead time'")
P("spec_share", "Specialty product share of 2029 forecast units", 0.20, "%", "one upcoming specialty product, which accounts for 20% of 2029 forecast units", f"{PK} §2", period="2029")
for y, f, s, o in (("2027", 8.3, 7.8, 0.0), ("2028", 9.6, 8.5, 0.6), ("2029", 11.2, 9.4, 2.2), ("2030", 12.4, 9.8, 3.4)):
    P(f"f{y}", f"Forecast good units, {y}", f, "M units", f'row "{y}"; column "Forecast good units (M)" = "{f}"', f"{PK} §3 table", period=y)
    P(f"s{y}", f"Signed minimum units, {y}", s, "M units", f'row "{y}"; column "Signed minimum (M)" = "{s}"', f"{PK} §3 table", period=y)
    P(f"ovp{y[2:]}", f"Overflow above 9.0M practical capacity (pack, before scrap allowance), {y}", o, "M units",
      f'row "{y}"; column "Overflow above 9.0M practical capacity" = "{o:.1f}M"', f"{PK} §3 table", period=y)
P("nameplate", "Existing line nameplate annual capacity", 10.0, "M units", "The existing line has 10.0M units of nameplate annual capacity", f"{PK} §3")
P("practical", "Existing line practical accepted capacity", 9.0, "M units", "reduce practical accepted capacity to 9.0M units", f"{PK} §3",
  definition="net of maintenance, validated changeovers and quality holds")
P("ops_util", "Operations-reported 2027 utilization (nameplate basis)", 0.83, "%", "A slide from Operations reports 83% utilization for 2027 (8.3M divided by 10.0M)", f"{PK} §3", period="2027")
P("ops_free", "Operations-reported 'free capacity', 2027", 0.17, "%", 'concludes there is "17% free capacity."', f"{PK} §3", period="2027")
P("scrap", "Extra scrap on specialty containers compared with standard mix", 0.04, "%", "Short-run tests on the specialty containers produce 4% more scrap than the standard mix", f"{PK} §3")
P("prem", "Contract molder premium per accepted unit", 0.12, "$", "+$0.12 per accepted unit vs internal variable cost", f"{PK} §4 table, Contract-mold overflow row")
P("contrib", "Contribution retained per good unit served internally", 0.45, "$", "The incremental contribution retained by molding a good unit internally rather than refusing an order is about $0.45 per unit", f"{PK} §4")
P("growth23", "Sales VP claim: faster growth of early capacity builders", 0.23, "%", '"Manufacturers that build capacity earlier grew 23% faster last year."', f"{PK} §5")
P("val_extra", "Possible extra specialty validation time", 2, "months", locator=f"{PK} §7: 'specialty validation may take two additional months'")

# ---------------------------------------------------------------- the analysis's own assumptions (s2, untraceable)
P("thr", "Proposed demand trigger: signed 2029 or 2030 minimums", 10.5, "M units", "Signed 2029 or 2030 minimums of 10.5M units or more", f"{AN} slides 2, 14; Appendix B: '10.5M threshold and $0.5M buffer are our proposals'", src="s2")
P("buffer", "Proposed cash buffer above the covenant floor", 0.5, "$M", "the $7.0M floor plus a $0.5M buffer", f"{AN} slide 14; Appendix B", src="s2")
P("rebid_s25", "Illustrative share of base allocation lost in a rebid (low case)", 0.25, "%", "+ rebid loses 25% of base allocation", f"{AN} slide 11; 'Rebid shares are illustrative'", src="s2")
P("rebid_s50", "Illustrative share of base allocation lost in a rebid (high case)", 0.5, "%", "+ rebid loses 50% of base allocation", f"{AN} slide 11; 'Rebid shares are illustrative'", src="s2")
P("spec28", "Assumed specialty share of 2028 units", 0.0, "%", "0% in 2028; 20% in 2030 (same as 2029)", f"{AN} Appendix B, row 'Specialty share in 2028 and 2030'", src="s2", period="2028")
P("spec30", "Assumed specialty share of 2030 units", 0.20, "%", "0% in 2028; 20% in 2030 (same as 2029)", f"{AN} Appendix B, row 'Specialty share in 2028 and 2030'", src="s2", period="2030")

# ---------------------------------------------------------------- derived (s3)
D("cash_avail", "Cash available above approved 2027 commitments", "$M", "cash - rd", "$11.0M − $2.2M")
D("headroom", "Cash headroom above the floor before any path", "$M", "cash_avail - floor", "$8.8M − $7.0M")
D("cash_order", "Cash after 2027 commitments if the line is ordered now", "$M", "cash_avail - capex", "$8.8M − $4.8M")
D("gap_order", "Order now: cash against the $7.0M floor", "$M", "cash_order - floor", "$4.0M − $7.0M")
D("cash_slot", "Cash after 2027 commitments if only the slot is reserved", "$M", "cash_avail - dep", "$8.8M − $0.6M")
D("head_slot", "Reserve slot: cash headroom above the floor", "$M", "cash_slot - floor", "$8.2M − $7.0M")
D("dep_share", "Share of the $1.8M headroom used by the deposit", "%", "dep / headroom", "$0.6M ÷ $1.8M")
D("balance", "Balance due on ordering after the credited deposit", "$M", "capex - dep", "$4.8M − $0.6M (deposit credited, not double-counted)")
D("cash_slot_order", "Cash after paying the $4.2M balance with no new funding", "$M", "cash_slot - balance", "$8.2M − $4.2M")
D("new_money", "New funding needed to order without breaching the floor", "$M", "floor - cash_slot_order", "$7.0M − $4.0M")
for y in ("2027", "2028", "2029", "2030"):
    D(f"un{y[2:]}", f"Ops KPI utilization, pack demand ÷ 10.0M nameplate, {y}", "%", f"f{y} / nameplate", f"{y} forecast ÷ 10.0M", digits=2)
    D(f"up{y[2:]}", f"Utilization on accepted units, pack demand ÷ 9.0M practical, {y}", "%", f"f{y} / practical", f"{y} forecast ÷ 9.0M", digits=2)
D("slack27", "Practical slack in 2027", "M units", "practical - f2027", "9.0M − 8.3M")
D("slack_share", "2027 practical slack as share of practical capacity", "%", "slack27 / practical", "0.7M ÷ 9.0M", digits=3)
D("np_slack", "2027 slack implied by the nameplate view", "M units", "nameplate - f2027", "10.0M − 8.3M")
D("sp29", "Specialty units, 2029", "M units", "spec_share * f2029", "20% × 11.2M")
D("scr29", "Specialty scrap allowance, 2029", "M units", "sp29 * scrap", "2.24M × 4%", value=0.09)
D("sp30", "Specialty units, 2030 (share assumed equal to 2029)", "M units", "spec30 * f2030", "20% × 12.4M")
D("scr30", "Specialty scrap allowance, 2030", "M units", "sp30 * scrap", "2.48M × 4%", value=0.10, estimate=True,
  assumptions=["Specialty share of 2030 units stays at 2029's 20% (the pack gives 2029 only)", "Specialty runs keep 4% more scrap than the standard mix"])
D("ov28", "Overflow above internal capacity at pack demand, 2028", "M units", "f2028 - practical + f2028 * spec28 * scrap", "9.6M − 9.0M; no specialty volume assumed in 2028",
  assumptions=["No specialty volume in 2028 (analysis assumption)"])
D("ov29", "Forecast overflow above internal capacity incl. specialty scrap, 2029", "M units", "f2029 - practical + scr29", "11.2M − 9.0M + 0.09M scrap", value=2.29)
D("ov30", "Forecast overflow above internal capacity incl. specialty scrap, 2030", "M units", "f2030 - practical + scr30", "12.4M − 9.0M + 0.10M scrap", value=3.5,
  assumptions=["2030 scrap allowance assumes the specialty share stays at 20%"])
D("ov30_short", "2030 forecast overflow beyond the molder ceiling", "M units", "ov30 - mold_cap", "3.5M − 2.5M", value=1.0)
P("zero_ov", "Overflow where demand stays below 9.0M practical capacity", 0.0, "M units", src="s3",
  derived_from=["f2027", "s2027", "s2028", "practical"],
  formula="Demand at or below 9.0M practical capacity leaves no overflow: forecast 2027 (8.3M), signed 2027–28 (7.8M, 8.5M), slip-case 2027–28 (8.3M moved to 2028)")
D("slip29", "Overflow, one-year slip case, 2029", "M units", "ov28 + f2028 * spec_share * scrap", "2028 forecast moved to 2029: 9.6M − 9.0M + 20% × 9.6M × 4%",
  assumptions=["Forecast demand arrives one year later than planned (analysis assumption)", "2029 specialty share of 20% applies to the delayed volume"])
D("slip30", "Overflow, one-year slip case, 2030", "M units", "ov29", "2029 forecast overflow moved to 2030",
  assumptions=["Forecast demand arrives one year later than planned (analysis assumption)"])
D("sov29", "Overflow at signed minimums only, 2029", "M units", "s2029 - practical + s2029 * spec_share * scrap", "9.4M − 9.0M + 20% × 9.4M × 4%")
D("sov30", "Overflow at signed minimums only, 2030", "M units", "s2030 - practical + s2030 * spec30 * scrap", "9.8M − 9.0M + 20% × 9.8M × 4%",
  assumptions=["2030 specialty share assumed at 20%"])
D("unsigned30", "2030 forecast volume above signed minimums", "M units", "f2030 - s2030", "12.4M − 9.8M")
D("unsigned_share", "Share of 2030 pack demand that is unsigned", "%", "unsigned30 / f2030", "2.6M ÷ 12.4M", digits=2)
# monthly view (slide 6), stored as the analysis shows them
D("dem28", "Average monthly demand, pack outlook, 2028", "M units", "f2028 / 12", "9.6M ÷ 12", value=0.80)
D("dem29", "Average monthly demand, pack outlook, 2029", "M units", "f2029 / 12", "11.2M ÷ 12", value=0.93)
D("dem30", "Average monthly demand, pack outlook, 2030", "M units", "f2030 / 12", "12.4M ÷ 12", value=1.03)
D("int28", "Internal practical monthly supply, 2028", "M units", "practical / 12", "9.0M ÷ 12", value=0.75)
D("int29", "Internal monthly supply after specialty scrap, 2029", "M units", "(practical - scr29) / 12", "(9.0M − 0.09M) ÷ 12", value=0.74)
D("int30", "Internal monthly supply after specialty scrap, 2030", "M units", "(practical - scr30) / 12", "(9.0M − 0.10M) ÷ 12", value=0.74)
D("mold_m", "Contract molder maximum monthly supply", "M units", "mold_cap / 12", "2.5M ÷ 12", value=0.21)
D("sup28", "Maximum monthly supply, internal + molder, 2028", "M units", "int28 + mold_m", "0.75 + 0.21", value=0.96)
D("sup29", "Maximum monthly supply, internal + molder, 2029", "M units", "int29 + mold_m", "0.74 + 0.21", value=0.95)
D("sup30", "Maximum monthly supply, internal + molder, 2030", "M units", "int30 + mold_m", "0.74 + 0.21", value=0.95)
D("pct28", "Average 2028 demand as share of maximum monthly supply", "%", "f2028 / (practical + mold_cap)", "9.6M ÷ (9.0M + 2.5M)", value=0.83)
D("pct29", "Average 2029 demand as share of maximum monthly supply", "%", "f2029 / (practical - scr29 + mold_cap)", "11.2M ÷ (9.0M − 0.09M + 2.5M)", value=0.98)
D("pct30", "Average 2030 demand as share of maximum monthly supply", "%", "f2030 / (practical - scr30 + mold_cap)", "12.4M ÷ (9.0M − 0.10M + 2.5M)", value=1.09)
D("peak28", "How far a 2028 peak month can exceed the average", "%", "(practical + mold_cap) / f2028 - 1", "11.5M ÷ 9.6M − 1", value=0.20)
D("peak29", "How far a 2029 peak month can exceed the average", "%", "(practical - scr29 + mold_cap) / f2029 - 1", "11.41M ÷ 11.2M − 1", value=0.02)
D("base_contrib", "Annual contribution of the base business exposed to a rebid (proxy)", "$M", "practical * contrib", "9.0M units × $0.45")
D("rebid25_loss", "Annual contribution lost if a rebid takes a quarter of the base", "$M", "base_contrib * rebid_s25", "$4.05M × 25% (illustrative share)")
D("short30_loss", "Contribution lost on the 2030 shortfall beyond the molder ceiling", "$M", "ov30_short * contrib", "1.0M units × $0.45", value=0.45)
# molder economics (slide 9)
D("p28", "Molder premium on 2028 overflow", "$M", "ov28 * prem", "0.6M × $0.12")
D("p29", "Molder premium on 2029 overflow", "$M", "ov29 * prem", "2.29M × $0.12")
D("p30", "Molder premium at the 2030 ceiling", "$M", "mold_cap * prem", "2.5M × $0.12")
D("prem_2829", "Molder premiums, 2028–29", "$M", "p28 + p29", "$0.07M + $0.27M")
D("keep_unit", "Contribution kept per unit served through the molder", "$", "contrib - prem", "$0.45 − $0.12")
D("sh28", "2028 overflow as share of the molder ceiling", "%", "ov28 / mold_cap", "0.6M ÷ 2.5M", digits=2)
D("sh29", "2029 overflow as share of the molder ceiling", "%", "ov29 / mold_cap", "2.29M ÷ 2.5M", digits=2)
D("sh30", "2030 overflow as share of the molder ceiling", "%", "ov30 / mold_cap", "3.5M ÷ 2.5M", digits=2)
D("slack29", "Molder slack left in 2029", "M units", "mold_cap - ov29", "2.5M − 2.29M")
# line against molder (slide 10)
D("mold_net", "2030 contribution on overflow, molder only", "$M", "mold_cap * keep_unit", "2.5M × ($0.45 − $0.12)", value=0.83)
D("line_contrib", "2030 contribution on overflow, new line", "$M", "ov30 * contrib", "3.5M × $0.45", value=1.58)
D("fixed_neg", "Line fixed cost, 2030", "$M", "0 - fixed", "−$0.55M")
D("line_net", "2030 net on overflow, new line, before capex", "$M", "mold_net + p30 + short30_loss - fixed", "$0.83M + $0.30M + $0.45M − $0.55M (= 3.5M × $0.45 − $0.55M)", value=1.03)
D("adv", "2030 advantage of the line over the molder, before capex", "$M", "line_net - mold_net", "$1.03M − $0.83M", value=0.20)
D("be", "Overflow volume at which the line's fixed cost equals the molder premium", "M units", "fixed / prem", "$0.55M ÷ $0.12 per unit", value=4.6)
# slot as an option (slide 11)
D("loss25", "Loss avoided with one year of late 2030 capacity, rebid takes 25% of base", "$M", "short30_loss + base_contrib * rebid_s25", "$0.45M + 9.0M × $0.45 × 25%", value=1.46)
D("loss50", "Loss avoided with one year of late 2030 capacity, rebid takes 50% of base", "$M", "short30_loss + base_contrib * rebid_s50", "$0.45M + 9.0M × $0.45 × 50%", value=2.48)
D("be_sh", "Break-even probability, shortfall only", "%", "dep / short30_loss", "$0.6M ÷ $0.45M", digits=2)
D("be25", "Break-even probability, rebid takes 25% of base", "%", "dep / loss25", "$0.6M ÷ $1.46M", digits=2)
D("be50", "Break-even probability, rebid takes 50% of base", "%", "dep / loss50", "$0.6M ÷ $2.48M", digits=2)
D("sig_prem30", "2030 molder premium in the signed-minimum case", "$M", "sov30 * prem", "0.9M × $0.12", value=0.11)
D("dep_years", "Years of signed-case 2030 molder premium equal to the deposit", "years", "dep / sig_prem30", "$0.6M ÷ $0.11M", value=5.5)
# path costs (slide 8)
D("cost_order", "Order now: 2027–30 incremental cost at pack demand", "$M", "capex + fixed * 3", "$4.8M + 3 years × $0.55M (line from about January 2028)",
  assumptions=["Line commissioned about January 2028, so fixed cost runs three years to 2030"])
D("p29h", "Molder premium for the first half of 2029", "$M", "p29 / 2", "$0.27M ÷ 2", estimate=True,
  assumptions=["Line ordered Q1 2028 is producing by about mid-2029, so the molder covers only H1 2029"])
D("fix15", "Line fixed cost, mid-2029 to 2030", "$M", "fixed * 1.5", "1.5 years × $0.55M", estimate=True,
  assumptions=["Line commissioned about mid-2029 after a Q1 2028 order"])
D("cost_rec", "Reserve slot + molder bridge: 2027–30 incremental cost at forecast, if ordered Q1 2028", "$M", "capex + p28 + p29h + fix15",
  "$4.8M + $0.07M + $0.14M + $0.83M (deposit credited inside the $4.8M)", value=5.8, estimate=True,
  assumptions=["Line ordered Q1 2028 once triggers are met, producing about mid-2029", "Molder covers 2028 and H1 2029 overflow at $0.12 per unit",
               "The $0.6M deposit is credited toward the $4.8M and not counted twice", "Excludes operating cash flow and value after 2030"])
D("save_rec", "Cost saved by reserving and bridging rather than ordering now", "$M", "cost_order - capex - p28 - p29h - fix15", "$6.45M − $5.83M (unrounded recommended-path cost)", value=0.62)
D("mold_only_prem", "Molder-only premiums, 2028–30", "$M", "p28 + p29 + p30", "$0.07M + $0.27M + $0.30M")
D("nothing_lost", "Do nothing: lost contribution 2028–30", "$M", "(ov28 + ov29 + ov30) * contrib", "(0.6M + 2.29M + 3.5M) × $0.45")
# triggers (slide 14)
D("thr_ov", "Overflow implied by signed minimums of 10.5M", "M units", "thr - practical + thr * spec_share * scrap", "10.5M − 9.0M + 20% × 10.5M × 4%")
D("unsigned_rem", "2030 forecast units above the 10.5M trigger", "M units", "f2030 - thr", "12.4M − 10.5M")
D("cash_target", "Minimum cash after the balance payment under the funding trigger", "$M", "floor + buffer", "$7.0M floor + $0.5M buffer")
D("fund_need", "Committed funding required before releasing the balance", "$M", "cash_target - cash_slot_order", "$7.5M − ($8.2M − $4.2M)")
D("int_after", "Internal capacity after the 2030 specialty scrap allowance", "M units", "practical - scr30", "9.0M − 0.10M", value=8.9)
D("coverable", "Demand coverable without the line (internal after scrap + molder)", "M units", "int_after + mold_cap", "8.9M + 2.5M")
# 2028 coverage (slide 13)
D("cover_total", "2028 cover from molder ceiling plus 2027 safety stock", "M units", "mold_cap + slack27", "2.5M + 0.7M")
D("cover_mult", "2028 cover as a multiple of the 0.6M overflow", "x", "cover_total / ov28", "3.2M ÷ 0.6M", digits=1)
# downside cases (slide 16)
D("slip_prem", "Molder premiums 2029–30, one-year slip case", "$M", "(slip29 + slip30) * prem", "(0.68M + 2.29M) × $0.12")
D("sig_prem", "Molder premiums 2029–30, signed-minimum case", "$M", "(sov29 + sov30) * prem", "(0.48M + 0.88M) × $0.12")
D("sig_share30", "2030 signed-case overflow as share of the molder ceiling", "%", "sov30 / mold_cap", "0.9M ÷ 2.5M (analysis rounds overflow to 0.9M)", value=0.36)
D("low_signed", "Lowest cash, signed-minimum case", "$M", "cash_avail - dep - sig_prem", "$8.8M − $0.6M − $0.16M")
D("low_slip", "Lowest cash, one-year slip case", "$M", "cash_avail - dep - slip_prem", "$8.8M − $0.6M − $0.36M")
D("low_nofund", "Lowest cash, forecast demand with no funding", "$M", "cash_avail - dep - mold_only_prem", "$8.8M − $0.6M − $0.65M")
D("hd_signed", "Signed-minimum case: lowest cash above the floor", "$M", "low_signed - floor", "$8.0M − $7.0M")
D("hd_slip", "Slip case: lowest cash above the floor", "$M", "low_slip - floor", "$7.8M − $7.0M")
D("hd_nofund", "No-funding case: lowest cash above the floor", "$M", "low_nofund - floor", "$7.6M − $7.0M")


D("fix_delay", "How much later line fixed costs start on the recommended path", "months", "(3 - 1.5) * 12", "3 years of fixed cost (order now) against 1.5 years (order Q1 2028) = 18 months")
D("line14", "Line timeline allowing extra specialty validation", "months", "lead + val_extra", "12 months + 2 months")
P("cash13", "Rolling cash forecast horizon proposed", 13, "weeks", "13-week cash forecast", f"{AN} slides 12, 17, 18", src="s2")
D("scr29k", "Specialty scrap allowance, 2029, thousand units", "thousand units", "scr29 * 1000", "0.09M units × 1,000")
