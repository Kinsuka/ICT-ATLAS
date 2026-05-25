from pathlib import Path
from bs4 import BeautifulSoup


def fragment(soup, html):
    wrapper = BeautifulSoup(html, "html.parser")
    nodes = [node for node in wrapper.contents if getattr(node, "name", None)]
    return nodes


def remove_existing(soup, element_id):
    old = soup.find(id=element_id)
    if old:
        old.decompose()


def insert_after_meta(path_name, element_id, html):
    path = Path(path_name)
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    remove_existing(soup, element_id)
    meta = soup.find("div", class_="page-meta-dashboard")
    target = meta or soup.find("div", class_="hero")
    nodes = fragment(soup, html)
    for node in reversed(nodes):
        target.insert_after(node)
    path.write_text(str(soup), encoding="utf-8")


def insert_before_bottom(path_name, element_id, html):
    path = Path(path_name)
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    remove_existing(soup, element_id)
    bottom = soup.find("nav", class_="lesson-bottom-nav")
    nodes = fragment(soup, html)
    for node in nodes:
        bottom.insert_before(node)
    path.write_text(str(soup), encoding="utf-8")


def update_home():
    path = Path("index.html")
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    links = soup.find("div", class_="section-links")
    if links and not links.find("a", href="22-structure-trend-range.html"):
        ref = links.find("a", href="21-liquidite-deplacement.html")
        a = soup.new_tag("a", href="22-structure-trend-range.html", **{"class": "section-link"})
        h = soup.new_tag("h3")
        h.string = "Trend, range et transitions"
        p = soup.new_tag("p")
        p.string = "Filtrer les setups selon l'environnement de marche."
        a.append(h)
        a.append(p)
        if ref:
            ref.insert_after(a)
        else:
            links.append(a)
    order = soup.find("div", class_="home-card")
    for h3 in soup.find_all("h3"):
        if h3.get_text(strip=True) == "Ordre recommandé":
            ul = h3.find_next("ul")
            if ul and "Trend/range" not in ul.get_text(" ", strip=True):
                items = [li.get_text(" ", strip=True) for li in ul.find_all("li")]
                ul.clear()
                new_items = [
                    "02. Modèle mental",
                    "03. Parcours",
                    "04. Mécanique",
                    "05. Liquidité et déplacement",
                    "06. Trend/range/transitions",
                    "07. Concept/plan",
                    "08. Fondations",
                    "09. Setups cœur",
                    "10. Graphique réel",
                    "11. Variantes",
                    "12. Failures",
                ]
                for item in new_items:
                    li = soup.new_tag("li")
                    li.string = item
                    ul.append(li)
            break
    path.write_text(str(soup), encoding="utf-8")


def update_parcours():
    path = Path("01-parcours.html")
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    for h3 in soup.find_all("h3"):
        text = h3.get_text(" ", strip=True)
        if "Semaine 2" in text and "Mécanique" in text:
            ul = h3.find_next("ul")
            if ul and "trend/range" not in ul.get_text(" ", strip=True).lower():
                li = soup.new_tag("li")
                li.string = "Ajouter le filtre trend/range/transitions avant le vocabulaire ICT."
                ul.append(li)
            break
    path.write_text(str(soup), encoding="utf-8")


FONDATIONS = """
<section class="card" id="filtre-environnement-trend-range">
  <header><h2>Filtre d'environnement : trend, range ou transition ?</h2><span>Market structure</span></header>
  <div class="chart">
    <svg height="auto" viewBox="0 0 960 360" width="100%" xmlns="http://www.w3.org/2000/svg">
      <rect fill="#081222" height="360" width="960"/>
      <rect fill="#0d1b2a" height="70" rx="12" stroke="#4fc3f7" width="210" x="375" y="40"/>
      <text fill="#d9e6f2" font-size="13" font-weight="900" text-anchor="middle" x="480" y="68">Environnement</text>
      <text fill="#8fa5ba" font-size="10.5" font-weight="700" text-anchor="middle" x="480" y="88">avant tout setup</text>
      <rect fill="#0d1b2a" height="96" rx="12" stroke="#26a69a" width="230" x="80" y="190"/>
      <rect fill="#0d1b2a" height="96" rx="12" stroke="#4fc3f7" width="230" x="365" y="190"/>
      <rect fill="#0d1b2a" height="96" rx="12" stroke="#ffb300" width="230" x="650" y="190"/>
      <text fill="#26a69a" font-size="13" font-weight="900" text-anchor="middle" x="195" y="218">Trend</text>
      <text fill="#d9e6f2" font-size="11" font-weight="750" text-anchor="middle" x="195" y="242">Pullback dans le flux</text>
      <text fill="#8fa5ba" font-size="10" font-weight="700" text-anchor="middle" x="195" y="262">FVG / OB / continuation</text>
      <text fill="#4fc3f7" font-size="13" font-weight="900" text-anchor="middle" x="480" y="218">Range</text>
      <text fill="#d9e6f2" font-size="11" font-weight="750" text-anchor="middle" x="480" y="242">Bords et failed breakout</text>
      <text fill="#8fa5ba" font-size="10" font-weight="700" text-anchor="middle" x="480" y="262">centre = prudence</text>
      <text fill="#ffb300" font-size="13" font-weight="900" text-anchor="middle" x="765" y="218">Transition</text>
      <text fill="#d9e6f2" font-size="11" font-weight="750" text-anchor="middle" x="765" y="242">Attendre confirmation</text>
      <text fill="#8fa5ba" font-size="10" font-weight="700" text-anchor="middle" x="765" y="262">sweep + displacement + MSS</text>
      <line stroke="#4fc3f7" stroke-width="1.6" x1="435" x2="195" y1="110" y2="185"/>
      <line stroke="#4fc3f7" stroke-width="1.6" x1="480" x2="480" y1="110" y2="185"/>
      <line stroke="#4fc3f7" stroke-width="1.6" x1="525" x2="765" y1="110" y2="185"/>
    </svg>
  </div>
  <div class="academy-grid">
    <div class="academy-card"><h3>Pourquoi ce filtre change tout</h3><p>Un FVG ou un MSS ne porte pas la meme information dans une tendance claire, dans une range equilibree ou pendant une transition. Le setup vient apres le diagnostic d'environnement.</p></div>
    <div class="academy-card"><h3>Decision pratique</h3><p>En trend, on favorise les pullbacks dans le flux. En range, on prefere les bords et les failed breakouts. En transition, on attend une preuve de changement de controle.</p></div>
  </div>
  <div class="rule-block"><strong>Regle :</strong> Si tu ne sais pas dire trend, range ou transition, tu n'as pas encore le droit de juger la qualite du setup.</div>
</section>
"""

SETUPS = """
<section class="card" id="templates-market-structure-setups">
  <header><h2>Templates de market structure appliques aux setups ICT</h2><span>Trend/range</span></header>
  <div class="academy-grid">
    <div class="academy-card"><h3>Pullback de tendance</h3><p>Contexte favorable aux FVG et OB dans le sens du flux. Le pullback doit etre plus faible que l'impulsion qui l'a precede.</p></div>
    <div class="academy-card"><h3>Failure test</h3><p>Sweep d'un niveau visible, rejet, displacement inverse et MSS. C'est une structure proche du retournement apres absorption.</p></div>
    <div class="academy-card"><h3>Breakout accepte</h3><p>Expansion hors range, maintien hors de la zone, premier pullback defendu. Le breakout doit montrer acceptation, pas seulement une meche.</p></div>
    <div class="academy-card"><h3>Failed breakout</h3><p>Le prix sort, declenche la liquidite, puis reintegre la range. Le retour dans la zone annule souvent le breakout initial.</p></div>
  </div>
  <div class="rule-block"><strong>Regle :</strong> Un setup coeur devient plus robuste quand il appartient a un template de structure identifiable.</div>
</section>
"""

VARIANTES = """
<section class="card" id="faux-amis-trend-range">
  <header><h2>Faux amis : quand la structure contredit le signal</h2><span>Market structure</span></header>
  <div class="chart">
    <svg height="auto" viewBox="0 0 960 430" width="100%" xmlns="http://www.w3.org/2000/svg">
      <rect fill="#081222" height="430" width="960"/>
      <rect fill="#0d1b2a" height="145" rx="12" stroke="#243e5e" width="390" x="70" y="56"/>
      <rect fill="#0d1b2a" height="145" rx="12" stroke="#243e5e" width="390" x="500" y="56"/>
      <rect fill="#0d1b2a" height="145" rx="12" stroke="#243e5e" width="390" x="70" y="230"/>
      <rect fill="#0d1b2a" height="145" rx="12" stroke="#243e5e" width="390" x="500" y="230"/>
      <polyline fill="none" points="100,150 150,112 205,136 260,100 318,134 370,98 430,112" stroke="#ef5350" stroke-width="2.1"/>
      <text fill="#ef5350" font-size="12" font-weight="900" x="102" y="82">Breakout sans acceptation</text>
      <text fill="#8fa5ba" font-size="10" font-weight="750" x="102" y="185">Sortie rapide puis retour dans la range.</text>
      <polyline fill="none" points="530,170 585,100 640,126 700,196 760,250 835,205" stroke="#ef5350" stroke-width="2.1"/>
      <text fill="#ef5350" font-size="12" font-weight="900" x="532" y="82">Pullback trop violent</text>
      <text fill="#8fa5ba" font-size="10" font-weight="750" x="532" y="185">La correction attaque le trend au lieu de respirer.</text>
      <polyline fill="none" points="100,310 155,260 210,324 270,262 330,322 430,284" stroke="#ffb300" stroke-width="2.1"/>
      <text fill="#ffb300" font-size="12" font-weight="900" x="102" y="256">Range trop equilibree</text>
      <text fill="#8fa5ba" font-size="10" font-weight="750" x="102" y="359">Le centre de range donne peu d'avantage.</text>
      <polyline fill="none" points="530,335 590,286 650,222 710,184 770,112 835,150" stroke="#ef5350" stroke-width="2.1"/>
      <text fill="#ef5350" font-size="12" font-weight="900" x="532" y="256">Climax confondu avec continuation</text>
      <text fill="#8fa5ba" font-size="10" font-weight="750" x="532" y="359">Entrer tard apres expansion verticale augmente le risque.</text>
    </svg>
  </div>
  <div class="rule-block"><strong>Regle :</strong> La structure peut invalider un signal visuellement propre. Le contexte prime sur la forme.</div>
</section>
"""

PREUVE = """
<section class="card" id="edge-pattern-preuve">
  <header><h2>Beau pattern ou edge prouve ?</h2><span>Statistique</span></header>
  <div class="chart">
    <svg height="auto" viewBox="0 0 960 330" width="100%" xmlns="http://www.w3.org/2000/svg">
      <rect fill="#081222" height="330" width="960"/>
      <defs><marker id="arrow-proof-v47" markerHeight="10" markerWidth="10" orient="auto" refX="8" refY="3"><path d="M0,0 L0,6 L9,3 z" fill="#4fc3f7"/></marker></defs>
      <rect fill="#0d1b2a" height="64" rx="12" stroke="#4fc3f7" width="150" x="60" y="135"/>
      <rect fill="#0d1b2a" height="64" rx="12" stroke="#4fc3f7" width="150" x="250" y="135"/>
      <rect fill="#0d1b2a" height="64" rx="12" stroke="#4fc3f7" width="150" x="440" y="135"/>
      <rect fill="#0d1b2a" height="64" rx="12" stroke="#ffb300" width="150" x="630" y="135"/>
      <rect fill="#0d1b2a" height="64" rx="12" stroke="#26a69a" width="150" x="820" y="135"/>
      <text fill="#d9e6f2" font-size="11.5" font-weight="900" text-anchor="middle" x="135" y="162">Pattern</text>
      <text fill="#8fa5ba" font-size="9.5" font-weight="700" text-anchor="middle" x="135" y="180">visuel</text>
      <text fill="#d9e6f2" font-size="11.5" font-weight="900" text-anchor="middle" x="325" y="162">Regles fixes</text>
      <text fill="#8fa5ba" font-size="9.5" font-weight="700" text-anchor="middle" x="325" y="180">hypothese</text>
      <text fill="#d9e6f2" font-size="11.5" font-weight="900" text-anchor="middle" x="515" y="162">Echantillon</text>
      <text fill="#8fa5ba" font-size="9.5" font-weight="700" text-anchor="middle" x="515" y="180">50-100 cas</text>
      <text fill="#d9e6f2" font-size="11.5" font-weight="900" text-anchor="middle" x="705" y="162">Expectancy</text>
      <text fill="#8fa5ba" font-size="9.5" font-weight="700" text-anchor="middle" x="705" y="180">R moyen</text>
      <text fill="#d9e6f2" font-size="11.5" font-weight="900" text-anchor="middle" x="895" y="162">Decision</text>
      <text fill="#8fa5ba" font-size="9.5" font-weight="700" text-anchor="middle" x="895" y="180">garder/reduire</text>
      <line marker-end="url(#arrow-proof-v47)" stroke="#4fc3f7" stroke-width="1.6" x1="214" x2="244" y1="167" y2="167"/>
      <line marker-end="url(#arrow-proof-v47)" stroke="#4fc3f7" stroke-width="1.6" x1="404" x2="434" y1="167" y2="167"/>
      <line marker-end="url(#arrow-proof-v47)" stroke="#4fc3f7" stroke-width="1.6" x1="594" x2="624" y1="167" y2="167"/>
      <line marker-end="url(#arrow-proof-v47)" stroke="#4fc3f7" stroke-width="1.6" x1="784" x2="814" y1="167" y2="167"/>
      <text fill="#f6aa1c" font-size="13" font-weight="900" text-anchor="middle" x="480" y="82">La beaute du graphique ne prouve pas l'avantage statistique</text>
    </svg>
  </div>
  <div class="academy-grid">
    <div class="academy-card"><h3>Qualite visuelle</h3><p>Elle sert a definir une hypothese propre : contexte, setup, entree, stop, cible et exclusions.</p></div>
    <div class="academy-card"><h3>Edge reel</h3><p>Il apparait seulement si l'echantillon montre une asymetrie exploitable apres frais, erreurs et regimes de marche.</p></div>
  </div>
  <div class="rule-block"><strong>Regle :</strong> Un setup est autorise au risque seulement quand sa definition produit une expectancy mesurable.</div>
</section>
"""

SYNTHESE = """
<section class="card" id="synthese-environnement-edge">
  <header><h2>Checklist ajoutee : environnement, structure et edge</h2><span>Validation V47</span></header>
  <div class="academy-grid">
    <div class="academy-card"><h3>Environnement</h3><p>Le marche est classe avant l'entree : trend, range ou transition. Sans classification, le setup reste incomplet.</p></div>
    <div class="academy-card"><h3>Setup adapte</h3><p>Pullback de tendance, bord de range, failed breakout ou transition confirmee : le type de trade doit correspondre au regime.</p></div>
    <div class="academy-card"><h3>Preuve statistique</h3><p>Le setup possede un echantillon documente et une expectancy positive ou une raison claire de reduction.</p></div>
    <div class="academy-card"><h3>Invalidation</h3><p>La condition qui annule le trade est connue avant l'ordre : reprise de range, perte de structure, DOL atteint ou momentum contraire.</p></div>
  </div>
  <div class="rule-block"><strong>Regle :</strong> La sequence finale devient : environnement -> liquidite -> displacement -> setup -> risque -> preuve -> execution.</div>
</section>
"""

INDEX_SECTION = """
<section class="card" id="index-v47-market-structure">
  <header><h2>Index V47 - Market structure et transitions</h2><span>Recherche rapide</span></header>
  <div class="academy-grid">
    <div class="academy-card"><h3>Trend / Range</h3><p><a href="22-structure-trend-range.html#cycle-fonctionnel">Cycle fonctionnel</a> - <a href="22-structure-trend-range.html#range-equilibre">Range comme equilibre</a></p></div>
    <div class="academy-card"><h3>Transitions</h3><p><a href="22-structure-trend-range.html#interfaces-trend-range">Interfaces trend/range</a> - <a href="22-structure-trend-range.html#mapping-ict-environnement">Mapping ICT</a></p></div>
    <div class="academy-card"><h3>Pullbacks</h3><p><a href="22-structure-trend-range.html#pullback-qualite">Pullback A/B/C</a> - <a href="05-variantes.html#faux-amis-trend-range">Faux amis</a></p></div>
    <div class="academy-card"><h3>Edge</h3><p><a href="22-structure-trend-range.html#edge-hypothese">Hypothese mesurable</a> - <a href="19-preuve-statistique.html#edge-pattern-preuve">Beau pattern ou edge</a></p></div>
  </div>
  <div class="rule-block"><strong>Regle :</strong> Utilise cet index pour relier les setups ICT a leur environnement de marche.</div>
</section>
"""


def main():
    insert_after_meta("03-fondations.html", "filtre-environnement-trend-range", FONDATIONS)
    insert_after_meta("04-setups-core.html", "templates-market-structure-setups", SETUPS)
    insert_before_bottom("05-variantes.html", "faux-amis-trend-range", VARIANTES)
    insert_after_meta("19-preuve-statistique.html", "edge-pattern-preuve", PREUVE)
    insert_after_meta("09-synthese.html", "synthese-environnement-edge", SYNTHESE)
    insert_before_bottom("15-index-concepts.html", "index-v47-market-structure", INDEX_SECTION)
    update_home()
    update_parcours()


if __name__ == "__main__":
    main()
