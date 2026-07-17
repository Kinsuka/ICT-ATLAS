(() => {
  const simulators = [...document.querySelectorAll('[data-session-simulator]')];
  if (!simulators.length) return;

  simulators.forEach((simulator) => {
    const stages = [...simulator.querySelectorAll('[data-sim-stage]')];
    const progress = simulator.querySelector('[role="progressbar"]');
    const progressBar = simulator.querySelector('[data-sim-progress-bar]');
    const progressLabel = simulator.querySelector('[data-sim-progress-label]');
    const marketState = simulator.querySelector('[data-sim-market-state]');
    const complete = simulator.querySelector('[data-sim-complete]');
    const reset = simulator.querySelector('[data-sim-reset]');

    function setProgress(step) {
      const safeStep = Math.min(Math.max(step, 1), stages.length);
      const currentStage = stages[safeStep - 1];
      simulator.dataset.step = String(safeStep);
      progress.setAttribute('aria-valuemax', String(stages.length));
      progress.setAttribute('aria-valuenow', String(safeStep));
      progressBar.style.width = `${(safeStep / stages.length) * 100}%`;
      progressLabel.textContent = `Décision ${safeStep} sur ${stages.length}`;
      marketState.textContent = currentStage.dataset.marketState || `Étape ${safeStep}`;
    }

    function unlockStage(index) {
      const stage = stages[index];
      if (!stage) return;
      stage.hidden = false;
      stage.classList.add('is-active');
      const fallbackLayer = Math.min(Math.max(index - 1, 1), 5);
      const layerToReveal = stage.dataset.revealLayer || String(fallbackLayer);
      simulator.querySelectorAll(`[data-sim-layer="${layerToReveal}"]`).forEach((layer) => {
        layer.classList.add('is-visible');
      });
      setProgress(index + 1);
    }

    stages.forEach((stage, index) => {
      const inputs = [...stage.querySelectorAll('input[type="radio"]')];
      const validate = stage.querySelector('[data-sim-validate]');
      const feedback = stage.querySelector('[data-sim-feedback]');

      inputs.forEach((input) => {
        input.addEventListener('change', () => {
          validate.disabled = false;
        });
      });

      validate.addEventListener('click', () => {
        const selected = inputs.find((input) => input.checked);
        if (!selected) return;

        const isCorrect = selected.dataset.correct === 'true';
        stage.classList.toggle('is-correct', isCorrect);
        stage.classList.toggle('is-wrong', !isCorrect);
        selected.closest('label').classList.add(isCorrect ? 'is-selected-correct' : 'is-selected-wrong');
        stage.querySelector('input[data-correct="true"]').closest('label').classList.add('is-answer');
        feedback.hidden = false;
        inputs.forEach((input) => { input.disabled = true; });
        validate.disabled = true;
        validate.hidden = true;

        if (index < stages.length - 1) {
          unlockStage(index + 1);
        } else {
          simulator.querySelectorAll('[data-sim-layer]').forEach((layer) => layer.classList.add('is-visible'));
          complete.hidden = false;
          simulator.classList.add('is-complete');
          progressLabel.textContent = `${stages.length} décisions terminées`;
          marketState.textContent = simulator.dataset.completeState || 'Débrief terminé';
        }
      });
    });

    reset.addEventListener('click', () => {
      stages.forEach((stage, index) => {
        stage.hidden = index !== 0;
        stage.classList.toggle('is-active', index === 0);
        stage.classList.remove('is-correct', 'is-wrong');
        const feedback = stage.querySelector('[data-sim-feedback]');
        const validate = stage.querySelector('[data-sim-validate]');
        feedback.hidden = true;
        validate.hidden = false;
        validate.disabled = true;
        stage.querySelectorAll('input[type="radio"]').forEach((input) => {
          input.checked = false;
          input.disabled = false;
        });
        stage.querySelectorAll('.sim-options label').forEach((label) => {
          label.classList.remove('is-answer', 'is-selected-correct', 'is-selected-wrong');
        });
      });
      simulator.querySelectorAll('[data-sim-layer]').forEach((layer, index) => {
        layer.classList.toggle('is-visible', index === 0);
      });
      complete.hidden = true;
      simulator.classList.remove('is-complete');
      setProgress(1);
      simulator.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });

    setProgress(1);
  });
})();
