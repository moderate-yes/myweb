# Flask로 수익형 강의 웹사이트 만들기 5: 보안, 테스트와 배포

로컬에서 잘 보이는 사이트와 공개해도 안전한 사이트는 다르다. 마지막 글에서는 비밀번호와 비밀 키를 코드에서 분리하고, 주요 페이지를 자동으로 점검한 뒤 배포 준비를 한다.

## 비밀 값을 코드에서 분리하기

비밀번호와 Flask 세션 키를 코드에 직접 작성하면 저장소나 배포 로그를 통해 노출될 수 있다. 환경변수로 분리한다.

```python
import os

app.secret_key = os.environ['SECRET_KEY']
PORTFOLIO_PASSWORD = os.environ['PORTFOLIO_PASSWORD']
```

로컬 PowerShell에서는 현재 터미널 세션에 다음처럼 설정할 수 있다.

```powershell
$env:SECRET_KEY = "충분히-긴-무작위-문자열"
$env:PORTFOLIO_PASSWORD = "나만의-비밀번호"
python app.py
```

실제 비밀 값이 들어간 `.env` 파일을 사용한다면 Git에 커밋하지 않도록 `.gitignore`에 추가한다.

## 세션에는 인증 상태만 저장하기

세션에 사용자가 입력한 비밀번호 자체를 저장할 필요는 없다.

```python
from flask import redirect, request, session, url_for


@app.route('/portfolio_login', methods=['GET', 'POST'])
def portfolio_login():
    if request.method == 'POST':
        if request.form.get('password') == PORTFOLIO_PASSWORD:
            session['portfolio_authenticated'] = True
            return redirect(url_for('portfolio_main'))

    return render_template('portfolio_login.html')
```

이 예시는 개인 포트폴리오를 가볍게 잠그는 수준이다. 여러 사용자의 회원가입과 결제가 필요한 서비스라면 비밀번호 해시, CSRF 보호, 데이터베이스와 계정 복구 절차를 갖춘 인증 시스템을 사용해야 한다.

## 보호된 페이지 확인하기

```python
def portfolio_is_authenticated():
    return session.get('portfolio_authenticated', False)


@app.route('/portfolio_main')
def portfolio_main():
    if not portfolio_is_authenticated():
        return redirect(url_for('portfolio_login'))

    return render_template('portfolio_main.html')
```

문자열 포함 여부가 아니라 정확한 인증 상태를 확인한다. 로그아웃할 때는 해당 값을 세션에서 제거한다.

## Flask 테스트 클라이언트 사용하기

브라우저로 모든 페이지를 반복 확인하는 대신 간단한 자동 테스트를 만들 수 있다.

```python
def test_public_pages():
    client = app.test_client()

    assert client.get('/').status_code == 200
    assert client.get('/lecture').status_code == 200


def test_portfolio_requires_login():
    client = app.test_client()
    response = client.get('/portfolio_main')

    assert response.status_code == 302
    assert '/portfolio_login' in response.location
```

강의 파일을 추가한 뒤 모든 URL이 `200`을 반환하는지도 확인한다.

## 공개 실행에서 디버그 모드 끄기

```python
if __name__ == '__main__':
    app.run(
        debug=os.environ.get('FLASK_DEBUG') == '1',
        port=int(os.environ.get('PORT', '5000')),
    )
```

디버그 모드는 개발 중에는 편리하지만 내부 정보가 노출될 수 있어 공개 환경에서는 사용하지 않는다. 실제 배포에서는 개발용 서버 대신 배포 플랫폼이 권장하는 WSGI 서버와 실행 방식을 따른다.

## 배포 전 체크리스트

- `SECRET_KEY`와 비밀번호가 환경변수에 설정되어 있다.
- 디버그 모드가 꺼져 있다.
- 모든 강의 링크와 이메일 링크가 동작한다.
- 모바일 화면에서 본문을 읽을 수 있다.
- 존재하지 않는 파일 경로로 서버 파일을 읽을 수 없다.
- 광고·제휴 링크가 콘텐츠와 명확히 구분된다.
- 개인정보처리방침과 필요한 고지 문서를 준비했다.
- 이미지 용량과 페이지 로딩 속도를 확인했다.

## 수익보다 먼저 측정할 것

초기에는 광고 수익만 보는 것보다 콘텐츠가 실제로 읽히는지 확인하는 편이 중요하다.

- 어떤 강의에 방문자가 들어오는가?
- 본문을 얼마나 읽고 다음 글로 이동하는가?
- 모바일 이탈이 유난히 높은가?
- 검색한 질문에 글이 충분히 답하고 있는가?
- 광고가 독서를 방해하고 있지 않은가?

이 결과를 바탕으로 제목, 설명, 글의 순서와 예제를 개선한다. 수익형 강의 사이트의 핵심 자산은 광고 코드가 아니라 **신뢰할 수 있고 계속 업데이트되는 강의 콘텐츠**다.

## 이번 글의 실습

1. 비밀 키와 포트폴리오 비밀번호를 환경변수로 옮긴다.
2. 세션에 비밀번호가 저장되지 않는지 확인한다.
3. 공개 페이지와 보호 페이지 테스트를 작성한다.
4. 디버그 모드를 끄고 동일하게 실행되는지 확인한다.
5. 배포 전 체크리스트를 하나씩 완료한다.

여기까지 마치면 마크다운으로 글을 추가하고, 후원과 광고 영역을 운영하며, 기본적인 보안과 테스트가 적용된 Flask 강의 사이트가 완성된다.
