from fastapi import APIRouter, HTTPException
from app.firebase import db, auth
from app.models.categorie_models import *
app_categorie = APIRouter(
    prefix="/categories",
    tags= ["categorie"],
)

@app_categorie.post('/create')
async def create_categorie(categorie: CategorieCreateModel):
    categorie_ref = db.collection("categories").where("codeCategorie", "==", categorie.codeCategorie).stream()
    if any(categorie_ref):
        raise HTTPException(status_code=400, detail="Code catégorie déjà utilisé")

    new_categorie_ref = db.collection("categories").add(categorie.dict())
    return {"message": "Catégorie créée avec succès", "designation": new_categorie_ref[2].id}


@app_categorie.get("/get_all", response_model=list)
async def get_categories():
    categories_ref = db.collection("categories").stream()
    categories = [dict(doc.to_dict(), id=doc.id) for doc in categories_ref]
    
    if not categories:
        raise HTTPException(status_code=404, detail="Aucune catégorie trouvée")
    
    return categories

# 🔹 3. Lire une catégorie par ID
@app_categorie.get("/get/{categorie_id}", response_model=Categorie)
async def get_categorie(categorie_id: str):
    categorie_ref = db.collection("categories").document(categorie_id)
    categorie = categorie_ref.get()
    
    if not categorie.exists:
        raise HTTPException(status_code=404, detail="Catégorie non trouvée")
    
    return categorie.to_dict()

# 🔹 4. Mettre à jour une catégorie
@app_categorie.put("/update/{categorie_id}", response_model=dict)
async def update_categorie(categorie_id: str, categorie: CategorieUpdateModel):
    categorie_ref = db.collection("categories").document(categorie_id)
    categorie_data = categorie_ref.get()
    
    if not categorie_data.exists:
        raise HTTPException(status_code=404, detail="Catégorie non trouvée")

    updated_data = categorie.dict(exclude_unset=True)
    categorie_ref.update(updated_data)

    return {"message": f"Catégorie {categorie_id} mise à jour avec succès"}

# 🔹 5. Supprimer une catégorie
@app_categorie.delete("/delete/{categorie_id}", response_model=dict)
async def delete_categorie(categorie_id: str):
    categorie_ref = db.collection("categories").document(categorie_id)
    
    if not categorie_ref.get().exists:
        raise HTTPException(status_code=404, detail="Catégorie non trouvée")

    categorie_ref.delete()
    return {"message": f"Catégorie {categorie_id} supprimée avec succès"}

