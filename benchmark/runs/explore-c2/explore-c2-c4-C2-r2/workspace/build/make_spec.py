"""Builds the storyline spec for the Palisade Docs 2027 pricing deck from the briefing pack."""
import json, re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
PACK = (ROOT / "evidence" / "briefing-pack.md").read_text()
FLAT = " ".join(PACK.split())

DPS, VAL = [], {}


def raw(id_, slide, label, value, unit, period, excerpt, locator, used_in, **kw):
    excerpt = " ".join(excerpt.split())
    assert excerpt in FLAT or excerpt.startswith('"'), f"excerpt not verbatim: {id_}: {excerpt}"
    d = dict(id=id_, slide_id=slide, label=label, value=value, unit=unit, period=period, source_id="s1",
             excerpt=excerpt, locator=locator, used_in=used_in, **kw)
    DPS.append(d); VAL[id_] = value


def ev(calc):
    e = calc
    for k in sorted(VAL, key=len, reverse=True):
        e = re.sub(rf"(?<![\w.]){re.escape(k)}(?![\w-])", repr(VAL[k]), e)
    return eval(e)


def der(id_, slide, label, unit, period, derived_from, formula, calc, used_in, assumptions=None, **kw):
    v = ev(calc)
    nd = (2 if abs(v) >= 0.1 else 4) if unit == "%" else 3 if unit in ("$M", "pp") else 2
    d = dict(id=id_, slide_id=slide, label=label, value=round(v, nd), unit=unit, period=period, source_id="s0",
             derived_from=derived_from, formula=formula, calc=calc, used_in=used_in, **kw)
    if assumptions:
        d["estimate"] = True; d["assumptions"] = assumptions
    DPS.append(d); VAL[id_] = d["value"]


def cell(row, col, val):
    return f'"{row}" row; column {col} = "{val}"'


T1 = "Briefing pack §5, Table 1 (segments, mid-2026)"
T2 = "Briefing pack §6, Table 2 (exit survey)"

# ---------- raw numbers from the briefing pack ----------
raw("arr", "1", "Palisade ARR", 86.0, "$M", "mid-2026", "ARR is $86.0M from 7,400", "Briefing pack §1", "weights; growth target base")
raw("cust", "1", "Palisade customers", 7400, "customers", "mid-2026", "ARR is $86.0M from 7,400", "Briefing pack §1", "weights")
for seg, lab, c, a in [("smb", "SMB", 5900, 21.0), ("mm", "Mid-market", 1350, 41.0), ("ent", "Enterprise", 150, 24.0)]:
    raw(f"{seg}_c", "1", f"{lab} customers", c, "customers", "mid-2026", cell(lab, "Customers", f"{c:,}"), T1, "weights")
    raw(f"{seg}_arr", "1", f"{lab} ARR", a, "$M", "mid-2026", cell(lab, "ARR, $M", f"{a:.1f}"), T1, "weights; heatmap")
churn = {"smb": (0.020, 0.031), "mm": (0.006, 0.008), "ent": (0.002, 0.002)}
labs = {"smb": "SMB", "mm": "Mid-market", "ent": "Enterprise"}
for seg, (a, b) in churn.items():
    raw(f"{seg}_ch25", "1", f"{labs[seg]} monthly logo churn, H1 2025", a, "%", "H1 2025",
        cell(labs[seg], "Monthly logo churn H1 2025", f"{a*100:.1f}%"), T1, "column chart")
    raw(f"{seg}_ch26", "1", f"{labs[seg]} monthly logo churn, H1 2026", b, "%", "H1 2026",
        cell(labs[seg], "Monthly logo churn H1 2026", f"{b*100:.1f}%"), T1, "column chart")
for seg, v in [("smb", 0.94), ("mm", 1.12), ("ent", 1.18)]:
    raw(f"{seg}_nrr", "7", f"{labs[seg]} net revenue retention, trailing 12 months", v, "%", "trailing 12 months to mid-2026",
        cell(labs[seg], "Net revenue retention (trailing 12 months)", f"{round(v*100)}%"), T1, "heatmap")
raw("grow", "4", "2027 ARR growth objective", 0.15, "%", "2027", "Grow ARR at least 15% in 2027 (from $86.0M).", "Briefing pack §3", "growth target")
raw("nrr_floor", "10", "Net revenue retention floor", 1.0, "%", "2027", "Keep net revenue retention above 100% overall.", "Briefing pack §3", "options table text")
raw("cfo_pct", "4", "CFO's proposed list-price rise, every plan", 0.12, "%", "from Jan 2027",
    "Raise list prices 12% on every plan at renewal from January 2027.", "Briefing pack §4, CFO", "basis strip")
raw("cfo_arr", "4", "ARR the CFO attributes to the 12% rise", 10.3, "$M", "2027", "That is $10.3M of ARR.", "Briefing pack §4, CFO", "footnote")
raw("promo_c", "2", "Promotion-cohort SMB customers still in the base", 2100, "customers", "mid-2026",
    "The\n  promotion brought in 2,100 SMB customers who are still counted in the base above", "Briefing pack §6", "sidebar bullet")
raw("promo_arr", "2", "Promotion-cohort ARR at full price", 4.4, "$M", "mid-2026", "about $4.4M of ARR at full price", "Briefing pack §6", "sidebar bullet")
raw("disc", "3", "2025 promotion discount, first six months", 0.5, "%", "Feb–Aug 2025",
    "new self-serve SMB customers got 50% off for their first six months", "Briefing pack §6", "footnote")
raw("act_promo", "3", "Promotion cohort: new customers sending ≥5 documents in first month", 0.41, "%", "2025 cohort",
    "41% for the promotion cohort", "Briefing pack §6", "panel bar")
raw("act_other", "3", "Other cohorts: new customers sending ≥5 documents in first month", 0.72, "%", "other cohorts",
    "72% for other cohorts", "Briefing pack §6", "panel bar")
raw("np_ch26", "2", "Monthly churn, SMB customers not from the promotion, H1 2026", 0.021, "%", "H1 2026",
    "come through the promotion: 2.1%", "Briefing pack §6", "waterfall input; scenario bar")
raw("np_ch25", "2", "Monthly churn, same kind of SMB customers, H1 2025", 0.020, "%", "H1 2025",
    "(H1 2025 for the\n  same kind of customers: 2.0%)", "Briefing pack §6", "waterfall input")
for id_, row, v in [("pr_smb25", "all SMB churners H1 2025", 0.19), ("pr_smb26", "all SMB churners H1 2026", 0.34),
                    ("pr_promo", "promo-cohort churners H1 2026", 0.52), ("pr_np", "non-promo SMB churners H1 2026", 0.18)]:
    raw(id_, "3", f"Churners citing price / cheaper option: {row}", v, "%", row[-7:], cell(row, "Share citing price", f"{round(v*100)}%"), T2, "panel bar")
raw("ink9", "5", "Inkwell Starter price", 9, "$", "since Oct 2025",
    "launched a Starter plan at $9 per user per month in October 2025", "Briefing pack §7", "panel bar", definition="per user per month")
raw("pal15", "5", "Palisade SMB plan price", 15, "$", "2026", "Palisade's SMB plan is $15 per\n  user per month",
    "Briefing pack §7", "panel bar", definition="per user per month")
raw("pal29", "5", "Palisade Business plan price", 29, "$", "2026", "Business plan $29", "Briefing pack §7", "panel bar", definition="per user per month")
raw("ink24", "5", "Inkwell Pro price", 24, "$", "2026", "Inkwell Pro $24", "Briefing pack §7", "panel bar", definition="per user per month")
raw("win25", "5", "Palisade SMB win rate where Inkwell was considered, H1 2025", 0.51, "%", "H1 2025",
    "fell from 51% (H1 2025) to 38% (H1 2026)", "Briefing pack §7", "panel column")
raw("win26", "5", "Palisade SMB win rate where Inkwell was considered, H1 2026", 0.38, "%", "H1 2026",
    "fell from 51% (H1 2025) to 38% (H1 2026)", "Briefing pack §7", "panel column; title")
raw("seats", "7", "Deal size above which Inkwell has not been seen", 200, "seats", "2026",
    "Inkwell has not been seen in mid-market or enterprise deals with more than 200 seats.", "Briefing pack §7", "footnote")
EX23 = "+8% at renewal. SMB monthly churn rose from 1.8% to 2.3% for six months, then\n  settled at 1.9%."
raw("p23", "6", "2023 SMB price increase at renewal", 0.08, "%", "2023", EX23, "Briefing pack §8", "KPI tile; SMB test level")
raw("ch23a", "6", "SMB monthly churn before the 2023 increase", 0.018, "%", "2023", EX23, "Briefing pack §8", "KPI tile")
raw("ch23b", "6", "SMB monthly churn in the six months after the 2023 increase", 0.023, "%", "2023", EX23, "Briefing pack §8", "KPI tile")
raw("ch23c", "6", "SMB monthly churn once settled after the 2023 increase", 0.019, "%", "2023", EX23, "Briefing pack §8", "KPI tile")
EX24 = "+10% list price for new mid-market sign-ups for three months: conversion 23.1%\n  against 23.6% for the control group (difference not statistically significant)."
raw("mmtest", "8", "2024 mid-market list-price test", 0.10, "%", "2024", EX24, "Briefing pack §8", "KPI tile; recommended rise")
raw("conv_t", "8", "Mid-market conversion at +10% list price", 0.231, "%", "2024 test", EX24, "Briefing pack §8", "KPI tile")
raw("conv_c", "8", "Mid-market conversion, control group", 0.236, "%", "2024 test", EX24, "Briefing pack §8", "KPI tile")
raw("cap_share", "4", "Share of enterprise ARR under contracts capping annual rises", 0.60, "%", "2026",
    "60% of\n  enterprise ARR is under contracts that cap annual price increases at 7%.", "Briefing pack §8", "waterfall input")
raw("cap7", "4", "Cap on annual price increases in capped enterprise contracts", 0.07, "%", "2026",
    "cap annual price increases at 7%", "Briefing pack §8", "waterfall input")
raw("ent_ren", "4", "Share of enterprise ARR renewing in 2027", 0.40, "%", "2027",
    "40% of\n  enterprise ARR renews in 2027", "Briefing pack §8", "waterfall input")
raw("mm_ren", "4", "Share of mid-market ARR renewing in 2027", 0.85, "%", "2027",
    "as does 85% of mid-market ARR and all SMB ARR", "Briefing pack §8", "waterfall input")
raw("x3", "3", "Churn multiple, SMB customers sending <5 documents in first month", 3, "x", "2026",
    "churn at about three times the rate of those who send more", "Briefing pack §9", "so-what bar")
raw("dash25", "1", "Board dashboard 'monthly churn', start", 0.014, "%", "undefined", "Monthly churn: 1.4% → 2.3%.", "Briefing pack §10", "footnote")
raw("dash26", "1", "Board dashboard 'monthly churn', end", 0.023, "%", "undefined", "Monthly churn: 1.4% → 2.3%.", "Briefing pack §10", "footnote")
raw("cs_half", "11", "Customer Success claim: reduction in SMB churn from onboarding", 0.5, "%", "within two quarters",
    "An onboarding programme will halve SMB churn within two quarters.", "Briefing pack §10", "scenario bar", definition="'halve' = 50% reduction")

# ---------- slide 1: where churn rises ----------
W = ["Mid-2026 customer counts and ARR are used as weights for both periods",
     "ARR per customer is the same for every customer within a segment"]
der("dch_smb", "1", "Change in SMB monthly churn, H1 2025 to H1 2026", "pp", "H1 2025–H1 2026", ["smb_ch26", "smb_ch25"], "(3.1% − 2.0%) × 100", "(smb_ch26 - smb_ch25) * 100", "heatmap; basis text")
der("dch_mm", "1", "Change in mid-market monthly churn, H1 2025 to H1 2026", "pp", "H1 2025–H1 2026", ["mm_ch26", "mm_ch25"], "(0.8% − 0.6%) × 100", "(mm_ch26 - mm_ch25) * 100", "heatmap; basis text")
der("dch_ent", "1", "Change in enterprise monthly churn, H1 2025 to H1 2026", "pp", "H1 2025–H1 2026", ["ent_ch26", "ent_ch25"], "(0.2% − 0.2%) × 100", "(ent_ch26 - ent_ch25) * 100", "heatmap")
der("sh_xlost", "1", "SMB share of the extra customers lost each month", "%", "H1 2026 against H1 2025",
    ["smb_c", "smb_ch26", "smb_ch25", "mm_c", "mm_ch26", "mm_ch25", "ent_c", "ent_ch26", "ent_ch25"],
    "5,900 × 1.1 pp ÷ (5,900 × 1.1 pp + 1,350 × 0.2 pp + 150 × 0 pp)",
    "smb_c * (smb_ch26 - smb_ch25) / (smb_c * (smb_ch26 - smb_ch25) + mm_c * (mm_ch26 - mm_ch25) + ent_c * (ent_ch26 - ent_ch25))",
    "sidebar row; title", assumptions=W[:1])
der("sh_xarr", "1", "SMB share of the extra ARR lost each month", "%", "H1 2026 against H1 2025",
    ["smb_arr", "smb_ch26", "smb_ch25", "mm_arr", "mm_ch26", "mm_ch25", "ent_arr", "ent_ch26", "ent_ch25"],
    "$21.0M × 1.1 pp ÷ ($21.0M × 1.1 pp + $41.0M × 0.2 pp + $24.0M × 0 pp)",
    "smb_arr * (smb_ch26 - smb_ch25) / (smb_arr * (smb_ch26 - smb_ch25) + mm_arr * (mm_ch26 - mm_ch25) + ent_arr * (ent_ch26 - ent_ch25))",
    "sidebar row", assumptions=W)
der("cw25", "1", "Customer-weighted monthly churn, H1 2025", "%", "H1 2025", ["smb_c", "smb_ch25", "mm_c", "mm_ch25", "ent_c", "ent_ch25", "cust"],
    "Σ customers × churn ÷ 7,400", "(smb_c * smb_ch25 + mm_c * mm_ch25 + ent_c * ent_ch25) / cust", "footnote (dashboard check)")
der("cw26", "1", "Customer-weighted monthly churn, H1 2026", "%", "H1 2026", ["smb_c", "smb_ch26", "mm_c", "mm_ch26", "ent_c", "ent_ch26", "cust"],
    "Σ customers × churn ÷ 7,400", "(smb_c * smb_ch26 + mm_c * mm_ch26 + ent_c * ent_ch26) / cust", "footnote (dashboard check)")
der("aw25", "1", "ARR-weighted monthly churn, H1 2025", "%", "H1 2025", ["smb_arr", "smb_ch25", "mm_arr", "mm_ch25", "ent_arr", "ent_ch25", "arr"],
    "Σ ARR × churn ÷ $86.0M", "(smb_arr * smb_ch25 + mm_arr * mm_ch25 + ent_arr * ent_ch25) / arr", "footnote (dashboard check)")
der("aw26", "1", "ARR-weighted monthly churn, H1 2026", "%", "H1 2026", ["smb_arr", "smb_ch26", "mm_arr", "mm_ch26", "ent_arr", "ent_ch26", "arr"],
    "Σ ARR × churn ÷ $86.0M", "(smb_arr * smb_ch26 + mm_arr * mm_ch26 + ent_arr * ent_ch26) / arr", "footnote (dashboard check)")

# ---------- slide 2: promotion explains the SMB rise ----------
der("np_drift", "2", "Change in churn of SMB customers not from the promotion", "%", "H1 2025–H1 2026", ["np_ch26", "np_ch25"], "2.1% − 2.0%", "np_ch26 - np_ch25", "waterfall step")
der("promo_mix", "2", "Churn added by the promotion cohort (SMB churn minus non-promotion churn)", "%", "H1 2026", ["smb_ch26", "np_ch26"], "3.1% − 2.1%", "smb_ch26 - np_ch26", "waterfall step")
der("sh_rise", "2", "Share of the SMB churn rise explained by the promotion cohort", "%", "H1 2025–H1 2026", ["promo_mix", "smb_ch26", "smb_ch25"], "1.0 pp ÷ 1.1 pp", "promo_mix / (smb_ch26 - smb_ch25)", "sidebar big number; title")
der("promo_cs", "2", "Promotion cohort as share of SMB customers", "%", "mid-2026", ["promo_c", "smb_c"], "2,100 ÷ 5,900", "promo_c / smb_c", "sidebar bullet")

# ---------- slide 4: CFO plan sizing ----------
A4 = ["Renewal shares from the briefing pack: all SMB, 85% of mid-market and 40% of enterprise ARR renew in 2027",
      "The 7% caps apply to the same 60% share of renewing enterprise ARR as of the whole enterprise book",
      "No extra churn caused by the rise is netted out, so this is an upper bound",
      "The full rise counts in ARR for every contract renewed by December 2027"]
der("cfo_calc", "4", "12% on all ARR (the CFO's figure)", "$M", "2027", ["arr", "cfo_pct"], "$86.0M × 12% = $10.3M (matches the CFO's $10.3M)", "arr * cfo_pct", "waterfall start; title")
der("mm_nonren", "4", "12% on mid-market ARR that does not renew in 2027", "$M", "2027", ["mm_arr", "mm_ren", "cfo_pct"], "−$41.0M × 15% × 12%", "0 - mm_arr * (1 - mm_ren) * cfo_pct", "waterfall step")
der("ent_nonren", "4", "12% on enterprise ARR that does not renew in 2027", "$M", "2027", ["ent_arr", "ent_ren", "cfo_pct"], "−$24.0M × 60% × 12%", "0 - ent_arr * (1 - ent_ren) * cfo_pct", "waterfall step")
der("capcut_pos", "4", "Uplift lost where 7% caps apply to renewing enterprise ARR", "$M", "2027", ["ent_arr", "ent_ren", "cap_share", "cfo_pct", "cap7"],
    "$24.0M × 40% × 60% × (12% − 7%)", "ent_arr * ent_ren * cap_share * (cfo_pct - cap7)", "basis strip", assumptions=A4[1:2])
der("capcut", "4", "Enterprise caps (negative step)", "$M", "2027", ["capcut_pos"], "−$0.29M", "0 - capcut_pos", "waterfall step", assumptions=A4[1:2])
der("renew27", "4", "ARR renewing in 2027", "$M", "2027", ["smb_arr", "mm_arr", "mm_ren", "ent_arr", "ent_ren"],
    "$21.0M (all SMB ARR renews in 2027) + $41.0M × 85% + $24.0M × 40%", "smb_arr + mm_arr * mm_ren + ent_arr * ent_ren", "basis strip")
der("ren_sh", "4", "Share of ARR renewing in 2027", "%", "2027", ["renew27", "arr"], "$65.5M ÷ $86.0M", "renew27 / arr", "sidebar bullet; exec summary")
der("reach12", "4", "ARR a 12% rise could add in 2027, before churn", "$M", "2027", ["renew27", "cfo_pct", "capcut_pos"],
    "$65.5M × 12% − $0.29M", "renew27 * cfo_pct - capcut_pos", "waterfall end; title", assumptions=A4)
der("smb_up12", "4", "12% of SMB ARR (all of it renews in 2027)", "$M", "2027", ["smb_arr", "cfo_pct"], "$21.0M × 12%", "smb_arr * cfo_pct", "sidebar basis")
der("sh_smb12", "4", "SMB share of the 12% plan's reachable ARR gain", "%", "2027", ["smb_up12", "reach12"], "$2.5M ÷ $7.6M", "smb_up12 / reach12", "sidebar row")
der("tgt", "4", "ARR growth needed for the 15% objective", "$M", "2027", ["arr", "grow"], "$86.0M × 15%", "arr * grow", "sidebar row; options")
der("sh_tgt12", "4", "Share of the 15% growth target the 12% plan could cover", "%", "2027", ["reach12", "tgt"], "$7.6M ÷ $12.9M", "reach12 / tgt", "sidebar row; options table")
der("mm_nonren_sh", "4", "Share of mid-market ARR not renewing in 2027", "%", "2027", ["mm_ren"], "100% − 85%", "1 - mm_ren", "sidebar bullet")
der("ent_nonren_sh", "4", "Share of enterprise ARR not renewing in 2027", "%", "2027", ["ent_ren"], "100% − 40%", "1 - ent_ren", "sidebar bullet")

# ---------- slide 5: Inkwell ----------
der("pal_smb12", "5", "Palisade SMB price after a 12% rise", "$", "2027", ["pal15", "cfo_pct"], "$15 × 1.12", "pal15 * (1 + cfo_pct)", "panel bar", definition="per user per month")
der("ratio12", "5", "Palisade SMB price after 12% rise as a multiple of Inkwell Starter", "x", "2027", ["pal_smb12", "ink9"], "$16.80 ÷ $9", "pal_smb12 / ink9", "panel delta")
der("win_d", "5", "Change in SMB win rate against Inkwell", "pp", "H1 2025–H1 2026", ["win26", "win25"], "(38% − 51%) × 100", "(win26 - win25) * 100", "panel delta")

# ---------- slide 6: 2023 increase ----------
der("bump23", "6", "Rise in SMB monthly churn after the 2023 increase", "pp", "2023", ["ch23b", "ch23a"], "(2.3% − 1.8%) × 100", "(ch23b - ch23a) * 100", "KPI driver")
der("loss23", "6", "SMB ARR a repeat of the 2023 churn bump would cost on today's base", "$M", "2027", ["smb_arr", "ch23b", "ch23a"],
    "$21.0M × 0.5 pp × 6 months", "smb_arr * (ch23b - ch23a) * 6", "KPI driver",
    assumptions=["The 2023 reaction repeats: 0.5 percentage points more monthly churn for six months", "Lost customers carry average SMB ARR"])

# ---------- slide 7: segment health ----------
der("mm_as", "7", "Mid-market share of ARR", "%", "mid-2026", ["mm_arr", "arr"], "$41.0M ÷ $86.0M", "mm_arr / arr", "callout")

# ---------- slide 8 ----------
der("conv_gap", "8", "Conversion gap, +10% price against control", "pp", "2024 test", ["conv_t", "conv_c"], "(23.1% − 23.6%) × 100", "(conv_t - conv_c) * 100", "KPI driver")

# ---------- slide 9: targeted plan sizing ----------
A9 = ["Renewal shares from the briefing pack: 85% of mid-market and 40% of enterprise ARR renew in 2027",
      "The 7% caps cover the same 60% share of renewing enterprise ARR as of the whole enterprise book; uncapped enterprise rises 10%",
      "Renewing customers churn at today's rates; no extra churn from the rise is netted out",
      "The full rise counts in ARR for every contract renewed by December 2027"]
der("mm_renarr", "9", "Mid-market ARR renewing in 2027", "$M", "2027", ["mm_arr", "mm_ren"], "$41.0M × 85%", "mm_arr * mm_ren", "equation caption")
der("ent_unc_arr", "9", "Uncapped enterprise ARR renewing in 2027", "$M", "2027", ["ent_arr", "ent_ren", "cap_share"], "$24.0M × 40% × 40%", "ent_arr * ent_ren * (1 - cap_share)", "equation caption", assumptions=A9[1:2])
der("ent_cap_arr", "9", "Capped enterprise ARR renewing in 2027", "$M", "2027", ["ent_arr", "ent_ren", "cap_share"], "$24.0M × 40% × 60%", "ent_arr * ent_ren * cap_share", "equation caption", assumptions=A9[1:2])
der("mm_up10", "9", "ARR added by +10% on mid-market renewals", "$M", "2027", ["mm_renarr", "mmtest"], "$34.85M × 10%", "mm_renarr * mmtest", "equation term", assumptions=A9)
der("ent_unc", "9", "ARR added by +10% on uncapped enterprise renewals", "$M", "2027", ["ent_unc_arr", "mmtest"], "$3.84M × 10%", "ent_unc_arr * mmtest", "equation term", assumptions=A9)
der("ent_cap", "9", "ARR added by +7% on capped enterprise renewals", "$M", "2027", ["ent_cap_arr", "cap7"], "$5.76M × 7%", "ent_cap_arr * cap7", "equation term", assumptions=A9)
der("rec_total", "9", "ARR the targeted rise would add in 2027, before churn", "$M", "2027", ["mm_up10", "ent_unc", "ent_cap"], "$3.49M + $0.38M + $0.40M", "mm_up10 + ent_unc + ent_cap", "equation result; title", assumptions=A9)
der("np_arr", "9", "Non-promotion SMB ARR", "$M", "mid-2026", ["smb_arr", "promo_arr"], "$21.0M − $4.4M", "smb_arr - promo_arr", "assumption text")
der("smb_up8", "9", "ARR an 8% rise on non-promotion SMB would add if the test passes", "$M", "2027", ["np_arr", "p23"], "$16.6M × 8%", "np_arr * p23", "assumption text; callout",
    assumptions=["The SMB renewal test confirms churn stays within the 2023 pattern", "Applied to all non-promotion SMB ARR for a full renewal cycle", "Promotion-cohort customers are excluded until activated"])

# ---------- slide 10: options ----------
der("sh_tgt_rec", "10", "Share of the 15% growth target the targeted rise covers", "%", "2027", ["rec_total", "tgt"], "$4.3M ÷ $12.9M", "rec_total / tgt", "options table; exec summary")
der("gap_ab", "10", "Uplift the targeted option gives up against the 12% plan, before churn", "$M", "2027", ["reach12", "rec_total"], "$7.6M − $4.3M", "reach12 - rec_total", "basis strip",
    assumptions=["Both options sized before any churn effect of the rise", "Same renewal calendar and cap assumptions as pages 8 and 15"])

# ---------- slide 11: onboarding ----------
der("cs_tgt", "11", "SMB monthly churn if halved, as Customer Success promises", "%", "within two quarters", ["smb_ch26", "cs_half"], "3.1% × 50%", "smb_ch26 * (1 - cs_half)", "scenario bar")
der("cut_sh", "11", "Cut in SMB churn if the promotion cohort churned like other SMB", "%", "scenario", ["smb_ch26", "np_ch26"], "(3.1% − 2.1%) ÷ 3.1%", "(smb_ch26 - np_ch26) / smb_ch26", "sidebar row",
    assumptions=["Activated promotion customers churn at the 2.1% rate of other SMB customers", "Other SMB customers keep their H1 2026 churn rate", "Segment mix stays at mid-2026 levels"])

json.dump(DPS, open(ROOT / "build" / "dps.json", "w"), indent=1)
print(len(DPS), "data points")
