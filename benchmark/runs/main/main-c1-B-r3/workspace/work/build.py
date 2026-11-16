import io, contextlib, runpy, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from lib import *

with contextlib.redirect_stdout(io.StringIO()):
    M = runpy.run_path(os.path.join(os.path.dirname(__file__), "model.py"))
run, run_j, amazon_cm, retail_cm = M["run"], M["run_j"], M["amazon_cm"], M["retail_cm"]
A_UNITS, DOORS = M["A_UNITS"], M["DOORS"]
B_AMZ = [390_000, 728_000, 1_105_000, 1_430_000]
A = run(A_UNITS); A32 = run(A_UNITS, acos=0.32); B = run(B_AMZ, DOORS); J = run_j()
mm = lambda v: v / 1e6

prs = new_prs()
BL = prs.slide_layouts[6]
N = [0]


def slide(section, title, source=None):
    s = prs.slides.add_slide(BL)
    N[0] += 1
    if title:
        header(s, section, title)
    footer(s, source, N[0])
    return s


def takeaway(s, y, t, h=0.5, size=12):
    rect(s, L, y, CW, h, fill=PANEL)
    rect(s, L, y, 0.07, h, fill=NAVY)
    text(s, L + 0.2, y, CW - 0.3, h, t, size=size, color=INK, anchor="m")


# =====================================================================
# 1. Title
s = prs.slides.add_slide(BL); N[0] += 1
rect(s, 0, 0, W, H, fill=NAVY)
rect(s, L, 2.2, 0.08, 2.0, fill=A_COL)
text(s, L + 0.3, 2.1, 11.5, 1.3, "US market entry: should Onsoo enter in 2027, and by which route?",
     size=34, bold=True, color=WHITE, line_spacing=1.0)
text(s, L + 0.3, 3.45, 11.5, 0.9,
     "Recommendation to CEO Park Ji-won and the Board of Onsoo Botanicals for the March 2027 board meeting",
     size=16, color="C9D3E6")
text(s, L + 0.3, 5.9, 11.5, 0.9,
     ["Prepared November 2026 from the planning team's briefing pack only (no external research)",
      "All company, competitor and market figures in the pack are synthetic benchmark data. $ = US dollars; M = millions"],
     size=11, color="9FB0CC", space_after=2)

# =====================================================================
# 2. Executive summary
s = slide(None, "Executive summary: enter the US in 2027 through Amazon (Option A), reset the 2030 targets, and add specialty retail only after awareness reaches 20%",
          "Onsoo planning-team briefing pack (Nov 2026); team analysis. Detailed calculations in the appendix.")
rows = [
    ("The US is the right market for the 2027 slot",
     "US K-beauty facial skincare is $3.6B and grew 17% a year in 2021–25. The Amazon pilot nearly doubled monthly units in six months at 4.5 stars. "
     "By 2030, Option A builds a US business of **$26M**, against **$7M** of extra revenue from a Japan scale-up. Japan is safer on cash to 2030, and it can follow in 2028."),
    ("Amazon-led (A) beats retail-led (B) on every board test",
     "On its own inputs, B breaches the $18M cash cap (**–$20.8M** by 2030), does not pay back and cuts group margin to **4.5%** in 2027. "
     "Its 4.5 units/door/week is what brands with >20% awareness sell (Onsoo: 4%), and its 1.3× Amazon halo rests on a correlation."),
    ("Even Option A will not hit every target, so the board should reset two of them",
     "A's peak cash need is $1.9–4.9M in every case except the severe one, and group margin stays at 9% or more. But payback by 2030 needs ad cost (ACoS) of **≤28.6%** against a 32% "
     "benchmark (otherwise ~2032), and 2030 revenue is **$26M, not $40M** ($40M around 2032)."),
    ("Specialty retail should come later, behind stricter gates",
     "At the CEO's 15% awareness trigger, brands sell a median 3.5 units/door/week, below the retailer's 4.0 removal line. Adding national retail in 2029 would cut 2029 group margin to "
     "**6.8%** and leave US cash at **–$9.6M** in 2030. Gate retail on ≥20% awareness and a measured halo."),
]
y0 = 1.72
for i, (k, v) in enumerate(rows):
    yy = y0 + i * 1.02
    number_badge(s, L, yy + 0.08, 0.36, i + 1)
    text(s, L + 0.5, yy, 3.55, 0.95, k, size=12.5, bold=True, color=NAVY, anchor="t")
    text(s, L + 4.2, yy, CW - 4.2, 0.95, v, size=11, color=INK, anchor="t")
    if i < 3:
        line(s, L + 0.5, yy + 0.98, W - R, yy + 0.98, color=GRID)
rect(s, L, 5.85, CW, 1.05, fill=PANEL)
rect(s, L, 5.85, 0.07, 1.05, fill=NAVY)
text(s, L + 0.2, 5.88, 2.0, 0.3, "Decisions for March 2027", size=11, bold=True, color=NAVY)
text(s, L + 0.2, 6.17, CW - 0.4, 0.72,
     ["**(1)** Approve Option A with a $5M peak-cash envelope.   **(2)** Restate the US targets: $25M+ revenue in 2030, $40M by ~2032, payback by 2030 at ≤28.6% ACoS and by 2032 at most.",
      "**(3)** Reject retail-first and replace the 2029 retail trigger with evidence gates.   **(4)** Review the Japan scale-up for 2028; the bandwidth limit applies to 2027 only."],
     size=10.5, color=INK, space_after=2)

# =====================================================================
# 3. Hypothesis test
s = slide("Approach", "We tested the CEO's hypothesis against five conditions. Two hold, one holds in part and two fail, so the route stands but the targets and retail trigger change",
          "Briefing pack §4 (CEO hypothesis), Tables 1–9, §10–12; team analysis.")
text(s, L, 1.62, CW, 0.5,
     "Starting hypothesis (CEO): “Launch in the US in 2027 through Amazon, then add specialty beauty retail from 2029 once Amazon sales pass $10M and aided awareness passes 15%.”",
     size=11.5, italic=True, color=INK2)
hdr = ["What would have to be true", "What the evidence shows", "Verdict"]
data = [
    ("1  The US is a better use of 2027 than a Japan scale-up",
     "US K-beauty is growing 17% a year against 1.5% for Japanese skincare. Option A reaches $26M by 2030, against $7M for Japan. But Japan is ahead on cash to 2030 unless ACoS stays at or below the pilot's 28%.", "good", "Holds, on scale"),
    ("2  Amazon is the right lead channel",
     "Amazon carries 41% of US K-beauty sales; 61% of K-beauty buyers buy there most often. The pilot sells at 4.5 stars; repeat is 29% against a 31% benchmark.", "good", "Holds"),
    ("3  Amazon-led stays within the cash, payback and margin limits",
     "Peak cash is $1.9–3.2M against the $18M cap, and group margin stays at 9.1% or more. Payback by 2030 holds only at ACoS ≤28.6%; at the 32% scaling benchmark it slips to ~2032.", "part", "Partly"),
    ("4  It puts Onsoo on the way to $40M by 2030",
     "Option A reaches $26.4M in 2030, and Option B $37.6M (while breaking the cash cap). At 20% growth after 2030, Option A reaches $40M in about 2032.", "bad", "Fails for 2030"),
    ("5  Retail added in 2029 at >$10M Amazon sales and >15% awareness pays off",
     "At 10–20% awareness, brands sell a median 3.5 units/door/week, below the 4.0 removal line. A national add in 2029 takes 2029 group margin to 6.8% and US cash to –$9.6M by 2030.", "bad", "Fails as specified"),
]
yy = 2.12
rect(s, L, yy, CW, 0.34, fill=NAVY)
for cx, cw, t in [(L, 4.1, hdr[0]), (L + 4.1, 6.9, hdr[1]), (L + 11.0, 1.33, hdr[2])]:
    text(s, cx + 0.08, yy, cw - 0.1, 0.34, t, size=10.5, bold=True, color=WHITE, anchor="m")
yy += 0.34
for a, b, k, lab in data:
    text(s, L + 0.08, yy, 3.95, 0.72, a, size=11, bold=True, color=NAVY, anchor="m")
    text(s, L + 4.18, yy, 6.75, 0.72, b, size=10.5, color=INK, anchor="m")
    pill(s, L + 11.05, yy + 0.17, 1.28, 0.38, k, lab, size=9)
    yy += 0.74
    line(s, L, yy - 0.01, W - R, yy - 0.01, color=GRID)
takeaway(s, 6.25, "**Revised answer:** keep the Amazon-led route; restate the 2030 revenue and payback targets around ad cost; replace the 15% retail trigger with a 20% awareness gate plus a measured halo.", h=0.62, size=11.5)

# =====================================================================
# 4. Market
s = slide("1 · Why the US", "US K-beauty facial skincare is a $3.6B market growing 17% a year, about five times as fast as other brands in the category",
          "Table 1 (US facial skincare sales); Table 2 (K-beauty channel shares, 2025); §12 (trade-press figure). CAGR = compound annual growth rate.")
years = ["2021", "2022", "2023", "2024", "2025"]
kb = [1.9, 2.3, 2.7, 3.1, 3.6]
allf = [20.1, 21.3, 22.6, 23.5, 24.5]
other = [round(a - k, 1) for a, k in zip(allf, kb)]
text(s, L, 1.65, 7.4, 0.3, "US facial skincare sales by brand origin, $B", size=11, bold=True, color=INK)
legend(s, L, 1.95, [("K-beauty brands", A_COL), ("Other brands", "D5D4CF")])
bar_chart(s, L, 2.35, 7.4, 4.45, years,
          [dict(name="K", values=kb, color=A_COL), dict(name="O", values=other, color="D5D4CF", dark=False)],
          0, 26, [0, 5, 10, 15, 20, 25], lambda t: f"{t:.0f}", label_fmt=lambda v: f"{v:.1f}", stacked=True,
          stack_labels=[f"{a:.1f}" for a in allf], gap=0.4)
# right panel
px = 8.35
stats = [
    ("17.3%", "K-beauty CAGR 2021–25 (1.9 → 3.6), against 3.5% for other brands (18.2 → 20.9). K-beauty's share of the category rose from 9.5% to 14.7%."),
    ("$1.5B", "K-beauty sold on Amazon in 2025 (41% of $3.6B), the largest channel. Specialty beauty retail carried 27% ($1.0B)."),
    ("0.5–0.7%", "Share of 2030 US K-beauty facial skincare that $40M would be, if growth runs at 10–17% a year ($5.8–8.0B). Market size is not the constraint."),
]
for i, (big, small) in enumerate(stats):
    yy = 1.75 + i * 1.5
    text(s, px, yy, 4.5, 0.55, big, size=26, bold=True, color=A_COL)
    text(s, px, yy + 0.55, 4.45, 0.9, small, size=10.5, color=INK)
text(s, px, 6.3, 4.45, 0.6, "Not used: the trade-press “$5.2B US K-beauty market” also counts makeup and hair care, so it overstates Onsoo's market.",
     size=9.5, italic=True, color=INK2)

# =====================================================================
# 5. Pilot
s = slide("1 · Why the US", "The Amazon pilot shows real US demand: monthly units nearly doubled in six months at 4.5 stars, and repeat is close to the benchmark",
          "Section 6 / Table 3 (Amazon pilot, Jan–Jun 2026, three SKUs via a cross-border seller); Table 5 (Option A 2027 volume); team analysis.")
text(s, L, 1.65, 6.6, 0.3, "Pilot units sold per month, 2026 (three SKUs)", size=11, bold=True, color=INK)
mon = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
pv = [7400, 8600, 10100, 11800, 12900, 14000]
ax, px0, pw, slot = bar_chart(s, L, 2.05, 6.6, 3.9, mon, [dict(name="u", values=[v / 1000 for v in pv], color=A_COL)],
                              0, 16, [0, 4, 8, 12, 16], lambda t: f"{t:.0f}k", label_fmt=lambda v: f"{v:.1f}k", gap=0.45)
mom = ["", "+16%", "+17%", "+17%", "+9%", "+9%"]
for i, m_ in enumerate(mom):
    if m_:
        text(s, px0 + i * slot, 5.95, slot, 0.25, m_, size=9, color=INK2, align="c")
text(s, L, 5.95, 0.55, 0.25, "m/m", size=9, color=MUTED, align="r")
text(s, L, 6.3, 6.6, 0.6, "Growth is slowing. The 2027 plan of 300k units needs ~4.6% a month sustained from July 2026, plus four new SKUs; at 3% a month, 2027 reaches ~244k.",
     size=10, color=INK2)
px = 7.6
kp = [
    ("64,800 units · $1.56M", "sold in six months with three SKUs, no US entity and no brand-run marketing"),
    ("4.5 stars · 2,140 reviews", "The top complaint (6% of reviews) is Korean-only label text, which the $0.8M setup budget for US labels fixes"),
    ("28% ACoS", "Ad spend as a share of Amazon sales, on a small budget. This is the number that decides payback (section 3)"),
    ("29% 90-day repeat", "Against 31% for first-year skincare brands on Amazon US and 48% for Onsoo in Korea: on par, not yet a strength"),
]
for i, (a, b) in enumerate(kp):
    yy = 1.7 + i * 1.22
    rect(s, px, yy, 0.06, 1.0, fill=A_COL)
    text(s, px + 0.2, yy, 5.0, 0.36, a, size=14, bold=True, color=NAVY)
    text(s, px + 0.2, yy + 0.38, 5.0, 0.7, b, size=10.5, color=INK)

# =====================================================================
# 6. US vs Japan
s = slide("1 · Why the US", "By 2030 a US launch builds a business nearly 4× the size of a Japan scale-up; Japan is safer on cash and can follow in 2028",
          "Tables 5–7; group context (§8); team model (appendix A3, A5). Option J figures are incremental to today's Japan business.")
text(s, L, 1.65, 5.6, 0.3, "Added revenue by option, $M", size=11, bold=True, color=INK)
legend(s, L, 1.95, [("Option A · US Amazon-led", A_COL), ("Option J · Japan scale-up", J_COL)])
ar = [mm(r["revenue"]) for r in A["rows"]]
jr = [mm(r["revenue"]) for r in J["rows"]]
bar_chart(s, L, 2.4, 5.6, 4.35, ["2027", "2028", "2029", "2030"],
          [dict(name="A", values=ar, color=A_COL), dict(name="J", values=jr, color=J_COL)],
          0, 30, [0, 10, 20, 30], lambda t: f"{t:.0f}", label_fmt=lambda v: f"{v:.1f}", gap=0.3)
tx = 6.55
rows_ = [["$M unless stated", "A · ACoS 25% (plan)", "A · ACoS 32% (benchmark)", "J · Japan"],
         ["2030 revenue", "26.4", "26.4", "7.0"],
         ["Market growth", "17% (US K-beauty)", "17% (US K-beauty)", "1.5% (Japan)"],
         ["Peak cumulative cash", "–1.9", "–3.2", "–1.1"],
         ["Cumulative cash, end-2030", "+2.4", "–2.3", "+1.8"],
         ["2030 operating profit", "3.1", "1.2", "1.3"],
         ["Serves the US ambition", "Yes", "Yes", "No"]]
table(s, tx, 1.7, [1.95, 1.45, 1.6, 1.28], rows_, rowh=0.44, size=10, aligns=["l", "c", "c", "c"],
      fills={(4, 2): CRIT_T, (4, 3): GOOD_T, (4, 1): GOOD_T, (6, 3): CRIT_T})
text(s, tx, 4.95, 6.3, 1.9,
     [dict(t="**Why the US anyway:** the board's ambition is a US business, and only the US offers a market growing 11× faster than Japan's. By 2030 Option A is still growing 29% a year, while J's additions are levelling off.", bullet=True),
      dict(t="**What Japan offers:** about $4M more cash by 2030 if US ad costs reach the benchmark. The bandwidth limit covers 2027 only, so a Japan scale-up can be reviewed for 2028 rather than given up.", bullet=True)],
     size=10.5, space_after=6)

# =====================================================================
# 7. Unit economics
s = slide("2 · Which route", "Amazon leaves Onsoo $4.73 a unit after ads; retail leaves $7.55, but only once Onsoo has funded $7.5M a year of retail marketing and field sales",
          "Table 4 (per-unit inputs, Rice Ferment Barrier Cream); Tables 5–6. ACoS = Amazon ad spend as a share of Amazon sales. Duty = 15% of $3.50 ex-factory cost.")
text(s, L, 1.62, 6.0, 0.3, "Amazon, per unit at the planning team's 25% ACoS", size=11, bold=True, color=INK)
waterfall(s, L, 2.0, 6.0, 3.5, [("Consumer price", 24.0, "start"), ("Referral fee 15%", 3.60, "neg"), ("FBA fee", 5.10, "neg"),
                                ("Product", 3.50, "neg"), ("Freight", 0.55, "neg"), ("Duty", 0.525, "neg"),
                                ("Ads (25% ACoS)", 6.00, "neg"), ("Contribution", 4.725, "total")], 31, A_COL, cat_size=8)
text(s, 6.85, 1.62, 6.0, 0.3, "Specialty retail, per unit", size=11, bold=True, color=INK)
waterfall(s, 6.85, 2.0, 6.0, 3.5, [("Shelf price", 28.0, "start"), ("Retailer margin 50%", 14.0, "neg"), ("Product", 3.50, "neg"),
                                   ("Freight", 0.75, "neg"), ("Duty", 0.525, "neg"), ("Co-op 8%", 1.12, "neg"),
                                   ("Returns 4%", 0.56, "neg"), ("Contribution", 7.545, "total")], 31, B_COL, cat_size=8)
text(s, L, 5.65, 6.0, 1.25,
     [dict(t="Every +1 pt of ACoS costs $0.24 a unit: **$4.01 at the pilot's 28%, $3.05 at the 32% benchmark**", bullet=True),
      dict(t="A 25% tariff adds $0.35 a unit of duty in both channels; a 10% weaker won saves about $0.37", bullet=True)],
     size=10.5, space_after=4)
text(s, 6.85, 5.65, 6.0, 1.25,
     [dict(t="600 doors × 4.5 units/week × 52 = 140k units, which earn **$1.06M** of contribution a year", bullet=True),
      dict(t="Retail-specific fixed costs are **$7.5M a year** ($6.0M marketing and sampling, $1.5M field sales). At 4.6 units/door/week, breakeven needs ~4,200 doors", bullet=True)],
     size=10.5, space_after=4)

# =====================================================================
# 8. Cumulative cash
s = slide("2 · Which route", "Option A's cumulative cash bottoms out at –$1.9M (–$3.2M at benchmark ad costs); Option B breaches the $18M cap in 2029 on its own inputs",
          "Team model from Tables 4–7. Cash = contribution – fixed and one-time costs – inventory build (4 months of landed cost). No tax. Appendix A3–A5.")
text(s, L, 1.62, 8.5, 0.3, "Cumulative US (or Japan) cash flow, $M", size=11, bold=True, color=INK)
cats = ["2027", "2028", "2029", "2030"]
cA = [mm(r["cum"]) for r in A["rows"]]; cA32 = [mm(r["cum"]) for r in A32["rows"]]
cB = [mm(r["cum"]) for r in B["rows"]]; cJ = [mm(r["cum"]) for r in J["rows"]]
ax, xs = line_chart(s, L, 2.0, 8.6, 4.85, cats,
                    [dict(values=cB, color=B_COL, end_label="B · retail-led (plan): –20.8", point_labels=[fm(v) for v in cB], label_offset=0.06),
                     dict(values=cA32, color=A_COL, dash=True, end_label="A at 32% ACoS: –2.3", end_dy=0.18),
                     dict(values=cA, color=A_COL, end_label="A · Amazon-led (plan): +2.4", end_dy=-0.16),
                     dict(values=cJ, color=J_COL, end_label="J · Japan: +1.8", end_dy=0.17)],
                    -24, 4, [-24, -20, -16, -12, -8, -4, 0, 4], lambda t: f"{t:.0f}", end_label_w=2.1)
cap = ax(-18)
line(s, L + 0.55, cap, L + 8.6 - 2.1, cap, color=CRIT, width=1.5, dash=True)
text(s, L + 0.6, cap - 0.27, 3.5, 0.25, "Board cap: –$18M peak cumulative cash", size=9.5, bold=True, color=CRIT)
px = 9.45
text(s, px, 1.7, 3.4, 5.2,
     [dict(t="Why B burns cash", bold=True, color=NAVY, size=12),
      dict(t="Fixed costs of $9.6M a year against $2.9–8.5M of contribution: B loses money every year, even with the 1.3× halo and 4.5 units/door/week", bullet=True),
      dict(t="One-time costs of $2.0M in 2027 (setup, launch fee, 600 sets of fixtures)", bullet=True),
      dict(t="Why A stays shallow", bold=True, color=NAVY, size=12),
      dict(t="Fixed costs of $2.1M a year, covered from 2028 at plan; inventory adds $0.4–0.5M a year", bullet=True),
      dict(t="Even at 32% ACoS the trough is –$3.2M, under a fifth of the cap; but cumulative cash is still negative at end-2030", bullet=True)],
     size=10.5, space_after=6)

# =====================================================================
# 9. Scorecard
s = slide("2 · Which route", "Option B fails all four financial tests on its own inputs; Option A passes the cash and margin tests, and whether it pays back depends on ad cost",
          "Board objectives (§3); team model (appendix A3–A5). Group margin = (ex-US plan at 11.0% + US operating result) ÷ (ex-US + US revenue); one-time costs expensed.")
cols = [3.1, 1.7, 1.95, 1.95, 1.95, 1.68]
hx = L
hdrs = ["Board test", "Limit", "A · Amazon-led\n(plan, 25% ACoS)", "A · Amazon-led\n(32% benchmark)", "B · Retail-led\n(plan)", "J · Japan\nscale-up"]
yy = 1.75
rect(s, L, yy, sum(cols), 0.62, fill=NAVY)
cx = L
for c, t in zip(cols, hdrs):
    text(s, cx + 0.06, yy, c - 0.1, 0.62, t, size=10, bold=True, color=WHITE, anchor="m", align="l" if cx == L else "c", line_spacing=0.95)
    cx += c
yy += 0.62
sc = [
    ("Ambition: US revenue in 2030", "$40M", [("bad", "$26.4M"), ("bad", "$26.4M"), ("bad", "$37.6M"), ("bad", "No US")]),
    ("Investment cap: peak cumulative cash", "≤ $18M", [("good", "$1.9M"), ("good", "$3.2M"), ("bad", "$20.8M"), ("good", "$1.1M")]),
    ("Payback: cumulative cash ≥ 0", "by end-2030", [("good", "2030"), ("bad", "~2032"), ("bad", "Never by 2030"), ("good", "2029")]),
    ("Group operating margin, lowest year", "≥ 8% every year", [("good", "9.5%"), ("good", "9.1%"), ("bad", "4.5% (2027)"), ("good", "10.1%")]),
    ("Bandwidth: one major launch in 2027", "one", [("good", "One"), ("good", "One"), ("part", "One, two channels"), ("good", "One")]),
]
for test, lim, vals in sc:
    text(s, L + 0.06, yy, cols[0] - 0.1, 0.62, test, size=11, bold=True, color=NAVY, anchor="m")
    text(s, L + cols[0], yy, cols[1], 0.62, lim, size=10.5, color=INK, anchor="m", align="c")
    cx = L + cols[0] + cols[1]
    for (k, lab), c in zip(vals, cols[2:]):
        pill(s, cx + 0.1, yy + 0.13, c - 0.2, 0.36, k, lab, size=9.5)
        cx += c
    yy += 0.66
    line(s, L, yy - 0.02, L + sum(cols), yy - 0.02, color=GRID)
takeaway(s, 5.95, "**Implication:** retail-led is ruled out by the board's own limits before its assumptions are even challenged. Amazon-led is the only US route left; the open question is when it pays back, not whether the board can afford it.", h=0.8, size=11.5)

# =====================================================================
# 10. Sell-through
s = slide("2 · Which route", "Option B assumes the sell-through of brands with >20% awareness; at Onsoo's 4%, the median brand falls below the 4.0 removal line",
          "Table 8 (retail analytics firm, 2025, 46 newcomer brands; leading retailer removes brands below 4.0 units/door/week at the 12-month review); §10 survey (Sep 2026, n=1,200); Table 5.")
text(s, L, 1.62, 7.4, 0.3, "First-year sell-through by aided awareness among category buyers, units per door per week", size=11, bold=True, color=INK)
cats = ["Below 10%\n(Onsoo: 4%)", "10–20%\n(CEO trigger: 15%)", "Above 20%"]
med = [2.6, 3.5, 4.6]; lo = [1.9, 2.8, 3.9]; hi = [3.4, 4.3, 5.5]
cols_ = [CRIT, WARN, GOOD]
ax, px0, pw, slot = bar_chart(s, L, 2.05, 7.4, 4.6, cats, [dict(name="m", values=med, color="8FA8C8", colors=["8FA8C8"] * 3, labels=False)],
                              0, 6, [0, 1, 2, 3, 4, 5, 6], lambda t: f"{t:.0f}", gap=0.5, cat_size=9.5, cat_h=0.5)
for i in range(3):
    cx = px0 + slot * (i + 0.5)
    line(s, cx, ax(hi[i]), cx, ax(lo[i]), color=NAVY, width=1.5)
    line(s, cx - 0.12, ax(hi[i]), cx + 0.12, ax(hi[i]), color=NAVY, width=1.5)
    line(s, cx - 0.12, ax(lo[i]), cx + 0.12, ax(lo[i]), color=NAVY, width=1.5)
    text(s, cx + 0.16, ax(med[i]) - 0.13, 1.25, 0.26, f"median {med[i]}", size=9.5, bold=True, color=INK)
    text(s, cx + 0.16, ax(hi[i]) - 0.12, 1.2, 0.24, f"IQR top {hi[i]}", size=8.5, color=INK2)
yl = ax(4.0)
line(s, px0, yl, px0 + pw, yl, color=CRIT, width=1.5, dash=True)
text(s, px0 + 0.05, yl + 0.03, 3.6, 0.25, "4.0: removal line at the 12-month review", size=9.5, bold=True, color=CRIT)
ya = ax(4.5)
line(s, px0, ya, px0 + pw, ya, color=B_COL, width=1.5)
text(s, px0 + 0.05, ya - 0.27, 3.6, 0.25, "4.5: Option B assumption", size=9.5, bold=True, color=B_COL)
px = 8.4
text(s, px, 1.7, 4.45, 5.2,
     [dict(t="Onsoo sits in the lowest tier", bold=True, color=NAVY, size=12),
      dict(t="Aided awareness is 4% of US skincare buyers (9% among K-beauty buyers). Both are below 10%", bullet=True),
      dict(t="At the tier median of 2.6, 600 doors sell ~81k units a year, not 140k. Even the top quartile (3.4) is below 4.0, so the most likely result is removal after 12 months", bullet=True),
      dict(t="The 4.5 is optimistic by construction", bold=True, color=NAVY, size=12),
      dict(t="It comes from the retailer's own deck on successful newcomers, a survivor sample, and matches the >20% tier. The independent analytics data covers 46 brands", bullet=True),
      dict(t="Clearing 4.0 with confidence needs >20% awareness: that tier's lower quartile is 3.9", bullet=True)],
     size=10.5, space_after=5)

# =====================================================================
# 11. Halo
s = slide("2 · Which route", "The 1.3× retail halo is unproven: the 0.71 correlation fits Amazon success leading to retail doors just as well as the reverse",
          "§12 (board member memo, 30 brands); Table 9 (recent K-beauty US entrants); §10 survey; Table 4; team analysis.")
colx = [L, L + 4.18, L + 8.36]
heads = ["Correlation is not causation", "The entry record favours Amazon-first", "US K-beauty buyers shop and discover away from the shelf"]
bodies = [
    [dict(t="Retailers add doors for brands that already sell. Higher Amazon sales and more doors move together whichever causes which", bullet=True),
     dict(t="**Saebom** shows the order: Amazon-first in 2022, about $30M US revenue by 2025, and only then 300 retail doors", bullet=True),
     dict(t="The memo gives no before/after or test-vs-control evidence, so 1.3× is an assumption, not a measurement", bullet=True)],
    [dict(t="**Mooncrest**, retail-first in 450 doors (2023): removed from shelves in 2025, with an estimated cumulative US loss of **$21M**", bullet=True),
     dict(t="**Amazon-first:** one of three entrants reached about $30M; two are below $5M. Amazon-first is not safe either, which is why section 4 adds stop gates", bullet=True)],
    [dict(t="**61%** of K-beauty buyers buy K-beauty on Amazon most often; **22%** at specialty retail", bullet=True),
     dict(t="**38%** found their last new brand on TikTok; **17%** in a store", bullet=True),
     dict(t="**52%** cite price compared with US brands. The $28 retail shelf price is 17% above Amazon's $24", bullet=True)],
]
for i in range(3):
    rect(s, colx[i], 1.75, 3.98, 0.06, fill=NAVY)
    text(s, colx[i], 1.88, 3.98, 0.62, heads[i], size=12.5, bold=True, color=NAVY)
    text(s, colx[i], 2.55, 3.98, 2.2, bodies[i], size=11, space_after=7)
rect(s, L, 4.85, CW, 1.0, fill=PANEL)
rect(s, L, 4.85, 0.07, 1.0, fill=B_COL)
text(s, L + 0.25, 4.88, CW - 0.4, 0.95,
     ["**What the halo would have to be for retail to pay for itself:** 600 doors at 4.6 units/week earn $1.08M against $7.5M of retail fixed costs. Covering the $6.4M gap at $4.73 a unit takes 1.36M extra Amazon units a year.",
      "That means Amazon sales **2.2–2.6× Option A's** (2030 / 2029), not 1.3×. The halo would need to be several times larger than even the unproven figure."],
     size=10.5, space_after=3)
takeaway(s, 6.05, "**Implication:** the case for retail-first rests on a sell-through rate and a halo that the evidence does not support. Amazon first, with retail earned later, is the sequence the evidence backs.", h=0.75, size=11.5)

# =====================================================================
# 12. B realism
s = slide("2 · Which route", "With evidence-based inputs, Option B's cumulative US loss reaches $31M by 2030, half as much again as Mooncrest's $21M",
          "Team model; each bar adds one change to the one before. Inputs: Table 8 (2.6 units/door/week), Table 5 (Option A volumes), agency ACoS benchmark (§11). Appendix A4.")
ladder = M["out"]["B_ladder"]
vals = [v["cum"] for v in ladder.values()]
labs = ["Planning case\n(4.5/door/wk, 1.3× halo,\n25% ACoS)", "Sell-through at\nOnsoo's awareness\n(2.6/door/wk)", "+ No proven halo\n(Amazon units =\nOption A)", "+ ACoS at 32%\nscaling benchmark"]
text(s, L, 1.62, 7.6, 0.3, "Option B cumulative US cash flow to end-2030, $M", size=11, bold=True, color=INK)
ax, px0, pw, slot = bar_chart(s, L, 2.0, 6.9, 4.85, labs, [dict(name="b", values=vals, color=B_COL)],
                              -35, 0, [-35, -30, -25, -20, -15, -10, -5, 0], lambda t: f"{t:.0f}", label_fmt=lambda v: fm(v), gap=0.4, cat_h=0.62, cat_size=8.5)
for val, lab, col in [(-18, "Board cap –18", CRIT), (-21, "Mooncrest –21", INK2)]:
    yv = ax(val)
    line(s, px0, yv, px0 + pw, yv, color=col, width=1.25, dash=True)
    text(s, px0 + pw + 0.05, yv - 0.11, 1.3, 0.22, lab.replace("-", "–"), size=8.5, bold=True, color=col)
px = 8.85
b_real = run(A_UNITS, DOORS, upw=2.6, acos=0.32)
text(s, px, 1.7, 4.0, 5.2,
     [dict(t="Reading the ladder", bold=True, color=NAVY, size=12),
      dict(t="Each step swaps one planning assumption for what the evidence supports. None of the steps is a worst case", bullet=True),
      dict(t=f"With all three changes, group margin falls to **{b_real['min_margin']*100:.1f}%** in 2027 against the 8% floor", bullet=True),
      dict(t="What would really happen", bold=True, color=NAVY, size=12),
      dict(t=f"At 2.6 units/door/week the retailer would remove Onsoo after 12 months. The first year alone costs **${-mm(b_real['rows'][0]['cf']):.1f}M**, leaving no retail presence and a weaker brand story. This is the Mooncrest pattern", bullet=True)],
     size=10.5, space_after=6)

# =====================================================================
# 13. ACoS sensitivity
s = slide("3 · What A will deliver", "Ad cost decides payback: Option A recovers its cash by 2030 only if ACoS stays at or below 28.6%, roughly the pilot's level",
          "Team model (Option A volumes and costs per Tables 4–6); pilot ACoS (§6); agency benchmark (§11); tariff review (§13).")
sens = M["out"]["A_sens"]
ac = ["0.25", "0.28", "0.30", "0.32", "0.35", "0.38"]
v15 = [sens[f"{a}|0.15|1.00"]["cum"] for a in ac]
v25 = [sens[f"{a}|0.25|1.00"]["cum"] for a in ac]
text(s, L, 1.62, 7.7, 0.3, "Option A cumulative cash at end-2030 by ACoS, $M", size=11, bold=True, color=INK)
legend(s, L, 1.92, [("Duty 15% (today)", A_COL), ("Duty 25% (under review)", A_LIGHT)])
ax, px0, pw, slot = bar_chart(s, L, 2.35, 7.7, 4.0, ["25%\nplan", "28%\npilot", "30%", "32%\nbenchmark", "35%", "38%\nbenchmark high"],
                              [dict(name="15", values=v15, color=A_COL), dict(name="25", values=v25, color=A_LIGHT)],
                              -8, 4, [-8, -6, -4, -2, 0, 2, 4], lambda t: f"{t:.0f}", label_fmt=lambda v: fm(v, plus=True), gap=0.28,
                              cat_size=9, label_size=8.5, cat_h=0.45)
be = M["out"]["be_acos"]
px = 8.65
text(s, px, 1.7, 4.2, 5.2,
     [dict(t="Breakeven ACoS for payback by 2030", bold=True, color=NAVY, size=12),
      dict(t=f"**{be['base']*100:.1f}%** at today's duty; **{be['t25']*100:.1f}%** if the duty rises to 25% in mid-2027", bullet=True),
      dict(t="Each +1 pt of ACoS costs **$0.67M** of cumulative cash by 2030", bullet=True),
      dict(t="The 25% plan figure runs against the evidence", bold=True, color=NAVY, size=12),
      dict(t="The planning team assumes ACoS falls as the brand matures. The agency data says the opposite: brands scaling from $5M to $20M on Amazon run a median **32%** (range 26–38%), because cost per click rises on broader keywords", bullet=True),
      dict(t="Option A scales from $7M to $26M, squarely in that range. The pilot's 28% was on a small budget", bullet=True)],
     size=10.5, space_after=6)

# =====================================================================
# 14. Scenarios
s = slide("3 · What A will deliver", "Even in a severe downside, Option A's peak cash need stays below $8M and group margin above 8%: the risk is to payback timing, not the balance sheet",
          "Team model. *Payback after 2030 extrapolates Option A at 10–20% annual unit growth after 2030 (team assumption; not in the briefing pack).")
rows_ = [["Scenario", "ACoS", "Duty", "Volume", "Peak cumulative cash", "Cumulative cash 2030", "Payback year", "Lowest group margin", "2030 revenue"]]
scen = [("Planning case", "0.25", "0.15", "1.00", "25%", "15%", "Plan", "2030"),
        ("Pilot ad cost", "0.28", "0.15", "1.00", "28%", "15%", "Plan", "2030"),
        ("Benchmark ad cost", "0.32", "0.15", "1.00", "32%", "15%", "Plan", "~2032*"),
        ("Downside", "0.32", "0.25", "0.75", "32%", "25%", "–25%", "~2035*"),
        ("Severe downside", "0.38", "0.25", "0.75", "38%", "25%", "–25%", "Never")]
for nm, a_, d_, v_, al, dl, vl, pb in scen:
    r = sens[f"{a_}|{d_}|{v_}"]
    rows_.append([nm, al, dl, vl, fm(r["peak"], pre="$", suf="M"), fm(r["cum"], plus=True, pre="$", suf="M"), pb, f"{r['minmargin']:.1f}%", f"${r['rev2030']:.1f}M"])
fills = {}
for ri in range(1, 6):
    fills[(ri, 4)] = GOOD_T
    fills[(ri, 7)] = GOOD_T
    fills[(ri, 6)] = GOOD_T if ri <= 2 else (WARN_T if ri <= 4 else CRIT_T)
table(s, L, 1.75, [2.3, 0.85, 0.85, 0.95, 1.6, 1.6, 1.35, 1.55, 1.28], rows_, rowh=0.5, size=10.5,
      aligns=["l", "c", "c", "c", "c", "c", "c", "c", "c"], fills=fills, row_heights=[0.62] + [0.5] * 5)
text(s, L, 5.0, CW, 0.3, "What this means for the board", size=12, bold=True, color=NAVY)
text(s, L, 5.35, CW / 2 - 0.2, 1.5,
     [dict(t="**Affordability is not the issue.** Peak cash is 11–44% of the $18M cap and group margin stays at 8.8% or more in every case", bullet=True),
      dict(t="**Payback is the issue.** It holds only in the two cases where ACoS is at or below the pilot's level", bullet=True)],
     size=10.5, space_after=6)
text(s, L + CW / 2, 5.35, CW / 2, 1.5,
     [dict(t="**The severe case must be stopped, not funded.** At 38% ACoS and 25% duty each unit earns $1.26, so 825k units in 2030 cannot cover $2.1M of fixed costs. Hence the stop rules in section 4", bullet=True),
      dict(t="Upside not modelled: a weaker won (10% ≈ +$0.37 a unit, ≈ +$1.0M to 2030)", bullet=True)],
     size=10.5, space_after=6)

# =====================================================================
# 15. Revenue path
s = slide("3 · What A will deliver", "No route reaches $40M of US revenue in 2030 within the limits; on the Amazon path, $40M comes around 2032 if growth holds at 20% a year",
          "Tables 4–5; team model. 2031–33 values are team extrapolations of Option A at 10% and 20% annual unit growth (not in the briefing pack).")
text(s, L, 1.62, 8.3, 0.3, "US revenue, $M", size=11, bold=True, color=INK)
cats = [str(y) for y in range(2027, 2034)]
aR = [7.2, 13.44, 20.4, 26.4]
e20 = [None, None, None, 26.4, 31.68, 38.02, 45.62]
e10 = [None, None, None, 26.4, 29.04, 31.94, 35.14]
bR = [mm(r["revenue"]) for r in B["rows"]]
ax, xs = line_chart(s, L, 2.0, 8.6, 4.85, cats,
                    [dict(values=e10, color=A_LIGHT, dash=True, end_label="A, +10%/yr after 2030", end_dy=0.1, markers=False),
                     dict(values=e20, color=A_COL, dash=True, end_label="A, +20%/yr after 2030", end_dy=-0.05, markers=False),
                     dict(values=aR + [None] * 3, color=A_COL, point_labels=[f"{v:.1f}" for v in aR] + [None] * 3, label_offset=0.08),
                     dict(values=bR + [None] * 3, color=B_COL, point_labels=[f"{v:.1f}" for v in bR] + [None] * 3, label_offsets=[-0.32, -0.32, -0.32, -0.1], label_dx=[0, 0, 0, 0.42])],
                    0, 50, [0, 10, 20, 30, 40, 50], lambda t: f"{t:.0f}", end_label_w=1.9)
y40 = ax(40)
line(s, L + 0.55, y40, L + 8.6 - 1.9, y40, color=NAVY, width=1.25, dash=True)
text(s, L + 0.6, y40 - 0.27, 2.6, 0.25, "Board ambition: $40M", size=9.5, bold=True, color=NAVY)
legend(s, L + 2.2, 1.64, [("A · Amazon-led (plan)", A_COL), ("B · Retail-led (plan)", B_COL)])
px = 9.45
text(s, px, 1.7, 3.4, 5.2,
     [dict(t="The gap is in the plans themselves", bold=True, color=NAVY, size=12),
      dict(t="Option A plan: **$26.4M** in 2030 (1.1M units × $24)", bullet=True),
      dict(t="Option B plan: **$37.6M**, and $40.9M only if retail is counted at shelf price rather than Onsoo's wholesale price. It gets there by breaking the cash cap", bullet=True),
      dict(t="Recommended restatement", bold=True, color=NAVY, size=12),
      dict(t="**$25M+ US revenue in 2030, $40M by ~2032**, both conditional on hitting the 2028 gate. This keeps “on the way to $40M” honest", bullet=True),
      dict(t="Precedent: Saebom reached ~$30M about three years after an Amazon-first entry", bullet=True)],
     size=10.5, space_after=6)

# =====================================================================
# 16. Retail gates
s = slide("4 · How to sequence", "Retail should wait for ≥20% awareness and a measured halo: the CEO's 15% trigger falls in the tier whose median sits below the 4.0 removal line",
          "Table 8; §10 survey; Tables 4–6; team model of the CEO plan (Option A, plus 600 doors from 2029 at 4.6 units/door/week, 1.3× Amazon halo, $7.5M a year of retail fixed costs).")
rows_ = [["Gate", "CEO proposal", "Recommended gate", "Why"],
         ["Awareness", ">15% aided awareness (base not specified)", "**≥20%** aided awareness among all US facial-skincare buyers, the base Table 8 uses", "At 10–20% the median is 3.5 units/door/week (IQR 2.8–4.3), below 4.0. The >20% tier's median is 4.6"],
         ["Amazon base", ">$10M Amazon sales", ">$10M **and** ACoS ≤30% **and** cumulative US cash on track to turn positive", "Retail's $7.5M a year has to be carried by a profitable Amazon business"],
         ["Halo proof", "None (assumed 1.3×)", "**Regional door test**: measure Amazon uplift in test regions against control regions", "Retail pays for itself only with a 2.2–2.6× halo; the 0.71 correlation shows neither the size nor the direction"],
         ["Timing & scale", "National launch from 2029", "**Not before 2030**; a test-sized programme first, then a separate board investment case", "A 2029 national add breaks the 2029 margin floor and the 2030 payback (right)"]]
table(s, L, 1.72, [1.3, 2.05, 3.0, 2.95], rows_, rowh=0.86, size=10, aligns=["l", "l", "l", "l"],
      row_heights=[0.38, 0.86, 0.78, 0.86, 0.86])
rect(s, L, 5.75, 9.3, 1.05, fill=PANEL); rect(s, L, 5.75, 0.07, 1.05, fill=NAVY)
text(s, L + 0.2, 5.75, 9.0, 1.05, "**Implication:** treat specialty retail as an awareness investment that Amazon performance has to earn, not as a 2029 calendar commitment. The gates make the decision depend on evidence the board can see.", size=11.5, anchor="m")
cv = M["out"]["ceo_variant"]
px = 10.0
rect(s, px, 1.72, 2.83, 5.1, fill=PANEL)
text(s, px + 0.15, 1.8, 2.6, 0.55, "CEO plan as written: Option A + 600 doors in 2029", size=11.5, bold=True, color=NAVY)
tiles = [("–$9.6M", "cumulative US cash at end-2030, against +$2.4M for Amazon-only, even granting 4.6 units/door/week and the 1.3× halo"),
         ("6.8%", "group operating margin in 2029, below the 8% floor"),
         ("$1,805", "yearly contribution per door at 4.6 units/week, against $12,500 per door of retail fixed costs")]
for i, (b, t) in enumerate(tiles):
    yy = 2.45 + i * 1.45
    text(s, px + 0.15, yy, 2.6, 0.48, b, size=22, bold=True, color=CRIT if i < 2 else NAVY)
    text(s, px + 0.15, yy + 0.48, 2.6, 0.95, t, size=9.5, color=INK)

# =====================================================================
# 17. Roadmap
s = slide("4 · How to sequence", "A stage-gated 2027–30 plan lets the board stop with about $2.5M at risk if the early signals disappoint",
          "Team recommendation. Gate thresholds are set from the pilot (§6), the agency ACoS benchmark (§11), the repeat benchmark (§6) and Table 8. Cash at risk = cumulative cash at end-2027 (–$1.9M at plan, –$2.4M at 32% ACoS).")
phases = [("2027 · Launch", "Q1–Q4 2027", A_COL,
           ["Set up the US entity; MoCRA registration; US-English labels", "Take over the Amazon listings from the cross-border seller", "Launch four more SKUs (seven in total)", "$0.7M off-Amazon marketing, TikTok first (38% discover there)"]),
          ("2028 · Prove", "Gate 1: Q1 2028", A_COL,
           ["Pass: 2027 units ≥250k · ACoS ≤30% · 90-day repeat ≥31% · rating ≥4.5", "Miss two or more: cut to a hold mode with low fixed cost; ~$2.0–2.5M spent", "Review the Japan scale-up for 2028"]),
          ("2029 · Scale", "Gate 2: Q1 2029", A_COL,
           ["Pass: 2028 revenue ≥$12M · ACoS ≤29% · cumulative cash ≥ –$3M", "Re-run the awareness survey on the Table 8 base", "If awareness ≥15%, design a regional retail test"]),
          ("2030+ · Extend", "Retail gate: 2030", B_COL,
           ["Aided awareness ≥20% and a measured halo from the test", "National retail only through a separate board investment case", "Target: US revenue $25M+ in 2030, $40M by ~2032"])]
pw_ = CW / 4
for i, (t, g, col, items) in enumerate(phases):
    x0 = L + i * pw_
    chev = s.shapes.add_shape(MSO_SHAPE.CHEVRON if i else MSO_SHAPE.PENTAGON, Inches(x0), Inches(1.75), Inches(pw_ + 0.1), Inches(0.62))
    chev.fill.solid(); chev.fill.fore_color.rgb = rgb(NAVY if i < 3 else "3C4A66"); chev.line.fill.background(); chev.shadow.inherit = False
    text(s, x0 + 0.3, 1.75, pw_ - 0.4, 0.62, t, size=12.5, bold=True, color=WHITE, anchor="m")
    text(s, x0 + 0.1, 2.5, pw_ - 0.2, 0.3, g, size=10.5, bold=True, color=col)
    text(s, x0 + 0.1, 2.85, pw_ - 0.25, 2.6, [dict(t=it, bullet=True) for it in items], size=10, space_after=5)
rect(s, L, 5.0, CW, 1.3, fill=PANEL)
text(s, L + 0.2, 5.05, 3.0, 0.3, "Standing watch-items", size=11, bold=True, color=NAVY)
text(s, L + 0.2, 5.37, CW / 2 - 0.3, 0.95,
     [dict(t="**Tariff decision (mid-2027):** at 25% duty, breakeven ACoS falls to 26.9%; re-plan price and cost if it passes", bullet=True),
      dict(t="**ACoS** is tracked monthly against the 28.6% breakeven, not the 25% plan", bullet=True)], size=10, space_after=3)
text(s, L + CW / 2, 5.37, CW / 2 - 0.2, 0.95,
     [dict(t="**Repeat purchase** by SKU count, to test whether a wider range lifts repeat towards Korea's 48%", bullet=True),
      dict(t="**FX:** a weaker won is an upside (10% ≈ +$0.37 a unit); do not plan on it", bullet=True)], size=10, space_after=3)

# =====================================================================
# 18. Decisions
s = slide("Decisions", "We ask the board to approve four decisions in March 2027",
          "Team recommendation based on the analysis in this document.")
dec = [("Approve US entry in 2027 through the Amazon-led route (Option A)",
        "With a US peak-cash envelope of $5M, covering the downside case (–$4.9M) and well inside the $18M cap. Any request beyond $5M comes back to the board."),
       ("Restate the US targets to match the evidence",
        "US revenue of $25M+ in 2030 and $40M by ~2032. Payback by end-2030 if ACoS ≤28.6%; the board accepts slippage to no later than 2032 provided peak cash stays inside the envelope."),
       ("Reject the retail-first route (Option B) and replace the 2029 retail trigger",
        "Specialty retail only with ≥20% aided awareness among all skincare buyers, a measured halo from a regional test and a separate investment case, and not before 2030."),
       ("Keep Japan as the next launch, not the alternative",
        "Ask the Head of Japan to bring the Japan scale-up (+$7M revenue by 2030, +$1.8M cumulative cash) to the 2028 plan, subject to US Gate 1.")]
for i, (a, b) in enumerate(dec):
    yy = 1.8 + i * 1.22
    number_badge(s, L, yy + 0.05, 0.45, i + 1)
    text(s, L + 0.65, yy, 11.5, 0.4, a, size=14, bold=True, color=NAVY)
    text(s, L + 0.65, yy + 0.42, 11.5, 0.7, b, size=11, color=INK)
    if i < 3:
        line(s, L + 0.65, yy + 1.1, W - R, yy + 1.1, color=GRID)

# =====================================================================
# Appendix divider-ish
# A1 assumptions / choices
s = slide("Appendix A1", "Choices we made where the briefing pack was silent or ambiguous",
          "Team notes. Questions could not be put to the planning team during the work, so each choice above is the option we recommend. They are listed so the board can challenge them.")
ch = [("“On the way to $40M revenue by 2030”", "Read as $40M of US revenue in calendar 2030, the stricter reading. Under a looser reading (“on a path to $40M”), Option A's 2032 trajectory could qualify."),
      ("Revenue recognition", "Amazon revenue at the $24 consumer price (Onsoo sells directly via FBA); retail revenue at the $14 wholesale price Onsoo receives."),
      ("Cash flow definition", "Contribution – annual fixed costs – one-time costs – increase in inventory. Inventory = 4 months of landed cost (ex-factory + freight + duty) of each year's units, not released by 2030. No tax, interest or FX change."),
      ("Group margin test", "(Ex-US plan revenue × 11.0% + US operating result) ÷ (ex-US + US revenue). One-time costs and fixtures expensed (conservative); inventory excluded from the P&L."),
      ("Retail timing", "As in the planning team's forecast, doors are counted as selling for the full year from 2027; new doors in 2029–30 carry $1,100 of fixtures each."),
      ("Option J", "No working-capital data was provided, so none is modelled. J figures are incremental to the existing Japan business."),
      ("Bandwidth limit", "Read as applying to 2027 launches only, so a Japan scale-up can be considered for 2028."),
      ("After 2030", "Extrapolations at 10% and 20% annual unit growth are team assumptions, used only for payback year and $40M timing."),
      ("Hero-product economics", "Applied to all SKUs, following the planning team. Real SKU-mix margins may differ (the hero is 31% of group revenue).")]
yy = 1.7
for a, b in ch:
    text(s, L, yy, 3.4, 0.55, a, size=10.5, bold=True, color=NAVY, anchor="m")
    text(s, L + 3.5, yy, CW - 3.5, 0.55, b, size=10, color=INK, anchor="m")
    yy += 0.575
    line(s, L, yy - 0.02, W - R, yy - 0.02, color=GRID)

# A2 unit economics
s = slide("Appendix A2", "Unit economics: how the per-unit contribution figures are built",
          "Table 4. Duty = 15% (or 25%) × $3.50 ex-factory. Co-op and returns are % of the $14 wholesale price. Landed cost = ex-factory + freight + duty.")
rows_ = [["$ per unit", "Amazon 25% ACoS", "Amazon 28%", "Amazon 32%", "Amazon 32%, 25% duty", "Specialty retail", "Retail, 25% duty"],
         ["Price Onsoo receives", "24.00", "24.00", "24.00", "24.00", "14.00", "14.00"],
         ["Referral fee (15%)", "–3.60", "–3.60", "–3.60", "–3.60", "—", "—"],
         ["FBA fulfilment fee", "–5.10", "–5.10", "–5.10", "–5.10", "—", "—"],
         ["Ex-factory product cost", "–3.50", "–3.50", "–3.50", "–3.50", "–3.50", "–3.50"],
         ["Freight", "–0.55", "–0.55", "–0.55", "–0.55", "–0.75", "–0.75"],
         ["Import duty", "–0.53", "–0.53", "–0.53", "–0.88", "–0.53", "–0.88"],
         ["Advertising (ACoS × $24)", "–6.00", "–6.72", "–7.68", "–7.68", "in fixed budget", "in fixed budget"],
         ["Co-op allowance (8%)", "—", "—", "—", "—", "–1.12", "–1.12"],
         ["Returns & damages (4%)", "—", "—", "—", "—", "–0.56", "–0.56"],
         ["**Contribution per unit**", "**4.73**", "**4.01**", "**3.05**", "**2.70**", "**7.55**", "**7.20**"],
         ["Contribution margin", "19.7%", "16.7%", "12.7%", "11.2%", "53.9%", "51.4%"],
         ["Landed cost (for inventory)", "4.58", "4.58", "4.58", "4.93", "4.78", "5.13"]]
table(s, L, 1.72, [3.0, 1.55, 1.4, 1.4, 1.85, 1.6, 1.53], rows_, rowh=0.38, size=10.5, aligns=["l"] + ["c"] * 6,
      highlight_rows={10: GOOD_T})
text(s, L, 6.7, CW, 0.3, "Retail per door per year at 4.6 units/week: 4.6 × 52 × $7.545 = $1,805. Retail fixed costs of $7.5M ÷ $1,805 ≈ 4,156 doors to break even on direct contribution.", size=10, color=INK2)

# A3 Option A cash flow
KEYS = [("Amazon units (k)", lambda r: f"{r['amz_units']/1000:,.0f}", "Table 5"),
        ("Retail units (k)", lambda r: f"{r['retail_units']/1000:,.0f}", "Doors × units/door/week × 52"),
        ("Revenue", lambda r: fm(mm(r['revenue'])), "Units × $24 (Amazon) + units × $14 (retail)"),
        ("Contribution", lambda r: fm(mm(r['contribution']), 2), "Units × per-unit contribution (A2)"),
        ("Fixed costs", lambda r: fm(-mm(r['fixed']), 2), "Table 6 annual lines"),
        ("One-time costs", lambda r: fm(-mm(r['one_time']), 2), "Setup, launch fee, $1,100 × new doors"),
        ("US operating result", lambda r: fm(mm(r['op']), 2), "Contribution – fixed – one-time"),
        ("Inventory build", lambda r: fm(-mm(r['d_inventory']), 2), "Δ (units ÷ 3 × landed cost)"),
        ("Cash flow", lambda r: fm(mm(r['cf']), 2), "Operating result – inventory build"),
        ("Cumulative cash", lambda r: fm(mm(r['cum']), 2), "Running total; peak = most negative"),
        ("Group operating margin", lambda r: f"{r['group_margin']*100:.1f}%", "See A1")]


def cf_table(s, runs, y, heads, rh=0.36):
    rows_ = [["$M"] + [h_ + " " + str(yv) for h_ in heads for yv in (2027, 2028, 2029, 2030)] + ["How calculated"]]
    for nm, f, how in KEYS:
        if nm == "Retail units (k)" and all(r["retail_units"] == 0 for R_ in runs for r in R_["rows"]):
            continue
        if nm == "One-time costs" and len(runs) > 1:
            pass
        rows_.append([nm] + [f(r) for R_ in runs for r in R_["rows"]] + [how])
    bold = {i for i, r in enumerate(rows_) if r[0] in ("Cash flow", "Cumulative cash")}
    n = len(runs) * 4
    cw = (CW - 2.2 - 3.0) / n if n > 4 else 1.15
    widths = [2.2] + [cw] * n + [CW - 2.2 - cw * n]
    return table(s, L, y, widths, rows_, rowh=0.36, size=9.5, aligns=["l"] + ["c"] * n + ["l"], bold_rows=bold,
                 row_heights=[0.5] + [rh] * (len(rows_) - 1))

s = slide("Appendix A3", "Option A cash flow: planning case (25% ACoS) and benchmark case (32% ACoS)",
          "Tables 4–6; team model. Fixed = compliance $0.5M + US team $0.9M + off-Amazon marketing $0.7M. One-time = $0.8M setup in 2027. Duty 15% in both cases.")
cf_table(s, [A, A32], 1.75, ["Plan", "32%"])

s = slide("Appendix A4", "Option B cash flow (planning case): it loses money in every year to 2030, before any challenge to its assumptions",
          "Tables 4–6; team model. Fixed = $2.1M shared + $6.0M national retail marketing + $1.5M field sales. One-time 2027 = $0.8M setup + $0.5M launch fee + 600 × $1,100 fixtures.")
text(s, L, 1.62, CW, 0.3, "Planning case: 600 → 1,000 doors at 4.5 units/door/week; Amazon units = Option A × 1.3; ACoS 25%", size=11, bold=True, color=NAVY)
yb = cf_table(s, [B], 1.98, [""], rh=0.32)
text(s, L, yb + 0.15, CW, 0.9,
     [dict(t="Ladder used on slide 12 (cumulative cash, end-2030): planning –$20.8M → 2.6 units/door/week –$22.9M → no halo –$26.4M → ACoS 32% –$31.1M.", bullet=True),
      dict(t="Stress tests on the planning case alone: ACoS 32% → –$26.9M; duty 25% → –$22.5M.", bullet=True)],
     size=10, space_after=3)

s = slide("Appendix A5", "Option J and the group margin test",
          "Table 7; group context (§8); team model. J has no working-capital data, so cash = operating result.")
rows_ = [["$M", "2027", "2028", "2029", "2030", "How calculated"],
         ["Incremental revenue", "2.5", "4.5", "6.0", "7.0", "Table 7"],
         ["Contribution (30%)", "0.75", "1.35", "1.80", "2.10", "Revenue × 30%"],
         ["Added fixed cost", "–0.80", "–0.80", "–0.80", "–0.80", "Table 7"],
         ["One-time cost", "–1.00", "—", "—", "—", "Table 7"],
         ["Operating result = cash", "–1.05", "0.55", "1.00", "1.30", ""],
         ["**Cumulative cash**", "**–1.05**", "**–0.50**", "**0.50**", "**1.80**", "Payback in 2029"]]
table(s, L, 1.72, [2.6, 1.15, 1.15, 1.15, 1.15, 5.13], rows_, rowh=0.34, size=10, aligns=["l", "c", "c", "c", "c", "l"])
text(s, L, 4.25, CW, 0.3, "Group operating margin by option (ex-US plan: revenue $140/146/152/158M at 11.0%)", size=11, bold=True, color=NAVY)
def gm(R_): return [f"{r['group_margin']*100:.1f}%" for r in R_["rows"]]
cvm = ["9.5%", "10.4%", "6.8%", "8.0%"]
rows_ = [["Option", "2027", "2028", "2029", "2030", "Floor ≥8%"],
         ["A · plan (25% ACoS)"] + gm(A) + ["Pass"],
         ["A · 32% ACoS"] + gm(A32) + ["Pass"],
         ["B · plan"] + gm(B) + ["Fails 2027–29"],
         ["CEO plan (A + 600 doors in 2029)"] + cvm + ["Fails 2029"],
         ["J · Japan"] + gm(J) + ["Pass"]]
table(s, L, 4.6, [3.4, 1.1, 1.1, 1.1, 1.1, 2.0], rows_, rowh=0.33, size=10, aligns=["l", "c", "c", "c", "c", "c"],
      fills={(3, 1): CRIT_T, (3, 2): CRIT_T, (3, 3): CRIT_T, (4, 3): CRIT_T})
text(s, 10.5, 4.6, 2.33, 2.0, "Example, B 2027: (140 × 11.0% – 8.66) ÷ (140 + 11.33) = 6.74 ÷ 151.33 = 4.5%", size=9.5, color=INK2, fill=PANEL)

# A6 evidence discounted
s = slide("Appendix A6", "Evidence we discounted or reinterpreted, and why",
          "Briefing pack §5, §8, §9, §11, §12; team analysis.")
ev = [("Trade-press “US K-beauty market $5.2B”", "Includes makeup and hair care. Replaced by Table 1's $3.6B for facial skincare, Onsoo's category.", "Market size overstated by 44%"),
      ("Board memo: retail doors correlate with Amazon sales (r = 0.71)", "Correlation across 30 brands with no direction or control. Saebom shows retail following Amazon success. Not used as evidence of a 1.3× halo.", "Option B's Amazon uplift unproven"),
      ("Retailer deck: 4.5 units/door/week", "A survivor sample of “successful newcomers” from an interested party. The independent analytics data (46 brands) puts Onsoo's awareness tier at 2.6.", "Option B retail volumes ~1.7× too high"),
      ("Planning assumption: ACoS falls to 25%", "Contradicted by the agency benchmark (32% median when scaling $5–20M; CPC rises). The pilot ran at 28% on a small budget.", "Payback at risk; benchmark case shown"),
      ("Pilot repeat rate of 29%", "Treated as on par with the 31% benchmark, not as evidence of US loyalty. The Korean-only label complaint may depress it and is fixable.", "No uplift assumed"),
      ("Planning team's Option A volumes", "Kept as the base, with a –25% volume case because pilot growth slowed (16–17% → 8–9% a month).", "Tested in downside scenarios")]
rows_ = [["Item", "Why we discounted or reinterpreted it", "Effect on the answer"]] + [list(e) for e in ev]
table(s, L, 1.72, [3.5, 6.33, 2.5], rows_, rowh=0.74, size=10, row_heights=[0.38] + [0.76] * 6)

out = os.path.join(os.path.dirname(__file__), "..", "deliverable", "Onsoo_US_entry_board_deck.pptx")
prs.save(out)
print("saved", os.path.abspath(out), N[0], "slides")
