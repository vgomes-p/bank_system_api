from sqlalchemy import create_engine, Column, String, Integer, Boolean, Float, ForeignKey
from sqlalchemy.orm import declarative_base

db = create_engine("sqlite:///database.db")

Base = declarative_base()

#Users Account
class User(Base):
    __tablename__ = "users"
    id = Column("id", Integer, primary_key=True, autoincrement=True, nullable=False)
    login = Column("login", String, nullable=False)
    name = Column("name", String)
    cpf = Column("cpf", String, nullable=False)
    email = Column("email", String, nullable=False)
    pin = Column("pin", String)
    pix_key = Column("pix_key", String)
    balance = Column("balance", Float)
    stats = Column("stats", Boolean, default=True)
    access = Column("access", String, default="client")

    def __init__(self, login, name, cpf, email, pin, pix_key, balance=0.00, stats=True, access="client"):
        self.login = login
        self.name = name
        self.cpf = cpf
        self.email = email
        self.pin = pin
        self.pix_key = pix_key
        self.balance = balance
        self.stats = stats
        self.access = access

#Statement
class Statement(Base):
    __tablename__ = "statements"

    id = Column("id", Integer, primary_key=True, autoincrement=True, nullable=False)
    operation = Column("operation", String)
    op_value = Column("op_value", Float)
    op_time = Column("op_time", String)
    op_maker = Column("op_maker", Integer, ForeignKey("users.id"))
    op_receiver = Column("op_receiver", String)

    def __init__(self, operation, op_value, op_time, op_maker, op_receiver):
        self.operation = operation
        self.op_value = op_value
        self.op_time = op_time
        self.op_maker = op_maker
        self.op_receiver = op_receiver

#Withdrawals times
class WithdrawalCount(Base):
    __tablename__ = "withdrawal_counter"
    id = Column("id", Integer, primary_key=True, autoincrement=True, nullable=False)
    user = Column("user", Integer, ForeignKey("users.id"))
    last_time = Column("last_time", String)
    counter = Column("counter", Integer)

    def __init__(self, user, last_time, counter):
        self.user = user
        self.last_time = last_time
        self.counter = counter
