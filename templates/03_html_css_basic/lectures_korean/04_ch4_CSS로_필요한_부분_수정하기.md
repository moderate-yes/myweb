# Editing Only What You Need with CSS

## 학습 목표

기존 페이지를 통째로 다시 만들지 않고 필요한 부분만 고치려면 CSS 규칙이 어떤 요소에 적용되는지 알아야 한다. 이 장은 선택자·속성·값의 구조와 수정 범위를 안전하게 좁히는 방법을 다룬다.

이 장을 마치면 다음을 할 수 있다.

- CSS 규칙의 선택자, 속성과 값을 구분한다.
- 태그·class·자손 선택자를 목적에 맞게 사용한다.
- cascade와 specificity 때문에 스타일이 적용되지 않는 상황을 설명한다.
- box model과 최소한의 반응형 규칙을 적용한다.

## 1. CSS 규칙은 대상과 변경 내용으로 나뉜다

```css
.analysis-card {
  max-width: 720px;
  padding: 20px;
  border: 1px solid #c9c9c6;
  border-radius: 8px;
  background: #f6f6f3;
}
```

`.analysis-card`는 **선택자**, 중괄호 안의 `padding`과 `background`는 **속성**, `20px`과 `#f6f6f3`은 **값**이다. HTML에서 같은 class를 가진 요소에 이 규칙이 적용된다.

## 2. 처음에는 세 종류의 선택자면 충분하다

```css
p { color: #333; }                       /* 모든 p 요소 */
.source-note { font-size: 0.875rem; }    /* 해당 class */
.analysis-card h2 { margin-top: 0; }     /* 카드 안의 h2 */
```

| 선택자 | 범위 | 사용할 때 |
|---|---|---|
| `p` | 모든 같은 태그 | 페이지 전체 기본값을 정말 바꿀 때 |
| `.source-note` | 해당 class가 붙은 모든 요소 | 재사용할 역할 스타일 |
| `.analysis-card h2` | 카드 내부의 하위 제목 | 특정 영역 안으로 범위를 제한할 때 |

`#result`, `div:nth-child(7)`처럼 위치에 강하게 의존하는 선택자는 구조가 조금만 바뀌어도 깨지기 쉽다. 기존 프로젝트의 class 이름을 먼저 재사용하고, 새 이름이 필요하면 역할을 드러내게 정한다.

## 3. box model로 간격 문제를 읽는다

모든 요소는 내용(content)을 중심으로 padding, border, margin이 둘러싼 상자로 계산된다.

```css
.analysis-card {
  box-sizing: border-box;
  width: 100%;
  padding: 16px;  /* 테두리 안쪽 여백 */
  border: 1px solid #bbb;
  margin: 24px 0; /* 다른 요소와의 바깥 간격 */
}
```

텍스트가 테두리에 붙으면 `padding`, 카드 사이가 너무 좁으면 `margin`을 확인한다. 폭이 100%인데 padding 때문에 넘친다면 `box-sizing: border-box`가 있는지 확인한다.

## 4. 분석 표와 그림에 최소 스타일 적용하기

```css
.result-table-wrap {
  max-width: 100%;
  overflow-x: auto;
}

.result-table {
  width: 100%;
  border-collapse: collapse;
}

.result-table th,
.result-table td {
  padding: 8px 12px;
  border: 1px solid #d5d5d2;
  text-align: right;
}

.result-table th:first-child,
.result-table td:first-child {
  text-align: left;
}

.analysis-figure img {
  display: block;
  max-width: 100%;
  height: auto;
}
```

좁은 화면에서 열이 많은 표를 억지로 압축하면 값과 머리글이 읽히지 않는다. 표를 감싼 영역에 가로 스크롤을 허용하고, 이미지는 컨테이너보다 커지지 않도록 한다.

```html
<div class="result-table-wrap">
  <table class="result-table">
    <!-- 표 내용 -->
  </table>
</div>
```

## 5. 문제 발생: 내가 쓴 CSS가 적용되지 않는다

브라우저는 여러 CSS 규칙이 같은 속성을 지정하면 cascade에 따라 하나를 선택한다. 같은 조건에서는 보통 더 구체적인 선택자가 우선하고, 구체성도 같으면 뒤에 선언한 규칙이 이긴다.

```css
p { color: #333; }
.analysis-card p { color: #555; }
```

카드 안의 문단에는 두 번째 규칙이 더 구체적이어서 적용된다. 적용이 안 된다고 곧바로 `!important`를 붙이지 않는다. 검사 도구의 Styles 패널에서 취소선이 그어진 규칙과 실제로 이긴 선택자를 확인한다. 필요하면 범위를 분명하게 하되 선택자를 지나치게 길게 만들지 않는다.

## 6. 화면 크기에 따라 꼭 필요한 부분만 조정한다

```css
@media (max-width: 640px) {
  .analysis-card {
    padding: 12px;
  }

  .analysis-card h2 {
    font-size: 1.25rem;
  }
}
```

미디어 쿼리는 특정 화면 조건에서만 규칙을 적용한다. 그러나 고정 폭을 많이 쓰지 않고 `max-width: 100%`와 자연스러운 문서 흐름을 사용하면 미디어 쿼리 없이 해결되는 문제도 많다. 특정 휴대전화 기종보다 콘텐츠가 실제로 깨지는 지점을 기준으로 확인한다.

## 짧은 활동

3장의 표와 그래프에 class를 추가하고 다음을 적용한다.

1. 표의 숫자는 오른쪽, 첫 번째 열은 왼쪽 정렬한다.
2. 표가 좁은 화면에서 잘리지 않고 가로로 확인되게 한다.
3. 그래프 너비가 부모 영역을 넘지 않게 한다.
4. 검사 도구에서 어떤 선택자가 최종 값을 만들었는지 확인한다.

## 이 장의 핵심

- CSS는 선택자로 대상을 찾고 속성과 값으로 표현을 바꾼다.
- 전체 태그보다 역할 class를 사용하면 수정 범위를 통제하기 쉽다.
- padding은 안쪽, margin은 바깥 간격이다.
- 스타일 충돌은 `!important`보다 cascade와 specificity를 먼저 확인한다.
- 표와 이미지는 좁은 화면에서 정보가 사라지지 않는지 검증한다.

## 학습 점검

1. `.analysis-card h2`는 어떤 요소를 선택하는가?
2. `padding`과 `margin`의 차이는 무엇인가?
3. 스타일이 적용되지 않을 때 `!important`를 먼저 쓰지 말아야 하는 이유는 무엇인가?

<details><summary>정답과 해설 보기</summary>

1. `analysis-card` class가 붙은 요소 안에 있는 모든 `h2`를 선택한다.
2. padding은 내용과 테두리 사이의 안쪽 여백, margin은 요소 바깥의 다른 요소와의 간격이다.
3. 충돌 원인을 숨기고 이후 수정이 더 어려워질 수 있으므로 실제로 이긴 선택자와 선언 순서를 먼저 확인해야 한다.

</details>

## 참고문헌과 공식 문서

- [MDN: CSS 선택자](https://developer.mozilla.org/docs/Web/CSS/CSS_Selectors)
- [MDN: CSS specificity](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Cascade/Specificity)
- [MDN: box model](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Box_model)
- [MDN: 반응형 웹 디자인](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/CSS_layout/Responsive_Design)

## 다음 장

마지막 장에서는 기존 프로젝트에서 수정 대상을 찾고, 작게 고친 뒤 접근성·모바일·콘텐츠 정확성을 검증하는 전체 작업 흐름을 연습한다.

> **화면이 원하는 모습으로 바뀌었다면 작업이 끝난 것일까? 다른 장과 모바일 화면까지 안전한지 어떻게 확인할까?**

