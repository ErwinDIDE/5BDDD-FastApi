# Test de création pour les livres

def test_creer_livre(client, livre_valide):
    r = client.post("/livres", json=livre_valide)
    assert r.status_code == 201
    corps = r.json()
    assert corps["id"] == 4
    assert corps["titre"] == "Le Petit Prince"
    assert client.get("/livres/4").status_code == 200
    assert len(client.get("/livres").json()) == 4


def test_titre_livre_vide_refuse(client, livre_valide):
    r = client.post("/livres", json={**livre_valide, "titre": ""})
    assert r.status_code == 422


def test_auteur_vide_refuse(client, livre_valide):
    r = client.post("/livres", json={**livre_valide, "auteur": ""})
    assert r.status_code == 422


def test_champ_obligatoire_manquant_livre(client):
    r = client.post("/livres", json={"titre": "Sans auteur"})
    assert r.status_code == 422


def test_champs_optionnels_livre(client):
    
    r = client.post(
        "/livres",
        json={"titre": "Minimal", "auteur": "Auteur Anonyme", "genre": "Action", "date_publication": "2026-08-01"}
    )
    assert r.status_code == 201
    assert r.json()["genre"]
    assert r.json()["date_publication"]
    assert r.json()["disponible"] is True

# Test de création pour les utilisateurs

def test_creer_utilisateur(client, utilisateur_valide):
    r = client.post("/utilisateurs/inscription", json=utilisateur_valide)
    assert r.status_code == 201
    corps = r.json()
    assert corps["id"] == 4
    assert corps["nom"] == "Nouvel Utilisateur"
    assert "motdepasse" not in corps
    assert client.get("/utilisateurs/4").status_code == 200
    assert len(client.get("/utilisateurs").json()) == 4


def test_nom_utilisateur_vide_refuse(client, utilisateur_valide):
    r = client.post("/utilisateurs/inscription", json={**utilisateur_valide, "nom": ""})
    assert r.status_code == 422


def test_email_invalide_refuse(client, utilisateur_valide):
    # Validé par pydantic[email] / email-validator
    r = client.post(
        "/utilisateurs/inscription", json={**utilisateur_valide, "email": "mauvais-email"}
    )
    assert r.status_code == 422


def test_mot_de_passe_trop_court_refuse(client, utilisateur_valide):
    # min_length=6 dans le schéma UtilisateurCreate
    r = client.post(
        "/utilisateurs/inscription", json={**utilisateur_valide, "motdepasse": "123"}
    )
    assert r.status_code == 422


def test_champ_obligatoire_manquant_utilisateur(client):
    r = client.post(
        "/utilisateurs/inscription", json={"nom": "Seul", "email": "seul@example.com"}
    )
    assert r.status_code == 422


# def test_champs_optionnels_utilisateur(client):
#     # Test sans numéro de téléphone
#     r = client.post(
#         "/utilisateurs/inscription",
#         json={
#             "nom": "Minimal",
#             "email": "minimal@example.com",
#             "motdepasse": "password123",
#         },
#     )
#     assert r.status_code == 201
#     assert r.json()["telephone"] is None