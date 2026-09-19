# Is Virtual Try-On a Real Fitting?

## 학습 목표

가상 착의(Virtual Try-On)는 사람 사진에 다른 옷을 입힌 것처럼 보이는 이미지를 만든다. 그러나 보기 좋은 합성이 실제 핏을 뜻하지는 않으므로, 이 장은 VTON이 무엇을 계산하고 무엇을 계산하지 않는지 구분한다.

이 장을 마치면 다음을 할 수 있다.

- Image-based Virtual Try-On의 입력과 출력을 설명한다.
- 사람의 정체성·자세와 상품의 무늬를 보존해야 하는 이유를 설명한다.
- VITON에서 StableVITON까지 연구 문제의 변화를 비교한다.
- 시각적으로 자연스러운 착용 이미지와 물리적으로 정확한 피팅을 구분한다.
- 생성 이미지 평가 지표가 실제 사이즈·압박감·활동성을 보장하지 않는 이유를 말한다.

## 1. 연구 질문: 옷을 입힌다는 것은 무엇을 생성하는가?

Image-based VTON의 목표는 3D 의복을 제작하거나 실제 압력을 계산하는 것이 아니다. 입력 사진 속 사람의 정체성과 자세는 유지하면서, 별도의 상품 이미지를 그 사람의 의복 영역에 자연스럽게 합성하는 것이 기본 목표다.

좋은 결과는 적어도 세 조건을 만족해야 한다.

1. 얼굴, 머리카락, 피부와 자세가 원래 사람처럼 유지되어야 한다.
2. 칼라, 단추, 로고, 체크무늬처럼 상품을 식별하는 특징이 보존되어야 한다.
3. 팔이 옷 앞을 가리거나 소매가 몸 뒤로 넘어가는 가림 관계가 자연스러워야 한다.

이 조건들은 모두 **사진의 시각적 일관성**에 관한 것이다. 아직 실제로 단추가 잠기는지, 어깨가 끼는지, 팔을 들 수 있는지는 묻지 않았다.

## 2. 가장 단순한 예: P501 남색 오버사이즈 코트 입히기

상품 DB에 `product_id=P501`, `category=Coat`, `color=Navy`, `fit=Oversized`가 기록되어 있다고 하자. 고객의 전신 사진과 P501의 정면 상품 사진을 모델에 넣는다.

```text
사람 사진 + P501 상품 사진 + 자세·신체 영역 정보
                          ↓
            P501을 입은 것처럼 보이는 사람 사진
```

모델은 사람이 원래 입은 상의를 지운 영역을 만들고, P501의 몸판과 소매를 자세에 맞게 변형한 뒤, 보이지 않던 피부나 팔 부분까지 합성해야 한다.

결과에서 남색, 더블브레스트 단추와 코트 길이가 잘 유지되면 상품 시각화에는 도움이 된다. 그러나 출력 한 장만으로 다음 질문에는 답할 수 없다.

- 고객의 실제 가슴둘레와 P501 완성 치수의 차이는 얼마인가?
- 어깨와 암홀의 여유분이 움직임에 충분한가?
- 두꺼운 울 원단이 접히는 위치와 압력은 어떠한가?
- 안에 니트를 입었을 때도 단추가 잠기는가?

> **가상착용 이미지는 ‘입은 것처럼 보이는 결과’이지, ‘실제로 맞는다는 측정 결과’가 아니다.**

## 3. 입력·표현·수식·출력

사람 이미지를 $I_p$, 상품 이미지를 $I_g$, 자세나 신체 영역 조건을 $C_p$라고 하면 VTON을 다음처럼 단순화할 수 있다.

$$
\hat I = G(I_p, I_g, C_p)
$$

$G$는 생성 모델이고 $\hat I$는 합성된 착용 이미지다. 학습에서는 같은 옷을 실제로 입은 목표 이미지 $I_{gt}$와 비교할 수 있다.

$$
L = \lambda_1 L_{reconstruction}(\hat I,I_{gt})
+\lambda_2 L_{perceptual}(\hat I,I_{gt})
+\lambda_3 L_{garment}
$$

Reconstruction Loss는 픽셀 차이를, Perceptual Loss는 사람이 느끼는 시각적 특징의 차이를, Garment Loss는 상품 특징 보존을 줄이려는 신호다. 연구마다 실제 Loss의 구성은 다르지만 공통 목표는 자연스러운 사람 이미지와 충실한 상품 표현을 함께 얻는 것이다.

| 입력·표현 | 담는 정보 | 담지 못할 수 있는 정보 |
| --- | --- | --- |
| 사람 RGB 이미지 | 외형, 배경, 현재 자세 | 정확한 신체 치수와 가려진 표면 |
| 상품 RGB 이미지 | 보이는 색상·무늬·실루엣 | 뒷면, 패턴, 원단 물성 |
| Pose keypoints | 관절의 대략적인 위치 | 피부 표면과 의복 압력 |
| Segmentation map | 얼굴·팔·상의 등의 픽셀 영역 | 깊이와 안쪽 구조 |
| 출력 RGB 이미지 | 예상되는 시각적 외관 | 실제 맞음새와 촉감 |

## 4. 대표 연구는 무엇을 개선해 왔는가?

### VITON: 3D 없이 시작한 이미지 합성

[VITON](https://openaccess.thecvf.com/content_cvpr_2018/html/Han_VITON_An_Image-Based_CVPR_2018_paper.html)은 3D 정보를 사용하지 않고, clothing-agnostic 사람 표현을 조건으로 한 coarse-to-fine 네트워크를 제안했다. 먼저 거친 착용 이미지를 만들고 refinement network가 상품의 시각적 세부를 보완했다.

이 연구의 의미는 “가상착용에는 반드시 정교한 3D 모델이 필요하다”는 전제를 낮춘 데 있다. 반대로 3D·패턴·물성을 입력하지 않았으므로 실제 피팅을 계산했다고 해석할 근거도 없다.

### VITON-HD: 고해상도에서 드러나는 정렬 오류

[VITON-HD](https://openaccess.thecvf.com/content/CVPR2021/html/Choi_VITON-HD_High-Resolution_Virtual_Try-On_via_Misalignment-Aware_Normalization_CVPR_2021_paper.html)는 1024×768 해상도에서 상품을 변형한 영역과 목표 의복 영역의 불일치가 더 눈에 띈다는 문제를 다뤘다. ALIAS normalization과 generator를 사용해 어긋난 영역을 처리하고 고해상도 상품 디테일을 보존했다.

즉, 연구 질문이 “입혀 보이는가?”에서 “고해상도에서도 경계와 무늬가 무너지지 않는가?”로 이동했다.

### Dress Code: 상의 밖의 여러 카테고리

[Dress Code](https://openaccess.thecvf.com/content/CVPR2022W/CVFAD/html/Morelli_Dress_Code_High-Resolution_Multi-Category_Virtual_Try-On_CVPRW_2022_paper.html)는 상의에 집중된 기존 데이터의 범위를 넓혀 상의·하의·드레스가 포함된 1024×768 paired dataset과 baseline을 제안했다. 의복 종류가 달라지면 지워야 할 신체 영역과 새로 만들어야 할 가림 관계도 달라진다.

데이터셋이 넓어졌다는 것은 모든 체형과 생활 자세가 대표되었다는 뜻은 아니다. 정면의 표준화된 사진에서 잘 작동하는 모델이 앉은 자세, 복잡한 배경, 여러 겹의 옷에서도 같은 성능을 낸다고 자동으로 결론 내릴 수 없다.

### StableVITON: 잠재 공간에서 대응 관계 학습

[StableVITON](https://openaccess.thecvf.com/content/CVPR2024/html/Kim_StableVITON_Learning_Semantic_Correspondence_with_Latent_Diffusion_Model_for_Virtual_CVPR_2024_paper.html)은 사전학습된 latent diffusion model 안에서 의복과 사람의 semantic correspondence를 학습한다. Zero cross-attention block을 통해 상품 특징을 전달하고, 별도의 RGB warping 결과에만 의존하던 구조를 바꾸었다.

**Diffusion model**은 노이즈에서 점차 이미지를 복원하도록 학습한 생성 모델이다. StableVITON은 의복 이미지를 사람 위로 기하학적으로 늘여 맞추는 **warping** 대신, 잠재 공간에서 의복의 각 부분이 신체의 어느 부분에 대응하는지(**semantic correspondence**)를 학습한다. Diffusion prior는 얼굴과 신체를 그럴듯하게 만드는 데 유리하지만, 강한 생성 능력이 입력 상품에 없는 단추나 주름을 만들어내는 위험도 있다. 따라서 사진의 자연스러움과 상품 충실도를 따로 확인해야 한다.

## 5. 문제 발생: 사진이 자연스러우면 실제로도 맞을까?

아니다. VTON 입력에 신체 치수·봉제 패턴·원단 물성·접촉 조건이 없다면 물리적 피팅(**physical fit**)을 직접 계산할 수 없다.

| 평가 질문 | Image-based VTON이 주로 답하는가? |
| --- | --- |
| 이 코트가 이 사람에게 시각적으로 어떻게 보일까? | 예 |
| 로고와 단추가 상품 사진처럼 유지되는가? | 예 |
| 실제 가슴둘레와 어깨너비에 맞는가? | 아니오 |
| 특정 동작에서 당김과 압력이 생기는가? | 아니오 |
| 울과 폴리에스터가 다르게 드레이프되는가? | 물성 입력이 없다면 아니오 |

SSIM·LPIPS 같은 paired 지표나 FID·KID 같은 분포 지표, 사용자 선호 평가는 이미지 품질을 비교하는 데 도움을 준다. 그러나 낮은 이미지 오차가 사이즈 정확도나 착용 쾌적성을 증명하지 않는다. 실제 피팅을 주장하려면 치수 오차, 접촉 압력, 동작 범위, 실물 착의 비교 같은 별도의 검증이 필요하다.

또한 사람 사진은 생체·신체 정보가 포함된 개인정보다. 데이터 수집 동의, 보관 범위, 체형·피부색·성별 표현의 편향, 합성 결과의 오용 가능성을 함께 점검해야 한다.

### Python으로 의복 Mask 겹침 확인하기

가상 착의에서 예측한 의복 영역이 정답 Mask와 얼마나 겹치는지 간단한 IoU로 계산할 수 있다. 픽셀 겹침이 높아도 실제 착용감이 맞다는 뜻은 아니다.

```python
import numpy as np

ground_truth = np.array([[1, 1], [0, 1]], dtype=bool)
prediction = np.array([[1, 0], [0, 1]], dtype=bool)

intersection = np.logical_and(ground_truth, prediction).sum()
union = np.logical_or(ground_truth, prediction).sum()
print("intersection =", intersection)
print("union =", union)
print(f"mask IoU = {intersection / union:.3f}")
```

```output
intersection = 2
union = 3
mask IoU = 0.667
```

## 짧은 활동: 결과 이미지의 주장 범위 정하기

P501 가상착용 결과를 평가한다고 가정하고 다음 항목을 세 칸으로 분류해 보자.

- 사진만으로 확인 가능
- 추가 데이터가 있으면 확인 가능
- 실물 검증이 필요

항목은 `남색 보존`, `단추 개수`, `어깨 압박`, `소매 길이`, `팔을 올릴 때 활동성`, `울의 촉감`, `얼굴 정체성 보존`이다. 같은 “소매 길이”도 사진 속 상대적 외관과 실제 센티미터 치수는 다른 주장임을 함께 적는다.

## 이 장의 핵심

- Image-based VTON은 사람 이미지와 상품 이미지로 새로운 착용 이미지를 생성한다.
- 연구는 3D 없는 합성에서 고해상도·다중 카테고리·diffusion 기반 대응 학습으로 발전했다.
- 얼굴·자세 보존, 상품 디테일 보존, 자연스러운 가림 관계는 서로 다른 평가 항목이다.
- 생성 이미지의 사실감은 신체 치수와 원단 물성에 근거한 물리적 정확성과 같지 않다.
- **VTON은 시각화 도구이며, 추가 입력과 검증 없이 실제 fit 판정 도구라고 부르면 안 된다.**

## 학습 점검

1. Clothing-agnostic representation을 만드는 이유는 무엇인가?
2. VITON-HD가 저해상도 연구보다 특히 다뤄야 했던 문제는 무엇인가?
3. Dress Code 데이터셋이 넓힌 의복 범위는 무엇인가?
4. StableVITON에서 semantic correspondence는 무엇을 연결하는가?
5. VTON 결과만으로 실제 맞음새를 판정할 수 없는 이유를 세 가지 입력 정보로 설명하시오.

<details>
<summary>정답과 해설 보기</summary>

1. 사람이 원래 입은 옷의 정보를 제거하고, 얼굴·머리·자세·신체 위치처럼 새 상품을 합성할 때 유지할 조건을 남기기 위해서다.
2. 해상도가 높아지면서 warped garment와 목표 의복 영역의 misalignment, 경계 artifact와 흐려진 상품 디테일이 더 잘 보이는 문제다.
3. 기존 데이터가 주로 상의에 집중한 것과 달리 상의·하의·드레스를 포함하는 multi-category 범위를 제공했다.
4. 상품 이미지의 소매·몸판 같은 부분과 사람 이미지에서 그것이 생성되어야 할 위치를 연결한다.
5. 정확한 신체 치수, 봉제 패턴과 완성 치수, 원단의 굽힘·신축 같은 물성 및 접촉 정보가 없기 때문이다.

</details>

## 참고문헌

1. Han, X. et al. (2018). [VITON: An Image-Based Virtual Try-On Network](https://openaccess.thecvf.com/content_cvpr_2018/html/Han_VITON_An_Image-Based_CVPR_2018_paper.html). *Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR)*.
2. Choi, S. et al. (2021). [VITON-HD: High-Resolution Virtual Try-On via Misalignment-Aware Normalization](https://openaccess.thecvf.com/content/CVPR2021/html/Choi_VITON-HD_High-Resolution_Virtual_Try-On_via_Misalignment-Aware_Normalization_CVPR_2021_paper.html). *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)*.
3. Morelli, D. et al. (2022). [Dress Code: High-Resolution Multi-Category Virtual Try-On](https://openaccess.thecvf.com/content/CVPR2022W/CVFAD/html/Morelli_Dress_Code_High-Resolution_Multi-Category_Virtual_Try-On_CVPRW_2022_paper.html). *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition Workshops (CVPRW)*.
4. Kim, J. et al. (2024). [StableVITON: Learning Semantic Correspondence with Latent Diffusion Model for Virtual Try-On](https://openaccess.thecvf.com/content/CVPR2024/html/Kim_StableVITON_Learning_Semantic_Correspondence_with_Latent_Diffusion_Model_for_Virtual_CVPR_2024_paper.html). *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)*.

## 다음 장

이번 장에서는 옷을 입은 것처럼 보이는 2D 이미지를 만들었다. 다음 장에서는 카메라에 보이지 않는 뒷면과 몸 안쪽까지 추론하며 사람과 옷을 3D 구조로 복원할 수 있는지 살펴본다.

## 핵심 용어

- **Virtual Try-On(VTON)**: 사람 이미지와 별도의 의복 이미지를 이용해 그 옷을 입은 것처럼 보이는 새 이미지를 생성하는 과제.
- **Clothing-agnostic representation**: 사람이 원래 입은 옷의 정보는 지우고 자세·얼굴·머리·신체 위치처럼 유지할 정보를 남긴 표현.
- **Warping**: 평면 상품 이미지를 사람의 자세와 의복 영역에 맞게 공간적으로 변형하는 과정.
- **Semantic correspondence**: 상품 이미지의 소매·몸판 같은 부분과 사람 이미지에서 그 부분이 놓일 위치의 대응 관계.
- **Diffusion model**: 노이즈에서 시작해 조건에 맞는 이미지를 단계적으로 복원하는 생성 모델.
- **Physical fit**: 치수, 여유분, 패턴, 원단 물성, 신체 접촉과 움직임을 포함한 실제 맞음새.
