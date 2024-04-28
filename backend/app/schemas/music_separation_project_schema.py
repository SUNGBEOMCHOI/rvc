from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class MusicSeparationProjectSchema(BaseModel):
    name: str
    created_at: datetime
    is_separation_done: bool

    # Use forward references to define relationships
    uploaded_music: Optional['UploadedMusicSchema']
    separated_instrument: Optional['SeparatedInstrumentSchema'] = None
    separated_voice: Optional['SeparatedVoiceSchema'] = None

class UploadedMusicSchema(BaseModel):
    filename: str
    storage_path: str
    youtube_link: str = None

class SeparatedInstrumentSchema(BaseModel):
    filename: str
    storage_path: str

class SeparatedVoiceSchema(BaseModel):
    filename: str
    storage_path: str

# Import and update_forward_refs at the end of the file
MusicSeparationProjectSchema.model_rebuild()
UploadedMusicSchema.model_rebuild()
SeparatedInstrumentSchema.model_rebuild()
SeparatedVoiceSchema.model_rebuild()