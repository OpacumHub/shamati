import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))
import random
import time

import httpx
from bs4 import BeautifulSoup
from scraper import CHAPTER_URL, HEADERS, fetch_chapter_list

# номера, которые не извлеклись (из твоего лога)
FAILED = [7, 10, 11, 20, 35, 37, 38, 44, 50, 58, 74, 91, 98,
          105, 130, 182, 190, 208, 210, 225, 235, 248]

# словарь {номер: глава} — быстрый доступ по номеру.
# {c["number"]: c for c in ...} — это dict comprehension (генератор словаря)
chapters = {c["number"]: c for c in fetch_chapter_list()}

for num in FAILED:
    ch = chapters.get(num)                 # .get() вернёт None, если ключа нет (без ошибки)
    if not ch:
        print(f"№{num}: нет в оглавлении")
        continue
    url = CHAPTER_URL.format(id=ch["id"])
    try:
        resp = httpx.get(url, headers=HEADERS, timeout=60, follow_redirects=True)
        soup = BeautifulSoup(resp.text, "lxml")
        node = soup.find(id="roodNodeOfShareText")
        p_count = len(node.find_all("p")) if node else 0
        txt = len(node.get_text(" ", strip=True)) if node else 0
        has = "да" if node else "НЕТ"
        print(f"№{num}: код={resp.status_code} размер={len(resp.text)} "
              f"контейнер={has} <p>={p_count} текст={txt} | {ch['name'][:35]}")
    except Exception as e:
        print(f"№{num}: ОШИБКА {e}")
    time.sleep(random.uniform(1.0, 2.0))    # пауза, как в парсере