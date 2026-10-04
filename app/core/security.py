import os
from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import UtilisateurDB
from app.schemas import TokenData

# Configuration du hachage des mots de passe
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Clé secrète et configuration JWT (Utilisez une variable d'environnement en production)
SECRET_KEY = os.getenv("SECRET_KEY", "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Indique à FastAPI la route permettant d'obtenir le jeton d'accès
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# ==========================================
# 1. GESTION DES MOTS DE PASSE
# ==========================================

def get_password_hash(password: str) -> str:
    """Hache un mot de passe en clair."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Vérifie un mot de passe en clair contre son hachage."""
    return pwd_context.verify(plain_password, hashed_password)


# ==========================================
# 2. GESTION DES TOKENS JWT
# ==========================================

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Génère un jeton d'accès JWT signé."""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# ==========================================
# 3. DÉPENDANCE D'AUTHENTIFICATION
# ==========================================

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> UtilisateurDB:
    """
    Décode le jeton JWT transmis dans l'en-tête Authorization
    et retourne l'instance de l'utilisateur connecté depuis la BDD.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Impossible de valider les identifiants.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception

    utilisateur = (
        db.query(UtilisateurDB)
        .filter(UtilisateurDB.email == token_data.email)
        .first()
    )
    
    if utilisateur is None:
        raise credentials_exception

    return utilisateur