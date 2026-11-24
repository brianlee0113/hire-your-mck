# Holdout results for Codex (paste the block below)

Prepared 2026-11-23 after the holdout scoring was complete (commit `f073250`, branch `v1.3-h`). The block is
self-contained: Codex does not need the branch to read it. If Codex should check the files themselves, push
`v1.3-h` first (local commits `7ff784e`..`8ac18a5` are not on origin yet).

Sources: `results/holdout/tables.md`, `results/holdout/summary.json`, `docs/06-holdout-deviations.md`,
`results/holdout/human-review/answers-2026-11-23.json`, `eval/holdout-slides/key.json`.

```text
Hire Your McK 홀드아웃(METHODOLOGY §16) 결과야. 네가 쓴 c6–c11, 조건 B / E1 / H2a-restyle, 1회씩 18회. 결과를 검토하고, 아래 질문에 답해 줘. 특히 우리가 결과를 과하게 해석하고 있는 부분이 있으면 지적해 줘.

## 조건
- B: 6줄 방법론 프롬프트 (메인 벤치마크와 동일)
- E1: decision audit을 넣은 스킬 (분석부터 렌더링까지 스킬이 함)
- H2a-restyle: B 덱(추출 텍스트 + 브리핑 팩)을 스킬의 compile 모드로 다시 그림. 비용은 B + compile

## 1. B → H2a: compile이 분석을 지키는가 (primary)
| 케이스 | 핵심 유효 단위 보존 | 핵심 오류 정정 | unsupported / missing / inherited | 새 오류 c/m/m | 숫자 추적 | check.py | Pass | H2a vs B |
|---|---|---|---|---|---|---|---|---|
| c6 make-buy | 81/81 | 0/2 | 0/0/2 | 0/0/0 | 93% | 0 fail | no | tie/split |
| c7 M&A | 74/74 | 0/3 | 0/0/3 | 0/0/1 (minor) | 97% | 0 fail | no | tie/split |
| c8 network | 94/94 | – | 0/0/0 | 0/0/0 | 99% | 0 fail | yes | tie/split |
| c9 capacity | 86/86 | 0/3 | 0/0/3 | 0/0/0 | 97% | 0 fail | no | tie/split |
| c10 portfolio | 73/73 | 1/1 | 0/0/0 | 0/0/0 | 97% | 0 fail | yes | tie/split |
| c11 licensing | 104/104 | 0/1 | 0/0/1 | 0/0/0 | 99% | 0 fail | no | tie/split |

- 보존율: 핵심 유효 단위 512/512 (100%). unsupported_alteration 0, missing 0.
- 정정률: 핵심 오류 1/10. 나머지 9개는 inherited_error (정정도 로그도 없이 그대로 옮김).
- 새 오류: c7 1건 minor (워터폴의 'Board floor' 막대에 $9.0M 대신 최저 현금 8.165가 들어감).
- 사전 규칙상 fidelity pass는 2/6 (c8, c10). 실패 4개는 전부 inherited_error 때문이고, H1에서 본 실패 유형(재순위, 반올림 drift, 주장 누락)은 다시 나오지 않음.
- H2a vs B 쌍대비교: 6/6 tie/split (규칙상 "compile로 잃은 것 없음"이 기대 결과).

## 2. E1 vs H2a: 최종 산출물로 무엇이 나은가
| 케이스 | E1 vs H2a | E1 vs B | Rubric B / E1 / H2a | 장수 B / E1 / H2a | 비용 B / E1 / H2a | API 분 B / E1 / H2a |
|---|---|---|---|---|---|---|
| c6 | H2a | B | 4.15 / 4.40 / 4.15 | 18 / 20 / 23 | $3.15 / $5.12 / $13.09 | 12.5 / 17.6 / 41.0 |
| c7 | H2a | B | 4.40 / 4.40 / 4.15 | 20 / 23 / 22 | $2.39 / $4.06 / $10.53 | 11.3 / 13.9 / 34.5 |
| c8 | H2a | B | 4.65 / 4.90 / 4.90 | 18 / 19 / 22 | $3.78 / $3.28 / $11.52 | 15.0 / 11.4 / 38.1 |
| c9 | H2a | B | 4.40 / 4.40 / 4.40 | 20 / 18 / 23 | $3.88 / $3.72 / $12.53 | 13.2 / 13.6 / 40.5 |
| c10 | H2a | B | 4.65 / 4.65 / 4.65 | 19 / 18 / 21 | $3.21 / $3.53 / $11.65 | 11.8 / 12.5 / 37.0 |
| c11 | H2a | B | 4.65 / 4.40 / 4.40 | 20 / 21 / 22 | $2.14 / $4.48 / $10.45 | 9.8 / 15.3 / 34.2 |

- 쌍대비교 (Fable 5.2, 단어 수 없음, 양쪽 순서 일치할 때만 승): H2a가 E1에 6–0, B가 E1에 6–0.
- Rubric 평균: B 4.48, E1 4.53, H2a 4.44. 답안키 기준 점수로는 세 조건 차이가 작음.
- 총비용: B $18.55, E1 $24.19, H2a $69.78 (B + compile $51.23). H2a는 B의 약 3.5배 비용, 약 3배 API 시간.

## 3. 제작자 블라인드 슬라이드 리뷰 (시각 품질)
- 자동 판정을 보기 전에 진행. 18쌍 중 7쌍에서 중단 (반복적이라고 느낌). 종합 판정 6쌍, 1쌍은 일부 항목만.
- H2a vs B: H2a 2–0 (둘 다 clear). 같은 쌍에서 judge는 tie.
- H2a vs E1: 1–1 (H2a slight, E1 clear).
- E1 vs B: 1–1 (E1 clear, B slight).
- judge와 비교: 둘 다 승부가 난 4쌍 중 2쌍 일치. E1이 낀 두 쌍(P1, P7)에서 리뷰는 E1, judge는 반대.
- 한계: 응답한 쌍 대부분에서 한쪽 덱을 알아봤다고 표시 (완전한 블라인드 아님). 표본이 작음.
- 조건 공통 피드백: 폰트가 작고 장표당 내용이 많음 (주로 B 덱), E1 포맷이 단조로움, B 덱의 박스 수식이 너무 단순해 보임, 좁은 칸의 차트 라벨이 겹치고 잘림 (H2a c7 4쪽).

## 4. 사전 계획과 달라진 점 (docs/06-holdout-deviations.md)
- E1의 check.py 값은 e2e.json(현재 저장소 check.py, E2 규칙 포함) 대신 E1 자체 check.py 값으로 보고 (6개 모두 0 fail). judge는 check.py 결과를 보지 않음.
- 평가 실행은 사용량 guard를 0.96으로 올려 진행. pairwise 16건이 Fable 한도(429)에 막혔다가 11/23에 재실행해 36/36 완료. 동결 파일 검증 통과 후 실행.
- 리뷰 7/18쌍 중단 (위 3번).
- 홀드아웃 이후 렌더러 수정 (8ac18a5): 좁은 칸 차트의 범주 이름·값 라벨 크기 맞춤, 차트가 너무 얇거나 낮을 때 경고. c7 H2a 4쪽을 보고 고친 것이라 홀드아웃 덱으로 이 수정을 평가할 수는 없음. 홀드아웃 점수는 수정 전 렌더러로 만든 덱 기준이라 영향 없음.

## 우리의 해석 (검토해 줘)
1. 분석은 스킬이 아니라 6줄 프롬프트가 맡는 게 맞다. 스킬이 분석까지 하면(E1) 처음 보는 케이스에서도 B에 6–0으로 진다. 개발 케이스 결과(E1 vs B 0–10)가 반복됐다.
2. H2a는 손실 없는 렌더러다. 핵심 내용 100% 보존, judge 기준 B와 동등, 제작자 리뷰에서는 시각적으로 B보다 나음(2–0, 약한 근거).
3. 하지만 H2a는 QA가 아니다. B의 핵심 오류 10개 중 9개를 그대로 옮긴다. "검증된 정정만 한다"는 규칙이 너무 보수적으로 작동했거나, compile이 오류를 찾지 못한 것.
4. 비용 3.5배, 시간 3배라서 H2a를 기본값으로 배포하지 않는다. 선택 모드(기존 덱·분석을 다시 그릴 때)로 두고, H2b(B가 덱 대신 결정 요약 + 스토리라인 → 스킬이 바로 렌더링)로 시간·비용을 줄일 수 있는지 개발 케이스 c2·c5에서 먼저 잰다.

## 질문
1. 위 해석 중 데이터보다 강하게 말하고 있는 부분이 있나? 특히 "H2a가 E1보다 낫다(6–0)"를 §16 규칙("5 of 6 이상이 허용되는 가장 강한 표현")에 맞게 어떻게 쓰는 게 맞을까? E1 vs B도 6–0인데, H2a vs E1 결과를 compile의 효과로 읽어도 되나, 아니면 B의 분석이 이긴 것으로만 읽어야 하나?
2. fidelity pass 2/6을 어떻게 보고해야 하나? 실패가 모두 inherited_error인데, compile의 목적(손실 없는 매핑)과 pass 규칙(오류 정정까지 요구)이 어긋난 건지, 아니면 정정을 못 한 게 진짜 실패인지.
3. 오류 정정률 1/10을 올리려면 compile에 무엇을 바꿔야 할까? (검증 기준 완화는 H1에서 재순위 같은 의미 변경을 낳았음.) 아니면 정정은 compile의 역할에서 빼고 별도 QA 단계로 두는 게 맞나?
4. 불완전한 제작자 리뷰(7/18쌍, 대부분 한쪽 덱을 알아봄)를 공개 글에서 어떻게 표현해야 할까?
5. HN 게시 문구 후보: "스킬로 분석하게 하면 6줄 프롬프트에 진다. 스킬은 렌더링을 맡을 때 의미가 있고, 분석 오류는 고쳐 주지 않는다." 이 문구가 데이터에 맞는지, 빠진 단서가 있는지.
6. H2b 실험 설계(개발 케이스 c2·c5, B-brief 2회 + compile 2회, H1s와 비용·시간·fidelity 비교)에 고칠 점이 있나?
```
