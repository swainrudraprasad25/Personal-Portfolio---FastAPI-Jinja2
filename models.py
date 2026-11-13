from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Integer,String

base=declarative_base()
class Portfolio(base):
    __tablename__="port"
    id=Column(Integer,autoincrement=True,primary_key=True)
    name=Column(String(150),nullable=False)
    email=Column(String(150),nullable=False)
    message=Column(String(200))
