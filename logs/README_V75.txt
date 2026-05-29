ICT Atlas V75 - Audit SVG et cohérence des graphiques

Objectif
- Auditer tous les SVG du cours.
- Vérifier que les graphiques ne coupent pas les textes importants.
- Vérifier que les quiz ne révèlent pas la réponse avant la correction.
- Améliorer la lisibilité des séries A/B/C.

Audit réalisé
- 45 pages HTML analysées.
- 219 SVG analysés.
- 0 SVG sans aria-label après correction.
- 0 réponse visible dans les SVG de quiz avant ouverture de la correction.
- 0 problème critique détecté après corrections.
- 52 avertissements "long-label" conservés : ce sont des labels longs mais non coupés par le viewBox.
- 0 lien manquant.
- 0 ancre cassée.

Corrections appliquées
- Les cartes A/B/C sont maintenant en lecture verticale :
  - graphique pleine largeur ;
  - liste d'interprétation sous le graphique ;
  - moins de compression horizontale.
- Les mini graphiques 320x280 ont reçu plus d'espace vertical :
  - viewBox porté à 320x300 ;
  - fond SVG allongé ;
  - labels bas de graphique moins proches du bord.
- Les quiz ne montrent plus directement "Réponse : ..." dans les SVG :
  - les labels visibles deviennent "Cas A : à classer" ou "Cas B : à classer".
- Les SVG sans aria-label héritent maintenant du titre de section pour clarifier leur intention.
- Deux labels détectés comme trop proches du bord ont été raccourcis :
  - Daily Bias : "0/1 pt alignement" ;
  - Premium/Discount : "50% / EQ".

Contrôle pédagogique
- Les pages conceptuelles clés OB, FVG, MSS, Breaker, PD Arrays, OTE, DOL, SMT, profils de journée, displacement et no trade ont été contrôlées par correspondance section -> aria-label SVG.
- Les graphiques correspondent bien à leur exemple annoncé :
  - anatomie conceptuelle ;
  - cas A/B/C ;
  - pièges ;
  - séquences de décision.

Limite
- Playwright n'est pas installé dans l'environnement local, donc la passe navigateur automatisée n'a pas été lancée ici.
- L'audit statique est néanmoins reproductible via audit_svg_quality.py.
