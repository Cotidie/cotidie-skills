# Note skeletons

Three formats, copied from the shapes his corpus actually uses. Pick one, fill it, delete the
guidance comments. `[FIGURE]` marks a slot the figure budget expects you to fill.

---

## A. Reference note (English)

For protocols, algorithms, tools, infrastructure. The long-form format.

```markdown
# <Topic noun>
[FIGURE: the one picture that shows what this thing is]  
| See: <canonical doc url>

- [<Topic noun>](#topic-noun)
  - [Overview](#overview)
  - [<Mechanism>](#mechanism)
  - [Questions](#questions)

## Overview
 <One sentence defining the title noun.> <One or two sentences qualifying it.>
- **<Term>**: <gloss>
  - <what the term implies, or the constraint it carries>
- **<Term>**: <gloss>

## <Mechanism>
### <Sub-mechanism>
[FIGURE: the mechanism, spatially]  
 <1-3 sentences. The rule the figure cannot state.>
1. <step>
   - <why this step is legal, or the failure mode it avoids>
2. <step>
   - <the other branch>
   - <the constraint>

```<lang>
// <comment explaining the line below>
<code>
```

### <Comparison>
| <A> | <B> |
|:---:|:---:|
| <fact> | <fact> |

## Questions
**| <A question you could not answer while writing this>**  
: <answer, or leave the line off entirely>
```

Notes on filling it: the TOC is worth including once the note passes roughly three H2 sections.
`| See:` takes a bare URL and nothing else. Body paragraphs get one leading space. The note ends
at `## Questions` or at the last technical item, with no summary.

Nesting stops at two levels. Level 1 is the claim or step, level 2 is what follows from it. If a
level-1 item needs its own sub-list, it wanted to be an `###` heading instead.

---

## B. Problem note (English or Korean)

For a solved problem: Leetcode, BOJ, a debugging session, an exercise. Under 200 words.

```markdown
## Link
[<Problem title>](<url>)

## Topic
- <Algorithm or concept>

## Approach
[FIGURE: the state or the invariant that makes the solution work]  

 <Korean: 제약을 다시 말한다. 그 제약이 강제하는 접근을 명명한다. 단, 복잡해지는 지점 하나를 붙인다.>

1. <step>
2. <step>
    - <the non-obvious fact that makes this step legal>

## Complexity
- Time complexity: O(n)
```

In English the Approach is a flat bullet list with reasoning in sub-bullets. In Korean it is one
leading-space paragraph in the constraint → forced choice → `단,` shape, then a numbered plan.

---

## C. Project note (Korean)

For an app, a lab, a build. What he learned while making something.

```markdown
# <앱 이름>
[FIGURE: 스크린샷이 있으면 스크린샷, 없으면 구조도]  
 <한 문장으로 이 앱이 무엇을 하는지>. 다음과 같은 기능을 구현해야 한다.
* **<command>**: <동작>
  * <예외 상황>

## 목차
- [배운점](#배운점)
- [오류](#오류)

## 배운점
### **<개념>**
[FIGURE: 개념의 동작 방식]  
```<lang>
// <이 줄이 무엇을 하는지>
<code>
```
<코드 뒤에 오는 1-2문장 설명>

* **<개념>**
: <정의. 이때 ~하므로 ~해야 한다.>

## 오류
### **<에러 문자열 그대로>**
 <무엇이 문제였는지 한 문장>
| ```<에러 메시지 원문>```
=> <해결 방법>
```

The explanatory sentence lands **after** the code block in this format, not before. `## 오류`
entries are titled with the verbatim error string.
