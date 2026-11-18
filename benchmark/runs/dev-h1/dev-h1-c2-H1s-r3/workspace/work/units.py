"""compile.units, untraceable numbers, corrections and the fidelity check (references/compile.md)."""

def U(id, type, text, loc, slides, critical=True):
    return {"id": id, "type": type, "text": text, "source_loc": loc, "critical": critical, "slide_ids": slides}

UNITS = [
    U("u01", "answer", "Fix gross margin and delivery economics, not headcount: seven firm levers lift operating margin from 1.0% to ~2.6% by FY2028, and a second wave prepared now closes the gap to the 3.0% target", "p.1-2", ["es", "15"]),
    U("u02", "claim", "Reaching 3.0% by FY2028 means adding ~$35.6M of operating income (target $43.3M on pro-forma sales of $1,444M; do-nothing FY2028 $7.7M after the 2027 wage step and +3% delivery rate)", "p.3", ["3"]),
    U("u03", "constraint", "Plan constraints: margin >= 3.0% by FY2028; <= $25M one-time cost FY2026-28; operating income >= $20M in FY2026 (covenant); no closure of a store leased beyond 2027 without a board vote; keep delivery in some form", "p.3", ["3"]),
    U("u04", "assumption", "Do-nothing baseline: FY2025 ratios and scale held (optimistic), wage step on the whole labor bill (conservative), provider's +3% accepted; if erosion continued FY2026 would already breach the covenant", "p.3", ["3"]),
    U("u05", "claim", "Hypothesis test: diagnosis holds (conditions 1-3, 6 supported; 4 partly; management's 8% cut not supported) but promotions and delivery alone (~$13M) are not enough; even all seven firm levers (~$30M) reach ~2.6%, so a second wave is needed", "p.4", ["4"]),
    U("u06", "claim", "Gross margin (-1.02 pp) and e-commerce fulfillment (-0.84 pp) explain 79% of the 2.35 pp decline; store labor -0.30 pp = 13%; occupancy 8%; other SG&A 0%", "p.5", ["es", "5"]),
    U("u07", "claim", "Dollar view misleads: labor +$14.3M but sales +5.8%; at FY2023 ratio FY2025 labor would be $177.4M, so only $4.5M excess; e-commerce fulfillment $5.2M -> $18.1M", "p.5", ["5"]),
    U("u08", "claim", "Gross-margin loss of 1.02 pp fully explained by promotion mix (-0.70 pp, -$10.5M) and shrink (-0.50 pp, -$7.5M); private label +0.18 pp (+$2.7M) offset less than a fifth; vendor funding 55% -> 46%; shrink $39.1M (waste 45%, theft 35%, admin 20%)", "p.6", ["6"]),
    U("u09", "claim", "Deeper promotion has not paid for itself: 38% of events lose money; +5 pp promo share costs $10.5M a year and needs ~$53M of new sales; category team's 'promotions work' fails its own arithmetic (break-even 2.3 pp of extra share; correlation)", "p.7", ["es", "7"]),
    U("u10", "recommendation", "Promotion implication: cut loss-making events chain-wide, require vendor funding per event, keep targeted depth only in ValuMart-exposed stores while traffic is measured, move the value message to private label; stage and track the reset because the needed promotion level is an open question", "p.7", ["7"]),
    U("u11", "claim", "Productivity absorbed two-thirds of the 9.4% wage rise (wage +1.11 pp, productivity -0.77 pp); lean-labor stores run more shrink (Q1 3.1% vs Q4 2.3%); rebalance hours rather than cut them (waste and receiving errors 65% of shrink)", "p.8", ["8"]),
    U("u12", "claim", "Fully costed, e-commerce loses ~$10.4M a year, not +6.1%: delivered order -$12.34, click-and-collect -$1.64; delivery -$9.5M; break-even needs 94% (delivery) / 39% (C&C) of sales new vs 30% survey; freezing locks in the loss", "p.9", ["es", "9"]),
    U("u13", "alternative", "Management draft plan (8% hours cut + e-commerce freeze) leaves FY2028 margin ~1.1% ($16.6M): added shrink $3.8-7.5M (midpoint $5.6M), each 1% of sales lost ~ $3.0M, freeze keeps -$10.4M, promotions untouched, shrink effects lag the covenant", "p.10", ["es", "10"]),
    U("u14", "alternative", "Three options: A draft (reject), B margin-first (recommend: ~2.6% firm, ~3.4% with full second wave, ~$17M one-time, ~$25M FY2026), C click-and-collect only (~3.0% on firm levers, $42.9M; breaks delivery commitment; fallback if second-wave delivery pricing fails); deeper promotions also rejected (~$2.1M per point)", "p.11", ["es", "11"]),
    U("u15", "recommendation", "Seven firm levers worth ~$30.1M (range $16.8-38.0M) by FY2028: promotion reset 6.1, vendor funding 3.7, private label 4.3, shrink 2.8, targeted labor 5.5, delivery pricing 3.3, exit 6 stores 4.4; with sizing, evidence strength and start", "p.12", ["es", "12"]),
    U("u16", "claim", "Tested delivery pricing adds ~$2.5M a year (+$0.8M contract), keeps the service; delivered orders still lose ~$9.04 (~$6.4M a year), only a quarter of the loss fixed; next test cost-recovery pricing or membership (~$3M)", "p.13", ["13"]),
    U("u17", "recommendation", "Exit the six loss-making stores whose leases end by 2027 (~$4.4M a year, no board vote, payback < 1 year); other three take ~3.4 years and $7.5M (44% of one-time budget): test a fix for 6 months, board vote mid-FY2027 if it fails; pro-rata split is the main uncertainty (~$3M)", "p.14", ["14"]),
    U("u18", "claim", "Firm levers take margin to ~2.6% ($37.8M) by FY2028; gap $5-6M; second wave ~$9.9M (exit 3 stores 2.2, cost-recovery delivery 3.0, vendor funding to 55% 4.7), about half needed; full plan 3.4%; prepare all three now", "p.15", ["es", "15"]),
    U("u19", "recommendation", "Four no-regret first moves in 90 days (promotion reset with vendor terms, delivery pricing roll-out, targeted labor rebalancing, notice on 6 stores) lift FY2026 operating income to ~$24.9M, ~$5M above covenant; why these first; FY2027-28 roadmap", "p.16", ["es", "16"]),
    U("u20", "gate", "Mid-FY2027 checkpoint: if run-rate margin is below ~2.4%, trigger the second wave in full and put fallback C to the owners", "p.16", ["16"]),
    U("u21", "risk", "If about a third of FY2025's $18M erosion recurs, the FY2026 covenant headroom is gone: track monthly and brief the lender early", "p.16", ["16"]),
    U("u22", "constraint", "One-time cost ~$17M inside the $25M cap with ~$8M contingency; firm wave alone ~$9.5M; cap holds unless allowances prove ~80% too low; only the $7.5M lease exit is from the pack", "p.17", ["es", "17"]),
    U("u23", "risk", "Sensitivities with triggers and responses: traffic (-$2.0M), vendor funding stays 46% (-$3.7M), 50% new e-commerce (loss -$5.3M; delivery still -$8.50/order), shrink only 2.45% (-$2.1M), wage +6% (-$3.6M), loss split (-$1.4M), FY2026 erosion (~$5M slippage); diagnosis robust", "p.18", ["18"]),
    U("u24", "gate", "Gates: comps in ValuMart areas below -4.2%; vendor funding share in next two cycles; shrink pilot scale only if >= 0.2 pp gain; store P&Ls before notice; monthly operating income vs $20M path", "p.18", ["18"]),
    U("u25", "decision", "Three decisions today: endorse the margin-first plan in place of the 8% cut; approve delivery repricing roll-out and e-commerce guardrail; authorize preparation of the second wave (3-store vote by mid-FY2027, cost-recovery pilot, vendor terms)", "p.19", ["es", "19"]),
    U("u26", "next_step", "Next 90 days: covenant forecast and lender briefing (CFO, wk 2); promotion calendar and vendor terms (Category, wk 4); delivery pricing live and contract (E-commerce, wk 6); labor plan (COO, wk 6); store P&L and notices (Property/CFO, wk 8); shrink pilot in 10 stores (COO, wk 12)", "p.19", ["19", "end"]),
    U("u27", "gate", "Quarterly scorecard: promo share 29% -> 25%; vendor funding 46% -> 50%+; private label 18.5% -> 21%; shrink 2.6% -> 2.3%; loss per delivered order $12.34 -> < $5; operating income >= $20M FY2026, 3.0% FY2028", "p.19", ["19"]),
    U("u28", "risk", "Key risks are ValuMart traffic and vendor push-back; if wave 2 falls short, click-and-collect-only reaches ~3.0% but needs owners' consent", "p.2", ["es", "11"]),
    U("u29", "claim", "Appendix A1: ratio changes sum to the 2.35 pp decline; mix and labor decompositions reconcile", "p.21", ["21"], False),
    U("u30", "claim", "Appendix A2: e-commerce fulfillment rebuilds exactly from order data; fully costed loss -2.6, -6.0, -10.4; team's 6.1% less delivery = -0.4% before cannibalization", "p.22", ["22"], False),
    U("u31", "range", "Appendix A3: low case ~$16.8M (FY2028 1.7%), base $30.1M (2.6%), high $38.0M (3.2%); FY2026 in-year $9.6M", "p.23", ["12", "23"]),
    U("u32", "assumption", "Appendix A4: choices made without CEO input (fiscal timing, baseline, wage step, pro-rata split), claims not relied on, team estimates, data caveats", "p.24", ["24"], False),
]

UNTRACEABLE = [
    {"data_point_id": "optC", "critical": True,
     "ack": "Kept as the analysis's estimate, flagged unverified on p.11 (no user available; recommended option chosen). A direct rebuild from the pack gives about $43.2M, so the ~3.0% conclusion holds either way",
     "note": "Option C's $42.9M cannot be rebuilt exactly; removing the post-repricing delivery loss and the contract gain, less the click-and-collect loss on 40% switchers, gives $42.9M only if the baseline +3% rate rise is not added back"},
    {"data_point_id": "chk", "critical": True,
     "ack": "Kept as the analysis's gate threshold, flagged as a team estimate (no user available; recommended option chosen)",
     "note": "The ~2.4% mid-FY2027 checkpoint is stated by the analysis without a derivation; it sits between the low case (1.7%) and the firm plan (2.6%)"},
    {"data_point_id": "pl26", "critical": True,
     "ack": "Kept as the analysis's FY2026 phasing estimate (no user available; recommended option chosen); it moves FY2026 operating income by about $0.1M at most",
     "note": "The analysis says ~25% of run-rate, which would be about $1.1M at FY2025 scale; it shows $1.0M"},
    {"data_point_id": "w_del", "critical": False, "note": "Analysis rounds half of the remaining $6.4M delivery loss ($3.2M) to ~$3M"},
    {"data_point_id": "l7_lo", "critical": False, "note": "Low case for the store exit is an analysis assumption (the 6 carry less of the loss)"},
    {"data_point_id": "l7_hi", "critical": False, "note": "High case for the store exit is an analysis assumption"},
    {"data_point_id": "al_tools", "critical": True, "ack": "Kept as the analysis's planning allowance, flagged for CFO validation as the source deck itself does", "note": "Team planning allowance"},
    {"data_point_id": "al_pl", "critical": True, "ack": "Kept as the analysis's planning allowance, flagged for CFO validation as the source deck itself does", "note": "Team planning allowance"},
    {"data_point_id": "al_promo", "critical": True, "ack": "Kept as the analysis's planning allowance, flagged for CFO validation as the source deck itself does", "note": "Team planning allowance"},
    {"data_point_id": "al_del", "critical": True, "ack": "Kept as the analysis's planning allowance, flagged for CFO validation as the source deck itself does", "note": "Team planning allowance"},
    {"data_point_id": "del_tgt", "critical": False, "note": "Scorecard target stated by the analysis; consistent with halving the post-repricing $9.04 loss"},
]

CORRECTIONS = [
    {"unit_id": "u02", "was": "Title: 'adding ~$35M of operating income'", "now": "'adding about $36M' (chart value $35.6M)",
     "why": "The gap is $43.3M − $7.7M = $35.6M, which rounds to $36M"},
    {"unit_id": "u23", "was": "Shrink only reaches 2.45%: FY2028 impact −$2.1M", "now": "−$2.2M",
     "why": "0.15 pp × $1,444M = $2.17M; the source took the difference of rounded lever values (2.8 − 0.7)"},
    {"unit_id": "u23", "was": "Title: 'The answer is most sensitive to traffic response and vendor funding'", "now": "'Vendor funding and wages move the answer most'",
     "why": "The analysis's own sensitivity table ranks vendor funding (−$3.7M) and a +6% wage step (−$3.6M) above shrink (−$2.2M) and traffic (−$2.0M); traffic stays a key risk in the executive summary because it is the least certain input (pack §11)"},
]

CHECK = {"critical_units": sum(1 for u in UNITS if u["critical"]), "preserved": sum(1 for u in UNITS if u["critical"]),
         "notes": "Read unit by unit against the rendered spec: every critical unit is on a main-deck slide with the same numbers, conditions and option ranking; "
                  "slide order and one-point-per-slide structure kept (source p.3-p.24 = our p.3-p.24). Wording changed to American English and our title style; three corrections logged; "
                  "untraceable numbers flagged. Source p.17 table became a ranked bar chart with the same items, values and waves; p.9 table became two waterfall panels with the same values; p.16 roadmap and FY2026 bridge became a timeline with the bridge in the sidebar. An independent reviewer then read the rendered deck against the source and the pack: no arithmetic errors; lost qualifiers it found (delivery guardrail on p.19, 'before lost sales', 'while traffic is measured', covenant lag on p.10, 'about'/'could be' hedges, lease-expiry, managers' claim on p.8) were restored, and the p.18 title ranking was corrected to match the table"}
