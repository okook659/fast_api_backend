from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.routes.client_routes import app_client
from app.routes.agent_routes import app_agent
from app.routes.admin_routes import app_admin
from app.routes.user_routes import app_user
from app.routes.categorie_routes import app_categorie
from app.routes.produit_routes import app_produit
from app.routes.commande_routes import app_commande
from app.firebase import auth
app = FastAPI()
app.include_router(app_commande)
app.include_router(app_categorie)
app.include_router(app_produit)
app.include_router(app_user)
app.include_router(app_client)
app.include_router(app_agent)
app.include_router(app_admin)

origins = [
    "http://localhost:5173",  # React en développement
    "http://127.0.0.1:5173",
]

# Ajout du middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Autoriser ces origines
    allow_credentials=True,
    allow_methods=["*"],  # Autoriser toutes les méthodes (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Autoriser tous les headers
)

@app.get("/")
async def hello():
    return {"message": "Hello, World!"}

@app.post("/login")
async def login(email: str, password: str):
    try:
        user = auth.get_user_by_email(email)
        return {"message": "Login successful", "uid": user.uid}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))