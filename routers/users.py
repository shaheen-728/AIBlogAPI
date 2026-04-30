from fastapi import APIRouter
from fastapi import Depends, HTTPException

from schemas import  Token, UserLogin, UserResponse, UserCreate
from database import get_db
import models
from utils.auth import create_access_token
from utils.security import hash_password, verify_password
from fastapi.security import OAuth2PasswordRequestForm



Router=APIRouter()

@Router.post("/login",response_model=Token, status_code=200)
def login_user(form_data:OAuth2PasswordRequestForm=Depends(),db = Depends(get_db)
):
    user=db.query(models.User).filter(models.User.username==form_data.username).first()
    if user is None:
        raise HTTPException(status_code=404,detail="User not found")
    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401,detail="Unauthorized")
    access_token = create_access_token({"sub": str(user.id)})

    return {
    "access_token": access_token,
    "token_type": "bearer"
}

@Router.post("/",response_model=UserResponse, status_code=201)
def create_user(user_create:UserCreate,db = Depends(get_db)
):
    new_user=models.User(username=user_create.username,email=user_create.email,password=hash_password(user_create.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@Router.get("/{user_id}",response_model=UserResponse,status_code=200)
def get_user(user_id:int,db=Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==user_id).first()
    if user is None:
        raise HTTPException(status_code=404,detail="User not found")
    return user
