from fastapi import FastAPI
from sqlalchemy import text

from app.database import engine
from app.routers import chapters

app = FastAPI()

# подключаем роуты глав к приложению
app.include_router(chapters.router)

@app.get("/api/health")
def health():
    return {"ok": True}

@app.get("/api/db-check")
def db_check():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT version()"))
        return {"db": result.scalar()}