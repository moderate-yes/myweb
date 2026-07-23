from flask import Flask, render_template, session, request, redirect, url_for
from markupsafe import Markup
import markdown
import os
import re

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'development-secret-key')
PORTFOLIO_PASSWORD = os.environ.get('PORTFOLIO_PASSWORD', '1234')


def portfolio_is_authenticated():
    return session.get('portfolio_authenticated', False)

LECTURE_LANGS = {'korean', 'english'}

# 과목(디렉터리) 키 -> 내비게이션에 표시할 라벨.
# templates/ 바로 아래에 lectures_english 또는 lectures_korean 하위 폴더를
# 가진 디렉터리는 자동으로 하나의 "과목"으로 인식된다(get_lecture_subjects 참고).
# 라벨을 지정하지 않으면 폴더명을 보기 좋게 변환해 사용하므로, 새 과목
# (예: consumer_data_application)을 추가할 때는 templates/ 아래에 폴더와
# lectures_english/lectures_korean 하위 폴더만 만들면 되고, 표시 이름을
# 다르게 하고 싶을 때만 아래에 항목을 추가하면 된다.
SUBJECT_LABELS = {
    'data_literacy': 'Data Literacy',
    'consumer_data_utilization': 'Activate User Data',
}

DEFAULT_SUBJECT = 'data_literacy'

def get_lecture_subjects():
    """templates/ 바로 아래에서 lectures_english/lectures_korean 폴더를 가진
    디렉터리를 강의 "과목"으로 인식해 반환한다."""
    base = app.template_folder
    subjects = []
    if os.path.isdir(base):
        for name in sorted(os.listdir(base)):
            path = os.path.join(base, name)
            if not os.path.isdir(path):
                continue
            if not any(os.path.isdir(os.path.join(path, f'lectures_{lang}')) for lang in LECTURE_LANGS):
                continue
            subjects.append({
                'key': name,
                'label': SUBJECT_LABELS.get(name, name.replace('_', ' ').title()),
            })
    return subjects

def get_lectures_dir(subject, lang):
    if lang not in LECTURE_LANGS:
        lang = 'korean'
    return os.path.join(app.template_folder, subject, f'lectures_{lang}')

def get_lecture_files(subject, lang):
    lectures_dir = get_lectures_dir(subject, lang)
    if not os.path.exists(lectures_dir):
        return []
    return sorted([f for f in os.listdir(lectures_dir) if f.endswith('.md')])

# 내비게이션 바 너비에 맞도록 "Chapter 1:", "Flask 1: ... 웹사이트 만들기" 같은
# 반복되는 상위 카테고리 표현은 제목에서 제거하고 핵심 소제목만 남긴다.
NAV_TITLE_STRIP_PATTERNS = [
    re.compile(r'^Chapter\s+\d+:\s*', re.IGNORECASE),
    re.compile(r'^Flask\s+\d+:\s*Building a Revenue-Generating Lecture Website\s*[—-]\s*', re.IGNORECASE),
    re.compile(r'^Flask로\s*수익형\s*강의\s*웹사이트\s*만들기\s*\d+\s*:\s*'),
]

def get_lecture_title(subject, lang, filename):
    """마크다운 파일의 첫 H1 헤딩을 내비게이션 제목으로 사용한다."""
    lectures_dir = get_lectures_dir(subject, lang)
    filepath = os.path.join(lectures_dir, filename)
    title = None
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line.startswith('#'):
                    title = line.lstrip('#').strip()
                    break
    except OSError:
        pass
    if title is None:
        title = os.path.splitext(filename)[0]

    for pattern in NAV_TITLE_STRIP_PATTERNS:
        stripped = pattern.sub('', title).strip()
        if stripped:
            title = stripped
    return title

def get_lecture_nav_items(subject, lang):
    return [
        {'name': os.path.splitext(f)[0], 'title': get_lecture_title(subject, lang, f)}
        for f in get_lecture_files(subject, lang)
    ]

@app.route('/')
def main():
    return render_template("main.html")

@app.route('/lecture')
@app.route('/lecture/<filename>')
def lecture(filename=None):
    lang = request.args.get('lang', 'english')
    if lang not in LECTURE_LANGS:
        lang = 'english'

    subjects = get_lecture_subjects()
    subject_keys = [s['key'] for s in subjects]
    subject = request.args.get('subject', DEFAULT_SUBJECT)
    if subject not in subject_keys:
        subject = subject_keys[0] if subject_keys else DEFAULT_SUBJECT

    # 사이드바에서 과목별 아코디언을 렌더링할 수 있도록 과목마다 챕터 목록을 채운다.
    for s in subjects:
        s['nav_items'] = get_lecture_nav_items(s['key'], lang)

    md_files = get_lecture_files(subject, lang)
    nav_items = next((s['nav_items'] for s in subjects if s['key'] == subject), [])
    content = None
    current = None

    if filename is None and md_files:
        filename = os.path.splitext(md_files[0])[0]

    if filename:
        lectures_dir = get_lectures_dir(subject, lang)
        filepath = os.path.join(lectures_dir, filename + '.md')
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                md_text = f.read()
            content = Markup(markdown.markdown(
                md_text,
                extensions=['fenced_code', 'tables', 'codehilite', 'toc', 'nl2br']
            ))
            current = filename

    return render_template(
        "lecture_main.html",
        md_files=md_files,
        nav_items=nav_items,
        subjects=subjects,
        subject=subject,
        content=content,
        current=current,
        lang=lang,
    )

@app.route('/portfolio_login', methods=['GET', 'POST'])
def portfolio_login():
    if portfolio_is_authenticated():
        return redirect(url_for('portfolio_main'))

    if request.method == 'POST':
        if request.form.get('password') == PORTFOLIO_PASSWORD:
            session['portfolio_authenticated'] = True
            return redirect(url_for('portfolio_main'))
        return render_template('portfolio_login.html', login_error=True)

    return render_template('portfolio_login.html')

@app.route('/portfolio_main')
def portfolio_main():
    if not portfolio_is_authenticated():
        return redirect(url_for('portfolio_login'))
    return render_template('portfolio_main.html')

@app.route('/portfolio_resume')
def portfolio_resume():
    if not portfolio_is_authenticated():
        return redirect(url_for('portfolio_login'))
    return render_template('portfolio_resume.html')

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('portfolio_authenticated', None)
    return redirect(url_for('portfolio_login'))

if __name__ == '__main__':
    app.run(
        debug=os.environ.get('FLASK_DEBUG') == '1',
        port=int(os.environ.get('PORT', '5001')),
    )
