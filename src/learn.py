"""CLI entry point for the learning loop system.

Usage:
    python src/learn.py                          # 전체 샘플 학습
    python src/learn.py --sample sample_01.pptx  # 특정 샘플만
    python src/learn.py --report-only            # 리포트만 (logic.md 자동 반영 안 함)
    python src/learn.py --guide "차트보다 테이블 위주로"  # 추가 가이드 전달
"""
import argparse
import os
import sys
from dotenv import load_dotenv

load_dotenv()

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import learner

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAMPLES_DIR = os.path.join(BASE_DIR, "samples", "structure")


def main():
    ap = argparse.ArgumentParser(
        description="학습 루프 — samples/structure/ 샘플로 장표 생성 로직 개선"
    )
    ap.add_argument(
        "--sample",
        default=None,
        help="특정 샘플 파일명 (예: sample_01.pptx). 미지정 시 전체 실행",
    )
    ap.add_argument(
        "--project",
        default="test-project",
        help="프로젝트 코드 (디자인 스펙 선택)",
    )
    ap.add_argument(
        "--report-only",
        action="store_true",
        help="리포트만 생성 (logic.md 자동 반영 안 함)",
    )
    ap.add_argument(
        "--guide",
        default=None,
        help="추가 가이드/팁 텍스트 (Claude API 분석에 반영)",
    )
    args = ap.parse_args()

    print("=" * 60)
    print("  학습 루프 시스템 시작")
    print("=" * 60)

    # Run learning
    if args.sample:
        sample_path = os.path.join(SAMPLES_DIR, args.sample)
        if not os.path.exists(sample_path):
            print(f"파일을 찾을 수 없습니다: {sample_path}")
            sys.exit(1)
        result = learner.learn_from_sample(sample_path, args.project, guide=args.guide)
        all_results = [result] if result else []
    else:
        all_results = learner.run_all_samples(args.project, guide=args.guide)

    if not all_results:
        print("\n분석 결과가 없습니다.")
        sys.exit(0)

    # Save individual reports
    print(f"\n{'='*60}")
    print("  리포트 저장")
    print(f"{'='*60}")

    for result in all_results:
        report_path = learner.save_report(result)
        print(f"  리포트 저장: {report_path}")

    # Apply to logic.md (unless --report-only)
    if not args.report_only:
        print(f"\n{'='*60}")
        print("  logic.md 자동 업데이트")
        print(f"{'='*60}")
        learner.apply_to_logic_md(all_results)

    # Update feedback log
    learner.update_feedback_log(all_results)

    # Summary
    print(f"\n{'='*60}")
    print("  학습 완료 요약")
    print(f"{'='*60}")
    print(f"  분석 샘플: {len(all_results)}개")

    total_suggestions = sum(
        len(r.get("improvement_suggestions", [])) for r in all_results
    )
    print(f"  총 개선 제안: {total_suggestions}개")

    if not args.report_only:
        updates = sum(
            1 for r in all_results
            if r.get("logic_md_updates", "").strip()
            and r.get("logic_md_updates", "").strip() != "(없음)"
        )
        print(f"  logic.md 업데이트: {updates}건")

    print(f"\n  리포트 위치: docs/learning-reports/")
    print()


if __name__ == "__main__":
    main()
