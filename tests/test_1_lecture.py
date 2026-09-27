# Tests pour les livres

def test_lire_livre_existant(client):
    r = client.get("/livres/2")
    assert r.status_code == 200
    assert r.json()["titre"] == "1984"
    assert r.json()["id"] == 2


def test_lire_livre_inexistant_renvoie_404(client):
    r = client.get("/livres/999")
    assert r.status_code == 404
    assert r.json() == {"detail": "Livre introuvable"}


def test_id_livre_non_numerique_renvoie_422(client):
    r = client.get("/livres/abc")
    assert r.status_code == 422


# Tests pour les utilisateurs

def test_lire_utilisateur_existant(client):
    r = client.get("/utilisateurs/2")
    assert r.status_code == 200
    assert r.json()["nom"] == "Bob Martin"
    assert r.json()["id"] == 2


def test_lire_utilisateur_inexistant_renvoie_404(client):
    r = client.get("/utilisateurs/999")
    assert r.status_code == 404
    assert r.json() == {"detail": "Utilisateur introuvable"}


def test_id_utilisateur_non_numerique_renvoie_422(client):
    r = client.get("/utilisateurs/abc")
    assert r.status_code == 422