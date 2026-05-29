from pathlib import Path
from bs4 import BeautifulSoup


def page(title, subtitle, tags, meta_goal, meta_prereq, sections):
    tag_html = "".join(f"<span>{tag}</span>" for tag in tags)
    sections_html = "\n".join(sections)
    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width,initial-scale=1" name="viewport"/>
<title>ICT Atlas - {title}</title>
<link href="style.css" rel="stylesheet"/>
</head>
<body>
<div class="app-shell">
<aside aria-label="Navigation principale" class="site-nav"></aside>
<main class="page" id="contenu">
<div class="hero">
<h1>ICT Atlas - {title}</h1>
<p>{subtitle}</p>
<div class="tagline">{tag_html}</div>
</div>
<div class="page-meta-dashboard">
<div class="meta-main">
<div class="meta-goal"><strong>Objectif</strong>{meta_goal}</div>
<div class="meta-prereq"><strong>Prérequis</strong>{meta_prereq}</div>
</div>
<div class="meta-sidebar">
<strong>À lire avec</strong>
<nav class="pill-nav">
<a class="pill" href="glossaire.html">Glossaire</a>
<a class="pill" href="15-index-concepts.html">Index</a>
<a class="pill" href="21-liquidite-deplacement.html">Liquidité</a>
</nav>
</div>
</div>
{sections_html}
</main>
</div>
</body>
</html>
"""


LANGAGE = page(
    "Le langage ICT en contexte",
    "Apprendre les sigles essentiels sans les détacher du modèle mental du cours.",
    ["vocabulaire", "contexte", "débutant"],
    "installer les mots dont les prochaines leçons ont besoin : liquidité, déplacement, zone, cible et invalidation.",
    "Avoir lu le modèle mental et la mécanique des marchés. Le but n’est pas de tout mémoriser, mais de comprendre à quoi sert chaque mot.",
    [
        """<section class="page-note beginner-bridge" id="bridge-langage-debutant"><strong>Pourquoi cette leçon revient dans le flux ?</strong> Le glossaire rapide aide quand tu bloques, mais cette leçon apprend les sigles dans l’ordre logique du modèle. Chaque terme répond à une question de lecture, pas à une définition scolaire.</section>""",
        """<section class="card" id="carte-langage-ict"><header><h2>La carte du langage : une question par famille de mots</h2><span>Vocabulaire · contexte</span></header>
<div class="chart"><svg width="100%" height="auto" viewBox="0 0 960 390" xmlns="http://www.w3.org/2000/svg"><rect width="960" height="390" fill="#081222"/><defs><marker id="arrow-lang" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#4fc3f7"/></marker></defs><g font-family="system-ui"><rect x="70" y="82" width="170" height="96" rx="14" fill="#0d1b2a" stroke="#4fc3f7"/><text x="155" y="112" text-anchor="middle" fill="#4fc3f7" font-size="13" font-weight="900">Où sont les ordres ?</text><text x="92" y="142" fill="#d9e6f2" font-size="12">Liquidité</text><text x="92" y="162" fill="#d9e6f2" font-size="12">BSL / SSL</text><text x="92" y="182" fill="#d9e6f2" font-size="12">PDH / PDL</text><rect x="285" y="82" width="170" height="96" rx="14" fill="#0d1b2a" stroke="#26a69a"/><text x="370" y="112" text-anchor="middle" fill="#26a69a" font-size="13" font-weight="900">Que fait le prix ?</text><text x="307" y="142" fill="#d9e6f2" font-size="12">Sweep / raid</text><text x="307" y="162" fill="#d9e6f2" font-size="12">Displacement</text><text x="307" y="182" fill="#d9e6f2" font-size="12">MSS</text><rect x="500" y="82" width="170" height="96" rx="14" fill="#0d1b2a" stroke="#ffb300"/><text x="585" y="112" text-anchor="middle" fill="#ffb300" font-size="13" font-weight="900">Où revenir ?</text><text x="522" y="142" fill="#d9e6f2" font-size="12">FVG</text><text x="522" y="162" fill="#d9e6f2" font-size="12">OB / Breaker</text><text x="522" y="182" fill="#d9e6f2" font-size="12">CE / OTE</text><rect x="715" y="82" width="170" height="96" rx="14" fill="#0d1b2a" stroke="#ef5350"/><text x="800" y="112" text-anchor="middle" fill="#ef5350" font-size="13" font-weight="900">Où viser / invalider ?</text><text x="737" y="142" fill="#d9e6f2" font-size="12">DOL</text><text x="737" y="162" fill="#d9e6f2" font-size="12">TP / invalidation</text><text x="737" y="182" fill="#d9e6f2" font-size="12">No trade</text><line x1="240" y1="130" x2="285" y2="130" stroke="#4fc3f7" stroke-width="2" marker-end="url(#arrow-lang)"/><line x1="455" y1="130" x2="500" y2="130" stroke="#4fc3f7" stroke-width="2" marker-end="url(#arrow-lang)"/><line x1="670" y1="130" x2="715" y2="130" stroke="#4fc3f7" stroke-width="2" marker-end="url(#arrow-lang)"/><rect x="170" y="250" width="620" height="48" rx="24" fill="#142943" stroke="#4fc3f7"/><text x="480" y="280" text-anchor="middle" fill="#d9e6f2" font-size="13" font-weight="900">Un terme ICT utile doit aider à prendre ou refuser une décision.</text></g></svg></div>
<div class="academy-grid"><div class="academy-card"><h3>Famille 1 : liquidité</h3><p>BSL, SSL, PDH et PDL servent à nommer les zones où des ordres peuvent attendre. Ce ne sont pas des signaux ; ce sont des destinations possibles.</p></div><div class="academy-card"><h3>Famille 2 : réaction</h3><p>Sweep, displacement et MSS servent à lire ce que le marché fait après avoir touché une zone importante.</p></div><div class="academy-card"><h3>Famille 3 : zone</h3><p>FVG, OB, Breaker, CE et OTE servent à localiser un retour potentiel après une impulsion. Sans contexte, ils restent des dessins.</p></div><div class="academy-card"><h3>Famille 4 : décision</h3><p>DOL, invalidation, stop et no trade transforment la lecture en plan ou en refus.</p></div></div><div class="rule-block"><strong>Règle :</strong> Si un sigle ne répond pas à une question utile, ne le trade pas.</div></section>""",
        """<section class="card" id="exemple-langage-sequence"><header><h2>Exemple simple : lire une phrase ICT sans se perdre</h2><span>Mini-cas</span></header><div class="explain"><div class="exbox"><h4>Phrase dense</h4><p>“Le prix sweep la SSL, produit un displacement bullish, casse la structure en MSS, puis revient dans le FVG avant de viser le DOL opposé.”</p></div><div class="exbox"><h4>Traduction débutant</h4><p>Le prix prend les stops sous un ancien bas, rejette cette zone avec force, montre que les acheteurs reprennent le contrôle, revient sur une zone laissée par l’impulsion, puis vise une liquidité au-dessus.</p></div><div class="exbox"><h4>Ce que tu dois faire</h4><p>Tu n’as pas besoin d’aimer les sigles. Tu dois savoir les traduire en actions observables.</p></div></div></section>""",
    ],
)


WHERE_WHEN = page(
    "Où et quand - Premium/Discount et Kill Zones",
    "Les deux filtres qui empêchent de chercher un setup au mauvais endroit ou au mauvais moment.",
    ["where", "when", "timing"],
    "ajouter les filtres de localisation et de timing avant les setups cœur.",
    "Avoir compris concept/setup/plan. Cette leçon vient avant les fondations pratiques.",
    [
        """<section class="page-note beginner-bridge" id="bridge-where-when"><strong>Le setup ne suffit pas.</strong> Trend/range répond au type d’environnement. Premium/discount répond à l’endroit dans la structure. Kill zone répond au moment où le marché mérite ton attention.</section>""",
        """<section class="card" id="premium-discount-range"><header><h2>Premium / Discount : savoir où chercher</h2><span>WHERE</span></header><div class="chart"><svg width="100%" height="auto" viewBox="0 0 960 410" xmlns="http://www.w3.org/2000/svg"><rect width="960" height="410" fill="#081222"/><rect x="120" y="80" width="700" height="230" rx="10" fill="#4fc3f7" opacity=".07" stroke="#314c6b"/><line x1="120" x2="820" y1="80" y2="80" stroke="#ef5350" stroke-width="2"/><line x1="120" x2="820" y1="195" y2="195" stroke="#ffb300" stroke-dasharray="8 6" stroke-width="2"/><line x1="120" x2="820" y1="310" y2="310" stroke="#26a69a" stroke-width="2"/><text x="840" y="85" fill="#ef5350" font-size="12" font-weight="900">Premium</text><text x="840" y="200" fill="#ffb300" font-size="12" font-weight="900">50% / Equilibrium</text><text x="840" y="315" fill="#26a69a" font-size="12" font-weight="900">Discount</text><polyline points="140,285 230,245 320,175 405,205 500,118 585,154 690,94 780,120" fill="none" stroke="#8fa5ba" stroke-width="2.6"/><rect x="180" y="238" width="180" height="50" rx="12" fill="#26a69a" opacity=".13" stroke="#26a69a"/><text x="270" y="268" text-anchor="middle" fill="#26a69a" font-size="12" font-weight="900">Chercher achats</text><rect x="560" y="92" width="180" height="50" rx="12" fill="#ef5350" opacity=".13" stroke="#ef5350"/><text x="650" y="122" text-anchor="middle" fill="#ef5350" font-size="12" font-weight="900">Chercher ventes</text></svg></div><div class="academy-grid"><div class="academy-card"><h3>Discount</h3><p>Sous le 50% d’une range pertinente, le prix est relativement bas. Les achats y ont plus de logique si le contexte autorise le long.</p></div><div class="academy-card"><h3>Premium</h3><p>Au-dessus du 50%, le prix est relativement haut. Les ventes y ont plus de logique si le contexte autorise le short.</p></div><div class="academy-card"><h3>Equilibrium</h3><p>Autour du milieu, l’avantage directionnel est souvent plus faible. Le débutant doit y être plus sélectif.</p></div></div><div class="rule-block"><strong>Règle :</strong> N’achète pas un FVG simplement parce qu’il existe ; demande d’abord s’il est situé dans une zone d’achat logique.</div></section>""",
        """<section class="card" id="killzones-timing"><header><h2>Kill Zones : savoir quand chercher</h2><span>WHEN</span></header><div class="chart"><svg width="100%" height="auto" viewBox="0 0 960 330" xmlns="http://www.w3.org/2000/svg"><rect width="960" height="330" fill="#081222"/><line x1="100" x2="860" y1="168" y2="168" stroke="#314c6b" stroke-width="2"/><g font-family="system-ui"><rect x="210" y="105" width="170" height="90" rx="14" fill="#0d1b2a" stroke="#26a69a"/><text x="295" y="132" text-anchor="middle" fill="#26a69a" font-size="13" font-weight="900">London Open</text><text x="295" y="158" text-anchor="middle" fill="#d9e6f2" font-size="12">08h00 - 09h30</text><text x="295" y="180" text-anchor="middle" fill="#8fa5ba" font-size="11">sweep / expansion</text><rect x="555" y="105" width="170" height="90" rx="14" fill="#0d1b2a" stroke="#4fc3f7"/><text x="640" y="132" text-anchor="middle" fill="#4fc3f7" font-size="13" font-weight="900">NY AM</text><text x="640" y="158" text-anchor="middle" fill="#d9e6f2" font-size="12">14h30 - 16h00</text><text x="640" y="180" text-anchor="middle" fill="#8fa5ba" font-size="11">raid / reversal / run</text><text x="100" y="222" fill="#ef5350" font-size="12" font-weight="900">Hors fenêtre : moins de qualité, plus de bruit</text><text x="100" y="82" fill="#d9e6f2" font-size="15" font-weight="900">Heure Europe/Bruxelles indicative : adapte selon actif, saison et changement d’heure.</text></g></svg></div><div class="explain"><div class="exbox"><h4>Pourquoi le temps compte</h4><p>ICT suppose que certains mouvements ont plus de probabilité pendant les ouvertures actives, quand la liquidité et le volume apparaissent.</p></div><div class="exbox"><h4>Erreur fréquente</h4><p>Scanner toute la journée transforme un filtre en chasse permanente. Le trader finit par prendre du bruit.</p></div></div></section>""",
        """<section class="card" id="matrice-where-when"><header><h2>Matrice de décision : bon setup, bon endroit, bon moment</h2><span>Filtre</span></header><div class="chart"><table class="référence-table"><tr><th>Forme visible</th><th>Zone</th><th>Timing</th><th>Décision pédagogique</th></tr><tr><td>FVG bullish propre</td><td>Discount</td><td>London ou NY AM</td><td class="ok">Chercher plan si contexte aligné</td></tr><tr><td>FVG bullish propre</td><td>Premium</td><td>Milieu de journée</td><td class="bad">Refuser ou classer faible</td></tr><tr><td>Sweep + rejet</td><td>Bord de range</td><td>NY AM</td><td class="ok">Étudier reversal possible</td></tr><tr><td>Signal isolé</td><td>Milieu de range</td><td>Hors kill zone</td><td class="bad">No trade</td></tr></table></div></section>""",
    ],
)


TOPDOWN = page(
    "Lire en top-down - du Weekly à l'entrée",
    "Donner un rôle clair à chaque timeframe pour éviter d’entrer contre la structure supérieure.",
    ["multi-timeframe", "top-down", "entrée"],
    "montrer comment construire une narrative du grand timeframe vers l’exécution précise.",
    "Avoir vu où/quand chercher. Cette leçon arrive juste avant les setups cœur.",
    [
        """<section class="page-note beginner-bridge" id="bridge-topdown"><strong>Le petit timeframe n’invente pas l’idée.</strong> Weekly et Daily donnent le décor, 4H/H1 cadrent la structure, 15M confirme, 5M précise. Si tu inverses cet ordre, tu rationalises souvent une entrée trop petite.</section>""",
        """<section class="card" id="cascade-timeframes"><header><h2>Cascade top-down : qui décide quoi ?</h2><span>Structure</span></header><div class="chart"><svg width="100%" height="auto" viewBox="0 0 960 430" xmlns="http://www.w3.org/2000/svg"><rect width="960" height="430" fill="#081222"/><g font-family="system-ui"><rect x="140" y="58" width="680" height="48" rx="14" fill="#0d1b2a" stroke="#8e44ad"/><text x="170" y="88" fill="#8e44ad" font-size="13" font-weight="900">Weekly / Daily</text><text x="375" y="88" fill="#d9e6f2" font-size="12">direction, grande liquidité, contexte</text><rect x="190" y="126" width="580" height="48" rx="14" fill="#0d1b2a" stroke="#4fc3f7"/><text x="220" y="156" fill="#4fc3f7" font-size="13" font-weight="900">4H</text><text x="375" y="156" fill="#d9e6f2" font-size="12">structure intermédiaire, range pertinente, DOL</text><rect x="240" y="194" width="480" height="48" rx="14" fill="#0d1b2a" stroke="#ffb300"/><text x="270" y="224" fill="#ffb300" font-size="13" font-weight="900">1H / 15M</text><text x="375" y="224" fill="#d9e6f2" font-size="12">confirmation, sweep, displacement, MSS</text><rect x="290" y="262" width="380" height="48" rx="14" fill="#0d1b2a" stroke="#26a69a"/><text x="320" y="292" fill="#26a69a" font-size="13" font-weight="900">5M / 1M</text><text x="445" y="292" fill="#d9e6f2" font-size="12">entrée précise uniquement</text><rect x="190" y="352" width="580" height="34" rx="17" fill="#142943" stroke="#ef5350"/><text x="480" y="374" text-anchor="middle" fill="#ef5350" font-size="12" font-weight="900">Interdit : laisser un beau 5M contredire le Daily / 4H.</text></g></svg></div></section>""",
        """<section class="card" id="roles-timeframes"><header><h2>Rôle pratique de chaque timeframe</h2><span>Méthode</span></header><div class="chart"><table class="référence-table"><tr><th>Timeframe</th><th>Question</th><th>Erreur débutant</th></tr><tr><td>Weekly / Daily</td><td>Où est la grande liquidité ? Dans quel sens le marché a-t-il de la place ?</td><td>Ne jamais les regarder.</td></tr><tr><td>4H</td><td>Quelle range ou structure intermédiaire guide la séance ?</td><td>Entrer contre une structure évidente.</td></tr><tr><td>1H / 15M</td><td>Le setup se confirme-t-il vraiment ?</td><td>Confondre micro-cassure et vraie confirmation.</td></tr><tr><td>5M / 1M</td><td>Où placer l’entrée et l’invalidation ?</td><td>Fabriquer une narrative depuis le signal d’entrée.</td></tr></table></div></section>""",
        """<section class="card" id="conflit-timeframe"><header><h2>Cas critique : beau signal, mauvaise hiérarchie</h2><span>Filtre</span></header><div class="academy-grid"><div class="academy-card"><h3>Signal 5M séduisant</h3><p>Un FVG bullish apparaît après une petite impulsion. Visuellement, il ressemble à un setup propre.</p></div><div class="academy-card"><h3>Contexte 4H bearish</h3><p>Le prix est en premium, sous une structure 4H baissière, et le DOL principal est sous le marché.</p></div><div class="academy-card"><h3>Décision</h3><p>Le 5M ne suffit pas à autoriser le long. On classe le signal en contre-contexte ou on attend un vrai changement de structure supérieur.</p></div></div><div class="rule-block"><strong>Règle :</strong> Le timeframe d’entrée exécute ; il ne doit pas inventer la direction.</div></section>""",
    ],
)


MENTAL = page(
    "Le jeu mental - trader sans se saboter",
    "Préparer le passage au réel : pertes, euphorie, tilt, revenge trade et discipline prop firm.",
    ["psychologie", "discipline", "prop firm"],
    "installer un protocole mental avant le workflow live et les contraintes de compte financé.",
    "Avoir compris la preuve statistique : tu sais qu’un edge vit sur un échantillon, pas sur un trade isolé.",
    [
        """<section class="page-note beginner-bridge" id="bridge-mental"><strong>Le mental protège le système.</strong> Le but n’est pas de “ne rien ressentir”. Le but est de savoir quoi faire quand une perte, un gain ou une série de trades modifie ton comportement.</section>""",
        """<section class="card" id="cycle-emotionnel-trader"><header><h2>Cycle émotionnel : gain, perte, tilt, protocole</h2><span>Psychologie</span></header><div class="chart"><svg width="100%" height="auto" viewBox="0 0 960 380" xmlns="http://www.w3.org/2000/svg"><rect width="960" height="380" fill="#081222"/><defs><marker id="arrow-mental" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#4fc3f7"/></marker></defs><g font-family="system-ui"><rect x="90" y="120" width="160" height="80" rx="16" fill="#0d1b2a" stroke="#26a69a"/><text x="170" y="152" text-anchor="middle" fill="#26a69a" font-size="13" font-weight="900">Gain</text><text x="170" y="174" text-anchor="middle" fill="#d9e6f2" font-size="11">euphorie possible</text><rect x="305" y="120" width="160" height="80" rx="16" fill="#0d1b2a" stroke="#ef5350"/><text x="385" y="152" text-anchor="middle" fill="#ef5350" font-size="13" font-weight="900">Perte</text><text x="385" y="174" text-anchor="middle" fill="#d9e6f2" font-size="11">urgence de se refaire</text><rect x="520" y="120" width="160" height="80" rx="16" fill="#0d1b2a" stroke="#ffb300"/><text x="600" y="152" text-anchor="middle" fill="#ffb300" font-size="13" font-weight="900">Tilt</text><text x="600" y="174" text-anchor="middle" fill="#d9e6f2" font-size="11">règles négociées</text><rect x="735" y="120" width="160" height="80" rx="16" fill="#0d1b2a" stroke="#4fc3f7"/><text x="815" y="152" text-anchor="middle" fill="#4fc3f7" font-size="13" font-weight="900">Protocole</text><text x="815" y="174" text-anchor="middle" fill="#d9e6f2" font-size="11">pause / journal / stop</text><line x1="250" y1="160" x2="305" y2="160" stroke="#4fc3f7" stroke-width="2" marker-end="url(#arrow-mental)"/><line x1="465" y1="160" x2="520" y2="160" stroke="#4fc3f7" stroke-width="2" marker-end="url(#arrow-mental)"/><line x1="680" y1="160" x2="735" y2="160" stroke="#4fc3f7" stroke-width="2" marker-end="url(#arrow-mental)"/><text x="480" y="282" text-anchor="middle" fill="#d9e6f2" font-size="13" font-weight="900">Le danger n’est pas l’émotion ; c’est la décision prise sans protocole.</text></g></svg></div></section>""",
        """<section class="card" id="protocoles-apres-trade"><header><h2>Protocoles après gain, perte et série de pertes</h2><span>Règles</span></header><div class="chart"><table class="référence-table"><tr><th>Situation</th><th>Risque mental</th><th>Protocole</th></tr><tr><td>Gain rapide</td><td>Surconfiance, ajouter un trade inutile.</td><td>Capture, journal, pause courte. Nouveau trade seulement si nouveau setup complet.</td></tr><tr><td>Perte normale</td><td>Revenge trade.</td><td>Classer : perte valide ou erreur. Si valide, ne rien “réparer”.</td></tr><tr><td>Deux pertes</td><td>Qualité de décision qui baisse.</td><td>Réduire taille ou passer en observation.</td></tr><tr><td>Trois pertes</td><td>Tilt et destruction du compte.</td><td>Stop journée. Revue à froid seulement.</td></tr></table></div><div class="rule-block"><strong>Règle :</strong> En prop firm, survivre à une mauvaise journée vaut plus qu’essayer de récupérer immédiatement.</div></section>""",
        """<section class="card" id="checklist-mental-session"><header><h2>Checklist mentale avant le live</h2><span>Préparation</span></header><div class="academy-grid"><div class="academy-card"><h3>État interne</h3><p>Fatigue, stress, excitation, envie de se refaire. Si l’état est mauvais, la taille baisse ou la session devient observation.</p></div><div class="academy-card"><h3>Limite écrite</h3><p>Nombre maximum de trades, pertes maximum, heure d’arrêt, condition de no trade.</p></div><div class="academy-card"><h3>Phrase de reset</h3><p>“Je ne dois pas gagner ce trade ; je dois exécuter mon protocole.”</p></div><div class="academy-card"><h3>Après session</h3><p>On corrige les décisions, pas les émotions. Une émotion normale avec une règle respectée n’est pas un problème.</p></div></div></section>""",
    ],
)


PAGES = {
    "23-langage-ict-contexte.html": LANGAGE,
    "24-premium-discount-killzones.html": WHERE_WHEN,
    "25-top-down-multi-timeframe.html": TOPDOWN,
    "26-psychologie-trader.html": MENTAL,
}


def update_home():
    path = Path("index.html")
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    for card in soup.select(".home-card"):
        title = card.find("h3")
        if title and "Ordre recommandé" in title.get_text(" ", strip=True):
            ul = card.find("ul")
            if ul:
                ul.clear()
                items = [
                    "02. Modèle mental",
                    "03. Parcours",
                    "04. Mécanique",
                    "05. Langage ICT en contexte",
                    "06. Liquidité et déplacement",
                    "07. Trend/range/transitions",
                    "08. Concept/plan",
                    "09. Où/quand : Premium/Discount + Kill Zones",
                    "10. Fondations",
                    "11. Top-down multi-timeframe",
                    "12. Setups cœur",
                    "13. Graphique réel",
                    "14. Variantes",
                    "15. Failures",
                ]
                for item in items:
                    li = soup.new_tag("li")
                    li.string = item
                    ul.append(li)
    links = soup.find("div", class_="section-links")
    if links:
        existing = {a.get("href") for a in links.find_all("a", href=True)}
        additions = [
            ("23-langage-ict-contexte.html", "Langage ICT", "Les sigles essentiels appris dans le contexte du modèle."),
            ("24-premium-discount-killzones.html", "Où et quand", "Premium/Discount et Kill Zones avant les setups."),
            ("25-top-down-multi-timeframe.html", "Top-down", "Construire la narrative du Weekly/Daily vers l’entrée."),
            ("26-psychologie-trader.html", "Jeu mental", "Revenge trade, tilt, euphorie et protocole prop firm."),
        ]
        for href, title, desc in additions:
            if href in existing:
                continue
            a = soup.new_tag("a", href=href, **{"class": "section-link"})
            h3 = soup.new_tag("h3")
            h3.string = title
            p = soup.new_tag("p")
            p.string = desc
            a.append(h3)
            a.append(p)
            links.append(a)
    path.write_text(str(soup), encoding="utf-8")


def update_index_concepts():
    path = Path("15-index-concepts.html")
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    old = soup.find(id="index-v48-zero-to-hero")
    if old:
        old.decompose()
    main = soup.find("main", class_="page")
    if not main:
        return
    section = BeautifulSoup("""<section class="card" id="index-v48-zero-to-hero"><header><h2>Index V48 — leçons zero-to-hero</h2><span>Progression</span></header><div class="academy-grid"><div class="academy-card"><h3>Langage ICT</h3><p><a href="23-langage-ict-contexte.html">Lire les sigles en contexte</a></p></div><div class="academy-card"><h3>Où et quand</h3><p><a href="24-premium-discount-killzones.html">Premium/Discount et Kill Zones</a></p></div><div class="academy-card"><h3>Top-down</h3><p><a href="25-top-down-multi-timeframe.html">Du Weekly à l'entrée</a></p></div><div class="academy-card"><h3>Jeu mental</h3><p><a href="26-psychologie-trader.html">Trader sans se saboter</a></p></div></div></section>""", "html.parser").section
    bottom = main.find("nav", class_="lesson-bottom-nav")
    if bottom:
        bottom.insert_before(section)
    else:
        main.append(section)
    path.write_text(str(soup), encoding="utf-8")


def main():
    for filename, html in PAGES.items():
        Path(filename).write_text(html, encoding="utf-8")
    update_home()
    update_index_concepts()


if __name__ == "__main__":
    main()
