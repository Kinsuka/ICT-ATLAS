V102 — Performance HTML/SVG, chargement, scripts et GitHub Pages

- Audit initial : 58 pages, 2 438 970 octets HTML bruts, 524 861 octets HTML gzip et 252 SVG inline.
- Suppression des 407 871 octets de panneau de glossaire répétés dans 41 pages.
- Extraction des 26 définitions rapides dans `js/glossary-data.js`, chargé uniquement à la première ouverture puis réutilisé.
- Conservation d’une coquille de dialogue légère dans le HTML pour préserver les sémantiques et le focus sans attendre le réseau.
- Préconversion de 16 graphiques génériques en composants HTML sémantiques : 236 SVG restants au lieu de 252.
- Suppression du remplacement JavaScript correspondant et report des enrichissements graphiques non critiques via `requestIdleCallback`.
- Passage du dernier script bloquant de la page 20 en `defer`.
- Ajout de `.nojekyll` pour éviter le traitement Jekyll inutile sur GitHub Pages.
- Ajout d’un mode `npm run preview` avec gzip, ETag, réponses 304 et cache court pour les ressources statiques.
- Ajout de budgets versionnés dans `data/performance-budgets.json` et de la commande `npm run test:performance`.
- Résultat final : 2 058 422 octets HTML bruts et 446 453 octets gzip, soit −380 548 octets bruts et −78 408 octets gzip par parcours complet.
