import os
import sys
# backend 경로를 sys.path에 추가
project_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_path)

from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base
from .cover_project_model import CoverProject
from .user_model import User

class MusicSeparationProject(Base):
    __tablename__ = "music_separation_projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    cover_project_id = Column(Integer, ForeignKey("cover_projects.id"))
    is_separation_done = Column(Boolean, default=False, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="music_separation_projects")
    cover_project = relationship("CoverProject", back_populates="music_separation_project")
    uploaded_music = relationship("UploadedMusic", back_populates="music_separation_project")
    separated_instrument = relationship("SeparatedInstrument", back_populates="music_separation_project")
    separated_voice = relationship("SeparatedVoice", back_populates="music_separation_project")

class UploadedMusic(Base):
    __tablename__ = "uploaded_musics"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    storage_path = Column(String, nullable=False)
    youtube_link = Column(String, nullable=True)
    music_separation_project_id = Column(Integer, ForeignKey("music_separation_projects.id"))
    music_separation_project = relationship("MusicSeparationProject", back_populates="uploaded_music")

class SeparatedInstrument(Base):
    __tablename__ = "separated_instruments"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.now)
    filename = Column(String, nullable=False)
    storage_path = Column(String, nullable=False)
    music_separation_project_id = Column(Integer, ForeignKey("music_separation_projects.id"))
    music_separation_project = relationship("MusicSeparationProject", back_populates="separated_instrument")

class SeparatedVoice(Base):
    __tablename__ = "separated_voices"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.now)
    filename = Column(String, nullable=False)
    storage_path = Column(String, nullable=False)
    music_separation_project_id = Column(Integer, ForeignKey("music_separation_projects.id"))
    music_separation_project = relationship("MusicSeparationProject", back_populates="separated_voice")