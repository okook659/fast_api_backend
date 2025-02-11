#lecture :
from pydantic import BaseModel, Field
from typing import Optional

class User(BaseModel):
    id: str  # L'ID est souvent attribué automatiquement par Firebase
    email: str
    password: str

#creation :
class UserCreateModel(BaseModel):
    email: str = Field(example="user@example.com", pattern=r"[^@]+@[^@]+\.[^@]+")
    password: str = Field(example="motdepasse",max_length=100)

#mise à jour :
class UserUpdateModel(BaseModel):
    email: Optional[str] = Field(example="user@example.com", pattern=r"[^@]+@[^@]+\.[^@]+")
    password: Optional[str] = Field(default=None,example="motdepasse",max_length=100)
    
class UserLoginModel(BaseModel):
    email: str = Field(example="user@example.com", pattern=r"[^@]+@[^@]+\.[^@]+")
    password: str = Field(example="motdepasse",max_length=100)
