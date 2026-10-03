import re
import httpx
from bs4 import BeautifulSoup

SQDATA_URL = "https://kabbalahmedia.info/backend/sqdata?ui_language=ru&content_languages=ru"
SHAMATI_ID = "qMUUn22b"
CHAPTER_URL = "https://kabbalahmedia.info/ru/sources/{id}"
HEADERS = {"User-Agent": "curl/8.5.0"}  # не-браузер → сервер отдаёт HTML с текстом


def normalize_ws(el):
    for t in el.find_all(string=True):
        t.replace_with(re.sub(r"\s+", " ", t))


def find_node(nodes, target_id):
    for node in nodes:
        if node.get("id") == target_id:
            return node
        if node.get("children"):
            found = find_node(node["children"], target_id)
            if found:
                return found
    return None


def fetch_chapter_list():
    resp = httpx.get(SQDATA_URL, headers=HEADERS, timeout=60, follow_redirects=True)
    resp.raise_for_status()
    shamati = find_node(resp.json()["sources"], SHAMATI_ID)
    if not shamati:
        raise RuntimeError("Сборник Шамати не найден в sqdata")
    out = []
    for c in shamati.get("children", []):
        if c.get("type") == "ARTICLE":
            out.append({
                "id": c["id"],
                "number": int(c["number"]) if c.get("number") else None,
                "name": re.sub(r"\s+", " ", (c.get("name") or "").strip()),
            })
    return out


def parse_article(html, name, number, source_url):
    soup = BeautifulSoup(html, "lxml")
    node = soup.find(id="roodNodeOfShareText")
    if not node:
        return None

    footnotes = []
    fnsec = node.find("section", class_="footnotes")
    if fnsec:
        for i, li in enumerate(fnsec.select("ol > li"), start=1):
            for back in li.select("a.footnote-back"):
                back.decompose()
            m = re.match(r"fn(\d+)", li.get("id", ""))
            normalize_ws(li)
            footnotes.append({"n": int(m.group(1)) if m else i,
                              "text": li.get_text(" ", strip=True)})
        fnsec.decompose()

    heard = None
    h2 = node.find("h2")
    if h2:
        for ref in h2.select("a.footnote-ref"):
            ref.decompose()
        normalize_ws(h2)
        heard = h2.get_text(" ", strip=True)

    for ref in node.select("a.footnote-ref"):
        sup = ref.find("sup")
        num = re.sub(r"\D", "", (sup.get_text() if sup else ref.get_text()) or "")
        new_sup = soup.new_tag("sup")
        a = soup.new_tag("a", href=f"#fn-{num}")
        a.string = num
        new_sup.append(a)
        ref.replace_with(new_sup)

    parts = []
    for p in node.find_all("p"):
        normalize_ws(p)
        parts.append(str(p))

    return {
        "number": number,
        "title": name,
        "heard": heard,
        "content_html": "\n".join(parts),
        "footnotes": footnotes,
        "source_url": source_url,
    }


def fetch_and_parse(chapter):
    url = CHAPTER_URL.format(id=chapter["id"])
    resp = httpx.get(url, headers=HEADERS, timeout=60, follow_redirects=True)
    resp.raise_for_status()
    return parse_article(resp.text, chapter["name"], chapter["number"], url)


if __name__ == "__main__":
    chapters = fetch_chapter_list()
    print("всего глав:", len(chapters))

    ch = chapters[0]
    r = fetch_and_parse(ch)
    print("\n=== ГЛАВА", ch["number"], "===")
    print("title       :", r["title"])
    print("heard       :", r["heard"])
    print("footnotes   :", len(r["footnotes"]), "->", [f["n"] for f in r["footnotes"]])
    print("content_html:", len(r["content_html"]), "символов")
    print("--- первые 300 символов тела ---")
    print(r["content_html"][:300])