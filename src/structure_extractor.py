"""Extract structural information from reference PPTX files.

Reads sample PPTX files in samples/structure/ where:
- Slide 1: dot/dash Exec Sum text (input)
- Slides 2+: example slides (expected output)
"""
import os
import re
from pptx import Presentation
from pptx.util import Emu


def _emu_to_inches(emu):
    """Convert EMU to inches."""
    if emu is None:
        return None
    return round(emu / 914400, 2)


def _safe_color_rgb(color_obj):
    """Safely extract RGB hex string from a color object."""
    try:
        if color_obj and color_obj.type is not None and color_obj.rgb:
            return str(color_obj.rgb)
    except (AttributeError, TypeError):
        pass
    return None


def _safe_fill_color(fill_obj):
    """Safely extract fill color."""
    try:
        if fill_obj and fill_obj.type is not None:
            return _safe_color_rgb(fill_obj.fore_color)
    except (AttributeError, TypeError):
        pass
    return None


def _extract_run_info(run):
    """Extract font info from a text run."""
    info = {}
    try:
        if run.font.name:
            info["font_name"] = run.font.name
    except Exception:
        pass
    try:
        if run.font.size:
            info["font_size_pt"] = run.font.size.pt
    except Exception:
        pass
    try:
        if run.font.bold is not None:
            info["bold"] = run.font.bold
    except Exception:
        pass
    try:
        rgb = _safe_color_rgb(run.font.color)
        if rgb:
            info["color"] = rgb
    except Exception:
        pass
    return info


def _get_slide_text(slide):
    """Extract all text from a slide, preserving paragraph breaks."""
    texts = []
    for shape in slide.shapes:
        if shape.has_text_frame:
            for para in shape.text_frame.paragraphs:
                line = para.text.strip()
                if line:
                    texts.append(line)
    return "\n".join(texts)


def _classify_shape(shape):
    """Classify a shape into content type."""
    try:
        _ = shape.chart
        return "chart"
    except (ValueError, AttributeError):
        pass

    if shape.has_table:
        return "table"

    if shape.has_text_frame:
        text = shape.text_frame.text.strip()
        if not text:
            return "empty_shape"
        return "textbox"

    # Check if it's an image/picture
    try:
        if hasattr(shape, "image"):
            return "image"
    except Exception:
        pass

    return "shape"


def _extract_chart_info(shape):
    """Extract chart structure details."""
    try:
        chart = shape.chart
        info = {
            "chart_type": str(chart.chart_type),
        }
        # Count series and categories
        try:
            plot = chart.plots[0]
            info["num_series"] = len(plot.series)
            info["num_categories"] = len(plot.categories)
            info["categories"] = [str(c) for c in plot.categories][:10]
        except Exception:
            pass
        return info
    except Exception:
        return {}


def _extract_table_info(shape):
    """Extract table structure details."""
    if not shape.has_table:
        return {}
    table = shape.table
    info = {
        "rows": len(table.rows),
        "cols": len(table.columns),
        "headers": [],
        "sample_data": [],
    }
    # Extract header row
    if len(table.rows) > 0:
        for col_idx in range(len(table.columns)):
            cell = table.cell(0, col_idx)
            info["headers"].append(cell.text.strip()[:50])

    # Extract first data row as sample
    if len(table.rows) > 1:
        for col_idx in range(len(table.columns)):
            cell = table.cell(1, col_idx)
            info["sample_data"].append(cell.text.strip()[:50])

    return info


def _extract_textbox_info(shape):
    """Extract text box content and formatting."""
    if not shape.has_text_frame:
        return {}
    info = {
        "text": shape.text_frame.text.strip()[:200],
        "paragraphs": [],
    }
    for para in shape.text_frame.paragraphs:
        p_info = {"text": para.text.strip()[:100]}
        if para.alignment:
            p_info["alignment"] = str(para.alignment)
        for run in para.runs:
            r_info = _extract_run_info(run)
            if r_info:
                p_info["formatting"] = r_info
                break
        if p_info["text"]:
            info["paragraphs"].append(p_info)
    return info


def extract_dotdash_from_slide(pptx_path):
    """Extract dot/dash Exec Sum text from the first slide of a PPTX.

    Args:
        pptx_path: Path to the sample PPTX file

    Returns:
        str: The dot/dash structured text from slide 1
    """
    prs = Presentation(pptx_path)
    if len(prs.slides) == 0:
        return ""

    slide = prs.slides[0]
    return _get_slide_text(slide)


def extract_slide_structure(pptx_path, skip_first=True):
    """Extract structural information from slides in a PPTX.

    Args:
        pptx_path: Path to the PPTX file
        skip_first: If True, skip slide 1 (assumes it's the dot/dash input)

    Returns:
        list of dicts, each representing a slide's structure:
        {
            "slide_num": int,
            "title": str or None,
            "subtitle": str or None,
            "content_blocks": [
                {
                    "type": "chart"|"table"|"textbox"|"shape"|"image",
                    "position": {"left": float, "top": float, "width": float, "height": float},
                    "details": dict (chart_info, table_info, or textbox_info),
                }
            ],
            "has_source": bool,
            "source_text": str or None,
            "layout_pattern": "full"|"split"|"3col"|"custom",
            "num_content_blocks": int,
        }
    """
    prs = Presentation(pptx_path)
    slides_structure = []

    start_idx = 1 if skip_first else 0

    for slide_idx in range(start_idx, len(prs.slides)):
        slide = prs.slides[slide_idx]
        slide_info = {
            "slide_num": slide_idx + 1,
            "title": None,
            "subtitle": None,
            "content_blocks": [],
            "has_source": False,
            "source_text": None,
            "layout_pattern": "custom",
            "num_content_blocks": 0,
        }

        # Extract title and subtitle from placeholders
        for ph in slide.placeholders:
            if ph.placeholder_format.idx == 0:  # Title
                slide_info["title"] = ph.text.strip() if ph.text else None
            elif ph.placeholder_format.idx == 1:  # Subtitle
                slide_info["subtitle"] = ph.text.strip() if ph.text else None

        # Analyze all shapes for content blocks
        content_shapes = []
        for shape in slide.shapes:
            # Skip placeholders (title, subtitle) - already handled
            if shape.is_placeholder:
                ph_idx = shape.placeholder_format.idx
                if ph_idx in (0, 1, 10):  # title, subtitle, tracker
                    continue

            pos = {
                "left": _emu_to_inches(shape.left),
                "top": _emu_to_inches(shape.top),
                "width": _emu_to_inches(shape.width),
                "height": _emu_to_inches(shape.height),
            }

            content_type = _classify_shape(shape)

            # Check if this is a source line (small text at bottom)
            if content_type == "textbox" and pos["top"] and pos["top"] > 6.5:
                text = shape.text_frame.text.strip()
                if text and (text.startswith("자료") or text.startswith("Source")
                             or text.startswith("출처") or len(text) < 100):
                    slide_info["has_source"] = True
                    slide_info["source_text"] = text[:100]
                    continue

            if content_type == "empty_shape":
                continue

            # Build content block info
            block = {
                "type": content_type,
                "position": pos,
                "name": shape.name,
            }

            if content_type == "chart":
                block["details"] = _extract_chart_info(shape)
            elif content_type == "table":
                block["details"] = _extract_table_info(shape)
            elif content_type == "textbox":
                block["details"] = _extract_textbox_info(shape)
            else:
                block["details"] = {}

            # Add fill color if present
            fill_color = _safe_fill_color(getattr(shape, "fill", None))
            if fill_color:
                block["fill_color"] = fill_color

            content_shapes.append(block)

        slide_info["content_blocks"] = content_shapes
        slide_info["num_content_blocks"] = len(content_shapes)

        # Determine layout pattern from content block positions
        slide_info["layout_pattern"] = _detect_layout_pattern(content_shapes)

        slides_structure.append(slide_info)

    return slides_structure


def _detect_layout_pattern(content_blocks):
    """Detect layout pattern from content block positions.

    Returns: "full", "split", "3col", or "custom"
    """
    if not content_blocks:
        return "empty"

    # Filter to significant content blocks (charts, tables, large textboxes)
    significant = [
        b for b in content_blocks
        if b["type"] in ("chart", "table")
        or (b["type"] == "textbox" and b["position"].get("width", 0)
            and b["position"]["width"] > 3)
    ]

    if len(significant) <= 1:
        return "full"

    if len(significant) == 2:
        # Check if they're side by side
        lefts = sorted([b["position"]["left"] for b in significant if b["position"]["left"] is not None])
        if len(lefts) == 2 and abs(lefts[1] - lefts[0]) > 3:
            return "split"

    if len(significant) == 3:
        lefts = sorted([b["position"]["left"] for b in significant if b["position"]["left"] is not None])
        if len(lefts) == 3 and (lefts[2] - lefts[0]) > 6:
            return "3col"

    return "custom"


def structure_to_text(slides_structure):
    """Convert extracted slide structure to a summarized text.

    Filters out small decorative shapes and data labels to focus on
    meaningful content blocks for Claude API comparison.
    """
    lines = []
    for slide in slides_structure:
        lines.append(f"=== 슬라이드 {slide['slide_num']} ===")
        lines.append(f"  타이틀: {slide['title'] or '(없음)'}")
        if slide["subtitle"]:
            lines.append(f"  서브타이틀: {slide['subtitle']}")

        # Categorize blocks
        charts = [b for b in slide["content_blocks"] if b["type"] == "chart"]
        tables = [b for b in slide["content_blocks"] if b["type"] == "table"]
        images = [b for b in slide["content_blocks"] if b["type"] == "image"]
        textboxes = [
            b for b in slide["content_blocks"]
            if b["type"] == "textbox"
            and b["position"].get("width", 0) and b["position"]["width"] > 1.5
        ]
        section_headers = [
            b for b in textboxes
            if b["position"].get("top", 0) and 1.5 < b["position"]["top"] < 2.5
            and b["position"].get("width", 0) > 3
        ]
        shapes = [b for b in slide["content_blocks"] if b["type"] == "shape"]

        type_counts = []
        if charts:
            type_counts.append(f"차트 {len(charts)}개")
        if tables:
            type_counts.append(f"테이블 {len(tables)}개")
        if images:
            type_counts.append(f"이미지 {len(images)}개")
        if textboxes:
            type_counts.append(f"텍스트박스 {len(textboxes)}개")
        if shapes:
            type_counts.append(f"도형 {len(shapes)}개")

        lines.append(f"  레이아웃: {slide['layout_pattern']}")
        lines.append(f"  구성: {', '.join(type_counts) if type_counts else '(비어있음)'}")

        for b in section_headers:
            text = b.get("details", {}).get("text", "")[:80]
            if text:
                pos = b["position"]
                side = "좌측" if pos["left"] < 5 else "우측"
                lines.append(f"  섹션헤더 ({side}): \"{text}\"")

        for i, b in enumerate(charts):
            pos = b["position"]
            side = "좌측" if pos["left"] < 5 else ("우측" if pos["left"] > 6 else "중앙")
            details = b.get("details", {})
            lines.append(f"  차트{i+1} ({side}): {details.get('chart_type', '?')} "
                         f"- {details.get('num_series', '?')}시리즈, "
                         f"{details.get('num_categories', '?')}카테고리")

        for i, b in enumerate(tables):
            details = b.get("details", {})
            lines.append(f"  테이블{i+1}: {details.get('rows', '?')}행 x {details.get('cols', '?')}열")
            if details.get("headers"):
                lines.append(f"    헤더: {', '.join(details['headers'][:5])}")

        content_texts = [
            b for b in textboxes
            if b not in section_headers
            and b["position"].get("width", 0) > 2
        ]
        for b in content_texts[:5]:
            text = b.get("details", {}).get("text", "")[:60]
            if text and len(text) > 5:
                pos = b["position"]
                side = "좌측" if pos["left"] < 5 else ("우측" if pos["left"] > 6 else "중앙")
                lines.append(f"  텍스트 ({side}, {pos['width']}x{pos['height']}in): \"{text}\"")

        for i, b in enumerate(images):
            pos = b["position"]
            lines.append(f"  이미지{i+1}: {pos['width']}x{pos['height']}in")

        if slide["has_source"]:
            lines.append(f"  Source: {slide['source_text']}")
        lines.append("")

    return "\n".join(lines)
