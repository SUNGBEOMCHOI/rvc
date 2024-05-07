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

def get_cover_projects_by_user_id(user_id: int, db: Session):
    projects = db.query(models.CoverProject).filter(models.CoverProject.user_id == user_id).all()
    return projects

def get_cover_projects_by_project_id(project_id: str, db: Session):
    project = db.query(models.CoverProject).filter(models.CoverProject.id == project_id).first()
    return project

def create_cover_project(project: schemas.CoverProjectCreate, user_id: int, db: Session, settings):
    project_id=str(uuid.uuid4())
    cover_project = models.CoverProject(
        id=project_id,
        name=project.name,
        user_id=user_id,
        storage_path=f"{settings.STORAGE_PATH}/{user_id}/{settings.COVER_PROJECT_PATH}/{project_id}"
    )
    
    db.add(cover_project)
    db.commit()
    db.refresh(cover_project)
    return cover_project

def delete_cover_project(project_id: str, db: Session):
    project = get_cover_projects_by_project_id(project_id, db)
    if not project:
        raise HttpErrorCode.PROJECT_NOT_FOUND()

    # delete generated cover
    if project.generated_cover:
        delete_generated_cover(project.generated_cover, db)

    # delete project
    if os.path.exists(project.storage_path):
        os.rmdir(project.storage_path)
    db.delete(project)
    db.commit()

def delete_generated_cover(generated_cover, db: Session):
    if not generated_cover:
        raise HttpErrorCode.PROJECT_NOT_FOUND()

    if generated_cover.filename:
        os.remove(os.path.join(generated_cover.storage_path, generated_cover.filename))
        db.delete(generated_cover)
        db.commit()