/*
 * For a custom domain, set s3BucketUrl to the bucket's REST URL, for example:
 * "https://my-bucket.s3.ap-northeast-2.amazonaws.com"
 *
 * On an *.s3-website.* URL the app normally detects this automatically.
 * Public S3 object listing + CORS lets new folders and Markdown files appear
 * without rebuilding content-index.js.
 */
window.SITE_CONFIG = Object.freeze({
  s3BucketUrl: "https://ppujju.s3.ap-northeast-2.amazonaws.com",
  contentPrefix: "templates/",
  defaultSubject: "fashion_bigdata_1",
  defaultLanguage: "korean",
  portfolioPassword: "1234"
});
