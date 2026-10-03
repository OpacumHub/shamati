import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# .env лежит в server/ (на уровень выше пакета app)
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass

# Зависимость для роутов: выдаёт сессию и закрывает её после запроса
def get_db():
    db = SessionLocal()          # открыли «разговор» с базой
    try:
        yield db                 # отдали сессию в роут (см. пояснение ниже)
    finally:
        db.close()               # после ответа — закрыли, всегда