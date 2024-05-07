import os
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi import File, UploadFile
from fastapi.responses import JSONResponse
from fastapi import Form, Body

from app.db.session import get_db
from app.crud.cover_project_crud import get_cover_projects_by_user_id, create_cover_project, delete_cover_project
from app.crud.user_crud import get_current_user
from app.errors import HttpErrorCode
from app.core.settings import get_settings
import app.schemas as schemas
from app.api.dependencies import oauth2_scheme, get_voice_conversion_manager

router = APIRouter(
    prefix="/cover-project",
)

@router.get("/project", response_model=list[schemas.CoverProject])
def get_project(token=Depends(oauth2_scheme), db=Depends(get_db), settings=Depends(get_settings)):
    user = get_current_user(db, token, settings)

    if not user:
        raise HttpErrorCode.USER_NOT_FOUND()
    
    projects = get_cover_projects_by_user_id(user.id, db)
    return projects

@router.post("/project")
def create_project(project: Annotated[schemas.CoverProjectCreate, Body(...)], token=Depends(oauth2_scheme), db=Depends(get_db), settings=Depends(get_settings)):
    user = get_current_user(db, token, settings)

    if not user:
        raise HttpErrorCode.USER_NOT_FOUND()
    
    db_project = create_cover_project(project, user.id, db, settings)
    return db_project

@router.delete("/project")
def delete_project(project: Annotated[schemas.CoverProjectBase, Body()], token=Depends(oauth2_scheme), db=Depends(get_db), settings=Depends(get_settings)):
    user = get_current_user(db, token, settings)

    if not user:
        raise HttpErrorCode.USER_NOT_FOUND()
    
    projects = get_cover_projects_by_user_id(user.id, db)
    if project.id not in [project.id for project in projects]:
        raise HttpErrorCode.PROJECT_NOT_FOUND()
    
    delete_cover_project(project.id, db)

    return JSONResponse(status_code=200, content={"message": "Project deleted successfully!"})