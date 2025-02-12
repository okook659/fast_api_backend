from fastapi import APIRouter, HTTPException
from app.firebase import db, auth
from app.models.client_models import *
from app.utils import get_user_role


app_client = APIRouter(
    prefix="/clients",
    tags= ["client"],
)

@app_client.get("/get_all")
async def get_clients():
    clients_ref = db.collection("clients").stream()
    clients = [dict(doc.to_dict(), id=doc.id) for doc in clients_ref]
    if not clients:
        raise HTTPException(status_code=404, detail="Aucun client trouvé")
    return clients

@app_client.get("/get/{client_id}")
async def get_client(client_id: str):
    doc_ref = db.collection("clients").document(client_id).get()

    if not doc_ref.exists:
        raise HTTPException(status_code=404, detail="Aucun client trouvé")

    return {"document_id": doc_ref.id, **doc_ref.to_dict()}


@app_client.post("/create")
async def create_client(client_data: ClientCreateModel):
    try:
        auth.get_user_by_email(client_data.email)  # Si l'email existe, une exception sera levée
        raise HTTPException(status_code=400, detail="Email already in use")
    except auth.UserNotFoundError:
        pass
    try:
        user_record = auth.create_user(
            email=client_data.email,
            password=client_data.password
        )
        uid = user_record.uid  # Récupérer l'UID généré par Firebase

        # 🔹 2. Stocker les infos du client dans Firestore
        client_dict = client_data.dict()
        del client_dict["password"]  # Sécurité : ne jamais stocker le mot de passe
        client_dict["uid"] = uid  # Associer l'UID Firebase

        db.collection("clients").document(uid).set(client_dict)

        return {"message": f"Client {client_data.email} créé avec succès", "uid": uid}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la création du client: {str(e)}")

@app_client.put("/{client_id}")
async def update_client(client_id: str, client: ClientUpdateModel):
    # Récupérer les données du client
    client_data = client.dict(exclude_unset=True)
    doc_ref = db.collection("clients").document(client_id)
    doc = doc_ref.get()

    if not doc.exists:
        raise HTTPException(status_code=404, detail="Client not found")
    
    # Récupérer l'utilisateur actuel (ancien email)
    old_email = doc.to_dict().get('email')

    if old_email != client.email:
        try:
            # Vérifier si un utilisateur existe avec le nouvel email
            auth.get_user_by_email(client.email)  # Si l'email existe, une exception sera levée
            raise HTTPException(status_code=400, detail="Email already in use")
        except auth.UserNotFoundError:
            pass
        
        try:
            # Vérifier que l'email existe avant d'essayer de l'actualiser
            user = auth.get_user_by_email(old_email)  # Récupérer l'utilisateur par l'email existant
            # Mettre à jour l'email dans Firebase
            auth.update_user(user.uid, email=client.email)
        except auth.UserNotFoundError:
            raise HTTPException(status_code=404, detail="User not found in Firebase Authentication")
        except auth.EmailAlreadyExistsError:
            raise HTTPException(status_code=400, detail="Email already in use")

    # Mettre à jour le mot de passe si nécessaire
    if client.password:
        try:
            user = auth.get_user_by_email(client.email)  # Récupérer l'utilisateur par le nouvel email
            auth.update_user(user.uid, password=client.password)  # Mettre à jour le mot de passe
        except auth.UserNotFoundError:
            raise HTTPException(status_code=404, detail="User not found in Firebase Authentication")

    # Mettre à jour le document Firestore du client
    doc_ref.update(client_data)
    
    return {"message": f"Client {client_id} updated successfully"}



@app_client.delete("/delete/{client_id}")
async def delete_client(client_id: str):
    doc_ref = db.collection("clients").document(client_id)
    doc = doc_ref.get()
    
    if not doc.exists:
        raise HTTPException(status_code=404, detail="Client not found")
    
    doc_ref.delete()
    return {"message": f"Client {client_id} deleted successfully"}