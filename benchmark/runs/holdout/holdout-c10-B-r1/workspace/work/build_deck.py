import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from decklib import Deck, WARNINGS

OUT = os.path.join(os.path.dirname(__file__), "..", "deliverable")
PREV = os.path.join(os.path.dirname(__file__), "preview")
os.makedirs(OUT, exist_ok=True)
os.makedirs(PREV, exist_ok=True)

# ---------------- palette ----------------
NAVY = "0B2A4A"      # titles, totals
INK = "1F1F1F"
INK2 = "52514E"      # secondary text
MUTED = "8A8986"
RULE = "D0CFCB"
PANEL = "F3F2EF"
BLUE = "2A78D6"      # positive / recommended
BLUE_LT = "CDE2FB"
RED = "C8393A"       # negative / fails (text-safe red)
RED_BAR = "E34948"
AMBER = "B07800"
GREEN = "1A7F4B"
GREY_BAR = "A9A8A4"

SRC = "Source: Vesper MedTech board briefing pack (FY2026 full-year figures; synthetic data). "
LM, CW = 0.5, 12.333  # left margin, content width

d = Deck()


def header(s, section, title):
    s.text(LM, 0.22, 9, 0.28, section.upper(), size=9, color=BLUE, bold=True, inset=0)
    s.text(LM, 0.48, CW, 0.92, title, size=20, color=NAVY, bold=True, inset=0, anchor="m")
    s.line(LM, 1.47, LM + CW, 1.47, color=NAVY, lw=1.0)


def footer(s, note=""):
    s.text(LM, 6.98, 11.4, 0.36, SRC + note, size=8, color=MUTED, inset=0, anchor="b")
    s.text(LM + CW - 0.6, 7.06, 0.6, 0.28, str(s.num), size=9, color=MUTED, align="r", inset=0, anchor="b")


def pill(s, x, y, w, label, color):
    s.rect(x, y, w, 0.26, fill=color, rounded=True)
    s.text(x, y, w, 0.26, label, size=9, color="FFFFFF", bold=True, align="c", anchor="m", inset=0.02)


def waterfall(s, x, y, w, h, items, vmin, vmax, label_h=0.55, fmt=lambda v: f"{v:+.2f}",
              bar_frac=0.58, show_zero=True, value_size=11, cat_size=9.5, tfmt="{:.2f}"):
    """items: (label, value, kind) kind: total | delta | sub. Values in $M.
    Chart plot area = y .. y+h-label_h ; category labels below."""
    ph = h - label_h
    n = len(items)
    slot = w / n
    bw = slot * bar_frac

    def Y(v):
        return y + (vmax - v) / (vmax - vmin) * ph

    run = 0.0
    prev_top = None
    for i, (lab, v, kind) in enumerate(items):
        bx = x + i * slot + (slot - bw) / 2
        if kind in ("total", "sub"):
            a, b = 0.0, v
            run = v
            col = NAVY if kind == "total" else "45617F"
        else:
            a, b = run, run + v
            run = run + v
            col = BLUE if v >= 0 else RED_BAR
        top, bot = Y(max(a, b)), Y(min(a, b))
        s.rect(bx, top, bw, max(bot - top, 0.01), fill=col)
        # value label
        txt = fmt(v) if kind == "delta" else (tfmt.format(v) if v >= 0 else "–" + tfmt.format(abs(v)))
        txt = txt.replace("-", "–")
        if (kind == "delta" and v < 0) or (kind != "delta" and v < 0):
            s.text(bx - 0.25, bot + 0.03, bw + 0.5, 0.26, txt, size=value_size, bold=True, color=INK, align="c", inset=0)
        else:
            s.text(bx - 0.25, top - 0.29, bw + 0.5, 0.26, txt, size=value_size, bold=True, color=INK, align="c", inset=0)
        # connector to next
        if i < n - 1:
            nx = x + (i + 1) * slot + (slot - bw) / 2
            s.line(bx + bw, Y(run), nx, Y(run), color=MUTED, lw=0.5, dash=True)
        s.text(x + i * slot + 0.02, y + ph + 0.08, slot - 0.04, label_h - 0.08, lab, size=cat_size,
               color=INK2, align="c", inset=0)
    if show_zero:
        s.line(x, Y(0), x + w, Y(0), color=INK2, lw=0.75)
    return Y


# =====================================================================
# 1. Title
# =====================================================================
s = d.new_slide("title")
s.rect(0, 0, 13.333, 7.5, fill=NAVY)
s.rect(LM, 2.2, 0.08, 2.0, fill=BLUE)
s.text(LM + 0.3, 1.2, 11, 0.4, "VESPER MEDTECH  |  BOARD OF DIRECTORS", size=12, color="9EC5F4", bold=True, inset=0)
s.text(LM + 0.3, 1.95, 11.5, 1.65, "Keep connector C: redesign it now, fix bundle service, and decide any 2029 sunset on evidence",
       size=31, color="FFFFFF", bold=True, inset=0, anchor="m")
s.text(LM + 0.3, 3.65, 11.5, 0.6,
       "Board question: should Vesper discontinue low reported-margin sterile connector C and redeploy the team to connector D?",
       size=15, color="DCE6F0", inset=0)
s.text(LM + 0.3, 5.6, 11.5, 0.9,
       ["Pre-read for the February 2027 board meeting  |  Prepared November 2026",
        "All figures in US$ millions, FY2026 full year, from the board briefing pack (synthetic benchmark data)"],
       size=11, color="9EC5F4", inset=0)

# =====================================================================
# 2. Executive summary
# =====================================================================
s = d.new_slide("exec summary")
header(s, "Executive summary",
       "Do not discontinue C in 2027: exiting would destroy cash and breach board constraints. "
       "Redesign C, fix bundle service, and make any sunset a 2029 decision")
rows = [
    ("A", "C's 8% margin comes from the cost allocation; C is actually the portfolio's highest-contribution connector",
     ["C earns $3.8M direct contribution, a 63% contribution margin vs 50% for D, 50% for A and 42% for B",
      "Only $0.4M of C's $3.3M allocated cost is avoidable; the other $2.9M would move onto A, B and D"]),
    ("B", "Exiting C in 2027 loses $4.75M in the first year and $2.65M every year after, and breaks two non-negotiables",
     ["Even if D wins the optimistic 25% of C revenue, D adds only $0.75M; break-even would need $6.8M of D sales (113% of C)",
      "The $2.1M penalty alone is 2.3x the $0.9M cash envelope; C sits in 9 of 14 major bundles with no validated substitute"]),
    ("C", "The customer case for exit does not hold up: the real problem is bundle fill, caused by A and B",
     ["The 9-point renewal gap is confounded by hospital size, legacy equipment and customer-success coverage; there is no before/after test",
      "C's 98% on-time figure leaves out bundle misses caused by A and B. Bundle fill is 91% vs the 95% contracted, and exiting C would not fix it"]),
    ("D", "Recommended: redesign C now (+$2.4M over 2027–29), recover bundle fill, then hand the team to D",
     ["The $0.55M redesign pays back in ~5 months of savings and still breaks even at 19% of the $1.25M estimate; it fits within the $0.9M",
      "Renew the two bundles without exit notice and with a consent-based D path; hold a Q4 2028 gate on a 2029 sunset"]),
]
y0, rh = 1.68, 1.28
for i, (k, head, buls) in enumerate(rows):
    yy = y0 + i * rh
    s.rect(LM, yy, 0.42, rh - 0.14, fill=NAVY)
    s.text(LM, yy, 0.42, rh - 0.14, k, size=18, color="FFFFFF", bold=True, align="c", anchor="m", inset=0)
    s.text(LM + 0.55, yy, 4.35, rh - 0.14, head, size=12.5, color=NAVY, bold=True, anchor="m", inset=0.02)
    s.text(LM + 5.1, yy, 7.2, rh - 0.14, [{"text": b, "bullet": True} for b in buls], size=11, color=INK,
           anchor="m", inset=0.02)
    if i < 3:
        s.line(LM + 0.55, yy + rh - 0.07, LM + CW, yy + rh - 0.07, color=RULE, lw=0.5)
footer(s, "Sections A–D of this deck follow these four points.")

# =====================================================================
# 3. Hypothesis test
# =====================================================================
s = d.new_slide("hypothesis")
header(s, "Approach: hypothesis test",
       "Our starting hypothesis, \"keep C\", survived four of five tests; the fifth showed that keeping C "
       "unchanged is not enough")
s.text(LM, 1.62, CW, 0.34,
       [{"runs": [("Initial hypothesis (set before testing): ", {"bold": True, "color": NAVY}),
                  ("Vesper should retain C, because its low reported margin is an allocation effect rather than an avoidable economic cost.", {})]}],
       size=11.5, inset=0)
cols = [(LM, 0.35, "#"), (LM + 0.35, 3.4, "What would have to be true"), (LM + 3.8, 6.55, "Test against the briefing-pack evidence"),
        (LM + 10.45, 1.88, "Verdict")]
ty = 2.08
for (cx, cw, lab) in cols:
    s.text(cx, ty, cw, 0.3, lab, size=10, color=INK2, bold=True, inset=0.02)
s.line(LM, ty + 0.32, LM + CW, ty + 0.32, color=NAVY, lw=0.75)
tests = [
    ("1", "C earns more cash than its exit would save",
     "C direct contribution $3.8M vs avoidable fixed cost $0.4M, so exit gives up a net $3.4M a year before any migration", "Holds", BLUE),
    ("2", "D cannot replace what C earns",
     "Migration ceiling 25% of C revenue = $1.5M (all of D's spare capacity) x 50% = $0.75M, vs $3.4M at stake", "Holds", BLUE),
    ("3", "Exit costs and constraints bind",
     "$2.1M first-year penalties vs $0.9M approved cash; C sits in 9 of 14 major bundles and no substitute is validated across every hospital model", "Holds", BLUE),
    ("4", "C is not driving customer attrition",
     "The 9-point renewal gap is correlational and confounded (size, legacy equipment, CS coverage); there is no before/after evidence either way", "Unproven", AMBER),
    ("5", "Retaining C as-is is acceptable",
     "Bundle fill is 91% vs 95% required; C faces price pressure; a $1.25M a year redesign saving is available for $0.55M", "Fails: refine", RED),
]
rh = 0.66
for i, (n, cond, ev, ver, col) in enumerate(tests):
    yy = ty + 0.4 + i * rh
    s.text(LM, yy, 0.35, rh - 0.06, n, size=13, color=NAVY, bold=True, anchor="m", inset=0.02)
    s.text(LM + 0.35, yy, 3.35, rh - 0.06, cond, size=11, color=INK, bold=True, anchor="m", inset=0.02)
    s.text(LM + 3.8, yy, 6.5, rh - 0.06, ev, size=10.5, color=INK, anchor="m", inset=0.02)
    pill(s, LM + 10.5, yy + (rh - 0.06 - 0.26) / 2, 1.45, ver, col)
    s.line(LM, yy + rh - 0.02, LM + CW, yy + rh - 0.02, color=RULE, lw=0.5)
s.text(LM, 5.88, CW, 0.92,
       [{"runs": [("Revised answer: ", {"bold": True, "color": "FFFFFF"}),
                  ("Keep C, but not unchanged. Fund the C redesign, bring bundle fill back to 95%, use the renewals to open a consent-based path to D, "
                   "and treat a 2029 sunset as a decision for Q4 2028, made on observed evidence. Test 4 stays open, and the plan includes a way to resolve it.",
                   {"color": "FFFFFF"})]}],
       size=11.5, fill=NAVY, inset=0.15, anchor="m")
footer(s, "Verdict colours carry labels; blue = supports hypothesis, amber = evidence inconclusive, red = hypothesis needs refining.")

# =====================================================================
# 4. Margin walk for C
# =====================================================================
s = d.new_slide("margin walk")
header(s, "A  |  Is C really unprofitable?",
       "C's 8% \"gross margin\" comes from the allocation: C earns $3.8M of direct contribution, and only $0.4M "
       "of its $3.3M allocated cost would go away if C exits")
s.text(LM, 1.62, 7.6, 0.3, "Connector C, FY2026, $M: walk from sales to reported profit", size=11, bold=True, color=INK, inset=0)
items = [("Sales", 6.0, "total"), ("Direct variable cost", -2.2, "delta"), ("Direct contribution", 3.8, "sub"),
         ("Avoidable fixed cost", -0.4, "delta"), ("Profit lost if C exits", 3.4, "sub"),
         ("Shared cost that stays (reallocated)", -2.9, "delta"), ("Reported profit", 0.5, "total")]
Y = waterfall(s, LM + 0.1, 2.15, 7.6, 4.2, items, 0, 6.6, label_h=0.62, fmt=lambda v: f"{v:+.1f}", tfmt="{:.1f}")
# brackets / annotations
s.text(LM + 0.1 + 2 * 7.6 / 7 - 0.2, 6.42, 7.6 / 7 + 0.4, 0.3, "63% of sales", size=9.5, color=BLUE, bold=True, align="c", inset=0)
s.text(LM + 0.1 + 6 * 7.6 / 7 - 0.2, 6.42, 7.6 / 7 + 0.4, 0.3, "8.3% of sales", size=9.5, color=RED, bold=True, align="c", inset=0)
# right panel
px0 = LM + 8.1
s.rect(px0, 1.62, 4.23, 5.2, fill=PANEL)
s.text(px0 + 0.15, 1.72, 3.95, 5.0, [
    {"text": "What the walk shows", "bold": True, "color": NAVY, "size": 12},
    {"runs": [("Two different margins. ", {"bold": True}),
              ("Reported margin = (6.0 – 2.2 – 3.3) / 6.0 = 8.3%. Contribution margin = 3.8 / 6.0 = 63.3%.", {})], "bullet": True},
    {"runs": [("88% of the allocation stays. ", {"bold": True}),
              ("$2.9M of the $3.3M is shared regulatory documentation and plant depreciation, spread by historical "
               "engineering hours. It does not go away when the SKU does.", {})], "bullet": True},
    {"runs": [("Exit decisions turn on $3.4M. ", {"bold": True}),
              ("Exiting C removes $3.8M of contribution and saves $0.4M of fixed cost, so Vesper loses $3.4M a year before any migration to D.", {})], "bullet": True},
    {"runs": [("The dashboard label misleads. ", {"bold": True}),
              ("The figure called \"product gross margin\" is measured after shared allocations, so it cannot be used to rank products for an exit or capacity decision.", {})], "bullet": True},
], size=10.5, inset=0.02)
s.text(px0 + 0.15, 5.55, 3.93, 1.12, [{"text": "Decision-relevant figure", "size": 10, "bold": True, "color": "FFFFFF"},
       {"text": "$3.4M a year of profit lost on exit, not 8%", "size": 15, "bold": True, "color": "FFFFFF"}],
       fill=NAVY, inset=0.14, anchor="m")
footer(s, "Avoidable fixed cost of $0.40M per Finance; direct variable cost is fully avoidable if shipments end.")

# =====================================================================
# 5. Product comparison + reallocation
# =====================================================================
s = d.new_slide("product comparison")
header(s, "A  |  Is C really unprofitable?",
       "On contribution, C is Vesper's strongest connector (63% vs D's 50%), and exiting it would move "
       "$2.9M of stranded cost onto A, B and D")
s.text(LM, 1.62, 6.3, 0.3, "Margin by product, FY2026, % of sales", size=11, bold=True, color=INK, inset=0)
# legend
s.rect(LM, 2.02, 0.16, 0.16, fill=GREY_BAR)
s.text(LM + 0.22, 1.96, 2.6, 0.28, "Reported margin (after allocations)", size=9.5, color=INK2, inset=0)
s.rect(LM + 2.95, 2.02, 0.16, 0.16, fill=BLUE)
s.text(LM + 3.17, 1.96, 2.8, 0.28, "Direct contribution margin", size=9.5, color=INK2, inset=0)
prods = [("A", 41.4, 50.0, "$14.0M"), ("B", 28.9, 42.2, "$9.0M"), ("C", 8.3, 63.3, "$6.0M"), ("D", 30.0, 50.0, "$4.0M")]
cx0, cy0, cw_, ch_ = LM + 0.1, 2.5, 6.0, 3.6
slot = cw_ / 4
vmax = 70.0
for i, (p, rep, con, sales) in enumerate(prods):
    bx = cx0 + i * slot + 0.25
    bw = (slot - 0.5) / 2 - 0.02
    for j, (v, col) in enumerate([(rep, GREY_BAR), (con, BLUE)]):
        xx = bx + j * (bw + 0.04)
        top = cy0 + ch_ * (1 - v / vmax)
        s.rect(xx, top, bw, cy0 + ch_ - top, fill=col)
        s.text(xx - 0.15, top - 0.28, bw + 0.3, 0.26, f"{v:.0f}%" if v >= 10 else f"{v:.1f}%", size=10.5, bold=True,
               color=INK, align="c", inset=0)
    s.text(cx0 + i * slot, cy0 + ch_ + 0.06, slot, 0.26, f"Connector {p}", size=10.5, bold=True,
           color=NAVY if p == "C" else INK, align="c", inset=0)
    s.text(cx0 + i * slot, cy0 + ch_ + 0.3, slot, 0.24, f"sales {sales}", size=9, color=MUTED, align="c", inset=0)
s.line(cx0, cy0 + ch_, cx0 + cw_, cy0 + ch_, color=INK2, lw=0.75)
s.rect(cx0 + 2 * slot + 0.08, cy0 - 0.15, slot - 0.16, ch_ + 0.73, line=NAVY, lw=1.0, dash=True)
# right: reallocation table
rx = LM + 6.75
s.text(rx, 1.62, 5.6, 0.3, "If C exits: illustrative reported margins once $2.9M is reallocated", size=11, bold=True, color=INK, inset=0)
hdr = ["Product", "Allocated cost, $M\ntoday → after exit", "Reported margin\ntoday → after exit"]
cws = [1.55, 2.0, 2.03]
yy = 2.05
xx = rx
for h_, w_ in zip(hdr, cws):
    s.text(xx, yy, w_, 0.5, [{"text": t, "space_after": 0} for t in h_.split("\n")], size=9.5, bold=True, color=INK2, inset=0.03, anchor="b")
    xx += w_
s.line(rx, yy + 0.54, rx + sum(cws), yy + 0.54, color=NAVY, lw=0.75)
rows_ = [("A", "1.20 → 2.29", "41.4% → 33.7%"), ("B", "1.20 → 2.29", "28.9% → 16.8%"),
         ("D (with 25%\nC migration)", "0.80 → 1.53", "30.0% → 22.3%"), ("Total", "3.20 → 6.10", "")]
for i, r in enumerate(rows_):
    y_ = yy + 0.6 + i * 0.5
    xx = rx
    for j, (v, w_) in enumerate(zip(r, cws)):
        s.text(xx, y_, w_, 0.46, v.split("\n") if "\n" in v else v, size=10.5 if j else 10.5,
               bold=(j == 0 or (j == 2 and r[0] == "B")), color=RED if (j == 2 and r[0] == "B") else INK,
               inset=0.03, anchor="m")
        xx += w_
    s.line(rx, y_ + 0.48, rx + sum(cws), y_ + 0.48, color=RULE, lw=0.5)
s.text(rx, 4.75, 5.6, 2.05, [
    {"runs": [("Implication: ", {"bold": True, "color": NAVY}),
              ("the stranded cost does not go away when C does; it lands on A, B and D. B's reported margin would fall to about 17%, and the same "
               "margin-ranking logic would then pick B as the next \"weakest\" product. Total allocated cost falls by only $0.4M (from 6.5 to 6.1).", {})]},
    {"text": "Allocation basis: the pack says the remaining cost \"would move to A, B and D\" but does not give the split. We assume it moves pro rata to today's "
             "allocation (1.2 : 1.2 : 0.8). D's figure includes $1.5M of migrated revenue at 50% contribution.", "size": 9, "color": MUTED},
], size=10.5, inset=0.02)
footer(s, "Contribution margin = (sales – direct variable cost) / sales. Reported margin = (sales – variable – allocated) / sales.")

# =====================================================================
# 6. Exit bridge
# =====================================================================
s = d.new_slide("exit bridge")
header(s, "B  |  What would exiting C cost?",
       "Exiting C cuts cash contribution by $4.75M in its first year and $2.65M every year after, even if D wins "
       "the optimistic 25% of C revenue")
s.text(LM, 1.62, 7.7, 0.3, "Exit bridge vs retaining C, first 12 months after exit, $M", size=11, bold=True, color=INK, inset=0)
items = [("C direct contribution lost", -3.8, "delta"), ("Avoidable fixed cost saved", 0.4, "delta"),
         ("D migration at ceiling (25% x $6.0M x 50%)", 0.75, "delta"), ("Recurring annual impact", -2.65, "sub"),
         ("First-year bundle penalties (one-time)", -2.1, "delta"), ("First-year impact", -4.75, "total")]
waterfall(s, LM + 0.1, 2.25, 7.7, 4.3, items, -5.3, 0.6, label_h=0.75, fmt=lambda v: f"{v:+.2f}")
px0 = LM + 8.2
s.rect(px0, 1.62, 4.13, 5.2, fill=PANEL)
s.text(px0 + 0.15, 1.72, 3.85, 0.3, "Operating profit after allocations, $M a year", size=10.5, bold=True, color=NAVY, inset=0)
tiles = [("Today (FY2026)", "10.10", "", INK), ("Exit C, 25% migration", "7.45", "–26%", RED), ("Exit C, no migration", "6.70", "–34%", RED)]
for i, (lab, v, dlt, col) in enumerate(tiles):
    yy = 2.12 + i * 0.68
    s.text(px0 + 0.15, yy, 2.25, 0.6, lab, size=10.5, color=INK2, anchor="m", inset=0)
    s.text(px0 + 2.35, yy, 0.95, 0.6, v, size=18, bold=True, color=INK, anchor="m", align="r", inset=0)
    s.text(px0 + 3.3, yy, 0.7, 0.6, dlt, size=11, bold=True, color=col, anchor="m", align="r", inset=0)
s.line(px0 + 0.15, 4.2, px0 + 3.98, 4.2, color=RULE, lw=0.5)
s.text(px0 + 0.15, 4.28, 3.85, 2.5, [
    {"runs": [("Penalties are one-time. ", {"bold": True}),
              ("Following Finance, the $2.1M is treated as a first-year cost, not recurring overhead. Even with every penalty waived, exit still loses $2.65M a year.", {})], "bullet": True},
    {"runs": [("Migration is a ceiling, not a forecast. ", {"bold": True}),
              ("The 25% comes from three sales interviews. It needs customer-specific adapters and validation.", {})], "bullet": True},
    {"runs": [("Not yet costed: ", {"bold": True}),
              ("replacement qualification, clinical documentation, and any A/B accounts lost with the bundle.", {})], "bullet": True},
], size=10, inset=0.02)
footer(s, "Operating profit = total contribution 16.6 – allocated fixed 6.5. Exit case: contribution 16.6 – 3.8 + 0.75; fixed 6.5 – 0.4.")

# =====================================================================
# 7. Migration sensitivity / break-even
# =====================================================================
s = d.new_slide("break-even")
header(s, "B  |  What would exiting C cost?",
       "No migration rate makes exit pay: even if every C customer moved to D, Vesper would still lose $0.4M "
       "a year, and D can take only 25% today")
s.text(LM, 1.62, 7.7, 0.3, "Recurring annual impact of exit, by share of C revenue migrating to D, $M", size=11, bold=True, color=INK, inset=0)
s.text(LM, 1.9, 7.7, 0.28, "Impact = –3.8 + 0.4 + (share x $6.0M x 50%)", size=9.5, color=INK2, inset=0)
shares = [(0, -3.40), (25, -2.65), (50, -1.90), (75, -1.15), (100, -0.40)]
gx, gy, gw, gh = LM + 0.6, 2.45, 7.0, 3.55
vmin, vmax = -4.0, 0.5
def Yv(v): return gy + (vmax - v) / (vmax - vmin) * gh
slot = gw / 5
for i, (sh, v) in enumerate(shares):
    bx = gx + i * slot + slot * 0.22
    bw = slot * 0.56
    within = sh <= 25
    col = RED_BAR if within else "F2B8B8"
    s.rect(bx, Yv(0), bw, Yv(v) - Yv(0), fill=col, line=None if within else RED_BAR, lw=0.75, dash=not within)
    s.text(bx - 0.2, Yv(v) + 0.04, bw + 0.4, 0.26, f"–{abs(v):.2f}", size=11, bold=True, color=INK, align="c", inset=0)
    s.text(gx + i * slot, gy - 0.02, slot, 0.26, f"{sh}%", size=11, bold=True, color=INK, align="c", inset=0)
    s.text(gx + i * slot, gy + 0.2, slot, 0.26, f"${sh * 0.06:.1f}M of D sales", size=9, color=MUTED, align="c", inset=0)
s.line(gx, Yv(0), gx + gw, Yv(0), color=INK2, lw=0.75)
# axis ticks
for t in [0, -1, -2, -3, -4]:
    s.text(gx - 0.55, Yv(t) - 0.12, 0.45, 0.24, f"{t:.0f}".replace("-", "–"), size=9, color=MUTED, align="r", inset=0)
    if t != 0:
        s.line(gx, Yv(t), gx + gw, Yv(t), color="E6E5E1", lw=0.5)
s.text(gx, 6.12, 1.6 * slot, 0.5, "Within D's current spare capacity ($1.5M)", size=9, color=INK2, align="c", inset=0)
s.text(gx + 2.0 * slot, 6.12, 3.0 * slot, 0.5, "Above D's current capacity: needs new D capacity and a validated adapter at every account",
       size=9, color=INK2, align="c", inset=0)
s.line(gx + 2 * slot - 0.1, 2.5, gx + 2 * slot - 0.1, 6.5, color=MUTED, lw=0.75, dash=True)
px0 = LM + 8.2
s.rect(px0, 1.62, 4.13, 5.2, fill=PANEL)
s.text(px0 + 0.15, 1.75, 3.85, 0.3, "Break-even requires the impossible", size=12, bold=True, color=NAVY, inset=0)
s.text(px0 + 0.15, 2.12, 3.85, 0.75, "$6.8M", size=34, bold=True, color=RED, inset=0, anchor="m")
s.text(px0 + 0.15, 2.88, 3.85, 0.7, "of migrated D revenue needed to offset the $3.4M lost each year "
       "($3.4M ÷ 50%). That is 113% of C's entire $6.0M revenue and 4.5x D's spare capacity.", size=10.5, color=INK, inset=0)
s.line(px0 + 0.15, 3.85, px0 + 3.98, 3.85, color=RULE, lw=0.5)
s.text(px0 + 0.15, 3.95, 3.85, 2.8, [
    {"runs": [("Why D cannot close the gap: ", {"bold": True}),
              ("C's contribution margin (63%) is higher than D's incremental 50%, so each dollar moved from C to D earns less.", {})], "bullet": True},
    {"runs": [("Migration crowds out D growth: ", {"bold": True}),
              ("the 25% ceiling would use all of D's $1.5M spare capacity, leaving no room for D's own organic growth.", {})], "bullet": True},
    {"runs": [("The 25% is unobserved: ", {"bold": True}),
              ("it is the portfolio team's ceiling from three interviews. Finance has not estimated any recapture beyond it.", {})], "bullet": True},
], size=10, inset=0.02)
footer(s, "Bars beyond 25% (light, dashed) are hypothetical and exceed D's current capacity. Excludes the one-time $2.1M penalty.")

# =====================================================================
# 8. Constraints check
# =====================================================================
s = d.new_slide("constraints")
header(s, "B  |  What would exiting C cost?",
       "A 2027 exit would also break the board's non-negotiables: the penalty alone is 2.3x the approved cash, "
       "and C is in 9 of 14 major hospital bundles")
cws = [2.6, 6.55, 1.55, 1.63]
hdr = ["Board requirement", "What a Q2 2027 exit of C would do", "Status", "Gap"]
x_ = LM
for h_, w_ in zip(hdr, cws):
    s.text(x_, 1.65, w_, 0.3, h_, size=10, bold=True, color=INK2, inset=0.03)
    x_ += w_
s.line(LM, 1.98, LM + CW, 1.98, color=NAVY, lw=0.75)
crow = [
    ("≥95% contracted bundle fill rate",
     "9 of 14 major hospital relationships specify a bundle containing C alongside A and B. No substitute for C has completed validation across every "
     "hospital model, so removing C leaves those bundles incomplete. Fill is already 91%.", "Fails", RED, "Already –4 pts; would worsen"),
    ("≤$0.9M one-time cash for 2027 portfolio changes",
     "First-year bundle penalties of $2.1M are payable unless counterparties consent. Replacement qualification and clinical documentation "
     "come on top and have not been costed.", "Fails", RED, "≥$1.2M over (2.3x)"),
    ("Honour customer commitments",
     "Exit requires notice, replacement qualification and clinical documentation. Two bundle agreements are being renewed now, so an exit "
     "notice would go into live negotiations.", "Fails", RED, "Consent of 9 bundle customers needed"),
    ("Judge on cash contribution, not the allocation report",
     "Cash contribution falls by $3.4M a year before migration and $2.65M after the 25% ceiling, plus the $2.1M penalty in year one.",
     "Fails", RED, "–$4.75M yr 1; –$2.65M a year after"),
]
rh = 1.05
for i, (req, what, st, col, gap) in enumerate(crow):
    yy = 2.06 + i * rh
    s.text(LM, yy, cws[0], rh - 0.08, req, size=11, bold=True, color=NAVY, anchor="m", inset=0.03)
    s.text(LM + cws[0], yy, cws[1], rh - 0.08, what, size=10.5, color=INK, anchor="m", inset=0.05)
    pill(s, LM + cws[0] + cws[1] + 0.15, yy + (rh - 0.08 - 0.26) / 2, 1.2, st, col)
    s.text(LM + cws[0] + cws[1] + cws[2], yy, cws[3], rh - 0.08, gap, size=10, bold=True, color=RED, anchor="m", inset=0.03)
    s.line(LM, yy + rh - 0.03, LM + CW, yy + rh - 0.03, color=RULE, lw=0.5)
s.text(LM, 6.32, CW, 0.5,
       [{"runs": [("Implication: ", {"bold": True, "color": NAVY}),
                  ("a 2027 exit cannot go ahead without the board relaxing at least two of its own constraints. No other option on the table requires that (see page 12).", {})]}],
       size=11, inset=0.02, anchor="m")
footer(s, "Assumes the $2.1M penalty counts against the 2027 one-time cash envelope because it is a direct cash consequence of the portfolio change.")

# =====================================================================
# 9. Redeploy to D
# =====================================================================
s = d.new_slide("redeploy to D")
header(s, "B  |  What would exiting C cost?",
       "Moving the team to D cannot replace C: D's spare capacity caps the upside at $0.75M a year, "
       "and Vesper can capture that without exiting C")
s.text(LM, 1.62, 6.0, 0.3, "Annual cash contribution, $M", size=11, bold=True, color=INK, inset=0)
bars = [("C profit lost on exit\n(contribution – avoidable fixed)", 3.4, NAVY),
        ("Most D can add at present capacity\n($1.5M revenue x 50%)", 0.75, BLUE)]
bx0, by0, bwid = LM + 2.75, 2.2, 3.2
for i, (lab, v, col) in enumerate(bars):
    yy = by0 + i * 0.95
    s.text(LM, yy, 2.65, 0.7, lab.split("\n"), size=10, color=INK, inset=0, anchor="m")
    s.rect(bx0, yy + 0.12, bwid * v / 3.4, 0.46, fill=col)
    s.text(bx0 + bwid * v / 3.4 + 0.08, yy + 0.12, 0.8, 0.46, f"{v:.2f}", size=12, bold=True, color=INK, anchor="m", inset=0)
s.line(bx0, by0, bx0, by0 + 1.85, color=INK2, lw=0.75)
s.text(LM, 4.2, 6.1, 0.4, "C's economics are 4.5x the most D can add without new capacity", size=11, bold=True, color=NAVY, inset=0)
s.text(LM, 4.6, 6.1, 2.2, [
    {"runs": [("D's \"30% margin\" is also after allocations. ", {"bold": True}),
              ("D's incremental contribution at existing capacity is 50%, still below C's 63%.", {})], "bullet": True},
    {"runs": [("Growth is not replacement. ", {"bold": True}),
              ("D's double-digit market growth adds value at the margin. It does not justify giving up $3.8M of existing contribution (Finance's point).", {})], "bullet": True},
], size=10.5, inset=0.02)
px0 = LM + 6.6
s.rect(px0, 1.62, 5.73, 5.2, fill=PANEL)
s.text(px0 + 0.18, 1.74, 5.4, 0.3, "Engineering capacity: what we know and what we don't", size=12, bold=True, color=NAVY, inset=0)
s.text(px0 + 0.18, 2.12, 5.4, 4.6, [
    {"runs": [("Known: ", {"bold": True}),
              ("D has room for $1.5M more revenue at present capacity. That room exists whether or not C exits. Under an exit, migrating C customers would "
               "fill it, crowding out D's own growth.", {})], "bullet": True},
    {"runs": [("Known: ", {"bold": True}),
              ("the C redesign needs one design team for about four months (validation phase), then hands the team back.", {})], "bullet": True},
    {"runs": [("Not known: ", {"bold": True}),
              ("the pack gives no quantified opportunity cost for those four months, and we do not invent one.", {})], "bullet": True},
    {"runs": [("Illustrative ceiling only: ", {"bold": True}),
              ("suppose the team's absence delayed filling D's spare capacity by the full four months. The cost would then be at most "
               "4/12 x $0.75M ≈ $0.25M, against $1.25M a year of redesign savings.", {})], "bullet": True},
    {"runs": [("Answer to \"redeploy to D?\": ", {"bold": True, "color": BLUE}),
              ("yes, but in sequence. The team works on the C redesign from March to June 2027 and moves to D (adapter validation and growth) from July.", {})], "bullet": True},
], size=10.5, inset=0.02)
footer(s, "The $0.25M is a bound under a stated assumption, not an estimate of lost D sales.")

# =====================================================================
# 10. Correlation claim
# =====================================================================
s = d.new_slide("correlation")
header(s, "C  |  Is C hurting customers?",
       "The 9-point renewal gap does not show C causes churn: C buyers are smaller, legacy-equipment, "
       "lower-coverage accounts, and nothing tests what removing C would do")
# causal diagram
s.text(LM, 1.62, 6.6, 0.3, "The CEO's claim and the factors it does not control for", size=11, bold=True, color=INK, inset=0)
def box(x, y, w, h, t, fill, col="FFFFFF", sz=10.5, b=True):
    s.text(x, y, w, h, t, size=sz, color=col, bold=b, fill=fill, align="c", anchor="m", inset=0.06)
box(LM + 0.1, 3.55, 1.9, 0.75, "Account buys C", NAVY)
box(LM + 4.5, 3.55, 2.1, 0.75, "Renews 9 pts less often", NAVY)
s.line(LM + 2.0, 3.92, LM + 4.5, 3.92, color=RED, lw=1.5, dash=True, arrow=True)
s.text(LM + 2.0, 3.6, 2.5, 0.3, "Claimed: C causes it", size=9.5, color=RED, bold=True, align="c", inset=0)
box(LM + 0.1, 2.1, 2.9, 0.62, "Smaller hospitals on legacy equipment", "E6E5E1", INK, 10)
box(LM + 3.6, 2.1, 3.0, 0.62, "Lower customer-success coverage", "E6E5E1", INK, 10)
box(LM + 1.75, 5.1, 3.2, 0.72, "Bundle fill 91%, caused by A/B misses (our hypothesis, untested)", "F8E7C5", INK, 9.5)
for (x1, y1, x2, y2) in [(LM + 1.0, 2.72, LM + 1.0, 3.55), (LM + 2.6, 2.72, LM + 5.0, 3.55),
                         (LM + 4.4, 2.72, LM + 1.6, 3.55), (LM + 5.6, 2.72, LM + 5.6, 3.55),
                         (LM + 3.6, 5.1, LM + 5.3, 4.3)]:
    s.line(x1, y1, x2, y2, color=INK2, lw=1.0, arrow=True)
s.text(LM, 6.0, 6.6, 0.8, "Grey boxes: confounders named in the briefing pack. Amber: a further plausible confounder. The 9 C-bundle customers are the ones "
       "receiving 91% fill, but the pack does not link this to renewals.", size=9, color=MUTED, inset=0)
px0 = LM + 7.0
s.rect(px0, 1.62, 5.33, 5.2, fill=PANEL)
s.text(px0 + 0.18, 1.74, 5.0, 0.3, "Verdict and the test the board should require", size=12, bold=True, color=NAVY, inset=0)
s.text(px0 + 0.18, 2.1, 5.0, 4.65, [
    {"runs": [("Correlation, not causation. ", {"bold": True}),
              ("C accounts differ systematically in size, equipment age and service coverage. Each of these could lower renewal on its own.", {})], "bullet": True},
    {"runs": [("No counterfactual. ", {"bold": True}),
              ("The sample has no before/after evidence that removing C raises retention. It cannot support exit, and it cannot rule out a C effect either.", {})], "bullet": True},
    {"text": "Tests to run before the Q4 2028 gate:", "bold": True, "color": NAVY},
    {"text": "Compare renewal within matched segments (size x equipment age x CS coverage)", "bullet": True, "indent": 0.15},
    {"text": "Control for bundle fill each account actually received", "bullet": True, "indent": 0.15},
    {"text": "Code lost-account exit reasons for any mention of C", "bullet": True, "indent": 0.15},
    {"text": "Track retention of any accounts that drop C or move to D", "bullet": True, "indent": 0.15},
    {"runs": [("Decision rule: ", {"bold": True}),
              ("only a renewal gap that persists within segments should feed the sunset decision, and then it should be valued against the $3.4M a year C contributes.", {})]},
], size=10.5, inset=0.02)
footer(s)

# =====================================================================
# 11. Fill-rate definition
# =====================================================================
s = d.new_slide("fill rate")
header(s, "C  |  Is C hurting customers?",
       "The real service problem is bundle fill, at 91% against 95% contracted; A and B misses cause it and the C dashboard "
       "hides it, so exiting C would not fix it")
s.text(LM, 1.62, 7.4, 0.3, "Two fill-rate measures, %", size=11, bold=True, color=INK, inset=0)
gx, gy, gw = LM + 2.9, 2.35, 4.6
vmin, vmax = 85.0, 100.0
def X(v): return gx + (v - vmin) / (vmax - vmin) * gw
rowsf = [("C on-time fill\n(service dashboard)", 98, BLUE, "Excludes late bundles when A or B is the missing item"),
         ("Contracted bundle fill\n(actual)", 91, RED_BAR, "What hospital contracts measure")]
for t in [85, 90, 95, 100]:
    s.line(X(t), gy - 0.1, X(t), gy + 2.0, color="E6E5E1" if t != 95 else NAVY, lw=0.5 if t != 95 else 1.25, dash=(t == 95))
    s.text(X(t) - 0.3, gy + 2.05, 0.6, 0.25, f"{t}%", size=9, color=MUTED, align="c", inset=0)
s.text(X(95) - 0.9, gy - 0.42, 1.8, 0.28, "Contract minimum 95%", size=9.5, bold=True, color=NAVY, align="c", inset=0)
for i, (lab, v, col, note) in enumerate(rowsf):
    yy = gy + 0.25 + i * 0.95
    s.text(LM, yy - 0.05, 2.8, 0.6, lab.split("\n"), size=10.5, color=INK, bold=False, inset=0, anchor="m")
    s.line(gx, yy + 0.25, X(v), yy + 0.25, color=RULE, lw=1.0)
    s.oval(X(v) - 0.11, yy + 0.14, 0.22, col)
    s.text(X(v) + 0.17, yy + 0.08, 0.6, 0.34, f"{v}%", size=13, bold=True, color=INK, inset=0)
s.text(X(91), gy + 1.62, X(95) - X(91), 0.3, "–4 pts", size=10, bold=True, color=RED, align="c", inset=0)
s.line(X(91), gy + 1.6, X(95), gy + 1.6, color=RED, lw=1.0)
s.text(LM, 4.9, 7.4, 0.3, "Note: axis starts at 85% to show the gap; values are labelled.", size=8.5, color=MUTED, inset=0)
s.text(LM, 5.25, 7.4, 1.6, [
    {"runs": [("The dashboard definition: ", {"bold": True}),
              ("C's 98% counts C as filled even when the bundle ships late because A or B is missing. The contract measures complete bundles, and that "
               "figure is 91%.", {})], "bullet": True},
    {"runs": [("The cause sits in A and B, ", {"bold": True}),
              ("not C. Exiting C leaves the A/B misses in place and makes the nine C-bundles incomplete.", {})], "bullet": True},
], size=10.5, inset=0.02)
px0 = LM + 7.9
s.rect(px0, 1.62, 4.43, 5.2, fill=PANEL)
s.text(px0 + 0.18, 1.74, 4.1, 0.3, "Fix the measure and the misses, not C", size=12, bold=True, color=NAVY, inset=0)
s.text(px0 + 0.18, 2.1, 4.1, 4.6, [
    {"runs": [("Redefine the KPI: ", {"bold": True}),
              ("make bundle-level contracted fill the headline service metric for every bundle customer. Report product-level fill only as a diagnostic.", {})], "bullet": True},
    {"runs": [("Root-cause the A and B misses ", {"bold": True}),
              ("on the nine bundle accounts. Size buffer stock or allocation priority for A and B in those bundles.", {})], "bullet": True},
    {"runs": [("Report monthly to the board ", {"bold": True}),
              ("until fill has stayed at 95% or above for two consecutive quarters.", {})], "bullet": True},
    {"runs": [("Unknown: recovery speed. ", {"bold": True}),
              ("The pack does not say how fast bundle service can recover or what that costs. We have set a Q3 2027 target as a working assumption "
               "for Operations to confirm in February.", {})], "bullet": True},
], size=10.5, inset=0.02)
footer(s)

# =====================================================================
# 12. Options comparison
# =====================================================================
s = d.new_slide("options")
header(s, "D  |  What should Vesper do instead?",
       "Redesigning C is the only option that adds value and meets every constraint: +$2.4M over 2027–29, "
       "against –$8.7M for an immediate exit")
cws = [2.35, 2.5, 2.4, 2.48, 2.6]
opts = ["Exit C in Q2 2027", "Retain C unchanged", "Delayed sunset in 2029\n(no redesign)", "Redesign C now,\n2029 sunset gate"]
x_ = LM + cws[0]
s.rect(LM + sum(cws[:4]), 1.58, cws[4], 5.3, fill="EAF2FC")
for j, (o, w_) in enumerate(zip(opts, cws[1:])):
    s.text(x_, 1.6, w_, 0.5, o.split("\n"), size=10.5, bold=True, color=BLUE if j == 3 else NAVY, align="c", anchor="m", inset=0.03)
    x_ += w_
s.text(LM + sum(cws[:4]), 1.6 - 0.02, cws[4], 0.2, "", size=6)
s.line(LM, 2.13, LM + CW, 2.13, color=NAVY, lw=0.75)
R = [
    ("Cash contribution vs retain unchanged, $M", None),
    ("2027", ["–3.43", "0", "0", "–0.13"]),
    ("2028", ["–2.65", "0", "0", "+1.25"]),
    ("2029", ["–2.65", "0", "0", "+1.25"]),
    ("Cumulative 2027–29", ["–8.73\n(–10.6 with no migration)", "0", "0\n(–2.65 to –3.4 a year from 2030)", "+2.37\n(downside +0.40)"]),
    ("One-time cash vs $0.9M", ["≥$2.1M penalties + qualification: fails", "$0: meets", "$0 if exits match expiries: meets", "$0.55M + $0.35M reserve: meets"]),
    ("95% bundle fill", ["Worsens: no validated substitute", "Needs A/B fix", "Needs A/B fix; time to validate adapter", "Needs A/B fix (in plan)"]),
    ("Customer commitments", ["Penalties unless 9 customers consent", "Honoured", "Honoured; exit only at expiry", "Honoured; renewals add D path"]),
    ("Main risk", ["A/B bundle volume at risk (unquantified); B next 'weakest'", "Price pressure erodes C; $1.25M saving forgone", "As retain; locks in high-cost C until 2029", "Requalification delay at 2 customers; savings below estimate"]),
]
yy = 2.18
for lab, vals in R:
    if vals is None:
        s.text(LM, yy, CW, 0.26, lab, size=9.5, bold=True, color=INK2, inset=0.03)
        yy += 0.28
        continue
    big = lab.startswith("Cumulative")
    multi = any("\n" in v for v in vals) or len(max(vals, key=len)) > 22
    h_ = 0.34 if not multi else (0.62 if big else 0.6)
    s.text(LM, yy, cws[0], h_, lab, size=10, bold=True, color=NAVY if not lab.isdigit() else INK, anchor="m", inset=0.03)
    x_ = LM + cws[0]
    for j, (v, w_) in enumerate(zip(vals, cws[1:])):
        neg = v.startswith("–") and v != "0"
        col = RED if (neg and lab[0].isdigit()) or (big and j == 0) else (BLUE if (big and j == 3) or (lab[0].isdigit() and v.startswith("+")) else INK)
        if "fails" in v or "Worsens" in v:
            col = RED
        if "meets" in v and j == 3:
            col = BLUE
        parts = v.split("\n")
        paras = [{"text": parts[0], "bold": big or lab[0].isdigit(), "size": 12 if big else 10}]
        if len(parts) > 1:
            paras.append({"text": parts[1], "size": 8.5, "color": INK2, "bold": False})
        s.text(x_, yy, w_, h_, paras, size=10, color=col, align="c", anchor="m", inset=0.04)
        x_ += w_
    yy += h_
    s.line(LM, yy + 0.02, LM + CW, yy + 0.02, color=RULE if not big else NAVY, lw=0.5 if not big else 0.75)
    yy += 0.05
footer(s, "Timing: exit effective 1 Jul 2027 (2027 loses half-year contribution, full $2.1M penalty); redesign savings from 1 Sep 2027 after validation and pilot. Migration at the 25% ceiling.")

# =====================================================================
# 13. Redesign economics
# =====================================================================
s = d.new_slide("redesign economics")
header(s, "D  |  What should Vesper do instead?",
       "The $0.55M redesign pays back in about 5 months of savings and still breaks even if it delivers only "
       "a fifth of the $1.25M estimate")
tiles = [("~5 months", "Payback on run-rate savings", "$0.55M ÷ $1.25M a year = 0.44 years"),
         ("19%", "Of estimated savings needed to break even by 2029", "$0.55M ÷ 2.33 years of savings = $0.24M a year"),
         ("+$0.40M", "2027–29 value in the downside case", "50% of savings, 3 months late, full $0.9M envelope spent")]
for i, (big, lab, calc) in enumerate(tiles):
    tx = LM + i * 4.18
    s.rect(tx, 1.65, 3.98, 1.55, fill=PANEL)
    s.text(tx + 0.18, 1.72, 3.6, 0.6, big, size=26, bold=True, color=BLUE, inset=0, anchor="m")
    s.text(tx + 0.18, 2.33, 3.6, 0.4, lab, size=10.5, bold=True, color=INK, inset=0)
    s.text(tx + 0.18, 2.75, 3.6, 0.4, calc, size=9, color=INK2, inset=0)
s.text(LM, 3.4, 7.6, 0.3, "Redesign scenarios: cash contribution vs retain unchanged, $M", size=11, bold=True, color=INK, inset=0)
cws = [2.9, 0.95, 0.95, 0.95, 1.2]
hdr = ["Scenario", "2027", "2028", "2029", "2027–29"]
x_ = LM
for h_, w_ in zip(hdr, cws):
    s.text(x_, 3.72, w_, 0.28, h_, size=9.5, bold=True, color=INK2, inset=0.03, align="l" if h_ == "Scenario" else "r")
    x_ += w_
s.line(LM, 4.02, LM + sum(cws), 4.02, color=NAVY, lw=0.75)
sc = [("Base: $1.25M a year from Sep 2027; $0.55M cost", ["–0.13", "+1.25", "+1.25", "+2.37"]),
      ("Downside: $0.63M a year from Dec 2027; $0.90M cost", ["–0.85", "+0.63", "+0.63", "+0.40"]),
      ("Break-even: $0.24M a year from Sep 2027; $0.55M cost", ["–0.47", "+0.24", "+0.24", "0.00"]),
      ("Break-even with full $0.9M spent: $0.39M a year", ["–0.77", "+0.39", "+0.39", "0.00"])]
for i, (lab, vals) in enumerate(sc):
    y_ = 4.07 + i * 0.5
    s.text(LM, y_, cws[0], 0.46, lab, size=9.5, color=INK, inset=0.03, anchor="m")
    x_ = LM + cws[0]
    for j, (v, w_) in enumerate(zip(vals, cws[1:])):
        s.text(x_, y_, w_, 0.46, v, size=10.5, bold=(j == 3), color=RED if v.startswith("–") else (BLUE if j == 3 and v.startswith("+") else INK),
               inset=0.03, anchor="m", align="r")
        x_ += w_
    s.line(LM, y_ + 0.48, LM + sum(cws), y_ + 0.48, color=RULE, lw=0.5)
s.text(LM, 6.15, 7.0, 0.7, "Rounded. 2027 savings run Sep–Dec (4 months); window = 28 months = 2.33 years. Downside 2027: –0.90 + 0.63 x 1/12. "
       "Break-even rows solve for the savings that make the 2027–29 total zero.", size=8.5, color=MUTED, inset=0)
px0 = LM + 7.75
s.rect(px0, 3.4, 4.58, 3.42, fill=PANEL)
s.text(px0 + 0.18, 3.5, 4.25, 3.3, [
    {"text": "What else the redesign changes", "bold": True, "color": NAVY, "size": 12},
    {"runs": [("C's reported margin rises to ~29%, ", {"bold": True}),
              ("level with D's 30%, if the $1.25M comes out of direct cost: (6.0 – 0.95 – 3.3) / 6.0. The ranking that started this debate goes away.", {})], "bullet": True},
    {"runs": [("Operating profit rises 12%, ", {"bold": True}),
              ("from $10.1M to $11.35M a year at full run-rate.", {})], "bullet": True},
    {"runs": [("Caution: ", {"bold": True, "color": AMBER}),
              ("$1.25M equals 57% of C's $2.2M direct cost, an engineering estimate at current volume. The two-site pilot exists to test it before "
               "the whole line converts.", {})], "bullet": True},
], size=10, inset=0.02)
footer(s, "Redesign cost excludes possible requalification tests at two customers; the downside case uses the $0.35M remaining in the envelope for them.")

# =====================================================================
# 14. Contract plan
# =====================================================================
s = d.new_slide("contract plan")
header(s, "D  |  What should Vesper do instead?",
       "Use the two renewals to secure C supply, bundle-level service terms and a consent-based path to D, "
       "not to give exit notice")
cws = [2.35, 6.4, 1.75, 1.83]
hdr = ["Workstream", "Actions", "Lead (proposed)", "Timing"]
x_ = LM
for h_, w_ in zip(hdr, cws):
    s.text(x_, 1.65, w_, 0.3, h_, size=10, bold=True, color=INK2, inset=0.03)
    x_ += w_
s.line(LM, 1.98, LM + CW, 1.98, color=NAVY, lw=0.75)
cp = [
    ("1. The two bundle renewals",
     ["Renew with C in the bundle; give no exit notice",
      "Add a clause allowing substitution by a validated D + adapter only with customer consent, after qualification",
      "Align term end with the 2029 expiry cohort so any sunset can happen at expiry, without penalty"],
     "Commercial + Legal", "Q1 2027; terms set at Feb board"),
    ("2. The other seven bundle customers",
     ["Confirm C supply through current terms",
      "Pre-notify the C design change and agree requalification tests early with the two customers that need them"],
     "Account leads + Quality", "Q1 2027"),
    ("3. Bundle service recovery",
     ["Make bundle-level fill the contract KPI on every service dashboard",
      "Root-cause A/B misses; set A/B buffer or allocation priority for bundle accounts; report monthly until ≥95%"],
     "Operations", "Start Feb 2027; target ≥95% by Q3 2027"),
    ("4. Penalty exposure",
     ["Carry the $2.1M as a contingent one-time liability tied to premature termination, not as annual overhead (Finance's rule)"],
     "Finance", "Ongoing"),
    ("5. D substitution evidence",
     ["Run adapter and quality qualification with willing C customers; record actual acceptance, not interview estimates"],
     "Engineering (D) + Sales", "From Jul 2027"),
]
yy = 2.05
for ws, acts, own, tim in cp:
    h_ = max(s.text_height(cws[1], [{"text": a, "bullet": True, "space_after": 2} for a in acts], size=10, inset=0.05),
             s.text_height(cws[3], tim, size=10), s.text_height(cws[0], ws, size=10.5, bold=True)) + 0.12
    s.text(LM, yy, cws[0], h_, ws, size=10.5, bold=True, color=NAVY, anchor="m", inset=0.03)
    s.text(LM + cws[0], yy, cws[1], h_, [{"text": a, "bullet": True, "space_after": 2} for a in acts], size=10, color=INK, anchor="m", inset=0.05)
    s.text(LM + cws[0] + cws[1], yy, cws[2], h_, own, size=10, color=INK, anchor="m", inset=0.03)
    s.text(LM + cws[0] + cws[1] + cws[2], yy, cws[3], h_, tim, size=10, color=INK, anchor="m", inset=0.03)
    yy += h_
    s.line(LM, yy + 0.02, LM + CW, yy + 0.02, color=RULE, lw=0.5)
    yy += 0.06
s.text(LM, yy + 0.08, CW, 6.85 - yy - 0.08,
       [{"runs": [("Why this order: ", {"bold": True, "color": NAVY}),
                  ("the penalty stands unless counterparties consent, so consent-based substitution and expiry-aligned terms are the only routes to a "
                   "penalty-free exit later. Fixing A/B fill protects all nine bundles whatever happens to C.", {})]}],
       size=10.5, inset=0.02, anchor="m")
footer(s, "Leads, and the Q3 2027 fill target, are proposals for management to confirm; the pack names neither owners nor a recovery date.")

# =====================================================================
# 15. Roadmap and gates
# =====================================================================
s = d.new_slide("roadmap")
header(s, "D  |  What should Vesper do instead?",
       "A staged plan with two decision gates protects $3.8M of contribution today and keeps a "
       "2029 sunset open if the evidence turns")
qx0, qw = LM + 2.6, (CW - 2.6) / 12
qy = 1.65
quarters = [f"Q{q}" for y in (2027, 2028, 2029) for q in (1, 2, 3, 4)]
for i, q in enumerate(quarters):
    s.text(qx0 + i * qw, qy + 0.25, qw, 0.25, q, size=9, color=INK2, align="c", inset=0)
for k, yr in enumerate((2027, 2028, 2029)):
    s.text(qx0 + k * 4 * qw, qy, 4 * qw, 0.25, str(yr), size=10, bold=True, color=NAVY, align="c", inset=0)
    s.line(qx0 + k * 4 * qw, qy, qx0 + k * 4 * qw, 5.1, color=RULE, lw=0.5)
s.line(qx0, qy + 0.53, LM + CW, qy + 0.53, color=NAVY, lw=0.75)
def qpos(q):  # q in quarters from start of 2027, fractional
    return qx0 + q * qw
lanes = [
    ("C redesign", [(0.67, 2.0, NAVY, "Design + validation"), (2.0, 2.67, "45617F", "Pilot"), (2.67, 12, BLUE_LT, "Full line at run-rate savings (from Sep 2027)")]),
    ("Engineering team", [(0.67, 2.0, NAVY, "On C"), (2.0, 12, BLUE, "On D: adapter validation and D growth")]),
    ("Bundle fill", [(0.33, 3.0, "E8A33C", "A/B root-cause; recover to ≥95%"), (3.0, 12, "F6DDB0", "Sustain ≥95%; monthly board report")]),
    ("Contracts", [(0.0, 1.0, NAVY, "Renew 2"), (1.0, 8.0, "D9D8D4", "Bundle terms run; requalification with 2 customers"), (8.0, 12, "45617F", "2029 expiries")]),
    ("D substitution evidence", [(2.0, 8.0, BLUE_LT, "Adapter qualification; observed acceptance rates"), (8.0, 12, "D9D8D4", "Only if Gate 2 passes: migrate at expiry")]),
]
# gates drawn first so lane bars sit on top of the dashed lines
for (q, lab) in [(2.67, "Gate 1"), (7.5, "Gate 2")]:
    s.line(qpos(q), 2.2, qpos(q), 5.12, color=RED, lw=1.25, dash=True)
    s.text(qpos(q) - 0.45, 5.12, 0.9, 0.26, lab, size=9.5, bold=True, color=RED, align="c", inset=0)
s.line(qpos(0.33), 2.2, qpos(0.33), 5.12, color=NAVY, lw=1.0, dash=True)
s.text(qpos(0.33) - 0.55, 5.12, 1.1, 0.26, "Feb board", size=9, bold=True, color=NAVY, align="c", inset=0)
for i, (lab, bars_) in enumerate(lanes):
    ly = 2.32 + i * 0.55
    s.text(LM, ly, 2.5, 0.42, lab, size=10.5, bold=True, color=NAVY, anchor="m", inset=0)
    for (a, b, col, t) in bars_:
        dark = col in (NAVY, "45617F", BLUE)
        s.text(qpos(a) + 0.02, ly + 0.04, (b - a) * qw - 0.04, 0.36, t, size=8.5, color="FFFFFF" if dark else INK,
               fill=col, align="c", anchor="m", inset=0.03)
gy = 5.48
s.rect(LM, gy, 6.07, 1.3, fill=PANEL)
s.text(LM + 0.12, gy + 0.05, 5.85, 1.32, [
    {"text": "Gate 1, end of Aug 2027: convert the whole C line?", "bold": True, "color": NAVY},
    {"text": "Go if the pilot run-rate saving is ≥$0.4M a year (the break-even with the full $0.9M spent) and no customer requalification has failed", "bullet": True},
    {"text": "Otherwise stop at the pilot sites, with spend capped inside the $0.9M envelope", "bullet": True},
], size=9.5, inset=0.02)
s.rect(LM + 6.27, gy, 6.07, 1.3, fill=PANEL)
s.text(LM + 6.39, gy + 0.05, 5.85, 1.32, [
    {"text": "Gate 2, Q4 2028 (or the notice deadline, if earlier): sunset C in 2029?", "bold": True, "color": NAVY},
    {"text": "Consider sunset only if: D adapter validated on every hospital model in C bundles; observed acceptance high enough; D capacity in place; "
             "fill ≥95% for 2 quarters; renewal gap shown to be causal; updated exit bridge positive", "bullet": True},
], size=9.5, inset=0.02)
footer(s, "Assumes redesign kick-off in Mar 2027, 4-month validation, 2-month pilot. Contract notice periods are not in the pack; Gate 2 must precede them.")

# =====================================================================
# 16. Risks & unknowns
# =====================================================================
s = d.new_slide("risks")
header(s, "D  |  What should Vesper do instead?",
       "None of the open unknowns is likely to flip the decision against exit, and each is tested at a gate in the plan")
cws = [2.15, 3.85, 3.6, 2.73]
hdr = ["Unknown", "What the evidence says", "Effect on the recommendation", "How the plan resolves it"]
x_ = LM
for h_, w_ in zip(hdr, cws):
    s.text(x_, 1.62, w_, 0.3, h_, size=10, bold=True, color=INK2, inset=0.03)
    x_ += w_
s.line(LM, 1.95, LM + CW, 1.95, color=NAVY, lw=0.75)
rk = [
    ("D substitution acceptance", "25% is a ceiling from three sales interviews; adapters and validation are customer-specific",
     "None: even 100% migration loses $0.4M a year", "Observed acceptance in qualification (from Jul 2027)"),
    ("Requalification at 2 customers", "Not included in the $0.55M; could delay savings",
     "Low: downside (3 months late, $0.9M spent, half the savings) is still +$0.40M", "Early engagement in Q1 2027; $0.35M reserve"),
    ("Redesign savings at scale", "$1.25M is an estimate at current volume, 57% of C's direct cost",
     "Low: breaks even at 19% of estimate (31% if the full $0.9M is spent)", "Two-site pilot; Gate 1 threshold $0.4M a year"),
    ("Speed of bundle-fill recovery", "Fill is 91% vs 95%; no recovery timeline or cost in the pack",
     "Same under every option, since the cause is A/B; matters for renewals", "Ops plan in Feb; monthly board tracking"),
    ("Engineering opportunity cost", "Not quantified for the four months on C",
     "Low: illustrative ceiling ≈$0.25M vs $1.25M a year of savings", "Team moves to D from Jul 2027"),
    ("C price pressure", "Competitive pressure named, not quantified",
     "Exit breaks even on run-rate only if C contribution falls ~70%, from $3.8M to $1.15M", "Re-test C contribution at Gate 2"),
]
rh = 0.74
for i, r in enumerate(rk):
    yy = 2.0 + i * rh
    x_ = LM
    for j, (v, w_) in enumerate(zip(r, cws)):
        s.text(x_, yy, w_, rh - 0.06, v, size=10 if j else 10.5, bold=(j == 0), color=NAVY if j == 0 else INK, anchor="m", inset=0.04)
        x_ += w_
    s.line(LM, yy + rh - 0.03, LM + CW, yy + rh - 0.03, color=RULE, lw=0.5)
s.text(LM, 6.48, CW, 0.4, "Key assumptions: FY2026 volumes and costs hold through 2029; the penalty is payable in full unless counterparties consent; the $0.4M avoidable "
       "fixed cost is Finance's estimate; cash effects are undiscounted (the horizon is three years).", size=9.5, color=INK2, inset=0.02, anchor="m")
footer(s, "C price-pressure threshold: exit run-rate = –C contribution + 0.4 + 0.75 = 0, so C contribution = $1.15M.")

# =====================================================================
# 17. Decisions requested
# =====================================================================
s = d.new_slide("decisions")
header(s, "Decisions for the February 2027 board",
       "We ask the board for six decisions that keep $3.8M of contribution, avoid $2.1M of penalties "
       "and add about $1.25M a year")
dec = [
    ("Reject", "discontinuing connector C in 2027", "Exit loses $4.75M in year one and $2.65M a year after, and breaches the cash and fill constraints"),
    ("Approve", "$0.55M for the C redesign, plus up to $0.35M reserve, within the $0.9M envelope", "Pilot at two sites first; Gate 1 at end of Aug 2027"),
    ("Mandate", "bundle-level contracted fill as the service KPI", "Operations to present an A/B recovery plan to reach ≥95%, with dates and cost"),
    ("Authorise", "renewal terms for the two bundle agreements", "C retained; consent-based D substitution clause; terms aligned to 2029 expiries"),
    ("Sequence", "engineering: C redesign Mar–Jun 2027, then D", "The D adapter work also builds the evidence for any later sunset"),
    ("Set", "Gate 2 criteria for any 2029 sunset (Q4 2028)", "Validated adapter, observed acceptance, sustained ≥95% fill, causal renewal test, positive exit bridge"),
]
for i, (verb, what, why) in enumerate(dec):
    yy = 1.68 + i * 0.84
    s.oval(LM, yy + 0.12, 0.5, NAVY)
    s.text(LM, yy + 0.12, 0.5, 0.5, str(i + 1), size=14, bold=True, color="FFFFFF", align="c", anchor="m", inset=0)
    s.text(LM + 0.7, yy, 6.1, 0.74, [{"runs": [(verb + " ", {"bold": True, "color": BLUE}), (what, {"bold": True})]}],
           size=12, color=NAVY, anchor="m", inset=0.02)
    s.text(LM + 6.95, yy, 5.38, 0.74, why, size=10.5, color=INK2, anchor="m", inset=0.02)
    if i < 5:
        s.line(LM + 0.7, yy + 0.8, LM + CW, yy + 0.8, color=RULE, lw=0.5)
footer(s)

# =====================================================================
# 18. Appendix: calculations
# =====================================================================
s = d.new_slide("appendix calcs")
header(s, "Appendix A  |  Calculation log",
       "Every number in the deck comes from briefing-pack inputs with the arithmetic shown here")
colL = [
    {"text": "Margins (FY2026, $M)", "bold": True, "color": NAVY, "size": 11},
    {"text": "Contribution margin = (sales – direct variable) / sales: A 7.0/14.0 = 50.0%; B 3.8/9.0 = 42.2%; C 3.8/6.0 = 63.3%; D 2.0/4.0 = 50.0%", "bullet": True},
    {"text": "Reported margin = (sales – variable – allocated) / sales: A 5.8/14.0 = 41.4%; B 2.6/9.0 = 28.9%; C 0.5/6.0 = 8.3%; D 1.2/4.0 = 30.0%", "bullet": True},
    {"text": "C allocated 3.3 = avoidable 0.4 + non-avoidable 2.9 (88%)", "bullet": True},
    {"text": "Company: contribution 16.6 – allocated 6.5 = operating profit 10.1", "bullet": True},
    {"text": "Exit bridge", "bold": True, "color": NAVY, "size": 11},
    {"text": "Recurring: –3.8 + 0.4 + (0.25 x 6.0 x 0.50 = 0.75) = –2.65; no migration –3.40", "bullet": True},
    {"text": "First 12 months: –2.65 – 2.1 penalty = –4.75", "bullet": True},
    {"text": "Calendar 2027 (exit 1 Jul): –1.9 + 0.2 + 0.375 – 2.1 = –3.43; 2027–29 = –3.43 – 2.65 – 2.65 = –8.73 (no migration: –3.8 – 3.4 – 3.4 = –10.6)", "bullet": True},
    {"text": "Break-even migrated D revenue = 3.4 / 0.5 = 6.8 = 113% of C sales, 4.5x D spare capacity of 1.5", "bullet": True},
    {"text": "Operating profit after exit: 16.6 – 3.8 + 0.75 = 13.55 contribution – 6.1 fixed = 7.45 (–26%); no migration 6.7 (–34%)", "bullet": True},
]
colR = [
    {"text": "Reallocation if C exits (pro rata assumption)", "bold": True, "color": NAVY, "size": 11},
    {"text": "2.9 split 1.2 : 1.2 : 0.8 gives A +1.0875, B +1.0875, D +0.725", "bullet": True},
    {"text": "A (14 – 7 – 2.29)/14 = 33.7%; B (9 – 5.2 – 2.29)/9 = 16.8%; D (5.5 – 2.75 – 1.53)/5.5 = 22.3% (with migration) or 11.9% (without)", "bullet": True},
    {"text": "Redesign", "bold": True, "color": NAVY, "size": 11},
    {"text": "Payback = 0.55 / 1.25 = 0.44 yr ≈ 5.3 months of run-rate", "bullet": True},
    {"text": "Base: 2027 = –0.55 + 1.25 x 4/12 = –0.13; 2028, 2029 = +1.25; total +2.37", "bullet": True},
    {"text": "Downside: 2027 = –0.90 + 0.625 x 1/12 = –0.85; 2028, 2029 = +0.625; total +0.40", "bullet": True},
    {"text": "Break-even savings = 0.55 / 2.333 = 0.236 (19% of 1.25); with 0.9 spent = 0.386 (31%)", "bullet": True},
    {"text": "Reported C margin after redesign = (6.0 – 0.95 – 3.3)/6.0 = 29.2%; operating profit 10.1 + 1.25 = 11.35 (+12%)", "bullet": True},
    {"text": "Other bounds", "bold": True, "color": NAVY, "size": 11},
    {"text": "Engineering ceiling = 4/12 x 0.75 = 0.25; C price-pressure break-even: 3.8 – 1.15 = 2.65 drop (70%)", "bullet": True},
]
s.text(LM, 1.62, 6.0, 5.25, colL, size=10.5, inset=0.02)
s.text(LM + 6.3, 1.62, 6.03, 5.25, colR, size=10.5, inset=0.02)
footer(s)

# =====================================================================
# 19. Appendix: assumptions / judgement calls
# =====================================================================
s = d.new_slide("appendix assumptions")
header(s, "Appendix B  |  Judgement calls",
       "Where the pack was silent we made eight working assumptions; each is conservative or does not change the answer")
asm = [
    ("Exit timing", "Exit effective 1 Jul 2027 (\"Q2 2027\"); the full $2.1M penalty falls in 2027", "Exit looks no better under any timing; recurring loss is timing-independent"),
    ("Penalty and cash envelope", "The $2.1M penalty counts against the $0.9M one-time cash for 2027 portfolio changes", "Even outside the envelope, exit fails the fill and contribution tests"),
    ("Migration", "25% migration used as a ceiling, never a forecast; no recapture beyond it", "100% migration still loses $0.4M a year"),
    ("Reallocation split", "The $2.9M of stranded cost moves pro rata to today's A/B/D allocation", "Illustrative only; total company profit is unaffected by the split"),
    ("Redesign timing", "Kick-off Mar 2027, 4-month validation, 2-month two-site pilot, savings from Sep 2027", "Pilot-site savings in Jul–Aug ignored (conservative)"),
    ("Savings location", "The $1.25M direct saving reduces C's direct cost (used only for the 29% reported-margin figure)", "Cash case is unchanged wherever the saving sits"),
    ("Delayed sunset", "Exits at contract expiry in 2029 avoid the penalty; contracts not expiring would still need consent", "Only affects the post-2029 view"),
    ("Horizon and discounting", "2027–29, undiscounted; FY2026 volumes, prices and costs held flat", "A short horizon and early redesign cash flows mean discounting would not change the ranking"),
]
cws = [2.3, 5.5, 4.53]
x_ = LM
for h_, w_ in zip(["Topic", "Assumption used", "Why it is safe / effect if wrong"], cws):
    s.text(x_, 1.62, w_, 0.3, h_, size=10, bold=True, color=INK2, inset=0.03)
    x_ += w_
s.line(LM, 1.95, LM + CW, 1.95, color=NAVY, lw=0.75)
rh = 0.6
for i, r in enumerate(asm):
    yy = 2.0 + i * rh
    x_ = LM
    for j, (v, w_) in enumerate(zip(r, cws)):
        s.text(x_, yy, w_, rh - 0.05, v, size=10, bold=(j == 0), color=NAVY if j == 0 else INK, anchor="m", inset=0.04)
        x_ += w_
    s.line(LM, yy + rh - 0.02, LM + CW, yy + rh - 0.02, color=RULE, lw=0.5)
footer(s, "No questions could be put to management while preparing this deck; these choices should be confirmed with Finance and Operations.")

d.save(os.path.join(OUT, "Vesper_MedTech_Connector_C_Board_Deck.pptx"), PREV,
       os.path.join(OUT, "Vesper_MedTech_Connector_C_Board_Deck_preview.pdf"))
print("\n".join(WARNINGS) if WARNINGS else "no layout warnings")
print("slides:", len(d.slides))
