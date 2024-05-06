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

class VoiceModelProject(Base):
    __tablename__ = "voice_model_projects"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    created_at = Column(DateTime, default=datetime.now)
    name = Column(String, nullable=False)
    is_training_done = Column(Boolean, default=False, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="voice_model_projects")
    uploaded_voices = relationship("UploadedVoice", back_populates="voice_model_project")
    voice_model = relationship("VoiceModel", back_populates="voice_model_project")

class UploadedVoice(Base):
    __tablename__ = "uploaded_voices"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    filename = Column(String, nullable=False)
    storage_path = Column(String, nullable=False)
    category = Column(Integer, nullable=False)
    voice_model_project_id = Column(String(36), ForeignKey("voice_model_projects.id"))
    voice_model_project = relationship("VoiceModelProject", back_populates="uploaded_voices")

class VoiceModel(Base):
    __tablename__ = "voice_models"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    created_at = Column(DateTime, default=datetime.now)
    filename = Column(String, nullable=False)
    storage_path = Column(String, nullable=False)
    voice_model_project_id = Column(String(36), ForeignKey("voice_model_projects.id"))
    voice_model_project = relationship("VoiceModelProject", back_populates="voice_model")