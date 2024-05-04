import os
import sys
# backend 경로를 sys.path에 추가
project_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(project_path)

import requests
from typing import Annotated
from fastapi import APIRouter, HTTPException, status, Depends, Query
from starlette.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.core.settings import get_settings
from app.crud.user_crud import get_user_by_email, create_user
from app.db.session import get_db
import app.schemas as schemas
from app.errors import HttpErrorCode
from app.core.security import exchange_code_for_token, get_user_profile

router = APIRouter()

@router.get("/google-login")
def google_login(settings=Depends(get_settings)):
    url = (
        f"{settings.GOOGLE_AUTHORIZATION_ENDPOINT}"
        "?response_type=code"
        f"&client_id={settings.GOOGLE_CLIENT_ID}"
        f"&redirect_uri={settings.GOOGLE_REDIRECT_URI}" # 127.0.0.1:8000/callback
        "&scope=openid%20email%20profile"
    )
    return RedirectResponse(url)

@router.get("/callback")
async def callback(
        code: Annotated[str, Query()], 
        db: Session = Depends(get_db), 
        settings=Depends(get_settings)
    ):
    # 구글에서 발급된 code를 access_token으로 교환
    token_response = exchange_code_for_token(code, settings)
    access_token = token_response.get("access_token")

    # access_token을 이용해 사용자 정보를 가져옴
    profile_data = get_user_profile(access_token, settings)
    google_email = profile_data['email']
    google_username = profile_data.get('name', google_email.split('@')[0])

    # 사용자 정보가 없으면 새로 생성
    existing_user = get_user_by_email(db, google_email)
    if not existing_user:
        user_data = schemas.User(
            username=google_username,
            email=google_email,
            is_active=True,
            is_superuser=False,
        )
        create_user(db, user_data)

    return {"token_type": "bearer", "access_token": access_token}