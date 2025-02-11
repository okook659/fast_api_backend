from pydantic import BaseModel, Field
from typing import Optional

#lecture :
class Livraison(BaseModel):
    idLivraison: str
    idProduit: str
    idAgent: str
    idClient: str
    dateLivraison: str
    qteLivraison: float

#creation :
class LivraisonCreateModel(BaseModel):
    idLivraison: str
    idProduit: str
    idAgent: str
    idClient: str
    dateLivraison: str
    qteLivraison: float

#mise à jour :
class LivraisonUpdateModel(BaseModel):
    idLivraison: Optional[str]
    idProduit: Optional[str]
    idAgent: Optional[str]
    idClient: Optional[str]
    dateLivraison: Optional[str]
    qteLivraison: Optional[float]