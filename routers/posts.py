from fastapi import APIRouter, Query
from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from schemas import PostResponse,PostCreate, PostUpdate
from database import get_db
import models
from utils.auth import get_current_user


Router=APIRouter()

@Router.post("/",response_model=PostResponse,status_code=201)
def create_post(post_create:PostCreate,db=Depends(get_db),user_id: int = Depends(get_current_user)):
    user=db.execute(select(models.User).where(models.User.id==user_id)).scalars().first()
    if user is None:
        raise HTTPException(status_code=404,detail="User not found")
    new_post=models.Post(title=post_create.title,content=post_create.content,user_id=user_id,author=user)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@Router.get("/",response_model=list[PostResponse])
def get_all_posts(limit:int=Query(10,ge=1,le=10),offset:int=Query(0,ge=0),db=Depends(get_db)):
    posts=db.execute(select(models.Post).options(selectinload(models.Post.author)).limit(limit).offset(offset)).scalars().all()
    return posts

@Router.get("/{post_id}",response_model=PostResponse)
def get_post(post_id:int,db=Depends(get_db)):
    post=db.execute(select(models.Post).options(selectinload(models.Post.author)).where(models.Post.id==post_id)).scalars().first()
    if post is None:
        raise HTTPException(status_code=404,detail="Post not found")
    return post 

@Router.patch("/{post_id}",response_model=PostResponse,status_code=200)
def patch_post(post_id:int,post_update:PostUpdate,db=Depends(get_db),user_id: int = Depends(get_current_user)):
    post=db.execute(select(models.Post).options(selectinload(models.Post.author)).where(models.Post.id==post_id)).scalars().first()
    if post.user_id != user_id:
        raise HTTPException(status_code=403,detail="Forbidden")
    if post is None:
        raise HTTPException(status_code=404,detail="Post not found")
    if post_update.title is not None:
       post.title=post_update.title
    if post_update.content is not None:
        post.content=post_update.content
    db.commit()
    db.refresh(post)
    return post

@Router.delete("/{post_id}",status_code=204)
def delete_post(post_id:int,db=Depends(get_db),user_id: int = Depends(get_current_user)):
    post=db.execute(select(models.Post).where(models.Post.id==post_id)).scalars().first()
    if post is None:
        raise HTTPException(status_code=404,detail="Post not found")
    if post.user_id != user_id:
        raise HTTPException(status_code=403,detail="Forbidden")
    db.delete(post)
    db.commit()
