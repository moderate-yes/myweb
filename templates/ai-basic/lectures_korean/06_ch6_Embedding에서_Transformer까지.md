# Embedding에서 Attention과 Transformer까지

> **중심 질문**<br>
> 문장 속 단어들은 서로의 관계를 어떻게 계산하고 학습할까?

## 1. 질문: 단어를 계산 가능한 형태로 바꾸려면?

컴퓨터는 “배”, “먹다”, “타다” 같은 글자의 의미를 그대로 계산하지 못한다. 먼저 문장을 작은 단위인 <strong>Token</strong>으로 나누고, 각 Token을 숫자 Vector인 <strong>Embedding</strong>으로 바꾼다.

## 2. 가장 단순한 예: 어떤 단어를 참고할까?

“나는 배를 타고 섬에 갔다”에서 “배”는 과일보다 탈것에 가깝다. “배”의 Vector가 주변 Token의 Vector와 얼마나 관련 있는지를 비교하면 문맥에 필요한 정보를 모을 수 있다.

두 Vector의 <strong>dot product</strong>가 크면 방향이 더 비슷하다고 해석할 수 있다.

$$
\mathbf{q}\cdot\mathbf{k}=\sum_i q_i k_i
$$

다만 크기까지 영향을 주므로 실제 모델에서는 학습된 표현과 scaling, normalization 같은 장치가 함께 사용된다.

## 3. 수식: Q, K, V에서 Attention으로

입력 Embedding 행렬 $X$에 학습 가능한 Parameter Matrix를 곱해 Query, Key, Value를 만든다.

$$
Q=XW_Q,\qquad K=XW_K,\qquad V=XW_V
$$

1장에서 만난 $W$가 다시 등장했다. 이제 하나의 기울기가 아니라 “무엇을 찾고, 무엇과 비교하고, 어떤 정보를 가져올지”를 학습하는 여러 행렬이다.

Query와 모든 Key의 관계 점수를 계산하고, 값이 지나치게 커지는 것을 막기 위해 $\sqrt{d_k}$로 나눈다. Softmax는 각 행을 합이 1인 가중치로 바꾼다.

$$
\boxed{\operatorname{Attention}(Q,K,V)
=\operatorname{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V}
$$

계산의 의미는 다음과 같다.

1. $QK^T$: 각 Token이 다른 Token을 얼마나 볼지 점수 계산
2. $\operatorname{softmax}$: 점수를 상대적인 Attention weight로 변환
3. $\times V$: weight에 따라 필요한 정보 혼합

서로 다른 관계를 동시에 보기 위해 여러 Attention을 병렬로 수행하는 것이 <strong>Multi-Head Attention</strong>이다. 여기에 Feed Forward Network, Residual Connection, Layer Normalization을 결합하면 Transformer block이 된다.

$$
\text{Embedding}
\rightarrow\text{Multi-Head Attention}
\rightarrow\text{Feed Forward}
\rightarrow\text{Transformer Blocks}
\rightarrow\text{Prediction}
$$

## 4. 문제 발생: 복잡한 모델의 Loss가 낮으면 충분할까?

Transformer도 특별한 학습 법칙을 쓰는 것은 아니다. Prediction으로 Loss를 계산하고 Backpropagation으로 $W_Q,W_K,W_V$를 비롯한 모든 Parameter의 Gradient를 구한 뒤 Optimizer가 업데이트한다.

하지만 Training Loss가 계속 낮아져도 새로운 문장에서 잘 작동한다는 보장은 없다. 학습 데이터를 외웠을 수도 있고, 우리가 실제로 중요하게 생각하는 품질과 Loss가 완전히 같지 않을 수도 있다.

## 5. 다음 장 연결

> **학습 데이터의 Loss가 낮은 모델을 정말 좋은 AI라고 할 수 있을까?**

다음 장에서는 Train·Validation·Test를 나누는 이유와 Loss와 Metric의 차이, 일반화 성능을 평가하는 방법을 배운다.

## 핵심 정리

- Token은 Embedding Vector로 변환된다.
- Attention은 $QK^T$로 관계를 계산하고 $V$의 정보를 가중합한다.
- $W_Q,W_K,W_V$도 Loss를 줄이도록 학습되는 Parameter다.
- Transformer 역시 Matrix Multiplication + Loss + Backpropagation + Optimizer로 학습한다.
