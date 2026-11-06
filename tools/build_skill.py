"""Assemble the Claude Skill from repo sources (no copies kept in the repo).

Usage: python tools/build_skill.py            -> dist/hire-your-mck/ and dist/hire-your-mck.zip
"""
import pathlib
import shutil
import zipfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
NAME = "hire-your-mck"
OUT = ROOT / "dist" / NAME

RENDER_WRAPPER = '''"""Render a storyline spec. Usage: python render.py <spec.json> [--out DIR] [--theme navy] [--font-pair arial]"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from renderer.__main__ import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main())
'''


def build():
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "references").mkdir(parents=True)
    (OUT / "examples").mkdir()
    (OUT / "scripts" / "renderer").mkdir(parents=True)
    (OUT / "scripts" / "templates").mkdir()

    shutil.copy(ROOT / "skill" / "SKILL.md", OUT / "SKILL.md")
    for f in (ROOT / "skill" / "references").glob("*.md"):
        shutil.copy(f, OUT / "references" / f.name)
    shutil.copy(ROOT / "docs/spec/examples/example-deck.json", OUT / "examples" / "example-deck.json")
    for f in (ROOT / "renderer" / "examples").glob("*.json"):
        shutil.copy(f, OUT / "examples" / f.name)

    shutil.copy(ROOT / "tools/spec/check.py", OUT / "scripts" / "check.py")
    shutil.copy(ROOT / "docs/spec/storyline.schema.json", OUT / "scripts" / "storyline.schema.json")
    for f in (ROOT / "renderer").glob("*.py"):
        shutil.copy(f, OUT / "scripts" / "renderer" / f.name)
    shutil.copy(ROOT / "templates" / "themes.json", OUT / "scripts" / "templates" / "themes.json")
    (OUT / "scripts" / "render.py").write_text(RENDER_WRAPPER)
    (OUT / "scripts" / "requirements.txt").write_text("python-pptx>=1.0.0\nopenpyxl>=3.1\njsonschema>=4.0\npillow>=9.0\n")

    zpath = OUT.parent / f"{NAME}.zip"
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(OUT.rglob("*")):
            if f.is_file() and "__pycache__" not in f.parts:
                z.write(f, f.relative_to(OUT.parent))
    files = [f for f in OUT.rglob("*") if f.is_file()]
    print(f"{OUT}  ({len(files)} files)")
    print(f"{zpath}  ({zpath.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    build()
