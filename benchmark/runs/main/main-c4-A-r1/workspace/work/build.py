import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import Slide, render_png, render_pptx, W, H
from calc import C

INK, INK2, MUTED, GRID = "#1a1a1a", "#52514e", "#8a8984", "#e3e2de"
BLUE, BLUE_LT, BLUE_DK = "#2a78d6", "#cde2fb", "#184f95"
ORANGE, ORANGE_LT = "#eb6834", "#fbe1d6"
GRAYBAR, PANEL = "#bdbcb7", "#f4f4f2"
GREEN = "#1f7a3a"
L, R = 0.6, W - 0.6
CW = R - L

SRC = "Source: Palisade Docs briefing pack (synthetic data)"


def m(v, d=1):
    return f"${v:.{d}f}M"


def B(t):
    return (t, {"bold": True})


def header(s, tag, title, page):
    s.text(L, 0.28, CW, 0.3, tag.upper(), size=10, color=BLUE_DK, bold=True)
    s.text(L, 0.55, CW, 0.95, title, size=23, bold=True, color=INK, valign="t")
    s.line(L, 1.55, R, 1.55, GRID, 1)
    s.text(R - 0.6, 7.05, 0.6, 0.28, str(page), size=9, color=MUTED, align="r")


def footer(s, note):
    s.text(L, 6.9, CW - 0.8, 0.48, note, size=8.5, color=MUTED, valign="b")


def panel(s, x, y, w, h, fill=PANEL):
    s.rect(x, y, w, h, fill)


def bullets(s, x, y, w, h, items, size=12, after=6, color=INK):
    paras = []
    for it in items:
        runs = it if isinstance(it, list) else [it]
        paras.append(dict(runs=runs, bullet=True, space_after=after))
    s.text(x, y, w, h, paras, size=size, color=color)


def legend(s, x, y, items, size=10):
    cx = x
    for label, col in items:
        s.rect(cx, y + 0.05, 0.16, 0.16, col)
        s.text(cx + 0.2, y - 0.01, 2.6, 0.28, label, size=size, color=INK2)
        cx += 0.32 + len(label) * size * 0.0075
    return cx


def hbars(s, x, y, w, rows, vmax, label_w=2.6, bar_h=0.26, gap=0.2, fmt=lambda v: f"{v:.0f}%", size=11,
          val_w=0.8):
    """rows: (label, value, color, label_bold). Horizontal bars from a single baseline."""
    bx = x + label_w
    bw = w - label_w - val_w
    yy = y
    for lab, v, col, bold in rows:
        s.text(x, yy - 0.06, label_w - 0.1, bar_h + 0.12, lab, size=size, color=INK, bold=bold, align="r", valign="m")
        ln = bw * v / vmax
        s.rect(bx, yy, ln, bar_h, col)
        s.text(bx + ln + 0.05, yy - 0.06, val_w + 0.3, bar_h + 0.12, fmt(v), size=size, bold=True, color=INK, valign="m")
        yy += bar_h + gap
    s.line(bx, y - 0.08, bx, yy - gap + 0.08, INK2, 0.75)
    return yy


# ======================================================================
slides = []

# 1 ---- Title -----------------------------------------------------------
s = Slide(notes="Title. Deck answers the decision question in the briefing pack using only its data. "
                "All estimates are labelled; assumptions are listed in Appendix A1.")
s.rect(0, 0, W, H, "#0f2c4f")
s.rect(L, 2.05, 0.08, 2.0, ORANGE)
s.text(L + 0.3, 1.95, 11.5, 0.45, "PALISADE DOCS  |  2027 PRICING PLAN", size=13, color="#9ec5f4", bold=True)
s.text(L + 0.3, 2.4, 11.8, 1.4, "Raise prices in 2027 where customers stay, hold them where customers are leaving",
       size=34, color="#ffffff", bold=True)
s.text(L + 0.3, 3.85, 11.5, 0.5, "Recommendation for Ravi Menon and the leadership team  |  Decision meeting, December 2026",
       size=15, color="#dfe9f6")
s.text(L + 0.3, 6.45, 12, 0.6,
       ["Prepared only from the Palisade briefing pack. Its company, competitor and figures are synthetic benchmark data.",
        "Figures marked “est.” are our calculations; the assumptions behind them are listed in Appendix A1."],
       size=10, color="#b7c7db")
slides.append(s)

# 2 ---- Executive summary ----------------------------------------------
s = Slide(notes="Executive summary. Numbers: calc.py. CFO gross 7.57; CFO net 2.7-5.3; recommended gross 4.27, net 2.36-3.46.")
header(s, "Executive summary",
       "Yes, raise prices in 2027: +10% in mid-market and up to contract caps in enterprise. Hold SMB prices until a Q1 test supports a rise", 2)
rows = [
    ("Churn is rising almost only in the 2025 promotion cohort.",
     f" Established SMB customers churn 2.1% a month (2.0% a year ago). The 2,100 promotion customers churn at an implied ~{C['promo_ch']:.1f}% and make up ~{C['promo_share_churners']*100:.0f}% of SMB churners. Mid-market (0.8%) and enterprise (0.2%) churn remains low."),
    ("The CFO is half right.",
     " Churn is not a broad price problem. But the promotion cohort is very price-sensitive: 52% of its churners cite price. And Inkwell’s $9 Starter plan has cut our SMB win rate from 51% to 38%."),
    ("A 12% rise on every plan is worth $7.6M gross in 2027, not $10.3M.",
     " 15% of mid-market ARR and 60% of enterprise ARR do not renew in 2027, and most enterprise contracts cap rises at 7%. In SMB, the rise nets anywhere from ~$1.2M to about zero once churn is counted."),
    ("Recommendation: raise prices segment by segment.",
     f" +10% at mid-market renewal (the level tested in 2024). Enterprise: 7% where capped, 10% elsewhere. SMB list prices held in H1, with a Q1 test of +8% for established customers. Promotion-cohort prices frozen, plus an activation push. Est. {m(C['rec_gross'])} gross, ${C['rec_net'][1]:.1f}–{C['rec_net'][0]:.1f}M net."),
    ("The trade-off.",
     f" On paper this is ${C['gap_vs_cfo'][0]:.1f}–{C['gap_vs_cfo'][1]:.1f}M less 2027 ARR than the CFO plan, but it avoids losing an extra ~320–640 SMB customers. NRR stays at ~112–113%. New customers still need to add ~$1.5–2.6M of ARR to reach +15%."),
]
y = 1.78
for i, (lead, rest) in enumerate(rows):
    s.text(L, y, 0.45, 0.45, str(i + 1), size=18, bold=True, color=BLUE)
    s.text(L + 0.5, y, CW - 0.5, 0.86, [dict(runs=[B(lead), (rest, {})])], size=12.5)
    y += 0.9
s.rect(L, 6.32, CW, 0.5, BLUE_LT)
s.text(L + 0.15, 6.32, CW - 0.3, 0.5,
       [dict(runs=[B("Decisions for December: "),
                   ("approve the segmented plan, the SMB test and its go/no-go rule, and a single churn definition for board reporting.", {})])],
       size=12, valign="m")
footer(s, SRC + ". Net figures are estimates; see Appendix A1.")
slides.append(s)

# 3 ---- Churn decomposition -------------------------------------------
s = Slide(notes="Implied promo churn = (5,900 x 3.1% - 3,800 x 2.1%) / 2,100 = 4.9%. Mid-2026 counts used as weights for H1 2026 (approximation).")
header(s, "Where churn is rising",
       "Rising churn is concentrated in the 2025 promotion cohort; churn among established customers is almost flat", 3)
s.text(L, 1.72, 7.6, 0.3, "Monthly logo churn by customer group, %", size=12, bold=True)
legend(s, L, 2.05, [("H1 2025", GRAYBAR), ("H1 2026", BLUE), ("H1 2026, promotion cohort (implied)", ORANGE)])
groups = [("SMB, not via\npromotion", 2.0, 2.1), ("SMB, 2025\npromotion cohort", None, C["promo_ch"]),
          ("SMB total", 2.0, 3.1), ("Mid-market", 0.6, 0.8), ("Enterprise", 0.2, 0.2)]
x0, base, top, vmax = L + 0.2, 5.95, 2.6, 5.5
s.line(x0, base, x0 + 7.3, base, INK2, 0.75)
gw = 7.3 / len(groups)
bwid = 0.42
for i, (lab, a, b) in enumerate(groups):
    gx = x0 + i * gw + gw / 2
    for j, (v, col) in enumerate([(a, GRAYBAR), (b, ORANGE if i == 1 else BLUE)]):
        bx = gx - bwid - 0.02 if j == 0 else gx + 0.02
        if v is None:
            s.text(bx - 0.1, base - 0.32, bwid + 0.2, 0.28, "n/a", size=10, color=MUTED, align="c")
            continue
        hgt = (base - top) * v / vmax
        s.rect(bx, base - hgt, bwid, hgt, col)
        lbl = f"{v:.1f}" + (" est." if i == 1 and j == 1 else "")
        s.text(bx - 0.25, base - hgt - 0.3, bwid + 0.5, 0.28, lbl, size=10.5, bold=True, align="c")
    s.text(gx - gw / 2, base + 0.06, gw, 0.5, lab.split("\n"), size=10, color=INK2, align="c")
# right panel
px = 8.45
panel(s, px, 1.72, R - px, 4.95)
s.text(px + 0.2, 1.85, R - px - 0.4, 0.3, "The promotion cohort in SMB (est.)", size=12, bold=True)
tiles = [(f"{C['promo_share_cust']*100:.0f}%", "of SMB customers (2,100 of 5,900)"),
         (f"{C['promo_share_arr']*100:.0f}%", "of SMB ARR ($4.4M of $21.0M at full price)"),
         (f"~{C['promo_share_churners']*100:.0f}%", "of SMB customers who churned in H1 2026")]
ty = 2.3
for v, lab in tiles:
    s.text(px + 0.2, ty, 1.3, 0.5, v, size=24, bold=True, color=ORANGE if v.startswith("~") else INK)
    s.text(px + 1.55, ty + 0.03, R - px - 1.75, 0.5, lab, size=11, color=INK2, valign="m")
    ty += 0.68
s.line(px + 0.2, 4.4, R - 0.2, 4.4, GRID)
s.text(px + 0.2, 4.5, R - px - 0.4, 2.1,
       [dict(runs=[B("So what: "), ("about 1.0 point of the 1.1-point rise in SMB churn comes from the promotion cohort. "
                                    "Without it, SMB churn would be 2.1%, close to last year’s 2.0%.", {})], space_after=6),
        dict(runs=[("Mid-market churn has also edged up (0.6% to 0.8%). The pack does not explain why; it should be checked before renewals.", {})])],
       size=11)
footer(s, SRC + ", Table 1 and §6. Promotion-cohort churn is implied: (5,900 × 3.1% − 3,800 × 2.1%) ÷ 2,100 ≈ 4.9%, "
          "using mid-2026 customer counts as weights. The cohort joined Feb–Aug 2025, so it has no H1 2025 rate.")
slides.append(s)

# 4 ---- Why the promo cohort leaves ------------------------------------
s = Slide(notes="Activation estimate: if low activators churn 3x others and non-promo (72% activated) churn 2.1%, then activated churn x=1.35%, low 4.0%; "
                "at 41% activation the promo cohort would churn ~2.9%, vs ~4.9% implied, so activation explains ~0.8 of ~2.8 pts excess (~30%).")
header(s, "Why the promotion cohort leaves",
       "Promotion customers left over price when the discount ended; weak activation explains only part of their churn", 4)
s.text(L, 1.72, 6.0, 0.3, "Churners citing “price / found a cheaper option” as main reason, %", size=12, bold=True)
hbars(s, L, 2.25, 6.0, [("All SMB churners, H1 2025", 19, GRAYBAR, False),
                        ("All SMB churners, H1 2026", 34, GRAYBAR, False),
                        ("Promotion-cohort churners, H1 2026", 52, ORANGE, True),
                        ("Other SMB churners, H1 2026", 18, BLUE, True)], vmax=60, label_w=3.0)
s.text(6.95, 1.72, 5.8, 0.3, "New customers sending ≥5 documents in month 1, %", size=12, bold=True)
hbars(s, 6.95, 2.25, 5.78, [("2025 promotion cohort", 41, ORANGE, True),
                            ("Other cohorts", 72, BLUE, True)], vmax=80, label_w=2.0)
s.text(6.95, 3.25, 5.78, 0.75,
       "SMB customers who send fewer than five documents in month 1 churn at about 3× the rate of those who send more.",
       size=10.5, color=INK2)
s.line(L, 4.25, R, 4.25, GRID)
cols = [("They joined for the discount",
         "They paid 50% less for six months. Most who left did so within two months of the discount ending, "
         "which for them was a 100% price step."),
        ("Established customers are not more price-sensitive yet",
         "18% of non-promotion churners cite price, vs 19% of all SMB churners a year ago, even after Inkwell’s launch."),
        ("Onboarding alone will not fix the cohort (est.)",
         f"The activation gap accounts for ~0.8 of the cohort’s ~2.8-point excess churn (~{C['activation_share_of_excess']*100:.0f}%). "
         "The rest coincides with the discount ending.")]
cx, cwid = L, (CW - 0.5) / 3
for t, b in cols:
    s.text(cx, 4.4, cwid, 0.55, t, size=12.5, bold=True, color=BLUE_DK)
    s.text(cx, 4.95, cwid, 1.4, b, size=11.5)
    cx += cwid + 0.25
s.rect(L, 6.25, CW, 0.5, ORANGE_LT)
s.text(L + 0.15, 6.25, CW - 0.3, 0.5, [dict(runs=[B("Implication: "), ("do not raise the promotion cohort’s price in 2027. A second price step within ~18 months would push out the customers onboarding is trying to save.", {})])],
       size=11.5, valign="m")
footer(s, SRC + ", Table 2, §6 and §9. Exit-survey shares are of churners who answered. Activation split is our estimate; see Appendix A1.")
slides.append(s)

# 5 ---- Segment scorecard ----------------------------------------------
s = Slide(notes="Scorecard compiled from Tables 1, sections 7-9.")
header(s, "Pricing power by segment",
       "Pricing power sits in mid-market and enterprise; SMB is where Inkwell is winning deals", 5)
cols = ["", "SMB", "Mid-market", "Enterprise"]
cx = [L, L + 2.35, L + 5.75, L + 9.15]
cwd = [2.25, 3.3, 3.3, CW - 9.15 + L - L]
cwd[3] = R - cx[3]
rowsd = [
    ("ARR (share of total)", "$21.0M (24%)", "$41.0M (48%)", "$24.0M (28%)"),
    ("Monthly logo churn, H1 2026 (H1 2025)", "3.1% (2.0%); 2.1% excluding the promotion cohort", "0.8% (0.6%)", "0.2% (0.2%)"),
    ("Net revenue retention, trailing 12 months", "94%", "112%", "118%"),
    ("Why customers stay or leave", "34% of churners cite price (18% excluding the promotion cohort)", "Integrations and audit trail (customer advisory board, 2026)", "Integrations and audit trail (customer advisory board, 2026)"),
    ("Competition", "Inkwell Starter $9 vs our $15; our win rate against Inkwell fell from 51% to 38%", "Inkwell not seen in deals over 200 seats; smaller accounts may be exposed", "Inkwell not seen"),
    ("Past price evidence", "2023: +8% lifted churn 1.8% to 2.3% for six months; it then settled at 1.9%", "2024: +10% for new sign-ups; conversion 23.1% vs 23.6% (not significant)", "60% of ARR capped at 7% a year"),
    ("ARR renewing in 2027", "100%", "85%", "40%"),
]
y = 1.75
s.rect(L, y, CW, 0.36, "#0f2c4f")
for i, c in enumerate(cols):
    s.text(cx[i] + 0.08, y, cwd[i], 0.36, c, size=11.5, bold=True, color="#ffffff", valign="m")
y += 0.36
rh = [0.4, 0.55, 0.4, 0.55, 0.72, 0.72, 0.4]
for k, r in enumerate(rowsd):
    if k % 2 == 1:
        s.rect(L, y, CW, rh[k], PANEL)
    for i, c in enumerate(r):
        s.text(cx[i] + 0.08, y, cwd[i] - 0.16, rh[k], c, size=10.5, bold=(i == 0), color=INK if i else INK2, valign="m")
    y += rh[k]
# verdict row
s.line(L, y, R, y, INK2, 1)
vh = 0.62
s.text(cx[0] + 0.08, y, cwd[0], vh, "Pricing power", size=11.5, bold=True, valign="m")
verd = [("Low: hold list price and test", ORANGE), ("High: raise at renewal", BLUE), ("High, but capped by contracts", BLUE)]
for i, (t, col) in enumerate(verd):
    s.rect(cx[i + 1] + 0.1, y + 0.23, 0.16, 0.16, col, shape="oval")
    s.text(cx[i + 1] + 0.32, y, cwd[i + 1] - 0.4, vh, t, size=11.5, bold=True, valign="m")
footer(s, SRC + ", Table 1, §7–§9. The 2024 mid-market test covered new sign-ups only, not renewals.")
slides.append(s)

# 6 ---- CFO waterfall --------------------------------------------------
s = Slide(notes="12% x 86.0 = 10.32. Less MM not renewing (15% x 41 x 12% = 0.74), Ent not renewing (60% x 24 x 12% = 1.73), "
                "Ent caps (9.6 x 60% x 5pts = 0.29) = 7.57 gross. Planning-case churn: SMB 1.27, MM 0.99 -> 5.30. Stress: SMB 2.54, MM 2.34 -> 2.68.")
header(s, "Testing the CFO proposal",
       "The CFO’s $10.3M is at most $7.6M in 2027 once renewal timing and enterprise caps are applied, before any churn", 6)
s.text(L, 1.72, 8.3, 0.3, "2027 ARR uplift from +12% on every plan at renewal, $M", size=12, bold=True)
steps = [("+12% on all\n$86.0M ARR", C["cfo_headline"], "total"),
         ("Mid-market ARR\nnot renewing\nin 2027", -C["cfo_mm_not_renew"], "delta"),
         ("Enterprise ARR\nnot renewing\nin 2027", -C["cfo_ent_not_renew"], "delta"),
         ("7% cap on\nenterprise\nrenewals", -C["cfo_ent_cap"], "delta"),
         ("Gross uplift\nreachable\nin 2027", C["cfo_gross_total"], "total"),
         ("SMB churn\nresponse (est.)", -C["smb_drag"][0], "est"),
         ("Mid-market\nchurn response\n(est.)", -C["cfo_mm"][0][1], "est"),
         ("Net uplift,\nplanning case\n(est.)", C["cfo_net"][0], "totalest")]
x0, base, top, vmax = L + 0.1, 5.55, 2.35, 11.0
pw = 8.4
sw = pw / len(steps)
bw = 0.6
s.line(x0, base, x0 + pw, base, INK2, 0.75)
run = 0
sc = (base - top) / vmax
for i, (lab, v, kind) in enumerate(steps):
    bx = x0 + i * sw + (sw - bw) / 2
    if kind.startswith("total"):
        yt, yb = base - v * sc, base
        col = BLUE if kind == "total" else "#86b6ef"
        run = v
        lbl = f"{v:.1f}"
    else:
        yt, yb = base - run * sc, base - (run + v) * sc
        col = GRAYBAR if kind == "delta" else ORANGE_LT
        run += v
        lbl = f"−{-v:.1f}"
    s.rect(bx, yt, bw, yb - yt, col)
    if kind == "est":
        s.rect(bx, yt, bw, yb - yt, None, line=ORANGE, lw=1)
    s.text(bx - 0.3, yt - 0.3, bw + 0.6, 0.28, lbl, size=11, bold=True, align="c")
    if i < len(steps) - 1:
        s.line(bx + bw, base - run * sc, bx + sw, base - run * sc, MUTED, 0.5, dash=True)
    s.text(x0 + i * sw - 0.02, base + 0.06, sw + 0.04, 0.75, lab.split("\n"), size=9.5, color=INK2, align="c")
s.text(x0, 6.4, pw, 0.4, f"Stress case (customers react twice as strongly): net {m(C['cfo_net'][1])}.", size=10.5, color=INK2)
px = 9.3
panel(s, px, 1.72, R - px, 4.95)
s.text(px + 0.2, 1.85, R - px - 0.4, 4.7,
       [dict(runs=[B("What the $10.3M assumes")], space_after=4),
        dict(runs=[("Every dollar of ARR renews in 2027 and takes the full 12%.", {})], space_after=12),
        dict(runs=[B("What the pack says")], space_after=4),
        dict(runs=[("15% of mid-market ARR renews after 2027", {})], bullet=True, space_after=3),
        dict(runs=[("60% of enterprise ARR renews after 2027", {})], bullet=True, space_after=3),
        dict(runs=[("60% of enterprise ARR is capped at 7% a year", {})], bullet=True, space_after=12),
        dict(runs=[B("So what")], space_after=4),
        dict(runs=[("The realistic gross figure is $2.8M (27%) lower, and churn has not yet been counted. Most of what remains comes from mid-market, not SMB.", {})])],
       size=11)
footer(s, SRC + ", §4 and §8. We assume the capped share of enterprise ARR is the same in the 2027 renewal tranche. "
          "Churn responses are our estimates (pp. 7–8, Appendix A1).")
slides.append(s)

# 7 ---- SMB ------------------------------------------------------------
s = Slide(notes="SMB gross = 21.0 x 12% = 2.52. 2023 analog scaled to 12%: +0.75pt/month for 6 months and +0.15pt after -> 5.4% of SMB customers lost extra "
                "(~320) -> 1.27 ARR. Twice 2023: 10.8% (~640) -> 2.54. Break-even loss for +12% = 10.7% of ARR.")
header(s, "SMB",
       "In SMB, a 12% rise nets between +$1.2M and about zero, and costs an extra 320–640 customers", 7)
s.text(L, 1.72, 5.9, 0.3, "2027 SMB ARR effect of +12% at renewal, $M (est.)", size=12, bold=True)
bars = [("Gross uplift\n(no extra churn)", C["cfo_gross"]["SMB"], BLUE, ""),
        ("Net if customers react\nas in 2023 (scaled)", C["smb_net"][0], "#86b6ef", "~320 extra\ncustomers lost"),
        ("Net if the reaction\nis twice 2023", max(C["smb_net"][1], 0), "#86b6ef", "~640 extra\ncustomers lost")]
x0, base, top, vmax = L + 0.2, 5.4, 2.6, 3.0
s.line(x0, base, x0 + 5.5, base, INK2, 0.75)
sw = 5.5 / 3
for i, (lab, v, col, note) in enumerate(bars):
    bx = x0 + i * sw + (sw - 0.7) / 2
    hgt = (base - top) * v / vmax
    if hgt > 0.01:
        s.rect(bx, base - hgt, 0.7, hgt, col)
    s.text(bx - 0.4, base - hgt - 0.32, 1.5, 0.3, f"{v:.1f}" if v > 0.05 else "≈0.0", size=12, bold=True, align="c")
    s.text(x0 + i * sw, base + 0.06, sw, 0.5, lab.split("\n"), size=10, color=INK2, align="c")
    if note:
        s.text(x0 + i * sw, base + 0.6, sw, 0.5, note.split("\n"), size=10, bold=True, color=ORANGE, align="c")
# price ladder
px = 6.85
s.text(px, 1.72, R - px, 0.3, "Price per user per month, $", size=12, bold=True)
ladder = [("Inkwell Starter", 9, ORANGE), ("Palisade SMB today", 15, BLUE), ("Palisade SMB +12%", 16.8, "#86b6ef"),
          ("Inkwell Pro", 24, ORANGE), ("Palisade Business", 29, BLUE)]
hbars(s, px, 2.2, R - px, [(a, b, c, a.startswith("Palisade SMB")) for a, b, c in ladder], vmax=32, label_w=1.9,
      bar_h=0.24, gap=0.14, fmt=lambda v: f"${v:.2f}" if v % 1 else f"${v:.0f}", size=10.5)
s.text(px, 4.2, R - px, 0.3, f"Premium over Inkwell Starter: {C['prem_now']*100:.0f}% today, {C['prem_after']*100:.0f}% after a 12% rise",
       size=10.5, color=INK2)
bullets(s, px, 4.65, R - px, 1.9,
        [[B("Win rate already falling: "), ("down from 51% to 38% in SMB deals where Inkwell was considered.", {})],
         [B("The 2023 benchmark predates Inkwell. "), ("How price-sensitive established SMB customers are now is the pack’s main open question.", {})],
         [B("A permanent cost: "), ("in 2023, churn settled 0.1 point above where it started, so lost customers keep compounding.", {})]],
        size=11, after=5)
footer(s, SRC + ", §7–§8. Estimate: the 2023 response (+0.5 pt monthly churn for six months, +0.1 pt after) scaled to 12% "
          "removes ~5.4% of SMB customers over 12 months. Break-even for +12% is a loss of 10.7% of ARR.")
slides.append(s)

# 8 ---- Mid-market ------------------------------------------------------
s = Slide(notes="MM renewing ARR 2027 = 41.0 x 85% = 34.85. +10% = 3.49 gross. Break-even loss = 10/110 = 9.1%. "
                "Planning: 2.1% of renewing ARR lost (2024 test gap 23.1 vs 23.6) -> 0.81 -> net 2.67. Stress 5% -> 1.92 -> net 1.57.")
header(s, "Mid-market",
       "In mid-market, +10% pays off unless it drives away over 9% of renewing ARR; the best evidence points to about 2%", 8)
s.text(L, 1.72, 7.0, 0.3, "Share of 2027 renewing mid-market ARR lost because of a +10% rise, %", size=12, bold=True)
yy = hbars(s, L, 2.25, 7.0, [("Planning case: 2024 test gap", C["mm_test_gap"] * 100, BLUE, True),
                             ("Stress case (assumed)", 5.0, "#86b6ef", False),
                             ("Break-even loss for +10%", C["mm_breakeven"] * 100, GRAYBAR, True)],
           vmax=10, label_w=2.6, fmt=lambda v: f"{v:.1f}%", bar_h=0.34, gap=0.3)
s.text(L, yy + 0.05, 7.0, 0.85,
       [dict(runs=[B("For scale: "), (f"all mid-market churn today is ~{C['annual']['MM']*100:.0f}% of customers a year (0.8% a month). "
                                      "Losing 9% on price alone would mean the rise roughly doubles mid-market churn.", {})])],
       size=11, color=INK2)
s.rect(L, 5.25, 7.0, 0.98, BLUE_LT)
s.text(L + 0.15, 5.32, 6.7, 0.9,
       [dict(runs=[B("What would change our mind")], space_after=4),
        dict(runs=[("If accounts renewed at the new price in Q1 lose more than ~4% of their ARR (twice the planning case), pause further rises and review accounts of up to 200 seats before Q2 renewals.", {})])],
       size=11)
# net tiles
px = 8.1
panel(s, px, 1.72, R - px, 4.95)
s.text(px + 0.2, 1.85, R - px - 0.4, 0.3, "2027 mid-market ARR uplift, $M (est.)", size=12, bold=True)
tiles = [(f"{C['rec_mm'][0][0]:.1f}", "gross: +10% on the 85% of ARR renewing"),
         (f"{C['rec_mm'][0][2]:.1f}", "net, planning case"),
         (f"{C['rec_mm'][1][2]:.1f}", "net, stress case")]
ty = 2.3
for v, lab in tiles:
    s.text(px + 0.2, ty, 1.1, 0.5, v, size=24, bold=True, color=INK)
    s.text(px + 1.3, ty + 0.02, R - px - 1.5, 0.5, lab, size=11, color=INK2, valign="m")
    ty += 0.62
s.line(px + 0.2, 4.2, R - 0.2, 4.2, GRID)
s.text(px + 0.2, 4.3, R - px - 0.4, 0.3, "Why 10%, not 12%", size=11.5, bold=True, color=BLUE_DK)
s.text(px + 0.2, 4.6, R - px - 0.4, 0.95,
       "10% is the level we tested. 12% adds ~$0.7M gross but goes beyond the evidence, in the segment that carries 48% of ARR.",
       size=10.5)
s.text(px + 0.2, 5.5, R - px - 0.4, 0.3, "Watch-outs", size=11.5, bold=True, color=BLUE_DK)
bullets(s, px + 0.2, 5.8, R - px - 0.4, 0.85,
        ["The test covered new sign-ups, not renewals",
         "Inkwell may reach accounts with 51–200 seats"], size=10.5, after=2)
footer(s, SRC + ", §8–§9. Planning case: renewal losses equal the 2024 test’s relative conversion gap (23.1% vs 23.6%, 2.1%). "
          "The stress case of 5% is our assumption.")
slides.append(s)

# 9 ---- Options ---------------------------------------------------------
s = Slide(notes="New-logo ARR needed = 12.9 - 7.98 (installed base at ~109% NRR) - net price effect.")
header(s, "Options",
       "Of three options, a segmented rise gives the best balance between 2027 ARR and churn risk", 9)
oc = [L, L + 2.6, L + 5.9, L + 9.0]
ow = [2.5, 3.2, 3.0, R - (L + 9.0)]
heads = ["", "A. +12% on every plan\n(CFO proposal)", "B. Hold all prices;\nfix onboarding first", "C. Segmented rise\n(recommended)"]
y = 1.75
for i, h in enumerate(heads):
    if i == 3:
        s.rect(oc[i] - 0.05, y, ow[i] + 0.05, 0.62, BLUE)
    elif i:
        s.rect(oc[i] - 0.05, y, ow[i] - 0.05, 0.62, "#0f2c4f")
    s.text(oc[i] + 0.08, y, ow[i] - 0.2, 0.62, h.split("\n"), size=11.5, bold=True, color="#ffffff", valign="m")
y += 0.62
orows = [
    ("2027 ARR uplift, gross", "$7.6M", "$0", f"{m(C['rec_gross'])}, plus up to {m(C['smb_h2_gross'])} if the SMB test passes"),
    ("Net of churn response (est.)", f"${C['cfo_net'][1]:.1f}–{C['cfo_net'][0]:.1f}M", "$0", f"${C['rec_net'][1]:.1f}–{C['rec_net'][0]:.1f}M"),
    ("Extra SMB customers lost (est.)", "~320–640", "None", "None in H1; SMB rise only if the test passes"),
    ("New-customer ARR still needed for +15% (est.)", f"$0–{C['need_cfo'][1]:.1f}M", f"{m(C['need_hold'])}", f"${C['need_rec'][0]:.1f}–{C['need_rec'][1]:.1f}M"),
    ("Overall NRR (est.)", "~112–115%", "~109%", "~112–113%"),
    ("Evidence base", "SMB and 12% are beyond tested levels", "Leaves proven pricing power in mid-market unused", "Stays within tested price levels"),
    ("Reversibility", "Low: hits all 7,400 customers at once", "High", "High: SMB decision taken on Q1 data"),
]
rhs = [0.6, 0.45, 0.6, 0.6, 0.45, 0.6, 0.6]
for k, r in enumerate(orows):
    if k % 2 == 0:
        s.rect(L, y, CW, rhs[k], PANEL)
    s.rect(oc[3] - 0.05, y, ow[3] + 0.05, rhs[k], "#e6f0fc" if k % 2 == 0 else "#f3f8fe")
    for i, c in enumerate(r):
        s.text(oc[i] + 0.08, y, ow[i] - 0.2, rhs[k], c, size=10.5, bold=(i == 0 or (i == 3 and k < 2)),
               color=INK2 if i == 0 else INK, valign="m")
    y += rhs[k]
s.text(L, y + 0.12, CW, 0.62,
       [dict(runs=[B("Why C over A: "),
                   (f"A adds ${C['gap_vs_cfo'][0]:.1f}–{C['gap_vs_cfo'][1]:.1f}M more 2027 ARR on paper, almost all from SMB. That gain shrinks to nothing if SMB customers react twice as strongly as in 2023, "
                    "and it costs customers in the one segment where a competitor is gaining ground.", {})])], size=11)
footer(s, SRC + ". All net, NRR and new-customer figures are estimates: they assume the trailing-12-month NRR (~109%) holds in 2027. See Appendix A1.")
slides.append(s)

# 10 ---- Recommended plan --------------------------------------------
s = Slide(notes="Enterprise: 9.6 renewing; 60% at 7% = 0.40, 40% at 10% = 0.38 -> 0.79. SMB H2 option: 16.6 x 8% x 50% = 0.66 gross.")
header(s, "Recommended plan",
       "Recommended 2027 plan: raise prices where customers stay; hold and test where they are leaving", 10)
pc = [L, L + 2.2, L + 6.2, L + 8.35, L + 10.05]
pw_ = [2.1, 3.9, 2.05, 1.6, R - (L + 10.05)]
heads = ["Customer group", "Action", "Timing", "2027 ARR effect", "Guardrail"]
y = 1.75
s.rect(L, y, CW, 0.38, "#0f2c4f")
for i, h in enumerate(heads):
    s.text(pc[i] + 0.08, y, pw_[i], 0.38, h, size=11, bold=True, color="#ffffff", valign="m")
y += 0.38
prow = [
    ("Mid-market", BLUE, "+10% on list price at renewal. Customer Success reviews accounts of up to 200 seats where Inkwell is present.",
     "Renewals from Jan 2027 (85% of ARR), subject to notice terms", f"+{C['rec_mm'][0][0]:.1f}M gross; {C['rec_mm'][1][2]:.1f}–{C['rec_mm'][0][2]:.1f}M net",
     "Pause if monthly churn exceeds 1.0% for a quarter"),
    ("Enterprise", BLUE, "Up to the 7% cap on capped contracts; 10% target on the rest, negotiated account by account.",
     "2027 renewals (40% of ARR)", f"+{C['rec_ent']:.1f}M", "No change to multi-year terms in force"),
    ("SMB, established customers", ORANGE, "Hold list price in H1. Randomised test of +8% (the 2023 level) on half of Q1 renewals.",
     "Test in Q1; decision by end of Q2; roll out in H2 if passed", f"$0 in plan; up to +{C['smb_h2_gross']:.1f}M gross",
     "Go only if extra churn is under 0.5 pt a month (the 2023 response)"),
    ("SMB, 2025 promotion cohort", ORANGE, "No price rise in 2027. Activation outreach to low-usage accounts, measured against a holdout group.",
     "From Jan 2027", "Protects a $4.4M ARR base", "Track cohort churn and usage monthly"),
    ("SMB, new customers", ORANGE, "Keep the $15 list price. No deep introductory discounts unless tied to activation.",
     "All of 2027", "Not modelled", "Win rate vs Inkwell (38% today)"),
]
rh = [0.78, 0.66, 0.78, 0.78, 0.66]
for k, r in enumerate(prow):
    if k % 2 == 1:
        s.rect(L, y, CW, rh[k], PANEL)
    s.rect(L, y + 0.08, 0.06, rh[k] - 0.16, r[1])
    vals = [r[0], r[2], r[3], r[4], r[5]]
    for i, c in enumerate(vals):
        s.text(pc[i] + 0.12 if i == 0 else pc[i] + 0.08, y, pw_[i] - 0.16, rh[k], c, size=10.5,
               bold=(i in (0, 3)), color=INK, valign="m")
    y += rh[k]
s.line(L, y, R, y, INK2, 1)
s.text(pc[0] + 0.12, y + 0.02, 6.0, 0.45, "Total (est.)", size=11.5, bold=True, valign="m")
s.text(pc[3] + 0.08, y + 0.02, 3.6, 0.45, f"+{C['rec_gross']:.1f}M gross; {C['rec_net'][1]:.1f}–{C['rec_net'][0]:.1f}M net",
       size=11.5, bold=True, valign="m")
footer(s, SRC + ". The 2027 ARR effect is the run-rate once 2027 renewals complete; in-year revenue will be lower. "
          "SMB test design: see p. 13.")
slides.append(s)

# 11 ---- Growth bridge -------------------------------------------------
s = Slide(notes="Target 98.9 = 86.0 x 1.15. Installed base at ARR-weighted NRR 109.3% adds 7.98. Price net 2.36-3.46. New logos needed 1.46-2.56.")
header(s, "Path to +15% ARR",
       "Even with the price rise, about $1.5–2.6M of the +15% ARR goal must come from new customers", 11)
s.text(L, 1.72, 7.8, 0.3, "ARR growth needed in 2027 to reach +15% ($86.0M to $98.9M), $M (est.)", size=12, bold=True)
st = [("Installed base\nat today’s NRR\n(~109%)", C["base_growth"], BLUE, False),
      ("Price rise, net\n(planning case)", C["rec_net"][0], "#86b6ef", False),
      ("New-customer\nARR needed", C["need_rec"][0], ORANGE_LT, True),
      ("Growth needed\nfor +15%", C["growth_needed"], "#0f2c4f", None)]
x0, base, top, vmax = L + 0.2, 5.6, 2.4, 13.5
pw = 7.4
sw = pw / len(st)
sc = (base - top) / vmax
s.line(x0, base, x0 + pw, base, INK2, 0.75)
run = 0
for i, (lab, v, col, est) in enumerate(st):
    bx = x0 + i * sw + (sw - 0.8) / 2
    if est is None:
        yt, yb = base - v * sc, base
    else:
        yt, yb = base - (run + v) * sc, base - run * sc
        run += v
    s.rect(bx, yt, 0.8, yb - yt, col)
    if est:
        s.rect(bx, yt, 0.8, yb - yt, None, line=ORANGE, lw=1.25)
    s.text(bx - 0.4, yt - 0.32, 1.6, 0.3, ("+" if est is not None else "") + f"{v:.1f}", size=12, bold=True, align="c")
    if i < len(st) - 1 and est is not None:
        s.line(bx + 0.8, base - run * sc, bx + sw, base - run * sc, MUTED, 0.5, dash=True)
    s.text(x0 + i * sw, base + 0.06, sw, 0.75, lab.split("\n"), size=10, color=INK2, align="c")
s.text(x0, 6.45, pw, 0.35, f"Stress case: price +{C['rec_net'][1]:.1f}M, so new customers must add +{C['need_rec'][1]:.1f}M.",
       size=10.5, color=INK2)
px = 8.6
panel(s, px, 1.72, R - px, 4.95)
s.text(px + 0.2, 1.85, R - px - 0.4, 4.7,
       [dict(runs=[B("Reading the bridge")], space_after=6),
        dict(runs=[("Price is the second-largest lever. Only option A, in its planning case, would close the gap without new customers.", {})], bullet=True, space_after=6),
        dict(runs=[(f"Holding prices (option B) would leave ~{m(C['need_hold'])} to new customers, about three times as much.", {})], bullet=True, space_after=6),
        dict(runs=[("NRR stays well above the 100% floor (~112–113%).", {})], bullet=True, space_after=14),
        dict(runs=[B("What we could not check")], space_after=6),
        dict(runs=[("The pack has no new-customer bookings or pipeline. Finance should confirm that $1.5–2.6M of new-customer ARR is realistic before December.", {})], bullet=True, space_after=6),
        dict(runs=[("Base growth assumes trailing NRR holds; SMB NRR (94%) is the drag.", {})], bullet=True)],
       size=11)
footer(s, SRC + ", §3 and Table 1. Today’s NRR is ARR-weighted from segment NRRs (21.0 × 94% + 41.0 × 112% + 24.0 × 118%) ÷ 86.0 ≈ 109%.")
slides.append(s)

# 12 ---- Onboarding ----------------------------------------------------
s = Slide(notes="If the promo cohort churned at the non-promo rate (2.1%), SMB churn would be 2.1% = 32% lower than 3.1%. Halving = 1.55%, below any SMB level in the pack (1.8%-2.3%).")
header(s, "Onboarding",
       "Fund onboarding, but plan on it cutting SMB churn by up to a third, not by half", 12)
s.text(L, 1.72, 6.6, 0.3, "SMB monthly logo churn, %", size=12, bold=True)
ob = [("H1 2026\nactual", 3.1, BLUE, ""), ("If the promotion cohort\nchurned like other SMB", 2.1, "#86b6ef", "−32%: best case\nfor fixing the cohort"),
      ("“Halve SMB churn”\n(Customer Success claim)", 1.55, GRAYBAR, "Below any SMB level in\nthe pack (lowest: 1.8%)")]
x0, base, top, vmax = L + 0.2, 5.3, 2.5, 3.6
pw = 6.2
sw = pw / 3
s.line(x0, base, x0 + pw, base, INK2, 0.75)
for i, (lab, v, col, note) in enumerate(ob):
    bx = x0 + i * sw + (sw - 0.75) / 2
    hgt = (base - top) * v / vmax
    s.rect(bx, base - hgt, 0.75, hgt, col)
    s.text(bx - 0.4, base - hgt - 0.32, 1.55, 0.3, f"{v:.2f}".rstrip("0").rstrip("."), size=12, bold=True, align="c")
    s.text(x0 + i * sw, base + 0.06, sw, 0.5, lab.split("\n"), size=10, color=INK2, align="c")
    if note:
        s.text(x0 + i * sw, base + 0.6, sw, 0.5, note.split("\n"), size=10, bold=True, color=INK, align="c")
px = 7.4
s.text(px, 1.72, R - px, 0.3, "What onboarding can and cannot do", size=12, bold=True)
bullets(s, px, 2.1, R - px, 2.4,
        [[B("Can: "), ("lift activation. Only 41% of promotion customers sent five documents in month 1, against 72% of others, and low activators churn ~3× as often.", {})],
         [B("Cannot: "), ("halve SMB churn in two quarters. Even if the promotion cohort churned like everyone else, SMB churn would fall to 2.1%, not 1.55%.", {})],
         [B("Also: "), ("the cohort will shrink on its own, so blended SMB churn should fall even without action. Measure the programme against a holdout, not a before/after comparison.", {})]],
        size=11, after=8)
s.rect(px, 4.55, R - px, 1.0, BLUE_LT)
s.text(px + 0.15, 4.62, R - px - 0.3, 0.9,
       [dict(runs=[B("Proposed targets for the Head of Customer Success")], space_after=5),
        dict(runs=[("Raise the promotion cohort’s activation and cut its churn toward 2.1% a month; report against the holdout monthly", {})], bullet=True, space_after=3),
        dict(runs=[("Make activation a condition of any future introductory discount", {})], bullet=True)],
       size=10.5)
footer(s, SRC + ", §6, §8–§10. SMB churn levels in the pack: 1.8% (before 2023 rise), 2.3% (2023 peak), 1.9% (after), 2.0% (H1 2025).")
slides.append(s)

# 13 ---- Guardrails & timeline ----------------------------------------
s = Slide(notes="Guardrails derived from break-even and 2023 analog. SMB test sized to detect a response twice the 2023 level (the level at which SMB pricing stops paying).")
header(s, "Guardrails",
       "Three checkpoints in 2027 let us stop or extend the rise before it hurts retention", 13)
phases = [("Dec 2026", "Decide", ["Approve the segmented plan", "Finance sets one churn definition", "Send renewal notices to mid-market and enterprise customers"]),
          ("Q1 2027", "Launch", ["Mid-market and enterprise renewals at the new prices", "SMB +8% test on half of Q1 renewals", "Activation programme starts, with a holdout"]),
          ("End of Q1", "Checkpoint 1", ["Read mid-market churn on accounts renewed at the new price", "Early read of the SMB test"]),
          ("End of Q2", "Checkpoint 2", ["SMB go/no-go for H2", "Onboarding results; reset targets"]),
          ("Q4 2027", "Checkpoint 3", ["Set 2028 pricing: mid-market beyond 10%? SMB packaging against Inkwell?"])]
pxw = (CW - 0.2 * 4) / 5
y0 = 1.8
for i, (when, what, items) in enumerate(phases):
    x = L + i * (pxw + 0.2)
    s.rect(x, y0, pxw, 0.62, "#0f2c4f" if i == 0 else BLUE)
    s.text(x + 0.1, y0, pxw - 0.2, 0.62, [dict(runs=[B(when)]), dict(runs=[(what, {})], size=10)], size=12, color="#ffffff", valign="m")
    panel(s, x, y0 + 0.62, pxw, 1.6)
    bullets(s, x + 0.08, y0 + 0.72, pxw - 0.16, 1.62, items, size=10.5, after=4)
s.text(L, 4.38, CW, 0.3, "Triggers agreed in advance", size=12, bold=True)
tc = [L, L + 2.4, L + 6.5]
tw = [2.3, 4.0, CW - 6.5 + L - L]
tw[2] = R - tc[2]
y = 4.72
s.rect(L, y, CW, 0.34, "#0f2c4f")
for i, h in enumerate(["Customer group", "Signal", "Action"]):
    s.text(tc[i] + 0.08, y, tw[i], 0.34, h, size=10.5, bold=True, color="#ffffff", valign="m")
y += 0.34
trig = [("Mid-market", "Monthly logo churn above 1.0% for a quarter (0.8% today)", "Pause further rises; review accounts of up to 200 seats"),
        ("SMB test", "Test group churns 0.5 pt or more a month above control", "No SMB list rise in H2; look at packaging against Inkwell instead"),
        ("Promotion cohort", "Churn not falling toward 2.1% by end of Q2", "Stop investing in the cohort; focus onboarding on new customers")]
for k, r in enumerate(trig):
    if k % 2 == 1:
        s.rect(L, y, CW, 0.42, PANEL)
    for i, c in enumerate(r):
        s.text(tc[i] + 0.08, y, tw[i] - 0.16, 0.42, c, size=10.5, bold=(i == 0), valign="m")
    y += 0.42
footer(s, "Thresholds are proposals derived from the break-even analysis (p. 8) and the 2023 SMB response (p. 7). "
          "The SMB test should be sized to detect a response twice the 2023 level, the point where an SMB rise stops paying.")
slides.append(s)

# 14 ---- Decisions -----------------------------------------------------
s = Slide(notes="Decision list.")
header(s, "Decisions needed",
       "Five decisions for the leadership team in December", 14)
dec = [("Mid-market", "Approve +10% on list price at renewal from January 2027, subject to notice periods, with Customer Success review of accounts of up to 200 seats."),
       ("Enterprise", "Approve renewal pricing of up to the 7% cap on capped contracts and a 10% target on uncapped contracts."),
       ("SMB", "Hold SMB list prices for H1 2027. Approve the Q1 +8% test on established customers and its go/no-go rule (extra churn under 0.5 pt a month)."),
       ("Promotion cohort", "Freeze the cohort’s prices for 2027. Fund the activation programme, measured against a holdout, with a target of ~2.1% monthly churn rather than “halving” SMB churn."),
       ("Board reporting", "Adopt one churn definition: logo and revenue churn by segment, with the promotion cohort shown separately.")]
y = 1.8
for i, (t, b) in enumerate(dec):
    s.oval(L, y + 0.05, 0.42, BLUE)
    s.text(L, y + 0.05, 0.42, 0.42, str(i + 1), size=13, bold=True, color="#ffffff", align="c", valign="m")
    s.text(L + 0.6, y, 2.2, 0.55, t, size=13, bold=True, valign="m")
    s.text(L + 2.85, y, R - L - 2.85, 0.6, b, size=12, valign="m")
    y += 0.72
s.line(L, y + 0.05, R, y + 0.05, GRID)
s.text(L, y + 0.2, CW, 0.3, "Open questions to close before the meeting", size=12, bold=True, color=BLUE_DK)
bullets(s, L, y + 0.55, CW, 1.2,
        ["Finance: new-customer bookings outlook (we need $1.5–2.6M of new ARR) and the definition behind the board’s “1.4% → 2.3%” churn figure",
         "Customer Success: why mid-market churn rose from 0.6% to 0.8%, and how much mid-market ARR sits in accounts of up to 200 seats",
         "Legal: notice periods for January renewals, and whether capped enterprise contracts allow price rises during their term"],
        size=11, after=4)
footer(s, SRC + ".")
slides.append(s)

# 15 ---- Appendix A1 -----------------------------------------------------
s = Slide(notes="Assumptions and calculations; all reproducible in work/calc.py.")
header(s, "Appendix A1",
       "Assumptions and calculations behind the estimates", 15)
ac = [L, L + 2.6, L + 7.6]
aw = [2.5, 4.9, R - (L + 7.6)]
y = 1.72
s.rect(L, y, CW, 0.34, "#0f2c4f")
for i, h in enumerate(["Item", "Calculation / assumption", "Basis in the pack"]):
    s.text(ac[i] + 0.08, y, aw[i], 0.34, h, size=10.5, bold=True, color="#ffffff", valign="m")
y += 0.34
arows = [
    ("Promotion-cohort churn", "(5,900 × 3.1% − 3,800 × 2.1%) ÷ 2,100 ≈ 4.9% a month; ~56% of SMB churners", "Table 1; §6. Mid-2026 counts used as weights"),
    ("Activation share of excess", "Low activators churn 3× others. Non-promotion: 0.72x + 0.28 × 3x = 2.1%, so x = 1.35%. Cohort at 41% activation: ~2.9%, i.e. ~0.8 of ~2.8 pt", "§6, §9 (“about three times”)"),
    ("CFO gross uplift", "SMB 21.0 × 12% + mid-market 41.0 × 85% × 12% + enterprise 9.6 × (60% × 7% + 40% × 12%) = $7.6M", "§8. Capped share assumed equal in the 2027 tranche"),
    ("SMB churn response", "2023: +8% gave +0.5 pt a month for six months, +0.1 pt after. Scaled linearly: +12% loses 5.4% of customers (~320); stress case 2× (~640)", "§8. Linear scaling and the 2× stress are our assumptions"),
    ("Mid-market churn response", "Loss of renewing ARR = 2.1% per 10 pts of price (planning) or 5% (stress), applied to 34.85M × (1 + price)", "2024 test: 23.1% vs 23.6% conversion; the test covered new sign-ups"),
    ("Enterprise churn response", "None assumed; rises negotiated within caps", "0.2% churn, 118% NRR"),
    ("Break-even loss", "A rise of p pays off unless it loses more than p ÷ (1 + p) of the ARR it applies to: 9.1% at 10%, 10.7% at 12%", "Arithmetic"),
    ("Growth bridge", "Target 86.0 × 1.15 = 98.9. Installed base at ARR-weighted NRR 109.3% adds 8.0; the rest comes from price and new customers", "§3, Table 1; assumes trailing NRR holds"),
    ("SMB H2 upside", "16.6M of established SMB ARR × 8% × half a year of renewals ≈ $0.7M gross ($1.3M full-year run-rate)", "Renewals assumed spread evenly"),
]
rh = 0.52
for k, r in enumerate(arows):
    if k % 2 == 1:
        s.rect(L, y, CW, rh, PANEL)
    for i, c in enumerate(r):
        s.text(ac[i] + 0.08, y, aw[i] - 0.16, rh, c, size=9.5, bold=(i == 0), color=INK if i < 2 else INK2, valign="m")
    y += rh
footer(s, SRC + ". All figures are reproducible from the pack; ARR effects are run-rate at the end of 2027.")
slides.append(s)

# 16 ---- Appendix A2 -----------------------------------------------------
s = Slide(notes="Dashboard reconciliation: customer-weighted 1.71% -> 2.62%; ARR-weighted 0.83% -> 1.19%.")
header(s, "Appendix A2",
       "Data issues to resolve: the board’s churn figure cannot be reproduced from segment data", 16)
s.text(L, 1.72, 6.5, 0.3, "Monthly churn, H1 2025 vs H1 2026, %", size=12, bold=True)
rowsx = [("Board dashboard (undefined)", "1.4", "2.3"),
         ("Customer-weighted, from Table 1", f"{C['cust_w'][0]:.1f}", f"{C['cust_w'][1]:.1f}"),
         ("ARR-weighted, from Table 1", f"{C['arr_w'][0]:.1f}", f"{C['arr_w'][1]:.1f}"),
         ("SMB excluding the promotion cohort", "2.0", "2.1")]
y = 2.1
s.rect(L, y, 6.5, 0.34, "#0f2c4f")
for xx, h in [(L + 0.08, "Measure"), (L + 4.3, "H1 2025"), (L + 5.4, "H1 2026")]:
    s.text(xx, y, 2.5, 0.34, h, size=10.5, bold=True, color="#ffffff", valign="m")
y += 0.34
for k, r in enumerate(rowsx):
    if k % 2 == 1:
        s.rect(L, y, 6.5, 0.42, PANEL)
    s.text(L + 0.08, y, 4.1, 0.42, r[0], size=11, bold=(k == 0), valign="m")
    s.text(L + 4.3, y, 1.0, 0.42, r[1], size=11, valign="m")
    s.text(L + 5.4, y, 1.0, 0.42, r[2], size=11, valign="m")
    y += 0.42
s.text(L, y + 0.15, 6.5, 1.2,
       "Neither weighting matches the dashboard, and a single blended number hides the story: the rise is concentrated in one cohort in one segment. "
       "We recommend reporting logo and revenue churn by segment, with the promotion cohort shown separately.",
       size=11, color=INK2)
px = 7.6
panel(s, px, 1.72, R - px, 3.75)
s.text(px + 0.2, 1.85, R - px - 0.4, 4.7,
       [dict(runs=[B("Other gaps in the evidence")], space_after=8),
        dict(runs=[B("Mid-market churn rise. "), ("It rose from 0.6% to 0.8% with no explanation in the pack. It needs checking before renewal notices go out.", {})], bullet=True, space_after=6),
        dict(runs=[B("Exit-survey coverage. "), ("Shares cover respondents only. As a check, mixing promotion and other churners gives ~37% citing price, vs 34% reported, which is broadly consistent.", {})], bullet=True, space_after=6),
        dict(runs=[B("Renewal response. "), ("The only mid-market test covered new sign-ups (uncertainty 3).", {})], bullet=True, space_after=6),
        dict(runs=[B("New-customer bookings. "), ("These are not in the pack, so the +15% bridge cannot be fully tested.", {})], bullet=True, space_after=6),
        dict(runs=[B("Contract terms. "), ("Notice periods, and whether capped contracts allow rises during their term.", {})], bullet=True)],
       size=10.5)
footer(s, SRC + ", Table 1, Table 2, §10–§11. Weighted averages use mid-2026 customer counts and ARR for both periods.")
slides.append(s)

# ======================================================================
if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "..", "deliverable")
    prev = os.path.join(here, "preview")
    os.makedirs(prev, exist_ok=True)
    warn = []
    ims = []
    for i, sl in enumerate(slides, 1):
        ims.append(render_png(sl, os.path.join(prev, f"s{i:02d}.png"), warn, i))
    render_pptx(slides, os.path.join(out, "Palisade_2027_Pricing_Recommendation.pptx"))
    ims[0].save(os.path.join(prev, "preview.pdf"), save_all=True, append_images=ims[1:], resolution=120)
    print("\n".join(warn) if warn else "no layout warnings")
