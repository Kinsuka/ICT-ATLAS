(() => {
  const exam = document.querySelector('[data-target-exam]');
  if (!exam) return;

  const cases = [
    {
      id: '01', kicker: 'LONG · DOL OUVERTE', title: 'La route vers la BSL est propre', tone: 'long',
      facts: [['Entrée', '100'], ['Invalidation', '98'], ['Low interne', '—'], ['BSL externe', '106']],
      levels: [{ value: 106, label: 'BSL · DOL', kind: 'target' }, { value: 100, label: 'ENTRÉE', kind: 'entry' }, { value: 98, label: 'STOP', kind: 'stop' }],
      path: 'M48 222 C112 205 145 236 196 198 S274 164 322 180 S400 122 456 146 S540 98 624 64',
      questions: [
        ['DOL / targets', 'Quelle destination principale est défendable ?', ['La BSL externe à 106, encore ouverte.', 'Un prix arbitraire à 110 pour obtenir 5R.', 'Le stop à 98, parce que c’est un niveau visible.'], 0, 'La BSL externe intacte est la destination structurelle explicite du scénario.'],
        ['Géométrie', 'Où placer le stop du plan ?', ['À 99,8 pour réduire artificiellement le risque.', 'Sous l’invalidation structurelle à 98.', 'Au point d’entrée dès l’exécution.'], 1, 'Le stop protège l’hypothèse : il se place au-delà de 98, pas à une distance choisie pour embellir le ratio.'],
        ['Calcul du R', 'Quel potentiel offre la DOL ?', ['1R', '2R', '3R'], 2, 'Risque = 100 − 98 = 2. Gain = 106 − 100 = 6. Potentiel = 6 / 2 = 3R.'],
      ],
    },
    {
      id: '02', kicker: 'SHORT · DEUX CIBLES', title: 'Un low interne précède la SSL', tone: 'short',
      facts: [['Entrée', '205'], ['Invalidation', '208'], ['Low interne', '201'], ['SSL externe', '196']],
      levels: [{ value: 208, label: 'STOP', kind: 'stop' }, { value: 205, label: 'ENTRÉE', kind: 'entry' }, { value: 201, label: 'TP1 · INTERNE', kind: 'partial' }, { value: 196, label: 'SSL · DOL', kind: 'target' }],
      path: 'M48 76 C118 92 150 58 205 94 S292 126 342 112 S420 170 470 150 S552 205 624 236',
      questions: [
        ['DOL / targets', 'Quelle hiérarchie respecte le chemin du prix ?', ['TP1 à 201 puis TP2/DOL à 196.', 'TP1 à 196 puis TP2 à 201.', 'Une seule cible fixe à 2R sans regarder les lows.'], 0, 'Le low interne à 201 est le premier obstacle logique ; la SSL externe à 196 reste la destination principale.'],
        ['Calcul du R', 'Quel R offre la SSL à 196 ?', ['1,33R', '2R', '3R'], 2, 'Risque = 208 − 205 = 3. Gain = 205 − 196 = 9. Le potentiel est donc 3R.'],
        ['Gestion', 'Quelle gestion est cohérente ?', ['Improviser selon la prochaine bougie.', 'Pré-écrire le partiel à 201 et la règle du reliquat vers 196.', 'Déplacer le TP2 à chaque nouveau low.'], 1, 'Le niveau interne permet un partiel planifié ; la gestion du reliquat doit être décidée avant l’entrée.'],
      ],
    },
    {
      id: '03', kicker: 'ANTI-CHASE · ENTRÉE TARDIVE', title: 'Le mouvement est parti sans toi', tone: 'warning',
      facts: [['Entrée prévue', '100'], ['Entrée actuelle', '104'], ['Invalidation', '98'], ['DOL', '106']],
      levels: [{ value: 106, label: 'DOL', kind: 'target' }, { value: 104, label: 'PRIX ACTUEL', kind: 'warning' }, { value: 100, label: 'ENTRÉE RATÉE', kind: 'entry' }, { value: 98, label: 'STOP', kind: 'stop' }],
      path: 'M48 226 C120 210 166 230 214 194 S300 176 346 142 S430 116 492 82 S565 72 624 58',
      questions: [
        ['Géométrie', 'Quel stop utiliser si tu entres à 104 ?', ['Le stop structurel sous 98.', 'Un stop artificiel à 103,5.', 'Aucun stop puisque le scénario était bon.'], 0, 'Une entrée tardive ne déplace pas l’invalidation. Le risque structurel devient 6 points depuis 104.'],
        ['Calcul du R', 'Quel potentiel reste vers 106 depuis 104 ?', ['0,33R', '1R', '3R'], 0, 'Gain restant = 2 ; risque = 6. Le ratio réel est 2 / 6 = 0,33R.'],
        ['Gestion', 'Quelle décision protège le processus ?', ['Chasser car la direction est correcte.', 'Réduire le stop pour retrouver 3R.', 'No trade : l’entrée disponible ne paie plus.'], 2, 'La qualité de l’idée ne sauve pas une mauvaise géométrie. Refuser est ici la décision correcte.'],
      ],
    },
    {
      id: '04', kicker: 'DOL CONSOMMÉE', title: 'Le signal arrive après la destination', tone: 'danger',
      facts: [['Biais', 'Bearish'], ['SSL initiale', '194 · touchée'], ['Signal', 'Après le touch'], ['Prochaine cible', 'Non cartographiée']],
      levels: [{ value: 203, label: 'SIGNAL TARDIF', kind: 'warning' }, { value: 199, label: 'LOW INTERNE PRIS', kind: 'partial' }, { value: 194, label: 'SSL CONSOMMÉE', kind: 'consumed' }],
      path: 'M48 62 C118 82 160 56 222 104 S302 132 364 170 S438 224 500 242 S560 220 624 198',
      questions: [
        ['DOL / targets', 'Quel constat prime sur le signal ?', ['La SSL prévue a déjà été livrée.', 'Le biais bearish garantit une autre expansion.', 'Toute FVG tardive devient une nouvelle DOL.'], 0, 'Une destination consommée ne peut pas justifier rétroactivement une nouvelle entrée. Il faut refaire la carte.'],
        ['Géométrie', 'Peut-on calculer un ordre valide avec ces seules données ?', ['Oui, en visant automatiquement 2R.', 'Non : aucune prochaine cible structurelle n’est définie.', 'Oui, avec un stop de cinq points.'], 1, 'Sans target encore ouverte, le potentiel mesurable manque ; l’ordre reste incomplet.'],
        ['Gestion', 'Quelle prochaine action est correcte ?', ['Vendre le signal puis chercher un TP.', 'Attendre une nouvelle cartographie ou classer no trade.', 'Doubler le risque car le premier mouvement est confirmé.'], 1, 'La séquence reprend à la carte des targets, jamais à l’entrée. Sans nouvelle destination claire : no trade.'],
      ],
    },
    {
      id: '05', kicker: 'OBSTACLE TROP PROCHE', title: 'Le beau trigger ne suffit pas', tone: 'warning',
      facts: [['Entrée short', '310'], ['Invalidation', '314'], ['Zone opposée', '307'], ['SSL externe', '300']],
      levels: [{ value: 314, label: 'STOP', kind: 'stop' }, { value: 310, label: 'ENTRÉE', kind: 'entry' }, { value: 307, label: 'ZONE OPPOSÉE', kind: 'warning' }, { value: 300, label: 'SSL', kind: 'target' }],
      path: 'M48 76 C112 58 164 82 216 102 S292 88 342 122 S408 148 468 154 S546 190 624 226',
      questions: [
        ['DOL / targets', 'Quel niveau doit être traité avant la SSL ?', ['La zone opposée à 307.', 'L’entrée à 310.', 'L’invalidation à 314.'], 0, 'La zone opposée se trouve sur le chemin ; elle peut interrompre la livraison avant la SSL externe.'],
        ['Calcul du R', 'Quel R existe jusqu’au premier obstacle ?', ['0,75R', '1,5R', '2,5R'], 0, 'Risque = 314 − 310 = 4. Gain jusqu’à 307 = 3. Le premier obstacle n’offre que 0,75R.'],
        ['Gestion', 'Si le plan exige au moins 1R avant le premier obstacle ?', ['Exécuter et espérer une traversée.', 'No trade : la route exploitable est trop courte.', 'Rapprocher le stop à 311.'], 1, 'Le filtre doit être appliqué avant l’entrée. Un trigger propre ne supprime ni l’obstacle ni le risque structurel.'],
      ],
    },
    {
      id: '06', kicker: 'APRÈS TP1 · RELIQUAT', title: 'La gestion est écrite avant le résultat', tone: 'long',
      facts: [['Entrée', '50'], ['Stop initial', '48'], ['TP1 atteint', '53'], ['TP2 / DOL', '56']],
      levels: [{ value: 56, label: 'TP2 · DOL', kind: 'target' }, { value: 53, label: 'TP1 ATTEINT', kind: 'partial' }, { value: 50, label: 'ENTRÉE', kind: 'entry' }, { value: 48, label: 'STOP INITIAL', kind: 'stop' }],
      path: 'M48 226 C120 210 164 230 222 188 S304 158 358 170 S430 126 482 138 S556 90 624 70',
      questions: [
        ['Gestion', 'Que faire immédiatement à TP1 ?', ['Appliquer le partiel prévu, sans inventer un nouveau plan.', 'Fermer tout automatiquement, quelle que soit la règle.', 'Augmenter la taille puisque le trade gagne.'], 0, 'TP1 déclenche la règle écrite avant le trade. La gestion ne dépend pas de l’euphorie du moment.'],
        ['Géométrie', 'Que représente 53 depuis l’ordre initial ?', ['0,5R', '1,5R', '3R'], 1, 'Risque initial = 50 − 48 = 2. Gain vers 53 = 3, soit 1,5R.'],
        ['DOL / targets', 'Quand conserver un reliquat vers 56 ?', ['Toujours, parce que TP2 existe.', 'Seulement si la condition pré-écrite reste valide et que le flux n’est pas invalidé.', 'Uniquement après avoir déplacé le stop au-dessus du prix.'], 1, 'Une DOL justifie une destination, pas une obligation de tenir. Le reliquat suit une règle de structure ou de protection préparée.'],
      ],
    },
  ];

  const categoryLinks = {
    'DOL / targets': ['37-dol-targets-hierarchie.html', 'Hiérarchie DOL et targets'],
    'Géométrie': ['29-fondations-stop-tp.html', 'Stop, invalidation et TP'],
    'Calcul du R': ['29-fondations-stop-tp.html#laboratoire-stop-tp', 'Laboratoire Stop / TP'],
    'Gestion': ['37-dol-targets-hierarchie.html#checklist-targets', 'Gestion des targets'],
  };
  const storageKey = 'ict-atlas-target-exam-best-v1';
  const diagnosticStorageKey = 'ict-atlas-target-exam-diagnostic-v1';
  const casesRoot = exam.querySelector('[data-target-cases]');
  const submit = exam.querySelector('[data-target-submit]');
  const results = exam.querySelector('[data-target-results]');
  const answeredLabel = exam.querySelector('[data-target-answered]');
  const progress = exam.querySelector('[role="progressbar"]');
  const progressBar = exam.querySelector('[data-target-progress-bar]');
  const diagnostics = exam.querySelector('[data-target-diagnostics]');
  const review = exam.querySelector('[data-target-review]');

  function diagram(item) {
    const values = item.levels.map((level) => level.value);
    const min = Math.min(...values);
    const max = Math.max(...values);
    const y = (value) => 252 - ((value - min) / Math.max(max - min, 1)) * 204;
    const colors = { target: '#4fd37b', partial: '#53d6e9', entry: '#f8c24e', stop: '#ff6868', warning: '#ff9e64', consumed: '#8e9baa' };
    const levels = item.levels.map((level) => `<g><line x1="38" x2="646" y1="${y(level.value)}" y2="${y(level.value)}" stroke="${colors[level.kind]}" stroke-width="2" stroke-dasharray="7 6"/><rect x="472" y="${y(level.value) - 14}" width="174" height="22" rx="5" fill="#07131f" opacity=".92"/><text x="634" y="${y(level.value) + 2}" text-anchor="end" fill="${colors[level.kind]}" font-size="10" font-weight="900">${level.label} · ${level.value}</text></g>`).join('');
    return `<svg aria-label="Schéma synthétique du cas ${item.id} : ${item.title}" role="img" viewBox="0 0 680 290"><rect width="680" height="290" fill="#06111d"/><g opacity=".55" stroke="#1b3249"><line x1="38" x2="646" y1="48" y2="48"/><line x1="38" x2="646" y1="150" y2="150"/><line x1="38" x2="646" y1="252" y2="252"/></g>${levels}<path d="${item.path}" fill="none" stroke="#d7e6f5" stroke-width="5" stroke-linecap="round"/><circle cx="624" cy="${item.tone === 'short' || item.tone === 'danger' ? 198 : 70}" r="6" fill="#06111d" stroke="#53d6e9" stroke-width="3"/></svg>`;
  }

  function render() {
    let questionNumber = 0;
    casesRoot.innerHTML = cases.map((item) => {
      const questions = item.questions.map(([category, prompt, options, correct, explanation]) => {
        questionNumber += 1;
        const name = `target-q${String(questionNumber).padStart(2, '0')}`;
        const labels = options.map((option, index) => `<label><input ${index === correct ? 'data-correct="true"' : ''} name="${name}" type="radio"/><span>${option}</span></label>`).join('');
        return `<fieldset class="exam-question" data-target-question data-category="${category}" data-explanation="${explanation}"><legend><span>${String(questionNumber).padStart(2, '0')}</span>${prompt}</legend>${labels}</fieldset>`;
      }).join('');
      const facts = item.facts.map(([label, value]) => `<div><small>${label}</small><strong>${value}</strong></div>`).join('');
      return `<section class="card exam-case target-case" id="target-case-${item.id}" data-tone="${item.tone}"><header><div><small>CAS ${item.id} · ${item.kicker}</small><h2>${item.title}</h2></div><span>3 décisions</span></header><div class="exam-case-layout"><div class="exam-chart">${diagram(item)}</div><div class="exam-case-data">${facts}</div></div><div class="exam-question-grid">${questions}</div></section>`;
    }).join('');
  }

  render();
  const questions = [...exam.querySelectorAll('[data-target-question]')];
  const bestLabels = [...exam.querySelectorAll('[data-target-best], [data-target-best-result]')];

  function getBest() {
    try { return Number.parseInt(localStorage.getItem(storageKey) || '0', 10); } catch (_) { return 0; }
  }

  function setBest(score) {
    const best = Math.max(getBest(), score);
    try { localStorage.setItem(storageKey, String(best)); } catch (_) { /* storage can be unavailable */ }
    bestLabels.forEach((label) => { label.textContent = best ? `${best} / ${questions.length}` : `— / ${questions.length}`; });
  }

  function selected(question) {
    return [...question.querySelectorAll('input')].find((input) => input.checked);
  }

  function optionText(input) {
    return input.closest('label').querySelector('span').textContent.trim();
  }

  function updateProgress() {
    const count = questions.filter(selected).length;
    answeredLabel.textContent = String(count);
    progress.setAttribute('aria-valuenow', String(count));
    progressBar.style.width = `${(count / questions.length) * 100}%`;
    submit.disabled = count !== questions.length;
    submit.textContent = count === questions.length ? 'Soumettre et révéler le diagnostic' : `Encore ${questions.length - count} décision${questions.length - count > 1 ? 's' : ''} à prendre`;
  }

  questions.forEach((question) => question.querySelectorAll('input').forEach((input) => input.addEventListener('change', () => {
    question.classList.add('is-answered');
    updateProgress();
  })));

  exam.addEventListener('submit', (event) => {
    event.preventDefault();
    if (questions.some((question) => !selected(question))) return;
    const categories = new Map();
    let score = 0;
    diagnostics.replaceChildren();
    review.replaceChildren();

    questions.forEach((question, index) => {
      const chosen = selected(question);
      const correct = question.querySelector('[data-correct="true"]');
      const isCorrect = chosen === correct;
      const category = question.dataset.category;
      const entry = categories.get(category) || { score: 0, total: 0 };
      entry.total += 1;
      if (isCorrect) { score += 1; entry.score += 1; }
      categories.set(category, entry);
      question.classList.add(isCorrect ? 'is-correct' : 'is-wrong');
      correct.closest('label').classList.add('is-answer');
      if (!isCorrect) chosen.closest('label').classList.add('is-selected-wrong');
      question.querySelectorAll('input').forEach((input) => { input.disabled = true; });

      const item = document.createElement('article');
      item.className = `exam-review-item ${isCorrect ? 'is-correct' : 'is-wrong'}`;
      item.innerHTML = `<div><span>${String(index + 1).padStart(2, '0')}</span><strong>${isCorrect ? 'Décision correcte' : 'Décision à corriger'}</strong></div><p>Ta réponse : ${optionText(chosen)}</p><p>Réponse attendue : ${optionText(correct)}</p><p>${question.dataset.explanation}</p>`;
      review.append(item);
    });

    let critical = false;
    categories.forEach((entry, category) => {
      if (entry.score === 0) critical = true;
      const [href, lesson] = categoryLinks[category];
      const card = document.createElement('article');
      card.className = `exam-diagnostic ${entry.score === entry.total ? 'is-mastered' : entry.score === 0 ? 'is-critical' : 'is-partial'}`;
      card.innerHTML = `<div><strong>${category}</strong><span>${entry.score} / ${entry.total}</span></div><i style="--exam-category-score:${(entry.score / entry.total) * 100}%"></i><a href="${href}">${entry.score === entry.total ? 'Compétence validée' : `Retravailler : ${lesson}`}</a>`;
      diagnostics.append(card);
    });

    try {
      localStorage.setItem(diagnosticStorageKey, JSON.stringify({
        score,
        total: questions.length,
        categories: Object.fromEntries(categories),
        completedAt: new Date().toISOString(),
      }));
    } catch (_) { /* storage can be unavailable */ }

    let code = 'RECONSTRUCTION';
    let band = 'La chaîne cible → ordre → décision reste fragile';
    let summary = 'Reprends uniquement les compétences signalées, recalcule les six cas sur papier puis repasse sans mémoriser les réponses.';
    if (score >= 16 && !critical) {
      code = 'MAÎTRISE'; band = 'Géométrie exploitable en replay'; summary = 'Tu sais hiérarchiser les targets, mesurer le R disponible et refuser une entrée tardive. Vérifie maintenant cette constance sur dix occurrences masquées.';
    } else if (score >= 13 && !critical) {
      code = 'CONSOLIDATION'; band = 'Base solide, faiblesse précisément localisée'; summary = 'Retravaille la ou les catégories incomplètes avant de transposer le protocole en replay autonome.';
    }

    exam.querySelector('[data-target-score]').textContent = `${score} / ${questions.length}`;
    exam.querySelector('[data-target-band-code]').textContent = code;
    exam.querySelector('[data-target-band]').textContent = band;
    exam.querySelector('[data-target-summary]').textContent = summary;
    setBest(score);
    exam.classList.add('is-submitted');
    submit.hidden = true;
    results.hidden = false;
    results.scrollIntoView({ behavior: 'smooth', block: 'start' });
  });

  exam.querySelector('[data-target-reset]').addEventListener('click', () => {
    exam.reset();
    questions.forEach((question) => {
      question.classList.remove('is-answered', 'is-correct', 'is-wrong');
      question.querySelectorAll('input').forEach((input) => { input.disabled = false; });
      question.querySelectorAll('label').forEach((label) => label.classList.remove('is-answer', 'is-selected-wrong'));
    });
    diagnostics.replaceChildren();
    review.replaceChildren();
    exam.classList.remove('is-submitted');
    results.hidden = true;
    submit.hidden = false;
    updateProgress();
    exam.scrollIntoView({ behavior: 'smooth', block: 'start' });
  });

  setBest(getBest());
  updateProgress();
})();
