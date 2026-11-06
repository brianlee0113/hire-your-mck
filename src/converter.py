"""Convert long-form text to dot/dash structure or rich slide specs using Claude API."""
from dotenv import load_dotenv

from src.api_client import call_claude, parse_json_response
from src.config import DEFAULT_SOURCE

load_dotenv()

SYSTEM_PROMPT = """당신은 맥킨지 스타일의 Executive Summary를 작성하는 전문가입니다.
주어진 긴 텍스트를 분석하여 닷(•)/대시(-) 구조의 Executive Summary로 변환하세요.

## 규칙
1. 각 핵심 논점을 닷(•)으로 표시합니다 (3~7개 권장)
2. 각 닷 아래에 근거/데이터를 대시(-)로 표시합니다 (닷당 1~3개)
3. 닷은 결론 선행의 액션 지향적 문장으로 작성합니다
4. 전체 닷들이 논리적 스토리라인을 구성해야 합니다
5. **원문에 수치/데이터가 있으면 반드시 인라인 데이터 스펙으로 포함합니다**

## 인라인 데이터 스펙 규칙

### 차트 데이터
수치 비교/추이가 있으면 차트 스펙을 추가하세요:
```
[차트: 제목 | 유형: bar | 카테고리: A, B, C | 시리즈: 시리즈명1(값1, 값2, 값3), 시리즈명2(값1, 값2, 값3)]
```
- 유형: `bar` (막대), `stacked_bar` (누적막대), `line` (라인), `pie` (원형)
- 카테고리: 비교 축 항목들 (콤마 구분)
- 시리즈: 데이터 시리즈들, 각각 `이름(값, 값, ...)` 형식
- 값은 숫자만 (단위 제외). 예: 150억 → 150, 33% → 33

### 테이블 데이터
비교표/상세 항목이 있으면 테이블 스펙을 추가하세요:
```
[테이블: 제목 | 헤더: 열1, 열2, 열3 | 행: 항목1(값1, 값2), 항목2(값1, 값2)]
```
- 헤더: 열 이름들 (콤마 구분)
- 행: 각 행은 `행이름(값, 값, ...)` 형식. 값에 단위 포함 가능 (150억, +33%)

### 데이터가 없는 경우
정성적 내용이면 데이터 스펙 없이 텍스트만 작성합니다.

## 출력 형식 (이 형식만 출력하세요)
• [리드 메시지 1]
  - [근거 텍스트] [차트: 채널별 매출 | 유형: bar | 카테고리: 온라인, 오프라인 | 시리즈: 2024(150, 300), 2025(200, 280)]
  - [근거 텍스트] [테이블: KPI 현황 | 헤더: 지표, 목표, 실적 | 행: ROAS(5.0, 4.2), CPC(500, 480)]
  - [근거 텍스트] (데이터 없으면 스펙 없이)
• [리드 메시지 2]
  - [근거/서브불렛]
"""


def convert(text):
    """Convert long-form text to dot/dash structured text using Claude API."""
    return call_claude(
        SYSTEM_PROMPT,
        f"다음 텍스트를 닷/대시 구조로 변환해주세요:\n\n{text}",
    )


# ── Rich conversion (longform → JSON slide specs) ─────────────────

RICH_SYSTEM_PROMPT = """당신은 맥킨지 전략 컨설팅 장표를 설계하는 시니어 컨설턴트입니다.
주어진 리서치 텍스트를 분석하여 맥킨지 스타일의 슬라이드 구성을 JSON으로 출력합니다.

## 핵심 원칙
1. **정보 밀도 극대화**: 원문의 데이터, 수치, 비교, 시사점을 최대한 보존합니다
2. **결론 선행 (So What)**: 각 슬라이드 타이틀은 현상 기술이 아닌 시사점/결론을 먼저 제시
3. **근거 기반**: 모든 주장은 데이터(차트/테이블)로 뒷받침
4. **스토리라인**: 슬라이드 간 논리적 흐름 유지 (현황→분석→시사점→실행안)

## 슬라이드 타이틀 작성법
- 포맷: `섹션명 | 핵심 메시지 (결론 선행, 액션 지향)`
- Bad: "매출 현황" → Good: "온라인 채널 매출 YoY 35% 성장, 추가 확대 여지 충분"
- 한 문장으로 완결, 가능하면 핵심 수치 포함

## 콘텐츠 블록 구성 원칙
각 슬라이드에 2~4개의 content_blocks를 배치합니다:
- **수치 비교가 있으면** → chart (bar/stacked_bar/line/pie)
- **항목별 상세 비교가 있으면** → table
- **핵심 KPI/메트릭이 있으면** → callout (큰 수치 강조)
- **시사점/포인트가 있으면** → text (불렛 포인트)
- **핵심 인사이트/결론이 있으면** → insight_box (강조 박스)

## 레이아웃 조합 예시
- 차트(left) + 시사점 텍스트(right) : 가장 일반적
- 차트(left) + 차트(right) : Before/After 비교
- 콜아웃(left) + 테이블(right) : 핵심 수치 + 상세 데이터
- 차트(full) : Full-page 차트
- 테이블(left) + 시사점(right) : 데이터 매트릭스 + 분석

## 데이터 추출 규칙
- 원문에 수치가 있으면 반드시 차트 또는 테이블의 실제 데이터로 포함
- 차트 series values에는 숫자만 (단위 제거). 예: 150억 → 150, 33% → 33
- 카테고리명은 간결하게 (예: "2024년 1분기" → "24Q1")
- 테이블 rows 값에는 단위 포함 가능 (150억, +33%)

## 출력 형식
반드시 아래 JSON 배열만 출력하세요. 다른 텍스트 없이 순수 JSON만 출력합니다.

[
  {
    "title": "섹션 | 결론 선행 메시지",
    "subtitle": "분석 범위/기간 (없으면 null)",
    "source": "자료: 데이터출처, 팀 분석",
    "layout": "split",
    "content_blocks": [
      {
        "type": "chart",
        "title": "차트 제목",
        "chart_type": "bar",
        "categories": ["A", "B", "C"],
        "series": [{"name": "시리즈명", "values": [10, 20, 30]}],
        "position": "left"
      },
      {
        "type": "text",
        "title": "핵심 시사점",
        "bullets": ["포인트 1: 구체적 근거와 함께", "포인트 2: 데이터 언급 포함", "포인트 3: 실행 방안"],
        "position": "right"
      }
    ]
  }
]

content_block type 종류:
- "chart": chart_type(bar/stacked_bar/line/pie), categories, series 필수
- "table": headers, rows 필수 (rows는 2차원 배열: [["행1값1", "행1값2"], ...])
- "callout": value(큰 숫자), label(설명), description(부연, 선택) 필수
- "text": title, bullets(문자열 배열) 필수
- "insight_box": text 필수, style("subtle"/"accent") 선택

position 값: "left", "right", "full"
layout 값: "split"(좌우), "full"(전체), "3col"(3분할), "dashboard"(4분할), "auto"(자동)
"""


def convert_rich(text, use_agents=False):
    """Convert long-form text directly to rich slide specifications.

    Args:
        text: Long-form input text
        use_agents: If True, use multi-agent pipeline for higher quality

    Returns:
        list[dict]: List of rich slide specification dicts
    """
    if use_agents:
        from src.agents import run_pipeline
        return run_pipeline(text)
    response_text = call_claude(
        RICH_SYSTEM_PROMPT,
        f"다음 리서치 텍스트를 분석하여 맥킨지 스타일 슬라이드 JSON으로 변환해주세요:\n\n{text}",
        max_tokens=8192,
    )

    slides = parse_json_response(response_text)

    if not isinstance(slides, list):
        raise ValueError(f"Expected JSON array, got {type(slides).__name__}")

    # Normalize defaults
    for slide in slides:
        slide.setdefault("subtitle", None)
        slide.setdefault("source", DEFAULT_SOURCE)
        slide.setdefault("footnote", None)
        slide.setdefault("is_backup", False)
        slide.setdefault("layout", "auto")
        slide.setdefault("content_blocks", [])
        for block in slide["content_blocks"]:
            block.setdefault("position", "full")

    return slides
