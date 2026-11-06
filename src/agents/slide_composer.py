"""Slide Composer Agent — assembles final JSON slide specs from strategy + data."""
import json
from .base import BaseAgent, MODEL

SYSTEM_PROMPT = """당신은 맥킨지 스타일 슬라이드를 조립하는 전문가입니다.
Strategist가 설계한 스토리라인/슬라이드 구성과 Data Analyst가 추출한 데이터 스펙을 받아
최종 JSON slide spec 배열을 생성합니다.

## 핵심 역할
1. **전략 프레임 실현**: Strategist의 타이틀/메시지를 그대로 사용
2. **데이터 매칭**: Data Analyst의 data_items를 적절한 슬라이드에 배치
3. **레이아웃 결정**: 콘텐츠 블록 수와 유형에 맞는 레이아웃 선택
4. **시사점 추가**: 데이터만으로 부족한 경우 텍스트 블록(불렛 포인트)으로 보완

## 레이아웃 조합 가이드
- 차트(left) + 시사점 텍스트(right): 가장 일반적
- 차트(left) + 차트(right): Before/After 비교
- 콜아웃(left) + 테이블(right): 핵심 수치 + 상세 데이터
- 차트(full): Full-page 차트
- 테이블(left) + 시사점(right): 데이터 매트릭스 + 분석

## content_block type별 필수 필드
- "chart": type, title, chart_type(bar/stacked_bar/line/pie), categories[], series[{name, values[]}], position
- "table": type, title, headers[], rows[[]], position
- "callout": type, value, label, description(선택), color(선택), position
- "text": type, title, bullets[], position
- "insight_box": type, text, style("subtle"/"accent"), position

## position 값: "left", "right", "full"
## layout 값: "split"(좌우 2분할), "full"(전체), "3col"(3분할), "dashboard"(4분할)

## 출력 형식
반드시 아래 JSON 배열만 출력하세요. 다른 텍스트 없이 순수 JSON만 출력합니다.

[
  {
    "title": "Strategist가 작성한 타이틀 그대로",
    "subtitle": "string 또는 null",
    "source": "자료: 출처, 팀 분석",
    "footnote": null,
    "is_backup": false,
    "layout": "split",
    "content_blocks": [
      {"type": "chart", "position": "left", "title": "...", "chart_type": "bar", "categories": [...], "series": [...]},
      {"type": "text", "position": "right", "title": "핵심 시사점", "bullets": ["...", "..."]}
    ]
  }
]"""


class SlideComposerAgent(BaseAgent):
    name = "slide_composer"
    model = MODEL
    system_prompt = SYSTEM_PROMPT
    max_tokens = 8192

    def run(self, composer_input):
        """Assemble final slide specs from strategy + data.

        Args:
            composer_input: JSON string with strategy_result, data_result, original_text

        Returns:
            list: Array of slide spec dicts
        """
        user_message = (
            "아래의 Strategist 분석 결과와 Data Analyst 추출 데이터를 조합하여 "
            "최종 슬라이드 JSON 배열을 생성해주세요.\n\n"
            f"{composer_input}"
        )
        result = super().run(user_message)
        # Ensure we return a list
        if isinstance(result, dict) and "slides" in result:
            return result["slides"]
        if isinstance(result, list):
            return result
        raise ValueError(f"Slide Composer returned unexpected type: {type(result).__name__}")

    def run_with_feedback(self, composer_input, feedback, previous_slides):
        """Re-run with QA feedback to fix issues.

        Args:
            composer_input: Original composer input
            feedback: QA Critic feedback text
            previous_slides: Previous slide specs that had issues

        Returns:
            list: Corrected slide spec dicts
        """
        user_message = (
            "이전에 생성한 슬라이드 JSON에 문제가 발견되었습니다. "
            "아래 피드백을 반영하여 수정된 JSON을 생성해주세요.\n\n"
            f"## 원본 입력\n{composer_input}\n\n"
            f"## 이전 생성 결과\n{json.dumps(previous_slides, ensure_ascii=False, indent=2)}\n\n"
            f"## QA 피드백\n{feedback}\n\n"
            "위 피드백을 반영하여 수정된 전체 슬라이드 JSON 배열을 출력하세요."
        )
        result = super().run(user_message)
        if isinstance(result, dict) and "slides" in result:
            return result["slides"]
        if isinstance(result, list):
            return result
        raise ValueError(f"Slide Composer returned unexpected type: {type(result).__name__}")
