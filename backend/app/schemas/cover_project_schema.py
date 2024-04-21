from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

class CoverProjectSchema(BaseModel):
    name: str
    created_at: Optional[datetime] = None
    is_generation_done: bool

    # Use forward references in strings
    generated_covers: Optional['GeneratedCoverSchema'] = None

class GeneratedCoverSchema(BaseModel):
    filename: str
    storage_path: str

# Import and update_forward_refs at the end of the file
CoverProjectSchema.update_forward_refs()
GeneratedCoverSchema.update_forward_refs()
