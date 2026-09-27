from fastapi import APIRouter, HTTPException, Query, status

from app import store
from app.schemas import UtilisateurCreate, UtilisateurResponse, EmpruntResponse

router = APIRouter(prefix="/utilisateurs", tags=["utilisateurs"])


def utilisateur_ou_404(utilisateur_id: int) -> dict:
    utilisateur = store.UTILISATEURS.get(utilisateur_id)
    if utilisateur is None:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")
    return utilisateur


@router.get("", response_model=list[UtilisateurResponse])
def lister_utilisateurs(q: str | None = Query(default=None)):
    utilisateurs = list(store.UTILISATEURS.values())
    if q:
        utilisateurs = [
            u for u in utilisateurs 
            if q.lower() in u["nom"].lower() or q.lower() in u["email"].lower()
        ]
    return utilisateurs


@router.get("/{utilisateur_id}", response_model=UtilisateurResponse)
def lire_utilisateur(utilisateur_id: int):
    return utilisateur_ou_404(utilisateur_id)


@router.post("/inscription", response_model=UtilisateurResponse, status_code=status.HTTP_201_CREATED)
def inscrire_utilisateur(utilisateur: UtilisateurCreate):
    # Vérification de l'unicité de l'email
    if any(u["email"] == utilisateur.email for u in store.UTILISATEURS.values()):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Cet email est déjà utilisé"
        )
    
    identifiantutilisateur = store.id_suivant("utilisateur")
    nouveau = {
        "id": identifiantutilisateur,
        "nom": utilisateur.nom,
        "email": utilisateur.email,
        "telephone": utilisateur.telephone,
        # Enregistrement du mot de passe
        "motdepasse": utilisateur.motdepasse 
    }
    store.UTILISATEURS[identifiantutilisateur] = nouveau
    return nouveau


@router.put("/{utilisateur_id}", response_model=UtilisateurResponse)
def modifier_utilisateur(utilisateur_id: int, utilisateur: UtilisateurCreate):
    utilisateur_ou_404(utilisateur_id)
    
    # Vérification de l'unicité de l'email si modifié
    if any(u["email"] == utilisateur.email and u["id"] != utilisateur_id for u in store.UTILISATEURS.values()):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Cet email est déjà utilisé par un autre utilisateur"
        )

    store.UTILISATEURS[utilisateur_id] = {
        "id": utilisateur_id,
        "nom": utilisateur.nom,
        "email": utilisateur.email,
        "telephone": utilisateur.telephone,
        "motdepasse": utilisateur.motdepasse
    }
    return store.UTILISATEURS[utilisateur_id]


@router.delete("/{utilisateur_id}", status_code=status.HTTP_204_NO_CONTENT)
def supprimer_utilisateur(utilisateur_id: int):
    utilisateur_ou_404(utilisateur_id)
    del store.UTILISATEURS[utilisateur_id]
    
    # Nettoyage des emprunts associés à cet utilisateur
    emprunts_a_supprimer = [
        lid for lid, loan in store.EMPRUNTS.items() if loan["user_id"] == utilisateur_id
    ]
    for lid in emprunts_a_supprimer:
        del store.EMPRUNTS[lid]
        
    return None


@router.get("/{utilisateur_id}/emprunts", response_model=list[EmpruntResponse])
def emprunts_utilisateur(utilisateur_id: int):
    utilisateur_ou_404(utilisateur_id)
    emprunts = [
        loan for loan in store.EMPRUNTS.values() if loan["user_id"] == utilisateur_id
    ]
    return emprunts