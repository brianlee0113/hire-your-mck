# Holdout case request for Codex (paste the block below)

Prepared 2026-11-18 for the held-out test of H2a / B / E1. Codex writes the cases; the skill and every condition are
frozen before the cases arrive, and nothing in the skill is changed after their answer keys have been seen.

Before pasting: Codex reads GitHub. The `benchmark` branch (pushed) has the case pipeline it needs; it does not need
the newer branches for this task.

```text
Hire Your McK 홀드아웃 검증용 새 케이스 6개와 정답키를 독립적으로 작성해 줘. 스킬을 수정한 쪽(Claude)이 케이스를 쓰면 편향이 생길 수 있어서 너에게 맡기는 거야. 스킬과 비교 조건(B, E1, H2a)은 케이스를 받기 전에 고정하고, 정답키를 본 뒤에는 스킬을 고치지 않을 거야.

## 기존 형식 (브랜치 benchmark, 경로는 benchmark/ 기준)
- 케이스 생성: cases/models.py(결정론적 계산), cases/build_cases.py(팩·정답키 생성)
- 브리핑 팩: cases/<case_id>/packet.md (기존 775~1,585단어, 섹션: 맥락, 의사결정 질문, 목표·제약, 경영진의 초기 가설, 시장·운영 데이터, 테스트 결과, 고객, 자본, 기타 자료, 불확실성)
- 정답키: answer_keys/<case_id>.json, .md, .calc.json
  - json 필드: case_id, title, decision_question, initial_hypothesis{holder, statement, expected_handling}, key_insights[{id, critical, text}], required_calculations[{id, text, expected, tolerance}], decision_relevant_evidence[{id, critical, text}], contradictory_evidence, reasoning_traps[{id, text}], key_tradeoffs[{id, text}], plausible_recommendations[{id, defensible, text}], defensibility_criteria
- 케이스 메타: config/experiment.json의 cases.<case_id> = {decision_maker, decision_question}

## 요청
1. case_id는 c6~c11. 기존 다섯 개(시장 진입, 마진 회복, AI 기능 출시, 가격 인상과 이탈, 진출 포기)와 문제 구조가 다르게. 네가 제안한 make-or-buy, M&A, 공급망 네트워크 재설계에 세 개를 더해 줘(예: 설비 투자 시점, 포트폴리오 정리, 파트너십·라이선스 등 네 판단으로).
2. initial_hypothesis.expected_handling은 keep_with_conditions 2개, revise 2개, reject 2개로 섞어 줘.
3. 각 팩에 기존처럼 세 가지 함정을 심어 줘: 정의의 불일치, 상관을 인과로 읽은 주장, 결함 있는 내부 지표. 그리고 결론을 바꾸는 binding constraint(현금, 일정, 승인, 용량 등) 하나 이상.
4. 모든 숫자는 서로 맞아야 하고, 계산은 결정론적 코드(models.py 방식)로 만들어 .calc.json에 남겨 줘. 팩은 800~1,600단어.
5. 정답키 json에 decision_requirements를 추가해 줘. 특정 장표 유형이나 표현을 강요하지 않고, 결정에 필요한 분석이 빠졌는지를 판단하기 위한 필드야.
   [{"id": "D1", "question": "Does the recommended option satisfy the cash constraint?", "critical": true, "acceptable_evidence": ["cash bridge", "scenario model"], "unnecessary_if": null}]
6. 케이스를 특정 조건이 유리하게 설계하지 마. 실제 컨설팅 의사결정처럼, 좋은 답이 여러 개일 수 있고 짧고 정확한 답이 길고 포괄적인 답보다 나을 수 있는 케이스면 좋아.
7. 결과물: benchmark 브랜치에서 새 브랜치(holdout-cases)로 PR을 만들 수 있으면 PR로, 아니면 파일별 전체 내용을 답변에 붙여 줘. packet.md와 정답키는 분리해서 보여 줘.
```

## After the cases arrive

1. Put them in place; regenerate nothing in the existing five cases.
2. Freeze `FREEZE-holdout.json` (skill snapshot, prompts, conditions B / E1 / H2a, judges, reading rules) before the
   first run; the generation sandbox already denies reads of `answer_keys/`.
3. Run after the usage reset (2026-11-21 17:00): 6 cases × 1 replicate × 3 conditions.
