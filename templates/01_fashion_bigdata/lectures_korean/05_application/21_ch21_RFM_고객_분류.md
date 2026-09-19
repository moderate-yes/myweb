# RFM and Behavior-Based Customer Segmentation

## 학습 목표

고객 분류의 목적은 사람에게 낙인을 붙이는 것이 아니라 서로 다른 다음 행동을 설계하는 것이다. 주문 기록의 RFM과 최근 행동 신호를 같은 고객 단위 표로 만들고, 규칙과 군집이 어떤 차이를 만드는지 비교한다.

이 장을 마치면 다음을 할 수 있다.

- R·F·M 세 지표를 기준일과 관찰 기간을 정해 정의하고 주문 기록에서 계산한다.
- F·M을 각각 5분위 등수(1~5등)로 바꾸고, 한두 번 구매한 고객을 제외하는 이유를 설명한다.
- F등수 × M등수 2차원 그래프를 읽고, k-means와 마케터의 수동 구획이 만드는 결과 차이를 설명한다.
- 인구통계·구매 이력 같은 설명 변수로 군집의 특성을 명명하고, 분류 변수를 3개 이내로 제한하는 이유를 설명한다.
- 세그먼트를 시장성·차별성·실행 가능성으로 평가하고 CRM 발송 목록으로 내보내는 시스템을 그린다.
- RFM과 최근 행동 신호를 결합해 메시지 대상·시점·채널을 정한다.
- 발송률이 아니라 증분 구매·수신 거부·피로도를 함께 평가한다.


## 개념부터 시작하기

기준일 \(T\)에서 고객 \(u\)의 RFM 벡터를 \(x_u=(R_u,F_u,M_u)\)로 둔다. \(R\)은 마지막 구매 이후 경과일, \(F\)는 구매 횟수, \(M\)은 구매 금액이다. 방향이 다른 \(R\)은 작을수록 활동적이라는 점을 등수화할 때 명시한다.

가장 단순한 기준선은 분위수 규칙이다. 그 다음 k-means를 적용하되 변수 스케일과 군집 수에 따라 결과가 달라짐을 확인한다. 최근 조회·찜·장바구니는 고객의 현재 상태를 보완하지만, 인구통계는 군집을 만든 변수와 군집을 설명하는 변수를 구분해 사용한다.

## 문제 설정: 매출을 많이 올려주는 고객은 누구인가

우리 쇼핑몰에서 매출을 많이 올려주는 고객이 "중산층, 46~60세, 가족 구성원이 적고 온라인 쇼핑을 자주 하는 사람"이라는 특성을 안다면, 마케팅을 그 조건에 집중할 수 있다. 반대로 매출 기여는 낮지만 최근 방문이 잦은 고객이 "수입차를 선호하고 서쪽 지역에 사는 사람"이라면 구매 잠재력이 높다고 판단해 그 지역에 홍보를 늘릴 수도 있다. RFM 분석의 목적은 이렇게 **고객의 행동을 바탕으로 고객을 구분**하고, 구분된 그룹의 특성을 설명하는 것이다.

나이·지역·성별·구매 상품보다 RFM으로 먼저 시작하는 이유는 분명하다. 분류 기준이 많으면 (1) 각 집단의 특성을 설명하기 어렵고, (2) 데이터와 분석 방법이 복잡해져 계산 자원이 더 필요하다. 추천 시스템을 처음 도입하는 회사라면 RFM으로 출발한 뒤 목적에 맞춰 변수를 늘리는 편이 낫다.

> **앞에서 배운 내용과 연결**
> - 고객 식별자와 주문·고객 표의 JOIN: [3장 식별자와 마스터 데이터](templates/01_fashion_bigdata/lectures_korean/02_data/03_ch3_식별자와_마스터_데이터.md).
> - 순서 척도(등수)와 비율 척도(금액)의 차이: [4장 데이터의 의미와 모양](templates/01_fashion_bigdata/lectures_korean/02_data/04_ch4_데이터의_의미와_모양.md).
> - 분위와 집단 비교: [10장 특성화와 차별화](templates/01_fashion_bigdata/lectures_korean/03_analysis/10_ch10_특성화와_차별화.md).
> - 군집 변수와 설명 변수, k-means, 군집 평가: [13장 군집](templates/01_fashion_bigdata/lectures_korean/03_analysis/13_ch13_군집.md).

## 1. 데이터를 표로 표현하기

| 데이터 | 파일 | 역할 | 데이터 특징 |
|---|---|---|---|
| 주문 기록 | `orders.csv` | R·F·M 계산의 원천 | 고객·상품 식별자, 날짜 속성, 비율 척도(금액) |
| 고객 마스터 | `customers.csv` | 성별·연령대·지역·앱 설치 | 명목 속성. 군집을 **설명**하는 변수 |
| 상품 마스터 | `products.csv` | 카테고리 | 군집별 구매 카테고리 설명 |

RFM은 **구매 거래**만 요약한다. 방문만 하고 사지 않은 고객은 여기에 없다. 강의의 F는 "정해진 기간 동안 얼마나 자주 쇼핑몰을 방문했는지"였지만, 주문 기록만 있는 상황에서는 구매 횟수를 쓴다. 방문·조회·장바구니 같은 행동은 이 장 후반에서 RFM과 결합한다.

## 2. 모형과 계산 원리

| 단계 | 분석 방법 | 이 과정의 장 |
|---|---|---|
| 고객별 R·F·M 계산 | 특성화(고객 단위 집계) | 10장 |
| 5분위 등수 변환 | 특성화(분위) | 10장 5절 |
| F등수 × M등수로 나누기 | 군집(k-means) 또는 규칙 기반 세그먼트 | 13장 1·5절 |
| 인구통계로 군집 특성 명명 | 차별화(군집 간 비교), 설명 변수 | 10장 9절, 13장 2절 |

RFM은 Recency(최근성), Frequency(빈도), Monetary(금액)의 머리글자다. R은 마지막 접속일 또는 마지막 구매일과 기준일 사이의 간격, F는 정해진 기간의 방문(구매) 횟수, M은 정해진 기간의 구매 금액이다.

## 3. 계산 순서

<div class="operations-flow" aria-label="RFM 고객 분류의 단계">
  <div><strong>1 데이터 확인</strong><span>주문 기록의 기간·상태·고객 ID 결측 점검</span></div>
  <b>↓</b>
  <div><strong>2 데이터 구축</strong><span>고객별 R·F·M 계산</span><i>→</i><span>F·M 5분위 등수(1~5)</span><i>→</i><span>한두 번 구매 고객 분리</span></div>
  <b>↓</b>
  <div><strong>3 분석</strong><span>F등수 × M등수 산점도</span><i>→</i><span>k-means(4~5개) 또는 수동 구획</span><i>→</i><span>인구통계로 군집 특성 명명</span></div>
  <b>↓</b>
  <div><strong>4 평가</strong><span>시장성·차별성·실행 가능성</span><i>→</i><span>안정성</span></div>
  <b>↓</b>
  <div class="flow-highlight"><strong>5 서비스 연동</strong><span>세그먼트 목록을 CRM·메시지 도구로 전달</span><i>→</i><span>VVIP 구매 상품을 VIP에게 추천</span></div>
</div>

## 4. Python으로 확인하기

### 1단계: 데이터 확인과 기준 고정

```python
import pandas as pd
import numpy as np

pd.set_option("display.width", 120)
pd.set_option("display.max_columns", 14)

DATA = "templates/01_fashion_bigdata/data/fashion_mall"
orders = pd.read_csv(f"{DATA}/orders.csv", parse_dates=["order_time"])
customers = pd.read_csv(f"{DATA}/customers.csv", parse_dates=["signup_date"])
products = pd.read_csv(f"{DATA}/products.csv")

SNAPSHOT = pd.Timestamp("2026-07-01")          # 기준일
completed = orders[orders["status"] == "completed"].copy()
completed["amount"] = completed["quantity"] * completed["unit_price"]
print("관찰 기간:", completed["order_time"].min().date(), "~", completed["order_time"].max().date())
print("결제 완료 주문 줄 수:", len(completed), "/ 고객 수:", completed["customer_id"].nunique())
```

```output
관찰 기간: 2026-01-01 ~ 2026-06-30
결제 완료 주문 줄 수: 11334 / 고객 수: 559
```

기준일과 관찰 기간(여기서는 2026년 상반기 6개월)이 바뀌면 R·F·M이 모두 바뀐다. 두 값을 노트 첫 줄에 기록한다.

### 2단계: 고객별 R·F·M 계산

```python
rfm = completed.groupby("customer_id").agg(
    last_order=("order_time", "max"),
    frequency=("order_id", "nunique"),      # 구매 횟수(주문 건수)
    monetary=("amount", "sum"),             # 구매 금액
)
rfm["recency"] = (SNAPSHOT - rfm["last_order"]).dt.days
rfm = rfm[["recency", "frequency", "monetary"]]
print(rfm.describe().round(1))
```

```output
       recency  frequency    monetary
count    559.0      559.0       559.0
mean      33.2       14.4   2569922.0
std       40.7       19.4   3835086.6
min        0.0        1.0     38000.0
25%        4.0        2.0    274500.0
50%       15.0        6.0    745500.0
75%       49.5       12.0   3936097.5
max      177.0       89.0  21887791.0
```

### 3단계: F·M을 5분위 등수로 바꾸고 한두 번 구매 고객을 분리

F와 M은 각각 5분위로 나누어 1등(낮음)부터 5등(높음)까지 등수를 줄 수 있다. 실제 그래프에서는 한두 번 방문해 한두 개 산 고객이 대부분이라 왼쪽 아래가 빽빽해지기 쉽다. 필요하면 이런 고객을 별도 집단으로 분리한 뒤 나머지 고객의 등수를 매겨 불균형을 줄인다.

```python
few = rfm[rfm["frequency"] <= 2]
core = rfm[rfm["frequency"] > 2].copy()
print(f"구매 2회 이하 고객 {len(few)}명은 별도 처리, 분류 대상 {len(core)}명")

core["F_rank"] = pd.qcut(core["frequency"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5]).astype(int)
core["M_rank"] = pd.qcut(core["monetary"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5]).astype(int)
core["R_rank"] = pd.qcut(core["recency"].rank(method="first"), 5, labels=[5, 4, 3, 2, 1]).astype(int)  # 최근일수록 5
print(core.head())
print(pd.crosstab(core["F_rank"], core["M_rank"]))
```

```output
구매 2회 이하 고객 141명은 별도 처리, 분류 대상 418명
             recency  frequency  monetary  F_rank  M_rank  R_rank
customer_id                                                      
C0001              1         64  17439498       5       5       5
C0003             11          3    420000       1       1       3
C0004             41          3    361000       1       1       1
C0005              0         64  15825296       5       5       5
C0006              7          6   1033800       2       3       3
M_rank   1   2   3   4   5
F_rank                    
1       59  23   2   0   0
2       23  34  26   0   0
3        2  23  42  17   0
4        0   3  14  48  18
5        0   0   0  18  66
```

등수는 **순서 척도**다. F 5등과 4등의 차이가 2등과 1등의 차이와 같다고 볼 수 없다(4장). F가 1등인데 M이 5등인 고객은 "한 번 올 때 많이 사는 소매상이거나 비싼 상품만 사는 고객"이고, F 5등에 M 1등이면 "자주 오지만 실속이 약한 고객"이다. 등수표가 준비되면 소비자 분류를 위한 전처리가 끝난 것이다.

제외한 고객은 버리는 것이 아니다. 강의처럼 RFM 군집과 인구통계가 비슷한 그룹의 추천을 받거나, 쇼핑몰에서 가장 잘 팔리는 상품을 일괄 추천받는다.

### 4단계: F등수 × M등수 2차원 그래프

```python
import matplotlib.pyplot as plt

grid = core.groupby(["F_rank", "M_rank"]).size().reset_index(name="customers")
fig, ax = plt.subplots(figsize=(6.2, 5))
ax.scatter(grid["F_rank"], grid["M_rank"], s=grid["customers"] * 14, color="#a85443", alpha=0.55)
for r in grid.itertuples():
    ax.text(r.F_rank, r.M_rank, str(r.customers), ha="center", va="center", fontsize=8)
ax.set_xlabel("Frequency rank (1 = low, 5 = high)"); ax.set_ylabel("Monetary rank (1 = low, 5 = high)")
ax.set_title("Customers on the F-rank × M-rank grid")
ax.set_xticks(range(1, 6)); ax.set_yticks(range(1, 6))
fig.tight_layout()
fig.savefig("templates/01_fashion_bigdata/lectures_korean/images/app-ch21-fm-grid.png", dpi=130)
print(grid.sort_values("customers", ascending=False).head(5))
```

```output
    F_rank  M_rank  customers
15       5       5         66
0        1       1         59
12       4       4         48
8        3       3         42
4        2       2         34
```

<figure class="analysis-example-figure">
  <img src="templates/01_fashion_bigdata/lectures_korean/images/app-ch21-fm-grid.png" alt="Bubble chart of customers on the frequency-rank by monetary-rank grid; most customers sit on the diagonal">
  <figcaption><strong>그림 1.</strong> F등수 × M등수 격자에 놓은 고객 수. 대각선(자주 사고 많이 쓰는 고객, 드물게 사고 적게 쓰는 고객)에 고객이 몰려 있고 오른쪽 아래(자주 오지만 적게 쓰는 고객)는 적다.</figcaption>
</figure>

이 그래프에서 마케팅의 방향이 보인다. 오른쪽 위의 비중을 넓히거나 왼쪽 아래의 비중을 좁히는 활동을 하게 된다.

### 5단계: k-means 또는 마케터의 직접 구획으로 나누기

고객군을 나누는 방법은 크게 두 가지다. k-means처럼 데이터 기반 군집화를 쓰거나, 마케터가 업무 기준에 따라 경계선을 직접 지정한다. 분류 기준이 명확하지 않다면 k-means의 군집 수를 4~5개로 두고 결과를 살핀 뒤 운영 가능한 규칙으로 조정한다.

```python
from sklearn.cluster import KMeans

X = core[["F_rank", "M_rank"]].to_numpy(dtype=float)
km = KMeans(n_clusters=4, n_init=10, random_state=0).fit(X)
core["cluster"] = km.labels_
centers = pd.DataFrame(km.cluster_centers_, columns=["F_rank", "M_rank"]).round(2)
centers["customers"] = core["cluster"].value_counts().sort_index().values
print(centers)
```

```output
   F_rank  M_rank  customers
0    2.54    2.52        132
1    4.82    4.82        102
2    1.22    1.22        105
3    3.78    3.82         79
```

같은 데이터를 마케터의 규칙으로 나누면 다음과 같다. 왼쪽 그림처럼 대각선으로 나누면 "쇼핑몰에 도움을 주는 고객" 순서가 되고, 오른쪽 그림처럼 사분면으로 나누면 "방문은 많으나 구매가 적은 고객"이 따로 보인다.

```python
def rule_segment(row):
    if row["F_rank"] >= 4 and row["M_rank"] >= 4:
        return "VIP"
    if row["F_rank"] >= 4 and row["M_rank"] <= 2:
        return "자주 오지만 적게 쓰는 고객"
    if row["F_rank"] <= 2 and row["M_rank"] >= 4:
        return "드물게 크게 쓰는 고객"
    if row["F_rank"] <= 2 and row["M_rank"] <= 2:
        return "저관여 고객"
    return "중간 고객"

core["segment"] = core.apply(rule_segment, axis=1)
print(core["segment"].value_counts())
print(pd.crosstab(core["segment"], core["cluster"]))
```

```output
segment
VIP                150
저관여 고객             139
중간 고객              126
자주 오지만 적게 쓰는 고객      3
Name: count, dtype: int64
cluster           0    1    2   3
segment                          
VIP               0  102    0  48
자주 오지만 적게 쓰는 고객   3    0    0   0
저관여 고객           34    0  105   0
중간 고객            95    0    0  31
```

두 방법의 교차표를 보면 k-means 군집과 규칙 세그먼트가 대체로 겹치지만 경계의 고객은 다르게 배정된다. 분석가는 마케터가 강조하고 싶은 방향(충성도인가, 방문 대비 구매인가)을 먼저 확인하고 방법을 고른다. 반대로 마케터의 의뢰가 "컨셉을 잡아 달라"이면 여러 분류표를 보여주고 컨셉을 정하게 한다. 예를 들어 "자주 오지만 적게 쓰는 고객" 비중이 지나치게 높다면 우리 쇼핑몰에서 구경만 하고 다른 곳에서 사는 형태를 의심하고 가격을 조금 낮추는 전략을 세울 수 있다.

### 6단계: 인구통계와 구매 이력으로 군집 특성 명명

분류가 끝나면 각 그룹의 인구통계와 구매 이력으로 군집의 특성을 정의한다.

```python
profile = core.merge(customers, on="customer_id")
demo = profile.groupby("segment").agg(
    customers=("customer_id", "size"),
    recency_median=("recency", "median"),
    frequency_median=("frequency", "median"),
    monetary_median=("monetary", "median"),
    female_share=("gender", lambda s: (s == "F").mean()),
    age_20s_30s=("age_band", lambda s: s.isin(["20s", "30s"]).mean()),
    seoul_share=("region", lambda s: (s == "Seoul").mean()),
    app_share=("app_installed", "mean"),
).round(2)
print(demo)

cat_share = (completed.merge(products[["product_id", "category"]], on="product_id")
             .merge(core[["segment"]], left_on="customer_id", right_index=True)
             .pivot_table(index="segment", columns="category", values="quantity", aggfunc="sum"))
print((cat_share.div(cat_share.sum(axis=1), axis=0) * 100).round(1))
```

```output
                 customers  recency_median  frequency_median  monetary_median  female_share  age_20s_30s  seoul_share  \
segment                                                                                                                 
VIP                    150             3.0              37.5        6505746.0          0.73         0.69         0.41   
자주 오지만 적게 쓰는 고객          3             8.0              11.0         685499.0          0.67         1.00         0.33   
저관여 고객                 139            28.0               4.0         422000.0          0.68         0.72         0.45   
중간 고객                  126            12.0               8.0        1131600.0          0.76         0.73         0.38   

                 app_share  
segment                     
VIP                   0.78  
자주 오지만 적게 쓰는 고객       0.67  
저관여 고객                0.44  
중간 고객                 0.40  
category         bag  bottom  dress  outer   top
segment                                         
VIP              7.9    26.2    9.0   30.5  26.4
자주 오지만 적게 쓰는 고객  3.0     9.1    3.0    3.0  81.8
저관여 고객           9.0    25.0    8.8   23.3  34.0
중간 고객            9.2    22.3    7.7   29.9  30.9
```

이제 "VIP는 최근 1주 안에 구매했고 중앙값 30회 이상 구매하며 앱 설치 비율이 높다"처럼 한 문장으로 말할 수 있다. 성별·연령·지역 구성은 군집 사이에 큰 차이가 없는데, 이것도 결과다. 실습 데이터의 구매 행동이 인구통계와 무관하게 만들어졌기 때문이며, 실제 데이터에서는 차이가 나타날 수도 있고 나타나지 않을 수도 있다.

여기서 "인구통계도 RFM과 같은 수준으로 넣어 군집을 만들면 안 되는가?"라는 질문이 생긴다. 계산은 가능하지만 변수가 3개를 넘으면 각 군집의 특성을 명확히 설명하기 어려워진다. 나이로 설명하려 하면 매출 기여 특성이 흐려지고, 지역으로 설명하면 나이 구분이 흐려진다. 마케팅 목적이 나이·지역에 맞춰져 있다면 **나이·지역 등 핵심 기준으로 먼저 집단을 나눈 뒤 RFM으로 각 집단을 설명**하는 편이 낫다. 13장 2절의 군집 변수(bases)와 설명 변수(descriptors) 구분과 같은 원칙이다.

## 5. RFM에 최근 행동을 결합한다

RFM만 보면 오래 축적된 구매 가치는 알 수 있지만 고객이 **지금 무엇을 하려는지**는 늦게 보인다. 행동 로그를 함께 보면 같은 VIP도 서로 다르게 대응할 수 있다.

| RFM 상태 | 최근 행동 | 해석 | 적절한 다음 행동 |
|---|---|---|---|
| VIP | 14일 미방문 | 휴면 위험 | 신상품·서비스 변화 안내 |
| VIP | 같은 코트 3회 조회 | 강한 탐색 | 재고·사이즈 정보 제공 |
| 신규 | 장바구니 후 미구매 | 구매 마찰 가능 | 배송비·반품·사이즈 안내 확인 |
| 잠재 | 카테고리 반복 조회 | 관심 형성 | 해당 카테고리 탐색 경험 개선 |
| 저활동 | 메시지 반복 미반응 | 피로·무관심 | 빈도 축소 또는 발송 중단 |

### 행동 이벤트를 고객 상태로 바꾸기

이벤트 하나를 곧바로 세그먼트로 부르지 않는다. 관찰 기간과 조건을 명시해 재현 가능한 규칙으로 만든다.

```text
장바구니 이탈 = 최근 24시간 add_to_cart ≥ 1
                AND purchase = 0
                AND consent_marketing = true

관심 카테고리 = 최근 14일 동일 category view_item ≥ 3
휴면 위험 VIP = RFM_segment = VIP AND 최근 30일 session = 0
```

같은 고객이 여러 조건에 들어갈 수 있으므로 우선순위를 정한다. 결제 오류처럼 고객 피해 가능성이 큰 신호를 먼저 처리하고, 장바구니·재입고, 일반 추천 순으로 배치한다. 이미 구매한 상품이나 품절 상품을 다시 권하지 않도록 주문·재고 표를 발송 직전에 확인한다.

### 메시지는 고객의 다음 행동을 돕도록 설계한다

- **대상**: 누가 받을 자격과 동의를 갖는가?
- **시점**: 행동 후 언제 정보가 가장 유용한가?
- **내용**: 가격·재고·배송·사이즈 중 어떤 새 정보를 주는가?
- **채널**: 이메일·앱 푸시·사이트 배너 중 어디가 적절한가?
- **빈도**: 같은 고객에게 하루·주 단위 상한을 어떻게 둘 것인가?
- **중단 조건**: 구매·찜 해제·수신 거부가 발생하면 언제 멈추는가?

### 효과는 대조군으로 측정한다

메시지를 받은 고객의 구매율이 높아도 메시지 때문이라고 단정할 수 없다. 원래 구매 가능성이 높은 고객을 골랐을 수 있기 때문이다. 발송 가능 고객 중 일부를 무작위 대조군으로 남기고 **증분 전환율**을 계산한다.

```text
증분 전환율 = 메시지 그룹 구매율 - 대조군 구매율
```

구매율과 함께 수신 거부율, 알림 해제율, 반품률, 고객 문의와 메시지 빈도를 가드레일로 본다. 단기 매출이 늘어도 피로도가 크게 오르면 지속 가능한 전략이 아니다.

## 6. 평가 기준

특강 자료는 분류된 집단을 세 기준으로 평가한다고 했다(CleverTap RFM 문서 참고).

| 기준 | 질문 | 확인 방법 |
|---|---|---|
| 시장성(substantial) | 집단이 마케팅 비용을 정당화할 만큼 큰가? | 세그먼트별 고객 수와 매출 비중 |
| 차별성(differential) | 집단들이 서로 다른 반응을 보이는가? | 세그먼트별 캠페인 반응률(25장), 구매 카테고리 |
| 실행 가능성(actionable) | 집단마다 다른 조치를 실제로 할 수 있는가? | CRM 도구에 목록을 넣을 수 있는가, 조치가 준비돼 있는가 |

여기에 13장 9절의 **안정성**(기준일을 한 달 옮겨도 같은 고객이 같은 군집에 남는가)을 더한다.

```python
seg_value = profile.groupby("segment")["monetary"].agg(["size", "sum"])
seg_value["revenue_share_%"] = (seg_value["sum"] / seg_value["sum"].sum() * 100).round(1)
print(seg_value.sort_values("sum", ascending=False))
```

```output
                 size         sum  revenue_share_%
segment                                           
VIP               150  1176200706             83.2
중간 고객             126   170926844             12.1
저관여 고객            139    64116367              4.5
자주 오지만 적게 쓰는 고객     3     1979199              0.1
```

## 7. 서비스 연동과 시스템 구성

분류 결과는 고객 특성에 맞는 이벤트와 상품 추천의 기초 자료다. 쇼핑몰은 매출 상위 고객을 VVIP와 VIP로 다시 나누고, **VVIP가 구매한 상품을 VIP에게 추천**해 VIP를 VVIP로 유인하는 전략을 쓴다. 분석 결과에 대한 기획자의 해석이 분석만큼 중요하다.

<figure class="system-figure">
  <div class="system-diagram" aria-label="System architecture for RFM segmentation">
    <section><b>Source</b>Orders, customer master<small>Shop platform export / DB</small></section><i>→</i>
    <section><b>Storage</b>Warehouse tables<small>orders, customers (16장)</small></section><i>→</i>
    <section class="sd-core"><b>Weekly job</b>RFM + quintile ranks<small>pandas or SQL, snapshot date logged</small></section><i>→</i>
    <section class="sd-core"><b>Segmenter</b>k-means or rules<small>segment_id per customer, history kept</small></section><i>→</i>
    <section><b>Segment table</b>customer_id, segment, valid_from<small>versioned for stability checks</small></section><i>→</i>
    <section class="sd-human"><b>Serving</b>CRM / messaging tool<small>Kakao, push, email lists; VVIP→VIP recommendations</small></section>
  </div>
  <figcaption><strong>그림 2.</strong> RFM 세그먼트 서비스의 권장 구성. 주 1회 배치로 충분하며, 세그먼트 표를 날짜별로 보관해야 고객이 어느 세그먼트에서 어디로 이동했는지 추적할 수 있다.</figcaption>
</figure>

- 소규모 쇼핑몰은 카페24·쇼피파이의 고객 그룹 기능이나 CRM 앱에 세그먼트 목록을 CSV로 올리는 것으로 충분하다. 이 장 5절의 최근 행동 상태와 결합하면 정적인 고객 등급을 발송 가능한 트리거로 바꿀 수 있다.
- 그룹 수가 많아지면 고객마다 다른 추천을 받는 경험을 줄 수 있지만, 그만큼 다양한 추천 메뉴와 높은 사양의 컴퓨터가 필요하다. 적당한 그룹 수를 정하는 것도 분석가의 능력이다.

```python
export = profile[["customer_id", "segment", "R_rank", "F_rank", "M_rank"]].copy()
export["valid_from"] = SNAPSHOT.date()
export = export[profile["marketing_consent"]]          # 마케팅 동의 고객만
print(export.head())
print("발송 대상:", len(export), "명")
```

```output
  customer_id segment  R_rank  F_rank  M_rank  valid_from
1       C0003  저관여 고객       3       1       1  2026-07-01
3       C0005     VIP       5       5       5  2026-07-01
4       C0006   중간 고객       3       2       3  2026-07-01
5       C0008   중간 고객       2       4       3  2026-07-01
7       C0010     VIP       4       4       4  2026-07-01
발송 대상: 356 명
```

## 8. 벤치마크 데이터셋으로 확장하기

19장의 **Online Retail II**는 고객 ID가 있는 거래가 많아 RFM의 표준 연습 데이터이고, **Olist**는 주문·고객·리뷰 표가 분리되어 있어 JOIN 뒤 RFM을 만드는 연습에 맞다. **H&M** 데이터는 실제 패션 거래라서 카테고리 비중으로 군집을 설명하는 6단계를 그대로 적용할 수 있다.

```python
# skip-run: Online Retail II로 같은 RFM 표 만들기
from ucimlrepo import fetch_ucirepo
retail = fetch_ucirepo(id=502).data.original
retail["InvoiceDate"] = pd.to_datetime(retail["InvoiceDate"])
ok = retail[(retail["Quantity"] > 0) & retail["Customer ID"].notna()].copy()
ok["amount"] = ok["Quantity"] * ok["Price"]
snapshot = ok["InvoiceDate"].max() + pd.Timedelta(days=1)
rfm_uk = ok.groupby("Customer ID").agg(last=("InvoiceDate", "max"), frequency=("Invoice", "nunique"), monetary=("amount", "sum"))
rfm_uk["recency"] = (snapshot - rfm_uk["last"]).dt.days
# 이후 3~6단계 코드를 rfm_uk에 적용한다 (설명 변수는 Country 정도만 있다)
```

<div class="lesson-section-box lesson-activity-box"><strong>짧은 활동</strong></div>

1. 3단계에서 제외 기준을 "구매 1회 이하"로 바꾸고 격자 그래프가 어떻게 달라지는지 비교한다.
2. 5단계의 k를 3, 5, 6으로 바꾸어 군집 중심이 어떻게 움직이는지 표로 정리하고, 마케터에게 어느 k를 권할지 한 문장으로 쓴다.
3. R_rank까지 넣어 3차원(R·F·M)으로 k-means를 돌리고, 2차원 결과와 어느 고객이 달라지는지 확인한다.

<div class="lesson-section-box lesson-summary-box"><strong>이 장의 핵심</strong></div>

- RFM은 최근성·빈도·금액으로 고객의 행동을 요약하는 가장 기본적인 고객 분류 방법이며, 추천 시스템의 시작점으로 권장된다.
- F·M을 5분위 등수로 바꾸고, 한두 번 구매한 고객을 분리해 불균형을 줄인 뒤 2차원 격자에 놓는다.
- 나누는 방법은 k-means와 마케터의 규칙 두 가지이며, 같은 데이터라도 마케터의 의도에 따라 다른 결과가 나온다.
- 군집을 만드는 변수는 3개 이내로 두고, 인구통계와 구매 이력은 군집을 설명하는 변수로 쓴다.
- 세그먼트는 시장성·차별성·실행 가능성·안정성으로 평가하고 CRM 발송 목록으로 연결한다.

## 학습 점검

1. R·F·M 각각의 정의를 기준일과 관찰 기간을 포함해 쓰시오.
2. 한두 번 구매한 고객을 제외하고 등수를 매기는 이유는 무엇인가? 제외된 고객은 어떻게 처리하는가?
3. F 1등·M 5등인 고객과 F 5등·M 1등인 고객은 각각 어떤 고객일 가능성이 있는가?
4. 마케터의 관심이 연령대별 전략에 있을 때 권장되는 분류 설계는 무엇인가?
5. 세그먼트를 평가하는 세 기준(시장성·차별성·실행 가능성)을 이 장의 결과에 적용해 한 문장씩 쓰시오.

<details>
<summary>정답과 해설 보기</summary>

1. R은 기준일과 마지막 구매일의 간격(일), F는 관찰 기간의 구매(또는 방문) 횟수, M은 관찰 기간의 구매 금액이다. 기준일 2026-07-01, 관찰 기간 2026년 상반기처럼 명시한다.
2. 그런 고객이 대부분이어서 격자의 왼쪽 아래가 빽빽해지고 분위가 왜곡되기 때문이다. 제외 고객은 인구통계가 비슷한 군집의 추천을 받거나 베스트 상품을 일괄 추천받는다.
3. 전자는 한 번에 많이 사는 소매상이거나 고가 상품만 사는 고객, 후자는 자주 오지만 실속이 약한 고객이다.
4. RFM으로 군집을 만들지 않고 연령대·지역 등 3개 이내의 변수로 나눈 뒤 RFM으로 각 집단을 설명한다.
5. 예: VIP는 고객 수 대비 매출 비중이 커 시장성이 있다. 세그먼트별 카테고리 구성이 다르므로 차별성이 있다. CRM 도구에 목록을 올릴 수 있으므로 실행 가능하다.

</details>

## 참고문헌과 공식 자료

- Birant, D. (2011). [Data Mining Using RFM Analysis](https://doi.org/10.5772/13683). In *Knowledge-Oriented Applications in Data Mining*. IntechOpen. — 강의 슬라이드의 RFM 그림 출처.
- CleverTap. [RFM Analysis](https://docs.clevertap.com/docs/rfm). CleverTap Documentation. — 시장성·차별성·실행 가능성 기준.
- Wedel, M., & Kamakura, W. A. (2000). [Market Segmentation: Conceptual and Methodological Foundations](https://doi.org/10.1007/978-1-4615-4651-1). Kluwer. — bases와 descriptors.
- scikit-learn developers. [`sklearn.cluster.KMeans`](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html). scikit-learn API Reference.
- pandas development team. [`pandas.qcut`](https://pandas.pydata.org/docs/reference/api/pandas.qcut.html). pandas API Reference.

<div class="lesson-section-box lesson-next-box"><strong>다음 장</strong></div>

이번 장에서는 주문 기록을 고객 단위로 요약해 RFM 등수를 만들고 군집과 규칙으로 고객을 나눈 뒤 인구통계로 설명했다. 다음 장에서는 숫자가 아닌 **상품 이미지**를 벡터로 바꾸어 비슷한 상품을 찾는 이미지 유사도 추천을 다룬다.

## 핵심 용어

- **RFM**: Recency(최근성), Frequency(빈도), Monetary(금액)로 고객 행동을 요약하는 방법. 예: 최근 5일 전 구매, 상반기 12회, 96만 원.
- **5분위 등수(quintile rank)**: 값을 크기순으로 5등분해 1~5등을 매긴 순서 척도. 예: 구매 금액 상위 20%는 M 5등.
- **군집 변수(bases)**: 군집을 만드는 데 쓰는 변수. 예: F등수, M등수.
- **설명 변수(descriptors)**: 만들어진 군집을 기술하는 변수. 예: 연령대, 지역, 앱 설치 여부, 구매 카테고리.
- **k-means**: 정해진 k개의 중심에 가까운 점을 묶는 군집 방법. 예: F·M 등수 2차원에서 4개 군집.
- **규칙 기반 세그먼트(rule-based segment)**: 마케터가 정한 경계로 나눈 집단. 예: F≥4이고 M≥4이면 VIP.
- **시장성·차별성·실행 가능성(substantial·differential·actionable)**: 세그먼트가 쓸모 있는지 판단하는 세 기준.
