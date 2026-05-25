from pathlib import Path
from bs4 import BeautifulSoup


BRIDGES = {
    "16-modele-mental.html": (
        "bridge-modele-debutant",
        "À ce stade, lis cette page comme une carte générale.",
        "Les noms techniques servent seulement de repères. Tu n’as pas besoin de maîtriser FVG, OB, MSS, OTE ou DOL maintenant : retiens d’abord que le prix cherche souvent une zone de liquidité, réagit, puis laisse parfois une zone de retour avant de viser une autre zone.",
    ),
    "11-mecanique-marches.html": (
        "bridge-mecanique-debutant",
        "Pourquoi cette leçon arrive avant les setups ?",
        "Avant de reconnaître une figure ICT, il faut comprendre ce qui peut pousser le prix : des ordres, des stops, des prises de profit, des acteurs qui doivent exécuter sans tout montrer. Les schémas viendront après ; ici, on installe la cause.",
    ),
    "21-liquidite-deplacement.html": (
        "bridge-liquidite-debutant",
        "Point de vigilance débutant",
        "Ne traduis pas encore chaque prise de liquidité en signal d’entrée. Dans cette leçon, la question est plus simple : après avoir pris une zone évidente, le prix accepte-t-il de continuer, ou rejette-t-il violemment cette prise ?",
    ),
    "22-structure-trend-range.html": (
        "bridge-structure-debutant",
        "Pourquoi parler de trend et range maintenant ?",
        "Parce que le même setup n’a pas la même valeur partout. Un FVG dans une tendance propre peut être un pullback logique ; le même FVG au milieu d’une range équilibrée peut n’être qu’un bruit de plus.",
    ),
    "17-concept-setup-plan.html": (
        "bridge-concept-plan-debutant",
        "La charnière du cours",
        "À partir d’ici, tu vas voir beaucoup de formes. Pour ne pas te perdre, sépare toujours trois niveaux : un concept décrit quelque chose, un setup combine plusieurs conditions, un plan autorise ou refuse une entrée avec un risque défini.",
    ),
    "03-fondations.html": (
        "bridge-fondations-debutant",
        "Comment lire cette page dense",
        "Cette leçon ne rajoute pas des setups : elle apprend à décider. Si un mot technique bloque, ouvre le glossaire, puis reviens à la question centrale : le contexte autorise-t-il vraiment ce trade ?",
    ),
    "04-setups-core.html": (
        "bridge-setups-debutant",
        "Avant de mémoriser les setups",
        "Lis les setups comme des histoires en plusieurs étapes, pas comme des formes à copier. L’ordre reste toujours : environnement, liquidité, déplacement, zone de retour, invalidation, cible.",
    ),
    "18-transition-reel.html": (
        "bridge-reel-debutant",
        "Ce qui change avec le graphique réel",
        "Les exemples propres servent à apprendre la logique. Le réel ajoute du bruit, des zones concurrentes et des signaux partiels. Le but de cette leçon est d’apprendre à ralentir, pas à prendre plus d’entrées.",
    ),
    "05-variantes.html": (
        "bridge-variantes-debutant",
        "Une variante n’est pas une permission",
        "Cette page existe pour apprendre le tri. Certains exemples ressemblent à des setups, mais il leur manque une condition centrale : contexte, déplacement, acceptation, cible ou risque.",
    ),
    "07-failures-journees.html": (
        "bridge-failures-debutant",
        "Perte valide ou erreur ?",
        "Cette distinction protège ton apprentissage. Une perte conforme au plan est une donnée ; une entrée sans condition complète est une erreur. Les deux ne doivent pas être corrigées de la même manière.",
    ),
    "19-preuve-statistique.html": (
        "bridge-edge-debutant",
        "Pourquoi la preuve arrive après les setups",
        "On ne teste pas une impression vague. On teste une hypothèse précise : mêmes conditions, même contexte, même invalidation, mêmes données notées. C’est seulement là qu’un pattern peut devenir un edge.",
    ),
}

TEXT_REPLACEMENTS = {
    "Un FVG, un OB ou un MSS ne sont pas des signaux isolés. Ils doivent etre relus dans cette séquence : pourquoi ici, pourquoi maintenant, vers quelle cible ?":
        "Les sigles ICT que tu verras plus tard ne sont pas des signaux isolés. Ils devront toujours être relus dans cette séquence : pourquoi ici, pourquoi maintenant, vers quelle cible ?",
    "FVG, OB, breaker ou OTE deviennent des zones candidates seulement si elles viennent du déplacement pertinent.":
        "Une zone de retour devient candidate seulement si elle vient d’un déplacement pertinent. Les noms techniques de ces zones seront détaillés plus loin.",
    "Highs, lows, PDH, PDL, Asia High/Low ou zones evidentes concentrent souvent stops, prises de profit et ordres breakout.":
        "Les anciens plus hauts, anciens plus bas et zones visibles concentrent souvent stops, prises de profit et ordres breakout. Le glossaire détaille les sigles associés.",
    "Range, premium/discount, kill zone, proximite du DOL et contexte higher timeframe.":
        "Sommes-nous en tendance, en range ou près d’une zone importante ? Le vocabulaire précis viendra ensuite, mais la question reste : où sommes-nous ?",
    "SSL, BSL, high/low de session, ancien niveau journalier ou zone interne.":
        "Un ancien plus haut, un ancien plus bas, un niveau de session ou une zone interne. Le nom exact compte moins que l’idée : quelle liquidité vient d’être touchée ?",
    "Displacement, MSS, FVG/OB exploitable, invalidation claire et risque acceptable.":
        "Une réaction forte, un changement de contrôle, une zone exploitable, une invalidation claire et un risque acceptable.",
    "Un concept nomme un phenomene : FVG, sweep, MSS, OB, OTE, premium, discount, DOL. Il aide a lire, mais ne donne pas encore une entrée.":
        "Un concept nomme un phénomène visible : prise de liquidité, déséquilibre, changement de structure, zone de retour, cible. Il aide à lire, mais ne donne pas encore une entrée.",
}


def make_note(soup, item_id, title, body):
    section = soup.new_tag("section", id=item_id, **{"class": "page-note beginner-bridge"})
    section.append(soup.new_tag("strong"))
    section.strong.string = title
    section.append(" " + body)
    return section


def insert_bridge(path, item_id, title, body):
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    old = soup.find(id=item_id)
    if old:
        old.decompose()
    main = soup.find("main", class_="page")
    if not main:
        return
    note = make_note(soup, item_id, title, body)
    anchor = main.find("div", class_="page-meta-dashboard") or main.find("section", class_="lesson-objectives")
    if anchor:
        anchor.insert_after(note)
    else:
        main.insert(0, note)
    path.write_text(str(soup), encoding="utf-8")


def apply_text_replacements(path):
    text = path.read_text(encoding="utf-8")
    for old, new in TEXT_REPLACEMENTS.items():
        text = text.replace(old, new)
    path.write_text(text, encoding="utf-8")


def main():
    for filename, bridge in BRIDGES.items():
        path = Path(filename)
        if not path.exists():
            continue
        apply_text_replacements(path)
        insert_bridge(path, *bridge)


if __name__ == "__main__":
    main()
