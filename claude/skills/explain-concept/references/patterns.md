# 구조 패턴 라이브러리

복붙해서 쓰는 HTML/CSS 골격. 각 패턴에 **쓸 수 있는 조건**이 붙어 있다. 조건이 안 맞으면 쓰지 않는다.

---

## 0. 토큰 골격 (항상 먼저)

```css
:root{
  --ground:#EDEFF0; --surface:#FFFFFF; --surface-2:#F5F7F8;
  --ink:#141A1D; --ink-2:#4C575C; --ink-3:#76838A;
  --line:#D2D9DC; --line-2:#B4BFC3;
  --a:#0A6C77; --a-soft:#DCEDEF;   /* 주체 A 정체성 */
  --b:#8F5D0D; --b-soft:#F5E8CF;   /* 주체 B 정체성 */
  --flag:#9C2A24;                  /* 주의 */
}
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]){
    --ground:#111517; --surface:#191E21; --surface-2:#20272A;
    --ink:#E7ECEE; --ink-2:#A6B1B6; --ink-3:#7C898E;
    --line:#2C3438; --line-2:#424C51;
    --a:#4ECAD5; --a-soft:#0E3236;
    --b:#E2B155; --b-soft:#362A11;
    --flag:#EF8A80;
  }
}
:root[data-theme="dark"]{ /* 위 다크 블록과 동일한 토큰 재정의 */ }

*{box-sizing:border-box}
body{margin:0;background:var(--ground);color:var(--ink);
  font-family:"IBM Plex Sans KR","Apple SD Gothic Neo",system-ui,sans-serif;
  font-size:16.5px;line-height:1.72}
.wrap{max-width:62rem;margin-inline:auto;padding:0 1.5rem 6rem}
p,li{max-width:42rem}
.label{font-family:"IBM Plex Mono",monospace;font-size:.72rem;
  letter-spacing:.14em;text-transform:uppercase;color:var(--ink-3)}
section{padding-top:3.6rem;margin-top:3.2rem;border-top:1px solid var(--line)}
h2{font-size:clamp(1.5rem,3.4vw,2rem);font-weight:600;
  letter-spacing:-.02em;margin:0 0 1.1rem;text-wrap:balance}
:focus-visible{outline:2px solid var(--a);outline-offset:3px}
```

폰트: `https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans+KR:wght@300;400;500;600;700&display=swap`

---

## 1. lede 블록

**조건:** 항상. 문서 첫 화면에 온다. 3~6문장. 절차 서술은 첫 문장 하나까지, 두 번째 문장은 최상위 "왜".
조립 절차는 SKILL.md Phase 2의 5단계.

```html
<div class="verdict">
  <p>정체 한 문장. 무엇을 하는 것인가.</p>
  <p>최상위 "왜" 한 문장. 그 다음에 대가와 경계.</p>
</div>
```
```css
.verdict{margin:2.5rem 0 0;padding:1.5rem 1.6rem;
  background:var(--surface);border:1px solid var(--line-2)}
.verdict p{margin:0;font-size:1.12rem;font-weight:500;max-width:46rem}
.verdict p+p{margin-top:.6rem;font-weight:400;font-size:1rem;color:var(--ink-2)}
```

---

## 2. 연표 + 해법 콜아웃

**조건:** 날짜가 인과를 담을 때만. B가 A의 문제 때문에 생겼을 때.
세로선도 점도 아이콘도 없다. 행마다 헤어라인 한 줄뿐.
중요한 행에만 불릿과 해법을 붙인다. 후속 행은 한 문장. 이 비대칭이 중요도를 말한다.
불릿은 과거형(문제), 해법은 현재형(전환점 표시).

```html
<div class="tl__item">
  <div class="tl__year">1998<small>RTSP</small></div>
  <div class="tl__body">
    <h3>파일이 다 내려와야 재생되던 시절</h3>
    <ul><li>불편 1</li><li>불편 2</li><li>불편 3</li></ul>
    <span class="fix"><b>해법</b>현재형 한두 문장.</span>
  </div>
</div>
```
```css
.tl__item{display:grid;grid-template-columns:7.5rem 1fr;gap:0 1.6rem;
  padding:1.4rem 0;border-top:1px solid var(--line)}
.tl__year{font-family:"IBM Plex Mono",monospace;font-size:1.1rem;
  font-weight:500;font-variant-numeric:tabular-nums}
.tl__year small{display:block;font-size:.68rem;letter-spacing:.12em;
  text-transform:uppercase;color:var(--ink-3);margin-top:.2rem}
.fix{display:block;padding:.7rem .9rem;background:var(--surface);
  border:1px solid var(--line);max-width:42rem}
.fix b{display:block;font-family:"IBM Plex Mono",monospace;font-size:.7rem;
  letter-spacing:.12em;text-transform:uppercase;color:var(--ink-3)}
@media (max-width:640px){
  .tl__item{grid-template-columns:1fr;gap:.5rem}
  .tl__year small{display:inline;margin-left:.6rem}
}
```

전제: `--ground`가 회색이고 `--surface`가 흰색이어야 콜아웃이 뜬다. 바탕이 순백이면 테두리를 진하게 바꾼다.

---

## 3. 대칭 비교 카드

**조건:** 두 항목이 대등한 선택지일 때만. 개수와 형식을 반드시 맞춘다(5개 대 5개).

```html
<article class="fill fill--a">
  <h3>A가 채운 B의 부족</h3>
  <p>이 묶음이 무엇에 관한 것인지 한 줄.</p>
  <ol>
    <li><b>짧은 제목</b><span>한 줄 설명.</span></li>
  </ol>
</article>
```
```css
.pair{display:grid;grid-template-columns:repeat(auto-fit,minmax(20rem,1fr));gap:1.25rem}
.fill{background:var(--surface);border:1px solid var(--line);padding:1.15rem 1.25rem 1.4rem}
.fill--a{--accent:var(--a)} .fill--b{--accent:var(--b)}
.fill h3{color:var(--accent);font-size:1rem;margin:0 0 .2rem}
.fill ol{margin:0;padding:0;list-style:none;counter-reset:f}
.fill li{counter-increment:f;padding:.7rem 0 .7rem 2rem;position:relative;
  border-top:1px solid var(--line);font-size:.96rem;max-width:none}
.fill li::before{content:counter(f,decimal-leading-zero);position:absolute;
  left:0;top:.85rem;font-family:"IBM Plex Mono",monospace;
  font-size:.7rem;color:var(--accent)}
.fill li span{display:block;color:var(--ink-2);font-size:.9rem}
```

---

## 4. 가로 막대 차트

**조건:** 비교할 실제 수치가 있고, 크기 차이가 논지일 때만. 3~5개 막대.
막대 폭은 공통 축의 백분율. 값 라벨은 별도 그리드 칸에 두어 넘치지 않게 한다.

```html
<div class="chart">
  <div class="chart__row">
    <div class="chart__name">RTSP</div>
    <div class="chart__track"><div class="chart__bar" style="width:6.3%;background:var(--a)"></div></div>
    <div class="chart__val">1.5초</div>
  </div>
  <div class="chart__axis"><span>0</span><span>6</span><span>12</span><span>18</span><span>24초</span></div>
  <p class="chart__note">수치의 내역과 근거 한 줄.</p>
</div>
```
```css
.chart{background:var(--surface);border:1px solid var(--line);padding:1.4rem 1.3rem 1.1rem}
.chart__row{display:grid;grid-template-columns:6.5rem 1fr 4.2rem;
  align-items:center;gap:.9rem;margin-bottom:.85rem}
.chart__name{font-family:"IBM Plex Mono",monospace;font-size:.78rem;color:var(--ink-2)}
.chart__track{height:1.35rem;background:var(--surface-2);border:1px solid var(--line)}
.chart__bar{height:100%;display:block}
.chart__val{font-family:"IBM Plex Mono",monospace;font-size:.8rem;
  font-variant-numeric:tabular-nums;text-align:right}
.chart__axis{display:flex;justify-content:space-between;border-top:1px solid var(--line-2);
  margin:0 5.1rem 0 7.4rem;padding-top:.35rem}
.chart__axis span{font-family:"IBM Plex Mono",monospace;font-size:.7rem;color:var(--ink-3)}
@media (max-width:640px){
  .chart__row{grid-template-columns:4.6rem 1fr 3.4rem;gap:.55rem}
  .chart__axis{margin:0 3.95rem 0 5.15rem}
}
```

---

## 5. 대조표 / 선택표

**조건:** 항목이 6개 이상이거나, 축이 두 개(대상 × 항목)일 때. 표는 5항목 제한의 예외다.
헤더 셀에 주체 정체성 색을 준다. 선택표는 `상황 → 선택 → 이유` 3열로 5행 이하.

```html
<div class="scroll">
  <table>
    <thead><tr><th>구분</th><th>A</th><th>B</th></tr></thead>
    <tbody><tr><th>항목</th><td>값</td><td>값</td></tr></tbody>
  </table>
</div>
```
```css
.scroll{overflow-x:auto;border:1px solid var(--line);background:var(--surface)}
table{border-collapse:collapse;width:100%;min-width:38rem;font-size:.94rem}
th,td{text-align:left;padding:.72rem .95rem;border-top:1px solid var(--line);vertical-align:top}
thead th{border-top:0;border-bottom:1px solid var(--line-2);
  font-family:"IBM Plex Mono",monospace;font-size:.72rem;
  letter-spacing:.12em;text-transform:uppercase;font-weight:500}
thead th:nth-child(2){color:var(--a)} thead th:nth-child(3){color:var(--b)}
tbody th{font-weight:500;color:var(--ink-2);white-space:nowrap;font-size:.88rem}
tbody tr:nth-child(even){background:var(--surface-2)}
```

---

## 6. 파이프라인 다이어그램

**조건:** 실제로 단계가 이어져 흐를 때. 노드 3~5개.

```html
<div class="pipe">
  <div class="node"><b>노드 이름</b><span>보조 설명<br>둘째 줄</span></div>
  <div class="hop"><em>→</em><span>구간 라벨</span></div>
  <div class="node"><b>다음 노드</b><span>보조 설명</span></div>
</div>
```
```css
.pipe{display:flex;flex-wrap:wrap;align-items:stretch;gap:.5rem;
  background:var(--surface);border:1px solid var(--line);padding:1.3rem 1.2rem}
.node{flex:1 1 9rem;min-width:8.5rem;padding:.75rem .85rem;
  background:var(--surface-2);border:1px solid var(--line)}
.node b{display:block;font-size:.93rem;margin-bottom:.15rem}
.node span{font-size:.8rem;color:var(--ink-3);line-height:1.5;display:block}
.hop{display:flex;flex-direction:column;justify-content:center;align-items:center;padding:0 .1rem}
.hop span{font-family:"IBM Plex Mono",monospace;font-size:.66rem;
  letter-spacing:.08em;color:var(--ink-3);white-space:nowrap}
.hop em{font-style:normal;color:var(--line-2);font-size:1.1rem}
```

---

## 7. 오해 노트

**조건:** 실제로 사람들이 틀리는 지점이 있을 때. 3~4개.

```html
<div class="notes">
  <div><span class="mark">01</span><p><b>단언 문장.</b> 왜 그런지 한 줄.</p></div>
</div>
```
```css
.notes div{padding:1rem 0;border-top:1px solid var(--line);
  display:grid;grid-template-columns:1.6rem 1fr;gap:.9rem}
.notes .mark{font-family:"IBM Plex Mono",monospace;font-size:.82rem;color:var(--flag)}
.notes p{margin:0;font-size:.96rem}
```

---

## 8. 출처 목록

**조건:** 항상. 등급 태그와 무엇을 가져왔는지를 함께 적는다.

```html
<ul class="src">
  <li><span class="k">RFC 2326</span><a href="...">문서 제목, 발행처 연도</a> · 여기서 가져온 것</li>
</ul>
```
```css
.src{padding:0;list-style:none}
.src li{padding:.6rem 0;border-top:1px solid var(--line);
  font-size:.9rem;color:var(--ink-2);max-width:none}
.src .k{font-family:"IBM Plex Mono",monospace;font-size:.72rem;
  letter-spacing:.08em;color:var(--ink-3);margin-right:.7rem}
```

---

## 코드·프로토콜 예시 블록

**조건:** 실제 문법·대화를 보여줄 때. 설명 열 줄보다 예시 여섯 줄이 낫다.

```css
pre{margin:1rem 0 0;padding:.9rem 1rem;overflow-x:auto;
  background:var(--surface-2);border:1px solid var(--line);
  font-family:"IBM Plex Mono",monospace;font-size:.78rem;
  line-height:1.85;color:var(--ink-2)}
pre b{color:var(--accent,var(--ink));font-weight:600}  /* 키워드 */
pre i{color:var(--ink-3);font-style:normal}            /* 주석 */
```
