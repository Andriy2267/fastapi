from fastapi import APIRouter, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import database, schemas, models, utils, oauth2

router = APIRouter(
    tags = ["Authentication"]
)

@router.post("/login", response_model=schemas.Token)
async def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    login_user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not login_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"No such credentials")
    
    if not utils.verify(user_credentials.password, login_user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"No such credentials")
    
    # create token
    # return token

    access_token = oauth2.create_access_token(data = {"user_id": login_user.id})

    return {"access_to token": access_token, "token_type": "bearer"}