"""Builds the storyline spec for the Meridian Motion make-or-buy deck.

Every number is a data point: either quoted from the briefing pack (source s1)
or derived with a calc over other data points (source s0).
"""
import json, re, sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "meridian-housings.json"
DP = {}          # id -> data point
ORDER = []


def P(i, label, value, unit, excerpt, locator, period=None, **kw):
    d = {"id": i, "slide_id": "1", "label": label, "value": value, "unit": unit, "source_id": "s1",
         "excerpt": excerpt, "locator": locator}
    if period: d["period"] = period
    d.update(kw)
    DP[i] = d; ORDER.append(i)


def D(i, label, value, unit, calc, formula, period=None, estimate=False, assumptions=None, **kw):
    ids = [t for t in re.findall(r"[A-Za-z_][A-Za-z0-9_]*", calc) if t in DP]
    d = {"id": i, "slide_id": "1", "label": label, "value": value, "unit": unit, "source_id": "s0",
         "derived_from": list(dict.fromkeys(ids)), "formula": formula, "calc": calc}
    if period: d["period"] = period
    if estimate:
        d["estimate"] = True
        d["assumptions"] = assumptions or []
    d.update(kw)
    DP[i] = d; ORDER.append(i)


def r(i): return {"data_ref": i}


# ------------------------------------------------------------------ pack inputs (s1)
T3 = "| Quoted unit cost | $73 at supplier gate | $46 per unit started | $49 per unit started |"
L3 = "§3 Economics and quotations, table"
P("gate", "Supplier quoted unit cost at the supplier gate", 73, "$", T3, L3 + ", row 'Quoted unit cost'", "2027 quote, valid to Mar 2027")
P("freight", "Supplier freight and inbound QA per good unit", 2, "$", "| Freight and inbound QA | $2 per good unit | included in variable cost | included in variable cost |", L3 + ", row 'Freight and inbound QA'")
P("ownvar", "Owned cell variable cost per unit started", 46, "$", T3, L3 + ", row 'Quoted unit cost'")
P("leasevar", "Leased cell variable cost per unit started", 49, "$", T3, L3 + ", row 'Quoted unit cost'")
P("own_eq", "Owned cell equipment cost", 6.5, "$M", "| Initial investment | None; optional alternate-shop tooling $0.25M | $6.5M equipment + $0.8M installation | $2.0M installation and training |", L3 + ", row 'Initial investment'")
P("own_inst", "Owned cell installation cost", 0.8, "$M", "| Initial investment | None; optional alternate-shop tooling $0.25M | $6.5M equipment + $0.8M installation | $2.0M installation and training |", L3 + ", row 'Initial investment'")
P("lease_inst", "Leased cell installation and training", 2.0, "$M", "| Initial investment | None; optional alternate-shop tooling $0.25M | $6.5M equipment + $0.8M installation | $2.0M installation and training |", L3 + ", row 'Initial investment'")
P("alt_tool", "Dedicated tooling at Meridian's alternate approved shop", 250, "$K", "would charge an extra $0.25M for dedicated tooling at Meridian's alternate approved shop", "§3, paragraph under the table")
P("own_fix", "Owned cell recurring fixed cost per year", 0.75, "$M", "| Recurring fixed cost | none beyond quoted price | $0.75M per year | $1.60M annual lease and staffing |", L3 + ", row 'Recurring fixed cost'", "per year")
P("lease_fix", "Leased cell annual lease and staffing", 1.6, "$M", "| Recurring fixed cost | none beyond quoted price | $0.75M per year | $1.60M annual lease and staffing |", L3 + ", row 'Recurring fixed cost'", "per year")
P("scr_o1", "Owned cell first-year scrap, share of starts", 0.08, "%", "| First-year scrap | supplier price covers rejects | 8% of starts | 6% of starts |", L3 + ", row 'First-year scrap'", "2027")
P("scr_l1", "Leased cell first-year scrap, share of starts", 0.06, "%", "| First-year scrap | supplier price covers rejects | 8% of starts | 6% of starts |", L3 + ", row 'First-year scrap'", "2027")
P("scr_lt", "Later-year scrap, both cells, share of starts", 0.04, "%", "| Later-year scrap | supplier price covers rejects | 4% of starts | 4% of starts |", L3 + ", row 'Later-year scrap'", "2028–29")
P("cap_sup", "Supplier practical annual output if renewed", 140000, "housings a year", "| Practical annual output | up to 140,000 if renewed | 120,000 accepted units | 125,000 accepted units |", L3 + ", row 'Practical annual output'")
P("cap_own", "Owned cell practical annual output", 120000, "accepted units a year", "| Practical annual output | up to 140,000 if renewed | 120,000 accepted units | 125,000 accepted units |", L3 + ", row 'Practical annual output'")
P("resale", "Estimated resale of owned-cell equipment after 2029 (dealer indication, not binding)", 2.1, "$M", "Build equipment could be sold for an estimated $2.1M after 2029, but a dealer's indication is not a binding offer.", "§3, paragraph under the table", "after 2029")
P("v27", "Planning demand, good units, 2027", 80000, "units", "Housing demand planning assumes 80,000 good units in 2027, 100,000 in 2028 and 120,000 in 2029.", "§2 Constraints", "2027")
P("v28", "Planning demand, good units, 2028", 100000, "units", "Housing demand planning assumes 80,000 good units in 2027, 100,000 in 2028 and 120,000 in 2029.", "§2 Constraints", "2028")
P("v29", "Planning demand, good units, 2029", 120000, "units", "Housing demand planning assumes 80,000 good units in 2027, 100,000 in 2028 and 120,000 in 2029.", "§2 Constraints", "2029")
P("c28", "Conservative demand, good units, 2028", 65000, "units", "The major customer's forecast is not a guaranteed order; the conservative 2028 case is 65,000 units.", "§2 Constraints; §4 table, row 'Conservative demand'", "2028")
P("c29", "Conservative demand, good units, 2029", 85000, "units", "| Conservative demand | 80,000 | 65,000 | 85,000 |", "§4 Operating volume and reliability, table, row 'Conservative demand'", "2029")
P("capex_lim", "New 2027 capital spending approvable without a new financing agreement", 5.0, "$M", "At most $5.0M of new 2027 capital spending can be approved without a new financing agreement.", "§2 Constraints agreed by the board", "2027")
P("cash_floor", "Minimum year-end unrestricted cash", 4.0, "$M", "Separately, year-end unrestricted cash must remain above $4.0M.", "§2 Constraints agreed by the board", "year-end 2027")
P("cash_now", "Available cash today", 9.2, "$M", "Today's available cash is $9.2M and no debt or equity increase is approved.", "§2 Constraints agreed by the board", "Nov 2026")
P("otd_req", "Contract requirement: share of requested units shipped within ten business days", 0.97, "%", "A customer delivery contract requires 97% of requested units to ship within ten business days.", "§2 Constraints agreed by the board", definition="share of requested units, not of orders")
P("otd", "Supplier on-time delivery: share of orders delivered within ten business days", 0.968, "%", "The supplier has delivered 96.8% of orders within ten business days, slightly below the customer requirement, but late deliveries were concentrated during one flood-related road closure.", "§4 Operating volume and reliability", definition="share of orders, not of requested units")
P("demo_yield", "Demonstration-cell production yield on the internal dashboard", 0.985, "%", "An internal dashboard reports 98.5% production yield for the demonstration cell.", "§4 Operating volume and reliability", definition="excludes start-up runs, rework and three days of tooling-change downtime")
P("emerg", "Second approved supplier price for emergency orders, per accepted unit", 88, "$", "A second approved supplier is available for emergency orders at $88 per accepted unit with six-week notice.", "§4 Operating volume and reliability")
DP["emerg_wk"] = {"id": "emerg_wk", "slide_id": "1", "label": "Notice the second approved supplier needs for emergency orders", "value": 6, "unit": "weeks", "source_id": "s1", "locator": "§4 Operating volume and reliability: 'at $88 per accepted unit with six-week notice'"}; ORDER.append("emerg_wk")
P("reserved", "Reserved units the supplier can provide after ninety days' notice", 40000, "units", "The supplier can provide 40,000 reserved units after giving ninety days' notice.", "§2 Constraints agreed by the board")
DP["lead_eq"] = {"id": "lead_eq", "slide_id": "1", "label": "Lead time on new equipment orders", "value": 9, "unit": "months", "source_id": "s1", "locator": "§5 Internal presentation circulated to management: 'new equipment orders take nine months'"}; ORDER.append("lead_eq")
P("cfo", "Saving per housing claimed on the CFO's slide", 27, "$", "Buying at $73 versus making at $46 saves $27 on every housing; at 100,000 units the payback is under three years.", "§5 Internal presentation circulated to management", definition="factory-gate price compared with variable cost per started unit")

# ------------------------------------------------------------------ derived (s0)
D("sup_u", "Supplier delivered cost per good unit", 75, "$", "gate + freight", "$73 + $2")
D("own_u1", "Owned cell variable cost per good unit, 2027 (8% scrap)", 50.0, "$", "ownvar / (1 - scr_o1)", "$46 ÷ (1 − 8%)", "2027")
D("own_ul", "Owned cell variable cost per good unit, 2028–29 (4% scrap)", 47.92, "$", "ownvar / (1 - scr_lt)", "$46 ÷ (1 − 4%)", "2028–29")
D("lease_u1", "Leased cell variable cost per good unit, 2027 (6% scrap)", 52.13, "$", "leasevar / (1 - scr_l1)", "$49 ÷ (1 − 6%)", "2027")
D("lease_ul", "Leased cell variable cost per good unit, 2028–29 (4% scrap)", 51.04, "$", "leasevar / (1 - scr_lt)", "$49 ÷ (1 − 4%)", "2028–29")
D("own_capex", "Owned cell upfront investment, equipment plus installation", 7.3, "$M", "own_eq + own_inst", "$6.5M + $0.8M", "2027")
D("vol_p", "Planning demand, good units, 2027–29", 300000, "units", "v27 + v28 + v29", "80,000 + 100,000 + 120,000", "2027–29")
D("vol_c", "Conservative demand, good units, 2027–29", 230000, "units", "v27 + c28 + c29", "80,000 + 65,000 + 85,000", "2027–29")
D("vol_gap", "Good units lost in the conservative case compared with planning, 2027–29", 70000, "units", "vol_p - vol_c", "300,000 − 230,000", "2027–29")
BUY_A0 = ["Delivered price $75 per good unit for 2027–29, indicative after March 2027", "$0.25M dedicated tooling at the alternate approved shop; its unit price is not in the briefing pack and is taken as equal to the supplier's", "Nominal dollars; no tax or financing"]
D("buy_p", "Buying: cost of housings, planning demand, 2027–29", 22.5, "$M", "sup_u * vol_p / 1000000", "$75 × 300,000", "2027–29", estimate=True,
  assumptions=["Delivered price stays at $73 gate + $2 freight and inbound QA for 2027–29; the quote lasts only to March 2027 and later pricing is indicative", "Supplier is paid on accepted units only, so rejects cost Meridian nothing", "Planning demand of 80,000, 100,000 and 120,000 good units", "Nominal dollars; no tax or financing"])
D("buy_c", "Buying: cost of housings, conservative demand, 2027–29", 17.25, "$M", "sup_u * vol_c / 1000000", "$75 × 230,000", "2027–29", estimate=True,
  assumptions=["Delivered price stays at $75 per good unit", "Conservative demand of 80,000, 65,000 and 85,000 good units", "Nominal dollars; no tax or financing"])
OWN_A = ["Cell produces all volume for full years 2027–29; the nine-month equipment lead time makes this optimistic for 2027",
         "Scrap of 8% of starts in 2027 and 4% in 2028–29 (process engineer's plan)",
         "Fixed staffing of $0.75M a year; $7.3M upfront for equipment and installation",
         "Equipment resold for $2.1M after 2029 (dealer indication, not binding) unless stated otherwise",
         "Nominal dollars; no tax, depreciation or financing"]
LEASE_A = ["Cell produces all volume for full years 2027–29; the five-month deployment makes this optimistic for 2027",
           "Scrap of 6% of starts in 2027 and 4% in 2028–29",
           "Lease and staffing of $1.60M a year plus $2.0M installation and training; no residual value after 2029",
           "Nominal dollars; no tax or financing"]
D("own_var_p", "Owned cell variable cost on accepted units, planning demand, 2027–29", 14.54, "$M", "(v27 * own_u1 + (v28 + v29) * own_ul) / 1000000", "80,000 × $50.00 + 220,000 × $47.92", "2027–29", True, OWN_A)
D("own_fix3", "Owned cell fixed cost, 2027–29", 2.25, "$M", "3 * own_fix", "3 × $0.75M", "2027–29")
D("own_tot_p", "Owned cell three-year cost net of resale, planning demand", 21.99, "$M", "own_capex + own_fix3 + own_var_p - resale", "$7.3M + $2.25M + $14.54M − $2.1M", "2027–29", True, OWN_A)
D("own_sav_p", "Owned cell saving compared with buying, planning demand, 2027–29", 0.51, "$M", "buy_p - own_tot_p", "$22.5M − $21.99M", "2027–29", True, OWN_A)
D("own_sav_sh", "Owned cell saving as a share of the cost of buying, planning demand", 0.023, "%", "own_sav_p / buy_p", "$0.51M ÷ $22.5M", "2027–29", True, OWN_A)
D("own_op_sav", "Owned cell operating saving before capital, planning demand, 2027–29", 5.71, "$M", "buy_p - own_var_p - own_fix3", "$22.5M − $14.54M − $2.25M", "2027–29", True, OWN_A)
D("own_rec", "Share of the owned cell's $7.3M outlay recovered by operating savings by 2029", 0.78, "%", "own_op_sav / own_capex", "$5.71M ÷ $7.3M", "2027–29", True, OWN_A)
D("own_tot_nr", "Owned cell three-year cost without resale, planning demand", 24.09, "$M", "own_tot_p + resale", "$21.99M + $2.1M", "2027–29", True, OWN_A[:4])
D("own_sav_nr", "Owned cell saving compared with buying without resale, planning demand", -1.59, "$M", "buy_p - own_tot_nr", "$22.5M − $24.09M", "2027–29", True, OWN_A[:4])
D("lease_var_p", "Leased cell variable cost on accepted units, planning demand, 2027–29", 15.40, "$M", "(v27 * lease_u1 + (v28 + v29) * lease_ul) / 1000000", "80,000 × $52.13 + 220,000 × $51.04", "2027–29", True, LEASE_A)
D("lease_fix3", "Leased cell lease and staffing, 2027–29", 4.8, "$M", "3 * lease_fix", "3 × $1.60M", "2027–29")
D("lease_tot_p", "Leased cell three-year cost, planning demand", 22.2, "$M", "lease_inst + lease_fix3 + lease_var_p", "$2.0M + $4.8M + $15.40M", "2027–29", True, LEASE_A)
D("lease_sav_p", "Leased cell saving compared with buying, planning demand, 2027–29", 0.30, "$M", "buy_p - lease_tot_p", "$22.5M − $22.2M", "2027–29", True, LEASE_A)
D("lease_sav_sh", "Leased cell saving as a share of the cost of buying, planning demand", 0.013, "%", "lease_sav_p / buy_p", "$0.30M ÷ $22.5M", "2027–29", True, LEASE_A)
D("own_var_c", "Owned cell variable cost on accepted units, conservative demand, 2027–29", 11.19, "$M", "(v27 * own_u1 + (c28 + c29) * own_ul) / 1000000", "80,000 × $50.00 + 150,000 × $47.92", "2027–29", True, OWN_A)
D("own_tot_c", "Owned cell three-year cost net of resale, conservative demand", 18.64, "$M", "own_capex + own_fix3 + own_var_c - resale", "$7.3M + $2.25M + $11.19M − $2.1M", "2027–29", True, OWN_A)
D("own_sav_c", "Owned cell saving compared with buying, conservative demand, 2027–29", -1.39, "$M", "buy_c - own_tot_c", "$17.25M − $18.64M", "2027–29", True, OWN_A)
D("lease_var_c", "Leased cell variable cost on accepted units, conservative demand, 2027–29", 11.83, "$M", "(v27 * lease_u1 + (c28 + c29) * lease_ul) / 1000000", "80,000 × $52.13 + 150,000 × $51.04", "2027–29", True, LEASE_A)
D("lease_tot_c", "Leased cell three-year cost, conservative demand", 18.63, "$M", "lease_inst + lease_fix3 + lease_var_c", "$2.0M + $4.8M + $11.83M", "2027–29", True, LEASE_A)
D("lease_sav_c", "Leased cell saving compared with buying, conservative demand, 2027–29", -1.38, "$M", "buy_c - lease_tot_c", "$17.25M − $18.63M", "2027–29", True, LEASE_A)
D("lease_ratio", "Leased cell loss on conservative demand as a multiple of its gain on planning demand", 4.6, "x", "(0 - lease_sav_c) / lease_sav_p", "$1.38M ÷ $0.30M", "2027–29", True, LEASE_A)
D("lease_sav_s6", "Leased cell saving compared with buying if scrap stays at 6% in 2028–29, planning demand", 0.06, "$M", "buy_p - (lease_inst + lease_fix3 + vol_p * lease_u1 / 1000000)", "$22.5M − ($2.0M + $4.8M + 300,000 × $52.13)", "2027–29", True,
  ["As the base lease case, but scrap stays at the first-year 6% of starts in 2028–29"])
D("own_sav_s8", "Owned cell saving compared with buying if scrap stays at 8% in 2028–29, planning demand", 0.05, "$M", "buy_p - (own_capex + own_fix3 + vol_p * own_u1 / 1000000 - resale)", "$22.5M − ($7.3M + $2.25M + 300,000 × $50.00 − $2.1M)", "2027–29", True,
  ["As the base owned-cell case, but scrap stays at the first-year 8% of starts in 2028–29"])

# waterfall, $ per good unit over 2027–29 planning demand
D("wf_scr", "Scrap on started units, $ per good unit, 2027–29 average", -2.47, "$", "(v27 * (ownvar - own_u1) + (v28 + v29) * (ownvar - own_ul)) / vol_p", "(80,000 × −$4.00 + 220,000 × −$1.92) ÷ 300,000", "2027–29", True, OWN_A)
D("wf_fix", "Owned cell fixed staffing, $ per good unit, 2027–29", -7.5, "$", "(0 - own_fix3) * 1000000 / vol_p", "−$2.25M ÷ 300,000", "2027–29", True, OWN_A)
D("wf_cap", "Owned cell equipment and installation, $ per good unit, 2027–29", -24.33, "$", "(0 - own_capex) * 1000000 / vol_p", "−$7.3M ÷ 300,000", "2027–29", True, OWN_A)
D("wf_res", "Owned cell equipment resale, $ per good unit, 2027–29", 7.0, "$", "resale * 1000000 / vol_p", "$2.1M ÷ 300,000", "2027–29", True, OWN_A)
D("wf_net", "Owned cell like-for-like saving per good unit compared with buying, 2027–29", 1.70, "$", "cfo + freight + wf_scr + wf_fix + wf_cap + wf_res", "$27 + $2 − $2.47 − $7.50 − $24.33 + $7.00", "2027–29", True, OWN_A)

# cash and limits
D("own_cash_left", "Cash left after the owned cell's upfront outlay", 1.9, "$M", "cash_now - own_capex", "$9.2M − $7.3M", "2027", True,
  ["Today's $9.2M of available cash; other 2027 business cash flows are not in the briefing pack and are left out", "Owned cell's $7.3M paid in 2027"])
D("lease_cash_left", "Cash left after the leased cell's upfront outlay", 7.2, "$M", "cash_now - lease_inst", "$9.2M − $2.0M", "2027", True,
  ["Today's $9.2M of available cash; other 2027 business cash flows are left out", "Lease installation of $2.0M paid in 2027"])
D("own_cap_x", "Owned cell outlay as a multiple of the 2027 capital limit", 1.46, "x", "own_capex / capex_lim", "$7.3M ÷ $5.0M", "2027")
BUF_A = ["Buffer sized to bridge the second supplier's six-week notice period (team choice; the pack says only that emergency inventory may cover a one-week outage)",
         "2027 planning demand of 80,000 good units spread evenly over 52 weeks",
         "Stock valued at the $75 delivered price; carrying cost not yet modelled"]
D("buf_units", "Buffer stock: six weeks of 2027 planning demand", 9230, "housings", "v27 * emerg_wk / 52", "80,000 × 6 ÷ 52 weeks", "2027", True, BUF_A)
D("buf_val", "Cash tied up in the buffer stock", 0.69, "$M", "buf_units * sup_u / 1000000", "9,230 × $75", "2027", True, BUF_A)
D("plan_out", "2027 cash for the recommended plan: alternate-shop tooling plus buffer stock", 0.94, "$M", "alt_tool / 1000 + buf_val", "$0.25M + $0.69M", "2027", True, BUF_A)
D("plan_cash_left", "Cash left after the recommended plan's outlay", 8.26, "$M", "cash_now - plan_out", "$9.2M − $0.94M", "2027", True, BUF_A + ["Other 2027 business cash flows left out"])

# break-even
D("unit_gap", "Leased cell saving per good unit at 4% scrap compared with buying", 23.96, "$", "sup_u - lease_ul", "$75 − $51.04", "2028–29")
D("scr_prem", "Extra 2027 cost of the lease's 6% first-year scrap compared with 4%", 0.087, "$M", "v27 * (lease_u1 - lease_ul) / 1000000", "80,000 × ($52.13 − $51.04)", "2027", True, LEASE_A)
D("lease_rec", "Costs the leased cell must recover over 2027–29 before it saves money", 6.89, "$M", "lease_inst + lease_fix3 + scr_prem", "$2.0M + $4.8M + $0.09M", "2027–29", True, LEASE_A)
D("be_lease", "Break-even volume for the leased cell, good units, 2027–29", 287000, "good units", "lease_rec * 1000000 / unit_gap", "$6.89M ÷ $23.96", "2027–29", True,
  LEASE_A + ["Supplier delivered price stays at $75 for all three years"])
D("be_head", "Planning demand above the lease break-even volume", 0.045, "%", "vol_p / be_lease - 1", "300,000 ÷ 287,000 − 1", "2027–29", True, LEASE_A)
D("be_cons", "Conservative demand as a share of the lease break-even volume", 0.80, "%", "vol_c / be_lease", "230,000 ÷ 287,000", "2027–29", True, LEASE_A)
D("be_margin", "Planning demand above the lease break-even volume, good units", 13000, "good units", "vol_p - be_lease", "300,000 − 287,000", "2027–29")
D("be_share", "Lease break-even volume as a share of planning demand", 0.957, "%", "be_lease / vol_p", "287,000 ÷ 300,000", "2027–29", True, LEASE_A)

# lease started in 2028 (trigger analysis)
L28_A = ["Lease triggered at the Q3 2027 review and producing from January 2028 for two full years",
         "Scrap of 6% of starts in 2028 (first year) and 4% in 2029; $2.0M installation; $1.60M a year; no residual value after 2029",
         "Supplier delivered price $75 unless stated", "Nominal dollars; no tax or financing"]
D("vol_p2829", "Planning demand, good units, 2028–29", 220000, "units", "v28 + v29", "100,000 + 120,000", "2028–29")
D("vol_c2829", "Conservative demand, good units, 2028–29", 150000, "units", "c28 + c29", "65,000 + 85,000", "2028–29")
D("be28", "Break-even volume for a lease started in 2028, good units, 2028–29", 222000, "good units", "(lease_inst + 2 * lease_fix + v28 * (lease_u1 - lease_ul) / 1000000) * 1000000 / unit_gap", "($2.0M + 2 × $1.60M + 100,000 × $1.09) ÷ $23.96", "2028–29", True, L28_A)
D("lease_c2829", "Cost of a lease started in 2028, conservative demand, 2028–29", 12.93, "$M", "lease_inst + 2 * lease_fix + (c28 * lease_u1 + c29 * lease_ul) / 1000000", "$2.0M + $3.2M + 65,000 × $52.13 + 85,000 × $51.04", "2028–29", True, L28_A)
D("price_be_c", "Delivered supplier price above which a 2028 lease beats buying on conservative demand", 86.2, "$", "lease_c2829 * 1000000 / vol_c2829", "$12.93M ÷ 150,000", "2028–29", True, L28_A)
D("wf_keep", "Share of the CFO's claimed saving per housing that survives a like-for-like comparison", 0.063, "%", "wf_net / cfo", "$1.70 ÷ $27", "2027–29")
D("emerg_prem", "Premium of emergency second-supplier housings over the supplier's delivered price", 13, "$", "emerg - sup_u", "$88 − $75", "2027", definition="assumes the $88 quote is delivered; the pack does not say whether freight is extra")
D("otd_gap", "Supplier on-time delivery compared with the contract requirement", -0.2, "pp", "(otd - otd_req) * 100", "96.8% − 97%", "last reported", definition="orders basis compared with a requested-units requirement")
D("res_share", "Reserved supplier units as a share of 2027 planning demand", 0.5, "%", "reserved / v27", "40,000 ÷ 80,000", "2027")

D("buy2_p", "Buying with a second source: cost of housings plus alternate-shop tooling, planning demand, 2027–29", 22.75, "$M", "buy_p + alt_tool / 1000", "$22.5M + $0.25M", "2027–29", True, BUY_A0)
D("buy2_sav", "Cost of the second source compared with plain buying, 2027–29", -250, "$K", "(buy_p - buy2_p) * 1000", "$22.5M − $22.75M", "2027–29", True, BUY_A0)
D("buy2_sh", "Cost of the second source as a share of plain buying", -0.011, "%", "buy2_sav / 1000 / buy_p", "−$0.25M ÷ $22.5M", "2027–29", True, BUY_A0)
D("own_sav_2", "Owned cell saving compared with buying with a second source, planning demand", 0.76, "$M", "buy2_p - own_tot_p", "$22.75M − $21.99M", "2027–29", True, OWN_A)
D("lease_sav_2", "Leased cell saving compared with buying with a second source, planning demand", 0.55, "$M", "buy2_p - lease_tot_p", "$22.75M − $22.2M", "2027–29", True, LEASE_A)
D("be80", "Break-even volume for a lease started in 2028 if the delivered supplier price rose to $80", 183000, "good units", "(lease_inst + 2 * lease_fix + v28 * (lease_u1 - lease_ul) / 1000000) * 1000000 / (80 - lease_ul)", "$5.31M ÷ ($80 − $51.04)", "2028–29", True, L28_A + ["Illustrative renewal price of $80 per delivered housing"])
D("emerg_event", "Extra cost of one six-week emergency order at the second supplier's price", 0.12, "$M", "buf_units * emerg_prem / 1000000", "9,230 × $13", "2027", True, BUF_A + ["Emergency units priced at $88 compared with $75 delivered"])

# year-by-year backup
def yearly(prefix, label, vals, assumptions):
    for (yr, calc, formula, v) in vals:
        D(f"{prefix}{yr}", f"{label}, {yr}" if yr != "res" else f"{label}, resale after 2029", v, "$M", calc, formula, str(yr) if yr != "res" else "after 2029", True, assumptions)

BUY_A = ["Delivered price $75 per good unit, indicative after March 2027", "Nominal dollars; no tax or financing"]
yearly("bp", "Buying, planning demand", [(2027, "sup_u * v27 / 1000000", "$75 × 80,000", 6.0), (2028, "sup_u * v28 / 1000000", "$75 × 100,000", 7.5), (2029, "sup_u * v29 / 1000000", "$75 × 120,000", 9.0)], BUY_A)
yearly("bc", "Buying, conservative demand", [(2028, "sup_u * c28 / 1000000", "$75 × 65,000", 4.88), (2029, "sup_u * c29 / 1000000", "$75 × 85,000", 6.38)], BUY_A)
yearly("lp", "Leased cell, planning demand", [(2027, "lease_inst + lease_fix + v27 * lease_u1 / 1000000", "$2.0M + $1.60M + 80,000 × $52.13", 7.77), (2028, "lease_fix + v28 * lease_ul / 1000000", "$1.60M + 100,000 × $51.04", 6.70), (2029, "lease_fix + v29 * lease_ul / 1000000", "$1.60M + 120,000 × $51.04", 7.72)], LEASE_A)
yearly("lc", "Leased cell, conservative demand", [(2028, "lease_fix + c28 * lease_ul / 1000000", "$1.60M + 65,000 × $51.04", 4.92), (2029, "lease_fix + c29 * lease_ul / 1000000", "$1.60M + 85,000 × $51.04", 5.94)], LEASE_A)
yearly("op", "Owned cell, planning demand", [(2027, "own_capex + own_fix + v27 * own_u1 / 1000000", "$7.3M + $0.75M + 80,000 × $50.00", 12.05), (2028, "own_fix + v28 * own_ul / 1000000", "$0.75M + 100,000 × $47.92", 5.54), (2029, "own_fix + v29 * own_ul / 1000000", "$0.75M + 120,000 × $47.92", 6.50)], OWN_A)
yearly("oc", "Owned cell, conservative demand", [(2028, "own_fix + c28 * own_ul / 1000000", "$0.75M + 65,000 × $47.92", 3.86), (2029, "own_fix + c29 * own_ul / 1000000", "$0.75M + 85,000 × $47.92", 4.82)], OWN_A)
D("neg_res", "Owned cell equipment resale after 2029 (credit)", -2.1, "$M", "0 - resale", "−$2.1M", "after 2029")

# ------------------------------------------------------------------ storyline
GT = ("Keep buying housings in 2027, add a qualified second source and hold the leased cell as a gated option for 2028; "
      "the owned cell cannot be funded within the board's limits")

exec_summary = [
    {"id": "1", "text": "Like for like, the owned cell's $27 saving per housing shrinks to about $1.70",
     "supports": ["1", "2"],
     "sub_points": [
         {"text": "Operating savings repay only 78% of the $7.3M outlay by 2029", "slide_id": "1"},
         {"text": "Over 2027–29 the owned cell saves $0.51M and the lease $0.30M", "slide_id": "2"}]},
    {"id": "2", "text": "The owned cell breaks the board's limits, and the lease needs near-full demand",
     "supports": ["3", "4", "5"],
     "sub_points": [
         {"text": "The $7.3M outlay tops the $5.0M limit and leaves only $1.9M of cash", "slide_id": "3"},
         {"text": "On conservative demand the lease loses $1.4M, 4.6 times its upside", "slide_id": "4"}]},
    {"id": "3", "text": "Delivery, not insourcing, is the mandate; a second source protects it at lower cost",
     "supports": ["6", "7", "8"],
     "sub_points": [
         {"text": "On-time delivery sits just under 97%, hurt by one flood closure", "slide_id": "6"},
         {"text": "Four layers, from a second shop to reserved capacity, cover an outage", "slide_id": "8"}]},
    {"id": "4", "text": "Buy with a second source in 2027 and switch to the lease only if a trigger fires",
     "supports": ["9", "10", "11"],
     "sub_points": [
         {"text": "A 2028 lease is a near tie; orders, price or delivery would tip it", "slide_id": "10"},
         {"text": "Renew the supplier contract before the quote lapses in March 2027", "slide_id": "11"}]},
]

next_steps = [
    {"action": "Approve buying for 2027 and the $250K alternate-shop tooling; decline the owned-cell capital request", "owner": "Executive committee", "timing": "Jan 2027"},
    {"action": "Renew the supplier contract with split quarterly orders, 40,000 reserved units and indicative 2028–29 prices", "owner": "Procurement", "timing": "Before Mar 2027"},
    {"action": "Commission the lessor's site survey on power and ventilation, with no commitment to lease", "owner": "Operations", "timing": "Q1 2027"},
    {"action": "Model buffer-stock carrying cost and re-measure on-time delivery on the contract's requested-units basis", "owner": "Finance and supply chain", "timing": "Q1 2027"},
    {"action": "Review the three lease triggers against confirmed 2028 orders and the renewed supplier price", "owner": "CFO and VP Operations", "timing": "Q3 2027"},
]

sections = [
    {"id": "1", "title": "Like-for-like economics", "exec_item_id": "1", "tracker_label": "Economics"},
    {"id": "2", "title": "Board limits and demand risk", "exec_item_id": "2", "tracker_label": "Limits and risk"},
    {"id": "3", "title": "Protecting delivery", "exec_item_id": "3", "tracker_label": "Delivery"},
    {"id": "4", "title": "Recommendation and triggers", "exec_item_id": "4", "tracker_label": "Recommendation"},
]

slides = [{"id": "c", "role": "cover", "status": "filled"},
          {"id": "es", "role": "exec_summary", "status": "filled", "archetype": "exec-summary", "message_type": "navigation"}]


def div(sec):
    slides.append({"id": f"d{sec}", "role": "section_divider", "section_id": sec, "status": "filled", "archetype": "section-divider", "message_type": "navigation"})


SRC_NOTE = "Briefing pack figures; costs nominal, before tax and financing, 2027–29"

# ---- Section 1
div("1")
slides.append({
    "id": "1", "role": "content", "section_id": "1", "status": "filled",
    "lead_message": {"text": "The CFO's $27 saving per housing shrinks to about $1.70 once scrap, staffing and capital are counted on accepted units",
                     "numbers": [{"text": "$27", "data_ref": "cfo"}, {"text": "$1.70", "data_ref": "wf_net"}],
                     "highlights": ["Equipment and installation"], "clauses": 1},
    "message_type": "component", "archetype": "waterfall-bridge",
    "rationale": "What adds up from the claimed saving to the real one -> waterfall",
    "unit_line": "**Owned cell saving compared with buying**, $ per good housing, 2027–29 planning demand of 300,000 units",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {
        "kind": "big_number", "header": "Capital, the cost the CFO's slide left out, decides the case",
        "big_number": r("wf_keep"),
        "caption": "of the CFO's claimed saving per housing survives a like-for-like comparison",
        "bullets": ["**Capital:** operating savings repay only 78% of the $7.3M outlay by 2029, not the claimed payback in under three years",
                    "**Scrap and staffing:** the supplier is paid only for accepted units, while the cell pays for every start",
                    "**Resale:** without the dealer's non-binding indication, the bridge turns negative"]}},
    "body": {"kind": "chart", "chart_type": "waterfall",
             "categories": ["CFO's claimed saving", "Freight and inbound QA", "Scrap on started units", "Fixed staffing",
                            "Equipment and installation", "Resale after 2029", "Like-for-like saving"],
             "series": [{"name": "Saving per housing", "points": [r("cfo"), r("freight"), r("wf_scr"), r("wf_fix"), r("wf_cap"), r("wf_res"), r("wf_net")]}],
             "waterfall_steps": ["total", "step", "step", "step", "step", "step", "total"],
             "sort": "none", "highlight": ["Equipment and installation"], "value_format": "$0.00"},
    "footnotes": ["The CFO compared the $73 factory-gate price with the $46 variable cost per started unit; steps spread each cost over the 300,000 good units planned for 2027–29",
                  "Assumes the cell runs all of 2027; with a nine-month equipment lead time it would not, so the real saving is lower"],
})
slides.append({
    "id": "2", "role": "content", "section_id": "1", "status": "filled",
    "lead_message": {"text": "Neither cell beats buying by more than 2.3% over 2027–29, too thin a margin for Meridian's first production cell",
                     "numbers": [{"text": "2.3%", "data_ref": "own_sav_sh"}], "clauses": 1},
    "message_type": "item", "archetype": "data-table",
    "rationale": "Three options on the same cost lines -> data table",
    "unit_line": "**Cost of housings by sourcing option**, $ millions, 2027–29, planning demand of 300,000 good units",
    "layout": {"variant": "full"},
    "body": {"kind": "table", "table_type": "data",
             "columns": ["Upfront investment", "Fixed cost", "Unit cost on accepted units", "Resale after 2029", "Three-year cost", "Saving compared with buying", "Saving, % of buying cost"],
             "rows": [
                 {"label": "Buy from the supplier", "cells": [{"text": "None"}, {"text": "None"}, {"point": r("buy_p")}, {"text": "None"}, {"point": r("buy_p")}, {"text": "Baseline"}, {"text": "Baseline"}]},
                 {"label": "Buy with a second source", "cells": [{"point": r("alt_tool")}, {"text": "None"}, {"point": r("buy_p")}, {"text": "None"}, {"point": r("buy2_p")}, {"point": r("buy2_sav")}, {"point": r("buy2_sh")}]},
                 {"label": "Lease a flexible cell", "cells": [{"point": r("lease_inst")}, {"point": r("lease_fix3")}, {"point": r("lease_var_p")}, {"text": "None"}, {"point": r("lease_tot_p")}, {"point": r("lease_sav_p")}, {"point": r("lease_sav_sh")}]},
                 {"label": "Build an owned cell", "highlight": True, "cells": [{"point": r("own_capex")}, {"point": r("own_fix3")}, {"point": r("own_var_p")}, {"point": r("neg_res")}, {"point": r("own_tot_p")}, {"point": r("own_sav_p")}, {"point": r("own_sav_sh")}]},
                 {"label": "Owned cell, no resale", "cells": [{"point": r("own_capex")}, {"point": r("own_fix3")}, {"point": r("own_var_p")}, {"text": "None"}, {"point": r("own_tot_nr")}, {"point": r("own_sav_nr")}, {"text": "Costs more"}]},
             ]},
    "so_what": "If first-year scrap persists, both savings fall to about $0.05M: the case rests on scrap rates no one has run at full speed",
    "so_what_style": "line",
    "footnotes": ["Rounded; exact values in the source workbook. Buying: $73 plus $2 freight and QA per accepted unit. Cells: cost per start ÷ (1 − scrap); 8% owned, 6% leased in 2027, 4% after",
                  "Against buying with a second source the cells save $0.76M (owned) and $0.55M (lease), but a single cell needs a backup too. Full-year 2027 output flatters both cells"],
})

# ---- Section 2
div("2")
slides.append({
    "id": "3", "role": "content", "section_id": "2", "status": "filled",
    "lead_message": {"text": "The owned cell is out of reach in 2027: its $7.3M outlay breaks the $5.0M capital limit and the cash floor",
                     "numbers": [{"text": "$7.3M", "data_ref": "own_capex"}, {"text": "$5.0M", "data_ref": "capex_lim"}],
                     "highlights": ["Build an owned cell"], "clauses": 1},
    "message_type": "item", "archetype": "column-time-series",
    "rationale": "Each option's outlay against one limit -> column chart with the limit as a benchmark line",
    "unit_line": "**Upfront 2027 cash outlay by option**, $ millions, against the capital limit approvable without new financing",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {
        "kind": "big_number", "header": "Only a new financing agreement would make the owned cell possible",
        "big_number": r("own_cash_left"),
        "caption": "of cash would be left after the owned cell's outlay, below the $4.0M year-end floor",
        "bullets": ["**Owned cell:** an outlay 1.46 times the limit, for capacity of 120,000 that leaves no headroom over 2029 demand",
                    "**Leased cell:** fits both limits, leaving $7.2M after installation, but commits $1.6M a year to lease and staffing",
                    "**Buy with a second source:** the smallest outlay, and most of it is stock that can be drawn down"]}},
    "body": {"kind": "chart", "chart_type": "column",
             "categories": ["Build an owned cell", "Lease a flexible cell", "Buy with a second source"],
             "series": [{"name": "2027 outlay", "points": [r("own_capex"), r("lease_inst"), r("plan_out")]}],
             "sort": "none", "highlight": ["Build an owned cell"], "value_format": "$0.00M",
             "benchmark": {"label": "Capital limit", "point": r("capex_lim")}},
    "basis": {"header": "How we sized the second-source plan", "terms": [
        {"point": r("alt_tool"), "caption": "dedicated tooling at the alternate approved shop"},
        {"op": "+", "point": r("buf_val"), "caption": "six weeks of 2027 demand as buffer stock, at $75 delivered"},
        {"op": "=", "point": r("plan_out"), "caption": "2027 cash for the second-source plan"}]},
    "footnotes": ["Cash test uses today's $9.2M of available cash; other 2027 business cash flows are not in the briefing pack. Lease installation counted as capital spending (conservative)"],
})
slides.append({
    "id": "4", "role": "content", "section_id": "2", "status": "filled",
    "lead_message": {"text": "If demand falls to the conservative case, either cell loses about $1.4M, far more than it gains if the plan holds",
                     "numbers": [{"text": "$1.4M", "data_ref": "lease_sav_c"}],
                     "highlights": ["Lease, conservative demand", "Own, conservative demand"], "clauses": 1},
    "message_type": "item", "archetype": "bar-ranking",
    "rationale": "Same metric for two options under two scenarios -> bar chart, downside bars highlighted",
    "unit_line": "**Saving compared with buying**, $ millions, 2027–29, by option and demand case",
    "layout": {"variant": "takeaway_sidebar", "sidebar": {
        "kind": "big_number", "header": "The downside is several times the upside",
        "big_number": r("lease_ratio"),
        "caption": "the lease's conservative-case loss as a multiple of its planning-case gain",
        "bullets": ["**Conservative demand:** 70,000 fewer housings carry the same fixed costs",
                    "**Owned cell:** loses on conservative demand even with the $2.1M resale"],
        "implication": "Insourcing makes a variable cost fixed before demand is secure"}},
    "body": {"kind": "chart", "chart_type": "bar",
             "categories": ["Lease, planning demand", "Lease, conservative demand", "Own, planning demand", "Own, conservative demand"],
             "series": [{"name": "Saving compared with buying", "points": [r("lease_sav_p"), r("lease_sav_c"), r("own_sav_p"), r("own_sav_c")]}],
             "sort": "none", "highlight": ["Lease, conservative demand", "Own, conservative demand"], "value_format": "$0.00M"},
    "footnotes": ["Planning demand 80,000, 100,000 and 120,000 good units in 2027–29; conservative 80,000, 65,000 and 85,000. Owned cell includes the $2.1M resale"],
})
slides.append({
    "id": "5", "role": "content", "section_id": "2", "status": "filled",
    "lead_message": {"text": "The lease pays back only above about 287,000 good units over 2027–29, close to the full uncommitted forecast",
                     "numbers": [{"text": "287,000", "data_ref": "be_lease"}], "clauses": 1},
    "message_type": "component", "archetype": "calculation-bridge",
    "rationale": "Our own break-even estimate and how it is built -> calculation bridge (B-08)",
    "unit_line": "**Leased cell break-even volume**, good units, 2027–29",
    "body": {"kind": "equation", "terms": [
        {"point": r("lease_rec"), "caption": "costs the lease must recover: $2.0M installation, $4.8M lease and staffing, $0.087M extra first-year scrap"},
        {"op": "÷", "point": r("unit_gap"), "caption": "saved on each good housing: $75 delivered purchase compared with $51.04 at 4% scrap"},
        {"op": "=", "point": r("be_lease"), "caption": "good housings needed over 2027–29 before the lease saves money"}],
        "assumptions_header": "The margin above break-even is thin, and every assumption cuts toward it",
        "assumptions": ["Planning demand of 300,000 is only 4.5% above break-even; the conservative 230,000 reaches 80% of it",
                        "The supplier's $75 delivered price holds for three years, though it is quoted only to March 2027",
                        "Lease scrap falls from 6% to 4% after 2027; if it stays at 6%, the three-year saving drops to $0.06M",
                        "The lease runs all of 2027; a five-month deployment after a site survey means fewer units to spread its costs over"]},
    "footnotes": ["Break-even = costs to recover ÷ saving per good unit; 2027 scrap premium = 80,000 × ($52.13 − $51.04). Planning demand clears break-even by only about 13,000 units"],
})

# ---- Section 3
div("3")
slides.append({
    "id": "6", "role": "content", "section_id": "3", "status": "filled",
    "lead_message": {"text": "The supplier's on-time record sits just under the requirement, and one flood closure explains most of the misses",
                     "clauses": 1},
    "message_type": "item", "archetype": "kpi-big-numbers",
    "rationale": "Three facts that size the supplier problem -> KPI tiles",
    "unit_line": "**Supplier delivery performance and capacity**, latest reported",
    "body": {"kind": "kpi", "items": [
        {"point": r("otd"), "caption": "of supplier orders delivered within ten business days",
         "drivers": ["Late deliveries were concentrated during one flood-related road closure",
                     "A customer audit found two late shipments last quarter",
                     "Measured on orders; the contract counts requested units, so re-measure on that basis"]},
        {"point": r("otd_gap"), "caption": "gap to the 97% requirement, on an orders basis",
         "drivers": ["The customer mandates delivery reliability and dimensional quality, not insourcing",
                     "Losing the designation would also hit electronics and software sales; not yet quantified",
                     "Misses from one road closure call for route and source redundancy, not a factory"]},
        {"point": r("cap_sup"), "caption": "housings a year of supplier capacity, if renewed",
         "drivers": ["Covers the 120,000 good units planned for 2029",
                     "The supplier will split quarterly orders and reserve 40,000 units on ninety days' notice",
                     "Pricing and capacity after 2027 are indicative, with no take-or-pay commitment"]}]},
    "so_what": "The weakness is reliance on one shop and one route; a second source fixes it without new capital",
    "so_what_style": "bar",
    "footnotes": ["Supplier figure is the share of orders; the contract requirement is the share of requested units shipped within ten business days"],
})
slides.append({
    "id": "7", "role": "content", "section_id": "3", "status": "filled",
    "lead_message": {"text": "Neither the demo cell nor the plants with machine shops show that owning machinery would make deliveries more reliable",
                     "clauses": 1},
    "message_type": "argument", "archetype": "text-columns",
    "rationale": "Three pieces of evidence for insourcing, each weaker than claimed -> text columns",
    "body": {"kind": "text", "style": "columns", "columns": [
        {"header": "The demo yield overstates what a new cell would deliver", "point": r("demo_yield"),
         "point_caption": "demonstration-cell yield on the internal dashboard",
         "detail": ["Excludes start-up runs, rework and three days down for a tooling change",
                    "With those included, the process engineer plans 8% scrap in year one",
                    "Same material, but the new housing never ran at full production speed"],
         "footer": "Plan on 8% first-year scrap"},
        {"header": "Plants with machine shops differ in more than ownership",
         "detail": ["They recorded fewer delivery delays last year",
                    "They also shipped larger, steadier volumes of different products",
                    "No before-and-after evidence isolates the effect of insourcing",
                    "The board was advised not to treat the link as causal"],
         "footer": "A correlation, not a cause"},
        {"header": "Insourcing adds delivery risks of its own in 2027", "point": r("lead_eq"),
         "point_caption": "months from equipment order to delivery",
         "detail": ["An owned cell approved in January would not run until late 2027",
                    "Meridian has never operated a production machining cell",
                    "The lease's five-month deployment depends on a site survey of power and ventilation"],
         "footer": "A new cell is a reliability risk first", "emphasis": True}]},
    "footnotes": ["No design change can be made until customer dimensional testing is complete, so any cell would start on the existing specification"],
})
slides.append({
    "id": "8", "role": "content", "section_id": "3", "status": "filled",
    "lead_message": {"text": "Four layers of supply protection would keep housings flowing through an outage without building a cell",
                     "count_word": 4, "clauses": 1},
    "message_type": "structure", "archetype": "process-flow",
    "rationale": "Protection that activates in sequence over time -> process flow",
    "layout": {"variant": "full"},
    "body": {"kind": "process", "steps": [
        {"header": "Always on: run the alternate shop in parallel", "point": r("alt_tool"),
         "point_caption": "dedicated tooling at the alternate approved shop",
         "detail": ["Qualify a shop off the flood-affected route",
                    "Split quarterly orders once it quotes a unit price",
                    "Ends the single-shop dependency"],
         "footer": "Owner: procurement", "emphasis": True},
        {"header": "Week 1: draw on buffer stock", "point": r("emerg_wk"),
         "point_caption": "weeks of stock, the second supplier's notice period",
         "detail": ["Covers a short outage", "About 9,230 housings, $0.69M of cash",
                    "Carrying cost still to be modelled"],
         "footer": "Trigger: any missed shipment"},
        {"header": "Week 6: second supplier", "point": r("emerg"),
         "point_caption": "per accepted unit, emergency orders",
         "detail": ["For outages beyond the buffer", "Costs $13 more per housing", "A six-week order adds about $0.12M"],
         "footer": "Trigger: outage over a week"},
        {"header": "After ninety days: use reserved capacity", "point": r("reserved"),
         "point_caption": "reserved supplier units on ninety days' notice",
         "detail": ["Agreed in the March 2027 renewal", "Half of the 80,000 planned for 2027", "Absorbs demand above plan"],
         "footer": "Trigger: orders above plan"}]},
    "callout": {"target": "Always on: run the alternate shop in parallel", "header": "The decisive layer",
                "detail": "The only layer that removes the dependence on one shop instead of bridging it"},
    "footnotes": ["Six-week buffer is our choice (the pack says inventory may cover a one-week outage); sizing on p. 7. The alternate shop has no unit price in the pack; the $88 quote may exclude freight"],
})

# ---- Section 4
div("4")
slides.append({
    "id": "9", "role": "content", "section_id": "4", "status": "filled",
    "lead_message": {"text": "Only buying with a second source fits the board's limits, survives weak demand and protects deliveries in 2027",
                     "clauses": 1},
    "message_type": "item", "archetype": "harvey-ball-table",
    "rationale": "Three options on the same criteria, mostly judged -> harvey-ball table with one numeric column",
    "unit_line": "**Sourcing options on the decision criteria**, team assessment from the briefing pack; saving in $ millions, 2027–29",
    "layout": {"variant": "full"},
    "body": {"kind": "table", "table_type": "harvey",
             "columns": ["Saving compared with buying", "Fits capital and cash limits", "Protects delivery in 2027", "Holds if demand falls", "Proven operation"],
             "rows": [
                 {"label": "Build an owned cell", "cells": [{"point": r("own_sav_p")}, {"rating": 0}, {"rating": 1}, {"rating": 1}, {"rating": 0}],
                  "note": "Reject: needs new financing and rests on a non-binding resale"},
                 {"label": "Lease a flexible cell", "cells": [{"point": r("lease_sav_p")}, {"rating": 4}, {"rating": 2}, {"rating": 1}, {"rating": 1}],
                  "note": "Prepare, do not sign: pays only near full forecast"},
                 {"label": "Buy with a second source", "highlight": True, "cells": [{"text": "Baseline"}, {"rating": 4}, {"rating": 3}, {"rating": 4}, {"rating": 3}],
                  "note": "Recommend for 2027"}],
             "legend": "Full circle = best of the three options on that criterion; team judgment from the briefing pack evidence"},
    "callout": {"target": "Buy with a second source", "header": "Recommended",
                "detail": "Meets every limit, closes the delivery gap and keeps the lease open for 2028"},
    "footnotes": ["Protects delivery: owned cell not running until late 2027; lease depends on a site survey and five-month deployment; second source needs tooling and qualification but no new plant"],
})
slides.append({
    "id": "10", "role": "content", "section_id": "4", "status": "filled",
    "lead_message": {"text": "A 2028 lease is a near tie at today's price and plan volume, so three triggers decide whether to switch",
                     "count_word": 3, "clauses": 1},
    "message_type": "argument", "archetype": "numbered-levers",
    "rationale": "N conditions that change the answer -> numbered levers with thresholds",
    "unit_line": "**Triggers for a 2028 lease**, thresholds for a lease producing in 2028–29",
    "body": {"kind": "levers", "headers": ["Trigger", "Threshold"], "items": [
        {"code": "1", "text": "Demand: firm or take-or-pay orders for 2028–29 reach break-even at today's $75 price",
         "point": r("be28"), "metric": "good units in 2028–29 for a 2028 lease to break even, against 220,000 planned"},
        {"code": "2", "text": "Price: the renewed 2028–29 price rises enough that the lease wins even on conservative demand",
         "point": r("price_be_c"), "metric": "per delivered housing, the price above which a 2028 lease wins even on conservative demand"},
        {"code": "3", "text": "Delivery: on-time delivery stays below the contract level after the second source is running",
         "point": r("otd_req"), "metric": "of requested units within ten business days, the contract requirement"}]},
    "so_what": "Any trigger needs the lessor's site survey on power and ventilation passed first, so commission it now",
    "so_what_style": "bar",
    "footnotes": ["At an $80 renewal price a 2028 lease would need about 183,000 units. Decide by end-September 2027 so a five-month deployment produces from January 2028"],
})
slides.append({
    "id": "11", "role": "content", "section_id": "4", "status": "filled",
    "lead_message": {"text": "The supplier contract must be renewed before the quote lapses in March 2027; the lease decision waits for the third quarter",
                     "clauses": 1},
    "message_type": "structure", "archetype": "timeline-roadmap",
    "rationale": "Actions with dates -> timeline",
    "unit_line": "**Implementation plan**, January 2027 to 2028",
    "layout": {"variant": "full"},
    "body": {"kind": "timeline", "periods": ["Jan 2027", "Feb 2027", "Mar 2027", "Q2 2027", "Q3 2027", "Q4 2027", "2028"],
             "rows": [
                 {"label": "Decision", "bars": [{"start": "Jan 2027", "end": "Jan 2027", "label": "Committee decides", "emphasis": True}]},
                 {"label": "Supplier contract", "bars": [{"start": "Jan 2027", "end": "Mar 2027", "label": "Renew: split orders, 40,000 reserved units", "emphasis": True}]},
                 {"label": "Alternate shop", "bars": [{"start": "Feb 2027", "end": "Q2 2027", "label": "Tooling and qualification"}]},
                 {"label": "Buffer stock", "bars": [{"start": "Feb 2027", "end": "Q2 2027", "label": "Model carrying cost, build stock"}]},
                 {"label": "Lease option", "bars": [{"start": "Feb 2027", "end": "Q2 2027", "label": "Site survey"},
                                                    {"start": "Q3 2027", "end": "Q3 2027", "label": "Trigger review", "emphasis": True},
                                                    {"start": "Q4 2027", "end": "2028", "label": "Deploy only if triggered"}]}],
             "milestones": [{"at": "Mar 2027", "label": "Quote lapses"}]},
    "so_what": "Missing the March renewal would leave Meridian buying without a price, which is the one outcome this plan must avoid",
    "so_what_style": "line",
    "footnotes": ["The supplier quote assumes the existing housing specification; a change after customer dimensional testing would need a new quote"],
})

# ---- Backup
slides.append({"id": "app", "role": "appendix_divider", "status": "filled"})
slides.append({
    "id": "b1", "role": "backup", "backup_of": "2", "section_id": "1", "status": "filled",
    "lead_message": {"text": "BACKUP: Year by year, the cells' upfront costs land in 2027, before volumes grow into them", "clauses": 1},
    "message_type": "item", "archetype": "data-table",
    "rationale": "Year-by-year build-up behind the three-year totals -> data table",
    "unit_line": "**Cost of housings by option and year**, $ millions, nominal, planning and conservative demand",
    "layout": {"variant": "full"},
    "body": {"kind": "table", "table_type": "data", "columns": ["2027", "2028", "2029", "Resale", "2027–29"],
             "rows": [
                 {"label": "Buy, planning", "cells": [{"point": r("bp2027")}, {"point": r("bp2028")}, {"point": r("bp2029")}, {"text": "None"}, {"point": r("buy_p")}]},
                 {"label": "Lease, planning", "cells": [{"point": r("lp2027")}, {"point": r("lp2028")}, {"point": r("lp2029")}, {"text": "None"}, {"point": r("lease_tot_p")}]},
                 {"label": "Own, planning", "highlight": True, "cells": [{"point": r("op2027")}, {"point": r("op2028")}, {"point": r("op2029")}, {"point": r("neg_res")}, {"point": r("own_tot_p")}]},
                 {"label": "Buy, conservative", "cells": [{"point": r("bp2027")}, {"point": r("bc2028")}, {"point": r("bc2029")}, {"text": "None"}, {"point": r("buy_c")}]},
                 {"label": "Lease, conservative", "cells": [{"point": r("lp2027")}, {"point": r("lc2028")}, {"point": r("lc2029")}, {"text": "None"}, {"point": r("lease_tot_c")}]},
                 {"label": "Own, conservative", "cells": [{"point": r("op2027")}, {"point": r("oc2028")}, {"point": r("oc2029")}, {"point": r("neg_res")}, {"point": r("own_tot_c")}]}]},
    "footnotes": ["2027 includes upfront investment: $7.3M owned, $2.0M lease. Unit costs on accepted units: buy $75; own $50.00 in 2027 and $47.92 after; lease $52.13 and $51.04",
                  "Both cells modelled as producing all of 2027, which their lead times rule out; nominal, before tax and financing"],
})
slides.append({"id": "end", "role": "end_page", "status": "filled"})

decision_audit = {
    "constraints": [
        {"item": "$5.0M limit on new 2027 capital spending without a new financing agreement", "reflected": True,
         "effect": "the owned cell's $7.3M breaks it; lease installation counted against it and fits", "slide_ids": ["3", "9"]},
        {"item": "Year-end unrestricted cash above $4.0M, from $9.2M today, no new debt or equity", "reflected": True,
         "effect": "the owned cell would leave $1.9M before other cash flows; the plan leaves $8.26M", "slide_ids": ["3"]},
        {"item": "Supplier paid on accepted units; cells pay for scrap on every start (8% and 6% in 2027, 4% after)", "reflected": True,
         "effect": "scrap and like-for-like unit costs are in every cost number", "slide_ids": ["1", "2", "5"]},
        {"item": "Fixed costs, upfront installation and $2 freight that the CFO's slide left out", "reflected": True,
         "effect": "they are the bridge from $27 to $1.70 per housing", "slide_ids": ["1"]},
        {"item": "Nine-month equipment lead time and five-month lease deployment", "reflected": False,
         "effect": "the model assumes full-year 2027 output for both cells, which flatters them; titles say savings are thin even so and footnotes flag it", "slide_ids": ["1", "2", "5", "7"]},
        {"item": "Supplier quote lapses in March 2027 and assumes the current specification; later prices are indicative", "reflected": True,
         "effect": "renewal before March is the first action; the price trigger covers a higher renewal", "slide_ids": ["10", "11"]},
        {"item": "Alternate shop's unit price is not in the briefing pack", "reflected": False,
         "effect": "the plan splits orders only after the shop quotes; the $0.25M tooling is shown as the second source's cost against plain buying", "slide_ids": ["2", "8"]},
        {"item": "Supplier price after March 2027 is indicative, with no take-or-pay", "reflected": True,
         "effect": "a 2028 lease is a near tie at $75 on plan volume; the price trigger and the $80 midpoint show how fast it tips", "slide_ids": ["10"]},
        {"item": "Buffer-stock carrying cost not modelled; unquantified loss if the customer designation is lost", "reflected": False,
         "effect": "the plan's cash includes the stock's value but not its carrying cost; both are named on the slides and in next steps", "slide_ids": ["6", "8"]},
    ],
    "alternatives": [
        {"option": "Lease the flexible cell now: it fits both limits, deploys in five months and saves $0.30M on planning demand",
         "verdict": "combined", "why": "the saving is 1.3% of purchases and turns into a $1.38M loss on conservative demand; break-even needs 96% of an unguaranteed forecast. Kept as a prepared option with triggers",
         "triage": "body", "slide_ids": ["4", "5", "9", "10"]},
        {"option": "Keep buying without the alternate-shop tooling, relying on buffer stock, $88 emergency orders and reserved units",
         "verdict": "rejected", "why": "it keeps the one-shop dependency the customer audit flagged; the $0.25M tooling costs about two six-week emergency orders at the $13 premium",
         "triage": "body", "slide_ids": ["8"]},
        {"option": "Phased owned cell: a smaller first capital request within the $5.0M limit",
         "verdict": "rejected", "why": "the pack gives no phased equipment costs, the full cell saves only $0.51M with resale, and the nine-month lead time means no 2027 output; the lease is the cheaper staged route to in-house capacity",
         "triage": "body", "slide_ids": ["3", "9"]},
    ],
    "failure_threshold": {
        "driver": "committed 2028–29 volume and the renewed supplier price",
        "threshold": "a 2028 lease beats buying above about 222,000 good units in 2028–29 (220,000 planned) or, even on conservative demand, above about $86 per delivered housing",
        "range": "lease saving compared with buying, 2027–29: low −$1.38M (conservative), base +$0.30M (planning), +$0.06M if scrap stays at 6%; the pack has no demand case above plan",
        "triage": "body", "slide_ids": ["4", "5", "10"]},
    "consistency": {"headline": GT, "holds": True,
                    "fix": "Governing thought changed from 'drop the owned cell' to 'cannot be funded within the board's limits'; the supplier title no longer compares the orders-based 96.8% with the units-based 97% as a like-for-like gap; the trigger title admits a 2028 lease is a near tie at plan volume"},
}

spec = {
    "spec_version": "0.1", "mode": "deck_detailed",
    "meta": {"title": "Precision housings: make, lease or buy in 2027", "subtitle": "Executive committee decision, January 2027",
             "company_name": "Meridian Motion", "audience": "Executive committee",
             "purpose": "Decide whether to make precision housings in-house in 2027, lease a flexible cell, or keep buying",
             "date": "2026-11-20", "language": "en-US", "confidentiality": "Synthetic benchmark data; every number from the briefing pack", "theme": "navy"},
    "inputs": [{"id": "in-1", "kind": "file", "label": "Meridian Motion briefing pack (c6)", "content": "evidence/briefing-pack.md"}],
    "storyline": {"governing_thought": GT, "exec_summary": exec_summary, "next_steps": next_steps},
    "decision_audit": decision_audit,
    "sections": sections, "slides": slides,
    "data_points": [], "sources": [
        {"id": "s1", "kind": "user_provided", "name": "Meridian Motion briefing pack", "input_id": "in-1"},
        {"id": "s0", "kind": "derived", "name": "Team analysis of the briefing pack"}],
}

# slide_id = first slide that shows the number; inputs not shown take the slide of their first dependent
order = [s["id"] for s in slides]
first = {}
def walk(o, sid):
    if isinstance(o, dict):
        if "data_ref" in o and o["data_ref"] not in first: first[o["data_ref"]] = sid
        for v in o.values(): walk(v, sid)
    elif isinstance(o, list):
        for v in o: walk(v, sid)
for s in slides:
    walk({k: v for k, v in s.items() if k != "lead_message"}, s["id"])
    walk(s.get("lead_message", {}), s["id"])
missing = [i for i in DP if i not in first]
changed = True
while changed:
    changed = False
    for i in ORDER:
        if i in first: continue
        deps = [first[j] for j in ORDER if j in first and i in DP[j].get("derived_from", [])]
        if deps:
            first[i] = min(deps, key=order.index); changed = True
for i in ORDER:
    DP[i]["slide_id"] = first.get(i, "1")
    DP[i]["used_in"] = "shown on slide" if i not in missing else "input to a calculation"
ESTIMATES = {"buf_units", "buf_val", "plan_out", "plan_cash_left", "emerg_event", "be80"}
for i in ORDER:
    if DP[i].get("estimate") and i not in ESTIMATES:
        del DP[i]["estimate"]
spec["data_points"] = [DP[i] for i in ORDER]
json.dump(spec, open(OUT, "w"), indent=2, ensure_ascii=False)
print("wrote", OUT, len(DP), "data points;", "not on any slide:", len([i for i in DP if i not in first]))
