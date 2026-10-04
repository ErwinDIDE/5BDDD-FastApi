from fastapi import FastAPI

from app.routers import auth, utilisateurs, livres, emprunts

app = FastAPI(
    title="Gestion de Bibliothèque API",
    description="API de gestion de bibliothèque avec FastAPI",
    version="1.0.0"
)

app.include_router(auth.router)
app.include_router(utilisateurs.router)
app.include_router(livres.router)
app.include_router(emprunts.router)


@app.get("/health", tags=["système"])
def health():
    return {"status": "ok"}