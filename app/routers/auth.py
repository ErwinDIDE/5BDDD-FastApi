from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import UtilisateurDB
from app.schemas import Token
from app.core.security import (
    verify_password,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)

router = APIRouter(prefix="/auth", tags=["Authentification"])


@router.post("/login", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Authentifie un utilisateur et retourne un jeton d'accès JWT.
    
    Remarque : Dans Swagger /docs, le champ 'username' correspond à l'adresse 'email'.
    """
    # 1. Recherche de l'utilisateur par son email (transmis dans form_data.username)
    utilisateur = (
        db.query(UtilisateurDB)
        .filter(UtilisateurDB.email == form_data.username)
        .first()
    )

    # 2. Vérification de l'existence de l'utilisateur et de la validité du mot de passe
    # (Remarque : assurez-vous que le champ dans UtilisateurDB s'appelle motdepasse ou mot_de_passe_hash)
    if not utilisateur or not verify_password(form_data.password, utilisateur.motdepasse):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 3. Génération du token JWT avec l'email en sujet ('sub')
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": utilisateur.email},
        expires_delta=access_token_expires
    )

    # 4. Retour du jeton
    return {"access_token": access_token, "token_type": "bearer"}