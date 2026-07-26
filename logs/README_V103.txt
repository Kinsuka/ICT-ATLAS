V103 — Audit final du parcours utilisateur, de l’accueil à la validation 20 sessions

- Audit de bout en bout : accueil, pré-cours, 41 leçons, tableau de progression, pratique guidée, examens, replay historique et programme de validation.
- Correction du premier CTA : un nouvel utilisateur commence désormais par le modèle mental au lieu d’être envoyé directement au cockpit de la leçon 34.
- Suppression du cul-de-sac de la leçon 41 avec une passerelle explicite vers la pratique et un bouton final vers le tableau de progression.
- Extension de la carte d’accueil de six à huit portes pour afficher les preuves jusque-là sautées : examen DOL / TP et replay historique.
- Normalisation des seuils : examen de décision à 10/12, examen DOL / TP à 16/18 et replay historique à 12/16.
- Priorité stricte des preuves locales : une donnée avancée isolée ne permet plus de contourner un seuil antérieur manquant.
- Harmonisation des menus et boutons finaux des cinq pages pratiques : cas/simulateurs → examen décision → examen DOL/TP → replay historique → 20 sessions → tableau de progression.
- Retour explicite au tableau après le programme de vingt sessions pour éviter une fin de parcours sans action.
- Ajout de `npm run test:journey` et de six scénarios Playwright (trois scénarios sur desktop, trois sur mobile), dont une traversée réelle des 41 leçons.
- Validation finale : structure valide, budgets V102 valides et suite complète à 252/252 tests Playwright réussis.
