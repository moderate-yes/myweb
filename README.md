# ppijju.kr

Static HTML, CSS, and JavaScript website deployed to Amazon S3.

## Review changes locally

On Windows, run:

```powershell
.\start-local.ps1
```

Open <http://127.0.0.1:8000> in your browser. Refresh the page after editing,
adding, moving, or deleting Markdown files under `templates/`. The local preview
builds the subject and lecture menus directly from the current directory names.

Stop the preview with `Ctrl+C`.

If port 8000 is already being used, choose another one:

```powershell
.\start-local.ps1 -Port 8080
```

## Publish

Commit and push approved changes to the `main` branch. GitHub Actions then
synchronizes the website and Markdown files to S3 and refreshes CloudFront.
