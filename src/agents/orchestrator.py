"""Orchestrator — coordinates the multi-agent pipeline."""
import json
from concurrent.futures import ThreadPoolExecutor

from src.config import DEFAULT_SOURCE
from .strategist import StrategistAgent
from .data_analyst import DataAnalystAgent
from .slide_composer import SlideComposerAgent
from .qa_critic import QACriticAgent

MAX_QA_RETRIES = 2


def _merge_inputs(strategy_result, data_result, original_text):
    """Merge Strategist + Data Analyst outputs into Composer input string."""
    merged = {
        "strategy": strategy_result,
        "data": data_result,
        "original_text_excerpt": original_text[:3000],
    }
    return json.dumps(merged, ensure_ascii=False, indent=2)


def _normalize_slides(slides):
    """Apply default values to slide specs (same as converter.convert_rich)."""
    for slide in slides:
        slide.setdefault("subtitle", None)
        slide.setdefault("source", DEFAULT_SOURCE)
        slide.setdefault("footnote", None)
        slide.setdefault("is_backup", False)
        slide.setdefault("layout", "auto")
        slide.setdefault("content_blocks", [])
        for block in slide["content_blocks"]:
            block.setdefault("position", "full")


def run_pipeline(text):
    """Run the full multi-agent pipeline.

    Pipeline:
        1. Strategist + Data Analyst (parallel)
        2. Slide Composer (merges strategy + data)
        3. QA Critic (validates, retries up to MAX_QA_RETRIES times)

    Args:
        text: Raw input text

    Returns:
        list[dict]: Slide spec dicts ready for generate_rich()

    Raises:
        Falls back to converter.convert_rich() on agent failure.
    """
    strategist = StrategistAgent()
    data_analyst = DataAnalystAgent()
    composer = SlideComposerAgent()
    critic = QACriticAgent()

    try:
        # Phase 1: Strategist + Data Analyst in parallel
        print("  [Agent] Phase 1: Strategist + Data Analyst (병렬 실행)...")
        with ThreadPoolExecutor(max_workers=2) as pool:
            strategy_future = pool.submit(strategist.run, text)
            data_future = pool.submit(data_analyst.run, text)
            strategy_result = strategy_future.result()
            data_result = data_future.result()

        slide_count = len(strategy_result.get("slides", []))
        data_count = len(data_result.get("data_items", []))
        print(f"  [Agent] Strategist: {slide_count}개 슬라이드 설계")
        print(f"  [Agent] Data Analyst: {data_count}개 데이터 항목 추출")

        # Phase 2: Slide Composer
        print("  [Agent] Phase 2: Slide Composer (JSON 조립)...")
        composer_input = _merge_inputs(strategy_result, data_result, text)
        slides = composer.run(composer_input)
        print(f"  [Agent] Composer: {len(slides)}개 슬라이드 생성")

        # Phase 3: QA Critic with retry loop
        for attempt in range(1, MAX_QA_RETRIES + 2):  # 1 check + up to MAX_QA_RETRIES retries
            print(f"  [Agent] Phase 3: QA Critic (검증 {attempt}차)...")
            qa_result = critic.run(slides)

            errors = [i for i in qa_result.get("issues", []) if i.get("severity") == "error"]
            warnings = [i for i in qa_result.get("issues", []) if i.get("severity") == "warning"]
            print(f"  [Agent] QA: errors={len(errors)}, warnings={len(warnings)}")

            if qa_result.get("passed", False):
                print("  [Agent] QA: PASSED")
                break

            if attempt <= MAX_QA_RETRIES:
                print(f"  [Agent] QA: FAILED — Composer 재시도 ({attempt}/{MAX_QA_RETRIES})...")
                for issue in errors[:3]:
                    print(f"    - [{issue.get('severity')}] {issue.get('message', '')[:80]}")
                slides = composer.run_with_feedback(
                    composer_input, qa_result.get("feedback", ""), slides
                )
                print(f"  [Agent] Composer: {len(slides)}개 슬라이드 재생성")
            else:
                print("  [Agent] QA: 최대 재시도 초과 — 현재 결과 사용")

        _normalize_slides(slides)
        return slides

    except Exception as e:
        print(f"  [Agent] 에이전트 파이프라인 실패: {e}")
        print("  [Agent] 기존 단일 호출 방식으로 폴백...")
        from src.converter import convert_rich
        return convert_rich(text, use_agents=False)
