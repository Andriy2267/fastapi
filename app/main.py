from fastapi import FastAPI, Response, status, HTTPException, Depends
from random import randrange
from typing import List
from psycopg2.extras import RealDictCursor
import psycopg2
import time
from . import models, utils
from .database import engine, get_db
from . import schemas
from sqlalchemy.orm import Session
from .routers import post, user, auth


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


while True:
    try:
        conn = psycopg2.connect(host="localhost", database="fastapi", user="postgres",
                                password="Chopek696", cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Connection to the database was succesfull!")
        break
    except Exception as error:
        print(f"Connection to database was failed: {error}")
        time.sleep(2)


@app.get("/")
async def root():
    return {"message": "Hello"}


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

