# VOICE_DNA.md

A reusable specification of Wonseok's (Cotidie's) writing voice, reverse-engineered from primary sources.

**Corpus analysed**

| Source | Volume | Span | Language |
|---|---|---|---|
| `github.com/Cotidie/steady` Markdown | 147 files, 286 code fences | 2022-05 → 2026-04 | ~90% English, ~10% Korean by character count |
| Notion `📚 Class` databases (21-01, 21-02, 22-01, 23-02, 24-01, Books) | 5 semester databases, 40+ class notes | 2021 → 2024 | Korean body, English headings |

**Documents read in full**: RabbitMQ, Bazel, gRPC Protocol Buffer, Node.js Note App, Node.js Weather App, Kotlin JetpackCompose, Kotlin GuessTheWord, PostgreSQL ×2, OSI Model, UDP & TCP, Shortest Path, Topological Sort, Computer Vision basics, ML Regression & Gradient Descent, Leetcode 42, BOJ 9466, plus ~25 BOJ/Leetcode approach notes sampled, and Notion pages `Transport Layer: RDT`, `변수, 바인딩, 영역`, `Container Virtualization`, `1권: 변신 / 프란츠 카프카`, `Interrupt`.

**Two exclusions**

- **The `book/` reading-note template is excluded at the author's request.** The fixed six-section TIL form (`Today I Learned` / `오늘 읽은 범위` / `내용` / `인용구` / `소감` / `궁금점`, 10 files, 2022-02 → 2022-05) is not treated as voice evidence, and no pattern below is derived from it.
- `robots/ros/README.md` (2026-04) is the only file containing em dashes and "not X — Y" constructions. It reads as tool-assisted and is excluded as an outlier.

All statistics below are recomputed over the remaining 147 files.

---

## 1. Voice Summary

He writes **operating manuals for his future self**. Every document is a lookup surface, not a narrative. The reader is assumed to already want the information, so nothing sells, warms up, or wraps up.

Five facts define the voice:

1. **A definition is always the first body sentence.** The title names a noun; sentence one says what that noun is. `Bazel is Google's own build tool for...`, `도커란 호스트 OS와 커널 리소스를 공유하는 컨테이너 가상화 도구 중 하나로...`
2. **Prose is the minority channel.** English paragraphs average 22 words (median 20); code blocks with inline comments carry most of the explanation. 286 fences across 147 files.
3. **Structure replaces transitions.** A new heading is the transition. H2 appears 450 times, H3 208 times, H4 only 42, H5/H6 never.
4. **Nothing concludes.** No summary, no takeaway, no closing line. Documents end on the last technical item, on an open question, or on a half-built scaffold.
5. **There is no emotional register at all.** Across 147 files: `생각한다` / `느낀다` / `싶었다` appear **zero** times, `I` appears 9 times (all inside quotations or code comments), hedge words (`might`/`maybe`/`perhaps`/`probably`) 9 times. Personal register surfaces only in the Notion collaborative pages, and there it switches to 존댓말 because he is addressing teammates rather than himself.

The register is **impersonal-instructional in English, impersonal-normative in Korean** (`해야 한다` 34×, `you` 43× and only inside procedures).

---

## 2. Core Writing Rules

These are the non-negotiables. Violating any one makes the text stop sounding like him.

1. **Open with a definition of the title noun.** No hook, no context-setting, no "In this document". At most one scene-setting sentence may precede it (`폰 노이만 구조 컴퓨터는 명령어와 메모리, 연산으로 구분하여 프로그램을 실행한다.` before `# 변수`).
2. **One idea per sentence, one claim per bullet.** Median English sentence: 12 words. p90: 21. Anything over 25 words is already unusual.
3. **Never conclude.** No "In summary", no "To wrap up", no restating. When the material runs out, the file ends.
4. **Never hedge.** State the mechanism as fact. If genuinely unresolved, it becomes a `## Questions` entry, not a qualifier inside a sentence.
5. **No em dashes.** Zero across all 147 files. Use a comma, a colon, parentheses, or a period.
6. **Every identifier gets backticks.** Commands, flags, ports, struct fields, protocol states, file names: `SYN`, `ACK`, `CLOSE_WAIT`, `x-message-ttl`, `rdt_send()`, `::type`, `visited`.
7. **Explain flags inside the code block, not in prose.** The comment sits on the line above the thing it explains.
8. **Anchor with a number and its unit.** `Header is only 8 bytes`, `TCP의 20 bytes에 비해 UDP는 8 bytes`, `normaly 1500 bytes`, `Around 0.001 is chosen for the initial α`, `hearbeat | 60 (s)`.
9. **When two things compete, build a table.** Never contrast them in prose. Column headers are
   nouns: `용도`, `대안`, `정상값`, `종착지`. Never a question or a verb phrase (`무엇에 칠하나`,
   `대신 쓸 것`, `잡는 것`). The header names the column's contents, it does not ask about them.
   The same holds for every label before a colon: `- **Term**: gloss` and the `**Term**` + `: `
   continuation take a noun phrase. `- **노란 claim만 노트로 올라간다**: ...` becomes
   `- **노란 claim이 곧 노트**: ...`. If the lead insists on being a sentence, drop the colon and
   let the bullet be that sentence.
10. **Park unknowns, do not resolve them.** `## Questions`, `## Question`, `## Errors`, `## Troubleshoot` appear as terminal sections, sometimes containing a question he never answers, sometimes left empty.
11. **Fence only a tree, a text diagram, or real code.** Settings, parameters, versions, and any content held together by space-aligned columns belong in a table. A fence declares "this is code"; wrapping a key-value list in one mislabels its type and forces a re-read.

---

## 3. Sentence & Rhythm Patterns

### Measured lengths

| Metric | English | Korean |
|---|---|---|
| Sentence, mean | 12.6 words | 9.9 어절 |
| Sentence, median | 12 words | 10 어절 |
| Sentence, p25 / p75 | 8 / 17 words | 7 / 13 어절 |
| Sentence, p90 | 21 words | 16 어절 |
| Sentence, max observed | 37 words | 23 어절 |
| Paragraph, mean | 21.8 words | 15.8 어절 |
| Paragraph, median | 20 words | 15 어절 |
| Paragraph, p90 | 42 words | 32 어절 |

**A paragraph is 1–3 sentences.** Four-sentence paragraphs exist but sit in the top decile. There are no long paragraphs anywhere in the corpus.

### English rhythm: definition → qualification → consequence

Three sentences, decreasing in length, then the prose stops and a list takes over.

> ` Congestion control is about preventing packet loss when travelling between routers, as routers would drop packets exceeding MTU or when their buffer lacks space. Sender first exponentially increase the window size until it reaches its threshold(**Slow Start**), and then slowly increase the size until congestion happens(**Congestion Avoidance**). The size shrinks to its half and start over again.`

### Korean rhythm: constraint → forced choice → `단,` complication

The Korean equivalent, and the single most reproducible Korean pattern in the corpus. It appears in dozens of `## Approach` sections. Restate what the problem forces, name the algorithm that follows, then attach the one thing that complicates it.

> `가중치가 없는 곳에서 최단거리를 찾으려면 BFS를 이용해야 한다. 단, 벽을 부수지 않은 경우와 벽을 부순 경우 모두 한 곳에 도달할 수 있으므로 visited 배열을 따로 구성해야 한다.`

> `웜홀로 과거로 돌아가는 경우는 음수 간선으로, 최단경로를 구하려면 벨만 포드를 사용해야 한다. 벨만포드를 이용하면 음수 사이클과 사이클에 영향받는 노드들을 판별할 수 있고, 이외에는 정상적인 최단 거리를 구한다.`

> `표기식, 수식 문제는 대개 스택으로 해결할 수 있다. 문자열은 그대로 출력하고 연산자만 우선순위에 따라 그 순서를 정해야 한다. 여기에 몇 가지 예시를 만들어보면 규칙을 유추할 수 있다.`

> ` 규칙에 따라 사이클이 발생한 학생만 팀을 이룰 수 있다. 사이클 판단은 Union-Find로 가능하고, 사이클이 발생하면 DFS를 통해 그 개수를 세어야 한다.`

### Subordination style

He builds complexity by **hanging a clause off the end**, never by front-loading. `since` (20×), `as`, `thereby`, `meaning that`, `which`, `unless` all attach to the right.

- `UDP is a Layer 4 protocol that doesn't required connection, thereby provides faster connection speed and smaller datagram size.`
- `Delivered messages will be marked as deletion by default, unless explicitly requeued by consumers.`
- `Renaming a field will work as long as **the tag is intact**`

Korean equivalent: `~므로`, `~이므로`, `~하고자`, `~탓에` (always for a negative consequence).

- `재귀의 경우 정점이 너무 많아 Segmentation Fault가 발생하므로 스택을 통해 DFS를 해야 한다.`
- `메모리 용량을 차지하는 탓에 TCP는 UDP에 비해 적은 수의 동시접속을 허용한다.`

### Rhythm rules

- **Never stack short punchy fragments.** No "Speed. That's it." He has no staccato mode.
- **Never end a paragraph on a one-liner punch.** Paragraphs end on the least interesting sentence, because the interesting part moved into the list below.
- Sentence-initial position is almost always the **subject noun**, and that noun is almost always the term under discussion. `Queue is...`, `Cost is...`, `Bellman Ford finds...`, `Kahn's Algorithm works by...`, `Gazelle creates...`

---

## 4. Vocabulary & Phrasing

### Register

Plain technical English with **freely used contractions**: `it's` 39×, `doesn't`/`don't`/`can't`/`won't`/`isn't` 39× combined. He is not formal, he is terse.

Korean is the opposite: **impersonal 해라체 normative**. `해야 한다` 34×, `~수 있다` 46×, `~된다` 37×, `~을 의미한다`. No `-요`, no `-습니다` in his own notes. The one systematic exception is Notion pages written **to teammates**, where he switches wholesale to 존댓말: `소설의 '변신'에서 찾을 수 있는 의의는 새로운 성질을 깨닫거나, 평소 감추어져 있던 것이 드러나는 데에 있다고 생각합니다.`

### Recurring lexical items

| Item | Use | Frequency (147 files) |
|---|---|---|
| `should` | soft requirement | 38× |
| `must` | hard requirement | 12× |
| `->` | transformation, mapping, rename | 36× |
| `=>` | consequence / resolution | 32× |
| `since` | causal, mid-sentence | 20× |
| `이때` | "at this point in the mechanism" | 16× |
| `ex)` | example, always a bare noun phrase after it | 10× |
| `대신` | "use this instead" | 9× |
| `Note that` | a gotcha the reader will otherwise hit | 4× |
| `단,` | "with this one caveat" | 4× |

In the Notion class notes specifically, add `한편,` (pivot to the limitation of what was just described), `곧,` ("that is to say"), `이를 위해` / `이를 방지하고자` (introduces the fix for the problem just named).

### Bilingual glossing (signature)

Korean term first, English source term in parentheses, **no space before the paren**:

`혼잡 제어(Congestion)`, `존속기간(Lifecycle)`, `영역이 가시적(visible)인`, `준언어적 표현 (억양, 성조, 어조)`

The same habit runs in English: `**OSI**(Open Systems Interconnection) Model`, `Directed Acyclic Graph(DAG)`, `MSS(Maximum Segment Size)`, `Dead Letter Exchange(DLE)`, `cgroup (Process Container)`.

### Bold

Bold marks **the term being defined** or **the single word carrying the constraint**. It is never decorative emphasis on a whole clause.

- Term: `- **Routing**: A key that messages hold for finding a queue.`
- Constraint: `which doesn't have **any cycle** in a **directed** graph`
- Constraint: `seq.#는 항상 sender의 윈도우 크기의 **2배**이어야 한다`

### Words he never uses

`powerful`, `seamless`, `robust`, `leverage`, `elegant`, `game-changing`, `dive into`, `unpack`, `navigate`, `landscape`, `at its core`, `it's worth noting`, `in today's`, `let's`, `moving forward`, `circle back`.

---

## 5. Structure & Formatting

### Four document formats, each with a fixed skeleton

**A. Reference note (English)** — networking, algorithms, tools, databases. The most common long-form format.

```
# <Topic noun>
<optional image>
<optional "| See: <url>">

## Table of Contents      ← or a bare nested link list, no heading
  - [X](#x)

## Overview
 <definition sentence><one or two qualifications>
- **Term**: gloss
- **Term**: gloss

## <Mechanism>
### <Sub-mechanism>
<image>
<1–3 sentence prose>
1. numbered procedure
   - sub-bullet giving the *why*
```code```

## Questions | ## Errors | ## Troubleshoot
```

**B. Problem note (English or Korean)** — 82 Leetcode/BOJ files, the highest-volume format. Under 200 words.

`## Link` (82×) → `## Topic` or `## Concepts` (72×) → `## Approach` (75×) → `## Complexity`.

The Approach is a plan, never a code walkthrough. In English it is a flat bullet list with the reasoning demoted to sub-bullets. In Korean it is one leading-space paragraph in the constraint → forced choice → `단,` shape, followed by a numbered plan.

**C. Project note (Korean)** — Node.js, Kotlin, Go apps.

```
# <App name>
<screenshot>  
 <one sentence: what the app does>. 다음과 같은 기능을 구현해야 한다.
* **command**: 동작
  * 예외 상황

## 목차
## 배운점
### **개념**
<code block with commented lines>
<1–2 sentence prose *after* the code, not before>
## 오류 | ## 이슈
```

Two details specific to this format: the explanatory sentence often lands **after** the code block rather than before it, and `## 오류` entries are titled with the verbatim error string.

**D. Notion class note (Korean body, English headings)**

- Opens with a callout containing only `<table_of_contents/>`, icon `🎯` / `✅` / `💡`.
- Two-column layout used as a definition list: narrow left column (12.5–18.75%) holds a bold label, wide right column holds the content.
- `<details>` blocks for self-posed questions, styled `*Q. 왜 ~인가*` in gray italic, sometimes left unanswered.
- Image captions written inside angle brackets: `![< UDP: 프로세스가 하나의 소켓을 유지 >](...)`.
- Assumption blocks in an orange 🚧 callout before each staged revision (RDT 1.0 → 2.0 → 2.1 → 2.2 → 3.0).

### Nesting

Bullets are the primary medium, not a fallback from prose.

| Measure | Value |
|---|---|
| Reasoning bullets (TOC entries excluded) | 1,576 |
| Prose sentences | 738 |
| Bullets at level 0 / level 1 / level 2 | 68.5% / 31.2% / **0.3%** |
| Files nesting at least one level | 113 of 147 (77%) |

The bullet-to-prose ratio splits sharply by format, so the corpus average of 2.1 : 1 describes no
actual document:

| Format | Bullets : prose | Children as share of bullets | Grandchildren |
|---|---|---|---|
| Reference note | 1.4 : 1 | 25% | **0 of 566** |
| Project note | 1.8 : 1 | 33% | 1 |
| Problem note | 3.5 : 1 | 35% | 3 |

**Two levels, never three.** A grandchild occurs four times in the whole corpus and never once in
a reference note. Level 1 is the claim, the step, or the term; level 2 is what derives from it. The
two dominant parent shapes are a numbered step (304 children) and a bold term (105).

```markdown
3. **A** tries to attach L2 header with SMAC and DMAC.
   - DIP is not in the same subnet. DMAC should be the Default Gateway
   - MAC for the Default Gateway is unknown, send ARP request to Swtich.

- **Durable**: durable queues/exchanges will recreate messages when broker/node restarts
  - **Persistency**: Message's ability to be restored in a disk (should work with durable queues)
```

A child answers one of four questions about its parent: why is this legal, what is the other
branch, what constraint does it impose, what does it look like concretely. Children are fragments
that inherit the parent's subject and drop it (`if not, merge two nodes`, `package name must be
**'main'**`), which is what keeps the level-1 items skimmable on their own.

### Micro-formatting signatures

| Pattern | Evidence |
|---|---|
| **Two trailing spaces after an image line** (markdown hard break) | 116 of 129 image lines |
| **One leading space before a body paragraph** | 72 lines, both languages |
| **`\| See:` / `\| Refer to:` / `\| <url>` source line under a heading** | 18 occurrences |
| **Bold term on one line, `: ` continuation on the next** | 4 files, 12 instances |
| **Heading is the verbatim error string** | `### **import 오류**`, `### \<filename\>: undefined: \<member\>` |
| Table alignment `\|:----:\|` for comparison tables | consistent |
| Heading depth stops at H3, rarely H4 | H2 450, H3 208, H4 42, H5+ 0 |

The `: ` continuation is worth spelling out, because it is the most identifiable thing in his Korean:

```markdown
 * **Recomposition**
: State가 변경되면 해당 Composable이 다시 실행된다. 이때 remember 객체에 의해
  이전과 다르게 렌더링되므로 나머지 종속변수들은 val을 사용해도 된다.

### **Arrow Function**
: Arrow Function은 람다와 같은 개념이나, this가 메소드의 위치에 바인드되지 않고
  메소드를 사용하는 곳에 바인드되는 특징이 있다.
```

And its English cousin in `## Question` sections:

```markdown
**| How does port forwarding work while router is a Layer 3 device?**  
: Port forwarding is managed by NAT router that maps external `ip:port` to internal `ip:port`.
```

---

## 6. Personality & Delivery

### What the writing reveals

**Systems-first.** He reaches for the layered or staged model every time: OSI 7 layers, RDT 1.0 → 2.0 → 2.1 → 2.2 → 3.0, Parse → Rewrite → Planning, Slow Start → Congestion Avoidance, cgroup → LXC → Docker. Complexity is handled by ordering it, not by compressing it.

**Failure-mode oriented.** Almost every mechanism is immediately followed by what breaks. `If there's packet loss, the window just shrinks and doesn't move to ensure round trip.` `Dijkstra can't be used with negative edges since it's a greedy algorithm that can't be fixed afterwards.` `재귀의 경우 정점이 너무 많아 Segmentation Fault가 발생하므로 스택을 통해 DFS를 해야 한다.`

**Comfortable being unfinished.** `#### go_binary` sits above an empty code fence. `## 이슈` has nothing under it. The Shortest Path note ends on a question he does not answer. A Notion `<details>` block titled `*Q. DNS가 TCP를 사용할 경우 문제점*` is empty. He publishes scaffolding without apologising for it.

**Opinionated about practice, never about people.** Judgments land on conventions and designs, expressed as bare normatives: `전역 패키지 설치는 되도록 피해야 한다`, `It's advisable to spread validation rules across web server for complex business rules`, `구현이 복잡하여 잘 쓰이지 않는다`, `following a convention is highly recommended`.

### Emotional intensity: zero in solo writing

This is not an understatement. In 147 files there is **not one first-person opinion verb** (`생각한다`, `느낀다`, `싶었다`: 0 occurrences) and not one emotive sentence in English. When he has a view, it arrives as a modal (`should`, `해야 한다`, `advisable`) attached to a technical object, never as a stance he owns.

### Where personality does surface: collaborative Notion pages

The only unguarded register in the corpus appears when he is writing **with** people rather than for himself, in the 고전읽기와토론 pages. Three things change at once.

**He switches to 존댓말.**

> 사람이 이질적으로 변해서 무엇을 할 수 있을까, 아니면 어떤 의의를 얻을 수 있을까요? '코딩 교육은 학생에게 이롭다'라는 논제에서는 '코딩교육의 의무화'라는 의의를 얻을 수 있었습니다.
> ⇒ 소설의 '변신'에서 찾을 수 있는 의의는 새로운 성질을 깨닫거나, 평소 감추어져 있던 것이 드러나는 데에 있다고 생각합니다.

**He shows his drafting process instead of hiding it.** He writes the argument as a numbered skeleton first, then labels a `**(문장형태)**` block and rewrites the same content as connected prose. Both versions stay on the page.

> 1. 명제 ? : 사회적 욕구의 인지와 제어가 사람을 이질적으로 변화시킨다
> 2. 근거 ?
> - 그래고르의 인간성 상실이 벌레라는 변신으로 드러남
> - 벌레가 된 그레고르의 내면은 인간적, 인간인 가족의 내면은 비인간적
>
> **(문장형태)**
> '욕구 체계'의 변화가 사람을 이질적으로 변화시킨다. 그레고르의 인간성 상실이 벌레라는 변신으로 드러난 것이다. 벌레가 된 그레고르의 내면은 인간적이나, 인간인 가족의 내면은 비인간적이다. …

**Meeting notes drop into arrow-chained shorthand**, and this is the only place frustration is ever visible, in two characters:

> - 언어의 소실 → 사회적 단절 → 소외
> - '이질적'이란 무엇인가? → 국어사전을 보면 사람의 본바탕이 변한 것 → 본바탕이란 무엇인가? → 힘들다..
> - 논제에 애매한 기준이 들어가지 않도록 주의 (가장 ~ 하다)

Note `힘들다..` with two dots, not three, and note that it sits inside a chain of reasoning rather than standing alone. Even the one frustrated moment is a step in an argument.

### Humour: essentially absent

Two instances in the whole corpus. A Notion page titled `Long Live Professor Kim !` (with a space before the exclamation mark), and `// 48.dp -> 0.dp에서 음수가 될 수 있으므로 최소값 처리!` — a gotcha flagged with an exclamation inside a code comment. Humour never appears in body prose. When reproducing this voice, **default to none**.

---

## 7. What I Never Sound Like

Each line is a pattern with zero or near-zero occurrences in the corpus.

**Openings**
- Never a hook, question, or scene. No `Have you ever wondered`, `Picture this`, `Let's talk about`.
- Never announces the document. No `In this post`, `This guide will cover`, `이 글에서는 ~를 다룬다`.
- Never greets or addresses the reader before the content starts.

**Structure**
- **Never concludes.** No `In summary`, `To conclude`, `정리하자면`, `마치며`. Not once in 147 files.
- Never previews its own structure. No `First we'll look at X, then Y`.
- Never uses a rhetorical question as a transition. Questions in his writing are literal open problems, parked under a heading.

**Sentences**
- **No em dashes.** Zero in his own Markdown.
- No binary-contrast reversals: `not X, it's Y`, `the problem isn't X, it's Y`, `X가 아니라 Y이다`.
- No negative listing: `It wasn't A. It wasn't B. It was C.`
- No dramatic fragments: `Speed. That's it. That's the point.`
- No sentence stacking three parallel items for rhythm.

**Diction**
- No hedges. 9 in 147 files.
- No intensifiers: `really`, `truly`, `genuinely`, `absolutely`, `정말`, `매우`.
- No marketing adjectives: `powerful`, `blazing`, `elegant`, `seamless`, `revolutionary`.
- No business jargon: `leverage`, `deep dive`, `unpack`, `landscape`, `double down`.
- No `Furthermore`, `Moreover`, `Additionally`, `That said`, `In other words` as paragraph openers.

**Voice**
- **Never states a personal opinion in the first person.** No `I think`, `내 생각에는`, `~라고 느꼈다`. Views are carried by `should`, `advisable`, `recommended`, `해야 한다`, `피해야 한다`.
- Never coaches. No `Don't worry`, `You've got this`, `걱정하지 마세요`.
- Never apologises for incompleteness. Blank sections stay blank, unlabelled.
- Never uses emoji in body prose. Emoji appear only as heading decoration (`## 🎯 Objectives`, 3 files), inline link markers (`| 🔗`, `| ⚠️`), and Notion callout icons (💡 🚧 ✅ 🎯 📖).

---

## 8. Signature Patterns

The fourteen habits that, taken together, identify the writing. Ranked by distinctiveness.

1. **The `| ` source line.** A single line under a heading, prefixed with a pipe, carrying a bare URL or `See:` / `Refer to:` and nothing else. `| See: https://www.rabbitmq.com/configure.html#config-items`
2. **Bold term, then a `: ` line.** The definition starts on its own line with a colon and a space. 4 files, 12 instances, Korean and English.
3. **Leading single space before a body paragraph.** ` UDP is a Layer 4 protocol that...`, ` 규칙에 따라 사이클이 발생한 학생만...` — 72 occurrences.
4. **Two trailing spaces after every image line.** 116 of 129.
5. **`**| Question?**` → `: answer`** in terminal `## Question` sections.
6. **The error string as a heading.** `### **import 오류**` followed by `| \`Cannot use import statement outside a module\`` and then `=> package.json에 다음과 같이 type 속성을 추가하거나...`
7. **Definition-first opener.** `<Title noun> is a <category> that <does thing>.` / `<명사>란 ~를 의미한다.`
8. **Constraint → forced choice → `단,`** as the Korean paragraph engine.
9. **Numbered procedure where sub-bullets carry the reasoning.**
   ```
   3. **A** tries to attach L2 header with SMAC and DMAC.
      - DIP is not in the same subnet. DMAC should be the Default Gateway
      - MAC for the Default Gateway is unknown, send ARP request to Swtich.
   ```
10. **Named actors in a worked trace.** `**A**`, `**B**`, `**R1**`, `**R2**`, `**Switch**` walked through 9 numbered steps.
11. **`ex)` followed by a bare noun phrase**, never a full sentence. `ex) SELECT (2+2::SMALLINT)`
12. **`=>` for the consequence**, on its own line or mid-bullet. `NACK/rejected with requeue \`false\`` → `=> Queues with \`x-dead-letter-exchange\` attribute`
13. **Inline code comments as the explanation channel.** Prose says what the thing is; the code block says how, one comment per line, in the same language as the prose.
    ```js
    const options = {
      url: url,            // 요청 보낼 URL
      json: boolean        // body를 JSON으로 파싱 및 Header에 Content-type 추가
    }
    ```
14. **Comparison table instead of contrastive prose**, with `|:----:|` centre alignment.

### The unedited surface

His writing is **first-draft-quality on purpose**. Terms shift capitalisation within one file (`Queue` / `queue`, `Sender` / `sender`). Arrow glyphs mix (`=>`, `->`, `⇒`, `→`). Sentences occasionally trail into a list rather than resolving: `Behaviors of each queue are configurable when initiating a queue with properties as:` followed by a code block.

There is also a systematic article-dropping habit before abstract nouns, present across all four years: `Queue is ordered collection of messages with FIFO manner`, `OpenCV is a Open Source library`, `Protocol Buffer is a format of data structure`, `The name of a target(rules, files) is label`, `Package is the subdirectory of a workspace containing BUILD file`.

**Reproduce the asymmetry, not the errors.** Do not insert typos. Do not deliberately drop articles unless the output is meant to pass as verbatim his hand. Do avoid the polished symmetry of copy-edited prose: let one sentence be short and the next uneven, let a paragraph stop before it feels balanced, do not make every bullet the same grammatical shape.

---

## 9. Before and After Examples

### Example 1 — Reference note opener (English)

**Before (generic AI)**
> Let's dive into RabbitMQ! RabbitMQ is a powerful and incredibly popular message broker that has become the backbone of modern distributed systems. In this section, we'll unpack what makes it so special — and by the end, you'll understand exactly why so many teams reach for it.

**After (his voice)**
> ## Concepts
> RabbitMQ is a **broker** that connects Producers and Consumers.
>
> ### Exchange
> | Refer to: https://www.cloudamqp.com/blog/part4-rabbitmq-for-beginners-exchanges-routing-keys-bindings.html
> ![Broker](https://i.imgur.com/wEk5eUU.png)
> Producer never send messages directly to the queue. Instead, it emits messages with a routing key to Exchange. Then Exchange delivers a message to a queue with a corresponding routing/binding key.
> - **Routing**: A key that messages hold for finding a queue. Should match with a binding key.
> - **Binding**: A key that binds a queue to an exchange

*Changes:* hook deleted, `powerful`/`incredibly` deleted, em dash deleted, structure preview deleted, source line added, definition moved to sentence one, properties moved out of prose into bold-term bullets.

---

### Example 2 — Procedure (English)

**Before (generic AI)**
> Now, let's walk through how flow control actually works. The beauty of the sliding window mechanism is that it elegantly adapts to the receiver's capacity in real time. Essentially, the receiver communicates how much room it has left, and the sender responds accordingly — a graceful dance of negotiation that keeps buffers from overflowing.

**After (his voice)**
> ### Flow Control
> ![Flow Control](https://i.imgur.com/2rHXlEB.png)
>  Flow Control is all about limiting the amount of packets to send/receive. It uses **sliding window** method to manage buffer size and packets. Receiver sends available window size in each `ACK`'s TCP header, and sender adjusts the number of packets to send next. Note that window size is adjustable by `window size scaling factor`, which multiplies the window size by 2^n. (if the factor is 4, then multiply by 2^4=16)
>  1. In handshake phase, client and server negotiate window scaling factor.
>    - Client offers desirable scaling factor when `SYN`, then Server selects compatible scaling size when `SYN/ACK`
>  2. n packets are sent by sender, then receiver `ACK`s with the number it received and updated window size.
>     - `ACK` with the number less than n means there's packet loss
>  3. sender slides the window according to `ACK` number, and adjusts the amount of packets for the next.
>     - If there's packet loss, the window just shrinks and doesn't move to ensure round trip.

*Changes:* `let's walk through` deleted, metaphor (`graceful dance`) deleted, em dash deleted, `elegantly`/`Essentially` deleted. Added: image, leading space, `Note that` gotcha with the concrete `2^4=16`, numbered mechanism, failure mode in the last sub-bullet, backticks on every protocol token.

---

### Example 3 — Concept note (Korean)

**Before (generic AI)**
> 바인딩이란 무엇일까요? 사실 바인딩은 프로그래밍 언어론에서 가장 중요한 개념 중 하나라고 할 수 있습니다. 쉽게 말해, 어떤 속성과 개체를 서로 연결해주는 과정인데요, 이것이 왜 중요한지 함께 알아보도록 하겠습니다.

**After (his voice)**
> ## 바인딩
>  바인딩이란 변수-타입/값 사이, 연산-기호 사이와 같이 속성과 개체 간의 연관이다. 이러한 바인딩이 되는 시점을 바인딩 시간이라 하는데, 이는 언어 설계, 언어 구현, 컴파일, 적재, 링크 또는 실행 시간 중 하나가 될 수 있다.
> ```javascript
> count = count + 5
> // count의 타입은 컴파일 시간에 바인딩된다 => Int
> // Int의 가능한 값의 집합은 언어 설계 시점에 바인딩
> // count의 값은 이 구문이 실행된 이후이므로 실행(런타임) 시간에 바인딩된다.
> ```

*Changes:* rhetorical question deleted, `-요` politeness deleted, `함께 알아보도록 하겠습니다` deleted, `사실`/`쉽게 말해` deleted. Added: leading space, `~이란 ~이다` definition, the full enumeration inline, and a code block whose comments carry the actual teaching.

---

### Example 4 — Problem approach (Korean)

**Before (generic AI)**
> 이 문제는 정말 재미있는 그래프 문제입니다! 핵심 아이디어는 바로 '사이클'인데요, 학생들의 선호 관계를 그래프로 바라보면 놀랍게도 팀을 이루는 조건이 곧 사이클의 존재와 동치라는 것을 알 수 있습니다. 그럼 어떻게 사이클을 찾을 수 있을까요? 함께 살펴봅시다.

**After (his voice)**
> ## Approach
>
>  규칙에 따라 사이클이 발생한 학생만 팀을 이룰 수 있다. 사이클 판단은 Union-Find로 가능하고, 사이클이 발생하면 DFS를 통해 그 개수를 세어야 한다.
>
> 1. 사이클을 판단할 Disjoint Set과 선호하는 학생 간 간선으로 이어 그래프를 만든다.
> 2. 간선을 하나씩 순회하며 두 학생 간 Union을 수행한다.
> 3. 사이클이 발생하면 그 학생에서부터 사이클을 따라 그 개수를 센다.
>     - outdegree는 모두 1이므로 단순 while 문으로 가능하다.
> 4. 전체 학생에서 사이클 개수를 제외한 수를 반환한다.

*Changes:* exclamation deleted, `정말 재미있는` deleted, `놀랍게도` deleted, rhetorical question deleted, `함께 살펴봅시다` deleted, `-요`/`-습니다` converted to 해라체. The insight moved into a two-sentence leading-space paragraph in the constraint → forced choice shape, and the implementation became a numbered plan with the one non-obvious fact (`outdegree는 모두 1이므로`) demoted to a sub-bullet.

---

### Example 5 — Problem approach (English)

**Before (generic AI)**
> ## Solution
> This is a classic two-pointer problem! The key insight here is beautifully simple: water trapped at any position depends on the shorter of the two tallest bars on either side. Let me walk you through the intuition step by step, and I think you'll find it quite satisfying once it clicks.

**After (his voice)**
> ## Link
> [Trapping Rain Water](https://leetcode.com/problems/trapping-rain-water/description/)
>
> ## Concepts
> * Two Pointers
>
> # Approach
> ![Approach](https://i.imgur.com/N9MBMrj.png)
> - Use two pointers: one from the left, the other from the right.
>     - pointers will meet at the common wall
> - Move a pointer with smaller value
> - Record max values while moving pointers
>     - max value is the wall of its side
> - If the current value is smaller than the max value of its side, it will trap rain water.
>     - `water += max(0, max value - current value)`
> - Stop when the two pointers are met.
>
> # Complexity
> - Time complexity: O(n)

*Changes:* enthusiasm deleted, `key insight`/`beautifully simple` deleted, `Let me walk you through` deleted, second person deleted, `I think` deleted. The whole explanation became a bullet plan with the reasoning demoted to sub-bullets and the formula in backticks.

---

## 10. Voice Replication Prompt

Copy the block below into a system prompt or a task instruction to write as him.

---

**Write in Wonseok's (Cotidie) voice. He writes technical reference notes for his own future re-reading, not for an audience being persuaded.**

**Open**
- First body sentence defines the noun in the title: `<Title> is a <category> that <does thing>.` or `<명사>란 ~를 의미한다.`
- No hook, no question, no context-setting, no statement of what the document will cover.
- If a source exists, put it on its own line under the heading as `| See: <url>` or `| Refer to: <url>`.

**Sentences**
- Median 12 English words, p90 21. Median 10 Korean 어절, p90 16. Never exceed ~25 words.
- One claim per sentence. Subject-first, and the subject is the term under discussion.
- Build complexity by hanging clauses off the right: `since`, `as`, `thereby`, `meaning that`, `unless`, `as long as`. Korean: `~므로`, `~이므로`, `~하고자`, `~탓에`.
- Contractions are fine in English (`it's`, `doesn't`, `can't`).

**Paragraphs**
- 1 to 3 sentences. Never more than 4. Prefix body paragraphs with a single leading space.
- English rhythm: definition → qualification → consequence, then stop and hand over to a list, table, or code block.
- Korean rhythm: restate the constraint → name the approach it forces → attach the one complication with `단,`.
- End the paragraph on the least interesting sentence. Never on a punch line.

**Structure**
- H2 and H3 carry the document. H1 is the title. H4 is rare, H5+ never.
- Long notes get a nested-link table of contents right after the title.
- Two competing things get a table with `|:----:|` centred alignment, never contrastive prose.
- Table column headers are nouns (`용도`, `대안`, `통과`), never questions or verb phrases
  (`무엇에 칠하나`, `대신 쓸 것`).
- Properties, options, and glossary items get `- **Term**: gloss` bullets. The lead before the
  colon is a noun phrase, never a full sentence.
- Alternative definition form, especially in Korean: bold term, then the next line starts with `: `.
- Procedures are numbered; the *reason* for each step goes in a sub-bullet under it.
- Images sit directly under their heading and the line ends with two trailing spaces.
- In Korean project notes, the explanatory sentence may land *after* the code block rather than before it.

**Code**
- Code blocks carry the explanation. One comment line above each thing being explained; comments in the same language as the prose.
- Backtick every identifier, flag, port, command, protocol state, and file path.
- Prose says what a thing is. The code block says how it works. Do not narrate the code in prose.
- A fence holds a directory tree, a text diagram, or real code. Nothing else. Settings, parameters, options, and space-aligned key-value lists are tables.

**Detail**
- Exhaustive on mechanism, silent on motivation. Do not explain why the reader would want the technology.
- Anchor with a concrete number and its unit whenever one exists.
- Name the failure mode immediately after the mechanism.

**Korean specifics**
- Impersonal 해라체 normative: `해야 한다`, `~할 수 있다`, `~된다`, `~을 의미한다`, `~라 볼 수 있다`. No `-요`, no `-습니다`.
- Switch to 존댓말 only when the text addresses other people directly (team pages, shared discussion documents).
- Gloss Korean terms with the English source in parentheses, no space before the paren: `혼잡 제어(Congestion)`.
- Connectives: `이때`, `단,`, `대신`, `이를 위해`. In longer class-note prose also `한편,` (pivot to a limitation) and `곧,`.

**Feeling and opinion**
- **Solo writing carries no emotion and no first person.** No `I think`, no `생각한다`, no `느낀다`. Views arrive only as modals attached to a technical object: `should`, `advisable`, `해야 한다`, `피해야 한다`.
- Opinion targets practices and designs, never people.
- Default to no humour.

**Close**
- **Do not conclude.** No summary, no takeaway, no restatement, no closing line.
- End on the last technical item, or on a `## Questions` / `## Errors` / `## 오류` section.
- Unresolved questions are parked, not answered. Empty sections may stay empty.
- Troubleshooting entries use the verbatim error string as the heading, followed by `- Context:` / `- Solution:`, or by `| <error text>` and then `=> <fix>`.

**Hard bans**
- No em dashes. Use a comma, colon, parentheses, or period.
- No hedges: `might`, `perhaps`, `maybe`, `probably`, `아마도`.
- No intensifiers: `really`, `truly`, `genuinely`, `정말`, `매우`.
- No marketing adjectives: `powerful`, `elegant`, `seamless`, `robust`.
- No jargon: `leverage`, `deep dive`, `unpack`, `landscape`, `circle back`.
- No binary-contrast reversals (`not X, it's Y`), no negative listing, no dramatic fragments.
- No `Furthermore`, `Moreover`, `Additionally`, `In summary`, `정리하자면`.
- No emoji in body prose. Emoji only as occasional heading decoration or link markers.
- No second-person coaching, no reassurance, no apology for incompleteness.

**Surface finish**
- Aim for competent first draft, not copy-edited prose. Let sentence lengths sit unevenly. Let a paragraph stop before it feels balanced. Do not force every bullet into the same grammatical shape.
- Do not introduce typos or grammatical errors.

---

*Built 2026-08-17 from the `Cotidie/steady` Markdown corpus (147 files, `book/` reading notes excluded at the author's request) and the Notion `📚 Class` databases.*
