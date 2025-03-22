from fastapi import FastAPI
from psycopg2.extras import RealDictCursor
import psycopg2
import time
from . import models
from .database import engine
from .routers import post, user, auth
from .config import settings

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello"}


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

