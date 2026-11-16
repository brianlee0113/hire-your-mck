from lib import *


def waterfall(sl, x, y, w, h, items, vmax, fmt, label_size=10.5, val_size=12, label_h=0.75, bar_frac=0.58,
              ref=None):
    """items: (label, value, kind) kind: 'total' | 'delta'. Draws within box; baseline at y+h-label_h."""
    n = len(items)
    slot = w / n
    base = y + h - label_h
    top_space = 0.32
    ph = h - label_h - top_space
    k = ph / vmax
    run = 0
    prev_top = None
    if ref:
        rv, rlabel = ref
        ry = base - rv * k
        sl.line(x, ry, x + w, ry, color=INK, lw=1.0, dash=True)
        sl.text(x, ry - 0.26, 2.6, 0.22, rlabel, size=9.5, color=INK, bold=True, align="l", name="ref")
    for i, (lab, v, kind) in enumerate(items):
        bx = x + i * slot + slot * (1 - bar_frac) / 2
        bw = slot * bar_frac
        if kind == "total":
            lo, hi = 0, v
            run = v
            col = TOTAL
        else:
            lo, hi = sorted([run, run + v])
            col = BLUE if v >= 0 else RED
            run = run + v
        y1 = base - hi * k
        hh = max((hi - lo) * k, 0.02)
        sl.rect(bx, y1, bw, hh, fill=col)
        # connector to next
        if i < n - 1:
            ly = base - run * k
            sl.line(bx + bw, ly, bx + slot, ly, color=MUTED, lw=0.5)
        txt = fmt(v, kind)
        sl.text(x + i * slot, y1 - 0.27, slot, 0.24, txt, size=val_size, bold=True, color=INK, align="c",
                name=f"wf val {lab}")
        sl.text(x + i * slot + 0.03, base + 0.08, slot - 0.06, label_h - 0.08, lab, size=label_size, color=SEC,
                align="c", name=f"wf lab {lab}")
    sl.line(x, base, x + w, base, color=RULE, lw=0.75)
    return base, k


def hbars(sl, x, y, w, rows, vmin, vmax, label_w, bar_h=0.34, gap=0.22, val_fmt=str, size=11.5, zero_line=True,
          ref=None):
    """rows: (label, value or (lo,hi), color). Draws horizontal bars. Returns bottom y."""
    px0 = x + label_w
    pw = w - label_w - 0.9
    k = pw / (vmax - vmin)
    zx = px0 + (0 - vmin) * k
    cy = y
    for lab, v, col in rows:
        sl.text(x, cy - 0.05, label_w - 0.15, bar_h + 0.1, lab, size=size, color=INK, anchor="m", align="r",
                name=f"hb {lab}")
        if isinstance(v, tuple):
            lo, hi = v
            sl.rect(zx + lo * k, cy, (hi - lo) * k, bar_h, fill=col)
            end = zx + hi * k
            sl.text(end + 0.08, cy - 0.05, 1.3, bar_h + 0.1, val_fmt(v), size=size, bold=True, anchor="m",
                    name="hbv")
        else:
            if v >= 0:
                sl.rect(zx, cy, v * k, bar_h, fill=col)
                sl.text(zx + v * k + 0.08, cy - 0.05, 1.3, bar_h + 0.1, val_fmt(v), size=size, bold=True,
                        anchor="m", name="hbv")
            else:
                sl.rect(zx + v * k, cy, -v * k, bar_h, fill=col)
                sl.text(zx + v * k - 1.38, cy - 0.05, 1.3, bar_h + 0.1, val_fmt(v), size=size, bold=True,
                        anchor="m", align="r", name="hbv")
        cy += bar_h + gap
    if zero_line:
        sl.line(zx, y - 0.1, zx, cy - gap + 0.1, color=RULE, lw=0.75)
    if ref:
        rv, rl = ref
        rx = zx + rv * k
        sl.line(rx, y - 0.25, rx, cy - gap + 0.1, color=INK, lw=1.0, dash=True)
        sl.text(rx - 1.0, y - 0.5, 2.0, 0.22, rl, size=9.5, bold=True, align="c", name="ref")
    return cy, zx, k


def columns(sl, x, y, w, h, cats, vals, cols, vmax, fmt, label_size=11, val_size=12, label_h=0.55, bar_frac=0.55):
    n = len(cats)
    slot = w / n
    base = y + h - label_h
    ph = h - label_h - 0.32
    k = ph / vmax
    for i, (c, v, col) in enumerate(zip(cats, vals, cols)):
        bx = x + i * slot + slot * (1 - bar_frac) / 2
        bw = slot * bar_frac
        sl.rect(bx, base - v * k, bw, v * k, fill=col)
        sl.text(x + i * slot, base - v * k - 0.28, slot, 0.25, fmt(v), size=val_size, bold=True, align="c",
                name="colv")
        sl.text(x + i * slot, base + 0.07, slot, label_h - 0.07, c, size=label_size, color=SEC, align="c",
                name="col")
    sl.line(x, base, x + w, base, color=RULE, lw=0.75)


def table(sl, x, y, widths, rows, heights, size=11, head_fill=None, head_color=INK, zebra=None,
          col_align=None, bold_first_col=False, pad=0.08, fills=None, rule=GRID):
    """rows: list of list of cell (str|list paras). First row is header."""
    cy = y
    for r, (row, rh) in enumerate(zip(rows, heights)):
        cx = x
        if r == 0 and head_fill:
            sl.rect(x, cy, sum(widths), rh, fill=head_fill)
        elif fills and fills.get(r):
            sl.rect(x, cy, sum(widths), rh, fill=fills[r])
        for c, (cell, cw) in enumerate(zip(row, widths)):
            if fills and fills.get((r, c)):
                sl.rect(cx, cy, cw, rh, fill=fills[(r, c)])
            al = (col_align[c] if col_align else "l")
            b = (r == 0) or (bold_first_col and c == 0)
            col = head_color if r == 0 else INK
            sl.text(cx + pad, cy + 0.04, cw - 2 * pad, rh - 0.08, cell, size=size, bold=b, color=col, align=al,
                    anchor="m", name=f"tbl r{r}c{c}")
            cx += cw
        cy += rh
        sl.line(x, cy, x + sum(widths), cy, color=RULE if r == 0 else rule, lw=0.75 if r == 0 else 0.5)
    return cy
