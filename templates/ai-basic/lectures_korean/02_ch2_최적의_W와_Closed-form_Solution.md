# 최적의 W를 한 번에 찾을 수 있을까

## 학습 목표

- 여러 관측치를 $\hat Y=XW$로 표현한다.
- 최소제곱의 목적과 정규방정식이 나오는 흐름을 설명한다.
- closed-form solution이 성립하는 조건을 말한다.

> **수식 선택 학습**: 유도 과정보다 의미가 중요하다. 행렬곱과 역행렬 계산은 AI Math 3–4장에서 천천히 연습할 수 있다.

> **중심 질문**<br>
> 반복해서 값을 바꾸지 않고 Loss가 가장 작은 $W$를 직접 계산할 수 있을까?

## 1. 질문: 여러 개의 식을 한꺼번에 풀 수 있을까?

1장에서는 한 사람의 예측을 $\hat y=wx+b$로 나타냈다. 데이터가 수천 개가 되어도 같은 식을 하나씩 쓰기보다는 행렬 하나로 묶으면 계산 구조가 선명해진다.

## 2. 가장 단순한 예: 두 특성으로 점수 예측하기

공부 시간과 수면 시간으로 시험 점수를 예측한다고 하자. 절편까지 $W$에 포함하려고 입력의 마지막 열에 1을 둔다.

$$
X=
\begin{bmatrix}
2&7&1\\
4&6&1\\
6&5&1
\end{bmatrix},\quad
W=
\begin{bmatrix}
w_1\\w_2\\b
\end{bmatrix},\quad
Y=
\begin{bmatrix}
60\\75\\88
\end{bmatrix}
$$

모든 예측은 다음 한 줄로 계산된다.

$$
\hat Y=XW
$$

$X$의 shape은 $3\times3$, $W$는 $3\times1$이므로 결과 $\hat Y$는 $3\times1$이다.

## 3. 수식: 최소제곱해 유도하기

제곱오차의 합을 최소화하는 문제는 다음과 같다.

$$
L(W)=\|Y-XW\|_2^2
$$

$W$에 대해 미분하고 기울기가 0인 지점을 찾으면,

$$
\nabla_W L=-2X^T(Y-XW)=0
$$

따라서 <strong>정규방정식(normal equation)</strong>을 얻는다.

$$
X^TXW=X^TY
$$

$X^TX$가 역행렬을 가질 때 양변에 $(X^TX)^{-1}$을 곱하면,

$$
\boxed{W=(X^TX)^{-1}X^TY}
$$

가 된다. 반복 업데이트 없이 유한한 연산으로 표현된 이런 답을 <strong>closed-form solution(폐쇄형 해)</strong>이라고 한다.

## 4. 문제 발생: 역행렬은 항상 존재할까?

이 공식에는 숨은 조건이 있다. $X$의 열들이 선형독립이어야 $X^TX$가 full rank이고 역행렬을 가진다. 예를 들어 두 특성이 완전히 같은 정보를 담으면 열 하나가 다른 열의 배수가 되어 역행렬이 사라질 수 있다.

또 역행렬이 존재하더라도 특성이 매우 많으면 계산과 메모리 비용이 커지고, 수치적으로 불안정할 수 있다. 무엇보다 신경망처럼 모델이 복잡한 비선형 함수가 되면 같은 방식의 간단한 공식 자체를 일반적으로 만들 수 없다.

## 5. 다음 장 연결

> **$X^TX$가 singular하거나 모델이 비선형이면 무엇이 달라질까?**

다음 장에서는 rank와 역행렬의 조건, pseudoinverse라는 대안, 그리고 Gradient Descent가 필요한 더 본질적인 이유를 구분한다.

## 핵심 정리

- 여러 예측은 $\hat Y=XW$로 한꺼번에 표현할 수 있다.
- 선형 모델과 제곱오차의 조합은 최적 $W$의 closed-form solution을 허용한다.
- $W=(X^TX)^{-1}X^TY$는 $X^TX$가 invertible일 때 사용할 수 있다.
- 단순한 모델에서는 Loss가 가장 작은 $W$를 직접 계산할 수도 있다.

## 짧은 활동

$X$의 행·열과 $W,Y$의 Shape를 적고, $XW$가 가능한지 확인한다. 특성 두 개가 완전히 같은 경우 $X^TX$에 어떤 문제가 생길지 말해 본다.

## 학습 점검

1. $X^TX$가 invertible이어야 하는 이유는 무엇인가?
2. 정규방정식의 해가 ‘모든 AI의 공식’이 아닌 이유는 무엇인가?

## 참고문헌과 공식 자료

- [Stanford CS229, Linear Regression](https://cs229.stanford.edu/notes2022fall/cs229-notes1.pdf)
- [NumPy, numpy.linalg.lstsq](https://numpy.org/doc/stable/reference/generated/numpy.linalg.lstsq.html)
