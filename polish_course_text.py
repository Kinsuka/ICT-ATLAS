from pathlib import Path


REPLACEMENTS = {
    "Parcours guide": "Parcours guidé",
    "schema": "schéma",
    "modele mental": "modèle mental",
    "difference": "différence",
    "isoles": "isolés",
    "Executer": "Exécuter",
    "Ordre recommande": "Ordre recommandé",
    "mecanique": "mécanique",
    "Point d'entrée": "Point d’entrée",
    "evaluation": "évaluation",
    "execution": "exécution",
    "Definitions": "Définitions",
    "executable": "exécutable",
    "degrades": "dégradés",
    "completes": "complètes",
    "regles": "règles",
    "arret": "arrêt",
    "apres": "après",
    "avancee": "avancée",
    "masquees": "masquées",
    "entrainement": "entraînement",
    "recapitulatif": "récapitulatif",
}


def main():
    for path in Path(".").glob("*.html"):
        text = path.read_text(encoding="utf-8")
        for old, new in REPLACEMENTS.items():
            text = text.replace(old, new)
        path.write_text(text, encoding="utf-8")

    Path("README_V44.txt").write_text(
        "ICT Atlas V44 - Layout plateforme de cours\n\n"
        "Refonte HTML/CSS pour une lecture type OpenClassrooms/Udemy : table des matières en parties, "
        "leçons numérotées, progression, navigation précédent/suivant, contenu clair centré et blocs pédagogiques.\n"
        "Le contenu existant est conservé et réorganisé en 4 parties / 22 leçons, avec un glossaire permanent séparé du parcours.\n\n"
        "Point d’entrée : index.html\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
