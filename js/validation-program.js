(() => {
  const root = document.querySelector('[data-validation-program]');
  if (!root) return;
  const key = 'ict-atlas-validation-20-sessions-v1';
  const gates = ['Préparation écrite avant le résultat','Carte minimale et DOL déclarées','Décision prévue respectée : attendre, entrer ou no trade','Risque, invalidation et taille respectés','Capture après et classification produites'];
  const phases = [
    ['Voir avant d’agir','01–05','Construire la carte et la prochaine action sans chercher une entrée.'],
    ['Attendre puis exécuter','06–10','Séparer événement, trigger et prix d’exécution.'],
    ['Risquer et gérer','11–15','Rendre stop, taille et gestion indépendants de l’émotion.'],
    ['Décider en autonomie','16–20','Conduire la session complète, y compris le no-trade.'],
  ];
  const sessions = [
    ['Lecture à blanc','Produire uniquement la lecture Daily/H4 avant la session.','Capture top-down annotée.','Aucun biais déduit d’une seule bougie.'],
    ['Carte de liquidité','Tracer BSL, SSL, PDH/PDL et extrêmes utiles.','Carte avant révélation.','Supprimer tout niveau sans rôle décisionnel.'],
    ['Une DOL, pas trois','Hiérarchiser une destination et une target interne.','Phrase DOL + TP1.','Deux côtés égaux = attendre.'],
    ['Scénarios A / B','Écrire le scénario attendu et son invalidation.','Deux phrases conditionnelles.','Aucun ordre sans événement préalable.'],
    ['No-trade actif','Rechercher une raison objective de ne pas cliquer.','Refus écrit et résultat après.','Le futur ne modifie pas le refus.'],
    ['Événement ou contact','Distinguer arrivée au POI et prise exploitable.','Horodatage de l’événement.','Un contact seul ne valide rien.'],
    ['Trigger unique','N’utiliser qu’un modèle déclaré avant replay.','Nom et capture du trigger.','Aucun trigger ajouté après coup.'],
    ['Attente du retour','Laisser le prix revenir sans le poursuivre.','Prix planifié vs prix obtenu.','Entrée non servie = aucun devoir de trader.'],
    ['Invalidation avant stop','Écrire où l’hypothèse devient fausse.','Phrase d’invalidation.','Le stop ne fabrique jamais le RR.'],
    ['Targets puis R','Choisir TP1/TP2 puis mesurer R.','Calcul vers les deux targets.','R insuffisant = no trade.'],
    ['Taille après stop','Calculer la taille depuis le risque et le stop.','Calcul de taille documenté.','Aucun lot choisi avant le stop.'],
    ['Gestion déclarée','Fixer partiel, BE et runner avant l’entrée.','Plan de gestion écrit.','Aucune modification par peur.'],
    ['BE sous contrôle','Comparer la règle BE testée au prix.','Moment exact du BE.','BE n’est pas une vérité universelle.'],
    ['Perte conforme','Conserver une perte valide sans changer le modèle.','Classification −1R conforme.','Ni revenge, ni suppression statistique.'],
    ['Gagnant hors plan','Classer comme erreur un gain hors protocole.','Écart de règle identifié.','Le P&L positif ne donne aucun point.'],
    ['Session autonome','Conduire les huit décisions sans le cours.','Fiche et captures avant/après.','Localiser toute hésitation par porte.'],
    ['Consolidation / news','Reconnaître une séance dominée par l’attente.','Filtre temporel documenté.','Aucun trade dans le bruit prévu.'],
    ['Anti-chase','Refuser une direction correcte devenue trop chère.','R initial vs R restant.','Ne jamais rapprocher le stop pour poursuivre.'],
    ['Deux refus consécutifs','Accepter deux sessions sans ordre.','Deux fiches no-trade complètes.','L’ennui ne devient pas permission.'],
    ['Évaluation finale','Réaliser une simulation comme un examen.','Dossier de preuve final.','Aucune correction consultée pendant.'],
  ];
  const empty = () => sessions.map(() => ({ checks: [false,false,false,false,false], finalized: false }));
  const load = () => { try { const x = JSON.parse(localStorage.getItem(key)); return Array.isArray(x) && x.length === 20 ? x.map(r => ({checks: Array.isArray(r.checks) && r.checks.length === 5 ? r.checks.map(Boolean) : [false,false,false,false,false], finalized: Boolean(r.finalized)})) : empty(); } catch (_) { return empty(); } };
  let records = load();
  let resetTimer;
  const save = () => { try { localStorage.setItem(key, JSON.stringify(records)); } catch (_) {} };
  const score = r => r.checks.filter(Boolean).length;
  const passes = r => r.finalized && score(r) >= 4 && r.checks[2] && r.checks[3];
  const phaseStats = i => { const list = records.slice(i*5,i*5+5); const completed=list.filter(r=>r.finalized).length; const passed=list.filter(passes).length; return {completed,passed,valid:completed===5&&passed>=4}; };

  function renderPhases() {
    const box=root.querySelector('[data-validation-phases]'); box.replaceChildren();
    phases.forEach((phase,i)=>{ const s=phaseStats(i), card=document.createElement('article'); card.className=`validation-phase ${s.valid?'is-valid':s.completed===5?'is-failed':''}`; card.innerHTML=`<div><span>0${i+1}</span><small>${s.valid?'PHASE VALIDÉE':`${s.completed} / 5 évaluées`}</small></div><h3>${phase[0]}</h3><strong>Sessions ${phase[1]}</strong><p>${phase[2]}</p><i style="--phase-progress:${s.completed*20}%"></i><em>${s.passed} conformes · seuil 4 / 5</em>`; box.append(card); });
  }

  function renderSessions(openIndex=0) {
    const box=root.querySelector('[data-validation-sessions]'); box.replaceChildren();
    sessions.forEach((session,i)=>{ const r=records[i], ok=passes(r), details=document.createElement('details'); details.className=`validation-session ${r.finalized?(ok?'is-passed':'is-failed'):''}`; details.dataset.sessionIndex=i; details.open=i===openIndex;
      const summary=document.createElement('summary'); summary.innerHTML=`<span>${String(i+1).padStart(2,'0')}</span><strong>${session[0]}</strong><small>Phase ${Math.floor(i/5)+1}</small><em>${r.finalized?`${score(r)} / 5 · ${ok?'CONFORME':'À REPRENDRE'}`:'À ÉVALUER'}</em>`;
      const body=document.createElement('div'); body.className='validation-session-body'; const mission=document.createElement('div'); mission.className='validation-session-mission'; [['Mission',session[1]],['Preuve attendue',session[2]],['Règle défensive',session[3]]].forEach(x=>{const d=document.createElement('div'),h=document.createElement('strong'),p=document.createElement('p');h.textContent=x[0];p.textContent=x[1];d.append(h,p);mission.append(d);});
      const gateBox=document.createElement('div'); gateBox.className='validation-session-gates'; gates.forEach((text,g)=>{const label=document.createElement('label'),input=document.createElement('input'),span=document.createElement('span'); if(g===2||g===3)label.classList.add('is-critical'); input.type='checkbox';input.checked=r.checks[g];input.disabled=r.finalized;input.dataset.gateIndex=g;span.textContent=text;label.append(input,span);gateBox.append(label);});
      const footer=document.createElement('div');footer.className='validation-session-footer';const note=document.createElement('p');note.textContent=r.finalized?(ok?'Session conforme. Le résultat financier n’ajoute aucun point.':'Session non conforme. Rejoue une nouvelle occurrence après correction.'):'Coche uniquement les faits prouvés par la fiche et les captures.';const button=document.createElement('button');button.type='button';button.dataset.validationFinalize=i;button.textContent=r.finalized?'Modifier l’évaluation':'Enregistrer la session';footer.append(note,button);body.append(mission,gateBox,footer);details.append(summary,body);box.append(details);
    });
  }

  function updateDashboard(){const completed=records.filter(r=>r.finalized).length,passed=records.filter(passes).length,total=records.filter(r=>r.finalized).reduce((n,r)=>n+score(r),0),avg=completed?Math.round(total/(completed*5)*100):null,phaseOK=phases.every((_,i)=>phaseStats(i).valid),riskOK=records.slice(10).every(r=>r.finalized&&r.checks[3]),ready=completed===20&&passed>=17&&phaseOK&&riskOK,missing=records.findIndex(r=>!r.finalized),failed=records.findIndex(r=>r.finalized&&!passes(r));root.querySelector('[data-validation-completed]').textContent=completed;root.querySelector('[data-validation-passed]').textContent=passed;root.querySelector('[data-validation-average]').textContent=avg===null?'—':`${avg} %`;const state=root.querySelector('[data-validation-readiness]'),next=root.querySelector('[data-validation-next]');state.textContent=ready?'VALIDATION REPLAY ACQUISE':completed===20?'REPRENDRE LES ÉCHECS':'POURSUIVRE LE PROGRAMME';state.classList.toggle('is-ready',ready);next.textContent=ready?'Étape suivante : nouvel échantillon indépendant, toujours sans risque live.':missing!==-1?`Session ${String(missing+1).padStart(2,'0')} · ${sessions[missing][0]}`:`Rejouer : session ${String(failed+1).padStart(2,'0')} · ${sessions[failed][0]}`;}
  const refresh=(open=0)=>{renderPhases();renderSessions(open);updateDashboard();};
  const sessionBox=root.querySelector('[data-validation-sessions]');
  sessionBox.addEventListener('change',e=>{const input=e.target.closest('input[data-gate-index]');if(!input)return;const i=Number(input.closest('[data-session-index]').dataset.sessionIndex);records[i].checks[Number(input.dataset.gateIndex)]=input.checked;save();});
  sessionBox.addEventListener('click',e=>{const b=e.target.closest('[data-validation-finalize]');if(!b)return;const i=Number(b.dataset.validationFinalize);records[i].finalized=!records[i].finalized;save();refresh(i);});
  const reset=root.querySelector('[data-validation-reset]');reset.addEventListener('click',()=>{if(reset.dataset.armed!=='true'){reset.dataset.armed='true';reset.textContent='Confirmer : effacer les 20 sessions';clearTimeout(resetTimer);resetTimer=setTimeout(()=>{reset.dataset.armed='false';reset.textContent='Effacer toute la progression';},5000);return;}clearTimeout(resetTimer);records=empty();try{localStorage.removeItem(key);}catch(_){}reset.dataset.armed='false';reset.textContent='Effacer toute la progression';refresh();});
  refresh();
})();
