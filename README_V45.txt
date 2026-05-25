ICT Atlas V45 - refonte lecture editorial dark

Objectif
- Conserver la navigation de cours type plateforme tout en retirant l'effet "catalogue de blocs".
- Revenir a une lecture plus fluide : texte structure, hierarchie typographique, sections longues, notes utiles et schemas mis en valeur.
- Se rapprocher d'une ambiance dark mode dense et professionnelle, inspiree par les plateformes de formation techniques.

Changements principaux
- Nouvelle couche CSS "COURSE EDITORIAL DARK LAYOUT V45" dans style.css.
- Passage du cours en dark mode : fond bleu-noir, texte clair, accent jaune, liens cyan.
- Sidebar plus compacte, proche table des matieres de formation.
- Titres de lecon plus grands, plus editoriaux, avec paragraphes d'introduction mieux aeres.
- Suppression visuelle de la plupart des blocs : academy-card, exbox, intro-card, home-card, reading-step et vocab-item deviennent des sections de texte separees par des filets.
- Les blocs restent reserves aux usages vraiment utiles : regles, avertissements, tableaux, schemas, navigation et liens d'accueil.
- Les objectifs de lecon et prerequis deviennent des zones de lecture discretes, sans effet carte.
- Les graphiques et tableaux gardent un encadrement sombre pour rester lisibles et clairement separables du texte.

Fichier principal
- style.css

Notes
- La structure HTML existante est conservee pour ne pas casser les ancres ni les scripts precedents.
- La refonte est volontairement appliquee par une couche CSS finale afin de rester reversible et facile a ajuster.
