import re
import datetime
import httpx
import random

HEBCAL_URL = "https://www.hebcal.com/hebcal"

# кэш в памяти процесса: храним (дата, номер_главы)
_cache = {"date": None, "chapter_number": None}


def get_parasha_number(today):
    """
    Номер недельной главы Торы (1..54) для недели, в которую попадает today.
    Берём ближайшую субботу чтения от сегодня и достаём номер из поля link.
    Возвращает int или None, если Hebcal недоступен.
    """
    start = today.isoformat()
    end = (today + datetime.timedelta(days=8)).isoformat()  # неделя+ вперёд
    params = {
        "cfg": "json", "v": "1",
        "start": start, "end": end,
        "s": "on", "c": "off", "geo": "none", "leyning": "off",
    }
    try:
        resp = httpx.get(HEBCAL_URL, params=params, timeout=10)
        resp.raise_for_status()
        items = resp.json().get("items", [])
        for item in items:
            if item.get("category") == "parashat":
                # link вида https://hebcal.com/s/5787/1?... -> берём число после года
                m = re.search(r"/s/\d+/(\d+)", item.get("link", ""))
                if m:
                    return int(m.group(1))
        return None
    except Exception as e:
        print(f"Hebcal недоступен: {e}")
        return None


def compute_daily_number(today, total_chapters):
    """
    Детерминированный номер главы на сегодня.
    seed = номер_параши * 7 + день_недели; глава = seed % total + 1.
    Если Hebcal недоступен — запасной seed только от даты (главная не падает).
    """
    weekday = today.weekday()
    parasha = get_parasha_number(today)
    if parasha is not None:
        seed = parasha * 7 + weekday
    else:
        seed = today.toordinal()
    rng = random.Random(seed)              # seed -> генератор
    return rng.randint(1, total_chapters)  # детерминированно-случайная глава


def get_daily_chapter_number(total_chapters):
    """Номер главы дня с суточным кэшем в памяти."""
    today = datetime.date.today()           # по времени сервера
    if _cache["date"] == today and _cache["chapter_number"] is not None:
        return _cache["chapter_number"]     # уже считали сегодня — отдаём из кэша

    number = compute_daily_number(today, total_chapters)
    _cache["date"] = today
    _cache["chapter_number"] = number
    return number