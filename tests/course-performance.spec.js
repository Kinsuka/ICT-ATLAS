const { test, expect } = require('@playwright/test');
const { readFileSync } = require('node:fs');
const path = require('node:path');
const { pathToFileURL } = require('node:url');

const root = path.resolve(__dirname, '..');
const budgets = JSON.parse(readFileSync(path.join(root, 'data/performance-budgets.json'), 'utf8'));
const representativePages = [
  'index.html',
  'pages/05-variantes.html',
  'pages/replay-cases.html',
  'pages/20-workflow-session.html',
  'pages/programme-validation-20-sessions.html',
];

function fileUrl(fileName) {
  return pathToFileURL(path.join(root, fileName)).href;
}

for (const fileName of representativePages) {
  test(`${fileName} reste dans les budgets DOM et chargement`, async ({ page }) => {
    const errors = [];
    page.on('pageerror', (error) => errors.push(error.message));
    await page.goto(fileUrl(fileName), { waitUntil: 'load' });

    if (await page.locator('script[src$="glossary-panel.js"]').count()) {
      await expect(page.locator('html')).toHaveAttribute('data-visuals-ready', 'true');
    }

    const audit = await page.evaluate(() => ({
      domNodes: document.querySelectorAll('*').length,
      svgs: document.querySelectorAll('svg').length,
      stylesheets: [...document.styleSheets].filter((sheet) => sheet.href).length,
      scriptSources: [...document.scripts].map((script) => script.src).filter(Boolean),
      blockingScripts: [...document.scripts]
        .filter((script) => script.src && !script.defer && !script.async && script.type !== 'module')
        .map((script) => script.src),
      glossaryDataLoaded: Boolean(document.querySelector('script[src$="glossary-data.js"]')),
    }));

    expect(audit.domNodes).toBeLessThanOrEqual(budgets.domNodesPerPage);
    expect(audit.svgs).toBeLessThanOrEqual(budgets.svgElementsPerPage);
    expect(audit.stylesheets).toBe(1);
    expect(new Set(audit.scriptSources).size).toBe(audit.scriptSources.length);
    expect(audit.blockingScripts).toEqual([]);
    expect(audit.glossaryDataLoaded, 'les définitions restent hors du chargement initial').toBe(false);
    expect(errors).toEqual([]);
  });
}

test('les données du glossaire sont chargées une seule fois et à la demande', async ({ page }) => {
  await page.goto(fileUrl('index.html'), { waitUntil: 'load' });
  await expect(page.locator('[data-glossary-item]')).toHaveCount(0);
  await expect(page.locator('script[src$="glossary-data.js"]')).toHaveCount(0);

  await page.locator('[data-glossary-open]').first().click();
  await expect(page.locator('[data-glossary-item]')).toHaveCount(26);
  await expect(page.locator('script[src$="glossary-data.js"]')).toHaveCount(1);
  await page.keyboard.press('Escape');

  await page.locator('[data-glossary-open]').last().click();
  await expect(page.locator('[data-glossary-item]')).toHaveCount(26);
  await expect(page.locator('script[src$="glossary-data.js"]')).toHaveCount(1);
});
