import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from decklib import *

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R_ = json.load(open(os.path.join(ROOT, "work/results.json")))

NAVY, INK, MUTED, GRID, LIGHT, TINT = "14213D", "262626", "666666", "D0D0D0", "F3F4F6", "EAF2FC"
A, B, J = "2A78D6", "EB6834", "1BAF7A"
GOOD, BAD, WARN = "0A8A0A", "D03B3B", "B77900"   # good/critical from status palette (good darkened slightly for text contrast)
REF = "8C8C8C"
SRC = "Source: Onsoo US-entry briefing pack (synthetic data); team analysis."

slides = []
def new(name, section, title, source=SRC):
    s = Slide(name); slides.append(s)
    n = len(slides)
    if section:
        s.add(T(0.5, 0.16, 9, 0.28, section.upper(), size=9, bold=True, color=A))
    s.add(T(0.5, 0.42, 12.3, 0.88, title, size=20, bold=True, color=NAVY, valign="t"))
    s.add(L(0.55, 1.33, 12.83, 1.33, NAVY, 1.0))
    s.add(L(0.55, 6.93, 12.83, 6.93, GRID, 0.5))
    s.add(T(0.5, 6.96, 11.0, 0.42, source, size=8, color=MUTED))
    s.add(T(12.2, 6.96, 0.65, 0.3, str(n), size=9, color=MUTED, align="r"))
    return s

def table(s, x, y, widths, rows, rh=0.34, size=10.5, header_fill=NAVY, header_color="FFFFFF", zebra=False,
          aligns=None, fills=None, bold_first_col=False, heights=None, valign="m"):
    """rows[0] = header. fills: dict (r,c)->hex. heights: per-row heights."""
    cy = y
    for ri, row in enumerate(rows):
        h = heights[ri] if heights else rh
        cx = x
        for ci, cell in enumerate(row):
            w = widths[ci]
            al = (aligns[ci] if aligns else "l")
            if ri == 0:
                s.add(T(cx, cy, w, h, cell, size=size - 0.5, bold=True, color=header_color, fill=header_fill, align=al, valign="m"))
            else:
                f = (fills or {}).get((ri, ci))
                if f is None and zebra and ri % 2 == 0: f = LIGHT
                s.add(T(cx, cy, w, h, cell, size=size, color=INK, fill=f, align=al, valign=valign,
                        bold=(bold_first_col and ci == 0)))
            cx += w
        if ri > 0:
            s.add(L(x, cy + h, x + sum(widths), cy + h, GRID, 0.5))
        cy += h
    return cy

def money(v, d=1, plus=False):
    sgn = "−" if v < -1e-9 else ("+" if plus and v > 1e-9 else "")
    return f"{sgn}${abs(v):.{d}f}M"

def nf(v, d=2):
    if abs(v) < 0.005: return "—"
    return f"{v:.{d}f}".replace("-", "−")

def pct(v, d=1): return f"{v*100:.{d}f}%"

# =====================================================================
# 1 Title
s = Slide("title"); slides.append(s)
s.add(R(0, 0, W, H, NAVY))
s.add(R(0.6, 2.05, 0.08, 2.1, A))
s.add(T(0.85, 1.9, 11.5, 0.9, "Onsoo Botanicals: US market entry", size=34, bold=True, color="FFFFFF"))
s.add(T(0.85, 2.8, 11.5, 0.6, "Should Onsoo enter the US market in 2027, and if so, by which route?", size=20, color="DCE6F5"))
s.add(T(0.85, 3.55, 11.5, 0.6, "Recommendation for CEO Park Ji-won and the Board · March 2027 board meeting", size=14, color="DCE6F5"))
s.add(T(0.85, 6.3, 11.8, 0.7, ["Draft for discussion · prepared November 2026",
        "All figures come from the US-entry briefing pack (synthetic benchmark data). $ = US dollars; KRW 1,380 per $. M = million, B = billion."],
        size=10, color="B8C4D6"))

# =====================================================================
# 2 Executive summary
s = new("exec", "Executive summary",
        "Enter the US in 2027 through Amazon, but fund it in stages: it is the only route within the board’s limits, and its payback depends on holding ad costs near pilot levels")
blocks = [
 ("1", "Whether", "Yes: the US deserves 2027’s single launch slot", [
   "US K-beauty skincare grew **17% a year** to $3.6B (2021–25), against 5% for all facial skincare; **41%** of it sells on Amazon.",
   "The Amazon pilot sold 64,800 units in six months; monthly volume rose **89%**, at 4.5 stars and 29% repeat (benchmark 31%).",
   "A Japan scale-up is safer (+$1.8M cash by 2030) but adds only **$7M** of revenue in a market growing 1.5% a year."]),
 ("2", "Route", "Amazon-led (A) is the only route that fits the board’s limits", [
   "On planning inputs A needs at most **$1.9M** of cash, pays back in 2030 (+$2.4M) and keeps group margin at or above 9.5%.",
   "Retail-led (B) breaches **all three** limits on its own inputs: −$20.8M peak cash (cap $18M), no payback, 4.5% group margin in 2027. Its inputs are also optimistic: 4.5 units/door/week vs 2.6 at Onsoo’s awareness.",
   "No route reaches $40M by 2030 within the limits; A reaches **$26M**, and about $40M by 2032 if it keeps growing ~29% a year."]),
 ("3", "How", "Payback hinges on ad cost, so commit in gated stages", [
   "A pays back by 2030 only if ACoS averages **≤28.6%**; the pilot ran at 28%, but brands scaling to $5–20M run at a **32%** median (→ −$2.3M in 2030).",
   "The downside is bounded: across ten cases, peak cash stays **≤$7.2M** (40% of the cap) and group margin ≥8.8%.",
   "Gate spend on H2-2027 ad cost; treat specialty retail as an option to earn (≥20% awareness, door test ≥4.0 units/week), not a 2029 date."]),
]
y = 1.5
for num, tag, head, buls in blocks:
    hgt = 1.6
    s.add(R(0.55, y, 0.42, hgt - 0.12, A))
    s.add(T(0.55, y, 0.42, hgt - 0.12, num, size=18, bold=True, color="FFFFFF", align="c", valign="m"))
    s.add(T(1.05, y - 0.02, 2.75, hgt - 0.1, [Para(tag.upper(), size=9, bold=True, color=A), Para(head, size=13, bold=True, color=NAVY, space_before=2)]))
    s.add(T(3.85, y - 0.02, 9.0, hgt - 0.1, [Para(b, bullet=True) for b in buls], size=11, space=3))
    if num != "3":
        s.add(L(1.05, y + hgt - 0.06, 12.83, y + hgt - 0.06, GRID, 0.5))
    y += hgt
s.add(T(0.55, 6.38, 12.3, 0.5, "**Board decisions for March 2027:** approve Stage 1 of Option A (2027 cash need $1.9–2.9M) · adopt ad-cost gates · pre-agree whether a 1–2-year payback slip is acceptable · restate the $40M ambition · raise the retail trigger",
        size=10.5, color=NAVY, fill=TINT, valign="m"))

# =====================================================================
# 3 Hypothesis test
s = new("hypothesis", "Approach",
        "We tested the CEO’s Amazon-first hypothesis against four conditions: two hold, one holds only if ad costs stay low, and the retail trigger does not hold")
s.add(T(0.55, 1.47, 12.3, 0.5, "**Starting hypothesis (CEO):** “Launch in the US in 2027 through Amazon, then add specialty beauty retail from 2029 once Amazon sales pass $10M and aided awareness passes 15%.”",
        size=11, color=NAVY, fill=TINT, valign="m"))
rows = [["What would have to be true", "What the evidence shows", "Verdict", "Slides"],
 ["1  The US is a better use of the single 2027 launch slot than a Japan scale-up",
  "US K-beauty skincare +17% a year vs Japan +1.5%; pilot demand is real. Japan yields more 4-year cash (+$1.8M) but only $7M revenue and no US progress", "✓ Holds", "4–6"],
 ["2  Amazon-led beats retail-led on the board’s limits",
  "B breaches cap, payback and margin floor even on its own inputs; its sell-through and halo inputs are optimistic", "✓ Holds", "7–10"],
 ["3  Amazon-led meets the cap, payback and margin limits under realistic inputs",
  "Cap and margin floor hold in all ten cases tested; payback by 2030 holds only if ACoS ≤28.6% (scale benchmark: 32%)", "◐ Only if ad cost stays ≤28.6%", "11–13"],
 ["4  Retail can be added profitably in 2029 at $10M Amazon sales and 15% awareness",
  "At 10–20% awareness newcomers sell a median 3.5 units/door/week, below the 4.0 delisting line; retail fixed costs need ~4,250 doors to cover", "✗ Does not hold: raise to 20% and test first", "14"]]
fills = {(1, 2): None}
yb = table(s, 0.55, 2.12, [4.1, 5.5, 1.95, 0.75], rows, size=10.5, aligns=["l", "l", "l", "c"], heights=[0.36, 0.72, 0.72, 0.72, 0.72])
# colour verdict text
for e in s.els:
    if isinstance(e, T) and e.paras[0].text.startswith(("✓", "◐", "✗")):
        e.color = GOOD if e.paras[0].text.startswith("✓") else (WARN if e.paras[0].text.startswith("◐") else BAD); e.bold = True
s.add(T(0.55, yb + 0.18, 12.3, 0.62, "**Revised answer:** enter the US in 2027 through Amazon (Option A), released in gated stages tied to ad cost at scale; keep specialty retail as an option earned at ≥20% awareness and a successful door test, not a dated 2029 commitment.",
        size=11.5, color="FFFFFF", fill=NAVY, valign="m"))
s.add(T(0.55, yb + 0.92, 12.3, 0.55, "Board limits used throughout: peak cumulative US cash outflow ≤$18M through 2030 · cumulative US cash back to zero by end-2030 · group operating margin ≥8% every year · one major launch in 2027 · ambition “on the way to $40M by 2030”.",
        size=9.5, color=MUTED))

# =====================================================================
# 4 Market
s = new("market", "1 · Whether: the US deserves the 2027 slot",
        "US K-beauty skincare has grown 17% a year to $3.6B, over three times the category’s pace, and Amazon is where most of it is bought",
        "Source: briefing pack Tables 1–2 and September 2026 survey (n = 1,200 US women 18–44); team analysis.")
# left chart: K-beauty sales columns
s.add(T(0.55, 1.5, 6.2, 0.5, [Para("US K-beauty facial skincare sales, $B", size=12, bold=True, color=NAVY),
                              Para("Share of all US facial skincare shown below each year", size=9.5, color=MUTED, space_before=1)]))
years = ["2021", "2022", "2023", "2024", "2025"]; kb = [1.9, 2.3, 2.7, 3.1, 3.6]; tot = [20.1, 21.3, 22.6, 23.5, 24.5]
cx0, base, cw, ch = 0.8, 5.25, 5.6, 2.9
slot = cw / 5
for i, v in enumerate(kb):
    bh = v / 4.0 * ch; bx = cx0 + i * slot + slot * 0.2
    s.add(R(bx, base - bh, slot * 0.6, bh, A))
    s.add(T(bx - 0.2, base - bh - 0.32, slot * 0.6 + 0.4, 0.3, f"{v:.1f}", size=11, bold=True, color=INK, align="c"))
    s.add(T(bx - 0.2, base + 0.04, slot * 0.6 + 0.4, 0.28, years[i], size=10, color=INK, align="c"))
    s.add(T(bx - 0.2, base + 0.3, slot * 0.6 + 0.4, 0.28, f"{kb[i]/tot[i]*100:.1f}%", size=9.5, color=MUTED, align="c"))
s.add(L(cx0, base, cx0 + cw, base, "7F7F7F", 0.75))
s.add(T(0.55, 5.95, 6.2, 0.9, ["**CAGR 2021–25:** K-beauty (3.6 ÷ 1.9)^¼ − 1 = **17.3%**; all facial skincare (24.5 ÷ 20.1)^¼ − 1 = **5.1%**",
        "The trade-press “$5.2B US K-beauty” figure also includes makeup and hair care, so we use the $3.6B skincare figure."], size=9.5, color=INK, space=2))
# right chart: channels
s.add(T(7.1, 1.5, 5.8, 0.5, [Para("Where US consumers bought K-beauty skincare, 2025", size=12, bold=True, color=NAVY),
                             Para("Share of sales, %", size=9.5, color=MUTED, space_before=1)]))
chans = [("Amazon", 41), ("Specialty beauty retail", 27), ("Mass retail", 14), ("Brand websites (DTC)", 12), ("Other", 6)]
by = 2.2
for nm, v in chans:
    s.add(T(7.1, by, 2.1, 0.36, nm, size=10.5, color=INK, align="r", valign="m"))
    bw = v / 45 * 3.0
    s.add(R(9.3, by + 0.06, bw, 0.24, A if nm == "Amazon" else "A6A6A6"))
    s.add(T(9.3 + bw + 0.04, by, 0.6, 0.36, f"{v}%", size=10.5, bold=nm == "Amazon", color=INK, valign="m"))
    by += 0.44
s.add(R(7.15, 4.55, 5.7, 1.95, LIGHT))
s.add(T(7.25, 4.6, 5.5, 1.85, [Para("Survey: K-beauty buyers shop on Amazon and discover on TikTok", bold=True, color=NAVY, size=11),
     Para("**61%** buy K-beauty most often on Amazon; 22% at specialty beauty retail", bullet=True),
     Para("**38%** discovered their last new brand on TikTok; 17% in a store", bullet=True),
     Para("**52%** of K-beauty triers cite price vs US brands as a reason to buy", bullet=True),
     Para("Onsoo is barely known: **4%** aided awareness overall, 9% among K-beauty buyers", bullet=True)], size=10.5, space=4))

# =====================================================================
# 5 Pilot
s = new("pilot", "1 · Whether: the US deserves the 2027 slot",
        "The Amazon pilot shows real US demand: monthly sales nearly doubled in six months, at 4.5 stars and near-benchmark repeat",
        "Source: briefing pack section 6 (Amazon pilot, Jan–Jun 2026, three SKUs, cross-border seller) and Table 5; team analysis.")
s.add(T(0.55, 1.5, 6.3, 0.5, [Para("Pilot units sold per month, 2026 (three SKUs)", size=12, bold=True, color=NAVY),
                              Para("Thousand units", size=9.5, color=MUTED, space_before=1)]))
mon = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]; u = [7.4, 8.6, 10.1, 11.8, 12.9, 14.0]
cx0, base, cw, ch = 0.8, 5.0, 5.8, 2.6; slot = cw / 6
for i, v in enumerate(u):
    bh = v / 15 * ch; bx = cx0 + i * slot + slot * 0.2
    s.add(R(bx, base - bh, slot * 0.6, bh, A))
    s.add(T(bx - 0.2, base - bh - 0.3, slot * 0.6 + 0.4, 0.28, f"{v:.1f}", size=10.5, bold=True, color=INK, align="c"))
    s.add(T(bx - 0.2, base + 0.04, slot * 0.6 + 0.4, 0.28, mon[i], size=10, color=INK, align="c"))
s.add(L(cx0, base, cx0 + cw, base, "7F7F7F", 0.75))
s.add(T(0.55, 5.45, 6.3, 1.4, [Para("**Is the 2027 plan of 300,000 units plausible?**", color=NAVY),
     Para("June run-rate: 14,000 × 12 = 168,000 units a year from 3 SKUs, i.e. ~4,700 units per SKU per month.", bullet=True),
     Para("With the four planned new SKUs (7 in total) at June’s per-SKU rate: 7 × 4,700 × 12 ≈ 390,000 units, so 300,000 is within reach, though it assumes new SKUs sell like the first three.", bullet=True)],
     size=10, space=3))
tiles = [("64,800 units", "$1.56M of sales in six months at $24.00 average price"),
         ("+89%", "Jan → Jun monthly units (7,400 → 14,000), ≈ 14% a month compounded"),
         ("4.5 ★", "from 2,140 reviews. Top complaint (6%): Korean-only labels, which US labelling in the 2027 setup budget fixes"),
         ("29% repeat", "90-day repeat of first-time buyers vs 31% for first-year skincare brands on Amazon US (Onsoo Korea: 48%)"),
         ("28% ACoS", "on a small ad budget: the number that must hold at scale (see slide 11)")]
ty = 1.55
for big, small in tiles:
    s.add(R(7.2, ty, 5.65, 0.98, LIGHT))
    s.add(R(7.2, ty, 0.07, 0.98, A))
    s.add(T(7.38, ty + 0.05, 1.75, 0.88, big, size=16, bold=True, color=NAVY, valign="m"))
    s.add(T(9.15, ty + 0.05, 3.65, 0.88, small, size=10, color=INK, valign="m"))
    ty += 1.06

# =====================================================================
# 6 Japan vs US
J_ = R_["J"]; A0 = R_["A"]; A32 = R_["A32"]
s = new("japan", "1 · Whether: the US deserves the 2027 slot",
        "A Japan scale-up is the safer use of 2027, but it adds only $7M of revenue by 2030 and does nothing for the US ambition")
rows = [["2027–2030, $M unless stated", "J · Japan scale-up", "A · US Amazon-led at planning ACoS 25%", "A · US Amazon-led at benchmark ACoS 32%"],
        ["Market growth", "Japan facial skincare ~1.5% a year; Onsoo already holds 3.1%", "US K-beauty skincare 17% a year (2021–25)", "US K-beauty skincare 17% a year (2021–25)"],
        ["Revenue added in 2030", "$7.0M", "$26.4M", "$26.4M"],
        ["Operating profit in 2030", money(J_["rows"][3]["op"]), money(A0["rows"][3]["op"]), money(A32["rows"][3]["op"])],
        ["Cumulative cash, end-2030", money(J_["cum2030"], plus=True), money(A0["cum2030"], plus=True), money(A32["cum2030"], plus=True)],
        ["Peak cash need", money(-J_["peak"]), money(-A0["peak"]), money(-A32["peak"])],
        ["Lowest group operating margin", pct(J_["min_gm"]), pct(A0["min_gm"]), pct(A32["min_gm"])],
        ["Progress toward US $40M", "None", "$26.4M in 2030, still growing ~29% a year", "$26.4M in 2030, still growing ~29% a year"]]
fl = {(4, 3): "FBE3E3", (4, 1): "E3F3E3", (4, 2): "E3F3E3"}
yb = table(s, 0.55, 1.55, [2.7, 3.2, 3.2, 3.2], rows, size=10.5, aligns=["l", "c", "c", "c"], bold_first_col=True,
           heights=[0.55, 0.62, 0.38, 0.38, 0.38, 0.38, 0.38, 0.55], fills=fl)
s.add(T(0.55, yb + 0.12, 7.6, 1.3, [Para("**Calculation (Japan, Table 7):** contribution 30% × (2.5 + 4.5 + 6.0 + 7.0) = $6.0M, less fixed cost 4 × $0.8M and one-time $1.0M = **+$1.8M**. US figures: slide 8 and appendix.", size=9.5),
     Para("Japan yields more four-year cash than the US unless US ACoS stays below ~26% (25% + (2.40 − 1.80) ÷ 0.67). The US case rests on what it builds: 2030 revenue ~4× Japan’s, still growing ~29% a year, toward the ambition.", size=9.5)], size=9.5, space=4))
s.add(R(8.4, yb + 0.12, 4.45, 1.45, NAVY))
s.add(T(8.5, yb + 0.15, 4.25, 1.4, [Para("So what", bold=True, color="FFFFFF", size=11),
     Para("Use 2027 for the US. Waiting a year would not resolve the key unknown, ad cost at scale, which can only be learned by scaling in the US; it would just delay the learning.", color="FFFFFF", size=10.5, space_before=3)], valign="m"))

# =====================================================================
# 7 Unit economics
s = new("unit", "2 · Route: Amazon-led is the only route within the limits",
        "Per unit, retail earns more than Amazon ($7.55 vs $4.73), but its $7.5M a year of extra fixed cost would need ~4,250 doors to cover")
s.add(T(0.55, 1.48, 6.6, 0.3, "Rice Ferment Barrier Cream (50 ml), $ per unit, planning inputs", size=12, bold=True, color=NAVY))
rows = [["", "Amazon", "Specialty retail"],
        ["Price Onsoo receives", "24.00", "14.00 (50% of $28 shelf)"],
        ["Amazon referral fee (15%)", "−3.60", "—"],
        ["Amazon fulfilment (FBA)", "−5.10", "—"],
        ["Advertising (ACoS 25% × price)", "−6.00", "in fixed budget"],
        ["Retailer co-op (8%) + returns (4%)", "—", "−1.68"],
        ["Ex-factory product cost", "−3.50", "−3.50"],
        ["Freight to US", "−0.55", "−0.75"],
        ["US import duty (15% of ex-factory)", "−0.53", "−0.53"],
        ["**Contribution per unit**", "**4.73**", "**7.55**"],
        ["Contribution margin", "19.7%", "53.9%"]]
fl = {(9, 0): TINT, (9, 1): TINT, (9, 2): TINT}
table(s, 0.55, 1.85, [3.2, 1.35, 2.05], rows, rh=0.36, size=10.5, aligns=["l", "r", "r"], fills=fl)
s.add(R(7.5, 1.85, 5.35, 1.85, LIGHT))
s.add(T(7.6, 1.9, 5.15, 1.75, [Para("Amazon contribution is very sensitive to ad cost", bold=True, color=NAVY, size=11.5),
     Para("Each +1 pt of ACoS = −$0.24 per unit", bullet=True),
     Para("ACoS 25% → $4.73 · 28% (pilot) → $4.01 · 32% (scale median) → $3.05 · 38% (top of range) → $1.61", bullet=True),
     Para("Duty at 25% instead of 15% → −$0.35 per unit (Amazon $4.38; retail $7.20)", bullet=True)], size=10.5, space=4))
s.add(R(7.5, 3.85, 5.35, 2.55, LIGHT))
s.add(T(7.6, 3.9, 5.15, 2.45, [Para("Retail doors cannot carry their own fixed cost", bold=True, color=NAVY, size=11.5),
     Para("Per door: 4.5 units/week × 52 = 234 units × $7.55 = **$1,766** contribution a year", bullet=True),
     Para("Retail-only fixed cost: $6.0M national marketing + $1.5M field sales = **$7.5M** a year", bullet=True),
     Para("Doors needed to cover it: $7.5M ÷ $1,766 ≈ **4,250**, vs 600–1,000 in Option B", bullet=True),
     Para("So retail only pays if it lifts Amazon sales, which is the halo assumption tested on slide 9", bullet=True)], size=10.5, space=4))

# =====================================================================
# 8 Cash curves + tests
B0 = R_["B"]
s = new("tests", "2 · Route: Amazon-led is the only route within the limits",
        "Only the Amazon-led route stays within the board’s limits; retail-led breaches all three even on the planning team’s own inputs")
s.add(T(0.55, 1.48, 6.4, 0.5, [Para("Cumulative cash flow by option, $M (planning-team inputs)", size=12, bold=True, color=NAVY),
                              Para("Operating cash flow less inventory build; end of year", size=9.5, color=MUTED, space_before=1)]))
# axes
px0, px1, py0, py1 = 1.25, 5.9, 2.25, 6.35   # plot box
vmax, vmin = 5, -25
def YV(v): return py0 + (vmax - v) / (vmax - vmin) * (py1 - py0)
xs = [px0 + i * (px1 - px0) / 4 for i in range(5)]
for gv in (5, 0, -5, -10, -15, -20, -25):
    s.add(L(px0, YV(gv), px1, YV(gv), "7F7F7F" if gv == 0 else "E6E6E6", 0.75 if gv == 0 else 0.5))
    s.add(T(px0 - 0.6, YV(gv) - 0.12, 0.52, 0.24, f"{gv:+d}" if gv else "0", size=9, color=MUTED, align="r"))
for i, lab in enumerate(["Start", "2027", "2028", "2029", "2030"]):
    s.add(T(xs[i] - 0.35, py1 + 0.04, 0.7, 0.24, lab, size=9.5, color=INK, align="c"))
s.add(L(px0, YV(-18), px1, YV(-18), BAD, 1.25, dash=True))
s.add(T(px0 + 0.05, YV(-18) + 0.02, 2.6, 0.24, "Investment cap: −$18M", size=9, bold=True, color=BAD))
series = [("A · Amazon-led", A, [0] + [r["cum"] for r in A0["rows"]]),
          ("J · Japan", J, [0] + [r["cum"] for r in J_["rows"]]),
          ("B · Retail-led", B, [0] + [r["cum"] for r in B0["rows"]])]
for nm, col, vals in series:
    s.add(P([(xs[i], YV(v)) for i, v in enumerate(vals)], col, 2.25))
    for i, v in enumerate(vals[1:], 1):
        s.add(R(xs[i] - 0.05, YV(v) - 0.05, 0.1, 0.1, col, "FFFFFF", 0.75, shape="oval"))
# end labels
s.add(T(px1 + 0.08, YV(A0["cum2030"]) - 0.33, 1.15, 0.3, f"A {money(A0['cum2030'], plus=True)}", size=9.5, bold=True, color=INK))
s.add(T(px1 + 0.08, YV(J_["cum2030"]) - 0.02, 1.15, 0.3, f"J {money(J_['cum2030'], plus=True)}", size=9.5, bold=True, color=INK))
s.add(T(px1 + 0.08, YV(B0["cum2030"]) - 0.15, 1.15, 0.3, f"B {money(B0['cum2030'])}", size=9.5, bold=True, color=INK))
# legend
lx = 1.3
for nm, col, _ in series:
    s.add(L(lx, 2.12, lx + 0.3, 2.12, col, 2.25)); s.add(T(lx + 0.33, 2.0, 1.5, 0.25, nm, size=9.5, color=INK)); lx += 1.6
# test table
rows = [["Board test", "A · Amazon-led", "B · Retail-led", "J · Japan"],
        ["Peak cash need ≤ $18M", f"✓ {money(-A0['peak'])}", f"✗ {money(-B0['peak'])}", f"✓ {money(-J_['peak'])}"],
        ["Cash back to zero by end-2030", f"✓ {money(A0['cum2030'], plus=True)} (2030)", f"✗ {money(B0['cum2030'])}", f"✓ {money(J_['cum2030'], plus=True)} (2029)"],
        ["Group margin ≥ 8% every year", f"✓ min {pct(A0['min_gm'])}", f"✗ {pct(B0['rows'][0]['group_margin'])} / {pct(B0['rows'][1]['group_margin'])} / {pct(B0['rows'][2]['group_margin'])} (2027–29)", f"✓ min {pct(J_['min_gm'])}"],
        ["Revenue in 2030", "$26.4M (US)", "$37.6M (US)", "$7.0M (Japan)"]]
yb = table(s, 7.35, 1.55, [1.85, 1.2, 1.35, 1.1], rows, size=10, aligns=["l", "c", "c", "c"], bold_first_col=True,
           heights=[0.45, 0.5, 0.62, 0.72, 0.5])
for e in s.els:
    if isinstance(e, T) and e.paras[0].text[:1] in "✓✗":
        e.color = GOOD if e.paras[0].text.startswith("✓") else BAD; e.bold = True
s.add(R(7.35, yb + 0.15, 5.5, 1.75, LIGHT))
s.add(T(7.45, yb + 0.2, 5.3, 1.65, [Para("Why B fails: fixed cost, not unit margin", bold=True, color=NAVY, size=11),
     Para("B carries $9.6M a year of fixed cost (A: $2.1M) plus $2.0M of 2027 one-offs (setup, launch fee, 600 × $1,100 fixtures).", bullet=True),
     Para("2027 US operating loss of $8.7M takes group margin to (15.4 − 8.7) ÷ (140 + 11.3) = **4.5%**.", bullet=True),
     Para("B buys $11.2M more 2030 revenue than A for $23.2M more cash.", bullet=True)], size=10, space=3))

# =====================================================================
# 9 Retail evidence
s = new("retail", "2 · Route: Amazon-led is the only route within the limits",
        "Retail-led rests on inputs the evidence does not support: at Onsoo’s awareness, newcomers sell 2.6 units per door a week, below the 4.0 delisting line",
        "Source: briefing pack Table 8 (retail analytics firm, 2025, 46 brands), Table 9, sections 10 and 12; team analysis.")
s.add(T(0.55, 1.48, 6.3, 0.5, [Para("First-year sell-through of newcomer skincare brands, US specialty retail", size=12, bold=True, color=NAVY),
                              Para("Units per door per week by aided awareness: median (dot) and interquartile range (bar)", size=9.5, color=MUTED, space_before=1)]))
px0, px1, py0, py1 = 1.2, 6.2, 2.35, 5.6
def YS(v): return py1 - v / 6.0 * (py1 - py0)
for gv in range(0, 7):
    s.add(L(px0, YS(gv), px1, YS(gv), "7F7F7F" if gv == 0 else "EEEEEE", 0.5))
    s.add(T(px0 - 0.45, YS(gv) - 0.12, 0.38, 0.24, str(gv), size=9, color=MUTED, align="r"))
bk = [("Below 10%", 2.6, 1.9, 3.4), ("10–20%", 3.5, 2.8, 4.3), ("Above 20%", 4.6, 3.9, 5.5)]
slot = (px1 - px0) / 3
for i, (nm, med, lo, hi) in enumerate(bk):
    cxm = px0 + slot * (i + 0.5)
    s.add(R(cxm - 0.2, YS(hi), 0.4, YS(lo) - YS(hi), "B9D3F3" if i else "7FAEE8"))
    s.add(R(cxm - 0.09, YS(med) - 0.09, 0.18, 0.18, NAVY, "FFFFFF", 0.75, shape="oval"))
    s.add(T(cxm + 0.24, YS(med) - 0.14, 0.55, 0.28, f"{med}", size=10.5, bold=True, color=INK))
    s.add(T(cxm - 0.8, py1 + 0.04, 1.6, 0.26, nm, size=10, color=INK, align="c"))
s.add(L(px0, YS(4.0), px1, YS(4.0), BAD, 1.25, dash=True))
s.add(L(px0, YS(4.5), px1, YS(4.5), B, 1.25, dash=True))
s.add(T(px0 + 0.02, YS(4.5) - 0.27, 2.6, 0.25, "Option B assumes 4.5", size=9, bold=True, color=INK))
s.add(T(px0 + 0.02, YS(4.0) + 0.01, 3.2, 0.25, "Delisting line after 12 months: 4.0", size=9, bold=True, color=BAD))
s.add(T(px0 - 0.1, py1 + 0.3, 2.6, 0.5, "▲ Onsoo today: 4% aided awareness (9% among K-beauty buyers)", size=9, bold=True, color=A))
s.add(T(0.55, 6.4, 6.4, 0.5, "Even the top quartile of the below-10% group (3.4) falls short of 4.0; at 2.6 units and no halo, B’s peak cash need grows to $26.4M.", size=9.5, color=INK))
pts = [("Sell-through of 4.5 is a best case", "It comes from the retailer’s deck on successful newcomers and matches the median for brands with >20% awareness. Onsoo has 4%. Most likely outcome: removal after the 12-month review."),
       ("The 1.3× halo is a correlation, not a cause", "Doors and Amazon sales correlate at 0.71 across 30 brands, but big brands win doors because they already sell: Saebom added 300 doors after reaching ~$30M on Amazon. B would need a 3.1× halo to pay back by 2030."),
       ("The precedent is a loss of similar size", "Mooncrest went retail-first in 450 doors in 2023, was removed in 2025 and lost an estimated $21M, close to B’s modeled −$20.8M.")]
ty = 1.5
for hd, bd in pts:
    s.add(R(7.25, ty, 0.07, 1.25, B))
    s.add(T(7.42, ty - 0.03, 5.45, 1.32, [Para(hd, bold=True, color=NAVY, size=11.5), Para(bd, size=10.5, space_before=3)]))
    ty += 1.42
s.add(R(7.25, ty + 0.05, 5.6, 0.95, NAVY))
s.add(T(7.35, ty + 0.05, 5.4, 0.95, "To pay back by 2030, B would need a 3.1× halo instead of 1.3×, or 23.5 units per door a week instead of 4.5.", size=11, bold=True, color="FFFFFF", valign="m"))

# =====================================================================
# 10 $40M ambition
s = new("ambition", "2 · Route: Amazon-led is the only route within the limits",
        "No route reaches $40M by 2030 within the limits: Amazon-led gets to ~$26M, and would reach $40M around 2032 if it keeps growing ~29% a year")
s.add(T(0.55, 1.48, 6.6, 0.5, [Para("US revenue by route, $M (planning-team volumes)", size=12, bold=True, color=NAVY),
                              Para("Option B retail revenue at wholesale price", size=9.5, color=MUTED, space_before=1)]))
px0, px1, py0, py1 = 1.15, 6.7, 2.35, 6.0
def YR(v): return py1 - v / 55 * (py1 - py0)
ya = [r["rev"] for r in A0["rows"]]; yb_ = [r["rev"] for r in B0["rows"]]
slot = (px1 - px0) / 4
for i in range(4):
    bx = px0 + slot * i + slot * 0.15; bw = slot * 0.33
    for k, (vals, col) in enumerate(((ya, A), (yb_, B))):
        x = bx + k * (bw + 0.03)
        s.add(R(x, YR(vals[i]), bw, py1 - YR(vals[i]), col))
        s.add(T(x - 0.15, YR(vals[i]) - 0.27, bw + 0.3, 0.26, f"{vals[i]:.1f}", size=9.5, bold=True, color=INK, align="c"))
    s.add(T(px0 + slot * i, py1 + 0.04, slot, 0.26, str(2027 + i), size=10, color=INK, align="c"))
s.add(L(px0, py1, px1, py1, "7F7F7F", 0.75))
s.add(L(px0, YR(40), px1, YR(40), REF, 1.25, dash=True))
s.add(T(px0, YR(40) - 0.27, 3, 0.26, "Ambition: $40M", size=9.5, bold=True, color=MUTED))
s.add(L(1.2, 2.2, 1.5, 2.2, A, 6)); s.add(T(1.55, 2.07, 1.7, 0.26, "A · Amazon-led", size=9.5, color=INK))
s.add(L(3.2, 2.2, 3.5, 2.2, B, 6)); s.add(T(3.55, 2.07, 2.6, 0.26, "B · Retail-led (Amazon + retail)", size=9.5, color=INK))
s.add(T(0.55, 6.38, 6.5, 0.5, "B’s 2030 revenue is $34.3M Amazon (1.43M units × $24) + $3.3M retail (234,000 units × $14).", size=9.5, color=MUTED))
s.add(R(7.4, 1.5, 5.45, 1.45, LIGHT))
s.add(T(7.5, 1.55, 5.25, 1.35, [Para("What it would take to reach $40M", bold=True, color=NAVY, size=11.5),
     Para("A’s 2029→30 growth is 26.4 ÷ 20.4 − 1 = 29%. Held for two more years: $34M in 2031, **$44M in 2032**.", bullet=True),
     Para("B gets closer ($37.6M) but burns $20.8M doing it, above the $18M cap.", bullet=True)], size=10.5, space=3))
s.add(R(7.4, 3.1, 5.45, 1.6, LIGHT))
s.add(T(7.5, 3.15, 5.25, 1.5, [Para("Amazon-first can get there, but not always", bold=True, color=NAVY, size=11.5),
     Para("Saebom (Amazon-first, 2022): ~$30M US revenue by 2025, then added 300 doors: the path A follows.", bullet=True),
     Para("Gaon Lab and Yeoreum (Amazon-first, 2022–23): both below $5M. Two of three stalled, so the gates on slide 13 matter.", bullet=True)], size=10.5, space=3))
s.add(R(7.4, 4.85, 5.45, 1.55, NAVY))
s.add(T(7.5, 4.9, 5.25, 1.45, [Para("Implication for the board", bold=True, color="FFFFFF", size=11.5),
     Para("Read “on the way to $40M by 2030” as a trajectory: “$25M+ by 2030, on a path to $40M by ~2032”. Hitting $40M by 2030 itself would mean relaxing the cash limits, and even B does not get there.", color="FFFFFF", size=10.5, space_before=3)]))

# =====================================================================
# 11 ACoS heatmap
s = new("acos", "3 · How: ad cost decides payback, so commit in stages",
        "Amazon-led pays back by 2030 only if ad cost averages ≤28.6% of sales, below the 32% median for brands at that scale")
s.add(T(0.55, 1.48, 7.2, 0.5, [Para("Option A cumulative cash at end-2030, $M, by ACoS and volume", size=12, bold=True, color=NAVY),
                              Para("Positive = paid back by 2030 (board test). Volume as % of planning-team forecast", size=9.5, color=MUTED, space_before=1)]))
import importlib.util
spec = importlib.util.spec_from_file_location("m", os.path.join(ROOT, "work/model_core.py")); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
acos_rows = [(.25, "25%  planning case"), (.28, "28%  pilot"), (.30, "30%"), (.32, "32%  scale median"), (.35, "35%"), (.38, "38%  top of range")]
vols = [.7, .85, 1.0, 1.15]
gx, gy, lw_, cw_, rh_ = 0.55, 2.4, 2.1, 1.25, 0.56
s.add(T(gx, gy - 0.36, lw_, 0.34, "ACoS", size=10, bold=True, color="FFFFFF", fill=NAVY, valign="m"))
for j, v in enumerate(vols):
    s.add(T(gx + lw_ + j * cw_, gy - 0.36, cw_, 0.34, f"{round(v*100)}%", size=10, bold=True, color="FFFFFF", fill=NAVY, align="c", valign="m"))
def heat(v):
    if v >= 2: return "9EC5F4"
    if v >= 0: return "CDE2FB"
    if v >= -2: return "F6DADA"
    if v >= -4: return "EFB4B3"
    return "E58C8B"
for i, (a, lab) in enumerate(acos_rows):
    yy = gy + i * rh_
    s.add(T(gx, yy, lw_, rh_, lab, size=10, bold=True, color=INK, valign="m", fill=LIGHT))
    for j, v in enumerate(vols):
        val = m.option_A(a, units=[u * v for u in m.A_units])["cum2030"]
        s.add(T(gx + lw_ + j * cw_, yy, cw_, rh_, money(val, plus=True), size=10.5, bold=(a == .25 and v == 1.0), color=INK,
                align="c", valign="m", fill=heat(val)))
    s.add(L(gx, yy + rh_, gx + lw_ + 4 * cw_, yy + rh_, "FFFFFF", 1.5))
for j in range(1, 4):
    s.add(L(gx + lw_ + j * cw_, gy, gx + lw_ + j * cw_, gy + 6 * rh_, "FFFFFF", 1.5))
s.add(R(gx + lw_ + 2 * cw_, gy, cw_, rh_, None, NAVY, 2.0))
s.add(T(gx, gy + 6 * rh_ + 0.08, 7.2, 0.5, "Outlined: planning case. Blue = cash back to zero by 2030; red = not. Every cell keeps peak cash ≤$7.2M and group margin ≥8.8%.", size=9.5, color=MUTED))
s.add(R(7.95, 1.5, 4.9, 5.3, LIGHT))
s.add(T(8.05, 1.55, 4.7, 5.2, [Para("How the 28.6% breakeven is derived", bold=True, color=NAVY, size=11.5),
     Para("Planning case leaves +$2.40M at end-2030 on 2.81M units sold over 2027–30.", bullet=True),
     Para("Each +1 pt ACoS costs $0.24 × 2.81M = $0.67M.", bullet=True),
     Para("Breakeven = 25% + 2.40 ÷ 0.67 pts = **28.6%**; with a 25% tariff from H2 2027: **27.0%**.", bullet=True),
     Para("Why 25% is unlikely to hold", bold=True, color=NAVY, size=11.5, space_before=10),
     Para("The plan assumes ACoS falls as the brand matures; the evidence points the other way.", bullet=True),
     Para("Pilot: 28% on a small budget. Agency data for brands scaling $5–20M on Amazon: median **32%** (range 26–38%), rising as brands bid on broader keywords.", bullet=True),
     Para("A’s revenue is $7–26M in 2027–30, squarely in that band.", bullet=True),
     Para("Volume matters less", bold=True, color=NAVY, size=11.5, space_before=10),
     Para("At 25% ACoS payback survives a 21% volume shortfall; at 28% only a 4% shortfall.", bullet=True)], size=10.5, space=3))

# =====================================================================
# 12 Scenarios
s = new("scenarios", "3 · How: ad cost decides payback, so commit in stages",
        "The downside is bounded: in every case tested, Amazon-led needs at most $7.2M of cash, 40% of the cap, and group margin stays above 8.8%")
cases = [("Planning case", "ACoS 25%, plan volume", m.option_A(.25)),
         ("Pilot ad cost", "ACoS 28%", m.option_A(.28)),
         ("Ramp to benchmark", "ACoS 28% → 30% → 32% → 32%", m.option_A(acos_path=[.28, .30, .32, .32])),
         ("Scale benchmark", "ACoS 32% (agency median)", m.option_A(.32)),
         ("Tariff rise", "Duty 25% from H2 2027, ACoS 25%", m.option_A(tariff=True)),
         ("Benchmark + tariff", "ACoS 32%, duty 25%", m.option_A(.32, tariff=True)),
         ("Volume shortfall", "70% of plan volume, ACoS 28%", m.option_A(.28, units=[u * .7 for u in m.A_units])),
         ("Top of ACoS range", "ACoS 38%", m.option_A(.38)),
         ("Stall like Gaon Lab / Yeoreum", "Flat 200k units (~$4.8M) a year, ACoS 32%", m.option_A(.32, units=[200000] * 4)),
         ("Combined stress", "ACoS 38% and 70% of plan volume", m.option_A(.38, units=[u * .7 for u in m.A_units]))]
rows = [["Case", "What changes vs planning case", "Peak cash need", "Cash, end-2030", "Lowest group margin", "Board tests"]]
fl = {}
for i, (nm, chg, r) in enumerate(cases, 1):
    ok = r["cum2030"] >= 0
    rows.append([nm, chg, money(-r["peak"]), money(r["cum2030"], plus=True), pct(r["min_gm"]),
                 "✓ All met" if ok else "◐ Payback missed"])
    fl[(i, 3)] = "CDE2FB" if ok else "F6DADA"
yb = table(s, 0.55, 1.5, [2.55, 3.4, 1.35, 1.35, 1.45, 2.2], rows, rh=0.36, size=10, aligns=["l", "l", "c", "c", "c", "l"],
           bold_first_col=True, fills=fl, heights=[0.42] + [0.36] * 10)
for e in s.els:
    if isinstance(e, T) and e.paras[0].text[:1] in "✓◐":
        e.color = GOOD if e.paras[0].text.startswith("✓") else WARN; e.bold = True
s.add(T(0.55, yb + 0.1, 7.6, 0.85, [Para("For comparison, Option B’s planning case needs **$20.8M**. Even the combined stress case for A uses 40% of the $18M cap, and the gates on the next slide are set to stop scaling long before these totals are reached.", size=10),
                                    Para("Payback in the benchmark case: if units keep growing 20% a year after 2030, cumulative cash turns positive in 2032 (illustrative).", size=9.5, color=MUTED)], space=3))
s.add(R(8.4, yb + 0.12, 4.45, 0.82, NAVY))
s.add(T(8.5, yb + 0.12, 4.25, 0.82, "The risk in A is missing the 2030 payback, not breaching the cap or the margin floor.", size=11, bold=True, color="FFFFFF", valign="m"))

# =====================================================================
# 13 Gated plan
s = new("gates", "3 · How: ad cost decides payback, so commit in stages",
        "Fund Amazon-led in gated stages, so the ad-cost question is answered on $2–3M of exposure before most of the money is spent")
cols = [("STAGE 1 · Mar–Dec 2027", "Build and prove ad cost at scale", A, [
            "US entity, MoCRA registration and safety substantiation, English labels (fixes the 6% complaint)",
            "Four new SKUs; US team; $0.7M off-Amazon social budget aimed at TikTok, where 38% discover brands",
            "2027 cost: $0.8M setup + $2.1M fixed; cash need **$1.9–2.9M** (ACoS 25–38%)",
            "Track monthly: ACoS, units vs 300k plan, 90-day repeat (29% today, 31% benchmark), tariff decision"]),
        ("GATE 1 · Q1 2028 board", "Decide on H2-2027 data, at a $5–20M run-rate", NAVY, [
            "**Green: ACoS ≤28% and volume on plan** → proceed to Stage 2 as planned; payback by 2030 holds",
            "**Amber: ACoS 28–34%** → proceed, but freeze new fixed cost and no retail; payback slips to ~2031–32 with peak cash ≤$4.4M",
            "**Red: ACoS >34% or volume <70% of plan** → above 34% the US makes no operating profit even in 2029; cut back to core SKUs, re-plan, free the 2028 slot for Japan",
            "If duty rises to 25%, lower each ACoS threshold by ~1.5 pts"]),
        ("STAGE 2 · 2028–2029", "Scale on Amazon; build awareness", A, [
            "Grow to 560k / 850k units; widen the range only where SKU-level economics match the hero product",
            "Build awareness off-Amazon (social, TikTok) and measure aided awareness among category buyers every six months",
            "**Gate 2 (2029):** specialty retail is an option, triggered only as set out on the next slide"])]
x = 0.55
for i, (hd, sub, col, buls) in enumerate(cols):
    wcol = 4.0
    s.add(R(x, 1.5, wcol, 0.75, col))
    s.add(T(x + 0.08, 1.52, wcol - 0.16, 0.72, [Para(hd, size=10, bold=True, color="FFFFFF"), Para(sub, size=11.5, bold=True, color="FFFFFF", space_before=2)], valign="m"))
    s.add(R(x, 2.25, wcol, 3.45, LIGHT))
    s.add(T(x + 0.08, 2.33, wcol - 0.16, 3.35, [Para(b, bullet=True) for b in buls], size=10.5, space=6))
    if i < 2:
        s.add(T(x + wcol - 0.02, 3.6, 0.2, 0.5, "›", size=22, bold=True, color=MUTED, align="c", check=False))
    x += wcol + 0.15
s.add(T(0.55, 6.3, 12.3, 0.5, "**Exposure at Gate 1** is the 2027 cash need of $1.9–2.9M, 11–16% of the $18M cap. If amber, peak cash stays ≤$4.4M; the red gate stops scaling before the $6–7M stress outcomes on slide 12.", size=10.5, color=NAVY, fill=TINT, valign="m"))
s.add(T(0.55, 5.78, 12.3, 0.5, "Thresholds come from the model: 28% ≈ the 28.6% payback breakeven; 34% ≈ the ACoS at which 2029 US operating profit is zero: ($10.73 contribution per unit before ads − $2.1M ÷ 850k units) ÷ $24 = 34.4%.", size=9.5, color=MUTED))

# =====================================================================
# 14 Retail option
s = new("retailoption", "3 · How: ad cost decides payback, so commit in stages",
        "Specialty retail should be earned, not scheduled: raise the awareness trigger to 20% and prove 4.0 units per door in a test before any national roll-out")
rows = [["Trigger", "CEO’s initial hypothesis", "Recommended", "Why"],
        ["Amazon sales", "> $10M", "> $10M (keep)", "Reached in 2028 on plan ($13.4M); proves the brand sells online"],
        ["Aided awareness", "> 15%", "≥ 20% among category buyers (4% today)", "At 10–20%, median sell-through is 3.5 units (IQR 2.8–4.3), below the 4.0 removal line; above 20% it is 4.6"],
        ["Proof in store", "None: straight to roll-out", "12-month test in a limited set of doors at ≥ 4.0 units/door/week", "The retailer removes newcomers below 4.0 after 12 months; a test caps the Mooncrest-type loss"],
        ["Halo", "Assumed 1.3×", "Measured: Amazon sales in test regions vs elsewhere", "The 0.71 correlation does not show cause; retail only pays if the halo is real (slide 7)"],
        ["Cost base", "$7.5M a year national marketing + field team", "Re-sized to the test; national budget only after the test", "At $1,766 per door a year, 600–1,000 doors cover $1.1–1.8M, not $7.5M"]]
yb = table(s, 0.55, 1.5, [1.6, 2.5, 3.45, 4.75], rows, size=10.5, aligns=["l", "l", "l", "l"], bold_first_col=True,
           heights=[0.4, 0.55, 0.72, 0.72, 0.62, 0.62], fills={(r, 2): TINT for r in range(1, 6)})
s.add(R(0.55, yb + 0.2, 12.3, 1.15, LIGHT))
s.add(T(0.65, yb + 0.24, 12.1, 1.1, [Para("Getting from 4% to 20% awareness is the real retail question", bold=True, color=NAVY, size=11.5),
     Para("K-beauty buyers discover new brands on TikTok (38%) more than in stores (17%), so awareness is cheaper to build with the off-Amazon social budget than with $6M of in-store marketing. This mirrors Saebom, which added 300 doors only after reaching ~$30M on Amazon.", size=10.5, space_before=3)]))

# =====================================================================
# 15 Risks
s = new("risks", "3 · How: ad cost decides payback, so commit in stages",
        "Four uncertainties drive the result; ad cost matters most, and each has an early signpost and a planned response")
rows = [["Uncertainty", "Effect on Option A (plan: +$2.4M cash, end-2030)", "Early signpost", "Response"],
        ["1  Ad cost at scale", "Each +1 pt ACoS = −$0.67M; at the 32% median, −$2.3M (payback missed)", "Monthly ACoS once run-rate passes $5M", "Gate 1 thresholds; shift spend to social/TikTok; favour SKUs with better repeat"],
        ["2  Volume and repeat", "−15% volume: +$0.7M (still pays back); stall like Gaon Lab: −$7.1M", "Units vs plan; 90-day repeat (29% vs 31% benchmark)", "US labels, new SKUs; red gate at <70% of plan"],
        ["3  Tariff 15% → 25%", "−$0.35/unit; −$1.1M by 2030; breakeven ACoS 28.6% → 27.0%", "US decision, mid-2027", "Re-run gates; consider price test (52% cite price as a reason to buy, so cautiously)"],
        ["4  FX (won)", "10% weaker won ≈ +$0.40/unit ≈ +$1.1M (if product cost is all in won)", "KRW/USD", "Upside; set a hedging policy for the US cost base"]]
yb = table(s, 0.55, 1.5, [2.0, 4.0, 2.75, 3.55], rows, size=10.5, bold_first_col=True, heights=[0.42, 0.72, 0.72, 0.72, 0.62])
s.add(T(0.55, yb + 0.2, 12.3, 0.3, "Key assumptions behind every number in this deck", size=11.5, bold=True, color=NAVY))
asm = ["Hero-product unit economics apply to all SKUs (planning-team convention); real SKU margins may differ.",
       "Inventory = four months of landed cost (ex-factory + freight + duty), built up as volumes grow; not released by 2030.",
       "All one-time costs, including in-store fixtures, expensed in the year incurred; no value counted beyond 2030.",
       "Group margin = (ex-US plan at 11.0% + US operating profit) ÷ (ex-US plan revenue + US revenue); the ex-US plan excludes the Japan scale-up.",
       "Japan (Option J) has no working-capital build (none given); this flatters J slightly."]
s.add(T(0.55, yb + 0.52, 12.3, 1.6, [Para(a, bullet=True) for a in asm], size=10, space=2))

# =====================================================================
# 16 Decisions
s = new("decisions", "Recommendation",
        "We ask the board to approve Stage 1 of the Amazon-led entry in March 2027 and to set the rules for the next two gates now")
dec = [("Approve", "US entry in 2027 via Option A, Amazon-led; reject the 600-door national retail launch (Option B); defer the Japan scale-up.", "2027 cash need $1.9–2.9M"),
       ("Adopt", "Gate 1 thresholds for the Q1 2028 board: green ≤28% ACoS on plan volume; amber 28–34%; red >34% or volume <70% of plan.", "Derived on slides 11 and 13"),
       ("Pre-agree", "Whether, in the amber case, a payback slip to ~2031–32 is acceptable while peak cash stays ≤$4.4M and group margin ≥9%. We recommend yes: the cap and floor hold, and Japan’s alternative adds only $1.8M.", "A departure from the 2030 payback limit: the board’s call"),
       ("Restate", "The ambition as “$25M+ US revenue by 2030, on a path to $40M by ~2032”; no route reaches $40M by 2030 within the cash limits.", "Slide 10"),
       ("Replace", "The retail trigger: Amazon sales >$10M and ≥20% aided awareness and a 12-month door test at ≥4.0 units/door/week.", "Slide 14")]
y = 1.5
for i, (verb, txt, note) in enumerate(dec, 1):
    s.add(R(0.55, y, 0.5, 0.78, NAVY)); s.add(T(0.55, y, 0.5, 0.78, str(i), size=16, bold=True, color="FFFFFF", align="c", valign="m"))
    s.add(T(1.15, y, 1.4, 0.78, verb, size=13, bold=True, color=NAVY, valign="m"))
    s.add(T(2.55, y, 7.7, 0.78, txt, size=11, color=INK, valign="m"))
    s.add(T(10.35, y, 2.5, 0.78, note, size=9.5, color=MUTED, valign="m"))
    s.add(L(1.15, y + 0.84, 12.83, y + 0.84, GRID, 0.5))
    y += 0.9
s.add(R(0.55, y + 0.05, 12.3, 0.85, LIGHT))
s.add(T(0.65, y + 0.07, 12.1, 0.82, [Para("Before the March board meeting", bold=True, color=NAVY, size=11),
     Para("Rebuild the model with SKU-level economics for the four new SKUs · agree an ad plan and ACoS reporting with the agency · start English labelling · prepare a tariff (25% duty) version of the gates", size=10.5, space_before=2)]))

# =====================================================================
# Appendix A1: Option A build
def build_table(s, res, label, extra_rows=None):
    yrs = [r["year"] for r in res["rows"]]
    rows = [["$M", *map(str, yrs), "Calculation"]]
    rows += extra_rows(res)
    return rows

s = new("appA", "Appendix",
        "Option A (planning case): the US turns cash-positive in 2028 and pays back in 2030, with peak cash of $1.9M",
        "Source: briefing pack Tables 4–6 and group context; team analysis. Figures may not add due to rounding.")
rA = R_["A"]["rows"]
rows = [["$M", "2027", "2028", "2029", "2030", "Calculation"],
        ["Amazon units (000)", *[f"{r['units']/1000:,.0f}" for r in rA], "Table 5"],
        ["Revenue", *[f"{r['rev']:.1f}" for r in rA], "units × $24.00"],
        ["Contribution", *[f"{r['contrib']:.2f}" for r in rA], "units × $4.725 (slide 7, ACoS 25%)"],
        ["Fixed and one-time cost", *[nf(-r['fixed']) for r in rA], "$0.5M compliance + $0.9M team + $0.7M marketing; +$0.8M setup in 2027"],
        ["US operating profit", *[nf(r['op']) for r in rA], "contribution − fixed"],
        ["Inventory build", *[nf(-r['dinv']) for r in rA], "change in (units × $4.575 landed cost × 4/12)"],
        ["Cash flow", *[nf(r['cf']) for r in rA], "operating profit − inventory build"],
        ["Cumulative cash", *[nf(r['cum']) for r in rA], "running total; peak −1.94 (2027)"],
        ["Group operating margin", *[pct(r['group_margin']) for r in rA], "(ex-US 11% × plan revenue + US op.) ÷ total revenue"]]
yb = table(s, 0.55, 1.5, [2.4, 1.05, 1.05, 1.05, 1.05, 5.7], rows, rh=0.36, size=10.5, aligns=["l", "r", "r", "r", "r", "l"], bold_first_col=True,
           fills={(8, c): TINT for c in range(6)})
r32 = R_["A32"]["rows"]
s.add(T(0.55, yb + 0.15, 12.3, 0.3, "Same model at benchmark ACoS 32% (contribution $3.045 per unit)", size=11.5, bold=True, color=NAVY))
rows = [["$M", "2027", "2028", "2029", "2030", ""],
        ["US operating profit", *[nf(r['op']) for r in r32], ""],
        ["Cumulative cash", *[nf(r['cum']) for r in r32], "peak −3.24 (2028); −2.32 at end-2030, so payback is missed"]]
table(s, 0.55, yb + 0.5, [2.4, 1.05, 1.05, 1.05, 1.05, 5.7], rows, rh=0.34, size=10.5, aligns=["l", "r", "r", "r", "r", "l"], bold_first_col=True)

# Appendix A2: Option B build
s = new("appB", "Appendix",
        "Option B (planning case): fixed costs of $9.6M a year keep the US loss-making through 2030, and cash need peaks at $20.8M",
        "Source: briefing pack Tables 4–6 and group context; team analysis. Figures may not add due to rounding.")
rB = R_["B"]["rows"]
rows = [["$M", "2027", "2028", "2029", "2030", "Calculation"],
        ["Doors / retail units (000)", *[f"{r['doors']:,} / {r['ret_units']/1000:.0f}" for r in rB], "doors × 4.5 units × 52 weeks"],
        ["Amazon units (000)", *[f"{r['amz_units']/1000:,.0f}" for r in rB], "Option A × 1.3 halo"],
        ["Revenue", *[f"{r['rev']:.1f}" for r in rB], "Amazon × $24 + retail × $14 wholesale"],
        ["Contribution", *[f"{r['contrib']:.2f}" for r in rB], "Amazon × $4.725 + retail × $7.545"],
        ["Fixed cost", *[nf(-r['fixed']) for r in rB], "$2.1M as A + $6.0M retail marketing + $1.5M field sales"],
        ["One-time cost", *[nf(-r['one_time']) for r in rB], "2027: $0.8M setup + $0.5M fee + 600 doors × $1,100; later 200 doors × $1,100"],
        ["US operating profit", *[nf(r['op']) for r in rB], "contribution − fixed − one-time"],
        ["Inventory build", *[nf(-r['dinv']) for r in rB], "four months of landed cost ($4.575 Amazon, $4.775 retail)"],
        ["Cumulative cash", *[nf(r['cum']) for r in rB], "never turns; −20.80 at end-2030 vs −18 cap"],
        ["Group operating margin", *[pct(r['group_margin']) for r in rB], "below 8% in 2027, 2028 and 2029"]]
yb = table(s, 0.55, 1.5, [2.4, 1.05, 1.05, 1.05, 1.05, 5.7], rows, rh=0.38, size=10.5, aligns=["l", "r", "r", "r", "r", "l"], bold_first_col=True,
           fills={(9, c): TINT for c in range(6)})
s.add(T(0.55, yb + 0.15, 12.3, 0.85, [Para("**What B would need to pay back by 2030 (other inputs unchanged):** a 3.1× Amazon halo instead of 1.3×, or 23.5 units per door per week instead of 4.5. Its group margin stays below 8% in 2027 even then (5.6% at a 3× halo).", size=10.5),
     Para("**Realistic inputs** (2.6 units/door/week, no halo): peak cash −$26.4M. If delisted after the 12-month review, the loss is cut, but peak cash still reaches −$10.1M in 2027 alone.", size=10.5)], space=4))

# Appendix A3: judgement calls
s = new("appC", "Appendix",
        "Judgement calls we made where the briefing pack was ambiguous; each is flagged so the board can challenge it",
        "Source: team analysis of the briefing pack.")
rows = [["Question", "Choice made", "Effect if the other choice were made"],
        ["What does “on the way to $40M by 2030” mean?", "A trajectory, not a hard 2030 test, since no route reaches $40M by 2030 on planning inputs", "If hard: no option passes; the board must relax cash limits or the target"],
        ["Which awareness measure applies to Table 8?", "Aided awareness among all category buyers: 4% (9% among K-beauty buyers)", "None: both are below 10%, so the same 2.6 median applies"],
        ["How is inventory treated?", "Year-end stock = 4/12 of the year’s landed cost; the build is a cash outflow; no release by 2030", "Lower stock would improve A and B similarly; ranking unchanged"],
        ["Are fixtures and launch fees expensed?", "Yes, in the year incurred (also counted in group margin)", "Capitalising fixtures lifts B’s 2027 margin by <0.5 pt; still below 8%"],
        ["When would a tariff rise bite?", "Duty 20% blended in 2027 (25% from mid-year), 25% from 2028", "Full-year 2027 at 25% costs a further ~$0.05M"],
        ["Does the ex-US plan include the Japan scale-up?", "No: J is incremental to the $140–158M plan", "If it were included, choosing the US removes J’s small profit (≤$1.3M a year) from the plan; conclusions unchanged"],
        ["Which K-beauty market size?", "$3.6B skincare (Table 1), not the $5.2B trade-press figure that adds makeup and hair care", "Market size does not constrain any option"]]
table(s, 0.55, 1.5, [3.3, 4.8, 4.2], rows, size=10.5, bold_first_col=True, heights=[0.4] + [0.64] * 7)

# =====================================================================
out_pptx = os.path.join(ROOT, "deliverable", "Onsoo_US_entry_board_deck.pptx")
to_pptx(slides, out_pptx)
os.makedirs(os.path.join(ROOT, "work/preview"), exist_ok=True)
issues = []
for i, sl in enumerate(slides, 1):
    issues += to_png(sl, os.path.join(ROOT, f"work/preview/s{i:02d}_{sl.name}.png"))
print("\n".join(issues) or "no overflow issues")
print(len(slides), "slides ->", out_pptx)
