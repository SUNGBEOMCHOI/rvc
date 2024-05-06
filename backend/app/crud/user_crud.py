import os
import sys
# backend 경로를 sys.path에 추가
project_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_path)

from fastapi import APIRouter, Depends, HTTPException, Cookie
from sqlalchemy.orm import Session

from app.db.session import get_db
import app.schemas as schemas
import app.models as models
from app.errors import HttpErrorCode
from app.core.security import get_user_profile

def get_user_by_user_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_current_user(db: Session, token: str, settings):
    try:
        idinfo = get_user_profile(token=token, settings=settings)
    except HTTPException as e:
        raise HttpErrorCode.CREDENTIALS_ERROR()
    print(idinfo)
    user = get_user_by_email(db, idinfo["email"])
    print(user)
    if user is None:
        raise HttpErrorCode.USER_NOT_FOUND()
    
    return user

def create_user(db: Session, user: schemas.User):
    db_user = models.User(
        username=user.username,
        email=user.email,
        is_active=user.is_active,
        is_superuser=user.is_superuser,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user