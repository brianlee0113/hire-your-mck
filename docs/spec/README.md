# Storyline spec v0.1

대화(사용자 입력)와 렌더러(PPTX + 소스 엑셀) 사이에 있는 **단일 원본**이다. 모드 3개가 모두 같은 spec을 쓴다.
모드가 다르면 장표가 **어느 상태까지 진행되는지**만 다르다.

- 스키마: `storyline.schema.json` (JSON Schema 2020-12)
- 예시: `examples/example-deck.json`. 한 덱 안에 filled, ghost, drafted 장표가 섞여 있다. 회사와 숫자는 전부 가상이다
- 검사: `python tools/spec/check.py <spec.json>`. 스키마 검사와 원칙 기반 교차 검사를 한다

## 1. 흐름

```
입력(붙여넣기 / Q&A / 리드 메시지)
   │
   ▼
① storyline      governing_thought + exec_summary[] (리드 메시지 3~7개)
   │              └ exec item id = section id = 제목 접두어 (A-08)
   ▼
② slides[]       장표마다 lead_message, message_type, archetype을 정한다 (라우팅 표)
   │              status = ghost  ──────────────▶  deck_flow 모드는 여기서 렌더
   ▼
③ data_requirements[]  장표마다 "무엇이 있어야 증명되는가"
   │              사용자 데이터 → 웹 리서치 → 없으면 placeholder (D2)
   ▼
④ body + data_points[] + sources[]
   │              status = drafted (placeholder 있음) → filled (전부 출처 있음)
   ▼
⑤ QA (check.py)  status = qa_passed
   │
   ▼
렌더러 → deck.pptx + sources.xlsx (data_points를 slide_id별로 묶어 시트 하나에 장표 하나)
```

| 모드 | 진입 | 장표의 최종 상태 |
|---|---|---|
| `deck_detailed` | ① | `filled` → `qa_passed` |
| `deck_flow` | ① | `ghost`: 리드 메시지 + Archetype + 권장 데이터만 있음 |
| `single_slide` | ②. exec_summary 1개, 본문 장표 1장 | `filled` |

플로우 모드 덱을 디테일 모드로 **승격**할 때는 같은 spec에서 ghost 장표의 data_requirements를 채우기만 하면 된다.

## 2. 장표 상태

| status | 조건 | 렌더 결과 |
|---|---|---|
| `ghost` | lead_message, archetype, data_requirements만 있음 | 제목 + 점선 와이어프레임 + "권장 데이터" 박스 + 스티커 |
| `drafted` | body는 있지만 placeholder가 남아 있음 | 실제 차트 + 점선 `?` 막대 + `ILLUSTRATIVE — DATA NEEDED` |
| `filled` | 모든 point가 출처 있는 data_point를 참조함 | 완성 장표 |
| `qa_passed` | check.py에서 fail 0 | 완성 장표 |

## 3. 핵심 설계 결정

1. **숫자는 장표에 직접 쓰지 않는다.** 차트, KPI, 사이드바의 모든 값은 `point`이고, point는 둘 중 하나다.
   - `{"data_ref": "d1-3"}`: data_points의 한 행을 가리킨다. 그 행에는 반드시 `source_id`가 있다
   - `{"placeholder": true}`: 값을 모르는 상태다
   스키마 단계에서 "출처 없는 숫자"를 만들 수 없다(D5, A-07).
2. **data_points 한 행 = 소스 엑셀 한 행.** 컬럼은 Data point | Value | Unit | Period | Source | URL | Excerpt | Accessed | Used in이다.
   계산값은 `source.kind = derived`, `derived_from`, `formula`로 근거를 남긴다.
3. **출처 우선순위 (D2).** `user_provided` > `web` > `derived`. 같은 값이 충돌하면 사용자 자료를 쓰고, 차이는 footnote에 남긴다.
4. **ID가 덱 구조를 만든다.**
   - exec item id = section id = 제목 접두어
   - 본문 장표는 정확히 하나의 exec item에 속한다(B-04)
   - backup은 `backup_of`로 본 장표 바로 뒤에 붙는다(S4)
   - tracker는 sections에서 자동으로 만든다(S3)
5. **원칙은 필드로 표현한다.** 예: `lead_message.highlights`(A-02), `count_word`(A-04), `clauses`(A-05), `numbers[].data_ref`(A-01).
   그래서 원칙 위반을 기계적으로 잡을 수 있다.
6. **body는 Archetype 20종을 12가지 kind로 묶는다.**

| kind | Archetype |
|---|---|
| `chart` | bar-ranking, column-time-series, line-trend, stacked-column, waterfall-bridge, stacked-100, scatter-bubble, survey-bars |
| `kpi` | kpi-big-numbers |
| `panels` | multi-chart-panel (패널 2~4개, 패널마다 chart 또는 kpi) |
| `table` | comparison-table, harvey-ball-table, data-table, heatmap, definition-table |
| `framework` | framework-pillars |
| `process` | process-flow |
| `timeline` | timeline-roadmap |
| `matrix` | matrix-2x2 |
| `tree` | issue-tree |
| `text` | bullet-argument, text-columns, statement (`style: "statement"`), quote-interview (`style: "quotes"`) |
| `levers` | numbered-levers |
| `case` | case-example |

## 3b. v2 밀도 필드 (A-12, 2026-11-05)

| 필드 | 위치 | 쓰임 |
|---|---|---|
| `so_what` + `so_what_style` | slide | 본문 아래 결론 한 문장(선택). `bar` = 진한 띠, `line` = 가는 선 + SO WHAT 라벨. ghost 장표에서는 "증명할 결론"으로 사이드바에 들어간다 |
| `callout` (`target`, `header`, `detail`) | slide | 제목이 가리키는 요소 하나에 붙는 강조 상자. target = 열·행·단계·항목의 header, label, id 또는 code. 텍스트 열, 프레임워크, 프로세스, 표, 레버에서 그린다 |
| `titled_item.footer` | 열·프레임워크·프로세스 | 박스 아래 굵은 한 줄(담당·시작 시점, 단계의 통과 조건) |
| `layout.sidebar.rows[]` (`label`, `point`, `highlight`) | layout | 사이드바 아래쪽의 값 행. 본문 값에서 계산한 숫자만 쓰되 단순 합·차는 쓰지 않는다(B-05, B-06). 추정치면 `basis`로 계산식을 적는다(B-08). 단위가 모두 같을 때만 막대를 그린다 |
| 사이드바 `bullets`의 `**머리말:**` | layout | 굵은 머리말로 차트의 막대·구간·선을 하나씩 짚는 해석 불렛 |
| placeholder `point.label` | point | 값이 없을 때 무엇이 필요한지. 이유 패널에서 "Data needed: …"로 보인다 |
| `body.rows[].note` | 표 | 행마다 평가 한 줄(선택). 레퍼런스처럼 평가는 표 안의 마지막 열(`columns`에 "Verdict")로 넣는 것을 권장한다. 행 구분선을 공유해 행이 구별된다 |
| `storyline.next_steps[]` (`action`, `owner`, `timing`) | storyline | 마무리 장표 오른쪽의 Next steps 패널 |
| `layout.sidebar.kind: "reasons"` + `reasons[]` | layout | 번호가 붙은 이유 2~4개(헤더, 한 줄 설명, 선택 point). 2x2의 오른쪽 패널에 쓴다 |
| `layout.sidebar.note` | layout | 사이드바 맨 아래 한 줄(다음 단계 등) |
| `items[].relation`, `items[].drivers[]` | body kpi | 비교 한 줄, 숫자를 만드는 요인 2~4줄(값이 없으면 빠진 것) |
| `titled_item.point` + `point_caption` | 열·프레임워크·프로세스 | 박스 아래 효과 숫자와 그 라벨 |
| ghost 장표의 `body` | slide | 값이 전부 placeholder인 뼈대. 실제 항목 이름과 축으로 그린다. data_ref가 있으면 fail |

## 4. check.py가 검사하는 원칙

| 규칙 | 검사 내용 | 수준 |
|---|---|---|
| schema | JSON Schema 유효성 | fail |
| **B-04** | 모든 exec item에 근거 장표가 있다. 모든 본문 장표가 정확히 1개의 exec item에 속한다 | fail |
| A-01 | 제목 속 숫자가 `numbers[]`에 선언됐고, 그 data_ref가 본문이나 사이드바에 실제로 있다 | fail / warn |
| A-02 | 제목의 highlights = 차트의 highlight | fail |
| A-03 | 제목 25단어 초과는 fail, 21단어 초과는 warn | fail / warn |
| A-04 | count_word = 본문 요소 수 | fail |
| A-05 | 절이 2개인 제목인데 split_2나 panels가 아니다 | warn |
| A-06 | 차트 장표에 unit_line이 있다 | fail |
| A-07 | 모든 data_ref가 존재하고 출처가 있다. derived 값에는 입력값이 적혀 있다 | fail |
| L3 | placeholder가 있으면 스티커가 붙어 있다 | fail |
| status | filled 장표에 placeholder가 없다 | fail |
| D8 | 제목이 마침표로 끝난다 | warn |
| ids | 같은 목록 안에서 id가 겹친다 | fail |
| **B-05** | 사이드바·콜아웃의 숫자가 본문에 이미 있다(같은 정보 반복) | fail |
| **B-06** | 사이드바·콜아웃의 숫자가 본문 값에서 계산된 것이 아니다(다른 주제를 끼워 넣음) | warn |
| **B-05** | 사이드바·콜아웃 숫자가 본문 값의 단순 합·차·나머지 / key_takeaways가 Exec Summary와 겹침 | warn |
| **B-08** | `calc` 재계산 값 불일치, estimate인데 `calc`·`assumptions` 없음, 추정치를 근거(`basis`, `equation`, 행 `basis`) 없이 보여줌 | fail |
| **B-08** | 추정처럼 보이는 계산값에 `estimate` 표시 없음, derived인데 `calc` 없음 | warn |
| **B-10** | 레버 숫자에 열 제목(`headers`) 없음, 단위가 섞였는데 `metric` 없음 | fail |
| units | 숫자 뒤 "points" (→ 문장은 percentage points, 라벨은 pp) | fail |
| units | 문장 속 "pp", "Nx", "vs." | warn |
| A-12 | 글자 수(본문 450자, 차트·도식 300자 미만 / 1,300자 초과), 박스 불렛 3개 미만, KPI drivers 없음, 한 결론 장치가 40% 초과 또는 3장 연속 | warn |
| A-12 | callout target이 장표 요소와 맞지 않음 | fail |
| status | ghost 본문에 data_ref가 있다 | fail |

**LLM 판정으로 넘기는 원칙** (구조만으로는 검사할 수 없는 것):
- B-01: 제목만 읽어도 이해되는가
- B-02: 영역마다 두괄식인가
- B-03: 한 장에 한 주제인가
- B-05: 사이드바 불렛·캡션·하단 결론이 본문을 다시 읽어 주기만 하는가
- B-06: 사이드바만 읽었을 때 왼쪽 차트의 무엇을 설명하는지 바로 알 수 있는가
- B-07: 제목에서 숫자를 빼도 판단(기회, 위험, 해야 할 일)이 남는가
- B-09: 화살표가 원인→결과, 차트→해석, 단계→결과에만 쓰였는가
- B-11: 불렛 하나만 떼어 읽어도 주어·지표·비교 대상이 보이는가
- G-01: 제목만 이어 읽어도 이야기가 되는가
- G-03: MECE인가

이 판정은 렌더 직전에 실행하고, 결과는 `qa.results`에 기록한다.

## 5. 아직 정하지 않은 것
- 렌더러의 좌표 토큰은 spec 밖에 둔다. spec은 내용만 담는다. 예외로 `meta.theme`(8종, 기본 `navy`)과 `meta.font_pair`(테마 기본값을 바꿀 때만)는 spec에 적는다. 값은 `templates/themes.json`에 있다.
- Tier 2 Archetype의 body: 지금은 같은 kind를 재사용한다. map과 org-chart는 v1.x에서 kind를 추가한다.
- 2차 태깅 결과에 따라 Archetype 목록이 바뀌면 enum을 업데이트한다.
