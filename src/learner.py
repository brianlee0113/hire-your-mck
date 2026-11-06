"""Learning loop: compare reference vs generated slides, extract improvements.

Uses Claude API to analyze structural differences and suggest rule updates.
Automatically updates docs/logic.md with learned rules.
"""
import os
import sys
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import parser, config, generator, structure_extractor
from src.api_client import call_claude, parse_json_response

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAMPLES_DIR = os.path.join(BASE_DIR, "samples", "structure")
REPORTS_DIR = os.path.join(BASE_DIR, "docs", "learning-reports")
LOGIC_MD_PATH = os.path.join(BASE_DIR, "docs", "logic.md")
FEEDBACK_LOG_PATH = os.path.join(BASE_DIR, "docs", "feedback-log.md")

ANALYSIS_SYSTEM_PROMPT = """당신은 맥킨지 스타일 PPT 장표의 구조를 분석하는 전문가입니다.
동일한 닷/대시 입력에 대해 [레퍼런스 장표 구조]와 [현재 시스템이 생성한 장표 구조]를 비교하여
생성 로직의 개선점을 도출해주세요.

## 분석 항목
1. **슬라이드 매핑**: 닷 1개 = 1장인지, 다른 매핑 패턴이 있는지
2. **타이틀(리드 메시지)**: 닷 텍스트가 타이틀로 정확히 매핑되는지, 포맷 차이
3. **콘텐츠 블록 유형**: 레퍼런스에서 chart/table/textbox/diagram 중 어떤 유형을 사용하는지
4. **레이아웃 패턴**: full/split/3col 등 레이아웃 선택 기준
5. **세부 구조**: 차트의 시리즈/카테고리 수, 테이블의 행/열 수 등
6. **누락된 요소**: subtitle, source, footnote, callout, 강조 박스 등
7. **시각 패턴**: 색상, 폰트 크기, 강조 방식의 차이

## 출력 형식
반드시 아래 JSON 형식으로만 출력하세요. 다른 텍스트는 포함하지 마세요.

```json
{
  "summary": "전체 비교 요약 (2-3문장)",
  "slide_mapping_rules": [
    "닷→슬라이드 매핑에 대한 관찰/규칙"
  ],
  "content_type_rules": [
    "콘텐츠 유형(차트/테이블/텍스트) 선택에 대한 관찰/규칙"
  ],
  "layout_rules": [
    "레이아웃 패턴 선택에 대한 관찰/규칙"
  ],
  "missing_elements": [
    "현재 시스템에서 누락된 요소"
  ],
  "improvement_suggestions": [
    "구체적 코드/로직 개선 제안"
  ],
  "logic_md_updates": "docs/logic.md에 추가할 새로운 규칙/패턴 텍스트 (마크다운 형식)"
}
```"""




def _load_guide_text(sample_pptx_path, cli_guide=None):
    """Load guide text from companion .txt file and/or CLI argument.

    Looks for a .txt file with the same name as the PPTX.
    Combines file guide + CLI guide if both exist.
    """
    parts = []

    # Check for companion .txt file
    txt_path = os.path.splitext(sample_pptx_path)[0] + ".txt"
    if os.path.exists(txt_path):
        with open(txt_path, "r", encoding="utf-8") as f:
            file_guide = f.read().strip()
        if file_guide:
            parts.append(file_guide)

    # CLI guide
    if cli_guide:
        parts.append(cli_guide)

    return "\n\n".join(parts) if parts else None


def learn_from_sample(sample_pptx_path, project_code="test-project", guide=None):
    """Run learning loop for a single sample PPTX.

    Args:
        sample_pptx_path: Path to sample PPTX (slide 1 = dot/dash, rest = reference)
        project_code: Project code for design config
        guide: Optional guide text (tips/instructions for the analysis)

    Returns:
        dict: Analysis results from Claude API
    """
    sample_name = os.path.splitext(os.path.basename(sample_pptx_path))[0]
    print(f"\n{'='*60}")
    print(f"학습 시작: {sample_name}")
    print(f"{'='*60}")

    # Step 1: Extract dot/dash text from slide 1
    print("\n[1/5] 닷/대시 텍스트 추출 중...")
    dotdash_text = structure_extractor.extract_dotdash_from_slide(sample_pptx_path)
    if not dotdash_text:
        print("  ⚠ 슬라이드 1에서 텍스트를 찾을 수 없습니다.")
        return None
    print(f"  추출된 텍스트: {dotdash_text[:100]}...")

    # Load guide text
    guide_text = _load_guide_text(sample_pptx_path, guide)
    if guide_text:
        print(f"\n  가이드 텍스트 로드됨 ({len(guide_text)}자)")

    # Step 2: Extract reference structure from slides 2+
    print("\n[2/5] 레퍼런스 장표 구조 추출 중...")
    ref_structure = structure_extractor.extract_slide_structure(sample_pptx_path, skip_first=True)
    print(f"  레퍼런스 슬라이드: {len(ref_structure)}장")
    for s in ref_structure:
        print(f"    슬라이드 {s['slide_num']}: {s['title'][:50] if s['title'] else '(제목없음)'} "
              f"- {s['layout_pattern']} ({s['num_content_blocks']}개 블록)")

    # Step 3: Parse and generate with current system
    print("\n[3/5] 현재 시스템으로 생성 중...")
    slides_data = parser.parse(dotdash_text)
    print(f"  파싱 결과: {len(slides_data)}개 슬라이드")

    cfg = config.load(project_code)

    gen_structure = []
    gen_text = "(파싱 실패 — 닷/대시 마커(•, -)가 없는 텍스트)"

    if slides_data:
        # Generate to temp file
        temp_dir = os.path.join(BASE_DIR, "output", "learn_temp")
        os.makedirs(temp_dir, exist_ok=True)
        temp_path = os.path.join(temp_dir, f"{sample_name}_generated.pptx")
        generator.generate(slides_data, cfg, temp_path)
        print(f"  생성 완료: {temp_path}")

        # Step 4: Extract structure from generated PPTX
        print("\n[4/5] 생성된 장표 구조 추출 중...")
        gen_structure = structure_extractor.extract_slide_structure(temp_path, skip_first=False)
        gen_text = structure_extractor.structure_to_text(gen_structure)
        print(f"  생성된 슬라이드: {len(gen_structure)}장")
    else:
        print("  ⚠ 파서가 닷/대시를 인식하지 못했습니다. 레퍼런스만 분석합니다.")
        print("\n[4/5] 건너뜀 (생성 결과 없음)")

    # Step 5: Compare using Claude API
    print("\n[5/5] Claude API로 비교 분석 중...")
    ref_text = structure_extractor.structure_to_text(ref_structure)

    user_message = f"""## 닷/대시 입력
```
{dotdash_text}
```

## 레퍼런스 장표 구조 (목표)
```
{ref_text}
```

## 현재 시스템 생성 결과
```
{gen_text}
```

위 레퍼런스와 생성 결과를 비교 분석해주세요."""

    if guide_text:
        user_message += f"""

## 사용자 가이드/팁
```
{guide_text}
```

위 가이드를 반드시 반영하여 분석해주세요."""

    response_text = call_claude(ANALYSIS_SYSTEM_PROMPT, user_message)
    analysis = parse_json_response(response_text)
    analysis["sample_name"] = sample_name
    analysis["timestamp"] = datetime.now().isoformat()
    analysis["dotdash_input"] = dotdash_text
    analysis["ref_slide_count"] = len(ref_structure)
    analysis["gen_slide_count"] = len(gen_structure)

    print(f"\n  분석 완료:")
    print(f"  요약: {analysis.get('summary', 'N/A')}")
    print(f"  개선 제안: {len(analysis.get('improvement_suggestions', []))}개")

    return analysis


def run_all_samples(project_code="test-project", guide=None):
    """Run learning loop for all samples in samples/structure/.

    Args:
        project_code: Project code for design config
        guide: Optional CLI guide text (applied to all samples)

    Returns:
        list of analysis results
    """
    if not os.path.isdir(SAMPLES_DIR):
        print(f"샘플 디렉토리가 없습니다: {SAMPLES_DIR}")
        return []

    sample_files = [f for f in os.listdir(SAMPLES_DIR)
                    if f.endswith(".pptx") and not f.startswith("~$")]
    if not sample_files:
        print(f"samples/structure/에 PPTX 파일이 없습니다.")
        return []

    print(f"\n총 {len(sample_files)}개 샘플 발견")
    results = []

    for f in sorted(sample_files):
        filepath = os.path.join(SAMPLES_DIR, f)
        try:
            result = learn_from_sample(filepath, project_code, guide=guide)
            if result:
                results.append(result)
        except Exception as e:
            print(f"\n  ⚠ 오류 발생 ({f}): {e}")

    return results


def save_report(analysis, report_dir=None):
    """Save individual learning report as markdown.

    Args:
        analysis: Analysis result dict
        report_dir: Directory to save report (default: docs/learning-reports/)

    Returns:
        str: Path to saved report
    """
    report_dir = report_dir or REPORTS_DIR
    os.makedirs(report_dir, exist_ok=True)

    sample_name = analysis["sample_name"]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{sample_name}_report_{timestamp}.md"
    filepath = os.path.join(report_dir, filename)

    lines = [
        f"# 학습 리포트: {sample_name}",
        f"\n> 분석일: {analysis.get('timestamp', 'N/A')}",
        f"> 레퍼런스 슬라이드: {analysis.get('ref_slide_count', '?')}장",
        f"> 생성 슬라이드: {analysis.get('gen_slide_count', '?')}장",
        "",
        "## 요약",
        analysis.get("summary", "N/A"),
        "",
        "## 닷/대시 입력",
        "```",
        analysis.get("dotdash_input", ""),
        "```",
        "",
        "## 슬라이드 매핑 규칙",
    ]
    for rule in analysis.get("slide_mapping_rules", []):
        lines.append(f"- {rule}")

    lines.extend(["", "## 콘텐츠 유형 규칙"])
    for rule in analysis.get("content_type_rules", []):
        lines.append(f"- {rule}")

    lines.extend(["", "## 레이아웃 규칙"])
    for rule in analysis.get("layout_rules", []):
        lines.append(f"- {rule}")

    lines.extend(["", "## 누락된 요소"])
    for item in analysis.get("missing_elements", []):
        lines.append(f"- {item}")

    lines.extend(["", "## 개선 제안"])
    for suggestion in analysis.get("improvement_suggestions", []):
        lines.append(f"- {suggestion}")

    lines.extend([
        "",
        "## logic.md 업데이트 제안",
        analysis.get("logic_md_updates", "(없음)"),
    ])

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    return filepath


def apply_to_logic_md(all_analyses):
    """Append learned rules to docs/logic.md.

    Args:
        all_analyses: List of analysis result dicts
    """
    if not all_analyses:
        return

    # Collect all logic_md_updates
    updates = []
    for analysis in all_analyses:
        update_text = analysis.get("logic_md_updates", "").strip()
        if update_text and update_text != "(없음)":
            updates.append({
                "sample": analysis["sample_name"],
                "text": update_text,
            })

    if not updates:
        print("\nlogic.md에 추가할 업데이트가 없습니다.")
        return

    # Read existing logic.md
    with open(LOGIC_MD_PATH, "r", encoding="utf-8") as f:
        existing = f.read()

    # Append new section
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    new_section = f"\n\n---\n\n## 9. 학습 루프 피드백 ({timestamp})\n\n"
    new_section += f"> 자동 학습으로 추출된 규칙 ({len(updates)}개 샘플 기반)\n\n"

    for update in updates:
        new_section += f"### 샘플: {update['sample']}\n\n"
        new_section += update["text"] + "\n\n"

    with open(LOGIC_MD_PATH, "w", encoding="utf-8") as f:
        f.write(existing + new_section)

    print(f"\nlogic.md 업데이트 완료 ({len(updates)}개 규칙 추가)")


def update_feedback_log(all_analyses):
    """Record learning run in feedback-log.md.

    Args:
        all_analyses: List of analysis result dicts
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    entry = f"\n### 학습 루프 실행 — {timestamp}\n\n"
    entry += f"**분석 샘플**: {len(all_analyses)}개\n\n"

    for analysis in all_analyses:
        entry += f"- **{analysis['sample_name']}**: "
        entry += f"레퍼런스 {analysis.get('ref_slide_count', '?')}장 vs "
        entry += f"생성 {analysis.get('gen_slide_count', '?')}장\n"
        summary = analysis.get("summary", "")
        if summary:
            entry += f"  - {summary[:100]}\n"

    suggestions_count = sum(
        len(a.get("improvement_suggestions", [])) for a in all_analyses
    )
    entry += f"\n**도출된 개선 제안**: {suggestions_count}개\n"

    with open(FEEDBACK_LOG_PATH, "a", encoding="utf-8") as f:
        f.write(entry)

    print(f"feedback-log.md 업데이트 완료")
