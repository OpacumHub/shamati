import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))
import re

import httpx
from bs4 import BeautifulSoup
from scraper import CHAPTER_URL, HEADERS, fetch_chapter_list

num = int(sys.argv[1])                     # sys.argv[1] — первый аргумент из командной строки
chapters = fetch_chapter_list()
# next(генератор, None) — берёт первый подходящий элемент или None
ch = next((c for c in chapters if c["number"] == num), None)
if not ch:
    print("Нет такой главы"); sys.exit()

url = CHAPTER_URL.format(id=ch["id"])
print("Глава", num, "|", ch["name"], "| id:", ch["id"])
print("URL:", url)

resp = httpx.get(url, headers=HEADERS, timeout=60, follow_redirects=True)
print("HTTP код:", resp.status_code, "| финальный URL:", str(resp.url))
print("размер HTML:", len(resp.text))

soup = BeautifulSoup(resp.text, "lxml")
node = soup.find(id="roodNodeOfShareText")
print("контейнер найден:", node is not None)

if node:
    print("<p> внутри:", len(node.find_all("p")), "| символов:", len(node.get_text(' ', strip=True)))
    print("--- HTML контейнера, первые 800 симв ---")
    print(str(node)[:800])
else:
    # контейнера нет — посмотрим, что за текст вообще на странице (пропустив меню сверху)
    page = re.sub(r"\s+", " ", soup.get_text(" ", strip=True))
    print("--- текст страницы, символы 400–1400 ---")
    print(page[400:1400])