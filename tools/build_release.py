"""Build the two pieces for the Claude plugin directory.

The directory accepts only Markdown, text, JSON, YAML and images from unverified organizations,
so the skill there carries no scripts. The renderer and the checker ship as a PyPI package
instead, and the directory's skill calls them with `uvx hire-your-mck ...`.

Usage: python tools/build_release.py                 -> dist/pypi/ (package source) and dist/directory/
       python tools/build_release.py --directory DIR -> only the directory plugin, written to DIR
                                                        (keeps DIR/.git, replaces everything else)

Then: cd dist/pypi && uv build && uv publish
"""
import pathlib
import re
import shutil
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
NAME = "hire-your-mck"
PKG = "hire_your_mck"
VERSION = "1.1.0"
DIST = ROOT / "dist"
ALLOWED = {".md", ".txt", ".json", ".yaml", ".yml", ".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico"}

PYPROJECT = f'''[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "{NAME}"
version = "{VERSION}"
description = "Render consulting-style PowerPoint decks and source workbooks from a storyline spec"
readme = "README.md"
license = "MIT"
license-files = ["LICENSE"]
authors = [{{ name = "Brian Lee" }}]
requires-python = ">=3.9"
dependencies = ["python-pptx>=1.0.0", "openpyxl>=3.1", "jsonschema>=4.0", "pillow>=9.0"]

[project.urls]
Homepage = "https://github.com/brianlee0113/hire-your-mck"

[project.scripts]
{NAME} = "{PKG}.cli:main"

[tool.hatch.build.targets.wheel]
packages = ["src/{PKG}"]
'''

CLI = f'''"""Usage: {NAME} check <spec.json>
       {NAME} render <spec.json> [--out DIR] [--theme navy] [--font-pair arial]"""
import pathlib
import runpy
import sys

HERE = pathlib.Path(__file__).resolve().parent


def main():
    cmd, args = (sys.argv[1], sys.argv[2:]) if len(sys.argv) > 1 else (None, [])
    if cmd == "check":
        sys.argv = ["{NAME} check", *args]
        runpy.run_path(str(HERE / "check.py"), run_name="__main__")
        return 0
    if cmd == "render":
        from .renderer.__main__ import main as render
        return render(args)
    if cmd in ("--version", "-V"):
        print("{NAME} {VERSION}")
        return 0
    print(__doc__)
    return 0 if cmd in ("-h", "--help") else 2


if __name__ == "__main__":
    sys.exit(main())
'''

PKG_README = f"""# {NAME}

The renderer and checker behind the [{NAME}](https://github.com/brianlee0113/hire-your-mck) Claude Skill.

```
uvx {NAME} check spec.json
uvx {NAME} render spec.json --out output [--theme navy]
```

`render` writes `<spec>.pptx` (editable PowerPoint, native charts) and `<spec>-sources.xlsx`
(one sheet per content slide, a source for every number).
"""

PLUGIN_README = f"""# {NAME}

**Brief it like a partner. Get the deck in minutes.**

A Claude Skill that turns your research, or just the decision you need to make, into a
McKinsey-style PowerPoint deck. It hands you two files:

- `<name>.pptx`: an editable deck with a storyline that holds together, an action title on every
  slide, and native PowerPoint charts you can edit
- `<name>-sources.xlsx`: a source workbook, one sheet per slide, with the value, source, URL and
  a verbatim excerpt for every number, and a live Excel formula for anything calculated

It never invents a number. A number without a source shows as "?" with a note on the data needed.

## How to use it

Brief it in plain words, for example:

> Our CEO has to decide whether to launch an AI package for our small-business customers.
> Build the deck from public data.

It asks a few multiple-choice questions (audience, decision, material, look), shows you the
storyline for approval, finds and sources the data slide by slide, checks the deck against its
rules, and renders the files. It can also build a storyline-only "ghost deck" or a single slide.

## Setup

The skill renders with the [`{NAME}`](https://pypi.org/project/{NAME}/) Python package, run through
[`uv`](https://docs.astral.sh/uv/): `uvx {NAME}` downloads it on first use. Without `uv`, run
`pip install {NAME}` (Python 3.9 or later). Nothing else to configure.

Source code, examples and the rules behind the slides:
[github.com/brianlee0113/hire-your-mck](https://github.com/brianlee0113/hire-your-mck).

MIT licensed. Not affiliated with or endorsed by McKinsey & Company.
"""

# SKILL.md and references: script paths -> package commands
SUBS = [
    ("python <skill>/scripts/check.py spec.json ", f"uvx {NAME} check spec.json  "),
    ("python <skill>/scripts/render.py spec.json", f"uvx {NAME} render spec.json"),
    ("Install if missing: `pip install python-pptx openpyxl jsonschema pillow` (Pillow measures text with the real fonts so nothing overflows).",
     f"`uvx` fetches the `{NAME}` package from PyPI on first run. Without `uv`: `pip install {NAME}`, then drop the `uvx`."),
    ("`scripts/templates/themes.json`", "`references/themes.json`"),
    ("`scripts/storyline.schema.json`", "`references/storyline.schema.json`"),
    ("`check.py`", f"`{NAME} check`"),
    ("`render.py`", f"`{NAME} render`"),
    ("check.py", f"`{NAME} check`"),
]


def substitute(text, path):
    for old, new in SUBS:
        text = text.replace(old, new)
    left = re.findall(r"scripts/|\.py\b", text)
    if left:
        sys.exit(f"{path}: script reference left after substitution: {left}")
    return text


def build_package(out=DIST / "pypi"):
    if out.exists():
        shutil.rmtree(out)
    src = out / "src" / PKG
    (src / "renderer").mkdir(parents=True)
    (src / "templates").mkdir()
    for f in (ROOT / "renderer").glob("*.py"):
        shutil.copy(f, src / "renderer" / f.name)
    (src / "renderer" / "geo").mkdir()
    for f in (ROOT / "renderer" / "geo").glob("*.json"):  # map outlines (Natural Earth, public domain)
        shutil.copy(f, src / "renderer" / "geo" / f.name)
    shutil.copy(ROOT / "tools/spec/check.py", src / "check.py")
    shutil.copy(ROOT / "docs/spec/storyline.schema.json", src / "storyline.schema.json")
    shutil.copy(ROOT / "templates/themes.json", src / "templates" / "themes.json")
    (src / "__init__.py").write_text(f'__version__ = "{VERSION}"\n')
    (src / "cli.py").write_text(CLI)
    (out / "pyproject.toml").write_text(PYPROJECT)
    (out / "README.md").write_text(PKG_README)
    shutil.copy(ROOT / "LICENSE", out / "LICENSE")
    print(out)


def build_directory(out=DIST / "directory"):
    out.mkdir(parents=True, exist_ok=True)
    for f in out.iterdir():
        if f.name != ".git":
            shutil.rmtree(f) if f.is_dir() else f.unlink()
    shutil.copytree(ROOT / ".claude-plugin", out / ".claude-plugin")
    (out / "plugin" / ".claude-plugin").mkdir(parents=True)
    for f in ("plugin.json", "icon.png"):
        shutil.copy(ROOT / "plugin/.claude-plugin" / f, out / "plugin/.claude-plugin" / f)
    skill = out / "plugin" / "skills" / NAME
    (skill / "references").mkdir(parents=True)
    (skill / "examples").mkdir()
    (skill / "SKILL.md").write_text(substitute((ROOT / "skill/SKILL.src.md").read_text(), "SKILL.md"))
    for f in (ROOT / "skill/references").glob("*.md"):
        (skill / "references" / f.name).write_text(substitute(f.read_text(), f.name))
    shutil.copy(ROOT / "docs/spec/storyline.schema.json", skill / "references" / "storyline.schema.json")
    shutil.copy(ROOT / "templates/themes.json", skill / "references" / "themes.json")
    shutil.copy(ROOT / "docs/spec/examples/example-deck.json", skill / "examples" / "example-deck.json")
    for f in (ROOT / "renderer/examples").glob("*.json"):
        shutil.copy(f, skill / "examples" / f.name)
    shutil.copy(ROOT / "LICENSE", out / "LICENSE")
    (out / ".gitignore").write_text(".DS_Store\n")
    # The directory reads the README at the plugin root (plugin/), so write it there and at the repo root
    for readme in (out / "README.md", out / "plugin" / "README.md"):
        readme.write_text(PLUGIN_README)

    bad = []
    for f in out.rglob("*"):
        if not f.is_file() or ".git" in f.relative_to(out).parts[:1]:
            continue
        data = f.read_bytes()
        if (f.suffix.lower() not in ALLOWED and f.name not in ("LICENSE", ".gitignore")) or data.startswith(b"#!"):
            bad.append(str(f))
        elif f.suffix.lower() not in {".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico"}:
            try:
                data.decode("utf-8")
            except UnicodeDecodeError:
                bad.append(f"{f} (not UTF-8)")
            if b"\0" in data:
                bad.append(f"{f} (NUL byte)")
    if bad:
        sys.exit("not allowed in the directory:\n  " + "\n  ".join(bad))
    print(out)


if __name__ == "__main__":
    target = sys.argv[sys.argv.index("--directory") + 1] if "--directory" in sys.argv else None
    if not target:  # --directory alone leaves dist/pypi (and its built wheel) untouched
        build_package()
    build_directory(pathlib.Path(target).expanduser().resolve() if target else DIST / "directory")
