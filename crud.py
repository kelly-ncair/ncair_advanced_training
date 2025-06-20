
from sqlalchemy.orm import sessionmaker
from models import User, Post
from connection import engine


Session = sessionmaker(bind=engine)


# CRUD OPERATIONS
## C= Create, R=Read, U=Update and D=Delete

def create_user(name, email, password, phoneNumber):
    
    session = Session()
    
    try:
        exists = session.query(User).filter(User.email == email).first()
        
        if exists:
            raise Exception(str("User exists"))
        else:
             new_user = User(name = name, email = email, password = password, phoneNumber = phoneNumber)
             session.add(new_user)
             session.commit()
             return new_user.to_dict()
    except Exception as e:
        raise Exception(str(e))
    finally:
        session.close()
        
        
def read_users(): 
     session = Session()
     try:
         users = session.query(User).all()
         return users
     except Exception as e:
         raise Exception(str(e))
     finally:
         session.close()
         
         
def get_user(id):
    session = Session()

    try:
        user = session.query(User).filter(User.id == id).first()

        if not user:
            raise Exception(str("User not found"))

        return user.to_dict()

    except Exception as e:
        raise Exception(str(e))
    finally:
        session.close()
         

def update_user(id, name=None, password=None, phoneNumber=None):
    session = Session()
    
    if not id:
        raise Exception(str("Please provide id"))
    
    try:
        user = session.query(User).filter(User.id == id).first()
        
        if not user:
            raise Exception(str("User doesnt exist"))
        
        if name:
            user.name = name
            
        if password:
            user.password = password
            
        if phoneNumber:
            user.phoneNumber = phoneNumber
            
        session.commit()
        
        return user
    
    except Exception as e:
         raise Exception(str(e))
    finally:
         session.close()
         
         
def delete_user(id):
    
    if not id:
        raise Exception(str("Please provide an id"))
    
    session = Session()
    
    try:
        user = session.query(User).filter(User.id == id).first()
        
        if not user:
            raise Exception(str("User not found"))

        session.delete(user)
        
        session.commit()
        
        return True
    
    except Exception as e:
         raise Exception(str(e))
    finally:
         session.close()


def create_post(user_id, title, description):
    session = Session()
    
    try:
        user = session.query(User).filter(User.id == user_id).first();
        
        if not user:
            raise Exception(str("User not found"))
        
        post = Post(title=title, description=description, user_id=user_id)
        
        session.add(post)
        session.commit()
        
        return post.to_dict()
    
    except Exception as e:
        session.rollback()
        raise Exception(str(e))
    
    finally:
        session.close()
    

