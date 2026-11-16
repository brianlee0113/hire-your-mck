import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from engine import Slide, build_pptx, render_png, check, W, H, norm_paras, measure, INS_L, INS_R, INS_T, INS_B


def hgt(content, w, size=12, bold=False):
    return measure(norm_paras(content, size, '#000', bold, 'l'), w - INS_L - INS_R)[0] + INS_T + INS_B

INK, SEC, MUTED = "#0b0b0b", "#52514e", "#898781"
GRID, AXIS, PANEL = "#e1e0d9", "#c3c2b7", "#f4f3ef"
BLUE, RED, ORANGE, AQUA = "#2a78d6", "#e34948", "#eb6834", "#1baf7a"
LBLUE, LRED = "#cde2fb", "#f8d7d6"
ACCENT = "#184f95"
GOOD, WARN, CRIT = "#0ca30c", "#fab219", "#d03b3b"
L, R = 0.6, 12.733
CW = R - L

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "deliverable")
SRC = "Source: Parcelbird board briefing pack; Parcelbird analysis."

slides = []


def new(section, title, source=SRC):
    s = Slide()
    s.text(L, 0.30, 9, 0.3, section.upper(), size=10, bold=True, color=ACCENT)
    s.text(L, 0.58, CW, 0.92, title, size=22, bold=True, color=INK)
    s.line(L, 1.55, R, 1.55, GRID, 0.75)
    s.text(L, 6.98, 11.3, 0.4, source, size=8.5, color=MUTED)
    s.text(12.0, 6.98, R - 12.0, 0.3, str(len(slides) + 1), size=9, color=MUTED, align="r")
    slides.append(s)
    return s


def status(s, x, y, kind, label, size=10.5):
    col = {"good": GOOD, "warn": WARN, "crit": CRIT}[kind]
    d = 0.13
    s.oval(x, y + 0.055, d, d, fill=col)
    s.text(x + 0.17, y - 0.01, 1.9, 0.27, label, size=size, bold=True, color=INK)


def fmt(v, dp=2, sign=True):
    s = f"{abs(v):,.{dp}f}"
    if v < 0:
        return "−$" + s
    return ("+$" if sign else "$") + s


# ===================================================================== 1. Title
s = Slide(); slides.append(s)
s.rect(0, 0, W, H, fill="#ffffff")
s.rect(L, 2.15, 0.09, 2.25, fill=BLUE)
s.text(0.95, 1.95, 11.2, 0.35, "PARCELBIRD  ·  BOARD OF DIRECTORS", size=12, bold=True, color=ACCENT)
s.text(0.95, 2.35, 11.4, 1.6, "Parcelbird Now: should we launch our own quick-commerce grocery delivery service in 2027?",
       size=34, bold=True, color=INK)
s.text(0.95, 3.95, 11.0, 0.45, "Discussion document for the January 2027 decision meeting", size=16, color=SEC)
s.text(0.95, 6.35, 11.5, 0.7,
       ["All figures come from the board briefing pack or are derived from it; the derivations are in the appendix (pages 13–14).",
        "No external research was used."], size=10.5, color=MUTED)

# ===================================================================== 2. Executive summary
s = new("Executive summary",
        "Recommendation: do not launch Parcelbird Now in 2027. Put the money into the software business, which can break even within today's cash if growth holds")
finds = [
    ("1", "Orders lose money at every level of performance we have seen.",
     "At the median of the 14 customer sites our software runs, each order loses $2.67 before dark-store costs and "
     "$6.17 after them. Combining the best value seen at any site on every input, which no single site has managed, still loses $1.76."),
    ("2", "The founders' plan turns positive only by beating our best site on three drivers at once.",
     "It assumes a $45 order (best seen: $42), 3.5 orders per rider-hour (best: 3.0), 1,800 orders a day (best: 1,400) "
     "and promotions at 2% of order value (every site: 6%). If order value or rider productivity only reaches the median, orders lose money again."),
    ("3", "Our own test and the market point the same way.",
     "The Columbus pop-up lost about $12.57 per order, falling below the median on every driver, and only 22% of customers were "
     "still ordering in month three. Both incumbents lose money on every order; QuickBasket closed 4 of its 11 cities in 2025."),
    ("4", "The plan breaks the 12-month runway rule even if it works; the software path does not.",
     "Holding 12 months of runway leaves $7.2M to deploy, and the plan needs $9.5M. Adding $0.8M a year of engineering and sales "
     "reaches break-even in months 26–32 if growth holds at 45–60% and other costs stay flat."),
]
fc = [[{"text": head, "bold": True, "size": 13, "space_after": 3}, {"text": body, "size": 11.5, "color": SEC}] for _, head, body in finds]
fh = [hgt(c, 7.65) for c in fc]
gap_ = (6.8 - 1.78 - sum(fh)) / 3
y = 1.78
for (n, head, body), c, h_ in zip(finds, fc, fh):
    s.oval(L, y + 0.02, 0.34, 0.34, fill=BLUE)
    s.text(L, y + 0.02, 0.34, 0.34, n, size=12, bold=True, color="#ffffff", align="c", valign="m")
    s.text(L + 0.5, y - 0.02, 7.65, h_ + 0.02, c)
    y += h_ + gap_
px = 8.95
s.rect(px, 1.78, R - px, 5.0, fill=PANEL)
s.text(px + 0.25, 1.95, R - px - 0.45, 0.35, "Decisions we ask the board to take", size=13, bold=True)
asks = [
    "**Decline Parcelbird Now for 2027.**",
    "**Approve $0.8M a year** for 2 engineers and 2 sales hires to work the 37-grocer pipeline.",
    "**Ask management to package the software** for grocers who want fast delivery from their own stores, selling to that trend rather than competing with our pipeline.",
    "**Agree now what would reopen the question** (page 12).",
]
y = 2.45
for i, a in enumerate(asks, 1):
    s.text(px + 0.25, y, 0.3, 0.3, f"{i}.", size=12, bold=True, color=ACCENT)
    s.text(px + 0.55, y, R - px - 0.75, hgt(a, R - px - 0.75, 12) + 0.02, a, size=12)
    y += hgt(a, R - px - 0.75, 12) + 0.3

# ===================================================================== 3. Claims tested
s = new("The founders' case, tested",
        "Of the founders' four claims, only market growth holds up, and the plan fails both of the board's constraints")
cols = [(L, 3.15), (L + 3.25, 7.05), (L + 10.45, CW - 10.45)]
s.text(cols[0][0], 1.72, cols[0][1], 0.3, "Claim or constraint", size=10.5, bold=True, color=SEC)
s.text(cols[1][0], 1.72, cols[1][1], 0.3, "What the briefing pack shows", size=10.5, bold=True, color=SEC)
s.text(cols[2][0], 1.72, cols[2][1], 0.3, "Verdict", size=10.5, bold=True, color=SEC)
s.line(L, 2.05, R, 2.05, AXIS, 1)
rows = [
    ("FOUNDERS' CLAIMS", None, None, None),
    ("“Quick commerce is growing over 40% a year”",
     "US quick-commerce grocery sales rose from $1.8B (2022) to $5.1B (2025), or 41.5% a year compounded.", "good", "Supported"),
    ("“Nobody owns the Midwest”",
     "No operator is named as owning it. But the one regional operator, QuickBasket, loses $3.40 per order and closed 4 of its 11 cities in 2025; an open market may simply be an unprofitable one.",
     "warn", "Partly"),
    ("“We know how to run them better than anyone”",
     "Our six-week Columbus pop-up was below our customers' median on all four drivers: order value $31 vs $34, promotions 12% vs 6%, 2.1 vs 2.4 orders per rider-hour, 280 vs 900 orders a day. Six weeks is early, but order value and promotions depend little on ramp-up.",
     "crit", "Not shown"),
    ("“Contribution profit per order by month 18”",
     "Requires order value, rider productivity and store density all above the best of the 14 sites at once, and promotions at one-third of the benchmark (pages 5–7).",
     "crit", "Not supported"),
    ("BOARD CONSTRAINTS", None, None, None),
    ("Path to profitability within current cash",
     "At benchmark-median performance a mature dark store loses about $2.0M a year, so nine would lose about $18M a year, more than the $12.0M we hold. A new round is “unlikely”.",
     "crit", "Fails"),
    ("At least 12 months of runway at all times",
     "The plan needs $9.5M to month 18; only $7.2M is available above a 12-month reserve (page 9).", "crit", "Fails"),
]
y = 2.12
for claim, ev, kind, lab in rows:
    if ev is None:
        s.text(L, y, 4, 0.26, claim, size=9.5, bold=True, color=ACCENT)
        y += 0.3
        continue
    hh = max(hgt(claim, cols[0][1], 11.5, True), hgt(ev, cols[1][1], 11)) + 0.04
    s.text(cols[0][0], y, cols[0][1], hh, claim, size=11.5, bold=True)
    s.text(cols[1][0], y, cols[1][1], hh, ev, size=11, color=SEC)
    status(s, cols[2][0] + 0.05, y + 0.02, kind, lab, size=11)
    y += hh
    s.line(L, y, R, y, GRID, 0.75)
    y += 0.1

# ===================================================================== 4. Market
s = new("Market",
        "The market is growing about 40% a year, yet both incumbent operators lose money on every order")
s.text(L, 1.75, 5.6, 0.3, "US quick-commerce grocery sales (GMV), $ billions", size=12, bold=True)
gmv = [(2022, 1.8), (2023, 2.6), (2024, 3.6), (2025, 5.1)]
cx0, cy_base, ch = L + 0.3, 5.95, 3.3
bw, gap = 0.85, 0.5
sc = ch / 5.5
s.line(L + 0.1, cy_base, L + 0.3 + 4 * (bw + gap), cy_base, AXIS, 1)
for i, (yr, v) in enumerate(gmv):
    x = cx0 + i * (bw + gap)
    h = v * sc
    s.rect(x, cy_base - h, bw, h, fill=BLUE)
    s.text(x - 0.2, cy_base - h - 0.33, bw + 0.4, 0.3, f"${v:.1f}B", size=12, bold=True, align="c")
    s.text(x - 0.2, cy_base + 0.06, bw + 0.4, 0.3, str(yr), size=11, color=SEC, align="c")
    if i:
        g = v / gmv[i - 1][1] - 1
        s.text(x - 0.2, cy_base + 0.34, bw + 0.4, 0.28, f"+{g:.0%} vs prior year", size=9.5, color=SEC, align="c")
s.text(L + 0.1, 2.1, 5.6, 0.3, "41.5% a year compounded, 2022–25",
       size=10, color=SEC)
# incumbents table
tx = 7.0
s.text(tx, 1.75, R - tx, 0.3, "Incumbent operators, 2025", size=12, bold=True)
hdr = ["Operator", "Revenue", "EBITDA", "EBITDA margin", "Contribution per order"]
cxs = [tx, tx + 1.75, tx + 2.65, tx + 3.55, tx + 4.55]
cws = [1.75, 0.9, 0.9, 1.0, R - tx - 4.55]
for x, w_, t in zip(cxs, cws, hdr):
    s.text(x, 2.15, w_, 0.5, t, size=10, bold=True, color=SEC, align="l" if t == "Operator" else "r", valign="b")
s.line(tx, 2.7, R, 2.7, AXIS, 1)
inc = [("Zipcart", "national", "$1,200M", "−$310M", "−26%", "−$1.90"),
       ("QuickBasket", "regional", "$210M", "−$96M", "−46%", "−$3.40")]
yy = 2.8
for nm, sub, rev, eb, mg, cpo in inc:
    s.text(cxs[0], yy, cws[0], 0.55, [{"text": nm, "bold": True, "size": 12}, {"text": sub, "size": 10, "color": SEC}])
    for x, w_, t in zip(cxs[1:], cws[1:], [rev, eb, mg, cpo]):
        s.text(x, yy, w_, 0.3, t, size=12, align="r", bold=(t == cpo))
    yy += 0.62
    s.line(tx, yy - 0.04, R, yy - 0.04, GRID, 0.75)
s.text(tx, yy + 0.05, R - tx, 0.3, "QuickBasket closed 4 of its 11 cities in 2025.", size=11, bold=True)
s.rect(tx, 4.65, R - tx, 1.48, fill=PANEL)
s.text(tx + 0.2, 4.78, R - tx - 0.4, 1.45,
       [{"text": "So what", "bold": True, "size": 12, "space_after": 4},
        {"text": "Demand is not the question. Growth has not produced profit: the larger operator loses less per order "
                 "than the regional one, but neither covers its costs. The board's question is whether any operator, "
                 "including us, can make money on each order.", "size": 11.5, "color": SEC}])

# ===================================================================== 5. Scenarios
s = new("Unit economics",
        "Only the founders' plan earns money per order, and it assumes better-than-best performance on every driver")
cx = [L, L + 2.85, L + 3.85, L + 4.95, L + 6.05, L + 7.2, L + 8.3]
cwid = [2.8, 0.95, 1.05, 1.05, 1.1, 1.05, 1.0]
heads = ["Scenario", "Order value", "Promotions, % of order", "Orders per rider-hour", "Orders per store per day",
         "Per order, before store costs", "Store cost per order"]
for x, w_, t in zip(cx, cwid, heads):
    s.text(x, 1.68, w_, 0.62, t, size=10, bold=True, color=SEC, align="l" if t == "Scenario" else "r", valign="b")
bx0 = L + 9.45
bww = R - bx0
s.text(bx0, 1.68, bww, 0.62, "Per order, after store costs", size=10, bold=True, color=SEC, align="c", valign="b")
s.line(L, 2.34, R, 2.34, AXIS, 1)
scen = [
    ("Columbus pop-up", "6 weeks, autumn 2026¹", "$31", "12%", "2.1", "280", -6.21, -6.36, -12.57, set()),
    ("Benchmark median", "our 14 customer sites, 2025", "$34", "6%", "2.4", "900", -2.67, -3.50, -6.17, set()),
    ("Best seen on every input", "no site achieved all at once²", "$42", "6%", "3.0", "1,400", 0.49, -2.25, -1.76, set()),
    ("Founders' plan", "", "$45", "2%", "3.5", "1,800", 3.77, -1.75, 2.02, {1, 2, 3, 4}),
]
vmin, vmax = -13.0, 7.0
zx = bx0 + 0.1 + (0 - vmin) / (vmax - vmin) * (bww - 0.2)
pxv = (bww - 0.2) / (vmax - vmin)
rh = 0.66
y = 2.42
for nm, sub, *vals, bef, stc, aft, hi in scen:
    s.text(cx[0], y, cwid[0], rh, [{"text": nm, "bold": True, "size": 12}, {"text": sub, "size": 9.5, "color": SEC}])
    for k, (x, w_, t) in enumerate(zip(cx[1:5], cwid[1:5], vals), 1):
        s.text(x, y, w_, 0.3, t + (" ▲" if k in hi else ""), size=12, align="r", bold=k in hi,
               color=ACCENT if k in hi else INK)
    s.text(cx[5], y, cwid[5], 0.3, fmt(bef), size=12, align="r")
    s.text(cx[6], y, cwid[6], 0.3, fmt(stc), size=12, align="r", color=SEC)
    bl = abs(aft) * pxv
    by = y + 0.06
    if aft < 0:
        s.rect(zx - bl, by, bl, 0.26, fill=RED)
        s.text(zx + 0.03, y + 0.02, 1.0, 0.3, fmt(aft), size=12, bold=True)
    else:
        s.rect(zx, by, bl, 0.26, fill=BLUE)
        s.text(zx + bl + 0.03, y + 0.02, 1.0, 0.3, fmt(aft), size=12, bold=True)
    y += rh
    s.line(L, y - 0.04, R, y - 0.04, GRID, 0.75)
s.line(zx, 2.38, zx, y - 0.04, INK, 1)
s.text(L, y + 0.02, 9.3, 0.3, "▲ = beyond the best value seen at any of the 14 sites (promotions: below the 6% every site ran)",
       size=9.5, color=ACCENT)
ins = [
    "**Even the best-of-everything case loses $1.76 per order** once a store's $1.15M annual cost is spread across 1,400 orders a day. Adding the plan's 2% promotions only reaches break-even (−$0.08).",
    "**The benchmark looks representative:** our median, −$2.67 before store costs, sits between the incumbents' reported −$1.90 and −$3.40 per order.",
    "**The pop-up's store cost per order is inflated by low volume** (280 orders a day), but it also lost $6.21 per order before any store cost.",
]
yy = 5.42
s.text(L, yy, CW, 1.5, [{"text": t, "bullet": True, "size": 11.5, "space_after": 5, "color": SEC} for t in ins])
slides[-1].text(L, 6.98, 11.3, 0.4,
                "1. Pop-up store cost uses its annualised $650K fixed cost.  2. Best order value and best density came from different sites.  "
                "Before store costs = goods margin − promotions + delivery fee − picking − rider − payment and packaging; full build on page 13.  " + SRC,
                size=8.5, color=MUTED)
# remove the default source (first footer) of this slide -> replace by keeping only the detailed one
slides[-1].els = [e for e in slides[-1].els if not (e[0] == "text" and e[1]["y"] == 6.98 and e[1]["w"] == 11.3
                                                 and "".join(t for t, _ in e[1]["paras"][0]["runs"]) == SRC)]

# ===================================================================== 6. Waterfall
s = new("Unit economics",
        "Closing the $8.19 gap between the median and the plan takes four improvements at once; order value and rider productivity supply over half",
        source="Steps are calculated in the order shown: the order-value step is valued at 6% promotions, the promotion step at a $45 order. "
               "Figures may not sum because of rounding. " + SRC)
s.text(L, 1.72, 8.3, 0.3, "Contribution per order after store costs, $: benchmark median to founders' plan", size=12, bold=True)
steps = [("Benchmark median", -6.17, "total", "", ""),
         ("Order value", 2.31, "step", "$34 → $45", "Best seen: $42"),
         ("Promotions", 1.80, "step", "6% → 2%", "Every site: 6%"),
         ("Rider productivity", 2.32, "step", "2.4 → 3.5 / hour", "Best seen: 3.0"),
         ("Store density", 1.75, "step", "900 → 1,800 / day", "Best seen: 1,400"),
         ("Founders' plan", 2.02, "total", "", "")]
c_top, c_bot = 2.25, 5.35
vmax, vmin = 3.0, -7.0
def Y(v): return c_top + (vmax - v) / (vmax - vmin) * (c_bot - c_top)
zero = Y(0)
x0 = L + 0.15
colw = 1.38
bw = 0.8
for g in (-6, -4, -2, 2):
    s.line(L, Y(g), L + 6 * colw + 0.2, Y(g), GRID, 0.5)
    s.text(L - 0.55, Y(g) - 0.12, 0.5, 0.25, f"{g:+d}".replace("-", "−"), size=9, color=MUTED, align="r")
cum = 0
prev_end = None
for i, (lab, v, kind, ch_, best) in enumerate(steps):
    x = x0 + i * colw + (colw - bw) / 2
    if kind == "total":
        top, bot = (Y(0), Y(v)) if v < 0 else (Y(v), Y(0))
        s.rect(x, top, bw, bot - top, fill=RED if v < 0 else BLUE)
        cum = v
        ly = (bot + 0.03) if v < 0 else (top - 0.32)
        s.text(x - 0.25, ly, bw + 0.5, 0.3, fmt(v), size=12, bold=True, align="c")
    else:
        a, b = cum, cum + v
        s.rect(x, Y(b), bw, Y(a) - Y(b), fill="#86b6ef")
        s.text(x - 0.25, Y(b) - 0.31, bw + 0.5, 0.3, "+" + f"${v:.2f}", size=12, bold=True, align="c")
        cum = b
    if prev_end is not None:
        s.line(prev_end[0], Y(prev_end[1]), x, Y(prev_end[1]), MUTED, 0.75)
    prev_end = (x + bw, cum)
    s.text(x0 + i * colw, 5.5, colw, 0.5, lab, size=10.5, bold=True, align="c")
    if ch_:
        s.text(x0 + i * colw, 5.9, colw, 0.3, ch_, size=10, color=INK, align="c")
        s.text(x0 + i * colw, 6.2, colw, 0.3, best, size=9.5, color=SEC, align="c", italic=True)
s.line(L, zero, L + 6 * colw + 0.2, zero, INK, 1)
s.text(L - 0.55, zero - 0.12, 0.5, 0.25, "0", size=9, color=MUTED, align="r")
px = 9.35
s.rect(px, 1.72, R - px, 4.85, fill=PANEL)
s.text(px + 0.2, 1.85, R - px - 0.4, 0.3, "What each step asks for", size=12.5, bold=True)
req = [
    "**Order value +32%** over the median and $3 above the best site, without losing the convenience use case (a risk the pack itself flags).",
    "**Promotions at a third of the benchmark.** The pop-up ran at 12%, twice the benchmark.",
    "**Rider productivity 17% above the best site**, outside the observed 1.9–3.0 range.",
    "**Density 29% above the best site**, outside the 400–1,400 range. The pop-up averaged 280 a day.",
]
s.text(px + 0.2, 2.3, R - px - 0.4, 4.2, [{"text": t, "bullet": True, "size": 11.5, "space_after": 9} for t in req])

# ===================================================================== 7. Fragility
s = new("Unit economics: sensitivity",
        "The plan has no room for error: if order value or rider productivity stays at the median, every order loses money")
s.text(L, 1.72, 6.6, 0.55, "Contribution per order after store costs if one plan input falls back to the benchmark median, $",
       size=12, bold=True)
tor = [("Founders' plan as proposed", 2.02), ("Density at 900 orders a day", 0.27), ("Promotions at 6%", 0.22),
       ("Rider productivity at 2.4 / hour", -0.31), ("Order value at $34", -0.73)]
lx, lw_ = L, 2.65
zx = L + lw_ + 1.05
sc = 1.2  # in per $
for g in (-0.5, 0.5, 1.0, 1.5, 2.0):
    gx = zx + g * sc
    s.line(gx, 2.4, gx, 5.6, GRID, 0.5)
    s.text(gx - 0.3, 5.62, 0.6, 0.25, (f"{g:+.1f}").replace("-", "−"), size=9, color=MUTED, align="c")
s.text(zx - 0.3, 5.62, 0.6, 0.25, "0", size=9, color=MUTED, align="c")
y = 2.5
for i, (lab, v) in enumerate(tor):
    s.text(lx, y, lw_, 0.45, lab, size=11, bold=(i == 0), align="r", valign="m")
    bl = abs(v) * sc
    if v >= 0:
        s.rect(zx, y + 0.08, bl, 0.3, fill=BLUE)
        s.text(zx + bl + 0.04, y + 0.07, 0.9, 0.3, fmt(v), size=11.5, bold=True)
    else:
        s.rect(zx - bl, y + 0.08, bl, 0.3, fill=RED)
        s.text(zx + 0.04, y + 0.07, 0.9, 0.3, fmt(v), size=11.5, bold=True)
    y += 0.62 if i else 0.72
    if i == 0:
        s.line(lx + 0.5, y - 0.07, zx + 2.75, y - 0.07, GRID, 0.75)
s.line(zx, 2.4, zx, 5.6, INK, 1)
s.text(L, 6.0, 6.6, 0.6,
       "Even with all four plan inputs, the margin is thin: $2.02 is 4.5% of a $45 order.",
       size=11, color=SEC)
# grid of 16 combinations
gx0 = 7.65
s.text(gx0, 1.72, R - gx0, 0.55, "Only 3 of 16 combinations of plan and median inputs make money", size=12, bold=True)
colh = ["Neither", "Plan promotions", "Plan density", "Both"]
rowh = ["Neither", "Plan order value", "Plan rider productivity", "Both"]
vals = [[-6.17, -4.81, -4.42, -3.06], [-3.86, -2.06, -2.11, -0.31], [-3.84, -2.48, -2.09, -0.73], [-1.53, 0.27, 0.22, 2.02]]
lab_w = 1.6
cw_ = (R - gx0 - lab_w) / 4
s.text(gx0 + lab_w, 2.22, cw_ * 4, 0.25, "Promotions (2%) and density (1,800 a day) at plan level?", size=9, color=SEC, align="c")
for j, t in enumerate(colh):
    s.text(gx0 + lab_w + j * cw_, 2.45, cw_, 0.42, t, size=9.5, bold=True, align="c", valign="b")
s.text(gx0, 2.22, lab_w - 0.05, 0.65, "Order value ($45) and rider productivity (3.5) at plan level?", size=9, color=SEC, valign="b")
ch_ = 0.46
for i, t in enumerate(rowh):
    yy = 2.95 + i * ch_
    s.text(gx0, yy, lab_w - 0.05, ch_, t, size=9.5, bold=True, valign="m")
    for j in range(4):
        v = vals[i][j]
        s.rect(gx0 + lab_w + j * cw_ + 0.02, yy + 0.02, cw_ - 0.04, ch_ - 0.04, fill=LBLUE if v > 0 else LRED)
        s.text(gx0 + lab_w + j * cw_, yy, cw_, ch_, fmt(v), size=11, bold=v > 0, align="c", valign="m")
s.text(gx0, 4.9, R - gx0, 0.75,
       "All three profitable cases need **both** the $45 order and 3.5 orders per rider-hour, and each is above the best site we have seen.",
       size=11, color=SEC)
s.rect(gx0, 5.72, R - gx0, 1.08, fill=PANEL)
s.text(gx0 + 0.15, 5.78, R - gx0 - 0.3, 1.0,
       [{"text": "Rider pay rules add downside", "bold": True, "size": 11, "space_after": 2},
        {"text": "Two of the three target cities are considering minimum pay for delivery workers. Each extra $1 per rider-hour costs "
                 "$0.29 per order at plan productivity ($0.42 at the median); $7.06 more an hour (+40%) erases the plan's margin on its own.",
         "size": 10, "color": SEC}])

# ===================================================================== 8. Demand
s = new("Customers and the pop-up test",
        "Demand is thinner than the survey suggests: 22% of pop-up customers stayed, so each retained customer cost about $173 to acquire")
tiles = [("44%", "of 1,500 Columbus residents aged 25–39 said they would use 15-minute delivery at least weekly", "Stated intent, one age band"),
         ("22%", "of pop-up customers were still ordering in month three", "Observed behaviour"),
         ("3.1", "orders a month from those who stayed: less than once a week", "Observed behaviour"),
         ("$173", "to acquire each customer who stays ($38 acquisition cost ÷ 22%)", "Derived")]
tw = (CW - 3 * 0.25) / 4
for i, (big, txt, tag) in enumerate(tiles):
    x = L + i * (tw + 0.25)
    s.rect(x, 1.75, tw, 1.95, fill=PANEL)
    s.text(x + 0.15, 1.83, tw - 0.3, 0.25, tag.upper(), size=8.5, bold=True, color=ACCENT)
    s.text(x + 0.15, 2.07, tw - 0.3, 0.65, big, size=30, bold=True)
    s.text(x + 0.15, 2.78, tw - 0.3, 0.85, txt, size=10.5, color=SEC)
for i in range(3):
    x = L + (i + 1) * (tw + 0.25) - 0.19
    s.text(x - 0.03, 2.45, 0.22, 0.4, "›", size=20, color=MUTED, align="c", check=False)
# payback table
s.text(L, 3.95, 6.6, 0.3, "Payback on acquisition depends entirely on per-order economics", size=12, bold=True)
pc = [L, L + 3.3, L + 5.0]
pw = [3.3, 1.7, 1.55]
for x, w_, t in zip(pc, pw, ["Per-order economics", "Contribution per retained customer per month", "Months to recover $173"]):
    s.text(x, 4.22, w_, 0.56, t, size=9.5, bold=True, color=SEC, valign="b", align="l" if x == L else "r")
s.line(L, 4.82, L + 6.55, 4.82, AXIS, 1)
prow = [("Pop-up actual, after store costs (−$12.57)", "−$38.97", "Never"),
        ("Benchmark median, after store costs (−$6.17)", "−$19.12", "Never"),
        ("Founders' plan, before store costs (+$3.77)", "+$11.68", "≈15"),
        ("Founders' plan, after store costs (+$2.02)", "+$6.26", "≈28")]
yy = 4.88
for a, b, c in prow:
    s.text(pc[0], yy, pw[0], 0.3, a, size=11)
    s.text(pc[1], yy, pw[1], 0.3, b, size=11, align="r")
    s.text(pc[2], yy, pw[2], 0.3, c, size=11, bold=True, align="r")
    yy += 0.38
    s.line(L, yy - 0.04, L + 6.55, yy - 0.04, GRID, 0.5)
s.text(L, yy + 0.02, 6.55, 0.4, "Contribution = 3.1 orders × per-order result. Ignores orders in months 1–3 and any later churn.",
       size=9, color=MUTED)
# fair reading
fx = 7.6
s.text(fx, 3.95, R - fx, 0.3, "Reading the pop-up fairly", size=12, bold=True)
fair = [
    "**It is an early read.** One temporary site for six weeks; orders grew 18% a week, which implies an exit rate of roughly 410 a day if growth was steady. That is still under half the 900 median.",
    "**The growth was bought.** Promotions averaged 12% of order value, and each customer cost $38 in paid social and first-order credits.",
    "**One figure needs checking.** A six-week test cannot fully observe month-three retention, so management should confirm how the 22% was measured.",
]
s.text(fx, 4.32, R - fx, 2.5, [{"text": t, "bullet": True, "size": 11, "space_after": 7, "color": SEC} for t in fair])

# ===================================================================== 9. Cash
s = new("Capital and runway",
        "Even if every assumption holds, the plan breaks the board's rule of keeping 12 months of runway",
        source="The briefing pack does not say whether the $9.5M includes the existing $0.4M a month burn, so both readings are shown. "
               "Runway = cash ÷ current monthly burn. Month-by-month figures assume even spending. " + SRC)
s.text(L, 1.72, 7.4, 0.3, "Cash available vs. cash the plan needs, $M", size=12, bold=True)
blx = L + 3.0
scl = 4.1 / 17.0
rows9 = [("Cash in the bank today", [(7.2, BLUE, "Available $7.2M", "#ffffff"), (4.8, "#d6d4cc", "12-month reserve $4.8M", INK)], "$12.0M"),
         ("Plan's cash need to month 18 (founders' figure)", [(9.5, RED, "", "")], "$9.5M"),
         ("Plan's need if today's software burn ($7.2M over 18 months) comes on top", [(16.7, RED, "", "")], "$16.7M")]
y = 2.3
for i, (lab, segs, tot) in enumerate(rows9):
    s.text(L, y, 2.9, 0.8, lab, size=11, align="r", valign="m", bold=(i < 2))
    x = blx
    for v, col, sl, tc in segs:
        s.rect(x, y + 0.16, v * scl - (0.02 if len(segs) > 1 else 0), 0.48, fill=col)
        if sl:
            s.text(x, y + 0.16, v * scl, 0.48, sl, size=10, bold=True, color=tc, align="c", valign="m")
        x += v * scl
    s.text(x + 0.06, y + 0.25, 0.9, 0.3, tot, size=12, bold=True)
    y += 1.05
avail_x = blx + 7.2 * scl
s.line(avail_x, 2.25, avail_x, y - 0.1, INK, 1)
s.text(avail_x - 1.6, y - 0.08, 3.2, 0.3, "Available without breaching the reserve", size=9.5, color=INK, align="c")
s.text(L, 6.35, 7.4, 0.3, "Reserve = 12 months × today's $0.4M monthly burn, the most lenient test.", size=9.5, color=MUTED)
s.text(L, 5.65, 7.3, 0.55, "Even on the founders' own figure, the plan needs $2.3M more than can be spent without breaching the reserve.",
       size=11, bold=True)
px = 8.4
s.rect(px, 1.72, R - px, 5.08, fill=PANEL)
pts = [
    ("At best, $2.5M left at month 18.", "That is about 6 months of runway even at today's burn. With even spending, runway falls below 12 months around month 11."),
    ("If the $9.5M excludes today's burn, cash runs out around month 13.", "That is before the plan's own month-18 milestone."),
    ("The $9.5M already assumes the plan's economics.", "At benchmark-median performance each mature store loses about $2.0M a year, so nine would lose about $18M a year."),
    ("There is no backstop.", "The lead investor calls a new round for a delivery operator “unlikely in this market”."),
]
s.text(px + 0.2, 1.88, R - px - 0.4, 4.85,
       sum([[{"text": a, "bold": True, "size": 11.5, "space_after": 2}, {"text": b, "size": 11, "color": SEC, "space_after": 11}]
            for a, b in pts], []))

# ===================================================================== 10. Options
s = new("Options",
        "Of three options, only scaling the software business meets both of the board's constraints")
ox = [L, L + 2.2, L + 2.2 + 3.33, L + 2.2 + 6.66]
ow = 3.25
opts = [("A. Launch Parcelbird Now as proposed", "9 dark stores in 3 cities; $5.4M capex; $9.5M to month 18", False),
        ("B. Open one permanent Columbus store as a further test", "$0.6M capex plus one store's operating losses", False),
        ("C. Scale software; serve grocers' own fast delivery", "$0.8M a year for 2 engineers and 2 sales hires", True)]
for i, (t, sub, rec) in enumerate(opts):
    x = ox[i + 1]
    if rec:
        s.rect(x - 0.05, 1.68, ow + 0.02, 5.17, fill=None, line=BLUE, lw=2)
        s.text(x + 0.05, 1.72, ow - 0.1, 0.25, "RECOMMENDED", size=8.5, bold=True, color=BLUE)
    s.text(x + 0.05, 1.95, ow - 0.1, 0.9, [{"text": t, "bold": True, "size": 12, "space_after": 2},
                                           {"text": sub, "size": 9.5, "color": SEC}])
s.line(L, 2.9, R, 2.9, AXIS, 1)
crit = ["Per-order economics", "Cash and 12-month runway", "Path to profit within current cash", "Effect on the core software business"]
cells = [
    [("crit", "Fails", "Positive only with better-than-best inputs: +$2.02 in the plan, −$6.17 at the median."),
     ("crit", "Fails", "Same economics at small scale: about −$2.0M a year per store at the median."),
     ("good", "Meets", "Software at 81% gross margin; no exposure to per-order losses.")],
    [("crit", "Fails", "Needs $9.5M against $7.2M available above the 12-month reserve."),
     ("warn", "Partly", "About $2.6M in year one fits, but uses the cushion the software plan relies on."),
     ("good", "Meets", "Cash bottoms at $3.6–5.4M at 45–60% growth; runway stays above 12 months.")],
    [("crit", "Fails", "None at any performance we have observed."),
     ("crit", "Fails", "None; delays the software break-even."),
     ("warn", "Conditional", "Break-even in months 26–32 if growth stays ≥45% and other costs are held (page 11).")],
    [("crit", "Fails", "Makes us a competitor to grocers in our pipeline and splits management attention."),
     ("warn", "Partly", "Smaller conflict, but repeats what the pop-up and the 14-site benchmark already show."),
     ("good", "Meets", "Sells to the trend: several pipeline grocers want fast delivery from their own stores.")],
]
y = 3.0
rhs = [0.92, 0.92, 0.92, 0.92]
for r_, c_ in enumerate(crit):
    s.text(L, y, 2.1, rhs[r_], c_, size=11, bold=True)
    for j, (k, lab, t) in enumerate(cells[r_]):
        x = ox[j + 1]
        status(s, x + 0.05, y + 0.01, k, lab, size=10.5)
        s.text(x + 0.05, y + 0.28, ow - 0.15, rhs[r_] - 0.28, t, size=10, color=SEC)
    y += rhs[r_]
    if r_ < 3:
        s.line(L, y - 0.04, R, y - 0.04, GRID, 0.75)

# ===================================================================== 11. Software path
cs = json.load(open(os.path.join(HERE, "cash_series.json")))
s = new("The alternative: scale the software business",
        "Scaling the software business breaks even within today's cash if growth stays at 45% or more and other costs are held",
        source="Illustrative Parcelbird model: $12.0M cash and $4.1M ARR in January 2027; revenue = ARR; 81% gross margin; operating costs held at "
               "today's implied $8.1M a year (gross profit + $4.8M burn) plus $0.8M for new hires; growth is net of churn. Not a substitute for a bottom-up plan.")
s.text(L, 1.72, 7.3, 0.3, "Cash balance by month under three growth rates for software ARR, $M", size=12, bold=True)
series = [("0.6", "60% a year (today's rate)", BLUE), ("0.45", "45% a year", ORANGE), ("0.3", "30% a year", AQUA)]
lgx = L
for k, lab, col in series:
    s.line(lgx, 2.23, lgx + 0.3, 2.23, col, 2.5)
    s.text(lgx + 0.35, 2.1, 2.2, 0.28, lab, size=10, color=INK)
    lgx += 2.35 if k == "0.6" else 1.4
gx_, gy_top, gy_bot = L + 0.45, 2.6, 6.2
gw_ = 5.25
ymax = 17.0
def GX(m): return gx_ + m / 48 * gw_
def GY(v): return gy_bot - v / ymax * (gy_bot - gy_top)
for v in (0, 4, 8, 12, 16):
    s.line(gx_, GY(v), gx_ + gw_, GY(v), GRID if v else AXIS, 0.5 if v else 1)
    s.text(gx_ - 0.45, GY(v) - 0.12, 0.38, 0.25, f"{v}", size=9, color=MUTED, align="r")
for m, lab in [(0, "Jan 2027"), (12, "Jan 2028"), (24, "Jan 2029"), (36, "Jan 2030"), (48, "Jan 2031")]:
    s.line(GX(m), gy_bot, GX(m), gy_bot + 0.05, AXIS, 0.75)
    s.text(GX(m) - 0.5, gy_bot + 0.07, 1.0, 0.25, lab, size=9, color=MUTED, align="c")
for k, lab, col in series:
    pts = [(GX(m), GY(max(v, 0))) for m, v in cs[k]]
    s.poly(pts, col, 2.0)
# trough markers and direct labels
for k, m, v, col in [("0.6", 25, 5.39, BLUE), ("0.45", 31, 3.58, ORANGE)]:
    s.oval(GX(m) - 0.06, GY(v) - 0.06, 0.12, 0.12, fill=col, line="#ffffff", lw=1.5)
s.text(GX(25) - 0.8, GY(5.39) - 0.3, 1.6, 0.24, "Low $5.4M, month 25", size=9, color=INK, align="c")
s.text(GX(31) - 0.8, GY(3.58) - 0.3, 1.6, 0.24, "Low $3.6M, month 31", size=9, color=INK, align="c")
ends = [("0.6", "60%: $16.3M"), ("0.45", "45%: $7.4M"), ("0.3", "30%: cash ≈ $0 by month 45")]
for k, lab in ends:
    v = cs[k][-1][1]
    yo = -0.55 if k == "0.3" else -0.14
    s.text(GX(48) + 0.08, GY(max(v, 0)) + yo, 1.2, 0.5 if k == "0.3" else 0.28, lab, size=9.5, bold=True, color=INK)
px = 8.15
s.text(px, 1.72, R - px, 0.3, "The pipeline can support the growth", size=12, bold=True)
pipe = [
    "**37 grocers in the pipeline, 9 at the late stage,** at an average $96,000 a year.",
    "**Late-stage deals alone add $0.86M of ARR (+21%);** the whole pipeline would add $3.55M (+87%).",
    "**Growing 60% in 2027 means about $2.5M of new ARR,** roughly 26 contracts at $96,000, net of churn.",
    "**Several pipeline grocers want fast delivery from their own stores,** which needs the inventory, picking and dispatch tools we already sell.",
]
s.text(px, 2.1, R - px, 2.9, [{"text": t, "bullet": True, "size": 11, "space_after": 6, "color": SEC} for t in pipe])
s.rect(px, 5.05, R - px, 1.3, fill=PANEL)
s.text(px + 0.15, 5.13, R - px - 0.3, 1.3,
       [{"text": "Cost discipline matters as much as growth", "bold": True, "size": 11, "space_after": 3},
        {"text": "If other costs rise 10% a year, 60% growth still breaks even (month 32, low of $3.1M), but 45% growth runs out of cash. "
                 "At 30% growth, runway falls below 12 months from month 23 even with costs held flat.", "size": 10.5, "color": SEC}])

# ===================================================================== 12. Recommendation
s = new("Recommendation and next steps",
        "We ask the board to decline Parcelbird Now for 2027, back a software-led plan, and agree in advance what would reopen the question")
c3 = [(L, 3.85), (L + 4.1, 3.95), (L + 8.3, CW - 8.3)]
heads = ["Decide in January", "Next 90 days (management)", "Reopen the operator question only if all three hold"]
bodies = [
    ["**Decline Parcelbird Now for 2027.** No dark stores, no capex.",
     "**Approve $0.8M a year** for 2 engineers and 2 sales hires.",
     "**Adopt a runway floor** of 12 months, reported at every board meeting against a monthly plan.",
     "**Mandate a fast-delivery-from-store offer** for pipeline grocers."],
    ["Put the new sales hires on the **9 late-stage grocers** ($0.86M of ARR).",
     "Scope the store-based offer with **3–5 pipeline grocers** who want fast delivery.",
     "Finance to **replace page 11 with a bottom-up operating plan**, with cost growth explicit.",
     "**Close the pop-up** and confirm how month-three retention was measured."],
    ["**A dark store in our customer network covers its own costs** (positive after store costs) for two consecutive quarters. Today even the best combined inputs give −$1.76 per order.",
     "**Rider minimum-pay rules in the target cities are settled,** and the economics re-tested at the new rate.",
     "**Software is at break-even,** so any venture can be funded without touching the 12-month reserve."],
]
for (x, w_), h_, b_ in zip(c3, heads, bodies):
    s.rect(x, 1.75, w_ - 0.1, 0.45, fill=ACCENT)
    s.text(x + 0.12, 1.75, w_ - 0.3, 0.45, h_, size=11.5, bold=True, color="#ffffff", valign="m")
    s.text(x + 0.05, 2.35, w_ - 0.2, 3.3, [{"text": t, "bullet": True, "size": 12, "space_after": 10} for t in b_])
s.rect(L, 5.6, CW, 0.95, fill=PANEL)
s.text(L + 0.2, 5.65, CW - 0.4, 0.85,
       [{"text": "What we give up", "bold": True, "size": 11.5, "space_after": 2},
        {"text": "A possible first-mover position in Midwest quick commerce. With QuickBasket retreating and Zipcart still losing $1.90 per order at "
                 "$1.2B of revenue, we judge that position to be worth less than the cash and focus it would cost.", "size": 11, "color": SEC}])

# ===================================================================== 13. Appendix A
s = new("Appendix A: per-order build",
        "Per-order economics, line by line, for the four scenarios",
        source="Inputs from Table 3 and section 7 of the briefing pack. Delivery fee is net of the payment cost on it. Annual result = per-order result × orders per day × 365. " + SRC)
ac = [L, L + 5.0, L + 6.9, L + 8.8, L + 10.7]
aw = [5.0, 1.75, 1.75, 1.75, CW - 10.7]
for x, w_, t in zip(ac, aw, ["", "Columbus pop-up", "Benchmark median", "Best seen on every input", "Founders' plan"]):
    s.text(x, 1.68, w_, 0.5, t, size=10.5, bold=True, color=SEC, align="r", valign="b")
s.line(L, 2.22, R, 2.22, AXIS, 1)
arows = [
    ("Inputs", None),
    ("Average order value", ["$31", "$34", "$42", "$45"]),
    ("Promotions, % of order value", ["12%", "6%", "6%", "2%"]),
    ("Orders per rider-hour", ["2.1", "2.4", "3.0", "3.5"]),
    ("Orders per store per day", ["280", "900", "1,400", "1,800"]),
    ("Store fixed cost per year", ["$0.65M", "$1.15M", "$1.15M", "$1.15M"]),
    ("Per order, $", None),
    ("Gross margin on goods (27% of order value)", ["8.37", "9.18", "11.34", "12.15"]),
    ("Promotions", ["−3.72", "−2.04", "−2.52", "−0.90"]),
    ("Delivery fee collected", ["+1.99", "+1.99", "+1.99", "+1.99"]),
    ("Picking and packing labour", ["−3.10", "−3.10", "−3.10", "−3.10"]),
    ("Rider cost ($17.75 an hour ÷ orders per hour)", ["−8.45", "−7.40", "−5.92", "−5.07"]),
    ("Payment processing and packaging", ["−1.30", "−1.30", "−1.30", "−1.30"]),
    ("=Contribution before store costs", ["−6.21", "−2.67", "+0.49", "+3.77"]),
    ("Store fixed cost per order", ["−6.36", "−3.50", "−2.25", "−1.75"]),
    ("=Contribution after store costs", ["−12.57", "−6.17", "−1.76", "+2.02"]),
    ("Annual result per store at that volume", ["−$1.28M", "−$2.03M", "−$0.90M", "+$1.33M"]),
]
y = 2.27
for lab, vals in arows:
    if vals is None:
        s.text(L, y + 0.04, 4, 0.26, lab.upper(), size=9, bold=True, color=ACCENT)
        y += 0.3
        continue
    tot = lab.startswith("=")
    lab = lab.lstrip("=")
    if tot:
        s.rect(L, y, CW, 0.27, fill=PANEL)
    s.text(ac[0], y, aw[0], 0.27, lab, size=10.5, bold=tot)
    for x, w_, v in zip(ac[1:], aw[1:], vals):
        s.text(x, y, w_, 0.27, v, size=10.5, bold=tot, align="r")
    y += 0.27

# ===================================================================== 14. Appendix B
s = new("Appendix B: method and open questions",
        "How we handled gaps in the briefing pack, and what management should confirm",
        source="Source: Parcelbird board briefing pack. The pack labels its company, competitor and market figures as synthetic benchmark data. No external research was used.")
left = [
    "**Two contribution measures.** “Before store costs” covers every per-order cost; “after store costs” also spreads each dark store's fixed cost over its orders. The pack does not define the founders' or incumbents' “contribution per order”, so we show both.",
    "**The $9.5M plan figure.** The pack does not say whether it includes today's $0.4M a month burn, so page 9 shows both readings. The conclusion holds under either.",
    "**Runway** = cash ÷ current monthly burn. We test the reserve at today's burn, the most lenient basis.",
    "**Timing.** The $12.0M is treated as cash available in January 2027; the pack does not date it.",
    "**Software path** (page 11) is a top-down illustration with stated assumptions, not a forecast.",
    "**Pop-up exit rate** of about 410 orders a day assumes steady 18% weekly growth across the six weeks (11,800 orders in total).",
    "**Waterfall** (page 6) is sequential. A different order changes the step sizes, not the end points.",
]
right = [
    "How was 22% month-three retention measured in a six-week test?",
    "Does the $9.5M include today's software burn, and what ramp from launch to 1,800 orders a day does it assume?",
    "Is there evidence from any operator, beyond our 14 sites, of 1,800 orders a day or 3.5 orders per rider-hour?",
    "Which minimum-pay proposals are under discussion, at what rate, and in which two cities?",
    "Which pipeline grocers would see Parcelbird Now as a competitor, and how much ARR do they represent?",
]
s.text(L, 1.72, 7.3, 0.3, "Choices made in this analysis", size=12, bold=True)
s.text(L, 2.08, 7.3, 4.8, [{"text": t, "bullet": True, "size": 11.5, "space_after": 8, "color": SEC} for t in left])
s.rect(8.3, 1.72, R - 8.3, 5.08, fill=PANEL)
s.text(8.5, 1.85, R - 8.7, 0.3, "Open questions for management", size=12, bold=True)
s.text(8.5, 2.25, R - 8.7, 4.4, [{"text": t, "bullet": True, "size": 11.5, "space_after": 10, "color": SEC} for t in right])

# ===================================================================== build
if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    prev = os.path.join(HERE, "preview"); os.makedirs(prev, exist_ok=True)
    for i, sl in enumerate(slides, 1):
        render_png(sl, os.path.join(prev, f"s{i:02d}.png"))
    for msg in check(slides):
        print(msg)
    build_pptx(slides, os.path.join(OUT, "Parcelbird-Now-board-deck.pptx"))
    print("slides:", len(slides))
