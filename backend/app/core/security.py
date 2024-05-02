import os
import sys
# backend 경로를 sys.path에 추가
project_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_path)

import requests

from app.core.settings import get_settings
from app.errors import HttpErrorCode

settings = get_settings()

def exchange_code_for_token(code: str, settings):
    token_data = {
        "code": code,
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    response = requests.post(settings.GOOGLE_TOKEN_ENDPOINT, data=token_data)
    if response.status_code != 200:
        raise HttpErrorCode.EXCHANGE_TOKEN_ERROR()
    return response.json()

def get_user_profile(access_token: str, settings):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(settings.GOOGLE_USERINFO_ENDPOINT, headers=headers)
    if response.status_code != 200:
        raise HttpErrorCode.RETRIEVE_USER_INFO_ERROR()
    return response.json()