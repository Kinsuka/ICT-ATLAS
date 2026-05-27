from pathlib import Path

from bs4 import BeautifulSoup


ROOT = Path(".")


def remove_existing(soup, section_id):
    old = soup.find(id=section_id)
    if old:
        old.decompose()


def insert_after_anchor(path, section_id, html, anchor_id):
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    remove_existing(soup, section_id)
    fragment = BeautifulSoup(html, "html.parser")
    anchor = soup.find(id=anchor_id)
    if anchor:
        anchor.insert_after(fragment)
    else:
        main = soup.find("main", class_="page")
        if main:
            main.insert(4, fragment)
    path.write_text(str(soup), encoding="utf-8")


def psychology_sections():
    return """
<section class="card" id="v61-sabotage-map">
  <header><h2>Carte des sabotages : ce qui casse le plan</h2><span>Diagnostic</span></header>
  <p>Un trader ne se sabote pas parce qu'il ne connait pas le setup. Il se sabote quand un etat interne transforme une regle claire en exception negociable. Le but est donc d'identifier le signal mental avant le clic.</p>
  <div class="chart">
    <table class="référence-table">
      <tr><th>Declencheur</th><th>Phrase interne typique</th><th>Action dangereuse</th><th>Protocole</th></tr>
      <tr><td><strong>Perte normale</strong></td><td>Je dois recuperer maintenant.</td><td>Revenge trade, taille augmentee, entree hors setup.</td><td>Pause 5 minutes, classer valide/erreur, nouveau trade seulement si nouvelle sequence complete.</td></tr>
      <tr><td><strong>Gain rapide</strong></td><td>Je suis dans le flow.</td><td>Surtrading, rendre la journee, transformer +2R en flat.</td><td>Reduire agressivite, noter objectif atteint, attendre un setup A+ ou finir la session.</td></tr>
      <tr><td><strong>Trade rate</strong></td><td>J'ai rate le mouvement, il faut entrer.</td><td>FOMO, entree au milieu, stop sans structure.</td><td>Noter "trade manque", chercher seulement le prochain retour structurel.</td></tr>
      <tr><td><strong>Deux pertes</strong></td><td>Le marche me doit une opportunite.</td><td>Forcer un troisieme trade de qualite inferieure.</td><td>Mode defensif : risque reduit ou observation. Si frustration presente, stop journee.</td></tr>
      <tr><td><strong>Proche drawdown</strong></td><td>Je vais faire un dernier trade pour sauver la journee.</td><td>Trade de panique, destruction prop firm.</td><td>Arret obligatoire. Review a froid uniquement.</td></tr>
    </table>
  </div>
  <div class="rule-block"><strong>Regle :</strong> si tu entends une justification emotionnelle, tu n'es plus en execution ; tu es en negociation avec ton plan.</div>
</section>
"""


def emotional_meter_section():
    return """
<section class="card" id="v61-thermometre-emotionnel">
  <header><h2>Thermometre emotionnel : savoir quand baisser le risque</h2><span>Controle</span></header>
  <div class="chart emotional-meter-chart">
    <svg viewBox="0 0 1040 430" role="img" aria-label="Thermometre emotionnel du trader">
      <rect x="24" y="24" width="992" height="382" rx="24" fill="#081222" stroke="#26394c" stroke-width="2"/>
      <text x="520" y="66" fill="#8ee5fa" text-anchor="middle" font-size="24" font-weight="900">Etat interne -> taille autorisee -> action</text>
      <g>
        <rect x="90" y="120" width="255" height="170" rx="18" fill="rgba(38,166,154,0.12)" stroke="#26a69a" stroke-width="2"/>
        <text x="218" y="155" fill="#26a69a" text-anchor="middle" font-size="24" font-weight="900">Zone verte</text>
        <text x="218" y="195" fill="#d9e6f2" text-anchor="middle" font-size="17">calme, clair, patient</text>
        <text x="218" y="232" fill="#b8c7d6" text-anchor="middle" font-size="16">risque normal</text>
        <text x="218" y="260" fill="#b8c7d6" text-anchor="middle" font-size="16">setup A ou A+</text>
      </g>
      <g>
        <rect x="392" y="120" width="255" height="170" rx="18" fill="rgba(251,191,36,0.12)" stroke="#f8c24e" stroke-width="2"/>
        <text x="520" y="155" fill="#f8c24e" text-anchor="middle" font-size="24" font-weight="900">Zone jaune</text>
        <text x="520" y="195" fill="#d9e6f2" text-anchor="middle" font-size="17">impatient, tendu</text>
        <text x="520" y="232" fill="#b8c7d6" text-anchor="middle" font-size="16">risque reduit</text>
        <text x="520" y="260" fill="#b8c7d6" text-anchor="middle" font-size="16">un seul trade autorise</text>
      </g>
      <g>
        <rect x="695" y="120" width="255" height="170" rx="18" fill="rgba(239,83,80,0.12)" stroke="#ef5350" stroke-width="2"/>
        <text x="823" y="155" fill="#ef5350" text-anchor="middle" font-size="24" font-weight="900">Zone rouge</text>
        <text x="823" y="195" fill="#d9e6f2" text-anchor="middle" font-size="17">urgence, colere, euphorie</text>
        <text x="823" y="232" fill="#b8c7d6" text-anchor="middle" font-size="16">0 trade</text>
        <text x="823" y="260" fill="#b8c7d6" text-anchor="middle" font-size="16">review ou observation</text>
      </g>
      <line x1="346" y1="205" x2="386" y2="205" stroke="#4fc3f7" stroke-width="4" stroke-dasharray="8 8"/>
      <line x1="648" y1="205" x2="688" y2="205" stroke="#4fc3f7" stroke-width="4" stroke-dasharray="8 8"/>
      <text x="520" y="346" fill="#f8c24e" text-anchor="middle" font-size="18" font-weight="800">La taille ne depend pas seulement du setup : elle depend aussi de ton etat d'execution.</text>
    </svg>
  </div>
  <div class="academy-grid">
    <div class="academy-card"><h3>Signal vert</h3><p>Tu peux expliquer le setup lentement, sans urgence. Le trade peut etre execute si le plan complet existe.</p></div>
    <div class="academy-card"><h3>Signal jaune</h3><p>Tu veux cliquer vite, tu cherches une confirmation qui t'arrange. Reduis ou attends une preuve plus nette.</p></div>
    <div class="academy-card"><h3>Signal rouge</h3><p>Tu veux recuperer, te prouver quelque chose ou profiter d'une euphorie. Le protocole interdit le trade.</p></div>
  </div>
</section>
"""


def if_then_section():
    return """
<section class="card" id="v61-regles-si-alors">
  <header><h2>Regles si/alors : retirer la decision au moment chaud</h2><span>Execution</span></header>
  <div class="academy-grid">
    <div class="academy-card"><h3>Si je prends une perte valide</h3><p>Alors je ne change rien au systeme. Je note la perte, je pause, puis j'attends une nouvelle sequence complete.</p></div>
    <div class="academy-card"><h3>Si je prends une perte hors plan</h3><p>Alors la prochaine opportunite est interdite. Je dois d'abord ecrire quelle regle a ete cassee.</p></div>
    <div class="academy-card"><h3>Si je fais +2R dans la journee</h3><p>Alors je protege la journee : taille reduite, A+ seulement, ou fin de session.</p></div>
    <div class="academy-card"><h3>Si le DOL est deja touche</h3><p>Alors je refuse les entrees tardives. Je ne cherche pas a extraire un trade d'un mouvement deja livre.</p></div>
    <div class="academy-card"><h3>Si je suis proche de la limite prop firm</h3><p>Alors je passe en mode survie : zero trade ou risque minimal. La priorite devient rester eligible demain.</p></div>
    <div class="academy-card"><h3>Si je veux absolument trader</h3><p>Alors c'est une information de danger. Je dois ouvrir la checklist, pas la fenetre d'ordre.</p></div>
  </div>
</section>
"""


def workflow_state_machine():
    return """
<section class="card" id="v61-workflow-state-machine">
  <header><h2>Workflow de session : une machine a etats, pas une improvisation</h2><span>Routine</span></header>
  <p>Une session bien construite force le trader a passer par des portes. Si une porte ne s'ouvre pas, le trade ne passe pas. Ce systeme evite de transformer une impression en execution.</p>
  <div class="chart workflow-state-chart">
    <svg viewBox="0 0 1120 500" role="img" aria-label="Workflow de session en portes de decision">
      <rect x="22" y="22" width="1076" height="456" rx="26" fill="#081222" stroke="#26394c" stroke-width="2"/>
      <defs>
        <marker id="workflow-arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#4fc3f7"/></marker>
      </defs>
      <text x="560" y="66" fill="#8ee5fa" font-size="24" font-weight="900" text-anchor="middle">Preparation -> permission -> execution -> review</text>
      <g font-size="15" font-weight="800" text-anchor="middle">
        <rect x="70" y="140" width="170" height="110" rx="18" fill="#0d1b2a" stroke="#4fc3f7" stroke-width="2"/>
        <text x="155" y="178" fill="#4fc3f7">Preparation</text>
        <text x="155" y="210" fill="#b8c7d6" font-size="13">biais, DOL, news</text>
        <rect x="300" y="140" width="170" height="110" rx="18" fill="#0d1b2a" stroke="#f8c24e" stroke-width="2"/>
        <text x="385" y="178" fill="#f8c24e">Permission</text>
        <text x="385" y="210" fill="#b8c7d6" font-size="13">sweep, reaction</text>
        <rect x="530" y="140" width="170" height="110" rx="18" fill="#0d1b2a" stroke="#26a69a" stroke-width="2"/>
        <text x="615" y="178" fill="#26a69a">Execution</text>
        <text x="615" y="210" fill="#b8c7d6" font-size="13">entree, stop, TP</text>
        <rect x="760" y="140" width="170" height="110" rx="18" fill="#0d1b2a" stroke="#a78bfa" stroke-width="2"/>
        <text x="845" y="178" fill="#a78bfa">Gestion</text>
        <text x="845" y="210" fill="#b8c7d6" font-size="13">BE, partiel, invalidation</text>
        <rect x="415" y="330" width="290" height="88" rx="18" fill="rgba(239,83,80,0.1)" stroke="#ef5350" stroke-width="2"/>
        <text x="560" y="365" fill="#ef5350">No trade / stop journee</text>
        <text x="560" y="392" fill="#b8c7d6" font-size="13">si une porte critique manque</text>
      </g>
      <line x1="240" y1="195" x2="294" y2="195" stroke="#4fc3f7" stroke-width="3" marker-end="url(#workflow-arrow)"/>
      <line x1="470" y1="195" x2="524" y2="195" stroke="#4fc3f7" stroke-width="3" marker-end="url(#workflow-arrow)"/>
      <line x1="700" y1="195" x2="754" y2="195" stroke="#4fc3f7" stroke-width="3" marker-end="url(#workflow-arrow)"/>
      <path d="M385 250 C385 292 470 316 520 330" fill="none" stroke="#ef5350" stroke-width="3" stroke-dasharray="8 8" marker-end="url(#workflow-arrow)"/>
      <path d="M615 250 C615 292 600 314 580 330" fill="none" stroke="#ef5350" stroke-width="3" stroke-dasharray="8 8" marker-end="url(#workflow-arrow)"/>
      <path d="M845 250 C845 315 720 352 705 368" fill="none" stroke="#ef5350" stroke-width="3" stroke-dasharray="8 8" marker-end="url(#workflow-arrow)"/>
    </svg>
  </div>
</section>
"""


def workflow_click_protocol():
    return """
<section class="card" id="v61-avant-clic">
  <header><h2>Les 90 secondes avant le clic</h2><span>Micro-routine</span></header>
  <p>La plupart des erreurs arrivent dans les secondes qui precedent l'entree. Cette micro-routine ralentit le geste et oblige le cerveau a repasser par la structure.</p>
  <div class="replay-steps">
    <div><strong>1</strong><span>Dire le contexte : trend, range ou transition. Si tu hesites, pas d'entree immediate.</span></div>
    <div><strong>2</strong><span>Nommer la liquidite prise et la DOL restante. Sans cible, pas de raison de tenir le trade.</span></div>
    <div><strong>3</strong><span>Verifier la permission : sweep, rejet, displacement, MSS ou zone de retour exploitable.</span></div>
    <div><strong>4</strong><span>Placer invalidation, stop, TP1, TP2 et calculer le R avant de cliquer.</span></div>
    <div><strong>5</strong><span>Lire l'etat mental : vert, jaune ou rouge. En rouge, le trade est interdit.</span></div>
  </div>
  <div class="rule-block"><strong>Regle :</strong> si une reponse doit etre inventee sous pression, le trade n'est pas pret.</div>
</section>
"""


def workflow_scorecard():
    return """
<section class="card" id="v61-score-session">
  <header><h2>Score de session : mesurer la qualite, pas seulement le PnL</h2><span>Review</span></header>
  <div class="chart">
    <table class="référence-table">
      <tr><th>Critere</th><th>0 point</th><th>1 point</th><th>2 points</th></tr>
      <tr><td><strong>Preparation</strong></td><td>Pas de plan ecrit.</td><td>Plan incomplet.</td><td>Biais, DOL, news, risque et scenarios notes.</td></tr>
      <tr><td><strong>Patience</strong></td><td>Entree impulsive.</td><td>Attente partielle.</td><td>Entree seulement apres permission claire.</td></tr>
      <tr><td><strong>Risque</strong></td><td>Taille ou stop improvises.</td><td>Risque note mais modifie.</td><td>Risque, stop, TP et invalidation fixes avant clic.</td></tr>
      <tr><td><strong>Emotion</strong></td><td>Revenge, FOMO ou euphorie executee.</td><td>Emotion observee tard.</td><td>Etat mental note et protocole respecte.</td></tr>
      <tr><td><strong>Review</strong></td><td>Aucune correction.</td><td>Correction vague.</td><td>Une correction actionnable pour demain.</td></tr>
    </table>
  </div>
  <p>Une session perdante peut etre de haute qualite. Une session gagnante peut etre dangereuse si elle recompense une rupture de protocole. Le score sert a separer progression et hasard.</p>
</section>
"""


def enrich():
    psychology_path = ROOT / "26-psychologie-trader.html"
    insert_after_anchor(psychology_path, "v61-sabotage-map", psychology_sections(), "v58-ressources-psychologie")
    insert_after_anchor(psychology_path, "v61-thermometre-emotionnel", emotional_meter_section(), "v61-sabotage-map")
    insert_after_anchor(psychology_path, "v61-regles-si-alors", if_then_section(), "v61-thermometre-emotionnel")

    workflow_path = ROOT / "20-workflow-session.html"
    insert_after_anchor(workflow_path, "v61-workflow-state-machine", workflow_state_machine(), "v58-ressources-workflow")
    insert_after_anchor(workflow_path, "v61-avant-clic", workflow_click_protocol(), "v61-workflow-state-machine")
    insert_after_anchor(workflow_path, "v61-score-session", workflow_scorecard(), "v61-avant-clic")


def main():
    enrich()


if __name__ == "__main__":
    main()
