# From Embeddings to Attention and Transformers

## 학습 목표

단어를 계산하려면 먼저 숫자 벡터(Embedding)로 바꿔야 하고, 문장 안에서 단어들이 서로를 참조하는 관계를 계산해야 한다. 이 장은 Embedding에서 Attention과 Transformer로 이어지는 흐름을 패션 텍스트 예로 따라간다.

이 장을 마치면 다음을 할 수 있다.

- Token, Embedding과 Position information의 역할을 구분한다.
- Q·K·V와 scaled dot-product attention의 Shape를 추적한다.
- Causal mask와 next-token objective가 생성형 언어모델 학습에 하는 역할을 설명한다.

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

### 순서 정보와 Mask

Self-attention만으로는 Token의 원래 순서를 자동으로 알 수 없으므로 Position embedding 또는 rotary position encoding 같은 순서 정보를 결합한다. 생성형 언어모델은 미래 Token을 미리 보지 못하도록 Causal mask를 적용하고, 앞선 Token들로 다음 Token을 맞히는 Cross Entropy loss를 줄이도록 학습할 수 있다.

| 장치 | 해결하는 문제 | 주의점 |
| --- | --- | --- |
| Position information | Token 순서 표현 | 구현 방식은 모델마다 다름 |
| Causal mask | 미래 Token 누설 방지 | Encoder형 모델에는 다른 Mask를 쓸 수 있음 |
| Attention weight | 정보 혼합 비중 | 인간의 설명이나 원인과 동일하지 않음 |

$$
\text{Embedding}
\rightarrow\text{Multi-Head Attention}
\rightarrow\text{Feed Forward}
\rightarrow\text{Transformer Blocks}
\rightarrow\text{Prediction}
$$

### Python으로 Attention 가중치 읽기

Attention score가 클수록 softmax 뒤의 가중치가 커진다. 아래 예에서는 두 번째 토큰의 값이 최종 표현에 가장 크게 반영된다.

```python
import numpy as np

scores = np.array([1.0, 2.0, 0.0])
weights = np.exp(scores - scores.max())
weights = weights / weights.sum()
values = np.array([10.0, 20.0, 30.0])

print("weights =", np.round(weights, 3))
print("weighted value =", round(float(weights @ values), 3))
```

```output
weights = [0.245 0.665 0.09 ]
weighted value = 18.453
```

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

## 짧은 활동

세 Token 문장을 정하고 $QK^T$를 3×3 표로 그린다. 마지막 Token을 예측하는 행에서 미래 위치가 가려져야 하는 칸을 표시한다.

## 학습 점검

1. Embedding만 있고 Position information이 없으면 어떤 정보가 약해지는가?
2. Attention weight가 높다는 사실을 곧바로 인간이 납득할 인과 설명으로 볼 수 없는 이유는 무엇인가?

## 참고문헌과 공식 자료

- [Vaswani et al., Attention Is All You Need](https://papers.nips.cc/paper/7181-attention-is-all-you-need)
- [The Illustrated Transformer](https://jalammar.github.io/illustrated-transformer/) — 수식과 함께 읽는 보조 시각 자료
