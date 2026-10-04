from datetime import date
from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict, Field


# UTILISATEUR

class UtilisateurCreate(BaseModel):
    nom: str = Field(min_length=1, max_length=100, examples=["Alice Dupont"])
    email: EmailStr = Field(examples=["alice@example.com"])
    telephone: str = Field(min_length=8, max_length=15, examples=["0601020304"])
    motdepasse: str = Field(min_length=6, max_length=100, examples=["motdepasse123"])


class UtilisateurResponse(BaseModel):
    id: int
    nom: str
    email: EmailStr
    telephone: str

    class Config:
        from_attributes = True


# TOKEN & AUTHENTIFICATION (JWT)

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    email: Optional[str] = None


# LIVRE

class LivreCreate(BaseModel):
    titre: str = Field(min_length=1, max_length=200, examples=["Le Comte de Monte-Cristo"])
    auteur: str = Field(min_length=1, max_length=100, examples=["Alexandre Dumas"])
    genre: str = Field(min_length=1, max_length=50, examples=["Aventure"])
    date_publication: Optional[date] = None


class LivreResponse(LivreCreate):
    id: int
    disponible: bool = Field(default=True)

    class Config:
        from_attributes = True


# EMPRUNT

class EmpruntCreate(BaseModel):
    utilisateur_id: int
    livre_id: int


class EmpruntResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    utilisateur_id: int
    livre_id: int
    date_emprunt: date
    date_retour_prevue: date | None = None
    statut: str = "en_cours"