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
  'pages/16-modele-mental.html',
  'pages/17-concept-setup-plan.html',
  'pages/19-preuve-statistique.html',
  'pages/20-workflow-session.html',
  'pages/21-liquidite-deplacement.html',
  'pages/22-structure-trend-range.html',
  'pages/25-top-down-multi-timeframe.html',
  'pages/26-psychologie-trader.html',
  'pages/27-fondations-liquidite.html',
  'pages/28-fondations-entree.html',
  'pages/29-fondations-stop-tp.html',
  'pages/30-replay-lab.html',
  'pages/replay-cases.html',
  'pages/examen-decision-session.html',
  'pages/programme-validation-20-sessions.html',
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
          horizontalOverflow: Math.max(
            0,
            document.documentElement.scrollWidth - document.documentElement.clientWidth,
          ),
          visibleAnswerLabels,
          invisibleSvgs,
          missingLabels,
          clippedText,
        };
      });

      expect(audit.visibleAnswerLabels, 'quiz answers must stay hidden until correction').toEqual([]);
      expect(audit.horizontalOverflow, 'page should not overflow horizontally').toBeLessThanOrEqual(2);
      expect(audit.invisibleSvgs, 'SVGs should have visible dimensions').toEqual([]);
      expect(audit.missingLabels, 'SVGs should describe what they illustrate').toEqual([]);
      expect(audit.clippedText, 'SVG text should stay inside its chart').toEqual([]);

      if (fileName === 'pages/replay-cases.html') {
        await expect(page.locator('.guided-case')).toHaveCount(6);
        const firstCorrection = page.locator('#cas-guide-01 .case-reveal');
        await expect(firstCorrection).not.toHaveAttribute('open', '');
        await firstCorrection.locator('summary').click();
        await expect(firstCorrection).toHaveAttribute('open', '');
        await expect(firstCorrection.locator('.case-correction')).toBeVisible();

        await expect(page.locator('[data-session-simulator]')).toHaveCount(4);
        const simulatorConfigs = [
          { id: '#simulateur-session', stages: 7 },
          { id: '#simulateur-session-02', stages: 5 },
          { id: '#simulateur-session-03', stages: 5 },
          { id: '#simulateur-session-04', stages: 5 },
        ];

        for (const config of simulatorConfigs) {
          const simulator = page.locator(config.id);
          await expect(simulator.locator('[data-sim-stage]')).toHaveCount(config.stages);
          await expect(simulator.locator('[data-sim-stage="1"]')).toBeVisible();
          await expect(simulator.locator('[data-sim-stage="2"]')).toBeHidden();

          for (let stage = 1; stage <= config.stages; stage += 1) {
            const stagePanel = simulator.locator(`[data-sim-stage="${stage}"]`);
            await expect(stagePanel).toBeVisible();
            await stagePanel.locator('input[data-correct="true"]').check();
            await stagePanel.locator('[data-sim-validate]').click();
          }

          await expect(simulator.locator('[data-sim-complete]')).toBeVisible();
          await expect(simulator.locator('[role="progressbar"]')).toHaveAttribute('aria-valuenow', String(config.stages));
        }
      }

      if (fileName === 'pages/29-fondations-stop-tp.html') {
        await expect(page.locator('.stop-tp-drill')).toHaveCount(8);
        const firstAnswer = page.locator('#stop-tp-drill-01 .lab-answer');
        await expect(firstAnswer).not.toHaveAttribute('open', '');
        await firstAnswer.locator('summary').click();
        await expect(firstAnswer).toHaveAttribute('open', '');
        await expect(firstAnswer.locator('div').first()).toBeVisible();
      }

      if (fileName === 'pages/examen-decision-session.html') {
        const questions = page.locator('[data-exam-question]');
        await expect(questions).toHaveCount(12);
        await expect(page.locator('[data-exam-results]')).toBeHidden();
        await expect(page.locator('[data-exam-submit]')).toBeDisabled();

        for (let question = 0; question < 12; question += 1) {
          await questions.nth(question).locator('input[data-correct="true"]').check();
        }

        await expect(page.locator('[data-exam-submit]')).toBeEnabled();
        await page.locator('[data-exam-submit]').click();
        await expect(page.locator('[data-exam-results]')).toBeVisible();
        await expect(page.locator('[data-exam-score]')).toHaveText('12 / 12');
        await expect(page.locator('.exam-diagnostic')).toHaveCount(6);
        await expect(page.locator('.exam-question.is-correct')).toHaveCount(12);
      }

      if (fileName === 'pages/programme-validation-20-sessions.html') {
        await expect(page.locator('.validation-session')).toHaveCount(20);
        await expect(page.locator('[data-validation-completed]')).toHaveText('0');

        const firstSession = page.locator('[data-session-index="0"]');
        for (let gate = 0; gate < 5; gate += 1) {
          await firstSession.locator(`[data-gate-index="${gate}"]`).check();
        }
        await firstSession.locator('[data-validation-finalize="0"]').click();
        await expect(page.locator('[data-session-index="0"]')).toHaveClass(/is-passed/);
        await expect(page.locator('[data-validation-completed]')).toHaveText('1');
        await expect(page.locator('[data-validation-passed]')).toHaveText('1');

        await page.reload();
        await expect(page.locator('[data-validation-completed]')).toHaveText('1');
        await expect(page.locator('[data-session-index="0"]')).toHaveClass(/is-passed/);

        const secondSession = page.locator('[data-session-index="1"]');
        await secondSession.locator('summary').click();
        for (const gate of [0, 1, 3, 4]) {
          await secondSession.locator(`[data-gate-index="${gate}"]`).check();
        }
        await secondSession.locator('[data-validation-finalize="1"]').click();
        await expect(page.locator('[data-session-index="1"]')).toHaveClass(/is-failed/);
        await expect(page.locator('[data-validation-completed]')).toHaveText('2');
        await expect(page.locator('[data-validation-passed]')).toHaveText('1');
      }

      if (['pages/04-setups-core.html', 'pages/08-quiz.html', 'pages/20-workflow-session.html', 'pages/29-fondations-stop-tp.html', 'pages/replay-cases.html', 'pages/examen-decision-session.html', 'pages/programme-validation-20-sessions.html', 'pages/41-no-trade.html'].includes(fileName)) {
        mkdirSync(path.join(__dirname, '..', 'test-results', 'visual-smoke'), { recursive: true });
        const safeProject = testInfo.project.name.replace(/[^a-z0-9_-]/gi, '-');
        const safeFileName = fileName.replace(/[^a-z0-9_-]/gi, '-');
        if (fileName === 'pages/programme-validation-20-sessions.html') {
          await page.evaluate(() => window.scrollTo(0, 0));
          await page.locator('.page').evaluate((element) => element.scrollTo(0, 0));
        }
        await page.screenshot({
          path: path.join(__dirname, '..', 'test-results', 'visual-smoke', `${safeProject}-${safeFileName}.png`),
          fullPage: false,
        });

        if (fileName === 'pages/20-workflow-session.html') {
          await page.locator('#protocole-operationnel').screenshot({
            path: path.join(__dirname, '..', 'test-results', 'visual-smoke', `${safeProject}-${safeFileName}-cockpit.png`),
          });
        }

        if (fileName === 'pages/replay-cases.html') {
          await page.locator('#cas-guide-01').screenshot({
            path: path.join(__dirname, '..', 'test-results', 'visual-smoke', `${safeProject}-${safeFileName}-guide-01.png`),
          });
          await page.locator('#simulateur-session .sim-market-panel').screenshot({
            path: path.join(__dirname, '..', 'test-results', 'visual-smoke', `${safeProject}-${safeFileName}-simulator-complete.png`),
          });
          for (const variant of ['02', '03', '04']) {
            await page.locator(`#simulateur-session-${variant} .sim-market-panel`).screenshot({
              path: path.join(__dirname, '..', 'test-results', 'visual-smoke', `${safeProject}-${safeFileName}-simulator-${variant}-complete.png`),
            });
          }
          await page.locator('#simulateur-session [data-sim-reset]').click();
          await expect(page.locator('#simulateur-session [data-sim-stage="1"]')).toBeVisible();
          await expect(page.locator('#simulateur-session [data-sim-stage="2"]')).toBeHidden();
          await expect(page.locator('#simulateur-session [role="progressbar"]')).toHaveAttribute('aria-valuenow', '1');

          const firstStage = page.locator('#simulateur-session [data-sim-stage="1"]');
          await firstStage.locator('input[value="bullish"]').check();
          await firstStage.locator('[data-sim-validate]').click();
          await expect(firstStage).toHaveClass(/is-wrong/);
          await expect(firstStage.locator('.sim-options label.is-answer')).toHaveCount(1);
        }

        if (fileName === 'pages/29-fondations-stop-tp.html') {
          await page.locator('#stop-tp-drill-01').screenshot({
            path: path.join(__dirname, '..', 'test-results', 'visual-smoke', `${safeProject}-${safeFileName}-drill-01.png`),
          });
        }

        if (fileName === 'pages/examen-decision-session.html') {
          await page.locator('[data-exam-results]').screenshot({
            path: path.join(__dirname, '..', 'test-results', 'visual-smoke', `${safeProject}-${safeFileName}-results.png`),
          });
          await page.locator('[data-exam-reset]').click();
          await expect(page.locator('[data-exam-results]')).toBeHidden();
          await expect(page.locator('[data-exam-answered]')).toHaveText('0');
          await expect(page.locator('[data-exam-submit]')).toBeDisabled();
          await expect(page.locator('[data-exam-best]')).toHaveText('12 / 12');

          const examQuestions = page.locator('[data-exam-question]');
          for (let question = 0; question < 12; question += 1) {
            await examQuestions.nth(question).locator('input:not([data-correct])').first().check();
          }
          await page.locator('[data-exam-submit]').click();
          await expect(page.locator('[data-exam-score]')).toHaveText('0 / 12');
          await expect(page.locator('.exam-diagnostic.is-critical')).toHaveCount(6);
          await expect(page.locator('[data-exam-band-code]')).toHaveText('RECONSTRUCTION');
          await expect(page.locator('[data-exam-best-result]')).toHaveText('12 / 12');
        }

        if (fileName === 'pages/programme-validation-20-sessions.html') {
          await page.locator('.validation-dashboard').screenshot({
            path: path.join(__dirname, '..', 'test-results', 'visual-smoke', `${safeProject}-${safeFileName}-dashboard.png`),
          });
          await page.locator('[data-session-index="1"]').screenshot({
            path: path.join(__dirname, '..', 'test-results', 'visual-smoke', `${safeProject}-${safeFileName}-critical-failure.png`),
          });

          const resetButton = page.locator('[data-validation-reset]');
          await resetButton.click();
          await expect(resetButton).toHaveAttribute('data-armed', 'true');
          await resetButton.click();
          await expect(page.locator('[data-validation-completed]')).toHaveText('0');
          await page.reload();
          await expect(page.locator('[data-validation-completed]')).toHaveText('0');
        }
      }
    });
  }
});
