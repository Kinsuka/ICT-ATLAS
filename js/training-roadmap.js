(() => {
  const root = document.querySelector('[data-training-roadmap]');
  if (!root) return;

  const examBestKey = 'ict-atlas-session-exam-best-v1';
  const examMasteryKey = 'ict-atlas-session-exam-mastery-v1';
  const targetBestKey = 'ict-atlas-target-exam-best-v1';
  const historicalKey = 'ict-atlas-historical-replay-v1';
  const validationKey = 'ict-atlas-validation-20-sessions-v1';
  const forwardKey = 'ict-atlas-forward-gate-v1';

  function read(key) {
    try { return localStorage.getItem(key); } catch (_) { return null; }
  }

  const best = Number.parseInt(read(examBestKey) || '0', 10) || 0;
  const examMastered = read(examMasteryKey) === 'true' || best >= 10;
  const targetBest = Number.parseInt(read(targetBestKey) || '0', 10) || 0;
  const targetMastered = targetBest >= 16;
  let historicalCompleted = 0;
  let historicalTotal = 0;
  try {
    const historical = JSON.parse(read(historicalKey));
    const scores = historical && typeof historical.scores === 'object' ? historical.scores : {};
    historicalCompleted = Object.keys(scores).length;
    historicalTotal = Object.values(scores).reduce((sum, value) => sum + (Number(value) || 0), 0);
  } catch (_) { /* unavailable or invalid local progress */ }
  const historicalMastered = historicalCompleted === 4 && historicalTotal >= 12;
  let records = [];
  try {
    const stored = JSON.parse(read(validationKey));
    if (Array.isArray(stored) && stored.length === 20) records = stored;
  } catch (_) { /* unavailable or invalid local progress */ }

  const finalized = records.filter((record) => record && record.finalized);
  const passes = (record) => {
    const checks = Array.isArray(record && record.checks) ? record.checks.map(Boolean) : [];
    return Boolean(record && record.finalized && checks.filter(Boolean).length >= 4 && checks[2] && checks[3]);
  };
  const passed = records.filter(passes).length;
  const phasesValid = [0, 1, 2, 3].every((phase) => {
    const phaseRecords = records.slice(phase * 5, phase * 5 + 5);
    return phaseRecords.length === 5
      && phaseRecords.every((record) => record && record.finalized)
      && phaseRecords.filter(passes).length >= 4;
  });
  const riskValid = records.length === 20
    && records.slice(10).every((record) => record && record.finalized && Array.isArray(record.checks) && record.checks[3]);
  const validationReady = finalized.length === 20 && passed >= 17 && phasesValid && riskValid;
  let forwardVerdict = '';
  try {
    const storedForward = JSON.parse(read(forwardKey));
    if (storedForward && ['go', 'correct', 'stop'].includes(storedForward.verdict)) forwardVerdict = storedForward.verdict;
  } catch (_) { /* unavailable or invalid local progress */ }

  const examStatus = root.querySelector('[data-roadmap-exam-status]');
  const targetStatus = root.querySelector('[data-roadmap-target-status]');
  const historicalStatus = root.querySelector('[data-roadmap-historical-status]');
  const validationStatus = root.querySelector('[data-roadmap-validation-status]');
  const forwardStatus = root.querySelector('[data-roadmap-forward-status]');
  const nextLink = root.querySelector('[data-roadmap-next-link]');
  const nextTitle = root.querySelector('[data-roadmap-next-title]');
  const nextDetail = root.querySelector('[data-roadmap-next-detail]');

  examStatus.textContent = examMastered ? 'SEUIL VALIDÉ' : best ? `MEILLEUR · ${best} / 12` : 'NON TENTÉ';
  targetStatus.textContent = targetMastered ? 'SEUIL VALIDÉ' : targetBest ? `MEILLEUR · ${targetBest} / 18` : 'NON TENTÉ';
  historicalStatus.textContent = historicalMastered ? 'SEUIL VALIDÉ' : `${historicalCompleted} / 4 · ${historicalTotal} / 16`;
  validationStatus.textContent = validationReady ? 'VALIDÉ · 20 / 20' : `${finalized.length} / 20 · ${passed} CONFORMES`;
  forwardStatus.textContent = !validationReady ? 'VERROUILLÉ' : forwardVerdict === 'go' ? 'GO PÉDAGOGIQUE' : forwardVerdict === 'stop' ? 'STOP / AUDIT' : forwardVerdict === 'correct' ? 'EN COURS' : 'À DÉMARRER';
  root.querySelector('[data-roadmap-stage="exam"]').classList.toggle('is-complete', examMastered);
  root.querySelector('[data-roadmap-stage="target"]').classList.toggle('is-complete', targetMastered);
  root.querySelector('[data-roadmap-stage="historical"]').classList.toggle('is-complete', historicalMastered);
  root.querySelector('[data-roadmap-stage="validation"]').classList.toggle('is-complete', validationReady);
  const forwardStage = root.querySelector('[data-roadmap-stage="forward"]');
  forwardStage.classList.toggle('is-unlocked', validationReady);
  forwardStage.classList.toggle('is-complete', validationReady && forwardVerdict === 'go');

  if (validationReady) {
    nextLink.href = forwardVerdict === 'go' ? 'pages/19-preuve-statistique.html#v90-risk-ladder' : 'pages/19-preuve-statistique.html';
    nextTitle.textContent = forwardVerdict === 'go' ? 'Configurer l’échelle de micro-risque' : forwardVerdict === 'stop' ? 'Auditer le bloc forward' : forwardVerdict === 'correct' ? 'Continuer le Forward Test Control' : 'Démarrer l’échantillon indépendant';
    nextDetail.textContent = forwardVerdict === 'go' ? 'Le GO ne déclenche pas une montée : il déverrouille seulement un bloc au plus petit risque.' : forwardVerdict === 'stop' ? 'Aucun risque : identifie la porte échouée avant de créer une version distincte.' : 'Conserve exactement le même modèle et mesure l’espérance hors échantillon.';
  } else if (!examMastered && (best > 0 || targetBest > 0 || historicalCompleted > 0 || finalized.length > 0)) {
    nextLink.href = 'pages/examen-decision-session.html';
    nextTitle.textContent = best ? 'Repasser l’examen de décision' : 'Passer l’examen de décision';
    nextDetail.textContent = best
      ? `Meilleur score : ${best}/12. Corrige d’abord les compétences sous le seuil.`
      : 'Des preuves plus avancées existent sur cet appareil, mais le premier seuil obligatoire manque encore.';
  } else if (examMastered && !targetMastered) {
    nextLink.href = 'pages/examen-dol-tp.html';
    nextTitle.textContent = targetBest ? 'Repasser l’examen DOL / TP' : 'Passer l’examen DOL / TP';
    nextDetail.textContent = targetBest ? `Meilleur score : ${targetBest}/18. Le seuil est 16/18.` : 'Valide la hiérarchie DOL, les targets et le R restant avant le replay historique.';
  } else if (targetMastered && !historicalMastered) {
    nextLink.href = 'pages/replay-historique.html';
    nextTitle.textContent = 'Résoudre les quatre gels historiques';
    nextDetail.textContent = `${historicalCompleted}/4 cas corrigés · ${historicalTotal}/16. Le seuil est 12/16.`;
  } else if (finalized.length > 0 || historicalMastered) {
    nextLink.href = 'pages/programme-validation-20-sessions.html';
    const nextIncomplete = records.findIndex((record) => !record || !record.finalized);
    nextTitle.textContent = finalized.length === 20
      ? 'Reprendre les sessions non conformes'
      : finalized.length
        ? `Continuer à la session ${String(nextIncomplete + 1).padStart(2, '0')}`
        : 'Commencer les 20 sessions replay';
    nextDetail.textContent = `${finalized.length} session${finalized.length > 1 ? 's' : ''} évaluée${finalized.length > 1 ? 's' : ''} · ${passed} conforme${passed > 1 ? 's' : ''}.`;
  } else {
    nextLink.href = 'pages/16-modele-mental.html';
    nextTitle.textContent = 'Commencer par le modèle mental';
    nextDetail.textContent = 'Première visite : suis ensuite les boutons Continuer jusqu’à la leçon 41.';
  }
})();
