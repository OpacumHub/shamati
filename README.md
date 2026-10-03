# Шамати — случайная глава

Веб-приложение для чтения книги «Шамати» (Бааль Сулам). На главной — «статья дня»
(детерминированный выбор на основе недельной главы Торы), плюс режим случайной главы
и прямые ссылки на конкретные главы.

Боевая версия: https://shamati.zencodecraft.ru

## Стек

- **Frontend:** Vue 3 (Composition API) + Vite + Naive UI + Vue Router + axios
- **Backend:** Python + FastAPI (SQLAlchemy 2.0, Alembic)
- **БД:** PostgreSQL
- **Сервер:** Ubuntu + nginx (reverse-proxy + SPA-fallback), systemd-служба для бэкенда,
  панель ISPmanager

## Как работает «статья дня»

Детерминированный выбор одной главы на сутки, единой для всех:
- номер недельной главы Торы (параша, 1..54) берётся из Hebcal API;
- `seed = номер_параши * 7 + день_недели`;
- `номер_главы = seed % кол-во_глав + 1`.

Результат кэшируется в памяти на сутки. Если Hebcal недоступен — запасной seed от даты.
Эндпоинт: `GET /api/chapters/daily`.

## Структура проекта

```
shamati/
├── client/              # фронтенд (Vue + Vite)
│   ├── src/
│   │   ├── components/   # ChapterContent, AppHeader
│   │   ├── views/        # HomeView, ChapterView
│   │   ├── router/       # маршруты Vue Router
│   │   ├── stores/       # общее состояние главы
│   │   └── assets/       # глобальные стили
│   └── vite.config.js    # прокси /api -> бэкенд в dev
├── server/              # бэкенд (FastAPI)
│   ├── app/
│   │   ├── main.py       # точка входа, подключение роутеров
│   │   ├── database.py   # engine, сессии, get_db
│   │   ├── models.py     # ORM-модель Chapter
│   │   ├── schemas.py    # Pydantic-схемы (ChapterOut)
│   │   ├── daily.py      # логика "статьи дня" (Hebcal + seed + кэш)
│   │   └── routers/
│   │       └── chapters.py
│   ├── scripts/          # наполнение БД
│   │   ├── scraper.py
│   │   ├── fetch_retry.py
│   │   └── import_chapters.py
│   ├── migrations/       # Alembic
│   ├── dev/              # архив диагностических скриптов
│   ├── .env              # секреты (НЕ в git)
│   └── requirements.txt
└── deploy-frontend.sh
```