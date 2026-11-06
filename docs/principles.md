# Slide Principles

생성기와 QA가 따르는 **최상위 원칙**이다. Archetype 카탈로그(`docs/archetypes/`)의 세부 규칙보다 우선한다.
원칙끼리 충돌하면 **B(Brian) > A(분석 근거) > G(일반 관행)** 순으로 따른다.

| 출처 표시 | 뜻 |
|---|---|
| **B** | **Brian 작성.** 전 맥킨지 컨설턴트로서 실제로 지킨 원칙. 원문을 그대로 보존한다 |
| **A** | **Claude 추가: 분석 근거.** 공개 맥킨지 덱 203개, 3,257페이지 태깅(최신성·게시처 가중)에서 반복 확인된 것. 근거 수치를 함께 적는다 |
| **G** | **Claude 추가: 일반 관행.** 컨설팅 업계에 널리 알려진 관행(Minto, Zelazny 등). 우리 데이터로는 아직 검증하지 않았다 |

각 원칙에는 생성기가 **어떻게 검사하는지**(QA 체크)를 붙인다. 검사할 수 없는 원칙은 생성 프롬프트로만 반영한다.

## Brian에게서 새 원칙을 받았을 때
1. 원문을 그대로 B 섹션 맨 아래에 추가한다. 번호는 B-01, B-02… 순서로 붙이고, 받은 날짜를 적는다.
2. 영어 버전(SKILL.md에 들어갈 문장)과 QA 체크를 함께 적는다.
3. 기존 A/G 원칙과 겹치면, 그 A/G 원칙에 `→ B-xx로 대체` 표시를 하고 B를 기준으로 삼는다.

---

## B. Brian's principles

### B-01 · 리드 메시지만 읽어도 한 장이 이해돼야 한다 (2026-11-05)
> 한 장의 내용은 리드 메시지만 읽어도 이해가 돼야한다.

- **공개 근거:** 2019년 공개된 맥킨지 교육용 덱(2차 태깅 r2-074)이 "결론 없는 장표 금지"를 명시한다.
- **EN:** A reader who reads only the action title must get the slide's full point. The body proves the title; it does not complete it.
- **QA:** 제목이 완결된 판단 문장인가(주어, 서술어, so-what). 본문에만 있고 제목에는 없는 핵심 결론이 있는가.
  LLM 판정: "본문을 가리고 제목만 보여줬을 때 이 장표의 결론을 말할 수 있는가?"

### B-02 · 시선 흐름(위→아래, 좌→우)과 영역별 두괄식 (2026-11-05)
> 사람들은 보통 위->아래, 좌->우로 장표를 읽을 때 시선이 가므로, 이 순서를 고려하고 각 영역에서도 두괄식으로 해당 영역의 핵심 내용을 먼저 알리고 그 안에 그에 대한 부연 설명이 들어가는 구조여야한다.

- **EN:** Lay the slide out in reading order: top to bottom, left to right. Each region (panel, column, box) leads with its own takeaway, then gives the supporting detail.
- **QA:**
  - 패널·열·박스마다 헤더가 있고, 그 헤더가 라벨이 아니라 그 영역의 결론 문장인가.
  - 논리 순서(원인→결과, 현재→미래, 문제→해결)가 왼쪽→오른쪽, 위→아래로 배치됐는가.
  - takeaway 사이드바는 차트의 오른쪽에 있는가(근거 → 결론 순서).

### B-03 · 한 장에 한 주제 (2026-11-05)
> 한 장에 여러 주제의 내용을 넣는 거는 지양해야한다. (관련 데이터/리서치를 깊게 가는 것은 상관없으나, 여러 내용이 혼합되는 거는 읽는 이에게 혼란을 줄 수 있다.)

- **공개 근거:** 같은 교육용 덱이 "장표당 아이디어 하나"를 명시한다.
- **EN:** One slide, one topic. Going deep on one point with several pieces of evidence is fine. Mixing different points on one slide is not.
- **QA:**
  - 본문의 모든 요소(차트, 박스, 콜아웃)가 같은 리드 메시지를 뒷받침하는가.
  - 리드 메시지와 연결되지 않는 요소가 있으면 → 장표를 나눈다.
  - `multi-chart-panel`의 패널들은 같은 주장의 근거여야 한다. 서로 다른 주장을 나란히 놓으면 안 된다.
- **보강 (2026-11-06):**
  > 0.7 points가 어디서 나온건지 읽는 사람 입장에서는 알 수가 없어. 이 계산식을 여기에 추가를 하거나, 여기에 넣기가 어렵다면 아예 다음 장으로 넘겨서 산식의 근거를 함께 표기를 해야해. 내가 앞서 얘기한 원칙들 있지. (장표에 내용 여러개 X, 주제 넘어가면 차라리 다음장에)
  - **EN:** If a number needs its own explanation (how it was calculated, what it assumes), it is a new topic: move it to the next slide with its formula rather than squeezing it into this one.

### B-04 · Exec Summary만 읽어도 덱 전체가 이해돼야 한다 (2026-11-05)
> 익썸은 각 장표의 리드 메시지를 보여준다. 그러므로 익썸만 읽어도 전체 장표의 내용이 이해가 가능해야한다.

- **EN:** The executive summary is the deck's action titles in order. Reading it alone must tell the whole story.
- **QA:**
  - Exec Summary의 각 불렛 ↔ 본문 섹션·장표 리드 메시지가 1:1로 대응하는가(spec의 `id`로 검사).
  - 본문에는 있지만 Exec Summary에 대응하는 불렛이 없는 핵심 장표가 있는가.
  - 반대로 Exec Summary 불렛인데 근거 장표가 없는가.

### B-05 · 한 장 안에서 같은 정보를 두 번 보여주지 않는다 (2026-11-05)
> 정보를 채운건 좋은데 좌측의 그래프와 동일한 내용이잖아. 이거는 worst야. 다른 인사이트나 차라리 데이터포인트를 넣어야하고 이 원칙은 모든 장표에 적용돼야해

- **EN:** Never show the same information twice on a slide. A sidebar, callout, row or bottom line must add a new insight or a new data point; restating what the chart or table already shows wastes the space and reads as padding. Applies to every slide.
- **QA:**
  - 사이드바(큰 숫자, 값 행), 콜아웃, 이유의 숫자 data_ref가 본문 차트·표·박스에 이미 있으면 fail.
  - 사이드바 불렛·캡션·하단 결론이 본문을 말로 다시 읽어 주기만 하는가(LLM 판정): "본문을 가리면 이 문장이 새로운 사실을 알려 주는가?"
  - 예외: A-01에 따라 제목의 숫자는 본문이나 사이드바 중 한 곳에 보여야 한다(두 곳 모두가 아니라).
- **보강 (2026-11-06):**
  > 36% would not buy more은 64%에서 그냥 빼면 되는거 같은데, 굳이 필요한지가 잘 모르겠다. 차라리 빼는게 나을거 같아.
  >
  > 박스 하단에 저 값은 단순 덧셈, 뺄셈으로 보여서. 먼가 예상 기대효과, 전문가 quote라던지 차라리 그런거를 넣는게 좋아보여
  >
  > 참고로 ExeSum과 Key Takeaway가 너무 유사하다면, Next Step만 넣는것도 방법이야. 중복은 지양해야해.
  - **EN:** A plain sum, difference or remainder of numbers the exhibit already shows (100% − 64%, 31% − 26%) is the same information again. Use the space for expected impact (with its basis), a driver, or a quote. At deck level, the end page does not repeat the executive summary: it shows next steps only, unless the takeaways say something new.
  - **QA:** 사이드바·콜아웃 숫자가 본문 값의 단순 합·차·나머지(곱셈·나눗셈 없음)면 warn. `key_takeaways`가 Exec Summary와 단어 절반 이상 겹치면 warn. 렌더러는 `key_takeaways`가 없으면 마지막 장에 Next steps만 그린다.

### B-06 · 여백을 채우려고 관련 없는 정보를 넣지 않는다 (2026-11-05)
> 새로운 정보를 넣은 건 좋은데, 이건 오히려 새로운 장표의 그래프 스러운 내용들이라 저기 좁은 공간에 들어간 내용만으로는 왜 있는지 모르겠어. 앞에서 내가 말한대로 여러가지가 들어가면 안된다 라는 원칙에 위반된건 아닌지 확인하고, 그리고 이건 한번에 읽었을 떄 알아볼 수 있다 라는 원칙은 정면으로 위반한거야. 여백을 채우려는 노력은 알겠으나 이런 접근은 절대 지양.
>
> 정보가 들어가는 건 좋은데, 이게 너무 좌측과 연관성이 떨어지면 뭔지 알아볼 수가 없어. 억지로 정보를 추가하려 하지마.

- **EN:** Never add information just to fill space. Everything beside the exhibit must explain that exhibit: why the pattern happens, what drives each highlighted element, what it means for the decision. A number that belongs on another slide's chart breaks B-03 (one topic) and B-01 (readable at a glance).
- **생성 규칙:** 사이드바는 왼쪽 차트의 해석이다. 굵은 머리말이 붙은 불렛 3~4개로 차트의 막대·구간·선을 하나씩 짚는다. 숫자를 넣는다면 차트 값에서 계산한 것만 넣되, 단순 합·차는 넣지 않는다(B-05). 비중, 기대 효과처럼 차트만 봐서는 바로 알 수 없는 값을 넣는다. 여백은 해석 불렛의 크기와 간격으로 메우고, 관련 없는 지표로 채우지 않는다.
- **QA:**
  - 사이드바·콜아웃 숫자가 본문 값에서 계산된 것(`derived_from`이 본문 data_ref를 포함)이 아니면 warn.
  - LLM 판정: "사이드바만 읽었을 때, 왼쪽 차트의 무엇을 설명하는지 바로 알 수 있는가?"


### B-07 · 리드 메시지는 표를 읽어 주지 않고 시사점을 말한다 (2026-11-06)
> 내용 좋은데, 리드 메시지가 단순히 아래의 두 표를 읽기만 하고 끝이야. 마진도 좋고 성장 속도도 빨라서 적용 시 기회영역이 크다 아님 빠르게 적용해야한다. 이런 내용까지 있어야해 리드 메시지에는. 단순히 표 읊는 거는 지양. 그건 독자들이 표 읽으면서 가능해. 이건 전체적으로 한 번 더 훑어봐야할거 같고, 필요시 전체 규칙에도 추가할 법하다.
>
> 이런 식의 리드 메시지 좋아. 우리의 가장 큰 기회 영역이다 이런 결론이 드러나잖아.

- **EN:** The action title states what the evidence means for the decision ("so it is our biggest opportunity", "so we should start now"), not only what the exhibit shows. Reading numbers off the chart is the reader's job; the title gives the implication.
- **QA (LLM):** 제목에서 숫자를 빼고 남는 말이 판단(기회, 위험, 해야 할 일)인가? 차트 값을 나열하고 끝나면 다시 쓴다. 덱 전체 제목을 한 번 더 훑는다.

### B-08 · 추정치는 근거를 장표와 엑셀에 함께 보여준다 (2026-11-06)
> 이런 그래프 아주 좋은데, 왜 연마다 1.5pp가 증가하는지에 대한 근거가 보이지는 않아. 그거가 함께 보여줘야해.
> 아래거는 규칙에 추가하자.
> 이렇게 Estimate되는 거라면
> 1) 소스가 있는 거라면 소스를 명확히 표기
> 2) 우리가 추정을 해서 한거라면 우리의 계산식도 장표에 함께 넣어야해
>
> 엑셀에도 단순히 더하기만 한거로 보이는데, 이런거는 엑셀에는 정말 Assumption까지 상세히 해서 표기하고, 그 계산이 이해가 되도록 PPT에도 표기를 해야해

- **EN:** Every estimate shows its basis. (1) If an input comes from a source, name the source on the slide. (2) If we estimated it, the formula is on the slide (number cards joined by operators, or a basis line under a sidebar row), and the source workbook has a Calculations sheet with every assumption written out and a live Excel formula, not a pasted value.
- **spec:** data point에 `estimate: true`, `calc`(data point id로 쓴 수식), `assumptions[]`. 장표에는 `basis`(숫자 카드 줄), `equation` 본문, 또는 사이드바 행의 `basis`.
- **QA:** `calc`를 다시 계산해 값과 다르면 fail. estimate인데 `calc`나 `assumptions`가 없으면 fail. 추정치가 보이는 장표에 근거가 없으면 fail. 추정처럼 보이는 계산값(project, uplift 등)에 표시가 없으면 warn.

### B-09 · 화살표는 인과·해석·결과에만 쓴다 (2026-11-06)
> 두 그래프가 원인 / 결과가 아닌데 중간에 화살표는 부적절해. 원인/결과나 그래프/해석 이런 곳에는 화살표가 맞지만 그게 아니면 화살표가 들어갈 이유는 없어
>
> 여기도 Situation / Approach 여기 사이에는 화살표가 굳이 필요한지 잘 모르겠어. Impact 앞에는 make sense.

- **EN:** Use an arrow only from cause to effect, from exhibit to interpretation, or from steps to their result. Parallel evidence (two panels proving one claim, situation next to approach) gets no arrow.
- **렌더러:** 패널 사이 화살표는 기본으로 그리지 않는다(`connector: "arrow"`일 때만). case-example은 Impact 앞에만. 차트 → takeaway 사이드바의 화살표는 유지(차트 → 해석).

### B-10 · 표의 모든 열과 숫자는 무엇인지 적는다 (2026-11-06)
> 이 표 좋은데, 표 위에 각각이 뭔지가 안 나왔잖아. 레버 / 임팩트 이런 식으로 달거나, 적절한 제목을 달고. 특히 우측의 % 값이랑 pp값은 정말 뭐를 말하는 건지 모르곘어. 이런 수치가 들어갈 때는 뭘 의미하는지가 당연히 이해돼야지.
> 밑에 ~$40M each가 뭘 뜻하는건지 이해가 안가. 저 위해 4개 레버 각각에 $40M? 앞에 장표를 보면 그건 아닐테고, 명확하게 표현을 해줘야해

- **EN:** Every column has a header and every number says what it measures ("of shoppers say it is hard to find"). A number in a sentence names its subject: not "~$40M each" but "each of the two peers invested about $40M".
- **QA:** 레버 숫자가 있는데 열 제목(`headers`)이 없으면 fail. 단위가 서로 다른데 `metric`이 없으면 fail. "each" 같은 대명사가 무엇을 가리키는지는 LLM 판정.

### B-11 · 불렛 하나만 읽어도 이해돼야 한다 (2026-11-06)
> 좋은데 서브 불렛에서 내용이 얘만 읽었을 때는 잘 이해가 안 돼. 마찬가지로 아래의 것들도 그렇고. 너무 simplify한 느낌이 있다.
>
> 문장이 좀 잘 안 읽혀. better quality and visibility가 아니라 improvement in quality and visibility 이런게 더 make sense할거 같은데, 이런 문장 관련 내용은 기존 맥킨지 장표들이나, 일부 맥킨지 웹사이트에서의 문장 스타일을 참고하는 것도 좋을 듯.

- **EN:** Each bullet reads on its own: who or what, the metric, the value with its period, and what it is compared with, in one sentence ("Private label makes up 18% of our sales, against a US grocery average of 26%"), not a clipped fragment ("18% vs. 26%"). Lists use parallel grammar. Phrasing follows `style.md` (units, comparisons, verbs).
- **QA (LLM):** 불렛 하나만 떼어 읽어도 주어·지표·비교 대상이 보이는가. 단위 표기(`percentage points`, `N times`, `compared with`)는 check.py가 검사한다.


### B-12 · 전체 덱에는 빈칸("?")을 남기지 않는다 (2026-11-06)
> 질문에서 Full Deck 만든다할 때에는 중간에 정보가 비어있는거는 지양시키자.

- **EN:** In a full deck (`deck_detailed`), a "?" is the last resort. For each missing number, ask the user as multiple choice with a recommended value and its basis first (a benchmark, a peer, or a calculation from sourced inputs, shown as an estimate under B-08), then upload/paste, then a wider web search. A target only the user can set (a pilot KPI, a price) is still a question with 2–3 concrete values to pick from.
- **QA:** `deck_detailed`인데 "?"가 남아 있으면 warn. 흐름 덱(`deck_flow`)에서는 "?"가 목적이므로 검사하지 않는다.

### 질문 방식 (2026-11-06, SKILL.md 운영 규칙)
> 그거를 내가 타이핑으로 답변하는게 별로야. 앞에서처럼 너가 객관식처럼 옵션들을 주고(물론 내가 기입도 가능), 그렇게 해야 이탈이 덜 될 듯.
>
> 맨 첫 질문들: 내가 조사한게 있는지를 묻는게 없었던 듯. 그리고 스타일/Theme 고르는 질문도 안 보였어.

- 모든 질문(체크포인트, 중간 가정 확인, 빠진 숫자)은 객관식. 추천안을 맨 앞에 두고 이유를 몇 단어로 붙인다. 직접 입력도 가능. 첫 질문에서 만들 것·자료 여부·청중·테마를 한 번에 묻는다.

---

## A. Claude 추가: 공개 덱 분석 근거

### A-01 · 제목 속 숫자는 본문에 다시 보여야 한다
- 근거: 5개 묶음 모두에서 확인됐다. 숫자가 든 제목은 합계 막대, 강조 막대, 콜아웃, 합계 행 중 하나에서 같은 숫자를 보여줬다.
- **QA:** 제목의 수치를 추출해 차트 데이터나 라벨에 같은 값(반올림·`~` 허용)이 있는지 기계적으로 검사한다.

### A-02 · 제목이 지목한 것만 강조한다
- 근거: 3개 묶음 이상. 강조색은 제목에 나온 항목에만 쓰고, 나머지는 중립색이다.
- B-01, B-02와 연결된다. 눈이 가장 먼저 가는 곳이 제목이 말한 바로 그곳이어야 한다.
- **QA:** 강조색 요소의 라벨이 제목에 등장하는가. 제목에 등장하는 항목이 강조돼 있는가.

### A-03 · 제목은 2줄 권장, 3줄은 경고
- 근거(v0.2): so-what 제목의 88%가 2줄 이하이고, 단어 수 중앙값은 14, 90%가 20단어 이하다.
  2022년 이후는 중앙값 15단어, 2줄 이하 84%로 조금 길어졌다.
- **QA:** 2줄 이하이면서 21단어 이하면 pass. 3줄이거나 22~25단어면 warn(장표는 만들고 QA에 표시). 25단어 초과면 fail(skill이 제목을 다시 쓴다).
- **상태:** v0.1의 "2줄 이내, 3줄이면 fail"을 완화한 안. Brian 승인 (2026-11-05).

### A-04 · 개수 단어 = 시각 요소 수
- 근거: "Three factors"면 3열, "five levers"면 5행이었다.
- **QA:** 제목의 수량사와 본문 요소 수가 일치하는가.

### A-05 · 제목에 절이 두 개면 장표도 둘로 나눈다
- 근거: 두 절로 된 제목은 2패널로 분할돼 있었다.
- B-03과의 경계: 같은 주제의 두 측면은 2패널 한 장으로, 서로 다른 주제는 두 장으로 만든다.
- **QA:** 제목이 "X, while Y" 구조면 레이아웃이 `split-2` 또는 2패널인가.

### A-06 · 차트 장표에는 단위 줄이 있다
- 근거: 단위 줄이 제목 바로 아래에 있었다(본문 38% 가중, 차트 장표는 대부분).
- **QA:** 차트가 있는 장표에 "지표, 단위, 기간" 줄이 있는가.

### A-07 · 숫자에는 출처가 있다 (D5)
- 근거: 출처 줄이 본문 64%(가중)에 있었다. 우리는 이를 **데이터 장표 100%**로 강화한다.
- 출처가 없는 수치는 placeholder로 두고, `ILLUSTRATIVE` 스티커와 점선 `?` 표현을 쓴다.
- **QA:** 장표의 모든 수치가 소스 엑셀의 행과 연결되는가.

### A-08 · Exec Summary 번호 = 섹션 번호, 마지막에 요약 반복
- 근거: 3개 묶음. B-04를 덱 구조로 구현하는 방법이다.
- **QA:** spec 단계에서 Exec Summary 불렛 id → 섹션 id 매핑을 강제한다. tracker는 자동 생성한다(사람이 만든 tracker 오류도 관찰됐다).

### A-09 · 장 사이는 연결어로 잇는다
- 근거: 3개 묶음. "However / In addition / As a result"로 다음 장을 열었다.
- **QA:** 제목만 순서대로 이어 읽었을 때 이야기가 되는가(G-01 수평 논리 테스트).

### A-10 · 같은 그림을 다시 쓰면서 강조만 바꾼다 (v0.2 신규)
- 근거: 2차 5개 묶음 이상에서 관찰됐다.
  - 같은 차트나 프레임워크를 다음 장에서 그대로 쓰고 강조만 옮겨 두 번째 메시지를 전달한다.
  - 프레임워크를 한 부분씩 채워 나간 뒤 종합 장표로 닫는다.
- 생성 규칙: 병렬 섹션은 같은 Archetype과 같은 레이아웃을 재사용하고, `highlights`만 바꾼다(S5와 연결).
- **QA:** 같은 section의 연속 장표가 Archetype을 바꿀 때, 그 이유가 `rationale`에 있는가(warn).

### A-11 · 차트 장표는 takeaway 사이드바가 기본 (v0.2 신규)
- 근거: 차트 + 사이드바가 2010년대 약 10%에서 **2022년 이후 21%**로 늘었다.
- 생성 규칙: 정량 차트 장표의 기본 layout을 `takeaway_sidebar`로 둔다. 차트가 넓어야 할 때만 `full`을 쓴다.

### A-12 · 장표는 본문 영역을 채운다 (v2 밀도, 2026-11-05 Brian 확정)
- 근거: 2020년 이후 공개 덱 28개, 본문 장표 577장을 측정했다(덱별 중앙값의 중앙값).
  - 본문 서체는 장표 높이의 2.6%(≈14pt), 제목은 4.6%(≈25pt)
  - 좌우 여백은 폭의 4.5%(≈0.6in), 콘텐츠는 높이의 91%까지 내려온다
  - 장표당 글자 수는 약 800자(중간 50%: 670~1,110자)
- 생성 규칙:
  - 본문 장표는 600~1,100자를 목표로 한다. 흐름만 짜는 장표(ghost)도 실제 장표 모양(항목 이름, 축, "?" 값)과 증명할 결론을 보여준다.
  - 결론 장치는 여러 선택지 중 장표마다 고른다(2026-11-05 Brian 결정). 제목이 곧 결론이므로(B-01) 장치가 없어도 된다.
    공개 덱 2020년 이후 본문 1,382장 기준 빈도: 없음 약 72%, 결론 사이드바 17%, 콜아웃 7%, 하단 결론 띠 4%.
    | 장치 | 쓰는 곳 |
    |---|---|
    | 없음 (본문이 공간을 채움) | 기본 |
    | 결론 사이드바 | 차트 장표 |
    | 콜아웃(`callout`) | 결론이 가리키는 요소가 하나일 때. 그 요소 옆에 붙인다 |
    | 진한 띠(`so_what`, `so_what_style: bar`) | 종합 장표, 강하게 못 박을 때 |
    | 가벼운 줄(`so_what_style: line`) | 섹션을 닫는 장표 |
  - 박스·열·단계마다 불렛 3~5개. KPI 타일마다 드라이버 2~4줄(값이 없으면 무엇이 빠졌는지).
  - 요소는 본문 영역 높이에 맞춰 늘린다(렌더러 책임).
- **QA:**
  - 글자 수 450자 미만이면 warn(얇음), 1,300자 초과면 warn(빽빽함). statement 장표와 ghost 장표는 제외한다.
  - 한 장치(사이드바·콜아웃·띠·줄)가 본문 장표의 40%를 넘거나 세 장 연속이면 warn(A-10과 같은 이유: 반복은 지루하다).
  - 콜아웃의 target이 장표의 어떤 요소와도 맞지 않으면 fail.
  - 차트 하나에 결론 한 줄뿐인 장표(사이드바·패널 없음, 450자 미만)는 warn. 차트 장표는 사이드바에 불렛과 값 행(`rows`)을 넣는다.
  - 사이드바 글이 160자 미만이고 값 행도 없으면 warn(아래가 빈다).
  - 콜아웃을 쓴 표는 모든 행에 `note`(평가 한 줄)를 넣어 오른쪽 평가 열을 채운다. 빠지면 warn.
  - 마무리 장표에는 `storyline.next_steps`를 넣는다(Key takeaways + Next steps). 빠지면 warn.
- 하단 결론 문장에 "So what" 같은 라벨을 붙이지 않는다. 근거: 공개 덱 94개의 PDF 본문에 "So what", "Bottom line" 라벨이 한 번도 없다.
  실제로 쓰는 라벨은 "Key takeaways", "Key messages", "Implications"(7개 덱)뿐이다. 하단 결론은 왼쪽 강조색 세로선 + 굵은 문장으로 쓴다.
- 피드백 반영 원칙(Brian, 2026-11-05): 한 덱에서 찾은 개선점은 렌더러·검사 규칙·모든 예시 덱에 함께 반영한다.
  - 열·프레임워크·프로세스 항목의 불렛이 3개 미만이면 warn. KPI 항목에 `drivers`가 없으면 warn.

---

## G. Claude 추가: 일반 관행 (미검증)

### G-01 · 수평 논리 (Horizontal logic)
- 덱의 제목만 순서대로 읽어도 하나의 이야기가 돼야 한다. B-04를 장표 단위로 확장한 것이다.
- 공개 근거: 2019년 맥킨지 교육용 덱(r2-074)이 "제목만 이어 읽어도 하나의 스토리가 돼야 한다"를 명시한다. → A급 근거로 올릴 후보.
- **QA:** 전체 제목 목록을 LLM에게 주고 "논리 비약이 있는 곳"을 찾게 한다.

### G-02 · 수직 논리 (Vertical logic)
- 본문의 모든 요소는 제목을 증명하는 데 쓰여야 한다. 증명에 기여하지 않는 요소는 뺀다. B-03의 반대 방향 검사다.

### G-03 · MECE
- 프레임워크, 이슈 트리, 레버 목록의 항목은 서로 겹치지 않고 빠짐없어야 한다.
- **QA:** `framework-pillars`, `issue-tree`, `numbered-levers`에 LLM으로 겹침과 누락을 검사한다.

### G-04 · 피라미드 구조 (Minto)
- 결론 → 근거 → 데이터 순서. Exec Summary(결론) → 장표 제목(근거) → 본문(데이터)이 하나의 피라미드를 이룬다.

### G-05 · 차트 하나에 메시지 하나 (Zelazny)
- 차트 유형은 메시지(비교 유형)가 결정한다. 데이터 모양이 결정하는 게 아니다. 라우팅 표의 근거가 이것이다.
