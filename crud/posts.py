from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
from models import User, Post
from connection import engine
from crud.users import authenticate_user

Session = sessionmaker(bind=engine)


def create_post(user_id, title, description, password):
    if not user_id:
        raise ValueError("Please provide User ID")
    elif not title:
        raise ValueError("Please provide article title")
    elif not description:
        raise ValueError("Please provide a description for the article")
    elif not password:
        raise ValueError("Please provide the User's password")
    
    session = Session()
    
    try:
        user = authenticate_user(user_id=user_id, password=password)
        if not user:
            raise ValueError("Invalid User ID or password")
        
        new_post = Post(user_id=user_id, title=title, description=description)
        session.add(new_post)
        session.commit()
        session.refresh(new_post)
        return new_post
    except Exception as e:
        session.rollback()
        raise
    finally:
        session.close()

def read_posts(): 
     session = Session()
     try:
         posts = session.query(Post).all()
         return posts
     except Exception as e:
         raise e
     finally:
         session.close()

         
def read_post(post_id):
    if not post_id:
        raise ValueError({"message": "Please provide an Article ID"})
    
    session = Session()
    try:
        post = session.query(Post).filter(Post.post_id == post_id).first()
        if not post:
            raise ValueError({"message": "Article not found"})
        return post
    except Exception as e:
        session.rollback()
        raise
    finally:
         session.close()



def update_post(user_id, post_id, password, title=None, description=None):
    
    if not user_id:
        raise ValueError("Please provide User ID")
    elif not post_id:
        raise ValueError("Please provide an article ID")
    elif not password:
        raise ValueError("Please provide the User's password")
    
    session = Session()
    try:
        user = authenticate_user(user_id=user_id, password=password)
        if not user:
            raise ValueError("Invalid User ID or password")
        
        post = session.query(Post).filter(Post.post_id == post_id).first()
        
        if not post:
            raise ValueError({"message": "Article not found"})
        
        if title:
            post.title = title

        if description:
            post.description = description
            
        session.commit()
        session.refresh(post)
        return post
    except Exception as e:
         session.rollback()
         raise
    finally:
         session.close()


         
def delete_post(user_id, password, post_id):
    if not user_id:
        raise ValueError("Please provide User's ID")
    elif not post_id:
        raise ValueError("Please provide an article's ID")
    elif not password:
        raise ValueError("Please provide the User's password")
    
    session = Session()

    try:
        user = authenticate_user(user_id=user_id, password=password)
        if not user:
            raise ValueError("Invalid User ID or password")
        
        post = session.query(Post).filter(Post.post_id == post_id).first()
        if not post:
            raise ValueError({"message": "Article not found"})
        session.delete(post)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        raise
    finally:
         session.close()