const { test, expect } = require('@playwright/test');
const { readFileSync, readdirSync } = require('node:fs');
const path = require('node:path');
const { pathToFileURL } = require('node:url');

const root = path.resolve(__dirname, '..');
const pages = [
  'index.html',
  ...readdirSync(path.join(root, 'pages'))
    .filter((name) => name.endsWith('.html'))
    .filter((name) => name !== '02-vocabulaire.html')
    .sort()
    .map((name) => `pages/${name}`),
];

function fileUrl(fileName) {
  return pathToFileURL(path.join(root, fileName)).href;
}

async function inspectAccessibility(page) {
  return page.evaluate(() => {
    const visible = (element) => {
      const style = getComputedStyle(element);
      return style.display !== 'none'
        && style.visibility !== 'hidden'
        && element.getClientRects().length > 0;
    };
    const referencedText = (ids) => ids
      .split(/\s+/)
      .map((id) => document.getElementById(id)?.textContent?.trim() || '')
      .join(' ')
      .trim();
    const accessibleName = (element) => {
      if (element.getAttribute('aria-label')?.trim()) return element.getAttribute('aria-label').trim();
      if (element.getAttribute('aria-labelledby')) {
        const name = referencedText(element.getAttribute('aria-labelledby'));
        if (name) return name;
      }
      if (element.id) {
        const label = [...document.querySelectorAll('label[for]')]
          .find((candidate) => candidate.htmlFor === element.id);
        if (label?.textContent?.trim()) return label.textContent.trim();
      }
      const wrappingLabel = element.closest('label');
      if (wrappingLabel?.textContent?.trim()) return wrappingLabel.textContent.trim();
      if (element.getAttribute('alt')?.trim()) return element.getAttribute('alt').trim();
      if (element.getAttribute('title')?.trim()) return element.getAttribute('title').trim();
      if (element.getAttribute('value')?.trim() && ['button', 'submit', 'reset'].includes(element.type)) {
        return element.getAttribute('value').trim();
      }
      return element.textContent?.trim() || '';
    };
    const selectorFor = (element) => {
      if (element.id) return `#${element.id}`;
      const classes = [...element.classList].slice(0, 2).join('.');
      return `${element.tagName.toLowerCase()}${classes ? `.${classes}` : ''}`;
    };

    const ids = [...document.querySelectorAll('[id]')].map((element) => element.id);
    const duplicateIds = [...new Set(ids.filter((id, index) => ids.indexOf(id) !== index))];
    const brokenAriaReferences = [];
    document.querySelectorAll('[aria-labelledby], [aria-describedby], [aria-controls]').forEach((element) => {
      ['aria-labelledby', 'aria-describedby', 'aria-controls'].forEach((attribute) => {
        const value = element.getAttribute(attribute);
        if (!value) return;
        value.split(/\s+/).forEach((id) => {
          if (id && !document.getElementById(id)) {
            brokenAriaReferences.push(`${selectorFor(element)}[${attribute}="${id}"]`);
          }
        });
      });
    });

    const interactive = [...document.querySelectorAll([
      'button',
      'input:not([type="hidden"])',
      'select',
      'textarea',
      'summary',
      '[role="button"]',
      '[role="link"]',
    ].join(','))].filter(visible);
    const unnamedControls = interactive
      .filter((element) => !accessibleName(element))
      .map(selectorFor);
    const undersizedTargets = interactive
      .map((element) => {
        let target = element;
        if (element.matches('input[type="checkbox"], input[type="radio"]')) {
          target = element.closest('label')
            || (element.id ? [...document.querySelectorAll('label[for]')]
              .find((label) => label.htmlFor === element.id) : null)
            || element;
        }
        const rect = target.getBoundingClientRect();
        return rect.width + 0.01 < 24 || rect.height + 0.01 < 24
          ? `${selectorFor(element)} (${rect.width.toFixed(1)}×${rect.height.toFixed(1)})`
          : null;
      })
      .filter(Boolean);
    const formButtonsWithoutType = [...document.querySelectorAll('form button:not([type])')]
      .map(selectorFor);
    const positiveTabindex = [...document.querySelectorAll('[tabindex]')]
      .filter((element) => Number(element.getAttribute('tabindex')) > 0)
      .map(selectorFor);
    const unnamedGraphics = [...document.querySelectorAll('svg:not([aria-hidden="true"])')]
      .filter(visible)
      .filter((svg) => !accessibleName(svg) && !svg.querySelector('title'))
      .map(selectorFor);

    const skipLink = document.querySelector('.skip-link');
    const main = document.querySelector('main');
    const viewport = document.querySelector('meta[name="viewport"]')?.content?.toLowerCase() || '';
    const glossaryShell = document.querySelector('.glossary-panel-shell');
    const glossaryDialog = glossaryShell?.querySelector('[role="dialog"]');
    const glossaryOpeners = [...document.querySelectorAll('[data-glossary-open]')];

    return {
      lang: document.documentElement.lang,
      mainCount: document.querySelectorAll('main').length,
      h1Count: document.querySelectorAll('h1').length,
      mainId: main?.id || '',
      skipCount: document.querySelectorAll('.skip-link').length,
      skipTarget: skipLink?.hash || '',
      duplicateIds,
      brokenAriaReferences,
      unnamedControls,
      undersizedTargets,
      formButtonsWithoutType,
      positiveTabindex,
      unnamedGraphics,
      zoomDisabled: /user-scalable\s*=\s*no|maximum-scale\s*=\s*1(?:\.0)?(?:,|$)/.test(viewport),
      glossary: glossaryShell ? {
        hidden: glossaryShell.getAttribute('aria-hidden'),
        dialogRole: glossaryDialog?.getAttribute('role') || '',
        modal: glossaryDialog?.getAttribute('aria-modal') || '',
        labelledBy: glossaryDialog?.getAttribute('aria-labelledby') || '',
        openerCount: glossaryOpeners.length,
        openersReady: glossaryOpeners.every((opener) => (
          opener.getAttribute('aria-controls') === glossaryShell.id
          && opener.getAttribute('aria-expanded') === 'false'
        )),
      } : null,
    };
  });
}

for (const fileName of pages) {
  test(`${fileName} respecte le socle d’accessibilité`, async ({ page }) => {
    await page.goto(fileUrl(fileName), { waitUntil: 'load' });
    const audit = await inspectAccessibility(page);

    expect(audit.lang, 'la langue du document').toBe('fr');
    expect(audit.mainCount, 'un seul contenu principal').toBe(1);
    expect(audit.h1Count, 'un seul titre de niveau 1').toBe(1);
    expect(audit.mainId, 'la cible du lien d’évitement').toBe('contenu');
    expect(audit.skipCount, 'un seul lien d’évitement').toBe(1);
    expect(audit.skipTarget, 'le lien d’évitement pointe vers main').toBe('#contenu');
    expect(audit.duplicateIds, 'identifiants dupliqués').toEqual([]);
    expect(audit.brokenAriaReferences, 'références ARIA cassées').toEqual([]);
    expect(audit.unnamedControls, 'contrôles sans nom accessible').toEqual([]);
    expect(audit.undersizedTargets, 'cibles interactives inférieures à 24 × 24 px').toEqual([]);
    expect(audit.formButtonsWithoutType, 'boutons de formulaire sans type').toEqual([]);
    expect(audit.positiveTabindex, 'tabindex positifs').toEqual([]);
    expect(audit.unnamedGraphics, 'SVG visibles sans nom accessible').toEqual([]);
    expect(audit.zoomDisabled, 'le zoom utilisateur reste disponible').toBe(false);

    if (audit.glossary) {
      expect(audit.glossary.hidden, 'le glossaire est masqué au chargement').toBe('true');
      expect(audit.glossary.dialogRole).toBe('dialog');
      expect(audit.glossary.modal).toBe('true');
      expect(audit.glossary.labelledBy).toBeTruthy();
      expect(audit.glossary.openerCount).toBeGreaterThan(0);
      expect(audit.glossary.openersReady, 'état ARIA des boutons du glossaire').toBe(true);
    }
  });
}

test('la redirection historique 02 conserve un fallback accessible', () => {
  const source = readFileSync(path.join(root, 'pages/02-vocabulaire.html'), 'utf8');
  expect(source).toMatch(/<html lang="fr">/);
  expect(source).toMatch(/<a class="skip-link" href="#contenu">/);
  expect(source).toMatch(/<main class="page" id="contenu" tabindex="-1"/);
  expect(source).toMatch(/<h1>Glossaire déplacé<\/h1>/);
  expect(source).not.toMatch(/user-scalable\s*=\s*no|maximum-scale\s*=\s*1(?:\.0)?(?:,|$)/i);
});

test('le parcours clavier et la modale du glossaire restent maîtrisés', async ({ page }) => {
  await page.goto(fileUrl('index.html'), { waitUntil: 'load' });

  await page.keyboard.press('Tab');
  const skipLink = page.locator('.skip-link');
  await expect(skipLink).toBeFocused();
  await expect(skipLink).toBeVisible();
  await page.keyboard.press('Enter');
  await expect(page.locator('main')).toBeFocused();

  const opener = page.locator('[data-glossary-open]').first();
  await opener.focus();
  await page.keyboard.press('Enter');

  const shell = page.locator('.glossary-panel-shell');
  const panel = page.locator('.glossary-panel');
  const search = page.locator('[data-glossary-search]');
  await expect(shell).toHaveClass(/is-open/);
  await expect(shell).toHaveAttribute('aria-hidden', 'false');
  await expect(opener).toHaveAttribute('aria-expanded', 'true');
  await expect(page.locator('.app-shell')).toHaveAttribute('inert', '');
  await expect(search).toBeFocused();
  await expect(panel.locator('[data-glossary-item]')).toHaveCount(26);
  await search.fill('FVG');
  await expect(panel.getByRole('heading', { name: 'FVG', exact: true })).toBeVisible();
  await expect(panel.getByRole('heading', { name: 'No Trade', exact: true })).toBeHidden();
  await search.fill('');

  const last = panel.locator('.glossary-full-link');
  await last.focus();
  await page.keyboard.press('Tab');
  await expect(panel.locator('.glossary-close')).toBeFocused();
  await page.keyboard.press('Shift+Tab');
  await expect(last).toBeFocused();

  await page.keyboard.press('Escape');
  await expect(shell).not.toHaveClass(/is-open/);
  await expect(shell).toHaveAttribute('aria-hidden', 'true');
  await expect(opener).toHaveAttribute('aria-expanded', 'false');
  await expect(page.locator('.app-shell')).not.toHaveAttribute('inert', '');
  await expect(opener).toBeFocused();
});

test('les couleurs de texte sémantiques gardent un contraste AA', async ({ page }) => {
  await page.goto(fileUrl('index.html'), { waitUntil: 'load' });
  const ratios = await page.evaluate(() => {
    const style = getComputedStyle(document.documentElement);
    const parse = (value) => {
      const hex = value.trim().replace('#', '');
      if (hex.length !== 6) throw new Error(`Couleur non prise en charge: ${value}`);
      return [0, 2, 4].map((offset) => Number.parseInt(hex.slice(offset, offset + 2), 16));
    };
    const luminance = (value) => {
      const [red, green, blue] = parse(value).map((channel) => {
        const normalized = channel / 255;
        return normalized <= 0.04045
          ? normalized / 12.92
          : ((normalized + 0.055) / 1.055) ** 2.4;
      });
      return 0.2126 * red + 0.7152 * green + 0.0722 * blue;
    };
    const contrast = (foreground, background) => {
      const high = Math.max(luminance(foreground), luminance(background));
      const low = Math.min(luminance(foreground), luminance(background));
      return (high + 0.05) / (low + 0.05);
    };
    const background = style.getPropertyValue('--course-bg');
    return Object.fromEntries(['--course-ink', '--course-muted', '--course-faint', '--course-accent', '--course-accent-2']
      .map((token) => [token, contrast(style.getPropertyValue(token), background)]));
  });

  Object.entries(ratios).forEach(([token, ratio]) => {
    expect(ratio, `${token}: ${ratio.toFixed(2)}:1`).toBeGreaterThanOrEqual(4.5);
  });
});
