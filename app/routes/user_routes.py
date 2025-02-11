from fastapi import APIRouter, HTTPException, Depends, Header
from app.firebase import db, auth
from app.models.user_models import *

app_user = APIRouter(
    prefix="/users",
    tags=["user"],
)



def verify_firebase_token(authorization: str = Header(...)):
    """ Vérifie et décode le token Firebase ID """
    try:
        if not authorization.startswith("Bearer "):
            raise HTTPException(status_code=403, detail="Format du token invalide")

        id_token = authorization.split("Bearer ")[1]
        decoded_token = auth.verify_id_token(id_token)

        return decoded_token
    except Exception:
        raise HTTPException(status_code=401, detail="Token invalide ou expiré")

@app_user.get("/me")
async def get_current_user(user_data: dict = Depends(verify_firebase_token)):
    """ Vérifie l'utilisateur connecté et récupère son rôle """
    email = user_data.get("email")

    for collection in ["clients", "admins", "agents"]:
        doc = db.collection(collection).where("email", "==", email).limit(1).stream()
        doc_list = list(doc)
        if doc_list:
            return {
                "message": "Connexion réussie",
                "user_id": user_data.get("uid"),
                "email": email,
                "role": collection
            }

    raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

@app_user.post("/logout")
async def logout():
    """ Déconnecte l'utilisateur """
    return {"message": "Déconnexion réussie"}
