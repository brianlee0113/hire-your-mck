"""Make the README demo GIF: brief -> checkpoint -> storyline -> deck -> sources -> install.

Uses the same inputs as tools/readme_images.py (output/png/pNN.png, docs/readme/receipt.png).
Output: docs/readme/demo.gif (and demo.mp4 if ffmpeg is installed).
"""
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from readme_images import (BG, BLUE, CARD, INK, LINE, MUTED, NAVY, OUT, MONO, SANS, SANS_B, SERIF_B,
                           slide, thumb, wrap)

W, H = 1280, 720
FPS = 10
GREEN, GOLD = "#1E8E5A", "#D99A00"
STEPS = ["Brief", "Pick", "Approve", "Build", "Source"]
BRIEF = ("Our CEO has to decide whether to launch an AI package for our small-business "
         "accounting customers now. Build the deck from public data.")

frames, durations = [], []


def add(img, seconds):
    frames.append(img.copy())
    durations.append(round(seconds * 1000))


def check(d, cx, cy, r, color, w=3):
    d.line((cx - r, cy, cx - r / 3, cy + r * 0.7, cx + r, cy - r * 0.7), fill=color, width=w, joint="curve")


def base(step, title):
    c = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(c)
    # brand + step tracker
    d.text((40, 30), "hire-your-mck", font=SANS_B(22), fill=NAVY)
    x = 440
    for i, s in enumerate(STEPS, 1):
        on, done = i == step, i < step
        fill = BLUE if on else (NAVY if done else "#C9D1DA")
        d.ellipse((x, 28, x + 28, 56), fill=fill)
        if done:
            check(d, x + 14, 42, 7, "white")
        else:
            d.text((x + 14, 42), str(i), font=SANS_B(15), fill="white", anchor="mm")
        d.text((x + 36, 42), s, font=SANS_B(17) if on else SANS(17), fill=NAVY if on or done else MUTED, anchor="lm")
        x += 36 + d.textlength(s, font=SANS_B(17)) + 34
    d.line((40, 78, W - 40, 78), fill=LINE, width=2)
    if title:
        d.text((40, 100), title, font=SERIF_B(34), fill=NAVY)
    return c, d


def bubble(d, xy, w, lines, f, fill, color, gap=1.4, pad=22):
    x, y = xy
    h = pad * 2 + len(lines) * f.size * gap - (gap - 1) * f.size
    d.rounded_rectangle((x, y, x + w, y + h), 18, fill=fill, outline=None if fill != CARD else LINE, width=2)
    for i, ln in enumerate(lines):
        d.text((x + pad, y + pad + i * f.size * gap), ln, font=f, fill=color)
    return y + h


# ---------- 1. Brief, typed ----------
def scene_brief():
    f = SANS(28)
    tmp = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    bw = 820
    full = wrap(tmp, BRIEF, f, bw - 44)
    n = len(BRIEF)
    for k in list(range(0, n, 6)) + [n]:
        c, d = base(1, "Brief it like a partner")
        part = BRIEF[:k]
        lines = wrap(d, part, f, bw - 44) if part else [""]
        lines += [""] * (len(full) - len(lines))
        if k < n:
            lines[len(wrap(d, part, f, bw - 44)) - 1 if part else 0] += "|"
        bubble(d, (W - 40 - bw, 200), bw, lines, f, NAVY, "white")
        d.text((W - 40, 200 + 39 * len(full) + 60), "You", font=SANS(18), fill=MUTED, anchor="ra")
        add(c, 1 / FPS)
    add(c, 1.0)


# ---------- 2. Checkpoint: multiple choice ----------
def scene_pick():
    q = [("Audience and decision", ["CEO: approve or reject", "Board: update", "Team: align on a plan"], 0),
         ("Your material", ["I have files to share", "Search the web", "Leave data as placeholders"], 1),
         ("Look", ["navy (deep navy, one blue accent)", "mono", "vivid", "slate"], 0)]
    for reveal in range(len(q) + 1):
        c, d = base(2, "It asks. You pick. No blank page.")
        y = 170
        for qi, (label, opts, pick) in enumerate(q):
            d.text((40, y), label, font=SANS_B(22), fill=MUTED)
            x = 40
            for oi, o in enumerate(opts):
                chosen = qi < reveal and oi == pick
                tw = d.textlength(o, font=SANS(22)) + 48
                d.rounded_rectangle((x, y + 38, x + tw, y + 90), 26,
                                    fill=BLUE if chosen else CARD, outline=BLUE if chosen else LINE, width=2)
                d.text((x + 24, y + 64), o, font=SANS(22), fill="white" if chosen else INK, anchor="lm")
                x += tw + 14
            y += 150
        add(c, 0.9 if reveal < len(q) else 1.2)


# ---------- 3. Storyline, approved before any data work ----------
SECTIONS = [
    ("Small firms are the next wave", ["AI use rose from 17% to 25% in under a year, so our customers will soon expect it",
                                       "Small firms use AI at about half the rate of large ones, so most have yet to adopt",
                                       "In accounting, under 6% of the smallest firms use AI, so our core is open"]),
    ("What holds them back", ["They skip AI because they do not see where it fits, not because of cost",
                              "Adopters cannot find tools that fit and doubt accuracy, so ours must be checkable"]),
    ("Why launch now", ["AI users closed the books 7.5 days faster, the gain our customers feel first",
                        "Intuit, Xero and Shopify have all shipped AI, so waiting leaves us the exception",
                        "Four launch moves turn this evidence into a package small firms will use"]),
]


def draw_story(d, shown):
    d.text((40, 160), "GOVERNING THOUGHT", font=SANS_B(16), fill=MUTED)
    d.text((40, 184), "Launch the AI package now, built into bookkeeping and the month-end close",
           font=SANS_B(24), fill=NAVY)
    y, count = 240, 0
    for si, (sec, titles) in enumerate(SECTIONS, 1):
        d.ellipse((40, y, 72, y + 32), fill=BLUE)
        d.text((56, y + 16), str(si), font=SANS_B(18), fill="white", anchor="mm")
        d.text((86, y + 16), sec, font=SANS_B(22), fill=NAVY, anchor="lm")
        y += 44
        for t in titles:
            if count < shown:
                d.text((86, y), "—  " + t, font=SANS(20), fill=INK)
            count += 1
            y += 31
        y += 14
    return count


def scene_story():
    total = sum(len(t) for _, t in SECTIONS)
    for shown in range(total + 1):
        c, d = base(3, "It writes the storyline. You approve it first.")
        draw_story(d, shown)
        add(c, 0.35 if shown < total else 0.8)
    d.rounded_rectangle((W - 330, 620, W - 40, 680), 30, fill=GREEN)
    check(d, W - 290, 650, 10, "white", 4)
    d.text((W - 265, 650), "Storyline approved", font=SANS_B(22), fill="white", anchor="lm")
    add(c, 1.6)


# ---------- 4. The deck builds ----------
def scene_build():
    cols, gap = 4, 16
    tw = (W - 80 - gap * (cols - 1)) // cols
    th = round(tw * 1080 / 1920)
    thumbs = [thumb(slide(n), tw) for n in range(1, 12)]
    stats = ["Finding the data…", "Sourcing every number…", "Checking against the rules…"]
    for k in range(len(thumbs) + 1):
        c, d = base(4, "It finds the data and builds the deck")
        for i in range(k):
            x, y = 40 + (i % cols) * (tw + gap), 170 + (i // cols) * (th + gap)
            c.paste(thumbs[i], (x, y))
            d.rectangle((x, y, x + tw, y + th), outline=LINE, width=1)
        msg = stats[min(k * len(stats) // len(thumbs), len(stats) - 1)]
        d.text((40 + 3 * (tw + gap), 170 + 2 * (th + gap) + th // 2), msg, font=SANS(20), fill=MUTED, anchor="lm")
        add(c, 0.28)
    c, d = base(4, "It finds the data and builds the deck")
    for i in range(len(thumbs)):
        x, y = 40 + (i % cols) * (tw + gap), 170 + (i // cols) * (th + gap)
        c.paste(thumbs[i], (x, y))
        d.rectangle((x, y, x + tw, y + th), outline=LINE, width=1)
    bx, by = 40 + 3 * (tw + gap), 170 + 2 * (th + gap)
    d.rounded_rectangle((bx, by, bx + tw, by + th), 12, fill=CARD, outline=LINE, width=2)
    for i, (a, b) in enumerate((("49", "data points"), ("10", "sources"), ("0", "QA failures"))):
        d.text((bx + 22, by + 26 + i * 50), a, font=SERIF_B(28), fill=GREEN if a == "0" else NAVY)
        d.text((bx + 80, by + 34 + i * 50), b, font=SANS(19), fill=INK)
    add(c, 1.8)


# ---------- 5. A receipt for every number ----------
def scene_source():
    r = Image.open(OUT / "receipt.png").convert("RGB")
    r = thumb(r, W - 80)
    c, d = base(5, "Every number comes with its source")
    c.paste(r, (40, 170))
    add(c, 2.6)


# ---------- 6. End card ----------
def scene_end():
    c = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(c)
    d.text((W // 2, 210), "hire-your-mck", font=SERIF_B(64), fill="white", anchor="mm")
    d.text((W // 2, 285), "Brief it like a partner. Get the deck in minutes.", font=SANS(30), fill="#C9D6E8", anchor="mm")
    for i, (name, kind) in enumerate((("cobalt-ledger.pptx", "Editable PowerPoint"),
                                      ("cobalt-ledger-sources.xlsx", "Every source, one sheet per slide"))):
        x = W // 2 - 420 + i * 440
        d.rounded_rectangle((x, 350, x + 400, 440), 14, fill="#13304D")
        d.text((x + 24, 372), name, font=SANS_B(22), fill="white")
        d.text((x + 24, 406), kind, font=SANS(18), fill="#9FB3CC")
    cmd = "claude plugin install hire-your-mck --marketplace brianlee0113/hire-your-mck"
    f = ImageFont.truetype("/System/Library/Fonts/Supplemental/Courier New Bold.ttf", 20)
    tw = d.textlength(cmd, font=f) + 48
    d.rounded_rectangle((W // 2 - tw / 2, 510, W // 2 + tw / 2, 566), 10, fill="#06121F")
    d.text((W // 2, 538), cmd, font=f, fill="#E6EDF5", anchor="mm")
    d.text((W // 2, 610), "or upload the zip in Claude.ai", font=SANS(20), fill="#9FB3CC", anchor="mm")
    add(c, 3.2)


def main():
    for s in (scene_brief, scene_pick, scene_story, scene_build, scene_source, scene_end):
        s()
    pal = [f.quantize(colors=128, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE) for f in frames]
    pal[0].save(OUT / "demo.gif", save_all=True, append_images=pal[1:], duration=durations, loop=0, optimize=True)
    print("demo.gif", len(frames), "frames,", round(sum(durations) / 1000, 1), "s,",
          round((OUT / "demo.gif").stat().st_size / 1e6, 2), "MB")
    if shutil.which("ffmpeg"):
        tmp = OUT / "_frames"
        tmp.mkdir(exist_ok=True)
        lst = []
        for i, (f, ms) in enumerate(zip(frames, durations)):
            p = tmp / f"f{i:04d}.png"
            f.save(p)
            lst.append(f"file '{p.name}'\nduration {ms / 1000}")
        lst.append(f"file 'f{len(frames) - 1:04d}.png'")
        (tmp / "list.txt").write_text("\n".join(lst))
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-i", "list.txt", "-fps_mode", "vfr",
                        "-pix_fmt", "yuv420p", "-c:v", "libx264", "-crf", "20", str(OUT / "demo.mp4")],
                       cwd=tmp, check=True)
        shutil.rmtree(tmp)
        print("demo.mp4", round((OUT / "demo.mp4").stat().st_size / 1e6, 2), "MB")


if __name__ == "__main__":
    main()
