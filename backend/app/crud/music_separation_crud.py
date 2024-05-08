import os
import sys
# backend 경로를 sys.path에 추가
project_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_path)

import re
import uuid
import threading
import subprocess

import ffmpeg
from pytube import YouTube
from fastapi import APIRouter, Depends, HTTPException, Cookie
from sqlalchemy.orm import Session

import app.schemas as schemas
import app.models as models
from app.errors import HttpErrorCode

def get_separation_projects_by_user_id(user_id: int, db: Session):
    projects = db.query(models.MusicSeparationProject).filter(models.MusicSeparationProject.user_id == user_id).all()
    return projects

def get_separation_project_by_project_id(project_id: str, db: Session):
    project = db.query(models.MusicSeparationProject).filter(models.MusicSeparationProject.id == project_id).first()
    return project

def create_separation_project(project: schemas.MusicSeparationProjectCreate, db: Session):
    project_id = str(uuid.uuid4())
    separation_project = models.MusicSeparationProject(
        id=project_id,
        name=project.name,
        user_id=project.user_id,
        cover_project_id=project.cover_project_id,
        uploaded_music_id=project.uploaded_music_id,
    )
    db.add(separation_project)
    db.commit()
    db.refresh(separation_project)
    return separation_project

def create_uploaded_music(uploaded_music: schemas.UploadedMusic, db: Session):
    db_uploaded_music = models.UploadedMusic(
        filename=uploaded_music.filename,
        storage_path=uploaded_music.storage_path,
        youtube_link=uploaded_music.youtube_link
    )
    db.add(db_uploaded_music)
    db.commit()
    db.refresh(db_uploaded_music)
    return db_uploaded_music

def delete_separation_project(project_id: str, db: Session):
    project = get_separation_project_by_project_id(project_id, db)
    if not project:
        raise HttpErrorCode.PROJECT_NOT_FOUND()

    # delete uploaded music
    if project.uploaded_music:
        delete_uploaded_music(project.uploaded_music.id, db)

    # delete separated instrument
    if project.separated_instrument:
        delete_separated_instrument(project.separated_instrument.id, db)

    # delete separated voice
    if project.separated_voice:
        delete_separated_voice(project.separated_voice.id, db)

    # delete project
    db.delete(project)
    db.commit()

def delete_uploaded_music(uploaded_music_id: str, db: Session):
    uploaded_music = db.query(models.UploadedMusic).filter(models.UploadedMusic.id == uploaded_music_id).first()
    if not uploaded_music:
        raise HttpErrorCode.PROJECT_NOT_FOUND()

    file_path = os.path.join(uploaded_music.storage_path, uploaded_music.filename)
    if os.path.exists(file_path):
        os.remove(file_path)
    db.delete(uploaded_music)
    db.commit()

def delete_separated_instrument(separated_instrument_id: str, db: Session):
    separated_instrument = db.query(models.SeparatedInstrument).filter(models.SeparatedInstrument.id == separated_instrument_id).first()
    if not separated_instrument:
        raise HttpErrorCode.PROJECT_NOT_FOUND()

    file_path = os.path.join(separated_instrument.storage_path, separated_instrument.filename)
    if os.path.exists(file_path):
        os.remove(file_path)
    db.delete(separated_instrument)
    db.commit()

def delete_separated_voice(separated_voice_id: str, db: Session):
    separated_voice = db.query(models.SeparatedVoice).filter(models.SeparatedVoice.id == separated_voice_id).first()
    if not separated_voice:
        raise HttpErrorCode.PROJECT_NOT_FOUND()

    file_path = os.path.join(separated_voice.storage_path, separated_voice.filename)
    if os.path.exists(file_path):
        os.remove(file_path)
    db.delete(separated_voice)
    db.commit()

def validate_youtube_link(youtube_link: str, max_length: int = 600):
    if not is_youtube_url(youtube_link):
        raise HttpErrorCode.INVALID_YOUTUBE_LINK()
    
    video_length = get_youtube_video_length(youtube_link)
    if video_length > max_length:
        raise HttpErrorCode.AUDIO_TOO_LONG()

def is_youtube_url(url):
    # 유튜브 URL 패턴
    youtube_regex = (
        r'(https?://)?(www\.)?'
        '(youtube|youtu|youtube-nocookie)\.(com|be)/'
        '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?\s"]{11})'
    )
    
    match = re.match(youtube_regex, url)
    return bool(match)

def get_youtube_video_length(youtube_link):
    yt = YouTube(youtube_link)
    video_duration = yt.length  # Duration in seconds
    print(video_duration)
    return video_duration


def download_youtube_audio(video_url, output_path):
    file_name, file_extension = os.path.splitext(output_path)
    file_extension = file_extension[1:]
    if file_extension not in ['mp3', 'wav']:
        raise ValueError("Unsupported format. Please choose 'mp3' or 'wav'.")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    command = [
        'yt-dlp',
        '--extract-audio',
        '--audio-format', file_extension,
        '--output', output_path,
        video_url
    ]

    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")

    return output_path

def download_youtube_audio_threaded(video_url, output_path):
    threading.Thread(target=download_youtube_audio, args=(video_url, output_path)).start()

def create_separated_instrument(project_id: str, instrument_path: str, db: Session):
    db_separated_instrument = models.SeparatedInstrument(
        filename=os.path.basename(instrument_path),
        storage_path=os.path.dirname(instrument_path),
        music_separation_project_id=project_id
    )
    db.add(db_separated_instrument)
    db.commit()
    db.refresh(db_separated_instrument)
    return db_separated_instrument

def create_separated_voice(project_id: str, voice_path: str, db: Session):
    db_separated_voice = models.SeparatedVoice(
        filename=os.path.basename(voice_path),
        storage_path=os.path.dirname(voice_path),
        music_separation_project_id=project_id
    )
    db.add(db_separated_voice)
    db.commit()
    db.refresh(db_separated_voice)
    return db_separated_voice

def separate_voice_and_instrument(separation_project_id: str, voice_conversion_manager, db: Session):
    project = get_separation_project_by_project_id(separation_project_id, db)
    if not project:
        raise HttpErrorCode.PROJECT_NOT_FOUND()

    def callback(voice_path, instrument_path):
        separated_voice = create_separated_voice(separation_project_id, voice_path, db)
        separated_instrument = create_separated_instrument(separation_project_id, instrument_path, db)
        project.is_separation_done = True
        project.separated_voice = separated_voice
        project.separated_instrument = separated_instrument
        db.commit()
        db.refresh(project)
    
    uploaded_music = project.uploaded_music
    if not uploaded_music:
        raise HttpErrorCode.PROJECT_NOT_FOUND()
    
    music_path = os.path.join(uploaded_music.storage_path, uploaded_music.filename)
    voice_conversion_manager.voice_separation(music_path, os.path.dirname(music_path), os.path.dirname(music_path), callback=callback)