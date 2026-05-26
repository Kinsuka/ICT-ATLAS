ICT Atlas - README V54
======================

Objectif
--------
V54 renforce les fondations debutant autour de la chaine :

Liquidite -> Entree -> Stop -> TP

Le but est de rendre le cours plus autonome avant les setups avances. On explique
d'abord ou le prix peut chercher des ordres, puis pourquoi une entree devient
defendable, puis ou le scenario est invalide et quelles cibles paient le trade.

Nouvelles lecons
----------------
Trois lecons ont ete ajoutees apres "Comprenez le deplacement du prix" et avant
"Comprenez trend, range et transitions".

1. 27-fondations-liquidite.html
   Titre navigation : Lisez la liquidite
   Contenu : BSL/SSL, PDH/PDL, Asia High/Low, equal highs/lows, liquidite
   interne/externe, cible vs declencheur, cas A/B/C.

2. 28-fondations-entree.html
   Titre navigation : Construisez le scenario d'entree
   Contenu : sweep, rejet, displacement, MSS, FVG/CE/OB, sequence complete,
   entrees trop tot, entree apres DOL, entree sans deplacement.

3. 29-fondations-stop-tp.html
   Titre navigation : Placez stop, invalidation et TP
   Contenu : stop logique, invalidation structurelle, TP1 interne, TP2 externe,
   refus du trade si l'asymetrie ne paie pas le risque.

Navigation
----------
Le cours passe a 29 lecons.

Sequence cle :

04. Mecanique des marches
05. Langage ICT en contexte
06. Deplacement du prix
07. Liquidite
08. Scenario d'entree
09. Stop, invalidation et TP
10. Trend, range et transitions
11. Concept, setup et plan

Fichiers enrichis
-----------------
- course_platform_layout.py : ajout des trois lecons, objectifs et compteur.
- index.html : bloc V54 + ordre recommande mis a jour.
- 15-index-concepts.html : entree rapide vers les cas V54.
- 21-liquidite-deplacement.html : pont vers le module fondation.
- 11-mecanique-marches.html : schema ordres -> absorption -> deplacement -> mitigation.
- 12-gestion-risque.html : schema entree / stop / TP1 / TP2.
- 09-synthese.html : checklist Liquidite -> Entree -> Stop -> TP.

Generation
----------
Le fichier add_v54_foundation_module.py genere les trois nouvelles pages et
insere les sections V54 de maniere idempotente.

Commandes de validation utilisees
---------------------------------
- python3 -m py_compile add_v54_foundation_module.py course_platform_layout.py
- python3 add_v54_foundation_module.py
- python3 course_platform_layout.py
- node --check glossary-panel.js
- audit HTML local : fichiers, liens internes, ancres, viewBox SVG, clipping texte,
  marqueurs cercles, pages sans SVG

Resultat attendu
----------------
- 31 fichiers HTML au total.
- 29 lecons dans la navigation.
- Aucun lien HTML manquant.
- Aucune ancre interne manquante.
- Aucun texte SVG coupe selon l'audit heuristique.
- Aucune page de lecon sans SVG dans le parcours principal.
- Tous les nouveaux graphiques ont des annotations lisibles et des marqueurs
  contrastes.
