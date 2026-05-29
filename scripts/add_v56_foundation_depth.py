from pathlib import Path

from bs4 import BeautifulSoup

from add_v54_foundation_module import ROOT, arrow_marker, candles, chart_base, dot, label, pill


def remove_existing(soup, section_id):
    old = soup.find(id=section_id)
    if old:
        old.decompose()


def insert_after_id(path, anchor_id, section_id, html):
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    remove_existing(soup, section_id)
    anchor = soup.find(id=anchor_id)
    fragment = BeautifulSoup(html, "html.parser")
    if anchor:
        anchor.insert_after(fragment)
    else:
        main = soup.find("main", class_="page")
        if main:
            main.insert(3, fragment)
    path.write_text(str(soup), encoding="utf-8")


def mechanics_sections():
    cause = f"""<section class="card" id="v56-mecanique-cause-effet"><header><h2>Lire la cause avant la forme</h2><span>V56 · socle</span></header>
{chart_base(arrow_marker("arr-cause") + '<rect fill="#0d1b2a" height="58" rx="12" stroke="#4fc3f7" width="135" x="58" y="146"></rect><rect fill="#0d1b2a" height="58" rx="12" stroke="#ffb300" width="135" x="238" y="146"></rect><rect fill="#0d1b2a" height="58" rx="12" stroke="#26a69a" width="135" x="418" y="146"></rect><rect fill="#0d1b2a" height="58" rx="12" stroke="#ef5350" width="135" x="598" y="146"></rect><rect fill="#0d1b2a" height="58" rx="12" stroke="#4fc3f7" width="135" x="778" y="146"></rect>' + label(125,170,"Ordres", "#4fc3f7") + label(305,170,"Niveaux vus", "#ffb300") + label(485,170,"Stops/TP", "#26a69a") + label(665,170,"Absorption", "#ef5350") + label(845,170,"Deplacement", "#4fc3f7") + '<line marker-end="url(#arr-cause)" stroke="#4fc3f7" stroke-width="1.8" x1="193" x2="238" y1="175" y2="175"></line><line marker-end="url(#arr-cause)" stroke="#4fc3f7" stroke-width="1.8" x1="373" x2="418" y1="175" y2="175"></line><line marker-end="url(#arr-cause)" stroke="#4fc3f7" stroke-width="1.8" x1="553" x2="598" y1="175" y2="175"></line><line marker-end="url(#arr-cause)" stroke="#4fc3f7" stroke-width="1.8" x1="733" x2="778" y1="175" y2="175"></line>' + label(480,292,"Une forme ICT est la trace visible d'une contrainte d'execution.", "#d9e6f2", "middle", 13))}
<div class="explain"><div class="exbox"><h4>Ce que voit le debutant</h4><p>Une bougie rapide, un FVG, un niveau casse, un retour dans une zone.</p></div><div class="exbox"><h4>Ce qu'il faut apprendre a lire</h4><p>Qui a ete force d'agir ? Quels stops ont ete pris ? Est-ce que le marche accepte ou rejette ce prix ?</p></div><div class="exbox"><h4>Pourquoi c'est fondateur</h4><p>Si tu lis seulement la forme, tu trades un dessin. Si tu lis la cause, tu peux filtrer les faux amis.</p></div></div><div class="rule-block"><strong>Regle :</strong> avant de nommer FVG, OB ou MSS, decris le mecanisme : ordres, liquidite, absorption, deplacement.</div></section>"""
    compare = f"""<section class="card" id="v56-absorption-vs-deplacement"><header><h2>Absorption, deplacement, bruit : trois reactions differentes</h2><span>V56 · exemples</span></header>
{chart_base(candles("105,245 160,210 215,232 270,190 325,214 380,176 435,198 490,162 545,184 600,148 660,170 720,132 805,154") + '<line stroke="#ffb300" stroke-dasharray="6 4" x1="90" x2="850" y1="176" y2="176"></line><rect fill="#26a69a" opacity=".1" x="92" y="206" width="240" height="62"></rect><rect fill="#4fc3f7" opacity=".1" x="360" y="112" width="220" height="82"></rect><rect fill="#ef5350" opacity=".1" x="618" y="132" width="220" height="70"></rect>' + dot(270,190,"#26a69a") + dot(490,162,"#4fc3f7") + dot(720,132,"#ef5350") + pill(126,276,150,"A absorption","#26a69a") + pill(396,84,162,"B deplacement","#4fc3f7") + pill(640,208,130,"C bruit","#ef5350") + label(480,324,"La suite du prix donne la qualite de la reaction, pas la meche seule.", "#d9e6f2", "middle", 12))}
<div class="academy-grid"><div class="academy-card"><h3>Absorption</h3><p>Le prix prend un niveau mais ne parvient pas a continuer. Quelqu'un absorbe les ordres agressifs.</p></div><div class="academy-card"><h3>Deplacement</h3><p>Le prix quitte la zone avec energie. C'est la preuve visuelle qu'un camp prend temporairement le controle.</p></div><div class="academy-card"><h3>Bruit</h3><p>La reaction est molle, sans cassure utile, sans destination claire. Pour un debutant, c'est souvent no trade.</p></div></div></section>"""
    insert_after_id(ROOT / "11-mecanique-marches.html", "v54-mecanique-visuelle", "v56-mecanique-cause-effet", cause)
    insert_after_id(ROOT / "11-mecanique-marches.html", "v56-mecanique-cause-effet", "v56-absorption-vs-deplacement", compare)


def displacement_sections():
    section = f"""<section class="card" id="v56-pourquoi-deplacement"><header><h2>Pourquoi le prix accelere apres une prise de liquidite ?</h2><span>V56 · causalite</span></header>
{chart_base(arrow_marker("arr-delivery") + candles("105,252 160,224 215,246 270,284 325,238 380,188 435,150 490,174 545,136 600,158 660,116 720,138 805,102") + '<line stroke="#26a69a" stroke-dasharray="7 5" x1="90" x2="850" y1="284" y2="284"></line><rect fill="#4fc3f7" opacity=".12" x="382" y="142" width="130" height="62"></rect><line stroke="#ffb300" stroke-dasharray="5 4" x1="382" x2="512" y1="173" y2="173"></line>' + dot(270,284,"#26a69a") + dot(435,150,"#4fc3f7") + dot(660,116,"#4fc3f7") + '<line marker-end="url(#arr-delivery)" stroke="#4fc3f7" stroke-width="1.8" x1="285" x2="420" y1="268" y2="165"></line><line marker-end="url(#arr-delivery)" stroke="#4fc3f7" stroke-width="1.8" x1="512" x2="650" y1="173" y2="122"></line>' + pill(200,294,132,"1. stops pris","#26a69a") + pill(382,210,150,"2. repricing","#4fc3f7") + pill(612,82,142,"3. delivery","#4fc3f7") + label(480,326,"La prise de liquidite cree souvent le carburant; le deplacement montre qui utilise ce carburant.", "#d9e6f2", "middle", 12))}
<div class="explain"><div class="exbox"><h4>Avant</h4><p>Le prix approche un niveau evident. Les ordres s'accumulent : stops, breakouts, TP, ordres limites.</p></div><div class="exbox"><h4>Pendant</h4><p>La prise du niveau declenche des ordres. Si ces ordres sont absorbes, le marche peut repartir violemment.</p></div><div class="exbox"><h4>Apres</h4><p>Le deplacement cree une nouvelle information : il montre un changement de controle exploitable plus tard sur retour.</p></div></div><div class="rule-block"><strong>Regle :</strong> le sweep seul ne suffit pas. Tu attends la reaction : rejet, deplacement, puis zone exploitable.</div></section>"""
    insert_after_id(ROOT / "21-liquidite-deplacement.html", "v54-pont-fondations", "v56-pourquoi-deplacement", section)


def liquidity_sections():
    section = f"""<section class="card" id="v56-score-liquidite"><header><h2>Donner du poids a une liquidite : forte, moyenne ou faible</h2><span>V56 · filtre</span></header>
{chart_base('<rect fill="#0d1b2a" height="230" rx="14" stroke="#1e3a5f" width="760" x="100" y="70"></rect><line stroke="#1e3a5f" x1="100" x2="860" y1="122" y2="122"></line><line stroke="#1e3a5f" x1="100" x2="860" y1="174" y2="174"></line><line stroke="#1e3a5f" x1="100" x2="860" y1="226" y2="226"></line>' + label(160,102,"Critere", "#8fa5ba", "middle", 12) + label(390,102,"Question", "#8fa5ba", "middle", 12) + label(720,102,"Lecture", "#8fa5ba", "middle", 12) + label(160,154,"Visibilite", "#4fc3f7", "middle", 13) + label(390,154,"Tout le monde voit-il ce niveau ?", "#d9e6f2", "middle", 12) + label(720,154,"Plus visible = plus d'ordres", "#26a69a", "middle", 12) + label(160,206,"Fraicheur", "#ffb300", "middle", 13) + label(390,206,"A-t-il deja ete pris ?", "#d9e6f2", "middle", 12) + label(720,206,"Deja pris = moins utile", "#ffb300", "middle", 12) + label(160,258,"Position", "#ef5350", "middle", 13) + label(390,258,"Interne ou externe ?", "#d9e6f2", "middle", 12) + label(720,258,"Externe = meilleure DOL", "#26a69a", "middle", 12) + label(480,334,"Une bonne cible combine visibilite, fraicheur, position et distance suffisante.", "#d9e6f2", "middle", 12))}
<div class="academy-grid"><div class="academy-card"><h3>Forte</h3><p>Visible, externe, non consommee, alignee avec la narrative. Elle peut devenir TP principal.</p></div><div class="academy-card"><h3>Moyenne</h3><p>Visible mais interne, ou proche, ou deja partiellement travaille. Elle sert plutot de TP1.</p></div><div class="academy-card"><h3>Faible</h3><p>Peu visible, deja prise, trop proche ou contre l'environnement. Elle ne justifie pas une entree seule.</p></div></div><div class="rule-block"><strong>Regle :</strong> si tu ne peux pas donner un poids a la liquidite, tu ne peux pas savoir si le trade merite d'etre pris.</div></section>"""
    insert_after_id(ROOT / "27-fondations-liquidite.html", "definir-ligne-liquidite", "v56-score-liquidite", section)


def entry_sections():
    section = f"""<section class="card" id="v56-entree-ladder"><header><h2>Sortir de la paralysie : quatre etats avant le clic</h2><span>V56 · execution</span></header>
{chart_base(arrow_marker("arr-ladder") + '<rect fill="#1a0505" height="58" rx="12" stroke="#ef5350" width="150" x="80" y="150"></rect><rect fill="#1a1200" height="58" rx="12" stroke="#ffb300" width="150" x="280" y="150"></rect><rect fill="#0d1b2a" height="58" rx="12" stroke="#4fc3f7" width="150" x="480" y="150"></rect><rect fill="#06180f" height="58" rx="12" stroke="#26a69a" width="150" x="680" y="150"></rect>' + label(155,172,"No trade", "#ef5350") + label(355,172,"Observation", "#ffb300") + label(555,172,"Preparation", "#4fc3f7") + label(755,172,"Execution", "#26a69a") + '<line marker-end="url(#arr-ladder)" stroke="#4fc3f7" stroke-width="1.8" x1="230" x2="280" y1="179" y2="179"></line><line marker-end="url(#arr-ladder)" stroke="#4fc3f7" stroke-width="1.8" x1="430" x2="480" y1="179" y2="179"></line><line marker-end="url(#arr-ladder)" stroke="#4fc3f7" stroke-width="1.8" x1="630" x2="680" y1="179" y2="179"></line>' + label(155,232,"Pas de cible", "#8fa5ba") + label(355,232,"Cible mais pas de reaction", "#8fa5ba") + label(555,232,"Zone + invalidation", "#8fa5ba") + label(755,232,"Trigger conforme", "#8fa5ba") + label(480,322,"Tu n'es pas paralyse si tu sais dans quel etat tu te trouves.", "#d9e6f2", "middle", 12))}
<div class="explain"><div class="exbox"><h4>No trade</h4><p>Aucune DOL claire, pas de timing, TP trop proche ou environnement contradictoire.</p></div><div class="exbox"><h4>Preparation</h4><p>La cible, l'invalidation et la zone candidate existent. Tu peux definir le prix ou tu agiras.</p></div><div class="exbox"><h4>Execution</h4><p>Le prix revient dans la zone et donne ton mode d'entree prevu : limite assummee ou confirmation.</p></div></div><div class="rule-block"><strong>Regle :</strong> un debutant doit savoir pourquoi il attend autant que pourquoi il entre.</div></section>"""
    insert_after_id(ROOT / "28-fondations-entree.html", "quand-comment-entrer", "v56-entree-ladder", section)


def stop_tp_sections():
    section = f"""<section class="card" id="v56-tp-decision-tree"><header><h2>Arbre de decision : TP, securisation, sortie</h2><span>V56 · gestion</span></header>
{chart_base(arrow_marker("arr-tp-tree") + '<rect fill="#0d1b2a" height="54" rx="12" stroke="#26a69a" width="135" x="80" y="150"></rect><rect fill="#0d1b2a" height="54" rx="12" stroke="#ffb300" width="135" x="282" y="150"></rect><rect fill="#0d1b2a" height="54" rx="12" stroke="#4fc3f7" width="135" x="484" y="150"></rect><rect fill="#0d1b2a" height="54" rx="12" stroke="#ef5350" width="135" x="686" y="150"></rect>' + label(147,172,"Entree", "#26a69a") + label(349,172,"TP1 touche", "#ffb300") + label(551,172,"Runner", "#4fc3f7") + label(753,172,"Sortie", "#ef5350") + '<line marker-end="url(#arr-tp-tree)" stroke="#4fc3f7" stroke-width="1.8" x1="215" x2="282" y1="177" y2="177"></line><line marker-end="url(#arr-tp-tree)" stroke="#4fc3f7" stroke-width="1.8" x1="417" x2="484" y1="177" y2="177"></line><line marker-end="url(#arr-tp-tree)" stroke="#4fc3f7" stroke-width="1.8" x1="619" x2="686" y1="177" y2="177"></line>' + label(147,230,"Stop initial", "#8fa5ba") + label(349,230,"Partiel ou BE", "#8fa5ba") + label(551,230,"Stop structurel", "#8fa5ba") + label(753,230,"DOL ou MSS inverse", "#8fa5ba") + label(480,322,"La securisation est une regle ecrite avant le trade, pas une emotion pendant le trade.", "#d9e6f2", "middle", 12))}
<div class="academy-grid"><div class="academy-card"><h3>Avant TP1</h3><p>Tu ne deplaces pas ton stop au hasard. Le trade respire tant que l'invalidation reste intacte.</p></div><div class="academy-card"><h3>Apres TP1</h3><p>Tu peux reduire le risque : partiel, break-even ou stop derriere une structure valide.</p></div><div class="academy-card"><h3>Apres DOL</h3><p>La raison principale est payee. Le reliquat sort sur cible, perte de momentum ou MSS inverse.</p></div></div><div class="rule-block"><strong>Regle :</strong> tu ne securises pas parce que tu devines le retournement ; tu securises parce que le plan avance.</div></section>"""
    insert_after_id(ROOT / "29-fondations-stop-tp.html", "tp-maximum-securisation", "v56-tp-decision-tree", section)


def environment_sections():
    section = f"""<section class="card" id="v56-environnement-avant-setup"><header><h2>Pourquoi l'environnement passe avant le setup</h2><span>V56 · filtre</span></header>
{chart_base(candles("105,252 160,220 215,238 270,198 325,218 380,176 435,196 490,154 545,176 600,132 660,152 720,112 805,136") + '<rect fill="#26a69a" opacity=".08" x="80" y="94" width="250" height="190"></rect><rect fill="#ffb300" opacity=".08" x="355" y="110" width="250" height="150"></rect><rect fill="#4fc3f7" opacity=".08" x="630" y="80" width="230" height="210"></rect>' + pill(126,66,112,"Trend","#26a69a") + pill(420,82,112,"Range","#ffb300") + pill(690,52,132,"Transition","#4fc3f7") + label(205,314,"Chercher pullbacks dans le flux", "#26a69a", "middle", 11) + label(480,314,"Attendre les bords ou failed breakouts", "#ffb300", "middle", 11) + label(745,314,"Reduire taille ou attendre confirmation", "#4fc3f7", "middle", 11))}
<div class="explain"><div class="exbox"><h4>En trend</h4><p>Un FVG ou OB dans le sens du flux a plus de sens, car le marche accepte deja le desequilibre.</p></div><div class="exbox"><h4>En range</h4><p>Le centre donne beaucoup de faux signaux. Les bords et les reprises de liquidite deviennent plus importants.</p></div><div class="exbox"><h4>En transition</h4><p>Le marche change peut-etre de regime. Tu demandes plus de preuve et tu acceptes moins d'agressivite.</p></div></div><div class="rule-block"><strong>Regle :</strong> un setup ne dit pas quoi faire tant que l'environnement ne dit pas s'il est adapte.</div></section>"""
    insert_after_id(ROOT / "22-structure-trend-range.html", "bridge-structure-debutant", "v56-environnement-avant-setup", section)


def main():
    mechanics_sections()
    displacement_sections()
    liquidity_sections()
    entry_sections()
    stop_tp_sections()
    environment_sections()


if __name__ == "__main__":
    main()
