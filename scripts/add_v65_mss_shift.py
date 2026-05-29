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
      <header><h2>{title}</h2><span>Structure</span></header>
      <p>{intro}</p>
      <div class="section-links">
        <a class="section-link" href="33-mss-changement-controle.html"><h3>Chapitre MSS</h3><p>Comprendre sweep, rejet, displacement, cassure utile et changement de contrôle.</p></a>
        <a class="section-link" href="33-mss-changement-controle.html#mss-checklist"><h3>Checklist MSS</h3><p>Origine, niveau cassé, displacement, retour, plan et invalidation.</p></a>
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
    button = soup.find("button", attrs={"data-glossary-term": "MSS"})
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
            '<a class="glosslink" href="33-mss-changement-controle.html">Référence principale</a>',
            "html.parser",
        )
    )
    cells[2].clear()
    cells[2].append(
        BeautifulSoup(
            '<a class="glosslink" href="33-mss-changement-controle.html#mss-checklist">checklist</a>, '
            '<a class="glosslink" href="04-setups-core.html#mss-bull">setup</a>, '
            '<a class="glosslink" href="05-variantes.html#mss-bear">variante</a>',
            "html.parser",
        )
    )
    path.write_text(str(soup), encoding="utf-8")


def enrich():
    insert_section(
        ROOT / "index.html",
        "v65-accueil-mss-shift",
        "Chapitre dédié : MSS et changement de contrôle",
        "Après les zones OB/FVG, on ajoute le filtre qui confirme qu’un marché change réellement de contrôle avant de chercher une entrée.",
        "v64-accueil-fvg-imbalance",
    )
    insert_section(
        ROOT / "04-setups-core.html",
        "v65-bridge-mss-shift",
        "Avant les setups : valider le changement de contrôle",
        "Le MSS empêche de confondre une simple mèche ou une micro-cassure avec une vraie confirmation. Cette leçon dédiée clarifie le niveau qui doit céder.",
        "v64-bridge-fvg-imbalance",
    )
    insert_section(
        ROOT / "15-index-concepts.html",
        "v65-index-mss-shift",
        "MSS / changement de contrôle",
        "Retrouve la leçon dédiée au MSS, aux cassures utiles, aux micro-cassures faibles et aux faux shifts.",
        "v64-index-fvg-imbalance",
    )
    update_concept_row()


def main():
    enrich()


if __name__ == "__main__":
    main()
