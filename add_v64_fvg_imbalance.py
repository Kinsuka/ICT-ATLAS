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
        <a class="section-link" href="32-fvg-imbalance-ce.html"><h3>Chapitre FVG / Imbalance / CE</h3><p>Comprendre FVG net, imbalance, CE, gap ambigu, zone comblée et retour dangereux.</p></a>
        <a class="section-link" href="32-fvg-imbalance-ce.html#fvg-checklist"><h3>Checklist FVG</h3><p>Origine, displacement, position, retour, invalidation et TP.</p></a>
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


def update_concept_row(term, href, related_html):
    path = ROOT / "15-index-concepts.html"
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    button = soup.find("button", attrs={"data-glossary-term": term})
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
            f'<a class="glosslink" href="{href}">Référence principale</a>',
            "html.parser",
        )
    )
    cells[2].clear()
    cells[2].append(BeautifulSoup(related_html, "html.parser"))
    path.write_text(str(soup), encoding="utf-8")


def enrich():
    insert_section(
        ROOT / "index.html",
        "v64-accueil-fvg-imbalance",
        "Chapitre dédié : FVG, imbalance et CE",
        "Après les OB, on isole les FVG pour éviter de traiter chaque petit gap comme un signal. Le chapitre explique la zone, son origine et ses pièges.",
        "v63-accueil-order-blocks",
    )
    insert_section(
        ROOT / "04-setups-core.html",
        "v64-bridge-fvg-imbalance",
        "Avant les setups : comprendre FVG, imbalance et CE",
        "Les FVG sont utiles seulement s’ils viennent d’un déplacement réel. Cette leçon dédiée évite les entrées mécaniques sur des gaps trop fins ou déjà comblés.",
        "v63-bridge-order-blocks",
    )
    insert_section(
        ROOT / "15-index-concepts.html",
        "v64-index-fvg-imbalance",
        "FVG / Imbalance / CE",
        "Retrouve la leçon dédiée aux FVG, à l’imbalance, au CE et aux retours de prix dans la zone.",
        "v63-index-order-blocks",
    )
    update_concept_row(
        "FVG",
        "32-fvg-imbalance-ce.html",
        '<a class="glosslink" href="32-fvg-imbalance-ce.html#fvg-checklist">checklist</a>, '
        '<a class="glosslink" href="04-setups-core.html#fvg-bull">setup</a>, '
        '<a class="glosslink" href="05-variantes.html#fvg-hors-contexte">variante</a>',
    )
    update_concept_row(
        "CE",
        "32-fvg-imbalance-ce.html#fvg-anatomie",
        '<a class="glosslink" href="32-fvg-imbalance-ce.html#fvg-retour">retour</a>, '
        '<a class="glosslink" href="04-setups-core.html#fvg-bull">setup</a>, '
        '<a class="glosslink" href="05-variantes.html#ce-fail">échec</a>',
    )


def main():
    enrich()


if __name__ == "__main__":
    main()
