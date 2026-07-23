# Flask로 수익형 강의 웹사이트 만들기 3: 마크다운 강의 시스템

강의를 HTML로 직접 작성하면 문단을 추가할 때마다 태그를 신경 써야 한다. 마크다운을 사용하면 글쓰기에 집중하면서 제목, 목록, 코드와 표를 표현할 수 있다.

이번 글에서는 `templates/lectures` 폴더의 마크다운 파일을 자동으로 메뉴에 표시하고, 선택한 글을 HTML로 변환한다.

## 강의 파일 이름 규칙

파일명 앞에 순서를 붙이면 별도의 데이터베이스 없이 정렬할 수 있다.

```text
templates/lectures/
├─ 01_intro_시작하기.md
├─ 02_html_템플릿.md
└─ 03_markdown_강의_시스템.md
```

파일명은 정렬과 URL에 사용하고, 실제 화면 제목은 마크다운의 첫 번째 `# 제목`을 사용한다.

## 마크다운 목록 읽기

```python
import os


def get_lecture_files():
    lectures_dir = os.path.join(app.template_folder, 'lectures')
    if not os.path.exists(lectures_dir):
        return []

    return sorted(
        filename
        for filename in os.listdir(lectures_dir)
        if filename.endswith('.md')
    )
```

`sorted()`는 파일명 앞 번호를 기준으로 강의 순서를 유지한다. `.md`가 아닌 파일은 목록에서 제외한다.

## 선택한 강의를 HTML로 변환하기

```python
import markdown
from markupsafe import Markup


@app.route('/lecture')
@app.route('/lecture/<filename>')
def lecture(filename=None):
    files = get_lecture_files()

    if filename is None and files:
        filename = os.path.splitext(files[0])[0]

    content = None
    current = None

    if filename and f'{filename}.md' in files:
        path = os.path.join(app.template_folder, 'lectures', f'{filename}.md')

        with open(path, encoding='utf-8') as lecture_file:
            source = lecture_file.read()

        content = Markup(markdown.markdown(
            source,
            extensions=['fenced_code', 'tables', 'codehilite', 'toc']
        ))
        current = filename

    return render_template(
        'lecture_main.html',
        md_files=files,
        content=content,
        current=current,
    )
```

요청받은 파일이 실제 강의 목록에 포함되어 있는지 확인하는 과정이 중요하다. 사용자가 입력한 경로를 그대로 열면 의도하지 않은 서버 파일에 접근할 가능성이 생긴다.

## 사이드바 메뉴 만들기

```html
<ul class="lecture-list">
  {% for file in md_files %}
    {% set name = file[:-3] %}
    {% set display_name = name.split('_')[2:] | join(' ') %}
    <li>
      <a class="{% if current == name %}active{% endif %}"
         href="/lecture/{{ name }}">
        {{ display_name }}
      </a>
    </li>
  {% endfor %}
</ul>
```

현재 읽고 있는 글에는 `active` 클래스를 적용해 독자가 위치를 쉽게 알 수 있게 한다.

## 본문 템플릿 구성

```html
{% extends 'base.html' %}

{% block body %}
<div class="lecture-layout">
  <aside>{% include 'lecture_nav.html' %}</aside>

  <main>
    {% if content %}
      <article class="md-content">{{ content }}</article>
    {% else %}
      <p>등록된 강의가 없습니다.</p>
    {% endif %}
  </main>

  <aside class="revenue-sidebar">
    광고와 후원 영역
  </aside>
</div>
{% endblock %}
```

## LaTeX 수식 표시하기

수학이나 데이터 강의라면 MathJax를 연결해 LaTeX 문법을 사용할 수 있다.

```html
<script>
  window.MathJax = {
    tex: {
      inlineMath: [['$', '$']],
      displayMath: [['$$', '$$']]
    }
  };
</script>
<script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
```

마크다운에는 다음과 같이 작성한다.

```text
인라인 수식은 $f(x)$처럼 작성한다.

$$
f(x) = ax + b
$$
```

## 이번 글의 실습

1. 번호가 붙은 마크다운 파일 세 개를 만든다.
2. 파일 목록이 사이드바에 자동으로 나타나는지 확인한다.
3. `/lecture`에서 첫 번째 글이 바로 표시되게 한다.
4. 코드 블록, 표와 LaTeX 수식을 하나씩 작성한다.
5. 존재하지 않는 강의 주소에서 서버 파일이 노출되지 않는지 확인한다.

다음 글에서는 오른쪽 사이드바에 후원 안내와 광고 슬롯을 배치하고, 독서를 방해하지 않는 수익 구조를 설계한다.
