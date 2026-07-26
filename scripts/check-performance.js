const { existsSync, readFileSync, readdirSync } = require('node:fs');
const path = require('node:path');
const { gzipSync } = require('node:zlib');

const root = path.resolve(__dirname, '..');
const budgets = JSON.parse(readFileSync(path.join(root, 'data/performance-budgets.json'), 'utf8'));
const htmlFiles = [
  path.join(root, 'index.html'),
  ...readdirSync(path.join(root, 'pages'))
    .filter((file) => file.endsWith('.html'))
    .sort()
    .map((file) => path.join(root, 'pages', file)),
];
const jsFiles = readdirSync(path.join(root, 'js'))
  .filter((file) => file.endsWith('.js'))
  .sort()
  .map((file) => path.join(root, 'js', file));
const failures = [];

function relative(file) {
  return path.relative(root, file);
}

function compressedBytes(buffer) {
  return gzipSync(buffer, { level: 9 }).length;
}

let totalHtmlBytes = 0;
let totalHtmlGzipBytes = 0;
let totalSvgBytes = 0;
let totalSvgCount = 0;
let prerenderedConcepts = 0;
let largestHtml = { file: '', bytes: 0, gzipBytes: 0 };
let largestSvgPage = { file: '', bytes: 0, count: 0 };

for (const file of htmlFiles) {
  const buffer = readFileSync(file);
  const html = buffer.toString('utf8');
  const gzipBytes = compressedBytes(buffer);
  const inlineSvgs = [...html.matchAll(/<svg\b[\s\S]*?<\/svg>/gi)].map((match) => match[0]);
  const svgBytes = inlineSvgs.reduce((sum, svg) => sum + Buffer.byteLength(svg), 0);
  totalHtmlBytes += buffer.length;
  totalHtmlGzipBytes += gzipBytes;
  totalSvgBytes += svgBytes;
  totalSvgCount += inlineSvgs.length;
  prerenderedConcepts += (html.match(/data-visual-version="v102"/g) || []).length;
  if (buffer.length > largestHtml.bytes) {
    largestHtml = { file: relative(file), bytes: buffer.length, gzipBytes };
  }
  if (svgBytes > largestSvgPage.bytes) {
    largestSvgPage = { file: relative(file), bytes: svgBytes, count: inlineSvgs.length };
  }

  if (buffer.length > budgets.htmlPageBytes) {
    failures.push(`${relative(file)}: ${buffer.length} octets HTML > budget ${budgets.htmlPageBytes}`);
  }
  if (gzipBytes > budgets.htmlPageGzipBytes) {
    failures.push(`${relative(file)}: ${gzipBytes} octets gzip > budget ${budgets.htmlPageGzipBytes}`);
  }
  if (inlineSvgs.length > budgets.svgElementsPerPage) {
    failures.push(`${relative(file)}: ${inlineSvgs.length} SVG > budget ${budgets.svgElementsPerPage}`);
  }
  if (svgBytes > budgets.inlineSvgPageBytes) {
    failures.push(`${relative(file)}: ${svgBytes} octets SVG > budget ${budgets.inlineSvgPageBytes}`);
  }
  if (/data-glossary-text="[^"]+"/.test(html) || /data-glossary-item/.test(html)) {
    failures.push(`${relative(file)}: les données du glossaire ne doivent plus être dupliquées dans le HTML`);
  }
  if (html.includes('120,270 190,210 260,232 330,150 405,182 480,108 560,132 640,82 760,104')) {
    failures.push(`${relative(file)}: un ancien SVG générique doit être préconverti en concept visuel`);
  }
  for (const match of html.matchAll(/<script\b([^>]*)>/gi)) {
    const attributes = match[1];
    if (!/\bsrc=/.test(attributes)) continue;
    if (!/\b(?:defer|async)\b|\btype=["']module["']/i.test(attributes)) {
      failures.push(`${relative(file)}: script externe sans defer, async ou module`);
    }
  }
}

if (totalHtmlBytes > budgets.htmlTotalBytes) {
  failures.push(`HTML total: ${totalHtmlBytes} octets > budget ${budgets.htmlTotalBytes}`);
}
if (totalHtmlGzipBytes > budgets.htmlTotalGzipBytes) {
  failures.push(`HTML gzip total: ${totalHtmlGzipBytes} octets > budget ${budgets.htmlTotalGzipBytes}`);
}
if (totalSvgBytes > budgets.inlineSvgTotalBytes) {
  failures.push(`SVG inline total: ${totalSvgBytes} octets > budget ${budgets.inlineSvgTotalBytes}`);
}
if (prerenderedConcepts !== 16) {
  failures.push(`Concepts V102 pré-rendus : ${prerenderedConcepts}, attendu : 16`);
}

const cssFile = path.join(root, 'css/style.css');
const cssGzipBytes = compressedBytes(readFileSync(cssFile));
if (cssGzipBytes > budgets.cssGzipBytes) {
  failures.push(`css/style.css: ${cssGzipBytes} octets gzip > budget ${budgets.cssGzipBytes}`);
}

for (const file of jsFiles) {
  const gzipBytes = compressedBytes(readFileSync(file));
  if (gzipBytes > budgets.javascriptFileGzipBytes) {
    failures.push(`${relative(file)}: ${gzipBytes} octets gzip > budget ${budgets.javascriptFileGzipBytes}`);
  }
}

if (!existsSync(path.join(root, '.nojekyll'))) {
  failures.push('.nojekyll absent : GitHub Pages lancera inutilement le traitement Jekyll');
}

if (failures.length) {
  console.error(failures.join('\n'));
  process.exitCode = 1;
} else {
  const savedRaw = 2438970 - totalHtmlBytes;
  const savedGzip = 524861 - totalHtmlGzipBytes;
  console.log([
    `Budgets V102 valides sur ${htmlFiles.length} pages.`,
    `HTML : ${totalHtmlBytes} octets (${totalHtmlGzipBytes} gzip).`,
    `Gain depuis l’audit : ${savedRaw} octets bruts, ${savedGzip} octets gzip.`,
    `Page la plus lourde : ${largestHtml.file} (${largestHtml.bytes} octets, ${largestHtml.gzipBytes} gzip).`,
    `SVG inline : ${totalSvgCount} figures, ${totalSvgBytes} octets ; maximum ${largestSvgPage.file} (${largestSvgPage.count} figures).`,
    `CSS partagé : ${cssGzipBytes} octets gzip ; ${jsFiles.length} scripts contrôlés.`,
  ].join('\n'));
}
