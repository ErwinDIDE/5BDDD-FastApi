from fastapi import APIRouter, HTTPException, Query, status

from app import store
from app.schemas import LivreCreate, LivreResponse

router = APIRouter(prefix="/livres", tags=["livres"])


def livre_ou_404(livre_id: int) -> dict:
    livre = store.LIVRES.get(livre_id)
    if livre is None:
        raise HTTPException(status_code=404, detail="Livre introuvable")
    return livre


@router.get("", response_model=list[LivreResponse])
def lister_livres(
    titre: str | None = Query(default=None),
    auteur: str | None = Query(default=None),
    genre: str | None = Query(default=None)
):
    livres = list(store.LIVRES.values())
    if titre:
        livres = [l for l in livres if titre.lower() in l["titre"].lower()]
    if auteur:
        livres = [l for l in livres if auteur.lower() in l["auteur"].lower()]
    if genre:
        livres = [l for l in livres if genre.lower() in l["genre"].lower()]
    return livres


@router.get("/{livre_id}", response_model=LivreResponse)
def lire_livre(livre_id: int):
    return livre_ou_404(livre_id)


@router.post("", response_model=LivreResponse, status_code=status.HTTP_201_CREATED)
def ajouter_livre(livre: LivreCreate):
    identifiantlivre = store.id_suivant("livre")
    nouveau = {
        "id": identifiantlivre,
        "disponible": True,
        **livre.model_dump()
    }
    store.LIVRES[identifiantlivre] = nouveau
    return nouveau


@router.put("/{livre_id}", response_model=LivreResponse)
def modifier_livre(livre_id: int, livre: LivreCreate):
    livre_existant = livre_ou_404(livre_id)
    
    store.LIVRES[livre_id] = {
        "id": livre_id,
        "disponible": livre_existant.get("disponible", True),
        **livre.model_dump()
    }
    return store.LIVRES[livre_id]


@router.delete("/{livre_id}", status_code=status.HTTP_204_NO_CONTENT)
def supprimer_livre(livre_id: int):
    livre_ou_404(livre_id)
    del store.LIVRES[livre_id]
    
    # Nettoyage des emprunts associés à ce livre
    emprunts_a_supprimer = [
        identifiantemprunt for identifiantemprunt, emprunt in store.EMPRUNTS.items() if emprunt["livre_id"] == livre_id
    ]
    for identifiantemprunt in emprunts_a_supprimer:
        del store.EMPRUNTS[identifiantemprunt]
        
    return None