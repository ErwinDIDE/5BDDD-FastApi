from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.database import Base

class UtilisateurDB(Base):
    __tablename__ = "utilisateurs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nom = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)

    emprunts = relationship("EmpruntDB", back_populates="utilisateur")


class LivreDB(Base):
    __tablename__ = "livres"

    id = Column(Integer, primary_key=True, autoincrement=True)
    titre = Column(String(200), nullable=False)
    auteur = Column(String(100), nullable=False)
    statut = Column(String(20), default="disponible")

    emprunts = relationship("EmpruntDB", back_populates="livre")


class EmpruntDB(Base):
    __tablename__ = "emprunts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    utilisateur_id = Column(Integer, ForeignKey("utilisateurs.id"), nullable=False)
    livre_id = Column(Integer, ForeignKey("livres.id"), nullable=False)
    date_emprunt = Column(Date, nullable=False)
    date_retour = Column(Date, nullable=True)

    utilisateur = relationship("UtilisateurDB", back_populates="emprunts")
    livre = relationship("LivreDB", back_populates="emprunts")
