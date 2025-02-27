from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.websocket_manager import websocket_manager

router = APIRouter(prefix="/ws", tags=["websocket"])

@router.websocket("/")
async def websocket_endpoint(websocket: WebSocket):
    """Gère la connexion WebSocket des agents de livraison."""
    await websocket_manager.connect(websocket)
    
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Message reçu via WebSocket: {data}")  
    except WebSocketDisconnect:
        await websocket_manager.disconnect(websocket)
