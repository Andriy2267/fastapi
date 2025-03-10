from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
from random import randrange
from psycopg2.extras import RealDictCursor
import psycopg2
import time
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True

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


@app.get("/posts")
async def get_posts(db: Session = Depends(get_db)):
    all_posts = db.query(models.Post).all()

    return {"data": all_posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def post_info(post: Post, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return {"your post": new_post}


@app.get("/posts/{id}")
async def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"This id {id} was not found")
    return {"Your post": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="message: " + f"such id {id} was not found")
    
    post.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, updated_post: Post, db: Session = Depends(get_db)):
    post_quary = db.query(models.Post).filter(models.Post.id == id)
    post = post_quary.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="message" + f"such {id} id was not found")
    
    post_quary.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return {"data": post_quary.first()}
