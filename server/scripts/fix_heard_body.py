import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # noqa: E402

import re  # noqa: E402
from bs4 import BeautifulSoup  # noqa: E402
from app.database import SessionLocal  # noqa: E402
from app.models import Chapter  # noqa: E402

DRY_RUN = False


def norm(s):
    return re.sub(r"\s+", " ", (s or "").strip())


def fix_heard(heard):
    """Убрать теги <strong> (оставив текст), обнулить пустое 'Услышано'."""
    if not heard:
        return heard, False
    soup = BeautifulSoup(heard, "lxml")
    changed = False
    # развернуть <strong>: заменить тег его содержимым
    for s in soup.find_all("strong"):
        s.unwrap()
        changed = True
    body = soup.body
    new = "".join(str(c) for c in body.contents).strip() if body else heard
    new = re.sub(r"\s+", " ", new)
    # пустое "Услышано" -> None
    if norm(BeautifulSoup(new, "lxml").get_text()) == "Услышано":
        return None, True
    return new, changed or (new != heard)


def fix_body(html):
    """Убрать абзац автора из тела."""
    soup = BeautifulSoup(html, "lxml")
    changed = False
    for p in soup.find_all("p"):
        txt = norm(p.get_text(" ", strip=True))
        if txt.startswith("Йегуда Лейб") and "Бааль Сулам" in txt:
            p.decompose()
            changed = True
    body = soup.body
    new = "".join(str(c) for c in body.contents).strip() if body else html
    return new, changed


def run():
    session = SessionLocal()
    changed = 0
    try:
        for ch in session.query(Chapter).order_by(Chapter.number).all():
            acts = []
            new_heard, h_ch = fix_heard(ch.heard)
            new_body, b_ch = fix_body(ch.content_html)
            if h_ch:
                acts.append(f"heard: {repr(ch.heard)[:40]} -> {repr(new_heard)[:40]}")
            if b_ch:
                acts.append("убран автор из тела")
            if not acts:
                continue
            changed += 1
            print(f"№{ch.number}: {'; '.join(acts)}")
            if not DRY_RUN:
                ch.heard = new_heard
                ch.content_html = new_body
        if not DRY_RUN:
            session.commit()
            print(f"\nЗАПИСАНО. Изменено: {changed}")
        else:
            print(f"\n[СУХОЙ ПРОГОН] Будет изменено: {changed}")
    finally:
        session.close()


if __name__ == "__main__":
    run()