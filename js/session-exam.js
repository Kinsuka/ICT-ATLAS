(() => {
  const exam = document.querySelector('[data-session-exam]');
  if (!exam) return;

  const questions = [...exam.querySelectorAll('[data-exam-question]')];
  const submit = exam.querySelector('[data-exam-submit]');
  const answeredLabel = exam.querySelector('[data-exam-answered]');
  const progress = exam.querySelector('[role="progressbar"]');
  const progressBar = exam.querySelector('[data-exam-progress-bar]');
  const results = exam.querySelector('[data-exam-results]');
  const diagnostics = exam.querySelector('[data-exam-diagnostics]');
  const review = exam.querySelector('[data-exam-review]');
  const reset = exam.querySelector('[data-exam-reset]');
  const bestLabels = [...exam.querySelectorAll('[data-exam-best], [data-exam-best-result]')];
  const storageKey = 'ict-atlas-session-exam-best-v1';
  const masteryStorageKey = 'ict-atlas-session-exam-mastery-v1';
  const diagnosticStorageKey = 'ict-atlas-session-exam-diagnostic-v1';

  function getBest() {
    try {
      return Number.parseInt(localStorage.getItem(storageKey) || '0', 10);
    } catch (_) {
      return 0;
    }
  }

  function setBest(score) {
    const best = Math.max(getBest(), score);
    try { localStorage.setItem(storageKey, String(best)); } catch (_) { /* local storage can be unavailable */ }
    bestLabels.forEach((label) => { label.textContent = best ? `${best} / ${questions.length}` : `— / ${questions.length}`; });
  }

  function selectedInput(question) {
    return [...question.querySelectorAll('input[type="radio"]')].find((input) => input.checked);
  }

  function optionText(input) {
    return input.closest('label').querySelector('span').textContent.trim();
  }

  function updateProgress() {
    const answered = questions.filter((question) => selectedInput(question)).length;
    answeredLabel.textContent = String(answered);
    progress.setAttribute('aria-valuenow', String(answered));
    progressBar.style.width = `${(answered / questions.length) * 100}%`;
    submit.disabled = answered !== questions.length;
    submit.textContent = answered === questions.length
      ? 'Soumettre et révéler le diagnostic'
      : `Encore ${questions.length - answered} décision${questions.length - answered > 1 ? 's' : ''} à prendre`;
  }

  questions.forEach((question) => {
    question.querySelectorAll('input[type="radio"]').forEach((input) => {
      input.addEventListener('change', () => {
        question.classList.add('is-answered');
        updateProgress();
      });
    });
  });

  exam.addEventListener('submit', (event) => {
    event.preventDefault();
    if (questions.some((question) => !selectedInput(question))) return;

    const categories = new Map();
    let score = 0;
    diagnostics.replaceChildren();
    review.replaceChildren();

    questions.forEach((question, index) => {
      const selected = selectedInput(question);
      const correct = question.querySelector('input[data-correct="true"]');
      const isCorrect = selected === correct;
      const category = question.dataset.category;
      const entry = categories.get(category) || {
        score: 0,
        total: 0,
        lesson: question.dataset.lesson,
        lessonLabel: question.dataset.lessonLabel,
      };

      entry.total += 1;
      if (isCorrect) {
        score += 1;
        entry.score += 1;
      }
      categories.set(category, entry);

      question.classList.add(isCorrect ? 'is-correct' : 'is-wrong');
      correct.closest('label').classList.add('is-answer');
      if (!isCorrect) selected.closest('label').classList.add('is-selected-wrong');
      question.querySelectorAll('input').forEach((input) => { input.disabled = true; });

      const item = document.createElement('article');
      item.className = `exam-review-item ${isCorrect ? 'is-correct' : 'is-wrong'}`;
      const head = document.createElement('div');
      const number = document.createElement('span');
      number.textContent = String(index + 1).padStart(2, '0');
      const title = document.createElement('strong');
      title.textContent = isCorrect ? 'Décision correcte' : 'Décision à corriger';
      head.append(number, title);
      const chosen = document.createElement('p');
      chosen.textContent = `Ta réponse : ${optionText(selected)}`;
      const expected = document.createElement('p');
      expected.textContent = `Réponse attendue : ${optionText(correct)}`;
      const explanation = document.createElement('p');
      explanation.textContent = question.dataset.explanation;
      item.append(head, chosen, expected, explanation);
      review.append(item);
    });

    let hasZeroCategory = false;
    categories.forEach((entry, category) => {
      if (entry.score === 0) hasZeroCategory = true;
      const card = document.createElement('article');
      card.className = `exam-diagnostic ${entry.score === entry.total ? 'is-mastered' : entry.score === 0 ? 'is-critical' : 'is-partial'}`;
      const head = document.createElement('div');
      const name = document.createElement('strong');
      name.textContent = category;
      const value = document.createElement('span');
      value.textContent = `${entry.score} / ${entry.total}`;
      head.append(name, value);
      const bar = document.createElement('i');
      bar.style.setProperty('--exam-category-score', `${(entry.score / entry.total) * 100}%`);
      const link = document.createElement('a');
      link.href = entry.lesson;
      link.textContent = entry.score === entry.total ? 'Compétence validée' : `Retravailler : ${entry.lessonLabel}`;
      card.append(head, bar, link);
      diagnostics.append(card);
    });

    try {
      localStorage.setItem(diagnosticStorageKey, JSON.stringify({
        score,
        total: questions.length,
        categories: Object.fromEntries(categories),
        completedAt: new Date().toISOString(),
      }));
    } catch (_) { /* local storage can be unavailable */ }

    const mastered = score >= 10 && !hasZeroCategory;
    if (mastered) {
      try { localStorage.setItem(masteryStorageKey, 'true'); } catch (_) { /* local storage can be unavailable */ }
    }
    let bandCode = 'RECONSTRUCTION';
    let band = 'Processus encore fragmenté';
    let summary = 'Reprends les portes indiquées avant un nouveau passage. Le but n’est pas de mémoriser les réponses, mais de restaurer l’ordre de décision.';
    if (mastered) {
      bandCode = 'MAÎTRISE PÉDAGOGIQUE';
      band = 'Prêt à transposer en replay non guidé';
      summary = 'Le protocole est cohérent sur les six compétences. Valide maintenant cette qualité sur un échantillon de sessions replay, jamais directement par du risque live.';
    } else if (score >= 8) {
      bandCode = 'CONSOLIDATION';
      band = 'Base solide, portes faibles identifiées';
      summary = 'Travaille uniquement les catégories sous 2/2, puis repasse l’examen sans consulter la correction.';
    } else if (score >= 5) {
      bandCode = 'PROCESSUS INCOMPLET';
      band = 'La séquence se brise encore sous décision';
      summary = 'Retourne aux simulateurs guidés et verbalise chaque prochaine action avant de cliquer.';
    }

    exam.querySelector('[data-exam-score]').textContent = `${score} / ${questions.length}`;
    exam.querySelector('[data-exam-band-code]').textContent = bandCode;
    exam.querySelector('[data-exam-band]').textContent = band;
    exam.querySelector('[data-exam-summary]').textContent = summary;
    setBest(score);
    exam.classList.add('is-submitted');
    submit.disabled = true;
    submit.hidden = true;
    results.hidden = false;
    results.scrollIntoView({ behavior: 'smooth', block: 'start' });
  });

  reset.addEventListener('click', () => {
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
