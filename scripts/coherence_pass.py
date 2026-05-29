from pathlib import Path
from bs4 import BeautifulSoup


PAGES = [
    ("index.html", "Accueil"),
    ("16-modele-mental.html", "Modèle mental"),
    ("01-parcours.html", "Parcours"),
    ("11-mecanique-marches.html", "Mécanique"),
    ("glossaire.html", "Glossaire"),
    ("17-concept-setup-plan.html", "Concept/plan"),
    ("03-fondations.html", "Fondations"),
    ("04-setups-core.html", "Setups cœur"),
    ("18-transition-reel.html", "Graphique réel"),
    ("05-variantes.html", "Variantes"),
    ("07-failures-journees.html", "Failures"),
    ("06-contextes-avances.html", "Contextes"),
    ("12-gestion-risque.html", "Risque"),
    ("19-preuve-statistique.html", "Preuve statistique"),
    ("20-workflow-session.html", "Session live"),
    ("14-live-chart.html", "TradingView"),
    ("10-programme-avance.html", "Programme"),
    ("08-quiz.html", "Quiz"),
    ("13-prop-firm.html", "Prop Firm"),
    ("09-synthese.html", "Synthèse"),
    ("15-index-concepts.html", "Index"),
]

GENERIC_RULE = "Une fiche est acquise seulement si tu peux expliquer la zone, les conditions, la décision, l’invalidation et le risque sans relire le texte."

PAGE_RULES = {
    "01-parcours.html": "Ne passe à l’étape suivante que si tu as produit une preuve : captures, réponses de quiz, journal ou backtest.",
    "glossaire.html": "Un mot est acquis seulement si tu peux le reconnaître sur un graphique et expliquer l’erreur classique associée.",
    "03-fondations.html": "Une décision est valide seulement si elle relie contexte, liquidité, structure, risque et cible.",
    "04-setups-core.html": "Un setup cœur doit toujours être relu dans la séquence : liquidité prise, déplacement, zone, risque, cible.",
    "10-programme-avance.html": "Le programme avancé sert à répéter un processus, pas à ajouter des exceptions pendant la session.",
    "11-mecanique-marches.html": "Une explication mécanique doit rester observable : ordres, liquidité, déplacement, absorption ou invalidation.",
    "14-live-chart.html": "En live, le bon réflexe est d’observer d’abord la réaction après liquidité, puis seulement de chercher une zone.",
    "15-index-concepts.html": "L’index sert à retrouver la page source, pas à apprendre un concept isolé sans exemple.",
}

TEXT_REPLACEMENTS = {
    "Cours guide + atlas visuel": "Cours guidé + atlas visuel",
    "Chemin du cours": "Chemin du cours",
    "Lecture guidee": "Lecture guidée",
    "Comprendre le modele": "Comprendre le modèle",
    "Filtrer le setup": "Filtrer le setup",
    "Tester avant d'executer": "Tester avant d’exécuter",
    "Modele mental": "Modèle mental",
    "Mecanique": "Mécanique",
    "Setups coeur": "Setups cœur",
    "Graphique reel": "Graphique réel",
    "Preuve stats": "Preuve statistique",
    "Synthese": "Synthèse",
    "ICT Atlas - Modele mental": "ICT Atlas - Modèle mental",
    "ICT Atlas - Preuve statistique": "ICT Atlas - Preuve statistique",
    "ICT Atlas - Workflow de session": "ICT Atlas - Workflow de session",
    "Regle :": "Règle :",
    "Prerequis": "Prérequis",
    "A lire avec": "À lire avec",
    "definitions": "définitions",
    "precise": "précise",
    "eviter": "éviter",
    "revisable": "révisable",
    "hypothese": "hypothèse",
    "entree": "entrée",
    "executer": "exécuter",
    "deplacement": "déplacement",
    "liquidite": "liquidité",
    "liquidites": "liquidités",
    "strategie": "stratégie",
    "decision": "décision",
    "donnees": "données",
    "re-test": "re-test",
    "echantillon": "échantillon",
    "Echantillon": "Échantillon",
    "deja": "déjà",
    "reel": "réel",
    "bruitees": "bruitées",
    "pedagogiques": "pédagogiques",
    "Journee": "Journée",
    "journee": "journée",
    "proprete": "propreté",
    "marche": "marché",
    "cote": "côté",
    "idee": "idée",
    "incomplete": "incomplète",
    "reponse": "réponse",
    "Sequence": "Séquence",
    "sequence": "séquence",
    "Liquidite": "Liquidité",
    "Ou sommes-nous": "Où sommes-nous",
    "Qu'est-ce qui vient d'etre pris": "Qu’est-ce qui vient d’être pris",
    "Qu'est-ce qui confirme": "Qu’est-ce qui confirme",
    "le marche": "le marché",
    "Le marche": "Le marché",
    "premiere": "première",
    "reference": "référence",
    "première fois": "première fois",
    "refusér": "refuser",
}

HREF_FIXES = {
    "11-mecanique-marchés.html": "11-mecanique-marches.html",
    "18-transition-réel.html": "18-transition-reel.html",
    "07-failures-journées.html": "07-failures-journees.html",
}


def text_tag(soup, name, text, **attrs):
    tag = soup.new_tag(name, **attrs)
    tag.string = text
    return tag


def rebuild_nav(soup, active_file):
    aside = soup.find("aside", class_="site-nav")
    if not aside:
        return
    aside.clear()
    brand = soup.new_tag("div", **{"class": "nav-brand"})
    brand.append(text_tag(soup, "strong", "ICT Atlas"))
    brand.append(text_tag(soup, "span", "Cours guidé + atlas visuel"))
    aside.append(brand)

    pages_section = soup.new_tag("div", **{"class": "nav-section"})
    pages_section.append(text_tag(soup, "div", "Chemin du cours", **{"class": "nav-section-title"}))
    nav = soup.new_tag("div", **{"class": "nav-links"})
    for i, (href, label) in enumerate(PAGES, 1):
        a = soup.new_tag("a", href=href, **{"class": "active" if href == active_file else ""})
        a.append(text_tag(soup, "span", f"{i:02d}", **{"class": "nav-num"}))
        a.append(text_tag(soup, "span", label))
        nav.append(a)
    pages_section.append(nav)
    aside.append(pages_section)

    sections = []
    for h2 in soup.select("main.page h2"):
        section = h2.find_parent("section")
        if section and section.get("id"):
            title = h2.get_text(" ", strip=True)
            sections.append((section["id"], title if len(title) <= 58 else title[:55] + "..."))
    if sections:
        toc_section = soup.new_tag("div", **{"class": "nav-section"})
        toc_section.append(text_tag(soup, "div", "Dans cette page", **{"class": "nav-section-title"}))
        toc = soup.new_tag("div", **{"class": "nav-links toc-links"})
        for sid, title in sections:
            a = soup.new_tag("a", href=f"#{sid}")
            a.string = title
            toc.append(a)
        toc_section.append(toc)
        aside.append(toc_section)

    help_box = soup.new_tag("div", **{"class": "nav-help"})
    help_box.append(text_tag(soup, "strong", "Lecture guidée :"))
    help_box.append(soup.new_tag("br"))
    help_box.append("1. Comprendre le modèle.")
    help_box.append(soup.new_tag("br"))
    help_box.append("2. Filtrer le setup.")
    help_box.append(soup.new_tag("br"))
    help_box.append("3. Tester avant d’exécuter.")
    aside.append(help_box)


def make_card(soup, title, items):
    card = soup.new_tag("div", **{"class": "academy-card"})
    card.append(text_tag(soup, "h3", title))
    ul = soup.new_tag("ul")
    for item in items:
        li = soup.new_tag("li")
        li.string = item
        ul.append(li)
    card.append(ul)
    return card


def update_parcours(soup):
    section = soup.find(id="parcours-12-semaines")
    if section:
        grid = section.find("div", class_="academy-grid")
        if grid:
            grid.clear()
            weeks = [
                ("Semaine 1 — Modèle mental et carte du cours", ["Lire le fil rouge liquidité → déplacement → retour → cible.", "Comprendre la différence concept / setup / plan.", "Objectif : expliquer le cours en 5 phrases."]),
                ("Semaine 2 — Mécanique des marchés", ["Market orders, limit orders, stops, carnet.", "Pourquoi les highs/lows attirent le prix.", "Objectif : annoter 30 zones de liquidité."]),
                ("Semaine 3 — Vocabulaire et repères visuels", ["OHLC, BSL/SSL, PDH/PDL, DOL, CE.", "Sessions et kill zones.", "Objectif : définir 25 termes sans relire."]),
                ("Semaine 4 — Fondations de décision", ["Top-down, premium/discount, DOL, arbre de décision.", "BUY / SELL / NO TRADE.", "Objectif : refuser 10 signaux incomplets."]),
                ("Semaine 5 — FVG, CE et displacement", ["Tracer B1/B2/B3.", "Distinguer FVG réel, FVG utile et FVG hors contexte.", "Objectif : 50 FVG classés."]),
                ("Semaine 6 — MSS, OB, Breaker et OTE", ["Reconnaître la structure après liquidité.", "Valider OB/Breaker par le déplacement.", "Objectif : 40 cas expliqués."]),
                ("Semaine 7 — Setups de session", ["Asia fakeout, NY AM reversal, PM continuation.", "Relier session, liquidité et cible.", "Objectif : 30 setups simulés."]),
                ("Semaine 8 — Du propre au réel", ["Comparer idéal, exploitable, ambigu, refusé, valide perdant.", "Travailler Variantes et Failures.", "Objectif : 30 no trades justifiés."]),
                ("Semaine 9 — Contextes avancés", ["Daily Bias, Narrative, SMT, FOMC.", "Savoir quand un contexte filtre ou annule un setup.", "Objectif : 20 journées scorées."]),
                ("Semaine 10 — Risque et preuve statistique", ["Sizing, RR, breakeven, expectancy.", "Définir une hypothèse testable.", "Objectif : protocole de 50 occurrences."]),
                ("Semaine 11 — Live chart et workflow", ["Préparer TradingView et Bar Replay.", "Appliquer la routine avant / pendant / après.", "Objectif : 10 sessions replay journalisées."]),
                ("Semaine 12 — Validation finale", ["Quiz, examen, synthèse, erreurs récurrentes.", "Décider ce qui est gardé, réduit ou abandonné.", "Objectif : plan pour 100 trades documentés."]),
            ]
            for title, items in weeks:
                grid.append(make_card(soup, title, items))
        rule = section.find(class_="rule-block")
        if rule:
            rule.clear()
            rule.append(text_tag(soup, "strong", "Règle :"))
            rule.append(" Le planning suit le chemin du cours : comprendre, filtrer, tester, puis seulement exécuter.")

    site_map = soup.find(id="site-map")
    if site_map:
        first = site_map.find("div", class_="academy-card")
        if first:
            h3 = first.find("h3")
            p = first.find("p")
            if h3:
                h3.string = "1. Comprendre le modèle"
            if p:
                p.string = "Commencer par la logique liquidité → déplacement → retour → cible, puis lire la mécanique avant le vocabulaire."

    chemin = soup.find(id="chemin-principal-v43")
    if chemin:
        replacements = {
            "1. Modele mental": "1. Modèle mental",
            "2. Langage": "2. Langage",
            "4. Realite": "4. Réalité",
            "5. Preuve": "5. Preuve",
            "6. Execution": "6. Exécution",
        }
        for h3 in chemin.find_all("h3"):
            h3.string = replacements.get(h3.get_text(strip=True), h3.get_text(strip=True))
        texts = {
            "Comprendre la sequence liquidite -> displacement -> zone de retour -> DOL.": "Comprendre la séquence liquidité → displacement → zone de retour → DOL.",
            "Lire la mecanique puis le vocabulaire, pour eviter les mots appris sans causalite.": "Lire la mécanique puis le vocabulaire, pour éviter les mots appris sans causalité.",
            "Comparer exemple propre, variante, faux ami, failure et journee complete.": "Comparer exemple propre, variante, faux ami, failure et journée complète.",
            "Tester sur un echantillon, mesurer l'expectancy et garder seulement ce qui resiste aux donnees.": "Tester sur un échantillon, mesurer l’expectancy et garder seulement ce qui résiste aux données.",
            "Utiliser le workflow de session avant de passer au live ou a la prop firm.": "Utiliser le workflow de session avant de passer au live ou à la prop firm.",
        }
        for p in chemin.find_all("p"):
            p.string = texts.get(p.get_text(strip=True), p.get_text(strip=True))


def update_variantes(soup):
    section = soup.find(id="ob-fvg-confluence-bull")
    if section:
        rows = section.select(".tc-row")
        for row in rows:
            label = row.find(class_="tc-label")
            content = row.find(class_="tc-content")
            if not label or not content:
                continue
            if label.get_text(strip=True) == "Pourquoi refusé":
                label.string = "Pourquoi valide"
            if label.get_text(strip=True) == "Erreur fréquente":
                label["class"] = ["tc-label"]
                label.string = "Objectifs"

    for row in soup.select(".tc-row"):
        label = row.find(class_="tc-label")
        content = row.find(class_="tc-content")
        if not label or not content:
            continue
        text = content.get_text(" ", strip=True)
        if label.get_text(strip=True) == "Erreur fréquente" and text.startswith("TP1 vise"):
            label["class"] = ["tc-label"]
            label.string = "Objectifs"

    for section in soup.select("section.card"):
        title = section.find("h2")
        rule = section.find(class_="rule-band")
        if not title or not rule:
            continue
        title_text = title.get_text(" ", strip=True)
        rule_text = rule.get_text(" ", strip=True).replace("Règle :", "").strip()
        new_rule = None
        if "trop tardif" in title_text.lower() or "DOL est déjà atteint" in title_text:
            new_rule = "Un setup propre devient secondaire si la cible principale est déjà consommée."
        elif "troisième mitigation" in title_text.lower():
            new_rule = "Plus une zone est revisitée, moins elle représente une inefficience fraîche."
        elif "Confluence OB + FVG" in title_text:
            new_rule = "Une confluence renforce une zone seulement si les outils racontent la même séquence, pas s’ils sont empilés au hasard."
        elif rule_text == GENERIC_RULE:
            new_rule = "Classe le cas par sa condition manquante : contexte, liquidité, déplacement, timing, risque ou cible."
        if new_rule:
            rule.clear()
            rule.append(text_tag(soup, "strong", "Règle :"))
            rule.append(" " + new_rule)


def update_synthese(soup):
    main = soup.find("main", class_="page")
    if not main:
        return
    hero = main.find("div", class_="hero")
    if hero:
        p = hero.find("p")
        if p:
            p.string = "Clôture du cours : checklist finale, critères de passage, erreurs éliminatoires et plan 30 jours."
    meta_goal = main.select_one(".meta-goal")
    if meta_goal:
        meta_goal.clear()
        meta_goal.append(text_tag(soup, "strong", "Objectif"))
        meta_goal.append("Transformer tout le cours en protocole vérifiable avant backtest, replay ou session live.")
    meta_prereq = main.select_one(".meta-prereq")
    if meta_prereq:
        meta_prereq.clear()
        meta_prereq.append(text_tag(soup, "strong", "Prérequis"))
        meta_prereq.append("Avoir parcouru le chemin principal : modèle mental, mécanique, vocabulaire, setups, variantes, risque, preuve statistique et workflow.")

    existing = {section.get("id") for section in main.select("section.card")}
    additions = [
        ("synthese-decision-flow", "82 — Ordre de décision final", "Décision", [
            ("1. Contexte", "Session, news, higher timeframe, premium/discount et DOL sont définis avant toute recherche d’entrée."),
            ("2. Liquidité", "Le trade doit répondre à une liquidité prise ou visée : SSL, BSL, PDH, PDL, Asia High/Low ou niveau interne."),
            ("3. Confirmation", "Displacement, MSS et zone exploitable doivent apparaître dans le bon ordre. Une zone seule ne suffit pas."),
            ("4. Plan", "Entrée, stop, TP1, TP2, invalidation, taille et règle de gestion sont écrits avant l’ordre."),
        ], "Si l’ordre de décision est inversé, le trade devient une justification après coup."),
        ("synthese-criteres-passage", "83 — Critères de passage avant live", "Validation", [
            ("Reconnaissance", "Identifier correctement FVG, MSS, OB, Breaker, OTE, sweep et DOL sur des captures non annotées."),
            ("Filtrage", "Refuser au moins 30 cas séduisants mais incomplets : hors contexte, tardifs, trop mitigés ou sans cible."),
            ("Backtesting", "Avoir 50 occurrences minimum sur un setup précis, avec résultats en R et erreurs séparées."),
            ("Journal", "Produire une capture et une raison écrite pour chaque trade pris ou refusé."),
        ], "Le passage au live ne dépend pas de la confiance ressentie, mais d’un échantillon documenté."),
        ("synthese-erreurs-eliminatoires", "84 — Erreurs éliminatoires", "Discipline", [
            ("Entrer sans DOL", "Le trade n’a pas de destination logique claire."),
            ("Confondre sweep et entrée", "La prise de liquidité est une information, pas une permission automatique."),
            ("Déplacer le stop", "La perte prévue devient une perte négociée émotionnellement."),
            ("Changer de règle après perte", "Le backtest devient illisible et l’edge ne peut plus être mesuré."),
            ("Trader après limite", "Deux pertes imposent réduction ou observation ; trois pertes imposent stop journée."),
        ], "Une erreur éliminatoire annule la qualité du setup, même si le trade finit gagnant."),
        ("synthese-plan-30-jours", "85 — Plan 30 jours après le cours", "Suite logique", [
            ("Jours 1-7", "Relecture active : modèle mental, mécanique, vocabulaire et fondations. Objectif : 50 captures annotées."),
            ("Jours 8-15", "Un seul setup en Bar Replay. Objectif : 50 occurrences sans regarder le futur."),
            ("Jours 16-23", "Ajout du risque, du journal et du classement : valide gagnant, valide perdant, hors plan, no trade."),
            ("Jours 24-30", "Synthèse des stats, trois erreurs récurrentes, décision garder/réduire/abandonner le setup."),
        ], "Après le cours, la priorité n’est pas de trader plus ; c’est de réduire la subjectivité."),
    ]
    for sid, title, tag, cards, rule_text in additions:
        if sid in existing:
            continue
        sec = soup.new_tag("section", **{"class": "card", "id": sid})
        header = soup.new_tag("header")
        header.append(text_tag(soup, "h2", title))
        header.append(text_tag(soup, "span", tag))
        sec.append(header)
        grid = soup.new_tag("div", **{"class": "academy-grid"})
        for card_title, body in cards:
            card = soup.new_tag("div", **{"class": "academy-card"})
            card.append(text_tag(soup, "h3", card_title))
            card.append(text_tag(soup, "p", body))
            grid.append(card)
        sec.append(grid)
        rule = soup.new_tag("div", **{"class": "rule-block"})
        rule.append(text_tag(soup, "strong", "Règle :"))
        rule.append(" " + rule_text)
        sec.append(rule)
        main.append(sec)


def update_rules(soup, filename):
    replacement = PAGE_RULES.get(filename)
    if not replacement:
        return
    for rule in soup.select(".rule-block,.rule-band"):
        text = rule.get_text(" ", strip=True)
        if GENERIC_RULE in text:
            rule.clear()
            rule.append(text_tag(soup, "strong", "Règle :"))
            rule.append(" " + replacement)


def apply_text_replacements(path):
    text = path.read_text(encoding="utf-8")
    for old, new in TEXT_REPLACEMENTS.items():
        text = text.replace(old, new)
    for old, new in HREF_FIXES.items():
        text = text.replace(old, new)
    path.write_text(text, encoding="utf-8")


def main():
    for path in sorted(Path(".").glob("*.html")):
        soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
        if path.name == "01-parcours.html":
            update_parcours(soup)
        if path.name == "05-variantes.html":
            update_variantes(soup)
        if path.name == "09-synthese.html":
            update_synthese(soup)
        update_rules(soup, path.name)
        rebuild_nav(soup, path.name)
        path.write_text(str(soup), encoding="utf-8")
        apply_text_replacements(path)

    readme = Path("README_V43.txt")
    readme.write_text(
        "ICT Atlas V43 - Cours guidé\n\n"
        "Passe de cohérence éditoriale appliquée : parcours 12 semaines aligné avec le chemin du cours, "
        "navigation accentuée, corrections de libellés dans Variantes, règles moins génériques, "
        "et Synthèse renforcée en page de clôture.\n\n"
        "Point d’entrée : index.html\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
