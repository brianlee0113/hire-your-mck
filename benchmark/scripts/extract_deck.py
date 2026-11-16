"""Deterministic, non-editorial text extraction from each run's deliverable.

For every run: find the delivered deck (.pptx; otherwise .md/.txt/.html in deliverable/), dump everything a reader
could see — text in reading order, tables, native chart data, speaker notes, and a marker for pictures — and write
  runs/<phase>/<run_id>/extract/deck.json   structured dump
  runs/<phase>/<run_id>/extract/deck.txt    plain text, one block per slide
  runs/<phase>/<run_id>/extract/images/     pictures embedded in the deck (for transcription during normalisation)

Usage: python benchmark/scripts/extract_deck.py --phase pilot
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from common import BENCH  # noqa: E402

from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE
from pptx.util import Emu


def shape_items(shape, slide_w, dx=0, dy=0):
    """Yield (top, left, kind, payload) for every visible element, recursing into groups."""
    top = (shape.top or 0) + dy
    left = (shape.left or 0) + dx
    if shape.shape_type == MSO_SHAPE_TYPE.GROUP:
        for s in shape.shapes:
            yield from shape_items(s, slide_w, 0, 0)
        return
    if getattr(shape, "has_chart", False) and shape.has_chart:
        ch = shape.chart
        data = {"chart_type": str(ch.chart_type).split(".")[-1].split(" ")[0], "title": None, "series": []}
        try:
            if ch.has_title and ch.chart_title.has_text_frame:
                data["title"] = ch.chart_title.text_frame.text
        except Exception:
            pass
        try:
            cats = [str(c) for c in ch.plots[0].categories]
        except Exception:
            cats = []
        data["categories"] = cats
        for plot in ch.plots:
            for s in plot.series:
                try:
                    vals = list(s.values)
                except Exception:
                    vals = []
                data["series"].append({"name": s.name, "values": [None if v is None else round(float(v), 6) for v in vals]})
        yield top, left, "chart", data
        return
    if getattr(shape, "has_table", False) and shape.has_table:
        rows = []
        for r in shape.table.rows:
            rows.append([c.text_frame.text.strip() if c.text_frame else "" for c in r.cells])
        yield top, left, "table", rows
        return
    if shape.shape_type == MSO_SHAPE_TYPE.PICTURE:
        try:
            alt = shape._element.xpath("./p:nvPicPr/p:cNvPr/@descr")
        except Exception:
            alt = []
        yield top, left, "picture", {"name": shape.name, "alt": alt[0] if alt else "", "image": shape}
        return
    if getattr(shape, "has_text_frame", False) and shape.has_text_frame:
        paras = []
        max_pt = 0
        for p in shape.text_frame.paragraphs:
            t = "".join(r.text for r in p.runs) or p.text
            t = t.strip()
            if not t:
                continue
            for r in p.runs:
                if r.font.size:
                    max_pt = max(max_pt, r.font.size.pt)
            paras.append({"text": t, "level": p.level})
        if paras:
            is_title = bool(shape.is_placeholder and "TITLE" in str(shape.placeholder_format.type))
            yield top, left, "text", {"paragraphs": paras, "max_pt": max_pt, "is_title_placeholder": is_title}


def extract_pptx(path: pathlib.Path, img_dir: pathlib.Path):
    prs = Presentation(str(path))
    sw = prs.slide_width or Emu(12192000)
    slides = []
    n_img = 0
    for i, slide in enumerate(prs.slides, 1):
        items = []
        for sh in slide.shapes:
            items.extend(shape_items(sh, sw))
        # reading order: top to bottom in bands of ~0.25 in, then left to right
        items.sort(key=lambda x: (round(x[0] / 228600), x[1]))
        elements, title = [], None
        texts = [it for it in items if it[2] == "text"]
        tp = [t for t in texts if t[3]["is_title_placeholder"]]
        NAV = {"contents", "agenda", "appendix", "backup", "table of contents", "overview"}
        slide_max = max((t[3]["max_pt"] for t in texts), default=0)
        nav = [t for t in texts if len(t[3]["paragraphs"]) == 1 and t[3]["paragraphs"][0]["text"].strip().lower().rstrip(":") in NAV
               and t[3]["max_pt"] >= 0.8 * slide_max]
        if tp:
            title = " ".join(p["text"] for p in tp[0][3]["paragraphs"])
        elif nav:
            # navigation slide (agenda tracker, appendix divider): its heading is the title, not a list item;
            # a small "APPENDIX" kicker above a real title does not qualify (font-size test)
            title = max(nav, key=lambda t: t[3]["max_pt"])[3]["paragraphs"][0]["text"].strip()
        elif texts:
            # largest font in the top 40% of the slide
            def wordy(t):
                s = " ".join(p["text"] for p in t[3]["paragraphs"])
                return len(re.findall(r"[A-Za-z]{2,}", s)) >= 2
            top_texts = [t for t in texts if t[0] < 0.4 * (prs.slide_height or 6858000) and wordy(t)] or [t for t in texts if wordy(t)] or texts
            best = max(top_texts, key=lambda t: (t[3]["max_pt"], -t[0]))
            title = " ".join(p["text"] for p in best[3]["paragraphs"])
        for top, left, kind, payload in items:
            if kind == "picture":
                n_img += 1
                img = payload.pop("image")
                try:
                    ext = img.image.ext
                    fn = f"s{i:02d}-img{n_img:02d}.{ext}"
                    img_dir.mkdir(parents=True, exist_ok=True)
                    (img_dir / fn).write_bytes(img.image.blob)
                    payload["file"] = fn
                except Exception:
                    payload["file"] = None
            elements.append({"kind": kind, **({"data": payload} if kind != "text" else payload)})
        notes = ""
        if slide.has_notes_slide and slide.notes_slide.notes_text_frame is not None:
            notes = slide.notes_slide.notes_text_frame.text.strip()
        slides.append({"n": i, "title": title, "elements": elements, "notes": notes})
    return {"source": path.name, "format": "pptx", "slides": slides}


def to_text(deck) -> str:
    out = []
    for s in deck["slides"]:
        out.append(f"=== Slide {s['n']} ===")
        if s.get("title"):
            out.append(f"[Title] {s['title']}")
        for e in s["elements"]:
            if e["kind"] == "text":
                for p in e["paragraphs"]:
                    if p["text"] == s.get("title"):
                        continue
                    out.append(("  " * p["level"]) + "- " + p["text"])
            elif e["kind"] == "table":
                out.append("[Table]")
                for r in e["data"]:
                    out.append("  | " + " | ".join(c.replace("\n", " / ") for c in r) + " |")
            elif e["kind"] == "chart":
                d = e["data"]
                out.append(f"[Chart: {d['chart_type']}{' — ' + d['title'] if d.get('title') else ''}]")
                out.append("  categories: " + "; ".join(d.get("categories", [])))
                for se in d["series"]:
                    out.append(f"  series {se['name']!r}: " + "; ".join("" if v is None else f"{v:g}" for v in se["values"]))
            elif e["kind"] == "picture":
                out.append(f"[Picture{': ' + e['data']['alt'] if e['data'].get('alt') else ''} (file {e['data'].get('file')})]")
        if s.get("notes"):
            out.append("[Speaker notes] " + s["notes"])
        out.append("")
    return "\n".join(out)


def extract_pdf(path: pathlib.Path):
    """A deck delivered as PDF: one page = one slide; text in reading order (no chart data available)."""
    import pymupdf
    slides = []
    with pymupdf.open(str(path)) as doc:
        pages = []
        for page in doc:
            blocks = sorted(page.get_text("blocks"), key=lambda b: (round(b[1] / 18), b[0]))
            pages.append([" ".join(b[4].split()) for b in blocks if b[4].strip()])
        from collections import Counter
        freq = Counter(t for p in pages for t in set(p))
        running = {t for t, n in freq.items() if len(pages) > 3 and n > 0.4 * len(pages)}  # running headers/footers
        for i, texts in enumerate(pages, 1):
            paras = [{"text": t, "level": 0} for t in texts]
            title = next((t for t in texts if t not in running), None)
            slides.append({"n": i, "title": title,
                           "elements": [{"kind": "text", "paragraphs": [p for p in paras if p["text"] != title], "max_pt": 0, "is_title_placeholder": False}],
                           "notes": ""})
    return {"source": path.name, "format": "pdf", "slides": slides}


def extract_text_file(path: pathlib.Path):
    txt = path.read_text(errors="replace")
    if path.suffix.lower() in (".html", ".htm"):
        txt = re.sub(r"<script.*?</script>|<style.*?</style>", " ", txt, flags=re.S)
        txt = re.sub(r"<[^>]+>", " ", txt)
        txt = re.sub(r"[ \t]+", " ", txt)
    return {"source": path.name, "format": path.suffix.lower().lstrip("."), "slides": [], "raw_text": txt}


def pick_deliverable(ws: pathlib.Path):
    d = ws / "deliverable"
    files = [p for p in d.rglob("*") if p.is_file() and not p.name.startswith("~$")]
    pptx = sorted([p for p in files if p.suffix.lower() == ".pptx"], key=lambda p: -p.stat().st_size)
    if pptx:
        return pptx[0], files
    for ext in (".pdf", ".md", ".txt", ".html"):
        cand = sorted([p for p in files if p.suffix.lower() == ext], key=lambda p: -p.stat().st_size)
        if cand:
            return cand[0], files
    return None, files


def process(run_dir: pathlib.Path):
    ws = run_dir / "workspace"
    out = run_dir / "extract"
    out.mkdir(exist_ok=True)
    main, files = pick_deliverable(ws)
    if main is None:
        rec = {"source": None, "format": None, "slides": [], "error": "no deliverable"}
        txt = ""
    elif main.suffix.lower() == ".pptx":
        try:
            rec = extract_pptx(main, out / "images")
            txt = to_text(rec)
        except Exception as e:
            rec = {"source": main.name, "format": "pptx", "slides": [], "error": f"unreadable pptx: {e!r}"}
            txt = ""
    elif main.suffix.lower() == ".pdf":
        rec = extract_pdf(main)
        txt = to_text(rec)
    else:
        rec = extract_text_file(main)
        txt = rec["raw_text"]
    rec["deliverable_files"] = [str(p.relative_to(ws)) for p in files]
    rec["n_slides"] = len(rec.get("slides", []))
    rec["n_pictures"] = sum(1 for s in rec.get("slides", []) for e in s["elements"] if e["kind"] == "picture")
    rec["n_native_charts"] = sum(1 for s in rec.get("slides", []) for e in s["elements"] if e["kind"] == "chart")
    rec["n_tables"] = sum(1 for s in rec.get("slides", []) for e in s["elements"] if e["kind"] == "table")
    rec["words"] = len(re.findall(r"\b[\w'’.%$-]+\b", txt))
    (out / "deck.json").write_text(json.dumps(rec, indent=1, ensure_ascii=False))
    (out / "deck.txt").write_text(txt)
    return rec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--phase", required=True)
    a = ap.parse_args()
    for run_dir in sorted((BENCH / "runs" / a.phase).glob(f"{a.phase}-*")):
        if not (run_dir / "meta.json").exists():
            continue
        rec = process(run_dir)
        print(f"{run_dir.name}: {rec.get('format')} {rec['n_slides']} slides · {rec['words']:,} words · "
              f"{rec['n_native_charts']} charts · {rec['n_pictures']} pictures · {rec.get('error', '')}")


if __name__ == "__main__":
    main()
