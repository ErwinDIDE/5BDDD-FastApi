from datetime import date

UTILISATEURS: dict[int, dict] = {}
LIVRES: dict[int, dict] = {}
EMPRUNTS: dict[int, dict] = {}

compteurs = {"utilisateur": 0, "livre": 0, "emprunt": 0}

ENREGISTREMENT_UTILISATEURS = [
    {
        "nom": "Alice Dupont",
        "email": "alice@example.com",
        "telephone": "0601020304",
        "motdepasse": "password123",
    },
    {
        "nom": "Bob Martin",
        "email": "bob@example.com",
        "telephone": "0605060708",
        "motdepasse": "securepassword",
    },
]

ENREGISTREMENT_LIVRES = [
    {
        "titre": "Le Comte de Monte-Cristo",
        "auteur": "Alexandre Dumas",
        "genre": "Aventure",
        "date_publication": "1844-08-28",
        "disponible": True,
    },
    {
        "titre": "1984",
        "auteur": "George Orwell",
        "genre": "Dystopie",
        "date_publication": "1949-06-08",
        "disponible": False,
    },
    {
        "titre": "Dune",
        "auteur": "Frank Herbert",
        "genre": "Science-Fiction",
        "date_publication": "1965-08-01",
        "disponible": True,
    },
]


def id_suivant(kind: str) -> int:
    compteurs[kind] += 1
    return compteurs[kind]


def reset() -> None:
    UTILISATEURS.clear()
    LIVRES.clear()
    EMPRUNTS.clear()

    compteurs["utilisateur"] = 0
    compteurs["livre"] = 0
    compteurs["emprunt"] = 0

    # Initialisation des utilisateurs
    for u in ENREGISTREMENT_UTILISATEURS:
        identifiantutilisateur = id_suivant("utilisateur")
        UTILISATEURS[identifiantutilisateur] = {"id": identifiantutilisateur, **u}

    # Initialisation des livres
    for l in ENREGISTREMENT_LIVRES:
        identifiantlivre = id_suivant("livre")
        LIVRES[identifiantlivre] = {"id": identifiantlivre, **l}

    # Initialisation d'un emprunt de test
    identifiantemprunt = id_suivant("emprunt")
    EMPRUNTS[identifiantemprunt] = {
        "id": identifiantemprunt,
        "utilisateur_id": 1,
        "livre_id": 2,
        "date_emprunt": date(2026, 3, 1),
        "date_retour": None,
    }


reset()