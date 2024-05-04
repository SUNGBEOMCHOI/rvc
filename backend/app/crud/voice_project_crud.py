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
from app.crud.user_crud import get_user_by_user_id

def get_voice_projects_by_user_id(db: Session, user_id: int):
    projects = db.query(models.VoiceModelProject).filter(models.VoiceModelProject.user_id == user_id).all()
    return projects

def create_voice_project(db: Session, project: schemas.VoiceModelProjectCreate, user_id: int):
    db_project = models.VoiceModelProject(
        name=project.name,
        user_id=user_id,
        is_training_done=False
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project