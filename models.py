
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String


Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    email = Column(String(100), unique=True)
    password = Column(String(255))
    phoneNumber = Column(String(13))
    
    def __init__(self, name, email, password, phoneNumber):
        self.name = name
        self.email = email
        self.password = password
        self.phoneNumber = phoneNumber

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phoneNumber": self.phoneNumber
        }
    
    

