"""CLI entry point for McKinsey PPT Generator."""
import argparse
import os
import sys
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import detector, parser, converter, config, generator


def main():
    ap = argparse.ArgumentParser(
        description="McKinsey-style PPT Generator - Exe Sum 텍스트로 PPT 자동 생성"
    )
    ap.add_argument("--input", required=True, help="입력 텍스트 파일 경로")
    ap.add_argument("--theme", "--project", dest="project", default="navy",
                    help="Theme key in templates/themes.json (default: navy)")
    ap.add_argument("--font-pair", default=None,
                    help="Override the theme's font pair (e.g. aptos-serif-aptos, arial)")
    ap.add_argument("--output", default=None, help="출력 .pptx 파일 경로")
    ap.add_argument("--legacy", action="store_true",
                    help="줄글 입력도 기존 닷/대시 변환 경로 사용 (디버그용)")
    ap.add_argument("--agents", action="store_true",
                    help="멀티 에이전트 파이프라인 사용 (고품질, 느림)")
    args = ap.parse_args()

    # Read input
    with open(args.input, "r", encoding="utf-8") as f:
        text = f.read()

    print(f"입력 파일: {args.input}")
    print(f"프로젝트: {args.project}")

    # Detect input type
    input_type = detector.detect(text)
    print(f"입력 타입: {input_type}")

    # Load design config
    cfg = config.load(args.project, args.font_pair)

    # Determine output path
    if args.output:
        output_path = args.output
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "output")
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, f"{args.project}_{timestamp}.pptx")

    if input_type == "longform" and not args.legacy:
        # ── Rich path: longform → JSON slide specs → PPT ──
        if args.agents:
            print("줄글 → 멀티 에이전트 파이프라인으로 변환 중...")
        else:
            print("줄글 → 리치 슬라이드 JSON 변환 중 (Claude API)...")
        slides_specs = converter.convert_rich(text, use_agents=args.agents)
        print(f"변환 완료: {len(slides_specs)}개 슬라이드")

        for i, spec in enumerate(slides_specs):
            prefix = "[참고] " if spec.get("is_backup") else ""
            blocks = spec.get("content_blocks", [])
            blocks_summary = ", ".join(b["type"] for b in blocks)
            print(f"  {i+1}. {prefix}{spec['title'][:60]}")
            print(f"     블록: {blocks_summary}")

        generator.generate_rich(slides_specs, cfg, output_path)

    else:
        # ── Dot/dash path: parse → generate (internally uses rich format) ──
        if input_type == "longform":
            print("줄글 → 닷/대시 변환 중 (Claude API, legacy 모드)...")
            text = converter.convert(text)
            print("변환 완료.\n변환 결과:")
            print(text)
            print()

        slides_data = parser.parse(text)
        print(f"파싱 완료: {len(slides_data)}개 슬라이드")

        for i, sd in enumerate(slides_data):
            prefix = "[참고] " if sd["is_backup"] else ""
            print(f"  {i+1}. {prefix}{sd['title'][:60]}")
            for sb in sd["sub_bullets"]:
                hints = []
                if sb["position"]:
                    hints.append(sb["position"])
                if sb["data_type"]:
                    hints.append(f"{sb['data_type']}: {sb['data_title']}")
                hint_str = f" ({', '.join(hints)})" if hints else ""
                print(f"     - {sb['text'][:50]}{hint_str}")

        generator.generate(slides_data, cfg, output_path)

    print(f"\nPPT 생성 완료: {output_path}")


if __name__ == "__main__":
    main()
