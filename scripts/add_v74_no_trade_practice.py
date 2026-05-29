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
            main.append(fragment)
    path.write_text(str(soup), encoding="utf-8")


def add_replay_no_trade_pack():
    html = """
    <section class="card" id="v74-no-trade-replay-pack">
      <header><h2>Pack replay : entraîner le no trade sur du bruit réel</h2><span>No trade</span></header>
      <p>Le replay ne doit pas seulement servir à chercher des entrées. Une grosse partie du progrès vient des cas où tu vois quelque chose de tentant, puis tu refuses parce qu’une condition obligatoire manque.</p>
      <div class="chart ob-wide-chart">
        <svg aria-label="Replay no trade avec décision avant résultat" role="img" viewBox="0 0 1120 520">
          <rect fill="#081222" height="480" rx="26" stroke="#26394c" stroke-width="2" width="1080" x="20" y="20"></rect>
          <g stroke="#19304a" stroke-width="1">
            <line x1="78" x2="1042" y1="122" y2="122"></line>
            <line x1="78" x2="1042" y1="214" y2="214"></line>
            <line x1="78" x2="1042" y1="306" y2="306"></line>
            <line x1="78" x2="1042" y1="398" y2="398"></line>
          </g>
          <rect fill="rgba(248,194,78,0.12)" height="182" rx="14" stroke="#f8c24e" stroke-width="3" width="510" x="96" y="158"></rect>
          <line stroke="#f8c24e" stroke-dasharray="8 8" stroke-width="3" x1="112" x2="590" y1="184" y2="184"></line>
          <line stroke="#f8c24e" stroke-dasharray="8 8" stroke-width="3" x1="112" x2="590" y1="314" y2="314"></line>
          <path d="M112 292 C174 150 232 334 296 188 S418 328 492 204 S564 286 596 240" fill="none" stroke="#b8c7d6" stroke-width="5"></path>
          <rect fill="rgba(83,214,233,0.16)" height="48" rx="10" stroke="#53d6e9" stroke-width="3" width="146" x="426" y="210"></rect>
          <text fill="#53d6e9" font-size="16" font-weight="900" text-anchor="middle" x="499" y="198">FVG tentant</text>
          <line stroke="#ef5350" stroke-dasharray="9 8" stroke-width="4" x1="654" x2="654" y1="76" y2="430"></line>
          <circle cx="654" cy="244" fill="#081222" r="10" stroke="#ef5350" stroke-width="4"></circle>
          <text fill="#ef5350" font-size="20" font-weight="900" text-anchor="middle" x="654" y="462">Décision écrite : NO TRADE</text>
          <rect fill="#0b1829" height="270" rx="18" stroke="#26394c" stroke-width="2" width="310" x="730" y="126"></rect>
          <text fill="#e6f4ff" font-size="22" font-weight="900" text-anchor="middle" x="885" y="170">Pourquoi refuser ?</text>
          <text fill="#b8c7d6" font-size="15" font-weight="800" x="766" y="212">1. Prix au milieu de range</text>
          <text fill="#b8c7d6" font-size="15" font-weight="800" x="766" y="248">2. Aucun displacement net</text>
          <text fill="#b8c7d6" font-size="15" font-weight="800" x="766" y="284">3. Target trop proche</text>
          <text fill="#b8c7d6" font-size="15" font-weight="800" x="766" y="320">4. Plusieurs mèches opposées</text>
          <text fill="#f8c24e" font-size="15" font-weight="900" x="766" y="360">Révéler ensuite seulement</text>
          <text fill="#e6f4ff" font-size="17" font-weight="900" text-anchor="middle" x="356" y="78">Le but du drill : résister à une forme séduisante mais incomplète.</text>
        </svg>
      </div>
      <div class="replay-grid">
        <article class="replay-card"><span class="replay-kicker">No trade 01</span><h3>Milieu de range</h3><p>Repère un FVG ou OB propre au centre d’une range. Refuse tant qu’un extrême n’a pas été travaillé.</p><ul><li>À noter : range, equilibrium, target disponible.</li><li>Score : refus précis, pas absence de décision.</li></ul></article>
        <article class="replay-card"><span class="replay-kicker">No trade 02</span><h3>DOL consommée</h3><p>Attends une journée où la cible principale est touchée tôt. Observe les entrées tardives qui deviennent pauvres en R.</p><ul><li>À noter : cible touchée, distance au prochain TP.</li><li>Score : refus si le R ne paie plus.</li></ul></article>
        <article class="replay-card"><span class="replay-kicker">No trade 03</span><h3>Conflit multi-timeframe</h3><p>Prends un signal M5 propre contre une structure H1/H4 encore intacte. Classe-le comme alerte, pas entrée.</p><ul><li>À noter : timeframe qui porte la décision.</li><li>Score : ne pas laisser le petit TF inverser le plan.</li></ul></article>
        <article class="replay-card"><span class="replay-kicker">No trade 04</span><h3>État mental rouge</h3><p>Après deux pertes en replay, continue sans prendre de trade. Note les entrées que tu aurais forcées en live.</p><ul><li>À noter : émotion, urgence, justification.</li><li>Score : protéger le protocole.</li></ul></article>
      </div>
      <div class="section-links">
        <a class="section-link" href="41-no-trade.html"><h3>Leçon No Trade</h3><p>Lire la méthode complète de refus structuré.</p></a>
        <a class="section-link" download="" href="templates/no-trade-log.csv"><h3>Template no trade</h3><p>Journaliser les refus comme des décisions mesurables.</p></a>
      </div>
    </section>
    """
    insert_after_id(ROOT / "30-replay-lab.html", "v74-no-trade-replay-pack", "drills-replay", html)


def add_quiz_realistic_bridge():
    html = """
    <section class="card" id="v74-quiz-vers-cas-reels">
      <header><h2>Utiliser les quiz sans rester bloqué sur les schémas propres</h2><span>Passage réel</span></header>
      <p>Les quiz ci-dessous entraînent la discrimination : valide, invalide, buy, sell ou no trade. Pour éviter l’apprentissage trop scolaire, chaque bonne réponse doit ensuite être rejouée sur un cas réel documenté.</p>
      <div class="academy-grid">
        <div class="academy-card"><h3>Étape 1</h3><p>Réponds au quiz sans ouvrir la correction. Écris une phrase : “je prends / je refuse parce que…”</p></div>
        <div class="academy-card"><h3>Étape 2</h3><p>Associe le quiz à un slot de la bibliothèque replay : FVG, MSS, OB, breakout, no trade ou psychologie.</p></div>
        <div class="academy-card"><h3>Étape 3</h3><p>Travaille un exemple bar replay avec capture avant, décision écrite et capture après.</p></div>
        <div class="academy-card"><h3>Étape 4</h3><p>Classe le résultat : reconnaissance correcte, contexte oublié, no trade correct, ou forme apprise trop mécaniquement.</p></div>
      </div>
      <div class="section-links">
        <a class="section-link" href="replay-cases.html"><h3>Associer à un cas replay</h3><p>Bibliothèque de slots vérifiables pour sortir du schéma abstrait.</p></a>
        <a class="section-link" href="41-no-trade.html"><h3>Quiz no trade</h3><p>La réponse correcte n’est pas toujours une direction : parfois c’est le refus.</p></a>
      </div>
    </section>
    """
    insert_after_id(ROOT / "08-quiz.html", "v74-quiz-vers-cas-reels", "v59-replay-lab-quiz", html)


def add_replay_case_slots():
    html = """
    <section class="card case-library-section" id="v74-cas-no-trade-avances">
      <header><h2>No trade avancé</h2><span>Slots de cas</span></header>
      <div class="case-library-grid">
        <article class="case-slot">
          <div class="case-slot-head"><span>CAS-11</span><small>à valider</small></div>
          <h3>Milieu de range séduisant</h3>
          <p>Documenter un FVG/OB propre visuellement mais placé à l’equilibrium, sans asymétrie de target.</p>
          <ul><li>Capture avant décision obligatoire.</li><li>Phrase de refus obligatoire.</li><li>Résultat après révélation obligatoire.</li></ul>
        </article>
        <article class="case-slot">
          <div class="case-slot-head"><span>CAS-12</span><small>à valider</small></div>
          <h3>DOL touchée puis setup tardif</h3>
          <p>Montrer une entrée tentante après que la liquidité principale de session a déjà été prise.</p>
          <ul><li>Identifier la DOL consommée.</li><li>Calculer le R restant.</li><li>Classer refus correct ou peur excessive.</li></ul>
        </article>
        <article class="case-slot">
          <div class="case-slot-head"><span>CAS-13</span><small>à valider</small></div>
          <h3>Conflit HTF / LTF</h3>
          <p>Comparer un signal intraday propre avec une structure supérieure encore opposée.</p>
          <ul><li>Nommer le timeframe de décision.</li><li>Nommer le timeframe d’exécution.</li><li>Refuser si le LTF invente la narrative.</li></ul>
        </article>
      </div>
    </section>
    """
    insert_after_id(ROOT / "replay-cases.html", "v74-cas-no-trade-avances", "cas-psychologie", html)


def add_resources_no_trade_link():
    html = """
    <section class="card" id="v74-ressources-no-trade">
      <header><h2>Journaliser les no trades</h2><span>Patience</span></header>
      <p>Les refus doivent entrer dans l’échantillon. Sinon tu ne mesures que les trades pris, jamais les erreurs évitées.</p>
      <div class="section-links">
        <a class="section-link" download="" href="templates/no-trade-log.csv"><h3>No trade log</h3><p>CSV pour documenter setup tentant, raison du refus, condition manquante et résultat après révélation.</p></a>
        <a class="section-link" href="41-no-trade.html"><h3>Leçon No Trade</h3><p>La méthode complète pour refuser sans confondre patience et peur.</p></a>
      </div>
    </section>
    """
    insert_after_id(ROOT / "ressources-pratiques.html", "v74-ressources-no-trade", "templates", html)


def add_index_no_trade_row():
    path = ROOT / "15-index-concepts.html"
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    if soup.find(id="v74-index-no-trade-row"):
        soup.find(id="v74-index-no-trade-row").decompose()
    table = soup.find("table", class_="référence-table")
    if not table:
        path.write_text(str(soup), encoding="utf-8")
        return
    tr = soup.new_tag("tr", id="v74-index-no-trade-row")
    td1 = soup.new_tag("td")
    td1.append(soup.new_tag("strong"))
    td1.strong.string = "No Trade"
    td2 = soup.new_tag("td")
    a = soup.new_tag("a", href="41-no-trade.html", **{"class": "glosslink"})
    a.string = "Référence principale"
    td2.append(a)
    td3 = soup.new_tag("td")
    links = [
        ("41-no-trade.html#no-trade-gate", "porte de décision"),
        ("41-no-trade.html#no-trade-families", "familles"),
        ("30-replay-lab.html#v74-no-trade-replay-pack", "drill replay"),
    ]
    for index, (href, label) in enumerate(links):
        if index:
            td3.append(", ")
        item = soup.new_tag("a", href=href, **{"class": "glosslink"})
        item.string = label
        td3.append(item)
    tr.extend([td1, td2, td3])
    table.append(tr)
    path.write_text(str(soup), encoding="utf-8")


def main():
    add_replay_no_trade_pack()
    add_quiz_realistic_bridge()
    add_replay_case_slots()
    add_resources_no_trade_link()
    add_index_no_trade_row()


if __name__ == "__main__":
    main()
