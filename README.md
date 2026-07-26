# ICT-ATLAS

Mini-site autonome organisé autour de l’atlas visuel ICT : parcours, mécanique du prix, liquidité, structure trend/range, setups, variantes, contextes, quiz et synthèse.

Version actuelle :
- 41 leçons guidées.
- Pré-cours autonome hors parcours principal, organisé comme un mini-cours de 7 leçons avec exemples visuels répétés.
- Glossaire permanent accessible depuis toutes les pages.
- Graphismes SVG pédagogiques intégrés aux chapitres.
- Navigation pensée pour GitHub Pages.
- Fichier `llms.txt` pour aider les IA et lecteurs automatisés à comprendre la structure du cours.

Entrées utiles :
- Site : https://kinsuka.github.io/ICT-ATLAS/
- Pré-cours : https://kinsuka.github.io/ICT-ATLAS/pages/00-precours-bases-trading.html
- Guide IA : https://kinsuka.github.io/ICT-ATLAS/llms.txt
- Sitemap : https://kinsuka.github.io/ICT-ATLAS/sitemap.xml

## Lancer le site en local

```bash
npm run dev
```

Le site est ensuite disponible sur http://localhost:4173. Pour choisir un autre port :

```bash
npm run dev -- --port 4174
```

Pour simuler le cache et la compression d’un hébergement statique avant publication :

```bash
npm run preview
```

## Maintenir la navigation

La structure des 41 leçons possède une source unique : `data/course-navigation.json`.

```bash
npm run sync:navigation
npm run test:structure
```

La première commande régénère les sidebars et les liens précédent/suivant. La seconde vérifie leur ordre, la leçon active, les checkpoints, les liens internes, les ancres et la couverture du sitemap.

## Vérifier l’accessibilité

```bash
npm run test:a11y
```

La matrice parcourt automatiquement toutes les pages HTML sur desktop et mobile. Elle contrôle notamment les landmarks, titres, liens d’évitement, noms accessibles, références ARIA, identifiants, cibles tactiles, zoom, SVG, contraste sémantique et comportement clavier du glossaire.

## Vérifier les performances

```bash
npm run test:performance
```

Les budgets couvrent les 58 pages : poids HTML brut et gzip, poids SVG, CSS/JavaScript partagé, volume DOM, nombre de graphiques et absence de scripts bloquants. Le glossaire rapide est chargé à la demande, tandis que `.nojekyll` garde le déploiement GitHub Pages strictement statique.

## Vérifier le parcours utilisateur

```bash
npm run test:journey
```

Le test traverse réellement les 41 leçons sur desktop et mobile, vérifie la sortie vers le tableau de progression, les seuils des preuves locales et la route sans boucle jusqu’au programme de validation en 20 sessions.
