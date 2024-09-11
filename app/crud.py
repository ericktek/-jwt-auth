from fastapi import HTTPException
from sqlalchemy.orm import Session
from . import models, schemas
from .utils.hash_password import get_password_hash

def get_active_user(db: Session, user_id: int):
    active_user =  db.query(models.User).filter(models.User.id == user_id, models.User.is_active == True).first()
    if not active_user:
        raise HTTPException(status_code=404, detail="User not found or inactive")
    return active_user

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    # Retrieves all users, including inactive ones
    users = db.query(models.User).offset(skip).limit(limit).all()
    if not users:
        raise HTTPException(status_code=404, detail="User not found")
    return users

def get_active_users(db: Session, skip: int = 0, limit: int = 100):
    # Retrieves only active users
    active_users = db.query(models.User).filter(models.User.is_active == True).offset(skip).limit(limit).all()
    if not active_users:
            raise HTTPException(status_code=404, detail="User not found or inactive")
    return active_users

def create_user(db: Session, user: schemas.UserCreate):
    password = get_password_hash(user.password)
    db_user = models.User(email=user.email, username=user.username, hashed_password=password, is_active=True)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_active_user(db: Session, user_id: int, user_update: schemas.UserUpdate):
    db_user = db.query(models.User).filter(models.User.id == user_id, models.User.is_active == True).first()
    if not db_user:
        return None
    
    for key, value in user_update.model_dump(exclude_unset=True).items():
        setattr(db_user, key, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id, models.User.is_active == True).first()
    if not db_user:
        return None
    
    db_user.is_active = False  # Mark as inactive instead of deleting
    db.commit()
    db.refresh(db_user)
    return db_user

def get_items(db: Session, skip: int = 0, limit: int = 100):
    items = db.query(models.Item).join(models.User).filter(models.User.is_active==True).offset(skip).limit(limit).all()
    if not items:
        raise HTTPException(status_code=404, detail="User is not")
    return items


def get_items(db: Session, skip: int = 0, limit: int = 100):
    items = db.query(models.Item).join(models.User).filter(models.User.is_active == True).offset(skip).limit(limit).all()
    
    if not items: 
        raise HTTPException(status_code=404, detail="No items found for active users.")
    
    return items

def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
     # Check if the user is active
    user = db.query(models.User).filter(models.User.id == user_id, models.User.is_active == True).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found or inactive")

    # Create the item for the user
    db_item = models.Item(**item.model_dump(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_blogs(db: Session, skip: int = 0, limit: int = 100):
    blogs = db.query(models.Blog).join(models.User).filter(models.User.is_active == True).offset(skip).limit(limit).all()
    if not blogs:
        raise HTTPException(status_code=404, detail="No blog found for active users")
    
    return blogs


def create_user_blog(db: Session, blog: schemas.BlogCreate, user_id: int):
    # Check if the user is active
    user = db.query(models.User).filter(models.User.id == user_id, models.User.is_active == True).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found or inactive")

    # Create the blog post
    db_blog = models.Blog(**blog.model_dump(), author_id=user_id)
    db.add(db_blog)
    db.commit()
    db.refresh(db_blog)
    return db_blog
