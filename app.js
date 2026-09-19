(() => {
  "use strict";

  const app = document.querySelector("#app");
  const config = window.SITE_CONFIG || {};
  const titleCache = new Map();
  const markdownCache = new Map();
  const hiddenSubjects = new Set(["consumer_data_utilization", "data_literacy"]);
  let contentKeys = [];
  let catalog = {};

  const escapeHtml = (value) => String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");

  function protectMathFromMarkdown(markdown) {
    // Marked consumes backslashes in MathJax delimiters, so restore TeX only after Markdown parsing.
    const segments = [];
    const tokenPrefix = "NMOFMATHTOKEN";
    const mathOrCode = /```[\s\S]*?```|`[^`\n]*`|\\\[[\s\S]*?\\\]|\\\([\s\S]*?\\\)|\$\$[\s\S]*?\$\$|\$(?!\$)(?:\\.|[^$\n])+\$/g;
    const source = markdown.replace(mathOrCode, (segment) => {
      if (segment.startsWith("`")) return segment;
      const token = `${tokenPrefix}${segments.length}END`;
      segments.push(segment);
      return token;
    });

    return {
      source,
      restore(html) {
        return segments.reduce(
          (result, segment, index) => result.replaceAll(`${tokenPrefix}${index}END`, escapeHtml(segment)),
          html
        );
      }
    };
  }

  function normalizeStrongBoundaries(markdown) {
    // CommonMark may leave **term(...)** raw when a Korean particle follows the closing marker.
    const codeOrStrongBeforeWord = /```[\s\S]*?```|`[^`\n]*`|\*\*([^*\n]+?)\*\*(?=[\p{L}\p{N}])/gu;
    return markdown.replace(codeOrStrongBeforeWord, (segment, strongText) => {
      if (segment.startsWith("`")) return segment;
      return `<strong>${strongText}</strong>`;
    });
  }

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
      const match = key.match(/^templates\/([^/]+)\/lectures_(english|korean)\/(?:([^/]+)\/)?([^/]+\.md)$/);
      if (!match) return result;
      const [, subject, language, part, filename] = match;
      if (hiddenSubjects.has(subject)) return result;
      result[subject] ||= { english: [], korean: [] };
      result[subject][language].push({ filename, key, part: part || "" });
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
      "00_start_here": "Start Here",
      "01_fashion_bigdata": "Fashion Data Analysis and AI",
      "02_python_basic": "Python Basic",
      "03_html_css_basic": "HTML·CSS Basic",
      "04_ai_basic": "AI Basic",
      "05_ai_math": "AI Math",
      "06_fashion_computing": "Fashion Computing",
    };
    if (labels[subject]) return labels[subject];
    return subject.replace(/^\d+_/, "").replaceAll(/[_-]/g, " ").replace(/\b\w/g, (letter) => letter.toUpperCase());
  }

  function partLabel(part) {
    const labels = {
      "01_introduction": "Introduction",
      "02_data": "Data",
      "03_analysis": "Analysis",
      "04_system": "System",
      "05_application": "Application",
      "06_ai": "Application",
    };
    return labels[part] || part.replace(/^\d+_/, "").replaceAll("_", " ");
  }

  function sectionsFromMarkdown(markdown) {
    const sections = [];
    let inFence = false;
    markdown.split("\n").forEach((line) => {
      if (line.trim().startsWith("```")) {
        inFence = !inFence;
        return;
      }
      const match = !inFence && line.match(/^##\s+(.+?)\s*#*\s*$/);
      if (match) sections.push(match[1].trim());
    });
    return sections;
  }

  function sectionListMarkup(subject, language, item) {
    const markdown = markdownCache.get(item.key);
    if (!markdown) return "";
    return sectionsFromMarkdown(markdown).map((title, index) => `
      <li><a class="toc-section" href="${lectureUrl(subject, language, item.filename, index)}" data-section="${index}">${escapeHtml(title)}</a></li>`).join("");
  }

  function scrollToSection(index) {
    const heading = document.querySelectorAll("#lecture-document .md-content h2")[index];
    heading?.scrollIntoView({ behavior: "smooth", block: "start" });
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
    if (markdownCache.has(key)) return markdownCache.get(key);
    const url = new URL(encodePath(key), location.href.split("#")[0]);
    url.searchParams.set("updated", Date.now().toString());
    const response = await fetch(url, { cache: "no-store" });
    if (!response.ok) throw new Error(`Unable to load ${key} (${response.status})`);
    const markdown = await response.text();
    markdownCache.set(key, markdown);
    return markdown;
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

  function bindSectionLinks(root) {
    root.querySelectorAll(".toc-chapter.current .toc-section").forEach((link) => {
      if (link.dataset.bound) return;
      link.dataset.bound = "true";
      link.addEventListener("click", (event) => {
        event.preventDefault();
        scrollToSection(Number(link.dataset.section));
        history.replaceState(null, "", link.getAttribute("href"));
      });
    });
  }

  function fillCurrentSections(subject, language, item) {
    const list = document.querySelector(".toc-chapter.current .toc-sections");
    if (!list || list.children.length) return;
    list.innerHTML = sectionListMarkup(subject, language, item);
    bindSectionLinks(list.closest(".toc-chapter"));
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

  function lectureUrl(subject, language, filename, section) {
    const params = new URLSearchParams({ subject, lang: language, doc: filename });
    if (section !== undefined) params.set("sec", String(section));
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
    const requestedSubject = currentRoute.params.get("subject") || config.defaultSubject || subjects[0];
    let subject = requestedSubject;
    const migratedSubjects = {
      data_literacy: "01_fashion_bigdata",
      consumer_data_utilization: "01_fashion_bigdata",
      fashion_bigdata_1: "01_fashion_bigdata",
      fashion_bigdata_2: "01_fashion_bigdata",
      fashion_bigdata: "01_fashion_bigdata",
      python_basic: "02_python_basic",
      html_css_basic: "03_html_css_basic",
      "ai-basic": "04_ai_basic",
      "ai-math": "05_ai_math",
      fashion_computing: "06_fashion_computing",
    };
    if (!catalog[subject]) subject = migratedSubjects[subject] || subjects[0];
    if (!(catalog[subject]?.[language] || []).length) {
      language = (catalog[subject]?.korean || []).length ? "korean" : "english";
    }
    const documents = catalog[subject][language] || [];
    let filename = currentRoute.params.get("doc") || documents[0]?.filename || "";
    const migratedBigdata2Files = {
      "01_ch1_데이터_프로젝트와_안전한_수집.md": "19_ch19_도구와_벤치마크_데이터셋.md",
      "02_ch2_상품_텍스트_마이닝.md": "23_ch23_상품명_키워드_분석.md",
      "03_ch3_판매량_급변과_이상치.md": "20_ch20_급상승_상품_분석.md",
      "04_ch4_RFM_고객_분석.md": "21_ch21_RFM_고객_분류.md",
      "05_ch5_이미지_유사도_검색.md": "22_ch22_이미지_유사도_추천.md",
      "06_ch6_검색의도와_SEO.md": "26_ch26_시장_데이터_융합_추천.md",
      "07_ch7_고객경험과_행동분석.md": "31_ch31_AB_테스트.md",
      "08_ch8_콘텐츠와_성과지표.md": "41_ch41_콘텐츠와_성과지표.md",
      "09_ch9_BCG_UGC_AIGC.md": "42_ch42_BCG_UGC_AIGC.md",
      "10_ch10_패션_이미지_생성과_검증.md": "43_ch43_패션_이미지_생성과_검증.md",
      "11_ch11_자동화와_의사결정.md": "44_ch44_자동화와_의사결정.md",
      "12_ch12_생성형_AI와_최종프로젝트.md": "45_ch45_생성형_AI와_최종프로젝트.md",
    };
    if (requestedSubject === "fashion_bigdata_2" && migratedBigdata2Files[filename]) {
      filename = migratedBigdata2Files[filename];
    }
    const shiftedFashionBigdataFiles = {
      "20_ch20_상품_텍스트_마이닝.md": "23_ch23_상품명_키워드_분석.md",
      "21_ch21_판매량_급변과_이상치.md": "20_ch20_급상승_상품_분석.md",
      "22_ch22_RFM_고객_분석.md": "21_ch21_RFM_고객_분류.md",
      "23_ch23_이미지_유사도_검색.md": "22_ch22_이미지_유사도_추천.md",
      "24_ch24_검색의도와_SEO.md": "26_ch26_시장_데이터_융합_추천.md",
      "25_ch25_고객경험과_행동분석.md": "31_ch31_AB_테스트.md",
      "26_ch26_콘텐츠와_성과지표.md": "41_ch41_콘텐츠와_성과지표.md",
      "27_ch27_BCG_UGC_AIGC.md": "42_ch42_BCG_UGC_AIGC.md",
      "28_ch28_패션_이미지_생성과_검증.md": "43_ch43_패션_이미지_생성과_검증.md",
      "29_ch29_자동화와_의사결정.md": "44_ch44_자동화와_의사결정.md",
      "30_ch30_생성형_AI와_최종프로젝트.md": "45_ch45_생성형_AI와_최종프로젝트.md",
      "07_ch7_질문과_분석_워크플로우.md": "07_ch7_분석_개괄.md",
      "07_ch7_질문과_분석_유형.md": "07_ch7_분석_개괄.md",
      "08_ch8_집단_비교.md": "10_ch10_특성화와_차별화.md",
      "08_ch8_현황_비교와_패턴_발견.md": "10_ch10_특성화와_차별화.md",
      "09_ch9_관계와_인과.md": "15_ch15_분석_평가.md",
      "09_ch9_예측과_불확실성.md": "12_ch12_분류와_회귀.md",
      "10_ch10_확률과_불확실성.md": "12_ch12_분류와_회귀.md",
      "10_ch10_관계_인과와_실험.md": "15_ch15_분석_평가.md",
      "11_ch11_데이터의_한계와_증거.md": "15_ch15_분석_평가.md",
      "11_ch11_편향_증거와_의사결정.md": "15_ch15_분석_평가.md",
      "12_ch12_데이터_분석_시스템과_보안.md": "16_ch16_데이터_저장과_이동.md",
      "12_ch12_로컬_서버_DB와_데이터_처리.md": "16_ch16_데이터_저장과_이동.md",
      "12_ch12_데이터_저장과_이동.md": "16_ch16_데이터_저장과_이동.md",
      "13_ch13_CPU_GPU_클라우드와_보안.md": "17_ch17_분석_시스템_도입과_비용_산정.md",
      "13_ch13_컴퓨터_자원과_처리_성능.md": "17_ch17_분석_시스템_도입과_비용_산정.md",
      "17_ch17_컴퓨터_자원과_처리_성능.md": "17_ch17_분석_시스템_도입과_비용_산정.md",
      "14_ch14_클라우드_비용과_보안.md": "18_ch18_분석_시스템_운영과_보안.md",
      "18_ch18_클라우드_비용과_보안.md": "18_ch18_분석_시스템_운영과_보안.md",
      "12_ch12_데이터_프로젝트와_안전한_수집.md": "19_ch19_도구와_벤치마크_데이터셋.md",
      "13_ch13_데이터_프로젝트와_안전한_수집.md": "19_ch19_도구와_벤치마크_데이터셋.md",
      "14_ch14_데이터_프로젝트와_안전한_수집.md": "19_ch19_도구와_벤치마크_데이터셋.md",
      "15_ch15_데이터_프로젝트와_안전한_수집.md": "19_ch19_도구와_벤치마크_데이터셋.md",
      "19_ch19_데이터_프로젝트와_안전한_수집.md": "19_ch19_도구와_벤치마크_데이터셋.md",
      "13_ch13_상품_텍스트_마이닝.md": "23_ch23_상품명_키워드_분석.md",
      "14_ch14_상품_텍스트_마이닝.md": "23_ch23_상품명_키워드_분석.md",
      "15_ch15_상품_텍스트_마이닝.md": "23_ch23_상품명_키워드_분석.md",
      "16_ch16_상품_텍스트_마이닝.md": "23_ch23_상품명_키워드_분석.md",
      "14_ch14_판매량_급변과_이상치.md": "20_ch20_급상승_상품_분석.md",
      "15_ch15_판매량_급변과_이상치.md": "20_ch20_급상승_상품_분석.md",
      "16_ch16_판매량_급변과_이상치.md": "20_ch20_급상승_상품_분석.md",
      "17_ch17_판매량_급변과_이상치.md": "20_ch20_급상승_상품_분석.md",
      "15_ch15_RFM_고객_분석.md": "21_ch21_RFM_고객_분류.md",
      "16_ch16_RFM_고객_분석.md": "21_ch21_RFM_고객_분류.md",
      "17_ch17_RFM_고객_분석.md": "21_ch21_RFM_고객_분류.md",
      "18_ch18_RFM_고객_분석.md": "21_ch21_RFM_고객_분류.md",
      "16_ch16_이미지_유사도_검색.md": "22_ch22_이미지_유사도_추천.md",
      "17_ch17_이미지_유사도_검색.md": "22_ch22_이미지_유사도_추천.md",
      "18_ch18_이미지_유사도_검색.md": "22_ch22_이미지_유사도_추천.md",
      "19_ch19_이미지_유사도_검색.md": "22_ch22_이미지_유사도_추천.md",
      "17_ch17_검색의도와_SEO.md": "26_ch26_시장_데이터_융합_추천.md",
      "18_ch18_검색의도와_SEO.md": "26_ch26_시장_데이터_융합_추천.md",
      "19_ch19_검색의도와_SEO.md": "26_ch26_시장_데이터_융합_추천.md",
      "20_ch20_검색의도와_SEO.md": "26_ch26_시장_데이터_융합_추천.md",
      "18_ch18_고객경험과_행동분석.md": "31_ch31_AB_테스트.md",
      "19_ch19_고객경험과_행동분석.md": "31_ch31_AB_테스트.md",
      "20_ch20_고객경험과_행동분석.md": "31_ch31_AB_테스트.md",
      "21_ch21_고객경험과_행동분석.md": "31_ch31_AB_테스트.md",
      "19_ch19_콘텐츠와_성과지표.md": "41_ch41_콘텐츠와_성과지표.md",
      "20_ch20_콘텐츠와_성과지표.md": "41_ch41_콘텐츠와_성과지표.md",
      "21_ch21_콘텐츠와_성과지표.md": "41_ch41_콘텐츠와_성과지표.md",
      "22_ch22_콘텐츠와_성과지표.md": "41_ch41_콘텐츠와_성과지표.md",
      "20_ch20_BCG_UGC_AIGC.md": "42_ch42_BCG_UGC_AIGC.md",
      "21_ch21_BCG_UGC_AIGC.md": "42_ch42_BCG_UGC_AIGC.md",
      "22_ch22_BCG_UGC_AIGC.md": "42_ch42_BCG_UGC_AIGC.md",
      "23_ch23_BCG_UGC_AIGC.md": "42_ch42_BCG_UGC_AIGC.md",
      "21_ch21_패션_이미지_생성과_검증.md": "43_ch43_패션_이미지_생성과_검증.md",
      "22_ch22_패션_이미지_생성과_검증.md": "43_ch43_패션_이미지_생성과_검증.md",
      "23_ch23_패션_이미지_생성과_검증.md": "43_ch43_패션_이미지_생성과_검증.md",
      "24_ch24_패션_이미지_생성과_검증.md": "43_ch43_패션_이미지_생성과_검증.md",
      "22_ch22_자동화와_의사결정.md": "44_ch44_자동화와_의사결정.md",
      "23_ch23_자동화와_의사결정.md": "44_ch44_자동화와_의사결정.md",
      "24_ch24_자동화와_의사결정.md": "44_ch44_자동화와_의사결정.md",
      "25_ch25_자동화와_의사결정.md": "44_ch44_자동화와_의사결정.md",
      "23_ch23_생성형_AI와_최종프로젝트.md": "45_ch45_생성형_AI와_최종프로젝트.md",
      "24_ch24_생성형_AI와_최종프로젝트.md": "45_ch45_생성형_AI와_최종프로젝트.md",
      "25_ch25_생성형_AI와_최종프로젝트.md": "45_ch45_생성형_AI와_최종프로젝트.md",
      "26_ch26_생성형_AI와_최종프로젝트.md": "45_ch45_생성형_AI와_최종프로젝트.md",
    };
    if (subject === "01_fashion_bigdata" && shiftedFashionBigdataFiles[filename]) {
      filename = shiftedFashionBigdataFiles[filename];
    }
    if (!documents.some((item) => item.filename === filename)) filename = documents[0]?.filename || "";

    const subjectMarkup = subjects.map((subjectName) => {
      const subjectDocuments = catalog[subjectName][language] || [];
      let lastPart = "";
      const chapters = subjectDocuments.map((item) => {
        const isCurrent = subjectName === subject && item.filename === filename;
        const partHeading = item.part && item.part !== lastPart
          ? `<p class="toc-part">${escapeHtml(partLabel(item.part))}</p>`
          : "";
        if (item.part) lastPart = item.part;
        return `${partHeading}
          <div class="toc-chapter ${isCurrent ? "current" : ""}">
            <a class="document-link ${isCurrent ? "active" : ""}"
               href="${lectureUrl(subjectName, language, item.filename)}" data-key="${escapeHtml(item.key)}">
              <span class="chapter-number">${chapterNumber(item.filename)}</span>
              <span class="document-title">${escapeHtml(titleCache.get(item.key) || documentLabel(item.filename))}</span>
            </a>
            <button class="toc-toggle" type="button" aria-expanded="${isCurrent}" aria-label="절 목록 펼치기"
                    data-subject="${escapeHtml(subjectName)}" data-filename="${escapeHtml(item.filename)}"></button>
            <ul class="toc-sections" ${isCurrent ? "" : "hidden"}>${isCurrent ? sectionListMarkup(subjectName, language, item) : ""}</ul>
          </div>`;
      }).join("");
      const body = subjectDocuments.length
        ? chapters
        : `<p class="document-link">${language === "korean" ? "이 폴더에 마크다운 파일을 추가하세요." : "Add Markdown files to this folder."}</p>`;
      return `
        <section class="toc-course">
          <p class="toc-caption">${escapeHtml(subjectLabel(subjectName))}</p>
          ${body}
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

    app.querySelectorAll(".toc-toggle").forEach((button) => {
      button.addEventListener("click", async () => {
        const expanded = button.getAttribute("aria-expanded") === "true";
        const list = button.nextElementSibling;
        button.setAttribute("aria-expanded", String(!expanded));
        list.hidden = expanded;
        if (expanded || list.children.length) return;
        const item = catalog[button.dataset.subject][language].find((entry) => entry.filename === button.dataset.filename);
        try {
          await fetchMarkdown(item.key);
          list.innerHTML = sectionListMarkup(button.dataset.subject, language, item);
          bindSectionLinks(list);
        } catch {
          list.innerHTML = "";
        }
      });
    });
    bindSectionLinks(app);
    app.querySelectorAll("[data-language]").forEach((button) => {
      button.addEventListener("click", () => {
        const nextLanguage = button.dataset.language;
        const nextDocs = catalog[subject][nextLanguage] || [];
        navigate(lectureUrl(subject, nextLanguage, nextDocs[0]?.filename || "").slice(1));
      });
    });
    hydrateTitles(subject, language).then(() => {
      subjects.filter((name) => name !== subject).forEach((name) => hydrateTitles(name, language));
    });
    loadDocument(subject, language, filename);
  }

  function hydrateAnalysisChartSwitchers(root) {
    root.querySelectorAll(".analysis-example-figure").forEach((figure, index) => {
      const nodesBeforeCode = [];
      let candidate = figure.nextElementSibling;
      let codeBlock = null;

      while (candidate && !/^H[12]$/.test(candidate.tagName)) {
        if (candidate.matches("pre") && candidate.querySelector("code.language-python")) {
          codeBlock = candidate;
          break;
        }
        nodesBeforeCode.push(candidate);
        candidate = candidate.nextElementSibling;
      }
      if (!codeBlock) return;

      const switcher = document.createElement("section");
      switcher.className = "analysis-chart-switcher";

      const tabs = document.createElement("div");
      tabs.className = "analysis-chart-tabs";
      tabs.setAttribute("role", "tablist");
      tabs.setAttribute("aria-label", `그림 ${index + 1} 보기 방식`);

      const graphTab = document.createElement("button");
      graphTab.type = "button";
      graphTab.className = "analysis-chart-tab";
      graphTab.textContent = "그래프";

      const codeTab = document.createElement("button");
      codeTab.type = "button";
      codeTab.className = "analysis-chart-tab";
      codeTab.textContent = "Python 코드";

      const graphPanel = document.createElement("div");
      const codePanel = document.createElement("div");
      const graphId = `analysis-chart-${index + 1}-graph`;
      const codeId = `analysis-chart-${index + 1}-code`;

      graphPanel.id = graphId;
      graphPanel.className = "analysis-chart-panel";
      graphPanel.setAttribute("role", "tabpanel");
      codePanel.id = codeId;
      codePanel.className = "analysis-chart-panel analysis-chart-code";
      codePanel.setAttribute("role", "tabpanel");

      graphTab.id = `${graphId}-tab`;
      graphTab.setAttribute("role", "tab");
      graphTab.setAttribute("aria-controls", graphId);
      codeTab.id = `${codeId}-tab`;
      codeTab.setAttribute("role", "tab");
      codeTab.setAttribute("aria-controls", codeId);
      graphPanel.setAttribute("aria-labelledby", graphTab.id);
      codePanel.setAttribute("aria-labelledby", codeTab.id);

      const activate = (showCode) => {
        graphTab.setAttribute("aria-selected", String(!showCode));
        codeTab.setAttribute("aria-selected", String(showCode));
        graphPanel.hidden = showCode;
        codePanel.hidden = !showCode;
      };

      graphTab.addEventListener("click", () => activate(false));
      codeTab.addEventListener("click", () => activate(true));
      tabs.append(graphTab, codeTab);
      figure.parentNode.insertBefore(switcher, figure);
      graphPanel.appendChild(figure);
      nodesBeforeCode.forEach((node) => codePanel.appendChild(node));
      codePanel.appendChild(codeBlock);
      switcher.append(tabs, graphPanel, codePanel);
      activate(false);
    });
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
        const protectedMath = protectMathFromMarkdown(markdown);
        const markdownSource = normalizeStrongBoundaries(protectedMath.source);
        const parsedMarkdown = protectedMath.restore(window.marked.parse(markdownSource));
        html = window.DOMPurify.sanitize(parsedMarkdown, {
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
        const raw = link.getAttribute("href") || "";
        const lecture = raw.match(/^templates\/([^/]+)\/lectures_(english|korean)\/(?:[^/]+\/)?([^/#?]+\.md)(?:#sec-(\d+))?$/);
        if (lecture) {
          const target = decodeURIComponent(lecture[3]);
          const known = (catalog[lecture[1]]?.[lecture[2]] || []).some((doc) => doc.filename === target);
          if (known) {
            link.setAttribute("href", lectureUrl(lecture[1], lecture[2], target, lecture[4] === undefined ? undefined : Number(lecture[4])));
            return;
          }
        }
        if (/^https?:/i.test(link.href)) {
          link.target = "_blank";
          link.rel = "noopener noreferrer";
        }
      });
      hydrateAnalysisChartSwitchers(container);
      hydrateYouTubeEmbeds(container);
      hydrateAnimatedLectureImages(container);
      fillCurrentSections(subject, language, item);
      const section = route().params.get("sec");
      if (section !== null) scrollToSection(Number(section));
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
