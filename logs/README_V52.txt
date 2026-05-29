ICT Atlas V52 - Passe lisibilite des graphiques A/B/C

Objectif :
Corriger les problemes de lecture constates sur les series A/B/C :
graphiques trop etroits, textes tronques, zones coupees et annotations
moins lisibles en grille 3 colonnes.

Changements :
- Les series A/B/C passent d'une grille 3 colonnes a une pile verticale.
- Sur desktop, chaque cas affiche le graphique en grand avec la liste de
  verification a droite.
- Sur mobile, le graphique et la liste se placent l'un sous l'autre.
- Les SVG A/B/C gardent leurs points + lignes tiretees, mais les titres et
  captions internes ont ete raccourcis pour ne plus sortir du graphe.
- Les labels de bord droit ont ete legerement rentres dans le viewBox.
- Deux graphiques SMT dans 06-contextes-avances.html avaient un viewBox trop
  court : hauteur corrigee de 220 a 340 pour ne plus couper les bougies.

Validation :
- 4 series A/B/C conservees :
  - 04-setups-core.html : 3 cas / 3 SVG
  - 21-liquidite-deplacement.html : 3 cas / 3 SVG
  - 22-structure-trend-range.html : 3 cas / 3 SVG
  - 24-premium-discount-killzones.html : 3 cas / 3 SVG
- Audit SVG : 0 coordonnee hors viewBox.
- Liens HTML : 0 fichier manquant, 0 ancre manquante.
- git diff --check : OK.
