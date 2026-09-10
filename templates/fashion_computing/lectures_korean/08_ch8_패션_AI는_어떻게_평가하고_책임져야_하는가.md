# 패션 AI는 어떻게 평가하고 책임져야 하는가?

> **중심 질문:** 높은 정확도와 그럴듯한 이미지가 실제로 좋은 옷, 공정한 서비스, 책임 있는 의사결정을 뜻할까?
## 학습 목표

- 분류·검색·가상 착의·3D 복원·패턴 생성·로봇 조작에 맞는 지표를 구분한다.
- 한 지표의 상승이 실제 품질과 사용자 만족을 보장하지 않는 이유를 설명한다.
- 패션 데이터의 범주 체계, 몸 정보, 창작물 출처에서 생기는 위험을 점검한다.
- P501 프로젝트의 오프라인 평가와 실물 검증, 중단 기준을 함께 설계한다.

## 핵심 용어

| 용어 | 이 장에서의 뜻 |
|---|---|
| metric | 모델 결과의 한 측면을 숫자로 요약한 측정값 |
| benchmark | 데이터, 분할, 과제, 지표를 정해 모델을 비교하는 규약 |
| ontology | 의복 범주·부위·속성과 관계를 정한 지식 체계 |
| 분포 변화 | 운영 데이터가 학습·시험 데이터와 달라지는 현상 |
| 데이터 계보 | 자료의 출처, 허가, 변환, 모델 사용 이력 |
| 실물 검증 | 사람·의복·장비가 있는 실제 조건에서 효용과 위험을 확인하는 과정 |

## 1. 연구 질문: “성능이 좋다”는 무엇을 뜻하는가?
패션 AI는 하나의 과제가 아니다. 코트 분류, 비슷한 상품 검색, 가상 착의 이미지 생성, 3D 메시 복원, 패턴 제작, 천 조작은 출력이 다르다.
출력이 다르면 정답의 정의와 실패 비용도 다르므로 같은 지표로 줄 세울 수 없다. 평가는 다음 네 질문을 차례로 물어야 한다.
1. **기술적 타당성:** 정해진 시험 데이터에서 목표 출력을 얼마나 잘 맞추는가?
2. **사용자 효용:** 디자이너·패턴사·착용자가 결과를 실제로 활용할 수 있는가?
3. **운영 안전성:** 낯선 몸, 소재, 조명, 의복에서도 실패를 감지하고 복구하는가?
4. **책임성:** 데이터 권리, 개인정보, 창작자 권리, 이의 제기를 다룰 절차가 있는가?
좋은 벤치마크 점수는 첫 질문의 일부에 대한 증거다. 그 점수만으로 나머지 세 질문에 답했다고 해석하면 안 된다.
## 2. P501 코트로 보는 단순한 예
P501 코트 프로젝트에 다섯 모델이 연결되어 있다고 하자.

- 검색 모델은 “더 긴 기장의 네이비 코트” 요청에 후보를 찾는다.
- 가상 착의 모델은 고객 사진 위에 P501을 입힌 이미지를 만든다.
- 3D 모델은 고객 몸과 코트 표면의 거리를 계산한다.
- 패턴 모델은 P501의 몸판·소매 패널과 봉제 관계를 생성한다.
- 로봇은 완성 코트를 펼쳐 검사 위치에 놓는다.
한 명의 정면 사진에서 결과가 좋아 보이는 데모만으로는 이 파이프라인을 평가할 수 없다. 큰 사이즈, 휠체어 사용 자세, 짙은 옷과 어두운 배경, 광택 안감, 주름진 실물에서도 시험해야 한다.
### P501 평가 카드

| 단계 | 온라인 이전 지표 | 사람이 확인할 것 | 실물 결과 |
|---|---|---|---|
| 검색 | Recall@K | 요청한 변화와 후보의 일치 | 선택 시간·누락 |
| 가상 착의 | LPIPS·FID·사용자 선호 | 로고·단추·체형 왜곡 | 구매 판단에 준 도움 |
| 3D·패턴 | 표면 거리·봉제 정확도 | 제작 가능성·디자인 유지 | 봉제 성공·수선량 |
| 사이즈·핏 | 여유량·관통률 | 압박 위치·동작 제약 | 착용감·가동성 |
| 로봇 | 면적·성공률·행동 수 | 방향·손상·복구 | 처리 시간·불량률 |
이 카드에서 어느 한 칸도 다른 칸을 대신하지 않는다. 특히 렌더링이 자연스럽다고 사이즈가 맞는 것은 아니고, 표면 거리가 작다고 편안한 것도 아니다.
## 3. 입력·표현·수식·출력

### 3.1 분류와 속성 인식
정밀도는 모델이 “코트”라고 한 것 중 실제 코트의 비율이다.
$$
\text{Precision}=\frac{TP}{TP+FP}, \qquad
\text{Recall}=\frac{TP}{TP+FN}
$$
F1은 두 값을 조화 평균하지만 희귀 의복의 오류와 집단별 격차를 하나의 수치에 감출 수 있다. 다중 속성 문제에서는 “라펠”을 맞히고 “싱글 브레스티드”를 틀리는 식의 부분 성공도 따로 봐야 한다.
### 3.2 검색
Recall@K는 정답 상품이 상위 $K$개 안에 포함된 질의의 비율이다.
$$
R@K=\frac{1}{N}\sum_{i=1}^{N}\mathbf{1}[\text{target}_i\in\text{top-}K_i]
$$
정답 하나를 찾는 능력은 측정하지만, 상위 후보의 다양성·설명 가능성·사용자 만족은 직접 측정하지 않는다.
### 3.3 이미지 생성과 가상 착의
SSIM과 LPIPS는 기준 이미지와의 구조적·지각적 차이를, FID는 두 이미지 집합의 특징 분포 차이를 요약한다. 짝이 없는 가상 착의에는 “같은 사람이 바로 그 옷을 입은 정답 사진” 자체가 없을 수 있다. 따라서 낮은 LPIPS나 FID만으로 로고 보존, 몸 왜곡, 사이즈 판단의 정확성을 증명할 수 없다.
### 3.4 3D, 패턴, 시뮬레이션
Chamfer Distance는 예측 점 집합 $P$와 정답 점 집합 $Q$ 사이의 최근접 거리를 양방향으로 평균한다.
$$
d_{\mathrm{CD}}(P,Q)=\frac{1}{|P|}\sum_{p\in P}\min_{q\in Q}\|p-q\|^2+
\frac{1}{|Q|}\sum_{q\in Q}\min_{p\in P}\|q-p\|^2
$$
표면이 가까워도 패널 수, 결 방향, 시접, 봉제 순서가 틀리면 제작할 수 없다. 패턴은 패널 경계 오차, 패널·봉제 짝 정확도, 시뮬레이션 성공률, 전문가 평가를 함께 봐야 한다.
### 3.5 집단별 결과와 불확실성
전체 평균 $M$뿐 아니라 사이즈·체형·피부 표현·의복 범주별 $M_g$를 함께 보고한다.
$$
\text{gap}=\max_g M_g-\min_g M_g
$$
격차가 작아도 모든 집단의 성능이 낮을 수 있으므로 평균, 최저 집단, 실패 유형을 같이 제시한다. 운영 출력에는 예측값뿐 아니라 신뢰도, 적용 범위, 실패 플래그, 사람에게 넘기는 조건이 포함되어야 한다.
## 4. 대표 연구와 평가 관점의 발전

### 4.1 DeepFashion: 대규모 인식과 검색 벤치마크
[DeepFashion(CVPR 2016)](https://openaccess.thecvf.com/content_cvpr_2016/html/Liu_DeepFashion_Powering_Robust_CVPR_2016_paper.html)은 80만 장이 넘는 이미지에 범주, 속성, 랜드마크, 매장-소비자 이미지 대응을 제공했다. 대규모 비교가 가능해졌지만 웹·매장 이미지의 분포와 정해진 속성 목록이 실제 패션 세계 전체를 대표하지는 않는다.
### 4.2 Fashionpedia: 온톨로지와 국소 속성
[Fashionpedia(ECCV 2020)](https://www.ecva.net/papers/eccv_2020/papers_ECCV/html/1203_ECCV_2020_paper.php)는 전문가가 만든 27개 주요 의복, 19개 부위, 294개 속성의 온톨로지와 48,825개 이미지를 공개했다. 분할과 속성을 함께 평가할 수 있지만, 온톨로지 밖의 지역적 명칭·비서구 의복·새로운 디자인은 “없는 것”처럼 처리될 수 있다.
### 4.3 FashionIQ: 자연어 수정 기반 검색
[FashionIQ(CVPR 2021)](https://openaccess.thecvf.com/content/CVPR2021/papers/Wu_Fashion_IQ_A_New_Dataset_Towards_Retrieving_Images_by_Natural_CVPR_2021_paper.pdf)는 비슷한 상품 쌍을 구별하는 사람이 쓴 상대 설명을 제공한다. 대표 평가는 Recall@10과 Recall@50이지만, 상위 후보가 사용자의 취향을 만족하는지는 별도 사용자 연구가 필요하다.
### 4.4 VITON: 사진의 그럴듯함과 착용 판단의 차이
[VITON(CVPR 2018)](https://openaccess.thecvf.com/content_cvpr_2018/html/Han_VITON_An_Image-Based_CVPR_2018_paper.html)은 3D 정보 없이 사람 이미지에 목표 옷을 합성했다. 이미지 기반 가상 착의의 목표는 시각적 합성이며, 실제 치수·압력·동작 여유를 계산하는 피팅 시스템과 구분해야 한다.
### 4.5 Which Is Plagiarism: 유사 후보 검색과 판정
[Which Is Plagiarism(CVPR 2020)](https://openaccess.thecvf.com/content_CVPR_2020/html/Lang_Which_Is_Plagiarism_Fashion_Image_Retrieval_Based_on_Regional_Representation_CVPR_2020_paper.html)은 랜드마크 기반 부분 표현으로 변형된 유사 의복을 검색하고 Plagiarized Fashion 데이터셋을 제안했다. 논문 제목과 달리 모델의 유사도 순위는 법적 침해나 윤리적 표절을 확정하는 판결이 아니다.
공통 모티프, 시대적 양식, 라이선스, 독립 창작, 선행 디자인을 사람이 조사해야 한다.
### 4.6 실물과 제작으로 넓어진 검증
[4D-DRESS(CVPR 2024)](https://eth-ait.github.io/4d-dress/)는 64개 실제 의상, 520개가 넘는 동작 시퀀스, 7만 8천 개 3D 스캔 프레임을 제공해 합성 데이터 밖의 동적 평가를 돕는다. 그러나 32명과 특정 캡처 환경의 데이터가 모든 몸과 소재를 대표하지는 않는다.
[Design2GarmentCode(CVPR 2025)](https://openaccess.thecvf.com/content/CVPR2025/html/Zhou_Design2GarmentCode_Turning_Design_Concepts_to_Tangible_Garments_Through_Program_Synthesis_CVPR_2025_paper.html)는 텍스트·이미지·스케치를 파라메트릭 봉제 프로그램으로 바꾸고 시뮬레이션 성공과 전문가 평가를 함께 사용했다. 시뮬레이션 성공은 봉제 가능성의 한 관문일 뿐이며 얇은 끈, 비정형 몸판, 복잡한 일대다 봉제는 제한점으로 남는다.
[Dress Anyone(PACMCGIT 2025)](https://igl.ethz.ch/projects/dress_anyone/)은 미분 가능한 물리로 다른 몸에 맞춘 2D 패턴과 3D 드레이프를 최적화했다. 논문의 기하학적 맞음은 압박, 움직임, 열적 쾌적성까지 측정한 착용감과 동일하지 않다.
### 4.7 과제별 평가표

| 과제 | 자주 쓰는 지표 | 지표가 놓치는 것 | 추가 검증 |
|---|---|---|---|
| 분류·분할 | F1, mAP, IoU | 온톨로지 밖 개념, 집단별 오류 | 혼동 사례·집단별 성능 |
| 검색 | Recall@K, 순위 | 다양성, 취향, 이유 | 사용자 선택·검색 시간 |
| 가상 착의 | SSIM, LPIPS, FID | 치수, 압력, 로고 왜곡 | 세부 체크·사용자 연구 |
| 3D 복원 | Chamfer, 꼭짓점 오차 | 패턴·소재·제작성 | 패턴사 검토·실물 비교 |
| 패턴 생성 | 패널·봉제 정확도, 성공률 | 시접·공정·착용감 | 샘플 봉제·동작 시험 |
| 로봇 조작 | coverage, 성공률, 시간 | 손상·복구·작업자 위험 | 장기 실물 시험 |

## 5. 문제 발생: 정확도 밖의 책임

### 5.1 데이터와 온톨로지 편향
라벨은 중립적인 사실 목록이 아니라 누가 무엇을 중요하게 보았는지 반영한 설계다. 학습·검증·시험에 같은 촬영처나 동일 상품이 섞이면 데이터 누출로 점수가 부풀 수 있다.
시간, 브랜드, 국가, 사이즈, 의복 범주를 나눈 외부분포 시험과 누락 보고가 필요하다.
### 5.2 몸 데이터와 프라이버시
전신 사진, 치수, 3D 스캔, 자세는 재식별과 신체 추론 위험을 가진다. 필요한 최소 데이터만 수집하고 목적·보관 기간·접근 권한·삭제 방법을 사전에 정해야 한다.
원본 몸 데이터와 고객 식별자를 분리하고, 공개 데모에는 당사자의 명확한 허락이 있어야 한다. 동의를 받았다는 이유만으로 새로운 목적에 무기한 재사용해서는 안 된다.
### 5.3 저작권, 출처, 표절
학습 이미지·패턴·브랜드 자산의 라이선스와 출처를 데이터 계보에 기록한다. 생성 결과는 훈련 자료나 입력 레퍼런스와의 근접 유사성을 점검하고, 의심 사례를 자동 공개하지 않고 사람에게 보낸다.
유사도는 조사 우선순위를 정할 수 있지만 창작 경위와 권리 관계를 대신 판단하지 못한다.
### 5.4 실물 안전과 책임의 연결
모델 소유자, 데이터 담당자, 패턴사, 품질 담당자 중 누가 어떤 실패를 승인·중단할지 정한다. 사용자에게 결과의 한계와 사람이 검토했는지 표시하고, 수정·이의 제기 경로를 제공한다.
중대한 몸 왜곡, 제작 불가 패턴, 원단 손상 위험이 발견되면 평균 점수가 좋아도 출시를 멈춘다.
### 5.5 검증 사다리

1. 고정 시험셋에서 기준 모델과 재현 가능한 비교
2. 범주·사이즈·체형·촬영 조건별 오류 분석
3. 새로운 시즌·브랜드·소재의 외부분포 시험
4. 패션 전문가와 사용자의 블라인드 검토
5. 시뮬레이션과 소량 실물 샘플의 분리 보고
6. 제한된 현장 시험과 실패 복구·중단 기준 확인

이 모든 단계에서 **metric은 실물 성능과 같지 않다(metric ≠ real-world performance).** 그리고 **기하학적 fit은 착용감과 같지 않다(geometric fit ≠ comfort).**
## 짧은 활동: “높은 점수”에 반론하기

조별로 P501 시스템의 홍보 문구 “FID가 낮으므로 누구에게나 완벽하게 맞는다”를 검토한다.

1. 논리적으로 연결되지 않는 단어 두 개를 찾는다.
2. 필요한 기술 지표, 집단별 지표, 실물 지표를 하나씩 제안한다.
3. 출시를 즉시 중단할 실패 사례 하나를 정한다.
4. 과장 없는 한 문장으로 홍보 문구를 다시 쓴다.

## 이 장의 핵심

- 패션 AI의 과제마다 출력과 실패 비용이 달라 지표도 달라야 한다.
- 평균 점수는 온톨로지 밖 개념, 집단별 오류, 실물 실패를 숨길 수 있다.
- 몸 데이터는 최소 수집·목적 제한·접근 통제·삭제가 필요하고, 디자인 자료는 출처와 허가를 추적해야 한다.
- 유사도 검색은 표절 판정이 아니며, 이미지 품질과 기하학적 맞음도 실제 제작·착용 경험을 대신하지 않는다.
- 책임 있는 평가는 오프라인 점수에서 끝나지 않고 사람 검토, 실물 시험, 중단과 이의 제기 절차까지 이어진다.

## 학습 점검

1. Recall@K가 높은 검색 시스템에서도 사용자가 만족하지 않을 수 있는 이유는 무엇인가?
2. 가상 착의 이미지의 FID가 낮다는 사실로 알 수 없는 것을 두 가지 쓰자.
3. 패션 디자인 유사도 모델의 결과를 바로 “표절” 판정으로 쓰면 안 되는 이유는 무엇인가?
4. P501 패턴의 Chamfer Distance가 낮아도 실물 샘플이 실패할 수 있는 이유를 하나 들자.

<details>
<summary>정답과 해설 보기</summary>

1. 목표 상품이 상위 후보에 포함되었는지만 측정하며 후보의 다양성, 설명, 취향 적합성, 선택 부담은 직접 측정하지 않기 때문이다.
2. 실제 사이즈와 압박, 동작 여유, 로고·단추의 정확한 보존, 다양한 몸 집단의 오류 등은 별도 검증이 필요하다.
3. 시각적 유사성만으로 라이선스, 독립 창작, 공통 선행 디자인, 창작 과정을 알 수 없으므로 조사 보조 신호로만 사용해야 한다.
4. 3D 표면은 가까워도 패널 경계, 시접, 결 방향, 봉제 짝이나 소재 값이 틀려 제작과 착용에서 실패할 수 있다.

</details>

## 참고문헌

1. Liu, Z. et al. (2016). [DeepFashion: Powering Robust Clothes Recognition and Retrieval with Rich Annotations](https://openaccess.thecvf.com/content_cvpr_2016/html/Liu_DeepFashion_Powering_Robust_CVPR_2016_paper.html). CVPR.
2. Han, X. et al. (2018). [VITON: An Image-Based Virtual Try-On Network](https://openaccess.thecvf.com/content_cvpr_2018/html/Han_VITON_An_Image-Based_CVPR_2018_paper.html). CVPR.
3. Jia, M. et al. (2020). [Fashionpedia: Ontology, Segmentation, and an Attribute Localization Dataset](https://www.ecva.net/papers/eccv_2020/papers_ECCV/html/1203_ECCV_2020_paper.php). ECCV.
4. Lang, Y. et al. (2020). [Which Is Plagiarism: Fashion Image Retrieval Based on Regional Representation for Design Protection](https://openaccess.thecvf.com/content_CVPR_2020/html/Lang_Which_Is_Plagiarism_Fashion_Image_Retrieval_Based_on_Regional_Representation_CVPR_2020_paper.html). CVPR.
5. Wu, H. et al. (2021). [Fashion IQ: A New Dataset Towards Retrieving Images by Natural Language Feedback](https://openaccess.thecvf.com/content/CVPR2021/papers/Wu_Fashion_IQ_A_New_Dataset_Towards_Retrieving_Images_by_Natural_CVPR_2021_paper.pdf). CVPR.
6. Wang, W. et al. (2024). [4D-DRESS: A 4D Dataset of Real-World Human Clothing with Semantic Annotations](https://openaccess.thecvf.com/content/CVPR2024/html/Wang_4D-DRESS_A_4D_Dataset_of_Real-World_Human_Clothing_With_Semantic_CVPR_2024_paper.html). CVPR.
7. Zhou, F. et al. (2025). [Design2GarmentCode: Turning Design Concepts to Tangible Garments Through Program Synthesis](https://openaccess.thecvf.com/content/CVPR2025/html/Zhou_Design2GarmentCode_Turning_Design_Concepts_to_Tangible_Garments_Through_Program_Synthesis_CVPR_2025_paper.html). CVPR.
8. Chen, H.-Y. et al. (2025). [Dress Anyone: Automatic Physically-Based Garment Pattern Refitting](https://igl.ethz.ch/projects/dress_anyone/). *Proceedings of the ACM on Computer Graphics and Interactive Techniques, 8*(4), Article 56.

## 과정 전체 결론과 최종 프로젝트

이 과정은 이미지를 분류하는 AI에서 시작해 언어 검색, 생성, 몸·의복의 3D 표현, 봉제 패턴, 천의 물리와 로봇 조작까지 확장했다. 모든 장을 관통하는 질문은 “모델이 무엇을 출력하는가?”와 “그 출력이 실제 패션 업무의 무엇을 아직 말하지 못하는가?”였다.
최종 프로젝트에서는 P501 또는 자신이 정한 한 제품을 골라 다음 여섯 항목을 제출한다.

1. 해결할 패션 문제와 사용하지 않을 범위를 한 문장씩 정의한다.
2. 데이터 출처·라이선스·온톨로지·몸 정보 처리 방식을 데이터 카드로 작성한다.
3. 가장 단순한 기준 모델과 과제별 지표, 집단별 분석 계획을 정한다.
4. 대표 성공 세 건보다 실패 유형 최소 다섯 건을 먼저 설명한다.
5. 전문가·사용자·실물 샘플 검증과 metric을 분리해 보고한다.
6. 출시 중단 조건, 사람에게 넘길 조건, 이의 제기와 삭제 절차를 제안한다.

최종 발표의 결론은 “AI가 디자이너를 대체한다”가 아니라, **어떤 조건에서 누구의 판단을 돕고 어디서 멈춰야 하는지**를 증거로 말해야 한다.
