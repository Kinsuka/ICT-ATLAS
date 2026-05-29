from pathlib import Path

from bs4 import BeautifulSoup


ROOT = Path(".")

CASE_GROUPS = [
    (
        "Liquidite",
        [
            ("CAS-01", "Carte de liquidite propre", "Identifier BSL/SSL, PDH/PDL, equal highs/lows et liquidite interne/externe avant toute entree."),
            ("CAS-02", "Cible deja consommee", "Montrer un mouvement ou la DOL principale a deja ete touchee et ou les entrees tardives perdent leur logique."),
        ],
    ),
    (
        "Prise et reaction",
        [
            ("CAS-03", "Sweep + rejet exploitable", "Observer une prise de liquidite suivie d'un rejet clair puis d'un displacement."),
            ("CAS-04", "Breakout accepte", "Montrer une sortie de range avec maintien hors range, sans retour immediat."),
            ("CAS-05", "Failed breakout", "Montrer une cassure visible puis une reintegration rapide de la range."),
        ],
    ),
    (
        "Entree et gestion",
        [
            ("CAS-06", "Entree causale complete", "Relier contexte, liquidite, MSS, FVG/OB, invalidation et TP logique."),
            ("CAS-07", "Entree trop tot", "Montrer un cas ou l'entree precede le displacement ou la confirmation structurelle."),
            ("CAS-08", "TP trop proche ou trop ambitieux", "Comparer le risque avec la liquidite disponible et refuser si le R ne justifie pas le trade."),
        ],
    ),
    (
        "Psychologie",
        [
            ("CAS-09", "Bon no trade", "Documenter un signal tentant mais refuse pour cause de contexte incomplet."),
            ("CAS-10", "Apres perte", "Rejouer une session ou la meilleure decision est de stopper ou reduire le risque apres une erreur."),
        ],
    ),
]


def remove_existing(soup, section_id):
    old = soup.find(id=section_id)
    if old:
        old.decompose()


def case_cards():
    sections = []
    for group, cases in CASE_GROUPS:
        cards = []
        for case_id, title, desc in cases:
            cards.append(
                f"""
                <article class="case-slot">
                  <div class="case-slot-head"><span>{case_id}</span><small>à valider</small></div>
                  <h3>{title}</h3>
                  <p>{desc}</p>
                  <ul>
                    <li>Capture avant décision obligatoire.</li>
                    <li>Capture après révélation obligatoire.</li>
                    <li>Décision écrite avant résultat.</li>
                  </ul>
                </article>
                """
            )
        sections.append(
            f"""
            <section class="card case-library-section" id="cas-{group.lower().replace(' ', '-')}">
              <header><h2>{group}</h2><span>Slots de cas</span></header>
              <div class="case-library-grid">{''.join(cards)}</div>
            </section>
            """
        )
    return "".join(sections)


def write_case_library_page():
    html = f"""<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>ICT Atlas - Bibliotheque de cas replay</title>
  <link rel="stylesheet" href="style.css" />
</head>
<body>
  <div class="app-shell">
    <aside class="site-nav" aria-label="Navigation cas replay">
      <div class="nav-brand"><strong>ICT Atlas</strong><span>Replay cases</span></div>
      <div class="course-nav-title"><span>Cas replay</span><small>vérifiables</small></div>
      <div class="course-part">
        <div class="course-part-head"><span>Retour</span><strong>Pratique</strong></div>
        <ol class="course-lessons">
          <li class="course-lesson"><a href="30-replay-lab.html"><span class="lesson-bullet">1</span><span class="lesson-link-text"><strong>Replay Lab</strong><small>Protocole</small></span></a></li>
          <li class="course-lesson"><a href="ressources-pratiques.html"><span class="lesson-bullet">2</span><span class="lesson-link-text"><strong>Ressources</strong><small>Templates</small></span></a></li>
          <li class="course-lesson"><a href="08-quiz.html"><span class="lesson-bullet">3</span><span class="lesson-link-text"><strong>Quiz</strong><small>Décision</small></span></a></li>
          <li class="course-lesson"><a href="15-index-concepts.html"><span class="lesson-bullet">4</span><span class="lesson-link-text"><strong>Index</strong><small>Concepts</small></span></a></li>
        </ol>
      </div>
      <div class="nav-help"><strong>Principe</strong><br />Un cas n'entre dans la bibliothèque qu'avec capture avant, capture après et décision écrite.</div>
    </aside>
    <main class="page" id="contenu">
      <div class="hero">
        <h1>Bibliothèque de cas replay</h1>
        <p>Un espace pour transformer les exercices en cas vérifiables : statut, captures attendues, décision avant résultat et correction.</p>
        <div class="tagline"><span>Cas vérifiables</span><span>Avant / après</span><span>Anti-biais</span></div>
      </div>
      <section class="card" id="principe-validation">
        <header><h2>Règle d’entrée dans la bibliothèque</h2><span>Qualité</span></header>
        <p>On ne publie pas un cas parce qu'il ressemble à un setup après coup. Un cas doit être reproductible en replay et documenté avant que le résultat soit connu.</p>
        <div class="academy-grid">
          <div class="academy-card"><h3>Avant</h3><p>Marché, timeframe, date, heure de départ, contexte HTF, liquidité visible et question posée.</p></div>
          <div class="academy-card"><h3>Pendant</h3><p>Décision écrite : buy, sell, no trade, attendre. Stop, invalidation et TP si une entrée est envisagée.</p></div>
          <div class="academy-card"><h3>Après</h3><p>Résultat, classification, correction, capture après révélation et lien vers le journal ou le backtest.</p></div>
        </div>
        <div class="rule-block"><strong>Règle :</strong> sans capture avant décision, le cas reste un exemple personnel, pas un cas validé du cours.</div>
      </section>
      <section class="card" id="workflow-ajout-cas">
        <header><h2>Workflow pour ajouter un vrai cas</h2><span>Méthode</span></header>
        <div class="replay-steps">
          <div><strong>1</strong><span>Choisir le phénomène : sweep, failed breakout, entrée causale, no trade, TP.</span></div>
          <div><strong>2</strong><span>Ouvrir le replay au bon moment et prendre une capture avant décision.</span></div>
          <div><strong>3</strong><span>Remplir la fiche `cas-replay-validation.md` et le CSV replay.</span></div>
          <div><strong>4</strong><span>Révéler la suite, capturer l'après, puis classer le cas sans réécrire l'histoire.</span></div>
          <div><strong>5</strong><span>Promouvoir le slot en cas validé seulement si les preuves sont complètes.</span></div>
        </div>
      </section>
      {case_cards()}
      <section class="card" id="templates-cas-replay">
        <header><h2>Templates liés aux cas</h2><span>Documents</span></header>
        <div class="section-links">
          <a class="section-link" href="templates/cas-replay-validation.md" download><h3>Validation d’un cas replay</h3><p>Fiche Markdown pour documenter les preuves avant/après.</p></a>
          <a class="section-link" href="templates/replay-lab.csv" download><h3>Replay Lab CSV</h3><p>Table pour suivre tous les cas travaillés.</p></a>
          <a class="section-link" href="templates/backtest-ict.csv" download><h3>Backtest ICT</h3><p>Table pour regrouper les occurrences validées.</p></a>
        </div>
      </section>
    </main>
  </div>
</body>
</html>
"""
    (ROOT / "replay-cases.html").write_text(html, encoding="utf-8")


def insert_section(path, section_id, title, intro, anchor_id=None):
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    remove_existing(soup, section_id)
    html = f"""
    <section class="card" id="{section_id}">
      <header><h2>{title}</h2><span>Cas replay</span></header>
      <p>{intro}</p>
      <div class="section-links">
        <a class="section-link" href="replay-cases.html"><h3>Bibliothèque de cas replay</h3><p>Slots de cas vérifiables et méthode pour ajouter de vrais exemples.</p></a>
        <a class="section-link" href="templates/cas-replay-validation.md" download><h3>Fiche validation</h3><p>Documenter capture avant, décision, capture après et correction.</p></a>
      </div>
    </section>
    """
    fragment = BeautifulSoup(html, "html.parser")
    anchor = soup.find(id=anchor_id) if anchor_id else soup.find("div", class_="page-meta-dashboard")
    if anchor:
        anchor.insert_after(fragment)
    else:
        main = soup.find("main", class_="page")
        if main:
            main.insert(3, fragment)
    path.write_text(str(soup), encoding="utf-8")


def enrich_pages():
    insert_section(
        ROOT / "30-replay-lab.html",
        "v62-bibliotheque-cas",
        "Bibliothèque de cas replay vérifiables",
        "Le Replay Lab explique comment s'entraîner. La bibliothèque organise les cas qui méritent d'être conservés, validés et retravaillés.",
        "fiche-cas-replay",
    )
    insert_section(
        ROOT / "08-quiz.html",
        "v62-cas-replay-quiz",
        "Après les quiz : documenter un cas réel",
        "Un quiz vérifie une reconnaissance. Un cas replay vérifié prouve que tu peux appliquer la décision dans le bruit du marché.",
    )
    insert_section(
        ROOT / "15-index-concepts.html",
        "v62-index-cas-replay",
        "Cas replay vérifiables",
        "Retrouve les slots de cas à remplir avec captures et décisions écrites.",
        "v59-index-replay-lab",
    )
    insert_section(
        ROOT / "ressources-pratiques.html",
        "v62-ressources-cas-replay",
        "Cas replay et validation",
        "Ces fichiers servent à faire entrer un cas dans la bibliothèque seulement s'il est documenté avant/après.",
        "templates",
    )


def main():
    write_case_library_page()
    enrich_pages()


if __name__ == "__main__":
    main()
