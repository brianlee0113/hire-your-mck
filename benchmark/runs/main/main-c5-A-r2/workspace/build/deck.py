import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from lib import *
from model import *

OUT = os.path.join(os.path.dirname(__file__), "..", "deliverable")
PREV = os.path.join(os.path.dirname(__file__), "preview")
os.makedirs(OUT, exist_ok=True); os.makedirs(PREV, exist_ok=True)

def usd(v, sign=True, d=2):
    s = f"${abs(v):,.{d}f}"
    if not sign: return ("−" if v < 0 else "") + s
    return ("+" if v >= 0 else "−") + s

def musd(v, d=1):  # v in dollars -> $xM
    return ("−" if v < 0 else "+") + f"${abs(v)/1e6:.{d}f}M"

D = Deck()
SRC = "Source: Board briefing pack"

# ---------------------------------------------------------------- charts
def waterfall(x, y, w, h, steps, vmin, vmax, label_h=0.62, size=11):
    """steps: (label, value, kind) kind in delta/total. Bars on a common zero axis."""
    ph = h - label_h
    sc = lambda v: y + (vmax - v) / (vmax - vmin) * ph
    n = len(steps); slot = w / n; bw = slot * 0.56
    # recessive grid + zero line
    D.line(x, sc(0), x + w, sc(0), color=INK, width=0.75)
    run, prev_end = 0.0, None
    for i, (lab, v, kind) in enumerate(steps):
        bx = x + i * slot + (slot - bw) / 2
        if kind == "total":
            a, b = 0, v; col = NAVY; run = v
        else:
            a, b = run, run + v; col = BLUE if v >= 0 else ORANGE; run = b
        top, bot = sc(max(a, b)), sc(min(a, b))
        D.rect(bx, top, bw, max(bot - top, 0.012), col)
        if prev_end is not None:
            D.line(bx - (slot - bw), sc(prev_end), bx, sc(prev_end), color=MUTED, width=0.5)
        prev_end = run
        vl = usd(v)
        if bot - top >= 0.34:
            D.text(bx - 0.1, top, bw + 0.2, bot - top, vl, size=size, bold=True, color=WHITE, align="c", anchor="m")
        elif v >= 0:
            D.text(bx - 0.3, top - 0.3, bw + 0.6, 0.28, vl, size=size, bold=kind == "total", align="c", anchor="b")
        else:
            D.text(bx - 0.3, bot + 0.02, bw + 0.6, 0.28, vl, size=size, bold=kind == "total", align="c")
        D.text(x + i * slot + 0.02, y + h - label_h + 0.06, slot - 0.04, label_h, lab, size=10, color=SEC, align="c",
               bold=kind == "total")

def hbars(x, y, w, rows, vmin, vmax, label_w=3.4, row_h=0.62, size=12):
    """rows: (label, value, color, note)."""
    bx0 = x + label_w; bw = w - label_w
    sc = lambda v: bx0 + (v - vmin) / (vmax - vmin) * bw
    for i, (lab, v, col, note) in enumerate(rows):
        cy = y + i * row_h
        D.text(x, cy, label_w - 0.15, row_h, lab, size=size, color=INK, align="r", anchor="m")
        bh = row_h * 0.5
        D.rect(sc(min(0, v)), cy + (row_h - bh) / 2, abs(sc(v) - sc(0)), bh, col)
        if v < 0:
            D.text(sc(v) - 1.0, cy, 0.96, row_h, usd(v), size=size, bold=True, align="r", anchor="m")
        else:
            D.text(sc(v) + 0.05, cy, 1.0, row_h, usd(v), size=size, bold=True, align="l", anchor="m")
    D.line(sc(0), y - 0.05, sc(0), y + len(rows) * row_h + 0.05, color=INK, width=0.75)
    return sc

def table(x, y, cols, rows, size=12, row_h=0.42, header_size=10, bold_first=True, shade=None, aligns=None):
    """cols: list of (header, width). rows: list of lists of strings."""
    aligns = aligns or ["l"] + ["r"] * (len(cols) - 1)
    cx = x; tw = sum(c[1] for c in cols)
    for (hdr, cw), al in zip(cols, aligns):
        D.text(cx, y, cw, 0.5, hdr, size=header_size, color=SEC, bold=True, align=al, anchor="b")
        cx += cw
    D.line(x, y + 0.52, x + tw, y + 0.52, color=INK, width=0.75)
    cy = y + 0.56
    for ri, r in enumerate(rows):
        if shade and ri in shade:
            D.rect(x, cy, tw, row_h, PANEL)
        cx = x
        for ci, ((hdr, cw), al, val) in enumerate(zip(cols, aligns, r)):
            D.text(cx, cy, cw, row_h, val, size=size, align=al, anchor="m", bold=(ci == 0 and bold_first))
            cx += cw
        cy += row_h
        D.line(x, cy, x + tw, cy, color=GRID, width=0.5)
    return cy

def panel(x, y, w, h, head, body, size=13, head_col=BLUE):
    hh = D.measure(head, size + 1, w - 0.4, bold=True)
    if h is None:
        if isinstance(body, list):
            bh = sum(D.measure(b, size, w - 0.4 - 0.22) for b in body) + 0.08 * (len(body) - 1)
        else:
            bh = D.measure(body, size, w - 0.4)
        h = 0.2 + hh + bh + 0.2
    D.rect(x, y, w, h, PANEL)
    D.rect(x, y, 0.06, h, head_col)
    D.text(x + 0.22, y + 0.15, w - 0.4, hh, head, size=size + 1, bold=True)
    if isinstance(body, list):
        D.bullets(x + 0.22, y + 0.2 + hh, w - 0.4, body, size=size, gap=0.08, mcolor=head_col)
    else:
        D.text(x + 0.22, y + 0.2 + hh, w - 0.4, h - hh - 0.3, body, size=size)
    return y + h

def stat(x, y, w, big, small, col=INK, big_size=30, small_size=12):
    D.text(x, y, w, 0.62, big, size=big_size, bold=True, color=col)
    sh = D.measure(small, small_size, w)
    D.text(x, y + 0.64, w, sh, small, size=small_size, color=SEC)
    return y + 0.64 + sh

med, best, best2, plan, pop = S["median"], S["best"], S["best2"], S["plan"], S["popup"]

# ================================================================ 1. Title
D.new_slide()
D.rect(0, 0, 13.333, 7.5, NAVY)
D.text(0.8, 0.9, 6, 0.35, "BOARD MEETING · JANUARY 2027", size=12, bold=True, color="9EC5F4")
D.text(0.8, 1.9, 11.5, 2.1, "Should Parcelbird launch its own quick-commerce grocery delivery service in 2027?",
       size=38, bold=True, color=WHITE)
D.text(0.8, 4.15, 11, 0.9, "An assessment of the Parcelbird Now proposal: 15-minute delivery from nine dark stores in "
       "Columbus, Indianapolis and Kansas City", size=17, color="CDE2FB")
D.line(0.8, 5.35, 4.8, 5.35, color="9EC5F4", width=1.5)
D.text(0.8, 5.5, 11, 0.9, ["Decision required: the board (two founders, two investors)",
                           "Prepared from the board briefing pack only; all figures come from the pack or are calculated from it"],
       size=12, color="CDE2FB", space_after=4)

# ================================================================ 2. Executive summary
D.new_slide()
y0 = D.chrome("Recommendation: do not launch Parcelbird Now in 2027. Put the money into the software business instead",
              SRC + " §§3, 6, 7, 9, 10; Parcelbird analysis. Store cost = dark-store fixed cost per order "
              "($1.15M a year ÷ orders per year).", "Executive summary")
rows = [
    ("Our own data says the orders lose money",
     f"At the median of the 14 dark stores our software already runs, each order loses **${-med['allin']:.2f}** after "
     f"store costs (${-med['var']:.2f} before them). Even the best observed value for every input, combined, still "
     f"loses **${-best['allin']:.2f}**. No site has ever achieved that combination."),
    ("The plan needs four records broken at once",
     f"The founders' **{usd(plan['allin'])}** per order needs a $45 average order, 3.5 orders per rider-hour, "
     f"1,800 orders a day and promotions at 2%. Each is beyond anything a site has achieved. The Columbus pop-up fell short of "
     f"the benchmark median on all four, losing **${-pop['allin']:.2f}** per order."),
    ("It breaks the cash rule even if it works",
     f"Spending $9.5M of $12.0M leaves **$2.5M at month 18**. That is about 6 months of runway at today's burn, half the "
     f"12-month floor. At median economics, nine stores would lose **~$18M a year**, and a new round is 'unlikely'."),
    ("Software is the cheaper way to catch the same growth",
     f"Nine late-stage deals are worth **$0.86M ARR (+21%)**, at 81% gross margin, for $0.8M a year of hires. Pipeline "
     f"grocers want fast delivery from their own stores, which is something we can sell them rather than compete with."),
]
cy = y0 + 0.05
for i, (h, b) in enumerate(rows):
    bh = D.measure(b, 13.5, 8.3)
    rh = max(bh, 0.62) + 0.22
    D.text(0.5, cy, 0.45, 0.45, str(i + 1), size=20, bold=True, color=BLUE)
    D.text(1.0, cy + 0.02, 3.2, rh - 0.1, h, size=14, bold=True)
    D.text(4.4, cy + 0.02, 8.4, bh, b, size=13.5)
    cy += rh
    D.line(0.5, cy - 0.1, 12.83, cy - 0.1, color=GRID, width=0.5)
D.rect(0.5, cy + 0.05, 12.33, 0.62, PANEL)
D.text(0.7, cy + 0.05, 12.0, 0.62, "**Decisions asked of the board:** (1) decline Parcelbird Now as proposed; (2) approve ~$0.8M a year "
       "for software hiring; (3) agree the evidence that would reopen the operator question (p. 12).", size=13, anchor="m")

# ================================================================ 3. Market
D.new_slide()
y0 = D.chrome("Quick commerce is growing ~40% a year, but the operators already in it lose money on every order",
              SRC + " §5, Tables 1–2. EBITDA margin = EBITDA ÷ revenue (calculated).", "Market")
D.text(0.5, y0, 6.0, 0.35, "US quick-commerce grocery GMV, $ billions", size=13, bold=True)
# bar chart
cx0, cy0, cw, chh = 0.7, y0 + 0.6, 5.6, 3.6
vmax = 6.0
yrs = list(GMV.items())
slot = cw / 4; bw = slot * 0.55
base_y = cy0 + chh
for gv in (0, 2, 4, 6):
    yy = base_y - gv / vmax * chh
    D.line(cx0, yy, cx0 + cw, yy, color=GRID if gv else INK, width=0.5 if gv else 0.75)
for i, (yr, v) in enumerate(yrs):
    bx = cx0 + i * slot + (slot - bw) / 2
    top = base_y - v / vmax * chh
    D.rect(bx, top, bw, base_y - top, BLUE)
    D.text(bx - 0.2, top - 0.32, bw + 0.4, 0.3, f"${v:.1f}B", size=12, bold=True, align="c", anchor="b")
    g = f"+{v / yrs[i - 1][1] - 1:.0%} y/y" if i else ""
    D.text(bx - 0.3, base_y + 0.05, bw + 0.6, 0.5, [str(yr), g] if g else str(yr), size=11, color=SEC, align="c")
D.text(0.5, base_y + 0.62, 6.2, 0.5, f"Compound growth 2022–25: **{CAGR:.0%} a year**, consistent with the founders' "
       "'over 40%'.", size=12, color=SEC)
# incumbents
tx = 7.1
D.text(tx, y0, 5.7, 0.35, "Incumbent operators, 2025", size=13, bold=True)
end = table(tx, y0 + 0.4, [("", 1.75), ("Revenue", 1.05), ("EBITDA", 1.0), ("EBITDA margin", 1.0), ("Contribution per order", 0.95)],
            [["Zipcart (national)", "$1,200M", "−$310M", "−26%", "−$1.90"],
             ["QuickBasket (regional)", "$210M", "−$96M", "−46%", "−$3.40"]], size=12, row_h=0.55)
panel(tx, end + 0.3, 5.75, 2.25, "Growth is real. Profit is not.",
      ["The national leader, at $1.2B of revenue, still loses $1.90 on the average order.",
       "The one regional operator closed 4 of its 11 cities in 2025.",
       "'Nobody owns the Midwest' may say more about the economics than about an open opportunity."], size=12)

# ================================================================ 4. Median waterfall
D.new_slide()
y0 = D.chrome(f"At the median of the 14 dark stores our software runs, each order loses ${-med['allin']:.2f}, "
              f"and ${-med['var']:.2f} even before paying for the store",
              SRC + " §6, Table 3 (benchmark median of 14 customer sites, 2025); Parcelbird analysis. Rider cost per order = "
              "$17.75 per hour ÷ 2.4 orders per rider-hour. Store cost = $1.15M ÷ (900 × 365).", "Unit economics")
D.text(0.5, y0, 8.5, 0.35, "Contribution per order at benchmark-median inputs, $", size=13, bold=True)
steps = [("Goods margin\n27% × $34", med["goods"], "delta"), ("Delivery fee", med["fee"], "delta"),
         ("Picking & packing", -med["pick"], "delta"), ("Rider\n$17.75 ÷ 2.4", -med["rider"], "delta"),
         ("Payment & packaging", -med["pay"], "delta"), ("Promotions\n6% of AOV", -med["promo"], "delta"),
         ("Before store cost", med["var"], "total"), ("Store cost\n900 a day", -med["fixed"], "delta"),
         ("After store cost", med["allin"], "total")]
# labels with explicit line breaks -> paragraphs
steps = [(l.split("\n") if "\n" in l else l, v, k) for l, v, k in steps]
waterfall(0.5, y0 + 0.55, 8.6, 4.55, steps, vmin=-7.5, vmax=12.5, label_h=0.75, size=11)
px = 9.5
p_end = panel(px, y0, 3.33, None, "The software edge is already in these numbers",
      "These 14 stores run on Parcelbird software. Running our own stores would not add an advantage they lack.", size=12)
panel(px, p_end + 0.3, 3.33, None, "Rider cost alone sinks the order",
      [f"At $7.40, riders cost more than the goods margin after picking (${med['goods']-med['pick']:.2f}).",
       f"To break even before store costs at a $34 order would take {RPH_NEEDED:.2f} orders per rider-hour. "
       "The observed range is 1.9–3.0."], size=12, head_col=ORANGE)

# ================================================================ 5. Bridge to plan
D.new_slide()
y0 = D.chrome(f"The plan's {usd(plan['allin'])} per order rests on four assumptions holding at once, each beyond "
              "anything a site has achieved",
              SRC + " §6, Table 3 and note; Parcelbird analysis. Bridge applies the plan's inputs one at a time in the order shown; "
              "values are contribution per order after store cost; steps may not sum exactly due to rounding.", "Founders' plan")
D.text(0.5, y0, 6.6, 0.35, "Median to plan: contribution per order after store cost, $", size=13, bold=True)
b = [x["allin"] for x in BRIDGE]
bsteps = [(["Benchmark", "median"], b[0], "total"),
          (["AOV", "$34 → $45"], b[1] - b[0], "delta"),
          (["Promotions", "6% → 2%"], b[2] - b[1], "delta"),
          (["Orders per", "rider-hour", "2.4 → 3.5"], b[3] - b[2], "delta"),
          (["Orders per day", "900 → 1,800"], b[4] - b[3], "delta"),
          (["Founders'", "plan"], b[4], "total")]
waterfall(0.5, y0 + 0.55, 6.4, 4.55, bsteps, vmin=-7.5, vmax=3.5, label_h=0.95, size=12)
tx = 7.3
D.text(tx, y0, 5.5, 0.35, "Each plan input against what has actually been seen", size=13, bold=True)
end = table(tx, y0 + 0.35, [("Input", 1.75), ("Median", 0.8), ("Best seen (range)", 1.35), ("Plan", 0.7), ("Plan vs best", 0.93)],
            [["Average order", "$34", "$42", "$45", "+7%"],
             ["Orders/rider-hour", "2.4", "3.0 (1.9–3.0)", "3.5", "+17%"],
             ["Orders/site/day", "900", "1,400 (400–1,400)", "1,800", "+29%"],
             ["Promotions", "6%", "6%", "2%", "⅓ of best"]], size=12, row_h=0.5)
D.text(tx, end + 0.12, 5.5, 0.6, "The best order value and the best density came from **different sites**. No site has achieved both.",
       size=12, color=SEC)
panel(tx, end + 0.85, 5.53, None, "What the board is really being asked to underwrite",
      f"The plan survives missing any one target ({usd(min(ONE_OFF.values()))} to {usd(max(ONE_OFF.values()))} per order). "
      "But it needs all four together, at levels no site has reached, in cities where density is the biggest open question (§12).",
      size=12)

# ================================================================ 6. Scenarios
D.new_slide()
y0 = D.chrome("Even if every store matched the best observed value on every input, Parcelbird Now would at best "
              "break even per order",
              SRC + " §§6–7; Parcelbird analysis. Nine-store result = contribution after store cost × orders per day × 365 × 9 "
              "(steady state, before launch marketing and head-office cost). Pop-up uses its own $650k annualised site cost.",
              "Scenarios")
D.text(0.5, y0, 8.0, 0.35, "Contribution per order after store cost, $", size=13, bold=True)
rows = [("Columbus pop-up (autumn 2026)", pop["allin"], ORANGE, ""),
        ("Benchmark median (14 sites)", med["allin"], ORANGE, ""),
        ("Best observed on every input*", best["allin"], ORANGE, ""),
        ("…and promotions cut to 2%", best2["allin"], ORANGE, ""),
        ("Founders' plan", plan["allin"], BLUE, "")]
row_h = 0.68
hbars(0.5, y0 + 0.5, 8.3, rows, vmin=-17.0, vmax=4.0, label_w=3.2, row_h=row_h, size=12)
# 9-store column
nx = 9.25
D.text(nx, y0, 3.6, 0.35, "Nine stores, per year", size=13, bold=True)
vals = ["n/a (one temporary site:\n−$1.3M a year)", musd(med["nine_yr"]), musd(best["nine_yr"]), musd(best2["nine_yr"]),
        musd(plan["nine_yr"])]
for i, v in enumerate(vals):
    cy = y0 + 0.5 + i * row_h
    if "\n" in v:
        D.text(nx, cy, 3.6, row_h, v.split("\n"), size=11, color=SEC, anchor="m")
    else:
        D.text(nx, cy, 3.6, row_h, v, size=16, bold=True, anchor="m")
    D.line(nx, cy + row_h, 12.83, cy + row_h, color=GRID, width=0.5)
yb = y0 + 0.5 + 5 * row_h + 0.15
D.text(0.5, yb, 12.3, 0.35, "* AOV $42, 3.0 orders per rider-hour and 1,400 orders a day are each the best seen, but at different sites. "
       "No site has combined them.", size=11, color=SEC)
D.rect(0.5, yb + 0.45, 12.33, 0.75, PANEL)
D.text(0.7, yb + 0.45, 12.0, 0.75, f"Only the founders' plan turns positive. The gap between 'best ever seen' ({usd(best['allin'])}) and the plan "
       f"({usd(plan['allin'])}) is {usd(plan['allin']-best['allin'],sign=False)} per order. That is worth about **$20M a year** across nine stores.", size=13, anchor="m")

# ================================================================ 7. Pop-up
D.new_slide()
y0 = D.chrome("Our own Columbus pop-up fell short of the benchmark median on all four drivers the plan depends on",
              SRC + " §§7–8; Parcelbird analysis. Weekly run-rates assume steady 18% weekly growth across the six weeks "
              "(11,800 orders in total). Payback counts only contribution after store cost and ignores churn after month 3.", "Columbus test")
end = table(0.5, y0, [("Driver", 2.35), ("Pop-up", 1.25), ("Benchmark median", 1.55), ("Founders' plan", 1.45)],
            [["Average order value", "$31", "$34", "$45"],
             ["Promotions, % of AOV", "12%", "6%", "2%"],
             ["Orders per rider-hour", "2.1", "2.4", "3.5"],
             ["Orders per site per day", "280", "900", "1,800"],
             ["Contribution / order after store cost", usd(pop["allin"]), usd(med["allin"]), usd(plan["allin"])]],
            size=12.5, row_h=0.56, shade={4})
D.text(0.5, end + 0.15, 6.6, 1.3,
       [f"Fair caveat: a six-week temporary site is not a mature store. But even the estimated **final-week rate (~{round(POPUP_W6_DAY,-1):,.0f} orders a day)** "
        f"is under half the benchmark median and under a quarter of the plan."], size=12, color=SEC)
px = 7.75
D.text(px, y0, 5.1, 0.35, "Demand is real, but it was bought", size=14, bold=True)
cy = y0 + 0.5
cy = stat(px, cy, 2.4, "18%", "weekly order growth (about 180 → 410 orders a day)", col=BLUE)
stat(px + 2.6, y0 + 0.5, 2.5, "12%", "of order value given away in promotions, twice the benchmark", col=ORANGE)
cy += 0.3
cy2 = stat(px, cy, 2.4, "22%", "of customers still ordering in month 3, against 44% in the survey saying 'weekly'", col=ORANGE)
stat(px + 2.6, cy, 2.5, "$38", "to acquire each customer (paid social and first-order credits)", col=ORANGE)
cy = max(cy2, cy + 1.3) + 0.25
panel(px, cy, 5.08, 6.9 - cy - 0.1, "Acquisition cost is not recovered",
      f"Even at the plan's {usd(plan['allin'])} per order, a $38 customer must place ~{38/plan['allin']:.0f} orders to pay back. "
      f"Retained customers order 3.1 times a month. At pop-up or median economics, payback never comes.", size=12, head_col=ORANGE)

# ================================================================ 8. Zipcart
D.new_slide()
y0 = D.chrome("The one profitable example, Zipcart's densest city, got there by charging customers more, and lost 14% of its volume",
              SRC + " §11 (founders' investor update; Zipcart shareholder letter); Parcelbird analysis. 'Zipcart levers' = add "
              "a $3.99 fee per order, cut promotions to 1% of AOV, and cut orders per day by 14%. Other inputs unchanged.",
              "Counter-evidence")
D.text(0.5, y0, 5.6, 0.35, "What the investor update said, and what it left out", size=13, bold=True)
cy = y0 + 0.5
cy = stat(0.5, cy, 5.4, "+$0.40", "Zipcart contribution per order in its densest city, Q4 2025", col=BLUE)
D.text(0.5, cy + 0.25, 5.5, 0.35, "This came only after:", size=12.5, bold=True)
cy = D.bullets(0.5, cy + 0.65, 5.5, ["A new **$3.99 service fee on every order**",
                                     "Promotions cut to **1% of order value**",
                                     "Order volume in that city then **fell 14%**",
                                     "Across the whole company, Zipcart still loses **$1.90 per order**"], size=12.5, gap=0.1)
D.text(0.5, cy + 0.25, 5.5, 0.9, "The founders' plan cuts promotions to 2% but adds no service fee. It also assumes volume 29% above the "
       "best site, where Zipcart's pricing cost it 14% of its volume.", size=12, color=SEC)
tx = 6.7
D.text(tx, y0, 6.1, 0.35, "Applying Zipcart's levers to our own benchmarks, per order", size=13, bold=True)
end = table(tx, y0 + 0.4, [("", 2.6), ("As is", 1.65), ("With Zipcart levers", 1.85)],
            [["Benchmark median", usd(med["allin"]), usd(ZIP_MEDIAN["allin"])],
             ["Best observed on every input", usd(best["allin"]), usd(ZIP_BEST["allin"])]], size=13, row_h=0.6)
panel(tx, end + 0.35, 6.1, None, "Pricing is the only lever with evidence behind it, and it is untested here",
      ["At median density, even Zipcart's pricing leaves each order losing about $1.",
       "It works only alongside best-ever order value and density, which no site has combined.",
       "Whether customers keep ordering at higher prices is the open question in §12."], size=12)

# ================================================================ 9. Cash
D.new_slide()
y0 = D.chrome("Even on plan, Parcelbird Now breaks the 12-month runway rule. On benchmark economics it would use up the cash",
              SRC + " §§1, 3, 9; Parcelbird analysis. We assume the $9.5M covers the whole company to month 18, the most generous "
              "reading. If it excludes today's $0.4M a month burn, the need is ~$16.7M, more than the cash.", "Cash and runway")
D.text(0.5, y0, 6.3, 0.35, "Cash, $M: founders' plan to month 18", size=13, bold=True)
cx0, base_y, chh = 0.9, y0 + 4.65, 3.9
vmax = 13.0
sc = lambda v: base_y - v / vmax * chh
for gv in (0, 4, 8, 12):
    D.line(cx0, sc(gv), cx0 + 5.6, sc(gv), color=GRID if gv else INK, width=0.5 if gv else 0.75)
bw = 1.15
bars = [("Cash today", 0, CASH, NAVY, f"${CASH:.1f}M"), ("Plan spend to month 18", LEFT, CASH, ORANGE, f"−${PLAN_NEED:.1f}M"),
        ("Left at month 18", 0, LEFT, NAVY, f"${LEFT:.1f}M")]
for i, (lab, a, bb, col, vl) in enumerate(bars):
    bx = cx0 + 0.3 + i * 1.8
    D.rect(bx, sc(bb), bw, sc(a) - sc(bb), col)
    D.text(bx - 0.3, sc(bb) - 0.32, bw + 0.6, 0.3, vl, size=12, bold=True, align="c", anchor="b")
    D.text(bx - 0.3, base_y + 0.05, bw + 0.6, 0.5, lab, size=11, color=SEC, align="c")
D.line(cx0, sc(FLOOR), cx0 + 5.6, sc(FLOOR), color=INK, width=1.25, dash=True)
D.text(cx0 + 3.2, sc(FLOOR) - 0.62, 2.45, 0.6, ["12-month floor at today's", f"$0.4M a month burn: ${FLOOR:.1f}M"], size=10.5,
       color=INK, align="r", anchor="b")
tx = 7.3
cy = stat(tx, y0, 5.5, f"~{LEFT/BURN:.0f} months", f"runway at month 18 if everything goes to plan, half the 12-month floor. "
          f"That is ${FLOOR-LEFT:.1f}M short.", col=ORANGE)
cy = stat(tx, cy + 0.3, 5.5, f"${-med['nine_yr']/1e6:.1f}M a year", "lost by nine stores at benchmark-median economics, "
          "1.5× all the cash we have. Losses would be about $1.5M a month.", col=ORANGE)
panel(tx, cy + 0.35, 5.53, None, "No safety net",
      ["The lead investor calls a new round for a delivery operator 'unlikely in this market'.",
       "The $9.5M assumes the plan's economics. Any shortfall comes straight out of runway."], size=12)

# ================================================================ 10. Risks
D.new_slide()
y0 = D.chrome("Two further risks are not priced into the plan: rider pay rules and conflict with our own software customers",
              SRC + " §§6, 10, 12; Parcelbird analysis. Sensitivity = $1 ÷ orders per rider-hour.", "Risks")
cw = 5.95
e1 = panel(0.5, y0, cw, 3.5, "Rider pay rules could move against us",
      ["Two of the three launch cities are considering **minimum pay standards** for delivery workers.",
       "Riders are already the biggest cost per order: $7.40 at the median, $5.07 in the plan.",
       "Every **+$1 an hour** in rider cost takes **$0.29 to $0.42** off each order (plan to median productivity). "
       "At the plan's volume across nine stores, that is about $1.7M a year.",
       "The plan has no allowance for this."], size=13, head_col=ORANGE)
e2 = panel(0.5 + cw + 0.43, y0, cw, 3.5, "Becoming an operator puts us in competition with our customers",
      ["Our benchmark data comes from **14 customer sites**. Using it to compete with those customers puts their trust at risk.",
       "Of 37 grocers in the pipeline, several want to launch fast delivery **from their own stores**. "
       "Parcelbird Now would compete with them in Columbus, Indianapolis and Kansas City.",
       "Founder time and engineering would be split between running stores and selling software, just as nine "
       "late-stage deals need closing."], size=13, head_col=ORANGE)
D.rect(0.5, max(e1, e2) + 0.3, 12.33, 0.7, PANEL)
D.text(0.7, max(e1, e2) + 0.3, 12.0, 0.7, "**Both risks grow with every store we open, and neither is costed in the $9.5M.** "
       "Better operations cannot remove either of them.", size=13, anchor="m")

# ================================================================ 11. Software
D.new_slide()
y0 = D.chrome("The software business is a cheaper way to ride the same growth: nine late-stage deals would add ~21% to ARR "
              "for $0.8M a year",
              SRC + " §§1, 6, 10; Parcelbird analysis. Pipeline values = deals × $96,000 average contract; close rates are not in the "
              "pack, so the full pipeline is an upper bound.", "The alternative")
sw = 3.0
stat(0.5, y0, sw - 0.2, f"${LATE_ARR/1e6:.2f}M", f"ARR from 9 late-stage deals, +{LATE_ARR/4.1e6:.0%} on today's $4.1M", col=BLUE)
stat(0.5 + sw, y0, sw - 0.2, f"${PIPE_ARR/1e6:.2f}M", "ARR if all 37 pipeline grocers signed (upper bound)", col=BLUE)
stat(0.5 + 2 * sw, y0, sw - 0.2, "81%", "gross margin, on a business already growing 60% a year", col=BLUE)
stat(0.5 + 3 * sw, y0, sw - 0.2, "$0.8M", "a year for 2 engineers and 2 sales hires, the whole cost", col=BLUE)
ty = y0 + 1.45
end = table(0.5, ty, [("", 3.0), ("Parcelbird Now (operator)", 4.6), ("Scale the software (supplier)", 4.73)],
            [["Cash committed", "$9.5M of $12.0M to month 18", "~$0.8M a year"],
             ["Unit economics", f"{usd(med['allin'])} per order at the benchmark median", "81% gross margin"],
             ["Runway rule", "Breached, even on plan (~6 months left)", "Kept"],
             ["Relationship with grocers", "Competitor", "Supplier to their fast delivery"],
             ["Exposure to rider pay rules", "Direct", "Borne by the grocer"]],
            size=12.5, row_h=0.5, aligns=["l", "l", "l"])
D.rect(0.5, end + 0.2, 12.33, 0.8, PANEL)
D.text(0.7, end + 0.2, 12.0, 0.8, f"**Insight:** delivering from grocers' existing stores avoids the $1.15M-a-year dark store. At median "
       f"density that store costs **{usd(med['fixed'],sign=False)} per order**, the biggest single line separating a loss from break-even. "
       "That is the product our pipeline is asking for.", size=13, anchor="m")

# ================================================================ 12. Decisions
D.new_slide()
y0 = D.chrome("We ask the board to decline Parcelbird Now for 2027, fund the software plan, and agree what would reopen the question",
              SRC + "; Parcelbird analysis. 1,400 orders a day is the best density seen at any site (Table 3); pricing evidence on p. 8.",
              "Recommendation")
D.text(0.5, y0, 6.2, 0.35, "Decisions for today", size=14, bold=True)
dec = [("Decline", "the Parcelbird Now launch (nine dark stores, $9.5M) for 2027."),
       ("Approve", "~$0.8M a year for 2 engineers and 2 sales hires, focused on closing the 9 late-stage deals."),
       ("Commission", "a plan for a fast-delivery-from-store module for pipeline grocers, to come to the next board."),
       ("Hold", "cash to the 12-month runway floor. Revisit only through the triggers on the right.")]
cy = y0 + 0.5
for k, v in dec:
    h = D.measure(f"**{k}** {v}", 13, 5.6)
    D.rect(0.5, cy + 0.06, 0.08, h - 0.12, BLUE)
    D.text(0.75, cy, 5.6, h, f"**{k}** {v}", size=13)
    cy += h + 0.22
D.rect(0.5, cy + 0.1, 6.0, 1.15, PANEL)
D.text(0.7, cy + 0.1, 5.7, 1.15, "**Waiting costs us little.** Our software already shows us how every customer site performs. "
       "If a customer's dark store starts to make money, we will see it early in our own data.", size=12.5, anchor="m")
tx = 7.0
D.rect(tx, y0, 5.83, cy + 1.25 - y0, PANEL)
D.text(tx + 0.25, y0 + 0.15, 5.4, 0.35, "What would reopen the operator question", size=14, bold=True)
D.text(tx + 0.25, y0 + 0.55, 5.4, 0.5, "All three, ideally shown first by a customer's site on our platform, at no cost to us:",
       size=12, color=SEC)
D.bullets(tx + 0.25, y0 + 1.15, 5.35,
          ["**Positive contribution after store costs for two quarters in a row** at a site in a mid-size city "
           "doing 1,400+ orders a day",
           "**Evidence that customers accept higher prices**, e.g. a service fee test where order volume holds",
           "**Funding that keeps 12+ months of runway** through the launch, plus clarity on rider pay rules in Indianapolis "
           "and Kansas City"],
          size=12.5, gap=0.18)

# ================================================================ 13. Appendix A: model
D.new_slide()
y0 = D.chrome("Appendix A: per-order model behind every scenario",
              SRC + " Table 3, §7; Parcelbird analysis. All inputs from the pack; only the arithmetic is ours.", "Appendix")
sc_ = [("Pop-up", pop), ("Median", med), ("Best seen*", best), ("Best + 2% promo", best2), ("Founders' plan", plan)]
cols = [("$ per order", 3.4)] + [(n, 1.78) for n, _ in sc_]
def r(label, key, neg=False, fmt=None):
    return [label] + [(fmt(e) if fmt else usd(-e[key] if neg else e[key])) for _, e in sc_]
rows = [
    ["Inputs: AOV / promo / rider-hr / day"] + [f"${e['aov']} / {e['promo_pct']:.0%} / {e['rph']} / {e['opd']:,}" for _, e in sc_],
    r("Goods margin (27% of AOV)", "goods"), r("Delivery fee, net", "fee"), r("Picking & packing", "pick", True),
    r("Rider ($17.75/hr ÷ orders per rider-hr)", "rider", True), r("Payment & packaging", "pay", True), r("Promotions", "promo", True),
    r("Contribution before store cost", "var"), r("Store fixed cost per order", "fixed", True),
    r("Contribution after store cost", "allin"),
    ["Nine stores, $M a year"] + ["n/a"] + [musd(e["nine_yr"]) for _, e in sc_[1:]],
]
end = table(0.5, y0, cols, rows, size=11.5, row_h=0.4, shade={7, 9})
D.text(0.5, end + 0.12, 12.3, 0.6, "* Best observed value for each input, which came from different sites. Pop-up store cost uses its "
       "$650k annualised fixed cost; all others use $1.15M a year.", size=10.5, color=SEC)

# ================================================================ 14. Appendix B: judgment calls
D.new_slide()
y0 = D.chrome("Appendix B: judgment calls and limits of this analysis",
              SRC + "; Parcelbird analysis.", "Appendix")
calls = [
    "**Definition of contribution.** The pack does not define the founders' 'contribution profit'. We show results both before "
    "and after the dark-store fixed cost. The conclusion holds either way: at the median an order loses money even before the store is paid for.",
    "**Cash need.** We read the $9.5M as the total company need to month 18, which is the most favourable reading for the plan. "
    "If it is on top of today's $0.4M a month burn, the plan needs ~$16.7M, more than the $12.0M in the bank.",
    "**Pop-up ramp.** Run-rates of ~180 and ~410 orders a day assume steady 18% weekly growth over six weeks. The pop-up was a temporary "
    "site with a lower $650k fixed cost, so it is evidence on demand and operations, not on mature-store economics.",
    "**Customer payback.** Payback uses contribution after store cost per order and leaves out orders in months 1–2 and churn after month 3, "
    "because the pack has no data on either.",
    "**Zipcart comparison.** We apply Zipcart's fee, promotion and volume changes to our benchmarks with every other input unchanged. "
    "Zipcart's own definition of contribution is not given.",
    "**Not modelled.** Launch marketing, head-office cost and ramp-up losses (all inside the founders' $9.5M), and close rates on the "
    "software pipeline, which the pack does not give.",
]
D.bullets(0.5, y0 + 0.05, 12.3, calls, size=13, gap=0.2)

D.save(os.path.join(OUT, "Parcelbird_Now_board_deck.pptx"), PREV)
print("\n".join(D.warnings) or "no overflow warnings")
