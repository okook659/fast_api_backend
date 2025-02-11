from pydantic import BaseModel, Field
from typing import Optional
from app.models.user_models import *

#lecture :
class Admin(User):
    nomAdmin: str = Field(..., max_length=50)
    prenomAdmin: str = Field(..., max_length=50)
    telephoneAdmin: str = Field(...,max_length=8)

#creation :
class AdminCreateModel(UserCreateModel):
    nomAdmin: str = Field(..., max_length=50)
    prenomAdmin: str = Field(..., max_length=50)
    telephoneAdmin: str = Field(...,max_length=8)

#mise à jour :
class AdminUpdateModel(UserUpdateModel):
    nomAdmin: str = Field(..., max_length=50)
    prenomAdmin: str = Field(..., max_length=50)
    telephoneAdmin: str = Field(None,max_length=8)

