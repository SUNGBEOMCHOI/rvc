import os
import threading
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi import File, UploadFile
from fastapi.responses import JSONResponse
from fastapi import Form, Body
from fastapi import BackgroundTasks

from app.db.session import get_db
from app.crud.cover_project_crud import get_cover_projects_by_user_id, create_cover_project, delete_cover_project, delete_all_cover_projects_by_user_id, get_cover_projects_by_project_id, generate_cover
from app.crud.music_separation_crud import download_youtube_audio, validate_youtube_link, create_uploaded_music, create_separation_project, download_youtube_audio_threaded, get_separation_projects_by_user_id, separate_voice_and_instrument
from app.crud.voice_project_crud import get_voice_projects_by_user_id
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

@router.post("/project", response_model=schemas.CoverProject)
def create_project(name: Annotated[str, Body(...)], youtube_link:Annotated[str, Body(...)], background_tasks: BackgroundTasks, token=Depends(oauth2_scheme), db=Depends(get_db), settings=Depends(get_settings)):
    user = get_current_user(db, token, settings)
    if not user:
        raise HttpErrorCode.USER_NOT_FOUND()
    
    # validate youtube link
    validate_youtube_link(youtube_link)
    
    # create cover project
    cover_project = schemas.CoverProjectCreate(
        name=name,
        user_id=user.id,
    )
    db_cover_project = create_cover_project(cover_project, db, settings)

    storage_path, filename = f"{settings.STORAGE_PATH}/{user.id}/{settings.COVER_PROJECT_PATH}/{db_cover_project.id}", f"{settings.DOWNLOADED_FILE_NAME}"
    output_path = os.path.join(storage_path, filename)
    background_tasks.add_task(download_youtube_audio_threaded, youtube_link, output_path)
    
    
    uploaded_music = schemas.UploadedMusic(
        filename=filename,
        storage_path=storage_path,
        youtube_link=youtube_link
    )
    db_uploaded_music = create_uploaded_music(uploaded_music, db)
    
    separation_project = schemas.MusicSeparationProjectCreate(
        user_id=user.id,
        cover_project_id=db_cover_project.id, 
        uploaded_music_id=db_uploaded_music.id
    )
    
    db_separation_project = create_separation_project(separation_project, db)
    db_cover_project.music_separation_project = db_separation_project
    
    return db_cover_project

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

@router.delete("/project/all")
def delete_all_project(token=Depends(oauth2_scheme), db=Depends(get_db), settings=Depends(get_settings)):
    user = get_current_user(db, token, settings)
    if not user:
        raise HttpErrorCode.USER_NOT_FOUND()
    
    delete_all_cover_projects_by_user_id(user.id, db)

    return JSONResponse(status_code=200, content={"message": "All projects deleted successfully!"})

@router.post("/project/separate_voice")
async def separate_voice(project: schemas.VoiceModelProjectBase, voice_converison_manager=Depends(get_voice_conversion_manager), token=Depends(oauth2_scheme), db=Depends(get_db), settings=Depends(get_settings)):
    user = get_current_user(db, token, settings)
    if not user:
        raise HttpErrorCode.USER_NOT_FOUND()
    
    projects = get_cover_projects_by_user_id(user.id, db)
    if project.id not in [project.id for project in projects]:
        raise HttpErrorCode.PROJECT_NOT_FOUND()
    
    cover_project = get_cover_projects_by_project_id(project.id, db)
    # 음성 분리
    separation_project_id = cover_project.music_separation_project.id
    separate_voice_and_instrument(separation_project_id, voice_converison_manager, db)

    return JSONResponse(status_code=200, content={"message": "Voice separation started!"})

@router.post("/project/cover")
async def generate_cover_router(cover_project: Annotated[schemas.CoverProjectBase, Body(embed=True)], voice_model_project: Annotated[schemas.VoiceModelProjectBase, Body(embed=True)], voice_conversion_manager=Depends(get_voice_conversion_manager), token=Depends(oauth2_scheme), db=Depends(get_db), settings=Depends(get_settings)):
    user = get_current_user(db, token, settings)
    if not user:
        raise HttpErrorCode.USER_NOT_FOUND()
    
    print(cover_project.id, voice_model_project.id)
    cover_projects = get_cover_projects_by_user_id(user.id, db)
    if cover_project.id not in [project.id for project in cover_projects]:
        raise HttpErrorCode.PROJECT_NOT_FOUND()
    
    voice_projects = get_voice_projects_by_user_id(user.id, db)
    if voice_model_project.id not in [project.id for project in voice_projects]:
        raise HttpErrorCode.PROJECT_NOT_FOUND()
    
    cover_project = schemas.CoverProjectBase(id=cover_project.id)
    voice_model_project = schemas.VoiceModelProjectBase(id=voice_model_project.id)
    
    # 커버 생성
    generate_cover(cover_project, voice_model_project, voice_conversion_manager, db)

    return JSONResponse(status_code=200, content={"message": "Cover generation started!"})