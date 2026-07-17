(() => {
  const root = document.querySelector('[data-training-roadmap]');
  if (!root) return;

  const examBestKey = 'ict-atlas-session-exam-best-v1';
  const examMasteryKey = 'ict-atlas-session-exam-mastery-v1';
  const validationKey = 'ict-atlas-validation-20-sessions-v1';
  const forwardKey = 'ict-atlas-forward-gate-v1';

  function read(key) {
    try { return localStorage.getItem(key); } catch (_) { return null; }
  }

  const best = Number.parseInt(read(examBestKey) || '0', 10) || 0;
  const examMastered = read(examMasteryKey) === 'true' || best === 12;
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
  const validationStatus = root.querySelector('[data-roadmap-validation-status]');
  const forwardStatus = root.querySelector('[data-roadmap-forward-status]');
  const nextLink = root.querySelector('[data-roadmap-next-link]');
  const nextTitle = root.querySelector('[data-roadmap-next-title]');
  const nextDetail = root.querySelector('[data-roadmap-next-detail]');

  examStatus.textContent = examMastered ? 'SEUIL VALIDÉ' : best ? `MEILLEUR · ${best} / 12` : 'NON TENTÉ';
  validationStatus.textContent = validationReady ? 'VALIDÉ · 20 / 20' : `${finalized.length} / 20 · ${passed} CONFORMES`;
  forwardStatus.textContent = !validationReady ? 'VERROUILLÉ' : forwardVerdict === 'go' ? 'GO PÉDAGOGIQUE' : forwardVerdict === 'stop' ? 'STOP / AUDIT' : forwardVerdict === 'correct' ? 'EN COURS' : 'À DÉMARRER';
  root.querySelector('[data-roadmap-stage="exam"]').classList.toggle('is-complete', examMastered);
  root.querySelector('[data-roadmap-stage="validation"]').classList.toggle('is-complete', validationReady);
  const forwardStage = root.querySelector('[data-roadmap-stage="forward"]');
  forwardStage.classList.toggle('is-unlocked', validationReady);
  forwardStage.classList.toggle('is-complete', validationReady && forwardVerdict === 'go');

  if (validationReady) {
    nextLink.href = 'pages/19-preuve-statistique.html';
    nextTitle.textContent = forwardVerdict === 'go' ? 'Relire le verdict forward' : forwardVerdict === 'stop' ? 'Auditer le bloc forward' : forwardVerdict === 'correct' ? 'Continuer le Forward Test Control' : 'Démarrer l’échantillon indépendant';
    nextDetail.textContent = forwardVerdict === 'go' ? 'Le GO reste pédagogique : applique uniquement le plus petit risque déjà défini dans ton plan.' : forwardVerdict === 'stop' ? 'Aucun risque : identifie la porte échouée avant de créer une version distincte.' : 'Conserve exactement le même modèle et mesure l’espérance hors échantillon.';
  } else if (finalized.length > 0 || examMastered) {
    nextLink.href = 'pages/programme-validation-20-sessions.html';
    const nextIncomplete = records.findIndex((record) => !record || !record.finalized);
    nextTitle.textContent = finalized.length === 20
      ? 'Reprendre les sessions non conformes'
      : finalized.length
        ? `Continuer à la session ${String(nextIncomplete + 1).padStart(2, '0')}`
        : 'Commencer les 20 sessions replay';
    nextDetail.textContent = `${finalized.length} session${finalized.length > 1 ? 's' : ''} évaluée${finalized.length > 1 ? 's' : ''} · ${passed} conforme${passed > 1 ? 's' : ''}.`;
  } else if (best > 0) {
    nextLink.href = 'pages/examen-decision-session.html';
    nextTitle.textContent = 'Repasser l’examen de décision';
    nextDetail.textContent = `Meilleur score : ${best}/12. Corrige d’abord les compétences sous le seuil.`;
  }
})();
