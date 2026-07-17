from pathlib import Path

from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parents[1]


def insert_after_id(filename: str, section_id: str, anchor_id: str, html: str) -> None:
    path = ROOT / "pages" / filename
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    existing = soup.find(id=section_id)
    if existing:
        existing.decompose()
    anchor = soup.find(id=anchor_id)
    if not anchor:
        raise RuntimeError(f"Missing anchor {anchor_id!r} in {filename}")
    fragment = BeautifulSoup(html, "html.parser").find(id=section_id)
    if not fragment:
        raise RuntimeError(f"Missing section {section_id!r} in generated fragment")
    anchor.insert_after(fragment)
    path.write_text(str(soup), encoding="utf-8")


def add_model_chain() -> None:
    insert_after_id(
        "16-modele-mental.html",
        "v80-chaine-causale",
        "phrase-fil-rouge",
        """
        <section class="card" id="v80-chaine-causale">
          <header><h2>La chaîne causale obligatoire</h2><span>Fil rouge</span></header>
          <p>Avant de chercher une entrée, construis une explication qui relie le point de départ à la destination. Chaque étape répond à une question différente ; aucune forme isolée ne peut remplacer la chaîne.</p>
          <div class="academy-grid">
            <div class="academy-card"><h3>1. Contexte HTF</h3><p>Quel environnement et quelle direction les timeframes supérieurs autorisent-ils ?</p></div>
            <div class="academy-card"><h3>2. Localisation</h3><p>Le prix travaille-t-il un POI pertinent, en premium, discount ou à l’equilibrium ?</p></div>
            <div class="academy-card"><h3>3. Liquidité</h3><p>Quelle BSL ou SSL vient d’être prise, et quelle liquidité reste disponible ?</p></div>
            <div class="academy-card"><h3>4. Réaction</h3><p>Le rejet, le displacement ou le changement de contrôle soutient-il réellement l’idée ?</p></div>
            <div class="academy-card"><h3>5. DOL</h3><p>Vers quelle cible encore ouverte le prix a-t-il une raison logique de se déplacer ?</p></div>
            <div class="academy-card"><h3>6. Exécution</h3><p>Quel modèle testé donne le prix d’entrée sans inventer la direction ?</p></div>
            <div class="academy-card"><h3>7. Invalidation</h3><p>Quel fait observable annule la narrative avant ou après l’entrée ?</p></div>
          </div>
          <div class="rule-block"><strong>Phrase obligatoire :</strong> « Parce que [contexte], à [localisation], après [liquidité + réaction], j’attends un déplacement vers [DOL]. J’exécute avec [modèle] et j’abandonne l’idée si [invalidation]. »</div>
          <div class="rule-block"><strong>Règle :</strong> si tu ne peux pas expliquer pourquoi le prix devrait aller de A vers B, tu n’as pas encore de trade.</div>
        </section>
        """,
    )


def add_decision_roles() -> None:
    insert_after_id(
        "17-concept-setup-plan.html",
        "v80-raison-confluence-trigger",
        "trois-niveaux",
        """
        <section class="card" id="v80-raison-confluence-trigger">
          <header><h2>Raison directionnelle, confluence et déclencheur</h2><span>Hiérarchie</span></header>
          <p>Une décision devient confuse quand ces trois rôles sont mélangés. Commence par la raison du mouvement, ajoute seulement les informations qui la renforcent, puis choisis comment l’exécuter.</p>
          <div class="table-wrap"><table><thead><tr><th>Rôle</th><th>Question</th><th>Exemples</th><th>Erreur à éviter</th></tr></thead><tbody>
            <tr><td><strong>Raison directionnelle</strong></td><td>Pourquoi le prix devrait-il aller de A vers B ?</td><td>Contexte HTF, POI, liquidité prise, DOL encore ouverte.</td><td>Répondre seulement « parce qu’il y a un FVG ».</td></tr>
            <tr><td><strong>Confluence</strong></td><td>Quelle information renforce ou affaiblit la lecture ?</td><td>SMT, timing, profil de journée, qualité supplémentaire d’un displacement déjà requis.</td><td>Empiler des indices faibles pour compenser un contexte contraire.</td></tr>
            <tr><td><strong>Déclencheur</strong></td><td>Quel événement autorise l’ordre maintenant ?</td><td>MSS de confirmation, retour FVG/CE ou retest OB, selon la règle définie dans le plan.</td><td>Laisser le trigger petit timeframe inventer le biais.</td></tr>
          </tbody></table></div>
          <div class="rule-block"><strong>Règle :</strong> FVG, OB, MSS et SMT sont des informations ou des outils d’exécution. Aucun ne constitue seul une raison directionnelle complète. Le MSS confirme un changement ; le plan doit ensuite préciser le prix exact d’entrée, par exemple à la clôture ou sur un retest.</div>
        </section>
        """,
    )


def add_topdown_case() -> None:
    insert_after_id(
        "25-top-down-multi-timeframe.html",
        "v80-cas-narrative-bearish",
        "conflit-timeframe",
        """
        <section class="card" id="v80-cas-narrative-bearish">
          <header><h2>Cas complet : narrative bearish, exécution conditionnelle</h2><span>Top-down</span></header>
          <div class="steps">
            <div class="step"><div class="step-icon">D</div><div class="step-body"><h5>Daily bearish</h5><p>La structure supérieure favorise les ventes et laisse de la sell-side liquidity disponible sous le marché.</p></div></div>
            <div class="step"><div class="step-icon">4H</div><div class="step-body"><h5>POI H4 en premium</h5><p>Le prix revient dans une zone de résistance cohérente avec la dealing range de référence.</p></div></div>
            <div class="step"><div class="step-icon">LQ</div><div class="step-body"><h5>Buy-side liquidity prise</h5><p>Un high visible est balayé. La prise seule n’autorise rien : la réaction doit encore montrer un changement de contrôle.</p></div></div>
            <div class="step"><div class="step-icon bear">↓</div><div class="step-body"><h5>Réaction bearish</h5><p>Un displacement ou MSS utile confirme que le prix refuse la zone supérieure.</p></div></div>
            <div class="step"><div class="step-icon entry">TP</div><div class="step-body"><h5>DOL sous le prix</h5><p>Une SSL claire reste ouverte et offre une distance suffisante par rapport à l’invalidation.</p></div></div>
          </div>
          <div class="callout-grid">
            <div class="callout"><h3>Signal M15 bullish</h3><p>Un FVG bullish M15 peut être propre visuellement. Il reste un contre-signal tant que le Daily/H4 bearish et la DOL baissière dominent. Décision : pas de long.</p></div>
            <div class="callout"><h3>Permission de short</h3><p>Le trader attend ensuite son modèle testé : MSS, retour FVG/CE ou retest OB. Le modèle précise le prix ; il ne crée pas la thèse.</p></div>
            <div class="callout"><h3>Invalidation de narrative</h3><p>L’idée tombe si le marché réaccepte durablement au-dessus du POI H4, détruit la structure bearish ou rend une DOL supérieure plus logique.</p></div>
          </div>
          <div class="rule-block"><strong>Narrative écrite :</strong> Daily bearish, POI H4 en premium, BSL prise puis réaction bearish, SSL ouverte sous le prix. Seuls les shorts confirmés sont autorisés tant que cette structure reste valide.</div>
        </section>
        """,
    )


def add_entry_comparison() -> None:
    insert_after_id(
        "04-setups-core.html",
        "v80-une-narrative-trois-entrees",
        "bridge-setups-debutant",
        """
        <section class="card" id="v80-une-narrative-trois-entrees">
          <header><h2>Une narrative, trois modèles d’entrée</h2><span>Exécution</span></header>
          <p>Supposons une même lecture : contexte bearish, POI HTF en premium, BSL prise, réaction bearish et DOL sous le prix. Les entrées ci-dessous ne créent pas trois idées ; elles exécutent la même hypothèse avec des compromis différents.</p>
          <div class="table-wrap"><table><thead><tr><th>Modèle</th><th>Ce qu’il apporte</th><th>Compromis à mesurer</th><th>Ce qui ne change pas</th></tr></thead><tbody>
            <tr><td><strong>Retour FVG / CE</strong></td><td>Zone de retracement précise après displacement.</td><td>Meilleur prix possible, mais ordre parfois non servi ou zone traversée.</td><td>Contexte, DOL et invalidation de narrative.</td></tr>
            <tr><td><strong>Retest Order Block</strong></td><td>Ancrage sur la zone source du mouvement de contrôle.</td><td>Stop et fréquence différents selon la profondeur du retour.</td><td>Contexte, DOL et invalidation de narrative.</td></tr>
            <tr><td><strong>Confirmation MSS</strong></td><td>Preuve supplémentaire avant l’ordre.</td><td>Entrée plus tardive, stop ou RR potentiellement moins favorables.</td><td>Contexte, DOL et invalidation de narrative.</td></tr>
          </tbody></table></div>
          <div class="rule-block"><strong>Règle :</strong> compare les modèles d’entrée séparément dans le backtest. N’ajoute pas un nouveau sigle au plan tant que sa définition et son apport statistique ne sont pas démontrés.</div>
        </section>
        """,
    )


def add_statistical_protocol() -> None:
    insert_after_id(
        "19-preuve-statistique.html",
        "v80-protocole-validation",
        "échantillon-minimum",
        """
        <section class="card" id="v80-protocole-validation">
          <header><h2>Protocole de validation : du backtest au risque minimal</h2><span>Méthode</span></header>
          <div class="academy-grid">
            <div class="academy-card"><h3>1. Figer l’hypothèse</h3><p>Écris narrative, exclusions, entrée, invalidation, targets et gestion avant de compter les résultats.</p></div>
            <div class="academy-card"><h3>2. Explorer</h3><p>Utilise un premier échantillon pour repérer erreurs grossières et variables utiles, sans annoncer encore un edge.</p></div>
            <div class="academy-card"><h3>3. Confirmer hors échantillon</h3><p>Teste les règles figées sur une autre période ou d’autres sessions sans les ajuster après chaque perte.</p></div>
            <div class="academy-card"><h3>4. Forward tester</h3><p>Après le replay masqué, exécute les règles figées en temps réel sur paper trading ou compte démo, sans capital à risque.</p></div>
            <div class="academy-card"><h3>5. Passer au risque minimal</h3><p>Commence seulement si l’expectancy reste positive après coûts et si le protocole est exécutable.</p></div>
            <div class="academy-card"><h3>6. Monter progressivement</h3><p>Augmente le risque uniquement si les résultats et le respect du plan restent stables.</p></div>
          </div>
          <div class="callout-grid">
            <div class="callout"><h3>Pas de nombre magique</h3><p>50, 100 ou 1 000 occurrences ne garantissent rien. La qualité des données, l’indépendance des cas et la diversité des régimes comptent autant que le volume.</p></div>
            <div class="callout"><h3>Coûts réels</h3><p>Ajoute spread, commissions, slippage, ordres non servis et erreurs d’exécution. Une simulation idéale peut surestimer l’edge.</p></div>
            <div class="callout"><h3>Une variable à la fois</h3><p>Si tu modifies l’entrée, ne change pas simultanément le filtre DOL, l’horaire et la gestion. Sinon tu ne sais plus ce qui produit la différence.</p></div>
          </div>
          <div class="rule-block"><strong>Porte go / no-go à définir dans le plan :</strong> nombre minimal de décisions forward, expectancy nette positive, drawdown maximal, taux maximal d’erreurs de processus, version de règles inchangée et pourcentage exact du risque minimal. Ces seuils dépendent du modèle ; ils doivent être écrits avant le test, pas choisis après les résultats.</div>
          <div class="rule-block"><strong>Éligibilité aux statistiques d’edge :</strong> marque « inclus » seulement si le ruleset était figé, le setup valide et l’exécution conforme. Les erreurs de processus restent comptées séparément pour mesurer l’exécution, sans être confondues avec l’expectancy théorique du modèle.</div>
          <div class="rule-block"><strong>Règle :</strong> le backtest formule une preuve conditionnelle, jamais une promesse de performance future.</div>
        </section>
        """,
    )


def add_psychology_boundary() -> None:
    insert_after_id(
        "26-psychologie-trader.html",
        "v80-edge-discipline",
        "v61-sabotage-map",
        """
        <section class="card" id="v80-edge-discipline">
          <header><h2>Diagnostiquer avant de changer de stratégie</h2><span>Edge × exécution</span></header>
          <p>Une perte ne dit pas automatiquement si le problème vient du modèle ou du trader. Classe d’abord la source de l’écart, puis corrige seulement la couche concernée.</p>
          <div class="table-wrap"><table><thead><tr><th>Couche</th><th>Question de diagnostic</th><th>Correction adaptée</th></tr></thead><tbody>
            <tr><td><strong>Stratégie</strong></td><td>L’expectancy reste-t-elle positive sur un échantillon confirmé après coûts ?</td><td>Re-tester ou abandonner selon les données.</td></tr>
            <tr><td><strong>Lecture</strong></td><td>La narrative, le POI et la DOL étaient-ils cohérents avant le signal ?</td><td>Revoir le top-down et les exclusions.</td></tr>
            <tr><td><strong>Exécution</strong></td><td>L’entrée correspond-elle exactement au modèle testé ?</td><td>Drill replay et checklist avant clic.</td></tr>
            <tr><td><strong>Risque</strong></td><td>La taille et la perte maximale respectaient-elles le plan ?</td><td>Réduire le risque et verrouiller les limites.</td></tr>
            <tr><td><strong>Comportement</strong></td><td>Y a-t-il eu FOMO, revenge, impatience ou règle négociée ?</td><td>Pause, journal et protocole si/alors.</td></tr>
          </tbody></table></div>
          <div class="rule-block"><strong>Règle :</strong> la discipline protège un edge prouvé ; elle ne transforme pas une stratégie à expectancy négative en stratégie rentable. Ne change pas de méthode à partir d’un trade ou d’une courte série.</div>
        </section>
        """,
    )


def add_amd_context() -> None:
    insert_after_id(
        "39-profils-journee-sessions.html",
        "v80-amd-hypothese",
        "profiles-map",
        """
        <section class="card" id="v80-amd-hypothese">
          <header><h2>AMD : une hypothèse de journée, pas une loi</h2><span>Power of Three</span></header>
          <p>Accumulation, manipulation et distribution peuvent organiser certaines sessions. Le modèle sert à décrire ce qui devient observable, pas à forcer chaque journée dans trois phases parfaites.</p>
          <div class="table-wrap"><table><thead><tr><th>Phase</th><th>Lecture</th><th>Action autorisée</th><th>Erreur fréquente</th></tr></thead><tbody>
            <tr><td><strong>Accumulation</strong></td><td>Range, compression ou équilibre relatif.</td><td>Tracer bornes, liquidités et scénarios.</td><td>Multiplier les entrées au centre de la consolidation.</td></tr>
            <tr><td><strong>Manipulation</strong></td><td>Sweep ou sortie d’un extrême.</td><td>Observer acceptation, rejet et déplacement.</td><td>Entrer sur la mèche seule.</td></tr>
            <tr><td><strong>Distribution</strong></td><td>Livraison directionnelle confirmée vers une DOL.</td><td>Chercher un modèle d’exécution aligné.</td><td>Poursuivre le mouvement si la DOL est déjà consommée.</td></tr>
          </tbody></table></div>
          <div class="rule-block"><strong>Règle :</strong> si le marché reste en chop, accepte la cassure ou ne montre aucune distribution nette, AMD ne donne aucune permission de trade.</div>
        </section>
        """,
    )


def add_no_trade_states() -> None:
    insert_after_id(
        "41-no-trade.html",
        "v80-etats-marche-no-trade",
        "no-trade-families",
        """
        <section class="card" id="v80-etats-marche-no-trade">
          <header><h2>États de marché qui ferment la porte</h2><span>Consolidation</span></header>
          <div class="academy-grid">
            <div class="academy-card"><h3>Avant une news majeure</h3><p>Compression et faux départs peuvent augmenter. Attends le protocole news prévu au lieu d’anticiper la première impulsion.</p></div>
            <div class="academy-card"><h3>Après une grande expansion</h3><p>Si la DOL principale est prise et que le prix rééquilibre, le mouvement résiduel peut ne plus payer le risque.</p></div>
            <div class="academy-card"><h3>Milieu de range</h3><p>Sans extrême travaillé ni asymétrie, les micro-FVG et micro-MSS donnent peu d’information.</p></div>
            <div class="academy-card"><h3>Aucun contrôle dominant</h3><p>Overlap, mèches des deux côtés et déplacements rapidement effacés signalent une absence de permission.</p></div>
          </div>
          <div class="rule-block"><strong>La porte se rouvre seulement si :</strong> une liquidité utile est travaillée, une réaction nette apparaît, une DOL reste disponible et le risque redevient défendable.</div>
        </section>
        """,
    )


def add_quiz_entry_models() -> None:
    insert_after_id(
        "08-quiz.html",
        "v80-quiz-une-narrative-trois-entrees",
        "quiz-mtf-conflict-v37",
        """
        <section class="card" id="v80-quiz-une-narrative-trois-entrees">
          <header><h2>Quiz — une narrative, trois entrées</h2><span>Quiz · exécution</span></header>
          <div class="quiz-prompt"><strong>Consigne :</strong> Daily bearish, POI H4 en premium, BSL prise, displacement bearish et SSL ouverte. Trois traders utilisent respectivement un retour FVG, un retest OB et une confirmation MSS. Combien de narratives sont présentes ?</div>
          <div class="steps">
            <div class="step"><div class="step-icon">A</div><div class="step-body"><h5>FVG / CE</h5><p>Entrée précise sur retour dans l’inefficience.</p></div></div>
            <div class="step"><div class="step-icon">B</div><div class="step-body"><h5>Order Block</h5><p>Entrée sur retest de la zone source.</p></div></div>
            <div class="step"><div class="step-icon">C</div><div class="step-body"><h5>MSS</h5><p>Entrée plus tardive après confirmation structurelle.</p></div></div>
          </div>
          <div class="rule-band"><strong>Règle :</strong> réponds d’abord sur la thèse, puis indique quelle variable doit être comparée dans le backtest.</div>
          <details class="quiz-answer"><summary>Révéler la réponse / correction</summary><div class="answer-inner"><p><strong>Réponse :</strong> une seule narrative et trois modèles d’exécution. Il faut comparer séparément fréquence, prix d’entrée, stop, RR, taux d’ordres servis et expectancy de chaque modèle, sans changer le contexte HTF ni la DOL.</p></div></details>
        </section>
        """,
    )


def add_replay_narrative_gate() -> None:
    insert_after_id(
        "30-replay-lab.html",
        "v80-narrative-avant-revelation",
        "protocole-replay",
        """
        <section class="card" id="v80-narrative-avant-revelation">
          <header><h2>Écrire la narrative avant de révéler le futur</h2><span>Validation</span></header>
          <p>La décision buy, sell ou no trade ne suffit pas. Avant chaque révélation, écris la chaîne qui rend cette décision défendable.</p>
          <div class="academy-grid">
            <div class="academy-card"><h3>Phrase avant résultat</h3><p>Contexte HTF, POI, premium/discount, liquidité travaillée, réaction, DOL, modèle et invalidation.</p></div>
            <div class="academy-card"><h3>Score de raisonnement</h3><p>La narrative était-elle cohérente avec les informations disponibles, même si le trade perd ?</p></div>
            <div class="academy-card"><h3>Score d’exécution</h3><p>L’ordre, le stop, les targets et la gestion respectaient-ils exactement le modèle testé ?</p></div>
            <div class="academy-card"><h3>Résultat séparé</h3><p>Le P&amp;L est noté à part. Un gain hors plan reste une erreur ; une perte conforme peut rester une bonne décision.</p></div>
          </div>
          <div class="rule-block"><strong>Règle :</strong> aucune bougie supplémentaire n’est révélée tant que la narrative et son invalidation ne sont pas écrites.</div>
        </section>
        """,
    )


def apply_reader_test_fixes() -> None:
    path = ROOT / "pages" / "16-modele-mental.html"
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    soup.find(id="cycle-liquidity-delivery").find("h2").string = "Cycle minimal : liquidité → réaction → retour → cible"
    path.write_text(str(soup), encoding="utf-8")

    path = ROOT / "pages" / "17-concept-setup-plan.html"
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    trigger = next(
        card
        for card in soup.find(id="checklist-plan").select(".academy-card")
        if card.find("h3").get_text(strip=True) in {"Declencheur", "Séquence et déclencheur"}
    )
    trigger.find("h3").string = "Séquence et déclencheur"
    trigger.find("p").string = (
        "La liquidité prise et le displacement valident la séquence. Le trigger exact — MSS de confirmation, "
        "retour FVG/CE ou retest OB — est nommé sans regarder le futur."
    )
    path.write_text(str(soup), encoding="utf-8")

    path = ROOT / "pages" / "04-setups-core.html"
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    invalidations = {
        "fvg-bull": "Le scénario est invalidé si le prix traverse le FVG sans réaction et casse le low structurel qui porte le displacement. TP1 vise la liquidité interne ; TP2 la BSL externe.",
        "fvg-bear": "Le scénario est invalidé si le prix reprend le FVG et casse le high structurel à l’origine du déplacement bearish. TP1 vise la liquidité interne ; TP2 la SSL externe.",
        "mss-bull": "Le scénario est invalidé si le prix reprend la SSL et détruit le low qui soutient le changement de structure. TP1 vise la liquidité haute interne ; TP2 la BSL externe.",
        "ob-bull": "Le scénario est invalidé si le prix clôture sous l’OB et sous le low structurel qui a lancé le displacement. TP1 vise la liquidité haute interne ; TP2 la BSL.",
        "breaker-bear": "Le scénario est invalidé si le prix réaccepte au-dessus du breaker et reprend la structure haussière. TP1 vise la liquidité interne ; TP2 la SSL plus basse.",
        "asia-rf": "Le scénario est invalidé si le prix ressort sous Asia Low et accepte la cassure au lieu de réintégrer. TP1 vise Asia High ; TP2 la BSL supérieure si l’extension reste ouverte.",
        "nyam-reversal": "Le scénario est invalidé si le prix réaccepte au-dessus du PDH raid et annule le MSS bearish. TP1 vise une liquidité basse interne ; TP2 le PDL ou la SSL externe.",
        "pm-continuation": "Le scénario est invalidé si le low du lunch est accepté à la baisse ou si le biais AM/Daily est détruit. TP1 vise le high AM ; TP2 la DOL encore ouverte.",
    }
    for section_id, text in invalidations.items():
        section = soup.find(id=section_id)
        block = next(
            item
            for item in section.select(".step-body")
            if item.find("h5") and item.find("h5").get_text(strip=True) == "Invalidation"
        )
        block.find("p").string = text
    path.write_text(str(soup), encoding="utf-8")

    path = ROOT / "pages" / "19-preuve-statistique.html"
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    rule = soup.find(id="edge-pattern-preuve").find("div", class_="rule-block")
    rule.clear()
    strong = soup.new_tag("strong")
    strong.string = "Règle :"
    rule.append(strong)
    rule.append(
        " Un setup est autorisé au risque seulement quand sa définition produit une expectancy positive après coûts "
        "sur une validation distincte de l’échantillon exploratoire."
    )
    path.write_text(str(soup), encoding="utf-8")

    path = ROOT / "pages" / "41-no-trade.html"
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    paragraph = soup.find(id="no-trade-journal").find("p")
    paragraph.string = (
        "Un no trade non noté disparaît de ton apprentissage. Tu ne vois alors que les trades pris, jamais les refus "
        "conformes ni les attentes correctement exécutées. La fiche no trade sert à prouver que ta patience respecte "
        "une règle répétable, même si le mouvement refusé aurait finalement gagné."
    )
    path.write_text(str(soup), encoding="utf-8")

    path = ROOT / "pages" / "08-quiz.html"
    text = path.read_text(encoding="utf-8").replace(
        "décide mentalement avant de révéler", "écris ta décision avant de révéler"
    )
    path.write_text(text, encoding="utf-8")


def main() -> None:
    add_model_chain()
    add_decision_roles()
    add_topdown_case()
    add_entry_comparison()
    add_statistical_protocol()
    add_psychology_boundary()
    add_amd_context()
    add_no_trade_states()
    add_quiz_entry_models()
    add_replay_narrative_gate()
    apply_reader_test_fixes()


if __name__ == "__main__":
    main()
