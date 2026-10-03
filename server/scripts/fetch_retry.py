import time
import random
import httpx
from bs4 import BeautifulSoup
from scraper import HEADERS, CHAPTER_URL, parse_article


def fetch_chapter_with_retry(ch, attempts=4):
    """
    Качает и парсит главу, повторяя попытки, если сервер вернул каркас без текста.
    Возвращает (data, info) — data это результат parse_article или None,
    info — строка с диагностикой для лога.
    """
    url = CHAPTER_URL.format(id=ch["id"])
    last_reason = "неизвестно"

    for attempt in range(1, attempts + 1):          # range(1, 5) => 1,2,3,4
        try:
            resp = httpx.get(url, headers=HEADERS, timeout=60, follow_redirects=True)
            resp.raise_for_status()

            # быстрая проверка: пришёл ли реальный контент
            soup = BeautifulSoup(resp.text, "lxml")
            node = soup.find(id="roodNodeOfShareText")
            has_body = node is not None and len(node.find_all("p")) > 0

            if has_body:
                data = parse_article(resp.text, ch["name"], ch["number"], url)
                if data and data["content_html"]:
                    return data, f"ок с попытки {attempt}"
            # каркас без текста — не повезло с этой попыткой
            last_reason = f"каркас без текста (размер {len(resp.text)})"

        except Exception as e:
            last_reason = f"ошибка запроса: {e}"

        # не последняя попытка — ждём подольше и пробуем снова
        if attempt < attempts:
            time.sleep(random.uniform(2.0, 4.0))

    return None, f"не удалось за {attempts} попыток ({last_reason})"