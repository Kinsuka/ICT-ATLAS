from pathlib import Path
from bs4 import BeautifulSoup


PARTS = [
    {
        "label": "Partie 1",
        "title": "Comprendre la logique ICT",
        "lessons": [
            ("index.html", "Accueil du cours"),
            ("16-modele-mental.html", "Modèle mental"),
            ("01-parcours.html", "Tirez le maximum du cours"),
            ("11-mecanique-marches.html", "Comprenez la mécanique des marchés"),
            ("23-langage-ict-contexte.html", "Lisez le langage ICT en contexte"),
            ("21-liquidite-deplacement.html", "Comprenez le déplacement du prix"),
            ("27-fondations-liquidite.html", "Lisez la liquidité"),
            ("28-fondations-entree.html", "Construisez le scénario d’entrée"),
            ("29-fondations-stop-tp.html", "Placez stop, invalidation et TP"),
            ("22-structure-trend-range.html", "Comprenez trend, range et transitions"),
            ("17-concept-setup-plan.html", "Distinguez concept, setup et plan"),
        ],
    },
    {
        "label": "Partie 2",
        "title": "Construire une lecture de setup",
        "lessons": [
            ("24-premium-discount-killzones.html", "Situez où et quand chercher"),
            ("03-fondations.html", "Posez les fondations de décision"),
            ("25-top-down-multi-timeframe.html", "Lisez en top-down multi-timeframe"),
            ("31-order-blocks.html", "Comprenez les Order Blocks"),
            ("32-fvg-imbalance-ce.html", "Comprenez FVG, imbalance et CE"),
            ("33-mss-changement-controle.html", "Validez le MSS et le changement de contrôle"),
            ("34-breaker-mitigation.html", "Comprenez breaker et mitigation"),
            ("35-pd-arrays-hierarchie.html", "Priorisez les PD Arrays"),
            ("04-setups-core.html", "Reconnaissez les setups cœur"),
            ("18-transition-reel.html", "Passez du propre au réel"),
            ("05-variantes.html", "Filtrez les variantes et faux signaux"),
            ("07-failures-journees.html", "Acceptez les failures et journées complexes"),
        ],
    },
    {
        "label": "Partie 3",
        "title": "Tester, risquer et exécuter",
        "lessons": [
            ("06-contextes-avances.html", "Ajoutez les contextes avancés"),
            ("12-gestion-risque.html", "Calculez le risque"),
            ("19-preuve-statistique.html", "Prouvez l’edge statistiquement"),
            ("26-psychologie-trader.html", "Travaillez le jeu mental"),
            ("20-workflow-session.html", "Préparez une session live"),
            ("14-live-chart.html", "Lisez un graphique TradingView"),
        ],
    },
    {
        "label": "Partie 4",
        "title": "Valider et pratiquer",
        "lessons": [
            ("10-programme-avance.html", "Suivez le programme avancé"),
            ("30-replay-lab.html", "Entraînez-vous en bar replay"),
            ("08-quiz.html", "Passez les quiz"),
            ("13-prop-firm.html", "Adaptez-vous aux prop firms"),
            ("09-synthese.html", "Validez la synthèse finale"),
            ("15-index-concepts.html", "Retrouvez les concepts"),
        ],
    },
]


def flatten_lessons():
    lessons = []
    for part_index, part in enumerate(PARTS, 1):
        for lesson_index, (href, title) in enumerate(part["lessons"], 1):
            lessons.append(
                {
                    "href": href,
                    "title": title,
                    "part_index": part_index,
                    "lesson_index": lesson_index,
                    "part_label": part["label"],
                    "part_title": part["title"],
                }
            )
    return lessons


LESSONS = flatten_lessons()
LESSON_BY_FILE = {lesson["href"]: lesson for lesson in LESSONS}

LESSON_OBJECTIVES = {
    "index.html": [
        ("Objectif", "Comprendre le parcours sans entrer encore dans les setups."),
        ("Avant de continuer", "Repère où se trouvent le glossaire, l’index et la progression principale."),
        ("Checkpoint", "Tu dois savoir quelle page lire ensuite et pourquoi."),
    ],
    "16-modele-mental.html": [
        ("Objectif", "Construire l’idée simple qui organise tout le cours : liquidité, réaction, retour, cible."),
        ("Avant de continuer", "Ne cherche pas encore à mémoriser les sigles ICT ; ils seront définis au fur et à mesure."),
        ("Checkpoint", "Tu dois pouvoir raconter le mouvement du prix en une phrase simple."),
    ],
    "01-parcours.html": [
        ("Objectif", "Comprendre comment travailler le cours, produire des captures et construire un journal."),
        ("Avant de continuer", "Le parcours sert à apprendre dans l’ordre, pas à picorer uniquement les setups."),
        ("Checkpoint", "Tu dois savoir quoi pratiquer après chaque leçon."),
    ],
    "11-mecanique-marches.html": [
        ("Objectif", "Comprendre pourquoi le prix bouge avant d’apprendre les formes ICT."),
        ("Avant de continuer", "Retiens surtout ordres, liquidité, absorption et déplacement ; les sigles viendront ensuite."),
        ("Checkpoint", "Tu dois savoir expliquer pourquoi une zone évidente attire le prix."),
    ],
    "23-langage-ict-contexte.html": [
        ("Objectif", "Apprendre les sigles essentiels dans la logique du modèle, pas comme une liste abstraite."),
        ("Avant de continuer", "Chaque mot doit répondre à une question : où est la liquidité, que fait le prix, quelle zone reste exploitable ?"),
        ("Checkpoint", "Tu dois pouvoir lire FVG, MSS, DOL, OB, CE, BSL et SSL sans quitter le fil du cours."),
    ],
    "21-liquidite-deplacement.html": [
        ("Objectif", "Relier recherche de liquidité et réaction du prix après la prise."),
        ("Avant de continuer", "Un sweep seul ne suffit pas : la réaction après la prise est le cœur de la leçon."),
        ("Checkpoint", "Tu dois distinguer continuation, absorption et retournement."),
    ],
    "27-fondations-liquidite.html": [
        ("Objectif", "Savoir où la liquidité se trouve avant de parler d’entrée."),
        ("Avant de continuer", "Une liquidité peut être une cible, un déclencheur ou une zone déjà consommée."),
        ("Checkpoint", "Tu dois pouvoir classer une zone : externe, interne, faible, propre ou déjà prise."),
    ],
    "28-fondations-entree.html": [
        ("Objectif", "Comprendre pourquoi une entrée n’est autorisée qu’après une séquence causale."),
        ("Avant de continuer", "FVG, CE, OB et MSS ne sont pas des boutons d’achat ou de vente."),
        ("Checkpoint", "Tu dois pouvoir dire ce qui manque dans une entrée trop tôt ou hors contexte."),
    ],
    "29-fondations-stop-tp.html": [
        ("Objectif", "Relier entrée, invalidation, stop, TP1 et TP2 à la structure du marché."),
        ("Avant de continuer", "Un stop n’est pas une distance confortable ; un TP n’est pas un chiffre rond."),
        ("Checkpoint", "Tu dois pouvoir justifier où le trade est faux et où le prix peut raisonnablement aller."),
    ],
    "22-structure-trend-range.html": [
        ("Objectif", "Identifier si le marché est en trend, en range ou en transition avant de chercher un setup."),
        ("Avant de continuer", "Cette leçon ne demande pas encore de trader : elle sert à filtrer l’environnement."),
        ("Checkpoint", "Tu dois pouvoir dire quel type de setup est cohérent avec l’environnement."),
    ],
    "17-concept-setup-plan.html": [
        ("Objectif", "Séparer concept observé, setup possible et plan réellement exécutable."),
        ("Avant de continuer", "Voir une forme sur le graphique n’autorise pas encore une entrée."),
        ("Checkpoint", "Tu dois pouvoir refuser un beau signal s’il manque contexte, risque ou cible."),
    ],
    "24-premium-discount-killzones.html": [
        ("Objectif", "Ajouter les deux filtres qui manquent avant les setups : où dans la range, et quand dans la session."),
        ("Avant de continuer", "Premium/discount répond au WHERE ; kill zone répond au WHEN."),
        ("Checkpoint", "Tu dois savoir refuser un setup bien formé s’il arrive au mauvais endroit ou au mauvais moment."),
    ],
    "03-fondations.html": [
        ("Objectif", "Assembler contexte, timing, environnement et décision avant les setups détaillés."),
        ("Avant de continuer", "Cette page est dense : lis-la comme une méthode de tri, pas comme une liste à mémoriser."),
        ("Checkpoint", "Tu dois savoir pourquoi un setup peut être interdit malgré une belle forme."),
    ],
    "25-top-down-multi-timeframe.html": [
        ("Objectif", "Comprendre de quel timeframe part la narrative et sur lequel l’entrée se précise."),
        ("Avant de continuer", "Un signal 5M peut être beau mais interdit si le Daily ou le 4H racontent l’inverse."),
        ("Checkpoint", "Tu dois pouvoir descendre Weekly/Daily vers 5M sans inverser les rôles."),
    ],
    "31-order-blocks.html": [
        ("Objectif", "Comprendre ce qu’un Order Block représente, quand il est utile et quand il devient un piège."),
        ("Avant de continuer", "Un OB n’est pas simplement la dernière bougie avant un mouvement : il doit être validé par contexte, liquidité et displacement."),
        ("Checkpoint", "Tu dois pouvoir distinguer OB valide, OB faible, OB mitigé et breaker."),
    ],
    "32-fvg-imbalance-ce.html": [
        ("Objectif", "Comprendre ce qu’un FVG représente, comment lire l’imbalance et quand utiliser le CE."),
        ("Avant de continuer", "Un FVG n’est pas une zone magique : il doit venir d’un displacement et rester cohérent avec liquidité, contexte et objectif."),
        ("Checkpoint", "Tu dois pouvoir distinguer FVG net, gap trop fin, zone déjà comblée et retour dangereux."),
    ],
    "33-mss-changement-controle.html": [
        ("Objectif", "Comprendre ce qu’un MSS valide confirme : un changement de contrôle après une prise de liquidité."),
        ("Avant de continuer", "Un simple break de micro-swing ne suffit pas : il faut contexte, displacement et niveau structurel pertinent."),
        ("Checkpoint", "Tu dois pouvoir distinguer MSS valide, cassure mineure, CHoCH faible et faux shift."),
    ],
    "34-breaker-mitigation.html": [
        ("Objectif", "Comprendre quand une zone tient, quand elle est mitigée, et quand elle devient breaker."),
        ("Avant de continuer", "Un breaker n’est pas une zone cassée au hasard : il vient d’une invalidation lisible après changement de contrôle."),
        ("Checkpoint", "Tu dois pouvoir distinguer OB actif, mitigation, OB cassé, breaker valide et faux breaker."),
    ],
    "35-pd-arrays-hierarchie.html": [
        ("Objectif", "Savoir prioriser les zones ICT quand plusieurs PD Arrays se superposent."),
        ("Avant de continuer", "Une zone n’a pas la même valeur selon timeframe, premium/discount, liquidité, contexte et distance au TP."),
        ("Checkpoint", "Tu dois pouvoir choisir la meilleure zone ou refuser le trade quand la carte est trop confuse."),
    ],
    "04-setups-core.html": [
        ("Objectif", "Découvrir les familles de setups cœur sans les confondre avec des signaux automatiques."),
        ("Avant de continuer", "Chaque setup doit être lu comme une séquence : contexte, liquidité, déplacement, zone, risque."),
        ("Checkpoint", "Tu dois pouvoir expliquer pourquoi une entrée est autorisée ou refusée."),
    ],
    "18-transition-reel.html": [
        ("Objectif", "Passer du schéma propre au graphique réel, plus ambigu et plus bruyant."),
        ("Avant de continuer", "Le but n’est pas de trouver plus de trades, mais de mieux trier."),
        ("Checkpoint", "Tu dois distinguer exemple idéal, cas exploitable, cas ambigu et no trade."),
    ],
    "05-variantes.html": [
        ("Objectif", "Reconnaître les faux amis et les versions dégradées des setups."),
        ("Avant de continuer", "Une variante n’est pas forcément tradable : elle sert d’abord à entraîner le filtre."),
        ("Checkpoint", "Tu dois savoir nommer ce qui manque dans un signal séduisant."),
    ],
    "07-failures-journees.html": [
        ("Objectif", "Comprendre qu’un setup valide peut perdre sans que le modèle soit faux."),
        ("Avant de continuer", "On sépare ici erreur de lecture, no trade et perte normale."),
        ("Checkpoint", "Tu dois pouvoir classer une perte : erreur, hors plan ou perte valide."),
    ],
    "19-preuve-statistique.html": [
        ("Objectif", "Transformer une idée visuelle en hypothèse mesurable."),
        ("Avant de continuer", "Un beau pattern ne prouve rien tant qu’il n’a pas été testé sur un échantillon."),
        ("Checkpoint", "Tu dois savoir quelles données noter pour vérifier un edge."),
    ],
    "26-psychologie-trader.html": [
        ("Objectif", "Préparer le passage au réel : pertes, euphorie, revenge trade, tilt et discipline prop firm."),
        ("Avant de continuer", "La psychologie ne remplace pas le plan ; elle protège le plan quand l’émotion monte."),
        ("Checkpoint", "Tu dois avoir un protocole écrit après gain, perte et série de pertes."),
    ],
    "30-replay-lab.html": [
        ("Objectif", "Transformer les schémas propres du cours en exercices sur graphique réel, sans regarder le futur."),
        ("Avant de continuer", "Le replay n’est utile que si tu notes ta décision avant de voir la suite."),
        ("Checkpoint", "Tu dois pouvoir produire une fiche de cas : contexte, liquidité, décision, invalidation, résultat."),
    ],
}

GLOSSARY_TERMS = [
    ("Liquidité", "Zones où les ordres sont probablement concentrés : stops au-dessus des highs, stops sous les lows, niveaux évidents."),
    ("BSL / SSL", "Buy-Side Liquidity au-dessus d’un high ; Sell-Side Liquidity sous un low. Ce sont des cibles possibles, pas des entrées."),
    ("Sweep / Raid", "Dépassement d’un high ou low visible pour prendre la liquidité. On observe ensuite la réaction du prix."),
    ("DOL", "Draw on Liquidity : cible de liquidité la plus logique dans le contexte actuel."),
    ("PDH / PDL", "Previous Day High / Low. Repères journaliers majeurs pour lire la liquidité et le biais."),
    ("Displacement", "Mouvement impulsif qui montre une livraison rapide du prix et un déséquilibre directionnel."),
    ("FVG", "Fair Value Gap : zone créée par une livraison rapide. Elle devient utile seulement avec contexte, cible et invalidation."),
    ("MSS", "Market Structure Shift : changement de structure après une prise de liquidité ou une rupture de contrôle."),
    ("OB", "Order Block : dernière zone opposée avant une impulsion significative. Zone candidate, pas signal automatique."),
    ("Breaker", "Ancien OB invalidé qui peut agir dans l’autre sens après changement de structure."),
    ("PD Arrays", "Famille de zones de prix utiles en lecture ICT : OB, FVG, breaker, liquidité, premium/discount ou niveaux HTF. Elles doivent être priorisées."),
    ("OTE", "Optimal Trade Entry : zone de retracement, généralement utilisée seulement si l’ancrage du mouvement est justifié."),
    ("CE", "Consequent Encroachment : milieu d’une zone, souvent utilisé comme repère de précision ou de qualité."),
    ("Premium / Discount", "Position du prix dans une range. Acheter en discount et vendre en premium donne une meilleure logique contextuelle."),
    ("Kill Zone", "Fenêtre horaire où l’on accepte de chercher certains setups. Hors timing, le même signal perd en qualité."),
    ("Trend", "Environnement directionnel : impulsions plus fortes que corrections. Les pullbacks dans le sens du flux sont favorisés."),
    ("Range", "Environnement d’équilibre relatif : rejet, absorption et faux breakouts sont plus fréquents."),
    ("Transition", "Phase où le marché passe d’un équilibre à un déséquilibre, ou d’une tendance à une autre."),
    ("Pullback", "Correction contre l’impulsion. Il est sain s’il respecte la structure et ne détruit pas le déplacement précédent."),
    ("Failed breakout", "Cassure sans acceptation : le prix sort d’une zone puis réintègre rapidement la range."),
    ("Edge", "Avantage mesurable sur échantillon. Un beau pattern ne devient un edge qu’après preuve statistique."),
]


def tag(soup, name, text=None, **attrs):
    item = soup.new_tag(name, **attrs)
    if text is not None:
        item.string = text
    return item


def lesson_position(filename):
    for index, lesson in enumerate(LESSONS):
        if lesson["href"] == filename:
            return index, lesson
    return 0, LESSONS[0]


def rebuild_course_nav(soup, filename):
    aside = soup.find("aside", class_="site-nav")
    if not aside:
        return
    _, current = lesson_position(filename)
    aside.clear()

    brand = tag(soup, "div", **{"class": "nav-brand"})
    brand.append(tag(soup, "strong", "ICT Atlas"))
    brand.append(tag(soup, "span", "Cours guidé · trading ICT"))
    aside.append(brand)

    nav_title = tag(soup, "div", **{"class": "course-nav-title"})
    nav_title.append(tag(soup, "span", "Table des matières"))
    nav_title.append(tag(soup, "small", f"{len(LESSONS)} leçons"))
    aside.append(nav_title)

    glossary_link = soup.new_tag("button", type="button", **{"class": "glossary-nav-link"})
    glossary_link["data-glossary-open"] = ""
    glossary_link.append(tag(soup, "strong", "Glossaire rapide"))
    glossary_link.append(tag(soup, "span", "Ouvrir sans quitter la leçon"))
    aside.append(glossary_link)

    resources_link = soup.new_tag("a", href="ressources-pratiques.html", **{"class": "resources-nav-link"})
    resources_link.append(tag(soup, "strong", "Ressources pratiques"))
    resources_link.append(tag(soup, "span", "Journal · Backtest · Checklist"))
    aside.append(resources_link)

    global_number = 1
    for part in PARTS:
        part_block = tag(soup, "div", **{"class": "course-part"})
        part_head = tag(soup, "div", **{"class": "course-part-head"})
        part_head.append(tag(soup, "span", part["label"]))
        part_head.append(tag(soup, "strong", part["title"]))
        part_block.append(part_head)

        lessons_list = tag(soup, "ol", **{"class": "course-lessons"})
        for local_index, (href, title) in enumerate(part["lessons"], 1):
            li_class = "course-lesson active" if href == filename else "course-lesson"
            li = tag(soup, "li", **{"class": li_class})
            a = soup.new_tag("a", href=href)
            a.append(tag(soup, "span", f"{local_index}", **{"class": "lesson-bullet"}))
            text = tag(soup, "span", **{"class": "lesson-link-text"})
            text.append(tag(soup, "strong", title))
            text.append(tag(soup, "small", f"Leçon {global_number:02d}"))
            a.append(text)
            li.append(a)
            lessons_list.append(li)
            global_number += 1
        part_block.append(lessons_list)
        aside.append(part_block)

    help_box = tag(soup, "div", **{"class": "nav-help"})
    help_box.append(tag(soup, "strong", "Méthode"))
    help_box.append(soup.new_tag("br"))
    help_box.append("Lisez dans l’ordre, pratiquez en replay, puis validez par journal et stats.")
    aside.append(help_box)

    old_fab = soup.find(class_="glossary-fab")
    if old_fab:
        old_fab.decompose()
    old_panel = soup.find("div", class_="glossary-panel-shell")
    if old_panel:
        old_panel.decompose()
    old_script = soup.find("script", src="glossary-panel.js")
    if old_script:
        old_script.decompose()
    if soup.body:
        fab = soup.new_tag("button", type="button", **{"class": "glossary-fab", "aria-label": "Ouvrir le glossaire ICT"})
        fab["data-glossary-open"] = ""
        fab.string = "Glossaire"
        soup.body.append(fab)
        soup.body.append(build_glossary_panel(soup))
        script = soup.new_tag("script", src="glossary-panel.js", defer=True)
        soup.body.append(script)


def build_glossary_panel(soup):
    shell = tag(soup, "div", **{"class": "glossary-panel-shell", "aria-hidden": "true"})
    backdrop = tag(soup, "button", type="button", **{"class": "glossary-backdrop", "aria-label": "Fermer le glossaire"})
    backdrop["data-glossary-close"] = ""
    shell.append(backdrop)

    panel = tag(
        soup,
        "aside",
        **{"class": "glossary-panel", "role": "dialog", "aria-modal": "true", "aria-labelledby": "glossary-panel-title"},
    )
    head = tag(soup, "div", **{"class": "glossary-panel-head"})
    title_wrap = tag(soup, "div")
    title_wrap.append(tag(soup, "span", "Référence rapide", **{"class": "glossary-panel-kicker"}))
    title_wrap.append(tag(soup, "h2", "Glossaire ICT", id="glossary-panel-title"))
    head.append(title_wrap)
    close = tag(soup, "button", "Fermer", type="button", **{"class": "glossary-close"})
    close["data-glossary-close"] = ""
    head.append(close)
    panel.append(head)

    intro = tag(soup, "p", "Cherche un terme sans quitter la leçon. Pour les définitions longues, ouvre la page complète.")
    intro["class"] = "glossary-panel-intro"
    panel.append(intro)

    search = soup.new_tag(
        "input",
        type="search",
        placeholder="Rechercher : FVG, sweep, DOL...",
        **{"class": "glossary-search", "aria-label": "Rechercher dans le glossaire"},
    )
    search["data-glossary-search"] = ""
    panel.append(search)

    list_wrap = tag(soup, "div", **{"class": "glossary-list"})
    list_wrap["data-glossary-list"] = ""
    for term, definition in GLOSSARY_TERMS:
        item = tag(soup, "article", **{"class": "glossary-item"})
        item["data-glossary-item"] = ""
        item["data-glossary-text"] = f"{term} {definition}".lower()
        item.append(tag(soup, "h3", term))
        item.append(tag(soup, "p", definition))
        list_wrap.append(item)
    panel.append(list_wrap)

    full = soup.new_tag("a", href="glossaire.html", **{"class": "glossary-full-link"})
    full.string = "Ouvrir la page glossaire complète"
    panel.append(full)
    shell.append(panel)
    return shell


def insert_lesson_header(soup, filename):
    main = soup.find("main", class_="page")
    if not main:
        return
    old = main.find("div", class_="lesson-header")
    if old:
        old.decompose()
    old_bottom = main.find("nav", class_="lesson-bottom-nav")
    if old_bottom:
        old_bottom.decompose()

    index, lesson = lesson_position(filename)
    previous_lesson = LESSONS[index - 1] if index > 0 else None
    next_lesson = LESSONS[index + 1] if index + 1 < len(LESSONS) else None

    header = tag(soup, "div", **{"class": "lesson-header"})
    meta = tag(soup, "div", **{"class": "lesson-meta"})
    meta.append(tag(soup, "span", lesson["part_label"]))
    meta.append(tag(soup, "span", f"Leçon {index + 1:02d}/{len(LESSONS):02d}"))
    header.append(meta)
    header.append(tag(soup, "div", lesson["part_title"], **{"class": "lesson-part-title"}))

    progress = tag(soup, "div", **{"class": "course-progress", "aria-label": "Progression du cours"})
    bar = tag(soup, "span")
    bar["style"] = f"width:{round(((index + 1) / len(LESSONS)) * 100, 2)}%"
    progress.append(bar)
    header.append(progress)

    pager = tag(soup, "nav", **{"class": "lesson-pager", "aria-label": "Navigation de leçon"})
    if previous_lesson:
        prev = soup.new_tag("a", href=previous_lesson["href"], **{"class": "pager-link"})
        prev.append(tag(soup, "small", "Précédent"))
        prev.append(tag(soup, "span", previous_lesson["title"]))
        pager.append(prev)
    else:
        pager.append(tag(soup, "span", "Début du cours", **{"class": "pager-link disabled"}))
    if next_lesson:
        nxt = soup.new_tag("a", href=next_lesson["href"], **{"class": "pager-link next"})
        nxt.append(tag(soup, "small", "Suivant"))
        nxt.append(tag(soup, "span", next_lesson["title"]))
        pager.append(nxt)
    else:
        pager.append(tag(soup, "span", "Fin du cours", **{"class": "pager-link disabled next"}))
    header.append(pager)

    hero = main.find("div", class_="hero")
    if hero:
        hero.insert_before(header)
    else:
        main.insert(0, header)

    bottom = tag(soup, "nav", **{"class": "lesson-bottom-nav", "aria-label": "Navigation finale de leçon"})
    if previous_lesson:
        prev = soup.new_tag("a", href=previous_lesson["href"], **{"class": "bottom-link"})
        prev.append(tag(soup, "small", "Revoir"))
        prev.append(tag(soup, "span", previous_lesson["title"]))
        bottom.append(prev)
    if next_lesson:
        nxt = soup.new_tag("a", href=next_lesson["href"], **{"class": "bottom-link next"})
        nxt.append(tag(soup, "small", "Continuer"))
        nxt.append(tag(soup, "span", next_lesson["title"]))
        bottom.append(nxt)
    main.append(bottom)


def add_lesson_intro(soup, filename):
    main = soup.find("main", class_="page")
    if not main:
        return
    old = main.find("section", class_="lesson-objectives")
    if old:
        old.decompose()
    hero = main.find("div", class_="hero")
    if not hero:
        return
    lesson = LESSON_BY_FILE.get(filename)
    if not lesson:
        return
    intro = tag(soup, "section", **{"class": "lesson-objectives"})
    intro.append(tag(soup, "h2", "Dans cette leçon"))
    grid = tag(soup, "div", **{"class": "lesson-objective-grid"})
    objectives = LESSON_OBJECTIVES.get(filename, [
        ("Objectif", "Comprendre le rôle de cette leçon dans le parcours complet."),
        ("À produire", "Une note, une capture ou une décision claire avant de passer à la suite."),
        ("À retenir", f"Cette leçon appartient à : {lesson['part_title']}."),
    ])
    for title, body in objectives:
        card = tag(soup, "div", **{"class": "lesson-objective"})
        card.append(tag(soup, "strong", title))
        card.append(tag(soup, "p", body))
        grid.append(card)
    intro.append(grid)
    hero.insert_after(intro)


def main():
    for path in sorted(Path(".").glob("*.html")):
        if path.name not in LESSON_BY_FILE:
            continue
        soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
        rebuild_course_nav(soup, path.name)
        insert_lesson_header(soup, path.name)
        add_lesson_intro(soup, path.name)
        path.write_text(str(soup), encoding="utf-8")


if __name__ == "__main__":
    main()
