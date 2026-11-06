"""Detect input type: structured (dot/dash) vs long-form text."""
import re


def detect(text):
    """Detect if text is structured (type 1) or long-form (type 2).

    Returns:
        "structured" if dot/dash format, "longform" otherwise.
    """
    lines = text.strip().split("\n")
    dot_count = 0
    dash_count = 0

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("•") or stripped.startswith("●"):
            dot_count += 1
        elif re.match(r'^\s*[-–—]\s', line):
            dash_count += 1

    # If we have at least 2 dots, it's structured
    if dot_count >= 2:
        return "structured"

    # If we have dots and dashes, structured
    if dot_count >= 1 and dash_count >= 1:
        return "structured"

    return "longform"
