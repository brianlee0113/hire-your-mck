"""Data points for the Palisade Docs pricing deck. Every number comes from the briefing pack (u1),
from parameters chosen on the user's behalf (u2), or is calculated from those (s0)."""

DPS = []


def U(id, slide, label, value, unit, excerpt, locator, period=None, src="u1", used_in=None):
    d = {"id": id, "slide_id": slide, "label": label, "value": value, "unit": unit, "source_id": src,
         "locator": locator}
    if excerpt:
        d["excerpt"] = excerpt
    if period:
        d["period"] = period
    if used_in:
        d["used_in"] = used_in
    DPS.append(d)


def D(id, slide, label, value, unit, calc, derived_from, formula, est=False, assumptions=None, period=None):
    d = {"id": id, "slide_id": slide, "label": label, "value": value, "unit": unit, "source_id": "s0",
         "derived_from": derived_from, "formula": formula, "calc": calc}
    if period:
        d["period"] = period
    if est:
        d["estimate"] = True
        d["assumptions"] = assumptions
    DPS.append(d)


T1 = "Table 1. Segments, mid-2026"
T2 = "Table 2. Main churn reason, exit survey"

# ---------------------------------------------------------------- briefing pack, as given
U("arr", "3c1", "Palisade ARR, mid-2026", 86.0, "$M", "ARR is $86.0M from 7,400 customers in three segments.", "§1 Context", "mid-2026")
U("ncust", "1a1", "Palisade customers, mid-2026", 7400, "customers", "ARR is $86.0M from 7,400 customers in three segments.", "§1 Context", "mid-2026")
U("smbc", "1a1", "SMB customers", 5900, "customers", 'Table 1 "SMB"; column Customers = "5,900"', T1, "mid-2026")
U("mmc", "1a1", "Mid-market customers", 1350, "customers", 'Table 1 "Mid-market"; column Customers = "1,350"', T1, "mid-2026")
U("entc", "1a1", "Enterprise customers", 150, "customers", 'Table 1 "Enterprise"; column Customers = "150"', T1, "mid-2026")
U("smbarr", "3b1", "SMB ARR", 21.0, "$M", 'Table 1 "SMB"; column ARR, $M = "21.0"', T1, "mid-2026")
U("mmarr", "2a1", "Mid-market ARR", 41.0, "$M", 'Table 1 "Mid-market"; column ARR, $M = "41.0"', T1, "mid-2026")
U("entarr", "2b1", "Enterprise ARR", 24.0, "$M", 'Table 1 "Enterprise"; column ARR, $M = "24.0"', T1, "mid-2026")
U("smb25", "1a1", "SMB monthly logo churn, H1 2025", 0.020, "%", 'Table 1 "SMB"; column Monthly logo churn H1 2025 = "2.0%"', T1, "H1 2025")
U("smb26", "1a1", "SMB monthly logo churn, H1 2026", 0.031, "%", 'Table 1 "SMB"; column Monthly logo churn H1 2026 = "3.1%"', T1, "H1 2026")
U("mm25", "1a1", "Mid-market monthly logo churn, H1 2025", 0.006, "%", 'Table 1 "Mid-market"; column Monthly logo churn H1 2025 = "0.6%"', T1, "H1 2025")
U("mm26", "1a1", "Mid-market monthly logo churn, H1 2026", 0.008, "%", 'Table 1 "Mid-market"; column Monthly logo churn H1 2026 = "0.8%"', T1, "H1 2026")
U("ent25", "1a1", "Enterprise monthly logo churn, H1 2025", 0.002, "%", 'Table 1 "Enterprise"; column Monthly logo churn H1 2025 = "0.2%"', T1, "H1 2025")
U("ent26", "1a1", "Enterprise monthly logo churn, H1 2026", 0.002, "%", 'Table 1 "Enterprise"; column Monthly logo churn H1 2026 = "0.2%"', T1, "H1 2026")
U("nrrs", "2a1", "SMB net revenue retention, trailing 12 months", 0.94, "%", 'Table 1 "SMB"; column Net revenue retention (trailing 12 months) = "94%"', T1, "trailing 12 months to mid-2026")
U("nrrm", "2a1", "Mid-market net revenue retention, trailing 12 months", 1.12, "%", 'Table 1 "Mid-market"; column Net revenue retention (trailing 12 months) = "112%"', T1, "trailing 12 months to mid-2026")
U("nrre", "2b1", "Enterprise net revenue retention, trailing 12 months", 1.18, "%", 'Table 1 "Enterprise"; column Net revenue retention (trailing 12 months) = "118%"', T1, "trailing 12 months to mid-2026")
EX_PROMO = ("The promotion brought in 2,100 SMB customers who are still counted in the base above "
            "(about $4.4M of ARR at full price).")
U("promoc", "1b2", "Promotion-cohort customers still in the base", 2100, "customers", EX_PROMO, "§6 The 2025 SMB promotion; base as in Table 1, mid-2026", "mid-2026")
U("promoarr", "1b2", "Promotion-cohort ARR at full price", 4.4, "$M", EX_PROMO, "§6 The 2025 SMB promotion; base as in Table 1, mid-2026", "mid-2026")
U("disc", "1b2", "Promotion discount for the first six months", 0.5, "%",
  "From February to August 2025, new self-serve SMB customers got 50% off for their first six months.", "§6 The 2025 SMB promotion", "Feb–Aug 2025")
EX_ACT = ("Share of new customers who sent at least five documents in their first month: 41% for the promotion cohort, "
          "72% for other cohorts.")
U("actp", "4b1", "Promotion cohort sending at least five documents in month one", 0.41, "%", EX_ACT, "§6 The 2025 SMB promotion")
U("acto", "4b1", "Other cohorts sending at least five documents in month one", 0.72, "%", EX_ACT, "§6 The 2025 SMB promotion")
EX_NP = ("Monthly churn in H1 2026 for SMB customers who did **not** come through the promotion: 2.1% "
         "(H1 2025 for the same kind of customers: 2.0%).")
U("np26", "1b1", "Non-promotion SMB monthly churn, H1 2026", 0.021, "%", EX_NP, "§6 The 2025 SMB promotion", "H1 2026")
U("np25", "1b1", "Non-promotion SMB monthly churn, H1 2025", 0.020, "%", EX_NP, "§6 The 2025 SMB promotion", "H1 2025")
U("ps25", "1c1", "All SMB churners citing price, H1 2025", 0.19, "%", 'Table 2 "all SMB churners H1 2025"; column Share citing price = "19%"', T2, "H1 2025")
U("ps26", "1c1", "All SMB churners citing price, H1 2026", 0.34, "%", 'Table 2 "all SMB churners H1 2026"; column Share citing price = "34%"', T2, "H1 2026")
U("psp", "1c1", "Promotion-cohort churners citing price, H1 2026", 0.52, "%", 'Table 2 "promo-cohort churners H1 2026"; column Share citing price = "52%"', T2, "H1 2026")
U("psn", "1c1", "Non-promotion SMB churners citing price, H1 2026", 0.18, "%", 'Table 2 "non-promo SMB churners H1 2026"; column Share citing price = "18%"', T2, "H1 2026")
U("inkst", "1c1", "Inkwell Starter plan price", 9, "$ per user per month",
  "Inkwell launched a Starter plan at $9 per user per month in October 2025.", "§7 Competitor", "October 2025")
EX_PR = "Palisade's SMB plan is $15 per user per month; Business plan $29; Inkwell Pro $24."
U("palsmb", "2d1", "Palisade SMB plan price", 15, "$ per user per month", EX_PR, "§7 Competitor")
U("palbus", "2d1", "Palisade Business plan price", 29, "$ per user per month", EX_PR, "§7 Competitor")
U("inkpro", "2d1", "Inkwell Pro plan price", 24, "$ per user per month", EX_PR, "§7 Competitor")
EX_WIN = ("Palisade's win rate in SMB deals where Inkwell was considered fell from 51% (H1 2025) to 38% (H1 2026).")
U("win25", "2d1", "SMB win rate where Inkwell was considered, H1 2025", 0.51, "%", EX_WIN, "§7 Competitor", "H1 2025")
U("win26", "2d1", "SMB win rate where Inkwell was considered, H1 2026", 0.38, "%", EX_WIN, "§7 Competitor", "H1 2026")
U("seats", "2d1", "Deal size above which Inkwell has not been seen", 200, "seats",
  "Inkwell has not been seen in mid-market or enterprise deals with more than 200 seats.", "§7 Competitor")
EX_23 = ("2023 SMB price increase: +8% at renewal. SMB monthly churn rose from 1.8% to 2.3% for six months, "
         "then settled at 1.9%.")
U("p23", "2c1", "2023 SMB price increase at renewal", 0.08, "%", EX_23, "§8 Pricing history and tests", "2023")
U("c23a", "2c1", "SMB monthly churn before the 2023 rise", 0.018, "%", EX_23, "§8 Pricing history and tests", "2023")
U("c23b", "2c1", "SMB monthly churn in the six months after the 2023 rise", 0.023, "%", EX_23, "§8 Pricing history and tests", "2023")
U("c23c", "2c1", "SMB monthly churn once settled after the 2023 rise", 0.019, "%", EX_23, "§8 Pricing history and tests", "2023")
EX_24 = ("2024 mid-market test: +10% list price for new mid-market sign-ups for three months: conversion 23.1% "
         "against 23.6% for the control group (difference not statistically significant).")
U("mmtest", "2a1", "List price rise in the 2024 mid-market test", 0.10, "%", EX_24, "§8 Pricing history and tests", "2024")
U("convt", "2a1", "Conversion of new mid-market sign-ups at +10%", 0.231, "%", EX_24, "§8 Pricing history and tests", "2024")
U("convc", "2a1", "Conversion of the control group", 0.236, "%", EX_24, "§8 Pricing history and tests", "2024")
EX_CAP = "60% of enterprise ARR is under contracts that cap annual price increases at 7%."
U("capsh", "2b1", "Share of enterprise ARR under capped contracts", 0.60, "%", EX_CAP, "§8 Pricing history and tests")
U("cap7", "2b1", "Annual price-increase cap in enterprise contracts", 0.07, "%", EX_CAP, "§8 Pricing history and tests")
EX_REN = "40% of enterprise ARR renews in 2027, as does 85% of mid-market ARR and all SMB ARR."
U("entren", "2b1", "Share of enterprise ARR renewing in 2027", 0.40, "%", EX_REN, "§8 Pricing history and tests", "2027")
U("mmren", "2a1", "Share of mid-market ARR renewing in 2027", 0.85, "%", EX_REN, "§8 Pricing history and tests", "2027")
U("low3", "4b1", "Churn of SMB customers sending under five documents in month one, compared with the rest", 3, "x",
  "SMB customers who send fewer than five documents in their first month churn at about three times the rate of those who send more.",
  "§9 Product and customer evidence")
EX_CFO = "Raise list prices 12% on every plan at renewal from January 2027. That is $10.3M of ARR."
U("cfo12", "3a1", "CFO's proposed rise on every plan", 0.12, "%", EX_CFO, "§4 Current views (CFO)", "2027")
U("cfo103", "3a1", "CFO's stated ARR gain", 10.3, "$M", EX_CFO, "§4 Current views (CFO)", "2027")
U("tgt", "3c1", "2027 ARR growth target", 0.15, "%", "Grow ARR at least 15% in 2027 (from $86.0M).", "§3 Objectives and constraints", "2027")
U("nrrfloor", "3c3", "Net revenue retention floor", 1.00, "%", "Keep net revenue retention above 100% overall.", "§3 Objectives and constraints")
U("dash14", "1a2", "Board dashboard churn, earlier reading", 0.014, "%", 'Board dashboard (Q2 2026): "Monthly churn: 1.4% → 2.3%."', "§10 Other material")
U("dash23", "1a2", "Board dashboard churn, latest reading", 0.023, "%", 'Board dashboard (Q2 2026): "Monthly churn: 1.4% → 2.3%."', "§10 Other material")

# ---------------------------------------------------------------- choices made on the user's behalf
U("h2", "3c2", "Share of 2027 SMB renewals falling after July", 0.5, "%", None,
  "Plan parameter chosen on the user's behalf: renewals assumed spread evenly through 2027", src="u2")

# ---------------------------------------------------------------- derived: section 1
D("smbrise", "L1", "Rise in SMB monthly churn, H1 2025 to H1 2026", 1.1, "pp", "(smb26 - smb25) * 100", ["smb26", "smb25"], "(3.1% − 2.0%) × 100")
D("mmrise", "1a1", "Rise in mid-market monthly churn, H1 2025 to H1 2026", 0.2, "pp", "(mm26 - mm25) * 100", ["mm26", "mm25"], "(0.8% − 0.6%) × 100")
D("smblost", "1b2", "SMB customers lost a month, H1 2026", 182.9, "customers a month", "smbc * smb26", ["smbc", "smb26"], "5,900 × 3.1%")
D("alllost", "1a1", "All customers lost a month, H1 2026", 194.0, "customers a month", "smbc * smb26 + mmc * mm26 + entc * ent26",
  ["smbc", "smb26", "mmc", "mm26", "entc", "ent26"], "5,900 × 3.1% + 1,350 × 0.8% + 150 × 0.2%")
D("smbshch", "1a1", "SMB share of customers lost a month, H1 2026", 0.94, "%", "smblost / alllost", ["smblost", "alllost", "smb26", "mm26", "ent26"], "182.9 ÷ 194.0")
D("cw25", "1a2", "Customer-weighted monthly logo churn, H1 2025", 0.017, "%", "(smbc * smb25 + mmc * mm25 + entc * ent25) / ncust",
  ["smbc", "smb25", "mmc", "mm25", "entc", "ent25", "ncust"], "Σ customers × churn ÷ 7,400 (mid-2026 counts)")
D("cw26", "1a2", "Customer-weighted monthly logo churn, H1 2026", 0.026, "%", "alllost / ncust", ["alllost", "ncust"], "194.0 ÷ 7,400")
D("aw25", "1a2", "ARR-weighted monthly logo churn, H1 2025", 0.0083, "%", "(smbarr * smb25 + mmarr * mm25 + entarr * ent25) / arr",
  ["smbarr", "smb25", "mmarr", "mm25", "entarr", "ent25", "arr"], "Σ ARR × churn ÷ $86.0M")
D("aw26", "1a2", "ARR-weighted monthly logo churn, H1 2026", 0.0119, "%", "(smbarr * smb26 + mmarr * mm26 + entarr * ent26) / arr",
  ["smbarr", "smb26", "mmarr", "mm26", "entarr", "ent26", "arr"], "Σ ARR × churn ÷ $86.0M")
D("npc", "1b1", "Non-promotion SMB customers", 3800, "customers", "smbc - promoc", ["smbc", "promoc"], "5,900 − 2,100")
D("nplost", "1b2", "Non-promotion SMB customers lost a month, H1 2026", 79.8, "customers a month", "npc * np26", ["npc", "np26"], "3,800 × 2.1%")
D("promolost", "1b2", "Promotion-cohort customers lost a month, H1 2026", 103.1, "customers a month", "smblost - nplost", ["smblost", "nplost"], "182.9 − 79.8")
D("promoch", "1b1", "Implied monthly churn of the promotion cohort, H1 2026", 0.049, "%", "promolost / promoc", ["promolost", "promoc", "smb26", "np26"],
  "(3.1% × 5,900 − 2.1% × 3,800) ÷ 2,100")
D("riseshare", "L1", "Share of the SMB churn rise from the promotion cohort", 0.91, "%", "(smb26 - np26) / (smb26 - smb25)", ["smb26", "np26", "smb25"],
  "(3.1% − 2.1%) ÷ (3.1% − 2.0%): the rise left if all SMB churned at the non-promotion rate")
D("nprise", "1b1", "Rise in non-promotion SMB churn, H1 2025 to H1 2026", 0.1, "pp", "(np26 - np25) * 100", ["np26", "np25"], "(2.1% − 2.0%) × 100")
D("promoshc", "1b2", "Promotion cohort as a share of SMB customers", 0.36, "%", "promoc / smbc", ["promoc", "smbc"], "2,100 ÷ 5,900")
D("promoshch", "1b2", "Promotion cohort as a share of SMB customers lost a month", 0.56, "%", "promolost / smblost", ["promolost", "smblost"], "103.1 ÷ 182.9")
D("surveysh", "1b2", "Promotion share of SMB exit-survey answers implied by the price-reason mix", 0.47, "%", "(ps26 - psn) / (psp - psn)", ["ps26", "psn", "psp"],
  "(34% − 18%) ÷ (52% − 18%): the mix s that solves 52% × s + 18% × (1 − s) = 34%")
D("promox", "4b1", "Promotion-cohort churn as a multiple of non-promotion SMB churn", 2.33, "x", "promoch / np26", ["promoch", "np26"], "4.9% ÷ 2.1%")

# ---------------------------------------------------------------- derived: section 2
D("convgap", "2a1", "Conversion gap, +10% test against control", -0.5, "pp", "(convt - convc) * 100", ["convt", "convc"], "(23.1% − 23.6%) × 100")
D("mmrenarr", "2a1", "Mid-market ARR renewing in 2027", 34.9, "$M", "mmarr * mmren", ["mmarr", "mmren"], "$41.0M × 85%")
D("entrenarr", "2b1", "Enterprise ARR renewing in 2027", 9.6, "$M", "entarr * entren", ["entarr", "entren"], "$24.0M × 40%")
D("entnot", "2b1", "Enterprise ARR not renewing in 2027", 14.4, "$M", "entarr * (1 - entren)", ["entarr", "entren"], "$24.0M × 60%")
D("entnotsh", "3a1", "Share of enterprise ARR not renewing in 2027", 0.6, "%", "1 - entren", ["entren"], "1 − 40%")
D("entcap", "2b1", "Enterprise ARR renewing in 2027 under a 7% cap", 5.76, "$M", "entrenarr * capsh", ["entrenarr", "capsh"], "$9.6M × 60%", True,
  ["The 60% capped share of enterprise ARR applies equally to the contracts renewing in 2027 (the pack gives no split)"])
D("entunc", "2b1", "Enterprise ARR renewing in 2027 without a cap", 3.84, "$M", "entrenarr * (1 - capsh)", ["entrenarr", "capsh"], "$9.6M × 40%", True,
  ["The 60% capped share of enterprise ARR applies equally to the contracts renewing in 2027 (the pack gives no split)"])
D("capgap", "2b1", "Gap between the CFO's rise and the enterprise cap", 5, "pp", "(cfo12 - cap7) * 100", ["cfo12", "cap7"], "(12% − 7%) × 100")
D("spike23", "2c1", "Extra SMB churn in the six months after the 2023 rise", 0.5, "pp", "(c23b - c23a) * 100", ["c23b", "c23a"], "(2.3% − 1.8%) × 100")
D("settle23", "2c1", "Lasting extra SMB churn after the 2023 rise", 0.1, "pp", "(c23c - c23a) * 100", ["c23c", "c23a"], "(1.9% − 1.8%) × 100")
D("inkdisc", "2d1", "Inkwell Starter price against Palisade's SMB plan", -0.4, "%", "inkst / palsmb - 1", ["inkst", "palsmb"], "$9 ÷ $15 − 1")
D("windrop", "2d1", "Change in SMB win rate where Inkwell was considered", -13, "pp", "(win26 - win25) * 100", ["win26", "win25"], "(38% − 51%) × 100")

# ---------------------------------------------------------------- derived: section 3
D("cfofull", "3a1", "CFO plan as stated: 12% on all ARR", 10.32, "$M", "arr * cfo12", ["arr", "cfo12"], "$86.0M × 12% (the CFO's $10.3M)")
D("mmnr", "3a1", "Lost from the CFO plan: mid-market ARR not renewing in 2027", -0.74, "$M", "0 - mmarr * (1 - mmren) * cfo12", ["mmarr", "mmren", "cfo12"], "−$41.0M × 15% × 12%")
D("entnr", "3a1", "Lost from the CFO plan: enterprise ARR not renewing in 2027", -1.73, "$M", "0 - entnot * cfo12", ["entnot", "cfo12"], "−$14.4M × 12%")
D("entcapl", "3a1", "Lost from the CFO plan: 7% caps on renewing enterprise ARR", -0.29, "$M", "0 - entrenarr * capsh * (cfo12 - cap7)",
  ["entrenarr", "capsh", "cfo12", "cap7"], "−$9.6M × 60% × (12% − 7%)")
D("reach12", "3a1", "ARR the CFO plan can add in 2027", 7.57, "$M", "cfofull + mmnr + entnr + entcapl", ["cfofull", "mmnr", "entnr", "entcapl"], "$10.3M − $0.7M − $1.7M − $0.3M")
D("notreachsh", "3a1", "Share of the CFO's figure that cannot land in 2027", 0.27, "%", "1 - reach12 / cfofull", ["reach12", "cfofull"], "1 − $7.6M ÷ $10.3M")
D("smbg12", "3b1", "SMB part of the CFO plan: 12% on SMB ARR, all renewing in 2027", 2.52, "$M", "smbarr * cfo12", ["smbarr", "cfo12"], "$21.0M × 12%")
D("smbshare12", "L3", "SMB share of the ARR the CFO plan can add in 2027", 0.33, "%", "smbg12 / reach12", ["smbg12", "reach12"], "$2.5M ÷ $7.6M")
D("smbnew", "3b1", "SMB ARR at the new price", 23.52, "$M", "smbarr * (1 + cfo12)", ["smbarr", "cfo12"], "$21.0M × 1.12")
ASM_2023 = ["SMB customers react to the 2027 rise as they did to the 2023 rise: 0.5 percentage points more churn for six months, then 0.1 for the rest of the year",
            "The reaction to a 12% rise is no larger than to the 8% rise of 2023 (likely an understatement now that Inkwell sells a $9 plan)",
            "Lost customers are valued at the new price for a full year"]
D("xloss", "3b1", "Extra share of SMB customers lost in the first year at the 2023 reaction", 0.036, "%", "(c23b - c23a) * 6 + (c23c - c23a) * 6",
  ["c23b", "c23a", "c23c"], "0.5 pp × 6 months + 0.1 pp × 6 months", True, ASM_2023)
D("be", "3b1", "Share of SMB customers the 12% rise could lose before it stops paying", 0.107, "%", "smbg12 / smbnew", ["smbg12", "smbnew"], "$2.52M ÷ $23.52M")
D("bemult", "3b1", "Break-even loss as a multiple of the 2023 reaction", 3.0, "x", "be / xloss", ["be", "xloss"], "10.7% ÷ 3.6%", True, ASM_2023)
D("smbloss12", "3b1", "SMB ARR lost to the 12% rise at the 2023 reaction", 0.85, "$M", "smbnew * xloss", ["smbnew", "xloss"], "$23.52M × 3.6%", True, ASM_2023)
D("smbnet12", "3b1", "Net SMB gain from the 12% rise at the 2023 reaction", 1.67, "$M", "smbg12 - smbloss12", ["smbg12", "smbloss12"], "$2.52M − $0.85M", True, ASM_2023)

ASM_PLAN = ["No extra mid-market or enterprise churn at the higher price; the 2024 test covered new sign-ups only, so Q1 2027 renewals are the check",
            "Enterprise caps apply to the same 60% share of the ARR renewing in 2027",
            "SMB renewals are spread evenly, so half fall after July; the promotion cohort gets no rise in 2027",
            "The SMB rise is charged the 2023 churn reaction, the same charge as the CFO plan's SMB rise",
            "Rises apply at renewal at the rates shown, with no extra discounting"]
D("mmg12", "3c2", "ARR added by a 12% mid-market rise at 2027 renewals", 4.19, "$M", "mmrenarr * cfo12", ["mmrenarr", "cfo12"], "$34.9M × 12%", True, ASM_PLAN)
D("entg12", "2b1", "ARR added by enterprise rises at 2027 renewals: 7% capped, 12% uncapped", 0.86, "$M", "entcap * cap7 + entunc * cfo12",
  ["entcap", "cap7", "entunc", "cfo12"], "$5.8M × 7% + $3.8M × 12%", True, ASM_PLAN)
D("mmentg", "3c1", "ARR added by the mid-market and enterprise rises in 2027", 5.05, "$M", "mmg12 + entg12", ["mmg12", "entg12"], "$4.19M + $0.86M", True, ASM_PLAN)
D("npsmbarr", "3c2", "Non-promotion SMB ARR", 16.6, "$M", "smbarr - promoarr", ["smbarr", "promoarr"], "$21.0M − $4.4M")
D("smbg", "3c2", "ARR added by an 8% non-promotion SMB rise from July 2027, before churn", 0.66, "$M", "npsmbarr * h2 * p23", ["npsmbarr", "h2", "p23"], "$16.6M × 50% × 8%", True, ASM_PLAN)
D("smbloss8", "3c2", "SMB ARR lost to the 8% rise at the 2023 reaction", 0.32, "$M", "npsmbarr * h2 * (1 + p23) * xloss", ["npsmbarr", "h2", "p23", "xloss"],
  "$16.6M × 50% × 1.08 × 3.6%", True, ASM_PLAN + ASM_2023)
D("smbnet8", "3c1", "Net ARR from the SMB rise after the test, at the 2023 reaction", 0.34, "$M", "smbg - smbloss8", ["smbg", "smbloss8"], "$0.66M − $0.32M", True, ASM_PLAN + ASM_2023)
D("recg", "3c2", "ARR added by the recommended price plan in 2027", 5.39, "$M", "mmg12 + entg12 + smbg - smbloss8", ["mmg12", "entg12", "smbg", "smbloss8"],
  "$4.19M + $0.86M + $0.66M − $0.32M", True, ASM_PLAN + ASM_2023)
D("mmsh", "3c2", "Mid-market share of the recommended plan's ARR gain", 0.78, "%", "mmg12 / recg", ["mmg12", "recg"], "$4.19M ÷ $5.39M", True, ASM_PLAN)
D("nrrall", "3c1", "ARR-weighted net revenue retention, trailing 12 months", 1.0928, "%", "(smbarr * nrrs + mmarr * nrrm + entarr * nrre) / arr",
  ["smbarr", "nrrs", "mmarr", "nrrm", "entarr", "nrre", "arr"], "($21.0M × 94% + $41.0M × 112% + $24.0M × 118%) ÷ $86.0M")
ASM_BASE = ["$86.0M (mid-2026) is taken as the 2027 starting base, as the 15% target does",
            "Net revenue retention in 2027 repeats the trailing-12-month rate of each segment, weighted by ARR",
            "The trailing rate contains no price rise (none was made in 2025–26), so the price plan is added on top",
            "New-customer ARR is not counted; the pack has no bookings plan"]
D("base27", "3c1", "2027 ARR from existing customers before any price change", 93.98, "$M", "arr * nrrall", ["arr", "nrrall"], "$86.0M × 109.3%", True, ASM_BASE)
D("nrrgain", "3c1", "ARR added by net retention at 2026 rates", 7.98, "$M", "base27 - arr", ["base27", "arr"], "$93.98M − $86.0M", True, ASM_BASE)
D("arr27", "3c1", "2027 ARR with the recommended plan, before new customers", 99.37, "$M", "base27 + recg", ["base27", "recg"], "$93.98M + $5.39M", True, ASM_BASE + ASM_PLAN)
D("tgtarr", "3c1", "2027 ARR at 15% growth", 98.9, "$M", "arr * (1 + tgt)", ["arr", "tgt"], "$86.0M × 1.15")
D("nrr1pp", "3c1", "2027 ARR moved by one percentage point of net retention", 0.86, "$M", "arr / 100", ["arr"], "$86.0M × 1%")
D("arr27cfo", "3c3", "2027 ARR with the CFO plan at the 2023 SMB reaction, before new customers", 100.70, "$M", "base27 + reach12 - smbloss12",
  ["base27", "reach12", "smbloss12"], "$93.98M + $7.57M − $0.85M", True, ASM_BASE + ASM_2023)
D("cfoextra", "3c3", "Extra 2027 ARR of the CFO plan over the recommended plan at the 2023 SMB reaction", 1.33, "$M", "arr27cfo - arr27", ["arr27cfo", "arr27"], "$100.70M − $99.37M", True, ASM_BASE + ASM_2023 + ASM_PLAN)
D("holdgap", "3c3", "Shortfall to the target if all prices are held", 4.92, "$M", "tgtarr - base27", ["tgtarr", "base27"], "$98.9M − $93.98M", True, ASM_BASE)
D("nrr27b", "3c3", "2027 net revenue retention with the recommended plan", 1.16, "%", "arr27 / arr", ["arr27", "arr"], "$99.37M ÷ $86.0M", True, ASM_BASE + ASM_PLAN)
D("nrr27a", "3c3", "2027 net revenue retention with the CFO plan at the 2023 SMB reaction", 1.17, "%", "arr27cfo / arr", ["arr27cfo", "arr"], "$100.70M ÷ $86.0M", True, ASM_BASE + ASM_2023)
D("arr27nosmb", "L3", "2027 ARR if the SMB test fails and SMB prices are held", 99.03, "$M", "arr27 - smbnet8", ["arr27", "smbnet8"], "$99.37M − $0.34M", True, ASM_BASE + ASM_PLAN)
D("arr27lo", "b4", "2027 ARR with the recommended plan and net retention 1 percentage point lower", 98.51, "$M", "arr27 - nrr1pp", ["arr27", "nrr1pp"], "$99.37M − $0.86M", True, ASM_BASE + ASM_PLAN)
D("mmloss", "b4", "Mid-market ARR lost if renewals react as SMB did in 2023", 1.41, "$M", "mmrenarr * (1 + cfo12) * xloss", ["mmrenarr", "cfo12", "xloss"],
  "$34.9M × 1.12 × 3.6%", True, ASM_2023)
D("arr27mmr", "b4", "2027 ARR if mid-market renewals react as SMB did in 2023", 97.96, "$M", "arr27 - mmloss", ["arr27", "mmloss"], "$99.37M − $1.41M", True, ASM_BASE + ASM_PLAN + ASM_2023)
D("headroom", "3c1", "Recommended plan's 2027 ARR above the target", 0.47, "$M", "arr27 - tgtarr", ["arr27", "tgtarr"], "$99.37M − $98.9M")
D("arr27be", "b4", "2027 ARR with the CFO plan if SMB churn reacts at break-even", 99.03, "$M", "base27 + reach12 - smbg12", ["base27", "reach12", "smbg12"],
  "$93.98M + $7.57M − $2.52M (the SMB gain fully lost)", True, ASM_BASE + ["SMB churn reaction exactly cancels the SMB gain (about three times the 2023 reaction)"])

# ---------------------------------------------------------------- derived: section 4
D("maxcut", "4a1", "Largest cut in SMB churn from bringing the promotion cohort to the non-promotion rate", 0.32, "%", "1 - np26 / smb26", ["np26", "smb26"], "1 − 2.1% ÷ 3.1%")
D("cstarget", "4a1", "SMB monthly churn if halved, as Customer Success claims", 0.0155, "%", "smb26 / 2", ["smb26"], "3.1% ÷ 2")
D("excessr", "4b2", "Promotion-cohort monthly churn above the rest of SMB", 2.8, "pp", "(promoch - np26) * 100", ["promoch", "np26"], "(4.9% − 2.1%) × 100")
D("excessyr", "4b2", "Share of cohort ARR lost a year beyond the rest of SMB, no compounding", 0.336, "%", "excessr * 12 / 100", ["excessr"], "2.8 pp × 12 months")
D("excess", "4b2", "ARR a year at stake from the promotion cohort's excess churn", 1.48, "$M", "promoarr * excessyr", ["promoarr", "excessyr"],
  "$4.4M × 2.8% × 12", True,
  ["Best case: the cohort's churn falls to the 2.1% of other SMB customers",
   "No compounding: lost ARR is counted on the mid-2026 cohort every month, so this is an upper bound",
   "The cohort gets no price rise in 2027, so its full-price ARR stays at $4.4M"])

D("smbcsh", "b2", "SMB share of all customers", 0.8, "%", "smbc / ncust", ["smbc", "ncust"], "5,900 ÷ 7,400")
