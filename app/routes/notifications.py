from fastapi import APIRouter, HTTPException
from app.firebase import db

app_notifications = APIRouter(  # Assurez-vous que c'est 'app_notifications' ici
    prefix="/notifications",
    tags=["notifications"],
)

@app_notifications.get("/get_all")
async def get_notifications():
    """Récupérer toutes les notifications non lues pour l'agent."""
    notifications_ref = db.collection("notifications").where("isRead", "==", False).stream()
    
    notifications = [dict(doc.to_dict(), id=doc.id) for doc in notifications_ref]

    if not notifications:
        raise HTTPException(status_code=404, detail="Aucune notification trouvée")

    return notifications

@app_notifications.put("/mark_as_read/{notif_id}")
async def mark_notification_as_read(notif_id: str):
    """Mettre à jour une notification comme lue"""
    notif_ref = db.collection("notifications").document(notif_id)
    notif = notif_ref.get()

    if not notif.exists:
        raise HTTPException(status_code=404, detail="Notification non trouvée")

    notif_ref.update({"isRead": True})
    return {"status": "success", "message": "Notification marquée comme lue"}
