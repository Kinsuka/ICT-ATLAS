/* V101 — keyboard entry point shared by every lesson page. */
(() => {
  const main = document.querySelector("main");
  if (!main) return;
  if (!main.id) main.id = "contenu";
  if (!main.hasAttribute("tabindex")) main.tabIndex = -1;
  if (document.querySelector(".skip-link")) return;

  const skipLink = document.createElement("a");
  skipLink.className = "skip-link";
  skipLink.href = `#${main.id}`;
  skipLink.textContent = "Aller au contenu principal";
  skipLink.addEventListener("click", () => {
    window.requestAnimationFrame(() => main.focus({ preventScroll: true }));
  });
  document.body.prepend(skipLink);
})();

(() => {
  const shell = document.querySelector(".glossary-panel-shell");
  if (!shell) return;

  const openers = document.querySelectorAll("[data-glossary-open]");
  const glossaryLinks = document.querySelectorAll('a[href^="glossaire.html"]:not(.glossary-full-link)');
  const closers = shell.querySelectorAll("[data-glossary-close]");
  const search = shell.querySelector("[data-glossary-search]");
  const list = shell.querySelector("[data-glossary-list]");
  const loading = shell.querySelector("[data-glossary-loading]");
  let items = Array.from(shell.querySelectorAll("[data-glossary-item]"));
  let glossaryDataPromise = null;
  const panel = shell.querySelector(".glossary-panel");
  const backgroundElements = [...document.body.children].filter((element) => (
    element !== shell && element.tagName !== "SCRIPT" && !element.hasAttribute("inert")
  ));
  let lastFocus = null;

  shell.id = shell.id || "glossary-panel-shell";
  panel?.setAttribute("tabindex", "-1");
  openers.forEach((opener) => {
    opener.setAttribute("aria-controls", shell.id);
    opener.setAttribute("aria-expanded", "false");
  });

  const focusableElements = () => [...(panel?.querySelectorAll([
    "a[href]",
    "button:not([disabled])",
    "input:not([disabled])",
    "select:not([disabled])",
    "textarea:not([disabled])",
    "[tabindex]:not([tabindex='-1'])",
  ].join(",")) || [])].filter((element) => element.getClientRects().length > 0);

  const populateGlossary = (terms = []) => {
    if (!list || items.length || !Array.isArray(terms) || !terms.length) return;
    const fragment = document.createDocumentFragment();
    terms.forEach(([term, definition]) => {
      const item = document.createElement("article");
      item.className = "glossary-item";
      item.dataset.glossaryItem = "";
      item.dataset.glossaryText = `${term} ${definition}`.toLocaleLowerCase("fr");
      const title = document.createElement("h3");
      title.textContent = term;
      const description = document.createElement("p");
      description.textContent = definition;
      item.append(title, description);
      fragment.append(item);
    });
    list.replaceChildren(fragment);
    items = Array.from(list.querySelectorAll("[data-glossary-item]"));
    applySearch(search?.value || "");
  };

  const loadGlossaryData = () => {
    if (items.length) return Promise.resolve(items);
    if (window.ICT_ATLAS_GLOSSARY_TERMS) {
      populateGlossary(window.ICT_ATLAS_GLOSSARY_TERMS);
      return Promise.resolve(items);
    }
    if (glossaryDataPromise) return glossaryDataPromise;

    if (loading) loading.textContent = "Chargement du glossaire…";
    glossaryDataPromise = new Promise((resolve) => {
      const sourceScript = [...document.scripts]
        .find((script) => script.src.endsWith("/glossary-panel.js"));
      if (!sourceScript) {
        if (loading) loading.textContent = "Le glossaire rapide est indisponible. Ouvre la page complète.";
        resolve([]);
        return;
      }
      const dataScript = document.createElement("script");
      dataScript.src = new URL("glossary-data.js", sourceScript.src).href;
      dataScript.async = true;
      dataScript.addEventListener("load", () => {
        populateGlossary(window.ICT_ATLAS_GLOSSARY_TERMS);
        resolve(items);
      }, { once: true });
      dataScript.addEventListener("error", () => {
        if (loading) loading.textContent = "Le glossaire rapide est indisponible. Ouvre la page complète.";
        resolve([]);
      }, { once: true });
      document.head.append(dataScript);
    });
    return glossaryDataPromise;
  };

  const applySearch = (value = "") => {
    if (search) search.value = value;
    const query = value.trim().toLowerCase();
    items.forEach((item) => {
      const text = item.dataset.glossaryText || "";
      item.classList.toggle("is-hidden", Boolean(query) && !text.includes(query));
    });
  };

  const openPanel = (term = "") => {
    if (shell.classList.contains("is-open")) return;
    lastFocus = document.activeElement;
    shell.classList.add("is-open");
    shell.setAttribute("aria-hidden", "false");
    document.body.classList.add("glossary-panel-open");
    void loadGlossaryData();
    backgroundElements.forEach((element) => {
      element.setAttribute("inert", "");
      element.dataset.glossaryInert = "true";
    });
    openers.forEach((opener) => opener.setAttribute("aria-expanded", "true"));
    if (term) applySearch(term);
    window.setTimeout(() => (search || panel)?.focus(), 80);
  };

  const closePanel = () => {
    if (!shell.classList.contains("is-open")) return;
    shell.classList.remove("is-open");
    shell.setAttribute("aria-hidden", "true");
    document.body.classList.remove("glossary-panel-open");
    backgroundElements.forEach((element) => {
      if (element.dataset.glossaryInert === "true") {
        element.removeAttribute("inert");
        delete element.dataset.glossaryInert;
      }
    });
    openers.forEach((opener) => opener.setAttribute("aria-expanded", "false"));
    if (lastFocus?.isConnected && typeof lastFocus.focus === "function") {
      lastFocus.focus();
    }
  };

  openers.forEach((button) => button.addEventListener("click", () => openPanel()));
  document.querySelectorAll("[data-glossary-term]").forEach((termButton) => {
    termButton.addEventListener("click", () => {
      openPanel(termButton.dataset.glossaryTerm || termButton.textContent || "");
    });
  });
  glossaryLinks.forEach((link) => {
    link.addEventListener("click", (event) => {
      event.preventDefault();
      openPanel();
    });
  });
  closers.forEach((button) => button.addEventListener("click", closePanel));
  search?.addEventListener("input", () => applySearch(search.value));

  document.addEventListener("keydown", (event) => {
    if (!shell.classList.contains("is-open")) return;
    if (event.key === "Escape") {
      event.preventDefault();
      closePanel();
      return;
    }
    if (event.key !== "Tab") return;

    const focusable = focusableElements();
    if (!focusable.length) {
      event.preventDefault();
      panel?.focus();
      return;
    }
    const first = focusable[0];
    const last = focusable[focusable.length - 1];
    if (event.shiftKey && (document.activeElement === first || !panel.contains(document.activeElement))) {
      event.preventDefault();
      last.focus();
    } else if (!event.shiftKey && document.activeElement === last) {
      event.preventDefault();
      first.focus();
    }
  });

  document.addEventListener("focusin", (event) => {
    if (!shell.classList.contains("is-open") || panel.contains(event.target)) return;
    (focusableElements()[0] || panel)?.focus();
  });
})();

/* V99 — editorial reading modes for the three densest lessons. */
(() => {
  const currentPage = window.location.pathname.split("/").pop() || "index.html";
  const pageConfigs = {
    "04-setups-core.html": {
      eyebrow: "Leçon 25 · Carte de lecture",
      intro: "Commence par les mécanismes indispensables, entraîne ensuite la reconnaissance, puis consulte les prérequis comme référence.",
      essential: [
        "v80-une-narrative-trois-entrees",
        "templates-market-structure-setups",
        "fvg-bull",
        "mss-bull",
        "ob-bull",
        "breaker-bear",
        "ote-anchor",
      ],
      application: [
        "fvg-bear",
        "fvg-abc-series",
        "asia-rf",
      ],
    },
    "05-variantes.html": {
      eyebrow: "Leçon 27 · Carte de lecture",
      intro: "Isole d’abord les erreurs de validation les plus fréquentes, puis compare-les aux situations de marché qui exigent un refus.",
      essential: [
        "ce-fail",
        "false-no-hunt",
        "false-no-fvg",
        "fvg-hors-contexte",
        "fvg-trop-tardif",
        "micro-mss-force",
        "ob-invalide",
        "ote-mauvais-ancrage",
      ],
      application: [
        "asia-vraie-cassure",
        "nyam-pdh-run",
        "trend-day-no-entry",
        "range-day-complet",
      ],
    },
    "06-contextes-avances.html": {
      eyebrow: "Leçon 30 · Carte de lecture",
      intro: "Construis le contexte en couches, vérifie-le sur des scénarios opposés, puis ouvre les cas événementiels en approfondissement.",
      essential: [
        "smt-divergence",
        "fomc-timeline",
        "daily-bias-strong-bull",
        "daily-bias-weak",
        "daily-bias-moderate",
        "narrative-bull-strong",
        "narrative-invalidated",
        "narrative-bear-strong",
      ],
      application: ["smt-bull-clear", "smt-bear-clear", "smt-false-no-trade"],
    },
  };
  const config = pageConfigs[currentPage];
  const main = document.querySelector("main.page");
  if (!config || !main) return;

  const sections = [...main.querySelectorAll(":scope > section.card[id]")];
  if (!sections.length) return;

  const essentialIds = new Set(config.essential);
  const applicationIds = new Set(config.application);
  const tiers = {
    essential: [],
    application: [],
    reference: [],
  };

  sections.forEach((section) => {
    const tier = essentialIds.has(section.id)
      ? "essential"
      : applicationIds.has(section.id)
        ? "application"
        : "reference";
    section.dataset.learningTier = tier;
    tiers[tier].push(section);
  });

  const readingMap = document.createElement("section");
  readingMap.className = "lesson-reading-map";
  readingMap.setAttribute("aria-labelledby", "lesson-reading-map-title");
  readingMap.innerHTML = `
    <div class="reading-map-intro">
      <span>${config.eyebrow}</span>
      <h2 id="lesson-reading-map-title">Choisis la profondeur utile maintenant</h2>
      <p>${config.intro}</p>
    </div>
    <div class="reading-mode-control" role="group" aria-label="Mode de lecture">
      <button type="button" data-reading-mode="essential">Essentiel</button>
      <button type="button" data-reading-mode="guided">Guidé</button>
      <button type="button" data-reading-mode="all">Tout afficher</button>
    </div>
    <div class="reading-tier-grid"></div>
    <p class="reading-mode-status" aria-live="polite"></p>
  `;

  const tierGrid = readingMap.querySelector(".reading-tier-grid");
  [
    ["essential", "01", "Essentiel", "Les mécanismes à savoir expliquer sans aide."],
    ["application", "02", "Application", "Les cas à comparer pour entraîner la décision."],
    ["reference", "03", "Approfondissement", "La bibliothèque complète à consulter au besoin."],
  ].forEach(([tier, number, label, description]) => {
    const firstSection = tiers[tier][0];
    const link = document.createElement("a");
    link.className = `reading-tier-link is-${tier}`;
    link.href = firstSection ? `#${firstSection.id}` : "#lesson-reading-map-title";
    link.dataset.readingTierLink = tier;
    link.innerHTML = `
      <small>${number} · ${tiers[tier].length} sections</small>
      <strong>${label}</strong>
      <span>${description}</span>
    `;
    tierGrid.append(link);
  });

  const insertionPoint = main.querySelector(".page-meta-dashboard") || main.querySelector(".lesson-objectives");
  insertionPoint?.insertAdjacentElement("afterend", readingMap);
  document.body.classList.add("has-editorial-reading-map");

  const buttons = [...readingMap.querySelectorAll("[data-reading-mode]")];
  const status = readingMap.querySelector(".reading-mode-status");

  function applyMode(mode) {
    const visibleTiers = mode === "essential"
      ? new Set(["essential"])
      : mode === "guided"
        ? new Set(["essential", "application"])
        : new Set(["essential", "application", "reference"]);
    let visibleCount = 0;

    sections.forEach((section) => {
      const visible = visibleTiers.has(section.dataset.learningTier);
      section.hidden = !visible;
      if (visible) visibleCount += 1;
    });
    buttons.forEach((button) => {
      const active = button.dataset.readingMode === mode;
      button.classList.toggle("is-active", active);
      button.setAttribute("aria-pressed", String(active));
    });
    readingMap.dataset.readingMode = mode;
    const hiddenCount = sections.length - visibleCount;
    status.textContent = hiddenCount
      ? `${visibleCount} sections affichées · ${hiddenCount} disponibles dans le mode complet.`
      : `${visibleCount} sections affichées · leçon complète.`;
    window.dispatchEvent(new CustomEvent("ict-atlas:visual-layout"));
  }

  buttons.forEach((button) => button.addEventListener("click", () => applyMode(button.dataset.readingMode)));
  readingMap.querySelectorAll("[data-reading-tier-link]").forEach((link) => {
    link.addEventListener("click", () => {
      const tier = link.dataset.readingTierLink;
      applyMode(tier === "reference" ? "all" : tier === "application" ? "guided" : "essential");
    });
  });

  function revealHashTarget() {
    if (!window.location.hash) return false;
    const target = document.getElementById(decodeURIComponent(window.location.hash.slice(1)));
    if (!target?.closest("section[data-learning-tier]")) return false;
    applyMode("all");
    return true;
  }

  if (!revealHashTarget()) applyMode("guided");
  window.addEventListener("hashchange", revealHashTarget);
})();

/* V100 — explicit editorial roles and readable Atlas case numbers. */
(() => {
  const currentPage = window.location.pathname.split("/").pop() || "index.html";
  const lessonArc = [
    {
      file: "03-fondations.html",
      number: "03",
      verb: "Décider",
      description: "Construire la grille avant de regarder un setup.",
    },
    {
      file: "04-setups-core.html",
      number: "04",
      verb: "Reconnaître",
      description: "Assembler les briques validées en modèles exécutables.",
    },
    {
      file: "05-variantes.html",
      number: "05",
      verb: "Refuser",
      description: "Nommer ce qui manque dans un signal séduisant.",
    },
    {
      file: "06-contextes-avances.html",
      number: "06",
      verb: "Contextualiser",
      description: "Adapter la décision sans ajouter de signal magique.",
    },
  ];
  if (!lessonArc.some(({ file }) => file === currentPage)) return;

  const main = document.querySelector("main.page");
  const objectives = main?.querySelector(".lesson-objectives");
  if (!main || !objectives) return;

  if (!main.querySelector(".lesson-role-arc")) {
    const arc = document.createElement("nav");
    arc.className = "lesson-role-arc";
    arc.setAttribute("aria-labelledby", "lesson-role-arc-title");
    arc.innerHTML = `
      <div class="lesson-role-arc-head">
        <span>Arc éditorial · leçons 03 à 06</span>
        <h2 id="lesson-role-arc-title">Une fonction différente à chaque étape</h2>
      </div>
      <ol></ol>
    `;
    const list = arc.querySelector("ol");
    lessonArc.forEach(({ file, number, verb, description }) => {
      const item = document.createElement("li");
      const link = document.createElement("a");
      const active = file === currentPage;
      link.href = file;
      link.className = active ? "is-current" : "";
      if (active) link.setAttribute("aria-current", "page");
      link.innerHTML = `<small>${number}</small><strong>${verb}</strong><span>${description}</span>`;
      item.append(link);
      list.append(item);
    });
    objectives.insertAdjacentElement("afterend", arc);
  }

  main.querySelectorAll(":scope > section.card > header h2").forEach((heading) => {
    if (heading.querySelector(".atlas-case-number")) return;
    const prefixNode = [...heading.childNodes].find((node) => (
      node.nodeType === Node.TEXT_NODE && /^\s*\d{2}\s*—\s*/.test(node.nodeValue || "")
    ));
    if (!prefixNode) return;
    const match = prefixNode.nodeValue.match(/^\s*(\d{2})\s*—\s*/);
    if (!match) return;

    prefixNode.nodeValue = prefixNode.nodeValue.replace(match[0], "");
    const title = heading.textContent.trim();
    const badge = document.createElement("span");
    badge.className = "atlas-case-number";
    badge.setAttribute("aria-hidden", "true");
    badge.textContent = `Cas Atlas ${match[1]}`;
    heading.prepend(badge);
    heading.setAttribute("aria-label", `Cas Atlas ${match[1]} — ${title}`);
  });
})();

/* V95–V98 visual clarity layer: responsive modes, concept replacements,
   dense-page hierarchy and a semantic graphic language. */
(() => {
  const visualSelectors = [
    ".chart",
    ".exam-chart",
    ".guided-case-chart",
    ".sim-chart-wrap",
    ".historical-chart-scroll",
  ];
  const scrollSelector = visualSelectors.join(",");
  const visualSvgSelector = visualSelectors.map((selector) => `${selector} svg`).join(",");
  const priorityPages = new Set([
    "04-setups-core.html",
    "05-variantes.html",
    "06-contextes-avances.html",
    "07-failures-journees.html",
    "24-premium-discount-killzones.html",
  ]);
  const redStrokes = new Set(["#ef5350", "#ff6868", "#f87171"]);
  const zoneStrokes = new Set(["#26a69a", "#4fc3f7", "#53d6e9", "#8e44ad", "#4caf50"]);

  const number = (node, attribute) => Number.parseFloat(node.getAttribute(attribute) || "0");
  const currentPage = window.location.pathname.split("/").pop() || "index.html";
  document.body.classList.toggle("visual-priority-page", priorityPages.has(currentPage));

  function classifyDenseCharts() {
    document.querySelectorAll(".chart svg").forEach((svg) => {
      const chart = svg.closest(".chart");
      if (!chart || chart.closest(".abc-case") || chart.classList.contains("chart--concept")) return;

      const texts = [...svg.querySelectorAll("text")];
      const lines = [...svg.querySelectorAll("line")];
      if (texts.length < 10 || lines.length < 6) return;

      chart.classList.add("chart--dense");
      if (priorityPages.has(currentPage)) chart.classList.add("chart--priority");
      const viewBox = svg.viewBox.baseVal;
      const rightEdge = viewBox.x + viewBox.width * 0.86;

      lines.forEach((line) => {
        const stroke = (line.getAttribute("stroke") || "").toLowerCase();
        if (["#1e3a5f", "#243e5e", "#314c6b", "#1b3249"].includes(stroke) && !line.hasAttribute("stroke-dasharray")) {
          line.classList.add("visual-grid-line");
        }
        if (number(line, "x1") >= rightEdge && number(line, "x2") >= rightEdge) {
          line.classList.add("visual-axis-detail");
        }
      });

      texts.forEach((text) => {
        const content = text.textContent.trim();
        if (number(text, "x") >= rightEdge && /^\d+(?:[.,]\d+)?$/.test(content)) {
          text.classList.add("visual-axis-detail");
        }
      });

      if (!chart.querySelector(".visual-density-controls")) {
        const controls = document.createElement("div");
        controls.className = "visual-density-controls";
        const note = document.createElement("span");
        note.className = "visual-line-key";
        note.setAttribute("aria-label", "Code visuel du graphique");
        [
          ["observed", "Observé"],
          ["level", "Niveau"],
          ["zone", "Zone"],
          ["projection", "Projection"],
          ["invalidation", "Invalidation"],
        ].forEach(([type, label]) => {
          const key = document.createElement("span");
          key.className = `visual-line-key-item is-${type}`;
          key.textContent = label;
          note.append(key);
        });
        const toggle = document.createElement("button");
        toggle.type = "button";
        toggle.className = "visual-density-toggle";
        toggle.setAttribute("aria-pressed", "false");
        toggle.textContent = "Afficher grille et axe";
        toggle.addEventListener("click", () => {
          const expanded = chart.classList.toggle("show-secondary-visuals");
          toggle.setAttribute("aria-pressed", String(expanded));
          toggle.textContent = expanded ? "Masquer grille et axe" : "Afficher grille et axe";
        });
        controls.append(note, toggle);
        chart.prepend(controls);
      }
    });
  }

  function normalizeGraphicSemantics() {
    document.querySelectorAll(visualSvgSelector).forEach((svg) => {
      const viewBox = svg.viewBox.baseVal;
      if (!viewBox.width || !viewBox.height) return;

      svg.querySelectorAll("line").forEach((line) => {
        if (line.classList.contains("visual-grid-line") || line.classList.contains("visual-axis-detail")) return;
        const stroke = (line.getAttribute("stroke") || "").toLowerCase();
        const dashed = line.hasAttribute("stroke-dasharray");
        const horizontal = Math.abs(number(line, "y1") - number(line, "y2")) < 0.5;
        const span = Math.abs(number(line, "x2") - number(line, "x1"));
        const longLine = span > viewBox.width * 0.28;

        if (redStrokes.has(stroke) && horizontal && longLine) {
          line.classList.add("visual-invalidation-line");
        } else if (dashed && horizontal && longLine) {
          line.classList.add("visual-level-line");
        } else if (dashed) {
          line.classList.add("visual-projection-line");
        } else if (horizontal && longLine && zoneStrokes.has(stroke)) {
          line.classList.add("visual-zone-boundary");
        }
      });

      svg.querySelectorAll("path, polyline").forEach((shape) => {
        const fill = (shape.getAttribute("fill") || "").toLowerCase();
        const stroke = shape.getAttribute("stroke");
        if (!stroke || (fill && fill !== "none")) return;
        if (shape.hasAttribute("stroke-dasharray")) {
          shape.classList.add("visual-projection-line");
        } else {
          shape.classList.add("visual-observed-line");
        }
      });

      svg.querySelectorAll("rect").forEach((rect) => {
        const fill = (rect.getAttribute("fill") || "").toLowerCase();
        const opacity = Number.parseFloat(rect.getAttribute("opacity") || "1");
        const isLargeZone = number(rect, "width") > viewBox.width * 0.24
          && number(rect, "height") > viewBox.height * 0.025
          && number(rect, "height") < viewBox.height * 0.78
          && opacity <= 0.32;
        if (!isLargeZone) return;
        rect.classList.add(redStrokes.has(fill) ? "visual-invalidation-zone" : "visual-zone-shape");
      });
    });
  }

  function classifyResponsiveModes() {
    document.querySelectorAll(scrollSelector).forEach((container) => {
      container.classList.remove("visual-mode-fit", "visual-mode-scroll");
      delete container.dataset.visualMode;

      if (container.classList.contains("chart--concept")) {
        container.classList.add("visual-mode-fit");
        container.dataset.visualMode = "fit";
        return;
      }

      const svg = container.querySelector(":scope > svg") || container.querySelector("svg");
      if (!svg) return;
      const viewBox = svg.viewBox.baseVal;
      if (!viewBox.width) return;

      const fontSizes = [...svg.querySelectorAll("text")]
        .map((text) => Number.parseFloat(
          text.getAttribute("font-size") || text.closest("[font-size]")?.getAttribute("font-size") || "0",
        ))
        .filter((size) => size > 0);
      const smallestLabel = fontSizes.length ? Math.min(...fontSizes) : 0;
      const widthForReadableLabels = smallestLabel ? (viewBox.width * 10.5) / smallestLabel : 0;
      const forcedScroll = container.classList.contains("chart--dense")
        || container.matches(".exam-chart, .guided-case-chart, .sim-chart-wrap, .historical-chart-scroll");
      const needsScroll = forcedScroll || widthForReadableLabels > container.clientWidth + 2;

      container.classList.add(needsScroll ? "visual-mode-scroll" : "visual-mode-fit");
      container.dataset.visualMode = needsScroll ? "scroll" : "fit";
      if (needsScroll) {
        const readableWidth = Math.min(1120, Math.max(704, Math.ceil(widthForReadableLabels || 704)));
        container.style.setProperty("--visual-scroll-width", `${readableWidth}px`);
      } else {
        container.style.removeProperty("--visual-scroll-width");
      }
    });
  }

  function updateScrollableVisuals() {
    classifyResponsiveModes();
    document.querySelectorAll(scrollSelector).forEach((container) => {
      if (container.classList.contains("chart--concept")) return;
      const scrollable = container.scrollWidth > container.clientWidth + 2;
      let hint = container.querySelector(":scope > .visual-pan-hint");
      container.classList.toggle("is-scrollable-visual", scrollable);

      if (scrollable && !hint) {
        hint = document.createElement("div");
        hint.className = "visual-pan-hint";
        hint.setAttribute("aria-hidden", "true");
        hint.innerHTML = "<span>↔</span> Balaye horizontalement pour lire tous les repères";
        container.prepend(hint);
        container.addEventListener("scroll", () => {
          container.classList.toggle("has-scrolled-visual", container.scrollLeft > 12);
        }, { passive: true });
      } else if (!scrollable && hint) {
        hint.remove();
      }
    });
  }

  let resizeFrame = 0;
  const scheduleVisualUpdate = () => {
    window.cancelAnimationFrame(resizeFrame);
    resizeFrame = window.requestAnimationFrame(updateScrollableVisuals);
  };
  const enhanceVisuals = () => {
    classifyDenseCharts();
    normalizeGraphicSemantics();
    updateScrollableVisuals();
    document.documentElement.dataset.visualsReady = "true";
    window.addEventListener("resize", scheduleVisualUpdate, { passive: true });
    window.addEventListener("ict-atlas:visual-layout", scheduleVisualUpdate);
  };

  if ("requestIdleCallback" in window) {
    window.requestIdleCallback(enhanceVisuals, { timeout: 350 });
  } else {
    window.setTimeout(enhanceVisuals, 0);
  }
})();
