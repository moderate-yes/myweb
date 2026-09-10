# Gradient Descent와 Optimizer

## 학습 목표

- Gradient의 부호와 크기를 update 방향과 연결한다.
- Learning rate가 너무 크거나 작을 때를 비교한다.
- Backpropagation과 Optimizer의 역할을 구분한다.

> **중심 질문**<br>
> 정답 $W$를 모르는 상태에서 Loss가 작은 $W$를 어떻게 찾아갈까?

## 1. 질문: 현재 값에서 무엇을 알 수 있을까?

최적의 $W$를 한 번에 계산하지 못해도 현재 $W$에서 Loss가 어느 방향으로 가장 빠르게 커지는지는 미분으로 알 수 있다. 반대 방향으로 조금 이동하면 Loss를 줄일 가능성이 높다.

## 2. 가장 단순한 예: 하나의 가중치가 만드는 골짜기

Loss가 다음과 같다고 하자.

$$
L(w)=(w-3)^2
$$

최솟값은 $w=3$이지만 모른다고 가정하고 $w=0$에서 출발한다. 미분은

$$
\frac{dL}{dw}=2(w-3)
$$

이므로 $w=0$에서 기울기는 $-6$이다. 학습률 $\eta=0.1$이면 다음 값은

$$
w_{new}=0-0.1(-6)=0.6
$$

이다. Loss는 $9$에서 $5.76$으로 줄어든다. 이 계산을 반복하면 $w$는 3에 가까워진다.

## 3. 수식: Gradient와 업데이트

Parameter가 여러 개일 때 각 방향의 편미분을 모은 벡터가 <strong>Gradient</strong>다.

$$
\nabla_W L=
\begin{bmatrix}
\frac{\partial L}{\partial w_1}\\
\frac{\partial L}{\partial w_2}\\
\vdots
\end{bmatrix}
$$

기본 Gradient Descent 업데이트는 다음과 같다.

$$
\boxed{W_{t+1}=W_t-\eta\nabla_W L(W_t)}
$$

$\eta$는 <strong>learning rate</strong>다. 너무 크면 최솟값을 지나치거나 발산하고, 너무 작으면 학습이 지나치게 느리다.

데이터 사용 방식과 업데이트 규칙에 따라 방법이 발전한다.

| 방법 | 핵심 생각 |
| --- | --- |
| Batch Gradient Descent | 전체 데이터의 Gradient로 한 번 업데이트 |
| SGD / Mini-batch SGD | 일부 데이터로 더 자주 업데이트 |
| Momentum | 이전 이동 방향을 누적해 흔들림을 줄임 |
| Adam | Parameter별 이동 크기를 적응적으로 조절 |

<strong>Gradient</strong>는 움직일 방향에 대한 정보이고, <strong>Optimizer</strong>는 그 정보를 이용해 실제 $W$를 바꾸는 규칙이다.

## 4. 문제 발생: 수백만 개의 Gradient는 누가 계산할까?

단순한 함수는 손으로 미분할 수 있지만 신경망은 여러 Layer와 Activation을 거쳐 Loss를 만든다. 모든 Parameter가 Loss에 미친 영향을 직접 전개하면 계산이 매우 복잡해진다.

또 한 번의 업데이트는 학습의 끝이 아니다. mini-batch마다 <strong>Forward → Loss → Gradient 계산 → Update</strong>를 반복하고, 전체 학습 데이터를 한 바퀴 본 것을 한 <strong>epoch</strong>라고 부른다.

## 5. 다음 장 연결

> **신경망은 모든 Layer의 $\partial L/\partial W$를 어떻게 효율적으로 계산할까?**

다음 장에서는 비선형성이 왜 필요한지 확인하고, Forward·Loss·Backward·Update를 하나의 학습 cycle로 연결한다.

## 핵심 정리

- Gradient는 Loss가 가장 빠르게 증가하는 방향을 가리킨다.
- Gradient Descent는 그 반대 방향으로 이동한다.
- Optimizer는 계산된 Gradient를 이용해 Parameter를 업데이트한다.
- Backpropagation은 Optimizer가 아니라 Gradient를 효율적으로 계산하는 방법이다.

## 짧은 활동

$L(W)=(W-3)^2$에서 $W=0$일 때 Gradient를 구하고, 학습률 0.1과 1.2로 한 번 업데이트한다. 어느 이동이 안정적인지 비교한다.

## 학습 점검

1. Gradient가 양수일 때 Gradient Descent는 W를 어느 방향으로 바꾸는가?
2. Adam과 SGD는 Gradient를 계산하는가, 계산된 Gradient로 Parameter를 바꾸는가?

## 참고문헌과 공식 자료

- [Ruder, An Overview of Gradient Descent Optimization Algorithms](https://arxiv.org/abs/1609.04747)
- [PyTorch, Optimizing Model Parameters](https://pytorch.org/tutorials/beginner/basics/optimization_tutorial.html)
