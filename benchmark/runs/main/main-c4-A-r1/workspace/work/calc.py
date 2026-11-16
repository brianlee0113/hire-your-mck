"""All numbers used in the deck, derived only from evidence/briefing-pack.md.
Run: python3 calc.py  -> prints every figure; build.py imports C."""

C = {}

# ---- Evidence (briefing pack) ----
ARR = {"SMB": 21.0, "MM": 41.0, "ENT": 24.0}
CUST = {"SMB": 5900, "MM": 1350, "ENT": 150}
CH25 = {"SMB": 2.0, "MM": 0.6, "ENT": 0.2}   # monthly logo churn %, H1 2025
CH26 = {"SMB": 3.1, "MM": 0.8, "ENT": 0.2}   # H1 2026
NRR = {"SMB": 0.94, "MM": 1.12, "ENT": 1.18}
PROMO_N, PROMO_ARR = 2100, 4.4
NONPROMO_CH26, NONPROMO_CH25 = 2.1, 2.0
RENEW27 = {"SMB": 1.00, "MM": 0.85, "ENT": 0.40}
ENT_CAPPED, CAP = 0.60, 0.07
TOTAL_ARR = sum(ARR.values())
TARGET = TOTAL_ARR * 1.15

C["total_arr"] = TOTAL_ARR
C["target"] = TARGET
C["growth_needed"] = TARGET - TOTAL_ARR

# ---- Churn decomposition ----
nonpromo_n = CUST["SMB"] - PROMO_N
promo_ch = (CUST["SMB"] * CH26["SMB"] - nonpromo_n * NONPROMO_CH26) / PROMO_N
C["nonpromo_n"] = nonpromo_n
C["promo_ch"] = promo_ch
C["promo_share_churners"] = PROMO_N * promo_ch / (CUST["SMB"] * CH26["SMB"])
C["promo_share_cust"] = PROMO_N / CUST["SMB"]
C["promo_share_arr"] = PROMO_ARR / ARR["SMB"]
C["smb_rise_from_promo"] = CH26["SMB"] - NONPROMO_CH26   # 1.0 pt of 1.1 pt
C["annual"] = {k: 1 - (1 - v / 100) ** 12 for k, v in
               {"SMB": 3.1, "nonpromo": 2.1, "promo": promo_ch, "MM": 0.8, "ENT": 0.2}.items()}

# Activation: low activators (<5 docs in month 1) churn ~3x others
# non-promo: 72% activated -> 0.72x + 0.28*3x = 2.1  => x
x = NONPROMO_CH26 / (0.72 + 0.28 * 3)
promo_from_activation = 0.41 * x + 0.59 * 3 * x
C["act_x"] = x
C["promo_pred_by_activation"] = promo_from_activation
C["activation_share_of_excess"] = (promo_from_activation - NONPROMO_CH26) / (promo_ch - NONPROMO_CH26)

# Exit survey consistency check
w = PROMO_N * promo_ch
C["survey_implied_all"] = (0.52 * w + 0.18 * nonpromo_n * NONPROMO_CH26) / (w + nonpromo_n * NONPROMO_CH26)

# Board dashboard reconciliation
def wavg(ch, wts):
    return sum(ch[k] * wts[k] for k in ch) / sum(wts.values())
C["cust_w"] = (wavg(CH25, CUST), wavg(CH26, CUST))
C["arr_w"] = (wavg(CH25, ARR), wavg(CH26, ARR))

# Overall NRR (ARR-weighted)
nrr = sum(NRR[k] * ARR[k] for k in ARR) / TOTAL_ARR
C["nrr"] = nrr
C["base_growth"] = TOTAL_ARR * (nrr - 1)

# ---- CFO plan: +12% all plans at renewal ----
p = 0.12
C["cfo_headline"] = TOTAL_ARR * p
C["cfo_mm_not_renew"] = ARR["MM"] * (1 - RENEW27["MM"]) * p
C["cfo_ent_not_renew"] = ARR["ENT"] * (1 - RENEW27["ENT"]) * p
ent_renew = ARR["ENT"] * RENEW27["ENT"]
C["cfo_ent_cap"] = ent_renew * ENT_CAPPED * (p - CAP)
gross = {
    "SMB": ARR["SMB"] * p,
    "MM": ARR["MM"] * RENEW27["MM"] * p,
    "ENT": ent_renew * ENT_CAPPED * CAP + ent_renew * (1 - ENT_CAPPED) * p,
}
C["cfo_gross"] = gross
C["cfo_gross_total"] = sum(gross.values())

# SMB churn response, 2023 analog: +8% -> +0.5pt/month for 6 months, then +0.1pt (settled 1.9 vs 1.8)
def smb_extra_loss(price, mult=1.0):
    s = price / 0.08 * mult
    return (0.5 * s * 6 + 0.1 * s * 6) / 100   # share of customers lost over 12 months (simple sum)

smb_loss_plan = smb_extra_loss(p, 1.0)
smb_loss_stress = smb_extra_loss(p, 2.0)
C["smb_loss_rate"] = (smb_loss_plan, smb_loss_stress)
C["smb_lost_cust"] = (smb_loss_plan * CUST["SMB"], smb_loss_stress * CUST["SMB"])
C["smb_drag"] = (ARR["SMB"] * (1 + p) * smb_loss_plan, ARR["SMB"] * (1 + p) * smb_loss_stress)
C["smb_net"] = (gross["SMB"] - C["smb_drag"][0], gross["SMB"] - C["smb_drag"][1])

# Mid-market churn response: loss of renewing ARR = k * price; planning k=0.21 (2024 test: 23.1 vs 23.6 = 2.1% relative), stress 5% at +10%
k_plan = (23.6 - 23.1) / 23.6 / 0.10
k_stress = 0.05 / 0.10
C["mm_test_gap"] = (23.6 - 23.1) / 23.6
mm_renew = ARR["MM"] * RENEW27["MM"]
def mm_net(price, k):
    g = mm_renew * price
    return g, mm_renew * (1 + price) * k * price, g - mm_renew * (1 + price) * k * price
C["mm_renew"] = mm_renew
C["cfo_mm"] = (mm_net(p, k_plan), mm_net(p, k_stress))
C["cfo_net"] = (C["smb_net"][0] + C["cfo_mm"][0][2] + gross["ENT"],
                C["smb_net"][1] + C["cfo_mm"][1][2] + gross["ENT"])

# ---- Recommended plan ----
rp = 0.10
rec_mm_plan = mm_net(rp, k_plan)
rec_mm_stress = mm_net(rp, k_stress)
rec_ent = ent_renew * ENT_CAPPED * CAP + ent_renew * (1 - ENT_CAPPED) * rp
C["rec_mm"] = (rec_mm_plan, rec_mm_stress)
C["rec_ent"] = rec_ent
C["rec_gross"] = rec_mm_plan[0] + rec_ent
C["rec_net"] = (rec_mm_plan[2] + rec_ent, rec_mm_stress[2] + rec_ent)
C["mm_breakeven"] = rp / (1 + rp)
C["mm_breakeven12"] = p / (1 + p)
C["smb_breakeven12"] = p / (1 + p)
# SMB H2 upside: +8% on non-promo SMB ARR from mid-year (half-year of renewals)
C["smb_h2_gross"] = (ARR["SMB"] - PROMO_ARR) * 0.08 * 0.5
C["smb_full_gross"] = (ARR["SMB"] - PROMO_ARR) * 0.08

# NRR after plan
C["nrr_cfo"] = (nrr + C["cfo_net"][1] / TOTAL_ARR, nrr + C["cfo_net"][0] / TOTAL_ARR)
C["nrr_rec"] = (nrr + C["rec_net"][1] / TOTAL_ARR, nrr + C["rec_net"][0] / TOTAL_ARR)

# New logos needed for +15%
need = C["growth_needed"] - C["base_growth"]
C["need_hold"] = need
C["need_cfo"] = (max(0, need - C["cfo_net"][0]), need - C["cfo_net"][1])
C["need_rec"] = (need - C["rec_net"][0], need - C["rec_net"][1])
C["gap_vs_cfo"] = (C["cfo_net"][1] - C["rec_net"][1], C["cfo_net"][0] - C["rec_net"][0])

# Onboarding
C["smb_if_promo_fixed"] = NONPROMO_CH26
C["smb_halved"] = CH26["SMB"] / 2
C["smb_fix_cut"] = 1 - NONPROMO_CH26 / CH26["SMB"]

# Inkwell gap
C["prem_now"] = 15 / 9 - 1
C["prem_after"] = 15 * 1.12 / 9 - 1

if __name__ == "__main__":
    import pprint
    pprint.pprint(C, width=110)
