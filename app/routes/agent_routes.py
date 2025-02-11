from fastapi import APIRouter, HTTPException
from app.firebase import db, auth
from app.models.agent_models import *
from app.utils import get_user_role
app_agent = APIRouter(
    prefix="/agents",
    tags= ["agent"],
)

@app_agent.post("/create")
async def create_agent(agent_data: AgentCreateModel):
    try:
        auth.get_user_by_email(agent_data.email)  # Si l'email existe, une exception sera levée
        raise HTTPException(status_code=400, detail="Email already in use")
    except auth.UserNotFoundError:
        pass
    try:
        user_record = auth.create_user(
            email=agent_data.email,
            password=agent_data.password
        )
        uid = user_record.uid  # Récupérer l'UID généré par Firebase

        # 🔹 2. Stocker les infos du agent dans Firestore
        agent_dict = agent_data.dict()
        del agent_dict["password"]  # Sécurité : ne jamais stocker le mot de passe
        agent_dict["uid"] = uid  # Associer l'UID Firebase

        db.collection("agents").document(uid).set(agent_dict)

        return {"message": f"Agent {agent_data.email} créé avec succès", "uid": uid}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la création du agent: {str(e)}")

@app_agent.put("/update/{agent_id}")
async def update_agent(agent_id: str, agent: AgentUpdateModel):
    agent_data = agent.dict(exclude_unset=True)
    doc_ref = db.collection("agents").document(agent_id)
    doc = doc_ref.get()
    if not doc.exists:
        raise HTTPException(status_code=404, detail="Agent not found")
    old_email = doc.to_dict().get('email')
    if old_email != agent.email:
        try:
            # Vérifier si un utilisateur existe avec le nouvel email
            auth.get_user_by_email(agent.email)  # Si l'email existe, une exception sera levée
            raise HTTPException(status_code=400, detail="Email already in use")
        except auth.UserNotFoundError:
            pass
        try:
            # Vérifier que l'email existe avant d'essayer de l'actualiser
            user = auth.get_user_by_email(old_email)  # Récupérer l'utilisateur par l'email existant
            # Mettre à jour l'email dans Firebase
            auth.update_user(user.uid, email=agent.email)
        except auth.UserNotFoundError:
            raise HTTPException(status_code=404, detail="User not found in Firebase Authentication")
        except auth.EmailAlreadyExistsError:
            raise HTTPException(status_code=400, detail="Email already in use")

    # Mettre à jour le mot de passe si nécessaire
    if agent.password:
        try:
            user = auth.get_user_by_email(agent.email)  # Récupérer l'utilisateur par le nouvel email
            auth.update_user(user.uid, password=agent.password)  # Mettre à jour le mot de passe
        except auth.UserNotFoundError:
            raise HTTPException(status_code=404, detail="User not found in Firebase Authentication")

    # Mettre à jour le document Firestore du agent
    doc_ref.update(agent_data)
    
    return {"message": f"Agent {agent_id} updated successfully"}



@app_agent.delete("/delete/{agent_id}")
async def delete_agent(agent_id: str):
    doc_ref = db.collection("agents").document(agent_id)
    doc = doc_ref.get()
    
    if not doc.exists:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    doc_ref.delete()
    return {"message": f"Agent {agent_id} deleted successfully"}