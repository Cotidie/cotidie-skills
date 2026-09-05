# 시각화 규칙

팔레트와 문체는 explain-concept, textbook-notes와 같다. 그림은 논문을 다시 그리는 것이
아니라 PACES 답 하나를 받친다. 받치는 답이 없으면 그리지 않는다.

## 팔레트

라이트 기준. SVG는 흰 카드 위에 그리므로 다크 페이지에서도 읽힌다.

| 토큰 | 값 | 용도 |
|---|---|---|
| ink | #141A1D | 본문 글자, 노드 테두리 |
| ink-2 / ink-3 | #4C575C / #76838A | 보조 글자, 화살표, 라벨 |
| line / line-2 | #D2D9DC / #B4BFC3 | 헤어라인, 카드 테두리 |
| surface / ground | #FFFFFF / #EDEFF0 | 카드 배경 / 페이지 배경 |
| accent / accent-soft | #0A6C77 / #DCEDEF | 논문이 새로 추가한 것 하나. Yes |
| warm / warm-soft | #8F5D0D / #F5E8CF | Partial |
| flag / flag-soft | #9C2A24 / #F3DDDB | No, 주의 |

폰트: `'IBM Plex Sans KR','Apple SD Gothic Neo','NanumGothic',system-ui,sans-serif`.
라벨: `'IBM Plex Mono',Menlo,monospace`. 그라디언트, 그림자, 아이콘, 이모지 없음.

## 1. PACES 카드 (`paperviz.py card`)

`paces.json`:

```json
{"title": "정식 제목", "authors": "First et al.", "venue": "ICLR", "year": 2021,
 "problem": "한 줄", "approach": "한두 줄", "claim": "한 줄", "evaluation": "한두 줄",
 "substantiation": {"verdict": "Yes", "text": "한 줄"}}
```

카드용 답은 본문보다 짧다. 항목당 4줄(약 160자)을 넘으면 `…`로 잘린다. 잘리면 문장을
줄인다. `verdict`는 `Yes`, `Partial`, `No` 중 하나.

## 2. 방법 다이어그램 (직접 쓰는 SVG)

무엇을 그리나: Approach 문장의 메커니즘. 입력 → 기존 구성요소 → **새 구성요소** → 출력.
논문의 Figure 1을 옮기지 않는다. Figure 1은 저자 관점의 전체 시스템이고, 이 그림은
"무엇이 새로운가" 하나만 말한다.

- viewBox 너비 960, 높이는 내용에 맞춘다. 좌→우 흐름. 노드 7개 이하.
- 노드는 둥근 사각형(rx 6), stroke ink 1.5, fill surface. 새 구성요소만 fill accent-soft,
  stroke accent, 글자 굵게.
- 라벨 4단어 이하. 화살표 위 라벨은 데이터 형태(패치 시퀀스, 토큰, 이미지)나 shape.
  논문에 없는 shape는 쓰지 않는다.
- 갈래가 둘 이상이면 갈라지는 이유를 라벨로 적는다.
- 글자 16px 이상. `paperviz.py preview`로 렌더해서 읽기 어려우면 노드를 줄인다.
- `text-anchor`는 `<text>`마다 직접 쓰고, 화살촉은 `<marker>` 대신 `<polygon>`으로 그린다.
  MuPDF(렌더러 fallback)가 `<g>` 상속과 marker를 지원하지 않아서다. 아래 골격이 그 형태다.

골격:

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 240" width="960" height="240"
     font-family="'IBM Plex Sans KR','NanumGothic',sans-serif" font-size="16">
  <rect width="960" height="240" fill="#FFFFFF" stroke="#B4BFC3"/>
  <!-- nodes: the new component alone gets the accent -->
  <rect x="40" y="90" width="170" height="60" rx="6" fill="#FFFFFF" stroke="#141A1D" stroke-width="1.5"/>
  <rect x="395" y="90" width="170" height="60" rx="6" fill="#DCEDEF" stroke="#0A6C77" stroke-width="1.5"/>
  <rect x="750" y="90" width="170" height="60" rx="6" fill="#FFFFFF" stroke="#141A1D" stroke-width="1.5"/>
  <text x="125" y="126" text-anchor="middle" fill="#141A1D">이미지</text>
  <text x="480" y="126" text-anchor="middle" fill="#141A1D" font-weight="600">패치 임베딩</text>
  <text x="835" y="126" text-anchor="middle" fill="#141A1D">클래스 확률</text>
  <!-- arrows: line + explicit polygon head (markers are dropped by some renderers) -->
  <line x1="210" y1="120" x2="385" y2="120" stroke="#4C575C" stroke-width="1.5"/>
  <polygon points="385,114 395,120 385,126" fill="#4C575C"/>
  <line x1="565" y1="120" x2="740" y2="120" stroke="#4C575C" stroke-width="1.5"/>
  <polygon points="740,114 750,120 740,126" fill="#4C575C"/>
  <!-- edge labels: what flows, only shapes the paper states -->
  <text x="302" y="110" text-anchor="middle" fill="#76838A" font-size="13">16×16 패치 N개</text>
  <text x="657" y="110" text-anchor="middle" fill="#76838A" font-size="13">토큰 시퀀스</text>
</svg>
```

## 3. 결과 차트 (`paperviz.py chart`)

`results.json`:

```json
{"title": "차트 제목", "metric": "축 라벨 (단위)", "higher_is_better": true,
 "highlight": "제안 방법 이름", "source": "Table 2, p.6",
 "groups": [{"name": "ImageNet", "values": {"BiT-L": 87.54, "ViT-H/14": 88.55}},
            {"name": "CIFAR-100", "values": {"BiT-L": 93.51, "ViT-H/14": 94.55}}]}
```

- 표 하나에서만 뽑는다. `source`에 표 번호와 페이지. 두 표를 섞지 않는다.
- 방법 6개 이하, 그룹 4개 이하. 표가 더 넓으면 Claim에 직접 닿는 열을 고른다. 열을 합치거나 평균을
  내지 않는다. 논문에 없는 숫자가 생기기 때문이다. 표에 이미 평균 열이 있으면 그 열은 쓸 수 있다.
- 값이 없는 칸은 `null`. `highlight`는 `values`의 키와 글자까지 같아야 한다.
- 자동 선택: 어느 그룹 안에서도 값의 폭이 최댓값의 15% 미만이면 점 그래프(축이 0에서 시작하지
  않는다고 표기), 한 그룹이라도 넓으면 0에서 시작하는 막대. SOTA 표(그룹마다 기준선이 다르고 안에서는
  1~3점 차이)는 점 그래프가 된다. `--kind bar|dot`으로 강제 가능.
- 제안 방법만 accent, 나머지는 회색. 색이 말하는 것은 "이것이 제안 방법" 하나다.

## 4. 원문 크롭 (`paperviz.py preview` → `crop`)

언제: 다시 그리면 정보가 사라지는 그림. 정성 결과(생성 샘플, attention map, segmentation),
실제 장치나 로봇 사진, 사용자 연구 화면. 아키텍처 그림은 크롭하지 않는다. 2번에서 다시 그린다.

1. `python3 <S>/paperviz.py preview paper.pdf --page N -o /tmp/pN.png` 를 Read.
   0.1 간격 격자에서 bbox를 읽는다.
2. `python3 <S>/paperviz.py crop paper.pdf --page N --bbox x0 y0 x1 y1 -o figures/fig-N.png`
   (좌상 x0 y0, 우하 x1 y1, 페이지 비율 0~1).
3. Read로 확인. 캡션이 잘렸거나 옆 컬럼이 들어왔으면 bbox를 한 번 조정한다.
4. 캡션에 `원문 Figure N, p.M` 또는 `원문 Table N, p.M`(정성 비교가 표 안에 있는 논문이 있다). 최대 2장.

## 5. 생성형 커버 (codex-image 스킬)

조건: `codex` CLI가 있고 codex-image 스킬을 부를 수 있을 때. 없으면 생략하고 template의
cover 두 줄을 지운다. 사용자에게 따로 알릴 필요 없다.

무엇: 논문 핵심 아이디어의 추상 일러스트. 장식이다. 사실 정보를 담지 않고 글자를 넣지 않는다.

프롬프트 골격:
`A minimal editorial illustration of <핵심 아이디어를 비유 하나로>, flat shapes,
palette teal #0A6C77 and warm sand #F5E8CF on off-white, no text, no logos, 16:9.`

저장: `figures/cover.png`. Read로 확인하고, 논문과 무관해 보이면 한 번만 다시 만든다.

## 캡션

주장을 말한다. "ViT 아키텍처"가 아니라 "패치 임베딩 뒤는 표준 Transformer 인코더
그대로다". 차트 캡션에는 출처 표와 페이지를 적는다.
