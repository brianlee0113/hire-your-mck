import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from deckkit import Deck, P, W, H

NAVY, INK, SEC, MUTED = "1B2A41", "0B0B0B", "52514E", "898781"
GRID, AXIS = "E1E0D9", "C3C2B7"
BLUE, BLUE_L, BLUE_D = "2A78D6", "E6F0FC", "1C5CAB"
ORANGE, ORANGE_L = "EB6834", "FDEDE6"
GRAYBAR, PANEL = "B9B7AE", "F4F3EF"
GOOD, WARN, CRIT = "0CA30C", "FAB219", "D03B3B"
SRC = "Source: Palisade Docs briefing pack"

deck = Deck()
page = [0]

def header(s, title, kicker=None):
    s.rect(0.6, 0.32, 0.55, 0.06, fill=BLUE)
    if kicker:
        s.text(1.25, 0.2, 8, 0.3, kicker.upper(), size=9, color=MUTED, bold=True)
    s.text(0.6, 0.5, 12.1, 1.0, title, size=22, color=NAVY, bold=True, valign="t")

def footer(s, source=SRC):
    page[0] += 1
    s.line(0.6, 6.98, 12.73, 6.98, color=GRID, lw=0.75)
    s.text(0.6, 7.02, 11.0, 0.36, source, size=8.5, color=MUTED)
    s.text(11.9, 7.02, 0.83, 0.3, str(page[0]), size=9, color=MUTED, align="r")

def takeaway(s, x, y, w, h, text, size=12.5):
    s.rect(x, y, 0.06, h, fill=BLUE)
    s.text(x + 0.15, y, w - 0.15, h, text, size=size, color=INK, valign="m")

def panel(s, x, y, w, h, title, paras, size=11.5, fill=PANEL, title_color=NAVY, para_space=5):
    s.rect(x, y, w, h, fill=fill)
    s.text(x + 0.18, y + 0.12, w - 0.36, 0.34, title, size=12.5, bold=True, color=title_color)
    s.text(x + 0.18, y + 0.5, w - 0.36, h - 0.6, paras, size=size, color=INK, para_space=para_space)

def chip(s, x, y, w, h, label, fill, ink="FFFFFF", size=10.5):
    s.rect(x, y, w, h, fill=fill)
    s.text(x, y, w, h, label, size=size, bold=True, color=ink, align="c", valign="m")

# ---------------- chart helpers ----------------
def yaxis(s, x, y, w, h, vmax, ticks, fmt, label_w=0.5, vmin=0):
    for t in ticks:
        yy = y + h - (t - vmin) / (vmax - vmin) * h
        s.line(x, yy, x + w, yy, color=GRID if t != vmin else AXIS, lw=0.75)
        s.text(x - label_w - 0.05, yy - 0.12, label_w, 0.24, fmt(t), size=9, color=MUTED, align="r")

def waterfall(s, x, y, w, h, steps, vmin, vmax, ticks, fmt=lambda v: f"{v:.1f}", label_h=0.75,
              label_size=9.5, value_size=10.5, bar_frac=0.62, target=None, tick_fmt=lambda t: f"{t:g}"):
    """steps: (label, value, kind, color) kind in total|delta. Values $M."""
    ph = h - label_h
    sy = lambda v: y + ph - (v - vmin) / (vmax - vmin) * ph
    yaxis(s, x, y, w, ph, vmax, ticks, tick_fmt, vmin=vmin)
    n = len(steps); slot = w / n; bw = slot * bar_frac
    run = 0; prev_top = None
    for i, (lab, val, kind, col) in enumerate(steps):
        bx = x + i * slot + (slot - bw) / 2
        if kind == "total":
            lo, hi = vmin, val; run = val; vtxt = fmt(val)
        else:
            lo, hi = sorted([run, run + val]); run = run + val
            vtxt = ("+" if val > 0 else "−") + fmt(abs(val))
        top, bot = sy(hi), sy(lo)
        s.rect(bx, top, bw, max(bot - top, 0.02), fill=col)
        if prev_top is not None:
            s.line(bx - (slot - bw), prev_top, bx, prev_top, color=MUTED, lw=0.5)
        prev_top = sy(run)
        vy = top - 0.27
        s.text(bx - 0.2, vy, bw + 0.4, 0.25, vtxt, size=value_size, bold=(kind == "total"), color=INK, align="c")
        s.text(x + i * slot + 0.02, y + ph + 0.06, slot - 0.04, label_h - 0.06, lab, size=label_size, color=SEC, align="c")
    if target is not None:
        tv, tl = target
        ty = sy(tv)
        s.line(x, ty, x + w, ty, color=ORANGE, lw=1.5)
        s.text(x + 0.05, ty - 0.29, 3.0, 0.26, tl, size=10, bold=True, color=ORANGE, align="l")

def hbars(s, x, y, w, rows, vmax, bar_h=0.34, gap=0.22, label_w=2.6, fmt=lambda v: f"{v:g}%", size=10.5):
    """rows: (label, value, color, value_text or None)."""
    bx = x + label_w; bwmax = w - label_w - 0.7
    for i, (lab, v, col, vt) in enumerate(rows):
        yy = y + i * (bar_h + gap)
        s.text(x, yy - 0.06, label_w - 0.12, bar_h + 0.12, lab, size=size, color=INK, align="r", valign="m")
        s.rect(bx, yy, max(bwmax * v / vmax, 0.02), bar_h, fill=col)
        s.text(bx + bwmax * v / vmax + 0.06, yy - 0.03, 1.4, bar_h + 0.06, vt or fmt(v), size=size, bold=True, color=INK, valign="m")
    s.line(bx, y - 0.08, bx, y + len(rows) * (bar_h + gap) - gap + 0.08, color=AXIS, lw=0.75)

def table(s, x, y, col_w, row_h, rows, header_fill=NAVY, size=10.5, header_size=11, first_col_bold=True,
          zebra=PANEL, col_align=None, highlight_col=None, hl_fill=BLUE_L, valign="m"):
    """rows[0] = header. row_h list or float."""
    if not isinstance(row_h, list):
        row_h = [row_h] * len(rows)
    yy = y
    for ri, row in enumerate(rows):
        xx = x; rh = row_h[ri]
        for ci, cell in enumerate(row):
            cw = col_w[ci]
            if ri == 0:
                s.rect(xx, yy, cw, rh, fill=header_fill if not (highlight_col == ci) else BLUE)
                s.text(xx + 0.08, yy, cw - 0.16, rh, cell, size=header_size, bold=True, color="FFFFFF", valign="m",
                       align=(col_align[ci] if col_align else "l"))
            else:
                fill = None
                if highlight_col == ci:
                    fill = hl_fill
                elif zebra and ri % 2 == 0:
                    fill = zebra
                if fill:
                    s.rect(xx, yy, cw, rh, fill=fill)
                s.text(xx + 0.08, yy + 0.02, cw - 0.16, rh - 0.04, cell, size=size, color=INK, valign=valign,
                       bold=(first_col_bold and ci == 0), align=(col_align[ci] if col_align else "l"))
            xx += cw
        yy += rh
        s.line(x, yy, x + sum(col_w), yy, color=GRID, lw=0.5)
    return yy

# =====================================================================================
# 1. Title
s = deck.new()
s.rect(0, 0, W, H, fill=NAVY)
s.rect(0.8, 2.0, 0.8, 0.08, fill=BLUE)
s.text(0.8, 2.25, 11.5, 1.45, "Raise prices in 2027 — but only where customers stay for value",
       size=34, bold=True, color="FFFFFF")
s.text(0.8, 3.85, 11.0, 1.0, "Mid-market and enterprise up at renewal from January; SMB held until a June test; "
       "fix the 2025 promotion cohort before pricing it", size=17, color="CDE2FB")
s.text(0.8, 5.3, 11, 0.4, "Pricing decision for the CEO and leadership team  ·  December 2026", size=13, color="FFFFFF", bold=True)
s.text(0.8, 5.7, 11.5, 0.6, "All figures from the Palisade Docs briefing pack (fictional benchmark data); no external data used. "
       "Money in $M of ARR unless stated.", size=10.5, color="B7D3F6")
page[0] += 1

# =====================================================================================
# 2. Executive summary
s = deck.new()
header(s, "Yes, raise prices in 2027, but not 12% on every plan: price mid-market and enterprise now, "
          "and hold SMB until the evidence is in", "Executive summary")
rows = [
    ("Churn is a cohort problem, not a market-wide price problem",
     "SMB monthly churn rose 2.0% → 3.1%; **~90% of the rise comes from the 2,100 customers who joined on the 2025 "
     "50%-off promotion**. Other SMB customers churn at 2.1% (2.0% a year ago) and only 18% of them cite price (19% in 2025). "
     "Mid-market 0.6% → 0.8%; enterprise flat at 0.2%."),
    ("The headroom is in mid-market and enterprise",
     "76% of ARR, net revenue retention (NRR) of 112% and 118%; customers stay for integrations and the audit trail; a +10% price test "
     "showed no significant conversion loss. SMB is where Inkwell's $9 plan is winning: win rate 51% → 38%."),
    ("The CFO's $10.3M is not available",
     "Only **$7.6M** can be repriced in 2027 (15% of mid-market and 60% of enterprise ARR do not renew; enterprise caps at 7%). "
     "After the likely churn response it is **$4.5–6.3M**."),
    ("Recommended plan",
     "Mid-market **+10%** at renewal; enterprise at contract terms (7% where capped, 10% otherwise): **+$4.3M**. SMB list "
     "price held through June while a controlled +8% test runs; go or no-go for the second half (+$0.4M). Activation programme for "
     "the promotion cohort (+$0.3M). **≈ $98.9M exit ARR, exactly the +15% target, before any new-customer ARR**; NRR ≈ 115%."),
    ("The trade-off",
     "≈ $1.6M less 2027 ARR than the CFO plan's base case on paper. In exchange: no wider price gap against Inkwell where Palisade "
     "is losing deals, and a measured answer on SMB price sensitivity before 5,900 customers are committed to it."),
]
yy = 1.62
hts = [0.86, 0.78, 0.72, 1.0, 0.78]
for (lab, body), hh in zip(rows, hts):
    s.text(0.6, yy, 3.0, hh, lab, size=12.5, bold=True, color=BLUE_D, valign="t")
    s.text(3.75, yy, 8.95, hh, body, size=12, color=INK, valign="t")
    yy += hh + 0.1
    s.line(0.6, yy - 0.06, 12.73, yy - 0.06, color=GRID, lw=0.5)
s.rect(0.6, yy + 0.02, 12.13, 0.5, fill=NAVY)
s.text(0.78, yy + 0.02, 11.8, 0.5, "**Decisions needed in December:** approve mid-market and enterprise renewal pricing · hold SMB and approve the "
       "test and June gate · fund the activation programme · restate the board churn metric", size=11.5, color="FFFFFF", valign="m")
footer(s, SRC + "; team analysis. Calculations and assumptions are in the appendix.")

# =====================================================================================
# 3. Churn by segment
s = deck.new()
header(s, "Churn rose almost only in SMB; mid-market edged up and enterprise is flat", "Where is churn rising?")
cx, cy, cw, ch = 1.25, 1.95, 6.2, 3.85
s.text(0.6, 1.55, 7, 0.3, "Monthly logo churn by segment, H1 2025 vs H1 2026", size=12, bold=True, color=INK)
vmax = 3.5
yaxis(s, cx, cy, cw, ch, vmax, [0, 1, 2, 3], lambda t: f"{t:g}%")
segs = [("SMB", 2.0, 3.1), ("Mid-market", 0.6, 0.8), ("Enterprise", 0.2, 0.2)]
slot = cw / 3; bw = 0.62
for i, (nm, a, b) in enumerate(segs):
    x0 = cx + i * slot + slot / 2 - bw - 0.02
    for j, (v, col) in enumerate([(a, GRAYBAR), (b, BLUE)]):
        bx = x0 + j * (bw + 0.04)
        hgt = v / vmax * ch
        s.rect(bx, cy + ch - hgt, bw, max(hgt, 0.02), fill=col)
        s.text(bx - 0.2, cy + ch - hgt - 0.28, bw + 0.4, 0.26, f"{v:.1f}%", size=11, bold=True, color=INK, align="c")
    s.text(cx + i * slot, cy + ch + 0.08, slot, 0.3, nm, size=11.5, bold=True, color=INK, align="c")
# legend
s.rect(cx, 6.35, 0.18, 0.18, fill=GRAYBAR); s.text(cx + 0.24, 6.29, 1.2, 0.3, "H1 2025", size=10, color=SEC)
s.rect(cx + 1.3, 6.35, 0.18, 0.18, fill=BLUE); s.text(cx + 1.54, 6.29, 1.2, 0.3, "H1 2026", size=10, color=SEC)
s.text(cx + 3.6, 6.29, 3.0, 0.3, "SMB: +1.1 pts   ·   MM: +0.2 pts   ·   Ent: 0", size=10, color=SEC, align="r")
# right: segment table
s.text(8.15, 1.55, 4.6, 0.3, "Segment economics, mid-2026", size=12, bold=True, color=INK)
table(s, 8.15, 1.95, [1.35, 1.1, 1.0, 1.13], 0.42,
      [["", "Customers", "ARR $M", "NRR"],
       ["SMB", "5,900", "21.0", "94%"],
       ["Mid-market", "1,350", "41.0", "112%"],
       ["Enterprise", "150", "24.0", "118%"],
       ["Total", "7,400", "86.0", "≈109%"]],
      col_align=["l", "r", "r", "r"], size=11)
takeaway(s, 8.15, 4.4, 4.58, 1.15,
         "SMB is **80% of customers but 24% of ARR**, and the only segment with NRR below 100%. Mid-market and enterprise, "
         "76% of ARR, are growing inside their base.", size=12)
s.text(8.15, 5.75, 4.58, 0.6, "Total NRR is ARR-weighted from the segment figures. Logo churn = share of customers lost per month.",
       size=9.5, color=MUTED)
footer(s, SRC + ", Table 1. NRR = net revenue retention, trailing 12 months.")

# =====================================================================================
# 4. Promo cohort explains the rise
s = deck.new()
header(s, "Inside SMB, the 2025 promotion cohort accounts for ~90% of the churn increase; "
          "the core SMB base is almost unchanged", "Why SMB churn rose")
s.text(0.6, 1.55, 7, 0.3, "SMB monthly logo churn, H1 2025 → H1 2026", size=12, bold=True, color=INK)
waterfall(s, 1.25, 2.0, 6.0, 4.3,
          [("SMB churn H1 2025", 2.0, "total", GRAYBAR),
           ("Core SMB drift (2.0% → 2.1%)", 0.1, "delta", BLUE),
           ("Promotion cohort mix effect", 1.0, "delta", ORANGE),
           ("SMB churn H1 2026", 3.1, "total", BLUE)],
          0, 3.5, [0, 1, 2, 3], fmt=lambda v: f"{v:.1f}%", label_h=0.6, label_size=10.5, tick_fmt=lambda t: f"{t:g}%")
s.text(0.6, 6.4, 7.0, 0.5, "If the cohort churned like other SMB customers, SMB churn would be 2.1%, not 3.1%.",
       size=10.5, color=SEC)
# right facts
s.text(8.0, 1.55, 4.7, 0.3, "The 2,100-customer promotion cohort", size=12, bold=True, color=INK)
facts = [
    ("~4.9%", "implied monthly churn, vs 2.1% for other SMB customers"),
    ("41% vs 72%", "sent ≥5 documents in month one (cohort vs other cohorts); low senders churn ~3× as often"),
    ("≤ 2 months", "after the 50% discount ended is when most of the leavers went"),
    ("$4.4M", "of ARR at full price, about $2.1k per customer vs $4.4k for other SMB customers"),
]
yy = 1.98
for big, small in facts:
    s.text(8.0, yy, 1.85, 0.8, big, size=20, bold=True, color=ORANGE, valign="t")
    s.text(9.9, yy + 0.04, 2.83, 0.85, small, size=11, color=INK)
    yy += 0.98
    s.line(8.0, yy - 0.1, 12.73, yy - 0.1, color=GRID, lw=0.5)
footer(s, SRC + ", §6. Cohort churn implied from mid-2026 counts: (5,900 × 3.1% − 3,800 × 2.1%) ÷ 2,100 = 4.9%. "
          "Mix effect = 3.1% − 2.1%.")

# =====================================================================================
# 5. Price sensitivity: promo vs core, Inkwell
s = deck.new()
header(s, "Price complaints come from the promotion cohort, not the core base; the real price pressure "
          "is Inkwell taking new SMB deals", "Is price driving churn?")
s.text(0.6, 1.55, 6.2, 0.55, "Churned SMB customers whose main exit reason was “price / found a cheaper option”",
       size=12, bold=True, color=INK)
hbars(s, 0.6, 2.35, 6.3,
      [("All SMB churners, H1 2025", 19, GRAYBAR, None),
       ("All SMB churners, H1 2026", 34, GRAYBAR, None),
       ("Promotion-cohort churners, H1 2026", 52, ORANGE, None),
       ("Other SMB churners, H1 2026", 18, BLUE, None)],
      vmax=60, bar_h=0.42, gap=0.32, label_w=2.75, size=11)
takeaway(s, 0.6, 5.45, 6.2, 1.1,
         "The jump from 19% to 34% is mix: the cohort's “price” is the discount ending (a doubling of their bill). "
         "Customers outside the cohort cite price as often as a year ago.", size=11.5)
# right: Inkwell
s.rect(7.35, 1.55, 5.38, 5.15, fill=PANEL)
s.text(7.55, 1.65, 5.0, 0.3, "Inkwell is winning new SMB business on price", size=12.5, bold=True, color=NAVY)
s.text(7.55, 2.05, 2.3, 0.75, "51% → 38%", size=24, bold=True, color=ORANGE)
s.text(9.85, 2.05, 2.75, 0.8, "Palisade's SMB win rate when Inkwell was considered, H1 2025 → H1 2026", size=10.5, color=INK)
s.text(7.55, 2.95, 5.0, 0.3, "List price per user per month", size=11, bold=True, color=INK)
ladder = [("Inkwell Starter (Oct 2025)", 9, GRAYBAR), ("Palisade SMB", 15, BLUE), ("Palisade SMB at +12%", 16.8, ORANGE),
          ("Inkwell Pro", 24, GRAYBAR), ("Palisade Business", 29, BLUE)]
hbars(s, 7.45, 3.35, 5.15, [(a, v, c, f"${v:.2f}".replace(".00", "")) for a, v, c in ladder], vmax=32, bar_h=0.3, gap=0.16,
      label_w=2.25, size=10)
s.text(7.55, 5.7, 5.0, 0.95, "A 12% rise takes the SMB plan from 1.7× to 1.9× Inkwell Starter. Inkwell has not been "
       "seen in mid-market or enterprise deals above 200 seats.", size=10.5, color=INK)
footer(s, SRC + ", Table 2 and §7. Exit-survey shares are of churned customers who answered the survey.")

# =====================================================================================
# 6. Headroom matrix
s = deck.new()
header(s, "Pricing headroom differs sharply by segment: mid-market and enterprise can carry an increase now, SMB cannot yet",
       "Where can price go up?")
rows = [
    ["", "SMB", "Mid-market", "Enterprise"],
    ["Share of ARR · renews in 2027", "24% · all of it", "48% · 85%", "28% · 40%; 60% of ARR capped at +7%/yr"],
    ["Churn trend (monthly)", "2.0% → 3.1%; core base 2.0% → 2.1%", "0.6% → 0.8%", "0.2% → 0.2%"],
    ["Net revenue retention", "94%", "112%", "118%"],
    ["Price evidence", "2023 +8%: churn 1.8% → 2.3% for 6 months, settled at 1.9%. Before Inkwell existed",
     "2024 +10% on new sign-ups: conversion 23.1% vs 23.6% (not significant)", "Contract terms; increases negotiated per account"],
    ["Competition", "Inkwell $9 Starter; win rate 51% → 38%", "Inkwell not seen above 200 seats", "Inkwell not seen"],
    ["Why customers stay", "Activation: <5 documents in month one → ~3× churn", "Integrations, audit trail (advisory board)",
     "Integrations, audit trail (advisory board)"],
    ["Verdict for 2027", "", "", ""],
]
cws = [2.55, 3.3, 3.1, 3.18]
rh = [0.42, 0.52, 0.52, 0.42, 0.82, 0.52, 0.62, 0.62]
endy = table(s, 0.6, 1.6, cws, rh, rows, size=10.5)
vy = endy - 0.62 + 0.11
x0 = 0.6 + cws[0]
chip(s, x0 + 0.1, vy, cws[1] - 0.2, 0.4, "HOLD AND TEST  ·  decide in June", WARN, ink=INK)
chip(s, x0 + cws[1] + 0.1, vy, cws[2] - 0.2, 0.4, "RAISE  ·  +10% at renewal", GOOD)
chip(s, x0 + cws[1] + cws[2] + 0.1, vy, cws[3] - 0.2, 0.4, "RAISE  ·  at contract terms", GOOD)
takeaway(s, 0.6, endy + 0.15, 12.13, 0.5,
         "Price is not what is driving churn in any segment, but **only in SMB is price what decides new deals**, and that is where the "
         "evidence is weakest.", size=12)
footer(s, SRC + ", §5, §7–§9.")

# =====================================================================================
# 7. CFO waterfall
s = deck.new()
header(s, "The CFO's $10.3M assumes all ARR reprices in 2027; renewal timing and contract caps cut it to $7.6M, "
          "and churn to $4.5–6.3M", "Testing the CFO plan: +12% on every plan")
s.text(0.6, 1.55, 8, 0.3, "ARR gained from +12% on every plan in 2027, $M", size=12, bold=True, color=INK)
waterfall(s, 1.1, 2.05, 7.7, 4.4,
          [("CFO estimate: 12% × $86.0M", 10.3, "total", GRAYBAR),
           ("Mid-market not renewing in 2027 (15%)", -0.7, "delta", ORANGE),
           ("Enterprise not renewing in 2027 (60%)", -1.7, "delta", ORANGE),
           ("Enterprise 7% caps", -0.3, "delta", ORANGE),
           ("Repriceable in 2027", 7.6, "total", BLUE),
           ("SMB churn response (2023 pattern)", -1.3, "delta", ORANGE),
           ("Base case", 6.3, "total", BLUE),
           ("Downside: 2× SMB response + mid-market reaction", -1.8, "delta", ORANGE),
           ("Downside case", 4.5, "total", BLUE)],
          0, 11.5, [0, 2, 4, 6, 8, 10], label_h=0.95, label_size=9, value_size=10.5)
panel(s, 9.2, 1.55, 3.53, 5.15, "What drives the gap", [
    P("**Renewal timing.** Price changes apply at renewal; 85% of mid-market and 40% of enterprise ARR renew in 2027.", bullet=True),
    P("**Contract caps.** 60% of enterprise ARR cannot rise more than 7% a year.", bullet=True),
    P("**SMB churn.** In 2023, +8% raised SMB churn by 0.5 pts for six months and 0.1 pts after; scaled to 12% that loses "
      "~5% of SMB ARR.", bullet=True),
    P("**Not counted:** any loss of new SMB deals to Inkwell from a higher list price.", bullet=True),
    P("**SMB is the weak link:** of its $2.5M gross gain, $1.3M (base) to $2.5M (downside) goes back out as churn.",
      bullet=True, color=BLUE_D),
], size=10.5, para_space=6)
footer(s, SRC + ", §4, §8. Assumes capped contracts are 60% of renewing enterprise ARR. Exit-2027 ARR effect; see appendix.")

# =====================================================================================
# 8. Options
s = deck.new()
header(s, "Of three options, a segmented increase meets the 15% growth target with the least exposure in SMB", "Options")
rows = [
    ["", "A · CFO plan: +12% on every plan", "B · Hold prices, fix onboarding", "C · Segmented increase (recommended)"],
    ["Price moves", "+12% at renewal on all plans and list prices from January",
     "None in 2027", "Mid-market +10%, enterprise at terms from January; SMB +8% from July only if the test passes"],
    ["Net 2027 ARR from price, $M (base / downside)", "6.3 / 4.5", "0 / 0", "4.7 / 3.8"],
    ["Exit-2027 ARR before new customers, $M (target $98.9M)", "100.5 / 98.4", "94.2 / 94.0", "98.9 / 97.8"],
    ["New-customer ARR needed for +15%, $M", "0 / 0.5", "4.7 / 4.9", "0 / 1.1"],
    ["Overall NRR (base)", "≈117%", "≈110%", "≈115%"],
    ["SMB exposure", "All 5,900 SMB customers, plus new buyers at $16.80 vs Inkwell's $9",
     "None", "None until July; +8% for the core base only if the test passes; promotion cohort deferred to 2028"],
    ["Main risk", "SMB deals and promotion-cohort churn; 2027 churn signal becomes hard to read",
     "Misses the target unless new-customer ARR is ≥ $4.7M; leaves mid-market and enterprise headroom unused",
     "≈ $1.6M below A in the base case; downside needs ≥ $1.1M of new-customer ARR"],
]
cws = [2.75, 3.1, 2.9, 3.38]
rh = [0.5, 0.66, 0.5, 0.5, 0.5, 0.4, 0.66, 0.86]
endy = table(s, 0.6, 1.55, cws, rh, rows, size=10.5, highlight_col=3, zebra=None)
yy = endy + 0.12
s.text(0.6, yy, cws[0], 0.4, "Verdict", size=10.5, bold=True, valign="m")
chip(s, 0.6 + cws[0] + 0.1, yy + 0.02, cws[1] - 0.2, 0.36, "NOT RECOMMENDED", CRIT, size=10)
chip(s, 0.6 + cws[0] + cws[1] + 0.1, yy + 0.02, cws[2] - 0.2, 0.36, "NOT RECOMMENDED", CRIT, size=10)
chip(s, 0.6 + cws[0] + cws[1] + cws[2] + 0.1, yy + 0.02, cws[3] - 0.2, 0.36, "RECOMMENDED", GOOD, size=10)
s.text(0.6, yy + 0.44, 12.13, 0.45, "All options include promotion-cohort activation (+$0.3M). Base = $86.0M × each segment's trailing NRR = $94.0M. "
       "Downside = stronger churn response, no activation gain, SMB test fails.", size=9, color=MUTED)
footer(s, SRC + "; team analysis. New-customer bookings for 2027 are not in the pack.")

# =====================================================================================
# 9. Bridge to target
s = deck.new()
header(s, "The recommended plan reaches the +15% target ($98.9M) before any new-customer ARR, but with no margin to spare", "Recommended plan: path to the 15% target")
s.text(0.6, 1.55, 8.5, 0.3, "Exit-2027 ARR, base case, $M", size=12, bold=True, color=INK)
waterfall(s, 1.1, 2.0, 7.9, 4.5,
          [("ARR mid-2026", 86.0, "total", GRAYBAR),
           ("Existing base at trailing NRR", 8.0, "delta", GRAYBAR),
           ("Mid-market +10% at renewal", 3.5, "delta", BLUE),
           ("Enterprise at contract terms", 0.8, "delta", BLUE),
           ("Promotion-cohort activation", 0.3, "delta", BLUE),
           ("SMB +8% from July (if test passes)", 0.4, "delta", BLUE),
           ("Exit 2027, before new customers", 98.9, "total", NAVY)],
          80, 102, [80, 85, 90, 95, 100], label_h=0.8, label_size=9.5, target=(98.9, "Target +15% = $98.9M"))
s.text(0.6, 6.55, 8.5, 0.35, "Axis starts at $80M. Existing base: SMB −1.3, mid-market +4.9, enterprise +4.3.", size=9.5, color=MUTED)
panel(s, 9.35, 1.55, 3.38, 5.2, "Reading the bridge", [
    P("**Downside: $97.8M.** Mid-market reacts at renewal, activation gains nothing, the SMB test fails. Closing the gap needs "
      "≥ $1.1M of new-customer ARR.", bullet=True),
    P("**New-customer ARR is the buffer.** It is not in the pack; Sales should confirm the 2027 plan before the board meeting.", bullet=True),
    P("**Spare lever:** if mid-market renewals hold through June, renew the second half at +12% (+$0.35M).", bullet=True),
    P("**Timing:** each month of renewals missed because notice periods have passed costs ≈ $0.36M.", bullet=True),
], size=10.5, para_space=6)
footer(s, SRC + "; team analysis. Assumes trailing NRR repeats in 2027 and contains no past price rises.")

# =====================================================================================
# 10. Trade-off vs CFO
s = deck.new()
header(s, "Against the CFO plan we give up ≈ $1.6M of 2027 ARR on paper: about half from deferring SMB, "
          "half from staying at the tested 10% in mid-market", "The trade-off")
s.text(0.6, 1.55, 6.3, 0.3, "Where the $1.6M gap comes from (base case, $M)", size=12, bold=True, color=INK)
waterfall(s, 1.0, 2.0, 5.9, 3.9,
          [("SMB +12% in January, net of churn", 1.25, "total", ORANGE),
           ("Mid-market and enterprise at 12% instead of 10%", 0.77, "delta", ORANGE),
           ("SMB +8% from July recovers", -0.40, "delta", BLUE),
           ("Gap: A minus C", 1.62, "total", NAVY)],
          0, 2.4, [0, 0.5, 1.0, 1.5, 2.0], fmt=lambda v: f"{v:.2f}", label_h=0.85, label_size=9.5)
s.text(0.6, 6.0, 6.3, 0.8, "In the downside case the January SMB rise nets **≈ $0**: $2.5M of extra churn cancels $2.5M of price. "
       "Deferring it costs at most ≈ $0.85M.", size=11, color=INK)
panel(s, 7.3, 1.55, 5.43, 5.2, "What the six-month SMB deferral buys", [
    P("**An answer to the biggest open question.** How price-sensitive the core SMB base is now that Inkwell exists, measured "
      "before committing all 5,900 customers.", bullet=True),
    P("**No wider gap at the point of sale.** SMB win rate against Inkwell is already down 13 points; neither A nor C "
      "counts the effect on new deals.", bullet=True),
    P("**A clean read on onboarding.** With SMB prices unchanged, 2027 churn shows whether activation works.", bullet=True),
    P("**Mid-market stays at the tested level** on 48% of ARR. The test covered new sign-ups, not renewals.", bullet=True),
    P("**Where the CFO is right:** the churn rise is mostly an onboarding and cohort problem. That is why mid-market and "
      "enterprise go ahead in January.", bullet=True, color=BLUE_D),
], size=11, para_space=7)
footer(s, SRC + "; team analysis.")

# =====================================================================================
# 11. Onboarding
s = deck.new()
header(s, "Onboarding will help, but it cannot halve SMB churn in two quarters: low activation explains under a "
          "third of the cohort's excess churn", "Testing the onboarding claim")
s.text(0.6, 1.55, 5.9, 0.55, "Promotion-cohort monthly churn split into its drivers, H1 2026 (%)", size=12, bold=True, color=INK)
waterfall(s, 1.0, 2.15, 5.5, 3.9,
          [("Core SMB rate", 2.1, "total", GRAYBAR),
           ("Lower activation (41% vs 72%)", 0.8, "delta", BLUE),
           ("Discount ending and other", 2.0, "delta", ORANGE),
           ("Cohort churn", 4.9, "total", NAVY)],
          0, 5.5, [0, 1, 2, 3, 4, 5], fmt=lambda v: f"{v:.1f}%", label_h=0.7, label_size=10, tick_fmt=lambda t: f"{t:g}%")
s.text(0.6, 6.15, 5.9, 0.7, "The activation share applies the pack's “~3× churn below five documents” to each cohort's activation mix.",
       size=9.5, color=MUTED)
s.text(7.0, 1.55, 5.7, 0.3, "SMB monthly churn under different outcomes", size=12, bold=True, color=INK)
hbars(s, 7.0, 2.05, 5.73,
      [("Today (H1 2026)", 3.1, NAVY, None),
       ("Cohort activates like others", 2.8, BLUE, "≈2.8%"),
       ("Cohort churns like core SMB", 2.1, BLUE, None),
       ("Lowest SMB rate in the pack (pre-2023)", 1.8, GRAYBAR, None),
       ("Customer Success claim: halve it", 1.55, ORANGE, "1.55%")],
      vmax=3.6, bar_h=0.36, gap=0.2, label_w=2.6, size=10.5)
panel(s, 7.0, 4.95, 5.73, 1.85, "Implication", [
    P("Plan on **≈ $0.3M** of saved ARR, with upside to $1.0M if the cohort settles at the core rate as the post-discount wave fades.", bullet=True),
    P("Set targets on activation and cohort churn, not “halve SMB churn”. Halving needs a rate below anything SMB has recorded.", bullet=True),
], size=10.5, fill=BLUE_L, para_space=4)
footer(s, SRC + ", §6, §8–§10. Saved ARR = cohort's 12-month loss at 4.9% vs 4.1% monthly on $4.4M; upside at 2.1%.")

# =====================================================================================
# 12. Roadmap
s = deck.new()
header(s, "How: mid-market and enterprise renewals start in January, SMB is tested in the first half, "
          "and leadership decides in June", "Implementation")
gx, gy, gw = 3.35, 1.65, 9.38
months = ["Dec", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
mw = gw / len(months)
for i, m in enumerate(months):
    s.text(gx + i * mw, gy, mw, 0.28, m, size=9.5, bold=True, color=SEC, align="c")
s.text(gx, gy - 0.3, mw, 0.28, "2026", size=8.5, color=MUTED, align="c")
s.text(gx + mw, gy - 0.3, 2, 0.28, "2027", size=8.5, color=MUTED)
s.line(gx, gy + 0.32, gx + gw, gy + 0.32, color=AXIS)
for i in range(1, len(months)):
    s.line(gx + i * mw, gy + 0.32, gx + i * mw, 6.2, color=GRID, lw=0.5)
lanes = [
    ("Mid-market and enterprise pricing", "Owner: CFO + Sales",
     [(0, 1, "Notices", GRAYBAR, INK), (1, 13, "Mid-market +10% and enterprise at terms, applied at each renewal", BLUE, "FFFFFF")]),
    ("SMB price test", "Owner: Growth / Product",
     [(0, 1, "Design", GRAYBAR, INK), (2, 6, "+8% test: new sign-ups and a 10% sample of renewals", BLUE, "FFFFFF"),
      (7, 13, "If go: +8% list; core base at renewal", BLUE_L, INK)]),
    ("Promotion-cohort activation", "Owner: Customer Success",
     [(1, 7, "Activation programme; targets by end-June", BLUE, "FFFFFF"), (7, 13, "Continue if targets met", BLUE_L, INK)]),
    ("Metrics and governance", "Owner: CFO",
     [(0, 1, "Define churn", GRAYBAR, INK), (1, 13, "Monthly guardrail review (p.13)", BLUE_L, INK)]),
]
jx = gx + 6.5 * mw
s.line(jx, gy + 0.32, jx, 6.2, color=ORANGE, lw=1.75)
ly = gy + 0.5
for name, owner, bars in lanes:
    s.text(0.6, ly, 2.65, 0.4, name, size=11, bold=True, color=INK)
    s.text(0.6, ly + 0.4, 2.65, 0.3, owner, size=9.5, color=MUTED)
    for a, b, lab, col, ink in bars:
        s.rect(gx + a * mw + 0.03, ly + 0.08, (b - a) * mw - 0.06, 0.5, fill=col)
        s.text(gx + a * mw + 0.06, ly + 0.08, (b - a) * mw - 0.12, 0.5, lab, size=9.5, color=ink, valign="m",
               align="c")
    ly += 1.0
    s.line(0.6, ly - 0.14, gx + gw, ly - 0.14, color=GRID, lw=0.5)
# June gate
s.diamond(jx, 6.32, 0.24, ORANGE)
s.text(jx - 1.6, 6.45, 3.2, 0.45, "**June gate:** SMB go or no-go; mid-market +12% for the second half?", size=10, color=INK, align="c")
s.diamond(gx + 10.5 * mw, 6.32, 0.24, NAVY)
s.text(gx + 10.5 * mw - 1.2, 6.45, 2.4, 0.45, "**Oct:** 2028 pricing, incl. an answer to Inkwell", size=10, color=INK, align="c")
s.diamond(gx + 0.5 * mw, 6.32, 0.24, NAVY)
s.text(gx - 0.5, 6.45, 1.6, 0.45, "**Dec:** decision", size=10, color=INK, align="c")
footer(s, "Team proposal. The promotion cohort is excluded from any 2027 SMB increase. Renewal notice periods to be confirmed by Legal.")

# =====================================================================================
# 13. Guardrails
s = deck.new()
header(s, "Guardrails tell us early whether to pause, extend or stop each move", "Guardrails (proposed thresholds)")
rows = [
    ["Move", "Metric", "Today", "Proposed trigger", "Action"],
    ["Mid-market +10%", "Monthly logo churn of renewing mid-market accounts", "0.8%",
     "> 1.0% for two months running", "Pause rises on remaining renewals; offer a multi-year price lock instead"],
    ["", "(same metric)", "", "≤ 0.8% through June", "Renew the second half at +12% (+$0.35M)"],
    ["Enterprise at terms", "Renewal outcome of each top account", "0.2% churn; NRR 118%",
     "Any renewal flagged at risk", "Trade the increase for a longer term; never breach the 7% cap"],
    ["SMB +8% test (June gate)", "Conversion at +8% vs control; churn of renewal sample vs control; price share of core churners",
     "2.1% core churn; 18% cite price", "Go only if conversion is not significantly lower, sample churn ≤ control + 0.3 pts and price share ≤ 20%",
     "Go: +8% from July for the core base. No-go: hold through 2027 and build a packaging answer to Inkwell for 2028"],
    ["Promotion-cohort activation", "Share sending ≥5 documents a month; cohort monthly churn", "41%; ≈4.9%",
     "≥ 55% and ≤ 4.0% by end-June", "If missed, stop extra spend; plan on ≈45% of the cohort's ARR ($2.0M) leaving within 12 months"],
    ["Competitive position", "SMB win rate where Inkwell is considered", "38%", "< 35%", "Bring the 2028 SMB packaging review forward"],
]
cws = [2.0, 3.0, 1.75, 2.65, 2.73]
rh = [0.42, 0.62, 0.52, 0.62, 1.02, 0.82, 0.55]
endy = table(s, 0.6, 1.55, cws, rh, rows, size=10, zebra=None)
s.text(0.6, endy + 0.12, 12.13, 0.5, "Thresholds are our proposal for leadership to confirm; the pack gives today's values only. "
       "Review monthly at the pricing steering meeting.", size=9.5, color=MUTED)
footer(s, SRC + "; team proposal.")

# =====================================================================================
# 14. Risks / uncertainties
s = deck.new()
header(s, "Three open questions could change the plan; each has a built-in test", "Risks and what would change our mind")
qs = [
    ("1", "How price-sensitive is the core SMB base now that Inkwell exists?",
     "The only evidence (2023, +8%) predates Inkwell.", "If the test is clean: +8% from July, and SMB returns to the 2028 plan. "
     "If not: hold, and work on packaging rather than list price."),
    ("2", "Can the promotion cohort be activated, or will it mostly churn anyway?",
     "Activation explains under a third of its excess churn.", "If targets are missed by June, stop extra spend. Its "
     "losses are already in the baseline NRR; a reverting cohort is upside."),
    ("3", "Does the 2024 mid-market test (new sign-ups) predict renewals?",
     "Existing customers may react differently from new buyers.", "The guardrail on renewing accounts gives a first read in Q1. "
     "Pause if churn exceeds 1.0%; extend to 12% if it holds."),
]
yy = 1.82
for n, q, why, resp in qs:
    s.oval(0.6, yy + 0.05, 0.5, 0.5, fill=BLUE)
    s.text(0.6, yy + 0.05, 0.5, 0.5, n, size=16, bold=True, color="FFFFFF", align="c", valign="m")
    s.text(1.3, yy, 4.6, 0.85, q, size=12.5, bold=True, color=INK)
    s.text(6.05, yy, 2.55, 0.95, why, size=10.5, color=SEC)
    s.text(8.75, yy, 3.98, 0.95, resp, size=10.5, color=INK)
    yy += 1.05
    s.line(0.6, yy - 0.08, 12.73, yy - 0.08, color=GRID, lw=0.5)
s.text(6.05, 1.45, 2.5, 0.28, "WHY IT IS OPEN", size=9, bold=True, color=MUTED)
s.text(8.75, 1.45, 3.9, 0.28, "WHAT WE WOULD DO", size=9, bold=True, color=MUTED)
s.text(0.6, yy + 0.08, 12, 0.3, "Gaps in the evidence to close before the board meeting", size=12, bold=True, color=NAVY)
gaps = [
    ("New-customer ARR plan for 2027", "Not in the pack. The downside case needs ≥ $1.1M of it to reach +15%."),
    ("Renewal notice periods", "Each month of renewals missed costs ≈ $0.36M of the $4.3M."),
    ("Board churn metric", "“1.4% → 2.3%” cannot be rebuilt from segment data (appendix)."),
]
gx = 0.6
for t, b in gaps:
    s.rect(gx, yy + 0.48, 3.93, 1.2, fill=PANEL)
    s.text(gx + 0.15, yy + 0.56, 3.65, 0.32, t, size=11, bold=True, color=INK)
    s.text(gx + 0.15, yy + 0.9, 3.65, 0.75, b, size=10.5, color=INK)
    gx += 4.1
footer(s, SRC + ", §11; team analysis.")

# =====================================================================================
# 15. Decisions
s = deck.new()
header(s, "Five decisions for the leadership team in December", "Next steps")
dec = [
    ("Approve", "Mid-market +10% at renewal and enterprise increases at contract terms (7% where capped, 10% target otherwise), "
     "effective with January 2027 renewals.", "CFO, Sales"),
    ("Reject", "The +12% rise on every plan. Hold SMB list prices through June 2027; exclude the promotion cohort from any "
     "2027 increase.", "CEO"),
    ("Approve", "The SMB +8% test (February–May) and the June go or no-go gate with the criteria on page 13.", "Growth / Product"),
    ("Fund", "The promotion-cohort activation programme, with targets on activation (≥55%) and cohort churn (≤4.0%), "
     "not “halve SMB churn”.", "Customer Success"),
    ("Fix", "The board churn metric: report logo and revenue churn by segment, and confirm the 2027 new-customer ARR plan.", "CFO, Sales"),
]
yy = 1.6
for i, (verb, body, own) in enumerate(dec):
    chip(s, 0.6, yy + 0.12, 1.35, 0.46, verb.upper(), NAVY if verb != "Reject" else CRIT, size=11)
    s.text(2.15, yy, 8.4, 0.75, body, size=12.5, color=INK, valign="m")
    s.text(10.7, yy, 2.03, 0.75, own, size=11, color=SEC, valign="m")
    yy += 0.92
    s.line(0.6, yy - 0.09, 12.73, yy - 0.09, color=GRID, lw=0.5)
s.text(10.7, 1.3, 2.0, 0.28, "SUGGESTED OWNER", size=9, bold=True, color=MUTED)
takeaway(s, 0.6, yy + 0.1, 12.13, 0.6, "Result: ≈ $98.9M exit ARR (+15%) before new customers, NRR ≈ 115%, and the SMB price "
         "decision taken in June on evidence rather than on the 2023 analogue.", size=12.5)
footer(s, "Team proposal.")

# =====================================================================================
# A1. Assumptions
s = deck.new()
header(s, "Appendix: how the numbers were built", "Appendix A · Calculations and assumptions")
left = [
    P("**Baseline (no price change).** Each segment's ARR × its trailing-12-month NRR: SMB 21.0 × 94% = 19.7; mid-market "
      "41.0 × 112% = 45.9; enterprise 24.0 × 118% = 28.3; total $94.0M (+9.3%). Assumes 2027 repeats the trailing year "
      "and that the trailing NRR contains no price rise.", bullet=True),
    P("**Target.** $86.0M × 1.15 = $98.9M exit-2027 ARR. Price effects are measured on exit ARR: every 2027 renewal counts in full.", bullet=True),
    P("**Repriceable ARR at +12%.** SMB 21.0 × 12% = 2.52; mid-market 41.0 × 85% × 12% = 4.18; enterprise 9.6 renewing, "
      "60% capped at 7% and 40% at 12% = 0.86; total $7.57M. If no renewing contract is capped: 1.15; if all are: 0.67.", bullet=True),
    P("**SMB churn response.** 2023: +8% → +0.5 pts a month for six months, then +0.1 pts. Scaled linearly to 12%: "
      "5.4% extra churn × $23.5M = $1.27M. Downside doubles it ($2.54M) for Inkwell.", bullet=True),
    P("**Mid-market response (downside only).** +0.2 pts a month for six months on renewing ARR: $0.46M at 10%, $0.56M at 12%.", bullet=True),
]
right = [
    P("**Recommended price ARR.** Mid-market 34.85 × 10% = 3.49; enterprise 5.76 × 7% + 3.84 × 10% = 0.79; total $4.27M.", bullet=True),
    P("**SMB +8% from July.** Half of the core SMB ARR ($16.6M) reprices by year-end: 8.3 × 8% = 0.66, less the 2023-style "
      "response of 3% × 8.96 = 0.27; net ≈ $0.40M.", bullet=True),
    P("**Promotion cohort.** Implied churn (5,900 × 3.1% − 3,800 × 2.1%) ÷ 2,100 = 4.9%. Activation split: with low senders "
      "churning 3× as often, core 2.1% implies 1.35% for activated customers; the cohort's 41% activation implies 2.9%; the rest "
      "(2.0 pts) is the discount ending and other factors.", bullet=True),
    P("**Activation value.** 12-month loss on $4.4M at 4.9% a month = 45% ($2.0M); at 4.1% = 39% ($1.7M); saves ≈ $0.3M. "
      "At 2.1% = 22% ($1.0M); saves ≈ $1.0M (upside).", bullet=True),
    P("**Rounding.** Figures are rounded to $0.1M; bars may not sum exactly.", bullet=True),
]
s.text(0.6, 1.5, 5.95, 5.4, left, size=11.5, para_space=9)
s.text(6.78, 1.5, 5.95, 5.4, right, size=11.5, para_space=9)
footer(s, SRC + "; team analysis.")

# =====================================================================================
# A2. Dashboard
s = deck.new()
header(s, "Appendix: the board dashboard's “1.4% → 2.3%” churn figure cannot be rebuilt from the segment data",
       "Appendix B · Churn metric definition")
rows = [
    ["Definition tried", "H1 2025", "H1 2026", "Matches 1.4% → 2.3%?"],
    ["Customer-weighted logo churn (mid-2026 customer counts)", "1.7%", "2.6%", "No"],
    ["Customer-weighted, 2025 base excluding the promotion cohort", "1.6%", "2.6%", "No"],
    ["ARR-weighted logo churn", "0.8%", "1.2%", "No"],
    ["Board dashboard (undefined)", "1.4%", "2.3%", "—"],
]
table(s, 0.6, 1.65, [5.6, 1.6, 1.6, 2.6], 0.5, rows, col_align=["l", "r", "r", "c"], size=11.5)
takeaway(s, 0.6, 4.4, 11.4, 0.95, "Do not use the dashboard figure for the pricing decision. Report **logo churn and revenue churn "
         "by segment**, with the promotion cohort shown separately, so the board can see whether price rises or onboarding move churn in 2027.",
         size=12)
footer(s, SRC + ", §5 and §10; team analysis.")

out = os.path.join(os.path.dirname(__file__), "..", "deliverable")
deck.save_pptx(os.path.join(out, "Palisade_2027_Pricing_Decision.pptx"))
prev = os.path.join(os.path.dirname(__file__), "preview"); os.makedirs(prev, exist_ok=True)
pngs = deck.render_png(os.path.join(prev, "slide_{:02d}.png"))
from PIL import Image
ims = [Image.open(x).convert("RGB") for x in pngs]
ims[0].save(os.path.join(out, "Palisade_2027_Pricing_Decision_preview.pdf"), save_all=True, append_images=ims[1:], resolution=120)
print("\n".join(deck.warnings) or "no overflow warnings")
print(len(deck.slides), "slides")
