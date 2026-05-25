(() => {
  const shell = document.querySelector(".glossary-panel-shell");
  if (!shell) return;

  const openers = document.querySelectorAll("[data-glossary-open]");
  const glossaryLinks = document.querySelectorAll('a[href^="glossaire.html"]:not(.glossary-full-link)');
  const closers = shell.querySelectorAll("[data-glossary-close]");
  const search = shell.querySelector("[data-glossary-search]");
  const items = Array.from(shell.querySelectorAll("[data-glossary-item]"));
  let lastFocus = null;

  const openPanel = () => {
    lastFocus = document.activeElement;
    shell.classList.add("is-open");
    shell.setAttribute("aria-hidden", "false");
    document.body.classList.add("glossary-panel-open");
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

  const filterItems = () => {
    const query = (search?.value || "").trim().toLowerCase();
    items.forEach((item) => {
      const text = item.dataset.glossaryText || "";
      item.classList.toggle("is-hidden", Boolean(query) && !text.includes(query));
    });
  };

  openers.forEach((button) => button.addEventListener("click", openPanel));
  glossaryLinks.forEach((link) => {
    link.addEventListener("click", (event) => {
      event.preventDefault();
      openPanel();
    });
  });
  closers.forEach((button) => button.addEventListener("click", closePanel));
  search?.addEventListener("input", filterItems);

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && shell.classList.contains("is-open")) {
      closePanel();
    }
  });
})();
