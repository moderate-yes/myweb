# Flask 3: Building a Revenue-Generating Lecture Website — The Markdown Lecture System

If you write lectures directly in HTML, you have to worry about tags every time you add a paragraph. With markdown, you can focus on writing while still expressing headings, lists, code, and tables.

In this post, we'll automatically display the markdown files in the `templates/lectures` folder in the menu, and convert the selected post into HTML.

## Lecture File Naming Convention

Prefixing filenames with an order number lets you sort them without a separate database.

```text
templates/lectures/
├─ 01_intro_시작하기.md
├─ 02_html_템플릿.md
└─ 03_markdown_강의_시스템.md
```

The filename is used for sorting and the URL, while the actual on-screen title uses the markdown's first `# heading`.

## Reading the Markdown List

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

`sorted()` keeps the lecture order based on the number prefix in the filename. Files that aren't `.md` are excluded from the list.

## Converting the Selected Lecture to HTML

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

It's important to verify that the requested file is actually included in the real lecture list. Opening a user-supplied path directly creates the possibility of accessing unintended server files.

## Building the Sidebar Menu

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

Applying the `active` class to the post currently being read helps readers easily know where they are.

## Structuring the Body Template

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

## Displaying LaTeX Equations

For a math or data lecture, you can connect MathJax to use LaTeX syntax.

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

Write it in markdown as follows.

```text
인라인 수식은 $f(x)$처럼 작성한다.

$$
f(x) = ax + b
$$
```

## Exercises for This Post

1. Create three numbered markdown files.
2. Check that the file list appears automatically in the sidebar.
3. Make the first post display immediately at `/lecture`.
4. Write a code block, a table, and a LaTeX equation, one each.
5. Check that server files are not exposed when visiting a lecture address that doesn't exist.

In the next post, we'll place a sponsorship notice and ad slot in the right sidebar, and design a revenue structure that doesn't interfere with reading.
