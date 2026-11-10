"""Second-pass source check (V-05): open every web source again and look for each excerpt on the page.

Usage: python verify.py <spec.json> [--write] [--only-key] [--timeout 20]

For each web data point with an excerpt, the page (HTML, PDF, XLSX or CSV) is fetched and the excerpt
searched for, first verbatim (case and whitespace ignored), then as a near match around the excerpt's
figures (tables and PDFs often extract with different spacing). Results:
  match        the excerpt is on the page
  not_found    the page opened but the excerpt is not on it (quoted wrongly, or the page changed)
  unreachable  the page could not be opened or read
--write stores them in each data point's "verified" ({result, at, by: "verify.py"}) and keeps any
"verifier" or "user" result already there. Exit code 1 if anything is not_found.
"""
import argparse, datetime, difflib, html, io, json, re, sys, urllib.request

UA = "Mozilla/5.0 (compatible; source-verify/1.0)"


def fetch(url, timeout):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read(), (r.headers.get("Content-Type") or "").lower()


def page_text(body, ctype, url):
    u = url.lower().split("?")[0]
    if "pdf" in ctype or u.endswith(".pdf") or body[:5] == b"%PDF-":
        try:
            import pymupdf
        except ImportError:
            try:
                import fitz as pymupdf
            except ImportError:
                pymupdf = None
        if pymupdf:
            doc = pymupdf.open(stream=body, filetype="pdf")
            return " ".join(p.get_text() for p in doc)
        try:
            from pypdf import PdfReader
            return " ".join((p.extract_text() or "") for p in PdfReader(io.BytesIO(body)).pages)
        except ImportError:
            raise RuntimeError("PDF needs pymupdf or pypdf (pip install pymupdf)")
    if "spreadsheet" in ctype or "excel" in ctype or u.endswith((".xlsx", ".xlsm")) or body[:2] == b"PK":
        from openpyxl import load_workbook
        wb = load_workbook(io.BytesIO(body), read_only=True, data_only=True)
        return [[["" if c is None else str(c) for c in row] for row in ws.iter_rows(values_only=True)] for ws in wb.worksheets]
    if "csv" in ctype or u.endswith(".csv"):
        import csv
        return [list(csv.reader(io.StringIO(body.decode("utf-8", errors="replace"))))]
    if u.endswith(".xls"):
        raise RuntimeError("legacy .xls cannot be read; open it and confirm by hand")
    text = body.decode("utf-8", errors="replace")
    text = re.sub(r"(?is)<(script|style|noscript)[^>]*>.*?</\1>", " ", text)
    text = re.sub(r"(?s)<[^>]+>", " ", text)
    return html.unescape(text)


def norm(t):
    t = t.replace("|", " ")  # excerpts copied from a reader's markdown table
    t = t.replace(" ", " ").replace("’", "'").replace("“", '"').replace("”", '"').replace("–", "-").replace("—", "-")
    return re.sub(r"\s+", " ", t).strip().lower()


def _words(t):
    return set(re.findall(r"[a-z0-9]+", norm(t))) - {"the", "a", "an", "of", "in", "or", "and", "to", "for", "this", "its"}


def find_in_table(excerpt, sheets):
    """Table-cell excerpts ('Q7 "question", answer "Yes"; column 202524 = "17.3%"'): a row holds the
    value (under the named column, when given) and most words of the quoted row labels. Labels may be
    reworded on the live file; the value may not."""
    m = re.search(r'(?:column\s+(\S+)\s*)?=\s*"([^"]+)"\s*$', excerpt.strip())
    if not m:
        return None
    col, val = m.group(1), norm(m.group(2))
    labels = _words(" ".join(re.findall(r'"([^"]+)"', excerpt[:m.start()])))
    for rows in sheets:
        head = next((r for r in rows[:15] if col and col in r), None)
        ci = head.index(col) if head else None
        for r in rows:
            cells = [norm(c) for c in r]
            if (ci is not None and (ci >= len(cells) or cells[ci] != val)) or (ci is None and val not in cells):
                continue
            if not labels or len(labels & _words(" ".join(r))) / len(labels) >= 0.7:
                return True
    return False


def find(excerpt, page):
    """'match' when the excerpt is on the page verbatim or nearly (≥ 0.85 similar around one of its figures)."""
    if isinstance(page, list):  # spreadsheet: list of sheets of rows
        got = find_in_table(excerpt, page)
        if got is not None:
            return got
        page = " ".join(" ".join(r) for rows in page for r in rows)
    e, p = norm(excerpt), norm(page)
    if e in p:
        return True
    # ellipses in a quote: every fragment must be on the page
    frags = [f.strip() for f in re.split(r"\[?(?:\.\.\.|…)\]?", e) if len(f.strip()) > 12]
    if len(frags) > 1 and all(f in p for f in frags):
        return True
    nums = sorted(set(re.findall(r"\d[\d,.]*\d|\d", e)), key=len, reverse=True)
    anchors = [n for n in nums if len(n) >= 2] or nums
    if not anchors:
        return False
    best = 0.0
    for a in anchors[:3]:
        for m in list(re.finditer(re.escape(a), p))[:200]:
            lo = max(0, m.start() - len(e))
            win = p[lo:m.end() + len(e)]
            # spacing and wording may differ, figures may not: every figure of the excerpt is in the window
            if not all(re.search(rf"(?<![\d.]){re.escape(n)}(?![\d])", win) for n in nums):
                continue
            sm = difflib.SequenceMatcher(None, e, win, autojunk=False)
            blocks = sum(b.size for b in sm.get_matching_blocks())
            best = max(best, blocks / len(e))
            if best >= 0.85:
                return True
    return False


def key_refs(spec):
    def refs(o):
        if isinstance(o, dict):
            return ([o["data_ref"]] if "data_ref" in o else []) + [r for v in o.values() for r in refs(v)]
        if isinstance(o, list):
            return [r for v in o for r in refs(v)]
        return []
    out = set()
    for s in spec["slides"]:
        if s["role"] == "content":
            out |= set(refs(s.get("lead_message") or {}))
    return out | set(refs(spec["storyline"].get("exec_summary", [])))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("spec")
    ap.add_argument("--write", action="store_true", help="store results in the spec")
    ap.add_argument("--only-key", action="store_true", help="only numbers in titles and the exec summary")
    ap.add_argument("--timeout", type=float, default=20)
    a = ap.parse_args()
    spec = json.load(open(a.spec))
    srcs = {s["id"]: s for s in spec.get("sources", [])}
    key = key_refs(spec)
    today = datetime.date.today().isoformat()
    todo = {}
    for d in spec.get("data_points", []):
        s = srcs.get(d.get("source_id"), {})
        if s.get("kind") != "web" or not s.get("url") or not d.get("excerpt") or d.get("estimate"):
            continue
        if a.only_key and d["id"] not in key:
            continue
        if (d.get("verified") or {}).get("by") in ("verifier", "user"):
            continue  # a person or an independent verifier already read the page
        todo.setdefault(s["id"], []).append(d)
    counts = {"match": 0, "not_found": 0, "unreachable": 0}
    for sid, items in todo.items():
        url = srcs[sid]["url"]
        try:
            body, ctype = fetch(url, a.timeout)
            page = page_text(body, ctype, url)
            err = None
        except Exception as ex:  # network, HTTP status, unreadable format
            page, err = None, f"{type(ex).__name__}: {str(ex)[:80]}"
        print(f"{sid}  {url[:90]}" + (f"  [{err}]" if err else ""))
        for d in items:
            res = "unreachable" if page is None else ("match" if find(d["excerpt"], page) else "not_found")
            counts[res] += 1
            mark = {"match": "ok ", "not_found": "!! ", "unreachable": "?? "}[res]
            print(f"   {mark}{d['id']:10s} {res:11s} \"{d['excerpt'][:70]}\"")
            if a.write:
                d["verified"] = {"result": res, "at": today, "by": "verify.py"} | ({"note": err} if err else {})
    if a.write:
        raw = open(a.spec).read()
        indent = 1 if re.search(r'^\{\n "', raw) else 2
        with open(a.spec, "w") as f:
            json.dump(spec, f, indent=indent, ensure_ascii=False)
            f.write("\n")
    print(f"\n{counts['match']} match · {counts['not_found']} not found · {counts['unreachable']} unreachable"
          + ("" if a.write else "  (dry run; --write stores the results)"))
    sys.exit(1 if counts["not_found"] else 0)


if __name__ == "__main__":
    main()
