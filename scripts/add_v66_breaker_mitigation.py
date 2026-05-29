from pathlib import Path

from bs4 import BeautifulSoup


ROOT = Path(".")


def remove_existing(soup, section_id):
    old = soup.find(id=section_id)
    if old:
        old.decompose()


def insert_section(path, section_id, title, intro, anchor_id=None):
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    remove_existing(soup, section_id)
    html = f"""
    <section class="card" id="{section_id}">
      <header><h2>{title}</h2><span>Zones ICT</span></header>
      <p>{intro}</p>
      <div class="section-links">
        <a class="section-link" href="34-breaker-mitigation.html"><h3>Chapitre Breaker / Mitigation</h3><p>Distinguer zone active, mitigation, invalidation, breaker valide et faux breaker.</p></a>
        <a class="section-link" href="34-breaker-mitigation.html#breaker-checklist"><h3>Checklist Breaker</h3><p>Zone initiale, invalidation, MSS, retour, objectif et risque.</p></a>
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


def update_concept_row():
    path = ROOT / "15-index-concepts.html"
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    button = soup.find("button", attrs={"data-glossary-term": "Breaker"})
    if not button:
        path.write_text(str(soup), encoding="utf-8")
        return
    row = button.find_parent("tr")
    if not row:
        path.write_text(str(soup), encoding="utf-8")
        return
    cells = row.find_all("td")
    if len(cells) < 3:
        path.write_text(str(soup), encoding="utf-8")
        return
    cells[1].clear()
    cells[1].append(
        BeautifulSoup(
            '<a class="glosslink" href="34-breaker-mitigation.html">Référence principale</a>',
            "html.parser",
        )
    )
    cells[2].clear()
    cells[2].append(
        BeautifulSoup(
            '<a class="glosslink" href="34-breaker-mitigation.html#breaker-checklist">checklist</a>, '
            '<a class="glosslink" href="04-setups-core.html#breaker-bear">setup</a>, '
            '<a class="glosslink" href="05-variantes.html#breaker-bull">variante</a>',
            "html.parser",
        )
    )
    path.write_text(str(soup), encoding="utf-8")


def enrich():
    insert_section(
        ROOT / "index.html",
        "v66-accueil-breaker-mitigation",
        "Chapitre dédié : Breaker et mitigation",
        "Après le MSS, on clarifie ce qui arrive aux zones : elles peuvent tenir, être mitigées, casser ou changer de rôle.",
        "v65-accueil-mss-shift",
    )
    insert_section(
        ROOT / "04-setups-core.html",
        "v66-bridge-breaker-mitigation",
        "Avant les setups : comprendre breaker et mitigation",
        "Les breakers sont puissants mais souvent mal nommés. Cette leçon dédiée évite de transformer chaque zone cassée en setup.",
        "v65-bridge-mss-shift",
    )
    insert_section(
        ROOT / "15-index-concepts.html",
        "v66-index-breaker-mitigation",
        "Breaker / mitigation",
        "Retrouve la leçon dédiée aux zones actives, mitigées, invalidées et aux breakers exploitables.",
        "v65-index-mss-shift",
    )
    update_concept_row()


def main():
    enrich()


if __name__ == "__main__":
    main()
