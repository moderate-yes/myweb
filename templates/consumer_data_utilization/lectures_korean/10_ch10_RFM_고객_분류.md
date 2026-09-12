# 빠른 고객 기준선 만들기: RFM에서 행동 검증까지

> **학습 우선순위**
> RFM은 최신 개인화 모델을 대신하는 정답이 아니라 적은 데이터로 빠르게 설명 가능한 기준선을 만드는 방법이다. 점수표 자체보다 기준 기간·환불 처리·집단 안정성·후속 실험을 이해하는 것이 핵심이며, 상세 점수 계산과 k-평균은 선택 실습으로 읽어도 된다.

모든 고객에게 같은 메시지를 보내기보다 최근 구매 고객, 반복 구매 고객, 고액 구매 고객을 구분하면 목적에 맞는 전략을 세울 수 있다. 이 장에서는 거래 기록을 고객별 **Recency·Frequency·Monetary**로 요약하고, 규칙 기반 점수와 k-평균 군집화를 구분해 사용한다.

## 생각해 보기: 어떤 고객이 더 중요한가?

“자주 방문하지만 거의 사지 않는 고객”과 “가끔 오지만 올 때 많이 사는 고객” 중 누가 더 중요한가? RFM은 **구매 거래**를 요약하는 방법이므로 방문만 하고 사지 않은 고객은 기본 RFM에 나타나지 않는다. 방문 행동까지 보고 싶다면 별도의 행동 지표로 정의해야 한다.

| 목적 | 먼저 볼 고객 | 이유 |
|---|---|---|
| 휴면 방지 | 과거 F·M은 높지만 R이 낮아진 고객 | 가치가 있었으나 최근 구매가 멀어짐 |
| 신상품 안내 | R이 높고 해당 카테고리를 산 고객 | 최근 관계와 상품 관련성이 있음 |
| VIP 유지 | F·M이 높고 R도 높은 고객 | 반복적·최근의 매출 기여 |
| 방문→구매 전환 | 방문은 많지만 주문이 없는 고객 | RFM이 아니라 행동 로그 분석 대상 |

> **핵심 관찰**
> “좋은 고객”의 정답은 하나가 아니다. 세분화 목적, 비용과 고객 경험을 먼저 정해야 한다.

## 학습 목표

- R·F·M의 관찰 기간, 기준일과 거래 정의를 명확히 쓸 수 있다.
- 주문 행을 고객별 RFM 표로 집계할 수 있다.
- 원시 Recency의 방향과 R 점수의 방향을 구분할 수 있다.
- 규칙 기반 점수와 k-평균 군집화를 구분할 수 있다.
- k-means 전에 로그 변환·표준화가 필요한 이유를 설명할 수 있다.
- 세분화 변수를 프로필 변수와 구분하고 결과를 실험으로 평가할 수 있다.

## 핵심 용어

- **Recency(R)**: 기준일에서 마지막 구매일까지 지난 일수. 원시값은 작을수록 최근이다.
- **Frequency(F)**: 관찰 기간 동안의 고유 구매 주문 수.
- **Monetary(M)**: 관찰 기간 동안의 순구매 금액.
- **세분화(segmentation)**: 비슷한 특징을 가진 고객을 실행 가능한 그룹으로 나누는 과정.
- **분위수 점수(quantile score)**: 값을 같은 수의 집단으로 나누어 부여한 상대 점수.
- **표준화(standardization)**: 단위가 다른 변수를 평균 0, 표준편차 1의 비슷한 척도로 바꾸는 처리.

## 1. RFM의 정의부터 고정하기

예를 들어 기준일이 2026-08-01이고 관찰 기간이 직전 1년이라면 다음처럼 정의할 수 있다.

\[
R_i = \text{기준일} - \text{고객 }i\text{의 마지막 구매일}
\]

\[
F_i = \text{고객 }i\text{의 고유 완료 주문 수}
\]

\[
M_i = \sum \text{고객 }i\text{의 결제액} - \sum \text{취소·반품액}
\]

| 항목 | 이 장의 정의 | 자주 생기는 오류 |
|---|---|---|
| 기준일 | 데이터 마지막 날 다음 날 | 고객마다 다른 기준일 사용 |
| 관찰 기간 | 기준일 직전 12개월 | 전체 영업 기간을 섞어 오래된 고객에 유리 |
| R | 마지막 **구매** 후 지난 일수 | 로그인과 구매를 섞음 |
| F | 고유 완료 주문 ID 수 | 한 주문의 상품 행 수를 구매 횟수로 셈 |
| M | 취소·반품을 뺀 순구매액 | 배송비·세금·쿠폰 처리 규칙이 없음 |

RFM을 방문 기준으로 변형할 수는 있지만, 그때는 `마지막 방문`, `세션 수`라고 명시해 구매 RFM과 구분한다.

## 2. 거래 기록을 고객별 한 행으로 바꾸기

```python
import pandas as pd

orders["order_date"] = pd.to_datetime(orders["order_date"])
snapshot_date = orders["order_date"].max().normalize() + pd.Timedelta(days=1)

valid = orders.loc[
    (orders["order_status"] == "completed") &
    orders["customer_id"].notna()
].copy()

rfm = valid.groupby("customer_id").agg(
    Recency=("order_date", lambda x: (snapshot_date - x.max().normalize()).days),
    Frequency=("order_id", "nunique"),
    Monetary=("net_amount", "sum")
)
```

[`pandas.DataFrame.groupby`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.groupby.html)와 [`GroupBy.agg`](https://pandas.pydata.org/docs/reference/api/pandas.core.groupby.DataFrameGroupBy.agg.html)는 거래 행을 고객별 요약표로 바꾼다.

<div class="operations-flow" aria-label="거래표에서 고객별 RFM 표로 집계">
  <div><strong>거래표</strong><span>고객 A · 주문 101</span><span>고객 A · 주문 102</span><span>고객 B · 주문 103</span></div>
  <b>↓</b>
  <div class="flow-highlight"><strong>고객별 한 행: 마지막 구매 간격 · 고유 주문 수 · 순구매액</strong></div>
</div>

고객 ID가 없는 비회원 주문, 취소·부분 반품, 통화와 중복 주문을 어떻게 처리했는지 기록한다. 세분화 결과는 이 정의에 따라 달라진다.

## 3. 선택 실습: 점수 방향을 ‘5점=좋음’으로 통일하기

원시 Recency는 **작을수록** 좋지만, R 점수는 최근 고객일수록 높게 만든다. F와 M은 원시값이 클수록 점수도 높다.

| 지표 | 원시값의 좋은 방향 | 점수의 좋은 방향 | 예시 |
|---|---|---|---|
| Recency | 낮음 | 높음 | 3일 전 구매→R 5점 |
| Frequency | 높음 | 높음 | 주문 12회→F 5점 |
| Monetary | 높음 | 높음 | 120만원→M 5점 |

```python
# 5점이 항상 더 좋은 상태가 되도록 방향을 맞춘다.
rfm["R_score"] = pd.qcut(
    rfm["Recency"].rank(method="first"), 5, labels=[5, 4, 3, 2, 1]
).astype(int)

rfm["F_score"] = pd.qcut(
    rfm["Frequency"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5]
).astype(int)

rfm["M_score"] = pd.qcut(
    rfm["Monetary"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5]
).astype(int)

rfm["RFM_code"] = (
    rfm["R_score"].astype(str) +
    rfm["F_score"].astype(str) +
    rfm["M_score"].astype(str)
)
```

[`pandas.qcut`](https://pandas.pydata.org/docs/reference/api/pandas.qcut.html)은 순위를 비슷한 인원 수의 구간으로 나눈다. 동일값이 많으면 경계가 불안정할 수 있으므로 고객 수, 동점 처리와 구간별 실제 값 범위를 함께 확인한다.

> **즉시 해석**
> `RFM=555`는 세 지표 모두 이 고객 집단 안에서 상위 분위라는 뜻이다. 절대적으로 충성 고객이라는 보증이나 미래 구매 확률은 아니다.

## 4. RFM을 2차원에 보이는 방법

RFM이 “원래 3차원 그래프”인 것은 아니다. 고객을 세 숫자로 표현한 표다. 화면에서 F와 M을 축으로 그릴 때 R을 색·크기로 표현하면 세 정보를 모두 보존할 수 있다.

| 시각 요소 | 표현하는 값 | 읽는 질문 |
|---|---|---|
| x축 | Frequency | 얼마나 자주 샀는가? |
| y축 | Monetary | 얼마나 많이 썼는가? |
| 점의 색 | Recency | 얼마나 최근에 샀는가? |
| 점 하나 | 고객 한 명 | 어느 고객군에 가까운가? |

```python
import matplotlib.pyplot as plt

plot = plt.scatter(
    rfm["Frequency"],
    rfm["Monetary"],
    c=rfm["Recency"],
    cmap="viridis_r",
    alpha=0.6
)
plt.xlabel("고유 주문 수(F)")
plt.ylabel("순구매액(M)")
plt.colorbar(plot, label="마지막 구매 후 경과일(R)")
plt.show()
```

FM만 보는 것은 계산 비용을 줄이기 위한 필수 절차가 아니라 **시각화를 위한 투영**이다. 세분화나 행동 결정에서 Recency가 중요하다면 버리지 않는다.

## 5. 두 가지 고객군 생성 방법

<div class="comparison-cards">
  <section class="concept-card"><span class="concept-icon">📏</span><h3>규칙 기반</h3><p>R·F·M 분위 점수와 업무 규칙으로 그룹을 정한다.</p><small>설명과 실행이 쉽지만 경계가 사람이 정한 규칙에 좌우됨</small></section>
  <section class="concept-card"><span class="concept-icon">🧩</span><h3>k-means</h3><p>연속형 R·F·M에서 가까운 고객을 k개 중심에 배정한다.</p><small>패턴 탐색에 유용하지만 스케일·k·초기값 검증 필요</small></section>
</div>

규칙 기반 예시는 다음과 같다.

| 고객군 | 예시 규칙 | 가능한 질문 |
|---|---|---|
| 최근 핵심 고객 | R≥4, F≥4, M≥4 | 유지 혜택이 필요한가? |
| 신규 고객 | R≥4, F=1 | 두 번째 구매를 어떻게 도울까? |
| 이탈 위험 고가치 | R≤2, F≥4, M≥4 | 최근 구매가 멀어진 이유는? |
| 저활성 | R≤2, F≤2, M≤2 | 연락 비용 대비 가치가 있는가? |

이 규칙은 예시다. 점수 경계에 있는 두 고객의 실제 차이는 작을 수 있다.

## 6. 선택 실습: k-평균을 사용할 때의 전처리와 검증

k-means는 유클리드 거리를 사용한다. 구매액의 숫자 범위가 구매 횟수보다 훨씬 크면 M이 거리를 지배한다. RFM은 보통 오른쪽으로 긴 분포이므로 로그 변환과 [`StandardScaler`](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html)를 검토한다.

```python
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

X_log = np.log1p(rfm[["Recency", "Frequency", "Monetary"]])
X = StandardScaler().fit_transform(X_log)

scores = {}
for k in range(2, 7):
    model = KMeans(n_clusters=k, random_state=42, n_init="auto")
    labels = model.fit_predict(X)
    scores[k] = silhouette_score(X, labels)

best_k = max(scores, key=scores.get)
model = KMeans(n_clusters=best_k, random_state=42, n_init="auto")
rfm["cluster"] = model.fit_predict(X)
```

[`KMeans`](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html)은 k를 스스로 정하지 않는다. [`silhouette_score`](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.silhouette_score.html)는 군집 내부 응집과 군집 간 분리를 비교하지만, 가장 높은 점수가 자동으로 가장 유용한 고객군을 보장하지 않는다.

| 확인 항목 | 질문 |
|---|---|
| 분포 | 극단적 구매액이 중심을 끌어당기는가? |
| 스케일 | R·F·M 중 하나가 거리 계산을 지배하는가? |
| 안정성 | 시점·초기값이 달라져도 비슷한 군집이 나오는가? |
| 규모 | 너무 작은 군집이 생기지 않는가? |
| 설명 가능성 | 각 군집을 RFM 중앙값으로 설명할 수 있는가? |
| 실행 가능성 | 서로 다른 메시지·혜택을 실제 운영할 수 있는가? |

k-means는 비슷한 크기의 둥근 군집을 잘 찾는 경향이 있다. 실제 고객 분포가 길거나 복잡하면 다른 방법이나 명확한 업무 규칙이 더 나을 수 있다.

## 7. 세분화 기준과 프로필 변수를 구분하기

나이·지역·선호 카테고리를 처음부터 넣는 것이 항상 틀린 것은 아니다. 다만 목적 없이 변수를 늘리면 거리의 의미와 고객군 설명이 흐려질 수 있고, 민감한 특성에 대한 차별 위험도 커진다.

<div class="operations-flow" aria-label="세분화 변수와 프로필 변수의 역할">
  <div><strong>세분화</strong><span>R·F·M으로 행동 그룹 생성</span></div>
  <b>↓</b>
  <div><strong>프로필</strong><span>카테고리 선호</span><i>·</i><span>채널</span><i>·</i><span>지역 분포</span></div>
  <b>↓</b>
  <div class="flow-highlight"><strong>설명 가능한 행동 가설을 만들고 차별·프라이버시를 검토</strong></div>
</div>

프로필 차이는 원인이 아니다. “이탈 위험군에 특정 지역이 많다”는 관찰만으로 지역이 이탈을 일으켰다고 말할 수 없다.

## 8. 고객군을 행동과 실험으로 연결하기

VVIP가 산 상품을 VIP에게 추천하면 VIP가 VVIP로 성장할 수 있다는 것은 **가설**이다. 상품 적합성, 메시지 피로도와 할인의 순이익을 대조군과 비교해야 한다.

| 고객군 | 행동 가설 | 성공 지표 | 보호 지표 |
|---|---|---|---|
| 신규 고객 | 첫 구매 관련 상품 안내가 2차 구매를 돕는다 | 30일 2차 구매율 | 수신 거부율 |
| 이탈 위험 고가치 | 재입고·신상품 개인화가 복귀를 돕는다 | 재활성률·순이익 | 할인 비용·불만 |
| 최근 핵심 | 선공개 혜택이 유지에 도움 된다 | 유지율·마진 | 과도한 혜택 비용 |
| 저활성 | 발송 빈도를 줄여 비용과 피로를 낮춘다 | 고객당 순이익 | 장기 이탈률 |

세분화 전후 매출만 비교하면 계절이나 캠페인 효과가 섞인다. 가능하면 무작위 홀드아웃이나 A/B 테스트로 증분 효과를 본다.

## 짧은 활동: 손으로 RFM 점수 매기기

기준일은 8월 1일이고, 모두 최근 3개월의 **고유 완료 주문 수와 순구매액**이다. 기존 FM 활동에 Recency를 복원한다. `5점=좋음`을 지킨다.

| 고객 | R(최근성) | F(빈도) | M(금액) | R 점수 | F 점수 | M 점수 |
|---|---:|---:|---:|---:|---:|---:|
| A | 4 | 12 | 850,000 |  |  |  |
| B | 42 | 3 | 1,200,000 |  |  |  |
| C | 2 | 15 | 90,000 |  |  |  |
| D | 80 | 1 | 50,000 |  |  |  |
| E | 18 | 8 | 400,000 |  |  |  |

고객이 5명이므로 각 지표에서 가장 좋은 값에 5점, 다음에 4점 … 가장 낮은 값에 1점을 준다. 그 뒤 다음을 적는다.

1. 최근 핵심 고객에 가장 가까운 고객은 누구인가?
2. 저빈도·고금액 고객은 누구이며, 어떤 추가 정보를 확인할 것인가?
3. 고빈도·저금액 고객에게 고가 상품을 무조건 추천하면 어떤 문제가 생길까?

## 9. 생성형 AI 시대에 RFM을 사용하는 위치

생성형 AI는 고객군 이름과 메시지 초안을 빠르게 만들 수 있지만, 고객의 의도·민감한 특성·미래 구매를 자동으로 확정하지 못한다. RFM 결과는 `설명 가능한 기준선 → 소규모 메시지 또는 서비스 실험 → 전환·피로·수익·공정성 확인`의 출발점으로 사용한다. 개인화 모델과 비교할 때는 같은 평가 기간과 고객군에서 단순 RFM 기준선을 실제로 이기는지 확인한다.

## 이 장의 핵심

- 기본 RFM은 구매 기준이다. 방문·로그인은 별도 행동 지표로 정의한다.
- R은 기준일부터 마지막 구매일까지의 일수, F는 고유 주문 수, M은 순구매액이다.
- 원시 R은 작을수록 최근이지만 R 점수는 높을수록 좋게 뒤집어, 세 점수 모두 5점=좋음으로 통일한다.
- FM 산점도는 RFM의 시각화 투영이며, R을 색이나 크기로 보존할 수 있다.
- 분위 점수·업무 규칙과 k-means는 서로 다른 세분화 방법이다.
- k-means에는 로그 변환, 표준화, k 선택, 안정성·설명 가능성·실행 가능성 검증이 필요하다.
- 인구통계·선호 정보는 군집을 설명하는 프로필로 쓸 수 있지만 원인으로 단정하거나 차별적으로 사용하면 안 된다.
- 고객군별 전략은 자동 정답이 아니라 A/B 테스트와 순이익·수신 거부 등으로 검증할 가설이다.

## 학습 점검

1. R·F·M을 이 장의 구매 기준으로 각각 정의하시오.
2. 원시 Recency와 R 점수의 좋은 방향은 왜 반대인가?
3. FM 산점도에서 Recency를 버리지 않고 표현하는 방법은 무엇인가?
4. 규칙 기반 세분화와 k-means의 차이는 무엇인가?
5. k-means 전에 RFM을 표준화하는 이유는 무엇인가?
6. VIP→VVIP 추천 전략이 곧바로 사실이 아니라 가설인 이유는 무엇인가?

<details>
<summary>정답과 해설 보기</summary>

1. R은 기준일에서 마지막 구매일까지 지난 일수, F는 관찰 기간의 고유 완료 주문 수, M은 취소·반품 등을 반영한 순구매액이다.
2. 원시 R은 지난 일수라 작을수록 최근이다. 점수는 세 항목 모두 높을수록 좋은 상태로 읽기 위해 최근 고객에게 높은 R 점수를 준다.
3. x축 F, y축 M을 쓰고 점의 색이나 크기로 R을 표현한다.
4. 규칙 기반은 사람이 정한 분위 점수와 업무 경계로 그룹을 만든다. k-means는 표준화된 연속값에서 거리상 가까운 고객을 k개 중심에 배정한다.
5. 단위와 숫자 범위가 큰 M 등이 거리 계산을 지배하지 않도록 같은 척도로 맞추기 위해서다.
6. 다른 고객이 산 상품이 VIP에게 맞는지, 메시지가 실제 추가 구매를 만들었는지 알 수 없으며 계절·할인 효과도 섞일 수 있으므로 대조군 실험이 필요하다.

</details>

## 알아볼 것: 생성형 AI로 풀어보는 과제

1. 가상 거래 20행을 만들게 한 뒤 주문 행과 고유 주문 수를 혼동하지 않았는지 검사한다.
2. 같은 RFM 표를 규칙 기반과 k-means로 각각 나눠 고객이 다르게 배정되는 이유를 설명한다.
3. 군집 이름을 AI에게 제안받고, 데이터에 없는 성격·소득·취향을 추측한 이름은 제거한다.

> **알아두기**
> 그룹 수와 경계에는 보편적 정답이 없다. 재현성, 실행 비용, 고객 경험과 증분 성과를 함께 보고 선택한다.

## 참고문헌과 공식 문서

- Fader, P. S., Hardie, B. G. S., & Lee, K. L. (2005). [RFM and CLV: Using Iso-Value Curves for Customer Base Analysis](https://www.brucehardie.com/papers/018/). *Journal of Marketing Research*, 42(4), 415–430.
- UCI Machine Learning Repository. [Online Retail](https://archive.ics.uci.edu/dataset/352/online+retail). Transaction dataset with invoices, customers, quantities and prices.
- pandas development team. [`DataFrame.groupby`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.groupby.html), [`GroupBy.agg`](https://pandas.pydata.org/docs/reference/api/pandas.core.groupby.DataFrameGroupBy.agg.html), [`qcut`](https://pandas.pydata.org/docs/reference/api/pandas.qcut.html). pandas API Reference.
- scikit-learn developers. [`StandardScaler`](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html), [`KMeans`](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html), [`silhouette_score`](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.silhouette_score.html). scikit-learn documentation.

## 다음 장

이번 장에서는 거래를 고객별 RFM으로 요약하고, 일관된 점수 방향과 검증 가능한 세분화 절차를 만들었다. 다음 장에서는 상품 사진을 고차원 임베딩으로 바꿔 시각적으로 가까운 옷을 검색하는 과정을 다룬다.
