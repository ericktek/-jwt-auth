from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas
from app.dependency import get_db

router = APIRouter()

@router.post("/", response_model=schemas.User, tags=["Users"])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    db_username = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    if db_username:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)

@router.put("/{user_id}/", response_model=schemas.User, tags=["Users"])
def update_active_user(user_id: int, user_update: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = crud.update_active_user(db, user_id, user_update)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found or inactive")
    return db_user

@router.delete("/{user_id}/", response_model=schemas.User, tags=["Users"])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.delete_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.get("/", response_model=list[schemas.User], tags=["Users"])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@router.get("/active/", response_model=list[schemas.User], tags=["Users"])
def read_active_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_active_users(db, skip=skip, limit=limit)
    return users

@router.get("/{user_id}/", response_model=schemas.User, tags=["Users"])
def read_active_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_active_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found or inactive")
    return db_user
