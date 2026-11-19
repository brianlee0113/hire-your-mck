"""Render a storyline spec. Usage: python render.py <spec.json> [--out DIR] [--theme navy] [--font-pair arial]"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from renderer.__main__ import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main())
