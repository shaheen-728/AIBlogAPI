from datetime import datetime, timedelta
import os

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

SECRET_KEY = os.getenv("SECRET_KEY")

if not SECRET_KEY:
    raise ValueError("SECRET_KEY not set")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


def create_access_token(data: dict):
    to_encode = data.copy()

    if "sub" in to_encode:
        to_encode["sub"] = str(to_encode["sub"])

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)

    user_id = payload.get("sub")

    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    return int(user_id)