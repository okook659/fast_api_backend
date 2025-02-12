from pydantic import BaseModel, Field
from typing import Optional

#lecture :
class Produit(BaseModel):
    id: str
    codeCategorie: str
    designationProduit: str
    prixProduit: float
    qteStock: float
    imageProduit: Optional[str]
    modeleProduit: str
    formatProduit: str

#creation :
class ProduitCreateModel(BaseModel):
    codeCategorie: str
    designationProduit: str
    prixProduit: float
    qteStock: float
    imageProduit: Optional[str]
    modeleProduit: Optional[str]
    formatProduit: Optional[str]

#mise à jour :
class ProduitUpdateModel(BaseModel):
    designationProduit: Optional[str]
    prixProduit: Optional[float]
    imageProduit: Optional[str]
    modeleProduit: Optional[str]
    formatProduit: Optional[str]