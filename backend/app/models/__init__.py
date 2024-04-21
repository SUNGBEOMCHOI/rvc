import os
import sys
# backend 경로를 sys.path에 추가
project_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_path)

from app.db.base import Base
from .user_model import User
from .cover_project_model import CoverProject, GeneratedCover
from .voice_project_model import VoiceModelProject, VoiceModel, UploadedVoice
from .music_separation_project_model import MusicSeparationProject, UploadedMusic, SeparatedInstrument, SeparatedVoice