from firebase_admin import firestore

db = firestore.client()

def get_user_role(user_id: str):
    """
    Vérifie dans quelle collection (admins, agents, clients) se trouve l'utilisateur
    et retourne le rôle en fonction du document trouvé.
    """
    for collection in ["admins", "agents", "clients"]:
        doc_ref = db.collection(collection).document(user_id)
        if doc_ref.get().exists:
            return collection  # Retourne le nom du document (rôle)
    return None  # L'utilisateur n'existe dans aucune collection
