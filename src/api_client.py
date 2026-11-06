"""Shared Claude API client utilities.

Centralizes API key validation, client creation, and JSON response parsing
used by converter.py and learner.py.
"""
import os
import json
import re

MODEL = "claude-sonnet-4-20250514"
MODEL_OPUS = "claude-opus-4-0-20250514"
MODEL_HAIKU = "claude-haiku-4-5-20251001"


def call_claude(system_prompt, user_message, max_tokens=4096, model=None):
    """Call Claude API and return the response text.

    Args:
        system_prompt: System prompt string
        user_message: User message string
        max_tokens: Maximum output tokens (default 4096)
        model: Model ID to use (default: MODEL / sonnet)

    Returns:
        str: Claude's response text

    Raises:
        RuntimeError: If API key is missing or anthropic package not installed
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError(
            "ANTHROPIC_API_KEY 환경변수가 설정되지 않았습니다.\n"
            "설정 방법: export ANTHROPIC_API_KEY=your-key-here"
        )

    try:
        import anthropic
    except ImportError:
        raise RuntimeError(
            "anthropic 패키지가 설치되지 않았습니다.\n"
            "설치: pip install anthropic"
        )

    client = anthropic.Anthropic(api_key=api_key)
    message = client.messages.create(
        model=model or MODEL,
        max_tokens=max_tokens,
        system=system_prompt,
        messages=[{"role": "user", "content": user_message}],
    )
    return message.content[0].text


def parse_json_response(text):
    """Extract JSON from Claude API response with 3-level fallback.

    Tries: direct parse → markdown code block → bracket search.

    Args:
        text: Raw response text from Claude API

    Returns:
        dict or list: Parsed JSON object

    Raises:
        ValueError: If JSON cannot be extracted
    """
    # 1. Direct parse
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # 2. Markdown code block
    json_match = re.search(r'```(?:json)?\s*\n(.*?)\n```', text, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group(1))
        except json.JSONDecodeError:
            pass

    # 3. Find outermost brackets
    for open_br, close_br in [("{", "}"), ("[", "]")]:
        start = text.find(open_br)
        end = text.rfind(close_br) + 1
        if start >= 0 and end > start:
            try:
                return json.loads(text[start:end])
            except json.JSONDecodeError:
                continue

    raise ValueError(f"Claude API 응답에서 JSON을 추출할 수 없습니다:\n{text[:300]}")
