from fastapi import APIRouter, Depends, HTTPException
from dependencies import get_session, check_token
from sqlalchemy.orm import Session
from datetime import datetime
from schemas import OperationSchema, EditSchema
from models import Statement, User
from main import ADMINISTRATION, ACCOUNT_TYPES

clients_router = APIRouter(prefix="/clients", tags=["clients"], dependencies=[Depends(check_token)])


@clients_router.get("/")
async def home() -> dict:
    """
    This is the standard route for clients.
    All routes for clients needs authentication!
    """
    return {"message": "You access clients -> get data"}

@clients_router.post("make_operation/")
async def make_operation(op_schema: OperationSchema, session: Session = Depends(get_session), user: User = Depends(check_token)) -> dict:
    time = datetime.now()
    operation_time = time.strftime("%d-%m-%Y %H:%M:%S")
    new_operation = Statement(
        operation=op_schema.op_type,
        op_value=op_schema.op_value,
        op_time=str(operation_time),
        op_maker=user.id,
        op_receiver=op_schema.receiver
        )
    session.add(new_operation)
    session.commit()
    return {"message": "Operation completed!"}

@clients_router.post("/client/manage/edit")
async def manage_edit_account(edit: EditSchema, client_id: int, session: Session = Depends(get_session), user_check: User = Depends(check_token)) -> dict:
    client = session.query(User).filter(User.id==client_id).first()
    if not client:
        raise HTTPException(status_code=400, detail="Client not found")
    if user_check.access not in ADMINISTRATION:
        raise HTTPException(status_code=401, detail="You are not allowed to execute this operation")
    if edit.access not in ACCOUNT_TYPES:
        raise HTTPException(status_code=400, detail=f"'{edit.access}' account type is not valid!")
    if edit.access in ADMINISTRATION:
        if user_check.access != "admin":
            raise HTTPException(status_code=401, detail=f"You are not allowed to execute this operation as a {user_check.access}!")
    client.name = edit.name
    client.email = edit.email
    client.access = edit.access
    client.stats = edit.stats
    session.commit()
    return {"message": f"'{edit.name}' datas edited successfully!"}

@clients_router.post("/client/manage/close_account")
async def manage_close_account(client_id: int, session: Session = Depends(get_session), user_check: User = Depends(check_token)) -> dict:
    client = session.query(User).filter(User.id==client_id).first()
    if not client:
        raise HTTPException(status_code=400, detail="Client not found")
    if user_check.access != "admin":
        raise HTTPException(status_code=401, detail="You are not allowed to execute this operation")
    session.delete(client)
    session.commit()
    return {"message": "Account closed!"}

@clients_router.get("/statement")
async def statement(session: Session = Depends(get_session), user: User = Depends(check_token)) -> dict:
    operations = session.query(Statement).filter(Statement.op_maker==user.id).all()
    ops_data = []
    for op in operations:
        maker = session.query(User).filter(User.id == op.op_maker).first()
        receiver = session.query(User).filter(User.id == op.op_receiver).first()
        ops_data.append({
            "Operation": op.operation,
            "Value": op.op_value,
            "Time": op.op_time,
            "Maker": maker.name if maker else "n/a",
            "Receiver": receiver.name if receiver else "n/a",
        })
    return {"operations": ops_data}

