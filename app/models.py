from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float

Base = declarative_base()

class Company(Base):
    __tablename__ = 'companies'
    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False, unique=True)
    location = Column(String(128), nullable=False)
    staff = relationship('Staff', backref='company', cascade='all, delete')

class Staff(Base):
    __tablename__ = 'staff'
    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    role = Column(String(64))
    salary = Column(Integer)
    email = Column(String(100), unique=True)
    phoneNumber = Column(String(10))  
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)