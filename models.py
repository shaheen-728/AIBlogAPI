from __future__ import annotations

from sqlalchemy import Integer, String, Text, ForeignKey
from sqlalchemy.orm import  Mapped, mapped_column, relationship
from database import Base

class User(Base):
    __tablename__ = "users"
    id:Mapped[int] = mapped_column(Integer,primary_key=True,index=True)
    username:Mapped[str] = mapped_column(String(255),unique=True,nullable=False)
    email:Mapped[str] = mapped_column(String(255),unique=True,nullable=False)
    password:Mapped[str] = mapped_column(String(255),nullable=False)
    posts:Mapped[list[Post]] = relationship(back_populates="author")


class Post(Base):
    __tablename__ = "posts"
    id:Mapped[int] = mapped_column(Integer,primary_key=True,index=True)
    title:Mapped[str] = mapped_column(String(255),nullable=False)
    content:Mapped[str] = mapped_column(Text,nullable=False)
    user_id:Mapped[int] = mapped_column(Integer,ForeignKey("users.id"),nullable=False)
    author: Mapped[User] = relationship(back_populates="posts")