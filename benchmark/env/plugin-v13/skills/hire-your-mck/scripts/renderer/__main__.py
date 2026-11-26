"""Usage: python -m renderer <spec.json> [--out DIR] [--theme navy] [--font-pair arial]"""
import argparse
import json
import os
import sys

from . import pptx_render, tokens, xlsx_render


def main(argv=None):
    ap = argparse.ArgumentParser(prog="python -m renderer")
    ap.add_argument("spec")
    ap.add_argument("--out", default="output")
    ap.add_argument("--theme", default=None, help="Overrides meta.theme")
    ap.add_argument("--font-pair", default=None, help="Overrides meta.font_pair")
    args = ap.parse_args(argv)
    with open(args.spec, encoding="utf-8") as f:
        spec = json.load(f)
    os.makedirs(args.out, exist_ok=True)
    base = os.path.splitext(os.path.basename(args.spec))[0]
    deck = pptx_render.render(spec, os.path.join(args.out, base + ".pptx"), args.theme, args.font_pair)
    tok = tokens.resolve(deck["theme"])
    book = xlsx_render.render(spec, os.path.join(args.out, base + "-sources.xlsx"), tok["primary"])
    print(f"{deck['path']}  ({deck['slides']} slides, theme {deck['theme']}, fonts {deck['font_pair']})")
    print(f"{book['path']}  ({book['sheets']} sheets)")
    for w in deck["warnings"]:
        print("warn:", w)
    return 0


if __name__ == "__main__":
    sys.exit(main())
