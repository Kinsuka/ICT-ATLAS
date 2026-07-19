(() => {
  const lab = document.querySelector('[data-historical-lab]');
  if (!lab) return;

  const storageKey = 'ict-atlas-historical-replay-v1';
  const ns = 'http://www.w3.org/2000/svg';
  const price = new Intl.NumberFormat('fr-FR', { maximumFractionDigits: 0 });

  const cases = [
    {
      id: 'hist-01',
      code: 'HIST-01',
      title: 'Le sommet est pris, puis le prix réintègre',
      date: '5 mars 2024',
      start: '12:00',
      freezeIndex: 13,
      freezeLabel: 'après la bougie 15:15–15:30 UTC',
      archetype: 'Sweep haut · déplacement baissier',
      context: [
        ['PDH', '68 603 · encore ouverte avant le sweep'],
        ['PDL', '62 300 · liquidité externe sous le prix'],
        ['Gel', '67 271 · après réintégration'],
      ],
      levels: [
        { label: 'PDH 68 603', value: 68602.98, tone: 'event', plot: true },
        { label: 'PDL 62 300 · hors écran', value: 62300, tone: 'target', plot: false },
      ],
      candles: [[66701.75,67083.74,66619.18,67078.63],[67088.97,67160.07,66886.12,66981.95],[66981.95,67262.82,66900.93,67170.45],[67165.08,67414.13,67071.39,67401.09],[67401.08,67891.02,67373.36,67878.23],[67878.62,68095.64,67690.59,67714.22],[67711.14,67939.05,67554.7,67881.35],[67884.41,67920,67604.98,67834.24],[67830.83,67870.15,67442.38,67567.44],[67567.44,67740,67301.52,67633.54],[67635.02,68524.99,67337,68460.75],[68464.11,68950,68300.8,68846.99],[68846.99,69324.58,67486.04,68406],[68405.99,68521.93,67188.76,67271.35],[67265.22,67456.18,66461.29,66904.99],[66912.61,67437.33,66786.24,66786.24],[66793.67,67000,64507.22,65386.92],[65373.74,65827.54,64750,65783.55],[65768,65967.71,65014,65063.42],[65042.79,65469.62,64819.2,65462.99],[65467.14,65469.61,63300,64170.75],[64175.54,64776.99,63891.42,64421.71],[64421.7,64996.58,64191,64989.29],[64987.65,65654.76,64866.12,65606.63],[65606.48,65611.53,65032.71,65162.6],[65158.93,65245.98,64559.65,64600.93],[64592.25,64810.86,64456.39,64514.48],[64514.48,64585.8,63704.82,64007.34],[64009.79,64283.99,63172.63,63419.18],[63419.17,63488.12,62471.81,63234.31],[63232.81,63305.24,61538.99,62305.76],[62298.23,62393.55,59224.68,61473.99],[61473.1,63179.66,61266.57,63135.84]],
      questions: [
        {
          key: 'state',
          prompt: 'Quelle information domine au moment du gel ?',
          options: [
            ['breakout', 'Le passage au-dessus du PDH confirme un breakout haussier.'],
            ['sweep', 'Le PDH est pris, puis le prix réintègre avec déplacement baissier.', true],
            ['fvg', 'Une zone locale suffit à vendre, même sans la prise du PDH.'],
          ],
          explanation: 'La séquence utile est prise de BSL → rejet → clôture sous le niveau → expansion baissière. Le sweep seul ne suffisait pas.',
        },
        {
          key: 'dol',
          prompt: 'Quelle destination reste logique ?',
          options: [
            ['high', 'Le nouveau high à 69 325.'],
            ['pdl', 'La liquidité sous 66 619, puis le PDL à 62 300 si la livraison continue.', true],
            ['none', 'Aucune cible : un rejet doit être tradé sans TP.'],
          ],
          explanation: 'Le prix vient de payer la liquidité haute. Les lows visibles puis le PDL constituent une hiérarchie, pas une promesse d’atteinte.',
        },
        {
          key: 'execution',
          prompt: 'Que faire après cette grande expansion ?',
          options: [
            ['chase', 'Vendre immédiatement au marché pour ne pas rater le mouvement.'],
            ['pullback', 'Attendre un pullback autorisé ; sinon classer analyse correcte sans ordre.', true],
            ['buy', 'Acheter parce que le prix est déjà descendu.'],
          ],
          explanation: 'La direction peut être cohérente et l’entrée mauvaise. Une clôture étendue réduit le R disponible et augmente le risque de chase.',
        },
        {
          key: 'invalidation',
          prompt: 'Quelle invalidation respecte la causalité ?',
          options: [
            ['fixed', 'Un stop fixe de 100 dollars, quelle que soit la structure.'],
            ['sweep-zone', 'Une acceptation durable au-dessus de la zone du sweep et du high 69 325.', true],
            ['tp', 'Le trade est invalidé si TP1 n’est pas touché en une bougie.'],
          ],
          explanation: 'L’idée vient du rejet de la liquidité haute. Une réacceptation au-dessus de cette zone détruirait cette lecture.',
        },
      ],
      correction: {
        classification: 'Lecture baissière valide · entrée à requalifier',
        observation: 'Après le gel, le prix prolonge fortement vers les liquidités inférieures. Ce résultat ne transforme pas la bougie étendue du gel en bonne entrée.',
        action: 'En replay, cherche le premier retracement qui conserve l’invalidation structurelle et recalcule le R vers chaque low avant de simuler un ordre.',
      },
    },
    {
      id: 'hist-02',
      code: 'HIST-02',
      title: 'La direction est juste, mais la DOL est déjà payée',
      date: '14 mars 2024',
      start: '12:00',
      freezeIndex: 13,
      freezeLabel: 'après la bougie 15:15–15:30 UTC',
      archetype: 'PDL consommée · anti-chase',
      context: [
        ['PDH', '73 710 · au-dessus du prix'],
        ['PDL', '71 337 · déjà traversée au gel'],
        ['Gel', '70 777 · expansion sous le PDL'],
      ],
      levels: [
        { label: 'PDH 73 710', value: 73709.99, tone: 'event', plot: false },
        { label: 'PDL 71 337', value: 71337.3, tone: 'target', plot: true },
      ],
      candles: [[72926.37,73096.88,72850.53,72987.03],[72987.03,72990.35,72470.03,72811.86],[72811.85,72820.67,72560,72744.33],[72744.33,72902.87,72639.72,72867.02],[72867.02,72958,72532.34,72576.17],[72575.16,72735.44,72354.86,72575.96],[72583.15,72688.88,71725,72116.8],[72116.79,72239.2,71441.49,71897.41],[71895.33,72202.54,71700.24,71996.04],[71996.04,72531.93,71965.51,72169.66],[72170.08,72233.94,71661.78,71766.81],[71767.89,71848.46,71155.3,71666.43],[71665.97,72062.84,71550.14,71915.01],[71917.82,71971.04,70685.97,70777.15],[70769.07,71171.21,70501.11,71013.64],[71012.37,71259.38,70745.67,70817.79],[70821.95,71125.25,70277.66,70480.55],[70478.52,70660,70122.22,70259.31],[70248.35,70875.78,69813.74,70700.57],[70700.57,71408.54,70689.43,71281.06],[71281.06,71408.89,70965.24,71164.72],[71165.4,71206.97,70643.75,70754.76],[70754.72,71131.98,70656.54,70845.84],[70845.05,71123.8,70658.25,71000.92],[71000.43,71006.82,70466,70568.47],[70572.95,70698.42,70253.51,70569.61],[70573.11,70622.57,70278.23,70404.43],[70402.62,70433.9,69300,70074.37],[70072.07,70428.86,69671.05,69996.56],[69996.55,70179.65,69361.59,69564.82],[69568.58,69587.81,68454.47,68834.36],[68834.37,69772.99,68791.81,69260],[69282.24,70155,69168.74,70070.18]],
      questions: [
        {
          key: 'state',
          prompt: 'Que dit objectivement la clôture du gel ?',
          options: [
            ['bullish', 'Le rejet du low garantit un retournement haussier.'],
            ['bearish', 'Le prix a livré une expansion baissière et traversé le PDL.', true],
            ['entry', 'Le PDL traversé est automatiquement une nouvelle entrée short.'],
          ],
          explanation: 'Le déplacement baissier est réel. Mais reconnaître la direction ne répond pas encore à la question du prix d’entrée.',
        },
        {
          key: 'dol',
          prompt: 'Quel est le statut du DOL initial ?',
          options: [
            ['open', 'Le PDL à 71 337 est encore ouvert.'],
            ['paid', 'Le PDL à 71 337 est déjà consommé ; une nouvelle cible doit être justifiée.', true],
            ['irrelevant', 'La DOL ne sert jamais à filtrer une entrée.'],
          ],
          explanation: 'Le PDL n’est plus une récompense future : il a été traversé. Continuer à vendre exige une nouvelle carte de liquidité et un nouveau R.',
        },
        {
          key: 'execution',
          prompt: 'Quelle décision évite la poursuite de prix ?',
          options: [
            ['sell', 'Vendre la clôture baissière parce que la tendance est visible.'],
            ['remap', 'Ne pas poursuivre : attendre un retracement et re-cartographier une cible encore ouverte.', true],
            ['reverse', 'Acheter immédiatement contre le déplacement.'],
          ],
          explanation: 'Le protocole impose cible → invalidation → R avant l’ordre. Ici, la cible initiale est déjà payée et la bougie est étendue.',
        },
        {
          key: 'classification',
          prompt: 'Comment classer correctement la situation ?',
          options: [
            ['missed', 'Trade raté : il fallait absolument participer.'],
            ['analysis-no-order', 'Analyse directionnelle correcte, ordre non autorisé au prix du gel.', true],
            ['loss', 'Perte conforme, même sans avoir exécuté.'],
          ],
          explanation: 'Ne pas entrer ne rend pas l’analyse fausse. Cette séparation protège contre le FOMO et l’évaluation par le résultat futur.',
        },
      ],
      correction: {
        classification: 'Analyse correcte · ordre non autorisé au gel',
        observation: 'Le prix continue plus bas après plusieurs rotations. Le mouvement futur ne rend pas rationnelle une vente prise après consommation du PDL sans nouvelle cible écrite.',
        action: 'Fige le graphique au gel, masque le futur, puis exige une nouvelle DOL et un R mesurable avant tout scénario de continuation.',
      },
    },
    {
      id: 'hist-03',
      code: 'HIST-03',
      title: 'La liquidité basse a été traitée avant le displacement',
      date: '20 mars 2024',
      start: '12:00',
      freezeIndex: 21,
      freezeLabel: 'après la bougie 17:15–17:30 UTC',
      archetype: 'PDL sweep · reversal haussier',
      context: [
        ['PDL', '61 506 · sweep à 05:30 UTC'],
        ['PDH', '68 136 · encore ouverte au gel'],
        ['Gel', '64 099 · après displacement haussier'],
      ],
      levels: [
        { label: 'PDL 61 506', value: 61506, tone: 'event', plot: true },
        { label: 'PDH 68 136 · hors écran', value: 68136.39, tone: 'target', plot: false },
      ],
      candles: [[63355.24,63884,63133.01,63766.43],[63761.57,64328.26,63655.79,64000.34],[64000.34,64197.62,63816.77,63980.04],[63990.62,64068.88,63765.8,64043.57],[64034.51,64046.69,63464.76,63522.71],[63529.94,63705.14,63388.74,63415.71],[63415.71,63782.52,63037.87,63575.62],[63583.94,63845.45,63347.04,63596.08],[63584.56,63981.13,63431.69,63799.45],[63801.47,64199.76,63792.71,64160.46],[64158.83,64319.75,63955.56,64043.02],[64043.03,64360.64,63960.72,64241.66],[64241.33,64414.39,63955.52,64160.31],[64160.04,64170.58,63714.11,63931.48],[63933.09,63983.94,63517.35,63517.79],[63515.53,63744.45,63381.43,63598.26],[63590.02,63787.14,63276.4,63690.64],[63687.03,63760.22,62326.59,62624.63],[62629.34,63209.32,62050.5,63070.57],[63069.98,63412.33,62943.53,63104.13],[63109.93,63685.74,62835.85,63652.83],[63654.11,64766.54,63628.08,64098.64],[64091.18,64468.36,63985.14,64137.37],[64137.37,64265.46,63852.88,64100.65],[64107.87,64810.42,64101.71,64773.78],[64772.89,64772.89,63987.04,64398.08],[64398.18,64450.71,63938.9,64436.39],[64454.39,65473.61,64393.45,65407.58],[65412.64,65750,65100,65608.07],[65607.29,65716.68,65203.4,65454.91],[65454.91,65752.13,65337.29,65651.19],[65651.19,66033.83,65560.5,65782.98],[65793.84,66487.18,65662.49,66270]],
      questions: [
        {
          key: 'state',
          prompt: 'Quelle séquence mérite l’attention ?',
          options: [
            ['random', 'Une simple bougie verte isolée dans une baisse.'],
            ['reversal', 'PDL traité plus tôt, nouveau rejet des lows, puis displacement haussier.', true],
            ['guarantee', 'Le sweep du PDL garantit que le PDH sera atteint.'],
          ],
          explanation: 'Le sweep antérieur fournit le contexte ; le displacement fournit une information de contrôle. Aucun des deux ne garantit le target.',
        },
        {
          key: 'dol',
          prompt: 'Comment hiérarchiser les cibles ?',
          options: [
            ['pdl', 'Viser le PDL déjà traité sous le prix.'],
            ['highs', 'Highs internes 64 768/64 810, puis PDH 68 136 si la structure tient.', true],
            ['infinite', 'Laisser courir sans cible car le mouvement est impulsif.'],
          ],
          explanation: 'Une cible interne paie d’abord le risque ; le PDH reste la destination externe candidate. Les deux rôles ne doivent pas être confondus.',
        },
        {
          key: 'execution',
          prompt: 'Le prix du gel autorise-t-il un achat automatique ?',
          options: [
            ['market', 'Oui, toute grande bougie verte est une entrée.'],
            ['pullback', 'Non : attendre un retracement qui conserve le low protégé et offre encore du R.', true],
            ['short', 'Non : il faut vendre parce que le marché montait déjà avant.'],
          ],
          explanation: 'Le displacement est une permission de chercher, pas l’ordre lui-même. L’entrée doit rester entre l’invalidation et une cible ouverte.',
        },
        {
          key: 'invalidation',
          prompt: 'Quel repère invalide la lecture haussière ?',
          options: [
            ['candle', 'La couleur de la prochaine bougie.'],
            ['protected-low', 'La perte du low protégé construit après le rejet, avec réacceptation sous la zone.', true],
            ['pdh', 'Le PDH invalide le long avant même d’être atteint.'],
          ],
          explanation: 'Le risque se place là où le changement de contrôle n’est plus défendable, pas à une distance arbitraire.',
        },
      ],
      correction: {
        classification: 'Reversal haussier conditionnel · entrée sur retracement',
        observation: 'Après le gel, le prix consolide, puis progresse vers les highs internes. La patience était nécessaire : le futur contient encore plusieurs rotations.',
        action: 'En replay, marque le low protégé, mesure l’espace vers 64 810 puis vers le PDH, et refuse tout achat dont l’entrée consomme cette asymétrie.',
      },
    },
    {
      id: 'hist-04',
      code: 'HIST-04',
      title: 'Après le sweep, le marché reste au milieu de sa range',
      date: '7 mars 2024',
      start: '12:00',
      freezeIndex: 19,
      freezeLabel: 'après la bougie 16:45–17:00 UTC',
      archetype: 'Milieu de range · no trade',
      context: [
        ['PDH', '67 654 · pris puis retravaillé'],
        ['Range visible', '66 635 → 68 019'],
        ['Gel', '67 409 · proche de l’équilibre'],
      ],
      levels: [
        { label: 'PDH 67 654', value: 67654.06, tone: 'event', plot: true },
        { label: 'Range low 66 635', value: 66634.98, tone: 'target', plot: true },
      ],
      candles: [[66950,67152.98,66950,67039.62],[67039.62,67131.22,66855.51,66885.71],[66884.53,66958.49,66760.46,66765.08],[66765.09,66802.89,66629.72,66767.8],[66767.8,66842.83,66631.83,66678.47],[66677.26,66915.96,66635.64,66912.85],[66912.84,67054.15,66800,66921.29],[66921.28,67067.57,66873.23,66951.07],[66951.07,67210.09,66937.43,67095.15],[67098.19,67406.86,67076.36,67349.05],[67339.93,68019.48,66910.32,67285],[67288.67,67300,66634.98,67105.2],[67094.47,67451.04,66944.06,67010.15],[67004.53,67183.51,66799.04,66993.63],[66993.63,67420,66986.17,67301.84],[67300.15,67666.65,67252.69,67332.67],[67319.98,67520,67112.15,67179.48],[67179.25,67600,67123.87,67395.77],[67390.68,67414.52,66912.53,67241.48],[67236.01,67440.93,67143.92,67408.61],[67412.88,67984.55,67319.65,67964.91],[67965.23,68098.09,67673.63,67962.53],[67947.96,67959.09,67680.02,67931.47],[67931.46,67943.91,67468.5,67689.06],[67689.06,67757.23,67478.86,67581.82],[67581.82,67815.54,67555.73,67733.6],[67729.44,67770,67526.31,67710.5],[67710.5,67907.53,67653.47,67712.34],[67716.7,67985.59,67692.09,67795.06],[67795.07,67823.4,67335,67432.83],[67432.82,67610.93,67316.42,67591.54],[67593.75,67692.32,67517.91,67594.2],[67594.2,67814.46,67565.17,67750]],
      questions: [
        {
          key: 'state',
          prompt: 'Où se trouve le prix au gel ?',
          options: [
            ['discount', 'À un extrême bas clair de la range.'],
            ['middle', 'Entre les extrêmes visibles, proche de l’équilibre et après plusieurs rotations.', true],
            ['breakout', 'En acceptation nette au-dessus du high 68 019.'],
          ],
          explanation: 'Le PDH a été pris, mais le prix n’a ni livré une continuation propre ni conservé un déplacement baissier exploitable.',
        },
        {
          key: 'dol',
          prompt: 'Quelle DOL domine avec certitude ?',
          options: [
            ['high', 'Le high, parce qu’il est au-dessus.'],
            ['low', 'Le low, parce qu’il est en dessous.'],
            ['none', 'Aucune : les deux côtés restent défendables depuis le milieu.', true],
          ],
          explanation: 'Nommer la liquidité la plus proche ne suffit pas. Il faut une raison contextuelle de privilégier un côté de la range.',
        },
        {
          key: 'execution',
          prompt: 'Quelle prochaine action est la plus opérationnelle ?',
          options: [
            ['guess', 'Choisir un côté pour être présent avant le prochain mouvement.'],
            ['edge', 'Attendre le travail d’un extrême, puis une acceptation ou une réintégration lisible.', true],
            ['both', 'Placer simultanément un buy et un sell.'],
          ],
          explanation: 'Le no-trade est temporaire : il précise l’événement qui doit transformer la carte avant une nouvelle décision.',
        },
        {
          key: 'classification',
          prompt: 'Comment noter cette décision ?',
          options: [
            ['fear', 'Trade manqué par peur si le prix bouge ensuite.'],
            ['valid-no-trade', 'No-trade conforme tant qu’aucun extrême ne livre une permission.', true],
            ['loss', 'Perte théorique parce qu’aucun ordre n’a été pris.'],
          ],
          explanation: 'Le mouvement futur ne doit pas rétroactivement transformer une zone ambiguë en setup évident.',
        },
      ],
      correction: {
        classification: 'No-trade conforme · attendre un extrême',
        observation: 'Le prix remonte ensuite travailler le high avant de revenir dans la range. Cette oscillation confirme surtout le coût d’une décision prise au milieu.',
        action: 'Programme deux alertes aux extrêmes, ferme le graphique et ne réouvre la décision qu’après un événement observable.',
      },
    },
  ];

  function readState() {
    try {
      const parsed = JSON.parse(localStorage.getItem(storageKey) || '{}');
      return {
        answers: parsed.answers && typeof parsed.answers === 'object' ? parsed.answers : {},
        scores: parsed.scores && typeof parsed.scores === 'object' ? parsed.scores : {},
        best: Number(parsed.best) || 0,
      };
    } catch {
      return { answers: {}, scores: {}, best: 0 };
    }
  }

  let state = readState();

  function saveState() {
    localStorage.setItem(storageKey, JSON.stringify(state));
  }

  function optionMarkup(caseId, question) {
    return question.options.map(([value, label, correct]) => `
      <label>
        <input ${correct ? 'data-correct="true"' : ''} name="${caseId}-${question.key}" type="radio" value="${value}"/>
        <span>${label}</span>
      </label>`).join('');
  }

  function caseMarkup(item) {
    return `
      <article class="historical-case" data-historical-case="${item.id}" id="${item.id}">
        <header class="historical-case-head">
          <div><span>${item.code} · ${item.date}</span><h2>${item.title}</h2><p>${item.archetype}</p></div>
          <strong data-case-status>FUTUR MASQUÉ</strong>
        </header>
        <div class="historical-context-strip">
          ${item.context.map(([label, value]) => `<div><small>${label}</small><strong>${value}</strong></div>`).join('')}
          <div><small>Source</small><strong>Coinbase Exchange · BTC-USD · M15</strong></div>
        </div>
        <div class="historical-chart-shell">
          <div class="historical-chart-head"><span>Fenêtre 12:00–20:00 UTC</span><strong>${item.freezeLabel}</strong></div>
          <div class="historical-chart-scroll"><svg data-historical-chart role="img" viewBox="0 0 920 420"></svg></div>
          <div class="historical-chart-key"><span><i class="up"></i>Clôture haussière</span><span><i class="down"></i>Clôture baissière</span><span><i class="level"></i>Repère connu au gel</span></div>
        </div>
        <form class="historical-form" data-historical-form>
          <div class="historical-mission-head"><div><small>MISSION AVANT RÉVÉLATION</small><h3>Décide avec les seules informations visibles</h3></div><span><b data-case-answered>0</b> / 4 réponses</span></div>
          <div class="historical-question-grid">
            ${item.questions.map((question, index) => `
              <fieldset data-question="${question.key}">
                <legend><span>0${index + 1}</span>${question.prompt}</legend>
                <div class="historical-options">${optionMarkup(item.id, question)}</div>
                <p class="historical-explanation" hidden><strong>Pourquoi :</strong> ${question.explanation}</p>
              </fieldset>`).join('')}
          </div>
          <button data-case-submit disabled type="submit">Verrouiller les réponses et révéler le futur</button>
        </form>
        <div class="historical-result" data-case-result hidden>
          <div class="historical-result-score"><small>SCORE DE DÉCISION</small><strong data-case-score>0 / 4</strong></div>
          <div><small>CLASSIFICATION</small><h3>${item.correction.classification}</h3><p>${item.correction.observation}</p><p><strong>Drill suivant :</strong> ${item.correction.action}</p></div>
        </div>
      </article>`;
  }

  lab.querySelector('[data-historical-cases]').innerHTML = cases.map(caseMarkup).join('');

  function svgNode(name, attributes = {}, content = '') {
    const node = document.createElementNS(ns, name);
    Object.entries(attributes).forEach(([key, value]) => node.setAttribute(key, value));
    if (content) node.textContent = content;
    return node;
  }

  function renderChart(item, reviewed) {
    const card = lab.querySelector(`[data-historical-case="${item.id}"]`);
    const svg = card.querySelector('[data-historical-chart]');
    const shown = reviewed ? item.candles.length : item.freezeIndex + 1;
    const visible = item.candles.slice(0, shown);
    const plotLevels = item.levels.filter((level) => level.plot);
    const values = visible.flatMap((candle) => [candle[1], candle[2]]).concat(plotLevels.map((level) => level.value));
    const rawMin = Math.min(...values);
    const rawMax = Math.max(...values);
    const pad = Math.max((rawMax - rawMin) * 0.08, 80);
    const min = rawMin - pad;
    const max = rawMax + pad;
    const left = 60;
    const right = 858;
    const top = 38;
    const bottom = 350;
    const step = (right - left) / item.candles.length;
    const bodyWidth = Math.max(5, step * 0.58);
    const y = (value) => bottom - ((value - min) / (max - min)) * (bottom - top);
    const x = (index) => left + step * index + step / 2;

    svg.replaceChildren();
    svg.setAttribute('aria-label', `${item.code}, chandeliers historiques BTC-USD M15, ${reviewed ? 'futur révélé' : 'futur masqué'} ${item.freezeLabel}`);
    svg.dataset.candlesShown = String(shown);

    svg.append(svgNode('rect', { x: 0, y: 0, width: 920, height: 420, fill: '#06111d' }));
    for (let row = 0; row < 5; row += 1) {
      const gridY = top + ((bottom - top) / 4) * row;
      svg.append(svgNode('line', { x1: left, x2: right, y1: gridY, y2: gridY, stroke: '#173048', 'stroke-width': 1 }));
      const value = max - ((max - min) / 4) * row;
      svg.append(svgNode('text', { x: 906, y: gridY + 4, fill: '#7890a7', 'font-size': 10, 'text-anchor': 'end' }, price.format(value)));
    }

    plotLevels.forEach((level) => {
      const levelY = y(level.value);
      const color = level.tone === 'target' ? '#4fd37b' : '#f8c24e';
      svg.append(svgNode('line', { x1: left, x2: right, y1: levelY, y2: levelY, stroke: color, 'stroke-width': 1.5, 'stroke-dasharray': '7 5', opacity: 0.9 }));
      svg.append(svgNode('rect', { x: 64, y: levelY - 19, width: 142, height: 18, rx: 9, fill: '#081725', stroke: color, opacity: 0.96 }));
      svg.append(svgNode('text', { x: 135, y: levelY - 7, fill: color, 'font-size': 9.5, 'font-weight': 900, 'text-anchor': 'middle' }, level.label));
    });

    visible.forEach((candle, index) => {
      const [open, high, low, close] = candle;
      const bullish = close >= open;
      const color = bullish ? '#36d59b' : '#ff6b72';
      const candleX = x(index);
      const bodyTop = y(Math.max(open, close));
      const bodyHeight = Math.max(2, Math.abs(y(open) - y(close)));
      svg.append(svgNode('line', { x1: candleX, x2: candleX, y1: y(high), y2: y(low), stroke: color, 'stroke-width': 1.6 }));
      svg.append(svgNode('rect', { x: candleX - bodyWidth / 2, y: bodyTop, width: bodyWidth, height: bodyHeight, rx: 1, fill: color }));
    });

    const freezeX = x(item.freezeIndex) + step / 2;
    svg.append(svgNode('line', { x1: freezeX, x2: freezeX, y1: top, y2: bottom, stroke: '#8ee5fa', 'stroke-width': 1.5, 'stroke-dasharray': '5 5' }));
    svg.append(svgNode('text', { x: freezeX - 8, y: 24, fill: '#8ee5fa', 'font-size': 10, 'font-weight': 900, 'text-anchor': 'end' }, 'GEL DE DÉCISION'));

    if (!reviewed) {
      svg.append(svgNode('rect', { x: freezeX + 2, y: top, width: right - freezeX - 2, height: bottom - top, fill: '#071019', opacity: 0.96, stroke: '#30465c', 'stroke-dasharray': '7 6' }));
      svg.append(svgNode('text', { x: freezeX + (right - freezeX) / 2, y: 181, fill: '#f8c24e', 'font-size': 18, 'font-weight': 900, 'text-anchor': 'middle' }, 'FUTUR MASQUÉ'));
      svg.append(svgNode('text', { x: freezeX + (right - freezeX) / 2, y: 207, fill: '#7f93a7', 'font-size': 11, 'text-anchor': 'middle' }, 'Réponds aux 4 décisions avant de révéler'));
    }

    for (let index = 0; index < item.candles.length; index += 4) {
      const minutes = 12 * 60 + index * 15;
      const label = `${String(Math.floor(minutes / 60)).padStart(2, '0')}:${String(minutes % 60).padStart(2, '0')}`;
      svg.append(svgNode('text', { x: x(index), y: 379, fill: '#72879b', 'font-size': 10, 'text-anchor': 'middle' }, label));
    }
    svg.append(svgNode('text', { x: 60, y: 405, fill: '#4f667c', 'font-size': 9.5 }, 'UTC · données historiques brutes, lecture ICT pédagogique ajoutée par le cours'));
  }

  function applyReview(item, card, answers, score) {
    card.classList.add('is-reviewed');
    card.querySelector('[data-case-status]').textContent = 'FUTUR RÉVÉLÉ';
    card.querySelector('[data-case-score]').textContent = `${score} / 4`;
    card.querySelector('[data-case-result]').hidden = false;
    card.querySelector('[data-case-submit]').textContent = 'Réponses verrouillées · futur révélé';
    card.querySelector('[data-case-submit]').disabled = true;

    item.questions.forEach((question) => {
      const fieldset = card.querySelector(`[data-question="${question.key}"]`);
      const selected = answers[question.key];
      fieldset.querySelectorAll('input').forEach((input) => {
        input.disabled = true;
        input.checked = input.value === selected;
        const label = input.closest('label');
        label.classList.toggle('is-answer', input.dataset.correct === 'true');
        label.classList.toggle('is-selected-wrong', input.checked && input.dataset.correct !== 'true');
      });
      fieldset.classList.toggle('is-correct', fieldset.querySelector('input:checked')?.dataset.correct === 'true');
      fieldset.classList.toggle('is-wrong', fieldset.querySelector('input:checked')?.dataset.correct !== 'true');
      fieldset.querySelector('.historical-explanation').hidden = false;
    });
    card.querySelector('[data-case-answered]').textContent = '4';
    renderChart(item, true);
  }

  function updateDashboard() {
    const completed = Object.keys(state.scores).filter((id) => cases.some((item) => item.id === id)).length;
    const total = Object.values(state.scores).reduce((sum, value) => sum + Number(value || 0), 0);
    if (completed === cases.length) state.best = Math.max(state.best, total);
    lab.querySelector('[data-historical-completed]').textContent = `${completed} / ${cases.length}`;
    lab.querySelector('[data-historical-score]').textContent = `${total} / ${cases.length * 4}`;
    lab.querySelector('[data-historical-best]').textContent = `${state.best} / ${cases.length * 4}`;
    lab.querySelector('[data-historical-progress]').style.width = `${(completed / cases.length) * 100}%`;
    lab.querySelector('[data-historical-progressbar]').setAttribute('aria-valuenow', String(completed));
    saveState();
  }

  cases.forEach((item) => {
    const card = lab.querySelector(`[data-historical-case="${item.id}"]`);
    const form = card.querySelector('[data-historical-form]');
    const savedAnswers = state.answers[item.id];
    const savedScore = state.scores[item.id];

    if (savedAnswers && Number.isFinite(Number(savedScore))) {
      applyReview(item, card, savedAnswers, Number(savedScore));
    } else {
      renderChart(item, false);
    }

    form.addEventListener('change', () => {
      if (card.classList.contains('is-reviewed')) return;
      const answered = item.questions.filter((question) => form.querySelector(`input[name="${item.id}-${question.key}"]:checked`)).length;
      card.querySelector('[data-case-answered]').textContent = String(answered);
      card.querySelector('[data-case-submit]').disabled = answered !== item.questions.length;
    });

    form.addEventListener('submit', (event) => {
      event.preventDefault();
      if (card.classList.contains('is-reviewed')) return;
      const answers = {};
      let score = 0;
      item.questions.forEach((question) => {
        const selected = form.querySelector(`input[name="${item.id}-${question.key}"]:checked`);
        answers[question.key] = selected?.value || '';
        if (selected?.dataset.correct === 'true') score += 1;
      });
      state.answers[item.id] = answers;
      state.scores[item.id] = score;
      applyReview(item, card, answers, score);
      updateDashboard();
      card.querySelector('[data-case-result]').scrollIntoView({ behavior: 'smooth', block: 'center' });
    });
  });

  const reset = lab.querySelector('[data-historical-reset]');
  reset.addEventListener('click', () => {
    if (reset.dataset.armed !== 'true') {
      reset.dataset.armed = 'true';
      reset.textContent = 'Confirmer la remise à zéro';
      window.setTimeout(() => {
        reset.dataset.armed = 'false';
        reset.textContent = 'Réinitialiser les quatre cas';
      }, 4000);
      return;
    }
    localStorage.removeItem(storageKey);
    window.location.reload();
  });

  updateDashboard();
})();
