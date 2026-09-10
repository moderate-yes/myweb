# 학습한 AI는 정말 좋은가

## 학습 목표

- Train·Validation·Test의 역할을 구분한다.
- Loss와 Metric을 목적에 맞게 선택한다.
- 데이터 누설, 분포 변화와 subgroup 성능을 점검한다.

> **중심 질문**<br>
> Training Loss가 낮으면 좋은 AI라고 말할 수 있을까?

## 1. 질문: 연습문제를 외운 학생은 실력이 좋은가?

학습에 사용한 문제의 답을 외우면 연습 점수는 높다. 그러나 처음 보는 문제를 풀지 못한다면 지식을 일반화했다고 할 수 없다. AI도 마찬가지다. 보지 못한 데이터에서 잘 작동하는 능력을 <strong>Generalization(일반화)</strong>이라고 한다.

## 2. 가장 단순한 예: 데이터를 역할별로 나누기

1,000개의 표본이 있다면 예를 들어 다음처럼 나눌 수 있다.

| 데이터 | 예시 비율 | 역할 |
| --- | ---: | --- |
| Train | 70% | Loss를 줄이며 $W$ 학습 |
| Validation | 15% | 모델·hyperparameter 선택, 과적합 감시 |
| Test | 15% | 모든 선택이 끝난 뒤 최종 성능 평가 |

Test 결과를 보고 반복해서 모델을 고치면 Test도 사실상 Validation처럼 사용한 셈이다. 공정한 최종 평가를 위해 Test는 마지막까지 분리한다. 시계열이나 사용자 데이터처럼 순서·그룹이 중요한 경우에는 무작위 분할이 누수(data leakage)를 만들 수 있으므로 문제에 맞는 분할법이 필요하다.

## 3. 수식: Loss와 Metric은 목적이 다르다

<strong>Loss</strong>는 Gradient를 계산해 모델을 학습시키는 함수다.

$$
W_{t+1}=W_t-\eta\nabla_W L_{train}(W_t)
$$

<strong>Metric</strong>은 모델의 성능을 사람이 해석하고 비교하기 위한 기준이다. 둘은 같을 수도 있지만 반드시 같지는 않다. 분류 모델은 differentiable한 cross entropy로 학습하면서 Accuracy나 F1으로 보고할 수 있다.

| 문제 | 자주 쓰는 Loss | 평가 Metric 예시 |
| --- | --- | --- |
| Regression | MSE, MAE | MAE, RMSE, $R^2$ |
| Classification | Cross Entropy | Accuracy, Precision, Recall, F1, AUROC |
| Language Model | Token Cross Entropy | Perplexity, task 성공률, 사람 평가, model-based 평가 |

예를 들어 precision과 recall은 다음과 같다.

$$
\operatorname{Precision}=\frac{TP}{TP+FP},\qquad
\operatorname{Recall}=\frac{TP}{TP+FN}
$$

어떤 Metric이 중요한지는 오탐과 미탐의 비용에 따라 달라진다. 생성형 AI는 정답이 하나가 아니므로 정확성, 유용성, 안전성 등을 단일 점수만으로 충분히 판단하기 어렵다.

## 4. 문제 발생: 숫자만 외우면 전체 학습 구조를 놓친다

Train Loss는 내려가는데 Validation Loss가 올라가면 모델이 학습 데이터에 과도하게 맞춰지는 <strong>Overfitting</strong> 신호일 수 있다. 반대로 Train과 Validation 성능이 모두 낮으면 모델이나 학습이 충분하지 않은 <strong>Underfitting</strong>일 수 있다.

평가지표 이름만 외우는 것보다 데이터 shape, $XW$, Gradient, Attention이 하나의 학습 흐름에서 어떤 역할을 했는지 연결하는 편이 중요하다.

## 5. 다음 장 연결

> **회귀분석부터 Transformer와 평가까지 실제로 사용한 수학은 어떻게 연결될까?**

마지막 장에서는 Vector·Matrix·Tensor, Shape, MatMul, Transpose, Dot Product, Inverse·Rank, Gradient를 전체 학습 cycle 안에서 다시 묶는다.

## 핵심 정리

- Train은 학습, Validation은 선택, Test는 최종 평가에 사용한다.
- Loss는 학습 방향을 만들고 Metric은 원하는 성능을 해석한다.
- 낮은 Training Loss만으로 좋은 AI라고 할 수 없다.
- 최종 목표는 보지 못한 데이터에서도 잘 작동하는 Generalization이다.

## 짧은 활동

같은 모델의 `Train loss↓ / Validation loss↑` 그래프를 그리고 원인을 추정한다. 전체 정확도가 같아도 사이즈·카테고리별 성능이 다른 두 모델 중 무엇을 배포할지 기준을 정한다.

## 학습 점검

1. Test set을 반복해서 보며 모델을 고르면 왜 Test가 Validation처럼 변하는가?
2. Cross Entropy loss가 낮아졌어도 실제 서비스 지표가 나빠질 수 있는 이유는 무엇인가?

## 참고문헌과 공식 자료

- [scikit-learn, Cross-validation](https://scikit-learn.org/stable/modules/cross_validation.html)
- [Google, Rules of Machine Learning](https://developers.google.com/machine-learning/guides/rules-of-ml)
