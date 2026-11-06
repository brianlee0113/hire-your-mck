"""QA Critic Agent — validates slide specs against structural rules."""
import json
from .base import BaseAgent, MODEL_HAIKU

SYSTEM_PROMPT = """당신은 맥킨지 슬라이드 JSON 스펙의 품질을 검증하는 QA 전문가입니다.
주어진 슬라이드 JSON 배열을 검증하고 문제점을 지적합니다.

## 검증 규칙

### 1. 필수 필드 검증 (error)
- 각 슬라이드: title(string), layout(string), content_blocks(array) 필수
- chart 블록: type, chart_type, categories, series 필수
- table 블록: type, headers, rows 필수
- callout 블록: type, value, label 필수
- text 블록: type, bullets(array) 필수
- insight_box 블록: type, text 필수

### 2. 데이터 정합성 (error)
- 차트: 모든 series[].values 길이 == categories 길이
- 차트: series[].values는 모두 숫자 (문자열 숫자도 허용하지만 경고)
- 테이블: 모든 rows[] 길이 == headers 길이
- layout이 "split"이면 content_blocks에 "left"와 "right" position이 있어야 함

### 3. 콘텐츠 품질 (warning)
- 타이틀이 결론 선행 형태인지 (단순 명사형이면 warning)
- content_blocks가 0개인 슬라이드 (warning)
- 동일한 position에 2개 이상의 블록이 겹치면 (warning)

### 4. 유효값 검증 (error)
- layout: "split", "full", "3col", "dashboard", "auto" 중 하나
- position: "left", "right", "full" 중 하나
- chart_type: "bar", "stacked_bar", "line", "pie" 중 하나
- insight_box style: "subtle", "accent" 중 하나

## 출력 형식
반드시 아래 JSON만 출력하세요.

{
  "passed": true/false,
  "issues": [
    {
      "slide_index": 0,
      "block_index": null,
      "severity": "error",
      "rule": "data_consistency",
      "message": "구체적 문제 설명"
    }
  ],
  "feedback": "Slide Composer에게 전달할 수정 지시 (passed=true이면 빈 문자열)"
}

판정 기준:
- error가 1개라도 있으면 passed=false
- warning만 있으면 passed=true (경고는 참고용)"""


class QACriticAgent(BaseAgent):
    name = "qa_critic"
    model = MODEL_HAIKU
    system_prompt = SYSTEM_PROMPT
    max_tokens = 2048

    def run(self, slides):
        """Validate slide specs and return QA results.

        Args:
            slides: list of slide spec dicts to validate

        Returns:
            dict: {passed, issues[], feedback}
        """
        slides_json = json.dumps(slides, ensure_ascii=False, indent=2)
        user_message = (
            "다음 슬라이드 JSON 배열을 검증해주세요:\n\n"
            f"{slides_json}"
        )
        result = super().run(user_message)

        # Ensure proper structure
        if not isinstance(result, dict):
            return {"passed": False, "issues": [], "feedback": "QA 응답 파싱 실패"}
        result.setdefault("passed", False)
        result.setdefault("issues", [])
        result.setdefault("feedback", "")
        return result
