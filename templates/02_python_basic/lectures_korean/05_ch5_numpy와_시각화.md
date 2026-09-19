# NumPy Arrays, Plots, and Next Steps

## 학습 목표

표의 한 열은 곧 숫자 배열이며, AI 수학이 말하는 벡터와 Shape가 여기서 시작된다. 이 장은 NumPy 배열의 Shape·축·브로드캐스팅과 matplotlib 기본 그래프를 다룬다.

이 장을 마치면 다음을 할 수 있다.

- NumPy 배열을 만들고 Shape를 읽는다.
- 벡터·행렬 연산과 브로드캐스팅을 이해한다.
- 평균·합·표준편차 같은 요약을 축(axis) 단위로 계산한다.
- matplotlib으로 기본 그래프를 그린다.
- 이 과정에서 배운 것을 다음 과정으로 연결한다.

## 1. 배열 만들기와 Shape 읽기

```python
import numpy as np

prices = np.array([59000, 129000, 229000, 39000])
print(prices.shape)   # (4,)      1차원, 원소 4개
print(prices.dtype)   # int64

matrix = np.array([[2, 7], [4, 6], [6, 5]])
print(matrix.shape)   # (3, 2)    행 3, 열 2
```

Shape는 튜플이다(2장). AI Math와 AI Basic에서 반복하는 "Shape가 계산 가능성을 결정한다"는 말은 여기서 확인된다.

```python
np.zeros((2, 3))          # 0으로 채운 2x3
np.arange(0, 10, 2)       # [0 2 4 6 8]
np.linspace(0, 1, 5)      # [0. 0.25 0.5 0.75 1.]
```

## 2. 벡터 연산: 반복문 없이 전체 계산

```python
prices = np.array([59000, 129000, 229000, 39000])
raised = prices * 1.1          # 모든 원소에 곱셈
diff = prices - prices.mean()  # 각 원소에서 평균을 뺌
```

2장에서 `for` 반복으로 하던 "10% 인상" 계산이 한 줄이 된다. 이것이 벡터화다.

두 벡터의 내적(dot product)은 AI Math 2장의 유사도, AI Basic의 $XW$에서 계속 나온다.

```python
q = np.array([1, 0, 2])
k = np.array([0, 1, 2])
print(np.dot(q, k))   # 4
```

행렬 곱은 `@`를 쓴다. 안쪽 차원이 같아야 한다.

```python
X = np.array([[2, 7], [4, 6], [6, 5]])   # (3, 2)
w = np.array([10, 3])                    # (2,)
print(X @ w)          # (3,)  각 행의 가중합
```

## 3. 브로드캐스팅

Shape가 달라도 규칙에 맞으면 자동으로 맞춰 계산한다.

```python
X = np.array([[2, 7], [4, 6], [6, 5]])   # (3, 2)
col_mean = X.mean(axis=0)                # (2,)  열별 평균
centered = X - col_mean                  # (3, 2) - (2,) -> 각 행에서 열 평균을 뺌
```

`axis=0`은 "행을 가로질러" 즉 열별로 요약하고, `axis=1`은 "열을 가로질러" 행별로 요약한다.

```python
X.sum(axis=0)    # 열별 합
X.sum(axis=1)    # 행별 합
X.std(axis=0)    # 열별 표준편차
```

## 4. matplotlib으로 그래프 그리기

```python
import matplotlib.pyplot as plt

categories = ["Coat", "Shirt", "Pants", "Shoes"]
counts = [12, 30, 21, 9]

plt.bar(categories, counts)
plt.ylabel("Number of orders")
plt.title("Orders by category")
plt.show()
```

선 그래프와 히스토그램도 자주 쓴다.

```python
x = np.linspace(-3, 3, 100)
plt.plot(x, x ** 2)      # 손실 함수 모양 확인
plt.show()

plt.hist(np.random.normal(0, 1, 1000), bins=30)   # 분포 확인
plt.show()
```

pandas와 함께 쓰면 더 짧다. `df["list_price"].plot(kind="hist")`처럼 DataFrame에서 바로 그릴 수 있다.

## 5. 문제 발생: 정수 배열에 실수를 넣을 때

```python
a = np.array([1, 2, 3])      # dtype int64
a[0] = 3.9
print(a)                     # [3 2 3]   소수점이 잘림
```

배열은 하나의 dtype만 가진다. 정수 배열에 실수를 넣으면 조용히 잘린다. 처음부터 `np.array([1, 2, 3], dtype=float)`로 만들거나 `a.astype(float)`로 바꾼다. AI 계산에서 Shape 오류만큼 자주 겪는 문제다.

## 6. AI가 만든 배열·그래프를 검증하는 세 질문

1. 배열의 각 축은 무엇을 뜻하며 기대한 Shape인가?
2. broadcasting이 의도한 축에 적용되었는가?
3. 그래프의 축·단위·분모·누락 범주가 질문과 일치하는가?

보기 좋은 그래프는 정확한 분석의 증거가 아니다. 원자료의 최소·최대, 표본 수와 집계표를 그래프 옆에 두고 같은 결론이 나오는지 확인한다.

## 통합 미니 프로젝트: 두 표에서 한 장짜리 요약 만들기

공통 실습 데이터로 다음을 하나의 노트로 정리한다. 이 과정의 완료 기준이다.

| 단계 | 할 일 | 확인 질문 |
|---|---|---|
| 로드 | `products.csv`, `orders.csv`를 pandas로 읽는다 | 각 표의 행 수와 컬럼은? |
| 점검 | `info`, `isna().sum()`으로 결측 확인 | 어떤 컬럼에 결측이 있는가? |
| 정제 | 취소·반품 주문을 제외한다 | 몇 행을 제외했는가? |
| 결합 | `product_id`로 두 표를 `merge` | 연결 후 행 수가 예상과 같은가? |
| 집계 | 카테고리별 주문 수량 합계 (`groupby`) | 상위 카테고리는? |
| 배열 | 카테고리별 합계를 NumPy 배열로 바꿔 평균·표준편차 계산 | 어떤 카테고리가 평균에서 먼가? |
| 시각화 | 카테고리별 합계 막대그래프 1개 | 제목·축 이름을 넣었는가? |

최종 산출물은 코드와 함께 **사용한 제외 규칙, 기준 기간, 연결 후 행 수**를 적은 짧은 메모다.

## 다음 단계로 연결

이 과정을 마치면 다음을 할 수 있다.

- **패션 데이터 분석과 AI 활용 15~26장**: 코랩에서 수집한 데이터를 pandas로 정제·집계한다.
- **AI Math**: 손으로 계산한 norm, 내적, 최소제곱, Gradient를 `np.dot`, `@`, `np.linalg`로 검산한다.
- **AI Basic**: $\hat Y = XW$, `W - η∇L` 같은 식을 작은 배열로 직접 실행해 본다.

## 이 장의 핵심

- NumPy 배열은 하나의 dtype을 가진 다차원 숫자 묶음이고 Shape는 각 축의 크기다.
- 벡터화로 반복문 없이 배열 전체를 계산한다. 내적은 `np.dot`, 행렬곱은 `@`.
- 브로드캐스팅은 Shape가 다른 배열을 규칙에 맞춰 자동으로 맞춘다.
- `axis=0`은 열별, `axis=1`은 행별 요약이다.
- matplotlib의 `bar`, `plot`, `hist`로 기본 그래프를 그린다.

## 학습 점검

1. Shape `(3, 2)` 배열에 `.mean(axis=0)`을 하면 결과 Shape는 무엇인가?
2. `np.dot(q, k)`와 `X @ w`는 각각 무엇을 계산하며, 곱셈이 가능한 조건은?
3. 정수 배열에 `a[0] = 3.9`를 넣으면 어떻게 되는가? 왜인가?

<details><summary>정답과 해설 보기</summary>

1. `(2,)`이다. `axis=0`은 행을 가로질러 각 열을 하나의 값으로 요약하므로 열 개수만 남는다.
2. `np.dot(q, k)`는 두 벡터의 내적(원소별 곱의 합), `X @ w`는 행렬과 벡터의 곱이다. 앞 배열의 마지막 축 크기와 뒤 배열의 첫 축 크기가 같아야 한다.
3. `3`으로 잘려 저장된다. 배열은 단일 dtype(여기서는 정수)만 담으므로 실수의 소수부가 버려진다.

</details>

## 참고문헌과 공식 문서

- [NumPy 공식: 초보자를 위한 안내](https://numpy.org/doc/stable/user/absolute_beginners.html)
- [Matplotlib 공식: Pyplot 튜토리얼](https://matplotlib.org/stable/tutorials/pyplot.html)

## 과정 마무리

> 도구의 문법보다 중요한 것은 **데이터의 Shape를 읽고, 무엇을 제외했는지 기록하고, 결과를 그림으로 확인하는 습관**이다. 다음 과정의 코드는 모두 이 위에서 돌아간다.

## 핵심 용어

- **배열(ndarray)**: NumPy가 다루는 같은 자료형의 다차원 숫자 묶음.
- **Shape**: 배열의 각 축 크기를 담은 튜플. 예: `(100, 3)`.
- **축(axis)**: 배열의 방향. 2차원에서 `axis=0`은 행 방향, `axis=1`은 열 방향.
- **브로드캐스팅(broadcasting)**: Shape가 다른 배열을 규칙에 따라 자동으로 맞춰 계산하는 것.
- **벡터화(vectorization)**: 반복문 없이 배열 전체를 한 번에 계산하는 방식.
