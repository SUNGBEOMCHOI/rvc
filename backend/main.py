from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.routers import user_router
from app.api.routers import google_auth_router
from app.api.dependencies.singleton_voice_conversion_module import VoiceConversionManager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the Voice Conversion model
    VoiceConversionManager() # Singleton Voice Conversion instance 생성
    yield
    print("Shutting down the Voice Conversion model")

app = FastAPI(lifespan=lifespan)

origins = [
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router.router)
app.include_router(google_auth_router.router)