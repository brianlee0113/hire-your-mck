import sys, os
from engine import Deck, WARNINGS, W, H
import model as M

OUT = sys.argv[1] if len(sys.argv) > 1 else "../deliverable"
PREV = sys.argv[2] if len(sys.argv) > 2 else os.environ.get("TMPDIR", "/tmp") + "/pbc5/png"
os.makedirs(PREV, exist_ok=True)

INK, SEC, MUTED = "#111827", "#52514e", "#898781"
GRID, BASE = "#e1e0d9", "#c3c2b7"
BLUE, BLUE_D, BLUE_T = "#2a78d6", "#0d366b", "#e8f1fc"
RED, RED_T = "#d03b3b", "#fbeaea"
ORANGE = "#eb6834"
PANEL = "#f4f4f1"
GREEN = "#006300"
MINUS = "−"

L, R = 0.6, 12.73
CW = R - L


def usd(v, d=2, sign=False):
    s = f"${abs(v):,.{d}f}"
    if v < 0 and round(abs(v), d) > 0:
        return MINUS + s
    return ("+" + s) if sign else s


def musd(v, d=1, sign=False):
    s = f"${abs(v):,.{d}f}M"
    if v < 0:
        return MINUS + s
    return ("+" + s) if sign else s


deck = Deck()
PAGE = [0]


def chrome(tracker, title, source):
    s = deck.new()
    PAGE[0] += 1
    s.text(L, 0.32, 8, 0.2, tracker.upper(), size=9, bold=True, color=BLUE)
    s.text(L, 0.56, CW, 0.9, title, size=22, bold=True, color=INK)
    s.line(L, 1.55, R, 1.55, color=BASE, lw=0.75)
    s.text(L, 7.0, 11.0, 0.3, source, size=8, color=MUTED)
    s.text(R - 0.6, 7.0, 0.6, 0.2, str(PAGE[0]), size=8, color=MUTED, align="r")
    return s


def takeaway(s, x, y, w, h, head, body, fill=BLUE_T, bar=BLUE):
    s.rect(x, y, w, h, fill=fill)
    s.rect(x, y, 0.06, h, fill=bar)
    paras = [{"runs": [(head, {"bold": True})], "size": 12}]
    if body:
        paras += [{"runs": [b] if isinstance(b, str) else b, "space": 5} for b in (body if isinstance(body, list) else [body])]
    s.text(x + 0.22, y + 0.14, w - 0.36, h - 0.24, paras, size=11, color=INK)


def table(s, x, y, widths, rows, row_h=0.36, head_size=10, size=11, aligns=None, fills=None, bold_rows=(),
          colors=None, head_fill=None, valign="m", heights=None):
    n = len(widths)
    aligns = aligns or (["l"] + ["r"] * (n - 1))
    yy = y
    for ri, row in enumerate(rows):
        rh = heights[ri] if heights else row_h
        xx = x
        is_head = ri == 0
        if is_head and head_fill:
            s.rect(x, yy, sum(widths), rh, fill=head_fill)
        for ci, cell in enumerate(row):
            f = fills.get((ri, ci)) if fills else None
            if f:
                s.rect(xx, yy, widths[ci], rh, fill=f)
            col = (colors or {}).get((ri, ci), MUTED if is_head else INK)
            if ci > 0 and isinstance(cell, str) and cell.startswith(MINUS) and not is_head and (ri, ci) not in (colors or {}):
                col = RED
            pad = 0.08
            s.text(xx + pad, yy + 0.02, widths[ci] - 2 * pad, rh - 0.04, cell, size=head_size if is_head else size,
                   bold=is_head or ri in bold_rows, color=col, align=aligns[ci], valign=valign if not is_head else "b")
            xx += widths[ci]
        yy += rh
        s.line(x, yy, x + sum(widths), yy, color=BASE if is_head else GRID, lw=0.75 if is_head else 0.5)
    return yy


def waterfall(s, x, y, w, h, steps, vmin, vmax, label_h=0.62, ticks=None, bar_frac=0.58, lsize=10, cat_size=9):
    """steps: list of (label, value, kind) with kind in {'abs','delta','total'}."""
    plot_h = h - label_h
    sy = lambda v: y + plot_h * (vmax - v) / (vmax - vmin)
    slot = w / len(steps)
    bw = slot * bar_frac
    for t in (ticks or []):
        s.line(x, sy(t), x + w, sy(t), color=GRID, lw=0.5)
        s.text(x - 0.62, sy(t) - 0.09, 0.55, 0.18, usd(t, 0), size=8, color=MUTED, align="r")
    run = 0.0
    prev_level = None
    for i, (lab, v, kind) in enumerate(steps):
        cx = x + slot * i + (slot - bw) / 2
        if kind in ("abs", "total"):
            lo, hi = min(0, v), max(0, v)
            run = v
            col = (BLUE_D if v >= 0 else RED) if kind == "total" else (BLUE if v >= 0 else RED)
        else:
            lo, hi = min(run, run + v), max(run, run + v)
            run += v
            col = BLUE if v >= 0 else RED
        s.rect(cx, sy(hi), bw, max(0.01, sy(lo) - sy(hi)), fill=col)
        if prev_level is not None and kind == "delta" or (prev_level is not None and kind == "total"):
            s.line(cx - (slot - bw), sy(prev_level), cx, sy(prev_level), color=MUTED, lw=0.5)
        prev_level = run
        txt = usd(v, 2, sign=(kind == "delta"))
        if kind == "delta" and sy(lo) - sy(hi) >= 0.34:
            s.text(cx - 0.1, sy(hi), bw + 0.2, sy(lo) - sy(hi), txt, size=lsize, bold=True, color="#ffffff", align="c", valign="m")
        elif v >= 0:
            s.text(cx - 0.25, sy(hi) - 0.24, bw + 0.5, 0.2, txt, size=lsize, bold=kind == "total", color=INK, align="c")
        else:
            s.text(cx - 0.25, sy(lo) + 0.04, bw + 0.5, 0.2, txt, size=lsize, bold=kind == "total", color=RED, align="c")
        s.text(x + slot * i + 0.03, y + plot_h + 0.1, slot - 0.06, label_h - 0.1, lab, size=cat_size,
               color=INK if kind == "total" else SEC, bold=kind == "total", align="c")
    s.line(x, sy(0), x + w, sy(0), color=SEC, lw=1)


SRC = "Source: Parcelbird briefing pack, January 2027; team analysis."

# ======================================================================= 1 Title
s = deck.new(); PAGE[0] += 1
s.rect(0, 0, W, H, fill=BLUE_D)
s.rect(L, 2.2, 0.08, 2.1, fill="#86b6ef")
s.text(L + 0.35, 1.55, 10, 0.3, "BOARD PAPER  ·  JANUARY 2027", size=11, bold=True, color="#9ec5f4")
s.text(L + 0.35, 2.15, 11.5, 1.4, "Should Parcelbird launch its own quick-commerce grocery delivery service in 2027?",
       size=32, bold=True, color="#ffffff")
s.text(L + 0.35, 3.62, 11, 0.8, "Recommendation: no. Do not launch Parcelbird Now in 2027; invest the cash in the software business instead",
       size=16, color="#cde2fb")
s.text(L + 0.35, 6.35, 12, 0.6, ["Prepared for the Parcelbird board (two founders, two investors).",
                                  "Based only on the January 2027 briefing pack; no external research. The pack's figures are synthetic benchmark data."],
       size=10, color="#9ec5f4", space=2)

# ======================================================================= 2 Exec summary
s = chrome("Executive summary",
           "Recommendation: do not launch Parcelbird Now in 2027; put the cash behind the software business instead",
           SRC + " All per-order figures are steady-state contribution after site costs unless stated.")
findings = [
    ("1", "Every order loses money in all the evidence we have.",
     f"At the median of the 14 sites our software runs, an order loses {usd(-M.BENCH['site'])} after site costs "
     f"({usd(-M.BENCH['var'])} even before them). Our own Columbus pop-up lost {usd(-M.POPUP['site'])} an order. The founders' "
     f"{usd(M.PLAN['site'], sign=True)} needs all four main inputs better than the best site has achieved."),
    ("2", "The market is growing, but nobody in it makes money.",
     f"US quick-commerce GMV grew {M.CAGR*100:.1f}% a year in 2022–25, yet Zipcart ({usd(-1.90)}/order) and QuickBasket "
     f"({usd(-3.40)}/order) both lose money. QuickBasket closed 4 of its 11 cities in 2025."),
    ("3", "The plan does not fit within our cash.",
     f"Holding 12 months of runway leaves {musd(M.DEPLOYABLE)} to spend; the plan needs {musd(M.PLAN_NEED)} to month 18, "
     f"and even then it reaches only contribution breakeven, not profit. At median economics, nine stores lose ~{musd(-M.BENCH['annual9']/1e6, 0)} a year, "
     f"more than the {musd(M.CASH)} in the bank."),
    ("4", "The software business is a better use of the same cash.",
     f"About $0.8M a year of hires to work a 37-grocer pipeline (9 at late stage, ≈{musd(M.LATE_ARR, 2)} of ARR). If 60% "
     f"growth holds, our illustrative path breaks even around month {M.SW60['breakeven']} with ≈{musd(M.SW60['min_cash'])} still in the bank."),
]
yy = 1.8
for num, head, body in findings:
    s.rect(L, yy + 0.02, 0.36, 0.36, fill=BLUE, shape="ellipse")
    s.text(L, yy + 0.02, 0.36, 0.36, num, size=12, bold=True, color="#ffffff", align="c", valign="m")
    s.text(L + 0.55, yy, 7.3, 1.2, [{"runs": [(head, {"bold": True, "size": 13})]},
                                    {"runs": [body], "space": 3}], size=11, color=INK)
    yy += 1.27
px, pw = 8.85, R - 8.85
s.rect(px, 1.8, pw, 4.95, fill=BLUE_D)
s.text(px + 0.3, 2.0, pw - 0.6, 0.3, "DECISIONS REQUESTED TODAY", size=10, bold=True, color="#9ec5f4")
asks = [
    ("Decline", " the Parcelbird Now launch (nine dark stores in three cities) for 2027."),
    ("Approve", " about $0.8M a year for 2 engineers and 2 sales hires to scale the software business."),
    ("Direct", " management to scope a store-based fast-delivery offer for the grocers in our pipeline who want one."),
    ("Agree", " the evidence that would reopen the question (slide 13), gathered from customer sites rather than from our own stores."),
]
s.text(px + 0.3, 2.42, pw - 0.6, 4.2,
       [{"runs": [(a, {"bold": True}), b], "space": 10 if i else 0, "bullet": False} for i, (a, b) in enumerate(asks)],
       size=12, color="#ffffff")
s.line(px + 0.3, 5.65, px + pw - 0.3, 5.65, color="#5598e7", lw=0.75)
s.text(px + 0.3, 5.8, pw - 0.6, 0.8, "Parcelbird can profit from quick commerce as the software supplier, without taking on the operator's losses.",
       size=11, italic=True, color="#cde2fb")

# ======================================================================= 3 Market
s = chrome("Market",
           f"Quick commerce is growing over 40% a year, as the founders say, but the operators in it are losing money",
           SRC + " EBITDA margin = EBITDA ÷ revenue. Incumbents may define contribution per order differently from our model.")
s.text(L, 1.8, 5.8, 0.3, "US quick-commerce grocery sales (GMV), $ billions", size=12, bold=True)
cx0, cy0, cw, ch = L + 0.2, 2.35, 5.4, 3.55
vmax = 6.0
sy = lambda v: cy0 + ch * (1 - v / vmax)
for t in (0, 2, 4, 6):
    s.line(cx0, sy(t), cx0 + cw, sy(t), color=GRID if t else SEC, lw=0.5 if t else 1)
    s.text(cx0 - 0.45, sy(t) - 0.09, 0.35, 0.18, f"{t}", size=8, color=MUTED, align="r")
slot = cw / 4
for i, (yr, v) in enumerate(M.GMV.items()):
    bx = cx0 + slot * i + slot * 0.2
    s.rect(bx, sy(v), slot * 0.6, sy(0) - sy(v), fill=BLUE)
    s.text(bx - 0.2, sy(v) - 0.26, slot * 0.6 + 0.4, 0.2, f"${v:.1f}B", size=11, bold=True, align="c")
    s.text(bx - 0.2, sy(0) + 0.08, slot * 0.6 + 0.4, 0.2, str(yr), size=10, color=SEC, align="c")
    if yr > 2022:
        s.text(bx - slot * 0.55, sy(0) + 0.36, slot * 0.7, 0.2, f"+{M.YOY[yr]*100:.0f}%", size=9, color=MUTED, align="c")
s.text(cx0, sy(0) + 0.62, cw, 0.25, f"Year-on-year growth shown between bars; 2022–25 compound annual growth {M.CAGR*100:.1f}%",
       size=9, color=SEC)
rx = 6.85
s.text(rx, 1.8, R - rx, 0.3, "Incumbent operators, 2025", size=12, bold=True)
table(s, rx, 2.25, [1.85, 0.95, 0.95, 1.0, 1.13],
      [["Operator", "Revenue", "EBITDA", "EBITDA margin", "Contribution per order"],
       ["Zipcart (national)", "$1,200M", MINUS + "$310M", MINUS + "26%", MINUS + "$1.90"],
       ["QuickBasket (regional)", "$210M", MINUS + "$96M", MINUS + "46%", MINUS + "$3.40"]],
      row_h=0.42, heights=[0.5, 0.42, 0.42])
s.text(rx, 3.72, R - rx, 0.5, "QuickBasket closed 4 of its 11 cities (36%) in 2025.", size=11, color=INK)
takeaway(s, rx, 4.25, R - rx, 2.0, "Growth is real; profit is not.",
         ["The national leader loses $1.90 on each order at about $1.2B of revenue. A fast-growing market "
          "tells us nothing about whether a new, smaller entrant can make money in it.",
          "“Nobody owns the Midwest”: the pack has no data on Midwest competitors. The regional operator's "
          "retreat suggests the gap may be about economics rather than opportunity."])

# ======================================================================= 4 Benchmark waterfall
B = M.BENCH
s = chrome("Unit economics: benchmark",
           f"At the benchmark median, every order loses {usd(-B['var'])} before site costs and {usd(-B['site'])} after them",
           "Source: Parcelbird briefing pack, Table 3 (median of 14 software-customer sites, 2025); team analysis. "
           "Rider cost = $17.75 per hour ÷ 2.4 orders per rider-hour. Fixed = $1.15M ÷ (900 orders × 365 days).")
s.text(L, 1.8, 8, 0.3, "Contribution per order at benchmark-median inputs, $", size=12, bold=True)
steps = [("Gross margin on goods (27% × $34)", B["gp"], "abs"), ("Delivery fee, net", B["fee"], "delta"),
         ("Picking and packing", -B["pick"], "delta"), ("Rider cost", -B["rider"], "delta"),
         ("Payment and packaging", -B["pay"], "delta"), ("Promotions (6% of AOV)", -B["promo_usd"], "delta"),
         ("Contribution before site costs", B["var"], "total"), ("Dark-store fixed cost", -B["fixed"], "delta"),
         ("Contribution after site costs", B["site"], "total")]
waterfall(s, L + 0.7, 2.3, 7.8, 4.45, steps, -7.5, 12.5, ticks=[-6, -3, 0, 3, 6, 9, 12], label_h=0.68, cat_size=8.5)
takeaway(s, 9.55, 1.85, R - 9.55, 4.9, "The order is underwater before rent.",
         [f"Rider cost is the largest cost: {usd(B['rider'])} an order, {B['rider']/34*100:.0f}% of the basket.",
          "Density spreads the $1.15M fixed cost over more orders, but it cannot fix a negative variable margin. "
          f"However many orders a site handles, the median order still loses {usd(-B['var'])}.",
          "These are not hypothetical figures: they are the median of 14 sites running Parcelbird software today."])

# ======================================================================= 5 Plan vs evidence
s = chrome("Unit economics: founders' plan",
           "The founders' plan turns positive only by beating the best site observed on all four main inputs at once",
           SRC + " Annual figures are steady state for nine stores at 365 days, before head-office costs, launch marketing and ramp-up.")
hdr = ["", "Benchmark median", "Best observed site¹", "Founders' plan", "Plan versus the evidence"]
rows = [hdr,
        ["Average order value", "$34", "$42", "$45", "$3 above the best site"],
        ["Orders per rider-hour", "2.4", "3.0", "3.5", "Above the observed range (1.9–3.0)"],
        ["Orders per site per day", "900", "1,400", "1,800", "Above the observed range (400–1,400)"],
        ["Promotions, % of AOV", "6%", "6%", "2%", "One-third of the level at every site observed"],
        ["Contribution before site costs, per order", usd(M.BENCH["var"]), usd(M.BEST["var"], sign=True), usd(M.PLAN["var"], sign=True), ""],
        ["Contribution after site costs, per order", usd(M.BENCH["site"]), usd(M.BEST["site"]), usd(M.PLAN["site"], sign=True), ""],
        ["Nine-store network, per year", musd(M.BENCH["annual9"] / 1e6), musd(M.BEST["annual9"] / 1e6), musd(M.PLAN["annual9"] / 1e6, sign=True), ""]]
fills = {(r, 3): BLUE_T for r in range(1, 8)}
colors = {(r, 4): RED for r in range(1, 5)}
colors.update({(5, 2): BLUE_D, (5, 3): BLUE_D, (6, 3): BLUE_D, (7, 3): BLUE_D})
yend = table(s, L, 1.8, [3.4, 1.7, 1.75, 1.7, 3.58], rows, row_h=0.47, heights=[0.42] + [0.47] * 7,
             aligns=["l", "r", "r", "r", "l"], fills=fills, bold_rows=(6, 7), colors=colors, size=12)
s.line(L, 1.8 + 0.42 + 0.47 * 4, R, 1.8 + 0.42 + 0.47 * 4, color=SEC, lw=1)
s.text(L, yend + 0.12, CW, 0.4,
       "¹ “Best observed” takes the best value of each input. The best order value and the best density were at different sites; no site has achieved them together.",
       size=9, color=SEC)
takeaway(s, L, 6.05, CW, 0.62,
         "Even at the best of each input, an order still loses $1.76 after site costs. The founders' plan has to beat that on all four inputs together.",
         None)

# ======================================================================= 6 Bridge
s = chrome("Unit economics: what it would take",
           "No single input closes the gap; the plan needs all four to move beyond anything observed",
           SRC + " Bridge steps are applied in the order shown; changing the order changes the size of each step slightly but not the total.")
s.text(L, 1.8, 7, 0.3, "Benchmark median to founders' plan, $ per order after site costs", size=12, bold=True)
bsteps = [("Benchmark median", M.BENCH["site"], "abs")] + [(a, b, "delta") for a, b in M.BRIDGE] + [("Founders' plan", M.PLAN["site"], "total")]
waterfall(s, L + 0.7, 2.35, 6.7, 4.4, bsteps, -7.5, 3.5, ticks=[-6, -4, -2, 0, 2], label_h=0.72)
rx = 8.4
s.text(rx, 1.8, R - rx, 0.3, "Any one input alone, all others at benchmark median", size=12, bold=True)
table(s, rx, 2.15, [2.05, 1.3, 0.98],
      [["To break even, would need…", "Needed", "Best observed"],
       ["Average order value", f"${M.AOV_ALONE:.0f}", "$42"],
       ["Orders per rider-hour", f"{M.RIDERS_ALONE:.1f}", "3.0"],
       ["Orders per site per day", "Not possible²", "1,400"],
       ["Promotions cut to zero", usd(M.PROMO_ZERO), "n/a"]],
      row_h=0.36, size=11, colors={(3, 1): RED, (4, 1): RED})
s.text(rx, 3.98, R - rx, 0.4, "² The order loses money before site costs, so more volume cannot reach breakeven.", size=9, color=SEC)
s.text(rx, 4.45, R - rx, 0.3, "Plan with one input set back to the evidence", size=12, bold=True)
slip_rows = [["Plan, except…", "Per order"]] + [[k, usd(v, sign=True)] for k, v in M.SLIP.items()]
table(s, rx, 4.8, [3.35, 0.98], slip_rows, row_h=0.36, size=11)

# ======================================================================= 7 Pop-up
P = M.POPUP
s = chrome("Columbus pop-up test",
           f"Our own Columbus pop-up did worse than the benchmark median on all four operating inputs, losing {usd(-P['site'])} an order",
           "Source: Parcelbird briefing pack, section 7 (six weeks, one temporary site, autumn 2026); team analysis. Pop-up fixed cost = $650,000 a year ÷ (280 × 365).")
rows = [["", "Columbus pop-up", "Benchmark median", "Founders' plan"],
        ["Average order value", "$31", "$34", "$45"],
        ["Promotions, % of AOV", "12%", "6%", "2%"],
        ["Orders per rider-hour", "2.1", "2.4", "3.5"],
        ["Orders per site per day", "280", "900", "1,800"],
        ["Fixed cost per order", usd(P["fixed"]), usd(M.BENCH["fixed"]), usd(M.PLAN["fixed"])],
        ["Contribution before site costs", usd(P["var"]), usd(M.BENCH["var"]), usd(M.PLAN["var"], sign=True)],
        ["Contribution after site costs", usd(P["site"]), usd(M.BENCH["site"]), usd(M.PLAN["site"], sign=True)]]
table(s, L, 1.85, [2.9, 1.55, 1.6, 1.55], rows, row_h=0.5, heights=[0.42] + [0.5] * 7, bold_rows=(7,),
      fills={(r, 1): RED_T for r in range(1, 8)}, colors={(6, 3): BLUE_D, (7, 3): BLUE_D}, size=12)
rx = 8.6
takeaway(s, rx, 1.85, R - rx, 2.05, "To be fair to the test",
         [f"It ran for six weeks on a temporary site, and orders grew 18% a week. Working back from 11,800 orders, "
          f"the site was running at about {round(M.POPUP_EXIT_PER_DAY, -1):,.0f} orders a day by week six. That is the bottom of the benchmark range, "
          f"less than a quarter of the plan's 1,800."],
         fill=PANEL, bar=MUTED)
takeaway(s, rx, 4.1, R - rx, 1.8, "What it tells us",
         ["The growth was bought with 12% promotions and a $38 acquisition cost. "
          "The founders argue that running the software makes us better operators. The one site we ran ourselves "
          "did worse than our customers' median on all four operating inputs."])

# ======================================================================= 8 Customers
s = chrome("Customers",
           "Demand is shallower than the survey suggests, and at plan economics each customer takes over two years to pay back",
           "Source: Parcelbird briefing pack, section 8; team analysis. Payback assumes no further churn after month three, which flatters the result.")
tiles = [("44%", "of 1,500 Columbus residents aged 25–39 said they would use 15-minute delivery at least weekly", "What people say"),
         ("22%", "of pop-up customers were still ordering in month three, at 3.1 orders a month (less than weekly)", "What customers did"),
         ("$38", "customer acquisition cost in the pop-up (paid social and first-order credits)", "What it cost")]
tw = (CW - 0.5) / 3
for i, (big, txt, lab) in enumerate(tiles):
    tx = L + i * (tw + 0.25)
    s.rect(tx, 1.85, tw, 2.05, fill=PANEL)
    s.text(tx + 0.25, 1.98, tw - 0.5, 0.25, lab.upper(), size=9, bold=True, color=SEC)
    s.text(tx + 0.25, 2.25, tw - 0.5, 0.75, big, size=36, bold=True, color=BLUE_D if i == 0 else INK)
    s.text(tx + 0.25, 3.02, tw - 0.5, 0.8, txt, size=11, color=INK)
s.text(L, 4.15, 7, 0.3, "Months to recover the $38 acquisition cost", size=12, bold=True)
bars = [("Founders' plan, before site costs", M.PAYBACK_MONTHS_PLAN_VAR, f"{usd(M.PLAN['var'], sign=True)}/order"),
        ("Founders' plan, after site costs", M.PAYBACK_MONTHS_PLAN, f"{usd(M.PLAN['site'], sign=True)}/order"),
        ("Benchmark median or pop-up", None, f"{usd(M.BENCH['site'])} / {usd(M.POPUP['site'])} per order")]
bx0, bwid = L + 3.0, 3.6
scale = bwid / 30
for i, (lab, v, sub) in enumerate(bars):
    by = 4.6 + i * 0.68
    s.text(L, by, 2.85, 0.5, [{"runs": [lab]}, {"runs": [(sub, {"color": SEC, "size": 9})]}], size=11, align="r")
    if v:
        s.rect(bx0, by + 0.06, v * scale, 0.32, fill=BLUE)
        s.text(bx0 + v * scale + 0.08, by + 0.08, 1.2, 0.28, f"{v:.0f} months", size=11, bold=True)
    else:
        s.text(bx0 + 0.12, by + 0.08, 3.5, 0.28, "Never: every order adds to the loss", size=11, bold=True, color=RED)
s.line(bx0, 4.55, bx0, 6.6, color=SEC, lw=0.75)
takeaway(s, 8.0, 4.15, R - 8.0, 2.1, "Stated intent overstates use",
         [f"Each customer acquired yields about {M.ORDERS_PER_ACQ_MONTH:.2f} orders a month from month three (22% × 3.1). "
          f"At the plan's {usd(M.PLAN['site'], sign=True)}, recovering $38 takes about {M.PAYBACK_ORDERS_PLAN:.0f} orders.",
          f"A 12-month payback would need about {M.RET_12M*100:.0f}% of customers still ordering at 3.1 a month: more than twice the pop-up's 22%."])

# ======================================================================= 9 Zipcart
s = chrome("The Zipcart precedent",
           "Zipcart's one contribution-positive city shows the price: a $3.99 fee, almost no promotions and 14% fewer orders",
           "Source: Parcelbird briefing pack, section 11 (founders' investor update; Zipcart shareholder letter); team analysis. "
           "The 14% volume loss raises fixed cost per order from $3.50 to $4.07.")
s.text(L, 1.8, 4.2, 0.3, "What happened at Zipcart", size=12, bold=True)
s.text(L, 2.2, 4.1, 3.2,
       [{"runs": ["Contribution turned positive, at ", ("+$0.40 an order", {"bold": True}), ", in its densest city in Q4 2025."]},
        {"runs": ["That followed a ", ("new $3.99 service fee", {"bold": True}), " on every order and a ",
                  ("cut in promotions to 1%", {"bold": True}), " of order value."], "space": 8},
        {"runs": [("Order volume in that city fell 14%", {"bold": True}), " afterwards."], "space": 8},
        {"runs": ["Across the whole company, Zipcart still loses ", ("$1.90 an order", {"bold": True}), "."], "space": 8}],
       size=12, bullet=True)
takeaway(s, L, 5.15, 4.1, 1.15, "Pricing, not density, did the work",
         "The precedent supports charging customers more. It does not support the founders' density-led plan.")
s.text(5.35, 1.8, 7.4, 0.3, "Zipcart's fix applied to our benchmark median, contribution per order after site costs, $", size=12, bold=True)
zsteps = [("Benchmark median", M.BENCH["site"], "abs"), ("$3.99 service fee", M.ZIP_FEE, "delta"),
          ("Promotions 6% → 1%", M.ZIP_PROMO_GAIN, "delta"), ("14% fewer orders", M.ZIP_VOL, "delta"),
          ("Benchmark with Zipcart's fix", M.ZIP["site"], "total")]
waterfall(s, 6.05, 2.35, 6.6, 3.55, zsteps, -7.5, 1.0, ticks=[-6, -4, -2, 0], label_h=0.62, bar_frac=0.5)
s.text(5.35, 6.05, 7.4, 0.75,
       f"Still negative at the median. The same fix at the best observed inputs gives about {usd(M.ZIP_BEST['site'], sign=True)}, but no site has "
       "achieved those inputs together. Whether a fee holds volume can be tested at a customer's site without our own capital.",
       size=11, color=INK)

# ======================================================================= 10 Cash
s = chrome("Cash and runway",
           "The plan breaks the 12-month runway rule even on its own numbers, and a new funding round is unlikely",
           "Source: Parcelbird briefing pack, sections 1, 3 and 9; team analysis. The pack does not say whether the $9.5M includes "
           "today's $0.4M monthly burn, so both readings are shown. Month-18 runway uses the plan's average burn.")
s.text(L, 1.8, 6.5, 0.3, "Cash available against the plan's requirement, $M", size=12, bold=True)
bars = [("Cash in the bank", M.CASH, INK), ("Reserve for 12 months' runway at today's $0.4M/month burn", -M.RESERVE, MUTED),
        ("Available to deploy", M.DEPLOYABLE, BLUE), ("Plan: cash needed to month 18", M.PLAN_NEED, ORANGE)]
lx, bx0, scale = L, L + 2.9, 3.3 / 12
for i, (lab, v, col) in enumerate(bars):
    by = 2.3 + i * 0.78
    s.text(lx, by, 2.75, 0.55, lab, size=11, align="r", valign="m", bold=i in (2, 3))
    if v >= 0:
        s.rect(bx0, by + 0.1, v * scale, 0.36, fill=col)
        s.text(bx0 + v * scale + 0.08, by + 0.13, 0.9, 0.3, musd(v), size=12, bold=True)
    else:
        x0 = bx0 + (M.CASH + v) * scale
        s.rect(x0, by + 0.1, -v * scale, 0.36, fill=col)
        s.text(x0 - 1.0, by + 0.13, 0.92, 0.3, musd(v), size=12, bold=True, color=SEC, align="r")
s.line(bx0, 2.25, bx0, 5.4, color=SEC, lw=0.75)
gx = bx0 + M.DEPLOYABLE * scale
s.line(gx, 3.95, gx, 5.3, color=RED, lw=1)
s.text(gx + 0.05, 5.3, 2.6, 0.3, f"Shortfall: {musd(M.PLAN_NEED - M.DEPLOYABLE)}", size=11, bold=True, color=RED)
s.text(L, 5.85, 6.6, 0.85,
       f"This is the most generous test: once the stores open, the burn rises and so does the 12-month reserve. "
       f"At the benchmark median, the nine stores would lose ~{musd(-M.BENCH['annual9']/1e6, 0)} a year in steady state.",
       size=11, color=INK)
rx = 7.75
s.text(rx, 1.8, R - rx, 0.3, "Two readings of the $9.5M", size=12, bold=True)
takeaway(s, rx, 2.2, R - rx, 1.3, f"If it includes today's burn: {musd(M.ALLIN_M18)} left at month 18",
         [f"That is about {M.ALLIN_RUNWAY_M18:.0f} months of runway at the plan's average burn. On even spending, the "
          f"12-month rule is broken around month {M.ALLIN_BREACH_MONTH:.0f}."], fill=PANEL, bar=ORANGE)
takeaway(s, rx, 3.65, R - rx, 1.4, f"If it is on top of today's burn: cash runs out around month {M.INCR_CASHOUT_MONTH:.0f}",
         [f"Combined burn of ~{musd(M.INCR_BURN, 2)} a month leaves a {musd(-M.INCR_M18)} deficit by month 18."],
         fill=RED_T, bar=RED)
s.text(rx, 5.3, R - rx, 0.7,
       "Either way, month 18 is the plan's contribution breakeven, not company profitability, and the lead investor calls a new round “unlikely”.",
       size=11, color=INK)

# ======================================================================= 11 Other risks
s = chrome("Further risks",
           "Three further risks point the same way: rider pay rules, competing with our own customers, and a distracted core business",
           SRC + " Channel conflict is the team's judgement; the pack contains no direct customer reaction to Parcelbird Now.")
cols = [("Rider pay rules", "Two of our three launch cities are considering minimum pay standards for delivery workers.",
         [f"Every $1 an hour on rider cost adds {usd(M.PER_DOLLAR_HR_BENCH)} to each order at benchmark productivity.",
          f"Across nine stores at median volume, that is ≈{musd(M.PER_DOLLAR_HR_9STORES/1e6)} a year for each $1 an hour.",
          "Rider cost is already the largest cost per order."]),
        ("Competing with our own customers", "Parcelbird Now would run dark stores in the same cities as the grocers we sell software to.",
         ["Several pipeline grocers want to launch their own fast delivery, and Parcelbird would become their rival.",
          "The 9 late-stage deals (≈$0.86M of ARR) are the most exposed.",
          "The risk is untested: we recommend asking 2–3 customers directly before any future decision."]),
        ("A distracted core business", "The software business has 81% gross margin and 60% growth, and needs only ~$0.8M a year to scale.",
         [f"Parcelbird Now would commit {M.PLAN_NEED/M.CASH*100:.0f}% of our cash to an operating business with thin margins.",
          "Founders' time would move from product and sales to rents, riders and stock.",
          "A failed launch would put the software business at risk too."])]
cw3 = (CW - 0.5) / 3
for i, (head, lead, pts) in enumerate(cols):
    x = L + i * (cw3 + 0.25)
    s.rect(x, 1.85, cw3, 0.06, fill=BLUE)
    s.text(x, 2.05, cw3, 0.35, head, size=15, bold=True, color=BLUE_D)
    s.text(x, 2.5, cw3, 1.0, lead, size=12, bold=True, color=INK)
    s.text(x, 3.5, cw3, 2.0, [{"runs": [p], "space": 8 if j else 0} for j, p in enumerate(pts)], size=11, bullet=True)
takeaway(s, L, 5.75, CW, 0.95, "The founders' plan keeps rider cost at today's $17.75 an hour and does not price in either of the other two risks.",
         "Even if the unit economics worked, Parcelbird Now would expose us to higher rider costs, strain customer relationships and pull focus from a business that already works.")

# ======================================================================= 12 Software alternative
s = chrome("The alternative",
           "Backing the software business offers a path to profitability within current cash",
           "Source: Parcelbird briefing pack, sections 1 and 10; team analysis. Illustrative: burn = operating loss, other costs flat, growth compounds monthly; Now lines assume even spending.")
s.text(L, 1.8, 4.6, 0.3, "What we already have", size=12, bold=True)
s.text(L, 2.2, 4.5, 3.0,
       [{"runs": [("$4.1M ARR", {"bold": True}), ", growing 60% a year, at 81% gross margin."]},
        {"runs": [("37 grocers in the pipeline", {"bold": True}), f", 9 at late stage. At $96k per contract that is ≈{musd(M.LATE_ARR, 2)} "
                  f"of late-stage ARR and ≈{musd(M.PIPE_ARR, 2)} if every deal closed."], "space": 8},
        {"runs": [f"Another year of 60% growth means ≈{M.CONTRACTS_60:.0f} new contracts at $96k; the pipeline holds 37."], "space": 8},
        {"runs": [("Demand that fits the product:", {"bold": True}), " several pipeline grocers want fast delivery from their existing stores. "
                  "Our software can serve the quick-commerce trend without us running stores."], "space": 8}],
       size=11, bullet=True)
takeaway(s, L, 5.0, 4.5, 1.05, "Cost: ≈$0.8M a year",
         "2 engineers and 2 sales hires. This raises the burn from $0.40M to ≈$0.47M a month.")
# line chart
s.text(5.55, 1.8, 7.2, 0.3, "Illustrative cash balance by month, $M", size=12, bold=True)
gx0, gy0, gw, gh = 6.15, 2.3, 5.2, 3.75
xmax, ymin, ymax = 36, -6, 12
X = lambda m: gx0 + gw * m / xmax
Y = lambda v: gy0 + gh * (ymax - v) / (ymax - ymin)
for t in (-6, -3, 0, 3, 6, 9, 12):
    s.line(gx0, Y(t), gx0 + gw, Y(t), color=SEC if t == 0 else GRID, lw=1 if t == 0 else 0.5)
    s.text(gx0 - 0.5, Y(t) - 0.09, 0.42, 0.18, (MINUS + str(-t)) if t < 0 else str(t), size=8, color=MUTED, align="r")
for m in (0, 6, 12, 18, 24, 30, 36):
    s.text(X(m) - 0.3, Y(ymin) + 0.06, 0.6, 0.18, str(m), size=8, color=MUTED, align="c")
s.text(gx0, Y(ymin) + 0.26, gw, 0.2, "Months from launch decision", size=8, color=MUTED, align="c")
pth = M.SW60["path"]
for (m1, c1), (m2, c2) in zip(pth[:-1], pth[1:]):
    s.line(X(m1), Y(c1), X(m2), Y(c2), color=BLUE, lw=2.25)
# Parcelbird Now readings (straight-line)
s.line(X(0), Y(12), X(18), Y(M.ALLIN_M18), color=ORANGE, lw=2.25)
s.line(X(0), Y(12), X(18), Y(M.INCR_M18), color=RED, lw=2.25)
for (m, v, col) in [(18, M.ALLIN_M18, ORANGE), (18, M.INCR_M18, RED), (M.SW60["breakeven"], M.SW60["min_cash"], BLUE)]:
    s.rect(X(m) - 0.06, Y(v) - 0.06, 0.12, 0.12, fill=col, shape="ellipse")
s.text(X(M.SW60["breakeven"]) - 1.3, Y(M.SW60["min_cash"]) - 0.62, 2.6, 0.45,
       [{"runs": [("Software-first", {"bold": True})]}, f"breakeven ~month {M.SW60['breakeven']}, {musd(M.SW60['min_cash'])} left"], size=9, align="c")

s.text(X(18) + 0.12, Y(M.ALLIN_M18) - 0.12, 2.3, 0.45,
       [{"runs": [("Parcelbird Now, $9.5M all-in", {"bold": True})]}, f"{musd(M.ALLIN_M18)} at month 18, still burning"], size=9)
s.text(X(18) + 0.12, Y(M.INCR_M18) - 0.2, 2.3, 0.45,
       [{"runs": [("Parcelbird Now, $9.5M on top", {"bold": True})]}, f"{musd(M.INCR_M18)} at month 18"], size=9)
s.text(5.55, 6.5, 7.2, 0.45,
       f"Sensitivity: at 45% growth the software path breaks even ~month {M.SW45['breakeven']} with {musd(M.SW45['min_cash'])} left. "
       f"Below ~35% it does not work within current cash (at 30%, cash runs out first).", size=10, color=SEC)

# ======================================================================= 13 Scorecard + triggers
s = chrome("Options and recommendation",
           "Against the board's own tests, only the software-first option passes; Parcelbird Now should wait for evidence from customer sites",
           SRC + " A smaller test of our own (one or two stores) was considered as a middle option. Each symbol carries a label, so the table does not rely on colour.")
PASS, PART, FAIL = ("●", "Passes", BLUE_D), ("◐", "Partly", ORANGE), ("○", "Fails", RED)
crit = ["Positive unit economics on the evidence", "Fits in cash with ≥12 months' runway", "Path to profitability without a new round", "Risk to the software business"]
opts = [("A. Launch Parcelbird Now as proposed", "9 stores, 3 cities",
         [(FAIL, f"{usd(M.BENCH['site'])}/order at median"), (FAIL, f"Needs $9.5M; {musd(M.DEPLOYABLE)} available"),
          (FAIL, "Contribution breakeven only, at month 18"), (FAIL, "High: competes with customers")]),
        ("B. Smaller own-store test", "1–2 Columbus stores",
         [(FAIL, f"Pop-up {usd(M.POPUP['site'])}; small sites carry more fixed cost per order"), (PART, f"Loses ≈{musd(-M.BENCH['annual_site']/1e6)} per store a year at median, plus $0.6M capex"),
          (FAIL, "Adds losses; no route to profit by itself"), (PART, "Medium: same conflict, smaller scale")]),
        ("C. Software-first, with a store-based fast-delivery offer", "Recommended",
         [(PASS, "81% gross margin software"), (PASS, "+$0.8M/yr; runway rule holds"),
          (PASS, f"Illustrative breakeven ~month {M.SW60['breakeven']} if growth ≥ ~35%"), (PASS, "Low: sells into the trend")])]
cx, colw = L, [2.73] + [2.35] * 4
ty = 1.8
s.text(cx + 0.08, ty, colw[0] - 0.1, 0.45, "Option", size=10, bold=True, color=MUTED, valign="b")
for j, c in enumerate(crit):
    s.text(cx + sum(colw[:j + 1]) + 0.08, ty, colw[j + 1] - 0.16, 0.45, c, size=10, bold=True, color=MUTED, valign="b")
ty += 0.5
s.line(L, ty, L + sum(colw), ty, color=BASE)
for i, (name, sub, cells) in enumerate(opts):
    rh = 0.86
    if i == 2:
        s.rect(L, ty, sum(colw), rh, fill=BLUE_T)
    s.text(cx + 0.08, ty + 0.1, colw[0] - 0.16, rh - 0.12,
           [{"runs": [(name, {"bold": True})]}, {"runs": [(sub, {"color": BLUE_D if i == 2 else SEC, "bold": i == 2, "size": 9})]}], size=11)
    for j, ((sym, word, col), note) in enumerate(cells):
        x = cx + sum(colw[:j + 1]) + 0.08
        s.rect(x, ty + 0.15, 0.14, 0.14, fill=col if sym == "●" else None, line=col, lw=1.5, shape="ellipse")
        if sym == "◐":
            s.rect(x + 0.035, ty + 0.185, 0.07, 0.07, fill=col, shape="ellipse")
        s.text(x + 0.22, ty + 0.1, colw[j + 1] - 0.38, rh - 0.12,
               [{"runs": [(word, {"bold": True, "color": col})]},
                {"runs": [(note, {"size": 9, "color": INK})], "space": 1}], size=11)
    ty += rh
    s.line(L, ty, L + sum(colw), ty, color=GRID, lw=0.5)
s.text(L, ty + 0.18, 5.6, 0.3, "What would reopen the question", size=12, bold=True)
trig = ["A customer site keeps positive contribution after site costs for two consecutive quarters.",
        "A customer site adds a service fee and keeps most of its volume, which Zipcart's 14% loss did not.",
        f"Month-three retention near {M.RET_12M*100:.0f}% (pop-up: 22%), which would recover the $38 acquisition cost within 12 months.",
        "Rider minimum-pay rules in Columbus, Indianapolis and Kansas City are settled and their cost is known."]
s.text(L, ty + 0.55, 6.1, 2.0, [{"runs": [t], "space": 4 if k else 0} for k, t in enumerate(trig)], size=10.5, bullet=True)
nx = 7.1
s.text(nx, ty + 0.18, R - nx, 0.3, "Next 90 days if the board agrees", size=12, bold=True)
nxt = ["Hire the 2 engineers and 2 sales staff; prioritise the 9 late-stage grocers.",
       "Scope a store-based fast-delivery module with 2–3 pipeline grocers.",
       "Add site-level contribution reporting to the software, so the 14 customer sites track the reopening tests.",
       "Bring a first read on the reopening tests to the board in Q3 2027."]
s.text(nx, ty + 0.55, R - nx, 2.0, [{"runs": [t], "space": 4 if k else 0} for k, t in enumerate(nxt)], size=10.5, bullet=True)

# ======================================================================= Appendix A1 sensitivity grid
s = chrome("Appendix A1: sensitivity",
           "Even with the founders' rider and promotion assumptions, the order makes money only at basket sizes and densities no site has reached together",
           SRC + " Cells show contribution per order after site costs ($); outlined cells are outside the range observed at the 14 sites (400–1,400 orders a day).")
panels = [("Benchmark rider productivity (2.4/hr) and promotions (6%)", 2.4, 0.06),
          ("Founders' rider productivity (3.5/hr) and promotions (2%)", 3.5, 0.02)]
for pi, (ttl, rr, pp) in enumerate(panels):
    x0 = L + pi * 6.2
    s.text(x0, 1.8, 5.9, 0.3, ttl, size=12, bold=True)
    s.text(x0 + 1.2, 2.18, 4.6, 0.2, "Orders per site per day", size=9, color=MUTED, align="c")
    s.text(x0, 2.42, 1.15, 0.3, "AOV", size=9, color=MUTED)
    cwid = 4.6 / 5
    for ci, o in enumerate(M.GRID_OPD):
        s.text(x0 + 1.2 + ci * cwid, 2.42, cwid, 0.3, f"{o:,}", size=10, bold=True, color=SEC, align="c")
    for ri, a in enumerate(M.GRID_AOV):
        yy = 2.75 + ri * 0.62
        s.text(x0, yy, 1.1, 0.58, f"${a}", size=11, bold=True, color=SEC, valign="m")
        for ci, o in enumerate(M.GRID_OPD):
            v = M.ue(a, rr, o, pp)["site"]
            out = o > 1400 or o < 400
            fill = (RED_T if v < 0 else BLUE_T)
            s.rect(x0 + 1.2 + ci * cwid + 0.02, yy + 0.02, cwid - 0.04, 0.58, fill=fill,
                   line=MUTED if out else None, lw=0.75)
            s.text(x0 + 1.2 + ci * cwid, yy, cwid, 0.62, usd(v, 2, sign=True), size=11, bold=v >= 0,
                   color=RED if v < 0 else BLUE_D, align="c", valign="m")
s.text(L, 5.4, CW, 0.3, "How to read it", size=12, bold=True)
s.text(L, 5.75, CW, 1.1,
       [{"runs": ["Rows $31 (pop-up), $34 (median), $42 (best), $45 (plan). Columns 280 (pop-up), 400 and 1,400 (ends of the observed range), 900 (median), 1,800 (plan). "
                  "Cells outlined in grey sit outside the observed density range."]},
        {"runs": ["At benchmark rider productivity and promotions, no combination of basket size and density is profitable, including the plan's $45 and 1,800 a day. "
                  "With the founders' assumptions, the order turns positive only from about $42 and 1,400 a day, or $45 and 900, and no site has achieved those together."], "space": 5}],
       size=11, bullet=True)

# ======================================================================= Appendix A2 full unit economics
s = chrome("Appendix A2: unit economics detail",
           "Per-order contribution, line by line, for the four cases used in this paper",
           "Source: Parcelbird briefing pack, Table 3 and section 7; team analysis.")
cases = [("Columbus pop-up", M.POPUP), ("Benchmark median", M.BENCH), ("Best observed¹", M.BEST), ("Founders' plan", M.PLAN)]
rows = [["$ per order"] + [c for c, _ in cases],
        ["Gross margin on goods (27% of AOV)"] + [usd(c["gp"]) for _, c in cases],
        ["+ Delivery fee, net of payment cost"] + [usd(c["fee"]) for _, c in cases],
        [MINUS.join(["", " Picking and packing labour"])] + [usd(-c["pick"]) for _, c in cases],
        [MINUS + " Rider cost ($17.75/hr ÷ orders per rider-hour)"] + [usd(-c["rider"]) for _, c in cases],
        [MINUS + " Payment processing and packaging"] + [usd(-c["pay"]) for _, c in cases],
        [MINUS + " Promotions (% of AOV)"] + [usd(-c["promo_usd"]) for _, c in cases],
        ["= Contribution before site costs"] + [usd(c["var"], sign=True) for _, c in cases],
        [MINUS + " Dark-store fixed cost per order"] + [usd(-c["fixed"]) for _, c in cases],
        ["= Contribution after site costs"] + [usd(c["site"], sign=True) for _, c in cases],
        ["Memo: inputs (AOV / orders per rider-hour / orders per day / promotions)"] +
        [f"${c['aov']} / {c['riders']} / {c['opd']:,} / {c['promo']*100:.0f}%" for _, c in cases]]
colors = {}
for ri in range(1, 11):
    for ci in range(1, 5):
        if rows[ri][ci].startswith(MINUS) and ri in (3, 4, 5, 6, 8):
            colors[(ri, ci)] = INK
for ci in range(1, 5):
    colors[(10, ci)] = SEC
yend = table(s, L, 1.8, [4.5, 1.9, 1.9, 1.9, 1.93], rows, row_h=0.38, heights=[0.4] + [0.38] * 9 + [0.5],
             bold_rows=(7, 9), fills={(r, 4): BLUE_T for r in range(1, 11)}, colors=colors, size=11)
s.text(L, yend + 0.15, CW, 0.5,
       "¹ The best value of each input, which no single site achieved. Pop-up fixed cost: $650,000 a year; all other cases $1.15M a year per site. "
       "Delivery fee and payment and packaging are the same in all cases.", size=9, color=SEC)

# ======================================================================= Appendix A3 assumptions
s = chrome("Appendix A3: method and judgement calls",
           "How the numbers were built, and the judgement calls made where the briefing pack was silent",
           "Source: Parcelbird briefing pack, January 2027. All figures in the pack are synthetic benchmark data; no external research was used.")
left = [("Contribution per order", "AOV × 27% + $1.99 fee − picking − (rider cost per hour ÷ orders per rider-hour) − payment and packaging − promotions. "
                                 "After site costs also subtracts fixed cost ÷ (orders per day × 365)."),
        ("“Best observed”", "Combines the best value of each input across sites, which flatters the case; no single site achieved them together."),
        ("Network totals", "Nine stores at steady state, 365 days a year; excludes head office, launch marketing, capex and ramp-up."),
        ("Incumbent comparison", "Zipcart and QuickBasket contribution figures are from the pack; their definitions may differ from ours.")]
right = [("The $9.5M", "The pack does not say whether it includes today's $0.4M monthly burn. Both readings are shown; the recommendation holds under either."),
         ("Runway rule", "Tested at today's burn (the most favourable test for the plan). Spending is assumed even over 18 months, since the pack gives no phasing."),
         ("Pop-up exit rate", "Back-solved: 11,800 orders over six weeks at 18% weekly growth puts week one at ≈1,250 orders and week six at ≈2,860 (≈410 a day)."),
         ("Software path", "Burn is taken as operating loss, so today's costs are ≈$0.68M a month ($0.28M gross profit + $0.40M burn), plus $0.07M a month for the hires. "
                           "Other costs are held flat and ARR growth compounds monthly. Breakeven ARR ≈$11.0M. Treat it as illustrative, not a forecast."),
         ("Option B", "A smaller own-store test was added as a middle option for comparison; the founders did not propose it.")]
for ci, items in enumerate([left, right]):
    x = L + ci * 6.2
    paras = []
    for k, (h, t) in enumerate(items):
        paras.append({"runs": [(h, {"bold": True, "color": BLUE_D})], "space": 9 if k else 0})
        paras.append({"runs": [t], "space": 2})
    s.text(x, 1.8, 5.95, 5.0, paras, size=10.5)

# ======================================================================= build
os.makedirs(OUT, exist_ok=True)
deck.save_pptx(os.path.join(OUT, "Parcelbird_Now_board_paper_Jan2027.pptx"))
for i in range(len(deck.slides)):
    deck.render_png(i, os.path.join(PREV, f"s{i+1:02d}.png"))
print("\n".join(WARNINGS) or "no layout warnings")
print(len(deck.slides), "slides")
