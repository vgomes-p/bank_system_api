from fastapi import APIRouter, Depends, HTTPException
from models import User
from dependencies import get_session
from main import bcrypt_context
from schemas import UserSchema
from sqlalchemy.orm import Session

def mk_login():
    return "test"

def mk_pix():
    return "123test890"

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get("/")
async def authenticate() -> dict:
    """
    This is the standard route for authentication
    """
    return {"message": "You access the authentication route", "auth_stats": False}

@auth_router.post("/register_user")
async def register_user(user_schema: UserSchema, session: Session = Depends(get_session)) -> dict:
    
    user = session.query(User).filter(User.email==user_schema.email).first()
    if user:
        raise HTTPException(status_code=400, detail="This email is already registered!")
    else:
        cryp_pin = bcrypt_context.hash(user_schema.pin)
        login = mk_login()
        pix_key = mk_pix()
        new_user = User(login, user_schema.name, user_schema.cpf, user_schema.email, cryp_pin, pix_key)
        session.add(new_user)
        session.commit()
        return {"message": f"User '{user_schema.name}' registered! You pix key is: {pix_key}"}
