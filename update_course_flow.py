from pathlib import Path
from bs4 import BeautifulSoup


PAGES = [
    ("index.html", "Accueil"),
    ("16-modele-mental.html", "Modele mental"),
    ("01-parcours.html", "Parcours"),
    ("11-mecanique-marches.html", "Mecanique"),
    ("glossaire.html", "Glossaire"),
    ("17-concept-setup-plan.html", "Concept/plan"),
    ("03-fondations.html", "Fondations"),
    ("04-setups-core.html", "Setups coeur"),
    ("18-transition-reel.html", "Graphique reel"),
    ("05-variantes.html", "Variantes"),
    ("07-failures-journees.html", "Failures"),
    ("06-contextes-avances.html", "Contextes"),
    ("12-gestion-risque.html", "Risque"),
    ("19-preuve-statistique.html", "Preuve stats"),
    ("20-workflow-session.html", "Session live"),
    ("14-live-chart.html", "TradingView"),
    ("10-programme-avance.html", "Programme"),
    ("08-quiz.html", "Quiz"),
    ("13-prop-firm.html", "Prop Firm"),
    ("09-synthese.html", "Synthese"),
    ("15-index-concepts.html", "Index"),
]


NEW_PAGES = {
    "16-modele-mental.html": {
        "title": "ICT Atlas - Modele mental",
        "h1": "ICT Atlas - Modele mental",
        "subtitle": "Le fil rouge du cours : liquidite, deplacement, retour et cible.",
        "goal": "donner une lecture simple avant les definitions techniques. Cette page sert de boussole : tout le reste precise, filtre ou teste ce modele.",
        "prereq": "Aucun. Lis cette page avant le parcours si tu decouvres ICT.",
        "sections": [
            {
                "id": "phrase-fil-rouge",
                "title": "La phrase qui organise tout le cours",
                "tag": "fil rouge",
                "cards": [
                    ("Version simple", "Le prix cherche souvent une liquidite visible, provoque un deplacement, laisse parfois une zone de retour, puis vise une autre liquidite."),
                    ("Ce que cela change", "Un FVG, un OB ou un MSS ne sont pas des signaux isoles. Ils doivent etre relus dans cette sequence : pourquoi ici, pourquoi maintenant, vers quelle cible ?"),
                    ("Question centrale", "Le marche vient-il de prendre une liquidite utile, et la reaction qui suit confirme-t-elle un vrai changement de flux ?"),
                ],
                "rule": "Le setup arrive a la fin de la lecture, jamais au debut.",
            },
            {
                "id": "cycle-liquidity-delivery",
                "title": "Cycle minimal : liquidite -> delivery -> mitigation",
                "tag": "sequence",
                "cards": [
                    ("1. Liquidite", "Highs, lows, PDH, PDL, Asia High/Low ou zones evidentes concentrent souvent stops, prises de profit et ordres breakout."),
                    ("2. Sweep ou cassure", "Le prix traverse la zone. Ce passage ne suffit pas : il peut annoncer une absorption, mais aussi une vraie continuation."),
                    ("3. Displacement", "Une bougie impulsive ou une sequence nette montre que les ordres agressifs dominent temporairement un cote du carnet."),
                    ("4. Zone de retour", "FVG, OB, breaker ou OTE deviennent des zones candidates seulement si elles viennent du deplacement pertinent."),
                    ("5. Cible", "La destination logique reste une autre liquidite. Sans cible, le trade manque de narrative."),
                ],
                "rule": "Si tu ne peux pas nommer la liquidite prise et la liquidite visee, ton idee est incomplete.",
            },
            {
                "id": "trois-questions",
                "title": "Les trois questions avant tout apprentissage technique",
                "tag": "decision",
                "cards": [
                    ("Ou sommes-nous ?", "Range, premium/discount, kill zone, proximite du DOL et contexte higher timeframe."),
                    ("Qu'est-ce qui vient d'etre pris ?", "SSL, BSL, high/low de session, ancien niveau journalier ou zone interne."),
                    ("Qu'est-ce qui confirme ?", "Displacement, MSS, FVG/OB exploitable, invalidation claire et risque acceptable."),
                ],
                "rule": "Une forme propre sans reponse a ces trois questions reste un dessin, pas un plan.",
            },
        ],
    },
    "17-concept-setup-plan.html": {
        "title": "ICT Atlas - Concept, setup, plan",
        "h1": "ICT Atlas - Concept, setup, plan",
        "subtitle": "La distinction qui evite de confondre reconnaissance et execution.",
        "goal": "separer clairement ce qui decrit le marche, ce qui cree une opportunite, et ce qui autorise une entree risquee.",
        "prereq": "Lis le modele mental puis garde cette page ouverte pendant les premiers setups.",
        "sections": [
            {
                "id": "trois-niveaux",
                "title": "Trois niveaux a ne jamais melanger",
                "tag": "clarte",
                "cards": [
                    ("Concept", "Un concept nomme un phenomene : FVG, sweep, MSS, OB, OTE, premium, discount, DOL. Il aide a lire, mais ne donne pas encore une entree."),
                    ("Setup", "Un setup combine plusieurs concepts dans un ordre logique : liquidite prise, reaction, structure, zone de retour, timing."),
                    ("Plan", "Un plan ajoute le risque : entree, stop, TP1/TP2, invalidation, taille de position, regle de gestion et condition de no trade."),
                ],
                "rule": "On peut observer un concept sans avoir de setup, et un setup sans avoir de plan executable.",
            },
            {
                "id": "exemple-fvg",
                "title": "Exemple : pourquoi FVG ne veut pas dire entree",
                "tag": "FVG",
                "cards": [
                    ("FVG comme concept", "Le prix a livre vite et laisse une zone peu negociee. C'est une information de desequilibre."),
                    ("FVG comme setup possible", "Le FVG devient interessant s'il suit un sweep utile, un displacement net et reste coherent avec le DOL."),
                    ("FVG comme plan", "Le plan precise l'entree dans la zone, le stop logique, la cible, le risque en R et le scenario qui annule l'idee."),
                ],
                "rule": "La question n'est pas 'y a-t-il un FVG ?', mais 'ce FVG appartient-il a une sequence tradable ?'.",
            },
            {
                "id": "checklist-plan",
                "title": "Checklist minimale d'un plan de trade",
                "tag": "execution",
                "cards": [
                    ("Contexte", "Bias, session, news, range, premium/discount et DOL sont notes avant le signal."),
                    ("Declencheur", "La liquidite prise, le displacement et la zone candidate sont nommes sans regarder le futur."),
                    ("Risque", "Stop, taille, TP1/TP2, BE, invalidation et limite journaliere sont definis avant l'ordre."),
                    ("Trace", "Une capture et une raison d'entree sont ecrites dans le journal, meme si le trade est refuse."),
                ],
                "rule": "Un plan incomplet se transforme presque toujours en improvisation pendant le trade.",
            },
        ],
    },
    "18-transition-reel.html": {
        "title": "ICT Atlas - Du propre au reel",
        "h1": "ICT Atlas - Du graphique propre au graphique reel",
        "subtitle": "Apprendre a passer des schemas parfaits aux marches ambigus sans sur-trader.",
        "goal": "faire la transition entre les exemples pedagogiques et les conditions bruitees d'un vrai graphique.",
        "prereq": "Avoir lu les setups coeur. Cette page se lit avant les variantes et les failures.",
        "sections": [
            {
                "id": "echelle-proprete",
                "title": "L'echelle de proprete d'un exemple",
                "tag": "progression",
                "cards": [
                    ("Niveau 1 - ideal", "Sweep net, displacement clair, FVG propre, DOL eloigne, timing parfait. Utile pour apprendre la forme."),
                    ("Niveau 2 - exploitable", "Quelques imperfections existent, mais la sequence centrale reste lisible et le risque est simple."),
                    ("Niveau 3 - ambigu", "Plusieurs FVG, structure hachee, DOL proche ou timing tardif. L'objectif est souvent d'attendre."),
                    ("Niveau 4 - refuse", "Le signal est seduisant mais il manque une condition centrale : liquidite, displacement, contexte ou risque."),
                    ("Niveau 5 - valide perdant", "Tout etait conforme, mais le resultat est negatif. C'est une donnee de backtest, pas une erreur automatique."),
                ],
                "rule": "Le marche reel paie la qualite du tri plus que la vitesse de reconnaissance.",
            },
            {
                "id": "ordre-de-comparaison",
                "title": "Comment etudier une famille de setups",
                "tag": "methode",
                "cards": [
                    ("1. Exemple parfait", "Comprendre la forme pure sans bruit."),
                    ("2. Variante acceptable", "Voir ce qui peut changer sans detruire la logique."),
                    ("3. Faux ami", "Identifier le detail qui rend le signal non tradable."),
                    ("4. Failure", "Accepter qu'un setup valide puisse perdre."),
                    ("5. Journee complete", "Replacer le trade dans la session entiere et pas dans une capture isolee."),
                ],
                "rule": "Pour chaque setup, etudie au moins un bon cas, un mauvais cas et un cas perdant valide.",
            },
            {
                "id": "signes-de-bruit",
                "title": "Signes que le graphique est trop sale",
                "tag": "no trade",
                "cards": [
                    ("Micro-signaux partout", "Chaque petite cassure ressemble a un MSS. En realite, aucun displacement ne domine."),
                    ("Zones concurrentes", "Trop de FVG ou d'OB se chevauchent. La zone d'execution n'est plus lisible."),
                    ("Cible deja atteinte", "Le DOL principal a ete touche. Entrer ensuite revient souvent a trader le reste du mouvement."),
                    ("News ou horaire pauvre", "Le setup technique existe mais le contexte d'execution rend le risque moins propre."),
                ],
                "rule": "No trade est une decision active, pas une absence de competence.",
            },
        ],
    },
    "19-preuve-statistique.html": {
        "title": "ICT Atlas - Preuve statistique",
        "h1": "ICT Atlas - Preuve statistique",
        "subtitle": "Transformer une idee visuelle en hypothese testee, mesurable et revisable.",
        "goal": "mettre le backtesting au centre du cours pour eviter de confondre confiance visuelle et edge reel.",
        "prereq": "Avoir compris concept, setup, plan et gestion du risque. Cette page se lit avant le trading live.",
        "sections": [
            {
                "id": "hypothese-testable",
                "title": "Un setup doit devenir une hypothese testable",
                "tag": "edge",
                "cards": [
                    ("Definition", "Une hypothese precise l'actif, la session, le contexte, le setup, l'entree, le stop, les objectifs et les exclusions."),
                    ("Mauvaise version", "Je trade les FVG propres quand le marche semble vouloir repartir."),
                    ("Bonne version", "Sur NQ, NY AM, apres sweep PDL et MSS M5, je teste un retour au CE du FVG si le DOL oppose reste a au moins 2R."),
                ],
                "rule": "Ce qui ne peut pas etre teste ne doit pas encore etre trade en reel.",
            },
            {
                "id": "echantillon-minimum",
                "title": "Echantillon minimum et donnees a noter",
                "tag": "backtest",
                "cards": [
                    ("50 occurrences", "Minimum pedagogique pour detecter les erreurs grossieres et commencer a voir le comportement du setup."),
                    ("100 occurrences", "Base plus serieuse pour comparer regimes de marche, sessions, jours de news et qualite A/B/C."),
                    ("Donnees obligatoires", "Date, actif, session, bias, DOL, setup, entree, stop, TP, resultat en R, frais/slippage, qualite et erreur eventuelle."),
                    ("Separation critique", "Distingue trade valide perdant, trade gagnant hors plan, no trade respecte et setup invalide evite."),
                ],
                "rule": "Un trade gagne hors plan n'est pas une preuve ; c'est une alerte de discipline.",
            },
            {
                "id": "decision-apres-test",
                "title": "Que faire apres le test",
                "tag": "decision",
                "cards": [
                    ("Garder", "Expectancy positive, drawdown acceptable, regles claires et erreurs corrigeables."),
                    ("Reduire", "Le setup fonctionne seulement dans certains horaires, certains actifs ou certains niveaux de qualite."),
                    ("Abandonner", "Expectancy negative, conditions trop subjectives ou pertes trop concentrees dans un regime frequent."),
                    ("Re-tester", "Modifier une seule variable a la fois : entree, BE, filtre DOL, horaire ou qualite minimale."),
                ],
                "rule": "Le backtest ne sert pas a prouver que tu as raison ; il sert a savoir quoi garder.",
            },
        ],
    },
    "20-workflow-session.html": {
        "title": "ICT Atlas - Workflow de session",
        "h1": "ICT Atlas - Workflow de session",
        "subtitle": "La routine complete avant, pendant et apres une session.",
        "goal": "relier la theorie, le risque, le live chart et le journal dans une sequence pratique.",
        "prereq": "Avoir lu les fondations, le risque et la preuve statistique. Cette page sert de protocole operationnel.",
        "sections": [
            {
                "id": "avant-session",
                "title": "Avant la session : preparer le terrain",
                "tag": "preparation",
                "cards": [
                    ("1. Contexte", "Verifier news, session, biais higher timeframe, range actuelle et zones premium/discount."),
                    ("2. Liquidites", "Marquer PDH, PDL, Asia High/Low, highs/lows internes et DOL probable."),
                    ("3. Scenario", "Ecrire le scenario prioritaire, le scenario alternatif et les conditions de no trade."),
                    ("4. Risque", "Fixer risque par trade, limite de pertes, nombre maximal de trades et heure d'arret."),
                ],
                "rule": "Une session commence avant la premiere bougie observee.",
            },
            {
                "id": "pendant-session",
                "title": "Pendant la session : attendre la permission",
                "tag": "execution",
                "cards": [
                    ("Observer", "Ne pas entrer sur le premier contact de liquidite. Attendre ce que le prix fait apres."),
                    ("Confirmer", "Chercher displacement, MSS, FVG/OB exploitable et coherence avec la cible."),
                    ("Executer", "Entrer seulement si le plan complet existe : entree, stop, TP, BE, invalidation et taille."),
                    ("Refuser", "Si une condition centrale manque, classer le cas en no trade avec une capture."),
                ],
                "rule": "Le role du trader est d'attendre une permission claire, pas de participer a chaque mouvement.",
            },
            {
                "id": "apres-session",
                "title": "Apres la session : transformer le resultat en donnee",
                "tag": "journal",
                "cards": [
                    ("Capture", "Garder une image avant/apres avec les niveaux et la raison d'entree ou de refus."),
                    ("Classement", "Valide gagnant, valide perdant, hors plan, no trade respecte ou setup invalide evite."),
                    ("Erreur", "Identifier si le probleme vient du biais, de l'entree, du risque, de la patience ou de la gestion."),
                    ("Prochaine action", "Un seul correctif pour la session suivante. Trop de modifications rendent le test illisible."),
                ],
                "rule": "La progression vient de la qualite du debrief, pas seulement du resultat financier.",
            },
        ],
    },
}


def text_tag(soup, name, text, **attrs):
    tag = soup.new_tag(name, **attrs)
    tag.string = text
    return tag


def page_links_html(active_file, soup):
    nav = soup.new_tag("div", **{"class": "nav-links"})
    for i, (href, label) in enumerate(PAGES, 1):
        attrs = {"href": href, "class": "active" if href == active_file else ""}
        a = soup.new_tag("a", **attrs)
        a.append(text_tag(soup, "span", f"{i:02d}", **{"class": "nav-num"}))
        a.append(text_tag(soup, "span", label))
        nav.append(a)
    return nav


def build_toc(soup):
    links = []
    for h2 in soup.select("main.page h2"):
        section = h2.find_parent("section")
        sid = section.get("id") if section else None
        if sid:
            title = h2.get_text(" ", strip=True)
            links.append((sid, title))
    if not links:
        return None
    wrapper = soup.new_tag("div", **{"class": "nav-section"})
    wrapper.append(text_tag(soup, "div", "Dans cette page", **{"class": "nav-section-title"}))
    toc = soup.new_tag("div", **{"class": "nav-links toc-links"})
    for sid, title in links:
        a = soup.new_tag("a", href=f"#{sid}")
        a.string = title if len(title) <= 58 else title[:55] + "..."
        toc.append(a)
    wrapper.append(toc)
    return wrapper


def rebuild_nav(soup, active_file):
    aside = soup.find("aside", class_="site-nav")
    if aside is None:
        return
    aside.clear()
    brand = soup.new_tag("div", **{"class": "nav-brand"})
    brand.append(text_tag(soup, "strong", "ICT Atlas"))
    brand.append(text_tag(soup, "span", "Cours guide + atlas visuel"))
    aside.append(brand)

    pages_section = soup.new_tag("div", **{"class": "nav-section"})
    pages_section.append(text_tag(soup, "div", "Chemin du cours", **{"class": "nav-section-title"}))
    pages_section.append(page_links_html(active_file, soup))
    aside.append(pages_section)

    toc = build_toc(soup)
    if toc:
        aside.append(toc)

    help_box = soup.new_tag("div", **{"class": "nav-help"})
    help_box.append(text_tag(soup, "strong", "Lecture guidee :"))
    help_box.append(soup.new_tag("br"))
    help_box.append("1. Comprendre le modele.")
    help_box.append(soup.new_tag("br"))
    help_box.append("2. Filtrer le setup.")
    help_box.append(soup.new_tag("br"))
    help_box.append("3. Tester avant d'executer.")
    aside.append(help_box)


def create_new_page(filename, spec):
    soup = BeautifulSoup("<!DOCTYPE html><html lang=\"fr\"><head></head><body></body></html>", "html.parser")
    head = soup.head
    head.append(soup.new_tag("meta", charset="utf-8"))
    head.append(soup.new_tag("meta", attrs={"name": "viewport", "content": "width=device-width,initial-scale=1"}))
    head.append(text_tag(soup, "title", spec["title"]))
    head.append(soup.new_tag("link", rel="stylesheet", href="style.css"))

    shell = soup.new_tag("div", **{"class": "app-shell"})
    aside = soup.new_tag("aside", **{"class": "site-nav", "aria-label": "Navigation principale"})
    shell.append(aside)
    main = soup.new_tag("main", **{"class": "page", "id": "contenu"})
    shell.append(main)
    soup.body.append(shell)

    hero = soup.new_tag("div", **{"class": "hero"})
    hero.append(text_tag(soup, "h1", spec["h1"]))
    hero.append(text_tag(soup, "p", spec["subtitle"]))
    main.append(hero)

    dashboard = soup.new_tag("div", **{"class": "page-meta-dashboard"})
    meta_main = soup.new_tag("div", **{"class": "meta-main"})
    goal = soup.new_tag("div", **{"class": "meta-goal"})
    goal.append(text_tag(soup, "strong", "Objectif"))
    goal.append(spec["goal"])
    prereq = soup.new_tag("div", **{"class": "meta-prereq"})
    prereq.append(text_tag(soup, "strong", "Prerequis"))
    prereq.append(spec["prereq"])
    meta_main.append(goal)
    meta_main.append(prereq)
    dashboard.append(meta_main)
    meta_side = soup.new_tag("div", **{"class": "meta-sidebar"})
    meta_side.append(text_tag(soup, "strong", "A lire avec"))
    pill_nav = soup.new_tag("nav", **{"class": "pill-nav"})
    for href, label in [("01-parcours.html", "Parcours"), ("12-gestion-risque.html", "Risque"), ("15-index-concepts.html", "Index")]:
        a = soup.new_tag("a", href=href, **{"class": "pill"})
        a.string = label
        pill_nav.append(a)
    meta_side.append(pill_nav)
    dashboard.append(meta_side)
    main.append(dashboard)

    for section in spec["sections"]:
        sec = soup.new_tag("section", **{"class": "card", "id": section["id"]})
        header = soup.new_tag("header")
        header.append(text_tag(soup, "h2", section["title"]))
        header.append(text_tag(soup, "span", section["tag"]))
        sec.append(header)
        grid = soup.new_tag("div", **{"class": "academy-grid"})
        for title, body in section["cards"]:
            card = soup.new_tag("div", **{"class": "academy-card"})
            card.append(text_tag(soup, "h3", title))
            card.append(text_tag(soup, "p", body))
            grid.append(card)
        sec.append(grid)
        rule = soup.new_tag("div", **{"class": "rule-block"})
        rule.append(text_tag(soup, "strong", "Regle :"))
        rule.append(" " + section["rule"])
        sec.append(rule)
        main.append(sec)

    rebuild_nav(soup, filename)
    Path(filename).write_text(str(soup), encoding="utf-8")


def update_home():
    path = Path("index.html")
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    hero = soup.find("div", class_="hero")
    if hero:
        h1 = hero.find("h1")
        p = hero.find("p")
        if h1:
            h1.string = "ICT Atlas - Cours complet"
        if p:
            p.string = "Parcours guide pour comprendre la logique ICT, filtrer les setups, tester l'edge et passer du schema au graphique live."

    intro = soup.find("div", id="v36-changelog")
    if intro:
        h3 = intro.find("h3")
        p = intro.find("p")
        if h3:
            h3.string = "V43 - transformation en vrai cours"
        if p:
            p.string = "Cette version ajoute les ponts pedagogiques manquants : modele mental, difference concept/setup/plan, passage au graphique reel, preuve statistique et workflow de session."

    home_map = soup.find("div", class_="home-map")
    if home_map:
        home_map.clear()
        cards = [
            ("Chemin principal", "Lis les pages dans l'ordre de la navigation. Les anciennes pages d'atlas deviennent des chapitres d'application, pas des blocs isoles.", ["Comprendre", "Filtrer", "Tester", "Executer"]),
            ("Ordre recommande", "La progression part de la mecanique, passe par les setups, puis seulement ensuite vers le live et les contraintes prop firm.", [f"{i:02d}. {label}" for i, (_, label) in enumerate(PAGES[1:11], 2)]),
        ]
        for title, body, items in cards:
            div = soup.new_tag("div", **{"class": "home-card"})
            div.append(text_tag(soup, "h3", title))
            div.append(text_tag(soup, "p", body))
            ul = soup.new_tag("ul")
            for item in items:
                li = soup.new_tag("li")
                li.string = item
                ul.append(li)
            div.append(ul)
            home_map.append(div)

    section_links = soup.find("div", class_="section-links")
    if section_links:
        section_links.clear()
        descriptions = {
            "Modele mental": "Le fil rouge : liquidite, delivery, retour et cible.",
            "Concept/plan": "Distinguer concept, setup et plan executable.",
            "Graphique reel": "Passer des exemples propres aux marches ambigus.",
            "Preuve stats": "Backtesting, echantillon, expectancy et decision.",
            "Session live": "Routine avant, pendant et apres la session.",
        }
        fallback = {
            "Accueil": "Point d'entree du cours.",
            "Parcours": "Plan d'apprentissage, exercices, evaluation et journal.",
            "Mecanique": "Ordres, liquidite, execution et logique institutionnelle.",
            "Glossaire": "Definitions ICT et bases visuelles toujours accessibles.",
            "Fondations": "Top-down, DOL, kill zones, erreurs et decision.",
            "Setups coeur": "FVG, MSS, OB, Breaker, OTE et setups principaux.",
            "Variantes": "Cas limites, faux signaux et setups degrades.",
            "Failures": "Setups valides perdants, journees completes et no trade.",
            "Contextes": "Daily Bias, Narrative, SMT et news.",
            "Risque": "Sizing, RR, expectancy, breakeven et regles d'arret.",
            "TradingView": "Configuration live chart et Bar Replay.",
            "Programme": "Routine avancee, checklist, examen et drills.",
            "Quiz": "Questions masquees et entrainement actif.",
            "Prop Firm": "Drawdown, challenge, sizing et discipline.",
            "Synthese": "Checklist finale et recapitulatif.",
            "Index": "Recherche rapide des concepts.",
        }
        for href, label in PAGES:
            a = soup.new_tag("a", href=href, **{"class": "section-link"})
            a.append(text_tag(soup, "h3", label))
            a.append(text_tag(soup, "p", descriptions.get(label, fallback.get(label, ""))))
            section_links.append(a)

    rebuild_nav(soup, "index.html")
    path.write_text(str(soup), encoding="utf-8")


def update_parcours():
    path = Path("01-parcours.html")
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    first_card = soup.find("section", class_="card")
    if first_card and not soup.find(id="chemin-principal-v43"):
        sec = soup.new_tag("section", **{"class": "card mini-anchor", "id": "chemin-principal-v43"})
        header = soup.new_tag("header")
        header.append(text_tag(soup, "h2", "00X - Chemin principal : du modele a l'execution"))
        header.append(text_tag(soup, "span", "V43"))
        sec.append(header)
        grid = soup.new_tag("div", **{"class": "academy-grid"})
        cards = [
            ("1. Modele mental", "Comprendre la sequence liquidite -> displacement -> zone de retour -> DOL."),
            ("2. Langage", "Lire la mecanique puis le vocabulaire, pour eviter les mots appris sans causalite."),
            ("3. Setup", "Passer de concept a setup puis a plan complet avec risque et invalidation."),
            ("4. Realite", "Comparer exemple propre, variante, faux ami, failure et journee complete."),
            ("5. Preuve", "Tester sur un echantillon, mesurer l'expectancy et garder seulement ce qui resiste aux donnees."),
            ("6. Execution", "Utiliser le workflow de session avant de passer au live ou a la prop firm."),
        ]
        for title, body in cards:
            div = soup.new_tag("div", **{"class": "academy-card"})
            div.append(text_tag(soup, "h3", title))
            div.append(text_tag(soup, "p", body))
            grid.append(div)
        sec.append(grid)
        rule = soup.new_tag("div", **{"class": "rule-block"})
        rule.append(text_tag(soup, "strong", "Regle :"))
        rule.append(" Le cours se lit en ligne droite la premiere fois, puis l'atlas sert de reference.")
        sec.append(rule)
        first_card.insert_before(sec)
    rebuild_nav(soup, "01-parcours.html")
    path.write_text(str(soup), encoding="utf-8")


def update_all_existing_nav():
    for path in Path(".").glob("*.html"):
        if path.name in NEW_PAGES:
            continue
        soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
        rebuild_nav(soup, path.name)
        path.write_text(str(soup), encoding="utf-8")


def main():
    for filename, spec in NEW_PAGES.items():
        create_new_page(filename, spec)
    update_home()
    update_parcours()
    update_all_existing_nav()
    Path("README_V43.txt").write_text(
        "ICT Atlas V43 - Cours guide\n\n"
        "Ajouts: modele mental, concept/setup/plan, transition graphique reel, preuve statistique, workflow de session.\n"
        "Navigation reordonnee pour transformer l'atlas en parcours lineaire sans supprimer les pages de reference.\n\n"
        "Point d'entree: index.html\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
