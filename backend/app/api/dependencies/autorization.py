import os
import sys
project_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.append(project_path)

from fastapi.security import OAuth2AuthorizationCodeBearer

from app.core.settings import get_settings

settings = get_settings()

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=settings.GOOGLE_AUTHORIZATION_ENDPOINT,
    tokenUrl=settings.GOOGLE_TOKEN_ENDPOINT,
)