const { test, expect } = require('@playwright/test');
const path = require('node:path');
const { pathToFileURL } = require('node:url');
const courseParts = require('../data/course-navigation.json');

const root = path.resolve(__dirname, '..');
const lessons = courseParts.flatMap((part) => part.lessons.map(([file, title]) => ({ file, title })));
const urlFor = (relativePath) => pathToFileURL(path.join(root, relativePath)).href;
const publicPath = (file) => file === 'index.html' ? file : `pages/${file}`;

async function open(page, relativePath) {
  await page.goto(urlFor(relativePath));
  await expect(page.locator('h1').first()).toBeVisible();
}

test.describe('V103 · parcours utilisateur complet', () => {
  test.beforeEach(async ({ page }) => {
    await open(page, 'index.html');
    await page.evaluate(() => localStorage.clear());
  });

  test('les 41 leçons forment un parcours continu vers la pratique', async ({ page }) => {
    test.setTimeout(120_000);

    for (let index = 0; index < lessons.length; index += 1) {
      const lesson = lessons[index];
      await expect(page).toHaveURL(urlFor(publicPath(lesson.file)));
      await expect(page.locator('.lesson-meta')).toContainText(`Leçon ${String(index + 1).padStart(2, '0')}/41`);

      const next = page.locator('.lesson-bottom-nav .next');
      await expect(next).toHaveCount(1);
      if (index < lessons.length - 1) {
        await next.click();
      }
    }

    await expect(page.locator('.course-completion-gateway')).toContainText('COURS TERMINÉ · 41 / 41');
    await expect(page.locator('[data-course-completion-next]')).toHaveAttribute('href', 'tableau-progression.html');
    await page.locator('[data-course-completion-next]').click();
    await expect(page).toHaveURL(urlFor('pages/tableau-progression.html'));
    await expect(page.locator('h1')).toContainText('Que travailler maintenant ?');
  });

  test('l’accueil recommande chaque preuve dans l’ordre et avec les bons seuils', async ({ page }) => {
    const next = page.locator('[data-roadmap-next-link]');
    await expect(next).toHaveAttribute('href', 'pages/16-modele-mental.html');

    await page.evaluate(() => {
      const records = Array.from(
        { length: 20 },
        (_, index) => ({ checks: index === 0 ? [true, true, true, true, true] : [false, false, false, false, false], finalized: index === 0 }),
      );
      localStorage.setItem('ict-atlas-validation-20-sessions-v1', JSON.stringify(records));
    });
    await page.reload();
    await expect(next).toHaveAttribute('href', 'pages/examen-decision-session.html');
    await page.evaluate(() => localStorage.clear());
    await page.reload();

    await page.evaluate(() => localStorage.setItem('ict-atlas-session-exam-best-v1', '8'));
    await page.reload();
    await expect(next).toHaveAttribute('href', 'pages/examen-decision-session.html');

    await page.evaluate(() => localStorage.setItem('ict-atlas-session-exam-best-v1', '10'));
    await page.reload();
    await expect(page.locator('[data-roadmap-exam-status]')).toHaveText('SEUIL VALIDÉ');
    await expect(next).toHaveAttribute('href', 'pages/examen-dol-tp.html');

    await page.evaluate(() => localStorage.setItem('ict-atlas-target-exam-best-v1', '16'));
    await page.reload();
    await expect(page.locator('[data-roadmap-target-status]')).toHaveText('SEUIL VALIDÉ');
    await expect(next).toHaveAttribute('href', 'pages/replay-historique.html');

    await page.evaluate(() => localStorage.setItem('ict-atlas-historical-replay-v1', JSON.stringify({ scores: { 'hist-01': 3, 'hist-02': 3, 'hist-03': 3, 'hist-04': 3 }, best: 12 })));
    await page.reload();
    await expect(page.locator('[data-roadmap-historical-status]')).toHaveText('SEUIL VALIDÉ');
    await expect(next).toHaveAttribute('href', 'pages/programme-validation-20-sessions.html');

    await page.evaluate(() => {
      const records = Array.from(
        { length: 20 },
        () => ({ checks: [true, true, true, true, true], finalized: true }),
      );
      localStorage.setItem('ict-atlas-validation-20-sessions-v1', JSON.stringify(records));
    });
    await page.reload();
    await expect(page.locator('[data-roadmap-validation-status]')).toHaveText('VALIDÉ · 20 / 20');
    await expect(next).toHaveAttribute('href', 'pages/19-preuve-statistique.html');
  });

  test('la route pratique ne boucle pas et revient au tableau après les 20 sessions', async ({ page }) => {
    const transitions = [
      ['pages/replay-cases.html', 'examen-decision-session.html'],
      ['pages/examen-decision-session.html', 'examen-dol-tp.html'],
      ['pages/examen-dol-tp.html', 'replay-historique.html'],
      ['pages/replay-historique.html', 'programme-validation-20-sessions.html'],
      ['pages/programme-validation-20-sessions.html', 'tableau-progression.html'],
    ];

    for (const [relativePath, expectedHref] of transitions) {
      await open(page, relativePath);
      await expect(page.locator('aside.site-nav .course-lessons > li')).toHaveCount(6);
      await expect(page.locator('aside.site-nav .course-lesson.active')).toHaveCount(1);
      await expect(page.locator('.lesson-bottom-nav .next')).toHaveAttribute('href', expectedHref);
    }

    await expect(page.locator('.validation-session')).toHaveCount(20);
    await expect(page.locator('[data-validation-completed]')).toHaveText('0');
  });
});
