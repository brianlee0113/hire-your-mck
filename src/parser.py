"""Parse dot/dash structured text into slide data."""
import re

from src.config import DEFAULT_SOURCE


def _parse_chart_spec(spec_str):
    """Parse chart data spec from inline format.

    Input: '제목 | 유형: bar | 카테고리: A, B, C | 시리즈: 매출(45, 62, 38), 성장률(12, 18, 9)'
    Returns: (title, data_spec_dict or None)
    """
    parts = [p.strip() for p in spec_str.split("|")]
    title = parts[0].strip()
    if len(parts) < 2:
        return title, None

    spec = {}
    for part in parts[1:]:
        if part.startswith("유형:"):
            spec["chart_type"] = part[3:].strip()
        elif part.startswith("카테고리:"):
            spec["categories"] = [c.strip() for c in part[5:].split(",")]
        elif part.startswith("시리즈:"):
            series_text = part[4:].strip()
            spec["series"] = _parse_series(series_text)

    if "categories" in spec and "series" in spec:
        return title, spec
    return title, None


def _parse_series(text):
    """Parse series from format: '매출(45, 62, 38), 성장률(12, 18, 9)'"""
    series_list = []
    # Match: name(val, val, ...)
    for m in re.finditer(r'([^,(]+?)\(([^)]+)\)', text):
        name = m.group(1).strip()
        vals_str = m.group(2).strip()
        values = []
        for v in vals_str.split(","):
            v = v.strip()
            try:
                values.append(float(v))
            except ValueError:
                values.append(0)
        series_list.append({"name": name, "values": values})
    return series_list


def _parse_table_spec(spec_str):
    """Parse table data spec from inline format.

    Input: '제목 | 헤더: 구분, 2024, 2025 | 행: 온라인(150억, 200억), 오프라인(300억, 280억)'
    Returns: (title, data_spec_dict or None)
    """
    parts = [p.strip() for p in spec_str.split("|")]
    title = parts[0].strip()
    if len(parts) < 2:
        return title, None

    spec = {}
    for part in parts[1:]:
        if part.startswith("헤더:"):
            spec["headers"] = [h.strip() for h in part[3:].split(",")]
        elif part.startswith("행:"):
            rows_text = part[2:].strip()
            spec["rows"] = _parse_table_rows(rows_text)

    if "headers" in spec and "rows" in spec:
        return title, spec
    return title, None


def _parse_table_rows(text):
    """Parse table rows from format: '온라인(150억, 200억), 오프라인(300억, 280억)'"""
    rows = []
    for m in re.finditer(r'([^,(]+?)\(([^)]+)\)', text):
        row_name = m.group(1).strip()
        vals = [v.strip() for v in m.group(2).split(",")]
        rows.append([row_name] + vals)
    return rows


def _extract_data_hint(text):
    """Extract [차트: ...] or [테이블: ...] hints from text.

    Supports both simple format [차트: 제목] and enriched format
    [차트: 제목 | 유형: bar | 카테고리: ... | 시리즈: ...].
    """
    chart_match = re.search(r'\[차트:\s*(.+?)\]', text)
    if chart_match:
        clean_text = text[:chart_match.start()].strip()
        spec_str = chart_match.group(1).strip()
        title, data_spec = _parse_chart_spec(spec_str)
        return clean_text, "chart", title, data_spec

    table_match = re.search(r'\[테이블:\s*(.+?)\]', text)
    if table_match:
        clean_text = text[:table_match.start()].strip()
        spec_str = table_match.group(1).strip()
        title, data_spec = _parse_table_spec(spec_str)
        return clean_text, "table", title, data_spec

    return text.strip(), None, None, None


def _extract_position(text):
    """Extract [좌]/[우] position hints from text."""
    position = None
    clean = text.strip()

    if clean.startswith("[좌]"):
        position = "left"
        clean = clean[3:].strip()
    elif clean.startswith("[우]"):
        position = "right"
        clean = clean[3:].strip()

    return clean, position


def _is_dot_line(line):
    """Check if line is a dot (•) / lead message line."""
    stripped = line.strip()
    return stripped.startswith("•") or stripped.startswith("● ")


def _is_dash_line(line):
    """Check if line is a dash (-) / sub-bullet line."""
    stripped = line.lstrip()
    return stripped.startswith("- ") or stripped.startswith("– ") or stripped.startswith("— ")


def _clean_dot(line):
    """Remove dot marker and clean up."""
    stripped = line.strip()
    for prefix in ["• ", "● ", "•", "●"]:
        if stripped.startswith(prefix):
            return stripped[len(prefix):].strip()
    return stripped


def _clean_dash(line):
    """Remove dash marker and clean up."""
    stripped = line.lstrip()
    for prefix in ["- ", "– ", "— "]:
        if stripped.startswith(prefix):
            return stripped[len(prefix):].strip()
    return stripped


def parse(text):
    """Parse dot/dash structured text into slide data list.

    Returns:
        list of dicts, each with:
            - title (str): lead message
            - is_backup (bool): whether this is a backup/reference slide
            - sub_bullets (list of dicts):
                - text (str): bullet text
                - position (str|None): "left"/"right" or None
                - data_type (str|None): "chart"/"table" or None
                - data_title (str|None): title for chart/table
                - data_spec (dict|None): chart/table data specification
    """
    lines = text.strip().split("\n")
    slides = []
    current_slide = None

    for line in lines:
        if not line.strip():
            continue

        if _is_dot_line(line):
            # Start new slide
            title = _clean_dot(line)

            # Check for [백업] or [참고] tag
            is_backup = False
            for tag in ["[백업]", "[참고]"]:
                if title.startswith(tag):
                    is_backup = True
                    title = title[len(tag):].strip()
                    break

            current_slide = {
                "title": title,
                "is_backup": is_backup,
                "sub_bullets": [],
            }
            slides.append(current_slide)

        elif _is_dash_line(line) and current_slide is not None:
            dash_text = _clean_dash(line)
            dash_text, position = _extract_position(dash_text)
            dash_text, data_type, data_title, data_spec = _extract_data_hint(dash_text)

            current_slide["sub_bullets"].append({
                "text": dash_text,
                "position": position,
                "data_type": data_type,
                "data_title": data_title,
                "data_spec": data_spec,
            })

        elif current_slide is not None:
            # Indented line without dash — treat as continuation or sub-item
            stripped = line.strip()
            if stripped and current_slide["sub_bullets"]:
                # Append to last sub-bullet's text
                last = current_slide["sub_bullets"][-1]
                last["text"] += " " + stripped

    return slides


def to_rich_format(slides_data):
    """Convert parsed dot/dash slide data to rich slide spec format.

    Bridges old parser output to the new rich format so that structured
    input can also flow through generator.generate_rich().

    Args:
        slides_data: list of dicts from parse()

    Returns:
        list[dict]: list of rich slide spec dicts
    """
    rich_slides = []

    for slide in slides_data:
        content_blocks = []

        for bullet in slide["sub_bullets"]:
            pos = bullet.get("position") or "full"

            if bullet["data_type"] == "chart":
                block = {
                    "type": "chart",
                    "title": bullet.get("data_title", ""),
                    "chart_type": "bar",
                    "categories": [],
                    "series": [],
                    "position": pos,
                }
                if bullet.get("data_spec"):
                    block["chart_type"] = bullet["data_spec"].get("chart_type", "bar")
                    block["categories"] = bullet["data_spec"].get("categories", [])
                    block["series"] = bullet["data_spec"].get("series", [])
                content_blocks.append(block)

            elif bullet["data_type"] == "table":
                block = {
                    "type": "table",
                    "title": bullet.get("data_title", ""),
                    "headers": [],
                    "rows": [],
                    "position": pos,
                }
                if bullet.get("data_spec"):
                    block["headers"] = bullet["data_spec"].get("headers", [])
                    block["rows"] = bullet["data_spec"].get("rows", [])
                content_blocks.append(block)

            else:
                content_blocks.append({
                    "type": "text",
                    "title": "",
                    "bullets": [bullet["text"]],
                    "position": pos,
                })

        # Infer layout
        n = len(content_blocks)
        if n <= 1:
            layout = "full"
        elif n == 2:
            layout = "split"
            if not any(b.get("position") in ("left", "right") for b in content_blocks):
                content_blocks[0]["position"] = "left"
                content_blocks[1]["position"] = "right"
        else:
            layout = "3col"

        rich_slides.append({
            "title": slide["title"],
            "subtitle": None,
            "source": DEFAULT_SOURCE,
            "footnote": None,
            "is_backup": slide.get("is_backup", False),
            "layout": layout,
            "content_blocks": content_blocks[:4],
        })

    return rich_slides
