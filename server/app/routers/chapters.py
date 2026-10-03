from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Chapter
from app.schemas import ChapterOut

# мини-app для роутов глав. prefix — общая приставка ко всем путям внутри.
# tags — группировка в /docs (просто для красоты документации)
router = APIRouter(prefix="/api/chapters", tags=["chapters"])


@router.get("/random", response_model=ChapterOut)
def get_random_chapter(db: Session = Depends(get_db)):
    # запрос: взять одну главу, упорядочив случайно
    chapter = db.query(Chapter).order_by(func.random()).first()
    if not chapter:
        raise HTTPException(status_code=404, detail="В базе нет глав")
    return chapter

@router.get("/{chapter_id}", response_model=ChapterOut)
def get_chapter(chapter_id: int, db: Session = Depends(get_db)):
    chapter = db.query(Chapter).filter(Chapter.id == chapter_id).first()
    if not chapter:
        raise HTTPException(status_code=404, detail="Глава не найдена")
    return chapter