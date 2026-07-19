(() => {
  const cockpit = document.querySelector('[data-session-cockpit]');
  if (!cockpit) return;

  const storageKey = 'ict-atlas-session-cockpit-v1';
  const fields = [...cockpit.querySelectorAll('[data-cockpit-field]')];
  const verdictLabel = cockpit.querySelector('[data-cockpit-verdict-label]');
  const verdictDetail = cockpit.querySelector('[data-cockpit-verdict-detail]');
  const nextAction = cockpit.querySelector('[data-cockpit-next-action]');
  const score = cockpit.querySelector('[data-cockpit-score]');
  const r1Label = cockpit.querySelector('[data-cockpit-r1]');
  const r2Label = cockpit.querySelector('[data-cockpit-r2]');
  const riskDistanceLabel = cockpit.querySelector('[data-cockpit-risk-distance]');
  const evidence = cockpit.querySelector('[data-cockpit-evidence]');
  const brief = cockpit.querySelector('[data-cockpit-brief]');
  const copyButton = cockpit.querySelector('[data-cockpit-copy]');
  const downloadButton = cockpit.querySelector('[data-cockpit-download]');
  const resetButton = cockpit.querySelector('[data-cockpit-reset]');

  const defaults = {
    date: new Date().toISOString().slice(0, 10),
    riskCap: '0.25',
    minR: '1.50',
    eventOccurred: false,
    triggerConfirmed: false,
  };

  const gateDefinitions = [
    ['context', '01 · CONTEXTE', 'Direction, environnement et localisation cohérents.'],
    ['map', '02 · CARTE', 'BSL et SSL externes identifiées avant la recherche d’entrée.'],
    ['target', '03 · DOL', 'Destination ouverte, alignée avec le sens du scénario.'],
    ['narrative', '04 · NARRATIVE', 'POI, scénario si/alors et invalidation écrits.'],
    ['event', '05 · ÉVÉNEMENT', 'Le marché a livré l’événement exigé par le plan.'],
    ['trigger', '06 · TRIGGER', 'Le modèle d’exécution choisi est confirmé.'],
    ['order', '07 · ORDRE', 'Géométrie entrée/stop/TP valide et R disponible suffisant.'],
    ['risk', '08 · RISQUE', 'Fenêtre, news, limites et taille respectent le plan.'],
  ];

  function load() {
    try {
      const stored = JSON.parse(localStorage.getItem(storageKey) || '{}');
      return stored && typeof stored === 'object' ? { ...defaults, ...stored } : { ...defaults };
    } catch {
      return { ...defaults };
    }
  }

  function readForm() {
    return fields.reduce((values, field) => {
      values[field.dataset.cockpitField] = field.type === 'checkbox' ? field.checked : field.value.trim();
      return values;
    }, {});
  }

  function writeForm(values) {
    fields.forEach((field) => {
      const value = values[field.dataset.cockpitField];
      if (field.type === 'checkbox') field.checked = Boolean(value);
      else if (value !== undefined && value !== null) field.value = String(value);
    });
  }

  function number(value) {
    const parsed = Number.parseFloat(value);
    return Number.isFinite(parsed) ? parsed : NaN;
  }

  function calculate(values) {
    const entry = number(values.entry);
    const stop = number(values.stop);
    const tp1 = number(values.tp1);
    const tp2 = number(values.tp2);
    const minR = number(values.minR);
    const plannedRisk = number(values.plannedRisk);
    const riskCap = number(values.riskCap);
    const riskDistance = Number.isFinite(entry) && Number.isFinite(stop) ? Math.abs(entry - stop) : NaN;
    const r1 = riskDistance > 0 && Number.isFinite(tp1) ? Math.abs(tp1 - entry) / riskDistance : NaN;
    const r2 = riskDistance > 0 && Number.isFinite(tp2) ? Math.abs(tp2 - entry) / riskDistance : NaN;
    const longGeometry = values.direction === 'long' && stop < entry && entry < tp1 && tp1 <= tp2;
    const shortGeometry = values.direction === 'short' && stop > entry && entry > tp1 && tp1 >= tp2;
    return { entry, stop, tp1, tp2, minR, plannedRisk, riskCap, riskDistance, r1, r2, geometry: longGeometry || shortGeometry };
  }

  function requiredMissing(values) {
    const required = [
      ['asset', 'Renseigne l’actif.'],
      ['date', 'Choisis la date de session.'],
      ['session', 'Choisis la session travaillée.'],
      ['direction', 'Choisis un sens de travail.'],
      ['environment', 'Classe l’environnement.'],
      ['location', 'Localise le prix dans la range active.'],
      ['bsl', 'Écris la BSL externe visible.'],
      ['ssl', 'Écris la SSL externe visible.'],
      ['dol', 'Choisis la DOL primaire.'],
      ['dolStatus', 'Déclare si la DOL est encore ouverte.'],
      ['obstacle', 'Évalue l’obstacle avant TP1.'],
      ['poi', 'Écris le POI de travail.'],
      ['scenario', 'Écris le scénario si/alors.'],
      ['narrativeInvalidation', 'Écris ce qui invalide la narrative.'],
      ['eventModel', 'Choisis l’événement attendu.'],
      ['triggerModel', 'Choisis un trigger unique.'],
      ['entry', 'Renseigne l’entrée envisagée.'],
      ['stop', 'Renseigne le stop structurel.'],
      ['tp1', 'Renseigne TP1.'],
      ['tp2', 'Renseigne TP2.'],
      ['plannedRisk', 'Renseigne le risque planifié.'],
      ['riskCap', 'Renseigne le plafond de risque du plan.'],
      ['minR', 'Renseigne le R minimal testé.'],
      ['window', 'Déclare l’état de la fenêtre horaire.'],
      ['news', 'Déclare l’état des news.'],
      ['dailyStop', 'Déclare l’état du stop journalier.'],
      ['tradeLimit', 'Déclare l’état de la limite de trades.'],
      ['ruleset', 'Confirme l’état du ruleset.'],
    ];
    return required.filter(([key]) => values[key] === '').map(([, message]) => message);
  }

  function evaluate(values) {
    const metrics = calculate(values);
    const missing = requiredMissing(values);
    const directionTargetAligned = (values.direction === 'long' && values.dol === 'bsl')
      || (values.direction === 'short' && values.dol === 'ssl');
    const locationAligned = (values.direction === 'long' && values.location === 'discount')
      || (values.direction === 'short' && values.location === 'premium');
    const targetOpen = values.dolStatus === 'open';
    const targetClear = values.obstacle === 'clear';
    const narrativeReady = Boolean(values.poi && values.scenario && values.narrativeInvalidation);
    const eventReady = Boolean(values.eventModel && values.eventOccurred);
    const triggerReady = Boolean(values.triggerModel && values.triggerConfirmed);
    const paymentReady = metrics.geometry && Number.isFinite(metrics.r2) && Number.isFinite(metrics.minR) && metrics.r2 >= metrics.minR;
    const riskSized = Number.isFinite(metrics.plannedRisk)
      && Number.isFinite(metrics.riskCap)
      && metrics.plannedRisk > 0
      && metrics.riskCap > 0
      && metrics.plannedRisk <= metrics.riskCap;
    const timingReady = values.window === 'inside';
    const newsReady = values.news === 'clear';
    const limitsReady = values.dailyStop === 'intact' && values.tradeLimit === 'intact';
    const rulesReady = values.ruleset === 'same';
    const contextReady = Boolean(values.direction && values.environment && values.location)
      && values.environment !== 'consolidation'
      && values.location !== 'equilibrium'
      && values.location !== 'unclear'
      && locationAligned;

    const gates = {
      context: contextReady,
      map: Boolean(values.bsl && values.ssl),
      target: directionTargetAligned && targetOpen && targetClear,
      narrative: narrativeReady,
      event: eventReady,
      trigger: triggerReady,
      order: paymentReady,
      risk: riskSized && timingReady && newsReady && limitsReady && rulesReady,
    };

    if (missing.length) {
      return {
        verdict: 'incomplete',
        label: 'À RENSEIGNER',
        detail: `${missing.length} information${missing.length > 1 ? 's' : ''} manque${missing.length > 1 ? 'nt' : ''} avant toute décision.`,
        next: missing[0],
        gates,
        metrics,
        blockers: [],
        waits: [],
      };
    }

    const blockers = [];
    if (values.environment === 'consolidation') blockers.push('Consolidation déclarée : attendre la manipulation puis re-cartographier.');
    if (values.location === 'equilibrium' || values.location === 'unclear') blockers.push('Localisation inexploitable : prix à l’équilibre ou range mal définie.');
    if (!locationAligned) blockers.push('La localisation premium/discount n’est pas alignée avec le sens choisi.');
    if (!directionTargetAligned) blockers.push('La DOL choisie ne correspond pas au sens du scénario.');
    if (!targetOpen) blockers.push(values.dolStatus === 'consumed' ? 'La DOL primaire est déjà consommée.' : 'Le statut de la DOL reste incertain.');
    if (!targetClear) blockers.push('Un obstacle structurel bloque le trajet avant TP1.');
    if (!metrics.geometry) blockers.push('La géométrie entrée → stop → TP1 → TP2 est invalide.');
    if (metrics.geometry && (!Number.isFinite(metrics.r2) || metrics.r2 < metrics.minR)) blockers.push('Le R vers TP2 est inférieur au minimum du modèle.');
    if (!riskSized) blockers.push('Le risque planifié dépasse le plafond ou contient une valeur invalide.');
    if (values.window === 'outside') blockers.push('La fenêtre de trading est terminée.');
    if (values.news === 'blocked') blockers.push('La règle news du plan bloque toute nouvelle entrée.');
    if (values.dailyStop === 'hit') blockers.push('Le stop journalier est atteint.');
    if (values.tradeLimit === 'hit') blockers.push('La limite de trades est atteinte.');
    if (values.ruleset === 'changed') blockers.push('Le ruleset a été modifié pendant la session.');

    if (blockers.length) {
      return {
        verdict: 'no-trade',
        label: 'NO TRADE',
        detail: `${blockers.length} porte${blockers.length > 1 ? 's' : ''} de protection bloque${blockers.length > 1 ? 'nt' : ''} l’ordre.`,
        next: blockers[0],
        gates,
        metrics,
        blockers,
        waits: [],
      };
    }

    const waits = [];
    if (values.window === 'before') waits.push('Attendre l’ouverture de la fenêtre autorisée.');
    if (values.news === 'pending') waits.push('Attendre la publication puis revalider le contexte.');
    if (!values.eventOccurred) waits.push(`Attendre : ${values.eventModel}.`);
    if (!values.triggerConfirmed) waits.push(`Après l’événement seulement, attendre : ${values.triggerModel}.`);

    if (waits.length) {
      return {
        verdict: 'wait',
        label: 'ATTENDRE',
        detail: 'La narrative est préparée, mais le marché n’a pas encore ouvert toutes les portes.',
        next: waits[0],
        gates,
        metrics,
        blockers: [],
        waits,
      };
    }

    return {
      verdict: 'authorized',
      label: 'AUTORISÉ',
      detail: 'Les huit portes du plan sont ouvertes. La permission n’est jamais une obligation de cliquer.',
      next: 'Si le prix reste dans les niveaux prévus, exécuter uniquement le modèle écrit et sa taille calculée.',
      gates,
      metrics,
      blockers: [],
      waits: [],
    };
  }

  function metric(value, suffix = 'R') {
    return Number.isFinite(value) ? `${value.toFixed(2)}${suffix}` : '—';
  }

  function textFor(values, result) {
    const m = result.metrics;
    const direction = values.direction === 'long' ? 'LONG' : values.direction === 'short' ? 'SHORT' : '—';
    const dol = values.dol === 'bsl' ? 'BSL' : values.dol === 'ssl' ? 'SSL' : '—';
    return [
      'ICT ATLAS · PLAN DE SESSION V92',
      `Date : ${values.date || '—'} | Actif : ${values.asset || '—'} | Session : ${values.session || '—'}`,
      `Verdict : ${result.label}`,
      '',
      `01 CONTEXTE · ${direction} | ${values.environment || '—'} | ${values.location || '—'}`,
      `02 CARTE · BSL : ${values.bsl || '—'} | SSL : ${values.ssl || '—'}`,
      `03 DOL · ${dol} | statut : ${values.dolStatus || '—'} | obstacle : ${values.obstacle || '—'}`,
      `04 NARRATIVE · POI : ${values.poi || '—'}`,
      `Scénario : ${values.scenario || '—'}`,
      `Invalidation narrative : ${values.narrativeInvalidation || '—'}`,
      `05 ÉVÉNEMENT · ${values.eventModel || '—'} | observé : ${values.eventOccurred ? 'oui' : 'non'}`,
      `06 TRIGGER · ${values.triggerModel || '—'} | confirmé : ${values.triggerConfirmed ? 'oui' : 'non'}`,
      `07 ORDRE · entrée ${values.entry || '—'} | stop ${values.stop || '—'} | TP1 ${values.tp1 || '—'} | TP2 ${values.tp2 || '—'}`,
      `Risque prix : ${metric(m.riskDistance, '')} | TP1 : ${metric(m.r1)} | TP2 : ${metric(m.r2)} | minimum : ${values.minR || '—'}R`,
      `08 RISQUE · planifié ${values.plannedRisk || '—'}% | plafond ${values.riskCap || '—'}%`,
      `Fenêtre : ${values.window || '—'} | News : ${values.news || '—'} | Stop journalier : ${values.dailyStop || '—'} | Limite trades : ${values.tradeLimit || '—'}`,
      '',
      `PROCHAINE ACTION · ${result.next}`,
      'Ce document structure une décision pédagogique. Il ne constitue ni un conseil financier ni une garantie de résultat.',
    ].join('\n');
  }

  function renderEvidence(result) {
    evidence.innerHTML = gateDefinitions.map(([key, title, description]) => {
      const passed = result.gates[key];
      const status = passed ? 'OUVERTE' : result.verdict === 'incomplete' ? 'INCOMPLÈTE' : result.verdict === 'wait' && ['event', 'trigger', 'risk'].includes(key) ? 'EN ATTENTE' : 'FERMÉE';
      return `<article class="${passed ? 'is-passed' : status === 'EN ATTENTE' ? 'is-waiting' : 'is-failed'}"><span>${title}</span><strong>${status}</strong><p>${description}</p></article>`;
    }).join('');
  }

  function update() {
    const values = readForm();
    const result = evaluate(values);
    const passed = Object.values(result.gates).filter(Boolean).length;
    cockpit.dataset.verdict = result.verdict;
    verdictLabel.textContent = result.label;
    verdictDetail.textContent = result.detail;
    nextAction.textContent = result.next;
    score.textContent = `${passed} / 8`;
    r1Label.textContent = metric(result.metrics.r1);
    r2Label.textContent = metric(result.metrics.r2);
    riskDistanceLabel.textContent = metric(result.metrics.riskDistance, '');
    renderEvidence(result);
    brief.textContent = textFor(values, result);
    copyButton.disabled = result.verdict === 'incomplete';
    downloadButton.disabled = result.verdict === 'incomplete';
    localStorage.setItem(storageKey, JSON.stringify(values));
    window.dispatchEvent(new CustomEvent('ict-atlas-session-cockpit-updated', { detail: { verdict: result.verdict } }));
  }

  async function copyBrief() {
    const value = brief.textContent;
    try {
      await navigator.clipboard.writeText(value);
    } catch {
      const helper = document.createElement('textarea');
      helper.value = value;
      helper.style.position = 'fixed';
      helper.style.opacity = '0';
      document.body.append(helper);
      helper.select();
      document.execCommand('copy');
      helper.remove();
    }
    copyButton.textContent = 'Plan copié';
    window.setTimeout(() => { copyButton.textContent = 'Copier le plan'; }, 1800);
  }

  function downloadBrief() {
    const values = readForm();
    const safeAsset = (values.asset || 'session').replace(/[^a-z0-9_-]+/gi, '-').toLowerCase();
    const blob = new Blob([brief.textContent], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `plan-session-${values.date || 'date'}-${safeAsset}.txt`;
    document.body.append(link);
    link.click();
    link.remove();
    URL.revokeObjectURL(url);
  }

  writeForm(load());
  fields.forEach((field) => {
    field.addEventListener('input', update);
    field.addEventListener('change', update);
  });
  copyButton.addEventListener('click', copyBrief);
  downloadButton.addEventListener('click', downloadBrief);
  resetButton.addEventListener('click', () => {
    if (resetButton.dataset.armed !== 'true') {
      resetButton.dataset.armed = 'true';
      resetButton.textContent = 'Confirmer la remise à zéro';
      window.setTimeout(() => {
        resetButton.dataset.armed = 'false';
        resetButton.textContent = 'Réinitialiser le cockpit';
      }, 4000);
      return;
    }
    localStorage.removeItem(storageKey);
    fields.forEach((field) => {
      if (field.type === 'checkbox') field.checked = false;
      else field.value = defaults[field.dataset.cockpitField] || '';
    });
    resetButton.dataset.armed = 'false';
    resetButton.textContent = 'Réinitialiser le cockpit';
    update();
  });
  update();
})();
