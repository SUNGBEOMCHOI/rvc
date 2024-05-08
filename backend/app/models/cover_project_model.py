import os
import sys
# backend 경로를 sys.path에 추가
project_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_path)

import uuid
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base
from .user_model import User
from .voice_project_model import VoiceModel

class CoverProject(Base):
    __tablename__ = "cover_projects"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    storage_path = Column(String, nullable=False)
    is_generation_done = Column(Boolean, default=False, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="cover_projects")
    voice_model_id = Column(String(36), ForeignKey("voice_models.id"), unique=True, nullable=True)
    voice_model = relationship("VoiceModel", uselist=False)
    generated_cover = relationship("GeneratedCover", back_populates="cover_project", uselist=False)
    music_separation_project = relationship("MusicSeparationProject", back_populates="cover_project", uselist=False)

class GeneratedCover(Base):
    __tablename__ = "generated_covers"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    created_at = Column(DateTime, default=datetime.now)
    filename = Column(String, nullable=False)
    storage_path = Column(String, nullable=False)
    cover_project_id = Column(String(36), ForeignKey("cover_projects.id"), unique=True, nullable=True)
    cover_project = relationship("CoverProject", back_populates="generated_cover", uselist=False)