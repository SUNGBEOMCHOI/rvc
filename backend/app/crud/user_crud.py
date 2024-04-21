from fastapi import APIRouter, Depends

from app.db.session import get_db
from app.models.user_model import User

router = APIRouter(
    prefix="/user",
)

@router.get("/list")
def get_users(db = Depends(get_db)):
    return db.query(User).all()