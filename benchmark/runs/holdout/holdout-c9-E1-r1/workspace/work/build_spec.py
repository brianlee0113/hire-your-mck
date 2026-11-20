"""Builds the storyline spec for the Pelican Packaging capacity deck from the briefing pack."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
DP = []


def src(id_, label, value, unit, excerpt, locator, period="", used_in="", slide="1", **kw):
    DP.append(dict(id=id_, slide_id=slide, label=label, value=value, unit=unit, period=period,
                   source_id="s1", excerpt=excerpt, locator=locator, used_in=used_in, **kw))


def der(id_, label, value, unit, calc, derived_from, formula, period="", used_in="", slide="1",
        estimate=False, assumptions=None, **kw):
    d = dict(id=id_, slide_id=slide, label=label, value=value, unit=unit, period=period, source_id="s2",
             derived_from=derived_from, formula=formula, calc=calc, used_in=used_in, **kw)
    if estimate:
        d["estimate"] = True
        d["assumptions"] = assumptions
    DP.append(d)


def P(ref):
    return {"data_ref": ref}


def tbl(year, col, val):
    return f'Row "{year}"; column "{col}" = "{val}"'


# ---------------------------------------------------------------- sourced numbers (briefing pack)
src("cash", "Available unrestricted cash", 11.0, "$M", "Available unrestricted cash is $11.0M", "Section 2, bullet 1", "January 2027", "waterfall start", slide="3")
src("rd", "Already-approved validation and R&D spending", 2.2, "$M", "Already-approved validation and R&D spending in 2027 is $2.2M", "Section 2, bullet 1", "2027", "waterfall step input", slide="3")
src("floor", "Covenant minimum cash balance after commitments", 7.0, "$M", "A debt covenant requires a $7.0M minimum cash balance after commitments; no committed borrowing facility is available", "Section 2, bullet 1", "2027", "covenant floor", slide="3")
src("capex", "Second line, equipment and installation", 4.8, "$M", "The new line requires $4.8M of equipment and installation, has a twelve-month lead time after order", "Section 2, bullet 2", "2027 commitment", "waterfall step input, gate", slide="3")
src("fixed", "Fixed maintenance and quality staffing of the second line", 0.55, "$M", "adds $0.55M/year of fixed maintenance and quality staffing from commissioning", "Section 2, bullet 2", "per year from commissioning", "cost comparison", slide="5")
src("dep", "Installation-slot deposit", 0.6, "$M", "A $0.60M slot deposit is credited toward the $4.8M if the machine is ordered; if cancelled it is forfeited", "Section 2, bullet 2", "March 2027", "equation, table", slide="10")
src("fill", "Monthly fill rate customers require", 0.98, "%", "Medical-device customers require a 98% monthly fill rate", "Section 2, bullet 3", "monthly", "KPI tile", slide="8")
src("mcap", "Contract-molder incremental capacity", 2.5, "M units", "The contract molder can provide up to 2.5M incremental accepted units per year, with five months' lead time", "Section 2, bullet 4", "per year", "benchmark line", slide="7")
src("spsh", "Specialty product share of 2029 forecast units", 0.2, "%", "one upcoming specialty product, which accounts for 20% of 2029 forecast units", "Section 2, bullet 4", "2029", "specialty units input", slide="8")
src("name", "Nameplate annual capacity of the existing line", 10.0, "M units", "The existing line has 10.0M units of nameplate annual capacity", "Section 3, paragraph after table", "per year", "KPI text", slide="2")
src("prac", "Practical accepted capacity of the existing line", 9.0, "M units", "reduce practical accepted capacity to 9.0M units", "Section 3, paragraph after table", "per year", "KPI input, benchmark line", slide="2")
src("ops83", "Operations-reported utilization (units on nameplate)", 0.83, "%", "A slide from Operations reports 83% utilization for 2027 (8.3M divided by 10.0M)", "Section 3, paragraph after table", "2027", "KPI tile 1, title", slide="2")
src("free", "Free capacity claimed by Operations", 0.17, "%", 'concludes there is "17% free capacity."', "Section 3, paragraph after table", "2027", "KPI relation", slide="2")
src("scrap", "Extra scrap on specialty containers", 0.04, "%", "Short-run tests on the specialty containers produce 4% more scrap than the standard mix", "Section 3, paragraph after table", "short-run tests", "KPI driver", slide="8")
src("prem", "Contract-molder premium per accepted unit", 0.12, "$", "+$0.12 per accepted unit vs internal variable cost", "Section 4 table, row Contract-mold overflow", "", "cost comparison input", slide="5")
src("contrib", "Contribution per good unit served instead of refused", 0.45, "$", "The incremental contribution retained by molding a good unit internally rather than refusing an order is about $0.45 per unit", "Section 4, paragraph after table", "", "cost comparison input", slide="5")
src("g23", "Faster growth of manufacturers that built capacity earlier", 0.23, "%", '"Manufacturers that build capacity earlier grew 23% faster last year."', "Section 5, paragraph 1", "last year", "title", slide="6")

COLF, COLS, COLO = "Forecast good units (M)", "Signed minimum (M)", "Overflow above 9.0M practical capacity"
for y, f, s, o in (("2027", 8.3, 7.8, 0.0), ("2028", 9.6, 8.5, 0.6), ("2029", 11.2, 9.4, 2.2), ("2030", 12.4, 9.8, 3.4)):
    yy = y[2:]
    src(f"f{yy}", f"Forecast good units, {y}", f, "M units", tbl(y, COLF, f), f"Section 3 table, row {y}", y, "input", slide="2")
    src(f"s{yy}", f"Signed minimum units, {y}", s, "M units", tbl(y, COLS, s), f"Section 3 table, row {y}", y, "stacked column, signed minimum", slide="2")
    src(f"o{yy}", f"Forecast overflow above practical capacity, {y}", o, "M units", tbl(y, COLO, f"{o}M"), f"Section 3 table, row {y}", y, "column", slide="7")

# ---------------------------------------------------------------- derived numbers
# Section 1
der("u27", "2027 demand outlook as a share of practical accepted capacity", 0.9222, "%", "f27 / prac", ["f27", "prac"], "8.3M ÷ 9.0M = 92%", "2027", "KPI tile 2, title", slide="2")
der("head27", "Practical headroom left in 2027", 0.7, "M units", "prac - f27", ["prac", "f27"], "9.0M − 8.3M = 0.7M", "2027", "KPI tile 3", slide="2")
der("freeu", "Units of free capacity implied by Operations' nameplate metric", 1.7, "M units", "name - f27", ["name", "f27"], "10.0M − 8.3M = 1.7M", "2027", "KPI relation", slide="2")
der("lossnp", "Nameplate units lost to maintenance, changeovers and quality holds", 1.0, "M units", "name - prac", ["name", "prac"], "10.0M − 9.0M = 1.0M", "per year", "KPI driver", slide="2")
for y, yy in (("2027", "27"), ("2028", "28"), ("2029", "29"), ("2030", "30")):
    f = {"27": 8.3, "28": 9.6, "29": 11.2, "30": 12.4}[yy]; s = {"27": 7.8, "28": 8.5, "29": 9.4, "30": 9.8}[yy]
    der(f"a{yy}", f"Forecast units above signed minimums (nonbinding), {y}", round(f - s, 2), "M units", f"f{yy} - s{yy}", [f"f{yy}", f"s{yy}"],
        f"{f}M − {s}M = {round(f - s, 1)}M", y, "stacked column, nonbinding segment", slide="3")
der("nb30", "Share of the 2030 demand outlook above signed minimums", 0.2097, "%", "a30 / f30", ["a30", "f30"], "2.6M ÷ 12.4M = 21%", "2030", "sidebar row", slide="3")
der("sp28", "Practical capacity left above 2028 signed minimums", 0.5, "M units", "prac - s28", ["prac", "s28"], "9.0M − 8.5M = 0.5M", "2028", "sidebar text", slide="3")
der("so29", "Overflow above practical capacity on signed minimums, 2029", 0.4, "M units", "s29 - prac", ["s29", "prac"], "9.4M − 9.0M = 0.4M", "2029", "table", slide="3")
der("so30", "Overflow above practical capacity on signed minimums, 2030", 0.8, "M units", "s30 - prac", ["s30", "prac"], "9.8M − 9.0M = 0.8M", "2030", "table", slide="3")

# Section 2: cash
der("rdn", "Approved 2027 R&D and validation (outflow)", -2.2, "$M", "0 - rd", ["rd"], "−$2.2M", "2027", "waterfall step", slide="4")
der("capn", "Second line ordered in full (outflow, deposit included)", -4.8, "$M", "0 - capex", ["capex"], "−$4.8M (the $0.60M deposit is part of it, not added again)", "2027", "waterfall step", slide="4")
der("avail", "Unrestricted cash after approved 2027 R&D and validation", 8.8, "$M", "cash - rd", ["cash", "rd"], "$11.0M − $2.2M = $8.8M", "2027", "harvey table, equation", slide="4")
der("cord", "Cash after ordering the whole line in January 2027", 4.0, "$M", "cash - rd - capex", ["cash", "rd", "capex"], "$11.0M − $2.2M − $4.8M = $4.0M", "2027", "waterfall end", slide="4")
der("short", "Cash compared with the covenant minimum after a full order", -3.0, "$M", "cord - floor", ["cord", "floor"], "$4.0M − $7.0M = −$3.0M", "2027", "sidebar big number, title", slide="4")
# Section 2: cost
der("prem28", "Contract-molder premium on 2028 overflow", 0.072, "$M", "prem * o28", ["prem", "o28"], "$0.12 × 0.6M = $0.07M", "2028", "column", slide="5")
der("prem29", "Contract-molder premium on 2029 overflow", 0.264, "$M", "prem * o29", ["prem", "o29"], "$0.12 × 2.2M = $0.26M", "2029", "column", slide="5")
der("capcost", "Contract-molder premium at its full 2.5M-unit cap", 0.3, "$M", "prem * mcap", ["prem", "mcap"], "$0.12 × 2.5M = $0.30M", "per year", "break-even input", slide="5")
der("gap30", "2030 overflow beyond the contract-molder cap", 0.9, "M units", "o30 - mcap", ["o30", "mcap"], "3.4M − 2.5M = 0.9M", "2030", "text", slide="5")
der("lost30", "Contribution lost on 2030 overflow the molder cannot take", 0.405, "$M", "gap30 * contrib", ["gap30", "contrib"], "0.9M × $0.45 = $0.41M", "2030", "input", slide="5")
der("mold30", "Contract-molder path cost in 2030: premium at cap plus contribution lost", 0.705, "$M", "capcost + lost30", ["capcost", "lost30"], "$0.30M + $0.41M = $0.71M", "2030", "column", slide="5")
der("rem", "Line fixed cost not covered by the molder premium at cap", 0.25, "$M", "fixed - capcost", ["fixed", "capcost"], "$0.55M − $0.30M = $0.25M", "per year", "basis caption", slide="5")
BE_ASSUME = ["The molder premium of $0.12 applies to every unit up to its 2.5M-unit cap (briefing pack)",
             "Each overflow unit beyond the cap that nobody makes loses about $0.45 of contribution (briefing pack)",
             "The second line costs $0.55M a year in fixed maintenance and quality staffing; the $4.8M capex, financing and any salvage value are left out",
             "Variable cost of the new line equals internal variable cost on the existing line"]
der("extra", "Overflow units beyond the molder cap at which lost contribution equals the remaining line fixed cost", 0.5556, "M units",
    "rem / contrib", ["rem", "contrib"], "$0.25M ÷ $0.45 = 0.56M", "per year", "basis strip", slide="5", estimate=True, assumptions=BE_ASSUME)
der("be", "Break-even overflow at which a second line's fixed cost equals the molder path's cost", 3.0556, "M units",
    "mcap + extra", ["mcap", "extra"], "2.5M + 0.56M = 3.06M", "per year", "sidebar big number, title", slide="5", estimate=True, assumptions=BE_ASSUME)

# Section 3
der("unsv30", "Share of 2030 overflow beyond the molder cap", 0.2647, "%", "gap30 / o30", ["gap30", "o30"], "0.9M ÷ 3.4M = 26%", "2030", "sidebar big number, title", slide="7")
der("specu", "Specialty units in the 2029 demand outlook", 2.24, "M units", "spsh * f29", ["spsh", "f29"], "20% × 11.2M = 2.24M", "2029", "KPI tile", slide="8")
der("scrl", "Accepted units lost to extra specialty scrap", 0.0896, "M units", "specu * scrap", ["specu", "scrap"], "2.24M × 4% = 0.09M", "2029", "KPI driver", slide="8",
    estimate=True, assumptions=["The 4% extra scrap seen in short-run tests holds at full volume",
                                "Lost units have to be remade on the existing line, so they use practical capacity",
                                "The financial forecast does not yet include a specialty yield allowance (briefing pack)"])
der("spare29", "Contract-molder capacity left after 2029 forecast overflow", 0.3, "M units", "mcap - o29", ["mcap", "o29"], "2.5M − 2.2M = 0.3M", "2029", "KPI tile, title", slide="8")
AR_ASSUME = ["Customers that rebid after two monthly fill-rate misses move their whole allocation; the briefing pack gives the right, not the probability",
             "Lost units cost about $0.45 of contribution each (briefing pack); this is an upper bound for one year of lost allocation",
             "Volume at risk is the 2029 signed minimum of 9.4M units, not the larger, nonbinding forecast"]
der("atrisk", "Contribution a year at stake if customers rebid their 2029 signed volume", 4.23, "$M", "s29 * contrib", ["s29", "contrib"],
    "9.4M × $0.45 = $4.2M", "2029", "KPI tile, basis strip", slide="8", estimate=True, assumptions=AR_ASSUME)

# Section 4
der("cslot", "Cash after paying the slot deposit", 8.2, "$M", "cash - rd - dep", ["cash", "rd", "dep"], "$11.0M − $2.2M − $0.60M = $8.2M", "2027", "harvey table", slide="9")
der("hs", "Cash above the covenant minimum after the slot deposit", 1.2, "$M", "avail - dep - floor", ["avail", "dep", "floor"], "$8.8M − $0.60M − $7.0M = $1.2M", "2027", "title, equation", slide="10")
der("bal", "Balance due if the line is ordered after the deposit", 4.2, "$M", "capex - dep", ["capex", "dep"], "$4.8M − $0.60M = $4.2M", "2027", "equation", slide="10")
NEED_ASSUME = ["The deposit is credited, so the order adds only the $4.2M balance (briefing pack)",
               "Line commissioned in mid-2028, so half a year of the $0.55M fixed cost falls in 2028",
               "2028 contract-molder premium of about $0.07M is paid from the same cash",
               "2027–28 operating cash flow, construction inflation and first-article validation cost are not in the briefing pack and are left out"]
der("cost28", "2028 cash costs before new funding: half-year line fixed cost plus molder premium", 0.347, "$M", "0.5 * fixed + prem28", ["fixed", "prem28"],
    "0.5 × $0.55M + $0.07M = $0.35M", "2028", "equation", slide="10", estimate=True, assumptions=NEED_ASSUME)
der("need", "New funding needed to complete the order and stay above the covenant minimum", 3.347, "$M", "bal + cost28 - hs", ["bal", "cost28", "hs"],
    "$4.2M + $0.35M − $1.2M = $3.35M", "2027–28", "equation result, title", slide="10", estimate=True, assumptions=NEED_ASSUME)
der("pbe", "Chance of averting a lost allocation year at which the deposit pays for itself", 0.1418, "%", "dep / atrisk", ["dep", "atrisk"],
    "$0.60M ÷ $4.2M = 14%", "", "basis strip, callout", slide="11", estimate=True,
    assumptions=AR_ASSUME + ["The deposit is forfeited in full if the slot is cancelled (briefing pack)"])
der("ceil", "Annual ceiling of plant plus contract molder", 11.5, "M units", "prac + mcap", ["prac", "mcap"], "9.0M + 2.5M = 11.5M", "per year", "gate text", slide="12")
der("conv30", "Share of nonbinding 2030 volume that must turn firm before demand passes the ceiling", 0.6538, "%", "(ceil - s30) / (f30 - s30)", ["ceil", "s30", "f30"],
    "(11.5M − 9.8M) ÷ (12.4M − 9.8M) = 65%", "2030", "gate text", slide="12")

# ---------------------------------------------------------------- slides
slides = [
    {"id": "c", "role": "cover", "status": "filled"},
    {"id": "es", "role": "exec_summary", "status": "filled", "archetype": "exec-summary", "message_type": "navigation"},
    {"id": "d1", "role": "section_divider", "section_id": "1", "status": "filled", "archetype": "section-divider", "message_type": "navigation"},
    # ---- 1
    {"id": "1", "role": "content", "section_id": "1", "status": "filled",
     "lead_message": {"text": "Measured on accepted output, the line is already 92% loaded in 2027, not the 83% Operations reports",
                      "numbers": [{"text": "92%", "data_ref": "u27"}, {"text": "83%", "data_ref": "ops83"}], "clauses": 1},
     "message_type": "item", "archetype": "kpi-big-numbers", "rationale": "Two measures of one quantity and the headroom left -> KPI tiles",
     "unit_line": "**Existing molding line, 2027 forecast**, utilization in % and headroom in million accepted units",
     "body": {"kind": "kpi", "items": [
         {"point": P("ops83"), "caption": "Operations KPI: units started divided by 10.0M nameplate units",
          "relation": "Basis of the claim of 17% free capacity",
          "drivers": ["Counts units started; quality rejects sit in a separate report",
                      "Nameplate output ignores maintenance, validated changeovers and quality holds",
                      "Overstates the room customers can draw on"]},
         {"point": P("u27"), "caption": "2027 forecast of 8.3M units divided by 9.0M practical accepted capacity",
          "relation": "The denominator that governs the fill rate",
          "drivers": ["Maintenance, changeovers and holds remove 1.0M units of nameplate a year",
                      "Specialty containers scrap 4% more, and the forecast has no allowance for it yet",
                      "Customers judge Pelican on accepted units each month"]},
         {"point": P("head27"), "caption": "million accepted units of headroom left in 2027",
          "relation": "Less than half the 1.7M units that the nameplate metric implies",
          "drivers": ["The 2028 forecast of 9.6M units already exceeds the 9.0M practical limit",
                      "Spare 2027 output could build buffer stock ahead of the 2028 launches",
                      "Launches clustered in one six-week window can use up a month's room"]}]},
     "footnotes": ["Practical accepted capacity nets out maintenance, validated changeovers and quality holds; fill-rate risk is judged on accepted units and specialty scrap"]},
    {"id": "2", "role": "content", "section_id": "1", "status": "filled",
     "lead_message": {"text": "Forecast demand overruns practical capacity from 2028, but signed minimums alone exceed it only from 2029",
                      "highlights": ["2028"], "clauses": 1},
     "message_type": "time-series", "archetype": "stacked-column", "rationale": "Demand over four years split by how firm it is, against a capacity line -> stacked column with benchmark",
     "unit_line": "**Forecast good units, by commitment**, million units a year, 2027–30",
     "layout": {"variant": "takeaway_sidebar", "sidebar": {
         "kind": "bullets", "header": "The gap is real at forecast, but rests on volume nobody has signed",
         "bullets": ["**2028:** forecast passes the 9.0M limit by 0.6M units, while signed minimums still leave 0.5M units spare",
                     "**2029–30:** forecast overflow grows to 3.4M units; on signed minimums it stays at 0.8M",
                     "**Firmness:** volume above minimums is nonbinding, and two key design programs slipped one quarter last year"],
         "rows": [{"label": "Share of 2030 forecast not backed by signed minimums", "basis": "2.6M nonbinding ÷ 12.4M forecast", "point": P("nb30"), "highlight": True}]}},
     "body": {"kind": "chart", "chart_type": "stacked_column", "categories": ["2027", "2028", "2029", "2030"],
              "series": [{"name": "Signed minimum", "points": [P("s27"), P("s28"), P("s29"), P("s30")]},
                         {"name": "Forecast above signed minimum (nonbinding)", "points": [P("a27"), P("a28"), P("a29"), P("a30")]}],
              "sort": "none", "highlight": ["2028"], "value_format": "0.0",
              "benchmark": {"label": "Practical accepted capacity, 9.0M", "point": P("prac")}},
     "footnotes": ["Overflow = forecast good units above 9.0M practical accepted capacity, as given in the briefing pack"]},
    {"id": "d2", "role": "section_divider", "section_id": "2", "status": "filled", "archetype": "section-divider", "message_type": "navigation"},
    # ---- 2
    {"id": "3", "role": "content", "section_id": "2", "status": "filled",
     "lead_message": {"text": "Ordering the whole line in January would leave cash $3.0M below the covenant minimum, with no facility to cover it",
                      "numbers": [{"text": "$3.0M", "data_ref": "short"}], "highlights": ["Second line, full order"], "clauses": 1},
     "message_type": "component", "archetype": "waterfall-bridge", "rationale": "What takes cash from today's balance to the post-order balance -> waterfall",
     "unit_line": "**Unrestricted cash if the line is ordered in January 2027**, $ millions",
     "layout": {"variant": "takeaway_sidebar", "sidebar": {
         "kind": "big_number", "big_number": P("short"), "caption": "cash compared with the $7.0M covenant minimum after a full order",
         "bullets": ["**Full order:** the $4.8M already includes the $0.60M deposit; it is not counted twice",
                     "**No buffer:** there is no committed borrowing facility, and a prepayment-backed loan is not contracted",
                     "**Board test:** growing demand is not accepted as a reason to breach the floor"]}},
     "body": {"kind": "chart", "chart_type": "waterfall",
              "categories": ["Unrestricted cash", "Approved 2027 R&D and validation", "Second line, full order", "Cash after order"],
              "series": [{"name": "Cash", "points": [P("cash"), P("rdn"), P("capn"), P("cord")]}],
              "sort": "none", "highlight": ["Second line, full order"], "value_format": "0.0"},
     "footnotes": ["Excludes 2027 operating cash flow, which the briefing pack does not give"]},
    {"id": "4", "role": "content", "section_id": "2", "status": "filled",
     "lead_message": {"text": "On cost alone, buying overflow beats running a second line until overflow passes about 3.1M units a year",
                      "numbers": [{"text": "3.1M", "data_ref": "be"}], "highlights": ["2028", "2029"], "clauses": 1},
     "message_type": "item", "archetype": "column-time-series", "rationale": "Two cost paths over three years -> clustered column, break-even as basis strip",
     "unit_line": "**Annual cost of serving forecast overflow**, $ millions a year, 2028–30",
     "layout": {"variant": "takeaway_sidebar", "sidebar": {
         "kind": "big_number", "big_number": P("be"), "caption": "million units of overflow a year at which a second line's fixed cost breaks even",
         "bullets": ["**2028–29:** buying overflow costs a fraction of the line's fixed cost",
                     "**2030:** units the molder cannot take lose contribution, and the line wins narrowly",
                     "**Before capex:** the $4.8M purchase is left out, so the case for the line rests on protecting the fill rate, not on cost",
                     "**Two measures:** $0.12 is a make-or-buy premium; $0.45 is contribution lost on units not served"]}},
     "body": {"kind": "chart", "chart_type": "column", "categories": ["2028", "2029", "2030"],
              "series": [{"name": "Contract molder: premium plus contribution lost above its cap", "points": [P("prem28"), P("prem29"), P("mold30")]},
                         {"name": "Second line: fixed maintenance and quality staffing", "points": [P("fixed"), P("fixed"), P("fixed")]}],
              "sort": "none", "highlight": ["2028", "2029"], "value_format": "0.00"},
     "basis": {"header": "How we found the break-even", "terms": [
         {"point": P("mcap"), "caption": "million units the molder takes at $0.12 each: $0.30M a year"},
         {"op": "+", "point": P("extra"), "caption": "million units more, lost at $0.45 each, match the other $0.25M"},
         {"op": "=", "point": P("be"), "caption": "million units a year where both paths cost the same"}]},
     "footnotes": ["2030 molder path: 2.5M units × $0.12 plus 0.9M units not served × $0.45; second line shown for a full year once commissioned"]},
    {"id": "5", "role": "content", "section_id": "2", "status": "filled",
     "lead_message": {"text": "The claim that early builders grew 23% faster cannot justify breaching the cash floor",
                      "numbers": [{"text": "23%", "data_ref": "g23"}], "clauses": 1},
     "message_type": "argument", "archetype": "text-columns", "rationale": "Three reasons a piece of evidence does not hold -> text columns",
     "body": {"kind": "text", "style": "columns", "columns": [
         {"header": "The faster growers also had firmer order books",
          "detail": ["They held more advance purchase commitments than slower peers",
                     "Firm commitments may explain both the early build and the growth",
                     "Pelican holds no commitments beyond contracted minimums today"],
          "point": P("g23"), "point_caption": "faster growth last year, as cited by the VP of Sales"},
         {"header": "They sold into faster-growing segments",
          "detail": ["Their customers sat in higher-growth therapeutic segments",
                     "Segment mix, not capacity timing, may drive the gap",
                     "The comparison does not control for either factor"]},
         {"header": "Pelican's own demand signal is weaker", "emphasis": True,
          "detail": ["One year of cross-section cannot show that a machine caused growth",
                     "Volume above signed minimums is a nonbinding forecast",
                     "Two key design programs slipped one quarter in the past year"],
          "footer": "Signed volume should release the order"}]},
     "so_what": "A public capacity commitment can rest on the reserved slot and booked overflow; it does not need the whole line ordered today",
     "so_what_style": "line"},
    {"id": "d3", "role": "section_divider", "section_id": "3", "status": "filled", "archetype": "section-divider", "message_type": "navigation"},
    # ---- 3
    {"id": "6", "role": "content", "section_id": "3", "status": "filled",
     "lead_message": {"text": "The contract molder can carry forecast overflow through 2029, but would leave 26% of 2030 overflow unserved",
                      "numbers": [{"text": "26%", "data_ref": "unsv30"}], "highlights": ["2030"], "clauses": 1},
     "message_type": "time-series", "archetype": "column-time-series", "rationale": "Overflow over four years against a capacity cap -> column with benchmark",
     "unit_line": "**Forecast overflow above 9.0M practical capacity**, million accepted units a year, 2027–30",
     "layout": {"variant": "takeaway_sidebar", "sidebar": {
         "kind": "big_number", "big_number": P("unsv30"), "caption": "of 2030 forecast overflow lies beyond the molder's annual cap",
         "bullets": ["**2028:** a small call on the molder, worth booking now given its five-month notice",
                     "**2029:** uses nearly all of the cap, so a monthly peak or a lost holiday slot breaks it"],

         "implication": "Book the molder for 2028 now; a second line is needed for 2030 only if the nonbinding volume turns firm"}},
     "body": {"kind": "chart", "chart_type": "column", "categories": ["2027", "2028", "2029", "2030"],
              "series": [{"name": "Forecast overflow", "points": [P("o27"), P("o28"), P("o29"), P("o30")]}],
              "sort": "none", "highlight": ["2030"], "value_format": "0.0",
              "benchmark": {"label": "Contract-molder cap, 2.5M a year", "point": P("mcap")}},
     "footnotes": ["Molder cap is incremental accepted units a year, validated for existing containers only; holiday-period capacity is not yet committed"]},
    {"id": "7", "role": "content", "section_id": "3", "status": "filled",
     "lead_message": {"text": "Annual totals understate the 2029 risk: the molder would have just 0.3M units to spare, and specialty units cannot go there",
                      "numbers": [{"text": "0.3M", "data_ref": "spare29"}], "clauses": 1},
     "message_type": "item", "archetype": "kpi-big-numbers", "rationale": "Four facts behind one risk -> KPI tiles with drivers",
     "unit_line": "**2029 service risk at forecast**, million units, monthly fill rate in %, contribution in $ millions a year",
     "body": {"kind": "kpi", "items": [
         {"point": P("spare29"), "caption": "million units of molder capacity left after 2029 forecast overflow",
          "drivers": ["Extra specialty scrap would use about 0.09M units of it", "Any upside on the 11.2M forecast closes the rest"]},
         {"point": P("specu"), "caption": "million specialty units in 2029 (20% of forecast) the molder cannot make",
          "drivers": ["They run only on the existing line, with no backup", "Molder validation may take two extra months, at a cost not yet quoted"]},
         {"point": P("fill"), "caption": "monthly fill rate customers require",
          "drivers": ["Two misses let a customer rebid its whole allocation", "Launches in one six-week window can break a month the year absorbs"]},
         {"point": P("atrisk"), "caption": "contribution a year at stake if customers rebid their 2029 signed volume",
          "drivers": ["An upper bound: the pack gives the right to rebid, not its odds", "A monthly simulation is needed to size the real exposure"]}]},
     "basis": {"header": "How we sized the contribution at stake", "terms": [
         {"point": P("s29"), "caption": "million units of 2029 signed minimums (briefing pack)"},
         {"op": "×", "point": P("contrib"), "caption": "contribution per good unit served rather than refused (briefing pack)"},
         {"op": "=", "point": P("atrisk"), "caption": "contribution a year at stake, upper bound"}]}},
    {"id": "d4", "role": "section_divider", "section_id": "4", "status": "filled", "archetype": "section-divider", "message_type": "navigation"},
    # ---- 4
    {"id": "8", "role": "content", "section_id": "4", "status": "filled",
     "lead_message": {"text": "Reserving the slot and buying overflow is the only path that holds the cash floor and keeps a pre-2029 line possible",
                      "highlights": ["Reserve slot and buy overflow"], "clauses": 1},
     "message_type": "structure", "archetype": "harvey-ball-table", "rationale": "Four paths compared on the board's criteria -> Harvey-ball table with a verdict column",
     "unit_line": "**Capacity paths compared on the investment committee's tests**, team assessment; cash in $ millions after 2027 commitments",
     "layout": {"variant": "full"},
     "body": {"kind": "table", "table_type": "harvey",
              "columns": ["Cash, $M", "Holds the $7.0M floor", "Serves 2028 overflow", "Protects 2029 fill rate", "Keeps 2030 options open", "Verdict"],
              "rows": [
                  {"label": "Order the whole line now", "cells": [{"point": P("cord")}, {"rating": 0}, {"rating": 3}, {"rating": 4}, {"rating": 1}, {"text": "Reject: cash falls $3.0M below the floor"}]},
                  {"label": "Reserve slot and buy overflow", "highlight": True, "cells": [{"point": P("cslot")}, {"rating": 4}, {"rating": 4}, {"rating": 3}, {"rating": 4}, {"text": "Recommend: cost capped at the deposit, order gated"}]},
                  {"label": "Buy overflow only, no deposit", "cells": [{"point": P("avail")}, {"rating": 4}, {"rating": 4}, {"rating": 2}, {"rating": 3}, {"text": "Close second: better if a later slot is easy to get"}]},
                  {"label": "Do nothing", "cells": [{"point": P("avail")}, {"rating": 4}, {"rating": 0}, {"rating": 0}, {"rating": 1}, {"text": "Reject: 0.6M units unserved in 2028"}]}],
              "legend": "Team assessment from the briefing pack; full circle = fully meets the test"},
     "footnotes": ["Ordered now, the line should arrive after twelve months; ordered by June 2027 under the slot, it arrives in mid-2028, after the 2028 peak starts",
                   "Buying overflow needs five months' notice; it adds about $0.07M of premium in 2028 and no 2027 cash"]},
    {"id": "9", "role": "content", "section_id": "4", "status": "filled",
     "lead_message": {"text": "The slot leaves only $1.2M above the covenant minimum, so completing the order needs about $3.3M of new funding",
                      "numbers": [{"text": "$1.2M", "data_ref": "hs"}, {"text": "$3.3M", "data_ref": "need"}], "clauses": 1},
     "message_type": "component", "archetype": "calculation-bridge", "rationale": "Our own estimate of the funding gap and how it is built -> equation",
     "unit_line": "**New funding needed to order the line after the deposit**, $ millions, 2027–28",
     "body": {"kind": "equation", "terms": [
         {"point": P("bal"), "caption": "balance due on the line once the $0.60M deposit is credited"},
         {"op": "+", "point": P("cost28"), "caption": "2028 cash costs: half a year of line fixed cost and the molder premium"},
         {"op": "−", "point": P("hs"), "caption": "cash above the $7.0M minimum after the deposit ($8.8M − $0.60M − $7.0M)"},
         {"op": "=", "point": P("need"), "caption": "customer prepayment or volume-backed debt needed before ordering"}],
         "assumptions_header": "The funding need is a floor, not a ceiling",
         "assumptions": ["2027–28 operating cash flow is not in the briefing pack and is left out",
                         "Construction inflation and debt pricing are not negotiated; either raises the need",
                         "First-article validation of the specialty product at the molder is not costed",
                         "The CFO's loan idea is for 2028 and nothing is contracted, so funding by June 2027 is the hardest test"]},
     "footnotes": ["Estimate by the team from the briefing pack; live formula in the Calculations sheet of the source workbook"]},
    {"id": "10", "role": "content", "section_id": "4", "status": "filled",
     "lead_message": {"text": "The $0.60M deposit pays off only if 2029 fails the monthly fill rate and the order can be funded",
                      "numbers": [{"text": "$0.60M", "data_ref": "dep"}], "clauses": 1},
     "message_type": "structure", "archetype": "data-table", "rationale": "Downside cases on customer orders and what each means for the deposit -> data table with verdict column",
     "unit_line": "**Downside cases on customer orders**, overflow above 9.0M practical capacity in million units; deposit in $ millions",
     "layout": {"variant": "full"},
     "body": {"kind": "table", "table_type": "data", "verdict_header": "What it means for the slot",
              "columns": ["2029 overflow", "2030 overflow", "When a line is needed", "Deposit, $M"],
              "rows": [
                  {"label": "Orders stay at signed minimums", "cells": [{"point": P("so29")}, {"point": P("so30")}, {"text": "Not by 2030: the molder covers both years"}, {"point": P("dep")}],
                   "note": "Bad bet: the deposit is forfeited for nothing"},
                  {"label": "Forecast, 2029 holds month by month", "cells": [{"point": P("o29")}, {"point": P("o30")}, {"text": "In service for 2030, ordered by early 2029"}, {"text": "Forfeited unless it transfers"}],
                   "note": "Insurance unused; decide 2030 on signed volume"},
                  {"label": "Forecast, 2029 fails a month, funding secured", "cells": [{"point": P("o29")}, {"point": P("o30")}, {"text": "In service by mid-2028, ordered by June 2027"}, {"text": "Credited toward the $4.8M"}],
                   "note": "Pays off: the slot is the only route to a line before 2029"},
                  {"label": "Forecast, 2029 fails a month, no funding", "cells": [{"point": P("o29")}, {"point": P("o30")}, {"text": "Needed, but ordering would breach the floor"}, {"text": "Forfeited"}],
                   "note": "Bad bet: rely on buffer stock and molder validation"}]},
     "callout": {"target": "Forecast, 2029 fails a month, funding secured", "header": "The one case that pays",
                 "detail": "Worth the deposit if this case has more than a 14% chance"},
     "basis": {"header": "How we judged the deposit", "terms": [
         {"point": P("dep"), "caption": "deposit forfeited if the slot is cancelled (briefing pack)"},
         {"op": "÷", "point": P("atrisk"), "caption": "contribution a year at stake if customers rebid (p. 10)"},
         {"op": "=", "point": P("pbe"), "caption": "chance of averting a lost allocation year that repays the deposit"}]}},
    {"id": "11", "role": "content", "section_id": "4", "status": "filled",
     "lead_message": {"text": "A June 2027 gate on 2029 service risk and funding separates the provisional reservation from the full $4.8M commitment",
                      "numbers": [{"text": "$4.8M", "data_ref": "capex"}], "clauses": 1},
     "message_type": "structure", "archetype": "process-flow", "rationale": "Decision steps with a gate between reservation and order -> process flow",
     "layout": {"variant": "full"},
     "body": {"kind": "process", "steps": [
         {"header": "January 2027: reserve and cover 2028",
          "detail": ["Pay the $0.60M deposit; cash stays at $8.2M", "Book the molder for 2028 overflow, five months ahead",
                     "Ask it to commit holiday-period capacity", "Use 2027 headroom to build buffer stock"],
          "footer": "Approve today: deposit only"},
         {"header": "February to May 2027: test 2029",
          "detail": ["Run a monthly fill-rate simulation for 2029", "Add a specialty yield allowance to the forecast",
                     "Quote specialty validation at the molder", "Seek prepayments or volume guarantees"],
          "footer": "Output: evidence for the gate"},
         {"header": "June 2027: release or cancel", "emphasis": True,
          "detail": ["Service: 2029 below 98% even with molder and buffer",
                     "Funding: about $3.3M secured",
                     "Both pass: pay the $4.2M balance",
                     "Either fails: cancel the slot"],
          "point": P("capex"), "point_caption": "full commitment, only if both tests pass", "footer": "Gate: both tests must pass"},
         {"header": "By early 2029: decide the 2030 line",
          "detail": ["Order if signed 2030 volume passes the 11.5M ceiling of plant plus molder",
                     "That needs 65% of nonbinding 2030 volume to turn firm",
                     "The line adds $0.55M a year of fixed cost from commissioning"],
          "footer": "Gate: signed volume and funding"}]},
     "callout": {"target": "June 2027: release or cancel", "header": "Decision gate",
                 "detail": "No order on growth alone: both tests, or the deposit is the cost of the option"}},
    {"id": "end", "role": "end_page", "status": "filled"},
]

storyline = {
    "governing_thought": "Do not build now: reserve the slot as a $0.60M option, book the contract molder for 2028, and order the line only once a 2029 service gap and about $3.3M of funding are proven",
    "exec_summary": [
        {"id": "1", "text": "The line is nearly full, and forecast demand overruns it from 2028, though much of the growth is unsigned",
         "supports": ["1", "2"],
         "sub_points": [{"text": "2027 demand uses 92% of practical capacity, not the 83% Operations reports", "slide_id": "1"},
                        {"text": "Forecast overflow: 0.6M units in 2028, 3.4M in 2030; 0.8M on signed minimums", "slide_id": "2"}]},
        {"id": "2", "text": "Building now breaks the cash covenant and buys little that cheaper bought-in overflow cannot provide",
         "supports": ["3", "4", "5"],
         "sub_points": [{"text": "A January order leaves cash $3.0M below the covenant minimum", "slide_id": "3"},
                        {"text": "Bought-in overflow costs less than a line until it passes about 3.1M units", "slide_id": "4"},
                        {"text": "The 23% faster growth Sales cites is a cross-section, not proof of cause", "slide_id": "5"}]},
        {"id": "3", "text": "The contract molder can bridge overflow through 2029, but 2029 is tight and 2030 needs a second line",
         "supports": ["6", "7"],
         "sub_points": [{"text": "The molder's cap covers 2028–29 but leaves 26% of 2030 overflow unserved", "slide_id": "6"},
                        {"text": "In 2029 just 0.3M units of molder room remain, and none for specialty", "slide_id": "7"}]},
        {"id": "4", "text": "Reserve the slot as a capped $0.60M option, and release the $4.2M balance only at a June 2027 gate",
         "supports": ["8", "9", "10", "11"],
         "sub_points": [{"text": "The slot keeps $1.2M above the floor; the order needs about $3.3M of funding", "slide_id": "9"},
                        {"text": "The deposit pays off only if a funded order averts a 2029 fill-rate miss", "slide_id": "10"},
                        {"text": "If either test fails in June 2027, cancel and decide 2030 on signed volume", "slide_id": "11"}]}],
    "next_steps": [
        {"action": "Before paying, confirm with the supplier how long the slot holds and whether the deposit can move to a later installation", "owner": "Operations Director", "timing": "January–March 2027"},
        {"action": "Pay the $0.60M deposit and book contract-molder capacity for 2028 overflow, including the holiday period", "owner": "Operations Director", "timing": "March 2027"},
        {"action": "Run the monthly 2029 fill-rate simulation with the launch window, specialty scrap and buffer stock", "owner": "Plant supervisor and Operations", "timing": "By May 2027"},
        {"action": "Negotiate customer prepayments or signed-volume guarantees to back about $3.3M of funding", "owner": "CFO and VP of Sales", "timing": "By May 2027"},
        {"action": "Bring the release-or-cancel decision to the investment committee", "owner": "Operations Director and CFO", "timing": "June 2027"}],
}

sections = [
    {"id": "1", "title": "The line is nearly full", "exec_item_id": "1", "tracker_label": "Capacity"},
    {"id": "2", "title": "Why not build now", "exec_item_id": "2", "tracker_label": "Build now"},
    {"id": "3", "title": "What overflow can cover", "exec_item_id": "3", "tracker_label": "Overflow"},
    {"id": "4", "title": "Reserve, then gate the order", "exec_item_id": "4", "tracker_label": "Decision"},
]

decision_audit = {
    "constraints": [
        {"item": "$7.0M covenant minimum after commitments, no committed borrowing facility", "reflected": True,
         "effect": "rules out a January order ($3.0M short); the slot leaves $1.2M above it", "slide_ids": ["3", "9"]},
        {"item": "$2.2M of approved 2027 validation and R&D", "reflected": True, "effect": "deducted before any capacity spend", "slide_ids": ["3", "9"]},
        {"item": "Deposit credited toward the $4.8M, not added again", "reflected": True, "effect": "order after the deposit adds only the $4.2M balance", "slide_ids": ["3", "9"]},
        {"item": "$0.55M a year of fixed cost from commissioning", "reflected": True, "effect": "in the cost comparison and as half a year in the 2028 funding need", "slide_ids": ["4", "9"]},
        {"item": "Contract molder: 2.5M-unit cap, five months' notice, not validated for the specialty product, holiday capacity uncommitted", "reflected": True,
         "effect": "molder covers 2028–29 on annual totals only; 2029 margin is 0.3M units", "slide_ids": ["6", "7"]},
        {"item": "98% monthly fill rate, rebid after two misses", "reflected": True, "effect": "the June 2027 service test is a monthly simulation, not an annual check", "slide_ids": ["7", "11"]},
        {"item": "Specialty scrap 4% higher, not yet in the forecast", "reflected": True, "effect": "uses about 0.09M of the 0.3M spare molder units in 2029", "slide_ids": ["7"]},
        {"item": "First-article validation cost, construction inflation, debt pricing, 2027–28 operating cash flow", "reflected": False,
         "effect": "not in the pack; the $3.3M funding need is stated as a floor and the slide says so", "slide_ids": ["9"]},
        {"item": "CFO's loan idea is for 2028 and not contracted", "reflected": True, "effect": "funding by June 2027 is named as the hardest test and a case where the slot is a bad bet", "slide_ids": ["9", "10"]},
    ],
    "alternatives": [
        {"option": "Skip the deposit, buy overflow, and decide the line in late 2028 for 2030", "verdict": "rejected",
         "why": "cheaper if 2029 holds month by month and a later slot is easy to get, but it gives up the only route to a line before 2029, the year with 0.3M units of molder room; kept as close second and its key uncertainty (later slot availability) is the first next step",
         "triage": "body", "slide_ids": ["8", "10"]},
        {"option": "Order the whole line now (VP of Sales)", "verdict": "rejected", "why": "breaches the covenant by $3.0M; the 23% growth evidence is cross-sectional", "triage": "body", "slide_ids": ["3", "5", "8"]},
        {"option": "Use 2027 headroom (0.7M units) to build buffer stock for 2028 launches", "verdict": "combined",
         "why": "covers part of the 2028 peak at no capex; working-capital cost and shelf life are not in the pack", "triage": "body", "slide_ids": ["1", "11"]},
    ],
    "failure_threshold": {"driver": "2029 monthly fill rate with the molder and buffer stock, and 2030 signed volume",
                          "threshold": "the line is needed before 2029 only if the monthly simulation shows 2029 below 98%; for 2030 once signed volume passes 11.5M units, i.e. 65% of nonbinding volume turns firm",
                          "range": "2029 overflow low / base / high: 0.4M (signed) / 2.2M (forecast) / about 2.3M (forecast plus specialty scrap), against the 2.5M molder cap",
                          "triage": "body", "slide_ids": ["2", "6", "7", "10", "11"]},
    "consistency": {"headline": storyline["governing_thought"], "holds": True,
                    "fix": "First draft gated the order on committed 2029 demand above 11.5M, a level above the forecast itself; the gate now tests 2029 monthly service and funding of about $3.3M (not $3.0M), and the deposit is framed as insurance that is lost in three of four cases"},
}

spec = {
    "spec_version": "0.1", "mode": "deck_detailed",
    "meta": {"title": "When to add molding capacity", "subtitle": "Second molding line: reserve, build or buy overflow. Investment committee, January 2027",
             "company_name": "Pelican Packaging", "audience": "Investment committee",
             "purpose": "Decide whether to reserve the installation slot, order the line, or rely on contract overflow",
             "date": "2026-11-20", "language": "en-US", "confidentiality": "Synthetic benchmark case; every number from the briefing pack", "theme": "navy"},
    "inputs": [{"id": "in-1", "kind": "file", "label": "Pelican Packaging briefing pack (evidence/briefing-pack.md)",
                "content": open(os.path.join(HERE, "..", "evidence", "briefing-pack.md")).read()}],
    "storyline": storyline, "sections": sections, "slides": slides, "data_points": DP,
    "sources": [{"id": "s1", "kind": "user_provided", "name": "Pelican Packaging briefing pack", "input_id": "in-1"},
                {"id": "s2", "kind": "derived", "name": "Team analysis of the briefing pack"}],
    "decision_audit": decision_audit,
}

KEEP = {"cash", "rd", "floor", "capex"}
def _refs(o):
    if isinstance(o, dict):
        if "data_ref" in o: yield o["data_ref"]
        for v in o.values(): yield from _refs(v)
    elif isinstance(o, list):
        for v in o: yield from _refs(v)
first = {}
for s in slides:
    if s["role"] != "content": continue
    for r in _refs({k: s.get(k) for k in ("lead_message", "body", "layout", "basis", "callout")}):
        first.setdefault(r, s["id"])
for d in DP:
    if d["id"] in first: d["slide_id"] = first[d["id"]]
    elif d["id"] not in KEEP: d["slide_id"] = str(int(d["slide_id"]) - 1)

with open(os.path.join(HERE, "pelican-capacity.json"), "w") as fh:
    json.dump(spec, fh, indent=1, ensure_ascii=False)
print("written", len(DP), "data points,", len([s for s in slides if s["role"] == "content"]), "content slides")
