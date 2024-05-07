import os
import sys
# backend 경로를 sys.path에 추가
project_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_path)

import uuid

from fastapi import APIRouter, Depends, HTTPException, Cookie
from sqlalchemy.orm import Session

from app.db.session import get_db
import app.schemas as schemas
import app.models as models
from app.errors import HttpErrorCode
from app.crud.user_crud import get_user_by_user_id

def get_voice_projects_by_user_id(user_id: int, db: Session):
    projects = db.query(models.VoiceModelProject).filter(models.VoiceModelProject.user_id == user_id).all()
    return projects

def get_voice_projects_by_project_id(project_id: str, db: Session):
    project = db.query(models.VoiceModelProject).filter(models.VoiceModelProject.id == project_id).first()
    return project

def create_voice_project(project: schemas.VoiceModelProjectCreate, user_id: int, db: Session, settings):
    db_project = models.VoiceModelProject(
        id=str(uuid.uuid4()),
        name=project.name,
        user_id=user_id,
        is_training_done=False
    )
    user_storage_path = f"{settings.STORAGE_PATH}/{user_id}/{settings.VOICE_PROJECT_PATH}/{db_project.id}"
    db_project.storage_path = user_storage_path
    
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project