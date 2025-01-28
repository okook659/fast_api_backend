#lecture :
from pydantic import BaseModel, Field
from typing import Optional

class TypeBoisson(BaseModel):
    codeTypeBoisson:Optional[str]
    designationTypeBoisson: str = Field(..., max_length=50)

#creation :
class CreateTypeBoissonSchema(BaseModel):
    designationTypeBoisson: str = Field(..., max_length=50)

#mise à jour :
class UpdateTypeBoissonSchema(BaseModel):
    designationTypeBoisson: str = Field(None, max_length=50)