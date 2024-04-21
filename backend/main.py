from fastapi import Depends, FastAPI, HTTPException
from starlette.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.db.session import get_db

app = FastAPI()

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

@app.post("/items/")
def create_item(item: str, db: Session = Depends(get_db)):
    # 아이템 생성 로직
    pass
