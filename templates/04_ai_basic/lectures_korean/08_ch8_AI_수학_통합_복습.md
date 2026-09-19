# AI Model Audit: From Learning Principles to Pre-Deployment Checks

## 학습 목표

AI를 이해한다는 것은 수식을 많이 외우는 것이 아니라, **무엇을 입력해 어떤 예측을 만들고, 어떤 Loss로 학습했으며, 실제 사용 전에 무엇을 검증해야 하는지 설명하는 것**이다. 마지막 장에서는 앞의 수학을 짧게 연결한 뒤 `P501 반품 위험 예측`을 Model Audit으로 완성한다.

이 장을 마치면 다음을 할 수 있다.

- Input·Target·Prediction·Parameter·Loss·Metric을 하나의 흐름으로 설명한다.
- Shape와 시간 순서를 이용해 계산 오류와 데이터 누수를 찾는다.
- 단순 기준선과 복잡한 모델을 같은 평가셋에서 비교한다.
- 평균 점수뿐 아니라 하위 집단·비용·calibration·실패 사례를 확인한다.
- 모델의 추천과 사람의 의사결정·승인을 구분한다.
- 배포 후 drift·오류·피해를 감시하고 중단 조건을 정한다.

<div class="learning-path" role="img" aria-label="AI 모델의 목적에서 데이터 학습 평가 사용 승인 관찰까지 이어지는 감사 흐름">
  <span>Purpose</span><b>→</b><span>Data</span><b>→</b><span>Learning</span><b>→</b><span>Evaluation</span><b>→</b><span>Approval</span><b>→</b><span>Monitoring</span>
</div>

## 1. 질문: Loss가 낮으면 사용할 수 있는 AI인가

Training Loss가 낮다는 것은 학습 데이터에서 목적함수가 작아졌다는 뜻이다. 다음을 자동으로 보장하지는 않는다.

- 새로운 시즌과 고객에게도 잘 작동한다.
- 중요한 소수 집단의 오류가 작다.
- 예측 확률이 실제 빈도와 맞는다.
- 모델을 사용한 행동이 고객과 사업에 도움이 된다.
- 개인정보·공정성·운영 비용 문제가 없다.

따라서 `학습 = Loss를 줄이는 Parameter W를 찾는 과정`이라는 중심 문장 뒤에는 항상 `사용 = 별도의 데이터와 실제 결과로 목적 적합성을 검증하는 과정`이 이어져야 한다.

## 2. 수학은 감사 질문을 읽는 도구다

| 수학·개념 | 모델 안에서 하는 일 | 감사할 질문 |
|---|---|---|
| Vector·Tensor·Shape | 고객·상품·문장·이미지를 계산 가능한 배열로 표현 | 각 축은 무엇이며 배치·시간·특성이 섞이지 않았는가? |
| Matrix multiplication | 입력을 Parameter로 변환 | 안쪽 차원이 맞고, 출력 각 축의 의미가 유지되는가? |
| Dot product·cosine | 임베딩의 관계와 유사도 계산 | 가까움이 실제 업무의 ‘비슷함’과 같은가? |
| Gradient·backpropagation | Loss가 줄어드는 Parameter 방향 계산 | 학습 신호가 원하는 행동과 맞는가? |
| Loss | 학습 중 줄일 수치 정의 | 쉬운 다수 사례만 잘 맞춰도 낮아지지 않는가? |
| Metric·threshold | 사용 목적에 따라 모델을 평가하고 행동 결정 | FP·FN 비용과 집단별 피해를 반영하는가? |

<details>
<summary><strong>선택 복습: 하나의 학습 loop로 수식 연결하기</strong></summary>

$$
X
\xrightarrow{f(X;W)}
\hat Y
\xrightarrow{Y\text{와 비교}}
L
\xrightarrow{\text{backprop}}
\nabla_W L
\xrightarrow{\text{optimizer}}
W_{new}
$$

- $X$는 입력, $W$는 학습할 Parameter, $\hat Y$는 예측이다.
- Loss는 예측과 Target의 차이를 학습 신호로 만든다.
- Backpropagation은 Gradient를 계산하고 Optimizer는 Parameter를 업데이트한다.
- Transformer도 Parameter와 연산 종류가 많아질 뿐 이 학습 구조를 공유한다.

정규방정식·inverse·rank·pseudoinverse의 상세 계산은 AI Math 3~4장의 선택 심화에서 확인한다.

</details>

## 3. 가장 단순한 예: P501 반품 위험 예측

`P501 남색 오버사이즈 코트` 주문이 반품될 가능성을 발송 전에 예측한다고 하자. 모델의 목적은 고객을 ‘좋은 고객·나쁜 고객’으로 분류하는 것이 아니다. 상담·사이즈 정보·재고 판단 중 어떤 제한된 행동을 도울지 먼저 정해야 한다.

| 항목 | 예시 정의 | 위험한 정의 |
|---|---|---|
| 결정 | 발송 전 사이즈 안내를 추가로 보여줄지 검토 | 고객의 주문을 자동 취소 |
| 분석 단위 | 주문 상품 한 줄 | 고객·주문·상품 행을 혼합 |
| 예측 시점 | 결제 완료 직후 | 반품 접수 이후 정보 사용 |
| Target | 배송 후 30일 안의 반품 여부 | 사유가 다른 취소와 반품을 혼합 |
| 기준선 | 전체 또는 카테고리별 반품률 | 기준선 없이 복잡한 모델만 보고 |
| 사용자 | CS·사이즈 콘텐츠 담당자 | 책임자와 행동이 정해지지 않음 |

## 4. 데이터 감사: 예측 시점에 알 수 있었는가

| 후보 입력 | 사용 가능성 | 확인할 문제 |
|---|---|---|
| 주문 시 선택한 사이즈 | 가능 | 상품별 사이즈 체계와 결측 |
| 주문 시 가격·쿠폰 | 가능 | 미래 할인 정보가 섞이지 않았는가? |
| 과거 완료 주문의 반품률 | 조건부 가능 | 현재 주문 이후 기록과 신규 고객 처리 |
| 실제 반품 사유 | 불가 | Target 발생 뒤에 생긴 누수 정보 |
| 반품 택배 접수 시각 | 불가 | 예측 결과를 사실상 미리 알려주는 정보 |
| 우편번호·연령 | 신중 | 필요성, proxy 차별, 개인정보 최소화 |

### Shape와 키를 기록한다

예를 들어 $X\in\mathbb{R}^{N\times D}$라면 $N$은 무엇의 개수이고 $D$는 어떤 특성인지 적는다. JOIN 전후 행 수, 고객·주문·상품 키의 중복과 미매칭을 확인한다. 데이터가 Tensor라면 각 축을 `batch × sequence × embedding`처럼 사람이 읽을 수 있는 말로 기록한다.

## 5. 학습 감사: Loss를 줄이는 일이 목적과 맞는가

반품이 전체의 5%라면 모두 ‘반품 아님’으로 예측해도 Accuracy 95%가 된다. Binary Cross Entropy를 사용해 학습하더라도 평가에서는 다음을 함께 본다.

| 지표 | 답하는 질문 | 단독 사용의 한계 |
|---|---|---|
| PR-AUC | 희소한 반품 사례의 순위 품질은 어떤가? | 실제 행동 임계값을 정하지 않음 |
| Recall | 실제 반품 중 얼마나 표시했는가? | 너무 많은 정상 주문을 경고할 수 있음 |
| Precision | 경고 중 실제 반품 비율은 얼마인가? | 놓친 반품 수를 숨길 수 있음 |
| Calibration | 0.7 예측이 실제 약 70%인가? | 행동의 가치와 비용은 별도 판단 |
| 운영 비용 | 안내·검토 비용과 절감 가능 비용은 얼마인가? | 고객 경험과 공정성을 하나로 표현하지 못함 |

모델은 `전체 반품률`, `상품군별 규칙`, 작은 Logistic Regression 같은 단순 기준선과 같은 Test 기간에서 비교한다. 복잡한 모델이 기준선을 안정적으로 이기지 못하면 복잡성을 채택할 이유가 약하다.

## 6. 평가셋은 평균뿐 아니라 실패를 찾도록 만든다

Train·Validation·Test는 시간 순서로 나누고, Test는 마지막 선택을 확인할 때까지 보지 않는다. 여기에 실제 사용에서 중요한 하위 집단과 어려운 사례를 포함한다.

| 평가 조각 | 확인 이유 |
|---|---|
| 신규 고객 | 과거 이력이 없는 경우 |
| 신규 상품·새 시즌 | 학습 때 없던 스타일과 정책 변화 |
| 사이즈 체계가 다른 브랜드 | 라벨·단위 불일치 |
| 할인·프로모션 기간 | 평시와 다른 구매·반품 행동 |
| 소수 체형·접근성 요구 | 평균 지표가 숨길 수 있는 피해 |
| 결측·중복·취소 주문 | 운영 데이터 오류에 대한 견고성 |

모델이나 전처리를 바꾸면 같은 고정 평가셋과 최신 기간 평가셋을 함께 사용한다. 평가셋도 데이터 범위, 라벨 기준, 버전과 한계를 문서화한다.

## 7. 예측과 행동 사이에는 사람이 결정할 정책이 있다

예측 확률 0.72가 곧 “반품할 고객”이라는 사실은 아니다. 확률을 어떤 행동으로 바꿀지는 비용·고객 경험·권리를 반영한 정책 결정이다.

<div class="operations-flow" role="img" aria-label="반품 확률을 정책과 승인 뒤 제한된 행동으로 연결하는 흐름">
  <div><strong>Model</strong><span>반품 위험 확률</span></div><b>→</b>
  <div><strong>Policy</strong><span>임계값·제외 대상·가드레일</span></div><b>→</b>
  <div><strong>Human Approval</strong><span>사용 목적·문구·대상 검토</span></div><b>→</b>
  <div class="flow-highlight"><strong>Limited Action</strong><span>사이즈 정보 제공·상담 연결</span></div>
</div>

주문 제한, 가격 변경, 고객 차별처럼 영향이 큰 행동을 모델 점수만으로 자동 실행하지 않는다. 먼저 정보 제공처럼 되돌릴 수 있는 낮은 위험의 행동을 작은 실험으로 검증한다.

## 8. 배포 후에는 모델뿐 아니라 결과를 감시한다

| 감시 대상 | 예 | 중단·재검토 신호 |
|---|---|---|
| 데이터 | 상품군·가격·고객 구성 | 학습 범위를 벗어난 큰 분포 변화 |
| 모델 | Precision·Recall·calibration | 기준선 이하 또는 특정 집단 급락 |
| 시스템 | 지연·누락·중복 | 잘못된 고객·상품에 결과 연결 |
| 고객 | 문의·불쾌감·반품 | 안내가 압박이나 차별로 받아들여짐 |
| 사업 | 검토 비용·마진·재고 | 절감보다 운영·재작업 비용이 큼 |

드리프트가 감지되었다고 무조건 재학습하지 않는다. 질문·라벨·정책·데이터 파이프라인 중 무엇이 바뀌었는지 먼저 찾는다.

### Python으로 학습·평가 데이터의 ID 중복 점검하기

같은 주문이나 고객이 학습셋과 평가셋에 동시에 들어가면 실제보다 성능이 좋아 보일 수 있다. 복잡한 모델을 돌리기 전에 식별자 중복부터 확인한다.

```python
train_customer_ids = {"C101", "C102", "C103", "C104"}
test_customer_ids = {"C104", "C201", "C202"}

overlap = train_customer_ids & test_customer_ids
print("overlap =", sorted(overlap))
print("leakage risk =", bool(overlap))
```

```output
overlap = ['C104']
leakage risk = True
```

## 최종 프로젝트: 한 장짜리 Model Audit Card

| 항목 | 작성 |
|---|---|
| 결정·사용자·예측 시점 |  |
| 분석 단위와 Input Shape |  |
| Target 정의와 라벨 기간 |  |
| 데이터 출처·권한·제외 규칙 |  |
| 누수 가능성이 큰 컬럼 |  |
| 단순 기준선과 후보 모델 |  |
| Loss와 그 한계 |  |
| Test 분할과 평가셋 버전 |  |
| 핵심 Metric·calibration·FP/FN 비용 |  |
| 하위 집단과 실패 사례 |  |
| 사람이 승인할 행동 |  |
| 배포 후 지표·중단·복구 조건 |  |

### 최종 판단문

> “이 모델은 ___ 시점의 ___을 이용해 ___을 예측한다. ___ 기준선과 비교해 ___ 평가셋에서는 ___했지만, ___에서는 한계가 있다. 따라서 ___ 행동만 사람이 승인해 시험하며, ___이면 중단하고 기존 ___ 방식으로 되돌린다.”

## 전체 강의 핵심 정리

- 파라미터 기반 모델의 학습은 Loss를 줄이는 Parameter를 찾는 과정이다.
- 데이터는 Vector·Matrix·Tensor로 표현되며 Shape는 축의 의미와 계산 가능성을 보여준다.
- Gradient와 backpropagation은 학습을 가능하게 하지만 좋은 사용 결과를 보장하지 않는다.
- Embedding과 Attention의 관계는 학습 데이터와 목표가 정한 표현이다.
- Train·Validation·Test를 분리하고 단순 기준선, 실패 사례와 하위 집단을 평가한다.
- 예측 확률, 정책, 사람의 결정과 실제 행동을 구분한다.
- 배포 이후 데이터·모델·시스템·고객·사업 결과를 감시하고 중단·복구 조건을 갖춘다.

## 학습 점검

1. Training Loss가 낮아도 바로 배포하면 안 되는 이유를 세 가지 쓰시오.
2. 반품 완료 후 생긴 정보를 발송 전 예측에 쓰면 어떤 문제가 생기는가?
3. 불균형한 반품 데이터에서 Accuracy만으로 평가하기 어려운 이유는 무엇인가?
4. 예측 확률과 실제 행동 정책은 왜 구분해야 하는가?
5. 복잡한 모델을 단순 기준선과 비교해야 하는 이유는 무엇인가?
6. 배포 후 성능이 떨어졌을 때 재학습 전에 확인할 대상을 세 가지 쓰시오.

<details>
<summary>정답과 해설 보기</summary>

1. 새로운 데이터의 일반화, 하위 집단 성능, calibration, 실제 행동 효과, 개인정보·비용을 Training Loss가 보장하지 않기 때문이다.
2. 예측 시점에 알 수 없는 미래 정보가 들어간 데이터 누수이며 Test 점수가 비현실적으로 높아진다.
3. 다수인 정상 주문만 예측해도 Accuracy가 높을 수 있어 실제 반품 탐지 능력을 숨기기 때문이다.
4. 같은 확률도 FP·FN 비용, 고객 경험, 권리와 승인 기준에 따라 다른 행동으로 연결되어야 하기 때문이다.
5. 복잡성이 실제 추가 가치를 만드는지, 운영 비용과 설명 부담을 감수할 이유가 있는지 확인하기 위해서다.
6. 입력 분포와 스키마, 라벨·정책, 데이터 파이프라인, 시스템 연결, 고객·사업 환경 변화 등을 확인한다.

</details>

## 참고문헌과 공식 자료

- Mitchell, M. et al. (2019), [Model Cards for Model Reporting](https://doi.org/10.1145/3287560.3287596).
- Gebru, T. et al. (2021), [Datasheets for Datasets](https://www.microsoft.com/en-us/research/publication/datasheets-for-datasets/).
- NIST, [AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework).
- scikit-learn, [Precision-Recall](https://scikit-learn.org/stable/auto_examples/model_selection/plot_precision_recall.html).
- scikit-learn, [Probability calibration](https://scikit-learn.org/stable/modules/calibration.html).

## 다음 학습으로 연결

AI Basic을 마쳤다면 관심에 따라 길을 선택한다. 수식을 더 깊게 계산하려면 AI Math의 핵심 장부터 읽고, 패션 AI 연구의 실제 입력·출력·평가를 보고 싶다면 Fashion Computing의 코어 트랙으로 이동한다. 어떤 길을 택하더라도 모델 이름보다 **목적·데이터·근거·평가·실패·책임**을 먼저 묻는다.
