# pandas로 표 데이터 다루기

## 학습 목표

- `DataFrame`과 `Series`의 관계를 설명한다.
- `read_csv`로 파일을 읽고 `head`, `info`, `describe`로 점검한다.
- 컬럼 선택, 조건 필터, 새 컬럼 만들기를 수행한다.
- `groupby`로 집계하고 `merge`로 두 표를 연결한다.

> **이 장의 중심 질문**<br>
> 반복문 없이 표 전체를 한 번에 필터하고 집계하려면 어떤 도구가 필요할까?

## 핵심 용어

- **DataFrame**: 행과 열로 이루어진 pandas의 표. 엑셀 시트와 비슷하다.
- **Series**: DataFrame의 한 열. 인덱스가 붙은 1차원 값의 모음.
- **결측치(NaN)**: 값이 비어 있는 자리.
- **집계(aggregation)**: 여러 행을 합계·평균·개수 같은 하나의 값으로 요약하는 것.
- **조인(join/merge)**: 공통 키로 두 표를 연결하는 것.

## 1. 표 불러오기와 첫 점검

```python
import pandas as pd

products = pd.read_csv("products.csv")
print(products.shape)      # (행 수, 열 수)
products.head()            # 처음 5행
products.info()            # 컬럼 이름, 자료형, 결측 여부
products.describe()        # 숫자 컬럼의 요약 통계
```

`read_csv`는 3장에서 한 줄씩 읽던 작업을 한 번에 처리하고, **숫자 컬럼을 자동으로 숫자 자료형으로 인식**한다. 항상 `shape`, `head`, `info`를 먼저 보고 행 수·컬럼·결측을 확인한다.

## 2. 컬럼과 행 선택하기

```python
products["list_price"]              # 한 컬럼 (Series)
products[["product_id", "color"]]   # 여러 컬럼 (DataFrame)

products.iloc[0]        # 첫 번째 행 (위치로)
products.loc[0, "color"]  # 0번 행의 color 값 (이름으로)
```

## 3. 조건 필터: 2장의 if를 표 전체에

2장에서는 `for`와 `if`로 조건에 맞는 값을 하나씩 골랐다. pandas는 조건식 하나로 전체 행을 거른다.

```python
mask = products["list_price"] >= 100000
expensive = products[mask]

# 조건을 바로 넣어도 된다
coats = products[products["category"] == "Coat"]

# 여러 조건은 & (그리고), | (또는), 각 조건은 괄호로 감싼다
navy_coats = products[(products["category"] == "Coat") & (products["color"] == "Navy")]
```

`products["list_price"] >= 100000`은 각 행에 대해 `True`/`False`를 담은 Series를 만든다. 그 Series로 DataFrame을 인덱싱하면 `True`인 행만 남는다.

## 4. 새 컬럼 만들기

```python
products["price_krw_10k"] = products["list_price"] / 10000
```

컬럼끼리의 연산은 행 단위로 자동 적용된다. 반복문이 필요 없다.

## 5. 결측치 확인과 처리

```python
products.isna().sum()          # 컬럼별 결측 개수
products = products.dropna(subset=["list_price"])   # 가격이 빈 행 제거
products["color"] = products["color"].fillna("unknown")  # 색상 결측은 표시로 대체
```

결측을 지울지 채울지는 분석 질문에 따라 다르다. 어느 쪽이든 **몇 행을 어떻게 처리했는지 기록**한다.

## 6. groupby: 그룹별 집계

```python
orders = pd.read_csv("orders.csv")

# 상품별 주문 건수
orders.groupby("product_id").size()

# 상품별 수량 합계
orders.groupby("product_id")["quantity"].sum()

# 여러 집계를 한 번에
orders.groupby("product_id").agg(
    order_count=("order_id", "count"),
    total_qty=("quantity", "sum"),
)
```

`groupby`는 "같은 값을 가진 행끼리 묶어 각 묶음을 하나의 숫자로 요약"한다. SQL의 `GROUP BY`, 패션 빅데이터 1의 질문·분석 워크플로우 장에서 배운 집계와 같은 개념이다.

## 7. merge: 두 표 연결하기

`orders.csv`에는 `product_id`만 있고 상품 이름·카테고리는 `products.csv`에 있다. 공통 키로 연결한다.

```python
merged = orders.merge(products, on="product_id", how="left")
print(merged.shape)
```

- `on="product_id"`: 이 컬럼의 값이 같은 행끼리 붙인다.
- `how="left"`: 왼쪽 표(`orders`)의 모든 행을 유지하고, 오른쪽에서 짝을 찾는다. 짝이 없으면 결측이 된다.

연결 후에는 **행 수가 예상과 같은지** 반드시 확인한다. 키가 중복되면 행이 늘어날 수 있다.

```python
category_sales = (
    merged.groupby("category")["quantity"].sum().sort_values(ascending=False)
)
print(category_sales)
```

## 8. 문제 발생: SettingWithCopyWarning

필터한 결과에 값을 새로 넣으면 경고가 나올 수 있다.

```python
coats = products[products["category"] == "Coat"]
coats["on_sale"] = True   # SettingWithCopyWarning
```

이는 "지금 원본의 일부를 보고 있는지 복사본을 보고 있는지 불분명하다"는 경고다. 가공할 부분은 명시적으로 복사한다.

```python
coats = products[products["category"] == "Coat"].copy()
coats["on_sale"] = True
```

2장의 "리스트는 복사되지 않는다"와 같은 원리다.

## 9. AI가 만든 pandas 코드 검수표

| 확인 | 최소 검사 |
|---|---|
| 입력 | `shape`, 컬럼, dtype, 날짜 범위 |
| 필터 | 포함·제외된 실제 행을 각각 확인 |
| `groupby` | 분모와 집계 단위, 합계의 보존 |
| `merge` | 키 중복, 미매칭, 조인 전후 행 수 |
| 결측 | 0·빈 문자열·`NaN`의 구분 |
| 출력 | 손으로 계산한 3~5행 예제와 일치 |

AI에게 “분석해 줘”라고만 요청하지 않는다. 분석 단위, 기간, 취소·반품 규칙과 기대 출력 컬럼을 먼저 제공하고, 생성된 코드의 각 변환 뒤 행 수를 출력하도록 한다.

## 짧은 활동

공통 실습 데이터로 코랩에서 수행한다.

1. `products.csv`와 `orders.csv`를 읽고 각각의 `shape`, `head`, 결측 개수를 확인한다.
2. `orders`에서 취소·반품이 아닌 주문만 남긴다(상태 컬럼 확인).
3. 두 표를 `product_id`로 연결한다. 연결 전후 행 수를 비교한다.
4. 카테고리별 총 수량을 큰 순서로 정렬해 출력한다.
5. 각 단계에서 제외한 행 수를 주석으로 남긴다.

## 이 장의 핵심

- `DataFrame`은 표, `Series`는 한 컬럼이다. `read_csv`가 파일을 표로 불러온다.
- `shape`/`head`/`info`/`isna().sum()`으로 항상 먼저 점검한다.
- 조건식으로 만든 불리언 Series로 행을 필터한다. 여러 조건은 `&`, `|`와 괄호를 쓴다.
- `groupby`는 그룹별 집계, `merge`는 공통 키로 표 연결이다.
- 연결·필터 뒤에는 행 수를 확인하고, 가공 전 `.copy()`를 쓴다.

## 학습 점검

1. `df["col"]`과 `df[["col"]]`의 결과 자료형은 각각 무엇인가?
2. `df[df["price"] > 100]`은 어떤 원리로 행을 거르는가?
3. `merge`에서 `how="left"`는 무엇을 보장하며, 연결 후 왜 행 수를 확인해야 하는가?

<details><summary>정답과 해설 보기</summary>

1. `df["col"]`은 `Series`(1차원), `df[["col"]]`은 컬럼이 하나인 `DataFrame`(2차원)이다.
2. 비교식이 각 행에 대해 `True`/`False`를 담은 Series를 만들고, 그 Series로 인덱싱하면 `True`인 행만 남는다.
3. 왼쪽 표의 모든 행이 유지된다. 오른쪽 키가 중복이면 한 행이 여러 행으로 늘어날 수 있으므로, 의도한 단위가 유지됐는지 행 수로 확인한다.

</details>

## 참고문헌과 공식 문서

- [pandas 공식: 10분 만에 배우는 pandas](https://pandas.pydata.org/docs/user_guide/10min.html)
- [pandas 공식: merge, join, concatenate](https://pandas.pydata.org/docs/user_guide/merging.html)

## 다음 장

이번 장에서는 표를 다뤘다. 다음 장에서는 표 아래에 있는 숫자 배열 자체를 NumPy로 계산하고, 결과를 그래프로 그린다.

> **표의 한 열을 벡터로 보고 평균·거리·기울기를 직접 계산하려면 무엇이 필요할까?**
