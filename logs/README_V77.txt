ICT Atlas V77 - Guide IA et découverte automatisée

Objectif
- Faciliter la lecture du site par les assistants IA et les outils automatisés quand seul le lien GitHub Pages est fourni.
- Donner un point d'entrée lisible, stable et complet au lieu de dépendre uniquement du rendu HTML.

Ajouts
- llms.txt à la racine du site :
  - positionnement du cours ;
  - règles d'interprétation ;
  - progression complète des 41 leçons ;
  - liens vers glossaire, index, ressources et templates.
- sitemap.xml :
  - accueil ;
  - guide llms.txt ;
  - 41 leçons ;
  - pages support.
- robots.txt :
  - autorise l'exploration ;
  - référence le sitemap ;
  - indique le guide LLM.

Mises à jour
- README.md corrigé de 26 à 41 leçons.
- index.html expose llms.txt et sitemap.xml dans le head via des liens alternatifs.

Validation
- Vérification locale de 105 URLs listées dans llms.txt/sitemap.xml.
- npm run test:e2e : 30 passed.

