# 가상 패션몰 실습 데이터 (fashion_mall)

APPLICATION 파트의 실습 장에서 사용하는 합성 데이터다. 실제 고객·상품 정보가 아니며 `scripts/generate_fashion_mall_data.py`로 재생성할 수 있다(난수 시드 고정). 기간은 2026-01-01~2026-06-30, 기준일(snapshot)은 2026-07-01이다.

| 파일 | 행 | 기본키 | 연결키 | 쓰는 장 |
| --- | ---: | --- | --- | --- |
| `products.csv` | 80 | `product_id` | — | 20·22·23·24·26·30·36·39 |
| `customers.csv` | 600 | `customer_id` | — | 21·25·27·31·39 |
| `orders.csv` | 12625 | `order_id`+`line_no` | `customer_id`, `product_id` | 20·21·24·27·30·39 |
| `events.csv` | 49317 | `event_id` | `session_id`, `customer_id`, `product_id` | 21·24·25·31·36·38·39 |
| `clicks.csv` | 18673 | — | `session_id` | 31 |
| `reviews.csv` | 1400 | `review_id` | `product_id`, `customer_id` | 29·37 |
| `product_names_past.csv` / `product_names_recent.csv` | 200 / 200 | `rank` | — | 23 |
| `market_keywords.csv` | 390 | `week_start`+`keyword` | — | 26 |
| `campaigns.csv` | 1305 | `campaign_id`+`customer_id` | `customer_id` | 21·25 |
| `price_history.csv` | 14480 | `product_id`+`date` | `product_id` | 30 |
| `competitor_promos.csv` | 30 | — | — | 30 |
| `injected_anomalies.csv` | 39 | — | `product_id` | 20 (정답 라벨) |
| `images/P###.png` | 80 | `product_id` | — | 22·39 |

주의 사항

- `orders.csv`의 `status`가 `cancelled`·`returned`인 행은 순매출 계산에서 제외한다.
- `orders.csv`에는 고객의 `signup_date`보다 앞선 주문이 일부 있다. 비회원 구매가 나중에 계정에 연결된 경우로 간주하며, 코호트 분석(31장)에서는 제외한다.
- `events.csv`의 익명 세션은 `customer_id`가 비어 있다. `variant`는 2026년 5월 결제 화면 A/B 테스트 배정(A/B)이며 그 외 기간은 빈값이다.
- `detail` 컬럼은 이벤트 유형마다 뜻이 다르다. `search`는 `검색어|결과수`, `apply_filter`는 `필터=값`, `view_category`는 카테고리, `session_start`는 유입 경로다.
- `reviews.csv`의 `aspect_labels`는 텍스트 분류 실습의 정답 라벨이다. 실제 리뷰 데이터에는 이런 라벨이 없다.
- `injected_anomalies.csv`는 20장에서 탐지 결과를 채점하기 위한 정답이다. 실제 판매 데이터에는 없다.
- 이미지는 카테고리별 실루엣과 색상만 다른 단순 그림이다. 실제 상품 사진은 19장의 벤치마크 데이터셋을 사용한다.
