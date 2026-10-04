import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # noqa: E402

from app.database import SessionLocal  # noqa: E402
from app.models import Chapter  # noqa: E402

BASE_URL = "https://shamati.ru"
# путь до public/ фронта (из server/scripts/ поднимаемся к корню проекта -> client/public)
OUTPUT = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "client", "public", "sitemap.xml",
)


def run():
    session = SessionLocal()
    try:
        chapters = session.query(Chapter).order_by(Chapter.number).all()

        lines = ['<?xml version="1.0" encoding="UTF-8"?>']
        lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

        # главная — высший приоритет, меняется ежедневно (статья дня)
        lines.append("  <url>")
        lines.append(f"    <loc>{BASE_URL}/</loc>")
        lines.append("    <changefreq>daily</changefreq>")
        lines.append("    <priority>1.0</priority>")
        lines.append("  </url>")

        # страницы глав
        for ch in chapters:
            lines.append("  <url>")
            lines.append(f"    <loc>{BASE_URL}/chapter/{ch.id}</loc>")
            lines.append("    <changefreq>yearly</changefreq>")
            lines.append("    <priority>0.8</priority>")
            lines.append("  </url>")

        lines.append("</urlset>")

        with open(OUTPUT, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        print(f"sitemap.xml создан: {OUTPUT}")
        print(f"URL в карте: {len(chapters) + 1} (главная + {len(chapters)} глав)")
    finally:
        session.close()


if __name__ == "__main__":
    run()