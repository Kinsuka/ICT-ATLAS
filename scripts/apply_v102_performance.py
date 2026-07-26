from pathlib import Path
import re

from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parents[1]
GENERIC_SIGNATURE = "120,270 190,210 260,232 330,150 405,182 480,108 560,132 640,82 760,104"


def make_tag(soup, name, text=None, **attrs):
    node = soup.new_tag(name, **attrs)
    if text is not None:
        node.string = text
    return node


def convert_file(file_path):
    source = file_path.read_text(encoding="utf-8")
    if GENERIC_SIGNATURE not in source:
        return 0

    soup = BeautifulSoup(source, "html.parser")
    converted = 0
    for svg in list(soup.find_all("svg")):
        first_line = svg.find("polyline")
        if not first_line or first_line.get("points") != GENERIC_SIGNATURE:
            continue
        chart = svg.find_parent(class_="chart")
        card = chart.find_parent(class_="card") if chart else None
        title_node = card.select_one("header h2") if card else None
        title = title_node.get_text(" ", strip=True) if title_node else svg.get("aria-label", "Lecture visuelle")
        title = re.sub(r"^Cas Atlas\s+\d+\s*", "", title).strip()
        steps = [step.strip() for step in re.split(r"\s*(?:->|→)\s*", title) if step.strip()]

        visual = make_tag(
            soup,
            "div",
            **{
                "class": "concept-visual",
                "role": "img",
                "aria-label": svg.get("aria-label", title),
            },
        )
        visual.append(make_tag(soup, "strong", title.replace("->", "→"), **{"class": "concept-visual-title"}))

        if len(steps) > 1:
            sequence = make_tag(soup, "ol", **{"class": "concept-sequence"})
            for index, step in enumerate(steps, 1):
                item = make_tag(soup, "li")
                item.append(make_tag(soup, "span", f"{index:02d}"))
                item.append(make_tag(soup, "b", step))
                sequence.append(item)
            visual.append(sequence)
        else:
            labels = svg.select('text[x="102"]')[:3]
            dots = svg.select('circle[cx="86"]')[:3]
            if labels:
                comparison = make_tag(soup, "div", **{"class": "concept-comparison"})
                fallback_colors = ["#26a69a", "#4fc3f7", "#ef5350"]
                for index, label in enumerate(labels, 1):
                    color = dots[index - 1].get("fill") if len(dots) >= index else fallback_colors[index - 1]
                    item = make_tag(soup, "article", style=f"--concept-accent:{color}")
                    item.append(make_tag(soup, "small", f"ISSUE {index:02d}"))
                    item.append(make_tag(soup, "b", label.get_text(strip=True)))
                    comparison.append(item)
                visual.append(comparison)

        chart_classes = list(chart.get("class", []))
        if "chart--concept" not in chart_classes:
            chart_classes.append("chart--concept")
        chart["class"] = chart_classes
        chart["data-visual-version"] = "v102"
        svg.replace_with(visual)
        converted += 1

    file_path.write_text(str(soup), encoding="utf-8")
    return converted


def main():
    files = [ROOT / "index.html", *(ROOT / "pages").glob("*.html")]
    converted = sum(convert_file(file_path) for file_path in files)
    print(f"V102 : {converted} graphiques génériques convertis en HTML sémantique.")


if __name__ == "__main__":
    main()
