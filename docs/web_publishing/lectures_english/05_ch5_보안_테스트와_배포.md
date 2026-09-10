# Flask 5: Building a Revenue-Generating Lecture Website — Security, Testing, and Deployment

A site that looks fine locally is different from a site that's safe to make public. In this final post, we separate passwords and secret keys out of the code, automatically check the main pages, and prepare for deployment.

## Separating Secret Values from the Code

If passwords and the Flask session key are written directly in the code, they can be exposed through the repository or deployment logs. Separate them out as environment variables.

```python
import os

app.secret_key = os.environ['SECRET_KEY']
PORTFOLIO_PASSWORD = os.environ['PORTFOLIO_PASSWORD']
```

In a local PowerShell session, you can set these for the current terminal session like this.

```powershell
$env:SECRET_KEY = "충분히-긴-무작위-문자열"
$env:PORTFOLIO_PASSWORD = "나만의-비밀번호"
python app.py
```

If you use a `.env` file containing actual secret values, add it to `.gitignore` so it isn't committed to Git.

## Store Only Authentication State in the Session

There's no need to store the password the user entered itself in the session.

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

This example is at the level of lightly locking a personal portfolio. A service that needs multi-user sign-up and payment should use a full authentication system with password hashing, CSRF protection, a database, and an account recovery process.

## Checking a Protected Page

```python
def portfolio_is_authenticated():
    return session.get('portfolio_authenticated', False)


@app.route('/portfolio_main')
def portfolio_main():
    if not portfolio_is_authenticated():
        return redirect(url_for('portfolio_login'))

    return render_template('portfolio_main.html')
```

Check the exact authentication state, not just whether a string is present. When logging out, remove that value from the session.

## Using the Flask Test Client

Instead of repeatedly checking every page in the browser, you can build simple automated tests.

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

After adding lecture files, also check that every URL returns `200`.

## Turning Off Debug Mode for Public Deployment

```python
if __name__ == '__main__':
    app.run(
        debug=os.environ.get('FLASK_DEBUG') == '1',
        port=int(os.environ.get('PORT', '5000')),
    )
```

Debug mode is convenient during development but can expose internal information, so don't use it in a public environment. For actual deployment, follow the WSGI server and execution method recommended by your deployment platform instead of the development server.

## Pre-Deployment Checklist

- `SECRET_KEY` and passwords are set as environment variables.
- Debug mode is turned off.
- All lecture links and email links work.
- Body content can be read on mobile screens.
- Server files cannot be read via a nonexistent file path.
- Ad and affiliate links are clearly distinguished from content.
- A privacy policy and other necessary disclosure documents are prepared.
- Image size and page load speed have been checked.

## What to Measure Before Revenue

Early on, it's more important to check whether content is actually being read than to look only at ad revenue.

- Which lectures are visitors coming into?
- How much of the body content do they read before moving to the next post?
- Is mobile drop-off unusually high?
- Does the post sufficiently answer the question that was searched for?
- Are the ads interfering with reading?

Use these results to improve titles, descriptions, post order, and examples. The core asset of a revenue-generating lecture site is not the ad code, but **trustworthy, continually updated lecture content**.

## Exercises for This Post

1. Move the secret key and portfolio password into environment variables.
2. Check that the password is not stored in the session.
3. Write tests for the public pages and the protected page.
4. Turn off debug mode and check that it runs the same way.
5. Complete the pre-deployment checklist item by item.

Once you've finished up to this point, you'll have a complete Flask lecture site where you can add posts in markdown, run a sponsorship and ad area, and have basic security and testing in place.
