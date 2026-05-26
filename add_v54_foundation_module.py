from pathlib import Path
from bs4 import BeautifulSoup


ROOT = Path(".")


def page_shell(title, subtitle, tags, body):
    tag_html = "".join(f"<span>{tag}</span>" for tag in tags)
    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width,initial-scale=1" name="viewport"/>
<title>{title}</title>
<link href="style.css" rel="stylesheet"/>
</head>
<body>
<div class="app-shell">
<aside aria-label="Navigation principale" class="site-nav"></aside>
<main class="page" id="contenu">
<div class="hero">
<h1>{title}</h1>
<p>{subtitle}</p>
<div class="tagline">{tag_html}</div>
</div>
{body}
</main>
</div>
</body>
</html>
"""


def glossary(term, label=None):
    label = label or term
    return f'<button class="glossary-term" data-glossary-term="{term}" type="button">{label}</button>'


def chart_base(inner, height=390):
    return f"""<div class="chart"><svg height="auto" viewbox="0 0 960 {height}" width="100%" xmlns="http://www.w3.org/2000/svg">
<rect fill="#081222" height="{height}" width="960"></rect>
<g opacity=".55">
<line stroke="#1e3a5f" x1="70" x2="850" y1="70" y2="70"></line>
<line stroke="#1e3a5f" x1="70" x2="850" y1="140" y2="140"></line>
<line stroke="#1e3a5f" x1="70" x2="850" y1="210" y2="210"></line>
<line stroke="#1e3a5f" x1="70" x2="850" y1="280" y2="280"></line>
</g>
{inner}
</svg></div>"""


def candles(points, color="#8fa5ba", width=2.4):
    return f'<polyline fill="none" points="{points}" stroke="{color}" stroke-width="{width}"></polyline>'


def dot(x, y, color):
    return f'<circle cx="{x}" cy="{y}" fill="{color}" paint-order="stroke fill" r="5.5" stroke="#e6f4ff" stroke-width="1.4"></circle>'


def label(x, y, text, color="#d9e6f2", anchor="middle", size=12):
    return f'<text fill="{color}" font-size="{size}" font-weight="900" text-anchor="{anchor}" x="{x}" y="{y}" paint-order="stroke fill" stroke="#081222" stroke-width="3">{text}</text>'


def pill(x, y, w, text, color="#4fc3f7"):
    return f'<rect fill="#081222" height="24" opacity=".98" rx="12" stroke="{color}" width="{w}" x="{x}" y="{y}"></rect>{label(x + w / 2, y + 16, text, color, size=10.5)}'


def arrow_marker(marker_id, color="#4fc3f7"):
    return f'<defs><marker id="{marker_id}" markerheight="10" markerwidth="10" orient="auto" refx="8" refy="3"><path d="M0,0 L0,6 L9,3 z" fill="{color}"></path></marker></defs>'


def abc_case(title, verdict, color, points, overlays, checks, bad=False):
    items = "".join(f'<li class="{"abc-cross" if bad else "abc-check"}">{item}</li>' for item in checks)
    svg = f"""<svg height="auto" viewbox="0 0 320 280" width="100%" xmlns="http://www.w3.org/2000/svg">
<rect fill="#081222" height="280" width="320"></rect>
<line opacity=".45" stroke="#1e3a5f" x1="12" x2="302" y1="58" y2="58"></line>
<line opacity=".45" stroke="#1e3a5f" x1="12" x2="302" y1="116" y2="116"></line>
<line opacity=".45" stroke="#1e3a5f" x1="12" x2="302" y1="174" y2="174"></line>
<line opacity=".45" stroke="#1e3a5f" x1="12" x2="302" y1="232" y2="232"></line>
<rect fill="#081222" height="30" rx="4" stroke="{color}" width="306" x="7" y="6"></rect>
<text fill="{color}" font-size="10" font-weight="900" text-anchor="middle" x="160" y="25" paint-order="stroke fill" stroke="#081222" stroke-width="2">{title}</text>
<polyline fill="none" points="{points}" stroke="#8fa5ba" stroke-width="2.1"></polyline>
{overlays}
<text fill="#8fa5ba" font-size="8" font-weight="700" text-anchor="middle" x="160" y="268" paint-order="stroke fill" stroke="#081222" stroke-width="2">{verdict}</text>
</svg>"""
    return f'<div class="abc-case"><div class="chart">{svg}</div><ul class="abc-list">{items}</ul></div>'


def liquidity_lesson():
    clean = abc_case(
        "A - Cible propre",
        "liquidite externe claire, non prise",
        "#26a69a",
        "28,210 60,170 92,194 124,142 156,166 188,118 220,148 252,96 290,118",
        '<line stroke="#ef5350" stroke-dasharray="5,3" x1="18" x2="302" y1="96" y2="96"></line>'
        + dot(252, 96, "#ef5350")
        + '<line stroke="#ef5350" stroke-dasharray="3,2" x1="252" x2="220" y1="96" y2="74"></line>'
        + label(215, 70, "BSL cible", "#ef5350", "end", 8),
        ["High évident, plusieurs réactions visibles", "Niveau encore non consommé", "Peut devenir DOL si le contexte pousse vers lui"],
    )
    weak = abc_case(
        "B - Cible faible",
        "niveau interne, avantage plus bas",
        "#ffb300",
        "28,205 60,165 92,190 124,150 156,170 188,138 220,158 252,132 290,150",
        '<line stroke="#ffb300" stroke-dasharray="5,3" x1="18" x2="302" y1="138" y2="138"></line>'
        + dot(188, 138, "#ffb300")
        + '<line stroke="#ffb300" stroke-dasharray="3,2" x1="188" x2="232" y1="138" y2="118"></line>'
        + label(236, 114, "interne", "#ffb300", "start", 8),
        ["Liquidité au milieu de la structure", "Peut servir de TP1, rarement de TP final", "Demande plus de prudence"],
        bad=True,
    )
    consumed = abc_case(
        "C - Deja consommee",
        "la cible a deja ete prise",
        "#ef5350",
        "28,205 60,165 92,190 124,126 156,150 188,115 220,148 252,132 290,158",
        '<line stroke="#ef5350" stroke-dasharray="5,3" x1="18" x2="302" y1="126" y2="126"></line>'
        + dot(124, 126, "#ef5350")
        + '<text fill="#ef5350" font-size="26" font-weight="900" x="230" y="96" text-anchor="middle" paint-order="stroke fill" stroke="#081222" stroke-width="2">x</text>'
        + label(222, 112, "deja prise", "#ef5350", "middle", 8),
        ["DOL déjà atteint ou sweep déjà fait", "Entrer vers cette cible arrive trop tard", "Le trade perd son asymétrie"],
        bad=True,
    )
    abc = f'<div class="abc-grid">{clean}{weak}{consumed}</div>'
    body = f"""
<div class="page-meta-dashboard"><div class="meta-main"><div class="meta-goal"><strong>Objectif</strong> apprendre a lire la liquidite avant toute idee d'entree.</div><div class="meta-prereq"><strong>Prerequis</strong> comprendre que le prix cherche des ordres, pas des lignes magiques.</div></div><div class="meta-sidebar"><strong>A lire avec</strong><nav class="pill-nav"><a class="pill" href="21-liquidite-deplacement.html">Deplacement du prix</a><a class="pill" href="28-fondations-entree.html">Scenario d'entree</a><a class="pill" href="29-fondations-stop-tp.html">Stop et TP</a></nav></div></div>
<section class="page-note beginner-bridge"><strong>Idee simple :</strong> avant de demander "ou entrer ?", demande "ou le prix peut-il trouver des ordres ?" Une entree sans cible de liquidite devient une opinion.</section>
<section class="card" id="origine-liquidite"><header><h2>D'ou vient la liquidite ?</h2><span>Fondation</span></header><div class="academy-grid"><div class="academy-card"><h3>Stops</h3><p>Au-dessus d'un high, des stops de shorts deviennent des achats forces. Sous un low, des stops de longs deviennent des ventes forcees.</p></div><div class="academy-card"><h3>Breakouts</h3><p>Beaucoup de traders achetent la cassure d'un high ou vendent la cassure d'un low. Ces ordres ajoutent du volume exactement autour des niveaux visibles.</p></div><div class="academy-card"><h3>Prises de profit</h3><p>Un trader deja en position vise souvent les anciens highs/lows. Les TP creent aussi de la liquidite disponible pour l'autre camp.</p></div></div><div class="rule-block"><strong>Regle :</strong> une zone de liquidite est utile si elle concentre des ordres probables et si elle n'a pas deja ete consommee.</div></section>
<section class="card" id="carte-cibles-liquidite"><header><h2>Carte des points cles : externe, interne, journalier, session</h2><span>Graphique</span></header>
{chart_base(arrow_marker("arr-liq") + candles("105,255 160,210 215,232 270,176 325,205 380,150 435,178 490,126 545,156 600,104 660,132 720,86 805,112") + '<line stroke="#ef5350" stroke-dasharray="7 5" stroke-width="1.4" x1="90" x2="850" y1="86" y2="86"></line>' + '<line stroke="#26a69a" stroke-dasharray="7 5" stroke-width="1.4" x1="90" x2="850" y1="255" y2="255"></line>' + '<line stroke="#ffb300" stroke-dasharray="5 4" stroke-width="1.2" x1="230" x2="610" y1="176" y2="176"></line>' + dot(720,86,"#ef5350") + dot(105,255,"#26a69a") + dot(380,150,"#ffb300") + pill(628,52,128,"BSL externe","#ef5350") + pill(102,266,128,"SSL externe","#26a69a") + pill(390,182,145,"liquidite interne","#ffb300") + label(790,156,"PDH / Asia High / EQH = points cles", "#4fc3f7", "end", 12))}
<div class="explain"><div class="exbox"><h4>Externe</h4><p>Liquidite au-dela de la structure actuelle. Elle sert souvent de DOL ou de TP principal.</p></div><div class="exbox"><h4>Interne</h4><p>Liquidite au milieu du mouvement. Elle peut servir de TP1, mais elle justifie rarement un trade complet seule.</p></div><div class="exbox"><h4>Session/journalier</h4><p>PDH, PDL, Asia High/Low et equal highs/lows sont importants parce que beaucoup de traders les voient.</p></div></div></section>
	<section class="card" id="abc-liquidite-cible"><header><h2>Liquidite cible A/B/C : propre, faible, deja consommee</h2><span>Serie A/B/C</span></header><div class="page-note">Le meme niveau horizontal n'a pas toujours la meme valeur. Il faut juger sa fraicheur, sa position et sa visibilite.</div>{abc}</section>
	<section class="card" id="definir-ligne-liquidite"><header><h2>Comment definir une ligne de liquidite ?</h2><span>Precision</span></header>
	{chart_base(arrow_marker("arr-zone") + candles("105,238 160,198 215,216 270,174 325,204 380,158 435,184 490,142 545,164 600,126 660,150 720,108 805,134") + '<rect fill="#ef5350" opacity=".12" x="90" y="94" width="760" height="34"></rect><line stroke="#ef5350" stroke-dasharray="7 5" stroke-width="1.5" x1="90" x2="850" y1="108" y2="108"></line><line stroke="#ef5350" opacity=".55" stroke-width="1" x1="90" x2="850" y1="128" y2="128"></line>' + dot(720,108,"#ef5350") + dot(600,126,"#ffb300") + '<line marker-end="url(#arr-zone)" stroke="#ef5350" stroke-dasharray="5 4" x1="720" x2="666" y1="108" y2="72"></line>' + '<line marker-end="url(#arr-zone)" stroke="#ffb300" stroke-dasharray="5 4" x1="600" x2="560" y1="126" y2="86"></line>' + pill(620,44,170,"zone, pas pixel","#ef5350") + pill(458,58,148,"marges de meches","#ffb300") + label(480,320,"Une ligne de liquidite est une zone visible ou des ordres sont probables, pas un trait magique.", "#d9e6f2", "middle", 12))}
	<div class="academy-grid"><div class="academy-card"><h3>Point d'ancrage</h3><p>Pars du high/low le plus visible : PDH, PDL, high de session, low de session, equal highs/lows.</p></div><div class="academy-card"><h3>Zone utile</h3><p>Ajoute une marge autour des meches. Plus le niveau est evident, plus il faut penser en zone de reaction.</p></div><div class="academy-card"><h3>Validation</h3><p>La zone compte si elle peut attirer des stops, des breakout traders ou des prises de profit.</p></div></div><div class="rule-block"><strong>Regle :</strong> tu traces le niveau pour definir une destination probable, pas pour predire que le prix s'arretera exactement dessus.</div></section>
	<section class="card" id="cible-vs-declencheur"><header><h2>Cible ou declencheur : ne melange pas les roles</h2><span>Decision</span></header>
{chart_base(candles("105,260 160,230 215,250 270,205 325,224 380,182 435,202 490,156 545,182 600,128 660,150 720,100 805,126") + '<line stroke="#26a69a" stroke-dasharray="7 5" x1="90" x2="850" y1="260" y2="260"></line>' + '<line stroke="#ef5350" stroke-dasharray="7 5" x1="90" x2="850" y1="100" y2="100"></line>' + dot(105,260,"#26a69a") + dot(720,100,"#ef5350") + '<line stroke="#4fc3f7" stroke-dasharray="4 3" x1="105" x2="720" y1="260" y2="100"></line>' + pill(120,270,165,"declencheur possible","#26a69a") + pill(580,66,148,"cible probable","#ef5350") + label(480,315,"Le sweep peut declencher; le DOL donne la destination.", "#d9e6f2", "middle", 13))}
<div class="rule-block"><strong>Regle :</strong> si tu ne sais pas dire quelle liquidite declenche et quelle liquidite sert de cible, le scenario n'est pas pret.</div></section>
<section class="card" id="exercice-liquidite"><header><h2>Mini exercice : classe les niveaux avant de continuer</h2><span>Pratique</span></header><div class="academy-grid"><div class="academy-card"><h3>Etape 1</h3><p>Sur un graphique vierge, marque seulement les highs/lows evidents : PDH, PDL, Asia High/Low, equal highs/lows.</p></div><div class="academy-card"><h3>Etape 2</h3><p>Classe chaque niveau : externe, interne, deja pris, faible ou propre.</p></div><div class="academy-card"><h3>Etape 3</h3><p>Choisis une seule destination logique. Si plusieurs niveaux se contredisent, attends plus d'information.</p></div></div></section>
"""
    return page_shell("ICT Atlas - Fondations liquidite", "Lire ou le prix veut aller avant de chercher une entree.", ["liquidite", "DOL", "points cles"], body)


def entry_lesson():
    valid = abc_case(
        "A - Entree valide",
        "sequence complete avant entree",
        "#26a69a",
        "28,214 60,180 92,202 124,230 156,246 188,188 220,145 252,170 290,112",
        '<line stroke="#26a69a" stroke-dasharray="5,3" x1="18" x2="302" y1="246" y2="246"></line>'
        + dot(156,246,"#26a69a")
        + '<rect fill="#4fc3f7" opacity=".14" x="176" y="170" width="88" height="42"></rect>'
        + dot(216,191,"#26a69a")
        + label(238, 162, "FVG/CE", "#4fc3f7", "middle", 8),
        ["Liquidité prise avant l’entrée", "Déplacement puis zone exploitable", "Entrée après retour, pas pendant la panique"],
    )
    early = abc_case(
        "B - Trop tot",
        "entree pendant le sweep",
        "#ffb300",
        "28,184 60,156 92,176 124,210 156,242 188,220 220,190 252,170 290,158",
        dot(156,242,"#ffb300")
        + '<line stroke="#ffb300" stroke-dasharray="3,2" x1="156" x2="210" y1="242" y2="226"></line>'
        + label(216, 222, "pas encore de rejet", "#ffb300", "start", 8),
        ["Sweep non confirmé", "Pas de displacement inverse", "Stop souvent placé au hasard"],
        bad=True,
    )
    no_context = abc_case(
        "C - Sans contexte",
        "beau FVG, mauvaise histoire",
        "#ef5350",
        "28,205 60,170 92,188 124,150 156,172 188,132 220,158 252,142 290,168",
        '<rect fill="#4fc3f7" opacity=".14" x="122" y="150" width="92" height="40"></rect>'
        + dot(170,170,"#ef5350")
        + '<text fill="#ef5350" font-size="26" font-weight="900" text-anchor="middle" x="250" y="112" paint-order="stroke fill" stroke="#081222" stroke-width="2">x</text>'
        + label(245, 132, "DOL absent", "#ef5350", "middle", 8),
        ["Zone jolie mais pas reliée à une liquidité", "Aucune destination claire", "Trade impossible à défendre"],
        bad=True,
    )
    body = f"""
<div class="page-meta-dashboard"><div class="meta-main"><div class="meta-goal"><strong>Objectif</strong> comprendre pourquoi entrer ici, maintenant, et pas seulement parce qu'une forme apparait.</div><div class="meta-prereq"><strong>Prerequis</strong> savoir classer une liquidite cible et un declencheur.</div></div><div class="meta-sidebar"><strong>A lire avec</strong><nav class="pill-nav"><a class="pill" href="27-fondations-liquidite.html">Fondations liquidite</a><a class="pill" href="29-fondations-stop-tp.html">Stop et TP</a><a class="pill" href="04-setups-core.html">Setups coeur</a></nav></div></div>
<section class="page-note beginner-bridge"><strong>Idee simple :</strong> une entree est une consequence. Elle vient apres la liquidite, la reaction et la preuve de changement de controle.</section>
<section class="card" id="sequence-entree"><header><h2>La sequence causale avant l'entree</h2><span>Fondation</span></header>
{chart_base(arrow_marker("arr-entry") + '<rect fill="#0d1b2a" height="62" rx="12" stroke="#4fc3f7" width="130" x="70" y="145"></rect><rect fill="#0d1b2a" height="62" rx="12" stroke="#26a69a" width="130" x="250" y="145"></rect><rect fill="#0d1b2a" height="62" rx="12" stroke="#ffb300" width="130" x="430" y="145"></rect><rect fill="#0d1b2a" height="62" rx="12" stroke="#4fc3f7" width="130" x="610" y="145"></rect><rect fill="#0d1b2a" height="62" rx="12" stroke="#26a69a" width="130" x="790" y="145"></rect>' + label(135,170,"1. Cible", "#4fc3f7") + label(315,170,"2. Sweep", "#26a69a") + label(495,170,"3. Rejet", "#ffb300") + label(675,170,"4. MSS/FVG", "#4fc3f7") + label(855,170,"5. Entree", "#26a69a") + '<line marker-end="url(#arr-entry)" stroke="#4fc3f7" stroke-width="1.8" x1="200" x2="250" y1="176" y2="176"></line><line marker-end="url(#arr-entry)" stroke="#4fc3f7" stroke-width="1.8" x1="380" x2="430" y1="176" y2="176"></line><line marker-end="url(#arr-entry)" stroke="#4fc3f7" stroke-width="1.8" x1="560" x2="610" y1="176" y2="176"></line><line marker-end="url(#arr-entry)" stroke="#4fc3f7" stroke-width="1.8" x1="740" x2="790" y1="176" y2="176"></line>' + label(480,285,"Si une etape manque, l'entree devient une hypothese fragile.", "#d9e6f2", "middle", 13))}
<div class="rule-block"><strong>Regle :</strong> une entree ICT doit pouvoir etre racontee dans l'ordre. Si tu commences par "j'ai vu un FVG", tu commences trop tard.</div></section>
<section class="card" id="abc-entree"><header><h2>Entree A/B/C : complete, prematuree, hors contexte</h2><span>Serie A/B/C</span></header><div class="abc-grid">{valid}{early}{no_context}</div></section>
	<section class="card" id="ou-entrer"><header><h2>Ou entrer : CE, FVG, OB ne sont que des zones candidates</h2><span>Graphique</span></header>
	{chart_base(candles("105,250 160,225 215,255 270,285 325,232 380,172 435,138 490,168 545,126 600,148 660,108 720,132 805,88") + '<line stroke="#26a69a" stroke-dasharray="7 5" x1="90" x2="850" y1="285" y2="285"></line>' + '<rect fill="#4fc3f7" opacity=".14" x="395" y="150" width="112" height="52"></rect>' + '<line stroke="#ffb300" stroke-dasharray="5 4" x1="395" x2="507" y1="176" y2="176"></line>' + dot(270,285,"#26a69a") + dot(450,176,"#26a69a") + dot(720,88,"#4fc3f7") + pill(214,294,110,"sweep SSL","#26a69a") + pill(413,207,92,"CE / FVG","#4fc3f7") + pill(693,54,78,"TP2","#4fc3f7") + label(480,322,"L'entree se place sur le retour dans la zone, apres preuve de controle.", "#d9e6f2", "middle", 12))}
	<div class="academy-grid"><div class="academy-card"><h3>CE</h3><p>Le CE sert de repere de precision, mais seulement si la zone est issue d'un vrai displacement.</p></div><div class="academy-card"><h3>FVG</h3><p>Le FVG indique une livraison rapide du prix. Il doit etre relie a liquidite, MSS, DOL et timing.</p></div><div class="academy-card"><h3>OB</h3><p>L'OB est une zone source. Il devient utile si le marche confirme qu'il defend cette zone.</p></div></div></section>
	<section class="card" id="quand-comment-entrer"><header><h2>Quand et comment entrer : ne pas cliquer sur la premiere forme</h2><span>Execution</span></header>
	{chart_base(candles("105,250 160,224 215,252 270,286 325,242 380,178 435,142 490,166 545,130 600,154 660,116 720,138 805,100") + '<line stroke="#26a69a" stroke-dasharray="7 5" x1="90" x2="850" y1="286" y2="286"></line><rect fill="#4fc3f7" opacity=".12" x="386" y="148" width="126" height="58"></rect><line stroke="#ffb300" stroke-dasharray="5 4" x1="386" x2="512" y1="177" y2="177"></line><line stroke="#26a69a" stroke-width="1.4" x1="512" x2="595" y1="177" y2="154"></line><line stroke="#4fc3f7" stroke-dasharray="5 4" x1="595" x2="660" y1="154" y2="116"></line>' + dot(270,286,"#26a69a") + dot(450,177,"#26a69a") + dot(600,154,"#ffb300") + dot(660,116,"#4fc3f7") + pill(215,298,108,"1 sweep","#26a69a") + pill(404,210,110,"2 retour CE","#4fc3f7") + pill(555,162,115,"3 reaction","#ffb300") + pill(630,82,118,"4 continuation","#4fc3f7") + label(480,326,"Entrer = zone + timing + reaction. Une seule piece manque, tu attends.", "#d9e6f2", "middle", 12))}
	<div class="explain"><div class="exbox"><h4>Entrée limite</h4><p>Tu poses sur CE/FVG/OB seulement si la sequence est nette et si l'invalidation est claire.</p></div><div class="exbox"><h4>Entrée confirmation</h4><p>Tu attends une reaction dans la zone : rejet, micro MSS ou bougie qui defend la zone.</p></div><div class="exbox"><h4>Pas d'entrée</h4><p>Si le prix arrive sans sweep, sans DOL, sans deplacement ou apres objectif atteint, le bon clic est souvent aucun clic.</p></div></div><div class="rule-block"><strong>Regle :</strong> l'entree sert a exploiter un scenario deja construit. Elle ne doit jamais construire le scenario a elle seule.</div></section>
	<section class="card" id="entree-apres-dol"><header><h2>Cas piege : entrer apres DOL atteint</h2><span>Faux ami</span></header>
{chart_base(candles("105,265 160,220 215,240 270,178 325,205 380,140 435,168 490,104 545,132 600,88 660,115 720,132 805,170") + '<line stroke="#ef5350" stroke-dasharray="7 5" x1="90" x2="850" y1="88" y2="88"></line>' + '<rect fill="#4fc3f7" opacity=".12" x="636" y="120" width="82" height="38"></rect>' + dot(600,88,"#ef5350") + dot(675,140,"#ef5350") + '<text fill="#ef5350" font-size="34" font-weight="900" text-anchor="middle" x="765" y="110" paint-order="stroke fill" stroke="#081222" stroke-width="3">x</text>' + pill(542,54,112,"DOL atteint","#ef5350") + pill(624,164,130,"FVG trop tard","#ef5350") + label(480,315,"Une belle zone apres destination atteinte vaut souvent moins qu'elle ne semble.", "#d9e6f2", "middle", 12))}
<div class="rule-block"><strong>Regle :</strong> apres DOL atteint, le trade doit etre requalifie. Tu ne cherches plus la meme continuation comme si rien n'avait change.</div></section>
<section class="card" id="exercice-entree"><header><h2>Mini exercice : justifie l'entree en une phrase</h2><span>Pratique</span></header><div class="academy-grid"><div class="academy-card"><h3>Phrase attendue</h3><p>"Le prix a pris telle liquidite, a rejete, a deplace, puis revient dans telle zone avant telle cible."</p></div><div class="academy-card"><h3>Si tu bloques</h3><p>Si tu ne peux pas nommer la liquidite, le deplacement ou la cible, l'entree n'est pas encore defendable.</p></div><div class="academy-card"><h3>Refus</h3><p>Un no trade propre est une bonne reponse. Le but est d'apprendre a ne pas cliquer.</p></div></div></section>
"""
    return page_shell("ICT Atlas - Fondations entree", "Construire le scenario qui explique pourquoi entrer ici.", ["scenario", "entree", "confirmation"], body)


def stop_tp_lesson():
    stop_good = abc_case(
        "A - Stop logique",
        "invalidation derriere structure",
        "#26a69a",
        "28,220 60,190 92,210 124,238 156,250 188,198 220,160 252,184 290,132",
        '<line stroke="#26a69a" stroke-dasharray="5,3" x1="18" x2="302" y1="250" y2="250"></line>'
        + '<line stroke="#ef5350" stroke-dasharray="5,3" x1="18" x2="302" y1="258" y2="258"></line>'
        + dot(188,198,"#26a69a")
        + label(238, 260, "stop sous sweep", "#ef5350", "middle", 8),
        ["Stop place la ou le scenario est faux", "Le risque se calcule depuis cette invalidation", "Le TP reste assez loin pour justifier le trade"],
    )
    stop_tight = abc_case(
        "B - Stop serre",
        "stop dans le bruit normal",
        "#ffb300",
        "28,220 60,190 92,210 124,238 156,250 188,198 220,160 252,184 290,132",
        '<line stroke="#ef5350" stroke-dasharray="5,3" x1="18" x2="302" y1="204" y2="204"></line>'
        + dot(188,198,"#ffb300")
        + label(245, 198, "trop serre", "#ffb300", "middle", 8),
        ["Le stop ne protege pas une structure", "Une simple respiration peut sortir le trade", "Risque joli mais fragile"],
        bad=True,
    )
    no_inv = abc_case(
        "C - Sans invalidation",
        "stop arbitraire, plan absent",
        "#ef5350",
        "28,205 60,178 92,196 124,164 156,188 188,150 220,174 252,142 290,166",
        '<line stroke="#ef5350" stroke-dasharray="5,3" x1="18" x2="302" y1="232" y2="232"></line>'
        + '<text fill="#ef5350" font-size="26" font-weight="900" x="230" y="118" text-anchor="middle" paint-order="stroke fill" stroke="#081222" stroke-width="2">?</text>'
        + label(210, 252, "distance arbitraire", "#ef5350", "middle", 8),
        ["Aucune condition claire qui annule l'idee", "Stop choisi pour le confort", "Impossible a backtester proprement"],
        bad=True,
    )
    body = f"""
<div class="page-meta-dashboard"><div class="meta-main"><div class="meta-goal"><strong>Objectif</strong> transformer une entree en plan complet : invalidation, stop, TP1, TP2 et gestion.</div><div class="meta-prereq"><strong>Prerequis</strong> avoir une cible de liquidite et une entree justifiee.</div></div><div class="meta-sidebar"><strong>A lire avec</strong><nav class="pill-nav"><a class="pill" href="27-fondations-liquidite.html">Fondations liquidite</a><a class="pill" href="28-fondations-entree.html">Fondations entree</a><a class="pill" href="12-gestion-risque.html">Gestion du risque</a></nav></div></div>
<section class="page-note beginner-bridge"><strong>Idee simple :</strong> un trade n'est complet que si tu sais ou il est faux et ou il peut raisonnablement payer.</section>
<section class="card" id="anatomie-plan"><header><h2>Anatomie du plan : entree, invalidation, TP1, TP2</h2><span>Graphique</span></header>
{chart_base(candles("105,258 160,224 215,246 270,282 325,236 380,178 435,144 490,172 545,128 600,150 660,108 720,132 805,86") + '<line stroke="#26a69a" stroke-dasharray="7 5" x1="90" x2="850" y1="282" y2="282"></line>' + '<rect fill="#4fc3f7" opacity=".14" x="390" y="154" width="112" height="48"></rect>' + '<line stroke="#ef5350" stroke-dasharray="6 4" x1="90" x2="850" y1="298" y2="298"></line>' + '<line stroke="#4fc3f7" stroke-dasharray="6 4" x1="90" x2="850" y1="132" y2="132"></line>' + '<line stroke="#4fc3f7" stroke-dasharray="6 4" x1="90" x2="850" y1="86" y2="86"></line>' + dot(270,282,"#26a69a") + dot(446,178,"#26a69a") + dot(720,132,"#4fc3f7") + dot(805,86,"#4fc3f7") + pill(224,304,110,"invalidation","#ef5350") + pill(400,210,90,"entree","#26a69a") + pill(680,140,76,"TP1","#4fc3f7") + pill(770,54,76,"TP2","#4fc3f7") + label(480,335,"Le stop repond a 'ou suis-je faux ?'. Les TP repondent a 'ou sont les prochains ordres ?'.", "#d9e6f2", "middle", 12))}
<div class="rule-block"><strong>Regle :</strong> si le TP logique est trop proche du point d'entree, le trade est refuse meme si le setup est propre.</div></section>
<section class="card" id="abc-stop"><header><h2>Stop A/B/C : logique, trop serre, arbitraire</h2><span>Serie A/B/C</span></header><div class="abc-grid">{stop_good}{stop_tight}{no_inv}</div></section>
	<section class="card" id="tp-logique"><header><h2>TP1 et TP2 : sortir sur des liquidites, pas sur l'espoir</h2><span>Objectifs</span></header>
	{chart_base(candles("105,255 160,220 215,245 270,196 325,220 380,176 435,198 490,152 545,178 600,126 660,150 720,98 805,120") + '<line stroke="#ffb300" stroke-dasharray="6 4" x1="90" x2="850" y1="176" y2="176"></line>' + '<line stroke="#4fc3f7" stroke-dasharray="6 4" x1="90" x2="850" y1="98" y2="98"></line>' + '<line stroke="#ef5350" stroke-dasharray="6 4" x1="90" x2="850" y1="245" y2="245"></line>' + dot(490,152,"#26a69a") + dot(600,126,"#ffb300") + dot(720,98,"#4fc3f7") + pill(420,160,94,"entree","#26a69a") + pill(562,184,132,"TP1 interne","#ffb300") + pill(680,64,132,"TP2 externe","#4fc3f7") + label(480,318,"TP1 reduit le risque; TP2 vise la liquidite principale.", "#d9e6f2", "middle", 12))}
	<div class="academy-grid"><div class="academy-card"><h3>TP1</h3><p>Premier niveau ou le prix peut rencontrer des ordres : high interne, milieu de range, niveau intraday.</p></div><div class="academy-card"><h3>TP2</h3><p>Destination principale : BSL/SSL externe, PDH/PDL, Asia High/Low ou DOL choisi.</p></div><div class="academy-card"><h3>Refus</h3><p>Si TP1 est trop proche et TP2 peu clair, le risque ne paie pas. Le bon trade peut etre de ne rien faire.</p></div></div></section>
	<section class="card" id="tp-maximum-securisation"><header><h2>TP maximum logique et securisation : sortir sans predire le retournement</h2><span>Gestion</span></header>
	{chart_base(candles("105,260 160,224 215,246 270,282 325,230 380,176 435,148 490,170 545,132 600,154 660,112 720,134 805,92") + '<line stroke="#ef5350" stroke-dasharray="6 4" x1="90" x2="850" y1="296" y2="296"></line><line stroke="#ffb300" stroke-dasharray="6 4" x1="90" x2="850" y1="154" y2="154"></line><rect fill="#4fc3f7" opacity=".12" x="90" y="78" width="760" height="34"></rect><line stroke="#4fc3f7" stroke-dasharray="6 4" x1="90" x2="850" y1="92" y2="92"></line>' + dot(446,176,"#26a69a") + dot(600,154,"#ffb300") + dot(805,92,"#4fc3f7") + '<line stroke="#26a69a" stroke-dasharray="4 3" x1="446" x2="600" y1="176" y2="154"></line><line stroke="#ffb300" stroke-dasharray="4 3" x1="600" x2="805" y1="154" y2="92"></line>' + pill(398,184,92,"entree","#26a69a") + pill(552,162,102,"TP1/BE","#ffb300") + pill(710,52,158,"TP max logique","#4fc3f7") + pill(214,304,120,"stop initial","#ef5350") + label(480,326,"On ne predit pas le retournement : on sort quand la raison du trade a ete payee.", "#d9e6f2", "middle", 12))}
	<div class="academy-grid"><div class="academy-card"><h3>TP maximum</h3><p>C'est la prochaine liquidite majeure non consommee : PDH/PDL, equal highs/lows, high/low externe ou DOL HTF.</p></div><div class="academy-card"><h3>Securiser</h3><p>A TP1, reduis le risque : partiel, stop break-even ou stop sous le dernier creux/haut structurel.</p></div><div class="academy-card"><h3>Runner</h3><p>Apres la cible principale, le runner devient optionnel. Si la structure casse contre toi, le reliquat sort.</p></div></div><div class="rule-block"><strong>Regle :</strong> le TP maximum n'est pas "le top". C'est la derniere zone ou ton scenario initial reste paye et rationnel.</div></section>
<section class="card" id="tp-abc"><header><h2>TP A/B/C : logique, trop ambitieux, trop proche</h2><span>Serie visuelle</span></header>
<div class="abc-grid">
{abc_case("A - TP logique","TP sur liquidite externe","#26a69a","28,220 60,190 92,210 124,178 156,198 188,160 220,182 252,130 290,152",'<line stroke="#4fc3f7" stroke-dasharray="5,3" x1="18" x2="302" y1="130" y2="130"></line>'+dot(252,130,"#4fc3f7")+label(230,112,"TP externe","#4fc3f7","middle",8),["Cible visible et non consommee","Distance suffisante pour le risque","Sortie reliee au DOL"])}
{abc_case("B - Trop ambitieux","cible loin sans relais","#ffb300","28,220 60,190 92,210 124,178 156,198 188,160 220,182 252,152 290,170",'<line stroke="#ffb300" stroke-dasharray="5,3" x1="18" x2="302" y1="72" y2="72"></line>'+label(230,66,"trop loin","#ffb300","middle",8),["TP choisi pour le ratio","Aucune liquidite evidente","Le plan devient de l'espoir"], True)}
{abc_case("C - Trop proche","asymetrie insuffisante","#ef5350","28,220 60,190 92,210 124,178 156,198 188,160 220,182 252,152 290,170",'<line stroke="#ef5350" stroke-dasharray="5,3" x1="18" x2="302" y1="170" y2="170"></line>'+dot(188,160,"#ef5350")+label(236,170,"TP proche","#ef5350","middle",8),["Gain potentiel trop faible","Stop plus grand que la cible","Refuser meme si l'entree est jolie"], True)}
</div></section>
<section class="card" id="exercice-stop-tp"><header><h2>Mini exercice : ecris le plan avant l'ordre</h2><span>Pratique</span></header><div class="academy-grid"><div class="academy-card"><h3>Question 1</h3><p>Ou le trade est-il faux ? Reponds avec une structure, pas avec un montant.</p></div><div class="academy-card"><h3>Question 2</h3><p>Quelle liquidite paie TP1 ? Quelle liquidite paie TP2 ?</p></div><div class="academy-card"><h3>Question 3</h3><p>Si TP1 est atteint, que fais-tu : partiel, BE, maintien ? La regle doit etre decidee avant.</p></div></div></section>
"""
    return page_shell("ICT Atlas - Fondations stop et TP", "Savoir ou le trade est faux, ou il paie, et quand refuser.", ["stop", "invalidation", "TP"], body)


def remove_existing(soup, section_id):
    old = soup.find(id=section_id)
    if old:
        old.decompose()


def insert_after_note(path, html, section_id):
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    remove_existing(soup, section_id)
    target = soup.find("section", class_="page-note") or soup.find("div", class_="page-meta-dashboard")
    fragment = BeautifulSoup(html, "html.parser")
    if target:
        target.insert_after(fragment)
    else:
        main = soup.find("main", class_="page")
        if main:
            main.insert(1, fragment)
    path.write_text(str(soup), encoding="utf-8")


def update_home_order():
    path = ROOT / "index.html"
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    order = [
        "02. Modèle mental",
        "03. Parcours",
        "04. Mécanique",
        "05. Langage ICT en contexte",
        "06. Liquidité et déplacement",
        "07. Lire la liquidité",
        "08. Construire l'entrée",
        "09. Stop, invalidation et TP",
        "10. Trend/range/transitions",
        "11. Concept/plan",
        "12. Où/quand : Premium/Discount + Kill Zones",
        "13. Fondations de décision",
        "14. Top-down multi-timeframe",
        "15. Setups cœur",
        "16. Graphique réel",
        "17. Variantes",
        "18. Failures",
    ]
    for card in soup.select(".home-card"):
        title = card.find("h3")
        if not title or "Ordre recommandé" not in title.get_text(" ", strip=True):
            continue
        paragraphs = card.find_all("p")
        if paragraphs:
            paragraphs[0].string = (
                "La progression part de la mécanique, solidifie le trajet Liquidité -> "
                "Entrée -> Stop -> TP, puis seulement ensuite passe aux filtres et setups."
            )
        ul = card.find("ul") or soup.new_tag("ul")
        ul.clear()
        for item in order:
            li = soup.new_tag("li")
            li.string = item
            ul.append(li)
        if not ul.parent:
            card.append(ul)
        paragraphs = card.find_all("p")
        if len(paragraphs) > 1:
            paragraphs[-1].string = (
                "Le glossaire reste hors numérotation : garde-le ouvert en panneau "
                "quand un sigle bloque la lecture."
            )
        break
    path.write_text(str(soup), encoding="utf-8")


def enrich_existing_pages():
    bridge = f"""<section class="card" id="v54-pont-fondations"><header><h2>Pont fondation : de la liquidite au plan complet</h2><span>V54</span></header><div class="academy-grid"><div class="academy-card"><h3>1. Lire la liquidite</h3><p>La prochaine lecon classe les zones : externe, interne, faible, propre ou deja consommee.</p><p><a class="pill" href="27-fondations-liquidite.html">Lire la liquidite</a></p></div><div class="academy-card"><h3>2. Construire l'entree</h3><p>Ensuite, tu relieras sweep, rejet, displacement, MSS et FVG a une raison d'entrer.</p><p><a class="pill" href="28-fondations-entree.html">Construire l'entree</a></p></div><div class="academy-card"><h3>3. Placer stop et TP</h3><p>Enfin, tu apprendras ou le trade est faux et quelles liquidites paient TP1 et TP2.</p><p><a class="pill" href="29-fondations-stop-tp.html">Stop et TP</a></p></div></div></section>"""
    insert_after_note(ROOT / "21-liquidite-deplacement.html", bridge, "v54-pont-fondations")

    mechanics = f"""<section class="card" id="v54-mecanique-visuelle"><header><h2>Fondation visuelle : pourquoi ordres, stops et mitigation creent les setups</h2><span>V54</span></header>
{chart_base(arrow_marker("arr-mech") + '<rect fill="#0d1b2a" height="64" rx="12" stroke="#4fc3f7" width="150" x="70" y="145"></rect><rect fill="#0d1b2a" height="64" rx="12" stroke="#26a69a" width="150" x="270" y="145"></rect><rect fill="#0d1b2a" height="64" rx="12" stroke="#ffb300" width="150" x="470" y="145"></rect><rect fill="#0d1b2a" height="64" rx="12" stroke="#4fc3f7" width="150" x="670" y="145"></rect>' + label(145,171,"Stops", "#4fc3f7") + label(345,171,"Absorption", "#26a69a") + label(545,171,"Deplacement", "#ffb300") + label(745,171,"Mitigation", "#4fc3f7") + '<line marker-end="url(#arr-mech)" stroke="#4fc3f7" stroke-width="1.8" x1="220" x2="270" y1="176" y2="176"></line><line marker-end="url(#arr-mech)" stroke="#4fc3f7" stroke-width="1.8" x1="420" x2="470" y1="176" y2="176"></line><line marker-end="url(#arr-mech)" stroke="#4fc3f7" stroke-width="1.8" x1="620" x2="670" y1="176" y2="176"></line>' + label(480,288,"Les formes ICT viennent de contraintes d'execution, pas d'un dessin magique.", "#d9e6f2", "middle", 13))}
<div class="rule-block"><strong>Regle :</strong> un FVG ou un OB devient plus clair quand tu sais quelle contrainte mecanique l'a produit.</div></section>"""
    insert_after_note(ROOT / "11-mecanique-marches.html", mechanics, "v54-mecanique-visuelle")

    risk = f"""<section class="card" id="v54-risque-plan-visuel"><header><h2>Risque visuel : entree, stop, TP1 et TP2 en une seule lecture</h2><span>V54</span></header>
{chart_base(candles("105,258 160,224 215,246 270,282 325,236 380,178 435,144 490,172 545,128 600,150 660,108 720,132 805,86") + '<line stroke="#ef5350" stroke-dasharray="6 4" x1="90" x2="850" y1="298" y2="298"></line><line stroke="#4fc3f7" stroke-dasharray="6 4" x1="90" x2="850" y1="132" y2="132"></line><line stroke="#4fc3f7" stroke-dasharray="6 4" x1="90" x2="850" y1="86" y2="86"></line>' + dot(446,178,"#26a69a") + dot(720,132,"#4fc3f7") + dot(805,86,"#4fc3f7") + pill(404,186,90,"entree","#26a69a") + pill(250,306,120,"stop logique","#ef5350") + pill(686,140,76,"TP1","#4fc3f7") + pill(770,54,76,"TP2","#4fc3f7") + label(480,335,"Le sizing vient apres le stop logique, jamais avant.", "#d9e6f2", "middle", 12))}
<div class="rule-block"><strong>Regle :</strong> calcule le risque seulement apres avoir trouve l'invalidation structurelle.</div></section>"""
    insert_after_note(ROOT / "12-gestion-risque.html", risk, "v54-risque-plan-visuel")

    checklist = f"""<section class="card" id="v54-checklist-liquidite-entree-tp"><header><h2>Checklist finale : Liquidite - Entree - Stop - TP</h2><span>V54</span></header><div class="academy-grid"><div class="academy-card"><h3>Liquidite</h3><p>Quelle zone attire le prix ? Est-elle externe, interne, propre, faible ou deja consommee ?</p></div><div class="academy-card"><h3>Entree</h3><p>Quelle sequence autorise l'entree : sweep, rejet, displacement, MSS, FVG/CE/OB ?</p></div><div class="academy-card"><h3>Stop</h3><p>Ou le scenario est-il faux ? Le stop est-il protege par une structure claire ?</p></div><div class="academy-card"><h3>TP</h3><p>Quelle liquidite paie TP1 ? Quelle liquidite paie TP2 ? Le trajet justifie-t-il le risque ?</p></div></div><div class="rule-block"><strong>Regle :</strong> si une case manque, le trade devient un exercice d'observation ou un no trade.</div></section>"""
    insert_after_note(ROOT / "09-synthese.html", checklist, "v54-checklist-liquidite-entree-tp")

    home = f"""<section class="card" id="v54-home-fondations"><header><h2>V54 — Nouveau module fondation : Liquidite - Entree - Stop - TP</h2><span>Fondations</span></header><div class="academy-grid"><div class="academy-card"><h3>07. Lire la liquidite</h3><p>Identifier BSL/SSL, PDH/PDL, Asia High/Low, liquidite interne/externe et niveaux deja consommes.</p><p><a class="pill" href="27-fondations-liquidite.html">Commencer</a></p></div><div class="academy-card"><h3>08. Construire l'entree</h3><p>Relier sweep, rejet, displacement, MSS et FVG/CE/OB a une raison d'entrer.</p><p><a class="pill" href="28-fondations-entree.html">Continuer</a></p></div><div class="academy-card"><h3>09. Stop et TP</h3><p>Placer l'invalidation, le stop logique, TP1 et TP2 selon les liquidites restantes.</p><p><a class="pill" href="29-fondations-stop-tp.html">Finaliser</a></p></div></div><div class="rule-block"><strong>Nouveau flux :</strong> mecanique - langage - deplacement - liquidite - entree - stop/TP - environnement - setups.</div></section>"""
    insert_after_note(ROOT / "index.html", home, "v54-home-fondations")
    update_home_order()

    index = f"""<section class="card" id="index-v54-fondations"><header><h2>Index V54 — Fondations Liquidite - Entree - Stop - TP</h2><span>Progression</span></header><div class="academy-grid"><div class="academy-card"><h3>Liquidite cible</h3><p><a href="27-fondations-liquidite.html#abc-liquidite-cible">Cible propre, faible ou deja consommee</a></p></div><div class="academy-card"><h3>Entree causale</h3><p><a href="28-fondations-entree.html#abc-entree">Entree complete, prematuree ou hors contexte</a></p></div><div class="academy-card"><h3>Stop logique</h3><p><a href="29-fondations-stop-tp.html#abc-stop">Stop structurel, serre ou arbitraire</a></p></div><div class="academy-card"><h3>TP logique</h3><p><a href="29-fondations-stop-tp.html#tp-abc">TP sur liquidite, trop ambitieux ou trop proche</a></p></div></div><div class="rule-block"><strong>Regle :</strong> Ces quatre familles servent a transformer un schema en decision complete.</div></section>"""
    insert_after_note(ROOT / "15-index-concepts.html", index, "index-v54-fondations")


def main():
    (ROOT / "27-fondations-liquidite.html").write_text(liquidity_lesson(), encoding="utf-8")
    (ROOT / "28-fondations-entree.html").write_text(entry_lesson(), encoding="utf-8")
    (ROOT / "29-fondations-stop-tp.html").write_text(stop_tp_lesson(), encoding="utf-8")
    enrich_existing_pages()


if __name__ == "__main__":
    main()
