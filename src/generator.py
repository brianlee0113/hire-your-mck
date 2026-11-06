"""Generate McKinsey-style PowerPoint from parsed slide data.

Starts from a blank 16:9 deck and places the title and unit line on our own
grid (src/config.py, templates/themes.json).
"""
from pptx import Presentation
from src.config import DEFAULT_SOURCE
from pptx.util import Inches, Pt, Emu
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.chart import XL_CHART_TYPE
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor


# ── Helpers ────────────────────────────────────────────────────────

def _delete_all_slides(prs):
    """Remove every existing slide from a presentation."""
    while len(prs.slides._sldIdLst) > 0:
        rId = prs.slides._sldIdLst[0].rId
        prs.part.drop_rel(rId)
        del prs.slides._sldIdLst[0]


def _set_run(run, text, font_name, font_size, bold=False, color=None):
    """Configure a single run's font properties."""
    run.text = text
    run.font.name = font_name
    run.font.size = font_size
    run.font.bold = bold
    if color:
        run.font.color.rgb = color


def _add_textbox(slide, left, top, width, height, text,
                 font_name, font_size, bold=False, color=None,
                 alignment=PP_ALIGN.LEFT, word_wrap=True):
    """Add a formatted text box to a slide."""
    txbox = slide.shapes.add_textbox(int(left), int(top), int(width), int(height))
    tf = txbox.text_frame
    tf.word_wrap = word_wrap
    tf.margin_left = 0
    tf.margin_right = 0
    tf.margin_top = 0
    tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.alignment = alignment
    run = p.add_run()
    _set_run(run, text, font_name, font_size, bold, color)
    return txbox


# ── Slide element builders ─────────────────────────────────────────

def _fill_title_placeholder(slide, text, cfg):
    """Fill the Title placeholder (PH[0]) with lead message text."""
    ph = slide.placeholders[0]
    ph.left, ph.top = cfg["title_left"], cfg["title_top"]
    ph.width, ph.height = cfg["title_width"], cfg["title_height"]
    ph.text = ""
    ph.text_frame.word_wrap = True
    p = ph.text_frame.paragraphs[0]
    p.alignment = 1  # left
    run = p.add_run()
    _set_run(run, text, cfg["font_title"], cfg["size_title"], bold=True, color=cfg["color_title"])


def _fill_subtitle_placeholder(slide, text, cfg):
    """Fill the Subtitle placeholder (PH[1]) if it exists."""
    if 1 in slide.placeholders:
        ph = slide.placeholders[1]
        ph.left, ph.top = cfg["title_left"], cfg["subtitle_top"]
        ph.width, ph.height = cfg["title_width"], cfg["subtitle_height"]
        ph.text = ""
        tf = ph.text_frame
    else:  # "Title Only" layout: unit line is a plain text box
        tf = slide.shapes.add_textbox(cfg["title_left"], cfg["subtitle_top"],
                                      cfg["title_width"], cfg["subtitle_height"]).text_frame
    p = tf.paragraphs[0]
    run = p.add_run()
    _set_run(run, text, cfg["font_body"], cfg["size_subtitle"], bold=False, color=cfg["color_text"])


def _add_source(slide, cfg, text=None):
    """Add source text at bottom of slide."""
    if text is None:
        text = DEFAULT_SOURCE
    _add_textbox(
        slide,
        left=cfg["margin_left"], top=cfg["source_top"],
        width=cfg["source_width"], height=cfg["source_height"],
        text=text,
        font_name=cfg["font_source"], font_size=cfg["size_source"],
        color=cfg["color_gray_dark"],
    )


def _add_section_header(slide, left, top, width, text, cfg):
    """Add a section header (18pt bold) in the content area."""
    return _add_textbox(
        slide, left, top, width, Inches(0.30),
        text=text,
        font_name=cfg["font_body"], font_size=cfg["size_section_header"],
        bold=True, color=cfg["color_text"],
    )



CHART_TYPE_MAP = {
    "bar": XL_CHART_TYPE.COLUMN_CLUSTERED,
    "stacked_bar": XL_CHART_TYPE.COLUMN_STACKED,
    "line": XL_CHART_TYPE.LINE,
    "pie": XL_CHART_TYPE.PIE,
}


def _add_chart(slide, left, top, width, height, cfg, data_spec=None):
    """Add a chart. Uses data_spec if provided, otherwise falls back to dummy data."""
    chart_data = CategoryChartData()

    if data_spec and "categories" in data_spec and "series" in data_spec:
        chart_data.categories = data_spec["categories"]
        for series in data_spec["series"]:
            chart_data.add_series(series["name"], tuple(series["values"]))
        chart_type = CHART_TYPE_MAP.get(data_spec.get("chart_type", "bar"), XL_CHART_TYPE.COLUMN_CLUSTERED)
    else:
        chart_data.categories = ["항목 A", "항목 B", "항목 C", "항목 D"]
        chart_data.add_series("시리즈 1", (45, 62, 38, 55))
        chart_data.add_series("시리즈 2", (25, 18, 32, 20))
        chart_type = XL_CHART_TYPE.COLUMN_STACKED

    chart_frame = slide.shapes.add_chart(
        chart_type,
        int(left), int(top), int(width), int(height),
        chart_data,
    )
    chart = chart_frame.chart
    chart.has_legend = True
    chart.legend.include_in_layout = False

    for i, series in enumerate(chart.series):
        fill = series.format.fill
        fill.solid()
        fill.fore_color.rgb = cfg["chart_colors"][i % len(cfg["chart_colors"])]

    return chart_frame


def _add_table(slide, left, top, width, height, cfg, data_spec=None):
    """Add a table. Uses data_spec if provided, otherwise falls back to dummy data."""
    if data_spec and "headers" in data_spec and "rows" in data_spec:
        headers = data_spec["headers"]
        data = data_spec["rows"]
    else:
        headers = ["구분", "항목 A", "항목 B"]
        data = [
            ["카테고리 1", "xx억", "+15%"],
            ["카테고리 2", "xx억", "+8%"],
            ["합계", "xx억", "+12%"],
        ]

    num_rows = len(data) + 1  # +1 for header
    num_cols = len(headers)
    table_shape = slide.shapes.add_table(
        num_rows, num_cols, int(left), int(top), int(width), int(height)
    )
    table = table_shape.table

    # Header
    for ci, h in enumerate(headers):
        cell = table.cell(0, ci)
        cell.text = ""
        p = cell.text_frame.paragraphs[0]
        run = p.add_run()
        _set_run(run, str(h), cfg["font_body"], cfg["size_label"], bold=True, color=cfg["color_white"])
        cell.fill.solid()
        cell.fill.fore_color.rgb = cfg["color_gray_dark"]

    # Data rows
    for ri, row_data in enumerate(data):
        for ci in range(num_cols):
            cell = table.cell(ri + 1, ci)
            cell.text = ""
            p = cell.text_frame.paragraphs[0]
            run = p.add_run()
            val = str(row_data[ci]) if ci < len(row_data) else ""
            _set_run(run, val, cfg["font_body"], cfg["size_body"], color=cfg["color_text"])

    return table_shape


def _add_callout_box(slide, left, top, width, height, text, cfg):
    """Add a text callout box with subtle background."""
    shape = slide.shapes.add_shape(
        1,  # MSO_SHAPE.RECTANGLE
        int(left), int(top), int(width), int(height),
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = cfg["color_bg_subtle"]
    shape.line.fill.background()

    tf = shape.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.15)
    tf.margin_top = Inches(0.1)
    p = tf.paragraphs[0]
    run = p.add_run()
    _set_run(run, text, cfg["font_body"], cfg["size_body"], color=cfg["color_text"])
    return shape


# ── Rich slide generation ─────────────────────────────────────────

def _add_callout_value(slide, left, top, width, height, block, cfg):
    """Add a large metric callout (24pt bold number + label + description)."""
    color_map = {
        "accent": cfg["color_accent"],
        "good": cfg["color_good"],
        "caution": cfg["color_caution"],
        "alert": cfg["color_alert"],
    }
    value_color = color_map.get(block.get("color"), cfg["color_accent"])

    # Value (large number)
    value_height = Inches(0.50)
    _add_textbox(
        slide, left, top, width, value_height,
        text=block.get("value", ""),
        font_name=cfg["font_body"], font_size=cfg["size_callout"],
        bold=True, color=value_color,
    )

    # Label
    label_top = int(top + value_height + Inches(0.05))
    label_height = Inches(0.30)
    _add_textbox(
        slide, left, label_top, width, label_height,
        text=block.get("label", ""),
        font_name=cfg["font_body"], font_size=cfg["size_label"],
        bold=True, color=cfg["color_text"],
    )

    # Description (optional)
    if block.get("description"):
        desc_top = int(label_top + label_height + Inches(0.05))
        desc_height = int(height - value_height - label_height - Inches(0.15))
        if desc_height > Inches(0.2):
            _add_textbox(
                slide, left, desc_top, width, desc_height,
                text=block["description"],
                font_name=cfg["font_body"], font_size=cfg["size_body"],
                color=cfg["color_gray_dark"],
            )


def _add_text_bullets(slide, left, top, width, height, block, cfg):
    """Add a section header + multiple bullet points."""
    header_height = Inches(0.30)
    title = block.get("title", "")
    if title:
        _add_section_header(slide, left, top, width, title, cfg)

    body_top = int(top + header_height + Inches(0.05)) if title else int(top)
    body_height = int(height - header_height - Inches(0.05)) if title else int(height)

    txbox = slide.shapes.add_textbox(int(left), body_top, int(width), max(body_height, int(Inches(0.5))))
    tf = txbox.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.1)
    tf.margin_top = 0
    tf.margin_bottom = 0
    tf.margin_right = 0

    bullets = block.get("bullets", [])
    for i, bullet_text in enumerate(bullets):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.space_after = Pt(4)
        run = p.add_run()
        _set_run(run, f"• {bullet_text}", cfg["font_body"], cfg["size_body"],
                 color=cfg["color_text"])
    return txbox


def _add_insight_box(slide, left, top, width, height, block, cfg):
    """Add a highlighted insight/conclusion box."""
    shape = slide.shapes.add_shape(
        1,  # MSO_SHAPE.RECTANGLE
        int(left), int(top), int(width), int(height),
    )

    style = block.get("style", "subtle")
    if style == "accent":
        shape.fill.solid()
        shape.fill.fore_color.rgb = cfg["color_accent"]
        text_color = cfg["color_white"]
    else:
        shape.fill.solid()
        shape.fill.fore_color.rgb = cfg["color_bg_subtle"]
        text_color = cfg["color_text"]
    shape.line.fill.background()

    tf = shape.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.15)
    tf.margin_top = Inches(0.1)
    tf.margin_right = Inches(0.15)
    p = tf.paragraphs[0]
    run = p.add_run()
    _set_run(run, block.get("text", ""), cfg["font_body"], cfg["size_body"],
             bold=True, color=text_color)
    return shape


def _infer_layout(blocks):
    """Infer layout from content block count and position hints."""
    if not blocks:
        return "full"
    positions = [b.get("position", "full") for b in blocks]
    if len(blocks) == 1:
        return "full"
    if any(p in ("left", "right") for p in positions):
        return "split"
    if len(blocks) == 3:
        return "3col"
    if len(blocks) >= 4:
        return "dashboard"
    return "split"


def _compute_block_positions(blocks, layout, cfg):
    """Compute (left, top, width, height) for each content block."""
    content_left = cfg["margin_left"]
    content_top = cfg["content_top"]
    content_width = cfg["title_width"]
    content_height = int(cfg["content_bottom"] - cfg["content_top"])
    gap = cfg["content_gap"]

    half_w = int((content_width - gap) / 2)
    third_w = int((content_width - gap * 2) / 3)
    half_h = int((content_height - gap) / 2)

    right_left = int(content_left + half_w + gap)
    bottom_top = int(content_top + half_h + gap)

    POS = {
        "full":         (content_left, content_top, content_width, content_height),
        "left":         (content_left, content_top, half_w, content_height),
        "right":        (right_left, content_top, half_w, content_height),
        "top-left":     (content_left, content_top, half_w, half_h),
        "top-right":    (right_left, content_top, half_w, half_h),
        "bottom-left":  (content_left, bottom_top, half_w, half_h),
        "bottom-right": (right_left, bottom_top, half_w, half_h),
        "bottom":       (content_left, bottom_top, content_width, half_h),
    }

    if layout == "auto" or layout is None:
        layout = _infer_layout(blocks)

    positions = []

    if layout == "full":
        n = len(blocks)
        if n == 1:
            positions.append(POS["full"])
        else:
            block_h = int((content_height - gap * (n - 1)) / n)
            for i in range(n):
                y = int(content_top + i * (block_h + gap))
                positions.append((content_left, y, content_width, block_h))

    elif layout == "split":
        for block in blocks:
            pos = block.get("position", "left")
            if pos in POS:
                positions.append(POS[pos])
            else:
                positions.append(POS["left"])

    elif layout == "3col":
        for i, block in enumerate(blocks):
            col_left = int(content_left + i * (third_w + gap))
            positions.append((col_left, content_top, third_w, content_height))

    elif layout == "dashboard":
        quad = ["top-left", "top-right", "bottom-left", "bottom-right"]
        for i, block in enumerate(blocks):
            key = quad[i] if i < 4 else "top-left"
            positions.append(POS[key])

    else:
        for block in blocks:
            pos = block.get("position", "full")
            positions.append(POS.get(pos, POS["full"]))

    return positions


def _add_rich_content_block(slide, block, left, top, width, height, cfg):
    """Add one rich content block to a slide based on its type."""
    block_type = block.get("type", "text")
    header_h = Inches(0.30)
    gap_h = Inches(0.10)

    if block_type == "chart":
        title = block.get("title", "")
        if title:
            _add_section_header(slide, left, top, width, title, cfg)
        chart_top = int(top + header_h + gap_h) if title else int(top)
        chart_height = int(height - header_h - gap_h) if title else int(height)
        categories = block.get("categories", [])
        series = block.get("series", [])
        data_spec = {
            "chart_type": block.get("chart_type", "bar"),
            "categories": categories,
            "series": series,
        } if categories and series else None
        _add_chart(slide, int(left), chart_top, int(width), max(chart_height, int(Inches(1.0))), cfg, data_spec)

    elif block_type == "table":
        title = block.get("title", "")
        if title:
            _add_section_header(slide, left, top, width, title, cfg)
        table_top = int(top + header_h + gap_h) if title else int(top)
        table_height = int(height - header_h - gap_h) if title else int(height)
        headers = block.get("headers", [])
        rows = block.get("rows", [])
        data_spec = {"headers": headers, "rows": rows} if headers else None
        _add_table(slide, int(left), table_top, int(width), max(table_height, int(Inches(0.5))), cfg, data_spec)

    elif block_type == "callout":
        _add_callout_value(slide, left, top, width, height, block, cfg)

    elif block_type == "text":
        _add_text_bullets(slide, left, top, width, height, block, cfg)

    elif block_type == "insight_box":
        _add_insight_box(slide, left, top, width, height, block, cfg)

    else:
        fallback_text = str(block.get("text", block.get("title", "")))
        _add_callout_box(slide, int(left), int(top), int(width), int(height), fallback_text, cfg)


def _generate_rich_slide(prs, slide_spec, cfg):
    """Generate a single slide from a rich slide specification dict."""
    layout_idx = cfg["layout_default"]
    layout = prs.slide_layouts[layout_idx]
    slide = prs.slides.add_slide(layout)

    # Title
    title_text = slide_spec.get("title", "")
    if slide_spec.get("is_backup"):
        title_text = f"[참고] {title_text}"
    _fill_title_placeholder(slide, title_text, cfg)

    # Subtitle
    if slide_spec.get("subtitle"):
        _fill_subtitle_placeholder(slide, slide_spec["subtitle"], cfg)

    # Source
    source_text = slide_spec.get("source") or DEFAULT_SOURCE
    _add_source(slide, cfg, text=source_text)

    # Footnote
    if slide_spec.get("footnote"):
        _add_textbox(
            slide,
            left=cfg["margin_left"], top=cfg["footnote_top"],
            width=cfg["footnote_width"], height=cfg["footnote_height"],
            text=slide_spec["footnote"],
            font_name=cfg["font_source"], font_size=cfg["size_source"],
            color=cfg["color_gray_dark"],
        )

    # Content blocks
    blocks = slide_spec.get("content_blocks", [])
    if not blocks:
        return slide

    slide_layout = slide_spec.get("layout", "auto")
    positions = _compute_block_positions(blocks, slide_layout, cfg)

    for block, (bleft, btop, bwidth, bheight) in zip(blocks, positions):
        _add_rich_content_block(slide, block, bleft, btop, bwidth, bheight, cfg)

    return slide


def generate_rich(slides_specs, cfg, output_path):
    """Generate a PowerPoint from rich slide specification dicts.

    Args:
        slides_specs: list of rich slide spec dicts
        cfg: design config from config.load()
        output_path: path to write .pptx file

    Returns:
        str: output_path
    """
    template_path = cfg.get("template_path")
    if template_path:
        prs = Presentation(template_path)
        _delete_all_slides(prs)
    else:
        prs = Presentation()
        prs.slide_width = cfg["slide_width"]
        prs.slide_height = cfg["slide_height"]

    for slide_spec in slides_specs:
        _generate_rich_slide(prs, slide_spec, cfg)

    prs.save(output_path)
    return output_path


# ── Public API (backward-compatible) ──────────────────────────────

def generate(slides_data, cfg, output_path):
    """Generate a PowerPoint from parsed dot/dash slide data.

    Converts to rich format internally, then delegates to generate_rich().
    Maintains backward compatibility with parser.parse() output.
    """
    from src.parser import to_rich_format
    rich_specs = to_rich_format(slides_data)
    return generate_rich(rich_specs, cfg, output_path)
