"""Compose the README images from rendered slide PNGs.

Inputs (made by rendering renderer/examples/cobalt-ledger.json and exporting through PowerPoint at 2x):
  output/png/pNN.png          full deck, navy
  output/themes/<theme>.png   page 4 in each theme
  output/ghost/p04.png        page 4 of the storyline-only (ghost) version
Output: docs/readme/*.png
"""
from pathlib import Path

import openpyxl
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
PNG, OUT = ROOT / "output", ROOT / "docs" / "readme"
OUT.mkdir(parents=True, exist_ok=True)

SUP = "/System/Library/Fonts/Supplemental/"
def font(name, size):
    return ImageFont.truetype(SUP + name, size)
SERIF_B = lambda s: font("Georgia Bold.ttf", s)
SANS = lambda s: font("Arial.ttf", s)
SANS_B = lambda s: font("Arial Bold.ttf", s)
MONO = lambda s: ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", s)

NAVY, BLUE, INK, MUTED, LINE, BG, CARD = "#0B1F33", "#2E5BFF", "#2E3A44", "#6A7682", "#D5DBDF", "#F4F6F9", "#FFFFFF"


def slide(n, folder="png"):
    return Image.open(PNG / folder / f"p{n:02d}.png").convert("RGB")


def thumb(img, w):
    return img.resize((w, round(img.height * w / img.width)), Image.LANCZOS)


def framed(canvas, img, xy, radius=10, border=LINE, shadow=True):
    x, y = xy
    d = ImageDraw.Draw(canvas)
    if shadow:
        d.rounded_rectangle((x + 6, y + 8, x + img.width + 6, y + img.height + 8), radius, fill="#E2E6EC")
    canvas.paste(img, (x, y))
    d.rounded_rectangle((x, y, x + img.width, y + img.height), radius, outline=border, width=2)


def wrap(d, text, f, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= width:
            cur = t
        else:
            lines.append(cur); cur = w
    lines.append(cur)
    return lines


def text_block(d, xy, text, f, width, fill=INK, gap=1.3):
    x, y = xy
    for ln in wrap(d, text, f, width):
        d.text((x, y), ln, font=f, fill=fill)
        y += f.size * gap
    return y


def arrow(d, x1, y, x2, color=BLUE, w=6):
    d.line((x1, y, x2 - 18, y), fill=color, width=w)
    d.polygon([(x2, y), (x2 - 24, y - 15), (x2 - 24, y + 15)], fill=color)


def step_label(d, xy, n, text):
    x, y = xy
    d.ellipse((x, y, x + 44, y + 44), fill=NAVY)
    d.text((x + 22, y + 22), str(n), font=SANS_B(24), fill="white", anchor="mm")
    d.text((x + 60, y + 22), text, font=SANS_B(28), fill=NAVY, anchor="lm")


# ---------- 1. Hero: brief -> storyline -> deck ----------
def hero():
    W, H = 2400, 630
    c = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(c)
    top = 120
    # brief card
    cx, cw, ch = 40, 520, 448
    d.rounded_rectangle((cx, top, cx + cw, top + ch), 16, fill=CARD, outline=LINE, width=2)
    step_label(d, (cx, 40), 1, "You brief it")
    y = top + 36
    d.text((cx + 32, y), "YOUR BRIEF", font=SANS_B(20), fill=MUTED); y += 46
    brief = ("Our CEO has to decide whether to launch an AI package for our "
             "small-business accounting customers now. Build the deck from public data.")
    y = text_block(d, (cx + 32, y), brief, SANS(27), cw - 64, fill=INK, gap=1.4) + 24
    for k, v in (("Audience", "CEO, approve or reject"), ("Mode", "Full deck, every number sourced"), ("Theme", "Navy")):
        d.text((cx + 32, y), k, font=SANS_B(22), fill=MUTED)
        d.text((cx + 170, y), v, font=SANS(22), fill=INK); y += 40
    # exec summary
    EXW, TW = 780, 380
    ex = thumb(slide(2), EXW)
    ex_x = cx + cw + 90
    step_label(d, (ex_x, 40), 2, "It writes the storyline")
    framed(c, ex, (ex_x, top))
    arrow(d, cx + cw + 20, top + ch // 2, ex_x - 20)
    # 2x2 deck
    gx = ex_x + EXW + 90
    step_label(d, (gx, 40), 3, "You get the deck and its sources")
    tw = TW
    for i, n in enumerate((3, 5, 6, 10)):
        t = thumb(slide(n), tw)
        framed(c, t, (gx + (i % 2) * (tw + 20), top + (i // 2) * (t.height + 20)), radius=8)
    arrow(d, ex_x + EXW + 18, top + ch // 2, gx - 18)
    c.save(OUT / "hero.png", optimize=True)


# ---------- 2. Storyline: exec summary items -> slide titles ----------
SECTIONS = [
    (1, "Small firms are the next wave", [3, 4, 5]),
    (2, "What holds them back", [6, 7]),
    (3, "Why launch now", [8, 9, 10]),
]
TITLES = {
    3: "AI use among US firms rose from 17% to 25% in under a year, so our customers will soon expect it",
    4: "Small firms use AI at about half the rate of large ones, so most of our customers have yet to adopt",
    5: "In accounting, under 6% of the smallest firms use AI against over 20% of the largest, so our core is open",
    6: "Small firms skip AI because they do not see where it fits, not because of cost, so we must show them",
    7: "Adopters cannot find tools that fit, and users doubt accuracy, so our package must be built in and checkable",
    8: "Accountants using AI closed the books 7.5 days faster, the gain our customers would feel first",
    9: "Intuit, Xero and Shopify have all shipped AI assistants for small businesses, so waiting would leave us the exception",
    10: "Four launch moves turn this evidence into an AI package small firms will actually use",
}


def storyline():
    W = 2400
    ex = thumb(slide(2), 1000)
    row_h, gap_sec = 132, 34
    H = max(ex.height + 200, 140 + sum(len(s[2]) for s in SECTIONS) * row_h + gap_sec * 3 + 40)
    c = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(c)
    d.text((40, 36), "Executive summary", font=SANS_B(30), fill=NAVY)
    d.text((1180, 36), "The slide titles under each item, read on their own", font=SANS_B(30), fill=NAVY)
    ex_xy = (40, 110)
    framed(c, ex, ex_xy)
    cap_y = ex_xy[1] + ex.height + 50
    for line, bold in (("Read only the executive summary: the whole story.", True),
                       ("Read only the slide titles: the same story, one step per page.", True),
                       ("Every title is a judgment the slide's evidence has to prove, not a label.", False)):
        d.text((40, cap_y), line, font=(SANS_B if bold else SANS)(30), fill=NAVY if bold else INK)
        cap_y += 52
    # y of exec items 1-3 on the slide (fractions of slide height, measured on the 1920x1080 render)
    item_y = [ex_xy[1] + ex.height * f for f in (310 / 1080, 560 / 1080, 760 / 1080)]
    y = 110
    tx = 1180
    for (num, name, pages), iy in zip(SECTIONS, item_y):
        y0 = y
        for p in pages:
            t = thumb(slide(p), 200)
            framed(c, t, (tx + 70, y), radius=6, shadow=False)
            d.text((tx + 300, y + 8), f"p. {p}", font=SANS_B(20), fill=MUTED)
            text_block(d, (tx + 370, y + 4), TITLES[p], SERIF_B(25), W - tx - 410, fill=NAVY, gap=1.25)
            y += row_h
        y1 = y - row_h + 112
        # section badge and bracket
        d.ellipse((tx, y0, tx + 48, y0 + 48), fill=BLUE)
        d.text((tx + 24, y0 + 24), str(num), font=SANS_B(26), fill="white", anchor="mm")
        d.line((tx + 24, y0 + 56, tx + 24, y1), fill=BLUE, width=4)
        # connector from exec item to badge
        sx = ex_xy[0] + ex.width + 12
        d.line((sx, iy, sx + 40, iy, tx - 40, y0 + 24, tx - 6, y0 + 24), fill=BLUE, width=4, joint="curve")
        d.ellipse((sx - 8, iy - 8, sx + 8, iy + 8), fill=BLUE)
        y += gap_sec
    c = c.crop((0, 0, W, max(y + 10, ex_xy[1] + ex.height + 40)))
    c.save(OUT / "storyline.png", optimize=True)


# ---------- 3. Receipt: a number on the slide -> its row in the workbook ----------
def receipt():
    W, H = 2400, 860
    c = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(c)
    s = slide(5)
    x0, y0 = 60, 255
    crop = thumb(s.crop((x0, y0, 1250, 960)), 1100)  # unit line and chart, 1920x1080 render
    cx, cy = 40, 100
    d.text((40, 36), "On the slide", font=SANS_B(30), fill=NAVY)
    framed(c, crop, (cx, cy))
    k = crop.width / (1250 - x0)
    rx, ry = cx + (516 - x0) * k, cy + (319 - y0) * k  # the highlighted "5.9%" label on the 1920 render
    d.ellipse((rx - 66, ry - 34, rx + 66, ry + 34), outline="#D99A00", width=6)
    wb = openpyxl.load_workbook(ROOT / "output" / "cobalt-ledger-sources.xlsx")
    ws = wb["p5 (slide 3)"]
    hdr = [x.value for x in ws[4]]
    rows = [{h: v for h, v in zip(hdr, [x.value for x in r])} for r in ws.iter_rows(min_row=5)]
    row = rows[0]
    kx, kw = 1250, W - 1250 - 40
    d.text((kx, 36), "In the source workbook that ships with the deck", font=SANS_B(30), fill=NAVY)
    d.rounded_rectangle((kx, cy, kx + kw, cy + 470), 16, fill=CARD, outline=LINE, width=2)
    fields = [("Value", f"{row['Value'] * 100:.1f}%"), ("Data point", row["Data point"]), ("Period", row["Period"]),
              ("Source", f"US Census Bureau, {row['Source']}"), ("URL", row["URL"]), ("Excerpt", row["Excerpt"]),
              ("Locator", row["Locator"])]
    y = cy + 28
    for k_, v in fields:
        d.text((kx + 36, y + (8 if k_ == "Value" else 0)), k_, font=SANS_B(23), fill=MUTED)
        f = SERIF_B(40) if k_ == "Value" else (MONO(19) if k_ in ("URL", "Excerpt") else SANS(23))
        col = BLUE if k_ == "URL" else (NAVY if k_ == "Value" else INK)
        y = text_block(d, (kx + 200, y), str(v), f, kw - 236, fill=col, gap=1.35) + 12
    # derived number: its formula stays live
    dy = cy + 500
    d.rounded_rectangle((kx, dy, kx + kw, H - 40), 16, fill=CARD, outline=LINE, width=2)
    d.text((kx + 36, dy + 26), "A number we calculated keeps its formula", font=SANS_B(26), fill=NAVY)
    d.text((kx + 36, dy + 80), "3.5x", font=SERIF_B(44), fill=BLUE)
    text_block(d, (kx + 200, dy + 80), "Largest firms' AI-use rate in finance and accounting as a multiple of the smallest firms' (sidebar, p. 5)",
               SANS(23), kw - 236, fill=INK)
    d.text((kx + 200, dy + 160), "Calculations sheet:  =20.5% / 5.9%, a live Excel formula",
           font=MONO(19), fill=INK)
    arrow(d, cx + crop.width + 14, round(ry), kx - 14, color="#D99A00")
    c.save(OUT / "receipt.png", optimize=True)


# ---------- 4. Themes ----------
THEMES = ["navy", "crimson", "forest", "mono", "vivid", "slate", "terracotta"]


def themes():
    W, cols, gap = 2400, 4, 24
    tw = (W - 80 - gap * (cols - 1)) // cols
    rows = 2
    th = round(tw * 1080 / 1920)
    H = 40 + rows * (th + 70) + 20
    c = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(c)
    for i, name in enumerate(THEMES):
        t = thumb(Image.open(PNG / "themes" / f"{name}.png").convert("RGB"), tw)
        x = 40 + (i % cols) * (tw + gap)
        y = 30 + (i // cols) * (th + 70)
        framed(c, t, (x, y), radius=8)
        d.text((x, y + th + 18), name + ("  (default)" if name == "navy" else ""), font=SANS_B(26), fill=NAVY)
    c.save(OUT / "themes.png", optimize=True)


# ---------- 5. Gallery ----------
def gallery():
    W, cols, gap = 2400, 3, 24
    pages = [3, 5, 7, 8, 9, 10]
    tw = (W - 80 - gap * (cols - 1)) // cols
    th = round(tw * 1080 / 1920)
    H = 40 + 2 * (th + gap) + 16
    c = Image.new("RGB", (W, H), BG)
    for i, p in enumerate(pages):
        framed(c, thumb(slide(p), tw), (40 + (i % cols) * (tw + gap), 30 + (i // cols) * (th + gap)), radius=8)
    c.save(OUT / "gallery.png", optimize=True)


# ---------- 6. Modes: storyline only vs full deck ----------
def modes():
    W, gap = 2400, 60
    tw = (W - 80 - gap) // 2
    a, b = thumb(slide(4, "ghost"), tw), thumb(slide(4), tw)
    H = 110 + a.height + 50
    c = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(c)
    d.text((40, 36), "Storyline only (ghost deck): what to prove and the data to find",
           font=SANS_B(26), fill=NAVY)
    d.text((40 + tw + gap, 36), "Full deck: the same slide with sourced data", font=SANS_B(26), fill=NAVY)
    framed(c, a, (40, 100))
    framed(c, b, (40 + tw + gap, 100))
    c.save(OUT / "modes.png", optimize=True)


if __name__ == "__main__":
    for f in (hero, storyline, receipt, themes, gallery, modes):
        f(); print("ok", f.__name__)
