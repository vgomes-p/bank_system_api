from fastapi import APIRouter, Depends, HTTPException
from dependencies import get_session, check_token
from sqlalchemy.orm import Session
from datetime import datetime
from schemas import OperationSchema, EditSchema
from models import Statement, User, WithdrawalCount
from main import ADMINISTRATION, ACCOUNT_TYPES


clients_router = APIRouter(prefix="/clients", tags=["clients"], dependencies=[Depends(check_token)])


def exec_op(op: str, value: float, balance) -> tuple[bool, float]:
    if op == "deposit":
        new_balance = balance + value
        return True, new_balance
    if op == "withdrawal":
        new_balance = balance - value
        return True, new_balance
    return False, 0.0


def exec_pix(value: float, personal_balance: float, alian_balance: float) -> tuple[bool, float, float]:
    new_personal_balance = personal_balance - value
    new_alian_balance = 0.0
    if alian_balance:
        new_alian_balance = alian_balance + value
    else:
        new_alian_balance = value
    return True, new_personal_balance, new_alian_balance


@clients_router.get("/")
async def home() -> dict:
    """
    This is the standard route for clients.
    All routes for clients needs authentication!
    """
    return {"message": "You access clients -> get data"}


@clients_router.post("/make_deposit")
async def make_deposit(op_value: float, session: Session = Depends(get_session), user: User = Depends(check_token)) -> dict:
    if op_value <= 0:
        raise HTTPException(status_code=422, detail="Operation value cannot be lower or equal to 0")
    stats, new_value = exec_op(op="deposit", value=op_value, balance=user.balance)
    if stats:
        time = datetime.now()
        operation_time = time.strftime("%d-%m-%Y %H:%M:%S")
        new_operation = Statement(
            operation="made a deposit",
            op_value=op_value,
            op_time=str(operation_time),
            op_maker=user.id,
            op_receiver=user.id
            )
        session.add(new_operation)
        user.balance = new_value
        session.commit()
        return {"message": "Operation completed!"}
    raise HTTPException(status_code=500, detail="Operation failed!")


@clients_router.post("/make_withdrawal")
async def make_withdrawal(op_value: float, session: Session = Depends(get_session), user: User = Depends(check_token)) -> dict:
    if op_value <= 0:
        raise HTTPException(status_code=422, detail="Operation value cannot be lower or equal to 0")
    if op_value < user.balance:
        raise HTTPException(status_code=402, detail="Operation value cannot be greater then your balance!")
    stats, new_value = exec_op(op="withdrawal", value=op_value, balance=user.balance)
    if stats:
        time = datetime.now()
        operation_time = time.strftime("%d-%m-%Y %H:%M:%S")
        operation_date = time.strftime("%d-%m-%Y")
        withdrawal_cnt = session.query(WithdrawalCount).filter(WithdrawalCount.user == user.id).first()
        if withdrawal_cnt:
            if withdrawal_cnt.counter >= 3 and withdrawal_cnt.last_time == operation_date:
                raise HTTPException(status_code=429, detail="You reached you withdrawal limits for today!")
            elif withdrawal_cnt.last_time != operation_date:
                withdrawal_cnt.counter = 1
            else:
                withdrawal_cnt.counter = withdrawal_cnt.counter + 1
        else:
            new_cnt = WithdrawalCount(
                user=user.id,
                last_time=str(operation_date),
                counter=1
            )
            session.add(new_cnt)
        new_operation = Statement(
            operation="made a withdrawal",
            op_value=op_value,
            op_time=str(operation_time),
            op_maker=user.id,
            op_receiver=user.id
            )
        session.add(new_operation)
        user.balance = new_value
        session.commit()
        return {"message": "Operation completed!"}
    raise HTTPException(status_code=500, detail="Operation failed!")


@clients_router.post("/make_pix")
async def make_pix(op_schema: OperationSchema, session: Session = Depends(get_session), user: User = Depends(check_token)) -> dict:
    personal_keys = [user.cpf, user.pix_key]
    if op_schema.receiver in personal_keys:
        raise HTTPException(status_code=409, detail="You cannot send pix to yourself")
    if op_schema.op_value <= 0:
        raise HTTPException(status_code=422, detail="Operation value cannot be lower or equal to 0")
    if op_schema.op_value > user.balance:
        raise HTTPException(status_code=402, detail="Operation value cannot be greater then your balance!")
    if len(op_schema.receiver) == 11:
        alian = session.query(User).filter(User.cpf == op_schema.receiver).first()
        if alian:
            stats, nw_personal_balance, nw_alian_balance = exec_pix(op_schema.op_value, user.balance, alian.balance)
            if stats:
                time = datetime.now()
                operation_time = time.strftime("%d-%m-%Y %H:%M:%S")
                new_operation = Statement(
                    operation="sent pix",
                    op_value=op_schema.op_value,
                    op_time=str(operation_time),
                    op_maker=user.id,
                    op_receiver=op_schema.receiver
                    )
                pix_received = Statement(
                    operation="received a pix",
                    op_value=op_schema.op_value,
                    op_time=str(operation_time),
                    op_maker=user.id,
                    op_receiver=op_schema.receiver
                )
                session.add(new_operation)
                session.add(pix_received)
                user.balance, alian.balance = nw_personal_balance, nw_alian_balance
                session.commit()
                return {"message": "Operation completed!"}
        raise HTTPException(status_code=404, detail="Receiver not found!")
    elif len(op_schema.receiver) != 11:
        alian = session.query(User).filter(User.pix_key == op_schema.receiver).first()
        if alian:
            stats, nw_personal_balance, nw_alian_balance = exec_pix(op_schema.op_value, user.balance, alian.balance)
            if stats:
                time = datetime.now()
                operation_time = time.strftime("%d-%m-%Y %H:%M:%S")
                new_operation = Statement(
                    operation="sent pix",
                    op_value=op_schema.op_value,
                    op_time=str(operation_time),
                    op_maker=user.id,
                    op_receiver=op_schema.receiver
                    )
                pix_received = Statement(
                    operation="received a pix",
                    op_value=op_schema.op_value,
                    op_time=str(operation_time),
                    op_maker=user.id,
                    op_receiver=op_schema.receiver
                )
                session.add(new_operation)
                session.add(pix_received)
                user.balance, alian.balance = nw_personal_balance, nw_alian_balance
                session.commit()
                return {"message": "Operation completed!"}
        raise HTTPException(status_code=404, detail="Receiver not found!")
    else:
        HTTPException(status_code=500, detail="Operation failed!")


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
