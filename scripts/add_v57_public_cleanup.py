from pathlib import Path
import re

from bs4 import BeautifulSoup


ROOT = Path(".")


def set_text_preserve_children(tag, text):
    tag.clear()
    tag.string = text


def replace_or_insert_after(anchor, fragment, soup):
    anchor.insert_after(BeautifulSoup(fragment, "html.parser"))


def normalize_version_label(text):
    raw = text.strip()
    lowered = raw.lower()
    if re.fullmatch(r"v\d+", raw, re.I):
        return "Fondation"
    if re.match(r"v\d+\s*[-–—·]\s*", raw, re.I):
        cleaned = re.sub(r"^v\d+\s*[-–—·]\s*", "", raw, flags=re.I).strip()
        return cleaned[:1].upper() + cleaned[1:] if cleaned else "Fondation"
    if "mini-site" in lowered:
        return "Cours structuré"
    if re.fullmatch(r"accueil\s+v\d+", raw, re.I):
        return "Accueil"
    if re.search(r"\bv\d+\b", raw, re.I):
        raw = re.sub(r"\s*[·|,-–—]?\s*\bv\d+\b", "", raw, flags=re.I).strip()
        return raw if raw else "Fondation"
    return raw


def cleanup_visible_versions(soup):
    for node in soup.find_all(string=True):
        if not isinstance(node, str):
            continue
        text = str(node)
        replacements = {
            "Mini-site V38": "Cours structuré",
            "Mini-site V34": "Cours structuré",
            "Mini-site V42": "Cours structuré",
            "Navigation par pages": "Navigation guidée",
            "Sidebar + liens croisés": "Glossaire intégré",
            "V43 - transformation en vrai cours": "Parcours guidé du cours",
            "V54 — Nouveau module fondation : Liquidite - Entree - Stop - TP": "Module fondation : Liquidité - Entrée - Stop - TP",
            "Index V54 — Fondations Liquidite - Entree - Stop - TP": "Index — Fondations Liquidité - Entrée - Stop - TP",
            "Index V36 — nouveaux modules consolidés": "Index — modules consolidés",
            "Index V48 — leçons zero-to-hero": "Index — leçons de consolidation",
            "V43 - transformation en vrai cours": "Parcours guidé du cours",
        }
        new_text = text
        for old, new in replacements.items():
            new_text = new_text.replace(old, new)
        new_text = re.sub(r"\b[Dd]e Z[eé]ro à Pro\b", "ICT Atlas", new_text)
        new_text = re.sub(r"\bzero-to-hero\b", "consolidation", new_text, flags=re.I)
        new_text = re.sub(r"\s+[Vv]\d+\b", "", new_text)
        new_text = new_text.replace("Plan du mini-site", "Plan du cours")
        new_text = new_text.replace("tout le mini-site", "tout le cours")
        new_text = new_text.replace("Index — Ajouts critiques", "Index — repères critiques")
        new_text = new_text.replace("Index - Market structure et transitions", "Index - market structure et transitions")
        if new_text != text:
            node.replace_with(new_text)

    for span in soup.find_all("span"):
        if not span.string:
            continue
        span.string = normalize_version_label(span.get_text(" ", strip=True))


def update_homepage():
    path = ROOT / "index.html"
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    title = soup.find("title")
    if title:
        title.string = "ICT Atlas - Comprendre ICT une bonne fois pour toutes"

    hero = soup.find("div", class_="hero")
    if hero:
        h1 = hero.find("h1")
        p = hero.find("p")
        tagline = hero.find("div", class_="tagline")
        if h1:
            h1.string = "ICT Atlas"
        if p:
            p.clear()
            p.append("Comprendre ICT une bonne fois pour toutes : ancrer les fondations, filtrer le bruit, passer du setup au graphique réel.")
        if tagline:
            tagline.clear()
            for item in ["Fondations ICT", "Clarté contre le bruit", "Du concept au live"]:
                span = soup.new_tag("span")
                span.string = item
                tagline.append(span)

    for old_id in ["v54-home-fondations", "v36-changelog"]:
        old = soup.find(id=old_id)
        if old:
            old.decompose()

    meta = soup.find("div", class_="page-meta-dashboard")
    positioning = """<section class="card" id="positionnement-public"><header><h2>Comprendre ICT une bonne fois pour toutes</h2><span>Positionnement</span></header><div class="academy-grid"><div class="academy-card"><h3>Pour qui ?</h3><p>Pour le trader qui a deja croise ICT/SMC, reconnait certains patterns, mais veut ancrer la logique pour ne plus etre ballotte par chaque video contradictoire.</p></div><div class="academy-card"><h3>Ce que le cours fait</h3><p>Il relie liquidite, deplacement, environnement, entree, invalidation, TP, risque et preuve statistique dans une progression lisible.</p></div><div class="academy-card"><h3>Ce que ce n'est pas</h3><p>Ce n'est pas un module debutant absolu sur brokers, plateformes, pips, spread ou levier. Le glossaire aide, mais le cours vise surtout la clarification ICT.</p></div></div><div class="rule-block"><strong>Promesse :</strong> moins de bruit, plus de structure. L'objectif n'est pas de multiplier les setups, mais de savoir lesquels meritent ton attention.</div></section>"""
    if not soup.find(id="positionnement-public"):
        if meta:
            replace_or_insert_after(meta, positioning, soup)
        else:
            main = soup.find("main", class_="page")
            if main:
                main.insert(2, BeautifulSoup(positioning, "html.parser"))

    path.write_text(str(soup), encoding="utf-8")


def cleanup_setup_logic():
    path = ROOT / "04-setups-core.html"
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    specific = {
        "power3-bull": "Power Three bullish decrit une journee ou l'accumulation prepare la manipulation sous la liquidite, puis la distribution dans le sens haussier. La valeur vient de la sequence complete, pas du nom du modele.",
        "power3-bear": "Power Three bearish decrit une manipulation au-dessus de la liquidite avant distribution baissiere. Le modele devient defendable seulement si le retour confirme le rejet et la cible reste disponible.",
    }
    for section_id, text in specific.items():
        section = soup.find(id=section_id)
        if not section:
            continue
        block = section.select_one(".inst-block p")
        if block:
            block.string = text

    for section in soup.select("section.card"):
        seen = set()
        for block in list(section.select(".inst-block")):
            content = block.get_text(" ", strip=True)
            if content in seen:
                block.decompose()
            else:
                seen.add(content)
    path.write_text(str(soup), encoding="utf-8")


def cleanup_all_html():
    for path in ROOT.glob("*.html"):
        soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
        cleanup_visible_versions(soup)
        old_zero_to_hero = soup.find(id="index-v48-zero-to-hero")
        if old_zero_to_hero:
            old_zero_to_hero["id"] = "index-v48-consolidation"
        path.write_text(str(soup), encoding="utf-8")


def main():
    cleanup_all_html()
    update_homepage()
    cleanup_setup_logic()


if __name__ == "__main__":
    main()
