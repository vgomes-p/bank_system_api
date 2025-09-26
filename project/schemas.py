from pydantic import BaseModel
from typing import Optional

class UserSchema(BaseModel):
    name: str
    cpf: str
    email: str
    pin: str

    class Config:
        from_attributes = True