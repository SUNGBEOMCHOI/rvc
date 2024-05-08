from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

class CoverProject(BaseModel):
    id: str
    name: str
    created_at: datetime | None = None
    is_generation_done: bool
    generated_cover: Optional['GeneratedCover'] | None = None

class GeneratedCover(BaseModel):
    filename: str | None = None
    storage_path: str | None = None

class CoverProjectCreate(BaseModel):
    name: str
    user_id: int

class CoverProjectBase(BaseModel):
    id: str

# Import and update_forward_refs at the end of the file
CoverProject.model_rebuild()
GeneratedCover.model_rebuild()
CoverProjectCreate.model_rebuild()
CoverProjectBase.model_rebuild()