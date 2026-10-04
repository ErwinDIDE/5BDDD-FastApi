import pytest


@pytest.fixture
def headers_auth(client):
    """Récupère un token JWT valide pour l'utilisateur de démonstration et renvoie les headers d'autorisation."""
    # 1. Utilisation d'un utilisateur présent dans ENREGISTREMENT_UTILISATEURS
    email = "charlie@example.com"
    motdepasse = "password123"

    # 2. Requête d'authentification OAuth2 (Form Data)
    login_res = client.post(
        "/auth/login",
        data={"username": email, "password": motdepasse},
    )

    # Si /auth/login attend du JSON au lieu de Form Data :
    if login_res.status_code != 200:
        login_res = client.post(
            "/auth/login",
            json={"email": email, "motdepasse": motdepasse},
        )

    # Assertion pour identifier directement le problème si la connexion échoue
    assert login_res.status_code == 200, f"Échec de l'authentification : {login_res.text}"

    data = login_res.json()
    token = data.get("access_token") or data.get("token")
    assert token, f"Aucun token trouvé dans la réponse : {data}"

    return {"Authorization": f"Bearer {token}"}


# -----------------------------------------------------------------------------
# Tests
# -----------------------------------------------------------------------------

def test_creer_emprunt_succes(client, headers_auth):
    """Vérifie qu'un utilisateur peut emprunter un livre disponible."""
    payload = {
        "utilisateur_id": 1,
        "livre_id": 1,
    }
    response = client.post("/emprunts", json=payload, headers=headers_auth)
    assert response.status_code == 201


def test_emprunter_livre_deja_emprunte_refuse(client, headers_auth):
    """Vérifie qu'on ne peut pas emprunter un livre déjà indisponible."""
    payload = {"utilisateur_id": 1, "livre_id": 1}

    # Premier emprunt
    r1 = client.post("/emprunts", json=payload, headers=headers_auth)
    assert r1.status_code == 201

    # Second emprunt refusé
    r2 = client.post("/emprunts", json=payload, headers=headers_auth)
    assert r2.status_code in (400, 409)  # Bad Request ou Conflict


def test_emprunter_livre_inexistant(client, headers_auth):
    """Vérifie l'erreur lors de l'emprunt d'un livre inconnu."""
    payload = {"utilisateur_id": 1, "livre_id": 9999}
    response = client.post("/emprunts", json=payload, headers=headers_auth)
    assert response.status_code == 404


def test_emprunter_utilisateur_inexistant(client, headers_auth):
    """Vérifie l'erreur lors de l'emprunt par un utilisateur inconnu."""
    payload = {"utilisateur_id": 9999, "livre_id": 1}
    response = client.post("/emprunts", json=payload, headers=headers_auth)
    assert response.status_code == 404


def test_retourner_livre_emprunte(client, headers_auth):
    """Vérifie qu'un livre peut être retourné."""
    # 1. On crée l'emprunt
    r_emprunt = client.post(
        "/emprunts",
        json={"utilisateur_id": 1, "livre_id": 1},
        headers=headers_auth,
    )
    assert r_emprunt.status_code == 201
    
    # 2. On effectue le retour (adapter la route selon ton API : /emprunts/1/retour ou /emprunts/1)
    emprunt_id = r_emprunt.json().get("id", 1)
    response = client.post(f"/emprunts/{emprunt_id}/retour", headers=headers_auth)
    if response.status_code == 404:
        response = client.put(f"/emprunts/{emprunt_id}", json={"statut": "termine"}, headers=headers_auth)
        
    assert response.status_code == 200