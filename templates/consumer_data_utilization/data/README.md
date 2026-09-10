# 가상 패션몰 공통 실습 데이터

실제 고객 정보가 아닌 교육용 합성 데이터다. 모든 금액은 원화이며 날짜는 ISO 8601 형식이다.

| 파일 | 기본키 | 연결키 | 주요 주의점 |
| --- | --- | --- | --- |
| `products.csv` | `product_id` | — | 가격은 목록가이며 거래 가격과 다를 수 있음 |
| `customers.csv` | `customer_id` | — | 동의 상태가 false인 고객은 마케팅 실습에서 제외 |
| `orders.csv` | `order_id` | `customer_id`, `product_id` | 취소·반품을 순매출 계산에 반영 |
| `events.csv` | `event_id` | `customer_id`, `product_id`, `order_id` | 익명 방문은 customer_id가 비어 있을 수 있음 |

권장 순서: 데이터 로드 → Shape·결측·중복 확인 → 키 관계 검증 → 분석 기간과 분모 정의 → 지표 계산 → 결과와 제외 규칙 기록.

이 데이터는 작아서 통계적 결론을 내리기 위한 표본이 아니다. 코드와 질문 정의를 연습하고 재현 가능한 결과 형식을 익히는 데 사용한다.
