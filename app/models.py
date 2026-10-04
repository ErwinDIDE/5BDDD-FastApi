from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date, Sequence
from sqlalchemy.orm import relationship
from app.database import Base

# Séquences Oracle
utilisateurs_id_seq = Sequence('utilisateurs_id_seq', start=1, increment=1)
livres_id_seq = Sequence('livres_id_seq', start=1, increment=1)
emprunts_id_seq = Sequence('emprunts_id_seq', start=1, increment=1)


class UtilisateurDB(Base):
    __tablename__ = "utilisateurs"

    id = Column(
        Integer, 
        utilisateurs_id_seq, 
        primary_key=True, 
        server_default=utilisateurs_id_seq.next_value()
    )
    nom = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    motdepasse = Column(String(255), nullable=False)
    telephone = Column(String(20), nullable=True)

    emprunts = relationship("EmpruntDB", back_populates="utilisateur")


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
    date_publication = Column(Date, nullable=True)
    disponible = Column(Boolean, default=True)

    emprunts = relationship("EmpruntDB", back_populates="livre")


class EmpruntDB(Base):
    __tablename__ = "emprunts"

    id = Column(
        Integer, 
        emprunts_id_seq, 
        primary_key=True, 
        server_default=emprunts_id_seq.next_value()
    )
    utilisateur_id = Column(Integer, ForeignKey("utilisateurs.id"), nullable=False)
    livre_id = Column(Integer, ForeignKey("livres.id"), nullable=False)
    date_emprunt = Column(Date, nullable=False)
    date_retour_prevue = Column(Date, nullable=True)
    statut = Column(String(50), nullable=True)

    utilisateur = relationship("UtilisateurDB", back_populates="emprunts")
    livre = relationship("LivreDB", back_populates="emprunts")