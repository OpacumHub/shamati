from datetime import datetime

from pydantic import BaseModel, ConfigDict


class Footnote(BaseModel):
    """Одна сноска: номер и текст."""
    n: int
    text: str


class ChapterOut(BaseModel):
    """Глава в том виде, в каком API отдаёт её наружу."""
    # разрешаем Pydantic читать данные прямо из ORM-объекта (не только из dict)
    model_config = ConfigDict(from_attributes=True)

    id: int
    number: int
    title: str
    heard: str | None            # может отсутствовать -> допускаем None
    content_html: str
    footnotes: list[Footnote] | None
    source_url: str | None
    created_at: datetime