from datetime import date, timedelta
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import EmpruntDB, LivreDB, UtilisateurDB
from app.schemas import EmpruntCreate, EmpruntResponse

# On importe la dépendance pour récupérer l'utilisateur connecté via le JWT
from app.core.security import get_current_user

router = APIRouter(prefix="/emprunts", tags=["Emprunts"])


@router.post("", response_model=EmpruntResponse, status_code=status.HTTP_201_CREATED)
def emprunter_livre(
    emprunt_in: EmpruntCreate,
    db: Session = Depends(get_db),
    current_user: UtilisateurDB = Depends(get_current_user),
):
    # L'utilisateur peut emprunter un livre disponible
    # On vérifie si le livre existe
    livre = db.query(LivreDB).filter(LivreDB.id == emprunt_in.livre_id).first()
    if not livre:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Livre non trouvé.",
        )

    # On vérifie si le livre est disponible
    if not livre.disponible:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ce livre est déjà emprunté.",
        )

    # On crée l'enregistrement d'emprunt
    date_emprunt = date.today()
    date_retour_prevue = date_emprunt + timedelta(days=14)

    nouvel_emprunt = EmpruntDB(
        utilisateur_id=current_user.id,
        livre_id=livre.id,
        date_emprunt=date_emprunt,
        date_retour_prevue=date_retour_prevue,
        statut="EN_COURS",
    )

    # Mis à jour du statut du livre
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
    
    emprunts = (
        db.query(EmpruntDB)
        .filter(EmpruntDB.utilisateur_id == current_user.id)
        .all()
    )
    return emprunts


@router.put("/{emprunt_id}/retour", response_model=EmpruntResponse)
def retourner_livre(
    emprunt_id: int,
    db: Session = Depends(get_db),
    current_user: UtilisateurDB = Depends(get_current_user),
):
    # On marque un emprunt comme retourné et on rend le livre disponible

    emprunt = (
        db.query(EmpruntDB)
        .filter(
            EmpruntDB.id == emprunt_id,
            EmpruntDB.utilisateur_id == current_user.id,
        )
        .first()
    )

    if not emprunt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Emprunt non trouvé.",
        )

    if emprunt.statut == "RETOURNE":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ce livre a déjà été retourné.",
        )

    # Mettre à jour l'emprunt et rendre le livre disponible
    emprunt.statut = "RETOURNE"
    emprunt.date_retour_effective = date.today()

    livre = db.query(LivreDB).filter(LivreDB.id == emprunt.livre_id).first()
    if livre:
        livre.disponible = True

    db.commit()
    db.refresh(emprunt)
    return emprunt