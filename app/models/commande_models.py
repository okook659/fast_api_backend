from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


class Commande(BaseModel):
    id: str
    idProduit: str
    idClient: str
    quantite: int
    montantTotal: float
    dateCommande : date

class CommandeCreateModel(BaseModel):
    idProduit: str = Field(example="5fd60nJgv5qFytPtl8bC")
    idClient: str = Field(example="tHaj1F6U7QY8t8FJAcHeIeuKlsf1")
    dateCommande : date = Field(example=("2025-02-26"))
    quantite: int = Field(example=5)

class CommandeUpdateModel(BaseModel):
    idProduit: Optional[str] = Field(example="5fd60nJgv5qFytPtl8bC")
    idClient: Optional[str] = Field(example="tHaj1F6U7QY8t8FJAcHeIeuKlsf1")
    dateCommande : Optional[date] = Field(example=("2025-03-26"))
    quantite: Optional[int] = Field(example=3)