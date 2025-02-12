from pydantic import BaseModel, Field
from typing import Optional

#lecture :
class Categorie(BaseModel):
    id: str
    codeCategorie: str
    designationCategorie: str
#creation :
class CategorieCreateModel(BaseModel):
    codeCategorie: str = Field(example="VinSp")
    designationCategorie: str = Field(example="Vins & Spiritueux")

#mise à jour :
class CategorieUpdateModel(BaseModel):
    codeCategorie: Optional[str] = Field(example="VinSp")
    designationCategorie: Optional[str] = Field(example="Viens & Spiritueux")