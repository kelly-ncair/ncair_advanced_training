
from sqlalchemy.orm import sessionmaker
from models import User
from connection import engine


Session = sessionmaker(bind=engine)


# CRUD OPERATIONS
## C= Create, R=Read, U=Update and D=Delete

def create_user(name, email, password, phoneNumber):
    if not name or not email or not password or not phoneNumber:
        raise ValueError("Please provide all entries")
    
    session = Session()
    try:
        exists = session.query(User).filter(User.email == email).first()
        
        if exists:
            raise ValueError({"message": "User already exists"})

        new_user = User(name=name, email=email, password=password, phoneNumber=phoneNumber)
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        return new_user
    except Exception as e:
        session.rollback()
        raise
    finally:
        session.close()
        
        
def read_users(): 
     session = Session()
     try:
         users = session.query(User).all()
         return users
     except Exception as e:
         raise e
     finally:
         session.close()

         
def read_user(id):
    if not id:
        raise ValueError({"message": "Please provide an id"})
    
    session = Session()
    try:
        user = session.query(User).filter(User.id == id).first()
        if not user:
            raise ValueError({"message": "User not found"})
        return user
    except Exception as e:
        session.rollback()
        raise
    finally:
         session.close()
         

def update_user(id, name=None, password=None, phoneNumber=None, email=None):
    session = Session()
    if not id:
        raise ValueError({"message": "Please provide an id"})
    try:
        user = session.query(User).filter(User.id == id).first()
        
        if not user:
            raise ValueError({"message": "User not found"})
        
        if name:
            user.name = name
            
        if password:
            user.password = password
            
        if phoneNumber:
            user.phoneNumber = phoneNumber
        
        if email:
            user.email = email
            
        session.commit()
        session.refresh(user)
        return user
    except Exception as e:
         session.rollback()
         raise
    finally:
         session.close()
         
         
def delete_user(id):
    
    if not id:
        raise ValueError({"message": "Please provide an id"})
    
    session = Session()
    
    try:
        user = session.query(User).filter(User.id == id).first()
        
        if not user:
            raise ValueError({"message": "User not found"})

        session.delete(user)
        session.commit()
        return True
    
    except Exception as e:
        session.rollback()
        raise
    finally:
         session.close()
         