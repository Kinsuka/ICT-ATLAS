(() => {
  const root = document.querySelector('[data-progress-dashboard]');
  if (!root) return;

  const keys = {
    sessionBest: 'ict-atlas-session-exam-best-v1',
    sessionMastery: 'ict-atlas-session-exam-mastery-v1',
    sessionDiagnostic: 'ict-atlas-session-exam-diagnostic-v1',
    targetBest: 'ict-atlas-target-exam-best-v1',
    targetDiagnostic: 'ict-atlas-target-exam-diagnostic-v1',
    historical: 'ict-atlas-historical-replay-v1',
    validation: 'ict-atlas-validation-20-sessions-v1',
    forward: 'ict-atlas-forward-gate-v1',
    risk: 'ict-atlas-risk-ladder-v1',
  };

  const routeDefinitions = [
    ['Décision', 'Examen session', 'examen-decision-session.html'],
    ['Targets', 'Examen DOL / TP', 'examen-dol-tp.html'],
    ['Reconnaissance', 'Replay historique', 'replay-historique.html'],
    ['Répétition', '20 sessions replay', 'programme-validation-20-sessions.html'],
    ['Preuve', 'Forward indépendant', '19-preuve-statistique.html'],
    ['Protection', 'Micro-risque', '19-preuve-statistique.html#v90-risk-ladder'],
  ];

  function read(key) {
    try { return localStorage.getItem(key); } catch (_) { return null; }
  }

  function json(key, fallback = null) {
    try { return JSON.parse(read(key)) ?? fallback; } catch (_) { return fallback; }
  }

  function integer(key) {
    return Number.parseInt(read(key) || '0', 10) || 0;
  }

  function validationState(records) {
    const list = Array.isArray(records) && records.length === 20 ? records : [];
    const finalized = list.filter((record) => record && record.finalized);
    const passes = (record) => {
      const checks = Array.isArray(record && record.checks) ? record.checks.map(Boolean) : [];
      return Boolean(record && record.finalized && checks.filter(Boolean).length >= 4 && checks[2] && checks[3]);
    };
    const passed = list.filter(passes).length;
    const phasesValid = [0, 1, 2, 3].every((phase) => {
      const phaseRecords = list.slice(phase * 5, phase * 5 + 5);
      return phaseRecords.length === 5 && phaseRecords.every((record) => record && record.finalized) && phaseRecords.filter(passes).length >= 4;
    });
    const riskValid = list.length === 20 && list.slice(10).every((record) => record && record.finalized && Array.isArray(record.checks) && record.checks[3]);
    return { completed: finalized.length, passed, ready: finalized.length === 20 && passed >= 17 && phasesValid && riskValid };
  }

  function collect() {
    const sessionBest = integer(keys.sessionBest);
    const targetBest = integer(keys.targetBest);
    const sessionDiagnostic = json(keys.sessionDiagnostic, {});
    const targetDiagnostic = json(keys.targetDiagnostic, {});
    const historical = json(keys.historical, {});
    const historicalScores = historical && typeof historical.scores === 'object' ? historical.scores : {};
    const historicalCompleted = Object.keys(historicalScores).length;
    const historicalTotal = Object.values(historicalScores).reduce((sum, value) => sum + (Number(value) || 0), 0);
    const validation = validationState(json(keys.validation, []));
    const forward = json(keys.forward, {});
    const risk = json(keys.risk, {});
    const sessionMastered = read(keys.sessionMastery) === 'true' || sessionBest >= 10;
    const targetMastered = targetBest >= 16;
    const historicalMastered = historicalCompleted === 4 && historicalTotal >= 12;
    const forwardMastered = validation.ready && forward.verdict === 'go';
    const riskMastered = forwardMastered && risk.verdict === 'stabilize';
    const stages = [sessionMastered, targetMastered, historicalMastered, validation.ready, forwardMastered, riskMastered];
    return { sessionBest, targetBest, sessionDiagnostic, targetDiagnostic, historicalCompleted, historicalTotal, validation, forward, risk, stages };
  }

  function priority(data) {
    if (data.sessionBest === 0) return { index: 0, state: 'FONDATION ACTIVE', title: 'Préparer puis passer l’examen de décision', detail: 'Remplis d’abord le cockpit sur une situation, puis vérifie si tu respectes l’ordre contexte → DOL → événement → ordre.', href: '20-workflow-session.html#v92-session-cockpit', cta: 'Ouvrir le cockpit' };
    if (!data.stages[0]) return { index: 0, state: 'REMÉDIATION PRIORITAIRE', title: 'Repasser l’examen de décision', detail: `Ton meilleur score est ${data.sessionBest}/12. Retravaille les compétences faibles affichées ci-dessous avant un nouveau passage.`, href: 'examen-decision-session.html', cta: 'Corriger la décision' };
    if (!data.stages[1]) return { index: 1, state: 'GÉOMÉTRIE À PROUVER', title: 'Valider DOL, TP et entrée tardive', detail: data.targetBest ? `Ton meilleur score est ${data.targetBest}/18. Recalcule targets, stop structurel et R restant.` : 'Passe les six scénarios sans consulter les corrections : targets, géométrie, R et gestion.', href: 'examen-dol-tp.html', cta: 'Passer l’examen DOL / TP' };
    if (!data.stages[2]) return { index: 2, state: 'TRANSFERT AU GRAPHIQUE', title: 'Résoudre les quatre gels historiques', detail: `${data.historicalCompleted}/4 cas terminés · ${data.historicalTotal}/16. Décide avant de révéler le futur.`, href: 'replay-historique.html', cta: 'Continuer le replay historique' };
    if (!data.stages[3]) return { index: 3, state: 'RÉPÉTITION EN COURS', title: 'Continuer les 20 sessions replay', detail: `${data.validation.completed}/20 sessions évaluées · ${data.validation.passed} conformes. Le P&L ne donne aucun point.`, href: 'programme-validation-20-sessions.html', cta: 'Produire la prochaine session' };
    if (!data.stages[4]) return { index: 4, state: data.forward.verdict === 'stop' ? 'AUDIT OBLIGATOIRE' : 'ÉCHANTILLON INDÉPENDANT', title: data.forward.verdict === 'stop' ? 'Auditer le bloc forward' : 'Compléter le Forward Test Control', detail: data.forward.verdict === 'stop' ? 'Le contrôle affiche STOP : aucun risque. Corrige la porte échouée dans un bloc distinct.' : 'Le replay est validé. Mesure maintenant le même modèle hors échantillon, sans modifier le ruleset.', href: '19-preuve-statistique.html', cta: 'Ouvrir le contrôle forward' };
    if (!data.stages[5]) return { index: 5, state: data.risk.verdict === 'pause' ? 'PAUSE PROTECTRICE' : 'MICRO-RISQUE UNIQUEMENT', title: data.risk.verdict === 'pause' ? 'Corriger la limite touchée' : 'Stabiliser le plus petit risque', detail: data.risk.verdict === 'pause' ? 'Une protection a été touchée. Archive le bloc avant toute nouvelle exposition.' : 'Le GO forward ne déverrouille qu’un bloc au risque minimum, jamais une montée automatique.', href: '19-preuve-statistique.html#v90-risk-ladder', cta: 'Ouvrir l’échelle de risque' };
    return { index: 5, state: 'PROCESSUS COMPLET', title: 'Répéter sans augmenter automatiquement', detail: 'Toutes les portes locales sont validées. Maintiens le ruleset et le plus petit risque tant qu’un nouveau seuil écrit n’est pas prouvé.', href: '19-preuve-statistique.html#v90-risk-ladder', cta: 'Revoir les protections' };
  }

  function skills(data) {
    const sources = [
      ['Examen session', data.sessionDiagnostic, 'examen-decision-session.html'],
      ['Examen DOL / TP', data.targetDiagnostic, 'examen-dol-tp.html'],
    ];
    return sources.flatMap(([source, diagnostic, href]) => {
      if (!diagnostic || typeof diagnostic.categories !== 'object') return [];
      return Object.entries(diagnostic.categories).map(([name, result]) => ({
        source, name, href, score: Number(result.score) || 0, total: Number(result.total) || 0,
      }));
    }).filter((item) => item.total > 0).sort((a, b) => (a.score / a.total) - (b.score / b.total));
  }

  function renderRoute(data, activeIndex) {
    const route = root.querySelector('[data-progress-route]');
    route.replaceChildren();
    routeDefinitions.forEach(([kicker, title, href], index) => {
      const card = document.createElement('a');
      card.href = href;
      card.className = `progress-route-step ${data.stages[index] ? 'is-complete' : index === activeIndex ? 'is-active' : 'is-locked'}`;
      card.innerHTML = `<span>${String(index + 1).padStart(2, '0')}</span><small>${kicker}</small><strong>${title}</strong><em>${data.stages[index] ? 'VALIDÉ' : index === activeIndex ? 'À FAIRE' : 'EN ATTENTE'}</em>`;
      route.append(card);
    });
  }

  function renderSkills(data) {
    const box = root.querySelector('[data-progress-skills]');
    const list = skills(data);
    box.replaceChildren();
    if (!list.length) {
      box.innerHTML = '<div class="progress-empty"><strong>Aucun diagnostic disponible</strong><p>Passe d’abord un examen. Les compétences les plus faibles apparaîtront ici automatiquement.</p></div>';
      return;
    }
    list.slice(0, 8).forEach((item) => {
      const ratio = item.score / item.total;
      const card = document.createElement('a');
      card.href = item.href;
      card.className = `progress-skill ${ratio === 1 ? 'is-strong' : ratio === 0 ? 'is-critical' : 'is-partial'}`;
      card.innerHTML = `<div><small>${item.source}</small><strong>${item.name}</strong></div><span>${item.score} / ${item.total}</span><i style="--skill-score:${ratio * 100}%"></i><em>${ratio === 1 ? 'Acquis au dernier passage' : ratio === 0 ? 'Premier verrou à reconstruire' : 'À consolider'}</em>`;
      box.append(card);
    });
  }

  function renderEvidence(data) {
    const rows = [
      ['Décision session', data.sessionBest ? `${data.sessionBest} / 12` : 'Non tenté', data.stages[0]],
      ['DOL / TP', data.targetBest ? `${data.targetBest} / 18` : 'Non tenté', data.stages[1]],
      ['Replay historique', `${data.historicalCompleted} / 4 · ${data.historicalTotal} / 16`, data.stages[2]],
      ['Sessions replay', `${data.validation.completed} / 20 · ${data.validation.passed} conformes`, data.stages[3]],
      ['Forward test', data.forward.verdict ? String(data.forward.verdict).toUpperCase() : 'Non démarré', data.stages[4]],
      ['Micro-risque', data.risk.verdict ? String(data.risk.verdict).toUpperCase() : 'Verrouillé', data.stages[5]],
    ];
    const box = root.querySelector('[data-progress-evidence]');
    box.innerHTML = rows.map(([label, value, complete], index) => `<article class="${complete ? 'is-complete' : ''}"><span>${String(index + 1).padStart(2, '0')}</span><div><strong>${label}</strong><small>${value}</small></div><em>${complete ? 'OK' : 'OUVERT'}</em></article>`).join('');
  }

  function report(data, next) {
    const weak = skills(data).filter((item) => item.score < item.total).slice(0, 4);
    return [
      'ICT ATLAS — BILAN DE PROGRESSION',
      `Généré : ${new Date().toLocaleString('fr-BE')}`,
      '',
      `Prochaine action : ${next.title}`,
      `Pourquoi : ${next.detail}`,
      '',
      `Examen session : ${data.sessionBest || 0}/12`,
      `Examen DOL / TP : ${data.targetBest || 0}/18`,
      `Replay historique : ${data.historicalCompleted}/4 · ${data.historicalTotal}/16`,
      `Programme replay : ${data.validation.completed}/20 · ${data.validation.passed} conformes`,
      `Forward : ${data.forward.verdict || 'non démarré'}`,
      `Micro-risque : ${data.risk.verdict || 'verrouillé'}`,
      '',
      'Compétences à renforcer :',
      ...(weak.length ? weak.map((item) => `- ${item.name} : ${item.score}/${item.total} (${item.source})`) : ['- Aucun diagnostic faible enregistré.']),
      '',
      'Ce bilan pédagogique ne prouve pas un edge et n’autorise aucun risque live.',
    ].join('\n');
  }

  let currentReport = '';

  function render() {
    const data = collect();
    const next = priority(data);
    const completed = data.stages.filter(Boolean).length;
    const command = root.querySelector('[data-progress-command]');
    command.dataset.progressCommand = completed === 6 ? 'complete' : next.state.includes('AUDIT') || next.state.includes('PAUSE') ? 'blocked' : 'active';
    root.querySelector('[data-progress-priority-code]').textContent = String(next.index + 1).padStart(2, '0');
    root.querySelector('[data-progress-state]').textContent = next.state;
    root.querySelector('[data-progress-title]').textContent = next.title;
    root.querySelector('[data-progress-detail]').textContent = next.detail;
    const action = root.querySelector('[data-progress-action]');
    action.href = next.href;
    action.querySelector('strong').textContent = `${next.cta} →`;
    root.querySelector('[data-progress-completed]').textContent = String(completed);
    root.querySelector('[data-progress-overall-bar]').style.setProperty('--progress-value', `${(completed / 6) * 100}%`);
    root.querySelector('[data-progress-session-score]').textContent = data.sessionBest ? `${data.sessionBest} / 12` : '— / 12';
    root.querySelector('[data-progress-session-label]').textContent = data.stages[0] ? 'SEUIL VALIDÉ' : data.sessionBest ? 'À REPRENDRE' : 'NON TENTÉ';
    root.querySelector('[data-progress-target-score]').textContent = data.targetBest ? `${data.targetBest} / 18` : '— / 18';
    root.querySelector('[data-progress-target-label]').textContent = data.stages[1] ? 'SEUIL VALIDÉ' : data.targetBest ? 'À REPRENDRE' : 'NON TENTÉ';
    root.querySelector('[data-progress-validation-score]').textContent = `${data.validation.completed} / 20`;
    root.querySelector('[data-progress-validation-label]').textContent = data.validation.ready ? 'VALIDÉ' : data.validation.completed ? `${data.validation.passed} CONFORMES` : 'À DÉMARRER';
    const bottom = root.querySelector('[data-progress-bottom-action]');
    bottom.href = next.href;
    root.querySelector('[data-progress-bottom-title]').textContent = next.title;
    renderRoute(data, next.index);
    renderSkills(data);
    renderEvidence(data);
    currentReport = report(data, next);
  }

  root.querySelector('[data-progress-refresh]').addEventListener('click', () => {
    render();
    root.querySelector('[data-progress-tool-status]').textContent = 'Preuves locales actualisées.';
  });

  root.querySelector('[data-progress-copy]').addEventListener('click', async () => {
    const status = root.querySelector('[data-progress-tool-status]');
    try {
      await navigator.clipboard.writeText(currentReport);
      status.textContent = 'Bilan copié.';
    } catch (_) {
      const area = document.createElement('textarea');
      area.value = currentReport;
      document.body.append(area);
      area.select();
      document.execCommand('copy');
      area.remove();
      status.textContent = 'Bilan copié.';
    }
  });

  root.querySelector('[data-progress-download]').addEventListener('click', () => {
    const url = URL.createObjectURL(new Blob([currentReport], { type: 'text/plain;charset=utf-8' }));
    const link = document.createElement('a');
    link.href = url;
    link.download = `ict-atlas-progression-${new Date().toISOString().slice(0, 10)}.txt`;
    link.click();
    URL.revokeObjectURL(url);
    root.querySelector('[data-progress-tool-status]').textContent = 'Bilan téléchargé.';
  });

  window.addEventListener('storage', render);
  render();
})();
