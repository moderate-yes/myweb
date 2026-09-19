# How Does a Neural Network Learn?

## 학습 목표

신경망은 Linear 계산과 비선형 활성화를 여러 층 쌓은 모델이며, 수많은 Parameter를 같은 원리로 갱신한다. 이 장은 순전파 → Loss → 역전파 → 갱신의 한 사이클을 따라가며 딥러닝 학습이 앞 장의 확장임을 보인다.

이 장을 마치면 다음을 할 수 있다.

- Activation이 없는 여러 Linear Layer가 하나로 합쳐지는 이유를 설명한다.
- Forward, Loss, Backward, Update의 순서를 말한다.
- Chain rule이 여러 Parameter의 Gradient를 연결하는 방식을 직관적으로 설명한다.

## 1. 질문: Linear Layer를 많이 쌓으면 충분할까?

신경망은 입력을 여러 단계로 변환한다. 하지만 각 단계가 선형 변환뿐이라면 깊게 쌓는 의미가 사라진다.

## 2. 가장 단순한 예: 선형 변환 두 개 쌓기

편의를 위해 bias를 생략하면 두 Layer는 다음과 같다.

$$
H=XW_1,\qquad \hat Y=HW_2
$$

두 식을 합치면,

$$
\hat Y=XW_1W_2=XW'
$$

이다. $W'=W_1W_2$로 둘 수 있으므로 선형 Layer를 아무리 많이 연결해도 결국 하나의 선형 변환과 같다. 곡선이나 복잡한 결정 경계를 표현하려면 Layer 사이에 <strong>Activation Function(활성화 함수)</strong>이 필요하다.

$$
H=\operatorname{ReLU}(XW_1+b_1),\qquad
\hat Y=HW_2+b_2
$$

ReLU는 $\operatorname{ReLU}(z)=\max(0,z)$라는 비선형성을 넣어 신경망이 단순한 직선 이상의 관계를 학습하게 한다.

## 3. 수식: Forward → Loss → Backward → Update

신경망 학습은 네 단계를 반복한다.

### ① Forward

입력 $X$를 Layer와 Activation에 통과시켜 Prediction $\hat Y$를 만든다.

$$
X\rightarrow Z_1\rightarrow H\rightarrow \hat Y
$$

### ② Loss

Prediction과 Target을 비교한다. 회귀라면 MSE, 분류라면 cross entropy 등을 사용할 수 있다.

$$
L=L(\hat Y,Y)
$$

### ③ Backward

연쇄법칙(chain rule)으로 Loss에서 각 Parameter까지 거슬러 올라가 Gradient를 계산한다.

$$
\frac{\partial L}{\partial W_1}
{}={}
\frac{\partial L}{\partial \hat Y}
\frac{\partial \hat Y}{\partial H}
\frac{\partial H}{\partial Z_1}
\frac{\partial Z_1}{\partial W_1}
$$

이 Gradient 계산 절차가 <strong>Backpropagation</strong>이다.

### ④ Update

Optimizer가 계산된 Gradient로 Parameter를 바꾼다.

$$
W_1\leftarrow W_1-\eta\frac{\partial L}{\partial W_1}
$$

### Python으로 Activation의 역할 확인하기

선형 변환 두 개만 이어 붙이면 하나의 선형 변환과 같다. 중간에 ReLU를 넣으면 음수 영역의 처리 방식이 달라져 같은 입력에도 다른 형태의 출력이 만들어진다.

```python
import numpy as np

x = np.array([-2, -1, 1, 2])
linear_stack = -0.5 * (2 * x)
with_relu = -0.5 * np.maximum(0, 2 * x)

print("linear only =", linear_stack)
print("with ReLU  =", with_relu)
```

```output
linear only = [ 2.  1. -1. -2.]
with ReLU  = [-0. -0. -1. -2.]
```

## 4. 문제 발생: 순서가 있는 데이터의 관계

이 cycle은 이미지, 표, 문장 모두에 적용된다. 하지만 문장에서 같은 단어도 주변 단어에 따라 의미가 달라진다. 각 위치를 독립적으로 처리하면 “그것”이 무엇을 가리키는지, 문장 앞부분과 뒷부분이 어떻게 연결되는지 놓치기 쉽다.

입력을 숫자 벡터로 바꾸고, 벡터끼리 어떤 관계가 중요한지 모델이 선택하도록 만들 필요가 있다.

## 5. 다음 장 연결

> **문장 속 각 token은 다른 token 중 무엇을 얼마나 참고해야 할까?**

다음 장에서는 Token을 Embedding으로 바꾸고, Q·K·V와 Attention을 거쳐 Transformer가 관계를 학습하는 과정을 살펴본다.

## 핵심 정리

- 선형 Layer만 쌓으면 하나의 선형 변환으로 합쳐진다.
- Activation은 신경망에 비선형성을 더한다.
- Forward는 예측, Loss는 비교, Backward는 Gradient 계산, Optimizer는 $W$ 업데이트다.
- <strong>Forward → Loss → Backward → Update</strong>가 신경망 학습의 기본 cycle이다.

## 짧은 활동

입력 하나, Linear Layer 하나, ReLU 하나, 출력 하나인 작은 신경망을 상자로 그린다. Forward 값과 Backward Gradient가 이동하는 방향을 서로 다른 화살표로 표시한다.

## 학습 점검

1. Linear Layer 사이에 Activation이 필요한 이유는 무엇인가?
2. Backward가 끝난 뒤에도 Optimizer step이 필요한 이유는 무엇인가?

## 참고문헌과 공식 자료

- [Rumelhart, Hinton & Williams, Learning representations by back-propagating errors](https://doi.org/10.1038/323533a0)
- [PyTorch, Build the Neural Network](https://pytorch.org/tutorials/beginner/basics/buildmodel_tutorial.html)
