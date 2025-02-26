from datetime import datetime
from fastapi import APIRouter, HTTPException
from app.firebase import db, auth
from app.models.commande_models import *
app_commande = APIRouter(
    prefix="/commandes",
    tags= ["commande"],
)

@app_commande.get("/get_all", response_model=list)
async def get_commandes():
    commandes_ref = db.collection("commandes").stream()
    commandes = [dict(doc.to_dict(), id=doc.id) for doc in commandes_ref]

    if not commandes:
        raise HTTPException(status_code=404, detail="Aucune commande trouvée")
    
    return commandes

@app_commande.get('/get/{commande_id}', response_model=Commande)
async def get_commande(commande_id:  str):
    commande_ref = db.collection('commandes').document(commande_id)
    commande = commande_ref.get()

    if not commande.exists:
        raise HTTPException(status_code=404, detail="Commande non trouvée")
    
    commande_dict = commande.to_dict()
    commande_dict['id'] = commande_id
    return commande_dict

@app_commande.post('/create')
async def create_commande(commande: CommandeCreateModel):
    commande_dict = commande.dict()
    commande_dict["dateCommande"] = commande.dateCommande.strftime("%Y-%m-%d")  # Convertir en string
    new_commande_ref = db.collection("commandes").add(commande_dict)

    return {"message": "Commande créée avec succès"}


@app_commande.put('/update/{commande_id}', response_model=dict)
async def update_commande(commande_id: str, commande:CommandeUpdateModel):
    commande_ref = db.collection("commandes").document(commande_id)
    commande_data = commande_ref.get()

    if not commande_data.exists:
        raise HTTPException(status_code=404, detail="Commande non trouvée")
    updated_data = commande.dict(exclude_unset=True)
    if "dateCommande" in updated_data:
        updated_data["dateCommande"] = updated_data["dateCommande"].strftime("%Y-%m-%d")
    try:
        commande_ref.update(updated_data)
        return {"message": "Commande modifiée avec succès"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la modification: {str(e)}")
   

@app_commande.delete("/delete/{commande_id}", response_model=dict)
async def delete_commande(commande_id: str):
    commande_ref = db.collection("commandes").document(commande_id)

    if not commande_ref.get().exists:
        raise HTTPException(status_code=404, detail="Commande non trouvée")
    
    commande_ref.delete()
    return {"message": "Commande supprimée avec succès"}