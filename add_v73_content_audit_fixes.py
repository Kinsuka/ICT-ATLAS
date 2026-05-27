from pathlib import Path

from bs4 import BeautifulSoup


ROOT = Path(".")


def remove_existing(soup, section_id):
    old = soup.find(id=section_id)
    if old:
        old.decompose()


def insert_after_id(path, section_id, anchor_id, html):
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    remove_existing(soup, section_id)
    fragment = BeautifulSoup(html, "html.parser")
    anchor = soup.find(id=anchor_id)
    if anchor:
        anchor.insert_after(fragment)
    else:
        main = soup.find("main", class_="page")
        if main:
            main.insert(3, fragment)
    path.write_text(str(soup), encoding="utf-8")


def add_mechanics_depth():
    html = """
    <section class="card" id="v73-retail-institutionnel">
      <header><h2>Retail vs institutionnel : pourquoi la liquidité est nécessaire</h2><span>Socle</span></header>
      <p>La différence n’est pas morale : elle est mécanique. Un trader retail peut entrer avec une petite taille sans déplacer le marché. Un acteur qui doit exécuter une taille importante ne peut pas simplement cliquer au marché sans impacter son propre prix d’exécution. Il a besoin de contreparties, donc de zones où beaucoup d’ordres sont regroupés.</p>
      <div class="chart ob-wide-chart">
        <svg aria-label="Retail institutionnel et liquidité" role="img" viewBox="0 0 1120 500">
          <defs>
            <marker id="mech-liq-arrow" markerHeight="8" markerWidth="8" orient="auto" refX="7" refY="4"><path d="M0 0 L8 4 L0 8 Z" fill="#53d6e9"></path></marker>
          </defs>
          <rect fill="#081222" height="460" rx="24" stroke="#26394c" stroke-width="2" width="1080" x="20" y="20"></rect>
          <g stroke="#19304a" stroke-width="1">
            <line x1="80" x2="1040" y1="110" y2="110"></line>
            <line x1="80" x2="1040" y1="200" y2="200"></line>
            <line x1="80" x2="1040" y1="290" y2="290"></line>
            <line x1="80" x2="1040" y1="380" y2="380"></line>
          </g>
          <rect fill="#0b1829" height="104" rx="16" stroke="#26394c" stroke-width="2" width="300" x="92" y="74"></rect>
          <rect fill="#0b1829" height="104" rx="16" stroke="#26394c" stroke-width="2" width="300" x="728" y="74"></rect>
          <text fill="#4fd37b" font-size="20" font-weight="900" text-anchor="middle" x="242" y="112">Retail</text>
          <text fill="#53d6e9" font-size="20" font-weight="900" text-anchor="middle" x="878" y="112">Institutionnel</text>
          <text fill="#b8c7d6" font-size="14" font-weight="800" text-anchor="middle" x="242" y="142">petite taille, faible impact</text>
          <text fill="#b8c7d6" font-size="14" font-weight="800" text-anchor="middle" x="878" y="142">taille importante, besoin de contreparties</text>
          <line stroke="#ef5350" stroke-dasharray="9 8" stroke-width="3" x1="104" x2="1016" y1="314" y2="314"></line>
          <text fill="#ef5350" font-size="17" font-weight="900" x="112" y="340">SSL : stops longs + vendeurs breakout + TP de shorts</text>
          <path d="M140 214 C222 184 308 216 386 248 S530 346 650 292 S800 228 972 184" fill="none" stroke="#8fa5ba" stroke-width="5"></path>
          <circle cx="650" cy="314" fill="#081222" r="10" stroke="#ef5350" stroke-width="4"></circle>
          <path d="M650 314 C720 248 788 216 874 190" fill="none" marker-end="url(#mech-liq-arrow)" stroke="#53d6e9" stroke-width="4"></path>
          <rect fill="rgba(83,214,233,0.13)" height="74" rx="12" stroke="#53d6e9" stroke-width="3" width="312" x="700" y="240"></rect>
          <text fill="#53d6e9" font-size="17" font-weight="900" text-anchor="middle" x="856" y="270">La zone fournit de la contrepartie</text>
          <text fill="#b8c7d6" font-size="14" font-weight="800" text-anchor="middle" x="856" y="294">le prix peut ensuite être rejeté ou continuer</text>
          <text fill="#e6f4ff" font-size="17" font-weight="900" text-anchor="middle" x="560" y="430">Un sweep n’est pas magique : c’est une zone où des ordres latents deviennent exécutables.</text>
        </svg>
      </div>
      <div class="academy-grid">
        <div class="academy-card"><h3>Pourquoi les stops comptent</h3><p>Un stop déclenché devient souvent un ordre au marché. Sous un low, des stops longs ajoutent du flux vendeur ; au-dessus d’un high, des stops shorts ajoutent du flux acheteur.</p></div>
        <div class="academy-card"><h3>Pourquoi le prix “cherche” les niveaux évidents</h3><p>Les highs/lows visibles regroupent stops, entrées breakout et prises de profit. Ce regroupement rend l’exécution plus facile qu’au milieu d’une zone vide.</p></div>
        <div class="academy-card"><h3>Pourquoi le sweep peut rejeter</h3><p>Si la liquidité déclenchée est absorbée par un acteur opposé, le prix peut réintégrer violemment. La réaction après la prise vaut plus que la prise elle-même.</p></div>
        <div class="academy-card"><h3>Pourquoi le sweep peut continuer</h3><p>Si les ordres déclenchés nourrissent le même flux et qu’il n’y a pas d’absorption opposée, le mouvement peut accepter la cassure et poursuivre.</p></div>
      </div>
      <div class="rule-block"><strong>Règle :</strong> ICT devient crédible quand chaque concept reste relié à une contrainte observable : où sont les ordres, qui est forcé d’agir, et quelle réaction suit l’exécution ?</div>
    </section>
    """
    insert_after_id(ROOT / "11-mecanique-marches.html", "v73-retail-institutionnel", "bridge-mecanique-debutant", html)


def add_parcours_psychology_bridge():
    html = """
    <section class="card" id="v73-psychologie-avant-replay">
      <header><h2>Avant le replay : protège ton protocole mental</h2><span>Jeu mental</span></header>
      <p>Le travail technique ne suffit pas si tu changes de règle après deux pertes ou si tu cours après un mouvement raté. Avant de commencer les sessions replay sérieuses, lis la leçon sur la psychologie : elle te donne les règles “si/alors” pour garder le plan intact.</p>
      <div class="section-links">
        <a class="section-link" href="26-psychologie-trader.html"><h3>Lire la leçon psychologie</h3><p>Revenge trade, FOMO, tilt, euphorie, série de pertes et règles de pause.</p></a>
        <a class="section-link" href="30-replay-lab.html"><h3>Ensuite seulement : Replay Lab</h3><p>Décider sans connaître le futur, puis journaliser la qualité de décision.</p></a>
      </div>
    </section>
    """
    insert_after_id(ROOT / "01-parcours.html", "v73-psychologie-avant-replay", "site-map", html)


def add_mss_timeframe_section():
    html = """
    <section class="card" id="v73-mss-timeframes">
      <header><h2>Quel swing doit casser ? La réponse vient du timeframe de décision</h2><span>Timeframes</span></header>
      <p>La confusion no. 1 sur le MSS vient du mauvais niveau de zoom. Un micro-swing M1 peut aider à affiner une entrée, mais il ne valide pas à lui seul une narrative Daily ou H1.</p>
      <div class="academy-grid">
        <div class="academy-card"><h3>Daily / H4</h3><p>Ils donnent le biais large, les liquidités importantes et les zones HTF. On ne demande pas au M1 de contredire seul ce contexte.</p></div>
        <div class="academy-card"><h3>H1 / M15</h3><p>Pour une session intraday, ce sont souvent les timeframes de décision : le MSS doit casser un swing visible à ce niveau, pas un bruit minuscule.</p></div>
        <div class="academy-card"><h3>M5 / M1</h3><p>Ils affinent l’exécution : entrée, stop plus précis, micro-retour. Ils ne doivent pas inventer un changement de contrôle HTF.</p></div>
        <div class="academy-card wide"><h3>Exemple concret</h3><p>Si ton top-down est Daily → H1 → M15, alors un MSS d’entrée doit au minimum casser un swing M15/H1 lisible selon ton plan. Une cassure M1 contre un H1 encore propre reste une alerte, pas une confirmation majeure.</p></div>
      </div>
      <div class="rule-block"><strong>Règle :</strong> le swing cassé doit appartenir au timeframe qui porte ta décision. Le timeframe inférieur sert à affiner, pas à justifier ce que le contexte supérieur refuse.</div>
    </section>
    """
    insert_after_id(ROOT / "33-mss-changement-controle.html", "v73-mss-timeframes", "mss-checklist", html)


def add_ob_bearish_mirror():
    html = """
    <section class="card" id="v73-ob-bearish-mirror">
      <header><h2>Mirror bearish : la logique s’inverse point par point</h2><span>Symétrie</span></header>
      <p>Le raisonnement ne change pas quand l’Order Block est vendeur. On ne cherche pas “une bougie verte” au hasard : on cherche une séquence complète avec BSL prise, rejet, displacement baissier, retour contrôlé dans la zone source, puis cible sous le prix.</p>
      <div class="chart ob-wide-chart">
        <svg aria-label="Anatomie bearish d'un Order Block valide" role="img" viewBox="0 0 1120 520">
          <defs>
            <marker id="ob-bear-arrow" markerHeight="8" markerWidth="8" orient="auto" refX="7" refY="4"><path d="M0 0 L8 4 L0 8 Z" fill="#ef5350"></path></marker>
          </defs>
          <rect fill="#081222" height="480" rx="26" stroke="#26394c" stroke-width="2" width="1080" x="20" y="20"></rect>
          <g stroke="#19304a" stroke-width="1">
            <line x1="80" x2="1040" y1="110" y2="110"></line>
            <line x1="80" x2="1040" y1="200" y2="200"></line>
            <line x1="80" x2="1040" y1="290" y2="290"></line>
            <line x1="80" x2="1040" y1="380" y2="380"></line>
          </g>
          <line stroke="#4fd37b" stroke-dasharray="10 10" stroke-width="3" x1="92" x2="1005" y1="120" y2="120"></line>
          <text fill="#4fd37b" font-size="17" font-weight="800" x="102" y="98">BSL prise</text>
          <line stroke="#ef5350" stroke-dasharray="10 10" stroke-width="3" x1="92" x2="1005" y1="414" y2="414"></line>
          <text fill="#ef5350" font-size="17" font-weight="900" x="846" y="442">DOL / SSL suivante</text>
          <rect fill="rgba(248,194,78,0.16)" height="92" rx="10" stroke="#f8c24e" stroke-width="2" width="92" x="354" y="138"></rect>
          <text fill="#f8c24e" font-size="18" font-weight="900" text-anchor="middle" x="400" y="260">OB bearish</text>
          <path d="M118 284 C184 238 264 204 342 154 S440 86 512 156 C574 216 640 276 722 326 S846 394 982 408" fill="none" stroke="#ef5350" stroke-width="5"></path>
          <g>
            <rect fill="#4fd37b" height="64" rx="5" width="20" x="136" y="246"></rect><line stroke="#4fd37b" stroke-width="5" x1="146" x2="146" y1="220" y2="334"></line>
            <rect fill="#4fd37b" height="58" rx="5" width="20" x="246" y="198"></rect><line stroke="#4fd37b" stroke-width="5" x1="256" x2="256" y1="170" y2="286"></line>
            <rect fill="#4fd37b" height="72" rx="5" width="22" x="382" y="132"></rect><line stroke="#4fd37b" stroke-width="5" x1="393" x2="393" y1="106" y2="222"></line>
            <rect fill="#ff6868" height="86" rx="6" width="28" x="512" y="168"></rect><line stroke="#ff6868" stroke-width="5" x1="526" x2="526" y1="146" y2="278"></line>
            <rect fill="#ff6868" height="92" rx="6" width="30" x="612" y="230"></rect><line stroke="#ff6868" stroke-width="5" x1="627" x2="627" y1="210" y2="346"></line>
            <rect fill="#ff6868" height="96" rx="6" width="30" x="720" y="294"></rect><line stroke="#ff6868" stroke-width="5" x1="735" x2="735" y1="270" y2="410"></line>
            <rect fill="#4fd37b" height="60" rx="6" width="24" x="824" y="324"></rect><line stroke="#4fd37b" stroke-width="5" x1="836" x2="836" y1="302" y2="402"></line>
          </g>
          <rect fill="rgba(83,214,233,0.14)" height="68" rx="10" stroke="#53d6e9" stroke-width="2" width="178" x="548" y="226"></rect>
          <text fill="#53d6e9" font-size="17" font-weight="900" text-anchor="middle" x="637" y="218">FVG possible</text>
          <path d="M692 324 C612 272 526 214 446 184" fill="none" stroke="#f8c24e" stroke-dasharray="8 8" stroke-width="3"></path>
          <circle cx="446" cy="184" fill="#081222" r="9" stroke="#f8c24e" stroke-width="4"></circle>
          <path d="M636 250 C720 310 804 370 910 404" fill="none" marker-end="url(#ob-bear-arrow)" stroke="#ef5350" stroke-width="4"></path>
          <text fill="#ef5350" font-size="20" font-weight="900" x="610" y="152">Displacement baissier</text>
          <line stroke="#ef5350" stroke-dasharray="6 6" stroke-width="2" x1="682" x2="622" y1="164" y2="236"></line>
          <text fill="#f8c24e" font-size="18" font-weight="800" x="704" y="356">Retour possible vers l’OB</text>
          <line stroke="#f8c24e" stroke-dasharray="7 7" stroke-width="2" x1="694" x2="456" y1="344" y2="188"></line>
          <text fill="#e6f4ff" font-size="17" font-weight="900" text-anchor="middle" x="560" y="474">BSL prise → rejet → displacement baissier → retour contrôlé → cible sous le prix.</text>
        </svg>
      </div>
      <div class="academy-grid">
        <div class="academy-card"><h3>BSL prise</h3><p>Le prix déclenche les stops shorts et attire les acheteurs breakout au-dessus d’un high visible.</p></div>
        <div class="academy-card"><h3>Rejet + livraison</h3><p>La reprise vendeuse doit être nette : corps directionnels, faible overlap, cassure d’un swing pertinent.</p></div>
        <div class="academy-card"><h3>Retour dans l’OB</h3><p>Le retour doit ressembler à une correction. S’il remonte violemment et annule le sellside displacement, la zone perd son autorité.</p></div>
        <div class="academy-card"><h3>Target</h3><p>La cible naturelle se trouve sous le prix : SSL, low interne, low externe ou DOL baissière selon le contexte.</p></div>
      </div>
      <div class="rule-block"><strong>Règle :</strong> bullish ou bearish, un OB reste une zone source validée par la séquence. La couleur de la bougie ne suffit jamais.</div>
    </section>
    """
    insert_after_id(ROOT / "31-order-blocks.html", "v73-ob-bearish-mirror", "ob-anatomie", html)


def clean_setups_core():
    path = ROOT / "04-setups-core.html"
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    for block in soup.find_all("div", class_="inst-block"):
        block.decompose()
    remove_existing(soup, "v73-setups-core-clean-note")
    html = """
    <section class="page-note beginner-bridge" id="v73-setups-core-clean-note">
      <strong>Note de lecture :</strong> la logique institutionnelle détaillée est volontairement dans les chapitres dédiés. Ici, les setups cœur servent surtout à voir comment les briques s’assemblent en plan complet.
    </section>
    """
    anchor = soup.find(id="bridge-setups-debutant")
    if anchor:
        anchor.insert_after(BeautifulSoup(html, "html.parser"))
    path.write_text(str(soup), encoding="utf-8")


TRANSITIONS = {
    "31-order-blocks.html": ("Comprenez FVG, imbalance et CE", "Tu sais maintenant ce qui rend une zone source défendable. La suite explique la trace laissée par une livraison rapide : FVG, imbalance et CE."),
    "32-fvg-imbalance-ce.html": ("Validez le MSS et le changement de contrôle", "Tu sais lire une inefficience. La suite ajoute la confirmation structurelle : quel niveau doit céder pour dire que le contrôle change vraiment."),
    "33-mss-changement-controle.html": ("Comprenez breaker et mitigation", "Tu sais valider un shift. La suite montre ce qui arrive quand une zone qui devait tenir est mitigée, cassée ou retournée en breaker."),
    "34-breaker-mitigation.html": ("Priorisez les PD Arrays", "Tu sais distinguer zone active, mitigation et breaker. La suite t’apprend à classer plusieurs zones concurrentes sans tout traiter au même niveau."),
    "35-pd-arrays-hierarchie.html": ("Ancrez OTE et dealing range", "Tu sais hiérarchiser les zones. La suite t’apprend à choisir la bonne range de référence avant de parler d’entrée optimale."),
    "36-ote-dealing-range.html": ("Hiérarchisez DOL et targets", "Tu sais ancrer un retracement. La suite verrouille la sortie : si la cible ne paie pas le risque, l’entrée n’a aucune valeur."),
    "37-dol-targets-hierarchie.html": ("Utilisez SMT comme confluence", "Tu sais construire les objectifs. La suite ajoute une confluence inter-marchés pour confirmer ou affaiblir une lecture déjà construite."),
    "38-smt-divergence.html": ("Lisez les profils de journée", "Tu sais utiliser SMT sans en faire un signal autonome. La suite replace cette confluence dans le comportement global de la journée."),
    "39-profils-journee-sessions.html": ("Reconnaissez les setups cœur", "Tu sais nommer le profil de journée. La suite assemble les briques en setups cœur, avec contexte, cible, invalidation et risque."),
}


def add_transitions():
    for filename, (next_title, body) in TRANSITIONS.items():
        path = ROOT / filename
        soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
        remove_existing(soup, "v73-transition-suivante")
        html = f"""
        <section class="page-note beginner-bridge" id="v73-transition-suivante">
          <strong>Pourquoi la suite ?</strong> {body}
        </section>
        """
        bottom = soup.find("nav", class_="lesson-bottom-nav")
        if bottom:
            bottom.insert_before(BeautifulSoup(html, "html.parser"))
        path.write_text(str(soup), encoding="utf-8")


def update_index_displacement():
    path = ROOT / "15-index-concepts.html"
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    table = soup.find("table", class_="référence-table")
    if not table:
        path.write_text(str(soup), encoding="utf-8")
        return
    for row in table.find_all("tr"):
        cells = row.find_all("td")
        if cells and "Displacement" in cells[0].get_text(" ", strip=True):
            cells[1].clear()
            link = soup.new_tag("a", href="40-displacement-operationnel.html", **{"class": "glosslink"})
            link.string = "Référence principale"
            cells[1].append(link)
            cells[2].clear()
            items = [
                ("40-displacement-operationnel.html#displacement-anatomie", "anatomie"),
                ("40-displacement-operationnel.html#displacement-checklist", "checklist"),
                ("40-displacement-operationnel.html#displacement-abc", "cas A/B/C"),
            ]
            for index, (href, label) in enumerate(items):
                if index:
                    cells[2].append(", ")
                item = soup.new_tag("a", href=href, **{"class": "glosslink"})
                item.string = label
                cells[2].append(item)
            break
    path.write_text(str(soup), encoding="utf-8")


def add_liquidity_to_displacement_bridge():
    html = """
    <section class="card" id="v73-pont-displacement-operationnel">
      <header><h2>Après la liquidité : valider le displacement</h2><span>Transition</span></header>
      <p>Cette leçon explique pourquoi le prix peut accélérer après une prise de liquidité. La suivante rend le critère opérationnel : comment distinguer une vraie livraison rapide d’une simple bougie impressionnante.</p>
      <div class="section-links">
        <a class="section-link" href="40-displacement-operationnel.html"><h3>Chapitre displacement opérationnel</h3><p>Critères, checklist, cas A/B/C et lecture multi-timeframe.</p></a>
      </div>
    </section>
    """
    insert_after_id(ROOT / "21-liquidite-deplacement.html", "v73-pont-displacement-operationnel", "v54-pont-fondations", html)


def main():
    add_mechanics_depth()
    add_parcours_psychology_bridge()
    add_mss_timeframe_section()
    add_ob_bearish_mirror()
    clean_setups_core()
    add_transitions()
    update_index_displacement()
    add_liquidity_to_displacement_bridge()


if __name__ == "__main__":
    main()
