from sqlalchemy.orm import sessionmaker
from connection import engine

from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from models import Post, User

Session = sessionmaker(bind=engine)

def create_post(title: str, content: str, author_id: int, category: str):
    """
    Create a new post
    """
    db = Session()
    try:
        new_post = Post(
            title=title,
            content=content,
            author_id=author_id,
            category=category,
            published_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        return new_post
    except SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Error creating post: {str(e)}")

def get_post(post_id: int):
    """
    Get a single post by ID
    """
    db = Session()
    try:
        return db.query(Post).filter(Post.post_id == post_id).first()
    except SQLAlchemyError as e:
        raise Exception(f"Error retrieving post: {str(e)}")

def get_all_posts(skip: int = 0, limit: int = 100):
    """
    Get all posts with pagination
    """
    db = Session()
    try:
        return db.query(Post).offset(skip).limit(limit).all()
    except SQLAlchemyError as e:
        raise Exception(f"Error retrieving posts: {str(e)}")

def get_posts_by_author(author_id: int, skip: int = 0, limit: int = 100):
    """
    Get all posts by a specific author
    """
    db = Session()
    try:
        return db.query(Post).filter(Post.author_id == author_id).offset(skip).limit(limit).all()
    except SQLAlchemyError as e:
        raise Exception(f"Error retrieving author's posts: {str(e)}")

def get_posts_by_category(category: str, skip: int = 0, limit: int = 100):
    """
    Get all posts in a specific category
    """
    db = Session()
    try:
        return db.query(Post).filter(Post.category == category).offset(skip).limit(limit).all()
    except SQLAlchemyError as e:
        raise Exception(f"Error retrieving category posts: {str(e)}")

def update_post(post_id: int, title: str = None, content: str = None, category: str = None):
    """
    Update a post's details
    """
    db = Session()
    try:
        post = db.query(Post).filter(Post.post_id == post_id).first()
        if not post:
            return None
        
        if title is not None:
            post.title = title
        if content is not None:
            post.content = content
        if category is not None:
            post.category = category
        # Automatically update the updated_at timestamp
        post.updated_at = datetime.utcnow()
            
        db.commit()
        db.refresh(post)
        return post
    except SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Error updating post: {str(e)}")

def delete_post(post_id: int):
    """
    Delete a post
    """
    db = Session()
    try:
        post = db.query(Post).filter(Post.post_id == post_id).first()
        if not post:
            return False
        
        db.delete(post)
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        raise Exception(f"Error deleting post: {str(e)}") 