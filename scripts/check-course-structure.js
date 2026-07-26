const { existsSync, readFileSync, readdirSync, statSync } = require("node:fs");
const path = require("node:path");

const root = path.resolve(__dirname, "..");
const parts = JSON.parse(readFileSync(path.join(root, "data", "course-navigation.json"), "utf8"));
const lessons = parts.flatMap((part) => part.lessons.map(([file, title]) => ({ file, title })));

function hrefFor(currentFile, targetFile) {
  if (currentFile === "index.html") {
    return targetFile === "index.html" ? "index.html" : `pages/${targetFile}`;
  }
  return targetFile === "index.html" ? "../index.html" : targetFile;
}

function pagePath(file) {
  return file === "index.html" ? path.join(root, file) : path.join(root, "pages", file);
}

const failures = [];

function safeDecode(value) {
  try {
    return decodeURIComponent(value);
  } catch {
    return value;
  }
}

for (const lesson of lessons) {
  const html = readFileSync(pagePath(lesson.file), "utf8");
  const nav = html.match(/<aside\b[^>]*class="[^"]*\bsite-nav\b[^"]*"[^>]*>([\s\S]*?)<\/aside>/)?.[1] || "";
  const actualHrefs = [...nav.matchAll(/<li\b[^>]*class="[^"]*\bcourse-lesson\b[^"]*"[^>]*>\s*<a\b[^>]*href="([^"]+)"/g)]
    .map((match) => match[1]);
  const expectedHrefs = lessons.map(({ file }) => hrefFor(lesson.file, file));

  if (!nav) failures.push(`${lesson.file}: navigation principale absente`);
  if (JSON.stringify(actualHrefs) !== JSON.stringify(expectedHrefs)) {
    failures.push(`${lesson.file}: ordre ou liens de navigation désynchronisés`);
  }

  const activeCount = (nav.match(/class="course-lesson active"/g) || []).length;
  const activeHref = nav.match(/class="course-lesson active"[^>]*>\s*<a\b[^>]*href="([^"]+)"/)?.[1];
  if (activeCount !== 1 || activeHref !== hrefFor(lesson.file, lesson.file)) {
    failures.push(`${lesson.file}: leçon active incorrecte`);
  }

  const objectiveCards = [...html.matchAll(/class="lesson-objective"[\s\S]*?<strong>([^<]+)<\/strong>[\s\S]*?<p>([^<]+)<\/p>/g)]
    .map((match) => ({ label: match[1].trim(), body: match[2].trim() }));
  if (objectiveCards.length !== 3) failures.push(`${lesson.file}: trois objectifs pédagogiques sont requis`);
  if (!objectiveCards.some(({ label }) => label === "Objectif")) failures.push(`${lesson.file}: objectif principal absent`);
  if (!objectiveCards.some(({ label }) => label === "Checkpoint")) failures.push(`${lesson.file}: checkpoint mesurable absent`);
  if (objectiveCards.some(({ body }) => body.includes("Comprendre le rôle de cette leçon dans le parcours complet"))) {
    failures.push(`${lesson.file}: objectif générique non remplacé`);
  }
}

const sitemap = readFileSync(path.join(root, "sitemap.xml"), "utf8");
const requiredPublicPages = [
  ...lessons.map(({ file }) => (file === "index.html" ? "" : `pages/${file}`)),
  "pages/examen-decision-session.html",
  "pages/programme-validation-20-sessions.html",
];

for (const publicPath of requiredPublicPages) {
  const url = `https://kinsuka.github.io/ICT-ATLAS/${publicPath}`;
  if (!sitemap.includes(`<loc>${url}</loc>`)) failures.push(`sitemap: URL absente ${url}`);
}

const legacyVocabulary = readFileSync(path.join(root, "pages", "02-vocabulaire.html"), "utf8");
if (!legacyVocabulary.includes('content="noindex, follow" name="robots"')) {
  failures.push("02-vocabulaire.html: la redirection legacy doit rester noindex");
}
if (!legacyVocabulary.includes('href="https://kinsuka.github.io/ICT-ATLAS/pages/glossaire.html" rel="canonical"')) {
  failures.push("02-vocabulaire.html: URL canonique du glossaire absente");
}
if (sitemap.includes("pages/02-vocabulaire.html")) {
  failures.push("sitemap: la redirection legacy 02-vocabulaire ne doit pas être indexée");
}

const allHtmlFiles = [
  path.join(root, "index.html"),
  ...readdirSync(path.join(root, "pages"))
    .filter((file) => file.endsWith(".html"))
    .map((file) => path.join(root, "pages", file)),
];

for (const sourcePath of allHtmlFiles) {
  const html = readFileSync(sourcePath, "utf8");
  const sourceLabel = path.relative(root, sourcePath);
  const hrefs = [...html.matchAll(/\bhref="([^"]+)"/g)].map((match) => match[1]);

  const viewport = html.match(/<meta\b[^>]*name="viewport"[^>]*content="([^"]+)"/i)?.[1]
    || html.match(/<meta\b[^>]*content="([^"]+)"[^>]*name="viewport"/i)?.[1]
    || "";
  if (!viewport) failures.push(`${sourceLabel}: viewport responsive absent`);
  if (/user-scalable\s*=\s*no|maximum-scale\s*=\s*1(?:\.0)?(?:,|$)/i.test(viewport)) {
    failures.push(`${sourceLabel}: le zoom utilisateur ne doit pas être désactivé`);
  }

  for (const href of hrefs) {
    if (!href || href === "#" || /^(?:https?:|mailto:|tel:|data:|\/\/)/i.test(href)) continue;
    const [rawTarget, rawHash = ""] = href.split("#", 2);
    const targetWithoutQuery = rawTarget.split("?", 1)[0];
    let targetPath = targetWithoutQuery
      ? path.resolve(path.dirname(sourcePath), safeDecode(targetWithoutQuery))
      : sourcePath;
    if (existsSync(targetPath) && statSync(targetPath).isDirectory()) targetPath = path.join(targetPath, "index.html");

    const relativeTarget = path.relative(root, targetPath);
    if (relativeTarget.startsWith("..") || path.isAbsolute(relativeTarget)) {
      failures.push(`${sourceLabel}: lien hors projet ${href}`);
      continue;
    }
    if (!existsSync(targetPath)) {
      failures.push(`${sourceLabel}: cible absente ${href}`);
      continue;
    }

    const anchor = safeDecode(rawHash);
    if (!anchor || path.extname(targetPath).toLowerCase() !== ".html") continue;
    const targetHtml = readFileSync(targetPath, "utf8");
    const hasAnchor = targetHtml.includes(`id="${anchor}"`) || targetHtml.includes(`name="${anchor}"`);
    if (!hasAnchor) failures.push(`${sourceLabel}: ancre absente ${href}`);
  }
}

const setupCore = readFileSync(path.join(root, "pages", "04-setups-core.html"), "utf8");
const obsoletePrerequisiteIds = [
  "v63-bridge-order-blocks",
  "v64-bridge-fvg-imbalance",
  "v65-bridge-mss-shift",
  "v66-bridge-breaker-mitigation",
  "v67-bridge-pd-arrays",
  "v68-bridge-ote-dealing-range",
  "v69-bridge-dol-targets",
  "v70-bridge-smt-divergence",
  "v71-bridge-profils-journee",
];
if (obsoletePrerequisiteIds.some((id) => setupCore.includes(`id="${id}"`))) {
  failures.push("04-setups-core.html: les anciennes cartes de prérequis dupliquées sont revenues");
}
const prerequisiteLinks = setupCore.match(/class="prerequisite-matrix"[\s\S]*?<\/ol>/)?.[0].match(/<li>/g) || [];
if (prerequisiteLinks.length !== 9) failures.push("04-setups-core.html: la grille compacte doit contenir neuf prérequis");

if (failures.length) {
  console.error(failures.join("\n"));
  process.exitCode = 1;
} else {
  console.log(`Structure valide : ${parts.length} parties, ${lessons.length} leçons, navigation, checkpoints, liens, ancres, viewport et sitemap synchronisés.`);
}
