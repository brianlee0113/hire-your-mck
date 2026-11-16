import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from kit import *

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "deliverable")
PREV = os.path.join(ROOT, "build", "preview")
os.makedirs(PREV, exist_ok=True)

D = Deck()
L, R = 0.6, 12.733          # content left/right edges
CW = R - L
SRC = "Source: Palisade briefing pack (2026), synthetic benchmark data."
TOTAL_MAIN = 12


def chrome(sl, tag, title, source=SRC, page=True):
    sl.text(L, 0.38, 8, 0.25, tag.upper(), size=10, bold=True, color=BLUE, name="tag")
    sl.text(L, 0.62, CW, 0.95, title, size=22, bold=True, color=INK, line_spacing=0.95, name="title")
    sl.line(L, 1.62, R, 1.62, RULE, 0.75)
    if source:
        sl.text(L, 6.98, 10.6, 0.3, source, size=9, color=MUTED, name="source")
    if page:
        sl.text(R - 0.6, 6.98, 0.6, 0.3, str(sl.num), size=9, color=MUTED, align="right", name="page")


def legend(sl, x, y, items, size=10):
    for (label, col) in items:
        sl.rect(x, y + 0.03, 0.14, 0.14, col)
        sl.text(x + 0.2, y, 2.6, 0.22, label, size=size, color=SEC, name="legend")
        x += 0.32 + font(size).getlength(label) / 72


def panel(sl, x, y, w, h, head, body, size=12, head_color=INK, fill=PANEL):
    sl.rect(x, y, w, h, fill)
    sl.text(x + 0.2, y + 0.18, w - 0.4, 0.5, head, size=12.5, bold=True, color=head_color, name="panel head")
    hh = sl.last_text_height
    sl.text(x + 0.2, y + 0.18 + hh + 0.1, w - 0.4, h - hh - 0.42, body, size=size, color=INK,
            space_after=6, name=f"panel body {head[:20]}")


# =====================================================================
# 1. Title
s = D.new()
s.rect(0, 0, W_IN, H_IN, "F7F6F2")
s.rect(L, 1.9, 0.08, 2.35, BLUE)
s.text(L + 0.35, 1.85, 11.2, 0.3, "PALISADE DOCS · 2027 PRICING DECISION", size=12, bold=True, color=BLUE)
s.text(L + 0.35, 2.3, 11.4, 1.6,
       "Raise prices in 2027 where we have pricing power, and hold SMB until we have tested it",
       size=34, bold=True, color=INK, line_spacing=0.95, name="cover title")
s.text(L + 0.35, 3.75, 11.2, 0.5,
       "Recommendation to the CEO and leadership team for the December 2026 pricing decision",
       size=16, color=SEC)
s.text(L + 0.35, 6.3, 11.5, 0.6,
       ["Prepared November 2026 from the internal briefing pack only. No outside research was used.",
        "All company figures are synthetic benchmark data. ARR figures are $M; churn is monthly logo churn unless stated."],
       size=10, color=MUTED, space_after=2)

# =====================================================================
# 2. Executive summary
s = D.new()
chrome(s, "Executive summary",
       "Yes, raise prices in 2027, but only for mid-market and enterprise. Hold SMB, test it, and fix the promotion cohort with onboarding, not price")
colw = 5.95
s.text(L, 1.85, colw, 0.3, "WHAT THE EVIDENCE SAYS", size=10.5, bold=True, color=SEC)
s.text(L, 2.2, colw, 4.6, [
    {"text": "**Churn is rising in one place.** About 90% of the SMB rise (2.0% → 3.1% a month) comes from the 2,100 customers who joined on the 2025 half-price promotion. Other SMB customers moved from 2.0% to 2.1%.", "bullet": True},
    {"text": "**The promotion cohort is an onboarding problem.** Only 41% got started properly (72% for other cohorts), and most leavers went within two months of the discount ending.", "bullet": True},
    {"text": "**Mid-market and enterprise can take an increase.** Their NRR is 112% and 118%, a +10% list test had no significant effect on conversion, and Inkwell is absent above 200 seats.", "bullet": True},
    {"text": "**SMB is the open question.** Inkwell sells at $9 against our $15. A 12% SMB increase adds about $1.2M if customers react as they did in 2023, and nothing if they react twice as strongly.", "bullet": True},
    {"text": "**The CFO's $10.3M is $7.6M before any churn response,** because only part of the ARR renews in 2027 and enterprise increases are capped.", "bullet": True},
], size=12, space_after=7, name="exec left")
xr = L + colw + 0.35
wr = R - xr
s.rect(xr, 1.85, wr, 4.95, PANEL)
s.text(xr + 0.25, 2.02, wr - 0.5, 0.3, "WHAT WE RECOMMEND", size=10.5, bold=True, color=BLUE)
s.text(xr + 0.25, 2.37, wr - 0.5, 2.6, [
    {"text": "**Mid-market:** +10% list price at renewal (the tested level).", "bullet": True},
    {"text": "**Enterprise:** up to the 7% cap where contracts cap increases; up to +10% elsewhere.", "bullet": True},
    {"text": "**SMB:** hold $15 in H1 and split-test +8% in Q1. Extend it to H2 renewals only if churn holds.", "bullet": True},
    {"text": "**Promotion cohort:** no increase. Run an onboarding programme aimed at returning it to normal SMB churn.", "bullet": True},
], size=12, space_after=6, name="exec right")
y0 = 4.72
s.line(xr + 0.25, y0, R - 0.25, y0, RULE)
stats = [("$4.3M", "ARR from price,\nplus up to $0.7M if the SMB test passes"),
         ("~114%", "overall NRR\n(target above 100%)"),
         ("+14.2%", "growth from existing customers. About $0.6M of new-customer ARR reaches 15%")]
sw = (wr - 0.5) / 3
for i, (big, small) in enumerate(stats):
    sx = xr + 0.25 + i * sw
    s.text(sx, y0 + 0.15, sw - 0.15, 0.5, big, size=22, bold=True, color=BLUE_D, name="stat")
    s.text(sx, y0 + 0.62, sw - 0.15, 0.85, small.split("\n"), size=10, color=SEC, space_after=0, name="stat label")
s.text(xr + 0.25, 6.12, wr - 0.5, 0.6,
       "**Trade-off:** on paper this is $0.8–2.0M less 2027 ARR than the CFO's plan. In return, we avoid betting the 5,900-customer SMB base on a reaction we have not measured.",
       size=10.5, color=INK, name="tradeoff")

# =====================================================================
# 3. Where churn is rising
s = D.new()
chrome(s, "Diagnosis · where churn is rising",
       "Churn is rising almost entirely in SMB, and within SMB almost entirely among customers who joined on the 2025 promotion")
s.text(L, 1.82, 7.5, 0.3, "Monthly logo churn by group, %, H1 2025 vs H1 2026", size=12, bold=True, color=INK)
legend(s, L, 2.17, [("H1 2025", GRAY), ("H1 2026", BLUE)])
rows = [("Enterprise", "150 customers", 0.2, 0.2),
        ("Mid-market", "1,350 customers", 0.6, 0.8),
        ("SMB: regular customers", "3,800 customers", 2.0, 2.1),
        ("SMB: 2025 promotion cohort", "2,100 customers, joined Feb–Aug 2025", None, 4.9),
        ("SMB total", "5,900 customers", 2.0, 3.1)]
lab_w = 2.45
bx = L + lab_w + 0.1
scale = 0.92  # in per pct-point
yy = 2.62
bh = 0.24
for (name, sub, a, b) in rows:
    is_total = name == "SMB total"
    if is_total:
        s.line(L, yy - 0.1, L + 7.55, yy - 0.1, RULE)
    s.text(L, yy, lab_w, 0.26, name, size=11.5, bold=True, color=INK, name="row label")
    s.text(L, yy + 0.25, lab_w, 0.4, sub, size=9.5, color=MUTED, name="row sub")
    if a is not None:
        s.rect(bx, yy, max(a * scale, 0.02), bh, GRAY)
        s.text(bx + a * scale + 0.07, yy + 0.01, 0.7, 0.24, f"{a:.1f}", size=10.5, color=SEC)
    else:
        s.text(bx + 0.02, yy + 0.02, 3.5, 0.24, "not yet a full cohort", size=9.5, color=MUTED)
    s.rect(bx, yy + bh + 0.04, b * scale, bh, BLUE)
    s.text(bx + b * scale + 0.07, yy + bh + 0.05, 0.9, 0.24, f"{b:.1f}" + ("*" if a is None else ""), size=10.5, bold=True, color=INK)
    yy += 0.78
s.line(bx, 2.5, bx, yy - 0.15, SEC, 0.75)
s.text(L, yy - 0.05, 7.6, 0.5,
       "* Implied, not reported: (5,900 × 3.1% − 3,800 × 2.1%) ÷ 2,100 ≈ 4.9%, using mid-2026 customer counts as weights.",
       size=9, color=MUTED, name="footnote")
panel(s, 8.55, 1.85, R - 8.55, 4.95, "What this means", [
    {"text": "If the promotion cohort churned like other SMB customers, **SMB churn would be 2.1%, not 3.1%.** About 1.0 of the 1.1-point rise is the cohort.", "bullet": True},
    {"text": "**Regular SMB customers have barely moved** (2.0% → 2.1%), even after Inkwell's launch in October 2025.", "bullet": True},
    {"text": "**Mid-market is up from a low base** (0.6% → 0.8%). Watch it, but it is not the driver. Enterprise is flat.", "bullet": True},
    {"text": "The board dashboard's \"1.4% → 2.3%\" does not define its measure and cannot be reconciled with these figures (appendix). **Decide on segment logo churn.**", "bullet": True},
], size=11.5)

# =====================================================================
# 4. Promotion cohort / price complaints
s = D.new()
chrome(s, "Diagnosis · why they leave",
       "The rise in price complaints comes from customers who left when their discount ended. Regular SMB customers cite price no more than in 2025")
s.text(L, 1.82, 6.6, 0.5, "Exit-survey churners whose main reason was \"price / found a cheaper option\", %", size=12, bold=True)
bars = [("All SMB churners, H1 2025", 19, GRAY),
        ("All SMB churners, H1 2026", 34, GRAY),
        ("Promotion-cohort churners, H1 2026", 52, ORANGE),
        ("Regular SMB churners, H1 2026", 18, BLUE)]
lab_w = 2.55; bx = L + lab_w + 0.1; sc = 3.3 / 52
yy = 2.45
for (name, v, col) in bars:
    s.text(L, yy + 0.04, lab_w, 0.5, name, size=11, color=INK, name="bar label")
    s.rect(bx, yy, v * sc, 0.38, col)
    s.text(bx + v * sc + 0.08, yy + 0.07, 0.6, 0.3, f"{v}%", size=12, bold=True)
    yy += 0.62
s.line(bx, 2.35, bx, yy - 0.12, SEC)
s.text(L, yy + 0.05, 6.5, 0.75, [
    "The blended rise (19% → 34%) is a mix effect. The promotion cohort's share of churners grew, and **52%** of those churners cite price. Regular SMB churners are flat at **18%**.",
], size=11, color=INK, name="bar note")
# right: activation stat tiles
xr = 7.75; wr = R - xr
s.text(xr, 1.82, wr, 0.3, "The cohort never got going", size=12, bold=True)
tiles = [("41%", "of promotion-cohort customers sent five or more documents in their first month", ORANGE),
         ("72%", "of customers in other cohorts did the same", BLUE),
         ("~3×", "higher churn for SMB customers who send fewer than five documents in month one", INK)]
ty = 2.3
for big, small, col in tiles:
    s.rect(xr, ty, wr, 0.95, PANEL)
    s.text(xr + 0.2, ty + 0.12, 1.3, 0.7, big, size=26, bold=True, color=col, anchor="middle", name="tile big")
    s.text(xr + 1.55, ty + 0.12, wr - 1.75, 0.7, small, size=11, color=INK, anchor="middle", name="tile small")
    ty += 1.07
s.text(xr, ty + 0.08, wr, 1.2, [
    "Most cohort leavers went **within two months of the 50% discount ending**. For them, the \"price\" answer is the jump back to full price, not our list level.",
    "**So what:** the CFO is right that this is mostly an onboarding problem. It also means this cohort will not absorb a further increase in 2027.",
], size=11, space_after=6, name="right note")

# =====================================================================
# 5. SMB exposure
s = D.new()
chrome(s, "Options · SMB",
       "SMB is now exposed on price. A 12% increase pays off only if customers react less than twice as strongly as they did in 2023, and we cannot yet tell")
# Left: price ladder
s.text(L, 1.82, 5.4, 0.3, "List price per user per month, $", size=12, bold=True)
ladder = [("Inkwell Starter", 9, "launched Oct 2025", GRAY),
          ("Palisade SMB", 15, "today", BLUE),
          ("Palisade SMB +12%", 16.8, "CFO proposal", BLUE_L),
          ("Inkwell Pro", 24, "", GRAY),
          ("Palisade Business", 29, "", BLUE)]
lab_w = 1.85; bx = L + lab_w + 0.1; sc = 2.6 / 29
yy = 2.3
for (n, v, sub, col) in ladder:
    s.text(L, yy + 0.02, lab_w, 0.25, n, size=11, color=INK, name="ladder")
    s.rect(bx, yy, v * sc, 0.3, col, line=BLUE if col == BLUE_L else None)
    s.text(bx + v * sc + 0.08, yy + 0.03, 1.9, 0.28,
           [{"runs": [(f"${v:g}".replace("16.8", "16.80"), {"bold": True}), (("  " + sub) if sub else "", {"color": MUTED, "size": 9.5})]}],
           size=11, name="ladder val")
    yy += 0.46
s.line(bx, 2.22, bx, yy - 0.1, SEC)
s.text(L, yy + 0.1, 5.3, 2.0, [
    {"text": "**Win rate vs Inkwell in SMB: 51% → 38%** (H1 2025 → H1 2026).", "bullet": True},
    {"text": "**2023 precedent:** +8% at renewal lifted SMB churn from 1.8% to 2.3% for six months, then it settled at 1.9%. That was before Inkwell existed.", "bullet": True},
    {"text": "**Pointing the other way:** regular SMB churners citing price are flat (18% vs 19%).", "bullet": True},
], size=11, space_after=5, name="smb bullets")
# Right: net effect by reaction strength
xr = 6.55; wr = R - xr
s.text(xr, 1.82, wr, 0.5, "Net 2027 ARR effect of +12% on all SMB, by strength of churn reaction, $M", size=12, bold=True, name="chart title")
cases = [("No reaction", 2.52), ("As in 2023", 1.25), ("2× the 2023 reaction", -0.02), ("3× the 2023 reaction", -1.29)]
zero_y = 4.2; vs = 0.62  # in per $M
cw = wr / 4
s.line(xr, zero_y, R, zero_y, SEC, 0.75)
for i, (n, v) in enumerate(cases):
    cx = xr + i * cw + cw * 0.22
    bw = cw * 0.56
    col = BLUE if v > 0.05 else (ORANGE if v < -0.05 else GRAY)
    if abs(v) < 0.05:
        s.rect(cx, zero_y - 0.02, bw, 0.04, GRAY)
        s.text(xr + i * cw, zero_y - 0.38, cw, 0.3, "≈ $0.0M", size=12, bold=True, align="center")
    elif v > 0:
        s.rect(cx, zero_y - v * vs, bw, v * vs, col)
        s.text(xr + i * cw, zero_y - v * vs - 0.32, cw, 0.3, f"+${v:.1f}M", size=12, bold=True, align="center")
    else:
        s.rect(cx, zero_y, bw, -v * vs, col)
        s.text(xr + i * cw, zero_y - v * vs + 0.05, cw, 0.3, f"−${-v:.1f}M", size=12, bold=True, align="center")
    s.text(xr + i * cw + 0.05, 5.58, cw - 0.1, 0.45, n, size=10.5, color=SEC, align="center", name="case label")
s.text(xr, 6.05, wr, 0.85, [
    "Gross gain is 12% × $21.0M = $2.5M. The 2023 response, scaled to 12%, means +0.75 pts of churn for six months and +0.15 pts after, losing about 5.4% of SMB customers. **Break-even is about twice the 2023 reaction.** The win-rate drop makes that plausible but not proven.",
], size=10, color=SEC, name="smb method")

# =====================================================================
# 6. MM + Enterprise pricing power
s = D.new()
chrome(s, "Options · mid-market and enterprise",
       "Mid-market and enterprise show pricing power. A 10% increase breaks even only if mid-market churn roughly doubles")
cols = [("Retention is strong", ["Net revenue retention: **112%** mid-market, **118%** enterprise", "Monthly logo churn: **0.8%** mid-market, **0.2%** enterprise"]),
        ("Price was tested", ["2024: +10% list price for new mid-market sign-ups", "Conversion **23.1% vs 23.6%** for the control group, not statistically significant"]),
        ("Competition is absent", ["Inkwell not seen in mid-market or enterprise deals **above 200 seats**", "Customers stay for **integrations and audit trail** (advisory board, 2026)"])]
cw3 = (CW - 0.5) / 3
for i, (h, items) in enumerate(cols):
    x = L + i * (cw3 + 0.25)
    s.rect(x, 1.85, cw3, 1.9, PANEL)
    s.text(x + 0.2, 2.0, cw3 - 0.4, 0.3, h, size=12.5, bold=True, color=BLUE_D)
    s.text(x + 0.2, 2.4, cw3 - 0.4, 1.3, [{"text": t, "bullet": True} for t in items], size=11, space_after=5, name="mm col")
# Breakeven scale
s.text(L, 4.0, 7.2, 0.3, "Mid-market monthly logo churn: where we are vs where +10% stops paying, %", size=12, bold=True)
sx0 = L + 0.1; sxs = 7.0 / 2.0   # in per pct
ay = 4.95
s.line(sx0, ay, sx0 + 2.0 * sxs, ay, RULE, 6)
marks = [(0.6, "H1 2025", GRAY, 0), (0.8, "H1 2026", BLUE, 0), (1.2, "Proposed tripwire", ORANGE, 0), (1.58, "Break-even", INK, 0)]
for v, lab, col, _ in marks:
    x = sx0 + v * sxs
    s.oval(x - 0.09, ay - 0.09, 0.18, 0.18, col)
    s.text(x - 0.8, ay - 0.5, 1.6, 0.3, f"{v:.1f}%".replace("1.58", "~1.6") if v != 1.58 else "~1.6%", size=12, bold=True, align="center")
    s.text(x - 0.8, ay + 0.15, 1.6, 0.3, lab, size=10, color=SEC, align="center")
for v in [0, 0.5, 1.0, 1.5, 2.0]:
    s.text(sx0 + v * sxs - 0.3, ay + 0.48, 0.6, 0.2, f"{v:.1f}", size=9, color=MUTED, align="center")
s.text(L, 5.85, 7.3, 1.0,
       "Break-even: +10% on renewing ARR is lost if an extra 9.1% of renewing customers leave within the year (0.10 ÷ 1.10). That is about +0.8 pts a month on top of today's 0.8%.",
       size=10, color=SEC, name="mm method")
panel(s, 8.3, 4.0, R - 8.3, 2.8, "Why +10%, not the CFO's 12%", [
    {"text": "10% is the level we tested. 12% on existing customers is untested.", "bullet": True},
    {"text": "The test covered new sign-ups. **Renewing customers may react differently**, so watch Q1 renewals.", "bullet": True},
    {"text": "Mid-market churn is up 0.2 pts, and accounts of 200 seats or fewer may meet Inkwell.", "bullet": True},
    {"text": "Cost of the caution: **$0.7M** of 2027 ARR.", "bullet": True},
], size=11)

# =====================================================================
# 7. CFO waterfall
s = D.new()
chrome(s, "Options · the CFO's plan",
       "The CFO's $10.3M assumes all ARR reprices in 2027. The realistic figure is $7.6M before any churn response, and $5.0–6.3M after it")
s.text(L, 1.82, 9, 0.3, "ARR added by +12% on every plan at renewal from January 2027, $M", size=12, bold=True)
steps = [("CFO headline\n12% × $86.0M", 10.32, "total"),
         ("Mid-market ARR\nnot renewing in 2027\n(15%)", -0.74, "step"),
         ("Enterprise ARR\nnot renewing in 2027\n(60%)", -1.73, "step"),
         ("Enterprise caps:\n7% max on 60%\nof contracts", -0.29, "step"),
         ("Before churn\nresponse", 7.57, "total"),
         ("SMB churn response\nas in 2023", -1.27, "step"),
         ("Realistic,\n2023-like\nreaction", 6.30, "total"),
         ("Extra loss if\nreaction is 2×", -1.27, "step"),
         ("Realistic,\n2× reaction", 5.03, "total")]
base_y = 5.45; vs = 0.27
n = len(steps); cw9 = CW / n
run = 0
s.line(L, base_y, R, base_y, SEC)
for i, (lab, v, kind) in enumerate(steps):
    x = L + i * cw9 + cw9 * 0.18; bw = cw9 * 0.64
    if kind == "total":
        top, bot = v, 0; run = v
        col = BLUE if i in (0, 4) else BLUE_D
        if i == 0: col = GRAY
        lbl = f"${v:.1f}M"
    else:
        top, bot = run, run + v; run = run + v
        col = ORANGE
        lbl = f"−{-v:.1f}"
    y1 = base_y - top * vs; h = (top - bot) * vs
    s.rect(x, y1, bw, h, col)
    s.text(L + i * cw9, y1 - 0.3, cw9, 0.28, lbl, size=12, bold=(kind == "total"), align="center", color=INK)
    if i < n - 1:
        ny = base_y - run * vs
        s.line(x + bw, ny, x + cw9, ny, MUTED, 0.5)
    s.text(L + i * cw9 + 0.04, base_y + 0.1, cw9 - 0.08, 0.8, lab.split("\n"), size=9.5, color=SEC, align="center", space_after=0, name="wf label")
s.text(L, 6.42, CW, 0.5,
       "Assumes 2027 enterprise renewals carry the same 60% capped share as the whole enterprise book, and 85% of mid-market ARR renews in 2027 (per the pack). The SMB response uses the 2023 precedent scaled to 12%. Mid-market and enterprise reactions are not modelled.",
       size=9.5, color=SEC, name="wf note")

# =====================================================================
# 8. Recommended plan
s = D.new()
chrome(s, "Recommendation · the 2027 plan",
       "Recommended plan: raise mid-market and enterprise prices at renewal, hold the SMB list price while we test it, and onboard the promotion cohort")
hdr_y = 1.85
cx = [L, L + 2.15, L + 6.25, L + 7.85]
cwid = [2.0, 3.95, 1.45, R - (L + 7.85)]
heads = ["Segment", "2027 action", "2027 ARR effect", "Why"]
for x, w, h in zip(cx, cwid, heads):
    s.text(x, hdr_y, w, 0.3, h.upper(), size=10, bold=True, color=SEC)
s.line(L, hdr_y + 0.32, R, hdr_y + 0.32, INK, 1)
plan = [
    ("Mid-market", "1,350 customers · $41.0M",
     "**+10% list price at renewal** from January. 85% of mid-market ARR ($34.9M) renews in 2027.",
     "+$3.5M", BLUE_D,
     "NRR 112%. The +10% test showed no significant effect. Break-even needs churn to roughly double."),
    ("Enterprise", "150 customers · $24.0M",
     "**Up to the 7% cap** on capped contracts; **up to +10%** on uncapped renewals, under each contract's terms. 40% renews in 2027.",
     "+$0.8M", BLUE_D,
     "NRR 118%, churn 0.2%. Customers stay for integrations and audit trail."),
    ("SMB: regular", "3,800 customers · $16.6M",
     "**Hold $15 in H1.** In Q1, split-test +8% on half of renewals. If the test passes, apply +8% to H2 renewals.",
     "$0 in plan;\nup to +$0.7M", SEC,
     "Inkwell at $9; win rate down to 38%. Whether customers react like 2023 or twice as strongly decides whether 12% pays."),
    ("SMB: promo cohort", "2,100 customers · $4.4M",
     "**No increase in 2027.** Run an onboarding programme for customers sending fewer than five documents a month.",
     "Up to ~$1.0M\nretained (upside)", SEC,
     "41% got started properly. Leavers went when the discount ended. Price would accelerate it."),
]
yy = hdr_y + 0.45
rh = 0.93
for (seg, sub, act, eff, ecol, why) in plan:
    s.text(cx[0], yy, cwid[0], 0.3, seg, size=12, bold=True)
    s.text(cx[0], yy + 0.3, cwid[0], 0.5, sub, size=9.5, color=MUTED, name="seg sub")
    s.text(cx[1], yy, cwid[1], rh - 0.1, act, size=11, name="action")
    s.text(cx[2], yy, cwid[2], rh - 0.1, eff.split("\n"), size=12 if "\n" not in eff else 11, bold=True, color=ecol, space_after=0, name="eff")
    s.text(cx[3], yy, cwid[3], rh - 0.1, why, size=10.5, color=SEC, name="why")
    yy += rh
    s.line(L, yy - 0.1, R, yy - 0.1, RULE)
s.rect(L, yy + 0.05, CW, 0.62, PANEL)
s.text(L + 0.2, yy + 0.1, CW - 0.4, 0.52,
       [{"runs": [("Total: +$4.3M of 2027 ARR from price in the plan, ", {"bold": True}),
                  ("with up to +$1.7M of upside if the SMB test passes and onboarding works. We also recommend not repeating untargeted 50%-off promotions for new self-serve customers.", {})]}],
       size=11.5, anchor="middle", name="total")

# =====================================================================
# 9. Bridge & plan comparison
s = D.new()
chrome(s, "Recommendation · against the objectives",
       "The plan keeps NRR near 114% and grows ARR 14.2% from existing customers. About $0.6M of new-customer ARR closes the gap to the 15% target")
s.text(L, 1.82, 6.9, 0.3, "2027 ARR bridge under the recommended plan, $M", size=12, bold=True)
br = [("Start of\n2027", 86.0, "total"), ("Existing customers\nat trailing NRR", 7.98, "step"),
      ("Mid-market\n+10%", 3.49, "step"), ("Enterprise\nto cap / +10%", 0.79, "step"),
      ("Existing\ncustomers,\nend 2027", 98.252, "total"), ("New-customer\nARR needed", 0.648, "gap"),
      ("15% target", 98.9, "target")]
cbx = L; cbw = 6.9; nb = len(br); bwc = cbw / nb
floor = 80.0; top_y = 2.55; base_y = 5.55; vsc = (base_y - top_y) / (100 - floor)
s.line(cbx, base_y, cbx + cbw, base_y, SEC)
runv = 0
for i, (lab, v, kind) in enumerate(br):
    x = cbx + i * bwc + bwc * 0.17; bw = bwc * 0.66
    if kind in ("total", "target"):
        t, b = v, floor; runv = v
        col = GRAY if i == 0 else (BLUE_D if kind == "total" else None)
        lbl = f"{v:.1f}"
    else:
        t, b = runv + v, runv; runv += v
        col = BLUE if kind == "step" else None
        lbl = f"+{v:.1f}"
    y1 = base_y - (t - floor) * vsc; h = (t - b) * vsc
    if kind == "gap":
        s.rect(x, y1, bw, max(h, 0.04), None, line=ORANGE, line_w=1.25)
    elif kind == "target":
        s.rect(x, y1, bw, h, None, line=INK, line_w=1.0)
    else:
        s.rect(x, y1, bw, h, col)
    s.text(cbx + i * bwc - 0.05, y1 - 0.3, bwc + 0.1, 0.28, lbl, size=11.5, bold=kind != "step", align="center",
           color=ORANGE if kind == "gap" else INK)
    if i < nb - 1:
        ny = base_y - (runv - floor) * vsc
        s.line(x + bw, ny, x + bwc + bwc * 0.17, ny, MUTED, 0.5)
    s.text(cbx + i * bwc, base_y + 0.08, bwc, 0.7, lab.split("\n"), size=9, color=SEC, align="center", space_after=0, name="br label")
s.text(cbx, 6.32, cbw, 0.6,
       "Axis starts at $80M. Trailing NRR: SMB 94%, mid-market 112%, enterprise 118%. If 2027 NRR runs 3 points below trailing, the new-customer ARR needed rises to about $3.2M.",
       size=9, color=SEC, name="bridge note")
# comparison table
tx = 7.95; tw = R - tx
s.text(tx, 1.82, tw, 0.3, "Recommended plan vs CFO plan", size=12, bold=True)
c1 = tx + 1.75; c2 = tx + 3.3
s.text(c1, 2.22, 1.5, 0.3, "RECOMMENDED", size=9.5, bold=True, color=BLUE_D)
s.text(c2, 2.22, R - c2, 0.3, "CFO: +12% ALL", size=9.5, bold=True, color=SEC)
s.line(tx, 2.5, R, 2.5, INK, 1)
rows = [("ARR from price", "$4.3M\n(+$0.7M option)", "$5.0–6.3M\n(after SMB response)"),
        ("End-2027 ARR, existing customers", "$98.3M", "$99.0–100.3M"),
        ("Overall NRR", "~114%", "~115–117%"),
        ("SMB customers repriced", "None until tested", "All 5,900, incl. the promo cohort"),
        ("Mid-market increase", "10%: tested level", "12%: untested on renewals"),
        ("Can we read churn in 2027?", "Yes: clean test and control", "No: price mixed with promo exits")]
ry = 2.6
for (k, a, b) in rows:
    s.text(tx, ry, 1.65, 0.6, k, size=10.5, bold=True, name="cmp key")
    s.text(c1, ry, 1.5, 0.6, a.split("\n"), size=10.5, space_after=0, name="cmp a")
    s.text(c2, ry, R - c2, 0.6, b.split("\n"), size=10.5, color=SEC, space_after=0, name="cmp b")
    ry += 0.58
    s.line(tx, ry - 0.08, R, ry - 0.08, RULE)
s.text(tx, ry + 0.02, tw, 0.75,
       "The CFO's plan is worth $0.8–2.0M more on paper. Both plans clear the NRR objective. The difference is which risk we carry into 2028.",
       size=10.5, bold=True, color=INK, name="cmp verdict")

# =====================================================================
# 10. Onboarding realism
s = D.new()
chrome(s, "Recommendation · onboarding",
       "Onboarding can bring SMB churn back to about 2.1%, not halve it. Plan around the promotion cohort, not the headline claim")
s.text(L, 1.82, 7.0, 0.3, "SMB monthly logo churn, %", size=12, bold=True)
pts = [("2023, before +8%", 1.8, GRAY, ""), ("2023, settled after +8%", 1.9, GRAY, ""),
       ("H1 2025", 2.0, GRAY, ""), ("H1 2026", 3.1, BLUE_D, ""),
       ("Cohort fixed: churns like regular SMB", 2.1, BLUE, "realistic target"),
       ("\"Halve SMB churn\" (CS claim)", 1.55, ORANGE, "below any level since 2023")]
lab_w = 2.9; bx = L + lab_w + 0.1; sc = 1.15
yy = 2.3
for i, (n, v, col, note) in enumerate(pts):
    if i == 4:
        s.line(L, yy - 0.1, L + 7.0, yy - 0.1, RULE)
        s.text(L, yy - 0.05, 3, 0.22, "SCENARIOS FOR 2027", size=9, bold=True, color=MUTED)
        yy += 0.22
    s.text(L, yy + 0.03, lab_w, 0.3, n, size=11, name="onb label")
    s.rect(bx, yy, v * sc, 0.32, col)
    s.text(bx + v * sc + 0.08, yy + 0.04, 2.8, 0.3,
           [{"runs": [(f"{v:.2f}%" if v == 1.55 else f"{v:.1f}%", {"bold": True}), (("  " + note) if note else "", {"color": MUTED, "size": 9.5})]}],
           size=11, name="onb val")
    yy += 0.5
s.line(bx, 2.22, bx, yy - 0.1, SEC)
s.text(L, yy + 0.1, 7.1, 0.8,
       "Halving 3.1% means 1.55%. That would need regular SMB customers to fall well below the 1.8–2.0% range SMB has run at since 2023, not just to fix the promotion cohort.",
       size=10.5, color=SEC, name="onb note")
panel(s, 8.3, 1.85, R - 8.3, 4.95, "What onboarding is worth", [
    {"text": "The cohort is **$4.4M of ARR**. At ~4.9% a month it loses about 45% of that over 12 months; at 2.1%, about 22%.", "bullet": True},
    {"text": "Closing that gap retains **up to ~$1.0M of ARR**. That is a real prize, but not a substitute for price.", "bullet": True},
    {"text": "**Caveat:** much of the H1 2026 churn was the cliff when the discount ended. The survivors may already churn less, so the gain could be smaller.", "bullet": True},
    {"text": "**Target:** cohort churn converging on the regular SMB rate (~2.1%) by mid-2027, tracked monthly.", "bullet": True},
], size=11.5)

# =====================================================================
# 11. Guardrails
s = D.new()
chrome(s, "Recommendation · guardrails",
       "Agreed tripwires let us stop or extend each 2027 increase on evidence, not opinion")
cxs = [L, L + 2.75, L + 6.35, L + 9.6]
cws = [2.6, 3.45, 3.1, R - (L + 9.6)]
for x, w, h in zip(cxs, cws, ["What we watch", "Tripwire", "Action", "Read-out"]):
    s.text(x, 1.85, w, 0.3, h.upper(), size=10, bold=True, color=SEC)
s.line(L, 2.17, R, 2.17, INK, 1)
g = [("Mid-market renewals at +10%", "Monthly churn of customers who renewed at the new price goes **above 1.2%** (0.8% today; break-even ~1.6%)",
      "Pause further increases. Review accounts of 200 seats or fewer first, since that is where Inkwell can compete", "Monthly from February; decision end of March"),
     ("SMB split test (+8%)", "Test group's churn exceeds control by **0.6 pts a month or more**. That reaction would wipe out the gain",
      "Below the line: +8% on H2 SMB renewals (up to +$0.7M). Above it: hold SMB through 2027", "End of Q1; H2 decision in April"),
     ("Promotion cohort", "Churn **not converging on ~2.1%** by mid-2027 despite the onboarding programme",
      "Stop extra onboarding spend and plan for the remaining cohort to churn", "Monthly; review in July"),
     ("SMB win rate vs Inkwell", "Falls **below 38%** (H1 2026 level)",
      "Revisit SMB packaging against Inkwell before any SMB increase", "Quarterly"),
     ("Board churn metric", "Undefined today: \"1.4% → 2.3%\" does not reconcile",
      "Report logo churn by segment, with the promotion cohort shown separately", "Before the December decision")]
yy = 2.3
for row in g:
    for j, (x, w) in enumerate(zip(cxs, cws)):
        s.text(x, yy, w - 0.15, 0.8, row[j], size=10.5 if j else 11, bold=(j == 0), color=INK if j < 3 else SEC, name=f"g{j}")
    yy += 0.8
    s.line(L, yy - 0.08, R, yy - 0.08, RULE)
s.text(L, yy + 0.02, CW, 0.5,
       "The SMB test should cover about half of regular SMB renewals. That is enough to detect a reaction large enough to cancel the gain (~0.6 pts a month), not a smaller one like 2023's (~0.3 pts). See appendix.",
       size=9.5, color=SEC, name="test note")

# =====================================================================
# 12. Decisions
s = D.new()
chrome(s, "Decisions for December",
       "Five decisions for the leadership team in December", source=None)
dec = [("Approve mid-market +10% and enterprise to-cap increases at renewal from January 2027",
        "Replaces the CFO's 12% on every plan. Worth +$4.3M of 2027 ARR."),
       ("Hold the SMB list price at $15 for H1 2027 and approve the Q1 split test",
        "Use the decision rule on the previous page to set H2 SMB pricing in April."),
       ("Fund an onboarding programme for the 2025 promotion cohort, with a realistic target",
        "Target: cohort churn converging on ~2.1% by mid-2027, not \"halve SMB churn\"."),
       ("Confirm the 2027 new-customer ARR plan covers at least $0.6M, ideally about $3M",
        "The pack has no new-business figures. This is the one input the 15% target still depends on."),
       ("Ask Finance to redefine the board churn metric before the board sees the pricing plan",
        "Logo churn by segment, with the promotion cohort shown separately.")]
yy = 1.9
for i, (a, b) in enumerate(dec, 1):
    s.oval(L, yy + 0.02, 0.42, 0.42, BLUE)
    s.text(L, yy + 0.02, 0.42, 0.42, str(i), size=14, bold=True, color=WHITE, align="center", anchor="middle")
    s.text(L + 0.65, yy, 8.0, 0.32, a, size=13, bold=True, name="dec a")
    s.text(L + 0.65, yy + 0.34, 8.0, 0.4, b, size=11, color=SEC, name="dec b")
    yy += 0.95
xr = 9.6; wr = R - xr
s.rect(xr, 1.85, wr, 4.85, PANEL)
s.text(xr + 0.2, 2.0, wr - 0.4, 0.3, "TIMELINE", size=10, bold=True, color=BLUE)
tl = [("Dec 2026", "Decision; define churn metric"), ("Jan 2027", "Mid-market and enterprise renewals at new prices; SMB test and onboarding start"),
      ("Mar 2027", "Q1 read-outs: mid-market tripwire, SMB test"), ("Apr 2027", "Decide H2 SMB pricing"),
      ("Jul 2027", "Promotion-cohort review")]
ty = 2.42
for d_, t in tl:
    s.text(xr + 0.2, ty, wr - 0.4, 0.25, d_, size=11, bold=True, color=INK)
    s.text(xr + 0.2, ty + 0.25, wr - 0.4, 0.6, t, size=10.5, color=SEC, name="tl")
    ty += 0.25 + s.last_text_height + 0.22

# =====================================================================
# Appendix A1: calculations
s = D.new()
chrome(s, "Appendix A · calculations", "How the main figures were calculated")
calc = [
    ("CFO headline", "12% × $86.0M = $10.3M. This assumes every dollar of ARR reprices in 2027 at the full 12%."),
    ("CFO before churn response", "SMB 12% × $21.0M = $2.52M; mid-market 12% × 85% × $41.0M = $4.18M; enterprise renewing $9.6M (40% of $24.0M): 60% capped at 7% = $0.40M, plus 40% at 12% = $0.46M. Total **$7.57M**."),
    ("SMB churn response", "2023: +8% gave +0.5 pts for six months, then +0.1 pts. Scaled linearly to 12%: +0.75 pts × 6 months + 0.15 pts × 6 months = 5.4% of customers lost, × $23.5M repriced ARR = **$1.27M** (×2 = $2.54M)."),
    ("Recommended price ARR", "Mid-market 10% × $34.85M = $3.49M. Enterprise: $5.76M capped at 7% = $0.40M, plus $3.84M at 10% = $0.38M. Total **$4.27M**."),
    ("SMB H2 option", "+8% on roughly half of regular SMB ARR (renewing in H2): 8% × 50% × $16.6M ≈ **$0.66M**. Regular SMB ARR = $21.0M − $4.4M cohort."),
    ("Existing-customer bridge", "$21.0M × 94% + $41.0M × 112% + $24.0M × 118% = $93.98M (+$7.98M), plus price $4.27M = **$98.25M** (+14.2%). 15% target = $98.9M, so the gap is $0.65M."),
    ("Break-evens", "Gain p is cancelled when the share of customers lost in the year reaches p ÷ (1 + p). Mid-market at 10%: 9.1% a year ≈ +0.8 pts a month. SMB at 8%: 7.4% ≈ +0.6 pts. SMB at 12%: 10.7%, about twice the 2023 response."),
    ("Promotion-cohort value", "12-month retention at 4.9% a month = 55%; at 2.1% = 78%. Difference × $4.4M ≈ **$1.0M**."),
    ("SMB test size", "About 1,900 customers per arm for three months at a 2.1% base rate gives a standard error of about 0.27 pts on the difference. A 0.6-pt reaction is about 2.2 standard errors (detectable); a 0.3-pt reaction is about 1.1 (not). This assumes most test customers renew within Q1, which needs monthly plans; fewer renewals means a weaker test."),
]
yy = 1.85
for k, v in calc:
    s.text(L, yy, 2.6, 0.5, k, size=11, bold=True, name="calc k")
    s.text(L + 2.75, yy, CW - 2.75, 0.62, v, size=10.5, name="calc v")
    hh = max(s.last_text_height, 0.2)
    yy += hh + 0.2
    s.line(L, yy - 0.1, R, yy - 0.1, RULE)

# Appendix A2: dashboard + assumptions/uncertainties
s = D.new()
chrome(s, "Appendix B · data caveats and choices",
       "The board churn figure cannot be reproduced. This page also lists the choices made where the briefing pack was silent")
hw = (CW - 0.4) / 2
s.text(L, 1.85, hw, 0.3, "Board dashboard \"monthly churn 1.4% → 2.3%\" vs Table 1", size=12, bold=True)
dash = [("Measure", "H1 2025", "H1 2026"), ("Board dashboard (undefined)", "1.4%", "2.3%"),
        ("Customer-weighted logo churn", "1.7%", "2.6%"), ("ARR-weighted logo churn", "0.8%", "1.2%"),
        ("SMB logo churn", "2.0%", "3.1%")]
yy = 2.3
for i, (a, b, c) in enumerate(dash):
    bold = i == 0
    s.text(L, yy, 3.3, 0.3, a, size=10.5, bold=bold, color=SEC if bold else INK)
    s.text(L + 3.4, yy, 1.0, 0.3, b, size=10.5, bold=bold, color=SEC if bold else INK, align="right")
    s.text(L + 4.6, yy, 1.0, 0.3, c, size=10.5, bold=bold, color=SEC if bold else INK, align="right")
    yy += 0.38
    s.line(L, yy - 0.07, L + 5.7, yy - 0.07, INK if i == 0 else RULE, 1 if i == 0 else 0.75)
s.text(L, yy + 0.05, hw, 1.4, [
    "Weighted with mid-2026 customer counts and ARR from Table 1. None of the obvious definitions gives 1.4% → 2.3%. Until Finance defines the figure, it should not be used for this decision.",
], size=10.5, color=SEC, name="dash note")
s.text(L, 4.95, hw, 0.3, "What would change the recommendation", size=12, bold=True)
s.text(L, 5.3, hw, 1.6, [
    {"text": "SMB test shows little reaction → extend +8% to H2 SMB renewals (already in the rule).", "bullet": True},
    {"text": "Mid-market renewals react much more than the new-sign-up test suggested → pause at the tripwire.", "bullet": True},
    {"text": "New-customer bookings fall short of ~$0.6M → revisit the 12% mid-market option ($0.7M).", "bullet": True},
], size=10.5, space_after=4, name="change")
xr = L + hw + 0.4
s.text(xr, 1.85, hw, 0.3, "Choices made where the pack was silent", size=12, bold=True)
s.text(xr, 2.25, hw, 4.6, [
    {"text": "**Mid-market increase set at 10%,** the tested level, rather than 12%.", "bullet": True},
    {"text": "**SMB test at +8%,** the 2023 level, so the 2023 response is a usable benchmark.", "bullet": True},
    {"text": "**Enterprise uncapped renewals at up to +10%,** matching mid-market. Actual terms vary by contract.", "bullet": True},
    {"text": "**2027 enterprise renewals assumed 60% capped,** the same share as the whole enterprise book.", "bullet": True},
    {"text": "**2027 NRR before price assumed equal to trailing 12-month NRR.** The SMB figure (94%) includes the promotion cliff, so it is probably conservative.", "bullet": True},
    {"text": "**Renewals spread evenly through the year**, so about half of SMB ARR renews in H2.", "bullet": True},
    {"text": "**Promotion-cohort churn (4.9%) is implied** from blended and regular SMB rates, weighted by mid-2026 counts.", "bullet": True},
    {"text": "**Not in the pack, so not modelled:** new-customer bookings, gross margin, and the cost of the onboarding programme.", "bullet": True},
], size=10.5, space_after=5, name="choices")

D.save(os.path.join(OUT, "Palisade_2027_pricing_decision.pptx"))
paths = D.render(PREV)
print("\n".join(D.warnings) or "no warnings")
print(len(paths), "slides")
