from pydantic import BaseModel, Field
from typing import Optional
from app.models.user_models import *

#lecture :
class Agent(User):
    nomAgent: str = Field(..., max_length=50)
    prenomAgent: str = Field(..., max_length=50)
    salaireAgent: float
    adresseAgent: str = Field(...,max_length=100)  
    telephoneAgent: str = Field(...,max_length=8)

#creation :
class AgentCreateModel(UserCreateModel):
    nomAgent: str = Field(..., max_length=50)
    prenomAgent: str = Field(..., max_length=50)
    salaireAgent: float
    adresseAgent: str = Field(...,max_length=100) 
    telephoneAgent: str = Field(...,max_length=8)

#mise à jour :
class AgentUpdateModel(UserUpdateModel):
    nomAgent: str = Field(..., max_length=50)
    prenomAgent: str = Field(..., max_length=50)
    salaireAgent: float
    adresseAgent: str = Field(...,max_length=100)
    telephoneAgent: str = Field(None,max_length=8)