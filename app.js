(() => {
  "use strict";

  const app = document.querySelector("#app");
  const config = window.SITE_CONFIG || {};
  const titleCache = new Map();
  const hiddenSubjects = new Set(["consumer_data_utilization", "data_literacy"]);
  let contentKeys = [];
  let catalog = {};

  const escapeHtml = (value) => String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");

  const encodePath = (path) => path.split("/").map(encodeURIComponent).join("/");

  function route() {
    const raw = location.hash.replace(/^#/, "") || "/contact";
    const [pathname, query = ""] = raw.split("?");
    return { pathname, params: new URLSearchParams(query) };
  }

  function navigate(path) {
    if (location.hash === `#${path}`) render();
    else location.hash = path;
  }

  function setActiveNav(section) {
    document.querySelectorAll("[data-route]").forEach((link) => {
      const active = link.dataset.route === section;
      link.classList.toggle("active", active);
      if (active) link.setAttribute("aria-current", "page");
      else link.removeAttribute("aria-current");
    });
    document.querySelector("#primary-nav").classList.remove("open");
    document.querySelector(".menu-button").setAttribute("aria-expanded", "false");
  }

  function inferBucketUrl() {
    const host = location.hostname;
    if (["localhost", "127.0.0.1", "::1"].includes(host)) return "";
    if (config.s3BucketUrl) return config.s3BucketUrl.replace(/\/+$/, "");
    let match = host.match(/^(.+)\.s3-website[.-]([a-z0-9-]+)\.amazonaws\.com$/i);
    if (match) return `https://${match[1]}.s3.${match[2]}.amazonaws.com`;
    match = host.match(/^(.+)\.s3\.([a-z0-9-]+)\.amazonaws\.com$/i);
    if (match) return `https://${match[1]}.s3.${match[2]}.amazonaws.com`;
    match = host.match(/^(.+)\.s3\.amazonaws\.com$/i);
    return match ? `https://${match[1]}.s3.amazonaws.com` : "";
  }

  async function listS3Markdown() {
    const bucketUrl = inferBucketUrl();
    if (!bucketUrl) return [];
    const keys = [];
    let token = "";
    do {
      const url = new URL(bucketUrl);
      url.searchParams.set("list-type", "2");
      url.searchParams.set("prefix", config.contentPrefix || "templates/");
      url.searchParams.set("max-keys", "1000");
      if (token) url.searchParams.set("continuation-token", token);
      const response = await fetch(url, { cache: "no-store" });
      if (!response.ok) throw new Error(`S3 listing returned ${response.status}`);
      const documentXml = new DOMParser().parseFromString(await response.text(), "application/xml");
      Array.from(documentXml.getElementsByTagName("Key")).forEach((node) => {
        if (node.textContent.endsWith(".md")) keys.push(node.textContent);
      });
      token = documentXml.getElementsByTagName("NextContinuationToken")[0]?.textContent || "";
    } while (token);
    return keys;
  }

  function buildCatalog(keys) {
    return keys.reduce((result, key) => {
      const match = key.match(/^templates\/([^/]+)\/lectures_(english|korean)\/([^/]+\.md)$/);
      if (!match) return result;
      const [, subject, language, filename] = match;
      if (hiddenSubjects.has(subject)) return result;
      result[subject] ||= { english: [], korean: [] };
      result[subject][language].push({ filename, key });
      return result;
    }, {});
  }

  async function loadCatalog() {
    try {
      contentKeys = await listS3Markdown();
    } catch (error) {
      console.info("Live S3 listing is unavailable; using the bundled content index.", error);
    }
    if (!contentKeys.length) {
      contentKeys = Array.isArray(window.CONTENT_INDEX) ? [...window.CONTENT_INDEX] : [];
    }
    contentKeys.sort((a, b) => a.localeCompare(b, undefined, { numeric: true }));
    catalog = buildCatalog(contentKeys);
  }

  function subjectLabel(subject) {
    const labels = {
      fashion_bigdata_1: "패션 빅데이터 1",
      fashion_bigdata_2: "패션 빅데이터 2",
    };
    if (labels[subject]) return labels[subject];
    return subject.replaceAll(/[_-]/g, " ").replace(/\b\w/g, (letter) => letter.toUpperCase());
  }

  function documentLabel(filename) {
    return filename
      .replace(/\.md$/i, "")
      .replace(/^\d+_(?:ch\d+|flask\d+)_/i, "")
      .replaceAll("_", " ");
  }

  function chapterNumber(filename) {
    const match = filename.match(/^(\d+)/);
    return match ? String(Number(match[1])).padStart(2, "0") : "•";
  }

  async function fetchMarkdown(key) {
    const url = new URL(encodePath(key), location.href.split("#")[0]);
    url.searchParams.set("updated", Date.now().toString());
    const response = await fetch(url, { cache: "no-store" });
    if (!response.ok) throw new Error(`Unable to load ${key} (${response.status})`);
    return response.text();
  }

  function titleFromMarkdown(markdown, fallback) {
    const heading = markdown.match(/^\s*#{1,6}\s+(.+?)\s*#*\s*$/m)?.[1];
    return (heading || fallback)
      .replace(/^Chapter\s+\d+:\s*/i, "")
      .replace(/^Flask\s+\d+:\s*Building a Revenue-Generating Lecture Website\s*[—-]\s*/i, "")
      .trim();
  }

  function hydrateYouTubeEmbeds(container) {
    container.querySelectorAll(".video-embed[data-youtube-id]").forEach((placeholder) => {
      const videoId = placeholder.dataset.youtubeId || "";
      if (!/^[A-Za-z0-9_-]{11}$/.test(videoId)) return;
      const title = placeholder.dataset.title || "YouTube video";
      const iframe = document.createElement("iframe");
      iframe.src = `https://www.youtube-nocookie.com/embed/${videoId}`;
      iframe.title = title;
      iframe.loading = "lazy";
      iframe.referrerPolicy = "strict-origin-when-cross-origin";
      iframe.allow = "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share";
      iframe.allowFullscreen = true;
      placeholder.append(iframe);
    });
  }

  function hydrateAnimatedLectureImages(container) {
    container.animatedImageObserver?.disconnect();
    const images = container.querySelectorAll('img[src*="video-shape-time-axis.gif"]');
    if (!images.length || !("IntersectionObserver" in window)) return;

    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        const image = entry.target;
        if (!entry.isIntersecting) {
          image.dataset.animationVisible = "false";
          return;
        }
        if (image.dataset.animationVisible === "true") return;

        image.dataset.animationVisible = "true";
        const source = image.dataset.animationSource || image.getAttribute("src");
        if (!source) return;
        image.dataset.animationSource = source;

        const replayUrl = new URL(source, document.baseURI);
        replayUrl.searchParams.set("play", Date.now().toString());
        image.src = replayUrl.href;
      });
    }, { threshold: 0.2 });

    container.animatedImageObserver = observer;
    images.forEach((image) => observer.observe(image));
  }

  async function hydrateTitles(subject, language) {
    const items = catalog[subject]?.[language] || [];
    await Promise.all(items.map(async (item) => {
      if (!titleCache.has(item.key)) {
        try {
          titleCache.set(item.key, titleFromMarkdown(await fetchMarkdown(item.key), documentLabel(item.filename)));
        } catch {
          titleCache.set(item.key, documentLabel(item.filename));
        }
      }
      const link = document.querySelector(`[data-key="${CSS.escape(item.key)}"] .document-title`);
      if (link) link.textContent = titleCache.get(item.key);
    }));
  }

  function renderContact() {
    setActiveNav("contact");
    app.innerHTML = `
      <section class="contact-main">
        <div class="character-wrap" aria-label="Site character">
          <div class="character-face">
            <div class="mainline" aria-hidden="true"></div>
            <img src="static/image/main.png" alt="">
          </div>
        </div>
        <div class="contact-email"><h2>on the construction</h2></div>
      </section>`;
    animateMouth();
  }

  function lectureUrl(subject, language, filename) {
    const params = new URLSearchParams({ subject, lang: language, doc: filename });
    return `#/lecture?${params}`;
  }

  function renderLecture() {
    setActiveNav("lecture");
    const currentRoute = route();
    const subjects = Object.keys(catalog).sort();
    if (!subjects.length) {
      app.innerHTML = `<div class="document-state"><h2>No lecture folders found</h2><p>Add Markdown files under <code>templates/&lt;subject&gt;/lectures_english/</code> or <code>lectures_korean/</code>.</p></div>`;
      return;
    }
    let language = currentRoute.params.get("lang") || config.defaultLanguage || "english";
    if (!["english", "korean"].includes(language)) language = "english";
    let subject = currentRoute.params.get("subject") || config.defaultSubject || subjects[0];
    const migratedSubjects = {
      data_literacy: "fashion_bigdata_1",
      consumer_data_utilization: "fashion_bigdata_2",
    };
    if (!catalog[subject]) subject = migratedSubjects[subject] || subjects[0];
    if (!(catalog[subject]?.[language] || []).length) {
      language = (catalog[subject]?.korean || []).length ? "korean" : "english";
    }
    const documents = catalog[subject][language] || [];
    let filename = currentRoute.params.get("doc") || documents[0]?.filename || "";
    if (!documents.some((item) => item.filename === filename)) filename = documents[0]?.filename || "";

    const subjectMarkup = subjects.map((subjectName) => {
      const open = subjectName === subject;
      const subjectDocuments = catalog[subjectName][language] || [];
      const links = subjectDocuments.length
        ? subjectDocuments.map((item) => `
            <a class="document-link ${open && item.filename === filename ? "active" : ""}"
               href="${lectureUrl(subjectName, language, item.filename)}" data-key="${escapeHtml(item.key)}">
              <span class="chapter-number">${chapterNumber(item.filename)}</span>
              <span class="document-title">${escapeHtml(titleCache.get(item.key) || documentLabel(item.filename))}</span>
            </a>`).join("")
        : `<p class="document-link">${language === "korean" ? "이 폴더에 마크다운 파일을 추가하세요." : "Add Markdown files to this folder."}</p>`;
      return `
        <section class="subject">
          <button class="subject-toggle" type="button" aria-expanded="${open}" data-subject="${escapeHtml(subjectName)}">
            ${escapeHtml(subjectLabel(subjectName))}
          </button>
          <div class="document-list" ${open ? "" : "hidden"}>${links}</div>
        </section>`;
    }).join("");

    app.innerHTML = `
      <div class="lecture-layout">
        <aside class="lecture-sidebar">
          <div class="sidebar-top">
            <h1>Library</h1>
            <div class="lang-switch" aria-label="Lecture language">
              <button type="button" data-language="english" class="${language === "english" ? "active" : ""}">EN</button>
              <button type="button" data-language="korean" class="${language === "korean" ? "active" : ""}">한국어</button>
            </div>
          </div>
          <nav aria-label="Lecture subjects">${subjectMarkup}</nav>
        </aside>
        <main class="lecture-main" id="lecture-document" tabindex="-1">
          <div class="document-meta">${escapeHtml(subjectLabel(subject))} · ${language}</div>
          <div class="document-state" role="status"><span class="loading-dot"></span><p>Loading document…</p></div>
        </main>
        <aside class="right-rail">
          <section class="rail-card">
            <span class="rail-label">Support</span>
            <h2>Keep this library alive.</h2>
            <p>Your support makes room for more open lessons and practical notes.</p>
            <a href="mailto:janyty@proton.me">on the construction ↗</a>
          </section>
          <section class="rail-card">
            <span class="rail-label">Advertisement</span>
            <div class="ad-slot">Google AdSense<br>or Coupang Partners</div>
          </section>
        </aside>
      </div>`;

    app.querySelectorAll(".subject-toggle").forEach((button) => {
      button.addEventListener("click", () => {
        const expanded = button.getAttribute("aria-expanded") === "true";
        button.setAttribute("aria-expanded", String(!expanded));
        button.nextElementSibling.hidden = expanded;
        if (!expanded) hydrateTitles(button.dataset.subject, language);
      });
    });
    app.querySelectorAll("[data-language]").forEach((button) => {
      button.addEventListener("click", () => {
        const nextLanguage = button.dataset.language;
        const nextDocs = catalog[subject][nextLanguage] || [];
        navigate(lectureUrl(subject, nextLanguage, nextDocs[0]?.filename || "").slice(1));
      });
    });
    hydrateTitles(subject, language);
    loadDocument(subject, language, filename);
  }

  async function loadDocument(subject, language, filename) {
    const container = document.querySelector("#lecture-document");
    if (!container) return;
    if (!filename) {
      container.innerHTML = `<div class="document-state"><h2>No ${escapeHtml(language)} lectures yet</h2><p>Add a Markdown file to this language directory and refresh.</p></div>`;
      return;
    }
    const item = catalog[subject][language].find((entry) => entry.filename === filename);
    try {
      const markdown = await fetchMarkdown(item.key);
      if (!container.isConnected) return;
      titleCache.set(item.key, titleFromMarkdown(markdown, documentLabel(filename)));
      let html;
      if (window.marked && window.DOMPurify) {
        window.marked.setOptions({ gfm: true, breaks: true });
        html = window.DOMPurify.sanitize(window.marked.parse(markdown), {
          USE_PROFILES: { html: true },
          ADD_ATTR: ["target", "rel", "data-youtube-id", "data-title"]
        });
      } else {
        html = `<pre>${escapeHtml(markdown)}</pre>`;
      }
      container.innerHTML = `
        <div class="document-meta">${escapeHtml(subjectLabel(subject))} · ${escapeHtml(language)}</div>
        <article class="md-content">${html}</article>`;
      container.querySelectorAll("a[href]").forEach((link) => {
        if (/^https?:/i.test(link.href)) {
          link.target = "_blank";
          link.rel = "noopener noreferrer";
        }
      });
      hydrateYouTubeEmbeds(container);
      hydrateAnimatedLectureImages(container);
      window.MathJax?.typesetPromise?.([container]).catch(() => {});
    } catch (error) {
      container.innerHTML = `<div class="document-state"><h2>Document unavailable</h2><p>${escapeHtml(error.message)}</p></div>`;
    }
  }

  function portfolioAuthenticated() {
    return sessionStorage.getItem("portfolio-authenticated") === "true";
  }

  function renderPortfolioLogin() {
    setActiveNav("portfolio");
    if (portfolioAuthenticated()) {
      navigate("/portfolio/about");
      return;
    }
    app.innerHTML = `
      <section class="portfolio-shell">
        <form class="login-card">
          <label class="sr-only" for="portfolio-password">Password</label>
          <div class="password-row">
            <input id="portfolio-password" name="password" type="password" autocomplete="current-password" placeholder="Password" required>
            <button class="button" type="submit">login</button>
          </div>
          <p class="form-error" role="alert"></p>
        </form>
      </section>`;
    const form = app.querySelector("form");
    form.addEventListener("submit", (event) => {
      event.preventDefault();
      if (form.elements.password.value === String(config.portfolioPassword ?? "1234")) {
        sessionStorage.setItem("portfolio-authenticated", "true");
        navigate("/portfolio/about");
      } else {
        form.querySelector(".form-error").textContent = "The password is not correct.";
        form.elements.password.select();
      }
    });
  }

  function portfolioNavigation(active) {
    return `
      <aside class="portfolio-sidebar">
        <h2>Portfolio</h2>
        <nav aria-label="Portfolio">
          <a href="#/portfolio/about" class="${active === "about" ? "active" : ""}">I am</a>
          <a href="#/portfolio/resume" class="${active === "resume" ? "active" : ""}">Resume</a>
        </nav>
        <button class="logout-button" type="button">Log out</button>
      </aside>`;
  }

  function renderPortfolio(page) {
    if (!portfolioAuthenticated()) {
      navigate("/portfolio/login");
      return;
    }
    setActiveNav("portfolio");
    const content = page === "resume"
      ? `<div class="resume-header"><img src="static/image/me.jpg" alt="Hyungjin Son"><div><h3>HYUNGJIN SON</h3><p>data analyst</p></div></div>`
      : `<p>요약 그림 넣기</p>`;
    app.innerHTML = `<div class="portfolio-layout">${portfolioNavigation(page)}<main class="portfolio-content">${content}</main></div>`;
    app.querySelector(".logout-button").addEventListener("click", () => {
      sessionStorage.removeItem("portfolio-authenticated");
      navigate("/portfolio/login");
    });
  }

  function animateMouth() {
    const mouth = document.querySelector(".mainline");
    if (!mouth || matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    const wait = (duration) => new Promise((resolve) => setTimeout(resolve, duration));
    (async () => {
      while (mouth.isConnected) {
        const direction = crypto.getRandomValues(new Uint8Array(1))[0] % 2 ? 1 : -1;
        await mouth.animate(
          [{ transform: "rotate(0deg)" }, { transform: `rotate(${direction * 360}deg)` }],
          { duration: 900 + Math.random() * 400, easing: "cubic-bezier(.45,0,.2,1)" }
        ).finished;
        await wait(900 + Math.random() * 1000);
      }
    })();
  }

  function render() {
    const { pathname } = route();
    if (pathname === "/" || pathname === "/contact") renderContact();
    else if (pathname === "/lecture" || pathname.startsWith("/lecture/")) renderLecture();
    else if (pathname === "/portfolio/login") renderPortfolioLogin();
    else if (pathname === "/portfolio/resume") renderPortfolio("resume");
    else if (pathname.startsWith("/portfolio")) renderPortfolio("about");
    else navigate("/contact");
  }

  document.querySelector(".menu-button").addEventListener("click", (event) => {
    const expanded = event.currentTarget.getAttribute("aria-expanded") === "true";
    event.currentTarget.setAttribute("aria-expanded", String(!expanded));
    document.querySelector("#primary-nav").classList.toggle("open", !expanded);
  });
  window.addEventListener("hashchange", render);

  loadCatalog().then(render);
})();
