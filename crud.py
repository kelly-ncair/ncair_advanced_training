from models import User
from sqlalchemy.orm import sessionmaker
from connection import engine

Session = sessionmaker(bind=engine)

def _serialize(user):
    data = {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "phoneNumber": user.phoneNumber
    }
    return data

def create_user(name, email, password, phoneNumber):
    if not all([name, email, password, phoneNumber]):
        raise ValueError("Please provide all entries")
    
    session = Session()
    try:
        exists = session.query(User).filter(User.email == email).first()
        if exists:
            return {"message": "User already exists"}
        new_user = User(
            name=name, email=email,
            password=password, phoneNumber=phoneNumber
        )
        session.add(new_user)
        session.commit()
        return _serialize(new_user)
    finally:
        session.close()

def read_users(id):
    session = Session()
    try:
        query = session.query(User)
        if id:
            query = query.filter(User.id == id)
        users = query.all()
        return [_serialize(u) for u in users]
    finally:
        session.close()

def update_user(name, new_name=None, password=None, phoneNumber=None):
    if not name:
        raise ValueError("Please provide a name to identify the user")
    session = Session()
    try:
        user = session.query(User).filter(User.name == name).first()
        if not user:
            return {"message": "User not found"}
        if new_name:
            user.name = new_name
        if password:
            user.password = password
        if phoneNumber:
            user.phoneNumber = phoneNumber
        session.commit()
        return _serialize(user)
    finally:
        session.close()

def delete_user(name):
    if not name:
        raise ValueError("Please provide a name to identify the user")
    session = Session()
    try:
        user = session.query(User).filter(User.name == name).first()
        if not user:
            return {"message": "User not found"}
        session.delete(user)
        session.commit()
        return {"message": "User deleted successfully"}
    finally:
        session.close()
