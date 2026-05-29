from pathlib import Path

from bs4 import BeautifulSoup


ROOT = Path(".")


def remove_existing(soup, section_id):
    old = soup.find(id=section_id)
    if old:
        old.decompose()


def insert_section(path, section_id, title, intro, links, anchor_id=None):
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    remove_existing(soup, section_id)
    cards = "".join(
        f'<a class="section-link" href="{href}"{download}><h3>{label}</h3><p>{desc}</p></a>'
        for href, label, desc, download in links
    )
    html = (
        f'<section class="card" id="{section_id}">'
        f'<header><h2>{title}</h2><span>Replay Lab</span></header>'
        f'<p>{intro}</p><div class="section-links">{cards}</div>'
        f'</section>'
    )
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
    replay_links = [
        ("30-replay-lab.html", "Ouvrir le Replay Lab", "Leçon dédiée au travail bar replay : cacher le futur, décider, corriger.", ""),
        ("templates/replay-lab.csv", "Template replay lab", "CSV pour documenter chaque cas réel travaillé en replay.", " download"),
    ]
    insert_section(
        ROOT / "index.html",
        "v59-replay-lab-accueil",
        "Replay Lab : entraîner la lecture sur graphique réel",
        "Le cours ne doit pas rester au niveau des schémas propres. Le Replay Lab ajoute une étape de pratique structurée avant les quiz.",
        replay_links,
        "v58-ressources-accueil",
    )
    insert_section(
        ROOT / "08-quiz.html",
        "v59-replay-lab-quiz",
        "Avant les quiz : passer par le replay",
        "Les quiz vérifient la reconnaissance. Le replay vérifie la décision dans le bruit réel du marché.",
        replay_links,
    )
    insert_section(
        ROOT / "19-preuve-statistique.html",
        "v59-replay-lab-preuve",
        "Replay et preuve statistique",
        "Un cas replay isolé n'est pas une preuve. Il devient utile quand il est noté dans un échantillon stable.",
        [
            ("30-replay-lab.html", "Replay Lab", "Transformer chaque exercice en observation exploitable.", ""),
            ("templates/backtest-ict.csv", "Backtest ICT", "Regrouper les occurrences pour mesurer l'edge.", " download"),
            ("templates/replay-lab.csv", "Fiche replay", "Noter le contexte, la décision et la correction du cas.", " download"),
        ],
    )
    insert_section(
        ROOT / "20-workflow-session.html",
        "v59-replay-lab-workflow",
        "Routine replay avant live",
        "Avant de chercher du live, travaille les mêmes heures en replay pour voir si tu respectes ton protocole sans pression.",
        [
            ("30-replay-lab.html", "Replay Lab", "Routine d'entraînement avant passage au live.", ""),
            ("templates/checklist-session.md", "Checklist session", "Préparer la session avant de lancer le replay.", " download"),
            ("templates/replay-lab.csv", "Fiche replay", "Documenter chaque décision sans regarder le futur.", " download"),
        ],
    )
    insert_section(
        ROOT / "15-index-concepts.html",
        "v59-index-replay-lab",
        "Replay Lab",
        "Retrouve la page d'entraînement qui relie cas réel, journal, backtest et correction.",
        replay_links,
        "v58-index-ressources",
    )


def main():
    enrich_pages()


if __name__ == "__main__":
    main()
