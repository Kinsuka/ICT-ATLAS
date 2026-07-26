import json
from pathlib import Path
from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parents[1]
PARTS = json.loads((ROOT / "data" / "course-navigation.json").read_text(encoding="utf-8"))


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
    "40-displacement-operationnel.html": [
        ("Objectif", "Transformer le mot displacement en critère observable : impulsion, corps, vitesse, rupture et acceptation."),
        ("Avant de continuer", "Une grosse bougie ne suffit pas ; le displacement doit livrer une information de contrôle."),
        ("Checkpoint", "Tu dois pouvoir classer un mouvement : displacement valide, impulsion ambiguë ou simple bruit."),
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
    "36-ote-dealing-range.html": [
        ("Objectif", "Savoir choisir la bonne dealing range et ancrer un OTE sans forcer le graphique."),
        ("Avant de continuer", "Un OTE n’est utile que si le swing choisi vient d’un déplacement pertinent et reste aligné avec la carte."),
        ("Checkpoint", "Tu dois pouvoir refuser un OTE joli mais ancré sur le mauvais mouvement."),
    ],
    "37-dol-targets-hierarchie.html": [
        ("Objectif", "Construire une hiérarchie de targets : TP1, TP2, DOL, protection et refus du trade."),
        ("Avant de continuer", "On ne prédit pas le retournement : on réduit le risque quand le prix arrive sur une zone de liquidité ou d’opposition."),
        ("Checkpoint", "Tu dois pouvoir dire où prendre partiel, où viser la cible principale et quand le TP est trop faible pour trader."),
    ],
    "38-smt-divergence.html": [
        ("Objectif", "Comprendre SMT comme divergence de confirmation entre marchés corrélés, pas comme setup autonome."),
        ("Avant de continuer", "Une SMT utile doit apparaître sur une liquidité pertinente et être suivie d’une réaction du prix."),
        ("Checkpoint", "Tu dois pouvoir distinguer SMT valide, non-confirmation faible, corrélation cassée et faux signal."),
    ],
    "39-profils-journee-sessions.html": [
        ("Objectif", "Identifier trend day, range day, reversal day, AM expansion/PM continuation et no-trade day avant de choisir un setup."),
        ("Avant de continuer", "Un setup n’a pas la même valeur selon le profil de journée et la phase de session."),
        ("Checkpoint", "Tu dois pouvoir adapter entrée, target, protection ou refus au profil dominant de la journée."),
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
    "41-no-trade.html": [
        ("Objectif", "Transformer le refus du trade en décision active, écrite et mesurable."),
        ("Avant de continuer", "Un no trade n’est pas une absence de travail : c’est le filtre qui protège l’edge."),
        ("Checkpoint", "Tu dois pouvoir refuser un setup tentant avec une raison précise : contexte, timing, target, risque ou état mental."),
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
    "06-contextes-avances.html": [
        ("Objectif", "Combiner Daily Bias, narrative, SMT et contexte événementiel sans transformer une confluence en signal automatique."),
        ("À produire", "Une fiche de contexte qui sépare faits observés, hypothèse, invalidation et conditions de no trade."),
        ("Checkpoint", "Sur un cas inédit, tu dois choisir trade ou no trade et nommer le fait précis qui invalide ta lecture."),
    ],
    "12-gestion-risque.html": [
        ("Objectif", "Transformer une invalidation graphique en taille de position et en risque total de session."),
        ("À produire", "Une fiche de risque avec capital, risque en pourcentage, distance du stop, taille et perte maximale quotidienne."),
        ("Checkpoint", "Tu dois calculer une taille correcte et refuser le trade si le stop structurel dépasse ton budget de risque."),
    ],
    "20-workflow-session.html": [
        ("Objectif", "Enchaîner préparation, autorisation, exécution et review dans un protocole unique."),
        ("À produire", "Un cockpit de session rempli avant l’ouverture, puis finalisé avec décision et preuve après la session."),
        ("Checkpoint", "Tu dois pouvoir autoriser ou refuser un trade avec les mêmes critères avant et après le résultat."),
    ],
    "14-live-chart.html": [
        ("Objectif", "Transférer la grille du cours vers un graphique réel sans bénéficier du recul."),
        ("À produire", "Une capture annotée avec contexte, liquidité, scénario, invalidation, DOL et décision horodatée."),
        ("Checkpoint", "Tu dois lire un graphique non préparé et distinguer observation, hypothèse et confirmation."),
    ],
    "10-programme-avance.html": [
        ("Objectif", "Organiser l’apprentissage en cycles de lecture, replay, journal et correction mesurable."),
        ("À produire", "Un calendrier de travail avec un modèle unique, un échantillon cible et une revue planifiée."),
        ("Checkpoint", "Tu dois terminer un cycle sans changer de règles en cours d’échantillon et présenter les preuves collectées."),
    ],
    "08-quiz.html": [
        ("Objectif", "Tester la compréhension des décisions plutôt que la mémorisation des sigles."),
        ("À produire", "Un journal d’erreurs classé par contexte, liquidité, confirmation, risque et cible."),
        ("Checkpoint", "Tu dois expliquer chaque correction avec une règle du cours sans relire immédiatement la réponse."),
    ],
    "13-prop-firm.html": [
        ("Objectif", "Adapter le plan aux limites d’une prop firm sans dégrader le modèle ni augmenter la fréquence."),
        ("À produire", "Une fiche de règles traduite en risque par trade, perte quotidienne, drawdown maximal et conditions d’arrêt."),
        ("Checkpoint", "Tu dois calculer le nombre maximal d’essais permis et arrêter la session avant la violation d’une limite."),
    ],
    "09-synthese.html": [
        ("Objectif", "Assembler contexte, setup, risque, exécution et preuve dans une méthode personnelle cohérente."),
        ("À produire", "Un plan d’une page qui définit ce que tu trades, ce que tu refuses et ce que tu mesures."),
        ("Checkpoint", "Tu dois présenter un scénario complet de la préparation à la review sans ajouter une règle après le résultat."),
    ],
    "15-index-concepts.html": [
        ("Objectif", "Retrouver rapidement la définition, la leçon source et l’usage pratique de chaque concept."),
        ("À produire", "Une carte personnelle reliant les concepts utilisés dans ton modèle aux chapitres de référence."),
        ("Checkpoint", "Tu dois retrouver en moins d’une minute la source et la checklist d’un terme rencontré en replay."),
    ],
}

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


def course_href(filename, target):
    if filename == "index.html":
        return "index.html" if target == "index.html" else f"pages/{target}"
    return "../index.html" if target == "index.html" else target


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

    resources_link = soup.new_tag(
        "a",
        href=course_href(filename, "ressources-pratiques.html"),
        **{"class": "resources-nav-link"},
    )
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
            a = soup.new_tag("a", href=course_href(filename, href))
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
    for old_script in soup.find_all(
        "script",
        src=lambda value: value and value.endswith("glossary-panel.js"),
    ):
        old_script.decompose()
    if soup.body:
        fab = soup.new_tag("button", type="button", **{"class": "glossary-fab", "aria-label": "Ouvrir le glossaire ICT"})
        fab["data-glossary-open"] = ""
        fab.string = "Glossaire"
        soup.body.append(fab)
        soup.body.append(build_glossary_panel(soup, filename))
        script_src = "js/glossary-panel.js" if filename == "index.html" else "../js/glossary-panel.js"
        script = soup.new_tag("script", src=script_src, defer=True)
        soup.body.append(script)


def build_glossary_panel(soup, filename):
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
    loading = tag(soup, "p", "Le glossaire sera chargé à sa première ouverture.", **{"class": "glossary-loading"})
    loading["data-glossary-loading"] = ""
    list_wrap.append(loading)
    panel.append(list_wrap)

    full = soup.new_tag(
        "a",
        href=course_href(filename, "glossaire.html"),
        **{"class": "glossary-full-link"},
    )
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
        prev = soup.new_tag(
            "a",
            href=course_href(filename, previous_lesson["href"]),
            **{"class": "pager-link"},
        )
        prev.append(tag(soup, "small", "Précédent"))
        prev.append(tag(soup, "span", previous_lesson["title"]))
        pager.append(prev)
    else:
        pager.append(tag(soup, "span", "Début du cours", **{"class": "pager-link disabled"}))
    if next_lesson:
        nxt = soup.new_tag(
            "a",
            href=course_href(filename, next_lesson["href"]),
            **{"class": "pager-link next"},
        )
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
        prev = soup.new_tag(
            "a",
            href=course_href(filename, previous_lesson["href"]),
            **{"class": "bottom-link"},
        )
        prev.append(tag(soup, "small", "Revoir"))
        prev.append(tag(soup, "span", previous_lesson["title"]))
        bottom.append(prev)
    if next_lesson:
        nxt = soup.new_tag(
            "a",
            href=course_href(filename, next_lesson["href"]),
            **{"class": "bottom-link next"},
        )
        nxt.append(tag(soup, "small", "Continuer"))
        nxt.append(tag(soup, "span", next_lesson["title"]))
        bottom.append(nxt)
    else:
        practice = soup.new_tag(
            "a",
            href=course_href(filename, "tableau-progression.html"),
            **{"class": "bottom-link next", "data-course-completion-next": ""},
        )
        practice.append(tag(soup, "small", "Passer à la pratique"))
        practice.append(tag(soup, "span", "Ouvrir le tableau de progression"))
        bottom.append(practice)
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
    paths = [ROOT / "index.html", *sorted((ROOT / "pages").glob("*.html"))]
    for path in paths:
        if path.name not in LESSON_BY_FILE:
            continue
        soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
        rebuild_course_nav(soup, path.name)
        insert_lesson_header(soup, path.name)
        add_lesson_intro(soup, path.name)
        path.write_text(str(soup), encoding="utf-8")


if __name__ == "__main__":
    main()
