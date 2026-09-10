# AI를 이해하는 수학: 통합 복습

## 학습 목표

- Vector·Matrix·Tensor의 Shape를 학습 Cycle과 연결한다.
- MatMul·Transpose·Dot product·Rank·Gradient의 역할을 한 흐름으로 설명한다.
- 작은 AI 프로젝트의 문제 정의부터 평가까지 설계한다.

> **중심 질문**<br>
> 회귀분석부터 Transformer까지 우리는 어떤 수학을, 왜 사용했을까?

## 1. 질문: 서로 다른 수식의 공통 구조는 무엇일까?

정규방정식, Gradient Descent, 신경망, Attention은 서로 다른 기술처럼 보인다. 그러나 모두 데이터를 숫자 구조로 표현하고, Parameter $W$로 Prediction을 만들고, Loss가 줄어들도록 $W$를 찾는 하나의 이야기다.

## 2. 가장 단순한 예: 값에서 Tensor까지

| 표현 | 예 | AI에서의 역할 |
| --- | --- | --- |
| Scalar | $x=3$ | 하나의 Loss, learning rate |
| Vector | $\mathbf{x}=[x_1,x_2,x_3]$ | 한 표본의 feature, 한 token의 embedding |
| Matrix | $X\in\mathbb{R}^{n\times d}$ | 여러 표본, Parameter $W$ |
| Tensor | $X\in\mathbb{R}^{B\times S\times D}$ | batch × sequence × embedding |

<strong>Shape</strong>는 각 축이 무엇을 의미하는지 보여준다. 예를 들어

$$
X\in\mathbb{R}^{32\times512\times768}
$$

은 batch 32개, sequence 길이 512, embedding 차원 768을 뜻할 수 있다. AI 계산에서는 숫자 하나보다 “어떤 축과 어떤 축이 만나는가”를 읽는 능력이 중요하다.

## 3. 수식: 일곱 개의 도구로 전체 흐름 읽기

### ① Matrix Multiplication

$$
X_{n\times d}W_{d\times h}=H_{n\times h}
$$

안쪽 차원 $d$가 같아야 곱할 수 있다. $XW$는 feature를 새로운 표현으로 변환하는 Linear Layer의 핵심 연산이다.

### ② Transpose

$$
K\in\mathbb{R}^{S\times d_k}
\quad\Rightarrow\quad
K^T\in\mathbb{R}^{d_k\times S}
$$

행과 열을 바꾸어 $QK^T$가 모든 Token 쌍의 점수 $S\times S$를 만들게 한다.

### ③ Dot Product

$$
\mathbf{q}\cdot\mathbf{k}=q_1k_1+\cdots+q_dk_d
$$

행렬곱 $QK^T$의 각 원소는 Query와 Key의 dot product다.

### ④ Inverse와 Rank

$$
W=(X^TX)^{-1}X^TY
$$

단순 선형회귀에서는 $X$가 full column rank일 때 closed-form solution을 쓸 수 있었다. rank가 부족하면 pseudoinverse $X^+$ 같은 대안을 사용할 수 있었다.

### ⑤ Derivative와 Gradient

$$
\nabla_W L=
\left[
\frac{\partial L}{\partial w_1},
\ldots,
\frac{\partial L}{\partial w_m}
\right]^T
$$

Gradient는 Parameter가 변할 때 Loss가 어떻게 변하는지 나타낸다.

### ⑥ Backpropagation

$$
\frac{\partial L}{\partial W_1}
{}={}
\frac{\partial L}{\partial H_2}
\frac{\partial H_2}{\partial H_1}
\frac{\partial H_1}{\partial W_1}
$$

연쇄법칙을 재사용해 모든 Layer의 Gradient를 효율적으로 계산한다.

### ⑦ Parameter Update

$$
W\leftarrow W-\eta\nabla_W L
$$

Optimizer가 Gradient를 사용해 다음 $W$를 만든다.

## 4. 문제 해결: 하나의 학습 loop로 통합하기

지금까지의 개념은 다음 loop 안에서 제자리를 찾는다.

$$
\boxed{
X
\xrightarrow{\ f(X;W)\ }
\hat Y
\xrightarrow{\ Y\text{와 비교}\ }
L
\xrightarrow{\ \text{backprop}\ }
\nabla_W L
\xrightarrow{\ \text{optimizer}\ }
W_{new}}
$$

업데이트된 $W_{new}$로 다시 Forward를 수행하며 Loss를 줄인다. Transformer에서도 $X$는 Embedding이 되고, $W$에는 $W_Q,W_K,W_V$와 Feed Forward Network의 Parameter가 포함될 뿐 이 원리는 같다.

| 장면 | 핵심 수식 | 사용한 도구 |
| --- | --- | --- |
| 선형회귀 예측 | $\hat Y=XW$ | Vector, Matrix, Shape, MatMul |
| Closed-form solution | $(X^TX)^{-1}X^TY$ | Transpose, Inverse, Rank |
| 반복 최적화 | $W-\eta\nabla_WL$ | Derivative, Gradient |
| 신경망 학습 | Forward → Loss → Backward → Update | Tensor, Chain Rule |
| Attention | $\operatorname{softmax}(QK^T/\sqrt{d_k})V$ | Dot Product, Transpose, MatMul |

## 통합 미니 프로젝트: P501 반품 위험 예측

> 이 프로젝트가 **AI Basic 과정의 최종 산출물(캡스톤)**이다. 작성 기준은 [과정 안내](templates/ai-basic/lectures_korean/00_ch0_과정_안내.md)의 "과정 완료 기준"을 따른다.

`P501 남색 오버사이즈 코트`의 주문이 반품될 가능성을 예측한다고 하자. 이 프로젝트는 계산보다 **누수 없는 학습 설계**를 완성하는 것이 목표다.

| 단계 | 작성할 것 | 점검 질문 |
| --- | --- | --- |
| 질문 | 발송 시점에 반품 가능성을 예측 | 예측을 어떤 결정에 쓸 것인가? |
| Input $X$ | 주문 시점의 사이즈·가격·고객 이력 | 반품 후에 생긴 정보가 섞이지 않았는가? |
| Target $Y$ | 정해진 기간 안의 반품 여부 | 라벨 기준이 일관적인가? |
| Model | 작은 Logistic regression 또는 MLP | 기준선보다 복잡할 이유가 있는가? |
| Loss | Binary Cross Entropy | 학습 가능한 신호인가? |
| Metric | PR-AUC, Recall, calibration과 운영 비용 | 클래스 불균형과 임계값을 반영하는가? |
| Split | 시간 순서 Train/Validation/Test | 미래 정보가 과거 학습에 들어오지 않았는가? |

최종 산출물은 코드가 아니라 한 장짜리 Model card다. 데이터 범위, Shape, Loss, Metric, 실패 가능성이 큰 하위 집단과 사람이 최종 확인할 지점을 적는다.

## 5. 다음 학습으로 연결

이제 새로운 모델을 만났을 때 이름부터 외우기보다 다음 질문을 던질 수 있다.

1. Input과 Parameter의 shape은 무엇인가?
2. 모델은 $X$와 $W$로 Prediction을 어떻게 만드는가?
3. Prediction과 Target을 어떤 Loss로 비교하는가?
4. Gradient를 어떻게 계산하고 Optimizer가 $W$를 어떻게 바꾸는가?
5. 보지 못한 데이터에서 어떤 Metric으로 평가하는가?

> 회귀분석부터 Transformer까지 모델의 복잡성은 크게 달라졌지만 핵심 질문은 같다.<br>
> **주어진 데이터에서 Loss를 줄이는 Parameter $W$를 어떻게 찾을 것인가?**

## 전체 강의 핵심 정리

- 데이터는 Vector·Matrix·Tensor로 표현되고 Shape가 계산 가능성을 결정한다.
- 모델은 $W$를 사용해 Input을 Prediction으로 변환한다.
- Loss는 Prediction과 Target의 차이를 학습 가능한 신호로 만든다.
- Backpropagation은 Gradient를 계산하고 Optimizer는 $W$를 업데이트한다.
- 좋은 AI는 Training Loss만 낮은 모델이 아니라 새로운 데이터에 일반화하는 모델이다.

## 학습 점검

1. 반품 완료 후에만 알 수 있는 정보를 Input으로 쓰면 어떤 문제가 생기는가?
2. 불균형한 반품 데이터에서 Accuracy만 쓰기 어려운 이유는 무엇인가?
3. 이 프로젝트에서 $W$는 무엇을 학습하고, Metric은 무엇을 판단하는가?

## 참고문헌과 공식 자료

- [Mitchell et al., Model Cards for Model Reporting](https://doi.org/10.1145/3287560.3287596)
- [scikit-learn, Precision-Recall](https://scikit-learn.org/stable/auto_examples/model_selection/plot_precision_recall.html)
