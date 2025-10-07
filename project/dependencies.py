from fastapi import Depends, HTTPException
from main import SECRET_KEY, ALGORITHM, oauth2_schema
from models import db, User
from sqlalchemy.orm import sessionmaker, Session
from jose import jwt, JWTError

def get_session():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally:
        session.close()

def check_token(token: str = Depends(oauth2_schema), session: Session = Depends(get_session)):
    try:
        info_dict = jwt.decode(token, SECRET_KEY, ALGORITHM)
        user_id = int(info_dict.get("sub"))
    except JWTError:

        raise HTTPException(status_code=401, detail="access denialed, check token validity")
    user = session.query(User).filter(User.id==user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="access denialed")
    return user
