from engine import Slide, Text, Rect, Line, W, H

NAVY = "#0d366b"
INK = "#0b0b0b"
INK2 = "#52514e"
MUTED = "#8a8984"
RULE = "#d9d8d4"
PANEL = "#f4f3f0"
BLUE = "#2a78d6"      # increases / recommended
BLUE_LT = "#9ec5f4"   # stretch
ORANGE = "#d4541f"    # decreases (darkened slot-2 orange for text-free bar contrast)
TOTAL = "#5f6b7a"     # totals
GREEN = "#1f7a3a"
RED = "#b3261e"

L, R = 0.55, W - 0.55
CW = R - L


def base_slide(kicker, title, source=None, page=None):
    s = Slide()
    s.add(Text(L, 0.28, 9, 0.3, kicker.upper(), size=10, bold=True, color=BLUE))
    s.add(Text(L, 0.55, CW, 0.95, title, size=22, bold=True, color=NAVY, valign="t"))
    s.add(Line(L, 1.52, R, 1.52, color=RULE, lw=1))
    if source:
        s.add(Text(L, 6.86, CW - 0.6, 0.5, source, size=8, color=MUTED, valign="b"))
    if page:
        s.add(Text(R - 0.5, 7.06, 0.5, 0.3, str(page), size=8, color=MUTED, align="r", valign="b"))
    return s


def panel(s, x, y, w, h, heading, paras, size=11.5, fill=PANEL, head_color=NAVY):
    s.add(Rect(x, y, w, h, fill=fill))
    s.add(Text(x + 0.15, y + 0.12, w - 0.3, 0.32, heading, size=12, bold=True, color=head_color))
    s.add(Text(x + 0.15, y + 0.48, w - 0.3, h - 0.58, paras, size=size, color=INK))


def fmt(v, dec=1, unit="", sign=True):
    s = f"{abs(v):,.{dec}f}"
    if sign:
        s = ("+" if v > 0 else "−" if v < 0 else "") + s
    elif v < 0:
        s = "−" + s
    return s + unit


def waterfall(s, x, y, w, h, steps, vmin, vmax, dec=1, unit="", label_h=0.62, bar_frac=0.62,
              label_size=10, value_size=11, target=None, target_label=None):
    """steps: list of dict(label, v, kind in {'total','delta','stretch'}, sub=None, vlabel=None)."""
    n = len(steps)
    slot = w / n
    bw = slot * bar_frac
    top = y + 0.32
    bottom = y + h - label_h
    sc = (bottom - top) / (vmax - vmin)
    Y = lambda v: bottom - (v - vmin) * sc
    run = 0.0
    prev_edge = None
    s.add(Line(x, Y(0) if vmin <= 0 else bottom, x + w, Y(0) if vmin <= 0 else bottom, color=MUTED, lw=0.75))
    for i, st in enumerate(steps):
        cx = x + slot * i + (slot - bw) / 2
        kind = st["kind"]
        if kind == "total":
            lo, hi = min(0, st["v"]), max(0, st["v"])
            color = st.get("color", TOTAL)
            run = st["v"]
            edge = run
            vtxt = st.get("vlabel") or fmt(st["v"], dec, unit, sign=False)
        else:
            a, b = run, run + st["v"]
            lo, hi = min(a, b), max(a, b)
            color = st.get("color") or (BLUE_LT if kind == "stretch" else (BLUE if st["v"] >= 0 else ORANGE))
            run = b
            edge = b
            vtxt = st.get("vlabel") or fmt(st["v"], dec, unit)
        hh = max((hi - lo) * sc, 0.025)
        s.add(Rect(cx, Y(hi) if (hi - lo) * sc >= 0.025 else Y(lo) - 0.025, bw, hh, fill=color))
        if prev_edge is not None:
            s.add(Line(cx - (slot - bw), Y(prev_edge), cx, Y(prev_edge), color="#b8b7b2", lw=0.75))
        prev_edge = edge
        bold = kind == "total"
        s.add(Text(cx - 0.25, Y(hi) - 0.3, bw + 0.5, 0.28, vtxt, size=value_size, bold=bold,
                   color=INK, align="c", valign="b"))
        paras = [{"t": st["label"], "bold": bold}]
        if st.get("sub"):
            paras.append({"t": st["sub"], "color": INK2, "size": label_size - 1})
        s.add(Text(x + slot * i + 0.02, bottom + 0.06, slot - 0.04, label_h - 0.06, paras,
                   size=label_size, color=INK, align="c"))
    if target is not None:
        ty = Y(target)
        s.add(Line(x, ty, x + w, ty, color=GREEN, lw=1.25, dash=True))
        if target_label:
            s.add(Text(x + 0.02, ty - 0.27, 3.2, 0.26, target_label, size=9.5, bold=True, color=GREEN))
    return Y


def hbars(s, x, y, w, rows, vmin, vmax, label_w=2.6, row_h=0.55, value_w=0.9, dec=2, unit="",
          label_size=11, colors=None):
    """Horizontal bars from zero. rows: (label, value, sublabel, color or None, value_text or None)."""
    plot_x = x + label_w
    plot_w = w - label_w - value_w * 0  # values placed outside bar ends; reserve inside plot
    sc = (plot_w) / (vmax - vmin)
    X = lambda v: plot_x + (v - vmin) * sc
    for i, (lab, v, sub, col, vt) in enumerate(rows):
        ry = y + i * row_h
        paras = [{"t": lab}]
        if sub:
            paras.append({"t": sub, "size": label_size - 1.5, "color": INK2})
        s.add(Text(x, ry, label_w - 0.1, row_h, paras, size=label_size, valign="m"))
        bh = row_h * 0.5
        a, b = X(min(0, v)), X(max(0, v))
        col = col or (BLUE if v >= 0 else ORANGE)
        s.add(Rect(a, ry + (row_h - bh) / 2, max(b - a, 0.02), bh, fill=col))
        vt = vt or fmt(v, dec, unit)
        if v >= 0:
            s.add(Text(b + 0.05, ry, value_w, row_h, vt, size=label_size, bold=True, valign="m"))
        else:
            s.add(Text(a - value_w - 0.05, ry, value_w, row_h, vt, size=label_size, bold=True, valign="m", align="r"))
    s.add(Line(X(0), y - 0.05, X(0), y + len(rows) * row_h + 0.05, color=MUTED, lw=0.75))
    return X


def table(s, x, y, col_w, rows, header=None, row_h=0.5, size=10.5, head_size=10, zebra=False,
          col_align=None, bold_first=True, rule_color=RULE, row_heights=None, fills=None):
    col_align = col_align or ["l"] * len(col_w)
    cy = y
    if header:
        cx = x
        for j, hdr in enumerate(header):
            s.add(Text(cx, cy, col_w[j], 0.42, hdr, size=head_size, bold=True, color=INK2,
                       align=col_align[j], valign="b"))
            cx += col_w[j]
        cy += 0.46
        s.add(Line(x, cy, x + sum(col_w), cy, color=INK2, lw=1))
    for i, row in enumerate(rows):
        rh = row_heights[i] if row_heights else row_h
        if fills and fills[i]:
            s.add(Rect(x, cy, sum(col_w), rh, fill=fills[i]))
        cx = x
        for j, cell in enumerate(row):
            if isinstance(cell, dict):
                c = dict(cell)
                t = c.pop("t")
            else:
                t, c = cell, {}
            s.add(Text(cx + 0.04, cy + 0.02, col_w[j] - 0.08, rh - 0.04, t, size=c.pop("size", size),
                       bold=c.pop("bold", bold_first and j == 0), color=c.pop("color", INK),
                       align=c.pop("align", col_align[j]), valign=c.pop("valign", "m")))
            cx += col_w[j]
        cy += rh
        s.add(Line(x, cy, x + sum(col_w), cy, color=rule_color, lw=0.75))
    return cy
