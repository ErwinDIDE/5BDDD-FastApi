def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_liste_livres(client):
    r = client.get("/livres")
    assert r.status_code == 200
    livres = r.json()
    assert len(livres) == 3 
    assert livres[0]["titre"] == "Le Comte de Monte-Cristo"
    assert {"id", "titre", "auteur", "disponible"} <= livres[0].keys()


def test_liste_utilisateurs(client):
    r = client.get("/utilisateurs")
    assert r.status_code == 200
    utilisateurs = r.json()
    assert len(utilisateurs) == 2 
    assert utilisateurs[0]["nom"] == "Alice Dupont"
    assert {"id", "nom", "email", "telephone"} <= utilisateurs[0].keys()
    assert "password" not in utilisateurs[0]  # on vérifie que le mot de passe est bien masqué