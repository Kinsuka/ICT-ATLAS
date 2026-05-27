from pathlib import Path

from bs4 import BeautifulSoup


REPLACEMENTS = {
    "Réponse : A valide": "Cas A : à classer",
    "Réponse : B refusé": "Cas B : à classer",
    "Réponse : A = MSS": "Cas A : à classer",
    "Réponse : B = faux MSS": "Cas B : à classer",
    "Réponse : A = fakeout": "Cas A : à classer",
    "Réponse : B = vraie cassure": "Cas B : à classer",
}


def add_aria_labels(path):
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    changed = False
    for section in soup.find_all("section"):
        heading = section.find(["h2", "h3"])
        heading_text = heading.get_text(" ", strip=True) if heading else ""
        for index, svg in enumerate(section.find_all("svg"), 1):
            label = svg.get("aria-label", "").strip()
            if not label and heading_text:
                svg["aria-label"] = f"{heading_text} - graphique {index}"
                svg["role"] = svg.get("role", "img")
                changed = True
    if changed:
        path.write_text(str(soup), encoding="utf-8")


def give_mini_svgs_more_bottom_room(path):
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    changed = False
    for svg in soup.find_all("svg"):
        raw_viewbox = svg.get("viewBox") or svg.get("viewbox")
        if raw_viewbox != "0 0 320 280":
            continue
        if svg.has_attr("viewBox"):
            svg["viewBox"] = "0 0 320 300"
        else:
            svg["viewbox"] = "0 0 320 300"
        first_rect = svg.find("rect")
        if first_rect and first_rect.get("width") == "320" and first_rect.get("height") == "280":
            first_rect["height"] = "300"
        changed = True
    if changed:
        path.write_text(str(soup), encoding="utf-8")


def fix_quiz_visible_answers():
    path = Path("08-quiz.html")
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    changed = False
    for text_node in soup.find_all("text"):
        text = text_node.get_text(" ", strip=True)
        if text in REPLACEMENTS:
            text_node.string = REPLACEMENTS[text]
            text_node["fill"] = "#f8c24e"
            changed = True
    if changed:
        path.write_text(str(soup), encoding="utf-8")


def main():
    fix_quiz_visible_answers()
    for path in sorted(Path(".").glob("*.html")):
        give_mini_svgs_more_bottom_room(path)
        add_aria_labels(path)


if __name__ == "__main__":
    main()
