from dp import D, VAL
Y = [27, 28, 29, 30]
M = "1000000"
# ---------------- Option A on plan (planning-team inputs)
D("a_fix", "2c1", "Option A fixed US costs per year (compliance, team, brand marketing)", "$M", "2027–2030 plan", "fc_comp + fc_team + fc_brand", "0.5 + 0.9 + 0.7")
D("usum", "2d1", "Option A Amazon units, 2027–2030 total", "units", "2027–2030 plan", "a_u27 + a_u28 + a_u29 + a_u30", "sum of plan units")
D("ua_c25", "2a1", "Amazon contribution per unit at the plan's 25% ACoS", "$", "2027–2030 plan", "ua_pre - price * acos_a", "pre-ad contribution − $24.00 × 25%")
D("ua_c28", "2d1", "Amazon contribution per unit at the pilot's 28% ACoS", "$", "2027–2030", "ua_pre - price * acos_p", "pre-ad contribution − $24.00 × 28%")
D("ua_c32", "2d1", "Amazon contribution per unit at the benchmark median 32% ACoS", "$", "2027–2030", "ua_pre - price * acos_b", "pre-ad contribution − $24.00 × 32%")
D("ua_c38", "2d3", "Amazon contribution per unit at the benchmark high 38% ACoS", "$", "2027–2030", "ua_pre - price * acos_x", "pre-ad contribution − $24.00 × 38%")
D("ua_ad", "2a1", "Advertising per Amazon unit at the plan's 25% ACoS", "$", "2027–2030 plan", "price * acos_a", "$24.00 × 25%")
for k, (i, lab) in enumerate([("ua_ref", "Referral fee"), ("fba", "Fulfillment fee"), ("exf", "Product cost"), ("frt_a", "Freight"), ("ua_duty", "Import duty"), ("ua_ad", "Advertising")]):
    D(f"wf{k}", "2a1", f"Amazon unit bridge step: {lab}", "$", "2027–2030 plan", f"0 - {i}", f"− {lab.lower()} per unit", derived_from=[i])
D("ad_sh", "2a1", "Share of pre-ad contribution spent on advertising at 25% ACoS", "%", "2027–2030 plan", "(0 - wf5) / (price + wf0 + wf1 + wf2 + wf3 + wf4)", "$6.00 ÷ ($24.00 − fees, product, freight and duty)")
for y in Y:
    D(f"a_rev{y}", "2e1" if y == 30 else "b3", f"Option A US revenue, 20{y}", "$M", f"20{y}", f"a_u{y} * price / {M}", "units × $24.00")
    D(f"a_cm{y}", "b3", f"Option A contribution after ads, 20{y}", "$M", f"20{y}", f"a_u{y} * ua_c25 / {M}", "units × $4.725")
    D(f"a_inv{y}", "b3", f"Option A inventory held at end of 20{y}", "$M", f"20{y}", f"a_u{y} * ua_land / 3 / {M}", "units × landed cost × 4 ÷ 12")
D("a_op27", "b3", "Option A operating result, 2027", "$M", "2027", "a_cm27 - a_fix - fc_setup", "contribution − fixed − setup")
for y in Y[1:]:
    D(f"a_op{y}", "b3", f"Option A operating result, 20{y}", "$M", f"20{y}", f"a_cm{y} - a_fix", "contribution − fixed")
D("a_cf27", "b3", "Option A cash flow, 2027", "$M", "2027", "a_op27 - a_inv27", "operating result − inventory build")
D("a_cum27", "2c1", "Option A cumulative cash, end-2027 (lowest point)", "$M", "2027", "a_cf27", "cash flow 2027")
for y in Y[1:]:
    D(f"a_cf{y}", "b3", f"Option A cash flow, 20{y}", "$M", f"20{y}", f"a_op{y} - (a_inv{y} - a_inv{y-1})", "operating result − inventory build")
    D(f"a_cum{y}", "2c1", f"Option A cumulative cash, end-20{y}", "$M", f"20{y}", f"a_cum{y-1} + a_cf{y}", "previous cumulative + cash flow")
for y in Y:
    D(f"a_gm{y}", "2c1", f"Group operating margin with Option A, 20{y}", "%", f"20{y}",
      f"(g_r{y} * g_m + a_op{y}) / (g_r{y} + a_rev{y})", "(non-US profit + US result) ÷ (non-US + US revenue)")
D("pk_sh", "2c1", "Option A peak cash need as a share of the $18M cap", "%", "2027–2030", "(0 - a_cum27) / cap", "$1.94M ÷ $18M")
D("amb_sh", "2e1", "Option A 2030 revenue as a share of the $40M ambition", "%", "2030", "a_rev30 / amb", "$26.4M ÷ $40M")
D("p_run", "2b1", "Pilot sales pace in June 2026, annualized", "units", "June 2026", "p_jun * 12", "14,000 units × 12 months")
D("vol_m", "2b1", "2027 plan units as a multiple of the pilot's June pace", "x", "2027 plan", "a_u27 / p_run", "300,000 ÷ 168,000")
# ---------------- Option A sensitivities (ad cost and duty)
CUM = {27: ("a_u27", 1), 28: ("(a_u27 + a_u28)", 2), 29: ("(a_u27 + a_u28 + a_u29)", 3), 30: ("usum", 4)}
SENS = ["Ad cost held for 2027–30 at the level shown; all other inputs as in the planning team's Option A",
        "Fixed costs, one-time setup and four months of inventory as in the planning team's model"]
for c, lab in [("28", "pilot 28%"), ("32", "benchmark median 32%"), ("38", "benchmark high 38%")]:
    for y in Y:
        if c == "38" and y != 30:
            continue
        u, n = CUM[y]
        D(f"s{c}_{y}", "2d1" if c != "38" else "2d3", f"Option A cumulative cash at {lab} ad cost, end-20{y}", "$M", f"20{y}",
          f"{u} * ua_c{c} / {M} - a_fix * {n} - fc_setup - a_u{y} * ua_land / 3 / {M}",
          "units to date × contribution per unit − fixed costs to date − setup − inventory held",
          assumptions=SENS)
D("s38_pk", "2d3", "Option A lowest cumulative cash at 38% ad cost (end-2030)", "$M", "2030", "s38_30", "lowest point is end-2030", assumptions=SENS)
D("acos_be", "2d1", "Highest blended ACoS at which Option A pays back by end-2030 (15% duty)", "%", "2027–2030",
  "acos_p + (acos_b - acos_p) * s28_30 / (s28_30 - s32_30)",
  "ad cost at which end-2030 cumulative cash is zero; exact, because cash falls in a straight line as ad cost rises: 28% + 4 pp × $0.38M ÷ ($0.38M + $2.32M)")
D("dd", "2d3", "Duty increase per unit if the duty rises from 15% to 25%", "$", "mid-2027 decision", "exf * (duty_hi - duty)", "$3.50 × (25% − 15%)")
TA = SENS + ["Duty of 25% of ex-factory cost applied from 2027, as the review could decide in mid-2027"]
for c, acos in [("25", "acos_a"), ("28", "acos_p"), ("32", "acos_b"), ("38", "acos_x")]:
    D(f"t{c}", "2d3", f"Option A cumulative cash at end-2030, {c}% ad cost and 25% duty", "$M", "2030",
      f"usum * (ua_pre - dd - price * {acos}) / {M} - a_fix * 4 - fc_setup - a_u30 * (ua_land + dd) / 3 / {M}",
      "units × (contribution before ads − extra duty − ads) − fixed − setup − inventory", assumptions=TA)
BE = ["All Option A planning-team inputs held; one blended ad cost for 2027–30",
      "Break-even = the ad cost at which cumulative cash returns to exactly zero at end-2030"]

D("acos_be25", "2d3", "Highest blended ACoS at which Option A pays back by end-2030 (25% duty)", "%", "2027–2030",
  f"(usum * (ua_pre - dd) / {M} - a_fix * 4 - fc_setup - a_u30 * (ua_land + dd) / 3 / {M}) / (usum * price / {M})",
  "same as the break-even at 15% duty, with $0.35 a unit more duty", assumptions=BE + TA[-1:])
D("ad_gap", "2d2", "Cumulative cash lost by 2030 at 32% ACoS compared with the plan's 25%", "$M", "2027–2030",
  f"(acos_b - acos_a) * price * usum / {M}", "(32% − 25%) × $24.00 × 2.81M units")
# ---------------- Option B (planning-team inputs)
D("wk", "3a2", "Weeks in a year", "weeks", "n/a", "52", "52 weeks", derived_from=[])
D("b_fix", "3a1", "Option B fixed US costs per year", "$M", "2027–2030 plan", "a_fix + fc_rmkt + fc_field", "2.1 + 6.0 + 1.5")
D("b_once", "3a2", "Option B one-time costs in 2027 (setup, launch fee, fixtures for 600 doors)", "$M", "2027", f"fc_setup + fc_lfee + b_d27 * fixt / {M}", "0.8 + 0.5 + 600 × $1,100")
D("b_fx29", "b5", "Option B fixtures for new doors, 2029", "$M", "2029", f"(b_d29 - b_d28) * fixt / {M}", "200 doors × $1,100")
D("b_fx30", "b5", "Option B fixtures for new doors, 2030", "$M", "2030", f"(b_d30 - b_d29) * fixt / {M}", "200 doors × $1,100")
for y in Y:
    D(f"b_ru{y}", "3a2" if y == 27 else "b5", f"Option B retail units, 20{y}", "units", f"20{y}", f"b_d{y} * upw * wk", "doors × 4.5 × 52")
    D(f"b_au{y}", "b5", f"Option B Amazon units, 20{y}", "units", f"20{y}", f"a_u{y} * halo", "Option A units × 1.3")
    D(f"b_rev{y}", "2e1" if y == 30 else "b5", f"Option B US revenue, 20{y}", "$M", f"20{y}", f"(b_ru{y} * whsl + b_au{y} * price) / {M}", "retail units × $14 + Amazon units × $24")
    D(f"b_cm{y}", "b5", f"Option B contribution, 20{y}", "$M", f"20{y}", f"(b_ru{y} * ur_c + b_au{y} * ua_c25) / {M}", "retail units × $7.545 + Amazon units × $4.725")
    D(f"b_inv{y}", "b5", f"Option B inventory held at end of 20{y}", "$M", f"20{y}", f"(b_ru{y} * ur_land + b_au{y} * ua_land) / 3 / {M}", "units × landed cost × 4 ÷ 12")
D("b_op27", "b5", "Option B operating result, 2027", "$M", "2027", "b_cm27 - b_fix - b_once", "contribution − fixed − one-time")
D("b_op28", "b5", "Option B operating result, 2028", "$M", "2028", "b_cm28 - b_fix", "contribution − fixed")
D("b_op29", "b5", "Option B operating result, 2029", "$M", "2029", "b_cm29 - b_fix - b_fx29", "contribution − fixed − fixtures")
D("b_op30", "b5", "Option B operating result, 2030", "$M", "2030", "b_cm30 - b_fix - b_fx30", "contribution − fixed − fixtures")
D("b_cum27", "3a1", "Option B cumulative cash, end-2027", "$M", "2027", "b_op27 - b_inv27", "operating result − inventory build")
for y in Y[1:]:
    D(f"b_cum{y}", "3a1", f"Option B cumulative cash, end-20{y}", "$M", f"20{y}", f"b_cum{y-1} + b_op{y} - (b_inv{y} - b_inv{y-1})", "previous + operating result − inventory build")
for y in Y:
    D(f"b_gm{y}", "3a1", f"Group operating margin with Option B, 20{y}", "%", f"20{y}", f"(g_r{y} * g_m + b_op{y}) / (g_r{y} + b_rev{y})", "(non-US profit + US result) ÷ (non-US + US revenue)")
D("r_cm", "3a2", "Retail contribution from 600 doors at 4.5 units per door per week, 2027", "$M", "2027", f"b_ru27 * ur_c / {M}", "140,400 units × $7.545")
D("r_fix", "3a2", "Retail-only fixed costs per year (national marketing and field team)", "$M", "2027–2030 plan", "fc_rmkt + fc_field", "6.0 + 1.5")
D("r_rat", "3a2", "Retail-only fixed costs as a multiple of retail contribution, 600 doors", "x", "2027", "r_fix / r_cm", "$7.5M ÷ $1.06M")
D("r_be", "3a2", "Units per door per week needed for 600 doors to cover retail-only fixed costs", "units per door per week", "2027", f"r_fix * {M} / (ur_c * wk * b_d27)", "$7.5M ÷ ($7.545 × 52 × 600)")
D("r_cm_hi", "5b", "Retail contribution from 600 doors at 4.6 units per door per week", "$M", "2029+", f"b_d27 * st_hi * wk * ur_c / {M}", "600 × 4.6 × 52 × $7.545")
D("r_rat_hi", "5b", "Retail-only fixed costs as a multiple of contribution at 4.6 units per door per week", "x", "2029+", "r_fix / r_cm_hi", "$7.5M ÷ $1.08M")
CORR = ["Doors, fixed costs, one-time costs and inventory rule as in the planning team's Option B"]
D("bn30", "3c2", "Option B cumulative cash at end-2030 without the Amazon halo", "$M", "2030",
  f"((b_ru27 + b_ru28 + b_ru29 + b_ru30) * ur_c + usum * ua_c25) / {M} - b_fix * 4 - b_once - b_fx29 - b_fx30 - (b_ru30 * ur_land + a_u30 * ua_land) / 3 / {M}",
  "retail and Amazon contribution − fixed − one-time − inventory, Amazon at Option A volumes",
  assumptions=CORR + ["Amazon units equal Option A's: no 1.3 times halo (3c)"])
D("bc30", "3c2", "Option B cumulative cash at end-2030 with 2.6 units per door per week and no halo", "$M", "2030",
  f"((b_d27 + b_d28 + b_d29 + b_d30) * st_lo * wk * ur_c + usum * ua_c25) / {M} - b_fix * 4 - b_once - b_fx29 - b_fx30 - (b_d30 * st_lo * wk * ur_land + a_u30 * ua_land) / 3 / {M}",
  "as above, retail at the 2.6 median for brands below 10% awareness",
  assumptions=CORR + ["Amazon units equal Option A's: no 1.3 times halo (3c)", "Retail sells the 2.6 median of newcomers below 10% awareness (3b); doors stay on shelf despite the 4.0 removal rule"])
D("w_halo", "3c2", "Change in Option B cumulative cash from removing the halo", "$M", "2030", "bn30 - b_cum30", "no-halo case − plan case", assumptions=["Amazon units equal Option A's: no 1.3 times halo (3c)"])
D("w_st", "3c2", "Change in Option B cumulative cash from 2.6 units per door per week", "$M", "2030", "bc30 - bn30", "2.6-unit case − no-halo case",
  assumptions=["Retail sells the 2.6 median of newcomers below 10% awareness (3b)"])
D("bc_x", "3c2", "Corrected Option B cash need as a multiple of the $18M cap", "x", "2030", "(0 - bc30) / cap", "$26.4M ÷ $18M",
  assumptions=["Corrected case as above"])
D("b_cap_x", "3a1", "Option B cash need at end-2030 as a multiple of the cap", "x", "2030", "(0 - b_cum30) / cap", "$20.8M ÷ $18M")
# ---------------- Option J
D("j_op27", "b6", "Option J operating result, 2027", "$M", "2027", "j_r27 * j_cm - j_fix - j_one", "revenue × 30% − fixed − one-time")
for y in Y[1:]:
    D(f"j_op{y}", "b6", f"Option J operating result, 20{y}", "$M", f"20{y}", f"j_r{y} * j_cm - j_fix", "revenue × 30% − fixed")
D("j_cum27", "4a1", "Option J cumulative cash, end-2027", "$M", "2027", "j_op27", "operating result 2027")
for y in Y[1:]:
    D(f"j_cum{y}", "4a1", f"Option J cumulative cash, end-20{y}", "$M", f"20{y}", f"j_cum{y-1} + j_op{y}", "previous + operating result")
for y in Y:
    D(f"j_gm{y}", "b6", f"Group operating margin with Option J, 20{y}", "%", f"20{y}", f"(g_r{y} * g_m + j_op{y}) / (g_r{y} + j_r{y})", "(non-US profit + Japan result) ÷ (group + Japan revenue)")
D("j_vs", "4b1", "Option A 2030 US revenue as a multiple of Option J 2030 Japan revenue", "x", "2030", "a_rev30 / j_r30", "$26.4M ÷ $7.0M")
D("j_sh", "2e1", "Option J 2030 revenue as a share of Option A 2030 revenue", "%", "2030", "j_r30 / a_rev30", "$7.0M ÷ $26.4M")
D("st_gap", "3b1", "Median sell-through below 10% awareness as a share of the removal threshold", "%", "2025", "st_lo / delist", "2.6 ÷ 4.0")
D("acos_j", "4a1", "Ad cost above which Option J returns more cash by end-2030 than Option A", "%", "2027–2030",
  "acos_a + (acos_p - acos_a) * (a_cum30 - j_cum30) / (a_cum30 - s28_30)",
  "ad cost at which Option A's end-2030 cash equals Option J's $1.8M; straight line between the 25% and 28% cases")
D("p_step", "2b1", "Average monthly gain in pilot units, January to June 2026", "units", "Jan–Jun 2026", "(p_jun - p_jan) / 5", "(14,000 − 7,400) ÷ 5")
D("p_trend", "2b1", "2027 units if the pilot kept its average monthly gain, three SKUs", "units", "2027",
  "p_jun * 12 + p_step * 150", "12 × 14,000 + 1,320 × (7 + 8 + … + 18) for January–December 2027")
D("r_rat30", "3a2", "Retail-only fixed costs as a multiple of retail contribution, 1,000 doors in 2030", "x", "2030",
  f"r_fix / (b_ru30 * ur_c / {M})", "$7.5M ÷ (234,000 units × $7.545)")
D("vol80", "5d", "Volume sensitivity case: share of plan units sold", "%", "2027–2030", "0.8", "80% of plan, a downside test chosen by the team", derived_from=[])
D("v80", "5d", "Option A cumulative cash at end-2030 at 80% of plan volume, 25% ad cost", "$M", "2030",
  f"usum * vol80 * ua_c25 / {M} - a_fix * 4 - fc_setup - a_u30 * vol80 * ua_land / 3 / {M}", "80% of plan units, all other inputs as planned")
