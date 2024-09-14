from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from . import models
from .database import engine
from .routers import users, items, blogs, auth

app = FastAPI(
    title="FastAPI CRUD with JWT Authentication",
    description="A FastAPI application with CRUD operations, JWT authentication, and PostgreSQL.",
    version="1.0.0",
)

models.Base.metadata.create_all(engine)

html = f"""
<!DOCTYPE html>
<html>
    <head>
        <title>FastAPI Auth</title>
    </head>
    <body>
        <div class="bg-gray-200 p-4 rounded-lg shadow-lg">
            <h1>FastAPI CRUD API with JWT Authentication!</h1>
            <ul>
                <li><a href="/docs">/docs</a></li>
                <li><a href="/redoc">/redoc</a></li>
            </ul>
           <p>Built and deployed by Lemajr <a href="https://github.com/ericktek" target="_blank">GitHub</a>
                    Powered by <a href="https://fastapi.tiangolo.com" target="_blank">FastAPI</a> and <a href="https://vercel.com" target="_blank">Vercel</a></p>
        </div>
    </body>
</html>
"""
@app.get("/", tags=["Health"])
async def root():
    return HTMLResponse(html)

app.include_router(auth.router, prefix="/v1/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/v1/users", tags=["Users"])
app.include_router(items.router, prefix="/v1/items", tags=["Items"])
app.include_router(blogs.router, prefix="/v1/blogs", tags=["Blogs"])

