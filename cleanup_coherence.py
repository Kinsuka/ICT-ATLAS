from pathlib import Path
from bs4 import BeautifulSoup, NavigableString


def replace_text_nodes(soup, replacements):
    for node in soup.find_all(string=True):
        if not isinstance(node, NavigableString):
            continue
        text = str(node)
        new = text
        for old, repl in replacements.items():
            new = new.replace(old, repl)
        if new != text:
            node.replace_with(new)


def rebuild_toc(soup):
    aside = soup.find("aside", class_="site-nav")
    if not aside:
        return
    old_toc = None
    for section in aside.find_all("div", class_="nav-section"):
        title = section.find("div", class_="nav-section-title")
        if title and title.get_text(strip=True) == "Dans cette page":
            old_toc = section
            break
    if old_toc:
        old_toc.decompose()

    links = []
    for h2 in soup.select("main.page h2"):
        section = h2.find_parent("section")
        if section and section.get("id"):
            title = h2.get_text(" ", strip=True)
            links.append((section["id"], title if len(title) <= 58 else title[:55] + "..."))
    if not links:
        return

    toc_section = soup.new_tag("div", **{"class": "nav-section"})
    title = soup.new_tag("div", **{"class": "nav-section-title"})
    title.string = "Dans cette page"
    toc_section.append(title)
    toc = soup.new_tag("div", **{"class": "nav-links toc-links"})
    for sid, text in links:
        a = soup.new_tag("a", href=f"#{sid}")
        a.string = text
        toc.append(a)
    toc_section.append(toc)

    help_box = aside.find("div", class_="nav-help")
    if help_box:
        help_box.insert_before(toc_section)
    else:
        aside.append(toc_section)


def cleanup_synthese():
    path = Path("09-synthese.html")
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")

    canonical = {
        "82 — Ordre de décision final": "synthese-decision-flow",
        "83 — Critères de passage avant live": "synthese-criteres-passage",
        "84 — Erreurs éliminatoires": "synthese-erreurs-eliminatoires",
        "85 — Plan 30 jours après le cours": "synthese-plan-30-jours",
    }
    seen = set()
    for section in list(soup.select("main.page section.card")):
        h2 = section.find("h2")
        if not h2:
            continue
        title = h2.get_text(" ", strip=True)
        if title in canonical:
            if title in seen:
                section.decompose()
            else:
                section["id"] = canonical[title]
                seen.add(title)

    rebuild_toc(soup)
    path.write_text(str(soup), encoding="utf-8")


def cleanup_all_text():
    replacements = {
        "00X - Chemin principal : du modele a l'execution": "00X — Chemin principal : du modèle à l’exécution",
        "Passer de concept a setup puis a plan complet": "Passer de concept à setup puis à plan complet",
        "premiere fois": "première fois",
        "reference": "référence",
        "refusér": "refuser",
        "Refusér": "Refuser",
        "Cycle minimal : liquidité -> delivery -> mitigation": "Cycle minimal : liquidité → delivery → mitigation",
    }
    for path in Path(".").glob("*.html"):
        soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
        replace_text_nodes(soup, replacements)
        path.write_text(str(soup), encoding="utf-8")


if __name__ == "__main__":
    cleanup_synthese()
    cleanup_all_text()
