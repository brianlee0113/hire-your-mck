"""Builds the Parcelbird board deck as a JSON scene for the Swift renderer.
All numbers are computed here from the briefing-pack inputs so the slides stay consistent."""
import json, math, sys

# ---------------------------------------------------------------- model
def unit(aov, rph, opd, promo, fixed=1.15e6, fee=1.99, pick=3.10, rider=17.75, pay=1.30, gm=0.27):
    goods = aov * gm; rc = rider / rph; pr = promo * aov
    var = goods + fee - pick - rc - pay - pr
    fpo = fixed / (opd * 365)
    return dict(aov=aov, rph=rph, opd=opd, promo=promo, goods=goods, fee=fee, pick=pick, rider=rc, pay=pay,
                promo_c=pr, var=var, fpo=fpo, site=var - fpo, annual=(var - fpo) * opd * 365)

MED = unit(34, 2.4, 900, .06)
BEST = unit(42, 3.0, 1400, .06)
PLAN = unit(45, 3.5, 1800, .02)
POP = unit(31, 2.1, 280, .12, fixed=650e3)

def sim(g=0.60, extra_opex=0.8, opex_growth=0.0, months=48, cash=12.0, arr=4.1, oneoff=None):
    opex = (0.81 * arr + 4.8) + extra_opex
    mg = (1 + g) ** (1 / 12); og = (1 + opex_growth) ** (1 / 12)
    rows = [(0, arr, None, cash, None)]; be = None; breach = None; cmin = cash
    for t in range(1, months + 1):
        arr *= mg; opex_t = opex * og ** t
        burn = (opex_t - 0.81 * arr) / 12
        if oneoff: burn += oneoff.get(t, 0)
        cash -= burn
        if be is None and burn <= 0: be = t
        floor = 12 * burn if burn > 0 else 0
        if burn > 0 and cash < floor and breach is None: breach = t
        cmin = min(cmin, cash); rows.append((t, arr, burn, cash, floor))
    return dict(be=be, breach=breach, cmin=cmin, rows=rows)

SW = sim()
# one-store pilot cost build
PILOT_OPD = 600
pilot_var_loss = -MED['var'] * PILOT_OPD * 365 / 1e6
pilot_active = PILOT_OPD * 365 / 12 / 3.1
pilot_cac = pilot_active / 0.22 * 38 / 1e6
PILOT = 0.6 + 1.15 + pilot_var_loss + pilot_cac
PIL = sim(oneoff={t: PILOT / 12 for t in range(1, 13)})
NOWB = sim(extra_opex=0, oneoff={t: 9.5 / 18 for t in range(1, 19)})
cash_out_B = next(t for t, a, b, c, f in NOWB['rows'] if c < 0)
# CAC / customers
orders_m_store = 1800 * 365 / 12
active_store = orders_m_store / 3.1
acq_store = active_store / 0.22
cac_store = acq_store * 38 / 1e6
orders_per_acq_month = 0.22 * 3.1
# pop-up exit rate
gsum = sum(1.18 ** k for k in range(6)); w1 = 11800 / gsum; w6 = w1 * 1.18 ** 5; exit_day = w6 / 7
# market
cagr = (5.1 / 1.8) ** (1 / 3) - 1
# Zipcart playbook applied to the median site
z_var = MED['var'] + 3.99 + (0.06 - 0.01) * 34
z_opd = 900 * 0.86
z_fpo = 1.15e6 / (z_opd * 365)
z_site = z_var - z_fpo
z_be_opd = 1.15e6 / 365 / z_var

stress = []
for g in [0.60, 0.50, 0.40, 0.35, 0.30]:
    s = sim(g=g, months=72); stress.append((f"{int(g*100)}% ARR growth, flat costs", s))
for og in [0.10, 0.15]:
    s = sim(opex_growth=og, months=72); stress.append((f"60% growth, costs +{int(og*100)}%/yr", s))
min_g = None
g = 0.60
while g > 0.2:
    if sim(g=g, months=72)['breach'] is not None:
        min_g = round(g + 0.01, 2); break
    g -= 0.01

def m(x, d=2):
    s = f"{abs(x):,.{d}f}"; return ("−$" if x < 0 else "$") + s
def mabs(x, d=2):
    return f"${abs(x):,.{d}f}"
def fm(x, d=1, unit='M'):
    if abs(x) < 0.05: return '≈$0' + unit
    return ('−$' if x < 0 else '$') + f"{abs(x):,.{d}f}" + unit
def sn(x, d=2):
    return ('−' if x < 0 else '') + f"{abs(x):,.{d}f}"
def sg(x, d=2):
    s = f"{abs(x):,.{d}f}"; return ("−$" if x < 0 else "+$") + s

# ---------------------------------------------------------------- drawing helpers
INK, INK2, MUTED, GRID, BASE = "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7"
BLUE, RED, SURF = "#2a78d6", "#e34948", "#ffffff"
BLUEW, REDW, GRAYW = "#eaf2fc", "#fcebea", "#f3f2ee"
GOOD, WARN, CRIT = "#0ca30c", "#fab219", "#d03b3b"
W, H = 1280, 720
X0, XR = 56, 1224
pages = []
P = None

def new():
    global P; P = []; pages.append(P); P.append(dict(type="rect", x=0, y=0, w=W, h=H, fill=SURF))
def T(x, y, w, h, t=None, size=14, f="R", c=INK, align="left", va="top", lh=1.15, ps=0, indent=0, runs=None):
    e = dict(type="text", x=x, y=y, w=w, h=h, size=size, f=f, c=c, align=align, va=va, lh=lh, ps=ps, indent=indent)
    if runs is not None: e["runs"] = runs
    else: e["t"] = t
    P.append(e)
def R(x, y, w, h, fill=None, stroke=None, sw=1, r=0, corners=None):
    e = dict(type="rect", x=x, y=y, w=w, h=h, fill=fill or "none", stroke=stroke or "none", sw=sw, r=r)
    if corners: e["corners"] = corners
    P.append(e)
def L(x1, y1, x2, y2, c=GRID, sw=1, dash=None):
    e = dict(type="line", x1=x1, y1=y1, x2=x2, y2=y2, stroke=c, sw=sw)
    if dash: e["dash"] = dash
    P.append(e)
def PL(pts, c=BLUE, sw=2, fill=None):
    P.append(dict(type="poly", pts=pts, stroke=c if c else "none", sw=sw, fill=fill or "none"))
def C(cx, cy, r, fill, ring=SURF):
    P.append(dict(type="circle", cx=cx, cy=cy, r=r, fill=fill, ring=ring))
def run(t, f="R", c=None, size=None):
    d = dict(t=t, f=f)
    if c: d["c"] = c
    if size: d["size"] = size
    return d

SECTIONS = ["Market", "Unit economics", "Funding", "Alternatives", "Recommendation"]
def header(title, sec=None, label=None):
    if sec is not None:
        x = X0
        for i, s in enumerate(SECTIONS):
            on = (i == sec)
            T(x, 20, 200, 16, f"{i+1}  {s.upper()}" if i < 4 else s.upper(), size=10, f="B" if on else "R", c=INK if on else MUTED)
            if on: R(x, 37, 150 if i != 4 else 110, 2, fill=BLUE)
            x += 168 if i < 3 else 172
    elif label:
        T(X0, 20, 400, 16, label.upper(), size=10, f="B", c=MUTED)
    T(X0, 48, XR - X0, 66, title, size=23, f="M", c=INK, lh=1.12, va="top")
def footer(src, n):
    L(X0, 676, XR, 676, c=GRID)
    T(X0, 683, 1060, 28, src, size=9.5, c=MUTED, lh=1.1)
    T(XR - 60, 683, 60, 14, str(n), size=9.5, c=MUTED, align="right")

def bullets(x, y, w, h, items, size=13, c=INK, ps=6, lh=1.18, bullet="•"):
    runs = []
    for i, it in enumerate(items):
        end = "\n" if i < len(items) - 1 else ""
        if isinstance(it, list):
            runs.append(run(bullet + "\t")); runs.extend(it); runs.append(run(end))
        else:
            runs.append(run(bullet + "\t" + it + end))
    T(x, y, w, h, runs=runs, size=size, c=c, ps=ps, lh=lh, indent=14)

def table(x, y, colw, rows, rh, size=12, hsize=10.5, header_fill=None, aligns=None, fills=None, bold_first=True, hh=34, pad=8, line_c=GRID, fonts=None):
    """rows[0] = header. rh = row height or list of row heights. fills[(r,c)] = color."""
    aligns = aligns or ["left"] * len(colw)
    rhs = rh if isinstance(rh, list) else [rh] * (len(rows) - 1)
    cy = y
    # header
    cx = x
    for j, cell in enumerate(rows[0]):
        T(cx + pad, cy, colw[j] - 2 * pad, hh - 4, cell, size=hsize, f="B", c=INK2, align=aligns[j], va="bottom", lh=1.1)
        cx += colw[j]
    cy += hh
    L(x, cy, x + sum(colw), cy, c=BASE, sw=1)
    for i, row in enumerate(rows[1:]):
        cx = x
        for j, cell in enumerate(row):
            if fills and (i + 1, j) in fills:
                R(cx + 1, cy + 2, colw[j] - 2, rhs[i] - 3, fill=fills[(i + 1, j)], r=3)
            f = "B" if (j == 0 and bold_first) else "R"
            if fonts and (i + 1, j) in fonts: f = fonts[(i + 1, j)]
            if isinstance(cell, list):
                T(cx + pad, cy + 4, colw[j] - 2 * pad, rhs[i] - 8, runs=cell, size=size, align=aligns[j], va="middle", lh=1.12)
            else:
                T(cx + pad, cy + 4, colw[j] - 2 * pad, rhs[i] - 8, cell, size=size, f=f, align=aligns[j], va="middle", lh=1.12)
            cx += colw[j]
        cy += rhs[i]
        L(x, cy, x + sum(colw), cy, c=line_c)
    return cy

def status(x, y, kind, label, size=12):
    col = {"ok": GOOD, "no": CRIT, "mid": WARN}[kind]
    icon = {"ok": "✓", "no": "✗", "mid": "~"}[kind]
    C(x + 8, y + 9, 8, col, ring=None)
    T(x, y + 1, 16, 16, icon, size=11, f="B", c="#ffffff" if kind != "mid" else INK, align="center")
    T(x + 22, y, 200, 20, label, size=size, f="B", c=INK)

def callout(x, y, w, h, title, body, fill=BLUEW, size=12.5):
    R(x, y, w, h, fill=fill, r=6)
    T(x + 16, y + 12, w - 32, 20, title, size=12, f="B", c=INK)
    if isinstance(body, list):
        bullets(x + 16, y + 36, w - 32, h - 44, body, size=size, ps=4)
    else:
        T(x + 16, y + 36, w - 32, h - 44, body, size=size, c=INK, lh=1.2)

SRC = "Source: Parcelbird briefing pack (synthetic benchmark data)"

# ================================================================ 1. Title
new()
R(0, 0, W, H, fill="#0d366b")
T(X0 + 20, 200, 1000, 30, "PARCELBIRD · BOARD OF DIRECTORS · JANUARY 2027", size=13, f="B", c="#9ec5f4")
T(X0 + 20, 240, 1080, 130, "Should Parcelbird launch its own quick-commerce grocery delivery service in 2027?", size=40, f="M", c="#ffffff", lh=1.1)
T(X0 + 20, 380, 1000, 60, "Assessment of the Parcelbird Now proposal: 15-minute delivery from nine dark stores in Columbus, Indianapolis and Kansas City", size=17, c="#cde2fb", lh=1.25)
R(X0 + 20, 470, 60, 3, fill="#86b6ef")
T(X0 + 20, 490, 1000, 40, "Board pre-read · prepared November 2026 · all figures from the briefing pack, which contains synthetic data", size=12.5, c="#b7d3f6")

# ================================================================ 2. Executive summary
new()
header("Executive summary: do not launch Parcelbird Now in 2027. Grow the software business, which can reach break-even on today’s cash", label="Executive summary")
R(X0, 128, XR - X0, 70, fill="#0d366b", r=6)
T(X0 + 20, 128, XR - X0 - 40, 70, runs=[run("Answer: No. ", "B", "#ffffff"), run(
    "Parcelbird Now loses money on every combination of inputs seen so far, and it would break the board’s 12-month runway floor even if everything went to plan. "
    "Put the cash into the software business instead, including selling fast delivery to grocers, and come back to the operator idea only if the triggers on page 16 are met.", "R", "#ffffff")],
  size=14, va="middle", lh=1.22)
pts = [
    ("1", "The market is growing fast, but nobody is making money from it yet",
     [f"US quick-commerce GMV grew {cagr*100:.0f}% a year from 2022 to 2025 ($1.8B to $5.1B).",
      "Both incumbents lose money (EBITDA −26% and −46% of revenue). The regional player, QuickBasket, closed 4 of its 11 cities in 2025."]),
    ("2", "A Parcelbird dark store loses money unless every input beats the best value observed so far",
     [f"At the 14-site benchmark median a store loses {mabs(MED['site'])} per order after site costs. Taking the best observed value for every input still loses {mabs(BEST['site'])}.",
      f"The founders’ +{mabs(PLAN['site'])} needs four inputs above anything observed. The Columbus pop-up was below the median on all four, and its customers do not order often enough to repay the $38 acquisition cost."]),
    ("3", "The launch breaks the board’s funding rules even if it goes to plan",
     [f"Spending $9.5M by month 18 leaves at most $2.5M, about 6 months of today’s burn. The board’s floor is 12 months, or at least $4.8M.",
      f"At median economics, nine stores would lose about ${-MED['annual']*9/1e6:.0f}M a year. A one-store pilot (about ${PILOT:.1f}M) would breach the floor by month {PIL['breach']}."]),
    ("4", "Growing the software business is the better route to profit, and to quick commerce",
     [f"With $0.8M a year of new hires, the software business breaks even in about {SW['be']} months, with cash bottoming out at ${SW['cmin']:.1f}M. It stays above the floor as long as ARR grows at least {int(min_g*100)}% a year.",
      "There are 37 grocers in the pipeline ($3.6M of annual contract value), and several want fast delivery from their own stores, which Parcelbird can sell them as software."]),
]
y = 214
for num, head, sup in pts:
    T(X0, y, 30, 30, num, size=22, f="B", c=BLUE)
    T(X0 + 36, y + 2, 360, 84, head, size=14.5, f="B", c=INK, lh=1.18)
    bullets(X0 + 420, y + 2, XR - X0 - 420, 88, sup, size=12.5, ps=3)
    y += 98
    if num != "4": L(X0, y - 8, XR, y - 8, c=GRID)
R(X0, 612, XR - X0, 46, fill=GRAYW, r=6)
T(X0 + 16, 612, XR - X0 - 32, 46, runs=[run("Decisions requested (page 14): ", "B"), run("turn down the launch and the pilot; approve $0.8M a year of software hires; fund a fast-delivery offer for grocers; adopt the reopening triggers.")], size=13, va="middle")
footer(SRC + "; team analysis. Calculations on pages 4–12 and in the appendix.", 2)

# ================================================================ 3. Hypothesis test
new()
header("We started from the founders’ answer (‘launch’) and tested the four things it needs to be true. None holds in full, so we changed the answer", label="Approach: testing the founders’ hypothesis")
T(X0, 126, XR - X0, 22, runs=[run("Starting hypothesis (the founders’ view): ", "B"), run("Yes. Launch Parcelbird Now in 2027 with 9 dark stores in 3 cities. Contribution per order turns positive by month 18.")], size=13.5)
rows = [["Test", "What would have to be true", "What the evidence shows", "Verdict", "Page"],
        ["1  Market", "The market is growing, and a regional operator can earn a profit in it",
         f"Growth is real ({cagr*100:.0f}% a year). Profit is not: both incumbents have negative contribution per order, and the regional one is shrinking", "", "4"],
        ["2  Unit economics", "A Parcelbird store makes money per order after site costs on inputs it can actually achieve, and customers repay their acquisition cost",
         f"Stores make money only on the founders’ inputs, all of which are above the best value observed. The pop-up was below the median on all four inputs, and the $38 acquisition cost is not repaid", "", "5–9"],
        ["3  Funding", "The launch fits inside $12.0M while keeping at least 12 months of runway the whole time",
         "At most $2.5M is left at month 18, against a floor of at least $4.8M. If losses run at median levels, the cash runs out within the first year", "", "10"],
        ["4  Alternatives", "Operating stores is a better use of cash and management time than growing the software",
         f"The software business reaches break-even on current cash in about {SW['be']} months, and the grocers in its pipeline want fast-delivery tools", "", "11–13"]]
yb = table(X0, 156, [170, 330, 470, 130, 68], rows, 92, size=12.5, aligns=["left", "left", "left", "left", "center"])
for i in range(4):
    status(X0 + 170 + 330 + 470 + 8, 156 + 34 + i * 92 + 36, "mid" if i == 0 else "no", "Half met" if i == 0 else "Not met")
R(X0, yb + 14, XR - X0, 56, fill=BLUEW, r=6)
T(X0 + 16, yb + 14, XR - X0 - 32, 56, runs=[run("Revised answer: ", "B"), run("No. Do not launch in 2027. Grow the software business, and set measurable triggers for reopening the decision. ")], size=13.5, va="middle")
footer(SRC + "; team analysis.", 3)

# ================================================================ 4. Market
new()
header(f"Quick commerce is growing about {cagr*100:.0f}% a year, but no operator makes money from it and the regional operator is pulling back", sec=0)
T(X0, 130, 560, 20, "US quick-commerce grocery GMV, $B", size=13, f="B")
T(X0, 150, 560, 18, f"Compound growth 2022–25: ({5.1} ÷ {1.8})^(1/3) − 1 = {cagr*100:.1f}% a year", size=11.5, c=INK2)
gmv = [1.8, 2.6, 3.6, 5.1]; yrs = ["2022", "2023", "2024", "2025"]
cx0, cy0, ch = X0 + 40, 600, 380; sc = ch / 6
for v in [0, 2, 4, 6]:
    yy = cy0 - v * sc; L(cx0, yy, cx0 + 480, yy, c=GRID if v else BASE)
    T(cx0 - 40, yy - 8, 32, 16, f"{v}", size=10.5, c=MUTED, align="right")
for i, v in enumerate(gmv):
    xx = cx0 + 60 + i * 120
    R(xx, cy0 - v * sc, 24, v * sc, fill=BLUE, r=4, corners="top")
    T(xx - 30, cy0 - v * sc - 22, 84, 18, f"${v}B", size=12.5, f="B", align="center")
    T(xx - 30, cy0 + 8, 84, 16, yrs[i], size=11.5, c=INK2, align="center")
    if i:
        T(xx - 92, cy0 - (gmv[i-1] + v) / 2 * sc - 44, 80, 16, f"+{(v/gmv[i-1]-1)*100:.0f}%", size=11, c=INK2, align="center")
# right: incumbents
T(640, 130, 584, 20, "Incumbent operators, 2025", size=13, f="B")
rows = [["Operator", "Revenue", "EBITDA", "EBITDA margin", "Contribution / order"],
        ["Zipcart (national)", "$1,200M", "−$310M", "−26%", "−$1.90"],
        ["QuickBasket (regional)", "$210M", "−$96M", "−46%", "−$3.40"]]
table(640, 156, [180, 90, 90, 104, 120], rows, 44, size=12.5, aligns=["left", "right", "right", "right", "right"])
T(640, 290, 584, 18, "EBITDA margin = EBITDA ÷ revenue (e.g., −310 ÷ 1,200 = −25.8%)", size=11, c=MUTED)
callout(640, 320, 584, 150, "What this means for Parcelbird",
        ["QuickBasket closed 4 of its 11 cities (36%) in 2025. It is the closest comparison to a regional newcomer, and it has the worse economics of the two.",
         "‘Nobody owns the Midwest’ may simply mean nobody has made it pay there yet.",
         "Zipcart’s one profitable city needed price rises and lost volume as a result (page 9)."])
callout(640, 486, 584, 114, "Verdict on test 1: half met",
        "The founders are right that demand is growing more than 40% a year. But growth in sales has not produced a pool of profit. Every operator in the briefing pack loses money on each order.", fill=GRAYW)
footer(SRC + ", Tables 1–2 and §5.", 4)

# ================================================================ 5. Unit economics overview
new()
header(f"A dark store loses {mabs(MED['site'])} per order at the benchmark median. Only the founders’ plan makes money, and it beats the best observed value on four inputs", sec=1)
T(X0, 128, 900, 18, "Contribution per order by scenario, $ (inputs from the 14 Parcelbird-software sites, the founders’ plan and the Columbus pop-up)", size=12.5, f="B")
cols = [220, 74, 74, 84, 92, 96, 92]
hdr = ["Scenario", "Order value (AOV)", "Promos, % of AOV", "Orders / rider-hour", "Orders / site / day", "Contribution before site costs", "Site fixed cost / order"]
scen = [("Columbus pop-up (6 weeks)", POP), ("Benchmark median", MED), ("Best observed, each input (never seen together)", BEST), ("Founders’ plan", PLAN)]
rows = [hdr]
fills = {}
for i, (nm, s) in enumerate(scen):
    rows.append([nm, f"${s['aov']}", f"{s['promo']*100:.0f}%", f"{s['rph']}", f"{s['opd']:,}", ("+" if s['var'] > 0 else "") + m(s['var']), m(-s['fpo'])])
for j in (1, 2, 3, 4): fills[(4, j)] = REDW
ty = 156
yb = table(X0, ty, cols, rows, 64, size=12.5, aligns=["left"] + ["right"] * 6, fills=fills, hh=44)
# bar chart column
bx0, bw = X0 + sum(cols) + 20, XR - (X0 + sum(cols) + 20)
T(bx0, ty, bw, 40, "Contribution after site costs, $ per order", size=10.5, f="B", c=INK2, va="bottom")
lo, hi = -16.5, 3.5
zx = bx0 + (0 - lo) / (hi - lo) * bw
def xs(v): return bx0 + (v - lo) / (hi - lo) * bw
L(zx, ty + 44, zx, yb, c=BASE)
for i, (nm, s) in enumerate(scen):
    cyy = ty + 44 + i * 64 + 32
    v = s['site']
    if v < 0:
        R(xs(v), cyy - 12, zx - xs(v), 24, fill=RED, r=4, corners="left")
        T(xs(v) - 70, cyy - 9, 64, 18, m(v), size=12.5, f="B", align="right")
    else:
        R(zx, cyy - 12, xs(v) - zx, 24, fill=BLUE, r=4, corners="right")
        T(xs(v) + 6, cyy - 9, 64, 18, "+" + m(v), size=12.5, f="B")
R(X0, yb + 14, 14, 14, fill=REDW, r=3)
T(X0 + 20, yb + 13, 700, 18, "Shaded cells are founders’ inputs outside the range seen at the 14 benchmark sites", size=11, c=INK2)
callout(X0, yb + 42, 560, 140, "How to read this",
        [f"Contribution per order = AOV × 27% goods margin + $1.99 delivery fee − $3.10 picking − rider cost ($17.75 ÷ orders per rider-hour) − $1.30 payment and packaging − promotions",
         "Site fixed cost per order = $1.15M a year ÷ (orders per day × 365). For the pop-up, $650k a year"], size=11.5)
callout(X0 + 580, yb + 42, XR - X0 - 580, 140, "So what",
        [f"Even at the median, each order loses {mabs(MED['var'])} before rent. More volume makes that worse, not better",
         f"Best observed values combined still lose {mabs(BEST['site'])} per order. At those inputs a site would need {1.15e6/365/BEST['var']:,.0f} orders a day to break even, 4.6× the best site seen",
         f"At full volume, nine stores would earn +${PLAN['annual']*9/1e6:.0f}M a year on the plan’s inputs and lose ${-MED['annual']*9/1e6:.0f}M at median"], fill=GRAYW, size=11.5)
footer(SRC + ", Table 3 (§6) and §7; team analysis. Line-by-line build in appendix A1.", 5)

# ================================================================ 6. Sensitivity waterfall
new()
p = PLAN['site']
a1 = unit(34, 3.5, 1800, .02)['site']; a2 = unit(34, 3.5, 1800, .06)['site']; a3 = unit(34, 2.4, 1800, .06)['site']; a4 = MED['site']
header(f"The plan has no margin for error. Moving any single input back to the benchmark median wipes out 87–136% of its profit per order", sec=1)
T(X0, 128, 640, 18, "Bridge from founders’ plan to benchmark median, contribution after site costs, $ per order", size=12.5, f="B")
steps = [("Founders’ plan", p, "total"), ("AOV $45 → $34", a1 - p, "d"), ("Promos 2% → 6%", a2 - a1, "d"),
         ("Riders 3.5 → 2.4 orders/hr", a3 - a2, "d"), ("Volume 1,800 → 900 orders/day", a4 - a3, "d"), ("Benchmark median", a4, "total")]
gx0, gy_top, gh, gw = X0 + 40, 170, 400, 600
vmax, vmin = 3, -7
def gy(v): return gy_top + (vmax - v) / (vmax - vmin) * gh
for v in range(vmin, vmax + 1):
    L(gx0, gy(v), gx0 + gw, gy(v), c=BASE if v == 0 else GRID)
    if v % 1 == 0: T(gx0 - 40, gy(v) - 8, 32, 16, f"{v:+d}" if v else "0", size=10.5, c=MUTED, align="right")
run_v = 0; slot = gw / len(steps)
for i, (lab, v, kind) in enumerate(steps):
    xx = gx0 + i * slot + slot / 2 - 12
    if kind == "total":
        top, bot = max(v, 0), min(v, 0); col = BLUE if v > 0 else RED; run_v = v
        R(xx, gy(top), 24, gy(bot) - gy(top), fill=col, r=4, corners="top" if v > 0 else "bottom")
        lbl = ("+" if v > 0 else "") + m(v); ly = gy(top) - 22 if v > 0 else gy(bot) + 6
    else:
        start, end = run_v, run_v + v
        R(xx, gy(start), 24, gy(end) - gy(start), fill="#f4a3a2", r=2)
        L(xx - slot + 24 + 12 if i else xx, gy(start), xx, gy(start), c=MUTED)
        lbl = m(v); ly = gy(end) + 6; run_v = end
    T(xx - 40, ly, 104, 18, lbl, size=12.5, f="B", align="center")
    T(gx0 + i * slot + 4, gy(vmin) + 10, slot - 8, 40, lab, size=11, c=INK2, align="center", lh=1.1)
L(gx0 + 4 * slot + slot / 2 + 12, gy(a3), gx0 + 4 * slot + slot / 2 - 12, gy(a3), c=MUTED)
T(X0, 630, 640, 34, "Steps are applied in the order shown. AOV is the biggest lever because the goods margin (27%) and promotions both scale with order value.", size=11, c=MUTED, lh=1.15)
# right: single-input reversion
rx = 740
T(rx, 128, XR - rx, 18, "Reverting one input at a time to the median", size=12.5, f="B")
rev = [("AOV $45 → $34", unit(34, 3.5, 1800, .02)['site']), ("Riders 3.5 → 2.4 /hr", unit(45, 2.4, 1800, .02)['site']),
       ("Promos 2% → 6%", unit(45, 3.5, 1800, .06)['site']), ("Volume 1,800 → 900/day", unit(45, 3.5, 900, .02)['site'])]
rows = [["Input changed (others at plan)", "Profit / order after change", "Share of plan profit wiped out"]]
for lab, v in rev:
    rows.append([lab, ("+" if v > 0 else "") + m(v), f"{(p - v) / p * 100:.0f}%"])
yb = table(rx, 156, [200, 130, 154], rows, 40, size=12.5, aligns=["left", "right", "right"], hh=40)
T(rx, yb + 6, XR - rx, 30, f"Plan profit = +{m(p)} per order. Share wiped out = (plan − after) ÷ plan", size=11, c=MUTED)
rows = [["Plan input", "Plan", "Best observed", "Above best by"],
        ["Order value (AOV)", "$45", "$42", "+7%"], ["Orders / rider-hour", "3.5", "3.0 (top of range)", "+17%"],
        ["Orders / site / day", "1,800", "1,400 (top of range)", "+29%"], ["Promotions, % of AOV", "2%", "6% at every site", "−4 pts"]]
T(rx, yb + 46, XR - rx, 18, "Every key plan input is outside the observed range", size=12.5, f="B")
table(rx, yb + 66, [170, 70, 150, 94], rows, 32, size=12, aligns=["left", "right", "right", "right"], hh=30)
footer(SRC + ", Table 3; team analysis. The best AOV and best volume come from different sites, and no site achieved both.", 6)

# ================================================================ 7. Pop-up
new()
header("The Columbus pop-up was below the benchmark median on every key input, so there is no evidence yet that Parcelbird runs dark stores better than others", sec=1)
rows = [["Metric", "Columbus pop-up", "Benchmark median", "Founders’ plan", "Pop-up vs plan"],
        ["Order value (AOV)", "$31", "$34", "$45", "−31%"],
        ["Promotions, % of AOV", "12%", "6%", "2%", "6× plan"],
        ["Orders / rider-hour", "2.1", "2.4", "3.5", "−40%"],
        ["Orders / site / day", f"280 avg (≈{round(exit_day,-1):,.0f} in week 6)", "900", "1,800", f"−84% (−{(1-exit_day/1800)*100:.0f}% at exit)"],
        ["Contribution before site costs", m(POP['var']), m(MED['var']), "+" + m(PLAN['var']), ""],
        ["Contribution after site costs", m(POP['site']), m(MED['site']), "+" + m(PLAN['site']), ""]]
fills = {(i, 1): REDW for i in range(1, 7)}
yb = table(X0, 132, [230, 200, 130, 120, 160], rows, 44, size=12.5, aligns=["left", "right", "right", "right", "right"], fills=fills)
R(X0, yb + 12, 14, 14, fill=REDW, r=3); T(X0 + 20, yb + 11, 700, 18, "Shaded: pop-up result worse than the benchmark median", size=11, c=INK2)
T(X0, yb + 40, 840, 50, f"Pop-up site cost per order = $650k ÷ (280 × 365) = {m(POP['fpo'])}. Week-6 run rate: week-1 orders = 11,800 ÷ Σ1.18^k (k = 0…5) = {w1:,.0f}; week 6 = {w1:,.0f} × 1.18^5 = {w6:,.0f} orders, or ≈{round(exit_day,-1):,.0f} a day.", size=11, c=MUTED, lh=1.2)
rx = X0 + 860
callout(rx, 132, XR - rx, 200, "In fairness to the pop-up",
        ["It ran for six weeks from a temporary site, so launch promotions and low volume are to be expected",
         "Orders grew 18% a week. Even so, the week-6 rate of about 410 a day sits at the bottom of the benchmark range (400–1,400)"], fill=GRAYW, size=12)
callout(rx, 348, XR - rx, 190, "Why ‘we run them better’ is unproven",
        ["The 14 benchmark sites already run on Parcelbird software, so the median already includes whatever the software adds",
         "Parcelbird’s own site came in below those customers on every input"], size=12)
footer(SRC + ", §6–7; team analysis.", 7)

# ================================================================ 8. Customers
new()
header("Customers do not stay long enough to repay the $38 acquisition cost, and the plan’s volumes imply about $27M of acquisition spend against a $9.5M budget", sec=1)
cw = (XR - X0 - 40) / 3
# panel 1
x1 = X0
T(x1, 130, cw, 18, "A. What people say vs. what they did", size=13, f="B")
R(x1, 158, cw, 130, fill=GRAYW, r=6)
T(x1 + 16, 164, 160, 58, "44%", size=40, f="M", c=INK)
T(x1 + 16, 216, cw - 32, 70, "of 1,500 Columbus residents aged 25–39 said they would use 15-minute delivery ‘at least weekly’ (survey)", size=11.5, c=INK2, lh=1.2)
R(x1, 300, cw, 130, fill=GRAYW, r=6)
T(x1 + 16, 306, 160, 58, "22%", size=40, f="M", c=INK)
T(x1 + 16, 358, cw - 32, 70, "of pop-up customers were still ordering in month 3, at 3.1 orders a month, which is less than once a week", size=11.5, c=INK2, lh=1.2)
T(x1, 444, cw, 170, "These are different measures, so they cannot be compared directly. But actual behavior is the more reliable signal. Across all customers acquired, that works out to 0.22 × 3.1 = 0.68 orders per customer per month from month 3.", size=11.5, c=INK, lh=1.22)
# panel 2
x2 = X0 + cw + 20
T(x2, 130, cw, 18, "B. Can a customer repay $38?", size=13, f="B")
rows = [["Scenario", "Contribution / order (before site costs)", "Orders to repay $38", "Months at 0.68 orders / month"],
        ["Founders’ plan", "+" + m(PLAN['var']), f"{38/PLAN['var']:.0f}", f"≈{38/PLAN['var']/orders_per_acq_month:.0f}"],
        ["Best observed", "+" + m(BEST['var']), f"{38/BEST['var']:.0f}", f"≈{38/BEST['var']/orders_per_acq_month:.0f}"],
        ["Median", m(MED['var']), "Never", "Never"],
        ["Pop-up", m(POP['var']), "Never", "Never"]]
yb = table(x2, 158, [118, 92, 66, cw - 276], rows, 40, size=12, aligns=["left", "right", "right", "right"], hh=58, hsize=10)
T(x2, yb + 10, cw, 120, "Months to repay = orders needed ÷ 0.68. This assumes no further churn after month 3, so the true figures are worse. Even on the plan’s inputs, repayment takes more than a year. At the median, every order adds to the loss.", size=11.5, c=INK, lh=1.22)
# panel 3
x3 = X0 + 2 * (cw + 20)
T(x3, 130, cw, 18, "C. Acquisition spend implied by the plan", size=13, f="B")
chain = [("Orders per store per month", f"1,800 × 365 ÷ 12 = {orders_m_store:,.0f}"),
         ("Active customers needed", f"÷ 3.1 orders each = {active_store:,.0f}"),
         ("Customers to acquire", f"÷ 22% retained = {acq_store:,.0f}"),
         ("Acquisition cost per store", f"× $38 = ${cac_store:.2f}M"),
         ("Nine stores", f"× 9 = ${cac_store*9:.1f}M")]
yy = 158
for i, (k, v) in enumerate(chain):
    last = i == len(chain) - 1
    R(x3, yy, cw, 54, fill=REDW if last else GRAYW, r=6)
    T(x3 + 14, yy + 7, cw - 28, 18, k, size=11, c=INK2)
    T(x3 + 14, yy + 25, cw - 28, 22, v, size=14, f="B" if last else "M", c=INK)
    yy += 62
T(x3, yy + 4, cw, 110, "The whole plan budget is $9.5M, including capex and operating losses. Rough sizing: it ignores orders from customers in months 1–2, which would lower the figure, and churn after month 3, which would raise it.", size=11.5, c=INK, lh=1.22)
footer(SRC + ", §8; team analysis. Contribution per order from page 5.", 8)

# ================================================================ 9. Zipcart
new()
header(f"Zipcart’s one profitable city shows what profit costs. Copying its fee and promotion moves would still leave a median Parcelbird site losing {mabs(z_site)} per order", sec=1)
T(X0, 128, 640, 18, "Median Parcelbird site with Zipcart’s Q4 2025 changes, contribution after site costs, $ per order", size=12.5, f="B")
steps = [("Median site today", MED['site'], "total"), ("+ $3.99 service fee on every order", 3.99, "d"),
         ("Promotions 6% → 1% of $34 AOV", 0.05 * 34, "d"), (f"14% fewer orders ({z_opd:,.0f}/day) spreads site cost over less volume", -(z_fpo - MED['fpo']), "d"),
         ("Median site with Zipcart’s changes", z_site, "total")]
gx0, gy_top, gh, gw = X0 + 40, 170, 380, 620
vmax, vmin = 1, -7
def gy2(v): return gy_top + (vmax - v) / (vmax - vmin) * gh
for v in range(vmin, vmax + 1):
    L(gx0, gy2(v), gx0 + gw, gy2(v), c=BASE if v == 0 else GRID)
    T(gx0 - 40, gy2(v) - 8, 32, 16, f"{v:+d}" if v else "0", size=10.5, c=MUTED, align="right")
run_v = 0; slot = gw / len(steps)
for i, (lab, v, kind) in enumerate(steps):
    xx = gx0 + i * slot + slot / 2 - 12
    if kind == "total":
        R(xx, gy2(0), 24, gy2(v) - gy2(0), fill=RED, r=4, corners="bottom"); run_v = v
        T(xx - 40, gy2(v) + 6, 104, 18, m(v), size=12.5, f="B", align="center")
    else:
        s0, e0 = run_v, run_v + v
        col = "#86b6ef" if v > 0 else "#f4a3a2"
        R(xx, gy2(max(s0, e0)), 24, abs(gy2(e0) - gy2(s0)), fill=col, r=2)
        T(xx - 40, gy2(max(s0, e0)) - 22, 104, 18, sg(v), size=12.5, f="B", align="center")
        run_v = e0
    T(gx0 + i * slot + 2, gy2(vmin) + 10, slot - 4, 54, lab, size=11, c=INK2, align="center", lh=1.1)
T(X0, 618, 660, 50, "Generous assumptions: the fee is taken as net of payment costs, and AOV and rider productivity stay unchanged after the volume loss. Site cost per order rises from $1.15M ÷ (900 × 365) = $3.50 to $1.15M ÷ (774 × 365) = $4.07.", size=11, c=MUTED, lh=1.18)
rx = 760
callout(rx, 128, XR - rx, 196, "What Zipcart actually did (shareholder letter)",
        ["Added a $3.99 service fee to every order and cut promotions to 1% of order value",
         "Order volume in that city then fell 14%",
         "Result: +$0.40 contribution per order in its densest city only. Group EBITDA is still −$310M"], fill=GRAYW, size=12)
callout(rx, 340, XR - rx, 270, "Implications for Parcelbird Now",
        [f"With Zipcart’s changes, a median site turns positive before site costs (+{m(z_var)} per order). Covering site costs as well would take {z_be_opd:,.0f} orders a day after the volume loss, or {z_be_opd/0.86:,.0f} before it, which is {(z_be_opd/0.86/900-1)*100:.0f}% above the median",
         "The founders’ plan assumes promotions of 2% and no service fee, so it does not use this lever",
         "Higher fees work against the impulse, convenience use that quick commerce depends on (uncertainty noted in the briefing pack)"], size=12)
footer(SRC + ", §11 and Table 3; team analysis.", 9)

# ================================================================ 10. Funding
new()
header("Even if everything goes to plan, the launch leaves at most $2.5M by month 18, about half the board’s 12-month runway floor", sec=2)
T(X0, 128, 660, 18, "Cash, $M: plan as stated vs. if the $9.5M is in addition to today’s burn", size=12.5, f="B")
gx0, gy_top, gh, gw = X0 + 40, 170, 380, 640
vmax, vmin = 13, -6
def gy3(v): return gy_top + (vmax - v) / (vmax - vmin) * gh
for v in [-6, -3, 0, 3, 6, 9, 12]:
    L(gx0, gy3(v), gx0 + gw, gy3(v), c=BASE if v == 0 else GRID)
    T(gx0 - 40, gy3(v) - 8, 32, 16, f"{v}", size=10.5, c=MUTED, align="right")
bars = [("Cash today", 12.0, "total", BLUE), ("Parcelbird Now spend to month 18 (capex, launch, losses)", -9.5, "d", "#f4a3a2"),
        ("Month 18 if $9.5M covers everything", 2.5, "total", BLUE), ("Today’s $0.4M/month burn × 18, if not included", -7.2, "d", "#f4a3a2"),
        ("Month 18 if it does not", -4.7, "total", RED)]
slot = gw / len(bars); run_v = 0
for i, (lab, v, kind, col) in enumerate(bars):
    xx = gx0 + i * slot + slot / 2 - 12
    if kind == "total":
        top, bot = max(v, 0), min(v, 0)
        R(xx, gy3(top), 24, gy3(bot) - gy3(top), fill=col, r=4, corners="top" if v > 0 else "bottom"); run_v = v
        ly = gy3(top) - 22 if v > 0 else gy3(bot) + 6
        T(xx - 40, ly, 104, 18, ("$" if v > 0 else "−$") + f"{abs(v):.1f}M", size=12.5, f="B", align="center")
    else:
        s0, e0 = run_v, run_v + v
        R(xx, gy3(s0), 24, gy3(e0) - gy3(s0), fill=col, r=2)
        T(xx - 40, gy3(e0) + 6, 104, 18, f"−${abs(v):.1f}M", size=12.5, f="B", align="center"); run_v = e0
    T(gx0 + i * slot + 2, gy3(vmin) + 10, slot - 4, 60, lab, size=11, c=INK2, align="center", lh=1.1)
L(gx0, gy3(4.8), gx0 + gw, gy3(4.8), c=INK, sw=1.5, dash=[5, 4])
T(gx0 + gw - 250, gy3(4.8) - 20, 250, 16, "12-month floor at today’s burn: $4.8M", size=11, f="B", c=INK, align="right")
rx = 770
callout(rx, 128, XR - rx, 196, "Plan as stated still fails the runway test",
        ["$12.0M − $9.5M = $2.5M at month 18",
         "$2.5M ÷ $0.4M a month = about 6 months of runway, against the required 12",
         "The floor goes up as burn goes up. At the plan’s own average burn ($9.5M ÷ 18 = $0.53M a month), cash drops below 12 months of runway at around month 11"], fill=GRAYW, size=12)
callout(rx, 340, XR - rx, 156, "If unit economics land at the median",
        [f"Each store loses {mabs(MED['site'])} × 900 × 365 = ${-MED['annual']/1e6:.2f}M a year at full volume",
         f"Nine stores: about ${-MED['annual']*9/1e6:.0f}M a year, 1.5× all the cash Parcelbird has, before any acquisition spend"], fill=REDW, size=12)
callout(rx, 512, XR - rx, 102, "No fallback funding",
        "The lead investor says a new round for a delivery operator is ‘unlikely in this market’, so a shortfall cannot be refinanced.", size=12)
T(X0, 620, 700, 44, f"The briefing pack does not say whether the $9.5M includes the existing software burn, so both readings are shown. In the second, cash runs out around month {cash_out_B} (appendix A2).", size=11, c=MUTED, lh=1.18)
footer(SRC + ", §1, §3, §9; team analysis.", 10)

# ================================================================ 11. Software path
new()
header(f"The software business can break even on today’s cash: about {SW['be']} months at 60% growth, with cash bottoming out at ${SW['cmin']:.1f}M, above the runway floor throughout", sec=3)
T(X0, 128, 680, 18, "Software-only path with $0.8M a year of extra hires: cash vs. 12-month runway floor, $M", size=12.5, f="B")
gx0, gy_top, gh, gw = X0 + 40, 166, 400, 620
rows36 = SW['rows'][:37]
def lx(t): return gx0 + t / 36 * gw
def ly(v): return gy_top + (13 - v) / 13 * gh
for v in [0, 3, 6, 9, 12]:
    L(gx0, ly(v), gx0 + gw, ly(v), c=BASE if v == 0 else GRID)
    T(gx0 - 40, ly(v) - 8, 32, 16, f"{v}", size=10.5, c=MUTED, align="right")
for t in [0, 6, 12, 18, 24, 30, 36]:
    T(lx(t) - 30, ly(0) + 8, 60, 16, f"M{t}", size=10.5, c=MUTED, align="center")
T(gx0, ly(0) + 26, gw, 16, "Months from January 2027", size=10.5, c=MUTED, align="center")
cash_pts = [[lx(r[0]), ly(r[3])] for r in rows36]
floor_pts = [[lx(r[0]), ly(r[4] if r[4] is not None else 12 * 0.456)] for r in rows36]
floor_pts[0] = [lx(0), ly(12 * rows36[1][2])]
PL(floor_pts, c=MUTED, sw=2)
PL(cash_pts, c=BLUE, sw=2)
C(cash_pts[-1][0], cash_pts[-1][1], 4.5, BLUE)
T(cash_pts[-1][0] - 120, cash_pts[-1][1] - 26, 140, 16, f"Cash ${rows36[-1][3]:.1f}M", size=11.5, f="B", align="right")
lowt = min(rows36, key=lambda r: r[3])
C(lx(lowt[0]), ly(lowt[3]), 4.5, BLUE)
T(lx(lowt[0]) - 80, ly(lowt[3]) - 28, 160, 16, f"Low point ${lowt[3]:.1f}M (M{lowt[0]})", size=11.5, f="B", align="center")
L(lx(SW['be']), ly(0), lx(SW['be']), ly(12.5), c=INK2, sw=1)
T(lx(SW['be']) + 6, ly(12.5), 200, 30, f"Break-even ≈ month {SW['be']}\n(monthly burn reaches zero)", size=11, c=INK2, lh=1.1)
T(lx(3), ly(12 * 0.456) - 22, 300, 16, "Runway floor = 12 × monthly burn", size=11.5, f="B", c=INK2)
# legend
L(gx0, 600, gx0 + 18, 600, c=BLUE, sw=2); T(gx0 + 24, 592, 120, 16, "Cash", size=11, c=INK2)
L(gx0 + 90, 600, gx0 + 108, 600, c=MUTED, sw=2); T(gx0 + 114, 592, 220, 16, "Runway floor", size=11, c=INK2)
T(X0, 616, 700, 50, "Model: cost base implied by today = 81% × $4.1M + $4.8M = $8.1M a year, plus $0.8M of hires = $8.9M, held flat. Revenue = ARR, growing 60% a year, compounded monthly. Monthly burn = (costs − 81% × ARR) ÷ 12. Break-even ARR = $8.9M ÷ 81% = $11.0M.", size=10.5, c=MUTED, lh=1.18)
rx = 780
T(rx, 128, XR - rx, 18, "Stress test: when does the software path fail?", size=12.5, f="B")
rows = [["Case", "Break-even month", "Lowest cash", "Floor held?"]]
fl = {}
for i, (lab, s) in enumerate(stress):
    rows.append([lab, f"M{s['be']}", fm(s['cmin']), "Yes" if s['breach'] is None else f"No, M{s['breach']}"])
    if s['breach'] is not None: fl[(i + 1, 3)] = REDW
yb = table(rx, 152, [190, 80, 80, 94], rows, 34, size=11.5, aligns=["left", "right", "right", "right"], fills=fl, hh=32, fonts={(i, 0): "R" for i in range(1, 8)})
callout(rx, yb + 14, XR - rx, 612 - yb - 14 + 50, "So what",
        [f"The path is robust: the floor holds down to about {int(min_g*100)}% ARR growth, or with costs rising about 10% a year",
         "60% growth in 2027 means about $2.5M of new ARR, or roughly 26 contracts at $96k. The 9 late-stage deals cover $0.86M (35%) of that",
         "Hiring can be tied to bookings, so the risk can be managed"], size=11.5)
footer(SRC + ", §1, §10; team analysis. Simplified model, assumptions in appendix A2.", 11)

# ================================================================ 12. Software & q-commerce exposure
new()
header("The pipeline offers a capital-light way into quick commerce: grocers want fast delivery from their own stores, and Parcelbird can sell them the software", sec=3)
tiles = [("37 grocers", "in the software pipeline: 37 × $96k = $3.55M of annual contract value, 87% of today’s ARR"),
         ("$0.86M", "of ARR from the 9 late-stage deals (9 × $96k), +21% on today’s $4.1M"),
         ("≈10 contracts", "pay for the $0.8M of hires: $0.8M ÷ 81% gross margin = $0.99M ARR, or 10.3 contracts at $96k"),
         ("81% vs 27%", "software gross margin vs. the margin on groceries an operator would earn")]
tw = (XR - X0 - 3 * 16) / 4
for i, (big, small) in enumerate(tiles):
    xx = X0 + i * (tw + 16)
    R(xx, 130, tw, 132, fill=GRAYW, r=6)
    T(xx + 16, 142, tw - 32, 36, big, size=24, f="M")
    T(xx + 16, 184, tw - 32, 74, small, size=11.5, c=INK2, lh=1.2)
T(X0, 284, 800, 18, "Two ways to take part in quick commerce", size=13, f="B")
rows = [["", "Operator: Parcelbird Now", "Enabler: software, including fast delivery from grocers’ stores"],
        ["Capital at risk", "$5.4M capex plus $1.15M a year of fixed cost per store; $9.5M needed by month 18", "$0.8M a year of hires, which can be scaled back"],
        ["Who carries the volume risk", "Parcelbird: each store loses money below the required order volume", "The grocer, who uses existing stores with no dark-store rent"],
        ["Margin", "27% on goods, with negative contribution per order at median inputs", "81% gross margin on recurring contracts"],
        ["Fit with customers", "Competes for the same delivery customers as the grocers Parcelbird sells to (our inference: a risk to the pipeline)", "Gives the 37 pipeline grocers the fast-delivery offer several of them have asked for"],
        ["Evidence base", "Six-week pop-up, below median on every input", "$4.1M ARR growing 60% a year, plus a named pipeline"]]
table(X0, 308, [210, 470, 488], rows, 54, size=12, aligns=["left", "left", "left"], hh=30, fills={(i, 2): BLUEW for i in range(1, 6)})
footer(SRC + ", §1, §6, §9, §10; team analysis. A store-based fast-delivery offer still needs product validation with pipeline grocers.", 12)

# ================================================================ 13. Options
new()
header("Of the four options, only growing the software business meets both of the board’s conditions. Launching or piloting Parcelbird Now fails the runway test", sec=3)
rows = [["", "A. Launch as planned (9 stores, 3 cities)", "B. One-store pilot in Columbus (12 months)", "C. Grow the software business and sell fast delivery to grocers", "D. Status quo (no launch, no hires)"],
        ["Profit within current cash?", "Only if all four inputs beat the best observed", "No. One store is not profitable at observed inputs", f"Yes: break-even ≈ month {SW['be']} at 60% growth", "Likely, but more slowly: growth would drop without the hires (not quantified)"],
        ["12 months of runway at all times?", "No: ≤ $2.5M left at month 18", f"No: ≈${PILOT:.1f}M cost breaches the floor by month {PIL['breach']}", f"Yes: low point ${SW['cmin']:.1f}M; holds down to ≈{int(min_g*100)}% growth", "Yes, if growth holds"],
        ["Upside", f"+${PLAN['annual']*9/1e6:.0f}M a year site contribution on plan inputs", "What we learn: mostly already visible from the 14 software sites", "$3.6M pipeline at 81% gross margin; fast delivery adds to the product", "Keeps cash; leaves pipeline capacity unused"],
        ["Downside", f"−${-MED['annual']*9/1e6:.0f}M a year at median inputs; cash runs out", f"−${PILOT:.1f}M; pulls focus from the software", f"Growth below {int(min_g*100)}% breaches the floor; hiring can slow to match", "Competitors serve the grocers who want fast delivery"],
        ["Reversibility", "Low: $5.4M capex, leases, riders", "Medium", "High: hiring can be paused", "High"]]
verd = [None, ("no", "Fails"), ("no", "Fails"), ("ok", "Recommended"), ("mid", "Viable, weaker")]
fills = {(r, 3): BLUEW for r in range(1, 6)}
yb = table(X0, 128, [176, 248, 248, 248, 248], rows, [74, 70, 74, 74, 48], size=12, aligns=["left"] * 5, hh=48, fills=fills, hsize=11.5)
for j in range(1, 5):
    status(X0 + 176 + (j - 1) * 248 + 8, yb + 14, verd[j][0], verd[j][1], size=12.5)
T(X0, yb + 46, XR - X0, 50, f"The pilot cost is built up in appendix A2: $0.6M capex + $1.15M site cost + {PILOT_OPD} orders a day × 365 × {m(-MED['var'])} variable loss (${pilot_var_loss:.2f}M) + acquisition to support {PILOT_OPD} orders a day (${pilot_cac:.2f}M) ≈ ${PILOT:.1f}M. The capex and site cost alone ($1.75M) are more than the ≈$1.5M a 12-month pilot could spend without breaching the floor.", size=11, c=MUTED, lh=1.18)
footer(SRC + "; team analysis. Options are framed by how much Parcelbird operates itself: fully, as a test, through customers, or not at all.", 13)

# ================================================================ 14. Recommendation & next steps
new()
header("We recommend the board turn down Parcelbird Now for 2027, fund the software plan, and agree the triggers for reopening the question", sec=4)
T(X0, 128, 560, 18, "Decisions requested in January 2027", size=13, f="B")
decs = [("1", "Turn down the Parcelbird Now launch and the one-store pilot for 2027", "Both fail the 12-month runway floor (pages 10 and 13)"),
        ("2", "Approve $0.8M a year for 2 engineers and 2 sales hires", "Pays for itself at about 10 contracts. Release in two tranches tied to bookings"),
        ("3", "Fund a store-based fast-delivery offer for pipeline grocers", "Validate it with the 9 late-stage grocers before building"),
        ("4", "Adopt the reopening triggers and a quarterly runway check", "Triggers on page 16. Cash floor = 12 × the latest monthly burn")]
yy = 156
for n, d, why in decs:
    R(X0, yy, 560, 92, fill=BLUEW if n == "1" else GRAYW, r=6)
    T(X0 + 16, yy + 12, 30, 30, n, size=22, f="B", c=BLUE)
    T(X0 + 50, yy + 12, 494, 40, d, size=13.5, f="B", lh=1.15)
    T(X0 + 50, yy + 54, 494, 34, why, size=11.5, c=INK2, lh=1.15)
    yy += 102
rx = 650
T(rx, 128, XR - rx, 18, "First 90 days", size=13, f="B")
rows = [["When", "Action", "Measure of success"],
        ["By end of Jan", "Board decision; communicate the reasons to the team and investors", "Decision minuted"],
        ["Feb", "Hire tranche 1 (1 engineer, 1 sales). Prioritise closing the 9 late-stage deals", "Signed ACV vs. $0.86M"],
        ["Feb–Mar", "Discovery with pipeline grocers on fast delivery from their stores: scope, pricing, pilot customer", "≥ 3 grocers commit to a paid pilot"],
        ["Mar", "Set up a quarterly dashboard: ARR growth, burn, runway, and trigger metrics from the benchmark sites", "Dashboard in the board pack"],
        ["Apr", "Release hire tranche 2 if trailing bookings are on track for ≥ 40% ARR growth", "Tranche-2 decision"]]
table(rx, 152, [100, 300, 174], rows, 72, size=11.5, aligns=["left", "left", "left"], hh=30)
footer(SRC + "; team analysis. Timing and tranche thresholds are our proposals, not from the pack.", 14)

# ================================================================ 15. Risks
new()
header("The recommendation holds under the main risks. The one that matters most is slower software growth, which hiring discipline can manage", sec=4)
rows = [["Assumption / risk", "What we assumed and why it matters", "Effect if wrong", "Response"],
        ["Software growth slows", f"60% ARR growth continues. The floor breaks below ≈{int(min_g*100)}% (flat costs)", f"At 30%: break-even ≈ M46, floor breached at M23", "Tranche hires against bookings; review each quarter"],
        ["Software costs rise", "Cost base flat apart from the $0.8M of hires", "Costs +15% a year: floor breached at M19", "Hold the cost base until break-even"],
        ["Founders are right about density", "The Midwest can reach plan volumes; nobody has shown it yet", f"Up to +${PLAN['annual']*9/1e6:.0f}M a year site contribution forgone", "Triggers keep the option open at no cost"],
        ["Rider minimum pay", "$17.75 an hour today; 2 of the 3 cities are considering minimum pay rules", f"Each +$1/hr = −$0.42 per order at the median. +$7.06/hr wipes out the plan’s margin", "Strengthens the ‘no’"],
        ["Losing the Midwest to a rival", "Being first does not protect profits (QuickBasket is retreating)", "A rival takes the Midwest market", "Sell software to that rival or to grocers instead"],
        ["Evidence limits", "Synthetic data; 6-week pop-up; 14 sites; survey covers ages 25–39 only", "Medians could move", "Re-run the model each quarter"],
        ["Model reading of the $9.5M", "Generous reading: it includes the existing burn", "If it does not, cash runs out ≈ M15", "Both readings fail, so the conclusion holds"]]
table(X0, 128, [210, 380, 310, 268], rows, 62, size=11.5, aligns=["left"] * 4, hh=30)
footer(SRC + "; team analysis. Rider-cost sensitivity: $1 ÷ 2.4 orders/hr = $0.42 per order; plan margin $2.02 × 3.5 orders/hr = $7.06/hr.", 15)

# ================================================================ 16. Triggers
new()
header("Parcelbird Now should come back to the board only if the data show what the plan assumes. Parcelbird already sees most of that data through its software", sec=4)
T(X0, 128, XR - X0, 20, "Triggers for reopening the operator decision. All must be met; each maps to one of the four tests", size=13, f="B")
rows = [["Test", "Trigger", "Why this threshold", "Where the data comes from"],
        ["1  Market", "An operator reports positive EBITDA in a mid-size US city", "Shows a profit pool exists, not just growth", "Public operator reporting"],
        ["2  Unit economics", "At least one benchmark site has positive contribution after site costs for 2 consecutive quarters", f"Today even the best values combined lose {mabs(BEST['site'])} per order", "Parcelbird’s own software data (14+ sites)"],
        ["2  Customers", "Customer payback under 12 months on observed cohorts", f"Plan inputs give ≈{38/PLAN['var']/orders_per_acq_month:.0f} months today; needs ≈{38/(12*3.1*PLAN['var'])*100:.0f}% month-3 retention at plan contribution", "Customer data from sites on the software"],
        ["3  Funding", "Software at break-even, or ring-fenced outside capital so the floor holds", "The floor must hold at all times", "Monthly management accounts"],
        ["—  Regulation", "Rider pay rules settled in the target cities", "Each +$1/hr costs $0.42 per order at median productivity", "City council decisions"]]
yb = table(X0, 156, [170, 380, 380, 238], rows, 62, size=12, aligns=["left"] * 4, hh=30)
R(X0, yb + 16, XR - X0, 64, fill=BLUEW, r=6)
T(X0 + 16, yb + 16, XR - X0 - 32, 64, runs=[run("Why this keeps the option open: ", "B"), run("Parcelbird sees its customers’ dark-store results through its software. It can wait for evidence without spending its own capital, and act early if a site proves the economics.")], size=13, va="middle")
footer(SRC + "; team analysis. Retention needed = $38 ÷ (12 months × 3.1 orders × $3.77) ≈ 27%.", 16)

# ================================================================ A1 Unit economics detail
new()
header("Appendix A1: Unit economics by line item. Each order loses money before rent unless AOV, rider productivity and promotions all beat the median", label="Appendix A1")
lines = [("Average order value (AOV)", lambda s: f"${s['aov']:.0f}"),
         ("Gross margin on goods (AOV × 27%)", lambda s: sn(s['goods'])),
         ("+ Delivery fee, net of payment cost", lambda s: sn(s['fee'])),
         ("− Picking and packing labor", lambda s: f"−{s['pick']:.2f}"),
         ("− Rider cost ($17.75 ÷ orders per rider-hour)", lambda s: f"−{s['rider']:.2f}"),
         ("− Payment processing and packaging", lambda s: f"−{s['pay']:.2f}"),
         ("− Promotions (% × AOV)", lambda s: f"−{s['promo_c']:.2f}"),
         ("= Contribution before site costs", lambda s: sn(s['var'])),
         ("− Site fixed cost ÷ (orders per day × 365)", lambda s: f"−{s['fpo']:.2f}"),
         ("= Contribution after site costs, per order", lambda s: sn(s['site'])),
         ("Annual result per site at that volume, $M", lambda s: sn(s['annual']/1e6))]
rows = [["$ per order", "Pop-up", "Median", "Best observed (each)", "Founders’ plan"]]
for lab, fn in lines:
    rows.append([lab] + [fn(s).replace("−-", "") for s in (POP, MED, BEST, PLAN)])
fonts = {(i, 0): "R" for i in range(1, 12)}
for i in (8, 10):
    for j in range(5): fonts[(i, j)] = "B"
fonts.update({(i, j): fonts.get((i, j), "R") for i in range(1, 12) for j in range(1, 5)})
table(X0, 126, [420, 170, 170, 200, 208], rows, 37, size=12, aligns=["left", "right", "right", "right", "right"], hh=30, fonts=fonts,
      fills={(8, j): GRAYW for j in range(5)} | {(10, j): GRAYW for j in range(5)})
T(X0, 600, XR - X0, 60, "Inputs: pop-up AOV $31, promos 12%, 2.1 orders/rider-hr, 280 orders/day, $650k site cost. Median: $34, 6%, 2.4, 900, $1.15M. Best observed: $42, 6%, 3.0, 1,400, $1.15M (from different sites). Plan: $45, 2%, 3.5, 1,800, $1.15M. "
  f"Break-even orders per day = $1.15M ÷ 365 ÷ contribution before site costs: plan {1.15e6/365/PLAN['var']:,.0f}; best observed {1.15e6/365/BEST['var']:,.0f}; median never (negative before site costs).", size=11, c=INK2, lh=1.2)
footer(SRC + ", Table 3 (§6), §7.", 17)

# ================================================================ A2 Funding calcs
new()
header("Appendix A2: Funding calculations. Both readings of the plan and a one-store pilot breach the 12-month floor; the software path does not", label="Appendix A2")
rows = [["Scenario (monthly model, from January 2027)", "Spend / burn assumption", "Cash low point", "Floor first breached", "Cash runs out"],
        ["Software path (recommended)", "Cost base $8.9M a year flat; ARR +60% a year; 81% gross margin", f"${SW['cmin']:.1f}M (M{min(SW['rows'], key=lambda r: r[3])[0]})", "Never", "Never"],
        ["Software + one-store pilot", f"As above + ${PILOT:.1f}M spread evenly over months 1–12", fm(PIL['cmin']), f"M{PIL['breach']}", "Never"],
        ["Parcelbird Now, reading A", "$9.5M covers everything to M18 (generous)", "$2.5M at M18", "≈M11 at the $0.53M average burn", "After M18 unless profitable"],
        ["Parcelbird Now, reading B", "$9.5M evenly over 18 months + existing software burn (no new hires)", fm(NOWB['cmin']), f"M{NOWB['breach']}", f"≈M{cash_out_B}"]]
yb = table(X0, 126, [270, 380, 160, 190, 168], rows, 50, size=11.5, aligns=["left", "left", "right", "right", "right"], hh=30)
T(X0, yb + 18, 560, 18, "Pilot cost build-up (12 months, one Columbus dark store)", size=12.5, f="B")
rows = [["Item", "Calculation", "$M"],
        ["Capex", "Per the founders’ plan", "0.60"],
        ["Site fixed cost", "$1.15M a year", "1.15"],
        ["Variable loss", f"{PILOT_OPD} orders a day (between the 410 exit rate and the 900 median) × 365 × $2.67", f"{pilot_var_loss:.2f}"],
        ["Customer acquisition", f"{PILOT_OPD} × 365 ÷ 12 ÷ 3.1 = {pilot_active:,.0f} active ÷ 22% × $38", f"{pilot_cac:.2f}"],
        ["Total", "", f"{PILOT:.2f}"]]
table(X0, yb + 42, [150, 340, 70], rows, [34, 34, 42, 34, 34], size=11.5, aligns=["left", "left", "right"], hh=26)
rx = X0 + 600
T(rx, yb + 18, XR - rx, 18, "Software model assumptions", size=12.5, f="B")
bullets(rx, yb + 44, XR - rx, 230, [
    "Implied cost base: gross profit 81% × $4.1M = $3.32M; plus $4.8M a year burn = $8.12M a year of operating costs (assumes revenue ≈ ARR)",
    "Add $0.8M a year of hires, giving $8.92M. Held flat in the base case; +10% and +15% a year tested on page 11",
    "ARR compounds monthly at (1 + g)^(1/12). Monthly burn = (costs − 0.81 × ARR) ÷ 12",
    "Runway floor = 12 × that month’s burn. The breach month is the first month cash falls below it",
    "Excludes working capital, one-off costs and any revenue from a fast-delivery offer"], size=11.5, ps=4)
footer(SRC + ", §1, §3, §9, §10; team analysis.", 18)

# ================================================================ A3 Notes / choices
new()
header("Appendix A3: Where the pack was silent, we took the reading most favourable to the launch and stress-tested our own alternative. No choice changes the answer", label="Appendix A3")
rows = [["Question", "Choice made", "Why, and effect on the answer"],
        ["What does ‘contribution per order’ include?", "Shown both before and after site fixed costs", "Founders’ month-18 claim and Zipcart’s figure appear to be before site costs; the median is negative either way"],
        ["Does the $9.5M include today’s $0.4M/month burn?", "Showed both readings; led with the generous one", "Both fail the runway floor, so the answer does not change"],
        ["How is the 12-month runway floor measured?", "12 × the current month’s net burn; $4.8M at today’s burn", "A higher burn raises the floor, so this is the lenient version"],
        ["Software growth after 2026", "60% continues (stated rate), with cost base flat apart from $0.8M of hires", "Stress-tested: the floor holds down to ≈34% growth"],
        ["Pilot size and cost", f"One store, 12 months, {PILOT_OPD} orders a day, ≈${PILOT:.1f}M", "Even capex + site cost alone ($1.75M) exceed the ≈$1.5M a pilot could spend without breaching the floor"],
        ["Zipcart’s $3.99 fee", "Treated as net of payment cost; no change to AOV or rider productivity", "Generous to the launch case; the result is still −$1.05 per order"],
        ["Channel conflict with grocers", "Flagged as our inference, not a stated fact", "Not needed for the conclusion"],
        ["Format", "Static PDF deck; values printed on charts instead of hover tooltips", "Charts use a validated blue/red palette; red = loss, blue = profit"]]
table(X0, 126, [300, 420, 448], rows, 56, size=11.5, aligns=["left"] * 3, hh=30)
footer(SRC + "; team analysis.", 19)

json.dump(dict(w=W, h=H, pages=pages), open(sys.argv[1], "w"))
print("pages", len(pages), "| pilot", round(PILOT, 2), PIL['breach'], "| sw", SW['be'], round(SW['cmin'], 2), "| min_g", min_g, "| nowB out", cash_out_B, NOWB['breach'])
