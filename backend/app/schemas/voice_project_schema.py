from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from fastapi import UploadFile

class VoiceModelProjectBase(BaseModel):
    id: str

class VoiceModelProject(VoiceModelProjectBase):
    name: str
    created_at: datetime
    is_training_done: bool

    # Use forward references to define relationships
    uploaded_voices: List['UploadedVoice'] = []
    voice_model: Optional['VoiceModel'] = None

class VoiceModelProjectCreate(BaseModel):
    name: str

class UploadedVoice(BaseModel):
    filename: str
    storage_path: str
    category: int

class VoiceModel(BaseModel):
    voice_model_filename: str | None = None
    voice_model_storage_path: str | None = None
    index_filename: str | None = None
    index_storage_path: str | None = None

class UploadedVoiceCreate(BaseModel):
    category: int

# Import and update_forward_refs at the end of the file
VoiceModelProject.model_rebuild()
UploadedVoiceCreate.model_rebuild()
VoiceModel.model_rebuild()
UploadedVoice.model_rebuild()