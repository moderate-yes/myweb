# Flask 4: Building a Revenue-Generating Lecture Website — The Sponsorship and Ad Area

Now that content is ready, it's time to design the revenue area. The key principle is to make sure ads never appear before the body content or interrupt the learning flow.

In this post, we split the right sidebar into two parts: **direct sponsorship information** and an **ad slot**.

## The Revenue Sidebar Structure

```html
<aside class="revenue-sidebar">
  <section class="support-card" aria-labelledby="support-title">
    <span class="card-label">support</span>
    <h2 id="support-title">후원 안내</h2>
    <p>후원은 이 사이트를 살아 숨 쉬게 하는 힘이 됩니다.</p>
    <a href="mailto:hello@example.com">
      후원 문의<br>
      <strong>hello@example.com</strong>
    </a>
  </section>

  <section class="ad-card" aria-label="광고 영역">
    <span class="card-label">advertisement</span>
    <div class="ad-slot">
      Google AdSense 또는 쿠팡 파트너스
    </div>
  </section>
</aside>
```

Using a `mailto:` link lets visitors reach out directly without having to copy the email address. When exposing a personal email on a public site, also consider the possibility of spam.

## Designing the Two Cards

```css
.revenue-sidebar {
  width: 265px;
  padding: 1.5rem 1rem;
}

.support-card,
.ad-card {
  padding: 1.1rem;
  border: 1px solid #e6e6e6;
  border-radius: 8px;
  background: #fff;
}

.support-card {
  margin-bottom: 1rem;
}

.card-label {
  display: block;
  margin-bottom: 0.75rem;
  color: #aaa;
  font-size: 0.65rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}

.ad-slot {
  display: grid;
  min-height: 220px;
  place-items: center;
  border: 1px dashed #ddd;
  color: #999;
  text-align: center;
}
```

Before you receive the actual code from an ad platform, use an empty slot where you can only verify the size. There's no need to create a fake banner that looks like an ad you haven't been issued yet.

## Prioritize Body Content on Mobile

Keeping three columns when the screen is narrow makes the body content hard to read. On mobile, it's better to move the sidebar below the body content or hide the ad area.

```css
@media (max-width: 992px) {
  .lecture-layout {
    display: block;
  }

  .revenue-sidebar {
    display: none;
  }
}
```

## Principles for Using Affiliate Links

When using an affiliate program such as Coupang Partners, follow these guidelines.

- Only introduce products that are actually relevant to the lecture content.
- Disclose that clicking the link or making a purchase may generate revenue for the site operator.
- Don't hide it to look unlike an ad, or induce excessive clicking.
- Verify the latest information before writing product prices and benefits as if they were fixed facts.
- Check each platform's latest policies and disclosure requirements.

## Preparation Before Adding Google Ads

Simply pasting in ad code first doesn't immediately make a site a good revenue-generating site. Before applying, check the following.

- Is the site's purpose and target audience clear?
- Is there enough content you've written yourself?
- Do the menu and page navigation work properly?
- Do you have necessary notice pages, such as a privacy policy?
- Can content be read comfortably on mobile?

Platform policies can change, so re-check the official documentation at the time you actually apply.

## Exercises for This Post

1. Create the sponsorship card and the ad card, each.
2. Change the sponsorship inquiry email link to your own address.
3. Test the size of the empty slot before inserting the ad code.
4. Check that the body content appears first at mobile size.
5. Draft wording that discloses the ad/affiliate facts.

In the next post, we'll cover the environment variables, session security, testing, and deployment preparation needed before going public.
