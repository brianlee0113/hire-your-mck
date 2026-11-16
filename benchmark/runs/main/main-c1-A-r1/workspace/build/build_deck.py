import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from canvas import Deck, INK, INK2, MUTED, GRID, BASE, OVERFLOWS, W, H
from pptx.enum.shapes import MSO_SHAPE
import model as M

OUT = sys.argv[1]; PREV = sys.argv[2]
os.makedirs(PREV, exist_ok=True)

# ---- palette (validated: slots 1-3 all-pairs) ----
CA, CB, CJ = '#2a78d6', '#eb6834', '#1baf7a'      # Option A, B, J
SLATE, LIGHT = '#33424f', '#c9c8c1'                # market data / de-emphasised
GOOD, BAD, WARN = '#0ca30c', '#d03b3b', '#fab219'
PANEL = '#f4f3ef'
BLUE_T, RED_T, AMB_T = '#dbe9fb', '#f8dcdb', '#fdf0d2'
L, R = 0.6, W - 0.6
CW = R - L

def money(v, d=1):
    s = f'{abs(v):.{d}f}'
    return ('−$' if v < 0 else '+$') + s + 'M'

# ---- model results ----
A, A_pk = M.option_a(); B, B_pk = M.option_b(); J, J_pk = M.option_j()
A32, A32_pk = M.option_a(.32); A28, A28_pk = M.option_a(.28)
A32T, A32T_pk = M.option_a(.32, .25)
STALL, STALL_pk = M.option_a(.32, .15, [200_000] * 4)
BR, BR_pk = M.option_b(acos=.32, upw=2.6, halo=1.0)
gmA, gmB, gmJ, gmA32 = M.group_margin(A), M.group_margin(B), M.group_margin(J), M.group_margin(A32)

d = Deck()

def frame(s, tracker, title, source, page=True):
    s.text(L, 0.34, 8, 0.25, tracker.upper(), size=10, bold=True, color=MUTED)
    s.text(L, 0.62, CW, 0.9, title, size=23, bold=True, color=INK, ls=1.12)
    s.line(L, 1.62, R, 1.62, BASE, 0.75)
    s.text(L, 6.98, CW - 0.8, 0.36, source, size=8.5, color=MUTED, ls=1.15)
    s.text(R - 0.6, 7.05, 0.6, 0.2, str(s.idx), size=9, color=MUTED, align='r')

def status(s, x, y, kind, label=None):
    col = {'pass': GOOD, 'fail': BAD, 'risk': WARN, 'partial': WARN}[kind]
    lab = label or {'pass': 'Pass', 'fail': 'Fail', 'risk': 'At risk', 'partial': 'Partial'}[kind]
    s.dot(x + 0.08, y + 0.11, 0.075, col, ring=None)
    s.text(x + 0.22, y, 1.4, 0.24, lab, size=11.5, bold=True, color=INK)

def yaxis(s, x0, x1, ymap, ticks, fmt, size=9.5, zero=None):
    for t in ticks:
        yy = ymap(t)
        s.line(x0, yy, x1, yy, BASE if t == zero else GRID, 1.0 if t == zero else 0.5)
        s.text(x0 - 0.62, yy - 0.09, 0.55, 0.2, fmt(t), size=size, color=MUTED, align='r')

def lin(lo, hi, top, bot):
    return lambda v: bot - (v - lo) / (hi - lo) * (bot - top)

def stat_tile(s, x, y, w, h, big, label, big_color=INK):
    s.rect(x, y, w, h, PANEL)
    s.text(x + 0.2, y + 0.14, w - 0.4, 0.55, big, size=26, bold=True, color=big_color)
    s.text(x + 0.2, y + 0.72, w - 0.4, h - 0.8, label, size=11, color=INK2, ls=1.2)

def takeaway(s, x, y, w, h, txt, size=12.5):
    s.rect(x, y, 0.06, h, INK)
    s.text(x + 0.2, y, w - 0.2, h, txt, size=size, color=INK, valign='m', ls=1.22)

# =====================================================================
# 1 Title
s = d.new()
s.rect(0, 0, 0.32, H, '#1f4d3a')
s.text(1.0, 1.0, 9, 0.3, 'ONSOO BOTANICALS · BOARD PAPER', size=11, bold=True, color=MUTED)
s.text(1.0, 1.9, 11.2, 1.9, 'US entry in 2027: go in through Amazon, and earn the way into specialty retail',
       size=36, bold=True, color=INK, ls=1.1)
s.text(1.0, 4.05, 10.5, 0.9, 'Should Onsoo enter the US market in 2027, and if so, by which route? '
       'Recommendation for CEO Park Ji-won and the board, March 2027 board meeting',
       size=16, color=INK2, ls=1.25)
s.line(1.0, 5.25, 5.0, 5.25, BASE, 0.75)
s.text(1.0, 5.45, 11, 0.9, ['Prepared November 2026 from the planning-team briefing pack only (no outside research).',
       'All company, competitor and market figures in the pack are synthetic benchmark data.'],
       size=11, color=MUTED, para_space=3)
s.notes('Deck built only from evidence/briefing-pack.md. Judgment calls made without client input are listed in the appendix.')

# =====================================================================
# 2 Executive summary
s = d.new()
frame(s, 'Executive summary', 'Enter the US in 2027 through Amazon. Do not launch 600 retail doors, '
      'and hold the Japan scale-up for a later year',
      'Source: briefing pack (Tables 1–9, survey Sep 2026); team model of planning-team inputs. ACoS = Amazon ad spend as a share of Amazon sales.')
s.rect(L, 1.85, CW, 0.95, PANEL)
s.text(L + 0.25, 1.85, CW - 0.5, 0.95,
       '**Recommendation:** approve Option A (Amazon-led) for 2027 with a $4M US cash envelope. Reject Option B '
       '(600-door retail launch) and defer Option J (Japan scale-up). Add specialty retail only once aided awareness passes 20%.',
       size=14.5, valign='m', ls=1.25)
cols = [
    ('The US is worth entering', [
        'US K-beauty skincare reached **$3.6B** in 2025, growing **17% a year** against 5% for all facial skincare',
        '**41%** of it sells on Amazon, and **61%** of K-beauty buyers buy there most often',
        'The pilot works: monthly units **+89%** in six months, **4.5 stars**, repeat close to benchmark (29% vs 31%)']),
    ('Only Amazon-led fits the board’s limits', [
        'Retail-led breaks the **$18M cap** (−$20.8M peak), never pays back and pulls group margin to **4.5%**, even on its own inputs',
        'Those inputs are optimistic: brands at Onsoo’s awareness sell **2.6 units/door/week**; the retailer removes brands below 4.0',
        'Amazon-led needs **$1.9–3.9M** of peak cash and keeps group margin at **9% or more**']),
    ('What the board has to accept', [
        'Payback by 2030 holds only if ACoS stays **at or below 28.6%**. At the 32% scaling benchmark it slips to about 2032',
        'No route reaches **$40M by 2030** within the limits. Option A reaches ~$26M; reset $40M as a 2031–32 milestone',
        'Guardrails on ad cost, cash and repeat purchase bring the decision back to the board early']),
]
cw = (CW - 0.5) / 3
for i, (hd, bl) in enumerate(cols):
    x = L + i * (cw + 0.25)
    s.text(x, 3.05, cw, 0.3, hd, size=13.5, bold=True, color=INK)
    s.line(x, 3.42, x + cw, 3.42, INK, 1.0)
    s.text(x, 3.58, cw, 3.25, [{'t': b, 'bullet': True} for b in bl], size=12.5, color=INK, ls=1.22, para_space=9)
s.notes('Answer first. Everything after this slide supports one of the three columns.')

# =====================================================================
# 3 Scorecard
s = d.new()
frame(s, 'The decision against the board’s tests', 'Only the Amazon-led route fits within the board’s limits. '
      'The retail-led route breaks three of them on its own numbers',
      'Note: planning-team inputs unless stated. “32% ACoS” = agency median for brands scaling $5M→$20M on Amazon US. (1) J excludes working capital (not given). '
      'Source: briefing pack Tables 4–7; team model.')
cx = [L, L + 2.75, L + 2.75 + 3.13, L + 2.75 + 6.26]; cwid = [2.6, 3.0, 3.0, 3.0]
heads = [('Board test', INK), ('A · Amazon-led', CA), ('B · Retail-led, 600 doors', CB), ('J · Japan scale-up', CJ)]
ty = 1.85
for i, (hname, col) in enumerate(heads):
    if i: s.rect(cx[i], ty + 0.36, cwid[i], 0.05, col)
    s.text(cx[i], ty, cwid[i], 0.32, hname, size=13, bold=True)
rows = [
    ('Ambition', 'US business “on the way to $40M by 2030”',
     [('partial', f'${A[-1]["rev"]:.1f}M US revenue in 2030, still growing ~30% a year'),
      ('partial', f'${B[-1]["rev"]:.1f}M in 2030 on paper, but only by breaking three limits'),
      ('fail', f'No US business. Adds ${J[-1]["rev"]:.1f}M of Japan revenue by 2030')]),
    ('Investment cap', 'Peak cumulative cash outflow ≤ $18M',
     [('pass', f'Peak {money(A_pk)} ({money(A32_pk)} at 32% ACoS)'),
      ('fail', f'Peak {money(B_pk)}, and still falling in 2030'),
      ('pass', f'Peak {money(J_pk, 2)}(1)')]),
    ('Payback', 'Cumulative cash back to zero by end-2030',
     [('risk', f'{money(A[-1]["cum"])} at 25% ACoS, but {money(A32[-1]["cum"])} at 32% ACoS'),
      ('fail', f'{money(B[-1]["cum"])} at end-2030. Operating loss every year'),
      ('pass', f'{money(J[-1]["cum"])} by end-2030(1)')]),
    ('Group margin floor', 'Operating margin ≥ 8% every year',
     [('pass', f'Lowest year {min(gmA):.1%} ({min(gmA32):.1%} at 32% ACoS)'),
      ('fail', f'{gmB[0]:.1%} / {gmB[1]:.1%} / {gmB[2]:.1%} in 2027–29'),
      ('pass', f'Lowest year {min(gmJ):.1%}')]),
    ('Bandwidth', 'One major launch in 2027',
     [('pass', 'Uses the 2027 slot. Japan waits'),
      ('pass', 'Uses the slot, plus a field team and 600 door launches'),
      ('pass', 'Uses the 2027 slot. The US waits')]),
]
rh = 0.86; y = ty + 0.55
for name, sub, cells in rows:
    s.line(L, y, R, y, GRID, 0.75)
    s.text(cx[0], y + 0.12, cwid[0], 0.25, name, size=12.5, bold=True)
    s.text(cx[0], y + 0.4, cwid[0], 0.42, sub, size=10.5, color=INK2, ls=1.15)
    for i, (k, t) in enumerate(cells):
        if k == 'fail': s.rect(cx[i + 1] - 0.08, y + 0.04, cwid[i + 1] + 0.04, rh - 0.08, RED_T)
        status(s, cx[i + 1], y + 0.12, k)
        s.text(cx[i + 1], y + 0.4, cwid[i + 1] - 0.1, 0.44, t, size=10.5, color=INK, ls=1.15)
    y += rh
s.line(L, y, R, y, GRID, 0.75)

# =====================================================================
# 4 Market
s = d.new()
frame(s, 'Why the US', 'The US prize is K-beauty skincare: $3.6B in 2025 and growing about 17% a year, '
      'more than three times as fast as the category',
      'Source: briefing pack Table 1 (US facial skincare sales, $B); trade-press article (2026). Growth = compound annual rate 2021–25.')
kb = [1.9, 2.3, 2.7, 3.1, 3.6]; tot = [20.1, 21.3, 22.6, 23.5, 24.5]
rest = [t - k for t, k in zip(tot, kb)]
ik = [v / kb[0] * 100 for v in kb]; ir = [v / rest[0] * 100 for v in rest]
gx0, gx1, gy0, gy1 = L + 0.7, L + 6.3, 2.35, 6.2
s.text(L, 1.85, 7.2, 0.3, 'US facial skincare sales, indexed (2021 = 100)', size=12, bold=True)
ym = lin(80, 200, gy0, gy1)
yaxis(s, gx0, gx1, ym, [80, 100, 120, 140, 160, 180, 200], lambda t: f'{t}', zero=None)
xs = [gx0 + 0.3 + i * (gx1 - gx0 - 0.6) / 4 for i in range(5)]
for i, yr in enumerate(range(2021, 2026)):
    s.text(xs[i] - 0.3, gy1 + 0.08, 0.6, 0.2, str(yr), size=9.5, color=MUTED, align='c')
for ser, col in [(ir, LIGHT), (ik, SLATE)]:
    for i in range(4): s.line(xs[i], ym(ser[i]), xs[i + 1], ym(ser[i + 1]), col, 2.25)
    for i in range(5): s.dot(xs[i], ym(ser[i]), 0.05, col)
s.text(gx1 + 0.1, ym(ik[-1]) - 0.2, 1.3, 0.45, [f'**K-beauty brands** {ik[-1]:.0f}'], size=10.5, color=INK, ls=1.15)
s.text(gx1 + 0.1, ym(ir[-1]) - 0.2, 1.3, 0.45, [f'**All other brands** {ir[-1]:.0f}'], size=10.5, color=INK, ls=1.15)
tx = L + 8.0; tw = R - tx
stat_tile(s, tx, 1.85, tw, 1.2, '$3.6B', f'K-beauty skincare sales in 2025: 14.7% of a $24.5B category, up from 9.5% in 2021')
stat_tile(s, tx, 3.2, tw, 1.2, '17% a year', 'K-beauty growth 2021–25, against 5% for the category and 3.5% for all other brands')
stat_tile(s, tx, 4.55, tw, 1.2, '1.1%', 'Share of 2025 K-beauty skincare sales that the $40M ambition represents')
s.text(tx, 5.95, tw, 0.9, '**Not comparable:** the trade-press “$5.2B US K-beauty market” includes makeup and hair care. '
       'We use the $3.6B skincare figure throughout.', size=10.5, color=INK2, ls=1.2)

# =====================================================================
# 5 Channels
s = d.new()
frame(s, 'Where the brand gets built', 'US K-beauty buyers shop and discover online. Amazon and TikTok, '
      'not the store, are where a new brand gets found',
      'Source: briefing pack Table 2 (channel shares of US K-beauty skincare sales, 2025); survey of 1,200 US women 18–44, Sep 2026 (K-beauty buyer sub-sample).')
panels = [
    ('Share of US K-beauty skincare sales, 2025', [('Amazon', 41), ('Specialty beauty retail', 27), ('Mass retail', 14), ('Brand websites', 12), ('Other', 6)]),
    ('K-beauty buyers: where they buy most often', [('Amazon', 61), ('Specialty beauty retail', 22)]),
    ('K-beauty buyers: where they found their last new brand', [('TikTok', 38), ('In a store', 17)]),
]
pw = (CW - 0.6) / 3
for pi, (ttl, rowsd) in enumerate(panels):
    x = L + pi * (pw + 0.3)
    s.text(x, 1.85, pw, 0.5, ttl, size=12, bold=True, ls=1.15)
    lab_w = 1.55; bx = x + lab_w + 0.1; bmax = pw - lab_w - 0.55
    for ri, (lab, v) in enumerate(rowsd):
        yy = 2.55 + ri * 0.52
        s.text(x, yy + 0.02, lab_w, 0.4, lab, size=10.5, color=INK, align='r', ls=1.1, valign='m')
        col = SLATE if ri == 0 else LIGHT
        s.rect(bx, yy + 0.08, bmax * v / 65, 0.3, col)
        s.text(bx + bmax * v / 65 + 0.06, yy + 0.12, 0.6, 0.22, f'{v}%', size=10.5, bold=(ri == 0))
    s.line(bx, 2.5, bx, 2.55 + len(rowsd) * 0.52, BASE, 0.75)
takeaway(s, L, 5.45, CW, 1.25,
         '**Implication:** build awareness where buyers already are: Amazon for purchase, TikTok and influencers for discovery. '
         'Price matters too: 52% of K-beauty triers name “price compared with US brands” as a reason, which favours the $24 Amazon price over a $28 shelf price.',
         size=13)

# =====================================================================
# 6 Pilot
s = d.new()
frame(s, 'Proof of demand', 'The Amazon pilot shows growing demand: monthly units nearly doubled in six months at 4.5 stars',
      'Source: briefing pack section 6 (Amazon pilot Jan–Jun 2026, three SKUs, cross-border seller); Table 5 (2027 forecast).')
units = [7400, 8600, 10100, 11800, 12900, 14000]; mons = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
s.text(L, 1.85, 6.8, 0.3, 'Pilot units sold per month, 2026 (thousands)', size=12, bold=True)
gx0, gx1, gy0, gy1 = L + 0.55, L + 6.6, 2.45, 5.6
ym = lin(0, 16, gy0, gy1)
yaxis(s, gx0, gx1, ym, [0, 4, 8, 12, 16], lambda t: f'{t}', zero=0)
bw = 0.62; step = (gx1 - gx0) / 6
for i, u in enumerate(units):
    bx = gx0 + i * step + (step - bw) / 2
    s.rect(bx, ym(u / 1000), bw, ym(0) - ym(u / 1000), SLATE)
    s.text(bx - 0.2, ym(u / 1000) - 0.26, bw + 0.4, 0.22, f'{u / 1000:.1f}', size=10.5, align='c', bold=(i in (0, 5)))
    s.text(bx - 0.2, gy1 + 0.08, bw + 0.4, 0.2, mons[i], size=10, color=MUTED, align='c')
    if i: s.text(bx - 0.2, gy1 + 0.3, bw + 0.4, 0.2, f'+{(u / units[i - 1] - 1) * 100:.0f}%', size=9.5, color=INK2, align='c')
s.text(gx0 - 0.6, gy1 + 0.3, 0.75, 0.2, 'vs prior', size=9, color=MUTED, align='r')
s.text(L, 6.15, 6.6, 0.7, '**2027 plan needs more:** 300k units = 25k a month, 1.8× the June run-rate. It relies on four new SKUs, '
       'and monthly growth slowed from 16–17% (Feb–Apr) to 8–9% (May–Jun).', size=11, color=INK2, ls=1.2)
tx = L + 7.2; tw2 = (R - tx - 0.2) / 2
tiles = [('4.5 / 5', 'Rating across 2,140 reviews'),
         ('28%', 'Ad cost of sales (ACoS) over the pilot, on a small budget'),
         ('29%', '90-day repeat. First-year US benchmark 31%; Onsoo Korea 48%'),
         ('6%', 'of reviews flag Korean-only labels. US labels are in the setup budget')]
for i, (b, l) in enumerate(tiles):
    stat_tile(s, tx + (i % 2) * (tw2 + 0.2), 1.85 + (i // 2) * 2.05, tw2, 1.85, b, l)
s.text(tx, 6.0, R - tx, 0.4, f'Pilot sales: 64,800 units, about ${64800 * 24 / 1e6:.2f}M at the $24 selling price.',
       size=11, color=INK2)

# =====================================================================
# 7 Unit economics
s = d.new()
frame(s, 'Unit economics', 'An Amazon unit earns $4.73 at the planned 25% ad cost but only $3.05 at the 32% benchmark. '
      'Retail earns more per unit but carries far more fixed cost',
      'Source: briefing pack Table 4 (Rice Ferment Barrier Cream, per unit, applied to all SKUs as the planning team does), Table 6; agency ACoS benchmark (section 11).')

def waterfall(s, x0, x1, items, total_label, title, top=2.55, bot=5.75, vmax=24):
    s.text(x0, 1.85, x1 - x0, 0.3, title, size=12, bold=True)
    ym = lin(0, vmax, top, bot)
    s.line(x0, ym(0), x1, ym(0), BASE, 0.75)
    n = len(items) + 1; step = (x1 - x0) / n; bw = step * 0.62
    run = 0
    for i, (lab, v) in enumerate(items + [(total_label, None)]):
        bx = x0 + i * step + (step - bw) / 2
        if i == 0:
            run = v; s.rect(bx, ym(v), bw, ym(0) - ym(v), SLATE); txt = f'${v:.2f}'; ty_ = ym(v) - 0.24
        elif v is None:
            s.rect(bx, ym(run), bw, ym(0) - ym(run), CA if 'Amazon' in title else CB); txt = f'${run + 1e-6:.2f}'; ty_ = ym(run) - 0.24
        else:
            s.rect(bx, ym(run), bw, ym(run - v) - ym(run), LIGHT); txt = f'−{v:.2f}'
            ty_ = ym(run - v) + 0.04; run -= v
            s.line(bx - (step - bw), ym(run + v), bx, ym(run + v), BASE, 0.5)
        s.text(bx - 0.25, ty_, bw + 0.5, 0.2, txt, size=9.5, align='c', bold=(i == 0 or v is None))
        lx, lw_ = bx - (step - bw) / 2, step
        if i == 0: lx, lw_ = lx - 0.3, lw_ + 0.6
        if i == n - 1: lw_ = lw_ + 0.35
        s.text(lx, bot + 0.08, lw_, 0.62, lab, size=8.5, color=INK2, align='l' if i == n - 1 else 'c', ls=1.12)
    return ym

waterfall(s, L, L + 4.9, [('Price', 24.0), ('Referral fee 15%', 3.60), ('FBA fee', 5.10), ('Product', 3.50),
                         ('Freight', 0.55), ('Duty 15%', 0.525), ('Ads at 25% ACoS', 6.00)], 'Contribution',
          'Amazon, $ per unit')
s.text(L, 6.5, 4.9, 0.4, 'At 32% ACoS, ads cost $7.68 and contribution falls to **$3.05** (−36%).', size=10.5, color=INK2)
waterfall(s, L + 5.4, L + 9.3, [('Wholesale', 14.0), ('Product', 3.50), ('Freight', 0.75), ('Duty 15%', 0.525),
                                 ('Co-op 8%', 1.12), ('Returns 4%', 0.56)], 'Contribution',
          'Specialty retail, $ per unit')
tx = L + 9.8; tw = R - tx
s.text(tx, 1.85, tw, 0.3, 'Retail’s fixed-cost problem', size=12, bold=True)
s.text(tx, 2.3, tw, 4.5, [
    {'t': 'Option B adds **$7.5M a year** of fixed cost: national marketing $6.0M and field sales $1.5M'},
    {'t': 'Covering it at $7.55 a unit takes **~994k retail units a year**: about **4,250 doors** at 4.5 units/door/week'},
    {'t': 'The plan has **600 doors** in 2027, selling 140k units'},
    {'t': 'Ads are the largest controllable Amazon cost: **each point of ACoS = $0.24 a unit**'}],
    size=11.5, ls=1.22, para_space=10)

# =====================================================================
# 8 B fails
s = d.new()
frame(s, 'Option B on its own numbers', 'Even on the planning team’s inputs, the retail-led route breaks the $18M cap, '
      'never pays back and takes group margin below 8% for three years',
      'Source: team model of planning-team inputs (Tables 4–7): 25% ACoS, 4.5 units/door/week, 1.3× Amazon halo; inventory = 4 months of landed cost. J excludes working capital.')
s.text(L, 1.85, 7.5, 0.3, 'Cumulative US (or Japan) cash flow from launch, $M', size=12, bold=True)
gx0, gx1, gy0, gy1 = L + 0.6, L + 6.4, 2.35, 6.3
ym = lin(-24, 4, gy0, gy1)
yaxis(s, gx0, gx1, ym, [-24, -20, -16, -12, -8, -4, 0, 4], lambda t: f'{t}', zero=0)
xs = [gx0 + 0.15 + i * (gx1 - gx0 - 0.3) / 4 for i in range(5)]
for i, lab in enumerate(['Start', '2027', '2028', '2029', '2030']):
    s.text(xs[i] - 0.3, gy1 + 0.08, 0.6, 0.2, lab, size=9.5, color=MUTED, align='c')
s.line(gx0, ym(-18), gx1, ym(-18), BAD, 1.25, dash=True)
s.text(gx0 + 0.05, ym(-18) - 0.25, 2.5, 0.2, 'Board cap: −$18M', size=10, bold=True, color=BAD)
for rows_, col, nm in [(J, CJ, 'J'), (A, CA, 'A'), (B, CB, 'B')]:
    pts = [0] + [r['cum'] for r in rows_]
    for i in range(4): s.line(xs[i], ym(pts[i]), xs[i + 1], ym(pts[i + 1]), col, 2.25)
    for i in range(5): s.dot(xs[i], ym(pts[i]), 0.055, col)
s.text(gx1 + 0.08, ym(A[-1]['cum']) - 0.32, 1.4, 0.3, f'**A** {money(A[-1]["cum"])}', size=10.5)
s.text(gx1 + 0.08, ym(J[-1]['cum']) - 0.04, 1.4, 0.3, f'**J** {money(J[-1]["cum"])}', size=10.5)
s.text(gx1 + 0.08, ym(B[-1]['cum']) - 0.1, 1.4, 0.3, f'**B** {money(B[-1]["cum"])}', size=10.5)
tx = L + 8.15; tw = R - tx
s.text(tx, 1.85, tw, 0.3, 'Group operating margin (floor 8%)', size=12, bold=True)
colx = [tx, tx + 1.2, tx + 1.95, tx + 2.7, tx + 3.45]
for i, h_ in enumerate(['', '2027', '2028', '2029', '2030']):
    s.text(colx[i], 2.3, 0.7, 0.22, h_, size=10, color=MUTED, bold=True, align='r' if i else 'l')
for ri, (nm, gm, col) in enumerate([('A Amazon', gmA, CA), ('B Retail', gmB, CB), ('J Japan', gmJ, CJ)]):
    yy = 2.62 + ri * 0.42
    s.rect(tx, yy + 0.05, 0.1, 0.22, col)
    s.text(tx + 0.17, yy + 0.04, 1.1, 0.25, nm, size=10.5, bold=True)
    for i, v in enumerate(gm):
        if v < 0.08: s.rect(colx[i + 1] - 0.05, yy, 0.75, 0.34, RED_T)
        s.text(colx[i + 1], yy + 0.05, 0.65, 0.25, f'{v:.1%}', size=10.5, align='r', bold=v < 0.08)
s.text(tx, 4.05, tw, 0.3, 'Why the numbers do not work', size=12, bold=True)
inc = [b['op'] - a['op'] for a, b in zip(A, B)]
s.text(tx, 4.45, tw, 2.4, [
    {'t': 'Versus A, B adds **$7.5M a year** of fixed cost plus **$1.2M** of launch fee and fixtures', 'bullet': True},
    {'t': 'In return its retail leg earns **$1.1–1.8M** a year and the assumed Amazon halo **$0.4–1.6M**', 'bullet': True},
    {'t': f'Net: B’s operating profit is **${-inc[-1]:.1f}–{-inc[0]:.1f}M a year below A’s** in every year to 2030', 'bullet': True}],
    size=11.5, ls=1.2, para_space=7)

# =====================================================================
# 9 B inputs optimistic
s = d.new()
frame(s, 'Option B’s inputs', 'And B’s inputs are optimistic: at Onsoo’s awareness, newcomer brands sell about 2.6 units per door a week, '
      'well below the 4.0 the retailer requires',
      'Source: briefing pack Table 8 (retail analytics firm, 2025, 46 brands); survey Sep 2026; Table 9; board-member memo. '
      'Awareness measured among category buyers (all facial-skincare buyers), the base Table 8 uses.')
s.text(L, 1.85, 6.8, 0.3, 'First-year units per door per week, by brand awareness', size=12, bold=True)
gx0, gx1, gy0, gy1 = L + 0.5, L + 6.4, 2.45, 5.75
ym = lin(0, 6, gy0, gy1)
yaxis(s, gx0, gx1, ym, [0, 1, 2, 3, 4, 5, 6], lambda t: f'{t}', zero=0)
bands = [('Below 10%', 2.6, 1.9, 3.4), ('10–20%', 3.5, 2.8, 4.3), ('Above 20%', 4.6, 3.9, 5.5)]
step = (gx1 - gx0) / 3; bw = 0.75
for i, (lab, med, lo, hi) in enumerate(bands):
    cx_ = gx0 + i * step + step / 2
    s.rect(cx_ - bw / 2, ym(med), bw, ym(0) - ym(med), SLATE if i == 0 else LIGHT)
    s.line(cx_, ym(hi), cx_, ym(lo), INK, 1.25); s.line(cx_ - 0.12, ym(hi), cx_ + 0.12, ym(hi), INK, 1.25)
    s.line(cx_ - 0.12, ym(lo), cx_ + 0.12, ym(lo), INK, 1.25)
    s.text(cx_ - bw / 2, ym(0) - 0.32, bw, 0.22, f'{med}', size=11, bold=True, align='c', color='#ffffff' if i == 0 else INK)
    s.text(cx_ - step / 2, gy1 + 0.08, step, 0.22, lab, size=10, color=INK2, align='c')
s.text(gx0 + step / 2 - 1.2, gy1 + 0.32, 2.4, 0.4, '**Onsoo today: 4%** (9% among K-beauty buyers)', size=10, align='c', ls=1.1)
s.text(gx0 - 0.5, gy1 + 0.75, 6.4, 0.22, 'Bars = median; whiskers = interquartile range. Awareness = aided, among category buyers.', size=9, color=MUTED)
s.line(gx0, ym(4.0), gx1, ym(4.0), BAD, 1.25, dash=True)
s.text(gx0 + 0.05, ym(4.0) + 0.02, 4.2, 0.2, 'Retailer removes brands below 4.0 after 12 months', size=9.5, bold=True, color=BAD)
s.line(gx0, ym(4.5), gx1, ym(4.5), CB, 1.5)
s.text(gx0 + 0.05, ym(4.5) - 0.23, 3.0, 0.2, 'Option B assumes 4.5', size=9.5, bold=True, color=INK)
tx = L + 7.15; tw = R - tx
blocks = [
    ('Sell-through: 4.5 is a top-band number', 'It comes from the retailer’s deck on successful newcomers. Even the top quartile of brands at <10% awareness (3.4) falls short of 4.0, so Onsoo would likely be removed after its first year.'),
    ('Halo: correlation, not cause', 'The 0.71 link between doors and Amazon sales can run the other way: retailers add brands that already sell. Saebom built ~$30M on Amazon first, then added 300 doors in 2025.'),
    ('Precedent: Mooncrest', 'Retail-first in 450 doors in 2023, removed from shelves in 2025, est. $21M US loss, more than Onsoo’s whole $18M cap.'),
]
yy = 1.85
for hd, body in blocks:
    s.text(tx, yy, tw, 0.28, hd, size=12, bold=True)
    used = s.text(tx, yy + 0.32, tw, 1.05, body, size=11, color=INK2, ls=1.2)
    yy += 0.32 + used + 0.22
takeaway(s, tx, 5.95, tw, 0.85, f'With 2.6 units, no halo and 32% ACoS, B’s cumulative cash reaches **{money(BR_pk, 0)}** by 2030, even if it is never removed from shelves.', size=11.5)

# =====================================================================
# 10 A sensitivity
s = d.new()
frame(s, 'Option A’s key risk', 'Option A pays back by 2030 only if ad cost stays at or below 28.6% of sales. '
      'Above that, payback slips, but the cash at risk stays small',
      'Source: team model; pilot ACoS 28% (section 6); agency benchmark: median ACoS 32% (range 26–38%) for brands scaling $5M→$20M on Amazon US (section 11); tariff review (section 13).')
s.text(L, 1.85, 6.4, 0.3, 'Option A cumulative cash flow by ad cost (ACoS), $M', size=12, bold=True)
gx0, gx1, gy0, gy1 = L + 0.55, L + 5.6, 2.35, 6.2
ym = lin(-4, 3, gy0, gy1)
yaxis(s, gx0, gx1, ym, [-4, -3, -2, -1, 0, 1, 2, 3], lambda t: f'{t}', zero=0)
xs = [gx0 + 0.15 + i * (gx1 - gx0 - 0.3) / 4 for i in range(5)]
for i, lab in enumerate(['Start', '2027', '2028', '2029', '2030']):
    s.text(xs[i] - 0.3, gy1 + 0.08, 0.6, 0.2, lab, size=9.5, color=MUTED, align='c')
for rows_, col, nm in [(A, '#86b6ef', '25% (plan)'), (A28, '#2a78d6', '28% (pilot)'), (A32, '#104281', '32% (benchmark)')]:
    pts = [0] + [r['cum'] for r in rows_]
    for i in range(4): s.line(xs[i], ym(pts[i]), xs[i + 1], ym(pts[i + 1]), col, 2.25)
    for i in range(5): s.dot(xs[i], ym(pts[i]), 0.055, col)
    s.text(gx1 + 0.05, ym(pts[-1]) - 0.11, 1.9, 0.24, f'**{nm}** {money(pts[-1])}', size=9.5)
tx = L + 7.35; tw = R - tx
s.text(tx, 1.85, tw, 0.3, 'Cumulative cash at end-2030, $M', size=12, bold=True)
acs = [.25, .28, .30, .32, .35, .38]; duties = [.15, .25]
s.text(tx, 2.27, 1.3, 0.22, 'ACoS', size=10, bold=True, color=MUTED)
s.text(tx + 1.3, 2.27, 1.4, 0.22, 'Duty 15% (today)', size=10, bold=True, color=MUTED, align='c')
s.text(tx + 2.75, 2.27, 1.4, 0.22, 'Duty 25% (review)', size=10, bold=True, color=MUTED, align='c')
for ri, ac in enumerate(acs):
    yy = 2.58 + ri * 0.38
    lab = {.25: '25% plan', .28: '28% pilot', .32: '32% benchmark', .38: '38% top of range'}.get(ac, f'{ac:.0%}')
    s.text(tx, yy + 0.07, 1.3, 0.22, lab, size=10.5)
    for ci, du in enumerate(duties):
        r_, pk = M.option_a(ac, du); v = r_[-1]['cum']
        fill = BLUE_T if v >= 0 else (RED_T if v < -2 else '#fbeceb')
        s.rect(tx + 1.3 + ci * 1.45, yy, 1.35, 0.33, fill)
        s.text(tx + 1.3 + ci * 1.45, yy + 0.07, 1.35, 0.22, money(v), size=10.5, align='c', bold=v >= 0)
s.text(tx, 4.95, tw, 0.22, 'Blue = pays back by 2030. Red = does not.', size=9, color=MUTED)
s.text(tx, 5.3, tw, 1.55, [
    {'t': 'Break-even ACoS is **28.6%**, or **26.9%** if the duty rises to 25%. The pilot ran at 28%', 'bullet': True},
    {'t': 'The plan assumes ACoS falls to 25%; the benchmark says it **rises** with scale as click costs climb', 'bullet': True},
    {'t': 'In every case peak cash stays **≤ $7.5M** and group margin **≥ 8.7%**', 'bullet': True}],
    size=11, ls=1.2, para_space=5)

# =====================================================================
# 11 Downside asymmetry
s = d.new()
frame(s, 'Downside', 'If Amazon stalls the way it did for two peers, Option A loses about $7M. '
      'A retail-first failure costs three times that',
      'Source: team model; briefing pack Table 9 (public reporting and interviews). Stall case: 200k units a year (~$4.8M revenue, like Gaon Lab and Yeoreum) at 32% ACoS, fixed costs unchanged.')
s.text(L, 1.85, 7.6, 0.3, 'Peak cumulative cash need through 2030, $M', size=12, bold=True)
cases = [('A · plan (25% ACoS)', -A_pk, CA), ('A · 32% ACoS', -A32_pk, CA), ('A · 32% ACoS + 25% duty', -A32T_pk, CA),
         ('A · stalls below $5M', -STALL_pk, CA), ('B · plan inputs', -B_pk, CB),
         ('Mooncrest · actual (est. loss)', 21.0, MUTED), ('B · realistic inputs', -BR_pk, CB)]
lab_w = 2.45; bx0 = L + lab_w + 0.12; bmax = 4.6; sc = bmax / 32
for i, (lab, v, col) in enumerate(cases):
    yy = 2.4 + i * 0.55
    s.text(L, yy + 0.08, lab_w, 0.25, lab, size=10.5, align='r')
    s.rect(bx0, yy + 0.06, v * sc, 0.32, col)
    s.text(bx0 + v * sc + 0.07, yy + 0.1, 0.8, 0.22, f'${v:.1f}M', size=10.5, bold=True)
s.line(bx0, 2.35, bx0, 2.4 + 7 * 0.55, BASE, 0.75)
s.line(bx0 + 18 * sc, 2.3, bx0 + 18 * sc, 2.4 + 7 * 0.55, BAD, 1.25, dash=True)
s.text(bx0 + 18 * sc - 1.6, 6.3, 3.2, 0.22, 'Board cap $18M', size=10, bold=True, color=BAD, align='c')
s.text(L, 6.55, 7.4, 0.3, 'B realistic = 2.6 units/door/week, no halo, 32% ACoS.', size=9, color=MUTED)
tx = L + 8.0; tw = R - tx
s.text(tx, 1.85, tw, 0.3, 'Recent K-beauty entrants', size=12, bold=True)
peers = [('Saebom', 'Amazon-first 2022', '~$30M revenue in 2025; added 300 doors'),
         ('Gaon Lab', 'Amazon-first 2022', 'Below $5M in 2025'),
         ('Yeoreum', 'Amazon-first 2023', 'Below $5M in 2025'),
         ('Mooncrest', 'Retail-first 2023, 450 doors', 'Removed in 2025; est. $21M loss')]
for i, (n, rt, oc) in enumerate(peers):
    yy = 2.3 + i * 0.72
    s.line(tx, yy, R, yy, GRID, 0.75)
    s.text(tx, yy + 0.08, 1.15, 0.25, n, size=11, bold=True)
    s.text(tx + 1.2, yy + 0.08, tw - 1.2, 0.25, rt, size=10.5, color=INK2)
    s.text(tx + 1.2, yy + 0.35, tw - 1.2, 0.25, oc, size=10.5)
s.line(tx, 2.3 + 4 * 0.72, R, 2.3 + 4 * 0.72, GRID, 0.75)
takeaway(s, tx, 5.35, tw, 1.45, 'Amazon-first does not guarantee scale: two of three peers stayed below $5M. '
         'But that failure is cheap and shows early, so it can be stopped. The retail-first failure cost more than Onsoo’s whole cap.', size=11.5)

# =====================================================================
# 12 Japan
s = d.new()
frame(s, 'The alternative: Japan', 'The Japan scale-up is safe but small: $7M of added revenue by 2030, '
      'in a market growing 1.5% a year, and it leaves the US untouched',
      'Source: briefing pack Table 7, group context, section 8; team model. J excludes working capital (not given). Growth rates: K-beauty US 2021–25 CAGR; Japan facial skincare per pack.')
s.text(L, 1.85, 6.4, 0.3, 'Added revenue by year, $M', size=12, bold=True)
gx0, gx1, gy0, gy1 = L + 0.5, L + 6.0, 2.45, 6.0
ym = lin(0, 30, gy0, gy1)
yaxis(s, gx0, gx1, ym, [0, 10, 20, 30], lambda t: f'{t}', zero=0)
step = (gx1 - gx0) / 4; bw = 0.42
for i, yr in enumerate(YEARS := [2027, 2028, 2029, 2030]):
    c = gx0 + i * step + step / 2
    for k, (val, col) in enumerate([(A[i]['rev'], CA), (J[i]['rev'], CJ)]):
        bx = c - bw - 0.02 + k * (bw + 0.04)
        s.rect(bx, ym(val), bw, ym(0) - ym(val), col)
        s.text(bx - 0.15, ym(val) - 0.24, bw + 0.3, 0.2, f'{val:.1f}', size=9.5, align='c')
    s.text(c - 0.4, gy1 + 0.08, 0.8, 0.2, str(yr), size=9.5, color=MUTED, align='c')
s.rect(gx0, 6.45, 0.16, 0.16, CA); s.text(gx0 + 0.22, 6.42, 2.2, 0.22, 'A · Amazon-led (US)', size=10)
s.rect(gx0 + 2.3, 6.45, 0.16, 0.16, CJ); s.text(gx0 + 2.52, 6.42, 2.2, 0.22, 'J · Japan scale-up', size=10)
tx = L + 6.85; tw = R - tx
c1, c2, c3 = tx, tx + 1.95, tx + 3.85
s.text(c2, 1.85, 1.85, 0.45, '**A · Amazon-led** (25% / 32% ACoS)', size=10.5, ls=1.1)
s.text(c3, 1.85, tw - 3.85, 0.45, '**J · Japan**', size=10.5, ls=1.1)
cmp_ = [('Revenue 2030', f'${A[-1]["rev"]:.1f}M', f'${J[-1]["rev"]:.1f}M'),
        ('Operating profit 2030', f'${A[-1]["op"]:.1f}M / ${A32[-1]["op"]:.1f}M', f'${J[-1]["op"]:.1f}M'),
        ('Cumulative cash to 2030', f'{money(A[-1]["cum"])} / {money(A32[-1]["cum"])}', f'{money(J[-1]["cum"])}'),
        ('Market growth', 'US K-beauty ~17%/yr', 'Japan facial ~1.5%/yr'),
        ('Starting position', 'New; pilot only', '3.1% share today')]
for i, (a_, b_, c_) in enumerate(cmp_):
    yy = 2.4 + i * 0.5
    s.line(tx, yy, R, yy, GRID, 0.75)
    s.text(c1, yy + 0.13, 1.9, 0.25, a_, size=10.5, bold=True)
    s.text(c2, yy + 0.13, 1.85, 0.25, b_, size=10.5)
    s.text(c3, yy + 0.13, tw - 3.85, 0.25, c_, size=10.5)
s.line(tx, 2.4 + 5 * 0.5, R, 2.4 + 5 * 0.5, GRID, 0.75)
takeaway(s, tx, 5.2, tw, 1.6, 'If ACoS runs at 32%, J returns more cash by 2030. But it adds only $7M of revenue and does nothing for the US ambition. '
         'A builds a $26M business still growing ~30% a year. Keep J on the list for 2028 or later, once the US team is running.', size=11.5)

# =====================================================================
# 13 Ambition
s = d.new()
frame(s, 'The $40M ambition', 'No route reaches $40M by 2030 within the board’s limits. '
      'Keep the limits and move the $40M milestone to about 2032',
      'Source: team model of Table 5 volumes. 2031–32 is an illustrative extension at +25% a year (below the plan’s +29% in 2030); it is not a planning-team forecast.')
s.text(L, 1.85, 7.0, 0.3, 'US revenue, $M', size=12, bold=True)
gx0, gx1, gy0, gy1 = L + 0.5, L + 6.8, 2.35, 6.3
ym = lin(0, 50, gy0, gy1)
yaxis(s, gx0, gx1, ym, [0, 10, 20, 30, 40, 50], lambda t: f'{t}', zero=0)
yrs = list(range(2027, 2033)); xs = [gx0 + 0.3 + i * (gx1 - gx0 - 0.6) / 5 for i in range(6)]
for i, yr in enumerate(yrs): s.text(xs[i] - 0.3, gy1 + 0.08, 0.6, 0.2, str(yr), size=9.5, color=MUTED, align='c')
s.line(gx0, ym(40), gx1, ym(40), INK, 1.0, dash=True)
s.text(gx0 + 0.05, ym(40) - 0.24, 2.0, 0.2, '$40M ambition', size=10, bold=True)
ar = [r['rev'] for r in A]; ext = [ar[-1] * 1.25, ar[-1] * 1.25 ** 2]; br = [r['rev'] for r in B]
for i in range(3): s.line(xs[i], ym(br[i]), xs[i + 1], ym(br[i + 1]), CB, 2.25)
for i in range(4): s.dot(xs[i], ym(br[i]), 0.055, CB)
for i in range(3): s.line(xs[i], ym(ar[i]), xs[i + 1], ym(ar[i + 1]), CA, 2.25)
s.line(xs[3], ym(ar[3]), xs[4], ym(ext[0]), CA, 2.0, dash=True); s.line(xs[4], ym(ext[0]), xs[5], ym(ext[1]), CA, 2.0, dash=True)
for i in range(4): s.dot(xs[i], ym(ar[i]), 0.055, CA)
for i in range(2): s.rect(xs[4 + i] - 0.055, ym(ext[i]) - 0.055, 0.11, 0.11, '#ffffff', line=CA, lw=1.5, shape=MSO_SHAPE.OVAL)
s.text(xs[3] + 0.12, ym(br[3]) - 0.1, 1.2, 0.22, f'**B** ${br[3]:.1f}M', size=10.5)
s.text(xs[3] + 0.1, ym(ar[3]) + 0.02, 1.2, 0.22, f'**A** ${ar[3]:.1f}M', size=10.5)
s.text(xs[5] - 1.85, ym(ext[1]) - 0.3, 1.7, 0.22, f'A extended ~${ext[1]:.0f}M', size=10.5, bold=True, align='r')
tx = L + 7.75; tw = R - tx
s.text(tx, 1.85, tw, 0.3, 'The choice for the board', size=12, bold=True)
opts = [('Keep “$40M in 2030”', 'Only B gets close ($37.6M), and only by breaking the cash cap, the payback test and the margin floor, on inputs that look optimistic.', BAD, 'Not recommended'),
        ('Keep the limits, move the date', 'A reaches ~$26M in 2030. At +25% a year it passes $40M around 2032, sooner if the retail gates (next page) are met.', GOOD, 'Recommended')]
yy = 2.3
for hd, body, col, tag in opts:
    s.rect(tx, yy, tw, 1.85, PANEL)
    s.dot(tx + 0.28, yy + 0.3, 0.075, col, ring=None)
    s.text(tx + 0.42, yy + 0.19, tw - 0.6, 0.25, f'{tag}', size=10.5, bold=True, color=INK2)
    s.text(tx + 0.2, yy + 0.52, tw - 0.4, 0.3, hd, size=12.5, bold=True)
    s.text(tx + 0.2, yy + 0.86, tw - 0.4, 0.95, body, size=11, color=INK2, ls=1.2)
    yy += 2.05

# =====================================================================
# 14 Retail gates
s = d.new()
frame(s, 'When to add retail', 'Add retail later, through tighter gates: awareness above 20% (not 15%) '
      'and a first step the group margin can absorb',
      'Source: briefing pack Table 8, Table 9, section 4 (CEO hypothesis), survey Sep 2026; team model (2030 headroom = group operating profit above 8% of revenue with Option A at 32% / 25% ACoS).')
cx = [L, L + 1.75, L + 3.75, L + 6.95]; cwid = [1.6, 1.85, 3.0, R - (L + 6.95)]
for i, h_ in enumerate(['Gate', 'CEO’s draft', 'Recommended', 'Why']):
    s.text(cx[i], 1.85, cwid[i], 0.25, h_, size=11, bold=True, color=MUTED)
gates = [
    ('Awareness', 'Aided awareness above 15%', '**20% or more** aided awareness among all facial-skincare buyers (today 4%)',
     'At 10–20% awareness newcomers sell a median 3.5 units/door/week (IQR 2.8–4.3): most fall below the 4.0 removal bar. Above 20% the median is 4.6.'),
    ('Amazon scale', 'Amazon sales above $10M', '**$20M or more** a year at ACoS of 30% or less',
     'Retail’s fixed costs need a profitable base. Saebom reached ~$30M before adding doors. On plan, A reaches $20M in 2029.'),
    ('First step', 'Not specified (board member proposes 600 doors nationally)', '**A test of ~300 doors**, with a budget below the margin headroom',
     'In 2030, group profit above the 8% floor is only $3.9–5.7M. B’s retail leg costs $4.4–7.2M a year more than A.'),
    ('Timing', 'From 2029', '**When the gates are met**, which means planning for 2030 at the earliest',
     'Awareness has to rise five-fold from 4%. Track it every six months from the 2027 launch.'),
]
yy = 2.2
for g, ceo, rec, why in gates:
    s.line(L, yy, R, yy, GRID, 0.75)
    s.text(cx[0], yy + 0.15, cwid[0], 0.5, g, size=12, bold=True)
    s.text(cx[1], yy + 0.15, cwid[1], 0.9, ceo, size=11, color=INK2, ls=1.18)
    s.rect(cx[2] - 0.08, yy + 0.06, cwid[2] + 0.06, 0.94, BLUE_T)
    s.text(cx[2], yy + 0.15, cwid[2] - 0.12, 0.85, rec, size=11, ls=1.18)
    s.text(cx[3], yy + 0.15, cwid[3], 0.85, why, size=10.5, color=INK2, ls=1.18)
    yy += 1.07
s.line(L, yy, R, yy, GRID, 0.75)

# =====================================================================
# 15 Decisions and guardrails
s = d.new()
frame(s, 'Decisions for the March 2027 board', 'Approve the Amazon-led launch with a $4M cash envelope '
      'and guardrails that bring the decision back to the board early',
      'Source: team analysis. The $4M envelope covers the 32% ACoS + 25% duty case (peak −$3.9M). The unit trigger matches the stall case on page 11. 2032 payback at 32% ACoS uses the illustrative +25%/yr extension (page 13).')
s.text(L, 1.85, 5.6, 0.3, 'Decisions requested', size=12.5, bold=True)
decs = ['**Enter the US in 2027 via the Amazon-led route.** No 600-door retail launch; no Japan scale-up in 2027',
        '**Authorise up to $4M of cumulative US cash outflow.** Any need beyond that returns to the board',
        '**Accept that 2030 payback is at risk.** On plan if ACoS ≤ 28.6%; at 32% ACoS, about 2032',
        '**Reset the ambition:** $40M as a 2031–32 milestone; add retail only through the gates on page 14']
yy = 2.3
for i, t in enumerate(decs):
    s.rect(L, yy + 0.02, 0.36, 0.36, INK)
    s.text(L, yy + 0.09, 0.36, 0.22, str(i + 1), size=12, bold=True, color='#ffffff', align='c')
    used = s.text(L + 0.5, yy, 5.1, 0.95, t, size=11.5, ls=1.2)
    yy += max(used, 0.4) + 0.28
tx = L + 6.1; tw = R - tx
s.text(tx, 1.85, tw, 0.3, 'Guardrails, reviewed quarterly', size=12.5, bold=True)
gc = [tx, tx + 1.85, tx + 3.4]; gw = [1.75, 1.5, tw - 3.4]
for i, h_ in enumerate(['Metric', 'Plan', 'Review trigger']):
    s.text(gc[i], 2.3, gw[i], 0.22, h_, size=10, bold=True, color=MUTED)
gr = [('Blended ACoS', '≤ 28%', 'Above 32% for two quarters in a row'),
      ('Cumulative US cash', '$1.9M peak on plan', 'Outflow passes $4M'),
      ('Amazon units', '300k in 2027', 'Below 200k annualised by Q4 2027'),
      ('90-day repeat', '≥ 31% benchmark', 'Still ≤ 29% after US labels and new SKUs'),
      ('US duty on Korean cosmetics', '15%', 'Rises to 25% (mid-2027 decision): re-plan, break-even ACoS 26.9%'),
      ('Aided awareness', 'Rising toward 20%', 'Surveyed every six months; feeds the retail gate')]
yy = 2.6
for m_, p_, t_ in gr:
    s.line(tx, yy, R, yy, GRID, 0.75)
    s.text(gc[0], yy + 0.08, gw[0], 0.45, m_, size=10.5, bold=True, ls=1.12)
    s.text(gc[1], yy + 0.08, gw[1], 0.45, p_, size=10.5, ls=1.12)
    s.text(gc[2], yy + 0.08, gw[2], 0.45, t_, size=10.5, ls=1.12)
    yy += 0.55
s.line(tx, yy, R, yy, GRID, 0.75)
s.rect(L, 6.05, CW, 0.78, PANEL)
s.text(L + 0.2, 6.05, CW - 0.4, 0.78, '**First moves in 2027:** set up the US entity and MoCRA registration · US-English labels (fixes the 6% complaint) · '
       'take the listings over from the cross-border seller · launch four new SKUs · hire the US team · first awareness survey in Q3',
       size=11, valign='m', ls=1.22)

# =====================================================================
# 16 Appendix: method
s = d.new()
frame(s, 'Appendix A · Method', 'How the options were modelled: the planning team’s inputs, applied consistently, '
      'with benchmark cases added', 'Source: briefing pack sections 6–8 and 13. All figures are synthetic benchmark data.')
colw = (CW - 0.4) / 2
s.text(L, 1.85, colw, 4.9, [
    {'t': '**Per-unit contribution** (hero product, applied to all SKUs as the planning team does)', 'size': 12},
    {'t': 'Amazon: $24.00 − 15% referral − $5.10 FBA − $3.50 product − $0.55 freight − 15% duty on product − ACoS × price = **$4.73** at 25% ACoS', 'bullet': True},
    {'t': 'Retail: $14.00 wholesale − $3.50 − $0.75 freight − $0.53 duty − 8% co-op − 4% returns = **$7.55**', 'bullet': True},
    {'t': 'Retail volume = doors × 4.5 units × 52 weeks; B Amazon units = A × 1.3', 'bullet': True},
    {'t': '**Costs and cash**', 'size': 12, 'space': 12},
    {'t': 'Fixed and one-time costs per Table 6; fixtures $1,100 for each new door in the year it opens', 'bullet': True},
    {'t': 'Inventory held = 4 months of that year’s landed cost (product + freight + duty); cash flow = operating profit − increase in inventory', 'bullet': True},
    {'t': 'Option J: revenue × 30% − $0.8M a year − $1.0M one-time; no working capital given, so none included', 'bullet': True},
], size=11, ls=1.2, para_space=5)
s.text(L + colw + 0.4, 1.85, colw, 4.9, [
    {'t': '**Board tests**', 'size': 12},
    {'t': 'Peak cash = lowest cumulative cash flow, 2027–30', 'bullet': True},
    {'t': 'Payback = cumulative cash ≥ 0 by end-2030', 'bullet': True},
    {'t': 'Group margin = (ex-US plan revenue × 11% + option operating profit) ÷ (ex-US revenue + option revenue)', 'bullet': True},
    {'t': '**Cases**', 'size': 12, 'space': 12},
    {'t': 'Plan: planning-team inputs (25% ACoS, 15% duty)', 'bullet': True},
    {'t': 'Benchmark: 32% ACoS, the agency median for $5M→$20M brands; range 26–38% tested', 'bullet': True},
    {'t': 'Tariff: duty 25% on product cost, applied to all four years (a conservative stress)', 'bullet': True},
    {'t': 'Not modelled: FX (a weaker won would help), tax, cost inflation, post-2030 terminal value', 'bullet': True},
], size=11, ls=1.2, para_space=5)

# =====================================================================
# 17 Appendix: financials
s = d.new()
frame(s, 'Appendix B · Financials', 'Option financials by year, $M (planning-team inputs; Option A also at the 32% ACoS benchmark)',
      'Source: team model. Operating profit is before group overheads already in the ex-US plan. Cash = operating profit − increase in inventory.')
blocks = [('A · Amazon-led, 25% ACoS', A, gmA, CA), ('A · Amazon-led, 32% ACoS', A32, gmA32, CA),
          ('B · Retail-led', B, gmB, CB), ('J · Japan scale-up', J, gmJ, CJ)]
colx = [L, L + 2.7, L + 4.0, L + 5.3, L + 6.6]
bw_ = (CW - 0.4) / 2
for bi, (nm, rows_, gm, col) in enumerate(blocks):
    x0 = L + (bi % 2) * (bw_ + 0.4); y0 = 1.85 + (bi // 2) * 2.5
    cxs = [x0, x0 + 1.95, x0 + 2.9, x0 + 3.85, x0 + 4.8]
    s.rect(x0, y0 + 0.05, 0.1, 0.22, col)
    s.text(x0 + 0.18, y0, 3.5, 0.3, nm, size=11.5, bold=True)
    for i, yr in enumerate(['', '2027', '2028', '2029', '2030']):
        s.text(cxs[i], y0 + 0.38, 0.9, 0.2, yr, size=9.5, bold=True, color=MUTED, align='r' if i else 'l')
    lines_ = [('Revenue', [r['rev'] for r in rows_]), ('Operating profit', [r['op'] for r in rows_]),
              ('Cash flow', [r['cash'] for r in rows_]), ('Cumulative cash', [r['cum'] for r in rows_]),
              ('Group op. margin', gm)]
    for li, (lab, vals) in enumerate(lines_):
        yy = y0 + 0.65 + li * 0.32
        s.line(x0, yy - 0.02, x0 + bw_, yy - 0.02, GRID, 0.5)
        s.text(cxs[0], yy + 0.04, 2.2, 0.22, lab, size=10, bold=(lab == 'Cumulative cash'))
        for i, v in enumerate(vals):
            t = f'{v:.1%}' if lab.startswith('Group') else f'{v:,.1f}'.replace('-', '−')
            s.text(cxs[i + 1], yy + 0.04, 0.9, 0.22, t, size=10, align='r', bold=(lab == 'Cumulative cash'),
                   color=BAD if (lab.startswith('Group') and v < 0.08) else INK)

# =====================================================================
# 18 Appendix: judgment calls
s = d.new()
frame(s, 'Appendix C · Judgment calls', 'Choices made without the CEO’s input, and how each affects the answer',
      'These were made in the absence of client input and should be confirmed before the board meeting.')
calls = [
    ('“On the way to $40M by 2030”', 'Read as a direction, not a hard limit. The four numeric limits (cap, payback, margin, bandwidth) are treated as binding.', 'If $40M in 2030 were binding, no option passes; B still breaks three limits.'),
    ('Awareness base', 'Onsoo’s awareness taken as 4% (all facial-skincare buyers), matching Table 8’s “category buyers”.', 'At 9% (K-beauty buyers) Onsoo is still in the lowest band; conclusion unchanged.'),
    ('Benchmark ACoS', '32% used as the main stress case, because A’s revenue path ($7M→$26M) matches the benchmark’s $5M→$20M brands.', 'Turns A’s payback from “pass” to “at risk”; cap and margin still pass.'),
    ('Tariff stress', 'A duty of 25% applied to all years, though a decision is due only in mid-2027.', 'Conservative; lowers break-even ACoS to 26.9%.'),
    ('$4M cash envelope', 'Set to cover the 32% ACoS + 25% duty case (peak $3.9M); our proposal, not a board figure.', 'Board may prefer a different number; the $18M cap is untouched.'),
    ('Retail gates', '20% awareness, $20M Amazon sales, ~300-door test: drawn from Table 8, Saebom and the margin headroom.', 'These are proposals for the board to confirm.'),
    ('2031–32 extension', '+25% a year after 2030, for illustration only.', 'Only affects when $40M is reached, not the 2027 decision.'),
]
cxs = [L, L + 2.55, L + 8.0]; cws = [2.4, 5.3, R - (L + 8.0)]
for i, h_ in enumerate(['Topic', 'Choice made', 'Effect on the answer']):
    s.text(cxs[i], 1.85, cws[i], 0.22, h_, size=10.5, bold=True, color=MUTED)
yy = 2.15
for a_, b_, c_ in calls:
    s.line(L, yy, R, yy, GRID, 0.75)
    s.text(cxs[0], yy + 0.08, cws[0], 0.55, a_, size=10.5, bold=True, ls=1.12)
    s.text(cxs[1], yy + 0.08, cws[1], 0.55, b_, size=10.5, ls=1.12)
    s.text(cxs[2], yy + 0.08, cws[2], 0.55, c_, size=10.5, color=INK2, ls=1.12)
    yy += 0.66
s.line(L, yy, R, yy, GRID, 0.75)

d.save(OUT, PREV)
print('saved', OUT, len(d.slides), 'slides')
print('\n'.join(OVERFLOWS) or 'no overflows')
