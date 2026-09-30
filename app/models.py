from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date, Identity, Sequence
from sqlalchemy.orm import relationship
from app.database import Base

class UtilisateurDB(Base):
    __tablename__ = "utilisateurs"

    id = Column(Integer, Identity(always=False, start=1), primary_key=True)
    nom = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    motdepasse = Column(String(255), nullable=False)
    telephone = Column(String(20), nullable=True)

    emprunts = relationship("EmpruntDB", back_populates="utilisateur")

livres_id_seq = Sequence('livres_id_seq', start=1, increment=1)

class LivreDB(Base):
    __tablename__ = "livres"

    id = Column(
        Integer, 
        livres_id_seq, 
        primary_key=True, 
        server_default=livres_id_seq.next_value()
    )
    titre = Column(String(200), nullable=False)
    auteur = Column(String(100), nullable=False)
    genre = Column(String(50), nullable=True)
    date_publication = Column(
        Date, nullable=True
    )
    disponible = Column(Boolean, default=True)

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
