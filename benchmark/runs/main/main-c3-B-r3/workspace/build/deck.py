import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from engine import *

OUT = sys.argv[1]; PREV = sys.argv[2]
D = Deck()
SECTIONS = ["1  Is it worth launching?", "2  How to package and price", "3  When to launch", "4  Making it work"]
page = [0]

def T(x, y, w, h, paras, size=12, **kw):
    if isinstance(paras, str): paras = [{"text": paras}]
    paras = [p if isinstance(p, dict) else {"text": p} for p in paras]
    return dict(t="text", x=x, y=y, w=w, h=h, paras=paras, size=size, **kw)

def B(items, size=12, sb=4, color=INK):
    return [{"text": t, "bullet": True, "size": size, "space_before": sb if i else 0, "color": color} for i, t in enumerate(items)]

def chrome(title, source, section=None, title_size=22):
    page[0] += 1
    els = []
    if section is not None:
        # tracker
        x = 0.5
        for i, s in enumerate(SECTIONS):
            active = i == section
            els.append(T(x, 0.22, 2.9, 0.28, [{"text": s, "size": 9, "bold": active, "color": BLUE if active else MUTED}]))
            x += 3.0
        els.append(dict(t="line", x=0.5, y=0.5, x2=12.83, y2=0.5, color=GRID, lw=0.5))
    els.append(T(0.5, 0.55, 12.33, 1.0, [{"text": title, "size": title_size, "bold": True}], valign="middle"))
    els.append(dict(t="line", x=0.5, y=1.6, x2=12.83, y2=1.6, color=INK, lw=1))
    els.append(T(0.5, 6.95, 11.3, 0.42, [{"text": source, "size": 8.5, "color": MUTED}], valign="bottom"))
    els.append(T(12.2, 7.05, 0.63, 0.3, [{"text": str(page[0]), "size": 9, "color": MUTED, "align": "r"}]))
    return els

def box_head(x, y, w, text, color=INK):
    return [T(x, y, w, 0.32, [{"text": text, "size": 12.5, "bold": True, "color": color}]),
            dict(t="line", x=x, y=y + 0.34, x2=x + w, y2=y + 0.34, color=RULE)]

SRC = "Source: Brightwork briefing pack (synthetic benchmark data); team analysis. "

# =========================== 1. Title ===========================
page[0] += 1
D.add([
    dict(t="rect", x=0, y=0, w=W, h=H, fill="ffffff"),
    dict(t="rect", x=0.5, y=2.2, w=0.08, h=2.2, fill=BLUE),
    T(0.8, 2.1, 11.5, 1.5, [{"text": "Dispatch Copilot: launch it inside a Pro tier, after the mobile rewrite", "size": 34, "bold": True}], valign="bottom"),
    T(0.8, 3.65, 11.5, 0.8, [{"text": "Launch timing, packaging and pricing: recommendation to the CEO and executive team", "size": 18, "color": INK2}]),
    T(0.8, 5.6, 11.5, 0.9, [{"text": "January 2027 planning  |  Prepared November 2026", "size": 12, "color": INK2},
                            {"text": "Built only from the internal briefing pack. All company, competitor and market figures are synthetic benchmark data.", "size": 10, "color": MUTED, "space_before": 4}]),
], "title")

# =========================== 2. Exec summary ===========================
els = chrome("Launch Dispatch Copilot in a new Pro tier at +$12 per seat in Q4 2027, not as a $149 add-on in Q2: "
             "it is a ~$2M ARR expansion lever, and the mobile rewrite should go first",
             SRC + "Ranges show low–high cases; base case in bold. ARR = annual recurring revenue; NRR = net revenue retention.", title_size=21)
pts = [
    ("1", "Copilot is worth launching, but it is worth ~$2M of ARR, not $8M",
     "The $8M rests on a survey with a 6% response rate; only 14% of engaged beta accounts actually paid $149. Realistic new ARR is "
     "$1.2–2.9M. It is still the only lever in the pack that adds the expansion NRR needs: without it NRR reaches ~103%, short of 105%.", 0),
    ("2", "Package it in Pro at +$12 per seat with a usage allowance, not as a $149 add-on",
     "A flat per-account fee draws the heaviest users (buyers average 6,800 requests, $61 a month of inference) and is an extra charge where "
     "Routewise includes AI in Pro. Pro base case: **$2.2M ARR, $0.9M gross profit, 76.6% company margin.** Free inclusion would cut margin to 70–74%.", 1),
    ("3", "Launch in Q4 2027 and keep the mobile rewrite on schedule",
     "Mobile reliability causes 27% of churn, AI 6%. A two-quarter mobile delay loses ~$0.54M of ARR for good; a two-quarter Copilot delay loses "
     "~$0.28M and defers ~$0.4M of profit. The money is close, so the stronger evidence and longer-lasting effect of the mobile fix decide it.", 2),
    ("4", "Use 2027 to prove Copilot with non-volunteers, with a trigger to launch sooner",
     "Run a randomised Pro pilot, keep beta accounts live, equip Sales for Routewise deals and renegotiate inference before Dec 2027. Bring launch "
     "forward to Q2 only if the Q4 2026 data show AI, not Routewise's 20% discount, drove the lost deals and the rewrite will fix <40% of mobile churn.", 3),
]
y = 1.8
for num, head, body, sec in pts:
    els += [T(0.5, y, 0.45, 0.45, [{"text": num, "size": 16, "bold": True, "color": "ffffff", "align": "c"}], fill=BLUE, valign="middle"),
            T(1.1, y - 0.04, 3.6, 1.1, [{"text": head, "size": 13, "bold": True}]),
            T(4.85, y - 0.04, 7.98, 1.1, [{"text": body, "size": 11.5, "color": INK}]),
            dict(t="line", x=1.1, y=y + 1.13, x2=12.83, y2=y + 1.13, color=GRID, lw=0.5)]
    y += 1.22
D.add(els, "exec")

# =========================== 3. Hypothesis test ===========================
els = chrome("We tested the CPO's plan against five conditions it needs: only the strategic need holds, so the answer changes on price, packaging and timing",
             SRC + "Initial hypothesis = CPO proposal (§4). Verdicts weigh evidence quality, not only direction.")
X = "×  Not supported"; P = "~  Plausible, unproven"; OK = "√  Supported"
rows = [["#", "For 'launch in Q2 2027 as a $149 add-on' to be right…", "What the evidence shows", "Verdict", "So what"],
        ["1", "Customers will buy at $149 at scale (≈46%)", "Survey: 6% response, respondents 9.4 seats vs 6.2 base. Paywall test: 14% of engaged volunteers bought",
         {"text": X, "color": CRIT, "bold": True}, "Size at $1.2–2.5M ARR, not $8M"],
        ["2", "Copilot improves outcomes for typical customers", "+11% vs +2% jobs per dispatcher-hour; 97% vs 93% renewal, but only among self-selected, larger volunteers",
         {"text": P, "color": INK2, "bold": True}, "Prove it with non-volunteers before scaling"],
        ["3", "A flat per-account price earns a healthy margin", "Buyers average 6,800 requests = $61/month cost (59% margin); top 10% of accounts = $131 (12% margin)",
         {"text": X, "color": CRIT, "bold": True}, "Price per seat, with an allowance"],
        ["4", "Copilot is needed to compete and to hit 105% NRR", "Win rate vs Routewise fell 44% → 37% after it put AI in Pro; NRR needs +4 pts and mobile alone gives ~+2",
         {"text": OK, "color": GOODTXT, "bold": True}, "Launch it, in a Pro tier like Routewise (causation partly confounded)"],
        ["5", "Copilot matters more than mobile over the next two quarters", "Churn reasons: mobile 27% vs AI 6%. Top request: mobile app 38% vs AI scheduling 19%",
         {"text": X, "color": CRIT, "bold": True}, "Keep the rewrite first; Copilot in Q4 2027"]]
els.append(dict(t="table", x=0.5, y=1.85, cols=[0.4, 3.0, 4.6, 1.9, 2.43], rows=rows, size=11, hsize=11, minh=0.62,
                aligns=["c", "l", "l", "l", "l"], hfill=INK))
els.append(T(0.5, 6.1, 12.33, 0.6, [{"text": "**Revised answer:** launch Copilot, but packaged in a per-seat Pro tier and sequenced after the mobile rewrite. The rest of the deck tests each part.", "size": 12}],
             fill=LBLUE, valign="middle"))
D.add(els, "hypothesis")

# =========================== 4. Demand sizing ===========================
els = chrome("The $8M forecast assumes 46% of accounts will buy; actual buying behaviour points to $1.2–2.5M of new ARR for a $149 add-on",
             SRC + "§4, §6, §10. Low case assumes non-volunteer accounts buy at half the volunteer rate (our assumption). Survey n = 610 of 9,800 admins.", section=0)
els += box_head(0.5, 1.8, 6.4, "New ARR from a $149/account/month add-on, $M")
els.append(dict(t="chart", kind="bar", x=0.5, y=2.25, w=6.4, h=2.9,
                cats=["CPO: survey intent (46%)", "Paywall rate, all accounts (14%)", "Low case: half paywall rate (7%)"],
                series=[("ARR", [8.06, 2.45, 1.23])], colors=[[ORANGE, BLUE, BLUE]],
                labels=[["$8.1M", "$2.5M", "$1.2M"]], vmax=10, gap=55, catsize=11))
els.append(T(0.5, 5.25, 6.4, 1.6, [
    {"text": "**How it is calculated:** accounts × buy rate × $149 × 12", "size": 10.5, "color": INK2},
    {"text": "CPO: 9,800 × 46% = 4,508 × $1,788 = $8.06M", "size": 10.5, "color": INK2, "space_before": 3},
    {"text": "Paywall: 9,800 × 14% = 1,372 × $1,788 = $2.45M", "size": 10.5, "color": INK2, "space_before": 2},
    {"text": "Low: 9,800 × 7% = 686 × $1,788 = $1.23M", "size": 10.5, "color": INK2, "space_before": 2}]))
els += box_head(7.3, 1.8, 5.53, "Why the survey overstates demand ~3–6×")
els.append(T(7.3, 2.25, 5.53, 4.5, B([
    "**Self-selected sample.** Only 610 of 9,800 admins replied (6%). People who reply to an AI survey tend to be the ones interested in AI.",
    "**Skewed to large accounts.** Respondents average 9.4 seats vs 6.2 across the base.",
    "**Intent is not purchase.** 'Likely' or 'very likely' (46%) compares with the 14% of beta accounts that paid after 8+ weeks of free use: 3.3× lower.",
    "**Even 14% is a ceiling.** Beta accounts volunteered, are larger (8.1 seats) and more active than the base. The typical account is likely to buy at a lower rate.",
    "**Implication:** plan on $1.2–2.5M for the add-on. That is enough to matter for NRR (+2–4 pts) but it is not an $8M business."], size=11.5, sb=7)))
D.add(els, "demand")

# =========================== 5. Beta evidence ===========================
els = chrome("Beta gains are encouraging, but they come from volunteers, so the productivity case is unproven for the typical customer",
             SRC + "§5 Tables 1–2. *Table 2 implies the top 10% generate ~40% of requests (14,500 × 10% ÷ 3,600), not the 58% stated; either way usage is concentrated.", section=0)
els += box_head(0.5, 1.8, 6.0, "Beta (240 volunteer accounts) vs matched non-beta accounts")
els.append(dict(t="chart", kind="col", x=0.5, y=2.3, w=2.9, h=3.2, cats=["Beta", "Matched"],
                series=[("Jobs/hr", [11, 2])], colors=[[BLUE, MGRAY]], labels=[["+11%", "+2%"]], vmax=14, gap=70, catsize=11))
els.append(T(0.5, 5.5, 2.9, 0.5, [{"text": "Change in jobs scheduled per dispatcher-hour vs prior 12 weeks", "size": 10, "color": INK2, "align": "c"}]))
els.append(dict(t="chart", kind="col", x=3.6, y=2.3, w=2.9, h=3.2, cats=["Beta", "Matched"],
                series=[("Renewal", [97, 93])], colors=[[BLUE, MGRAY]], labels=[["97%", "93%"]], vmax=112, gap=70, catsize=11))
els.append(T(3.6, 5.5, 2.9, 0.5, [{"text": "90-day renewal rate", "size": 10, "color": INK2, "align": "c"}]))
els.append(T(0.5, 6.1, 6.0, 0.65, [{"text": "Dispatchers also self-reported 4.1 hours saved per week (no control group, so not measured).", "size": 10.5, "color": INK2}]))
els += box_head(7.0, 1.8, 5.83, "Why the gains may not carry over to the whole base")
els.append(T(7.0, 2.25, 5.83, 3.4, B([
    "**Selection bias.** Volunteers chose to join; they are larger (8.1 vs 6.2 seats) and more active. Engaged accounts renew more anyway.",
    "**Concentrated use.** The median account sent 1,900 requests a month, the mean 3,600 and the top 10% 14,500*. A few power users drive the averages.",
    "**Short window.** 12 weeks, with novelty effects, and a 90-day renewal read on a sample of 240.",
    "**Still a real signal.** A 9-point productivity gap against a matched group is not nothing. It needs confirming, not dismissing."], size=11.5, sb=7)))
els.append(T(7.0, 5.75, 5.83, 1.0, [{"text": "**Implication:** run a randomised pilot on non-volunteer accounts (slide 14) before committing to scale assumptions. Our Pro base case already discounts the beta results.", "size": 11.5}],
             fill=LBLUE, valign="middle"))
D.add(els, "beta")

# =========================== 6. NRR bridge ===========================
els = chrome("Copilot is still needed: no other lever in the pack adds the expansion needed to lift NRR from 101% to 105%",
             SRC + "§3, §8. Lever size = ARR effect ÷ $57.6M. Pro: 25% of accounts × 6.2 seats × $12 × 12. Mobile: 50% of the 27% mobile-driven churn removed (assumption). "
             "AI churn: half of 6% AI-driven churn avoided (assumption).", section=0)
els += box_head(0.5, 1.8, 7.2, "NRR bridge to 2028 vs the 105% target, base case, % (levers at full effect)")
base = [0, 101, 104.8, 106.7, 0]; delta = [101, 3.8, 1.9, 0.4, 107.1]
els.append(dict(t="chart", kind="stackcol", x=0.5, y=2.25, w=7.2, h=3.9,
                cats=["Today", "Copilot in Pro\n(tier migration)", "Mobile rewrite\n(less churn)", "Copilot\n(less AI churn)", "2028 potential"],
                series=[("base", [100, 101, 104.8, 106.7, 100]), ("delta", [1, 3.8, 1.9, 0.4, 7.1]), ("label", [0.6] * 5)],
                colors=[[None] * 5, [MGRAY, BLUE, ORANGE, BLUE, INK], [None] * 5],
                labels=[None, None, ["101%", "+3.8", "+1.9", "+0.4", "107.1%"]], lpos=[None, None, XL_LABEL_POSITION.CENTER],
                vmin=100, vmax=108.5, gap=45, catsize=10))
els.append(T(0.5, 6.2, 7.2, 0.55, [{"text": "Axis starts at 100% (no net change). Target: 105%. Orange marks the non-Copilot lever.", "size": 9.5, "color": MUTED}]))
els += box_head(8.1, 1.8, 4.73, "Can each lever reach 105% on its own?")
rows = [["NRR in 2028", "Low", "Base", "High"],
        ["Copilot (Pro) only", "103.1%", {"text": "105.2%", "bold": True}, "106.8%"],
        ["Mobile rewrite only", "101.9%", {"text": "102.9%", "bold": True}, "103.8%"],
        ["Both levers", "104.0%", {"text": "107.1%", "bold": True}, "109.6%"]]
els.append(dict(t="table", x=8.1, y=2.3, cols=[1.9, 0.94, 0.95, 0.94], rows=rows, size=11, minh=0.4, aligns=["l", "r", "r", "r"], hfill=INK))
els.append(T(8.1, 4.1, 4.73, 2.7, B([
    "Only Copilot can reach 105% alone, and only in the base case. Both levers together give a margin of safety.",
    "**Migration is a one-off step.** NRR rises while accounts move to Pro, then the uplift fades; lower churn from a reliable app keeps paying every year.",
    "So the question is not whether to do Copilot, but **in what order**: section 3."], size=11, sb=6)))
D.add(els, "nrr")

# =========================== 7. Competition ===========================
els = chrome("The competitive threat is real but worth at most ~$0.6M of new ARR a year, not the ~$1.9M the Sales memo implies",
             SRC + "§7, §10, §11. ARR per new account = 6.2 seats × $79 × 12 = $5,878. Contested opportunities = 2,600 × 60% = 1,560 a year.", section=0)
els += box_head(0.5, 1.8, 6.2, "Win rate where Routewise competes")
els.append(dict(t="chart", kind="col", x=0.5, y=2.25, w=6.2, h=3.3,
                cats=["Q1–Q2 2026", "Q3 2026\n(Routewise AI + 20% promo)", "Sales memo implies"],
                series=[("Win rate", [44, 37, 58])], colors=[[MGRAY, BLUE, ORANGE]], labels=[["44%", "37%", "58%"]], vmax=68, gap=60, catsize=10))
els.append(T(0.5, 5.6, 6.2, 1.2, [
    {"text": "**Most that Copilot could recover:** the 7-pt drop × 1,560 = 109 deals × $5,878 = **$0.64M ARR a year**", "size": 10.5, "color": INK},
    {"text": "**Sales memo:** a third of 983 lost deals = 328 deals = $1.93M. That needs a 58% win rate, well above the 44% before Routewise launched AI.", "size": 10.5, "color": INK, "space_before": 4}]))
els += box_head(7.1, 1.8, 5.73, "Why the true AI effect is likely smaller")
els.append(T(7.1, 2.25, 5.73, 3.3, B([
    "**Confounded timing.** In the same quarter, Routewise offered 20% off the first year. The drop may be about price, not AI.",
    "**Mention is not cause.** 31% of loss notes mention AI; that does not mean AI decided those deals.",
    "**Testable now.** The promo ran in Q3 2026. If the Q4 2026 win rate recovers towards 44%, AI was not the main driver.",
    "**Doesn't count towards NRR.** New-logo wins grow ARR but are outside the NRR objective."], size=11.5, sb=7)))
els.append(T(7.1, 5.65, 5.73, 1.1, [{"text": "**Implication:** competing means matching Routewise's **packaging** (AI in Pro) as much as the feature. The base case assumes AI explains half the drop: ~$0.32M ARR a year.", "size": 11.5}],
             fill=LBLUE, valign="middle"))
D.add(els, "competition")

# =========================== 8. Options ===========================
els = chrome("Of four packaging options, a Pro tier at +$12 per seat earns the most and is the only one that matches Routewise while keeping margin above 75%",
             SRC + "§1, §5, §6, §7. Run-rate after one year; ranges low–high. Copilot gross profit = revenue − inference − $0.6M platform cost (treated as cost of revenue). "
             "Company margin base: $57.6M ARR at 78%. Full workings in the appendix.", section=1)
G = {"text": "", "fill": "e6f2e6"}
rows = [["", "A  $149 add-on per account\n(CPO proposal)", "B  Pro tier, +$12 per seat,\nwith allowance (recommended)", "C  Include free in Core", "D  Don't launch"],
        ["Adoption assumed", "10% (7–14%)", "25% (14–33%)", "All accounts", "—"],
        ["New ARR", "$1.75M (1.23–2.45)", {"text": "$2.19M (1.23–2.89)", "bold": True}, "$0", "$0"],
        ["Copilot gross profit", "$0.43M (0.12–0.85)", {"text": "$0.86M (0.22–1.33)", "bold": True}, "−$2.6M to −$4.4M", "$0"],
        ["Company gross margin (≥75%)", "76.4% √", {"text": "76.6% √ (≥76.3% even if heavy users)", "bold": True}, {"text": "70.3–73.5% ×", "color": CRIT, "bold": True}, "78.0% √"],
        ["NRR uplift from expansion", "+3.0 pts", {"text": "+3.8 pts", "bold": True}, "0 pts", "0 pts"],
        ["vs Routewise (AI included in Pro)", "Looks like an extra charge", {"text": "Matches", "bold": True}, "Better than parity", {"text": "Gap widens ×", "color": CRIT, "bold": True}],
        ["Heavy-user cost risk", {"text": "High: buyers self-select (6,800 requests)", "color": CRIT}, "Capped by allowance", {"text": "Highest", "color": CRIT}, "None"]]
for r in rows[1:]:
    r[2] = r[2] if isinstance(r[2], dict) else {"text": r[2]}
    r[2]["fill"] = "e8f1fc"
els.append(dict(t="table", x=0.5, y=1.85, cols=[2.45, 2.5, 2.98, 2.2, 2.2], rows=rows, size=11, hsize=11, minh=0.5,
                aligns=["l", "c", "c", "c", "c"], hfill=INK))
els.append(T(0.5, 6.15, 12.33, 0.6, [{"text": "**Read-across:** A and B bring in similar revenue, but B earns twice the gross profit, matches Routewise, and costs an average account $74 a month instead of $149. C breaks the margin rule; D gives up the main NRR lever.", "size": 11.5}],
             fill=LBLUE, valign="middle"))
D.add(els, "options")

# =========================== 9. Unit economics ===========================
els = chrome("A flat $149 fee attracts heavy users whose inference cost nearly eats the price; per-seat pricing with an allowance keeps cost in step with revenue",
             SRC + "§5 Table 2, §6. Inference at $0.009 per request (fixed through Dec 2027). Per-seat use = beta mean 3,600 ÷ 8.1 seats = 444 requests. "
             "Heavy case = Pro adopters behave like paywall buyers (6,800 per 6.2-seat account).", section=1)
els += box_head(0.5, 1.8, 6.6, "Monthly inference cost per account vs the $149 add-on price")
els.append(dict(t="chart", kind="bar", x=0.5, y=2.25, w=6.6, h=3.3,
                cats=["Median account (1,900 req.)", "Mean account (3,600)", "Paywall buyers (6,800)", "Top 10% of accounts (14,500)"],
                series=[("Cost", [17.1, 32.4, 61.2, 130.5])], colors=[[MGRAY, MGRAY, ORANGE, ORANGE]],
                labels=[["$17 (89% margin)", "$32 (78%)", "$61 (59%)", "$131 (12%)"]], vmax=170, gap=50, catsize=10.5))
els.append(T(0.5, 5.6, 6.6, 1.2, B([
    "Those who buy are the heavy users: buyers averaged 6,800 requests a month, nearly twice the beta mean.",
    "Price is the same for every account, but cost grows with use, so the best customers are the least profitable."], size=11, sb=4)))
els += box_head(7.5, 1.8, 5.33, "Per seat: revenue scales with account size")
rows = [["Per Pro seat, per month", "Typical use", "At allowance cap"],
        ["Price uplift", "$12.00", "$12.00"],
        ["Requests", "444", "500"],
        ["Inference cost", "$4.00", "$4.50"],
        ["Contribution margin", {"text": "67%", "bold": True}, {"text": "62.5%", "bold": True}]]
els.append(dict(t="table", x=7.5, y=2.3, cols=[2.33, 1.5, 1.5], rows=rows, size=11, minh=0.36, aligns=["l", "r", "r"], hfill=INK))
els.append(T(7.5, 4.25, 5.33, 1.3, B([
    "Seats track use: beta accounts were 8.1 seats and used 444 requests per seat.",
    "**Without a cap, a heavy-user Pro mix breaks the margin rule:** company margin 74.1–74.8% at 25–33% adoption. With a 500-request allowance it stays at 76.3–76.4%."], size=11, sb=4)))
els.append(T(7.5, 5.75, 5.33, 1.0, [{"text": "**Implication:** price per seat and include a pooled usage allowance; sell extra usage in packs rather than giving it away.", "size": 11.5}],
             fill=LBLUE, valign="middle"))
D.add(els, "unit")

# =========================== 10. Pro design ===========================
els = chrome("Recommended design: Pro at $91 per seat with 500 pooled AI requests per seat and paid request packs above that, with no standalone add-on",
             SRC + "§1, §5, §6, §9. Allowance level and pack price are our design proposals, to be confirmed in the 2027 pilot. Payback includes retained and won ARR "
             "(base: $0.56M a year at 78% margin) and the $1.47M engineering cost (14 × 0.5 year × $210k).", section=1)
els += box_head(0.5, 1.8, 5.9, "The offer")
rows = [["Element", "Recommendation", "Rationale"],
        ["Pro price", "$91/seat/month (Core $79 + $12)", "Matches Routewise; average account pays +$74 a month (+15%)"],
        ["Included usage", "500 AI requests/seat/month, pooled", "Above beta mean (444/seat); caps cost at $4.50/seat"],
        ["Extra usage", "Packs at $20 per 1,000 requests", "2.2× the $9 cost; heavy users pay their way"],
        ["Core plan", "Unchanged at $79; no AI", "Price drives 22% of churn: no forced rise"],
        ["Add-on", "None at launch", "One price point; avoids adverse selection"],
        ["Beta accounts", "Keep live until launch, then a Pro launch offer", "Protects 240 engaged accounts"]]
els.append(dict(t="table", x=0.5, y=2.3, cols=[1.25, 2.2, 2.45], rows=rows, size=10.5, minh=0.42, aligns=["l", "l", "l"], hfill=INK))
els += box_head(6.8, 1.8, 6.03, "Economics, base case (25% adoption)")
els.append(dict(t="chart", kind="bar", x=6.8, y=2.25, w=6.03, h=2.4,
                cats=["Pro revenue", "Inference cost", "Platform, evaluation, support", "Copilot gross profit"],
                series=[("$M", [2.19, -0.73, -0.60, 0.86])], colors=[[BLUE, ORANGE, ORANGE, INK]],
                labels=[["$2.19M", "−$0.73M", "−$0.60M", "$0.86M"]], vmin=-1.2, vmax=3.0, gap=45, catsize=10.5, ticklow=True))
rows = [["Test", "Result"],
        ["Adoption needed to cover the $0.6M run cost", "10% (6,250 seats ≈ 1,010 accounts)"],
        ["Payback of $1.47M engineering", "~21 months after launch"],
        ["Upside if inference falls 35% at renewal", "Cost/seat $4.00 → $2.60; margin 67% → 78%"]]
els.append(dict(t="table", x=6.8, y=4.8, cols=[3.33, 2.7], rows=rows, size=10.5, minh=0.38, aligns=["l", "l"], hfill=INK2))
D.add(els, "design")

# =========================== 11. Churn ===========================
els = chrome("Mobile reliability, not AI, drives churn: it explains 27% of lost accounts and ~$2.2M of ARR a year, 4.5× the AI-related loss",
             SRC + "§1, §8 Table 3. ARR lost by reason = share × 14% logo churn × $57.6M, assuming churned accounts are average size. n = 1,190 churned accounts in 2026.", section=2)
els += box_head(0.5, 1.8, 7.4, "Main reason for churning, 2026: share of churned accounts and ARR lost a year")
els.append(dict(t="chart", kind="bar", x=0.5, y=2.25, w=7.4, h=4.4,
                cats=["Mobile app reliability", "Price", "Other", "Missing integrations", "Out of business / sold", "Switched for AI features"],
                series=[("share", [27, 22, 16, 15, 14, 6])], colors=[[ORANGE, MGRAY, MGRAY, MGRAY, MGRAY, BLUE]],
                labels=[["27%  ·  $2.18M", "22%  ·  $1.77M", "16%  ·  $1.29M", "15%  ·  $1.21M", "14%  ·  $1.13M", "6%  ·  $0.48M"]], vmax=36, gap=45, catsize=11))
els += box_head(8.3, 1.8, 4.53, "Customers say the same thing")
els.append(dict(t="chart", kind="bar", x=8.3, y=2.25, w=4.53, h=1.6, cats=["Reliable mobile app", "AI scheduling"],
                series=[("rank", [38, 19])], colors=[[ORANGE, BLUE]], labels=[["38%", "19%"]], vmax=50, gap=50, catsize=10.5))
els.append(T(8.3, 3.85, 4.53, 0.35, [{"text": "Share of customers ranking it their top feature request, 2026", "size": 9.5, "color": INK2}]))
els.append(T(8.3, 4.3, 4.53, 2.45, B([
    "Head of Customer Success: \"Mobile reliability is what customers complain about.\"",
    "This evidence is solid: actual churn from 1,190 accounts, not volunteers or stated intent.",
    "Copilot's own case for fewer churned accounts is small: at most $0.48M a year."], size=11, sb=6)))
D.add(els, "churn")

# =========================== 12. Delay cost ===========================
els = chrome("Delaying the mobile rewrite costs about twice as much lasting ARR as delaying Copilot, so the rewrite should go first",
             SRC + "§3, §7, §8. Assumes the constraint is a straight swap: whichever ships first delays the other by two quarters. Base: rewrite removes 50% of mobile churn (25–75%); "
             "AI explains 50% of the win-rate drop (0–100%); Copilot avoids 50% of AI churn.", section=2)
els += box_head(0.5, 1.8, 6.7, "Cost of a two-quarter delay, base case, $M")
els.append(dict(t="chart", kind="bar", x=0.5, y=2.25, w=6.7, h=2.6,
                cats=["Delay mobile: ARR lost for good", "Delay Copilot: ARR lost for good", "Delay Copilot: profit deferred (not lost)"],
                series=[("$M", [0.54, 0.28, 0.43])], colors=[[ORANGE, BLUE, "86b6ef"]],
                labels=[["$0.54M (0.27–0.82)", "$0.28M (0.12–0.44)", "$0.43M, one-off"]], vmax=0.85, gap=45, catsize=10.5))
els.append(T(0.5, 4.95, 6.7, 1.85, [
    {"text": "**Mobile:** ½ year × 50% × $2.18M mobile-driven churn = $0.54M", "size": 10.5, "color": INK2},
    {"text": "**Copilot:** ½ year × (50% × $0.64M win-rate recovery + 50% × $0.48M AI churn) = $0.28M", "size": 10.5, "color": INK2, "space_before": 3},
    {"text": "**Deferred:** ½ year × Pro gross profit $1.46M before platform, less $0.30M platform cost saved = $0.43M", "size": 10.5, "color": INK2, "space_before": 3}]))
els += box_head(7.6, 1.8, 5.23, "The money is close; three tie-breakers favour mobile")
els.append(T(7.6, 2.25, 5.23, 3.4, B([
    "**Evidence quality.** Mobile's cost comes from real churn data. Copilot's comes from volunteers and a win-rate drop that coincides with a price promotion.",
    "**Durability.** Lower churn is a lasting gain. Deferring Copilot only moves profit later, and once the accounts have migrated to Pro, NRR is the same.",
    "**Fit with the 2028 target.** A Q4 2027 launch puts ~75% of a 12-month Pro migration inside 2028, against ~25% for a Q2 launch (if NRR is measured on calendar 2028)."], size=11, sb=7)))
els.append(T(7.6, 4.6, 5.23, 0.9, [{"text": "**Implication:** keep the rewrite on schedule and launch Copilot two quarters later, in Q4 2027.", "size": 11.5}],
             fill=LBLUE, valign="middle"))
D.add(els, "delay")

# =========================== 13. Sensitivity ===========================
els = chrome("Mobile-first holds in most scenarios: it flips only if AI explains most of the lost deals and the rewrite fixes less than ~26–40% of mobile churn",
             SRC + "Cell = lasting ARR lost by delaying mobile two quarters, minus lasting ARR lost by delaying Copilot two quarters ($M). Positive = mobile first is better. "
             "Excludes the one-off $0.43M profit deferral, which favours Copilot first.", section=2)
els += box_head(0.5, 1.8, 7.0, "Lasting-ARR advantage of mobile-first, $M")
def cell(v):
    fill = "c7dcf6" if v >= 0.2 else ("e8f1fc" if v > 0.02 else (LGRAY if v >= -0.02 else "f8d3d3"))
    return {"text": f"{v:+.2f}", "fill": fill, "bold": True, "align": "c"}
rows = [["Share of mobile churn the rewrite removes ↓   /   share of the win-rate drop AI explains →", "0%", "50%", "100%"],
        [{"text": "75%", "bold": True}, cell(0.70), cell(0.54), cell(0.37)],
        [{"text": "50%  (base)", "bold": True}, cell(0.42), cell(0.26), cell(0.10)],
        [{"text": "25%", "bold": True}, cell(0.15), cell(-0.01), cell(-0.17)]]
els.append(dict(t="table", x=0.5, y=2.3, cols=[3.4, 1.2, 1.2, 1.2], rows=rows, size=13, hsize=10.5, minh=0.7, aligns=["l", "c", "c", "c"], hfill=INK))
els.append(T(0.5, 5.25, 7.0, 1.5, B([
    "Break-even: if AI explains 100% of the drop, mobile first needs the rewrite to remove ≥40% of mobile churn; at 50%, ≥26%.",
    "Blue = mobile first is better; grey = neutral; red = Copilot first is better."], size=11, sb=5)))
els += box_head(7.9, 1.8, 4.93, "Trigger to bring the launch forward to end-Q2 2027")
els.append(T(7.9, 2.25, 4.93, 2.6, [
    {"text": "Bring the launch forward only if **both** are true at a trigger check by mid-February, once Q4 2026 data are final:", "size": 11.5},
    {"text": "**AI drove the lost deals:** the Q4 2026 win rate vs Routewise stays at ~37% after the 20% promotion ended, and the share of loss notes citing AI rises.", "size": 11.5, "bullet": True, "space_before": 7},
    {"text": "**The rewrite will under-deliver:** Engineering and CS cannot show it removes at least ~40% of mobile-driven churn.", "size": 11.5, "bullet": True, "space_before": 7}]))
els.append(T(7.9, 4.55, 4.93, 1.0, [{"text": "**Otherwise hold Q4 2027.** If the win rate recovers towards 44%, the case for waiting gets stronger: the Q3 drop was most likely the promotion, not AI.", "size": 11.5}],
             fill=LBLUE, valign="middle"))
D.add(els, "sensitivity")

# =========================== 14. Roadmap ===========================
els = chrome("A 2027 plan keeps the rewrite on track, uses the wait to prove Copilot with non-volunteers, and launches Pro in Q4",
             SRC + "Pilot size is our proposal: ~500 accounts gives about ±3 pts precision on a ~14% conversion rate. "
             "Beta inference ≈ 240 × 3,600 × $0.009 ≈ $8k a month. Assumes the rewrite needs the 14 engineers in H1 2027 only (to confirm).", section=3)
qx = [3.0, 5.46, 7.92, 10.38]; qw = 2.38
els.append(T(0.5, 1.8, 2.4, 0.35, [{"text": "Workstream", "size": 11, "bold": True, "color": INK2}]))
for i, q in enumerate(["Q1 2027", "Q2 2027", "Q3 2027", "Q4 2027"]):
    els.append(T(qx[i], 1.8, qw, 0.35, [{"text": q, "size": 11, "bold": True, "color": INK2, "align": "c"}]))
els.append(dict(t="line", x=0.5, y=2.18, x2=12.83, y2=2.18, color=INK, lw=0.75))
streams = [
    ("Mobile rewrite", [(0, 2, "On schedule with the full team, including the 14 engineers", ORANGE, "ffffff"), (2, 2, "Continues to its original plan; track mobile-driven churn after release", "fbe1d6", INK)]),
    ("Copilot build\n(14 engineers)", [(0, 2, "No launch build; small crew keeps the beta running", LGRAY, INK), (2, 2, "Launch hardening, allowance and metering; GA in Pro late Q4", BLUE, "ffffff")]),
    ("Validation", [(0, 1, "Keep 240 beta accounts live; design pilot", LGRAY, INK), (1, 1, "Randomised Pro pilot: ~500 non-volunteer accounts, 12 weeks", LBLUE, INK), (2, 2, "Track Pro usage per seat and productivity vs control", LGRAY, INK)]),
    ("Go-to-market", [(0, 1, "Routewise battlecard; read Q4 2026 win rate", LGRAY, INK), (1, 2, "Set final Pro price from pilot; early access in Routewise deals", LBLUE, INK), (3, 1, "Pro launch; beta launch offer", LBLUE, INK)]),
    ("Cost and margin", [(2, 2, "Renegotiate inference ahead of Dec 2027 expiry (list prices −35%)", LBLUE, INK)]),
    ("Decision gates", [(0, 1, "Mid-Feb: trigger check (launch sooner?)", WARN, INK), (1, 1, "End-Q2: go / no-go on pilot (conversion ≥10%, margin ≥75%)", WARN, INK)]),
]
y = 2.3
for name, bars in streams:
    els.append(T(0.5, y, 2.4, 0.62, [{"text": name.split("\n")[0], "size": 11.5, "bold": True}] + ([{"text": name.split("\n")[1], "size": 9.5, "color": INK2}] if "\n" in name else []), valign="middle"))
    for (q0, n, txt, fill, col) in bars:
        els.append(T(qx[q0] + 0.03, y + 0.05, qw * n + (qx[1] - qx[0] - qw) * (n - 1) - 0.06, 0.55, [{"text": txt, "size": 10, "color": col, "align": "c"}], fill=fill, valign="middle"))
    els.append(dict(t="line", x=0.5, y=y + 0.68, x2=12.83, y2=y + 0.68, color=GRID, lw=0.5))
    y += 0.74
D.add(els, "roadmap")

# =========================== 15. Risks ===========================
els = chrome("Six risks could change the answer; each has an early warning sign and a planned response",
             SRC + "Thresholds are proposed by the team and derived from the calculations in this deck.", section=3)
rows = [["Risk", "Early warning sign", "Response", "Impact if it happens"],
        ["1  Non-volunteers value Copilot less", "Pilot conversion <10% (run-cost break-even)", "Hold GA; narrow scope to AI scheduling for competitive deals", "Pro ARR at 14% adoption: $1.2M; gross profit $0.2M"],
        ["2  Heavy users erode margin", ">10% of Pro accounts above the 500-request allowance", "Enforce packs; revisit allowance at contract renewal", "Uncapped: company margin 74.1–74.8%"],
        ["3  Routewise extends its lead while we wait", "Win rate ≤37% after promo ended; AI share of loss notes rising", "Mid-February trigger check; early access in contested deals", "Up to $0.32M lasting ARR per half-year"],
        ["4  Rewrite fixes less churn than assumed", "Mobile-driven churn share not falling two quarters after ship", "Re-test sequencing; mobile first needs ≥26–40% fix", "Mobile-first advantage shrinks to ~$0"],
        ["5  Pro is read as a price rise", "Complaints or downgrades on Pro offers", "Core stays $79; Pro is opt-in; no forced migration", "Price already drives 22% of churn"],
        ["6  Inference prices after 2027", "Renewal terms in Q3–Q4 2027", "Per-seat pricing leaves headroom; tender if needed", "Mostly upside: cost/seat $4.00 → $2.60 at −35%"]]
els.append(dict(t="table", x=0.5, y=1.85, cols=[3.0, 3.25, 3.25, 2.83], rows=rows, size=11, minh=0.58, aligns=["l", "l", "l", "l"], hfill=INK, zebra="f7f7f5"))
D.add(els, "risks")

# =========================== 16. Decisions ===========================
els = chrome("Three decisions today lock in the plan and keep the option to launch sooner if the evidence shifts",
             SRC, section=3)
dec = [("Approve packaging and price", "Copilot only inside a new Pro tier at $91 per seat (+$12), with 500 pooled AI requests per seat and paid packs above that. Do not launch the $149 add-on; do not include Copilot free in Core."),
       ("Approve the sequence", "The mobile rewrite stays on schedule. Copilot GA targets late Q4 2027, with the 14-engineer build in H2. Engineering confirms by 31 January that the rewrite needs those engineers only in H1."),
       ("Approve the 2027 validation plan and trigger", "Randomised Pro pilot on ~500 non-volunteer accounts; keep the beta accounts live (~$8k a month); renegotiate inference before Dec 2027; trigger check by mid-February using final Q4 2026 win-rate data.")]
y = 1.9
for i, (h, b) in enumerate(dec, 1):
    els += [T(0.5, y, 0.55, 0.55, [{"text": str(i), "size": 18, "bold": True, "color": "ffffff", "align": "c"}], fill=BLUE, valign="middle"),
            T(1.25, y - 0.02, 3.6, 0.9, [{"text": h, "size": 14, "bold": True}]),
            T(4.9, y - 0.02, 7.93, 0.95, [{"text": b, "size": 12}]),
            dict(t="line", x=1.25, y=y + 1.0, x2=12.83, y2=y + 1.0, color=GRID, lw=0.5)]
    y += 1.15
els.append(T(0.5, 5.45, 12.33, 1.3, [
    {"text": "What success looks like", "size": 12, "bold": True},
    {"text": "By end-2028: 14–33% of accounts on Pro (base 25%, +$2.2M ARR), mobile-driven churn down by half (+$1.1M ARR kept a year), company gross margin ≥76%, and NRR at ~107% in the base case (104% in the low case, against a 105% target).", "size": 11.5, "space_before": 4}],
    fill=LGRAY, valign="middle"))
D.add(els, "decisions")

# =========================== 17. Appendix calcs ===========================
els = chrome("Appendix A: every figure in this deck comes from the briefing pack through the calculations below",
             SRC + "All values annual unless stated. Rounded.", title_size=20)
rows = [["Item", "Calculation", "Result"],
        ["Current ARR / COGS", "9,800 × 6.2 × $79 × 12; COGS = 22% of ARR", "$57.6M / $12.7M"],
        ["ARR per average account", "6.2 × $79 × 12", "$5,878"],
        ["Add-on ARR (CPO / paywall / low)", "9,800 × {46%, 14%, 7%} × $149 × 12", "$8.06M / $2.45M / $1.23M"],
        ["Add-on inference (base 10%)", "980 accounts × 6,800 × $0.009 × 12", "$0.72M"],
        ["Pro ARR (14% / 25% / 33%)", "9,800 × share × 6.2 × $12 × 12", "$1.23M / $2.19M / $2.89M"],
        ["Pro inference (base)", "2,450 × 6.2 × 444 × $0.009 × 12; cap: 500 requests/seat", "$0.73M (cap: ≤$0.82M)"],
        ["Company margin, Pro base", "1 − (12.67 + 0.73 + 0.60) ÷ (57.6 + 2.19)", "76.6%"],
        ["Free in Core: cost", "9,800 × {3,600, 1,900} × $0.009 × 12 + $0.6M", "$4.41M / $2.61M → 70.3% / 73.5%"],
        ["ARR lost to mobile / AI churn", "{27%, 6%} × 14% × $57.6M", "$2.18M / $0.48M"],
        ["Win-rate recovery ceiling", "(44% − 37%) × 1,560 × $5,878", "$0.64M"],
        ["Sales-memo claim", "1/3 × (63% × 1,560) × $5,878; implied win rate (577+328)/1,560", "$1.93M; 58%"],
        ["Engineering cost", "14 × 0.5 year × $210,000", "$1.47M"],
        ["Run-cost break-even", "$0.6M ÷ (($12 − $4.00) × 12) = 6,250 seats ÷ 6.2", "≈1,010 accounts (10%)"],
        ["NRR points", "ARR effect ÷ $57.6M (Pro +3.8; mobile +1.9; AI churn +0.4)", "Base 107.1%"]]
els.append(dict(t="table", x=0.5, y=1.8, cols=[3.0, 6.13, 3.2], rows=rows, size=10, hsize=10.5, minh=0.3, aligns=["l", "l", "r"], hfill=INK2, zebra="f7f7f5", maxy=6.9))
D.add(els, "appendix_calc")

# =========================== 18. Appendix assumptions ===========================
els = chrome("Appendix B: the answer rests on a few stated assumptions; data caveats and the choices we made in place of open questions are listed here",
             SRC + "No-one was available for questions during the work. Each choice below is the option we recommend; the executive team may override any of them.", title_size=20)
cols3 = [
    ("Key assumptions", [
        "Add-on adoption 7–14% (half to full paywall rate); base 10%.",
        "Pro adoption 14–33% (paywall rate to the 2023 tier precedent); base 25%.",
        "Pro use = beta mean 444 requests per seat; heavy case 6,800 per account.",
        "Platform cost of $0.6M is a cost of revenue.",
        "Churned accounts are average size.",
        "Rewrite removes 50% of mobile-driven churn (25–75%); the pack has no estimate.",
        "AI explains 50% of the win-rate drop (0–100%); Copilot avoids 50% of AI churn."]),
    ("Data caveats", [
        "Table 2 implies the top 10% of accounts generate ~40% of requests (14,500 × 10% ÷ 3,600); the pack states 58%.",
        "1,190 churn responses vs 14% × 9,800 = 1,372 churned accounts; we used rates, not counts.",
        "Beta results are volunteer-only; hours saved are self-reported.",
        "2023 tier take-up (33%) was for a different offer.",
        "Win-rate data cover only one quarter after Routewise launched AI."]),
    ("Choices made in place of questions", [
        "Format: 16:9 PowerPoint with native, editable charts.",
        "Read the engineering constraint as a straight swap: whichever goes first delays the other by two quarters. Rewrite keeps the 14 engineers in H1 2027; Copilot builds in H2.",
        "Pro = Core + Copilot; no other features priced in.",
        "NRR measured on the existing base; new-logo ARR excluded.",
        "Allowance (500/seat) and packs ($20 per 1,000) are proposals for the pilot to test.",
        "Base cases use midpoints rather than the CPO or Sales figures."])]
x = 0.5
for h, items in cols3:
    els += box_head(x, 1.8, 3.95, h)
    els.append(T(x, 2.25, 3.95, 4.6, B(items, size=11.5, sb=6)))
    x += 4.19
D.add(els, "appendix_assume")

D.build(OUT, PREV)
for w in D.warnings: print("WARN", w)
print("slides", len(D.specs))
