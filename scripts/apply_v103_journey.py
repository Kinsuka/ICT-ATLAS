#!/usr/bin/env python3
"""Apply the V103 end-to-end journey corrections idempotently."""

from pathlib import Path

from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parents[1]


PRACTICE_STEPS = [
    ("tableau-progression.html", "Tableau de progression", "Prochaine action"),
    ("replay-cases.html#pack-six-cas", "Cas et simulateurs", "Apprendre"),
    ("examen-decision-session.html", "Examen de décision", "10/12 minimum"),
    ("examen-dol-tp.html", "Examen DOL / TP", "16/18 minimum"),
    ("replay-historique.html", "Replay historique", "12/16 minimum"),
    ("programme-validation-20-sessions.html", "20 sessions replay", "Valider"),
]


def fragment(html):
    return BeautifulSoup(html, "html.parser").find()


def write(path, soup):
    path.write_text(str(soup), encoding="utf-8")


def update_home():
    path = ROOT / "index.html"
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    root = soup.select_one("[data-training-roadmap]")

    next_link = root.select_one("[data-roadmap-next-link]")
    next_link["href"] = "pages/16-modele-mental.html"
    root.select_one("[data-roadmap-next-title]").string = "Commencer par le modèle mental"
    root.select_one("[data-roadmap-next-detail]").string = (
        "Première visite : suis ensuite les boutons Continuer jusqu’à la leçon 41."
    )

    rails = root.select(".roadmap-two-rails article")
    rails[1].find("h3").string = "Huit portes observables"

    stages = root.select_one(".roadmap-stages")
    stages["aria-label"] = "Huit portes du parcours pratique"
    for node in stages.select('[data-v103-stage="true"]'):
        node.decompose()

    exam = stages.select_one('[data-roadmap-stage="exam"]')
    target = fragment(
        '<li data-roadmap-stage="target" data-v103-stage="true"><a href="pages/examen-dol-tp.html">'
        '<span class="roadmap-stage-number">05</span><div><small>CALCULER</small>'
        '<h3>Examen DOL / TP</h3><p>Six scénarios et dix-huit décisions sur les targets, le stop et le R restant.</p>'
        '<strong>PASSAGE · 16/18 minimum avant le transfert aux données historiques.</strong></div>'
        '<em data-roadmap-target-status>NON TENTÉ</em></a></li>'
    )
    historical = fragment(
        '<li data-roadmap-stage="historical" data-v103-stage="true"><a href="pages/replay-historique.html">'
        '<span class="roadmap-stage-number">06</span><div><small>TRANSFÉRER</small>'
        '<h3>Quatre gels historiques</h3><p>Décisions prises sur données Coinbase avec le futur masqué.</p>'
        '<strong>PASSAGE · Quatre cas corrigés et 12/16 minimum.</strong></div>'
        '<em data-roadmap-historical-status>0 / 4 · 0 / 16</em></a></li>'
    )
    exam.insert_after(target)
    target.insert_after(historical)

    validation = stages.select_one('[data-roadmap-stage="validation"]')
    validation.select_one(".roadmap-stage-number").string = "07"
    forward = stages.select_one('[data-roadmap-stage="forward"]')
    forward.select_one(".roadmap-stage-number").string = "08"
    write(path, soup)


def replace_practice_nav(soup, active_href):
    nav = soup.select_one("aside.site-nav ol.course-lessons")
    if not nav:
        return
    nav.clear()
    for index, (href, title, detail) in enumerate(PRACTICE_STEPS, 1):
        active = href.split("#", 1)[0] == active_href
        item = fragment(
            f'<li class="course-lesson{" active" if active else ""}"><a href="{href}">'
            f'<span class="lesson-bullet">{index}</span><span class="lesson-link-text">'
            f'<strong>{title}</strong><small>{detail}</small></span></a></li>'
        )
        nav.append(item)


def replace_bottom_nav(soup, previous_href, previous_title, next_href, next_title, next_kicker="Continuer"):
    main = soup.select_one("main.page")
    old = main.select_one("nav.lesson-bottom-nav")
    new = fragment(
        '<nav aria-label="Navigation finale" class="lesson-bottom-nav">'
        f'<a class="bottom-link" href="{previous_href}"><small>Revoir</small><span>{previous_title}</span></a>'
        f'<a class="bottom-link next" href="{next_href}"><small>{next_kicker}</small><span>{next_title}</span></a>'
        '</nav>'
    )
    if old:
        old.replace_with(new)
    else:
        main.append(new)


def update_support_pages():
    routes = {
        "replay-cases.html": (
            "20-workflow-session.html#v92-session-cockpit",
            "Cockpit de session",
            "examen-decision-session.html",
            "Passer l’examen de décision",
        ),
        "examen-decision-session.html": (
            "replay-cases.html#simulateur-session",
            "Cas et simulateurs",
            "examen-dol-tp.html",
            "Passer l’examen DOL / TP",
        ),
        "examen-dol-tp.html": (
            "examen-decision-session.html",
            "Examen de décision",
            "replay-historique.html",
            "Résoudre les gels historiques",
        ),
        "replay-historique.html": (
            "examen-dol-tp.html",
            "Examen DOL / TP",
            "programme-validation-20-sessions.html",
            "Commencer les 20 sessions replay",
        ),
        "programme-validation-20-sessions.html": (
            "replay-historique.html",
            "Replay historique",
            "tableau-progression.html",
            "Voir toutes les preuves",
        ),
    }

    for filename, route in routes.items():
        path = ROOT / "pages" / filename
        soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
        replace_practice_nav(soup, filename)
        replace_bottom_nav(soup, *route, next_kicker="Étape suivante" if filename != "programme-validation-20-sessions.html" else "Retour au tableau")

        if filename == "examen-decision-session.html":
            after_exam = next(
                (section for section in soup.select("section.card") if section.find("h2") and section.find("h2").get_text(strip=True) == "Après l’examen"),
                None,
            )
            if after_exam:
                after_exam.find("header").find("span").string = "Deuxième preuve"
                after_exam.find("p").string = (
                    "Le score identifie tes points faibles. Valide maintenant la hiérarchie des DOL, "
                    "des targets et du R restant avant de travailler sur les données historiques."
                )
                link = after_exam.select_one("a.section-link")
                link["href"] = "examen-dol-tp.html"
                link.find("h3").string = "Passer l’examen DOL / TP"
                link.find("p").string = "Six scénarios, dix-huit décisions et un seuil explicite de 16/18."

        write(path, soup)


def update_course_completion():
    path = ROOT / "pages" / "15-index-concepts.html"
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    for node in soup.select(".course-completion-gateway"):
        node.decompose()
    gateway = fragment(
        '<section class="course-completion-gateway" id="fin-du-cours">'
        '<small>COURS TERMINÉ · 41 / 41</small>'
        '<h2>Tu as terminé la carte. Produis maintenant une preuve.</h2>'
        '<p>La lecture construit le langage ; elle ne valide pas encore la décision. Le tableau de progression '
        'ouvre une route unique jusqu’aux vingt sessions replay, sans risque réel.</p>'
        '<div class="course-completion-steps">'
        '<article><span>01 · PRÉPARER</span><strong>Cockpit, cas guidés et simulateurs</strong></article>'
        '<article><span>02 · MESURER</span><strong>Deux examens puis quatre gels historiques</strong></article>'
        '<article><span>03 · RÉPÉTER</span><strong>Vingt sessions et preuves conservées</strong></article>'
        '</div><div class="course-completion-actions">'
        '<a href="tableau-progression.html">Ouvrir ma prochaine action →</a>'
        '<a href="replay-cases.html#pack-six-cas">Voir les cas guidés</a>'
        '</div></section>'
    )
    bottom = soup.select_one("nav.lesson-bottom-nav")
    bottom.insert_before(gateway)
    write(path, soup)


def main():
    update_home()
    update_support_pages()
    update_course_completion()
    print("V103 journey corrections applied.")


if __name__ == "__main__":
    main()
