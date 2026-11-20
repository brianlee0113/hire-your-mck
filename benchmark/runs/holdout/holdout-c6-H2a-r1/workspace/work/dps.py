# Data points for the Meridian Motion housings deck. Every value is either quoted from the briefing pack (bp),
# quoted from the finished analysis (an, only for the analysis's own planning choices), or derived with calc.
DPS = []


def dp(id, slide, label, value, unit, src="bp", excerpt=None, locator=None, period=None, derived=None, formula=None,
       calc=None, estimate=False, assumptions=None, used_in=None, definition=None):
    d = {"id": id, "slide_id": slide, "label": label, "value": value, "unit": unit, "source_id": src}
    if period: d["period"] = period
    if excerpt: d["excerpt"] = excerpt
    if locator: d["locator"] = locator
    if derived:
        d["derived_from"] = derived
        d["formula"] = formula
        d["calc"] = calc
        d["source_id"] = "calc"
    if estimate:
        d["estimate"] = True
        d["assumptions"] = assumptions or []
    if used_in: d["used_in"] = used_in
    if definition: d["definition"] = definition
    DPS.append(d)


# ---- briefing pack, quoted ------------------------------------------------------------------------
ROW_UNIT = "| Quoted unit cost | $73 at supplier gate | $46 per unit started | $49 per unit started |"
ROW_FRT = "| Freight and inbound QA | $2 per good unit | included in variable cost | included in variable cost |"
ROW_INV = "| Initial investment | None; optional alternate-shop tooling $0.25M | $6.5M equipment + $0.8M installation | $2.0M installation and training |"
ROW_FIX = "| Recurring fixed cost | none beyond quoted price | $0.75M per year | $1.60M annual lease and staffing |"
ROW_S1 = "| First-year scrap | supplier price covers rejects | 8% of starts | 6% of starts |"
ROW_S2 = "| Later-year scrap | supplier price covers rejects | 4% of starts | 4% of starts |"
ROW_CAP = "| Practical annual output | up to 140,000 if renewed | 120,000 accepted units | 125,000 accepted units |"
VOL = "Housing demand planning assumes 80,000 good units in 2027, 100,000 in 2028 and 120,000 in 2029."
T3 = "§3 Economics and quotations, table"

dp("gate73", "3b", "Supplier quoted price at the supplier gate, per good unit", 73, "$", excerpt=ROW_UNIT, locator=T3 + ", Quoted unit cost")
dp("own46", "3b", "Owned cell variable cost per unit started", 46, "$", excerpt=ROW_UNIT, locator=T3 + ", Quoted unit cost")
dp("lease49", "3b", "Leased cell variable cost per unit started", 49, "$", excerpt=ROW_UNIT, locator=T3 + ", Quoted unit cost")
dp("frt2", "3b", "Supplier freight and inbound QA per good unit", 2, "$", excerpt=ROW_FRT, locator=T3 + ", Freight and inbound QA")
dp("tool025", "3b", "Optional alternate-shop tooling charge", 0.25, "$M", excerpt=ROW_INV, locator=T3 + ", Initial investment")
dp("own_eq", "3b", "Owned cell equipment", 6.5, "$M", excerpt=ROW_INV, locator=T3 + ", Initial investment")
dp("own_inst", "3b", "Owned cell installation", 0.8, "$M", excerpt=ROW_INV, locator=T3 + ", Initial investment")
dp("lease_up", "3b", "Leased cell installation and training (upfront)", 2.0, "$M", excerpt=ROW_INV, locator=T3 + ", Initial investment")
dp("own_fix", "3b", "Owned cell fixed staffing per year", 0.75, "$M", excerpt=ROW_FIX, locator=T3 + ", Recurring fixed cost")
dp("lease_fix", "3b", "Leased cell annual lease and staffing", 1.6, "$M", excerpt=ROW_FIX, locator=T3 + ", Recurring fixed cost")
dp("own_s1", "3b", "Owned cell first-year scrap, share of starts", 0.08, "%", excerpt=ROW_S1, locator=T3 + ", First-year scrap")
dp("lease_s1", "3b", "Leased cell first-year scrap, share of starts", 0.06, "%", excerpt=ROW_S1, locator=T3 + ", First-year scrap")
dp("s_later", "3b", "Later-year scrap for either cell, share of starts", 0.04, "%", excerpt=ROW_S2, locator=T3 + ", Later-year scrap")
dp("cap_buy", "3b", "Supplier practical annual output if renewed", 140, "k", excerpt=ROW_CAP, locator=T3 + ", Practical annual output", definition="thousand units a year")
dp("cap_own", "3b", "Owned cell practical annual output", 120, "k", excerpt=ROW_CAP, locator=T3 + ", Practical annual output", definition="thousand accepted units a year")
dp("cap_lease", "3b", "Leased cell practical annual output", 125, "k", excerpt=ROW_CAP, locator=T3 + ", Practical annual output", definition="thousand accepted units a year")
dp("resale", "3b", "Owned cell equipment resale after 2029 (dealer indication, not binding)", 2.1, "$M",
   excerpt="Build equipment could be sold for an estimated $2.1M after 2029, but a dealer's indication is not a binding offer.", locator="§3, below the table")
dp("lt_own", "3b", "Lead time for new equipment orders", 9, "months", locator='§5: "the head of Finance notes that new equipment orders take nine months"')
dp("lt_lease", "3b", "Leased cell deployment time if the site survey passes", 5, "months", locator='§5: "The lease company promises a five-month deployment if its site survey passes."')

dp("caplim", "3", "New 2027 capital that can be approved without new financing", 5.0, "$M",
   excerpt="At most **$5.0M of new 2027 capital spending** can be approved without a new financing agreement.", locator="§2 Constraints agreed by the board")
dp("floor", "3", "Minimum year-end unrestricted cash", 4.0, "$M",
   excerpt="Separately, year-end unrestricted cash must remain above **$4.0M**.", locator="§2 Constraints agreed by the board")
dp("cash0", "3", "Available cash today", 9.2, "$M",
   excerpt="Today's available cash is **$9.2M** and no debt or equity increase is approved.", locator="§2 Constraints agreed by the board")
dp("v27", "3", "Good housings, 2027 (both demand cases)", 80, "k", excerpt=VOL, locator="§2 and §4 volume table", definition="thousand good units")
dp("v28p", "3", "Good housings, 2028, planning case", 100, "k", excerpt=VOL, locator="§2 and §4 volume table", definition="thousand good units")
dp("v29p", "3", "Good housings, 2029, planning case", 120, "k", excerpt=VOL, locator="§2 and §4 volume table", definition="thousand good units")
dp("v28c", "3", "Good housings, 2028, conservative case", 65, "k",
   excerpt="The major customer's forecast is not a guaranteed order; the conservative 2028 case is 65,000 units.", locator="§2", definition="thousand good units")
dp("v29c", "3", "Good housings, 2029, conservative case", 85, "k", excerpt="| Conservative demand | 80,000 | 65,000 | 85,000 |",
   locator="§4 volume table, Conservative demand", definition="thousand good units")
dp("otd_req", "3", "Customer requirement: share of requested units shipped within ten business days", 0.97, "%",
   excerpt="A customer delivery contract requires 97% of requested units to ship within ten business days.", locator="§2")
dp("otd", "4", "Supplier on-time delivery within ten business days, trailing", 0.968, "%",
   excerpt="The supplier has delivered 96.8% of orders within ten business days, slightly below the customer requirement, but late deliveries were concentrated during one flood-related road closure.",
   locator="§4")
dp("demo", "4", "Demonstration cell production yield on the internal dashboard", 0.985, "%",
   excerpt="An internal dashboard reports **98.5% production yield** for the demonstration cell.", locator="§4")
dp("res40", "10", "Supplier reserved units available on notice", 40, "k",
   excerpt="The supplier can provide 40,000 reserved units after giving ninety days' notice.", locator="§2", definition="thousand units")
dp("notice_res", "10", "Notice period for the supplier's reserved units", 90, "days", locator='§2: "after giving ninety days\' notice"')
dp("emg88", "10", "Second approved supplier, emergency price per accepted unit", 88, "$",
   excerpt="A second approved supplier is available for emergency orders at $88 per accepted unit with six-week notice.", locator="§4")
dp("notice_emg", "10", "Notice period for the emergency supplier", 6, "weeks", locator='§4: "with six-week notice"')
dp("cfo27", "6", "Saving per housing on the circulated CFO slide ($73 against $46)", 27, "$",
   excerpt="Buying at $73 versus making at $46 saves $27 on every housing; at 100,000 units the payback is under three years.", locator="§5 Internal presentation circulated to management")
dp("proc75", "6", "Supplier freight-inclusive price on the procurement chart", 75, "$",
   excerpt="A separate procurement chart labels the supplier's freight-inclusive price as $75; it is not a second quote.", locator="§5")

# ---- the analysis's own planning choices (not in the pack) ------------------------------------------
dp("wks50", "11", "Shipping weeks a year used to size the buffer", 50, "weeks", src="an",
   excerpt="Buffer = 6 weeks × 1,600 units/week (80k ÷ 50 weeks) × $75", locator="Analysis slide 11, source line")
dp("carry_rate", "15", "Assumed annual inventory carrying cost rate", 0.25, "%", src="an",
   excerpt="At an assumed 25% a year the buffer adds ~$0.5M over 2027–29", locator="Analysis slide 15, Inventory carrying cost row")
dp("split25", "11", "Share of volume proposed for the alternate shop", 0.25, "%", src="an",
   excerpt="split quarterly orders (e.g. ~25% of volume)", locator="Analysis slide 11, Layer 2")
dp("emg_frt", "11", "Freight and QA assumed on top of the emergency price", 2, "$", src="an",
   excerpt="Emergency premium assumes $2 freight/QA on top of $88", locator="Analysis slide 11, source line")
dp("dec12", "13", "Lead time for deciding on an owned cell before capacity is needed", 12, "months", src="an",
   excerpt="Decide ≥ 12 months before the capacity is needed (nine-month equipment lead time).", locator="Analysis slide 13")
dp("w_buf", "10", "Weeks until buffer stock can supply housings", 0, "weeks", src="an",
   locator="Analysis slide 10 and slide 11, Layer 1 Buffer stock: time to act \"Immediate\"")

# ---- derived ---------------------------------------------------------------------------------------
def dv(id, slide, label, value, unit, derived, formula, calc, **kw):
    dp(id, slide, label, value, unit, derived=derived, formula=formula, calc=calc, **kw)

dv("buy75", "3b", "Supplier cost per good unit, delivered", 75, "$", ["gate73", "frt2"], "$73 + $2", "gate73 + frt2")
dv("lease_cpu1", "3b", "Leased cell cost per good unit, first year", 52.13, "$", ["lease49", "lease_s1"], "$49 ÷ (1 − 6%)", "lease49 / (1 - lease_s1)")
dv("lease_cpu2", "3b", "Leased cell cost per good unit, later years", 51.04, "$", ["lease49", "s_later"], "$49 ÷ (1 − 4%)", "lease49 / (1 - s_later)")
dv("own_cpu1", "3b", "Owned cell cost per good unit, first year", 50.00, "$", ["own46", "own_s1"], "$46 ÷ (1 − 8%)", "own46 / (1 - own_s1)")
dv("own_cpu2", "3b", "Owned cell cost per good unit, later years", 47.92, "$", ["own46", "s_later"], "$46 ÷ (1 − 4%)", "own46 / (1 - s_later)")
dv("own_up", "3b", "Owned cell upfront investment", 7.3, "$M", ["own_eq", "own_inst"], "$6.5M + $0.8M", "own_eq + own_inst")
dv("vol_plan", "3", "Good housings 2027–29, planning case", 300, "k", ["v27", "v28p", "v29p"], "80k + 100k + 120k", "v27 + v28p + v29p", definition="thousand good units")
dv("vol_cons", "3", "Good housings 2027–29, conservative case", 230, "k", ["v27", "v28c", "v29c"], "80k + 65k + 85k", "v27 + v28c + v29c", definition="thousand good units")
dv("vol2829p", "9", "Good housings 2028–29, planning case", 220, "k", ["v28p", "v29p"], "100k + 120k", "v28p + v29p", definition="thousand good units")
dv("vol2829c", "13", "Good housings 2028–29, conservative case", 150, "k", ["v28c", "v29c"], "65k + 85k", "v28c + v29c", definition="thousand good units")

# yearly cost of supplying good housings, $M
dv("buy27", "8", "Buy, 2027 cost", 6.00, "$M", ["v27", "buy75"], "80k × $75", "v27 * buy75 / 1000")
dv("buy28p", "A1", "Buy, 2028 cost, planning", 7.50, "$M", ["v28p", "buy75"], "100k × $75", "v28p * buy75 / 1000")
dv("buy29p", "A1", "Buy, 2029 cost, planning", 9.00, "$M", ["v29p", "buy75"], "120k × $75", "v29p * buy75 / 1000")
dv("buy28c", "A1", "Buy, 2028 cost, conservative", 4.88, "$M", ["v28c", "buy75"], "65k × $75", "v28c * buy75 / 1000")
dv("buy29c", "A1", "Buy, 2029 cost, conservative", 6.38, "$M", ["v29c", "buy75"], "85k × $75", "v29c * buy75 / 1000")
dv("l27", "A1", "Lease, 2027 cost", 5.77, "$M", ["v27", "lease_s1", "lease49", "lease_fix"], "80k ÷ (1 − 6%) × $49 + $1.6M", "v27 / (1 - lease_s1) * lease49 / 1000 + lease_fix")
dv("l28p", "A1", "Lease, 2028 cost, planning", 6.70, "$M", ["v28p", "s_later", "lease49", "lease_fix"], "100k ÷ (1 − 4%) × $49 + $1.6M", "v28p / (1 - s_later) * lease49 / 1000 + lease_fix")
dv("l29p", "A1", "Lease, 2029 cost, planning", 7.73, "$M", ["v29p", "s_later", "lease49", "lease_fix"], "120k ÷ (1 − 4%) × $49 + $1.6M", "v29p / (1 - s_later) * lease49 / 1000 + lease_fix")
dv("l28c", "A1", "Lease, 2028 cost, conservative", 4.92, "$M", ["v28c", "s_later", "lease49", "lease_fix"], "65k ÷ (1 − 4%) × $49 + $1.6M", "v28c / (1 - s_later) * lease49 / 1000 + lease_fix")
dv("l29c", "A1", "Lease, 2029 cost, conservative", 5.94, "$M", ["v29c", "s_later", "lease49", "lease_fix"], "85k ÷ (1 − 4%) × $49 + $1.6M", "v29c / (1 - s_later) * lease49 / 1000 + lease_fix")
dv("o27", "A1", "Own, 2027 cost", 4.75, "$M", ["v27", "own_s1", "own46", "own_fix"], "80k ÷ (1 − 8%) × $46 + $0.75M", "v27 / (1 - own_s1) * own46 / 1000 + own_fix")
dv("o28p", "A1", "Own, 2028 cost, planning", 5.54, "$M", ["v28p", "s_later", "own46", "own_fix"], "100k ÷ (1 − 4%) × $46 + $0.75M", "v28p / (1 - s_later) * own46 / 1000 + own_fix")
dv("o29p", "A1", "Own, 2029 cost, planning", 6.50, "$M", ["v29p", "s_later", "own46", "own_fix"], "120k ÷ (1 − 4%) × $46 + $0.75M", "v29p / (1 - s_later) * own46 / 1000 + own_fix")
dv("o28c", "A1", "Own, 2028 cost, conservative", 3.86, "$M", ["v28c", "s_later", "own46", "own_fix"], "65k ÷ (1 − 4%) × $46 + $0.75M", "v28c / (1 - s_later) * own46 / 1000 + own_fix")
dv("o29c", "A1", "Own, 2029 cost, conservative", 4.82, "$M", ["v29c", "s_later", "own46", "own_fix"], "85k ÷ (1 − 4%) × $46 + $0.75M", "v29c / (1 - s_later) * own46 / 1000 + own_fix")

dv("buy_tot_p", "8", "Buy, total cost 2027–29, planning", 22.50, "$M", ["buy27", "buy28p", "buy29p"], "6.00 + 7.50 + 9.00", "buy27 + buy28p + buy29p")
dv("buy_tot_c", "8", "Buy, total cost 2027–29, conservative", 17.25, "$M", ["buy27", "buy28c", "buy29c"], "6.00 + 4.88 + 6.38", "buy27 + buy28c + buy29c")
dv("l_tot_p", "8", "Lease, total cost 2027–29 incl. upfront, planning", 22.20, "$M", ["l27", "l28p", "l29p", "lease_up"], "5.77 + 6.70 + 7.73 + 2.00", "l27 + l28p + l29p + lease_up")
dv("l_tot_c", "8", "Lease, total cost 2027–29 incl. upfront, conservative", 18.63, "$M", ["l27", "l28c", "l29c", "lease_up"], "5.77 + 4.92 + 5.94 + 2.00", "l27 + l28c + l29c + lease_up")
dv("o_tot_p", "8", "Own, total cost 2027–29 incl. upfront, planning", 24.09, "$M", ["o27", "o28p", "o29p", "own_up"], "4.75 + 5.54 + 6.50 + 7.30", "o27 + o28p + o29p + own_up")
dv("o_tot_c", "8", "Own, total cost 2027–29 incl. upfront, conservative", 20.74, "$M", ["o27", "o28c", "o29c", "own_up"], "4.75 + 3.86 + 4.82 + 7.30", "o27 + o28c + o29c + own_up")
dv("on_tot_p", "8", "Own net of $2.1M resale, total 2027–29, planning", 21.99, "$M", ["o_tot_p", "resale"], "24.09 − 2.1", "o_tot_p - resale")
dv("on_tot_c", "8", "Own net of $2.1M resale, total 2027–29, conservative", 18.64, "$M", ["o_tot_c", "resale"], "20.74 − 2.1", "o_tot_c - resale")
dv("own_up_net", "A1", "Owned cell upfront net of resale", 5.2, "$M", ["own_up", "resale"], "$7.3M − $2.1M", "own_up - resale")
dv("l_d_p", "8", "Lease cost compared with buying, 2027–29, planning", -0.30, "$M", ["l_tot_p", "buy_tot_p"], "22.20 − 22.50", "l_tot_p - buy_tot_p")
dv("l_d_c", "8", "Lease cost compared with buying, 2027–29, conservative", 1.38, "$M", ["l_tot_c", "buy_tot_c"], "18.63 − 17.25", "l_tot_c - buy_tot_c")
dv("o_d_p", "8", "Own cost compared with buying, 2027–29, planning", 1.59, "$M", ["o_tot_p", "buy_tot_p"], "24.09 − 22.50", "o_tot_p - buy_tot_p")
dv("o_d_c", "8", "Own cost compared with buying, 2027–29, conservative", 3.49, "$M", ["o_tot_c", "buy_tot_c"], "20.74 − 17.25", "o_tot_c - buy_tot_c")
dv("on_d_p", "A1", "Own net of resale compared with buying, planning", -0.51, "$M", ["on_tot_p", "buy_tot_p"], "21.99 − 22.50", "on_tot_p - buy_tot_p")
dv("on_d_c", "A1", "Own net of resale compared with buying, conservative", 1.39, "$M", ["on_tot_c", "buy_tot_c"], "18.64 − 17.25", "on_tot_c - buy_tot_c")
dv("l_share", "8", "Lease saving as a share of the cost of buying, planning", 0.01, "%", ["l_d_p", "buy_tot_p"], "0.30 ÷ 22.50", "(0 - l_d_p) / buy_tot_p")
dv("l_pu_p", "8", "Lease, average cost per good housing 2027–29, planning", 74.00, "$", ["l_tot_p", "vol_plan"], "$22.20M ÷ 300k", "l_tot_p / vol_plan * 1000")
dv("l_pu_c", "8", "Lease, average cost per good housing 2027–29, conservative", 80.98, "$", ["l_tot_c", "vol_cons"], "$18.63M ÷ 230k", "l_tot_c / vol_cons * 1000")
dv("o_pu_p", "8", "Own, average cost per good housing 2027–29, planning", 80.31, "$", ["o_tot_p", "vol_plan"], "$24.09M ÷ 300k", "o_tot_p / vol_plan * 1000")
dv("o_pu_c", "8", "Own, average cost per good housing 2027–29, conservative", 90.16, "$", ["o_tot_c", "vol_cons"], "$20.74M ÷ 230k", "o_tot_c / vol_cons * 1000")
dv("on_pu_p", "8", "Own net of resale, average cost per good housing, planning", 73.31, "$", ["on_tot_p", "vol_plan"], "$21.99M ÷ 300k", "on_tot_p / vol_plan * 1000")
dv("on_pu_c", "8", "Own net of resale, average cost per good housing, conservative", 81.03, "$", ["on_tot_c", "vol_cons"], "$18.64M ÷ 230k", "on_tot_c / vol_cons * 1000")
dv("own_sav_ops", "6", "Owned cell cumulative operating saving against buying, 2027–29, planning", 5.71, "$M", ["buy_tot_p", "o27", "o28p", "o29p"], "22.50 − (4.75 + 5.54 + 6.50)", "buy_tot_p - o27 - o28p - o29p")
dv("lfix_be", "8", "Annual volume at which the lease's unit margin covers its fixed cost", 66.8, "k", ["lease_fix", "buy75", "lease_cpu2"], "$1.6M ÷ ($75 − $51.04)", "lease_fix / (buy75 - lease_cpu2) * 1000", definition="thousand good units a year")

# owned-cell saving per good housing, 2027 (slide 6 waterfall)
dv("wf_scr", "6", "Owned cell first-year scrap cost per good housing", -4.00, "$", ["own_cpu1", "own46"], "−($50.00 − $46)", "own46 - own_cpu1")
dv("wf_fix", "6", "Owned cell fixed staffing per good housing, 2027", -9.38, "$", ["own_fix", "v27"], "−$0.75M ÷ 80k", "0 - own_fix / v27 * 1000")
dv("sav27", "6", "Owned cell true saving per good housing against buying, 2027", 15.63, "$", ["cfo27", "frt2", "wf_scr", "wf_fix"], "$27 + $2 − $4.00 − $9.38", "cfo27 + frt2 + wf_scr + wf_fix")
dv("ann_cfo", "6", "Annual saving implied by the CFO slide at 100k units", 2.7, "$M", ["cfo27", "v28p"], "$27 × 100k", "cfo27 * v28p / 1000")
dv("pb_cfo", "6", "Payback on the CFO slide's basis", 2.7, "years", ["own_up", "cfo27", "v28p"], "$7.3M ÷ ($27 × 100k)", "own_up / (cfo27 * v28p / 1000)")
dv("sav_ss_unit", "6", "Owned cell steady-state saving per good housing before fixed cost (4% scrap)", 27.08, "$", ["buy75", "own_cpu2"], "$75 − $47.92", "buy75 - own_cpu2")
dv("fix_pu100", "6", "Owned cell fixed cost per housing at 100k units", 7.50, "$", ["own_fix", "v28p"], "$0.75M ÷ 100k", "own_fix / v28p * 1000")
dv("sav_ss_net", "6", "Owned cell steady-state net saving per housing at 100k units", 19.58, "$", ["sav_ss_unit", "fix_pu100"], "$27.08 − $7.50", "sav_ss_unit - fix_pu100")
dv("ann100", "6", "Owned cell annual net saving at 100k units", 1.96, "$M", ["sav_ss_net", "v28p"], "$19.58 × 100k", "sav_ss_net * v28p / 1000")
dv("pb100", "6", "Owned cell payback at 100k units, corrected", 3.7, "years", ["own_up", "ann100", "cfo27", "frt2"], "$7.3M ÷ $1.96M", "own_up / ann100")
dv("ann65", "6", "Owned cell annual net saving at 65k units (conservative 2028)", 1.01, "$M", ["sav_ss_unit", "v28c", "own_fix"], "$27.08 × 65k − $0.75M", "sav_ss_unit * v28c / 1000 - own_fix")
dv("pb65", "6", "Owned cell payback at 65k units, corrected", 7.2, "years", ["own_up", "ann65", "cfo27", "frt2"], "$7.3M ÷ $1.01M", "own_up / ann65")
dv("own_pb_vol", "5", "2028–29 volume the owned cell needs to pay back by 2029 without resale", 279, "k",
   ["own_up", "buy27", "o27", "own_fix", "sav_ss_unit"], "($7.3M − ($6.00M − $4.75M) + 2 × $0.75M) ÷ $27.08", "(own_up - (buy27 - o27) + 2 * own_fix) / sav_ss_unit * 1000", definition="thousand good units")
dv("own_cap2", "5", "Owned cell capacity over 2028–29", 240, "k", ["cap_own"], "2 × 120k", "2 * cap_own", definition="thousand accepted units")

# cash and capital (slides 7 and 12)
dv("buf_wks", "11", "Buffer stock held, weeks of supply", 6, "weeks", ["notice_emg"], "sized to the emergency supplier's six-week notice", "notice_emg")
dv("wk_units", "11", "Housings shipped per week in 2027", 1600, "units", ["v27", "wks50"], "80k ÷ 50 weeks", "v27 / wks50 * 1000")
dv("buf_units", "11", "Buffer stock, housings", 9600, "units", ["wk_units", "buf_wks"], "6 weeks × 1,600", "wk_units * buf_wks")
dv("buf", "7", "Buffer stock working capital", 0.72, "$M", ["buf_units", "buy75"], "9,600 × $75", "buf_units * buy75 / 1000000")
dv("cash_buy", "7", "Year-end 2027 cash, buy and de-risk", 8.23, "$M", ["cash0", "tool025", "buf"], "$9.2M − $0.25M − $0.72M", "cash0 - tool025 - buf")
dv("cash_lease", "7", "Year-end 2027 cash, lease cell", 7.43, "$M", ["cash0", "lease_up", "l27", "buy27"], "$9.2M − ($2.0M + $5.77M − $6.00M)", "cash0 - (lease_up + l27 - buy27)")
dv("cash_own", "7", "Year-end 2027 cash, owned cell", 3.15, "$M", ["cash0", "own_up", "o27", "buy27"], "$9.2M − ($7.3M + $4.75M − $6.00M)", "cash0 - (own_up + o27 - buy27)")
dv("cash_own_pay", "7", "Cash immediately after paying the $7.3M owned-cell investment", 1.9, "$M", ["cash0", "own_up"], "$9.2M − $7.3M", "cash0 - own_up")
dv("cap_share", "12", "Share of the $5.0M 2027 capital limit used by the recommendation", 0.05, "%", ["tool025", "caplim"], "$0.25M ÷ $5.0M", "tool025 / caplim")
dv("head_buy", "12", "Headroom above the $4.0M cash floor, recommendation", 4.23, "$M", ["cash_buy", "floor"], "$8.23M − $4.0M", "cash_buy - floor")
dv("lease_trig_cash", "12", "Lease upfront if triggered", -2.00, "$M", ["lease_up"], "−$2.0M", "0 - lease_up")
dv("cash_trig", "12", "Year-end 2027 cash if the lease is triggered", 6.23, "$M", ["cash_buy", "lease_up"], "$8.23M − $2.0M", "cash_buy - lease_up")
dv("head_trig", "12", "Headroom above the $4.0M cash floor if the lease is triggered", 2.23, "$M", ["cash_trig", "floor"], "$6.23M − $4.0M", "cash_trig - floor")
dv("tool_neg", "12", "Alternate-shop tooling (cash outflow)", -0.25, "$M", ["tool025"], "−$0.25M", "0 - tool025")
dv("buf_neg", "12", "Buffer stock (cash outflow)", -0.72, "$M", ["buf"], "−$0.72M", "0 - buf")
dv("d_per1", "12", "Extra 2027–29 cost of buying for every $1 added to the 2028–29 supplier price", 0.22, "$M", ["vol2829p"], "220k × $1", "vol2829p / 1000")

# lease sensitivity (slide 9)
dv("lsav27", "9", "Lease saving against buying in 2027, full year", 0.23, "$M", ["buy27", "l27"], "$6.00M − $5.77M", "buy27 - l27")
dv("lsav_base", "9", "Lease saving against buying 2027–29, planning base case", 0.30, "$M", ["l_d_p"], "−(22.20 − 22.50)", "0 - l_d_p")
dv("sens_p5", "9", "Lease saving if the supplier's 2028–29 price is $5 higher", 1.40, "$M", ["lsav_base", "vol2829p"], "$0.30M + 220k × $5", "lsav_base + vol2829p * 5 / 1000")
dv("l27_7pr", "9", "2027 supply cost if the lease runs 7 months, fixed cost pro-rated", 5.87, "$M", ["v27", "lease_s1", "lease49", "lease_fix", "buy75"],
   "7/12 × 80k ÷ (1 − 6%) × $49 + 7/12 × $1.6M + 5/12 × 80k × $75", "v27 * 7 / 12 / (1 - lease_s1) * lease49 / 1000 + lease_fix * 7 / 12 + v27 * 5 / 12 * buy75 / 1000")
dv("l27_7fy", "9", "2027 supply cost if the lease runs 7 months, full-year fixed cost", 6.53, "$M", ["v27", "lease_s1", "lease49", "lease_fix", "buy75"],
   "7/12 × 80k ÷ (1 − 6%) × $49 + $1.6M + 5/12 × 80k × $75", "v27 * 7 / 12 / (1 - lease_s1) * lease49 / 1000 + lease_fix + v27 * 5 / 12 * buy75 / 1000")
dv("sens_7pr", "9", "Lease saving if it runs 7 months of 2027, fixed cost pro-rated", 0.21, "$M", ["lsav_base", "lsav27", "buy27", "l27_7pr"], "0.30 − 0.23 + (6.00 − 5.87)", "lsav_base - lsav27 + buy27 - l27_7pr")
dv("sens_s6", "9", "Lease saving if later-year scrap is 6% instead of 4%", 0.06, "$M", ["lsav_base", "vol2829p", "lease_s1", "s_later", "lease49"],
   "0.30 − 220k × $49 × (1 ÷ 0.94 − 1 ÷ 0.96)", "lsav_base - (vol2829p / (1 - lease_s1) - vol2829p / (1 - s_later)) * lease49 / 1000")
dv("be_vol", "9", "2028–29 volume at which the lease breaks even against buying", 207.4, "k", ["lease_up", "lease_fix", "lsav27", "buy75", "lease_cpu2"],
   "($2.0M + 2 × $1.6M − $0.23M) ÷ ($75 − $51.04)", "(lease_up + 2 * lease_fix - lsav27) / (buy75 - lease_cpu2) * 1000", definition="thousand good units")
dv("sens_vol", "9", "Lease saving if 2028–29 volume is 6% below plan (207k)", 0.0, "$M", ["lsav_base", "vol2829p", "be_vol", "buy75", "lease_cpu2"],
   "$0.30M − (220k − 207k) × ($75 − $51.04) ≈ 0", "lsav_base - (vol2829p - be_vol) * (buy75 - lease_cpu2) / 1000")
dv("sens_m2", "9", "Lease saving if the supplier's 2028–29 price is $2 lower", -0.14, "$M", ["lsav_base", "vol2829p"], "$0.30M − 220k × $2", "lsav_base - vol2829p * 2 / 1000")
dv("sens_7fy", "9", "Lease saving if it runs 7 months of 2027 but pays full-year fixed cost", -0.46, "$M", ["lsav_base", "lsav27", "buy27", "l27_7fy"], "0.30 − 0.23 + (6.00 − 6.53)", "lsav_base - lsav27 + buy27 - l27_7fy")
dv("sens_cons", "9", "Lease saving with conservative demand", -1.38, "$M", ["l_d_c"], "−(18.63 − 17.25)", "0 - l_d_c")
dv("be_p", "9", "2028–29 supplier price above which the lease wins, planning", 73.6, "$", ["l_tot_p", "buy27", "vol2829p"], "($22.20M − $6.00M) ÷ 220k", "(l_tot_p - buy27) / vol2829p * 1000")
dv("be_c", "9", "2028–29 supplier price above which the lease wins, conservative", 84.2, "$", ["l_tot_c", "buy27", "vol2829c"], "($18.63M − $6.00M) ÷ 150k", "(l_tot_c - buy27) / vol2829c * 1000")
dv("price_gap", "9", "Supplier price cut that erases the lease's edge", 1.4, "$", ["buy75", "be_p"], "$75 − $73.6", "buy75 - be_p")

# gates (slide 13)
dv("t1", "13", "Gate T1: committed 2028–29 volume that triggers the lease", 208, "k", ["be_vol"], "207.4k break-even, rounded up to the next thousand", "be_vol", definition="thousand good units")
dv("t2a", "13", "Gate T2: supplier 2028–29 delivered price that triggers the lease on any volume", 84, "$", ["be_c"], "$84.2 break-even, rounded", "be_c")
dv("t2b", "13", "Gate T2: supplier price that triggers the lease together with T1", 74, "$", ["be_p"], "$73.6 break-even, rounded", "be_p")
dv("p3", "13", "Gate P3: first-year yield on accepted units the lease must prove", 0.94, "%", ["lease_s1"], "1 − 6% scrap", "1 - lease_s1")

# reliability (slides 10 and 11)
dv("otd_gap", "10", "On-time delivery gap to the 97% requirement", -0.2, "pp", ["otd", "otd_req"], "96.8% − 97.0%", "(otd - otd_req) * 100")
dv("late_units", "10", "Housings a year the gap represents at 80k units", 160, "units", ["otd_req", "otd", "v27"], "0.2% × 80,000", "(otd_req - otd) * v27 * 1000")
dv("w_emg", "10", "Weeks until the emergency supplier can deliver", 6, "weeks", ["notice_emg"], "six-week notice", "notice_emg")
dv("w_res", "10", "Weeks until the supplier's reserved units can deliver", 12.9, "weeks", ["notice_res"], "90 days ÷ 7", "notice_res / 7")
dv("w_lease", "10", "Weeks until a leased cell can supply (survey passes, before ramp-up)", 21.7, "weeks", ["lt_lease"], "5 months × 52 ÷ 12", "lt_lease * 52 / 12")
dv("w_own", "10", "Weeks until an owned cell can supply (equipment lead time, before install)", 39, "weeks", ["lt_own"], "9 months × 52 ÷ 12", "lt_own * 52 / 12")
dv("emg_prem", "11", "Emergency supply premium per housing over buying", 15, "$", ["emg88", "emg_frt", "buy75"], "$88 + $2 − $75", "emg88 + emg_frt - buy75")
dv("mon_units", "11", "Housings in one month at 2027 volume", 6700, "units", ["v27"], "80,000 ÷ 12", "v27 / 12 * 1000")
dv("emg_month", "11", "Extra cost of one fully emergency-sourced month", 0.1, "$M", ["mon_units", "emg_prem"], "6,700 × $15", "mon_units * emg_prem / 1000000")
dv("emg_months", "11", "Months of emergency supply equal in cost to the lease's conservative-case downside", 13.8, "months", ["l_d_c", "emg_month"], "$1.38M ÷ $0.1M", "l_d_c / emg_month")
dp("carry", "15", "Buffer carrying cost over 2027–29 at an assumed 25% a year", 0.54, "$M", derived=["buf", "carry_rate"], formula="$0.72M × 25% × 3 years",
   calc="buf * carry_rate * 3", estimate=True, assumptions=["Carrying cost of 25% of inventory value a year (the analysis's assumption; the pack says it is not yet modelled)",
                                                           "Buffer held at $0.72M for all three years"])
