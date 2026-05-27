from pathlib import Path

from bs4 import BeautifulSoup


ROOT = Path(".")

RESOURCES = [
    ("templates/journal-trades.csv", "Journal de trades", "CSV pour documenter trades, no trades, emotion, respect du plan et resultat en R."),
    ("templates/backtest-ict.csv", "Backtest ICT", "CSV pour tester un setup sur echantillon : contexte, DOL, sweep, MSS, entree, resultat."),
    ("templates/checklist-session.md", "Checklist session", "Markdown a lire avant, pendant et apres la session pour eviter les decisions improvisees."),
    ("templates/review-post-session.md", "Review post-session", "Markdown pour separer trade conforme, erreur, emotion et correction unique."),
    ("templates/plan-trading-ict.md", "Plan de trading ICT", "Markdown pour formaliser setups autorises, risque, TP, BE et regles non negociables."),
    ("templates/regles-prop-firm.md", "Regles prop firm", "Markdown pour traduire les limites prop firm en regles defensives concretes."),
    ("templates/replay-lab.csv", "Replay Lab", "CSV pour documenter les cas bar replay : contexte, decision, resultat et correction."),
]


def remove_existing(soup, section_id):
    old = soup.find(id=section_id)
    if old:
        old.decompose()


def resource_cards(include_all=True, selected=None):
    items = RESOURCES if include_all else [item for item in RESOURCES if item[0] in selected]
    cards = []
    for href, title, desc in items:
        cards.append(
            f'<a class="section-link" href="{href}" download><h3>{title}</h3><p>{desc}</p></a>'
        )
    return "".join(cards)


def write_resources_page():
    cards = resource_cards()
    html = f"""<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>ICT Atlas - Ressources pratiques</title>
  <link rel="stylesheet" href="style.css" />
</head>
<body>
  <div class="app-shell">
    <aside class="site-nav" aria-label="Navigation ressources">
      <div class="nav-brand"><strong>ICT Atlas</strong><span>Outils pratiques</span></div>
      <div class="course-nav-title"><span>Ressources</span><small>templates</small></div>
      <div class="course-part">
        <div class="course-part-head"><span>Retour</span><strong>Cours</strong></div>
        <ol class="course-lessons">
          <li class="course-lesson"><a href="index.html"><span class="lesson-bullet">1</span><span class="lesson-link-text"><strong>Accueil</strong><small>Positionnement</small></span></a></li>
          <li class="course-lesson"><a href="19-preuve-statistique.html"><span class="lesson-bullet">2</span><span class="lesson-link-text"><strong>Preuve statistique</strong><small>Backtest</small></span></a></li>
          <li class="course-lesson"><a href="20-workflow-session.html"><span class="lesson-bullet">3</span><span class="lesson-link-text"><strong>Workflow session</strong><small>Checklist</small></span></a></li>
          <li class="course-lesson"><a href="15-index-concepts.html"><span class="lesson-bullet">4</span><span class="lesson-link-text"><strong>Index</strong><small>Concepts</small></span></a></li>
        </ol>
      </div>
      <div class="nav-help"><strong>Methode</strong><br />Un template ne remplace pas le plan : il force le plan a devenir observable.</div>
    </aside>
    <main class="page" id="contenu">
      <div class="hero">
        <h1>Ressources pratiques</h1>
        <p>Templates pour passer de la lecture a la pratique documentee : journal, backtest, checklist, review, plan et prop firm.</p>
        <div class="tagline"><span>Journal</span><span>Backtest</span><span>Execution</span></div>
      </div>
      <section class="card" id="ressources-mode-emploi">
        <header><h2>Comment utiliser ces fichiers</h2><span>Mode d'emploi</span></header>
        <div class="academy-grid">
          <div class="academy-card"><h3>Avant session</h3><p>Ouvre la checklist et le plan de trading. Si une condition obligatoire manque, le trade reste une observation.</p></div>
          <div class="academy-card"><h3>Pendant replay ou live</h3><p>Remplis le journal seulement avec ce que tu savais au moment de la decision, pas apres avoir vu la suite.</p></div>
          <div class="academy-card"><h3>Apres session</h3><p>Fais la review. Une seule correction pour demain suffit : trop de changements rendent le test illisible.</p></div>
        </div>
        <div class="rule-block"><strong>Regle :</strong> si un setup n'est pas documente, il n'existe pas dans ton echantillon.</div>
      </section>
      <section class="card" id="templates">
        <header><h2>Templates telechargeables</h2><span>Outils</span></header>
        <div class="section-links">{cards}</div>
      </section>
    </main>
  </div>
</body>
</html>
"""
    (ROOT / "ressources-pratiques.html").write_text(html, encoding="utf-8")


def insert_resource_section(path, section_id, title, intro, selected, anchor_id=None):
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    remove_existing(soup, section_id)
    cards = resource_cards(include_all=False, selected=selected)
    html = f"""<section class="card" id="{section_id}"><header><h2>{title}</h2><span>Outils pratiques</span></header><p>{intro}</p><div class="section-links">{cards}<a class="section-link" href="ressources-pratiques.html"><h3>Toutes les ressources</h3><p>Ouvrir la page centrale avec tous les templates du cours.</p></a></div></section>"""
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
    insert_resource_section(
        ROOT / "index.html",
        "v58-ressources-accueil",
        "Outils pratiques pour travailler le cours",
        "Ces templates transforment la lecture en preuves : decisions ecrites, backtests, journal et reviews.",
        {
            "templates/journal-trades.csv",
            "templates/backtest-ict.csv",
            "templates/checklist-session.md",
        },
        "positionnement-public",
    )
    insert_resource_section(
        ROOT / "19-preuve-statistique.html",
        "v58-ressources-preuve",
        "Templates pour prouver un edge",
        "Un edge ne se prouve pas dans la tete : il se documente ligne par ligne, occurrence par occurrence.",
        {
            "templates/backtest-ict.csv",
            "templates/journal-trades.csv",
            "templates/plan-trading-ict.md",
        },
    )
    insert_resource_section(
        ROOT / "20-workflow-session.html",
        "v58-ressources-workflow",
        "Templates pour executer une session",
        "Le workflow devient utile quand il est visible avant la session et relu apres la session.",
        {
            "templates/checklist-session.md",
            "templates/review-post-session.md",
            "templates/journal-trades.csv",
        },
    )
    insert_resource_section(
        ROOT / "12-gestion-risque.html",
        "v58-ressources-risque",
        "Templates pour relier risque et resultat en R",
        "Le risque ne doit pas rester theorique : chaque trade doit montrer stop, taille, resultat et respect du plan.",
        {
            "templates/journal-trades.csv",
            "templates/backtest-ict.csv",
            "templates/plan-trading-ict.md",
        },
    )
    insert_resource_section(
        ROOT / "26-psychologie-trader.html",
        "v58-ressources-psychologie",
        "Templates pour rendre la psychologie observable",
        "Le mental ne se corrige pas en generalites. Il faut noter l'etat avant, pendant, apres, puis choisir une correction.",
        {
            "templates/review-post-session.md",
            "templates/checklist-session.md",
            "templates/journal-trades.csv",
        },
    )
    insert_resource_section(
        ROOT / "13-prop-firm.html",
        "v58-ressources-prop",
        "Templates pour proteger un compte prop firm",
        "Une prop firm se perd souvent par absence de regles d'arret. Ces templates rendent les limites non negociables.",
        {
            "templates/regles-prop-firm.md",
            "templates/checklist-session.md",
            "templates/review-post-session.md",
        },
    )
    insert_resource_section(
        ROOT / "15-index-concepts.html",
        "v58-index-ressources",
        "Ressources pratiques",
        "Retrouve les outils qui accompagnent le backtest, le journal, la session et la discipline.",
        {
            "templates/journal-trades.csv",
            "templates/backtest-ict.csv",
            "templates/checklist-session.md",
        },
        "index-alphabetique",
    )


def main():
    write_resources_page()
    enrich_pages()


if __name__ == "__main__":
    main()
