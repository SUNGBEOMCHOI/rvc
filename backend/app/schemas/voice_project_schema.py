from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class VoiceModelProject(BaseModel):
    name: str
    created_at: datetime
    is_training_done: bool

    # Use forward references to define relationships
    uploaded_voices: List['UploadedVoice'] = []
    voice_model: Optional['VoiceModel'] = None

class UploadedVoice(BaseModel):
    filename: str
    storage_path: str

class VoiceModel(BaseModel):
    filename: str
    storage_path: str

# Import and update_forward_refs at the end of the file
VoiceModelProject.model_rebuild()
UploadedVoice.model_rebuild()
VoiceModel.model_rebuild()