from pathlib import Path

from bs4 import BeautifulSoup

from course_platform_layout import LESSON_OBJECTIVES


ROOT = Path(__file__).resolve().parents[1]
OBJECTIVE_PAGES = [
    "06-contextes-avances.html",
    "12-gestion-risque.html",
    "20-workflow-session.html",
    "14-live-chart.html",
    "10-programme-avance.html",
    "08-quiz.html",
    "13-prop-firm.html",
    "09-synthese.html",
    "15-index-concepts.html",
]
PREREQUISITE_IDS = [
    "v63-bridge-order-blocks",
    "v64-bridge-fvg-imbalance",
    "v65-bridge-mss-shift",
    "v66-bridge-breaker-mitigation",
    "v67-bridge-pd-arrays",
    "v68-bridge-ote-dealing-range",
    "v69-bridge-dol-targets",
    "v70-bridge-smt-divergence",
    "v71-bridge-profils-journee",
]

PREREQUISITE_INDEX = """
<section aria-labelledby="setup-prerequisite-title" class="setup-prerequisite-index" id="setup-prerequisites">
  <header>
    <div>
      <span>Avant les setups · contrôle rapide</span>
      <h2 id="setup-prerequisite-title">Neuf prérequis, une seule grille de décision</h2>
    </div>
    <p>Cette leçon assemble les concepts ; elle ne les redéfinit pas. Si une question reste floue, retourne directement à la checklist source avant d’étudier les setups.</p>
  </header>
  <ol class="prerequisite-matrix">
    <li><a href="31-order-blocks.html#ob-checklist"><small>Leçon 16 · 01</small><strong>Order Block</strong><span>La zone vient-elle d’un déplacement validé plutôt que d’une bougie choisie après coup ?</span></a></li>
    <li><a href="32-fvg-imbalance-ce.html#fvg-checklist"><small>Leçon 17 · 02</small><strong>FVG / CE</strong><span>Le gap est-il net, encore disponible et créé par une vraie livraison du prix ?</span></a></li>
    <li><a href="33-mss-changement-controle.html#mss-checklist"><small>Leçon 18 · 03</small><strong>MSS</strong><span>Le prix a-t-il cassé un niveau utile avec displacement après la prise de liquidité ?</span></a></li>
    <li><a href="34-breaker-mitigation.html#breaker-checklist"><small>Leçon 19 · 04</small><strong>Breaker</strong><span>La zone a-t-elle réellement changé de rôle après une invalidation lisible ?</span></a></li>
    <li><a href="35-pd-arrays-hierarchie.html#pd-checklist"><small>Leçon 20 · 05</small><strong>PD Arrays</strong><span>Cette zone est-elle prioritaire selon le timeframe, l’emplacement et la fraîcheur ?</span></a></li>
    <li><a href="36-ote-dealing-range.html#ote-checklist"><small>Leçon 21 · 06</small><strong>OTE / Range</strong><span>Le retracement est-il ancré sur la dealing range et le swing réellement pertinents ?</span></a></li>
    <li><a href="37-dol-targets-hierarchie.html#dol-checklist"><small>Leçon 22 · 07</small><strong>DOL / Targets</strong><span>La cible est-elle visible, fraîche et assez éloignée pour rémunérer le risque ?</span></a></li>
    <li><a href="38-smt-divergence.html#smt-checklist"><small>Leçon 23 · 08</small><strong>SMT</strong><span>La divergence compare-t-elle deux marchés, deux niveaux et un timing réellement comparables ?</span></a></li>
    <li><a href="39-profils-journee-sessions.html#profiles-session-playbook"><small>Leçon 24 · 09</small><strong>Profil de journée</strong><span>Le setup est-il cohérent avec la phase de session et le comportement dominant ?</span></a></li>
  </ol>
  <p class="prerequisite-gate"><strong>Gate :</strong> une réponse incertaine suffit à suspendre l’étude du setup et à rouvrir le chapitre source.</p>
</section>
"""


def write_soup(path, soup):
    path.write_text(str(soup), encoding="utf-8")


def compact_setup_prerequisites():
    path = ROOT / "pages" / "04-setups-core.html"
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    existing = soup.select_one("#setup-prerequisites")
    source_sections = [soup.select_one(f"#{section_id}") for section_id in PREREQUISITE_IDS]
    source_sections = [section for section in source_sections if section]

    if not existing and source_sections:
        compact_index = BeautifulSoup(PREREQUISITE_INDEX, "html.parser").section
        source_sections[0].replace_with(compact_index)
        for section in source_sections[1:]:
            section.decompose()

    heading = soup.select_one("#templates-market-structure-setups h2")
    if heading and heading.get_text(" ", strip=True) == "Templates de market structure appliques aux setups ICT":
        heading.string = "Templates de market structure appliqués aux setups ICT"

    write_soup(path, soup)


def replace_generic_objectives():
    for filename in OBJECTIVE_PAGES:
        path = ROOT / "pages" / filename
        soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
        cards = soup.select("section.lesson-objectives .lesson-objective")
        objectives = LESSON_OBJECTIVES[filename]
        if len(cards) != len(objectives):
            raise RuntimeError(f"{filename}: expected {len(objectives)} objective cards, found {len(cards)}")

        for card, (label, body) in zip(cards, objectives):
            card.select_one("strong").string = label
            card.select_one("p").string = body
        write_soup(path, soup)


if __name__ == "__main__":
    compact_setup_prerequisites()
    replace_generic_objectives()
    print("V100 applied: compact prerequisites and measurable lesson checkpoints.")
