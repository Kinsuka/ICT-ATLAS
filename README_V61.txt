ICT Atlas - V61 - Psychologie et workflow d'execution

Objectif
Renforcer les deux pages qui preparent le passage au reel : psychologie du
trader et workflow de session. Le but est de passer de conseils generaux a des
protocoles executables.

Changements
- 26-psychologie-trader.html :
  - carte des sabotages : declencheur, phrase interne, action dangereuse,
    protocole ;
  - thermometre emotionnel vert / jaune / rouge ;
  - regles si/alors pour retirer la decision au moment chaud.
- 20-workflow-session.html :
  - workflow de session comme machine a etats ;
  - micro-routine des 90 secondes avant le clic ;
  - score de session pour mesurer la qualite d'execution au-dela du PnL.
- templates/checklist-session.md :
  - ajout du thermometre mental.
- templates/review-post-session.md :
  - ajout d'une section sabotage potentiel.
- add_v61_psychology_workflow.py :
  - script idempotent pour reinserer les sections.

Principe pedagogique
La psychologie n'est pas traitee comme une motivation abstraite. Elle devient
observable : etat interne, declencheur, phrase interne, action, protocole,
score de session.

Validation attendue
- Aucun changement de compteur : 30 lecons.
- Aucun lien HTML ou template casse.
- Graphiques SVG lisibles et non coupes.
- Navigation conservee.
