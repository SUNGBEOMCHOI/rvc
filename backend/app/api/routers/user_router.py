from fastapi import APIRouter, Depends
from fastapi import HTTPException

from app.db.session import get_db
from app.models.user_model import User

from app.crud.user_crud import get_current_user

from app.errors import HttpErrorCode
from app.core.settings import get_settings

router = APIRouter(
    prefix="/user",
)

@router.get("/current_user")
def current_user(token: str, db=Depends(get_db), settings=Depends(get_settings)):
    user = get_current_user(db, token, settings)

    if not user:
        raise HttpErrorCode.USER_NOT_FOUND()
    
    return user