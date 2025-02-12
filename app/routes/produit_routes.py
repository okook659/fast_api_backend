from fastapi import APIRouter, HTTPException
from app.firebase import db, auth
from app.models.produit_models import *
app_produit = APIRouter(
    prefix='/produits',
    tags=['produit']
)

@app_produit.post('/create')
async def create_product(produit_data: ProduitCreateModel):
    produit_ref = db.collection('produits').where("designationProduit" ,"==", produit_data.designationProduit).stream()
    if any(produit_ref):
        raise HTTPException(status_code=400, detail="Ce produit existe déjà!")
    
    new_produit_ref = db.collection('produits').add(produit_data.dict())
    return {"message": "Produit créé avec succès"}

@app_produit.get('/get_all')
async def get_produits():
    produits_ref = db.collection("produits").stream()
    produits = [dict(doc.to_dict(), id=doc.id) for doc in produits_ref]

    if not produits:
        raise HTTPException(status_code=404, detail="Aucun produit trouvé")
    
    return produits

@app_produit.get("/get/{produit_designation}", response_model=Produit)
async def get_produit(produit_designation: str):
    produit_ref = db.collection("produits").where("designationProduit", "==", produit_designation).stream()
    