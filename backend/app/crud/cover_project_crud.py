import os
import sys
# backend 경로를 sys.path에 추가
project_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_path)

import uuid

from fastapi import APIRouter, Depends, HTTPException, Cookie
from sqlalchemy.orm import Session
import yt_dlp as youtube_dl

import app.schemas as schemas
import app.models as models
from app.errors import HttpErrorCode
from app.crud.music_separation_crud import delete_separation_project
from app.crud.voice_project_crud import get_voice_projects_by_project_id

def get_cover_projects_by_user_id(user_id: int, db: Session):
    projects = db.query(models.CoverProject).filter(models.CoverProject.user_id == user_id).all()
    return projects

def get_cover_projects_by_project_id(project_id: str, db: Session):
    project = db.query(models.CoverProject).filter(models.CoverProject.id == project_id).first()
    return project

def delete_all_cover_projects_by_user_id(user_id: int, db: Session):
    projects = get_cover_projects_by_user_id(user_id, db)
    for project in projects:
        delete_cover_project(project.id, db)

def create_cover_project(project: schemas.CoverProjectCreate, db: Session, settings):
    project_id=str(uuid.uuid4())
    cover_project = models.CoverProject(
        id=project_id,
        name=project.name,
        user_id=project.user_id,
        storage_path=f"{settings.STORAGE_PATH}/{project.user_id}/{settings.COVER_PROJECT_PATH}/{project_id}"
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

    # delete music separation project
    if project.music_separation_project:
        delete_separation_project(project.music_separation_project.id, db)

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

def create_generated_cover(project_id: str, output_cover_path: str, db: Session):
    generated_cover = models.GeneratedCover(
        filename=os.path.basename(output_cover_path),
        storage_path=os.path.dirname(output_cover_path),
        cover_project_id=project_id
    )

    db.add(generated_cover)
    db.commit()
    db.refresh(generated_cover)
    return generated_cover

def generate_cover(cover_project: schemas.CoverProjectBase, voice_model_project: schemas.VoiceModelProjectBase, voice_conversion_manager, db: Session):
    cover_project = get_cover_projects_by_project_id(cover_project.id, db)
    voice_model_project = get_voice_projects_by_project_id(voice_model_project.id, db)

    voice_model = voice_model_project.voice_model
    voice_model_path = os.path.join(voice_model.voice_model_storage_path, voice_model.voice_model_filename)
    index_path = os.path.join(voice_model.index_storage_path, voice_model.index_filename)

    music_separation_project = cover_project.music_separation_project
    separated_instrument = music_separation_project.separated_instrument
    separated_voice = music_separation_project.separated_voice

    input_instrument_path = os.path.join(separated_instrument.storage_path, separated_instrument.filename)
    input_voice_path = os.path.join(separated_voice.storage_path, separated_voice.filename)

    def callback(output_voice_path, output_mix_path):
        generated_cover = create_generated_cover(cover_project.id, output_mix_path, db)
        cover_project.is_generation_done = True
        cover_project.generated_cover = generated_cover
        db.commit()
        db.refresh(cover_project)

    output_voice_path = f"{cover_project.storage_path}/generated_voice.wav"
    output_mix_path = f"{cover_project.storage_path}/generated_mix.wav"

    voice_conversion_manager.inference(voice_model_path, input_voice_path, input_instrument_path, output_voice_path, output_mix_path, index_path, callback=callback)