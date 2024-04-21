from pydantic import BaseModel
from typing import List, Optional

class UserSchema(BaseModel):
    username: str
    email: str
    is_active: bool
    is_superuser: bool

    # Use a forward reference in a string
    cover_projects: Optional[List['CoverProjectSchema']] = []
    voice_model_projects: Optional[List['VoiceModelProjectSchema']] = []

# Import and update_forward_refs at the end of the file
from .cover_project_schema import CoverProjectSchema
from .voice_project_schema import VoiceModelProjectSchema
UserSchema.update_forward_refs()