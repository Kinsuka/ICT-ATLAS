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
  'pages/01-parcours.html',
  'pages/03-fondations.html',
  'pages/04-setups-core.html',
  'pages/05-variantes.html',
  'pages/06-contextes-avances.html',
  'pages/07-failures-journees.html',
  'pages/08-quiz.html',
  'pages/09-synthese.html',
  'pages/10-programme-avance.html',
  'pages/11-mecanique-marches.html',
  'pages/12-gestion-risque.html',
  'pages/13-prop-firm.html',
  'pages/14-live-chart.html',
  'pages/15-index-concepts.html',
  'pages/16-modele-mental.html',
  'pages/17-concept-setup-plan.html',
  'pages/18-transition-reel.html',
  'pages/19-preuve-statistique.html',
  'pages/20-workflow-session.html',
  'pages/21-liquidite-deplacement.html',
  'pages/22-structure-trend-range.html',
  'pages/23-langage-ict-contexte.html',
  'pages/24-premium-discount-killzones.html',
  'pages/25-top-down-multi-timeframe.html',
  'pages/26-psychologie-trader.html',
  'pages/27-fondations-liquidite.html',
  'pages/28-fondations-entree.html',
  'pages/29-fondations-stop-tp.html',
  'pages/30-replay-lab.html',
  'pages/replay-cases.html',
  'pages/replay-historique.html',
  'pages/examen-decision-session.html',
  'pages/examen-dol-tp.html',
  'pages/tableau-progression.html',
  'pages/programme-validation-20-sessions.html',
  'pages/31-order-blocks.html',
  'pages/32-fvg-imbalance-ce.html',
  'pages/33-mss-changement-controle.html',
  'pages/34-breaker-mitigation.html',
  'pages/35-pd-arrays-hierarchie.html',
  'pages/36-ote-dealing-range.html',
  'pages/37-dol-targets-hierarchie.html',
  'pages/38-smt-divergence.html',
  'pages/39-profils-journee-sessions.html',
  'pages/40-displacement-operationnel.html',
  'pages/41-no-trade.html',
  'pages/glossaire.html',
];

const previouslyMissingVisualPages = [
  'pages/01-parcours.html',
  'pages/03-fondations.html',
  'pages/05-variantes.html',
  'pages/06-contextes-avances.html',
  'pages/07-failures-journees.html',
  'pages/09-synthese.html',
  'pages/10-programme-avance.html',
  'pages/12-gestion-risque.html',
  'pages/13-prop-firm.html',
  'pages/15-index-concepts.html',
  'pages/18-transition-reel.html',
  'pages/23-langage-ict-contexte.html',
  'pages/24-premium-discount-killzones.html',
  'pages/34-breaker-mitigation.html',
  'pages/35-pd-arrays-hierarchie.html',
  'pages/36-ote-dealing-range.html',
  'pages/37-dol-targets-hierarchie.html',
  'pages/38-smt-divergence.html',
  'pages/glossaire.html',
];

function fileUrl(fileName) {
  return pathToFileURL(path.join(__dirname, '..', fileName)).href;
}

test.describe('ICT Atlas visual smoke audit', () => {
  test('the visual matrix includes the 19 previously omitted pages', async () => {
    expect(previouslyMissingVisualPages).toHaveLength(19);
    expect(previouslyMissingVisualPages.filter((fileName) => !pages.includes(fileName))).toEqual([]);
  });

  for (const fileName of pages) {
    test(`${fileName} renders SVG charts without obvious visual regressions`, async ({ page }, testInfo) => {
      await page.goto(fileUrl(fileName));
      await expect(page.locator('h1').first()).toBeVisible();
      await page.evaluate(() => new Promise((resolve) => requestAnimationFrame(() => resolve())));

      const audit = await page.evaluate(() => {
        const svgs = [...document.querySelectorAll('svg')];
        const visualContainers = [...document.querySelectorAll([
          '.chart',
          '.exam-chart',
          '.guided-case-chart',
          '.sim-chart-wrap',
          '.historical-chart-scroll',
        ].join(','))].filter((container) => !container.classList.contains('chart--concept'));
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
            .filter((textNode) => textNode.getClientRects().length > 0)
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

        const remainingDecorativeSeries = svgs
          .map((svg, index) => ({
            index,
            signature: svg.querySelector('polyline')?.getAttribute('points') || '',
          }))
          .filter((item) => item.signature === '120,270 190,210 260,232 330,150 405,182 480,108 560,132 640,82 760,104');

        const inaccessibleConceptVisuals = [...document.querySelectorAll('.concept-visual')]
          .map((visual, index) => ({
            index,
            role: visual.getAttribute('role') || '',
            label: visual.getAttribute('aria-label') || '',
          }))
          .filter((visual) => visual.role !== 'img' || !visual.label.trim());

        const missingScrollAffordances = visualContainers
          .filter((container) => container.scrollWidth > container.clientWidth + 2)
          .filter((container) => !container.querySelector(':scope > .visual-pan-hint'))
          .map((container) => container.className);

        const unreadableDenseText = [...document.querySelectorAll('.chart--dense svg text')]
          .filter((textNode) => textNode.getClientRects().length > 0)
          .map((textNode) => ({
            text: textNode.textContent.trim(),
            height: Math.round(textNode.getBoundingClientRect().height * 10) / 10,
          }))
          .filter((item) => item.text && item.height < 8);

        const responsiveModeErrors = visualContainers
          .filter((container) => container.querySelector('svg, .concept-visual'))
          .map((container) => ({
            className: container.className,
            modes: ['visual-mode-fit', 'visual-mode-scroll']
              .filter((mode) => container.classList.contains(mode)),
          }))
          .filter((item) => item.modes.length !== 1);

        const incompleteSemanticKeys = [...document.querySelectorAll('.chart--dense .visual-line-key')]
          .map((key, index) => ({ index, items: key.querySelectorAll('.visual-line-key-item').length }))
          .filter((item) => item.items !== 5);

        const unclassifiedDashedLines = [...document.querySelectorAll([
          '.visual-mode-scroll svg line[stroke-dasharray]',
          '.visual-mode-fit svg line[stroke-dasharray]',
          '.visual-mode-scroll svg path[stroke-dasharray]',
          '.visual-mode-fit svg path[stroke-dasharray]',
        ].join(','))]
          .filter((line) => ![
            'visual-level-line',
            'visual-projection-line',
            'visual-invalidation-line',
          ].some((className) => line.classList.contains(className)))
          .map((line) => line.outerHTML.slice(0, 160));

        const unreadableVisualText = [...document.querySelectorAll([
          '.visual-mode-scroll svg text',
          '.visual-mode-fit svg text',
        ].join(','))]
          .filter((textNode) => textNode.getClientRects().length > 0)
          .map((textNode) => ({
            text: textNode.textContent.trim(),
            height: Math.round(textNode.getBoundingClientRect().height * 10) / 10,
          }))
          .filter((item) => item.text && item.height < 8);

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
          remainingDecorativeSeries,
          inaccessibleConceptVisuals,
          missingScrollAffordances,
          unreadableDenseText,
          responsiveModeErrors,
          incompleteSemanticKeys,
          unclassifiedDashedLines,
          unreadableVisualText,
        };
      });

      expect(audit.visibleAnswerLabels, 'quiz answers must stay hidden until correction').toEqual([]);
      expect(audit.horizontalOverflow, 'page should not overflow horizontally').toBeLessThanOrEqual(2);
      expect(audit.invisibleSvgs, 'SVGs should have visible dimensions').toEqual([]);
      expect(audit.missingLabels, 'SVGs should describe what they illustrate').toEqual([]);
      expect(audit.clippedText, 'SVG text should stay inside its chart').toEqual([]);
      expect(audit.remainingDecorativeSeries, 'decorative multi-line charts should use a concept visual').toEqual([]);
      expect(audit.inaccessibleConceptVisuals, 'concept visuals should expose an accessible description').toEqual([]);
      expect(audit.missingScrollAffordances, 'scrollable visuals should explain horizontal navigation').toEqual([]);
      expect(audit.unreadableDenseText, 'dense chart labels should remain readable').toEqual([]);
      expect(audit.responsiveModeErrors, 'each graphic should use exactly one responsive mode').toEqual([]);
      expect(audit.incompleteSemanticKeys, 'dense charts should explain all five graphic roles').toEqual([]);
      expect(audit.unclassifiedDashedLines, 'dashed lines should carry a semantic role').toEqual([]);
      expect(audit.unreadableVisualText, 'all visible chart labels should meet the minimum rendered size').toEqual([]);

      if (fileName === 'index.html') {
        await expect(page.locator('.roadmap-stages > li')).toHaveCount(6);
        const roadmapHrefs = await page.locator('.roadmap-stages > li > a').evaluateAll((links) => links.map((link) => link.getAttribute('href')));
        expect(roadmapHrefs).toEqual([
          'pages/20-workflow-session.html#v92-session-cockpit',
          'pages/replay-cases.html#pack-six-cas',
          'pages/replay-cases.html#simulateur-session',
          'pages/examen-decision-session.html',
          'pages/programme-validation-20-sessions.html',
          'pages/19-preuve-statistique.html',
        ]);
        await expect(page.locator('[data-roadmap-next-link]')).toHaveAttribute('href', 'pages/20-workflow-session.html#v92-session-cockpit');
        await expect(page.locator('[data-roadmap-next-title]')).toHaveText('Remplir le cockpit de session');

        await page.evaluate(() => localStorage.setItem('ict-atlas-session-exam-best-v1', '8'));
        await page.reload();
        await expect(page.locator('[data-roadmap-exam-status]')).toHaveText('MEILLEUR · 8 / 12');
        await expect(page.locator('[data-roadmap-next-link]')).toHaveAttribute('href', 'pages/examen-decision-session.html');

        await page.evaluate(() => localStorage.setItem('ict-atlas-session-exam-mastery-v1', 'true'));
        await page.reload();
        await expect(page.locator('[data-roadmap-exam-status]')).toHaveText('SEUIL VALIDÉ');
        await expect(page.locator('[data-roadmap-next-link]')).toHaveAttribute('href', 'pages/programme-validation-20-sessions.html');

        await page.evaluate(() => {
          const records = Array.from({ length: 20 }, () => ({ checks: [true, true, true, true, true], finalized: true }));
          localStorage.setItem('ict-atlas-validation-20-sessions-v1', JSON.stringify(records));
        });
        await page.reload();
        await expect(page.locator('[data-roadmap-validation-status]')).toHaveText('VALIDÉ · 20 / 20');
        await expect(page.locator('[data-roadmap-forward-status]')).toHaveText('À DÉMARRER');
        await expect(page.locator('[data-roadmap-next-link]')).toHaveAttribute('href', 'pages/19-preuve-statistique.html');
        await page.evaluate(() => localStorage.setItem('ict-atlas-forward-gate-v1', JSON.stringify({ verdict: 'go' })));
        await page.reload();
        await expect(page.locator('[data-roadmap-forward-status]')).toHaveText('GO PÉDAGOGIQUE');
        await expect(page.locator('[data-roadmap-next-title]')).toHaveText('Configurer l’échelle de micro-risque');
        await expect(page.locator('[data-roadmap-next-link]')).toHaveAttribute('href', 'pages/19-preuve-statistique.html#v90-risk-ladder');
      }

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

      if (fileName === 'pages/replay-historique.html') {
        const historicalCases = page.locator('[data-historical-case]');
        await expect(historicalCases).toHaveCount(4);
        await expect(page.locator('[data-historical-completed]')).toHaveText('0 / 4');
        await expect(page.locator('[data-historical-score]')).toHaveText('0 / 16');
        await expect(page.locator('#hist-01 [data-historical-chart]')).toHaveAttribute('data-candles-shown', '14');
        await expect(page.locator('#hist-01 [data-case-status]')).toHaveText('FUTUR MASQUÉ');

        for (let caseIndex = 0; caseIndex < 4; caseIndex += 1) {
          const historicalCase = historicalCases.nth(caseIndex);
          const correctAnswers = historicalCase.locator('input[data-correct="true"]');
          await expect(correctAnswers).toHaveCount(4);
          for (let answerIndex = 0; answerIndex < 4; answerIndex += 1) {
            await correctAnswers.nth(answerIndex).check();
          }
          await expect(historicalCase.locator('[data-case-answered]')).toHaveText('4');
          await expect(historicalCase.locator('[data-case-submit]')).toBeEnabled();
          await historicalCase.locator('[data-case-submit]').click();
          await expect(historicalCase).toHaveClass(/is-reviewed/);
          await expect(historicalCase.locator('[data-case-score]')).toHaveText('4 / 4');
          await expect(historicalCase.locator('[data-case-status]')).toHaveText('FUTUR RÉVÉLÉ');
          await expect(historicalCase.locator('[data-historical-chart]')).toHaveAttribute('data-candles-shown', '33');
        }

        await expect(page.locator('[data-historical-completed]')).toHaveText('4 / 4');
        await expect(page.locator('[data-historical-score]')).toHaveText('16 / 16');
        await expect(page.locator('[data-historical-best]')).toHaveText('16 / 16');
        await page.reload();
        await expect(page.locator('[data-historical-completed]')).toHaveText('4 / 4');
        await expect(page.locator('#hist-01 [data-case-status]')).toHaveText('FUTUR RÉVÉLÉ');
        await expect(page.locator('#hist-01 [data-case-score]')).toHaveText('4 / 4');
      }

      if (fileName === 'pages/20-workflow-session.html') {
        const cockpit = page.locator('[data-session-cockpit]');
        const field = (name) => cockpit.locator(`[data-cockpit-field="${name}"]`);
        await expect(cockpit.locator('[data-cockpit-evidence] article')).toHaveCount(8);
        await expect(cockpit.locator('[data-cockpit-verdict-label]')).toHaveText('À RENSEIGNER');
        await expect(cockpit.locator('[data-cockpit-copy]')).toBeDisabled();
        await expect(cockpit.locator('[data-cockpit-download]')).toBeDisabled();

        await field('asset').fill('NQ');
        await field('session').selectOption({ label: 'NY AM' });
        await field('direction').selectOption('short');
        await field('environment').selectOption('trend');
        await field('location').selectOption('premium');
        await field('bsl').fill('PDH 19 850');
        await field('ssl').fill('PDL 19 600');
        await field('dol').selectOption('ssl');
        await field('dolStatus').selectOption('open');
        await field('obstacle').selectOption('clear');
        await field('poi').fill('Résistance H4 en premium');
        await field('scenario').fill('Si le PDH est sweepé puis réintégré, je cherche un short vers le PDL.');
        await field('narrativeInvalidation').fill('Acceptation au-dessus du swing high H4.');
        await field('eventModel').selectOption({ label: 'Sweep puis réintégration' });
        await field('triggerModel').selectOption({ label: 'Displacement + MSS + retour FVG' });
        await field('entry').fill('19800');
        await field('stop').fill('19820');
        await field('tp1').fill('19780');
        await field('tp2').fill('19740');
        await field('plannedRisk').fill('0.25');
        await field('window').selectOption('inside');
        await field('news').selectOption('clear');
        await field('dailyStop').selectOption('intact');
        await field('tradeLimit').selectOption('intact');
        await field('ruleset').selectOption('same');

        await expect(cockpit.locator('[data-cockpit-verdict-label]')).toHaveText('ATTENDRE');
        await expect(cockpit.locator('[data-cockpit-score]')).toHaveText('6 / 8');
        await expect(cockpit.locator('[data-cockpit-r1]')).toHaveText('1.00R');
        await expect(cockpit.locator('[data-cockpit-r2]')).toHaveText('3.00R');
        await expect(cockpit.locator('.session-evidence article.is-waiting')).toHaveCount(2);

        await field('eventOccurred').check();
        await expect(cockpit.locator('[data-cockpit-verdict-label]')).toHaveText('ATTENDRE');
        await expect(cockpit.locator('[data-cockpit-score]')).toHaveText('7 / 8');
        await field('triggerConfirmed').check();
        await expect(cockpit.locator('[data-cockpit-verdict-label]')).toHaveText('AUTORISÉ');
        await expect(cockpit.locator('[data-cockpit-score]')).toHaveText('8 / 8');
        await expect(cockpit.locator('.session-evidence article.is-passed')).toHaveCount(8);
        await expect(cockpit.locator('[data-cockpit-copy]')).toBeEnabled();
        await expect(cockpit.locator('[data-cockpit-download]')).toBeEnabled();
        await expect(cockpit.locator('[data-cockpit-brief]')).toContainText('Verdict : AUTORISÉ');

        mkdirSync(path.join(__dirname, '..', 'test-results', 'visual-smoke'), { recursive: true });
        const safeProject = testInfo.project.name.replace(/[^a-z0-9_-]/gi, '-');
        await cockpit.locator('.session-planner-head').screenshot({
          path: path.join(__dirname, '..', 'test-results', 'visual-smoke', `${safeProject}-pages-20-workflow-session-html-v92-authorized.png`),
        });

        await page.reload();
        await expect(page.locator('[data-cockpit-verdict-label]')).toHaveText('AUTORISÉ');
        await expect(page.locator('[data-cockpit-field="asset"]')).toHaveValue('NQ');
        await page.locator('[data-cockpit-field="plannedRisk"]').fill('0.50');
        await expect(page.locator('[data-cockpit-verdict-label]')).toHaveText('NO TRADE');
        await expect(page.locator('[data-cockpit-next-action]')).toContainText('risque planifié');
        await page.locator('[data-cockpit-field="plannedRisk"]').fill('0.25');
        await page.locator('[data-cockpit-field="dolStatus"]').selectOption('consumed');
        await expect(page.locator('[data-cockpit-verdict-label]')).toHaveText('NO TRADE');
        await expect(page.locator('[data-cockpit-next-action]')).toContainText('DOL primaire est déjà consommée');
      }

      if (fileName === 'pages/29-fondations-stop-tp.html') {
        await expect(page.locator('.stop-tp-drill')).toHaveCount(8);
        const firstAnswer = page.locator('#stop-tp-drill-01 .lab-answer');
        await expect(firstAnswer).not.toHaveAttribute('open', '');
        await firstAnswer.locator('summary').click();
        await expect(firstAnswer).toHaveAttribute('open', '');
        await expect(firstAnswer.locator('div').first()).toBeVisible();
      }

      if (fileName === 'pages/19-preuve-statistique.html') {
        const gate = page.locator('[data-forward-gate]');
        const ladder = page.locator('[data-risk-ladder]');
        await expect(gate.locator('[data-forward-evidence] article')).toHaveCount(8);
        await expect(gate.locator('[data-forward-verdict-label]')).toHaveText('CORRIGER');
        await expect(ladder.locator('[data-risk-evidence] article')).toHaveCount(9);
        await expect(ladder.locator('[data-risk-verdict-label]')).toHaveText('VERROUILLÉ');

        await gate.locator('[data-forward-field="decisions"]').fill('30');
        await gate.locator('[data-forward-field="trades"]').fill('20');
        await gate.locator('[data-forward-field="netR"]').fill('4');
        await gate.locator('[data-forward-field="drawdown"]').fill('3');
        await gate.locator('[data-forward-field="processErrors"]').fill('2');
        for (const field of ['rulesFrozen', 'independent', 'costsIncluded']) {
          await gate.locator(`[data-forward-field="${field}"]`).check();
        }

        await expect(gate.locator('[data-forward-verdict-label]')).toHaveText('GO PÉDAGOGIQUE');
        await expect(gate.locator('[data-forward-expectancy]')).toHaveText('0.20R');
        await expect(gate.locator('[data-forward-error-rate]')).toHaveText('6.7 %');
        await expect(gate.locator('.forward-evidence article.is-passed')).toHaveCount(8);
        await expect(ladder.locator('[data-risk-verdict-label]')).toHaveText('COLLECTER');

        await ladder.locator('[data-risk-field="trades"]').fill('20');
        await ladder.locator('[data-risk-field="netR"]').fill('3');
        await ladder.locator('[data-risk-field="drawdown"]').fill('2');
        await ladder.locator('[data-risk-field="processErrors"]').fill('0');
        await ladder.locator('[data-risk-field="dailyStopHits"]').fill('0');
        for (const field of ['rulesUnchanged', 'noScaleUp']) {
          await ladder.locator(`[data-risk-field="${field}"]`).check();
        }

        await expect(ladder.locator('[data-risk-verdict-label]')).toHaveText('STABILISER');
        await expect(ladder.locator('[data-risk-score]')).toHaveText('9 / 9');
        await expect(ladder.locator('.risk-evidence article.is-passed')).toHaveCount(9);

        mkdirSync(path.join(__dirname, '..', 'test-results', 'visual-smoke'), { recursive: true });
        const safeProject = testInfo.project.name.replace(/[^a-z0-9_-]/gi, '-');
        await gate.screenshot({
          path: path.join(__dirname, '..', 'test-results', 'visual-smoke', `${safeProject}-pages-19-preuve-statistique-html-forward-go.png`),
        });
        await ladder.screenshot({
          path: path.join(__dirname, '..', 'test-results', 'visual-smoke', `${safeProject}-pages-19-preuve-statistique-html-risk-stabilize.png`),
        });

        await page.reload();
        await expect(page.locator('[data-forward-verdict-label]')).toHaveText('GO PÉDAGOGIQUE');
        await expect(page.locator('[data-risk-verdict-label]')).toHaveText('STABILISER');
        await page.locator('[data-forward-field="netR"]').fill('-2');
        await expect(page.locator('[data-forward-verdict-label]')).toHaveText('STOP');
        await expect(page.locator('[data-forward-next-action]')).toContainText('Ne risque rien');
        await expect(page.locator('[data-risk-verdict-label]')).toHaveText('VERROUILLÉ');
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
        await expect.poll(() => page.evaluate(() => localStorage.getItem('ict-atlas-session-exam-mastery-v1'))).toBe('true');
        await expect.poll(() => page.evaluate(() => JSON.parse(localStorage.getItem('ict-atlas-session-exam-diagnostic-v1')).score)).toBe(12);
      }

      if (fileName === 'pages/examen-dol-tp.html') {
        const questions = page.locator('[data-target-question]');
        await expect(page.locator('.target-case')).toHaveCount(6);
        await expect(questions).toHaveCount(18);
        await expect(page.locator('[data-target-results]')).toBeHidden();
        await expect(page.locator('[data-target-submit]')).toBeDisabled();

        mkdirSync(path.join(__dirname, '..', 'test-results', 'visual-smoke'), { recursive: true });
        const safeProject = testInfo.project.name.replace(/[^a-z0-9_-]/gi, '-');
        await page.locator('#target-case-01').screenshot({
          path: path.join(__dirname, '..', 'test-results', 'visual-smoke', `${safeProject}-pages-examen-dol-tp-html-case-01.png`),
        });

        for (let question = 0; question < 18; question += 1) {
          await questions.nth(question).locator('input[data-correct="true"]').check();
        }

        await expect(page.locator('[data-target-submit]')).toBeEnabled();
        await page.locator('[data-target-submit]').click();
        await expect(page.locator('[data-target-results]')).toBeVisible();
        await expect(page.locator('[data-target-score]')).toHaveText('18 / 18');
        await expect(page.locator('.target-diagnostic-grid .exam-diagnostic')).toHaveCount(4);
        await expect(page.locator('.target-case .exam-question.is-correct')).toHaveCount(18);
        await expect(page.locator('[data-target-band-code]')).toHaveText('MAÎTRISE');
        await expect.poll(() => page.evaluate(() => JSON.parse(localStorage.getItem('ict-atlas-target-exam-diagnostic-v1')).score)).toBe(18);
      }

      if (fileName === 'pages/tableau-progression.html') {
        await expect(page.locator('.progress-route-step')).toHaveCount(6);
        await expect(page.locator('[data-progress-completed]')).toHaveText('0');
        await expect(page.locator('[data-progress-title]')).toHaveText('Préparer puis passer l’examen de décision');
        await expect(page.locator('.progress-route-step.is-active')).toHaveCount(1);

        mkdirSync(path.join(__dirname, '..', 'test-results', 'visual-smoke'), { recursive: true });
        const safeProject = testInfo.project.name.replace(/[^a-z0-9_-]/gi, '-');
        await page.screenshot({
          path: path.join(__dirname, '..', 'test-results', 'visual-smoke', `${safeProject}-pages-tableau-progression-html-start.png`),
          fullPage: false,
        });

        await page.evaluate(() => {
          localStorage.setItem('ict-atlas-session-exam-best-v1', '8');
          localStorage.setItem('ict-atlas-session-exam-diagnostic-v1', JSON.stringify({
            score: 8,
            total: 12,
            categories: {
              Contexte: { score: 0, total: 2 },
              'DOL / repères': { score: 2, total: 2 },
            },
          }));
        });
        await page.locator('[data-progress-refresh]').click();
        await expect(page.locator('[data-progress-title]')).toHaveText('Repasser l’examen de décision');
        await expect(page.locator('.progress-skill.is-critical')).toHaveCount(1);
        await expect(page.locator('[data-progress-skills] .progress-skill').first()).toContainText('Contexte');

        await page.evaluate(() => {
          localStorage.setItem('ict-atlas-session-exam-best-v1', '12');
          localStorage.setItem('ict-atlas-session-exam-mastery-v1', 'true');
          localStorage.setItem('ict-atlas-target-exam-best-v1', '18');
          localStorage.setItem('ict-atlas-historical-replay-v1', JSON.stringify({ scores: { 'hist-01': 4, 'hist-02': 4, 'hist-03': 4, 'hist-04': 4 }, best: 16 }));
          localStorage.setItem('ict-atlas-validation-20-sessions-v1', JSON.stringify(Array.from({ length: 20 }, () => ({ checks: [true, true, true, true, true], finalized: true }))));
          localStorage.setItem('ict-atlas-forward-gate-v1', JSON.stringify({ verdict: 'go' }));
          localStorage.setItem('ict-atlas-risk-ladder-v1', JSON.stringify({ verdict: 'stabilize' }));
        });
        await page.locator('[data-progress-refresh]').click();
        await expect(page.locator('[data-progress-completed]')).toHaveText('6');
        await expect(page.locator('.progress-route-step.is-complete')).toHaveCount(6);
        await expect(page.locator('[data-progress-state]')).toHaveText('PROCESSUS COMPLET');
        await expect(page.locator('[data-progress-command]')).toHaveAttribute('data-progress-command', 'complete');
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

      if (['index.html', 'pages/04-setups-core.html', 'pages/08-quiz.html', 'pages/19-preuve-statistique.html', 'pages/20-workflow-session.html', 'pages/29-fondations-stop-tp.html', 'pages/replay-cases.html', 'pages/replay-historique.html', 'pages/examen-decision-session.html', 'pages/examen-dol-tp.html', 'pages/tableau-progression.html', 'pages/programme-validation-20-sessions.html', 'pages/41-no-trade.html'].includes(fileName)) {
        mkdirSync(path.join(__dirname, '..', 'test-results', 'visual-smoke'), { recursive: true });
        const safeProject = testInfo.project.name.replace(/[^a-z0-9_-]/gi, '-');
        const safeFileName = fileName.replace(/[^a-z0-9_-]/gi, '-');
        if (['pages/programme-validation-20-sessions.html', 'pages/tableau-progression.html'].includes(fileName)) {
          await page.evaluate(() => {
            document.documentElement.style.scrollBehavior = 'auto';
            window.scrollTo(0, 0);
          });
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
          await page.locator('.session-planner-rail').screenshot({
            path: path.join(__dirname, '..', 'test-results', 'visual-smoke', `${safeProject}-${safeFileName}-v92-no-trade.png`),
          });
          const cockpitReset = page.locator('[data-cockpit-reset]');
          await cockpitReset.click();
          await expect(cockpitReset).toHaveAttribute('data-armed', 'true');
          await cockpitReset.click();
          await expect(page.locator('[data-cockpit-verdict-label]')).toHaveText('À RENSEIGNER');
          await expect(page.locator('[data-cockpit-field="asset"]')).toHaveValue('');
          await expect(page.locator('[data-cockpit-field="riskCap"]')).toHaveValue('0.25');
          await page.reload();
          await expect(page.locator('[data-cockpit-verdict-label]')).toHaveText('À RENSEIGNER');
        }

        if (fileName === 'pages/19-preuve-statistique.html') {
          await page.locator('[data-forward-gate]').screenshot({
            path: path.join(__dirname, '..', 'test-results', 'visual-smoke', `${safeProject}-${safeFileName}-forward-stop.png`),
          });
          await page.evaluate(() => localStorage.setItem('ict-atlas-forward-gate-v1', JSON.stringify({
            minDecisions: 30,
            minTrades: 20,
            minExpectancy: 0.10,
            maxDrawdown: 6,
            maxErrorRate: 10,
            decisions: 30,
            trades: 20,
            netR: 4,
            drawdown: 3,
            processErrors: 2,
            rulesFrozen: true,
            independent: true,
            costsIncluded: true,
            verdict: 'go',
          })));
          await page.reload();
          await page.locator('[data-risk-field="trades"]').fill('20');
          await page.locator('[data-risk-field="netR"]').fill('2');
          await page.locator('[data-risk-field="drawdown"]').fill('2');
          await page.locator('[data-risk-field="processErrors"]').fill('2');
          await page.locator('[data-risk-field="rulesUnchanged"]').check();
          await page.locator('[data-risk-field="noScaleUp"]').check();
          await expect(page.locator('[data-risk-verdict-label]')).toHaveText('PAUSE');
          await page.locator('[data-risk-ladder]').screenshot({
            path: path.join(__dirname, '..', 'test-results', 'visual-smoke', `${safeProject}-${safeFileName}-risk-pause.png`),
          });
          const riskReset = page.locator('[data-risk-reset]');
          await riskReset.click();
          await expect(riskReset).toHaveAttribute('data-armed', 'true');
          await riskReset.click();
          await expect(page.locator('[data-risk-field="trades"]')).toHaveValue('0');
          await expect(page.locator('[data-risk-verdict-label]')).toHaveText('COLLECTER');
          const resetButton = page.locator('[data-forward-reset]');
          await resetButton.click();
          await expect(resetButton).toHaveAttribute('data-armed', 'true');
          await resetButton.click();
          await expect(page.locator('[data-forward-verdict-label]')).toHaveText('CORRIGER');
          await expect(page.locator('[data-forward-field="decisions"]')).toHaveValue('0');
          await page.reload();
          await expect(page.locator('[data-forward-field="decisions"]')).toHaveValue('0');
        }

        if (fileName === 'index.html') {
          await page.locator('#parcours-operationnel').screenshot({
            path: path.join(__dirname, '..', 'test-results', 'visual-smoke', `${safeProject}-${safeFileName}-operational-roadmap.png`),
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

        if (fileName === 'pages/replay-historique.html') {
          await page.locator('.historical-dashboard').screenshot({
            path: path.join(__dirname, '..', 'test-results', 'visual-smoke', `${safeProject}-${safeFileName}-dashboard.png`),
          });
          await page.locator('#hist-01').screenshot({
            path: path.join(__dirname, '..', 'test-results', 'visual-smoke', `${safeProject}-${safeFileName}-reviewed-case.png`),
          });

          const resetButton = page.locator('[data-historical-reset]');
          await resetButton.click();
          await expect(resetButton).toHaveAttribute('data-armed', 'true');
          await resetButton.click();
          await expect(page.locator('[data-historical-completed]')).toHaveText('0 / 4');
          await expect(page.locator('#hist-01 [data-case-status]')).toHaveText('FUTUR MASQUÉ');
          await expect(page.locator('#hist-01 [data-historical-chart]')).toHaveAttribute('data-candles-shown', '14');

          const firstHistoricalCase = page.locator('#hist-01');
          const wrongAnswers = firstHistoricalCase.locator('input:not([data-correct])');
          for (let questionIndex = 0; questionIndex < 4; questionIndex += 1) {
            await wrongAnswers.nth(questionIndex * 2).check();
          }
          await firstHistoricalCase.locator('[data-case-submit]').click();
          await expect(firstHistoricalCase.locator('[data-case-score]')).toHaveText('0 / 4');
          await expect(firstHistoricalCase.locator('fieldset.is-wrong')).toHaveCount(4);
          await expect(firstHistoricalCase.locator('label.is-answer')).toHaveCount(4);
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

        if (fileName === 'pages/examen-dol-tp.html') {
          await page.locator('[data-target-results]').screenshot({
            path: path.join(__dirname, '..', 'test-results', 'visual-smoke', `${safeProject}-${safeFileName}-results.png`),
          });
          await page.locator('[data-target-reset]').click();
          await expect(page.locator('[data-target-results]')).toBeHidden();
          await expect(page.locator('[data-target-answered]')).toHaveText('0');
          await expect(page.locator('[data-target-submit]')).toBeDisabled();
          await expect(page.locator('[data-target-best]')).toHaveText('18 / 18');

          const targetQuestions = page.locator('[data-target-question]');
          for (let question = 0; question < 18; question += 1) {
            await targetQuestions.nth(question).locator('input:not([data-correct])').first().check();
          }
          await page.locator('[data-target-submit]').click();
          await expect(page.locator('[data-target-score]')).toHaveText('0 / 18');
          await expect(page.locator('.target-diagnostic-grid .exam-diagnostic.is-critical')).toHaveCount(4);
          await expect(page.locator('[data-target-band-code]')).toHaveText('RECONSTRUCTION');
          await expect(page.locator('[data-target-best-result]')).toHaveText('18 / 18');
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
