from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
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
    posts = relationship("Post", back_populates="author")

class Post(Base):
    __tablename__ = "posts"

    post_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255))
    author_id = Column(Integer, ForeignKey('users.id'))
    content = Column(Text)
    category = Column(String(50))
    published_at = Column(DateTime)
    updated_at = Column(DateTime)
    
    author = relationship("User", back_populates="posts")
      

