#lecture :
from pydantic import BaseModel, Field
from typing import Optional
from app.models.user_models import *

class Client(User):
    designationClient: str = Field(..., max_length=50)
    adresseClient: str = Field(...,max_length=100)  
    telephoneClient: str = Field(...,max_length=8)

#creation :
class ClientCreateModel(UserCreateModel):
    designationClient: str = Field(..., max_length=50)
    adresseClient: str = Field(...,max_length=100) 
    telephoneClient: str = Field(...,max_length=8)

#mise à jour :
class ClientUpdateModel(UserUpdateModel):
    designationClient: str = Field(None, max_length=50)
    adresseClient: str = Field(None,max_length=100) 
    telephoneClient: str = Field(None,max_length=8)