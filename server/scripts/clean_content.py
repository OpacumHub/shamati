import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # noqa: E402

import re  # noqa: E402
from bs4 import BeautifulSoup  # noqa: E402
from app.database import SessionLocal  # noqa: E402
from app.models import Chapter  # noqa: E402

# режим: True = только показать, False = реально записать
DRY_RUN = False


def norm(s):
    return re.sub(r"\s+", " ", (s or "").strip())


def clean_chapter(ch):
    """
    Возвращает (new_html, new_heard, actions) — что станет с телом/heard и список действий.
    Ничего не пишет в объект.
    """
    soup = BeautifulSoup(ch.content_html, "lxml")
    ps = soup.find_all("p")
    actions = []
    new_heard = ch.heard

    title_variants = {norm(ch.title), norm(f"{ch.number}. {ch.title}")}

    # смотрим только первые 3 абзаца — мусор всегда там
    for p in ps[:3]:
        txt = norm(p.get_text(" ", strip=True))
        if not txt:
            continue

        # (A) абзац = дубль заголовка -> удалить
        if txt in title_variants:
            p.decompose()
            actions.append(f"удалён дубль заголовка: «{txt[:40]}»")
            continue

        # (B) абзац начинается с "Услышано"
        if txt.startswith("Услышано"):
            # чистое "Услышано" без даты -> просто удалить
            if txt == "Услышано":
                p.decompose()
                actions.append("удалён пустой «Услышано»")
                continue
            # есть дата. если heard пуст -> перенести дату в heard, затем удалить абзац
            if not norm(new_heard):
                # убрать висячий номер сноски: после "г." или после года, в т.ч. в середине
                date_text = re.sub(r"(г\.)\s*\d+\b", r"\1", txt)      # "г. 1" -> "г."
                date_text = re.sub(r"(\d{4})\s+\d+\b", r"\1", date_text)  # "1943 1" -> "1943"
                date_text = re.sub(r"\s*\d+\s*$", "", date_text)      # хвостовой номер, если остался
                date_text = re.sub(r"\s{2,}", " ", date_text).strip() # двойные пробелы
                date_text = re.sub(r"\s+,", ",", date_text)           # пробел перед запятой
                new_heard = date_text
                actions.append(f"перенесено в heard: «{date_text[:40]}»")
            else:
                actions.append(f"дубль даты, heard уже есть: «{txt[:40]}»")
            p.decompose()
            continue

    # собираем тело обратно: берём внутренности <body>, которое добавил парсер
    body = soup.body
    new_html = "".join(str(c) for c in body.contents) if body else str(soup)
    new_html = new_html.strip()

    return new_html, new_heard, actions


def run():
    session = SessionLocal()
    changed = 0
    try:
        chapters = session.query(Chapter).order_by(Chapter.number).all()
        for ch in chapters:
            new_html, new_heard, actions = clean_chapter(ch)
            if not actions:
                continue
            changed += 1
            print(f"№{ch.number}: {'; '.join(actions)}")
            if not DRY_RUN:
                ch.content_html = new_html
                ch.heard = new_heard
        if not DRY_RUN:
            session.commit()
            print(f"\nЗАПИСАНО. Изменено глав: {changed}")
        else:
            print(f"\n[СУХОЙ ПРОГОН] Будет изменено глав: {changed}. Записи НЕ было.")
    finally:
        session.close()


if __name__ == "__main__":
    run()