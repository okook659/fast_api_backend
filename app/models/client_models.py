#lecture :
from pydantic import BaseModel, Field
from typing import Optional

class Client(BaseModel):
    idClient: Optional[str]  # L'ID est souvent attribué automatiquement par Firebase
    designationClient: str = Field(..., max_length=50)
    emailClient: str = Field(..., regex=r"[^@]+@[^@]+\.[^@]+")
    adresseClient: str = Field(...,max_length=100)  
    telephoneClient: str = Field(...,max_length=8)

#creation :
class CreateClientSchema(BaseModel):
    designationClient: str = Field(..., max_length=50)
    emailClient: str = Field(..., regex=r"[^@]+@[^@]+\.[^@]+")
    adresseClient: str = Field(...,max_length=100) 
    telephoneClient: str = Field(...,max_length=8)

#mise à jour :
class UpdateClientSchema(BaseModel):
    designationClient: str = Field(None, max_length=50)
    emailClient: str = Field(None, regex=r"[^@]+@[^@]+\.[^@]+")
    adresseClient: str = Field(None,max_length=100) 
    telephoneClient: str = Field(None,max_length=8)