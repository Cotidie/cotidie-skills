---
name: summary-paper
description: Use when the user hands over a research paper (local PDF path, arXiv URL or ID) and wants it read, summarized, digested or judged. Triggers include "이 논문 요약해줘", "논문 정리", "논문 읽어줘", "핵심만", "기여가 뭐야", "읽을 가치 있어?", "PACES", "paper summary", "summarize this paper", "what does this paper claim", "is this paper worth reading", and any pasted arXiv link with a request to summarize it. Use it even when the user only says "이거 뭐야" about a paper PDF. Not for textbook chapters (textbook-notes), a concept with no specific paper (explain-concept), or a request to explain a paper in the chat, walk through its math, critique it, or find a follow-up idea (paper-forge, when installed).
trigger: /summary-paper
---

# /summary-paper

Jason Corso의 PACES(Problem, Approach, Claim, Evaluation, Substantiation)로 논문 한 편을
읽고, 시각화가 붙은 요약 한 편을 만든다. 목표는 둘이다. 이 논문을 더 읽을지 10초 안에
판단하게 하고, 한 달 뒤에도 기여와 근거를 떠올리게 한다. 방법론 원문 요약과 Corso의
예시는 `references/paces.md`. 시각화 규칙과 골격은 `references/visual-style.md`.
둘 다 작업 시작 전에 읽는다.

## 사용법

```
/summary-paper <paper.pdf | arXiv URL | arXiv ID>     # 형식은 시작할 때 묻는다
/summary-paper <...> --md                              # 묻지 않고 Markdown
/summary-paper <...> --html                            # 묻지 않고 HTML (summary.md도 남는다)
/summary-paper <...> --en                              # 본문 영어 (기본: 한국어 본문 + 영어 용어)
```

## 산출물

```
<실행 위치>/<paper-slug>/
  summary.md        # 항상. 원본
  summary.html      # HTML을 골랐을 때. 자립형 한 파일 (SVG 인라인, PNG base64)
  paces.json        # 카드 입력. 다섯 답의 한 줄 버전
  results.json      # 차트 입력. 표 하나에서 뽑은 수치
  paper.pdf         # arXiv에서 받았을 때만
  figures/          # paces-card.svg, method.svg, results.svg, fig-N.png, cover.png
```

`<paper-slug>`는 제목의 핵심 단어 2~5개, 영어 소문자 kebab-case: `vit-16x16-words`,
`llava-visual-instruction-tuning`. 실행 위치가 곧 저장 위치다. 다른 곳에 저장하려면
사용자가 그곳에서 실행한다.

`<S>`는 이 스킬의 `scripts/` 폴더. 처음 한 번: `python3 -m pip install markdown pymupdf matplotlib`.
SVG 미리보기는 rsvg-convert나 inkscape가 있으면 정확하고, 없으면 MuPDF로 근사한다.

## 절차

### 0. 형식 확인 (한 번, 논문을 열기 전에)

형식 규칙 하나: 요청에 형식이 있으면(`--md`, `--html`, "HTML로", "마크다운으로") 그대로 따르고,
없으면 Markdown인지 HTML인지 AskUserQuestion으로 묻고, 물을 수 없는 런타임(서브에이전트, 배치,
크론)이면 Markdown이다. 논문을 읽은 뒤에 물으면 답을 기다리는 동안 컨텍스트가 식으므로 읽기 전에 묻는다.

언어는 묻지 않는다. 한국어 본문에 기술 용어는 영어 원어. `--en`이면 영어.

### 1. 준비

1. 입력 해석. 로컬 PDF면 그대로 쓴다. arXiv URL이나 ID면
   `curl -L https://arxiv.org/pdf/<id> -o <slug>/paper.pdf`.
2. `<slug>/figures/` 생성. 작업용 임시 폴더는 `T=$(mktemp -d)`. 같은 머신에서 여러 요약이
   동시에 돌 수 있으므로 `/tmp/x.png` 같은 고정 이름은 쓰지 않는다. 결과 폴더에 임시 파일을 두지 않는다.
3. 섹션 지도: `python3 <S>/paperviz.py toc <pdf>`가 쪽별 제목 후보(섹션, TABLE N)를 찍는다.
   본문 텍스트는 `pdftotext -f N -l M <pdf> - 2>/dev/null`로 쪽 범위씩 뽑는다. `-layout`은 표가 있는
   쪽에서 공백 패딩으로 수십 KB가 되므로 쓰지 않는다.

### 2. 읽기

Corso의 순서. Method만 skim에서 정독으로 올린다.

| 순서 | 구간 | 깊이 | 여기서 채우는 것 |
|---|---|---|---|
| 1 | Abstract, Introduction | 정독 | Problem, Claim 초안. 기여 목록 문단은 Claim 하나로 압축 |
| 2 | Experiments, Discussion, Limitations, Conclusion | 정독 | Evaluation, Substantiation. 차트에 쓸 표 하나 고르기 |
| 3 | Method | 정독 | Approach 확정. 다이어그램의 입력→구성요소→출력과 새로 더한 부분 |
| 4 | Related Work | skim | Problem을 분야 안에 놓는 문장 하나 |

Corso가 Method를 skim하는 이유는 사람의 시간이다. LLM에게 열 쪽은 비용이 아니고, 다이어그램은
skim으로 그리면 틀린다. 많이 읽고 짧게 쓴다. 길이 상한은 그대로다.

읽으면서 작업 표를 채운다(채팅 또는 `$T/notes.md`): 항목 | 답 초안 | 근거 페이지. 근거 페이지는
summary.md 마지막 표에 들어간다. 텍스트는 `pdftotext -f N -l M`, 그림이 있는 쪽만
`paperviz.py preview <pdf> --page N -o $T/pN.png`로 렌더해 Read로 본다.

### 3. PACES 쓰기

형태는 "리드 문장 하나 + 불릿"이다. 긴 산문 한 덩어리는 읽는 사람이 다시 쪼개야 한다. 불릿 앞의 굵은
라벨은 명사구(데이터셋·베이스라인, Red flag, 나라면). 단위 하나는 문장 하나 또는 불릿 하나.

| 항목 | 형태 | 단위 상한 | 글자(공백 제외) | 반드시 담는 것 | 함정 |
|---|---|---|---|---|---|
| Problem | 산문 1~2문장 | 2 | 250 | 분야 안에서의 위치. "object detection"이 아니라 "무엇을 위한 object detection" | 논문 첫 문장 옮기기 |
| Approach | 리드 1 + 불릿 ≤3 | 4 | 450 | 핵심 메커니즘. 불릿은 구성요소, 마지막 불릿이 새로 더한 부분 | 수식, 하이퍼파라미터 나열 |
| Claim | 산문 1문장 | 1 | 200 | 저자가 가장 자랑하는 기여 하나. 분야 맥락 안에서 | 기여 목록 셋을 그대로 옮기기 |
| Evaluation | 리드 1 + 불릿 3~5 | 6 | 750 | 데이터셋·베이스라인, 설정, red flag, "나라면" | 표 숫자 나열, 한 불릿에 두 문장 |
| Substantiation | Verdict 줄 + 1문장 + 불릿 ≤2 | 3 | 300 | 평가가 Claim을 어디까지 받치는지. 불릿은 받치는 것과 못 받치는 것 | 결론 문단 요약 |

문장 하나는 140자(공백 제외)를 넘지 않는다. 불릿 하나에 문장 하나. `check_summary.py`가 단위 수,
글자 수, 문장 길이, 불릿당 문장 수를 모두 잡는다. 카드용 한 줄 답을 먼저 쓰고 본문은 그것을 불릿으로
펼친 것이면 상한 안에 든다. 캡션과 그림 줄은 세지 않는다.

- 자기 말로 쓴다. 원문 인용 금지. `check_summary.py`가 8단어 이상 연속 일치를 FAIL로 잡는다.
- 이론 논문이면 Evaluation에 "실험 평가 없음, 증명으로 대신함"을 쓰고 Substantiation은 증명이
  Claim을 받치는지로 판단한다.
- 숫자는 판단에 필요한 것만 본문에. 나머지는 차트가 맡는다. 논문에 없는 숫자(직접 계산한 평균, 기준선
  F1)를 쓰면 "이 값은 계산한 것" 표시를 붙인다.
- Verdict가 Partial이나 No면 그 이유가 Substantiation 문장이다.

### 4. 시각화

규칙과 JSON 형식은 `references/visual-style.md`. 여기서는 조건과 명령만.

| 그림 | 조건 | 만드는 법 |
|---|---|---|
| PACES 카드 | 항상 | `paces.json` 작성 → `python3 <S>/paperviz.py card paces.json -o figures/paces-card.svg` |
| 방법 다이어그램 | 항상 | SVG를 직접 써서 `figures/method.svg`. 노드 7개 이하, 새 구성요소 하나만 accent |
| 결과 차트 | 실험 논문이면 항상 | 표 하나의 원시 열만 골라(평균 내지 않는다) `results.json` → `python3 <S>/paperviz.py chart results.json -o figures/results.svg` |
| 원문 크롭 | 다시 그리면 정보가 사라지는 그림(정성 결과, attention map, 로봇 사진)일 때, 최대 2장 | `paperviz.py preview --page N` 격자로 bbox 읽기 → `crop` → Read로 확인 |
| 생성형 커버 | codex-image 스킬과 `codex` CLI가 있을 때만 | 읽기가 끝난 직후 백그라운드로 먼저 띄운다(1~3분 걸린다): codex-image 스킬의 `codex-image.sh "<prompt>" figures/cover.png &`. 글자 없는 추상 일러스트. 없으면 조용히 생략 |

모든 SVG는 `python3 <S>/paperviz.py preview figures/x.svg -o $T/x.png`로 렌더한 뒤 Read로
확인한다. 안 보고 넘기지 않는다. 글자가 겹치거나 잘리면 고친다. 렌더러는 rsvg-convert, inkscape,
Chrome 순으로 찾고, 셋 다 없으면 MuPDF로 대신하는데 MuPDF는 폰트를 바꿔 끼우고 `<marker>` 화살촉을
그리지 않는다. 골격이 화살촉을 `<polygon>`으로 그리는 이유다.

### 5. 조립

`assets/template.md` 골격대로 `summary.md`를 쓴다. 그림은 그 그림이 받치는 문장 바로 뒤에 둔다.
Evaluation 문단 사이에 끼워도 된다. 템플릿의 위치는 예시다. 캡션은 그림 설명이 아니라 주장이고, 그림
줄과 캡션 줄 사이는 빈 줄 하나다. 커버가 없으면 cover 두 줄을 지운다.

서브에이전트로 돌 때 Write 도구가 "보고서 파일은 텍스트로 반환하라"며 거부하면 Bash heredoc으로 쓴다.
summary.md는 이 스킬의 산출물이지 보고서가 아니다.

HTML을 골랐으면 `python3 <S>/build_html.py <slug>/summary.md`. `summary.html`이 옆에 생긴다.

### 6. 검산

```
python3 <S>/check_summary.py <slug>/summary.md --pdf <paper.pdf>
```

FAIL 0이어야 끝. 그 다음 직접 확인한다.

- [ ] Claim이 기여 목록이 아니라 한 문장의 판단이다
- [ ] Evaluation에 "나라면" 문장이 있다
- [ ] 다이어그램의 accent 노드가 Approach 문장의 핵심 단어와 같다
- [ ] 차트 수치가 `results.json`의 source 표와 일치한다 (표 페이지를 다시 연다)
- [ ] 그림마다 캡션이 주장을 말한다
- [ ] HTML이면 외부 리소스 참조가 없다 (`grep -c -E '(src|href)="https?://' summary.html`이 0)

끝나면 사용자에게 세 줄: 결과 폴더 경로, Verdict와 한 문장, 카드 파일 경로.

## 흔한 실패

| 증상 | 원인 | 고치는 법 |
|---|---|---|
| 문장 하나가 세 줄 | 나열을 쉼표로 이었다 | 나열은 불릿으로. 문장은 140자 안에서 끊는다 |
| Approach가 6문장 | Method를 정독하고 다 쓰려 함 | 메커니즘 하나만. 나머지는 다이어그램 |
| Claim이 "A, B, C를 제안한다" | 기여 목록 복사 | 저자가 셋 중 무엇을 가장 자랑하는지 하나 고르기 |
| Evaluation이 숫자 나열 | 표를 문장으로 옮김 | 숫자는 차트, 문장은 설정과 red flag |
| 카드 텍스트가 `…`로 잘림 | paces.json이 본문과 같은 길이 | 카드용은 한 줄. 본문과 달라도 된다 |
| 다이어그램이 논문 Figure 1 복제 | 원문 구조를 그대로 옮김 | 입력 → 새 부분 → 출력 세 덩어리로 다시 |
| 차트 막대가 다 비슷 | 값 폭이 좁은데 `--kind bar` 강제 | `auto`로 두어 점 그래프를 쓴다 |

## 다른 에이전트에서 쓰기

- Codex: 이 폴더를 `~/.agents/skills/summary-paper/`에 두거나 플러그인으로 설치한다.
  형식 질문은 채팅으로 한다. 생성형 커버는 내장 image_gen을 쓴다.
- Read 도구가 없는 런타임: PDF는 `pdftotext`와 `paperviz.py preview`(쪽 PNG)로 읽는다.
- 파일 쓰기가 막힌 런타임: Bash heredoc으로 쓴다.
