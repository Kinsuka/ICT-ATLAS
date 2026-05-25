from pathlib import Path
from bs4 import BeautifulSoup


ROOT = Path(".")
SOURCE = ROOT / "02-vocabulaire.html"
TARGET = ROOT / "glossaire.html"


def tag(soup, name, text=None, **attrs):
    item = soup.new_tag(name, **attrs)
    if text is not None:
        item.string = text
    return item


def build_reference_nav(soup):
    aside = soup.find("aside", class_="site-nav")
    if not aside:
        aside = soup.new_tag("aside", **{"class": "site-nav", "aria-label": "Navigation du glossaire"})
    aside.clear()

    brand = tag(soup, "div", **{"class": "nav-brand"})
    brand.append(tag(soup, "strong", "ICT Atlas"))
    brand.append(tag(soup, "span", "Glossaire permanent"))
    aside.append(brand)

    title = tag(soup, "div", **{"class": "course-nav-title"})
    title.append(tag(soup, "span", "Référence"))
    title.append(tag(soup, "small", "toujours accessible"))
    aside.append(title)

    back = soup.new_tag("a", href="index.html", **{"class": "glossary-nav-link"})
    back.append(tag(soup, "strong", "Retour au cours"))
    back.append(tag(soup, "span", "Reprendre la progression guidée"))
    aside.append(back)

    part = tag(soup, "div", **{"class": "course-part"})
    head = tag(soup, "div", **{"class": "course-part-head"})
    head.append(tag(soup, "span", "Glossaire"))
    head.append(tag(soup, "strong", "Repères rapides"))
    part.append(head)
    links = [
        ("#glossaire-detaille", "Dictionnaire pédagogique"),
        ("#guide-glossaire-visuel", "Glossaire visuel"),
        ("#ohlc", "Bougie OHLC"),
        ("#order-types", "Types d'ordres"),
        ("#sessions-timeline", "Sessions et kill zones"),
    ]
    ol = tag(soup, "ol", **{"class": "course-lessons"})
    for index, (href, label) in enumerate(links, 1):
        li = tag(soup, "li", **{"class": "course-lesson"})
        a = soup.new_tag("a", href=href)
        a.append(tag(soup, "span", str(index), **{"class": "lesson-bullet"}))
        body = tag(soup, "span", **{"class": "lesson-link-text"})
        body.append(tag(soup, "strong", label))
        body.append(tag(soup, "small", "référence"))
        a.append(body)
        li.append(a)
        ol.append(li)
    part.append(ol)
    aside.append(part)

    help_box = tag(soup, "div", **{"class": "nav-help"})
    help_box.append(tag(soup, "strong", "Méthode"))
    help_box.append(soup.new_tag("br"))
    help_box.append("Ouvre cette page dès qu'un sigle ou une zone te bloque, puis reviens à la leçon.")
    aside.append(help_box)
    return aside


def make_glossary_page():
    soup = BeautifulSoup(SOURCE.read_text(encoding="utf-8"), "html.parser")
    if soup.title:
        soup.title.string = "ICT Atlas - Glossaire permanent"

    shell = soup.find("div", class_="app-shell")
    if shell:
        shell["class"] = "app-shell glossary-shell"

    build_reference_nav(soup)

    main = soup.find("main", class_="page")
    if main:
        for selector in [
            ("div", "lesson-header"),
            ("section", "lesson-objectives"),
            ("nav", "lesson-bottom-nav"),
        ]:
            for item in main.find_all(selector[0], class_=selector[1]):
                item.decompose()
        hero = main.find("div", class_="hero")
        if hero:
            h1 = hero.find("h1")
            p = hero.find("p")
            if h1:
                h1.string = "ICT Atlas — Glossaire permanent"
            if p:
                p.string = "La référence rapide pour comprendre les acronymes, zones, ordres et repères ICT sans quitter ton fil d'apprentissage."
            tagline = hero.find("div", class_="tagline")
            if tagline:
                tagline.clear()
                for label in ["référence", "hors progression", "accessible partout"]:
                    tagline.append(tag(soup, "span", label))

        note = tag(soup, "section", **{"class": "page-note"})
        note.append(tag(soup, "strong", "Usage"))
        note.append(
            " Cette page n'est plus une leçon du parcours. Elle sert de dictionnaire permanent : consulte-la quand un terme apparaît, puis reprends la leçon en cours."
        )
        first_section = main.find("section")
        if first_section:
            first_section.insert_before(note)

    old_fab = soup.find("a", class_="glossary-fab")
    if old_fab:
        old_fab.decompose()

    TARGET.write_text(str(soup), encoding="utf-8")


def replace_old_links():
    for path in ROOT.glob("*.html"):
        if path.name in {"02-vocabulaire.html", "glossaire.html"}:
            continue
        text = path.read_text(encoding="utf-8")
        text = text.replace("02-vocabulaire.html", "glossaire.html")
        path.write_text(text, encoding="utf-8")


def make_legacy_redirect():
    html = """<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1" name="viewport"/>
<meta http-equiv="refresh" content="0; url=glossaire.html"/>
<title>ICT Atlas - Redirection glossaire</title>
<link href="style.css" rel="stylesheet"/>
</head>
<body>
<main class="page" style="max-width:42rem;margin:10vh auto;padding:2rem">
<section class="card">
<header><h1>Glossaire déplacé</h1><span>Référence permanente</span></header>
<p>Le vocabulaire ICT est maintenant sorti du parcours de leçons pour rester accessible à tout moment.</p>
<p><a class="pill" href="glossaire.html">Ouvrir le glossaire permanent</a></p>
</section>
</main>
</body>
</html>
"""
    SOURCE.write_text(html, encoding="utf-8")


if __name__ == "__main__":
    make_glossary_page()
    replace_old_links()
    make_legacy_redirect()
