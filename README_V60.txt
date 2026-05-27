ICT Atlas - V60 - Acces permanent aux ressources

Objectif
Rendre les ressources pratiques accessibles depuis chaque lecon, sans leur
donner le meme role que le glossaire.

Changements
- Ajout d'un lien permanent "Ressources pratiques" dans la sidebar du cours.
- Position : juste sous "Glossaire rapide".
- Destination : ressources-pratiques.html.
- Texte secondaire : "Journal · Backtest · Checklist".
- Style volontairement secondaire : accent jaune, moins contextuel que la
  modal glossaire.

Raison pedagogique
Le glossaire sert a comprendre sans quitter la page. Les ressources servent
a pratiquer : ouvrir un journal, un backtest, une checklist ou une fiche replay.
Un lien permanent est donc plus adapte qu'une modal.

Validation attendue
- Navigation regeneree avec course_platform_layout.py.
- Compteur coherent : 30 lecons.
- Aucun lien HTML manquant.
- Aucun bruit de version visible dans les pages publiques.
