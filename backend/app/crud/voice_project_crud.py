from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.voice_project_model import VoiceModelProject

router = APIRouter(
    prefix="/api/voice_project",
)

@router.get("/list")
def get_voice_projects(db: Session = Depends(get_db)):
    return db.query(VoiceModelProject).all()