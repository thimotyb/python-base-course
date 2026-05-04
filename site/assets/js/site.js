(() => {
  const KEY_THEME = "course_theme";
  const KEY_LANG = "course_lang";
  const THEMES = new Set(["light", "dark"]);

  const getTheme = () => {
    const saved = localStorage.getItem(KEY_THEME);
    return THEMES.has(saved || "") ? saved : "light";
  };

  const applyTheme = (theme) => {
    const safeTheme = THEMES.has(theme) ? theme : "light";
    document.body.setAttribute("data-theme", safeTheme);
    localStorage.setItem(KEY_THEME, safeTheme);
    const themeSelect = document.getElementById("theme-select");
    if (themeSelect) themeSelect.value = safeTheme;
  };

  const setGoogTransCookie = (lang) => {
    const value = lang === "en" ? "/it/en" : "/it/it";
    document.cookie = `googtrans=${value};path=/`;
    localStorage.setItem(KEY_LANG, lang);
  };

  const getCurrentLang = () => {
    const saved = localStorage.getItem(KEY_LANG);
    if (saved === "it" || saved === "en") return saved;
    return "it";
  };

  const applyLanguage = (lang) => {
    setGoogTransCookie(lang);
    const gtSelect = document.querySelector(".goog-te-combo");
    if (gtSelect) {
      gtSelect.value = lang === "en" ? "en" : "it";
      gtSelect.dispatchEvent(new Event("change"));
      if (lang === "it") window.setTimeout(() => location.reload(), 100);
    } else {
      location.reload();
    }
  };

  window.googleTranslateElementInit = () => {
    if (!window.google || !window.google.translate) return;
    new window.google.translate.TranslateElement(
      { pageLanguage: "it", includedLanguages: "it,en", autoDisplay: false },
      "google_translate_element"
    );
    const select = document.getElementById("lang-select");
    const initialLang = getCurrentLang();
    if (select) select.value = initialLang;
  };

  const setupCommonUI = () => {
    const headerShell = document.querySelector(".site-header .shell");
    if (headerShell && !headerShell.querySelector(".header-top")) {
      const headerTop = document.createElement("div");
      headerTop.className = "header-top";
      headerTop.innerHTML = `
        <p class="site-mark">Python Base</p>
        <label class="lang-switch" for="lang-select">
          <span>Lingua</span>
          <select id="lang-select" aria-label="Choose language">
            <option value="it">Italiano</option>
            <option value="en">English</option>
          </select>
        </label>
        <label class="theme-switch" for="theme-select">
          <span>Tema</span>
          <select id="theme-select" aria-label="Choose theme">
            <option value="light">Chiaro</option>
            <option value="dark">Scuro</option>
          </select>
        </label>
        <button class="print-btn print-btn-top" type="button" data-print aria-label="Stampa questo modulo">Stampa</button>
      `;
      headerShell.insertBefore(headerTop, headerShell.firstChild);
    }

    if (!document.querySelector(".print-fixed")) {
      const btn = document.createElement("button");
      btn.className = "print-btn print-fixed";
      btn.type = "button";
      btn.setAttribute("data-print", "");
      btn.setAttribute("aria-label", "Stampa questo modulo");
      btn.textContent = "Stampa";
      document.body.appendChild(btn);
    }

    if (!document.querySelector(".top-link")) {
      const link = document.createElement("a");
      link.className = "top-link";
      link.href = "#top";
      link.setAttribute("aria-label", "Torna in alto");
      link.textContent = "Su";
      document.body.appendChild(link);
    }

    // Event Listeners for Theme and Language
    const themeSelect = document.getElementById("theme-select");
    if (themeSelect) {
      themeSelect.value = getTheme();
      themeSelect.addEventListener("change", () => applyTheme(themeSelect.value));
    }
    const langSelect = document.getElementById("lang-select");
    if (langSelect) {
      langSelect.value = getCurrentLang();
      langSelect.addEventListener("change", () => applyLanguage(langSelect.value));
    }

    // Print functionality
    document.querySelectorAll("[data-print]").forEach(btn => {
      btn.addEventListener("click", () => window.print());
    });
  };

  // Run initialization
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", setupCommonUI);
  } else {
    setupCommonUI();
  }
  applyTheme(getTheme());
})();

(() => {
  const root = document.getElementById("outline-nav");
  const main = document.querySelector(".module-main");
  if (!root || !main) return;

  const allHeadings = [...main.querySelectorAll("h2, h3")];
  const list = document.createElement("ul");
  list.className = "outline-list";

  const slugify = (text) =>
    text.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/(^-|-$)/g, "").slice(0, 64) || "section";

  const ensureId = (heading) => {
    if (heading.id) return heading.id;
    const base = slugify(heading.textContent || "section");
    let candidate = base;
    let index = 2;
    while (document.getElementById(candidate)) {
      candidate = `${base}-${index++}`;
    }
    heading.id = candidate;
    return candidate;
  };

  const headings = [];
  const links = new Map();

  let currentLi = null;
  let currentSubList = null;

  allHeadings.forEach((heading) => {
    const isH2 = heading.tagName.toLowerCase() === "h2";
    const id = ensureId(heading);
    const a = document.createElement("a");
    a.href = `#${id}`;
    a.textContent = heading.textContent || "Section";
    headings.push(heading);
    links.set(id, a);

    if (isH2) {
      currentLi = document.createElement("li");
      const row = document.createElement("div");
      row.className = "outline-item-row";
      const spacer = document.createElement("div");
      spacer.className = "outline-toggle-spacer";
      row.appendChild(spacer);
      row.appendChild(a);
      currentLi.appendChild(row);
      list.appendChild(currentLi);
      currentSubList = null;
    } else if (currentLi) {
      if (!currentSubList) {
        const subList = document.createElement("ul");
        subList.className = "outline-list outline-sublist";
        currentLi.appendChild(subList);
        currentSubList = subList;
        const row = currentLi.querySelector(".outline-item-row");
        const spacer = row.querySelector(".outline-toggle-spacer");
        if (spacer) spacer.remove();
        const toggle = document.createElement("button");
        toggle.type = "button";
        toggle.className = "outline-toggle";
        toggle.setAttribute("aria-expanded", "true");
        toggle.textContent = "▾";
        row.insertBefore(toggle, row.firstChild);
        toggle.addEventListener("click", () => {
          const isExpanded = toggle.getAttribute("aria-expanded") === "true";
          toggle.setAttribute("aria-expanded", String(!isExpanded));
          toggle.textContent = !isExpanded ? "▾" : "▸";
          subList.hidden = isExpanded;
        });
      }
      const subLi = document.createElement("li");
      subLi.appendChild(a);
      currentSubList.appendChild(subLi);
    }
  });

  root.replaceChildren(list);

  const markActive = () => {
    let active = headings[0];
    for (const heading of headings) {
      if (heading.getBoundingClientRect().top <= 130) active = heading;
      else break;
    }
    links.forEach((a) => a.classList.remove("active"));
    const activeLink = links.get(active.id || "");
    if (activeLink) activeLink.classList.add("active");
  };

  window.addEventListener("scroll", markActive, { passive: true });
  window.addEventListener("hashchange", markActive);
  markActive();
})();

(() => {
  const figures = [...document.querySelectorAll("figure[data-zoomable] img")];
  if (figures.length === 0) return;

  const lightbox = document.createElement("div");
  lightbox.className = "figure-lightbox";
  lightbox.hidden = true;
  lightbox.setAttribute("role", "dialog");
  lightbox.setAttribute("aria-modal", "true");
  lightbox.setAttribute("aria-label", "Image viewer");
  lightbox.innerHTML = `<div class="figure-lightbox-inner"><img class="figure-lightbox-image" alt=""><p class="figure-lightbox-caption"></p></div>`;
  document.body.appendChild(lightbox);

  const lightboxImg = lightbox.querySelector(".figure-lightbox-image");
  const lightboxCaption = lightbox.querySelector(".figure-lightbox-caption");

  const closeLightbox = () => {
    lightbox.hidden = true;
    document.body.style.overflow = "";
  };

  const openLightbox = (img) => {
    const caption = img.closest("figure")?.querySelector("figcaption")?.textContent || "";
    lightboxImg.src = img.currentSrc || img.src;
    lightboxImg.alt = img.alt || "";
    lightboxCaption.textContent = caption;
    lightbox.hidden = false;
    document.body.style.overflow = "hidden";
  };

  figures.forEach((img) => {
    img.addEventListener("click", () => openLightbox(img));
  });

  lightbox.addEventListener("click", (event) => {
    if (event.target === lightbox || event.target === lightboxImg) closeLightbox();
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && !lightbox.hidden) closeLightbox();
  });
})();
