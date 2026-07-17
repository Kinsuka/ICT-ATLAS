(() => {
  const root = document.querySelector('[data-risk-ladder]');
  if (!root) return;

  const storageKey = 'ict-atlas-risk-ladder-v1';
  const forwardKey = 'ict-atlas-forward-gate-v1';
  const defaults = {
    riskCap: 0.25,
    minTrades: 20,
    minNetR: 0,
    maxDrawdown: 3,
    maxProcessErrors: 1,
    trades: 0,
    netR: 0,
    drawdown: 0,
    processErrors: 0,
    dailyStopHits: 0,
    rulesUnchanged: false,
    noScaleUp: false,
  };
  const fields = [...root.querySelectorAll('[data-risk-field]')];
  let resetTimer;

  function readJson(key) {
    try { return JSON.parse(localStorage.getItem(key)); } catch (_) { return null; }
  }

  function load() {
    const stored = readJson(storageKey);
    return stored && typeof stored === 'object' ? { ...defaults, ...stored } : { ...defaults };
  }

  let state = load();

  function number(key) {
    const value = Number.parseFloat(state[key]);
    return Number.isFinite(value) ? value : 0;
  }

  function forwardGo() {
    const stored = readJson(forwardKey);
    return Boolean(stored && stored.verdict === 'go');
  }

  function save(verdict) {
    try {
      localStorage.setItem(storageKey, JSON.stringify({ ...state, verdict, updatedAt: new Date().toISOString() }));
    } catch (_) { /* storage can be unavailable */ }
  }

  function syncFields() {
    fields.forEach((field) => {
      const key = field.dataset.riskField;
      if (field.type === 'checkbox') field.checked = Boolean(state[key]);
      else field.value = state[key];
    });
  }

  function renderGates(gates) {
    const list = root.querySelector('[data-risk-evidence]');
    list.replaceChildren();
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
      status.textContent = gate.pass ? 'OK' : 'BLOCAGE';
      item.append(numberLabel, body, status);
      list.append(item);
    });
  }

  function setLocked() {
    root.dataset.riskVerdict = 'locked';
    root.querySelector('[data-risk-verdict]').dataset.riskVerdict = 'locked';
    root.querySelector('[data-risk-verdict-label]').textContent = 'VERROUILLÉ';
    root.querySelector('[data-risk-verdict-detail]').textContent = 'Le Forward Test Control doit afficher GO pédagogique avant de préparer un bloc de micro-risque.';
    root.querySelector('[data-risk-next-action]').textContent = 'Retourne au forward test : aucune exposition réelle ne doit précéder cette porte.';
    root.querySelector('[data-risk-score]').textContent = '0 / 9';
    root.querySelector('[data-risk-exposure]').textContent = '—';
    root.querySelector('[data-risk-net]').textContent = '—';
    root.querySelector('[data-risk-errors]').textContent = '—';
    renderGates([
      { label: 'GO forward préalable', pass: false, value: 'MANQUANT' },
      { label: 'Risque au minimum prévu', pass: false, value: 'EN ATTENTE' },
      { label: 'Bloc micro-risque', pass: false, value: 'EN ATTENTE' },
      { label: 'Résultat net minimal', pass: false, value: 'EN ATTENTE' },
      { label: 'Aucune montée de taille', pass: false, value: 'EN ATTENTE' },
      { label: 'Stops journaliers', pass: false, value: 'EN ATTENTE' },
      { label: 'Erreurs de processus', pass: false, value: 'EN ATTENTE' },
      { label: 'Drawdown sous plafond', pass: false, value: 'EN ATTENTE' },
      { label: 'Ruleset inchangé', pass: false, value: 'EN ATTENTE' },
    ]);
    save('locked');
  }

  function evaluate() {
    if (!forwardGo()) {
      setLocked();
      return;
    }

    const trades = Math.max(0, number('trades'));
    const processErrors = Math.max(0, number('processErrors'));
    const dailyStopHits = Math.max(0, number('dailyStopHits'));
    const enoughSample = trades >= number('minTrades');
    const gates = [
      { label: 'GO forward préalable', pass: true, value: 'VALIDÉ' },
      { label: 'Risque au minimum prévu', pass: number('riskCap') > 0 && number('riskCap') <= 0.25, value: `${number('riskCap').toFixed(2)} % max` },
      { label: 'Bloc micro-risque complet', pass: enoughSample, value: `${trades} / ${number('minTrades')} trades` },
      { label: 'Résultat net minimal', pass: number('netR') >= number('minNetR'), value: `${number('netR').toFixed(2)}R / ${number('minNetR').toFixed(2)}R` },
      { label: 'Aucune montée de taille', pass: Boolean(state.noScaleUp), value: state.noScaleUp ? 'PROMIS' : 'MANQUANT' },
      { label: 'Zéro stop journalier', pass: dailyStopHits === 0, value: `${dailyStopHits} incident(s)` },
      { label: 'Erreurs sous plafond', pass: processErrors <= number('maxProcessErrors'), value: `${processErrors} / ${number('maxProcessErrors')}` },
      { label: 'Drawdown sous plafond', pass: number('drawdown') <= number('maxDrawdown'), value: `${number('drawdown').toFixed(1)}R / ${number('maxDrawdown').toFixed(1)}R` },
      { label: 'Ruleset inchangé', pass: Boolean(state.rulesUnchanged), value: state.rulesUnchanged ? 'VALIDÉ' : 'MANQUANT' },
    ];
    const netValid = number('netR') >= number('minNetR');
    const hardFailure = dailyStopHits > 0
      || processErrors > number('maxProcessErrors')
      || number('drawdown') > number('maxDrawdown')
      || (enoughSample && !netValid)
      || number('riskCap') > 0.25;
    const allPassed = gates.every((gate) => gate.pass) && netValid;

    let verdict = 'collect';
    let label = 'COLLECTER';
    let detail = 'Le forward est validé ; complète le bloc au risque minimum sans changer les règles.';
    let nextAction = 'Continue uniquement ce bloc micro-risque, sans augmenter la taille ni compenser une perte.';

    if (hardFailure) {
      verdict = 'pause';
      label = 'PAUSE';
      detail = 'Une limite de protection est touchée : le bloc ne peut pas servir de feu vert opérationnel.';
      nextAction = 'Stoppe le bloc, archive les données et corrige la cause avant toute nouvelle exposition.';
    } else if (allPassed) {
      verdict = 'stabilize';
      label = 'STABILISER';
      detail = 'Le bloc respecte les protections. La prochaine décision n’est pas de grossir vite, mais de répéter proprement.';
      nextAction = 'Refais un bloc identique ou maintiens le plus petit risque ; aucune montée sans nouveau seuil écrit.';
    } else {
      const firstFailure = gates.find((gate) => !gate.pass);
      if (enoughSample && !netValid) {
        nextAction = 'Résultat net insuffisant : pas de montée, pas de challenge, audit obligatoire.';
      } else if (firstFailure) {
        nextAction = `Traite d’abord la porte « ${firstFailure.label} ».`;
      }
    }

    root.dataset.riskVerdict = verdict;
    const verdictBox = root.querySelector('[data-risk-verdict]');
    verdictBox.dataset.riskVerdict = verdict;
    root.querySelector('[data-risk-verdict-label]').textContent = label;
    root.querySelector('[data-risk-verdict-detail]').textContent = detail;
    root.querySelector('[data-risk-next-action]').textContent = nextAction;
    root.querySelector('[data-risk-score]').textContent = `${gates.filter((gate) => gate.pass).length} / ${gates.length}`;
    root.querySelector('[data-risk-exposure]').textContent = `${number('riskCap').toFixed(2)} %`;
    root.querySelector('[data-risk-net]').textContent = `${number('netR').toFixed(2)}R`;
    root.querySelector('[data-risk-errors]').textContent = `${processErrors}`;
    renderGates(gates);
    save(verdict);
  }

  root.querySelector('[data-risk-form]').addEventListener('input', (event) => {
    const field = event.target.closest('[data-risk-field]');
    if (!field) return;
    state[field.dataset.riskField] = field.type === 'checkbox' ? field.checked : field.value;
    evaluate();
  });

  const reset = root.querySelector('[data-risk-reset]');
  reset.addEventListener('click', () => {
    if (reset.dataset.armed !== 'true') {
      reset.dataset.armed = 'true';
      reset.textContent = 'Confirmer la réinitialisation';
      clearTimeout(resetTimer);
      resetTimer = setTimeout(() => {
        reset.dataset.armed = 'false';
        reset.textContent = 'Réinitialiser';
      }, 5000);
      return;
    }
    clearTimeout(resetTimer);
    state = { ...defaults };
    try { localStorage.removeItem(storageKey); } catch (_) { /* storage can be unavailable */ }
    reset.dataset.armed = 'false';
    reset.textContent = 'Réinitialiser';
    syncFields();
    evaluate();
  });

  window.addEventListener('ict-atlas-forward-updated', evaluate);
  syncFields();
  evaluate();
})();
