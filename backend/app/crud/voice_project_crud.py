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

def get_voice_projects_by_project_id(db: Session, project_id: str):
    project = db.query(models.VoiceModelProject).filter(models.VoiceModelProject.id == project_id).first()
    return project

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

def update_audio_voice_project(project_id: str, category: int,  file_path: str, db: Session):
    db_project = db.query(models.VoiceModelProject).filter(models.VoiceModelProject.id == project_id).first()
    
    # 프로젝트 내에 해당 카테고리의 음성이 있는지 확인
    origin_uploaded_voice = detect_category_uploaded_voice(project_id, category, db)
    if origin_uploaded_voice:
        # 파일 삭제
        os.remove(os.path.join(origin_uploaded_voice.storage_path, origin_uploaded_voice.filename))
        # db에서 삭제
        db.delete(origin_uploaded_voice)
        db.commit()

    # 새로운 음성 추가
    uploaded_voice = create_uploaded_voice(project_id, category, file_path, db)
    db.add(uploaded_voice)
    db.commit()

    # db 프로젝트에 음성 추가
    db_project.uploaded_voices.append(uploaded_voice)    
    db.commit()
    db.refresh(db_project)
    return db_project

def detect_category_uploaded_voice(project_id: str, category: int, db: Session):
    # 프로젝트 내에 해당 카테고리의 음성이 있는지 확인
    # 있으면 해당 음성 반환 없으면 None 반환
    origin_uploaded_voice = db.query(models.UploadedVoice).filter(models.UploadedVoice.voice_model_project_id == project_id).filter(models.UploadedVoice.category == category).first()
    return origin_uploaded_voice

def create_uploaded_voice(project_id: str, category: int, file_path: str, db: Session):
    db_uploaded_voice = models.UploadedVoice(
        filename=os.path.basename(file_path),
        storage_path=os.path.dirname(file_path),
        category=category,
        voice_model_project_id=project_id
    )
    db.add(db_uploaded_voice)
    db.commit()
    db.refresh(db_uploaded_voice)
    return db_uploaded_voice

def train_voice_model(project_id: str, voice_conversion_manager, db: Session, settings):
    project = get_voice_projects_by_project_id(db, project_id)
    if not project:
        raise HttpErrorCode.PROJECT_NOT_FOUND()
    
    # get all uploaded voices
    uploaded_voices = project.uploaded_voices
    if not uploaded_voices:
        raise HttpErrorCode.NO_UPLOADED_VOICE()
    
    # check if uploaded voices are in the same directory
    uploaded_voices_dir = list(set(list(uploaded_voice.storage_path for uploaded_voice in uploaded_voices)))
    if len(uploaded_voices_dir) >= 2:
        raise HttpErrorCode.UPLOADED_VOICE_DIR_ERROR()
    
    # train voice model
    output_model_dir = f"{settings.STORAGE_PATH}/{project.user_id}/{settings.VOICE_PROJECT_PATH}/{project_id}/{settings.VOICE_MODEL_PATH}"
    
    def callback(trained_voice_model_path, trained_index_path):
        voice_model = create_voice_model(db, project_id, trained_voice_model_path, trained_index_path)
        project.is_training_done = True
        project.voice_model = voice_model
        db.commit()
        db.refresh(project)
    
    voice_conversion_manager.train(uploaded_voices_dir[0], output_model_dir, callback)

def create_voice_model(db: Session, project_id: str, voice_model_path: str, index_path:str):
    voice_model = models.VoiceModel(
        voice_model_filename = os.path.basename(voice_model_path),
        voice_model_storage_path = os.path.dirname(voice_model_path),
        index_filename = os.path.basename(index_path),
        index_storage_path = os.path.dirname(index_path),
        voice_model_project_id=project_id
    )
    db.add(voice_model)
    db.commit()
    return voice_model