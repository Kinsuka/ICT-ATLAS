ICT Atlas - README V55
======================

Objectif
--------
V55 renforce les points demandes apres V54 :

- comment definir une ligne de liquidite sans la traiter comme un trait magique ;
- comment savoir ou, quand et comment entrer ;
- comment definir un TP maximum logique ;
- comment securiser un trade sans pretendre prevoir le retournement.

Ajouts principaux
-----------------
1. 27-fondations-liquidite.html
   Nouvelle section : "Comment definir une ligne de liquidite ?"
   Idee cle : une ligne de liquidite est une zone visible ou des ordres sont
   probables. On part d'un high/low visible, on pense en zone de meches, puis
   on valide par la concentration probable de stops, breakouts et TP.

2. 28-fondations-entree.html
   Nouvelle section : "Quand et comment entrer"
   Idee cle : l'entree n'est pas le point de depart du raisonnement. Elle vient
   apres la cible, le sweep, le rejet, le displacement et le retour dans une
   zone exploitable. La section distingue entree limite, entree confirmation et
   no trade.

3. 29-fondations-stop-tp.html
   Nouvelle section : "TP maximum logique et securisation"
   Idee cle : le TP maximum n'est pas le top. C'est la prochaine liquidite
   majeure non consommee ou la raison initiale du trade est payee. La
   securisation se fait par regle : partiel, break-even, stop structurel ou
   sortie du runner apres cassure inverse.

Validation
----------
Les pages sont regenerees via :

- python3 add_v54_foundation_module.py
- python3 course_platform_layout.py

L'audit attendu reste :

- 29 lecons dans la navigation ;
- aucun lien HTML manquant ;
- aucune ancre manquante ;
- aucun texte SVG coupe ;
- aucun marqueur de point sans contraste.
