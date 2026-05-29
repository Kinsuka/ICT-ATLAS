from pathlib import Path

from bs4 import BeautifulSoup

from course_platform_layout import LESSONS


ROOT = Path(".")


def lesson_items():
    return [f"{index:02d}. {lesson['title']}" for index, lesson in enumerate(LESSONS, 1)]


def update_order_recommended(soup):
    for card in soup.find_all("div", class_="home-card"):
        title = card.find("h3")
        if not title or "Ordre recommandé" not in title.get_text(" ", strip=True):
            continue
        paragraph = card.find("p")
        if paragraph:
            paragraph.string = (
                "La progression suit exactement la table des matières : fondations, zones ICT, "
                "confluences, setups, passage au réel, puis validation par pratique et statistiques."
            )
        old_list = card.find("ul")
        if old_list:
            old_list.clear()
            for item in lesson_items():
                li = soup.new_tag("li")
                li.string = item
                old_list.append(li)
        note = card.find_all("p")[-1] if card.find_all("p") else None
        if note and "glossaire" in note.get_text(" ", strip=True).lower():
            note.string = "Le glossaire reste hors parcours : garde-le ouvert en panneau quand un sigle bloque la lecture."
        return


def replace_legacy_link_grid(soup):
    home_map = soup.find("div", class_="home-map")
    if not home_map:
        return
    legacy_grid = home_map.find_next_sibling("div", class_="section-links")
    if not legacy_grid:
        return
    legacy_grid.decompose()

    html = """
    <section class="card" id="commencer-parcours">
      <header><h2>Commencer le parcours</h2><span>Navigation</span></header>
      <p>La sidebar reste la table des matières de référence. Pour suivre le cours sans te disperser, avance simplement avec le bouton suivant en haut ou en bas de chaque leçon.</p>
      <div class="section-links">
        <a class="section-link" href="16-modele-mental.html"><h3>Commencer le cours</h3><p>Démarrer par le modèle mental, puis suivre la progression guidée.</p></a>
      </div>
    </section>
    """
    home_map.insert_after(BeautifulSoup(html, "html.parser"))


def main():
    path = ROOT / "index.html"
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    update_order_recommended(soup)
    replace_legacy_link_grid(soup)
    path.write_text(str(soup), encoding="utf-8")


if __name__ == "__main__":
    main()
