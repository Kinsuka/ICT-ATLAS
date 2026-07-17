(() => {
  const root = document.querySelector('[data-forward-gate]');
  if (!root) return;

  const storageKey = 'ict-atlas-forward-gate-v1';
  const defaults = {
    minDecisions: 30,
    minTrades: 20,
    minExpectancy: 0.10,
    maxDrawdown: 6,
    maxErrorRate: 10,
    decisions: 0,
    trades: 0,
    netR: 0,
    drawdown: 0,
    processErrors: 0,
    rulesFrozen: false,
    independent: false,
    costsIncluded: false,
  };
  const fields = [...root.querySelectorAll('[data-forward-field]')];
  let resetTimer;

  function load() {
    try {
      const stored = JSON.parse(localStorage.getItem(storageKey));
      return stored && typeof stored === 'object' ? { ...defaults, ...stored } : { ...defaults };
    } catch (_) { return { ...defaults }; }
  }

  let state = load();

  function number(key) {
    const value = Number.parseFloat(state[key]);
    return Number.isFinite(value) ? value : 0;
  }

  function save(verdict) {
    try { localStorage.setItem(storageKey, JSON.stringify({ ...state, verdict, updatedAt: new Date().toISOString() })); } catch (_) { /* storage can be unavailable */ }
  }

  function syncFields() {
    fields.forEach((field) => {
      const key = field.dataset.forwardField;
      if (field.type === 'checkbox') field.checked = Boolean(state[key]);
      else field.value = state[key];
    });
  }

  function evaluate() {
    const decisions = Math.max(0, number('decisions'));
    const trades = Math.max(0, number('trades'));
    const errors = Math.max(0, number('processErrors'));
    const expectancy = trades > 0 ? number('netR') / trades : null;
    const errorRate = decisions > 0 ? (errors / decisions) * 100 : null;
    const validCounts = trades <= decisions && errors <= decisions;

    const gates = [
      { label: 'Décisions minimum', pass: decisions >= number('minDecisions'), value: `${decisions} / ${number('minDecisions')}` },
      { label: 'Trades éligibles minimum', pass: trades >= number('minTrades') && trades <= decisions, value: `${trades} / ${number('minTrades')}` },
      { label: 'Expectancy nette', pass: expectancy !== null && expectancy >= number('minExpectancy'), value: expectancy === null ? '—' : `${expectancy.toFixed(2)}R` },
      { label: 'Drawdown sous la limite', pass: number('drawdown') <= number('maxDrawdown'), value: `${number('drawdown').toFixed(1)}R / ${number('maxDrawdown').toFixed(1)}R` },
      { label: 'Erreurs de processus', pass: errorRate !== null && errorRate <= number('maxErrorRate') && errors <= decisions, value: errorRate === null ? '—' : `${errorRate.toFixed(1)} %` },
      { label: 'Ruleset inchangé', pass: Boolean(state.rulesFrozen), value: state.rulesFrozen ? 'PROUVÉ' : 'MANQUANT' },
      { label: 'Échantillon indépendant', pass: Boolean(state.independent), value: state.independent ? 'PROUVÉ' : 'MANQUANT' },
      { label: 'Coûts et slippage inclus', pass: Boolean(state.costsIncluded), value: state.costsIncluded ? 'PROUVÉ' : 'MANQUANT' },
    ];

    const enoughSample = gates[0].pass && gates[1].pass;
    const performanceFailed = enoughSample && (expectancy < number('minExpectancy') || number('drawdown') > number('maxDrawdown'));
    const invalidatedSample = decisions > 0 && !state.rulesFrozen;
    const allPassed = gates.every((gate) => gate.pass);
    let verdict = 'correct';
    let label = 'CORRIGER';
    let detail = 'Complète le cadre et l’échantillon avant toute décision de risque.';
    let nextAction = 'Fige le cadre, puis collecte sans modifier le modèle.';

    if (!validCounts) {
      verdict = 'stop';
      label = 'STOP';
      detail = 'Les comptes sont incohérents : trades ou erreurs supérieurs aux décisions.';
      nextAction = 'Corrige le journal source avant d’interpréter la moindre statistique.';
    } else if (performanceFailed || invalidatedSample) {
      verdict = 'stop';
      label = 'STOP';
      detail = invalidatedSample ? 'Le ruleset a changé pendant le bloc : cet échantillon ne valide plus la même hypothèse.' : 'L’edge net ou l’enveloppe de drawdown échoue après atteinte du minimum.';
      nextAction = invalidatedSample ? 'Archive ce bloc. Toute nouvelle version recommence sur un échantillon séparé.' : 'Ne risque rien. Audite le modèle et ne change qu’une variable avant un nouveau test distinct.';
    } else if (allPassed) {
      verdict = 'go';
      label = 'GO PÉDAGOGIQUE';
      detail = 'Les huit portes pré-engagées sont respectées sur ce bloc indépendant.';
      nextAction = 'Si ton plan l’autorise, utilise uniquement son plus petit risque et conserve des règles identiques.';
    } else {
      const firstFailure = gates.find((gate) => !gate.pass);
      nextAction = enoughSample ? `Corrige la porte « ${firstFailure.label} » sans maquiller les autres données.` : `Continue la collecte : prochaine porte incomplète, « ${firstFailure.label} ».`;
    }

    root.dataset.forwardVerdict = verdict;
    const verdictBox = root.querySelector('[data-forward-verdict]');
    verdictBox.dataset.forwardVerdict = verdict;
    root.querySelector('[data-forward-verdict-label]').textContent = label;
    root.querySelector('[data-forward-verdict-detail]').textContent = detail;
    root.querySelector('[data-forward-expectancy]').textContent = expectancy === null ? '—' : `${expectancy.toFixed(2)}R`;
    root.querySelector('[data-forward-error-rate]').textContent = errorRate === null ? '—' : `${errorRate.toFixed(1)} %`;
    root.querySelector('[data-forward-gate-score]').textContent = `${gates.filter((gate) => gate.pass).length} / ${gates.length}`;
    root.querySelector('[data-forward-next-action]').textContent = nextAction;

    const evidence = root.querySelector('[data-forward-evidence]');
    evidence.replaceChildren();
    gates.forEach((gate, index) => {
      const item = document.createElement('article');
      item.className = gate.pass ? 'is-passed' : 'is-failed';
      const numberLabel = document.createElement('span');
      numberLabel.textContent = String(index + 1).padStart(2, '0');
      const body = document.createElement('div');
      const title = document.createElement('strong');
      title.textContent = gate.label;
      const value = document.createElement('small');
      value.textContent = gate.value;
      body.append(title, value);
      const status = document.createElement('em');
      status.textContent = gate.pass ? 'OK' : 'À TRAITER';
      item.append(numberLabel, body, status);
      evidence.append(item);
    });
    save(verdict);
  }

  root.querySelector('[data-forward-form]').addEventListener('input', (event) => {
    const field = event.target.closest('[data-forward-field]');
    if (!field) return;
    state[field.dataset.forwardField] = field.type === 'checkbox' ? field.checked : field.value;
    evaluate();
  });

  const reset = root.querySelector('[data-forward-reset]');
  reset.addEventListener('click', () => {
    if (reset.dataset.armed !== 'true') {
      reset.dataset.armed = 'true';
      reset.textContent = 'Confirmer la réinitialisation';
      clearTimeout(resetTimer);
      resetTimer = setTimeout(() => {
        reset.dataset.armed = 'false';
        reset.textContent = 'Réinitialiser le contrôle';
      }, 5000);
      return;
    }
    clearTimeout(resetTimer);
    state = { ...defaults };
    try { localStorage.removeItem(storageKey); } catch (_) { /* storage can be unavailable */ }
    reset.dataset.armed = 'false';
    reset.textContent = 'Réinitialiser le contrôle';
    syncFields();
    evaluate();
  });

  syncFields();
  evaluate();
})();
