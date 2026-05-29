from pathlib import Path

from bs4 import BeautifulSoup


ROOT = Path(".")


def remove_existing(soup, section_id):
    old = soup.find(id=section_id)
    if old:
        old.decompose()


def insert_section(path, section_id, title, intro, anchor_id=None):
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    remove_existing(soup, section_id)
    html = f"""
    <section class="card" id="{section_id}">
      <header><h2>{title}</h2><span>Priorité</span></header>
      <p>{intro}</p>
      <div class="section-links">
        <a class="section-link" href="35-pd-arrays-hierarchie.html"><h3>Chapitre PD Arrays</h3><p>Prioriser OB, FVG, breaker, liquidité, premium/discount et zones HTF/LTF.</p></a>
        <a class="section-link" href="35-pd-arrays-hierarchie.html#pd-checklist"><h3>Checklist de priorité</h3><p>Timeframe, emplacement, liquidité, fraîcheur, risque et TP.</p></a>
      </div>
    </section>
    """
    fragment = BeautifulSoup(html, "html.parser")
    anchor = soup.find(id=anchor_id) if anchor_id else soup.find("div", class_="page-meta-dashboard")
    if anchor:
        anchor.insert_after(fragment)
    else:
        main = soup.find("main", class_="page")
        if main:
            main.insert(3, fragment)
    path.write_text(str(soup), encoding="utf-8")


def insert_index_row():
    path = ROOT / "15-index-concepts.html"
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    table = soup.find("table", class_="référence-table")
    if not table:
        path.write_text(str(soup), encoding="utf-8")
        return
    existing = table.find(string=lambda value: value and "PD Arrays" in value)
    if existing:
        path.write_text(str(soup), encoding="utf-8")
        return
    rows = table.find_all("tr")
    html = """
    <tr>
      <td><strong>PD Arrays</strong></td>
      <td><a class="glosslink" href="35-pd-arrays-hierarchie.html">Référence principale</a></td>
      <td><a class="glosslink" href="35-pd-arrays-hierarchie.html#pd-checklist">checklist</a>, <a class="glosslink" href="35-pd-arrays-hierarchie.html#pd-abc">cas A/B/C</a>, <a class="glosslink" href="04-setups-core.html">setups</a></td>
    </tr>
    """
    new_row = BeautifulSoup(html, "html.parser")
    insert_after = None
    for row in rows:
        if "OTE" in row.get_text(" ", strip=True):
            insert_after = row
            break
    if insert_after:
        insert_after.insert_after(new_row)
    else:
        table.append(new_row)
    path.write_text(str(soup), encoding="utf-8")


def insert_glossary_entry():
    path = ROOT / "glossaire.html"
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    vocab_list = soup.find("div", class_="vocab-list")
    if not vocab_list or vocab_list.find(string=lambda value: value and "PD Arrays" in value):
        path.write_text(str(soup), encoding="utf-8")
        return
    html = """
    <div class="vocab-entry">
      <div class="vocab-term">PD Arrays</div>
      <div class="vocab-body">
        <div>Définition :</div>
        <div>famille de zones de prix utilisées en lecture ICT : OB, FVG, breaker, mitigation, premium/discount, liquidité ou niveau HTF.</div>
        <div>À quoi ça sert :</div>
        <div>prioriser les zones quand plusieurs repères apparaissent en même temps et éviter de traiter chaque zone comme une entrée.</div>
        <div>Ce que ce n’est pas :</div>
        <div>une liste de signaux automatiques ; une PD Array doit être classée par contexte, timeframe, liquidité, fraîcheur et risque.</div>
        <br/>
        <div>Mini-exemple : un FVG M5 dans un OB H1 en discount vaut plus qu’un FVG isolé au milieu du range.</div>
        <div class="vocab-error"><b>Erreur fréquente :</b> tracer trop de zones et choisir celle qui arrange le trade au lieu de prioriser la carte.</div>
      </div>
    </div>
    """
    entry = BeautifulSoup(html, "html.parser")
    insert_after = None
    for item in vocab_list.find_all("div", class_="vocab-entry"):
        term = item.find("div", class_="vocab-term")
        if term and "Breaker Block" in term.get_text(" ", strip=True):
            insert_after = item
            break
    if insert_after:
        insert_after.insert_after(entry)
    else:
        vocab_list.append(entry)
    path.write_text(str(soup), encoding="utf-8")


def enrich():
    insert_section(
        ROOT / "index.html",
        "v67-accueil-pd-arrays",
        "Chapitre dédié : PD Arrays et hiérarchie des zones",
        "Avant les setups, on apprend à choisir quelle zone prioriser quand plusieurs repères ICT apparaissent en même temps.",
        "v66-accueil-breaker-mitigation",
    )
    insert_section(
        ROOT / "04-setups-core.html",
        "v67-bridge-pd-arrays",
        "Avant les setups : prioriser les PD Arrays",
        "Cette hiérarchie évite de traiter tous les OB, FVG et breakers au même niveau. Une zone doit être classée avant d’être tradée.",
        "v66-bridge-breaker-mitigation",
    )
    insert_section(
        ROOT / "15-index-concepts.html",
        "v67-index-pd-arrays",
        "PD Arrays / hiérarchie des zones",
        "Retrouve la leçon dédiée à la priorisation des zones HTF/LTF, OB, FVG, breaker, liquidité et premium/discount.",
        "v66-index-breaker-mitigation",
    )
    insert_index_row()
    insert_glossary_entry()


def main():
    enrich()


if __name__ == "__main__":
    main()
