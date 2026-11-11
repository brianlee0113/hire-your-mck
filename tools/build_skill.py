"""Assemble the Claude Skill from repo sources.

The assembled skill is committed at plugin/skills/hire-your-mck/ so Claude Code can install it as a
plugin straight from GitHub; the zip for Claude.ai goes to dist/ (attached to GitHub releases).

Usage: python tools/build_skill.py           -> plugin/skills/hire-your-mck/ and dist/hire-your-mck.zip
       python tools/build_skill.py --check   -> exit 1 if the committed plugin copy is out of date
"""
import filecmp
import pathlib
import shutil
import sys
import tempfile
import zipfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
NAME = "hire-your-mck"
OUT = ROOT / "plugin" / "skills" / NAME
DIST = ROOT / "dist"

RENDER_WRAPPER = '''"""Render a storyline spec. Usage: python render.py <spec.json> [--out DIR] [--theme navy] [--font-pair arial]"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from renderer.__main__ import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main())
'''


def build(OUT=OUT, zip_it=True):
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "references").mkdir(parents=True)
    (OUT / "examples").mkdir()
    (OUT / "scripts" / "renderer").mkdir(parents=True)
    (OUT / "scripts" / "templates").mkdir()

    # The source is SKILL.src.md so that skill installers (e.g. `npx skills add`) find only the built copy
    shutil.copy(ROOT / "skill" / "SKILL.src.md", OUT / "SKILL.md")
    for f in (ROOT / "skill" / "references").glob("*.md"):
        shutil.copy(f, OUT / "references" / f.name)
    shutil.copy(ROOT / "docs/spec/examples/example-deck.json", OUT / "examples" / "example-deck.json")
    for f in (ROOT / "renderer" / "examples").glob("*.json"):
        shutil.copy(f, OUT / "examples" / f.name)

    shutil.copy(ROOT / "tools/spec/check.py", OUT / "scripts" / "check.py")
    shutil.copy(ROOT / "tools/spec/verify.py", OUT / "scripts" / "verify.py")
    shutil.copy(ROOT / "docs/spec/storyline.schema.json", OUT / "scripts" / "storyline.schema.json")
    for f in (ROOT / "renderer").glob("*.py"):
        shutil.copy(f, OUT / "scripts" / "renderer" / f.name)
    (OUT / "scripts" / "renderer" / "geo").mkdir()
    for f in (ROOT / "renderer" / "geo").glob("*.json"):  # map outlines (Natural Earth, public domain)
        shutil.copy(f, OUT / "scripts" / "renderer" / "geo" / f.name)
    shutil.copy(ROOT / "templates" / "themes.json", OUT / "scripts" / "templates" / "themes.json")
    (OUT / "scripts" / "render.py").write_text(RENDER_WRAPPER)
    (OUT / "scripts" / "requirements.txt").write_text("python-pptx>=1.0.0\nopenpyxl>=3.1\njsonschema>=4.0\npillow>=9.0\n")

    if not zip_it:
        return
    DIST.mkdir(exist_ok=True)
    zpath = DIST / f"{NAME}.zip"
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(OUT.rglob("*")):
            if f.is_file() and "__pycache__" not in f.parts:
                z.write(f, f.relative_to(OUT.parent))
    files = [f for f in OUT.rglob("*") if f.is_file()]
    print(f"{OUT}  ({len(files)} files)")
    print(f"{zpath}  ({zpath.stat().st_size // 1024} KB)")


def check():
    with tempfile.TemporaryDirectory() as tmp:
        fresh = pathlib.Path(tmp) / NAME
        build(fresh, zip_it=False)
        def diff(cmp):
            out = cmp.left_only + cmp.right_only + cmp.diff_files
            for sub in cmp.subdirs.values():
                out += diff(sub)
            return [x for x in out if x != "__pycache__"]
        stale = diff(filecmp.dircmp(fresh, OUT, ignore=["__pycache__"])) if OUT.exists() else ["(missing)"]
    if stale:
        print("plugin copy is out of date; run python tools/build_skill.py:", ", ".join(sorted(set(stale))))
        sys.exit(1)
    print("plugin copy is up to date")


if __name__ == "__main__":
    check() if "--check" in sys.argv else build()
