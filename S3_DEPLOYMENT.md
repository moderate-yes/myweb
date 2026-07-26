# Amazon S3 deployment

The browser application consists of:

- `index.html`
- `app.js`
- `styles.css`
- `site-config.js`
- `content-index.js`
- `static/`
- `templates/`

The older Flask files are not needed in the bucket.

## Bucket setup

1. Enable static website hosting and use `index.html` for both the index and error document.
2. Upload the files and folders listed above while preserving their paths.
3. Allow public reads for the website objects.
4. To discover new subject directories and Markdown files automatically, allow `s3:ListBucket` on this bucket and add a CORS rule that permits `GET` and `HEAD` from the website origin.

Example CORS configuration:

```json
[
  {
    "AllowedHeaders": ["*"],
    "AllowedMethods": ["GET", "HEAD"],
    "AllowedOrigins": ["https://your-site.example"],
    "ExposeHeaders": []
  }
]
```

Example additions to the bucket policy (replace both placeholders):

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicWebsiteObjects",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::YOUR_BUCKET_NAME/*"
    },
    {
      "Sid": "ListLectureMarkdown",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:ListBucket",
      "Resource": "arn:aws:s3:::YOUR_BUCKET_NAME",
      "Condition": {
        "StringLike": {
          "s3:prefix": ["templates/*"]
        }
      }
    }
  ]
}
```

Public object listing exposes object names under `templates/`; it does not grant write access. If public listing is disabled, the app uses the bundled `content-index.js` instead.

## Markdown workflow

Use this directory convention:

```text
templates/
  subject_directory_name/
    lectures_english/
      01_first_lecture.md
    lectures_korean/
      01_first_lecture.md
```

- A first-level directory becomes a subject menu. Underscores become spaces and each word is capitalized.
- The `lectures_english` and `lectures_korean` directory names control the language switch.
- Markdown files are ordered naturally by filename.
- The first Markdown heading becomes the document title.
- Replacing or adding a Markdown file requires no application rebuild when S3 listing is enabled.

If the site uses a custom domain, set `s3BucketUrl` in `site-config.js` to the bucket REST endpoint, such as:

```js
s3BucketUrl: "https://YOUR_BUCKET_NAME.s3.ap-northeast-2.amazonaws.com",
```

The S3 website hostname is detected automatically, so this setting can stay empty when the site is accessed directly through its `s3-website` URL.
