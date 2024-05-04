import os
import sys
# backend 경로를 sys.path에 추가
project_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_path)

from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base
from .user_model import User
from .voice_project_model import VoiceModel

class CoverProject(Base):
    __tablename__ = "cover_projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    is_generation_done = Column(Boolean, default=False, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="cover_projects")
    voice_model_id = Column(Integer, ForeignKey("voice_models.id"))
    voice_model = relationship("VoiceModel")
    generated_cover = relationship("GeneratedCover", back_populates="cover_project")
    music_separation_project = relationship("MusicSeparationProject", back_populates="cover_project")

class GeneratedCover(Base):
    __tablename__ = "generated_covers"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.now)
    filename = Column(String, nullable=False)
    storage_path = Column(String, nullable=False)
    cover_project_id = Column(Integer, ForeignKey("cover_projects.id"))
    cover_project = relationship("CoverProject", back_populates="generated_cover")