ICT Atlas V50 - Series A/B/C : exemples visuels comparatifs par concept

Objectif :
Passe qualitative sur les 4 concepts les plus critiques du cours.
Chaque concept recoit 3 SVG annotes en grille : cas valide, cas ambigu, faux ami.
L'objectif n'est pas d'ajouter "plus de visuels" mais de montrer la discrimination
entre un signal propre, un signal incomplet et une confusion classique.

Concepts traites :

1. FVG (Fair Value Gap) — 04-setups-core.html
   Section : #fvg-abc-series
   A — Valide   : gap net, B2 impulsif, sweep prealable, zone non comblee
   B — Ambigu   : gap < 2 ticks, B2 faible, pas de sweep
   C — Faux ami : B3 chevauche B1 — pas de gap reel, ce n'est pas un FVG

2. MSS (Market Structure Shift) — 22-structure-trend-range.html
   Section : #mss-abc-series
   A — Valide   : sweep SSL → displacement → cassure STH → FVG dans le deplacement
   B — Ambigu   : cassure sans sweep, deplacement faible, structure incertaine
   C — Faux ami : cassure en range sans contexte de liquidite (breakout, pas MSS)

3. Sweep / Raid — 21-liquidite-deplacement.html
   Section : #sweep-abc-series
   A — Valide   : wick depasse le niveau, corps ferme en dessous, deplacement immediat
   B — Ambigu   : wick effleure a peine, corps ambigu, pas de deplacement net
   C — Faux ami : corps ferme AU-DESSUS = cassure reelle, pas un sweep

4. Premium / Discount — 24-premium-discount-killzones.html
   Section : #pd-abc-series
   A — Correct  : range bien ancree sur vrais swing H/L, buy en discount, sell en premium
   B — Piege    : chercher un buy en premium "parce que ca monte"
   C — Erreur   : anchors incorrects → discount et premium inverses → lecture entierement fausse

Structure HTML ajoutee :
- Chaque serie utilise <div class="abc-grid"> avec 3 <div class="abc-case">
- Chaque cas : 1 SVG annote (verdict en bandeau couleur) + liste abc-check / abc-cross
- CSS ajoute dans style.css : .abc-grid (grid 3 colonnes, responsive 1 col mobile)

Validation :
- 04-setups-core.html         : 14 SVGs (+3), 1 abc-grid, 3 abc-case
- 22-structure-trend-range.html : 10 SVGs (+3), 1 abc-grid, 3 abc-case
- 21-liquidite-deplacement.html :  8 SVGs (+3), 1 abc-grid, 3 abc-case
- 24-premium-discount-killzones.html : 6 SVGs (+3), 1 abc-grid, 3 abc-case
- 0 lien casse introduit
- Commit : 6980e0d
