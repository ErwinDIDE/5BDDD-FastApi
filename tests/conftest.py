import pytest
from fastapi.testclient import TestClient

from app import store
from app.main import app


@pytest.fixture
def client():
    store.reset()
    return TestClient(app)


@pytest.fixture
def utilisateur_valide():
    return {
        "nom": "Charlie Brown",
        "email": "charlie@example.com",
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