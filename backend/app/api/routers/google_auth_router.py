import os
import sys
# backend 경로를 sys.path에 추가
project_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(project_path)

import requests
from fastapi import APIRouter, HTTPException, status, Depends
from starlette.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.core.settings import get_settings
from app.crud.user_crud import get_user_by_email, create_user
from app.db.session import get_db
from app.schemas.user_schema import UserSchema

router = APIRouter()

@router.get("/google-login")
async def google_login(settings=Depends(get_settings)):
    url = (
        "https://accounts.google.com/o/oauth2/auth"
        "?response_type=code"
        f"&client_id={settings.GOOGLE_CLIENT_ID}"
        f"&redirect_uri={settings.REDIRECT_URI}"
        "&scope=openid%20email%20profile"
    )
    return RedirectResponse(url)

def exchange_code_for_token(code: str, settings):
    token_data = {
        "code": code,
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "redirect_uri": settings.REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    response = requests.post(settings.GOOGLE_TOKEN_ENDPOINT, data=token_data)
    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to exchange authorization code for tokens",
        )
    return response.json()

def get_user_profile(access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get("https://www.googleapis.com/oauth2/v3/userinfo", headers=headers)
    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to retrieve user information from Google",
        )
    return response.json()

@router.get("/callback")
async def callback(code: str, db: Session = Depends(get_db), settings=Depends(get_settings)):
    token_response = exchange_code_for_token(code, settings)
    access_token = token_response.get("access_token")
    profile_data = get_user_profile(access_token)

    google_email = profile_data['email']
    google_username = profile_data.get('name', google_email.split('@')[0])

    existing_user = get_user_by_email(db, google_email)
    if not existing_user:
        user_data = UserSchema(
            username=google_username,
            email=google_email,
            is_active=True,
            is_superuser=False,
        )
        create_user(db, user_data)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists",
        )

    redirect_url = "http://127.0.0.1:8000/docs"  # Redirect URL after login
    return RedirectResponse(redirect_url)