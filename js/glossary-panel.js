(() => {
  const shell = document.querySelector(".glossary-panel-shell");
  if (!shell) return;

  const openers = document.querySelectorAll("[data-glossary-open]");
  const glossaryLinks = document.querySelectorAll('a[href^="glossaire.html"]:not(.glossary-full-link)');
  const closers = shell.querySelectorAll("[data-glossary-close]");
  const search = shell.querySelector("[data-glossary-search]");
  const items = Array.from(shell.querySelectorAll("[data-glossary-item]"));
  let lastFocus = null;

  const applySearch = (value = "") => {
    if (search) search.value = value;
    const query = value.trim().toLowerCase();
    items.forEach((item) => {
      const text = item.dataset.glossaryText || "";
      item.classList.toggle("is-hidden", Boolean(query) && !text.includes(query));
    });
  };

  const openPanel = (term = "") => {
    lastFocus = document.activeElement;
    shell.classList.add("is-open");
    shell.setAttribute("aria-hidden", "false");
    document.body.classList.add("glossary-panel-open");
    if (term) applySearch(term);
    window.setTimeout(() => search?.focus(), 80);
  };

  const closePanel = () => {
    shell.classList.remove("is-open");
    shell.setAttribute("aria-hidden", "true");
    document.body.classList.remove("glossary-panel-open");
    if (lastFocus && typeof lastFocus.focus === "function") {
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
    if (event.key === "Escape" && shell.classList.contains("is-open")) {
      closePanel();
    }
  });
})();

/* V95–V98 visual clarity layer: responsive modes, concept replacements,
   dense-page hierarchy and a semantic graphic language. */
(() => {
  const genericSeriesSignature = "120,270 190,210 260,232 330,150 405,182 480,108 560,132 640,82 760,104";
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

  function replaceDecorativeSeries() {
    document.querySelectorAll("svg").forEach((svg) => {
      const signature = svg.querySelector("polyline")?.getAttribute("points");
      if (signature !== genericSeriesSignature) return;

      const chart = svg.closest(".chart");
      if (!chart) return;

      const titleNode = [...svg.querySelectorAll("text")].find((node) => (
        node.getAttribute("text-anchor") === "middle" && number(node, "y") <= 40
      ));
      const title = titleNode?.textContent.trim() || svg.getAttribute("aria-label") || "Lecture visuelle";
      const steps = title.split(/\s*(?:->|→)\s*/).map((step) => step.trim()).filter(Boolean);
      const displayTitle = title.replaceAll("->", "→");
      const legendLabels = [...svg.querySelectorAll('text[x="102"]')].slice(0, 3);
      const legendDots = [...svg.querySelectorAll('circle[cx="86"]')].slice(0, 3);

      const visual = document.createElement("div");
      visual.className = "concept-visual";
      visual.setAttribute("role", "img");
      visual.setAttribute("aria-label", svg.getAttribute("aria-label") || title);

      const heading = document.createElement("strong");
      heading.className = "concept-visual-title";
      heading.textContent = displayTitle;
      visual.append(heading);

      if (steps.length > 1) {
        const sequence = document.createElement("ol");
        sequence.className = "concept-sequence";
        steps.forEach((step, index) => {
          const item = document.createElement("li");
          const count = document.createElement("span");
          count.textContent = String(index + 1).padStart(2, "0");
          const label = document.createElement("b");
          label.textContent = step;
          item.append(count, label);
          sequence.append(item);
        });
        visual.append(sequence);
      }

      if (legendLabels.length && steps.length === 1) {
        const comparison = document.createElement("div");
        comparison.className = "concept-comparison";
        legendLabels.forEach((labelNode, index) => {
          const item = document.createElement("article");
          const color = legendDots[index]?.getAttribute("fill") || ["#26a69a", "#4fc3f7", "#ef5350"][index];
          item.style.setProperty("--concept-accent", color);
          const count = document.createElement("small");
          count.textContent = `ISSUE ${String(index + 1).padStart(2, "0")}`;
          const label = document.createElement("b");
          label.textContent = labelNode.textContent.trim();
          item.append(count, label);
          comparison.append(item);
        });
        visual.append(comparison);
      }

      chart.classList.add("chart--concept");
      chart.dataset.visualVersion = "v96";
      svg.replaceWith(visual);
    });
  }

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

  replaceDecorativeSeries();
  classifyDenseCharts();
  normalizeGraphicSemantics();
  classifyResponsiveModes();
  requestAnimationFrame(updateScrollableVisuals);

  let resizeFrame = 0;
  window.addEventListener("resize", () => {
    window.cancelAnimationFrame(resizeFrame);
    resizeFrame = window.requestAnimationFrame(updateScrollableVisuals);
  }, { passive: true });
})();
