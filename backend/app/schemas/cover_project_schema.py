from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

class CoverProject(BaseModel):
    name: str
    created_at: datetime | None = None
    is_generation_done: bool
    generated_cover: Optional['GeneratedCover'] | None = None

class GeneratedCover(BaseModel):
    filename: str
    storage_path: str

# Import and update_forward_refs at the end of the file
CoverProject.model_rebuild()
GeneratedCover.model_rebuild()
