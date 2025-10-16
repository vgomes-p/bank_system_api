from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from models import User
from dependencies import get_session, check_token
from main import bcrypt_context, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXP_MIN, ADMINISTRATION, ACCOUNT_TYPES
from schemas import UserSchema, LoginSchema
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
import random
import string


def mk_login(name: str) -> str:
    splited_name = name.split(" ")
    if len(splited_name) >=3 :
        """init letter first, mid name, - init letter last name"""
        init_letter = splited_name[0][0]
        end_letter = splited_name[-1][0]
        return f"{init_letter}{splited_name[1]}-{end_letter}".lower()
    else:
        """Three first letter first - init and last letter last name"""
        init_letter = splited_name[-1][0]
        end_letter = splited_name[-1][-1]
        return f"{splited_name[0][0:3]}-{init_letter}{end_letter}".lower()


def mk_pix() -> str:
    pix_key = (
        random.sample(string.ascii_letters, k=5)
        + random.sample(string.digits, k=5)
    )
    random.shuffle(pix_key)
    return "".join(pix_key)


auth_router = APIRouter(prefix="/auth", tags=["auth"])


def mk_token(user_id: str, token_duration: int=timedelta(minutes=ACCESS_TOKEN_EXP_MIN)) -> str:
    exp_date = datetime.now(timezone.utc) + token_duration
    data_dict = {"sub": str(user_id),
                 "exp": exp_date}
    encoded_jwt = jwt.encode(data_dict, SECRET_KEY, ALGORITHM)
    return encoded_jwt


def auth_user(email, pin, session):
    user = session.query(User).filter(User.email==email).first()
    if not user:
        return False
    elif not bcrypt_context.verify(pin, user.pin):
        return False
    return user


@auth_router.get("/")
async def authenticate() -> dict:
    """
    This is the standard route for authentication
    """
    return {"message": "You access the authentication route", "auth_stats": False}

@auth_router.post("/user")
async def register_user(user_schema: UserSchema, session: Session = Depends(get_session)) -> dict:
    user = session.query(User).filter(User.email==user_schema.email).first()
    if user:
        raise HTTPException(status_code=400, detail="This email is already registered!")
    if len(user_schema.name.split(" ")) < 2:
        raise HTTPException(status_code=400, detail="Please, inform your full name!")
    if user_schema.access not in ACCOUNT_TYPES:
        raise HTTPException(status_code=400, detail=f"'{user_schema.access}' account type is not valid!")
    if user_schema.access != "client":
        raise HTTPException(status_code=401, detail="You are only allowed to create an account with access as 'client'!")
    if len(user_schema.pin) > 15:
        raise HTTPException(status_code=400, detail="Your pin cannot be longer than 15 chars")
    else:
        cryp_pin = bcrypt_context.hash(user_schema.pin)
        login = mk_login(user_schema.name)
        pix_key = mk_pix()
        formated_cpf = str(user_schema.cpf).replace(".", "").replace("-", "")
        new_user = User(login, user_schema.name, formated_cpf, user_schema.email, cryp_pin, pix_key, access=user_schema.access)
        session.add(new_user)
        session.commit()
        return {"message": f"User '{user_schema.name}' registered!",
                "pix": pix_key,
                "login": login}

@auth_router.post("/login")
async def login(login: LoginSchema, session: Session = Depends(get_session)) -> dict:
    user = auth_user(login.email, login.pin, session)
    if not user:
        raise HTTPException(status_code=400, detail="User not found or wrong credentials")
    else:
        access_token = mk_token(user.id)
        refresh_token = mk_token(user.id, token_duration=timedelta(days=7))
        return {"access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "Bearer"}

@auth_router.post("/login-form")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)) -> dict:
    user = auth_user(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(status_code=400, detail="User not found or wrong credentials")
    else:
        access_token = mk_token(user.id)
        return {"access_token": access_token,
                "token_type": "Bearer"}

@auth_router.get("/refresh")
async def use_refresh_token(user: User = Depends(check_token)) -> dict:
    access_token = mk_token(user.id)
    return {"access_token": access_token,
            "token_type": "Bearer"}
