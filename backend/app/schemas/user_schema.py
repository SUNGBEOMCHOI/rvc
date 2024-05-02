from pydantic import BaseModel
from typing import List, Optional

class User(BaseModel):
    username: str
    email: str
    is_active: bool
    is_superuser: bool

    # Use a forward reference in a string
    cover_projects: Optional[List['CoverProject']] = []
    voice_model_projects: Optional[List['VoiceModelProject']] = []

# Import and update_forward_refs at the end of the file
from .cover_project_schema import CoverProject
from .voice_project_schema import VoiceModelProject
User.model_rebuild()