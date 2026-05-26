ICT Atlas - README V56
======================

Objectif
--------
V56 est une passe de profondeur pedagogique sur les fondations. Elle n'ajoute
pas de nouveau chapitre : elle ralentit les explications la ou un debutant peut
se perdre, en reliant chaque concept a sa cause, sa consequence et sa decision.

Chapitres renforces
-------------------
1. 11-mecanique-marches.html
   - Ajout "Lire la cause avant la forme".
   - Ajout "Absorption, deplacement, bruit".
   - But : comprendre qu'un FVG, un OB ou un MSS est une trace d'execution, pas
     un dessin a reconnaitre mecaniquement.

2. 21-liquidite-deplacement.html
   - Ajout "Pourquoi le prix accelere apres une prise de liquidite ?"
   - But : expliquer la chaine avant / pendant / apres la prise de liquidite.

3. 27-fondations-liquidite.html
   - Ajout "Donner du poids a une liquidite".
   - But : distinguer liquidite forte, moyenne ou faible selon visibilite,
     fraicheur, position et distance.

4. 28-fondations-entree.html
   - Ajout "Sortir de la paralysie : quatre etats avant le clic".
   - But : enseigner quand attendre, quand preparer, quand executer, et quand
     refuser.

5. 29-fondations-stop-tp.html
   - Ajout "Arbre de decision : TP, securisation, sortie".
   - But : securiser par regle, sans pretendre predire le retournement.

6. 22-structure-trend-range.html
   - Ajout "Pourquoi l'environnement passe avant le setup".
   - But : faire comprendre qu'un signal ICT ne vaut rien sans son regime de
     marche : trend, range ou transition.

Generation
----------
La passe V56 est appliquee par :

- python3 add_v56_foundation_depth.py
- python3 course_platform_layout.py

Validation attendue
-------------------
- 29 lecons conservees.
- Aucun lien HTML manquant.
- Aucune ancre interne manquante.
- Aucun texte SVG coupe.
- Aucun marqueur de point sans contraste.

Intention pedagogique
---------------------
Les fondations doivent expliquer pourquoi les concepts existent avant de montrer
comment les utiliser. Le cours doit eviter le piege classique : reconnaitre un
setup sans comprendre la liquidite, l'entree, l'invalidation et la sortie.
