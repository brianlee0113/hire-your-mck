"""Write transcript-*.slim.jsonl.gz next to every transcript, with base64 image data replaced by its SHA-256 and size.

The full transcripts (slide previews the agents rendered and looked at) stay local and are git-ignored; the slim
copies are committed. Nothing else is changed.
Usage: python benchmark/scripts/slim_transcripts.py
"""
import base64
import gzip
import hashlib
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from common import BENCH  # noqa: E402


def slim(o):
    if isinstance(o, dict):
        if o.get("type") == "base64" and isinstance(o.get("data"), str) and len(o["data"]) > 1000:
            raw = base64.b64decode(o["data"], validate=False)
            return {"type": "base64", "media_type": o.get("media_type"), "omitted": True,
                    "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw)}
        return {k: slim(v) for k, v in o.items()}
    if isinstance(o, list):
        return [slim(v) for v in o]
    if isinstance(o, str) and len(o) > 5000 and B64.fullmatch(o[:4000]):
        return {"omitted_base64": True, "sha256": hashlib.sha256(o.encode()).hexdigest(), "chars": len(o)}
    return o


B64 = re.compile(r"[A-Za-z0-9+/=\s]+")


def main():
    n = 0
    for p in sorted(BENCH.glob("runs/**/transcript-attempt*.jsonl.gz")):
        if p.name.endswith(".slim.jsonl.gz"):
            continue
        out = p.with_name(p.name.replace(".jsonl.gz", ".slim.jsonl.gz"))
        with gzip.open(p, "rt") as f, gzip.open(out, "wt") as g:
            for line in f:
                try:
                    g.write(json.dumps(slim(json.loads(line))) + "\n")
                except json.JSONDecodeError:
                    g.write(line)
        n += 1
    print(f"slimmed {n} transcripts")


if __name__ == "__main__":
    main()
