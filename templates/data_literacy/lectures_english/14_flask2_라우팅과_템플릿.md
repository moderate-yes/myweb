# Flask 2: Building a Revenue-Generating Lecture Website — Routing and Templates

In the first post, we ran the smallest possible Flask app. Now we'll create the main, lecture, and portfolio pages and build a shared navigation.

## Splitting Pages with Routing

Routing connects a URL to the Python function that should run.

```python
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def main():
    return render_template('main.html')


@app.route('/lecture')
def lecture():
    return render_template('lecture_main.html')


@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')
```

`render_template()` reads HTML from the `templates` folder and delivers it to the browser. Keep URL names short and clearly meaningful.

## Building a Shared Layout

If you copy the navigation into every HTML file, you'll have to fix multiple files whenever you change the menu. Using Jinja's template inheritance lets you manage the shared structure in one place.

Create `templates/base.html`.

```html
<!doctype html>
<html lang="ko">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{% block title %}나의 강의 사이트{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/main.css') }}">
  </head>
  <body>
    {% include 'main_nav.html' %}
    {% block body %}{% endblock %}
  </body>
</html>
```

A `block` is a slot that changes per page, and `include` is a feature that pulls in another template fragment.

## Building the Navigation

Write `templates/main_nav.html`.

```html
<nav class="top-nav" aria-label="주요 메뉴">
  <a href="/lecture">lecture</a>
  <a href="/">contact</a>
  <a href="/portfolio">portfolio</a>
</nav>
```

In a real service, it's good practice to indicate the current page. You can use Flask's `request.endpoint` to check which function is currently running.

```html
<a class="{% if request.endpoint == 'lecture' %}active{% endif %}"
   href="/lecture">lecture</a>
```

## Inheriting in Individual Pages

`templates/main.html` inherits the shared layout and only writes the body content it needs.

```html
{% extends 'base.html' %}

{% block title %}contact · 나의 강의 사이트{% endblock %}

{% block body %}
  <main class="contact-main">
    <h1>안녕하세요</h1>
    <a href="mailto:hello@example.com">hello@example.com</a>
  </main>
{% endblock %}
```

## Linking Static Files

Place CSS, images, and JavaScript in the `static` folder. Instead of writing paths directly, using `url_for()` lets you build addresses safely even in a deployment environment.

```html
<img src="{{ url_for('static', filename='image/main.png') }}"
     alt="사이트 캐릭터">
```

## Basic Layout CSS

```css
html,
body {
  margin: 0;
  min-height: 100%;
  font-family: system-ui, sans-serif;
}

.top-nav {
  display: flex;
  justify-content: center;
  gap: 1rem;
  padding: 1rem;
}

.top-nav a {
  color: #666;
  text-decoration: none;
}

.top-nav a.active {
  color: #111;
  font-weight: 700;
}
```

## Exercises for This Post

1. Create the main, lecture, and portfolio routes.
2. Create the shared `base.html` and the navigation.
3. Bold the menu item for the current page.
4. Load the CSS and character image from the `static` folder.
5. Check what response comes back when visiting an arbitrary address.

In the next post, we'll implement a small content system that reads markdown files and automatically builds the lecture menu and body content.
