# AI를 이해하려면 어떤 수학이 필요한가

제공된 데이터사이언스 수학·통계·머신러닝 평가 자료에는 벡터, 행렬, 최소제곱, 미분, 확률분포, 최대우도, 분류 평가가 한꺼번에 등장한다. 이 과정은 문제 풀이 순서를 외우는 대신, 각 수학 도구가 AI 학습 과정의 어느 위치에서 필요한지 연결한다.

<div class="learning-path" role="img" aria-label="데이터 표현에서 모델 평가까지 이어지는 AI 수학 학습 경로">
  <span>벡터·행렬</span><b>→</b><span>예측</span><b>→</b><span>Loss</span><b>→</b><span>미분·최적화</span><b>→</b><span>확률·평가</span>
</div>

> **이 장의 중심 질문**<br>
> AI 수식은 서로 달라 보이는데, 어떤 공통 구조로 읽을 수 있을까?

> **AI Basic 연계**: AI Basic 1장을 읽었다면 이 장을 함께 본다. "학습 = Loss를 줄이는 Parameter 찾기"를 표현·예측·비교·업데이트·평가의 다섯 단계로 펼친다.

## 학습 목표

- AI 학습을 표현·예측·비교·업데이트·평가의 흐름으로 설명한다.
- Scalar, Vector, Matrix, Tensor의 차이를 Shape와 함께 읽는다.
- 선형대수·미분·확률이 각각 담당하는 역할을 구분한다.

## 핵심 용어

- **Parameter**: 데이터로부터 조정되는 모델 내부의 값
- **Prediction**: 모델이 입력으로부터 계산한 출력
- **Loss**: 예측과 정답의 차이를 하나의 수치로 모은 값
- **Gradient**: Parameter가 변할 때 Loss가 가장 빠르게 증가하는 방향
- **Metric**: 학습 결과를 사람이 판단하기 위한 평가 기준

## 1. 가장 단순한 예: 코트 판매량 예측

P501 남색 오버사이즈 코트를 다음 세 숫자로 표현한다고 하자.

$$
\mathbf{x}=
\begin{bmatrix}
\text{가격 정규화} & \text{최근 조회 비율} & \text{재고 비율}
\end{bmatrix}
$$

가중치 벡터 $\mathbf{w}$와 내적하면 판매량 예측값을 만들 수 있다.

$$
\hat y=\mathbf{x}\cdot\mathbf{w}+b
$$

실제 판매량 $y$와 비교해 제곱오차를 계산한다.

$$
L=(y-\hat y)^2
$$

AI 학습은 $L$이 작아지도록 $\mathbf{w}$와 $b$를 바꾸는 과정이다.

## 2. 값의 모양: Scalar에서 Tensor까지

| 표현 | Shape 예 | AI에서의 역할 |
|---|---|---|
| Scalar | `()` | 하나의 Loss, learning rate |
| Vector | `(3,)` | 한 상품의 특징, 한 token의 embedding |
| Matrix | `(100, 3)` | 100개 상품 × 3개 특징 |
| Tensor | `(32, 128, 768)` | batch × sequence × embedding |

<div class="comparison-cards" role="img" aria-label="선형대수 미분 확률이 AI에서 담당하는 역할 비교">
  <section class="concept-card"><span class="concept-icon">📐</span><h3>선형대수</h3><p>데이터와 Parameter를 배열로 표현하고 변환한다.</p><small>Vector · Matrix · Tensor</small></section>
  <section class="concept-card"><span class="concept-icon">⛰️</span><h3>미분·최적화</h3><p>Loss를 줄이기 위해 어느 방향으로 움직일지 계산한다.</p><small>Derivative · Gradient</small></section>
  <section class="concept-card"><span class="concept-icon">🎲</span><h3>확률·통계</h3><p>불확실한 관측과 모델 출력을 해석하고 평가한다.</p><small>Distribution · Likelihood</small></section>
</div>

## 3. 하나의 AI 학습 loop로 읽기

<div class="operations-flow" role="img" aria-label="입력에서 평가까지 이어지는 AI 학습 루프">
  <div><strong>표현</strong><span>$X$, $W$의 Shape를 정한다.</span></div>
  <div><strong>예측</strong><span>$\hat Y=f(X;W)$를 계산한다.</span></div>
  <div class="flow-highlight"><strong>Loss</strong><span>$Y$와 $\hat Y$를 비교한다.</span></div>
  <div><strong>업데이트</strong><span>$W\leftarrow W-\eta\nabla_WL$</span></div>
  <div><strong>평가</strong><span>새 데이터에서 Metric을 확인한다.</span></div>
</div>

| 질문 | 필요한 수학 |
|---|---|
| 두 상품은 얼마나 비슷한가? | Vector, norm, dot product, cosine similarity |
| 여러 특징으로 판매량을 예측할 수 있는가? | Matrix multiplication, least squares |
| Loss를 줄이려면 Parameter를 어떻게 바꿀까? | Derivative, gradient, optimization |
| 예측 확률 0.8은 무엇을 뜻하는가? | Probability distribution, likelihood |
| 모델 A가 모델 B보다 좋은가? | Sampling, metric, uncertainty |

## 4. 문제 발생: 수식을 계산할 수 있으면 이해한 것일까?

수식을 계산하는 능력과 모델을 해석하는 능력은 다르다. 다음 세 질문을 함께 물어야 한다.

1. 각 기호는 현실의 무엇을 나타내는가?
2. Shape와 계산 조건이 맞는가?
3. 계산 결과가 실제 의사결정에서 무엇을 의미하는가?

예를 들어 cosine similarity가 높다는 것은 두 벡터의 방향이 비슷하다는 뜻이지, 두 옷이 인간에게 반드시 같은 스타일로 보인다는 뜻은 아니다.

## 짧은 활동

다음 AI 장면에 필요한 수학을 연결해 보자.

| AI 장면 | 입력 | 출력 | 필요한 수학 |
|---|---|---|---|
| 이미지 검색 | 상품 이미지 | 유사 상품 순위 |  |
| 수요 예측 | 가격·재고·노출 | 다음 주 판매량 |  |
| 반품 분류 | 주문·상품 특징 | 반품 확률 |  |

## 이 장의 핵심

- 선형대수는 데이터를 계산 가능한 구조로 표현한다.
- 미분과 최적화는 Loss를 줄이는 Parameter의 이동 방향을 만든다.
- 확률과 통계는 불확실한 출력과 평가 결과를 해석한다.
- AI 수식은 대부분 `표현 → 예측 → Loss → 업데이트 → 평가` 안에서 읽을 수 있다.

## 학습 점검

1. Matrix의 Shape를 읽는 것이 중요한 이유는 무엇인가?
2. Loss와 Metric의 역할은 어떻게 다른가?
3. Gradient는 Parameter 업데이트에 어떻게 사용되는가?

<details><summary>정답과 해설 보기</summary>

1. 행과 열의 의미, 곱셈 가능 조건, 출력 Shape를 결정하기 때문이다.
2. Loss는 학습 과정에서 Parameter를 바꾸는 신호이고, Metric은 모델을 사람이 평가하는 기준이다.
3. 보통 Gradient의 반대 방향으로 learning rate만큼 이동해 Loss를 줄인다.

</details>

## 참고문헌과 공식 자료

1. Goodfellow, I., Bengio, Y., & Courville, A. (2016). [Deep Learning: Part I, Applied Math and Machine Learning Basics](https://www.deeplearningbook.org/contents/TOC.html). MIT Press.
2. MIT OpenCourseWare. [18.06SC Linear Algebra](https://ocw.mit.edu/courses/18-06sc-linear-algebra-fall-2011/).

## 다음 장

> 데이터가 Vector라면, 두 데이터가 비슷하다는 것은 정확히 무엇을 뜻할까?

