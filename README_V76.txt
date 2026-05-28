ICT Atlas V76 - Installation Playwright

Objectif
- Installer Playwright pour valider visuellement le cours en rendu navigateur.
- Ajouter un test smoke visuel desktop/mobile sur les pages graphiques clés.

Installation
- package.json initialise.
- @playwright/test installe en devDependency.
- Chromium installe via npx playwright install chromium.
- .gitignore complete :
  - node_modules/
  - test-results/
  - playwright-report/

Commandes
- npm run test:e2e
- npm run test:e2e:headed
- npm run test:e2e:update

Test ajoute
- tests/course-visual.spec.js
- Pages couvertes :
  - index.html
  - 04-setups-core.html
  - 08-quiz.html
  - 21-liquidite-deplacement.html
  - 27-fondations-liquidite.html
  - 28-fondations-entree.html
  - 29-fondations-stop-tp.html
  - 31-order-blocks.html
  - 32-fvg-imbalance-ce.html
  - 33-mss-changement-controle.html
  - 39-profils-journee-sessions.html
  - 40-displacement-operationnel.html
  - 41-no-trade.html

Contrôles Playwright
- h1 visible.
- SVG visibles avec dimensions utiles.
- aucun SVG sans aria-label.
- aucune réponse de quiz visible avant correction.
- aucun texte SVG hors de son graphique.
- screenshots smoke sur pages clés.

Validation
- npm run test:e2e : 26 passed.
- Projets :
  - chromium-desktop
  - chromium-mobile
