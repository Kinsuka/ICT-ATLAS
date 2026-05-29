from pathlib import Path

from bs4 import BeautifulSoup


ROOT = Path(".")


def remove_existing(soup, section_id):
    old = soup.find(id=section_id)
    if old:
        old.decompose()


def insert_section(path, section_id, title, intro, anchor_id=None, label="Ancrage"):
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    remove_existing(soup, section_id)
    html = f"""
    <section class="card" id="{section_id}">
      <header><h2>{title}</h2><span>{label}</span></header>
      <p>{intro}</p>
      <div class="section-links">
        <a class="section-link" href="36-ote-dealing-range.html"><h3>Chapitre OTE / Dealing Range</h3><p>Choisir la bonne range, ancrer le swing et refuser les OTE forcés.</p></a>
        <a class="section-link" href="36-ote-dealing-range.html#ote-checklist"><h3>Checklist OTE</h3><p>Range, ancrage, confluence, réaction, invalidation et TP disponible.</p></a>
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


def update_index_row():
    path = ROOT / "15-index-concepts.html"
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    table = soup.find("table", class_="référence-table")
    if not table:
        path.write_text(str(soup), encoding="utf-8")
        return
    for row in table.find_all("tr"):
        cells = row.find_all("td")
        if not cells:
            continue
        if "OTE" not in cells[0].get_text(" ", strip=True):
            continue
        cells[1].clear()
        link = soup.new_tag("a", href="36-ote-dealing-range.html", **{"class": "glosslink"})
        link.string = "Référence principale"
        cells[1].append(link)
        cells[2].clear()
        items = [
            ("36-ote-dealing-range.html#ote-ancrage", "ancrage"),
            ("36-ote-dealing-range.html#ote-abc", "cas A/B/C"),
            ("08-quiz.html#quiz-ote-good-bad", "quiz"),
        ]
        for index, (href, label) in enumerate(items):
            if index:
                cells[2].append(", ")
            item = soup.new_tag("a", href=href, **{"class": "glosslink"})
            item.string = label
            cells[2].append(item)
        break
    path.write_text(str(soup), encoding="utf-8")


def update_home_order():
    path = ROOT / "index.html"
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    for card in soup.find_all("div", class_="home-card"):
        title = card.find("h3")
        if not title or "Ordre recommandé" not in title.get_text(" ", strip=True):
            continue
        summary = card.find("p")
        if summary:
            summary.string = (
                "La progression part de la mécanique, solidifie le trajet Liquidité -> Entrée -> Stop -> TP, "
                "puis construit les zones ICT une par une avant les setups."
            )
        old_list = card.find("ul")
        if old_list:
            old_list.clear()
            items = [
                "02. Modèle mental",
                "03. Parcours",
                "04. Mécanique",
                "05. Langage ICT en contexte",
                "06. Liquidité et déplacement",
                "07. Lire la liquidité",
                "08. Construire l'entrée",
                "09. Stop, invalidation et TP",
                "10. Trend/range/transitions",
                "11. Concept/plan",
                "12. Où/quand : Premium/Discount + Kill Zones",
                "13. Fondations de décision",
                "14. Top-down multi-timeframe",
                "15. Order Blocks",
                "16. FVG, imbalance et CE",
                "17. MSS et changement de contrôle",
                "18. Breaker et mitigation",
                "19. PD Arrays",
                "20. OTE et dealing range",
                "21. Setups cœur",
                "22. Graphique réel",
                "23. Variantes",
                "24. Failures",
            ]
            for item in items:
                li = soup.new_tag("li")
                li.string = item
                old_list.append(li)
        break
    path.write_text(str(soup), encoding="utf-8")


def enrich():
    insert_section(
        ROOT / "index.html",
        "v68-accueil-ote-dealing-range",
        "Chapitre dédié : OTE et Dealing Range",
        "Après la hiérarchie des zones, on apprend à choisir le bon swing d’ancrage pour éviter les OTE dessinés après coup.",
        "v67-accueil-pd-arrays",
    )
    insert_section(
        ROOT / "35-pd-arrays-hierarchie.html",
        "v68-bridge-ote-dealing-range",
        "Après les PD Arrays : ancrer l’OTE",
        "Une fois les zones classées, il faut encore choisir la bonne dealing range. C’est ce qui évite de tracer un fib sur un mouvement qui n’a aucune autorité.",
        "pd-rang",
    )
    insert_section(
        ROOT / "04-setups-core.html",
        "v68-bridge-ote-dealing-range",
        "Avant les setups : ancrer OTE et dealing range",
        "Un OTE n’est pas une entrée magique. Cette leçon dédiée explique le swing autorisé, la range de référence et les cas où le trade doit être refusé.",
        "v67-bridge-pd-arrays",
    )
    insert_section(
        ROOT / "15-index-concepts.html",
        "v68-index-ote-dealing-range",
        "OTE / Dealing Range",
        "Retrouve la leçon dédiée au bon ancrage du swing, aux OTE valides et aux OTE forcés.",
        "v67-index-pd-arrays",
    )
    update_index_row()
    update_home_order()


def main():
    enrich()


if __name__ == "__main__":
    main()
