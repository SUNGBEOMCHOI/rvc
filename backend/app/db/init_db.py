from .base import Base, engine
from models import *  # 모델 모듈 임포트

def init_db():
    Base.metadata.create_all(bind=engine)
