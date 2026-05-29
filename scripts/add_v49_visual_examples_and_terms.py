from pathlib import Path
import re
from bs4 import BeautifulSoup, NavigableString


SKIP_FILES = {"02-vocabulaire.html", "glossaire.html"}
TERMS = [
    ("Premium/Discount", "Premium / Discount"),
    ("Premium / Discount", "Premium / Discount"),
    ("failed breakout", "Failed breakout"),
    ("Kill Zones", "Kill Zone"),
    ("Kill Zone", "Kill Zone"),
    ("Displacement", "Displacement"),
    ("displacement", "Displacement"),
    ("Liquidité", "Liquidité"),
    ("liquidité", "Liquidité"),
    ("liquidite", "Liquidité"),
    ("Sweep", "Sweep / Raid"),
    ("sweep", "Sweep / Raid"),
    ("Raid", "Sweep / Raid"),
    ("raid", "Sweep / Raid"),
    ("FVG", "FVG"),
    ("MSS", "MSS"),
    ("DOL", "DOL"),
    ("OB", "OB"),
    ("OTE", "OTE"),
    ("CE", "CE"),
    ("BSL", "BSL / SSL"),
    ("SSL", "BSL / SSL"),
    ("PDH", "PDH / PDL"),
    ("PDL", "PDH / PDL"),
    ("Breaker", "Breaker"),
    ("breaker", "Breaker"),
    ("Edge", "Edge"),
    ("edge", "Edge"),
    ("Trend", "Trend"),
    ("trend", "Trend"),
    ("Range", "Range"),
    ("range", "Range"),
    ("Transition", "Transition"),
    ("transition", "Transition"),
    ("Pullback", "Pullback"),
    ("pullback", "Pullback"),
]


def svg_three_paths(title, labels):
    colors = ["#26a69a", "#4fc3f7", "#ef5350"]
    paths = [
        "120,270 190,210 260,232 330,150 405,182 480,108 560,132 640,82 760,104",
        "120,190 190,132 260,168 330,112 405,156 480,122 560,168 640,120 760,154",
        "120,118 190,168 260,138 330,200 405,172 480,238 560,212 640,278 760,250",
    ]
    label_svg = ""
    for index, label in enumerate(labels):
        y = 54 + index * 28
        label_svg += f'<circle cx="86" cy="{y-4}" r="5" fill="{colors[index]}"/><text x="102" y="{y}" fill="#d9e6f2" font-size="12" font-weight="800">{label}</text>'
    lines = "".join(
        f'<polyline points="{paths[i]}" fill="none" stroke="{colors[i]}" stroke-width="2.4" opacity=".95"/>'
        for i in range(3)
    )
    return f"""<div class="chart"><svg width="100%" height="auto" viewBox="0 0 900 340" xmlns="http://www.w3.org/2000/svg"><rect width="900" height="340" fill="#081222"/><g opacity=".55"><line x1="90" x2="810" y1="80" y2="80" stroke="#1e3a5f"/><line x1="90" x2="810" y1="150" y2="150" stroke="#1e3a5f"/><line x1="90" x2="810" y1="220" y2="220" stroke="#1e3a5f"/><line x1="90" x2="810" y1="290" y2="290" stroke="#1e3a5f"/></g><text x="450" y="36" text-anchor="middle" fill="#8ee5fa" font-size="18" font-weight="900">{title}</text>{label_svg}{lines}</svg></div>"""


VISUAL_SECTIONS = {
    "index.html": """<section class="card" id="v49-carte-parcours-visuelle"><header><h2>Carte visuelle du parcours complet</h2><span>Vue d’ensemble</span></header>{svg}<div class="academy-grid"><div class="academy-card"><h3>Comprendre</h3><p>Modèle mental, mécanique, langage, liquidité et structure.</p></div><div class="academy-card"><h3>Filtrer</h3><p>Où, quand, top-down, environnement et setup.</p></div><div class="academy-card"><h3>Tester</h3><p>Risque, edge statistique, failures et variantes.</p></div><div class="academy-card"><h3>Exécuter</h3><p>Psychologie, workflow live, prop firm et synthèse.</p></div></div></section>""".format(svg=svg_three_paths("Comprendre -> Filtrer -> Tester -> Exécuter", ["Base", "Filtre", "Execution"])),
    "01-parcours.html": """<section class="card" id="v49-parcours-repetitions-visuelles"><header><h2>Comment répéter sans se perdre</h2><span>Méthode visuelle</span></header>{svg}<div class="academy-grid"><div class="academy-card"><h3>Lecture</h3><p>Tu lis la leçon et tu notes les mots qui bloquent.</p></div><div class="academy-card"><h3>Capture</h3><p>Tu cherches deux ou trois exemples visuels du même cas.</p></div><div class="academy-card"><h3>Journal</h3><p>Tu écris ce qui valide, invalide ou transforme l’exemple en no trade.</p></div></div></section>""".format(svg=svg_three_paths("Lire -> Capturer -> Journaliser", ["Lecture", "Exemples", "Journal"])),
    "16-modele-mental.html": """<section class="card" id="v49-exemples-cycle-modele"><header><h2>Trois lectures du même modèle mental</h2><span>Exemples visuels</span></header>{svg}<div class="academy-grid"><div class="academy-card"><h3>Continuation</h3><p>Le prix prend une liquidité, livre fort, corrige proprement puis continue vers la prochaine cible.</p></div><div class="academy-card"><h3>Reversal</h3><p>Le prix prend une liquidité, rejette, casse la structure interne puis revient sur une zone de retour.</p></div><div class="academy-card"><h3>No trade</h3><p>La prise existe, mais la réaction est molle ou contradictoire. On observe au lieu de forcer une lecture.</p></div></div></section>""".format(svg=svg_three_paths("Même logique, trois issues possibles", ["Continuation", "Reversal", "No trade"])),
    "17-concept-setup-plan.html": """<section class="card" id="v49-fvg-trois-niveaux-visuel"><header><h2>Un même FVG lu à trois niveaux</h2><span>Exemples visuels</span></header>{svg}<div class="chart"><table class="référence-table"><tr><th>Niveau</th><th>Ce que tu vois</th><th>Ce qui manque encore</th></tr><tr><td>Concept</td><td>Une zone de déséquilibre existe.</td><td>Contexte, cible, invalidation.</td></tr><tr><td>Setup</td><td>La zone suit une prise de liquidité et un déplacement.</td><td>Entrée, stop, risque, timing.</td></tr><tr><td>Plan</td><td>La zone est tradable avec cible, stop et scénario d’annulation.</td><td>Rien : on exécute ou on refuse.</td></tr></table></div></section>""".format(svg=svg_three_paths("Concept -> Setup -> Plan", ["Concept seul", "Setup possible", "Plan complet"])),
    "18-transition-reel.html": """<section class="card" id="v49-propre-reel-quatre-cas"><header><h2>Du propre au réel : plusieurs versions du même signal</h2><span>Exemples visuels</span></header>{svg}<div class="academy-grid"><div class="academy-card"><h3>Cas A</h3><p>Signal propre : contexte aligné, déplacement net, retour lisible.</p></div><div class="academy-card"><h3>Cas B</h3><p>Signal exploitable mais moins clair : taille réduite ou exigence de confirmation plus forte.</p></div><div class="academy-card"><h3>Cas C</h3><p>Signal ambigu : plusieurs zones concurrentes, donc observation.</p></div></div></section>""".format(svg=svg_three_paths("Même idée, qualité différente", ["A propre", "B moyen", "C refusé"])),
    "20-workflow-session.html": """<section class="card" id="v49-workflow-scenarios-session"><header><h2>Trois scénarios de session avant de cliquer</h2><span>Exemples visuels</span></header>{svg}<div class="academy-grid"><div class="academy-card"><h3>Plan A</h3><p>Le marché prend la liquidité attendue pendant la kill zone et confirme : tu peux chercher le setup.</p></div><div class="academy-card"><h3>Plan B</h3><p>Le niveau est atteint trop tôt ou sans réaction : tu attends une nouvelle structure.</p></div><div class="academy-card"><h3>Plan C</h3><p>News, range sale ou DOL déjà atteint : session d’observation.</p></div></div></section>""".format(svg=svg_three_paths("Préparer plusieurs issues", ["Plan A", "Plan B", "No trade"])),
    "11-mecanique-marches.html": """<section class="card" id="v49-mecanique-trois-mouvements"><header><h2>Trois mouvements mécaniques à reconnaître</h2><span>Exemples visuels</span></header>{svg}<div class="academy-grid"><div class="academy-card"><h3>Run</h3><p>La cassure est acceptée : le prix continue car les ordres agressifs dominent.</p></div><div class="academy-card"><h3>Sweep rejeté</h3><p>La liquidité est prise, mais le marché réintègre vite : absorption possible.</p></div><div class="academy-card"><h3>Compression</h3><p>Le prix accumule près d’un niveau : l’expansion peut venir après.</p></div></div></section>""".format(svg=svg_three_paths("Run, rejet, compression", ["Run", "Sweep rejeté", "Compression"])),
    "12-gestion-risque.html": """<section class="card" id="v49-risque-series-visuel"><header><h2>Visualiser une série de trades en R</h2><span>Exemples visuels</span></header>{svg}<div class="academy-grid"><div class="academy-card"><h3>Série normale</h3><p>Une stratégie peut perdre plusieurs fois et rester valide si le risque est contrôlé.</p></div><div class="academy-card"><h3>Série dangereuse</h3><p>Le problème commence quand la taille augmente après une perte.</p></div><div class="academy-card"><h3>Série saine</h3><p>Le trader garde la même unité de risque et laisse l’échantillon parler.</p></div></div></section>""".format(svg=svg_three_paths("Equity en R : trois comportements", ["Risque fixe", "Over-risk", "Réduction"])),
    "13-prop-firm.html": """<section class="card" id="v49-prop-drawdown-visuel"><header><h2>Trois journées prop firm : survivre d’abord</h2><span>Exemples visuels</span></header>{svg}<div class="academy-grid"><div class="academy-card"><h3>Journée propre</h3><p>Un trade ou deux, risque respecté, arrêt après objectif ou perte limite.</p></div><div class="academy-card"><h3>Journée de tilt</h3><p>Les pertes déclenchent une hausse de taille. C’est le chemin le plus court vers l’échec.</p></div><div class="academy-card"><h3>Journée sauvée</h3><p>Deux pertes, arrêt immédiat, capital mental préservé pour demain.</p></div></div></section>""".format(svg=svg_three_paths("Drawdown : propre, tilt, stop", ["Propre", "Tilt", "Stop journée"])),
    "14-live-chart.html": """<section class="card" id="v49-live-chart-decoupage"><header><h2>Découper un graphique live en zones lisibles</h2><span>Exemples visuels</span></header>{svg}<div class="academy-grid"><div class="academy-card"><h3>Zone HTF</h3><p>La grande structure donne le sens et les niveaux importants.</p></div><div class="academy-card"><h3>Zone setup</h3><p>Le timeframe intermédiaire confirme ou refuse l’idée.</p></div><div class="academy-card"><h3>Zone entrée</h3><p>Le petit timeframe sert seulement à préciser le risque.</p></div></div></section>""".format(svg=svg_three_paths("HTF -> Setup -> Entrée", ["HTF", "Setup", "Entrée"])),
    "15-index-concepts.html": """<section class="card" id="v49-index-carte-concepts"><header><h2>Carte des familles de concepts</h2><span>Index visuel</span></header>{svg}<div class="academy-grid"><div class="academy-card"><h3>Structure</h3><p>Trend, range, transition, top-down.</p></div><div class="academy-card"><h3>Liquidité</h3><p>BSL, SSL, PDH, PDL, DOL, sweep.</p></div><div class="academy-card"><h3>Exécution</h3><p>FVG, OB, CE, OTE, stop, target, invalidation.</p></div></div></section>""".format(svg=svg_three_paths("Structure -> Liquidité -> Exécution", ["Structure", "Liquidité", "Exécution"])),
    "10-programme-avance.html": """<section class="card" id="v49-programme-cycle-pratique"><header><h2>Cycle hebdomadaire de progression</h2><span>Programme visuel</span></header>{svg}<div class="academy-grid"><div class="academy-card"><h3>Backtest</h3><p>Tu construis l’échantillon sans chercher à avoir raison.</p></div><div class="academy-card"><h3>Replay</h3><p>Tu répètes les décisions dans l’ordre réel du marché.</p></div><div class="academy-card"><h3>Live réduit</h3><p>Tu passes au réel seulement avec taille contrôlée et protocole.</p></div></div></section>""".format(svg=svg_three_paths("Backtest -> Replay -> Live réduit", ["Backtest", "Replay", "Live"])),
    "23-langage-ict-contexte.html": """<section class="card" id="v49-langage-mini-cas"><header><h2>Mini-cas : le même mot dans trois contextes</h2><span>Exemples visuels</span></header>{svg}<div class="academy-grid"><div class="academy-card"><h3>FVG utile</h3><p>Il vient après une prise de liquidité et un déplacement clair.</p></div><div class="academy-card"><h3>FVG faible</h3><p>Il apparaît au milieu d’une range sans cible évidente.</p></div><div class="academy-card"><h3>FVG piège</h3><p>Il est propre visuellement mais contre la structure supérieure.</p></div></div></section>""".format(svg=svg_three_paths("Un terme, trois qualités", ["Utile", "Faible", "Piège"])),
    "24-premium-discount-killzones.html": """<section class="card" id="v49-where-when-combinaisons"><header><h2>Plusieurs combinaisons WHERE / WHEN</h2><span>Exemples visuels</span></header>{svg}<div class="chart"><table class="référence-table"><tr><th>Cas</th><th>Où ?</th><th>Quand ?</th><th>Lecture</th></tr><tr><td>A</td><td>Discount</td><td>NY AM</td><td class="ok">Long possible si contexte aligné.</td></tr><tr><td>B</td><td>Premium</td><td>London</td><td class="ok">Short possible si structure confirme.</td></tr><tr><td>C</td><td>Milieu de range</td><td>Hors kill zone</td><td class="bad">No trade pour débutant.</td></tr></table></div></section>""".format(svg=svg_three_paths("Bon endroit, bon moment", ["Long logique", "Short logique", "No trade"])),
    "25-top-down-multi-timeframe.html": """<section class="card" id="v49-topdown-conflits-visuels"><header><h2>Trois conflits multi-timeframe fréquents</h2><span>Exemples visuels</span></header>{svg}<div class="academy-grid"><div class="academy-card"><h3>5M beau, Daily opposé</h3><p>Le signal est refusé ou réduit à une observation.</p></div><div class="academy-card"><h3>4H en range</h3><p>Le 5M ne doit pas être lu comme une grande tendance.</p></div><div class="academy-card"><h3>Daily aligné</h3><p>Le petit timeframe devient un outil d’exécution, pas une source de biais.</p></div></div></section>""".format(svg=svg_three_paths("Conflits de timeframes", ["Conflit", "Range HTF", "Aligné"])),
    "26-psychologie-trader.html": """<section class="card" id="v49-mental-reactions-visuelles"><header><h2>Trois réactions possibles après une perte</h2><span>Exemples visuels</span></header>{svg}<div class="academy-grid"><div class="academy-card"><h3>Revenge</h3><p>Tu augmentes la taille pour récupérer. C’est une rupture de protocole.</p></div><div class="academy-card"><h3>Paralysie</h3><p>Tu refuses le prochain setup valide par peur. C’est aussi une réaction émotionnelle.</p></div><div class="academy-card"><h3>Protocole</h3><p>Tu classes la perte, tu pauses, puis tu reprends seulement si les conditions reviennent.</p></div></div></section>""".format(svg=svg_three_paths("Après perte : trois chemins", ["Revenge", "Peur", "Protocole"])),
}


def insert_visual_sections():
    for filename, html in VISUAL_SECTIONS.items():
        path = Path(filename)
        if not path.exists():
            continue
        soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
        fragment = BeautifulSoup(html, "html.parser").section
        old = soup.find(id=fragment.get("id"))
        if old:
            old.decompose()
        main = soup.find("main", class_="page")
        if not main:
            continue
        bottom = main.find("nav", class_="lesson-bottom-nav")
        if bottom:
            bottom.insert_before(fragment)
        else:
            main.append(fragment)
        path.write_text(str(soup), encoding="utf-8")


def can_replace(node):
    parent = node.parent
    while parent is not None:
        if parent.name in {"script", "style", "svg", "button", "a", "code", "pre"}:
            return False
        classes = parent.get("class", []) if hasattr(parent, "get") else []
        if any(name in classes for name in ["site-nav", "glossary-panel-shell", "lesson-header"]):
            return False
        parent = parent.parent
    return True


def annotate_terms():
    term_patterns = [(raw, target, re.compile(rf"(?<![\w/]){re.escape(raw)}(?![\w/])")) for raw, target in TERMS]
    for path in sorted(Path(".").glob("*.html")):
        if path.name in SKIP_FILES:
            continue
        soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
        used = {button.get("data-glossary-term") for button in soup.select("[data-glossary-term]")}
        for text_node in list(soup.find_all(string=True)):
            if not isinstance(text_node, NavigableString) or not can_replace(text_node):
                continue
            text = str(text_node)
            match_info = None
            for raw, target, pattern in term_patterns:
                if target in used:
                    continue
                match = pattern.search(text)
                if match and (match_info is None or match.start() < match_info[2].start()):
                    match_info = (raw, target, match)
            if not match_info:
                continue
            _, target, match = match_info
            before, term, after = text[: match.start()], text[match.start() : match.end()], text[match.end() :]
            button_html = f'<button class="glossary-term" type="button" data-glossary-term="{target}">{term}</button>'
            nodes = BeautifulSoup(before + button_html + after, "html.parser")
            text_node.replace_with(*nodes.contents)
            used.add(target)
        path.write_text(str(soup), encoding="utf-8")


def main():
    insert_visual_sections()
    annotate_terms()


if __name__ == "__main__":
    main()
