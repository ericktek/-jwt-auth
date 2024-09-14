from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.utils import oauth2
from .. import crud, schemas
from app.dependency import get_db

router = APIRouter()

@router.post("/", response_model=schemas.Blog, status_code=201, tags=["Blogs"]) 
def create_blog_for_user(user_id: int, blog: schemas.BlogCreate, db: Session = Depends(get_db), get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    return crud.create_user_blog(db=db, blog=blog, user_id=user_id)

@router.get("/", response_model=list[schemas.Blog], tags=["Blogs"])
def read_blogs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    blogs = crud.get_blogs(db, skip=skip, limit=limit)
    return blogs
