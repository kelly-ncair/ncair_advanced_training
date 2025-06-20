
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    email = Column(String(100), unique=True)
    password = Column(String(255))
    phoneNumber = Column(String(13))
    
    posts = relationship("Post", back_populates="user")
    
    def __init__(self, name, email, password, phoneNumber):
        self.name = name
        self.email = email
        self.password = password
        self.phoneNumber = phoneNumber

    def to_dict(self, include_posts=True):
        result = {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phoneNumber": self.phoneNumber,
        }
        
        if include_posts:
            result["posts"] = [post.to_dict(include_user=False) for post in self.posts]
            
        return result
    
class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    description = Column(String(100))
    user_id = Column(Integer, ForeignKey("users.id"))
    
    user = relationship("User", back_populates="posts")

    def __init__(self, title, description, user_id):
        self.title = title
        self.description = description
        self.user_id = user_id

    def to_dict(self, include_user=True):
        result =  {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "user_id": self.user_id,
        }
        
        if include_user and self.user:
            result["user"] = self.user.to_dict(include_posts=False)
        
        return result  







# RELATIONSHIPS
# 1. One-One Relationship - One table will always be referenced once by another table and vice_versa
# 2. One-Many Relationship - One table can be referenced many times in another table.
# 3. Many-One Relationship - One table can reference another table many times.
# 4. Many-Many Relationship - Many rows in a table can be referenced by many rows in another table