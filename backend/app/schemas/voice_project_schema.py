from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class VoiceModelProjectSchema(BaseModel):
    name: str
    created_at: datetime
    is_training_done: bool

    # Use forward references to define relationships
    uploaded_voices: List['UploadedVoiceSchema'] = []
    voice_model: Optional['VoiceModelSchema'] = None

class UploadedVoiceSchema(BaseModel):
    filename: str
    storage_path: str

class VoiceModelSchema(BaseModel):
    filename: str
    storage_path: str

# Import and update_forward_refs at the end of the file
VoiceModelProjectSchema.model_rebuild()
UploadedVoiceSchema.model_rebuild()
VoiceModelSchema.model_rebuild()