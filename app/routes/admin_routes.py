from fastapi import APIRouter, HTTPException
from app.firebase import db, auth
from app.models.admin_models import *
from app.utils import get_user_role
app_admin = APIRouter(
    prefix="/admins",
    tags= ["admin"],
)

@app_admin.post("/create")
async def create_admin(admin_data: AdminCreateModel):
    try:
        auth.get_user_by_email(admin_data.email)  # Si l'email existe, une exception sera levée
        raise HTTPException(status_code=400, detail="Email already in use")
    except auth.UserNotFoundError:
        pass
    try:
        user_record = auth.create_user(
            email=admin_data.email,
            password=admin_data.password
        )
        uid = user_record.uid  # Récupérer l'UID généré par Firebase

        # 🔹 2. Stocker les infos du admin dans Firestore
        admin_dict = admin_data.dict()
        del admin_dict["password"]  # Sécurité : ne jamais stocker le mot de passe
        admin_dict["uid"] = uid  # Associer l'UID Firebase

        db.collection("admins").document(uid).set(admin_dict)

        return {"message": f"Admin {admin_data.email} créé avec succès", "uid": uid}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la création du admin: {str(e)}")

@app_admin.put("/update/{admin_id}")
async def update_admin(admin_id: str, admin: AdminUpdateModel):
    admin_data = admin.dict(exclude_unset=True)
    doc_ref = db.collection("admins").document(admin_id)
    doc = doc_ref.get()
    if not doc.exists:
        raise HTTPException(status_code=404, detail="Admin not found")
    old_email = doc.to_dict().get('email')
    if old_email != admin.email:
        try:
            # Vérifier si un utilisateur existe avec le nouvel email
            auth.get_user_by_email(admin.email)  # Si l'email existe, une exception sera levée
            raise HTTPException(status_code=400, detail="Email already in use")
        except auth.UserNotFoundError:
            pass
        try:
            # Vérifier que l'email existe avant d'essayer de l'actualiser
            user = auth.get_user_by_email(old_email)  # Récupérer l'utilisateur par l'email existant
            # Mettre à jour l'email dans Firebase
            auth.update_user(user.uid, email=admin.email)
        except auth.UserNotFoundError:
            raise HTTPException(status_code=404, detail="User not found in Firebase Authentication")
        except auth.EmailAlreadyExistsError:
            raise HTTPException(status_code=400, detail="Email already in use")

    # Mettre à jour le mot de passe si nécessaire
    if admin.password:
        try:
            user = auth.get_user_by_email(admin.email)  # Récupérer l'utilisateur par le nouvel email
            auth.update_user(user.uid, password=admin.password)  # Mettre à jour le mot de passe
        except auth.UserNotFoundError:
            raise HTTPException(status_code=404, detail="User not found in Firebase Authentication")

    # Mettre à jour le document Firestore du admin
    doc_ref.update(admin_data)
    
    return {"message": f"Admin {admin_id} updated successfully"}



# @app_admin.delete("/delete/{admin_id}")
# async def delete_admin(admin_id: str):
#     doc_ref = db.collection("admins").document(admin_id)
#     doc = doc_ref.get()
    
#     if not doc.exists:
#         raise HTTPException(status_code=404, detail="Admin not found")
    
#     doc_ref.delete()
#     return {"message": f"Admin {admin_id} deleted successfully"}