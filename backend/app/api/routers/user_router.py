from fastapi import APIRouter, Depends
from fastapi import HTTPException
from fastapi.security import OAuth2AuthorizationCodeBearer

from app.db.session import get_db
from app import schemas
from app.crud.user_crud import get_current_user
from app.errors import HttpErrorCode
from app.core.settings import get_settings
from app.api.dependencies import oauth2_scheme

router = APIRouter(
    prefix="/user",
)

settings = get_settings()

@router.get("/current-user", response_model=schemas.User)
def current_user(token=Depends(oauth2_scheme), db=Depends(get_db), settings=Depends(get_settings)):
    user = get_current_user(db, token, settings)

    if not user:
        raise HttpErrorCode.USER_NOT_FOUND()
    
    return user