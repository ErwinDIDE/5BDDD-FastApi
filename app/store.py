from datetime import date
from app.core.security import get_password_hash

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
    {
        "nom": "Charlie Brown",
        "email": "charlie@example.com",
        "telephone": "0611223344",
        "motdepasse": "password123",
    },
]

ENREGISTREMENT_LIVRES = [
    {
        "titre": "Le Petit Prince",
        "auteur": "Antoine de Saint-Exupéry",
        "genre": "Conte",
        "date_publication": date(1943, 4, 6),
        "disponible": True,
    },
    {
        "titre": "1984",
        "auteur": "George Orwell",
        "genre": "Dystopie",
        "date_publication": date(1949, 6, 8),
        "disponible": False,
    },
    {
        "titre": "L'Étranger",
        "auteur": "Albert Camus",
        "genre": "Roman",
        "date_publication": date(1942, 5, 19),
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

    # Initialisation des utilisateurs avec hachage du mot de passe
    for u in ENREGISTREMENT_UTILISATEURS:
        identifiantutilisateur = id_suivant("utilisateur")
        # On crée une copie pour ne pas altérer le dictionnaire d'origine
        user_data = u.copy()
        
        # Hachage avant le stockage
        user_data["motdepasse"] = get_password_hash(user_data["motdepasse"])
        
        UTILISATEURS[identifiantutilisateur] = {
            "id": identifiantutilisateur,
            **user_data,
        }

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