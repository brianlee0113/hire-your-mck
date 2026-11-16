from engine import Slide, Text, Rect, Line, W, H

NAVY = "0B2545"
INK = "1F1F1F"
INK2 = "52514E"
MUTED = "8A8985"
RULE = "C9C8C3"
PALE = "F3F2EF"
PALE_BLUE = "EAF2FC"
BLUE = "2A78D6"      # increases / positive / recommended
ORANGE = "EB6834"    # decreases / negative
SLATE = "4A5866"     # totals
GREEN = "1E7B34"
AMBER = "B57A00"
RED = "C53B3A"

SECTIONS = ["Diagnosis", "Options", "Plan", "First moves", "Risks & asks"]


def base(title, section=None, source=None, page=None):
    s = Slide()
    if section:
        # section tracker
        x = 0.5
        for i, nm in enumerate(SECTIONS):
            on = nm == section
            s.text(x, 0.22, 1.6, 0.25, f"{i+1}  {nm.upper()}", size=8, bold=on, color=NAVY if on else MUTED)
            if on:
                s.rect(x + 0.04, 0.47, 1.2, 0.03, fill=NAVY)
            x += 1.55
    s.text(0.5, 0.55, 12.3, 0.82, title, size=21, bold=True, color=NAVY, valign="b", name="Title")
    s.line(0.5, 1.45, W - 0.5, 1.45, color=NAVY, lw=1.0)
    if source:
        s.text(0.5, 6.92, 11.6, 0.42, source, size=8, color=MUTED, valign="b")
    if page:
        s.text(W - 1.0, 7.05, 0.5, 0.25, str(page), size=8, color=MUTED, align="r")
    return s


def fmt(v, dec=1, sign=False):
    t = f"{abs(v):,.{dec}f}"
    if sign:
        return ("+" if v > 0 else "−" if v < 0 else "±") + t
    return ("−" if v < 0 else "") + t


def waterfall(s, x, y, w, h, items, vmax, vmin=0.0, dec=2, unit="", label_h=0.55, label_size=9,
              val_size=10, bar_frac=0.62, target=None, target_label=None, colors=None, delta_unit=None, target_pos="right"):
    """items: list of (label, value, kind) kind 'total' (absolute) or 'delta'."""
    n = len(items)
    plot_h = h - label_h
    slot = w / n
    bw = slot * bar_frac

    def Y(v):
        return y + plot_h * (1 - (v - vmin) / (vmax - vmin))

    run = 0.0
    prev_top = None
    for i, (lab, v, kind) in enumerate(items):
        bx = x + i * slot + (slot - bw) / 2
        if kind == "total":
            lo, hi = max(min(0, v), vmin), max(0, v)
            col = (colors or {}).get(i, SLATE)
            run = v
            txt = fmt(v, dec) + unit
            ty = Y(hi) - 0.27
        else:
            lo, hi = sorted([run, run + v])
            col = (colors or {}).get(i, BLUE if v > 0 else ORANGE)
            txt = fmt(v, dec, sign=True) + (unit if delta_unit is None else delta_unit)
            ty = Y(hi) - 0.27
            run += v
        top, bot = Y(hi), Y(lo)
        if hi <= 0 and (kind == "total" or v < 0):
            ty = bot + 0.01
        if bot - top < 0.02:
            bot = top + 0.02
        s.rect(bx, top, bw, bot - top, fill=col)
        s.text(bx - 0.3, ty, bw + 0.6, 0.26, txt, size=val_size, bold=True, color=INK, align="c", valign="b")
        # connector
        if i < n - 1:
            nx = x + (i + 1) * slot + (slot - bw) / 2
            s.line(bx + bw, Y(run), nx, Y(run), color=MUTED, lw=0.5, dash=True)
        s.text(x + i * slot + 0.02, y + plot_h + 0.06, slot - 0.04, label_h - 0.06, lab, size=label_size,
               color=INK2, align="c")
    s.line(x, Y(0), x + w, Y(0), color=MUTED, lw=0.75)
    if target is not None:
        s.line(x, Y(target), x + w, Y(target), color=RED, lw=1.25, dash=True)
        if target_label:
            if target_pos == "right":
                s.text(x + w - 2.6, Y(target) - 0.27, 2.6, 0.25, target_label, size=9, bold=True, color=RED, align="r")
            else:
                s.text(x, Y(target) - 0.27, 2.6, 0.25, target_label, size=9, bold=True, color=RED, align="l")
    return Y


def table(s, x, y, widths, rows, row_h, size=10, header_size=9.5, header_fill=NAVY, header_color="FFFFFF",
          aligns=None, bold_first_col=False, zebra=False, header_h=None, fills=None, bolds=None, colors=None, valign="m"):
    """rows[0] is header. row_h: float or list per body row."""
    header_h = header_h or 0.4
    cx = [x]
    for wd in widths:
        cx.append(cx[-1] + wd)
    tot_w = sum(widths)
    # header
    s.rect(x, y, tot_w, header_h, fill=header_fill)
    for j, c in enumerate(rows[0]):
        s.text(cx[j] + 0.03, y, widths[j] - 0.06, header_h, c, size=header_size, bold=True, color=header_color,
               align=(aligns[j] if aligns else "l"), valign="m")
    yy = y + header_h
    for i, r in enumerate(rows[1:]):
        rh = row_h[i] if isinstance(row_h, list) else row_h
        if fills and fills.get(i):
            s.rect(x, yy, tot_w, rh, fill=fills[i])
        elif zebra and i % 2 == 1:
            s.rect(x, yy, tot_w, rh, fill=PALE)
        for j, c in enumerate(r):
            b = bool((bold_first_col and j == 0) or (bolds and (i, j) in bolds) or (bolds and (i, -1) in bolds))
            col = (colors or {}).get((i, j), INK)
            s.text(cx[j] + 0.03, yy + 0.02, widths[j] - 0.06, rh - 0.04, c, size=size, bold=b, color=col,
                   align=(aligns[j] if aligns else "l"), valign=valign)
        yy += rh
        s.line(x, yy, x + tot_w, yy, color=RULE, lw=0.5)
    return yy


def callout(s, x, y, w, h, head, body, size=10.5, head_size=11, fill=PALE_BLUE, bar=BLUE):
    s.rect(x, y, w, h, fill=fill)
    s.rect(x, y, 0.06, h, fill=bar)
    s.text(x + 0.15, y + 0.08, w - 0.25, 0.32, head, size=head_size, bold=True, color=NAVY)
    s.text(x + 0.15, y + 0.42, w - 0.25, h - 0.5, body, size=size, color=INK, bullet=True, space=4)


def stat(s, x, y, w, big, small, big_color=NAVY, big_size=26, h=1.1):
    s.text(x, y, w, 0.55, big, size=big_size, bold=True, color=big_color)
    s.text(x, y + 0.58, w, h - 0.58, small, size=9.5, color=INK2)


def verdict(s, x, y, kind):
    col = {"Supported": GREEN, "Partly": AMBER, "Not supported": RED, "Revised": RED}[kind]
    s.rect(x, y + 0.07, 0.14, 0.14, fill=col, shape="oval")
    s.text(x + 0.18, y, 1.4, 0.28, kind, size=10, bold=True, color=col)


def subhead(s, x, y, w, t, size=12, color=NAVY):
    s.text(x, y, w, 0.3, t, size=size, bold=True, color=color)
    s.line(x, y + 0.32, x + w, y + 0.32, color=RULE, lw=0.75)
