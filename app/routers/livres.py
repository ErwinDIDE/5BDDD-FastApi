from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import EmpruntDB, LivreDB
from app.schemas import LivreCreate, LivreResponse

router = APIRouter(prefix="/livres", tags=["livres"])


# def livre_ou_404(livre_id: int) -> dict:
#     livre = store.LIVRES.get(livre_id)
#     if livre is None:
#         raise HTTPException(status_code=404, detail="LivreDB introuvable")
#     return livre

def livre_ou_404(livre_id: int, db: Session) -> LivreDB:
    livre = db.get(LivreDB, livre_id)
    if livre is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Livre introuvable"
        )
    return livre


# @router.get("", response_model=list[LivreResponse])
# def lister_livres(
#     titre: str | None = Query(default=None),
#     auteur: str | None = Query(default=None),
#     genre: str | None = Query(default=None)
# ):
#     livres = list(store.LIVRES.values())
#     if titre:
#         livres = [l for l in livres if titre.lower() in l["titre"].lower()]
#     if auteur:
#         livres = [l for l in livres if auteur.lower() in l["auteur"].lower()]
#     if genre:
#         livres = [l for l in livres if genre.lower() in l["genre"].lower()]
#     return livres

@router.get("", response_model=list[LivreResponse])
def lister_livres(
    titre: str | None = Query(default=None),
    auteur: str | None = Query(default=None),
    genre: str | None = Query(default=None),
    db: Session = Depends(get_db),
):
    stmt = select(LivreDB)

    # Filtrage insensible à la casse avec icontains / ilike
    if titre:
        stmt = stmt.where(LivreDB.titre.icontains(titre))
    if auteur:
        stmt = stmt.where(LivreDB.auteur.icontains(auteur))
    if genre:
        stmt = stmt.where(LivreDB.genre.icontains(genre))

    return db.scalars(stmt).all()


# @router.get("/{livre_id}", response_model=LivreResponse)
# def lire_livre(livre_id: int):
#     return livre_ou_404(livre_id)

@router.get("/{livre_id}", response_model=LivreResponse)
def lire_livre(livre_id: int, db: Session = Depends(get_db)):
    return livre_ou_404(livre_id, db)


# @router.post("", response_model=LivreResponse, status_code=status.HTTP_201_CREATED)
# def ajouter_livre(livre: LivreCreate):
#     identifiantlivre = store.id_suivant("livre")
#     nouveau = {
#         "id": identifiantlivre,
#         "disponible": True,
#         **livre.model_dump()
#     }
#     store.LIVRES[identifiantlivre] = nouveau
#     return nouveau

@router.post("", response_model=LivreResponse, status_code=status.HTTP_201_CREATED)
def ajouter_livre(livre_in: LivreCreate, db: Session = Depends(get_db)):
    # Si 'disponible' n'est pas dans LivreCreate, passez-le explicitement :
    nouveau_livre = LivreDB(**livre_in.model_dump(), disponible=True)

    db.add(nouveau_livre)
    db.commit()
    db.refresh(nouveau_livre)
    return nouveau_livre


# @router.put("/{livre_id}", response_model=LivreResponse)
# def modifier_livre(livre_id: int, livre: LivreCreate):
#     livre_existant = livre_ou_404(livre_id)
    
#     store.LIVRES[livre_id] = {
#         "id": livre_id,
#         "disponible": livre_existant.get("disponible", True),
#         **livre.model_dump()
#     }
#     return store.LIVRES[livre_id]

@router.put("/{livre_id}", response_model=LivreResponse)
def modifier_livre(
    livre_id: int,
    livre_in: LivreCreate,
    db: Session = Depends(get_db),
):
    livre_db = livre_ou_404(livre_id, db)

    for key, value in livre_in.model_dump().items():
        setattr(livre_db, key, value)

    db.commit()
    db.refresh(livre_db)

    return livre_db


# @router.delete("/{livre_id}", status_code=status.HTTP_204_NO_CONTENT)
# def supprimer_livre(livre_id: int):
#     livre_ou_404(livre_id)
#     del store.LIVRES[livre_id]
    
#     # Nettoyage des emprunts associés à ce livre
#     emprunts_a_supprimer = [
#         identifiantemprunt for identifiantemprunt, emprunt in store.EMPRUNTS.items() if emprunt["livre_id"] == livre_id
#     ]
#     for identifiantemprunt in emprunts_a_supprimer:
#         del store.EMPRUNTS[identifiantemprunt]
        
#     return None

@router.delete("/{livre_id}", status_code=status.HTTP_204_NO_CONTENT)
def supprimer_livre(livre_id: int, db: Session = Depends(get_db)):
    livre_ou_404(livre_id, db)

    # Suppression en cascade des emprunts liés
    stmt_emprunts = delete(EmpruntDB).where(EmpruntDB.livre_id == livre_id)
    db.execute(stmt_emprunts)

    # Suppression du livre
    livre = db.get(LivreDB, livre_id)
    if livre:
        db.delete(livre)

    db.commit()
    return None