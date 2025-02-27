from datetime import datetime
import uuid
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

@app_commande.post('/create', response_model=dict)
async def create_commande(commande: CommandeCreateModel):
    commande_dict = commande.dict()
    commande_dict["dateCommande"] = datetime.utcnow().strftime("%Y-%m-%d")

    # Récupérer le produit concerné
    produit_ref = db.collection("produits").document(commande.idProduit)
    produit = produit_ref.get()

    if not produit.exists:
        raise HTTPException(status_code=404, detail="Produit non trouvé")

    produit_data = produit.to_dict()

    if produit_data["qteStock"] < commande.quantite:
        raise HTTPException(status_code=400, detail="Stock insuffisant")

    # Calcul du montant total (prix initial * quantité)
    commande_dict["montantTotal"] = produit_data["prixProduit"] * commande.quantite

    # Déduire la quantité commandée du stock
    produit_ref.update({"qteStock": produit_data["qteStock"] - commande.quantite})

    # Récupérer les informations du client
    client_ref = db.collection("clients").document(commande.idClient)
    client = client_ref.get()

    if not client.exists:
        raise HTTPException(status_code=404, detail="Client non trouvé")

    client_data = client.to_dict()


    # Ajouter la commande à Firestore
    new_commande_ref = db.collection("commandes").add(commande_dict)
    commande_id = new_commande_ref[1].id  # Récupérer l'ID de la commande

    # Ajouter une notification pour l'agent de livraison
    notification = {
    "id": str(uuid.uuid4()),  
    "idCommande": commande_id,
    "idClient": commande.idClient,
    "designationClient": client_data.get("designationClient", "Inconnu"),  # Ajout du nom
    "adresseClient": client_data.get("adresseClient", "Adresse inconnue"),  # Ajout de l'adresse
    "telephoneClient": client_data.get("telephoneClient", "Numéro inconnu"),  # Ajout du téléphone
    "idProduit": commande.idProduit,
    "designationProduit": produit_data["designationProduit"],
    "quantite": commande.quantite,
    "montantTotal": commande_dict["montantTotal"],
    "date": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
    "isRead": False  
    }


    db.collection("notifications").document(notification["id"]).set(notification)

    return {"status": "success", "message": "Commande créée avec succès", "data": commande_dict}

@app_commande.put('/update/{commande_id}', response_model=dict)
async def update_commande(commande_id: str, commande: CommandeUpdateModel):
    commande_ref = db.collection("commandes").document(commande_id)
    commande_data = commande_ref.get()

    if not commande_data.exists:
        raise HTTPException(status_code=404, detail="Commande non trouvée")

    ancienne_commande = commande_data.to_dict()
    updated_data = commande.dict(exclude_unset=True)

    if "dateCommande" in updated_data:
        updated_data["dateCommande"] = updated_data["dateCommande"].strftime("%Y-%m-%d")

    # Vérifier et ajuster le stock si la quantité change
    if "quantite" in updated_data:
        produit_ref = db.collection("produits").document(ancienne_commande["idProduit"])
        produit = produit_ref.get()

        if not produit.exists:
            raise HTTPException(status_code=404, detail="Produit non trouvé")

        produit_data = produit.to_dict()
        difference = updated_data["quantite"] - ancienne_commande["quantite"]

        if produit_data["qteStock"] < difference:
            raise HTTPException(status_code=400, detail="Stock insuffisant")

        # Mettre à jour le stock
        produit_ref.update({"qteStock": produit_data["qteStock"] - difference})

        # Recalcul du montant total (en utilisant le prix initial)
        updated_data["montantTotal"] = produit_data["prixProduit"] * updated_data["quantite"]

    try:
        commande_ref.update(updated_data)
        return {"status": "success", "message": "Commande modifiée avec succès", "data": updated_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la modification: {str(e)}")


@app_commande.delete("/delete/{commande_id}", response_model=dict)
async def delete_commande(commande_id: str):
    commande_ref = db.collection("commandes").document(commande_id)
    commande_data = commande_ref.get()

    if not commande_data.exists:
        raise HTTPException(status_code=404, detail="Commande non trouvée")

    commande = commande_data.to_dict()

    # Récupérer le produit concerné
    produit_ref = db.collection("produits").document(commande["idProduit"])
    produit = produit_ref.get()

    if produit.exists:
        produit_data = produit.to_dict()
        produit_ref.update({"qteStock": produit_data["qteStock"] + commande["quantite"]})

    # Supprimer la commande
    commande_ref.delete()
    return {"status": "success", "message": "Commande supprimée avec succès", "data": commande}