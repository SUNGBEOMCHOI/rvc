import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    GOOGLE_CLIENT_ID: str = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET: str = os.getenv("GOOGLE_CLIENT_SECRET")
    GOOGLE_AUTHORIZATION_ENDPOINT: str = "https://accounts.google.com/o/oauth2/auth"
    GOOGLE_TOKEN_ENDPOINT: str = "https://accounts.google.com/o/oauth2/token"
    GOOGLE_USERINFO_ENDPOINT: str = "https://www.googleapis.com/oauth2/v3/userinfo"
    GOOGLE_REDIRECT_URI: str = "http://127.0.0.1:8000/callback"

def get_settings():
    return Settings()