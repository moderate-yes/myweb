# How Derivatives Show the Direction of Loss

## 학습 목표

Loss를 줄이려면 어느 방향으로 Parameter를 움직여야 하는지 알아야 한다. 이 장은 기울기와 편미분에서 gradient와 연쇄법칙으로, 그리고 backpropagation이 그것을 신경망 전체로 확장하는 방식까지 다룬다.

이 장을 마치면 다음을 할 수 있다.

- derivative와 partial derivative를 구분한다.
- gradient vector의 방향과 크기를 해석한다.
- chain rule이 neural network의 backpropagation에 사용되는 이유를 설명한다.

<div class="learning-path" role="img" aria-label="기울기에서 편미분 gradient 연쇄법칙 backpropagation으로 이어지는 경로">
  <span>Slope</span><b>→</b><span>Partial</span><b>→</b><span>Gradient</span><b>→</b><span>Chain Rule</span><b>→</b><span>Backprop</span>
</div>

> **AI Basic 연계**: AI Basic 4~5장(Gradient Descent·Backpropagation)을 읽었다면 이 장을 함께 본다. gradient와 chain rule을 작은 예로 직접 계산한다.

## 1. 가장 단순한 예: 한 개의 가중치

$$
L(w)=(w-3)^2
$$

미분하면

$$
\frac{dL}{dw}=2(w-3)
$$

$w=5$에서는 derivative가 4다. $w$가 증가할수록 Loss가 증가하므로 반대 방향인 작은 $w$ 쪽으로 이동해야 한다.

$$
w_{new}=w-\eta\frac{dL}{dw}
$$

## 2. Parameter가 여러 개라면

$$
L(w_1,w_2)=(w_1-2)^2+2(w_2+1)^2
$$

각 변수만 바뀐다고 보고 partial derivative를 계산한다.

$$
\frac{\partial L}{\partial w_1}=2(w_1-2),\qquad
\frac{\partial L}{\partial w_2}=4(w_2+1)
$$

이를 한 벡터로 모은 것이 gradient다.

$$
\nabla L=
\begin{bmatrix}
\partial L/\partial w_1\\
\partial L/\partial w_2
\end{bmatrix}
$$

<div class="comparison-cards" role="img" aria-label="derivative partial derivative gradient의 차이">
  <section class="concept-card"><h3>Derivative</h3><p>입력 하나에 대한 순간 변화율</p><small>$dL/dw$</small></section>
  <section class="concept-card"><h3>Partial derivative</h3><p>다른 변수를 고정하고 하나만 변화</p><small>$\partial L/\partial w_i$</small></section>
  <section class="concept-card"><h3>Gradient</h3><p>모든 partial derivative를 모은 벡터</p><small>가장 빠른 증가 방향</small></section>
</div>

## 3. Chain rule: 계산이 여러 단계를 지날 때

예측과 Loss가 다음처럼 이어진다고 하자.

$$
z=wx+b,\qquad \hat y=\sigma(z),\qquad L=L(y,\hat y)
$$

$w$가 Loss에 미치는 영향은 중간 단계를 곱해 연결한다.

$$
\frac{\partial L}{\partial w}
=\frac{\partial L}{\partial \hat y}
\frac{\partial \hat y}{\partial z}
\frac{\partial z}{\partial w}
$$

<div class="operations-flow" role="img" aria-label="forward 계산과 backward 미분이 반대 방향으로 흐르는 구조">
  <div><strong>Forward</strong><span>$x\rightarrow z\rightarrow\hat y\rightarrow L$</span></div>
  <div class="flow-highlight"><strong>Local derivative</strong><span>각 연산은 자신의 변화율을 저장</span></div>
  <div><strong>Backward</strong><span>$\partial L/\partial\hat y\rightarrow\partial L/\partial z\rightarrow\partial L/\partial w$</span></div>
</div>

Backpropagation은 새로운 미분 규칙이 아니라, computation graph에서 chain rule을 효율적으로 재사용하는 알고리즘이다.

## 4. Matrix calculus를 Shape로 읽기

$$
\hat Y=XW
$$

$X$가 $(n,d)$, $W$가 $(d,k)$이면 $\hat Y$는 $(n,k)$다. Loss가 scalar일 때 gradient $\nabla_WL$은 $W$와 같은 $(d,k)$ Shape를 가져야 한다.

| 대상 | Shape | Gradient Shape |
|---|---|---|
| $W$ | $(d,k)$ | $(d,k)$ |
| $b$ | $(k,)$ | $(k,)$ |
| $X$ | $(n,d)$ | $(n,d)$ |

Shape 확인은 matrix derivative의 많은 전치 오류를 잡아 준다.

## 5. 문제 발생: derivative가 0이면 최솟값인가

Derivative가 0인 점은 minimum, maximum, saddle point 모두 가능하다. 두 번째 derivative 또는 Hessian의 곡률을 함께 봐야 한다.

또한 sigmoid처럼 입력 절댓값이 클 때 derivative가 0에 가까워지는 함수는 gradient vanishing을 만들 수 있다. 반대로 깊은 곱셈에서 derivative가 커지면 exploding gradient가 발생할 수 있다.

### Python으로 해석적 미분과 수치 미분 비교하기

수치 미분은 작은 간격 앞뒤의 Loss 차이로 기울기를 근사한다. 해석적으로 구한 Gradient와 가까운지 비교하면 미분 구현을 점검할 수 있다.

```python
def loss(w):
    return (w - 3) ** 2

w = 2.0
epsilon = 1e-5
analytic = 2 * (w - 3)
numeric = (loss(w + epsilon) - loss(w - epsilon)) / (2 * epsilon)

print(f"analytic gradient = {analytic:.6f}")
print(f"numeric gradient  = {numeric:.6f}")
```

```output
analytic gradient = -2.000000
numeric gradient  = -2.000000
```

## 짧은 활동

$L(w)=(2w-6)^2$에 대해 답하자.

1. $dL/dw$를 계산하자.
2. $w=1$일 때 derivative의 부호는 무엇인가?
3. Loss를 줄이려면 $w$를 어느 방향으로 움직여야 하는가?

<details><summary>짧은 활동 풀이</summary>

1. $dL/dw=4(2w-6)=8w-24$다.
2. $w=1$이면 $-16$으로 음수다.
3. Gradient Descent는 derivative의 반대 방향으로 이동하므로 $w$를 증가시킨다.

</details>

## 이 장의 핵심

- derivative는 입력 변화에 따른 출력의 순간 변화율이다.
- gradient는 모든 Parameter 방향의 변화율을 모은 벡터다.
- backpropagation은 chain rule을 computation graph에서 재사용한다.
- gradient Shape는 원래 Parameter Shape와 같아야 한다.

## 학습 점검

1. derivative, partial derivative, gradient의 차이는 무엇인가?
2. backpropagation은 새로운 미분 규칙인가? 아니라면 무엇인가?
3. derivative가 0인 점이 항상 최솟값은 아닌 이유는 무엇인가?

<details><summary>정답과 해설 보기</summary>

1. derivative는 입력 하나에 대한 순간 변화율, partial derivative는 다른 변수를 고정하고 하나만 변화시킨 변화율, gradient는 모든 partial derivative를 모아 가장 빠른 증가 방향을 가리키는 벡터다.
2. 아니다. computation graph에서 chain rule을 효율적으로 재사용하는 알고리즘이다.
3. minimum, maximum, saddle point 모두 derivative가 0일 수 있으므로 2차 도함수 또는 Hessian의 곡률을 함께 봐야 한다.

</details>

## 참고문헌과 공식 자료

1. Goodfellow, I., Bengio, Y., & Courville, A. [Numerical Computation](https://www.deeplearningbook.org/contents/numerical.html). *Deep Learning*, Chapter 4.
2. Stanford CS229. [Course Materials: Linear Algebra, Multivariable Calculus, and Backpropagation](https://cs229.stanford.edu/syllabus-spring2021.html).

## 다음 장

> Gradient를 알았다면, 얼마나 크게 움직이고 어떤 제약을 지켜야 할까?
