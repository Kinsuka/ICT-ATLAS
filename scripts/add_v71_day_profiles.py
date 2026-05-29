from pathlib import Path

from bs4 import BeautifulSoup


ROOT = Path(".")


def remove_existing(soup, section_id):
    old = soup.find(id=section_id)
    if old:
        old.decompose()


def insert_section(path, section_id, title, intro, anchor_id=None, label="Sessions"):
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    remove_existing(soup, section_id)
    html = f"""
    <section class="card" id="{section_id}">
      <header><h2>{title}</h2><span>{label}</span></header>
      <p>{intro}</p>
      <div class="section-links">
        <a class="section-link" href="39-profils-journee-sessions.html"><h3>Chapitre profils de journée</h3><p>Trend day, range day, reversal day, continuation PM et no-trade day.</p></a>
        <a class="section-link" href="39-profils-journee-sessions.html#profiles-session-playbook"><h3>Playbook session</h3><p>Adapter le setup au profil dominant et à la phase de session.</p></a>
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

    rows = table.find_all("tr")
    for row in rows:
        cells = row.find_all("td")
        if cells and "Profils de journée" in cells[0].get_text(" ", strip=True):
            row.decompose()
            break

    new_row = BeautifulSoup(
        """
        <tr>
          <td><strong>Profils de journée</strong></td>
          <td><a class="glosslink" href="39-profils-journee-sessions.html">Référence principale</a></td>
          <td>
            <a class="glosslink" href="39-profils-journee-sessions.html#profiles-map">profils</a>,
            <a class="glosslink" href="39-profils-journee-sessions.html#profiles-abc">cas A/B/C/D</a>,
            <a class="glosslink" href="39-profils-journee-sessions.html#profiles-session-playbook">playbook</a>
          </td>
        </tr>
        """,
        "html.parser",
    ).tr

    insert_after = None
    for row in table.find_all("tr"):
        cells = row.find_all("td")
        if cells and "SMT" in cells[0].get_text(" ", strip=True):
            insert_after = row
            break
    if insert_after:
        insert_after.insert_after(new_row)
    else:
        table.append(new_row)
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
                "23. Profils de journée",
                "24. Setups cœur",
                "25. Graphique réel",
                "26. Variantes",
                "27. Failures",
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
        "v71-accueil-profils-journee",
        "Chapitre dédié : profils de journée et sessions avancées",
        "Avant les setups cœur, on ajoute le filtre de comportement de journée : trend, range, reversal, continuation PM ou no-trade.",
        "v70-accueil-smt-divergence",
    )
    insert_section(
        ROOT / "38-smt-divergence.html",
        "v71-bridge-profils-journee",
        "Après SMT : nommer le profil de journée",
        "Une SMT ne vaut pas pareil dans un trend day, un range day ou une journée de reversal. Le profil décide si la confluence mérite d’être utilisée.",
        "smt-process",
    )
    insert_section(
        ROOT / "04-setups-core.html",
        "v71-bridge-profils-journee",
        "Avant les setups : lire le profil de journée",
        "Un setup cœur doit être cohérent avec le comportement de la session : continuation, rejet de range, reversal confirmé ou no-trade.",
        "v70-bridge-smt-divergence",
    )
    insert_section(
        ROOT / "15-index-concepts.html",
        "v71-index-profils-journee",
        "Profils de journée / sessions",
        "Retrouve la leçon qui relie les setups à trend day, range day, reversal day, continuation PM et no-trade day.",
        "v70-index-smt-divergence",
    )
    update_index_row()
    update_home_order()


def main():
    enrich()


if __name__ == "__main__":
    main()
