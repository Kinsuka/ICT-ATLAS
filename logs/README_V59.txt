ICT Atlas - V59 - Replay Lab

Objectif
Ajouter la brique manquante entre les schemas pedagogiques et la pratique :
un laboratoire de bar replay pour travailler sur graphique reel, sans regarder
le futur, avec decision ecrite et correction.

Changements principaux
- Nouvelle lecon : 30-replay-lab.html
- Le cours passe de 29 a 30 lecons.
- La nouvelle lecon est placee dans la Partie 4, entre le programme avance et
  les quiz, afin que l'etudiant s'entraine avant d'etre evalue.
- Ajout du template templates/replay-lab.csv.
- Ajout de liens vers le Replay Lab depuis :
  - index.html
  - 08-quiz.html
  - 15-index-concepts.html
  - 19-preuve-statistique.html
  - 20-workflow-session.html
  - ressources-pratiques.html via la liste des templates

Choix pedagogique important
La V59 n'invente pas de faux cas TradingView dates. Un cas date doit etre
verifie par capture ou replay reel. La lecon fournit donc :
- un protocole anti-biais ;
- six drills obligatoires ;
- une matrice de correction ;
- une fiche CSV de cas replay ;
- des liens vers journal, backtest et review.

Validation attendue
- Navigation regeneree avec course_platform_layout.py.
- Compteur coherent : 30 lecons.
- Aucun lien HTML ou template manquant.
- Aucun texte SVG coupe dans la nouvelle page.
- Le Replay Lab est accessible via precedent/suivant, accueil, quiz et index.
