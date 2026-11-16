import sys, os
from components import *

OUT = sys.argv[1]
PREV = sys.argv[2]
SRC = "Source: Dispatch Copilot briefing pack (fictional data prepared for this exercise)"

D = Deck()
B = lambda t: (t, {"bold": True})
C = lambda t, c: (t, {"color": c})
BC = lambda t, c: (t, {"bold": True, "color": c})

# ------------------------------------------------------------------ 1. Title
s = D.new()
s.rect(0, 0, W, H, fill="#0f2a4a")
s.rect(0.8, 2.05, 0.08, 2.6, fill=BLUE)
s.text(1.15, 1.2, 10, 0.4, "BRIGHTWORK · EXECUTIVE TEAM · JANUARY 2027 PLANNING", size=12, bold=True, color="#9ec5f4")
s.text(1.15, 2.0, 11, 1.4, "Dispatch Copilot: launch it in Q2 2027 inside a new Pro tier, not as a $149 add-on",
       size=34, bold=True, color="#ffffff", ls=1.12)
s.text(1.15, 3.65, 10.5, 1.0, "Our decision question: should we launch Dispatch Copilot in Q2 2027, and if so, how "
       "should we package and price it?", size=16, color="#cde2fb")
s.text(1.15, 6.3, 11, 0.6, ["Prepared for CEO Maya Okafor and the executive team",
                            "Based only on the internal briefing pack. All figures in the pack are fictional."],
       size=11, color="#b7d3f6", space_after=2)
s.notes("Purpose: get a decision on launch timing, packaging and price at January 2027 planning. "
        "Every number in this deck comes from, or is calculated from, the briefing pack. Calculations are in Appendix A.")

# ------------------------------------------------------------------ 2. Executive summary
s = D.new()
s.header("Executive summary", "Launch Copilot in Q2 2027 as part of a new Pro tier at +$12 per seat. A $149 add-on "
         "would earn less, and Copilot free in Core would breach the margin floor")
lx, lw = 0.6, 7.75
y = 1.85
blocks = [
    ("Launch. The competitive threat is real, though smaller than claimed",
     ["Routewise put AI scheduling in its Pro plan, and since then our win rate in deals against them has fallen from 44% to 37%. "
      "At most that is ~110 deals, or $0.6M of new ARR a year, not the $1.9M the Sales memo implies.",
      "In the beta, jobs per dispatcher-hour rose 11%, against 2% for matched accounts. The beta accounts volunteered, "
      "so this is an upper bound."]),
    ("Package it as a Pro tier. The $8M add-on case rests on the survey",
     ["When beta users actually hit a $149 paywall, 14% bought, against 46% in the survey. That means at most $2.5M of add-on ARR.",
      "A flat $149 attracts heavy users: their inference costs eat 41% of the price, and 88% for the top accounts. A per-seat Pro tier "
      "grows with account size and matches Routewise. Base case: ~$2.2M ARR, +3.8 NRR points and a 76.6% company gross margin.",
      "Including Copilot free in Core would take gross margin to 72–74%, below the 75% floor."]),
    ("Guardrails. Protect mobile and test before we scale",
     ["Launching first delays the mobile rewrite by two quarters, which costs ~$0.5M of churn we could have avoided. "
      "Holding Copilot back until mobile ships would forgo ~$1.1M or more of Copilot ARR.",
      "Go or no-go in March: if a random-sample Pro offer points to adoption below 15%, the 14 engineers go back to mobile."]),
]
for head, bullets in blocks:
    hgt = s.text(lx, y, lw, 0.3, head, size=13.5, bold=True, color=BLUE_D)
    y += hgt + 0.07
    hgt = s.text(lx, y, lw, 2.0, bullets, size=11.5, bullet=True, space_after=3, check=False)
    y += hgt + 0.2
if y > 6.95:
    WARN.append(f"[2] exec summary too tall: {y:.2f}")
# decisions box
bx, bw = 8.75, 3.98
s.rect(bx, 1.85, bw, 4.95, fill=PANEL)
s.rect(bx, 1.85, bw, 0.06, fill=BLUE)
s.text(bx + 0.25, 2.05, bw - 0.5, 0.3, "Decisions requested today", size=14, bold=True)
decs = [
    [B("1. Approve a Q2 2027 launch of Pro: "), "$91 per seat ($79 Core + $12), including Copilot with 600 AI requests per seat per month, pooled per account."],
    [B("2. Reject "), "the $149 add-on and the free-in-Core option."],
    [B("3. Assign 14 engineers "), "to Copilot for Q1–Q2, and re-baseline the mobile rewrite two quarters later with a fixed date."],
    [B("4. Approve the Q1 price test "), "and the March go/no-go checkpoint."],
]
s.text(bx + 0.25, 2.5, bw - 0.5, 4.2, decs, size=12, space_after=10)
s.footer(SRC + ". Ranges and assumptions: slides 10, 14 and 15.")

# ------------------------------------------------------------------ 3. Three tests
s = D.new()
s.header("What the decision must achieve", "Any option has to pass three tests: lift NRR toward 105%, hold gross margin "
         "at 75% or more, and justify a two-quarter delay to mobile")
cw, gap = 3.9, 0.215
cards = [
    ("1 · Net revenue retention", "101% → 105%",
     [[B("Gap: 4 points"), ", or ~$2.3M of net expansion on $57.6M ARR, by 2028."],
      "Only paid upgrades by existing accounts, or less churn, move NRR. New-customer wins do not.",
      ]),
    ("2 · Company gross margin", "78% → ≥75%",
     [[B("Headroom: 3 points"), ", or ~$1.7M of extra cost at today’s revenue."],
      "Copilot adds $0.009 per AI request (price fixed until December 2027) plus ~$0.6M a year of platform, evaluation and support cost. "
      "The price has to cover both."]),
    ("3 · Engineering trade-off", "14 of 60",
     [[B("Engineers for two quarters"), ", or $1.47M fully loaded. The mobile app rewrite slips by two quarters."],
      "Mobile reliability is the top churn reason (27%) and the top feature request (38% rank it first, against 19% for AI scheduling)."]),
]
for i, (k, hero, body) in enumerate(cards):
    card(s, 0.6 + i * (cw + gap), 1.9, cw, 3.1, k, hero, body, hero_size=28)
s.rect(0.6, 5.3, 12.13, 1.05, fill="#ffffff", line=GRID)
s.text(0.85, 5.38, 11.7, 0.9,
       [[B("Baseline today:  "), "9,800 accounts · 6.2 office seats each · Core at $79/seat/month · $57.6M ARR · "
         "78% gross margin · 14% logo churn · 101% NRR"],
        [B("Average account:  "), "$5,878 ARR (6.2 seats × $79 × 12). We use this to turn deal and churn counts into ARR."]],
       size=11.5, valign="m", space_after=4)
s.footer(SRC)

# ------------------------------------------------------------------ 4. Demand
s = D.new()
s.header("Demand", "When customers faced a real paywall they bought at a third of the survey rate. "
         "The add-on is worth $2.5M of ARR at most, not $8M")
s.text(0.6, 1.85, 6.3, 0.3, "Share of accounts buying Copilot at $149 per account per month", size=12, bold=True)
s.text(0.6, 2.12, 6.3, 0.3, "First-year ARR if the rate held across all 9,800 accounts is shown in brackets", size=10.5, color=INK2)
yb = hbars(s, 0.6, 2.75, 6.4, 2.35,
           [("Survey: said likely to buy", 46), ("Paywall test: bought", 14),
            ("Planning range, all accounts", 14)],
           vmax=50, bar_h=0.5, gap=0.45, size=11, value_w=1.4,
           colors=[GRAYBAR, BLUE, BLUE_L],
           sublabels=["46%  ($8.1M)", "14%  ($2.5M)", "7–14%  ($1.2–2.5M)"])
# range overlay for 7-14: draw darker segment 0-7 lighter? show range as band from 7 to 14
plot_x = 0.6 + 2.35; plot_w = 6.4 - 2.35 - 1.4
ry = 2.75 + 2 * (0.5 + 0.45)
s.rect(plot_x, ry, plot_w * 7 / 50, 0.5, fill="#ffffff")
s.rect(plot_x + plot_w * 7 / 50, ry, plot_w * 7 / 50, 0.5, fill=BLUE_L, line=BLUE, lw=1)
s.line(plot_x, 2.65, plot_x, ry + 0.6, color=AXIS, lw=1)
s.text(0.6, 5.55, 6.4, 0.75, "The CPO’s $8M figure is 46% × 9,800 accounts × $149 × 12. Our planning range halves the paywall "
       "rate at the low end, because the test accounts were volunteers.", size=10.5, color=INK2)
rx = 7.5; rw = 5.23
s.rect(rx, 1.85, rw, 4.85, fill=PANEL)
s.text(rx + 0.25, 2.0, rw - 0.5, 0.3, "Why the survey overstates demand", size=13, bold=True, color=BLUE_D)
s.text(rx + 0.25, 2.38, rw - 0.5, 1.5,
       [[B("Self-selected: "), "only 610 of 9,800 admins replied (6%)."],
        [B("Skewed to big accounts: "), "respondents average 9.4 seats, against 6.2 across the base."],
        [B("Stated intent: "), "saying “likely” is not the same as paying."]], size=11.5, bullet=True, space_after=4)
s.text(rx + 0.25, 3.6, rw - 0.5, 0.3, "Why even 14% is a ceiling for the base", size=13, bold=True, color=BLUE_D)
s.text(rx + 0.25, 3.98, rw - 0.5, 1.3,
       [[B("Volunteers: "), "beta accounts are larger (8.1 seats) and more active than average."],
        [B("Heavy users bought: "), "buyers averaged 6,800 requests a month, against a beta mean of 3,600."]],
       size=11.5, bullet=True, space_after=4)
s.rect(rx + 0.25, 5.3, rw - 0.5, 1.15, fill="#ffffff")
s.text(rx + 0.4, 5.38, rw - 0.8, 0.95, [[B("So what: "), "a $149 add-on would add about 2–4 NRR points at best, "
       "and its buyers would be the most expensive accounts to serve (slide 7)."]], size=11.5, valign="m")
s.footer(SRC + ". Survey October 2026; paywall test in the last four weeks of the 12-week beta.")

# ------------------------------------------------------------------ 5. Competition
s = D.new()
s.header("Competition", "Routewise’s AI is costing us at most ~110 deals ($0.6M of new ARR) a year, "
         "a third of what the Sales memo implies")
s.text(0.6, 1.85, 4.6, 0.3, "Brightwork win rate in deals Routewise contests", size=12, bold=True)
vbars(s, 0.8, 2.25, 4.0, 3.6, [("Q1–Q2 2026", 44), ("Q3 2026", 37)], vmax=50, bar_w=1.1,
      value_fmt=lambda v: f"{v}%", colors=[GRAYBAR, BLUE])
s.text(0.6, 6.0, 4.6, 0.8, "In September 2026 Routewise launched AI scheduling in its Pro plan. In Q3 it also offered 20% off the "
       "first year, so the drop has two possible causes.", size=10.5, color=INK2)
# sizing table
tx = 5.6
s.text(tx, 1.85, 7.1, 0.3, "Sizing the threat: the most we could recover", size=12, bold=True)
end, rows_, cx = table(s, tx, 2.2, [4.7, 2.43], ["Step", "Value"],
      [["Qualified new-customer opportunities a year", "2,600"],
       ["× share where Routewise competes (60%)", "1,560 deals"],
       ["× drop in win rate (44% → 37%, 7 points)", "~109 deals"],
       [[B("× $5,878 ARR per new account (6.2 seats on Core)")], {"paras": [B("≤ $0.64M new ARR a year")], "color": BLUE_D}]],
      size=11.5, bold_first_col=False)
s.rect(tx, end + 0.25, 7.13, 2.15, fill=PANEL)
s.text(tx + 0.2, end + 0.35, 6.75, 0.3, "Why the memo’s “recover a third of losses” (~328 deals, $1.9M) is too high",
       size=12, bold=True, color=BLUE_D)
s.text(tx + 0.2, end + 0.7, 6.75, 2.0,
       ["When 31% of loss notes mention AI, that does not mean AI caused those losses. The 31% also covers all Q3 losses, not just Routewise deals.",
        "We were already losing 56% of these deals before Routewise had AI. Parity can only win back the 7-point drop.",
        "Some of the drop is probably Routewise’s 20% promotion, so $0.64M is a ceiling."],
       size=11, bullet=True, space_after=3)
s.footer(SRC + ". The win-back shows up in new ARR, not in NRR.")

# ------------------------------------------------------------------ 6. Beta
s = D.new()
s.header("Beta evidence", "The beta shows real productivity value, but because the accounts volunteered, every figure is an upper bound")
tiles = [("Jobs scheduled per dispatcher-hour", "+11%", "vs +2% for matched non-beta accounts (9 points net), against the prior 12 weeks"),
         ("90-day renewal rate", "97%", "vs 93% for matched accounts. Probably selection: active volunteers renew more anyway"),
         ("Dispatcher hours saved per week", "4.1 h", "Self-reported, with no comparison group")]
for i, (k, v, sub) in enumerate(tiles):
    yy = 1.9 + i * 1.6
    s.rect(0.6, yy, 5.3, 1.45, fill=PANEL)
    s.text(0.85, yy + 0.15, 4.9, 0.3, k, size=11, bold=True, color=INK2)
    s.text(0.85, yy + 0.45, 1.6, 0.7, v, size=30, bold=True, color=BLUE_D if i == 0 else INK)
    s.text(2.5, yy + 0.47, 3.25, 0.9, sub, size=10.5, color=INK2, valign="m")
rx = 6.3; rw = 6.43
s.text(rx, 1.9, rw, 0.3, "What 240 volunteer accounts over 12 weeks can and cannot tell us", size=12.5, bold=True)
end, _, _ = table(s, rx, 2.3, [1.0, 5.43], ["", "Finding"],
      [[{"paras": [BC("✓ Can", GOOD_T)]}, "Engaged dispatchers who opt in use Copilot heavily and schedule more jobs per hour."],
       [{"paras": [BC("✗ Cannot", CRIT)]}, "Assume the base will gain 9 points. Volunteers are larger (8.1 seats against 6.2) and more active."],
       [{"paras": [BC("✗ Cannot", CRIT)]}, "Credit Copilot with the 4-point renewal gap. We leave any retention gain out of the base case."],
       [{"paras": [BC("! Note", "#9a6a00")]}, "Usage is concentrated: the top 10% of accounts make 58% of requests. "
        "The median account makes 1,900 requests a month and the mean 3,600, so pricing has to handle heavy users (slide 7)."],
       [{"paras": [BC("! Data", "#9a6a00")]}, "A top-10% mean of 14,500 requests implies a 40% share, not 58%. We cost on the higher "
        "mean (3,600). Product should reconcile the two figures before launch."]],
      size=11, bold_first_col=False)
s.footer(SRC + ". Tables 1–2.")

# ------------------------------------------------------------------ 7. Unit economics
s = D.new()
s.header("Unit economics", "A flat $149 add-on draws in the heaviest users. Per-seat pricing with an allowance keeps "
         "inference cost in line with revenue")
s.text(0.6, 1.85, 6.4, 0.3, "Monthly inference cost per account at $0.009 per request", size=12, bold=True)
s.text(0.6, 2.12, 6.4, 0.3, "Requests per month in brackets. Dashed line: the $149 add-on price", size=10.5, color=INK2)
hbars(s, 0.6, 2.95, 6.5, 2.45,
      [("Median beta account (1,900)", 17.1), ("Mean beta account (3,600)", 32.4),
       ("Paywall buyers (6,800)", 61.2), ("Top 10% of accounts (14,500)", 130.5)],
      vmax=160, bar_h=0.42, gap=0.38, size=11, value_w=1.15,
      colors=[GRAYBAR, GRAYBAR, BLUE, BLUE],
      sublabels=["$17", "$32", "$61 (41%)", "$131 (88%)"], ref_lines=[(149, "$149 price")], inside=True)
s.text(0.6, 6.1, 6.4, 0.6, "Percentages show inference cost as a share of the $149 price. The ~$0.6M a year of fixed platform "
       "cost comes on top.", size=10.5, color=INK2)
rx = 7.45
s.text(rx, 1.85, 5.28, 0.3, "Per-account economics, typical case", size=12, bold=True)
end, _, _ = table(s, rx, 2.2, [1.7, 1.75, 1.83], ["", "$149 add-on (typical buyer)", "Pro +$12/seat (6.2-seat account)"],
      [["Revenue a month", "$149", {"paras": [B("$74")]}],
       ["Inference at expected use", "$61 (6,800 requests)", "$25 (444 per seat, the beta mean)"],
       ["Inference share of revenue", "41%", {"paras": [B("33%")]}],
       ["Worst case", "Top-10% account: $131, or 88% of price", "Capped at 600 per seat: $33 (45%). Overage billed above that"],
       ["Does revenue grow with usage?", "No. The price is flat per account", {"paras": [B("Yes. Revenue rises with seats and overage")]}]],
      size=10.5, hsize=10.5, col_fills=[None, None, "#eef4fc"])
s.rect(rx, end + 0.2, 5.28, 6.75 - end - 0.2, fill=PANEL)
s.text(rx + 0.2, end + 0.28, 4.9, 6.75 - end - 0.36,
       [[B("Upside we don’t price in: "), "inference list prices fell 35% in the last 12 months. Our $0.009 rate is fixed until "
         "December 2027, so we should renegotiate in H2 2027 and keep the savings as margin."]], size=10.5, valign="m")
s.footer(SRC + ". Table 2 and paywall test. Beta per-seat usage = 3,600 requests ÷ 8.1 seats.")

# ------------------------------------------------------------------ 8. Options
s = D.new()
s.header("Options", "Of the four ways to launch, only a Pro tier passes all three tests")
hdr = ["", "A · Defer: mobile first, Copilot in Q4 2027", "B · $149 per account add-on (CPO proposal)",
       "C · Pro tier at +$12 per seat with Copilot (recommended)", "D · Copilot free in Core (Routewise-style)"]
rows = [
    ["Expansion ARR, base case", "None in H1 2027. C’s ARR arrives ~2 quarters later", "$1.75M (10% adopt; $1.2–2.5M)",
     {"paras": [B("$2.19M (25% adopt; $1.3–2.9M)")]}, "$0, because there is no price"],
    ["NRR contribution", "Deferred", "+3.0 points", {"paras": [B("+3.8 points")]}, "Indirect only, via retention"],
    ["Copilot gross profit a year", "n/a in 2027", "$0.43M", {"paras": [B("$0.86M")]}, "−$3.5M"],
    ["Company gross margin", "78.0%", "76.4%", {"paras": [B("76.6%")]}, "71.9–73.5%"],
    ["Parity with Routewise", "None until Q4 2027", "Weak: an extra fee on top of the plan", {"paras": [B("Matches “AI in Pro”")]}, "Strongest"],
    ["Mobile rewrite", "On schedule", "Two quarters late", "Two quarters late", "Two quarters late"],
]
end, rws, cx = table(s, 0.6, 1.85, [2.0, 2.53, 2.53, 2.53, 2.54], hdr, rows, size=11, hsize=11,
                     col_fills=[None, None, None, "#eef4fc", None])
# verdict row
vy = end + 0.05
s.text(0.68, vy + 0.1, 1.9, 0.3, "Verdict", size=11, bold=True)
verdicts = [("Fails on value", "bad", "Gives up ~$1.1M of Copilot ARR to save ~$0.5M of mobile churn. Routewise gets two more quarters"),
            ("Passes, but weaker", "mid", "Lower profit, draws heavy users, and the buying evidence comes from volunteers"),
            ("Passes all three", "good", "Higher expansion and profit, matches Routewise, and costs stay controlled"),
            ("Fails the margin test", "bad", "Breaches 75% if more than ~39% of accounts use it at the beta mean")]
for i, (lab, k, why) in enumerate(verdicts):
    xx = cx[i + 1] + 0.08
    if i == 2:
        s.rect(cx[i + 1], vy, 2.53, 1.2, fill="#eef4fc")
    pill(s, xx, vy + 0.08, 2.4, lab, k)
    s.text(xx, vy + 0.38, 2.37, 0.8, why, size=10, color=INK2)
s.line(0.6, vy + 1.25, 12.73, vy + 1.25, color=INK2, lw=1)
s.footer(SRC + ". Copilot gross profit = revenue − inference − $0.6M platform cost. See Appendix A.")

# ------------------------------------------------------------------ 9. Package design
s = D.new()
s.header("Recommended package", "Pro at $91 per seat (Core plus $12) includes Copilot and a pooled allowance of 600 AI requests per seat")
end, _, _ = table(s, 0.6, 1.85, [1.75, 4.75, 5.63], ["Element", "Recommendation", "Why"],
      [["Plan", "A new Pro tier: Core plus Dispatch Copilot (schedule proposals, quote drafts, call summaries). Core stays at $79.",
        "An opt-in upgrade avoids raising the Core price (price drives 22% of churn), and it mirrors Routewise’s packaging."],
       ["Price", [[B("+$12 per office seat per month"), " ($91 in total)."]],
        "Revenue grows with account size, which is what drives usage. A typical 6.2-seat account pays $74 a month, half the $149 add-on."],
       ["Allowance", [[B("600 AI requests per seat per month"), ", pooled across the account."]],
        "That is 35% above the beta mean (444 per seat), and it holds worst-case inference to $5.40 per seat, or 45% of the uplift."],
       ["Overage", [[B("$20 per extra 1,000 requests"), " (about 2.2× today’s cost)."]],
        "The heaviest accounts (the top 10% average 14,500 requests a month) pay for what they use rather than eating into margin."],
       ["New business", "Pro becomes the lead plan in every deal Routewise contests.",
        "It neutralises the “AI included” comparison, worth up to $0.64M of new ARR a year."],
       ["Inference contract", "Renegotiate in H2 2027, ahead of the December 2027 expiry.",
        "List prices fell 35% in 12 months. We keep the savings as margin and hold the price."]],
      size=11, hsize=11)
s.rect(0.6, end + 0.2, 12.13, 0.62, fill=PANEL)
s.text(0.8, end + 0.2, 11.8, 0.62, [[B("Our choice, to be validated: "), "$12 is the only per-seat price in the pack, and the 600-request allowance and "
       "$20 overage are our proposals. The Q1 test adds a $15 arm to check whether customers would pay more."]], size=11, valign="m")
s.footer(SRC + ". Allowance and overage levels are recommendations, not tested figures.")

# ------------------------------------------------------------------ 10. Financials
s = D.new()
s.header("Financial case", "Base case: Pro adds ~$2.2M of ARR and ~3.8 NRR points at a 76.6% company margin. "
         "Fixing mobile closes the rest of the gap to 105%")
s.text(0.6, 1.85, 6.2, 0.3, "NRR points each lever adds (low to high, base case marked)", size=12, bold=True)
levers = [("Pro tier (15–33% adopt)", 2.3, 3.8, 5.0, BLUE), ("$149 add-on (7–14% adopt)", 2.1, 3.0, 4.3, GRAYBAR),
          ("Mobile rewrite (halves or ends mobile churn)", 1.6, None, 3.3, GRAYBAR)]
lab_w = 2.3; px0 = 0.6 + lab_w; pw = 3.7; vmax = 6.0
yy = 2.75
for lab, lo, mid, hi, col in levers:
    s.text(0.6, yy - 0.05, lab_w - 0.12, 0.5, lab, size=10.5, align="r", valign="m")
    s.rect(px0 + pw * lo / vmax, yy + 0.08, pw * (hi - lo) / vmax, 0.26, fill=BLUE_L if col == BLUE else "#e6e5df")
    if mid:
        s.rect(px0 + pw * mid / vmax - 0.03, yy, 0.06, 0.42, fill=BLUE_D if col == BLUE else INK2)
        s.text(px0 + pw * mid / vmax - 0.75, yy - 0.3, 0.7, 0.25, f"base {mid}", size=10.5, bold=True, align="r")
    s.text(px0 + pw * lo / vmax - 0.6, yy + 0.08, 0.55, 0.26, f"{lo}", size=10, color=INK2, align="r", valign="m")
    s.text(px0 + pw * hi / vmax + 0.06, yy + 0.08, 0.6, 0.26, f"{hi}", size=10, color=INK2, valign="m")
    yy += 0.95
s.line(px0, 2.45, px0, yy - 0.4, color=AXIS, lw=1)
gx = px0 + pw * 4 / vmax
s.line(gx, 2.35, gx, yy - 0.4, color=INK2, lw=1, dash=True)
s.text(gx - 1.0, 2.1, 2.0, 0.25, "4-point gap to 105%", size=9.5, color=INK2, align="c")
for t in range(0, 7, 2):
    s.text(px0 + pw * t / vmax - 0.2, yy - 0.35, 0.4, 0.22, str(t), size=9, color=MUTED, align="c")
s.text(0.6, 5.65, 6.4, 1.1,
       ["Pro’s base case plus a rewrite that halves mobile churn gives ~5.4 points, enough to clear the gap.",
        "Upgrades lift NRR once. Holding 105% also needs lower churn, which is the case for protecting mobile."],
       size=10.5, color=INK2, bullet=True, space_after=3)
rx = 7.35
s.text(rx, 1.85, 5.38, 0.3, "Pro tier scenarios (full-year run-rate)", size=12, bold=True)
end, _, _ = table(s, rx, 2.2, [2.08, 1.1, 1.1, 1.1], ["", "Low", "Base", "High"],
      [["Accounts adopting", "15%", "25%", "33%"],
       ["Expansion ARR", "$1.31M", {"paras": [B("$2.19M")]}, "$2.89M"],
       ["NRR points", "+2.3", {"paras": [B("+3.8")]}, "+5.0"],
       ["Copilot gross profit", "$0.27M", {"paras": [B("$0.86M")]}, "$1.32M"],
       ["Company gross margin", "76.7%", {"paras": [B("76.6%")]}, "76.5%"],
       ["…if every seat uses its full allowance", "76.5%", "76.2%", "75.9%"]],
      size=11, hsize=11, col_fills=[None, None, "#eef4fc", None])
s.text(rx, end + 0.15, 5.38, 6.8 - end - 0.15,
       ["Low = the paywall rate. High = 33% of accounts moved to the 2023 higher tier within a year. Base sits between them.",
        "One-off engineering cost of $1.47M pays back in ~1.7 years on base gross profit, before any new-customer wins (≤ $0.64M ARR a year)."],
       size=10.5, color=INK2, bullet=True, space_after=3)
s.footer(SRC + ". Assumes adopters average 6.2 seats; the $0.6M platform cost is counted in cost of revenue.")

# ------------------------------------------------------------------ 11. Mobile trade-off
s = D.new()
s.header("The mobile trade-off", "Launching Copilot first costs ~$0.5M of avoidable mobile churn, while holding it back "
         "forgoes ~$1.1M or more. Launch, but fix the new mobile date")
s.text(0.6, 1.85, 5.9, 0.3, "Main reason churned accounts gave, 2026 (n = 1,190)", size=12, bold=True)
s.text(0.6, 2.12, 5.9, 0.3, "Share of churned accounts. ARR lost a year in brackets", size=10.5, color=INK2)
hbars(s, 0.6, 2.6, 6.0, 2.0,
      [("Mobile app reliability", 27), ("Price", 22), ("Other", 16), ("Missing integrations", 15),
       ("Out of business or sold", 14), ("Switched for AI features", 6)],
      vmax=32, bar_h=0.34, gap=0.21, size=11, value_w=1.35,
      colors=[BLUE, GRAYBAR, GRAYBAR, GRAYBAR, GRAYBAR, BLUE_L],
      sublabels=["27%  ($1.9M)", "22%  ($1.5M)", "16%", "15%", "14%", "6%  ($0.4M)"])
s.text(0.6, 6.0, 5.9, 0.75, "Mobile drives 4.5× as much churn as AI. Ending it would be worth ~3.3 NRR points. "
       "It is a real lever, and it is being delayed, not dropped.", size=10.5, color=INK2)
rx = 6.95
s.text(rx, 1.85, 5.78, 0.3, "Cost of each sequence (both shift the other project by two quarters)", size=12, bold=True)
end, _, _ = table(s, rx, 2.2, [1.55, 4.23], ["Sequence", "What we give up"],
      [[{"paras": [B("Copilot first"), ("  (recommended)", {"color": BLUE_D, "bold": True})]},
        [[B("~$0.5M ARR"), " of mobile churn not avoided for six months, if the rewrite halves mobile churn. "
          "$0.9M if it would end mobile churn entirely."]]],
       [{"paras": [B("Mobile first")]},
        [[B("~$1.1M ARR"), " of Pro expansion deferred (base case, or $0.65M if adoption is low), plus up to $0.3M of new ARR lost to Routewise "
          "and up to $0.2M of AI-driven churn."]]]],
      size=11, hsize=11, col_fills=[None, None])
s.rect(rx, end + 0.2, 5.78, 2.3, fill=PANEL)
s.text(rx + 0.2, end + 0.3, 5.4, 0.3, "How we protect mobile", size=12, bold=True, color=BLUE_D)
s.text(rx + 0.2, end + 0.65, 5.4, 6.7 - end - 0.7,
       ["The order flips if Pro adoption is low (~15%) and the rewrite would end most mobile churn. That is why the March checkpoint uses the price test.",
        "Re-baseline the mobile rewrite two quarters later on a fixed, published date, and return the 14 engineers to it in Q3.",
        "Ask the CTO whether the 14 can come from teams other than mobile. If they can, the delay shrinks."],
       size=10.5, bullet=True, space_after=3)
s.footer(SRC + ". ARR = accounts × $5,878. The rewrite’s effect on churn is our assumption (half or all of mobile churn).")

# ------------------------------------------------------------------ 12. Risks
s = D.new()
s.header("Risks", "Four uncertainties could change the answer. Each has a test and a trigger")
table(s, 0.6, 1.85, [2.3, 3.2, 3.35, 3.28], ["Uncertainty", "Why it matters", "How we test it", "Trigger and action"],
      [["Will demand hold beyond volunteers?", "All adoption and productivity data come from volunteer accounts, which are larger than average.",
        "Q1: offer Pro to a random sample of non-beta accounts at $12, with a $15 arm, and measure conversion and usage.",
        [[B("Below 15% implied adoption: "), "pause the launch and move the engineers back to mobile."]]],
       ["Usage and inference cost", "The top 10% of accounts make 58% of requests, and the inference price is fixed only until December 2027.",
        "Track requests per seat each month and renegotiate the contract in H2 2027.",
        [[B("Mean above 600 per seat, or Copilot margin below 55%: "), "tighten the allowance or raise the overage price."]]],
       ["Is Routewise’s AI the cause?", "Our win-rate drop coincided with Routewise’s 20%-off first-year promotion.",
        "Q1 win-loss interviews that separate AI from price. Track the win rate after launch.",
        [[B("No recovery toward 44% by Q4 2027: "), "respond on price and promotion rather than adding more AI."]]],
       ["Cost of the mobile delay", "Mobile is the top churn reason, and its rewrite slips by two quarters.",
        "Use a re-baselined date and track churn by reason each month.",
        [[B("Mobile-related churn rising: "), "bring the engineers back as soon as the launch ships."]]]],
      size=11, hsize=11)
s.rect(0.6, 5.2, 12.13, 1.6, fill=PANEL)
s.text(0.85, 5.3, 11.6, 0.3, "What would change our recommendation", size=12.5, bold=True, color=BLUE_D)
s.text(0.85, 5.66, 11.6, 1.1,
       [[B("Mobile first: "), "the Q1 test implies Pro adoption below 15%, or engineering confirms the rewrite would end most mobile churn."],
        [B("A higher Pro price: "), "the $15 arm converts at least 80% as well as the $12 arm. At that point $15 earns the same or more ARR (12 ÷ 15 = 0.8)."],
        [B("Not launching: "), "random-sample accounts show no productivity gain and win-loss work shows Routewise’s promotion, not its AI, drove the losses."]],
       size=11, bullet=True, space_after=3)
s.footer(SRC + ". Thresholds are proposed management triggers.")

# ------------------------------------------------------------------ 13. Plan
s = D.new()
s.header("2027 plan", "Test in Q1, launch in Q2, review in Q3 and restart mobile on a fixed date")
qs = ["Q1 2027", "Q2 2027", "Q3 2027", "Q4 2027"]
lanes = [("Copilot and Pro", ["Make Copilot production-ready (14 engineers)", "Launch Pro at $91 per seat. Move beta accounts onto Pro",
                              "Tune the allowance and overage on real usage", "Renegotiate the inference contract before December expiry"]),
         ("Mobile", ["Rewrite paused, with the date re-baselined", "Rewrite paused", "The 14 engineers return to the rewrite",
                     "Rewrite in progress against the fixed date"]),
         ("Commercial", ["Random-sample price test ($12 and $15). Win-loss study", "Pro leads every deal Routewise contests",
                         "Track Pro adoption and win rate", "Plan the 2028 price, with inference costs falling"])]
x0 = 2.6; qw = 2.53
for i, q in enumerate(qs):
    s.rect(x0 + i * qw + 0.04, 1.85, qw - 0.08, 0.42, fill="#0f2a4a")
    s.text(x0 + i * qw + 0.04, 1.85, qw - 0.08, 0.42, q, size=12, bold=True, color="#ffffff", align="c", valign="m")
ly = 2.37
for lab, cells in lanes:
    s.text(0.6, ly, 1.9, 0.7, lab, size=12, bold=True, valign="m")
    for i, c in enumerate(cells):
        s.rect(x0 + i * qw + 0.04, ly, qw - 0.08, 0.7, fill="#eef4fc" if lab != "Mobile" else PANEL)
        s.text(x0 + i * qw + 0.14, ly, qw - 0.28, 0.7, c, size=10.5, valign="m")
    ly += 0.78
# gates
s.text(0.6, ly + 0.05, 1.9, 0.55, "Decision gates", size=12, bold=True, valign="m")
for qi, txt in [(0, "March go/no-go: implied adoption of at least 15%?"), (2, "Q3 review: adoption, requests per seat, Copilot margin of 55% or more, win rate")]:
    gx_ = x0 + qi * qw + 0.04
    s.rect(gx_, ly + 0.05, qw - 0.08, 0.6, fill="#ffffff", line=BLUE, lw=1.25)
    s.text(gx_ + 0.1, ly + 0.05, qw - 0.28, 0.6, [("◆ ", {"color": BLUE, "bold": True}), (txt, {"bold": True})], size=10, valign="m")
ly += 0.82
s.rect(0.6, ly, 12.13, 6.8 - ly, fill=PANEL)
s.text(0.85, ly + 0.12, 11.6, 0.3, "Decisions requested today", size=13, bold=True, color=BLUE_D)
for i, t in enumerate([[B("1. "), "Approve a Q2 2027 launch of Pro at $91 per seat, with Copilot and 600 requests per seat"],
                        [B("2. "), "Reject the $149 add-on and the free-in-Core option"],
                        [B("3. "), "Assign 14 engineers for Q1–Q2 and re-baseline mobile on a fixed date"],
                        [B("4. "), "Approve the Q1 price test and the March go/no-go"]]):
    s.text(0.85 + (i % 2) * 5.9, ly + 0.48 + (i // 2) * 0.48, 5.7, 0.45, [t], size=11.5, space_after=4)
s.footer(SRC)

# ------------------------------------------------------------------ 14. Appendix A: calculations
s = D.new()
s.header("Appendix A · Calculations", "How the key numbers are built")
table(s, 0.6, 1.8, [2.55, 6.6, 2.98], ["Figure", "Calculation (all inputs from the briefing pack unless marked as an assumption)", "Result"],
      [["ARR and gross profit today", "9,800 accounts × 6.2 seats × $79 × 12, at a 78% gross margin", "$57.6M ARR, $44.9M gross profit"],
       ["CPO add-on claim", "46% × 9,800 × $149 × 12", "$8.06M"],
       ["Add-on scenarios", "7% / 10% / 14% × 9,800 × $1,788 a year. Inference: 6,800 requests × $0.009 × 12 per buyer. Less $0.6M platform cost",
        "$1.23M / $1.75M / $2.45M ARR. GP $0.12M / $0.43M / $0.85M"],
       ["Pro scenarios", "15% / 25% / 33% × 9,800 × 6.2 seats × $12 × 12. Inference: 444 requests per seat (3,600 ÷ 8.1) × $0.009. "
        "Less $0.6M. Adoption rates are an assumption", "$1.31M / $2.19M / $2.89M ARR. GP $0.27M / $0.86M / $1.32M"],
       ["Free in Core", "9,800 × 2,756 requests (or 1,900 at the median) × $0.009 × 12, plus $0.6M. GM = ($44.9M − cost) ÷ $57.6M",
        "Cost $3.5M ($2.6M). GM 71.9% (73.5%)"],
       ["NRR points", "Expansion ARR ÷ $57.6M starting ARR", "Pro base: 3.8 points"],
       ["Routewise exposure", "2,600 × 60% × 7 points × $5,878. Sales memo: 1,560 × 63% lost ÷ 3 × $5,878",
        "≤ $0.64M a year (memo: $1.9M)"],
       ["Churn by reason", "1,190 churned accounts × share × $5,878", "Mobile $1.9M · price $1.5M · AI $0.4M"],
       ["Mobile delay", "$1.9M × 0.5 year × the share of mobile churn the rewrite removes (assumption: 50%, or 100% at worst)",
        "$0.47M ($0.94M)"],
       ["Engineering", "14 engineers × $210K × 0.5 year", "$1.47M one-off"]],
      size=10.5, hsize=10.5, pad=0.065)
s.footer(SRC + ". GP = Copilot gross profit after inference and platform cost.")

# ------------------------------------------------------------------ 15. Appendix B: judgement calls & evidence notes
s = D.new()
s.header("Appendix B · Evidence notes", "Where we corrected internal claims, and the judgement calls behind this deck")
s.text(0.6, 1.8, 6.0, 0.3, "Internal claims, compared with the evidence", size=12, bold=True)
table(s, 0.6, 2.15, [2.2, 3.85], ["Claim", "What the evidence supports"],
      [["“46% likely to buy, about $8M in year one” (CPO)", "A 6% response skewed to large accounts. Real paywall conversion was 14% among volunteers. Plan on $1.2–2.5M."],
       ["“Copilot recovers a third of the deals we lose to Routewise” (VP Sales)", "Mentioning AI is not the same as losing because of AI. "
        "At most, parity wins back the 7-point drop: ~109 deals, or $0.64M."],
       ["Beta renewal of 97% against 93%", "Volunteer selection. Not used as a benefit."],
       ["Top 10% of accounts make 58% of requests", "Inconsistent with their 14,500-request mean (which implies 40%). Product should reconcile the two."]],
      size=11, hsize=11, pad=0.08)
s.text(6.95, 1.8, 5.78, 0.3, "Judgement calls we made (open to challenge)", size=12, bold=True)
s.text(6.95, 2.2, 5.78, 4.6,
       [[B("Pro adoption of 25% in the base case, "), "set between the paywall rate (14%) and the 2023 tier precedent (33%)."],
        [B("The allowance (600 per seat) and the overage price ($20 per 1,000) "), "are our design proposals, not figures from the pack."],
        [B("The $0.6M platform cost "), "is treated as cost of revenue. That is conservative for the margin test."],
        [B("Mobile rewrite effect: "), "we assume it halves mobile churn, and show an upper case where it ends it."],
        [B("Churn uses the 1,190 accounts in Table 3. "), "With a full year of 14% churn (~1,370 accounts), each figure rises ~15%. "
         "The recommendation does not change."],
        [B("Costs use the beta mean of 3,600 requests "), "rather than the lower figure that the 58% share implies."],
        [B("No retention benefit from Copilot "), "is counted in the base case."]],
      size=11.5, bullet=True, space_after=6)
s.footer(SRC)

D.save(OUT, PREV)
print("\n".join(WARN) if WARN else "no overflow warnings")
