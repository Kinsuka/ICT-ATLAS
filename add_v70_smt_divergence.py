from pathlib import Path

from bs4 import BeautifulSoup


ROOT = Path(".")


def remove_existing(soup, section_id):
    old = soup.find(id=section_id)
    if old:
        old.decompose()


def insert_section(path, section_id, title, intro, anchor_id=None, label="Confluence"):
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    remove_existing(soup, section_id)
    html = f"""
    <section class="card" id="{section_id}">
      <header><h2>{title}</h2><span>{label}</span></header>
      <p>{intro}</p>
      <div class="section-links">
        <a class="section-link" href="38-smt-divergence.html"><h3>Chapitre SMT</h3><p>Lire divergence inter-marchés, non-confirmation et limites de corrélation.</p></a>
        <a class="section-link" href="38-smt-divergence.html#smt-checklist"><h3>Checklist SMT</h3><p>Marchés corrélés, niveau comparable, timing, contexte et confirmation.</p></a>
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
        if "SMT" not in cells[0].get_text(" ", strip=True):
            continue
        cells[1].clear()
        link = soup.new_tag("a", href="38-smt-divergence.html", **{"class": "glosslink"})
        link.string = "Référence principale"
        cells[1].append(link)
        cells[2].clear()
        items = [
            ("38-smt-divergence.html#smt-map", "bearish"),
            ("38-smt-divergence.html#smt-bullish", "bullish"),
            ("38-smt-divergence.html#smt-abc", "cas A/B/C"),
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
                "21. DOL et targets",
                "22. SMT et divergence",
                "23. Setups cœur",
                "24. Graphique réel",
                "25. Variantes",
                "26. Failures",
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
        "v70-accueil-smt-divergence",
        "Chapitre dédié : SMT et divergence inter-marchés",
        "Avant les setups cœur, on ajoute SMT comme confluence de liquidité, pas comme signal isolé.",
        "v69-accueil-dol-targets",
    )
    insert_section(
        ROOT / "37-dol-targets-hierarchie.html",
        "v70-bridge-smt-divergence",
        "Après les targets : lire la non-confirmation",
        "Quand un marché prend une cible et qu’un marché corrélé ne confirme pas, SMT peut signaler un affaiblissement. La réaction reste obligatoire.",
        "dol-checklist",
    )
    insert_section(
        ROOT / "04-setups-core.html",
        "v70-bridge-smt-divergence",
        "Avant les setups : utiliser SMT comme confluence",
        "SMT peut renforcer un setup, mais ne remplace ni la liquidité, ni le déplacement, ni l’invalidation.",
        "v69-bridge-dol-targets",
    )
    insert_section(
        ROOT / "15-index-concepts.html",
        "v70-index-smt-divergence",
        "SMT / divergence inter-marchés",
        "Retrouve la leçon dédiée aux divergences entre marchés corrélés et aux faux signaux de corrélation.",
        "v69-index-dol-targets",
    )
    update_index_row()
    update_home_order()


def main():
    enrich()


if __name__ == "__main__":
    main()
