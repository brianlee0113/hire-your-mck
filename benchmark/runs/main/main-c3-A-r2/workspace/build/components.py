from kit import *


def measure(paras, w, size=13, bold=False, ls=1.2, space_after=4, bullet=False):
    base = {"size": size, "color": INK, "bold": bold, "bullet": bullet, "space_after": space_after, "align": "l"}
    if not isinstance(paras, list) or (paras and isinstance(paras[0], tuple)):
        paras = [paras]
    P = [norm_para(p, base) for p in paras]
    tot = 0
    for i, p in enumerate(P):
        lines, ms = wrap_para(p, w)
        tot += ms * ls / 72 * len(lines) + (p["space_after"] / 72 if i < len(P) - 1 else 0)
    return tot


def table(s, x, y, col_w, header, rows, size=11, hsize=10.5, pad=0.08, row_fills=None,
          header_fill=None, col_fills=None, min_row_h=0.0, header_color=INK2, bold_first_col=True,
          valign="t"):
    """rows: list of list of cells; cell = str | list of paras | dict(paras=..., color=, bold=)"""
    cx = [x]
    for cw in col_w:
        cx.append(cx[-1] + cw)
    total_w = sum(col_w)
    # header
    hh = max(measure(hcell, cw - 2 * pad, size=hsize, bold=True) for hcell, cw in zip(header, col_w)) + 2 * pad
    if header_fill:
        s.rect(x, y, total_w, hh, fill=header_fill)
    if col_fills:
        pass
    for i, (hc, cw) in enumerate(zip(header, col_w)):
        if hc:
            s.text(cx[i] + pad, y + pad, cw - 2 * pad, hh - 2 * pad, hc, size=hsize, bold=True, color=header_color, valign="b")
    cy = y + hh
    s.line(x, cy, x + total_w, cy, color=INK2, lw=1)
    out_rows = []
    for ri, row in enumerate(rows):
        cells = []
        for ci, c in enumerate(row):
            if isinstance(c, dict):
                cells.append(c)
            else:
                cells.append({"paras": c})
        rh = max(measure(c["paras"], col_w[ci] - 2 * pad, size=c.get("size", size),
                         bold=c.get("bold", bold_first_col and ci == 0)) for ci, c in enumerate(cells)) + 2 * pad
        rh = max(rh, min_row_h)
        out_rows.append((cy, rh))
        if row_fills and row_fills[ri]:
            s.rect(x, cy, total_w, rh, fill=row_fills[ri])
        if col_fills:
            for ci, f in enumerate(col_fills):
                if f:
                    s.rect(cx[ci], cy, col_w[ci], rh, fill=f)
        for ci, c in enumerate(cells):
            s.text(cx[ci] + pad, cy + pad, col_w[ci] - 2 * pad, rh - 2 * pad, c["paras"], size=c.get("size", size),
                   bold=c.get("bold", bold_first_col and ci == 0), color=c.get("color", INK), valign=c.get("valign", valign))
        cy += rh
        s.line(x, cy, x + total_w, cy, color=GRID, lw=0.75)
    return cy, out_rows, cx


def hbars(s, x, y, w, label_w, rows, vmax, bar_h=0.32, gap=0.22, value_fmt=lambda v: f"{v}", size=11,
          value_w=0.9, colors=None, sublabels=None, ref_lines=(), inside=False):
    """Horizontal bar chart. rows = [(label, value)]. Returns bottom y."""
    plot_x = x + label_w
    plot_w = w - label_w - value_w
    cy = y
    for i, (lab, v) in enumerate(rows):
        col = colors[i] if colors else BLUE
        s.text(x, cy - 0.04, label_w - 0.12, bar_h + 0.1, lab, size=size, color=INK, align="r", valign="m")
        bw = max(0.02, plot_w * v / vmax)
        s.rect(plot_x, cy, bw, bar_h, fill=col)
        lab_txt = value_fmt(v) if not sublabels else sublabels[i]
        need = font(size, True).getlength(lab_txt) / DPI + 0.25
        if inside and bw > need and any(bw - 0.05 < plot_w * rv / vmax < bw + need for rv, _ in ref_lines):
            s.text(plot_x + 0.05, cy - 0.04, bw - 0.15, bar_h + 0.1, lab_txt, size=size, color="#ffffff", bold=True,
                   valign="m", align="r")
        else:
            s.text(plot_x + bw + 0.08, cy - 0.04, value_w + plot_w - bw, bar_h + 0.1, lab_txt,
                   size=size, color=INK, bold=True, valign="m")
        cy += bar_h + gap
    s.line(plot_x, y - 0.1, plot_x, cy - gap + 0.1, color=AXIS, lw=1)
    for val, lab in ref_lines:
        rx = plot_x + plot_w * val / vmax
        s.line(rx, y - 0.25, rx, cy - gap + 0.1, color=INK2, lw=1, dash=True)
        s.text(rx - 1.5, y - 0.5, 3.0, 0.25, lab, size=9.5, color=INK2, align="c")
    return cy - gap


def vbars(s, x, y, w, h, rows, vmax, bar_w=0.9, size=11, value_fmt=lambda v: f"{v}", colors=None, label_h=0.5,
          ref=None):
    """Vertical bars; rows=[(label, value)]. Area: x,y,w,h includes labels at bottom."""
    n = len(rows)
    plot_h = h - label_h - 0.35
    base_y = y + 0.35 + plot_h
    slot = w / n
    s.line(x, base_y, x + w, base_y, color=AXIS, lw=1)
    for i, (lab, v) in enumerate(rows):
        col = colors[i] if colors else BLUE
        bx = x + slot * i + (slot - bar_w) / 2
        bh = plot_h * v / vmax
        s.rect(bx, base_y - bh, bar_w, bh, fill=col)
        s.text(bx - 0.4, base_y - bh - 0.36, bar_w + 0.8, 0.32, value_fmt(v), size=size + 3, bold=True, align="c", valign="b")
        s.text(x + slot * i + 0.05, base_y + 0.08, slot - 0.1, label_h, lab, size=size - 0.5, color=INK2, align="c")
    if ref:
        val, lab = ref
        ry = base_y - plot_h * val / vmax
        s.line(x, ry, x + w, ry, color=INK2, lw=1, dash=True)
        s.text(x + w - 2.5, ry - 0.28, 2.5, 0.25, lab, size=9.5, color=INK2, align="r")
    return base_y


def pill(s, x, y, w, label, kind):
    """status pill with symbol + label (never color alone)"""
    col = {"good": GOOD_T, "bad": CRIT, "mid": "#9a6a00"}[kind]
    sym = {"good": "✓", "bad": "✗", "mid": "~"}[kind]
    s.text(x, y, w, 0.3, [(sym + " ", {"bold": True, "color": col}), (label, {"bold": True, "color": col})], size=11)


def card(s, x, y, w, h, kicker, hero, body, fill=PANEL, hero_size=30):
    s.rect(x, y, w, h, fill=fill)
    s.rect(x, y, 0.06, h, fill=BLUE)
    s.text(x + 0.25, y + 0.2, w - 0.45, 0.3, kicker, size=11, bold=True, color=INK2)
    s.text(x + 0.25, y + 0.52, w - 0.45, 0.65, hero, size=hero_size, bold=True, color=INK)
    s.text(x + 0.25, y + 1.25, w - 0.45, h - 1.4, body, size=12, color=INK, space_after=6)
