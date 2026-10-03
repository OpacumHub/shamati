import os
import sys

# бутстрап: добавляем server/ в пути поиска, чтобы находился пакет app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # noqa: E402

import random  # noqa: E402  случайная пауза в диапазоне
import time  # noqa: E402  паузы между запросами

from app.database import SessionLocal  # noqa: E402  фабрика сессий к БД
from app.models import Chapter  # noqa: E402  ORM-модель chapters
from fetch_retry import fetch_chapter_with_retry  # noqa: E402  сосед по scripts/
from scraper import fetch_chapter_list  # noqa: E402  сосед по scripts/

MIN_DELAY = 1.0
MAX_DELAY = 2.5


def run():
    chapters = fetch_chapter_list()
    total = len(chapters)
    print(f"Глав в оглавлении: {total}\n")

    session = SessionLocal()
    added = skipped = failed = 0

    try:
        for i, ch in enumerate(chapters, start=1):
            prefix = f"[{i}/{total}] №{ch['number']}"

            if session.query(Chapter).filter_by(number=ch["number"]).first():
                skipped += 1
                print(f"{prefix} уже есть — пропуск")
                continue

            try:
                data, info = fetch_chapter_with_retry(ch)
                if not data:
                    failed += 1
                    print(f"{prefix} — {info}")
                    continue

                chapter = Chapter(
                    number=data["number"],
                    title=data["title"],
                    heard=data["heard"],
                    content_html=data["content_html"],
                    footnotes=data["footnotes"],
                    source_url=data["source_url"],
                )
                session.add(chapter)
                session.commit()
                added += 1
                print(f"{prefix} '{data['title'][:45]}' — {info}")

            except Exception as e:  # noqa: BLE001
                session.rollback()
                failed += 1
                print(f"{prefix} — ОШИБКА: {e}")

            time.sleep(random.uniform(MIN_DELAY, MAX_DELAY))

    finally:
        session.close()

    print(f"\nГотово. Добавлено: {added}, пропущено: {skipped}, ошибок: {failed}")


if __name__ == "__main__":
    run()