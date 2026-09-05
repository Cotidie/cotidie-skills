# PACES 방법론

출처: Jason Corso, "How to Read Conference Papers" (Medium, 2024).
https://medium.com/@jasoncorso/how-to-read-conference-papers-fa78c75f78aa
Corso는 미시간대 교수이고 CVPR area chair를 여러 번 맡았다. 20년간 학생들에게 이 방법을 가르쳤다.

## 전제

컨퍼런스 논문은 공식(formula)을 따른다. 기여는 보통 하나다. 서론 마지막 문단에 셋을
나열해도 그렇다. PACES는 그 하나를 문헌 맥락 안에서 가장 빨리 꺼내는 도구다. 한 편에
한 시간 이내. 읽을지 말지를 정하고, 나중에 떠올릴 수 있게 하는 첫 독해용이다. 메커니즘의
세부를 알아야 하면 그때 더 읽는다.

## 다섯 질문

### Problem

논문이 다루는 주 문제. 분야와 문헌 안에서 가능한 한 선명하게. "object detection 논문인가,
translation 논문인가." 여러 문제에 적용되는 표현(representation)을 제안하는 논문이면 문제
서술도 그만큼 추상적으로 쓴다: "space-time video representations".

### Approach

문제를 푸는 주 기법. 2~3문장. 재현할 만큼의 세부는 없어도 된다. 더 길면 PACES가 아니다.
더 짧으면 뒤의 세 질문에 답할 만큼 이해하지 못한 것이다.

### Claim

저자가 생각하는, 분야에 대한 고유한 기여. 가장 중요한 질문. 한 문장. 저자가 말하는 분야
맥락과 내가 아는 분야 맥락 안에서 소화한다. 자기 말로 쓴다. 인용이 아니다(모든 답이 그렇다).

### Evaluation

어떻게 평가했나. 데이터셋, 베이스라인, 평가 설정. 눈에 띄는 성공이나 red flag, 평가가 논문
방향과 맞는지. 몇 문장. 그림과 표를 복붙하지 않는다. 이론 논문이면 평가가 없을 수 있다고
적는다. 핵심 질문 하나: 내가 평가했다면 같게 했을까, 다르게 했을까. 이 질문은 방법을 깊이
이해하지 않아도 답할 수 있다.

### Substantiation

평가가 Claim을 실제로 받치는가. 기여 한 줄과, 그것을 논증(이론)이나 평가(실증)가 어떻게
받치는지 한 줄. Yes면 기억에 잘 남는다. No면 다시 볼 논문이 아니다.

## 읽기 순서

Corso의 순서:

1. Abstract, Introduction
2. Evaluation(Experiments), Discussion, Conclusion. 여기까지 오면 대부분 답할 수 있다.
3. Method와 Related Work를 skim.

이 스킬은 3에서 Method를 정독으로 바꾼다. 방법 다이어그램을 그려야 하고, LLM에게 열 쪽
읽기는 비용이 아니기 때문이다. Related Work는 skim 그대로.

답의 granularity는 분야 익숙도에 따른다. 주제를 깊이 파는 중이면 같은 논문을 여러 번 읽어
답을 깊게 한다.

## Corso의 예시: Grounded Video Description (CVPR 2019)

- **PROBLEM**: Video captioning with an emphasis on grounding caption text in video pixels.
- **APPROACH**: In a fully supervised manner, connects groundable language terms like a set
  of object classes to embedding-based region features, which are used by an LSTM-based
  language generation module. The loss function drives the attention module to learn how to
  emphasize groundable regions. To enable the full grounding supervision, a new dataset with
  sparse object grounding is introduced.
- **CLAIM**: The work makes video captioning more robust and reliable by explicitly
  incorporating an object-grounding mechanism into the learned model.
- **EVALUATION**: The introduced ActivityNet-Entities dataset is the primary evaluation
  medium. The work tests against SOTA video captioning methods and runs an ablation on the
  grounding-and-attention mechanisms; both use standard language generation metrics, a new
  localization-accuracy evaluation for grounded terms, and a human assessment of the text.
  For robustness, it also tests on the image-based Flickr30K Entities.
- **SUBSTANTIATION**: Yes, the evaluation sufficiently demonstrates the potential value of
  adding grounding mechanisms in language generation from video.

길이 감각: Problem 한 줄, Approach 세 문장, Claim 한 문장, Evaluation 네 문장,
Substantiation 한 문장.

## LLM 자동화에 대한 Corso의 단서

자동 PACES는 읽을 논문을 고르고, 읽기 시작할 때의 맥락을 주는 데 쓴다. 독자의 맥락과 최신
문헌을 모른다. 그래서 이 스킬의 답은 짧게, 판단(Verdict, "나라면")은 명시적으로 쓴다.
사용자가 자기 맥락을 얹기 쉽도록.
