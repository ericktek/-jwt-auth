from pydantic import BaseModel
from typing import Optional

class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True

class BlogBase(BaseModel):
    title: str
    description: Optional[str] = None

class BlogCreate(BlogBase):
    pass

class Blog(BlogBase):
    id: int
    author_id: int

    class Config:
        from_attributes = True  

class UserBase(BaseModel):
    username: str 
    email: str
    

class UserCreate(UserBase):
    password: str  # Required during creation

class UserUpdate(BaseModel):
    email: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None

class User(UserBase):
    id: int
    is_active: bool 
    items: list[Item] = []
    blogs: list[Blog] = []

    class Config:
        from_attributes = True 

class Login(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None

