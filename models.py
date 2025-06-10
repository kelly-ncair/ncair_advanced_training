from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float

Base = declarative_base()

class User(Base):
    __tablename__ = "users"     

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    email = Column(String(100), unique=True)
    password = Column(String(20))
    phoneNumber = Column(String(10))    
      
