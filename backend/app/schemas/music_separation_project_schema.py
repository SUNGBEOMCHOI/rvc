from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class MusicSeparationProject(BaseModel):
    name: str
    created_at: datetime
    is_separation_done: bool

    # Use forward references to define relationships
    uploaded_music: Optional['UploadedMusic']
    separated_instrument: Optional['SeparatedInstrument'] = None
    separated_voice: Optional['SeparatedVoice'] = None

class UploadedMusic(BaseModel):
    filename: str
    storage_path: str
    youtube_link: str = None

class SeparatedInstrument(BaseModel):
    filename: str
    storage_path: str

class SeparatedVoice(BaseModel):
    filename: str
    storage_path: str

# Import and update_forward_refs at the end of the file
MusicSeparationProject.model_rebuild()
UploadedMusic.model_rebuild()
SeparatedInstrument.model_rebuild()
SeparatedVoice.model_rebuild()