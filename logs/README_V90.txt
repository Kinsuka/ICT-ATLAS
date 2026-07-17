ICT Atlas V90 — Micro Risk Ladder

- Ajout d'une porte post-forward test pour encadrer le passage eventuel au plus petit risque.
- Verrouillage automatique tant que le Forward Test Control n'affiche pas GO pedagogique.
- Controle interactif d'un bloc micro-risque : risque maximal, nombre de trades, resultat net, drawdown, stops journaliers et erreurs de processus.
- Separation explicite entre performance, discipline de taille et ruleset inchange.
- Verdicts operationnels : VERROUILLE, COLLECTER, STABILISER et PAUSE.
- PAUSE automatique si une limite de protection est touchee ou si le bloc minimum echoue.
- Message central : un GO forward autorise seulement une phase pedagogique de micro-risque, jamais une garantie ni un passage agressif au capital.
- Nouveau journal CSV dedie au bloc micro-risque.
- Raccord de la roadmap d'accueil vers la nouvelle etape lorsque le forward test est valide.
- Couverture Playwright du verrouillage, du deblocage par GO forward, de la stabilisation, de la pause, de la persistance et du reset.
