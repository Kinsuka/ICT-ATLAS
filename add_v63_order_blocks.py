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
        <a class="section-link" href="31-order-blocks.html"><h3>Chapitre Order Blocks</h3><p>Comprendre OB valide, OB faible, OB mitigé et breaker avant de chercher une entrée.</p></a>
        <a class="section-link" href="31-order-blocks.html#ob-checklist"><h3>Checklist OB</h3><p>Contexte, liquidité, displacement, retour, invalidation et TP.</p></a>
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


def update_concept_index():
    path = ROOT / "15-index-concepts.html"
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    ob_button = soup.find("button", attrs={"data-glossary-term": "OB"})
    if not ob_button:
        path.write_text(str(soup), encoding="utf-8")
        return
    row = ob_button.find_parent("tr")
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
            '<a class="glosslink" href="31-order-blocks.html">Référence principale</a>',
            "html.parser",
        )
    )
    cells[2].clear()
    cells[2].append(
        BeautifulSoup(
            '<a class="glosslink" href="31-order-blocks.html#ob-checklist">checklist</a>, '
            '<a class="glosslink" href="04-setups-core.html#ob-bull">setup</a>, '
            '<a class="glosslink" href="05-variantes.html#ob-bear">variante</a>',
            "html.parser",
        )
    )
    path.write_text(str(soup), encoding="utf-8")


def enrich():
    insert_section(
        ROOT / "04-setups-core.html",
        "v63-bridge-order-blocks",
        "Avant les setups : comprendre les Order Blocks",
        "Les setups utilisent souvent les OB comme zone de retour. Cette leçon dédiée évite de confondre une zone validée avec une bougie choisie après coup.",
    )
    insert_section(
        ROOT / "15-index-concepts.html",
        "v63-index-order-blocks",
        "Order Blocks",
        "Retrouve la leçon dédiée aux OB, à la mitigation et aux breakers.",
        "v62-index-cas-replay",
    )
    insert_section(
        ROOT / "index.html",
        "v63-accueil-order-blocks",
        "Chapitre dédié : Order Blocks",
        "Les zones ICT méritent leurs propres chapitres. On commence par les OB, car ils sont centraux et souvent mal compris.",
        "v59-replay-lab-accueil",
    )
    update_concept_index()


def main():
    enrich()


if __name__ == "__main__":
    main()
