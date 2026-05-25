ICT Atlas V53 - Passe globale des marqueurs SVG

Objectif :
Etendre la correction de lisibilite a tous les graphiques du guide, pas
seulement aux series A/B/C ajoutees recemment.

Probleme traite :
Certains cercles utilises pour pointer une bougie ou une zone avaient la meme
couleur que l'element pointe. Quand le marqueur tombait sur une bougie verte,
rouge, bleue ou jaune de meme teinte, il devenait difficile a voir.

Changements :
- Audit de 131 SVG dans les pages HTML du guide.
- Tous les petits cercles d'annotation recoivent maintenant :
  - un contour clair #e6f4ff ;
  - une epaisseur minimale adaptee a leur taille ;
  - paint-order="stroke fill" pour que le contour reste lisible.
- Les textes a risque dans le schema OHLC du glossaire ont ete raccourcis
  pour eviter le debordement a droite.

Validation :
- 0 coordonnee SVG hors viewBox.
- 0 texte SVG estime comme debordant horizontalement.
- 0 petit cercle d'annotation sans contour.
- git diff --check : OK.

Note :
Cette passe ne modifie pas la logique pedagogique des graphiques. Elle ajoute
uniquement une couche de contraste et de lisibilite aux pointeurs visuels.
