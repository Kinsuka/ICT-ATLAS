ICT Atlas V78 - Branche precours-bases-trading

Objectif
- Ajouter un pré-cours autonome, hors parcours principal, pour les bases trading indispensables.
- Transformer la page passerelle en mini-cours scolaire de 7 leçons avec plusieurs exemples visuels par concept.
- Ne pas modifier la structure des 41 leçons ICT.
- Garder le positionnement du cours principal : clarification ICT, avec passerelle facultative pour les débutants trading.

Ajouts
- pages/00-precours-bases-trading.html : accueil du mini-cours.
- pages/00-precours-01-graphique.html : bougies, OHLC, mèches, timeframe.
- pages/00-precours-02-structure.html : swing high/low, tendance, range, faux breakout.
- pages/00-precours-03-ordres.html : market, limit, stop, SL, TP.
- pages/00-precours-04-liquidite.html : niveaux visibles, stops, prise et réaction.
- pages/00-precours-05-trade-simple.html : long/short, entrée, invalidation, TP, no trade.
- pages/00-precours-06-risque.html : R, lot, spread, marge, levier.
- pages/00-precours-07-pont-ict.html : traduction vers BSL, SSL, DOL, sweep, displacement, MSS, FVG, CE, OB.

Mises à jour
- README.md référence le pré-cours.
- llms.txt explique que le pré-cours est autonome et hors progression 41 leçons.
- sitemap.xml référence la nouvelle page.
- tests/course-visual.spec.js inclut le pré-cours dans l'audit Playwright.

Approfondissement V79
- Chaque leçon reçoit une lecture guidée plus progressive.
- Ajout de blocs erreurs fréquentes / anti-confusion.
- Ajout de corrections masquées aux exercices clés.
- Ajout de checkpoints de fin de leçon pour éviter que les chapitres se terminent trop vite.
- Priorité donnée aux notions structurantes :
  - graphique vers structure ;
  - structure vers ordres ;
  - ordres vers liquidité ;
  - liquidité vers trade simple ;
  - trade simple vers risque ;
  - risque vers vocabulaire ICT.
