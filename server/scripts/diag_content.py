import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # noqa: E402

import re  # noqa: E402
from bs4 import BeautifulSoup  # noqa: E402
from app.database import SessionLocal  # noqa: E402
from app.models import Chapter  # noqa: E402


def first_paragraphs_text(html, n=2):
    """Вернёт текст первых n абзацев <p> как список строк."""
    soup = BeautifulSoup(html, "lxml")
    ps = soup.find_all("p")[:n]
    return [re.sub(r"\s+", " ", p.get_text(" ", strip=True)) for p in ps]


def run():
    session = SessionLocal()
    try:
        chapters = session.query(Chapter).order_by(Chapter.number).all()
        print(f"Всего глав: {len(chapters)}\n")

        heard_in_body_no_field = []   # дата в теле, но heard ПУСТОЙ (терять нельзя!)
        heard_in_body_has_field = []  # дата в теле И heard заполнен (дубль, можно чистить)
        empty_heard_literal = []      # ровно "Услышано" без даты

        for ch in chapters:
            soup = BeautifulSoup(ch.content_html, "lxml")
            paras = [re.sub(r"\s+", " ", p.get_text(" ", strip=True)) for p in soup.find_all("p")]

            for p in paras[:3]:
                if p.startswith("Услышано"):
                    if p.strip() == "Услышано":
                        empty_heard_literal.append(ch.number)
                    elif ch.heard and ch.heard.strip():
                        heard_in_body_has_field.append((ch.number, p[:45], ch.heard[:45]))
                    else:
                        heard_in_body_no_field.append((ch.number, p[:45], repr(ch.heard)))
                    break

        print(f"=== Дата в теле + heard ПУСТОЙ (перенести, не терять): {len(heard_in_body_no_field)} ===")
        for num, body, field in heard_in_body_no_field[:20]:
            print(f"  №{num}: тело=«{body}» | heard={field}")

        print(f"\n=== Дата в теле + heard заполнен (дубль, чистим): {len(heard_in_body_has_field)} ===")
        for num, body, field in heard_in_body_has_field[:20]:
            print(f"  №{num}: тело=«{body}» | heard=«{field}»")

        print(f"\n=== Ровно 'Услышано' без даты: {len(empty_heard_literal)} ===")
        print("  ", empty_heard_literal)

    finally:
        session.close()


if __name__ == "__main__":
    run()