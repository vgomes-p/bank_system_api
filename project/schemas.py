from pydantic import BaseModel
from typing import Optional

class UserSchema(BaseModel):
    name: str
    cpf: str
    email: str
    pin: str
    access: str = "client"

    class Config:
        from_attributes = True

class OperationSchema(BaseModel):
    op_value: float
    receiver: str

    class Config:
        from_attributes = True

class LoginSchema(BaseModel):
    email: str
    pin: str

    class Config:
        from_attributes = True

class EditSchema(BaseModel):
    name: str
    email: str
    stats: bool
    access: str

    class Config:
        from_attributes = True
