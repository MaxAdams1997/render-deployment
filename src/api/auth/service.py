from sqlalchemy.orm import Session
from datetime import timedelta, datetime, timezone
from jose import jwt
from ..deps import bcrypt_context
from . import repository
from . import model
import os

SECRET_KEY = os.getenv("AUTH_SECRET_KEY")
ALGORITHM = os.getenv("AUTH_ALGORITHM")

def authenticate_user(db: Session, username: str, password: str):
    user = repository.get_user_by_username(db, username)
    if not user:
        return None
    if not bcrypt_context.verify(password, user.hashed_password):
        return None
    return user

def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

def create_user(db: Session, user_create: model.UserCreateRequest):
    hashed_password = bcrypt_context.hash(user_create.password)
    return repository.create_user(db, user_create.username, hashed_password)
