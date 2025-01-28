#lecture :
from pydantic import BaseModel, Field
from typing import Optional

class Livraison(BaseModel):
    idLivraison:Optional[str]
    dateLivraison: str = Field(..., max_length=50)
    prixBoisson: float = Field(..., ge=25)

#creation :
class CreateBoissonSchema(BaseModel):
    designationTypeBoisson: str = Field(..., max_length=50)
    prixBoisson: float = Field(..., ge=25)

#mise à jour :
class UpdateBoissonSchema(BaseModel):
    designationTypeBoisson: str = Field(None, max_length=50)
    prixBoisson: float = Field(None, ge=25)