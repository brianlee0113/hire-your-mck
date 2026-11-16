"""End-to-end product metrics, reported separately from reasoning quality.

Per run: was a .pptx delivered and does it open; slide count; native (editable) charts vs pictures; tables; a
source workbook or other traceability artefact; the share of numbers in the deck that appear in the briefing pack
(directly traceable) — a crude, deterministic proxy, since derived numbers are legitimately absent from the pack;
the share of content slides that cite a source; and, for Hire Your McK runs, the product's own check.py result
(shown for completeness — it is the product's self-check, not an independent measure).

Usage: python benchmark/scripts/e2e_metrics.py --phase pilot
Writes runs/<phase>/<run_id>/e2e.json and results/<phase>/e2e.csv
"""
from __future__ import annotations

import argparse
import csv
import json
import pathlib
import re
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from common import BENCH, CONFIG, REPO  # noqa: E402

NUM = re.compile(r"(?<![\w.])[$€£]?\d[\d,]*(?:\.\d+)?\s*(?:%|pp|x|M|B|K|k|bn|million|billion)?", re.I)


def norm_num(s):
    s = s.strip().lower().replace(",", "").replace("$", "")
    m = re.match(r"(\d+(?:\.\d+)?)", s)
    return float(m.group(1)) if m else None


def numbers(text):
    out = []
    for m in NUM.finditer(text):
        v = norm_num(m.group(0))
        if v is None:
            continue
        if 1900 <= v <= 2100 and re.fullmatch(r"\d{4}", m.group(0).strip()):
            continue  # years
        if v < 10 and re.fullmatch(r"\d", m.group(0).strip()):
            continue  # single digits (list numbers, slide numbers)
        out.append(v)
    return out


def traceable_share(deck_text, packet_text):
    pk = set()
    for v in numbers(packet_text):
        pk.add(round(v, 2))
        pk.add(round(v, 1))
        pk.add(round(v))
    vals = numbers(deck_text)
    if not vals:
        return None, 0
    hit = sum(1 for v in vals if round(v, 2) in pk or round(v, 1) in pk)
    return hit / len(vals), len(vals)


def metrics(run_dir: pathlib.Path):
    meta = json.loads((run_dir / "meta.json").read_text())
    ws = run_dir / "workspace"
    deck = json.loads((run_dir / "extract" / "deck.json").read_text()) if (run_dir / "extract" / "deck.json").exists() else {}
    files = [p for p in (ws / "deliverable").rglob("*") if p.is_file()]
    pptx = [p for p in files if p.suffix.lower() == ".pptx"]
    xlsx = [p for p in files if p.suffix.lower() == ".xlsx"]
    specs = [p for p in ws.rglob("*.json") if p.is_file() and '"slides"' in p.read_text(errors="ignore")[:200000]]
    text = (run_dir / "extract" / "deck.txt").read_text() if (run_dir / "extract" / "deck.txt").exists() else ""
    packet = (BENCH / "cases" / meta["case"] / "packet.md").read_text()
    share, n_nums = traceable_share(text, packet)
    slides = deck.get("slides", [])
    content = [s for s in slides if len(s.get("elements", [])) > 2]
    cites = sum(1 for s in content if re.search(r"\bsource", json.dumps(s), re.I))
    rec = {"run_id": meta["run_id"], "case": meta["case"], "condition": meta["condition"], "status": meta["status"],
           "pptx_delivered": bool(pptx), "pptx_opens": bool(pptx) and not deck.get("error"), "deliverable_files": len(files),
           "slides": deck.get("n_slides", 0), "words": deck.get("words", 0), "native_charts": deck.get("n_native_charts", 0),
           "pictures": deck.get("n_pictures", 0), "tables": deck.get("n_tables", 0), "source_workbook": bool(xlsx),
           "numbers_in_deck": n_nums, "share_numbers_in_pack": share,
           "share_content_slides_citing_source": (cites / len(content)) if content else None,
           "spec_json": bool(specs), "check_py": None}
    if CONFIG["conditions"][meta["condition"]]["plugin"] and specs:
        spec = max(specs, key=lambda p: p.stat().st_size)
        r = subprocess.run([sys.executable, str(REPO / "tools" / "spec" / "check.py"), str(spec)], capture_output=True, text=True)
        last = (r.stdout.strip().splitlines() or [""])[-1]
        m = re.search(r"(\d+) fail · (\d+) warn", last)
        rec["check_py"] = {"exit": r.returncode, "summary": last, "fail": int(m.group(1)) if m else None, "warn": int(m.group(2)) if m else None}
    (run_dir / "e2e.json").write_text(json.dumps(rec, indent=1))
    return rec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--phase", required=True)
    a = ap.parse_args()
    rows = [metrics(d) for d in sorted((BENCH / "runs" / a.phase).glob(f"{a.phase}-*")) if (d / "meta.json").exists()]
    out = BENCH / "results" / a.phase
    out.mkdir(parents=True, exist_ok=True)
    flat = [{k: (json.dumps(v) if isinstance(v, dict) else v) for k, v in r.items()} for r in rows]
    if flat:
        with open(out / "e2e.csv", "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(flat[0]))
            w.writeheader()
            w.writerows(flat)
    for r in rows:
        print(r["run_id"], {k: r[k] for k in ("slides", "native_charts", "pictures", "source_workbook", "share_numbers_in_pack", "check_py")})


if __name__ == "__main__":
    main()
