const { test, expect } = require('@playwright/test');
const { mkdirSync } = require('node:fs');
const path = require('node:path');
const { pathToFileURL } = require('node:url');

const pages = [
  'index.html',
  'pages/00-precours-bases-trading.html',
  'pages/00-precours-01-graphique.html',
  'pages/00-precours-02-structure.html',
  'pages/00-precours-03-ordres.html',
  'pages/00-precours-04-liquidite.html',
  'pages/00-precours-05-trade-simple.html',
  'pages/00-precours-06-risque.html',
  'pages/00-precours-07-pont-ict.html',
  'pages/04-setups-core.html',
  'pages/08-quiz.html',
  'pages/11-mecanique-marches.html',
  'pages/14-live-chart.html',
  'pages/21-liquidite-deplacement.html',
  'pages/22-structure-trend-range.html',
  'pages/25-top-down-multi-timeframe.html',
  'pages/26-psychologie-trader.html',
  'pages/27-fondations-liquidite.html',
  'pages/28-fondations-entree.html',
  'pages/29-fondations-stop-tp.html',
  'pages/31-order-blocks.html',
  'pages/32-fvg-imbalance-ce.html',
  'pages/33-mss-changement-controle.html',
  'pages/39-profils-journee-sessions.html',
  'pages/40-displacement-operationnel.html',
  'pages/41-no-trade.html',
];

function fileUrl(fileName) {
  return pathToFileURL(path.join(__dirname, '..', fileName)).href;
}

test.describe('ICT Atlas visual smoke audit', () => {
  for (const fileName of pages) {
    test(`${fileName} renders SVG charts without obvious visual regressions`, async ({ page }, testInfo) => {
      await page.goto(fileUrl(fileName));
      await expect(page.locator('h1').first()).toBeVisible();

      const audit = await page.evaluate(() => {
        const svgs = [...document.querySelectorAll('svg')];
        const visibleAnswerLabels = [...document.querySelectorAll('svg text')]
          .filter((node) => node.textContent.includes('Réponse') && !node.closest('details'))
          .map((node) => node.textContent.trim());

        const invisibleSvgs = svgs
          .map((svg, index) => {
            const rect = svg.getBoundingClientRect();
            return {
              index,
              label: svg.getAttribute('aria-label') || '',
              width: Math.round(rect.width),
              height: Math.round(rect.height),
            };
          })
          .filter((item) => item.width < 80 || item.height < 50);

        const missingLabels = svgs
          .map((svg, index) => ({ index, label: svg.getAttribute('aria-label') || '' }))
          .filter((item) => item.label.trim().length === 0);

        const clippedText = svgs.flatMap((svg, svgIndex) => {
          const svgRect = svg.getBoundingClientRect();
          return [...svg.querySelectorAll('text')]
            .map((textNode) => {
              const textRect = textNode.getBoundingClientRect();
              const text = textNode.textContent.trim();
              return { svgIndex, text, svgRect, textRect };
            })
            .filter(({ text, svgRect, textRect }) => {
              if (!text) return false;
              const isPriceAxis = /^\d+(?:\.\d+)?$/.test(text) && textRect.left > svgRect.right - svgRect.width * 0.12;
              if (isPriceAxis) return false;
              return (
                textRect.left < svgRect.left - 2 ||
                textRect.right > svgRect.right + 2 ||
                textRect.top < svgRect.top - 2 ||
                textRect.bottom > svgRect.bottom + 2
              );
            })
            .map(({ svgIndex, text }) => ({ svgIndex, text }));
        });

        return {
          svgCount: svgs.length,
          visibleAnswerLabels,
          invisibleSvgs,
          missingLabels,
          clippedText,
        };
      });

      expect(audit.visibleAnswerLabels, 'quiz answers must stay hidden until correction').toEqual([]);
      expect(audit.invisibleSvgs, 'SVGs should have visible dimensions').toEqual([]);
      expect(audit.missingLabels, 'SVGs should describe what they illustrate').toEqual([]);
      expect(audit.clippedText, 'SVG text should stay inside its chart').toEqual([]);

      if (['pages/04-setups-core.html', 'pages/08-quiz.html', 'pages/41-no-trade.html'].includes(fileName)) {
        mkdirSync(path.join(__dirname, '..', 'test-results', 'visual-smoke'), { recursive: true });
        const safeProject = testInfo.project.name.replace(/[^a-z0-9_-]/gi, '-');
        const safeFileName = fileName.replace(/[^a-z0-9_-]/gi, '-');
        await page.screenshot({
          path: path.join(__dirname, '..', 'test-results', 'visual-smoke', `${safeProject}-${safeFileName}.png`),
          fullPage: false,
        });
      }
    });
  }
});
