# C:\Users\ASUS\PycharmProjects
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange
from psycopg2.extras import RealDictCursor
import psycopg2
import time


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


my_post = [
    {"title": "My 1 title", "content": "My 1 content", "id": 1},
    {"title": "My 2 title", "content": "My 2 content", "id": 2}
]

# Function to find a post by ID
def find_post(id):
    for p in my_post:
        if p["id"] == id:
            return p

async def find_index_post(id):
    for k, v in enumerate(my_post):
        if v["id"] == id:
            return k

@app.get("/")
async def root():
    return {"message": "Hello"}

@app.get("/posts")
async def get_posts():
    cursor.execute("""SELECT * FROM posts """)
    posts = cursor.fetchall()
    return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def post_info(post: Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
                   (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()

    return {"your post": new_post}


@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id)))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"This id {id} was not found")
    return {"Your post": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()

    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="message: " + f"such id {id} was not found")
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
async def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", 
                   (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="message" + f"such {id} id was not found")

    return {"message": updated_post}
