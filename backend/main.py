from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from app.db.session import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

@app.post("/items/")
def create_item(item: str, db: Session = Depends(get_db)):
    # 아이템 생성 로직
    pass
