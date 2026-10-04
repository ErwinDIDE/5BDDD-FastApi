from datetime import date, timedelta
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.database import get_db
from app.models import EmpruntDB, LivreDB, UtilisateurDB
from app.schemas import EmpruntCreate, EmpruntResponse

router = APIRouter(prefix="/emprunts", tags=["Emprunts"])


@router.post("", response_model=EmpruntResponse, status_code=status.HTTP_201_CREATED)
def emprunter_livre(
    emprunt_in: EmpruntCreate,
    db: Session = Depends(get_db),
    current_user: UtilisateurDB = Depends(get_current_user),
):
    # 1. Vérification de l'existence de l'utilisateur demandé dans le body
    user_cible = (
        db.query(UtilisateurDB)
        .filter(UtilisateurDB.id == emprunt_in.utilisateur_id)
        .first()
    )
    if not user_cible:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utilisateur non trouvé.",
        )

    # 2. Vérification de l'existence du livre
    livre = db.query(LivreDB).filter(LivreDB.id == emprunt_in.livre_id).first()
    if not livre:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Livre non trouvé.",
        )

    # 3. Vérification de la disponibilité du livre
    if not livre.disponible:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ce livre est déjà emprunté.",
        )

    # 4. Enregistrement de l'emprunt
    date_emprunt = date.today()
    date_retour_prevue = date_emprunt + timedelta(days=14)

    nouvel_emprunt = EmpruntDB(
        utilisateur_id=emprunt_in.utilisateur_id,
        livre_id=livre.id,
        date_emprunt=date_emprunt,
        date_retour_prevue=date_retour_prevue,
        statut="en_cours",
    )

    # Mise à jour du statut du livre
    livre.disponible = False

    db.add(nouvel_emprunt)
    db.commit()
    db.refresh(nouvel_emprunt)
    return nouvel_emprunt


@router.get("/mes-emprunts", response_model=List[EmpruntResponse])
def lister_mes_emprunts(
    db: Session = Depends(get_db),
    current_user: UtilisateurDB = Depends(get_current_user),
):
    return (
        db.query(EmpruntDB)
        .filter(EmpruntDB.utilisateur_id == current_user.id)
        .all()
    )


@router.post("/{emprunt_id}/retour", response_model=EmpruntResponse)
def retourner_livre(
    emprunt_id: int,
    db: Session = Depends(get_db),
    current_user: UtilisateurDB = Depends(get_current_user),
):
    # Recherche de l'emprunt par son ID
    emprunt = (
        db.query(EmpruntDB)
        .filter(EmpruntDB.id == emprunt_id)
        .first()
    )

    if not emprunt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Emprunt non trouvé.",
        )

    if emprunt.statut in ["RETOURNE", "retourne"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ce livre a déjà été retourné.",
        )

    # Mise à jour du statut et libération du livre
    emprunt.statut = "RETOURNE"

    livre = db.query(LivreDB).filter(LivreDB.id == emprunt.livre_id).first()
    if livre:
        livre.disponible = True

    db.commit()
    db.refresh(emprunt)
    return emprunt