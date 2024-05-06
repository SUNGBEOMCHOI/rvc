import os

from fastapi import APIRouter, Depends
from fastapi import File, UploadFile
from fastapi.responses import JSONResponse
from fastapi import Body

from app.db.session import get_db
from app.crud.voice_project_crud import get_voice_projects_by_user_id, create_voice_project, update_audio_voice_project
from app.crud.user_crud import get_current_user
from app.errors import HttpErrorCode
from app.core.settings import get_settings
import app.schemas as schemas
from app.api.dependencies import oauth2_scheme

router = APIRouter(
    prefix="/voice-project",
)

@router.get("/project")
def get_project(token=Depends(oauth2_scheme), db=Depends(get_db), settings=Depends(get_settings)):
    user = get_current_user(db, token, settings)

    if not user:
        raise HttpErrorCode.USER_NOT_FOUND()
    
    projects = get_voice_projects_by_user_id(db, user.id)
    return projects

@router.post("/project")
def create_project(project: schemas.VoiceModelProjectCreate, token=Depends(oauth2_scheme), db=Depends(get_db), settings=Depends(get_settings)):
    user = get_current_user(db, token, settings)

    if not user:
        raise HttpErrorCode.USER_NOT_FOUND()
    
    db_project = create_voice_project(db, project, user.id)
    return db_project

@router.post("/project/audio")
async def update_audio(project_id: str = Body(), category:int = Body(), file: UploadFile = File(...), token=Depends(oauth2_scheme), db=Depends(get_db), settings=Depends(get_settings)):
    user = get_current_user(db, token, settings)
    
    user_storage_path = f"{settings.STORAGE_PATH}/{user.id}/voice_project/{project_id}"
    if not os.path.exists(user_storage_path):
        os.makedirs(user_storage_path)
    
    # 업로드된 파일 저장
    file_location = f"{user_storage_path}/{file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(await file.read())
    
    # 데이터베이스 업데이트
    db_project = update_audio_voice_project(project_id, category, file_location, db)

    # 성공 메시지 반환
    return JSONResponse(status_code=200, content={"message": "File uploaded successfully!", "file_path": file_location})
