# AI의 학습이란 무엇인가

## 학습 목표

- Input, Target, Prediction과 Parameter를 구분한다.
- 여러 Error를 하나의 Loss로 모으는 이유를 설명한다.
- 이 과정에서 다루는 학습의 핵심 문장을 자신의 말로 표현한다.

> **이 강의의 중심 문장**<br>
> 학습은 <strong>Loss를 줄이는 Parameter $W$를 찾는 과정</strong>이다.

## 1. 질문: AI가 학습할 때 무엇이 달라질까?

AI가 새로운 지식을 파일처럼 저장한다고 생각하기 쉽다. 그러나 모델 안에서 실제로 바뀌는 것은 수많은 <strong>Parameter(파라미터)</strong>다. 가장 단순한 회귀분석에서 이 생각을 시작해 보자.

## 2. 가장 단순한 예: 키로 몸무게 예측하기

| 키 $x$ (cm) | 실제 몸무게 $y$ (kg) |
| ---: | ---: |
| 160 | 52 |
| 170 | 65 |
| 180 | 78 |

직선 하나로 몸무게를 예측한다면 다음과 같이 쓸 수 있다.

$$
\hat y = wx+b
$$

$x$는 입력, $y$는 실제값, $\hat y$는 예측값이다. $w$는 키가 1만큼 변할 때 예측이 얼마나 변하는지를 정하고, $b$는 기준점을 정한다. 이 모델이 학습해야 하는 Parameter는 $w$와 $b$다.

예를 들어 $w=1.3$, $b=-156$이면 키 170cm의 예측은 65kg이다. 하지만 다른 사람들에게도 잘 맞는지는 모든 예측을 실제값과 비교해야 알 수 있다.

## 3. 수식: 오차를 하나의 Loss로 모으기

한 사람의 오차는 $y_i-\hat y_i$다. 오차의 부호가 서로 상쇄되지 않도록 제곱하고 평균을 내면 <strong>평균제곱오차(MSE)</strong>가 된다.

$$
L(w,b)=\frac{1}{n}\sum_{i=1}^{n}\left(y_i-(wx_i+b)\right)^2
$$

여기서 $L$은 여러 예측이 전체적으로 얼마나 틀렸는지를 나타내는 <strong>Loss Function</strong>이다. 학습의 목표는 다음 한 줄로 표현된다.

$$
\boxed{(w^{\star},b^{\star})=\arg\min_{w,b} L(w,b)}
$$

즉, 좋은 모델을 만든다는 말은 데이터에 대한 Loss가 작은 Parameter를 찾는다는 뜻이다. 이 관점은 선형회귀뿐 아니라 신경망과 Transformer에도 그대로 이어진다.

## 4. 문제 발생: 가장 좋은 $W$를 어떻게 찾을까?

$w$와 $b$를 임의로 계속 대입해 볼 수도 있지만 가능한 값은 사실상 무한하다. Parameter가 두 개뿐인 지금도 비효율적인데, 수십억 개라면 모든 조합을 시험할 수 없다.

먼저 질문을 더 단순하게 만들어 보자. 모델이 선형이고 Loss가 제곱오차라면, 최적의 Parameter를 반복 없이 수학적으로 계산할 수 있을까?

## 5. 다음 장 연결

> **최적의 $W$를 공식 하나로 한 번에 구할 수 있을까?**

다음 장에서는 여러 데이터를 행렬 $X$와 $Y$로 묶고, 최소제곱법의 closed-form solution을 유도한다.

## 핵심 정리

- Input $X$가 모델을 지나 Prediction $\hat Y$가 된다.
- Prediction과 Target $Y$의 차이를 Loss로 측정한다.
- 학습되는 것은 규칙 문장이 아니라 Parameter $W$와 $b$다.
- <strong>학습 = Loss를 줄이는 Parameter $W$를 찾는 과정</strong>이다.

> 이 문장은 지도학습과 신경망을 이해하기 위한 중심축이다. 규칙 기반 시스템, 검색 시스템이나 모든 AI를 이 문장 하나로 정의하는 것은 아니다.

## 짧은 활동

세 개의 키–몸무게 쌍을 만들고 서로 다른 $w,b$ 두 쌍으로 예측한다. 각 예측의 제곱오차를 직접 더해 어느 Parameter가 더 나은지 판단한다.

## 학습 점검

1. Error와 Loss는 어떻게 다른가?
2. 데이터가 고정돼 있을 때 학습 과정에서 바뀌는 것은 무엇인가?

<details><summary>정답과 해설 보기</summary>

1. Error는 개별 예측의 차이이고, Loss는 학습을 위해 여러 Error를 하나의 값으로 요약한다.
2. 모델의 Parameter $W,b$가 바뀐다.

</details>

## 참고문헌과 공식 자료

- [Deep Learning, Chapter 5: Machine Learning Basics](https://www.deeplearningbook.org/contents/ml.html)
- [scikit-learn, Mean squared error](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.mean_squared_error.html)
