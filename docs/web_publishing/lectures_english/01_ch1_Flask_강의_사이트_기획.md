# Flask 1: Building a Revenue-Generating Lecture Website — Planning and Development Environment

In this series, we'll build a markdown-based lecture site from scratch using the Python web framework **Flask**. Rather than simply copying finished code, the goal is to add features one step at a time and learn the basic structure of web development.

The finished site will include the following features.

- Top navigation
- A markdown lecture list and body content
- A sponsorship/donation inquiry area
- A Google AdSense or Coupang Partners ad area
- A password-protected portfolio
- A responsive screen readable on mobile as well

> Revenue is a result that follows once enough content that's genuinely useful to visitors has accumulated. Focus on creating lectures worth reading before worrying about ad placement.

## Why Choose Flask

Flask is a lightweight Python web framework where you assemble the features you need yourself. Relatively little is handled automatically, which makes it good for learning how routing, templates, static files, and sessions connect to each other.

In this project, you'll learn the following concepts.

1. Routing, which connects a URL to a Python function
2. Jinja templates, which reuse HTML
3. Static files such as CSS and images
4. The process of converting markdown to HTML
5. Sessions, which remember login state

## Creating the Project Folder

Start with the following structure.

```text
app/
├─ app.py
├─ templates/
│  ├─ main.html
│  └─ lectures/
└─ static/
   ├─ css/
   └─ image/
```

By default, Flask looks for HTML in the `templates` folder and serves CSS and images from the `static` folder. The lecture manuscripts are kept as markdown files under `templates/lectures`.

## Installing Required Packages

Create a virtual environment, then install Flask and Markdown.

```bash
python -m venv .venv
```

On Windows PowerShell, activate the virtual environment with the following command.

```powershell
.\.venv\Scripts\Activate.ps1
pip install flask markdown
```

Recording package versions makes it easy to recreate the same environment on another computer.

```bash
pip freeze > requirements.txt
```

## The Smallest Flask App

Write the following code in `app.py`.

```python
from flask import Flask

app = Flask(__name__)


@app.route('/')
def home():
    return '<h1>Hello, Flask!</h1>'


if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

`@app.route('/')` means "run the `home()` function when the browser requests the main address." Use `debug=True` only during development, and turn off debug mode on a public server.

After running it, open `http://127.0.0.1:5000` in your browser to check the first screen.

## Designing the Revenue Model First

There are broadly three revenue paths to consider for a lecture site.

- **Display ads**: Place ads in areas that don't interfere with the body content.
- **Affiliate marketing**: Introduce products or services related to the lectures and use affiliate links.
- **Direct sponsorship**: Receive sponsorship from readers or companies who resonate with the site's purpose.

Ads and affiliate links must always be clearly marked as such so readers can recognize them. Before applying any of these to your service, also check the latest operating policies and relevant laws for each advertising platform.

## Exercises for This Post

1. Create the project folder and virtual environment.
2. Install Flask and Markdown.
3. Output `Hello, Flask!` at the `/` address.
4. Write, in one sentence, the lecture topic you want to create and your expected audience.
5. Decide which revenue model — ads, affiliate, or sponsorship — suits your site.

In the next post, we'll separate the HTML that was being returned as a string into a template file, and build navigation shared across multiple pages.
