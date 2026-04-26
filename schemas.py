
from pydantic import BaseModel, EmailStr, Field,ConfigDict
class UserBase(BaseModel):
    name:str=Field(min_length=3,max_length=255)
    email:EmailStr =Field(min_length=5,max_length=255)


class UserCreate(UserBase):
    password:str = Field(min_length=6,max_length=255)

class UserResponse(UserBase):
    model_config =ConfigDict(from_attributes=True)
    id:int

class PostBase(BaseModel):
    title:str = Field(min_length=1,max_length=255)
    content:str = Field(min_length=1)

class PostCreate(PostBase):
      pass

class PostResponse(PostBase):
    model_config = ConfigDict(from_attributes=True)
    id:int
    user_id:int
    author:UserResponse

class PostUpdate(PostBase):
    title:str|None = None
    content:str|None = None

class UserLogin(BaseModel):
    email:EmailStr =Field(min_length=5,max_length=255)
    password:str = Field(min_length=6,max_length=255)

class LoginResponse(BaseModel):
    message: str

class Token(BaseModel):
    access_token: str
    token_type: str