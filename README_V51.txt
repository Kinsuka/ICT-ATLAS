ICT Atlas V51 - Refonte qualité des SVGs ABC (précision et lisibilité)

Contexte :
Passe correctrice sur les 12 SVGs de la série A/B/C introduits en V50.
Problèmes signalés : textes invisibles, graphiques trop étroits cachant des
éléments, annotations flottantes sans lien précis avec ce qu'elles pointent.

Cause racine identifiée :
Le viewBox "0 0 960 300" dans une grille 3 colonnes (~315 px par colonne)
produisait un scale de ~33%. Les textes font-size=12 s'affichaient à 4 px
(illisibles). Les éléments en bas du viewBox (y=278/300) étaient souvent
coupés par le navigateur.

Corrections apportées :

1. viewBox 960×300 → 320×280 sur les 12 SVGs ABC
   - Scale désormais ~1:1 avec la colonne (~315-380 px)
   - font-size=9 s'affiche à ~10-12 px (lisible)
   - Aucun élément coupé (footer à y=274/280, marge suffisante)

2. Annotations précises : point + ligne tiretée + label
   - Chaque élément clé est annoté avec un cercle (r=2.5) au point exact,
     une ligne stroke-dasharray="3,2" vers un label en zone dégagée
   - Exemples : wick qui perce le BSL, B1.high, B3.low, bornes du FVG,
     Sweep ✓, cassure STH (MSS), breakout vs sweep (Cas C)

3. Labels hors des corps de chandelier
   - Tous les labels de niveau (SSL, DOL, CE, STH, Range High/Low)
     placés en marge droite (x=310, text-anchor="end")
   - Labels de chandelier (B1, B2, B3) au-dessus ou en dessous du wick,
     jamais superposés au corps

4. Taille des symboles ✕ réduite
   - font-size=55 → 28-30 (proportionné au nouveau viewBox)

Fichiers modifiés :
- 04-setups-core.html           : 3 SVGs ABC (FVG A/B/C)
- 22-structure-trend-range.html : 3 SVGs ABC (MSS A/B/C)
- 21-liquidite-deplacement.html : 3 SVGs ABC (Sweep A/B/C)
- 24-premium-discount-killzones.html : 3 SVGs ABC (P/D A/B/C)

CSS : aucun changement nécessaire (.chart svg { max-width:100%; height:auto }
      s'adapte naturellement au nouveau viewBox).

Validation :
- 12 SVGs reconstruits (viewBox 320×280)
- 0 ancien viewBox 960×300 résiduel dans les 4 fichiers
- 0 lien cassé introduit
- Commit : 77f6220
