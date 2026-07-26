V101 — Accessibilité globale et navigation clavier

- Ajout d’un lien d’évitement « Aller au contenu principal » sur toutes les surfaces du site.
- Normalisation de la cible principale `#contenu` et de sa prise de focus au clavier.
- Renforcement global des indicateurs `:focus-visible`, y compris en contraste forcé.
- Respect de `prefers-reduced-motion` pour les transitions d’interface ajoutées.
- Taille minimale de 44 px pour les contrôles principaux et de 24 px pour les termes interactifs intégrés au texte.
- Relèvement de la couleur de texte secondaire `--course-faint` au niveau de contraste AA.
- Transformation du glossaire latéral en modale clavier robuste : état ARIA, arrière-plan inerte, piège de focus, fermeture par Échap et restitution du focus.
- Correction de cinq identifiants SVG `arrow` dupliqués sur la page 03.
- Extension du contrôle structurel pour empêcher la désactivation du zoom utilisateur.
- Ajout d’une matrice Playwright automatique couvrant 58 pages, sur desktop et mobile, plus les parcours clavier et le contraste des couleurs sémantiques.
- Ajout de la commande dédiée `npm run test:a11y`.
