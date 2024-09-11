from fastapi import FastAPI
from . import models
from .database import engine
from .routers import users, items, blogs

app = FastAPI(
    title="FastAPI CRUD with JWT Authentication",
    description="A FastAPI application with CRUD operations, JWT authentication, and PostgreSQL.",
    version="1.0.0",
)

models.Base.metadata.create_all(engine)

@app.get("/", tags=["Health"])
def read_root():
    return {"message": "Welcome to the FastAPI CRUD API with JWT Authentication!"}

app.include_router(users.router, prefix="/v1/users", tags=["Users"])
app.include_router(items.router, prefix="/v1/items", tags=["Items"])
app.include_router(blogs.router, prefix="/v1/blogs", tags=["Blogs"])

