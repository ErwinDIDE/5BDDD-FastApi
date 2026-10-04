import pytest
from fastapi.testclient import TestClient

from app.core.security import get_password_hash
from app.database import Base, engine, get_db
from app.main import app
from app.models import LivreDB, UtilisateurDB
from app.store import ENREGISTREMENT_LIVRES, ENREGISTREMENT_UTILISATEURS


# @pytest.fixture(autouse=True)
# def reinitialiser_store():
#     # Réinitialise le store avant chaque test
#     store.reset()

@pytest.fixture(autouse=True)
def reinitialiser_db():
    # 1. On vide et on re-crée toutes les tables SQLite
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    # 2. On injecte les données initiales requises par les tests
    db = next(get_db())
    try:
        for u in ENREGISTREMENT_UTILISATEURS:
            u_copy = u.copy()
            # 🔒 On hache les mots de passe pour que l'auth / login fonctionne dans les tests
            u_copy["motdepasse"] = get_password_hash(u_copy["motdepasse"])
            db.add(UtilisateurDB(**u_copy))

        for l in ENREGISTREMENT_LIVRES:
            db.add(LivreDB(**l))

        db.commit()
    finally:
        db.close()


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture
def utilisateur_valide():
    return {
        "nom": "Nouvel Utilisateur",
        "email": "nouvelutilisateur@example.com",
        "telephone": "0611223344",
        "motdepasse": "password123",
    }


@pytest.fixture
def livre_valide():
    return {
        "titre": "Le Petit Prince",
        "auteur": "Antoine de Saint-Exupéry",
        "genre": "Conte",
        "date_publication": "1943-04-06",
    }