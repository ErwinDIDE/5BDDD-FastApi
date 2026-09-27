
def test_remplacer_livre(client, livre_valide):
    r = client.put("/livres/1", json=livre_valide)
    assert r.status_code == 200
    assert r.json()["id"] == 1
    assert r.json()["titre"] == "Le Petit Prince"
    assert client.get("/livres/1").json()["titre"] == "Le Petit Prince"


def test_remplacer_livre_inexistant(client, livre_valide):
    r = client.put("/livres/999", json=livre_valide)
    assert r.status_code == 404
    assert r.json() == {"detail": "Livre introuvable"}


def test_remplacer_livre_avec_donnees_invalides(client, livre_valide):
    r = client.put("/livres/1", json={**livre_valide, "titre": ""})
    assert r.status_code == 422


def test_supprimer_livre(client):
    r = client.delete("/livres/1")
    assert r.status_code == 204
    assert r.content == b""
    assert client.get("/livres/1").status_code == 404
    assert len(client.get("/livres").json()) == 2


def test_supprimer_livre_inexistant(client):
    r = client.delete("/livres/999")
    assert r.status_code == 404
    assert r.json() == {"detail": "Livre introuvable"}