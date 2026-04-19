# IncognitoTgBot

Анонимный Telegram-бот для 1v1 чатов. Production-ready архитектура на Python 3.11+.

## Стек

| Компонент     | Технология              |
|---------------|-------------------------|
| Telegram Bot  | Aiogram 3.x             |
| Admin API     | FastAPI + WebSocket      |
| База данных   | MySQL 8 + SQLAlchemy 2  |
| Кеш / Очередь| Redis 7                 |
| Миграции      | Alembic                 |
| Контейнеры    | Docker + docker-compose |

## Структура проекта

```
app/
├── core/
│   └── config.py              # Настройки (pydantic-settings)
├── database/
│   ├── models.py              # SQLAlchemy модели
│   ├── session.py             # Async движок + get_session
│   ├── redis_client.py        # Redis connection pool
│   └── repositories/
│       ├── user_repo.py       # CRUD пользователей
│       └── chat_repo.py       # CRUD чатов и сообщений
├── services/
│   └── matcher.py             # Redis-очередь + логика матчинга
├── bot/
│   ├── handlers/
│   │   ├── start.py           # /start, регистрация
│   │   ├── profile.py         # Профиль пользователя
│   │   └── chat.py            # Поиск, чат, пересылка сообщений
│   ├── keyboards/
│   │   └── main.py            # Reply и Inline клавиатуры
│   ├── middlewares/
│   │   ├── ban_check.py       # Проверка бана
│   │   └── anti_spam.py       # Rate limiting (sliding window)
│   └── main.py                # Точка входа бота
└── admin_api/
    └── main.py                # FastAPI + WebSocket admin
```

## Быстрый старт

### 1. Клонирование и настройка

```bash
git clone <repo>
cd incognito_bot
cp .env.example .env
# Отредактируй .env — впиши BOT_TOKEN и пароли
```

### 2. Docker (рекомендуется)

```bash
docker-compose up -d
```

Бот и Admin API запустятся автоматически после MySQL и Redis.

### 3. Локально без Docker

```bash
python -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Убедись что MySQL и Redis запущены
python -m app.bot.main       # Бот
python run_admin.py          # Admin API (в другом терминале)
```

## Миграции (Alembic)

```bash
# Создать первую миграцию
alembic revision --autogenerate -m "initial"

# Применить
alembic upgrade head

# Откатить
alembic downgrade -1
```

## Admin API

Базовый URL: `http://localhost:8000`

Все запросы требуют заголовок:
```
X-Admin-Key: <ADMIN_SECRET_KEY из .env>
```

| Метод  | Путь                            | Описание                    |
|--------|---------------------------------|-----------------------------|
| GET    | `/api/stats`                    | Общая статистика            |
| GET    | `/api/users?limit=50&offset=0`  | Список пользователей        |
| POST   | `/api/users/{telegram_id}/ban`  | Бан / разбан пользователя  |
| GET    | `/api/chats?active_only=true`   | Список чатов                |
| GET    | `/api/chats/{id}/messages`      | Сообщения конкретного чата |
| WS     | `/ws/events`                    | Realtime события            |

### WebSocket события

```json
{ "event": "new_chat",           "chat_id": 1, "user1_id": 123, "user2_id": 456 }
{ "event": "new_message",        "chat_id": 1, "sender_id": 123, "type": "text" }
{ "event": "user_status_changed","telegram_id": 123, "status": "banned" }
```

## Функционал бота

| Кнопка / Команда     | Действие                              |
|----------------------|---------------------------------------|
| `/start`             | Регистрация, выдача internal_id       |
| `👤 Мой профиль`     | Статистика и информация               |
| `🔍 Найти собеседника`| Вход в очередь, ожидание пары        |
| `❌ Отменить поиск`  | Выход из очереди                      |
| `🚫 Завершить чат`   | Завершение с подтверждением           |

### Поддерживаемые типы сообщений

- Текст, Фото, Видео, Голосовые, Стикеры, Документы

## Переменные окружения

| Переменная           | Описание                        | По умолчанию |
|----------------------|---------------------------------|--------------|
| `BOT_TOKEN`          | Токен Telegram бота             | —            |
| `MYSQL_HOST`         | Хост MySQL                      | localhost    |
| `MYSQL_PASSWORD`     | Пароль MySQL                    | —            |
| `MYSQL_DB`           | Имя базы данных                 | incognito_bot|
| `REDIS_HOST`         | Хост Redis                      | localhost    |
| `ADMIN_SECRET_KEY`   | Ключ для Admin API              | —            |
| `SPAM_MAX_MESSAGES`  | Макс. сообщений за окно         | 10           |
| `SPAM_WINDOW_SECONDS`| Окно антиспама (сек)            | 10           |
